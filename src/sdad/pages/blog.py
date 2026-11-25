"""Blogoverzicht (met zoeken en onderwerpen) en de afzonderlijke blogartikels."""

import re
from html import escape

from sdad.components import crumbs, cta
from sdad.config import SOCIAL
from sdad.content import BLOG, DETAILS
from sdad.layout import layout
from sdad.util import Page, fix_links, short, slugify, split_heading, write

TOPICS = [
    ("binnen", "Binnen", r"muur|muren|plafond|keuken|trap|deur|badkamer|vochtig|kleur|faience|wandtegel|gyproc|mdf|interieur|binnen"),
    ("buiten", "Buiten", r"gevel|buiten|tuinhuis|kalei|aluminium|pvc|bakste"),
    ("behang", "Behang", r"behang"),
    ("techniek", "Voorbereiding en techniek", r"ontvet|verwijder|afplaktape|kit|strepen|kwaliteitsverf|lik verf|stappen"),
]


def topics_of(b):
    t = (b["title"] + " " + b["excerpt"]).lower()
    return [k for k, _, rx in TOPICS if re.search(rx, t)] or ["techniek"]


def read_min(slug):
    words = sum(len(re.sub("<[^>]+>", " ", s["html"]).split()) for s in DETAILS["blog"][slug]["sections"])
    return max(1, round(words / 200))


def blog_card(pg, b, cls="card"):
    tp = topics_of(b)
    return (
        f'<a class="{cls} rv" data-topics="{" ".join(tp)}" data-search="{escape((b["title"] + " " + b["excerpt"]).lower())}" href="{pg.u(f"blog/{b["slug"]}/")}">'
        f'<div class="card__img">{pg.img(b["img"], b["title"], w=500, h=375)}</div>'
        f'<div class="card__body"><div class="card__meta">{dict((k, n) for k, n, _ in TOPICS)[tp[0]]} · {read_min(b["slug"])} min lezen</div>'
        f'<h3>{b["title"]}</h3><p>{short(b["excerpt"], 150)}</p><span class="card__more">Lees meer</span></div></a>'
    )


def blog():
    pg = Page("blog/")
    first, rest = BLOG[0], BLOG[1:]
    socials = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL.items())
    chips = '<button type="button" data-topic="alle" aria-pressed="true">Alle</button>' + "".join(
        f'<button type="button" data-topic="{k}" aria-pressed="false">{n}</button>' for k, n, _ in TOPICS
    )
    body = f"""<section class="lh"><div class="wrap">
  {crumbs(pg, [("Blog", None)])}<span class="eyebrow">Tips &amp; advies</span>
  <h1><em class="stroke">Blogberichten</em></h1>
  <div class="lh__row"><p class="lead">Met meer dan 25 jaar ervaring in ons vak delen we onze opgebouwde expertise graag met u.</p><p>Volg ons: {socials}</p></div>
</div></section>
<section class="section" style="padding-top:12px"><div class="wrap">
  <h2 class="sr-only">Uitgelicht</h2>
  <a class="feature rv" href="{pg.u(f"blog/{first['slug']}/")}"><div class="feature__img">{pg.img(first["img"], first["title"])}</div>
    <div class="feature__text"><span class="chip">Nieuwste · {read_min(first["slug"])} min lezen</span><h3>{first["title"]}</h3><p>{first["excerpt"]}</p><span class="btn">Lees het artikel</span></div></a>
  <div class="btool"><label class="bsearch"><span class="sr-only">Zoek in de blog</span><input type="search" placeholder="Zoek een onderwerp, bv. gevel of plafond"></label>
    <div class="fchips" role="group" aria-label="Onderwerp">{chips}</div></div>
  <h2 class="sr-only">Alle blogberichten</h2>
  <div class="grid grid--3 bgrid">{"".join(blog_card(pg, b) for b in rest)}</div><p class="empty">Geen artikels gevonden. Probeer een ander woord.</p>
</div></section>
{cta(pg)}"""
    write(
        pg,
        layout(
            pg,
            "Blog over schilderwerken en afwerking | SDAD Izegem",
            "Met meer dan 25 jaar ervaring in hun vak wil schilderwerken SDAD hun opgebouwde expertise graag met u delen in hun blogs.",
            body,
        ),
    )


def blog_pages():
    for i, b in enumerate(BLOG):
        pg = Page(f"blog/{b['slug']}/")
        d = DETAILS["blog"][b["slug"]]
        first, rest = d["sections"][0], d["sections"][1:]
        hero_img = first["imgs"][0] if first["imgs"] else b["img"]
        toc, art = [], ""
        for s in rest:
            title, html = split_heading(fix_links(pg, s["html"]))
            if title:
                sid = slugify(title)
                toc.append((sid, title))
                art += f'<h2 id="{sid}">{title}</h2>'
            art += html
            if len(s["imgs"]) == 1:
                art += f'<figure class="art-fig">{pg.img(s["imgs"][0], title or d["title"])}</figure>'
            elif s["imgs"]:
                art += (
                    '<div class="gallery art-gal">'
                    + "".join(
                        f'<button type="button" data-full="{pg.r}assets/img/{im}">{pg.img(im, d["title"], w=400, h=400)}</button>'
                        for im in s["imgs"]
                    )
                    + "</div>"
                )
        toc_html = (
            (
                '<nav class="toc" aria-label="Inhoud"><p>In dit artikel</p><ol>'
                + "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc)
                + "</ol></nav>"
            )
            if len(toc) > 1
            else ""
        )
        others = [BLOG[(i + k) % len(BLOG)] for k in (1, 2, 3)]
        tp = topics_of(b)
        body = f"""<div class="progress" aria-hidden="true"><span></span></div>
<section class="sh sh--article"><div class="wrap sh__grid">
  <div class="sh__text">{crumbs(pg, [("Blog", "blog/"), (escape(d["title"]), None)])}<span class="eyebrow">{dict((k, n) for k, n, _ in TOPICS)[tp[0]]} · {read_min(b["slug"])} min lezen</span>
  <h1>{escape(d["title"])}</h1><div class="lead">{fix_links(pg, first["html"])}</div></div>
  <div class="sh__media"><div class="sh__img">{pg.img(hero_img, d["title"], lazy=False)}</div></div>
</div></section>
<section class="section"><div class="wrap art{" art--toc" if toc_html else ""}">
  {f'<aside class="art__aside">{toc_html}</aside>' if toc_html else ""}
  <article class="art__body prose">{art}</article>
</div></section>
<section class="section section--soft"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Blog</span><h2>Lees ook</h2></div><a class="arrow-link" href="{pg.u('blog/')}">Alle blogberichten</a></div>
  <div class="grid grid--3">{"".join(blog_card(pg, o) for o in others)}</div>
</div></section>{cta(pg)}"""
        write(pg, layout(pg, f"{d['title']} | Blog SDAD", d["desc"] or b["excerpt"], body))
