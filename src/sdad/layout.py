"""Paginaskelet: <head>, menubalk, footer en gestructureerde gegevens (schema.org) voor elke pagina."""

import json
from functools import lru_cache
from html import escape

from sdad.config import (
    BASE,
    BOOKING,
    DEMO,
    DIENSTEN,
    LANDING_DOMAINS,
    MAIL,
    MAPS,
    MENU,
    OUT,
    PHONES,
    REGIO,
    SERVICE_GROUP,
    SERVICE_SHORT,
    SERVICES,
    SITE,
    SOCIAL,
)
from sdad.util import site_link, thumb

ICONS = {
    "Facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></svg>',
    "Instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM21.9 8c-.1-1.6-.4-3-1.6-4.2S17.6 2.2 16 2.1C14.4 2 9.6 2 8 2.1 6.4 2.2 5 2.5 3.8 3.7S2.2 6.4 2.1 8C2 9.6 2 14.4 2.1 16c.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.6.1 6.4.1 8 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.1-1.6.1-6.4 0-8zm-2 9.7a3.3 3.3 0 0 1-1.9 1.9c-1.3.5-4.4.4-5.9.4s-4.6.1-5.9-.4a3.3 3.3 0 0 1-1.9-1.9c-.5-1.3-.4-4.4-.4-5.9s-.1-4.6.4-5.9A3.3 3.3 0 0 1 6.2 4c1.3-.5 4.4-.4 5.9-.4s4.6-.1 5.9.4a3.3 3.3 0 0 1 1.9 1.9c.5 1.3.4 4.4.4 5.9s.1 4.6-.4 5.9z"/></svg>',
    "LinkedIn": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.9 21H3.2V8.9h3.7V21zM5 7.3a2.1 2.1 0 1 1 0-4.3 2.1 2.1 0 0 1 0 4.3zM21 21h-3.7v-5.9c0-1.4 0-3.2-2-3.2s-2.2 1.5-2.2 3.1v6H9.4V8.9H13v1.7c.5-.9 1.7-1.9 3.4-1.9 3.7 0 4.4 2.4 4.4 5.6V21z"/></svg>',
}


def nav(pg):
    cur = pg.path
    dd_cur = " is-current" if cur.startswith("diensten/") else ""
    cards = "".join(
        f'<a class="mm-card" href="{pg.u(h)}"{" aria-current=page" if h == cur else ""}>'
        f'<span class="mm-img">{pg.img(thumb(i), "", w=260, h=195)}</span>'
        f'<span class="mm-txt"><small>{SERVICE_GROUP[h]}</small>{SERVICE_SHORT[h]}</span></a>'
        for h, i, t, x in SERVICES
    )
    links = "".join(f'<a class="nav-link" href="{pg.u(p)}"{" aria-current=page" if p == cur else ""}>{n}</a>' for n, p in MENU)
    return f"""<a class="skip" href="#main">Naar inhoud</a>
<div class="topbar"><div class="wrap">
  <span>Prinsdomlaan 50, 8870 Izegem</span>
  <a href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a>
  <a href="mailto:{MAIL}">{MAIL}</a>
</div></div>
<header class="header"><div class="wrap">
  <a class="logo" href="{pg.u()}" aria-label="SDAD – naar de startpagina">{pg.img("logo_dark.png", "SDAD – Schilderkracht tot de vierde macht", lazy=False, w=42, h=58)}</a>
  <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Hoofdmenu">
    <div class="dd{dd_cur}"><button aria-expanded="false">Diensten</button><div class="dd-panel">
      <p class="mm-title">Onze diensten</p><div class="mm-grid">{cards}</div></div></div>
    <div class="nav-links">{links}</div>
    <a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a>
    <div class="mm-contact"><a href="tel:{PHONES[0][2]}">Bel {PHONES[0][1]}</a><a href="mailto:{MAIL}">{MAIL}</a></div>
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


SCHEMA = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "HousePainter",
        "name": "SDAD bv",
        "slogan": "Schilderkracht tot de vierde macht",
        "url": SITE + "/",
        "email": MAIL,
        "telephone": PHONES[0][2],
        "vatID": "BE0823.935.816",
        "image": SITE + "/site/assets/files/1/kleurbepaling_linkedin.jpeg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Prinsdomlaan 50",
            "postalCode": "8870",
            "addressLocality": "Izegem",
            "addressCountry": "BE",
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "West-Vlaanderen"},
            {"@type": "AdministrativeArea", "name": "Oost-Vlaanderen"},
        ],
        "sameAs": list(SOCIAL.values()),
    },
    ensure_ascii=False,
)


@lru_cache(maxsize=None)
def asset_version():
    import hashlib

    h = hashlib.md5()
    for f in ("assets/fonts/fonts.css", "assets/css/site.css", "assets/js/main.js"):
        h.update((OUT / f).read_bytes())
    return h.hexdigest()[:8]


def layout(pg, title, desc, body, og_img="1_kleurbepaling_linkedin.webp", landing=False, body_cls=""):
    return f"""<!doctype html>
