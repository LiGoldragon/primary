# 102 — context refresh: schema as channel-contract reframing

## Frame

Per psyche record 671 (2026-05-25): *"wake up like I had a fresh
night's sleep and you just woke up all fresh and not a bunch of
staling, rotting context reports"* — this refresh sweeps the
designer/operator/skill substrate through the new lens crystallized
in records 668-670:

1. **Schemas warrant from need-to-interact** (record 668) — every
   major component or part-of-system worth describing warrants its
   own schema declaration. Schema IS the substrate for inspecting +
   interacting with that part of the system. Supersedes the
   retracted "interact trait" framing (records 660 + 665, retracted
   by 666).

2. **Contract IS Channel** (record 668) — "contract" and "channel"
   are the SAME thing. Repository contract IS a channel; wire
   contract IS a channel; storage contract IS a channel; each
   internal-actor-message-vocabulary IS a channel. **Schemas
   describe channels. Each channel-contract gets ONE schema.**

3. **Internal vs external schemas — three categories** (record 669) —
   components have TWO schema categories with three internal
   sub-shapes:
   - **EXTERNAL** schemas describe surfaces external to daemon
     runtime: **wire contracts** (signal sockets) AND **storage
     contracts** (database, files; state surviving process exit).
   - **INTERNAL** schemas describe surfaces within daemon runtime:
     **internal actor message vocabularies**, **internal channel
     contracts**.
   - Record 659's narrower "two languages (wire vs effect)" is
     REFINED to the three-category taxonomy
     (**wire / storage / internal**).

4. **Schema location follows contract** (record 670) — wire-contract
   schemas live in `signal-<component>` crate (separate repo
   because wire affects compilation across multiple components);
   storage-contract schemas live with the DAEMON;
   internal-message-channel schemas live with the DAEMON.
   **Multi-schema per crate is now allowed** — one per contract.
   Naming convention: `<crate>/<contract-name>.schema`.

The **five surviving crystallized principles** from /341 still hold
(records 656-658, 661-662). The 7-principle list now SHIFTS:
- Principle 4 (two languages) is REFINED to three categories.
- Principles 5-6 (interact-trait + interaction-actor) RETRACTED per
  record 666.
- Two new principles slot in from records 668-670 (schemas-from-need-
  to-interact, contract-IS-channel, multi-schema-per-crate).

Scope of this refresh: ~20 files read (canonical authority reports,
workspace contract files, seed skill files, aski-core verification).
Goal: surface which passages survive the new lens, which are
contradicted, which need reframing, and which seed the new
principles.

## Summary

| Bucket | Count of passages | Top files |
|---|---|---|
| Survives | ~38 | aski-core trio, ESSENCE, INTENT (intent layer), `/341` 5 surviving principles, `/344` 5-principle bumper-sticker, `/185` substrate runtime emission, `architectural-truth-tests.md`, `language-design.md`, `actor-systems.md`, `contract-repo.md` (layering + versioning) |
| Superseded | ~14 | `/342` entire body, `/341` §2.5 + §5.1 items 17-18, `/343` §5 "interact-trait" derivations (already revised but residual mentions), single-schema-per-crate implicit in `/338`, `/340`, `/184`, `/185`, `enum-contact-points.md` §3-4 |
| Needs reframing | ~22 | `component-triad.md` triad-shape (storage-schema + internal-schema sit alongside wire-schema), `contract-repo.md` ("contract repo" vs "contract IS channel"), `subscription-lifecycle.md` (kernel-grammar via `signal_channel!`), `enum-contact-points.md` examples 3-4, `actor-systems.md` (no schema framing yet), `/338` §6 (one module per `.schema` → one module per channel-schema), `/340` §3-7 (schema-codegen scope expands), `/343` §1-4 (effect-table + fan-out reframe to internal-channel schemas) |
| Freshly load-bearing | ~10 | `/341` §2.1 (schema-as-architecture), `/344` slide 1 (one declaration, multiple projections), record 659's "internal vs external" sentence in `/341` §2.4, `/185` "What I Discovered" §, `/343` §2-4 (the effect-side as internal channels), `component-triad.md` §"Vocabulary" (signal types / signal tree — extends to channel-schema), `contract-repo.md` §"Layered pattern" (multiple schemas in one crate), `/340` §3 "schema-codegen" (composer per channel) |

