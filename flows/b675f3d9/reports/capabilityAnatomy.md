# Capability Anatomy

## 1. The anatomy of a trait function signature

### Seven signatures spanning the space

```rust
fn len(&self) -> usize;                                                // Q: pure query
fn push(&mut self, item: T);                                           // M: mutation
fn into_bytes(self) -> Vec<u8>;                                        // C: consumer
fn create(config: Config) -> Self where Self: Sized;                   // K: constructor
async fn fetch(&self, key: &str) -> Payload;                           // A: async effect
fn try_from(value: T) -> Result<Self, Self::Error> where Self: Sized;  // F: fallible conversion
fn convert<V: From<Self::Output>>(&self) -> V;                         // G: generic method
```

### Exhaustive dissection

Slot: which part of the capability this constituent belongs to. IDENTITY = what makes this capability *this* capability; INPUTS = what enters; OUTPUT = what comes out; MODE = how it touches its bearer or the world; ASSEMBLY = Rust-only plumbing, eliminated or absorbed in Ethos.

| # | Constituent | What it is | Card. | Slot | Ethos (no generics, only kinds) | In |
|---|---|---|---|---|---|---|
| 1 | **name** | method identifier | 1 | IDENTITY | capability name | all |
| 2 | **`async`** | async qualifier | 0..1 | MODE | tbd -- whether the capability awaits | A |
| 3 | **`const`** | const-evaluable qualifier | 0..1 | ASSEMBLY | eliminated (compile-time concern) | -- |
| 4 | **`unsafe`** | safety contract qualifier | 0..1 | MODE | tbd | -- |
| 5 | **`extern`** | ABI qualifier | 0..1 | ASSEMBLY | eliminated (FFI plumbing) | -- |
| 6 | **lifetime params** | `<'a, 'b: 'a>` on the method | 0..n | ASSEMBLY | eliminated (borrow mechanics) | -- |
| 7 | **type params + bounds** | `<V: From<Output>>` | 0..n | INPUTS | each param becomes a kind; each bound IS a kind | G |
| 8 | **const generic params** | `<const N: usize>` | 0..n | ASSEMBLY | tbd -- value, not a kind | -- |
| 9 | **self: none** | no receiver | -- | MODE | creates (constructor) | K, F |
| 10 | **self: `&self`** | shared reference | -- | MODE | reads the bearer | Q, A, G |
| 11 | **self: `&mut self`** | exclusive reference | -- | MODE | changes the bearer | M |
| 12 | **self: `self`** | by value | -- | MODE | consumes the bearer | C |
| 13 | **self: `Box`/`Arc`/`Rc`/`Pin`** | smart-pointer receiver | -- | MODE+ASSEMBLY | semantic per #10-12; wrapper = assembly | -- |
| 14 | **`where Self: Sized`** | object-safety gate | 0..1 | ASSEMBLY | eliminated (dispatch concern) | K, F |
| 15 | **param pattern** | variable name (`item`, `key`) | 0..n | INPUTS | tbd -- name or positional | M,K,A,F |
| 16 | **param type** | the type of each param | 0..n | INPUTS | input kind | M,K,A,F |
| 17 | **`impl Trait` in param** | anon bounded param | variant of 16 | INPUTS | input kind (bounds = kinds) | -- |
| 18 | **`&`/`&mut` on param** | borrow/mutability on param | per param | ASSEMBLY | eliminated (borrow mechanics) | A |
| 19 | **`dyn Trait`** | trait object | variant of 16 | INPUTS | kind (the trait = the kind) | -- |
| 20 | **return: `()`** | unit / void | -- | OUTPUT | no yield | M |
| 21 | **return: concrete** | named type | -- | OUTPUT | yield kind | Q, C, A |
| 22 | **return: `Self`** | the type itself | -- | OUTPUT | yields the bearer kind | K |
| 23 | **return: `Self::Assoc`** | associated type | -- | OUTPUT | yields the associated kind | -- |
| 24 | **return: `impl Trait`** | RPITIT | -- | OUTPUT | yield kind (bounds = kinds) | -- |
| 25 | **return: `Result<T, E>`** | success-or-failure | -- | OUTPUT | yield kind + refusal kind | F |
| 26 | **return: `Option<T>`** | present-or-absent | -- | OUTPUT | optional yield kind | -- |
| 27 | **return: `!`** | diverging / never | -- | OUTPUT | diverges | -- |
| 28 | **where clause** | extra bounds | 0..n | ASSEMBLY | absorbed into kind constraints | K, F |
| 29 | **default body** | provided implementation | 0..1 | MODE | provided capability (default interaction) | -- |
| 30 | **attributes** | `#[must_use]`, `#[deprecated]` | 0..n | ASSEMBLY | tbd | -- |

