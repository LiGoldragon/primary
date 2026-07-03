# A — whole-graph staged-green checkpoint (bead `primary-aa2i`)

Session: RenamePropagator. Phase: A (execution). Role: general code implementer
(Claude Opus 4.8, 1M). Date: 2026-07-03. Driver tools: synchronizer `main`
`57082fa6` (`staged-cascade`), rename-propagator `main` `d4ef1e69` (edits-only).

HARD GATE honored: NO migration producer/consumer `main` was pushed, merged, or
mutated. All work landed on tool-owned `drop-next` staging branches only.

> Status of the whole-graph verify run: see § "Whole-graph verify" — filled from
> the `synchronizer … staged-cascade` report over the full component set.

## 1. Staged-set reconciliation (audit residual-risk #1) — CLEAN

Before staging any consumer, I swept the canonical GitHub remote of every one of
the 86 run-config repos for a `drop-next` branch (`git ls-remote --heads`).
Result: **exactly two** repos carried `drop-next` — the two producers
`schema` (`a393c8c8`) and `schema-rust` (`ba6f6df7`). No consumer carried a
stray/leftover `drop-next`; `nota` correctly had none (0 edits). So the
pre-staged set the harness discovers by branch-existence was exactly the intended
producer set — no unrelated `drop-next` pollutes the cascade. (The local `-next`
producer clones carry STALE `drop-next` bookmarks `ef499e25` / `4732e4a3`; the
harness reads remotes, so those are the known red herrings, not the authoritative
tips.)

## 2. Consumers staged onto drop-next

Mechanism (two-phase, per the B design): rename-propagator `--apply` rewrites the
family URL/key/use-path tokens (`nota-next→nota`, `schema-next→schema`,
`schema-rust-next→schema-rust`) and I commit each onto a `drop-next` branch
(author `rename-propagator <rename@criome.net>`), working copy restored to `main`
(non-invasive); then the synchronizer `staged-cascade` repins each consumer's
producer edges to the producers' `drop-next` tips, force-pushes `drop-next`, and
build-verifies on prometheus.

- **80 consumers staged** onto `drop-next` (all clean rewrites, pushed): the 83
  swept consumers minus the 3 held out (below). All 80 reported STAGED with
  family edits; 0 NO-EDITS, 0 dirty-skips, 0 push failures.
- **3 producers**: `schema` `drop-next a393c8c8`, `schema-rust`
  `drop-next ba6f6df7` (already staged by B); `nota` no `drop-next` (0 edits,
  resolves to `main bea7e284`).

### Held out of this pass (honest exclusions)

| repo | reason | disposition |
|---|---|---|
| `mind` | active concurrent Codex claim ("fix Mind log path…") | BLOCKED — staging + the 4 flagged pins + mind build deferred (see §5) |
| `cloud` | active concurrent Codex claim ("fix DigitalOcean gopass…") | BLOCKED — deep app consumer; nobody Cargo-depends on it, so its exclusion breaks no other build |
| `spirit` | pre-existing **uncommitted WIP** (`flake.nix` mirror-shipper-daemon, bookmark pushed 2 h ago) | BLOCKED — not force-staged (dirty-WIP precedent). Its Cargo manifest is ALREADY family-migrated (`nota.git`/`schema.git`/`schema-rust.git`); it needs only the NOTA_NEXT_REF residue rename (§5) + a `drop-next` repin once its WIP is dispositioned |

`synchronizer` + `sema-engine` were already out of the sweep (fixture-name data);
`CriomOS-test-cluster` + the 2 non-canonical `CriomOS-home` jj worktrees were
already excluded by the run config. Those exclusions are honored unchanged.

### Held out of the default-package verify (staged, not nix-verified)

- `CriomOS`, `CriomOS-home` — NO-CARGO NixOS/home configs; their only family
  edit was a `flake.lock` rev. A flake input resolves independently (no
  `--locked` cross-source blocker), so they are staged coherently, but a
  `nix build .#packages…default` is meaningless for them. Kept staged; excluded
  from the synchronizer verify config (would false-fail on "no default package").

## 3. Whole-graph verify (staged-cascade over the full set)

Config: 81 components (3 producers + 78 Rust consumers), `branch-scheme
(main drop-next)`, `DirectHost prometheus`, `DefaultBuild`, author
`rename-propagator`. One `synchronizer … staged-cascade` run; per-component
failures are collected, the ascent continues (driver.rs:11), so the report is a
complete per-component ledger.

