import {spawnSync} from 'node:child_process';

const result = spawnSync('npm', ['audit', '--omit=dev', '--json'], {
  cwd: process.cwd(),
  encoding: 'utf8',
});
if (!result.stdout) {
  process.stderr.write(result.stderr || 'npm audit produced no JSON output\n');
  process.exit(result.status || 1);
}
const report = JSON.parse(result.stdout);
const vulnerabilities = Object.keys(report.vulnerabilities || {});
if (vulnerabilities.length > 0) {
  process.stderr.write(`Docs-site npm vulnerabilities: ${vulnerabilities.join(', ')}\n`);
  process.exit(1);
}
process.stdout.write('No docs-site npm vulnerabilities found\n');
