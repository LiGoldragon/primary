# Proposal — repos manifest and active set (review gate)

Decision-support proposal for the psyche to review at a gate. Agents propose;
the psyche decides. This report recommends an active/deprecate classification
over the ~116 LiGoldragon repos, a concrete manifest design to replace the stale
`repos/` symlink surface, a safe `repos/` deprecation path, the coverage-gap
work list, and the exact decisions the psyche must make.

Nothing here was executed. No repo edited, no tracker mutated, no deprecation
performed. The only write is this file.

EVIDENCE and RECOMMENDATION are separated in every section. Every deprecate call
states CONFIDENCE and what remains unverified.

## Sources consulted (read-only)

- `agent-outputs/RepoManifestDiscovery/Scout-MissedRepos.md` — 54 missed repos;
  all remotes live/unarchived; 43 carry real `INTENT.md`; 2 no-fold-target
  (`CriomOS-test-cluster`, `signal-standard`); dependents never scanned.
- `agent-outputs/RepoManifestDiscovery/Scout-CoveredRepos.md` — 62 covered; fold
  held (0 residual `INTENT.md`); 6 lack `ARCHITECTURE.md`; all live.
- `agent-outputs/RepoManifestDiscovery/Scout-DependencyGraph.md` — 491 edges;
  hubs, 18 zero-edge orphans (11 content, 7 code), `CriomOS-test-cluster`'s
  dangling `persona-spirit` flake input.
- `agent-outputs/PerRepoDoctrineCoverageGap/Scout-SituationalMap.md` — dormancy /
  last-commit dates joined for liveness calls.
- `reports/legacy-disposition/HANDOVER-2026-06-30-coverage-gap-and-repos-deprecation.md`
  — settled intent: deprecate `repos/`; direction lives in `ARCHITECTURE.md`.
- Workspace conventions: `ARCHITECTURE.md` §3 "Repos surface", §4 "Boundaries";
  `protocols/active-repositories.md`; `RECENT-REPOSITORIES.md`; the
  `.nota` manifest pattern in `repos/skills/manifests/` (`skills-roster.nota`,
  `module-dependencies.nota`); skills `repo-intent`, `architecture-editor`,
  `intent-manifestation`, `nota-design`.
- Spirit read-only: `(PublicTextSearch [repos manifest inventory active
  deprecate])` and `(PublicTextSearch [repository ledger symlink repos
  surface])`.

EVIDENCE — Spirit carries **no repos-manifest, inventory, or active-set intent**.
Both public text searches returned only generic privacy/architecture/documentation
principles (`k09z`, `qjrf`, `c5nq`, `t5qr`, ...), none about a repos inventory.
The dependency scout's own `PublicTextSearch` reached the same negative.
Consequence: manifest **shape** is matter (a workspace convention), not Spirit
intent — it lands in workspace files, and the psyche decides the shape at this
gate. The one durable rule that bites is `qjrf`: do not invent psyche-authorized
status; where the active/deprecate call is unverified, surface it as a question,
which this proposal does.

## Current inventory surfaces (EVIDENCE — three overlapping, all partly stale)

There is not one inventory today; there are three, and they disagree.

1. `repos/` — 64 symlinks + 3 real dirs. 62 symlinks point into
   `/git/github.com/LiGoldragon/<name>`; 2 point into `../private-repos/`
   (`assistant-reports`, `counselor-reports`). The 3 real dirs are the canonical
   `skills` checkout, its jj workspace `skills-primary-ascl-doctrine`, and the
   `spirit` jj workspace `spirit-guardian-config`. `repos/` is git-ignored
   (`/repos/` in `.gitignore`) and untracked. It was never re-synced as new repo
   families were added → it exposes only 62 of 116 repos → it is the root cause
   of the 47% doctrine-campaign miss.
2. `RECENT-REPOSITORIES.md` — a tracked prose table, "broad checkout index",
   regenerated 2026-06-09. Lists ~102 repos but with **stale membership**: it
   still lists `lojix-cli` and `persona-spirit` (both since retired/absent) and
   its last-commit dates are a month old.
