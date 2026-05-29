# Audit — `/167` Horizon pure-schema concept: divergence from intent + fixes

*Designer audit of `reports/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md` against intent. Per psyche directive 2026-05-28: point out where `/167` diverges from intent, with proposed fixes. Artifact-grounded — I read the report, `concept/horizon/schema/proposal.schema`, and the full emitted `tests/fixtures/horizon-concept/generated/src/schema/lib.rs` (777 lines) on the `horizon-schema-concept` branch (commit `vzxyzkptokqm`). `/167` is real and honest work; the divergences below are mostly "deferred the hard parts" — reasonable for a prototype, but divergent from the FULL intent of generating Horizon's actual datatypes.*

## What `/167` gets right (the baseline is sound)

Verified real, not marketing: the pipeline genuinely runs (`examples/horizon_concept.rs` writes the three observable stages — `01-input-schema`, `02-assembled-schema`, `03-generated-rust`); the emitted `lib.rs` is a substantial genuine schema-emitted file (real `ClusterProposal`/`Node`/`ProjectionRequest`/`Input`/`Output` types with full NOTA codecs + signal-frame encode/decode); intra-crate imports work (`pub use crate::schema::proposal::ClusterProposal as Proposal;` + the per-module `NotaDecodeError` bridges); it incorporates the latest runtime model (plane envelopes `Signal<Root>`/`Nexus<Root>`/`Sema<Root>` with `origin_route`, `InputNexus`/`OutputNexus` dispatch traits, `UpgradeFrom`); and the report has an honest "Limits Exposed" section. This is a working pipeline with real artifacts — it meets the anti-marketing bar (Spirit 1049). The divergences are about WHAT the pipeline generates and HOW the support layer is structured, not whether it runs.

## Divergence 1 — the generated datatypes are a collections-free caricature, not real Horizon (CENTRAL)

**Intent**: the psyche asked to "generate all of the needed data types for Horizon using a pure schema" (Spirit 1048), and proposed collections as the enabling syntax (Spirit 1034: `Vec <element>`, `KeyValueMap <key> <value>`). `/40` established collections as the decisive gate — the real `ClusterProposal` is collection-bearing (a map of N nodes, each with a Vec of features).

**Divergence** (artifact): `proposal.schema` declares
```
Node [NodeName MajorNodeKind NodeFeature]          ; ONE feature per node
Workstation [Node]
Router [Node]
ClusterProposal [ClusterName Workstation Router]   ; exactly TWO fixed node slots
```
So a "cluster" is hard-wired to exactly one Workstation + one Router, and a node has exactly one feature. The real Horizon cluster is N nodes keyed by name with multiple features each. `/167` generates a **2-node, 1-feature-per-node proxy**, not Horizon's actual datatypes. `/167` honestly flags this (its limit #2) — but it is the central divergence from "generate all the needed Horizon datatypes": the thing the psyche wanted to SEE generate (the real cluster proposal) is exactly what isn't generated.

**Proposed fix**: implement Spirit 1034 collections (grow `TypeReference` from a bare name into an enum with `Vector`/`Map`/`Optional`, per `/40/4`), then the schema becomes the real shape:
```
NodeFeatures (Vec NodeFeature)
Node [NodeName MajorNodeKind NodeFeatures]
Nodes (KeyValueMap NodeName Node)
ClusterProposal [ClusterName Nodes]
```
**Already in motion**: the `/41` build subagent (in flight) is implementing exactly this collections capability + demonstrating it on a collection-bearing Horizon schema. `/167` + that collections work converge into the real datatype generation.

## Divergence 2 — the generic runtime floor is hand-emitted and duplicated per module, not a shared schema core

**Intent**: schema-at-heart (Spirit 1000: schema-emitted types are the canonical truth for every type; no hand-written shims); the shared-schema-home direction (`/37/3` Decision A); cross-crate import as the mechanism (`/39`, proven in Nix).

