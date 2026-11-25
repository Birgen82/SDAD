"""Dienstpagina's: binnen, buiten, decoratieve technieken, gordijnen en lamellen."""

import re

from sdad.components import cta, facts_block, faq2, gallery_bento, garantie_block, related, service_hero, subnav, text_section, video
from sdad.config import BOOKING
from sdad.content import REAL
from sdad.layout import layout
from sdad.util import Page, p, write

SVC = {
    "diensten/schilderwerken/binnen/": {
        "stroke": "juiste afwerking",
        "badge": ("25+ jaar", "vakmanschap in binnenschilderwerk"),
        "facts": [
            ("Kleuradvies", "We denken mee over kleuren, materialen en afwerking."),
            ("Plamuur en vliesbehang", "Een strakke, egale ondergrond als basis."),
            ("Deuren, ramen en trappen", "Ook binnenschrijnwerk voor een harmonieus geheel."),
            ("Particulier en bedrijf", "Woningen, kantoren, praktijken, horeca en projecten."),
        ],
    },
    "diensten/schilderwerken/buiten/": {
        "stroke": "buitenschilderwerken",
        "badge": ("10 jaar", "garantie op gevelschilderwerk*"),
        "facts": [
            ("Schilderen of kaleien", "Advies over de techniek die esthetisch en technisch klopt."),
            ("Reiniging en ontmossing", "Gevels, blauwsteen en aluminiumprofielen eerst proper."),
            ("Buitenschrijnwerk", "Ramen en deuren schilderen of oliën."),
            ("10 jaar garantie", "Op gevelschilderwerk, mits geschikte ondergrond en correct verfsysteem."),
        ],
    },
    "diensten/schilderwerken/decoratieve-technieken/": {
        "stroke": "karakter",
        "badge": ("Boss Paints", "uitsluitend kwaliteitsproducten"),
        "facts": [
            ("Vier signatuurtechnieken", "Limestone, Calco, Aqua Sensa en Stone Art."),
            ("Handwerk", "Manueel aangebracht, dus elke wand is uniek."),
            ("Ook voor badkamer en keuken", "Aqua Sensa is gemaakt voor intensief gebruikte ruimtes."),
            ("Advies ter plaatse", "Samen kiezen we de techniek die past bij ruimte en budget."),
        ],
    },
    "diensten/interieurafwerking/gordijnen/": {
        "stroke": "comfort",
        "badge": ("Op maat", "advies, opmeting en plaatsing"),
        "facts": [
            ("Advies over stof en kleur", "Afgestemd op uw interieur en de lichtinval."),
            ("Professionele opmeting", "Zodat alles perfect aansluit op ruimte en ramen."),
            ("Elektrisch of manueel", "Bediening die past bij uw gebruiksgemak."),
            ("Plaatsing inbegrepen", "Van advies tot een perfect afgewerkt resultaat."),
        ],
    },
    "diensten/interieurafwerking/lamellen/": {
        "stroke": "uitstraling",
        "badge": ("Op maat", "advies, opmeting en plaatsing"),
        "facts": [
            ("Vier materialen", "Hout, aluminium, pvc of textiel."),
            ("Horizontaal of verticaal", "Verticaal ideaal voor grote glaspartijen en schuiframen."),
            ("Elektrisch of manueel", "Zelf bepalen hoeveel licht en inkijk u wenst."),
            ("Ook voor projecten", "Van woning tot hotel of bedrijvencentrum."),
        ],
    },
}


def service(path, title, desc, crumb_group, hero_title, hero_html, hero_img, sections, gal_title, gal, faq_title, qa, gal_link=None):
    pg = Page(path)
    name = crumb_group[1]
    cfg = SVC[path]
    t = hero_title.replace(cfg["stroke"], f'<em class="stroke">{cfg["stroke"]}</em>', 1)
    m = re.match(r"\s*<p>(.*?)</p>(.*)", hero_html, re.S)
    lead, rest = (f'<p class="lead">{m.group(1)}</p>', m.group(2)) if m else ("", hero_html)
    extra = "".join(re.findall(r'<ul class="tags">.*?</ul>|<div class="tag-group">.*?</ul></div>', rest, re.S))
    rest_p = "".join(re.findall(r"<p>.*?</p>", re.sub(r'<div class="tag-group">.*?</ul></div>', "", rest, flags=re.S), re.S))
    body = service_hero(pg, [(crumb_group[0], None), (name, None)], crumb_group[0], t, lead, extra, hero_img, name, cfg["badge"])
    body += facts_block(cfg["facts"])
    main = ""
    if rest_p:
        main += text_section(name, "Over deze dienst", rest_p)
    for s_ in sections:
        main += s_(pg) if callable(s_) else s_
    links = (
        [("aanpak", "Aanpak")]
        + ([("garantie", "Garantie")] if 'id="garantie"' in main else [])
        + ([("technieken", "Technieken")] if 'id="technieken"' in main else [])
        + [("sfeerbeelden", "Sfeerbeelden"), ("vragen", "Vragen"), ("andere", "Andere diensten")]
    )
    body += subnav(links)
    cat = {"diensten/schilderwerken/binnen/": "binnen", "diensten/schilderwerken/buiten/": "buiten"}.get(path)
    pool = [r["img"] for r in REAL if cat and cat in r["cats"] and r["img"] != hero_img] or gal[1:]
    k = [0]

    def add_fig(m):
        im = pool[k[0] % len(pool)]
        k[0] += 1
        return m.group(0) + f'<figure class="ed__fig">{pg.img(im, name)}</figure>'

    main = re.sub(r'<div class="ed__head">.*?</h2>', add_fig, main, flags=re.S)
    body += f'<div id="aanpak" class="anchor-wrap">{main}</div>'
    body += gallery_bento(pg, gal_title, gal, gal_link, name)
    body += faq2(pg, faq_title, qa)
    body += related(pg, path)
    body += cta(pg)
    write(pg, layout(pg, title, desc, body))


