# 561 — rewrite shortlist: foundational kernels to re-record (psyche approval)

designer, 2026-06-08. Recovered from the crashed `w8du7wvq4` rewrite run (8 of 9 agents completed; pulled from the journal, zero re-spend). These are the foundational durable kernels the 560 cleanup swept (mostly from the borderline set), reworded timeless. **Nothing is recorded until you approve.** Each is shown in ready-to-record form; on your nod I run them. Drop any you don't want; edit any wording.

**70 proposed records** across 10 themes (1 dropped as live-covered). Source record in parentheses; all sources are confirmed removed from the live store.

## Schema as the single source of truth & emission (13)

- from `ug6i` — *A contract's schema is the single source of truth; its Rust is always regenerated from the schema, with no step beyond regeneration.*
  ```
  spirit "(Record ([schema generated-artifacts single-source-of-truth contract] Principle [The generated Rust of a contract is always regenerated from its schema. The schema is the single source of truth, and the only step is regenerating the Rust from it — there is no ceremony beyond regeneration. Checked-in generated artifacts must be byte-identical to current generator output; a per-crate freshness gate that asserts this holds fleet-wide, so generated code can never diverge from the schema it claims to mirror.] VeryHigh Zero))"
  ```
- from `fz9n` — *The schema is itself a typed rkyv-serializable value; Rust is regenerated from it by canonical round-trip, with no public intermediate representation.*
  ```
  spirit "(Record ([schema rust-emission rkyv canonical-round-trip] Decision [Schema-in-Rust is the rkyv-serializable typed schema value. Equivalence is established by canonical round-trip, not byte-identical source preservation. No public schema-resolution intermediate representation is exposed, and Rust emission lowers from high-level schema-datatype methods.] High Zero))"
  ```
- from `1xjh` — *Schema-derived Rust emits in-tree under src/schema/ alongside hand-written code, not into the build output directory.*
  ```
  spirit "(Record ([schema rust-emission in-tree visibility] Decision [Code derived from a schema is emitted into the crate source tree (src/schema/lib.rs and src/schema/<module>.rs), living beside hand-written Rust so humans and tools can read and grep it without a rebuild. It is regenerated content keyed to schema-file edits; the build-output directory is not where it belongs.] High Zero))"
  ```
- from `o7a3` — *Runtime code emission lowers through typed tokens, not hand-formatted source strings.*
  ```
  spirit "(Record ([schema rust-emission typed-tokens] Constraint [Schema-driven runtime code emission produces Rust by lowering into typed token trees rather than concatenating hand-formatted source strings. Hand-formatted string emission is not an acceptable target shape for generated runtime code.] High Zero))"
  ```
- from `0bw0` — *Schema codegen lowers through typed/token construction, never string-formatted source.*
  ```
  spirit "(Record ([codegen schema rust-lowering] Principle [Code generated from schema is produced by Rust-native typed/token lowering — constructing the target syntax structurally — rather than by formatting strings into source text. String-concatenation codegen is not an accepted shape for the emitter; the typed lowering path is the intended design.] High Zero))"
  ```
- from `e6v5` — *The schema-to-Rust generator is built on a rust-native code-generation approach, not ad-hoc build-time string emission.*
  ```
  spirit "(Record ([schema-codegen rust-native code-generation] Decision [Generating Rust from a schema is done with a rust-native code-generation approach (constructing typed tokens), not by formatting strings line by line at build time. Ad-hoc string-emission codegen is not the intended shape of the generator; the engine stack is built properly on the rust-native approach.] High Zero))"
  ```
- from `kuw2` — *Rust is emitted through a structured item/impl/match token model where the writer owns indentation, not through hand-formatted strings.*
  ```
  spirit "(Record ([schema rust emission code-writer] Decision [Schema-to-Rust emission uses a structured model of Rust items, impl blocks, and match tokens, with the writer owning indentation depth. Emission flows through these typed constructs rather than through hand-counted formatted strings of implementation code.] Medium Zero))"
  ```
- from `g1wb` — *Rust source emission is a distinct stage from macro consumption: the stack emits Rust first, and macros are a later, separate consumption surface.*
  ```
  spirit "(Record ([schema rust-emission macros layering] Decision [Generating Rust source from a schema and consuming a schema through macros are separate layers. The stack produces Rust code as its own step; macros are a later or separate surface, not the same operation as source emission.] High Zero))"
  ```
- from `gh29` — *The schema emitter automatically wraps recursive enum variants in Box so generated types compile without hand intervention.*
  ```
  spirit "(Record ([schema-emission recursive-variants box] Decision [When an enum variant's payload type is the same as or recursive on the enclosing type, the emitter wraps it as Box rather than emitting the bare type, avoiding the unsized-type compile failure that every schema author would otherwise hit by hand.] High Zero))"
  ```
