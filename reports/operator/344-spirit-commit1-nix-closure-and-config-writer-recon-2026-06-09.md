# Spirit Commit-1 Recon — Nix Closure + Config-Writer, and the q3q7 Config-Type Gap — 2026-06-09

## Frame

New operator onboarding for the Spirit production OS cutover thread (continues
`reports/operator/343-new-spirit-production-os-cutover-investigation-2026-06-09.md`).
I skilled up across the full operator required-reading list and ran read-only
recon on the two commit-1 surfaces report 343 recommended: (1) close the
`spirit` Nix derivation so `nix build .#default` succeeds offline, and (2) ship a
`spirit-write-configuration` helper that prebuilds `configuration.rkyv`.

Fresh Spirit intent queried live this session reshapes the work beyond what
report 343 knew — chiefly `q3q7` (today, High): the daemon configuration type
belongs in the `signal-spirit` contract, not hand-written in the daemon crate.

All facts below are verified directly against source, not inferred.

## Correction to report 343 — the offline blocker is two repos, not one

Report 343 named `signal-frame` as the dependency Cargo tries to fetch from
GitHub inside the derivation. That symptom is real but the diagnosis was one hop
short. `signal-frame` is **already vendored** in `flake.nix` and pinned to the
same commit `spirit` resolves (`#166bda84…`, `Cargo.lock` lines 688/699).

The actual gap: of the 10 distinct `git+https://github.com/LiGoldragon` sources
in `spirit/Cargo.lock`, exactly **two** have no flake input, no vendor copy, no
`[patch]` block, no `.cargo/config.toml` path, and no `Cargo.lock` source-line
deletion:

- `signal-spirit` (`Cargo.lock:718`, rev `3c6fd6c3…`) — optional dep behind
  `production-migration`.
- `version-projection` (`Cargo.lock:921`, rev `f00b239f…`) — a transitive dep of
  `signal-spirit`.

`signal-frame` surfaces in the error only because it is pulled *through*
`signal-spirit`'s unvendored subtree during `craneLib.vendorCargoDeps`, which
vendors the whole locked closure regardless of which features later build steps
enable. `signal-spirit` is **never compiled** by the current build matrix — no
crane target passes `--features production-migration` — so for the `.#default`
goal the fix is purely lockfile/vendor closure, not a compile change.

## The offline-closure recipe (mechanical, no design judgment)

`flake.nix` vendors each LiGoldragon repo via the `runCommand
"spirit-source-with-local-schema-patches"` derivation (lines ~86–183) in seven
steps per repo: flake input `<name>-source { flake = false }`; `cp -R` into
`vendor-sources/<name>`; top-level `Cargo.toml` git→path substitute; inner
`Cargo.toml` git→`../sibling` substitute; `.cargo/config.toml` `paths` entry;
`[patch."…<repo>.git?branch=main"]` block; `sed`-delete the matching
`source = "git+…"` line from `Cargo.lock`.

Apply the same treatment to `signal-spirit` and `version-projection`:

- `signal-spirit`: single crate, no sub-members. Its direct git deps are
  `signal-frame` (default-features off), `nota-next` (optional), and
  `version-projection` — `signal-frame` and `nota-next` are already vendored and
  reused via the existing `[patch]` blocks, so only its inner `Cargo.toml`
  needs `version-projection` → `../version-projection`. Its top-level dep line in
  `spirit/Cargo.toml` carries `, optional = true`, so the `--replace-fail` match
  string must include that exactly.
- `version-projection`: single crate; depends only on `nota-next` (optional,
  already vendored) plus crates.io. Appears only transitively, so it needs the
  inner-`Cargo.toml` patch + a top-level `[patch]` block + `Cargo.lock` deletion,
  but **no** top-level `Cargo.toml` dep-line substitution.

Both pin `signal-frame` to the same already-vendored commit, so no second
`signal-frame` revision is introduced.

**Proof obligations:**

- Acceptance is `nix build .#default -L` succeeding from a **pushed `github:`
  ref**, not the local path checkout (intent `6x2k`/`9y0r`/`d0k8`: build the
  landed artifact from the remote, never a local-path/git+file ref). Use
  `--max-jobs 0` so the remote builder takes the load.
- A `vcin`-compliant **narrow negative guard** check may assert no
  `git+https://github.com/LiGoldragon` source line survives in the vendored
  `Cargo.lock`. Positive grep is not proof; the build succeeding offline is.
- Bump `spirit` from `0.3.0` per `hg78` (every logic change bumps at least the
  patch component).

## The config-writer helper — data layer already exists

`src/config.rs` already carries everything but the CLI edge:

- `struct Configuration { socket_path, meta_socket_path: Option, database_path,
  trace_socket_path: Option }` (each a `ConfigurationPath(String)` newtype).
- Constructors `new`, `new_with_trace`, `with_meta_socket_path`; serializers
  `to_binary_bytes`, `write_binary_file`, `from_binary_path` (rkyv only, no NOTA
  derive — and it must stay that way; the `nota-surface-is-opt-in` flake check
  negative-greps `nota_next` out of `config.rs`/`daemon.rs`).

Missing: a `spirit-write-configuration` `[[bin]]` (currently only `spirit`,
`spirit-daemon`, `spirit-migrate-production` exist), a NOTA text edge, and a
flake package that installs it.

Shape, per the discipline and the existing `src/bin/spirit-migrate-production.rs`
model:

