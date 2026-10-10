# Structural Forms

## A. THE DISCRIMINATION SPACE

Four axes tell one structural form from another at zero or one extra token.

### Axis 1: body delimiter after the head

| Body form | Example | Protos shape | Scanner |
|---|---|---|---|
| none | `Sendable` | Bare | Working |
| `.Word` | `len.Count` | DottedBare | Working |
| `.{...}` | `Lock.{LockId LockName}` | DottedBraced | Working |
| `.[...]` | `LockRejection.[DuplicateName PathOverlap]` | DottedSquareBracketed | Working |
| `.(...)` | `Stream.(Query IntentEvent)` | DottedParenthesized | Working |
| `."..."` | `Name."text"` | DottedQuoted | Working |
| `<...>` | `Processable<[Clonable Sendable] Serializable>` | -- | Design only |

Six working body forms plus `<>` in head position (psyche: "`<>` is a real Protos delimiter of course"; scanner does not yet recognise it).

### Axis 2: arity and field shape within a body

Within `{...}`: the walker counts children. Arity 1, 2, 3, 4 are structurally distinct. Within each arity, a field's own shape (bare word vs `[vector]` vs `{struct}`) adds further discrimination. Example: body arity 2 with `{[inputs] Yield}` (second field bare) is distinct from `{[inputs] [yields]}` (second field vector).

Within `<...>` in head position: the number of position groups (each a single kind or a `[multi-bound]` vector).

Arity discrimination is structurally available (the walker counts children) but the current `ShapeDefined::select` does not use it -- it dispatches by delimiter shape only.

### Axis 3: head delimiter character

The character between head and body. Today only `.` (dot). The psyche's thought experiment proposes `!` (bang) for mutable-self capabilities. Every keyboard candidate:

