<a href="https://rakshit-737.is-a.dev">
  <img src="assets/hero.svg" width="100%" alt="Terminal: whoami → Rakshit Rameshbabu, Software & Security Engineer, B.Tech CSE (Cyber Security) at VIT Chennai. A radar sweeps across his public security repos." />
</a>

<img src="assets/taglines.svg" width="100%" alt="detection-as-code, measured on real telemetry · provenance graphs to root cause and blast radius · static analysis that never runs the sample · attribution that can say I don't know · every number regenerates from one command" />

<p align="center">
  <a href="https://rakshit-737.is-a.dev"><img src="assets/buttons/portfolio.svg" height="34" alt="Portfolio: rakshit-737.is-a.dev" /></a>
  <a href="https://www.linkedin.com/in/rakshit-rameshbabu/"><img src="assets/buttons/linkedin.svg" height="34" alt="LinkedIn: rakshit-rameshbabu" /></a>
  <a href="mailto:rakshitoffl@gmail.com"><img src="assets/buttons/email.svg" height="34" alt="Email: rakshitoffl@gmail.com" /></a>
  <a href="https://rakshit-737.is-a.dev/rakshit-rameshbabu-resume.pdf"><img src="assets/buttons/resume.svg" height="34" alt="Resume (PDF)" /></a>
  <a href="https://learn.cylabacademy.org/users/rrakshit"><img src="assets/buttons/cylab.svg" height="34" alt="CyLab Academy" /></a>
</p>

## <samp>❯ cat about.md</samp>

I'm a B.Tech CSE (Cyber Security) student at **VIT Chennai** (CGPA 9.07, class of 2028). I build **defensive security tooling** and **full-stack products**, and I take them end to end: written requirements, architecture, CI, then a release.

Every repo is held to one rule: **every number regenerates from one command.** That means public datasets, committed results, baselines run on identical inputs, and a *Limitations* section that says what does not work. The security tools are defensive and lab-safe: static where possible, sandboxed where not.

```yaml
# ~/.config/rakshit.yml
now:
  - wiring 13 detection / DFIR / CTI engines into one evidence graph   # throughline
  - Warden v2: supply-chain firewall for PyPI, manifests and images    # warden
  - taking Fillwright toward a Chrome Web Store release                # fillwright
research: ML job scheduling, reported as a negative result             # proactive-feasibility-scheduler
interests: [detection engineering, DFIR, supply-chain security, AI-agent security, post-quantum crypto]
open_to: internships & full-time roles in software / security engineering
```

## <samp>❯ ls ~/featured</samp>

> [!NOTE]
> Every number on these cards is copied from the linked repo's README or committed `results/`. Where a result is synthetic or simulated, the card says so.

<p align="center">
  <a href="https://github.com/rakshit-737/throughline"><img src="generated/card-throughline.svg" width="49%" alt="THROUGHLINE: evidence-first security knowledge graph" /></a>
  <a href="https://github.com/rakshit-737/warden-supply-chain-security"><img src="generated/card-warden-supply-chain-security.svg" width="49%" alt="WARDEN: software supply-chain security platform" /></a>
  <a href="https://github.com/rakshit-737/nikasha"><img src="generated/card-nikasha.svg" width="49%" alt="NIKASHA: fact-checks vulnerability reports against source" /></a>
  <a href="https://github.com/rakshit-737/afterlock"><img src="generated/card-afterlock.svg" width="49%" alt="AFTERLOCK: Kubernetes containment verifier" /></a>
  <a href="https://github.com/rakshit-737/anvil"><img src="generated/card-anvil.svg" width="49%" alt="ANVIL: detection-as-code for Sigma" /></a>
  <a href="https://github.com/rakshit-737/sluice"><img src="generated/card-sluice.svg" width="49%" alt="SLUICE: information-flow control for LLM agents" /></a>
  <a href="https://github.com/rakshit-737/proactive-feasibility-scheduler"><img src="generated/card-proactive-feasibility-scheduler.svg" width="49%" alt="Proactive Feasibility Scheduler: ML scheduling evaluation with a negative result" /></a>
  <a href="https://github.com/rakshit-737/docforge"><img src="generated/card-docforge.svg" width="49%" alt="DOCFORGE: local-first document studio" /></a>
  <a href="https://github.com/rakshit-737/fillwright"><img src="generated/card-fillwright.svg" width="49%" alt="FILLWRIGHT: privacy-first resume autofill extension" /></a>
  <a href="https://github.com/rakshit-737/feelslike"><img src="generated/card-feelslike.svg" width="49%" alt="FEELSLIKE: digital-twin HVAC optimizer" /></a>
</p>

## <samp>❯ throughline --map</samp>

