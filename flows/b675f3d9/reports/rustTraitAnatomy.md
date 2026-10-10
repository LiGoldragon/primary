# Rust Trait Anatomy

## 1. THE ANATOMY OF A RUST TRAIT

### The maximally complex trait

```rust
mod private { pub trait Sealed {} }
use private::Sealed;

#[must_use]
pub unsafe trait Processable<
    'a,
    'b: 'a,
    T: Clone + Send + 'a,
    U = Vec<u8>,
    const N: usize = 16,
>: Display + Debug + Send + Sync + Sealed
where
    T: Hash + Eq,
    U: Into<Vec<u8>>,
{
    type Output: Serialize + DeserializeOwned + 'a = T;
    type Ref<'c>: AsRef<Self::Output> + 'c where Self: 'c;

    const KIND: &'static str;
    const MAX_ITEMS: usize = N;

    fn process(&'a self, input: &T) -> Self::Output;
    fn process_mut(&mut self, input: T) -> Result<Self::Output, Box<dyn Error>>;
    fn into_output(self) -> Self::Output;
    fn boxed_process(self: Box<Self>) -> Self::Output;
    fn pinned_poll(self: Pin<&mut Self>) -> Poll<Self::Output>;
    fn create(config: U) -> Self where Self: Sized;
    async fn fetch(&self, key: &str) -> Self::Output;
    unsafe fn raw_access(&self) -> *const Self::Output;
    fn accept(&self, source: impl Into<T> + Send);
    fn summarize(&self) -> impl Display + 'a;
    fn convert<V: From<Self::Output>>(&self) -> V;

    fn validate(&self, input: &T) -> bool { true }
    fn process_validated(&'a self, input: &T) -> Option<Self::Output> {
        if self.validate(input) { Some(self.process(input)) } else { None }
    }
}

// Related phenomena:
pub auto trait Sendable {}                        // marker trait
trait Readable = Read + BufRead + Send;           // trait alias (nightly)
impl<X: Processable<...>> SomeTrait for X { ... } // blanket impl
```

### Dissection: every distinct constituent

Card. = cardinality (/p = per param, /a = per assoc, /m = per method). Slot = identity | constraint | capability. Gen->Kind = what the no-generics ruling does to this constituent.

