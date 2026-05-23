# 263 — Schema specification language design

*Fresh-design sketch for the persona-component contract schema
language. The aski-stack-as-foundation framing of the now-superseded
predecessor was wrong per psyche correction (`intent/signal.nota`
records 33 and 42); the language is its own design — not an extension
of aski-core / askic / askicc / corec — and is scoped strictly to the
workspace's Rust subset. Cap'n Proto is the closest reference point;
the workspace language is more explicit in a precise sense developed
below. The three-layer separation and schema-change classes sections
below were absorbed from the superseded predecessor (`/262`,
content-addressable schema-layout schema, retired in the same commit
this lands).*

## What this language is

The schema specification language declares the typed records that
form a `signal-<component>` (or `owner-signal-<component>`) wire
and storage contract. A schema file is the single source of truth
for one contract: Rust types (with rkyv `Archive` / `Serialize` /
`Deserialize` and workspace `NotaRecord` / `NotaEnum` /
`NotaTransparent` derives) are generated from it; the file's Blake3
content address is the contract version (record 29); the schema
carries layout-bound annotations sufficient for a diff classifier
to identify zero-cost vs append-only vs structural changes (record
30, the rkyv-headroom Principle).

Consumers: the **generator** emits Rust source; the **diff
classifier** reads two schemas and emits a typed migration plan
(Approach C mechanism per intent record 21 — not in scope here); the
**daemon** at boot compares stored vs current address and runs the
plan (also out of scope). Designers and operators read the schema
directly.

## Three layers, three concerns

*Absorbed from superseded `/262`. The framing carries forward
unchanged because it pins down which concern this language
addresses and which it does not.*

What prior reports conflated, this design separates cleanly.

| Layer | Format | Role | Strictness |
|---|---|---|---|
| User-facing | NOTA text | Agent ↔ daemon wire arguments, intent capture, contract documentation | Strict positional, no tail-omission, every field appears |
| Schema-layout | NOTA-based DSL (this language) | Source of truth for rkyv layout; content-addressed; diff-able | Whatever the DSL declares |
| Storage | rkyv bytes | Persistent records in redb | Has natural headroom (byte-wide enums, sized fields) |

The user-facing strictness lives at the top layer; the migration
discipline lives at the bottom; the **schema-layout layer is the
bridge** that lets the bottom be reasoned about by machines rather
than by hand. This report specifies that middle layer.

## Constraints

**Workspace Rust subset.** The language declares only what the
`signal-*` crates already use: named-field structs, tagged enums
with PascalCase variants (unit or single-payload), transparent
newtypes, fixed-width integer scalars, `String`, `Vec<T>`,
`Option<T>`. No anonymous types; no in-schema generics (`Vec` and
`Option` are built-ins); no traits, lifetimes, or references.

**No tuples — ever.** Per record 42 and `skills/nota-design.md`,
a tuple is a poorly-defined struct: position without field names.
Every heterogeneous-positional shape declares as a named-field
struct. Hard rule, not a style guideline.

**Positional NOTA-flavoured syntax.** The schema *is* a NOTA file.
Records are positional `(Tag fields…)`; no `(key value)` labels.
Variants are PascalCase; bare camelCase / kebab-case identifiers
are field names.

**Content-addressable.** A canonical encoding of the schema text
(whitespace-normalised NOTA, declaration order load-bearing) hashes
with Blake3. The hash is the contract version. No manual version
constants; no semver; no human-bumped numbers.

**Layout-bound annotations are first-class declarations.** Every
type carries the rkyv-layout commitments the operator has chosen
(discriminant width, append-only marker). They are part of the
contract, not optimisation hints. A change inside the reserved
headroom is zero-cost; a change that violates an annotation is
structural.

**Names follow workspace discipline.** `Entry` not `IntentEntry`;
`topic` not `entryTopic` (`ESSENCE.md` §"Naming",
`skills/naming.md`).

## How this differs from Cap'n Proto

Cap'n Proto is the closest published reference. The differences
move the language toward *more explicit*.

**Layout commitments are stated, not inferred from field IDs.** In
Cap'n Proto, on-disk layout is implied by author-assigned ordinals
(`@0`, `@1`). Here, the layout-bound annotation says directly
what's reserved: `(discriminant-width 1)` means a one-byte variant
index with 256 variants of headroom. The diff classifier reads the
annotation rather than reconstructing intent from ordinals.

**Positional declaration; no field IDs.** Field order in the
schema is field order in rkyv. No `@7` ordinal. Reordering fields
*is* a structural change, full stop; layout-affecting changes show
up as syntactic changes in the schema text.

