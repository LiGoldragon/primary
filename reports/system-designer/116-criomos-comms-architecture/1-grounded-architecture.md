# 116.1 — the architecture, grounded in code

## The shape

Each agent runs in one real KVM/qemu microVM (**proven live**:
`CriomOS/modules/nixos/test-vm-host.nix` — own kernel, writable root + store, sized
from cluster machine facts, `microvm.vms.<guest>`). Inside it the agent runs its
component daemons, each with its per-component-per-domain agent space (Spirit `a4i6`)
and its own criome BLS identity (the public key *is* the identifier — `jtmt`/`3fm6`).
The microVM is the new *physical* isolation boundary; it **refines** `a4i6`'s logical
agent-space unit (one VM nests many component spaces). This nesting is unrecorded
production topology — only test constructs exist today — so the psyche must confirm it.

One **router per system** owns transport in two directions; **criome stays
auth-only**; **mirror** moves bytes; **spirit** is intent.

## Components (scope · role · transport)

| Component | Scope | Role | Transport |
|---|---|---|---|
| microVM sandbox | per-agent | isolation host for one agent + its component spaces | to its router: tap/L3 today, vsock proposed |
| **router** | **per-system (one per node)** | the fabric: cross-sandbox local + cross-network router↔router; channel-auth + delivery authority for the routed path | binds intra-host (vsock/tap) + inter-host tailnet TCP; Unix meta socket |
| message | per-agent | SO_PEERCRED ingress / existence boundary; mints `MessageOrigin`; stays separate (`alom`) | `message.sock` Unix 0660 |
| criome | per-agent (+ node peer-key registry) | auth-only identity/signature; "criome verifies, Persona decides" | `criome.sock` Unix 0600; meta socket; **never a network socket** |
| mirror | per-system or central (open) | object version-control / fetch; append-ingest, ack-after-durable-write | `triad_runtime::TcpListenerDaemon` on the tailnet |
| spirit | per-agent | intent; a Record is a sema commit; its outbox is what the mirror ships | `spirit.sock`; ComponentShipper → its mirror (**does not exist yet**) |
| triad-runtime | shared lib | transport substrate: `TcpListenerDaemon`, signal-frame codec, `PeerIdentity {Unix, Tcp}` (closed sum) | provides Unix + TCP; vsock variant proposed |
| orchestrate / mind | per-system | Persona decision plane: decides delivery of verified cross-router messages, authorizes cross-system grants | router meta socket; router→mind transport is a stub today |

## Current state (the seam is pre-cut, but unwired)

Router and message are **strictly local, single-host** today: message = stateless
SO_PEERCRED ingress → forwards to router over Unix; router = channel-auth +
adjudication + persists `router.sema` + delivers **only** to local harness/PTY Unix
sockets (`EndpointKind [Human HarnessSocket PtySocket]`). **Zero network transport,
zero encryption, zero criome auth, no peer-router concept** in any daemon. But the
wire model already anticipates it (`ConnectionClass::Network`/`OtherPersona`,
`HostName`/`NetworkPeer` types), and triad-runtime ships an unwired `TcpListenerDaemon`
("cross-host transport, tailnet-only ingress"). mirror **already proves** the
inter-host pattern: a green cross-host TCP e2e over the tailnet
(`mirror/tests/end_to_end_arc.rs`, `PeerIdentity::Tcp`, `tcp_listen_address` from
rkyv config).

## Transport tiers (grounded)

- **Inter-host router↔router — SOUND and AVAILABLE.** Reuse the mirror precedent:
  `TcpListenerDaemon` bound to the tailnet interface (Yggdrasil `200::/7` over yggTun,
  or WireGuard), length-prefixed signal-frame, `PeerIdentity::Tcp`. **Encryption is
  the tailnet**; per-frame authenticity is the criome BLS detached attestation
  (honors `x0ja`: blake3 + BLS, no divergent scheme). **Two live tailnet nodes
  already exist** (ouranos↔prometheus, ~16ms) — a real two-node bed.
- **Intra-host sandbox↔router — the genuine fork.** vsock (AF_VSOCK) is the clean
  kernel-mediated isolation fit for the private-netns microVM — **but it does not
  exist anywhere today** (needs a virtio-vsock device + reopening the closed
  `PeerIdentity` sum) **and it loses SO_PEERCRED** (vsock gives a CID, not uid/gid),
  which breaks the `MessageOrigin` minting `alom`/`n775` depend on. tap/L3 is
  proven-today (each guest already gets `<agent>.<cluster>.criome` + a routed IP) but
  is L3 isolation and still needs an origin-minting story across the VM boundary. This
  is decision **B** in `2-…`.

## The e2e flow (and its real gaps)

1. Spirit records → sema commit + outbox suffix. *(works)*
2. Spirit's mirror version-controls the outbox → tailnet TCP → mirror `ServerCommitted`.
   **GAP: the spirit→mirror ComponentShipper does not exist** (no mirror dep in
   `spirit/Cargo.toml`). This is the first leg and it is unbuilt.
3. The message is built carrying the peer node's contact-info in
   `signal-message::ConnectionClass` (**not** criome — criome is address-free).
4. Origin router asks its criome to `Sign` a detached attestation over the frame
   digest (extends `2st7` cross-router). **GAP: real BLS — fixed on the
   `criome-auth-pilot` branch, not on main; not merged.**
5. Origin router → peer router over tailnet TCP (encrypted by the tunnel).
6. Peer router → its criome `VerifyAttestation`; trusts iff `Valid`. **GAP: criome
   registry has no admission control (decision A); peer-key surface unbuilt.**
7. Persona/mind decides delivery; peer-router-ack is a **new cross-network delivery
   fact** `l3k4`'s harness-ack does not cover (decision C).
8. Peer router notifies the peer mirror (new `MirrorObjectNotify` channel kind).
9. Peer mirror fetches the object by blake3 ref (ImportSession restore — green).
   **GAP: mirror ingest is unauthenticated (`rj9y`/`x3l7`) — the bytes path that
   mutates the store is unverified even if the notification is verified.**

## message / router relationship

They stay **two separate components** — this **extends** `alom` (SO_PEERCRED boundary
cannot move into router) and `n775` (message keeps its meta-signal owner-policy plane).
But the per-agent-microVM split puts message *inside the guest* and router *on the
host*, so the message→router hop crosses the VM boundary — where vsock has no
SO_PEERCRED. The same-host-Unix ingress assumption breaks; a replacement origin proof
at that hop is **undefined** and must be designed (a tap/L3 + local-IP credential, or
a criome attestation at the boundary). On delivery authority: `i99x` **already**
recorded router as the cross-network delivery authority for the gated/remote path — so
the network role is largely a *realization* of `i99x`, and the only true supersession
is narrowing `l3k4`'s "harness-side ack is THE delivery fact" to the local path
(decision C).
