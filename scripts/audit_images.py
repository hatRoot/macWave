import os
import re

def audit_images():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    results = []
    
    img_pattern = re.compile(r'<img[^>]+>', re.IGNORECASE | re.DOTALL)
    alt_pattern = re.compile(r'alt\s*=\s*["\']', re.IGNORECASE)
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            imgs = img_pattern.findall(content)
            for img in imgs:
                if not alt_pattern.search(img):
                    results.append(f"{filename}: {img.strip()}")
                    
    return results

if __name__ == "__main__":
    report = audit_images()
    if report:
        print("\n".join(report))
    else:
        print("All images have alt tags!")
