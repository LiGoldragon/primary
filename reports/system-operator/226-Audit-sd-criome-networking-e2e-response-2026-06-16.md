# 226 — Audit: SD criome networking/e2e response

Reviewed `reports/system-designer/115-criome-networking-e2e-and-audit-response-2026-06-16.md`.

## Verdict

The report is directionally right and accepts the security audit honestly. Its strongest point is separating three concerns that were getting blurred:

- criome authenticates and signs;
- router should probably own message delivery;
- mirror/version-control owns object propagation and fetch.

The important caveat: report 115 is a planning/triage report, not an implementation update. None of the P1 crypto hardening from system-operator report 225 has landed in the `criome-auth-pilot` worktree yet.

## Findings

### P1 — Do not let meta-config design block the immediate key-mismatch fix

Report 115 proposes folding “configured secret-key path” and “meta-config identity↔key binding” into the first audit-fix slice because they directly resolve the restore-mismatch P1.

They are related, but they should not be a prerequisite for the immediate P1. The current bug is simple and local: `CriomeRoot::on_start` must reconcile the loaded/generated master public key with the existing registered `Host("criome")` identity and fail loudly on mismatch. That fix can land now without waiting for `meta-signal-criome` to grow authenticated key configuration.

Meta-config is the better long-term custody/control path. It should not hold the short-term safety fix hostage.

### P1 — “CriomOS-test-cluster never boots” is now inaccurate

Report 115 says `CriomOS-test-cluster` is a pure `nix flake check` regression fixture, never boots, and is not a live node.

The “not a live node” part is fair. The “never boots” part is now stale. `/git/github.com/LiGoldragon/CriomOS-test-cluster/README.md` and `flake.nix` expose Prometheus runners and an nspawn smoke runner:

- `nix run .#run-on-prometheus`
- `nix run .#build-dune-on-prometheus`
- `nix run .#nspawn-dune-on-prometheus`
- `nix run .#nspawn-spirit-upgrade-on-prometheus`

That still does not provide a ready criome↔criome network e2e, and SD’s conclusion remains mostly intact. But the test substrate status should be phrased as: “fixture cluster with pure checks plus Prometheus/nspawn runners; no standing live criome network node and no cross-node criome transport test yet.”

### P2 — “router owns cross-node delivery” is plausible, not settled by current router

SD’s lean, “criome signs / router delivers,” is architecturally attractive. It lines up with router owning routing policy and delivery state.

But current router intent and implementation are local: `router.sock`, local channel authorization, local harness delivery, and local durable delivery state. The router does not currently have a cross-node encrypted transport or a remote-peer delivery contract. If router becomes cross-node delivery authority, that is a real router expansion, not just “use the existing router.”

The report should state this more sharply: router is the best candidate owner, but it needs a new remote-delivery adapter/contract and a network transport substrate.

### P2 — The transport substrate should be specified before choosing component ownership

Report 115 correctly identifies “no component has cross-node encrypted transport” as the load-bearing gap, but the staged plan jumps to “criome (or router) network transport + encryption.”

That “or” is doing too much work. Before deciding whether criome or router opens remote sockets, the reusable substrate needs a shape:

- transport type: TLS, Noise, SSH tunnel, or signed frames over an encrypted channel;
- peer identity binding: criome BLS key, host identity, or node certificate;
- frame semantics: raw `signal-frame` over network, a network envelope around `signal-frame`, or component-specific remote frames;
- replay and freshness behavior;
- where connection state lives and how it is configured.

Without that, the first implementation is likely to become a component-local transport that every other daemon reimplements.

### P2 — The full-flow description needs mirror/server precision

The psyche flow in §3 says spirit’s configured mirror version-controls, peer criome receives, peer mirror is notified, and peer mirror fetches the object.

That is the right rough story, but it leaves an important boundary unstated: mirror notification/fetch is not just networking, it is the sema version-control server/mirror protocol. The report should name whether the peer mirror is:

- the sema mirror daemon from the version-control stack;
- a component-local spirit mirror actor;
- or a future networked object store.

This matters because the router/criome path should probably deliver an attested object reference and proof, while the mirror path should fetch/verify object bytes through the version-control protocol.

### P3 — Intent/no-capture judgment looks correct

I agree with SD’s “no Spirit capture this turn” call for report 115. The networking ownership and key-config mechanism are still discussion-level; forcing a durable decision now would probably create cleanup work.

## What Is Solid

Report 115 accepts the audit without defensiveness and accurately keeps `RegisterIdentity` signing on `primary-kr40`.

The cross-host gap is real. `signal-criome/ARCHITECTURE.md` explicitly says cross-host transport is open, and current criome/router/message surfaces are local `signal-frame` over Unix sockets.

The local two-daemon sandbox is the right first proof target, as long as it uses the same transport substrate intended for real nodes rather than a bespoke test-only shortcut.

## Recommendation

Use report 115 as a discussion map, but tighten it before it becomes a work order:

1. land the local audit P1 fixes first, without waiting for meta-config;
2. correct the `CriomOS-test-cluster` status;
3. split “network transport substrate” from “which component owns delivery”;
4. treat router-as-cross-node-delivery as a proposed expansion, not current fact;
5. specify the mirror/object-fetch boundary in the full e2e.
