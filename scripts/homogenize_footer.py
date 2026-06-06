import os
import re

def homogenize_footers():
    # Read the canonical footer from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the footer block
    footer_match = re.search(r'<footer class="main-footer">.*?</footer>', content, flags=re.DOTALL)
    if not footer_match:
        print("Could not find footer in index.html")
        return
    
    canonical_footer = footer_match.group(0)
    print(f"Extracted canonical footer ({len(canonical_footer)} chars)")
    
    # Exclude internal app pages
    excludes = ['dashboard-ods.html', 'ods.html', 'tecnicos.html', 'status-ods.html', 'ticket-badge.html']
    
    modified_files = 0
    for filename in os.listdir('.'):
        if not filename.endswith('.html') or filename in excludes or filename == 'index.html':
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
            
        # Try finding the footer
        new_content = None
        if '<footer class="main-footer">' in file_content:
            new_content = re.sub(r'<footer class="main-footer">.*?</footer>', canonical_footer, file_content, flags=re.DOTALL)
        elif '<div class="footer">' in file_content: # For terminos.html potentially
             # Find where to insert it or replace it
             new_content = re.sub(r'<div class="footer">.*?</div>', canonical_footer, file_content, flags=re.DOTALL)
        else:
            print(f"Skipping {filename} - no footer found")
            continue
            
        if new_content and new_content != file_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_files += 1
            print(f"Updated footer in {filename}")
            
    print(f"Completed. Updated {modified_files} files.")

if __name__ == "__main__":
    homogenize_footers()
