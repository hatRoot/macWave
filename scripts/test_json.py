import json

s1 = """
    [
      {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "macWave Mexico",
        "alternateName": ["MacWave", "Mac Wave T2", "Reparación de Mac México"],
        "url": "https://macwave.com.mx/",
        "potentialAction": {
          "@type": "SearchAction",
          "target": "https://macwave.com.mx/?s={search_term_string}",
          "query-input": "required name=search_term_string"
        }
      },
      {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "¿Cuánto cuesta reparar una MacBook mojada en CDMX?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "El costo depende del daño a la tarjeta lógica. En Mac Wave T2 reparamos a nivel componente, lo cual es hasta un 60% más económico que cambiar toda la pieza en centros oficiales. Ofrecemos diagnóstico técnico profesional."
            }
          },
          {
            "@type": "Question",
            "name": "¿Tienen servicio de reparación de Mac a domicilio en Polanco o Santa Fe?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Sí, contamos con servicio de recolección y entrega a domicilio express en las zonas de Polanco, Santa Fe, Interlomas, Pedregal y Satélite."
            }
          },
          {
            "@type": "Question",
            "name": "¿Reparan equipos Apple fuera de garantía?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Especialistas en equipos Apple fuera de garantía. Si te dijeron que tu Mac ya es vintage o que no tiene arreglo, nosotros la rescatamos con garantía por escrito."
            }
          }
        ]
      },
      {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Mac Wave T2 - Reparación de Mac y MacBook CDMX",
        "image": "https://macwave.com.mx/images/apple.png",
        "description": "Centro de Reparación de Mac en CDMX. Expertos en MacBook Pro, MacBook Air e iMac. Diagnóstico Profesional, servicio a domicilio y reparación a nivel componente. Cobertura en Polanco, Santa Fe, Interlomas, Lomas, Pedregal, Satélite.",
        "@id": "https://macwave.com.mx/#localbusiness",
        "url": "https://macwave.com.mx/",
        "telephone": "+525535757364",
        "priceRange": "$$",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Agendar Cita vía WhatsApp",
          "addressLocality": "Ciudad de México",
          "addressRegion": "CDMX / Estado de México",
          "addressCountry": "MX"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": 19.432608,
          "longitude": -99.133209
        },
        "specialty": "Reparación de Tarjeta Lógica de MacBook y Recuperación de Datos",
        "knowsAbout": ["Reparación de MacBook Pro", "Servicio Técnico Apple", "Micro-soldadura", "macOS Sonoma", "Apple T2 Chip"],
        "areaServed": [
          "Polanco", "Interlomas", "Santa Fe", "Bosques de las Lomas", "Lomas de Chapultepec", "Tecamachalco", "Pedregal", "Satélite", "CDMX", "Estado de México"
        ],
        "openingHoursSpecification": [
          {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00",
            "closes": "19:00"
          },
          {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": "Saturday",
            "opens": "10:00",
            "closes": "15:00"
          }
        ],
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "5.0",
          "reviewCount": "50"
        },
        "sameAs": [
          "https://wa.me/525535757364"
        ],
        "hasOfferCatalog": {
          "@type": "OfferCatalog",
          "name": "Servicios de Reparación",
          "itemListElement": [
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "Reparación de Mac y MacBook",
                "description": "Servicio técnico especializado para toda la gama Mac: MacBook Pro, Air, iMac y Mac mini."
              }
            },
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "Reparación de Tarjeta Lógica Dañada o Mojada",
                "description": "Micro-soldadura y rescate de tarjetas lógicas con daño por líquidos, cortocircuitos o componentes quemados en MacBook Pro, Air e iMac."
              }
            },
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "Reparación de iMac",
                "description": "Servicio técnico completo para iMac: pantalla, tarjeta lógica, SSD, fuente de poder y mantenimiento preventivo."
              }
            },
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "Cambio de Pantalla MacBook",
                "description": "Sustitución de pantallas para MacBook Pro y MacBook Air."
              }
            }
          ]
        }
      }
    ]
"""

s2 = """
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
    "mainEntity": [{
    "@type": "Question",
    "name": "¿Cuánto cobran por revisar una Mac?",
    "acceptedAnswer": {
    "@type": "Answer",
    "text": "En Mac Wave T2 ofrecemos diagnóstico técnico para todos los modelos de MacBook Pro y MacBook Air. Nuestro objetivo es que conozcas el problema real y el costo total antes de comprometerte a cualquier gasto. ¡Transparencia total!"
    }
    },{
    "@type": "Question",
    "name": "¿Cuánto cuesta restaurar un Mac?",
    "acceptedAnswer": {
    "@type": "Answer",
    "text": "Restaurar una Mac (formateo, instalación de sistema macOS Sonoma/Sequoia y limpieza interna) tiene un costo base altamente competitivo. Esto incluye respaldo de archivos y optimización total para que tu equipo vuele como nuevo."
    }
    },{
    "@type": "Question",
    "name": "¿Puedes simplemente presentarte en una tienda Apple para repararlo?",
    "acceptedAnswer": {
    "@type": "Answer",
    "text": "Sí, pero en las tiendas oficiales suelen decir que equipos con más de 5 años son 'vintage' y no tienen piezas, o te cobran la tarjeta lógica completa. En Mac Wave T2 reparamos a nivel componente, rescatando tu equipo a una fracción del costo oficial."
    }
    },{
    "@type": "Question",
    "name": "¿Cuánto tardan en reparar un Mac?",
    "acceptedAnswer": {
    "@type": "Answer",
    "text": "La mayoría de los cambios (pantallas, baterías, SDD) se realizan el mismo día. Las reparaciones complejas de micro-soldadura suelen tardar de 24 a 48 horas tras la aprobación del presupuesto gratuito."
    }
    }]
    }
"""

try:
    json.loads(s1)
    print("S1 valid")
except Exception as e:
    print(f"S1 invalid: {e}")

try:
    json.loads(s2)
    print("S2 valid")
except Exception as e:
    print(f"S2 invalid: {e}")
