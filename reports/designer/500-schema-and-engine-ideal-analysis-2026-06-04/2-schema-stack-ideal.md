---
title: Slice 2 — the schema stack, ideal vs current, per repo
role: designer
variant: Synthesis
date: 2026-06-04
topics: [schema-stack, nota-next, schema-next, schema-rust-next, triad-runtime, ideal-vs-current, dual-engine, RustItem, triad-runner, data-before-text, strings-at-edges]
description: |
  Ideal-vs-current analysis of the four substrate repos of the schema stack —
  nota-next, schema-next, schema-rust-next, triad-runtime. For each, the
  future-oriented reusable pattern it should embody, contrasted with the
  landed code at file:line, with the gap made explicit. The headline gaps:
  schema-next ships two divergent lowering engines (one-way emit, no witnessed
  round-trip); schema-rust-next honors data-before-text for type declarations
  but hand-spells the impl layer in 504 self.line(format!()) calls with
  manually-counted four-space indentation; triad-runtime owns only trace, with
  the generic runner (triad_main!) still unbuilt. nota-next is the one repo at
  or near its ideal.
---

# Slice 2 — the schema stack: ideal vs current, per repo

The schema stack is the substrate that emits the persona triad. Four repos
form the lowering pipeline before `spirit` consumes the output:

```text
nota-next  ->  schema-next  ->  schema-rust-next  ->  triad-runtime  ->  spirit
(structural    (lower to          (emit Rust text)      (shared runtime,    (the proof)
 NOTA parse)    Asschema)                                trace + runner)
```

The analysis frame (record 2550): for each repo, the IDEAL is the most correct,
future-oriented, reusable pattern it should embody. Below each ideal sits WHAT
WE HAVE NOW at file:line, so the gap is visible. The ideal is the target, not a
description of the present.

Across the four, the maturity gradient is steep. nota-next is at its ideal — a
clean structural substrate with no schema semantics. schema-next has the right
shape but ships the stack's one correctness bug (two divergent engines) and a
one-way emit where a witnessed round-trip is the destination. schema-rust-next
honors data-before-text exactly at the type-declaration layer and abandons it
for the 80% of output that is impls. triad-runtime is correct for its current
single concern (trace) but the most-repeated missing noun — the generic runner
— is not in it yet.

## nota-next — the structural substrate (at its ideal)

The IDEAL: the clean structural-NOTA substrate any structural-macro language
reuses. It parses delimiters, atoms, and block structure into `Document` /
`Block` / `Atom`; preserves byte/line/column spans; offers `qualifies_as_*`
structural predicates and a value codec — and knows *nothing* about schema. The
boundary is the whole point: a second consumer (an intent-record language, a
deployment-stanza language) reuses the same parse without inheriting schema
vocabulary.

WHAT WE HAVE NOW matches the ideal closely. The crate's own doc states the
contract as a rule, not a description — [This crate does not know what a schema
type, field, declaration, enum, macro, or import means. It only exposes the raw
structure and value serialization needed by the next layer] (ARCHITECTURE.md:82-84).
The structural predicates are present and named correctly — factual methods use
`is_*` (`src/parser.rs:81-139`), structural candidate methods use
`qualifies_as_*` (`src/parser.rs:190-206` on `Block`, `:542-567` on `Atom`).
The macro-node layer is explicitly semantic-neutral — [The mechanism is
semantic-neutral: schema-next may register struct/enum/newtype patterns, but
nota-next only matches atoms, delimiters, literals, and rest captures]
(ARCHITECTURE.md:51-54). Spans are preserved for diagnostics
(`SourceSpan` carries byte/line/column, `src/parser.rs:11`).

The GAP is narrow and is about reuse-proof, not correctness: there is exactly
one consumer (schema-next) today, so the "any structural-macro language reuses
it" claim is latent — asserted by the clean boundary but unwitnessed by a second
language. The `Name@{...}` / `Name@[...]` at-binding sigil syntax
(ARCHITECTURE.md:58-78) lives in the structural parser; if a future structural
language wants different name-binding syntax, that sigil is a schema-leaning
choice sitting in the substrate. Minor. nota-next is the repo closest to its
ideal and is not where the stack's debt concentrates.

## schema-next — the lowering front end (the dual-engine bug)

The IDEAL has three layers, all ratified in recent intent:

