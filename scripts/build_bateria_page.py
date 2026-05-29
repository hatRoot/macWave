import os
import re

ROOT_DIR = '/Users/joelduran/Documents/GitHub/MacWaveT2'
REPARACIONES_FILE = os.path.join(ROOT_DIR, 'reparaciones.html')

p = {
    "filename": "cambio-bateria-macbook-pro-air.html",
    "meta_title": "🔋 Cambio Batería MacBook Pro y Air CDMX | 2 Años Garantía | macWave",
    "meta_desc": "Cambio express de batería para MacBook Pro y Air en CDMX. Baterías calidad original OEM con 2 años de garantía por escrito. Listo el mismo día.",
    "schema_name": "Cambio Express de Batería MacBook con Garantía",
    "schema_desc": "Servicio de sustitución de baterías degradadas o infladas en equipos Apple MacBook Pro y Air. Único centro con 2 Años de Garantía oficial.",
    "schema_sku": "MW-REP-BAT",
    "hero_badge": "🔋 2 Años de Garantía por Escrito",
    "hero_h1": "¿La batería de tu MacBook <span>dura menos de 2 horas o te marca 'Servicio Recomendado'?</span>",
    "hero_sub": "No corras el riesgo de que una batería inflada rompa tu trackpad. Hacemos el cambio en tiempo récord y te damos 2 AÑOS DE GARANTÍA, algo que ni la marca oficial te ofrece.",
    "hero_bg_style": "linear-gradient(135deg, #001a0d 0%, #0d0d0d 50%, #001a0d 100%)",
    "hero_symptoms": """
        <span class="symptom-tag">Dice 'Servicio Recomendado'</span>
        <span class="symptom-tag">Trackpad no hace click</span>
        <span class="symptom-tag">Se apaga al 30%</span>
        <span class="symptom-tag">Teclado levantado (Batería Inflada)</span>
    """,
    "hub_badge_class": "badge-green",
    "hub_badge_text": "⚡ Cero Degradación",
    "hub_h2": "Instalación Segura <span>y Rápida</span>",
    "hub_sub": "Para extraer las baterías pegadas con adhesivo industrial usamos solventes seguros que no dañan tu placa madre. Retiramos la anterior sin doblarla (peligro de fuego).",
    "theme_class": "green-theme",
    "features": """
            <div class="feature-card">
                <span class="feature-icon">🛡️</span>
                <h3>2 Años de Garantía Oficial</h3>
                <p>Nadie en México te da 2 años de garantía por escrito en baterías OEM. Nuestra calidad de celdas nos permite esa absoluta confianza.</p>
            </div>
            <div class="feature-card">
                <span class="feature-icon">⏱️</span>
                <h3>Tiempo Express</h3>
                <p>Las reparaciones de batería son uno de los servicios más solicitados. Entregamos el mismo día para que nunca dejes de trabajar.</p>
            </div>
            <div class="feature-card">
                <span class="feature-icon">🌿</span>
                <h3>Ciclos en Cero Reales</h3>
                <p>Las baterías de reemplazo cuentan con celdas de alto rendimiento nuevas y vírgenes que el sistema reconocerá con Condición Normal.</p>
            </div>
    """
}

acsp_block = """
        <!-- ACSP AUTHORITY BLOCK -->
        <section class="acsp-authority-block">
            <div class="acsp-container">
                <div class="acsp-badge">
                    <span style="font-size: 3rem; display: block; margin-bottom:10px;"> ACSP</span>
                    <strong>Apple Certified</strong><br>Support Professional
                </div>
                <div class="acsp-text">
                    <h3>18 Años de Experiencia Comprobables en CDMX</h3>
                    <p>"El talento de un ingeniero de laboratorio de microelectrónica, con la certificación oficial de la marca que fabricó tu equipo."</p>
                    <p class="acsp-sub">A diferencia de grandes tiendas que cambian piezas a precios absurdos o talleres amateurs de celular que experimentan en hardware pesado, nosotros combinamos reparación nivel componente con credenciales oficiales de Apple ACSP. No confíes tu herramienta de trabajo de $40,000 MXN en alguien más.</p>
                </div>
            </div>
        </section>
"""

with open(REPARACIONES_FILE, 'r', encoding='utf-8') as f:
    template = f.read()

header_part = template.split('<main>')[0] + '<main>'
footer_part = '</main>' + template.split('</main>')[1]

page_html = header_part
page_html = re.sub(r'<title>.*?</title>', f'<title>{p["meta_title"]}</title>', page_html)
page_html = re.sub(r'<meta name="description"\s+content=".*?">', f'<meta name="description" content="{p["meta_desc"]}">', page_html, flags=re.DOTALL)

main_content = f"""
    <!-- PAIN HERO -->
    <section class="pain-hero" style="background: {p["hero_bg_style"]}">
        <div class="pain-badge">{p["hero_badge"]}</div>
        <h1 class="pain-title">{p["hero_h1"]}</h1>
        <p class="pain-subtitle">{p["hero_sub"]}</p>

        <div class="warning-symptoms">
            {p["hero_symptoms"]}
        </div>
    </section>

    {acsp_block}

    <!-- SEC: HUB -->
    <section class="hub-section {p["theme_class"]}">
        <div class="hub-badge {p["hub_badge_class"]}">{p["hub_badge_text"]}</div>
        <h2 class="hub-title">{p["hub_h2"]}</h2>
        <p class="hub-subtitle">{p["hub_sub"]}</p>

        <div class="features-grid">
            {p["features"]}
        </div>
        <a href="https://wa.me/525535757364" class="hub-cta cta-blue" style="font-size: 1.1rem; padding: 14px 30px;">Consulta Gratuita por WhatsApp →</a>
    </section>
    
    <!-- FINAL CTA HUB -->
    <section class="cta-final-hub" style="padding: 100px 20px; background: #000;">
        <div class="cta-box" style="padding: 80px 40px; max-width: 800px; margin: 0 auto; background: rgba(0,0,0,0.4);">
            <h2 style="margin-bottom: 30px; font-size: 2.5rem; line-height: 1.3;">¿Estás de acuerdo en que la reparamos?</h2>
            <p style="margin-bottom: 40px; font-size: 1.2rem; line-height: 1.6; max-width: 600px; margin-left: auto; margin-right: auto; color:#aaa;">
                Envíame un mensaje de WhatsApp ahora mismo. Te daré una pre-cotización técnica franca, comprobando mi nivel de compromiso antes de que te muevas del sillón.
            </p>
            <a href="https://wa.me/525535757364" target="_blank" class="cta-wa-hub">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
                </svg>
                Contactar Ingeniero
            </a>
        </div>
    </section>
"""

full_html = page_html + main_content + footer_part

with open(os.path.join(ROOT_DIR, p["filename"]), 'w', encoding='utf-8') as fw:
    fw.write(full_html)
print(f"Gen: {p['filename']}")
