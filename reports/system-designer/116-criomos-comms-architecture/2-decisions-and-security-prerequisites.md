# 116.2 — decisions, security prerequisites, staged plan (the deliverable)

## The security reality (before any decision)

The cross-node mesh's trust chain is **not establishable today**, and the gap is
upstream of networking:

1. **criome registry has no admission control** — `IdentityRegistration` has no
   signer field; `register()` only dedups (`criome/src/actors/registry.rs:90`). Any
   principal reaching the working socket registers an arbitrary identity↔key. **#1
   prerequisite, above BLS.**
2. **First-cross-system-trust bootstrap is circular** — router B trusts A iff A's key
   is Active in B's criome registry, populated via an unbuilt peer surface over an
   unbuilt encrypted meta-session. No TOFU, no cluster-root-signs-members in code.
3. **Real BLS** — fixed on the `criome-auth-pilot` branch (reports 113/114), but on
   *main* sign/verify are still skeletons; the branch is unmerged.
4. **mirror ingest is unauthenticated** (`rj9y`/`x3l7`) — the bytes path that mutates
   the store is unverified even when the router notification is verified.
5. **No cross-router replay window** — must live in router (which sees the frame
   twice); router has no such state today.

These are **blocking security prerequisites**, not "dependencies."

## Decisions for the psyche

### A — Trust root: what admits a key into criome, and how is the first cross-system trust edge made? (THE prerequisite; the synthesis omitted it)

- **Cluster-root signs member keys** — a recorded cluster-root identity whose
  signature is the admission gate; `RegisterIdentity` requires a valid root/Developer
  signature; peer routers trust keys chained to the cluster root. *Scales a mesh;
  gives criome a real admission gate; subsumes the `kr40` RegisterIdentity-signing gap
  and the meta-signal-criome peer surface.* **(recommended)**
- **TOFU + out-of-band confirm** — trust-on-first-use, the psyche confirms each new
  peer out of band. Simple to start; weak at scale; manual.
- **Manual per-peer meta-socket provisioning** — each peer key installed by an
  authenticated meta-signal `Configure`. Explicit; rigid; no live revocation.

*Recommendation: cluster-root-signs-member-keys* — it is the only option that gives
criome a principled admission authority and a non-circular bootstrap. Everything else
(B/C/D, networking) is unsafe to exercise until this exists.

### B — Intra-host sandbox↔router transport (the SO_PEERCRED tradeoff)

- **tap/L3 (proven today)** — each guest already gets `<agent>.<cluster>.criome` + a
  routed IP; router fronts a per-node guest bridge. Ships on the proven substrate, the
  guest stays addressable — but it is L3 isolation, and the origin proof across the VM
  boundary must be designed (SO_PEERCRED doesn't cross). **(recommended first cut)**
- **vsock (AF_VSOCK)** — kernel-mediated, respects the private-netns isolation. But it
  **exists nowhere today** (needs a virtio-vsock device + reopening the closed
  `PeerIdentity` sum) and **loses SO_PEERCRED** (CID, not uid/gid), breaking the
  `MessageOrigin` minting `alom`/`n775` rely on.

*Recommendation: tap/L3 for the first cut* (proven, addressable, and the credential
story is solvable with a local-IP/criome attestation), with vsock as a later isolation
hardening once the credential-replacement is designed. (The synthesis preferred vsock;
the critique correctly flips this on the SO_PEERCRED loss.)

### C — Confirm the intent reframe (prose, low-ceremony)

`i99x` **already** records router as the cross-network delivery authority for the
gated/remote path — so router-owns-networking is largely a *realization* of recorded
intent, not a new decision. The one true **supersession** is narrowing `l3k4`'s
"harness-side ack is THE delivery fact" to the **local-harness path only**, so delivery
becomes per-path (harness-ack local · direct-ack local `i99x` · peer-router-ack
cross-network). I'll record that supersession (and the per-agent-microVM refinement of
`a4i6`) once you confirm the direction — flag if you disagree.

### D — Mirror topology + ingest authentication

- **Per-system mirror** (one per node, like router) — matches your two-mirror e2e
  (origin version-controls, peer fetches); router carries the lightweight
  `MirrorObjectNotify`, mirror keeps its proven fetch transport. *Plus: authenticate
  the ingest* (criome attestation on the object, per `x0ja`). **(recommended)**
- **One central mirror daemon** (today's `0yx5` model) — proven and simple, but does
  not naturally model a mirror-per-side.

*Recommendation: per-system mirror + authenticated ingest* — but `0yx5` recorded one
central daemon, so this needs your confirmation.

## Staged plan

1. **criome security core (foundation).** Merge the BLS branch + land the SO `225`
   P1 fixes + registry admission control (decision A) + the first-trust bootstrap.
   Nothing cross-node is trustworthy until this lands.
2. **spirit→mirror shipper (the missing e2e leg) + authenticated mirror ingest.**
   Build the ComponentShipper (it does not exist) on the proven local mirror arc.
3. **router network transport.** Lift `triad_runtime::TcpListenerDaemon` into router;
   signal-router network roots (listen address, `peer_routers`, `RemoteRouter`
   endpoint kind); criome `VerifyAttestation` on cross-router frames; router replay
   window; router discovery via `domain-criome` (.criome resolution).
4. **intra-host sandbox↔router** (decision B) + the cross-VM-boundary origin proof.
5. **two-node e2e** on the live ouranos↔prometheus tailnet (or a multi-node
   `mkVmTest`): spirit record → criome sign → router cross-net → peer mirror fetch.

## Intent

No Spirit capture this turn — the decisions are not yet made. When they are: the
architecture **extends** `alom`/`n775`/`i99x`/`a4i6`/`x0ja`; the one explicit
**supersession** the psyche must record is narrowing `l3k4`'s harness-ack delivery
clause to the local path (decision C); the per-agent-microVM topology **refines**
`a4i6` and needs explicit confirmation; the trust-root (decision A) is new intent.
All captured once the psyche decides — and the `Clarify` edit-path repair (`9cop`)
is wanted before refining records like `psc6`/`a4i6` so edits don't stack.
