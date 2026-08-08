import assert from 'node:assert/strict';
import path from 'node:path';
import test from 'node:test';
import {fileURLToPath} from 'node:url';

import {
  DEFAULT_FLOOR,
  RELAXED_FLOOR,
  RELAXED_ROOTS,
  auditFailure,
} from '../scripts/audit-report.mjs';
import {productionRoots, rootsFrom} from '../scripts/audit-scope.mjs';

const siteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const NO_ROOTS = new Map();
const reached = (pkg, ...roots) => new Map([[pkg, new Set(roots)]]);
const report = (severity) => ({vulnerabilities: {victim: {severity}}});

test('fails closed on npm audit errors and malformed reports', () => {
  assert.match(
    auditFailure({error: {code: 'ENOAUDIT'}}, NO_ROOTS),
    /npm audit failed.*ENOAUDIT/
  );
  assert.equal(
    auditFailure({metadata: {}}, NO_ROOTS),
    'npm audit report has no vulnerabilities object'
  );
  assert.equal(auditFailure({vulnerabilities: {}}, NO_ROOTS), null);
});

test('a severity npm does not define fails loud rather than passing', () => {
  assert.match(
    auditFailure(report('catastrophic'), NO_ROOTS),
    /unknown severity "catastrophic" for victim/
  );
});

test('high outside the relaxed scope blocks', () => {
  assert.match(
    auditFailure(report('high'), reached('victim', 'react')),
    /victim \(high, floor high, via react\)/
  );
});

test('moderate outside the relaxed scope is below the default floor', () => {
  assert.equal(auditFailure(report('moderate'), reached('victim', 'react')), null);
});

test('high in the relaxed scope is allowed', () => {
  assert.equal(
    auditFailure(report('high'), reached('victim', '@docusaurus/core')),
    null
  );
});

test('critical in the relaxed scope still blocks', () => {
  assert.match(
    auditFailure(report('critical'), reached('victim', '@docusaurus/core')),
    /victim \(critical, floor critical, via @docusaurus\/core\)/
  );
});

test('a package reached by a strict root stays strict', () => {
  // Shared between docusaurus and react: one relaxed parent must not lower the
  // floor for the path that arrives through react.
  assert.match(
    auditFailure(report('high'), reached('victim', '@docusaurus/core', 'react')),
    /victim \(high, floor high, via @docusaurus\/core, react\)/
  );
});

test('a package the lockfile walk cannot place keeps the default floor', () => {
  assert.match(
    auditFailure(report('high'), NO_ROOTS),
    /victim \(high, floor high, via unresolved\)/
  );
});

test('the relaxed floor is above the default floor', () => {
  assert.equal(DEFAULT_FLOOR, 'high');
  assert.equal(RELAXED_FLOOR, 'critical');
  assert.ok(RELAXED_ROOTS.every((root) => root.includes('docusaurus')));
});

test('rootsFrom follows npm nesting rather than assuming a flat tree', () => {
  const packages = {
    'node_modules/root-a': {dependencies: {shared: '1'}},
    'node_modules/root-b': {dependencies: {shared: '1'}},
    // root-b resolves its own nested copy before the hoisted one.
    'node_modules/root-b/node_modules/shared': {dependencies: {deep: '1'}},
    'node_modules/shared': {},
    'node_modules/deep': {},
  };
  const roots = rootsFrom(packages, ['root-a', 'root-b']);
  assert.deepEqual([...roots.get('shared')].sort(), ['root-a', 'root-b']);
  // `deep` hangs off root-b's nested copy only.
  assert.deepEqual([...roots.get('deep')], ['root-b']);
});

test('productionRoots places every package the real audit can report', () => {
  const roots = productionRoots(siteRoot);
  assert.ok(roots.size > 0);
  // The stack the relaxed floor exists for must actually resolve, otherwise
  // every advisory silently falls back to the default floor.
  for (const root of RELAXED_ROOTS) {
    assert.ok(roots.has(root), `${root} is not reachable in the production tree`);
  }
});
