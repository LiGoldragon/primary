# 671 — First E2E, leg one: spirit → mirror shipper integrated and green

BUILD H3. The offline e2e's first leg is the spirit→mirror shipper. The two
upstream blockers (meta-signal-spirit MirrorTarget reland, mirror Arc-engine
shipper) were cleared on feature branches in 669/1 and 670; this session pushed
them, repinned spirit, closed the spirit-side H1 gap, re-landed the deferred
gated wiring, and proved both halves of `tests/mirror_shipper.rs` green.

Result: `cargo build` (default), `cargo build --features nota-text`,
`cargo build --features mirror-shipper`, `cargo clippy --features mirror-shipper`
all green; both proofs pass.

## 1. Dependency feature branches pushed to origin

The designer-ships-feature-branch flow (psyche-authorized this session). All
three bookmarks confirmed on origin by `git ls-remote`:

| repo | bookmark | origin commit | what it carries |
|---|---|---|---|
| meta-signal-spirit | `mirror-target-reland` | `5d61ae8c` | MirrorTarget/MirrorAddress/MirrorAddressText nouns + `mirror_target` slot on ConfigureRequest/Receipt |
| mirror | `arc-shipper-mainline` | `6bcefa4f` | additive `ComponentShipper::from_shared_engine`/`with_shared_client` |
| spirit | `mirror-shipper-reland` | `9b022c1e` | this session's integration commit |

