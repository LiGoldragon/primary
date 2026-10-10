# Consumer Sweep: protos 0.15.0 / datomic 0.8.0 / ethos-zero 1.0.0

Swept on 2026-09-04. Excludes already-updated: orchestrate, signal-orchestrate,
meta-signal-orchestrate, CriomOS, CriomOS-home.

Current mains: protos `56c683ec8d1e`, datomic `a27f9b8e7789`, ethos-zero `185f13a90354`.
The old repo name for datomic was `datom`; `curriculum-deploy` still pins the old URL.

---

## 1. Dependency hits — Cargo.toml and flake.nix/flake.lock

All pinned revs below are confirmed ancestors of the respective current mains
(verified with `git merge-base --is-ancestor`).

### claude-answers

Remote: `git@github.com:LiGoldragon/claude-answers.git`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 19 | `datomic = { git = "https://github.com/LiGoldragon/datomic", rev = "b670c72d0c2cb94ad1e39b372271f6569d91e214" }` |
| Cargo.toml | 20 | `protos = { git = "https://github.com/LiGoldragon/protos", rev = "bfde3b878dd3de2991d7f605b59f57a13ef8f20b" }` |
| Cargo.toml | 26 | `ethos-zero = { git = "https://github.com/LiGoldragon/ethos-zero", rev = "b922afba278d5e1430f0a52ce49898c3263e87bc" }` |

All three revs are behind main. Last commit: `e637388f` 2026-08-29 "Prove Ethos map matches recursive query D3". Clean.

### core-logos

Remote: `git@github.com:LiGoldragon/core-logos.git`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 18 | `protos = { git = "https://github.com/LiGoldragon/protos.git", rev = "cdc74bd28187bdb39b8ddc2228eef4934873dd45" }` |

Rev is behind main. Last commit: `98873669` 2026-08-13 "docs: mark Protos estate status". Clean.

### curriculum-deploy

Remote: `git@github.com:LiGoldragon/curriculum-deploy`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 16 | `datom = { git = "https://github.com/LiGoldragon/datom", rev = "d47419ef872ab76bfbd6bb4b3e84b62a883a8d31" }` |
| Cargo.toml | 18 | `protos = { git = "https://github.com/LiGoldragon/protos", rev = "bfea114c96eb548ceae17ab05da9c231a6412ba1" }` |

Both revs are behind main. The `datom` URL uses the retired name; the repo
`github.com/LiGoldragon/datom` is a local alias of `datomic` (remote reports
`git@github.com:LiGoldragon/datomic.git`). Last commit: `74581e74` 2026-09-04
"Render target-specific skill conditionals". Clean.

### meta-signal-spirit

Remote: `git@github.com:LiGoldragon/meta-signal-spirit.git`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 20 | `protos = { git = "https://github.com/LiGoldragon/protos.git", rev = "d06c4a9" }` |

Rev is behind main. Last commit: `922f8a0e` 2026-08-13 "docs: mark Protos estate status". Clean.

### meta-signal-upgrade

Remote: `git@github.com:LiGoldragon/meta-signal-upgrade.git`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 31 | `protos = { git = "https://github.com/LiGoldragon/protos.git", rev = "9bce5ed8efadeb157811b256aa69a1f88cd5314f" }` |

Rev is behind main. Last commit: `8e4a82e8` 2026-07-31 "docs: mark Protos estate status".
**Dirty**: `M ARCHITECTURE.md`, `M Cargo.lock`, `M Cargo.toml` — the Cargo.toml in
the working tree already references an updated protos rev; uncommitted.

### signal-spirit

Remote: `git@github.com:LiGoldragon/signal-spirit.git`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 25 | `protos = { git = "https://github.com/LiGoldragon/protos.git", rev = "d06c4a9" }` |

Rev is behind main. Last commit: `d1a9f2fd` 2026-08-13 "docs: mark Protos estate status". Clean.

### signal-terminal

Remote: `git@github.com:LiGoldragon/signal-terminal.git`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 28 | `protos = { git = "https://github.com/LiGoldragon/protos.git", rev = "9bce5ed8efadeb157811b256aa69a1f88cd5314f" }` |

