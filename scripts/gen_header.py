#!/usr/bin/env python3
"""Builds assets/header.svg the scorpion icon on header.
"""
import pathlib
from html import escape

import config as C
from scorpion import scorpion

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "header.svg"

TEMPLATE = r"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1000 320" width="1000" height="320">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#090a0d"/><stop offset=".6" stop-color="#1a0709"/><stop offset="1" stop-color="#6e0f0f"/></linearGradient>
<pattern id="gr" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern>
<linearGradient id="sc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="@@ACCENT@@" stop-opacity="0"/><stop offset=".5" stop-color="@@ACCENT@@" stop-opacity=".12"/><stop offset="1" stop-color="@@ACCENT@@" stop-opacity="0"/></linearGradient>
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="@@ACCENT@@"/><stop offset="1" stop-color="@@ACCENT@@" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="@@ACCENT@@" stop-opacity=".35"/><stop offset="1" stop-color="@@ACCENT@@" stop-opacity="0"/></radialGradient>
</defs>
<style>
text{font-family:'Courier New',Courier,monospace}
.pr{font-size:20px;fill:#8b949e}
.t{font-size:100px;font-weight:700;letter-spacing:4px}
.s{font-size:32px;fill:@@ACCENT@@;opacity:0;animation:s @@CYCLE@@s infinite both}
@@DELAYS@@
@keyframes s{@@KEYFRAMES@@}
.p{opacity:0;animation:p 6s linear infinite}
@keyframes p{0%{transform:translateY(0);opacity:0}20%{opacity:.8}100%{transform:translateY(-110px);opacity:0}}
.g1{animation:g 4s infinite;fill:#00e5ff;opacity:.0}
.g2{animation:g 4s infinite .05s;fill:@@ACCENT@@;opacity:0}
@keyframes g{0%,88%{opacity:0;transform:translate(0,0)}90%{opacity:.7;transform:translate(-5px,2px)}92%{opacity:.7;transform:translate(5px,-2px)}94%,100%{opacity:0;transform:translate(0,0)}}
</style>
<rect width="1000" height="320" fill="url(#bg)"/>
<rect width="1000" height="320" fill="url(#gr)"/>
<circle cx="810" cy="165" r="200" fill="url(#gl)"/>
<text x="60" y="78" class="pr">@@PROMPT@@</text>
<text x="60" y="172" class="t" fill="#ffffff">@@NAME@@</text>
<rect x="60" y="192" width="560" height="4" fill="url(#ln)"/>
@@TAGLINES@@
"""

def build():
    svg = TEMPLATE
    svg = svg.replace("@@ACCENT@@", C.ACCENT)
    svg = svg.replace("@@PROMPT@@", escape(f"root@{C.USER}:~$ ./whoami"))
    svg = svg.replace("@@NAME@@", escape(C.NAME))
    # any number of taglines, each shown for SLOT seconds in turn
    n = len(C.TAGLINES)
    slot = 3
    pct = 100 / n
    svg = svg.replace("@@CYCLE@@", str(slot * n))
    svg = svg.replace("@@DELAYS@@", "".join(f".d{i}{{animation-delay:{i * slot}s}}" for i in range(1, n)))
    svg = svg.replace("@@KEYFRAMES@@",
        f"0%{{opacity:0}}{pct*.18:.2f}%{{opacity:1}}{pct*.84:.2f}%{{opacity:1}}{pct:.2f}%{{opacity:0}}100%{{opacity:0}}")
    lines = []
    for i, line in enumerate(C.TAGLINES):
        cls = "s" if i == 0 else f"s d{i}"
        lines.append(f'<text x="60" y="246" class="{cls}">{escape(line)}</text>')
    svg = svg.replace("@@TAGLINES@@", "\n".join(lines))
    return svg + scorpion(fill=C.ACCENT) + "\n</svg>\n"


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")