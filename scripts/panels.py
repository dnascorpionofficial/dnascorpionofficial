"""Builders for every SVG except the header. Each returns the SVG text."""
import math
from html import escape

import config as C

FONT = "text{font-family:'Courier New',Courier,monospace}"
NS = 'xmlns="http://www.w3.org/2000/svg"'


def _t(n):
    """seconds, 2 decimals"""
    return "%.2f" % n


# terminal
def terminal():
    A = C.ACCENT
    rows = []
    for kind, txt in C.TERMINAL:
        full = "$ " + txt if kind == "cmd" else txt
        rows.append((kind, txt, len(full)))
    clips, texts = [], []
    begin, gap = 0.6, 0.25
    for i, (kind, txt, n) in enumerate(rows):
        dur = n * 0.025
        y = 84 + 34 * i
        vals = ";".join(str(w) for w in range(0, (n + 2) * 12, 12))
        clips.append(
            f'<clipPath id="c{i}"><rect x="24" y="{y - 22}" width="0" height="30">'
            f'<animate attributeName="width" values="{vals}" calcMode="discrete" '
            f'dur="{_t(dur)}s" begin="{_t(begin)}s" fill="freeze"/></rect></clipPath>'
        )
        common = f'<text x="28" y="{y}" clip-path="url(#c{i})" textLength="{n * 12:.1f}" lengthAdjust="spacing" style="font-size:20px"'
        if kind == "cmd":
            texts.append(f'{common}><tspan fill="{A}">$ </tspan><tspan fill="#e6edf3">{escape(txt)}</tspan></text>')
        else:
            colour = "#8b949e" if kind == "out" else "#3fb950"
            texts.append(f'{common} fill="{colour}">{escape(txt)}</text>')
        last_end, last_n, last_y = begin + dur, n, y
        begin = begin + dur + gap
    height = 84 + 34 * (len(rows) - 1) + 50
    cursor = (
        f'<rect x="{28 + last_n * 12 + 4}" y="{last_y - 17}" width="11" height="22" fill="{A}" opacity="0">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" begin="{_t(last_end)}s" repeatCount="6" fill="freeze"/></rect>'
    )
    return (
        f'<svg {NS} viewBox="0 0 640 {height}" width="640" height="{height}">\n'
        f"<style>{FONT}</style>\n"
        f'<defs>{"".join(clips)}</defs>\n'
        f'<rect x="1" y="1" width="638" height="{height - 2}" rx="14" fill="#0d1117" stroke="{A}" stroke-opacity=".55" stroke-width="2"/>\n'
        '<path d="M1,15 a14,14 0 0 1 14,-14 H625 a14,14 0 0 1 14,14 V44 H1 Z" fill="#161b22"/>\n'
        '<circle cx="26" cy="23" r="6" fill="#ff5f56"/><circle cx="48" cy="23" r="6" fill="#ffbd2e"/><circle cx="70" cy="23" r="6" fill="#27c93f"/>\n'
        f'<text x="320" y="28" text-anchor="middle" fill="#8b949e" style="font-size:15px">{escape(C.TERMINAL_TITLE)}</text>\n'
        f'{"".join(texts)}\n{cursor}\n</svg>'
    )

# build cards
def _icons(A):
    return {
        "bot": f'<g fill="none" stroke="{A}" stroke-width="3" stroke-linecap="round"><rect x="-22" y="-16" width="44" height="34" rx="8"/><path d="M0,-16 V-26"/><circle cx="0" cy="-29" r="3" fill="{A}"/><circle cx="-9" cy="-1" r="4" fill="{A}"/><circle cx="9" cy="-1" r="4" fill="{A}"/><path d="M-8,10 H8"/></g>',
        "phone": f'<g fill="none" stroke="{A}" stroke-width="3" stroke-linecap="round"><rect x="-17" y="-28" width="34" height="56" rx="7"/><path d="M-6,-21 H6"/><circle cx="0" cy="20" r="2.5" fill="{A}"/></g>',
        "gear": f'<g fill="none" stroke="{A}" stroke-width="3"><circle cx="0" cy="0" r="13"/><circle cx="0" cy="0" r="22" stroke-width="7" stroke-dasharray="7 9.6"/></g>',
    }


def build():
    A = C.ACCENT
    icons = _icons(A)
    cards = []
    for i, (icon, title, l1, l2) in enumerate(C.BUILD):
        cards.append(
            f'<g class="cd" style="animation-delay:{i * 0.25}s" transform="translate(0,{84 + 112 * i})">\n'
            f'<rect x="20" y="0" width="560" height="96" rx="14" fill="#10151c" stroke="{A}" stroke-opacity=".4" stroke-width="1.5"></rect>\n'
            f'<rect x="20" y="0" width="6" height="96" rx="3" fill="{A}"/>\n'
            f'<g transform="translate(78,48)">{icons[icon]}</g>\n'
            f'<text x="130" y="38" class="a">{escape(title)}</text>'
            f'<text x="130" y="62" class="b">{escape(l1)}</text>'
            f'<text x="130" y="82" class="b">{escape(l2)}</text></g>'
        )
    height = 84 + 112 * len(C.BUILD) + 4
    return (
        f'<svg {NS} viewBox="0 0 600 {height}" width="600" height="{height}">\n'
        f"<style>{FONT}.h{{font-size:28px;font-weight:700;fill:#fff}}.a{{font-size:23px;font-weight:700;fill:#e6edf3}}.b{{font-size:16px;fill:#8b949e}}\n"
        ".cd{opacity:0;animation:in .7s ease-out both}@keyframes in{from{opacity:0;transform:translateX(-30px)}to{opacity:1}}</style>\n"
        f'<text x="24" y="44" class="h">{escape(C.BUILD_TITLE)}</text><rect x="24" y="56" width="60" height="3" fill="{A}"/>\n'
        f'{"".join(cards)}</svg>'
    )

