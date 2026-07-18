import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const repoRoot = path.resolve(path.dirname(scriptPath), '..', '..');
const docsMap = JSON.parse(
  await fs.readFile(path.resolve(repoRoot, 'docs-site', 'docs-map.json'), 'utf8')
);
const links = new Set();

for (const document of docsMap.documents) {
  const text = await fs.readFile(path.resolve(repoRoot, document.source), 'utf8');
  for (const match of text.matchAll(/\[[^\]]*]\((https?:\/\/[^)\s]+)\)/g)) {
    links.add(match[1]);
  }
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

for (const url of [...links].sort()) {
  await checkLink(url);
}
process.stdout.write(`External links healthy: ${links.size}\n`);
