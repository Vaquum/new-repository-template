import {readFileSync} from 'node:fs';
import path from 'node:path';

const NODE_MODULES = 'node_modules/';

// npm resolves a dependency by walking up the `node_modules` chain from the
// requiring package to the tree root, taking the first match. Reproduce that
// walk rather than assuming a flat, hoisted tree: docusaurus nests several
// duplicate versions, and a flat lookup silently attributes them to the wrong
// parent.
function resolveFrom(packages, requirePath, name) {
  let base = requirePath;
  for (;;) {
    const candidate = base === '' ? NODE_MODULES + name : `${base}/${NODE_MODULES}${name}`;
    if (packages[candidate] !== undefined) {
      return candidate;
    }
    if (base === '') {
      return null;
    }
    const cut = base.lastIndexOf('/' + NODE_MODULES);
    base = cut === -1 ? '' : base.slice(0, cut);
  }
}

function packageName(packages, packagePath) {
  return packages[packagePath].name
    ?? packagePath.slice(packagePath.lastIndexOf(NODE_MODULES) + NODE_MODULES.length);
}

/**
 * Map each package in the tree to the set of direct dependencies that reach it.
 *
 * A package reachable only through `@docusaurus/core` maps to that one root; a
 * package shared with `react` maps to both. The severity floor in
 * `audit-report.mjs` is chosen from this set, so a shared dependency cannot
 * inherit a relaxed floor from one of its parents alone.
 */
export function rootsFrom(packages, directDependencies) {
  const roots = new Map();
  for (const root of directDependencies) {
    const start = resolveFrom(packages, '', root);
    if (start === null) {
      continue;
    }
    const pending = [start];
    const visited = new Set([start]);
    while (pending.length > 0) {
      const current = pending.pop();
      const name = packageName(packages, current);
      if (!roots.has(name)) {
        roots.set(name, new Set());
      }
      roots.get(name).add(root);
      for (const dependency of Object.keys(packages[current].dependencies ?? {})) {
        const resolved = resolveFrom(packages, current, dependency);
        if (resolved !== null && !visited.has(resolved)) {
          visited.add(resolved);
          pending.push(resolved);
        }
      }
    }
  }
  return roots;
}

/**
 * Reachability for the site's production tree, read from `package-lock.json`.
 *
 * The lockfile is checked in and fully resolved, so this needs no install step
 * and returns the same answer on every machine.
 */
export function productionRoots(siteRoot) {
  const lock = JSON.parse(readFileSync(path.join(siteRoot, 'package-lock.json'), 'utf8'));
  const manifest = JSON.parse(readFileSync(path.join(siteRoot, 'package.json'), 'utf8'));
  return rootsFrom(lock.packages, Object.keys(manifest.dependencies ?? {}));
}
