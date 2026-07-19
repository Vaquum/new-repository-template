import assert from 'node:assert/strict';
import test from 'node:test';

import {
  isPathInside,
  normalizeForMdx,
  rewriteOutsideCode,
  validateSections,
} from '../scripts/assemble-docs.mjs';
import {auditFailure} from '../scripts/audit-report.mjs';
import {
  assertPublicUrl,
  extractExternalLinks,
  isPublicAddress,
} from '../scripts/check-external-links.mjs';
import {markdownSources} from '../scripts/lint-markdown.mjs';
import {canonicalSitemapUrl} from '../scripts/site-urls.mjs';

const mark = (value) => value.replaceAll('{TOKEN}', 'REWRITTEN');

test('fails closed on npm audit errors and malformed reports', () => {
  assert.match(
    auditFailure({error: {code: 'ENOAUDIT'}}),
    /npm audit failed.*ENOAUDIT/
  );
  assert.equal(
    auditFailure({metadata: {}}),
    'npm audit report has no vulnerabilities object'
  );
  assert.equal(auditFailure({vulnerabilities: {}}), null);
  assert.equal(
    auditFailure({vulnerabilities: {package: {severity: 'high'}}}),
    'Docs-site npm vulnerabilities: package'
  );
});

test('rewrites prose but preserves fenced and inline code', () => {
  const source = [
    'before {TOKEN}',
    '```text',
    'inside {TOKEN}',
    '```',
    'after `{TOKEN}` and {TOKEN}',
  ].join('\n');

  assert.equal(
    rewriteOutsideCode(source, mark),
    [
      'before REWRITTEN',
      '```text',
      'inside {TOKEN}',
      '```',
      'after `{TOKEN}` and REWRITTEN',
    ].join('\n')
  );
});

test('preserves the tail of an unclosed fence', () => {
  const source = 'before {TOKEN}\n```text\ninside {TOKEN}';

  assert.equal(
    rewriteOutsideCode(source, mark),
    'before REWRITTEN\n```text\ninside {TOKEN}'
  );
});

test('preserves the tail of unmatched inline code', () => {
  const source = 'before {TOKEN} and `{TOKEN}';

  assert.equal(
    rewriteOutsideCode(source, mark),
    'before REWRITTEN and `{TOKEN}'
  );
});

test('extracts unique Markdown and HTML external links', () => {
  const source = [
    '[Repository](https://github.com/Vaquum/example)',
    '<a href="https://docs.vaquum.fi/example/">Docs</a>',
    '<img src="https://docs.vaquum.fi/example/logo.png" alt="Logo" />',
    '[Duplicate](https://github.com/Vaquum/example)',
  ].join('\n');

  assert.deepEqual(
    [...extractExternalLinks(source)].sort(),
    [
      'https://docs.vaquum.fi/example/',
      'https://docs.vaquum.fi/example/logo.png',
      'https://github.com/Vaquum/example',
    ]
  );
});

test('rewrites prose links without mutating code examples', () => {
  const source = [
    '[Docs](docs/README.md)',
    '```markdown',
    '[Docs](docs/README.md)',
    '```',
    '`[Docs](docs/README.md)`',
  ].join('\n');

  assert.equal(
    normalizeForMdx(source, 'README.md'),
    [
      '[Docs](overview/docs-hub.md)',
      '```markdown',
      '[Docs](docs/README.md)',
      '```',
      '`[Docs](docs/README.md)`',
    ].join('\n')
  );
});

test('keeps repository link resolution inside the repository root', () => {
  assert.equal(isPathInside('/repo', '/repo'), true);
  assert.equal(isPathInside('/repo', '/repo/docs/README.md'), true);
  assert.equal(isPathInside('/repo', '/repo-neighbor/README.md'), false);
  assert.equal(isPathInside('/repo', '/outside/README.md'), false);
});

test('builds canonical sitemap URLs for root and nested docs paths', () => {
  assert.equal(
    canonicalSitemapUrl('https://docs.example.com', '/'),
    'https://docs.example.com/sitemap.xml'
  );
  assert.equal(
    canonicalSitemapUrl('https://docs.example.com/', '/product/'),
    'https://docs.example.com/product/sitemap.xml'
  );
});

test('derives Markdown lint sources from the route map', () => {
  const map = {
    documents: [
      {source: 'README.md'},
      {source: 'docs/README.md'},
      {source: 'README.md'},
    ],
  };

  assert.deepEqual(
    markdownSources(map),
    ['CHANGELOG.md', 'README.md', 'docs/README.md']
  );
});

test('validates every category field before generation', () => {
  const sections = Array.from({length: 5}, (_, index) => ({
    dir: `section-${index}`,
    label: `Section ${index}`,
    position: index + 1,
    slug: `/section-${index}`,
    description: `Section ${index} description.`,
  }));

  assert.doesNotThrow(() => validateSections(sections));
  assert.throws(
    () => validateSections([{...sections[0], label: ''}, ...sections.slice(1)]),
    /section.label must be a non-empty string/
  );
  assert.throws(
    () => validateSections([{...sections[0], position: 0}, ...sections.slice(1)]),
    /section.position must be a positive integer/
  );
});

test('rejects external-link destinations that can reach private networks', async () => {
  assert.equal(isPublicAddress('8.8.8.8'), true);
  assert.equal(isPublicAddress('127.0.0.1'), false);
  assert.equal(isPublicAddress('169.254.169.254'), false);
  assert.equal(isPublicAddress('10.20.30.40'), false);
  assert.equal(isPublicAddress('192.0.2.1'), false);
  assert.equal(isPublicAddress('::1'), false);
  assert.equal(isPublicAddress('fe80::1'), false);

  await assert.rejects(
    assertPublicUrl('http://localhost/private'),
    /non-public destination/
  );
  await assert.rejects(
    assertPublicUrl('http://169.254.169.254/latest/meta-data'),
    /non-public destination/
  );
  await assert.rejects(
    assertPublicUrl('https://user:secret@example.com/'),
    /must not contain credentials/
  );
});
