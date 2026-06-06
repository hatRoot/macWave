import os
import re

def process_files(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html") and not any(x in root for x in ["legacy", "clientes", "cotizaciones"]):
                html_files.append(os.path.join(root, file))
                
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Remove canonical tags
        content = re.sub(r'\s*<link rel="canonical"[^>]*>', '', content, flags=re.IGNORECASE)
        
        # 2. Convert internal .html links to clean URLs
        # Match href="page.html" or href='./page.html' etc.
        # Avoid external links
        def link_replacer(match):
            link = match.group(2)
            if link.startswith('http') or link.startswith('mailto') or link.startswith('tel') or link.startswith('#') or link.startswith('//'):
                return match.group(0)
            
            if link.endswith('.html'):
                clean_link = link[:-5]
                # If it ends up being empty (only was .html), maybe keep it or handle index
                if not clean_link or clean_link == 'index':
                    clean_link = '/'
                return f'{match.group(1)}="{clean_link}"'
            return match.group(0)

        content = re.sub(r'(href)=["\'](.*?)["\']', link_replacer, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {os.path.basename(file_path)}")

if __name__ == "__main__":
    process_files("/Users/joelduran/Documents/GitHub/MacWaveT2")
