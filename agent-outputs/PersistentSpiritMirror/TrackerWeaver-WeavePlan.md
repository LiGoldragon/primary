# Tracker-Weaver Weave Plan — Persistent Two-VM Spirit A→B Mirror (prometheus)

## Task and scope

Lay a tracked, sequenced dependency graph (beads) to deliver ONE slice: two
persistent VMs (node A, node B) on host `prometheus`; Spirit state created on
node A mirrors **one-directionally** to node B over the Criome daemon's
auto-authenticated propagation path, with state that **persists across runs**
(real deployment, not an ephemeral runNixOSTest). Bidirectional/multi-master is
explicitly a LATER slice. This is a PLANNING weave — no implementation
dispatched. Graph only.

Grounded in `agent-outputs/PersistentSpiritMirror/Scout-SituationalMap.md`.

## B1 resolution (the dominant design fork) — CODE-CONFIRMED

**Verdict: the sender leg is CONFIG/DEPLOY, not net-new standing code.**

Two independent read-only source passes confirm two distinct, coexisting
mechanisms in the codebase:

1. **Direct spirit→mirror body carry (THIS SLICE — config-only).**
   - `meta-signal-spirit/src/schema/meta_signal.rs:150-153`:
     `MirrorTarget { Default, Address(MirrorAddress) }`; `MirrorAddress` wraps a
     bare `String` (`:134-142`).
   - `spirit/src/shipper.rs:59-66` parses that string as
     `text.parse::<SocketAddr>()` — i.e. any host:port, not a local unix path.
   - `mirror/src/shipper.rs:42-52` `exchange()` dials
     `TcpStream::connect(self.address)` to **any** `SocketAddr` and writes a
     length-prefixed frame; `:150-166` ships the full `EntryEnvelope`
     (head digest + rkyv payload **body**) directly.
   - `mirror/src/service.rs:158-170`: the mirror receives one append,
     persists to its own sema store, acks — **no router fan-out, no forward.**
   - `spirit` `engine.gate_and_ship_head()` authorizes each head through the
     **armed criome gate** before calling `mirror_shipper.ship_unshipped()`.
   - Conclusion: pointing spirit's `MirrorShipper` at node B's remote mirror is
     **configuration** (`MirrorTarget::Address(node-b:7474)`), gated only by the
     OFF-by-default `mirror-shipper` cargo feature. No net-new sender daemon.

