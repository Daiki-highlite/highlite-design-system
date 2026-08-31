#!/usr/bin/env node
/**
 * PoC Website Generator
 * Usage: node website-system/generate-poc.js <client-slug>
 * Example: node website-system/generate-poc.js nextstride
 *
 * Template is selected via profile._meta.template:
 *   "corporate" (default) → poc-template.html  — B2B・コンサル・専門サービス
 *   "warmth"              → poc-warmth.html    — カフェ・飲食・ライフスタイル
 *   "launch"              → poc-launch.html    — スタートアップ・SaaS・プロダクト
 *
 * Reads  clients/<slug>/profile.json
 * Writes clients/<slug>/poc/index.html
 */

const fs = require('fs');
const path = require('path');

const slug = process.argv[2];
if (!slug) {
  console.error('Usage: node generate-poc.js <client-slug>');
  console.error('Example: node generate-poc.js nextstride');
  process.exit(1);
}

const root = path.join(__dirname, '..');
const profilePath = path.join(root, 'clients', slug, 'profile.json');
const outputDir  = path.join(root, 'clients', slug, 'poc');
const outputPath = path.join(outputDir, 'index.html');

if (!fs.existsSync(profilePath)) {
  console.error(`Profile not found: ${profilePath}`);
  console.error(`Copy clients/_template/profile.json → clients/${slug}/profile.json and fill it in.`);
  process.exit(1);
}

const profile = JSON.parse(fs.readFileSync(profilePath, 'utf8'));

// --- Template selection ---
const TEMPLATES = {
  corporate: 'poc-template.html',
  warmth:    'poc-warmth.html',
  launch:    'poc-launch.html',
};
const templateName = profile._meta?.template || 'corporate';
const templateFile = TEMPLATES[templateName] || TEMPLATES.corporate;
const templatePath = path.join(__dirname, 'templates', templateFile);

if (!fs.existsSync(templatePath)) {
  console.error(`Template not found: ${templatePath}`);
  process.exit(1);
}

let html = fs.readFileSync(templatePath, 'utf8');

// --- Token resolver ---
function getVal(obj, dotPath) {
  const val = dotPath.split('.').reduce((o, k) => (o && o[k] !== undefined ? o[k] : null), obj);
  return val !== null && val !== undefined ? String(val) : '';
}

// --- HTML builders (template-specific) ---

function buildNavLinksHtml(links) {
  return (links || [])
    .map(l => `<a href="${l.href}" class="nav-link">${l.label}</a>`)
    .join('\n      ');
}

function buildStatsHtml(stats) {
  return (stats || [])
    .filter(s => s.value)
    .map(s => `
      <div class="stat-item">
        <div class="stat-value">${s.value}</div>
        <div class="stat-label">${s.label}</div>
      </div>`)
    .join('');
}

function buildServicesHtml(items, template) {
  const list = (items || []).filter(s => s.title);

  if (template === 'warmth') {
    // Alternating feature rows with circular icon
    return list.map(s => `
      <div class="feature-row">
        <div class="feature-visual"><span class="feature-icon">${s.icon || '◆'}</span></div>
        <div class="feature-text">
          <h3 class="feature-title">${s.title}</h3>
          <p class="feature-desc">${s.description}</p>
        </div>
      </div>`).join('');
  }

  if (template === 'launch') {
    // Numbered list with CSS counter
    return list.map(s => `
      <div class="service-item">
        <div class="service-number"></div>
        <div class="service-content">
          <span class="service-icon-sm">${s.icon || '◆'}</span>
          <h3 class="service-title">${s.title}</h3>
          <p class="service-desc">${s.description}</p>
        </div>
      </div>`).join('');
  }

  // corporate (default) — card grid
  return list.map(s => `
      <div class="service-card">
        <span class="service-icon">${s.icon || '◆'}</span>
        <h3 class="service-title">${s.title}</h3>
        <p class="service-desc">${s.description}</p>
      </div>`).join('');
}

function buildFooterLinksHtml(links) {
  return (links || [])
    .map(l => `<a href="${l.href}" class="footer-link">${l.label}</a>`)
    .join('');
}

// --- Step 1: Inject block HTML before token replacement ---
html = html
  .replace('{{NAV_LINKS_HTML}}',    buildNavLinksHtml(profile.content?.nav?.links))
  .replace('{{STATS_HTML}}',        buildStatsHtml(profile.content?.about?.stats))
  .replace('{{SERVICES_HTML}}',     buildServicesHtml(profile.content?.services?.items, templateName))
  .replace('{{FOOTER_LINKS_HTML}}', buildFooterLinksHtml(profile.content?.footer?.links));

// --- Step 2: Replace {{path.to.value}} tokens ---
html = html.replace(/\{\{([^}]+)\}\}/g, (match, token) => getVal(profile, token.trim()));

// --- Write output ---
fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(outputPath, html, 'utf8');

const absPath = path.resolve(outputPath).replace(/\\/g, '/');
console.log(`\n✓ PoC generated  [${templateName}]  clients/${slug}/poc/index.html`);
console.log(`  Browser: file://${absPath}\n`);
