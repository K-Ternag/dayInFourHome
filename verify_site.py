from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

root=Path(__file__).resolve().parent
class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.duplicate=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:self.duplicate.append(a['id'])
            self.ids.add(a['id'])
        for key in ('href','src','data-full'):
            if a.get(key):self.links.append(a[key])
docs={}
for file in root.glob('*.html'):
    doc=Document();doc.feed(file.read_text(encoding='utf-8'));docs[file.name]=doc
errors=[]
for filename,doc in docs.items():
    errors.extend(f'{filename}: duplicate id {v}' for v in doc.duplicate)
    for link in doc.links:
        url=urlsplit(link)
        if url.scheme or url.netloc:continue
        target=unquote(url.path) or filename
        if not (root/target).is_file():errors.append(f'{filename}: missing {link}')
        if url.fragment and target in docs and url.fragment not in docs[target].ids:errors.append(f'{filename}: missing anchor {link}')
result={'html_pages':len(docs),'local_references_checked':sum(len(d.links) for d in docs.values()),'static_errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