| Char | Spoken name | Ethos use today | Visual clarity | Hazards |
|---|---|---|---|---|
| `.` | dot | Head-body delimiter | High | -- |
| `!` | bang | -- | High | Shell `!!` history |
| `:` | colon | Import path separator (`signal_standard:lib.[...]`) | High | MD definition list |
| `?` | question | -- | High | Shell glob |
| `@` | at | -- | High | -- |
| `#` | hash | -- | High | Shell comment; MD heading |
| `~` | tilde | -- | Medium (small) | Shell `~` at word start |
| `^` | caret | -- | Low (small) | -- |
| `*` | star | -- | High | Shell glob; MD emphasis |
| `+` | plus | -- | High | -- |
| `-` | dash | -- | Medium (thin) | MD list; name hyphens |
| `=` | equals | -- | High | -- |
| `\|` | pipe | -- | High | Shell pipe; MD table |
| `&` | and | -- | High | Shell background |
| `%` | percent | -- | High | -- |
| `$` | dollar | -- | High | Shell variable |
| `'` | tick | -- | Low (confusable) | Shell string |
| `` ` `` | backtick | -- | Low (small) | Shell subst; MD code |
| `/` | slash | -- | High | Shell path |
| `\` | backslash | -- | Medium | Shell escape |

Colon-import verified: `:` appears as an import-path separator in signal-mirror (`[signal_standard:lib.[ObjectDigest StandardSocket]]`), meta-signal-criome, signal-mentci, meta-signal-lojix, and others. Not found in signal-orchestrate (it has no imports). `:` is therefore unavailable as a head delimiter.

**Best candidates** after `.` (current) and `!` (psyche-proposed): `?` `+` `@` `=` `~`. All are unseen in Ethos, sayable in speech, visually distinct, and free of critical hazards.

### Axis 4: nesting

A body can contain further structural forms (vectors within structs, structs within vectors). Nesting depth adds discrimination power. The psyche constrains: "too many heads in a row, very unrefined."

### How many distinct forms a single head can carry

| Configuration | Distinct forms |
|---|---|
| One delimiter (`.`), body shape only | 6 (bare + 5 body delimiters) |
| + `<>` in head | 7 |
| + arity 1-4 within `{}` | 10 (bare + 4 braced arities + word + vector + paren + string) |
| + field-shape discrimination within arity | ~14 (arity-2 splits by second-field shape, etc.) |
| Two delimiter chars (`.` `!`), with arity | ~19 (bare shared; each non-bare form x 2 + arities) |
| Four delimiter chars, with arity | ~33 |


## B. THE CAPABILITY ENUM

### Axis assignment

| Slot | Axis | Justification |
|---|---|---|
| Name | Head | Always; identity |
| Bearer mode | Head delimiter char | `.` reads, `!` changes, `~` consumes, `+` creates |
| Inputs 0..n | First field of `{...}` body (always a vector) | Positional; absent when body is bare word or `[...]` |
| Yield 0..n | Body shape: bare word = 1; `[...]` = n; second `{...}` field | Discriminated by body delimiter and field shape |
| Refusal 0..1 | Third `{...}` field (arity 3 discriminates) | Psyche's arity-discrimination insight |
| Async | `?` after bearer char | One char, one axis; absent = sync |
| Provided | `=` after bearer char | One char, one axis; absent = required |

Bearer mode is the psyche's ruling (`.` and `!`). Consumes (`~` "tilde") and creates (`+` "plus") are proposals -- unruled. Async (`?` "question") and provided (`=` "equals") are proposals -- unruled. The stacked-character pattern keeps the delimiter sequence short: `head[bearer][?async][=provided]body`. Most capabilities carry only the bearer char.

### The enum

```
Capability.[                                    ;; Vector-represented Enum

  ;; -- READS  .  bearer observed, not changed --

  Void.{Name}
  ;; name                                       ;; notify

  SingleYield.{Name Concept}
  ;; name.Concept                               ;; len.Count

  MultipleYields.{Name Vector<Concept>}
  ;; name.[C1 C2 ...]                           ;; describe.[Name Type Size]

  Standard.{Name Vector<Concept> Concept}
  ;; name.{[inputs] Yield}                      ;; lookup.{[Key] Value}

  MultipleStandard.{Name Vector<Concept> Vector<Concept>}
  ;; name.{[inputs] [yields]}                   ;; transform.{[Source Config] [Target Report]}

  Fallible.{Name Vector<Concept> Concept Concept}
  ;; name.{[inputs] Yield Refusal}              ;; validate.{[Input] Valid Invalid}

  ;; -- CHANGES  !  bearer mutated --

  MutableSingleYield.{Name Concept}
  ;; name!Concept                               ;; pop!Item

  MutableInputsOnly.{Name Vector<Concept>}
  ;; name!{[inputs]}                            ;; push!{[Item]}

  MutableStandard.{Name Vector<Concept> Concept}
  ;; name!{[inputs] Yield}                      ;; insert!{[Key Value] Inserted}

  MutableFallible.{Name Vector<Concept> Concept Concept}
  ;; name!{[inputs] Yield Refusal}              ;; register!{[PathLock] Registered Refused}

  MutableMultipleYields.{Name Vector<Concept>}
  ;; name![C1 C2 ...]

  ;; -- CONSUMES  ~  bearer destroyed (proposal: unruled) --

  ConsumingSingleYield.{Name Concept}
  ;; name~Concept                               ;; into_bytes~Bytes

  ConsumingStandard.{Name Vector<Concept> Concept}
  ;; name~{[inputs] Yield}

  ;; -- CREATES  +  no bearer, constructor (proposal: unruled) --

  CreatingStandard.{Name Vector<Concept> Concept}
  ;; name+{[inputs] Yield}                      ;; create+{[Config] Self}

  CreatingFallible.{Name Vector<Concept> Concept Concept}
  ;; name+{[inputs] Yield Refusal}              ;; try_from+{[Source] Self Error}

  ;; ...
  ;; Pattern continues: each bearer mode x signal shape is a variant.
  ;; Rare crossings (ConsumingFallible, CreatingMultipleYields, ...)
  ;; follow the same naming and representation rules.
]
```

Sixteen named variants covering all six reference capabilities. The `...` extends to ~22 meaningful crossings (some combinations like CreatingVoid are nonsensical).

The signal shapes are seven: Void (bare), SingleYield (word), MultipleYields (vector), InputsOnly (braced arity 1), Standard (braced arity 2, bare yield), MultipleStandard (braced arity 2, vector yields), Fallible (braced arity 3). The bearer modes are four (`.` `!` `~` `+`). The first body field in any `{...}` form is always a vector of input concepts, even when empty (`[]`), to prevent positional ambiguity.

### The six reference capabilities

```
;; 1. fn len(&self) -> Count;
len.Count                                       ;; 9 chars   (~3 tok)
;; Rust: 24 chars. Variant: SingleYield.