## What survives (top 10 sample)

1. **`/341` §2.1 — schema-as-architecture (record 656).** "The
   schema IS the architecture." Strongest under the new lens —
   the new framing reinforces this: multiple schemas, multiple
   projections, the schemas COLLECTIVELY are the architecture.

2. **`/341` §2.2 — extension semantics for headers (record 657).**
   ShortHeader as 8-byte prefix preserved inside ExtendedHeader.
   This is a wire-channel-schema property; it survives intact.

3. **`/341` §2.3 — deep tree + type index (record 658).** Type
   index naturally generalizes across multiple schemas — the
   per-schema namespace + cross-schema qualified imports already
   support this.

4. **`/341` §2.7 — actor fan-out execution (record 662).** SIMO
   shape survives; it's now a property of internal-channel
   schemas (the actor's method returns fan-out outputs).

5. **`/341` §2.6 — effect-table match-driven dispatch (record
   661).** "Match always; map always; never compute when you can
   match." Survives directly — the effect-table now lives in the
   internal-channel schema (one of the daemon-resident schemas).

6. **`/185` substrate runtime emission landed.** ExtendedHeader,
   Interact/InteractionActor traits scaffold (per retraction
   pending unwind), Effect enum + EffectTable + FanOut /
   FanOutOutput, parallel owner/sema names. The RUNTIME types
   survive; their schema-side authoring needs to reframe to
   the per-channel-schema location.

7. **`architectural-truth-tests.md` entire skill.** Witness
   discipline survives — every channel-schema gets its own
   witness tests. The skill needs cross-reference to schemas-as-
   channels but its substance is intact.

8. **`language-design.md` entire skill** (NOTA discipline,
   positional records, no keywords, position-defines-meaning).
   Independent of the schema-as-architecture layer; NOTA is the
   substrate every channel-schema renders against.

9. **`actor-systems.md` entire skill** (kameo, planes-as-actors,
   release-before-notify, no shared locks). Independent of the
   schema layer; the internal-channel schemas declare what actors
   speak about, not how they're shaped.

10. **`contract-repo.md` §"Layered pattern" + §"Versioning is the
    wire".** Layering composes naturally with multi-schema per
    crate; layered effect crates ARE per-channel-schema
    extensions. Versioning discipline survives.

## What's superseded

Passages contradicted by records 668-670. Should be marked
superseded with the standard supersession header pattern (NOT
rewritten — preserve historical framing).

| File | Section | Note |
|---|---|---|
| `/342` | entire body | Already RETRACTED in entirety per record 666; no action needed beyond verifying the retraction note remains at top |
| `/341` | §2.5 (interact-trait + interaction-actor) | Already marked RETRACTED inline; verify ordering between §2 principles after the retraction |
| `/341` | §5.1 items 17-18 (composer emit inventory) | Already struck inline; the inventory shrinks to wire-side + effect-table + fan-out items |
| `/341` | §5.2 (new skill files) entries `interact-trait.md` + `interaction-actor.md` | These skills should NOT be written; the row should be retracted from the §5.2 table |
| `/343` | §5 (operations-to-actor-methods note about no derived trait) | Already revised post-666; verify the residual `<Operation>Interact` trait references in §1, §4, §7 also drop |
| `/338` | §6 ("emission") | "ONE Rust module per `.schema` file" assumes single-schema-per-crate; superseded by record 670 (multi-schema per crate, naming `<crate>/<contract>.schema`) — needs supersession header |
| `/340` | §3 (correct architecture) | "spirit.schema generates module `spirit`" — under the new framing this becomes `signal-persona-spirit/spirit.schema` (wire) plus `persona-spirit/spirit-storage.schema` (storage) plus `persona-spirit/spirit-recorder.schema` etc. Single-module assumption superseded. |
| `/340` | §4 ("what schema-codegen emits, top-down") | Top-down emission lists 15 items for ONE schema; under multi-schema the composer runs per-schema. Needs supersession note. |
| `/184` | §"Correct Replacement Shape" + §"Structured Composer Model" | Single `RustComposer` walking ONE `AssembledSchema` → ONE module is superseded; need composer-per-channel-schema. Mark with header. |
| `/185` | §"Generated Shape" + §"What Landed" | Effect enum + EffectTable + FanOut generated INSIDE the wire-schema crate's output module; under new framing these belong to a DAEMON-side internal-channel schema, not the signal-* wire crate. Generated shape correct in spirit; location wrong. |
| `enum-contact-points.md` | §3 "SchemaMacro<Input> over BuiltinMacroVariant" example | Refers to `schema/src/engine.rs:7-44`. The structural shape SURVIVES; the framing "the schema engine has one canonical BuiltinMacroVariant" needs to flex to per-channel macro indexing (each schema can declare its own macros). |
| `enum-contact-points.md` | §4 "signal_channel! macro emits the Dispatch trait" | Heading + `signal-frame/macros/src/emit.rs:389-472` references already flagged P1 by `/101` heresy inventory; the example survives if reframed to "schema-rust emits the Dispatch trait per channel-schema". |
| Workspace AGENTS.md | "Hard overrides" "Component triad means daemon + working signal + policy signal" | The component-triad sentence implies the triad is the canonical multi-repo shape. Per record 668, the triad's two signal repos are STILL channels; but the daemon ALSO holds additional channel-schemas (storage + internal). The hard override needs a small extension to acknowledge that triad's 3 repos do not exhaust the schema count. (Direction not retraction.) |
| `/341` | §6 "the synthesized architecture" mermaid | The diagram shows ONE schema layer feeding TWO emission paths. Under the new framing the schema layer is MULTIPLE schemas (wire + storage + internal-N), each with its own emission. Diagram needs supersession or update. |

## What needs reframing

Substance survives; framing assumes single-schema-per-component or
"two languages (wire vs effect)" or "interact trait" or
"single-`.schema`-file" — needs follow-on edit by designer.

| File | Section | Reframing note |
|---|---|---|
| `component-triad.md` | §"The shape" (top-of-skill triad diagram) | The diagram shows two `signal-*` repos as the schema-bearing surfaces. Under record 670, the DAEMON also carries storage-channel + internal-channel schemas; the triad shape extends: 3 repos with N schemas where wire-schemas live in `signal-*` and storage + internal schemas live alongside the daemon. |
| `component-triad.md` | §"Vocabulary" — signal types, signal tree | The vocabulary survives but adopts new entries: "channel" (= contract = schema substrate), "channel-schema" (the .schema file describing a channel), "external channel" vs "internal channel". |
| `component-triad.md` | §1 invariant ("CLI has exactly one Signal peer") | Survives; "Signal peer" is more precisely "wire-channel peer" (the one signal-* contract the CLI speaks). |
| `component-triad.md` | §3 invariant ("verbs come in three layers") | The three layers (Contract Operation / Component Command / Sema Operation) now correspond more precisely to (external wire channel / internal channel / sema cross-channel classifier). The semantic still holds; the framing tightens. |
| `component-triad.md` | §5 invariant ("policy state + working state in ONE redb") | Under record 670, the daemon's redb IS a storage-channel-schema-described surface. The "one redb per component" rule becomes "one storage-channel per component, schema-described". Multiple internal sub-channels still allowed; the storage channel is ONE schema covering both policy + working tables. |
| `contract-repo.md` | §"What goes in a contract repo" | The file list (`request.rs`, `reply.rs`, etc.) assumes the contract is the wire channel only. Under record 670, multi-schema per crate is allowed — a contract crate can hold the wire schema AND additional schemas (e.g. introspection extension). Skill needs to acknowledge `<crate>/<contract-name>.schema` as the per-channel-schema naming. |
| `contract-repo.md` | §"Contracts name a component's wire surface" | "One component's wire surface" assumes single-wire-schema-per-component. Under record 670, a component may have multiple wire-channel-schemas (e.g. ordinary + owner + introspection). The skill needs to acknowledge multi-wire-schema-per-component. |
| `contract-repo.md` | §"Kernel extraction trigger" | Extraction trigger still valid; the kernel IS a separate channel-schema (the frame envelope channel). The skill framing fits naturally; just needs the "kernel as channel-schema" cross-reference. |
| `subscription-lifecycle.md` | §"The kernel grammar enforces it" | References `signal-core/macros/src/validate.rs:303-331`. Already flagged in `/101` heresy inventory as needing rewrite. Under new framing: the close-is-Retract enforcement IS a schema property (the `stream` block of the wire-channel-schema declares `close Retract<token>`). Reframe to `<crate>/<contract>.schema` `stream` block + `schema-rust` enforcement. |
| `subscription-lifecycle.md` | §"The grammar shape" (code block illustrating signal_channel! { ... }) | Already flagged by `/101`. Reframe to NOTA `.schema` shape with positional records — `(Subscribe (...) (opens ...))`, `(Retract (...) (closes ...))`, etc. |
| `subscription-lifecycle.md` | §"The producer's three-actor shape" | The three actors (SubscriptionManager / StreamingReplyHandler / DeltaPublisher) are an INTERNAL channel topology. Under record 669, the daemon could carry an internal-channel schema describing these actor message vocabularies. Skill could acknowledge this is the seed of an internal-channel schema. |
| `enum-contact-points.md` | §3 SchemaMacro example | Survives if reframed: "SchemaMacro<Input> works per-channel-schema" — every channel-schema has its own macro pipeline; the example shows one pipeline per schema. |
| `enum-contact-points.md` | §4 "signal_channel! macro emits the Dispatch trait" | Already flagged by `/101`. Reframe to: `schema-rust` composer emits the Dispatch trait FROM the wire-channel-schema. The pattern of "macro emits one Dispatch trait per channel" generalizes. |
| `actor-systems.md` | §"Actor per plane" + §"Runtime roots are actors" | Survives as-is; under the new framing, internal-channel-schemas describe what the actor's messages look like. The skill could acknowledge this is the substrate the daemon's actor messages live against. |
| `actor-systems.md` | §"Traces are required" | Trace events (actor started / message received / commit completed) ARE the internal channel's vocabulary. Trace IS a channel. Acknowledge cross-reference. |
| `/338` | §6.1 module-per-schema output | Reframe: "one module per channel-schema; multi-schema per crate produces multiple modules in one crate, by `<contract-name>` per module". |
| `/338` | §"the next operator slices" #2 (`schema-rust` composer) | Reframe to clarify composer runs per-schema; the composer library handles N channel-schemas per crate. |
| `/340` | §3-7 (entire correct architecture section) | The mermaid diagram + emission inventory needs to reflect multi-schema. One `emit_schema!` invocation emits ONE channel-schema's projection; a crate with multiple schemas has multiple invocations or a directory-style auto-discovery. |
| `/343` | §1-4 (effect-table + fan-out as feature variants) | Effect-table + fan-out are NOT new feature variants on the wire-channel-schema. They are the SUBJECT of a separate internal-channel-schema (the effect-channel). The two-schema split (wire-schema + effect-channel-schema) materializes here. Major reframing — this is the load-bearing change in /343. |
| `/343` | §6 (worked example of spirit.schema after extension) | The worked example puts `(EffectTable [...])` and `(FanOutTargets [...])` INSIDE the wire schema's features. Under new framing they go in a SEPARATE `.schema` file (e.g. `persona-spirit/spirit-recorder.schema` for the recorder actor's internal channel). |
| `/185` | §"What I Discovered" | Already gets this RIGHT in spirit: "the next durable step is in the schema crate, not in `signal-frame`: add a schema feature or declaration family for authored effect tables". Now the answer is: a separate `.schema` file, located with the DAEMON. The schema crate's support for multi-schema-per-crate is the prerequisite. |
| `/184` | §"Migration Plan" #8 ("Delete ChannelSpec...") | Survives; ChannelSpec deletion is unrelated to multi-schema. |
| `enum-contact-points.md` | §"What this means for engine design" | Engine logic reads one outer `match operation` per handler — survives. The "operation" enum comes from one channel-schema; under multi-schema each channel has its own `Operation` enum (often differently named to avoid clash: `WireOperation`, `RecorderOperation`, etc.). |

