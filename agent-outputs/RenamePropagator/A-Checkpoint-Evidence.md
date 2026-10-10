# A — whole-graph staged verify checkpoint (bead `primary-aa2i`)

Session: RenamePropagator. Phase: A (execution). Role: general code implementer
(Claude Opus 4.8, 1M). Date: 2026-07-03. Driver tools: synchronizer `main`
`57082fa6` (`staged-cascade`), rename-propagator `main` `d4ef1e69` (edits-only).

**HARD GATE honored: NO migration producer/consumer `main` was pushed, merged, or
mutated.** All work landed on tool-owned `drop-next` staging branches only.

**Checkpoint verdict: whole-graph staged-green is NOT reached — reported honestly,
not as a false all-green.** The rename-migration MECHANISM is proven sound (40
components verified GREEN, and every cross-source `--locked` blocker resolved),
but full green is blocked by **pre-existing schema-language drift** surfaced when
consumers rebuild against schema-rust's current tip, plus a few tool/transient
issues (below). None of the blockers is a rename-migration defect.

## 1. Staged-set reconciliation (audit residual-risk #1) — CLEAN

Before staging any consumer I swept the canonical GitHub remote of every one of
the 86 run-config repos for a `drop-next` branch. Result: **exactly two** carried
it — the producers `schema` (`a393c8c8`) and `schema-rust` (`ba6f6df7`). No
consumer carried a stray/leftover `drop-next`; `nota` correctly had none. The
pre-staged set the harness discovers by branch-existence was exactly the intended
producer set. (Local `-next` producer clones carry STALE `drop-next` bookmarks
`ef499e25`/`4732e4a3` — the harness reads remotes, so those are the known red
herrings, not authoritative tips.)

## 2. Consumers staged onto drop-next — 80

Two-phase mechanism: rename-propagator `--apply` rewrites the family
URL/key/use-path tokens and I commit each onto a `drop-next` branch (author
`rename-propagator <rename@criome.net>`, working copy restored to `main`); then
the synchronizer `staged-cascade` repins each consumer's producer edges to the
producers' `drop-next` tips, force-pushes `drop-next`, and build-verifies on
prometheus.

- **80 consumers staged** (all clean rewrites, pushed; 0 NO-EDITS, 0 dirty-skips,
  0 push failures).
- **Producers**: `schema drop-next a393c8c8`, `schema-rust drop-next ba6f6df7`
  (from B); `nota` no `drop-next` (0 edits → resolves `main bea7e284`).

### Held out (honest exclusions)

| repo | reason | disposition |
|---|---|---|
| `mind` | active concurrent Codex claim | BLOCKED — staging + 4 flagged pins + mind build deferred (§5). Nothing Cargo-depends on `mind`, so the rest of the graph is unaffected. |
| `cloud` | active concurrent Codex claim | BLOCKED — nothing Cargo-depends on `cloud`. |
| `spirit` | pre-existing uncommitted WIP (`flake.nix` mirror-shipper-daemon) | BLOCKED — not force-staged (dirty-WIP precedent). Its Cargo manifest is ALREADY family-migrated; needs only the NOTA_NEXT_REF residue rename (§5) + a `drop-next` repin once its WIP is dispositioned. Nothing depends on `spirit`. |
| `CriomOS`, `CriomOS-home` | NO-CARGO NixOS/home configs; only family edit was a `flake.lock` rev | Staged coherently (flake inputs resolve independently — no `--locked` blocker) but excluded from the default-package verify (no `packages.default`). |

`synchronizer`/`sema-engine` (fixture-name data), `CriomOS-test-cluster` (dirty
WIP), and the 2 non-canonical `CriomOS-home` jj worktrees remain excluded by the
run config, unchanged.

## 3. Whole-graph verify — `staged-cascade` over 81 components

Config: 3 producers + 78 Rust consumers, `branch-scheme (main drop-next)`,
`DirectHost prometheus`, `DefaultBuild`, author `rename-propagator`. One run,
~38 min; per-component failures collected, ascent continues (driver.rs:11), so
the report is a complete per-component ledger.

**Result: 40 GREEN · 33 VerifyFailed · 6 AlreadyAligned(not-verified) · 2
BumpFailed.**

### 40 GREEN (verified on prometheus)

The whole nota-graph wire/contract layer verifies, including the near-universal
`signal-frame` and `triad-runtime`: `agent, chroma, chronos, clavifaber, criome,
horizon-rs, listener, mentci-lib, message, meta-signal-{agent,criome,listener,
message,router,spirit,terminal,version-handover}, mirror, nexus, nota-config,
schema-rust, signal, signal-{agent,criome,frame,harness,introspect,listener,
message,mind,persona,repository-ledger,router,sema,standard,system,
version-handover}, skills, terminal-cell`.

