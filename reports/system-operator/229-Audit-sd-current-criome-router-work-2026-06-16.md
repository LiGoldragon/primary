# 229 — Audit: SD current criome/router work

The psyche asked for a situation read on what SD is working on, an audit of
the code already made, and the parts that are unclear or objectionable.

## What SD is working on

SD has two active arcs:

1. **Criome authentication handoff.** This is the completed auth branch stack:
   real BLS signing, real verification, cluster-root admission of external
   identity registrations, and the `signal-criome` contract fields needed to
   carry admissions. This is the auth substrate for Spirit and later
   router/mirror trust.
2. **Networking through the router.** This is the new active work from report
   120: `signal-router` grows a router-to-router forwarding contract, and
   `router` grows a milestone-2 daemon implementation that forwards a message
   over loopback TCP between two in-process router runtimes. The intended path
   is local router → tailnet TCP → peer router, with criome attestation replacing
   `SO_PEERCRED` across the network hop.

The router work is now more than design. It exists in two worktrees:

- `signal-router/router-network-transport`: committed branch
  `74484ac3` (`signal-router: RegisterActor.home for remote-route resolution`).
- `router/router-network-transport`: uncommitted working copy on branch
  `router-network-transport`, with about 2k inserted lines across daemon,
  runtime, peer delivery, remote registry, attestation seam, and e2e tests.

## Verification Run

`signal-criome/criome-admission-gate`:

- `nix flake check` — passed. This confirms SD fixed report 228's P1 stale
  NOTA fixture issue at commit `4b27b935`.

`signal-router/router-network-transport`:

- `nix flake check` — passed.

`router/router-network-transport`:

- `cargo test --offline` — passed, including
  `tests/end_to_end_remote_forward.rs`.
- `cargo clippy --offline --all-targets -- -D warnings` — passed.
- `cargo fmt --check` — failed. The failures are mechanical formatting in
  `src/config.rs`, `src/lib.rs`, `src/peer_delivery.rs`, `src/router.rs`, and
  `tests/end_to_end_remote_forward.rs`.
- `nix flake check` — inconclusive in this audit. It reached the remote-build
  phase and then sat silent for several minutes; I terminated only my audit's
  local `nix flake check` process. A separate Claude/SD-launched
  `nix flake check -L` process for the same router worktree was also running
  under `/tmp/router-m2-flakecheck.log`; I did not touch it.

## What The Code Does

### Criome

The auth stack now has the right broad shape:

- `signal-criome` adds `IdentityRegistration.admission`,
  `CriomeDaemonConfiguration.cluster_root`, and
  `RejectionReason::UnauthorizedRegistration`.
- `criome` threads the configured cluster root into `IdentityRegistry`.
- external `RegisterIdentity` is rejected unless the registration carries a
  valid cluster-root `SignatureEnvelope`.
- the previous scheme-confusion bug is fixed; `ClusterRoot::admits` rejects
  non-`Bls12_381MinPk` admission envelopes.

My remaining caveat from report 228 still applies: the daemon's own
`Host("criome")` self-registration bypasses the cluster-root gate. That may be
the intended local self-owned bootstrap, but it means the production
"cluster-root signs each node's criome master key" ceremony is not enforced in
code yet.

### Signal Router Contract

`signal-router` now carries the router-to-router forwarding wire vocabulary:

- `ForwardMessage(RouterForwardRequest)`.
- `ForwardAccepted(RouterForwardAccepted)` and
  `ForwardRefused(RouterForwardRefused)`.
- `ForwardedMessagePayload`, `RouterPeerAttestation`, `ForwardMarker`,
  `ReplayNonce`, `TimestampNanos`, `TailnetAddress`, and
  `RemoteRouterIdentity`.
- `RegisterRemoteRouter`.
- `RegisterActor.home: Optional RemoteRouterIdentity`, which is SD's chosen
  milestone-2 answer for "which actor lives behind which peer router?"
- `RouterDaemonConfiguration.tailnet_listen_address`, `router_identity`, and
  `criome_socket_path`.

