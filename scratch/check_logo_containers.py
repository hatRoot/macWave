import os
import re
import glob

workspace = '/Users/joelduran/Documents/GitHub/MacWaveT2'
html_files = glob.glob(os.path.join(workspace, '*.html'))

logo_container_pattern = re.compile(r'<div[^>]*class="[^"]*logo[^"]*"[^>]*>.*?</div>\s*</a>\s*</div>', re.DOTALL | re.IGNORECASE)

print("Checking logo container HTML in all files:")
for f in html_files:
    content = open(f, 'r', encoding='utf-8').read()
    # Search for <div class="*logo*">...</div>
    # Let's find index of <div class="logo"> or similar
    matches = re.findall(r'<div class="[^"]*logo[^"]*">.*?</a>\s*</div>', content, re.DOTALL | re.IGNORECASE)
    if matches:
        print(f"--- {os.path.basename(f)} ({len(matches)} matches) ---")
        for i, match in enumerate(matches):
            # clean up whitespace to print nicely
            clean = "\n".join([line.strip() for line in match.split("\n") if line.strip()])
            print(f"  Match {i+1}:\n{clean}")
    else:
        # try search for logo-link inside header
        header_match = re.search(r'<header[^>]*>.*?</header>', content, re.DOTALL | re.IGNORECASE)
        if header_match:
            logo_in_header = re.findall(r'<a[^>]*class="[^"]*logo-link[^"]*"[^>]*>.*?</a>', header_match.group(0), re.DOTALL | re.IGNORECASE)
            if logo_in_header:
                print(f"--- {os.path.basename(f)} (in header) ---")
                for i, match in enumerate(logo_in_header):
                    clean = "\n".join([line.strip() for line in match.split("\n") if line.strip()])
                    print(f"  Match {i+1}:\n{clean}")
            else:
                print(f"--- {os.path.basename(f)}: No logo in header ---")
        else:
            print(f"--- {os.path.basename(f)}: No header found ---")
