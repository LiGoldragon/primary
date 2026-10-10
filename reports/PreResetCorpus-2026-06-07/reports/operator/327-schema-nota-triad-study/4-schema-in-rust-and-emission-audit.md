---
title: Schema-in-Rust Data Types and the Emission Audit (Criterion 2)
role: operator
variant: Psyche
date: 2026-06-06
topics:
  - schema-rust-next
  - rust-emission
  - token-vs-string
  - quote-prettyplease
  - mid-migration-audit
  - component-triad
description: |
  Audits how schema-rust-next turns a typed schema value into checked-in Rust
  source. Covers the Rust-model nouns (RustStruct/RustEnum/RustField/...), the
  LowerToRust trait + the context-carrying *Tokens wrappers that render via
  quote!, the RustEmissionTarget set + runtime_planes(), and the
  tokens -> prettyplease -> src/schema/*.rs artifact boundary. The crux is
  Criterion 2: is emission token-based or string-based? Verdict:
  PARTIAL / MID-MIGRATION, but FURTHER along than report 317 described — the
  whole declaration surface AND the runtime engine traits / trace / plane
  envelopes / runner adapter are now tokenized (28 ToTokens wrappers, 86
  quote! sites); the residual string surface is one 113-method RustWriter
  god-struct with 200 self.line + 62 format! calls concentrated in 20 named
  methods (signal-frame codec, route enums, split-plane projections, NOTA
  bridges, upgrade, enum constructors).
---

# Schema-in-Rust Data Types and the Emission Audit (Criterion 2)

## The one-paragraph answer

`schema-rust-next` takes a typed schema value and emits Rust interface
source into `src/schema/*.rs` in the consumer crate. There are two
distinct "schema-in-Rust" layers, and conflating them is the single
biggest source of confusion in the intent records. Layer one is the
**rkyv-serializable canonical schema value** that lives upstream in the
`schema-next` crate (`SchemaSource`, `Declaration`, `TypeDeclaration`,
`Schema`); that is the fz9n "schema-in-Rust is the rkyv-serializable
typed schema value." Layer two — the thing this repo actually owns — is a
**Rust-MODEL projection**: `RustStruct`, `RustEnum`, `RustField`,
`RustEnumVariant`, `RustAlias`, `RustNewtype`, `RustDeclaration`,
`RustTypeDeclaration`. These mirror the shape of the Rust they will emit
(a struct-with-fields noun, an enum-with-variants noun) and are produced
from the schema-next source nouns through `LowerToRust<Target>`. They are
NOT rkyv — they derive only `Clone, Debug, Eq, PartialEq`
(`lib.rs:786`, `840`, `815`). That is correct: they are an ephemeral
emission-shaped model, not a persisted artifact. Their MAIN USE (jypw) is
to make Rust emission convenient, and that is exactly what they do.

The emission itself is **mid-migration** between two mechanisms living in
the same file:

- A **token-based** path: 28 context-carrying `*Tokens` wrapper nouns,
  each `impl ToTokens`, building Rust with `quote!` (86 call sites), then
  funnelled through one `prettyplease::unparse` at `lib.rs:2885`.
- A **string-based** path: one `RustWriter` god-struct (113 methods)
  that accumulates a `String` buffer via `self.line(...)` (200 calls)
  and `format!` (62 calls).

Both paths write into the **same** `RustWriter.output: String` buffer
(`lib.rs:2669`), and the whole buffer is what `build.rs` writes to disk
(`build.rs:504`). So the final file is a literal interleaving of
prettyplease-formatted token output and hand-formatted strings. The
direction is decided (token-first, per intent e6v5 / o7a3 / 0bw0); the
string surface is acknowledged debt, captured in this repo's own
`INTENT.md:66-73`.

## 1. What the schema-in-Rust (Rust-model) data types look like

The Rust-model nouns are plain data records whose shape mirrors the Rust
construct they emit. A struct-noun holds a name and a vector of
field-nouns; an enum-noun holds a name and a vector of variant-nouns; a
variant-noun holds a name and an optional payload type. That direct
mirroring is what makes `quote!` interpolation trivial later.

`RustStruct` / `RustField` (`lib.rs:786`, `815`):

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RustStruct {
    name: Name,
    fields: Vec<RustField>,
}
// ...
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RustField {
    name: Name,
    reference: TypeReference,
}
```

`RustEnum` / `RustEnumVariant` (`lib.rs:840`, `869`):

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RustEnum {
    name: Name,
    variants: Vec<RustEnumVariant>,
}
// ...
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RustEnumVariant {
    name: Name,
    payload: Option<TypeReference>,
}
```

The alias-vs-newtype distinction the architecture insists on
(`ARCHITECTURE.md:99-103`) is encoded as two separate nouns under one
sum type (`lib.rs:709`):

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum RustTypeDeclaration {
    Alias(RustAlias),
    Struct(RustStruct),
    Enum(RustEnum),
    Newtype(RustNewtype),
}
```

`RustAlias` and `RustNewtype` are byte-for-byte the same fields (`name:
Name`, `reference: TypeReference`, `lib.rs:737`, `762`) — they are
distinct TYPES precisely so the emitter can render `type X = Y;` versus
`struct X(Y);` by which variant it is, not by inspecting a flag. This is
the de8i "each noun renders itself" shape: the discriminator is the Rust
type, not runtime data.

### These are NOT the rkyv canonical value — the important divergence

Intent fz9n says "schema-in-Rust is the rkyv-serializable typed schema
value." If you read that as describing the nouns above, it is **wrong** —
`RustStruct` et al. are not rkyv (`lib.rs:786` derives
`Clone, Debug, Eq, PartialEq` only). The rkyv-serializable value lives in
`schema-next`, e.g. `SchemaSource`
(`schema-next/src/source.rs:19` derives `rkyv::Archive,
rkyv::Serialize, rkyv::Deserialize, ...`) and the `declarative.rs`
declaration nouns (15+ `rkyv::Archive` derives). The Rust-model nouns in
this repo are a downstream, throwaway projection of that rkyv value,
shaped for emission. The pipeline is:

```
authored .schema (NOTA text)
   -> schema-next decode  -> SchemaSource / Schema   [rkyv, canonical, fz9n]
   -> LowerToRust          -> RustStruct/RustEnum/... [Rust-model, this repo]
   -> ToTokens + self.line -> RustCode (String)       [emitted text]
   -> prettyplease + fs    -> src/schema/*.rs          [checked-in artifact]
```

The report should not claim the de8i nouns are rkyv; they are the
emission model, and the rkyv image is one stage upstream. This is a
faithful reading of vez8 ("schema-in-Rust then LOWERS into rust interface
code") — the de8i nouns are the lowering's working set, not the canonical
round-trip image.

## 2. The lowering trait and the context-carrying wrappers

There are two trait layers, and they do different jobs.

### LowerToRust<Target> — source noun -> Rust-model noun

`LowerToRust<Target>` (`lib.rs:181`) is the recursive projection trait.
It is implemented FOR the schema-next source nouns, projecting them INTO
the Rust-model nouns:

```rust
pub trait LowerToRust<Target> {
    fn lower_to_rust(&self, context: &RustLoweringContext) -> Target;
}
```

For example `impl LowerToRust<RustStruct> for StructDeclaration`
(`lib.rs:802`) maps a source struct to a Rust-model struct, recursing
into each field. There are 13 mentions / impls of this trait. This is
the de8i "lowering is methods ON the schema objects" leg — each source
noun knows how to become its Rust-model counterpart; nothing is rerouted
through a central adapter. Note the direction: `LowerToRust` does NOT
produce tokens; it produces the model. Tokens come next.

### The *Tokens wrappers — Rust-model noun -> TokenStream via quote!

The model nouns themselves do NOT implement `ToTokens`. Instead, each is
wrapped in a context-carrying `*Tokens` struct that implements
`ToTokens`. A noun renders itself via `quote!`, e.g.
`RustStructTokens` (`lib.rs:2412`):

```rust
impl ToTokens for RustStructTokens<'_, '_> {
    fn to_tokens(&self, tokens: &mut TokenStream) {
        let attributes = self.context.data_type_attributes(self.structure.name());
        let visibility = self.context.visibility_tokens(self.visibility);
        let name = RustIdentifier::new(self.structure.name().as_str());
        let fields = self.structure.fields().iter()
            .map(|field| RustFieldTokens::new(field, self.visibility, self.context))
            .collect::<Vec<_>>();
        quote! {
            #(#attributes)*
            #visibility struct #name {
                #(#fields)*
            }
        }
        .to_tokens(tokens);
    }
}
```

`RustEnumVariantTokens` (`lib.rs:2537`) shows the alias/payload branch:

```rust
impl ToTokens for RustEnumVariantTokens<'_> {
    fn to_tokens(&self, tokens: &mut TokenStream) {
        let name = RustIdentifier::new(self.variant.name().as_str());
        match self.variant.payload() {
            Some(reference) => {
                let reference = RustTypeReferenceTokens::new(reference);
                quote! { #name(#reference), }.to_tokens(tokens);
            }
            None => quote! { #name, }.to_tokens(tokens),
        }
    }
}
```

### Why plain ToTokens was insufficient — the global-context problem

`quote::ToTokens::to_tokens(&self, &mut TokenStream)` has NO context
parameter. But three generation-wide decisions cannot live on the leaf
nouns without being duplicated into every one of them:

1. **The NOTA feature gate** (whether to emit
   `#[cfg_attr(feature = "nota-text", derive(NotaDecode, NotaEncode))]`).
2. **Private-type visibility** (a public field whose type is a private
   schema declaration must drop to `pub(crate)`).
3. **Map-key ordering derives** (a type used as a `BTreeMap` key earns
   `PartialOrd, Ord`).

The wrapper carries a `&RustRenderContext` (`lib.rs:925`) holding
`map_key_type_names`, `private_type_names`, and `nota_surface`. The
context owns the policy methods: `data_type_attributes`
(`lib.rs:944`), `derive_attributes` (`lib.rs:957`, which itself builds
the derive list with `quote!`), `visibility_tokens` (`lib.rs:1001`), and
`field_visibility_tokens` (`lib.rs:1008`, the private-type demotion).
This is the INTENT.md "context stays contextual while nouns own intrinsic
shape" rule (`INTENT.md:75-81`) made literal: the noun owns
name/fields/variants; the context owns the cross-cutting switches.

`field_visibility_tokens` is the cleanest example of why the context is
load-bearing (`lib.rs:1008`):

```rust
fn field_visibility_tokens(&self, visibility: Visibility, reference: &TypeReference) -> TokenStream {
    if visibility == Visibility::Public && self.references_private_type(reference) {
        quote! { pub(crate) }
    } else {
        self.visibility_tokens(visibility)
    }
}
```

A leaf `RustField` cannot know whether its referenced type is private —
that is a whole-module fact. The wrapper consults the context. Plain
`ToTokens` had no seat for that fact.

There are **28** `impl ToTokens` wrapper nouns (`lib.rs`, enumerated
2303-2548 for the declaration surface plus 1059-2286 for the runtime
surface) and **86** `quote!` call sites.

## 3. RustEmissionTarget and runtime_planes() — one schema, many targets

`RustEmissionTarget` (`lib.rs:409`) is the five-way switch that decides
which surfaces a single schema emits:

```rust
pub enum RustEmissionTarget {
    WireContract,     // external signal/meta-signal wire vocabulary + codecs only
    ComponentRuntime, // bootstrap all-in-one runtime (unsplit schemas)
    SignalRuntime,    // daemon-side Signal plane support
    NexusRuntime,     // daemon-side Nexus plane support
    SemaRuntime,      // daemon-side SEMA plane support
}
```

The target collapses to a `RuntimePlaneSet` via `runtime_planes()`
(`lib.rs:427`):

```rust
fn runtime_planes(self) -> RuntimePlaneSet {
    match self {
        Self::WireContract  => RuntimePlaneSet::none(),
        Self::ComponentRuntime => RuntimePlaneSet::all(),
        Self::SignalRuntime => RuntimePlaneSet::signal_only(),
        Self::NexusRuntime  => RuntimePlaneSet::nexus_only(),
        Self::SemaRuntime   => RuntimePlaneSet::sema_only(),
    }
}
```

`RuntimePlaneSet` is three booleans (`signal/nexus/sema`,
`lib.rs:439`). The same schema shape (imports, namespace, input, output)
is lowered identically; the target only gates the SUPPORT surfaces. You
see this in `RustModule::render()` (`lib.rs:238`): the declarations and
root enums always emit, then:

```rust
if writer.emits_short_headers() { writer.emit_short_headers(...); }
if writer.emits_signal()        { writer.emit_signal_frame_support(...); }
if writer.emits_runtime_support() {
    writer.emit_plane_route_support(...);
    writer.emit_trace_support(...);
    writer.emit_mail_event_support(...);
    writer.emit_plane_namespaces(...);
    writer.emit_plane_projection_support(...);
    writer.emit_runtime_role_trait_impls(...);
    writer.emit_schema_plane_trait_support(...);
    writer.emit_upgrade_support();
}
```

So `WireContract` (planes = none) emits only the data nouns + codecs;
`NexusRuntime` emits the Nexus envelope/route/trace/engine; the unsplit
`ComponentRuntime` emits all three planes plus the generic `Plane` enum.
This matches the lc2r/l6zw triad split: a `signal-<component>` contract
crate uses `WireContract`; the daemon's `nexus.schema` /`sema.schema`
use the per-plane targets. The spirit pilot still uses the all-in-one
bootstrap shape (its `schema/` has `signal.schema` + `nexus.schema` +
`sema.schema` as separate files but generated with runtime support), the
"named bootstrap exception" of l6zw.

`Plane` (`lib.rs:525`) deliberately owns ONLY plane-intrinsic names; the
three-tier boundary (`ARCHITECTURE.md:39-44`) keeps target selection out
of `Plane` and schema-presence checks on the writer. That boundary holds
in the code.

## 4. The artifact boundary: tokens -> prettyplease -> checked .rs

The single seam where tokens become text is `emit_item_tokens`
(`lib.rs:2883`):

```rust
fn emit_item_tokens(&mut self, tokens: TokenStream) {
    let file = syn::parse2::<syn::File>(tokens).expect("generated Rust item tokens parse");
    let source = prettyplease::unparse(&file);
    self.output.push_str(source.trim_end());
    self.output.push('\n');
}
```

Three things to notice, all consequential:

1. There is exactly **ONE** `prettyplease::unparse` in the whole crate
   (confirmed by grep: only `lib.rs:2885`). It runs **per item**, not
   once over the finished file.
2. It pushes the pretty-printed text into the SAME `output: String`
   buffer (`lib.rs:2669`) that the string path writes to via
   `self.line` (`lib.rs:2870`). The two emission styles are merged at the
   string level, not the token level.
3. The string path (`self.line`, `lib.rs:2870`) does NO formatting — it
   appends a raw line + `\n`. So hand-formatted strings are NOT
   prettyplease-normalized; whatever indentation the author typed is what
   lands.

The finished buffer leaves through `RustWriter::finish()` (`lib.rs:2879`)
as `RustCode`, and `build.rs` writes it to disk in
`GeneratedArtifact::write` (`build.rs:497-508`):

```rust
fn write(&self) -> Result<(), BuildError> {
    if let Some(parent) = self.path.parent() {
        fs::create_dir_all(parent)...?;
    }
    fs::write(&self.path, &self.content)...
}
```

with a freshness gate (`build.rs:472`): in check mode it compares the
freshly generated content against the committed file and errors with a
`StaleGeneratedArtifact` if they differ (naming the update env var); in
update mode it rewrites. This is the "source-visible generated
interfaces are reviewable / freshness-checked build artifacts" of
`INTENT.md:10-12`.

### Why build-time tokens into checked files beats inline proc-macro

The intent (4np2) is explicit that token-vs-string is the design axis and
checked-file-vs-inline is a SEPARATE visibility choice. This repo chose
checked files (`ARCHITECTURE.md:104-109`), and the reason is artifact
visibility (report 317 contention 2): the generated `src/schema/*.rs` is
a real reviewable file a human or future agent can open, diff, and
freshness-check, instead of expansion hidden inside the compiler. The
emitted `// @generated by schema-rust-next` header (`lib.rs:242`) and the
3002 lines of checked output across the spirit pilot
(`spirit/src/schema/sema.rs` 669, `nexus.rs` 802, `signal.rs` 1531) are
the payoff: the interface is inspectable without running `cargo expand`.

## The concrete text at each layer (spirit pilot)

### Input: authored .schema (NOTA) — spirit/schema/sema.schema:1

```
{
  Entry spirit:signal:Entry
  Query spirit:signal:Query
  ...
}
[WriteInput ReadInput]
[WriteOutput ReadOutput]
{
  WriteInput [(Record Record) (Remove Remove) (ChangeCertainty ChangeCertainty)]
  Record Entry
  ...
  ReadInput [(Observe Observe) (Lookup Lookup) (Count Count)]
  ...
}
```

This is the TRANSITIONAL pipe form, not the n2z3 at-binder form
(`Name@{...}` struct / `Name@(...)` enum). The square brackets
`[WriteInput ReadInput]` declare the input root pair; `[(Record Record)
...]` declares enum bodies. Per n2z3 the settled form is `Name@{...}` and
"pipe declaration forms are transitional" — this fixture has not yet
migrated. That is a real as-intended/as-implemented gap to flag.

### Output: token-emitted declaration surface — spirit/src/schema/sema.rs:25

```rust
#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum WriteInput {
    Record(Record),
    Remove(Remove),
    ChangeCertainty(ChangeCertainty),
}
```

This is `RustEnumTokens` -> `quote!` -> prettyplease. The
`#[cfg_attr]`+`#[derive]` two-attribute split and the exact spacing are
prettyplease's signature.

### Output: token-emitted runtime engine trait — spirit/src/schema/sema.rs:617

```rust
pub trait SemaEngine {
    fn on_start(&mut self) -> Result<(), ActorStartFailure> { Ok(()) }
    fn on_stop(&mut self) -> Result<(), ActorStopFailure> { Ok(()) }
    fn apply_inner(&mut self, input: sema::Sema<sema::WriteInput>) -> sema::Sema<sema::WriteOutput>;
    fn observe_inner(&self, input: sema::Sema<sema::ReadInput>) -> sema::Sema<sema::ReadOutput>;
    fn apply(&mut self, input: sema::Sema<sema::WriteInput>) -> sema::Sema<sema::WriteOutput> {
        let output = self.apply_inner(input);
        self.trace_sema_write_applied();
        output
    }
    ...
}
```

This is emitted by `SemaEngineTraitTokens` (`lib.rs:1715`, the
`emit_schema_plane_trait_support` token path) — so the engine traits, the
3d5z SEMA/Nexus/Signal separation surface, are ALREADY tokenized. Report
317 listed these as still-string; they have since moved.

### Output: STRING-emitted runner projection — spirit/src/schema/sema.rs / nexus runner

`emit_nexus_action_projection` (`lib.rs:4203`) builds the same kind of
Rust entirely with `self.line`:

```rust
self.line("impl nexus::Nexus<nexus::Action> {");
self.line("    pub fn into_sema_write_input(self) -> sema::Sema<sema::WriteInput> {");
self.line("        let origin_route = self.origin_route();");
self.line("        match self.into_root() {");
self.line("            NexusAction::CommandSemaWrite(input) => input.with_origin_route(origin_route),");
self.line("            _ => panic!(\"nexus action is not a SEMA write input\"),");
...
```

Functionally identical output, but hand-formatted strings with manual
indentation — the e6v5 "remaining string surface is transitional" debt.

## AUDIT CRITERION 2 — token-based vs string-based: PARTIAL / MID-MIGRATION

### Falsifiable grep counts (src/lib.rs unless noted)

| Marker | Count | Path |
|---|---|---|
| `quote!` | 86 | TOKEN |
| `impl ToTokens for` | 28 | TOKEN (wrapper nouns) |
| `TokenStream` | 39 | TOKEN |
| `LowerToRust` | 13 | TOKEN (model projection) |
| `format_ident!` | 0 | — |
| `proc_macro2` | 1 (import) | TOKEN |
| `syn::` | 2 | TOKEN (parse2 at the prettyplease seam) |
| `prettyplease` | 1 (`lib.rs:2885`) | TOKEN seam |
| `RustWriter` | 1 struct, 113 methods | STRING god-struct |
| `self.line(` | 200 | STRING |
| `format!` | 62 | STRING |
| `push_str` | 2 | STRING (buffer ops) |
| `write!`/`writeln!` | 7 | mixed (some in emitted code, not emission) |

`migration.rs` is a SEPARATE pilot emitter (UpgradeObject -> migration
module) that is still fully string-based: 0 `quote!`, 21 `format!`,
6 `self.line`. `build.rs` is the driver: 0 emission primitives.

### The split — exactly which sections are token vs string

Token-based (route through `*Tokens` wrappers via `emit_item_tokens`):

- All scalar/struct/enum/newtype/alias DECLARATIONS — `emit_type`
  (`lib.rs:2914`), `emit_root_enum` (`lib.rs:2973`).
- Signal-frame streaming support — `emit_signal_frame_streaming_support`
  (`lib.rs:3461`).
- Trace support + object-name enums — `emit_trace_support`
  (`lib.rs:3467`), `emit_object_name_enum` (`lib.rs:3515`).
- Mail event support — `emit_mail_event_support` (`lib.rs:3716`,
  2 token calls).
- Signal message root + mail lifecycle — `emit_signal_message_root_support`
  (`lib.rs:3761`), `emit_signal_mail_lifecycle_support` (`lib.rs:3766`).
- Plane envelope / namespaces / schema-plane enum —
  `emit_schema_plane_support` (`lib.rs:3773`), `emit_plane_envelope`
  (`lib.rs:3777`), `emit_plane_namespaces` (`lib.rs:3781`).
- Nexus runner next-step projection + adapter —
  `emit_nexus_runner_next_step_projection` (`lib.rs:4107`),
  `emit_nexus_runner_adapter` (`lib.rs:4112`).
- The Signal/Nexus/SEMA ENGINE TRAITS + actor lifecycle —
  `emit_schema_plane_trait_support` (`lib.rs:4681`, 3 token calls),
  `emit_actor_lifecycle_support` (`lib.rs:4731`).

String-based (still `self.line`/`format!`, the residual debt — 20
methods, `lib.rs`):

| Method | line | self.line | format! |
|---|---|---|---|
| `emit_signal_frame_impl` | 3340 | 44 | 13 |
| `emit_nexus_action_projection` | 4203 | 23 | 0 |
| `emit_signal_frame_support` | 3250 | 21 | 0 |
| `emit_split_nexus_work_projection` | 4117 | 21 | 6 |
| `emit_newtype_inherent_impl` | 2945 | 16 | 6 |
| `emit_nota_root_enum_support` | 3197 | 11 | 2 |
| `emit_upgrade_support` | 4497 | 10 | 0 |
| `emit_nota_inherent_bridge` | 3171 | 8 | 1 |
| `emit_nota_copy_inherent_bridge` | 3184 | 8 | 1 |
| `emit_route_impl` | 3316 | 8 | 5 |
| `emit_split_sema_output_projection` | 4250 | 6 | 1 |
| `emit_enum_payload_from_impls_for` | 3007 | 5 | 3 |
| `emit_enum_variant_constructors_for` | 3053 | 5 | 3 |
| `emit_route_enum` | 3298 | 4 | 2 |
| `emit_nota_support` | 2921 | 3 | 0 |
| `emit_short_headers` | 3234 | 3 | 2 |
| `emit_scalar_alias` | 2896 | 1 | 1 |
| `emit_imports` | 2904 | 1 | 0 |
| `emit_nota_gate` | 3228 | 1 | 0 |
| `emit_runtime_role_trait_impls` | 3938 | 1 | 1 |

Plus `rust_type` (`lib.rs:4781`), `constant_name` (`lib.rs:4798`),
`rust_method_name` (`lib.rs:4815`) which build small strings for the
above.

### Quantified residual string surface

- **1** `RustWriter` god-struct (`lib.rs:2668`) with a `String`
  accumulator and **113** methods.
- **200** `self.line(...)` call sites and **62** `format!(...)` call
  sites, concentrated in the **20** methods above.
- The heaviest single string debt is the **signal-frame binary
  encode/decode codec** (`emit_signal_frame_impl`, 44 self.line + 13
  format!) and the **split-plane projection family**
  (`emit_nexus_action_projection` + `emit_split_nexus_work_projection` +
  `emit_split_sema_output_projection`, ~50 self.line combined), i.e. the
  hyng/7ca4 runner/NexusAction-projection surface.

### Verdict

**partial-mid-migration**, and notably FURTHER along than report 317
described. Report 317 had the declaration surface tokenized but
runtime/support (plane routes, trace names, runner projection, engine
traits) still on RustWriter. As of the current tree, the **engine traits,
trace support, object-name enums, plane envelopes/namespaces, mail
lifecycle, runner next-step projection AND adapter** have ALL moved to
the token path. The residual string surface is now narrower: the
signal-frame binary codec, the cross-plane `into_*` projections, the NOTA
inherent bridges + root-enum support, the route enums, enum constructors,
newtype inherent impls, upgrade support, scalar alias + imports. The
single string buffer at `RustWriter.output` (`lib.rs:2669`) is the
remaining seam; once the 20 methods are tokenized, `RustWriter` collapses
to a token-collector and the `self.line`/`format!` surface goes to zero.

This matches the psyche standard exactly: 4np2 ("the hand-rolled string
emitter ... is replaced ENTIRELY") is the DESTINATION; e6v5 / o7a3 / 0bw0
("mid-migration ... remaining string surface is transitional, the
direction is DECIDED") is the CURRENT STATE. The code is honestly
mid-stream, with the harder-to-tokenize runtime pieces (binary codec,
panicking projections) left for last.
