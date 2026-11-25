"""Landingspagina offerteschilderwerken.be (/offerte/): offerteformulier in stappen, zonder menu."""

from sdad.components import reviews_block
from sdad.config import BOOKING, GARANTIE_VOORWAARDE, PHONES, REGIO, TP_COUNT, TP_SCORE, TRUSTPILOT
from sdad.layout import layout
from sdad.util import Page, site_link, thumb, write


def offerte_wizard(pg):
    def opts(name, items, kind="radio", need=None):
        n = f' data-need="{need}"' if need else ""
        return (
            f'<div class="opts"{n}>'
            + "".join(f'<label><input type="{kind}" name="{name}" value="{v}"><span>{v}</span></label>' for v in items)
            + "</div>"
        )

    def field(label, name, typ="text", req=True, full=False, ac="", mode="", hint=""):
        h = f'<small class="fhint">{hint}</small>' if hint else ""
        return (
            f'<div{" class=full" if full else ""}><label for="o-{name}">{label}{" *" if req else " <span class=opt>(optioneel)</span>"}</label>'
            f'<input id="o-{name}" name="{name}" type="{typ}"{" required" if req else ""}{f" autocomplete={ac!r}" if ac else ""}{f" inputmode={mode!r}" if mode else ""}>{h}</div>'
        )

    return f"""<div class="wiz lp-wiz" data-subject="Offerteaanvraag via offerteschilderwerken.be" data-submit="Vraag mijn gratis offerte aan"><form onsubmit="return false" novalidate>
  <div class="wiz__body">
    <p class="lp-wiz__title">Gratis offerte in 3 stappen <span>Vrijblijvend</span></p>
    <div class="wiz__bar"><span></span></div>
    <fieldset class="wiz__step"><legend>Welk werk mogen we doen?</legend><p class="hint">Meerdere keuzes mogelijk.</p>
      {opts("Werken", ["Binnenschilderwerken", "Buitenschilderwerken", "Decoratieve technieken", "Ramen, deuren of trap", "Gordijnen, lamellen of raamfolie", "Nog niet zeker, ik wil advies"], "checkbox", "Kies minstens één optie.")}</fieldset>
    <fieldset class="wiz__step"><legend>Wanneer wilt u starten?</legend><p class="hint">Een indicatie volstaat.</p>
      {opts("Timing", ["Zo snel mogelijk", "Binnen 3 maanden", "Later dit jaar", "Nog geen idee"], "radio", "Kies een periode.")}
      <p class="hint" style="margin-top:18px">Voor wie is het?</p>
      {opts("Klanttype", ["Particulier", "Professioneel"], "radio", "Kies particulier of professioneel.")}
      <div data-show-if="Klanttype=Professioneel" hidden style="margin-top:12px"><div class="form-grid">{field("Bedrijfsnaam", "Bedrijfsnaam", req=False, ac="organization")}{field("Btw-nummer", "Btw-nummer", req=False)}</div></div>
    </fieldset>
    <fieldset class="wiz__step"><legend>Waar kunnen we u bereiken?</legend><p class="hint">We nemen snel contact op om een vrijblijvend plaatsbezoek af te spreken.</p>
      <div class="form-grid lp-grid">{field("Naam", "Naam", full=True, ac="name")}{field("Telefoon", "Telefoon", "tel", full=True, ac="tel", hint="Om het plaatsbezoek af te spreken.")}{field("E-mail", "E-mail", "email", full=True, ac="email")}{field("Postcode van de werken", "Postcode", full=True, ac="postal-code", mode="numeric")}
        <div class="full"><label for="o-besch">Korte beschrijving <span class="opt">(optioneel)</span></label><textarea id="o-besch" name="Beschrijving" rows="3" placeholder="bv. living en hal schilderen, ca. 60 m²"></textarea></div>
        <div class="hp" aria-hidden="true" style="position:absolute;left:-9999px"><input name="website" tabindex="-1" autocomplete="off"></div>
      </div></fieldset>
    <p class="wiz__err" aria-live="polite"></p>
    <div class="wiz__nav"><button type="button" class="wiz__back">← Vorige</button><button type="button" class="btn wiz__next">Volgende</button></div>
    <p class="lp-legal">Gratis en zonder verplichtingen. We reageren snel. Uw gegevens gebruiken we alleen voor uw aanvraag (<a href="{site_link(pg, 'cookie-en-privacybeleid/')}" target="_blank">privacybeleid</a>).</p>
  </div>
  <div class="wiz__done" hidden><div class="ok"></div><h3>Bedankt!</h3><p>We nemen snel contact met u op.</p></div>
</form></div>"""


