# Type, new type and type alias: research

Research for the book on type, new type and type alias, made for flow
d5df1d. Each claim is marked with where it comes from: **record** is
the living's words, quoted verbatim; **read** is code this flow read;
**witnessed** is a compile or run this flow did; **inference** is this
flow's own reasoning.

## 1. What the living has said

The living's order for this book, 2026-10-09, typed, comment on «The
golden ethos» §2 (`FlowId.{ String }`),
`flows/ebbe30/vision/ethos.md`:

> Well, this is already wrong. Ethos should be in the distill vision,
> but single-field structs are forbidden. If it was a string, it would
> be just a new type, and I want the new types not to be type aliases.
> That was never brought back to me. Also, type, new type, and type
> aliases: the difference, why we want new types, or why we might not.
> I need a book on that [...]
>
> First of all, it would not be a struct, and second of all, it should
> not be a string. I don't think we need it. Let's just leave it as a
> string for now, but let's put a comment there that says the string
> is very unideal, and we need a real ID based on the real hash bit
> that we're going to use to identify the flows.

The same comment: "There are some invariants that we want to enforce
in the code." (also `flows/445410/vision/ethos.md`, "Invariants the
code enforces").

**New types, not type aliases**, 2026-10-06, comment on
`pub type FlowId = String;` in «The code» 1st edition,
`flows/d4ae97/vision/ethos.md`:

> Isn't that a type alias? We want new types not type aliases. Let's
> look at what this is in practice on the Rust side and what the
> differences are. From memory I don't think I want type aliases. I'm
> pretty sure I want... I think they're called the single tuple new
> types or just new type for short. I think the properties of those
> are more interesting than these type aliases, which I think don't
> really offer much in terms of correctness but you're welcome to
> correct me.

**The new type's syntax**, 2026-09-08, typed,
`flows/8e9e77/vision/single-field-structs.md`, on `X.{ T }`:

> Which, as I was talking in the other flow, is something that I want
> to make illegal now because it's absurd. This should be a new type
> and not a struct with just a single element in it.
>
> Then the implementation is wrong because a new type should be just
> the name of the type and then the separator, which is a period, and
> then the name of the contained type. [...] It would be absurd to
> make a new type that contains another complex type. A new type
> generally is like `name.string`, `age.integer`, or whatever we use:
> `int`.

Same file, same date: "I think we should possibly even refuse
single-field struct types and ethos, and instruct against them even
in Rust, because those should be new types."

**A one-position type is called a new type**, 2026-10-06, comment on
«Ethos, distilled» proposal 7, `flows/d4ae97/vision/ethos.md`:

> No it's not. It's named `a.` and that's a type. It's a new type,
> which is explained syntactically elsewhere. [...] We're engineers
> here. We're going to call things what they are and that's a new
> type.

**Don't double-wrap**, 2026-10-06, comment on `Role.[ Voice Job ]`,
Job wrapping a FlowId, `flows/d4ae97/vision/ethos.md`:

> If a job is a flow ID, then why are we even using the word "job"?
> Just use "flow ID". Why are you going to wrap a new type with
> another new type? Don't double-wrap types. That's silly.

Earlier, 2026-08-07, `flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md`:
"is it a newtype around another newtype? Looks really confusing to
me." and "And what are the double new type wrapping about? I don't
like it. I don't like the single field struct."

**Single-field structs**, 2026-09-03, STT,
`flows/e4a40e/vision/archive-newtypeWrappingAndSingleFieldStructs.md`:
"it creates a single-field struct, which would be really bad design,
and I would never want that kind of pattern to start spreading."

**Tuples; the newtype is allowed**, 2026-08-22,
`flows/cff271af/vision/tuples.md`:

> the newtype is allowed. the fact that its a tuple is unfortunate
> for us, so it would have to be mentionned in case. [...] I really
> dont like tuples, they're a form of un-specification

**A new type for a thing built from two things**, 2026-08-21,
`vision-raw/mainFunction.md`: "if you build a thing from two things,
so then can't you just create a new type that can be created?"
(Here "new type" means a newly declared type, not the one-position
wrapper.)

**Inline declaration is "a new type"**, `flows/e8c4cc61/vision/archive-ethosTypes.md`
(undated in file): "So I'm specifying a new type inline. [...] So
that these types will essentially become full types of their own and
not something minor." (Again "new type" in the general sense.)

