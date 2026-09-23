import os
import re

svg_icons = {
    'shield': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M5.338 1.59a61.44 61.44 0 0 0-2.837.856.481.481 0 0 0-.328.39c-.554 4.157.726 7.19 2.253 9.188a10.725 10.725 0 0 0 2.287 2.233c.346.244.652.42.893.533.12.057.218.095.293.118a.55.55 0 0 0 .101.025.615.615 0 0 0 .1-.025c.076-.023.174-.061.294-.118.24-.113.547-.29.893-.533a10.726 10.726 0 0 0 2.287-2.233c1.527-1.997 2.807-5.031 2.253-9.188a.48.48 0 0 0-.328-.39c-.651-.213-1.75-.56-2.837-.855C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.524zM5.072.56C6.157.265 7.31 0 8 0s1.843.265 2.928.56c1.11.3 2.229.655 2.887.87a1.54 1.54 0 0 1 1.044 1.262c.596 4.477-.787 7.795-2.465 9.99a11.775 11.775 0 0 1-2.517 2.453 7.159 7.159 0 0 1-1.048.625c-.28.132-.581.24-.829.24s-.548-.108-.829-.24a7.158 7.158 0 0 1-1.048-.625 11.777 11.777 0 0 1-2.517-2.453C1.928 10.487.545 7.169 1.141 2.692A1.54 1.54 0 0 1 2.185 1.43 62.456 62.456 0 0 1 5.072.56z"/><path d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"/></svg>',
    'clock': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/></svg>',
    'battery': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M2 6h10v4H2V6z"/><path d="M2 4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H2zm10 1a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h10zm4 3a1.5 1.5 0 0 1-1.5 1.5v-3A1.5 1.5 0 0 1 16 8z"/></svg>',
    'droplet': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M7.21.8C7.69.295 8 0 8 0c.109.363.234.708.371 1.038.812 1.946 2.073 3.35 3.197 4.6 1.205 1.343 2.166 2.609 2.166 4.162 0 3.22-2.55 5.7-5.734 5.7C4.78 15.5 2.25 13.02 2.25 9.8c0-1.553.96-2.82 2.166-4.163 1.123-1.25 2.384-2.654 3.197-4.6.137-.33.262-.675.371-1.038zM3.75 9.8c0 2.404 1.895 4.2 4.25 4.2 2.355 0 4.234-1.796 4.234-4.2 0-1.08-.72-2.115-1.782-3.3-1.077-1.202-2.223-2.48-2.452-4.195-.229 1.716-1.375 2.993-2.452 4.195C4.47 7.685 3.75 8.72 3.75 9.8z"/></svg>',
    'search': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/></svg>',
    'briefcase': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm3 1a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5h3zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l3.614 1.764a1.5 1.5 0 0 0 1.354 0L8 7.82l1.932 1.094a1.5 1.5 0 0 0 1.454 0z"/></svg>',
    'tool': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M1 0 0 1l2.2 3.081a1 1 0 0 0 .815.419h.07a1 1 0 0 1 .708.293l2.675 2.675-2.617 2.654A3.003 3.003 0 0 0 0 13a3 3 0 1 0 5.878-.851l2.654-2.617.968.968-.305.914a1 1 0 0 0 .242 1.023l3.27 3.27a.997.997 0 0 0 1.414 0l1.586-1.586a.997.997 0 0 0 0-1.414l-3.27-3.27a1 1 0 0 0-1.023-.242L10.5 9.5l-.96-.96 2.68-2.643A3.005 3.005 0 0 0 16 3c0-.269-.035-.53-.102-.777l-2.14 2.141L12 4l-.364-1.757L13.777.102a3 3 0 0 0-3.675 3.68L7.462 6.46 4.793 3.793a1 1 0 0 1-.293-.707v-.071a1 1 0 0 0-.419-.814L1 0zm9.646 10.646a.5.5 0 0 1 .708 0l2.914 2.915a.5.5 0 0 1-.707.707l-2.915-2.914a.5.5 0 0 1 0-.708zM3 11l.471.242 1.115.197-.495.744L4 13l-.328-.535-.867-.282.695-.561.428-.485-.928-.137z"/></svg>',
    'lightning': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M11.251.068a.5.5 0 0 1 .454.579L10.437 6.5H14a.5.5 0 0 1 .374.832l-9 10a.5.5 0 0 1-.828-.475l1.267-5.857H2a.5.5 0 0 1-.374-.832l9-10a.5.5 0 0 1 .625-.1z"/></svg>',
    'chip': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M5 0a.5.5 0 0 1 .5.5V2h1V.5a.5.5 0 0 1 1 0V2h1V.5a.5.5 0 0 1 1 0V2h1V.5a.5.5 0 0 1 1 0V2A2.5 2.5 0 0 1 14 4.5h1.5a.5.5 0 0 1 0 1H14v1h1.5a.5.5 0 0 1 0 1H14v1h1.5a.5.5 0 0 1 0 1H14v1h1.5a.5.5 0 0 1 0 1H14a2.5 2.5 0 0 1-2.5 2.5v1.5a.5.5 0 0 1-1 0V14h-1v1.5a.5.5 0 0 1-1 0V14h-1v1.5a.5.5 0 0 1-1 0V14h-1v1.5a.5.5 0 0 1-1 0V14A2.5 2.5 0 0 1 2 11.5H.5a.5.5 0 0 1 0-1H2v-1H.5a.5.5 0 0 1 0-1H2v-1H.5a.5.5 0 0 1 0-1H2v-1H.5a.5.5 0 0 1 0-1H2A2.5 2.5 0 0 1 4.5 2V.5A.5.5 0 0 1 5 0zm-1.5 3A1.5 1.5 0 0 0 2 4.5v7A1.5 1.5 0 0 0 3.5 13h9a1.5 1.5 0 0 0 1.5-1.5v-7A1.5 1.5 0 0 0 12.5 3h-9zM5 5h6v6H5V5z"/></svg>',
    'check': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z"/></svg>',
    'plug': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M6 0a.5.5 0 0 1 .5.5V3h3V.5a.5.5 0 0 1 1 0V3h1a.5.5 0 0 1 .5.5v3A3.5 3.5 0 0 1 8.5 10H8v4.5a.5.5 0 0 1-1 0V10h-.5A3.5 3.5 0 0 1 3 6.5v-3a.5.5 0 0 1 .5-.5h1V.5a.5.5 0 0 1 .5-.5z"/></svg>',
    'rocket': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 6.293V.5A.5.5 0 0 1 8 0zm-2.5 12a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1-.5-.5zm-2 2a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 0 1H4a.5.5 0 0 1-.5-.5z"/></svg>',
    'desktop': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M0 1.5A1.5 1.5 0 0 1 1.5 0h13A1.5 1.5 0 0 1 16 1.5v9a1.5 1.5 0 0 1-1.5 1.5h-5.06a.5.5 0 0 0-.442.276l-.736 1.472A.5.5 0 0 1 7.82 14h-1.64a.5.5 0 0 1-.442-.252l-.736-1.472A.5.5 0 0 0 4.56 12H1.5A1.5 1.5 0 0 1 0 10.5v-9zM1.5 1a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h13a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-13z"/></svg>',
    'ram': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M2 2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H2zm2 3.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-5zm5 0a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-5z"/></svg>',
    'disc': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M10 8a2 2 0 1 1-4 0 2 2 0 0 1 4 0zM8 4a4 4 0 0 0-4 4 .5.5 0 0 1-1 0 5 5 0 0 1 5-5 .5.5 0 0 1 0 1z"/></svg>',
    'apple': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 170 170"><path d="M150.37 130.25c-2.45 5.66-5.35 10.87-8.71 15.66-4.58 6.53-8.33 11.05-11.22 13.56-4.48 4.12-9.28 6.23-14.42 6.35-3.69 0-8.14-1.05-13.32-3.18-5.19-2.12-9.97-3.17-14.34-3.17-4.58 0-9.49 1.05-14.75 3.17-5.26 2.13-9.5 3.24-12.74 3.35-4.35.13-9.16-1.9-14.42-6.08-3.7-3.04-7.6-7.85-11.7-14.42-6.1-9.79-10.74-21.45-13.91-34.98-3.17-13.53-4.76-26.11-4.76-37.74 0-14.68 3.59-26.68 10.77-36 7.18-9.32 16.3-14.15 27.35-14.48 4.47 0 9.79 1.17 15.96 3.51 6.17 2.34 10.15 3.57 11.95 3.7 2.24-.26 6.53-1.63 12.87-4.12 6.34-2.48 11.83-3.64 16.48-3.48 12.28.65 22.38 5.25 30.28 13.8-10.77 6.53-16.03 15.56-15.79 27.1.33 9.14 4.02 16.86 11.07 23.18 7.05 6.31 15.35 10.01 24.89 11.1-2.28 6.96-5.06 14.14-8.34 21.54zM119.22 31.85c-.13-3.59 1.04-7.4 3.51-11.42 2.47-4.03 5.92-7.29 10.35-9.79-3.48-4.24-7.72-7.39-12.72-9.46-5-2.06-9.89-2.88-14.68-2.45-.65 3.8.38 7.72 3.09 11.75 2.72 4.02 6.19 7.29 10.45 9.8 4.26 2.5 8.16 3.69 11.7 3.57-.44-2.61-.7-5.03-.7-7.25z"/></svg>',
    'gem': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M3.1.7a.5.5 0 0 1 .4-.2h9a.5.5 0 0 1 .4.2l2.976 3.974c.149.185.156.45.01.644L8.4 15.3a.5.5 0 0 1-.8 0L.1 5.318a.5.5 0 0 1 .01-.644L3.1.7zm.864 1.3L1.583 4.5h3.474L4.064 2zm1.488 0l1.103 2.5h2.69l1.103-2.5H5.452zm4.484 0l-.993 2.5h3.474L10.436 2zm2.08 3.5H9.516l-1.516 6.064 5.016-6.064zm-5.032 0H3.484l5.016 6.064-1.516-6.064zm1.516 6.064V5.5H7.5v6.064z"/></svg>',
    'target': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M8 13A5 5 0 1 1 8 3a5 5 0 0 1 0 10zm0 1A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/><path d="M8 11A3 3 0 1 1 8 5a3 3 0 0 1 0 6zm0 1A4 4 0 1 0 8 4a4 4 0 0 0 0 8z"/><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/></svg>',
    'chart': '<svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16"><path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/></svg>'
}

