# 183 — Orchestrate worktree audit and rework

*Kind: Audit + Rework Plan · Topic: orchestrate-schema-engine-port · Date: 2026-05-25 · Lane: second-operator*

## Situation

Yes: orchestrate is still the current work. The Spirit refresh was prerequisite context, not a replacement for the orchestrate parity task.

The current orchestrate state has two tracks:

- **Second-operator mainline track:** landed a narrower parser-backed schema witness across the orchestrate triad on `main`.
- **Second-designer feature track:** landed a richer prototype of the intended shape on feature branches, but under `/tmp`, not `~/wt`, and not integrated into current mainline.

The right next move is not to merge the designer branch wholesale. It should be treated as a design prototype and reworked into smaller operator slices that match the maturity Spirit now has.

## Mainline State I Own

Current clean mainline commits:

- `/git/github.com/LiGoldragon/orchestrate` — `59669e30` — `orchestrate: add schema upgrade witness`
- `/git/github.com/LiGoldragon/signal-orchestrate` — `df605591` — `signal-orchestrate: validate concept schema`
- `/git/github.com/LiGoldragon/owner-signal-orchestrate` — `37bbf4da` — `owner-signal-orchestrate: validate concept schema`

Report for that slice:

- `reports/second-operator/182-orchestrate-schema-mainline-integration-2026-05-24.md`

What it proves:

- `orchestrate` has parser-backed `.schema` files with local `./` imports.
- ordinary and owner routes lower into the assembled schema.
- short-header lookup works in schema tests.
- v0.1 to v0.1.1 upgrade planning exists as an additive schema witness.
- signal and owner-signal repos have parser-backed concept schemas.

What it does not prove:

- no daemon ingress path consumes generated `ShortHeader` yet;
- no signal contract is schema-derived yet;
- no `VersionProjection` is consumed by an upgrade runtime yet;
- no daemon handover socket or no-downtime protocol is live.

## Designer Track Audit

Designer report:

- `reports/second-designer/173-orchestrate-port-to-schema-engine-and-no-downtime-upgrade-2026-05-24.md`

Designer worktrees and commits:

- `/tmp/port-signal-orchestrate` — `45a63ab3` — `port: orchestrate schema source-of-truth + hand-equivalent emitter + handover protocol`
- `/tmp/port-orchestrate` — `44a98a7b` — `arch: record schema-engine port + drain-with-mirror handover plan`
- `/tmp/orchestrate-schema-example` — `0d16db07` — `schema: add orchestrate schema fixture + assemble witness`

All three worktrees are clean and pushed. The location is the first problem: current branch discipline says designer feature work belongs in `~/wt`, while operators maintain and rebase `main`. These `/tmp` worktrees should not become the ongoing authoritative worktrees.

The signal-contract branch is the valuable one. It adds:

- `orchestrate.schema`, using the richer v13 six-position schema shape;
- `src/schema_emitted.rs`, a hand-equivalent target for future macro output;
- `src/upgrade_handover.rs`, a drain-with-mirror no-downtime protocol skeleton;
- tests around short-header assignment, dispatch, Sema projection, and handover state transitions.

The key limitation is acknowledged in the designer report: the current macro stack cannot emit this shape yet because orchestrate needs multi-endpoint roots and unit endpoints:

- `Observe [Roles Lanes]`
- `Retire [Role Lane]`

That makes the branch a strong target specification, not a drop-in operator implementation.

## Nota Audit Impact

`reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` changes the implementation route.

The orchestrate port should not be advanced by teaching `signal-frame-macros/src/schema_reader.rs` more schema grammar. That private reader is already the drift surface: it accepts retired shapes and duplicates schema ownership. Orchestrate should instead pressure the shared `schema` crate toward the reusable lowering engine:

- authored `.schema` text;
- typed schema document and node-definition inputs;
- builtin lowerers;
- canonical `AssembledSchema`;
- downstream adapters for `signal-frame`, version projection, storage, and daemon registries.

This reinforces the recommendation not to merge `schema_emitted.rs` as production architecture. It is useful as an executable target specification, but production generation should come from `schema`-owned assembly plus a macro adapter.

## Rework Against Spirit Maturity

Spirit is now the maturity reference point after `reports/operator/177-schema-constraint-implementation-2026-05-24.md`.

Spirit has:

- schema macro constraints exposed as named Nix checks;
- schema-derived `ShortHeader` validation on the production ordinary daemon ingress path;
- an upgrade crate consuming contract-owned `VersionProjection`;
- named Nix checks for those constraints.

Orchestrate currently has:

- schema parser/import/lowering tests;
- short-header lookup tests at schema level;
- concept schemas in signal and owner-signal;
- a designer prototype for schema-derived dispatch and handover.

So orchestrate is behind Spirit in three concrete ways:

- **Ingress:** orchestrate does not reject mismatched short headers on a production daemon socket.
- **Projection:** orchestrate has upgrade-plan schema text, but no contract-owned `VersionProjection` consumed by `upgrade`.
- **Emission:** orchestrate still uses hand-written signal contract types; the designer `schema_emitted.rs` is a target sketch, not generated production code.

## Reworked Operator Plan

1. Recreate or rebase the designer feature work under `~/wt`, or explicitly retire the `/tmp` worktrees as prototypes and reimplement from their commits on `main`.
2. Pull the schema fixture/test parts forward first, because they are the least speculative and already prove the rich route shape.
3. Extend the shared schema lowering stack for multi-endpoint roots and unit endpoints before trying to switch `signal-orchestrate` to schema-derived production types. Do this by consolidating into `schema`, not by deepening the private `signal-frame-macros` schema reader.
4. Treat `schema_emitted.rs` as a temporary target-spec file only. Once the macro can emit equivalent code, it should disappear or remain as a test fixture, not become a parallel production contract.
5. Add production daemon ingress short-header validation after the signal contract exposes generated headers.
6. Add a contract-owned orchestrate `VersionProjection` and make the upgrade runtime consume it, matching the Spirit authority pattern.
7. Decide whether drain-with-mirror is accepted for orchestrate; if accepted, implement it after the projection and ingress pieces exist, because it depends on both.

## Immediate Recommendation

Keep bead `primary-8089` open, but split its implementation mentally into four operator slices:

- schema lowering capability: multi-endpoint + unit endpoint assembly, then macro adapter emission;
- signal contract cutover: schema-derived ordinary and owner types;
- daemon ingress: short-header validation on production receive path;
- upgrade/handover: contract-owned projection, then drain-with-mirror.

Do not merge `45a63ab3` wholesale into `signal-orchestrate` main right now. It contains good code-shaped design, but it would create a second hand-written contract layer beside the existing one before the macro is ready to own that layer.

## Questions Needing Psyche

1. Should the `/tmp` designer worktrees be recreated under `~/wt` and rebased as living feature branches, or should they be treated as frozen prototype commits that operator mines from while reimplementing on `main`?
2. Is drain-with-mirror accepted as orchestrate's no-downtime upgrade protocol, given orchestrate's lane-claim authority role?
3. Should multi-endpoint + unit endpoint schema lowering support be part of the Spirit schema epic, or a separate shared schema slice driven by orchestrate and mind?