1. ONE lowering engine (records 1572/1578). A single authored-schema → Asschema
   front end, multi-pass (collect names, then resolve forward references), with
   exactly one home for every lowering rule — header resolution, the
   single-field→Newtype decision, the `Vec`/`Optional`/`Map` reference dispatch.
2. Schema-as-its-own-codec with a *witnessed* round-trip (record 1573). The
   authored `.schema` text projects to typed `SchemaSource`, lowers to
   `Asschema`, and the path round-trips — schema is encoded and decoded by its
   own machinery, proven by a witness, not a one-way emit.
3. Multi-pass resolution as the single front end (record 1556) — pass-1 collect
   candidate type names, pass-2 resolve variant-payload shorthand against that
   namespace.

WHAT WE HAVE NOW is the right shape with the stack's one correctness bug. There
are TWO lowering engines that share no code and disagree on behavior:

- The registry/document path: `SchemaEngine::lower_source` (`src/engine.rs:238`),
  `lower_document` (`src/engine.rs:276`), lowering a `nota_next::Document`
  through `MacroRegistry` handlers in `declarative.rs`.
- The typed-source path: `SchemaSource::lower` (`src/source.rs:98`) →
  `to_asschema` (`src/source.rs:106`), the only production caller
  (`SchemaModuleSource::lower`, `src/module.rs`).

The multi-pass resolver lives on ONLY the source path —
`SourceTypeResolver::from_source` (`src/source.rs:112`) collects names, then
`push_public_declarations` (`:114-115`) and `to_asschema_enum` (`:116-117`)
resolve against them. The registry path has no resolver: `AssembledVariant::lower`
(`src/declarative.rs:1846-1849`) lowers a bare PascalCase header variant straight
to `payload: None`. For the identical `Lookup RecordIdentifier` header shape,
the source path resolves the payload and the registry path drops it. The green
test suite hides this because the equivalence fixture has no bare header (full
trace in report 495 entry 2).

The GAP: the dual engine is on main today — both `lower_source` (engine.rs:238)
and `SchemaSource::lower` (source.rs:98) coexist, with the divergent
`payload: None` at declarative.rs:1849. The ratified fix (1572/1578) unifies on
`SchemaSource` as the one front end and retires the registry engine, but that is
ratified *intent*, not landed code. The codec round-trip is also a destination,
not a witnessed present: ARCHITECTURE.md:33-43 describes the `SchemaSourceArtifact`
writer projecting back through NOTA before rebuilding `SchemaSource`, but report
499's correction-5 is explicit — [schema-as-its-own-codec is a destination — the
source has a one-way emit path today, not a witnessed round-trip] (record 1591).
The third sub-gap is `SymbolPath` shape: it landed flat (`Vec<Name>`,
`src/asschema.rs:85-86`) and the psyche REOPENED the structured component/plane/
variant/payload/field form at record 1586 — unresolved, an open decision (covered
in slice on SymbolPath; flagged here because it is a schema-next data type).

## schema-rust-next — Rust emission (data-before-text stops at declarations)

The IDEAL: data before text ALL the way down (records 1576/1584). A `RustItem` /
`RustImplBlock` / `RustMatch` token model where every emitted construct — type
declaration, trait, `From` impl, inherent impl, match arm, brace — is first a
typed data object, and a single renderer with an owned indentation depth turns
the whole tree into text exactly once. No construct is hand-spelled as a format
string; manual four-space counting is structurally impossible because the
renderer owns depth.

WHAT WE HAVE NOW honors data-before-text for the type-declaration layer and
abandons it for the impl layer. The declaration layer is real data: `RustModule`
(`src/lib.rs:88`), `RustTypeDeclaration` — a four-arm `Alias`/`Struct`/`Enum`/
`Newtype` sum (`src/lib.rs:386`), projected one-to-one from
`schema_next::TypeDeclaration`. INTENT.md:238-240 states the right direction —
[Rust emission is data before it is text. The emitter maps Asschema into a typed
RustModule object ... rendering RustModule produces RustCode].

But the support/impl layer is `RustWriter` (`src/lib.rs:704`), a `String`
accumulator whose one primitive `line(...)` is called **504 times** (confirmed
unchanged since the 495 audit). The clearest symptom is hand-counted
indentation. `emit_newtype_inherent_impl` (`src/lib.rs:955`):

```rust
self.line(format!("impl {name} {{"));
self.line(format!(
    "    pub fn new(payload: {payload_type}) -> Self {{"
));
self.line("        Self(payload)");
self.line("    }");
self.blank();
self.line(format!("    pub fn payload(&self) -> &{payload_type} {{"));
self.line("        &self.0");
self.line("    }");
```

