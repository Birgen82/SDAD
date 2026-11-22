#!/usr/bin/env python3
"""Maakt één klikbaar voorbeeldbestand van de volledige site (alle pagina's, verkleinde foto's).
Gebruik: python3 preview/make_preview.py  (vanuit de map sdad, na python3 build.py)"""
import base64, io, json, posixpath, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MAX, Q = 520, 52
PAGES = sorted([str(p.parent.relative_to(ROOT)) + "/" if p.parent != ROOT else "" for p in ROOT.rglob("index.html")
                if "preview" not in p.parts], key=lambda x: (x.count("/"), x))
imgs = {}


def key(path):
    if path not in imgs:
        f = ROOT / path
        if f.suffix == ".png":
            imgs[path] = "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()
        else:
            im = Image.open(f); im.thumbnail((MAX, MAX)); b = io.BytesIO(); im.save(b, "WEBP", quality=Q, method=6)
            imgs[path] = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
    return str(list(imgs).index(path))


def resolve(page, href):
    return posixpath.normpath(posixpath.join(page or ".", href))


def fix(page, html):
    html = re.sub(r'(src|data-full)="([^"]*assets/img/[^"]+)"',
                  lambda m: f'data-{"img" if m.group(1) == "src" else "full-img"}="{key(resolve(page, m.group(2)))}"', html)

    def link(m):
        pre, h = m.group(1), m.group(2)
        if h.startswith(("http", "mailto:", "tel:", "#")):
            return m.group(0)
        path, _, frag = h.partition("#")
        t = resolve(page, path) if path else page.rstrip("/")
        t = "" if t == "." else t.rstrip("/") + "/"
        if t in PAGES:
            return pre + f'href="#/{t}"' + (f' data-frag="{frag}"' if frag else "")
        return pre + 'href="#" data-off="1"'
    return re.sub(r'(<a\b[^>]*?)href="([^"]*)"', link, html)


home = (ROOT / "index.html").read_text()
head, foot = fix("", home.split('<main id="main">')[0]), fix("", home.split("</main>")[1])
mains = []
for pg in PAGES:
    h = (ROOT / pg / "index.html").read_text()
    title = re.search(r"<title>(.*?)</title>", h).group(1)
    body = fix(pg, h.split('<main id="main">')[1].split("</main>")[0])
    mains.append(f'<div class="pv-page" data-page="{pg}" data-title="{title}" hidden>{body}</div>')
css = (ROOT / "assets/css/style.css").read_text()
css = re.sub(r"url\(\.\./img/([^)]+)\)", lambda m: "url(data:image/png;base64," + base64.b64encode((ROOT / "assets/img" / m.group(1)).read_bytes()).decode() + ")", css)
head = re.sub(r'<link rel="icon"[^>]*>', "", head)
head = head.replace('<link rel="stylesheet" href="assets/css/style.css">', "<style>" + css + ".pv-note{background:#fff8d6;color:#5a4a00;font-size:.85rem;text-align:center;padding:6px 12px}</style>")
head = head.replace("<body>", '<body><div class="pv-note">Voorbeeld van de nieuwe SDAD-site · foto\'s verkleind</div>')
router = """<script>
const IMG=%s;
document.querySelectorAll('[data-full-img]').forEach(b=>b.dataset.full=IMG[b.dataset.fullImg]);
function load(root){root.querySelectorAll('img[data-img]').forEach(i=>{if(!i.src){i.src=IMG[i.dataset.img];}});}
load(document.querySelector('header'));load(document.querySelector('footer'));
function show(){const h=location.hash.replace(/^#\\//,'').split('#')[0];const t=document.querySelector('.pv-page[data-page="'+h+'"]')||document.querySelector('.pv-page[data-page=""]');
document.querySelectorAll('.pv-page').forEach(p=>p.hidden=p!==t);load(t);document.title=t.dataset.title;document.body.classList.remove('menu-open');window.scrollTo(0,0);}
document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;
 if(a.dataset.off){e.preventDefault();alert('Deze pagina zit niet in het voorbeeldbestand.');return;}
 if(a.dataset.frag){e.preventDefault();location.hash=a.getAttribute('href');setTimeout(()=>{const el=document.getElementById(a.dataset.frag);if(el)el.scrollIntoView();},60);}});
addEventListener('hashchange',show);show();
</script>""" % json.dumps(list(imgs.values()))
foot = foot.replace('<script src="assets/js/main.js" defer></script>', router + "<script>" + (ROOT / "assets/js/main.js").read_text() + "</script>")
out = ROOT / "preview/sdad-site-preview.html"
out.write_text(head + '<main id="main">' + "".join(mains) + "</main>" + foot)
print(len(PAGES), "pagina's,", len(imgs), "foto's,", out.stat().st_size // 1024, "KB")
