# R5gr — synchronizer multi-pin repin fix (bead `primary-r5gr`)

Session: RenamePropagator. Bead: `primary-r5gr` (P2, Tier 2). Role: general code
implementer (Claude Opus 4.8, 1M). Date: 2026-07-04. Repo touched:
`LiGoldragon/synchronizer` (public tool dev, its own `main`). NO migration
producer/consumer `main` touched — only tool-owned `drop-next` staging.

## 1. Root cause of the multi-pin `BumpFailed`

Under the whole-graph `staged-cascade` (A checkpoint), `router` and
`signal-spirit` hit `BumpFailed` with `ManifestEdit: unbumpable pin: several
same-name entries pin the producer`. Confirmed shape on the real `drop-next`
manifests:

- `router` declares the producer **`signal-criome`** in TWO tables:
  `[dependencies]` (line 57) and `[dev-dependencies]` (line 76), both keyed
  `signal-criome`, both on `branch = "criome-authorization-push"`.
- `signal-spirit` declares the producer **`schema`** (`package = "schema"`) in
  TWO tables: `[dependencies]` (line 29) and `[dev-dependencies]` (line 39),
  both on `branch = "main"`.

Mechanism (verified in source at `57082fa6`):

- Topology discovery (`src/topology.rs`) emits one `DependencyEdge` per
  manifest *entry*, so a producer in two tables yields TWO identical
  `CargoManifest` edges — violating the documented invariant "one edge per
  (consumer, producer, layer)".
- `CargoManifest::redirect_git_dependency` (`src/cargo_manifest.rs`) refused
  ANY producer matched by more than one entry: `if matches.len() > 1 { return
  Err(UnbumpablePin{ reason: MultipleEntries }) }`. The guard existed because
  the edit addressed a single `(table, key)` and "addressing by name would
  silently alias the first match."

So the cascade never repinned `router`/`signal-spirit`: their `drop-next`
carried the rename-propagator URL rewrite but no producer repin. NOT a rename
defect — a synchronizer limitation.

The `Cargo.lock` side was never the blocker: cargo records the producer once
per (name, version, source), so both repos have exactly ONE lock entry for the
multi-pinned producer (`router` signal-criome rev `2986f8f8`, `signal-spirit`
schema rev `9af2c546`). The failure was purely the manifest redirect.

## 2. The fix (synchronizer `main`)

The multiplicity of textual entries is a manifest concern; every same-name
entry follows the one producer, so all must follow the cascade coherently. The
special case dissolves into the normal case (one edge, N textual entries):

- `src/cargo_manifest.rs` — `redirect_git_dependency` now redirects **every**
  same-name entry, each addressed by its own `(table, key)` (never by the
  shared package name). It validates every match first: a deliberate rev/tag
  pin among them still fails loud (`DeliberateRevisionPin`/`DeliberateTagPin`)
  and leaves the manifest untouched. The read model stays coherent across every
  table the entries live in.
- `src/topology.rs` — `DependencyGraph::discover` collapses duplicate edges
  (`deduplicated`), restoring "one edge per (consumer, producer, layer, local
  name)", so the layer bumps and reports once and the manifest edit owns the
  entry multiplicity. No misleading duplicate `AppliedBump` in the report.
- `src/error.rs` — `UnbumpablePinReason::MultipleEntries` doc scoped to the
  *lock* case only (several same-name git lock entries at genuinely different
  revisions — no single target rev repins them coherently). `Cargo.lock`
  behavior is UNCHANGED (`src/cargo_lock.rs` guard kept, `tests/cargo_lock.rs`
  `same_name_lock_entries_fail_loud_instead_of_aliasing` still green).
- `ARCHITECTURE.md` — updated the "Multi-pin and rev-pin safety" note, the
  ascent pseudocode, the topology section, and the invariants list.

Design discipline: typed records/errors (no anyhow at edges), methods on the
data-bearing `CargoManifest`/`DependencyGraph` types, no project literals. The
`Mainline` path is untouched (the change is in shared discovery + manifest edit,
exercised identically in both modes).

### Tests

- `tests/cargo_manifest.rs::every_same_name_entry_redirects_coherently` —
  the required guard: a manifest with N same-name entries (`signal-frame` in
  `[dependencies]` + a `package =`-renamed `[dev-dependencies]` entry) repins
  ALL N to the cascade branch, byte-for-byte, with the rev-pinned neighbour
  untouched. (Replaces the old `a_package_aliased_by_several_entries_fails_loud`
  which asserted the now-removed failure.)