The `"    "` / `"        "` literals are the author counting four spaces by hand,
line by line. That single method emits the `Output::rejected` constructor pattern
visible in the checked-in output (`spirit/src/schema/lib.rs:611-614`):

```rust
pub fn rejected(payload: Rejected) -> Self {
    Self::Rejected(payload)
}
```

The data model gets the noun right (`Rejected` is an `Alias`, so the constructor
is pass-through and gets no `From` impl) but the *bytes* of that constructor are
hand-templated, not rendered from a `RustImplBlock { name, methods: [...] }`.

The GAP: the `RustItem` / `RustImplBlock` / `RustMatch` token model (1576/1584)
is ratified intent, not landed — and the symptom that proves it is missing is the
504 `self.line()` calls plus the manual indentation in `emit_newtype_inherent_impl`
and its siblings (`emit_route_impl` at `src/lib.rs:1366` and `emit_signal_frame_impl`
at `:1390` emit a byte-identical `route()` match; the lifecycle preamble is
emitted three times verbatim at `:2387/:2431/:2459`). Until the impl layer becomes
data, every new emitted construct is another format-string with another chance to
miscount spaces, and the duplicated walks (three `TypeReference` descents at
`src/lib.rs:680/856/2579`) drift independently.

## triad-runtime — the shared runtime (only trace is built)

The IDEAL: the shared runtime owns the four reusable mechanics every
schema-emitted daemon would otherwise hand-copy:

1. The generic triad runner — `triad_main!` (records 1574/1581). The socket-bind
   + accept-loop + dispatch every daemon repeats; extracted once so a component's
   `main` is one macro line.
2. The length-prefixed frame codec (the wire-framing already present for trace,
   generalized to the signal transport).
3. The single-NOTA-argument parser — the one-argument-rule front door
   (`binary <nota-string-or-path>`), shared so no component re-implements
   argument handling.
4. Trace — the typed event log, binary frame, socket listener, generic-over-event
   client.

WHAT WE HAVE NOW is item 4 only, plus the frame codec scoped to trace. The
production surface is two files: `src/lib.rs` (re-exports) and `src/trace.rs`
(331 lines). The trace mechanic is correct and at its ideal for its scope —
`TraceEventFrame` is the component boundary (`src/trace.rs:16`), the runtime is
generic over the event noun, `TraceFrame::to_bytes` writes a 4-byte big-endian
length + rkyv archive (`src/trace.rs:118-127`), and NOTA/text appears only at
the client display edge (`TraceClient::print_events`, `src/trace.rs:316-321`).
This is the strings-at-edges contract (records 1490/1492/1495) honored: no string
touches the typed interior. The crate's INTENT.md is explicit that the runner is
not yet here — [Future extraction waves may add generic daemon command
scaffolding, signal transport, and trace-aware test harnesses. Those move here
only when a second component would otherwise copy the same mechanics]
(ARCHITECTURE.md:55-57).

The GAP: the runner (`triad_main!`) is the single most-repeated missing noun in
the whole engine (report 499 §What's missing). It is ratified (1574/1581) and
absent — no `triad_main`, no signal transport, no single-argument parser in the
crate (`grep` finds only the trace-scoped length-prefix frame). Today `spirit`'s
daemon hand-writes its own socket-bind + accept-loop; the second component would
copy it verbatim, which is exactly the trigger the crate's own boundary rule
names for extraction. The runner is the load-bearing missing mechanism that turns
the stack from "emits one daemon's types" into "emits and runs the whole fleet."

## The cross-repo shape

The four repos sort cleanly along one axis — how far data-before-text and
single-home discipline have actually reached the code versus the ratified intent:

- nota-next: ideal reached. Boundary clean, predicates named, no schema leak.
- schema-next: shape right, one engine too many (the correctness bug), codec
  round-trip still one-way.
- schema-rust-next: data-before-text reaches declarations, stops at the 80% that
  is impls.
- triad-runtime: ideal for trace, missing the runner that is the most-repeated
  noun.

Three of the four gaps are the same gap viewed from different repos: ratified
intent that has not become landed code (the 1572/1578 one engine, the 1576/1584
token model, the 1574/1581 runner). Per report 499's correction-2, [Ratified is
not built] — these are intent, not main. The fourth, nota-next, is the proof that
when the discipline lands, the result is a clean reusable substrate; it is the
shape the other three are converging toward.