## What's freshly load-bearing

Passages that seed the new principles 668-670 and should be
cross-referenced in the upcoming /345 synthesis.

| File | Section | New principle it seeds |
|---|---|---|
| `/341` §2.1 (record 656 schema-as-architecture) | Crystallized statement | Direct seed for record 668's "schemas warrant from need-to-interact". The architecture-as-schema framing IS the parent claim. |
| `/341` §2.4 (record 659 two languages) | Newly named: "wire vocabulary" + "effect vocabulary" | Seed for record 669's three-category refinement; the two-language framing is the PARENT to the three-category split. |
| `/344` Slide 1 + Slide 11 (5-principle bumper sticker) | Schema is the architecture; many projections | Direct cross-reference for record 668. |
| `/185` §"What I Discovered" | "the next durable step is in the schema crate, not in `signal-frame`: add a schema feature or declaration family for authored effect tables" | Direct seed for record 670: the effect schema lives WITH THE DAEMON (not in signal-frame, not in signal-* wire crate). The implementation pressure of /185 surfaced the location question that 670 answers. |
| `/343` §1-4 (the entire effect-table + fan-out design) | "Authored, not route-derived" | Pressure that surfaced the question: where do effect-side schemas LIVE? Answer: with the daemon. Seed for 670. |
| `component-triad.md` §"Vocabulary" | "signal types" + "signal tree" definitions | Seed for the channel-schema vocabulary expansion. Naturally extends to "channel types" + "channel tree". |
| `contract-repo.md` §"Layered pattern" | signal-forge over signal | Seed for multi-schema per crate: the layered effect crate is ALREADY a per-channel-schema separation. Generalizes. |
| `/340` §3 ("the right architecture" mermaid) | New `schema-codegen` crate consumes `AssembledSchema` directly | Seed for the composer-per-channel-schema model: the schema-codegen crate handles N channels uniformly. |
| `architectural-truth-tests.md` §"Constraints first" | Each constraint gets a witness test | Direct cross-reference: each channel-schema declares its own constraints + witnesses. The channel IS the unit of architectural truth testing. |
| `language-design.md` §0 "NOTA is the only text syntax" | NOTA as the substrate every channel-schema renders against | Direct cross-reference: every channel-schema renders to NOTA. The schemas describe channels; NOTA is the syntax in which schemas are written. |

