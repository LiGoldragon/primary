# Stream construct — how the subscription kind enters core-schema's ruled kind system (design proposal v1)

Design-authority document. Session `LanguageEngine`, lane `StreamConstructDesign`,
Fresh, generalist, Opus 4.8 (1M), 2026-07-18. Read-only on every engine repo; this
file, the tracker slice it registers, and this lane's own directory are the only
writes. The psyche does not read reports — the chat return is his surface; this file
is the agent pickup point. He rules on syntax and kind-system shape personally; §7
is the numbered decision set the manager presents from chat alone.

Provenance markers: **[observed — cite]** = a code fact read this pass; **[ruling]** =
a settled psyche decision carried from `textual-form-vision-design-v2.md` /
`up-close-design-v1.md`; **[reconciled]** = this document's design move inside the
rulings; **[DECISION n]** = a joint returned to the manager, never asked of the
psyche directly.

## 0.0 Ruling capture and supersession (2026-07-18, lane StreamRulingsCapture, Opus 4.8)

The psyche graded the four §7 decision items (chat, epic `primary-56d1.48`). His words
are verbatim and are the source of truth; this section **supersedes** the sections named
below. The original proposal (§0–§9) is kept as the agent pickup context, but where §0.0
and a later section conflict, §0.0 governs.

### Ruling A — the kind-system seat, and the MECHANISM it names (supersedes §2 and §7 [DECISION 1])

Psyche verbatim: **"thats the power of nomos; just create a new kind of object"**.

This is more than a seat choice. It **accepts that Stream is a new *declaration* kind** —
resolving [DECISION 1] against the reference-position options (a)/(b) and onto the
declaration-kind family (the §2.3 (c) direction). And it **names the mechanism**: new kinds
of objects are minted **through Nomos** — the language grows its kind vocabulary via the
macro / transformation layer (the dialect-as-macro-package lineage tracked on
`primary-56d1.2`), **not** through hand edits to core Rust. **Stream is the first
Nomos-minted object kind.**

**The honest bootstrap tension (returned, not resolved).** Today the kind vocabulary is a
set of **closed Rust enums, deliberately closed** to preserve static exhaustiveness and
disjointness:

- **[observed — `core-schema/src/declaration.rs:224`]** `CoreType { Newtype | Struct |
  Enumeration }` — a closed enum, matched exhaustively with no wildcard everywhere it is
  used (`identifier`, `constructor_count`, `restamp`, the textual reflect/reify paths).
- **[observed — `core-schema/src/universe.rs:30-52`]** `MemberKind { ScalarLeaf | Field |
  Declaration(CoreDeclaration) }`, whose `constructor_count` funnels through the closed
  `CoreType`.
- **[observed — `core-nomos/src/identity.rs`]** `SectionDefault { Newtype | Struct |
  Enumeration }` with `of_core_type` **exhaustive over `CoreType`, no wildcard** — its own
  doc-comment: *"a new declaration kind is a compile error until its section is named"*.
  `MacroKind { Named | Structural(SectionDefault) }` is closed to *"exactly two"* per a
  prior ruling.

So "just create a new kind of object via Nomos" cannot be honoured today without editing
these closed Rust surfaces. The design question is therefore: **what minimal hook must
core-schema / core-nomos provide so Nomos can *mint* a new declaration kind, versus what a
Nomos package supplies?** — returned as [DECISION A1]/[A2] below. This is a change to the
**kind-system schema/topology** and is therefore gated on explicit psyche design acceptance
before any implementation (authority boundary); this pass captures the ruling and the
minimal-hook options, and implements nothing.

The invariant that must survive whatever mint mechanism is chosen: **kind identity minted
through the central authority** (kinds allocated like the central-authority-assigned type
ids of `CoreUniverse::from_assignment`, not by parse order), **static disjointness preserved**
(`validate_disjoint` must still prove every declaration-body form provably disjoint at seal
time), and the **structuretree forms supplied** for the new kind (its `ConstructorCodec`
decode/encode forms, §6) rather than special-cased in the codec.

### Ruling B — role modeling (supersedes §3 and §7 [DECISION 2])

Psyche verbatim: **"whatever"** — indifference. The recommendation therefore **stands as
accepted-by-indifference**: **four named typed fields** (`token opened event close`), the
closed role vocabulary living in the field set, lowering dispatching on the field, never on
a role-name string. Recorded status: **agents' choice, psyche indifferent** — not a
positive endorsement, but the agents are free to proceed with (i) and did.

### Ruling C — the spelling was REJECTED as invalid syntax (supersedes §4 and §7 [DECISION 3])

Psyche verbatim: **"that's invalid syntax. the types are different so naming them must be an
error"**.

**Manager's reading [manager interpretation — then checked against fixtures + codec below]:**
explicit field names are legal **only** where two or more fields in the block **share a
type** (elision would otherwise collide); **naming a field whose type is unique in the block
is an ERROR, not a style choice.** The role name is a disambiguator, never decoration.

**Fixture check [observed — `core-schema/tests/textual_roundtrip.rs:76`,
`core-schema/src/fixture.rs`]:** the delivered `DatabaseMarker` fixture
`DatabaseMarker.{ CommitSequence StateDigest secretDigest.StateDigest }` **already obeys the
law at the value level.** `CommitSequence` is unique → elided. `StateDigest` appears twice
(second and third fields both of type `StateDigest`); the second elides to its derived name
`state_digest`, the third carries the explicit name `secretDigest` — the *only* explicit
name in the block, and it sits on a field whose type collides. So the fixture is a valid
witness under the ruled law and needs no change.

