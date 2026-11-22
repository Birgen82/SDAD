# SDAD – vernieuwde website (statisch)

Herbouw van sdad.be met dezelfde inhoud en huisstijl (rood #da291c, antraciet #4b4f54, logo en beelden van SDAD).

- Bekijken: `cd sdad && python3 -m http.server` en open http://localhost:8000
- Aanpassen: wijzig teksten in `build.py` (overzichten in `data/realisaties.json` en `data/blog.json`, detailpagina's in `data/details.json`) en draai `python3 build.py`.
- Stijl: `assets/css/style.css` · gedrag: `assets/js/main.js`
- Voorbeeldbestand (hele site in één HTML, foto's verkleind): `python3 preview/make_preview.py` → `preview/sdad-site-preview.html`

## Nog te doen vóór livegang
- Zet `DEMO = False` in `build.py` en draai `python3 build.py`. Dan verdwijnt `noindex` en wijzen deel-links, canonical en deelafbeelding naar sdad.be in plaats van de GitHub-demo.
- Offerteaanvragen gaan naar https://www.offerteschilderwerken.be/#Offerteaanvraag (constante `OFFERTE` in `build.py`). Controleer dat dit adres klopt.
- Het cookie- en privacybeleid noemt nog cookies van Google en Facebook; deze site plaatst die niet. Laat de tekst juridisch nakijken en bijwerken (ook het oude adres van de privacycommissie).
- Lettertype: Avenir Next (Typekit-licentie van de huidige site) valt terug op Nunito Sans; koppel de Typekit-kit voor exacte huisstijl.
- Google Tag Manager en Meta-pixel zijn bewust weggelaten; terugplaatsen kan alleen met cookietoestemming.