## Refresh observations

1. **The single-schema-per-crate assumption runs through ~12
   files.** It's mostly implicit, not stated. `/338`, `/340`, `/184`,
   `/185`, `/343`, `/344`, the seed skills `component-triad.md` and
   `contract-repo.md`, the heresy inventory `/101`, `enum-contact-
   points.md` — all assume one `.schema` per crate. Lifting this
   assumption is the load-bearing change; the convention rename
   `<crate>/<contract-name>.schema` is the mechanical part.

2. **The "two-languages" framing appears K=6 times across the
   recent designer reports + `/185` operator report.** Each
   occurrence needs a refinement note (NOT supersession) — the
   two-categories framing is the PARENT, three-category
   (wire/storage/internal) is the REFINEMENT. The framing is not
   wrong; it's narrower than the new shape.

3. **The retraction story is well-handled in `/341` + `/342` +
   `/344`.** `/342` is RETRACTED top-to-bottom; `/341` §2.5 carries
   the inline retraction; `/344` Slide 7 narrates the retraction
   gracefully. The remaining cleanup is the `/343` residual
   references to `<Operation>Interact` trait in §1, §4, §7 (the
   header section + the worked example + the implementation
   plan) — `/343` §5 already revised but the earlier sections
   carry traces.

4. **The triad story has a small but real friction.** The triad
   (daemon + working signal + policy signal) is NOT contradicted
   by the new framing — both signal-* repos remain channel-
   schemas. But the triad emphasizes the wire-channel-schemas as
   the primary substrate. Under records 669-670, the daemon
   carries additional channel-schemas (storage + internal-N) and
   the triad shape extends without being broken. The `component-
   triad.md` skill needs a small additive section — not a
   replacement — acknowledging that triad's 3 repos do not
   exhaust the schema count for a stateful component.