3. `protocols/active-repositories.md` — a tracked, hand-maintained prose
   "attention map" of the core stack. Rich per-repo role prose, but **not a full
   inventory** (omits many repos), and **stale in places**: it lists `terminal`
   as merely "Archived/inactive" (not retired) and `lojix-cli` / `persona-spirit`
   as active.

RECOMMENDATION — the reworked manifest should become the single authoritative
inventory and **supersede all three surfaces**: replace the `repos/` symlink dir
as the coverage/iteration surface, absorb and retire `RECENT-REPOSITORIES.md`,
and let `active-repositories.md`'s rich role prose either migrate into a manifest
field or be demoted to a generated view. Deciding whether to keep
`active-repositories.md` as a human narrative or fold it in is a psyche gate
decision (see §5).

## 1 · Active-set recommendation

Classification: **ACTIVE** (keep, wired or foundational), **CONTENT** (non-code
asset repo, keep, dependency-graph silence is expected), **DEPRECATE-CANDIDATE**
(propose retiring; every one is unverified — see confidence column). No repo is a
confident retire: **dependents/importers were never scanned**, so the "no
dependents" leg of the deprecation test is unproven for every candidate.

### 1a · The bulk — ACTIVE by dependency + recency (no per-repo table)

EVIDENCE — the ~90 repos in the connected dependency graph are unambiguously
ACTIVE and are **not** listed row-by-row here (this is a review artifact):

- Tier-1 hubs: `nota-next` (IN=79), `signal-frame` (66), `schema-rust-next` (50),
  `rust-build` (28), `kameo` (24), `triad-runtime` (21).
- Tier-2 contract/engine hubs (IN 5–17): `signal-persona`, `sema-engine`,
  `schema-next`, `signal-criome`, and the shared `signal-*` wire layer.
- Every `meta-signal-*` and `signal-*` family member (IN 1–4, wired to its
  daemon and often `spirit`).
- Top-level leaves / products / rigs (IN=0 but wire real deps): `persona`,
  `spirit`, `cloud`, `domain-criome`, `CriomOS`, `CriomOS-home`,
  `CriomOS-test-cluster`, `skills`, `chronos`, `nexus`, `nexus-cli`,
  `signal-forge`, `kameo-testing`, `mentci-egui`, `nota-config`.
- The whole cloud / domain-criome / mentci / mirror / lojix / repository-ledger
  families are internally connected and current (June 2026 commits).
- All 62 covered repos and 43 of 54 missed repos pushed in June 2026; no covered
  repo is dormant (oldest last-commit `CriomOS-pkgs`, 2026-05-28).

CONFIDENCE — high. Dependency edges are parsed from real `flake.nix`/`Cargo.toml`;
recency corroborates. No action needed beyond folding them into the manifest as
`Active`.

### 1b · The 7 CODE orphans (zero parsed edges in or out — the real question)

EVIDENCE — these have a `flake.nix` and/or `Cargo.toml` but no parsed dependency
edge to or from any LiGoldragon repo. All remotes live/unarchived.

