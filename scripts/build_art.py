"""Hand-built animated art for the profile README.

Run:  python scripts/build_art.py
Writes assets/: hero, taglines (self-hosted typing banner), buttons/*, toolchain,
constellation (THROUGHLINE map), trophies and footer.

Output is deterministic (fixed seeds, font timestamps pinned), so the workflow
can rebuild it on every run and only commits when the copy below changes.
Everything is SMIL: no JavaScript, no external requests, and the resting frame
of every animation is the finished picture.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from svgkit import C, CHAR_W, NOISE, appear, beam, counter, cursor, esc, reveal, scramble, sheen, svg_doc, typed, window

OUT = Path(__file__).resolve().parent.parent / "assets"

NAME = "RAKSHIT RAMESHBABU"
ROLE = "Software & Security Engineer"
SUB = "B.Tech CSE (Cyber Security) @ VIT Chennai  ·  Chennai, IN"
FETCH = [
    ("focus", "detection eng · DFIR · supply chain · agent security"),
    ("stack", "Python · TypeScript · Go · C · SQL · Rego"),
    ("ethos", "evidence-first: every number reruns from one command"),
    ("cgpa", "9.07 / 10"),
    ("status", "open to internships & full-time roles"),
]
# Radar blips: (label, angle in degrees clockwise from +x, radius)
BLIPS = [
    ("warden", 30, 100),
    ("anvil", 72, 64),
    ("rootline", 118, 128),
    ("nikasha", 158, 86),
    ("afterlock", 205, 132),
    ("sluice", 246, 58),
    ("dragnet", 292, 112),
    ("vitrine", 334, 80),
]


def hero() -> str:
    W, H = 1000, 430
    parts: list[str] = [window(W, H, "rakshit@rakshit-737: ~ — zsh", "h")]
    x0 = 32
    fs = 15

    # moving scan beam
    parts.append(f"""
