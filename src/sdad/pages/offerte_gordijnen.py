"""Landingspagina offertegordijnen.be (/offerte-gordijnen/), zachtere variant van de huisstijl (theme-soft)."""

from sdad.config import BOOKING, PHONES, TP_COUNT, TP_SCORE, TRUSTPILOT
from sdad.layout import layout
from sdad.util import Page, site_link, thumb, write

CURTAIN_REVIEWS = [  # letterlijk van Trustpilot; reviews die gordijnen/raamdecoratie noemen + algemene
    (
        "Franky H.",
        "juni 2023",
        5,
        "… onze gordijnen zijn een streling voor het oog. We waren ook zeer tevreden, alles werd tot in de puntjes verzorgd en proper afgewerkt …",
    ),
    (
        "Karel D.",
        "november 2023",
        5,
        "Ons nieuw opgeleverd appartement werd zeer vakkundig geschilderd en top perfect afgewerkt. Ook de raamdecoratie werd prima verzorgd.",
    ),
]


CURTAIN_SHOTS = [
    ("c_1644_0166.webp", "Vouwgordijnen", None),
    ("1647_lamel_combo_gordijn_3.webp", "Overgordijn met houten lamellen", None),
    ("1644_rolgordijnen_2.webp", "Rolgordijn, lichtdoorlatend", None),
    ("1647_0105.webp", "Aluminium lamellen", None),
    ("c_1644_cambr_diaz_3_-_kopie_0.webp", "Rolgordijn in kleur", None),
    ("1644_sleepend_gordijn.webp", "Linnen overgordijn", None),
]


def curtain_wizard(pg):
    def opts(name, items, kind="radio", need=None):
        n = f' data-need="{need}"' if need else ""
        return (
            f'<div class="opts"{n}>'
            + "".join(f'<label><input type="{kind}" name="{name}" value="{v}"><span>{v}</span></label>' for v in items)
            + "</div>"
        )

    def field(label, name, typ="text", req=True, ac="", mode="", hint=""):
        h = f'<small class="fhint">{hint}</small>' if hint else ""
        return (
            f'<div class="full"><label for="g-{name}">{label}{" *" if req else " <span class=opt>(optioneel)</span>"}</label>'
            f'<input id="g-{name}" name="{name}" type="{typ}"{" required" if req else ""}{f" autocomplete={ac!r}" if ac else ""}{f" inputmode={mode!r}" if mode else ""}>{h}</div>'
        )

    return f"""<div class="wiz lp-wiz" data-subject="Offerteaanvraag gordijnen via offertegordijnen" data-submit="Vraag mijn gratis offerte aan"><form onsubmit="return false" novalidate>
  <div class="wiz__body">
    <p class="lp-wiz__title">Gratis offerte in 4 stappen <span>Opmeting aan huis</span></p>
    <div class="wiz__bar"><span></span></div>
    <fieldset class="wiz__step"><legend>Wat zoekt u?</legend><p class="hint">Meerdere keuzes mogelijk.</p>
      {opts("Raamdecoratie", ["Overgordijnen", "Inbetweens", "Rolgordijnen", "Vouwgordijnen", "Lamellen", "Nog niet zeker, ik wil advies"], "checkbox", "Kies minstens één optie.")}</fieldset>
    <fieldset class="wiz__step"><legend>Wat is voor u het belangrijkst?</legend><p class="hint">Meerdere keuzes mogelijk.</p>
      {opts("Wens", ["Verduisteren", "Privacy", "Licht regelen", "Sfeer en warmte", "Akoestiek"], "checkbox", "Kies minstens één wens.")}
      <p class="hint" style="margin-top:18px">Om hoeveel ramen gaat het? Een schatting volstaat.</p>
      {opts("Aantal ramen", ["1", "2 à 3", "4 tot 6", "7 of meer"], "radio", "Kies het aantal ramen.")}
    </fieldset>
    <fieldset class="wiz__step"><legend>Nog twee korte vragen</legend><p class="hint">Bediening</p>
      {opts("Bediening", ["Manueel", "Elektrisch", "Weet ik nog niet"], "radio", "Kies een bediening.")}
      <p class="hint" style="margin-top:18px">Wanneer?</p>
      {opts("Timing", ["Zo snel mogelijk", "Binnen 1 à 3 maanden", "Bij verbouwing of nieuwbouw"], "radio", "Kies een periode.")}
      <p class="hint" style="margin-top:18px">Voor wie is het?</p>
      {opts("Klanttype", ["Particulier", "Professioneel"], "radio", "Kies particulier of professioneel.")}
    </fieldset>
    <fieldset class="wiz__step"><legend>Waar kunnen we u bereiken?</legend><p class="hint">We nemen snel contact op om de opmeting af te spreken.</p>
      <div class="form-grid lp-grid">{field("Naam", "Naam", ac="name")}{field("Telefoon", "Telefoon", "tel", ac="tel", hint="Om de opmeting af te spreken.")}{field("E-mail", "E-mail", "email", ac="email")}{field("Postcode", "Postcode", ac="postal-code", mode="numeric")}
        <div class="full"><label for="g-besch">Korte beschrijving <span class="opt">(optioneel)</span></label><textarea id="g-besch" name="Beschrijving" rows="3" placeholder="bv. living met schuifraam, verduisterend in de slaapkamer, voorkeur voor een moment van opmeting"></textarea></div>
        <div class="hp" aria-hidden="true" style="position:absolute;left:-9999px"><input name="website" tabindex="-1" autocomplete="off"></div>
      </div></fieldset>
    <p class="wiz__err" aria-live="polite"></p>
    <div class="wiz__nav"><button type="button" class="wiz__back">← Vorige</button><button type="button" class="btn wiz__next">Volgende</button></div>
    <p class="lp-legal">Gratis en zonder verplichtingen. Uw gegevens gebruiken we alleen voor uw aanvraag (<a href="{site_link(pg, 'cookie-en-privacybeleid/')}" target="_blank">privacybeleid</a>).</p>
  </div>
  <div class="wiz__done" hidden><div class="ok"></div><h3>Bedankt!</h3><p>We nemen snel contact met u op.</p></div>
</form></div>"""