def binnen():
    def vid(pg):
        return f"""<section class="section section--dark"><div class="wrap split">
  <div><span class="eyebrow">Achter de schermen</span><h2>Onze vakmensen aan het werk</h2>
  <p>Achter elk mooi eindresultaat schuilt vakmanschap. Neem een kijkje achter de schermen bij één van onze ploegen tijdens binnenschilderwerken.</p>
  <div class="btns"><a class="btn btn--ghost" href="https://www.youtube.com/watch?v=tOgcMzXHw5E" target="_blank" rel="noopener">Bekijk de video</a></div></div>
  <div>{video(pg, "2506_thumbnail_video_binnenschilderwerken.webp", "https://www.youtube.com/watch?v=tOgcMzXHw5E", "Binnenschilderwerken in beeld", "Video: SDAD aan het werk tijdens binnenschilderwerken")}</div>
</div></section>"""

    service(
        "diensten/schilderwerken/binnen/",
        "Binnenschilderwerken Izegem | SDAD",
        "Bij schilderbedrijf SDAD uit Izegem, West-Vlaanderen kunt u terecht voor professionele binnenschilderwerken.",
        ("Schilderwerken", "Binnenschilderwerken"),
        "Een mooi interieur begint met de juiste afwerking",
        p(
            "Schilderwerken bepalen mee de uitstraling, sfeer en beleving van een ruimte.",
            "Bij SDAD begeleiden we particulieren en bedrijven bij alle schilderwerken, van kleuradvies en voorbereiding tot de uiteindelijke afwerking. We luisteren naar uw wensen, denken mee over materialen, kleuren en technieken en zorgen voor een resultaat dat perfect aansluit bij uw interieur.",
            "Of het nu gaat om een nieuwbouw, renovatie, woning, kantoor of praktijkruimte: elk project krijgt dezelfde aandacht voor detail, kwaliteit en afwerking.",
            "Dankzij jarenlange ervaring, vakkennis en een gestructureerde aanpak zorgen we ervoor dat elk project correct wordt voorbereid en professioneel wordt afgewerkt. Zo creëren we ruimtes waarin mensen zich goed voelen, graag wonen, werken en thuiskomen.",
        ),
        "1340_hectaar_5.webp",
        [
            text_section(
                "Voorbereiding",
                "Een perfect resultaat begint bij de juiste ondergrond",
                p(
                    "Een mooi schilderresultaat staat of valt met de kwaliteit van de ondergrond. Daarom beperken we ons bij SDAD niet enkel tot het schilderwerk zelf.",
                    "Indien nodig verzorgen we ook plamuurwerken om muren en plafonds strak en egaal af te werken. Voor nieuwbouw- en renovatieprojecten adviseren we vaak vliesbehang of renovatievlies als basis voor een duurzaam en verzorgd eindresultaat.",
                    "Door eerst aandacht te besteden aan de voorbereiding en opbouw van de ondergrond zorgen we ervoor dat de uiteindelijke afwerking niet alleen mooi oogt, maar ook jarenlang mooi blijft.",
                    "Van voorbereiding tot eindafwerking begeleiden we u graag naar een resultaat waarin alles klopt.",
                ),
            ),
            vid,
            lambda pg: text_section(
                "Kleuradvies",
                "Meer dan alleen een kleur op de muur",
                p(
                    "De juiste kleur bepaalt mee de sfeer van een ruimte. Toch heeft elke kleur een andere uitstraling afhankelijk van de ruimte, lichtinval, materialen en omgeving.",
                    "Daarom kijken we bij SDAD verder dan enkel een kleurstaal. We luisteren naar uw wensen, bekijken de functie van de ruimte en denken mee over het totaalplaatje. Zo komen we samen tot keuzes die niet alleen vandaag mooi zijn, maar waar u ook op lange termijn tevreden van blijft.",
                    "Of u nu houdt van tijdloos en rustig, warm en huiselijk of net uitgesproken en karaktervol: wij begeleiden u graag naar een resultaat dat perfect aansluit bij uw stijl en interieur.",
                    "Dankzij onze ervaring met kleuren, materialen en afwerkingstechnieken helpen we u keuzes maken die niet alleen mooi ogen, maar ook perfect passen bij uw woning, interieur en manier van leven.",
                    f'<strong>Twijfelt u over kleuren of afwerking?</strong><br>Tijdens een <a href="{BOOKING}" target="_blank" rel="noopener">vrijblijvend plaatsbezoek</a> denken we graag met u mee en bekijken we samen de mogelijkheden.',
                ),
                soft=True,
                aside=pg.img("1_kleurbepaling_linkedin.webp", "Kleuradvies met kleurstalen"),
            ),
        ],
        "Inspiratie uit onze realisaties",
        [
            "1627_hectaar_4_0.webp",
            "1627_vichte_kijkapp_9.webp",
            "1627_ruiselede_mooi_3.webp",
            "1627_particulier_fb_8.webp",
            "1627_binnenschilderwerken_sdad_3.webp",
            "1627_zwijn_2na.webp",
            "1627_dsc_1462.webp",
            "1627_nieuwpoort_living.webp",
        ],
        "Veelgestelde vragen over binnenschilderwerken",
        [
            (
                "Voeren jullie ook plamuurwerken uit?",
                "Ja. Een mooi schilderresultaat begint bij een goede ondergrond. Daarom verzorgen wij indien nodig ook plamuurwerken om muren en plafonds strak, egaal en schilderklaar af te werken.",
            ),
            (
                "Werken jullie ook met vliesbehang?",
                "Ja. Vliesbehang en renovatievlies vormen vaak de ideale basis voor nieuwbouw- en renovatieprojecten. Ze zorgen voor een strakke afwerking en helpen kleine oneffenheden in de ondergrond op te vangen. We adviseren u graag welke oplossing het best aansluit bij uw woning en wensen.",
            ),
            (
                "Geven jullie ook kleuradvies?",
                "Ja. Een geslaagd interieur begint met de juiste keuzes. Daarom begeleiden we klanten die met ons samenwerken graag bij de keuze van kleuren, materialen en afwerkingen, zodat alles perfect op elkaar afgestemd is.",
            ),
            (
                "Schilderen jullie ook deuren, ramen en binnenschrijnwerk?",
                "Absoluut. Naast muren en plafonds verzorgen we ook het schilderen van deuren, kozijnen, trappen en ander binnenschrijnwerk. Zo creëren we een mooi en harmonieus geheel doorheen uw interieur.",
            ),
            (
                "Moeten mijn muren eerst geëgaliseerd worden?",
                "Niet altijd. Tijdens het plaatsbezoek beoordelen we de staat van de ondergrond. Indien nodig voeren we plamuur-, schuur- en egalisatiewerken uit zodat de uiteindelijke schilderafwerking perfect tot haar recht komt.",
            ),
            (
                "Werken jullie zowel voor renovaties, nieuwbouw als bestaande woningen?",
                "Ja. Of het nu gaat om een nieuwbouwwoning, renovatieproject of bestaande woning: wij zorgen steeds voor een professionele voorbereiding, een vlotte uitvoering en een hoogwaardige afwerking.",
            ),
            (
                "Hoe lang duren binnenschilderwerken?",
                "Dat hangt af van de omvang van het project en de nodige voorbereidingswerken. Na het plaatsbezoek ontvangt u een duidelijke offerte en planning, zodat u precies weet wat u mag verwachten.",
            ),
            (
                "Werken jullie ook voor bedrijven?",
                "Ja. We voeren binnenschilderwerken uit voor particulieren, kantoren, handelszaken, praktijken, horeca en residentiële projecten. Daarbij hanteren we steeds dezelfde focus op kwaliteit, planning, communicatie en afwerking.",
            ),
        ],
        gal_link="realisaties/",
    )


