"""Instellingen en vaste gegevens van SDAD: adressen, telefoons, menu, diensten, reviews.

Pas hier contactgegevens, links en de demo/live-modus (DEMO) aan."""

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "docs"  # de website zelf (HTML + assets)
CONTENT_DIR = REPO / "content"  # teksten en lijsten in JSON

# Adres van de hoofdsite bij livegang
SITE = "https://sdad.be"

# True: demo op GitHub Pages (noindex, links naar BASE). False: live (ook export naar dist/)
DEMO = True

# Basisadres voor canonical-, deel- en afbeeldingslinks
BASE = "https://birgen82.github.io/SDAD/" if DEMO else SITE + "/"

# Offertepagina's met een eigen domein: pad op de site -> domein
LANDING_DOMAINS = {"offerte/": "https://www.offerteschilderwerken.be/", "offerte-gordijnen/": "https://www.offertegordijnen.be/"}

# Reviews
TRUSTPILOT = "https://nl-be.trustpilot.com/review/sdad.be"

REVIEWS = [  # letterlijk overgenomen van Trustpilot (nl-be.trustpilot.com/review/sdad.be)
    ("Roger V.", "september 2026", 5, "In enkele woorden: TOP resultaat. En niet te vergeten: na de werken is alles netjes achtergelaten."),
    (
        "Sofie C.",
        "oktober 2025",
        5,
        "Zeer correcte en vlotte communicatie! Alles wordt duidelijk afgesproken en nadien ook zo uitgevoerd. Schilderwerken zijn tot in de puntjes verzorgd.",
    ),
    (
        "Febe V.",
        "augustus 2025",
        5,
        "Je voelt dat je in bekwame handen bent, vanaf het begin bij het advies en planning tot de uiteindelijke schilderswerken. … Zeer correcte mensen, zowel qua prijs als communicatie.",
    ),
    (
        "Bart",
        "buitengevel · juli 2024",
        5,
        "Van A tot Z was alles zoals afgesproken. Vanaf de offerte, de uitvoering en tenslotte de eindfactuur was alles in orde. … Zeer tevreden over het resultaat!",
    ),
]

# Trustpilot-score en aantal reviews: handmatig bijwerken
TP_SCORE, TP_COUNT = "4,7", 40

# Knoppen 'Offerte aanvragen' op sdad.be
OFFERTE = "https://www.offerteschilderwerken.be/#Offerteaanvraag"

# Afspraak inplannen (YouCanBook.me)
BOOKING = "https://afspraaksdad.youcanbook.me/"

# Contact
MAIL = "info@sdad.be"

PHONES = [("Lies Nuyttens", "0473 52 09 20", "+32473520920"), ("Arne Deseure", "0478 42 81 95", "+32478428195")]

REGIO = "West- en Oost-Vlaanderen"

MAPS = "https://www.google.com/maps/search/?api=1&query=Prinsdomlaan+50+8870+Izegem"

# Sociale media (footer en schema.org)
SOCIAL = {
    "Facebook": "https://www.facebook.com/DeseureArneNuyttensLies/",
    "Instagram": "https://www.instagram.com/schilderwerken_sdad/",
    "LinkedIn": "https://www.linkedin.com/company/sdad-arne-deseure/",
}

# Menu: uitklapmenu Diensten en de overige menu-items
DIENSTEN = [
    (
        "Schilderwerken",
        [
            ("Binnen", "diensten/schilderwerken/binnen/"),
            ("Buiten", "diensten/schilderwerken/buiten/"),
            ("Decoratieve technieken", "diensten/schilderwerken/decoratieve-technieken/"),
        ],
    ),
    (
        "Interieurafwerking",
        [("Gordijnen", "diensten/interieurafwerking/gordijnen/"), ("Lamellen", "diensten/interieurafwerking/lamellen/")],
    ),
]

MENU = [("Realisaties", "realisaties/"), ("Over SDAD", "over-sdad/"), ("Blog", "blog/"), ("Contact", "contact/")]

# Korte namen per dienst (filters, labels, kruimelpad)
LABELS = {
    "binnen": "Binnen",
    "buiten": "Buiten",
    "gordijnen": "Gordijnen",
    "lamellen": "Lamellen",
    "decoratieve-technieken": "Decoratieve technieken",
}

SERVICE_GROUP = {
    "diensten/schilderwerken/binnen/": "Schilderwerken",
    "diensten/schilderwerken/buiten/": "Schilderwerken",
    "diensten/schilderwerken/decoratieve-technieken/": "Schilderwerken",
    "diensten/interieurafwerking/gordijnen/": "Interieurafwerking",
    "diensten/interieurafwerking/lamellen/": "Interieurafwerking",
}

SERVICE_SHORT = {
    "diensten/schilderwerken/binnen/": "Binnen",
    "diensten/schilderwerken/buiten/": "Buiten",
    "diensten/schilderwerken/decoratieve-technieken/": "Decoratieve technieken",
    "diensten/interieurafwerking/gordijnen/": "Gordijnen",
    "diensten/interieurafwerking/lamellen/": "Lamellen",
}

# Voorwaarde die bij elke garantievermelding staat
GARANTIE_VOORWAARDE = "mits een geschikte ondergrond en een correct opgebouwd verfsysteem"

# Dienstentegels: pad, foto, titel, korte omschrijving
SERVICES = [
    (
        "diensten/schilderwerken/binnen/",
        "1627_nieuwpoort_living.webp",
        "Binnenschilderwerken",
        "Van kleuradvies tot perfecte afwerking, alles voor een interieur dat klopt.",
    ),
    (
        "diensten/schilderwerken/buiten/",
        "1345_gevel_kortrijk.webp",
        "Buitenschilderwerken",
        "Bescherming, uitstraling en vakmanschap voor uw gevel en buitenschrijnwerk.",
    ),
    (
        "diensten/schilderwerken/decoratieve-technieken/",
        "2502_aqua_sensa_1.webp",
        "Decoratieve technieken",
        "Unieke afwerkingen met karakter, structuur en beleving.",
    ),
    (
        "diensten/interieurafwerking/gordijnen/",
        "1644_app_kortrijk_4.webp",
        "Gordijnen",
        "Sfeer, privacy en afwerking perfect afgestemd op uw interieur.",
    ),
    ("diensten/interieurafwerking/lamellen/", "1354_modelapp_4.webp", "Lamellen", "Modern, functioneel en perfect afgestemd op uw ruimte."),
]
