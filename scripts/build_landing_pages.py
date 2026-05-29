import json
import os
import re

# Base path
ROOT_DIR = '/Users/joelduran/Documents/GitHub/MacWaveT2'
REPARACIONES_FILE = os.path.join(ROOT_DIR, 'reparaciones.html')

pages_data = [
    {
        "filename": "cambio-teclado-macbook-cdmx.html",
        "meta_title": "⚡ Cambio de Teclado MacBook en CDMX | En 2 Horas | macWave",
        "meta_desc": "Reparación y cambio de teclado para MacBook Pro y Air en CDMX. Piezas originales, 2 años de garantía y técnicos nivel componente. ¡Cotiza por WhatsApp!",
        "schema_name": "Cambio de Teclado MacBook CDMX",
        "schema_desc": "Cambio de teclado original para todos los modelos de MacBook Pro y MacBook Air con garantía extendida.",
        "schema_sku": "MW-REP-KBD",
        "hero_badge": "⚠️ Teclas pegajosas o rotas",
        "hero_h1": "¿Tu teclado de MacBook <span>falla, se traban las teclas o le cayó agua?</span>",
        "hero_sub": "No cambies todo el top case por precios ridículos. Nosotros sustituimos únicamente el teclado dañado dejándola como nueva el mismo día.",
        "hero_bg_style": "linear-gradient(135deg, #1a0f00 0%, #0d0d0d 50%, #1a0f00 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Teclas dobles</span>
            <span class="symptom-tag">Barra espaciadora atascada</span>
            <span class="symptom-tag">Teclado de mariposa</span>
            <span class="symptom-tag">Touchbar sin luz</span>
        """,
        "hub_badge_class": "badge-orange",
        "hub_badge_text": "⌨️ Tacto Perfecto",
        "hub_h2": "Cambio de Teclado <span>Express y Garantizado</span>",
        "hub_sub": "Contamos con repuestos para modelos Retina, TouchBar y los nuevos M1, M2 y M3. Recupera la velocidad de escritura sin trucos.",
        "theme_class": "orange-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">⏱️</span>
                    <h3>Reparación Express</h3>
                    <p>En el 90% de los casos entregamos el mismo día. Sabemos que es tu herramienta de trabajo.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">💎</span>
                    <h3>Tacto Original</h3>
                    <p>Usamos repuestos OEM para que la presión y retroiluminación sean exactas a las de fábrica.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🛡️</span>
                    <h3>Remache Perfecto</h3>
                    <p>Aplicamos técnicas de remachado de fábrica, tu teclado no quedará hundido ni ruidoso.</p>
                </div>
        """
    },
    {
        "filename": "mantenimiento-macbook-cdmx.html",
        "meta_title": "🧹 Mantenimiento Preventivo MacBook CDMX | Limpieza Térmica | macWave",
        "meta_desc": "Tu Mac se calienta o hace ruido? Servicio especializado de mantenimiento térmico, limpieza de ventiladores y cambio de pasta térmica para MacBooks. CDMX.",
        "schema_name": "Mantenimiento Preventivo y Limpieza Térmica MacBook",
        "schema_desc": "Limpieza profunda de ventiladores, placa base y aplicación de pasta térmica de alto rendimiento para evitar daños mayores en procesadores Apple.",
        "schema_sku": "MW-SVC-MANT",
        "hero_badge": "🔥 Evita fallas costosas de tarjeta lógica",
        "hero_h1": "¿Tu Mac <span>se calienta demasiado o los ventiladores suenan como avión?</span>",
        "hero_sub": "El polvo obstruye el flujo de aire y seca la pasta térmica, llevando a tu procesador a temperaturas mortales. Rescátala a tiempo.",
        "hero_bg_style": "linear-gradient(135deg, #0d001a 0%, #0a0a0a 50%, #0d0d0d 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Muy caliente al tacto</span>
            <span class="symptom-tag">Se congela trabajando</span>
            <span class="symptom-tag">Kernel Panic</span>
            <span class="symptom-tag">Batería drena rápido</span>
        """,
        "hub_badge_class": "badge-purple",
        "hub_badge_text": "❄️ Enfriamiento Supremo",
        "hub_h2": "Mantenimiento de <span>Grado Industrial</span>",
        "hub_sub": "No le damos un 'soplido' por fuera. Desensamblamos a nivel milimétrico, limpiamos los disipadores y aplicamos pasta térmica premium.",
        "theme_class": "purple-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">🛠️</span>
                    <h3>Desarme Profundo</h3>
                    <p>Retiro seguro de todos los componentes para un lavado químico anti-estática de la carcasa interna.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">❄️</span>
                    <h3>Pasta Térmica Premium</h3>
                    <p>Sustituimos el compuesto de fábrica seco por pastas de conductividad extrema y duración prolongada.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">⚡</span>
                    <h3>Velocidad Recuperada</h3>
                    <p>Al no haber 'Thermal Throttling' (ahogo térmico), tu Mac vuelve a rendir al 100% de su capacidad.</p>
                </div>
        """
    },
    {
        "filename": "actualizar-mac-os-vieja.html",
        "meta_title": "🚀 Actualizar macOS en Mac Antigua | Revive tu equipo | macWave",
        "meta_desc": "¿Tu Mac ya no descarga Chrome o Office? Actualizamos sistemas operativos bloqueados por Apple a versiones modernas (Monterey, Sonoma) para darle 5 años más de vida.",
        "schema_name": "Actualización de macOS en Equipos Vintage",
        "schema_desc": "Servicio de parcheo de software e instalación de sistemas modernos en MacBooks e iMacs declaradas obsoletas por el fabricante.",
        "schema_sku": "MW-SW-UPG",
        "hero_badge": "💻 Dile adiós al aviso de 'Incompatible'",
        "hero_h1": "¿Tu Mac está perfecta físicamente pero <span>ya no puedes instalar apps ni navegar?</span>",
        "hero_sub": "Apple te empuja a comprar una máquina nueva bloqueando el software. Nosotros forzamos la instalación de un macOS moderno y seguro.",
        "hero_bg_style": "linear-gradient(135deg, #001f3f 0%, #0d0d0d 50%, #001f3f 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Netflix/YouTube no abre</span>
            <span class="symptom-tag">Safari sin soporte</span>
            <span class="symptom-tag">No instala Word</span>
            <span class="symptom-tag">Certificados CAD obsoletos</span>
        """,
        "hub_badge_class": "badge-blue",
        "hub_badge_text": "✨ Magia por Software",
        "hub_h2": "Revive tu inversión con <span>Sistemas Nuevos</span>",
        "hub_sub": "Equipos desde 2012 hasta 2017 volando con macOS Monterey, Ventura o Sonoma con total estabilidad y uso de iCloud.",
        "theme_class": "blue-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">🔓</span>
                    <h3>Software Desbloqueado</h3>
                    <p>Derribamos las barreras de Apple para que tengas compatibilidad con navegadores y apps modernas.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🛡️</span>
                    <h3>Seguridad Bancaria</h3>
                    <p>Un sistema viejo está lleno de virus. Un macOS nuevo te protege online al hacer transacciones.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">💰</span>
                    <h3>Ahorro Inmenso</h3>
                    <p>Invierte una fracción del costo de un equipo nuevo y sácale brillo al aluminio que todavía sirve.</p>
                </div>
        """
    },
    {
        "filename": "bateria-pantalla-iphone-express.html",
        "meta_title": "📱 Cambio de Batería y Pantalla de iPhone en CDMX | Exprés | macWave",
        "meta_desc": "Cambio de batería, display original y lavados químicos de iPhone el mismo día en CDMX. Servicio exprés sin engaños, piezas seleccionadas.",
        "schema_name": "Rescate Express iPhone Batería y Display",
        "schema_desc": "Cambios de batería sin error de capacidad y displays OEM para iPhone de gama alta con instalación el mismo día.",
        "schema_sku": "MW-IPH-EXP",
        "hero_badge": "⚡ Listo en el mismo día",
        "hero_h1": "Cambio exprés de <span>Batería y Display para iPhone</span>",
        "hero_sub": "Sin trucos. Resolvemos estallidos de pantalla, baterías degradadas y daños menores por líquido al instante. Especialistas en lo urgente.",
        "hero_bg_style": "linear-gradient(135deg, #111111 0%, #000000 50%, #111111 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Cristal roto</span>
            <span class="symptom-tag">Condición de batería en Servicio</span>
            <span class="symptom-tag">Pantalla parpadea</span>
            <span class="symptom-tag">Manchas de tinta</span>
        """,
        "hub_badge_class": "badge-green",
        "hub_badge_text": "🍏 Refacciones Premium",
        "hub_h2": "Reparaciones Exprés <span>Transparentes</span>",
        "hub_sub": "Soluciones fiables. OJO: No reparamos daño profundo en tarjeta lógica de FaceID ni fallas baseband complejas, elegimos brindar excelencia en lo vital.",
        "theme_class": "green-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">🔋</span>
                    <h3>Baterías sin 'Mensaje'</h3>
                    <p>Si es posible, transferimos el flexor para conservar la condición del 100% en configuración en modelos recientes.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">📱</span>
                    <h3>Displays OLED/LCD OEM</h3>
                    <p>Colores vivos y tacto idéntico al original. No pierdes True Tone en la instalación.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🚿</span>
                    <h3>Baño Químico</h3>
                    <p>¿Cayó a la piscina? Si lo traes el mismo día eliminamos el sarro antes de que la lógica colapse.</p>
                </div>
        """
    },
    {
        "filename": "reparacion-laptops-gamer-cdmx.html",
        "meta_title": "🎮 Reparación de Laptops Gamer Alta Gama CDMX | Alienware, ASUS, MSI",
        "meta_desc": "Soporte técnico avanzado para Laptops Gamer en CDMX. Alienware, ASUS ROG, MSI, Razer. Especialistas en cortos, mantenimiento extremo y GPU.",
        "schema_name": "Reparación Especializada de Laptops Gamer Serie Alta",
        "schema_desc": "Mantenimiento, des-corrosión y microelectrónica de placas base en Laptops de altas prestaciones Alienware, Asus ROG, Lenovo Legion y MSI.",
        "schema_sku": "MW-GAM-HV",
        "hero_badge": "👾 Restaura el rendimiento gráfico de tu equipo",
        "hero_h1": "¿Tu equipo de alto rendimiento <span>presenta fallos de video, no enciende o sufre sobrecalentamiento?</span>",
        "hero_sub": "Sabemos que tu estación de trabajo o equipo especializado es una inversión crítica. Aplicamos estándares de ingeniería a nivel componente para equipos de gama alta (Alienware, ASUS, MSI, Razer, Workstations).",
        "hero_bg_style": "linear-gradient(135deg, #1f0122 0%, #0d0d0d 50%, #001a1a 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Parpadea el teclado pero no da imagen</span>
            <span class="symptom-tag">Corto en conector de carga</span>
            <span class="symptom-tag">Fans a 100% ruidosos</span>
            <span class="symptom-tag">Muerta por agua/refresco</span>
        """,
        "hub_badge_class": "badge-purple",
        "hub_badge_text": "✨ Cirugía RGB",
        "hub_h2": "Soporte a Laptops de <span>Gama Entusiasta</span>",
        "hub_sub": "Las placas base Gamer sufren estrés térmico severo en el GPU y VRMs de poder. Encontramos los condensadores quemados sin cambiar el Motherboard completo.",
        "theme_class": "purple-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">🔬</span>
                    <h3>Reparación Fase de Poder</h3>
                    <p>Solución a cortos en líneas principales de poder (19V) y controladores IC quemados.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">❄️</span>
                    <h3>Metal Líquido / PTM7950</h3>
                    <p>Servicio VIP de conductividad térmica para bajar hasta 20°C y ganar FPS sostenidos en juegos.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">⚡</span>
                    <h3>Firmware y BIOS</h3>
                    <p>Recuperación de laptops 'briqueadas' durante actualizaciones corruptas inyectando el binario directo en chip.</p>
                </div>
        """
    },
    {
        "filename": "mac-mojada-urgencia.html",
        "meta_title": "💧 Rescate Urgente Mac Mojada CDMX | Baño Químico Nivel Componente",
        "meta_desc": "¿Cayó líquido a tu MacBook? No la enciendas. Limpieza ultrasónica urgente el mismo día para salvar el chip PCH y evitar daños irreversibles en Tarjeta Lógica.",
        "schema_name": "Rescate Crítico Mac Mojada Lógica",
        "schema_desc": "Baño químico ultrasónico y des-corrosión de líneas primarias PPBUS en MacBook tras derrames líquidos (agua, café, vino) para prevenir muerte de PCH/CPU.",
        "schema_sku": "MW-REP-LIQ",
        "hero_badge": "⏳ Tienes horas antes de la corrosión total",
        "hero_h1": "¿Derramaste líquido en la Mac? <span>Apágala y no la conectes a la corriente.</span>",
        "hero_sub": "El 80% de los equipos que nos traen EL MISMO DÍA se salvan de ser basura. El agua oxidará en horas la tarjeta lógica, fulminando el chip puente PCH y el Procesador. ¡Corre!",
        "hero_bg_style": "linear-gradient(135deg, #1c0f00 0%, #0d0d0d 50%, #1c0f00 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Cayó Café, Vino o Agua</span>
            <span class="symptom-tag">Se apagó de golpe</span>
            <span class="symptom-tag">Teclado chicloso</span>
            <span class="symptom-tag">Cargador no prende luz</span>
        """,
        "hub_badge_class": "badge-orange",
        "hub_badge_text": "🆘 Emergencia Quirúrgica",
        "hub_h2": "Desactivando <span>la Bomba de Relojería</span>",
        "hub_sub": "Un baño en arroz no sirve de absolutamente nada. La electricidad atrapada con minerales crea sarro que corroe el estaño al instante. Aplicamos limpieza química pura.",
        "theme_class": "orange-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">🚿</span>
                    <h3>Lavado Ultrasónico</h3>
                    <p>Sumergimos la placa en solventes anti-minerales vibrando a alta frecuencia para limpiar debajo del procesador.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🔍</span>
                    <h3>Detección de Corto G3H</h3>
                    <p>Trasladamos calorímetro para ver qué capacitores en líneas de 12V reventaron antes del daño de CPU.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">💼</span>
                    <h3>Rescate de tu Vida (NAND)</h3>
                    <p>Si la CPU ya está muerta, enfocamos nuestras máquinas en dar energía forzada solo al disco duro para sacar tus PDFs y fotos.</p>
                </div>
        """
    },
    {
        "filename": "reparacion-flexgate-macbook.html",
        "meta_title": "📺 Reparación Flexgate MacBook Pro | Corrección de luz pantalla | macWave",
        "meta_desc": "¿Tu MacBook Pro pierde luz al abrir la tapa o salen luces de escenario? Reparamos la falla crónica Flexgate Nivel Componente al instante, sin cambiar pantalla. CDMX.",
        "schema_name": "Reparación Falla Crónica Flexgate MacBook Pro",
        "schema_desc": "Reconstrucción y soldado de cable flexor backlight defectuoso (conocido como Flexgate) en equipos MacBook Pro A1706, A1708 sin tener que comprar display nuevo.",
        "schema_sku": "MW-REP-FXG",
        "hero_badge": "📐 El error de diseño de las MacBook Pro",
        "hero_h1": "¿A tu Mac le salen 'luces de escenario' o <span>se apaga la pantalla al abrirla a 90 grados?</span>",
        "hero_sub": "El temido problema del 'Flexgate'. Apple te cobrará Miles por una pantalla completa. Nosotros reconstruimos y soldamos un cable reforzado internamente por una fracción del costo.",
        "hero_bg_style": "linear-gradient(135deg, #0d1a0d 0%, #0d0d0d 50%, #0d1a0d 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Se ve oscura abajo (Teatro)</span>
            <span class="symptom-tag">Abro a más de 45° y se apaga</span>
            <span class="symptom-tag">Se ve con linterna</span>
            <span class="symptom-tag">Falla común A1708/A1706</span>
        """,
        "hub_badge_class": "badge-green",
        "hub_badge_text": "🛠️ Solución Definitiva",
        "hub_h2": "Venciendo el <span>Flexgate</span>",
        "hub_sub": "Con nuestros microscopios de precisión cortamos el flexor original corroído/doblado de backlight y soldamos extensiones permanentes más largas que ya no se romperán.",
        "theme_class": "green-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">💰</span>
                    <h3>Ahorro Inmenso</h3>
                    <p>Una pantalla nueva son arriba de $10,000. Nuestra micro-cirugía cobra únicamente el puente de cobre extendido.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🛡️</span>
                    <h3>Mejorado de Fábrica</h3>
                    <p>Al extender los milímetros de cable, la tensión en la bisagra desaparece y el problema no vuelve a pasar.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">⏱️</span>
                    <h3>Velocidad y Precisión</h3>
                    <p>Realizado en nuestro laboratorio local. Un procedimiento que requiere pulso de cirujano que tenemos dominado.</p>
                </div>
        """
    },
    {
        "filename": "reparacion-corto-logica-mac.html",
        "meta_title": "🔬 Reparación Tarjeta Lógica MacBook CDMX | Nivel Componente Experto",
        "meta_desc": "La MacStore te pidió cambiarla completa? Reparamos en corto tu Tarjeta Lógica de MacBook identificando condensadores e IC quemados uno a uno. Laboratorio Propio.",
        "schema_name": "Restauración Electrónica de Tarjeta Lógica Nivel Componente",
        "schema_desc": "Diagnóstico esquemático y reemplazo de SMD, PMIC y líneas de resistencia baja en circuitos impresos de dispositivos Apple portátiles.",
        "schema_sku": "MW-REP-BD",
        "hero_badge": "🛑 Diagnósticos letales sin esperanza revividos",
        "hero_h1": "Si te dijeron que 'Se quemó la tarjeta electrónica', <span>bienvenido al lugar correcto.</span>",
        "hero_sub": "Somos especialistas de diagnóstico profundo. Donde otros centros solo atornillan partes, nosotros leemos diagramas eléctricos y cambiamos ese minúsculo chip de 1 milímetro que causa el caos.",
        "hero_bg_style": "linear-gradient(135deg, #001018 0%, #0d0d0d 50%, #001018 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Muerta, no hay sonido ni luz</span>
            <span class="symptom-tag">El Trackpad no hace 'Click' Mágico</span>
            <span class="symptom-tag">Pantalla ilumina pero sin manzana</span>
            <span class="symptom-tag">Presupuesto inasumible por Apple</span>
        """,
        "hub_badge_class": "badge-blue",
        "hub_badge_text": "🔬 Ingeniería Inversa",
        "hub_h2": "Dominando los <span>Milivoltios</span>",
        "hub_sub": "Rastreamos las líneas I2C de datos, voltajes parásitos y el famoso PMIC para encontrar la fuga que impide despertar a tu Mac. Pura ciencia electrónica pura.",
        "theme_class": "blue-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">📡</span>
                    <h3>Cámaras Térmicas</h3>
                    <p>Usamos tecnología Flir térmica para observar qué microscópico condensador se ilumina a más de 100°C en falso rojo vivo.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🗺️</span>
                    <h3>Esquemáticos Originales</h3>
                    <p>Poseemos los planos confidenciales de diseño y la placa para seguir la ruta de poder desde el cargador USB-C hasta la batería.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">✨</span>
                    <h3>Apenas un rasguño</h3>
                    <p>Quitas un diminuto cubo cerámico de 1mm de área, sueldas uno nuevo, y el equipo vuelve a la vida por el 80% menos del costo oficial.</p>
                </div>
        """
    },
    {
        "filename": "reflow-gpu-mac.html",
        "meta_title": "📺 Reparación GPU e Imagen Mac | Reflow Gráfico Especializado | macWave",
        "meta_desc": "La imagen de tu Mac parpadea, tiene mosaicos, colores raros o no pasa de la barra? Reparación de tarjeta gráfica (GPU) en iMac y MacBook en CDMX.",
        "schema_name": "Corrección de Defectos en Chip Gráfico GPU Mac",
        "schema_desc": "Servicio de Reflow y diagnóstico en fallas masivas de imagen derivadas del excesivo estrés térmico de los chips video AMD Radeon o Nvidia.",
        "schema_sku": "MW-REP-GPU",
        "hero_badge": "🔥 Fallas de Soldadura BGA por estrés térmico",
        "hero_h1": "¿Tu Mac arranca pero <span>la pantalla tiene rayas, mosaicos imposibles o barra truncada?</span>",
        "hero_sub": "Estos son síntomas clásicos de muerte temporal en el chip de video integrado (GPU). El calor reventó las micro-esferas de estaño que adhieren el chip a la placa madre.",
        "hero_bg_style": "linear-gradient(135deg, #100018 0%, #0d0d0d 50%, #100018 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Rayas rosas o amarillas</span>
            <span class="symptom-tag">Se queda a 3/4 de barra de carga</span>
            <span class="symptom-tag">Pantalla blanca eterna</span>
            <span class="symptom-tag">El sistema arroja Kernel Panic GPU</span>
        """,
        "hub_badge_class": "badge-purple",
        "hub_badge_text": "🌡️ Alta Temperatura VIP",
        "hub_h2": "Reflow controlado <span>y seguro</span>",
        "hub_sub": "Utilizamos estaciones de calor especializadas y flux de alto rendimiento para derretir la soldadura oculta permitiendo que haga contacto perfecto de nuevo.",
        "theme_class": "purple-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">🌡️</span>
                    <h3>Curvas de Temperatura Infrarroja</h3>
                    <p>Sometemos tu tarjeta a una rampa gradual de 200 a 240 grados controlados para no deformar o doblar el procesador de video adyacente.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">❄️</span>
                    <h3>Extensión de vida (Mods Térmicos)</h3>
                    <p>Después de reparar el daño, evitamos que vuelva a pasar mejorando la disipación original e incluso programando los ventiladores al 50% vía Software preventivo.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">✅</span>
                    <h3>Asesoría Honesta</h3>
                    <p>Si determinamos que el chip está partido por desgaste físico extremo, te decimos con claridad lo irrecuperable de la situación sin hacerte gastar de más.</p>
                </div>
        """
    },
    {
        "filename": "reparacion-imac-cdmx.html",
        "meta_title": "🖥️ Reparación iMac CDMX | Centros de Trabajo Mac Especializados",
        "meta_desc": "Laboratorio central para reparación de equipos pesados iMac 21, 24 y 27 pulgadas en CDMX. Pantallas, fuentes de poder de alto voltaje, SSD M2.",
        "schema_name": "Centro de Servicio Autorizado Alternativo para iMac Sobremesa",
        "schema_desc": "Reparaciones quirúrgicas de sobremesas All-In-One iMac. Eliminación de fallas de alto voltaje, recableado interno y sellado hermético OEM.",
        "schema_sku": "MW-REP-IMC",
        "hero_badge": "🏛️ Las bestias de Apple en buenas manos",
        "hero_h1": "Servicio Técnico Premium para iMac: <span>Restaura tu Estación de Trabajo</span>",
        "hero_sub": "Las pesadas iMac conllevan riesgos de altos voltajes AC y fuentes de poder peligrosas. Somos uno de los pocos talleres que desarma, sella y repara iMacs.",
        "hero_bg_style": "linear-gradient(135deg, #001f3f 0%, #0d0d0d 50%, #001f3f 100%)",
        "hero_symptoms": """
            <span class="symptom-tag">Se le mete el polvo a la pantalla</span>
            <span class="symptom-tag">Se apaga de la nada</span>
            <span class="symptom-tag">Hizo chispa / Olor eléctrico</span>
            <span class="symptom-tag">Quiero pasar del disco lento HDD a M.2 SSD</span>
        """,
        "hub_badge_class": "badge-blue",
        "hub_badge_text": "🛠️ Manejo Técnico iMac",
        "hub_h2": "Reparamos a Gran <span>Escala Todo-en-Uno</span>",
        "hub_sub": "Cortar el cristal pegado de una iMac de 27 pulgadas toma herramientas únicas y cintas TESA originales para que la pantalla no se estrelle a los 3 meses en tu casa o se despegue. Nosotros lo hacemos bajo estándar industrial.",
        "theme_class": "blue-theme",
        "features": """
                <div class="feature-card">
                    <span class="feature-icon">🔌</span>
                    <h3>Fuentes de Poder Internas</h3>
                    <p>La fuente ATX en la parte de atrás de la iMac absorbe todos los picos de voltaje mexicanos. Sustituimos mosfets blindando el futuro voltaje.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🚀</span>
                    <h3>Adiós a Fusion Drive - Hola NVMe</h3>
                    <p>Eliminamos el terror del viejo disco duro mecánico que hace tu iMac de $60,000 inusable por lentitud. SSDs 5,000MB/s reales.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🛡️</span>
                    <h3>Sellado Milimétrico Original</h3>
                    <p>No usamos cinta doble cara de papelería. Aplicamos bandas TESA y rodillos oficiales para un ensamblado impecable a presión tal como Apple lo pensó.</p>
                </div>
        """
    }
]

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

# We need to extract:
# 1. Everything before the <main> tag (including header)
# 2. Everything after the </main> tag (footer)
# 3. And we construct the main manually.

header_part = template.split('<main>')[0] + '<main>'
footer_part = '</main>' + template.split('</main>')[1]

# Now, we make the landing generator.
for p in pages_data:
    page_html = header_part
    
    # Replace meta tags in header_part
    page_html = re.sub(r'<title>.*?</title>', f'<title>{p["meta_title"]}</title>', page_html)
    page_html = re.sub(r'<meta name="description"\s+content=".*?">', f'<meta name="description" content="{p["meta_desc"]}">', page_html, flags=re.DOTALL)
    
    # Re-write the JSON-LD inside header_part to avoid hard complex regex
    # Well, let's just do a simple replacement for the schema values if they exist, or not touch it.
    
    # Generating the injected MAIN content
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

print("DONE.")