def buiten():
    service(
        "diensten/schilderwerken/buiten/",
        "Buitenschilderwerken Izegem | SDAD",
        "Schilderwerken SDAD uit Izegem heeft een getraind oog en ziet wat uw project nodig heeft. Gevel laten schilderen of uw buitenmuren afwerken? Dat kan!",
        ("Schilderwerken", "Buitenschilderwerken"),
        "Professionele buitenschilderwerken",
        p(
            "Uw gevel, buitenschrijnwerk of gevelbekleding bepalen mee de eerste indruk van uw woning of bedrijfspand. Een professionele afwerking zorgt niet alleen voor een verzorgde uitstraling, maar beschermt ook jarenlang tegen weer, wind en vervuiling.",
            "Bij SDAD combineren we technisch advies, kwaliteitsproducten en vakmanschap tot een duurzaam eindresultaat waarop u jarenlang kunt vertrouwen.",
        )
        + '<p class="hero-badge"><strong>10 jaar garantie</strong> op gevelschilderwerk <a href="#garantie">Voorwaarden</a></p>',
        "1345_gevel_kortrijk.webp",
        [
            lambda pg: (
                f"""<section class="section"><div class="wrap grid grid--2" style="align-items:start">
  <div><span class="eyebrow">Gevelbescherming</span><h2>Duurzame bescherming voor uw gevel</h2>
  {
                    p(
                        "Een buitenschilderproject draait niet alleen om kleur. De keuze van het juiste verfsysteem, de staat van de ondergrond en een grondige voorbereiding bepalen mee hoe lang het resultaat mooi blijft.",
                        "Daarom bekijken we vooraf welke aanpak het meest geschikt is voor uw woning of gebouw. Of het nu gaat om schilderen, kaleien of een combinatie van technieken: we adviseren u graag naar een oplossing die zowel esthetisch als technisch klopt.",
                    )
                }</div>
  <div><span class="eyebrow">Reiniging</span><h2>Last van mos, vervuiling of verwering?</h2>
  {
                    p(
                        "Geen probleem! Voordat we de gevel met kleur aanpakken, zorgen we eerst dat alle vuil verwijderd is. Zo kunt u bij SDAD terecht voor onder meer de ontmossing en reiniging van gevels, blauwsteen en de dieptereiniging van aluminiumprofielen.",
                        "Na de reiniging volgt uiteraard de afwerking. We schilderen de gevel met een primerlaag gevolgd door de nodige afwerkingslagen. Liever kaleien? Ook daarvoor bent u bij SDAD aan het juiste adres. We werken zowel met minerale kalei als met decoratieve kwartstechnieken, afhankelijk van de gewenste uitstraling.",
                        "Voor elk buitenproject geeft SDAD steeds voorafgaand technisch advies over het meest geschikte verfsysteem en de ondergrond.",
                    )
                }</div>
</div></section>"""
            ),
            garantie_block,
            lambda pg: text_section(
                "Ramen en deuren",
                "Schilderen of oliën van buitenschrijnwerk",
                p(
                    "Een gevel nieuw leven in blazen zonder het schrijnwerk van de ramen en deuren af te werken? Dat lijkt natuurlijk nergens naar en komt slordig over. SDAD zorgt er dan ook voor dat het gebouw helemaal piekfijn in orde wordt gebracht door het buitenschrijnwerk ook te schilderen of te oliën."
                ),
                soft=True,
                aside=pg.img("1636_ramen_deerlijk.webp", "Geschilderd buitenschrijnwerk in Deerlijk"),
            ),
            lambda pg: text_section(
                "Totaalplaatje",
                "Zorg dat het plaatje klopt",
                p(
                    f'Een verzorgde gevel verdient een interieur dat diezelfde uitstraling doortrekt. Daarom kunt u bij SDAD niet alleen terecht voor buitenschilderwerken, maar ook voor <a href="{pg.u("diensten/schilderwerken/binnen/")}">binnenschilderwerken</a> en <a href="{pg.u("diensten/schilderwerken/decoratieve-technieken/")}">decoratieve technieken</a>.',
                    "Zo zorgen we ervoor dat alles mooi op elkaar afgestemd is en het totaalplaatje klopt.",
                ),
            ),
        ],
        "Inspiratie uit onze realisaties",
        [
            "1636_juli_2012_008_0.webp",
            "1636_odigo.webp",
            "1636_gevel_roeselare.webp",
            "1636_gevel_izegem.webp",
            "1636_gevel_kortrijk_2.webp",
            "1636_gevel_zwevegem.webp",
            "1636_gevel_deinze.webp",
            "1636_ramen_deerlijk.webp",
        ],
        "Veelgestelde vragen over buitenschilderwerken",
        [
            (
                "Wanneer is de beste periode om buitenschilderwerken uit te voeren?",
                "Buitenschilderwerken worden meestal uitgevoerd tussen het voorjaar en het najaar. De ideale omstandigheden hangen af van temperatuur, luchtvochtigheid en weersomstandigheden. Daarom bekijken we per project wat het meest geschikte moment is.",
            ),
            (
                "Wat is het verschil tussen schilderen en kaleien?",
                p(
                    "<strong>Bij schilderen</strong> wordt de bestaande structuur van de gevel behouden. Een verfsysteem beschermt de ondergrond en geeft de gevel een nieuwe kleur en frisse uitstraling, zonder het karakter van de steen of het oppervlak te wijzigen.",
                    "<strong>Bij kaleien</strong> wordt er een minerale kalklaag aangebracht die de gevel een volledig andere uitstraling geeft. De ondergrond krijgt een meer natuurlijke, authentieke en landelijke look. Kalei zorgt voor meer diepte en karakter dan een klassieke schilderafwerking.",
                    "Welke techniek het meest geschikt is, hangt af van de uitstraling die u wenst, de staat van de gevel en de technische eigenschappen van de ondergrond. Tijdens een plaatsbezoek adviseren wij u graag over de beste oplossing voor uw woning.",
                ),
            ),
            (
                "Hoe lang gaat het buitenschilderwerk van een gevel mee?",
                p(
                    "De levensduur van een buitenschilderwerk hangt af van verschillende factoren, zoals de staat van de ondergrond, de ligging van het gebouw, de weersbelasting en het gekozen verfsysteem.",
                    "Bij SDAD besteden we daarom veel aandacht aan een correcte voorbereiding van de ondergrond, technisch advies en het gebruik van hoogwaardige kwaliteitsproducten.",
                    "<strong>Voor gevelschilderwerken</strong> kunnen wij, mits een geschikte ondergrond en een correct opgebouwd verfsysteem, opleveren met <strong>10 jaar garantie</strong>.",
                    "<strong>Voor schilderwerken aan buitenschrijnwerk</strong> gelden andere omstandigheden. Houten ramen en deuren worden immers veel intensiever belast door zon, regen, temperatuurschommelingen en mechanische belasting. Daarom is de levensduur hiervan afhankelijk van verschillende factoren en kunnen deze werken niet met dezelfde garantievoorwaarden worden opgeleverd als gevelschilderwerken.",
                ),
            ),
            (
                "Moet een gevel eerst gereinigd worden?",
                p(
                    "Ja. Een duurzame afwerking begint altijd met een correcte voorbereiding van de ondergrond.",
                    "Mos, algen, straatvuil en andere vervuiling worden eerst verwijderd zodat verf of kalei optimaal kan hechten. Zonder een grondig gereinigde ondergrond kan geen duurzaam verfsysteem worden opgebouwd.",
                    "Daarom bekijken we bij elk project vooraf welke reiniging en voorbereiding nodig zijn om een kwalitatief eindresultaat te garanderen.",
                ),
            ),
            (
                "Schilderen jullie ook ramen en deuren?",
                p(
                    "Absoluut. Naast gevels verzorgen we ook het schilderen of oliën van houten buitenschrijnwerk zoals ramen, deuren, dakoversteken en andere houten elementen.",
                    "Ook PVC- en aluminiumschrijnwerk kunnen wij voorzien van een duurzame schilderafwerking, mits de ondergrond hiervoor geschikt is.",
                ),
            ),
            (
                "Werken jullie ook op hoogte?",
                "Ja. Afhankelijk van het project werken we met ladders, rolstellingen, hoogtewerkers of vaste stellingen om een veilige en kwalitatieve uitvoering te garanderen.",
            ),
            (
                "Geven jullie advies over kleuren en afwerking?",
                "Absoluut. We begeleiden klanten niet alleen bij de uitvoering, maar ook bij de keuze van kleuren, materialen en afwerking zodat het eindresultaat perfect aansluit bij de woning en omgeving.",
            ),
            (
                "Kan ik een vrijblijvende offerte aanvragen?",
                "Ja. Tijdens een plaatsbezoek bekijken we de situatie ter plaatse en ontvangt u een duidelijke en vrijblijvende offerte op maat van uw project.",
            ),
        ],
        gal_link="realisaties/",
    )