**Corrected Stream spelling (seated, superseding §4 / §7 [DECISION 3]):**

```
IntentEventStream.Stream.{ token.SubscriptionToken SubscriptionStarted IntentEvent close.SubscriptionToken }
```

The two uniquely-typed legs **lose their labels** — `opened.SubscriptionStarted` becomes
bare `SubscriptionStarted` and `event.IntentEvent` becomes bare `IntentEvent`; their core
field names become the type-derived names (`subscription_started`, `intent_event`). The two
colliding `SubscriptionToken` legs **keep explicit names** (`token`, `close`) because the
collision requires distinguishing them. **Role semantics are carried by the Stream kind's
structure — the fixed slot order of the four legs — never by magic recognition of the label
strings.** (This tightens Ruling B: the four fields remain named *typed slots* in Core, but
their **text** may only spell a name where collision forces it.)

**Codec verification against delivered decode/encode [observed — `core-schema/src/textual.rs:193-314`,
`core-schema/src/declaration.rs:403-415`]: the delivered codec DIVERGES from the ruled law.**
The elision predicate is `CoreField::name_is_derivable` = `stored_name == reference.derived_field_name`
— a pure **name-equals-derived** test with **no block-level type-multiplicity check**:

- **Decode** (`reify_field`, `textual.rs:217-227`): the explicit-name alternative
  `Application(Atom(name), Atom(type))` is accepted **unconditionally**; the codec **does
  not** reject a superfluous explicit name on a uniquely-typed field. `Config.{ retries.Integer }`
  (or `Stream.{ opened.SubscriptionStarted … }`) decodes today with no error.
- **Encode** (`reflect_field`, `textual.rs:301-312`): emits the explicit form whenever
  `name_is_derivable` is false, again with **no collision check** — a Core struct holding a
  non-derived name on a uniquely-typed field **encodes to** the exact spelling the psyche
  ruled invalid.

The divergence is one-directional and clean: **the codec is more permissive than the ruled
law** — it accepts and emits explicit names on uniquely-typed fields. If the manager reading
survives the psyche's review (see the open veto below), the codec's elision rule must become
**collision-aware**: explicit text names legal only where a type is shared in the block;
`name_is_derivable` gains block context, and decode rejects a redundant explicit name. This
is registered as an implementation work item on `primary-56d1.48`, gated on C surviving.

**Open veto surfaced in chat.** The manager reading has a real consequence the psyche may
reject: it forbids giving a *meaningful custom name* to a single field of an otherwise-unique
type (`count.Integer` would be illegal, forced to bare `Integer` → derived `integer`). Whether
that is intended or the law should instead be "names are always legal but redundant ones are
discouraged/normalized" is the psyche's to settle. Until he confirms, **Ruling C stands as
the manager reading, subject to his veto**; the codec work item does not land until he
confirms the law.

### Item D — the close-leg question is OPEN, not a ruling

Psyche verbatim on the close-leg / `close`-mandatory-vs-defaulted question ([DECISION 4]):
**"I dont follow all that."** This is a **lost-understanding signal, NOT a ruling.** The
question (is `close` a mandatory explicit role, or does it default to `token`'s type when
elided; and the broader close-leg semantics) has been **re-grounded to the psyche in chat**
and **stays OPEN** on `primary-56d1.48`. Nothing is resolved here. [DECISION 4] remains open
and is folded into Item D.

### Ruling E — field names are illegal EVERYWHERE (2026-07-19, supersedes the collision-name clause of Ruling C and Item D's naming reasoning)

Psyche verbatim: **"field names are now COMPLETLY ILLEGAL EVERYWHERE"**, with the
authorization **"create a deterministic rule for structs that contain more than one field
with the same type"**.

This **abolishes the collision-aware elision law** that Ruling C stood on. Ruling C's
manager reading kept explicit names legal *where a type is shared in the block* — the two
colliding `SubscriptionToken` legs kept the names `token` / `close`; the `DatabaseMarker`
fixture kept `secretDigest`. That entire clause is **superseded**: no field name is ever
emitted, accepted, or represented in any Protos textual surface. The collision case that
Ruling C treated as the *one* place a name was forced is now handled the deterministic way
the psyche authorized — **by position alone**: a struct's fields are positional slots typed
by the expected type at each position (the `PositionalSignature` machinery already present
in the structuretree), and two fields of the same type are told apart by their order, never
by a name. It also **supersedes Item D's naming reasoning** insofar as Item D reasoned about
`close` as a *named* leg distinguished from `token` by its label; under Ruling E a leg can
never be distinguished by a label.

**[reconciled — implemented this pass, lane `FieldNameBanCodec`, bead `primary-56d1.40`]** The
new-engine codec now enforces this: encode never writes a field name; decode rejects any
explicit `name.Type` as illegal Protos; the `Field` meta-type carries one positional
constructor; the `enforce_elision_law` / `field_types_share_names` / `SuperfluousName`
apparatus is deleted. The `DatabaseMarker` fixture is now
`DatabaseMarker.{ CommitSequence StateDigest StateDigest }` (its two `StateDigest` fields
told apart by position), and the logos `Newtype` witness — two `Visibility` fields
(`visibility`, `wrapped_visibility`) at positions 0 and 3 — round-trips purely positionally.
core-schema 0.3.0, `nix flake check` green; core-logos re-pinned and green.

