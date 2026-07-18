export function canonicalSitemapUrl(siteUrl, basePath) {
  const siteRoot = siteUrl.replace(/\/+$/, '');
  const docsRoot = basePath === '/' ? '/' : `${basePath.replace(/\/+$/, '')}/`;
  return `${siteRoot}${docsRoot}sitemap.xml`;
}