30 constituents. 11 are ASSEMBLY (eliminated or absorbed). What survives:

| Category | What remains |
|---|---|
| IDENTITY | name |
| INPUTS | param types as kinds, type params as kinds, `impl Trait` as kind, `dyn Trait` as kind |
| OUTPUT | yield kind, refusal kind (from `Result`), optional yield, no yield, diverges |
| MODE | bearer mode (reads/changes/consumes/creates), async, unsafe, provided |


## 2. What a capability is

Derived from the table above.

### Minimal slots

| Slot | What fills it | Identity? |
|---|---|---|
| **name** | identifier | yes |
| **input kinds** | what enters (0..n kinds) | no |
| **yield kind** | what comes out on success (0..1 kind) | no |
| **refusal kind** | what comes out on failure (0..1 kind) | no |
| **bearer mode** | reads / changes / consumes / creates | no |
| **provided** | whether a default interaction exists | no |

**Identity.** In Rust, the method name alone distinguishes methods within a trait -- no overloading. Two capabilities of one kind cannot share a name. The name is the sole identity.

**Input kinds.** Each non-self parameter type becomes an input kind. Method-level type parameters (`<V: From<Output>>`) become kind positions with kind requirements. `impl Trait` in parameter position becomes an anonymous kind. References, mutability, and lifetimes on parameters are assembly.

**Yield kind.** The return type, stripped of `Result`/`Option` wrappers. `Self` yields the bearer kind. `Self::Assoc` yields the associated kind. `()` = no yield. `!` = diverges.

**Refusal kind.** The `E` in `Result<T, E>`. Compare the signal interface's refusal section:

```
;; spirit interface, section 3 (refusals):
[AdmissionRejected.{GuardianReason Explanation}  QueryRejected.{QueryRefusal Explanation}]
```

The signal interface separates the triple into three top-level sections because multiple requests may share a refusal type and each has its own name (`Record` -> `Recorded` -> `AdmissionRejected`). A capability unifies the triple under one name: `register` takes `PathLock`, yields `Registered`, may refuse with `Refused`. The name is the shared identity.

Not every capability has a refusal. `len` cannot fail in its type-level contract. `into_bytes` consumes and yields without failure. A refusal slot is present only when the capability's Rust signature wraps its return in `Result` or the Ethos declaration names a refusal kind.

**Effect vs conversion (the punch teaching).** "You wouldn't punch somebody to try and break your own knuckles." The psyche's distinction:

- **Effect:** the action changes the world; the yield is incidental. `register` changes the nexus's state; `Registered` tells you it happened.
- **Conversion:** the yield IS the point. `into_bytes` exists to produce `Bytes`.

Does this belong in the capability declaration? The signal interface does not mark it -- requests do not say whether the response is the point or a side effect. Bearer mode partially captures the distinction: effects that change state will have mode `changes`; pure conversions will have mode `consumes` or `reads`. The punch teaching may be fully expressed by mode + refusal without a separate marker. I do not know; this is for the psyche.

**Required vs provided.** A provided capability has a default interaction body -- interactors may override, not must implement. Whether this is marked in the kind or only visible in the interaction is open.

