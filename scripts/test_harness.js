#!/usr/bin/env node

/**
 * =========================================================================
 * MacWave — Production Pre-flight Test Harness (Arnés de Pruebas)
 * =========================================================================
 * Tests:
 * 1. JavaScript Syntax Validation (.js files and inline <script> in HTML)
 * 2. Structured Data / JSON-LD Validation
 * 3. Local Asset Reference Check (CSS, JS, Images)
 * 4. Critical ODS & Dashboard Functions Integrity Check
 * 5. General HTML Tag / Structure Integrity Check
 * =========================================================================
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT_DIR = path.resolve(__dirname, '..');
const EXCLUDE_DIRS = new Set(['.git', '.vscode', 'node_modules', 'legacy', 'scratch', 'clientes']);

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;
const failures = [];

function pass(name, detail = '') {
  totalTests++;
  passedTests++;
  console.log(`  \x1b[32m✔\x1b[0m ${name} ${detail ? `\x1b[90m(${detail})\x1b[0m` : ''}`);
}

function fail(name, error) {
  totalTests++;
  failedTests++;
  failures.push({ name, error });
  console.log(`  \x1b[31m✖\x1b[0m ${name}`);
  console.log(`    \x1b[31mError: ${error}\x1b[0m`);
}

function getFiles(dir, extensions) {
  let results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (EXCLUDE_DIRS.has(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(getFiles(fullPath, extensions));
    } else if (extensions.some(ext => entry.name.endsWith(ext))) {
      results.push(fullPath);
    }
  }
  return results;
}

// -----------------------------------------------------------------------------
// Test Suite 1: JavaScript File Syntax
// -----------------------------------------------------------------------------
function testJsFiles() {
  console.log('\n\x1b[36m[1/5] Validating JavaScript Files (.js)...\x1b[0m');
  const jsFiles = getFiles(ROOT_DIR, ['.js']);
  
  for (const filePath of jsFiles) {
    const relPath = path.relative(ROOT_DIR, filePath);
    try {
      const code = fs.readFileSync(filePath, 'utf8');
      new vm.Script(code, { filename: relPath });
      pass(`JS Syntax: ${relPath}`);
    } catch (err) {
      fail(`JS Syntax: ${relPath}`, err.message);
    }
  }
}

// -----------------------------------------------------------------------------
// Test Suite 2: HTML Inline Scripts and JSON-LD
// -----------------------------------------------------------------------------
function testHtmlScripts() {
  console.log('\n\x1b[36m[2/5] Validating Inline <script> & JSON-LD in HTML...\x1b[0m');
  const htmlFiles = getFiles(ROOT_DIR, ['.html']);

  for (const filePath of htmlFiles) {
    const relPath = path.relative(ROOT_DIR, filePath);
    const content = fs.readFileSync(filePath, 'utf8');

    // Extract script tags
    const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
    let match;
    let scriptIndex = 0;

    while ((match = scriptRegex.exec(content)) !== null) {
      scriptIndex++;
      const attrs = match[1] || '';
      const scriptCode = match[2];

      if (!scriptCode || !scriptCode.trim()) continue;

      if (attrs.includes('application/ld+json')) {
        // Test JSON-LD
        try {
          JSON.parse(scriptCode);
          pass(`JSON-LD #${scriptIndex} in ${relPath}`);
        } catch (err) {
          fail(`JSON-LD #${scriptIndex} in ${relPath}`, `Invalid JSON: ${err.message}`);
        }
      } else if (!attrs.includes('type="text/template"') && !attrs.includes('type="text/html"')) {
        // Test Standard JS syntax
        try {
          new vm.Script(scriptCode, { filename: `${relPath}#script-${scriptIndex}` });
          pass(`Inline JS #${scriptIndex} in ${relPath}`);
        } catch (err) {
          // Identify approximate line number in HTML file
          const preScriptLines = content.substring(0, match.index).split('\n').length;
          fail(`Inline JS #${scriptIndex} in ${relPath} (around line ${preScriptLines})`, err.message);
        }
      }
    }
  }
}

// -----------------------------------------------------------------------------
// Test Suite 3: Local Asset References (CSS, JS, Images)
// -----------------------------------------------------------------------------
function testAssetReferences() {
  console.log('\n\x1b[36m[3/5] Validating Local Asset References in Key Pages...\x1b[0m');
  const htmlFiles = getFiles(ROOT_DIR, ['.html']);

  for (const filePath of htmlFiles) {
    const relPath = path.relative(ROOT_DIR, filePath);
    const fileDir = path.dirname(filePath);
    const content = fs.readFileSync(filePath, 'utf8');

    // Check <link rel="stylesheet" href="...">
    const linkRegex = /<link\b[^>]*href=["']([^"']+)["'][^>]*>/gi;
    let match;
    while ((match = linkRegex.exec(content)) !== null) {
      const href = match[1].split('?')[0].split('#')[0];
      if (href.startsWith('http://') || href.startsWith('https://') || href.startsWith('//') || href.startsWith('data:')) continue;
      
      const targetPath = href.startsWith('/') ? path.join(ROOT_DIR, href.slice(1)) : path.resolve(fileDir, href);
      if (!fs.existsSync(targetPath)) {
        fail(`Broken CSS Link in ${relPath}`, `File not found: ${href}`);
      } else {
        pass(`CSS Link in ${relPath}: ${href}`);
      }
    }

    // Check <script src="...">
    const scriptSrcRegex = /<script\b[^>]*src=["']([^"']+)["'][^>]*>/gi;
    while ((match = scriptSrcRegex.exec(content)) !== null) {
      const src = match[1].split('?')[0].split('#')[0];
      if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('//') || src.startsWith('data:')) continue;

      const targetPath = src.startsWith('/') ? path.join(ROOT_DIR, src.slice(1)) : path.resolve(fileDir, src);
      if (!fs.existsSync(targetPath)) {
        fail(`Broken Script Reference in ${relPath}`, `File not found: ${src}`);
      } else {
        pass(`Script Reference in ${relPath}: ${src}`);
      }
    }
  }
}

// -----------------------------------------------------------------------------
// Test Suite 4: Critical ODS & Dashboard Functionality Checks
// -----------------------------------------------------------------------------
function testCriticalFunctions() {
  console.log('\n\x1b[36m[4/5] Checking Critical ODS & Dashboard Logic Integrity...\x1b[0m');
  
  const dashboardPath = path.join(ROOT_DIR, 'dashboard-ods.html');
  if (fs.existsSync(dashboardPath)) {
    const code = fs.readFileSync(dashboardPath, 'utf8');

    const requiredSymbols = [
      'renderDetail',
      'timelineHtml',
      'statusOptions',
      'STATUS_CONFIG',
      'uploadGalleryPhotos',
      'deleteGalleryPhoto',
      'PhotoFlowV3'
    ];

    for (const sym of requiredSymbols) {
      if (code.includes(sym)) {
        pass(`Dashboard Symbol Check: ${sym} present in dashboard-ods.html`);
      } else {
        fail(`Dashboard Symbol Check: ${sym}`, `Missing required symbol '${sym}' in dashboard-ods.html`);
      }
    }

    // Check that timelineHtml doesn't have unbalanced template string/closing brackets
    if (code.includes('const timelineHtml =') && code.includes('${timelineHtml}')) {
      pass(`Dashboard Timeline: timelineHtml definition and binding intact`);
    } else {
      fail(`Dashboard Timeline`, `timelineHtml definition or injection missing`);
    }
  } else {
    fail('Dashboard Check', 'dashboard-ods.html not found');
  }

  // Check ods.html
  const odsPath = path.join(ROOT_DIR, 'ods.html');
  if (fs.existsSync(odsPath)) {
    const odsCode = fs.readFileSync(odsPath, 'utf8');
    if (odsCode.includes('supabase') || odsCode.includes('createClient')) {
      pass(`ODS Supabase integration present in ods.html`);
    } else {
      fail(`ODS Supabase integration`, `Missing supabase integration in ods.html`);
    }
  }
}

// -----------------------------------------------------------------------------
// Test Suite 5: HTML Structural Validation
// -----------------------------------------------------------------------------
function testHtmlStructure() {
  console.log('\n\x1b[36m[5/5] Checking HTML Structure & Basic Tags...\x1b[0m');
  const mainPages = ['index.html', 'dashboard-ods.html', 'ods.html', 'status-ods.html', 'tecnicos.html', 'reparaciones.html'];

  for (const page of mainPages) {
    const pPath = path.join(ROOT_DIR, page);
    if (!fs.existsSync(pPath)) continue;
    const content = fs.readFileSync(pPath, 'utf8');

    const hasDoctype = /<!DOCTYPE\s+html>/i.test(content);
    const hasHtmlOpen = /<html\b/i.test(content);
    const hasHtmlClose = /<\/html>/i.test(content);
    const hasBodyClose = /<\/body>/i.test(content);

    if (hasDoctype && hasHtmlOpen && hasHtmlClose && hasBodyClose) {
      pass(`HTML Structure: ${page}`);
    } else {
      fail(`HTML Structure: ${page}`, `Missing standard DOCTYPE or closing tags (html/body)`);
    }
  }
}

// -----------------------------------------------------------------------------
// Main Runner
// -----------------------------------------------------------------------------
function run() {
  console.log('\x1b[1m\x1b[34m================================================================');
  console.log('   macWave Pre-Production Test Harness — Verification Suite');
  console.log('================================================================\x1b[0m');

  const start = Date.now();

  testJsFiles();
  testHtmlScripts();
  testAssetReferences();
  testCriticalFunctions();
  testHtmlStructure();

  const elapsed = ((Date.now() - start) / 1000).toFixed(2);

  console.log('\n\x1b[1m================================================================\x1b[0m');
  console.log(`\x1b[1mSummary: ${totalTests} Tests Executed in ${elapsed}s\x1b[0m`);
  console.log(`  \x1b[32mPassed: ${passedTests}\x1b[0m`);
  console.log(`  \x1b[31mFailed: ${failedTests}\x1b[0m`);
  console.log('\x1b[1m================================================================\x1b[0m');

  if (failedTests > 0) {
    console.log('\n\x1b[31mDetailed Failures:\x1b[0m');
    failures.forEach((f, i) => {
      console.log(`  ${i + 1}. \x1b[1m${f.name}\x1b[0m: ${f.error}`);
    });
    process.exit(1);
  } else {
    console.log('\n\x1b[32m🎉 ALL TESTS PASSED! No syntax or critical errors detected. Ready for production.\x1b[0m\n');
    process.exit(0);
  }
}

run();