**The topic name as a new type**, 2026-10-09, STT, relayed by 4ddfe1,
`flows/445410/notion/metaflow-ethos.md`: "the struct, will contain
their details, such as [...] the name of their topic, right? Which
will be a, a new type which I talked about yesterday".

**Special representation** (bears on how a new type reads in datom),
2026-10-09, `flows/445410/vision/ethos.md`: "the special
representation is basically an implementation for a special way to
decode and encode, so that the representation has a different type
than the type when it's read into the Rust runtime. [...] It's a
custom Datom [...]"

**Datom payload cost**, 2026-10-08, STT, `flows/d4ae97/vision/ethos.md`:
"the guiding principle in designing the ethos and the datom payload
is also keeping in mind what the datom payload looks like,
considering that the datom will probably be more expensive because
machines will have to output them."

Not found: no record on "nominal" or "structural" typing as such
(the hits for `Nominal` are a kind name in `flows/995a164e/vision/kinds.md`
and `flows/62022e8f/vision/archive-designPractice.md`). "Alias" in
`flows/e8c4cc61/vision/archive-kinds.md` ("Embodied, which is an
alias of Sized") and `flows/62022e8f/vision/archive-kinds.md` is about
kinds, both archived.

**Read, the distilled skill today**: `vision-ethos` still says
"FilePath is an alias of String" and shows
`pub type LockId = Integer;` as what `LockId.Integer` turns into; its
section "Every declared type bears both kinds" says "an alias is not
a new type and cannot carry a derive." The two rulings above
(2026-10-06, 2026-10-09) are not yet in it.

## 2. Ethos Zero today

Read at ethos-zero `c2653d`, under the `Repository root` skill
variable, `github.com/LiGoldragon/ethos-zero`.

The declaration enum, `src/lib.rs` 277-286:

```rust
pub enum TypeDeclaration {
    /// A headed brace: the positions in order.
    Struct(Identity, Vec<Position>),
    /// A headed bracket: the variants.
    Enum(Identity, Vec<Variant>),
    /// A headed bare: the aliased type.
    Alias(Identity, Reference),
}
```

There are three forms: struct, enum, alias. **No new type construct
exists.** `Name.Type` is read as an alias and emitted as `pub type`
(`src/generation.rs` 876-886):

```rust
quote! { #[rustfmt::skip]
  pub type #name #parameters = #aliased; }
```

Fixture `fixtures/orchestrate.ethos` 6-8:

```
[ LockId.Integer
  LockName.String
  FlowId.String
```

Committed output `tests/generated/orchestrate.rs` 2-7:

```rust
#[rustfmt::skip]
pub type LockId = i64;
#[rustfmt::skip]
pub type LockName = String;
#[rustfmt::skip]
pub type FlowId = String;
```

A struct carries derives; an alias carries none
(`orchestrate.rs` 14-22):

```rust
#[derive(rkyv::Archive, rkyv::Serialize,
  rkyv::Deserialize, Clone, Debug,
  PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom",
  derive(datom_codec::Datomizable,
         datom_codec::Composing))]
pub struct LockRequest {
    pub lock_name: LockName,
    pub flow_id: FlowId,
    ...
}
```

**A single-field struct is accepted today.**
`fixtures/tree-types.ethos` 11 `Loop.{ Knot }` and 14
`B.{ String }` generate; `tests/generated/tree-types.rs` 138-141:

```rust
pub struct Loop {
    #[rkyv(omit_bounds)]
    pub knot: std::boxed::Box<Knot>,
}
```

The alias is also used to name a defined type a second time:
`orchestrate.ethos` 14 `DuplicateName.Lock` emits
`pub type DuplicateName = Lock;` (`orchestrate.rs` 34), a double name
for one type.

Read, a side finding: the generated code gates the datom derives on
`feature = "datom"` (`src/generation.rs` 782), while the
`knowledge-ethos` skill says the feature is `knowledge-datom`.

### A hand-written new type exists, outside ethos

ethos-zero's own `Name`, `src/lib.rs` 56-84, is a new type that holds
an invariant from construction:

```rust
pub struct Name(String);

impl TryFrom<&str> for Name {
    type Error = String;
    fn try_from(text: &str)
        -> Result<Self, Self::Error> {
        if !text.starts_with("r#")
            && (text == "Self"
                || syn::parse_str::<syn::Ident>(
                    text)
                    .is_ok())
            && !text.is_empty()
        { Ok(Self(text.to_owned())) }
        else { Err(text.to_owned()) }
    }
}
```

datom-codec holds two more, `src/composition.rs` 339
`pub struct Meaning(pub Opaque);` and `src/decimal.rs` 43
`pub struct Decimal(f64);`, with hand-written datom impls.

### How each reads in datom today

Witnessed, scratch crate on datom-codec `4dff16`, derive as ethos
emits it:

```rust
pub type FlowAlias = String;
#[derive(Datomizable, Composing)]
pub struct FlowId(pub String);
```

Output:

```
alias: abc123
newtype: { abc123 }
```

The derive treats a one-field tuple struct as a struct of arity one
(`crates/datom-codec-derive/src/lib.rs` 103 and the `Form::Struct`
arm near 196), so a new type through today's derive costs a brace pair
in every datom. An alias costs nothing. A new type that reads as its
inner value (`abc123`) needs either a hand-written impl, as `Decimal`
and `Meaning` have, or a derive change.

## 3. Engineering reasons, wrong form and right form

The ethos right form below, `FlowId.String` generating a new type, is
the shape the living ruled (2026-09-08, 2026-10-06); Ethos Zero does
not generate it today.

### 3.1 No accidental mixing

Witnessed (rustc). With aliases, a lock name passes where a flow id
is wanted; it compiles.

Wrong, ethos then Rust:

```
[ FlowId.String
  LockName.String ]
```

```rust
type FlowId = String;
type LockName = String;
fn release(_f: FlowId) {}
let n: LockName = "x".into();
release(n); // compiles
```

Right:

```rust
struct FlowId(String);
struct LockName(String);
fn release(_f: FlowId) {}
let n = LockName("x".into());
release(n); // error[E0308]
```

An alias is a second name for the same type; the checker sees only
`String`. A new type is a distinct type (nominal), so the compiler
refuses the mix.

### 3.2 Traits can be implemented on it

Witnessed (rustc). Wrong:

```rust
type FlowId = String;
impl std::fmt::Display for FlowId { .. }
// error[E0117]: only traits defined in the
// current crate can be implemented for
// types defined outside of the crate
```

Right:

```rust
struct FlowId(String);
impl std::fmt::Display for FlowId { .. }
```

The orphan rule forbids a foreign trait on a foreign type; an alias of
`String` is `String`. A new type is local, so foreign kinds (Display,
Datomizable, a special representation) and its own kinds attach to
it. This matters for ethos associations: `FlowId.[ Hashable ]` can
only be an interaction on a type that exists. It is also what the
living's special representation needs: a type of its own to carry a
custom datom conversion.

### 3.3 Invariants held at construction

Read (ethos-zero `Name`, above). Wrong:

```rust
type Name = String;
let n: Name = "r#bad name".into();
// any string is a Name
```

Right:

```rust
struct Name(String);
let n = Name::try_from("Lock")?;
// only a valid identifier is a Name
```

With the inner field private and a `TryFrom` as the one way in, every
value of the type has passed the check, and no later code re-checks
it. This is the mechanism for the living's "invariants that we want
to enforce in the code". For FlowId, the flow inference is: once the
real hash-based id exists, its new type is where its validity lives.

### 3.4 Zero cost

Witnessed (rustc): `size_of::<FlowId>()` and `size_of::<String>()`
both print 24. A one-field struct has its field's layout; with
`#[repr(transparent)]` that is guaranteed. Wrapping adds no runtime
cost.

### 3.5 A derive per type

Read (`orchestrate.rs`). An alias carries no derive, so `FlowId`
bears rkyv, Hash, Datomizable only because `String` does. A new type
carries the generated derive like every struct and enum, so "every
ethos-declared type bears both kinds" holds without the alias
exception the `vision-ethos` skill writes today.

### 3.6 Why one might not (the costs)

- Datom payload. Witnessed above: through today's derive a new type
  reads `{ abc123 }`, not `abc123`. Against the living's 2026-10-08
  principle on datom payload cost, a new type should read as its
  inner value. Flow inference: the generator or the derive gives a
  new type the inner type's form, a transparent form, so the text is
  the same as with an alias.
- Access. Inference from Rust: a new type does not deref to its
  inner type; reading it needs `AsRef`, a getter, or a `From`
  into the inner type. Ethos Zero would emit these or the bodies are
  hand-written.
- Double wrapping. A new type over a new type (`Job` over `FlowId`)
  adds a name with no new meaning; the living rejected it
  (2026-10-06). The same applies to today's alias of a declared type
  (`DuplicateName.Lock`).
- Container aliases. Read: `LockPaths.Vector<LockPath>` and
  `Forest.Vector<Tree>` are aliases of containers. The living's
  ruling names `name.string` and `age.integer` and calls a new type
  over "another complex type" absurd (2026-09-08). Whether
  `Name.Vector<T>` becomes a new type, stays an alias, or is written
  inline is not ruled; open question for the living.

## 3a. Further records: the special representation, the identifier, the audit

Which vision counts, by the living's rule as relayed by the
coordinator: "the recent vision and the one that's been repeated a
lot, which hasn't been overridden by newer decisions or statements",
raw records included. Lines a newer statement overrides are marked
**[overridden]** with what overrides them.

**`flows/445410/vision/ethos.md`** (2026-10-09, STT, relayed by
ebbe30) holds two entries, both quoted in section 1: "The special
representation" and "Invariants the code enforces". On types, it
says a type keeps its real Rust type in ethos, and a trait gives it a
different representation in datom: "In Ethos, we're going to
describe the real type, the real Rust type that it has, and then the
special representation is going to implement the representation
type. We could maybe even somehow describe that type in Ethos, what
that representation type is, which would be interesting because then
we would force the input and output types, and we would let Rust do
the implementation." Inference: a trait such as this can be
implemented only on a type of its own (3.2), so the special
representation needs new types; an alias of `String` cannot carry
it.

**The flow id as a hash**, `flows/edf227/vision/identifiers.md`,
2026-10-03, STT (cited by audit C4):

> The flow ID is not a string, it's a hash. [...] I would like this
> to be a serialization and deserialization thing so that it's not
> actually in the Nexus. The Nexus just thinks of it as a hash, which
> is maybe an integer with certain kinds of traits. In the
> deserialization, we can have special implementations, maybe, so
> that a certain kind of thing is deserialized with a certain kind of
> algorithm that creates an alphanumeric hash from a string [...]

Same file, 2026-10-03, typed: "First of all it's not an integer,
it's a hash, right? [...]". Inference: this is the clearest case in
the records for a new type with a special representation: one Rust
type, a hash with its own kinds, read and written as alphanumeric
text by a custom datom conversion.

**[overridden for now]** The 2026-10-03 hash ruling sets the
destination, but the living's 2026-10-09 comment sets today's shape:
"Let's just leave it as a string for now, but let's put a comment
there that says the string is very unideal, and we need a real ID
based on the real hash bit that we're going to use to identify the
flows." The hash remains the target (the 2026-10-09 comment repeats
it); the near-term type is a new type over String with that comment.

