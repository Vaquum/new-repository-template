import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const repoRoot = path.resolve(path.dirname(scriptPath), '..', '..');
const siteRoot = path.resolve(repoRoot, 'docs-site');
const outRoot = path.resolve(siteRoot, '.generated', 'docs');
const staticRoot = path.resolve(siteRoot, '.generated', 'static');
const profile = JSON.parse(
  await fs.readFile(path.resolve(siteRoot, 'product-docs.json'), 'utf8')
);
const docsMap = JSON.parse(
  await fs.readFile(path.resolve(siteRoot, 'docs-map.json'), 'utf8')
);
const documents = docsMap.documents;
const sections = docsMap.sections;
const repoBlobBaseUrl = `${profile.sourceRepoUrl}/blob/main`;
const repoEditBaseUrl = `${profile.sourceRepoUrl}/edit/main`;
const repoTreeBaseUrl = `${profile.sourceRepoUrl}/tree/main`;

function normalizePath(value) {
  return value.split(path.sep).join('/');
}

function requireString(object, key, context) {
  const value = object[key];
  if (typeof value !== 'string' || value.length === 0) {
    throw new Error(`${context}.${key} must be a non-empty string`);
  }
  return value;
}

function assertUnique(values, label) {
  if (new Set(values).size !== values.length) {
    throw new Error(`${label} values must be unique`);
  }
}

function validateConfiguration() {
  for (const key of ['productId', 'productName', 'tagline', 'siteUrl', 'basePath', 'sourceRepoUrl']) {
    requireString(profile, key, 'product-docs.json');
  }
  if (!Array.isArray(sections) || !Array.isArray(documents)) {
    throw new Error('docs-map.json sections and documents must be arrays');
  }
  if (sections.length !== 5) {
    throw new Error('docs-map.json must define the five standard sections');
  }
  assertUnique(sections.map((section) => requireString(section, 'dir', 'section')), 'section dir');
  assertUnique(sections.map((section) => requireString(section, 'slug', 'section')), 'section slug');
  assertUnique(documents.map((doc) => requireString(doc, 'source', 'document')), 'document source');
  assertUnique(documents.map((doc) => requireString(doc, 'dest', 'document')), 'document dest');
  assertUnique(documents.map((doc) => requireString(doc, 'slug', 'document')), 'document slug');

  for (const doc of documents) {
    const sourcePath = path.resolve(repoRoot, doc.source);
    const destPath = path.resolve(outRoot, doc.dest);
    if (
      !sourcePath.startsWith(`${repoRoot}${path.sep}`)
      || !fsSync.existsSync(sourcePath)
      || !fsSync.statSync(sourcePath).isFile()
    ) {
      throw new Error(`document source is missing or outside the repository: ${doc.source}`);
    }
    if (!destPath.startsWith(`${outRoot}${path.sep}`)) {
      throw new Error(`document destination is outside generated docs: ${doc.dest}`);
    }
  }
}

const mappingBySource = new Map(
  documents.map((doc) => [normalizePath(doc.source), doc])
);

async function ensureDir(directory) {
  await fs.mkdir(directory, {recursive: true});
}

async function writeJson(filePath, value) {
  await ensureDir(path.dirname(filePath));
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function buildFrontMatter(doc) {
  const lines = ['---', `slug: ${JSON.stringify(doc.slug)}`];
  if (doc.title) {
    lines.push(`title: ${JSON.stringify(doc.title)}`);
  }
  if (typeof doc.sidebarPosition === 'number') {
    lines.push(`sidebar_position: ${doc.sidebarPosition}`);
  }
  if (doc.sidebarLabel) {
    lines.push(`sidebar_label: ${JSON.stringify(doc.sidebarLabel)}`);
  }
  if (doc.dest === 'index.md') {
    lines.push('pagination_next: null', 'pagination_prev: null');
  }
  lines.push(
    `custom_edit_url: ${JSON.stringify(`${repoEditBaseUrl}/${doc.source}`)}`,
    '---',
    ''
  );
  return lines.join('\n');
}

function resolveDocLink(fromSource, target) {
  if (!target || /^(https?:|mailto:|#|\/)/.test(target)) {
    return target;
  }
  const [targetPath, targetHash] = target.split('#');
  const resolvedSource = normalizePath(
    path.posix.normalize(path.posix.join(path.posix.dirname(normalizePath(fromSource)), targetPath))
  );
  let targetDoc = mappingBySource.get(resolvedSource);
  if (!targetDoc && !path.posix.extname(resolvedSource)) {
    targetDoc = mappingBySource.get(normalizePath(path.posix.join(resolvedSource, 'README.md')));
  }
  if (!targetDoc) {
    const repoFsPath = path.resolve(repoRoot, resolvedSource);
    if (!fsSync.existsSync(repoFsPath)) {
      return target;
    }
    const repoUrlBase = fsSync.statSync(repoFsPath).isDirectory()
      ? repoTreeBaseUrl
      : repoBlobBaseUrl;
    return targetHash
      ? `${repoUrlBase}/${resolvedSource}#${targetHash}`
      : `${repoUrlBase}/${resolvedSource}`;
  }
  const currentDoc = mappingBySource.get(normalizePath(fromSource));
  const fromDest = currentDoc ? normalizePath(currentDoc.dest) : '';
  const toDest = normalizePath(targetDoc.dest);
  const relative = normalizePath(
    path.posix.relative(path.posix.dirname(fromDest), toDest)
  ) || path.posix.basename(toDest);
  return targetHash ? `${relative}#${targetHash}` : relative;
}

function rewriteLinks(content, fromSource) {
  return content.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, target) =>
    `[${label}](${resolveDocLink(fromSource, target.trim())})`
  );
}