| Repo | Last commit | RECOMMENDATION | CONFIDENCE | Unverified / caveat |
|---|---|---|---|---|
| `arca` | 2026-06-30 | **ACTIVE — do NOT deprecate** | med-high | Committed *today*; recency contradicts "orphan = dead". Zero edges only means nothing links it yet. Confirm purpose with psyche; do not retire an actively-committed repo. |
| `forge` | 2026-06-30 | **ACTIVE — do NOT deprecate** | med-high | Committed today; `active-repositories.md` names it the criome-stack executor / future Nix build-infra replacement (Truth Pins). Isolated by design, not dead. |
| `persona-pi` | 2026-06-27 | **DEPRECATE-CANDIDATE** | low | Nix-packaged Pi harness; isolated despite the `persona` name (NOT wired into the persona graph). Recent commit weakens the case. Ask psyche if the Pi harness is still a live target. Dependents unscanned. |
| `WebPublish` | last 2026-05-30 | **DEPRECATE-CANDIDATE** | low-med | Web publishing (aski source); isolated; ~5 weeks dormant. `aski*` compiler family is already archived (`RECENT-REPOSITORIES.md`), so its source lineage is retired — but not verified that nothing consumes it. |
| `kibord` | last 2026-05-30 | **CONTENT — keep** | med | Keyboard/keymap (ergodone); hardware artifact, naturally edge-free and low-churn. Not a deprecation signal. Reclassify as content, not code-orphan. |
| `tree-sitter-nota` | last 2026-06-13 | **ACTIVE — do NOT retire (build-time caveat)** | n/a for retire | **BUILD-TIME CAVEAT:** grammars are typically consumed via `tree-sitter generate` / vendored C at dev/build time on a path Cargo/flake parsing does not see. Zero parsed edges is NOT evidence of disuse. Do not retire without verifying the NOTA tooling's grammar consumption path. |
| `tree-sitter-schema` | last 2026-06-13 | **ACTIVE — do NOT retire (build-time caveat)** | n/a for retire | Same build-time caveat as `tree-sitter-nota`. |

RECOMMENDATION — of the 7 code orphans, only **2 are even weak deprecate
candidates** (`persona-pi`, `WebPublish`), both LOW confidence and both requiring
a dependents scan + psyche confirmation. `arca` and `forge` are actively
committed and should stay ACTIVE. The two grammars carry an explicit build-time
caveat and must NOT be retired on dependency-absence alone. `kibord` is really
content.

### 1c · The 11 CONTENT orphans (non-code — keep; edge-silence expected)

EVIDENCE — no `flake.nix`/`Cargo.toml`; books, notes, sites, config, firmware.
"No dependency edge" is expected and is NOT a deprecation signal for these.

`ArtificialIntelligence`, `BookOfGoldragon`, `BookOfLuna`, `TheBookOfSol`,
`caraka-samhita`, `criomos-horizon-config`, `goldragon`, `library`, `lore`,
`qmkBinaries`, plus `AnaSeahawk-website` (also a fork — see 1d).

RECOMMENDATION — all **CONTENT / keep**. Nuances:

- `criomos-horizon-config` — config-data repo, but it IS consumed by `horizon-rs`
  on the `horizon-leaner-shape` arc (`active-repositories.md`); it is config
  content, active, keep.
- `goldragon` — content, but the handover names it a **live jj-only data repo**
  homing `cloud-node-data` records (`t5vj` set). Definitely keep; note it is data,
  not a crate.
- `lore` — content, but hosts the canonical cross-workspace agent contract
  (`repos/lore/AGENTS.md`, per workspace §4). Keep; high-value.
- `AnaSeahawk-website` — the single softest signal: a fork, dormant since
  2025-12-01 (~7 months). Most plausible retire/leave candidate of all repos.
  CONFIDENCE low; it is a personal Hugo site with no dependents expected.
  See 1d — the fork handling decision covers it.

### 1d · Forks (3) — fork status is a keep/own question, NOT a deprecation signal

EVIDENCE — `fork=true` on GitHub: `AnaSeahawk-website`, `kameo`, `whisrs`.

| Fork | RECOMMENDATION | CONFIDENCE | Note |
|---|---|---|---|
| `kameo` | **ACTIVE — keep** | high | It is a **24-dependent HUB** (vendored actor-runtime lifecycle fork; Cargo `[patch]` target). Its fork status is explicitly NOT a deprecation signal. Load-bearing. |
| `whisrs` | **ACTIVE — keep** | med | Voice-to-text dictation tool; IN=1 (consumed by `CriomOS-home`). Actively used despite being a fork. |
| `AnaSeahawk-website` | **DEPRECATE-CANDIDATE** | low | The only fork that is also dormant + edge-free; softest ownership signal. Retire/leave is a psyche call (§5). |

RECOMMENDATION — record `IsFork` as a manifest fact, not a status. Keep `kameo`
and `whisrs` ACTIVE; `AnaSeahawk-website` is the one fork worth a deprecate
question.