def offerte_gordijnen_page():
    pg = Page("offerte-gordijnen/")
    trust = f'<a class="tp" href="{TRUSTPILOT}" target="_blank" rel="noopener"><span class="tp__stars" aria-hidden="true">★★★★★</span><span><b>{TP_SCORE}</b> op 5 · {TP_COUNT} reviews op Trustpilot</span></a>'
    types = "".join(
        f'<li class="rv" style="--i:{n}">{pg.img(thumb(i, 640), t, w=320, h=240)}<div><h3>{t}</h3><p>{x}</p></div></li>'
        for n, (i, t, x) in enumerate(
            [
                ("c_1351_modelapp_3.webp", "Overgordijnen", "Sfeer, warmte en een betere akoestiek. Elegant tot op de vloer."),
                ("c_1644_0166.webp", "Rol- en vouwgordijnen", "Strak en praktisch, ook verduisterend voor de slaapkamer."),
                ("1647_0105.webp", "Lamellen", "Hout, aluminium, pvc of textiel. Horizontaal of verticaal."),
                (
                    "c_1647_vb_tr_014_diaz_2_-_kopie_1_0.webp",
                    "Elektrische bediening",
                    "Manueel of elektrisch, ideaal voor grote of hoge ramen.",
                ),
            ]
        )
    )
    shots = "".join(
        f'<button type="button" class="rv" style="--i:{n % 3}" data-full="{pg.r}assets/img/{i}">{pg.img(i, t, w=600, h=450)}<span class="lp-cap"><b>{t}</b>{f"<span class=lp-sep> · </span>{pl}" if pl else ""}</span></button>'
        for n, (i, t, pl) in enumerate(CURTAIN_SHOTS)
    )
    cards = "".join(
        f'''<figure class="rv-card rv" style="--i:{n}"><div class="rv-stars" aria-label="{st} op 5 sterren">{"★" * st}</div>
      <blockquote>“{t}”</blockquote><figcaption><b>{nm}</b> · via Trustpilot</figcaption></figure>'''
        for n, (nm, d, st, t) in enumerate(CURTAIN_REVIEWS)
    )
    wishes = "".join(
        f'<li class="rv" style="--i:{n % 4}"><h3>{w}</h3><p>{d}</p><span class="wish__tip">Ons advies: {t}</span></li>'
        for n, (w, d, t) in enumerate(
            [
                ("Verduisteren", "Rust in de slaapkamer of kinderkamer, ook overdag.", "verduisterende rol- of overgordijnen"),
                ("Privacy", "Geen inkijk, wel daglicht.", "lichtdoorlatende stoffen, inbetweens of lamellen"),
                ("Licht regelen", "Zelf bepalen hoeveel licht en inkijk u wenst.", "lamellen: kantelen of opzij schuiven"),
                ("Sfeer en akoestiek", "Een warme, rustige ruimte met minder galm.", "overgordijnen tot op de vloer"),
            ]
        )
    )
    steps = "".join(
        f'<li class="rv" style="--i:{n}"><span class="lp-step">{n + 1}</span><h3>{t}</h3><p>{d}</p></li>'
        for n, (t, d) in enumerate(
            [
                ("Aanvraag", "U vult het formulier in of belt ons."),
                ("Advies en opmeting", "We komen langs met stalen, adviseren over stof, kleur en bediening en meten zelf nauwkeurig op."),
                ("Offerte", "U krijgt een duidelijke offerte op maat."),
                ("Plaatsing", "We plaatsen alles netjes en vakkundig."),
            ]
        )
    )
    qa = [
        ("Is de opmeting gratis en vrijblijvend?", "Ja. Het advies en de opmeting aan huis zijn gratis en zonder verplichtingen."),
        (
            "Komen jullie zelf opmeten?",
            "Ja. Een correcte opmeting is essentieel voor een mooi resultaat. Daarom komen we steeds ter plaatse om de ramen nauwkeurig op te meten.",
        ),
        ("Wie is verantwoordelijk als de maat niet klopt?", "Wij. Omdat we zelf opmeten, staan we in voor de maat."),
        (
            "Kan ik stalen bekijken?",
            "Ja. We komen met stalen bij u thuis, zodat u stoffen en kleuren kunt bekijken in uw eigen interieur en licht.",
        ),
        (
            "Met welke merken werken jullie?",
            "Met verschillende merken, zodat er voor ieder wat wils is, qua stijl en budget. We adviseren u welk product en merk het best past.",
        ),
        (
            "Wat is het verschil tussen verduisterend en lichtdoorlatend?",
            "Verduisterende stoffen houden (bijna) al het licht tegen, ideaal voor slaapkamers. Lichtdoorlatende stoffen en inbetweens filteren het licht en geven privacy. Bij gordijnen langs de zijkant valt altijd wat licht binnen; we adviseren u over de beste oplossing per raam.",
        ),
        (
            "Wat kies ik voor de badkamer of keuken?",
            "In vochtige ruimtes kiezen we materialen die daartegen bestand zijn, zoals aluminium of kunststof. We bekijken dit samen tijdens het bezoek.",
        ),
        (
            "Wat is veilig in een kinderkamer?",
            "Voor kinderkamers raden we koordloze of elektrische bediening aan. We adviseren u graag over de veiligste oplossing.",
        ),
        (
            "Geven jullie advies over stoffen en kleuren?",
            "Ja. Tijdens het bezoek bekijken we samen welke stoffen, kleuren en afwerkingen het best aansluiten bij uw interieur, lichtinval en wensen.",
        ),
        (
            "Zijn elektrische gordijnen en lamellen mogelijk?",
            "Ja. Afhankelijk van het gekozen systeem kunnen gordijnen en lamellen manueel of elektrisch bediend worden.",
        ),
        ("Plaatsen jullie ook?", "Ja. Naast advies en opmeting verzorgen wij ook de professionele plaatsing."),
        (
            "Doen jullie ook projecten voor bedrijven?",
            "Ja. Ook voor omvangrijke projecten zoals de inrichting van een hotel, kantoor of bedrijvencentrum kunt u bij ons terecht.",
        ),
        (
            "Kan ik gordijnen combineren met lamellen?",
            "Ja. Zo combineert u het praktische karakter van lamellen met de zachtheid en gezelligheid van gordijnen.",
        ),
        (
            "Kunnen jullie ook schilderen?",
            f"Ja. SDAD is in de eerste plaats een schildersbedrijf. Muren, kleuren en raamdecoratie stemmen we graag samen op elkaar af. <a href=\"{site_link(pg, 'offerte/')}\">Offerte voor schilderwerken</a>",
        ),
    ]
    faqs = "".join(f"<details><summary>{q}</summary><div class=\"answer\">{a}</div></details>" for q, a in qa)
    body = f"""<section class="lp-hero">
  <div class="lp-hero__bg" aria-hidden="true">{pg.img("1647_lamel_combo_gordijn_2.webp", "", lazy=False).replace("<img", '<img fetchpriority="high"')}</div>
  <div class="wrap lp-hero__grid">
    <div class="lp-hero__text">
      {trust}
      <h1>Gordijnen en lamellen op maat, <em class="stroke">mooi afgewerkt</em></h1>
      <p class="lead">Advies met stalen aan huis, opmeting en plaatsing door het team van Arne en Lies uit Izegem. Verschillende merken, voor ieder wat wils.</p>
      <ul class="lp-usp"><li>Gratis advies en opmeting aan huis, met stalen</li><li>Wij meten op, wij staan in voor de maat</li><li>Plaatsing inbegrepen</li></ul>
      <p class="lp-alt">Liever bellen? <a href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a> · <a href="{BOOKING}" target="_blank" rel="noopener">Zelf een afspraak inplannen</a></p>
    </div>
    <div id="offerte" class="lp-hero__form">{curtain_wizard(pg)}</div>
  </div>
</section>

<section class="section" id="reviews"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Reviews over raamdecoratie</span><h2><span class="tp-big">{TP_SCORE}</span> op 5 op Trustpilot</h2>
    <p class="rv-sub">Gemiddelde van alle {TP_COUNT} reviews over SDAD. <a href="{TRUSTPILOT}" target="_blank" rel="noopener">Lees alle reviews</a></p></div><a class="btn" href="#offerte">Vraag mijn gratis offerte aan</a></div>
  <div class="rv-grid rv-grid--2">{cards}</div>
</div></section>

<section class="section section--soft"><div class="wrap">
  <div class="rv"><span class="eyebrow">Wat wilt u bereiken?</span><h2>Kies op basis van uw wens</h2></div>
  <ul class="wish">{wishes}</ul>
  <div class="rv" style="margin-top:clamp(40px,6vw,64px)"><span class="eyebrow">Wat we plaatsen</span><h2>Raamdecoratie voor elke ruimte</h2></div>
  <ul class="lp-services">{types}</ul>
</div></section>

<section class="section"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Inspiratie</span><h2>Sfeerbeelden</h2></div><a class="arrow-link" href="#offerte">Vraag uw offerte</a></div>
  <div class="lp-gallery gallery">{shots}</div>
</div></section>

<section class="section section--soft"><div class="wrap split">
  <div class="rv">{pg.img("2509_arne_en_lies_samen.webp", "Arne Deseure en Lies Nuyttens van SDAD")}</div>
  <div class="rv" style="--i:1"><span class="eyebrow">Wie komt er langs?</span><h2>Eén aanspreekpunt voor muren én ramen</h2>
    <p>Lies begeleidt u van het eerste contact tot de plaatsing en denkt mee over stoffen, kleuren en bediening. Omdat SDAD ook schildert, stemmen we de kleuren van muren en gordijnen perfect op elkaar af.</p>
    <ul class="checks"><li>Persoonlijk advies aan huis, met stalen</li><li>Verschillende merken, voor ieder wat wils</li><li>Wij meten op en staan in voor de maat</li><li>Vakkundige plaatsing, volgens afspraak</li></ul>
    <div class="btns"><a class="btn" href="#offerte">Vraag mijn gratis offerte aan</a></div></div>
</div></section>

<section class="section lp-steps-sec"><div class="wrap">
  <div class="rv"><span class="eyebrow">Zo werkt het</span><h2>In 4 stappen naar raamdecoratie op maat</h2></div>
  <ol class="lp-steps">{steps}</ol>
</div></section>

<section class="section section--soft"><div class="wrap faq2">
  <div class="faq2__aside rv"><span class="eyebrow">Vragen</span><h2>Goed om te weten</h2>
    <div class="ask"><p><strong>Andere vraag?</strong><br>Lies helpt u graag verder.</p><a class="ask__tel" href="tel:{PHONES[0][2]}">{PHONES[0][1]}</a></div></div>
  <div class="faq rv" style="--i:1">{faqs}</div>
</div></section>

<section class="section"><div class="wrap"><div class="cta lp-cta">
  <h2>Klaar voor raamdecoratie op maat?</h2><p>Vraag uw gratis offerte aan, of laat uw nummer achter en we bellen u terug.</p>
  <div class="btns"><a class="btn" href="#offerte">Vraag mijn gratis offerte aan</a></div>
  <form class="callback" novalidate><label for="cb-tel" class="sr-only">Telefoonnummer</label><input id="cb-tel" type="tel" required autocomplete="tel" placeholder="Uw telefoonnummer"><button class="btn btn--ghost no-arrow" type="submit">Bel mij terug</button>
  <p class="callback__ok" hidden>Bedankt! We bellen u zo snel mogelijk terug.</p></form>
</div></div></section>"""
    write(
        pg,
        layout(
            pg,
            "Offerte gordijnen en lamellen op maat | SDAD Izegem",
            "Gratis offerte voor gordijnen, rolgordijnen en lamellen op maat in West- en Oost-Vlaanderen. Advies, opmeting en plaatsing door SDAD uit Izegem.",
            body,
            landing=True,
            body_cls="theme-soft",
        ),
    )
