import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const siteRoot = path.resolve(path.dirname(scriptPath), '..');
const buildRoot = path.resolve(siteRoot, 'build');
const profile = JSON.parse(
  await fs.readFile(path.resolve(siteRoot, 'product-docs.json'), 'utf8')
);
const docsMap = JSON.parse(
  await fs.readFile(path.resolve(siteRoot, 'docs-map.json'), 'utf8')
);
const maxJavaScriptBytes = 1_500_000;
const maxCssBytes = 400_000;

function routeFile(slug) {
  if (slug === '/') {
    return 'index.html';
  }
  return `${slug.replace(/^\//, '')}.html`;
}

const expectedRoutes = new Set([
  ...docsMap.sections.map((section) => routeFile(section.slug)),
  ...docsMap.documents.map((document) => routeFile(document.slug)),
  'search.html',
]);
for (const route of expectedRoutes) {
  await fs.access(path.resolve(buildRoot, route));
}

const sitemap = await fs.readFile(path.resolve(buildRoot, 'sitemap.xml'), 'utf8');
const sitemapCount = [...sitemap.matchAll(/<loc>/g)].length;
if (sitemapCount !== expectedRoutes.size) {
  throw new Error(`sitemap has ${sitemapCount} URLs, expected ${expectedRoutes.size}`);
}
const robots = await fs.readFile(path.resolve(buildRoot, 'robots.txt'), 'utf8');
const basePath = profile.basePath.endsWith('/') ? profile.basePath : `${profile.basePath}/`;
const expectedSitemap = `${profile.siteUrl}${basePath}sitemap.xml`;
if (!robots.includes(expectedSitemap)) {
  throw new Error(`robots.txt must name ${expectedSitemap}`);
}
const searchIndex = await fs.readFile(path.resolve(buildRoot, 'search-index.json'), 'utf8');
if (!searchIndex.includes('Documentation system contract')) {
  throw new Error('search index does not contain the documentation contract');
}

const assetRoot = path.resolve(buildRoot, 'assets');
const assetPaths = [];
async function collect(directory) {
  for (const entry of await fs.readdir(directory, {withFileTypes: true})) {
    const entryPath = path.resolve(directory, entry.name);
    if (entry.isDirectory()) {
      await collect(entryPath);
    } else {
      assetPaths.push(entryPath);
    }
  }
}
await collect(assetRoot);
const largestJavaScript = Math.max(
  ...await Promise.all(
    assetPaths.filter((file) => file.endsWith('.js')).map(async (file) => (await fs.stat(file)).size)
  )
);
const largestCss = Math.max(
  ...await Promise.all(
    assetPaths.filter((file) => file.endsWith('.css')).map(async (file) => (await fs.stat(file)).size)
  )
);
if (largestJavaScript > maxJavaScriptBytes || largestCss > maxCssBytes) {
  throw new Error(`asset budget exceeded: js=${largestJavaScript}, css=${largestCss}`);
}
process.stdout.write(
  `Build verified: ${expectedRoutes.size} routes, js<=${largestJavaScript}, css<=${largestCss}\n`
);
