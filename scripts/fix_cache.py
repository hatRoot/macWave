import glob
import re

acsp_css = """
/* ACSP AUTHORITY BLOCK */
.acsp-authority-block {
    background: linear-gradient(135deg, #0a0a0a 0%, #000 100%);
    border-top: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: 60px 20px;
}
.acsp-container {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 40px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(212, 175, 55, 0.2);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), inset 0 0 20px rgba(212, 175, 55, 0.03);
    transition: transform 0.3s ease;
}
.acsp-container:hover {
    transform: translateY(-5px);
    border-color: rgba(212, 175, 55, 0.4);
}
.acsp-badge {
    text-align: center;
    color: #d4af37;
    border-right: 1px solid rgba(255,255,255,0.1);
    padding-right: 40px;
    flex-shrink: 0;
}
.acsp-text h3 {
    color: #fff;
    font-size: 1.8rem;
    margin-bottom: 15px;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.acsp-text p {
    color: #d4af37;
    font-size: 1.35rem;
    font-style: italic;
    font-weight: 600;
    line-height: 1.4;
    margin-bottom: 15px;
}
.acsp-text .acsp-sub {
    color: #a0a0a0;
    font-size: 0.95rem;
    font-style: normal;
    font-weight: 400;
    line-height: 1.6;
}
@media(max-width: 768px) {
    .acsp-container { flex-direction: column; text-align: center; padding: 30px 20px; gap: 20px; }
    .acsp-badge { border-right: none; border-bottom: 1px solid rgba(255,255,255,0.1); padding-right: 0; padding-bottom: 25px; width: 100%; }
}
"""

pages = [
    "cambio-bateria-macbook-pro-air.html",
    "cambio-teclado-macbook-cdmx.html",
    "mantenimiento-macbook-cdmx.html",
    "actualizar-mac-os-vieja.html",
    "bateria-pantalla-iphone-express.html",
    "reparacion-laptops-gamer-cdmx.html",
    "mac-mojada-urgencia.html",
    "reparacion-flexgate-macbook.html",
    "reparacion-corto-logica-mac.html",
    "reflow-gpu-mac.html",
    "reparacion-imac-cdmx.html"
]

for p in pages:
    path = f"/Users/joelduran/Documents/GitHub/MacWaveT2/{p}"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Update css version to force cache busting
        content = content.replace("style.css?v=26.0.0", "style.css?v=26.1.0")
        
        # 2. Inject CSS inline before </style> to guarantee loading
        if ".acsp-authority-block {" not in content:
            content = content.replace("</style>", f"{acsp_css}\n</style>")
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed CSS cache & injected ACSP styles in: {p}")
    except Exception as e:
        print(f"Error {p}: {e}")
