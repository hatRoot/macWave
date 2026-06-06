import os
import re

pairs = {
    "actualizar-mac-os-vieja.html": ("computadoras.jpg", "ios26.png"),
    "bateria-pantalla-iphone-express.html": ("displayiphone1.jpeg", "iphone.png"),
    "cambio-bateria-macbook-pro-air.html": ("bateria_dolor.jpg", "bateria_solucion.jpg"),
    "cambio-teclado-macbook-cdmx.html": ("macbook1.png", "macbook2.png"),
    "mantenimiento-macbook-cdmx.html": ("milagro_mantenimiento.jpg", "mac-repair-logic.jpg"),
    "mac-mojada-urgencia.html": ("mac_mojada_dolor.jpg", "mac_mojada_solucion.jpg"),
    "reparacion-flexgate-macbook.html": ("reparacionmac1.jpeg", "imac.png"),
    "reparacion-corto-logica-mac.html": ("macbook-logic-board.jpg", "mac_board_repair.png"),
    "reflow-gpu-mac.html": ("circuito_bronce.jpg", "mac-repair-logic.jpg"),
    "reparacion-imac-cdmx.html": ("imac_repair_broken.png", "imac_repair_solution.png"),
    "reparacion-laptops-gamer-cdmx.html": ("multimarca.jpg", "dispositivos.jpg")
}

for filename, (img1, img2) in pairs.items():
    if not os.path.exists(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has pain-image
    if 'pain-image-wrapper' not in content:
        # insert before <div class="warning-symptoms">
        injection1 = f"""
            <div class="pain-image-wrapper" style="max-width: 500px; margin: 40px auto; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <img src="./images/{img1}" alt="Error en equipo Mac" style="width: 100%; display: block; filter: saturate(1.1) contrast(1.05);">
            </div>
"""
        content = content.replace('<div class="warning-symptoms">', injection1 + '            <div class="warning-symptoms">')
        
    if 'solution-image-wrapper' not in content:
        # insert before <div class="features-grid">
        injection2 = f"""
            <div class="solution-image-wrapper" style="max-width: 600px; margin: 40px auto 60px auto; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <img src="./images/{img2}" alt="Reparacion solucion Mac" style="width: 100%; display: block;">
            </div>
"""
        content = content.replace('<div class="features-grid">', injection2 + '            <div class="features-grid">')

    print(f"Modifying {filename}")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

