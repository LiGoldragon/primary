# 124 - Spirit-vcs Router PoC: clarification blockers and dependency/style status

## Status summary

The offline PoC is real and currently green from the `spirit` checkout:

```text
cargo test --features mirror-shipper --test end_to_end_offline_full_chain
```

Result: one test passed. The path proven is:

```text
spirit A records intent
-> mirror A receives shipped version-control state
-> router A forwards an object-accepted notice to router B
-> mirror B restores exactly to the router-announced head
```

What this proves: the causal chain is valid. Spirit can produce mirrored state, Router can carry the notice, and the receiver restores precisely the announced state.

What it does not yet prove: production criome authentication on the router hop, production mirror notification/auto-fetch, or live ouranos-to-prometheus Yggdrasil deployment.

## Areas needing clarification before full implementation

### 1 - Production mirror notification contract

Current PoC uses a harness-local `MirrorObjectNotice { store, head }` carried as a Router message body. The production path needs a real contract decision:

- Does `signal-mirror` get a `MirrorObjectNotify` / `ObjectAccepted` input?
- Does Router deliver that input directly to mirror, or to a mirror-side adapter actor?
- Is the notice just `{store, head}`, or does it also carry source router, source mirror, durability, digest, and fetch hints?
- What is the refusal surface when mirror sees a notice but cannot fetch or restore?

This is the largest semantic gap between "harness proof" and "component implementation."

### 2 - Mirror auto-fetch responsibility

The current harness explicitly tells mirror B to restore after the notice is received. Full implementation needs the owner of that action:

- Mirror may subscribe/receive a `MirrorObjectNotify` and fetch/restore itself.
- Router may only deliver the notice and remain payload-blind.
- A future orchestration/mind policy actor may decide when a received notice becomes a restore.

Recommendation: mirror owns fetch/restore once notified; Router stays transport/policy.

### 3 - Router criome m3 seam

Router m2 has the correct seam but uses `AcceptFixedTestIdentity`. Full implementation needs:

- outbound `ForwardAttestationVerifier::attest` to ask local criome to sign the exact forwarded payload digest;
- inbound verify to ask local criome to verify against the recomputed digest;
- Router to stamp the criome-verified identity, never the wire-claimed identity;
- mapping from criome decisions to `RouterForwardRefusalReason`.

Clarification needed: make the verifier trait async, or keep a synchronous mapping trait and perform criome I/O in `TailnetForwardIngress`.

### 4 - Router-owned replay and freshness

Criome proves a payload was signed, but a valid signed frame can still be replayed. Router needs its own window:

- skew tolerance;
- duplicate `(signer, nonce)` rejection;
- durable `router-forward-replay` SEMA family;
- restart survival;
- eviction policy.

Clarification needed: exact skew tolerance and whether the replay table is maintained by a child actor or directly under `RouterRuntime`.

### 5 - Service-scoped `.criome` endpoint invariant

The short-term live target should be:

```text
router.<node>.<cluster>.criome -> node Yggdrasil address
Router config supplies port -> [ygg-address]:router-port
```

Clarification needed: which repo owns the alias projection first:

- CriomOS `network/default.nix` adds `router.<node>.<cluster>.criome` host aliases;
- Horizon exposes service endpoint names explicitly;
- `message-router.nix` derives the alias locally without changing Horizon.

The architecture now says Router startup must fail closed if the audited service name does not resolve to the literal Yggdrasil address in its startup archive.

### 6 - Cluster-root provisioning ceremony

Criome BLS/admission is mostly in place, but a live authenticated mesh needs admitted router identities:

- what is the exact router identity type/name: Host, Cluster, service principal, or dedicated Router principal?
- does the cluster-root sign node criome keys only, or service-specific Router identities too?
- do we build the one-shot admission-signing CLI now?
- where is the cluster-root secret held during the pilot?

This is the live-auth bootstrap blocker.

### 7 - Deploy capability and host scope

The live test needs daemons on at least ouranos and prometheus:

- `criome.nix`;
- `message-router.nix`;
- `MessageFabric` service capability;
- firewall binding to Yggdrasil;
- per-node peer manifest.

Clarification needed: confirm `MessageFabric` as its own capability rather than tying the fabric to `PersonaDevelopment`.

### 8 - Mirror transport reconciliation

Mirror's current NixOS module still binds TCP on Tailscale-style settings. Router's short-term live fabric is Yggdrasil.

Clarification needed: move mirror live TCP to Yggdrasil for the first full live chain, or keep mirror separate and only use Yggdrasil for Router.

Recommendation: converge mirror toward Yggdrasil for daemon fabric; leave Tailscale/Headscale as human/admin overlay.

### 9 - Whether full reaction-frame porting gates the PoC

Spirit and Router are using the generic schema reaction-frame style. Mirror still has concrete `NexusWork` / `NexusAction` schema. That is not blocking the spirit-vcs Router PoC.

Clarification needed: is "everything ported to the new style" a prerequisite for live mirroring, or a parallel cleanup? Recommendation: parallel cleanup. Do not block Router m3/m4 on mirror reaction-frame conversion.

## Dependency and new-style status