function rewriteOutsideFences(content, transform) {
  let output = '';
  let index = 0;
  let inFence = false;
  let plainStart = 0;
  while (index < content.length) {
    if (content.startsWith('```', index)) {
      if (plainStart < index) {
        const segment = content.slice(plainStart, index);
        output += inFence ? segment : transform(segment);
      }
      inFence = !inFence;
      output += '```';
      index += 3;
      plainStart = index;
      continue;
    }
    index += 1;
  }
  const tail = content.slice(plainStart);
  output += inFence ? tail : transform(tail);
  return output;
}

function rewriteOutsideInlineCode(content, transform) {
  let output = '';
  let index = 0;
  let plainStart = 0;
  while (index < content.length) {
    if (content[index] === '`') {
      if (plainStart < index) {
        output += transform(content.slice(plainStart, index));
      }
      const close = content.indexOf('`', index + 1);
      if (close === -1) {
        output += content.slice(index);
        return output;
      }
      output += content.slice(index, close + 1);
      index = close + 1;
      plainStart = index;
      continue;
    }
    index += 1;
  }
  output += transform(content.slice(plainStart));
  return output;
}

export function rewriteOutsideCode(content, transform) {
  return rewriteOutsideFences(
    content,
    (chunk) => rewriteOutsideInlineCode(chunk, transform)
  );
}

function rewriteLinksOutsideCode(content, fromSource) {
  return rewriteOutsideFences(content, (chunk) => {
    const inlineCode = [];
    const masked = chunk.replace(/`[^`]*(?:`|$)/g, (match) => {
      const marker = `\u0000INLINE_CODE_${inlineCode.length}\u0000`;
      inlineCode.push(match);
      return marker;
    });
    const rewritten = rewriteLinks(masked, fromSource);
    return inlineCode.reduce(
      (result, code, index) =>
        result.replace(`\u0000INLINE_CODE_${index}\u0000`, code),
      rewritten
    );
  });
}

export function normalizeForMdx(content, fromSource) {
  const rewrittenLinks = rewriteLinksOutsideCode(content, fromSource);
  return rewriteOutsideCode(rewrittenLinks, (chunk) =>
    chunk
      .replace(/<p align="center">([\s\S]*?)<\/p>/g, '<div align="center">$1</div>')
      .replace(/<br>/g, '<br />')
      .replace(/<hr>/g, '<hr />')
      .replace(/<img([^>]*?)(?<!\/)>/g, '<img$1 />')
      .replace(
        /\{(DISPLAY_NAME|ONE_SENTENCE_DESCRIPTION|REPOSITORY_NAME|REPOSITORY_OWNER)\}/g,
        '&#123;$1&#125;'
      )
  );
}

async function copyDoc(doc) {
  const sourcePath = path.resolve(repoRoot, doc.source);
  const destPath = path.resolve(outRoot, doc.dest);
  const raw = await fs.readFile(sourcePath, 'utf8');
  const output = `${buildFrontMatter(doc)}${normalizeForMdx(raw, doc.source)}`;
  await ensureDir(path.dirname(destPath));
  await fs.writeFile(destPath, output);
}

async function writeCategoryFiles() {
  for (const category of sections) {
    await writeJson(path.resolve(outRoot, category.dir, '_category_.json'), {
      label: category.label,
      position: category.position,
      collapsible: true,
      collapsed: true,
      link: {
        type: 'generated-index',
        slug: category.slug,
        title: category.label,
        description: category.description,
      },
    });
  }
}

async function writeRobots() {
  const basePath = profile.basePath.endsWith('/') ? profile.basePath : `${profile.basePath}/`;
  await ensureDir(staticRoot);
  await fs.writeFile(
    path.resolve(staticRoot, 'robots.txt'),
    `User-agent: *\nAllow: /\nSitemap: ${profile.siteUrl}${basePath}sitemap.xml\n`
  );
}

async function main() {
  validateConfiguration();
  await fs.rm(path.resolve(siteRoot, '.generated'), {recursive: true, force: true});
  await ensureDir(outRoot);
  await writeCategoryFiles();
  for (const doc of documents) {
    await copyDoc(doc);
  }
  await writeRobots();
}

if (process.argv[1] === scriptPath) {
  await main();
}