# Mapping of emojis to SVG
emoji_to_svg = {
    '🛡️': svg_icons['shield'],
    '⏱️': svg_icons['clock'],
    '🌿': svg_icons['battery'],
    '🔋': svg_icons['battery'],
    '🚿': svg_icons['droplet'],
    '🔍': svg_icons['search'],
    '💼': svg_icons['briefcase'],
    '🛠️': svg_icons['tool'],
    '❄️': svg_icons['tool'],
    '⚡': svg_icons['lightning'],
    '🌡️': svg_icons['tool'],
    '✅': svg_icons['check'],
    '📡': svg_icons['chip'],
    '🗺️': svg_icons['chip'],
    '✨': svg_icons['gem'],
    '💰': svg_icons['shield'],
    '🔌': svg_icons['plug'],
    '🚀': svg_icons['rocket'],
    '👾': svg_icons['chip'],
    '🔬': svg_icons['chip'],
    '🖥️': svg_icons['desktop'],
    '📊': svg_icons['chart'],
    '💧': svg_icons['droplet'],
    '💾': svg_icons['ram'],
    '💿': svg_icons['disc'],
    '🧠': svg_icons['chip'],
    '🍎': svg_icons['apple'],
    '💎': svg_icons['gem'],
    '🎯': svg_icons['target']
}