**Stream spelling under Ruling E (superseding Ruling C's corrected spelling).** The two
`SubscriptionToken` legs lose their `token` / `close` labels too — the earlier "colliding
legs keep explicit names" carve-out is gone. Their disambiguation must come from the
Stream kind's fixed slot order alone, OR from the legs being different types (see Ruling F).
Stream is **not implemented** this pass; this only records how the abolition reshapes its
spelling.

**Downstream tension surfaced (NOT resolved here).** A struct whose two same-typed fields
lower to Rust needs two *distinct* Rust field names, but positional decode derives the same
name from the type for both (`state_digest`, `state_digest`). Rust codegen cannot emit two
fields of the same name. The ruling settles the Protos/Core level (position is meaning) but
leaves the schema→Rust field-naming decision for same-typed fields OPEN — the psyche resolved
this for the specific Stream case in Ruling F (give the colliding leg its own type). The
general case is registered as a Nomos-lowering question, not invented here.

### Ruling F — the stream close leg exists, as an event (2026-07-19, settles Item D / [DECISION 4])

Psyche verbatim: **"and yes, we should have a stream close event"**.

This **closes Item D / [DECISION 4]**, which stood OPEN on the lost-understanding signal
"I dont follow all that." The close leg **exists**, and it is an **event** — a member of the
stream's event flow, not a bare token echoed back. Its own event **type** is therefore
distinct from the subscription `token` type, which **dissolves the `token` / `close`
same-type collision** that forced the two-name carve-out in Ruling C: once `close` is its
own event type, the two legs are no longer the same type, so nothing positional-or-otherwise
needs to disambiguate two `SubscriptionToken` legs — there are none. This is the same "make
the colliding fields different types" move that resolves Ruling E's downstream tension for
this concrete construct.

Stream remains **design-blocked and unimplemented** (Ruling A's Nomos-mint mechanism is still
gated on psyche design acceptance); this records only that the close leg is settled as an
event with its own type.

### Deterministic same-typed-field rule — DIRECTED-WORK DELIVERY (2026-07-19, lane DeterministicFieldRule, Opus 4.8, general-code-implementer)

Psyche verbatim (the directive this delivers): **"OUTRIGHT FORBID FIELD NAMES, and create a
deterministic rule for structs that contain more than one field with the same type"**. Ruling
E (above) delivered the forbid half and **explicitly left the create half open** — its
"Downstream tension surfaced (NOT resolved here)" clause (a struct's two same-typed fields
lower to Rust needing two *distinct* Rust field names, but positional decode derives the same
name for both) registered the general schema→Rust field-naming question as a Nomos-lowering
decision "not invented here." This entry records the delivery of that create half. **It is
directed work, not a psyche ruling on the rule's *form*: the psyche authorized that a
deterministic rule exist and be created; his review of this particular rule shape is pending.**

**The rule (one sentence).** A struct field's Rust name is the `snake_case` of its type, and
when a type names more than one field in that struct, each such field is distinguished by
prefixing the **ordinal English word of its position among the same-typed fields**
(`first_state_digest`, `second_state_digest`, …), a type naming a single field keeping the bare
base name as the degenerate empty-ordinal case rather than a separate branch.

**Why this shape.** Judged against the psyche's design values. *Special case dissolves:* the
singleton `commit_sequence` is not a side branch but the empty-ordinal identity of the one
disambiguation — the rule is uniformly "qualify each member of a same-type group by its ordinal
position," and a group of size one has an empty qualifier, exactly as English omits "first" when
there is only one door. *Full English words:* ordinals are spelled `first`/`second`/`twenty_third`
(cardinal words with the final word ordinalized: `twenty` → `twentieth`, `three` → `third`), so
the mapping is **total over `usize` and never falls back to a numeral** like `_2`. *Mechanism
over cleverness:* it is a pure function of field **position and type** — no stored or authored
name is read (honoring the field-name ban), the same struct always lowers to the same names, and
adding a later field of another type never moves an earlier field's name. Prefix (not suffix)
follows English word order and reads decently in real Rust field access.

**Where it lives — Nomos lowering, not core-schema.** The stringless positional substrate
deliberately carries **no** field names (that is the whole of Ruling E); manufacturing distinct
identifiers is purely a property of lowering to a **name-bearing target** (Rust), which NOTA's
positional surface never needs. So core-schema stays untouched at `2e47dec5`; its per-field
`CoreReference::derived_field_name` supplies the base name, reused. The rule is new in
**core-nomos** (`Evaluator::derive_group_names` computes the group's names; the `SameTypeOrdinal`
newtype spells the ordinal word; `field_name` now takes the pre-computed group name). This also
keeps Ruling E's "position is meaning" invariant intact at the Core level while resolving its
downstream general case at the lowering boundary — the same "make distinct identifiers only
where a named target forces it" move.

**Real `DatabaseMarker` proof (verbatim from code output, not hand-mocked).** Input positional
schema text decoded through `TextualSchema::fixture`:
`DatabaseMarker.{ CommitSequence StateDigest StateDigest }`. Derived Rust field names:
`commit_sequence` (unique → bare), `first_state_digest` + `second_state_digest` (the two
`StateDigest` fields, ordinal-disambiguated). Emitted Rust (wire preamble), exactly as the
pipeline test prints it:

```rust
#[rustfmt::skip]
#[cfg_attr(
    feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)
)]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct DatabaseMarker {
    pub commit_sequence: CommitSequence,
    pub first_state_digest: StateDigest,
    pub second_state_digest: StateDigest,
}
```

Before the rule, both `StateDigest` fields derived `state_digest` — invalid Rust; now
positionally distinct.

**Landed.** core-nomos `main` `4d6e8480ccf36fce44b50cbd4e58593b7f044db9`: re-pinned core-schema
`66611bb5` → `2e47dec5` (0.3.0), the reverted `pipeline.rs` test updated from the now-illegal
named spelling to the legal positional spelling asserting the derived names, `nix flake check`
green (fmt, clippy, build, doc, test). Scope boundary honored: the wider consumer re-pin cascade
(schema-engine and beyond) was **not** continued — that is a separate lane. Evidence also on
tracker `primary-56d1.48`.

## 0. Why this exists, in one paragraph

Spirit's live contract declares one streaming operation. **[observed —
`signal-spirit/schema/signal.schema:166`]**
`IntentEventStream (Stream { token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken })`,
opened by `SubscribeIntent` (`:44`, `(SubscribeIntent SubscribeIntent opens IntentEventStream)`)
and populated by four `IntentEvent` variants each marked `belongs IntentEventStream`
(`:165`). Legacy schema-rust already emits the full Rust lowering for this — the
`SubscriptionRegistry` / `SubscriptionEventPublisher` / `StreamEvent` associated
type / `IntentSubscriptionToken` bridge (`spirit/src/schema/daemon.rs:93-750`,
`spirit/src/subscription.rs`) riding the `signal-frame` `StreamingFrameBody`
envelope (`signal-frame/src/frame.rs:65-84`). The next-generation pipeline has **no
counterpart kind** and therefore no lowering target; per the tracked note on
`primary-56d1.39`, this is *already blocking* the Spirit port. This proposal says
where `Stream` sits in core-schema's kind system, how its real declaration is
spelled in next-gen grammar, how it lowers to Rust (behaviorally mirroring the
already-emitted plumbing), and how the structuretree / `Protos` organs carry it.

