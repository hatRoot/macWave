import os
import re

ROOT = '/Users/joelduran/Documents/GitHub/MacWaveT2'

# Landing pages that have og:url wrongly pointing to /reparaciones
LANDING_PAGES = [
    'actualizar-mac-os-vieja.html',
    'bateria-pantalla-iphone-express.html',
    'cambio-teclado-macbook-cdmx.html',
    'mac-mojada-urgencia.html',
    'mantenimiento-macbook-cdmx.html',
    'reflow-gpu-mac.html',
    'reparacion-corto-logica-mac.html',
    'reparacion-flexgate-macbook.html',
    'reparacion-imac-cdmx.html',
    'reparacion-laptops-gamer-cdmx.html',
]

def fix_og_url(fname):
    slug = fname.replace('.html', '')
    correct_url = f'https://macwave.com.mx/{slug}'
    path = os.path.join(ROOT, fname)

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace og:url content regardless of current value
    new_content = re.sub(
        r'(<meta\s+property=["\']og:url["\']\s+content=["\'])([^"\']+)(["\'])',
        lambda m: f'{m.group(1)}{correct_url}{m.group(3)}',
        content,
        flags=re.IGNORECASE
    )

    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'  Fixed og:url -> {correct_url}  ({fname})')
    else:
        print(f'  No change needed for {fname}')

if __name__ == '__main__':
    print('=== Fixing og:url on landing pages ===')
    for fname in LANDING_PAGES:
        fix_og_url(fname)
    print('Done.')