5. **`/185`'s "What I Discovered" passage is the load-bearing
   pivot.** That single paragraph — "the next durable step is in
   the schema crate, not in `signal-frame`" — surfaces the
   location question. Records 670 answers it: schemas LIVE WITH
   the daemon for storage + internal-channel cases. This is the
   single highest-leverage cross-reference for the /345
   synthesis.

6. **NOTA-side discipline is independent of the schema-as-
   channel reframing.** `language-design.md`, `nota-design.md`,
   `architectural-truth-tests.md`, `actor-systems.md`,
   `naming.md` — none of these need substantive changes. Their
   substance applies uniformly across all channel-schemas. The
   schema-as-channel reframing is purely about HOW schemas are
   organized + located, not about the NOTA syntax or the engine
   logic or the testing discipline.

7. **The `/101` heresy inventory is still valid.** The 125-130
   flagged passages (P1 + P2 + P3 + P4) remain correct flags
   under the new framing. P4 ("two languages") now needs
   downgrading: the flag is correct that the framing is
   incomplete, but the FIX is refinement (three categories), not
   replacement. P1 + P2 + P3 are unchanged. The heresy sweep can
   still execute as previously planned; the /345 synthesis just
   adds a sentence about the three-category refinement.

8. **AGENTS.md hard override "Component triad means..." needs a
   one-sentence extension.** Under the new framing, the triad's
   3 repos carry the wire-channel schemas; the daemon carries
   additional storage + internal-channel schemas. The hard
   override survives but should mention the broader schema count
   in a single subordinate clause.

