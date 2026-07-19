import {spawnSync} from 'node:child_process';

import {auditFailure} from './audit-report.mjs';

const result = spawnSync('npm', ['audit', '--omit=dev', '--json'], {
  cwd: process.cwd(),
  encoding: 'utf8',
});
if (!result.stdout) {
  process.stderr.write(result.stderr || 'npm audit produced no JSON output\n');
  process.exit(result.status || 1);
}
const report = JSON.parse(result.stdout);
const failure = auditFailure(report);
if (failure) {
  process.stderr.write(`${failure}\n`);
  process.exit(1);
}
process.stdout.write('No docs-site npm vulnerabilities found\n');