page_metadata = {
    'reparacion-corto-logica-mac.html': {
        'title': 'Tarjeta Lógica y Mac Mojada CDMX | Si No Prende Ven Hoy',
        'desc': '¿Tu MacBook se mojó o no prende? Reparación a nivel microelectrónica sin cambiar la placa completa. Rescatamos tu equipo e información el mismo día.',
        'wa_intent': 'Hola%20macWave%2C%20necesito%20reparaci%C3%B3n%20urgente%20de%20tarjeta%20l%C3%B3gica%20para%20MacBook%20que%20no%20prende.'
    },
    'mac-mojada-cdmx.html': {
        'title': 'Reparación Mac Mojada CDMX | Baño Químico Mismo Día',
        'desc': 'Laboratorio de rescate para MacBook mojada en CDMX. Detenemos la corrosión y reparamos cortos en tarjeta lógica el mismo día. Diagnóstico certero.',
        'wa_intent': 'Hola%20macWave%2C%20se%20moj%C3%B3%20mi%20MacBook%20y%20requiero%20lavado%20qu%C3%ADmico%20urgente%20el%20mismo%20d%C3%ADa.'
    },
    'mac-mojada-urgencia.html': {
        'title': 'Mac Mojada CDMX Urgente | Baño Químico y Rescate Hoy',
        'desc': '¿Se cayó agua o café en tu MacBook? No la prendas. Baño ultrasónico y reparación de cortos hoy mismo en CDMX. Salva tu equipo e información.',
        'wa_intent': 'Hola%20macWave%2C%20urgencia%20extrema%3A%20se%20cay%C3%B3%20l%C3%ADquido%20en%20mi%20MacBook%20y%20necesito%20salvarla%20hoy.'
    },
    'upgrades.html': {
        'title': 'Actualizar Mac e iMac CDMX | 10x Más Rápida y macOS Nuevo',
        'desc': 'Haz tu Mac o iMac hasta 10 veces más rápida con disco SSD NVMe y más RAM. Instalamos macOS Sequoia o Sonoma para correr todas tus apps sin trabas.',
        'wa_intent': 'Hola%20macWave%2C%20quiero%20repotenciar%20mi%20Mac%20con%20SSD%20NVMe%20y%20actualizar%20sistema%20operativo%20macOS.'
    },
    'reparacion-imac-cdmx.html': {
        'title': 'Repotenciación iMac CDMX | Disco SSD 10x y macOS Actual',
        'desc': '¿Tu iMac está lenta o no actualiza? Cambiamos a disco SSD ultrarrápido y sistema operativo actual. Multiplica su velocidad por 10 hoy en CDMX.',
        'wa_intent': 'Hola%20macWave%2C%20mi%20iMac%20est%C3%A1%20muy%20lenta%20y%20quiero%20ponerle%20SSD%20ultrarr%C3%A1pido%20y%20macOS%20actual.'
    },
    'actualizar-mac-os-vieja.html': {
        'title': 'Actualizar macOS en Mac Vieja CDMX | Apps y Soporte Hoy',
        'desc': '¿Tu Mac ya no descarga apps por sistema viejo? Instalamos versiones recientes de macOS con compatibilidad total y máxima velocidad. Cotiza en CDMX.',
        'wa_intent': 'Hola%20macWave%2C%20necesito%20actualizar%20macOS%20en%20mi%20Mac%20antigua%20para%20poder%20descargar%20mis%20aplicaciones.'
    },
    'reparaciones.html': {
        'title': 'Servicio Técnico Mac CDMX | Baterías y Microelectrónica',
        'desc': 'Laboratorio especializado Apple en CDMX. Baterías con 2 años de garantía, rescate de Mac mojada y reparación de tarjeta lógica. Cotiza en 5 min.',
        'wa_intent': 'Hola%20macWave%2C%20solicito%20diagn%C3%B3stico%20especializado%20para%20mi%20equipo%20Apple%20en%20su%20laboratorio.'
    },
    'cambio-teclado-macbook-cdmx.html': {
        'title': 'Cambio de Teclado MacBook CDMX | Teclas y Fallas Hoy',
        'desc': '¿Teclas pegadas o sin responder en tu MacBook? Cambio de teclado original e individual sin cambiar todo el topcase. Entrega express en CDMX.',
        'wa_intent': 'Hola%20macWave%2C%20necesito%20cambio%20de%20teclado%20para%20MacBook%20porque%20tengo%20teclas%20que%20fallan.'
    },
    'mantenimiento-macbook-cdmx.html': {
        'title': 'Mantenimiento MacBook CDMX | Pasta Térmica y Limpieza',
        'desc': '¿Tu MacBook se calienta o hace ruido el ventilador? Mantenimiento preventivo, limpieza interna profunda y cambio de pasta térmica de alto nivel.',
        'wa_intent': 'Hola%20macWave%2C%20mi%20MacBook%20se%20calienta%20mucho%20y%20requiero%20mantenimiento%20profundo%20con%20pasta%20t%C3%A9rmica.'
    },
    'reparacion-flexgate-macbook.html': {
        'title': 'Reparación Flexgate MacBook CDMX | Falla Luz de Pantalla',
        'desc': '¿La luz de tu MacBook Pro falla al abrir la tapa? Reparamos el cable Flexgate a nivel micro-soldadura sin cambiar la pantalla completa. Cotiza ya.',
        'wa_intent': 'Hola%20macWave%2C%20mi%20MacBook%20Pro%20tiene%20falla%20Flexgate%20%28se%20apaga%20la%20luz%20al%20abrirla%29%2C%20solicito%20cotizaci%C3%B3n.'
    },
    'reflow-gpu-mac.html': {
        'title': 'Reparación Chip de Video Mac CDMX | Reballing y Gráficos',
        'desc': '¿Tu Mac tiene rayas o pantalla en negro? Reparación de GPU y tarjeta de video a nivel componente con garantía por escrito. Diagnóstico en CDMX.',
        'wa_intent': 'Hola%20macWave%2C%20mi%20Mac%20tiene%20fallas%20de%20video%20y%20requiero%20reparaci%C3%B3n%20de%20chip%20gr%C3%A1fico.'
    },
    'reparacion-laptops-gamer-cdmx.html': {
        'title': 'Reparación Laptops Gamer CDMX | Cortos y Tarjeta Madre',
        'desc': 'Servicio técnico de microelectrónica para laptops gamer en CDMX. Reparación de fuentes de poder, cortos y sobrecalentamiento. Garantía por escrito.',
        'wa_intent': 'Hola%20macWave%2C%20solicito%20reparaci%C3%B3n%20electr%C3%B3nica%20para%20laptop%20gamer%20con%20falla%20en%20placa.'
    },
    'empresas.html': {
        'title': 'Soporte Técnico Apple Empresas CDMX | Pólizas y Servicio',
        'desc': 'Mantenimiento preventivo y correctivo de flotillas Mac para empresas en CDMX. Facturación, atención prioritaria y técnicos certificados Apple.',
        'wa_intent': 'Hola%20macWave%2C%20solicito%20informaci%C3%B3n%20de%20soporte%20t%C3%A9cnico%20y%20mantenimiento%20para%20flotillas%20Mac%20corporativas.'
    },
    'software.html': {
        'title': 'Instalación de Software Mac CDMX | Licencias y Respaldo',
        'desc': 'Instalación y configuración de software profesional para macOS en CDMX. Paqueterías de diseño, arquitectura, ofimática y respaldo de datos seguro.',
        'wa_intent': 'Hola%20macWave%2C%20necesito%20instalaci%C3%B3n%20y%20configuraci%C3%B3n%20de%20software%20profesional%20en%20mi%20Mac.'
    },
    'casos-reales.html': {
        'title': 'Casos de Éxito Reparación Mac CDMX | macWave México',
        'desc': 'Conoce casos reales de MacBooks e iMacs rescatadas de cortos graves, derrames de líquidos y fallas complejas que en otros lugares daban por perdidas.',
        'wa_intent': 'Hola%20macWave%2C%20vi%20sus%20casos%20de%20%C3%A9xito%20y%20tengo%20un%20equipo%20con%20falla%20dif%C3%ADcil%20que%20quiero%20revisar.'
    },
    'terminos.html': {
        'title': 'Términos y Condiciones | macWave México Reparación Mac',
        'desc': 'Términos de servicio, garantías por escrito de hasta 2 años y políticas de privacidad del laboratorio especializado Apple macWave en la CDMX.',
        'wa_intent': 'Hola%20macWave%2C%20tengo%20una%20consulta%20sobre%20sus%20servicios%20y%20garant%C3%ADas.'
    }
}