- from `gb95` — *Emitted per-construct support code is gated to what the target actually emits; signal-frame support is generated only for signal-emitting targets.*
  ```
  spirit "(Record ([schema-emission plane-gating signal-frame] Principle [Construct-specific support code from the emitter is gated by the target's actual capabilities, not generated unconditionally. Signal-frame support is gated by whether the target emits signals, so Nexus-only, SEMA-only, and wire-contract targets do not receive signal-frame code.] High Zero))"
  ```
- from `m5po` — *Schema lowering is a real macro registry with macro dispatch, not hard-coded special cases.*
  ```
  spirit "(Record ([schema macro-registry lowering] Decision [Schema lowering is driven by a real macro registry and macro-dispatch design rather than hard-coded lowering of known cases. Schema macros are looked up and dispatched, so the macro system is a genuine extensible mechanism exercised by the working CLI and daemon targets.] High Zero))"
  ```
- from `pe2d` — *Schema-driven emission covers type declarations completely, but byte-level recognition (lexing) cannot be emitted without a separate sub-language for declaring lexer states and disambiguation rules.*
  ```
  spirit "(Record ([schema-emission code-generation lexer] Constraint [The reach of schema-driven code emission has a structural boundary. Type declarations emit cleanly and completely from the schema. Byte-recognition policy — the lexer and walker that turn raw bytes into tokens — cannot be derived from a type schema alone; it requires its own sub-language for declaring lexer states and disambiguation rules. The principle: schema emission is sound for declarative type structure and stops at byte-level recognition, which is a distinct concern needing its own declarative surface.] Medium Zero))"
  ```
- from `hwsk` — *Spirit's signal, owner, and signal-to-sema languages are each defined as schema files that expand through schema macros into Rust.*
  ```
  spirit "(Record ([spirit schema signal sema] Decision [Spirit follows the full-schema approach: its ordinary peer-signal language, owner-signal language, and the signal-to-sema lowering language are all defined as schema files. Those schemas expand through schema macros into an assembled schema and then into Rust, so Spirit's contracts are generated rather than hand-written.] High Zero))"
  ```

## Schema language shape & parsing layers (12)

- from `k2eg` — *A schema file is a top-level sequence of type declarations, not itself wrapped in an enclosing struct.*
  ```
  spirit "(Record ([schema-language schema-shape] Clarification [A schema file has no outer struct wrapper. It is a flat top-level sequence of type declarations; the file is a namespace of definitions, not a single struct value. This complements the everything-is-struct rule for the payloads while keeping the file itself a declaration list rather than a wrapped record.] High Zero))"
  ```
- from `mnl1` — *A schema file is legal raw NOTA: its core roots are known from the filename, and its datatype maps are native brace key-value maps of raw NOTA datatype objects prior to lowering.*
  ```
  spirit "(Record ([schema nota raw-nota-first datatype-map] Clarification [Schema files are raw-NOTA-first. A .schema file is itself legal NOTA; its core schema roots are identified by the filename rather than by in-file labels, and its datatype declarations are native brace key-value maps of raw NOTA datatype objects, interpreted only when the separate lowering layer runs.] High Zero))"
  ```
- from `y0nj` — *A schema is two parts — a namespace of named type definitions and a root entry-point type — with delimiters carrying structural meaning so no keywords are needed.*
  ```
  spirit "(Record ([schema syntax namespace root] Clarification [A plain schema has two parts: the namespace (the type vocabulary — a map of name to definition) and the root (the entry-point type, itself a struct, where a struct is a sequence of fields). The aim is the shortest unambiguous syntax for data specification, with delimiters carrying the structural meaning so the form needs no keywords.] Medium Zero))"
  ```
- from `7o63` — *The schema grammar reads files against a known root type: roots are positional, data-carrying variants use a star suffix, and macros are at-sign heads.*
  ```
  spirit "(Record ([schema-grammar nota schema-language] Clarification [Schema files are read against a known root type, so explicit Input/Output root labels disappear and a base schema is just a namespace. A reactive schema root is positional: input enum body, then output enum body, then namespace. A same-name data-carrying variant is sugared with a star suffix (Record* lowering to (Record Record)). Macro invocations are at-sign heads such as (@Vec (Topic)), (@Option (Topic)), (@KeyValue (Topic Entry)); unsigiled Vec/Option/KeyValue forms are not part of the grammar. Brace namespaces are key/value style rather than a parenthesized declaration list.] VeryHigh Zero))"
  ```
- from `2xb8` — *Schema parsing is structured as passes over NOTA object forms that produce the assembled schema.*
  ```
  spirit "(Record ([schema parsing nota assembled-schema] Correction [Parsing a schema is organized as passes over NOTA-delimited object forms whose product is the assembled schema, rather than an ad-hoc character-level parser. The NOTA object structure is the unit the passes operate on.] High Zero))"
  ```
