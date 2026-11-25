"""Startpagina van sdad.be."""

from html import escape

from sdad.components import cta, reviews_block, werkgebied, werkwijze
from sdad.config import BOOKING, LABELS, OFFERTE, REGIO, SERVICES, TRUSTPILOT
from sdad.content import REAL
from sdad.layout import layout
from sdad.util import Page, write


def home():
    pg = Page("")
    tiles = "".join(
        f"""<a class="tile rv" style="--i:{n}" href="{pg.u(h)}">{pg.img(i, t)}<span class="num">0{n + 1}</span><span class="go" aria-hidden="true">→</span><h3>{t}</h3><p>{x}</p></a>"""
        for n, (h, i, t, x) in enumerate(SERVICES)
    )
    picks = [
        "buitenschilderwerken-kasteel-blauwhuis-te-izegem",
        "rood-residentie-porto-fino-te-wenduine-stop-rood",
        "gevel-villa-te-knokke",
        "babu-gent",
        "frituur-de-platse-lendelede",
        "gevel-villa-te-kortrijk",
        "villa-te-zwijnaarde",
        "schilderen-gevel-te-marke",
    ]
    shots = "".join(
        f"""<a class="shot" href="{pg.u(f"realisaties/{r['slug']}/")}">{pg.img(r["img"], r["title"])}<span class="chip">{" · ".join(LABELS[c] for c in r["cats"]) or ("Project" if r["type"] == "project" else "Particulier")}</span><h3>{escape(r["title"])}</h3></a>"""
        for s_ in picks
        for r in REAL
        if r["slug"] == s_
    )
    four = [
        ("Stielkennis", "voor een vakkundige uitvoering."),
        ("Service", "voor een zorgeloze samenwerking."),
        ("Snelheid", "voor een vlotte en duidelijke planning."),
        ("Stijl", "voor een afwerking tot in de kleinste details."),
    ]
    four_li = "".join(f'<li><span class="s-word">{w}</span><span class="s-desc">{d[0].upper() + d[1:]}</span></li>' for w, d in four)
    ticks = "".join(
        f'<li class="rv" style="--i:{i % 4}">{b}</li>'
        for i, b in enumerate(
            [
                "Ervaren vakmensen",
                "Persoonlijke aanpak",
                "Meedenkend advies",
                "Nakomen van afspraken &amp; planning",
                "Capaciteit en flexibiliteit",
                "Tijdige en heldere offertes",
                "Duidelijke communicatie",
                "Netheid op de werf",
            ]
        )
    )
    body = f"""
<section class="hx hx--full">
  <div class="hx__slides hx__slides--video" aria-hidden="true">
    <video class="hx__video" autoplay muted loop playsinline preload="auto" poster="{pg.r}assets/video/hero-poster.webp">
      <source src="{pg.r}assets/video/hero-m.mp4" type="video/mp4" media="(max-width: 700px)">
      <source src="{pg.r}assets/video/hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="wrap hx__inner">
    <div class="hx__content">
    <span class="eyebrow">Schilderwerken &amp; interieurafwerking<span class="hide-m"> · {REGIO}</span></span>
    <h1><span class="line"><span style="--i:0">Een mooi resultaat</span></span><span class="line"><span style="--i:1">begint lang voor de</span></span><span class="line"><span style="--i:2"><em class="stroke">eerste verflaag.</em></span></span></h1>
    <p class="lead">Van kleuradvies tot een perfect afgewerkt eindresultaat, met persoonlijk advies en een ervaren team.</p>
    <div class="btns"><a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a></div>
    <p class="hx__note">Daarna ontvangt u een duidelijke offerte en planning. Liever meteen een offerte? <a href="{OFFERTE}" target="_blank" rel="noopener">Vraag ze online aan</a>.</p>
    <ul class="hx__stats">
      <li><b data-count="25" data-suffix="+">25+</b>jaar ervaring</li>
      <li><b data-count="10">10</b>jaar garantie op gevels* <a href="{pg.u('diensten/schilderwerken/buiten/')}#garantie">voorwaarden</a></li>
      <li><b>4,7</b><a class="tp-link" href="{TRUSTPILOT}" target="_blank" rel="noopener">op 5 op Trustpilot</a></li>
    </ul>
    </div>

  </div>
</section>

<section class="section rail-wrap"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Recent werk</span><h2>Ons werk spreekt <em class="stroke">voor zich</em></h2></div>
    <div class="rail-nav"><a class="arrow-link" href="{pg.u('realisaties/')}" style="align-self:center;margin-right:10px">Alle realisaties</a><button type="button" data-dir="-1" aria-label="Vorige">←</button><button type="button" data-dir="1" aria-label="Volgende">→</button></div></div>
</div>
<div><div class="rail" tabindex="0" aria-label="Realisaties, horizontaal scrollen">{shots}</div></div>
</section>

<section class="section"><div class="wrap">
  <div class="intro-row rv"><div><span class="eyebrow">Onze diensten</span><h2>Wat we voor u <em class="stroke">doen</em></h2></div>
  <p>Binnen- en buitenschilderwerken, decoratieve technieken en interieurafwerking met gordijnen en lamellen. Van kleuradvies tot oplevering.</p></div>
  <div class="bento">{tiles}</div>
</div></section>

<section class="section four" id="waarom"><div class="wrap four__grid four__grid--img">
  <figure class="four__fig rv">{pg.img("1045_home_header.webp", "Kunstzinnig portret beschilderd in de kleuren van SDAD")}<span class="four__big" aria-hidden="true">S<sup>4</sup></span></figure>
  <div class="rv" style="--i:1"><h2>Schilderkracht tot de vierde macht</h2><p>Zo creëren we ruimtes waar mensen graag wonen, werken en leven.</p>
  <ul class="s-list">{four_li}</ul></div>
</div>
<div class="wrap" style="margin-top:clamp(40px,6vw,72px)"><h3 class="rv" style="color:#fff;font-size:1.6rem;margin-bottom:18px">Daarom kiezen klanten voor SDAD</h3>
  <ul class="ticks">{ticks}</ul></div></section>

<section class="section section--soft"><div class="wrap split">
  <div class="rv">
    <span class="eyebrow">Over SDAD</span><h2>Advies &amp; vakmanschap</h2>
    <p>Bij <a href="{pg.u('over-sdad/')}">SDAD</a> begeleiden we particulieren en bedrijven bij <a href="{pg.u('diensten/schilderwerken/binnen/')}">binnen</a>- en <a href="{pg.u('diensten/schilderwerken/buiten/')}">buitenschilderwerken</a>, <a href="{pg.u('diensten/schilderwerken/decoratieve-technieken/')}">decoratieve technieken</a> en interieurafwerking (<a href="{pg.u('diensten/interieurafwerking/gordijnen/')}">gordijnen</a> en <a href="{pg.u('diensten/interieurafwerking/lamellen/')}">lamellen</a>). Van kleuradvies tot oplevering zorgen we voor een resultaat waarin kwaliteit, uitstraling en vakmanschap samenkomen.</p>
    <p>Met meer dan 25 jaar ervaring en een team van gespecialiseerde schilders beschikken we over de kennis en expertise om elk project professioneel uit te voeren. Of het nu gaat om een woning, kantoor, praktijkruimte, horecazaak of residentieel project, we denken mee over de juiste keuzes en zorgen voor een afwerking die jarenlang blijft overtuigen.</p>
    <p>Wat ons onderscheidt, is onze persoonlijke aanpak. We luisteren naar uw wensen, adviseren waar nodig en communiceren helder gedurende het volledige traject. Zo weet u steeds waar u aan toe bent en kan u rekenen op een zorgeloze samenwerking van eerste gesprek tot oplevering.</p>
    <p>De basis van dat vertrouwen is eenvoudig: <strong>we doen wat we zeggen en zeggen wat we doen.</strong></p>
    <div class="btns"><a class="btn" href="{pg.u('over-sdad/')}">Meer over ons</a></div>
  </div>
  <div class="rv" style="--i:1">{pg.img("2509_arne_en_lies_samen.webp", "Arne Deseure en Lies Nuyttens van SDAD")}</div>
</div></section>
{werkwijze(pg)}



{reviews_block(pg, soft=True, cta=False)}
{werkgebied(pg)}
{cta(pg)}"""
    write(
        pg,
        layout(
            pg,
            "Schilderwerken SDAD | binnen, buiten en interieurafwerking",
            "Bij schilderwerken SDAD uit Izegem kunt u terecht voor professionele binnen en buiten schilderwerken, decoratieve afwerkingen en raamdecoratie in West- en Oost-Vlaanderen.",
            body,
        ),
    )
