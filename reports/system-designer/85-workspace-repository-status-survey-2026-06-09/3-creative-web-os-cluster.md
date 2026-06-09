---
role: system-designer
lane: scout
session: 85-workspace-repository-status-survey-2026-06-09
part: 3-creative-web-os-cluster
date: 2026-06-09
scope: read-only classification of creative / writing / web / OS-adjacent repos under /git/github.com/LiGoldragon/
method: INTENT.md + README.md + top-level ls + git log -1 per repo; no builds; no private-repos access
---

# Creative / Web / OS-Adjacent Repository Classification

Read-only survey. Owning-surface vocabulary: POET (prose/writing craft),
VIDEOGRAPHER (video craft), WEB (web publishing/sites), SYSTEM-OPERATOR
(OS/platform/deploy/desktop daemons), PERSONA-CORE (cluster/identity
production data), ARCHIVE (intentional historical store), UNKNOWN.

Fit vocabulary: KEEP-ACTIVE (live, owned, fits a surface), KEEP-ADJACENT
(supports an active surface but not itself the focus), ARCHIVE (move to /
already an archive), RETIRE (superseded; candidate for removal),
ASK-PSYCHE (genuine ambiguity, psyche must decide).

## Classification table

| Repo | What it is | Last commit | Owning surface | Fit | INTENT.md |
|---|---|---|---|---|---|
| TheBookOfSol | Li Goldragon's primary prose book — solar/lunar cosmology, ayurveda, diet, yoga-tantra | 2026-06-08 cosmology arc-measurement note | POET | KEEP-ACTIVE | no |
| TheBookOfGoldragon | Companion philosophy book + raw notes (Kali Yuga, warrior/tyrant) | 2026-02-23 add(raw_note) | POET | KEEP-ACTIVE | no |
| BookOfLuna | Lunar counterpart book; currently only an AI-intent + generated-images stub | 2026-05-18 add Luna AI intent | POET | KEEP-ADJACENT | no (has Artificial_Intelligence/Intent.md) |
| BookMaker | Nix+Gemini OCR tool that digitizes book-page images to Markdown | 2026-02-12 init(BookMaker v0.1) | POET (tooling) | KEEP-ADJACENT | no |
| caraka-samhita | Philological study/translation repo for the Caraka Saṃhitā; sources TheBookOfSol | 2026-06-05 Su.27 fruit-verse correction | POET | KEEP-ACTIVE | no |
| AnaSeahawk-website | Public-facing archive site for Ana Seahawk (sovereign-biophysics research) | 2026-04-27 journal entry, Sarande | WEB / POET | KEEP-ACTIVE | no (has ARCHITECTURE.md) |
| webpage | Hugo site (ligoldragon.com); planeEarth content removed Dec 2025 | 2025-12-13 remove(hugoYaml(planeEarth)) | WEB | ASK-PSYCHE | no |
| WebPublish | Rust + Cap'n Proto schema-driven Cloudflare Pages apply engine | 2026-05-30 add aski source | WEB / SYSTEM-OPERATOR | KEEP-ACTIVE | no |
| wiki | Org-roam-style personal knowledge wiki (91 dated notes, 2021–2023) | 2025-09-10 add(reduced shivambu) | POET / PERSONA-CORE | KEEP-ADJACENT | no |
| chroma | Rust user-service daemon: desktop colour state (theme/warmth/brightness) | 2026-06-08 migrate to nota-next stack | SYSTEM-OPERATOR | KEEP-ACTIVE | yes |
| chronos | Rust user-service daemon: zodiacal time / sunrise-sunset / twilight events | 2026-06-08 migrate to nota-next stack | SYSTEM-OPERATOR | KEEP-ACTIVE | yes |
| CriomOS-emacs | Emacs distribution flake for CriomOS home profile (split from archive) | 2026-06-08 drop aski editor support | SYSTEM-OPERATOR | KEEP-ACTIVE | no |
| CriomOS-pkgs | Package stubs (e.g. vscode extension index) for CriomOS | 2026-05-28 update vscode extension index | SYSTEM-OPERATOR | KEEP-ADJACENT | no |
| CriomOS-test-cluster | Independent fixture cluster proving CriomOS/Horizon consume projected data without prod leakage | 2026-05-25 migrate fixtures to canonical nota | SYSTEM-OPERATOR | KEEP-ACTIVE | no |
| criomos-archive | Intentional archive of legacy CriomOS (pkdjz, mkEmacs, mkWebpage, etc.) | 2026-04-27 update mentci-tools | ARCHIVE | ARCHIVE | no |
| Armbian-RockPi4B-NixOS | One-off bootstrap scripts (setup-armbian-gnome) for RockPi 4B on NixOS | 2026-01-21 modify(bootstrap scripts) | SYSTEM-OPERATOR | ASK-PSYCHE | no |
| goldragon | Production cluster proposal (datom.nota) — every node/user/trust relation; fed to horizon-cli | 2026-06-05 add ouranos swap policy | PERSONA-CORE | KEEP-ACTIVE | no |
| forge | Criome-stack executor daemon — planned replacement for nix build infra (future work, skeleton) | 2026-06-05 docs: add INTENT.md | SYSTEM-OPERATOR | KEEP-ADJACENT | yes |
| signal-forge | Wire-contract crate for criome↔forge effect verbs (skeleton-as-design, paused) | 2026-05-24 add v0.1 concept schema | SYSTEM-OPERATOR | KEEP-ADJACENT | no |
| horizon-next | Concept prototype proving Horizon datatypes generate from a pure schema; scaled-down vs horizon-rs | 2026-05-28 Plane runtime surface | SYSTEM-OPERATOR | ASK-PSYCHE (lean RETIRE) | yes |