Cross-consumer coupling is real and was proven necessary: a 4-consumer subset run
FAILED `upgrade` because it Cargo-depends on `meta-signal-upgrade@branch=main`,
whose un-staged `main` still declares `nota-next` — the exact `--locked`
cross-source blocker, one level out. Only the WHOLE-graph run (every consumer
staged AND a component, so every cross-consumer edge repins to a `drop-next` tip)
resolves it. The dependency map confirms the web is almost entirely `branch`
pins (synchronizer-handleable); the only `rev` pins are inside the excluded
`mind`; and nothing Cargo-depends on the excluded `mind`/`cloud`.

> **[VERIFY RESULTS — finalized from the completed run report below.]**

## 4. Residue reconciliation (item 5) — no live `-next` survives

Full sweep of all 80 staged `drop-next` trees for LIVE `-next`: a Cargo git-dep
URL on `*-next.git` (or bare `*-next` dep key) and a Rust `use *_next::` /
`pub use *_next::` path. **Result: 0 live Cargo `-next` deps, 0 live `use *_next`
paths — across all 80.** Every remaining `-next` occurrence (the 219 residue) is
authorized: `.md` prose, `dependency_boundary.rs` guard string-literals (must
stay), `@generated by schema-rust-next` header comments (see §5), `.schema`/`.nota`
fixture data, and the `spirit` script/README repo-name args (in the held-out
`spirit`). No stray live `-next` dep or use-path survives in any staged in-scope
repo.

## 5. Riding-along items

- **`spirit` NOTA_NEXT_REF variable** — analyzed; edit set prepared. The env var
  naming is already asymmetric (`SCHEMA_REF`/`SCHEMA_RUST_REF` were de-`-next`ed;
  only nota's stayed `NOTA_NEXT_REF`). Live occurrences to rename `→ NOTA_REF`:
  `scripts/run-nix-integration-tests:44`, `scripts/check-local-schema-stack:26`,
  `tests/nix_integration.rs:268`, `README.md:124` (plus the coupled repo-name args
  `nota-next→nota`, `schema-next→schema`, `schema-rust-next→schema-rust` on those
  lines). Guard literal that STAYS: `src/production_migration.rs:140` (a comment
  recording the rename mapping). **BLOCKED** by spirit's uncommitted WIP — the
  edit belongs on spirit's `drop-next` and must not disturb the active flake.nix
  work; deferred with the exact edit list above.
- **Generated files (39 vs 28)** — reconciled. On-disk `@generated by
  schema-rust-next` headers: **39**; **2** inside the excluded `rename-propagator`
  → **37 in-scope**, of which **7 are in the claimed `mind` (4) / `cloud` (3)**.
  The 39-vs-28 gap is header-vs-code: rename-propagator rewrites the generated
  CODE (`use nota_next::`→`use nota::`, verified: 0 live `use *_next` in the sweep)
  but not the header COMMENT. The files are produced by each crate's `build.rs`
  calling `schema_rust(_next)::…generate()`, so the header self-heals to
  `@generated by schema-rust` on the next build/regen. Header-comment refresh +
  formal regenerate-and-diff is a bounded cosmetic follow-up (per-repo generator
  runs; does not affect build-green); the code drift is already nil.
- **`mind` 4 flagged pins** — located exactly (Cargo.toml build-dep line 22
  `schema-rust-next rev bb4dfe29`; `[patch]` blocks: `nota-next rev 7105c2be`,
  `schema-rust-next rev bb4dfe29`, `schema-next rev b3be7d0f`). Advancing them to
  post-rename revs + building `mind` green is **BLOCKED** by the active Codex
  claim on `mind`; not touched.
- **synchronizer** — left alone (already B-landed + excluded); its dep/fixtures
  untouched.

## 6. HARD GATE — no migration `main` touched

- Producer `drop-next` tips are the staging targets; producer/consumer `main`s
  were never a push target. rename-propagator commits went only to `drop-next`
  (working copies restored to `main`); the synchronizer force-pushes only the
  `staging` branch `drop-next` via git plumbing that never touches a working copy
  (git_repository.rs:18 invariant).
- Spot-verified mains unmoved at their pre-migration commits (`schema` 9af2c546,
  `schema-rust` 6218fb64, `signal-standard` 895015c2, `lojix` a3553334, `upgrade`
  5098cbae, `router` 14f85574); a full main-integrity check (no `main` HEAD
  authored by the staging identities) is in § "Main-integrity".

## 7. Blockers

1. `mind`, `cloud` — active concurrent Codex claims (staging + mind pins/build
   deferred; nothing else depends on them so the rest of the graph is unaffected).
2. `spirit` — pre-existing uncommitted WIP; staging + NOTA_NEXT_REF rename
   deferred pending the WIP owner's disposition.

None of these are structural blockers to the migration; they are
concurrency/ownership boundaries, honestly deferred.