## 1. The one fact that decides the shape: Stream is role-keyed, not type-keyed

**[observed]** The existing reference-position kind partition
(`schema-language/src/schema.rs:2390`, mirrored stringless at
`core.rs:718` as `CoreReference`) dispatches **by kind and projection, never by a
head string** (`schema.rs:2364-2377`, its own invariant comment):

```
[ (scalar leaves      String Integer Boolean Path Bytes)
  (Plain               a declared-name leaf)
  (SingleTypeApplication  projection ∈ {Vector Optional ScopeOf}   one type argument)
  (MultiTypeApplication   projection ∈ {Map}                        a positional type list)
  (ValueApplication       projection ∈ {Bytes}                      a u64 width, not a type)
  (Application            an open PascalCase head + type arguments) ]
```

The projection is chosen at the codec boundary by a **closed** `from_canonical_name`
lookup over the kind's fixed variant set (`schema.rs:2306`, `:2330`, `:2357`) — an
enum-to-spelling projection, not open head dispatch. Built-in heads (`Map`,
`Optional`, `Bytes`) map to their kind through the source generic-definition table
*before* any `Application` form is produced (`schema.rs:2374-2377`).

Stream does **not** fit any existing kind, and the reason is load-bearing:

- It is **not** a single-type generic (`Optional.T`): it carries four constituents.
- It is **not** a homogeneous/positional multi-type generic (`Map.(K V)`): its
  constituents are **named lifecycle roles**, and — decisively — **[observed]** two
  of them, `token` and `close`, carry the **same** type (`SubscriptionToken`) yet
  name **distinct** legs (open-key versus close-key). A positional list cannot tell
  those two apart; only names can. So Stream's argument is a **role-keyed record**,
  and the roles are the identity, not the types.
- The role names are a **fixed closed set** — `{token opened event close}` — each
  with fixed lowering meaning. They are a vocabulary, not free-form keys.

**[reconciled]** So the design question is not "which existing kind" but "Stream is a
role-keyed construct with a fixed role vocabulary — where in the kind system does a
role-keyed construct belong, and how are the roles modeled so lowering dispatches on
role, never on a role-name string?" §2 answers placement; §3 answers role modeling.

## 2. Placement — three options, honest trade-offs, one recommendation

### 2.1 Option (a) — a dedicated role-keyed **reference-position** kind

Add a fourth application arm to `CoreReference` / `TypeReference`, beside the single-,
multi-, and value-kinds:

```rust
// in CoreReference (core.rs) and its source mirror TypeReference (schema.rs)
RoleKeyedApplication {
    projection: RoleKeyedReferenceProjection,   // closed set — { Stream } today
    roles:      StreamRoles,                     // the fixed typed role record (§3)
}
// with, beside SingleTypeReferenceProjection etc.:
pub enum RoleKeyedReferenceProjection { Stream }
```