Thirteen single-purpose security engines, each benchmarked on its own, plugged into one graph. [THROUGHLINE](https://github.com/rakshit-737/throughline) fuses them, so *what happened, how did it start, who did it, and how sure are we?* becomes one query.

<img src="assets/constellation.svg" width="100%" alt="THROUGHLINE map: ANVIL, GAUNTLET, VANTAGE (detection), REVENANT, ROOTLINE (DFIR), DRAGNET, OCCAM (intel), VITRINE, SPECIMEN (malware), FEINT (network), LINCHPIN, STRATUM, TRACEGATE (infra and supply chain) all feeding one evidence graph" />

<details>
<summary><b>open the full arsenal: every security repo, one measured headline each</b></summary>
<br/>

| domain | repo | headline (from the repo's own results) |
|---|---|---|
| detection engineering | [**ANVIL**](https://github.com/rakshit-737/anvil) | 461/461 evaluable SigmaHQ regression cases detected; 2,994,137 benign events replayed against 2,803 rules |
| purple team | [**GAUNTLET**](https://github.com/rakshit-737/gauntlet) | replays 96 real OTRF attack recordings through 2,519 SigmaHQ rules; ranked gaps and a CI regression gate |
| control coverage | [**VANTAGE**](https://github.com/rakshit-737/vantage) | CIS IG2 on classic Windows logs: 53.9% *claimed* ATT&CK coverage vs 11.2% *defended* |
| DFIR timelines | [**REVENANT**](https://github.com/rakshit-737/revenant) | confidence-graded incident stories; every claim cites the SHA-256 of its event; append-only custody ledger |
| attack reconstruction | [**ROOTLINE**](https://github.com/rakshit-737/rootline) | ATLAS S1–S4: event F1 0.559 vs 0.077 for IOC grep; graph reduction 3.8–4.4× with 100% of attack edges kept |
| attribution | [**DRAGNET**](https://github.com/rakshit-737/dragnet) | right group ranked first in 68% of 25 ATT&CK campaigns; never commits at MEDIUM+ to a wrong actor |
| CTI reasoning | [**OCCAM**](https://github.com/rakshit-737/occam) | under planted false flags, names the framed group 1.1% of the time vs 88.0% for TTP similarity |
| malware triage | [**VITRINE**](https://github.com/rakshit-737/vitrine) | EMBER 2018 temporal split: ROC AUC 0.9917, 74.5% TPR at 0.1% FPR; never executes a sample |
| malware pipeline | [**SPECIMEN**](https://github.com/rakshit-737/specimen) | static gate skips 42% of detonations, misses 1.2% of malware; 95.9% family accuracy on 48,976 CAPEv2 reports |
| NIDS robustness | [**FEINT**](https://github.com/rakshit-737/feint) | XGBoost at 99.7% clean accuracy detects 42% of flows under realisable evasion; adversarial training restores 80–96% |
| attack paths | [**LINCHPIN**](https://github.com/rakshit-737/linchpin) | exact minimum remediation cut over scanner, BloodHound and EPSS/KEV data; sends no packets |
| cloud-native | [**STRATUM**](https://github.com/rakshit-737/stratum) | F1 1.000 on 148 upstream PSS conformance pods; 32 of 87 real workloads not PSS-restricted |
| CI/CD provenance | [**TRACEGATE**](https://github.com/rakshit-737/tracegate) | finding → introducing commit: 97.5% (356/365) vs 17.3% for the best baseline |
| K8s containment | [**AFTERLOCK**](https://github.com/rakshit-737/afterlock) | Go collector + Python planner; live kind lab agrees with the model on 17/17 steps across 3 runs |
| supply chain | [**WARDEN**](https://github.com/rakshit-737/warden-supply-chain-security) | 14 static analyzers, SBOM + SARIF + CI gate; 2,908 backend tests in CI |
| vuln-report triage | [**NIKASHA**](https://github.com/rakshit-737/nikasha) | v0.1.0 on PyPI; 0/126 genuine curl reports falsely flagged (Wilson 95% upper bound 2.96%) |
| agent security | [**SLUICE**](https://github.com/rakshit-737/sluice) · [**taintwall**](https://github.com/rakshit-737/taintwall) | taintwall: exfiltration 43% → 0% with all four layers, benign utility held at 100% |
| state reconstruction | [**SPECTRA**](https://github.com/rakshit-737/spectra-security) | pre-alpha: a Python reference slice runs end to end; no milestone is green yet, and the README says so |

</details>

## <samp>❯ ls ~/also-built</samp>

- **[PlantPal+](https://github.com/rakshit-737/PlantPal-Plus)**: plant care, fitness and nutrition on one habit loop. TypeScript monorepo (Expo, React + Vite, Express, PostgreSQL) with an IEEE-830 requirements package: 228 FRs, 119 user stories, 89 use cases.
- **[RailMind](https://github.com/rakshit-737/Railmind)**: a digital twin of a 21-station railway network feeding LangGraph agents that score incident-response plans. Runs offline, no API keys.
- **[portfolio](https://github.com/rakshit-737/portfolio)**: a candlelit, scroll-driven Next.js site. CI gates Lighthouse, axe, CSP and link checks; accessibility, best-practices and SEO score 100.
- **[VIT CGPA Calculator](https://github.com/rakshit-737/cgpa-calculator)** · **[learn-sql](https://github.com/rakshit-737/learn-sql)** · **[PaceReader](https://github.com/rakshit-737/pace-reader)** · **[ZT Web Security Simulator](https://github.com/rakshit-737/web-security-simulator)**: small tools for studying and campus life.

## <samp>❯ which --all</samp>

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,ts,js,go,c,cpp,java,bash,linux&perline=9" alt="Python, TypeScript, JavaScript, Go, C, C++, Java, Bash, Linux" /><br/>
  <img src="https://skillicons.dev/icons?i=fastapi,django,nodejs,express,postgres,redis,mongodb,sqlite,supabase&perline=9" alt="FastAPI, Django, Node.js, Express, PostgreSQL, Redis, MongoDB, SQLite, Supabase" /><br/>
  <img src="https://skillicons.dev/icons?i=react,nextjs,tailwind,vite,pytorch,sklearn,docker,kubernetes,githubactions,aws,vercel,git&perline=12" alt="React, Next.js, Tailwind, Vite, PyTorch, scikit-learn, Docker, Kubernetes, GitHub Actions, AWS, Vercel, Git" />
</p>

<img src="assets/toolchain.svg" width="100%" alt="Security toolchain: Sigma, YARA, MITRE ATT&CK, Sysmon, Volatility 3, plaso, eBPF, Trivy, Syft, OSV, OPA/Rego, Tetragon, BloodHound, nmap, OpenVAS, NVD/EPSS/KEV, XGBoost, SHAP, LangGraph, MCP and more" />

## <samp>❯ tail trophies.log</samp>

<img src="assets/trophies.svg" width="100%" alt="trophies.log: 2025-06-21 FIRST PRIZE, Cyber Secure 360 Expo 2025, SCOPE, VIT Chennai · 2026-06 TOP 100, FarAway Zuup Hackathon, of ~11,000 participants · 2026-08 FINALS, FeelsLike (Team Goldilocks), digital-twin building optimizer · 2026-09-17 RELEASE, Warden v2.0.0, supply-chain security platform · 2026-09-20 RELEASE, Fillwright v0.6.1, privacy-first autofill extension · 2026-09-26 RELEASE, Nikasha v0.1.0 on PyPI, GHCR and GitHub Releases · ongoing: CGPA 9.07, B.Tech CSE (Cyber Security), VIT Chennai, class of 2028" />

## <samp>❯ gh telemetry</samp>

<p align="center">
  <img src="generated/stats.svg" width="49%" alt="GitHub telemetry: contributions, commits, pull requests, stars and streaks, with a 52-week heatmap" />
  <img src="generated/languages.svg" width="49%" alt="Language breakdown by bytes across public repositories" />
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rakshit-737/rakshit-737/main/profile-3d-contrib/profile-night-green.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rakshit-737/rakshit-737/main/profile-3d-contrib/profile-green-animate.svg" />
  <img src="https://raw.githubusercontent.com/rakshit-737/rakshit-737/main/profile-3d-contrib/profile-night-green.svg" width="100%" alt="3D contribution calendar" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rakshit-737/rakshit-737/main/generated/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rakshit-737/rakshit-737/main/generated/snake-light.svg" />
  <img src="https://raw.githubusercontent.com/rakshit-737/rakshit-737/main/generated/snake-dark.svg" width="100%" alt="A snake eating the contribution graph" />
</picture>

<details>
<summary><b>how this profile builds itself</b></summary>
<br/>

```mermaid
flowchart LR
  API[("GitHub GraphQL API")] --> CARDS["build_cards.py<br/>telemetry · languages · project cards"]
  ART["build_art.py<br/>hero · taglines · buttons · map · trophies"] --> GIT
  API --> SNK["Platane/snk<br/>contribution snake"]
  API --> D3["github-profile-3d-contrib<br/>3D calendar"]
  CARDS & SNK & D3 --> GIT["profile.yml<br/>daily at 01:47 IST · on script changes"]
  GIT -->|git commit| SVG["assets/ + generated/*.svg"]
  SVG --> README(["this README"])
  classDef n fill:#0a0e14,stroke:#00e38c,color:#e6edf3
  classDef hub fill:#00e38c,stroke:#00e38c,color:#0a0e14
  class API,CARDS,ART,SNK,D3,GIT,SVG n
  class README hub
```

The hero, tagline banner, link buttons, toolchain, map, trophies log and footer are hand-built animated SVGs (`scripts/build_art.py`): SMIL only, no JavaScript, with a subset of JetBrains Mono embedded so they render the same on every OS, and every animation rests on its finished frame. The public instances of github-readme-stats, trophies and activity-graph now return 503/402, so the telemetry and language cards are generated here instead. Apart from the skill icons, every image on this page is served from this repo.

</details>

<img src="assets/footer.svg" width="100%" alt="exit: process completed" />
