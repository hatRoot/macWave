import os
import re
import glob

workspace = '/Users/joelduran/Documents/GitHub/MacWaveT2'
html_files = glob.glob(os.path.join(workspace, '*.html'))

logo_pattern = re.compile(r'<img[^>]*class="[^"]*logo-img[^"]*"[^>]*src="([^"]+)"')
logo_link_pattern = re.compile(r'<a[^>]*class="logo-link"[^>]*>.*?<img[^>]*src="([^"]+)"', re.DOTALL)

print("Checking logo sources in HTML files:")
for f in html_files:
    content = open(f, 'r', encoding='utf-8').read()
    logo_match = logo_pattern.search(content)
    if logo_match:
        print(f"{os.path.basename(f)} (via logo-img class): {logo_match.group(1)}")
    else:
        # try logo_link pattern
        link_match = logo_link_pattern.search(content)
        if link_match:
            print(f"{os.path.basename(f)} (via logo-link child): {link_match.group(1)}")
        else:
            print(f"{os.path.basename(f)}: No logo image found")
