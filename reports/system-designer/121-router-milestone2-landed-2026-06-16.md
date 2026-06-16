# 121 — Networking through the router: milestone 2 landed (the working forward)

*The working two-router forward is built, tested, and nix-green. This is the
landing record for milestone 2 of report 120's plan. Design + rationale:
report 120. Tracker: bead `primary-9x9f`.*

## What shipped

Branch `router-network-transport` on the `router` repo (commit `b5364876`,
**local — not pushed**), depending on the pushed `signal-router` contract
(`74484ac3`). Built by a build→adversarial-review workflow; the reviewer found
**no code defects** and independently re-ran the e2e + full suite.

- **`RemoteRouterRegistry`** (`src/remote_router.rs`) — a new child actor
  holding `RemoteRouterIdentity → TailnetAddress` (from `RegisterRemoteRouter`)
  and `recipient ActorIdentifier → RemoteRouterIdentity` (from `RegisterActor`
  whose `home` is `Some`). Decision shape **(A)**.
- **`RouterPeerDelivery`** (`src/peer_delivery.rs`) — the outbound network twin
  of `HarnessDelivery`: one `TcpStream::connect`, one `ForwardMessage` frame,
  one reply; runs off the mailbox.
- **`TailnetForwardIngress` + eager bind in `RouterRuntime::on_start`** — the
  corrected bind location (`RouterEngine` has no lifecycle hook + a lazy
  `OnceCell`). Decodes **only** `ForwardMessage`; verifies the attestation
  **off** the single-writer mailbox.
- **`ApplyForwardedMessage`** — stamps the **verified** peer identity as the
  origin (never the wire-claimed field; the attestation content-digest binds
  the sender), marks the message `Forwarded`, and reuses the local
  delivery + channel-auth path so a forward to a local harness delivers
  identically.
- **The seam** — the unregistered-recipient park path consults
  `RemoteRouterRegistry` *before* parking (local-first preserved). The
  `ForwardMarker` loop guard makes a `Forwarded` message never re-resolve
  remotely — airtight by construction (the reviewer confirmed there is no code
  path that re-forwards).
- **`ForwardAttestationVerifier` trait + offline `AcceptFixedTestIdentity`** —
  real content-digest binding (a tampered payload fails verify). This is the
  clean seam where **milestone 3 swaps in the criome client**.
- config network projection (fallible `from_raw`); typed `TailnetListener`
  error on the daemon side.

## The proof

`tests/end_to_end_remote_forward.rs`: two in-process `RouterRuntime`s on
OS-assigned loopback ports; submit on A for an actor homed on B; **A's trace =
`ForwardedRemote`, B verifies and delivers to its local harness, reply =
`ForwardAccepted`**. Diagnostic trace: A `[MessageCommitted, ForwardedRemote]`,
B `[MessageCommitted, DeliveryAttempted, DeliveryMarked]`. `nix flake check`
green; full suite (68 tests) + zero warnings, run independently by the
reviewer. Fully offline — no tailnet, no criome daemon.

## One gate hiccup (resolved)

The first `nix flake check` failed only on `process_boundary.rs`'s
`router_cli_reaches_working_observation_socket` — the daemon binary cold-started
slower than the test's 5s socket-wait under the (heavily loaded, all-session)
nix remote builder. No daemon crash, no panic — just slow spawn. Fixed by
giving the spawn test realistic headroom (5s → 30s); the socket normally
appears in well under a second. (A separate, mundane snag: a `nix flake
check -L` verbose run filled the task temp filesystem; re-run without `-L`.)

## Open items (all deferred by design — bead `primary-9x9f`)

- **Milestone 3 — real criome + replay window.** Swap the offline verifier for
  the criome client over `criome_socket_path`; add the router-owned bounded
  seen-`(signer, nonce)` window + clock-skew rejection. The replay window must
  land **with** real attestation (a valid attestation is trivially replayable
  until it exists). **This depends on the criome BLS track (bead `kr40`)**,
  which the psyche deferred ("not worrying about key encryption for now") — so
  milestone 3 is the point where networking rejoins the criome track.
- **Milestone 4 — live nodes.** The daemon-launched receive-only bind is still
  lazy (the `RouterEngine` `OnceCell` inits on first Unix connection); the
  in-process acceptance path binds eagerly. For live ouranos↔prometheus the
  daemon must init its runtime eagerly so a receive-only node binds its TCP
  ingress before any Unix traffic.
- **Low cosmetics:** `ForwardAccepted` carries a placeholder slot; an inbound
  forward to an unauthorized channel accept-and-parks rather than replying
  `ChannelUnauthorized`; transport failure on a down peer returns `Err` (no
  loss) rather than park-for-adjudication.

## Where this leaves networking-through-the-router

A complete, tested, **working offline** implementation: the contract is pushed
(`signal-router` M1), the daemon forwards end-to-end (`router` M2, local). The
remaining milestones (M3 real criome, M4 live) need the criome/key track the
psyche parked — so this is a natural pause point. Open decisions: push the
router branch / hand to the operator for integration; and whether to un-defer
the criome track to continue to a live forward.