def decoratief():
    techs = [
        (
            "LIMESTONE",
            "Rust, diepte en natuurlijke charme",
            "2452_limestone_new_brushtop_7_bosspaints-1.webp",
            [
                "Limestone is een kalktechniek die zorgt voor zachte kleurnuances en natuurlijke bewegingen. De afwerking creëert warmte, diepte en een tijdloze elegantie.",
                "Perfect voor wie houdt van een rustig, natuurlijk interieur met een exclusieve uitstraling.",
            ],
        ),
        (
            "CALCO",
            "Authentieke kalklook met zachte kleurschakeringen",
            "2454_calco_original_5_bosspaints.webp",
            [
                "Calco is een decoratieve kalktechniek die zorgt voor een warme en levendige uitstraling. De subtiele kleurnuances en natuurlijke effecten geven elke wand een eigen uitstraling. Afhankelijk van de gekozen uitvoering kan de afwerking strak en tijdloos ogen of net een meer verweerde, authentieke uitstraling krijgen.",
                "Perfect voor wie op zoek is naar sfeer, warmte en een interieur met een natuurlijke uitstraling.",
            ],
        ),
        (
            "AQUA SENSA",
            "Naadloze uitstraling met moderne elegantie",
            "2456_techniek_11.webp",
            [
                "Aqua Sensa combineert de uitstraling van beton of natuursteen met het comfort van een naadloze afwerking. Dankzij de sterke en onderhoudsvriendelijke eigenschappen is deze techniek geschikt voor zowel woonruimtes als commerciële toepassingen. Ook in badkamers, keukens en andere intensief gebruikte ruimtes komt deze afwerking perfect tot haar recht.",
                "De afwerking zorgt voor een strak en tijdloos resultaat waarbij rust, eenvoud en duurzaamheid centraal staan.",
                "Perfect voor wie houdt van een moderne uitstraling met een minimum aan voegen en een maximum aan beleving.",
            ],
        ),
        (
            "STONE ART",
            "De uitstraling van steen, de kracht van structuur",
            "2458_techniek_21.webp",
            [
                "Stone Art creëert een authentieke steenlook met extra diepte en reliëf. De decoratieve afwerking combineert een natuurlijke uitstraling met een robuust karakter en vormt zo een echte blikvanger binnen elk interieur.",
                "Dankzij de hoge kras- en stootvastheid is Stone Art niet alleen esthetisch sterk, maar ook bijzonder duurzaam in gebruik.",
                "Perfect voor wie op zoek is naar een uitgesproken accentmuur met een unieke uitstraling en een voelbare structuur.",
            ],
        ),
    ]

    def offer(pg):
        tabs = "".join(
            f'<button type="button" role="tab" id="tab-{i}" aria-controls="tp-{i}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}">{n.title()}</button>'
            for i, (n, sub, img, txt) in enumerate(techs)
        )
        blocks = "".join(
            f"""<div class="tech-panel" role="tabpanel" id="tp-{i}" aria-labelledby="tab-{i}"{" hidden" if i else ""}>
  <div class="tech-panel__img">{pg.img(img, f"Decoratieve techniek {n.title()}")}</div>
  <div class="tech-panel__text"><span class="tech-nr">0{i + 1} / 0{len(techs)}</span><h3>{n}</h3><p class="sub">{sub}</p>{p(*txt)}</div>
</div>"""
            for i, (n, sub, img, txt) in enumerate(techs)
        )
        blocks = f'<div class="tabs rv"><div class="tablist" role="tablist" aria-label="Decoratieve technieken">{tabs}</div>{blocks}</div>'
        return f"""<section class="section" id="technieken"><div class="wrap">
  <div class="narrow"><span class="eyebrow">Ons aanbod</span><h2>Inspiratie uit ons aanbod</h2>
  {
            p(
                "Elke decoratieve afwerking heeft haar eigen uitstraling, structuur en toepassing. De mogelijkheden zijn bijzonder veelzijdig. Hieronder ontdekt u alvast enkele afwerkingen uit ons aanbod. Tijdens een vrijblijvend plaatsbezoek bekijken we samen welke techniek het best aansluit bij uw interieur, wensen en de functie van de ruimte.",
                "Voor het realiseren van deze technieken werken we uitsluitend met kwaliteitsproducten van Boss Paints. Zo bent u verzekerd van duurzame afwerkingen, hoogwaardige materialen en een professioneel eindresultaat.",
            )
        }</div>
  {blocks}
</div></section>"""

    more = text_section(
        "Meer mogelijkheden",
        "Nog meer inspiratie",
        p(
            "Niet alle mogelijke technieken staan hierboven vermeld. Het aanbod aan decoratieve afwerkingen, structuren en effecten is bijzonder uitgebreid.",
            f'Tijdens een <a href="{BOOKING}" target="_blank" rel="noopener">vrijblijvend plaatsbezoek</a> bekijken we graag welke decoratieve afwerking het best aansluit bij uw interieur, stijl en wensen.',
            "Hieronder vindt u alvast enkele sfeerbeelden die tonen hoe decoratieve afwerkingen een interieur extra karakter kunnen geven.",
        ),
        soft=True,
    )
    service(
        "diensten/schilderwerken/decoratieve-technieken/",
        "Decoratieve technieken | kalkverf en betonlook | SDAD Izegem",
        "Limestone, Calco, Aqua Sensa en Stone Art. SDAD uit Izegem geeft uw interieur karakter met decoratieve afwerkingen op maat.",
        ("Schilderwerken", "Decoratieve technieken"),
        "Geef uw interieur karakter met decoratieve afwerkingen",
        p(
            "Decoratieve afwerkingen geven een ruimte een unieke uitstraling. Ze zorgen voor sfeer, diepte, structuur en karakter.",
            "Of u nu kiest voor een subtiele kalkafwerking, een strakke betonlook of een uitgesproken accentmuur: samen bekijken we welke techniek het best aansluit bij uw woning, zaak of project.",
            "Zo ontstaat een interieur dat niet alleen mooi oogt, maar ook jarenlang blijft overtuigen.",
        )
        + '<ul class="tags"><li>Limestone</li><li>Calco</li><li>Aqua Sensa</li><li>Stone Art</li></ul>',
        "2442_techniek_12.webp",
        [offer, more],
        "Sfeerbeelden",
        [
            "2502_aqua_sensa_1.webp",
            "2502_b_b_blauwhuis_2.webp",
            "2502_lijo.webp",
            "2502_limestone_1.webp",
            "2502_stucco_puro_1.webp",
            "2502_techniek_7.webp",
            "2502_techniek_9.webp",
            "2502_tusk_1.webp",
        ],
        "Veelgestelde vragen over decoratieve technieken",
        [
            (
                "Zijn decoratieve technieken geschikt voor elke ruimte?",
                "Ja. Afhankelijk van de gekozen techniek kunnen decoratieve afwerkingen toegepast worden in leefruimtes, slaapkamers, keukens, badkamers, kantoren en commerciële ruimtes. Samen bekijken we welke oplossing het best past bij de functie van de ruimte.",
            ),
            (
                "Wat is het verschil tussen een decoratieve techniek en gewone schilderwerken?",
                "Decoratieve technieken creëren extra diepte, structuur en beleving. Waar klassieke schilderwerken vooral kleur brengen, zorgen decoratieve afwerkingen voor een unieke uitstraling met meer karakter en persoonlijkheid.",
            ),
            (
                "Zijn decoratieve afwerkingen onderhoudsvriendelijk?",
                "Ja. De meeste decoratieve technieken zijn eenvoudig te onderhouden. Afhankelijk van de gekozen afwerking kunnen bijkomende beschermlagen voorzien worden voor extra duurzaamheid en gebruiksgemak.",
            ),
            (
                "Kunnen decoratieve technieken ook in badkamers of keukens toegepast worden?",
                "Zeker. Technieken zoals Aqua Sensa zijn speciaal ontwikkeld voor ruimtes die intensief gebruikt worden en bieden een duurzame en onderhoudsvriendelijke oplossing.",
            ),
            (
                "Is elke decoratieve afwerking uniek?",
                "Ja. Decoratieve technieken worden manueel aangebracht waardoor subtiele nuances, kleurschakeringen en structuren ontstaan. Dat maakt elke wand uniek.",
            ),
            (
                "Hoe kiezen we de juiste techniek?",
                f'Tijdens een <a href="{BOOKING}" target="_blank" rel="noopener">vrijblijvend plaatsbezoek</a> luisteren we naar uw wensen en bekijken we samen de ruimte, de gewenste uitstraling en het beschikbare budget. Op basis daarvan adviseren we welke techniek het best aansluit bij uw project.',
            ),
            (
                "Zijn decoratieve technieken duurder dan klassieke schilderwerken?",
                f'Dat hangt af van de gekozen techniek en de oppervlakte. Decoratieve afwerkingen vragen meer vakmanschap en worden vaak in meerdere lagen opgebouwd. Tijdens <a href="{BOOKING}" target="_blank" rel="noopener">het plaatsbezoek</a> ontvangt u steeds een duidelijke offerte op maat.',
            ),
        ],
    )


