# Scout Dependency Graph — LiGoldragon Repos Manifest Discovery

## Task and scope

Read-only discovery. Map cross-repo dependency edges among the ~116 repos under
`/git/github.com/LiGoldragon/` to feed a repos-manifest ACTIVE vs deprecatable
proposal. Dependencies are the key signal: a repo depended on by live repos is
active; an orphan (no edges in or out) is a deprecation candidate.

No edits, no commits. Every edge below is backed by a parsed `flake.nix` input
or `Cargo.toml` git/path dependency. Observation (edges found) is kept separate
from interpretation (hub/leaf/orphan classification).

## Sources and method (observed)

- Repo set: `ls /git/github.com/LiGoldragon/` → 117 entries; `lojix-primary-5rzf-7`
  excluded as a transient jj workspace of `lojix` (matches the prior
  coverage-gap map). **116 repos** analyzed.
- Edge extraction over every repo:
  - Nix flake inputs: `rg -o 'github:LiGoldragon/<name>'` in each `flake.nix`
    (94 repos have one).
  - Rust deps: `rg -o 'github.com/LiGoldragon/<name>'` in every `Cargo.toml`
    (git deps + `[patch]` + workspace members; 95 repos have one; `find`-walked
    each repo, excluding `target/`, `.jj/`, `.git/`).
  - `.gitmodules`: **none present** in any repo (checked all 116).
- Cleaning: dropped self-references (workspace-internal path deps such as
  `agent -> agent`) and edges whose target is not itself a LiGoldragon repo dir.
- Result: **491 directed edges** among 116 repos. Adjacency dump written to
  `/tmp/adjacency2.txt`; raw edge list `/tmp/clean_edges2.txt` (both transient).
- Spirit `PublicTextSearch [repos manifest active deprecate]` returned only
  generic privacy/architecture principles — **no repos-manifest or deprecation
  intent** is recorded; not load-bearing for this map.

### Edges referencing repos NOT present under LiGoldragon (observed)

These targets are referenced by a live repo but have **no matching directory**
under `/git/github.com/LiGoldragon/` (verified absent). They are the older
generation the `-next` crates supersede, plus genuine externals:

- `nota` (referenced by `nota-next`) — superseded predecessor of `nota-next`.
- `schema` (by `schema-next`), `schema-rust` (by `schema-rust-next`) — likewise.
- `persona-spirit` (by `CriomOS-test-cluster` flake).
- `annas-mcp` (by `CriomOS-home` flake), `tree-sitter-cozo` (by `CriomOS-emacs`) —
  third-party.
- `nixpkgs` and standard flake-utils — external, not counted as edges.

Interpretation: these are not deprecation candidates in the LiGoldragon set
(they are absent); flag only that `CriomOS-test-cluster` still references a
`persona-spirit` input that no longer exists locally — a possibly-stale edge.

## PART A — Adjacency summary (OBSERVED)

IN = number of LiGoldragon repos that depend on this repo (dependents).
OUT = number of LiGoldragon repos this repo depends on.
Full per-repo dependents/dependsOn lists are in `/tmp/adjacency2.txt`.

### Most-depended-on repos (IN-degree ranking, IN ≥ 2)