### 1e · Private repos (2) — keep; carry substance without leaking it

EVIDENCE — `private=true`: `meta-signal-mentci-client`, `signal-mentci-client`.
Both are live fold-backlog members with `ARCHITECTURE.md` targets and are wired
into the mentci family (IN 1–2).

RECOMMENDATION — both **ACTIVE — keep**. Fold them normally, but keep private
substance out of public surfaces (workspace leak gate + `k09z`). If the manifest
is a public/tracked file, private repos must appear with **name + status only**,
no private role prose, or be listed in a private manifest partition (§5 decision).

### 1f · Covered repos lacking `ARCHITECTURE.md` (6)

`CriomOS-pkgs`, `goldragon`, `library`, `substack-cli`, `tree-sitter-nota`,
`tree-sitter-schema`. All ACTIVE (see §4 for the author-vs-leave call). None is a
deprecation candidate.

### 1g · Summary of deprecate candidates (all unverified)

RECOMMENDATION — the entire deprecate-candidate set is exactly **three, all LOW
confidence, none actionable without a dependents scan**:

1. `AnaSeahawk-website` (dormant fork, ~7 months) — softest, most plausible.
2. `persona-pi` (isolated Pi harness) — recent commit weakens it.
3. `WebPublish` (isolated, retired aski lineage) — needs consumer check.

Everything else is ACTIVE or CONTENT. The two `tree-sitter-*` grammars are
explicitly excluded from retire on the build-time caveat.

BLOCKER for any confident retire — a reverse-dependency scan (who imports/patches
these) has never been run. `qjrf` forbids inventing psyche-authorized status;
these three are surfaced as questions, not decisions.

## 2 · Manifest design

RECOMMENDATION — do NOT invent a foreign format. The workspace already has a
manifest convention: `repos/skills/manifests/*.nota` are positional NOTA records
with a `;;` header, a status enum `(Active ...)` / `(Archived ...)`, and a
per-record kind. Mirror that convention exactly.

### 2a · Home and format

- **Format:** NOTA (`.nota`), positional records, per `nota-design` and the
  existing `skills/manifests/` precedent. NOTA is the workspace's only structured
  data syntax; a machine-readable manifest lets a future coverage run iterate the
  active set directly (closing the stale-symlink root cause).
- **Home:** `protocols/repos-manifest.nota` (tracked, public). `protocols/`
  already owns `active-repositories.md`; the manifest is the structured successor
  and belongs beside it. The workspace `ARCHITECTURE.md` §3 "Repos surface" and
  §4 "Boundaries" are updated to name this file as the authoritative inventory
  (matter → `ARCHITECTURE.md`, per `intent-manifestation`).
- **Private partition:** either a second private manifest
  (`private-repos/repos-manifest-private.nota`) for the 2 private repos, or a
  name+status-only stub in the public manifest. Psyche decides (§5). Default
  recommendation: name+status-only in public, full role prose private, honoring
  the leak gate.

### 2b · Per-record schema (pseudo-NOTA, per `nota-schema-docs`)

```
;; protocols/repos-manifest.nota
;; Authoritative inventory of LiGoldragon repos. Supersedes the repos/ symlink
;; index, RECENT-REPOSITORIES.md, and the inventory role of active-repositories.md.
;; Positional records. One record per repo. Status is the active/deprecate call.

(Repo
  <name>                      ;; bare atom: canonical repo name = /git/.../LiGoldragon/<name>
  <remote>                    ;; bare atom or pipe-text: github:LiGoldragon/<name>
  (Family <family>)           ;; grouping: Signal | MetaSignal | Cloud | DomainCriome | Mentci
                              ;;   | Mirror | Lojix | RepositoryLedger | CriomOS | Nota | Schema
                              ;;   | Sema | Persona | Content | Tooling | Fork | ...
  <status>                    ;; enum variant — see below
  (DoctrineHome <variant>)    ;; where durable direction lives (repo-intent skill)
  [<flag> ...])               ;; optional facts: IsFork IsPrivate BuildTimeConsumed DataRepo

;; status enum (named variants, not flags — nota-design + typed-records-over-flags):
;;   Active
;;   (DeprecateCandidate <reason-pipe-text>)   ;; unverified; carries the caveat
;;   Content                                    ;; non-code asset repo; kept
;;   (Deprecated <disposition-pipe-text>)       ;; only after psyche confirms + execution

;; DoctrineHome enum (repo-intent: ARCHITECTURE.md or a code stub):
;;   Architecture            ;; has ARCHITECTURE.md
;;   (CodeStub <path>)       ;; direction in a code comment
;;   (OtherDoc <path>)       ;; AGENTS.md / README.md / CLAUDE.md (the 6 gap repos)
;;   None                    ;; no direction surface yet (a gap to close)
```