**Trade-offs.** *For:* maximally symmetric with the three existing application kinds
— a new kind with a closed projection, dispatched by kind+projection exactly as the
invariant demands; `Stream` registered in the builtin generic-definition table like
`Map`. *Against:* it seats Stream at the **reference position** — anywhere a type
reference may appear (a struct field, an enum payload, an `Optional.T` argument). But
**[observed]** Stream appears in the whole spirit contract **only** as a top-level
named declaration body, and is referenced elsewhere solely by its `Plain` name
(`opens IntentEventStream`, `belongs IntentEventStream`). Admitting it at reference
position therefore admits forms the domain can never produce — `Optional.(Stream {…})`,
a field typed by an inline stream — which the `design-quality` gate rejects (a special
case that should not exist). It also leaves `opens`/`belongs` (relations that need a
declared anchor) with nothing to attach to.

### 2.2 Option (b) — a generalized role-keyed projection mechanism, Stream first

Same reference-position arm as (a), but framed as the general home for *all* future
role-keyed constructs, `projection` growing (`{ Stream, Exchange, … }`) and the role
vocabulary carried per projection.

**Trade-offs.** *For:* one mechanism for a whole family (a bidirectional channel, a
request/reply exchange, a pub-sub topic would each be a new projection). *Against:*
the role **vocabulary differs per projection** (Stream's `{token opened event close}`
versus a hypothetical exchange's `{request reply}`), so the roles cannot be one fixed
typed record at the kind level — they degrade to a `Vec<(RoleIdentifier, CoreReference)>`
keyed by name-table identifiers. Lowering then has to find "the token role" / "the
event role" **by role name**, which is exactly the **convention-based dispatch the
rulings forbid**. Recovering typed dispatch would require a role enum *per projection*
inside one flat kind — more machinery than a single speculative second instance earns.
It inherits (a)'s reference-position mismatch on top.

### 2.3 Option (c) — Stream is a **declaration-body kind**, roles as named typed fields — RECOMMENDED

**[observed]** Declarations already form their own ruled kind partition, disjoint from
the reference partition: `CoreType { Struct(CoreStruct) | Enum(CoreEnum) | Newtype(CoreNewtype) }`
(`core.rs:452`), source-mirrored by `TypeDeclaration { Struct | Enum | Newtype }`.
This is the partition Stream actually belongs to. In the source, `IntentEventStream
(Stream {…})` sits as a **sibling of** `VersionReport { … }` (struct) and
`ValidationError [ … ]` (enum) inside the output type block — it *is* a declared type
body, and it is referenced by name everywhere else. Seat it there:

```rust
// core.rs — the stringless substrate
pub enum CoreType { Struct(CoreStruct) | Enum(CoreEnum) | Newtype(CoreNewtype) | Stream(CoreStream) }

pub struct CoreStream {
    token:  CoreReference,   // the subscription key — opens the subscription
    opened: CoreReference,   // the reply payload returned the moment it opens
    event:  CoreReference,   // the streamed event payload
    close:  CoreReference,   // the key presented to close it (distinct leg from `token`)
}
// schema.rs — the source mirror
pub enum TypeDeclaration { Struct(..) | Enum(..) | Newtype(..) | Stream(StreamDeclaration) }
pub struct StreamDeclaration { name: Name, token: TypeReference, opened: TypeReference,
                               event: TypeReference, close: TypeReference }
```

The head `Stream` is registered in the closed builtin generic/kind-definition table
so the source parser maps it to the Stream declaration kind by closed lookup (same
mechanism as `Map`/`Optional`), never open string dispatch.

**Why this is the cleanest inside the rulings:**

1. **Grammatical faithfulness / no impossible forms.** Stream lives exactly where the
   contract puts it — a declared body, referenced by name. No inline/nested stream
   form is admitted, so there is no special case to remember (`design-quality`).
2. **`opens` / `belongs` get their anchor.** Both are relations on a *declaration*;
   a declaration-kind Stream is the natural identity they point at. A reference-position
   generic has no such identity.
3. **No convention dispatch.** The four roles are **named typed fields**, a closed set
   fixed in the Rust type system; lowering matches the field, never a string (§3).
   The `token`/`close` same-type-distinct-leg fact is captured exactly by two named
   fields — unrepresentable positionally, and free of the name-keyed `Vec` that (b)
   would force.
4. **Kind dispatch preserved and extended.** `CoreType` is already matched
   exhaustively by kind; adding `Stream` is one new arm, dispatched by kind — the
   generics-by-kind ruling holds by construction.
5. **Static disjointness holds.** A Stream body is a `Stream`-headed brace block; a
   struct body is a bare/PascalCase-keyed brace block; an enum body is a bracket
   block; a newtype body is a bare reference. `validate_disjoint` proves these four
   declaration forms provably disjoint — the universal-static-disjointness ruling
   (§0.0 FR-1 of the vision doc) is satisfied with no ordered-overlap.

**The one honest cost of (c):** if the psyche later wants a stream usable *inline* at
a reference position (an anonymous stream as a field type), (c) does not admit it and
(a)/(b) would be needed. Given the sole current and contract-faithful use is a
top-level declaration referenced by name, (c) is correct now and can be widened later
without rework (a declaration kind and a reference kind can coexist). This is
**[DECISION 1]**.

## 3. Role modeling — named typed roles, dispatch on role not string

**[reconciled]** Under every option the four roles must be a **closed typed
vocabulary**, resolved at the codec boundary by the same closed `from_canonical_name`
lookup the existing projections use (`schema.rs:2306`) and stored in the substrate as
**structure, never a string**. In (c) this is the four named fields of `CoreStream`
directly — the vocabulary lives in the field set, so a fifth role is a compile error,
not a silently-ignored key, and lowering reads `stream.event` / `stream.token` by
field, never by name lookup. The role→spelling map (the only place role names are text)
is a closed table:

```
[ (token  → the subscription key type)   (opened → the open-reply payload type)
  (event  → the streamed event type)     (close  → the close-key type) ]
```

Two roles (`token`, `close`) legitimately share a type today (`SubscriptionToken`);
they stay two fields because they are two lifecycle legs and a future stream may key
them differently. Whether `close` is a **mandatory** role or **defaults to `token`'s
type** when elided (brevity vs. explicitness) is **[DECISION 4]**.

## 4. The next-gen TextualForm spelling of spirit's real declaration

Spirit's real line today **[observed — `signal.schema:166`]**:

```
IntentEventStream (Stream { token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken })
```

**[reconciled]** honoring the dotted right-associative-delimiter ruling and the
object-prefixed-block form (`Object.{ … }`, cf. `up-close-design-v1.md` §4.1 /
`CommitSequence.{ Integer }`), the recommended next-gen spelling of the **same
declaration** is:

```
IntentEventStream.Stream.{ token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken }
```

Read as: `IntentEventStream` the declared name, dot-prefixing `Stream` the kind head,
dot-prefixing a brace role-block; each role `token.SubscriptionToken` is a dotted
right-associative `role.Type` binding (camelCase role atom, PascalCase type). This is
brief (drops the wrapping parenthesis of the legacy form), disjoint (the `Stream`
kind head + camelCase role atoms distinguish it statically from a PascalCase-keyed
struct body and a bracketed enum body), and uses only proto-language machinery —
delimiters, capitalization, typed inner blocks. The exact declaration-envelope
spelling (whether the kind head binds as `Name.Stream.{…}` as shown, or the name
carries differently) is a syntax sub-choice — **[DECISION 3]**, recommendation as
spelled above.

The `opens` / `belongs` relations reference the declared name unchanged
(`SubscribeIntent … opens IntentEventStream`; each event variant `… belongs
IntentEventStream`) — they resolve to a `Plain` reference to the Stream declaration,
which (c) makes a first-class declaration identity.

## 5. The lowering contract to Rust — behaviorally mirror the emitted plumbing

The already-emitted surface is the spec **by behavior, not by byte**
(`spirit/src/schema/daemon.rs`, `subscription.rs`, `signal-frame/src/frame.rs`). A
declared `Stream` (its presence anywhere in a component contract) drives, per role:

```
[ (token   → the daemon `SubscriptionToken` associated type + registry key.
             Emits: `type SubscriptionToken: triad_runtime::SubscriptionToken …`
             (daemon.rs:93); the `SubscriptionRegistry<SubscriptionToken, Filter>`
             field + `register_token` (daemon.rs:395,428); the contract-side
             `SubscriptionToken` newtype and its bridge to the runtime trait —
             spirit's `IntentSubscriptionToken` (subscription.rs), emitted per
             declared stream, hand-written only for the runtime-trait bridge.)
  (opened  → an ordinary Output reply variant (`SubscriptionStarted`) returned when
             the subscription opens, carrying the issued token.
             Emits: `fn subscription_token(output: &Output) -> Option<SubscriptionToken>`
             (daemon.rs:193) that recognizes this variant and registers it.)
  (event   → the daemon `StreamEvent` associated type + the published payload.
             Emits: `type StreamEvent: …` (daemon.rs:95); `fn published_event(output)
             -> Option<StreamEvent>` (daemon.rs:194); `fn event_matches_filter`
             (daemon.rs:203); the `SubscriptionEventPublisher<Input, Output,
             StreamEvent>` field + `publish` / `publish_matching` path
             (daemon.rs:400,438,446). The `belongs` variants are the Output arms
             `published_event` maps to a StreamEvent.)
  (close   → the unregister leg keyed by the same token type.
             Emits: the `unregister` / writer-drop path (daemon.rs:476) presented the
             close key.) ]
```

Presence of any Stream in the contract **flips the wire frame** from the exchange-only
body to the streaming body **[observed — `signal-frame/src/frame.rs:47-84`]**: the
generated codec targets `StreamingFrameBody<Request, Reply, Event>` (adding the
`SubscriptionEvent { event_identifier, token, event }` arm) instead of
`ExchangeFrameBody`. This flip is the one contract-surface consequence and must be
versioned as such (`versioning`): a contract that gains a Stream changes its wire body
type. **[reconciled]** the generated component reproduces these behaviors — registry,
publisher, the two associated types, the token bridge, the streaming frame — from the
four typed roles of `CoreStream`; it need not reproduce the legacy bytes, only the
behavior (the retired byte-exact schema-rust oracle is not restored; see `.39`).

This is the lowering target whose absence blocks `.39`. It is **not** the "add
`Stream` to `SingleTypeReferenceProjection` beside `Optional`" shortcut the `.39` note
flags as a forced special case — that shortcut fails precisely because Stream is
role-keyed, not single-type (§1). (c) supplies the real target.

## 6. How the structuretree / Protos organs carry it

**[ruling]** the structuretree *is* the data-driven enc/decoder (`up-close` §2 /
vision §2); each Core constructor carries a `ConstructorCodec` with disjoint
`decode_forms` and one canonical `encode_form` (`up-close` §4.6). Stream is one more
constructor of the `CoreType` declaration kind, carried entirely in the existing
`Protos` vocabulary (`up-close` §4.1 `StructuralElement`) — **no new organ, no new
element type**:

```
;; ConstructorCodec for the Stream declaration body (Protos vocabulary, up-close §4.1/§7.3 shape)
ConstructorCodec { constructor: CoreType::Stream, signature: [ token opened event close ],
  decode_forms: [ ObjectPrefixed(ObjectSymbolPrefixedBlock {          ;; Stream.{ … }
      object: AtomForm{ case: Some(PascalCase), sigil: None },        ;; the `Stream` kind head
      block:  DelimitedBlock{ delimiter: Brace,
                sequence: Product([                                    ;; a fixed four-slot record
                  Application(head: Atom{camelCase "token"},  payload: Delegate(SubscriptionToken)),
                  Application(head: Atom{camelCase "opened"}, payload: Delegate(SubscriptionStarted)),
                  Application(head: Atom{camelCase "event"},  payload: Delegate(IntentEvent)),
                  Application(head: Atom{camelCase "close"},  payload: Delegate(SubscriptionToken)),
                ]) } }) ],
  encode_form: <the same, normalized to the canonical Application chain> }
```

Each role binding is a right-associative `Application(camelCase-role-atom, type-ref)`
— the same dotted application the proto-language already carries; the four-slot
`Product` sequence (up-close §4.6 sequence algebra) fixes the role arity, and
`validate_no_silent_conflicts` / `validate_disjoint` prove the Stream body form
disjoint from the struct/enum/newtype body forms. The camelCase role atoms resolve to
the closed role vocabulary at the codec boundary (§3), so the structuretree stays
stringless underneath. **[reconciled]** Help/Version (secondary structuretree
projections, vision §4) render Stream's declaration from this same form for free.

Since Stream is a `CoreType` arm (c), it needs **no** `structural-codec`/`raw-discovery`
change and **no** new reference-kind projection — it reuses `ObjectPrefixedBlock`,
`Application`, `Delimited`, `Product`, and `Delegate` exactly as struct/newtype
already do. Under (a)/(b) the same form would instead sit at the reference position
and additionally need a new `RoleKeyedReferenceProjection`, the source generic-table
entry, and the CoreReference arm — strictly more surface for the impossible-form cost
of §2.1.

## 7. Numbered decision items for the manager (options + recommendation; not asked of the psyche directly)

**[DECISION 1] — Where does Stream sit in the kind system?** *(the primary kind-system
shape decision)* Options: **(a)** a dedicated role-keyed **reference-position** kind
(`CoreReference::RoleKeyedApplication`, projection `{Stream}`); **(b)** a generalized
role-keyed reference kind, Stream the first of many projections; **(c)** a
**declaration-body kind** — a fourth `CoreType` arm beside Struct/Enum/Newtype.
**Recommendation: (c).** It matches Stream's only real position (a named declaration
referenced by name), admits no impossible inline forms, anchors `opens`/`belongs`,
keeps kind dispatch and static disjointness, and needs no reference-projection or
`Protos` change. (a) is the fallback if inline anonymous streams are ever wanted; (b)
additionally forces name-keyed roles → convention dispatch the rulings forbid.

