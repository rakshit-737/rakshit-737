"""Tiny SVG toolkit shared by build_art.py and build_cards.py.

Everything here is standard library + fontTools (only for font subsetting).
The fonts are embedded as base64 WOFF2 subsets, so the images render the same
on every OS even though GitHub serves them through <img> (which cannot load
external fonts).
"""
from __future__ import annotations

import base64
import random
import re
import html
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"

# JetBrains Mono: every glyph advance is 600/1000 em, so layout is exact.
CHAR_W = 0.6

FAMILY = "JBM"
FONT_STACK = f"{FAMILY}, 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

WEIGHTS = {
    400: "JetBrainsMono-Regular.ttf",
    700: "JetBrainsMono-Bold.ttf",
    800: "JetBrainsMono-ExtraBold.ttf",
}

# Console palette (dark). Every card carries its own background, so the same
# file reads well on both GitHub themes.
C = {
    "bg": "#0a0e14",
    "bg2": "#0d1117",
    "bar": "#161b22",
    "border": "#30363d",
    "text": "#e6edf3",
    "soft": "#c9d1d9",
    "dim": "#7d8590",
    "faint": "#30363d",
    "green": "#00e38c",
    "cyan": "#22d3ee",
    "magenta": "#f472b6",
    "amber": "#fbbf24",
    "red": "#ff5f56",
    "yellow": "#ffbd2e",
    "ok": "#27c93f",
    "purple": "#a78bfa",
    "coral": "#ff7b72",
}

ASCII = "".join(chr(c) for c in range(32, 127))

# Noise glyphs for scramble(): all plain ASCII, so the font subset stays small.
NOISE = "01<>/\\|=+*#%$&@?ABCDEFXYZ0123456789"


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def text_w(s: str, size: float) -> float:
    return len(s) * size * CHAR_W


def wrap(s: str, width_chars: int) -> list[str]:
    words, lines, cur = s.split(), [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width_chars:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _subset_woff2(path: Path, text: str) -> bytes | None:
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:  # pragma: no cover - fall back to system fonts
        return None
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern"]
    opts.name_IDs = []
    opts.notdef_outline = True
    font = TTFont(str(path), recalcTimestamp=False)
    sub = subset.Subsetter(options=opts)
    sub.populate(text=text + " ")
    sub.subset(font)
    buf = io.BytesIO()
    try:
        font.flavor = "woff2"
        font.save(buf)
    except Exception:  # brotli missing -> plain TTF subset still works
        font.flavor = None
        buf = io.BytesIO()
        font.save(buf)
        return b"ttf:" + buf.getvalue()
    return buf.getvalue()


def font_face(text: str, weights=(400, 700, 800)) -> str:
    """@font-face rules with only the glyphs `text` needs."""
    rules = []
    for w in weights:
        data = _subset_woff2(FONT_DIR / WEIGHTS[w], text)
        if data is None:
            continue
        if data.startswith(b"ttf:"):
            mime, fmt, data = "font/ttf", "truetype", data[4:]
        else:
            mime, fmt = "font/woff2", "woff2"
        b64 = base64.b64encode(data).decode()
        rules.append(
            f"@font-face{{font-family:{FAMILY};font-weight:{w};"
            f"src:url(data:{mime};base64,{b64}) format('{fmt}');}}"
        )
    return "\n".join(rules)


def svg_doc(w: int, h: int, body: str, css: str, title: str, used_text: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n"
        f"<style>\n{font_face(used_text)}\n"
        f"text{{font-family:{FONT_STACK};text-rendering:geometricPrecision;}}\n{css}\n</style>\n"
        f"{body}\n</svg>\n"
    )


def window(w: int, h: int, title: str, uid: str, r: int = 12, accent: str | None = None) -> str:
    """Terminal window chrome: rounded frame, title bar, traffic lights.
    `accent` tints the corner glow (defaults to the brand green)."""
    glow = accent or C["green"]
    return f"""
<defs>
  <clipPath id="{uid}-frame"><rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}"/></clipPath>
  <pattern id="{uid}-scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#ffffff" opacity="0.025"/>
  </pattern>
  <radialGradient id="{uid}-glow" cx="15%" cy="0%" r="90%">
    <stop offset="0" stop-color="{glow}" stop-opacity="0.10"/>
    <stop offset="1" stop-color="{glow}" stop-opacity="0"/>
  </radialGradient>
</defs>
<g clip-path="url(#{uid}-frame)">
  <rect width="{w}" height="{h}" fill="{C['bg']}"/>
  <rect width="{w}" height="{h}" fill="url(#{uid}-glow)"/>
  <rect width="{w}" height="34" fill="{C['bar']}"/>
  <line x1="0" y1="34.5" x2="{w}" y2="34.5" stroke="{C['border']}"/>
  <circle cx="20" cy="17" r="6" fill="{C['red']}"/>
  <circle cx="40" cy="17" r="6" fill="{C['yellow']}"/>
  <circle cx="60" cy="17" r="6" fill="{C['ok']}"/>
  <text x="{w/2}" y="22" text-anchor="middle" font-size="12.5" fill="{C['dim']}">{esc(title)}</text>
  <rect y="35" width="{w}" height="{h-35}" fill="url(#{uid}-scan)"/>
</g>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{C['border']}"/>
"""


def typed(x: float, y: float, text: str, size: float, begin: float, uid: str,
          cps: float = 32, fill: str | None = None, weight: int = 400,
          extra: str = "") -> tuple[str, float]:
    """Text that types itself in, one character at a time (SMIL, no JS).

    The resting state is the full text; the animation runs from t=0 and hides
    it until `begin`. A renderer without SMIL therefore shows finished text
    instead of an empty card. Returns (svg, end_time)."""
    n = max(len(text), 1)
    cw = size * CHAR_W
    begin = max(begin, 0.01)
    total = begin + n / cps
    values = ["0"] + [f"{i*cw:.2f}" for i in range(1, n + 1)]
    times = ["0"] + [f"{(begin + (i - 1) / cps) / total:.4f}" for i in range(1, n + 1)]
    fill_attr = f' fill="{fill}"' if fill else ""
    svg = (
        f'<clipPath id="{uid}"><rect x="{x}" y="{y-size}" width="{n*cw:.2f}" height="{size*1.5}">'
        f'<animate attributeName="width" values="{";".join(values)}" keyTimes="{";".join(times)}" '
        f'calcMode="discrete" dur="{total:.3f}s" begin="0s" fill="freeze"/>'
        f"</rect></clipPath>"
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}"{fill_attr} '
        f'clip-path="url(#{uid})" xml:space="preserve" {extra}>{esc(text)}</text>'
    )
    return svg, total


