# 721 — Production-watch status + operator handoff; worktree cleanup outcome

Closes the two tasks the psyche set (`1. implement` the production-watch, `2. yes`
the cleanup). The production-watch turns out to be **one operator increment + a
deploy away** — both halves are already built; the remaining piece is spirit-
production territory. The cleanup retired the redundant designer branches and
surfaced one fork to resolve.

## Production-watch — both halves built; one operator gap

The goal (`2st7`/`xhwa`/`719`): spirit emits a non-blocking criome authorization
request per operation and proceeds regardless (ungated pass-through); a launchable
mentci monitors the ongoing requests.

- **Spirit emit — built.** `spirit/src/criome_gate.rs:237` `emit_authorization()`
  fires fire-and-forget over the criome socket via `spawn_blocking` and returns
  immediately; `AuthorizationMode::{Gating, Observing}` exists and is wired in
  `engine.rs:168-172`; Observing ships unconditionally (`GateDecision::Emitted`).
- **Mentci monitor — built and proven.** `mentci/src/criome_bridge.rs` sends
  `meta_signal_criome::Input::ObserveParkedAuthorizations` → `ParkedAuthorizationSnapshot`;
  `state.rs:absorb_criome_parked_authorizations()` dedups by slot and mints
  questions; the `CriomeEscalation` live demo proved park → mentci question →
  answer → criome. Production-ready for a single long-lived instance.

### The one gap — operator / spirit-production

A launchable spirit daemon never **arms the criome gate**: `arm_criome_gate` is
`#[cfg(feature = "mirror-shipper")]` and is called **only by tests**; the
`SpiritAttestor` (contract digest + evidence/keypair) is a test fixture. So
spirit cannot emit *valid* requests in production until the daemon arms the gate
from authenticated meta-signal config. Operator handoff:

1. Wire the spirit daemon startup (or a meta-signal config hook) to build the
   `SpiritAttestor` from an admitted contract digest + signer keypair and call
   `engine.arm_criome_gate(...)`, with the `mirror-shipper` feature on. (Keyring
   sourcing is system-operator/deploy.)
2. Run the daemon in `AuthorizationMode::Observing`.
3. Deploy a launchable production mentci (`mentci-write-configuration` →
   `mentci-daemon`) pointed at the local criome's meta socket, plus a mentci
   client.

### Refinements (not blocking the first watch)

- Slot correlation: spirit discards the `GateDecision` (`daemon.rs:33
  Ok(_decision) => {}`) and never publishes the `AuthorizationRequestSlot` /
  operation digest, so mentci shows an **uncorrelated chronological** request
  stream. `719`'s open question stands: uncorrelated is fine to start; correlation
  needs spirit to surface the slot.
- Restart resilience: mentci's slot dedup is in-memory; a durable watermark (or a
  `SubscribeParkedAuthorizations` stream on criome) is a later system-operator
  refinement for multi-instance / restart.

## Fork to resolve — the live-proven trace-client query is not on main

The mentci-side introspect work that **rendered the 23 real spirit events in the
GUI** (`mentci-lib` `trace-introspect-slice` `72a9b4da` = `src/introspect.rs`
direct `ComponentTrace` query; `mentci-egui` `b501ebb8` = `MENTCI_INTROSPECT_ENGINE`
engine selector) is **not on main**. Operator's main reached `ComponentTrace` by a
different route — the daemon-bridge pane (`mentci 32ec6f80`). So fork #2 recurs:

- **direct client query** (live-proven, the universal-client direction), or
- **daemon-bridge pane** (the `7x5z` daemon-owns-canonical-state shape, on main).

They overlap; main should carry one. Both branches are **archived, not deleted**,
pending the call.

## Cleanup outcome (`eh5a`)

- **Retired** (proof: zero commits not on main): `trace-introspect-slice` on
  signal-introspect / introspect / spirit; `meta-tier-split` on
  signal-mentci-client / mentci-egui (empty diff vs main); `gui-system-theme` on
  mentci-egui (superseded by operator's portal-read `7c1e008a`). Bookmarks deleted
  local + origin; five worktrees removed.
- **Archived** (un-integrated substance, kept for a human pass): the three
  `criome-mentci-bootstrap` doc branches (signal-mentci / mentci-lib / mentci-egui
  — fold the still-valid daemon-routing / criome-access-mode INTENT into each main
  `INTENT.md`, then retire), and the trace-client tail above.

## Correction (psyche): the criome-auth watch is tracing, not the parked-poll

The psyche corrected the framing above: criome authorization requests **are
tracing** — observable trace events on the unified `trace → introspect → mentci`
surface (the path proven in the 23-events demo), not a separate
`ObserveParkedAuthorizations` seam. Covered intent (`m5jl`/`xqkv`: tracing is
schema-defined trace events; `80bl`: mentci observes introspect tracing; `7x5z`:
mentci is the criome gate; `2st7`: non-blocking now) — the guardian confirmed
`Duplicate`, so no new record. The corrected shape:

- **Watch (now)** rides the **tracing** surface: spirit emits a criome-authorization
  trace event (one more event type in its trace vocabulary, `testing-trace`-gated
  per `xqkv`/`q13r`) → introspect ingests → mentci observes, reusing the introspect
  query path already built. So the watch is a **tracing-instrumentation increment**
  (add the criome-auth trace event to spirit's trace vocabulary), not the
  parked-auth poll loop described earlier in this report.
- **Gate (future)** is what the current ungated emit is *scaffold* for: mentci
  approving the observed request so its approval becomes the criome verdict — the
  parked-question/verdict path (`7x5z`, already demoed). The watch evolves into the
  gate over the same surface.

So the operator handoff above (arm the spirit gate from config) belongs to the
**gate** half; the **watch** half is the tracing increment.