**[DECISION 2] — Role modeling.** Options: **(i)** four **named typed fields**
(`token opened event close`), the closed vocabulary living in the field set, lowering
dispatching on the field; **(ii)** a positional type list (Map-style); **(iii)** a
name-keyed `Vec<(RoleIdentifier, CoreReference)>`. **Recommendation: (i).** Only named
typed fields capture the `token`/`close` same-type-distinct-leg fact and keep dispatch
off role-name strings; (ii) cannot distinguish the two token legs, (iii) reintroduces
convention-based name dispatch.

**[DECISION 3] — The next-gen declaration spelling (syntax).** Recommended spelling of
spirit's real line, in next-gen dotted grammar:

```
IntentEventStream.Stream.{ token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken }
```

(declared name `.` kind head `.` brace role-block; each role a dotted `role.Type`
binding). Sub-choice: whether the kind head binds as `Name.Stream.{…}` (shown) or the
declaration name carries the kind differently. **Recommendation: as spelled** — brief,
statically disjoint, pure proto-language (delimiters + capitalization + typed inner
blocks).

**[DECISION 4] — Is `close` mandatory or defaulted?** Options: **(i)** `close` is a
**mandatory** explicit role (faithful to the contract, all four legs named); **(ii)**
`close` **defaults to `token`'s type** when elided (briefer, since they coincide
today). **Recommendation: (i)** — explicit and faithful; the two legs are semantically
distinct and a future stream may key close differently, so eliding it buries a real
distinction. Returned because it is a syntax/brevity call the psyche owns.

