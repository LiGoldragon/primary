# Why collections + Option is the first and decisive gate

*Detailed explainer for the `/40/3` synthesis claim: "What blocks a FULL port today is a small, well-scoped set of schema-next CAPABILITY gaps — and both waves independently converge on collections (Vec/BTreeMap) + Option at type-reference positions as the first and decisive gate." Grounded in the actual schema-next source (`schema-next/src/asschema.rs`) + Wave A's horizon inventory.*

## The claim, unpacked into its four parts

The sentence makes four sub-claims; this explainer walks each:

1. "a small, well-scoped set of capability gaps" — the gaps are schema-next FEATURES, not architecture.
2. "collections (Vec/BTreeMap) + Option" — the specific missing features.
3. "at type-reference positions" — WHERE the gap lives (this is the precise, load-bearing phrase).
4. "the first and decisive gate" — why this one, before the others.

## What a "type-reference position" is

In the schema language, there are two distinct kinds of place a type name appears:

- **Declaration position** — where a type is DEFINED. In the namespace (position 3 of the schema document): `(NodeProposal [Center Trust ...])` defines a struct named `NodeProposal`; `(Phase (Building Activating Observed))` defines an enum.
- **Type-reference position** — where a type is USED as the type OF something. Two places this happens:
  - A **struct field's type**: in `(NodeProposal [Center Trust ...])`, each of `Center`, `Trust` is a reference to another type.
  - An **enum variant's payload type**: in `(Input ((Submit DeploymentRequest)))`, `DeploymentRequest` is a reference.

The schema-next AST makes this split explicit. From `schema-next/src/asschema.rs`:

```rust
pub struct FieldDeclaration {
    pub name: Name,
    pub reference: TypeReference,   // a field's type is a TypeReference
}

pub struct EnumVariant {
    pub name: Name,
    pub payload: Option<TypeReference>,  // a variant's payload is a TypeReference
}
```

So a "type-reference position" is: the `reference` of a struct field, or the `payload` of an enum variant. That is where one type points at another.

## The decisive fact — `TypeReference` is a bare name

Here is the entire `TypeReference` type, verbatim from `asschema.rs:153-164`:

```rust
pub struct TypeReference {
    pub name: Name,
}

impl TypeReference {
    pub fn new(name: impl Into<String>) -> Self {
        Self { name: Name::new(name) }
    }
}
```

That is the whole gate, in one struct. **A type reference is JUST a name.** It can say "this field is a `Topic`." It has no capacity to say "this field is a `Vec` of `Topic`," or "a `BTreeMap` from `NodeName` to `NodeProposal`," or "an `Option` of `Config`." There is no slot for type arguments. There is no "collection of" or "optional of" wrapper.

Correspondingly, `TypeDeclaration` (asschema.rs:113-118) is only three shapes:

```rust
pub enum TypeDeclaration {
    Struct(StructDeclaration),
    Enum(EnumDeclaration),
    Newtype(StructDeclaration),
}
```

No `Vec`, no `Map`, no `Option`. The type model is closed over struct/enum/newtype with bare-name references between them.

## Why `Topics [Topic]` becomes a newtype, not `Vec<Topic>`

This is the concrete symptom Wave A found. You might think you could write `Topics [Topic]` in the namespace and get `Topics = Vec<Topic>`. You don't. The square-bracket form `[...]` at the namespace level means "struct/newtype fields" — so `Topics [Topic]` parses as a **newtype with one field of type `Topic`**: `pub struct Topics(Topic)`. Wave A confirmed this against the emission test fixture: the generated code reads `entry.topics.0.0` — a single value reached through two tuple-wrapper layers (`Topics(Topic)` then `Topic(String)`), NOT `Vec<Topic>` iterated.

The bracket means "wrap these fields in a struct," not "make a list of this." There is no syntax — and more fundamentally no AST capacity — for "list of `Topic`" at a reference position.

## Why horizon NEEDS it — the aggregate roots are all collection-bearing

A leaf type (a scalar, a single enum, a one-field newtype) references nothing collection-shaped, so it emits today. The problem is the AGGREGATE roots — and horizon is nearly all aggregate. Wave A's inventory: **112 container-field-lines (21 `BTreeMap`, 39 `Vec`)** across the proposal layer. The root, `ClusterProposal`, is itself collection-bearing — conceptually a map of node-name → node-proposal plus a list of user-proposals plus cluster-wide config. From the cluster data shape seen earlier in the workspace, the proposal is literally `(ClusterProposal [ (Entry <node-name> (NodeProposal ...)) ... ])` — a keyed collection of nodes.

You cannot emit `ClusterProposal` from schema while `TypeReference` can only say "a `NodeProposal`" and never "a map of `NodeName` to `NodeProposal`." Every aggregate above the leaf layer hits this wall. That is why the datatype-driver verdict is PARTIAL: leaves emit, the real thing doesn't.

## Why Option specifically

