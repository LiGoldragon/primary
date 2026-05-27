# Schema runtime actor upgrade vision - repo manifestation targets

Subagent: operator
Date: 2026-05-27

## Frame

This report inspects the main checkouts:

- `/git/github.com/LiGoldragon/nota-next`
- `/git/github.com/LiGoldragon/schema-next`
- `/git/github.com/LiGoldragon/schema-rust-next`
- `/git/github.com/LiGoldragon/spirit-next`

I read each repo's `AGENTS.md`, `ARCHITECTURE.md`, and `INTENT.md`. No
`skills.md` file is present in these four repos. I did not edit source or repo
docs.

Recent Spirit records already capture the core direction:

- Records 925-940: macro expansion, schema root struct, positional schema
  fields, recursive macro lowering to scalar leaves.
- Records 929-935: binary rkyv communication, signal frames, mail state,
  request-reply correlation, database markers.
- Records 945-950 and 953-959: schema-created actor input/output enums,
  generated schema objects as Rust nouns, internal SEMA/database message
  language, owner/core permission checks, upgrade traits, and upgrade
  observability.
- Gap-fill records 951-952 add REST-shaped wire framing and schema/Rust mirror
  naming.

The repo files are partially manifested. The strongest current manifestation is
`spirit-next`, followed by `schema-next`. `nota-next` and `schema-rust-next`
need concise doc expansion so agents entering those repos see the same runtime
vision without reading Spirit history.

## Cross-repo target shape

The repo docs should now state one coherent chain:

1. `nota-next` owns raw structure only: delimiter spans, root blocks, source
   spans, structural headers, and symbol-shape predicates.
2. `schema-next` owns macro lowering from NOTA structure into assembled schema.
   Macro selection is position-aware and object-shape-aware; the endpoint is
   ordered, macro-free schema objects.
3. `schema-rust-next` owns Rust source emission from assembled schema into
   `src/schema/`. The generated code defines data nouns, NOTA projections,
   rkyv archive types, route/header support, frame traits or methods, and
   upgrade trait requirements where schema diffing demands hand-written logic.
4. `spirit-next` is the running proof: schema-authored `Input`/`Output` and
   internal `SemaCommand`/`SemaResponse` are generated, hand-written Rust
   attaches methods to those generated nouns, and the CLI/daemon process
   boundary uses binary rkyv signal frames rather than NOTA.

The docs should use "actor input/output enum roots" as the general framing, but
with the correction that the authoring schema may declare input and output as
separate root fields while binary emission can partition a single tag/header
space. For components with one message shape, `Input` can be a struct at the
schema level; the actor-channel rule is that each actor has a schema-defined
reaction language and response language.

## nota-next

Current coverage:

- `ARCHITECTURE.md` correctly states that `nota-next` owns raw NOTA structure,
  `Document`, `Block`, `SourceSpan`, factual `is_*` methods, and structural
  `qualifies_as_*` candidate methods.
- `INTENT.md` already states the delimiter-balanced first pass and compact
  first-two-level structure header.
- The boundary is correctly negative: it does not know type, field, schema,
  enum, macro, or import semantics.

Docs gaps:

- Add to `ARCHITECTURE.md` under `Planes`: `StructureHeader` is the text-side
  routing witness consumed by `schema-next`, analogous to the short-header idea
  used later by binary signal frames.
- Add to `ARCHITECTURE.md` under `Boundary`: `nota-next` exposes candidate
  predicates for macro dispatch but never chooses a schema macro or actor
  message meaning.
- Add to `INTENT.md` after the existing header paragraph: NOTA is the
  structural floor for schema macro matching; delimiter shape, object count,
  and symbol qualification must be preserved without semantic lowering.

Implementation gaps:

- None for the new actor/runtime intent directly. This repo should stay narrow.
  Any pull toward schema-object nouns, actor roots, rkyv, or upgrade traits in
  `nota-next` would violate its boundary.

## schema-next

Current coverage:

- `ARCHITECTURE.md` documents the current pipeline from `nota-next::Document`
  through `StructureHeader`, root validation, `MacroRegistry`, and `Asschema`.
- It names `SchemaPackage`, the standard `schema/lib.schema` entrypoint, module
  loading, colon-qualified module names, and crate-name namespace identity.
- It documents positional root fields: imports, input, output, namespace.
- It captures pair-style brace namespaces, struct square brackets, enum
  parentheses, implicit root `Schema`, and macro trace witnesses.
