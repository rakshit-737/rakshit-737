#!/usr/bin/env python3
"""Self-hosted GitHub profile cards.

The public instances of github-readme-stats, github-profile-trophy and
github-readme-activity-graph now answer 503/402, so this script builds the
same cards from the GitHub GraphQL API inside a GitHub Action and commits the
SVGs to the profile repo. Nothing is fetched when someone views the profile.

    python scripts/build_cards.py --user rakshit-737            # live (needs GITHUB_TOKEN)
    python scripts/build_cards.py --offline scripts/offline.json  # no network

Outputs (generated/):
    stats.svg        contributions, commits, PRs, stars, streaks + 52-week heatmap
    languages.svg    language share by bytes across owned public repos
    card-<repo>.svg  one card per entry in scripts/projects.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import C, CHAR_W, appear, cursor, esc, reveal, svg_doc, typed, window, wrap  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
API = os.environ.get("GITHUB_GRAPHQL_URL", "https://api.github.com/graphql")
# Markup/prose that would drown out the code languages.
EXCLUDE_LANGS = {"HTML", "CSS", "SCSS", "TeX", "Jupyter Notebook", "Roff", "Makefile"}

Q_PROFILE = """
query($login: String!) {
  user(login: $login) {
    login name createdAt
    followers { totalCount }
    mergedPRs: pullRequests(states: MERGED) { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""

Q_REPOS = """
query($login: String!, $after: String) {
  user(login: $login) {
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false,
                 privacy: PUBLIC, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        name description stargazerCount forkCount pushedAt isArchived
        primaryLanguage { name color }
        languages(first: 20, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}"""


# --------------------------------------------------------------------------- data
def gql(query: str, variables: dict, token: str) -> dict:
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "rakshit-737-profile-cards",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        payload = json.load(r)
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload["data"]


def fetch_live(login: str, token: str) -> dict:
    prof = gql(Q_PROFILE, {"login": login}, token)["user"]
    repos, after = [], None
    while True:
        page = gql(Q_REPOS, {"login": login, "after": after}, token)["user"]["repositories"]
        repos.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    cc = prof["contributionsCollection"]
    days = [
        (d["date"], d["contributionCount"])
        for w in cc["contributionCalendar"]["weeks"]
        for d in w["contributionDays"]
    ]
    return {
        "login": prof["login"],
        "window": "365d",
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "prs": cc["totalPullRequestContributions"],
        "reviews": cc["totalPullRequestReviewContributions"],
        "issues": cc["totalIssueContributions"],
        "merged_prs": prof["mergedPRs"]["totalCount"],
        "followers": prof["followers"]["totalCount"],
        "days": days,
        "repos": [
            {
                "name": r["name"],
                "stars": r["stargazerCount"],
                "forks": r["forkCount"],
                "pushed": r["pushedAt"],
                "archived": r["isArchived"],
                "primary": (r["primaryLanguage"] or {}).get("name"),
                "primary_color": (r["primaryLanguage"] or {}).get("color"),
                "langs": [
                    (e["node"]["name"], e["node"]["color"], e["size"])
                    for e in r["languages"]["edges"]
                ],
            }
            for r in repos
        ],
    }


def streaks(days: list[tuple[str, int]]) -> tuple[int, int]:
    counts = [c for _, c in sorted(days)]
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    cur = 0
    # today may still be empty: it does not break the streak yet
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if c == 0:
            break
        cur += 1
    return cur, longest


def fmt(n) -> str:
    if n is None:
        return "…"
    return f"{n:,}"


# --------------------------------------------------------------------------- cards
def stats_card(d: dict) -> str:
    W, H = 500, 300
    days = d.get("days") or []
    cur, lng = streaks(days) if days else (d.get("streak_current"), d.get("streak_longest"))
    repos = [r for r in d["repos"] if not r.get("archived")]
    stars = sum(r["stars"] for r in repos)
    parts = [window(W, H, f"telemetry — last {d.get('window', '365d')}", "s")]
    fs = 13.5
    parts.append(f'<text x="24" y="64" font-size="{fs}" fill="{C["green"]}" font-weight="700">❯</text>')
    cmd = f"gh telemetry --user {d['login']}"
    s, t = typed(24 + 2 * fs * CHAR_W, 64, cmd, fs, 0.3, "sc", fill=C["soft"])
    parts.append(s)
    rows = [
        ("contributions", fmt(d.get("contributions")), "stars", fmt(stars)),
        ("commits", fmt(d.get("commits")), "public repos", fmt(len(repos))),
        ("pull requests", fmt(d.get("prs")), "merged PRs", fmt(d.get("merged_prs"))),
        ("streak now", f"{fmt(cur)}d" if cur is not None else "…", "longest", f"{fmt(lng)}d" if lng is not None else "…"),
    ]
    y = 98
    for i, (k1, v1, k2, v2) in enumerate(rows):
        g = (
            f'<text x="24" y="{y}" font-size="13" fill="{C["dim"]}">{esc(k1)}</text>'
            f'<text x="226" y="{y}" font-size="14" font-weight="700" text-anchor="end" fill="{C["text"]}">{esc(v1)}</text>'
            f'<text x="262" y="{y}" font-size="13" fill="{C["dim"]}">{esc(k2)}</text>'
            f'<text x="476" y="{y}" font-size="14" font-weight="700" text-anchor="end" fill="{C["green"]}">{esc(v2)}</text>'
        )
        parts.append(appear(g, t + 0.15 + i * 0.12))
        y += 26
    t += 0.15 + len(rows) * 0.12
    # 52-week heatmap
    cell, gap = 6.6, 1.6
    step = cell + gap
    weeks = []
    if days:
        cols = {}
        for date, c in sorted(days)[-371:]:
            day = dt.date.fromisoformat(date)
            wk = (day - dt.date(1970, 1, 4)).days // 7  # weeks start Sunday, like GitHub
            cols.setdefault(wk, [None] * 7)[(day.weekday() + 1) % 7] = c
        weeks = [cols[k] for k in sorted(cols)][-53:]
    nonzero = sorted(c for w in weeks for c in w if c)
    def level(c):
        if not c:
            return 0
        if not nonzero:
            return 1
        q = [nonzero[int(len(nonzero) * p)] for p in (0.25, 0.5, 0.75)]
        return 1 + sum(c > x for x in q)
    shades = [C["faint"], "#0b4d33", "#0a7a4e", "#00b36e", C["green"]]
    ncols = 53
    x0 = (W - ncols * step + gap) / 2
    y0 = 212
    more_x = 476
    sq_end = more_x - 4 * 11.5 * CHAR_W - 6
    sq_start = sq_end - 5 * 9 + 2
    legend = (
        f'<text x="24" y="{y0-12}" font-size="11.5" fill="{C["dim"]}">activity · 52 weeks</text>'
        f'<text x="{sq_start - 6:.1f}" y="{y0-12}" font-size="11.5" text-anchor="end" fill="{C["dim"]}">less</text>'
        + "".join(f'<rect x="{sq_start + i*9:.1f}" y="{y0-20}" width="7" height="7" rx="1.5" fill="{sh}"/>' for i, sh in enumerate(shades))
        + f'<text x="{more_x}" y="{y0-12}" font-size="11.5" text-anchor="end" fill="{C["dim"]}">more</text>'
    )
    parts.append(appear(legend, t))
    for wi in range(ncols):
        col = weeks[wi - (ncols - len(weeks))] if weeks and wi >= ncols - len(weeks) else [None] * 7
        rects = []
        for di in range(7):
            c = col[di]
            fill = shades[level(c)] if c is not None else ("#11161d" if not weeks else "none")
            if fill == "none":
                continue
            rects.append(f'<rect x="{x0 + wi*step:.1f}" y="{y0 + di*step:.1f}" width="{cell}" height="{cell}" rx="1.4" fill="{fill}"/>')
        parts.append(appear("".join(rects), t + 0.1 + wi * 0.018, 0.15))
    if not weeks:
        parts.append(appear(
            f'<text x="{W/2}" y="{y0 + 3.5*step + 4}" font-size="11.5" text-anchor="middle" fill="{C["dim"]}">'
            f'heatmap fills in on the first workflow run</text>', t + 0.4))
    end = t + 0.1 + ncols * 0.018
    parts.append(appear(
        f'<text x="24" y="{H-16}" font-size="11" fill="#56606b">generated {dt.date.today().isoformat()} · self-hosted, no third-party API</text>',
        end))
    used = "".join(r[0] + r[1] + r[2] + r[3] for r in rows) + cmd + "❯ telemetry — last activity · 52 weeks less more heatmap fills in on the first workflow run generated self-hosted, no third-party API 0123456789-d…" + d.get("window", "")
    return svg_doc(W, H, "\n".join(parts), "", f"GitHub telemetry for {d['login']}", used)


def languages_card(d: dict, top: int = 7) -> str:
    W, H = 500, 300
    totals: dict[str, list] = {}
    for r in d["repos"]:
        for name, color, size in r["langs"]:
            if name in EXCLUDE_LANGS:
                continue
            e = totals.setdefault(name, [color or C["dim"], 0])
            e[1] += size
    ranked = sorted(totals.items(), key=lambda kv: -kv[1][1])
    grand = sum(v[1] for _, v in ranked) or 1
    head = ranked[:top]
    rest = sum(v[1] for _, v in ranked[top:])
    if rest:
        head.append(("other", [C["dim"], rest]))
    nrepos = sum(1 for r in d["repos"] if r["langs"])
    parts = [window(W, H, f"languages — {nrepos} public repos, by bytes", "l")]
    fs = 13.5
    parts.append(f'<text x="24" y="64" font-size="{fs}" fill="{C["green"]}" font-weight="700">❯</text>')
    cmd = "linguist --breakdown ~/rakshit-737/*"
    s, t = typed(24 + 2 * fs * CHAR_W, 64, cmd, fs, 0.3, "lc", fill=C["soft"])
    parts.append(s)
    # stacked bar
    bx, by, bw, bh = 24, 84, W - 48, 10
    parts.append(f'<defs><clipPath id="lbar"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5"/></clipPath></defs>')
    segs, x = [], bx
    for i, (name, (color, size)) in enumerate(head):
        w = bw * size / grand
        segs.append(
            f'<rect x="{x:.2f}" y="{by}" width="{w:.2f}" height="{bh}" fill="{color}">'
            + reveal(t + i * 0.09, 0.35, "width", f"{w:.2f}") + "</rect>")
        x += w
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5" fill="{C["faint"]}"/>')
    parts.append(f'<g clip-path="url(#lbar)">{"".join(segs)}</g>')
    t += 0.2
    # rows: name, block bar, percent
    y = 122
    bar_chars = 22
    fsr = 13
    for i, (name, (color, size)) in enumerate(head):
        pct = 100 * size / grand
        full = max(1 if pct > 0 else 0, round(bar_chars * pct / max(100 * head[0][1][1] / grand, 1e-9)))
        filled = "█" * full
        empty = "░" * (bar_chars - full)
        row = (
            f'<circle cx="30" cy="{y-4.5}" r="4.5" fill="{color}"/>'
            f'<text x="44" y="{y}" font-size="{fsr}" fill="{C["soft"]}">{esc(name[:14])}</text>'
            f'<text x="{44 + 15*fsr*CHAR_W:.1f}" y="{y}" font-size="{fsr}" fill="{color}">{filled}'
            f'<tspan fill="{C["faint"]}">{empty}</tspan></text>'
            f'<text x="476" y="{y}" font-size="{fsr}" font-weight="700" text-anchor="end" fill="{C["text"]}">{pct:5.1f}%</text>'
        )
        parts.append(appear(row, t + i * 0.1))
        y += 20
    parts.append(appear(
        f'<text x="24" y="{H-16}" font-size="11" fill="#56606b">markup excluded: HTML, CSS, TeX, notebooks · non-fork repos only</text>',
        t + len(head) * 0.1))
    used = cmd + "".join(n for n, _ in head) + "█░%.0123456789 ❯ languages — public repos, by bytes markup excluded: HTML, CSS, TeX, notebooks · non-fork repos only" + str(nrepos)
    return svg_doc(W, H, "\n".join(parts), "", "Language breakdown", used)


def chip(x: float, y: float, label: str, color: str) -> tuple[str, float]:
    size = 11
    w = len(label) * size * CHAR_W + 14
    return (
        f'<rect x="{x:.1f}" y="{y-13}" width="{w:.1f}" height="18" rx="9" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.55"/>'
        f'<text x="{x + 7:.1f}" y="{y}" font-size="{size}" fill="{color}">{esc(label)}</text>',
        w,
    )


def project_card(p: dict, live: dict | None) -> str:
    W, H = 500, 214
    repo = p["repo"]
    parts = [window(W, H, f"~/rakshit-737/{repo}", "p")]
    ts = 22
    title = p["title"]
    parts.append(appear(
        f'<text x="24" y="74" font-size="{ts}" font-weight="800" fill="{C["green"]}">{esc(title)}</text>', 0.15))
    # chips, right-aligned
    x = W - 24
    chip_svg = []
    for label in reversed(p.get("chips", [])):
        est = len(label) * 11 * CHAR_W + 14
        x -= est
        svg, _ = chip(x, 70, label, C["cyan"])
        chip_svg.append(svg)
        x -= 6
    parts.append(appear("".join(chip_svg), 0.3))
    width_chars = int((W - 48) / (13 * CHAR_W * 1.04))  # 4% slack for hinting
    lines = wrap(p["tagline"], width_chars)[:3]
    y = 104
    for i, line in enumerate(lines):
        parts.append(appear(f'<text x="24" y="{y}" font-size="13" fill="{C["soft"]}">{esc(line)}</text>', 0.35 + i * 0.08))
        y += 19
    metric = "▸ " + p["metric"]
    msize = min(12.5, (W - 48) / (len(metric) * CHAR_W * 1.04))
    parts.append(appear(
        f'<text x="24" y="{H-46}" font-size="{msize:.2f}" font-weight="700" fill="{C["amber"]}">{esc(metric)}</text>', 0.6))
    # footer: language · stars · updated
    foot = []
    lang = (live or {}).get("primary") or p.get("lang")
    color = (live or {}).get("primary_color") or C["dim"]
    fx = 24
    if lang:
        foot.append(f'<circle cx="{fx+5}" cy="{H-20}" r="5" fill="{color}"/>')
        foot.append(f'<text x="{fx+16}" y="{H-16}" font-size="12" fill="{C["dim"]}">{esc(lang)}</text>')
        fx += 16 + len(lang) * 12 * CHAR_W + 18
    if live is not None:
        if live["stars"]:
            foot.append(f'<text x="{fx:.1f}" y="{H-16}" font-size="12" fill="{C["dim"]}">★ {live["stars"]}</text>')
        if live.get("pushed"):
            foot.append(f'<text x="{W-24}" y="{H-16}" font-size="12" text-anchor="end" fill="{C["dim"]}">pushed {live["pushed"][:10]}</text>')
    parts.append(appear("".join(foot), 0.7))
    used = title + "".join(p.get("chips", [])) + p["tagline"] + metric + (lang or "") + "★ pushed 0123456789-~/rakshit-737/" + repo
    return svg_doc(W, H, "\n".join(parts), "", f"{title}: {p['tagline']}", used)


# --------------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=os.environ.get("GITHUB_REPOSITORY_OWNER", "rakshit-737"))
    ap.add_argument("--offline", help="JSON snapshot instead of the API")
    ap.add_argument("--out", default=str(ROOT / "generated"))
    ap.add_argument("--dump", help="also write the fetched data to this JSON file")
    a = ap.parse_args()

    if a.offline:
        data = json.loads(Path(a.offline).read_text())
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            sys.exit("GITHUB_TOKEN is not set (use --offline for a local build)")
        data = fetch_live(a.user, token)
    if a.dump:
        Path(a.dump).write_text(json.dumps(data, indent=1))

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "stats.svg").write_text(stats_card(data), encoding="utf-8")
    (out / "languages.svg").write_text(languages_card(data), encoding="utf-8")
    by_name = {r["name"].lower(): r for r in data["repos"]}
    projects = json.loads((ROOT / "scripts" / "projects.json").read_text())
    for p in projects:
        live = by_name.get(p["repo"].lower())
        (out / f"card-{p['repo']}.svg").write_text(project_card(p, live), encoding="utf-8")
    print(f"wrote {2 + len(projects)} cards to {out}")


if __name__ == "__main__":
    main()
