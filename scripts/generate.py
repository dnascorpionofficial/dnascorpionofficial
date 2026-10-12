#!/usr/bin/env python3
"""Regenerates every profile SVG except contribution  (snake.yml) into ../assets.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gen_header
import panels

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

FILES = {
    "header.svg": gen_header.build,
    "terminal.svg": panels.terminal,
    "build.svg": panels.build,
    "skills.svg": panels.skills,
    "title-snake.svg": panels.title_snake,
    "private.svg": panels.private,
    "title-contact.svg": panels.title_contact,
    "btn-telegram.svg": panels.btn_telegram,
    "footer.svg": panels.footer,
}

if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, fn in FILES.items():
        (ASSETS / name).write_text(fn(), encoding="utf-8")
        print(f"{name:20s} {(ASSETS / name).stat().st_size:>7,} bytes")