This branch is clean under Nix. I understand the design trade: the contract
stays self-contained, so it does not depend on `signal-criome` or
`signal-message`. The daemon maps between the self-contained forwarding record
and real component records.

The tradeoff I want watched: this duplicates crypto-adjacent vocabulary
(`SignatureScheme`, attestation fields) and message payload shape. That is
acceptable for milestone 1 only if milestone 3 adds projection tests against
real `signal-criome::Attestation` and current `signal-message` semantics.

### Router Daemon

The router daemon code implements a real offline milestone-2 forward:

- `RemoteRouterRegistry` owns peer identity → tailnet address, and recipient
  actor → peer identity.
- `RouterPeerDelivery` is the outbound TCP client: one `TcpStream`, one
  length-prefixed `signal-router::ForwardMessage`, one reply.
- `TailnetForwardIngress` implements `AsyncConnectionRuntime<TcpStream>`,
  decodes only `ForwardMessage`, verifies through the
  `ForwardAttestationVerifier` seam, asks `RouterRuntime` to apply the
  forward, and writes one `signal-router::Output`.
- `RouterRuntime::on_start` eagerly binds the TCP listener when configured.
  This corrects SD's earlier design mistake of trying to bind from the lazy
  non-actor engine.
- `RouterRoot::retry_pending` preserves local-first behavior: local harness
  lookup runs first; if it misses and the message is not already forwarded,
  the remote-route table is consulted before parking.
- the e2e test starts two routers on `127.0.0.1:0`, registers a target only
  on router B, routes a message on router A, and proves B delivers to its
  local harness while A reports `ForwardedRemote`.

That is real progress. The witness proves the transport seam and actor
placement are viable.

## Findings

### P1 — Router branch is not clean: `cargo fmt --check` fails

The current `router/router-network-transport` working copy is not ready to
hand off or merge because `cargo fmt --check` fails. This is mechanical but
still a real gate in this workspace.

The affected files are:

- `src/config.rs`
- `src/lib.rs`
- `src/peer_delivery.rs`
- `src/router.rs`
- `tests/end_to_end_remote_forward.rs`

### P1 — `ForwardAccepted` returns a fake slot

The receiving ingress returns:

- `src/router.rs:394` maps `ForwardApplied::Accepted` to
  `SignalRouterOutput::forward_accepted(signal_router::MessageSlot::new(0))`.

But `apply_forwarded` actually mints a real signal slot:

- `src/router.rs:2243` calls `next_signal_message_slot`.
- `src/router.rs:2250` persists using that slot.
- `src/router.rs:2253` records the message/slot mapping.

The real slot is then discarded; the network reply always says slot `0`.
That violates the contract meaning of `RouterForwardAccepted` as "peer
accepted the forward, returning the minted delivery slot." The e2e test only
checks that the reply variant is `ForwardAccepted`, so it does not catch this.

Fix shape: make `ForwardApplied::Accepted` carry the minted `SignalSlot` or
the `signal_router::MessageSlot`, and have the ingress return that.

### P1 — `ForwardAccepted` currently means "persisted/enqueued", not "delivered"

`apply_forwarded` always returns `ForwardApplied::Accepted` after
`retry_pending()` succeeds:

- `src/router.rs:2257` calls `retry_pending`.
- `src/router.rs:2258` returns `Accepted`.

It does not inspect whether the message was delivered, parked for
adjudication, left pending because the recipient is unknown locally, or blocked
by channel authorization. Meanwhile the forwarding contract has refusal
reasons for `RecipientUnknown`, `ChannelUnauthorized`, and `AlreadyForwarded`.

This may be a semantic decision, but it is not clear. There are two coherent
options:

- **Accepted means durable acceptance by the peer router.** Then the refusal
  enum should stop implying local delivery/auth refusal, and the docs/tests
  should say the sender only knows the peer took custody.
- **Accepted means delivered/routed locally.** Then `apply_forwarded` must map
  local unknown recipient and channel-adjudication cases to `ForwardRefused`
  where appropriate.