## 7.1 Post-ruling decision items — the Nomos-minted-kind bootstrap (2026-07-18)

Ruling A resolved the *placement* ([DECISION 1] → declaration kind) and the *mechanism*
(minted through Nomos). What it opened is the bootstrap: reconciling a Nomos-minted kind
with the closed Rust `CoreType`/`SectionDefault`/`MemberKind` enums (§0.0 Ruling A). These
items are the concrete kind-system-schema delta the psyche must accept **before** any
implementation (authority boundary). Options + recommendation; not silently picked.

**[DECISION A1] — How does a Nomos-minted declaration kind enter, given the closed Rust
kind enums?**

- **(a) Open the kind set to data.** Replace the closed `CoreType` enum with an extensible
  kind registry: kind identity centrally assigned (like the authority-assigned type ids of
  `CoreUniverse::from_assignment`), each kind supplying its `ConstructorCodec` structuretree
  form and its Nomos lowering; every current exhaustive `match` becomes a total function
  over the registry. *For:* maximal fidelity to "just create a new kind of object" — no Rust
  edit per kind. *Against:* dissolves the compile-time exhaustiveness the family leans on;
  static disjointness moves entirely to seal-time `validate_disjoint` (already how *forms*
  are checked, so partially precedented, but a large blast radius across core-schema +
  core-nomos + the universe bridge).