9. **The aski-core verification confirms the lineage.** The
   `core/*.core` files (body, domain, expr, module, origin,
   param, pattern, primitive, program, statement, trait, type)
   ARE per-domain schema declarations — one schema per part of
   the language. This is the structural ancestor of "schemas
   warrant from need-to-interact" (record 668). The askic ↔
   veric ↔ semac triad is the structural ancestor of "contract
   IS channel" (record 668) — each leg IS a channel-schema
   describing one part of the system. The connection is direct;
   the workspace-side framing is the second iteration of a
   pattern that already lived in aski.

10. **Multi-schema-per-crate has zero implementation friction —
    it's a convention rename + a parser path.** `schema-rust`
    already operates on `AssembledSchema`; the change is to load
    multiple `.schema` files per crate by convention
    (`<crate>/<contract-name>.schema`) and emit one module per
    file. The schema crate's `LoadedSchema::read_path` already
    takes a path; the composer just runs per-schema. No
    architectural barrier; the change is mostly nomenclature +
    a convention for the proc-macro entry to discover all
    `.schema` files in a crate.

## Recommended next-action sequence

For the designer's /345 synthesis + downstream work, the priority
order:

1. **Write `/345 — schema as channel-contract` synthesis** —
   THE load-bearing report. Naming the 7 → (5 + 2 + retraction)
   shift, the three-category refinement (wire / storage /
   internal), the multi-schema-per-crate convention, the
   `<crate>/<contract-name>.schema` naming. This is the
   canonical authority for everything downstream.

2. **Update `/341` §2.4 + §6 to cross-reference /345** — the
   two-languages framing in `/341` needs an inline note pointing
   forward to `/345`. Not a rewrite; a forward-reference. The
   §6 mermaid needs a supersession note pointing at the new
   architecture.

3. **Add the AGENTS.md hard-override extension** — one
   sentence extending "Component triad..." to acknowledge daemon-
   side schemas. Tiny edit; high-leverage discipline.

4. **Update `component-triad.md` §"Vocabulary" + §"Filesystem
   shape"** — additive section naming channel-schemas
   (external wire + external storage + internal-N) with the
   `<crate>/<contract-name>.schema` convention. NOT a rewrite —
   triad survives with a layered shape underneath.