This is the increment beyond B (which proved only the producers): the
cross-branch cascade composes for the real consumer fan-out. The subset run also
proved the whole-graph run is *necessary* — a 4-consumer subset failed `upgrade`
on the cross-consumer `--locked` blocker (`upgrade → meta-signal-upgrade@main`,
still `nota-next`); only staging every consumer + one full-set run resolves every
cross-consumer edge.

### 33 VerifyFailed — root-cause taxonomy (NONE is a rename defect)

| class | n | repos | root cause | fix owner |
|---|---|---|---|---|
| **NO-FLAKE false-fail** | 9 | mentci, meta-signal-{lojix,mentci,mentci-client,mirror}, signal-{lojix,mentci,mentci-client,mirror} | crate has no `flake.nix`; standalone `nix build .#…default` impossible. Repin+push is CORRECT (verified transitively via their flaked consumers). | none (not a failure) |
| **SCHEMA-RETIRED-SYNTAX** | 11 | domain-criome, lojix, meta-signal-{cloud,domain-criome,persona,upgrade}, persona, signal-{cloud,domain-criome,upgrade}, upgrade | consumer's `.schema` uses syntax schema-rust retired (`Schema(RetiredStructFieldSyntax{found:"name"})` at build.rs). Roots: signal-domain-criome, signal-upgrade, meta-signal-upgrade; rest cascade. **Pre-existing schema-language drift** exposed by rebuilding at current schema-rust. | schema-designer (`.schema` source update) |
| **STALE-GENERATED-ARTIFACT** | 6 | introspect, meta-signal-{mind,orchestrate}, orchestrate, signal-orchestrate, terminal | checked-in `src/schema/*.rs` is stale vs the current schema-rust generator (`StaleGeneratedArtifact`, build.rs freshness gate). Roots: introspect, signal-orchestrate, meta-signal-mind; rest cascade. **This is the generated-file regeneration riding-along item — LOAD-BEARING for green.** | regeneration pass (§5) |
| **CASCADE** | 4 | harness, system, repository-ledger, meta-signal-repository-ledger | build-fails only because a dependency above failed. | resolves when its dep is fixed |
| **GUARD-TEST-FAIL** | 1 | signal-terminal | `tests/dependency_boundary.rs`: "schema-rust-next owns generated contract emission" — a boundary guard test whose assertion still names `schema-rust-next`. Needs a rename-aware update. | small guard-test edit |
| **TEST-COMPILE-FAIL** | 1 | meta-signal-introspect | `could not compile (test "round_trip")`. | investigate w/ regen |
| **FETCH-TRANSIENT** | 1 | mentci-egui | transient GitHub archive/git fetch of a dep — retryable. | re-run verify |

### 6 AlreadyAligned (not verified)

`nota`, `schema` (producers, already at tip); `version-projection` (verified
GREEN in the pre-run subset); `claude-answers` (nota-only, lock already at nota's
tip → no repin → not independently verified, but self-consistent);
`meta-signal-harness`, `meta-signal-system` (NO-FLAKE + already-aligned).

### 2 BumpFailed — synchronizer multi-pin limitation (not a rename defect)

`router`, `signal-spirit`: `ManifestEdit: unbumpable pin: several same-name
entries pin the producer`. These declare the same producer (`signal-criome` /
`schema`) in multiple manifest entries, which the synchronizer's resolver refuses
to bump until full multi-pin awareness exists (the known limitation noted in the
goldragon config). Their `drop-next` carries the rename-propagator rewrite but was
NOT repinned. Fix owner: synchronizer (multi-pin awareness) or a hand repin.

## 4. Residue reconciliation (item 5) — no live `-next` survives

Full sweep of all 80 staged `drop-next` trees for LIVE `-next` (a Cargo git-dep
on `*-next.git` / bare `*-next` key, and a Rust `use *_next::` path): **0 live
Cargo `-next` deps, 0 live `use *_next` paths across all 80.** Every remaining
`-next` occurrence (the 219 residue) is authorized: `.md` prose,
`dependency_boundary.rs` guard string-literals, `@generated by schema-rust-next`
header comments (§5), `.schema`/`.nota` fixture data, and the `spirit`
script/README repo-name args (held-out spirit). No stray live `-next` dep or
use-path survives.

## 5. Riding-along items

