# SDAD – websites

Eén codebasis voor drie sites, met dezelfde huisstijl (rood `#da291c`, antraciet `#4b4f54`):

| Site | Pad in `docs/` | Status |
|---|---|---|
| sdad.be | alles behalve de twee offertepagina's | vernieuwde versie van de bestaande site |
| offerteschilderwerken.be | `offerte/` | landingspagina met offerteformulier |
| offertegordijnen.be | `offerte-gordijnen/` | landingspagina, zachtere variant (`theme-soft`) |

Demo: https://birgen82.github.io/SDAD/ (staat op `noindex`).

De site is statisch: een Python-script genereert gewone HTML-bestanden. Er is geen CMS, database of server nodig.

## Snel starten

```bash
python3 src/build.py                       # bouwt alle pagina's naar docs/
python3 -m http.server -d docs 8000        # bekijken op http://localhost:8000
```

Nodig: Python 3 (getest met 3.13), zonder extra pakketten. Alleen `tools/make_preview.py` heeft Pillow nodig (`pip install pillow`).

## Mappen

```
content/             teksten in JSON: realisaties, blog, detailpagina's, juridische pagina's
src/build.py         startpunt: bouwt alle pagina's
src/sdad/
  config.py          instellingen en vaste gegevens (contact, menu, diensten, reviews, DEMO)
  content.py         laadt content/*.json
  layout.py          paginaskelet: <head>, menubalk, footer, schema.org
  components.py      herbruikbare blokken (werkwijze, reviews, FAQ, galerij, call-to-action ...)
  util.py            hulpfuncties: relatieve paden, miniaturen, wegschrijven
  export.py          live-modus: offertepagina's als losse sites in dist/
  pages/             één module per pagina of paginagroep
docs/                GEGENEREERDE website (HTML) + vaste bestanden in docs/assets/
  assets/css/site.css   alle stijl
  assets/js/main.js     al het gedrag
  assets/img/           foto's (t_… = miniaturen die de build zelf maakt)
  assets/fonts/         Archivo en Nunito Sans, lokaal (SIL Open Font License)
  assets/video/         herovideo (desktop en gsm) en stilstaand beeld
tools/make_preview.py  hele site als één HTML-bestand (om te delen zonder server)
extras/              afbeelding voor de GitHub-deelpreview
```

**Let op:** de HTML in `docs/` wordt bij elke build overschreven. Pas dus nooit HTML in `docs/` aan, maar de bron in `src/` of `content/`. CSS, JS, foto's en lettertypes in `docs/assets/` zijn wél bronbestanden.

## Wat pas je waar aan?

| Wat | Waar |
|---|---|
| Telefoon, e-mail, adres, sociale media, menu | `src/sdad/config.py` |
| Reviews en Trustpilot-score | `REVIEWS`, `TP_SCORE`, `TP_COUNT` in `config.py` |
| Realisaties en blogartikels | `content/realisaties.json`, `content/blog.json`, teksten in `content/details.json` |
| Juridische teksten | `content/legal.json` |
| Teksten van een pagina | `src/sdad/pages/<pagina>.py` |
| Blok dat op meerdere pagina's staat | `src/sdad/components.py` |
| Kleuren, lettertypes, afstanden | variabelen bovenaan `docs/assets/css/site.css` |
| Gedrag (menu, formulieren, filters) | `docs/assets/js/main.js` |

Nieuwe foto: zet hem als `.webp` in `docs/assets/img/` en verwijs ernaar met de bestandsnaam. De build maakt zelf de miniaturen.

Nieuwe pagina: maak een functie in `src/sdad/pages/`, die met `Page("pad/")`, `layout(...)` en `write(...)` een pagina schrijft. Voeg ze toe aan `PAGES` in `src/build.py`. Bekijk `pages/contact.py` als eenvoudig voorbeeld.

## CSS

