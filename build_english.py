"""Build static English pages and add reciprocal language links to Korean pages.

Run after build_site.py when regenerating Korean content. No image kit needed.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit, urlunsplit
import json
import re

ROOT = Path(__file__).resolve().parent
PAGES = ('index', 'guide', 'support', 'privacy', 'delete-account', 'terms')
ASSETS = json.loads((ROOT / 'assets-data.js').read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
COPY = {
    '사진으로 쓰는 나만의 작은 일기': 'A LITTLE DIARY, A LASTING MEMORY',
    '오늘의 네 장이,': 'Little moments today.',
    '오래 꺼내 볼 추억으로.': 'Memories to keep.',
    '사진 한 장, 짧은 이야기로 오늘을 기록해요.': 'A photo, a few words, a little piece of your day.',
    '차곡차곡 모인 하루는 기념사진과 일기책이 됩니다.': 'Turn your everyday stories into photo keepsakes and monthly diary books.',
    'Google Play 출시 준비 중': 'Coming soon to Google Play',
    '기록하는 방법 보기 ↓': 'See how it works ↓',
    'Android · 1–4장의 사진 · 나만의 일기': 'Android · 1–4 photos · Your own little diary',
    '실제 앱 화면 · 예시 기록': 'Real app screen · sample entry',
    '앱에서 만든 기념사진': 'A keepsake made in the app',
    '오늘을 기록하기': 'Capture your day',
    '기념사진 만들기': 'Make a photo keepsake',
    '일기책으로 간직하기': 'Keep it in a diary book',
    '거창하지 않아도,': 'Ordinary days.',
    '남기고 싶은 하루가 있으니까.': 'Worth remembering.',
    '아침의 커피, 지나가다 만난 꽃, 함께한 저녁.': 'Morning coffee. A flower on your walk. Dinner together.',
    '사진 몇 장과 짧은 이야기면 충분해요.': 'A few photos and a little story are all you need.',
    '사진을 골라요': 'Pick your photos',
    '직접 촬영하거나 사진첩에서 한 장부터 네 장까지.': 'Take a photo or choose one to four from your library.',
    '오늘을 네 칸에 담아요': 'Put your day in place',
    '사진의 위치와 순서를 마음에 들게 조절해요.': 'Arrange your photos just the way you like.',
    '짧은 이야기를 남겨요': 'Add a little story',
    '기분과 날씨, 오늘의 한마디를 함께 저장해요.': 'Save a few words, your mood, and the weather.',
    '일기 속 사진이,': 'From a diary photo',
    '나만의 작은 기념사진으로.': 'to a little keepsake.',
    '한 장은 작은 즉석사진처럼, 네 장은 네컷 액자처럼.': 'One photo for an instant print feel. Four for a photo booth frame.',
    '사진 수에 맞춰 오늘의 기억을 담아보세요.': 'Find the right layout for your memories.',
    'PLUS · 이미지 저장·공유 / 미리보기 무료': 'PLUS · Save & share images / Free previews',
    '아래는 실제 앱의 출력 예시입니다.': 'Explore real examples exported from the app.',
    '1장': '1 photo', '2장': '2 photos', '3장': '3 photos', '4장': '4 photos',
    '세로 네컷': 'Photo strip', '네칸 액자': 'Four-photo grid', '두 줄 네컷': 'Twin strips',
    '사진관 화면 자세히 보기 →': 'Explore the photo booth →',
    '여덟 가지 프레임 견본 · 사진 수 미리보기와는 별개의 디자인 예시입니다.': 'Eight frame designs · These samples are independent of the photo-count preview above.',
    '날짜를 누르면,': 'Tap a date.',
    '그날의 기억이.': 'Revisit a memory.',
    '작은 사진으로 채워지는 나의 달력.': 'A calendar filled with little glimpses of your life.',
    '평범했던 날도 다시 보면 소중한 한 장면이 돼요.': 'Even an ordinary day can become a favorite memory.',
    '기록 목록과 사진 달력에서 지난 일기를 돌아보고,': 'Browse your journal or photo calendar',
    '마음에 남는 하루를 다시 펼쳐보세요.': 'and return to a day you want to remember.',
    '실제 사진 달력 · 예시 기록': 'Real photo calendar · sample entries',
    '한 달의 추억을,': 'A month of memories.',
    '한 권의 PDF로.': 'A book of your own.',
    '표지와 제목, 담고 싶은 일기를 직접 고르면': 'Choose a cover, a title, and the entries you love.',
    '흩어진 하루가 한 달의 이야기가 됩니다.': 'Bring those little days together in a monthly PDF.',
    'PLUS · PDF 저장·공유 / 미리보기 무료': 'PLUS · Save & share PDFs / Free previews',
    '한 쪽에 일기 하나': 'One entry per page', '한 쪽에 일기 두 개': 'Two entries per page',
    '실제 PDF 예시 보기 ↗': 'Open a sample PDF ↗',
    '디지털 PDF 파일이며, 인쇄·제본·배송 서비스가 아닙니다.': 'A digital PDF file. Printing, binding, and delivery are not included.',
    '월별 PDF · 실제 표지': 'Monthly PDF · sample cover',
    '월별 PDF · 한 쪽에 일기 하나': 'Monthly PDF · one entry per page',
    '01 · 표지 색 고르기': '01 · Choose a cover color',
    '02 · 제목 남기기': '02 · Give it a title',
    '03 · 내지 구성하기': '03 · Pick a page layout',
    '04 · 담을 일기 고르기': '04 · Select your entries',
    '같은 하루도,': 'Your memories.',
    '나에게 어울리는 분위기로.': 'Your kind of mood.',
    '사진 중심 미니멀, 차분한 종이 일기장, 부드러운 앨범.': 'Photo Minimal, a quiet Paper Diary, or a soft Album.',
    '세 가지 테마를 무료로 만나보세요.': 'Find your favorite among three free themes.',
    '사진 중심 미니멀': 'Photo Minimal', '미니멀': 'Minimal', '종이 일기장': 'Paper Diary', '앨범': 'Album',
    '실제 화면 모두 둘러보기 →': 'Browse all app screens →',
    '홈 화면에서 바로': 'Right from your home screen',
    '‘오늘의 네 장’ 위젯의 빈칸을 눌러 직접 촬영하고 오늘의 초안에 모아보세요.': 'Tap an empty space in the daily photo widget to take a photo and add it to today’s draft.',
    '조금 더 나답게': 'Make it feel like you',
    '프레임, 필터, 스티커와 그리기. 사진 위치와 순서까지 마음에 들게 다듬어요.': 'Frames, filters, stickers, and drawings. Fine-tune the position and order of your photos, too.',
    '내 기록은 내 곁에': 'Keep your stories close',
    '일기는 기기에 보관해요. 앱 잠금과 파일 백업·복원으로 소중한 기록을 관리하세요.': 'Your diary stays on your device. Manage your memories with app lock and file backup and restore.',
    '개인정보 처리 방식 →': 'How we handle your data →',
    '궁금한 이야기': 'A few things to know',
    '사진이 꼭 네 장이어야 하나요?': 'Do I need exactly four photos?',
    '아니요. 일기와 사진관 모두 1~4장의 사진으로 시작할 수 있어요.': 'No. Both diary entries and the photo booth work with one to four photos.',
    '무료로 무엇을 쓸 수 있나요?': 'What can I use for free?',
    '일기, 달력, 테마, 위젯, 기본 사진 편집, 앱 잠금, 수동 파일 백업·복원을 사용할 수 있어요. 사진관 이미지와 월별 PDF 저장·공유는 Plus 기능입니다. 가격과 제공 여부는 출시된 앱의 구매 화면에서 확인하세요.': 'Diary entries, the calendar, themes, widgets, basic photo editing, app lock, and manual file backup and restore are free. Saving and sharing photo booth images and monthly PDFs are Plus features. Check the purchase screen in the released app for pricing and availability.',
    '휴대폰을 바꾸면 기록을 옮길 수 있나요?': 'Can I move my diary to a new phone?',
    '파일 백업 후 새 기기에서 복원할 수 있어요. 앱을 삭제하기 전, 백업 파일을 앱 바깥의 안전한 위치에 보관해 주세요.': 'Yes. Create a file backup and restore it on your new device. Before uninstalling the app, keep the backup in a safe place outside the app.',
    '계정을 삭제하면 구독도 해지되나요?': 'Does deleting my account cancel my subscription?',
    '계정 삭제와 Google Play 구독 해지는 별개입니다.': 'Account deletion and Google Play subscription cancellation are separate. See the',
    '계정·데이터 삭제 안내': 'account and data deletion guide',
    '에서 삭제 범위와 구독 관리 방법을 확인하세요.': 'for deletion details and subscription management.',
    '어떤 기기에서 사용할 수 있나요?': 'Which devices are supported?',
    'Android 앱입니다. 출시 후 Google Play의 기기 호환성 안내를 확인해 주세요.': 'Day in Four is an Android app. Once it launches, check Google Play for device compatibility.',
    '오늘의 작은 순간부터 남겨볼까요?': 'Start with a little moment today.',
    '오래 기억하고 싶은 하루, 한 장부터 시작하세요.': 'One photo is all it takes to keep a day close.',
    '화면 둘러보기 ↗': 'Explore the app ↗',
    '주요 기능 바로가기': 'Explore the main features', '사진 수 선택': 'Number of photos',
    '네 장 배치 선택': 'Four-photo layout', '일기책 내지 선택': 'Diary book page layout',
    '앱 테마 선택': 'App theme',
}
for asset in ASSETS:
    COPY.setdefault(asset['title_ko'], asset['title_en'])
    COPY.setdefault(asset['alt_ko'], asset['alt_en'])
    COPY[asset['alt_ko'] + ' 확대'] = 'Enlarge: ' + asset['alt_en']


def english_url(value):
    url = urlsplit(value)
    if not url.scheme and not url.netloc and url.path in {p + '.html' for p in PAGES}:
        return urlunsplit(('', '', url.path[:-5] + '.en.html', url.query, url.fragment))
    return value


def translate(value):
    key = value.strip()
    if not re.search('[가-힣]', key):
        return value
    if key not in COPY:
        raise ValueError('Missing English copy: ' + repr(key))
    return value[:len(value) - len(value.lstrip())] + COPY[key] + value[len(value.rstrip()):]


class HomeTranslator(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []

    def handle_starttag(self, tag, attrs):
        converted = []
        for key, value in attrs:
            if value is not None:
                value = english_url(value) if key == 'href' else translate(value)
            converted.append(key if value is None else f'{key}="{escape(value, quote=True)}"')
        self.output.append('<' + tag + (' ' + ' '.join(converted) if converted else '') + '>')

    def handle_endtag(self, tag):
        self.output.append(f'</{tag}>')

    def handle_data(self, data):
        self.output.append(escape(translate(data)))


NOTICE = '''<div class="notice" data-policy-notice><strong>Pre-launch draft</strong><br>
The operator, contact details, response times, and retention policies have not been finalized.
Check the information below for the effective policy and whether requests are being accepted.</div>'''
IDENTITY = '''<p>App: <strong>Day in Four</strong> (com.fourfold.journal)<br>
Operator: <span data-config="developerName">To be confirmed</span><br>
Privacy and deletion inquiries: <span data-contact>Contact details coming soon</span><br>
Effective date: <span data-config="policyEffectiveDate">To be confirmed before launch</span></p>'''

GUIDE = '''<section class="wrap section"><span class="eyebrow">A CLOSER LOOK</span>
<h1>A little look inside<br>Day in Four.</h1><p class="lead">Real app screens, photo keepsakes, and diary book samples.<br>Tap an image to see the full-size version.</p>
<p class="muted">Screenshots include Korean and English interfaces. Sample entries and the sample PDF may contain Korean text.</p>
<div class="gallery-tools"><label for="search">Search screens<input id="search" type="search" placeholder="Calendar, photo booth, book…"></label><label for="category">Category<select id="category"><option value="">All categories</option></select></label></div>
<p id="gallery-count" aria-live="polite"></p><div class="gallery" id="gallery"></div>
<noscript><p>Search and image enlargement require JavaScript. <a href="index.en.html">Explore the main features on the homepage.</a></p></noscript></section>'''

SUPPORT = '''<article class="wrap legal"><span class="eyebrow">HERE TO HELP</span>
<h1>How can we help?</h1><p class="lead">A little help with keeping your memories.<br>Find guidance on using Day in Four and managing your data.</p>
<div class="notice"><h2 style="margin-top:0">App support</h2><p>Support email: <span data-contact>Support contact details will be available before launch</span></p>
<p class="muted">Please include your app version, device model, Android version, and the steps that led to the issue. Do not send original diary entries, passwords, or verification codes.</p></div>
<h2>Moving your diary to a new phone</h2><p>Save a backup file from the app’s settings and restore it on your new device. Before uninstalling the app, make sure the backup is saved outside the app.</p>
<h2>Deleting an account or personal data</h2><p>Your account, on-device diary, and Drive backups are stored separately. See <a href="delete-account.en.html">account and data deletion</a> for instructions and request options.</p>
<h2>Managing your Plus subscription</h2><p>Check your subscription and cancellation options in <a href="https://play.google.com/store/account/subscriptions">Google Play subscriptions</a>. Sign in with the Google account used for the purchase.</p>
<h2>Exploring the app before you start</h2><p>Browse the <a href="guide.en.html">app screen gallery</a> or open a <a href="assets/sample-diary-book.pdf">sample monthly PDF</a>. The sample PDF contains Korean text.</p></article>'''

PRIVACY = f'''<article class="wrap legal"><span class="eyebrow">PRIVACY &amp; YOUR MEMORIES</span>
<h1>Privacy policy</h1>{NOTICE}{IDENTITY}
<p>This policy explains how the Day in Four app and its website handle personal information. Optional Google sign-in, Plus payments, and Google Drive backups apply when these features are offered in the released version and you choose to use them.</p>
<h2>1. Information, purposes, and storage</h2><div class="table-scroll"><table><thead><tr><th>Category</th><th>Information</th><th>Purpose and storage</th></tr></thead><tbody>
<tr><td>Diary and photos</td><td>Selected or captured photos, diary text, dates, moods, weather, tags, favorites, editing details, drafts, and recovery records</td><td>Creating, finding, displaying, and exporting entries. Stored by default in app-specific storage on your device. Diary content is not uploaded to the developer’s server.</td></tr>
<tr><td>Settings</td><td>Theme, language, reminders, app lock, and display settings</td><td>Remembering your preferences. Stored on your device.</td></tr>
<tr><td>Plus account</td><td>Google authentication identifiers and provided basic profile details, such as email, name, and profile image; app user ID; authentication sessions</td><td>Google sign-in, Supabase authentication, and linking subscription access. The information provided depends on the Google consent screen.</td></tr>
<tr><td>Subscription</td><td>Purchase tokens, product and plan IDs, subscription status, expiry and verification times, and account-linking identifiers</td><td>Verifying Google Play purchases and managing Plus access. Tokens are encrypted when stored on the server. The app does not directly process card numbers.</td></tr>
<tr><td>Optional backups</td><td>Diary entries, photos, and related metadata included in a backup</td><td>A file location you select or your own Google Drive app data area. Drive access is used for backups.</td></tr>
<tr><td>Support and deletion requests</td><td>Reply email address, account identifiers you provide, and the content of your request</td><td>Verifying identity and handling your request. Do not include passwords, verification codes, or original diary entries.</td></tr>
</tbody></table></div>
<h2>2. Sources and optional permissions</h2><p>Photos come from items you select in the system photo picker or capture with the camera. Optional notification permission is used for diary reminders. The current app does not request contacts, location, or microphone permissions. Google sign-in and Drive connections require separate consent.</p>
<h2>3. External services and data processing</h2><p>Google handles sign-in, Google Play payments, and Drive backups you connect. Supabase supports server processing for Plus authentication and subscription verification. Diary entries and photos are not sent to the Plus authentication or payment server. If you share images or PDFs or store backups with another service, that service’s policies apply.</p>
<p>Processing countries, regions, and international transfer details: <span data-config="processingRegion">To be announced once the operating environment is finalized. Processors, destination countries, data categories, purposes, transfer methods, retention periods, and related procedures must be confirmed before launch.</span></p>
<p>See the <a href="https://policies.google.com/privacy">Google privacy policy</a>, <a href="https://supabase.com/privacy">Supabase privacy policy</a>, and <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a>.</p>
<h2>4. Retention and deletion</h2><p>You manage records stored on your device. Deleting an entry may leave trash or recovery data. To remove all app data on a device, clear the app’s storage in Android settings or uninstall the app. Separately saved photos, PDFs, backup files, and Drive data are not removed by this action.</p>
<p>Retention of account, payment, and support records and residual data after deletion: <span data-config="retentionPolicy">The operating policy is not yet final. Retention periods for each data category, deletion timing, server backup removal, and the basis, scope, and duration of any legally required retention will be specified in the final policy.</span></p>
<p>Drive backup is designed to retain up to three recent snapshots per device. Older photo fragments may remain, so replacing a snapshot does not necessarily completely delete all original data. See the deletion guide for removing Drive app data.</p>
<h2>5. Access, correction, deletion, and withdrawal of consent</h2><p>You can view and edit on-device diary entries in the app. Use the privacy contact above to request access to, correction or deletion of, or restrictions on processing account information and support records. Limited identity verification may be needed. See <a href="delete-account.en.html">account and data deletion</a> for instructions by data type.</p>
<h2>6. Safeguards</h2><p>Account, payment, and Drive communications use HTTPS. Authentication sessions and purchase tokens are protected according to their storage mechanisms. Diary data is managed in app-specific storage. Exported backups, PDFs, and images may contain personal records, so choose where you share them carefully.</p>
<h2>7. Advertising, analytics, and this website</h2><p>The current app does not include advertising or analytics SDKs. This website does not use advertising scripts, visitor analytics scripts, or tracking cookies. GitHub may process connection information, such as IP addresses, when hosting the site on GitHub Pages. Text entered in the deletion request form is not sent to or stored on this site’s server. It is processed by your email service and the recipient only if you actually send it from your email app.</p>
<h2>8. Policy changes</h2><p>Material changes to data categories, purposes, or external services will be announced on this page and, where needed, in the app. Any necessary consent procedures will be followed. Refer to the version with a confirmed operator and effective date.</p></article>'''

DELETION = f'''<article class="wrap legal"><span class="eyebrow">YOU ARE IN CONTROL</span>
<h1>Account and data deletion</h1><p class="lead">Manage your Day in Four account and records. You can prepare an account deletion request without reinstalling the app.</p>{NOTICE}{IDENTITY}
<h2>1. Request deletion of a Plus account</h2><p>Select a request type below and enter the email used for your Plus sign-in. When your email app opens, review and send the message yourself to submit it. You can also email the privacy contact directly. We recommend sending from the account’s email address to help verify ownership.</p>
<p>Requests cover the Plus authentication account and linked profile, subscription access, and purchase verification records. On-device diaries, personal Drive backups, exported files, and your Google account itself must be managed separately.</p>
<form id="deletion-form"><label for="request-type">Request type</label><select id="request-type"><option>Delete my Plus account and all linked data</option><option>Keep my account — ask about deleting specific personal data</option><option>Help with deleting backups or on-device data</option></select>
<label for="account-email">Account email</label><input id="account-email" type="email" autocomplete="email" required maxlength="254" placeholder="Email used for Plus sign-in">
<label for="request-note">Additional details (optional)</label><textarea id="request-note" rows="4" maxlength="1500" placeholder="Describe only the data involved. Do not include passwords, verification codes, or photos."></textarea>
<p class="muted">Your entries are not stored on this website. If you send the email, they are shared with the recipient to handle your request.</p><button class="button primary" id="send-request" type="submit" disabled>Draft a deletion request email</button><p id="request-status" role="status">Email requests will be enabled once the contact address is confirmed.</p></form>
<noscript><p>Drafting an email requires JavaScript. You can email the privacy contact above directly with your request type and account email.</p></noscript>
<p>Response timeframe: <span data-config="deletionTimeframe">To be confirmed before requests are accepted</span><br>Retention exceptions and periods: <span data-config="retentionPolicy">To be announced when the operating policy is finalized</span></p>
<p>We are preparing a process to verify account ownership, explain the deletion scope and retention exceptions, and report the outcome. The current development version does not include in-app account deletion. Request channels and operating procedures are planned to be connected before release.</p>
<h2>2. Remove all diary data and photos from a device</h2><ol><li>If you want to keep any records, first create a file backup and save it outside the app.</li><li>Open Android <strong>Settings → Apps → Day in Four → Storage → Clear data</strong>, or uninstall the app. Menu names vary by device manufacturer.</li><li>This removes the app’s diary entries, drafts, recovery data, and settings. Deleting individual entries in the app does not necessarily immediately erase all recovery data.</li></ol>
<p>Original photos in your library, downloaded images and PDFs, manual backup files, and files shared with others are not deleted by this action. Delete them separately from their respective locations.</p>
<h2>3. Delete Google Drive backups</h2><ol><li>First turn off automatic backup and disconnect Drive in the app so that backups are not recreated.</li><li>In Google Drive on the web, open <strong>Settings → Manage apps</strong>, find the entry linked to Day in Four, and choose <strong>Options → Delete hidden app data</strong>. The registered OAuth app may appear under a different name.</li><li>You can also revoke access in <a href="https://myaccount.google.com/connections">Google account connections</a>. Disconnecting or revoking access alone does not delete existing backup data.</li></ol>
<h2>4. Cancel a Google Play subscription</h2><p><strong>Deleting your account or uninstalling the app does not cancel your subscription.</strong> Open <a href="https://play.google.com/store/account/subscriptions">Google Play subscriptions</a>, select Day in Four Plus, and cancel. Refunds and remaining access periods are subject to the purchase terms and Google Play policies. Deleting an account may prevent you from using the Plus access linked to it.</p>
<h2>5. Keep your account and delete specific data</h2><p>You can delete on-device diary entries yourself. For specific personal data held on the server, select “Keep my account — ask about deleting specific personal data” in the form and describe the data involved. Data needed for authentication or an active subscription may require further explanation and confirmation of the scope.</p>
<p><a href="privacy.en.html">Read the privacy policy →</a></p></article>'''

TERMS = f'''<article class="wrap legal"><span class="eyebrow">TERMS OF USE</span><h1>Terms of use</h1>{NOTICE}{IDENTITY}
<h2>1. The service</h2><p>Day in Four is an Android app for writing diary entries with photos and text, viewing records, and keeping them as images, PDFs, or backup files using supported features. Available features depend on the installed version and purchase terms.</p>
<h2>2. Your content and rights</h2><p>Rights in content you create or select remain with the respective rights holders. Respect other people’s copyright and privacy and use content you have permission to use. Use that infringes others’ rights or disrupts normal service operation may be restricted.</p>
<h2>3. Paid features</h2><p>Plus pricing, billing periods, automatic renewal, and benefits are governed by the terms shown on the Google Play purchase screen. Subscription management, cancellation, and refunds follow Google Play procedures and applicable law. Account deletion or app removal alone does not cancel a subscription.</p>
<h2>4. Keeping and restoring your records</h2><p>Diary entries are stored on your device by default. Keep backups in case you change or lose your device or delete app data. Files you share or export must be managed in their respective locations. Liability for matters attributable to the service is subject to applicable law.</p>
<h2>5. Changes and discontinuation</h2><p>Material changes to features, these terms, or service availability will be announced through appropriate channels on the website or in the app. Changes to or discontinuation of paid services are subject to the purchase terms and applicable law.</p>
<h2>6. Support and privacy</h2><p>For app questions, visit <a href="support.en.html">support</a>. Read the <a href="privacy.en.html">privacy policy</a> for data handling, or <a href="delete-account.en.html">account and data deletion</a> for account closure. These terms do not limit rights provided by applicable law.</p></article>'''


def language_links(page, language):
    return f'''<span class="language-switch" aria-label="Language"><a href="{page}.html" lang="ko" hreflang="ko"{(' aria-current="true"' if language == 'ko' else '')}>한국어</a><a href="{page}.en.html" lang="en" hreflang="en"{(' aria-current="true"' if language == 'en' else '')}>EN</a></span>'''


def alternates(page):
    return f'''<link rel="alternate" hreflang="ko" href="{page}.html"><link rel="alternate" hreflang="en" href="{page}.en.html"><link rel="alternate" hreflang="x-default" href="{page}.en.html">'''


def render(page, title, body, description):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(description, quote=True)}"><meta name="theme-color" content="#faf9f6">
<meta property="og:title" content="{escape(title, quote=True)} · Day in Four"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta property="og:locale:alternate" content="ko_KR">
<title>{escape(title)} · Day in Four</title><link rel="stylesheet" href="styles.css">{alternates(page)}</head>
<body><a class="skip" href="#main">Skip to content</a><header><div class="wrap"><a class="brand" href="index.en.html">Day in Four<small>A LITTLE PHOTO DIARY</small></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu</button><nav id="navigation" aria-label="Main navigation"><a href="index.en.html#story">Your diary</a><a href="index.en.html#booth">Photo booth</a><a href="index.en.html#book">Diary books</a><a href="guide.en.html">Explore</a><a href="support.en.html">Support</a>{language_links(page, 'en')}</nav></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div><a class="brand" href="index.en.html">Day in Four<small>A LITTLE PHOTO DIARY</small></a><p class="muted">Little moments. Lasting memories.</p></div><div><div class="footer-links"><a href="privacy.en.html">Privacy policy</a><a href="delete-account.en.html">Account &amp; data deletion</a><a href="terms.en.html">Terms of use</a><a href="support.en.html">Contact</a></div><p class="muted">© <span data-year>2026</span> <span data-developer>Day in Four</span></p></div></div></footer>
<dialog id="lightbox" aria-labelledby="lightbox-title"><div class="dialog-bar"><span id="lightbox-title">View full-size image</span><button aria-label="Close enlarged image" id="close-lightbox">×</button></div><img class="zoomed" alt=""><p>Real app screens or exports · sample entries may contain Korean text</p></dialog><script src="site-config.js"></script><script src="assets-data.js"></script><script src="app.js"></script></body></html>
'''


def build():
    home = (ROOT / 'index.html').read_text(encoding='utf-8')
    main = re.search(r'<main id="main">(.*?)</main>', home, re.S).group(1)
    translator = HomeTranslator()
    translator.feed(main)
    home_en = ''.join(translator.output)
    home_en = home_en.replace('<div class="hero-art">', '<div class="hero-art" aria-label="App and keepsake previews">', 1)
    home_en = home_en.replace('Real app screen · sample entry', 'Real app screen · sample entry in Korean')
    home_en = home_en.replace('A keepsake made in the app', 'A keepsake made in the app · Korean sample')
    home_en = home_en.replace('A digital PDF file. Printing, binding, and delivery are not included.', 'A digital PDF file. Printing, binding, and delivery are not included. The sample PDF contains Korean text.')
    default = 'A little photo diary for everyday moments. Start with one to four photos, create photo keepsakes, and keep your memories in monthly PDF diary books.'
    pages = {
        'index': ('Little moments. Lasting memories.', home_en, default),
        'guide': ('Explore the app', GUIDE, 'Browse real Day in Four app screens, photo booth exports, and diary book samples.'),
        'support': ('Support', SUPPORT, 'Get help with Day in Four, moving your diary, subscriptions, and managing your data.'),
        'privacy': ('Privacy policy', PRIVACY, 'How Day in Four handles on-device diary entries, optional accounts, subscriptions, backups, and privacy requests.'),
        'delete-account': ('Account and data deletion', DELETION, 'Request Plus account deletion, remove on-device records and Google Drive backups, and manage your subscription.'),
        'terms': ('Terms of use', TERMS, 'Terms for using the Day in Four Android photo diary app and optional Plus features.'),
    }
    for page, (title, body, description) in pages.items():
        (ROOT / (page + '.en.html')).write_text(render(page, title, body, description), encoding='utf-8')
        korean = ROOT / (page + '.html')
        source = korean.read_text(encoding='utf-8')
        source = re.sub(r'<span class="language-switch".*?</span>', '', source)
        source = re.sub(r'<link rel="alternate"[^>]*>', '', source)
        source = source.replace('</nav>', language_links(page, 'ko') + '</nav>', 1)
        source = source.replace('</head>', alternates(page) + '</head>', 1)
        korean.write_text(source, encoding='utf-8')
    print('Built 6 English pages and reciprocal language links on 6 Korean pages.')


if __name__ == '__main__':
    build()