| IN | OUT | Repo | Role |
|---:|---:|---|---|
| 79 | 1 | **nota-next** | universal typed-config/serialization crate — nearly everything |
| 66 | 2 | **signal-frame** | the wire kernel; every Signal contract + daemon |
| 50 | 7 | **schema-rust-next** | schema-derived Rust codegen build dep |
| 28 | 0 | **rust-build** | shared Nix rust builder (`lib.${system}`) |
| 24 | 0 | **kameo** | vendored actor-runtime fork (patch target) |
| 21 | 3 | **triad-runtime** | shared component runtime library |
| 17 | 3 | signal-persona | persona wire contract; broadly consumed |
| 14 | 3 | sema-engine | Sema classification engine |
| 12 | 2 | schema-next | schema next-gen |
| 11 | 3 | signal-criome | criome wire contract |
| 6 | 7 | criome | criome daemon (also a consumer) |
| 6 | 3 | signal-harness | |
| 6 | 3 | signal-message | |
| 6 | 1 | version-projection | version-adjacent projection lib |
| 5 | 5 | signal-introspect | |
| 5 | 3 | signal-router | |
| 5 | 1 | signal-sema | |
| 5 | 3 | signal-terminal | |
| 4 | 3 | meta-signal-mentci | |
| 4 | 7 | mirror | mirror daemon (consumer + provider) |
| 4 | 3 | signal-domain-criome | |
| 4 | 4 | signal-mentci | |
| 4 | 4 | signal-mind | |
| 4 | 6 | signal-orchestrate | |
| 3 | 0 | CriomOS-lib | consumed by the three CriomOS repos |
| 3 | 7 | lojix | deploy daemon; consumed by CriomOS family |
| 3 | 4 | meta-signal-criome | |
| 3 | 17 | router | PersonaRouter daemon (also a big consumer) |
| 3 | 3 | signal-mirror | |
| 3 | 3 | signal-system | |
| 3 | 6 | terminal-cell | |
| 3 | 30 | spirit | psyche-facing daemon; consumed by CriomOS-home/test-cluster/persona |
| 2 | 0 | CriomOS-pkgs | |
| 2 | 1 | horizon-rs | consumed by lojix + test-cluster |
| 2 | 7 | mentci-lib | |
| 2 | 7 | message | |
| 2 | 3 | meta-signal-mentci-client | |
| 2 | 3 | meta-signal-mirror | |
| 2 | 6 | meta-signal-orchestrate | |
| 2 | 3 | meta-signal-router | |
| 2 | 3 | meta-signal-terminal | |
| 2 | 4 | meta-signal-upgrade | |
| 2 | 1 | sema | Sema vocabulary root |
| 2 | 4 | signal | legacy signal crate (consumed by nexus, signal-forge) |
| 2 | 4 | signal-agent | |
| 2 | 3 | signal-cloud | |
| 2 | 3 | signal-lojix | |
| 2 | 3 | signal-repository-ledger | |
| 2 | 6 | signal-spirit | |
| 2 | 2 | signal-standard | |
| 2 | 4 | signal-upgrade | |
| 2 | 9 | upgrade | |
| 2 | 7 | agent | agent daemon (consumed by CriomOS-home + spirit) |
| 2 | 13 | mentci | mentci daemon (consumed by CriomOS-home + mentci-egui) |

### Repos with exactly ONE dependent (IN = 1) — depended-on but narrowly

`CriomOS` (by test-cluster), `CriomOS-home` (by CriomOS), `CriomOS-emacs`,
`brightness-ctl`, `chroma`, `clavifaber`, `hexis`, `substack-cli`, `whisrs`
(all by `CriomOS-home` or `CriomOS`); `harness`, `introspect`, `mind`,
`orchestrate`, `system`, `terminal` (each by `persona`); `repository-ledger`
(by CriomOS); `signal-derive` (by `signal`); `signal-mentci-client` (by
mentci-egui); `signal-version-handover` (by orchestrate); every single-daemon
`meta-signal-*` (each by its own daemon); `mentci-egui` (by CriomOS-home);
`meta-signal-cloud`/`meta-signal-domain-criome` (by cloud/domain-criome).

## PART B — Classification (INTERPRETATION)

Definitions: **HUB** = high IN-degree, many dependents (removal breaks many
repos). **LEAF** = IN = 0 but OUT > 0 (a top-level consumer: a product, entry
point, or test rig — nothing builds on it, but it is actively wired up).
**ORPHAN** = IN = 0 AND OUT = 0 (no dependency edge in or out — deprecation
candidate on the dependency signal alone).

### HUBS (foundation — unambiguously ACTIVE)

Tier-1 (huge fan-in, foundational): **nota-next (79), signal-frame (66),
schema-rust-next (50), rust-build (28), kameo (24), triad-runtime (21)**.
Removing any of these breaks most of the graph.

Tier-2 (contract/engine hubs, IN 5–17): **signal-persona (17), sema-engine (14),
schema-next (12), signal-criome (11), signal-harness, signal-message,
version-projection, signal-introspect, signal-router, signal-sema,
signal-terminal**. These are the shared wire/engine layer; clearly active.

