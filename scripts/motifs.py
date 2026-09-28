"""Small looping animations, one per featured project card.

Each motif draws inside a 76 x 76 box (local coordinates) in the card's accent
colour and says, in one glance, what the project does. SMIL only; the
attributes written on each element are a sensible still frame, so a renderer
without SMIL shows a finished picture.

    svg = draw("graph", accent)          # -> '<g>...</g>' in local coordinates
    text = glyphs("page")                # characters the font subset must hold
"""
from __future__ import annotations

import math

from svgkit import C

S = 76  # box size


def _kt(times: list[float], T: float) -> str:
    return ";".join(f"{min(max(t / T, 0), 1):.4f}" for t in times)


def _anim(attr: str, values: list, times: list[float], T: float, extra: str = "") -> str:
    return (f'<animate attributeName="{attr}" values="{";".join(str(v) for v in values)}" '
            f'keyTimes="{_kt(times, T)}" dur="{T}s" repeatCount="indefinite" {extra}/>')


# ---------------------------------------------------------------- THROUGHLINE
def graph(a: str) -> str:
    """Evidence graph: engines around a hub send cited claims inward."""
    cx, cy, R = 38, 38, 29
    out = []
    pts = [(cx + R * math.cos(math.radians(-90 + i * 60)), cy + R * math.sin(math.radians(-90 + i * 60))) for i in range(6)]
    for i, (x, y) in enumerate(pts):  # ring edges between neighbours
        x2, y2 = pts[(i + 1) % 6]
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{C["faint"]}" stroke-dasharray="2 3"/>')
    for i, (x, y) in enumerate(pts):
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{cx}" y2="{cy}" stroke="{a}" stroke-opacity="0.35"/>')
        out.append(
            f'<circle r="1.9" fill="{a}" opacity="0"><animateMotion path="M{x:.1f},{y:.1f} L{cx},{cy}" '
            f'dur="1.8s" begin="{i * 0.3:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="1.8s" begin="{i * 0.3:.1f}s" repeatCount="indefinite"/></circle>')
    for i, (x, y) in enumerate(pts):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{C["bg"]}" stroke="{a}" stroke-width="1.4"/>')
    out.append(
        f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="{a}">'
        f'<animate attributeName="r" values="8;17" dur="0.9s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke-opacity" values="0.7;0" dur="0.9s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="8" fill="{a}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="3" fill="{C["bg"]}"/>')
    return "".join(out)


# ---------------------------------------------------------------- WARDEN
def shield(a: str) -> str:
    """Packages roll toward a shield; the malicious one is stopped."""
    T = 4.5
    out = []
    sh = "M52 12 L70 19 V36 C70 49 62 58 52 64 C42 58 34 49 34 36 V19 Z"
    out.append(f'<line x1="0" y1="45" x2="34" y2="45" stroke="{C["faint"]}" stroke-dasharray="2 3"/>')
    out.append(f'<path d="{sh}" fill="{a}" fill-opacity="0.10" stroke="{a}" stroke-width="1.6" stroke-linejoin="round">'
               + _anim("fill-opacity", [0.10, 0.10, 0.4, 0.10, 0.10], [0, 2.6, 2.7, 3.3, T], T) + '</path>')
    # three packages, the middle one malicious
    for k, bad in enumerate((False, True, False)):
        s = k * 1.5
        arr = s + 1.1
        col = C["red"] if bad else C["soft"]
        s = max(s, 0.001)
        xs = [0, 0, 26, 15 if bad else 42, 0]  # good ones enter the shield, the bad one bounces off
        xt = [0, s, arr, arr + 0.35, T]
        op_v = [0, 0, 1, 1, 0, 0]
        ot = [0, s, s + 0.15, arr, arr + 0.35, T]
        out.append(
            f'<rect x="0" y="40" width="9" height="9" rx="1.5" fill="{col}" fill-opacity="0.85" opacity="0">'
            + _anim("x", xs, xt, T) + _anim("opacity", op_v, ot, T) + '</rect>')
    # verdict marks inside the shield
    tick = f'<path d="M45 37 L50 42 L59 31" fill="none" stroke="{a}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
    out.append(tick + _anim("opacity", [0, 1, 0, 0, 1, 0], [0, 1.1, 1.55, 4.1, 4.1001, T], T, 'calcMode="discrete"') + '</path>')
    cross = f'<path d="M47 31 L57 41 M57 31 L47 41" fill="none" stroke="{C["red"]}" stroke-width="2.4" stroke-linecap="round" opacity="0">'
    out.append(cross + _anim("opacity", [0, 1, 0, 0], [0, 2.6, 3.3, T], T, 'calcMode="discrete"') + '</path>')
    return "".join(out)


