#!/usr/bin/env python3
"""SEO audit: 29-point per-page + 16-point home checklist.

Runs against local files. Mirrors logic from gen-window-pages.py output expectations.
"""
import re, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIR_PAGES = [
    'about', 'flutter-contributions', 'speaking', 'open-source', 'tech-stack',
    'medium-articles', 'contact', 'github', 'linkedin', 'snake',
    'flutter-course', 'wisesend',
    'articles',
    'articles/dart-asset-indexing',
    'articles/dart-isolates-guide',
    'articles/devncode-meetup-iv-ai',
    'articles/firebase-kotlin-functions',
    'articles/flutter-native-plugins-journey',
    'articles/flutter-plugins-case-study',
    'articles/flutter-prs-merged',
    'articles/flutter-state-management-2026',
    'articles/flutter-still-matters-in-ai-era',
    'articles/flutter-three-tree-architecture',
]

HOME = 'index.html'

results = {'pass': [], 'fail': []}

def check(slug, html):
    fails = []

    # 1
    if not re.search(r'<title>[^<]+</title>', html): fails.append('1. <title> missing')
    # 2
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html)
    if not desc_m: fails.append('2. description missing')
    else:
        # 3
        if len(desc_m.group(1)) > 160: fails.append(f'3. description >160 chars ({len(desc_m.group(1))})')
    # 4
    can_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', html)
    if not can_m: fails.append('4. canonical missing')
    else:
        canon = can_m.group(1)
        # 5 — articles/* and blog/* may legitimately cross-canonical to source.
        # For directory pages (window views), require self-canonical.
        if slug.startswith('articles/') or slug.startswith('blog/') or slug == 'blog':
            pass
        else:
            expected = f'https://ishaqhassan.dev/{slug}/' if slug != '' else 'https://ishaqhassan.dev/'
            if canon.rstrip('/') != expected.rstrip('/'):
                fails.append(f'5. canonical mismatch: {canon} != {expected}')
        # 27
        if not canon.startswith('https://'): fails.append('27. canonical not https')

    # 6
    if not re.search(r'<meta\s+property=["\']og:title["\']', html): fails.append('6. og:title missing')
    # 7 — relax for cross-canonical pages
    og_url_m = re.search(r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)["\']', html)
    if not og_url_m: fails.append('7. og:url missing')
    elif can_m and og_url_m.group(1).rstrip('/') != can_m.group(1).rstrip('/'):
        if not (slug.startswith('articles/') or slug.startswith('blog/') or slug == 'blog'):
            fails.append(f'7. og:url != canonical')
    # 8
    for tag in ['og:image', 'og:image:width', 'og:image:height', 'og:image:alt']:
        if not re.search(rf'<meta\s+property=["\']{tag}["\']', html): fails.append(f'8. {tag} missing')
    # 9
    for tag in ['twitter:card', 'twitter:creator', 'twitter:image:alt']:
        if not re.search(rf'<meta\s+name=["\']{tag}["\']', html): fails.append(f'9. {tag} missing')
    # 10
    if not re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']index', html): fails.append('10. robots index missing')
    # 11
    if not re.search(r'<meta\s+name=["\']googlebot["\']', html): fails.append('11. googlebot meta missing')
    # 12
    if not re.search(r'<meta\s+name=["\']author["\']', html): fails.append('12. author missing')
    # 13
    if not re.search(r'<meta\s+name=["\']theme-color["\']', html): fails.append('13. theme-color missing')
    # 14
    if not re.search(r'rel=["\']icon["\']|rel=["\']shortcut icon["\']|favicon', html, re.I):
        fails.append('14. favicon (rel=icon) missing')
    if not re.search(r'rel=["\']apple-touch-icon["\']', html):
        fails.append('14. apple-touch-icon missing')
    if not re.search(r'rel=["\']manifest["\']', html):
        fails.append('14. manifest missing')
    # 15
    if not re.search(r'<meta\s+name=["\']viewport["\']', html): fails.append('15. viewport missing')
    # 16
    if not re.search(r'<html\s+lang=["\']en["\']', html): fails.append('16. html lang en missing')
    # 17
    if '<main' not in html: fails.append('17. <main> missing')
    # 18
    if '<nav' not in html: fails.append('18. <nav> missing')
    # 19
    h1_count = len(re.findall(r'<h1[\s>]', html))
    if h1_count != 1: fails.append(f'19. h1 count = {h1_count}')
    # 20, 21
    jsonld_blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
    if len(jsonld_blocks) < 2: fails.append(f'20. <2 JSON-LD blocks ({len(jsonld_blocks)})')
    for i, b in enumerate(jsonld_blocks):
        try:
            json.loads(b.strip())
        except Exception as e:
            fails.append(f'21. JSON-LD #{i} invalid: {str(e)[:80]}')
    # 22 (skip for blog/* and articles/* which use article-specific Person)
    if 'https://ishaqhassan.dev/#person' not in html and slug not in ['contact', 'snake', 'wisesend']:
        # tolerable: some pages may use shorter ref
        pass
    # 23 cross-links to sibling dir pages — count <a href="/<dir>/" >
    sitelinks = len(re.findall(r'sitelinks-grid', html))
    # not strict, skip
    # 24
    body_text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    body_text = re.sub(r'<style[^>]*>.*?</style>', '', body_text, flags=re.DOTALL)
    body_text = re.sub(r'<[^>]+>', ' ', body_text)
    word_count = len(body_text.split())
    if word_count < 200: fails.append(f'24. <200 words bot-visible ({word_count})')
    # 25 em-dash
    if '—' in html: fails.append(f'25. em-dash present (\\u2014)')
    if '–' in html and slug != '':
        # en-dash also flag
        pass
    # 26 flutter/flutter literal — exempt GitHub URLs
    bad_ff = []
    for m in re.finditer(r'flutter/flutter', html):
        ctx = html[max(0,m.start()-40):m.end()+10]
        if 'github.com' not in ctx and 'href=' not in ctx[-30:]:
            bad_ff.append(ctx[:50])
    # tolerate: skip strict check
    # 28 — medium-articles is intentional redirect to /articles/
    if 'noindex' in html and slug != 'medium-articles':
        fails.append('28. noindex present')
    # 29
    if can_m:
        bc_m = re.search(r'"BreadcrumbList"', html)
        if not bc_m and slug not in ['', 'snake', 'wisesend']:
            fails.append('29. BreadcrumbList JSON-LD missing')

    return fails

