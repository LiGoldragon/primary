# Lojix / Horizon / CriomOS rewrite intent and implementation audit

## Frame

User request: review `reports/system-designer/42-horizon-167-intent-divergence-and-fixes.md`, research the full intent behind the Lojix / Horizon / CriomOS reworking, audit the implementation, and write an independent report.

This is an operator-lane audit from the outside. I did not edit the implementation branches. I read the reports, inspected the current concept code, and ran tests where they were safe to run.

## Sources read

Primary intent and synthesis:

- `INTENT.md` — two deploy stacks, schema-driven stack, three schema types, Nexus as mail keeper, schema-at-heart.
- `reports/system-designer/42-horizon-167-intent-divergence-and-fixes.md` — the report under review.
- `reports/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md` — the original Horizon pure-schema concept.
- `reports/system-designer/41-horizon-schema-pipeline-concept/0-frame-and-method.md` — the current collections + Horizon concept brief.
- `reports/system-designer/40-horizon-lojix-schema-next-port-feasibility/3-overview.md` and `4-collections-and-option-gate-explained.md` — the port feasibility and collection gate.
- `reports/system-designer/39-schema-cargo-cross-crate-import/3-overview.md` — cross-crate schema import and types-only-module finding.
- `reports/system-designer/37-prototype-schema-deep-iteration-2-nexus-mail-sema-engine-2026-05-27/3-overview.md` — schema-deep Lojix depth iteration.
- `reports/system-operator/164-criomos-lojix-rewrite-audit-and-production-vision-2026-05-27.md` and `165-lojix-source-staging-prototype-and-full-component-critique.md` — production vision and source-staging implementation critique.
- `reports/system-designer/36-criomos-reconciliation-audit.md` and `29-lean-horizon-cluster-data-shape.md` — production-to-lean reconciliation and Horizon destination data shape.

Implementation inspected:

- `/home/li/wt/github.com/LiGoldragon/schema-rust-next/horizon-schema-concept/` — the `/167` prototype.
- `/home/li/wt/github.com/LiGoldragon/schema-next/collections-horizon-2026-05-28/` — current collection implementation.
- `/home/li/wt/github.com/LiGoldragon/schema-rust-next/collections-horizon-2026-05-28/` — current collection emitter implementation.
- `/git/github.com/LiGoldragon/horizon-next/` — current Horizon concept repository.
- `/git/github.com/LiGoldragon/horizon-rs/` and `/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape/` — production and lean destination Horizon shapes.
- `/git/github.com/LiGoldragon/lojix/` plus `schema-deep` and `schema-deep-iteration-2` worktrees — current daemon rewrite surfaces.

Spirit records I treated as load-bearing:

- 905, 906, 908 — production-to-lean reconciliation and remote-build constraint.
- 974 — prototypes must use designed components fully, or develop incomplete components instead of bypassing them.
- 1000 — schema-emitted types are the canonical truth source.
- 1028, 1030, 1037, 1038 — three-engine / origin-route / don't leave scaffolding dead.
- 1034, 1045, 1048, 1049, 1050 — collections syntax, KeyValue rename, Horizon pure-schema demonstration, anti-marketing, runtime shape open.
- 1058 — this audit request.

## Validation I ran

- `/git/github.com/LiGoldragon/horizon-next`: `cargo test` — passed, 7 Horizon projection tests.
- `/git/github.com/LiGoldragon/horizon-next`: `nix flake check` — passed, but emitted crane placeholder warnings for missing workspace package name/version.
- `/home/li/wt/github.com/LiGoldragon/schema-next/collections-horizon-2026-05-28`: `cargo test` — passed, including 8 new collection tests and existing lowering / resolution tests.
- `/home/li/wt/github.com/LiGoldragon/schema-rust-next/collections-horizon-2026-05-28`: `cargo test` — passed, including 6 collection-emission tests, cross-crate import tests, and legacy emission tests.

## The full intent, compressed

The Lojix / Horizon / CriomOS rework is not one refactor. It is three converging arcs:

