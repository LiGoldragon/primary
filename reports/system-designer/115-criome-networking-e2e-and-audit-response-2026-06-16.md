# 115 — criome: audit response, networking/e2e architecture, test-node status

*The psyche opened a large scope (networking, cross-node end-to-end testing,
meta-socket trust/key config, a reproducible test key) framed as "let's talk about
all this", and the system-operator landed a security audit
(`reports/system-operator/225`) of the BLS branch. This report accepts the audit,
maps the cross-node e2e architecture and its real gaps, reports the test-node status
the psyche asked me to check, and stages the work. No Spirit capture this turn —
the design is mid-discussion (see §"Intent" below).*

## 1 — The SO audit: accepted in full

The audit is correct and valuable; several findings are real gaps beyond what 114
flagged. This is a **crypto-core spike, not production-ready auth** — I agree it must
not integrate as "auth done" until the P1s land.

Triage:

| Finding | Sev | Mine to fix? | Note |
|---|---|---|---|
| Restored store mints unverifiable attestations (key B vs registered key A) | P1 | **yes** | Sharp catch. `on_start` must reconcile master key vs the registered `Host("criome")` key and fail loudly on mismatch; register-must-succeed when absent. |
| Expired attestations verify `Valid` | P1 | **yes** | Verifier needs a clock; return `Expired`. Clear correctness bug. |
| Key-file creation window + unsafe load | P1 | **yes** | `OpenOptions::create_new + mode(0600)` + fsync; reject non-regular/foreign-owned/symlink/loose-mode existing keys. |
| Verifier ignores `envelope.scheme` | P2 | **yes** | Match scheme; reject `MinSig` until implemented. |
| Preimage omits signer + validity interval | P2 | **yes** | Bind signer, issued_at, expires_at, scheme into the preimage. |
| Startup panics on key error | P2 | **yes** | `CriomeRoot::Error = crate::Error`; typed startup failure + corrupt-key test. |
| `ARCHITECTURE.md` stale | P3 | **yes** | Update in the same pass. |
| `RegisterIdentity` signature verification | P1 (open) | **kr40** | Not retired by this branch; stays critical on `primary-kr40`. |

The first seven are correctness/safety fixes I own and can land on `criome-auth-pilot`
immediately. The `RegisterIdentity`-signing gap is the deeper trust-root work that
keeps `kr40` open — until it lands, the registry is self-asserted and relabeling is
cheap, so even with the P1 fixes this is "sound spike", not "trustworthy auth".

## 2 — Test-node / networking status (what I could verify)

The psyche asked me to check whether the test node is wired. From the workspace:

- **`CriomOS-test-cluster`** is a *regression fixture* — pure `nix flake check`
  (Horizon projection, tailnet-controller rejection, network-service rendering). It
  never boots; it is not a live node.
- **The cloud-designer has real live-VM e2e capability** (reports 45–51): lojix ran
  live microVM e2e on a host "Prometheus" via a bespoke `/tmp/lojix-e2e` apparatus
  (48/49); report 50 proposes a *general, cluster-data-generated* VM-testing
  interface (branch `horizon-test-vm`) to replace the bespoke rig; 51 is a live VM
  host. So the **capability to boot live VM test nodes exists**, driven by projected
  Horizon cluster data.
- **What I cannot verify from files:** whether a node is *currently deployed and
  wired* for criome↔criome networking. That is runtime + cloud-designer's domain.
  Confirm with the cloud-designer / system-operator before assuming a live node.

**Recommendation (unblock-the-blocker):** start the networking test as a **local
two-daemon sandbox** (two criome instances over loopback or a network namespace pair
with real network transport + encryption between them) — this proves the cross-node
*protocol* without waiting on VM provisioning — then **graduate to the cloud-designer's
live-VM cross-node e2e** for the real topology. Per `skills/human-interaction.md`,
the sandbox is where we make production-grade conditions exist.

## 3 — The cross-node e2e, and the gap that blocks it