<defs>
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['green']}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{C['green']}" stop-opacity="0.06"/>
    <stop offset="1" stop-color="{C['green']}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect x="1" y="35" width="{W-2}" height="70" fill="url(#beam)">
  <animateTransform attributeName="transform" type="translate" values="0 -80;0 {H}" dur="7s" repeatCount="indefinite"/>
</rect>""")

    t = 0.4
    # $ whoami
    parts.append(f'<text x="{x0}" y="72" font-size="{fs}" fill="{C["green"]}" font-weight="700">❯</text>')
    s, t = typed(x0 + 2 * fs * CHAR_W, 72, "whoami", fs, t, "t1", fill=C["soft"])
    parts.append(s)
    t += 0.25

    # name: decrypts letter by letter, then a chromatic glitch every few seconds
    ns, ny = 44, 128
    name_svg, name_end = scramble(x0, ny, NAME, ns, t, C["text"], weight=800, frames=9, fps=26,
                                  stagger=0.05, seed=737, noise_fill=C["green"])
    gb = f"{name_end + 1.2:.2f}s"
    glitch_kt = "0;0.90;0.905;0.92;0.935;0.95;1"
    name_layers = f"""
<g>
  <text x="{x0}" y="{ny}" font-size="{ns}" font-weight="800" fill="{C['cyan']}" opacity="0">{esc(NAME)}
    <animate attributeName="opacity" values="0;0;0.85;0;0.85;0;0" keyTimes="{glitch_kt}" calcMode="discrete" dur="5s" begin="{gb}" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 0;-4 0;3 -1;-3 1;0 0;0 0" keyTimes="{glitch_kt}" calcMode="discrete" dur="5s" begin="{gb}" repeatCount="indefinite"/>
  </text>
  <text x="{x0}" y="{ny}" font-size="{ns}" font-weight="800" fill="{C['magenta']}" opacity="0">{esc(NAME)}
    <animate attributeName="opacity" values="0;0;0.8;0;0.8;0;0" keyTimes="{glitch_kt}" calcMode="discrete" dur="5s" begin="{gb}" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 0;4 1;-3 0;3 -1;0 0;0 0" keyTimes="{glitch_kt}" calcMode="discrete" dur="5s" begin="{gb}" repeatCount="indefinite"/>
  </text>
  {name_svg}
</g>"""
    parts.append(name_layers)
    # a scan line that wipes across the name as it locks
    parts.append(
        f'<rect x="{x0 - 6}" y="{ny - ns * 0.86:.1f}" width="3" height="{ns * 1.05:.1f}" fill="{C["green"]}" opacity="0">'
        f'<animate attributeName="x" values="{x0 - 6};{x0 - 6};{x0 + len(NAME) * ns * CHAR_W + 6:.1f}" '
        f'keyTimes="0;{t / name_end:.4f};1" dur="{name_end:.3f}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0;0;0.9;0" keyTimes="0;{t / name_end:.4f};0.97;1" dur="{name_end:.3f}s" fill="freeze"/>'
        f'</rect>')
    t = name_end - 0.25
    parts.append(appear(
        f'<text x="{x0}" y="162" font-size="17" font-weight="700" fill="{C["green"]}">{esc(ROLE)}</text>'
        f'<text x="{x0}" y="187" font-size="14" fill="{C["dim"]}">{esc(SUB)}</text>',
        t + 0.25))
    t += 0.7

    # $ neofetch --profile
    parts.append(appear(
        f'<text x="{x0}" y="226" font-size="{fs}" fill="{C["green"]}" font-weight="700">❯</text>', t, 0.1))
    s, t = typed(x0 + 2 * fs * CHAR_W, 226, "neofetch --profile", fs, t, "t2", fill=C["soft"])
    parts.append(s)
    t += 0.2
    y = 256
    for i, (k, v) in enumerate(FETCH):
        row = (
            f'<text x="{x0}" y="{y}" font-size="14" font-weight="700" fill="{C["cyan"]}">{esc(k)}</text>'
            f'<text x="{x0 + 78}" y="{y}" font-size="14" fill="{C["dim"]}">:</text>'
            f'<text x="{x0 + 96}" y="{y}" font-size="14" fill="{C["soft"]}">{esc(v)}</text>'
        )
        parts.append(appear(row, t + i * 0.12, 0.2))
        y += 24
    t += len(FETCH) * 0.12 + 0.15
    # neofetch colour blocks
    blocks = [C["bg2"], C["red"], C["ok"], C["amber"], C["cyan"], C["purple"], C["magenta"], C["soft"]]
    bl = "".join(
        f'<rect x="{x0 + 96 + i*26}" y="{y-8}" width="22" height="12" rx="2" fill="{c}" stroke="{C["border"]}"/>'
        for i, c in enumerate(blocks))
    parts.append(appear(bl, t, 0.2))
    t += 0.3
    # final prompt + cursor
    parts.append(appear(
        f'<text x="{x0}" y="{y+36}" font-size="{fs}" fill="{C["green"]}" font-weight="700">❯</text>', t, 0.1))
    parts.append(cursor(x0 + 2 * fs * CHAR_W, y + 36, fs, t))

    # ---- radar -----------------------------------------------------------
    cx, cy, R, T = 832, 236, 150, 6.0
    rad = ['<g>']
    rad.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{C["green"]}" fill-opacity="0.03" stroke="{C["green"]}" stroke-opacity="0.35"/>')
    for rr in (R * 2 / 3, R / 3):
        rad.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="{C["green"]}" stroke-opacity="0.18" stroke-dasharray="3 5"/>')
    rad.append(f'<line x1="{cx-R}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{C["green"]}" stroke-opacity="0.15"/>')
    rad.append(f'<line x1="{cx}" y1="{cy-R}" x2="{cx}" y2="{cy+R}" stroke="{C["green"]}" stroke-opacity="0.15"/>')
    for deg in range(0, 360, 10):
        a = math.radians(deg)
        r1 = R - (8 if deg % 30 == 0 else 4)
        rad.append(
            f'<line x1="{cx + r1*math.cos(a):.1f}" y1="{cy + r1*math.sin(a):.1f}" '
            f'x2="{cx + R*math.cos(a):.1f}" y2="{cy + R*math.sin(a):.1f}" stroke="{C["green"]}" stroke-opacity="0.4"/>')
    # sweep: trailing wedges (behind the leading edge at 0 deg)
    sweep = [f'<g>']
    steps = 18
    for i in range(steps):
        a1 = math.radians(-50 + i * (50 / steps))
        a2 = math.radians(-50 + (i + 1) * (50 / steps))
        op = 0.28 * ((i + 1) / steps) ** 2
        sweep.append(
            f'<path d="M{cx} {cy} L{cx + R*math.cos(a1):.2f} {cy + R*math.sin(a1):.2f} '
            f'A{R} {R} 0 0 1 {cx + R*math.cos(a2):.2f} {cy + R*math.sin(a2):.2f} Z" '
            f'fill="{C["green"]}" fill-opacity="{op:.3f}"/>')
    sweep.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{C["green"]}" stroke-width="1.6" stroke-opacity="0.9"/>')
    sweep.append(
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
        f'to="360 {cx} {cy}" dur="{T}s" repeatCount="indefinite"/></g>')
    rad.append("".join(sweep))
    for label, deg, r in BLIPS:
        a = math.radians(deg)
        bx, by = cx + r * math.cos(a), cy + r * math.sin(a)
        off = deg / 360 * T
        anchor = "start" if math.cos(a) >= -0.2 else "end"
        lx = bx + (9 if anchor == "start" else -9)
        rad.append(
            f'<g opacity="0.3"><circle cx="{bx:.1f}" cy="{by:.1f}" r="3.2" fill="{C["green"]}"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3" fill="none" stroke="{C["green"]}" stroke-opacity="0">'
            f'<animate attributeName="r" values="3;12;12" keyTimes="0;0.2;1" dur="{T}s" begin="{off:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="0.9;0;0" keyTimes="0;0.2;1" dur="{T}s" begin="{off:.2f}s" repeatCount="indefinite"/>'
            f'</circle>'
            f'<text x="{lx:.1f}" y="{by+4:.1f}" font-size="11.5" text-anchor="{anchor}" fill="{C["green"]}">{esc(label)}</text>'
            f'<animate attributeName="opacity" values="1;0.3" dur="{T}s" begin="{off:.2f}s" repeatCount="indefinite"/></g>')
    rad.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{C["green"]}"/>')
    rad.append(f'<text x="{cx}" y="{cy-R-10}" font-size="11" text-anchor="middle" fill="{C["dim"]}" letter-spacing="2">SWEEP // PUBLIC REPOS</text>')
    rad.append(reveal(0.8, 0.8) + '</g>')
    parts.append("".join(rad))

    body = "\n".join(parts)
    used = "".join([NAME, ROLE, SUB, "".join(k + v for k, v in FETCH), "".join(b[0] for b in BLIPS),
                    "❯whoami neofetch --profile: rakshit@rakshit-737: ~ — zsh SWEEP // PUBLIC REPOS", NOISE])
    return svg_doc(W, H, body, "", "Rakshit Rameshbabu — Software & Security Engineer", used)


def footer() -> str:
    W, H = 1000, 128
    parts = [window(W, H, "session — closing", "f")]
    fs = 14.5
    parts.append(f'<text x="32" y="68" font-size="{fs}" fill="{C["green"]}" font-weight="700">❯</text>')
    s, t = typed(32 + 2 * fs * CHAR_W, 68, "exit", fs, 0.6, "ft1", fill=C["soft"])
    parts.append(s)
    msg = "[process completed]  thanks for reading. every claim above links to its evidence."
    parts.append(appear(f'<text x="32" y="96" font-size="13" fill="{C["dim"]}">{esc(msg)}</text>', t + 0.2))
    parts.append(cursor(32 + (len(msg) + 1) * 13 * CHAR_W, 96, 13, t + 0.4, C["dim"]))
    # heartbeat trace along the right side of the first row
    x, pts, coords = 640, [], []
    base = 60
    pattern = [0, 0, 0, -3, 3, 0, 0, -20, 16, -5, 0, 0, 0, 0]
    while x < W - 32:
        for dy in pattern:
            coords.append((x, base + dy))
            x += 6
            if x >= W - 32:
                break
    L = sum(math.dist(coords[i], coords[i + 1]) for i in range(len(coords) - 1))
    path = " ".join(f"{a:.0f},{b}" for a, b in coords)
    parts.append(
        f'<polyline points="{path}" fill="none" stroke="{C["green"]}" stroke-width="1.6" '
        f'stroke-linejoin="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}" opacity="0.85">'
        f'<animate attributeName="stroke-dashoffset" values="{L:.0f};0;{-L:.0f}" dur="4s" repeatCount="indefinite"/></polyline>')
    used = "❯exit" + msg + "session — closing"
    return svg_doc(W, H, "\n".join(parts), "", "End of profile", used)


TOOLCHAIN = [
    ("detection", ["Sigma", "YARA", "MITRE ATT&CK", "Sysmon", "EVTX", "Atomic Red Team", "OTRF datasets"]),
    ("forensics", ["Volatility 3", "plaso", "auditd", "eBPF / bpftrace", "strace", "provenance graphs"]),
    ("cloud & supply", ["Trivy", "Syft SBOM", "OSV", "OPA / Rego", "Tetragon", "kind", "SARIF"]),
    ("attack surface", ["BloodHound", "nmap", "OpenVAS", "NVD · EPSS · KEV", "Neo4j", "min-cut"]),
    ("ml & eval", ["XGBoost", "LightGBM", "SHAP", "scikit-learn", "PyTorch", "TOST / bootstrap"]),
    ("agents & llm", ["LangGraph", "MCP", "information-flow labels", "RAG", "FastAPI"]),
]


def toolchain() -> str:
    W = 1000
    fs = 13
    row_h = 40
    H = 35 + 58 + len(TOOLCHAIN) * row_h + 20
    parts = [window(W, H, "~/toolchain — security tooling I have shipped code against", "tc")]
    parts.append(f'<text x="32" y="70" font-size="14.5" fill="{C["green"]}" font-weight="700">❯</text>')
    s, t = typed(32 + 2 * 14.5 * CHAR_W, 70, "ls -1 /opt/toolchain/*", 14.5, 0.3, "tct", fill=C["soft"])
    parts.append(s)
    y = 110
    rnd = random.Random(1337)
    for i, (cat, tools) in enumerate(TOOLCHAIN):
        row = [f'<text x="32" y="{y}" font-size="{fs}" font-weight="700" fill="{C["cyan"]}">{esc(cat)}</text>']
        x = 32 + 16 * fs * CHAR_W
        for tool in tools:
            w = len(tool) * fs * CHAR_W + 18
            if x + w > W - 28:
                break
            # each chip lights up briefly at a random moment of a 14 s cycle,
            # like processes waking on a busy box
            b = rnd.uniform(2.5, 16.5)
            flash = f'keyTimes="0;0.03;0.10;1" dur="14s" begin="{b:.2f}s" repeatCount="indefinite"'
            row.append(
                f'<rect x="{x:.1f}" y="{y-16}" width="{w:.1f}" height="23" rx="5" fill="{C["green"]}" '
                f'fill-opacity="0.06" stroke="{C["green"]}" stroke-opacity="0.35">'
                f'<animate attributeName="stroke-opacity" values="0.35;1;0.35;0.35" {flash}/>'
                f'<animate attributeName="fill-opacity" values="0.06;0.2;0.06;0.06" {flash}/></rect>'
                f'<text x="{x+9:.1f}" y="{y}" font-size="{fs}" fill="{C["soft"]}">{esc(tool)}</text>')
            x += w + 8
        parts.append(appear("".join(row), t + 0.1 + i * 0.12))
        y += row_h
    used = "".join(c + "".join(ts) for c, ts in TOOLCHAIN) + "❯ls -1 /opt/toolchain/* ~/toolchain — security tooling I have shipped code against"
    return svg_doc(W, H, "\n".join(parts), "", "Security toolchain", used)


DOMAINS = {
    "detection": C["green"],
    "DFIR": C["cyan"],
    "intel": C["purple"],
    "malware": C["magenta"],
    "network": C["coral"],
    "infra & supply chain": C["amber"],
}
ENGINES = [  # (name, domain, flow): flow "in" writes claims to the graph, "out" consumes it
    ("ANVIL", "detection", "in"), ("GAUNTLET", "detection", "out"), ("VANTAGE", "detection", "in"),
    ("REVENANT", "DFIR", "in"), ("ROOTLINE", "DFIR", "in"),
    ("DRAGNET", "intel", "in"), ("OCCAM", "intel", "in"),
    ("VITRINE", "malware", "in"), ("SPECIMEN", "malware", "in"),
    ("FEINT", "network", "in"),
    ("LINCHPIN", "infra & supply chain", "in"), ("STRATUM", "infra & supply chain", "in"),
    ("TRACEGATE", "infra & supply chain", "in"),
]


def constellation() -> str:
    W, H = 1000, 590
    cx, cy, rx, ry = 500, 318, 375, 200
    parts = [window(W, H, "throughline --map  ·  13 engines -> 1 evidence graph", "k")]
    # legend
    lx = 28
    leg = []
    for name, col in DOMAINS.items():
        leg.append(f'<circle cx="{lx+5}" cy="62" r="4.5" fill="{col}"/>'
                   f'<text x="{lx+15}" y="66" font-size="12" fill="{C["dim"]}">{esc(name)}</text>')
        lx += 15 + len(name) * 12 * CHAR_W + 22
    leg.append(f'<text x="{W-28}" y="66" font-size="12" text-anchor="end" fill="{C["dim"]}">'
               f'<tspan fill="{C["amber"]}">&#8592;</tspan> consumes the graph</text>')
    parts.append(appear("".join(leg), 0.2))
    # hub ring
    hub_r = 62
    parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{hub_r+16}" fill="none" stroke="{C["green"]}" stroke-opacity="0.35" '
        f'stroke-dasharray="4 7"><animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="24s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="{hub_r+30}" fill="none" stroke="{C["green"]}" stroke-opacity="0.12"/>')
    n = len(ENGINES)
    nodes = []
    for i, (name, dom, flow) in enumerate(ENGINES):
        a = math.radians(-90 + i * 360 / n)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        col = DOMAINS[dom]
        # spoke from node edge to hub edge
        d = math.hypot(x - cx, y - cy)
        ux, uy = (cx - x) / d, (cy - y) / d
        sx, sy = x + ux * 26, y + uy * 18
        ex, ey = cx - ux * (hub_r + 2), cy - uy * (hub_r + 2)
        parts.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{col}" '
                     f'stroke-opacity="0.28" stroke-dasharray="2 5"/>')
        path = f"M{sx:.1f},{sy:.1f} L{ex:.1f},{ey:.1f}" if flow == "in" else f"M{ex:.1f},{ey:.1f} L{sx:.1f},{sy:.1f}"
        pc = col if flow == "in" else C["amber"]
        for k in range(2):
            b = (i * 0.37 + k * 1.3) % 2.6
            parts.append(
                f'<circle r="2.8" fill="{pc}"><animateMotion path="{path}" dur="2.6s" begin="{b:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.8;1" dur="2.6s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')
        bw = len(name) * 13 * CHAR_W + 24
        nodes.append(appear(
            f'<rect x="{x-bw/2:.1f}" y="{y-15:.1f}" width="{bw:.1f}" height="30" rx="7" fill="{C["bg"]}" '
            f'stroke="{col}" stroke-opacity="0.85"/>'
            f'<text x="{x:.1f}" y="{y+4.5:.1f}" font-size="13" font-weight="700" text-anchor="middle" fill="{col}">{esc(name)}</text>',
            0.3 + i * 0.06))
    parts.extend(nodes)
    # hub
    parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{hub_r}" fill="{C["bg"]}" stroke="{C["green"]}" stroke-width="1.5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{hub_r}" fill="{C["green"]}" fill-opacity="0.08">'
        f'<animate attributeName="fill-opacity" values="0.05;0.16;0.05" dur="2.6s" repeatCount="indefinite"/></circle>'
        f'<text x="{cx}" y="{cy-4}" font-size="15" font-weight="800" text-anchor="middle" fill="{C["green"]}">THROUGHLINE</text>'
        f'<text x="{cx}" y="{cy+14}" font-size="11" text-anchor="middle" fill="{C["dim"]}">evidence graph</text>'
        f'<text x="{cx}" y="{cy+28}" font-size="11" text-anchor="middle" fill="{C["dim"]}">cited · graded</text>')
    q = 'ask "how did it start, who did it, and how sure are we?"'
    parts.append(f'<text x="{cx - (len(q)+2)*13.5*CHAR_W/2:.1f}" y="{H-20}" font-size="13.5" fill="{C["green"]}" font-weight="700">❯</text>')
    s, _ = typed(cx - (len(q)+2)*13.5*CHAR_W/2 + 2*13.5*CHAR_W, H - 20, q, 13.5, 1.4, "kq", fill=C["soft"])
    parts.append(s)
    used = "".join(e[0] for e in ENGINES) + "".join(DOMAINS) + q + "❯THROUGHLINE evidence graph cited · graded consumes the graph throughline --map  ·  13 engines -> 1 evidence graph←"
    return svg_doc(W, H, "\n".join(parts), "", "THROUGHLINE: 13 security engines writing cited claims into one evidence graph", used)


# ---------------------------------------------------------------- tagline banner
# Replaces the third-party readme-typing-svg: same five lines, typed and deleted
# in a loop, served from this repo.
TAGLINES = [
    "detection-as-code, measured on real telemetry",
    "provenance graphs → root cause → blast radius",
    "static analysis that never runs the sample",
    "attribution that can say: I don't know",
    "every number regenerates from one command",
]


def _kt(pts: list[tuple[float, float]], T: float) -> tuple[str, str]:
    """(values, keyTimes) for a discrete animation from (time, value) points."""
    out, last = [], -1.0
    for t, v in pts:
        k = round(t / T, 5)
        if k <= last:
            k = round(last + 0.00001, 5)
        out.append((k, v))
        last = k
    if out[-1][0] < 1:
        out.append((1.0, out[-1][1]))
    return ";".join(f"{v:.2f}" for _, v in out), ";".join(f"{k:g}" for k, _ in out)


def taglines() -> str:
    W, H, fs = 1000, 60, 17
    cw = fs * CHAR_W
    x0, y = 28, 37
    tx = x0 + 2 * cw
    cps_t, cps_d, hold, gap = 30.0, 75.0, 2.1, 0.45
    slots, t = [], 0.35
    for line in TAGLINES:
        n = len(line)
        a, b = t, t + n / cps_t
        c = b + hold
        d = c + n / cps_d
        slots.append((a, b, c, d))
        t = d + gap
    T = t
    parts = [
        f'<defs><radialGradient id="tg-glow" cx="0%" cy="50%" r="60%">'
        f'<stop offset="0" stop-color="{C["green"]}" stop-opacity="0.12"/><stop offset="1" stop-color="{C["green"]}" stop-opacity="0"/>'
        f'</radialGradient><pattern id="tg-scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="4" height="1" fill="#ffffff" opacity="0.025"/></pattern></defs>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{C["bg"]}"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="url(#tg-glow)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="url(#tg-scan)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{C["border"]}"/>',
        f'<text x="{x0}" y="{y}" font-size="{fs}" font-weight="700" fill="{C["green"]}">❯</text>',
    ]
    cur = [(0.0, 0.0)]
    prog = []
    for i, (line, (a, b, c, d)) in enumerate(zip(TAGLINES, slots)):
        n = len(line)
        pts = [(0.0, 0.0)]
        pts += [(a + (k - 1) / cps_t, k * cw) for k in range(1, n + 1)]
        pts += [(c + (n - k) / cps_d, k * cw) for k in range(n - 1, -1, -1)]
        cur += pts[1:]
        vals, kts = _kt(pts, T)
        base = n * cw if i == 0 else 0
        parts.append(
            f'<clipPath id="tg{i}"><rect x="{tx:.2f}" y="{y - fs}" width="{base:.2f}" height="{fs * 1.6}">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kts}" calcMode="discrete" dur="{T:.3f}s" repeatCount="indefinite"/>'
            f'</rect></clipPath>'
            f'<text x="{tx:.2f}" y="{y}" font-size="{fs}" fill="{C["text"]}" clip-path="url(#tg{i})" xml:space="preserve">{esc(line)}</text>')
        # counter on the right: [i/5]
        k1, k2 = a / T, min((slots[i + 1][0] if i + 1 < len(slots) else T) / T, 1)
        parts.append(
            f'<text x="{W - 28}" y="{y - 1}" font-size="12.5" text-anchor="end" fill="{C["dim"]}" opacity="{1 if i == 0 else 0}">'
            f'taglines <tspan fill="{C["green"]}">{i + 1}</tspan>/{len(TAGLINES)}'
            f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;{k1:.5f};{k2:.5f};1" calcMode="discrete" dur="{T:.3f}s" repeatCount="indefinite"/></text>')
        prog.append((a, d))
    cvals, ckts = _kt([(t0, tx + w) for t0, w in cur], T)
    parts.append(
        f'<rect x="{tx + len(TAGLINES[0]) * cw:.2f}" y="{y - fs * 0.82:.2f}" width="{cw * 0.55:.2f}" height="{fs * 1.02:.2f}" fill="{C["green"]}">'
        f'<animate attributeName="x" values="{cvals}" keyTimes="{ckts}" calcMode="discrete" dur="{T:.3f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.05s" repeatCount="indefinite"/></rect>')
    # thin progress line along the bottom edge, one sweep per tagline
    pv, pk = [], []
    for (a, d) in prog:
        pv += ["0", "0", f"{W - 40}", "0"]
        pk += [a / T, a / T + 0.00001, d / T, d / T + 0.00001]
    pk = [0.0] + pk + [1.0]
    pv = ["0"] + pv + ["0"]
    kt = ";".join(f"{k:.5f}" for k in pk)
    parts.append(
        f'<rect x="20" y="{H - 3}" width="{W - 40}" height="1.5" rx="0.75" fill="{C["green"]}" opacity="0.35">'
        f'<animate attributeName="width" values="{";".join(pv)}" keyTimes="{kt}" dur="{T:.3f}s" repeatCount="indefinite"/></rect>')
    used = "".join(TAGLINES) + "❯ taglines 0123456789/"
    return svg_doc(W, H, "\n".join(parts), "", " · ".join(TAGLINES), used)


# ------------------------------------------------------------------ link buttons
LINKS = [  # (file stem, label, accessible title)
    ("portfolio", "PORTFOLIO", "Portfolio: rakshit-737.is-a.dev"),
    ("linkedin", "LINKEDIN", "LinkedIn: rakshit-rameshbabu"),
    ("email", "EMAIL", "Email: rakshitoffl@gmail.com"),
    ("resume", "RESUME", "Resume (PDF)"),
    ("cylab", "CYLAB", "CyLab Academy profile"),
]


def button(label: str, title: str, i: int) -> str:
    fs, h, pad = 12.5, 34, 14
    cw = fs * CHAR_W
    w = round(pad + cw + 9 + len(label) * cw + 10 + cw + pad)
    uid = f"b{i}"
    y = h / 2 + fs * 0.36
    x_label = pad + cw + 9
    body = (
        f'<defs><radialGradient id="{uid}-glow" cx="0%" cy="50%" r="75%">'
        f'<stop offset="0" stop-color="{C["green"]}" stop-opacity="0.16"/><stop offset="1" stop-color="{C["green"]}" stop-opacity="0"/>'
        f'</radialGradient></defs>'
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="{C["bg"]}"/>'
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="url(#{uid}-glow)"/>'
        + sheen(w, h, uid, 8, begin=1.0 + i * 0.22, every=6.5)
        + f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="none" stroke="{C["border"]}"/>'
        f'<text x="{pad}" y="{y:.1f}" font-size="{fs}" font-weight="700" fill="{C["green"]}">❯</text>'
        f'<text x="{x_label:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="700" fill="{C["text"]}" letter-spacing="0">{esc(label)}</text>'
        f'<text x="{w - pad - cw:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="700" fill="{C["dim"]}">↗</text>'
    )
    return svg_doc(w, h, body, "", title, label + "❯↗")


# --------------------------------------------------------------- trophies log
TROPHIES = [  # (diff marker, date, tag, event, colour)
    ("+", "2025-06-21", "FIRST PRIZE", "Cyber Secure 360 Expo 2025 · SCOPE, VIT Chennai", "amber"),
    ("+", "2026-06", "TOP 100", "FarAway Zuup Hackathon · of ~11,000 participants", "green"),
    ("+", "2026-08", "FINALS", "FeelsLike (Team Goldilocks) · digital-twin building optimizer", "magenta"),
    ("+", "2026-09-17", "RELEASE", "Warden v2.0.0 · supply-chain security platform", "cyan"),
    ("+", "2026-09-20", "RELEASE", "Fillwright v0.6.1 · privacy-first autofill extension", "cyan"),
    ("+", "2026-09-26", "RELEASE", "Nikasha v0.1.0 · PyPI, GHCR, GitHub Releases", "cyan"),
    ("!", "ongoing", "CGPA 9.07", "B.Tech CSE (Cyber Security), VIT Chennai · class of 2028", "purple"),
]


def trophies() -> str:
    W, fs, row = 1000, 13.5, 40
    cw = fs * CHAR_W
    top = 112
    H = top + (len(TROPHIES) - 1) * row + 44
    parts = [window(W, H, "~/trophies.log — tail -f", "tr")]
    parts.append(f'<text x="32" y="70" font-size="14.5" fill="{C["green"]}" font-weight="700">❯</text>')
    s, t = typed(32 + 2 * 14.5 * CHAR_W, 70, f"tail -n {len(TROPHIES)} trophies.log", 14.5, 0.3, "trt", fill=C["soft"])
    parts.append(s)
    t += 0.15
    rail_x = 58
    y_first, y_last = top - 4.5, top + (len(TROPHIES) - 1) * row - 4.5
    per = 0.28
    draw = per * (len(TROPHIES) - 1)
    # the rail draws itself downward, reaching each node as its row appears
    parts.append(
        f'<line x1="{rail_x}" y1="{y_first}" x2="{rail_x}" y2="{y_last}" stroke="{C["faint"]}" stroke-width="2"/>'
        f'<line x1="{rail_x}" y1="{y_first}" x2="{rail_x}" y2="{y_last}" stroke="{C["green"]}" stroke-width="2" '
        f'stroke-opacity="0.7" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0">'
        f'<animate attributeName="stroke-dashoffset" values="1;1;0" keyTimes="0;{t / (t + draw):.4f};1" dur="{t + draw:.3f}s" fill="freeze"/></line>')
    date_w = max(len(r[1]) for r in TROPHIES) * cw
    chip_fs = 11.5
    chip_w = max(len(r[2]) for r in TROPHIES) * chip_fs * CHAR_W + 18
    x_date = rail_x + 22
    x_chip = x_date + date_w + 18
    x_event = x_chip + chip_w + 14
    for i, (mark, date, tag, event, key) in enumerate(TROPHIES):
        col = C[key]
        y = top + i * row
        b = t + i * per
        last = i == len(TROPHIES) - 1
        mcol = C["green"] if mark == "+" else C["amber"]
        rep = 'repeatCount="indefinite"' if last else 'fill="freeze"'
        pd = 1.6 if last else 0.9
        pulse = (
            f'<circle cx="{rail_x}" cy="{y - 4.5}" r="6" fill="none" stroke="{col}">'
            f'<animate attributeName="r" values="6;16" dur="{pd}s" begin="{b:.2f}s" {rep}/>'
            f'<animate attributeName="stroke-opacity" values="0.9;0" dur="{pd}s" begin="{b:.2f}s" {rep}/></circle>')
        tw = len(tag) * chip_fs * CHAR_W + 18
        row_svg = (
            f'<text x="26" y="{y}" font-size="{fs}" font-weight="700" fill="{mcol}">{esc(mark)}</text>'
            f'<circle cx="{rail_x}" cy="{y - 4.5}" r="7" fill="{C["bg"]}" stroke="{col}" stroke-width="1.5"/>'
            f'<circle cx="{rail_x}" cy="{y - 4.5}" r="3.2" fill="{col}"/>'
            f'<text x="{x_date:.1f}" y="{y}" font-size="{fs}" fill="{C["dim"]}">{esc(date)}</text>'
            f'<rect x="{x_chip:.1f}" y="{y - 15}" width="{tw:.1f}" height="21" rx="10.5" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.6"/>'
            f'<text x="{x_chip + tw / 2:.1f}" y="{y - 0.5}" font-size="{chip_fs}" font-weight="700" text-anchor="middle" fill="{col}">{esc(tag)}</text>'
            f'<text x="{x_event:.1f}" y="{y}" font-size="{fs}" fill="{C["soft"]}">{esc(event)}</text>'
        )
        slide = (f'<g>{row_svg}<animateTransform attributeName="transform" type="translate" values="-10 0;-10 0;0 0" '
                 f'keyTimes="0;{b / (b + 0.3):.4f};1" dur="{b + 0.3:.3f}s" fill="freeze"/>{reveal(b, 0.3)}</g>')
        parts.append(slide + appear(pulse, b, 0.05))
        if last:
            parts.append(cursor(x_event + (len(event) + 1) * cw, y, fs, b + 0.4, C["dim"]))
    used = "".join("".join(r[:4]) for r in TROPHIES) + "❯tail -n 0123456789 trophies.log ~/trophies.log — tail -f+!"
    return svg_doc(W, H, "\n".join(parts), "", "trophies.log: " + " · ".join(f"{r[1]} {r[2]} {r[3]}" for r in TROPHIES), used)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero(), encoding="utf-8")
    (OUT / "footer.svg").write_text(footer(), encoding="utf-8")
    (OUT / "toolchain.svg").write_text(toolchain(), encoding="utf-8")
    (OUT / "constellation.svg").write_text(constellation(), encoding="utf-8")
    (OUT / "taglines.svg").write_text(taglines(), encoding="utf-8")
    (OUT / "trophies.svg").write_text(trophies(), encoding="utf-8")
    written = ["hero.svg", "footer.svg", "toolchain.svg", "constellation.svg", "taglines.svg", "trophies.svg"]
    (OUT / "buttons").mkdir(exist_ok=True)
    for i, (stem, label, title) in enumerate(LINKS):
        (OUT / "buttons" / f"{stem}.svg").write_text(button(label, title, i), encoding="utf-8")
        written.append(f"buttons/{stem}.svg")
    for f in written:
        print(f, (OUT / f).stat().st_size, "bytes")
