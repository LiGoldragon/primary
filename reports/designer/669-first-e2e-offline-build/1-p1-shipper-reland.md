# P1 — re-land the spirit→mirror MirrorShipper onto a fresh feature branch

Slice P1 of the 669 first-e2e-offline-build arc. Goal: bring the dropped,
fully-tested gated `MirrorShipper` (built then dropped from spirit main by
merge `d2cf86f`, added by `a7b7d95`; surviving on `origin/store-decomposition`
and `origin/vc-followups`) back onto a fresh spirit designer feature branch,
reconciling its mirror / triad-runtime / sema-engine pins to current main.

## Branch

- Worktree: `/home/li/wt/github.com/LiGoldragon/spirit/mirror-shipper`
- Bookmark: `mirror-shipper-reland` (commit `4acce197`), fresh off current
  spirit `main@origin` (`41f1173`, spirit 0.13.0). The pre-existing
  `mirror-shipper` worktree was reused but its stale 0.12.0 bookmark was NOT
  built on — a new change was started off current main instead.
- NOT pushed (operator integrates).

## What landed

All six files from the original landing's spirit-side surface, committed and
green on the default build:

- `src/shipper.rs` — the `MirrorShipper` OFF-by-default gate, verbatim from
  `store-decomposition` plus a RE-LAND STATUS doc block recording the two
  upstream blockers.
- `tests/mirror_shipper.rs` — the two-proof witness (configured ships +
  fresh-store restores identically; unset ships nothing), verbatim.
- `src/store/mod.rs` — added `Store::engine_handle() -> Arc<SemaDatabase>`
  (the shared-Arc seam; pure additive, present on `store-decomposition`,
  absent on current main).
- `src/lib.rs` — `#[cfg(feature = "mirror-shipper")] pub mod shipper;`.
- `Cargo.toml` — the `mirror-shipper` feature (`dep:mirror`), the
  `mirror_shipper` test entry, the reconciled pins, the dev-dep mirror
  contracts.
- `Cargo.lock` — regenerated.

The default build (`cargo build`, no features) is GREEN with the reconciled
pins. The daemon's no-NOTA / binary-only dependency tree is unchanged: `mirror`
is `optional` behind `mirror-shipper`, so nota-next stays out of the default
build.

## Pin reconciliation

The original landing's three load-bearing pins, reconciled to current main:

| Crate | store-decomposition pin | current main pin | re-land pin | why |
|---|---|---|---|---|
| `sema-engine` | `rev 65a6126` | `branch main` | `rev 65a6126` | must be byte-identical to mirror arc-shipper's sema-engine so Cargo unifies ONE engine instance (precondition for sharing `Arc<Engine>`). `65a6126` is two commits behind sema-engine main (the engine-plane decompose). |
| `triad-runtime` | `branch tailnet-listener` | `branch main` | `branch tailnet-listener` | mirror's shipper actor uses the tailnet-listener kameo surface; same branch spec unifies the runtime instance. |
| `mirror` | n/a (was external new dep) | n/a | `branch arc-shipper`, `default-features = false`, optional | only `arc-shipper` exposes `ComponentShipper::new(engine: Arc<Engine>, ...)`. |

The base build proves this trio compiles together for the production daemon
path (spirit at sema-engine 65a6126 still builds clean).

### The shared-Engine seam — the hard part

The seam is: spirit's store keeps `database: Arc<sema_engine::Engine>` and
writes through it; the shipper must hold a CLONE of that SAME `Arc` so it reads
the outbox the working writes append to and records `acknowledge_mirror` back
into it. This forces `mirror::ComponentShipper` to accept `Arc<Engine>`.

Decisive finding: mirror `main` (current, green, deployed) REGRESSED the
shipper to take `Engine` BY VALUE (`engine: ComponentEngine`, not
`Arc<ComponentEngine>`), and renamed `TailnetClient` → `MirrorTailnetClient`.
A store that keeps its engine behind an `Arc` cannot hand an owned `Engine` to
a by-value constructor, and `sema_engine::Engine` is deliberately not `Clone`
(it holds a `Mutex`; it is `Send + Sync` for `Arc` sharing). So the seam forces
the `arc-shipper` branch over `main` — the prompt's "if the shared-Engine type
identity forces a specific pin, document it" case, sharpened: it is the
sharing MODEL, not just type identity, that forces it.

## Test result

`cargo test --features mirror-shipper --test mirror_shipper` does NOT run — the
`mirror-shipper` feature does not compile. Two independent upstream blockers,
neither fixable from this spirit-only slice:

### Blocker 1 — meta-signal-spirit dropped the `MirrorTarget` schema

At `store-decomposition`, spirit owned its `meta_signal` schema LOCALLY in
`src/schema/meta_signal.rs`, including `MirrorAddressText`, `MirrorAddress`,
`MirrorTarget` (an enum with `Address(MirrorAddress)` + `Default`), and a
`mirror_target: Option<MirrorTarget>` field on both `ConfigureRequest` and
`ConfigureReceipt`, plus `ConfigureRejection` / `ConfigureRejectionReason`.

Current spirit re-exports `meta_signal` from the external `meta-signal-spirit`
crate, whose `ConfigureRequest(ArchiveDatabaseTarget)` is a single-field tuple
with NO mirror target, and which defines no `MirrorTarget` family at all. The
shipper's `configure(target: Option<&MirrorTarget>, ...)` and the test's
`ConfigureRequest { archive_database_target, mirror_target }` both reference
types that no longer exist.

Fix (out of slice): re-add the `MirrorTarget` schema noun to the
`meta-signal-spirit` contract and regenerate it into spirit; re-thread
`set_mirror_target` / `mirror_target` through `Nexus` and `Store`; re-add the
`engine.rs` (arm/disarm + `ship_unshipped_to_mirror` + `publish_checkpoint_to_mirror`)
and `daemon.rs` (post-commit drain) wiring from `a7b7d95`. Hand-rolling a
parallel `MirrorTarget` inside spirit would violate the schema-emitted-nouns
discipline (no hand-written mirrors of schema types), so it was NOT done.

### Blocker 2 — mirror arc-shipper does not compile against today's tree

`arc-shipper` pins `nota-next` 0.4.0 (branch `structural-shape-extension`)
while current `signal-mirror` / `meta-signal-mirror` main pin `nota-next` 0.5.0.
The Cargo.lock carries TWO nota-next instances; mirror's `client.rs` uses the
0.4.0 codec API against signal-mirror's 0.5.0-derived types:

```
error[E0271]: type mismatch resolving `<Input as FromStr>::Err == NotaDecodeError`
  --> mirror/src/client.rs:55:52
error[E0599]: no method named `to_nota` found for enum `signal_mirror::Output`
  --> mirror/src/client.rs:63:40
error: could not compile `mirror` (lib) due to 2 previous errors
```

So `arc-shipper` is stale: it was frozen at an older nota-next than its own
current signal-mirror dependency. Mirror `main` is internally consistent
(nota-next 0.5.0 throughout) and compiles, but lacks the `Arc<Engine>` shipper.

Fix (mirror-repo change, out of slice): forward-port arc-shipper's
`Arc<Engine>`-accepting `ComponentShipper` onto mirror main's current
nota-next 0.5.0 base — i.e. add an `Arc<Engine>` constructor (or restore the
`Arc` field) on mirror main, keeping its `MirrorTailnetClient` rename.

## The fork, stated plainly

Neither mirror branch satisfies the seam today:

- mirror `main`: current nota-next (compiles, deployed), but `ComponentShipper`
  takes `Engine` by value → can't share spirit's `Arc<Engine>`.
- mirror `arc-shipper`: `ComponentShipper` takes `Arc<Engine>` (shareable), but
  stale nota-next → can't compile against current signal-mirror.

The clean unblock is a single mirror-repo task: bring the `Arc<Engine>` shipper
onto mirror main's nota-next base. Then spirit can pin `mirror = branch main`
(and drop the `sema-engine rev 65a6126` / `triad-runtime tailnet-listener`
special pins back toward `main` once mirror main also moves there), and the
remaining blocker is just re-adding the `MirrorTarget` schema to
meta-signal-spirit + regenerating spirit's engine/daemon wiring.

## Recommended next slices

1. **mirror-repo (operator):** forward-port the `Arc<Engine>` `ComponentShipper`
   onto mirror main (current nota-next 0.5.0). Unblocks blocker 2.
2. **meta-signal-spirit (nota-designer):** re-add the `MirrorTarget` schema noun
   + `mirror_target` field on `ConfigureRequest`/`ConfigureReceipt`; regenerate.
   Unblocks blocker 1.
3. **spirit (this branch):** once both land, re-thread `set_mirror_target` /
   `mirror_target` through `Nexus`/`Store`, re-add the `engine.rs` + `daemon.rs`
   wiring from `a7b7d95`, repin `mirror = branch main`, then
   `cargo test --features mirror-shipper --test mirror_shipper`.