- One argument via `triad_runtime::ComponentCommand` `nota_argument()` (the
  one-argument rule; the helper is a deploy/CLI text edge, so it may parse NOTA
  and encode to rkyv — the daemon never does). Gate it behind `nota-text`, **not**
  `production-migration` (which would couple it to the unvendored `signal-spirit`
  and break offline build).
- A `nota-text` NOTA-mirror record decoded into the rkyv `Configuration` (no NOTA
  derive on `Configuration` itself); typed `thiserror` error; method on a
  data-bearing type, no free functions, no ZST holder.
- Acceptance test extends `tests/process_boundary.rs`: invoke
  `CARGO_BIN_EXE_spirit-write-configuration` to produce `configuration.rkyv`,
  spawn `spirit-daemon` with it, wait for both the working and meta sockets to
  bind; plus the missing-meta-socket rejection
  (`tests/meta_configure.rs::daemon_rejects_missing_meta_socket_before_serving`).

## The design gap — q3q7 / t803 / ur16 (the decision)

All five recon agents converged on a drift the freshly-recorded intent calls out:

- **`q3q7`** (today, High): the daemon configuration *type* belongs in the
  ordinary `signal-spirit` contract, imported by the daemon for binary startup
  decode; "duplicating the configuration struct inside the daemon is drift to
  reconcile." **Code does the opposite:** `Configuration` is hand-written in
  `spirit/src/config.rs`; `signal-spirit` defines no such type (grep: zero hits).
- **`t803`/`ur16`**: the meta-signal `Configure` op should wrap the *same* daemon
  configuration type, so the rkyv startup argument and live meta reconfiguration
  share one wire object. **Code:** startup reads `config.rs::Configuration` (four
  paths); the live meta `Configure` wraps `ConfigureRequest(ArchiveDatabaseTarget)`
  (an archive-target, a different/narrower concern). Two unrelated types.
- A third wrinkle: there are **two meta surfaces** — the daemon serves a
  crate-local `schema/meta_signal.rs` (`Configure`/`ArchiveDatabaseTarget`), while
  the separate `meta-signal-spirit` repo defines an unrelated
  `Start/Drain/Reload/Register/Retire` channel with no `Configure`.

Reconciling this is a **contract/schema redesign** rippling through
`signal-spirit`, the meta schema, the daemon's `load_configuration`, and the meta
listener — and the "unified Configure shape" (does meta `Configure` absorb the
full daemon config, or startup config absorb the archive target, or a union?) is
a design decision, not an operator mechanical call. It is **not mechanically
required** for commit-1's two goals: the helper can ship today encoding the
existing `config.rs::Configuration` (which already has the write API), and would
migrate trivially when the type relocates. But building it against the
daemon-local type knowingly adds a second consumer of the drifted type, and
`ur16`'s preferred end-state is the helper encoding a contract-owned `Configure`
message.

Per operator discipline (surface design gaps; open psyche questions the design
names are not operator's to resolve), this is put to the psyche below rather than
silently chosen. A designer is **actively in this repo** (lane `designer`,
worktree `spirit/spirit-plane-split`, task `9hx0`) — the contract reconciliation
is the natural designer-coordinated surface.

## Decision points

1. **Sequence the q3q7 reconciliation vs commit-1** — the live fork (see chat).
2. **Compile `signal-spirit` or not** — `.#default` does not need it; vendor +
   negative guard closes the build. Adding a `--features production-migration`
   crane target (to actually exercise the migration path) is a separable
   follow-up, deferred unless asked (don't add what the task doesn't require).
3. **Commit-2 (CriomOS-home)** — out of commit-1 scope, captured for continuity:
   the new family must export `SPIRIT_SOCKET` (the new CLI reads that, not
   `PERSONA_SPIRIT_SOCKET`); the new `Configuration` has only socket + optional
   meta + database + optional trace (no owner/upgrade socket — those collapse into
   the single meta socket); ExecStart becomes `spirit-daemon
   /…/configuration.rkyv` (binary path, not inline NOTA); and the existing
   `persona-spirit-versioned-deployment` check proves via positive grep, which a
   new spirit-family check should replace with a real round-trip per `vcin`/`wyte`.

## Status

- **Decision:** psyche chose **B** — reconcile the contract first; build the
  helper + daemon against the contract-owned `Configuration`, no transitional
  shape. (The "ship now against the drifted type, migrate later" option was the
  ESSENCE-forbidden transitional shape — `What I am not optimising for` /
  `Backward compatibility is not a constraint`.)
- **Offline closure — DONE and proven.** `spirit/flake.nix` now vendors
  `signal-spirit` + `version-projection` (seven-step path-patch, all
  `--replace-fail` strings byte-exact, `flake.lock` pinned). A network-free
  sandbox build of `.#default` compiled `spirit` + `spirit-daemon` on the remote
  builder; the pushed commit `6eb31976` rebuilds from `github:LiGoldragon/spirit`
  to the identical store path. Corrects report 343: the leak was
  `version-projection`, not `signal-frame`. No version bump (pure
  build-reproducibility, no runtime logic change).
- **Next:** contract reshape (B's core) — define `Configuration` in
  `signal-spirit` (absorbing `archive_target`), reshape the crate-local meta
  `Configure` to wrap it, rewire the daemon via a local `DaemonConfiguration`
  wrapper, then add `spirit-write-configuration` against the contract type.