The psyche's flow: Spirit records → its configured **mirror** version-controls →
the logged message goes to **criome to be signed** → that message also carries node
**contact info** → it is sent across the network to the **peer node's criome** →
propagated → the peer **mirror** is told a new object was accepted in a spirit it
version-controls → the peer mirror **fetches the object**. Cross-network, encrypted.

Mapped to components (and where it connects to prior intent):

- **spirit** — records the intent; owns the per-operation digest; configured with a
  mirror for VC. (The auth pilot, `5zur`, attaches the criome attestation here.)
- **criome** — signs (auth). Today its wire is `signal-frame` over a *Unix socket*;
  it has **no network transport**. `signal-criome` has cross-criome *signature*
  routing (`RouteSignatureRequest`/`SignatureSolicitationRoute`, peers by socket
  name) — but that is quorum signature solicitation, not cross-node message/object
  propagation.
- **router** — per the message/router design (reports 75/76/111), the **router is
  the network-delivery authority** ("router routes … to agents across the network").
  So cross-node *delivery* is most coherently the router's job, not criome's —
  criome signs, the router delivers. The psyche's "sent through the crayon to the
  other crayon" likely folds delivery + auth together; worth separating: **criome =
  trust/signature, router = network delivery, mirror = object VC/fetch.**
- **mirror** — version-controls spirit's objects; the peer mirror is notified and
  fetches the new object.
- **networking layer** — node setup, network, encryption.

**The load-bearing gap:** *no component has a cross-node network transport with
encryption today.* criome, the router, and the mirror all speak local Unix-socket
`signal-frame`. The e2e the psyche wants needs a **networked, encrypted transport**
between nodes — a genuinely new capability. That is the first architectural decision,
and it sits underneath everything else in the flow.

## 4 — Open architecture questions (the discussion)

1. **Who owns networking setup?** A `system` component already exists but is scoped
   to OS/window *observation* (focus). The psyche mused "maybe the system component
   sets up networking." Options: extend `system` to own host networking setup; a new
   dedicated networking/transport component; or cloud + horizon own it (they already
   own tailnet/LAN derivation from cluster facts). The transport *protocol* (who
   speaks encrypted `signal-frame` over the network) is separate from *node network
   setup* (who configures interfaces/tailnet).
2. **criome's role across nodes:** trust + signature only (router delivers), or does
   criome itself carry cross-node messages? I lean criome-signs / router-delivers,
   reusing the existing message/router network-delivery intent.
3. **Trust + known keys via meta-socket config** (the psyche's "config message in
   the meta socket"): populate criome's identity registry + peer trust through an
   authenticated `meta-signal-criome` `Configure` — this is also the clean fix for
   the audit's restore-mismatch P1 (config declares the criome identity ↔ key
   binding rather than racing a generated key).
4. **Reproducible test key:** allow a *configured secret-key path* (a deterministic
   key checked into the test repo) alongside generate-on-first-run — so cross-node
   tests are reproducible.

## 5 — Staged plan (proposed)

1. **Land the audit P1 fixes** on `criome-auth-pilot` (the seven mine-to-fix items)
   — sound the auth core before networking is built on it. Fold in the configured
   secret-key-path (Q4) and the meta-config identity↔key binding (Q3) since they
   directly resolve the restore-mismatch P1.
2. **`RegisterIdentity` signing** (`kr40`) — the trust-root, with the operator.
3. **Local two-daemon networking sandbox** — criome (or router) network transport +
   encryption, two instances, real cross-process network test.
4. **Graduate to the cloud-designer live-VM cross-node e2e** — real topology.
5. **The full flow** — spirit record → criome sign → router cross-node delivery →
   peer mirror notified → mirror fetches object.

## Intent

No Spirit capture this turn. The networking/component design is mid-discussion
(psyche: "let's talk about all this", "maybe", "still figuring this out with the
cloud designer"), so it is exploratory, not settled. The two firmest items —
meta-socket trust/key config (Q3) and the configured test-key path (Q4) — are held
pending the discussion and will be captured as one clean key-custody/meta-config
decision once it converges (and once the `Clarify` edit path is repaired per
`primary-9cop`, so refining `psc6` does not stack a second record).