- from `ite1` — *Schema parsing has an object-block pass that breaks NOTA text into delimiter-bounded blocks with source locations before any schema-macro lowering.*
  ```
  spirit "(Record ([schema nota parser object-block] Principle [Schema parsing begins with an object-block pass that divides NOTA text into delimiter-bounded blocks carrying their source spans, before schema-macro lowering. A block exposes its delimiter kind, source span, root-object count, and recursive child-shape predicates, so lowering works against structured blocks with location information rather than against raw text.] High Zero))"
  ```
- from `n3k6` — *Three separated layers: NOTA object parsing is delimiter-first, schema interpretation is a distinct lowering layer above it, and Rust reading code is emitted from the assembled schema.*
  ```
  spirit "(Record ([nota schema layering code-emission] Principle [The schema pipeline is three cleanly separated layers. NOTA object parsing is delimiter-first and structural, knowing nothing of schema meaning. Schema interpretation is a separate lowering layer above the parse. Rust reading code is emitted from the resulting assembled schema, not produced from legacy signal-macro text.] High Zero))"
  ```
- from `7mgq` — *Schema macros are recognized structurally, by recursive shape predicates over their object blocks, not by keyword.*
  ```
  spirit "(Record ([schema macro nota shape-dispatch] Principle [A schema macro form is identified by the recursive shape of its object blocks — for example, a form holding two root objects whose second is a bracket block or a qualifying symbol — rather than by a reserved keyword. Recognition dispatches on head symbol and structural shape, which keeps the schema language extensible by adding new shape predicates.] High Zero))"
  ```
- from `vuy5` — *A self-describing schema rests on a minimal built-in core schema that defines just the macro positions and shapes needed to read richer schemas.*
  ```
  spirit "(Record ([schema self-description bootstrap core-schema] Clarification [Before a schema can fully describe itself, it rests on a minimal built-in core schema — distinct from the full communication schema — that defines only the macro positions and shapes needed to read richer schemas. A node still in macro shape lowers through the built-in macro path; a node already in assembled-schema shape is read as assembled schema. This is the bootstrap layer beneath full self-description.] Low Zero))"
  ```
- from `h2rv` — *NOTA's name-value map form is written with curly braces, distinct from the positional record form.*
  ```
  spirit "(Record ([nota map-form notation] Clarification [Alongside the positional record form written with parentheses, NOTA carries a name-value map notation written with curly braces. The curly-brace map is the canonical surface for keyed name-value associations; records remain positional.] High Zero))"
  ```
- from `lkp7` — *Schema and NOTA syntax is strictly the current canonical form — positional roots, brace key-value declarations, homogeneous enum vectors — with no legacy keyed, piped, or labeled-wrapper forms.*
  ```
  spirit "(Record ([schema nota syntax canonical-form] Constraint [The schema and NOTA syntax is exactly the current canonical form: positional roots, strict brace key-value declarations, and homogeneous enum vectors. Labeled root wrappers, keyed declaration sigils, and pipe declaration forms are not part of the language. There is one syntax, followed directly, with no alternate or legacy path preserved alongside it.] High Zero))"
  ```
- from `8mdt` — *When an authored closed-sum enum grows past roughly ten variants, the emitter splits it into sub-enums grouped by semantic kinship.*
  ```
  spirit "(Record ([schema-emission enum closed-sum rkyv] Decision [The schema emitter does not ship a single flat closed-sum enum once it exceeds a rule-of-thumb of about ten variants. Beyond that threshold it sub-divides the closed sum into nested sub-enums grouped by semantic kinship. The motivation is both rkyv match-table size and authoring ergonomics; the ten-variant figure is a heuristic, not a hard boundary.] High Zero))"
  ```

## The shared runtime triad engine (Signal / Nexus / SEMA) (8)

- from `ocu7` — *Every component runs on one shared schema-derived runtime engine expressed as the Signal, Nexus, and SEMA traits, not a hand-rolled per-component runtime.*
  ```
  spirit "(Record ([component-runtime triad-engine schema-derived] Decision [The component runtime is a single schema-derived engine that every component inhabits: a generated daemon module plus the Signal, Nexus, and SEMA engine traits. Components supply their typed behaviour against these traits rather than each carrying its own bespoke runtime substrate, so the runtime shape is uniform and emitted from the schema rather than hand-authored per component.] High Zero))"
  ```
- from `7ca4` — *Every schema-derived daemon plugs component-specific logic into shared Signal, Nexus, and SEMA runner objects rather than re-implementing daemon boilerplate.*
  ```
  spirit "(Record ([triad runtime schema-derived daemon] Decision [The daemon runtime — Signal handling, Nexus routing, and SEMA state — lives once in a generic runner shared across components. A component supplies only its own logic and plugs it into that runner; the repetitive daemon scaffolding is not hand-written per component.] High Zero))"
  ```