**No anonymous types.** Cap'n Proto allows anonymous unions, groups,
parameterised types. Here, every type is declared by name at the
top level; field types are built-in scalars, built-in containers,
or another named type from the same schema.

**Identity is content-addressable, not nominal.** Cap'n Proto uses
64-bit type ids the author assigns once. Here, identity is Blake3
of the canonical schema text. Renaming a type changes the address
(the diff classifier sees the rename as remove-then-add); the
author does not maintain an id table.

**Append-only is declared, not implicit through ordinal
monotonicity.** Cap'n Proto's compatibility rests on never reusing
or reordering field ids. Here, `(append-only)` on an enum or
channel leg is a promise that *all future additions land at the
end*. The diff classifier flags mid-position insertions as
structural breaks even when raw rkyv would have tolerated them.

## Sketch of the syntax

A schema file is a NOTA stream of top-level declarations. Four
top-level variant tags: `Record`, `Enum`, `Transparent`, `Channel`.
Each declaration's positional fields are name, body (a sequence),
and layout annotation (also a sequence). Scalar built-ins
(`String`, `u8`, `u64`) appear bare at field-type positions.
Container built-ins take their inner type as a nested sequence:
`[Vec Topic]`, `[Option Topic]`.

### A transparent newtype

```nota
(Transparent Topic String)
```

Name then inner type. Transparent newtypes have no layout headroom
to declare; they inherit the inner type's layout.

### A scalar struct

```nota
(Record Entry
    [(topic     Topic    )
     (kind      Kind     )
     (summary   Summary  )
     (context   Context  )
     (certainty Certainty)
     (quote     Quote    )]
    [])
```

Each field is a `(name type)` positional pair where `name` is the
camelCase Rust field name and `type` is a scalar, a container, or
a named type. Fields appear in rkyv layout order. The trailing
empty sequence is the (empty) layout annotation block.

### A small enum with reserved headroom

```nota
(Enum Kind
    [Decision Principle Correction Clarification Constraint]
    [(discriminant-width 1) (append-only)])
```

Body is the variant list — bare PascalCase tokens for unit
variants. The layout annotation declares one-byte discriminant
(251 more variants fit zero-cost) and append-only (additions land
at the end).

### An enum with mixed unit and data variants

```nota
(Enum Observation
    [State
     (Records RecordQuery)
     Questions]
    [(discriminant-width 1) (append-only)])
```

`(Records RecordQuery)` is a variant tag followed by the payload
type — the NOTA shape for a data-carrying variant. The language
does not allow inline anonymous payloads; a payload type is always
a named type declared elsewhere in the schema.

### The channel declaration

```nota
(Channel Spirit
    [(operation State   Statement  )
     (operation Record  Entry      )
     (operation Observe Observation)
     (operation Watch   Subscription opens DomainStream)
     (operation Unwatch SubscriptionToken)]
    [(reply RecordAccepted) (reply StateObserved)
     (reply RecordsObserved) (reply RecordProvenancesObserved)
     (reply QuestionsObserved) (reply SubscriptionOpened)
     (reply SubscriptionRetracted) (reply RequestUnimplemented)]
    [(event StateChanged   belongs DomainStream)
     (event RecordCaptured belongs DomainStream)]
    [(stream DomainStream
        (token  SubscriptionToken )
        (opened SubscriptionOpened)
        (close  Unwatch           ))]
    [(observable
        (filter          default          )
        (operation_event OperationReceived)
        (effect_event    EffectEmitted    ))])
```

The channel ties named types into the wire vocabulary. Each leg
(operations, replies, events, streams, observable) is an ordered
list, implicitly append-only (see §"Open questions").

## Schema-change classes

*Absorbed from superseded `/262`. The three-way classification is
the vocabulary the diff classifier emits and the worked example
below demonstrates concretely.*

A diff between two schemas falls into one of three classes per
affected type. The classification determines whether a migration
step is needed and which leg of the daemon's version-pipeline
handles it.

**Zero-cost (no migration).** The new schema is byte-compatible
with the old — existing stored payloads decode correctly under
the new types without any transformation. Examples:

- Adding a unit variant to an enum whose discriminator still fits
  in the declared width (a 3-variant enum becoming 4-variant in a
  `(discriminant-width 1)` byte). Variant order preserved.