- **(b) Keep `CoreType` closed; Nomos supplies behaviour only.** A new kind is still one new
  Rust arm, but **all behaviour** — structuretree form, lowering, role semantics — is
  authored as a Nomos package, not hand-written Rust. "Create a new kind" = author the Nomos
  package; the one-line arm is mechanical plumbing. *For:* preserves static
  exhaustiveness/disjointness untouched. *Against:* still a Rust edit per kind — contradicts
  the letter of the ruling ("just create a new kind of object", implying no core edit).
- **(c) One generic extension arm, minted into — RECOMMENDED.** Core provides the **minimal
  hook**: a single `CoreType::Extension(CoreExtension { kind: MintedKindId, fields })` arm
  (plus the mirror in `MemberKind`), where `MintedKindId` is **centrally assigned** exactly
  like a type id. One Rust arm admits an **open family** of Nomos-minted kinds; each minted
  kind supplies its own `ConstructorCodec` structuretree form and its structural lowering
  from its Nomos package. Static disjointness is preserved because all extension kinds share
  one Rust arm yet are proven pairwise-disjoint at seal by `validate_disjoint` over their
  supplied forms (Stream's `Stream.{…}` head vs any future kind's head). *For:* honours "mint
  a kind via Nomos" with **no per-kind Rust edit after the one hook**, keeps the three native
  kinds closed and fast, and localises the change to one arm + a kind-id registry + a
  form/lowering slot. *Against:* extension kinds are dispatched by `kind_id` (a small
  dynamic step) rather than a Rust variant; the exhaustive-match guarantee holds for the
  native three but becomes a registry lookup for extensions. **Recommendation: (c)** — the
  honest minimal hook that lets Stream be *minted* rather than *hand-carved*, while the
  native kinds keep their closed-enum discipline. Stream is the first mint and the witness.

**[DECISION A2] — Does the Nomos dispatch side open with it?** `SectionDefault::of_core_type`
is exhaustive-over-`CoreType` with no wildcard, and `MacroKind` is closed to *"exactly two"*.
The "exactly two macro kinds" ruling is **untouched** — the two remain `Named` /
`Structural`. But under A1(a)/(c) the **`Structural(SectionDefault)`** selector must map an
**open** kind set to structural defaults, so `SectionDefault` becomes keyed by the
centrally-assigned `MintedKindId` (a lookup) rather than the closed 3-variant enum for
extension kinds. Recommendation: **keep the three native `SectionDefault` variants closed,
add a `Structural` path keyed by `MintedKindId` for minted kinds** — consistent with A1(c),
leaving `MacroKind`'s two-kind ruling intact.

**[DECISION A3 = former DECISION 4, now Item D — OPEN, not agent-owned].** Whether `close` is
a mandatory explicit role or defaults to `token`'s type when elided is **re-grounded to the
psyche** ("I dont follow all that") and stays open (§0.0 Item D). No recommendation is
carried forward as ruled; the earlier §7 [DECISION 4] recommendation (i) is now just a prior
agent lean pending the psyche's own answer.

**Implementation work item (consequence of Ruling C, gated on the veto).** The codec's
elision rule (`CoreField::name_is_derivable`, `textual.rs` reify/reflect) must become
**collision-aware**: reject on decode and never emit on encode an explicit text name for a
field whose type is unique in its block. Registered on `primary-56d1.48`; does not land until
the psyche confirms the manager reading of Ruling C.

## 8. Tracker

Registered slice **`primary-56d1.48`** — "Stream subscription kind: ruling +
implementation" — parent epic `primary-56d1`, **blocked-on-psyche** for [DECISION 1]
(the kind-system shape) and [DECISION 3] (the syntax). It **blocks the Stream leg of
`primary-56d1.39`** (the Spirit port's `SubscribeIntent` operation). Dependencies
truthful: the ordinary-leg codec-body work (the classes-E/F / Class-C encode-decode
bodies, `.39` BLOCKED (b), running as a parallel lane) **does not** wait on this
slice — the two legs are independent; a component with no Stream lowers its ordinary
exchange leg regardless of the Stream ruling. Once the psyche rules [DECISION 1]/[3],
this slice unblocks to implement the chosen kind in core-schema + core-nomos lowering
+ the structuretree form, witnessed by Spirit's `IntentEventStream`.

## 9. Validation scope

Design-authority only. No engine source, generated artifact, store, deployment, or
Spirit record was changed. Every kind-system, plumbing, and wire fact is cited to code
read this pass (`schema-language/src/{schema,core}.rs`, `spirit/src/schema/daemon.rs`,
`spirit/src/subscription.rs`, `signal-frame/src/frame.rs`, `signal-spirit/schema/signal.schema`).
Ruling claims cite `textual-form-vision-design-v2.md` and `up-close-design-v1.md`.
Nothing here is accepted until the psyche grades §7; the decision items are returned to
the manager, never asked of the psyche directly.