- from `b7mp` — *The runtime triad exposes three engine traits — a Signal engine that triages and replies, a Nexus engine that executes, and a Sema engine that applies writes separately from observing reads.*
  ```
  spirit "(Record ([runtime-triad engine-traits signal nexus sema] Decision [Each plane of the runtime triad is expressed as an engine trait. The Signal engine triages an incoming signal and produces its reply form; the Nexus engine executes work; the Sema engine splits apply (committing writes) from observe (serving reads) so reads can proceed in parallel with writes. This engine-trait shape is the workspace-level discipline for the runtime triad.] High Zero))"
  ```
- from `v1ne` — *Schema owns component meaning; reusable byte-level and process-edge mechanics live in a shared triad runtime.*
  ```
  spirit "(Record ([schema triad-runtime separation-of-concerns component-shape] Principle [Responsibility divides cleanly: the schema is responsible for what a component MEANS — its types and contract — while reusable mechanics at the byte and process edge (length-prefixed framing, typed component arguments, runtime error types) belong in a shared triad runtime rather than being re-derived per component. Component meaning stays schema-defined; the plumbing that every component shares stays in one runtime.] High Zero))"
  ```
- from `hehp` — *Request execution is a Nexus responsibility; there is no separate executor layer that components depend on.*
  ```
  spirit "(Record ([nexus execution component-dependency] Correction [Components run request execution through Nexus, not through a standalone executor layer. No component daemon depends on a separate signal-executor; any such dependency is drift, and execution belongs to Nexus.] High Zero))"
  ```
- from `latq` — *The two-socket dual-listener triad daemon is a single shared construct: it binds a peer-callable socket and an owner meta socket, tags each arrival into the schema's signal-input union, and routes through the generated engine.*
  ```
  spirit "(Record ([triad-runtime daemon dual-listener two-socket] Decision [Every triad component shares one dual-listener daemon construct rather than reimplementing socket handling. It binds the ordinary peer-callable socket and the owner meta socket, tags each arrival into the shared signal-input union the nexus schema declares, and routes through the generated nexus engine's recursive runner. The two-socket shape is built once and reused, never worked around per component.] High Zero))"
  ```
- from `lnhj` — *The daemon skeleton is schema-emitted source-visible code; a component hand-writes only its escape hatches, and even publish/subscribe wiring is generated from schema-declared streams.*
  ```
  spirit "(Record ([triad daemon code-emission streaming] Decision [Each component's daemon is an emitted, source-visible module generated by the schema-to-Rust path, not a literal macro. The emitter produces the uniform skeleton: the entry point, argv-to-configuration decoding, listener bind/serve, and the decode-execute-encode handling spine with per-tier dispatch. The component hand-writes only its escape hatches — runtime construction of its store and engine, and its configuration, engine, error, and process-name declarations — plus a schema-side declaration of process name, listener tiers, and socket modes. Streaming follows the same rule: the daemon-side publish/subscribe wiring is emitted from the schema's declared streams, so a component merely declares a stream rather than hand-writing a subscription hub.] High Zero))"
  ```
- from `g3ax` — *The emitted daemon spine threads per-connection peer-credential context into the working-input handler so components can mint origin tags from peer credentials.*
  ```
  spirit "(Record ([daemon-spine peer-credential connection-context origin] Constraint [The generated component daemon spine must capture per-connection context — peer credentials from SO_PEERCRED — and pass it to the working-input hook. Components that mint message-origin tags from peer credentials depend on this; a spine that discards the connection and forwards only the decoded input collapses origin to a constant Owner tag and is wrong.] High Zero))"
  ```

## Request path & NOTA/rkyv boundary (7)

- from `r33n` — *The request path is NOTA at the human-facing CLI boundary and binary rkyv between components on the wire; the engine matches a typed Input to an Action and produces a typed SEMA reaction.*
  ```
  spirit "(Record ([request-path nota-rkyv-boundary engine sema] Principle [The component request path has a fixed shape. NOTA is the surface language at the human-facing CLI boundary (argv in, stdout out); between components the wire carries binary rkyv only. The runtime engine matches an incoming typed Input against the contract to select an Action, and the result is a typed SEMA reaction object. This fixes where the pretty NOTA boundary sits (the CLI) versus the raw binary boundary (inter-component wire), and names the Input-to-Action-to-reaction engine core.] High Zero))"
  ```
