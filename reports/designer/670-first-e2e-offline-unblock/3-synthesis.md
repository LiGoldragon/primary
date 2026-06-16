# 670 — Synthesis: both upstream blockers cleared, green

The two unblocks from report 669 are done, in parallel, on designer feature branches — both green,
both additive, neither pushed (the boundary decision below).

| Unblock | Branch (worktree) | Change | Build/test |
|---|---|---|---|
| **H1** meta-signal-spirit `MirrorTarget` | `mirror-target-reland` @ `3283925f` (off main) | authored `schema/meta-signal.schema`: `MirrorTarget` (Default \| Address(MirrorAddress)), `MirrorAddress`/`MirrorAddressText` newtypes, Optional `mirror_target` on `ConfigureRequest` + `ConfigureReceipt`; regenerated `src/schema/meta_signal.rs` (no hand-written Rust); crate fixtures updated | `cargo build`/`test`/`test --features nota-text` **green** |
| **H2** mirror `Arc<Engine>` shipper | `arc-shipper-mainline` @ `6bcefa4f` (off main `b9c171a7`) | `src/shipper.rs` +48/−1: engine field → `Arc<ComponentEngine>`; by-value `new`/`with_client` unchanged (wrap internally); new `from_shared_engine`/`with_shared_client` + `shared_engine()`; reconciled to current main pins | `cargo build`/`clippy`/`test` **green** incl. `end_to_end_arc.rs` + 14 daemon tests |

## What this leaves for the offline green (H3)

H1 surfaced one more spirit-side gap beyond the re-land: spirit's `src/engine.rs` `configure()`
(~452-460, **not** feature-gated) still treats `ConfigureRequest` as the old newtype — it calls
`into_payload()` (gone on the named struct) and builds `ConfigureReceipt` without the new
`mirror_target`, and never reads `mirror_target` nor arms the shipper. So H3 (the next designer step,
spirit repo) is:

1. Repin spirit's `mirror-shipper-reland` deps: `mirror` → `arc-shipper-mainline`, `meta-signal-spirit`
   → `mirror-target-reland`.
2. Adapt `engine.rs` `configure()` to the named-struct `ConfigureRequest` (read `mirror_target`, build
   the receipt with it, arm the shipper).
3. Re-add the deferred wiring P1 enumerated (engine `arm/disarm` + `ship_unshipped_to_mirror` +
   `publish_checkpoint_to_mirror`, and the `daemon.rs` post-commit drain) — they reference the now-present
   `MirrorTarget`, so they can compile.
4. Construct via `ComponentShipper::from_shared_engine(store.engine_handle(), …)`.
5. Get the `mirror-shipper` feature + `tests/mirror_shipper.rs` green.

Then the harness round (P5, option b) adds signal-router and needs the cross-branch pin unify (H4).

## The boundary decision

The three feature branches (spirit `mirror-shipper-reland`, meta-signal-spirit `mirror-target-reland`,
mirror `arc-shipper-mainline`) are green but **local**. For H3's spirit build to dep H1/H2 by git
branch, those branches must be fetchable — i.e. the feature branches get **pushed to origin** (the
normal designer-ships-feature-branch flow). That is the first outward action in this arc; earlier
rounds were entirely local. The alternative is handing the three green branches to operator now for
main integration. Surfaced to the psyche rather than pushing unilaterally, since prior chat said
"not pushed; operator integrates."

## Status

Offline-e2e unblock: **complete and green**. Remaining to the first offline green: H3 (spirit
integration, designer) → P5 harness (designer + operator pin unify) → operator main integration of
the now-four-branch stack. The live/gated track (criome integration + ceremony, router m3 + Yggdrasil
+ NixOS modules) is designed and waiting (669/3, 669/4).