def clean_page(filename):
    if not os.path.exists(filename):
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. Update Title & Meta description if configured
    if filename in page_metadata:
        meta = page_metadata[filename]
        content = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', content, count=1)
        content = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']>', f'<meta name="description" content="{meta["desc"]}">', content, count=1)
        # og:title & twitter:title
        content = re.sub(r'<meta\s+property=["\']og:title["\']\s+content=["\'].*?["\']>', f'<meta property="og:title" content="{meta["title"]} | macWave">', content, count=1)
        content = re.sub(r'<meta\s+name=["\']twitter:title["\']\s+content=["\'].*?["\']>', f'<meta name="twitter:title" content="{meta["title"]}">', content, count=1)
        # og:desc & twitter:desc
        content = re.sub(r'<meta\s+property=["\']og:description["\']\s+content=["\'].*?["\']>', f'<meta property="og:description" content="{meta["desc"]}">', content, count=1)
        content = re.sub(r'<meta\s+name=["\']twitter:description["\']\s+content=["\'].*?["\']>', f'<meta name="twitter:description" content="{meta["desc"]}">', content, count=1)

    # 2. Schema cleanup: remove aggregateRating and review with Cliente Satisfecho
    content = re.sub(r',\s*"aggregateRating":\s*\{\s*"@type":\s*"AggregateRating"[^}]*?\}\s*,\s*"review":\s*\{\s*"@type":\s*"Review"[^}]*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'"description":\s*"Reparación técnica de tarjetas lógicas, pantallas, teclados y baterías para MacBook Pro, Air e iMac con 2 años de garantía."', '"description": "Reparación de tarjeta lógica, cambio de batería y repotenciación para MacBook Pro, Air e iMac con 2 años de garantía."', content)

    # 3. Clean emojis in pain-badge
    content = re.sub(r'<div class="pain-badge">[\U00010000-\U0010ffff\u2600-\u27bf\s]+(.*?)</div>', r'<div class="pain-badge">\1</div>', content)
    # Clean emojis in hub-badge
    content = re.sub(r'<div class="hub-badge([^"]*)">[\U00010000-\U0010ffff\u2600-\u27bf\s]+(.*?)</div>', r'<div class="hub-badge\1">\2</div>', content)
    # Clean emojis in solution-badge
    content = re.sub(r'<div class="solution-badge">[\U00010000-\U0010ffff\u2600-\u27bf\s]+(.*?)</div>', r'<div class="solution-badge">\1</div>', content)

    # 4. Clean emojis in feature-icon
    for emoji, svg in emoji_to_svg.items():
        content = content.replace(f'<span class="feature-icon">{emoji}</span>', f'<span class="feature-icon">{svg}</span>')
        content = content.replace(f'<span class="trust-icon">{emoji}</span>', f'<span class="trust-icon">{svg}</span>')

    # Specific replacements
    content = content.replace('📍 Cobertura:', 'Cobertura:')
    content = content.replace('📍 Polanco', 'Cobertura: Polanco')
    content = content.replace('<div class="num" style="font-size:1.2rem;">⚠️</div>', '<div class="num" style="font-size:1.2rem;">!</div>')
    content = content.replace('<li>✅ <strong>', '<li><strong>')

    # 5. Fix WhatsApp links without text query param
    if filename in page_metadata:
        intent = page_metadata[filename]['wa_intent']
        content = content.replace('href="https://wa.me/525535757364"', f'href="https://wa.me/525535757364?text={intent}"')
        content = content.replace('Consulta Gratuita por WhatsApp →', 'Cotizar Solución con Garantía →')
        content = content.replace('Consulta Gratuita', 'Cotizar Solución')

    if content != orig:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Cleaned & optimized {filename}")
    else:
        print(f"[NOOP] No changes for {filename}")

if __name__ == '__main__':
    for fn in page_metadata.keys():
        clean_page(fn)