Design notes grounded in doctrine:
- Status is a **named-variant enum**, so `DeprecateCandidate` and `Deprecated`
  carry their reason/disposition as a field — no bool flag soup
  (`typed-records-over-flags`, `nota-design`).
- `Family` groups the ~116 repos so the manifest stays skimmable and a coverage
  run can iterate a family.
- Optional flags (`IsFork`, `IsPrivate`, `BuildTimeConsumed`, `DataRepo`) are
  facts, distinct from status — fork status is not deprecation (1d).
- Fields are positional; adding a trailing optional flag is compatible, per
  `nota-design`.

### 2c · Worked example (3 real repos filled in)

```
;; ...
(Repo nota-next github:LiGoldragon/nota-next (Family Nota)
  Active Architecture [])
(Repo kameo github:LiGoldragon/kameo (Family Fork)
  Active (OtherDoc README.md) [IsFork])
(Repo AnaSeahawk-website github:LiGoldragon/AnaSeahawk-website (Family Content)
  (DeprecateCandidate [|fork, dormant since 2025-12-01, no dependents scanned|])
  None [IsFork])
;; tree-sitter grammar with the build-time caveat as a first-class flag:
(Repo tree-sitter-nota github:LiGoldragon/tree-sitter-nota (Family Nota)
  Active (OtherDoc README.md) [BuildTimeConsumed])
```

### 2d · How it replaces the `repos/` symlink surface as authoritative inventory

EVIDENCE — `repos/` today answers "which repos does the doctrine campaign
iterate?" purely by which symlinks exist. That coupling is exactly the failure:
adding a repo family without adding symlinks silently drops it from coverage.

RECOMMENDATION — the manifest inverts the dependency. A coverage/doctrine run
reads `protocols/repos-manifest.nota`, filters `status = Active`, and iterates
`/git/github.com/LiGoldragon/<name>` **directly** (workers already target `/git`
paths, per the handover). The manifest is the single source of truth for "what
repos exist and their status"; `/git` remains the checkout home; `repos/`
symlinks are no longer needed for coverage and can be deprecated (§3). Editing
tools that need a repo path resolve `<name>` → `/git/.../LiGoldragon/<name>`.

## 3 · `repos/` deprecation approach

### 3a · What `repos/` currently is (EVIDENCE)

- 64 symlinks (62 → `/git/.../LiGoldragon/<name>`, 2 → `../private-repos/…`)
  plus 3 real dirs (canonical `skills` checkout + 2 jj workspaces).
- Git-ignored (`/repos/` in `.gitignore`); untracked; workspace-local only.
- Documented in `ARCHITECTURE.md` §3 and §4 ("owns the `repos/` symlink index").
- Referenced as a path prefix in doctrine and reports (e.g.
  `repos/lore/AGENTS.md`, `repos/skills/...`), and — critically — the 3 real
  dirs are **live working checkouts**, not disposable symlinks.

### 3b · Safe execution path (RECOMMENDATION — sequenced after the manifest)

Deprecation must NOT be a blind `rm -rf repos/`: the 3 real dirs hold the
canonical `skills` checkout and two active jj workspaces. Sequence:

1. **Stand up the manifest first** (§2). Nothing may rely on `repos/` for
   coverage until `protocols/repos-manifest.nota` is authoritative.