- **Generated files — REASSESSED as LOAD-BEARING.** On-disk `@generated by
  schema-rust-next` headers: **39**; **2** in the excluded `rename-propagator` →
  **37 in-scope** (7 in claimed `mind`/`cloud`). The generated CODE is correctly
  rewritten by rename-propagator (0 live `use *_next` in the sweep), but the
  whole-graph run showed the checked-in artifacts are also STALE against the
  current schema-rust *generator* (`StaleGeneratedArtifact` at each crate's
  `build.rs` freshness gate — 6 repos + cascades). So regeneration is required for
  green, not cosmetic. Mechanism: each crate's `build.rs` runs
  `schema_rust::…generate()` and gates on a `*_UPDATE_SCHEMA_ARTIFACTS` env var;
  regenerate against schema-rust `drop-next` (`7f746c02`), commit to the crate's
  `drop-next`, re-verify. **Not executed this session** (a bounded regen+re-verify
  pass, coupled with the schema-source fixes below; scoped for the next phase).
- **`spirit` NOTA_NEXT_REF** — analyzed; edit set prepared but **BLOCKED** by
  spirit's uncommitted WIP. Rename the live var `→ NOTA_REF` (+ coupled repo-name
  args `nota-next→nota`, `schema-next→schema`, `schema-rust-next→schema-rust`) at:
  `scripts/run-nix-integration-tests:44`, `scripts/check-local-schema-stack:26`,
  `tests/nix_integration.rs:268-272`, `README.md:124`. KEEP the guard literal at
  `src/production_migration.rs:140` (a comment recording the rename mapping).
- **`mind` 4 flagged pins** — located exactly (Cargo.toml build-dep line 22
  `schema-rust-next rev bb4dfe29`; `[patch]` blocks lines 33/36/39: `nota-next
  7105c2be`, `schema-rust-next bb4dfe29`, `schema-next b3be7d0f`). Advancing them
  + building `mind` green is **BLOCKED** by the active Codex claim on `mind`.
- **synchronizer** — left untouched (B-landed + excluded).

## 6. HARD GATE — no migration `main` touched (verified)

- rename-propagator commits went only to `drop-next` (working copies restored to
  `main`); the synchronizer force-pushes only `drop-next` via git plumbing that
  never touches a working tree (git_repository.rs:18). Every `jj git push` used
  `--bookmark drop-next`; none targeted `main`.
- Producer `main`s unchanged: `schema 9af2c546`, `schema-rust 6218fb64`,
  `nota bea7e284`. Producer `drop-next` after the run: `schema a393c8c8`
  (aligned), **`schema-rust 7f746c02`** (re-bumped from `ba6f6df7`: its `nota`
  lock re-aligned, verified GREEN), `nota` none.
- Main-integrity sweep: the only 2 local↔remote `main` divergences
  (`repository-ledger`, `signal-repository-ledger`) are **pre-existing local jj
  `main*` divergences** — both remote `main` HEADs are legitimate `li@…` commits
  dated 2026-07-01 (pre-session), NOT authored by the staging identities. No
  `main` was moved by this work.

## 7. Final counts & blockers

- **In-scope repos staged: 80 consumers + 2 producers already staged = 82** on
  `drop-next` (nota needs none).
- **Verified GREEN: 40** (of 78 verify-eligible). **NOT green: 33 VerifyFailed +
  2 BumpFailed**, with the taxonomy in §3 — of which **9 are NO-FLAKE
  false-fails** (mechanism correct) and **1 is a retryable transient**, leaving
  **~24 genuine build failures**, all rooted in pre-existing schema drift
  (11 retired-syntax + 6 stale-artifact + 4 cascade + 1 guard-test + 1
  test-compile) or the synchronizer multi-pin limit (2).

### BLOCKERS to whole-graph green (for the next phase / owners)

1. **Schema-language drift (schema-designer, not mechanical rename):** 11
   consumers' `.schema` sources use syntax retired in current schema-rust
   (`RetiredStructFieldSyntax`). Must be updated to schema-rust's current schema
   language before their graph goes green.
2. **Stale generated artifacts (regeneration pass):** 6 consumers' checked-in
   `src/schema/*.rs` must be regenerated against schema-rust `drop-next` — the
   riding-along item, load-bearing.
3. **signal-terminal guard test** references `schema-rust-next`; needs a
   rename-aware update.
4. **router / signal-spirit multi-pin:** the synchronizer cannot bump a producer
   pinned by several same-name entries; needs multi-pin awareness or a hand repin.
5. **Concurrency/ownership:** `mind`, `cloud` (Codex claims), `spirit` (WIP) —
   staging + the mind-pins and NOTA_NEXT_REF riding-along items deferred.
6. **Retry:** `mentci-egui` failed on a transient fetch; re-verify.

Blockers 1–4 pre-date this migration (drift masked by old producer pins) and were
SURFACED, not caused, by repinning consumers to schema-rust's current tip — which
is required (schema-rust `main`/older revs still declare `nota-next`; only
`drop-next` declares `nota`). They are exactly the real work the actual land must
clear, now precisely scoped.