The same gap in the optional direction. Horizon (and lojix) have fields that may be absent — `Option<SomeConfig>`, an optional override, a may-or-may-not-be-present capability. Note a subtlety: `EnumVariant.payload` is `Option<TypeReference>` in the AST — but that optionality means "this VARIANT may carry no payload," NOT "the referenced type is optional." There is no way to say a struct field is `Option<Config>`. Optionality at the type-reference position is the same missing capability as collections: the reference can't be wrapped. So `Option` rides in on the same fix.

## Why "first"

Two reasons it comes before the other gaps:

1. **Nothing aggregate emits without it.** The JSON-emission gap (Gate 2) and the streaming-topology gap (Gate 3) are about what you do WITH emitted types. Collections is about whether the central types emit AT ALL. `ClusterProposal` — the thing horizon exists to project — cannot be a schema-emitted noun until collections land. It is upstream of everything else.
2. **Both layers wait on the same fix.** Wave A (horizon datatypes) and Wave B (lojix wire breadth — cache-retention lists, multi-phase observation sequences) independently land on it. One fix, two unblocks. The convergence is why it's the highest-leverage single change.

## Why "decisive"

- **It's the leaf-vs-real-thing line.** Before it: scalars, single enums, one-field newtypes emit — enough for a toy, not for horizon's `ClusterProposal` or lojix's full wire. After it: the actual aggregate types emit. It is the difference between "the pilot can emit a few types" and "the system's real datatypes are schema-driven."
- **It's shared, so its leverage is doubled.** Most gaps are layer-local (JSON emission is horizon-only; streaming topology is lojix-wire-only). Collections is the one both need.
- **It's already authorized in principle.** Spirit record 883 authorized modifying schema-next for vectors; `/37/3` deferred it as I-6; `/39` re-flagged it. The psyche has already sanctioned the direction — this explainer just shows it's the FIRST domino, not an incremental nicety.
- **It's bounded.** See next section — it's a contained type-model + emitter change, not a substrate rewrite.

## What landing it concretely requires (and what it does NOT)

**Requires** (the bounded work):

1. **Grow `TypeReference`** from a bare `{ name: Name }` into something that can carry type arguments — most naturally an enum:
   ```rust
   pub enum TypeReference {
       Plain(Name),
       Vector(Box<TypeReference>),
       Map(Box<TypeReference>, Box<TypeReference>),
       Optional(Box<TypeReference>),
   }
   ```
   (Exact shape is a schema-language design choice — see `/40/3 §"What this audit does NOT settle"`.)
2. **Macro lowering** recognizes a collection/option syntax at reference positions (e.g. a `[T]` form meaning Vec-of-T when used as a field type, or explicit `(Vec T)` / `(Map K V)` / `(Option T)` heads) and lowers to the new `TypeReference` variants.
3. **schema-rust-next emits** `Vec<T>` / `BTreeMap<K, V>` / `Option<T>` from those variants instead of a bare type path.

**Does NOT require** (why it's "well-scoped," not architecture): the wire substrate is untouched. Wave A confirmed nota-next already parses `{}` brace blocks (the textual structure for maps is there), and the legacy `nota-codec` already has full `Vec` / `BTreeMap` / `Option` rkyv+NOTA codecs. So once the type model expresses a collection and the emitter writes `Vec<T>`, the encoding/decoding already works. The gap is purely (a) schema-next's `TypeReference` type model and (b) the emitter — two files, not a stack. That is the entire reason the FULL-port blocker is "small and well-scoped" rather than "rebuild the substrate."

## The three schema-next gaps in dependency order

| Gap | Where | Gates | Order |
|---|---|---|---|
| **Collections + Option at type-reference positions** | schema-next `TypeReference` + emitter | every aggregate type in BOTH horizon + lojix | **FIRST — upstream of all aggregate emission** |
| JSON-output emission | schema-rust-next | horizon (emits JSON for Nix) | After collections — horizon-specific |
| Streaming-channel topology (schema-derived signal-frame) | schema-next + `/390` | lojix observation-stream wire | After collections — lojix-wire-specific |

Collections is first because the other two operate on types that can't even be emitted until collections exist. It is decisive because it's the single change that turns "leaf types emit" into "the real aggregate datatypes of both horizon and lojix emit" — and it's already psyche-sanctioned and bounded to two files of schema-next/schema-rust-next.

## See also

- `3-overview.md` — the synthesis this explainer expands (the §"convergent finding" + the gap-ranking table).
- `1-horizon-datatype-and-projection-state.md` — Wave A: the 112-container-field inventory + the `Topics [Topic]` → newtype evidence.
- `2-lojix-signal-sema-state.md` — Wave B: the lojix wire-breadth need for collections.
- `schema-next/src/asschema.rs:113-164` — the `TypeDeclaration` + `TypeReference` source this explainer reads.
- `/37/3` I-6 + Spirit record 883 — the prior flagging + the psyche authorization for vectors.
- `/39/3` — the types-only-module finding (a sibling schema-next capability gap; not on the critical path for collections).