- from `wuvc` — *The Signal actor validates a message before pushing it to Nexus, and lifecycle events along the push path are hookable for multi-observer fanout.*
  ```
  spirit "(Record ([signal-actor nexus validation lifecycle-events actor-systems] Decision [A Signal actor validates (and may pre-process) an incoming message before pushing it to the Nexus engine; pushing means sending the typed object on to its next logical destination — Signal to Nexus, Nexus to SEMA, SEMA a reply back. Lifecycle events on this path (a sent event at the Signal-to-Nexus moment, a processed event later) are hookable: observers attach to the typed event and react — for UI, introspection, or subscription — with multiple observers fanning out from a single event.] High Zero))"
  ```
- from `yzy4` — *A runtime layer pushes a validated object onward to the next layer in the flow; the Signal layer pushes to Nexus after its own checks pass.*
  ```
  spirit "(Record ([runtime-flow signal nexus push] Clarification [Push names the act of sending a typed object onward to its next logical place in the runtime flow. The Signal layer first validates an incoming message and performs Signal-layer checks; once those pass it pushes the object on to Nexus for processing. Each layer owns its own checks and hands a clean object forward, so responsibility moves with the object rather than being re-derived downstream.] High Zero))"
  ```
- from `i1bd` — *Mail through the Nexus is a data-bearing typestate: in-flight and reached mail are structurally distinct values, making processing a compile-time fact rather than a logged claim.*
  ```
  spirit "(Record ([nexus typestate mail compile-time-invariant] Clarification [The Nexus realizes mail-keeping as a data-bearing typestate rather than one struct wearing a phantom marker. In-flight mail and reached mail carry different data and are therefore distinct value types; the only constructor of the reached type consumes an in-flight value by value, threading it through the durable store. That the mail was processed becomes a compile-time fact, not a log entry. The Nexus owns the SEMA store handle and the mail ledger; the engine is a thin composer that never touches the store directly.] High Zero))"
  ```
- from `def2` — *A 64-bit short header identifies a schema and resolves to the typed schema that produced it.*
  ```
  spirit "(Record ([schema registry short-header runtime] Principle [The schema stack carries a runtime registry that, given a 64-bit short header from a wire message or a SEMA operation, returns the typed schema — signal or SEMA — that produced it. The short header is the durable identity by which a payload's schema is recovered at runtime.] Medium Zero))"
  ```
- from `2g1c` — *Signal types use tiered size encoding: a packed-tag fast tier, a bounded-summary tier, and a full structured-record tier.*
  ```
  spirit "(Record ([signal type-sizing encoding] Decision [Signal types are sized in tiers: a compact tier that packs the root variant tag plus sub-discriminators into a single machine word, a bounded summary tier held to a fixed byte budget, and a full structured-record tier. The variant tag sits at the root for generated signal types; internal data records emit a constant discriminator plus packed fields rather than being reshaped into top-level enums.] Medium Zero))"
  ```
- from `gwiv` — *A text client's emit step auto-injects the caller process id into the frame envelope as origin, in a single emission.*
  ```
  spirit "(Record ([component-shape cli frame-envelope origin] Decision [Producing a client message is one emission that yields the full binary frame and injects the caller's process id into the frame envelope, so origin is carried automatically rather than supplied separately by the caller.] Medium Zero))"
  ```

## Testing authenticity (3)

- from `fip0` — *Tests assert against typed schema-emitted values, never string-encoded state; NOTA round-trip is the canonical serializable form for assertions.*
  ```
  spirit "(Record ([testing schema-data-types no-string-encoding nota] Correction [A test that encodes observed state as strings bypasses the very type system the design relies on and is not a real test. Observer state and assertions must hold typed schema-emitted data and compare typed values directly; where a serializable representation is wanted, NOTA round-trip is the canonical assertion format, since the system already converts to NOTA at the wire boundary. This is the same do-not-hide-typification-in-strings discipline, applied at the test layer.] High Zero))"
  ```
- from `nt00` — *Tests exercise the schema-emitted surface itself, never hand-written shims standing in for it.*
  ```
  spirit "(Record ([schema testing schema-emitted-types] Principle [Schema-emitted Rust types are the canonical truth for every type that appears in the system; everything else is methods on those nouns or trait impls those types satisfy. No hand-written enum stubs at boundaries, no hand-written observer state, no hand-written validation-error or marker shims. Tests construct schema-emitted values, invoke the engine through its schema-emitted trait surfaces, observe schema-emitted events, and assert on schema-emitted typed outputs — so the tests exercise the real built system and prove the schema drives it.] High Zero))"
  ```
- from `fizd` — *An engine trait is proven in use only by observing it exercised at runtime, not by its presence in source.*
  ```
  spirit "(Record ([runtime-witness engine-traits proof-of-usage observability] Principle [Proof that the Signal, Nexus, and SEMA engine traits are actually called belongs to a runtime witness — a live log stream observable from the client — rather than to source inspection. The witness is the deployable realization of the proof-of-usage ladder: a trait present in source is not the same as a trait exercised by the running system.] High Zero))"
  ```