- `INTENT.md` captures position-aware macro lowering, structural macro
  matching, brace sugar as macro, root struct reading, and structure header
  recording.

Docs gaps:

- Rename or qualify `Asschema` in docs against the intent name
  `AssembledSchema`. Current source still uses `Asschema`; docs can say
  "`Asschema` is the current crate type for the assembled schema endpoint" until
  the implementation name changes.
- Add an `Assembled schema nouns` section to `ARCHITECTURE.md`: assembled
  schema contains named structs, newtypes, enums, root actor reaction enums, and
  ordered namespace declarations. These are the nouns that downstream Rust
  emission and hand-written methods attach behavior to.
- Add an `Actor channel roots` section: schema-level `input` and `output`
  fields declare the actor/channel reaction and response languages; the binary
  emitter may merge them into one reserved tag/header space.
- Add an `Upgrade surface` section: schema diffing compares assembled schema
  versions; unchanged types require no Rust upgrade code, changed types require
  generated trait obligations for hand-written upgrade methods, and accepted
  old-version messages should produce observable upgrade events.
- Add to `INTENT.md`: internal SEMA/database channels are also schemas, not
  special engine-only shapes.

Implementation gaps:

- The macro registry is real, but macro definitions are still Rust-defined
  domain lowerers. Spirit records 888-889 require schema-defined macros and
  generic macro-loading logic. The repo should identify this as the next
  architectural gap rather than overclaim completion.
- `Asschema` currently models `input` and `output` as independent
  `EnumDeclaration`s. It does not yet model single tag-space partitioning,
  actor/channel metadata, upgrade metadata, schema hashes, or version
  adjacency.
- There is no schema diff model, no upgrade operation model, no generated
  upgrade-trait requirement surface, and no observable upgrade event schema.
- Scalars are still minimal (`Text`, `Integer`) through downstream emission;
  vector support and typed-string/newtype richness are incomplete.

## schema-rust-next

Current coverage:

- `ARCHITECTURE.md` says `schema-rust-next` consumes `schema-next::Asschema`
  and emits Rust source.
- It documents `RustEmitter`, `RustCode`, `GeneratedFile`, and
  `RustModulePath`.
- It correctly says generated Rust is source-visible under `src/schema/`, not
  hidden in `OUT_DIR`, and that old signal macros are not used.
- `INTENT.md` captures Rust emission as a separate step from Rust macros and
  `src/schema/` as the fixed materialization path.

Docs gaps:

- Add a `Generated nouns and handwritten behavior` section to
  `ARCHITECTURE.md`: emitted Rust defines data-bearing nouns; hand-written Rust
  implements methods and traits on those generated nouns. Generated data types
  are not mirrored by hand-written sibling types.
- Add a `Signal frame emission` section: root signal objects emit route enums,
  short-header logic, NOTA text projection, rkyv binary encode/decode, and
  eventually a reusable communication trait instead of ad hoc methods on each
  root enum.
- Add an `Upgrade trait emission` section: unchanged types emit no upgrade
  requirement; changed types emit trait obligations for version-boundary
  upgrade and accept behavior; old-version ingress and database load use those
  traits.
- Add to `INTENT.md`: schema/Rust names mirror each other through
  single-colon schema paths and Rust module paths, making schema source and
  emitted Rust grep-compatible.

Implementation gaps:

- The emitter already derives rkyv archive types, NOTA parsing/formatting,
  route enums, 64-bit short headers, and `encode_signal_frame` /
  `decode_signal_frame` methods for `Input` and `Output`.
- There is no `Communicate` trait or reusable signal-frame trait object yet.
  Current emission places frame behavior as inherent methods on each root enum.
- Header partitioning is currently root-index based in a 64-bit header
  (`Input` root index 0, `Output` root index 1). It is not yet the documented
  actor input/output partition of one first-byte or schema-declared tag space.
- Emission has no schema hash/version identity in generated code.
- Emission has no schema diff input, no previous-version type namespace, no
  upgrade traits, no upgrade events, and no database-marker reply support.
- Generated support code includes helper structs such as `NotaSource`,
  `NotaBlock`, and `NotaText`; these are data-bearing and acceptable as support
  nouns, but the docs should keep the focus on schema-created domain nouns.

## spirit-next

Current coverage:

