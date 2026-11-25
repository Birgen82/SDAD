"""Hulpfuncties: relatieve paden (Page), miniaturen, tekstopmaak en het wegschrijven van pagina's."""

import re
from html import escape

from sdad.config import DEMO, LANDING_DOMAINS, OUT, SITE
from sdad.content import PAGES


def site_link(pg, path):
    """Link vanuit een landingspagina naar de hoofdsite: relatief in de demo, absoluut naar sdad.be bij livegang."""
    if DEMO:
        return pg.u(path)
    if path in LANDING_DOMAINS:
        return LANDING_DOMAINS[path]
    return SITE + "/" + path


def short(t, n=180):
    return t if len(t) < n + 10 else t[:n].rsplit(" ", 1)[0] + "…"


class Page:
    def __init__(self, path):
        self.path = path
        self.r = "../" * path.count("/")  # relatief pad naar de root

    def u(self, p=""):
        return self.r + p if self.r or p else "./"

    def img(self, name, alt, cls="", lazy=True, w=None, h=None):
        size = f' width="{w}" height="{h}"' if w else ' width="800" height="800"'
        return (
            f'<img src="{self.r}assets/img/{name}" alt="{escape(alt)}"{size}'
            f'{' loading="lazy" decoding="async"' if lazy else ""}{f" class={cls!r}" if cls else ""}>'
        )


def thumb(name, size=520):
    """Kleine versie van een foto (voor menu en collages), wordt eenmalig aangemaakt."""
    out = OUT / "assets/img" / f"t_{name}"
    if not out.exists():
        from PIL import Image

        im = Image.open(OUT / "assets/img" / name)
        im.thumbnail((size, size))
        im.save(out, "WEBP", quality=70, method=6)
    return f"t_{name}"


def p(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


def write(pg, html):
    out = OUT / pg.path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf8")
    print("✓", out.relative_to(OUT))


def fix_links(pg, html):
    """Interne sdad.be-links naar de nieuwe pagina's laten wijzen; externe links in een nieuw tabblad."""

    def repl(m):
        href = m.group(1)
        path = re.sub(r"^(https?://(www\.)?sdad\.be)?/", "", href) if re.match(r"^(https?://(www\.)?sdad\.be)?/", href) else None
        if path is not None:
            path = path.split("#")[0].split("?")[0]
            if path and not path.endswith("/"):
                path += "/"
            if path in PAGES:
                return f'<a href="{pg.u(path)}">'
            return f'<a href="{SITE}/{path}">'
        if href.startswith(("http", "//")):
            return f'<a href="{href}" target="_blank" rel="noopener">'
        return m.group(0)

    return re.sub(r'<a href="([^"]*)">', repl, html)


def split_heading(html):
    m = re.match(r"\s*<h2>(.*?)</h2>(.*)", html, re.S)
    return (m.group(1).strip(), m.group(2)) if m else ("", html)


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub("<[^>]+>", "", t).lower()).strip("-")[:50]
