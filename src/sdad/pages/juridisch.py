"""Juridische pagina's: algemene voorwaarden, cookie- en privacybeleid, disclaimer."""

from sdad.components import page_hero
from sdad.content import LEGAL
from sdad.layout import layout
from sdad.util import Page, fix_links, write


def legal_pages():
    meta = {
        "cookie-en-privacybeleid": (
            "Cookie- en privacybeleid",
            "cookie-en privacybeleid SDAD",
            "<p class=\"lead\">BV Schilder &amp; Decoratiewerken Arne Deseure verwerkt persoonsgegevens overeenkomstig deze privacyverklaring.</p>",
        ),
        "disclaimer": ("Disclaimer", "Disclaimer | Schilderwerken Izegem | SDAD", ""),
        "algemene-voorwaarden": ("Algemene Voorwaarden BV SDAD", "Algemene Voorwaarden BV SDAD", ""),
    }
    for slug, (h1, title, lead) in meta.items():
        pg = Page(f"{slug}/")
        body = page_hero(pg, [(h1, None)], "Juridisch", h1, lead)
        body += f'<section class="section"><div class="wrap"><article class="narrow prose legal">{fix_links(pg, LEGAL[slug]["html"]).replace("<h3>", "<h2>").replace("</h3>", "</h2>")}</article></div></section>'
        write(pg, layout(pg, title, f"{h1} van SDAD bv, Prinsdomlaan 50, 8870 Izegem.", body))