# skills
def skills():
    A = C.ACCENT
    circ = round(2 * math.pi * 42, 1) # 263.9
    rows = math.ceil(len(C.SKILLS) / 3)
    legend_y = 150 + 170 * (rows - 1) + 122
    height = legend_y + 52
    groups = []
    for i, (badge, name, level) in enumerate(C.SKILLS):
        frac, col, _ = C.LEVELS[level]
        cx, cy = 100 + 200 * (i % 3), 150 + 170 * (i // 3)
        off = "%.1f" % (circ * (1 - frac))
        d = f"{i * 0.12:.2f}"
        ring = (
            f'<circle cx="{cx}" cy="{cy}" r="42" fill="none" stroke="{col}" %s stroke-linecap="round" '
            f'stroke-dasharray="{circ}" stroke-dashoffset="{off}" transform="rotate(-90 {cx} {cy})" class="rg" style="animation-delay:{d}s"/>'
        )
        groups.append(
            "<g>\n"
            f'<circle cx="{cx}" cy="{cy}" r="42" fill="none" stroke="#21262d" stroke-width="9"/>\n'
            + ring % 'stroke-opacity=".22" stroke-width="15"' + "\n"
            + ring % 'stroke-width="9"' + "\n"
            f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" class="gl">{escape(badge)}</text>\n'
            f'<text x="{cx}" y="{cy + 72}" text-anchor="middle" class="nm">{escape(name)}</text>\n'
            f'<text x="{cx}" y="{cy + 94}" text-anchor="middle" class="lv" fill="{col}">{level}</text></g>'
        )
    legend = "".join(
        f'<circle cx="{lx}" cy="0" r="6" fill="{col}"/><text x="{lx + 12}" y="5" class="k">{lvl}</text>'
        + ("\n" if j == 0 else "")
        for j, (lvl, (_, col, lx)) in enumerate(C.LEVELS.items())
    )
    return (
        f'<svg {NS} viewBox="0 0 600 {height}" width="600" height="{height}">\n'
        '<defs><filter id="gw" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>\n'
        f"<style>{FONT}.h{{font-size:28px;font-weight:700;fill:#fff}}.gl{{font-size:24px;font-weight:700;fill:#e6edf3}}.nm{{font-size:19px;font-weight:700;fill:#e6edf3}}.lv{{font-size:16px;font-weight:700}}.k{{font-size:15px;fill:#8b949e}}\n"
        f".rg{{animation:r 1.4s ease-out both}}@keyframes r{{from{{stroke-dashoffset:{circ}}}}}</style>\n"
        f'<rect x="1" y="1" width="598" height="{height - 2}" rx="16" fill="#0d1117" stroke="{A}" stroke-opacity=".5" stroke-width="1.5"/>\n'
        f'<text x="30" y="52" class="h">{escape(C.SKILLS_TITLE)}</text><rect x="30" y="64" width="60" height="3" fill="{A}"/>\n'
        + "".join(groups)
        + f'<g transform="translate(0,{legend_y})">{legend}\n'
        f'<text x="300" y="34" text-anchor="middle" class="k">{escape(C.SKILLS_NOTE)}</text></g></svg>'
    )

# small ones
def _title(text):
    return (
        f'<svg {NS} viewBox="0 0 600 60" width="600" height="60"><style>{FONT}</style>\n'
        f'<rect x="24" y="14" width="6" height="30" rx="3" fill="{C.ACCENT}"/>\n'
        f'<text x="42" y="38" style="font-size:28px;font-weight:700" fill="#fff">{escape(text)}</text></svg>'
    )

def title_snake():
    return _title(C.SNAKE_TITLE)

def title_contact():
    return _title(C.CONTACT_TITLE)

def btn_telegram():
    return (
        f'<svg {NS} viewBox="0 0 440 76" width="440" height="76"><style>{FONT}</style>\n'
        '<defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2aabee"/><stop offset="1" stop-color="#1d82c4"/></linearGradient></defs>\n'
        '<rect x="4" y="4" width="432" height="68" rx="18" fill="none" stroke="#2aabee" stroke-width="2"><animate attributeName="stroke-opacity" values=".9;.15;.9" dur="2.4s" repeatCount="indefinite"/></rect>\n'
        '<rect x="8" y="8" width="424" height="60" rx="14" fill="url(#tg)"/>\n'
        '<g transform="translate(46,38)"><path d="M-18,-2 L18,-17 L11,17 L1,9 L-6,15 L-6,5 Z" fill="#fff"/><path d="M-6,5 L11,-9" stroke="#2aabee" stroke-width="2" fill="none"/></g>\n'
        f'<text x="86" y="46" style="font-size:25px;font-weight:700" fill="#fff">{escape(C.TELEGRAM_TEXT)}</text></svg>'
    )

def footer():
    waves = [(52, 14, 0.0, "#6e0f0f", "0.55"), (72, 10, 1.5, C.ACCENT, "0.45"), (92, 8, 3.0, "#0d0d0f", "1")]
    paths = []
    for c, a, ph, fill, op in waves:
        pts = "".join(
            f" L{x},{c + a * math.sin(2 * math.pi * x / 500 + ph):.1f}" for x in range(0, 1001, 25)
        )
        paths.append(f'<path d="M0,120{pts} L1000,120 Z" fill="{fill}" fill-opacity="{op}"/>')
    return (
        f'<svg {NS} viewBox="0 0 1000 120" width="1000" height="120" preserveAspectRatio="none">'
        + "".join(paths) + "</svg>"
    )