;; 2. fn push(&mut self, item: Item);
push!{[Item]}                                   ;; 13 chars  (~5 tok)
;; Rust: 31 chars. Variant: MutableInputsOnly.

;; 3. fn into_bytes(self) -> Bytes;
into_bytes~Bytes                                ;; 16 chars  (~4 tok)
;; Rust: 29 chars. Variant: ConsumingSingleYield.

;; 4. fn create(config: Config) -> Self where Self: Sized;
create+{[Config] Self}                          ;; 22 chars  (~6 tok)
;; Rust: 52 chars. Variant: CreatingStandard.

;; 5. fn register(&mut self, lock: PathLock) -> Result<Registered, Refused>;
register!{[PathLock] Registered Refused}        ;; 40 chars  (~8 tok)
;; Rust: 70 chars. Variant: MutableFallible.

;; 6. async fn fetch(&self, key: Key) -> Payload;
fetch.?{[Key] Payload}                          ;; 22 chars  (~6 tok)
;; Rust: 44 chars. Variant: Standard; ? marks async.
```


## C. THE KIND ENUM

### Axis assignment

| Slot | Axis |
|---|---|
| Kind name | Head |
| Positions (identity) | `<...>` in head: `Name<Positions>` |
| Superkinds | First `{...}` body field (vector) |
| Associated kinds | Second `{...}` body field (vector of `{KindName [bounds]}`) |
| Associated values | Third `{...}` body field (vector of `{ValueName Type}`) |
| Capabilities | `.[...]` body (simple) or last `{...}` body field (full) |

Positions are orthogonal to the body variant -- any variant's head may include `<Positions>` when the kind has identity positions. This avoids doubling every variant.

### The enum

```
Kind.[                                          ;; Vector-represented Enum

  Marker.{Name}
  ;; Name                                       ;; Sendable

  CapabilityOnly.{Name Capabilities}
  ;; Name.[capabilities]                        ;; Runnable.[run.Count]

  SuperkindsOnly.{Name Superkinds}
  ;; Name.{[superkinds]}                        ;; SafelyProcessable.{[Processable Sendable]}
  ;; DottedBraced, body arity 1.

  Constrained.{Name Superkinds Capabilities}
  ;; Name.{[superkinds] [capabilities]}
  ;; DottedBraced, body arity 2.

  Associated.{Name Superkinds AssociatedKinds Capabilities}
  ;; Name.{[superkinds] [assocKinds] [capabilities]}
  ;; DottedBraced, body arity 3.

  Full.{Name Superkinds AssociatedKinds AssociatedValues Capabilities}
  ;; Name.{[superkinds] [assocKinds] [assocValues] [capabilities]}
  ;; DottedBraced, body arity 4.
]
```

Six variants. Body arity (0 through 4) plus the `.[...]` form (CapabilityOnly) give six distinct structural forms. Positions in `<...>` layer on top of any variant.

### The three reference kinds

```
;; 1. Sendable -- marker
Sendable
;; Variant: Marker. 0 heads, 0 fields, 0 brackets.


;; 2. Runnable -- capability-only, one capability (run yields Count)
Runnable.[
  run.Count
]
;; Variant: CapabilityOnly. 2 heads (Runnable, run), 2 brackets.