Commit-id reconciliation vs the prompt: the prompt named meta-signal-spirit at
`3283925f`, but bookmark `mirror-target-reland` actually sits one commit forward
at `5d61ae8c` ("re-add MirrorTarget/MirrorAddress contract nouns + mirror_target
slot") — the correct reland tip, verified by its `schema/meta-signal.schema`
(`MirrorTarget [Default (Address MirrorAddress)]`, `mirror_target (Optional
MirrorTarget)` on both records) and a clean `cargo build`. The bookmark name
matched, so it was the right one to push. mirror `6bcefa4f` and spirit
`4acce197` matched the prompt exactly.

## 2. Cargo repin (spirit, ~/wt/.../spirit/mirror-shipper/Cargo.toml)

Beyond the two repins the prompt named, the shared-engine type-identity
precondition forced two more — the seam only holds if spirit and mirror resolve
to ONE `sema_engine::Engine` and ONE `triad_runtime` instance:

- `mirror` → `branch = "arc-shipper-mainline"` (was `arc-shipper`) — Cargo.toml:99
- `meta-signal-spirit` → `branch = "mirror-target-reland"` (was `main`) — Cargo.toml:117
- `sema-engine` → `branch = "main"` (was `rev = 65a6126a`) — Cargo.toml:105.
  `arc-shipper-mainline` was forward-ported onto mainline schema tooling, so it
  now tracks sema-engine `main` (`73eea24b`), not the old `65a6126` rev the
  dropped `arc-shipper` branch pinned. Both crates must share the source spec.
- `triad-runtime` → `branch = "main"` (was `tailnet-listener`) — Cargo.toml:123.
  `arc-shipper-mainline` pins triad-runtime `main`; the kameo actor/runtime
  types must match for the shared engine and shipper actor to compose.

`cargo update mirror meta-signal-spirit` resolved the lock: mirror →
`arc-shipper-mainline#6bcefa4f`, meta-signal-spirit →
`mirror-target-reland#5d61ae8c`, sema-engine unified onto `main#73eea24b`
(removing the old `65a6126` rev), triad-runtime unified onto `main` (removing
the `tailnet-listener` entry), and the stale `nota-next 0.4.0` that broke the
old `arc-shipper` branch was dropped.

## 3. engine.rs `configure()` adaptation — H1 gap closed (src/engine.rs:457)

The default build surfaced exactly the H1 gap from 670/1: the old handler
called `request.into_payload()` (gone on the named struct) and built
`ConfigureReceipt` without `mirror_target`. Both compile errors appeared in the
DEFAULT build, confirming the new contract is wired.

The default-vs-feature split the prompt required:

- UNCONDITIONAL (compiles with the shipper module absent): destructure the
  named-field `ConfigureRequest { archive_database_target, mirror_target }`,
  set the archive target, and echo `mirror_target` into `ConfigureReceipt`.
- GATED behind `#[cfg(feature = "mirror-shipper")]`: arm/disarm the shipper via
  `self.mirror_shipper.configure(mirror_target.as_ref(), engine_handle)`; a bad
  mirror address rejects the Configure (`InternalError`) rather than silently
  leaving mirroring off.

## 4. Deferred gated wiring re-landed (recovered from `a7b7d95`)

Recovered the exact prior shape from spirit `a7b7d95` ("gated mirror shipper
(29pb)") and re-landed it gated:

- engine.rs: `mirror_shipper: MirrorShipper` field (engine.rs:289) + initializers
  in `new`/`new_with_trace`; `Engine::store()` accessor (engine.rs:431);
  `mirror_shipping_armed()`, `ship_unshipped_to_mirror()`,
  `publish_checkpoint_to_mirror()` (engine.rs:485-509); import of
  `MirrorShipper`/`MirrorShipperError` (engine.rs:3-4).
- daemon.rs: post-commit drain in `handle_working_input` — best-effort
  `engine.ship_unshipped_to_mirror()` after the local commit (daemon.rs:144-159).
- lib.rs: `pub use shipper::{MirrorShipper, MirrorShipperError}` (lib.rs:101-102);
  `pub mod shipper` was already present.
- shipper.rs:86 — construct via `ComponentShipper::from_shared_engine(engine,
  socket_address, VersionedStoreName::new(RecordFamily::STORE_NAME))` so store
  and shipper hold clones of ONE `Arc<sema_engine::Engine>`. (The reland had
  `ComponentShipper::new`, which takes the engine by value and won't accept the
  store's `Arc`; `from_shared_engine` is the shared-engine seam.)

Type-identity confirmed: spirit's `Store` aliases `Engine as SemaDatabase`, and
`Store::engine_handle() -> Arc<SemaDatabase>` is exactly the `Arc<ComponentEngine>`
(= `Arc<sema_engine::Engine>`) `from_shared_engine` wants — unified by the
sema-engine repin above.

### Deliberate scope note (not a blocker)

The historical `configure` also called `self.nexus.set_mirror_target(...)` to
PERSIST the target on the store for daemon self-resume. That `set_mirror_target`
lived on a SEPARATE slice (parent commit `37bafef` "VersionReport store axes +
meta MirrorTarget + Store Arc<Engine>"), which adds a `mirror_target` slot to
`Store`/`Nexus` and was NOT part of the `a7b7d95` reland nor present in the
current tree. I did NOT re-add it: the test does not require persistence (it
checks the receipt and live arming, not store-resume), and re-adding the store
axis is a distinct slice. The mirror target is therefore echoed in the receipt
and used to arm the live shipper, but not yet persisted across a daemon restart.
Flagged for whoever lands the store-axes slice.

## 5. One naming reconciliation (test import)

The reland test imported `mirror::TailnetClient`, but `arc-shipper-mainline`
keeps the Mirror-prefixed name `MirrorTailnetClient` (the rename to
`TailnetClient` lives only on the dropped `arc-shipper` branch, commit
`02ba9d5e`). Fixed in the test, not the pushed mirror branch:
`use mirror::{..., MirrorTailnetClient as TailnetClient, ...}`
(tests/mirror_shipper.rs:19). The test body uses the alias unchanged.

## 6. Exact test/build result

```
cargo build                              Finished (green)
cargo build --features nota-text         Finished (green)
cargo build --features mirror-shipper    Finished (green)
cargo clippy --features mirror-shipper   Finished (zero warnings, zero errors)

cargo test --features mirror-shipper --test mirror_shipper
  test unconfigured_mirror_target_ships_nothing_and_leaves_behavior_unchanged ... ok
  test configured_mirror_target_ships_commits_and_a_fresh_store_restores_identically ... ok
  test result: ok. 2 passed; 0 failed
```

`configured…ships_commits_and_a_fresh_store_restores_identically` exercises the
full leg: arm the shipper on a real loopback mirror daemon, record + checkpoint
+ record, assert `QueuedForMirror`, drain via the daemon hook, assert
`ServerCommitted` + empty outbox, publish the checkpoint, restore a FRESH spirit
store from the mirror, and assert `len` and `database_marker` match.
`unconfigured…` proves the OFF-by-default path ships nothing and leaves the
store `QueuedForMirror`.

## 7. Commit and push

Spirit commit `9b022c1e` on bookmark `mirror-shipper-reland`, pushed to origin
(`jj git push --bookmark mirror-shipper-reland --allow-new`). The two
dependency bookmarks were pushed first (section 1). No blockers — leg one of the
offline e2e is green end to end.
