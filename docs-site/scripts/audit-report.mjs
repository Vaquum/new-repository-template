export function auditFailure(report) {
  if (Object.hasOwn(report, 'error')) {
    return `npm audit failed: ${JSON.stringify(report.error)}`;
  }
  if (
    !Object.hasOwn(report, 'vulnerabilities')
    || typeof report.vulnerabilities !== 'object'
    || report.vulnerabilities === null
  ) {
    return 'npm audit report has no vulnerabilities object';
  }
  const vulnerabilities = Object.keys(report.vulnerabilities);
  return vulnerabilities.length > 0
    ? `Docs-site npm vulnerabilities: ${vulnerabilities.join(', ')}`
    : null;
}
