# Tier2-Regen-Evidence — schema-artifact regeneration + test-literal fixes on drop-next

Session: RenamePropagator. Phase: Tier 2 (execution). Role: general code
implementer (Claude Opus 4.8, 1M). Date: 2026-07-03/04. Beads: `primary-qipw`
(6-repo regen), `signal-terminal` slice of `primary-zy24` (guard-test literal),
`primary-djb0` (mentci-egui re-verify).

Producer baseline (regenerated against): `schema-rust@drop-next 7f746c02`,
`schema@drop-next a393c8c8`, `nota@main bea7e284`. Each consumer's Cargo.lock
already pinned exactly these revs (synchronizer staged-cascade), so a local
`cargo build --locked` runs the correct generator.

## SAFETY GATE — HELD (verified)

No migration `main` was touched. Every push was `jj git push --bookmark
drop-next`. Post-work remote `main` HEADs are byte-for-byte the session-start
values:

| repo | remote main (unchanged) |
|---|---|
| introspect | 7b53b37e |
| meta-signal-mind | ee3afc10 |
| meta-signal-orchestrate | 2fa05874 |
| orchestrate | 0c8e67fe |
| signal-orchestrate | 76a663a2 |
| terminal | 985dc926 |
| signal-terminal | bd858e0c |

## Regen mechanism

Each crate's `build.rs` runs `schema_rust::…generate()` and gates the checked-in
`src/schema/*.rs` on a `<CRATE>_UPDATE_SCHEMA_ARTIFACTS` env var
(`write_or_check`). Regen = `<VAR>=1 cargo build --locked` (writes the artifact);
drift check = (a) run regen twice and confirm the artifact is byte-identical
(idempotent md5), then (b) `cargo clean -p <crate> && cargo build --locked`
(no var) → the freshness gate re-runs on a clean build and exits 0. The
authoritative green is the prometheus `nix build …#packages.x86_64-linux.default`
against the pushed drop-next tip (a clean sandbox that runs build.rs fresh and,
for `packages.default`, also the `cargo test` checkPhase).

## Internal dependency order among the 6

Roots (own stale artifact, no internal producer dep): `introspect`,
`meta-signal-mind`, `signal-orchestrate`. Cascade:
`meta-signal-orchestrate` → signal-orchestrate; `orchestrate` →
signal-orchestrate + meta-signal-orchestrate; `terminal` → (its own artifact
only; deps are signal-terminal/meta-signal-terminal/terminal-cell). Cascade
consumers required a Cargo.lock bump to the regenerated root tips so the roots'
freshness gates are satisfied during the consumer build.

## Per-repo disposition (all drop-next only)

| repo | drop-next before | drop-next after | change | drift | prometheus |
|---|---|---|---|---|---|
| signal-orchestrate | d4cb8676 | **b6ada30a** | regen (1-line header) | idempotent+gate OK | GREEN |
| introspect | 01d01bea | **c3b70639** | regen (1-line header, daemon.rs) | idempotent+gate OK | GREEN |
| meta-signal-mind | 972117b4 | **ae03d038** | regen (lib.rs, 81+/39-) | idempotent+gate OK | GREEN |
| meta-signal-orchestrate | 9b090e5a | **9cf46ba6** | regen (header) + lock bump signal-orchestrate→b6ada30a + stale schema-contract test counts 7→8 / 11→12 | idempotent+gate OK; full test suite OK | GREEN |
| orchestrate | 0f28fda8 | **f763c966** | regen (3 headers) + lock bump signal-orchestrate→b6ada30a, meta-signal-orchestrate→9cf46ba | idempotent+gate OK | GREEN |
| terminal | 064f88e5 | **0bc75661** | regen (4 files, 524+) + WirePath/ComponentName access adaptation (src+test) | idempotent+gate OK; full test suite OK | GREEN |

All six regenerated on drop-next, drift-clean, GREEN on the prometheus builder.

### Regen was NOT sufficient for two repos — additional fixes (disclosed)

Clearing the StaleGeneratedArtifact gate let the compile/checkPhase proceed and
surfaced two pre-existing, non-regen issues that blocked full green. Both were
fixed with minimal, verified changes; neither is a rename defect.

