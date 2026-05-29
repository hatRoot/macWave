const fs = require('fs');

let html = fs.readFileSync('/Users/joelduran/Documents/GitHub/MacWaveT2/index.html', 'utf8');

// The Breadcrumb schema fix
html = html.replace(/"item": "https:\/\/macwave\.com\.mx\/"/g, '"item": {\n          "@id": "https://macwave.com.mx/",\n          "name": "Inicio"\n        }');
html = html.replace(/"item": "https:\/\/macwave\.com\.mx\/#soluciones"/g, '"item": {\n          "@id": "https://macwave.com.mx/#soluciones",\n          "name": "Reparación MacBook"\n        }');

// FAQPage fix - let's add name just in case
html = html.replace(/("@type": "FAQPage",)/g, '$1\n        "name": "Preguntas Frecuentes",');

fs.writeFileSync('/Users/joelduran/Documents/GitHub/MacWaveT2/index.html', html);
console.log("Fixed!");