| Component | Current integration state | Dependency/style status | Gap |
|---|---|---|---|
| `spirit` | Full offline chain harness exists on `main`; targeted test passed in this session. | Uses current `schema-next#abaae95`, `schema-rust-next#733b76d`, `triad-runtime#f46f66`, `signal-frame#e2eae5`, `nota-next#7426a6`. Ported to generic `Work`/`Action` reaction frames. | Lock still contains stale unused `sema-engine` rev entries, though active cargo tree resolves current `sema-engine#73eea24`. Full `nix flake check` previously hit network fetch failure, not code failure. |
| `meta-signal-spirit` | Main carries `MirrorTarget` / `MirrorAddress` and `mirror_target` config fields. | Main is `90d64b1f`; Spirit locks this exact main commit. Schema-derived contract style. | No obvious PoC gap. |
| `mirror` | Main carries `Arc<Engine>` shipper support used by Spirit harness. | Spirit locks `mirror main#91ec76fa`. Schema-derived daemon/sema/nexus modules exist. | Mirror's `schema/nexus.schema` still uses concrete `NexusWork` / `NexusAction`, not generic reaction frames. TCP ingress remains hand-wired; production mirror auto-fetch notify not built. |
| `signal-router` | Main carries forwarding contract (`ForwardMessage`, `RemoteRouterIdentity`, `RegisterRemoteRouter`, `RegisterActor.home`, `ForwardedRemote`). | Spirit/Router lock `signal-router main#7331456f`; build passes. | `signal-router main` still locks older `schema-next#e721626` and `schema-rust-next#6e04d70`. Local unbookmarked work `81221e0a` suggests a schema-support pin refresh started but is not the bookmarked integration state. |
| `router` | Main has m2 networked router-to-router forwarding. `router/ARCHITECTURE.md` now documents service-scoped `.criome` endpoint invariant. | Main/Cargo lock use current schema/toolchain pins: `schema-next#abaae95`, `schema-rust-next#733b76d`, `triad-runtime#f46f66`, `sema-engine#73eea24`, `signal-frame#e2eae5`. Ported to generic `Work`/`Action` reaction frames. | M3 real criome verifier + replay/freshness window not built. Remote `main` seen at `39f62df3`; Spirit lock still pins router `075ca731`, which contains m2 and is enough for the PoC. |
| `signal-criome` | Main has admission contract fields. | Main is `20ed63db`; criome locks it. Schema-derived contract style. | No blocking PoC gap for offline path. |
| `criome` | Main has restored real-BLS/auth pilot; branch `criome-auth-pilot#c6b6e132` has final repin. | Main locks `signal-criome#20ed63db`, `sema-engine#73eea24`, `triad-runtime#f46f66`, `signal-frame#e2eae5`, `nota-next#7426a6`. | `criome main` still locks `schema-rust-next#e2e20b`, older than current `733b76d`. Need regenerate/pin-refresh if "latest generator everywhere" is required. Production key custody and provisioning ceremony still open. |
| `meta-signal-criome` | Skeleton/config contract exists. | Current main observed at `16b9a196`. | Not yet the deployed meta-config authority for criome; `criome-write-configuration` / one-binary-startup deploy path still needs confirmation/building. |
| `schema-next` | Main provides schema generics and current schema lowering. | Main observed at `abae95f`. | Core support exists. |
| `schema-rust-next` | Main provides current emitter, including generic frame expansion used by Spirit/Router. | Main observed at `733b76d`. | Some consumers still locked to older emitter revisions. |
| `triad-runtime` | Current shared runtime used by Router/Spirit/Criome active graph. | Main observed at `f46f66e`. | No immediate PoC gap. |
| `sema-engine` | Current active graph resolves main `73eea24`. | Used by Spirit/Router/Criome current graph. | Lockfile cleanup may be needed where stale rev entries remain. |

## Dependency conclusion

The PoC path is not blocked by dependency drift. The active Spirit full-chain harness builds and passes against the mainline pins it currently locks.

But the answer to "is everything on the latest new style?" is **no**:

- Spirit and Router are on the generic reaction-frame schema style.
- Mirror is schema-derived but not converted to generic reaction frames.
- Signal contracts are schema-derived; not all locks are on the latest generator revision.
- `signal-router main` is the most visible generator-pin laggard.
- `criome main` also lags current `schema-rust-next`.
- Some local working copies are sitting on unbookmarked or feature commits, so remote/bookmarked main should be treated as the integration truth unless a lane explicitly lands the local state.

## Recommended next implementation order

1. Build Router m3 against real criome: async/sync seam choice, criome client, replay/freshness SEMA family, refusal mapping, restart-survival tests.
2. Define and implement production `signal-mirror` notify + mirror auto-fetch path.
3. Add `router.<node>.<cluster>.criome` alias projection and Router startup invariant test.
4. Build `criome.nix` and `message-router.nix` under a `MessageFabric` capability.
5. Build the cluster-root/router-identity admission ceremony.
6. Run live ouranos-to-prometheus Yggdrasil forward, then full spirit-vcs remote mirror.
7. In parallel, refresh schema generator pins and reaction-frame ports where not yet updated; do not make that a prerequisite for Router m3 unless the codegen change directly touches the edited crate.

## Verification performed

- `cargo test --features mirror-shipper --test end_to_end_offline_full_chain` in `/git/github.com/LiGoldragon/spirit`: passed.
- `cargo check --locked` in `/git/github.com/LiGoldragon/signal-router`: passed from the current local checkout.
- Inspected Cargo locks and branch heads for `spirit`, `router`, `signal-router`, `meta-signal-spirit`, `mirror`, `criome`, `signal-criome`, `schema-next`, `schema-rust-next`, `triad-runtime`, `sema-engine`, `nota-next`, and `signal-frame`.