;; 3. Processable -- full, with positions, all six capabilities
Processable<[Clonable Sendable] Serializable>.{
  [Displayable Debuggable Sendable Syncable Sealed]
  [{Output [Serializable DeserializeOwned]} {Ref []}]
  [{KIND String} {MAX_ITEMS Integer}]
  [
    len.Count
    push!{[Item]}
    into_bytes~Bytes
    create+{[Config] Self}
    register!{[PathLock] Registered Refused}
    fetch.?{[Key] Payload}
  ]
}
;; Variant: Full (with positions in head).
;; Head: Processable<[Clonable Sendable] Serializable>
;; Body arity: 4 (superkinds, assocKinds, assocValues, capabilities).
;; 9 heads, ~32 fields, ~20 brackets.
```


## D. WHAT "CONCEPT" IS

The psyche defined: "A Concept being a type or a Kind."

This fills a vocabulary gap. Until now, a capability's yield was called "yield kind" and its input types were "input kinds" -- but they may be concrete types (Count, Bytes, String), not kinds (Sendable, Processable). The term "Concept" subsumes both:

- **Type**: a concrete data shape (Count, Bytes, Lock)
- **Kind**: what a Rust trait becomes (Sendable, Serializable)
- **Concept**: either a type or a kind

Every position in a capability's struct that holds a type-or-kind reference is typed as Concept: `SingleYield.{Name Concept}`, `Standard.{Name Vector<Concept> Concept}`. The term appears nowhere in existing rulings and collides with none. It enters the vocabulary alongside Type and Kind, one level above both.


## E. RECOMMENDATION AND OPEN QUESTIONS

### Recommendation

The head delimiter character carries bearer mode at one token; body arity carries refusal at zero tokens; `<>` becomes a real delimiter for kind identity. These three extensions -- already present in the psyche's page -- give the structural forms enough discrimination to represent every surviving capability and kind slot without exceeding two heads in a row.

### Open questions for the psyche (at most eight)

1. Does `~` (tilde, "consumes") carry the consuming-self bearer mode, or should a different character?
2. Does `+` (plus, "creates") carry the no-self constructor mode, or should a different character?
3. Does `?` after the bearer character mark async, or does async live outside the capability entry (in a section, in the interaction)?
4. Does `=` after the bearer character mark provided (default implementation), or does that live only in the interaction?
5. Are associated values (const generics: `{KIND String}`) expressed in the kind declaration, or are they Rust-only and eliminated?
6. When a `{...}` body has arity 2, is the field-shape distinction (bare yield vs `[vector]` yield) a reliable discriminant, or must `Standard` and `MultipleStandard` use different arities?
7. Is `Self` a valid Concept in a yield position (used by CreatingStandard), or does the psyche want a different spelling for "yields the bearer kind"?
8. Does the Capability kind get declared in Ethos (the enum above), or is it only realised in walker code as TypeElement is today?

### Realization items (parser must gain)

- Arity discrimination in `ShapeDefined::select` (count children within `{...}` and dispatch).
- `<>` recognised as a structural delimiter in the protos scanner.
- New head delimiter characters (at minimum `!`; potentially `~` `+` `?` `=`) in the scanner's prefix handling.


## F. Sources

### Psyche vision (read in full)

- flows/b675f3d9/vision/structuralParsing.md -- the psyche's newest words and handwritten page
- flows/b675f3d9/vision/ethosAdvancedStructuralParsing.jpg -- the handwritten page (authoritative)
- flows/b675f3d9/vision/kinds.md -- all rulings through 2026-08-27

### Flow reports (read in full)

- flows/b675f3d9/reports/kindAndCapabilityTypes.md -- especially section A (parser witness, arity, `<>`, absence spellings) and slot inventories
- flows/b675f3d9/reports/capabilityAnatomy.md sections 1-3 -- the 30 signature constituents, minimal slots
- flows/b675f3d9/reports/rustTraitAnatomy.md sections 1-2 -- kind slots
- flows/b675f3d9/reports/ethosAnatomyVision.md -- corpus, non-repetition law, sections confer, spoken vocabulary, colon imports

### Distilled vision

- Vision/datom.md
- Vision/ethos.md

### Living fixtures (syntax witness)

- /git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos
- /git/github.com/LiGoldragon/signal-mirror/ethos/interface.ethos (colon imports: `signal_standard:lib.[...]`)
- /git/github.com/LiGoldragon/meta-signal-criome/ethos/interface.ethos (colon imports)
- /git/github.com/LiGoldragon/signal-mentci/ethos/interface.ethos (colon imports)

### Implementation

- /git/github.com/LiGoldragon/protos/src/block.rs lines 147-168 (scanner: `.` prefix, delimiter recognition `()` `""` `[]` `{}` only)
- /git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs lines 123-127 (TypeElement enum), 430-451 (ShapeDefined select by delimiter)

## Correction (b675f3d9, 2026-08-27)

Section A's conclusion that `:` "is therefore unavailable as a head
delimiter" is wrong and withdrawn. The psyche's ruling
(vision/structuralParsing.md, last entry): Ethos parsing is always
dependent on the current context; a character's meaning in the import
block does not constrain its meaning in a capabilities block. The
column "Ethos use today" stands as a fact; no candidate is excluded by
it. The head-delimiter candidate set is therefore the whole table,
`:` included.