2. **Migrate the 3 real entries out of `repos/`.** The `skills` checkout and the
   `skills` / `spirit` jj workspaces need a new home (e.g. move canonical
   `skills` under `/git`, re-point jj workspaces). This is the one genuinely
   destructive step and needs its own careful sub-plan; it is the reason
   deprecation is not trivial.
3. **Re-point path references.** Grep the workspace for `repos/<name>` path
   prefixes (doctrine, reports, `active-repositories.md`, tooling) and rewrite to
   `/git/.../LiGoldragon/<name>` or the manifest-resolved path. Load-bearing
   examples: `repos/lore/AGENTS.md` (the cross-workspace agent contract),
   `repos/skills/...`.
4. **Handle the 2 private symlinks.** `assistant-reports` / `counselor-reports`
   point into `private-repos/`; decide whether the manifest or a direct
   `private-repos/` path replaces them (they are not LiGoldragon `/git` repos).
5. **Remove the symlink set** once nothing references `repos/` for coverage or
   paths. Because `repos/` is git-ignored, removal is a local filesystem change,
   not a commit — but the path-reference rewrites in tracked files ARE commits.
6. **Update `ARCHITECTURE.md` §3 and §4** to describe the manifest as the
   inventory and drop the "`repos/` symlink index" ownership line.

### 3c · Sequencing against manifest stand-up

Manifest stand-up **blocks** `repos/` removal. Order: build manifest → migrate 3
real dirs → rewrite path references → remove symlinks → update `ARCHITECTURE.md`.
Coverage-gap folds (§4) can run **in parallel** with manifest stand-up (they
target `/git` paths directly and do not depend on `repos/`), but the manifest is
the cleaner iteration surface for them once it exists.

## 4 · Coverage-gap disposition

### 4a · The ~43 INTENT.md → ARCHITECTURE.md folds (EVIDENCE + list)

EVIDENCE — 43 missed repos still carry a real (non-stub) `INTENT.md`; 41 already
have an `ARCHITECTURE.md` fold target; all live; all clean working trees.

RECOMMENDATION — fold `INTENT.md` into `ARCHITECTURE.md` per `repo-intent` /
`architecture-editor` (agent-written synthesis backed by psyche statements, then
eliminate the `INTENT.md`), for the 41 repos with an existing target:

`agent`, `BookOfGoldragon`, `clavifaber`, `cloud`, `criomos-horizon-config`,
`domain-criome`, `lojix`, `mentci`, `meta-signal-agent`, `meta-signal-cloud`,
`meta-signal-domain-criome`, `meta-signal-lojix`, `meta-signal-mentci`,
`meta-signal-mentci-client` (private), `meta-signal-mind`, `meta-signal-mirror`,
`meta-signal-orchestrate`, `meta-signal-persona`, `meta-signal-repository-ledger`,
`meta-signal-router`, `meta-signal-spirit`, `meta-signal-terminal`,
`meta-signal-version-handover`, `mirror`, `nota-config`, `persona-pi`,
`repository-ledger`, `rust-build`, `signal-cloud`, `signal-domain-criome`,
`signal-frame`, `signal-lojix`, `signal-mentci`, `signal-mentci-client` (private),
`signal-mirror`, `signal-repository-ledger`, `signal-sema`, `signal-spirit`,
`signal-version-handover`, `triad-runtime`, `version-projection`.

Constraints: keep private substance out of public surfaces for the 2 private
repos. `BookOfGoldragon` has an explicit privacy gate in its own INTENT — honor
it when folding.

### 4b · The 2 authored ARCHITECTURE.md (no fold target)

EVIDENCE — `CriomOS-test-cluster` (129-line INTENT, has `flake.nix`/`checks/`/
`lib/`/`README.md`) and `signal-standard` (63-line INTENT, has `src/`/`schema/`/
`Cargo.toml`/`README.md`) carry substantial real direction but no
`ARCHITECTURE.md`.

RECOMMENDATION — author a new `ARCHITECTURE.md` in each (or a code stub where the
direction is best expressed at a code location, per `repo-intent`), synthesizing
the INTENT direction, then eliminate the `INTENT.md`.

