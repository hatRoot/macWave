import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_FOOTER_GRID = '''  <div class="container footer-grid" style="margin-top: 20px;">
  <div class="footer-col brand-info">
  <h3 style="font-size: 1.5em; color: var(--text-primary); margin-bottom: 8px;"><strong>macWave</strong>
  <span style="font-weight: 300;">México</span>
  </h3>
  <p class="tagline"
  style="font-style: normal; color: var(--accent-orange); font-weight: 700; margin-bottom: 12px; font-size: 0.85em;">
  Soporte de Reparaciones Apple desde hace 18 años.</p>
  <p style="font-size: 0.8em; color: var(--text-muted); margin-bottom: 12px;">Servicio Técnico Especializado Apple en CDMX. Diagnóstico honesto y reparación a nivel componente.</p>
  <p style="margin-top: 12px; font-weight: 600; font-size: 0.85em;">
  <a href="tel:5535757364" style="color: inherit; text-decoration: none; display: block; margin-bottom: 6px;">📞 55-3575-7364</a>
  <a href="mailto:contacto@macwave.com.mx" style="color: inherit; text-decoration: none; display: block; margin-bottom: 10px;">✉️ contacto@macwave.com.mx</a>
  </p>
  <div style="display:flex; align-items:center; gap:14px; margin-top: 10px;">
  <a href="https://www.facebook.com/macwavet2" target="_blank" rel="noopener noreferrer" aria-label="Facebook" style="color: inherit;">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
  <path d="M16 8.049C16 3.604 12.418 0 8 0S0 3.604 0 8.049C0 12.068 2.925 15.398 6.75 16v-5.625H4.719V8.049H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.875 0 1.79.158 1.79.158v1.98h-1.008c-.994 0-1.303.621-1.303 1.258v1.509h2.219l-.355 2.326H9.25V16C13.075 15.398 16 12.068 16 8.049z"/>
  </svg>
  </a>
  <a href="https://www.instagram.com/macwavet2" target="_blank" rel="noopener noreferrer" aria-label="Instagram" style="color: inherit;">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
  <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.27.222 2.76.42a5.4 5.4 0 0 0-1.95 1.27A5.4 5.4 0 0 0 .42 3.64c-.198.51-.332 1.09-.372 1.943C.01 6.436 0 6.709 0 8.88c0 2.17.01 2.444.048 3.297.04.853.174 1.433.372 1.943.26.67.624 1.24 1.07 1.686a5.4 5.4 0 0 0 1.95 1.27c.51.198 1.09.332 1.943.372.853.038 1.126.048 3.297.048s2.444-.01 3.297-.048c.853-.04 1.433-.174 1.943-.372a5.4 5.4 0 0 0 1.95-1.27 5.4 5.4 0 0 0 1.27-1.95c.198-.51.332-1.09.372-1.943.038-.853.048-1.126.048-3.297s-.01-2.444-.048-3.297c-.04-.853-.174-1.433-.372-1.943a5.4 5.4 0 0 0-1.27-1.95A5.4 5.4 0 0 0 13.24.42c-.51-.198-1.09-.332-1.943-.372C10.444.01 10.171 0 8 0m0 1.441c2.134 0 2.387.008 3.231.046.78.035 1.204.165 1.486.275.373.145.639.318.918.597.279.279.452.545.597.918.11.282.24.706.275 1.486.038.844.046 1.097.046 3.231s-.008 2.387-.046 3.231c-.035.78-.165 1.204-.275 1.486a3.96 3.96 0 0 1-.597.918 3.96 3.96 0 0 1-.918.597c-.282.11-.706.24-1.486.275-.844.038-1.097.046-3.231.046s-2.387-.008-3.231-.046c-.78-.035-1.204-.165-1.486-.275a3.96 3.96 0 0 1-.918-.597 3.96 3.96 0 0 1-.597-.918c-.11-.282-.24-.706-.275-1.486-.038-.844-.046-1.097-.046-3.231s.008-2.387.046-3.231c.035-.78.165-1.204.275-1.486.145-.373.318-.639.597-.918.279-.279.545-.452.918-.597.282-.11.706-.24 1.486-.275.844-.038 1.097-.046 3.231-.046"/><path d="M8 3.891A4.109 4.109 0 1 0 8 12.11 4.109 4.109 0 0 0 8 3.89m0 6.778A2.669 2.669 0 1 1 8 5.33a2.669 2.669 0 0 1 0 5.338m4.271-7.172a.96.96 0 1 1-1.92 0 .96.96 0 0 1 1.92 0"/></svg>
  </a>
  <a href="https://wa.me/525535757364" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp" style="color: inherit;">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
  <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326z"/>
  <path d="M7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zM11.609 9.587c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
  </svg>
  </a>
  </div>
  </div>

  <div class="footer-col">
  <h4>Servicios Principales</h4>
  <ul>
  <li><a href="bateria-macbook-cdmx">Cambio Batería MacBook</a></li>
  <li><a href="mac-mojada-cdmx">Reparación Mac Mojada</a></li>
  <li><a href="mantenimiento-macbook-cdmx">Mantenimiento Térmico</a></li>
  <li><a href="reparacion-imac-cdmx">Reparación iMac CDMX</a></li>
  <li><a href="cambio-bateria-macbook-pro-air">Baterías MacBook Pro y Air</a></li>
  <li><a href="bateria-pantalla-iphone-express">Batería y Pantalla iPhone</a></li>
  </ul>
  </div>

  <div class="footer-col">
  <h4>Reparación Lógica</h4>
  <ul>
  <li><a href="reparacion-corto-logica-mac">Reparación de Cortos</a></li>
  <li><a href="reparacion-flexgate-macbook">Reparación Flexgate</a></li>
  <li><a href="cambio-teclado-macbook-cdmx">Cambio Teclado Mac</a></li>
  <li><a href="reflow-gpu-mac">Reflow GPU MacBook</a></li>
  <li><a href="reparacion-laptops-gamer-cdmx">Laptops Gamer CDMX</a></li>
  <li><a href="reparaciones">Todas las Reparaciones</a></li>
  </ul>
  </div>

  <div class="footer-col">
  <h4>Upgrades & Soporte</h4>
  <ul>
  <li><a href="upgrades">Upgrades SSD y RAM</a></li>
  <li><a href="actualizar-mac-os-vieja">Actualizar macOS Viejo</a></li>
  <li><a href="empresas">Soporte Empresas</a></li>
  <li><a href="casos-reales">Casos Reales</a></li>
  <li><a href="software">Licencias Software</a></li>
  <li><a href="terminos">Términos y Condiciones</a></li>
  </ul>
  </div>
  </div>'''

GRID_REGEX = re.compile(r'<div class="container footer-grid"[^>]*>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>', re.MULTILINE)

def update_file_footer(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <div class="container footer-grid" ...> up to the end of that container
    start_str = '<div class="container footer-grid"'
    idx = content.find(start_str)
    if idx == -1:
        return False

    # Look for the footer-bottom-mini or closing footer
    end_marker = '<div class="footer-bottom-mini"'
    end_idx = content.find(end_marker, idx)
    if end_idx == -1:
        # Fallback to </footer>
        end_idx = content.find('</footer>', idx)
        if end_idx == -1:
            return False

    new_content = content[:idx] + NEW_FOOTER_GRID + '\n  \n  ' + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(ignored in root for ignored in ['.git', 'node_modules', 'legacy', 'scratch']):
            continue
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                if update_file_footer(full_path):
                    print(f"Updated footer in: {file}")
                    count += 1
    print(f"Total files updated: {count}")

if __name__ == '__main__':
    main()
