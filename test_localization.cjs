// Check shared localization behavior without launching a browser.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

class Element {
  constructor() { this.dataset = {}; this.attributes = {}; this.events = {}; this.nodes = {}; this.textContent = ''; }
  addEventListener(name, callback) { this.events[name] = callback; }
  setAttribute(key, value) { this.attributes[key] = value; }
  querySelector(selector) { return this.nodes[selector]; }
  replaceWith(node) { this.replacement = node; }
  replaceChildren(node) { this.child = node; }
}

function fixture(language, configured = true, englishPolicy = true) {
  const selectors = {};
  for (const id of ['.menu-toggle', '#navigation', '#lightbox', '#close-lightbox', '#theme-preview', '#deletion-form', '#request-status', '#send-request', '#request-type', '#account-email', '#request-note']) {
    selectors[id] = new Element();
  }
  const preview = selectors['#theme-preview'];
  for (const selector of ['img', '[data-full]', 'figcaption']) preview.nodes[selector] = new Element();
  const policy = new Element();
  const field = new Element(); field.dataset.config = 'retentionPolicy'; field.textContent = 'Draft placeholder';
  const store = new Element(); store.className = 'button primary';
  const link = new Element(); link.href = 'file:///site/guide.html';
  const groups = {'.language-switch a': [link], '[data-config]': [field], '[data-policy-notice]': [policy], '[data-store]': [store]};
  const document = {
    documentElement: {lang: language},
    querySelector: selector => selectors[selector] || null,
    querySelectorAll: selector => groups[selector] || [],
    addEventListener() {},
    createElement: () => new Element(),
  };
  const config = configured ? {
    developerName: 'Test operator', supportEmail: 'support@example.com', policyEffectiveDate: '2026-10-28',
    policiesApproved: true, deletionTimeframe: 'Base timeframe', retentionPolicy: 'Base retention', processingRegion: 'Base region',
    playStoreUrl: 'https://play.google.com/store/apps/details?id=com.fourfold.journal',
    localized: {en: englishPolicy ? {deletionTimeframe: 'English timeframe', retentionPolicy: 'English retention', processingRegion: 'English region'} : {}},
  } : {};
  const context = vm.createContext({window: {SITE_CONFIG: config}, document, URL, URLSearchParams, location: {search: '?group=book', hash: '#gallery', href: ''}});
  vm.runInContext(fs.readFileSync('assets-data.js', 'utf8'), context);
  vm.runInContext(fs.readFileSync('app.js', 'utf8'), context);
  return {context, selectors, preview, policy, field, store, link};
}

for (const language of ['ko', 'en']) {
  const f = fixture(language);
  assert.match(f.link.href, /guide\.html\?group=book#gallery$/);
  assert.equal(f.policy.hidden, true);
  assert.equal(f.field.textContent, language === 'en' ? 'English retention' : 'Base retention');
  if (language === 'en') assert.equal(f.store.replacement.textContent, 'Get it on Google Play');
  vm.runInContext("changeImage('#theme-preview', 'diary-album')", f.context);
  const asset = f.context.window.GALLERY_ASSETS.find(a => a.id === 'diary-album');
  assert.equal(f.preview.nodes.img.alt, asset['alt_' + language]);
  assert.equal(f.preview.nodes.figcaption.textContent, asset['title_' + language]);
  if (language === 'en') assert.equal(f.preview.nodes['[data-full]'].attributes['aria-label'], 'Enlarge: ' + asset.alt_en);
}

const draft = fixture('en', true, false);
assert.equal(draft.field.textContent, 'Draft placeholder');
assert.notEqual(draft.policy.hidden, true);
const unconfigured = fixture('en', false);
assert.notEqual(unconfigured.selectors['#send-request'].disabled, false);

const email = fixture('en');
email.selectors['#request-type'].value = 'Delete my Plus account and all linked data';
email.selectors['#account-email'].value = 'user@example.com';
email.selectors['#request-note'].value = 'Please delete my account.';
email.selectors['#deletion-form'].reportValidity = () => true;
email.selectors['#deletion-form'].events.submit({preventDefault() {}});
const mailto = new URL(email.context.location.href);
assert.equal(mailto.protocol, 'mailto:');
assert.equal(mailto.pathname, 'support@example.com');
assert.match(mailto.searchParams.get('subject'), /^\[Day in Four\]/);
assert.match(mailto.searchParams.get('body'), /Account email: user@example.com/);
assert.doesNotMatch(mailto.searchParams.get('body'), /[\uac00-\ud7a3]/);
assert.match(email.selectors['#request-status'].textContent, /does not submit/);
console.log('Passed: bilingual image updates, language links, store label, policy configuration, and English email draft.');