### LEAVES (top-level consumers — ACTIVE, nothing depends on them)

These have IN = 0 but wire up real dependencies; they are products / entry
points / rigs, not deprecation candidates:

- **persona** (OUT=32) — the top consumer; the aggregate agent product.
- **spirit** (OUT=30, but ALSO IN=3) — technically a hub+leaf; it is a daemon
  consumed by CriomOS-home/test-cluster/persona AND consumes 30 repos. Active.
- **cloud** (OUT=9) — cloud family root; ACTIVE (consumes signal-cloud,
  meta-signal-cloud, signal-domain-criome, triad-runtime, ...).
- **domain-criome** (OUT=8) — domain-criome family root; ACTIVE.
- **CriomOS-test-cluster** (OUT=9) — the regression fixture rig; consumes
  CriomOS/lojix/mirror/router/spirit/upgrade/criome/horizon-rs. Active fixture.
- **CriomOS** (OUT=11, IN=1) and **CriomOS-home** (OUT=12, IN=1) — mutually
  referencing OS roots; active.
- **skills** (OUT=4) — generator source; ACTIVE (the maintained skills checkout
  lives in `repos/`, per the coverage-gap map).
- **chronos** (OUT=2), **nota-config** (OUT=2), **nexus** (OUT=4),
  **nexus-cli** (OUT=1), **signal-forge** (OUT=1), **kameo-testing** (OUT=1),
  **meta-signal-version-handover** (OUT=3) — consumers with no dependents.
  Lower-signal leaves: their activity should be corroborated by commit recency
  (the coverage-gap map has last-commit dates), since "nothing depends on it"
  plus "few deps" is a weaker liveness signal.

### ORPHANS — no dependency edges in OR out (18 — DEPRECATION CANDIDATES)

These have zero parsed dependency edges to or from any other LiGoldragon repo.
On the dependency signal alone they are deprecation candidates. **11 are
non-code repos** (no `flake.nix` and no `Cargo.toml` — books, notes, sites,
firmware, config), for which "no dependency edge" is expected and NOT by itself
evidence of deprecation; they are content/asset repos.

Non-code orphans (expected to have no edges — judge by purpose/recency, not deps):

- `AnaSeahawk-website` — Hugo site (least active, 2025-12-01 per prior map)
- `ArtificialIntelligence` — AI notes README
- `BookOfGoldragon` — autobiographical notes
- `BookOfLuna` — Luna AI notes
- `TheBookOfSol` — notes/book
- `caraka-samhita` — study/translation working repo
- `criomos-horizon-config` — pan-horizon config source (config data, not a crate)
- `goldragon` — (content)
- `library` — (content/research)
- `lore` — (content)
- `qmkBinaries` — QMK firmware binaries

Code orphans (have a `flake.nix` and/or `Cargo.toml` but NO edge in or out —
strongest deprecation candidates on the dependency signal):

- **arca** — code repo, zero edges. Prime deprecation candidate.
- **forge** — Cargo repo (self-only `forge -> forge`); no external edge.
  Note: `signal-forge` exists and depends on `signal`, not on `forge`; forge
  itself is isolated. Deprecation candidate.
- **kibord** — keyboard/keymap repo; isolated.
- **persona-pi** — Nix-packaged Pi harness; has a `flake.nix` but no
  LiGoldragon flake inputs and no dependents. Isolated despite the `persona`
  name — NOT wired into the persona graph.
- **tree-sitter-nota** — grammar repo; no parsed edge. Likely used at build/dev
  time via a path not captured by Cargo/flake parsing (grammars are often
  vendored). Weak-evidence orphan; verify before deprecating.
- **tree-sitter-schema** — same caveat as tree-sitter-nota.
- **WebPublish** — web publishing; isolated.

The 7 CODE orphans of real interest for deprecation are: **arca, forge, kibord,
persona-pi, tree-sitter-nota, tree-sitter-schema, WebPublish** (with the
grammar caveat noted). Boundary note to prevent confusion: `substack-cli`,
`whisrs`, `hexis`, `brightness-ctl`, `chroma`, `CriomOS-emacs`, `CriomOS-pkgs`,
`CriomOS-lib` all have IN=1 (consumed by the CriomOS family) — they are NOT in
the orphan set and are NOT deprecation candidates.

