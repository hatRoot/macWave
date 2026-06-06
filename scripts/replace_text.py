import glob
import os

target_dir = '/Users/joelduran/Documents/GitHub/MacWaveT2'

# Archivos a procesar: HTML y Scripts
files = glob.glob(os.path.join(target_dir, '*.html')) + glob.glob(os.path.join(target_dir, 'scripts', '*.py'))

old_str1 = "nosotros combinamos reparación nivel componente con credenciales oficiales de Apple ACSP"
new_str1 = "nosotros combinamos reparación nivel componente con credenciales oficiales de Apple ACSP"

old_str2 = "nosotros combinamos reparación nivel componente micro con credenciales oficiales de Apple Inc"
new_str2 = "nosotros combinamos reparación nivel componente con credenciales oficiales de Apple ACSP"

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    if old_str1 in content:
        content = content.replace(old_str1, new_str1)
        changed = True
    elif old_str2 in content:
        content = content.replace(old_str2, new_str2)
        changed = True

    if changed:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Texto reemplazado en: {os.path.basename(file)}")

print("¡Reemplazo de texto completado!")
