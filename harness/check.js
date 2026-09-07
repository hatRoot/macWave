#!/usr/bin/env node

/**
 * ==============================================================================
 * macWave Anti-Regression Harness & Guardrails
 * ==============================================================================
 * Audita automáticamente la integridad del sitio:
 * 1. Enlaces internos y recursos locales rotos (soporte para Apache Clean URLs).
 * 2. Sintaxis HTML, duplicados y etiquetas críticas.
 * 3. Parámetros canónicos de contacto (teléfono 5535757364 y WhatsApp 525535757364).
 * 4. Sincronización de sitemap.xml y robots.txt.
 * 5. Prevención de colisiones en UI móvil (barra fija vs botón flotante).
 * ==============================================================================
 */

const fs = require('node:fs');
const path = require('node:path');

const ROOT_DIR = path.resolve(__dirname, '..');

// Colores ANSI para terminal
const C = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
};

// Parámetros canónicos oficiales de macWave
const CANONICAL = {
  phoneRaw: '5535757364',
  waNumber: '525535757364',
};

const IGNORED_DIRS = new Set(['.git', 'node_modules', 'legacy', 'scratch', '.vscode', '.github']);

let totalErrors = 0;
let totalWarnings = 0;
let filesAudited = 0;

function logHeader(title) {
  console.log(`\n${C.bold}${C.cyan}=== ${title} ===${C.reset}`);
}

function logPass(msg) {
  console.log(`  ${C.green}✔${C.reset} ${msg}`);
}

function logWarn(msg) {
  totalWarnings++;
  console.log(`  ${C.yellow}⚠ WARN:${C.reset} ${msg}`);
}

function logError(msg) {
  totalErrors++;
  console.log(`  ${C.red}✖ ERROR:${C.reset} ${msg}`);
}

/**
 * Obtiene recursivamente los archivos HTML del repositorio excluyendo directorios ignorados.
 */
