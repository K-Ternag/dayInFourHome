# 네컷일기 / Day in Four 홈페이지

빌드 없이 GitHub Pages에서 제공하는 한국어·영어 정적 홈페이지입니다. 실제 앱 이미지와 PDF 예시를 사용합니다. HTML 본문은 JavaScript 없이도 읽을 수 있습니다. 서버·추적 스크립트·외부 폰트·쿠키를 추가하지 않았습니다.

## 위치와 실행

프로젝트 위치는 `D:\Projects\foutFoldHome`입니다. 기존 앱 소스와 독립된 홈페이지 저장소입니다.

`index.html`을 열거나 폴더에서 `python -m http.server 8080`을 실행하고 `http://localhost:8080`으로 접속하세요.

## 한국어·영어

한국어 시작 페이지는 `index.html`, 영어 시작 페이지는 `index.en.html`입니다. 소개·갤러리·고객지원·개인정보처리방침·삭제 안내·이용약관을 각각 제공합니다. 상단의 한국어 / EN 링크는 같은 페이지와 검색 분류·앵커를 유지합니다. 언어 전환에는 로그인이나 쿠키가 필요하지 않습니다. 언어별 검색 메타데이터와 `hreflang` 링크도 포함합니다.

`build_english.py`에서 영문 문구를 관리합니다. 한국어 HTML을 수정한 뒤 `python build_english.py`를 실행하면 영어 페이지와 양쪽 언어 링크를 다시 생성합니다. `build_site.py`로 전체를 재생성할 때도 자동 호출됩니다. 생성된 `.en.html`을 직접 수정하면 다음 생성 때 덮어씁니다. 이미지의 UI·예시 일기와 PDF는 원본을 공유하므로 일부 한국어가 포함되어 있으며 영문 페이지에 안내합니다.

운영 정보의 영어 안내는 `site-config.js`의 `localized.en`에서 설정합니다. `deletionTimeframe`, `retentionPolicy`, `processingRegion`의 영어 값이 비어 있으면 한국어 운영 문구로 대체하지 않고 영문 검토본 안내를 유지합니다. 연락처·운영자명·시행일·스토어 URL은 공통 설정을 사용합니다.

검증: `python verify_site.py`는 12개 페이지의 경로·앵커·언어 링크와 영문 번역 누락을 검사합니다. `node test_localization.cjs`는 공유 스크립트의 언어별 이미지·운영 설정·영문 메일 작성을 검사합니다. `python browser_check.py`는 양쪽 언어의 반응형 화면과 실제 브라우저 상호작용을 검사합니다. 브라우저 실행이 차단된 환경에서는 그 한계를 `verification.json`에 기록합니다.

## 페이지

| 파일 | 용도 |
| --- | --- |
| index.html | 기능 소개, 사진 수·배치·테마·PDF 내지 미리보기 |
| guide.html | 실제 이미지 45개 검색·분류·원본 확대 |
| privacy.html | 개인정보처리방침 |
| delete-account.html | 계정·데이터 삭제 안내 및 이메일 요청 작성 |
| support.html | 문의·백업·구독 안내 |
| terms.html | 이용약관 |

사진은 원본 PNG와 최적화 WebP를 함께 제공합니다. 갤러리는 로컬 JS 데이터를 사용하므로 `file://`에서도 fetch 제약을 받지 않습니다. 홈페이지는 이미지 원본 확대, 키보드 조작, 모바일 메뉴, 반응형 레이아웃을 지원합니다.

## 운영 정보 입력 — Google Play 제출 전에 필요

`site-config.js`에서 다음을 실제 운영 정보로 설정하세요. 정보가 없으면 실제 연락처를 추측하거나 가짜 접수 완료를 표시하지 않습니다.

- `developerName`: Play 등록정보와 일치하는 개발자/사업자명
- `supportEmail`: 수신·회신 가능한 개인정보 및 삭제 요청 이메일
- `policyEffectiveDate`: 실제 정책 시행일
- `deletionTimeframe`: 본인 확인, 삭제 완료, 회신까지의 기한
- `retentionPolicy`: 계정/구매/문의/로그별 보관 기간, 삭제 후 서버 백업 소거 기간, 법적 보관이 있다면 근거·항목·기간
- `processingRegion`: 실제 Supabase 리전, 수탁자·처리 국가 및 적용되는 국외 이전 고지 사항
- `playStoreUrl`: 실제 공개된 Google Play 앱 URL. 미설정이면 출시 준비 중 표시
- `siteUrl`: 실제 홈페이지 주소 (운영 기록용)
- `policiesApproved`: 정책 본문과 실제 운영의 일치를 검토한 뒤 `true`. 필수 정보가 모두 있어야 검토본 배너가 사라집니다.

지원 이메일이 설정되면 삭제 양식은 mailto 초안을 엽니다. 사이트가 자동으로 삭제하거나 서버에 접수하는 기능이 아닙니다. 메일 앱에서 직접 전송해야 합니다. 서버 계정 삭제는 운영자가 별도로 수행해야 하며, 연락처 설정만으로 운영 절차가 완성되지 않습니다.

