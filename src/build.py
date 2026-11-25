#!/usr/bin/env python3
"""Bouwt de drie SDAD-sites naar de map docs/.

Gebruik (vanuit de hoofdmap van de repository):
    python3 src/build.py

- Hoofdsite (sdad.be): alle pagina's behalve /offerte/ en /offerte-gordijnen/
- offerteschilderwerken.be: docs/offerte/
- offertegordijnen.be: docs/offerte-gordijnen/

Met DEMO = False in src/sdad/config.py wordt bovendien per offertedomein een
zelfstandige map in dist/ gemaakt (zie src/sdad/export.py).
"""

from sdad.config import DEMO
from sdad.export import export_landings
from sdad.pages import blog, contact, diensten, home, juridisch, offerte_gordijnen, offerte_schilderwerken, over, realisaties

PAGES = [
    # Hoofdsite
    home.home,
    over.over,
    diensten.binnen,
    diensten.buiten,
    diensten.decoratief,
    diensten.gordijnen,
    diensten.lamellen,
    realisaties.realisaties,
    blog.blog,
    contact.contact,
    realisaties.realisatie_pages,
    blog.blog_pages,
    juridisch.legal_pages,
    # Offertesites
    offerte_schilderwerken.offerte_page,
    offerte_gordijnen.offerte_gordijnen_page,
]

if __name__ == "__main__":
    for build_page in PAGES:
        build_page()
    if not DEMO:
        export_landings()