Eén bestand, `site.css`, ingedeeld in genummerde hoofdstukken (inhoudstafel bovenaan het bestand): variabelen en basis, lay-out, typografie, knoppen, menubalk, footer, hero, kaarten, FAQ, reviews, blog, filters, formulieren, offertepagina's, thema gordijnen, hulpklassen.

- Breekpunten: `980px` (tablet/gsm-menu) en `600px` (gsm).
- `.theme-soft` op `<body>` geeft de gordijnenpagina zachtere tinten met dezelfde componenten.
- `?v=…` achter CSS/JS-links verandert automatisch als het bestand wijzigt, zodat browsers geen oude versie tonen.

## JavaScript

`main.js` is gewoon JavaScript, zonder framework of build-stap. Elk onderdeel is een eigen functie (`initMobileMenu`, `initWizards` ...). Die start alleen als de bijhorende HTML op de pagina staat. Onderaan staat de lijst van alle onderdelen.

Het offerteformulier is generiek. Elk veld met een `name` komt vanzelf in de aanvraag, en met `data-need` en `data-show-if` stuur je validatie en zichtbaarheid vanuit de HTML (uitleg bij `initWizards`).

## Demo en livegang

`DEMO` in `config.py`:

- `True` (nu): `noindex`; canonical- en deellinks wijzen naar de GitHub-demo.
- `False`: geen `noindex`; links wijzen naar sdad.be. De build maakt bovendien per offertedomein een zelfstandige map in `dist/` (bv. `dist/offerteschilderwerken.be/`), klaar om naar die hosting te uploaden. De domeinen staan in `LANDING_DOMAINS`.

### Hosting van de demo (GitHub Pages)

De site staat in `docs/`. Stel in GitHub in: **Settings → Pages → Branch: `main`, map: `/docs`**.

Tot dat gebeurd is, sturen `index.html` en `404.html` in de hoofdmap bezoekers door naar `docs/`. Dat is een tijdelijke oplossing: verwijder beide bestanden en de `.nojekyll` in de hoofdmap zodra Pages op `/docs` staat.

## Nog te doen vóór livegang

- **Formulieren:** het offerte- en het terugbelformulier openen nu het e-mailprogramma van de bezoeker (`sendByMail` in `main.js`). Dat is onbetrouwbaar en niet meetbaar. Koppel ze aan een formulierdienst (bv. Netlify Forms, Formspree of HubSpot).
- **Meten:** er staan geen Google Tag Manager, Analytics of Meta-pixel in. Terugplaatsen kan alleen met een cookiebanner en toestemming.
- **Privacybeleid:** de tekst noemt nog cookies van Google en Facebook en het oude adres van de privacycommissie. Laat hem juridisch nakijken.
- **Offerteknop sdad.be:** verwijst naar `OFFERTE` in `config.py`. Pas aan zodra offerteschilderwerken.be de nieuwe pagina is.
- **Afspraken:** sdad.be gebruikt YouCanBook `afspraaksdad`, de oude offerteschilderwerken.be `schilderwerkensdad`. SDAD kiest welke blijft.
- **Gordijnen, nog te bevestigen door SDAD:** levertijd, garantie (product, motor, plaatsing), duur van het huisbezoek, btw-tarief (vermoedelijk 21%), en welke sfeerbeelden eigen werk zijn. Bevestigd: stalen aan huis, SDAD meet zelf op, verschillende merken.
- **Reviews:** letterlijk overgenomen van Trustpilot. Werk score en aantal handmatig bij. De gordijnenpagina toont alleen reviews over gordijnen of raamdecoratie.

## Controle na een wijziging

Er zijn geen automatische tests. Controleer na een wijziging minstens:

1. `python3 src/build.py` geeft geen fouten.
2. De startpagina, een dienstpagina, `/offerte/` en `/offerte-gordijnen/` op desktop- en gsm-breedte.
3. Menu en uitklapmenu, en het offerteformulier tot de laatste stap.
4. De browserconsole toont geen fouten.

Python-stijl: `ruff check src tools` en `ruff format src tools` (instellingen in `pyproject.toml`).