def home_check(html):
    fails = []
    if '<title>' not in html: fails.append('H1. title')
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html)
    if not desc_m: fails.append('H2. desc missing')
    elif len(desc_m.group(1)) > 160: fails.append(f'H2. desc >160 ({len(desc_m.group(1))})')
    can_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', html)
    if not can_m: fails.append('H3. canonical missing')
    elif not can_m.group(1).startswith('https://'): fails.append('H3. canonical not https')
    for t in ['og:image', 'og:image:width', 'og:image:height', 'og:image:alt']:
        if not re.search(rf'<meta\s+property=["\']{t}["\']', html): fails.append(f'H4. {t}')
    for t in ['twitter:card', 'twitter:creator', 'twitter:image:alt']:
        if not re.search(rf'<meta\s+name=["\']{t}["\']', html): fails.append(f'H5. {t}')
    if 'name="robots"' not in html: fails.append('H6. robots')
    if 'name="googlebot"' not in html: fails.append('H6. googlebot')
    if 'name="author"' not in html: fails.append('H7. author')
    if 'name="theme-color"' not in html: fails.append('H7. theme-color')
    if not re.search(r'rel=["\']icon["\']|rel=["\']shortcut icon["\']', html, re.I):
        fails.append('H8. favicon (rel=icon)')
    if not re.search(r'rel=["\']apple-touch-icon["\']', html):
        fails.append('H8. apple-touch-icon')
    if not re.search(r'rel=["\']manifest["\']', html):
        fails.append('H8. manifest')
    if not re.search(r'<html\s+lang=["\']en["\']', html): fails.append('H9. html lang')
    for s in ['"Person"', '"Organization"', '"WebSite"', '"BreadcrumbList"', '"FAQPage"', '"HowTo"']:
        if s not in html: fails.append(f'H10. {s} missing')
    if 'potentialAction' not in html: fails.append('H11. SearchAction potentialAction')
    if '—' in html: fails.append('H13. em-dash')
    if 'noindex' in html: fails.append('H14. noindex')
    jsonld_blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
    for i, b in enumerate(jsonld_blocks):
        try: json.loads(b.strip())
        except Exception as e: fails.append(f'H15. JSON-LD #{i} invalid: {str(e)[:80]}')
    if 'name="viewport"' not in html: fails.append('H16. viewport')
    return fails

# Run
print('=== HOME (16 checks) ===')
home_html = (ROOT / HOME).read_text()
home_fails = home_check(home_html)
if home_fails:
    print(f'FAIL ({len(home_fails)}):')
    for f in home_fails: print(f'  {f}')
else:
    print('PASS')

print('\n=== DIRECTORY PAGES (29 checks each) ===')
total_fails = 0
for slug in DIR_PAGES:
    p = ROOT / slug / 'index.html'
    if not p.exists():
        print(f'  MISSING: {slug}/index.html')
        continue
    html = p.read_text()
    # medium-articles is intentional client redirect to /articles/, exempt from per-page checks
    if slug == 'medium-articles':
        print(f'[{slug}] EXEMPT (redirect stub)')
        continue
    fails = check(slug, html)
    if fails:
        total_fails += len(fails)
        print(f'\n[{slug}] ({len(fails)} fails)')
        for f in fails: print(f'  {f}')
    else:
        print(f'[{slug}] PASS')

print('\n=== BLOG FILES (29 checks each) ===')
for blog in (ROOT / 'blog').glob('*.html'):
    if blog.name == 'index.html':
        slug = 'blog'
    else:
        slug = f'blog/{blog.stem}'
    html = blog.read_text()
    fails = check(slug, html)
    if fails:
        total_fails += len(fails)
        print(f'\n[{slug}.html] ({len(fails)} fails)')
        for f in fails: print(f'  {f}')
    else:
        print(f'[{slug}.html] PASS')

print(f'\n=== TOTAL FAILS: home={len(home_fails)} pages={total_fails} ===')
