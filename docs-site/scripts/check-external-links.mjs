import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const repoRoot = path.resolve(path.dirname(scriptPath), '..', '..');
const docsMap = JSON.parse(
  await fs.readFile(path.resolve(repoRoot, 'docs-site', 'docs-map.json'), 'utf8')
);

export function extractExternalLinks(text) {
  const links = new Set();
  const patterns = [
    /\[[^\]]*]\((https?:\/\/[^)\s]+)\)/g,
    /(?:href|src)=["'](https?:\/\/[^"']+)["']/g,
  ];
  for (const pattern of patterns) {
    for (const match of text.matchAll(pattern)) {
      links.add(match[1]);
    }
  }
  return links;
}

async function checkLink(url) {
  const response = await fetch(url, {
    method: 'HEAD',
    redirect: 'follow',
    signal: AbortSignal.timeout(15000),
    headers: {'user-agent': 'vaquum-docs-link-check/1.0'},
  });
  if (response.status === 405) {
    const getResponse = await fetch(url, {
      redirect: 'follow',
      signal: AbortSignal.timeout(15000),
      headers: {'user-agent': 'vaquum-docs-link-check/1.0'},
    });
    if (!getResponse.ok) {
      throw new Error(`${url} returned ${getResponse.status}`);
    }
    return;
  }
  if (!response.ok) {
    throw new Error(`${url} returned ${response.status}`);
  }
}

async function main() {
  const links = new Set();
  for (const document of docsMap.documents) {
    const text = await fs.readFile(path.resolve(repoRoot, document.source), 'utf8');
    for (const url of extractExternalLinks(text)) {
      links.add(url);
    }
  }
  for (const url of [...links].sort()) {
    await checkLink(url);
  }
  process.stdout.write(`External links healthy: ${links.size}\n`);
}

if (process.argv[1] === scriptPath) {
  await main();
}