def reveal(begin: float, dur: float = 0.25, attr: str = "opacity", end_value: str = "1") -> str:
    """SMIL child that keeps an attribute at 0 until `begin`, then eases it to
    `end_value`. Without SMIL the element simply shows its resting value."""
    begin = max(begin, 0.01)
    total = begin + dur
    return (
        f'<animate attributeName="{attr}" values="0;0;{end_value}" '
        f'keyTimes="0;{begin/total:.4f};1" dur="{total:.3f}s" begin="0s" fill="freeze"/>'
    )


def appear(inner: str, begin: float, dur: float = 0.25) -> str:
    """Wrap `inner` so it fades in at `begin` seconds and stays."""
    return f"<g>{inner}{reveal(begin, dur)}</g>"


def cursor(x: float, y: float, size: float, begin: float = 0.0, color: str | None = None) -> str:
    color = color or C["green"]
    hide = f'<animate attributeName="opacity" values="0;0" dur="{begin:.3f}s" begin="0s"/>' if begin > 0 else ""
    return (
        f'<rect x="{x}" y="{y-size*0.82}" width="{size*CHAR_W}" height="{size*1.02}" fill="{color}">'
        f"{hide}"
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
        f'dur="1.05s" begin="{begin:.3f}s" repeatCount="indefinite"/></rect>'
    )


# --------------------------------------------------------------------------- motion helpers
# Every helper below keeps the finished picture as the resting state: SMIL only
# hides things until their moment. A renderer without SMIL shows the end frame.

def scramble(x: float, y: float, text: str, size: float, begin: float, fill: str,
             weight: int = 400, frames: int = 8, fps: float = 24, stagger: float = 0.045,
             seed: int = 7, extra: str = "", noise_fill: str | None = None) -> tuple[str, float]:
    """Text that decrypts in: each character flickers through noise glyphs,
    then locks to its real letter, left to right. Returns (svg, end_time)."""
    rnd = random.Random(seed)
    cw = size * CHAR_W
    step = 1 / fps
    out, end = [], begin
    common = f'y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}'
    noisy = f'y="{y}" font-size="{size}" font-weight="{weight}" fill="{noise_fill or fill}" {extra}'
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        cx = x + i * cw
        t0 = begin + i * stagger
        lock = t0 + frames * step
        end = max(end, lock)
        for k in range(frames):
            g = rnd.choice(NOISE)
            out.append(
                f'<text x="{cx:.2f}" {noisy} visibility="hidden" opacity="0.9">{esc(g)}'
                f'<set attributeName="visibility" to="visible" begin="{t0 + k*step:.3f}s" dur="{step:.3f}s"/></text>')
        out.append(f'<text x="{cx:.2f}" {common}>{esc(ch)}{reveal(lock, 0.01)}</text>')
    return "".join(out), end


