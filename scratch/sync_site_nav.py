#!/usr/bin/env python3
"""Sincroniza la barra de menú canónica en todas las páginas públicas."""

import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

LINKS = [
    ("reparaciones", "/reparaciones.html", "Reparaciones"),
    ("empresas", "/empresas.html", "Empresas"),
    ("software", "/software.html", "Software"),
    ("casos-reales", "/casos-reales.html", "Casos Reales"),
]

# Páginas públicas y sección activa en el menú
PAGES = {
    "index.html": None,
    "reparaciones.html": "reparaciones",
    "empresas.html": "empresas",
    "software.html": "software",
    "casos-reales.html": "casos-reales",
    "terminos.html": None,
    "bateria-macbook-cdmx.html": "reparaciones",
    "mac-mojada-cdmx.html": "reparaciones",
    "upgrades.html": "reparaciones",
    "actualizar-mac-os-vieja.html": "reparaciones",
    "bateria-pantalla-iphone-express.html": "reparaciones",
    "cambio-bateria-macbook-pro-air.html": "reparaciones",
    "cambio-teclado-macbook-cdmx.html": "reparaciones",
    "mac-mojada-urgencia.html": "reparaciones",
    "mantenimiento-macbook-cdmx.html": "reparaciones",
    "reparacion-corto-logica-mac.html": "reparaciones",
    "reparacion-flexgate-macbook.html": "reparaciones",
    "reparacion-imac-cdmx.html": "reparaciones",
    "reparacion-laptops-gamer-cdmx.html": "reparaciones",
    "reflow-gpu-mac.html": "reparaciones",
}

TOGGLE_SCRIPT = """  <script>
  // Definición global e inmediata para evitar fallos en iPhone
  function toggleMobileMenu(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    var body = document.body;
    var btn = document.getElementById('mobile-menu-toggle');
    var isNowActive = body.classList.toggle('menu-active');
    if (btn) {
      if (isNowActive) btn.classList.add('active');
      else btn.classList.remove('active');
    }
  }
  </script>"""


def nav_class(slug: str, active: Optional[str], prefix: str) -> str:
    base = f"{prefix}-link" if prefix == "nav" else "cloned-nav-link"
    return f'{base} active' if active == slug else base


def build_nav(active: Optional[str]) -> str:
    desktop_links = []
    mobile_links = []
    for i, (slug, href, label) in enumerate(LINKS, start=1):
        dc = nav_class(slug, active, "cloned")
        mc = nav_class(slug, active, "nav")
        desktop_links.append(f'        <a href="{href}" class="{dc}">{label}</a>')
        mobile_links.append(
            f'            <a href="{href}" class="{mc}" style="--i:{i}">{label}</a>'
        )

    return f"""  <!-- Cloned Top Bar -->
  <div class="cloned-topbar">
    <div class="container">
      <div class="cloned-topbar-left">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8 0a.5.5 0 0 1 .5.5v11.793l3.147-3.146a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 12.293V.5A.5.5 0 0 1 8 0zM0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5v-7z"/>
        </svg>
        <span>Servicio a domicilio sin costo en CDMX</span>
      </div>
      <div class="cloned-topbar-right">
        <div class="cloned-topbar-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
            <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
          </svg>
          <span>Lun - Vie: 9:00 - 18:00</span>
        </div>
        <a href="tel:5535757364" class="cloned-topbar-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
            <path d="M3.654 1.328a.678.678 0 0 0-.57-.383 1.834 1.834 0 0 0-1.424.59 2.76 2.76 0 0 0-.746 1.984c.159 1.488.948 3.013 2.119 4.185 1.171 1.171 2.697 1.96 4.185 2.119.8.086 1.583-.242 1.984-.746.39-.48.59-1.116.59-1.424a.678.678 0 0 0-.383-.57l-2.634-1.202a.678.678 0 0 0-.71.128l-.71.71a2.182 2.182 0 0 1-1.045-.51 2.182 2.182 0 0 1-.51-1.045l.71-.71a.678.678 0 0 0 .128-.71L3.654 1.328z"/>
          </svg>
          <span>55-3575-7364</span>
        </a>
        <a href="https://wa.me/525535757364?text=Hola%20me%20ayudas%20a%20reparar%20mi%20Mac%3F" target="_blank" rel="noopener noreferrer" class="cloned-topbar-item whatsapp-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
            <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z" />
          </svg>
          <span>WhatsApp</span>
        </a>
      </div>
    </div>
  </div>

  <!-- Cloned Main White Header -->
  <header class="cloned-header">
    <div class="container">
      <button class="mobile-menu-toggle" id="mobile-menu-toggle" aria-label="Abrir menú" onclick="toggleMobileMenu(event)">
        <span></span><span></span><span></span>
      </button>

      <div class="cloned-logo-container logo">
        <a href="/" class="logo-link">
          <img src="./images/negro.png" alt="Logo Mac Wave T2" class="logo-img">
          <div class="logo-text-container">
            <span class="logo-brand"><strong>macWave</strong> <span style="font-weight: 300;">México</span></span>
            <span class="logo-subtext">Para tu dispositivo Apple fuera de garantía</span>
          </div>
        </a>
      </div>

      <!-- Desktop Nav -->
      <nav class="cloned-nav">
{chr(10).join(desktop_links)}
      </nav>

      <!-- Reusing main-nav overlay structure for Mobile Slide Menu -->
      <nav class="main-nav">
        <button class="mobile-nav-close" onclick="toggleMobileMenu(event)" aria-label="Cerrar menú">✕</button>
        <div class="mobile-menu-content">
          <div class="mobile-nav-links">
{chr(10).join(mobile_links)}
          </div>
        </div>
      </nav>

      <a href="https://wa.me/525535757364?text=Hola%20me%20ayudas%20a%20reparar%20mi%20Mac%3F" target="_blank" rel="noopener noreferrer" class="cloned-header-cta">
        Solicitar servicio
      </a>
    </div>
  </header>
"""


