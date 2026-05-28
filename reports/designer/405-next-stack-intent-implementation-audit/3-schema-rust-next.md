# 405/3 — schema-rust-next: intent↔implementation audit

*Kind: Sub-agent audit (Layer 2, Rust emission) · Topics: schema, nexus,
sema, signal, emission, mirror-naming, audit · 2026-05-28 · Read-only*

*Pinned `main` `68559f86311bffb341e7cf1b3663e5ef0c123403` ("emission:
emit schema-plane engine traits"). HEAD confirmed equal — no repo drift.
One build-graph drift worth flagging up front: `Cargo.lock` pins
`schema-next` at `807c5250c313e0dbedf0e4d2dbc41cb97116a44e`, but the
meta-report frame and the canonical `schema-next` checkout are at
`e0681f2`. The emitter therefore builds against an OLDER `schema-next`
than the sibling audit measures. `cargo test` passes (10/10) against the
locked rev.*

## Verdict

The emitter does the load-bearing thing intent asks: it is a genuine
text-emission step (`RustEmitter::emit` builds a `String` via a
`RustWriter`, consuming `schema_next::Asschema`), it produces real
data-bearing nouns (structs/enums with rkyv derives, not stubs), and the
GENERATED code is rigorously method-only — every generated `fn` lands
inside an `impl` block of the owning struct/enum, there is not a single
free helper in `spirit_generated.rs`. The pinned commit adds the two
schema-plane engine traits (`NexusEngine`, `SemaEngine`), so the
three-plane-trait intent is now PARTIAL-moving-to-MET. The real gaps are
in **mirror naming** (the headline gap: the emitter mirrors the schema
namespace into the FILE PATH only — type references are emitted by bare
local name, `imports()` is dead, so a cross-namespace `schema:spirit:Entry`
could never become `spirit::Entry` in emitted Rust), and in **plane
fidelity** (the three "engine" traits are shallow single-method shims that
do not match the richer per-variant Nexus dispatch the same file already
proves for the Signal roots; SEMA gets a trait but no dispatch/translation
surface, and Nexus's translator role — Signal↔SEMA — is unmodelled). The
emitter's OWN source has one method-discipline smell (a ZST-flavoured
helper pair on `RustWriter`) but no hard free-function violation.

## Per-item classification

### Item 1 — Schema-emitted types are the Rust nouns (records 947/954/945) — MET

The emitter produces data-bearing types, not stubs. Structs:
`src/lib.rs:269-280` (`emit_struct`) emits `pub struct X { pub field: T,
... }` with the rkyv derive line at `:270`. Newtypes:
`src/lib.rs:259-267`. Enums: `src/lib.rs:282-289`. Root input/output
enums: `src/lib.rs:291-298`. The fixture confirms the output is real
nouns: `Entry`/`Query`/`RecordSet` structs and `Kind`/`Magnitude` enums
at `tests/fixtures/spirit_generated.rs:116-175`, with `Input`/`Output`
root enums at `:165-175`. Behaviour is attached as methods/traits on
these nouns (NOTA conversion `:177-395`, signal frame `:441-539`, Nexus
trait + dispatch `:646-686`, upgrade `:688-700`). This is exactly the
"schema is the noun, hand-written Rust is the verb" shape. The one caveat
is scope: only `Text`/`Integer` scalars are handled (`rust_type`
`src/lib.rs:869-875`); any other scalar floor type intent later names
(record 1007's `DatabaseMarker`, etc.) is passed through as a bare type
name with no special handling, which is correct for user-declared nouns
but means the emitter has no built-in scalar vocabulary beyond two types.

### Item 2 — Mirror naming (records 902/909/952) — PARTIAL (the headline gap)

Two halves; they diverge sharply.

**File-path half — MET.** `RustModulePath` (`src/lib.rs:82-114`) takes the
schema identity's component `Name`, splits on `:` via
`namespace_segments()` (`schema-next` `asschema.rs:15-17`), drops the
first (crate) segment (`src/lib.rs:104-108`), snake-cases the rest
(`field_name()`, `:111`), and lands `src/schema/<…>.rs`
(`:92-100`). Proven by `emitted_path_mirrors_schema_module_identity`:
`spirit-next:signal:public` → `src/schema/signal/public.rs`
(`tests/emission.rs:50-61`). Matches record 909 exactly.

**Type-reference half — MISSING.** The colon→`::` mirror does NOT reach
emitted type references. `rust_type` (`src/lib.rs:869-875`) renders every
`TypeReference` as its bare name (`name.to_owned()`, `:873`); there is no
namespace qualification, no `::` segment emission anywhere except the
hardcoded `std::`/`nota_next::`/`rkyv::` library paths inside emitted
string literals. Decisively: `Asschema` carries `imports: Vec<
ImportDeclaration>` with `{ local_name, source: TypeReference }`
(`schema-next` `asschema.rs:53,80-82,107-111`), but the emitter NEVER
calls `asschema.imports()` — grep of `src/lib.rs` shows zero references.
So a schema that imports `schema:spirit:Entry` from another namespace has
no path by which the emitter could produce `spirit::Entry`; it would emit
a bare `Entry` and rely on it being in-module. The mirror property record
952 calls "load-bearing for navigability" holds for FILES but breaks for
the cross-module TYPE identifiers that navigability actually needs. No
test exercises a multi-namespace schema, so the gap is untested as well
as unimplemented. This is the single most consequential gap in the repo.

### Item 3 — Three-plane engine traits (pinned commit; records 964/967/968) — PARTIAL

The pinned commit adds `emit_schema_plane_trait_support`
(`src/lib.rs:823-836`), gated on type presence via `has_type`
(`:838-842`). When the namespace declares `NexusInput`+`NexusOutput` it
emits `pub trait NexusEngine { fn execute(&self, input: NexusInput) ->
NexusOutput; }` (`:824-829`); when it declares `SemaInput`+`SemaOutput` it
emits `pub trait SemaEngine { fn apply(&mut self, input: SemaInput) ->
SemaOutput; }` (`:830-835`). Proven by
`emits_schema_plane_engine_traits_for_declared_nexus_and_sema_languages`
(`tests/emission.rs:63-109`). So the traits are REAL and DISTINCT per
plane (distinct names, distinct method names `execute` vs `apply`,
distinct receiver `&self` vs `&mut self` — a nice touch: SEMA mutates
durable state, Nexus does not). This is a genuine step toward record 964's
"each plane has its own engine with its own traits."

But three shortfalls keep it PARTIAL, not MET:

1. **No SIGNAL engine trait.** Intent (record 964 table, workspace
   `INTENT.md:312-316`) names THREE planes each sharing
   "input-message-in, output-message-out." The emitter emits engine
   traits for only TWO (Nexus, Sema). The Signal plane gets the rich
   `*Nexus` dispatch trait + signal-frame machinery instead, so Signal is
   not left empty — but there is no `SignalEngine`-shaped
   `Input→Output` trait that parallels the other two. The symmetric
   "three engines, same pattern" framing (record 982,
   `INTENT.md:333-341`) is only two-thirds emitted.

2. **The two new traits are shallow shims, inconsistent with the file's
   own richer pattern.** `NexusEngine::execute` is one opaque
   `NexusInput → NexusOutput` method. Yet the SAME emitter already proves
   a far richer Nexus surface for the Signal roots: `emit_nexus_trait`
   (`src/lib.rs:759-778`) emits `InputNexus` with ONE METHOD PER VARIANT
   (`fn record(...)`, `fn observe(...)`,
   `tests/fixtures/spirit_generated.rs:646-652`) plus a
   `dispatch_mail_with_nexus` dispatcher (`:654-665`). Workspace
   `INTENT.md:17-21` says runtime engines implement Nexus traits "with one
   method per reaction variant." The new `NexusEngine` trait contradicts
   that: a single `execute` over an opaque input enum, no per-variant
   methods, no dispatch helper. So the repo now carries TWO different,
   unreconciled notions of "Nexus trait" — the per-variant `*Nexus`
   (record-faithful) and the monolithic `NexusEngine` (the pinned-commit
   shim). The shim does not return populated reply objects through the mail
   types (`NexusMail`/`MessageProcessed`); it bypasses them.

3. **Nexus's TRANSLATOR / mail-keeper role is unmodelled in the new
   traits.** Record 968 / 970 (`INTENT.md:359-386`) make Nexus the thing
   that translates Signal→SEMA inbound and SEMA→Signal outbound and holds
   the in-flight mail. `NexusEngine::execute(NexusInput) -> NexusOutput`
   is a single black-box step with no translation surface, no mail
   lifecycle, no SEMA hand-off. The mail machinery that WOULD support this
   (`NexusMail<Payload>`, `MessageProcessed<Reply>`,
   `tests/fixtures/spirit_generated.rs:557-567,590-624`) exists but is
   wired to the `*Nexus` dispatch path, not to `NexusEngine`. The two
   surfaces are not connected.

`ARCHITECTURE.md:50-53` and `INTENT.md:41-47` document the new traits
accurately, so the docs are honest about what was built — but neither
flags the unreconciled-double-Nexus or the missing Signal engine.

### Item 4 — Method-only Rust, no ZST holders, no free functions (records 712/882/881)

Two surfaces to audit: the GENERATED code, and the EMITTER's own source.

**Generated code — MET (strict).** Every `fn` in
`tests/fixtures/spirit_generated.rs` is inside an `impl` of a named
data-bearing type or a trait. NOTA conversion methods live on the nouns
(`impl Topic` `:177`, `impl Entry` `:217`, `impl Kind` `:267`, etc.).
Signal-frame methods on the root enums (`impl Input` `:441`). Nexus trait
+ dispatch on the noun (`:646-665`). Upgrade traits `:688-700`. The one
construct that could read as a "namespace" — `pub mod short_header`
(`:397-402`) — holds only `pub const` values, not functions, so it is a
constant namespace, not a free-function holder; that is legitimate and not
a method-discipline violation. No free `fn` exists anywhere in the
generated output. This is a strong result: the schema-emitted code obeys
the Maximum-certainty rule it is most likely to be judged on.

**Emitter source — PARTIAL (one smell, no hard violation).** All emitter
logic lives in methods on `RustEmitter` (`src/lib.rs:33-80`), `RustWriter`
(`:121-893`), or `RustModulePath` (`:87-114`) — all NON-zero-sized
(`RustWriter` owns `output: String` `:118`; `RustModulePath` owns
`schema_name: Name` `:84`; `RustEmitter` owns `generator_name` `:22`). So
there is no free function and no ZST method holder at the struct level.
The smell: the pinned commit's `has_type` (`:838-842`) and `type_name`
(`:844-851`) are methods on `RustWriter` that read `&self` but use NOTHING
from `self` — they operate purely on the `declarations` argument. They are
free functions wearing a method's coat. By the test in the workspace
override ("does the helper's job vanish if you erase the owning type from
the type system?"), `type_name` in particular is a pure
`&TypeDeclaration -> Name` projection that belongs as
`impl From<&TypeDeclaration> for Name` or as a method ON `TypeDeclaration`
in `schema-next` (where `TypeDeclaration::name()` ALREADY EXISTS —
`schema-next` `asschema.rs:120-127` — making the emitter's `type_name` a
duplicated re-implementation of an upstream method). `has_type` similarly
wants to be `impl`-located on a namespace/declaration-slice noun. Not a
hard free-function violation (they are technically methods), but they
violate the spirit of records 712/882 and duplicate upstream behaviour.
See Item 5 for the related `From` point.

### Item 5 — Projection/conversion uses `impl From` (record 882) — PARTIAL

**Generated conversions — MET-by-absence.** The generator does not emit
free `fn project_x_to_y`. The cross-type conversions it emits are the
upgrade traits (`UpgradeFrom<Previous>` / `AcceptPrevious<Previous>`,
`tests/fixtures/spirit_generated.rs:688-700`) — which are deliberately a
fallible `Result`-returning trait, not infallible `From`, and that is
defensible since schema upgrades can fail (`type Error;` `:689`).
NOTA parse/format are methods on the nouns, not free projections. So
nothing in the GENERATED output violates the `From` preference.

**Emitter-internal projection — PARTIAL.** `RustWriter::type_name`
(`src/lib.rs:844-851`) is exactly the projection shape record 882 says to
express as `impl From`: it maps `&TypeDeclaration -> Name`. It is written
as an ad-hoc method that re-derives what `schema-next`'s
`TypeDeclaration::name()` already returns. The record-882-faithful form is
to call the upstream `declaration.name().clone()` (one method, already
exists) or, if a distinct owned projection is wanted, `impl From<&
TypeDeclaration> for Name`. Minor, internal, but it is a real instance of
the anti-pattern the record names.

### Item 6 — Separate text step, not an in-place proc-macro (active-repos role) — MET

`RustEmitter::emit` (`src/lib.rs:41-79`) constructs a `RustWriter`
(`:42`), appends lines into an owned `String` (`RustWriter::line`
`:122-125`), and returns `RustCode(String)` (`:78`). `emit_file`
(`:34-39`) wraps it with the mirrored path into `GeneratedFile { path,
code }` (`:5-9`). The output is SOURCE TEXT. The crate is a plain `[lib]`
(`Cargo.toml:11-13`) with NO `proc-macro = true`, and
`ARCHITECTURE.md:16-17` states the constraint "No `macro_rules!` or
proc-macro surface in `src/`" — confirmed by grep (none present). The
`examples/emit_schema.rs` binary prints the generated source to stdout
(`:19`) for a consumer to refresh its checked-in `src/schema/<mod>.rs`,
matching record-909 source-visible-emission intent. This is squarely a
separate-text-step-before-macros design, exactly as the role demands.

## Cross-cutting observations

- **The input fixture and the engine-trait test use DIFFERENT schemas.**
  `tests/fixtures/spirit-min.schema` declares no Nexus/Sema types, so the
  committed `spirit_generated.rs` fixture contains NO `NexusEngine` /
  `SemaEngine` (confirmed: absent from the 701-line fixture). The
  three-plane traits are proven ONLY by an inline-source test
  (`tests/emission.rs:63-109`) that is NOT round-tripped through the
  compiled-fixture path. So the engine traits are asserted to be EMITTED
  as text, but never COMPILED as Rust the way the signal/nexus/upgrade
  surfaces are (`compiled_fixture_is_usable_rust` `:111-129` only covers
  the min fixture). Per the meta-report's record-1006 "tests prove not
  pretend" yardstick, the engine traits sit at the weaker "string
  contains" proof tier, not the "compiles and runs" tier the rest of the
  emitter reaches.
- **`SemaEngine` exists but the SEMA plane has no dispatch / no DB-work
  surface.** Record 1007 (`INTENT.md:343-349`) says real SEMA is durable
  database writes. The emitter gives SEMA a single `apply(&mut self,
  SemaInput) -> SemaOutput` (`src/lib.rs:830-835`) — appropriate as a
  minimal language surface, but there is no per-variant dispatch, no
  durable-marker handling, no notion that `apply` writes state. That is
  acceptable at Layer 2 (durability is the daemon's job), but the trait as
  emitted gives the daemon no schema-emitted hook to hang single-writer
  durability on beyond the opaque method.
- **`Input`/`Output` are the literal root names; no `signal:`
  namespacing.** The min fixture's roots are bare `Input`/`Output`
  (`tests/fixtures/spirit_generated.rs:165-175`). The mirror-naming intent
  (record 902) anticipates roots like `spirit-next:signal:Frame`. Since
  the emitter drops the crate segment and never qualifies type refs, all
  roots collapse to bare local names in a flat module — fine for a
  single-namespace pilot, but it is the same untested-multi-namespace gap
  as Item 2 viewed from the root-enum side.

## Top gaps (ranked)

1. **Mirror naming reaches files but not type references; `imports()` is
   dead code.** `rust_type` emits bare names (`src/lib.rs:873`) and
   `asschema.imports()` is never consumed, so cross-namespace
   `schema:spirit:Entry → spirit::Entry` is impossible. The
   navigability property record 952 calls load-bearing is half-built and
   wholly untested for the multi-namespace case. (Item 2)

2. **Two unreconciled notions of "Nexus trait."** The record-faithful
   per-variant `*Nexus` + `dispatch_mail_with_nexus`
   (`tests/fixtures/spirit_generated.rs:646-665`) coexists with the new
   monolithic single-method `NexusEngine` (`src/lib.rs:824-829`), which
   contradicts `INTENT.md:17-21`'s "one method per reaction variant" and
   bypasses the mail types. Pick one shape, or state how they compose.
   (Item 3.2)

3. **No `SignalEngine`; three-plane symmetry is two-thirds emitted.** The
   "three engines, same input→output pattern" intent (record 964/982,
   `INTENT.md:312-341`) emits engine traits for Nexus and Sema only.
   (Item 3.1)

4. **Engine traits proven only at the string-contains tier.** They are
   not in the compiled fixture and never exercised as real Rust
   (`tests/emission.rs:63-109` vs the compiled path `:111-129`),
   falling short of the record-1006 "prove not pretend" bar. (Cross-cutting)

5. **Nexus's translator/mail-keeper role is absent from the new traits.**
   `NexusEngine::execute` is a black box with no Signal↔SEMA translation
   or mail lifecycle, though the supporting mail nouns exist unused-by-it
   (records 968/970, `INTENT.md:359-386`). (Item 3.3)

6. **Emitter-internal `type_name`/`has_type` are free-functions-as-methods
   and duplicate `schema-next`'s `TypeDeclaration::name()`** (`src/lib.rs:
   838-851` vs `schema-next` `asschema.rs:120-127`). Minor, but a real
   instance of the record-712/882 anti-pattern inside the emitter itself;
   `type_name` wants to be the upstream method or an `impl From`. (Items 4-5)

7. **Build-graph drift:** `Cargo.lock` pins `schema-next` `807c525` while
   the canonical checkout / sibling audit is at `e0681f2`. The emitter is
   validated against an older lowering layer than the one being audited
   next door. (Front-matter)