`delete-account.html`에는 현재 개발 버전에 앱 내 계정 삭제 경로가 없다는 상태를 명시했습니다. 해당 기능과 운영 절차를 실제 구현·검증한 후 상태 설명도 수정하세요. 개인정보처리방침의 운영 환경 미확정 안내 역시 실제 환경에 맞게 검토하세요. 사용자 답변 없이 처리 기한·법정 보관 기간을 임의로 확정하지 않았습니다.

## Google Play 연결

1. 개인정보처리방침 URL에 `https://<사용자>.github.io/<저장소>/privacy.html`을 입력합니다.
2. 계정 삭제 웹 URL에 `https://<사용자>.github.io/<저장소>/delete-account.html`을 입력합니다.
3. 앱 내 설정에도 개인정보처리방침 및 계정 삭제 요청으로 연결되는 경로를 구현합니다. 현재 앱에는 계정 삭제 경로가 없습니다. 홈페이지 제작만으로 이 요건이 충족되지는 않습니다.
4. 데이터 보안 양식은 출시 APK/AAB의 실제 기능·SDK·서버 배포와 일치하게 작성합니다. 로컬 일기 외에 Plus 인증·결제 정보가 있으므로 무조건 ‘수집 없음’으로 제출하면 안 됩니다.
5. 실제 메일 전송 → 본인 확인 → 계정 및 연관 데이터 삭제 → 보관 예외 안내 → 결과 회신을 운영 환경에서 검증합니다. 계정 삭제는 구독 해지·Drive 삭제와 별개입니다.
6. 공개 URL은 로그인 없이 열려야 하며, 확정된 정책·연락처로 제공되어야 합니다. 초안 상태에서는 Play에 제출하지 마세요.

정책 확인 기준: 2026-10-28.

- [Google Play 사용자 데이터 정책](https://support.google.com/googleplay/android-developer/answer/10144311?hl=ko)
- [계정 삭제 요건](https://support.google.com/googleplay/android-developer/answer/13327111?hl=ko)

정책 문구는 앱 소스의 로컬 저장, Google 인증, Supabase 계정/구독 검증, Drive 백업 흐름에 맞춰 작성한 검토본입니다. 사업자·서비스 지역·실제 운영에 따른 확정 검토가 남아 있습니다.

## GitHub Pages 배포

1. 별도 GitHub 저장소를 만들고 이 폴더의 사이트 파일을 저장소 루트에 업로드합니다.
2. 저장소 Settings → Pages → Build and deployment에서 **Deploy from a branch**, **main**, **/(root)** 를 선택합니다.
3. 배포 후 제공되는 URL을 열어 홈페이지·정책·삭제 페이지가 모두 공개되는지 확인합니다.

모든 내부 링크는 상대 경로이므로 프로젝트 하위 경로에서도 동작합니다. `.nojekyll`도 포함되어 있습니다. 저장소 생성·push·배포는 수행하지 않았습니다. `build_site.py`, `verify_site.py`, `verification.json`, `README.md`는 운영에 필요하지 않아 업로드에서 제외해도 됩니다. 검토 스크린샷도 제외할 수 있습니다.

## 수정과 검증

직접 HTML/CSS/JS를 수정할 수 있습니다. `build_site.py`는 원본 앱의 `marketing/20261028-website-assets`가 있어야 재생성할 수 있는 제작용 스크립트입니다. 실행하면 HTML이 다시 생성되므로 정책 확정 후에는 HTML을 직접 편집하거나 생성기에도 동일 내용을 반영하세요. 사이트 구동에는 Python/Pillow가 필요하지 않습니다.

정적 경로·앵커 검사: `python verify_site.py`. JS 문법 검사: `node --check app.js`. 검증 결과와 브라우저 확인 범위는 `verification.json`을 확인하세요.

## 광고 안내 업데이트 · 2026-10-29

0.8.3의 무료 배너·전면광고 및 Plus 광고 제거를 한국어·영어 소개, 개인정보처리방침과 약관에 반영했다. 생성 스크립트에도 같은 내용을 반영했다.

확인된 공개 홈페이지: https://k-ternag.github.io/dayInFourHome/

이 폴더의 app-ads.txt를 배포하면 /dayInFourHome/app-ads.txt가 된다. AdMob은 https://k-ternag.github.io/app-ads.txt를 확인하므로 **별도 사용자 사이트 저장소 K-Ternag.github.io의 루트에도 같은 파일이 필요하다.** 기존 홈페이지를 옮길 필요는 없다. 이미 사용자 사이트 저장소가 있다면 기존 파일을 보존하며 해당 판매자 행만 추가한다.

공개 정책에는 운영자명·지원 이메일·시행일 등 실제 운영 정보가 여전히 필요하다. 광고 문구 변경만으로 정책 검토 완료 상태로 전환하지 않았다. 공개 사이트 갱신과 AdMob 인증은 별도 단계다.

참고: https://support.google.com/admob/answer/9363762?hl=ko · https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
