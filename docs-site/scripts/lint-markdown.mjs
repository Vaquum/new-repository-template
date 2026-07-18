import fs from 'node:fs/promises';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const siteRoot = path.resolve(path.dirname(scriptPath), '..');
const docsMap = JSON.parse(
  await fs.readFile(path.resolve(siteRoot, 'docs-map.json'), 'utf8')
);

export function markdownSources(map) {
  return [
    ...new Set([
      'CHANGELOG.md',
      ...map.documents.map((document) => document.source),
    ]),
  ].sort();
}

function main() {
  const sources = markdownSources(docsMap).map((source) => `../${source}`);
  const result = spawnSync(
    'markdownlint-cli2',
    ['--config', '../.markdownlint.json', ...sources],
    {
      cwd: siteRoot,
      encoding: 'utf8',
      stdio: 'inherit',
    }
  );
  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    process.exit(result.status);
  }
}

if (process.argv[1] === scriptPath) {
  main();
}