## CriomOS deploy family (context only — one line each, not deep-audited)

| Repo | One-line | Last commit | INTENT.md |
|---|---|---|---|
| CriomOS | NixOS platform — modules + module aggregate; the production OS (Stack A); deploys driven by lojix-cli | 2026-06-07 pin medium video production tools | yes |
| CriomOS-home | Standalone home-profile blueprint flake (desktop survivability, shell safety) split from legacy CriomOS | 2026-06-08 drop Gas City tooling | yes |
| CriomOS-lib | Shared constants, helpers, and data files for CriomOS and CriomOS-home | 2026-05-29 add Gemma 4 quantized variants | no |

## Notes

### Poet surface
TheBookOfSol (active, edited yesterday), TheBookOfGoldragon, and
caraka-samhita are the live prose cluster. caraka-samhita explicitly
exists to source TheBookOfSol ("move from translator-told-me-so to the
Sanskrit says so") — KEEP-ACTIVE as a poet support repo. TheBookOfGoldragon
is quieter (Feb) but is a named companion book, not dead. BookOfLuna is
near-empty (only an AI-intent file + generated images) — a stub for a
planned lunar book; KEEP-ADJACENT. BookMaker is the OCR tooling that feeds
all of these — poet tooling, low-churn but functional.

### Web surface
- **AnaSeahawk-website** — a real public archive site (front-door README,
  ARCHITECTURE.md, publish checklist/queue, batch-publish doc). Active
  through April. Owning surface is genuinely web-publishing; content is
  poet-adjacent (the psyche's partner's research archive). KEEP-ACTIVE.
- **WebPublish** — Rust + Cap'n Proto Cloudflare Pages apply engine
  (`webpublish apply`, one stdin message). This is the publishing engine,
  not a site. Active (May), schema-driven, fits the component discipline.
  KEEP-ACTIVE; owning surface straddles WEB and SYSTEM-OPERATOR.
- **webpage** — Hugo site for ligoldragon.com. Last touched Dec 2025 to
  *remove* the planeEarth content; `content/` now holds little more than an
  `_index.md`. Unclear whether it is being retired in favour of WebPublish
  output or simply dormant. ASK-PSYCHE: is webpage still the live site, or
  superseded by the WebPublish pipeline?

### System-operator surface
- **chroma** and **chronos** are the two live desktop daemons (both
  migrated to nota-next yesterday, both have full INTENT.md/ARCHITECTURE.md).
  chronos publishes solar events; chroma subscribes. KEEP-ACTIVE — the
  flagship active system-operator visual/scheduler work.
- **CriomOS-emacs** — actively split out of criomos-archive's legacy
  mkEmacs; still scaffold-stage per README but committed yesterday.
  KEEP-ACTIVE.
- **CriomOS-pkgs** — small package-stub repo (vscode extension index).
  KEEP-ADJACENT to the CriomOS platform.
- **CriomOS-test-cluster** — deliberately-separate fixture cluster that
  proves CriomOS/Horizon consume projected data without prod secrets
  leaking into the platform repo. KEEP-ACTIVE infrastructure.
- **Armbian-RockPi4B-NixOS** — a single `setup-armbian-gnome` script dir,
  untouched since Jan 2026, no README/INTENT. Looks like a one-off
  board-bring-up artifact. ASK-PSYCHE: keep as a reference snippet or
  retire? (Leaning RETIRE/ARCHIVE, but board-specific bootstrap can have
  long-tail value, so flagging rather than deciding.)

### forge / signal-forge
forge's own INTENT/README is explicit: it is the **criome-stack executor
daemon, planned replacement for nix build infra**, "future work,
skeleton-as-design until criome scaffolds," and explicitly **NOT** the old
lojix→forge deploy rename (the GitHub `lojix`→`forge` redirect is a naming
artifact; the deploy stack is lojix-cli / lojix / signal-lojix). Verified —
matches the task's note. signal-forge is its paused wire contract
("skeleton-as-design, type signatures pinned, bodies todo!(), lands when
forge-daemon is wired"). Both KEEP-ADJACENT: intentional future work with
clear intent, not dead, but not on a current production path.

### horizon-next vs horizon-rs
**horizon-rs** exists and is more recently active (committed 2026-06-08,
"migrate proposal codec to nota-next") and carries the real
`ClusterProposal` with full collection fields. **horizon-next**'s own
INTENT frames it as a **concept prototype** that "closes the /40
feasibility audit's first-and-decisive gate with running code" using a
*scaled-down* cluster slice — its stated job was to *prove* schema-driven
generation, not to be the runtime ("runtime shape demonstrated, not
decided"). It has not been committed since 2026-05-28. This reads as a
proof-of-concept whose lesson has been absorbed into the live schema stack
+ horizon-rs. ASK-PSYCHE, leaning RETIRE: confirm the concept is discharged
and horizon-rs is canonical before removing horizon-next.

### Archive
criomos-archive is the intentional legacy store (pkdjz, mkEmacs, mkWebpage,
old proposals). Confirmed ARCHIVE — leave as-is; active children
(CriomOS-emacs, CriomOS-home, CriomOS) are being carved out of it.

### Persona-core
- **goldragon** is production cluster data (datom.nota: nodes, users, trust,
  router/Wi-Fi facts, swap policy) consumed by horizon-cli. KEEP-ACTIVE,
  PERSONA-CORE. Distinct from CriomOS-test-cluster by design.
- **wiki** is the long-running personal knowledge base (91 dated org-roam
  notes, 2021–2023, last touched Sep 2025). Low churn but a coherent
  personal/poet knowledge surface. KEEP-ADJACENT.

### INTENT.md gap
Only 5 of the 20 primary repos carry an INTENT.md (chroma, chronos, forge,
horizon-next, plus the CriomOS-family CriomOS/CriomOS-home). Per the
workspace contract every repo needs one and its absence is the first gap to
fill. The active poet repos (TheBookOfSol, caraka-samhita,
TheBookOfGoldragon), the web repos (AnaSeahawk-website, WebPublish,
webpage), goldragon, wiki, and the CriomOS satellites (CriomOS-emacs/-pkgs/
-test-cluster/-lib) all lack one. AnaSeahawk-website at least has an
ARCHITECTURE.md.

## Open questions for the psyche

1. **webpage** — still the live ligoldragon.com site, or superseded by the
   WebPublish pipeline now that planeEarth content was removed?
2. **horizon-next** — is the schema-generation concept discharged and
   horizon-rs canonical, so horizon-next can be retired?
3. **Armbian-RockPi4B-NixOS** — keep the RockPi 4B bootstrap script as a
   reference, archive it, or retire it?