- `ARCHITECTURE.md` is already close to the desired manifestation. It shows
  the full path from `schema/lib.schema` through `schema-next`,
  `schema-rust-next`, checked-in `src/schema/lib.rs`, and runtime shims.
- It states the CLI/daemon binary boundary: CLI parses NOTA into generated
  `Input`, frames generated `Input` as short-header plus rkyv archive bytes,
  daemon decodes generated `Input`, dispatches through `Engine`, and returns
  generated `Output`.
- It states that transport owns only length-prefix socket I/O and not route
  enums, short-header matching, or rkyv encoding.
- It documents the executor shape: `Input -> SemaCommand -> SemaResponse ->
  Output`, with schema emitting nouns and Rust attaching behavior.
- It names schema-generated types as implementation nouns and rejects parallel
  hand-written mirrors.
- `INTENT.md` captures NOTA CLI I/O, binary rkyv component/process
  communication, generated `src/schema/`, build freshness, generated
  Signal/SEMA surfaces, old macro exclusion, and upgrade/redb as future work.

Docs gaps:

- Add an `Actor channels` subsection to `ARCHITECTURE.md`: `Input`/`Output`
  are the external actor reaction/response roots; `SemaCommand`/`SemaResponse`
  are the internal storage actor reaction/response roots. Future internal
  actors should get their own schema files rather than ad hoc Rust mail enums.
- Add a `Communication trait and mail state` subsection: binary exchange should
  move from synchronous `SignalTransport::exchange` toward a schema-defined
  communication trait with unique message identifiers, handshake semantics,
  response correlation, and database markers in replies.
- Add an `Upgrade path` subsection: durable storage and old-version ingress
  should load previous schema versions, invoke generated upgrade trait
  obligations on changed schema objects, accept upgraded messages, and emit
  observable upgrade events.
- Add to `INTENT.md`: accepted old-version messages must be observable so the
  runtime, routers, or agents can notify clients to upgrade schema.

Implementation gaps:

- Storage is still in-memory. There is no redb database marker, no durable
  schema version marker, and no read-time database upgrade path.
- Messaging is synchronous request/reply over a length-prefixed Unix stream.
  It lacks async unique identifiers, mail queue state, handshake, response
  correlation, and database marker replies.
- The binary signal frame exists, but it is generated directly in
  `src/schema/lib.rs`; it is not imported from a schema-declared
  `signal-frame.schema` substrate.
- `Input::lower_to_sema`, `SemaResponse::into_output`, and `Store::apply` are
  good examples of hand-written methods on generated/runtime nouns. There are
  no generated traits yet requiring those methods, so compile-time enforcement
  of the method surface is still informal.
- No upgrade traits, old-version type namespaces, schema diff products, or
  upgrade observability events exist yet.
- The repo-triad split remains absent by design in this pilot. Docs should name
  whether the pilot remains a one-repo proof or becomes a migration target for
  final `spirit` / `signal-spirit` / `core-signal-spirit` split.

## Suggested exact target sections

For later doc edits, the minimal section targets are:

- `nota-next/ARCHITECTURE.md`: add `## Structure header` and expand
  `## Boundary`.
- `nota-next/INTENT.md`: add one paragraph under the existing header intent
  about preserving macro-dispatch structure without semantics.
- `schema-next/ARCHITECTURE.md`: add `## Assembled schema nouns`,
  `## Actor channel roots`, and `## Upgrade surface`; qualify `Asschema` as the
  current implementation name for assembled schema.
- `schema-next/INTENT.md`: add schema-object nouns, actor input/output roots,
  internal SEMA/database schemas, and upgrade-diff intent.
- `schema-rust-next/ARCHITECTURE.md`: add `## Generated nouns and handwritten
  behavior`, `## Signal frame emission`, and `## Upgrade trait emission`.
- `schema-rust-next/INTENT.md`: add schema/Rust mirror naming, generated traits,
  and hand-written methods on generated objects.
- `spirit-next/ARCHITECTURE.md`: add `## Actor channels`,
  `## Communication trait and mail state`, and `## Upgrade path`.
- `spirit-next/INTENT.md`: add old-version message acceptance, upgrade event
  observability, communication trait, and database-marker replies.

No `skills.md` exists in these repos. If repo-specific agent discipline becomes
needed, create `skills.md` only when it contains operational rules not already
clear from `AGENTS.md`, `ARCHITECTURE.md`, and `INTENT.md`.