<html lang="nl-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add("js")</script>
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{LANDING_DOMAINS[pg.path] if (not DEMO and pg.path in LANDING_DOMAINS) else BASE + pg.path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{LANDING_DOMAINS[pg.path] if (not DEMO and pg.path in LANDING_DOMAINS) else BASE + pg.path}">
<meta property="og:site_name" content="SDAD">
<meta property="og:locale" content="nl_BE">
<meta property="og:image" content="{BASE}assets/img/og-sdad.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo van SDAD – Schilderkracht tot de vierde macht">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#00080a">
{'<meta name="robots" content="noindex, nofollow">' if DEMO else ""}
<link rel="icon" href="{pg.r}assets/img/list_icon.png">
<link rel="preload" href="{pg.r}assets/fonts/archivo-wdth.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pg.r}assets/fonts/fonts.css?v={asset_version()}">
<link rel="stylesheet" href="{pg.r}assets/css/site.css?v={asset_version()}">
<script type="application/ld+json">{SCHEMA}</script>
</head>
<body{f' class="{body_cls}"' if body_cls else ""}>
{landing_nav(pg) if landing else nav(pg)}
<main id="main">
{body}
</main>
{landing_footer(pg) if landing else footer(pg)}
<script src="{pg.r}assets/js/main.js?v={asset_version()}" defer></script>
</body>
</html>
"""


def landing_nav(pg):
    return f"""<a class="skip" href="#main">Naar inhoud</a>
<header class="header lp-header"><div class="wrap">
  <span class="logo">{pg.img("logo_dark.png", "SDAD – Schilderkracht tot de vierde macht", lazy=False, w=42, h=58)}</span>
  <div class="lp-actions"><a class="lp-tel" href="tel:{PHONES[0][2]}">Bel {PHONES[0][1]}</a><a class="btn no-arrow" href="#offerte">Gratis offerte</a></div>
</div></header>"""


def landing_footer(pg):
    return f"""<footer class="footer lp-footer"><div class="wrap">
  <div class="lp-foot">
    <div>{pg.img("logo.png", "SDAD", cls="footer-logo", w=66, h=92)}</div>
    <div><h4>SDAD bv</h4><p>Schilderkracht tot de vierde macht<br>Prinsdomlaan 50, 8870 Izegem<br><a href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a> · <a href="mailto:{MAIL}">{MAIL}</a></p></div>
  </div>
  <div class="subfooter"><span>© SDAD BV, BV Schilder &amp; Decoratiebedrijf Arne Deseure, BE 0823.935.816, Prinsdomlaan 50, 8870 Izegem</span>
    <a href="{site_link(pg, 'cookie-en-privacybeleid/')}">Privacybeleid</a></div>
</div></footer>
<div class="mobile-bar"><a href="tel:{PHONES[0][2]}">Bel ons</a><a href="#offerte">Gratis offerte</a></div>"""