function getHtmlFiles(dir) {
  let results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    if (IGNORED_DIRS.has(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      results = results.concat(getHtmlFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

/**
 * Comprueba si un recurso local existe en disco (con soporte para Apache Clean URLs y partials).
 */
function checkLocalResourceExists(sourceFilePath, refPath) {
  // Ignorar templates dinámicos en JavaScript del cliente
  if (refPath.includes('${') || refPath.includes('{{')) {
    return true;
  }

  // Limpiar anchors y query params
  const cleanRef = refPath.split('#')[0].split('?')[0].trim();
  if (!cleanRef || cleanRef.startsWith('data:') || cleanRef.startsWith('blob:')) {
    return true;
  }

  let candidates = [];

  if (cleanRef.startsWith('/')) {
    const fromRoot = path.join(ROOT_DIR, cleanRef.replace(/^\/+/, ''));
    candidates.push(fromRoot);
    candidates.push(fromRoot + '.html');
    candidates.push(path.join(fromRoot, 'index.html'));
  } else {
    // Relativo al archivo actual
    const fromCurrent = path.resolve(path.dirname(sourceFilePath), cleanRef);
    candidates.push(fromCurrent);
    candidates.push(fromCurrent + '.html');
    candidates.push(path.join(fromCurrent, 'index.html'));

    // Si el archivo fuente está en partials/, evaluar también relativo a la raíz del sitio
    if (sourceFilePath.includes(path.sep + 'partials' + path.sep)) {
      const fromRootRelative = path.resolve(ROOT_DIR, cleanRef);
      candidates.push(fromRootRelative);
      candidates.push(fromRootRelative + '.html');
      candidates.push(path.join(fromRootRelative, 'index.html'));
    }
  }

  return candidates.some((candidate) => fs.existsSync(candidate));
}

/**
 * 1. Auditoría de Enlaces Locales, Imágenes y Assets
 */
function auditLinksAndAssets(htmlFiles) {
  logHeader('1. AUDITORÍA DE ENLACES INTERNOS Y ASSETS LOCALES');
  let issuesFound = 0;

  for (const filePath of htmlFiles) {
    const relFile = path.relative(ROOT_DIR, filePath);
    const content = fs.readFileSync(filePath, 'utf8');

    // Revisar <a> enlaces locales
    const hrefRegex = /<a\s+[^>]*?href=["']([^"']+)["']/gi;
    let match;
    while ((match = hrefRegex.exec(content)) !== null) {
      const href = match[1].trim();
      if (
        href.startsWith('http://') ||
        href.startsWith('https://') ||
        href.startsWith('tel:') ||
        href.startsWith('mailto:') ||
        href.startsWith('#') ||
        href.startsWith('javascript:')
      ) {
        continue;
      }
      if (!checkLocalResourceExists(filePath, href)) {
        logError(`[${relFile}] Enlace roto hacia archivo inexistente: "${href}"`);
        issuesFound++;
      }
    }

    // Revisar imágenes locales
    const imgRegex = /<img\s+[^>]*?src=["']([^"']+)["']/gi;
    while ((match = imgRegex.exec(content)) !== null) {
      const src = match[1].trim();
      if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:')) {
        continue;
      }
      if (!checkLocalResourceExists(filePath, src)) {
        logError(`[${relFile}] Imagen local no encontrada: "${src}"`);
        issuesFound++;
      }
    }

    // Revisar scripts locales
    const scriptRegex = /<script\s+[^>]*?src=["']([^"']+)["']/gi;
    while ((match = scriptRegex.exec(content)) !== null) {
      const src = match[1].trim();
      if (src.startsWith('http://') || src.startsWith('https://')) continue;
      if (!checkLocalResourceExists(filePath, src)) {
        logError(`[${relFile}] Script local no encontrado: "${src}"`);
        issuesFound++;
      }
    }

    // Revisar hojas de estilo locales
    const cssRegex = /<link\s+[^>]*?rel=["']stylesheet["'][^>]*?href=["']([^"']+)["']/gi;
    while ((match = cssRegex.exec(content)) !== null) {
      const href = match[1].trim();
      if (href.startsWith('http://') || href.startsWith('https://')) continue;
      if (!checkLocalResourceExists(filePath, href)) {
        logError(`[${relFile}] CSS local no encontrado: "${href}"`);
        issuesFound++;
      }
    }
  }

  if (issuesFound === 0) {
    logPass('Todos los enlaces internos, imágenes y hojas de estilo locales existen.');
  }
}

/**
 * 2. Auditoría de Sintaxis HTML, Duplicados e Higiene
 */
function auditHtmlSyntax(htmlFiles) {
  logHeader('2. AUDITORÍA DE HIGIENE HTML Y DUPLICADOS');
  let issuesFound = 0;

  for (const filePath of htmlFiles) {
    const relFile = path.relative(ROOT_DIR, filePath);
    const content = fs.readFileSync(filePath, 'utf8');

    // Doble style="" en un mismo elemento
    if (/<[^>]*\bstyle=["'][^"']*["'][^>]*\bstyle=["']/i.test(content)) {
      logError(`[${relFile}] Elemento HTML con atributo 'style' duplicado.`);
      issuesFound++;
    }

    // Comprobar múltiples <title>
    const titleMatches = content.match(/<title[^>]*>[\s\S]*?<\/title>/gi);
    if (titleMatches && titleMatches.length > 1) {
      logError(`[${relFile}] Múltiples etiquetas <title> detectadas (${titleMatches.length}).`);
      issuesFound++;
    }

    // Comprobar scripts o styles no cerrados
    const openStyles = (content.match(/<style\b[^>]*>/gi) || []).length;
    const closeStyles = (content.match(/<\/style>/gi) || []).length;
    if (openStyles !== closeStyles) {
      logError(`[${relFile}] Desbalance en etiquetas <style>: ${openStyles} aperturas vs ${closeStyles} cierres.`);
      issuesFound++;
    }

    const openScripts = (content.match(/<script\b[^>]*>/gi) || []).length;
    const closeScripts = (content.match(/<\/script>/gi) || []).length;
    if (openScripts !== closeScripts) {
      logError(`[${relFile}] Desbalance en etiquetas <script>: ${openScripts} aperturas vs ${closeScripts} cierres.`);
      issuesFound++;
    }

    // Comprobar IDs duplicados
    const idRegex = /\bid=["']([^"']+)["']/gi;
    let match;
    const ids = new Set();
    while ((match = idRegex.exec(content)) !== null) {
      const id = match[1];
      if (ids.has(id)) {
        logWarn(`[${relFile}] ID duplicado en el mismo documento: "#${id}"`);
      } else {
        ids.add(id);
      }
    }
  }

  if (issuesFound === 0) {
    logPass('Estructura HTML limpia: sin atributos style duplicados ni bloques sin cerrar.');
  }
}

/**
 * 3. Auditoría de Contacto y CRO (Teléfonos y WhatsApp Canónicos)
 */
function auditContactChannels(htmlFiles) {
  logHeader('3. AUDITORÍA DE CANALES DE CONTACTO (CRO & CANÓNICOS)');
  let issuesFound = 0;

  for (const filePath of htmlFiles) {
    const relFile = path.relative(ROOT_DIR, filePath);
    const content = fs.readFileSync(filePath, 'utf8');

    // Revisar enlaces tel:
    const telRegex = /href=["']tel:([^"']+)["']/gi;
    let match;
    while ((match = telRegex.exec(content)) !== null) {
      const rawTel = match[1].replace(/[\s\-\(\)\+]/g, '');
      if (rawTel.includes('${')) continue; // template variable
      if (rawTel !== CANONICAL.phoneRaw && rawTel !== `52${CANONICAL.phoneRaw}`) {
        logError(`[${relFile}] Teléfono no canónico o con tipografía errónea: "tel:${match[1]}". Esperado: "tel:${CANONICAL.phoneRaw}"`);
        issuesFound++;
      }
    }

    // Revisar enlaces wa.me
    const waRegex = /href=["'](?:https?:\/\/)?wa\.me\/([^"'\?\/]+)(?:\?([^"']*))?["']/gi;
    while ((match = waRegex.exec(content)) !== null) {
      const waTarget = match[1];
      if (waTarget.includes('${')) continue; // template variable
      const waNum = waTarget.replace(/[\s\-\(\)\+]/g, '');
      if (waNum !== CANONICAL.waNumber && waNum !== CANONICAL.phoneRaw) {
        logError(`[${relFile}] Número de WhatsApp no canónico: "wa.me/${match[1]}". Esperado: "wa.me/${CANONICAL.waNumber}"`);
        issuesFound++;
      }
    }
  }

  if (issuesFound === 0) {
    logPass(`Todos los enlaces tel: y wa.me apuntan a los números oficiales de macWave (${CANONICAL.phoneRaw} / ${CANONICAL.waNumber}).`);
  }
}

/**
 * 4. Auditoría de Colisiones UI Móviles
 */
function auditMobileUiCollisions(htmlFiles) {
  logHeader('4. AUDITORÍA DE UI / UX MÓVIL (PREVENCIÓN DE COLISIONES)');
  let warningsFound = 0;

  for (const filePath of htmlFiles) {
    const relFile = path.relative(ROOT_DIR, filePath);
    const content = fs.readFileSync(filePath, 'utf8');

    const hasStickyBar = /class=["'][^"']*(?:sticky-mobile-cta|mobile-call-bar|mobileCallBar)[^"']*["']/i.test(content) ||
                         /id=["'](?:mobileCallBar|sticky-mobile-cta)["']/i.test(content);
    const hasFloatingWa = /class=["'][^"']*(?:floating-wa-btn|floatingWA|floating-btn)[^"']*["']/i.test(content) ||
                          /id=["']floatingWA["']/i.test(content);

    if (hasStickyBar && hasFloatingWa) {
      const hidesFloatingOnMobile = /\.floating-wa-btn\s*\{[^}]*display:\s*none/i.test(content) ||
                                    /display:\s*none\s*!important/i.test(content);
      if (!hidesFloatingOnMobile) {
        logWarn(`[${relFile}] Contiene barra fija inferior y botón flotante sin regla CSS de ocultamiento móvil.`);
        warningsFound++;
      }
    }
  }

  if (warningsFound === 0) {
    logPass('No se detectaron colisiones evidentes entre barras fijas y botones flotantes.');
  }
}

/**
 * 5. Auditoría de Sitemap y Robots
 */
function auditSitemapAndRobots() {
  logHeader('5. AUDITORÍA DE SITEMAP.XML Y ROBOTS.TXT');
  let issuesFound = 0;

  const sitemapPath = path.join(ROOT_DIR, 'sitemap.xml');
  if (!fs.existsSync(sitemapPath)) {
    logError('El archivo sitemap.xml no existe en la raíz.');
    issuesFound++;
  } else {
    const sitemapContent = fs.readFileSync(sitemapPath, 'utf8');
    const locRegex = /<loc>\s*https?:\/\/[^\/]+\/([^<]+)\s*<\/loc>/gi;
    let match;
    let urlsChecked = 0;

    while ((match = locRegex.exec(sitemapContent)) !== null) {
      const pagePath = match[1].trim();
      urlsChecked++;
      if (pagePath && !pagePath.endsWith('/')) {
        const directFile = path.join(ROOT_DIR, pagePath);
        const htmlFile = path.join(ROOT_DIR, pagePath + '.html');
        if (!fs.existsSync(directFile) && !fs.existsSync(htmlFile)) {
          logError(`[sitemap.xml] La URL referenciada no existe localmente: "${pagePath}"`);
          issuesFound++;
        }
      }
    }
    logPass(`Sitemap validado: ${urlsChecked} URLs analizadas y corroboradas contra archivos locales.`);
  }

  const robotsPath = path.join(ROOT_DIR, 'robots.txt');
  if (!fs.existsSync(robotsPath)) {
    logWarn('El archivo robots.txt no existe en la raíz.');
  } else {
    const robotsContent = fs.readFileSync(robotsPath, 'utf8');
    if (!robotsContent.includes('Sitemap:')) {
      logWarn('[robots.txt] No incluye la directiva "Sitemap:". Se recomienda añadirla para SEO técnico.');
    } else {
      logPass('robots.txt presente y con referencia a Sitemap.');
    }
  }
}

/**
 * Función principal de ejecución
 */
function runHarness() {
  const startTime = Date.now();
  console.log(`${C.bold}${C.cyan}╔═══════════════════════════════════════════════════════════════╗${C.reset}`);
  console.log(`${C.bold}${C.cyan}║    macWave — Arnés Anti-Regresiones & Control de Calidad      ║${C.reset}`);
  console.log(`${C.bold}${C.cyan}╚═══════════════════════════════════════════════════════════════╝${C.reset}`);

  const htmlFiles = getHtmlFiles(ROOT_DIR);
  filesAudited = htmlFiles.length;
  console.log(`${C.gray}Total de páginas HTML a inspeccionar: ${filesAudited}${C.reset}`);

  auditLinksAndAssets(htmlFiles);
  auditHtmlSyntax(htmlFiles);
  auditContactChannels(htmlFiles);
  auditMobileUiCollisions(htmlFiles);
  auditSitemapAndRobots();

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
  logHeader('RESUMEN DE AUDITORÍA');
  console.log(`  Páginas auditadas : ${filesAudited}`);
  console.log(`  Errores críticos  : ${totalErrors > 0 ? C.red + totalErrors : C.green + 0}${C.reset}`);
  console.log(`  Advertencias      : ${totalWarnings > 0 ? C.yellow + totalWarnings : C.green + 0}${C.reset}`);
  console.log(`  Tiempo ejecución  : ${elapsed}s`);

  if (totalErrors > 0) {
    console.log(`\n${C.bold}${C.red}❌ FALLO DE COMPUERTA: Se encontraron ${totalErrors} errores críticos. Resuélvelos antes de entregar.${C.reset}\n`);
    process.exit(1);
  } else {
    console.log(`\n${C.bold}${C.green}✅ COMPUERTA APROBADA: El sitio cumple con todos los guardrails de calidad.${C.reset}\n`);
    process.exit(0);
  }
}

runHarness();
