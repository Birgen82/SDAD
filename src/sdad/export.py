"""Live-modus: zet elke offertepagina als zelfstandige site in dist/<domein>/, klaar om te uploaden."""

import re

from sdad.config import LANDING_DOMAINS, OUT, REPO


def export_landings():
    """Maakt per landingsdomein een zelfstandige map in dist/ (index.html in de root + enkel de nodige bestanden)."""
    import shutil

    for path, url in LANDING_DOMAINS.items():
        out = REPO / "dist" / url.split("//")[1].strip("/").replace("www.", "")
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        html = (OUT / path / "index.html").read_text(encoding="utf8").replace('"../', '"')
        (out / "index.html").write_text(html, encoding="utf8")
        for d in ("assets/css", "assets/js", "assets/fonts"):
            shutil.copytree(OUT / d, out / d)
        for ref in set(re.findall(r'"(assets/(?:img|video)/[^"?]+)', html)) | {"assets/img/list_icon.png", "assets/img/brush.svg"}:
            (out / ref).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(OUT / ref, out / ref)
        print("✓ dist/" + out.name)