- Widening a fixed-width integer field if rkyv reserved the larger
  size already (less common; check rkyv's layout rules).
- Renaming a field or variant without changing position
  (identity-only schema change; the new code reads the same bytes).

The diff classifier emits a zero-cost class; the daemon updates
the schema-address reference on the affected records (or treats
the old address as a synonym for the new) and continues without
touching the payload bytes.

**Append-only (cheap migration).** The new schema extends an
existing type at its boundary with a new field/variant whose
default value can be computed without consulting the old data.
Examples:

- Adding a new field to the **end** of a struct (a 3-component
  struct becoming 4-component with the new field at the tail).
  Existing payloads gain the default-encoded new field appended
  at read or rewrite time.
- Adding a unit variant beyond the current discriminator width
  (requires byte widening — append-only at the discriminator
  level if the framework handles the width transition).

The migration step is mechanical: per existing record, append the
default bytes for the new field at the read position. No
type-specific logic needed.

**Structural (typed migration).** The schema diff cannot be
resolved mechanically — the migration requires domain information
the diff alone doesn't carry. Examples:

- Splitting an enum variant into two (`Phase` becomes
  `Phase::Active` and `Phase::Latent` — the old `Phase` values
  need to be disambiguated using context the schema doesn't see).
- Renaming a field with semantic change (the new field carries
  different intent; old values may need transformation).
- Field-type change where the new type doesn't subsume the old
  (e.g., a `Topic` `String` becoming a typed sum).
- Reordering fields in the middle of a struct (or, in this
  language's terms, any change that violates an `(append-only)`
  annotation).

The schema must let the agent **declare** the transformation for
structural changes — either inline in the schema diff or as a
sibling migration NOTA file the schema-tooling applies during the
version-pipeline run. The mechanism is out of scope here; the
classification is the contract this language hands the classifier.

## The worked example — spirit master vs deployed

The diff between deployed `signal-persona-spirit` (`b89731f`,
pinned in CriomOS) and master (`cda5469`, "add topic catalog
observation") is the concrete case the language must let the
designer express clearly and the diff classifier must flag.

### Deployed shape (relevant fragments)

```nota
(Enum Observation
    [State (Records RecordQuery) Questions]
    [(discriminant-width 1) (append-only)])

(Channel Spirit …
    [(reply RecordAccepted) (reply StateObserved)
     (reply RecordsObserved) (reply RecordProvenancesObserved)
     (reply QuestionsObserved) (reply SubscriptionOpened)
     (reply SubscriptionRetracted) (reply RequestUnimplemented)]
    …)
```

`TopicCount` and `TopicsObserved` do not exist. `Observation` has
three variants; the reply leg has eight.

### Master shape (relevant fragments)

```nota
(Record TopicCount
    [(topic Topic) (entries u64)] [])

(Record TopicsObserved
    [(topics [Vec TopicCount])] [])

(Enum Observation
    [State (Records RecordQuery) Topics Questions]
    [(discriminant-width 1) (append-only)])

(Channel Spirit …
    [(reply RecordAccepted) (reply StateObserved)
     (reply RecordsObserved) (reply RecordProvenancesObserved)
     (reply TopicsObserved) (reply QuestionsObserved)
     (reply SubscriptionOpened) (reply SubscriptionRetracted)
     (reply RequestUnimplemented)]
    …)
```

Both `Topics` (in `Observation`) and `TopicsObserved` (in the reply
leg) were inserted **mid-position**. The canonical schema text
changed; the Blake3 address changed; the contract version
therefore changed.

### What the diff classifier reports

```nota
(Plan
    (Added Record TopicCount      ZeroCost)
    (Added Record TopicsObserved  ZeroCost)
    (Modified Enum Observation
        [(InsertVariant Topics 2)]
        Structural
        (Violation append-only
                   "variant Topics inserted at index 2"))
    (Modified ChannelReply Spirit
        [(InsertReply TopicsObserved 4)]
        Structural
        (Violation append-only
                   "reply TopicsObserved inserted at index 4")))
```

Reading the plan:

- `TopicCount` and `TopicsObserved` are added — no prior data,
  zero-cost.
- The mid-insertion of `Topics` into `Observation` shifts the rkyv
  discriminant of `Questions` from 2 to 3. `Observation` is a
  Request payload in spirit's channel (not stored), so storage
  bytes are unaffected — but any agent still emitting the
  deployed-shape discriminant would misroute. Append-only
  annotation is violated; classifier flags Structural.
- The mid-insertion of `TopicsObserved` into the reply leg shifts
  the rkyv discriminant of every reply past index 4
  (`QuestionsObserved`, `SubscriptionOpened`,
  `SubscriptionRetracted`, `RequestUnimplemented`) by one. Wire
  compatibility breaks for any agent on the deployed schema.
  Structural.
- The `Entry` storage record is unchanged. Stored intent entries
  are byte-compatible; no payload migration required.

### The append-at-end fix

Move both insertions to the end of their variant lists:

```nota
(Enum Observation
    [State (Records RecordQuery) Questions Topics]
    [(discriminant-width 1) (append-only)])

(Channel Spirit …
    [(reply RecordAccepted) (reply StateObserved)
     (reply RecordsObserved) (reply RecordProvenancesObserved)
     (reply QuestionsObserved) (reply SubscriptionOpened)
     (reply SubscriptionRetracted) (reply RequestUnimplemented)
     (reply TopicsObserved)]
    …)
```

Under the fixed schema the classifier emits:

```nota
(Plan
    (Added Record TopicCount      ZeroCost)
    (Added Record TopicsObserved  ZeroCost)
    (Modified Enum Observation
        [(AppendVariant Topics 3)]
        ZeroCost)
    (Modified ChannelReply Spirit
        [(AppendReply TopicsObserved 8)]
        ZeroCost))
```

Every change is zero-cost. The contract version still bumps (the
content address changed); the daemon updates its address reference
at boot; no payload bytes are touched. This is the rkyv-headroom
Principle expressed in code-review terms — the schema language
makes it visible whether a change was zero-cost or not, before
the change lands.

## Open design questions worth psyche input

1. **Where do channel-level layout annotations live?** Each
   channel leg (operations, replies, events) is an ordered list
   and effectively an enum at the rkyv level. The sketch puts
   `(append-only)` on top-level `Enum` declarations but doesn't
   say where the equivalent sits for channel legs. Candidates:
   inline at the leg, at the channel level, or implicit (every
   leg is append-only by default and dissent is explicit).
   Designer lean: **implicit append-only** for channel legs, since
   channel legs *are* enums and the workspace convention is that
   the only reason to insert mid-position is forgetting the rule.

2. **Are struct-level layout annotations actually load-bearing?**
   rkyv computes struct alignment from field alignments; the
   schema author rarely overrides. The annotation block on
   `Record` declarations might be write-only (declared but never
   violated). If so, drop it and require layout annotations only
   on `Enum` declarations. Designer lean: drop struct-level
   annotations until a concrete case demands one.

3. **Is the schema one file or many?** A `signal-<component>`
   contract has 30+ types. One file is grep-able but long; many
   files (per-type or per-domain) compose into one logical
   schema. Either way the content address spans the *logical*
   schema — the canonical encoding has to define how multiple
   files combine. Lexical filename concatenation is the obvious
   choice; doesn't survive renames cleanly. Open.

4. **What does the `owner-signal-<component>` schema look like?**
   Owner-channel records have different lifecycle than
   working-channel records. Same language, same shape? Or does
   the owner channel need bootstrap-specific declarations?
   Designer lean: same language; the owner-channel difference
   lives in the daemon's bootstrap handling, not in the schema.

5. **What gets a built-in scalar?** The sketch commits to
   `String`, `u8 / u16 / u32 / u64`, `bool`. `Date` and `Time`
   (currently hand-written in `signal-persona-spirit`) feel like
   they could be built-ins too — they appear in many components
   and have fixed NOTA encodings already. Open whether the
   language ships workspace-specific scalars or stays purely
   Rust-shape.

6. **Inline payloads for one-off variants?** The *no anonymous
   types* rule forces a name on every payload struct. For
   variants whose payload is genuinely one-off (e.g.,
   `RequestUnimplemented(UnimplementedReason)`), naming the
   payload type is the right friction — but for shapes that exist
   only to discriminate a sum, the ceremony might over-tax the
   schema. Designer lean: keep the absolute rule. Naming the type
   is what `ESSENCE.md` §"Naming" wants.

## References

- `intent/signal.nota` records 28-30, 33, 42 — psyche's framing:
  rkyv-headroom Principle, content-addressable schema Decision,
  fresh design (not aski-stack-extension), no tuples.
- `intent/component-shape.nota` record 21 — Approach C
  (in-process versioned reads), the migration mechanism this
  language composes with. The content address subsumes the
  per-component vs per-record-type question (per-type addresses
  derive by hashing each subtree).
- `reports/designer/315-design-sema-upgrade-and-handover-current-state.md`
  — current sema-upgrade and handover state; this language feeds the
  schema-address branch of that work.
- `skills/nota-design.md` — NOTA discipline the syntax inherits.
- `skills/component-triad.md` — signal-type / signal-tree
  vocabulary the schema declares.
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`
  (master, `cda5469`) — worked example data.