5. **Update `contract-repo.md` §"What goes in a contract repo"
   + §"Naming a contract repo"** — multi-schema per crate;
   `<crate>/<contract-name>.schema` naming; layered-effect-crate
   IS a separate channel-schema (already structurally true,
   just name it).

6. **Update `subscription-lifecycle.md` §"The kernel grammar
   enforces it" + §"The grammar shape"** — reframe to the NOTA
   `.schema` shape + `schema-rust` enforcement. Already flagged
   by `/101`; the /345 lens makes the rewrite cleaner because
   subscriptions ARE wire-channel-schema concerns.

7. **Operator slice: extend schema crate to load multiple
   `.schema` files per crate** — convention discovery
   (`<crate>/*.schema` or `<crate>/schemas/*.schema`); `emit_schema!`
   accepts a path or runs per discovered file; `schema-rust`
   composer runs per-schema. This is the implementation work
   that materializes the `/345` framing.

8. **Operator slice: extract a storage-channel-schema example
   for `signal-persona-spirit`'s storage** — first concrete
   storage schema. `persona-spirit/spirit-storage.schema`
   covering the redb tables. Establishes the convention in
   production.

9. **Operator slice: extract an internal-channel-schema example
   for the spirit recorder actor** — first internal schema.
   `persona-spirit/spirit-recorder.schema`. Replaces the
   currently-route-derived effect table per `/185` Remaining
   Work + `/343`'s redirected design.

10. **Update `/343` to align with /345** — the effect-table +
    fan-out designs land in the internal-channel-schema, NOT
    the wire-channel-schema's feature variants. Either rewrite
    `/343` or supersede with `/343-v2`. Lean: supersession +
    `/343-v2` because the load-bearing direction shifts.

11. **Continue heresy sweep per `/101` as previously planned** —
    the sweep is still correct; the only adjustment is the P4
    framings get refinement notes (not replacement). Operator
    can land mechanical-sweep per repo as feature branches per
    psyche 2026-05-24's designer-on-worktree discipline.

12. **DEFER: skill files for new principles.** Don't write
    `interact-trait.md` or `interaction-actor.md` (RETRACTED).
    DO consider `channel-schema.md` or `schemas-warrant-from-
    need-to-interact.md` as a new Apex skill once `/345`
    crystallizes. Single Apex skill consolidating records
    656-662 + 668-670 may be the right shape.

## References

- Records 668-670 (the new framing — schemas warrant from need-
  to-interact; contract IS channel; three-category internal vs
  external; schema location follows contract; multi-schema per
  crate)
- Record 671 (the refresh prompt — wake up like fresh sleep)
- Records 656-666 (the seven crystallized principles + the
  interact-trait retraction)
- `/338` — refreshed schema engine vision (pre-new-framing)
- `/340` — schema emission no-legacy review
- `/341` — schema crystallization synthesis
- `/342` — interact-trait code walkthrough (RETRACTED in
  entirety)
- `/343` — schema syntax for the effect side (post-666 revised
  but pre-670 single-schema assumed)
- `/344` — the design explained back (12-slide presentation)
- `/184` — schema macro old-emitter audit
- `/185` — schema crystallization implementation
- `/101` — heresy inventory (still valid; P4 needs refinement
  framing)
- `/git/github.com/LiGoldragon/aski-core/core/*.core` —
  structural ancestor: one schema per language part
- `/git/github.com/LiGoldragon/aski-core/Cargo.toml` description
  "aski-core — rkyv contract types for askic↔veric↔semac (parse
  tree types)" — direct lineage to the contract-IS-channel
  framing
- `ESSENCE.md` (workspace) — intent layer authority + naming
  rule
- `AGENTS.md` (workspace) — component-triad hard override
  needing minor extension
- `INTENT.md` (workspace) — workspace prose synthesis
- Seed skills (read in this refresh):
  `skills/component-triad.md`,
  `skills/enum-contact-points.md`,
  `skills/contract-repo.md`,
  `skills/actor-systems.md`,
  `skills/subscription-lifecycle.md`,
  `skills/language-design.md`,
  `skills/architectural-truth-tests.md`,
  `skills/skills.nota`
