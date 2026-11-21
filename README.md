# SDAD – vernieuwde website (statisch)

Herbouw van sdad.be met dezelfde inhoud en huisstijl (rood #da291c, antraciet #4b4f54, logo en beelden van SDAD).

- Bekijken: `cd sdad && python3 -m http.server` en open http://localhost:8000
- Aanpassen: wijzig teksten in `build.py` (overzichten in `data/realisaties.json` en `data/blog.json`, detailpagina's in `data/details.json`) en draai `python3 build.py`.
- Stijl: `assets/css/style.css` · gedrag: `assets/js/main.js`

## Nog te doen vóór livegang
- Contactformulier: opent nu het e-mailprogramma van de bezoeker (er is geen server). Koppel een formulierdienst of het bestaande CMS.
- De juridische pagina's (privacybeleid, disclaimer, algemene voorwaarden) linken nog naar sdad.be.
- Lettertype: Avenir Next (Typekit-licentie van de huidige site) valt terug op Nunito Sans; koppel de Typekit-kit voor exacte huisstijl.
- Google Tag Manager en Meta-pixel zijn bewust weggelaten; terugplaatsen kan alleen met cookietoestemming.