1. **Production continuity.** The live cluster still deploys through the old `lojix-cli` stack using `horizon-rs`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`, and `goldragon` on main. That stack remains the only deployable path until replacement witnesses exist.
2. **Lean Horizon / Lojix rewrite.** The `horizon-leaner-shape` arc cleans the cluster data boundary: cluster proposal data should be dials and facts, not CriomOS implementation constants. Roles become variants; booleans and derived predicates move out of the proposal; CriomOS / CriomOS-lib own operational constants and Nix predicates.
3. **Schema-derived substrate replacement.** The deeper direction is that Horizon and Lojix stop maintaining hand-authored boundary types. Schema declares data types; schema-rust-next emits Rust / NOTA / rkyv; hand-written Rust attaches behavior to those nouns. Lojix becomes a daemon with Signal, Nexus, and SEMA centers. Horizon's projection should either remain a pure schema-generated library or become a component shape, but its datatypes should still come from schema.

The important synthesis: **this is not “make current Lojix compile.”** It is “keep production safe while moving deployment and projection onto schema-emitted nouns, typed mail, durable SEMA, and component-shaped authority.”

## Review of report 42

Report 42 is substantially correct for the artifact it audited: `/167` was a real, honest, working pipeline, but it generated a collections-free Horizon caricature. The report correctly identifies the four big divergences:

- no real collections, so not real Horizon aggregate types;
- duplicated runtime/support floor instead of a shared schema core;
- pure type modules forced to carry vestigial Input/Output planes;
- three-engine machinery emitted but not driven.

I agree with its bottom line: `/167` should not be thrown away. It is a stepping stone. The right fix is to grow the missing schema substrate and then regenerate a more real Horizon.

The one thing report 42 now lacks is recency against the implementation that followed it. The current `horizon-next` / collections work has partially closed D1, but it also exposes new divergences from later intent.

## Implementation audit — what is real now

The current implementation has real progress beyond `/167`.

### Collections are implemented and tested

`schema-next` now has:

- `TypeReference::Plain`;
- `TypeReference::Vector`;
- `TypeReference::Map`;
- `TypeReference::Optional`.

It lowers collection forms at reference positions and preserves non-collection behavior. `schema-rust-next` emits `Vec<T>`, `BTreeMap<K, V>`, and `Option<T>`, plus NOTA collection codecs. Tests pass in both repos.

### `horizon-next` proves the collection path on a Horizon-shaped slice

`/git/github.com/LiGoldragon/horizon-next/horizon/schema/horizon.schema` declares:

- a map of nodes;
- vector fields;
- optional cache field;
- a cross-crate imported `Magnitude`;
- `Input::Project` and `Output::Projected` / `Rejected`.

Generated code contains a collection-bearing `ClusterProposal`:

- `nodes: BTreeMap<NodeName, NodeProposal>`;
- `cache: Option<BinaryCache>`;
- `cluster_services: Vec<ServiceName>`.

The concept also adds behavior in the right place: `ClusterProposal::project(&self) -> Output` and `NodeProposal::project_node(&self, ...)` are methods on schema-emitted nouns, not free projection helpers. The tests construct a real map-bearing proposal, run projection, round-trip NOTA, archive through rkyv, and round-trip an output signal frame.

This is no longer the `/167` two-fixed-node / one-feature-only toy. It is a genuine proof that the collection gate can be crossed.

## Implementation audit — remaining divergences

### 1. The collection name is already stale: `KeyValueMap` vs `KeyValue`

Spirit record 1045 says the collection macro is named `KeyValue`, not `KeyValueMap` and not `Map`. The current collection implementation, tests, docs, and Horizon schema still use `KeyValueMap`.

This should not land to main as-is. It will create immediate schema-language churn and rework every Horizon schema written against the stale name.

Fix: rename the macro and test surface from `KeyValueMap` to `KeyValue` before integration. If backward compatibility is desired for the branch, accept `KeyValueMap` only as a deprecated alias in tests that assert the alias is transitional.

### 2. Explicit lowercase field names reintroduce a field-authoring surface

The collection implementation supports schema fields like:

```nota
ClusterProposal [(nodes (KeyValueMap NodeName NodeProposal))]
```

That is useful mechanically, but it conflicts with the earlier schema discipline that field names are inferred from type names and that records are positional. It also introduces snake_case/camelCase field-name tokens into the schema surface.

The shape report 42 itself proposed is better:

```nota
NodeFeatures (Vec NodeFeature)
Node [NodeName MajorNodeKind NodeFeatures]
Nodes (KeyValue NodeName Node)
ClusterProposal [ClusterName Nodes]
```

That keeps named type boundaries as the field identity. It also matches the workspace naming discipline: the schema authors nouns, not anonymous field-name/type pairs.

Fix: prefer collection newtypes (`Nodes`, `NodeFeatures`, `ClusterServices`, `OptionalCache`) and field-name derivation. If explicit field names remain necessary for some cases, they need a fresh psyche decision because they are a schema-language expansion, not just an implementation detail.

### 3. `horizon-next` is still a representative slice, not “all needed Horizon datatypes”

The current `horizon-next` schema proves collections, but it does not generate Horizon's actual destination datatypes.

The lean destination in `horizon-rs/horizon-leaner-shape/ARCHITECTURE.md` names a much richer input surface:

- `HorizonProposal`;
- `ClusterProposal` with nodes, users, domains, trust, secret bindings, tailnet, AI provider selections, VPN profiles;
- `Role` with about 15 variants, including data-carrying `NixBuilder`, `PersonaDevelopment`, `Router`, `CloudHost`, and capability roles;
- `NodePlacement` / `Pod`;
- `Machine`, `Io`, `NodePubKeys`, `Wireguard`, `ClusterTrust`, users, domains, secret references;
- `Viewpoint` and a viewpoint-scoped `view::Horizon` output.

The current concept instead has:

- `NodeRole (Center Edge Builder)`;
- one `services: Vec<ServiceName>` string-ish field;
- no `HorizonProposal`;
- no `Viewpoint`;
- no users/domains/secret bindings/placement/machine/io/pubkeys;
- no JSON consumer witness.

That is fine as a collection proof, but it must not be described as generating “all Horizon datatypes.” The honest label is: **collection-bearing Horizon concept slice**.

Fix: the next schema should mirror the lean destination architecture, at least for the aggregate roots and role taxonomy. Minimum next target: generate `Role`, `NodePlacement`, `NodeProposal`, `ClusterTrust`, `ClusterProposal`, `HorizonProposal`, `Viewpoint`, and a small `Horizon` output with JSON emission.

### 4. The imported `Magnitude` is not yet the shared-schema-home story

The current `horizon-next` creates a local `horizon-core` crate with:

```nota
Magnitude (Zero Min Low Medium High Max)
```

That is neither the real lean `horizon-rs` ladder (`Zero Min Medium Large Max`) nor the workspace universal `Magnitude` intent (`Minimum VeryLow Low Medium High VeryHigh Maximum`). It also does not use the previously proven `/39` `schema-core` shared home directly; it creates a Horizon-local core crate.

There may be a valid reason for Horizon to keep its own capacity/trust ladder. If so, the schema should make that explicit and avoid colliding mentally with the workspace universal Magnitude. If not, this is a shared-type divergence.

Fix: decide whether Horizon's magnitude is domain-specific or shared. If domain-specific, align the variants with the real Horizon ladder and document why it is not the universal Magnitude. If shared, import the real shared type from the shared schema home once that exists.

### 5. The duplicated generated support floor remains

`horizon-next/horizon/src/schema/horizon.rs` emits the whole generic support floor:

- `Text` / `Integer`;
- `NotaDecodeError`;
- `NotaSource`, `NotaBlock`, `NotaText`, `NotaCollection`;
- signal short-header support;
- mail event and Nexus traits;
- upgrade traits.

That is exactly report 42's D2. Collections did not fix it. It is acceptable for a concept, but it should not multiply across every generated module forever.

Fix: extract the generic floor into a shared schema/runtime crate after types-only modules land. Generated modules should import the floor, not re-emit it.

### 6. Types-only modules are still unresolved

The current Horizon concept avoids the types-only-module problem by making Horizon a component-like schema with `Input` and `Output`. That is a legitimate exploration under Spirit 1050, but it does not solve the shared-types case. Even `horizon-core/magnitude.schema` carries a token Input/Output plane:

```nota
(Input ((Rank Magnitude)))
(Output ((Ranked Magnitude)))
```

That is a vestigial signal plane on a shared type crate.

Fix: implement imports + namespace-only schema modules. Then shared type crates such as schema-core / persona-mail / horizon-core can be honest type homes.

### 7. The runtime-shape question is still open, but the implementation leans component

Spirit 1050 leaves Horizon's runtime shape open: library, signal-only, or full triad. `horizon-next` chooses the component-ish shape (`Input::Project`, `Output::Projected`), but it does not yet include a daemon or a SEMA state plane.

That is not wrong. It is a useful demonstration. But the report should phrase it as a runtime-shape experiment, not a settled architecture. A pure projection library remains viable, and a full triad would need owner authority / SEMA state decisions that have not been made.

### 8. Lojix integration still has the old Horizon text placeholder

The Lojix rewrite has two valuable but split branches:

- `/165` source staging on `schema-deep`;
- `/37` sema-engine / Nexus mail / Communicate depth on `schema-deep-iteration-2`.

These have not yet been amalgamated. More importantly for Horizon: the source-staging report still names `HorizonView(Text)` as a placeholder. The current `horizon-next` proof has not yet replaced that with a schema-emitted Horizon view object in Lojix's schema.

Fix: merge the Lojix schema-deep branches first, then replace `HorizonView(Text)` with generated Horizon types or an imported `horizon-next` projection result. Do not wire another string wrapper around the new proof.

### 9. Nix witness passes, but packaging hygiene is unfinished

`horizon-next` passes `cargo test` and `nix flake check`, but with caveats:

- root `Cargo.toml` has no workspace package name/version, so crane emits placeholder package warnings;
- repository is currently a plain Git repo, not a jj-backed working tree;
- files are staged/untracked rather than landed as a clean commit at the time of this audit;
- `ARCHITECTURE.md` and `INTENT.md` exist but were untracked in `git status`.

These are normal for an in-flight concept, but they matter before integration. The workspace's “always push all changes” and jj discipline should apply before any handoff.

## What report 42 missed or should now amend

Report 42 was correct as an audit of `/167`. If it were updated against the current implementation, I would add four findings:

1. **D1 is partially closed:** collections now exist and are proven on a Horizon slice.
2. **D1 is not fully closed:** the slice is still not the real Horizon datatype surface.
3. **New D1a:** collection syntax/name drift (`KeyValueMap` vs `KeyValue`) must be fixed before landing.
4. **New D1b:** explicit field-name pairs are a schema-language decision and appear to conflict with field-name derivation intent.

## Recommended next sequence

1. **Normalize collection syntax now.** Rename `KeyValueMap` to `KeyValue` and decide whether explicit field names are allowed. My recommendation: use named collection newtypes and keep field-name derivation.
2. **Commit and push the current concept cleanly or label it explicitly as in-flight.** No untracked `INTENT.md` / `ARCHITECTURE.md`; no plain-git ambiguity if jj is expected.
3. **Move from concept slice to real Horizon root slice.** Generate the lean destination aggregate roots: `Role`, `NodePlacement`, `NodeProposal`, `ClusterTrust`, `ClusterProposal`, `HorizonProposal`, `Viewpoint`, and a minimal `Horizon` output.
4. **Add JSON emission and a Nix consumer witness.** Horizon's production value is not just Rust and NOTA; CriomOS consumes JSON. The next proof should show generated types projecting to JSON that a tiny Nix fixture reads.
5. **Keep projection as methods on generated nouns.** The current `ClusterProposal::project` placement is correct. Scale that up; do not move projection into free helper functions or a string transformer.
6. **Extract shared support after types-only modules.** Cross-crate import is proven. Use it to remove the duplicated floor once the schema language can express type-only crates.
7. **Amalgamate Lojix branches before wiring Horizon.** Source staging and sema/Nexus depth compose; wire Horizon into the combined branch, not one half.
8. **Replace `HorizonView(Text)` with a typed imported shape.** This is the moment where the Horizon proof becomes part of Lojix rather than a standalone demonstration.

## Bottom line

The direction is right. Report 42's criticism of `/167` was accurate, and the current implementation proves the most important fix — collections — is real enough to run. But the current `horizon-next` implementation is still a **collection-bearing concept slice**, not the final “all Horizon datatypes” proof. The highest-risk drift is not technical failure; it is language/intent drift: using `KeyValueMap` after `KeyValue` was chosen, adding explicit field names despite field-name-derivation intent, and calling a small slice “Horizon” before it mirrors the lean destination shape.

My recommendation: fix the schema-language surface immediately, then make the next Horizon proof mirror the actual lean architecture instead of growing the current toy taxonomy. Once that root slice emits and JSON/Nix consumes it, the port will have crossed from “demonstration” into “replacement substrate.”
