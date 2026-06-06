import sys
import os

def replace_header(target_files):
    with open('/Users/joelduran/Documents/GitHub/MacWaveT2/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<header class="main-header">'
    end_tag = '</header>'
    
    start_idx = content.find(start_tag)
    if start_idx == -1:
        print("Header not found in index.html")
        return
        
    end_idx = content.find(end_tag, start_idx) + len(end_tag)
    
    header_content = content[start_idx:end_idx]
    
    for filename in target_files:
        filepath = os.path.join('/Users/joelduran/Documents/GitHub/MacWaveT2', filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            target_content = f.read()
            
        t_start_idx = target_content.find(start_tag)
        t_end_idx = target_content.find(end_tag, t_start_idx) + len(end_tag)
        
        new_content = target_content[:t_start_idx] + header_content + target_content[t_end_idx:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Updated header in {filename}")

replace_header(['reparaciones.html', 'empresas.html', 'software.html', 'upgrades.html', 'bateria-macbook-cdmx.html', 'mac-mojada-cdmx.html', 'terminos.html', 'status-ods.html', 'tecnicos.html'])