_NUM = re.compile(r"^(?P<pre>[^\d]*)(?P<num>\d[\d,]*(?:\.\d+)?)(?P<suf>.*)$")


def counter(x: float, y: float, final: str, begin: float, attrs: str,
            dur: float = 1.1, frames: int = 16) -> str:
    """A number that counts up from 0 to `final` (keeps its commas, decimals,
    prefix and suffix, e.g. '3,557', '67.0%', '10d'). Non-numbers render plain."""
    m = _NUM.match(final)
    if not m:
        return f'<text x="{x}" y="{y}" {attrs}>{esc(final)}</text>'
    pre, num, suf = m["pre"], m["num"], m["suf"]
    dec = len(num.split(".")[1]) if "." in num else 0
    commas = "," in num
    val = float(num.replace(",", ""))
    step = dur / frames
    out = []
    for k in range(frames):
        p = 1 - (1 - k / frames) ** 3  # ease-out cubic
        v = val * p
        s = f"{v:,.{dec}f}" if commas else f"{v:.{dec}f}"
        out.append(
            f'<text x="{x}" y="{y}" {attrs} visibility="hidden">{esc(pre + s + suf)}'
            f'<set attributeName="visibility" to="visible" begin="{begin + k*step:.3f}s" dur="{step:.3f}s"/></text>')
    out.append(f'<text x="{x}" y="{y}" {attrs}>{esc(final)}{reveal(begin + dur, 0.01)}</text>')
    return "".join(out)


def beam(w: float, h: float, color: str, uid: str, r: float = 12, dur: float = 8.0,
         phase: float = 0.0, length: float = 16) -> str:
    """A comet of light that orbits a rounded frame (three stacked dashes make
    the tail). `phase` (0-1) desynchronises cards that sit side by side."""
    layers = [(length, 0.4, 7, True), (length * 0.55, 0.75, 3.5, True), (length * 0.3, 1.0, 2.0, False)]
    out = [f'<defs><filter id="{uid}-bl" x="-5%" y="-5%" width="110%" height="110%">'
           f'<feGaussianBlur stdDeviation="2.6"/></filter></defs><g fill="none" stroke="{color}" stroke-linecap="round">']
    for L, op, sw, blur in layers:
        o0 = -(length - L)
        flt = f' filter="url(#{uid}-bl)"' if blur else ""
        out.append(
            f'<rect x="1.2" y="1.2" width="{w-2.4}" height="{h-2.4}" rx="{r-0.7}" pathLength="100" '
            f'stroke-width="{sw}" stroke-opacity="{op}" stroke-dasharray="{L:.2f} {100-L:.2f}" '
            f'stroke-dashoffset="{o0:.2f}"{flt}>'
            f'<animate attributeName="stroke-dashoffset" values="{o0:.2f};{o0-100:.2f}" dur="{dur}s" '
            f'begin="{-phase*dur:.2f}s" repeatCount="indefinite"/></rect>')
    out.append("</g>")
    return "".join(out)


def sheen(w: float, h: float, uid: str, r: float, begin: float, every: float = 6.0) -> str:
    """A soft diagonal highlight that glides across a clipped shape now and then."""
    band = max(40.0, h * 1.4)
    travel = w + band * 2
    return (
        f'<defs><clipPath id="{uid}-c"><rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}"/></clipPath>'
        f'<linearGradient id="{uid}-g" x1="0" x2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="#ffffff" stop-opacity="0.13"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>'
        f'</linearGradient></defs>'
        f'<g clip-path="url(#{uid}-c)"><rect x="{-band*2:.1f}" y="{-h}" width="{band:.1f}" height="{h*3}" '
        f'fill="url(#{uid}-g)" transform="rotate(20 {w/2:.1f} {h/2:.1f})">'
        f'<animate attributeName="x" values="{-band*2:.1f};{travel:.1f};{travel:.1f}" keyTimes="0;{min(0.9, 1.1/every):.3f};1" '
        f'dur="{every}s" begin="{begin:.2f}s" repeatCount="indefinite"/></rect></g>'
    )
