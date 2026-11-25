"""Contactpagina."""

from sdad.components import cta, page_hero
from sdad.config import BOOKING, MAIL, MAPS, OFFERTE, PHONES
from sdad.layout import layout
from sdad.util import Page, thumb, write


def contact():
    pg = Page("contact/")
    portraits = {"Lies Nuyttens": "2436_profielfoto_lies.webp", "Arne Deseure": "1423_arne_bewerkt.webp"}
    people = "".join(
        f'<div class="contact-card person-card">{pg.img(thumb(portraits[n], 300), n, w=120, h=120)}<div><h3>{n}</h3><p><a href="tel:{t}">{d}</a></p></div></div>'
        for n, d, t in PHONES
    )
    body = (
        page_hero(
            pg,
            [("Contact", None)],
            "Contact",
            "Contacteer ons",
            '<p class="lead">Schilderwerken, gordijnen of lamellen in het vooruitzicht? Neem contact op. Wij helpen u graag verder en reageren snel op uw vraag. We werken in heel West- en Oost-Vlaanderen.</p>',
        )
        + f"""
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="contact-cards"><h2 class="sr-only">Contactgegevens</h2>
    <div class="contact-card"><h3>SDAD bv</h3><p>Prinsdomlaan 50<br>8870 Izegem<br>BE0823.935.816</p><p style="margin-top:10px"><a href="{MAPS}" target="_blank" rel="noopener" style="font-size:1rem">Route plannen →</a></p></div>
    {people}
    <div class="contact-card"><h3>E-mail</h3><p><a href="mailto:{MAIL}">{MAIL}</a></p></div>
    <div class="contact-card" style="background:var(--ink);border-color:var(--ink);color:#c9cbcd"><h3 style="color:#fff">Liever meteen een afspraak?</h3><p style="margin-bottom:14px">Plan zelf een vrijblijvend plaatsbezoek in. Na het vrijblijvende plaatsbezoek ontvangt u een duidelijke offerte en planning.</p><a class="btn" href="{BOOKING}" target="_blank" rel="noopener" style="font-size:1rem;color:#fff">Plaatsbezoek inplannen</a></div>
  </div>
  <div class="offer-card">
    <span class="eyebrow">Offerte aanvragen</span>
    <h2>Vraag uw offerte online aan</h2>
    <p>Via ons offerteformulier bezorgt u ons de gegevens van uw project. We reageren snel en plannen graag een vrijblijvend plaatsbezoek.</p>
    <ul class="checks"><li>Binnen- en buitenschilderwerken</li><li>Decoratieve technieken</li><li>Gordijnen en lamellen</li></ul>
    <div class="btns"><a class="btn" href="{OFFERTE}" target="_blank" rel="noopener">Naar het offerteformulier</a>
    <a class="btn btn--ghost no-arrow" href="{BOOKING}" target="_blank" rel="noopener">Plaatsbezoek inplannen</a></div>
    <p class="offer-note">Het formulier opent op offerteschilderwerken.be, de offertepagina van SDAD.</p>
  </div>
</div></section>
{cta(pg)}"""
    )
    write(
        pg,
        layout(
            pg,
            "Contacteer ons voor schilderwerken, gordijnen of lamellen",
            "Schilderwerken in het vooruitzicht? Neem contact op met schilderwerken SDAD uit Izegem, West-Vlaanderen. Wij helpen u graag verder!",
            body,
        ),
    )