OFFER_SHOTS = [
    ("1893_kortrijk_afgewerkt.webp", "Gevel geschilderd", "Kortrijk"),
    ("1627_nieuwpoort_living.webp", "Leefruimte", "Nieuwpoort"),
    ("1913_blauwhuis_voorzijde_afgewerkt.webp", "Kasteel, binnen en buiten", "Izegem"),
    ("2306_babu_na_3.webp", "Horeca-interieur", "Gent"),
    ("2044_knokke_na_1_3.webp", "Villa, gevel", "Knokke"),
    ("1835_oblix_1.webp", "Restaurant", "Merelbeke"),
]


def offerte_page():
    pg = Page("offerte/")
    trust = f'<a class="tp" href="{TRUSTPILOT}" target="_blank" rel="noopener"><span class="tp__stars" aria-hidden="true">★★★★★</span><span><b>{TP_SCORE}</b> op 5 · {TP_COUNT} reviews op Trustpilot</span></a>'
    services = "".join(
        f'<li class="rv" style="--i:{n}">{pg.img(thumb(i, 640), t, w=320, h=240)}<div><h3>{t}</h3><p>{x}</p></div></li>'
        for n, (i, t, x) in enumerate(
            [
                (
                    "1627_nieuwpoort_living.webp",
                    "Binnenschilderwerken",
                    "Muren, plafonds, deuren en trappen. Met gratis kleuradvies en een strakke afwerking.",
                ),
                (
                    "1893_kortrijk_afgewerkt.webp",
                    "Buitenschilderwerken",
                    "Gevel schilderen of kaleien, ramen en deuren. 10 jaar garantie op gevelschilderwerk*.",
                ),
                ("2442_techniek_12.webp", "Decoratieve technieken", "Kalk, betonlook of een accentmuur met karakter."),
                ("1644_app_kortrijk_4.webp", "Gordijnen en lamellen", "Advies, opmeting en plaatsing op maat."),
            ]
        )
    )
    shots = "".join(
        f'<button type="button" class="rv" style="--i:{n % 3}" data-full="{pg.r}assets/img/{i}">{pg.img(i, f"{t} in {pl}", w=600, h=450)}<span class="lp-cap"><b>{t}</b><span class="lp-sep"> · </span>{pl}</span></button>'
        for n, (i, t, pl) in enumerate(OFFER_SHOTS)
    )
    ticks = "".join(
        f'<li>{b}</li>'
        for b in ["Ervaren vakmensen", "Tijdige en heldere offertes", "Nakomen van afspraken &amp; planning", "Netheid op de werf"]
    )
    steps = "".join(
        f'<li class="rv" style="--i:{n}"><span class="lp-step">{n + 1}</span><h3>{t}</h3><p>{d}</p></li>'
        for n, (t, d) in enumerate(
            [
                ("Aanvraag", "U vult het formulier in of belt ons."),
                ("Plaatsbezoek", "We komen vrijblijvend langs en geven advies."),
                ("Offerte", "U krijgt een duidelijke offerte en planning."),
                ("Uitvoering", "Vakkundig, netjes en volgens afspraak."),
            ]
        )
    )
    qa = [
        ("Wat kost een offerte?", "Niets. De offerte en het plaatsbezoek zijn gratis en vrijblijvend."),
        ("Waar werken jullie?", f"Vanuit Izegem in heel {REGIO}."),
        (
            "Geldt het verlaagde btw-tarief van 6%?",
            "Bij renovatie van een woning ouder dan 10 jaar kan het verlaagde tarief van 6% gelden. We bekijken dit bij de offerte.",
        ),
        (
            "Wat met garantie?",
            f"Voor gevelschilderwerken kunnen we, {GARANTIE_VOORWAARDE}, opleveren met 10 jaar garantie. Voor buitenschrijnwerk gelden andere voorwaarden.",
        ),
        ("Laten jullie de woning netjes achter?", "Ja. Netheid op de werf is een van onze vaste afspraken."),
    ]
    faqs = "".join(f"<details><summary>{q}</summary><div class=\"answer\">{a}</div></details>" for q, a in qa)
    body = f"""<section class="lp-hero">
  <div class="lp-hero__bg" aria-hidden="true">
    <video class="hx__video" autoplay muted loop playsinline preload="metadata" poster="{pg.r}assets/video/hero-poster.webp">
      <source src="{pg.r}assets/video/hero-m.mp4" type="video/mp4" media="(max-width: 700px)">
      <source src="{pg.r}assets/video/hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="wrap lp-hero__grid">
    <div class="lp-hero__text">
      {trust}
      <h1>Schilderwerken in West- en Oost-Vlaanderen, afgewerkt tot in de <em class="stroke">kleinste details</em></h1>
      <p class="lead">Binnen- en buitenschilderwerken door het team van Arne en Lies uit Izegem. Met persoonlijk advies en een vlotte planning.</p>
      <ul class="lp-usp"><li>Gratis plaatsbezoek en offerte</li><li>Meer dan 25 jaar vakmanschap</li><li>10 jaar garantie op gevelschilderwerk*</li></ul>
      <p class="lp-alt">Liever bellen? <a href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a> · <a href="{BOOKING}" target="_blank" rel="noopener">Zelf een plaatsbezoek inplannen</a></p>
    </div>
    <div id="offerte" class="lp-hero__form">{offerte_wizard(pg)}</div>
  </div>
</section>

{reviews_block(pg)}

<section class="section section--soft"><div class="wrap">
  <div class="rv"><span class="eyebrow">Wat we doen</span><h2>Schilderwerken met een hoge afwerkingsgraad</h2></div>
  <ul class="lp-services">{services}</ul>
</div></section>

<section class="section"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Eigen werk</span><h2>Recente realisaties</h2></div><a class="arrow-link" href="#offerte">Vraag uw offerte</a></div>
  <div class="lp-gallery gallery">{shots}</div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="rv">{pg.img("2509_arne_en_lies_samen.webp", "Arne Deseure en Lies Nuyttens van SDAD")}</div>
  <div class="rv" style="--i:1"><span class="eyebrow">Wie komt er langs?</span><h2>Arne en Lies, met hun team</h2>
    <p>Arne Deseure leeft al meer dan 25 jaar voor het schildersvak en bewaakt de kwaliteit op de werf. Lies begeleidt u van het eerste contact tot de oplevering.</p>
    <ul class="checks">{ticks}</ul>
    <div class="btns"><a class="btn" href="#offerte">Vraag mijn gratis offerte aan</a></div></div>
</div></section>

<section class="section section--dark"><div class="wrap">
  <div class="rv"><span class="eyebrow">Zo werkt het</span><h2>In 4 stappen naar een mooi resultaat</h2></div>
  <ol class="lp-steps">{steps}</ol>
</div></section>

<section class="section"><div class="wrap faq2">
  <div class="faq2__aside rv"><span class="eyebrow">Vragen</span><h2>Goed om te weten</h2>
    <div class="ask"><p><strong>Andere vraag?</strong><br>Lies helpt u graag verder.</p><a class="ask__tel" href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a></div></div>
  <div class="faq rv" style="--i:1">{faqs}</div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap"><div class="cta lp-cta">
  <h2>Klaar voor een mooi resultaat?</h2><p>Vraag uw gratis offerte aan, of laat uw nummer achter en we bellen u terug.</p>
  <div class="btns"><a class="btn" href="#offerte">Vraag mijn gratis offerte aan</a></div>
  <form class="callback" novalidate><label for="cb-tel" class="sr-only">Telefoonnummer</label><input id="cb-tel" type="tel" required autocomplete="tel" placeholder="Uw telefoonnummer"><button class="btn btn--ghost no-arrow" type="submit">Bel mij terug</button>
  <p class="callback__ok" hidden>Bedankt! We bellen u zo snel mogelijk terug.</p></form>
</div></div></section>"""
    write(
        pg,
        layout(
            pg,
            "Offerte schilderwerken West- en Oost-Vlaanderen | SDAD",
            "Gratis offerte voor binnen- en buitenschilderwerken in West- en Oost-Vlaanderen. Schildersbedrijf SDAD uit Izegem: 4,7 op 5 op Trustpilot, 25+ jaar vakmanschap.",
            body,
            landing=True,
        ),
    )