- `CriomOS-test-cluster` — **also resolve the dangling `persona-spirit` flake
  input** (§4d) as part of authoring, since its architecture describes the
  projection→config test pipeline that references it.
- `signal-standard` — its INTENT cites Spirit `eeeo`/`t312`; ground the authored
  ARCHITECTURE in those records when folding (`intent-manifestation`).

### 4c · The 6 covered repos lacking ARCHITECTURE.md (author vs leave)

EVIDENCE — `CriomOS-pkgs` (dir prose in `AGENTS.md`), `goldragon` (`README.md`),
`library` (`CLAUDE.md` one-liner), `substack-cli` (`AGENTS.md`+`README.md`),
`tree-sitter-nota` (`README.md`), `tree-sitter-schema` (`README.md`). None ever
had an `INTENT.md`; the campaign did not regress them; this is a pre-existing gap.
`repo-intent` says direction may live in a code stub, and "a pure skeleton with
no repo-specific direction may carry only structural architecture."

RECOMMENDATION — **do NOT bulk-author `ARCHITECTURE.md` for all 6.** Split:

- **Author** where real psyche-backed direction exists but is homed in the wrong
  file: `substack-cli` and `goldragon` carry direction prose in `AGENTS.md`/
  `README.md` — migrate the durable-direction slice into `ARCHITECTURE.md`
  (`architecture-editor`: durable direction goes in ARCHITECTURE, operating rules
  stay in AGENTS). `goldragon` is also the `cloud-node-data` home — its data role
  is genuine architecture.
- **Leave** the thin ones: `library` (one-line scope), `tree-sitter-nota`,
  `tree-sitter-schema` (2-commit skeletons, README-only) — a skeleton with no
  psyche-specific direction legitimately carries no `ARCHITECTURE.md`. Record
  their `DoctrineHome` as `(OtherDoc README.md)` in the manifest so the gap is
  visible without forcing invented direction (`qjrf`: do not synthesize psyche
  intent to fill a slot).
- **Ask** on `CriomOS-pkgs` — its `AGENTS.md` may or may not carry durable
  direction worth promoting; the psyche should decide (§5).

CONFIDENCE — this is a judgment split, not a fact. The author-vs-leave line is a
psyche gate decision; the recommendation is a default, not authority.

### 4d · CriomOS-test-cluster dangling `persona-spirit` input

EVIDENCE — `CriomOS-test-cluster`'s `flake.nix` references a `persona-spirit`
input that has **no matching directory** under `/git/.../LiGoldragon/`.
`RECENT-REPOSITORIES.md` still lists `persona-spirit` (stale). The active stack
renamed `signal-persona-spirit` → `signal-spirit`; `persona-spirit` looks like a
retired/renamed predecessor.

RECOMMENDATION — resolve as part of authoring `CriomOS-test-cluster`'s
ARCHITECTURE (4b): either re-point the flake input to the current repo
(likely `spirit` or a `signal-spirit`-family target) or remove the dead input.
CONFIDENCE med — the exact correct target needs a one-step check of what
`persona-spirit` supplied; flagged as a decision (§5).

### 4e · Deprecation exclusions from the fold list (explicit)

RECOMMENDATION — exclude any repo recommended for deprecation from the fold work.
Of the deprecate-candidate set (`AnaSeahawk-website`, `persona-pi`, `WebPublish`),
**none carries an `INTENT.md`** except `persona-pi` (which is in the 41-repo fold
list above). If the psyche confirms `persona-pi` as deprecate at the gate,
**remove `persona-pi` from the fold list** — do not author/fold direction into a
repo about to be retired. `AnaSeahawk-website` and `WebPublish` have no INTENT and
are already outside the fold list. This exclusion is stated so the fold worker
does not waste effort on a repo the psyche is retiring.

## 5 · Decisions the psyche must make at the review gate