**Divergence** (artifact): the emitted `lib.rs` carries, hand-emitted into the module, the entire generic runtime floor — `Text`/`Integer`/`NotaDecodeError`, the plane envelopes `Signal<Root>`/`Nexus<Root>`/`Sema<Root>`, `OriginRoute`, `MessageIdentifier`, `MessageRoot`, `MessageSent`, `NexusMail`, `MessageProcessed`, the `MessageSentHook`/`InputNexus`/`OutputNexus` traits, `UpgradeFrom`/`AcceptPrevious`. None of these are Horizon-specific; they are generic substrate. `/167` admits (limit #3) the support floor is "duplicated per generated module." This diverges from schema-at-heart's DRY intent: the generic runtime types are emitter-injected boilerplate replicated in every module rather than declared once and imported.

**Proposed fix**: a shared `schema-core` crate (the `/39` proof's `core` crate is the seed) owns the generic floor — `Text`/`Integer`/`NotaDecodeError`, the three plane envelopes, `OriginRoute`, the mail types, and the engine-trait shapes — and every consumer module IMPORTS them via the `/39` cross-crate import (`pub use schema_core::...`), which is already proven to work in Nix. This is `/37/3` Decision A (shared schema home) made concrete, using the `/39` mechanism that already exists. Note `/167` used INTRA-crate imports (`pub use crate::schema::...`) — the fix extends to CROSS-crate (`pub use schema_core::...`) so the floor lives in ONE place workspace-wide, not once per crate.

## Divergence 3 — pure type modules are forced to carry vestigial signal planes

**Intent**: Horizon's runtime shape is open (Spirit 1050) and a pure-projection-library Horizon needs the types-only-module shape; `/39` found the 4-position document forces a signal plane onto any schema module.

**Divergence** (artifact): `proposal.schema` is a pure TYPES module (cluster nouns), yet it is forced to declare its own signal plane:
```
(Input ((Accept ClusterProposal)))
(Output ((Accepted ProjectionReceipt) (Rejected ProjectionRejection)))
```
The proposal module has no business being a signal component — it's a type library imported by `lib.schema`. The `(Input ...)`/`(Output ...)` here is vestigial, present only because the 4-position document requires non-empty Input/Output. Same for `view.schema`. This diverges from the types-only-module need: pure type modules should be Imports + Namespace only.

**Proposed fix**: implement the types-only-module schema shape (`/39`'s flagged gap) — make Input/Output OPTIONAL at the 4-position document so a module that only declares types needs no signal plane. Then `proposal.schema` and `view.schema` drop their vestigial Input/Output; only the boundary `lib.schema` (the actual component surface) declares them. Pairs naturally with Divergence 2's shared `schema-core` (also a types-only module).

## Divergence 4 — the three-engine runtime model is emitted but not driven (scope boundary to confirm)

**Intent**: designed components must ACTUALLY drive the system, not be dead scaffolding (Spirit 1030); the runtime is three trait-ordered engines + plane envelopes (Spirit 1028/1037).

**Divergence** (artifact, softer): `/167` EMITS the plane envelopes + `InputNexus`/`OutputNexus` dispatch traits + `MessageSent` hooks, but does not WIRE a running three-engine chain (Signal→Nexus→Sema threading the envelopes) or a daemon that exercises them. The tests exercise the TYPES + NOTA codec + signal-frame round-trip + the import boundary — real and valuable — but not a live three-engine pipeline. Per Spirit 1030, emitted-but-unexercised engine traits risk being dead scaffolding.

**Why this is softer**: the psyche themselves left Horizon's runtime shape OPEN (Spirit 1050 — library? signal-only? triad?), and the concept's CORE ask was datatype GENERATION, which `/167` delivers. So this is a scope boundary, not a clear flaw. **Proposed fix / confirm**: decide Horizon's runtime shape (Spirit 1050) — the `/41` frame argues Horizon-as-component (Input=Project/Output=Projected) fits the schema model naturally; once decided, the NEXT iteration wires a running three-engine chain with a witness test that drives Signal→Nexus→Sema end to end (closing 1030). Until the shape is decided, emitting the engine types is acceptable groundwork, but it shouldn't be called a working runtime — only a working datatype pipeline.

## The fix sequencing

The four divergences have a clean dependency order, and two are already in motion:

| Divergence | Fix | Status |
|---|---|---|
| D1 — collections-free caricature | implement Spirit 1034 collections; regenerate real `ClusterProposal` | **in flight** (`/41` build subagent) |
| D2 — duplicated runtime floor | shared `schema-core` floor imported via `/39` cross-crate import | mechanism proven (`/39`); needs the floor extracted |
| D3 — vestigial signal planes | types-only-module schema shape (Input/Output optional) | `/39`-flagged gap; schema-language change |
| D4 — engines emitted not driven | confirm runtime shape (1050), then wire a live three-engine chain + test | gated on the psyche's runtime-shape call |

D1 is the central one and is already being closed. D2 + D3 are schema-language/emitter capability gaps (both small, both already identified in `/39`); landing them turns `/167`'s honest workarounds into the real shape. D4 is gated on the psyche's runtime-shape decision and is the next iteration after the datatypes are real.

## Bottom line

`/167` is a genuine, honest, working pipeline — it clears the anti-marketing bar (Spirit 1049) and its limits section already names D1 and D2. The divergences from intent are: it generates a **collections-free 2-node caricature** rather than Horizon's real datatypes (D1, central, already being closed by `/41`); it **duplicates the generic runtime floor per module** instead of importing a shared schema core (D2, fix = `/39` cross-crate import of a shared floor); it **forces vestigial signal planes onto pure type modules** (D3, fix = types-only-module shape); and it **emits the three-engine model without driving it** (D4, fix = confirm runtime shape then wire a live chain). None require throwing away `/167`'s work — D1/D2/D3 are capability gaps that, once closed, upgrade `/167`'s honest workarounds into the real thing; D4 is the next iteration. The single highest-leverage fix remains collections (D1) — it is the gate the psyche already proposed the syntax for (1034) and the one `/41` is implementing now.

## See also

- `/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md` — the prototype this audits.
- `/system-designer/41-horizon-schema-pipeline-concept/0-frame-and-method.md` — the parallel `/41` concept (closes D1 with real collections).
- `/system-designer/40-horizon-lojix-schema-next-port-feasibility/4-collections-and-option-gate-explained.md` — why collections (D1) is the decisive gate + the `TypeReference` fix.
- `/system-designer/39-schema-cargo-cross-crate-import/3-overview.md` — the cross-crate import (D2's fix mechanism) + the types-only-module finding (D3).
- `/system-designer/37-prototype-schema-deep-iteration-2-nexus-mail-sema-engine-2026-05-27/3-overview.md` — Decision A shared schema home (D2).
- Spirit records: 1048 (generate all Horizon datatypes), 1034 (collections syntax — D1), 1000 (schema-at-heart — D2), 1037/1038 (plane envelopes + origin route — D2/D4), 1050 (runtime shape open — D3/D4), 1030 (components must drive, not scaffold — D4), 1049 (show working, not marketing — the bar `/167` clears).
