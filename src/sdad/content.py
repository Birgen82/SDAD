"""Laadt de teksten uit content/*.json (realisaties, blog, detailpagina's, juridische pagina's)."""

import json

from sdad.config import CONTENT_DIR

REAL = json.loads((CONTENT_DIR / "realisaties.json").read_text(encoding="utf8"))


BLOG = json.loads((CONTENT_DIR / "blog.json").read_text(encoding="utf8"))


DETAILS = json.loads((CONTENT_DIR / "details.json").read_text(encoding="utf8"))


LEGAL = json.loads((CONTENT_DIR / "legal.json").read_text(encoding="utf8"))


PAGES = (
    {"", "over-sdad/", "realisaties/", "blog/", "contact/"}
    | {f"{k}/" for k in LEGAL}
    | {
        p
        for _, items in [
            (
                "",
                [
                    ("", "diensten/schilderwerken/binnen/"),
                    ("", "diensten/schilderwerken/buiten/"),
                    ("", "diensten/schilderwerken/decoratieve-technieken/"),
                    ("", "diensten/interieurafwerking/gordijnen/"),
                    ("", "diensten/interieurafwerking/lamellen/"),
                ],
            )
        ]
        for _, p in items
    }
    | {f"realisaties/{r['slug']}/" for r in REAL}
    | {f"blog/{b['slug']}/" for b in BLOG}
)
