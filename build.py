#!/usr/bin/env python3
"""Bouwt de statische SDAD-website. Gebruik: python3 build.py

Header, footer en gedeelde blokken staan hier één keer; elke pagina wordt
als <map>/index.html weggeschreven zodat de URL's gelijk blijven aan sdad.be.
"""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://sdad.be"
BOOKING = "https://afspraaksdad.youcanbook.me/"
MAIL = "info@sdad.be"
PHONES = [("Lies Nuyttens", "0473 52 09 20", "+32473520920"), ("Arne Deseure", "0478 42 81 95", "+32478428195")]
REGIO = "Oost- en West-Vlaanderen"
MAPS = "https://www.google.com/maps/search/?api=1&query=Prinsdomlaan+50+8870+Izegem"
SOCIAL = {
    "Facebook": "https://www.facebook.com/DeseureArneNuyttensLies/",
    "Instagram": "https://www.instagram.com/schilderwerken_sdad/",
    "LinkedIn": "https://www.linkedin.com/company/sdad-arne-deseure/",
}
ICONS = {
    "Facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></svg>',
    "Instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM21.9 8c-.1-1.6-.4-3-1.6-4.2S17.6 2.2 16 2.1C14.4 2 9.6 2 8 2.1 6.4 2.2 5 2.5 3.8 3.7S2.2 6.4 2.1 8C2 9.6 2 14.4 2.1 16c.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.6.1 6.4.1 8 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.1-1.6.1-6.4 0-8zm-2 9.7a3.3 3.3 0 0 1-1.9 1.9c-1.3.5-4.4.4-5.9.4s-4.6.1-5.9-.4a3.3 3.3 0 0 1-1.9-1.9c-.5-1.3-.4-4.4-.4-5.9s-.1-4.6.4-5.9A3.3 3.3 0 0 1 6.2 4c1.3-.5 4.4-.4 5.9-.4s4.6-.1 5.9.4a3.3 3.3 0 0 1 1.9 1.9c.5 1.3.4 4.4.4 5.9s.1 4.6-.4 5.9z"/></svg>',
    "LinkedIn": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.9 21H3.2V8.9h3.7V21zM5 7.3a2.1 2.1 0 1 1 0-4.3 2.1 2.1 0 0 1 0 4.3zM21 21h-3.7v-5.9c0-1.4 0-3.2-2-3.2s-2.2 1.5-2.2 3.1v6H9.4V8.9H13v1.7c.5-.9 1.7-1.9 3.4-1.9 3.7 0 4.4 2.4 4.4 5.6V21z"/></svg>',
}

DIENSTEN = [
    ("Schilderwerken", [("Binnen", "diensten/schilderwerken/binnen/"), ("Buiten", "diensten/schilderwerken/buiten/"),
                        ("Decoratieve technieken", "diensten/schilderwerken/decoratieve-technieken/")]),
    ("Interieurafwerking", [("Gordijnen", "diensten/interieurafwerking/gordijnen/"), ("Lamellen", "diensten/interieurafwerking/lamellen/")]),
]
MENU = [("Realisaties", "realisaties/"), ("Over SDAD", "over-sdad/"), ("Blog", "blog/"), ("Contact", "contact/")]

REAL = json.loads((ROOT / "data/realisaties.json").read_text(encoding="utf8"))
BLOG = json.loads((ROOT / "data/blog.json").read_text(encoding="utf8"))
DETAILS = json.loads((ROOT / "data/details.json").read_text(encoding="utf8"))
LABELS = {"binnen": "Binnen", "buiten": "Buiten", "gordijnen": "Gordijnen", "lamellen": "Lamellen", "decoratieve-technieken": "Decoratieve technieken"}
LEGAL = json.loads((ROOT / "data/legal.json").read_text(encoding="utf8"))
PAGES = {"", "over-sdad/", "realisaties/", "blog/", "contact/"} | {f"{k}/" for k in LEGAL} | {p for _, items in [
    ("", [("", "diensten/schilderwerken/binnen/"), ("", "diensten/schilderwerken/buiten/"), ("", "diensten/schilderwerken/decoratieve-technieken/"),
          ("", "diensten/interieurafwerking/gordijnen/"), ("", "diensten/interieurafwerking/lamellen/")])] for _, p in items} \
    | {f"realisaties/{r['slug']}/" for r in REAL} | {f"blog/{b['slug']}/" for b in BLOG}


def short(t, n=180):
    return t if len(t) < n + 10 else t[:n].rsplit(" ", 1)[0] + "…"


# ---------- bouwstenen ----------
class Page:
    def __init__(self, path):
        self.path = path
        self.r = "../" * path.count("/")  # relatief pad naar de root

    def u(self, p=""):
        return self.r + p if self.r or p else "./"

    def img(self, name, alt, cls="", lazy=True, w=None, h=None):
        size = f' width="{w}" height="{h}"' if w else ' width="800" height="800"'
        return (f'<img src="{self.r}assets/img/{name}" alt="{escape(alt)}"{size}'
                f'{" loading=\"lazy\" decoding=\"async\"" if lazy else ""}{f" class={cls!r}" if cls else ""}>')


def nav(pg):
    cur = pg.path
    dd_cur = " is-current" if cur.startswith("diensten/") else ""
    cols = "".join(
        f'<div><strong>{g}</strong>' + "".join(
            f'<a href="{pg.u(p)}"{" aria-current=page" if p == cur else ""}>{n}</a>' for n, p in items) + "</div>"
        for g, items in DIENSTEN)
    links = "".join(f'<a href="{pg.u(p)}"{" aria-current=page" if p == cur else ""}>{n}</a>' for n, p in MENU)
    return f"""<a class="skip" href="#main">Naar inhoud</a>
<div class="topbar"><div class="wrap">
  <span>Prinsdomlaan 50, 8870 Izegem · actief in {REGIO}</span>
  <a href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a>
  <a href="mailto:{MAIL}">{MAIL}</a>
</div></div>
<header class="header"><div class="wrap">
  <a class="logo" href="{pg.u()}" aria-label="SDAD – naar de startpagina">{pg.img("logo_dark.png", "SDAD – Schilderkracht tot de vierde macht", lazy=False, w=42, h=58)}</a>
  <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Hoofdmenu">
    <div class="dd{dd_cur}"><button aria-expanded="false">Diensten</button><div class="dd-panel">{cols}</div></div>
    {links}
    <a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a>
  </nav>
</div></header>"""


def footer(pg):
    dienst_links = "".join(f'<li><a href="{pg.u(p)}">{n}</a></li>' for _, items in DIENSTEN for n, p in items)
    menu_links = "".join(f'<li><a href="{pg.u(p)}">{n}</a></li>' for n, p in [("Home", "")] + MENU)
    phones = "".join(f'<li>{n}<br><a href="tel:{t}">{d}</a></li>' for n, d, t in PHONES)
    socials = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICONS[n]}</a>' for n, u in SOCIAL.items())
    return f"""<footer class="footer"><div class="wrap">
  <div class="footer-grid">
    <div>{pg.img("logo.png", "SDAD – Schilderkracht tot de vierde macht", cls="footer-logo", w=66, h=92)}</div>
    <div><h4>Bedrijfsgegevens</h4><p><strong style="color:#fff">SDAD bv</strong><br>Prinsdomlaan 50<br>8870 Izegem<br><br>BE0823.935.816<br><br>Werkgebied: {REGIO}</p><a href="{MAPS}" target="_blank" rel="noopener">Route plannen →</a></div>
    <div><h4>Diensten</h4><ul>{dienst_links}</ul></div>
    <div><h4>Website</h4><ul>{menu_links}</ul></div>
    <div><h4>Advies nodig?</h4><ul><li><a href="mailto:{MAIL}">{MAIL}</a></li>{phones}</ul>
      <p style="margin:18px 0 0">Volg ons</p><div class="socials">{socials}</div></div>
  </div>
  <div class="subfooter">
    <span>© 2026 SDAD. Alle rechten voorbehouden.</span>
    <a href="{pg.u('cookie-en-privacybeleid/')}">Cookie- en privacybeleid</a>
    <a href="{pg.u('disclaimer/')}">Disclaimer</a>
    <a href="{pg.u('algemene-voorwaarden/')}">Algemene Voorwaarden BV SDAD</a>
  </div>
</div></footer>
<div class="mobile-bar"><a href="tel:{PHONES[0][2]}">Bel ons</a><a href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek</a></div>"""


SCHEMA = json.dumps({
    "@context": "https://schema.org", "@type": "HousePainter", "name": "SDAD bv",
    "slogan": "Schilderkracht tot de vierde macht", "url": SITE + "/", "email": MAIL,
    "telephone": PHONES[0][2], "vatID": "BE0823.935.816", "image": SITE + "/site/assets/files/1/kleurbepaling_linkedin.jpeg",
    "address": {"@type": "PostalAddress", "streetAddress": "Prinsdomlaan 50", "postalCode": "8870",
                "addressLocality": "Izegem", "addressCountry": "BE"},
    "areaServed": [{"@type": "AdministrativeArea", "name": "Oost-Vlaanderen"}, {"@type": "AdministrativeArea", "name": "West-Vlaanderen"}],
    "sameAs": list(SOCIAL.values()),
}, ensure_ascii=False)


def layout(pg, title, desc, body, og_img="1_kleurbepaling_linkedin.webp"):
    return f"""<!doctype html>
<html lang="nl-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{SITE}/{pg.path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{SITE}/{pg.path}">
<meta property="og:image" content="{SITE}/site/assets/files/1/kleurbepaling_linkedin.1200x628.jpeg">
<meta name="theme-color" content="#00080a">
<link rel="icon" href="{pg.r}assets/img/list_icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Nunito+Sans:wght@400;600;700&display=swap">
<link rel="stylesheet" href="{pg.r}assets/css/style.css">
<script type="application/ld+json">{SCHEMA}</script>
</head>
<body>
{nav(pg)}
<main id="main">
{body}
</main>
{footer(pg)}
<script src="{pg.r}assets/js/main.js" defer></script>
</body>
</html>
"""


