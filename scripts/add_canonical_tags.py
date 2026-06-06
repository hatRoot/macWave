import os
import re

# Base URL for the website
BASE_URL = "https://macwave.com.mx/"

def process_file(filepath):
    filename = os.path.basename(filepath)
    if filename == "index.html":
        canonical_url = BASE_URL
    else:
        # e.g., reparaciones.html -> https://macwave.com.mx/reparaciones
        canonical_url = f"{BASE_URL}{filename.replace('.html', '')}"

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if a canonical tag already exists
    if re.search(r'<link\s+rel=["\']canonical["\']', content, re.IGNORECASE):
        print(f"Skipping {filename}: Canonical tag already exists.")
        return

    # Create the canonical tag
    canonical_tag = f'\n  <link rel="canonical" href="{canonical_url}">\n'

    # Try inserting right before </head>
    if '</head>' in content:
        new_content = content.replace('</head>', f'{canonical_tag}</head>')
    else:
        print(f"Warning: No </head> tag found in {filename}.")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added canonical tag to {filename}: {canonical_url}")

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    count = 0
    
    # Process only HTML files in the root directory
    for f in os.listdir(root_dir):
        if f.endswith(".html"):
            process_file(os.path.join(root_dir, f))
            count += 1
            
    print(f"\nProcessed {count} HTML files in root directory.")

if __name__ == "__main__":
    main()