Rev is behind main. Last commit: `ad74f5a3` 2026-08-13 "docs: mark Protos estate status". Clean.

### signal-upgrade

Remote: `git@github.com:LiGoldragon/signal-upgrade.git`

| File | Line | Verbatim |
|------|------|----------|
| Cargo.toml | 28 | `protos = { git = "https://github.com/LiGoldragon/protos.git", rev = "9bce5ed8efadeb157811b256aa69a1f88cd5314f" }` |

Rev is behind main. Last commit: `9df12e3c` 2026-08-13 "docs: mark Protos estate status". Clean.

### protos-engine (flake.nix — integration harness, not a consumer crate)

Remote: `git@github.com:LiGoldragon/protos-engine`

| File | Line | Verbatim |
|------|------|----------|
| flake.nix | 17 | `legacy-protos.url = "github:LiGoldragon/protos/1343d0c405cdb6929552ea6b12c48739e73f35ab";` |
| flake.nix | 27 | `protos.url = "github:LiGoldragon/protos/65e7c6d4692a40e1c49deffb3fb4a9a2c3555c5b";` |
| flake.nix | 28 | `nomos-protos.url = "github:LiGoldragon/protos/1263f9d1f73b57885d695ac033bdd6faa1334ddf";` |
| flake.nix | 56 | `stream-protos.url = "github:LiGoldragon/protos/95aeb1470c549a404518faf1ab0280a36583a2b3";` |

All revs are behind main. By design: protos-engine is a pinned conformance sink
that deliberately pins historical slices for comparative testing. Last commit:
`7a1bfd19` 2026-08-07 "docs: mark Protos estate status". **Dirty**: `A ideas/guardedObjects-2026-08-07.md`.

---

## 2. Per-repository status

| Repository | Remote | Last commit | Dirty | Liveness |
|---|---|---|---|---|
| claude-answers | github.com/LiGoldragon/claude-answers | 2026-08-29 "Prove Ethos map matches recursive query D3" | no | **LIVE** — referenced by CriomOS and CriomOS-home flake.lock |
| core-logos | github.com/LiGoldragon/core-logos | 2026-08-13 "docs: mark Protos estate status" | no | **LIVE** — transitive dependency of lojix, which is in CriomOS |
| curriculum-deploy | github.com/LiGoldragon/curriculum-deploy | 2026-09-04 "Render target-specific skill conditionals" | no | **LIVE** — primary flake.nix pulls it as the skill-deployment runtime |
| meta-signal-spirit | github.com/LiGoldragon/meta-signal-spirit | 2026-08-13 "docs: mark Protos estate status" | no | **LIVE** — referenced by CriomOS and CriomOS-home flake.lock |
| signal-spirit | github.com/LiGoldragon/signal-spirit | 2026-08-13 "docs: mark Protos estate status" | no | **LIVE** — referenced by CriomOS flake.lock |
| meta-signal-upgrade | github.com/LiGoldragon/meta-signal-upgrade | 2026-07-31 "docs: mark Protos estate status" | YES | dormant — listed Active in repos-manifest; not in CriomOS/CriomOS-home/lojix; has uncommitted upgrade attempt |
| signal-terminal | github.com/LiGoldragon/signal-terminal | 2026-08-13 "docs: mark Protos estate status" | no | dormant — listed Active in repos-manifest; not yet in CriomOS |
| signal-upgrade | github.com/LiGoldragon/signal-upgrade | 2026-08-13 "docs: mark Protos estate status" | no | dormant — listed Active in repos-manifest; not yet in CriomOS |
| protos-engine | github.com/LiGoldragon/protos-engine | 2026-08-07 "docs: mark Protos estate status" | YES | dormant — conformance/integration harness; not deployed |

---

## 3. Old shapes in /home/li/primary

Searched: `*.md`, `*.ethos`, `*.datom`, `*.rs`, `*.nix`, `*.toml`, `*.dotos`
under `/home/li/primary`, excluding `.git/`, `.jj/`, `target/`, `result*`.

