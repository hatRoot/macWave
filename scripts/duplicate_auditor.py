import os
import re
from collections import defaultdict

def audit_duplicates(directory):
    titles = defaultdict(list)
    descriptions = defaultdict(list)
    h1s = defaultdict(list)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html") and not any(x in root for x in ["legacy", "clientes", "cotizaciones"]):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                if title_match:
                    titles[title_match.group(1).strip()].append(file)
                
                desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
                if desc_match:
                    descriptions[desc_match.group(1).strip()].append(file)
                
                h1_matches = re.findall(r'<h1.*?>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
                for h1 in h1_matches:
                    clean_h1 = re.sub(r'<.*?>', '', h1).strip()
                    h1s[clean_h1].append(file)

    print("--- DUPLICATE TITLES ---")
    for t, files in titles.items():
        if len(files) > 1:
            print(f"Title: {t} in files: {files}")
            
    print("\n--- DUPLICATE DESCRIPTIONS ---")
    for d, files in descriptions.items():
        if len(files) > 1:
            print(f"Description: {d[:50]}... in files: {files}")
            
    print("\n--- DUPLICATE H1s ---")
    for h, files in h1s.items():
        if len(files) > 1:
            print(f"H1: {h} in files: {files}")

if __name__ == "__main__":
    audit_duplicates("/Users/joelduran/Documents/GitHub/MacWaveT2")
