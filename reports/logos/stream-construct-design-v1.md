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
