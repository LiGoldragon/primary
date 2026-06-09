# Handover — Spirit Daemon-Config Relocation into signal-spirit — 2026-06-09

## How to use this handover

This is a mid-task handover for a fresh operator session. The thread is the
**New Spirit production OS cutover** (continues reports/operator/343 and 344).
Read 344 first (the commit-1 recon + the B-core plan), then this. The current
focused task is **relocating the spirit daemon `Configuration` type into the
`signal-spirit` contract crate** so the daemon imports + wraps it, per the
proven `terminal`/`signal-terminal` exemplar. One half is landed; the spirit-side
rewire is the next concrete chunk (precise steps in §5).

Operator lane currently holds: `/git/.../signal-spirit` + `/git/.../spirit`
(orchestrate/operator.lock). Release when the rewire lands or you stop.

## 1. The goal

Switch the OS's production `spirit` from the deployed `persona-spirit` stack to
the new schema-derived `spirit`. Commit-1 (per report 343) = (a) close the spirit
Nix derivation for offline build, (b) ship a way to prebuild `configuration.rkyv`.
Along the way the psyche steered the work onto the **durable contract shape**:
the daemon's `Configuration` type belongs in the `signal-spirit` contract, not in
the daemon crate (record `q3q7`). That relocation is the current task.

## 2. Landed and pushed (verified green)