**Audit C3-C6**, `flows/ebbe30/reports/book-audit-verified.md`
76-84, a flow's findings (claims, witnessed by ebbe30 against
psyche-skills `4312cc0`; not re-read here except as noted):

- C3, line 78: "P/vision-ethos.md:226, current: "[ FilePath.String ;
  types: FilePath is an alias of String"; line 234: "pub type
  FilePath = String;". The same holds at :206-207 and :323-324."
  Its ruling: "We want new types not type aliases."
  (`flows/d4ae97/vision/ethos.md`:82, 2026-10-06, re-read here and
  matches). Its replacement: "[ FilePath.String ; types: FilePath is
  a new type holding String", and at 234 "pub struct
  FilePath(String);". "The other aliases change the same way."
  This agrees with the read of the `vision-ethos` skill in section 1.
- C4, line 80: "P/vision-ethos.md:316 and :325, current:
  "FlowId.String" and "pub type FlowId = String;"." Its ruling: "The
  flow ID is not a string, it's a hash." (edf227, 2026-10-03). Its
  replacement: "FlowId.Integer" and "pub struct FlowId(Integer);";
  "the type is I and waits on D2." **[overridden in part]** The
  new-type form stands (2026-10-06, 2026-10-09). The `Integer`
  content is ebbe30's inference, against "it's not an integer, it's
  a hash" (2026-10-03 typed), and the 2026-10-09 comment keeps it a
  String for now. Flow inference: `FlowId.String`, generating
  `pub struct FlowId(String);`, with the living's comment.
- C5, line 82 and C6, line 84: Sema renamed Memory in
  `vision-ethos` and `vision-sema`. Nothing on type, new type or
  alias.

Further lines in the same audit bearing on new types:

- Line 34, «Datom» bad807: "replace `FlowId.{ Integer }` with
  `FlowId.Integer` (v2:112, 189, 214); replace `{ 12232711 }` with
  `12232711` (v2:122, 255)". This assumes a new type reads in datom
  as its bare inner value. Today's derive writes the braces
  (witnessed, section 2), so that datom form needs a transparent
  form in the derive or generator.
- Line 47, «Curriculum, a vision in ethos»: ""Every semantic string
  has a named struct type" becomes "Every semantic string has a new
  type, Name.Type"; `Text.{ String }` becomes `Text.String`, and
  every other one-position struct changes the same way
  (8e9e77/vision/single-field-structs.md, 2026-09-08;
  d4ae97/vision/ethos.md:49)."
- Line 37, «Clojure, the vision»: "add "LockName.String is a new
  type, not an alias." (see C3)".

### Override marks on section 1

- `vision-ethos` skill, "FilePath is an alias of String", "an alias
  is not a new type and cannot carry a derive", and every
  `pub type X = String;` it shows for `X.String`: **[overridden]** by
  2026-10-06 and 2026-10-09 ("new types not type aliases").
- 2026-09-08, "I think we should possibly even refuse single-field
  struct types": the hedge is **[overridden]** by 2026-10-09, "single-field
  structs are forbidden".
- `flows/d63804f2` (2026-08-07), `flows/e4a40e` (2026-09-03),
  `flows/cff271af` (2026-08-22) and the "don't double-wrap" record
  (2026-10-06): not overridden; repeated and consistent.
- `vision-raw/mainFunction.md` (2026-08-21) and
  `flows/e8c4cc61/vision/archive-ethosTypes.md` use "new type" in
  the general sense of a newly declared type; not overridden, but a
  different sense from the one-position new type.
- Ethos Zero's `Name.Type` emitting `pub type` (section 2) is code,
  not vision; it is out of line with the 2026-10-06 and 2026-10-09
  rulings.

## 4. Open questions for the book

- Does `Name.Vector<T>` (and `Name.Option<T>`) become a new type, or
  is it refused with a direction to declare inline?
- Does `Name.DeclaredType` (`DuplicateName.Lock`) become an error,
  as a double name?
- Does a new type read in datom as its inner value (transparent),
  or as a one-position struct?
- What does Ethos Zero emit for access: `AsRef`, `From`, a
  `TryFrom` hook for invariants written by hand?

## Sources

- `flows/ebbe30/vision/ethos.md` (2026-10-09 comments)
- `flows/d4ae97/vision/ethos.md` (2026-10-06 to 2026-10-08)
- `flows/8e9e77/vision/single-field-structs.md` (2026-09-08)
- `flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md`
- `flows/e4a40e/vision/archive-newtypeWrappingAndSingleFieldStructs.md`
- `flows/cff271af/vision/tuples.md` (2026-08-22)
- `vision-raw/mainFunction.md` (2026-08-21)
- `flows/e8c4cc61/vision/archive-ethosTypes.md`
- `flows/445410/vision/ethos.md`, `flows/445410/notion/metaflow-ethos.md`
- `flows/edf227/vision/identifiers.md` (2026-10-03)
- `flows/ebbe30/reports/book-audit-verified.md` 34, 37, 47, 76-84
  (ebbe30's claims)
- Skills `vision-ethos`, `knowledge-ethos`, `knowledge-datom`
- ethos-zero `c2653d`: `src/lib.rs`, `src/generation.rs`,
  `fixtures/orchestrate.ethos`, `fixtures/tree-types.ethos`,
  `tests/generated/orchestrate.rs`, `tests/generated/tree-types.rs`
- datom-codec `4dff16`: `crates/datom-codec-derive/src/lib.rs`,
  `src/composition.rs`, `src/decimal.rs`
- Witness runs: rustc on four scratch files (alias mixing compiles,
  newtype mixing E0308, Display on alias E0117, size 24 = 24); a
  scratch crate on datom-codec printing alias and newtype datoms.
  Scratch under this session's scratchpad; not kept.
- Provenance receipt: unavailable.
