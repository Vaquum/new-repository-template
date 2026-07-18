"""The inherited documentation scaffold remains portable and complete."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_SITE = REPO_ROOT / 'docs-site'


def _json(name: str) -> dict[str, object]:
    return json.loads((DOCS_SITE / name).read_text(encoding='utf-8'))


def test_product_profile_has_one_portable_identity_boundary() -> None:
    profile = _json('product-docs.json')

    assert list(profile) == [
        'productId',
        'productName',
        'tagline',
        'siteUrl',
        'basePath',
        'sourceRepoUrl',
    ]
    assert profile['sourceRepoUrl'] == (
        'https://github.com/{REPOSITORY_OWNER}/{REPOSITORY_NAME}'
    )


def test_route_map_owns_five_sections_and_existing_unique_sources() -> None:
    docs_map = _json('docs-map.json')
    sections = docs_map['sections']
    documents = docs_map['documents']

    assert isinstance(sections, list)
    assert [section['label'] for section in sections] == [
        'Overview',
        'Guides',
        'Reference',
        'Developer',
        'Packages',
    ]
    assert isinstance(documents, list)
    sources = [document['source'] for document in documents]
    destinations = [document['dest'] for document in documents]
    routes = [document['slug'] for document in documents]
    assert len(sources) == len(set(sources))
    assert len(destinations) == len(set(destinations))
    assert len(routes) == len(set(routes))
    assert all((REPO_ROOT / source).is_file() for source in sources)


def test_docs_check_covers_portable_acceptance_surfaces() -> None:
    package = _json('package.json')
    scripts = package['scripts']
    check = scripts['check']

    assert 'markdownlint-cli2' in scripts['lint']
    assert 'check-external-links.mjs' in scripts['check:external-links']
    assert 'audit-security.mjs' in scripts['security:audit']
    assert 'docusaurus build --no-minify' in check
    assert 'verify:build' in check
    assert 'test:browser' in check


def test_shared_docs_site_has_no_limen_literals() -> None:
    excluded = {'node_modules', 'build', '.generated', '.docusaurus'}
    files = [
        path
        for path in DOCS_SITE.rglob('*')
        if path.is_file()
        and path.name != 'package-lock.json'
        and not excluded.intersection(path.relative_to(DOCS_SITE).parts)
    ]

    assert all(
        literal not in path.read_text(encoding='utf-8')
        for path in files
        for literal in ('Limen', '/limen/')
    )


def test_visual_contract_self_hosts_plex_fonts() -> None:
    css = (DOCS_SITE / 'src' / 'css' / 'custom.css').read_text(encoding='utf-8')

    assert "@import '@fontsource/ibm-plex-sans/400.css';" in css
    assert "@import '@fontsource/ibm-plex-mono/400.css';" in css
    assert 'fonts.googleapis.com' not in css