## Named families from the handover (dependency view — OBSERVED)

- **Cloud surface:** `cloud` (leaf root, OUT=9) → `signal-cloud` (IN=2),
  `meta-signal-cloud` (IN=1), `signal-domain-criome`. Internally connected,
  active; nothing outside consumes `cloud` itself (it is a top-level daemon).
- **domain-criome:** `domain-criome` (leaf root, OUT=8) → `signal-domain-criome`
  (IN=4, also consumed by cloud/meta-signal-cloud), `meta-signal-domain-criome`
  (IN=1). Active; `signal-domain-criome` is a shared contract bridging cloud and
  domain-criome.
- **meta-signal-\*:** every `meta-signal-X` has IN=1 or 2 (consumed by its `X`
  daemon and sometimes `spirit`) and OUT 3–6 (consumes nota-next, signal-frame,
  schema-rust-next, its `signal-X`). All are ACTIVE contract crates, none orphan.
- **mentci family:** `mentci` (OUT=13, IN=2), `mentci-lib` (IN=2), `mentci-egui`
  (leaf, OUT=10), `signal-mentci` (IN=4), `signal-mentci-client` (IN=1),
  `meta-signal-mentci` (IN=4), `meta-signal-mentci-client` (IN=2). Dense, active.
- **mirror:** `mirror` (IN=4, OUT=7) consumed by CriomOS, test-cluster, router,
  spirit; `signal-mirror` (IN=3), `meta-signal-mirror` (IN=2). Active hub-ish.
- **lojix:** `lojix` (IN=3: CriomOS, CriomOS-home, test-cluster; OUT=7),
  `signal-lojix` (IN=2), `meta-signal-lojix` (IN=1), `horizon-rs` (IN=2, feeds
  lojix + test-cluster). Active.
- **repository-ledger:** `repository-ledger` (IN=1 from CriomOS, OUT=8),
  `signal-repository-ledger` (IN=2), `meta-signal-repository-ledger` (IN=1).
  Active, low fan-in but wired into CriomOS.

## Checks run (exact)

- `for d in */; do [ -f "$d/flake.nix" ]...` → 94 flakes, 95 Cargo repos, 0 `.gitmodules`.
- Two-pass Python extraction; first pass had a `.git`-strip bug truncating some
  targets (`agen`, `nota-nex`); **fixed** with a bounded regex and re-verified
  (e.g. `spirit -> agent`, `skills -> nota-next` now resolve correctly).
  Final: 116 repos, 491 edges, 18 orphans, 12 pure leaves.
- Verified the 6 non-LiGoldragon edge targets are genuinely absent as dirs.
- `spirit "(PublicTextSearch ...)"` → no manifest/deprecation intent recorded.

## Blockers, unknowns, follow-up (named)

- **Weak-evidence orphans:** `tree-sitter-nota`/`tree-sitter-schema` grammars and
  any C/build-time integration are NOT visible to flake/Cargo parsing; do not
  deprecate on dependency-absence alone. Verify how NOTA/schema tooling consumes
  the grammars (likely `tree-sitter generate` at dev time, or a path not in a
  parsed manifest).
- **Non-code orphans are expected to have no edges;** they must be judged by
  purpose and commit recency (in the coverage-gap map), not by this graph.
- **Absent predecessor targets** (`nota`, `schema`, `schema-rust`,
  `persona-spirit`): a live repo references them but they are gone locally —
  potentially stale inputs (esp. `CriomOS-test-cluster`'s `persona-spirit`
  flake input). Flag for the synthesizer as edges-to-nowhere, not orphans.
- **Not checked:** transitive reachability / cycle analysis, GitHub remote
  liveness, commit recency (available in the sibling coverage-gap map —
  synthesizer should join on it), and whether any repo is consumed only via a
  Nix `follows`/indirect path not captured by `github:LiGoldragon/` matching.
- **`repos/`-symlink vs `/git`:** this graph is over `/git` directly and is
  independent of the campaign's symlink coverage; join to the coverage-gap map
  for the ACTIVE-and-covered vs ACTIVE-but-missed cross-tab.
