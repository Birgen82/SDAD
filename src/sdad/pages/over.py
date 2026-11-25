"""Pagina Over SDAD."""

from sdad.components import cta, service_hero, video, werkwijze
from sdad.config import SERVICES
from sdad.layout import layout
from sdad.util import Page, p, write


def over():
    pg = Page("over-sdad/")
    values = [
        ("Klantgericht", "we luisteren, denken mee en begeleiden klanten naar de juiste keuzes."),
        ("Efficiënt", "we maken duidelijke afspraken, werken georganiseerd en zorgen voor een vlotte uitvoering."),
        ("Proactief", "we denken vooruit, anticiperen op uitdagingen en zoeken actief naar oplossingen."),
        (
            "Duurzaamheid",
            "we kiezen voor kwalitatieve oplossingen die mooi blijven op lange termijn en bouwen graag aan duurzame klantenrelaties.",
        ),
        ("Gegarandeerd", "we voeren elk project zorgvuldig, correct en volgens de afgesproken kwaliteitsnormen uit."),
        ("Open communicatief", "we luisteren naar elkaar, maken alles bespreekbaar en communiceren open en eerlijk."),
    ]
    vals = "".join(
        f'<li class="rv" style="--i:{i % 3}"><span class="val-nr">0{i + 1}</span><h3>{n}</h3><p>{t[0].upper() + t[1:]}</p></li>'
        for i, (n, t) in enumerate(values)
    )
    timeline = [
        ("2008", "De start", "Arne Deseure start zijn eenmanszaak."),
        ("2016", "SDAD BV", "De eenmanszaak groeit uit tot SDAD BV."),
        (
            "2017",
            "Lies stapt mee in de zaak",
            "Samen bouwen Arne en Lies verder aan een gedeelde visie op vakmanschap, kwaliteit en persoonlijke service.",
        ),
        (
            "Vandaag",
            "Een team van vakmensen",
            "Een gevestigde waarde in de sector, met gespecialiseerde schilders voor particulieren en bedrijven.",
        ),
    ]
    tl = "".join(
        f'<li class="rv" style="--i:{i}"><span class="tl-year">{y}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (y, t, d) in enumerate(timeline)
    )
    verthe = '<a href="https://www.verthe-interieurs.be/" target="_blank" rel="noopener">Verthe Interieurs</a>'
    tiles = "".join(
        f'<a class="tile tile--sm rv" style="--i:{n}" href="{pg.u(h)}">{pg.img(i, t)}<span class="go" aria-hidden="true">→</span><h3>{t}</h3></a>'
        for n, (h, i, t, x) in enumerate(SERVICES)
    )

    def person(img, name, role, paras):
        return f"""<article class="person2 rv">
    <div class="person2__img">{pg.img(img, name)}</div>
    <div class="person2__text"><h3>{name}</h3><p class="role">{role}</p>{p(*paras)}</div></article>"""

    body = (
        service_hero(
            pg,
            [("Over SDAD", None)],
            "Over SDAD",
            'Het <em class="stroke">verhaal</em> achter SDAD',
            '<p class="lead">Wat in 2008 begon als de eenmanszaak van Arne Deseure, groeide in 2016 uit tot SDAD BV. Toen Lies in 2017 mee in de zaak stapte, werd verder gebouwd aan een gedeelde visie gebaseerd op vakmanschap, kwaliteit en persoonlijke service.</p>',
            "<p>Vandaag is SDAD uitgegroeid tot een gevestigde waarde in de sector, met een team van gespecialiseerde schilders dat dagelijks particulieren en bedrijven begeleidt bij schilderwerken en interieurafwerking.</p>",
            "1378_linkedin_30_graden.webp",
            "Bestelwagen met het logo van SDAD",
            ("Sinds 2008", "van eenmanszaak tot team van vakmensen"),
        )
        + f"""

<section class="section section--dark"><div class="wrap">
  <div class="rv"><span class="eyebrow">Onze geschiedenis</span><h2>Van eenmanszaak tot <em class="stroke">gevestigde waarde</em></h2></div>
  <ol class="timeline">{tl}</ol>
</div></section>

<section class="section"><div class="wrap">
  <div class="duo-intro rv"><div><span class="eyebrow">Zaakvoerders</span><h2>Drijvende kracht achter SDAD</h2></div>
  <p class="lead">Achter SDAD staan ondernemers Arne en Lies. Samen bouwen zij dagelijks verder aan een bedrijf waarin vakmanschap, kwaliteit en persoonlijke opvolging centraal staan. Arne bewaakt de technische uitvoering en kwaliteit op de werf, terwijl Lies klanten begeleidt van eerste contact tot oplevering. Elk vanuit hun eigen expertise vormen ze een sterk complementair duo.</p></div>
  <div class="duo-photo rv">{pg.img("2509_arne_en_lies_samen.webp", "Arne Deseure en Lies Nuyttens")}</div>
  <div class="duo">
  {
            person(
                "1423_arne_bewerkt.webp",
                "Arne Deseure",
                "Vakmanschap als fundament",
                [
                    "Al meer dan 25 jaar leeft Arne Deseure voor het schildersvak. Wat begon als een passie, groeide uit tot een carrière waarin vakkennis, kwaliteit en voortdurende bijscholing centraal staan in alles wat hij doet.",
                    "Als meewerkend zaakvoerder binnen SDAD bewaakt Arne dagelijks de kwaliteit van de uitvoering. Hij volgt projecten op, ondersteunt het team op de werf en deelt zijn ervaring met de vakmensen met wie hij samenwerkt.",
                    "Daarnaast blijft hij zich verdiepen in nieuwe technieken, materialen en afwerkingsmethodes, zodat SDAD blijft inspelen op de nieuwste ontwikkelingen binnen het vak.",
                    "Zijn jarenlange ervaring en doorgedreven kennis vormen vandaag nog steeds een van de fundamenten waarop SDAD gebouwd is.",
                ],
            )
        }
  {
            person(
                "2436_profielfoto_lies.webp",
                "Lies Nuyttens",
                "De verbindende schakel",
                [
                    "Sinds Lies in 2017 mee in de zaak stapte, bouwt ze dagelijks mee aan de groei van SDAD. Vandaag vormt ze de verbindende schakel tussen klanten, medewerkers en organisatie.",
                    "Voor veel klanten is Lies het eerste aanspreekpunt binnen SDAD. Ze begeleidt projecten van eerste kennismaking tot oplevering, denkt mee over kleuren en afwerkingen en zorgt voor een duidelijke communicatie gedurende het volledige traject.",
                    "Daarnaast staat ze in voor de dagelijkse organisatie van het bedrijf. Van planning en personeelsopvolging tot administratie en klantencontacten: Lies zorgt ervoor dat zowel klanten als medewerkers kunnen rekenen op een vlotte en gestructureerde aanpak.",
                    "Met haar gedrevenheid, betrokkenheid en ondernemingszin bouwt ze samen met Arne verder aan één duidelijke ambitie: een bedrijf uitbouwen waar kwaliteit, vertrouwen en mensen centraal staan.",
                ],
            )
        }
  </div>
</div></section>

<section class="team-hero">
  <div class="team-hero__img">{pg.img("2438_teamfoto.webp", "Het team van SDAD")}</div>
  <div class="wrap"><div class="team-card rv"><span class="eyebrow">Ons team</span><h2>Het team achter SDAD</h2>
  {
            p(
                "Achter elk geslaagd project staat een team van gemotiveerde vakmensen die elke dag het beste van zichzelf geven.",
                "Binnen SDAD geloven we dat kwaliteit niet alleen bepaald wordt door materialen of technieken, maar vooral door de mensen die het werk uitvoeren. Daarom investeren we in vakkennis, samenwerking en een positieve werkcultuur waarin verantwoordelijkheid en betrokkenheid centraal staan.",
                "Elke medewerker brengt zijn eigen ervaring en talenten mee, maar deelt dezelfde visie: afspraken nakomen, kwalitatief werk afleveren en trots zijn op het resultaat dat wordt afgeleverd.",
                "Samen vormen zij de kracht achter SDAD en zorgen zij er elke dag voor dat klanten kunnen rekenen op kwaliteit, vakmanschap en een betrouwbare partner.",
            )
        }</div></div>
</section>
{werkwijze(pg)}

<section class="section section--soft"><div class="wrap">
  <div class="intro-row rv"><div><span class="eyebrow">Onze waarden</span><h2>Het DNA van SDAD</h2></div>
  <p>Deze waarden vormen de basis van hoe we samenwerken en onze projecten aanpakken.</p></div>
  <ul class="dna">{vals}</ul>
</div></section>

<section class="section"><div class="wrap split">
  <div class="rv"><span class="eyebrow">Twee expertises, één visie</span><h2>Samen sterker voor onze klanten</h2>
  {
            p(
                "Vandaag hebben klanten meer keuzes dan ooit op vlak van interieur, materialen en afwerking. Net daarom geloven wij sterk in het samenbrengen van de juiste expertises rond één project.",
                f"Daarom werken SDAD Schilderwerken en {verthe} al jarenlang nauw samen. Wat ons verbindt, is dezelfde visie op kwaliteit, afwerking en begeleiding van klanten.",
                f"{verthe} begeleidt klanten bij interieuradvies, zit-, woon- en slaapcomfort en totaalinrichting. Bij SDAD vertalen we kleurkeuzes en afwerkingsmogelijkheden naar vakkundig uitgevoerde schilderwerken.",
                "Samen zorgen we ervoor dat interieur en afwerking elkaar versterken en keuzes niet los van elkaar worden gemaakt, maar samen één logisch geheel vormen. Met telkens hetzelfde doel: klanten helpen om met vertrouwen keuzes te maken die op elkaar afgestemd zijn.",
            )
        }
  </div>
  <div class="rv" style="--i:1">{
            video(
                pg,
                "2434_thumbnail_video_sdad_verthe.webp",
                "https://www.youtube.com/watch?v=zO2ZFUFUiMw",
                "Bekijk de film: SDAD × Verthe Interieurs",
                "Film over de samenwerking tussen SDAD en Verthe Interieurs",
            )
        }</div>
</div></section>

<section class="section section--soft"><div class="wrap">
  <div class="head-row rv"><div><span class="eyebrow">Ontdek onze diensten</span><h2>Waarmee kunnen we u helpen?</h2></div></div>
  <div class="related related--5">{tiles}</div>
</div></section>
{cta(pg)}"""
    )
    write(
        pg,
        layout(
            pg,
            "Over SDAD | Schilderwerken en interieurafwerking in Izegem",
            "Schilderwerken SDAD uit Izegem heeft meer dan 25 jaar ervaring in schilderwerken.",
            body,
        ),
    )
