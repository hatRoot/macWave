import sys
import os

def replace_footer(target_files):
    # Try current directory first, then fallback to parent of script directory
    base_dir = '.'
    if not os.path.exists(os.path.join(base_dir, 'index.html')):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    index_path = os.path.join(base_dir, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<footer class="main-footer">'
    end_tag = '</footer>'
    
    start_idx = content.find(start_tag)
    if start_idx == -1:
        print("Footer not found in index.html")
        return
        
    end_idx = content.find(end_tag, start_idx) + len(end_tag)
    footer_content = content[start_idx:end_idx]
    
    for filename in target_files:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            target_content = f.read()
            
        t_start_idx = target_content.find(start_tag)
        if t_start_idx == -1:
            print(f"Footer not found in {filename}")
            continue
            
        t_end_idx = target_content.find(end_tag, t_start_idx) + len(end_tag)
        
        new_content = target_content[:t_start_idx] + footer_content + target_content[t_end_idx:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Updated footer in {filename}")

replace_footer(['reparaciones.html', 'empresas.html', 'software.html', 'upgrades.html', 'terminos.html', 'tecnicos.html', 'status-ods.html', 'dashboard-ods.html', 'bateria-macbook-cdmx.html', 'mac-mojada-cdmx.html'])