**Async and unsafe.** The table marks them as MODE, not ASSEMBLY -- they carry real semantic content (the capability awaits; the capability's contract is not compiler-checked). Whether they appear in the kind declaration is unruled.


## 3. The self-form question

Rust has six receiver forms. Four are semantically distinct; two are wrappers:

| Rust form | Semantic | Wrapper? |
|---|---|---|
| none | no bearer involvement | -- |
| `&self` | reads the bearer | -- |
| `&mut self` | changes the bearer | -- |
| `self` | consumes the bearer | -- |
| `self: Box<Self>` | consumes | Box is the wrapper |
| `self: Arc<Self>` / `Rc<Self>` | reads via shared ownership | Arc/Rc is the wrapper |
| `self: Pin<&mut Self>` | changes, pinned in memory | Pin is the wrapper |

### For: Ethos's business

The four semantic forms express information the caller needs:

- A `consumes` capability destroys the bearer. Calling it means the bearer is gone.
- A `changes` capability may alter state. Calling sequence matters.
- A `reads` capability is safe to call without mutation concerns.
- A `creates` capability is how bearers come into existence.

This is the anatomy of the machine. The psyche wants the map to show the machine's shape. Hiding whether a capability eats its bearer behind the interaction means the map does not show that shape.

### Against: assembly

The receiver form -- reference, Box, Pin -- is Rust machinery. `&self` vs `&mut self` is how the borrow checker enforces the semantic. A language above Rust would express the semantic ("reads", "changes") without the mechanism ("shared reference", "exclusive reference"). Even the four-way semantic split may be too fine for the declaration level: the interaction is where the contract becomes concrete.

### Position

**The semantic is Ethos's business. The mechanism is assembly.** Four bearer modes: reads, changes, consumes, creates. Collapse Box/Arc/Rc/Pin into their semantic equivalent. Drop `where Self: Sized`. The four modes are exhaustive: every capability either involves its bearer in one of three ways, or does not involve it at all.

How the mode is expressed -- per-entry marker, section grouping, or something else -- is the design question for section 4.


## 4. Shape candidates

Six capabilities, same set for each shape:

```rust
fn len(&self) -> usize;                                                // Q: reads, no input, yields
fn push(&mut self, item: Item);                                        // M: changes, one input, no yield
fn into_bytes(self) -> Bytes;                                          // C: consumes, no input, yields
fn create(config: Config) -> Self where Self: Sized;                   // K: creates, one input, yields Self
fn register(&mut self, lock: PathLock) -> Result<Registered, Refused>; // E: changes, one input, yield + refusal
async fn fetch(&self, key: Key) -> Payload;                            // A: reads, one input, yields
```

Kind-name translations: `usize` -> `Count`. `Item` is a kind position. `Bytes`, `Config`, `PathLock`, `Registered`, `Refused`, `Key`, `Payload` are kinds. The lean: existing Rust trait names (Display, Clone, Send) may be kept as-is; the qualifier form (Displayable, Clonable, Sendable) is the default. Both shown in the full declaration.

### (a) Per-capability struct, sections confer inside

Each capability is either `name.yield` (no inputs, no refusal) or `name.{[inputs] yield refusal}` (complex). Sections inside the struct mirror the signal interface triple: section 1 (vector) = input kinds, section 2 = yield kind, section 3 = refusal kind. Absent sections = absent slots.

```
len.Count                                  ;; Q: no inputs, yields Count
push.{[Item]}                              ;; M: inputs [Item], no yield
into_bytes.Bytes                           ;; C: no inputs, yields Bytes
create.{[Config] Self}                     ;; K: inputs [Config], yields Self
register.{[PathLock] Registered Refused}   ;; E: inputs [PathLock], yields Registered, refuses Refused
fetch.{[Key] Payload}                      ;; A: inputs [Key], yields Payload
```

Two heads everywhere: `name.yield` or `name.{struct}`. Non-repetition: each datum appears once. No generics: every position is a kind.

**Runs out at:** bearer mode not expressed -- a reader cannot tell from `register.{...}` whether it reads, changes, or consumes. Async not expressed. Required vs provided not expressed. A capability with no inputs but a refusal needs an empty inputs section: `validate.{[] Valid Invalid}`.

**Cost:** Capabilities with inputs pay the struct tax. No bearer mode means the map does not fully show the machine's shape.

**Note:** The capability struct mixes a vector field (`[PathLock]`) and plain-type fields (`Registered`, `Refused`) in one struct. The existing fixtures do not show this pattern -- interface structs use only vector sections, normal structs use only plain-type fields. Whether protos supports this mix or needs a different encoding is open.

### (b) Mode sections group capabilities

Capabilities grouped into sub-sections by bearer mode. Sections confer (the psyche's ruling applied to the capability level): sub-section 1 = reads, 2 = changes, 3 = consumes, 4 = creates. Each entry uses the form from (a).

```
[
  [                                    ;; reads bearer
    len.Count
    fetch.{[Key] Payload}
  ]
  [                                    ;; changes bearer
    push.{[Item]}
    register.{[PathLock] Registered Refused}
  ]
  [                                    ;; consumes bearer
    into_bytes.Bytes
  ]
  [                                    ;; creates (no bearer)
    create.{[Config] Self}
  ]
]
```

**Runs out at:** async, required vs provided. Mode IS expressed (structurally) -- the gain over (a).

**Cost:** Four sub-sections, even when some modes are empty (a kind with no constructors needs `[]` in position 4). Nesting depth: kind struct > capabilities section > mode sub-section > capability entry -- three bracket levels. Adding a capability means knowing its bearer mode up front.

### (c) Yield-only declaration

The kind declaration carries only name and yield kind. Inputs, mode, refusal, async live in the interaction.

```
len.Count
push
into_bytes.Bytes
create.Self
register.Registered
fetch.Payload
```

**Runs out at:** inputs, mode, refusal, async, required vs provided -- nearly everything. This was the prior report's shape (`process.Output`) and the psyche judged it: "You havent actually thought about this."

**Cost:** The map loses the machine's shape. The psyche cannot see what a capability takes or what can go wrong. The non-repetition argument is real (inputs live in the interaction, do not repeat here), but the psyche ruled: "I don't think we can just define traits implicitly ... it's going to be complex to try to extract what that trait actually is and how many interactions it has." A yield-only declaration does not tell you what the capability actually is.

### The winning shape

**(a) with the open question of mode from (b).**

Shape (a) is the right capability entry -- it carries the signal-interface triple (inputs, yield, refusal) without repetition. Shape (c) loses too much. Shape (b) solves mode but adds nesting.

Whether mode is expressed by sectional grouping (b), by a per-entry marker, or left to the interaction is open. Two alternatives for the full kind declaration:

**Flat (mode not in the kind declaration):**

```
Processable<[Clonable Sendable] Serializable>.{
  [Displayable Debuggable Sendable]               ;; superkinds (qualifier form)
  [Output]                                         ;; associated kinds
  [                                                ;; capabilities
    len.Count
    push.{[Item]}
    into_bytes.Bytes
    create.{[Config] Self}
    register.{[PathLock] Registered Refused}
    fetch.{[Key] Payload}
  ]
}
```

**With mode sections (mode in the declaration):**

```
Processable<[Clonable Sendable] Serializable>.{
  [Display Debug Send]                             ;; superkinds (Rust names per the lean)
  [Output]                                         ;; associated kinds
  [                                                ;; capabilities
    [                                              ;;   reads
      len.Count
      fetch.{[Key] Payload}
    ]
    [                                              ;;   changes
      push.{[Item]}
      register.{[PathLock] Registered Refused}
    ]
    [                                              ;;   consumes
      into_bytes.Bytes
    ]
    [                                              ;;   creates
      create.{[Config] Self}
    ]
  ]
}
```


## 5. Recommendation

A capability is `name.yield` or `name.{[inputs] yield refusal}`, mirroring the signal interface's triple. Bearer mode (reads/changes/consumes/creates) is real semantics, not assembly, and belongs in the declaration -- whether by section grouping or per-entry marker is the open question. Async, required-vs-provided, and the struct-with-mixed-fields encoding need the psyche's eye before they can be settled.


## 6. Open questions

1. Do mode sub-sections (reads/changes/consumes/creates) group capabilities, or is mode a per-entry marker?
2. Is async expressed in the kind declaration (marker? mode variant?), or only in the interaction?
3. Are required vs provided capabilities distinguished in the kind, or is that the interaction's concern?
4. Method-level type parameters (`convert<V: From<Output>>`) -- do they become capability-level kind positions?
5. A capability struct mixing vector and plain-type fields (`register.{[PathLock] Registered Refused}`) -- is this valid protos, or does it need a different encoding?
6. Are parameter names (`push`'s `item`, `fetch`'s `key`) expressed, or are inputs positional-only?
7. Is `Self` as a yield kind written literally, or does the kind's own name substitute?
8. Do existing Rust trait names (Display, Clone, Send) stay as-is in superkind positions, or does qualifier form always apply?
9. Is effect vs conversion (the punch teaching) marked in the declaration, or emergent from mode + refusal?
10. Does `Optional` wrapping a yield (the capability may produce nothing) differ from no yield (the capability returns unit)?
11. Can multiple capabilities share a refusal kind at the kind level (a kind-level refusal section, as the signal interface does), or is refusal always per-capability?


## 7. Sources

### Ground (read before designing)

- flows/b675f3d9/vision/kinds.md -- today's rulings on kind/capability vocabulary, identity, and the psyche's feedback on the prior report
- flows/b675f3d9/reports/rustTraitAnatomy.md -- the prior study; capability treatment rejected
- flows/b675f3d9/reports/ethosAnatomyVision.md -- the full psyche corpus on ethos/anatomy (dated, verbatim)
- flows/f426777b/vision/nexusTraits.md -- the punch teaching (effect vs conversion) and three-heads rejection
- Vision/datom.md -- protos syntax reference (heads, structs, vectors, enums)
- Vision/ethos.md -- what Ethos is and why

### Living fixtures (syntax witness)

- /git/github.com/LiGoldragon/ethos-monolith/fixtures/psyche/interface.ethos -- signal interface with 5-section struct
- /git/github.com/LiGoldragon/spirit-ethos/interface.ethos -- request/response/refusal/event/types sections
- /git/github.com/LiGoldragon/spirit-ethos/nexus.ethos -- nexus types and roles
- /git/github.com/LiGoldragon/spirit-ethos/sema.ethos -- sema types and tables
- /git/github.com/LiGoldragon/spirit-ethos/meta.ethos -- meta interface with empty sections
- /git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos -- PathLock register/release operations
- /git/github.com/LiGoldragon/signal-agent/ethos/interface.ethos -- agent request/reply/event patterns
- /git/github.com/LiGoldragon/signal-standard/ethos/interface.ethos -- standard types, no requests
- /git/github.com/LiGoldragon/signal-message/ethos/interface.ethos -- message operations
