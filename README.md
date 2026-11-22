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
- Lettertypes (Archivo, Nunito Sans) staan lokaal in `assets/fonts/` (SIL Open Font License): geen verbinding met Google nodig.
- Google Tag Manager en Meta-pixel zijn bewust weggelaten; terugplaatsen kan alleen met cookietoestemming.

## Offertepagina (voorstel voor offerteschilderwerken.be)
- Staat op `/offerte/` (functie `offerte_page()` in `build.py`), zelfde huisstijl als de site.
- Doel volgens LocaliQ (VS, 2024-2025): schilders halen op Google Ads gemiddeld ca. 10,8% conversie (formulier + oproepen).
- Opgebouwd volgens onderzoek naar conversie: formulier bovenaan in 3 stappen (werk, timing, contact; adres beperkt tot postcode), geen menu of uitgaande links, statische hoofdfoto, eigen realisaties met plaats, 4 stappen, korte FAQ, terugbelformulier.
- Reviews: 4 echte Trustpilot-reviews (REVIEWS in build.py), letterlijk overgenomen. Werk score en aantal bij (TP_SCORE, TP_COUNT).
- Nog aan te leveren door SDAD: voor/na-foto's; nieuwe reviews verzamelen (Trustpilot meldt 1 review in de afgelopen 12 maanden).
- Het formulier In deze demo opent het bij verzenden het e-mailprogramma; voor livegang koppelen aan het bestaande Webflow/HubSpot-formulier.
- Afspraken: offerteschilderwerken.be gebruikt YouCanBook-domein `schilderwerkensdad`, sdad.be `afspraaksdad`. Laat SDAD kiezen welke de juiste is.

## Offertepagina gordijnen (voorstel)
- Staat op `/offerte-gordijnen/` (functie `offerte_gordijnen_page()`), afgeleide stijl `theme-soft`: zelfde logo, letters en rode knoppen, maar zachtere linnentinten en geen zwarte blokken.
- Formulier: soort raamdecoratie, aantal ramen, bediening, klanttype, contact.
- VOORLOPIG: sfeerbeelden komen van de gordijnen/lamellen-pagina's van sdad.be; SDAD moet bevestigen welke eigen werk zijn. Reviews: 2 die gordijnen/raamdecoratie noemen + 2 algemene (CURTAIN_REVIEWS).
