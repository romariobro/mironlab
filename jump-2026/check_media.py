from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
root=Path(__file__).parent
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        for key,value in attrs:
            if key in ("href","src") and value: self.links.append(value)
errors=[]
pages=list((root/"media").rglob("*.html"))
for page in pages:
    parser=Links(); parser.feed(page.read_text(encoding="utf-8"))
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme or u.netloc or not u.path: continue
        target=page.parent/unquote(u.path)
        if not target.exists(): errors.append((str(page.relative_to(root)),link))
print("HTML pages:",len(pages),"Missing local targets:",len(errors))
for error in errors: print(error)
assert len(pages)==58 and not errors