def gordijnen():
    service(
        "diensten/interieurafwerking/gordijnen/",
        "Gordijnen op maat | gordijnen Izegem | SDAD",
        "Voor alle gordijnen op maat bent u bij schilderwerken SDAD uit Izegem aan het goede adres.",
        ("Interieurafwerking", "Gordijnen"),
        "Gordijnen op maat voor sfeer, privacy en comfort",
        '<ul class="tags"><li>Overgordijnen</li><li>Rolgordijnen</li><li>Vouwgordijnen</li><li>Elektrisch of manueel te bedienen</li></ul>',
        "1351_modelapp_3.webp",
        [
            text_section(
                "Advies, opmeting en plaatsing",
                "De afwerking die uw interieur compleet maakt",
                p(
                    "Gordijnen doen veel meer dan enkel een raam aankleden. Ze zorgen voor sfeer, privacy, een betere akoestiek en brengen rust in uw interieur.",
                    "Daarom begeleiden we u bij SDAD graag bij de keuze van de juiste stof, kleur, afwerking en bediening. Samen bekijken we welke oplossing het best aansluit bij uw woning, interieur en wensen.",
                    "Of u nu kiest voor elegante overgordijnen, praktische rolgordijnen of stijlvolle vouwgordijnen: alles wordt nauwkeurig opgemeten en volledig op maat uitgewerkt.",
                    "Van advies en opmeting tot plaatsing zorgen wij voor een vlotte opvolging en een perfect afgewerkt eindresultaat.",
                ),
            )
        ],
        "Sfeerbeelden",
        [
            "1644_0166.webp",
            "1644_cambr_diaz_3_-_kopie_0.webp",
            "1644_app_kortrijk_4.webp",
            "1644_sleepend_gordijn.webp",
            "1644_paneelgordijnen.webp",
            "1644_rolgordijnen_2.webp",
            "1644_rolgordijnen.webp",
            "1644_gordijn_2.webp",
        ],
        "Veelgestelde vragen over gordijnen",
        [
            (
                "Geven jullie advies over stoffen en kleuren?",
                "Ja. Tijdens een plaatsbezoek bekijken we samen welke stoffen, kleuren en afwerkingen het best aansluiten bij uw interieur, lichtinval en wensen.",
            ),
            (
                "Komen jullie zelf opmeten?",
                "Ja. Wij zorgen voor een professionele opmeting zodat uw gordijnen perfect aansluiten op de ruimte en de ramen.",
            ),
            (
                "Zijn elektrische gordijnen mogelijk?",
                "Ja. Afhankelijk van het gekozen systeem kunnen gordijnen manueel of elektrisch bediend worden. We adviseren u graag over de mogelijkheden die het best aansluiten bij uw woning en gebruiksgemak.",
            ),
            (
                "Plaatsen jullie de gordijnen ook?",
                "Ja. Naast advies en opmeting verzorgen wij ook de professionele plaatsing van uw gordijnen.",
            ),
            (
                "Kunnen gordijnen gecombineerd worden met lamellen of andere raamdecoratie?",
                'Ja. Afhankelijk van de ruimte en de gewenste uitstraling kunnen gordijnen perfect gecombineerd worden met bijvoorbeeld <a href="../lamellen/">lamellen</a> of andere vormen van raamdecoratie.',
            ),
        ],
    )