def replace_header(content: str, nav: str) -> str:
    """Reemplaza bloque de navegación existente por el canónico."""
    if "cloned-topbar" in content or "emergency-ticker" in content or "urgency-today-bar" in content or "main-header" in content:
        # Intentar reemplazo desde comentario top bar / urgency / emergency
        patterns = [
            re.compile(
                r"<!--\s*Cloned Top Bar\s*-->[\s\S]*?</header>\s*",
                re.IGNORECASE,
            ),
            re.compile(
                r"<!--\s*URGENCY BAR\s*-->[\s\S]*?</header>\s*",
                re.IGNORECASE,
            ),
            re.compile(
                r"<!--\s*Emergency Ticker[\s\S]*?</header>\s*",
                re.IGNORECASE,
            ),
            re.compile(
                r"<div class=\"urgency-today-bar\">[\s\S]*?</header>\s*",
                re.IGNORECASE,
            ),
            re.compile(
                r"<div class=\"emergency-ticker\">[\s\S]*?</header>\s*",
                re.IGNORECASE,
            ),
            re.compile(
                r"<header class=\"main-header\">[\s\S]*?</header>\s*",
                re.IGNORECASE,
            ),
        ]
        for pat in patterns:
            if pat.search(content):
                return pat.sub(nav + "\n", content, count=1)

    return content


def ensure_head_assets(content: str) -> str:
    if "style.css" not in content:
        content = content.replace(
            "</head>",
            '  <link rel="stylesheet" href="style.css?v=26.3.0">\n</head>',
            1,
        )
    if "function toggleMobileMenu" not in content:
        content = content.replace("</head>", TOGGLE_SCRIPT + "\n</head>", 1)
    if 'script src="script.js' not in content:
        content = content.replace("</body>", '  <script src="script.js?v=26.0.0" defer></script>\n</body>', 1)
    return content


def process_terminos(content: str, nav: str) -> str:
    content = ensure_head_assets(content)
    if "cloned-topbar" not in content:
        content = content.replace(
            "<body>\n\n  <div class=\"container\">",
            "<body>\n\n" + nav + "\n  <main class=\"site-main legal-main\">\n  <div class=\"container\">",
            1,
        )
        if "</body>" in content and "</main>" not in content.split("<main")[0]:
            # Cerrar main antes del cierre de body
            content = re.sub(
                r"(\n</body>)",
                "\n  </main>\\1",
                content,
                count=1,
            )
    return content


def main():
    updated = []
    skipped = []

    for filename, active in PAGES.items():
        path = ROOT / filename
        if not path.exists():
            skipped.append(f"{filename} (no existe)")
            continue

        content = path.read_text(encoding="utf-8")
        nav = build_nav(active)

        if filename == "terminos.html":
            new_content = process_terminos(content, nav)
        else:
            new_content = replace_header(content, nav)
            new_content = ensure_head_assets(new_content)

        if new_content != content:
            path.write_text(new_content, encoding="utf-8")
            updated.append(filename)
        else:
            skipped.append(f"{filename} (sin cambios)")

    print("Actualizados:", len(updated))
    for f in updated:
        print("  ✓", f)
    if skipped:
        print("\nOmitidos / sin cambios:")
        for s in skipped:
            print("  -", s)


if __name__ == "__main__":
    main()