## SEMA storage & daemon lifecycle (5)

- from `2dku` — *The durable-state substrate is named SEMA consistently across schema, runtime engine, and the .sema on-disk file.*
  ```
  spirit "(Record ([sema durable-state naming storage] Clarification [SEMA names the durable-state layer coherently: the SEMA schema describes the data types, the SEMA engine performs the read/write database work, and the durable state lives in a file carrying the .sema extension. The naming chain is consistent from type to engine to on-disk substrate.] High Zero))"
  ```
- from `9rxq` — *SEMA state is durably persisted so a reopened store resumes both its records and its commit sequence; the state digest is a content-addressed hash over the committed records.*
  ```
  spirit "(Record ([sema persistence state-digest durability] Decision [The SEMA store is durable on disk: it holds a records table keyed by identifier to its archived entry and a ledger of the next-identifier and commit-sequence counters. A store reopened from the same path resumes its records and continues its commit sequence rather than restarting the count, so a daemon self-resumes from persisted state. The state digest is a real content-addressed hash (blake3) over the committed records reduced to the schema's integer width, with an empty store digesting to zero.] High Zero))"
  ```
- from `k8in` — *A daemon's data types are compiled in, so changing a type means compiling and spawning a new daemon binary, never mutating the running one.*
  ```
  spirit "(Record ([daemon compilation data-types upgrade] Constraint [Daemon data types are statically compiled into the binary. Introducing or changing a Rust data type therefore requires recompiling the daemon from the derived types and spawning the resulting new binary; a running daemon's type set is fixed for its lifetime.] High Zero))"
  ```
- from `0yk3` — *A virgin daemon starts unconfigured and is configured by a runtime meta-signal, not a startup config argument.*
  ```
  spirit "(Record ([daemon configuration bootstrap component-triad] Decision [A daemon that has never started, holds no state, and is unconfigured boots into a semi-started state and waits for an authenticated configuration meta-signal. Configuration is a runtime reaction to a typed message rather than a configuration-file argument supplied at startup.] High Zero))"
  ```
- from `mxmn` — *Component resources are scoped per engine identity: each engine owns its own federation of component instances, including its own spirit.*
  ```
  spirit "(Record ([engine-scoped spirit component-federation] Decision [Resources are scoped to an engine identity. Each engine owns its own federation of component instances rather than sharing global ones, and spirit is part of that federation — every engine has its own spirit instance scoped under that engine's identity, following the same engine-id-scoped pattern as the other components.] High Zero))"
  ```

## Versioning, upgrade & handover (6)

- from `prwb` — *A schema's content-addressable version hash is its canonical version identity, above Cargo semver.*
  ```
  spirit "(Record ([component-shape schema-version content-addressable-hash] Decision [The SEMA database holds its schema-version hash as canonical version identity. The hash is deterministic and content-addressable — the schema's content fully determines its hash, and the hash is the address. This schema-version hash is the version identity, layered above Cargo semver, and it is what upgrade dispatch keys on.] VeryHigh Zero))"
  ```
- from `76jt` — *rkyv enum discriminants are persisted wire values, so variant declaration order is fixed and semantic ordering comes from a manual Ord, never from declaration order.*
  ```
  spirit "(Record ([rkyv storage-and-wire schema enum-ordering] Principle [For an enum persisted through rkyv, the discriminant assigned by source declaration order is part of the on-disk wire contract: reordering variants reinterprets every already-archived value. Therefore declaration order is frozen by what is already persisted, and any new variant appends at the end rather than displacing existing discriminants. Semantic ordering that disagrees with declaration order is expressed through a hand-written Ord (mapping each variant to an explicit rank), not through Rust's derived Ord over declaration order.] High Zero))"
  ```
- from `60an` — *Version handover between component versions runs under an authority that can force-flip, roll back, and quarantine a version.*
  ```
  spirit "(Record ([signal version-handover component-shape] Decision [Handover from one component version to its successor is governed by an explicit version-handover contract held by the owning component. That authority can force-flip traffic to the new version, roll back to the prior version, and quarantine a version that proves bad. Version transition is a controlled, reversible operation under a single owner, not an uncoordinated swap.] High Zero))"
  ```
- from `81b2` — *During an upgrade handover the new daemon copies the old database to its own location and migrates the copy; it does not share the live store.*
  ```
  spirit "(Record ([upgrade-handover database migration rollback] Clarification [At an upgrade handover the incoming daemon takes its own copy of the outgoing daemon's database and runs migration against that copy, rather than opening the shared store in place. Copy-then-migrate is required for cross-version upgrades because the schemas differ, and is safer even for same-version handovers because it preserves the old store for rollback if the new daemon fails after cutover. State changes occurring between the copy point and the cutover instant are reconciled per component: synchronous-write components need no delta, while in-memory-state components carry a mirror delta across.] High Zero))"
  ```