def lamellen():
    service(
        "diensten/interieurafwerking/lamellen/",
        "Lamellen op maat | Lamellen Izegem | SDAD",
        "Houten, aluminium, pvc of textiel lamellen op maat. SDAD uit Izegem adviseert, meet op en plaatst. Vraag uw vrijblijvend plaatsbezoek aan.",
        ("Interieurafwerking", "Lamellen"),
        "Lamellen op maat voor licht, privacy en uitstraling",
        '<div class="tag-group"><p class="tag-label">Materialen</p><ul class="tags"><li>Houten lamellen</li><li>Aluminium lamellen</li><li>Pvc lamellen</li><li>Textiel lamellen</li></ul>'
        '<p class="tag-label">Uitvoeringen</p><ul class="tags"><li>Horizontale lamellen</li><li>Verticale lamellen</li><li>Elektrisch of manueel bedienbaar</li></ul></div>',
        "1354_modelapp_4.webp",
        [
            lambda pg: text_section(
                "Advies op maat",
                "Functioneel, stijlvol en volledig op maat",
                p(
                    "Lamellen combineren een strakke uitstraling met een grote flexibiliteit in lichtinval en privacy. Door de lamellen te kantelen bepaalt u zelf hoeveel licht binnenkomt en hoeveel inkijk u wenst.",
                    "Ook voor omvangrijke projecten zoals de inrichting van een hotel of een bedrijvencentrum kunt u bij ons terecht. Onze experts komen bij u langs om u professioneel advies te geven over de mogelijkheden en het esthetische aspect.",
                    "Lamellen zijn verkrijgbaar in heel wat materialen. Kies voor hout, pvc, textiel of aluminium. Houd er wel rekening mee dat stoffen lamellen minder licht tegenhouden dan pvc lamellen. Met verticale lamellen kunt u dan weer snel schakelen tussen privacy en openheid door ze dicht te doen of opzij te schuiven. Of speel met de lichtinval voor een leuk effect.",
                    "Over elk model of elk materiaal valt er wat te zeggen. Alles hangt af van de ruimte waar u lamellen wenst en wat uw voorkeuren zijn. Zeker voor hogere raampartijen zijn lamellen bijzonder geschikt.",
                    f'SDAD komt graag bij u langs om de ruimte te bekijken en de juiste lamellen op maat op te voorzien. Neem vrijblijvend <a href="{pg.u("contact/")}">contact</a> met ons op voor professioneel advies of een vrijblijvende offerte.',
                    f'Op zoek naar een zachtere uitstraling? Ontdek ook onze <a href="{pg.u("diensten/interieurafwerking/gordijnen/")}">gordijnen</a> op maat, van elegante overgordijnen tot praktische rol- en vouwgordijnen.',
                ),
            )
        ],
        "Sfeerbeelden",
        [
            "1647_0085.webp",
            "1647_0105.webp",
            "1647_lamel_combo_gordijn.webp",
            "1647_vb_tr_014_diaz_2_-_kopie_1_0.webp",
            "1647_houten_lamellen.webp",
            "1647_lamel_combo_gordijn_3.webp",
            "1647_lamel_combo_gordijn_2.webp",
            "1647_lamel_4.webp",
        ],
        "Veelgestelde vragen over lamellen",
        [
            (
                "Welke lamellen passen het best bij mijn interieur?",
                "Dat hangt af van de ruimte, de gewenste uitstraling en de functie van de raamdecoratie. Houten lamellen zorgen voor een warme en natuurlijke uitstraling, terwijl aluminium of pvc lamellen eerder strak en modern ogen. Tijdens een plaatsbezoek adviseren we u graag over de mogelijkheden.",
            ),
            (
                "Komen jullie zelf opmeten?",
                "Ja. Een correcte opmeting is essentieel voor een mooi eindresultaat. Daarom komen we steeds ter plaatse om de situatie te bekijken en de lamellen nauwkeurig op te meten.",
            ),
            (
                "Kunnen lamellen elektrisch bediend worden?",
                "Ja. Afhankelijk van het gekozen systeem kunnen lamellen zowel manueel als elektrisch bediend worden. We bekijken graag welke oplossing het best aansluit bij uw woning, comfortwensen en gebruiksgemak.",
            ),
            (
                "Zijn lamellen geschikt voor grote raampartijen of schuiframen?",
                "Absoluut. Lamellen zijn bijzonder geschikt voor grote ramen en hoge glaspartijen. Ze bieden een strakke uitstraling en laten toe om de lichtinval eenvoudig te regelen zonder het zicht volledig weg te nemen.",
            ),
            (
                "Wat is het verschil tussen horizontale en verticale lamellen?",
                "Horizontale lamellen worden vaak toegepast bij ramen in woningen en zorgen voor een strakke, tijdloze uitstraling. Verticale lamellen zijn bijzonder geschikt voor grote glaspartijen en schuiframen en bieden veel flexibiliteit in lichtregeling en privacy.",
            ),
            (
                "Kunnen lamellen gecombineerd worden met gordijnen?",
                'Ja. Lamellen kunnen perfect gecombineerd worden met <a href="../gordijnen/">gordijnen</a> voor een warmere uitstraling en extra sfeer. Zo combineert u het praktische karakter van lamellen met de zachtheid en gezelligheid van gordijnen.',
            ),
            (
                "Geven jullie ook advies over kleuren en materialen?",
                "Ja. Tijdens een plaatsbezoek bekijken we samen welke kleuren, materialen en afwerkingen het best aansluiten bij uw interieur, lichtinval en persoonlijke smaak. Zo bent u zeker van een oplossing die niet alleen mooi oogt, maar ook perfect past bij uw woning en manier van leven.",
            ),
        ],
    )