No `;;` comments found in any `.ethos` or `.datom` file under primary.
No `to_dotos` found anywhere in primary.
No `Schema.{` found anywhere in primary.

### DatomRealizing / DatomTextualizing

| File | Line | Verbatim |
|------|------|----------|
| design/ProtosEngine/ontologicalMap-2026-08-18.md | 57 | `Currently ~17 dialect-local traits: DatomRealizing, DatomTextualizing,` |
| design/ProtosEngine/ontologicalMap-2026-08-18.md | 157 | `Vanish (12): DatomRealizing, DatomTextualizing, TagPayloading,` |

### Interface.{

| File | Line | Verbatim |
|------|------|----------|
| design/ProtosEngine/psycheEthosFixture-2026-08-11.md | 41 | `Interface.{1 0 0}` |
| design/ProtosEngine/psycheEthosFixtureStage2-2026-08-14.md | 47 | `Interface.{1 0 0}` |
| design/ProtosEngine/psycheEthosFixtureStage2-2026-08-14.md | 319 | `- Is \`Interface.{1 0 0}\` the exact header and version form?` |
| flows/4decf7/reports/ethosObjects.md | 173 | `Interface.{1 0 0}` |
| flows/4decf7/reports/ethosObjects.md | 186 | `sections: [inputs] [outputs] [refusals] [streams]. The \`Interface.{}\`` |
| flows/4decf7/reports/ethosObjects.md | 493–494 | `Interface files keep their ruled shape: \`Interface.{v}\`, …` |
| flows/4decf7/reports/ethosObjects.md | 499 | `and has no Channel. The Interface.{} head with [inputs]/[outputs]` |
| flows/4decf7/reports/ethosObjects.md | 505 | `` `Interface.{}` is superseded by `Signal.{}` or whether they name `` |
| flows/ba906ae2/vision/signalIsOurMessagingLayer.md | 52 | `typed, on the \`Interface.{1 0 0}\` header in Codex's proposed` |
| flows/ba906ae2/vision/signalIsOurMessagingLayer.md | 56 | `` `Interface.{1 0 0}`) `` |
| flows/01a03eda/reports/orchestrateChangesProposal.md | 22 | `Interface.{0 2 0}` |

### Channel.{

| File | Line | Verbatim |
|------|------|----------|
| flows/01a03d6e/reports/orchestrateLockInterfaceProposal.md | 101 | `Channel.{Orchestrate 1 5}` |
| flows/4decf7/reports/ethosObjects.md | 450 | (discussion of `Channel.{Orchestrate 1 5}`) |
| flows/4decf7/reports/ethosObjects.md | 493–494 | `` `Channel.{Name contract wire}` `` |
| flows/01a03eda/reports/orchestrateChangesProposal.md | 23 | `Channel.{Orchestrate 1 5}` |
| flows/01a03603/reports/orchestrateInterfaces.md | 22 | `Ordinary \`Channel.{Orchestrate 1 4}\`` |

### Portion (historical, in flow archives)

Occurrences in `flows/4decf7/reports/protos.md`, `flows/4decf7/reports/datom.md`,
`flows/4decf7/reports/ethos.md` (lines 1112, 1114, 1182–1196, 851, etc.)
and `flows/index.md:124`. All are historical design records documenting the term
before it was replaced. No occurrence in active skills, tools, or flake.

### Prospective (historical, in flow archives)

Occurrences in `flows/4decf7/reports/protos.md` (lines 772, 776, 810, 812, 915,
925, 947, 987, 1093, 1099–1100, 1598–1599), `flows/4decf7/reports/ethos.md`
(lines 1034, 1036, 1072, 1084, 1086, 1266, 1268, 1272, 1716),
`flows/4decf7/reports/datom.md` (lines 386, 399, 450, 459, 484, 493, 505, 539,
548, 1119, 1161). All historical records. No occurrence in active skills or flake.

### Dotos in orchestrate-related text