- from `7jd9` — *Spirit database upgrades are exercised only against a sandbox copy of the store, never the live store.*
  ```
  spirit "(Record ([spirit schema-upgrade sandbox testing] Constraint [Database upgrade and migration runs are validated against an isolated sandbox copy of the Spirit store, never against the live store. Schema versioning begins each repo's schema files at the initial version and every upgrade path is proven on the copy before it can touch real persisted records.] High Zero))"
  ```
- from `pzqw` — *A plain file copy of a live transactional database is not transaction-coherent under concurrent writes; coherent snapshots require freezing writes or a coherent-copy mechanism.*
  ```
  spirit "(Record ([storage redb coherent-snapshot] Constraint [The operating system does not lock a redb file against a plain filesystem copy while another process holds it open, but that copy is not transaction-coherent: a copy taken during concurrent writes can suffer torn reads, partial pages, inconsistent B-tree state, and headers pointing to nonexistent pages. A coherent snapshot requires either freezing writes before the copy or using a coherent-copy mechanism such as a database backup API or a filesystem copy-on-write snapshot.] High Zero))"
  ```

## Spirit intent-store design (4)

- from `2otq` — *A Spirit record carries a collection of topics, not a single topic.*
  ```
  spirit "(Record ([spirit topics record-shape] Decision [A Spirit record is tagged with multiple topics rather than one, so a record can be discovered along any of the several subjects it bears.] High Zero))"
  ```
- from `o1sl` — *A Spirit record's identity is a random hash, giving one uniform hash identity space.*
  ```
  spirit "(Record ([spirit record-identity hash] Decision [Spirit record identities are random hashes rather than sequential integers, yielding a single uniform hash identity space. Identity carries no ordinal meaning and no positional encoding.] High Zero))"
  ```
- from `dppt` — *In the intent store a record's certainty distinguishes withdrawn confidence (absent) from weak-but-real intent (Minimum); the two must never collapse.*
  ```
  spirit "(Record ([intent-store certainty removal-candidate] Decision [Absent certainty on a record means confidence has been withdrawn and the record is nominated for removal; a Minimum certainty means weak but genuine intent that must be preserved. Removal nomination and weak intent are distinct states and must not be conflated.] High Zero))"
  ```
- from `ubgg` — *Spirit supports agent-facing subscription to incoming intent records, filterable by topic, so agents stay current with what others record.*
  ```
  spirit "(Record ([spirit streaming subscription intent] Decision [An agent can subscribe through the Spirit interface to newly recorded intent, filtering by topic or similar criteria, so agents keep up to date with what other agents are recording without polling the whole store.] Medium Zero))"
  ```

## Plane model (1)

- from `h3cy` — *The plane axis is modeled as first-class nouns — a Plane node owning plane-intrinsic naming and a PlaneProjection edge owning the cross-plane transforms — rather than booleans and inline conditionals.*
  ```
  spirit "(Record ([plane plane-projection schema-codegen noun-owned] Decision [The implicit plane axis is promoted into two typed nouns instead of plane booleans and per-plane conditionals scattered across a code-generation god-struct. Plane is the node — Signal, Nexus, Sema — owning plane-intrinsic naming as pure self constants (module name, wrapper path, envelope name, engine-trait name, and the like). PlaneProjection is the edge — the directed cross-plane transforms — owning edge identity, its wrapper paths, and per-variant mapping. Each runtime construct holds a Plane or a PlaneProjection and composes it with its schema data when emitting, so the generator's god-struct dissolves. Questions that depend on the schema's roots rather than the plane (which role traits, which actor-variant labels, which route-type membership) take the roots as a parameter instead of living on the plane nouns.] High Zero))"
  ```

## Roles, process & deploy (10)

- from `r310` — *Engine migrations proceed one component at a time — lock a single repository, test it thoroughly, then move to the next.*
  ```
  spirit "(Record ([migration component-locking testing] Constraint [Engine migrations advance component by component: lock one repository at a time, test that component thoroughly before moving on, and revise the approach whenever implementation evidence reveals a better design.] VeryHigh Zero))"
  ```
- from `9l1z` — *Designer lanes design, prototype, report, and hand work forward to operators; they do not implement, and their reports carry separate open-question sections for the psyche and for the implementing operator.*
  ```
  spirit "(Record ([orchestrate designer-lane handoff reports] Principle [A designer lane's deliverable is design, prototype, report, and tracked work items for the operator lane to implement; the designer does not carry the implementation itself. Each design report splits its open questions into two audiences: questions awaiting psyche direction before implementation can begin, and clarifications the implementing operator resolves as they build. Passing both sets of open questions forward is part of the lane handoff, not an afterthought.] High Zero))"
  ```