- `tests/topology.rs::same_name_manifest_entries_collapse_to_one_edge` — a
  producer in `[dependencies]` + `[dev-dependencies]` collapses to one manifest
  edge (+ the single lock edge).

Full suite: `cargo test --offline` = **46 passed, 0 failed, 1 ignored**
(stateful `nix_resolution` probe). `cargo fmt --check` clean. `cargo clippy
--all-targets` clean.

### Landed commit

`LiGoldragon/synchronizer` `main`: `57082fa6` → **`ae75e8a270bd8f095090a193cb3beb93ed25bca9`**
("synchronizer: redirect every same-name manifest entry, not just the first"),
pushed to `origin/main` (confirmed `git ls-remote`).

## 3. Verify on the real repos — `router` + `signal-spirit`

### Repin proof — both repin CLEAN, no `BumpFailed` (definitive)

Driver: the landed binary (`ae75e8a2`) run as
`synchronizer <config> staged-cascade`, verify host set to an unresolvable
`no-verify-host` so the built-in ssh-verify fails fast (the prometheus
credential gap makes the tool's own `ssh prometheus nix build` unusable for
uncached private deps — verify is done out-of-band, below). Branch scheme
`(main drop-next)`, author `rename-propagator`.

**router** — config `[router, signal-criome, criome]`. Report action:

```
(router (Bumped ([
  (signal-criome CargoManifest (Reference criome-authorization-push) (Reference drop-next))
  (criome        CargoManifest (Reference criome-authorization-push) (Reference drop-next))
  (criome        CargoLock (Revision 19184a1f...) (Revision dd6c70f5669a...))
  (signal-criome CargoLock (Revision 2986f8f8...) (Revision 91096526fbf2...))
] (drop-next f3482fcab8f5662c0dbc3e3c239f43ea8f56f951))) (VerifyFailed no-verify-host))
```

**`Bumped`, not `BumpFailed`.** The multi-pin `signal-criome` produced ONE
collapsed manifest edge (dedup) that redirected BOTH textual entries.
Confirmed in the pushed tree `f3482fca`:

```
57: signal-criome = { ...signal-criome.git, branch = "drop-next", ... }   ([dependencies])
76: signal-criome = { ...signal-criome.git, branch = "drop-next", ... }   ([dev-dependencies])
```

Both were `branch = "criome-authorization-push"` before (and previously
`BumpFailed`); both now follow the cascade.

**signal-spirit** — config `[signal-spirit, schema, schema-rust]`. Report action:

```
(signal-spirit (Bumped ([
  (schema      CargoManifest (Reference main) (Reference drop-next))
  (schema-rust CargoManifest (Reference main) (Reference drop-next))
  (schema      CargoLock (Revision 9af2c546...) (Revision a393c8c822ce...))   ; crate "schema" 0.2.0
  (schema      CargoLock (Revision 9af2c546...) (Revision a393c8c822ce...))   ; crate "schema-cc" 0.1.0 (same repo)
  (schema-rust CargoLock (Revision 6218fb64...) (Revision 982fe099...))
] (drop-next 0650ea3ddfcb6e972a27079a5e72ddf445c618b2))) (VerifyFailed no-verify-host))
```

**`Bumped`, not `BumpFailed`.** The multi-pin `schema` (declared in
`[dependencies]` + `[dev-dependencies]`) redirected as one collapsed edge;
the pushed tree `0650ea3d` confirms BOTH manifest entries (lines 29, 39)
`main → drop-next`. The two `schema CargoLock` bumps are the two distinct
crates the schema repo publishes (`schema`, `schema-cc`) — both correctly
repinned to schema's drop-next rev, not a duplicate.

Both `VerifyFailed` lines are the deliberate `no-verify-host` (`ssh: Could not
resolve hostname`), NOT a build failure — the repin is what these runs prove.

Before this fix both were `BumpFailed(ManifestEdit: several same-name entries
pin the producer)`. The multi-pin limitation is gone.

### GREEN build

<!-- filled after coherent-closure build on prometheus builder -->



## 4. Gate compliance

- Claimed via Orchestrate: `/git/github.com/LiGoldragon/synchronizer`,
  `/git/github.com/LiGoldragon/router`, `/git/github.com/LiGoldragon/signal-spirit`.
- `drop-next` only for the migration repos; no migration `main` touched.
- Synchronizer is public: no private material in source, config, or commit.
