# Bead Implementation Evidence — Persistent Spirit A→B Mirror (NON-GATED slice)

## Scope

Four beads implemented in dependency order: sos8, x3l7, 85hv, om4g.1, om4g.2.
All are now closed in the tracker with build evidence.

## primary-sos8 — Spirit Checkout Disposition

**Outcome:** clean rev; no work discarded.

The `spirit-strict-positional-v11` bookmark was already pointing to commit `05269499`
(same as `main`). It was pushed to origin via `jj git push --bookmark spirit-strict-positional-v11`.
No uncommitted work existed; the bookmark was unpushed, not dirty.

## primary-x3l7 — Mirror TCP Ingress Authentication Stopgap

**Repo:** `LiGoldragon/mirror`, branch `criome-auth-witness`, commit `c2e4fed8`

**File changed:** `src/config.rs`

`Configuration::try_from(DaemonConfiguration)` now calls
`tcp_listen_address.ip().is_unspecified()` after parsing the address and returns
`Err(ConfigurationError::ListenAddressUnspecified { address })` when the result
is `true`. This makes 0.0.0.0 and `::` binds fail at startup rather than silently
exposing the ingress to every reachable peer.

Three new unit tests in `#[cfg(test)] mod tests`:
- `rejects_ipv4_unspecified_address` — `0.0.0.0:7474` yields `ListenAddressUnspecified`
- `rejects_ipv6_unspecified_address` — `[::]:7474` yields `ListenAddressUnspecified`
- `accepts_specific_tailnet_address` — `127.0.0.1:7474` yields `Ok`

**Build evidence (prometheus):** `cargo test` — all 3 new tests pass, full suite 20/20.

## primary-85hv — Mirror Shipper Confirmation

**Outcome:** no code change required.

`spirit/src/shipper.rs` contains `MirrorShipper` with `configure()`,
`ship_unshipped()`, and `publish_checkpoint()` behind `#[cfg(feature = "mirror-shipper")]`.
The bead was a confirmation step; the shipper was already landed.

## primary-om4g.1 — Authorization Trace Event

**Outcome:** no new code required.

`AuthorizationObjectName::Observed` already exists in `src/trace_event.rs`.
The `observe_gate_head()` method introduced for om4g.2 emits it under
`#[cfg(feature = "testing-trace")]` on each `GateDecision::Observed` result.

## primary-om4g.2 — Arm Criome Gate in Shipped Daemon

**Repo:** `LiGoldragon/spirit`, branch `criome-authorization-push`, commit `4a017504`

**Files changed:** `Cargo.toml`, `src/lib.rs`, `src/engine.rs`, `src/daemon.rs`

**Core change: new `criome-gate` Cargo feature**

`criome_gate.rs` uses `criome::transport::CriomeClient` and types from
`signal_criome` — both are optional deps previously activated only by
`mirror-shipper`. The gate could not compile without the shipper. The fix was a
new feature that separates the gate from the shipper:

```
criome-gate = ["dep:criome", "dep:signal-criome"]
mirror-shipper = ["criome-gate", "dep:mirror", "dep:signal-mirror"]
```

`mirror-shipper` implies `criome-gate` so all existing tests continue to work.

**Structural changes by file:**

`Cargo.toml`:
- Added `criome-gate` feature with `dep:criome` + `dep:signal-criome`
- Removed `dep:criome`/`dep:signal-criome` from `mirror-shipper` (now implied by `criome-gate`)
- `criome_gate_1of1` test stays at `required-features = ["mirror-shipper"]` because it exercises `gate_and_ship_head` and `mirror::Service`

`src/lib.rs`:
- `pub mod criome_gate`: `mirror-shipper` → `criome-gate`
- `pub use criome_gate::{...}`: `mirror-shipper` → `criome-gate`
- `pub use engine::ObserveGateError`: now `#[cfg(feature = "criome-gate")]`

`src/engine.rs`:
- `ObserveGateError` enum: added `#[cfg(feature = "criome-gate")]`
- `Engine::criome_gate` field: added `#[cfg(feature = "criome-gate")]`
- `Engine::new()` and `Engine::new_with_trace()`: `criome_gate` init under `#[cfg(feature = "criome-gate")]`
- Configure gate block in `configure()`: wrapped with `#[cfg(feature = "criome-gate")]`
- `arm_criome_gate`, `criome_gate_armed`, `observe_gate_head`: added `#[cfg(feature = "criome-gate")]`

`src/daemon.rs`:
- Observe dispatch: `#[cfg(not(feature = "mirror-shipper"))]` → `#[cfg(all(feature = "criome-gate", not(feature = "mirror-shipper")))]`

**Build evidence (prometheus):**

| Command | Result |
|---|---|
| `cargo check` (no features) | `Finished` — 0 errors |
| `cargo check --features criome-gate` | `Finished` — 0 errors |
| `cargo check --features mirror-shipper` | `Finished` — 0 errors |
| `cargo test --features mirror-shipper` | all tests pass |

criome_gate_1of1 witness results:
- `meta_configure_arms_and_clears_criome_gate_socket` — ok
- `socket_only_gate_observes_signed_auto_approved_authorization` — ok
- `authorized_head_ships_and_emits_projected_reference_denied_head_does_not_ship` — ok

## Tracker State

All five beads closed:
- `primary-sos8` — closed
- `primary-x3l7` — closed
- `primary-85hv` — closed
- `primary-om4g.1` — closed
- `primary-om4g.2` — closed

## Open Items

- `primary-1e6b` authorization-gated and deploy-gated items (.1–.8) remain out of scope
- The shipped daemon now has `criome-gate` compiled in; a production deploy needs an owner
  `Configure` with `CriomeGateTarget::Socket` to arm the gate
- The full `gate_and_ship_head` path (sender leg, `primary-1e6b.5`) requires `mirror-shipper`
  plus a configured `MirrorTarget::Address`