GARANTIE_VOORWAARDE = "mits een geschikte ondergrond en een correct opgebouwd verfsysteem"


def trust_strip(pg):
    """Korte strook met kernbeloftes onder de hero (alleen claims die al op de site staan)."""
    items = [
        ("25+ jaar", "ervaring in het schildersvak"),
        ("10 jaar garantie", f'op gevelschilderwerk, {GARANTIE_VOORWAARDE} <a href="{pg.u("diensten/schilderwerken/buiten/")}#garantie">Meer info</a>'),
        ("Snel antwoord", "op uw vraag, met een vrijblijvend plaatsbezoek"),
        (REGIO, f'ons werkgebied, vanuit Izegem <a href="{pg.u()}#werkgebied">Bekijk waar</a>'),
    ]
    cells = "".join(f"<li><strong>{t}</strong><span>{s}</span></li>" for t, s in items)
    return f'<section class="trust" aria-label="Waarom SDAD"><div class="wrap"><ul>{cells}</ul></div></section>'


def werkwijze(pg):
    """Werkwijze in 5 stappen, opgebouwd uit teksten die al op de site staan."""
    steps = [
        ("Plaatsbezoek", "We komen vrijblijvend langs, luisteren naar uw wensen en bekijken samen de mogelijkheden en de staat van de ondergrond."),
        ("Kleuradvies", "We denken mee over kleuren, materialen en afwerking, afgestemd op de ruimte, de lichtinval en uw stijl."),
        ("Offerte en planning", "U ontvangt een duidelijke offerte en planning, zodat u precies weet wat u mag verwachten."),
        ("Voorbereiding en uitvoering", "Eerst een correcte voorbereiding van de ondergrond, daarna een vakkundige uitvoering. Met duidelijke communicatie en netheid op de werf."),
        ("Oplevering", "Een afwerking tot in de kleinste details en een zorgeloze samenwerking tot de oplevering. We doen wat we zeggen en zeggen wat we doen."),
    ]
    items = "".join(f"<li><span class=\"step-nr\">{i}</span><h3>{t}</h3><p>{d}</p></li>" for i, (t, d) in enumerate(steps, 1))
    return f"""<section class="section section--dark" id="werkwijze"><div class="wrap">
  <span class="eyebrow">Onze werkwijze</span><h2>Zo pakken we uw project aan</h2>
  <p class="lead narrow">Een mooi resultaat begint lang voor de eerste verflaag. Van het eerste gesprek tot de oplevering weet u steeds waar u aan toe bent.</p>
  <ol class="steps">{items}</ol>
  <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plan stap 1: uw plaatsbezoek</a></div>
</div></section>"""


def garantie_block(pg):
    return f"""<section class="section section--soft" id="garantie" style="scroll-margin-top:90px"><div class="wrap">
  <div class="guarantee">
    <div class="guarantee__badge" aria-hidden="true"><strong>10</strong><span>jaar</span></div>
    <div>
      <span class="eyebrow">Garantie</span><h2>10 jaar garantie op gevelschilderwerk</h2>
      {p(f"Voor gevelschilderwerken kunnen wij, {GARANTIE_VOORWAARDE}, opleveren met <strong>10 jaar garantie</strong>.",
         "Daarom besteden we veel aandacht aan een correcte voorbereiding van de ondergrond, technisch advies en het gebruik van hoogwaardige kwaliteitsproducten.",
         "Voor schilderwerken aan buitenschrijnwerk gelden andere omstandigheden. Houten ramen en deuren worden veel intensiever belast door zon, regen, temperatuurschommelingen en mechanische belasting. Deze werken kunnen daarom niet met dezelfde garantievoorwaarden worden opgeleverd als gevelschilderwerken.")}
    </div>
  </div>
</div></section>"""


def werkgebied(pg):
    """Werkgebied met plaatsen uit de eigen realisaties als bewijs."""
    seen, tags = set(), []
    for r in REAL:
        m = re.search(r"(?:\bte\s+|@)([a-zë]+)", r["title"], re.I)
        place = m.group(1).capitalize() if m else None
        if not place and not r["title"].startswith("Residentie") and re.search(r"\s([A-Z][a-z]+)$", r["title"]):
            place = r["title"].split()[-1]  # bv. "Frituur De Platse Lendelede"
        if place and place not in seen:
            seen.add(place)
            href = pg.u("realisaties/" + r["slug"] + "/")
            tags.append(f'<li><a href="{href}">{place}</a></li>')
    return f"""<section class="section" id="werkgebied" style="scroll-margin-top:90px"><div class="wrap split" style="align-items:start">
  <div><span class="eyebrow">Werkgebied</span><h2>Actief in heel {REGIO}</h2>
  <p>Vanuit Izegem werken we voor particulieren en bedrijven in heel {REGIO}. We reageren snel op uw vraag en plannen graag een vrijblijvend plaatsbezoek bij u ter plaatse.</p>
  <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a></div></div>
  <div><h3>Hier werkten we al</h3><ul class="tags place-tags">{"".join(tags)}</ul></div>
</div></section>"""


def cta(pg, title="Een mooi resultaat begint met een goed gesprek.",
        text="Tijdens een vrijblijvend plaatsbezoek luisteren we naar uw wensen, geven we professioneel advies en bekijken we samen de mogelijkheden voor uw schilderwerken of interieurafwerking."):
    return f"""<section class="section"><div class="wrap"><div class="cta">
  <h2>{title}</h2><p>{text}</p>
  <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Vraag uw plaatsbezoek aan</a>
  <a class="btn btn--ghost" href="{pg.u('contact/')}">Offerte aanvragen</a></div>
</div></div></section>"""


def crumbs(pg, items):
    parts = [f'<a href="{pg.u()}">Home</a>'] + [f'<a href="{pg.u(p)}">{n}</a>' if p is not None else n for n, p in items]
    return f'<nav class="crumbs" aria-label="Kruimelpad">{"<span>/</span>".join(parts)}</nav>'


def page_hero(pg, crumb, eyebrow, title, content, img=None, alt=""):
    pic = f'<div class="page-hero__img">{pg.img(img, alt, lazy=False)}</div>' if img else ""
    plain = "" if img else " page-hero--plain"
    return f"""<section class="page-hero{plain}"><div class="wrap">
  <div>{crumbs(pg, crumb)}<span class="eyebrow">{eyebrow}</span><h1>{title}</h1>{content}</div>{pic}
</div>{pg.img("red_deco.png", "", cls="deco deco--br", w=220, h=240) if img else ""}</section>"""


def gallery(pg, title, imgs, link=None, alt_base=""):
    more = f'<a class="arrow-link" href="{pg.u(link)}">Bekijk enkele volledige realisaties</a>' if link else ""
    items = "".join(
        f'<button type="button" data-full="{pg.r}assets/img/{i}">{pg.img(i, f"{alt_base} – sfeerbeeld {n + 1}", w=400, h=400)}</button>'
        for n, i in enumerate(imgs))
    return f"""<section class="section"><div class="wrap">
  <div class="head-row"><h2>{title}</h2>{more}</div>
  <div class="gallery">{items}</div>
</div></section>"""


def faq(title, qa, soft=True):
    items = "".join(f"<details><summary>{q}</summary><div class=\"answer\">{a}</div></details>" for q, a in qa)
    return f"""<section class="section{' section--soft' if soft else ''}"><div class="wrap">
  <span class="eyebrow">Veelgestelde vragen</span><h2>{title}</h2>
  <div class="faq">{items}</div>
</div></section>"""


def video(pg, img, url, label, alt):
    return f'<a class="video" href="{url}" target="_blank" rel="noopener">{pg.img(img, alt, w=800, h=500)}<span class="video__play" aria-hidden="true"></span><span class="video__label">{label}</span></a>'


def card(pg, href, img, title, text="", more="Lees meer", meta="", attrs="", external=False):
    t = ' target="_blank" rel="noopener"' if external else ""
    return f"""<a class="card" href="{href}"{t}{attrs}>
  <div class="card__img">{pg.img(img, title, w=500, h=375)}</div>
  <div class="card__body">{f'<div class="card__meta">{meta}</div>' if meta else ""}<h3>{title}</h3>{f"<p>{text}</p>" if text else ""}<span class="card__more">{more}</span></div>
</a>"""


