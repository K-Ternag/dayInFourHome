'use strict';
const config = window.SITE_CONFIG || {};
const assets = window.GALLERY_ASSETS || [];
const language = document.documentElement.lang === 'en' ? 'en' : 'ko';
const isEnglish = language === 'en';
const copy = (ko, en) => isEnglish ? en : ko;
const assetText = (asset, key) => asset[key + '_' + language];
const localizedConfig = config.localized?.[language] || {};
const translatedFields = ['deletionTimeframe', 'retentionPolicy', 'processingRegion'];
const configuredValue = key => isEnglish && translatedFields.includes(key)
  ? localizedConfig[key] : (localizedConfig[key] || config[key]);
document.querySelectorAll('.language-switch a').forEach(link => {
  const destination = new URL(link.href);
  destination.search = location.search;
  destination.hash = location.hash;
  link.href = destination.href;
});
const emailReady = typeof config.supportEmail === 'string' && /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(config.supportEmail);
document.querySelectorAll('[data-config]').forEach(el => {
  const value = configuredValue(el.dataset.config);
  if (typeof value === 'string' && value.trim()) el.textContent = value;
});
document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
document.querySelectorAll('[data-developer]').forEach(el => { if (config.developerName) el.textContent = config.developerName; });
document.querySelectorAll('[data-contact]').forEach(el => {
  if (!emailReady) return;
  const link = document.createElement('a');
  link.href = 'mailto:' + config.supportEmail;
  link.textContent = config.supportEmail;
  el.replaceChildren(link);
});
const policyReady = config.policiesApproved && emailReady && ['developerName','policyEffectiveDate','deletionTimeframe','retentionPolicy','processingRegion'].every(key => typeof configuredValue(key) === 'string' && configuredValue(key).trim());
if (policyReady) document.querySelectorAll('[data-policy-notice]').forEach(el => el.hidden = true);
document.querySelectorAll('[data-store]').forEach(el => {
  try {
    const url = new URL(config.playStoreUrl);
    if (url.protocol !== 'https:' || url.hostname !== 'play.google.com') return;
    const link = document.createElement('a');
    link.href = url.href; link.className = el.className;
    link.textContent = copy('Google Play에서 만나기', 'Get it on Google Play'); el.replaceWith(link);
  } catch { /* No published store URL yet. */ }
});
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open);
});
nav.addEventListener('click', event => { if(event.target.closest('a')) { menu.setAttribute('aria-expanded','false'); nav.classList.remove('open'); } });
document.addEventListener('keydown', event => { if (event.key === 'Escape') { menu.setAttribute('aria-expanded','false'); nav.classList.remove('open'); } });
const dialog = document.querySelector('#lightbox');
let trigger;
document.addEventListener('click', event => {
  const button = event.target.closest('[data-full]');
  if (!button) return;
  trigger = button;
  const source = button.querySelector('img');
  dialog.querySelector('img').src = button.dataset.full;
  dialog.querySelector('img').alt = source.alt;
  document.querySelector('#lightbox-title').textContent = source.alt;
  dialog.showModal();
});
document.querySelector('#close-lightbox').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const rect = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
});
dialog.addEventListener('close', () => trigger?.focus());
function changeImage(container, id) {
  const asset = assets.find(item => item.id === id);
  const root = document.querySelector(container);
  if (!asset || !root) return;
  const img = root.querySelector('img');
  img.src = asset.preview; img.alt = assetText(asset, 'alt');
  img.width = asset.width; img.height = asset.height;
  const button = root.querySelector('[data-full]');
  button.dataset.full = asset.path; button.setAttribute('aria-label', copy(asset.alt_ko + ' 확대', 'Enlarge: ' + asset.alt_en));
  root.querySelector('figcaption').textContent = assetText(asset, 'title');
}
let layout = 'grid';
document.querySelectorAll('[data-choice]').forEach(group => group.addEventListener('click', event => {
  const button = event.target.closest('button');
  if (!button) return;
  group.querySelectorAll('button').forEach(el => el.setAttribute('aria-pressed',String(el === button)));
  const value = button.dataset.value;
  switch (group.dataset.choice) {
    case 'count': document.querySelector('#layout-choices').hidden = value !== '4'; changeImage('#booth-preview', 'keepsake-' + (value === '4' ? layout : value)); break;
    case 'layout': layout = value; changeImage('#booth-preview', 'keepsake-' + value); break;
    case 'book': changeImage('#book-preview', 'book-page-' + value); break;
    case 'theme': changeImage('#theme-preview', 'diary-' + value); break;
  }
}));
const gallery = document.querySelector('#gallery');
if (gallery) {
  const search = document.querySelector('#search');
  const category = document.querySelector('#category');
  const labels = isEnglish
    ? {diary:'Diary',write:'Writing',booth:'Photo booth',frames:'Frames',calendar:'Calendar',book:'Diary books',themes:'Themes',widget:'Widgets',exports:'Exports'}
    : {diary:'일기',write:'쓰기',booth:'사진관',frames:'프레임',calendar:'달력',book:'일기책',themes:'테마',widget:'위젯',exports:'출력 결과'};
  [...new Set(assets.map(a => a.group))].forEach(group => { const option = document.createElement('option'); option.value = group; option.textContent = labels[group] || group; category.append(option); });
  const initial = new URLSearchParams(location.search).get('group');
  if ([...category.options].some(option => option.value === initial)) category.value = initial;
  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    const selected = assets.filter(a => (!category.value || a.group === category.value) && (a.title_ko + ' ' + a.title_en + ' ' + (labels[a.group] || a.group)).toLocaleLowerCase().includes(query));
    gallery.replaceChildren();
    selected.forEach(asset => {
      const figure = document.createElement('figure');
      const button = document.createElement('button'); button.className = 'zoom'; button.dataset.full = asset.path; button.setAttribute('aria-label',copy(asset.alt_ko + ' 확대', 'Enlarge: ' + asset.alt_en));
      const img = document.createElement('img'); img.src = asset.preview; img.alt = assetText(asset, 'alt'); img.width = asset.width; img.height = asset.height; img.loading = 'lazy';
      const caption = document.createElement('figcaption'); caption.textContent = assetText(asset, 'title');
      button.append(img); figure.append(button,caption); gallery.append(figure);
    });
    document.querySelector('#gallery-count').textContent = selected.length
      ? copy(`${selected.length}개의 화면과 결과`, `${selected.length} screens and samples`)
      : copy('검색 결과가 없습니다. 다른 검색어나 분류를 선택해 주세요.', 'No results. Try another search or category.');
  }
  search.addEventListener('input',render); category.addEventListener('change',render); render();
}
const form = document.querySelector('#deletion-form');
if (form) {
  const status = document.querySelector('#request-status');
  const submit = document.querySelector('#send-request');
  if (emailReady) { submit.disabled = false; status.textContent = copy('메일 앱에서 전송을 완료해야 요청이 접수됩니다. 메일 앱이 없다면 위 이메일 주소로 직접 보내 주세요.', 'Send the message from your email app to submit your request. If no email app is available, write directly to the address above.'); }
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!emailReady || !form.reportValidity()) return;
    const type = document.querySelector('#request-type').value;
    const email = document.querySelector('#account-email').value;
    const note = document.querySelector('#request-note').value;
    const body = copy(
      `네컷일기 / Day in Four 개인정보 요청\n\n요청 종류: ${type}\n계정 이메일: ${email}\n추가 설명: ${note || '없음'}\n\n계정 소유 확인 및 처리 범위를 안내해 주세요.`,
      `Day in Four privacy request\n\nRequest type: ${type}\nAccount email: ${email}\nAdditional details: ${note || 'None'}\n\nPlease explain the ownership verification process and the scope of this request.`
    );
    location.href = `mailto:${config.supportEmail}?subject=${encodeURIComponent(copy('[네컷일기] ', '[Day in Four] ') + type)}&body=${encodeURIComponent(body)}`;
    status.textContent = copy('이메일 앱에서 내용을 확인하고 전송해 주세요. 이 웹페이지에서는 요청이 전송되지 않습니다. 메일 앱이 열리지 않으면 위 주소로 직접 보내 주세요.', 'Review and send the message in your email app. This webpage does not submit the request. If your email app does not open, write directly to the address above.');
  });
}
