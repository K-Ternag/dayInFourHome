from pathlib import Path
import json
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
report={'browser':'not run','checks':[]}
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()
        errors=[]
        page.on('pageerror',lambda error: errors.append(str(error)))
        for name in [p + suffix for suffix in ['', '.en'] for p in ['index','guide','privacy','delete-account','support','terms']]:
            page.goto((root/(name+'.html')).as_uri())
            for width in [360,390,768,1024,1440]:
                page.set_viewport_size({'width':width,'height':1000})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(name,width)
            report['checks'].append(name+': no overflow at five widths')
        page.goto((root/'index.html').as_uri())
        page.locator('[data-choice=count] button').first.click()
        assert page.locator('#layout-choices').is_hidden()
        assert 'keepsake-1' in page.locator('#booth-preview img').get_attribute('src')
        page.locator('[data-choice=theme] button').last.click()
        assert 'diary-album' in page.locator('#theme-preview img').get_attribute('src')
        page.locator('[data-choice=book] button').last.click()
        assert 'book-page-two' in page.locator('#book-preview img').get_attribute('src')
        page.locator('.zoom').first.click()
        assert page.locator('#lightbox').evaluate('(el)=>el.open')
        page.keyboard.press('Escape')
        assert not page.locator('#lightbox').evaluate('(el)=>el.open')
        page.set_viewport_size({'width':390,'height':1000})
        page.locator('.menu-toggle').click()
        assert page.locator('#navigation').is_visible()
        page.screenshot(path=str(root/'preview-mobile.png'),full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        page.screenshot(path=str(root/'preview-desktop.png'),full_page=True)
        page.goto((root/'guide.html').as_uri())
        assert page.locator('#gallery figure').count()==45
        page.locator('#search').fill('不存在')
        assert page.locator('#gallery figure').count()==0
        page.locator('#search').fill('book')
        assert page.locator('#gallery figure').count()>0
        page.goto((root/'index.en.html').as_uri())
        assert page.locator('html').get_attribute('lang')=='en'
        page.locator('[data-choice=count] button').first.click()
        assert page.locator('#layout-choices').is_hidden()
        assert 'keepsake-1' in page.locator('#booth-preview img').get_attribute('src')
        page.locator('[data-choice=theme] button').last.click()
        assert 'diary-album' in page.locator('#theme-preview img').get_attribute('src')
        assert page.locator('#theme-preview img').get_attribute('alt')=='Soft album · diary entry'
        page.locator('[data-choice=book] button').last.click()
        assert 'book-page-two' in page.locator('#book-preview img').get_attribute('src')
        page.locator('.zoom').first.click()
        assert page.locator('#lightbox').evaluate('(el)=>el.open')
        page.keyboard.press('Escape')
        page.screenshot(path=str(root/'preview-desktop-en.png'),full_page=True)
        page.set_viewport_size({'width':390,'height':1000})
        page.screenshot(path=str(root/'preview-mobile-en.png'),full_page=True)
        page.goto((root/'guide.en.html').as_uri()+'?group=book#gallery')
        assert page.locator('#category').input_value()=='book'
        assert '?group=book#gallery' in page.locator('.language-switch [lang=ko]').get_attribute('href')
        assert 'screens and samples' in page.locator('#gallery-count').inner_text()
        page.locator('#category').select_option('')
        assert page.locator('#gallery figure').count()==45
        page.locator('#search').fill('no-matching-screen-123')
        assert 'No results' in page.locator('#gallery-count').inner_text()
        page.locator('.language-switch [lang=ko]').click()
        assert page.locator('html').get_attribute('lang')=='ko'
        page.goto((root/'delete-account.en.html').as_uri())
        assert page.locator('#send-request').is_disabled()
        assert 'confirmed' in page.locator('#request-status').inner_text()
        assert not errors,errors
        report['browser']='passed'
        report['checks'].append('Image selectors, modal Escape, mobile menu and gallery search passed')
        report['checks'].append('English previews, gallery, language links and unconfigured deletion form passed')
        browser.close()
except Exception as exc:
    report['browser']='incomplete'
    report['reason']=str(exc)[:1600]
(root/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