- **terminal — generated-newtype API adaptation.** The current generator emits
  path/name domain newtypes (`WirePath(String)`, `ComponentName(String)`) with a
  `payload()` accessor and NO `AsRef` impl. Hand-written `src/config.rs`,
  `src/supervisor.rs` (7 socket/store path sites) and
  `tests/terminal_supervisor.rs` (1 ComponentName site) called `.as_ref()` on
  them, relying on an AsRef that the generator does not emit (signal-terminal's
  own `main` ships these newtypes without AsRef and is green, so `.payload()` is
  the ecosystem convention). Adapted the path sites to `.payload().payload()`
  and the ComponentName site to `.payload().as_str()`, matching the existing
  `.payload().payload()` socket_mode idiom in the same files. `cargo build`
  (release) + full test suite pass locally; prometheus `packages.default`
  (incl. checkPhase) GREEN. The local `cargo build` alone did NOT catch the test
  site (it doesn't compile tests) — the prometheus checkPhase did, and the fix
  was verified there.

- **meta-signal-orchestrate — stale schema-contract test counts.**
  `tests/schema_contract.rs` asserted the lowered schema has 7 input / 11 output
  variants; the schema source (`schema/lib.schema`, byte-identical on main and
  drop-next) defines 8 input ops and 12 output replies (the `ArchiveWorktree` /
  `WorktreeArchived` operation, added in the repo's own `main` HEAD "add
  ArchiveWorktree to nexus schema", was never reflected in the test). Updated the
  literals 7→8 and 11→12 (verified by counting the schema enums; imports count 9
  unchanged). Full test suite passes; prometheus GREEN. This is a pre-existing
  stale test literal (same class as zy24), surfaced by clearing the gate, not
  caused by the regen.

## primary-zy24 — signal-terminal slice

`signal-terminal` drop-next `729a04a9` → **`4f75a6c5`**.
`tests/dependency_boundary.rs`: the stale POSITIVE assertion
`cargo_toml.contains("schema-rust-next")` (message "schema-rust-next owns
generated contract emission") updated to `contains("schema-rust")` (manifest is
correctly migrated: 1× `schema-rust`, 0× `schema-rust-next`). The LEGITIMATE
negative boundary guards `!contains("signal-engine-management")` and
`!contains("signal-persona-origin")` left LITERAL and still passing. Its
checked-in schema artifact is already fresh (regen no-op). Guard test passes;
prometheus `packages.default` GREEN. (Out of my slice: signal-upgrade /
meta-signal-upgrade guard literals — behind the retired-syntax blocker, other
owner.)

## primary-djb0 — mentci-egui re-verify

drop-next `ee84ae10` (unchanged; read-only re-verify, no edits). Direct
`ssh prometheus nix build …` fails — root cause identified and RECLASSIFIED:
not a mentci-egui/migration defect and not a plain transient, but a
**prometheus builder credential issue**. The crane `vendorCargoDeps` step fetches
the (uncached) private Cargo git dep `meta-signal-mentci-client@d7abb5b0` (its
current drop-next tip, valid) and prometheus's nix git fetcher fails with
`fatal: could not read Username for 'https://github.com': No such device or
address`. Other private deps build only because they are already cached in the
prometheus store; this rev was never cached (mentci-egui failed in the A run
too). The same `builtins.fetchGit` succeeds locally (my credentials).

**mentci-egui itself is GREEN.** Driving `nix build` from my credentialed
machine (which vendors the deps locally and offloads the compile to prometheus
as a remote builder) succeeds end-to-end: EXIT 0 →
`/nix/store/ivsiw3sp6pdddpyc14xybdkjwjn3cxyk-mentci-egui-0.1.0`, with the crate
compiled on prometheus. So the code and the migration are fine; the direct
`ssh prometheus nix build` failure is purely the builder's inability to fetch an
uncached private repo without credentials.

**BLOCKER (infra, flagged for the operator / whole-graph convergence):**
prometheus's nix git fetcher lacks a working GitHub credential for uncached
private `github.com/LiGoldragon/*` repos. Any direct-on-prometheus build whose
private Cargo git deps are not already cached will fail the same way. Workaround
used here: drive the build from a credentialed machine with prometheus as remote
builder. Durable fix (out of implementer scope): configure prometheus's
`access-tokens` / git credential for private-repo fetches.