1. **Confirm the deprecation set.** The proposal has exactly three LOW-confidence
   candidates: `AnaSeahawk-website` (dormant fork), `persona-pi` (isolated Pi
   harness), `WebPublish` (isolated, retired aski lineage). Choose per repo:
   RETIRE / KEEP-ACTIVE / KEEP-AS-CONTENT. Note: a dependents scan has NOT run —
   authorize that scan first, or accept the risk of retiring on dormancy alone.
   (The 2 `tree-sitter-*` grammars are explicitly NOT candidates — build-time
   caveat.)
2. **Approve the manifest shape + home.** Adopt `protocols/repos-manifest.nota`
   as NOTA (mirroring `skills/manifests/`) with the §2b schema (name, remote,
   family, status-enum, doctrine-home, flags)? Confirm home = `protocols/`.
3. **Decide the 6 covered-lacking-ARCHITECTURE repos.** Approve the author-vs-leave
   split: author for `substack-cli` + `goldragon`; leave `library` +
   `tree-sitter-nota` + `tree-sitter-schema` as README-homed; and decide
   `CriomOS-pkgs` (promote its `AGENTS.md` direction, or leave).
4. **Decide fork + private handling.** Confirm forks are a fact-flag not a status
   (`kameo`/`whisrs` stay ACTIVE; `AnaSeahawk-website` is the one fork question in
   #1). For the 2 private repos, choose: name+status-only in the public manifest,
   or a separate private manifest partition (`private-repos/…`).
5. **Resolve the CriomOS-test-cluster dangling `persona-spirit` input.** Choose:
   re-point the flake input to the current target (likely `spirit`/`signal-spirit`
   family) or remove the dead input — settled while authoring its ARCHITECTURE.
6. **(Consolidation call.)** Confirm the manifest SUPERSEDES all three current
   surfaces: retire `RECENT-REPOSITORIES.md`, and decide whether
   `active-repositories.md`'s role prose migrates into a manifest field, becomes a
   generated view, or is kept as a separate human narrative. (Raised because the
   overlap is the deeper root cause; not in the original 5 asks but load-bearing.)

## Recommended auditor

RECOMMENDATION — this is a proposal, not an implementation; the immediate
"audit" is the **psyche review gate** itself (decisions §5). For the downstream
execution that follows approval, recommend a distinct auditor per work stream:

- **Coverage-gap folds (§4a/b):** an ARCHITECTURE/repo-intent reviewer checks each
  fold is psyche-backed synthesis (not inference, per `qjrf`/`repo-intent`),
  `INTENT.md` is eliminated, and no private substance leaked (the 2 private +
  `BookOfGoldragon` privacy gate). Evidence to hand the auditor: the before/after
  `ARCHITECTURE.md` diffs, confirmation of `INTENT.md` removal, and a leak-gate
  pass statement.
- **Manifest + `repos/` deprecation (§2/§3):** a Nix/repo-structure reviewer
  validates the NOTA manifest parses, the 3 real-dir migrations preserved the
  `skills`/`spirit` checkouts, path-reference rewrites are complete (grep proof),
  and no consumer still reads `repos/`. Evidence: manifest parse result, the
  path-reference grep before/after, and a `skills`/`spirit` checkout-intact check.

These findings are provisional recommendations until the psyche accepts them;
distinguish defect review (folds/migrations correct?) from provisional corpus
observations (the three-surface overlap, the unscanned dependents).

## Blockers / unverified (carried, do not lose)

- **No reverse-dependency scan** — the "no dependents" leg is unproven for every
  deprecate candidate. This is the single missing input for any confident retire.
- **Grammar build-time consumption unverified** — `tree-sitter-nota`/`-schema`
  may be consumed at build time on an unparsed path; do not retire on edge-absence.
- **Spirit has no manifest/inventory intent** — manifest shape is matter decided
  at this gate, not Spirit-authorized; do not capture the shape as intent.
- **`persona-spirit` correct re-point target unverified** — needs a one-step
  check of what it supplied to `CriomOS-test-cluster`.
- **INTENT substance sampled, not fully audited** — the 43 folds were size/line
  audited + 9 fully read; all genuine, but the fold worker should read each in
  full at execution.