| Repo | main | What |
|---|---|---|
| `spirit` | `6eb31976` | **Offline Nix closure** — flake vendors `signal-spirit` + `version-projection` (corrected report 343: the leak was `version-projection`, not `signal-frame`). `nix build .#default` closes offline. |
| `triad-runtime` | `6ea83162` (0.6.1) | **Rename `DaemonConfiguration` trait → `BindingSurface`** (the socket-and-storage binding surface the emitted daemon spine reads; old name carried `Daemon`-ancestry + shadowed the data type). |
| `schema-rust-next` | (was `261c7795`/0.5.2) | **Emit `BindingSurface`** (tracks the trait rename). NOTE: main has since advanced to `c0f76c2` by another agent ("emit new(impl Into<String>) for string newtypes") — see §8. |
| `spirit` | `98be1e21` | **Track the rename** (impl `BindingSurface`, repin triad-runtime/schema-rust-next, regenerated daemon bound). |
| `spirit` | `a9d41bfc` → reverted by `da31d0b4` | build-time-emit docs — **WRONG, reverted** (framed the daemon as owning its contract locally / signal-spirit as migration-only). |
| `spirit` | `2c33016e` | **sub-step 1: Configuration emitted from `spirit/schema/signal.schema`** — this is the MISPLACED version; the rewire (§5) reverts it. Also gated `production_database_sandbox` behind `production-migration` (a real pre-existing fix), synced Cargo.lock revs. |
| `signal-spirit` | `87b45edb` (0.5.1) | **Add `SpiritDaemonConfiguration`** (the config type's correct home) — socket/meta/db/trace `ConfigurationPath` fields + `from_rkyv_bytes`/`to_rkyv_bytes` + archive error, hand-rolled in signal-spirit's idiom, copied from `signal-terminal::TerminalDaemonConfiguration`. Compiles green. |
| `primary` | (main) | reports/operator/344 + this handover. |

`spirit` main is currently `da31d0b4`; `spirit` and `signal-spirit` both build in
the meantime (spirit still has its crate-local `Configuration` at `2c33016e`,
signal-spirit now also exposes `SpiritDaemonConfiguration`).

## 3. THE architecture understanding (hard-won — do not re-derive wrong)

I misread this **four times** by spot-grepping; the authoritative answer (from
intent records + the `terminal` exemplar) is:

- **The ordinary signal WIRE contract lives in the `signal-spirit` repo, and the
  daemon IMPORTS its types.** Records: `f8ds` ("the daemon imports all Signal
  types from the contract crate; the contract repository IS the canonical source
  for client-facing Signal types" — the workspace template), `26e7` (VeryHigh:
  "the Signal wire contract lives in the contract repos and stays wire-only"; only
  Nexus/SEMA schemas stay in the daemon), `k2o1` (VeryHigh: components emitting
  their own contract in-repo is "a migration gap, not a tombstone"), `q3q7`
  (config TYPE belongs in the ordinary signal-component contract).
- **`spirit/schema/signal.schema` owning the working signal contract is the
  migration gap, not the target.** Only `spirit/schema/nexus.schema` +
  `sema.schema` legitimately live crate-local.
- **The PROVEN, COPYABLE exemplar is `terminal`/`signal-terminal`:**
  - `signal-terminal/schema/lib.schema` + `build.rs` (`ContractCrateBuild::from_environment(...)`)
    emits the wire types, including `TerminalDaemonConfiguration`.
  - `terminal/src/config.rs` does `use signal_terminal::TerminalDaemonConfiguration`,
    then defines a **local `Configuration` that WRAPS it** (`raw:
    TerminalDaemonConfiguration` + derived `PathBuf`s) and impls
    `triad_runtime::DaemonConfiguration` (→ now `BindingSurface`) **on the local
    wrapper**. `from_binary_path` → `TerminalDaemonConfiguration::from_rkyv_bytes`
    then wrap.
- **The wrapper IS the canonical pattern.** My earlier "emit Configuration
  locally so there's no newtype" was the divergence. Because the daemon imports a
  *foreign* contract type, the local wrapper carrying the `BindingSurface` impl is
  necessary and correct (orphan rule) — exactly what `terminal` does.
- **Form nuance (open, separate):** `signal-spirit` is currently hand-rolled
  `signal_channel!` (commit `3c6fd6c` deliberately deleted its earlier
  schema-derived form). `signal-terminal` is schema-driven. Whether `signal-spirit`
  should migrate hand-rolled→schema-driven is the bigger `k2o1` / designer-558
  open question ("either migrate them to schema-next or formally bless spirit's
  in-crate schema as the shared source"). The current task adds the config type in
  signal-spirit's *current hand-rolled* idiom — it does NOT take on that migration.

## 4. What `signal-spirit` now has (landed)

`signal-spirit/src/lib.rs` (main `87b45edb`):
- `pub struct ConfigurationPath(String)` — newtype, `new`/`as_str`.
- `pub struct SpiritDaemonConfiguration { socket_path, meta_socket_path:
  Option, database_path, trace_socket_path: Option }` (all `ConfigurationPath`),
  with `new`/`with_meta_socket_path`/`with_trace_socket_path`, `&str` accessors,
  `from_rkyv_bytes`/`to_rkyv_bytes`.
- `pub enum SpiritDaemonConfigurationArchiveError { Encode, Decode }`.

## 5. NEXT: the spirit-side rewire (precise — copy `terminal/src/config.rs`)

1. **`spirit/Cargo.toml`**: make `signal-spirit` a **non-optional** dependency
   (the daemon imports it now). It's currently `optional = true` behind
   `production-migration` (line ~57). Keep `production-migration` working but the
   crate must always be linked.
2. **`spirit/schema/signal.schema`**: **remove** the `ConfigurationPath` +
   `Configuration` lines I added (revert sub-step 1's schema change). Then
   **regenerate** `src/schema/signal.rs`: from the repo,
   `nix develop --command bash -c 'SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check'`
   (local; needs network for git deps). Confirm `Configuration`/`ConfigurationPath`
   are gone from `src/schema/signal.rs`.
3. **`spirit/src/config.rs`**: rewrite the local `Configuration` to **wrap**
   `signal_spirit::SpiritDaemonConfiguration` — copy `terminal/src/config.rs`
   verbatim-ish: `struct Configuration { raw: SpiritDaemonConfiguration,
   socket_path: PathBuf, meta_socket_path: Option<PathBuf>, database_path: PathBuf,
   trace_socket_path: Option<PathBuf> }`; `from_raw`; `from_binary_path` →
   `SpiritDaemonConfiguration::from_rkyv_bytes` then `from_raw`; `impl
   BindingSurface for Configuration` (delegating to the stored `PathBuf`s); keep
   `new`/`with_meta_socket_path`/`new_with_trace`/`write_binary_file` (the tests
   use them — build the inner `SpiritDaemonConfiguration` and wrap; `write_binary_file`
   writes `raw.to_rkyv_bytes()`). `ConfigurationError` stays.
4. **`spirit/src/lib.rs`**: `Configuration` already comes from `config` again
   (after sub-step 1 it was re-exported via... check: `pub use config::{...}`).
   Ensure `pub use config::{Configuration, ConfigurationError};` (NOT
   `schema::signal::Configuration`). The witness
   `crate_root_does_not_reexport_generated_plane_nouns` (record `k4d9`) forbids
   `pub use schema::signal::...` at the crate root — but `config::Configuration` is
   the hand-written wrapper now, so re-exporting it from `config` is fine.
5. **Re-pin `signal-spirit`** in spirit: `nix flake update signal-spirit-source`
   (→ `87b45edb`), and `cargo update -p signal-spirit` (so Cargo.lock rev+version
   match — see §8 gotcha). The flake already vendors signal-spirit (from the
   closure work).
6. **Verify**: offline `nix build .#default -L --max-jobs 0`, then
   `.#checks.x86_64-linux.test` + `.#checks.x86_64-linux.binary-boundary-test`.
   (`production_database_sandbox` is gated; the 3 `generated_signal_plane`
   bracket-string failures are pre-existing — bead `primary-5top`, not yours.)
7. Bump `spirit` version per `hg78` if behavior changes (the wrapper is
   behavior-neutral on the wire — judgement call; the closure/rename/sub-step-1
   were left unbumped as behavior-neutral). Commit + push spirit; release the lock.

## 6. Open / deferred (beads)

- **`primary-iumz`** (P2): fleet migration `DaemonConfiguration → BindingSurface`
  in the ~17 other triad daemons (agent, cloud, criome, domain-criome, harness,
  introspect, message, mind, orchestrate, persona, persona-spirit,
  repository-ledger, router, system, terminal, terminal-cell, lojix). They build
  on pinned `triad-runtime` until each bumps (`cb0j` one-at-a-time). `terminal`
  still uses the old `DaemonConfiguration` name (seen in its config.rs).
- **`primary-5top`** (P2): 3 pre-existing `generated_signal_plane` bracket-string
  snapshot failures in spirit, under epic `primary-36iq` (NOTA bracket-string
  migration). Unmasked when sub-step 1 gated `production_database_sandbox`.
- **Bigger, separate (k2o1 / designer-558):** migrate `signal-spirit` itself from
  hand-rolled `signal_channel!` → schema-driven (give it `schema/lib.schema` +
  `ContractCrateBuild` build.rs like `signal-terminal`), and have `spirit` import
  the WHOLE wire contract from it (not just the config type). This closes the
  migration gap fully. Designer/psyche call on timing + the hand-rolled-vs-schema
  form. Not in the current scoped task.
- **B sub-step 3 (deferred):** fold `archive_target` into the config + make the
  daemon startup arg a meta `Configure` message wrapping the config type
  (`ur16`/`t803`); the `Configure` VERB belongs in `meta-signal-spirit` (which is
  unbuilt — `lxu6`). Then the `spirit-write-configuration` helper. See report 344 §B.

## 7. Corrections & lessons (don't repeat my mistakes)

- **Build the durable shape; never recommend ship-now-migrate-later.** I
  recommended a transitional shape; ESSENCE "What I am not optimising for" forbids
  it. (psyche corrected.)
- **Never gloss intent with approval valence** ("sanctioned", "blessed") the
  psyche didn't state, and never invert a corrective record into an approving one.
  I called the all-in-one pilot a "sanctioned exception" — it never was. (psyche
  corrected; record `lc2r` was rewritten → `26e7` to excise an agent-inserted
  "named bootstrap exception" clause, then `lc2r` removed.)
- **Read the authoritative per-repo `INTENT.md` BEFORE claiming/documenting.** I
  misread the spirit/signal-spirit architecture repeatedly by spot-grepping
  instead of reading `signal-spirit/INTENT.md` + the records.
- **Size effort to the request; don't over-fire workflows.** I launched a 4-agent
  workflow for what one careful doc read would answer.
- **No harness-dependent memory.** AGENTS.md forbids the Claude Code per-user
  memory store (`~/.claude/.../memory/`); lessons go in workspace files
  (ESSENCE/INTENT/skills/reports). (I had wrongly written two memory files; removed.)

## 8. Gotchas & mechanics

- **Never `nix build ... | tail`** in a background task — the runner reports
  `tail`'s exit code (0), masking nix failures. Run unpiped; the output file has
  the log. Confirm success by the `result` symlink, not the reported code.
- **Version bump → stale Cargo.lock.** Bumping a crate's `version` in Cargo.toml
  leaves Cargo.lock's self-version (and, for git deps, the rev) stale; the
  sandbox runs `cargo --locked` and fails. Fix: bump the self-version in
  Cargo.lock too, and for a dependency on a freshly-pushed rev use
  `cargo update -p <crate>` (updates rev+version together). The spirit flake
  DELETES git source lines and vendors, so the rev in spirit's lock is cosmetic
  but the VERSION must match the vendored crate.
- **Regen mechanism:** spirit's `build.rs` runs `write_or_check` — with
  `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check` it rewrites `src/schema/*.rs`;
  otherwise it verifies freshness. The offline flake build runs it in check mode,
  so committed `src/schema/*.rs` must match the emitter's output.
- **`schema-rust-next` advanced** to `c0f76c2` ("emit new(impl Into<String>) for
  string newtypes"). When you re-pin/regen spirit, you may pull this; it changes
  emitted newtype constructors. Re-pin deliberately and re-verify the freshness
  check; expect the regenerated `src/schema/*.rs` to gain `new(impl Into<String>)`
  on string newtypes.
- **Witness:** `tests/public_surface.rs` (`crate_root_does_not_reexport_generated_plane_nouns`,
  record `k4d9`) string-greps `src/lib.rs` and FAILS on any `pub use
  schema::signal::` / `schema::nexus::` / `schema::sema::` / `schema::meta_signal::`
  at the crate root. Route generated-plane-noun consumers through the full plane
  path (`spirit::schema::signal::X`); the hand-written `config::Configuration`
  wrapper is exempt (it's not a generated noun).
- **nota-opt-in check** (`flake.nix` `nota-surface-is-opt-in`) greps only
  `src/config.rs`, `src/daemon.rs`, `src/bin/spirit-daemon.rs` for `nota_next`/
  `NotaSource` and fails if present. Keep the daemon files NOTA-free.
- **`--max-jobs 0`** sends builds to the remote builder (prometheus); use it for
  the heavy Rust compiles (intent `jb73`/`cqit`).

## 9. Key intent records

`q3q7` (config type in the ordinary signal contract), `f8ds` (daemon imports
Signal types from the contract crate — the triad template), `26e7` (Signal
contract lives in contract repos, wire-only; rewritten from the removed `lc2r`),
`k2o1` (in-repo contracts are a migration gap not a tombstone), `u4st` (prebuild
configuration.rkyv; daemon binary-only), `ur16`/`t803` (startup arg is a meta
`Configure` message wrapping the config type; bootstrap+runtime config share one
type), `n0ss` (exactly two contracts per component: signal-X + meta-signal-X),
`lxu6` (meta-signal-spirit is new/unbuilt), `cb0j` (one-component-at-a-time
migration), `k4d9` (don't flatten generated plane nouns to the crate root),
`hg78` (bump component version per change), `6x2k`/`9y0r`/`d0k8` (build from
`github:` after push, not local path).

## 10. Files to read (exemplars)

- `terminal/src/config.rs` — the wrapper pattern to copy for spirit's config.rs.
- `signal-terminal/src/lib.rs` (the `TerminalDaemonConfiguration` impl ~line 186)
  + `signal-terminal/schema/lib.schema` + `signal-terminal/build.rs` — the
  contract-crate shape (relevant for the bigger §6 signal-spirit schema migration).
- `signal-spirit/src/lib.rs` — `SpiritDaemonConfiguration` (already added).
- `spirit/src/config.rs` — current crate-local `Configuration` (to be rewritten as
  the wrapper).
- reports/operator/343, 344 — the cutover investigation + commit-1 recon + B plan.