# ---------------------------------------------------------------- NIKASHA
def magnifier(a: str) -> str:
    """A lens reads a report line by line; each checked line turns accent."""
    T = 6.0
    per = 0.75
    lines = [(20, 17, 30), (20, 24, 26), (20, 31, 32), (20, 38, 22), (20, 45, 30), (20, 52, 18)]
    out = [f'<rect x="12" y="8" width="44" height="56" rx="4" fill="{C["bg"]}" stroke="{C["dim"]}" stroke-width="1.2"/>']
    for i, (x, y, L) in enumerate(lines):
        out.append(f'<line x1="{x}" y1="{y}" x2="{x + L}" y2="{y}" stroke="{C["faint"]}" stroke-width="2.6" stroke-linecap="round"/>')
        t0, t1 = i * per, (i + 1) * per
        out.append(
            f'<line x1="{x}" y1="{y}" x2="{x + L}" y2="{y}" stroke="{a}" stroke-width="2.6" stroke-linecap="round" '
            f'stroke-dasharray="{L} {L}" stroke-dashoffset="0">'
            + _anim("stroke-dashoffset", [L, L, 0, 0, L], [0, t0 + 0.001, t1, T - 0.35, T], T) + '</line>')
    # lens path: sweeps each line left to right
    vals, ts = [], []
    for i, (x, y, L) in enumerate(lines):
        vals += [f"{x - 2} {y - 2}", f"{x + L + 2} {y - 2}"]
        ts += [i * per + 0.001 if i else 0, (i + 1) * per - 0.02]
    vals += [f"{lines[-1][0] + lines[-1][2] + 2} {lines[-1][1] - 2}", f"{lines[0][0] - 2} {lines[0][1] - 2}"]
    ts += [T - 0.35, T]
    out.append(
        f'<g><circle cx="0" cy="0" r="7" fill="{a}" fill-opacity="0.12" stroke="{a}" stroke-width="2"/>'
        f'<line x1="5" y1="5" x2="11" y2="11" stroke="{a}" stroke-width="3" stroke-linecap="round"/>'
        f'<animateTransform attributeName="transform" type="translate" values="{";".join(vals)}" '
        f'keyTimes="{_kt(ts, T)}" dur="{T}s" repeatCount="indefinite"/></g>')
    # verdict badge once every line is checked
    done = len(lines) * per
    out.append(
        f'<g opacity="0"><circle cx="58" cy="60" r="8" fill="{a}"/>'
        f'<path d="M54.5 60 L57.2 62.6 L61.8 57.4" fill="none" stroke="{C["bg"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        + _anim("opacity", [0, 0, 1, 1, 0], [0, done, done + 0.15, T - 0.35, T], T) + '</g>')
    return "".join(out)


# ---------------------------------------------------------------- AFTERLOCK
def padlock(a: str) -> str:
    """Access paths light up, the lock snaps shut, the paths go dark."""
    T = 4.4
    cx, cy = 38, 50
    nodes = [(8, 12), (68, 12), (8, 70), (68, 70)]
    out = []
    for i, (x, y) in enumerate(nodes):
        out.append(
            f'<line x1="{x}" y1="{y}" x2="{cx}" y2="{cy}" stroke="{C["red"]}" stroke-width="1.3" stroke-dasharray="3 3" opacity="0">'
            + _anim("opacity", [0.8, 0.8, 0, 0, 0.8], [0, 1.5, 1.9, T - 0.4, T], T)
            + _anim("stroke-dashoffset", [0, -12], [0, T], T) + '</line>')
        out.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{C["bg"]}" stroke="{C["dim"]}" stroke-width="1.2"/>')
    # shackle: up (open) -> drops shut at 1.3s -> reopens at the end
    out.append(
        f'<path d="M30 42 V33 a8 8 0 0 1 16 0 V42" fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round">'
        f'<animateTransform attributeName="transform" type="translate" values="0 -7;0 -7;0 0;0 0;0 -7" '
        f'keyTimes="{_kt([0, 1.15, 1.35, T - 0.45, T], T)}" dur="{T}s" repeatCount="indefinite"/></path>')
    out.append(f'<rect x="24" y="41" width="28" height="22" rx="4" fill="{C["bg"]}" stroke="{a}" stroke-width="1.8"/>')
    out.append(f'<rect x="24" y="41" width="28" height="22" rx="4" fill="{a}" fill-opacity="0.12">'
               + _anim("fill-opacity", [0.12, 0.12, 0.45, 0.12, 0.12], [0, 1.35, 1.45, 2.2, T], T) + '</rect>')
    out.append(f'<circle cx="{cx}" cy="50" r="2.6" fill="{a}"/><rect x="37" y="51" width="2" height="6" rx="1" fill="{a}"/>')
    out.append(
        f'<circle cx="{cx}" cy="52" r="16" fill="none" stroke="{a}" stroke-width="1.4" opacity="0">'
        + _anim("r", [16, 16, 30, 30], [0, 1.35, 2.0, T], T)
        + _anim("opacity", [0, 0, 0.8, 0, 0], [0, 1.35, 1.36, 2.0, T], T) + '</circle>')
    return f'<g>{"".join(out)}</g>'


# ---------------------------------------------------------------- ANVIL
def telemetry(a: str) -> str:
    """Telemetry scrolls past a rule; every spike that crosses it is caught."""
    P, v = 38.0, 19.0  # period (px) and scroll speed (px/s): one spike per 2 s
    base, peak = 46, 16
    d = [f"M0 {base}"]
    for k in range(6):
        x0 = k * P
        d.append(f"L{x0 + 4:.1f} {base - 3}")
        d.append(f"L{x0 + 9:.1f} {base - 2}")
        d.append(f"L{x0 + 13:.1f} {base + 1}")
        d.append(f"L{x0 + 17:.1f} {base}")
        d.append(f"L{x0 + 19:.1f} {peak}")
        d.append(f"L{x0 + 21:.1f} {base + 7}")
        d.append(f"L{x0 + 24:.1f} {base}")
        d.append(f"L{x0 + 31:.1f} {base - 1}")
        d.append(f"L{x0 + P:.1f} {base}")
    path = " ".join(d)
    dur = P / v
    out = [
        f'<defs><clipPath id="m-tel"><rect x="0" y="6" width="{S}" height="60" rx="4"/></clipPath></defs>',
        f'<rect x="0.5" y="6.5" width="{S - 1}" height="59" rx="4" fill="{a}" fill-opacity="0.04" stroke="{C["faint"]}"/>',
    ]
    for gy in (21, 36, 51):
        out.append(f'<line x1="1" y1="{gy}" x2="{S - 1}" y2="{gy}" stroke="{C["faint"]}" stroke-opacity="0.6" stroke-dasharray="1 3"/>')
    out.append(f'<line x1="38" y1="8" x2="38" y2="64" stroke="{a}" stroke-opacity="0.45" stroke-dasharray="2 2"/>')
    out.append(
        f'<g clip-path="url(#m-tel)"><path d="{path}" fill="none" stroke="{a}" stroke-width="1.6" stroke-linejoin="round">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{-P} 0" dur="{dur}s" repeatCount="indefinite"/></path></g>')
    # the spike reaches the rule half-way through each period
    out.append(
        f'<circle cx="38" cy="{peak}" r="3" fill="none" stroke="{a}" stroke-width="1.5" opacity="0">'
        f'<animate attributeName="r" values="3;11;11" keyTimes="0;0.4;1" dur="{dur}s" begin="{dur / 2:.2f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0;0" keyTimes="0;0.4;1" dur="{dur}s" begin="{dur / 2:.2f}s" repeatCount="indefinite"/></circle>'
        f'<path d="M34 9 L38 13 L42 9" fill="none" stroke="{a}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" opacity="0.4">'
        f'<animate attributeName="opacity" values="1;0.4;0.4" keyTimes="0;0.3;1" dur="{dur}s" begin="{dur / 2:.2f}s" repeatCount="indefinite"/></path>')
    return "".join(out)


# ---------------------------------------------------------------- SLUICE
def gate(a: str) -> str:
    """Values flow down a channel; the labelled (tainted) one stops at the gate."""
    T = 3.2
    y, gx = 38, 48
    out = [
        f'<line x1="2" y1="{y - 12}" x2="{S - 2}" y2="{y - 12}" stroke="{C["faint"]}" stroke-width="1.4"/>',
        f'<line x1="2" y1="{y + 12}" x2="{S - 2}" y2="{y + 12}" stroke="{C["faint"]}" stroke-width="1.4"/>',
    ]
    # the gate: two posts and a scanning beam, flashing red when it blocks
    out.append(
        f'<line x1="{gx}" y1="{y - 12}" x2="{gx}" y2="{y + 12}" stroke="{a}" stroke-width="1.6" stroke-dasharray="2 2.5">'
        + _anim("stroke", [a, a, C["red"], a, a], [0, T / 4 + T / 2, T / 4 + T / 2 + 0.02, T / 4 + T / 2 + 0.5, T], T, 'calcMode="discrete"')
        + _anim("stroke-dashoffset", [0, -9], [0, T], T) + '</line>')
    for py in (y - 16, y + 12):
        out.append(f'<rect x="{gx - 3}" y="{py}" width="6" height="4" rx="1" fill="{a}"/>')
    # four values per cycle; the second is tainted
    for k in range(4):
        b = k * T / 4
        if k == 1:
            out.append(
                f'<g opacity="0"><circle cx="0" cy="{y}" r="3.4" fill="{C["red"]}"/>'
                f'<circle cx="0" cy="{y}" r="6" fill="none" stroke="{C["red"]}" stroke-opacity="0.7" stroke-dasharray="2 2"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;{gx - 8} 0;{gx - 8} 0" '
                f'keyTimes="0;0.5;1" dur="{T}s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.08;0.55;0.75;1" dur="{T}s" begin="{b:.2f}s" repeatCount="indefinite"/></g>')
        else:
            out.append(
                f'<circle cx="0" cy="{y}" r="3" fill="{a}" opacity="0">'
                f'<animate attributeName="cx" values="0;{S}" dur="{T}s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{T}s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


# ---------------------------------------------------------------- SCHEDULER
def sort_bars(a: str) -> str:
    """A job queue shuffles, then settles ranked by size: the negative result."""
    T = 5.0
    hs = [30, 12, 46, 20, 38, 8]
    order = sorted(range(len(hs)), key=lambda i: hs[i])  # ascending
    slot = {i: order.index(i) for i in range(len(hs))}
    out = [f'<line x1="4" y1="64.5" x2="72" y2="64.5" stroke="{C["faint"]}"/>']
    ks = "0 0 1 1;.5 0 .2 1;0 0 1 1;.5 0 .2 1"
    ts = [0, 1.2, 2.1, 3.9, T]
    for i, h in enumerate(hs):
        x = 6 + i * 11
        dx = (slot[i] - i) * 11
        out.append(
            f'<rect x="{x}" y="{64 - h}" width="8" height="{h}" rx="1.5" fill="{a}" fill-opacity="0.25" stroke="{a}" stroke-width="1.2">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{dx} 0;{dx} 0;0 0" '
            f'keyTimes="{_kt(ts, T)}" calcMode="spline" keySplines="{ks}" dur="{T}s" repeatCount="indefinite"/>'
            + _anim("fill-opacity", [0.25, 0.25, 0.8, 0.8, 0.25], ts, T) + '</rect>')
    # dispatch pointer over the head of the queue
    out.append(f'<path d="M7 6 L13 6 L10 10 Z" fill="{a}">'
               + _anim("opacity", [0.3, 0.3, 1, 1, 0.3], ts, T) + '</path>')
    return "".join(out)


# ---------------------------------------------------------------- DOCFORGE
def page(a: str) -> str:
    """Markdown in, typeset page out; the output flips between PDF and DOCX."""
    T = 4.0
    out = [
        f'<rect x="2" y="18" width="24" height="32" rx="3" fill="{C["bg"]}" stroke="{C["dim"]}" stroke-width="1.2"/>',
        f'<text x="6" y="30" font-size="9" font-weight="800" fill="{C["dim"]}">#</text>',
        f'<line x1="13" y1="27" x2="22" y2="27" stroke="{C["faint"]}" stroke-width="2" stroke-linecap="round"/>',
        f'<line x1="6" y1="35" x2="22" y2="35" stroke="{C["faint"]}" stroke-width="2" stroke-linecap="round"/>',
        f'<line x1="6" y1="41" x2="18" y2="41" stroke="{C["faint"]}" stroke-width="2" stroke-linecap="round"/>',
    ]
    for k in range(3):  # chevrons streaming right
        out.append(
            f'<path d="M0 30 L4 34 L0 38" fill="none" stroke="{a}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="28 0;40 0" dur="1.2s" begin="{k * 0.4:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;0" dur="1.2s" begin="{k * 0.4:.1f}s" repeatCount="indefinite"/></path>')
    out.append(f'<rect x="46" y="8" width="28" height="42" rx="3" fill="{C["bg"]}" stroke="{a}" stroke-width="1.4"/>')
    rows = [(50, 15, 16, 2.6), (50, 22, 20, 1.6), (50, 27, 20, 1.6), (50, 32, 14, 1.6), (50, 38, 20, 1.6), (50, 43, 12, 1.6)]
    for i, (x, y, L, w) in enumerate(rows):
        t0 = 0.3 + i * 0.3
        out.append(
            f'<line x1="{x}" y1="{y}" x2="{x + L}" y2="{y}" stroke="{a if i == 0 else C["soft"]}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-dasharray="{L} {L}" stroke-dashoffset="0" stroke-opacity="{1 if i == 0 else 0.7}">'
            + _anim("stroke-dashoffset", [L, L, 0, 0, L], [0, t0, t0 + 0.25, T - 0.3, T], T) + '</line>')
    # output format label, alternating each cycle
    for j, lab in enumerate(("PDF", "DOCX")):
        out.append(
            f'<text x="60" y="64" font-size="9" font-weight="800" text-anchor="middle" fill="{a}" opacity="{1 if j == 0 else 0}">{lab}'
            f'<animate attributeName="opacity" values="{"1;0" if j == 0 else "0;1"}" keyTimes="0;0.5" calcMode="discrete" dur="{2 * T}s" repeatCount="indefinite"/></text>')
    return "".join(out)


# ---------------------------------------------------------------- FILLWRIGHT
def form(a: str) -> str:
    """A form fills itself field by field, locally; nothing is submitted."""
    T = 4.6
    fields = [(12, 40), (32, 30), (52, 46)]
    out = []
    for i, (y, L) in enumerate(fields):
        t0 = 0.4 + i * 0.85
        t1 = t0 + 0.55
        out.append(
            f'<rect x="6" y="{y}" width="64" height="14" rx="3.5" fill="{C["bg"]}" stroke="{C["faint"]}" stroke-width="1.2">'
            + _anim("stroke", [C["faint"], a, C["faint"], C["faint"]], [0, t0, t1 + 0.25, T], T, 'calcMode="discrete"') + '</rect>')
        out.append(
            f'<rect x="11" y="{y + 5}" width="{L}" height="4" rx="2" fill="{a}" fill-opacity="0.85">'
            + _anim("width", [0, 0, L, L, 0], [0, t0, t1, T - 0.02, T], T)
            + _anim("opacity", [1, 1, 0, 1], [0, T - 0.35, T - 0.02, T], T) + '</rect>')
        # tick at the end of each field once it's filled
        out.append(
            f'<path d="M60 {y + 7} L62.5 {y + 9.5} L66 {y + 4.5}" fill="none" stroke="{a}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
            + _anim("opacity", [0, 0, 1, 1, 0], [0, t1, t1 + 0.1, T - 0.35, T], T) + '</path>')
    # caret hops between fields as it types
    cx, cts = [f"11 {fields[0][0] + 3}"], [0.0]
    for i, (y, L) in enumerate(fields):
        t0 = 0.4 + i * 0.85
        cx += [f"{11} {y + 3}", f"{11 + L + 1} {y + 3}"]
        cts += [t0, t0 + 0.55]
    cx += [f"{11 + fields[-1][1] + 1} {fields[-1][0] + 3}", f"11 {fields[0][0] + 3}"]
    cts += [T - 0.35, T]
    out.append(
        f'<rect x="0" y="0" width="1.6" height="8" fill="{C["text"]}">'
        f'<animateTransform attributeName="transform" type="translate" values="{";".join(cx)}" keyTimes="{_kt(cts, T)}" '
        f'dur="{T}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" calcMode="discrete" dur="0.7s" repeatCount="indefinite"/></rect>')
    return "".join(out)


# ---------------------------------------------------------------- FEELSLIKE
def building(a: str) -> str:
    """A building's comfort reading cools from too warm to just right."""
    T = 5.0
    out = [
        f'<path d="M6 30 L25 18 L44 30" fill="none" stroke="{a}" stroke-width="1.6" stroke-linejoin="round"/>',
        f'<rect x="9" y="30" width="32" height="34" rx="2" fill="{C["bg"]}" stroke="{a}" stroke-width="1.6"/>',
    ]
    k = 0
    for r in range(3):
        for c in range(3):
            x, y = 14 + c * 9, 35 + r * 9
            b = (k * 0.71) % T
            out.append(
                f'<rect x="{x}" y="{y}" width="5" height="5" rx="1" fill="{a}" fill-opacity="0.2">'
                f'<animate attributeName="fill-opacity" values="0.2;0.85;0.2" keyTimes="0;0.15;1" dur="{T}s" begin="{b:.2f}s" repeatCount="indefinite"/></rect>')
            k += 1
    # airflow: three wisps drifting off the roof
    for i in range(3):
        y = 8 + i * 5
        out.append(
            f'<path d="M0 {y} q3 -2.5 6 0 t6 0" fill="none" stroke="{C["cyan"]}" stroke-width="1.2" stroke-linecap="round" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="10 0;30 0" dur="2.4s" begin="{i * 0.8:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.8;0" dur="2.4s" begin="{i * 0.8:.1f}s" repeatCount="indefinite"/></path>')
    # thermometer: warm (amber, high) -> comfortable (cyan, lower)
    tx, top, bot = 58, 12, 56
    ts = [0, 1.0, 3.0, 4.5, T]
    hv = [34, 34, 18, 18, 34]
    yv = [bot - h for h in hv]
    out.append(f'<rect x="{tx - 4}" y="{top}" width="8" height="{bot - top + 2}" rx="4" fill="{C["bg"]}" stroke="{C["dim"]}" stroke-width="1.2"/>')
    out.append(
        f'<rect x="{tx - 2}" y="{bot - 18}" width="4" height="18" rx="2" fill="{C["cyan"]}">'
        + _anim("height", hv, ts, T) + _anim("y", yv, ts, T)
        + _anim("fill", [C["amber"], C["amber"], C["cyan"], C["cyan"], C["amber"]], ts, T) + '</rect>')
    out.append(
        f'<circle cx="{tx}" cy="{bot + 5}" r="6" fill="{C["cyan"]}" stroke="{C["bg"]}" stroke-width="1.5">'
        + _anim("fill", [C["amber"], C["amber"], C["cyan"], C["cyan"], C["amber"]], ts, T) + '</circle>')
    for i, yy in enumerate((20, 30, 40)):
        out.append(f'<line x1="{tx + 6}" y1="{yy}" x2="{tx + 9}" y2="{yy}" stroke="{C["dim"]}"/>')
    return "".join(out)


MOTIFS = {
    "graph": graph, "shield": shield, "magnifier": magnifier, "padlock": padlock,
    "telemetry": telemetry, "gate": gate, "sort": sort_bars, "page": page,
    "form": form, "building": building,
}
_GLYPHS = {"page": "#PDFDOCX"}


def draw(name: str | None, accent: str) -> str:
    fn = MOTIFS.get(name or "")
    return fn(accent) if fn else ""


def glyphs(name: str | None) -> str:
    return _GLYPHS.get(name or "", "")
