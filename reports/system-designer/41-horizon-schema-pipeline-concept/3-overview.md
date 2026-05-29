# Overview — Horizon schema pipeline concept (orchestrator synthesis)

*Orchestrator synthesis closing the `/41` arc. The concept the psyche asked to SEE working — Horizon's datatypes generated from a pure schema, step by step, actually running — is delivered and verified. Built across two subagent passes (the first crashed on infrastructure mid-build and was recovered; the second finished it + reached the freshest intent). Verified by me, not relayed: pushed commits confirmed, the running three-engine chain confirmed at file:line, the hermetic `nix flake check` confirmed green.*

## What landed (verified)

- **The pipeline generates Horizon's real datatypes from a pure schema** — `horizon/schema/horizon.schema` → nota-next → schema-next → schema-rust-next → emitted Rust with `ClusterProposal { nodes: BTreeMap<NodeName, NodeProposal>, cache: Option<BinaryCache>, cluster_services: Vec<ServiceName> }`, the imported `Magnitude`, and `Output::Projected(BTreeMap<NodeName, NodeConfig>)`. Real collections (map of N nodes, Vec services, Option cache) — not `/167`'s fixed-field proxy. The step-by-step walkthrough with pasted artifacts is `1-build-and-step-by-step-walkthrough.md`; the completion detail is `2-completion-and-fresh-intent.md`.
- **A running three-engine chain** (records 1028/1030 + 1054) — verified: `Plane::drive` at `horizon/src/schema/horizon.rs:874`; `impl SignalEngine for SignalGate` / `impl NexusEngine for ProjectionNexus` / `impl SemaEngine for ProjectionSema` at `horizon/src/lib.rs:133/168/215`. `Plane::drive` threads a real `ClusterProposal` projection request Signal→Nexus→Sema and echoes the origin route. Not dead scaffolding (record 1030) — it drives, with a passing end-to-end test (`three_engine_chain.rs`).
- **The record-1054 data-carrying `Plane` enum** — variants carry the actual messages (matched directly), superseding the crashed agent's separate-envelope+`Kind`-tag shape that record 1052 calls wrong. Origin route (1038/1039) auto-created as the variant's leading tuple element.
- **Types-only modules (D3)** — Input/Output now optional at the 4-position document (`Asschema.signal_plane: Option<SignalPlane>`); `horizon-core` is a pure type library (emitted Rust dropped ~520→~150 lines, zero runtime floor).
- **Hermetic witness** — `nix flake check` on the pushed clean tree passes 12 checks (build/test/fmt/clippy + 8 architectural-truth checks), including `running-three-engine-chain`, `plane-surface-data-carrying`, and `types-only-core-has-no-runtime-floor`. The finisher caught + fixed a real fake-green (the chain test file was untracked, so the `git+file://` flake source skipped it) — exactly the anti-marketing discipline (record 1049) the psyche demanded.
- **Pushed + in sync**: schema-next `f73274f6`, schema-rust-next `419db039`, horizon-next `1b64d1b` (GitHub remote created, public, matching siblings) — all on `collections-horizon-2026-05-28`, local==remote verified. Per-repo INTENT/ARCHITECTURE updated (record 944).

## Divergence closure (vs `/42`)

| Divergence | Status |
|---|---|
| D1 — collections-free caricature | CLOSED — real `BTreeMap`/`Vec`/`Option` cluster proposal generates + projects |
| D3 — vestigial signal planes | CLOSED — types-only modules; `horizon-core` carries no signal plane |
| D4 — engines emitted not driven | CLOSED — `Plane::drive` runs the three-engine chain end to end |
| D2 — duplicated runtime floor | CLOSED for the type-library case (floor gone from `horizon-core`); the dedicated shared-floor crate across MULTIPLE components is honestly deferred (one component = no duplication yet) |

## What's honestly still open

- **D2's dedicated shared-floor crate** — deferred until a second component exists to share with (the floor lives once today; a second component would re-emit it). This is `/37/3` Decision A / B (shared schema home / persona-mail) at the workspace scale.
- **The `Plane` payload for distinct execution languages** — Horizon is Signal-only, so its `Plane` Nexus/Sema variants carry the Signal roots (`Input`/`Output`), which is correct for Horizon. A schema like Spirit with distinct `NexusInput`/`SemaInput` languages would, under the deepest reading of 1054, carry those — the current emitter carries the Signal roots uniformly. Record 1062 (captured this session) flags the related origin-route-placement question. Both pending psyche confirmation.
- **Operator reconciliation of the nota-next pin** (record 1057) — the three repos are aligned to nota-next `5e063042` on the feature branches; the operator reconciles both pins to main on integration.

## What it unblocks

The horizon-next concept is the de-risking evidence for the next real migrations:

- **`signal-persona-spirit` onto the schema-derived stack** — `/43` (the `/168` review) recommends migrating production Spirit's domain types + reply shapes onto schema-next/schema-rust-next as the structural fix for `/168`'s findings 4 + 8 (the reply-shape double-wrapper + schema-not-source-of-truth). horizon-next proves the emitter handles exactly the surfaces Spirit needs: collection payloads, cross-crate shared types, the clean data-carrying reply enum, types-only modules. Spirit is the natural next consumer (spirit-next was the pilot; production persona-spirit is the destination).
- **The lojix/horizon schema-next port** (`/40`) — `/40` named collections as the decisive Gate-1 unlock. It is now landed + proven. The horizon datatype port (Gate 2) is unblocked; the projection logic was already schema-at-heart (`/40` Wave A).
- **The emitter no-ancestry naming improvement** (`/43` finding-7 fold-in) — schema-rust-next should shed containing-type ancestry from emitted field names, with a witness, so migrations don't re-introduce names like `record_identifier_selection`.

## Bottom line

The psyche asked to SEE the schema pipeline working for Horizon, not marketing. It works — real collections, a running three-engine chain, hermetic Nix green, pushed, verified by me at file:line and by re-reading the `nix flake check` result. It closes three of the four `/42` divergences and the type-library instance of the fourth, and it implements the freshest plane design (record 1054). The open items are honestly bounded and named. The concept de-risks the production-Spirit migration `/43` recommends and the lojix/horizon port `/40` scoped.

## See also

- `0-frame-and-method.md` / `1-build-and-step-by-step-walkthrough.md` / `2-completion-and-fresh-intent.md` — the frame, the verified walkthrough, the finisher's completion detail.
- `/system-designer/42-horizon-167-intent-divergence-and-fixes.md` — the D1-D4 divergences this closes.
- `/system-designer/43-spirit-signal-surface-168-review.md` — the production-Spirit migration this unblocks.
- `/system-designer/40-horizon-lojix-schema-next-port-feasibility/3-overview.md` — collections as the Gate-1 unlock, now landed.
- Spirit records 1034 (collections), 1054 (Plane enum), 1038/1039 (origin route), 1028/1030 (three-engine chain that drives), 1057 (nota-next pin), 1060 (iterative deepening), 1062 (NEW — Plane origin-route placement, pending confirmation).