The current shape says both things in different places, so I do not trust the
protocol semantics yet.

### P2 — The loop guard is not reflected in the network reply

Inbound forwards are always converted to
`PendingRouterMessage::forwarded(...)`, so they will not be re-forwarded. That
part is good.

But `RouterForwardRequest.forwarded` is ignored by `TailnetForwardIngress`:

- `src/router.rs:377` verifies only attestation and payload.
- `src/router.rs:387` sends only `verified_origin` and `payload` into
  `ApplyForwardedMessage`.

The `AlreadyForwarded` refusal reason is therefore not exercised. If the field
is meant to be a first-class wire guard, the ingress should reject
`ForwardMarker::Forwarded` or otherwise document why the receiver ignores the
wire marker and always applies its own local marker.

### P2 — The daemon path installs the offline test identity even from real config

`RouterDaemonConfiguration` now carries `router_identity` and
`criome_socket_path`, but `RouterEngine::from_configuration` still builds:

- `AcceptFixedTestIdentity::new(RemoteRouterIdentity::new("router-offline-test"))`

That means a daemon started with a tailnet listener today signs/verifies with
the shared offline test identity, not its configured `router_identity`, and it
does not use `criome_socket_path`.

The comments are honest that this is milestone 2, and milestone 3 swaps in
criome. Still, this must be operationally fenced. A deploy should not be able
to accidentally start this as a real tailnet transport and think it is using
criome auth.

Recommended guard: reject `tailnet_listen_address: Some(...)` in the production
daemon path unless an explicit offline-test mode is also present, or keep the
listener constructor test-only until the criome verifier lands.

### P3 — The self-contained forwarded payload may drift from `signal-message`

`ForwardedMessagePayload` carries `from`, `to`, `body`, and `attachments`.
On receive, router reconstructs a `SignalMessageSubmission` with
`MessageKind::Send`.

That is fine for the current e2e, but it means the forwarding contract is not
yet a faithful transport for arbitrary future `signal-message` semantics. If
message kinds, rich bodies, attachment metadata, or sender/origin distinctions
grow, the self-contained payload must grow in lockstep or the forwarding path
will silently project away meaning.

## What I Agree With

- The high-level split is right: criome signs/verifies identity, router
  transports/routs messages, tailnet encrypts bytes.
- Binding TCP in `RouterRuntime::on_start` is the right lifecycle fix.
- The local-first seam is the right place to add remote routing.
- The dedicated `RemoteRouterRegistry` and `RouterPeerDelivery` owners are
  better than widening `RouterRoot` with raw maps and TCP calls.
- Keeping the local Unix `SO_PEERCRED` path untouched while adding a separate
  network ingress is the right risk boundary.
- The loopback e2e is a good milestone witness. It proves real TCP framing and
  real actor interaction without requiring two machines.

## What I Do Not Yet See Clearly

- Whether `ForwardAccepted` means "peer took custody" or "peer delivered/routed
  locally." The code and the refusal enum disagree.
- Whether `ForwardMarker` is meant to be trusted as a sender-declared field, or
  only a local receiver-side marker. The code treats it as local-only; the
  contract makes it look wire-load-bearing.
- How the real criome attestation projection will bind exactly the same bytes
  that `ForwardedMessagePayload` represents. The offline verifier only checks a
  local FNV digest over a subset of fields and ignores scheme/public-key/signature
  semantics.
- How production config will prevent accidental use of the offline verifier.

## Operator Read

Criome auth is close to operator integration after the signal-criome fixture fix,
modulo the self-admission/provisioning decision.

The router networking work is promising but still in-progress. I would not merge
the `router` working copy as-is. First steps should be:

1. Run `cargo fmt`.
2. Fix `ForwardAccepted` to return the real minted slot.
3. Decide and encode the `ForwardAccepted` semantics.
4. Add negative e2e tests for unknown recipient, unauthorized channel, wrong
   attestation/digest, and loop-guard behavior.
5. Fence the offline verifier from production daemon config.
6. Re-run full `nix flake check` after the other agent's long-running check
   settles.
