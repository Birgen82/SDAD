"""Herbruikbare blokken die op meerdere pagina's terugkomen (werkwijze, reviews, FAQ, galerij, call-to-action ...)."""

import re
from html import escape

from sdad.config import BOOKING, GARANTIE_VOORWAARDE, LABELS, OFFERTE, PHONES, REGIO, REVIEWS, SERVICES, TP_COUNT, TP_SCORE, TRUSTPILOT
from sdad.content import REAL
from sdad.util import fix_links, p, split_heading


def werkwijze(pg):
    """Werkwijze in 5 stappen, opgebouwd uit teksten die al op de site staan."""
    steps = [
        (
            "Plaatsbezoek",
            "We komen vrijblijvend langs, luisteren naar uw wensen en bekijken samen de mogelijkheden en de staat van de ondergrond.",
        ),
        ("Kleuradvies", "We denken mee over kleuren, materialen en afwerking, afgestemd op de ruimte, de lichtinval en uw stijl."),
        ("Offerte en planning", "U ontvangt een duidelijke offerte en planning, zodat u precies weet wat u mag verwachten."),
        (
            "Voorbereiding en uitvoering",
            "Eerst een correcte voorbereiding van de ondergrond, daarna een vakkundige uitvoering. Met duidelijke communicatie en netheid op de werf.",
        ),
        (
            "Oplevering",
            "Een afwerking tot in de kleinste details en een zorgeloze samenwerking tot de oplevering. We doen wat we zeggen en zeggen wat we doen.",
        ),
    ]
    items = "".join(f'<li data-n="{i}"><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps, 1))
    return f"""<section class="section section--dark" id="werkwijze"><div class="wrap flow">
  <div class="flow__head"><span class="eyebrow">Onze werkwijze</span><h2>Zo pakken we uw project <em class="stroke">aan</em></h2>
  <p class="lead">Een mooi resultaat begint lang voor de eerste verflaag. Van het eerste gesprek tot de oplevering weet u steeds waar u aan toe bent.</p>
  <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a></div></div>
  <ol class="flow__steps">{items}</ol>
</div></section>"""


def garantie_block(pg):
    return f"""<section class="section section--soft" id="garantie" style="scroll-margin-top:90px"><div class="wrap">
  <div class="guarantee">
    <div class="guarantee__badge" aria-hidden="true"><strong>10</strong><span>jaar</span></div>
    <div>
      <span class="eyebrow">Garantie</span><h2>10 jaar garantie op gevelschilderwerk</h2>
      {
        p(
            f"Voor gevelschilderwerken kunnen wij, {GARANTIE_VOORWAARDE}, opleveren met <strong>10 jaar garantie</strong>.",
            "Daarom besteden we veel aandacht aan een correcte voorbereiding van de ondergrond, technisch advies en het gebruik van hoogwaardige kwaliteitsproducten.",
            "Voor schilderwerken aan buitenschrijnwerk gelden andere omstandigheden. Houten ramen en deuren worden veel intensiever belast door zon, regen, temperatuurschommelingen en mechanische belasting. Deze werken kunnen daarom niet met dezelfde garantievoorwaarden worden opgeleverd als gevelschilderwerken.",
        )
    }
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
  <p>Vanuit Izegem werken we voor particulieren en bedrijven in heel {REGIO}. We reageren snel op uw vraag en komen graag bij u ter plaatse.</p>
</div>
  <div><h3>Een greep uit onze realisaties</h3><p class="place-note">Tik op een gemeente om het project te bekijken.</p><ul class="tags place-tags">{"".join(tags)}</ul></div>
</div></section>"""


def cta(
    pg,
    title="Een mooi resultaat begint met een goed gesprek.",
    text="Tijdens een vrijblijvend plaatsbezoek luisteren we naar uw wensen, geven we professioneel advies en bekijken we samen de mogelijkheden voor uw schilderwerken of interieurafwerking.",
):
    return f"""<section class="section"><div class="wrap"><div class="cta">
  <h2>{title}</h2><p>{text}</p>
  <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a></div>
  <p class="cta-sub">Na het vrijblijvende plaatsbezoek ontvangt u een duidelijke offerte en planning. Liever meteen een offerte? <a href="{OFFERTE}" target="_blank" rel="noopener">Vraag ze online aan</a>.</p>
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


def video(pg, img, url, label, alt):
    return f'<a class="video" href="{url}" target="_blank" rel="noopener">{pg.img(img, alt, w=800, h=500)}<span class="video__play" aria-hidden="true"></span><span class="video__label">{label}</span></a>'


def service_hero(pg, crumb, eyebrow, title, lead, extra, img, alt, badge):
    return f"""<section class="sh"><div class="wrap sh__grid">
  <div class="sh__text">{crumbs(pg, crumb)}<span class="eyebrow">{eyebrow}</span><h1>{title}</h1>{lead}{extra}
    <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a>
    <a class="btn btn--ghost no-arrow" href="tel:{PHONES[0][2]}">Bel {PHONES[0][1]}</a></div></div>
  <div class="sh__media"><div class="sh__img">{pg.img(img, alt, lazy=False).replace("<img", '<img fetchpriority="high"')}</div>
    <div class="sh__badge"><strong>{badge[0]}</strong><span>{badge[1]}</span></div>
    {pg.img("red_deco.png", "", cls="sh__deco", w=220, h=240)}</div>
</div></section>"""


def facts_block(facts):
    items = "".join(
        f'<li class="rv" style="--i:{i}"><span class="fact-nr">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(facts)
    )
    return f'<section class="facts"><div class="wrap"><h2 class="sr-only">In het kort</h2><ul>{items}</ul></div></section>'


def subnav(links):
    items = "".join(f'<a href="#{i}">{n}</a>' for i, n in links)
    return f'<nav class="subnav" aria-label="Op deze pagina"><div class="wrap"><span>Op deze pagina</span>{items}</div></nav>'


def faq2(pg, title, qa):
    items = "".join(f"<details><summary>{q}</summary><div class=\"answer\">{a}</div></details>" for q, a in qa)
    return f"""<section class="section section--soft" id="vragen"><div class="wrap faq2">
  <div class="faq2__aside rv"><span class="eyebrow">Veelgestelde vragen</span><h2>{title}</h2>
    <div class="ask"><p><strong>Staat uw vraag er niet bij?</strong><br>Lies helpt u graag verder.</p>
    <a class="ask__tel" href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a>
    <a class="arrow-link" href="{pg.u('contact/')}">Stel uw vraag online</a></div></div>
  <div class="faq rv" style="--i:1">{items}</div>
</div></section>"""


def related(pg, path):
    tiles = "".join(
        f'<a class="tile tile--sm rv" style="--i:{n}" href="{pg.u(h)}">{pg.img(i, t)}<span class="go" aria-hidden="true">→</span><h3>{t}</h3></a>'
        for n, (h, i, t, x) in enumerate([sv for sv in SERVICES if sv[0] != path])
    )
    return f"""<section class="section" id="andere"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Ook interessant</span><h2>Andere diensten</h2></div></div>
  <div class="related">{tiles}</div>
</div></section>"""


def gallery_bento(pg, title, imgs, link, alt_base):
    more = f'<a class="arrow-link" href="{pg.u(link)}">Bekijk volledige realisaties</a>' if link else ""
    items = "".join(
        f'<button type="button" class="rv" style="--i:{n % 4}" data-full="{pg.r}assets/img/{i}">{pg.img(i, f"{alt_base} – sfeerbeeld {n + 1}", w=600, h=600)}</button>'
        for n, i in enumerate(imgs)
    )
    return f"""<section class="section" id="sfeerbeelden"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Inspiratie</span><h2>{title}</h2></div>{more}</div>
  <div class="gallery gallery--bento">{items}</div>
</div></section>"""


def text_section(eyebrow, title, html, soft=False, aside=""):
    inner = (
        f'<div class="split"><div class="rv"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{html}</div><div class="rv img-reveal" style="--i:1">{aside}</div></div>'
        if aside
        else f'<div class="ed"><div class="ed__head"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div><div class="ed__body">{html}</div></div>'
    )
    return f'<section class="section{" section--soft" if soft else ""}"><div class="wrap">{inner}</div></section>'


def shot(pg, r, extra=""):
    chip = " · ".join(LABELS[c] for c in r["cats"]) or ("Project" if r["type"] == "project" else "Particulier")
    return (
        f'<a class="shot"{extra} href="{pg.u(f"realisaties/{r["slug"]}/")}">{pg.img(r["img"], r["title"])}'
        f'<span class="chip">{chip}</span><h3>{escape(r["title"])}</h3></a>'
    )


def detail_sections(pg, secs, alt):
    out, soft = "", False
    for s in secs:
        title, rest = split_heading(fix_links(pg, s["html"]))
        imgs = s["imgs"]
        if len(imgs) > 1:
            if rest.strip():
                out += f'<section class="section"><div class="wrap">{text_block(title, rest)}</div></section>'
            out += gallery_bento(pg, title if not rest.strip() and title else "Sfeerbeelden", imgs, None, alt)
            soft = False
            continue
        if not title and not rest.strip() and not imgs:
            continue
        soft = not soft
        if imgs:
            inner = f'<div class="split"><div class="rv">{f"<h2>{title}</h2>" if title else ""}{rest}</div><div class="rv img-reveal" style="--i:1">{pg.img(imgs[0], title or alt)}</div></div>'
        else:
            inner = text_block(title, rest)
        out += f'<section class="section{" section--soft" if soft else ""}"><div class="wrap">{inner}</div></section>'
    return out


def text_block(title, html):
    if title:
        return f'<div class="ed"><div class="ed__head"><h2>{title}</h2></div><div class="ed__body prose">{html}</div></div>'
    return f'<div class="narrow prose rv">{html}</div>'


def reviews_block(pg, soft=False, cta=True):
    cards = "".join(
        f'''<figure class="rv-card rv" style="--i:{n}"><div class="rv-stars" aria-label="{st} op 5 sterren">{"★" * st}</div>
      <blockquote>“{t}”</blockquote><figcaption><b>{nm}</b> · {d}</figcaption></figure>'''
        for n, (nm, d, st, t) in enumerate(REVIEWS)
    )
    more = '<a class="btn" href="#offerte">Vraag mijn gratis offerte aan</a>' if cta else ""
    return f"""<section class="section{' section--soft' if soft else ''}" id="reviews"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Wat klanten zeggen</span><h2><span class="tp-big">{TP_SCORE}</span> op 5 op Trustpilot</h2>
    <p class="rv-sub">Gemiddelde van {TP_COUNT} reviews. <a href="{TRUSTPILOT}" target="_blank" rel="noopener">Lees alle reviews</a></p></div>{more}</div>
  <div class="rv-grid">{cards}</div>
</div></section>"""
