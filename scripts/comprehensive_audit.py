import os
import re

def find_html_files(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def audit_seo(html_files):
    results = {}
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        file_name = os.path.basename(file_path)
        issues = []
        
        # Check for Title
        if not re.search(r'<title>.*?</title>', content, re.IGNORECASE):
            issues.append("Missing <title>")
            
        # Check for Meta Description
        if not re.search(r'<meta name="description"', content, re.IGNORECASE):
            issues.append("Missing <meta name=\"description\">")
            
        # Check for H1
        h1s = re.findall(r'<h1.*?>.*?</h1>', content, re.IGNORECASE | re.DOTALL)
        if len(h1s) == 0:
            issues.append("Missing <h1>")
        elif len(h1s) > 1:
            issues.append(f"Multiple <h1> tags ({len(h1s)})")
            
        # Check for Canonical
        if not re.search(r'<link rel="canonical"', content, re.IGNORECASE):
            issues.append("Missing <link rel=\"canonical\">")
            
        # Check for JSON-LD
        if not re.search(r'<script type="application/ld\+json">', content, re.IGNORECASE):
            issues.append("Missing JSON-LD structured data")
            
        # Check for images without alt tags
        img_tags = re.findall(r'<img.*?>', content, re.IGNORECASE)
        imgs_without_alt = [img for img in img_tags if 'alt=' not in img.lower()]
        if imgs_without_alt:
            issues.append(f"{len(imgs_without_alt)} images missing 'alt' attribute")
            
        # Check for internal links
        links = re.findall(r'href=["\'](.*?)["\']', content)
        for link in links:
            if link.startswith('/') or (not link.startswith('http') and not link.startswith('mailto') and not link.startswith('tel') and not link.startswith('#')):
                # Internal link
                target = link.split('?')[0].split('#')[0]
                if not target or target == '/':
                    continue
                
                # Check if target exists as .html or exactly
                possible_paths = [
                    os.path.join(os.path.dirname(file_path), target),
                    os.path.join(os.path.dirname(file_path), target + ".html"),
                    os.path.join("/Users/joelduran/Documents/GitHub/MacWaveT2", target.lstrip('/')),
                    os.path.join("/Users/joelduran/Documents/GitHub/MacWaveT2", target.lstrip('/') + ".html")
                ]
                exists = any(os.path.exists(p) for p in possible_paths)
                if not exists and not target.endswith('.css') and not target.endswith('.js') and not target.endswith('.png') and not target.endswith('.jpg') and not target.endswith('.pdf'):
                   issues.append(f"Potential broken internal link: {link}")
                   
        if issues:
            results[file_name] = issues
            
    return results

if __name__ == "__main__":
    base_dir = "/Users/joelduran/Documents/GitHub/MacWaveT2"
    html_files = find_html_files(base_dir)
    # Exclude legacy and clientes/cotizaciones dirs if needed
    html_files = [f for f in html_files if "legacy" not in f and "clientes" not in f and "cotizaciones" not in f]
    
    audit_results = audit_seo(html_files)
    
    for file, issues in audit_results.items():
        print(f"--- {file} ---")
        for issue in issues:
            print(f"  [!] {issue}")