- from `p4dj` — *A major architectural break runs two parallel implementation tracks — operator on the new repo's main, designer on branches off it — compared periodically until convergence drives integration.*
  ```
  spirit "(Record ([workspace component-shape double-implementation] Decision [Major architectural breaks proceed as two parallel implementation tracks. Operator creates new repositories (suffix -next when upgrading a prior concept, a new name for a new concept) and works directly on their main branch, which amalgamates the best ideas from earlier prototypes into one substrate. Designer iterates a parallel design on worktree branches based off operator's main, or on dedicated design-prefixed repositories. The two tracks are compared periodically and convergence drives integration.] High Zero))"
  ```
- from `0xcq` — *Intent is manifested into each worked repo's INTENT.md and ARCHITECTURE.md, not only the workspace log.*
  ```
  spirit "(Record ([intent-manifestation per-repo intent architecture] Principle [Captured intent is reflected into the per-repo INTENT.md and ARCHITECTURE.md of every repo it affects, so an agent working inside a repo sees the intent governing its design, implementation, and testing without first reading the workspace-wide intent log. Whenever new intent affects how to design, build, or test in a specific repo, it propagates into that repo's intent files alongside the Spirit capture.] High Zero))"
  ```
- from `tdit` — *A required skill must be structurally unskippable at the moment it applies, not enforced by a hortative reminder inside the skill file.*
  ```
  spirit "(Record ([skills enforcement structural-prevention] Principle [A skill that must govern a class of work has to be enforced structurally — through hooks, a hard-override pointer in the every-session contract, or a skill-index shape that forces the read — so it cannot be skipped at the moment the work is authored. A reminder living inside the skill file is insufficient, because the agent that skips the skill never reads the reminder.] Maximum Zero))"
  ```
- from `ot9e` — *Full operating-system build tests run on remote builders with no local build fanout.*
  ```
  spirit "(Record ([nix testing remote-builders] Constraint [Full operating-system build verification runs on remote builders, with local max-jobs held at zero so the local machine dispatches rather than fans out the build. Whole-OS builds are not a local laptop workload.] High Zero))"
  ```
- from `65bo` — *A node whose own administrative path rides the services its deploy would restart must transition via boot-mode-plus-reboot or detached activation, never a live restart.*
  ```
  spirit "(Record ([deployment platform router] Constraint [When the activation of a new configuration restarts the very services that carry the operator's connection to a node (router, gateway, or any host reached through services it also serves), a live in-session activation severs that path mid-transition and strands the node half-configured. Such a node transitions either by booting the new configuration and rebooting with no live service restart, or by detaching the activation on the host so it survives the connection drop. A backup uplink is a recovery net for a bad boot, not a mechanism that makes a live switch survivable, because it does not change the administrative path into the node.] High Zero))"
  ```
- from `3n4c` — *Context maintenance ranks reports per topic by recency favoring newer design, and cross-lane runs land as one meta-report in the dispatcher's lane with per-lane sub-reports as handoffs.*
  ```
  spirit "(Record ([context-maintenance meta-report cross-lane topic-recency] Decision [Context maintenance gathers, per topic, the reports across lanes and recency-ranks them, distinguishing stale from newer design and favoring the newer. A cross-lane pass produces a single meta-report directory in the dispatcher's lane — a frame-and-method entry, one numbered sub-report per lane covered, and an overview synthesis — where each per-lane sub-report is a handoff the agent in that role reads during their own context maintenance.] High Zero))"
  ```
- from `b1lv` — *A magnitude or priority concept is one shared schema type reused across components, not re-declared per component.*
  ```
  spirit "(Record ([schema shared-types magnitude component-shape] Decision [Where multiple components need a graded magnitude or priority scale, they collapse onto a single shared schema type rather than each declaring its own near-duplicate enum. The shared type is defined once and referenced everywhere it is needed, consistent with the schema-of-schemas reuse discipline.] High Zero))"
  ```
- from `v0xn` — *Health and readiness are expressed through a single magnitude type, with an explicit unknown for indeterminate state.*
  ```
  spirit "(Record ([schema magnitude health readiness component-shape] Decision [Component health and readiness collapse onto one shared magnitude type rather than living as separate parallel notions, and that type carries an explicit unknown variant so indeterminate state is representable instead of being faked with a sentinel.] Medium Zero))"
  ```

## Dropped (live-covered)

- `ocrf` — covered by live 5zur (methods on schema types, not free functions)

## Unplaced (review)

- `0huc` — The schema-derived Spirit carries the full intent vocabulary, not a reduced subset.
- `ujwl` — Prefer a compact enum-payload variant that carries a reason enum directly over wrapping the reason in a larger report struct.