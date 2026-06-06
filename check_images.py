import re
import os
import glob

html_files = glob.glob('*.html')
image_files = set(os.listdir('images'))

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find all image sources correctly
    matches = re.findall(r'src=["\']([^"\']+)["\']', content)
    backgrounds = re.findall(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', content)
    ogs = re.findall(r'content=["\']([^"\']*\.(?:png|jpg|jpeg|svg|webp))["\']', content)
    
    all_imgs = matches + backgrounds + ogs
    
    missing = set()
    for img in all_imgs:
        if img.startswith('http') or img.startswith('//') or img.startswith('data:'):
            continue
            
        basename = os.path.basename(img)
        if basename and basename not in image_files:
            if not basename.endswith('.js') and not basename.endswith('.css'):
                if '.' in basename: # likely a file
                    missing.add(img)
                
    if missing:
        print(f"{html_file}: Missing images -> {missing}")

