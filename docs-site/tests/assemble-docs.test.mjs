import assert from 'node:assert/strict';
import test from 'node:test';

import {rewriteOutsideCode} from '../scripts/assemble-docs.mjs';
import {extractExternalLinks} from '../scripts/check-external-links.mjs';

const mark = (value) => value.replaceAll('{TOKEN}', 'REWRITTEN');

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
