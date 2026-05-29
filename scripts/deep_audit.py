import os
import re

ROOT = '/Users/joelduran/Documents/GitHub/MacWaveT2'

# Pages that are intentionally blocked from Google (internal tools)
BLOCKED_PAGES = {'dashboard-ods.html', 'status-ods.html', 'ods.html', 'ticket-badge.html', 'tecnicos.html'}

def get_expected_canonical(fname):
    if fname == 'index.html':
        return 'https://macwave.com.mx/'
    return f"https://macwave.com.mx/{fname.replace('.html', '')}"

def audit_file(path):
    fname = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    issues = []

    # 1. Canonical tag
    canon = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not canon:
        issues.append('[CRITICAL] Missing <link rel="canonical"> tag')
    elif len(canon) > 1:
        issues.append(f'[CRITICAL] Multiple canonical tags found: {canon}')
    else:
        expected = get_expected_canonical(fname)
        if canon[0].rstrip('/') != expected.rstrip('/'):
            issues.append(f'[CRITICAL] Wrong canonical URL. Got: "{canon[0]}" Expected: "{expected}"')

    # 2. noindex check
    if re.search(r'noindex', content, re.IGNORECASE):
        issues.append('[CRITICAL] "noindex" found — this page is BLOCKED from Google indexing!')

    # 3. Title tag
    titles = re.findall(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if not titles:
        issues.append('[ERROR] Missing <title> tag')
    elif len(titles) > 1:
        issues.append(f'[WARN] Multiple <title> tags ({len(titles)}) — only the first is used')

    # 4. Meta description
    if not re.search(r'<meta\s+name=["\']description["\']', content, re.IGNORECASE):
        issues.append('[ERROR] Missing <meta name="description"> tag')

    # 5. H1 count
    h1s = re.findall(r'<h1[\s>]', content, re.IGNORECASE)
    if len(h1s) == 0:
        issues.append('[ERROR] Missing <h1> tag')
    elif len(h1s) > 1:
        issues.append(f'[WARN] Multiple <h1> tags ({len(h1s)}) — bad for SEO')

    # 6. JSON-LD structured data
    if not re.search(r'application/ld\+json', content, re.IGNORECASE):
        issues.append('[ERROR] Missing JSON-LD structured data (schema.org)')

    # 7. Google Analytics
    if 'G-JENWM4W22D' not in content:
        issues.append('[ERROR] Missing Google Analytics 4 tag')

    # 8. Images missing alt attributes
    imgs = re.findall(r'<img[^>]+>', content, re.IGNORECASE)
    missing_alt = [img[:80] for img in imgs if 'alt=' not in img.lower()]
    if missing_alt:
        issues.append(f'[WARN] {len(missing_alt)} <img> tag(s) missing alt attribute')

    # 9. Unmatched div tags
    open_divs = len(re.findall(r'<div[\s>]', content, re.IGNORECASE))
    close_divs = content.count('</div>')
    if open_divs != close_divs:
        issues.append(f'[ERROR] Unmatched <div> tags: {open_divs} opening, {close_divs} closing')

    # 10. og:url matches canonical
    og_urls = re.findall(r'property=["\']og:url["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if og_urls and canon:
        if og_urls[0].rstrip('/') != canon[0].rstrip('/'):
            issues.append(f'[WARN] og:url "{og_urls[0]}" does not match canonical "{canon[0]}"')

    # 11. hreflang matches canonical
    hreflangs = re.findall(r'<link[^>]+hreflang=[^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not hreflangs:
        hreflangs = re.findall(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+hreflang', content, re.IGNORECASE)
    if hreflangs and canon:
        for hl in hreflangs:
            if hl.rstrip('/') != canon[0].rstrip('/'):
                issues.append(f'[WARN] hreflang URL "{hl}" does not match canonical "{canon[0]}"')

    # 12. Broken internal links
    internal_links = re.findall(r'href=["\']([^"\'#][^"\']*)["\']', content, re.IGNORECASE)
    broken = set()
    for link in internal_links:
        if link.startswith('http') or link.startswith('mailto') or link.startswith('tel'): continue
        link_clean = link.split('?')[0].split('#')[0].strip('/')
        if not link_clean: continue
        if any(link_clean.endswith(ext) for ext in ['.css', '.js', '.pdf', '.png', '.jpg', '.jpeg', '.ico', '.xml', '.txt', '.svg', '.webp']): continue
        possible = [
            os.path.join(ROOT, link_clean),
            os.path.join(ROOT, link_clean + '.html'),
        ]
        if not any(os.path.exists(p) for p in possible):
            broken.add(link_clean)
    for b in sorted(broken):
        issues.append(f'[WARN] Broken internal link: "{b}"')

    return issues

def main():
    html_files = sorted([f for f in os.listdir(ROOT) if f.endswith('.html')])
    public_files = [f for f in html_files if f not in BLOCKED_PAGES]

    print(f'MacWave SEO Audit — {len(public_files)} public pages\n')
    print('=' * 60)

    all_errors = {}
    for fname in public_files:
        path = os.path.join(ROOT, fname)
        issues = audit_file(path)
        if issues:
            all_errors[fname] = issues

    if not all_errors:
        print('✅ No issues found across all pages!')
    else:
        for fname, issues in all_errors.items():
            print(f'\n📄 {fname}')
            for issue in issues:
                prefix = '🔴' if 'CRITICAL' in issue else ('🟠' if 'ERROR' in issue else '🟡')
                print(f'  {prefix} {issue}')

    print('\n' + '=' * 60)
    print(f'Summary: {len(all_errors)} files with issues / {len(public_files)} total public pages')
    print(f'Clean: {len(public_files) - len(all_errors)} files')

    # Indexability summary
    print('\n--- INDEXABILITY REPORT ---')
    for fname in public_files:
        path = os.path.join(ROOT, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        canon = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
        noindex = bool(re.search(r'noindex', content, re.IGNORECASE))
        expected = get_expected_canonical(fname)
        canon_ok = bool(canon) and canon[0].rstrip('/') == expected.rstrip('/')
        status = '✅ Indexable' if (canon_ok and not noindex) else '❌ PROBLEM'
        canon_display = canon[0] if canon else 'MISSING'
        print(f'  {status}  {fname}  →  {canon_display}')

if __name__ == '__main__':
    main()