2. **Router-forward attestation path (LATER SLICE — genuinely net-new).**
   - Fans out a **typed reference**, not the body.
   - `router` `peer_delivery::payload_for` hardcodes `Vec::new()` for
     `routed_objects`; the `Message` struct (`router/src/message.rs:163-170`)
     has **no** `routed_objects` field; the working-socket daemon handler
     (`daemon.rs:111-151`) accepts only `SignalMessageInput`/`RouterObservation`.
   - Header truth (verbatim, `router_forward_witness.rs:4-6`): "No router daemon
     ingress accepts a `RoutedContractObject` for an OUTBOUND forward (a real
     code limitation)." The witness reuses the router's **production**
     `CriomeForwardAttestation` (sign on A, verify on B's criome) but is a test
     bin, not a standing daemon.
   - Enabling this path = net-new code (a standing outbound shipper modeled on
     `router-forward-witness`, or invasive `Message`/`peer_delivery`/
     `DeliverRemote`/ingress changes). Parked as **primary-1e6b.8 (deferred)**;
     overlaps `primary-ymww` and `primary-om4g.11`.

**Where the "criome auto-authentication" lives for THIS slice:** the
**sender-side armed criome gate** (`primary-om4g.2`). Every head is
criome-authorized before it ships. Receiver-side hardening is the mirror TCP
ingress auth (`primary-x3l7`), whose real per-request BLS/criome attestation is
deferred; the psyche-accepted interim is the tailnet-bind stopgap, and the
strict psyche sequence is **authenticate ingress THEN enable the shipper**
(`primary-85hv` comment 2026-06-13).

## The slice reuses existing beads (do NOT duplicate)

| Existing bead | Role in this slice |
|---|---|
| `primary-85hv` | Production mirror shipper in spirit — **LANDED, gated** behind `mirror-shipper` feature + meta `MirrorTarget`; the sender code already exists. |
| `primary-x3l7` | Rebind/authenticate mirror TCP ingress off 0.0.0.0 — **strict prereq** before enabling the shipper. |
| `primary-om4g.2` | Arm the criome gate in the shipped spirit daemon (today cfg'd out / test-only). Provides the sender-side auto-authentication. (Its own dep: `primary-om4g.1` trace event.) |
| `primary-dw95` | Single-node VmHost + `TestVm` on prometheus **plus the kink-1 guest-network fix** (guests are network-dark today). Foundation for a reachable pair. |
| `primary-sos8` | Disposition the dirty/detached spirit checkout so the slice builds from a clean pushed rev. |
| `primary-yluj` | Rebuild + redeploy the spirit daemon (referenced by the sender-leg deploy). |

## The new slice graph (epic `primary-1e6b`)

All new beads carry label `persistent-spirit-mirror`.

| ID | Title | Gate | Blocked by |
|---|---|---|---|
| `primary-1e6b` | [EPIC] Persistent two-VM Spirit A→B mirror over the criome-authenticated path | — | — |
| `primary-1e6b.1` | Author node A + node B: two persistent `TestVm` guests on prometheus (private goldragon facts) | **authorization-gated** (private facts) | `primary-dw95` |
| `primary-1e6b.2` | Reproject goldragon horizon + BootOnce-redeploy prometheus with the two guests | **deploy-gated / real-world** | `.1` |
| `primary-1e6b.3` | Criome A→B trust seed: node B pre-registers node A BLS identity→key at deploy (Stage-A) | deploy-gated (mechanism buildable ahead) | `.2` |
| `primary-1e6b.4` | Mirror receiver seed: pre-register the mirror store-row for `spirit` on node B at deploy | deploy-gated (mechanism buildable ahead) | `.2` |
| `primary-1e6b.5` | **Sender leg (B1 config/deploy):** enable `mirror-shipper` feature + meta `Configure` `CriomeGateTarget::Socket` + `MirrorTarget::Address(node-b)` | deploy-gated | `.2 .3 .4` + `85hv om4g.2 x3l7 sos8` |
| `primary-1e6b.6` | State-creation-on-A mechanism: guardian-armed organic `Record` vs owner meta `Import` seeding | **psyche-decision** | — (feeds `.7`) |
| `primary-1e6b.7` | Verify A→B mirror on the standing pair AND state survives a guest restart | deploy-gated / verification | `.5 .6 .2` |
| `primary-1e6b.8` | DEFERRED (router-attestation variant): standing router outbound forward + persona-router bootstrap | deferred (LATER slice) | — (parked) |

Graph verified: `bd dep cycles` → no cycles. Full chain renders under
`bd dep tree primary-1e6b.7`.

### Ordered execution reading (dependency order)

```
primary-sos8 ─┐
primary-x3l7 ─┤
om4g.1→om4g.2─┤
primary-85hv ─┤
              │
dw95 → 1e6b.1 → 1e6b.2 ─┬─ 1e6b.3 ─┐
                        └─ 1e6b.4 ─┤
                                   ├─ 1e6b.5 ─┐
   (sos8,x3l7,om4g.2,85hv) ────────┘          ├─ 1e6b.7  (verify + restart)
                             1e6b.6 ──────────┘
1e6b.8  (deferred / parked, router-attestation variant)
```

## First executable (non-gated) beads — start here

These are workable now with no authorization or standing hardware:

1. **`primary-x3l7`** — authenticate/rebind the mirror TCP ingress off 0.0.0.0.
   Hard strict-sequence prereq for the sender leg. Pure code (mirror crate).
2. **`primary-om4g.1` → `primary-om4g.2`** — add the criome-auth trace event,
   then arm the criome gate in the shipped spirit daemon. Pure code; provides
   the sender-side auto-authentication.
3. **`primary-sos8`** — disposition the dirty/detached spirit checkout so the
   slice builds from a clean pushed rev. (Carries a small commit-vs-discard
   psyche micro-decision.)
4. **`primary-85hv`** — already landed/gated; confirm it is current and that the
   `mirror-shipper` feature + meta `MirrorTarget` still hold on a clean rev.

Buildable-ahead (mechanism only, though the *act* is deploy-gated): the seed
hooks behind `primary-1e6b.3` (criome peer-identity ExecStartPost seed) and
`primary-1e6b.4` (mirror store-row seed generated from node config) can be
coded and unit-proven before the pair is standing; only the actual seeding
waits on the deploy.

## Resolvable now by the psyche (not worker tasks)

- **`primary-1e6b.6`** — decide how state is created on node A: arm a guardian
  agent so ordinary `Record` works organically, OR accept owner-only meta
  `Import` seeding for this slice. (Today `Record` is fail-closed:
  `ReferentGuardianRejected` — the current proof uses guardian-bypass meta
  `Import`.) This decision can be made immediately and unblocks the verification
  definition.
- **`primary-1e6b.1` authorization** — authoring the two guests touches the
  **private `goldragon`** cluster facts. This is authorization-gated; no worker
  should open/author those facts until the psyche grants it. Also inherits
  `primary-dw95`'s cluster-wide clavifaber/nota-derive deploy blocker.

## Real-world / deploy-gated stretch (after authorization)

`primary-1e6b.1 → .2 → {.3,.4} → .5 → .7`. Each is a real prometheus host
mutation on the push-first loop (fixtures pushed to GitHub, fired via
`ssh root@prometheus … nix …`; Rust/system builds run ON prometheus — local
build fails at `max-jobs=1`). BootOnce, never Switch. The verification bead
`.7` proves both the A→B mirror equality (`B head == A head` via destination
meta `Import` re-hash / mirror `ObserveHeads`) and persistence across a guest
restart, plus a fresh post-restart record propagating.

## Boundaries honored

- No `/nix/store` filesystem search. NOTA positional. jj on primary; no raw git.
- Private `goldragon` facts are referenced but not opened/quoted; `.1` is
  labelled `authorization-gated` and marked blocked behind `primary-dw95`.
- No implementation dispatched. Read-only source confirmation only for B1.

## Commands run (tracker mutations)

- `bd create` × 9 (epic `primary-1e6b` + 8 children); `bd update -d` × 8
  (descriptions); `bd dep <blocker> --blocks <blocked>` × 14 (edges).
- Read-back: `bd dep tree`, `bd dep list`, `bd list --parent`,
  `bd dep cycles` (no cycles).

## Blockers / unknowns carried forward

- `primary-dw95` is itself blocked cluster-wide (clavifaber pins deleted
  `nota-derive`, blocking all deploys) per its own notes — the whole
  deploy-gated tail inherits that until it clears.
- `primary-om4g.2` depends on `primary-om4g.1`; both are the ready leaves for
  the sender-side gate arming.
- Receiver-side per-request criome verification on the direct mirror ingress is
  DEFERRED (`primary-x3l7` real fix); the slice ships on the tailnet-bind
  stopgap + sender-side gate, per prior psyche acceptance. If the psyche wants
  receiver-verifiable criome attestation on every append, that pulls in the
  router-attestation variant (`primary-1e6b.8`) — a scope increase, not this
  slice.