| # | Constituent | What it is | Card. | Slot | Ethos term | Gen->Kind |
|---|---|---|---|---|---|---|
| 1 | Name | Identifier of the trait | 1 | identity | Kind name (qualifier: Processable) | -- |
| 2 | Visibility | pub / pub(crate) / private | 0..1 | identity | tbd | -- |
| 3 | `unsafe` marker | Whole-trait unsafe contract | 0..1 | identity | tbd | -- |
| 4 | Supertrait | Trait bound on Self | 0..n | constraint | Superkind (carried kind) | Yes: each IS a kind |
| 5 | Lifetime param | Named borrow scope ('a, 'b) | 0..n | identity | Eliminated (Rust detail) | -- |
| 6 | Type param | Type variable (T, U) | 0..n | identity | Eliminated: position IS a kind | Yes |
| 7 | Type param bound | Trait on type param (T: Clone) | 0..n/p | constraint | Kind(s) that position requires | Yes: each bound IS a kind |
| 8 | Type param default | Fallback (U = Vec<u8>) | 0..1/p | identity | Default kind for that position | Yes |
| 9 | Const generic | Value param (const N: usize) | 0..n | identity | tbd -- value, not a kind | No |
| 10 | Where clause | Extra bounds (T: Hash + Eq) | 0..n | constraint | Absorbed into kind constraints | Yes |
| 11 | Assoc type | Implementor-chosen type (Output) | 0..n | capability | Associated kind | Yes |
| 12 | Assoc type bound | Bound on assoc (Output: Serialize) | 0..n/a | constraint | Kind(s) the assoc kind must carry | Yes |
| 13 | Assoc type default | Fallback (Output = T) | 0..1/a | capability | Default kind | Yes |
| 14 | GAT | Assoc type with own params (Ref<'c>) | 0..n | capability | tbd -- kind with kind params | Partial |
| 15 | Assoc constant | Named value (KIND: &str) | 0..n | capability | tbd -- value, not a kind | No |
| 16 | Assoc const default | Fallback (MAX_ITEMS = N) | 0..1/c | capability | tbd | No |
| 17 | Required method | No default body | 0..n | capability | Capability (required) | -- |
| 18 | Provided method | Has default body | 0..n | capability | Capability (derived?) | -- |
| 19 | Self receiver | &self / &mut self / self / Box / Pin / none | 1/m | cap detail | tbd | -- |
| 20 | Method params | Non-self inputs | 0..n/m | cap detail | Kinds (each param type IS a kind) | Yes |
| 21 | Method return | Output type | 0..1/m | cap detail | Yield kind | Yes |
| 22 | Method type params | Per-method generics (<V: From<...>>) | 0..n/m | cap detail | Eliminated into kinds | Yes |
| 23 | Method qualifiers | async / unsafe / const | 0..3/m | cap detail | tbd | -- |
| 24 | impl Trait in arg | Anonymous bounded param | 0..n/m | cap detail | Kind (bounds are kinds) | Yes |
| 25 | impl Trait in return | Anonymous bounded return (RPITIT) | 0..1/m | cap detail | Yield kind (bounds are kinds) | Yes |
| 26 | Attributes | #[must_use], #[deprecated] | 0..n | identity | tbd | -- |

Count: 26 distinct constituents. Of these, 15 collapse partially or fully under the no-generics ruling: every type-parameterized position becomes a kind reference; every trait bound becomes a kind requirement.

### Related phenomena (not constituents of the declaration)

| Phenomenon | What it is | Ethos |
|---|---|---|
| Marker trait | Trait with no methods (Send, Sync) | Marker kind: bare name, no capabilities |
| Sealed pattern | Private supertrait preventing external impl | tbd |
| Object safety | Rules for `dyn Trait` (no generics, no Sized, etc.) | tbd -- possibly irrelevant (Ethos may not expose dyn) |
| Blanket impl | `impl<T: Foo> Bar for T` -- universal interaction | Interaction (universal) |
| Trait alias | `trait Foo = Bar + Baz` (nightly) | Kind alias? tbd |
| Auto trait | `auto trait Send {}` -- compiler-implemented | tbd |

## 2. WHAT A KIND HOLDS

### Minimal slots derived from the anatomy

The 26 Rust constituents collapse into these Ethos slots after the no-generics ruling eliminates type parameters, lifetime parameters, where clauses, and impl-Trait boundaries into kind references:

| Slot | What fills it | From constituents | Card. |
|---|---|---|---|
| **Kind name** | Qualifier identifier (Processable) | #1 | 1 |
| **Superkinds** | Kinds this kind requires on Self | #4 + #10 (where on Self) | 0..n |
| **Associated kinds** | Kinds the interaction must name (Output, Ref) | #6, #7, #8, #11, #12, #13 | 0..n |
| **Associated values** | Named constants (KIND, MAX_ITEMS) | #9, #15, #16 | 0..n |
| **Capabilities** | Named functions (process, fetch, validate) | #17, #18 | 0..n |

Each capability in turn holds:

| Detail | From constituents |
|---|---|
| Capability name | #17/#18 name |
| Parameter kinds | #20, #22, #24 |
| Yield kind | #21, #25 |
| Self form | #19 |
| Qualifiers | #23 |
| Required/provided | #17 vs #18 |

Whether capabilities carry their full detail in the kind declaration or only `name.yield` (with the rest in the interaction) is open. Non-repetition argues for the latter: the interaction is where the full signature lives; the kind declaration says what capabilities exist and what they yield.

### Ethos-only slots (candidates from the corpus)

These are things the psyche said kinds will "imply which aren't in Rust world" (kinds.md):

| Candidate | Source |
|---|---|
| **Sections confer** | A kind is conferred by section position, not by keyword (sectionsExistToConferTraits.md) |
| **Spoken derivation** | The qualifier form yields speech: "a Registration is Performable" (f426777b proposal) |
| **Carrying** | Which kind carries which capability -- the carrying declaration (ethosAnatomyVision.md) |
| **Effect classification** | Conversion vs effect (the punch teaching, nexusTraits.md) -- tbd |

## 3. SHAPE CANDIDATES

Syntax follows the fixtures exactly. Discrepancy noted: Vision/datom.md says `.(...)` is a string-carrying variant; the fixtures use `Stream.(Query IntentEvent)` for stream declarations. Both `Option<T>` and `Optional<T>` appear in fixtures. The fixtures are followed where they disagree with datom.md.

Each candidate shows three declarations:
- (M) marker kind: Sendable -- no capabilities
- (S) simple kind: Runnable with `run`
- (C) complex kind: Processable from section 1

### (a) One struct -- every kind has the same shape

The kind declaration is always `Name.{[superkinds] [associated kinds] [capabilities]}`. Empty sections shown as `[]`.

```
;; (M) marker
Sendable.{
  []
  []
  []
}

;; (S) simple capability kind
Runnable.{
  []
  []
  [run.Output]
}

;; (C) complex kind
Processable.{
  [Displayable Debuggable Sendable Syncable Sealed]
  [Output.Serializable Ref]
  [
    process.Output
    process_mut.Fallible<Output>
    into_output.Output
    fetch.Output
    validate.Boolean
  ]
}
```

**Cost:** Markers carry three empty sections. Simple kinds carry two. Every kind pays the full section tax.
**Expression runs out at:** capability parameters, self receiver, qualifiers (async/unsafe), required vs provided, associated values.

### (b) Root enum -- sections differentiate kinds of kinds

The document has sections whose position confers the kind of kind. Section 1 = markers, section 2 = capability kinds, section 3 = complex kinds. The section IS the discriminant.

```
;; within a kinds document or kinds section of a nexus document:

;; section 1: markers
[Sendable Syncable Copyable]

;; section 2: capability kinds (name + capabilities, no superkinds)
[
  Runnable.[run.Output]
  Writable.[write.Result]
]

;; section 3: complex kinds (superkinds + associated kinds + capabilities)
[
  Processable.{
    [Displayable Debuggable Sendable Syncable Sealed]
    [Output.Serializable Ref]
    [
      process.Output
      process_mut.Fallible<Output>
      into_output.Output
      fetch.Output
      validate.Boolean
    ]
  }
]
```

**Cost:** A kind's complexity determines its section. Promoting a marker to a bearer moves it between sections -- but gaining a capability IS a categorical change.
**Expression runs out at:** same as (a) for the complex form. Also: a kind with superkinds but no capabilities (e.g., `SafelyProcessable: Processable + Sendable {}`) has no natural section -- it is more than a marker but less than a capability kind.

### (c) Struct with an inner enum classifying capabilities

Every non-marker kind is a struct. An enum inside classifies capabilities by effect type, addressing the punch teaching (conversion vs effect).

```
;; (M) marker
Sendable

;; (S) simple
Runnable.{
  []
  [Performing.[run.Output]]
}

;; (C) complex
Processable.{
  [Displayable Debuggable Sendable Syncable Sealed]
  [
    Converting.[
      process.Output
      into_output.Output
    ]
    Performing.[fetch.Output]
    Querying.[validate.Boolean]
  ]
}
```

**Cost:** Adds an unruled classification vocabulary (Converting, Performing, Querying -- the psyche floated Perform and Apply but has not ruled). Adds a head to every capability group. Every simple kind still needs `[]` for empty superkinds.
**Expression runs out at:** parameters, self receiver, qualifiers. Also: the classification names are speculative. If the psyche does not want capability classification, every capability group would be the same variant -- the enum collapses.

### (d) Shape-discriminated -- the delimiter IS the discriminant

No wrapper. The protos delimiter itself tells you the kind of kind:
- Bare name = marker kind (no capabilities, no superkinds)
- `Name.[capabilities]` = capability kind (capabilities only)
- `Name.{[superkinds] [assoc kinds] [capabilities]}` = complex kind

```
;; (M) marker -- bare name
Sendable

;; (S) simple -- enum form: capabilities as variants
Runnable.[run.Output]

;; (C) complex -- struct form: sections for superkinds, associated kinds, capabilities
Processable.{
  [Displayable Debuggable Sendable Syncable Sealed]
  [Output.Serializable Ref]
  [
    process.Output
    process_mut.Fallible<Output>
    into_output.Output
    fetch.Output
    validate.Boolean
  ]
}
```

A kind with superkinds but no capabilities:

```
SafelyProcessable.{[Processable Sendable]}
```

One section (superkinds only). The section count tells you what is present.

**Cost:** Promoting a bare name to a capability kind changes its syntax form. But form SHOULD change when nature changes. The capability-only enum form `.[...]` and the type-declaration enum form `.[...]` share syntax -- the section confers which is which (kind section vs type section), as protos positional semantics already require.
**Expression runs out at:** same as (a) for the complex form. Gains over (a): markers and simple kinds are maximally terse (no empty sections). Gains over (b): kinds are not sorted by complexity level. Gains over (c): no unruled vocabulary.

## 4. RECOMMENDATION

**(d) Shape-discriminated.** The protos principle -- shape IS meaning, sections confer -- already provides the discriminant. Adding a wrapper (root enum, classification labels, or uniform struct) would be machinery against the grain. Candidate (d) is the only shape where every kind is exactly as complex as it needs to be and nothing is wasted, which is the non-repetition law applied to syntax structure itself.

## 5. OPEN QUESTIONS

1. Does a capability entry carry its parameter kinds and yield (`process.{Input}.Output` -- three heads, rejected), only its yield (`process.Output`), or a collapsed form (`process.{Input Output}`)?
2. Are required vs provided capabilities distinguished in the kind declaration, or is that the interaction's concern?
3. Do method qualifiers (async, unsafe) and self receiver forms appear in the kind declaration or only in the interaction?
4. Are associated values (const generics, associated constants) expressed in kind declarations, and if so, how? They are values, not kinds.
5. Is `Fallible<Output>` the yield for a fallible capability, or are refusals declared separately as in signal interfaces?
6. Where do kind declarations live -- their own document type, a section within nexus.ethos, or inline?
7. Does the qualifier lean seal? Does it reach already-confirmed names (Textualize -> Textualizable, Realize -> Realizable)?
8. `Output` appears as a yield in capabilities AND as an associated kind with bounds -- is that repetition, and which site is authoritative?
9. What replaces the sealed pattern in Ethos (preventing external interactions)?

## 6. Sources

### Ground (read before designing)

- flows/b675f3d9/vision/kinds.md -- today's rulings
- flows/b675f3d9/reports/ethosAnatomyVision.md -- full psyche corpus on ethos/anatomy
- flows/b675f3d9/reports/rememberF426777b.md -- rejected proposal (section 3), terminology research (section 5)
- Vision/ethos.md -- distilled ethos vision
- Vision/datom.md -- distilled datom vision (protos syntax)

### Living fixtures (syntax witness)

- /git/github.com/LiGoldragon/ethos-monolith/fixtures/psyche/interface.ethos
- /git/github.com/LiGoldragon/ethos-monolith/ARCHITECTURE.md
- /git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos
- /git/github.com/LiGoldragon/spirit-ethos/interface.ethos
- /git/github.com/LiGoldragon/spirit-ethos/sema.ethos
- /git/github.com/LiGoldragon/spirit-ethos/meta.ethos
- /git/github.com/LiGoldragon/spirit-ethos/nexus.ethos
- /git/github.com/LiGoldragon/signal-agent/ethos/interface.ethos
- /git/github.com/LiGoldragon/signal-standard/ethos/interface.ethos
- /git/github.com/LiGoldragon/signal-message/ethos/interface.ethos
