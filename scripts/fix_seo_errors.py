import os
import re

files = [
    "actualizar-mac-os-vieja.html",
    "bateria-macbook-cdmx.html",
    "bateria-pantalla-iphone-express.html",
    "cambio-bateria-macbook-pro-air.html",
    "cambio-teclado-macbook-cdmx.html",
    "mac-mojada-urgencia.html",
    "mantenimiento-macbook-cdmx.html",
    "reflow-gpu-mac.html",
    "reparacion-corto-logica-mac.html",
    "reparacion-flexgate-macbook.html",
    "reparacion-imac-cdmx.html",
    "reparacion-laptops-gamer-cdmx.html"
]

def fix_seo(content, filename):
    slug = filename.replace(".html", "")
    canonical_url = f"https://macwave.com.mx/{slug}"
    
    # 1. Fix og:url
    content = re.sub(r'<meta property="og:url" content="https://macwave\.com\.mx/reparaciones">', 
                     f'<meta property="og:url" content="{canonical_url}">', content)
    
    # 2. Fix JSON-LD IDs
    content = content.replace("https://macwave.com.mx/reparaciones#mac-repair-v4", f"{canonical_url}#product")
    content = content.replace("https://macwave.com.mx/reparaciones#webpage", f"{canonical_url}#webpage")
    content = content.replace("https://macwave.com.mx/#website", "https://macwave.com.mx/#website")
    
    # 3. Add Breadcrumb if missing
    if '"@type": "BreadcrumbList"' not in content:
        breadcrumb_json = f"""{{
        "@type": "BreadcrumbList",
        "@id": "{canonical_url}#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "item": {{
              "@id": "https://macwave.com.mx/",
              "name": "Inicio"
            }}
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "item": {{
              "@id": "{canonical_url}",
              "name": "{slug.replace('-', ' ').title()}"
            }}
          }}
        ]
      }},"""
        # Insert before LocalBusiness or Product in the list
        content = content.replace('"@graph": [', f'"@graph": [\n      {breadcrumb_json}')

    # 4. Ensure </main> exists before <footer>
    if "</main>" not in content and "<main>" in content:
        content = content.replace('<footer class="main-footer">', '</main>\n\n    <footer class="main-footer">')

    return content

for f in files:
    if os.path.exists(f):
        print(f"Fixing {f}...")
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        
        new_c = fix_seo(c, f)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_c)
    else:
        print(f"File {f} not found.")
