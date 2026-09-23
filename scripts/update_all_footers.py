import os
import re

def update_footers():
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    footer_match = re.search(r'<footer class="main-footer">.*?</footer>', index_content, flags=re.DOTALL)
    if not footer_match:
        print("ERROR: Canonical footer not found in index.html")
        return
    
    canonical_footer = footer_match.group(0)
    
    target_files = [
        'cambio-bateria-macbook-pro-air.html',
        'bateria-macbook-cdmx.html',
        'reparacion-corto-logica-mac.html',
        'mac-mojada-cdmx.html',
        'mac-mojada-urgencia.html',
        'upgrades.html',
        'reparacion-imac-cdmx.html',
        'actualizar-mac-os-vieja.html',
        'reparaciones.html',
        'cambio-teclado-macbook-cdmx.html',
        'mantenimiento-macbook-cdmx.html',
        'reparacion-flexgate-macbook.html',
        'reflow-gpu-mac.html',
        'reparacion-laptops-gamer-cdmx.html',
        'empresas.html',
        'software.html',
        'casos-reales.html',
        'terminos.html',
        'bateria-pantalla-iphone-express.html'
    ]
    
    for filename in target_files:
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = None
        pattern = re.compile(r'<footer class="main-footer">.*?</footer>', re.DOTALL)
        new_content = pattern.sub(canonical_footer, content, count=1)
            
        if new_content and new_content != content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] Updated footer in {filename}")
        else:
            print(f"[SKIP] No change in {filename}")

if __name__ == '__main__':
    update_footers()
