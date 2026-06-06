import os
import glob
import re

workspace = '/Users/joelduran/Documents/GitHub/MacWaveT2'
all_html_files = glob.glob(os.path.join(workspace, '**', '*.html'), recursive=True)

print(f"Found {len(all_html_files)} HTML files in the workspace:")
logo_img_pattern = re.compile(r'class="[^"]*logo-img[^"]*"|src="[^"]*negro\.png"|src="[^"]*logo_dashboard_white\.png"', re.IGNORECASE)

for f in all_html_files:
    rel_path = os.path.relpath(f, workspace)
    # Ignore backup or third-party folders if any
    if '.git' in rel_path or 'node_modules' in rel_path or 'legacy' in rel_path:
        continue
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    if logo_img_pattern.search(content):
        print(f"  {rel_path}: Matches logo patterns")
    else:
        # Check if there is any img tag with src containing 'logo'
        if re.search(r'<img[^>]*src="[^"]*logo[^"]*"', content, re.IGNORECASE):
            print(f"  {rel_path}: Matches general logo image")
