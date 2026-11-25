"""Realisaties: overzicht met filters en de detailpagina per project."""

import re
from html import escape

from sdad.components import crumbs, cta, detail_sections, shot
from sdad.config import LABELS
from sdad.content import DETAILS, REAL
from sdad.layout import layout
from sdad.util import Page, fix_links, short, write


def realisaties():
    pg = Page("realisaties/")
    n_p = sum(r["type"] == "particulier" for r in REAL)
    n_j = len(REAL) - n_p
    present = [k for k in LABELS if any(k in r["cats"] for r in REAL)]
    items = "".join(
        shot(pg, r, f' data-type="{r["type"]}" data-cats="{" ".join(r["cats"])}" style="--i:{i % 3}"').replace(
            'class="shot"', f'class="shot rv{" big" if i % 7 == 0 else (" wide" if i % 7 == 4 else "")}"', 1
        )
        for i, r in enumerate(REAL)
    )
    seg = '<button type="button" data-type="alle" aria-pressed="true">Alle</button><button type="button" data-type="particulier" aria-pressed="false">Particulier</button><button type="button" data-type="project" aria-pressed="false">Projecten</button>'
    chips = '<button type="button" data-cat="alle" aria-pressed="true">Alle diensten</button>' + "".join(
        f'<button type="button" data-cat="{k}" aria-pressed="false">{LABELS[k]}</button>' for k in present
    )
    body = f"""<section class="lh"><div class="wrap">
  {crumbs(pg, [("Realisaties", None)])}<span class="eyebrow">Portfolio</span>
  <h1>Een selectie van onze <em class="stroke">realisaties</em></h1>
  <div class="lh__row"><p class="lead">Laat u inspireren door de vele realisaties, zowel particulier als op projectbasis, die SDAD reeds tot een goed einde bracht.</p>
  <ul class="lh__stats"><li><b>{len(REAL)}</b>realisaties</li><li><b>{n_p}</b>particulier</li><li><b>{n_j}</b>projecten</li></ul></div>
</div></section>
<div class="fbar"><div class="wrap"><div class="seg" role="group" aria-label="Type">{seg}</div><div class="fchips" role="group" aria-label="Dienst">{chips}</div><span class="fcount" aria-live="polite">{len(REAL)} realisaties</span></div></div>
<section class="section" style="padding-top:28px"><div class="wrap">
  <h2 class="sr-only">Alle realisaties</h2><div class="mosaic">{items}</div><p class="empty">Geen realisaties voor deze combinatie.</p>
</div></section>
{cta(pg)}"""
    write(
        pg,
        layout(
            pg,
            "Realisaties schilderwerken SDAD Izegem",
            "Laat u inspireren door de vele realisaties, zowel particulier als op projectbasis, die schilderwerken SDAD reeds tot een goed einde bracht.",
            body,
        ),
    )


def realisatie_pages():
    for i, r in enumerate(REAL):
        pg = Page(f"realisaties/{r['slug']}/")
        d = DETAILS["realisaties"][r["slug"]]
        first, rest = d["sections"][0], d["sections"][1:]
        hero_img = first["imgs"][0] if first["imgs"] else r["img"]
        chips = "".join(
            f'<span class="chip">{c}</span>'
            for c in ["Particulier" if r["type"] == "particulier" else "Project"] + [LABELS[c] for c in r["cats"]]
        )
        prv, nxt = REAL[i - 1], REAL[(i + 1) % len(REAL)]
        others = [o for o in REAL if o is not r and (set(o["cats"]) & set(r["cats"]) or not r["cats"])][:8] or [
            o for o in REAL if o is not r
        ][:8]
        body = f"""<section class="ih">
  <div class="ih__img">{pg.img(hero_img, r["title"], lazy=False).replace("<img", '<img fetchpriority="high"')}</div>
  <div class="wrap ih__text">{crumbs(pg, [("Realisaties", "realisaties/"), (escape(r["title"]), None)])}<div class="ih__chips">{chips}</div><h1>{escape(r["title"])}</h1></div>
</section>
<section class="section"><div class="wrap"><div class="ed"><div class="ed__head rv"><span class="eyebrow">Het project</span><h2>Over deze realisatie</h2></div>
  <div class="ed__body prose rv" style="--i:1">{fix_links(pg, first["html"])}</div></div></div></section>
{detail_sections(pg, rest, r["title"])}
<nav class="pn" aria-label="Andere realisaties"><div class="wrap pn__grid">
  <a class="pn__item" href="{pg.u(f"realisaties/{prv['slug']}/")}">{pg.img(prv["img"], "")}<span><small>← Vorige realisatie</small>{escape(prv["title"])}</span></a>
  <a class="pn__item pn__item--next" href="{pg.u(f"realisaties/{nxt['slug']}/")}"><span><small>Volgende realisatie →</small>{escape(nxt["title"])}</span>{pg.img(nxt["img"], "")}</a>
</div></nav>
<section class="section rail-wrap"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Portfolio</span><h2>Meer realisaties</h2></div>
  <div class="rail-nav"><a class="arrow-link" href="{pg.u('realisaties/')}" style="align-self:center;margin-right:10px">Alle realisaties</a><button type="button" data-dir="-1" aria-label="Vorige">←</button><button type="button" data-dir="1" aria-label="Volgende">→</button></div></div>
</div><div><div class="rail" tabindex="0" aria-label="Meer realisaties, horizontaal scrollen">{"".join(shot(pg, o) for o in others)}</div></div></section>
{cta(pg)}"""
        desc = d["desc"] or short(re.sub("<[^>]+>", " ", first["html"]).strip(), 150)
        write(pg, layout(pg, f"{r['title']} | Realisaties SDAD", re.sub(r"\s+", " ", desc), body))