def p(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


def write(pg, html):
    out = ROOT / pg.path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf8")
    print("✓", out.relative_to(ROOT))


SERVICES = [
    ("diensten/schilderwerken/binnen/", "1340_hectaar_5.webp", "Binnenschilderwerken", "Van kleuradvies tot perfecte afwerking, alles voor een interieur dat klopt."),
    ("diensten/schilderwerken/buiten/", "1345_gevel_kortrijk.webp", "Buitenschilderwerken", "Bescherming, uitstraling en vakmanschap voor uw gevel en buitenschrijnwerk."),
    ("diensten/schilderwerken/decoratieve-technieken/", "2442_techniek_12.webp", "Decoratieve technieken", "Unieke afwerkingen met karakter, structuur en beleving."),
    ("diensten/interieurafwerking/gordijnen/", "1351_modelapp_3.webp", "Gordijnen", "Sfeer, privacy en afwerking perfect afgestemd op uw interieur."),
    ("diensten/interieurafwerking/lamellen/", "1354_modelapp_4.webp", "Lamellen", "Modern, functioneel en perfect afgestemd op uw ruimte."),
]


# ---------- Home ----------
def home():
    pg = Page("")
    services = "".join(card(pg, pg.u(h), i, t, x) for h, i, t, x in SERVICES)
    benefits = "".join(f'<div>{pg.img("list_icon.png", "", w=13, h=15)}{b}</div>' for b in [
        "Ervaren vakmensen", "Persoonlijke aanpak", "Meedenkend advies", "Nakomen van afspraken &amp; planning",
        "Capaciteit en flexibiliteit", "Tijdige en heldere offertes", "Duidelijke communicatie", "Netheid op de werf"])
    recent = [r for s in ["babu-gent", "buitenschilderwerken-kasteel-blauwhuis-te-izegem", "gevel-villa-te-knokke"] for r in REAL if r["slug"] == s]
    recent_cards = "".join(card(pg, pg.u(f"realisaties/{r['slug']}/"), r["img"], r["title"], more="Bekijk realisatie") for r in recent)
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    <span class="eyebrow">Schilderwerken &amp; interieurafwerking · {REGIO}</span>
    <h1>Een mooi resultaat begint lang voor de eerste verflaag.</h1>
    <p class="lead">Wij begeleiden u van kleuradvies tot een perfect afgewerkt eindresultaat. Met persoonlijk advies, duidelijke communicatie en een ervaren team zorgen we voor een zorgeloos traject van begin tot einde.</p>
    <p class="power-title">Wij bezorgen Schilderkracht tot de vierde macht</p>
    <ul class="power">
      <li><b>Stielkennis</b>voor een vakkundige uitvoering.</li>
      <li><b>Service</b>voor een zorgeloze samenwerking.</li>
      <li><b>Snelheid</b>voor een vlotte en duidelijke planning.</li>
      <li><b>Stijl</b>voor een afwerking tot in de kleinste details.</li>
    </ul>
    <p style="margin-top:22px">Zo creëren we ruimtes waar mensen graag wonen, werken en leven.</p>
    <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a><a class="btn btn--ghost" href="{pg.u('contact/')}">Offerte aanvragen</a></div>
  </div>
  <div class="hero__img">{pg.img("1045_home_header.webp", "Kunstzinnig portret beschilderd in de kleuren van SDAD", lazy=False)}</div>
</div></section>
{trust_strip(pg)}

<section class="section"><div class="wrap">
  <div class="head-row"><div><span class="eyebrow">Onze diensten</span><h2>Wat we voor u doen</h2></div></div>
  <div class="grid services">{services}</div>
</div></section>

<section class="section section--soft"><div class="wrap split">
  <div>
    <span class="eyebrow">Over SDAD</span><h2>Advies &amp; vakmanschap</h2>
    <p>Bij <a href="{pg.u('over-sdad/')}">SDAD</a> begeleiden we particulieren en bedrijven bij <a href="{pg.u('diensten/schilderwerken/binnen/')}">binnen</a>- en <a href="{pg.u('diensten/schilderwerken/buiten/')}">buitenschilderwerken</a>, <a href="{pg.u('diensten/schilderwerken/decoratieve-technieken/')}">decoratieve technieken</a> en interieurafwerking (<a href="{pg.u('diensten/interieurafwerking/gordijnen/')}">gordijnen</a> en <a href="{pg.u('diensten/interieurafwerking/lamellen/')}">lamellen</a>). Van kleuradvies tot oplevering zorgen we voor een resultaat waarin kwaliteit, uitstraling en vakmanschap samenkomen.</p>
    <p>Met meer dan 25 jaar ervaring en een team van gespecialiseerde schilders beschikken we over de kennis en expertise om elk project professioneel uit te voeren. Of het nu gaat om een woning, kantoor, praktijkruimte, horecazaak of residentieel project, we denken mee over de juiste keuzes en zorgen voor een afwerking die jarenlang blijft overtuigen.</p>
    <p>Wat ons onderscheidt, is onze persoonlijke aanpak. We luisteren naar uw wensen, adviseren waar nodig en communiceren helder gedurende het volledige traject. Zo weet u steeds waar u aan toe bent en kan u rekenen op een zorgeloze samenwerking van eerste gesprek tot oplevering.</p>
    <p>De basis van dat vertrouwen is eenvoudig: <strong>we doen wat we zeggen en zeggen wat we doen.</strong></p>
    <div class="btns"><a class="btn" href="{pg.u('over-sdad/')}">Meer over ons</a><a class="btn btn--ghost" href="{pg.u('contact/')}">Contacteer ons</a></div>
  </div>
  <div>{pg.img("1_kleurbepaling_linkedin.webp", "Kleurbepaling met kleurstalen bij SDAD")}</div>
</div>{pg.img("red_deco.png", "", cls="deco deco--br", w=220, h=240)}</section>
{werkwijze(pg)}

<section class="section"><div class="wrap">
  <span class="eyebrow">Waarom SDAD</span><h2>Daarom kiezen klanten voor SDAD</h2>
  <div class="benefits">{benefits}</div>
</div></section>

<section class="section section--soft"><div class="wrap">
  <div class="head-row"><div><span class="eyebrow">Portfolio</span><h2>Recente realisaties</h2></div><a class="arrow-link" href="{pg.u('realisaties/')}">Alle realisaties</a></div>
  <div class="grid grid--3">{recent_cards}</div>
</div></section>
{werkgebied(pg)}
{cta(pg)}"""
    write(pg, layout(pg, "Schilderwerken SDAD | binnen, buiten en interieurafwerking",
                     "Bij schilderwerken SDAD uit Izegem kunt u terecht voor professionele binnen en buiten schilderwerken, decoratieve afwerkingen en raamdecoratie in Oost- en West-Vlaanderen.", body))


# ---------- Over SDAD ----------
def over():
    pg = Page("over-sdad/")
    values = [("Klantgericht", "we luisteren, denken mee en begeleiden klanten naar de juiste keuzes."),
              ("Efficiënt", "we maken duidelijke afspraken, werken georganiseerd en zorgen voor een vlotte uitvoering."),
              ("Proactief", "we denken vooruit, anticiperen op uitdagingen en zoeken actief naar oplossingen."),
              ("Duurzaamheid", "we kiezen voor kwalitatieve oplossingen die mooi blijven op lange termijn en bouwen graag aan duurzame klantenrelaties."),
              ("Gegarandeerd", "we voeren elk project zorgvuldig, correct en volgens de afgesproken kwaliteitsnormen uit."),
              ("Open communicatief", "we luisteren naar elkaar, maken alles bespreekbaar en communiceren open en eerlijk.")]
    vals = "".join(f'<div class="value"><h3>{n}</h3><p>{t[0].upper() + t[1:]}</p></div>' for n, t in values)
    links = [("Binnenschilderwerken", pg.u("diensten/schilderwerken/binnen/")), ("Buitenschilderwerken", pg.u("diensten/schilderwerken/buiten/")),
             ("Decoratieve technieken", pg.u("diensten/schilderwerken/decoratieve-technieken/")), ("Gordijnen", pg.u("diensten/interieurafwerking/gordijnen/")),
             ("Lamellen", pg.u("diensten/interieurafwerking/lamellen/"))]
    verthe = '<a href="https://www.verthe-interieurs.be/" target="_blank" rel="noopener">Verthe Interieurs</a>'
    body = page_hero(pg, [("Over SDAD", None)], "Over SDAD", "Het verhaal achter SDAD", p(
        "Wat in 2008 begon als de eenmanszaak van Arne Deseure, groeide in 2016 uit tot SDAD BV. Toen Lies in 2017 mee in de zaak stapte, werd verder gebouwd aan een gedeelde visie gebaseerd op vakmanschap, kwaliteit en persoonlijke service.",
        "Vandaag is SDAD uitgegroeid tot een gevestigde waarde in de sector, met een team van gespecialiseerde schilders dat dagelijks particulieren en bedrijven begeleidt bij schilderwerken en interieurafwerking."),
        "1378_linkedin_30_graden.webp", "SDAD viert 30 jaar vakmanschap") + f"""

<section class="section"><div class="wrap split">
  <div>{pg.img("2509_arne_en_lies_samen.webp", "Arne Deseure en Lies Nuyttens")}</div>
  <div><span class="eyebrow">Zaakvoerders</span><h2>Drijvende kracht achter SDAD</h2>
  <p>Achter SDAD staan ondernemers Arne en Lies. Samen bouwen zij dagelijks verder aan een bedrijf waarin vakmanschap, kwaliteit en persoonlijke opvolging centraal staan. Arne bewaakt de technische uitvoering en kwaliteit op de werf, terwijl Lies klanten begeleidt van eerste contact tot oplevering. Elk vanuit hun eigen expertise vormen ze een sterk complementair duo.</p></div>
</div></section>

<section class="section section--soft"><div class="wrap grid grid--2" style="align-items:start">
  <article class="person">{pg.img("1423_arne_bewerkt.webp", "Arne Deseure")}
    <h2 style="margin-top:28px">Arne Deseure</h2><p class="role">Vakmanschap als fundament</p>
    {p("Al meer dan 25 jaar leeft Arne Deseure voor het schildersvak. Wat begon als een passie, groeide uit tot een carrière waarin vakkennis, kwaliteit en voortdurende bijscholing centraal staan in alles wat hij doet.",
       "Als meewerkend zaakvoerder binnen SDAD bewaakt Arne dagelijks de kwaliteit van de uitvoering. Hij volgt projecten op, ondersteunt het team op de werf en deelt zijn ervaring met de vakmensen met wie hij samenwerkt.",
       "Daarnaast blijft hij zich verdiepen in nieuwe technieken, materialen en afwerkingsmethodes, zodat SDAD blijft inspelen op de nieuwste ontwikkelingen binnen het vak.",
       "Zijn jarenlange ervaring en doorgedreven kennis vormen vandaag nog steeds een van de fundamenten waarop SDAD gebouwd is.")}
  </article>
  <article class="person">{pg.img("2436_profielfoto_lies.webp", "Lies Nuyttens")}
    <h2 style="margin-top:28px">Lies Nuyttens</h2><p class="role">De verbindende schakel</p>
    {p("Sinds Lies in 2017 mee in de zaak stapte, bouwt ze dagelijks mee aan de groei van SDAD. Vandaag vormt ze de verbindende schakel tussen klanten, medewerkers en organisatie.",
       "Voor veel klanten is Lies het eerste aanspreekpunt binnen SDAD. Ze begeleidt projecten van eerste kennismaking tot oplevering, denkt mee over kleuren en afwerkingen en zorgt voor een duidelijke communicatie gedurende het volledige traject.",
       "Daarnaast staat ze in voor de dagelijkse organisatie van het bedrijf. Van planning en personeelsopvolging tot administratie en klantencontacten: Lies zorgt ervoor dat zowel klanten als medewerkers kunnen rekenen op een vlotte en gestructureerde aanpak.",
       "Met haar gedrevenheid, betrokkenheid en ondernemingszin bouwt ze samen met Arne verder aan één duidelijke ambitie: een bedrijf uitbouwen waar kwaliteit, vertrouwen en mensen centraal staan.")}
  </article>
</div></section>

<section class="section"><div class="wrap split split--rev">
  <div>{pg.img("2438_teamfoto.webp", "Het team van SDAD")}</div>
  <div><span class="eyebrow">Ons team</span><h2>Het team achter SDAD</h2>
  {p("Achter elk geslaagd project staat een team van gemotiveerde vakmensen die elke dag het beste van zichzelf geven.",
     "Binnen SDAD geloven we dat kwaliteit niet alleen bepaald wordt door materialen of technieken, maar vooral door de mensen die het werk uitvoeren. Daarom investeren we in vakkennis, samenwerking en een positieve werkcultuur waarin verantwoordelijkheid en betrokkenheid centraal staan.",
     "Elke medewerker brengt zijn eigen ervaring en talenten mee, maar deelt dezelfde visie: afspraken nakomen, kwalitatief werk afleveren en trots zijn op het resultaat dat wordt afgeleverd.",
     "Samen vormen zij de kracht achter SDAD en zorgen zij er elke dag voor dat klanten kunnen rekenen op kwaliteit, vakmanschap en een betrouwbare partner.")}</div>
</div></section>
{werkwijze(pg)}

<section class="section section--soft"><div class="wrap">
  <span class="eyebrow">Onze waarden</span><h2>Het DNA van SDAD</h2>
  <p class="lead narrow">Deze waarden vormen de basis van hoe we samenwerken en onze projecten aanpakken.</p>
  <div class="grid grid--3 values" style="margin-top:32px">{vals}</div>
</div></section>

<section class="section"><div class="wrap split">
  <div><span class="eyebrow">Twee expertises, één visie</span><h2>Samen sterker voor onze klanten</h2>
  {p("Vandaag hebben klanten meer keuzes dan ooit op vlak van interieur, materialen en afwerking. Net daarom geloven wij sterk in het samenbrengen van de juiste expertises rond één project.",
     f"Daarom werken SDAD Schilderwerken en {verthe} al jarenlang nauw samen. Wat ons verbindt, is dezelfde visie op kwaliteit, afwerking en begeleiding van klanten.",
     f"{verthe} begeleidt klanten bij interieuradvies, zit-, woon- en slaapcomfort en totaalinrichting. Bij SDAD vertalen we kleurkeuzes en afwerkingsmogelijkheden naar vakkundig uitgevoerde schilderwerken.",
     "Samen zorgen we ervoor dat interieur en afwerking elkaar versterken en keuzes niet los van elkaar worden gemaakt, maar samen één logisch geheel vormen. Met telkens hetzelfde doel: klanten helpen om met vertrouwen keuzes te maken die op elkaar afgestemd zijn.")}
  </div>
  <div>{video(pg, "2434_thumbnail_video_sdad_verthe.webp", "https://www.youtube.com/watch?v=zO2ZFUFUiMw", "Bekijk de film: SDAD × Verthe Interieurs", "Film over de samenwerking tussen SDAD en Verthe Interieurs")}</div>
</div></section>

<section class="section section--soft"><div class="wrap">
  <span class="eyebrow">Ontdek onze diensten</span><h2>Waarmee kunnen we u helpen?</h2>
  <ul class="tags" style="margin-top:20px">{"".join(f'<li><a href="{u}" style="text-decoration:none;color:inherit">{n}</a></li>' for n, u in links)}</ul>
</div></section>
{cta(pg)}"""
    write(pg, layout(pg, "Over SDAD | Schilderwerken en interieurafwerking in Izegem",
                     "Schilderwerken SDAD uit Izegem heeft meer dan 25 jaar ervaring in schilderwerken.", body))


# ---------- Dienstpagina's ----------
def service(path, title, desc, crumb_group, hero_title, hero_html, hero_img, sections, gal_title, gal, faq_title, qa, gal_link=None):
    pg = Page(path)
    name = crumb_group[1]
    body = page_hero(pg, [(crumb_group[0], None), (name, None)], crumb_group[0], hero_title, hero_html, hero_img, name)
    for i, s in enumerate(sections):
        body += s(pg) if callable(s) else s
    body += gallery(pg, gal_title, gal, gal_link, name)
    body += faq(faq_title, qa)
    body += cta(pg)
    write(pg, layout(pg, title, desc, body))


def text_section(eyebrow, title, html, soft=False, aside=""):
    inner = f'<div class="split"><div><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{html}</div><div>{aside}</div></div>' if aside else \
        f'<div class="narrow"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{html}</div>'
    return f'<section class="section{" section--soft" if soft else ""}"><div class="wrap">{inner}</div></section>'


def binnen():
    def vid(pg):
        return f"""<section class="section section--dark"><div class="wrap split">
  <div><span class="eyebrow">Achter de schermen</span><h2>Onze vakmensen aan het werk</h2>
  <p>Achter elk mooi eindresultaat schuilt vakmanschap. Neem een kijkje achter de schermen bij één van onze ploegen tijdens binnenschilderwerken.</p>
  <div class="btns"><a class="btn btn--ghost" href="https://www.youtube.com/watch?v=tOgcMzXHw5E" target="_blank" rel="noopener">Bekijk de video</a></div></div>
  <div>{video(pg, "2506_thumbnail_video_binnenschilderwerken.webp", "https://www.youtube.com/watch?v=tOgcMzXHw5E", "Binnenschilderwerken in beeld", "Video: SDAD aan het werk tijdens binnenschilderwerken")}</div>
</div></section>"""

    service("diensten/schilderwerken/binnen/", "Binnenschilderwerken Izegem | SDAD",
            "Bij schilderbedrijf SDAD uit Izegem, West-Vlaanderen kunt u terecht voor professionele binnenschilderwerken.",
            ("Schilderwerken", "Binnenschilderwerken"), "Een mooi interieur begint met de juiste afwerking",
            p("Schilderwerken bepalen mee de uitstraling, sfeer en beleving van een ruimte.",
              "Bij SDAD begeleiden we particulieren en bedrijven bij alle schilderwerken, van kleuradvies en voorbereiding tot de uiteindelijke afwerking. We luisteren naar uw wensen, denken mee over materialen, kleuren en technieken en zorgen voor een resultaat dat perfect aansluit bij uw interieur.",
              "Of het nu gaat om een nieuwbouw, renovatie, woning, kantoor of praktijkruimte: elk project krijgt dezelfde aandacht voor detail, kwaliteit en afwerking.",
              "Dankzij jarenlange ervaring, vakkennis en een gestructureerde aanpak zorgen we ervoor dat elk project correct wordt voorbereid en professioneel wordt afgewerkt. Zo creëren we ruimtes waarin mensen zich goed voelen, graag wonen, werken en thuiskomen."),
            "1340_hectaar_5.webp",
            [text_section("Voorbereiding", "Een perfect resultaat begint bij de juiste ondergrond", p(
                "Een mooi schilderresultaat staat of valt met de kwaliteit van de ondergrond. Daarom beperken we ons bij SDAD niet enkel tot het schilderwerk zelf.",
                "Indien nodig verzorgen we ook plamuurwerken om muren en plafonds strak en egaal af te werken. Voor nieuwbouw- en renovatieprojecten adviseren we vaak vliesbehang of renovatievlies als basis voor een duurzaam en verzorgd eindresultaat.",
                "Door eerst aandacht te besteden aan de voorbereiding en opbouw van de ondergrond zorgen we ervoor dat de uiteindelijke afwerking niet alleen mooi oogt, maar ook jarenlang mooi blijft.",
                "Van voorbereiding tot eindafwerking begeleiden we u graag naar een resultaat waarin alles klopt.")),
             vid,
             lambda pg: text_section("Kleuradvies", "Meer dan alleen een kleur op de muur", p(
                 "De juiste kleur bepaalt mee de sfeer van een ruimte. Toch heeft elke kleur een andere uitstraling afhankelijk van de ruimte, lichtinval, materialen en omgeving.",
                 "Daarom kijken we bij SDAD verder dan enkel een kleurstaal. We luisteren naar uw wensen, bekijken de functie van de ruimte en denken mee over het totaalplaatje. Zo komen we samen tot keuzes die niet alleen vandaag mooi zijn, maar waar u ook op lange termijn tevreden van blijft.",
                 "Of u nu houdt van tijdloos en rustig, warm en huiselijk of net uitgesproken en karaktervol: wij begeleiden u graag naar een resultaat dat perfect aansluit bij uw stijl en interieur.",
                 "Dankzij onze ervaring met kleuren, materialen en afwerkingstechnieken helpen we u keuzes maken die niet alleen mooi ogen, maar ook perfect passen bij uw woning, interieur en manier van leven.",
                 f'<strong>Twijfelt u over kleuren of afwerking?</strong><br>Tijdens een <a href="{BOOKING}" target="_blank" rel="noopener">vrijblijvend plaatsbezoek</a> denken we graag met u mee en bekijken we samen de mogelijkheden.'),
                 soft=True, aside=pg.img("1_kleurbepaling_linkedin.webp", "Kleuradvies met kleurstalen"))],
            "Inspiratie uit onze realisaties",
            ["1627_hectaar_4_0.webp", "1627_vichte_kijkapp_9.webp", "1627_ruiselede_mooi_3.webp", "1627_particulier_fb_8.webp",
             "1627_binnenschilderwerken_sdad_3.webp", "1627_zwijn_2na.webp", "1627_dsc_1462.webp", "1627_nieuwpoort_living.webp"],
            "Veelgestelde vragen over binnenschilderwerken", [
                ("Voeren jullie ook plamuurwerken uit?", "Ja. Een mooi schilderresultaat begint bij een goede ondergrond. Daarom verzorgen wij indien nodig ook plamuurwerken om muren en plafonds strak, egaal en schilderklaar af te werken."),
                ("Werken jullie ook met vliesbehang?", "Ja. Vliesbehang en renovatievlies vormen vaak de ideale basis voor nieuwbouw- en renovatieprojecten. Ze zorgen voor een strakke afwerking en helpen kleine oneffenheden in de ondergrond op te vangen. We adviseren u graag welke oplossing het best aansluit bij uw woning en wensen."),
                ("Geven jullie ook kleuradvies?", "Ja. Een geslaagd interieur begint met de juiste keuzes. Daarom begeleiden we klanten die met ons samenwerken graag bij de keuze van kleuren, materialen en afwerkingen, zodat alles perfect op elkaar afgestemd is."),
                ("Schilderen jullie ook deuren, ramen en binnenschrijnwerk?", "Absoluut. Naast muren en plafonds verzorgen we ook het schilderen van deuren, kozijnen, trappen en ander binnenschrijnwerk. Zo creëren we een mooi en harmonieus geheel doorheen uw interieur."),
                ("Moeten mijn muren eerst geëgaliseerd worden?", "Niet altijd. Tijdens het plaatsbezoek beoordelen we de staat van de ondergrond. Indien nodig voeren we plamuur-, schuur- en egalisatiewerken uit zodat de uiteindelijke schilderafwerking perfect tot haar recht komt."),
                ("Werken jullie zowel voor renovaties, nieuwbouw als bestaande woningen?", "Ja. Of het nu gaat om een nieuwbouwwoning, renovatieproject of bestaande woning: wij zorgen steeds voor een professionele voorbereiding, een vlotte uitvoering en een hoogwaardige afwerking."),
                ("Hoe lang duren binnenschilderwerken?", "Dat hangt af van de omvang van het project en de nodige voorbereidingswerken. Na het plaatsbezoek ontvangt u een duidelijke offerte en planning, zodat u precies weet wat u mag verwachten."),
                ("Werken jullie ook voor bedrijven?", "Ja. We voeren binnenschilderwerken uit voor particulieren, kantoren, handelszaken, praktijken, horeca en residentiële projecten. Daarbij hanteren we steeds dezelfde focus op kwaliteit, planning, communicatie en afwerking."),
            ], gal_link="realisaties/")


def buiten():
    service("diensten/schilderwerken/buiten/", "Buitenschilderwerken Izegem | SDAD",
            "Schilderwerken SDAD uit Izegem heeft een getraind oog en ziet wat uw project nodig heeft. Gevel laten schilderen of uw buitenmuren afwerken? Dat kan!",
            ("Schilderwerken", "Buitenschilderwerken"), "Professionele buitenschilderwerken",
            p("Uw gevel, buitenschrijnwerk of gevelbekleding bepalen mee de eerste indruk van uw woning of bedrijfspand. Een professionele afwerking zorgt niet alleen voor een verzorgde uitstraling, maar beschermt ook jarenlang tegen weer, wind en vervuiling.",
              "Bij SDAD combineren we technisch advies, kwaliteitsproducten en vakmanschap tot een duurzaam eindresultaat waarop u jarenlang kunt vertrouwen.") +
            '<p class="hero-badge"><strong>10 jaar garantie</strong> op gevelschilderwerk <a href="#garantie">Voorwaarden</a></p>',
            "1345_gevel_kortrijk.webp",
            [lambda pg: f"""<section class="section"><div class="wrap grid grid--2" style="align-items:start">
  <div><span class="eyebrow">Gevelbescherming</span><h2>Duurzame bescherming voor uw gevel</h2>
  {p("Een buitenschilderproject draait niet alleen om kleur. De keuze van het juiste verfsysteem, de staat van de ondergrond en een grondige voorbereiding bepalen mee hoe lang het resultaat mooi blijft.",
     "Daarom bekijken we vooraf welke aanpak het meest geschikt is voor uw woning of gebouw. Of het nu gaat om schilderen, kaleien of een combinatie van technieken: we adviseren u graag naar een oplossing die zowel esthetisch als technisch klopt.")}</div>
  <div><span class="eyebrow">Reiniging</span><h2>Last van mos, vervuiling of verwering?</h2>
  {p("Geen probleem! Voordat we de gevel met kleur aanpakken, zorgen we eerst dat alle vuil verwijderd is. Zo kunt u bij SDAD terecht voor onder meer de ontmossing en reiniging van gevels, blauwsteen en de dieptereiniging van aluminiumprofielen.",
     "Na de reiniging volgt uiteraard de afwerking. We schilderen de gevel met een primerlaag gevolgd door de nodige afwerkingslagen. Liever kaleien? Ook daarvoor bent u bij SDAD aan het juiste adres. We werken zowel met minerale kalei als met decoratieve kwartstechnieken, afhankelijk van de gewenste uitstraling.",
     "Voor elk buitenproject geeft SDAD steeds voorafgaand technisch advies over het meest geschikte verfsysteem en de ondergrond.")}</div>
</div></section>""",
             garantie_block,
             lambda pg: text_section("Ramen en deuren", "Schilderen of oliën van buitenschrijnwerk", p(
                 "Een gevel nieuw leven in blazen zonder het schrijnwerk van de ramen en deuren af te werken? Dat lijkt natuurlijk nergens naar en komt slordig over. SDAD zorgt er dan ook voor dat het gebouw helemaal piekfijn in orde wordt gebracht door het buitenschrijnwerk ook te schilderen of te oliën."),
                 soft=True, aside=pg.img("1636_ramen_deerlijk.webp", "Geschilderd buitenschrijnwerk in Deerlijk")),
             lambda pg: text_section("Totaalplaatje", "Zorg dat het plaatje klopt", p(
                 f'Een verzorgde gevel verdient een interieur dat diezelfde uitstraling doortrekt. Daarom kunt u bij SDAD niet alleen terecht voor buitenschilderwerken, maar ook voor <a href="{pg.u("diensten/schilderwerken/binnen/")}">binnenschilderwerken</a> en <a href="{pg.u("diensten/schilderwerken/decoratieve-technieken/")}">decoratieve technieken</a>.',
                 "Zo zorgen we ervoor dat alles mooi op elkaar afgestemd is en het totaalplaatje klopt."))],
            "Inspiratie uit onze realisaties",
            ["1636_juli_2012_008_0.webp", "1636_odigo.webp", "1636_gevel_roeselare.webp", "1636_gevel_izegem.webp",
             "1636_gevel_kortrijk_2.webp", "1636_gevel_zwevegem.webp", "1636_gevel_deinze.webp", "1636_ramen_deerlijk.webp"],
            "Veelgestelde vragen over buitenschilderwerken", [
                ("Wanneer is de beste periode om buitenschilderwerken uit te voeren?", "Buitenschilderwerken worden meestal uitgevoerd tussen het voorjaar en het najaar. De ideale omstandigheden hangen af van temperatuur, luchtvochtigheid en weersomstandigheden. Daarom bekijken we per project wat het meest geschikte moment is."),
                ("Wat is het verschil tussen schilderen en kaleien?", p(
                    "<strong>Bij schilderen</strong> wordt de bestaande structuur van de gevel behouden. Een verfsysteem beschermt de ondergrond en geeft de gevel een nieuwe kleur en frisse uitstraling, zonder het karakter van de steen of het oppervlak te wijzigen.",
                    "<strong>Bij kaleien</strong> wordt er een minerale kalklaag aangebracht die de gevel een volledig andere uitstraling geeft. De ondergrond krijgt een meer natuurlijke, authentieke en landelijke look. Kalei zorgt voor meer diepte en karakter dan een klassieke schilderafwerking.",
                    "Welke techniek het meest geschikt is, hangt af van de uitstraling die u wenst, de staat van de gevel en de technische eigenschappen van de ondergrond. Tijdens een plaatsbezoek adviseren wij u graag over de beste oplossing voor uw woning.")),
                ("Hoe lang gaat het buitenschilderwerk van een gevel mee?", p(
                    "De levensduur van een buitenschilderwerk hangt af van verschillende factoren, zoals de staat van de ondergrond, de ligging van het gebouw, de weersbelasting en het gekozen verfsysteem.",
                    "Bij SDAD besteden we daarom veel aandacht aan een correcte voorbereiding van de ondergrond, technisch advies en het gebruik van hoogwaardige kwaliteitsproducten.",
                    "<strong>Voor gevelschilderwerken</strong> kunnen wij, mits een geschikte ondergrond en een correct opgebouwd verfsysteem, opleveren met <strong>10 jaar garantie</strong>.",
                    "<strong>Voor schilderwerken aan buitenschrijnwerk</strong> gelden andere omstandigheden. Houten ramen en deuren worden immers veel intensiever belast door zon, regen, temperatuurschommelingen en mechanische belasting. Daarom is de levensduur hiervan afhankelijk van verschillende factoren en kunnen deze werken niet met dezelfde garantievoorwaarden worden opgeleverd als gevelschilderwerken.")),
                ("Moet een gevel eerst gereinigd worden?", p(
                    "Ja. Een duurzame afwerking begint altijd met een correcte voorbereiding van de ondergrond.",
                    "Mos, algen, straatvuil en andere vervuiling worden eerst verwijderd zodat verf of kalei optimaal kan hechten. Zonder een grondig gereinigde ondergrond kan geen duurzaam verfsysteem worden opgebouwd.",
                    "Daarom bekijken we bij elk project vooraf welke reiniging en voorbereiding nodig zijn om een kwalitatief eindresultaat te garanderen.")),
                ("Schilderen jullie ook ramen en deuren?", p(
                    "Absoluut. Naast gevels verzorgen we ook het schilderen of oliën van houten buitenschrijnwerk zoals ramen, deuren, dakoversteken en andere houten elementen.",
                    "Ook PVC- en aluminiumschrijnwerk kunnen wij voorzien van een duurzame schilderafwerking, mits de ondergrond hiervoor geschikt is.")),
                ("Werken jullie ook op hoogte?", "Ja. Afhankelijk van het project werken we met ladders, rolstellingen, hoogtewerkers of vaste stellingen om een veilige en kwalitatieve uitvoering te garanderen."),
                ("Geven jullie advies over kleuren en afwerking?", "Absoluut. We begeleiden klanten niet alleen bij de uitvoering, maar ook bij de keuze van kleuren, materialen en afwerking zodat het eindresultaat perfect aansluit bij de woning en omgeving."),
                ("Kan ik een vrijblijvende offerte aanvragen?", "Ja. Tijdens een plaatsbezoek bekijken we de situatie ter plaatse en ontvangt u een duidelijke en vrijblijvende offerte op maat van uw project."),
            ], gal_link="realisaties/")


def decoratief():
    techs = [
        ("LIMESTONE", "Rust, diepte en natuurlijke charme", "2452_limestone_new_brushtop_7_bosspaints-1.webp",
         ["Limestone is een kalktechniek die zorgt voor zachte kleurnuances en natuurlijke bewegingen. De afwerking creëert warmte, diepte en een tijdloze elegantie.",
          "Perfect voor wie houdt van een rustig, natuurlijk interieur met een exclusieve uitstraling."]),
        ("CALCO", "Authentieke kalklook met zachte kleurschakeringen", "2454_calco_original_5_bosspaints.webp",
         ["Calco is een decoratieve kalktechniek die zorgt voor een warme en levendige uitstraling. De subtiele kleurnuances en natuurlijke effecten geven elke wand een eigen uitstraling. Afhankelijk van de gekozen uitvoering kan de afwerking strak en tijdloos ogen of net een meer verweerde, authentieke uitstraling krijgen.",
          "Perfect voor wie op zoek is naar sfeer, warmte en een interieur met een natuurlijke uitstraling."]),
        ("AQUA SENSA", "Naadloze uitstraling met moderne elegantie", "2456_techniek_11.webp",
         ["Aqua Sensa combineert de uitstraling van beton of natuursteen met het comfort van een naadloze afwerking. Dankzij de sterke en onderhoudsvriendelijke eigenschappen is deze techniek geschikt voor zowel woonruimtes als commerciële toepassingen. Ook in badkamers, keukens en andere intensief gebruikte ruimtes komt deze afwerking perfect tot haar recht.",
          "De afwerking zorgt voor een strak en tijdloos resultaat waarbij rust, eenvoud en duurzaamheid centraal staan.",
          "Perfect voor wie houdt van een moderne uitstraling met een minimum aan voegen en een maximum aan beleving."]),
        ("STONE ART", "De uitstraling van steen, de kracht van structuur", "2458_techniek_21.webp",
         ["Stone Art creëert een authentieke steenlook met extra diepte en reliëf. De decoratieve afwerking combineert een natuurlijke uitstraling met een robuust karakter en vormt zo een echte blikvanger binnen elk interieur.",
          "Dankzij de hoge kras- en stootvastheid is Stone Art niet alleen esthetisch sterk, maar ook bijzonder duurzaam in gebruik.",
          "Perfect voor wie op zoek is naar een uitgesproken accentmuur met een unieke uitstraling en een voelbare structuur."]),
    ]

    def offer(pg):
        blocks = "".join(f"""<div class="technique split{' split--rev' if i % 2 else ''}">
  <div>{pg.img(img, f"Decoratieve techniek {n.title()}")}</div>
  <div><h3>{n}</h3><p class="sub">{sub}</p>{p(*txt)}</div>
</div>""" for i, (n, sub, img, txt) in enumerate(techs))
        return f"""<section class="section"><div class="wrap">
  <div class="narrow"><span class="eyebrow">Ons aanbod</span><h2>Inspiratie uit ons aanbod</h2>
  {p("Elke decoratieve afwerking heeft haar eigen uitstraling, structuur en toepassing. De mogelijkheden zijn bijzonder veelzijdig. Hieronder ontdekt u alvast enkele afwerkingen uit ons aanbod. Tijdens een vrijblijvend plaatsbezoek bekijken we samen welke techniek het best aansluit bij uw interieur, wensen en de functie van de ruimte.",
     "Voor het realiseren van deze technieken werken we uitsluitend met kwaliteitsproducten van Boss Paints. Zo bent u verzekerd van duurzame afwerkingen, hoogwaardige materialen en een professioneel eindresultaat.")}</div>
  {blocks}
</div></section>"""

    more = text_section("Meer mogelijkheden", "Nog meer inspiratie", p(
        "Niet alle mogelijke technieken staan hierboven vermeld. Het aanbod aan decoratieve afwerkingen, structuren en effecten is bijzonder uitgebreid.",
        f'Tijdens een <a href="{BOOKING}" target="_blank" rel="noopener">vrijblijvend plaatsbezoek</a> bekijken we graag welke decoratieve afwerking het best aansluit bij uw interieur, stijl en wensen.',
        "Hieronder vindt u alvast enkele sfeerbeelden die tonen hoe decoratieve afwerkingen een interieur extra karakter kunnen geven."), soft=True)
    service("diensten/schilderwerken/decoratieve-technieken/", "Decoratieve technieken | kalkverf en betonlook | SDAD Izegem",
            "Limestone, Calco, Aqua Sensa en Stone Art. SDAD uit Izegem geeft uw interieur karakter met decoratieve afwerkingen op maat.",
            ("Schilderwerken", "Decoratieve technieken"), "Geef uw interieur karakter met decoratieve afwerkingen",
            p("Decoratieve afwerkingen geven een ruimte een unieke uitstraling. Ze zorgen voor sfeer, diepte, structuur en karakter.",
              "Of u nu kiest voor een subtiele kalkafwerking, een strakke betonlook of een uitgesproken accentmuur: samen bekijken we welke techniek het best aansluit bij uw woning, zaak of project.",
              "Zo ontstaat een interieur dat niet alleen mooi oogt, maar ook jarenlang blijft overtuigen.") +
            '<ul class="tags"><li>Limestone</li><li>Calco</li><li>Aqua Sensa</li><li>Stone Art</li></ul>',
            "2442_techniek_12.webp", [offer, more], "Sfeerbeelden",
            ["2502_aqua_sensa_1.webp", "2502_b_b_blauwhuis_2.webp", "2502_lijo.webp", "2502_limestone_1.webp",
             "2502_stucco_puro_1.webp", "2502_techniek_7.webp", "2502_techniek_9.webp", "2502_tusk_1.webp"],
            "Veelgestelde vragen over decoratieve technieken", [
                ("Zijn decoratieve technieken geschikt voor elke ruimte?", "Ja. Afhankelijk van de gekozen techniek kunnen decoratieve afwerkingen toegepast worden in leefruimtes, slaapkamers, keukens, badkamers, kantoren en commerciële ruimtes. Samen bekijken we welke oplossing het best past bij de functie van de ruimte."),
                ("Wat is het verschil tussen een decoratieve techniek en gewone schilderwerken?", "Decoratieve technieken creëren extra diepte, structuur en beleving. Waar klassieke schilderwerken vooral kleur brengen, zorgen decoratieve afwerkingen voor een unieke uitstraling met meer karakter en persoonlijkheid."),
                ("Zijn decoratieve afwerkingen onderhoudsvriendelijk?", "Ja. De meeste decoratieve technieken zijn eenvoudig te onderhouden. Afhankelijk van de gekozen afwerking kunnen bijkomende beschermlagen voorzien worden voor extra duurzaamheid en gebruiksgemak."),
                ("Kunnen decoratieve technieken ook in badkamers of keukens toegepast worden?", "Zeker. Technieken zoals Aqua Sensa zijn speciaal ontwikkeld voor ruimtes die intensief gebruikt worden en bieden een duurzame en onderhoudsvriendelijke oplossing."),
                ("Is elke decoratieve afwerking uniek?", "Ja. Decoratieve technieken worden manueel aangebracht waardoor subtiele nuances, kleurschakeringen en structuren ontstaan. Dat maakt elke wand uniek."),
                ("Hoe kiezen we de juiste techniek?", f'Tijdens een <a href="{BOOKING}" target="_blank" rel="noopener">vrijblijvend plaatsbezoek</a> luisteren we naar uw wensen en bekijken we samen de ruimte, de gewenste uitstraling en het beschikbare budget. Op basis daarvan adviseren we welke techniek het best aansluit bij uw project.'),
                ("Zijn decoratieve technieken duurder dan klassieke schilderwerken?", f'Dat hangt af van de gekozen techniek en de oppervlakte. Decoratieve afwerkingen vragen meer vakmanschap en worden vaak in meerdere lagen opgebouwd. Tijdens <a href="{BOOKING}" target="_blank" rel="noopener">het plaatsbezoek</a> ontvangt u steeds een duidelijke offerte op maat.'),
            ])


def gordijnen():
    service("diensten/interieurafwerking/gordijnen/", "Gordijnen op maat | gordijnen Izegem | SDAD",
            "Voor alle gordijnen op maat bent u bij schilderwerken SDAD uit Izegem aan het goede adres.",
            ("Interieurafwerking", "Gordijnen"), "Gordijnen op maat voor sfeer, privacy en comfort",
            '<ul class="tags"><li>Overgordijnen</li><li>Rolgordijnen</li><li>Vouwgordijnen</li><li>Elektrisch of manueel te bedienen</li></ul>',
            "1351_modelapp_3.webp",
            [text_section("Advies, opmeting en plaatsing", "De afwerking die uw interieur compleet maakt", p(
                "Gordijnen doen veel meer dan enkel een raam aankleden. Ze zorgen voor sfeer, privacy, een betere akoestiek en brengen rust in uw interieur.",
                "Daarom begeleiden we u bij SDAD graag bij de keuze van de juiste stof, kleur, afwerking en bediening. Samen bekijken we welke oplossing het best aansluit bij uw woning, interieur en wensen.",
                "Of u nu kiest voor elegante overgordijnen, praktische rolgordijnen of stijlvolle vouwgordijnen: alles wordt nauwkeurig opgemeten en volledig op maat uitgewerkt.",
                "Van advies en opmeting tot plaatsing zorgen wij voor een vlotte opvolging en een perfect afgewerkt eindresultaat."))],
            "Sfeerbeelden",
            ["1644_0166.webp", "1644_cambr_diaz_3_-_kopie_0.webp", "1644_app_kortrijk_4.webp", "1644_sleepend_gordijn.webp",
             "1644_paneelgordijnen.webp", "1644_rolgordijnen_2.webp", "1644_rolgordijnen.webp", "1644_gordijn_2.webp"],
            "Veelgestelde vragen over gordijnen", [
                ("Geven jullie advies over stoffen en kleuren?", "Ja. Tijdens een plaatsbezoek bekijken we samen welke stoffen, kleuren en afwerkingen het best aansluiten bij uw interieur, lichtinval en wensen."),
                ("Komen jullie zelf opmeten?", "Ja. Wij zorgen voor een professionele opmeting zodat uw gordijnen perfect aansluiten op de ruimte en de ramen."),
                ("Zijn elektrische gordijnen mogelijk?", "Ja. Afhankelijk van het gekozen systeem kunnen gordijnen manueel of elektrisch bediend worden. We adviseren u graag over de mogelijkheden die het best aansluiten bij uw woning en gebruiksgemak."),
                ("Plaatsen jullie de gordijnen ook?", "Ja. Naast advies en opmeting verzorgen wij ook de professionele plaatsing van uw gordijnen."),
                ("Kunnen gordijnen gecombineerd worden met lamellen of andere raamdecoratie?", 'Ja. Afhankelijk van de ruimte en de gewenste uitstraling kunnen gordijnen perfect gecombineerd worden met bijvoorbeeld <a href="../lamellen/">lamellen</a> of andere vormen van raamdecoratie.'),
            ])


def lamellen():
    service("diensten/interieurafwerking/lamellen/", "Lamellen op maat | Lamellen Izegem | SDAD",
            "Houten, aluminium, pvc of textiel lamellen op maat. SDAD uit Izegem adviseert, meet op en plaatst. Vraag uw vrijblijvend plaatsbezoek aan.",
            ("Interieurafwerking", "Lamellen"), "Lamellen op maat voor licht, privacy en uitstraling",
            '<div class="tag-group"><h3>Materialen</h3><ul class="tags"><li>Houten lamellen</li><li>Aluminium lamellen</li><li>Pvc lamellen</li><li>Textiel lamellen</li></ul>'
            '<h3>Uitvoeringen</h3><ul class="tags"><li>Horizontale lamellen</li><li>Verticale lamellen</li><li>Elektrisch of manueel bedienbaar</li></ul></div>',
            "1354_modelapp_4.webp",
            [lambda pg: text_section("Advies op maat", "Functioneel, stijlvol en volledig op maat", p(
                "Lamellen combineren een strakke uitstraling met een grote flexibiliteit in lichtinval en privacy. Door de lamellen te kantelen bepaalt u zelf hoeveel licht binnenkomt en hoeveel inkijk u wenst.",
                "Ook voor omvangrijke projecten zoals de inrichting van een hotel of een bedrijvencentrum kunt u bij ons terecht. Onze experts komen bij u langs om u professioneel advies te geven over de mogelijkheden en het esthetische aspect.",
                "Lamellen zijn verkrijgbaar in heel wat materialen. Kies voor hout, pvc, textiel of aluminium. Houd er wel rekening mee dat stoffen lamellen minder licht tegenhouden dan pvc lamellen. Met verticale lamellen kunt u dan weer snel schakelen tussen privacy en openheid door ze dicht te doen of opzij te schuiven. Of speel met de lichtinval voor een leuk effect.",
                "Over elk model of elk materiaal valt er wat te zeggen. Alles hangt af van de ruimte waar u lamellen wenst en wat uw voorkeuren zijn. Zeker voor hogere raampartijen zijn lamellen bijzonder geschikt.",
                f'SDAD komt graag bij u langs om de ruimte te bekijken en de juiste lamellen op maat op te voorzien. Neem vrijblijvend <a href="{pg.u("contact/")}">contact</a> met ons op voor professioneel advies of een vrijblijvende offerte.',
                f'Op zoek naar een zachtere uitstraling? Ontdek ook onze <a href="{pg.u("diensten/interieurafwerking/gordijnen/")}">gordijnen</a> op maat, van elegante overgordijnen tot praktische rol- en vouwgordijnen.'))],
            "Sfeerbeelden",
            ["1647_0085.webp", "1647_0105.webp", "1647_lamel_combo_gordijn.webp", "1647_vb_tr_014_diaz_2_-_kopie_1_0.webp",
             "1647_houten_lamellen.webp", "1647_lamel_combo_gordijn_3.webp", "1647_lamel_combo_gordijn_2.webp", "1647_lamel_4.webp"],
            "Veelgestelde vragen over lamellen", [
                ("Welke lamellen passen het best bij mijn interieur?", "Dat hangt af van de ruimte, de gewenste uitstraling en de functie van de raamdecoratie. Houten lamellen zorgen voor een warme en natuurlijke uitstraling, terwijl aluminium of pvc lamellen eerder strak en modern ogen. Tijdens een plaatsbezoek adviseren we u graag over de mogelijkheden."),
                ("Komen jullie zelf opmeten?", "Ja. Een correcte opmeting is essentieel voor een mooi eindresultaat. Daarom komen we steeds ter plaatse om de situatie te bekijken en de lamellen nauwkeurig op te meten."),
                ("Kunnen lamellen elektrisch bediend worden?", "Ja. Afhankelijk van het gekozen systeem kunnen lamellen zowel manueel als elektrisch bediend worden. We bekijken graag welke oplossing het best aansluit bij uw woning, comfortwensen en gebruiksgemak."),
                ("Zijn lamellen geschikt voor grote raampartijen of schuiframen?", "Absoluut. Lamellen zijn bijzonder geschikt voor grote ramen en hoge glaspartijen. Ze bieden een strakke uitstraling en laten toe om de lichtinval eenvoudig te regelen zonder het zicht volledig weg te nemen."),
                ("Wat is het verschil tussen horizontale en verticale lamellen?", "Horizontale lamellen worden vaak toegepast bij ramen in woningen en zorgen voor een strakke, tijdloze uitstraling. Verticale lamellen zijn bijzonder geschikt voor grote glaspartijen en schuiframen en bieden veel flexibiliteit in lichtregeling en privacy."),
                ("Kunnen lamellen gecombineerd worden met gordijnen?", 'Ja. Lamellen kunnen perfect gecombineerd worden met <a href="../gordijnen/">gordijnen</a> voor een warmere uitstraling en extra sfeer. Zo combineert u het praktische karakter van lamellen met de zachtheid en gezelligheid van gordijnen.'),
                ("Geven jullie ook advies over kleuren en materialen?", "Ja. Tijdens een plaatsbezoek bekijken we samen welke kleuren, materialen en afwerkingen het best aansluiten bij uw interieur, lichtinval en persoonlijke smaak. Zo bent u zeker van een oplossing die niet alleen mooi oogt, maar ook perfect past bij uw woning en manier van leven."),
            ])


# ---------- Realisaties ----------
def realisaties():
    pg = Page("realisaties/")
    labels = LABELS
    present = [k for k in labels if any(k in r["cats"] for r in REAL)]
    btns = '<button type="button" data-filter="alle" aria-pressed="true">Alle realisaties</button>' + "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="false">{labels[k]}</button>' for k in present)

    def group(typ, anchor, title, other_anchor, other_label):
        cards = "".join(
            f'<div data-cats="{" ".join(r["cats"])}">' + card(pg, pg.u(f"realisaties/{r['slug']}/"), r["img"], r["title"], more="Bekijk realisatie",
                                                             meta=" · ".join(LABELS[c] for c in r["cats"])) + "</div>"
            for r in REAL if r["type"] == typ)
        return f"""<div data-group id="{anchor}" style="scroll-margin-top:100px;margin-bottom:64px">
  <div class="head-row"><h2>{title}</h2><a class="arrow-link" href="#{other_anchor}">{other_label}</a></div>
  <div class="grid grid--3">{cards}</div><p class="empty">Geen realisaties in deze categorie.</p>
</div>"""

    body = page_hero(pg, [("Realisaties", None)], "Portfolio", "Een selectie van onze realisaties",
                     '<p class="lead">Laat u inspireren door de vele realisaties, zowel particulier als op projectbasis, die SDAD reeds tot een goed einde bracht.</p>') + f"""
<section class="section"><div class="wrap">
  <div class="filter" role="group" aria-label="Filter op dienst">{btns}</div>
  {group("particulier", "particulieren", "Particuliere realisaties", "projecten", "Bekijk realisaties op projectbasis")}
  {group("project", "projecten", "Gerealiseerde projecten", "particulieren", "Bekijk particuliere realisaties")}
</div></section>
{cta(pg)}"""
    write(pg, layout(pg, "Realisaties schilderwerken SDAD Izegem",
                     "Laat u inspireren door de vele realisaties, zowel particulier als op projectbasis, die schilderwerken SDAD reeds tot een goed einde bracht.", body))


# ---------- Blog ----------
def blog():
    pg = Page("blog/")
    cards = "".join(card(pg, pg.u(f"blog/{b['slug']}/"), b["img"], b["title"], short(b["excerpt"])) for b in BLOG)
    socials = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL.items())
    body = page_hero(pg, [("Blog", None)], "Tips &amp; advies", "Blogberichten",
                     f'<p class="lead">Met meer dan 25 jaar ervaring in ons vak delen we onze opgebouwde expertise graag met u.</p><p>Volg ons: {socials}</p>') + f"""
<section class="section"><div class="wrap"><div class="grid grid--3">{cards}</div></div></section>
{cta(pg)}"""
    write(pg, layout(pg, "Blog over schilderwerken en afwerking | SDAD Izegem",
                     "Met meer dan 25 jaar ervaring in hun vak wil schilderwerken SDAD hun opgebouwde expertise graag met u delen in hun blogs.", body))


# ---------- Contact ----------
def contact():
    pg = Page("contact/")
    people = "".join(f'<div class="contact-card"><h3>{n}</h3><p><a href="tel:{t}">{d}</a></p></div>' for n, d, t in PHONES)
    body = page_hero(pg, [("Contact", None)], "Contact", "Contacteer ons",
                     '<p class="lead">Schilderwerken, gordijnen of lamellen in het vooruitzicht? Neem contact op. Wij helpen u graag verder en reageren snel op uw vraag. We werken in heel Oost- en West-Vlaanderen.</p>') + f"""
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="contact-cards">
    <div class="contact-card"><h3>SDAD bv</h3><p>Prinsdomlaan 50<br>8870 Izegem<br>BE0823.935.816</p><p style="margin-top:10px"><a href="{MAPS}" target="_blank" rel="noopener" style="font-size:1rem">Route plannen →</a></p></div>
    {people}
    <div class="contact-card"><h3>E-mail</h3><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div class="contact-card" style="background:var(--ink);border-color:var(--ink);color:#c9cbcd"><h3 style="color:#fff">Liever meteen een afspraak?</h3><p style="margin-bottom:14px">Plan zelf een vrijblijvend plaatsbezoek in.</p><a class="btn" href="{BOOKING}" target="_blank" rel="noopener" style="font-size:1rem;color:#fff">Plaatsbezoek inplannen</a></div>
  </div>
  <form class="form" id="contact-form">
    <h2 style="font-size:2rem">Stel ons een vraag</h2>
    <div class="form-grid">
      <div><label for="f-vn">Naam *</label><input id="f-vn" name="voornaam" required autocomplete="given-name"></div>
      <div><label for="f-n">Familienaam *</label><input id="f-n" name="naam" required autocomplete="family-name"></div>
      <div class="full"><label for="f-a">Straat + huisnr. *</label><input id="f-a" name="adres" required autocomplete="street-address"></div>
      <div><label for="f-pc">Postcode *</label><input id="f-pc" name="postcode" required autocomplete="postal-code" inputmode="numeric"></div>
      <div><label for="f-s">Stad *</label><input id="f-s" name="stad" required autocomplete="address-level2"></div>
      <div><label for="f-t">Telefoon *</label><input id="f-t" name="telefoon" type="tel" required autocomplete="tel"></div>
      <div><label for="f-e">E-mail *</label><input id="f-e" name="email" type="email" required autocomplete="email"></div>
      <div class="hp" aria-hidden="true"><label for="f-w">Website</label><input id="f-w" name="website" tabindex="-1" autocomplete="off"></div>
      <div class="full"><label for="f-m">Hoe kunnen we je helpen? *</label><textarea id="f-m" name="bericht" rows="5" required></textarea></div>
      <div class="full"><label class="check"><input type="checkbox" name="privacy" required> <span>Ik ga akkoord met het <a href="{pg.u('cookie-en-privacybeleid/')}" target="_blank">Cookie- en privacybeleid</a></span></label></div>
    </div>
    <button class="btn" type="submit" style="margin-top:20px">Verstuur bericht</button>
    <p class="form-note" aria-live="polite">We reageren snel op uw vraag.</p>
  </form>
</div></section>
{cta(pg)}"""
    write(pg, layout(pg, "Contacteer ons voor schilderwerken, gordijnen of lamellen",
                     "Schilderwerken in het vooruitzicht? Neem contact op met schilderwerken SDAD uit Izegem, West-Vlaanderen. Wij helpen u graag verder!", body))


# ---------- Detailpagina's (realisaties en blog) ----------
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


def detail_sections(pg, secs, alt):
    out = ""
    soft = False
    for s in secs:
        title, rest = split_heading(fix_links(pg, s["html"]))
        imgs = s["imgs"]
        if len(imgs) > 1:
            out += gallery(pg, title or "Sfeerbeelden", imgs, alt_base=alt) if not rest.strip() else \
                f'<section class="section"><div class="wrap"><div class="narrow">{f"<h2>{title}</h2>" if title else ""}{rest}</div></div></section>' + gallery(pg, "Sfeerbeelden", imgs, alt_base=alt)
            soft = False
            continue
        if not title and not rest.strip() and not imgs:
            continue
        soft = not soft
        head = f"<h2>{title}</h2>" if title else ""
        if imgs:
            inner = f'<div class="split"><div>{head}{rest}</div><div>{pg.img(imgs[0], title or alt)}</div></div>'
        else:
            inner = f'<div class="narrow prose">{head}{rest}</div>'
        out += f'<section class="section{" section--soft" if soft else ""}"><div class="wrap">{inner}</div></section>'
    return out


def realisatie_pages():
    for i, r in enumerate(REAL):
        pg = Page(f"realisaties/{r['slug']}/")
        d = DETAILS["realisaties"][r["slug"]]
        first, rest = d["sections"][0], d["sections"][1:]
        hero_img = first["imgs"][0] if first["imgs"] else r["img"]
        meta = ("Particulier" if r["type"] == "particulier" else "Project") + "".join(f" · {LABELS[c]}" for c in r["cats"])
        others = [o for o in REAL if o is not r and (set(o["cats"]) & set(r["cats"]) or not r["cats"])][:3] or [o for o in REAL if o is not r][:3]
        more = "".join(card(pg, pg.u(f"realisaties/{o['slug']}/"), o["img"], o["title"], more="Bekijk realisatie") for o in others)
        body = page_hero(pg, [("Realisaties", "realisaties/"), (escape(r["title"]), None)], meta, escape(r["title"]),
                         fix_links(pg, first["html"]), hero_img, r["title"])
        body += detail_sections(pg, rest, r["title"])
        body += f"""<section class="section section--soft"><div class="wrap">
  <div class="head-row"><div><span class="eyebrow">Portfolio</span><h2>Meer realisaties</h2></div><a class="arrow-link" href="{pg.u('realisaties/')}">Alle realisaties</a></div>
  <div class="grid grid--3">{more}</div>
</div></section>{cta(pg)}"""
        desc = d["desc"] or short(re.sub("<[^>]+>", " ", first["html"]).strip(), 150)
        write(pg, layout(pg, f"{r['title']} | Realisaties SDAD", re.sub(r"\s+", " ", desc), body))


def blog_pages():
    for i, b in enumerate(BLOG):
        pg = Page(f"blog/{b['slug']}/")
        d = DETAILS["blog"][b["slug"]]
        first, rest = d["sections"][0], d["sections"][1:]
        hero_img = first["imgs"][0] if first["imgs"] else b["img"]
        others = [BLOG[(i + k) % len(BLOG)] for k in (1, 2, 3)]
        more = "".join(card(pg, pg.u(f"blog/{o['slug']}/"), o["img"], o["title"], short(o["excerpt"], 120)) for o in others)
        body = page_hero(pg, [("Blog", "blog/"), (escape(d["title"]), None)], "Tips &amp; advies", escape(d["title"]),
                         fix_links(pg, first["html"]), hero_img, d["title"])
        body += detail_sections(pg, rest, d["title"])
        body += f"""<section class="section section--soft"><div class="wrap">
  <div class="head-row"><div><span class="eyebrow">Blog</span><h2>Lees ook</h2></div><a class="arrow-link" href="{pg.u('blog/')}">Alle blogberichten</a></div>
  <div class="grid grid--3">{more}</div>
</div></section>{cta(pg)}"""
        write(pg, layout(pg, f"{d['title']} | Blog SDAD", d["desc"] or b["excerpt"], body))


# ---------- Juridische pagina's ----------
def legal_pages():
    meta = {
        "cookie-en-privacybeleid": ("Cookie- en privacybeleid", "cookie-en privacybeleid SDAD",
                                    "<p class=\"lead\">BV Schilder &amp; Decoratiewerken Arne Deseure verwerkt persoonsgegevens overeenkomstig deze privacyverklaring.</p>"),
        "disclaimer": ("Disclaimer", "Disclaimer | Schilderwerken Izegem | SDAD", ""),
        "algemene-voorwaarden": ("Algemene Voorwaarden BV SDAD", "Algemene Voorwaarden BV SDAD", ""),
    }
    for slug, (h1, title, lead) in meta.items():
        pg = Page(f"{slug}/")
        body = page_hero(pg, [(h1, None)], "Juridisch", h1, lead)
        body += f'<section class="section"><div class="wrap"><article class="narrow prose legal">{fix_links(pg, LEGAL[slug]["html"])}</article></div></section>'
        write(pg, layout(pg, title, f"{h1} van SDAD bv, Prinsdomlaan 50, 8870 Izegem.", body))


if __name__ == "__main__":
    for f in (home, over, binnen, buiten, decoratief, gordijnen, lamellen, realisaties, blog, contact, realisatie_pages, blog_pages, legal_pages):
        f()