| File | Notes |
|------|-------|
| flows/01a03d6e/reports/orchestrateDeployment.md:93 | "removal of legacy Dotos file surfaces" |
| flows/01a03d6e/reports/orchestrateLockInterfaceProposal.md:92,141,144,391,434 | Orchestrate/Dotos transition history |
| flows/01a03eda/log.md:11,21,23 | Transition log entries |
| flows/01a03eda/reports/orchestrateRealizationStatus.md:9 | Dotos-only restriction removal |
| flows/01a03eda/reports/orchestrateChangesProposal.md:12,89,117,121 | Proposal to remove Dotos from Orchestrate |
| flows/01a03603/reports/orchestrateInterfaces.md:63 | Dotos derivations mentioned |
| flows/01a03603/reports/orchestrateNexus.md:14 | Dotos carrier framing |
| flows/01a02fd5/reports/metaOrchestrateRestoration.md:5 | Dotos path deletion history |
| design/ProtosEngine/ethosProductionFirstTargets-2026-08-02.md:27 | "Dotos: orchestrate → orchestrator" |
| design/ProtosEngine/VISION-2026-08-07.md:501 | NOTA to Dotos train reference |
| Vision/datom.md:6,28,30 | Canonical definition: Dotos is the notation layer |

Note: Vision/datom.md and design/ entries name Dotos as the current data notation
layer — those are not stale references but live definitions. The flow reports list
old Dotos wire use inside Orchestrate that this flow's work replaces.

---

## Summary

### Live consumers that must move

1. **claude-answers** — pins protos@bfde3b87, datomic@b670c72d, ethos-zero@b922afba; referenced by CriomOS and CriomOS-home.
2. **core-logos** — pins protos@cdc74bd2; transitive dependency of lojix (in CriomOS).
3. **curriculum-deploy** — pins protos@bfea114c and `datom`@d47419ef (retired URL); used by primary flake.nix to deploy skills.
4. **meta-signal-spirit** — pins protos@d06c4a9; referenced by CriomOS and CriomOS-home.
5. **signal-spirit** — pins protos@d06c4a9; referenced by CriomOS.

### Dormant consumers (stale but not deployed)

6. **meta-signal-upgrade** — pins protos@9bce5ed8; dirty (uncommitted upgrade attempt in working tree); not in CriomOS.
7. **signal-terminal** — pins protos@9bce5ed8; not yet in CriomOS.
8. **signal-upgrade** — pins protos@9bce5ed8; not yet in CriomOS.
9. **protos-engine** — four stale protos flake inputs; intentional historical slices for conformance testing; dirty (untracked ideas file); not deployed.

### Primary references to old shapes

Active (design docs agents may read):
- `design/ProtosEngine/ontologicalMap-2026-08-18.md:57,157` — DatomRealizing, DatomTextualizing
- `design/ProtosEngine/psycheEthosFixture-2026-08-11.md:41` — Interface.{1 0 0}
- `design/ProtosEngine/psycheEthosFixtureStage2-2026-08-14.md:47,319` — Interface.{1 0 0}

Historical (flow archives, not consulted by agents during normal operation):
- `flows/4decf7/reports/*` — Portion, Prospective throughout
- `flows/01a03d6e/reports/*`, `flows/01a03eda/*`, `flows/01a03603/reports/*` — Channel.{}, Interface.{}, Dotos-in-orchestrate references

---

## Sources

- `/git/github.com/LiGoldragon/*/Cargo.toml` — direct dependency declarations
- `/git/github.com/LiGoldragon/*/flake.nix` — flake input declarations
- `/git/github.com/LiGoldragon/CriomOS/flake.lock` — CriomOS repo references
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock` — CriomOS-home repo references
- `/git/github.com/LiGoldragon/lojix/Cargo.lock` — lojix transitive deps
- `/home/li/primary/flake.nix` — primary flake inputs (curriculum-deploy)
- `/home/li/primary/protocols/repos-manifest.dotos` — lifecycle field
- `git log`, `git status --porcelain`, `git merge-base --is-ancestor` — commit and ancestry data
- `grep -r` across `/home/li/primary` — old-shape search
