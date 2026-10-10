<!-- to-the-living:start -->
Presentation.{ «Type, new type, alias» }

## What each one is

```
 TYPE
 a shape of data the compiler knows
 by its name
   Lock { lock_id, lock_name }
 ──────────────────────────────────────
 NEW TYPE
 a type of its own that holds exactly
 one value of another type
   struct FlowId(String)
   FlowId, LockName and String are
   three types; none passes for another
 ──────────────────────────────────────
 ALIAS
 no type at all: a second name for a
 type that already exists
   type FlowId = String
   FlowId, LockName and String are
   one type under three names
```

A type is what the compiler checks: a struct with
its positions, an enum with its variants. A new
type is the smallest type: one name holding one
value, such as a flow id holding a string or an
age holding an integer. An alias adds nothing the
compiler can see; it is a label written over an
existing type, and every check runs against the
type underneath.

```
 ethos            FlowId.String
                       │
 Ethos Zero            ▼
 today            type FlowId = String
                  an alias
                       │
 the records           ▼
 ask for          struct FlowId(String)
                  a new type
```

Ethos Zero, in production on its main branch,
reads `Name.Type` as an alias and emits a Rust
alias. It has no new type at all: its three forms
are struct, enum and alias. It also accepts a
struct with one position, `FlowId.{ String }`,
and emits a one-field struct. The vision-ethos
skill describes the same shape: it calls
`FilePath.String` an alias and shows
`pub type LockId = Integer;`.

That is out of line with the records:
flows/d4ae97/vision/ethos.md, 2026-10-06 (new
types, not aliases; a one-position type is called
a new type; no double wrapping);
flows/ebbe30/vision/ethos.md, 2026-10-09 (new
types, not aliases; single-field structs
forbidden; the flow id stays a string for now,
with a comment); flows/8e9e77/vision/
single-field-structs.md, 2026-09-08 (the syntax:
name, period, contained type; a new type over a
complex type is absurd). The 2026-10-09 record
settles what the 2026-09-08 one left as
"possibly": single-field structs are forbidden.

Two further records point at new types as the
carrier of a special representation:
flows/445410/vision/ethos.md, 2026-10-09 (a type
keeps its real Rust type, and a trait gives it a
custom datom form) and flows/edf227/vision/
identifiers.md, 2026-10-03 (the flow id is a hash,
read and written as text by its own conversion).
A trait can be implemented only on a type that
exists, so both need the flow id to be a new type.

## Why new types

Each reason below shows the ethos, the Rust it
yields as an alias (wrong) and as a new type
(right). `FlowId` names one flow; `LockName`
names one lock; both hold a String. Facts marked
measured were compiled or run by this flow;
facts marked read were read in code. All seven
Rust claims in this book were confirmed on
Prometheus (flows/1d0733/reports/types-book-tests.md,
2026-10-09).

### 1. No accidental mixing (measured)

```
[ FlowId.String
  LockName.String ]
```

Wrong: a lock name passes as a flow id and the
program compiles.

```rust
type FlowId = String;
type LockName = String;
fn release(_flow: FlowId) {}
let name: LockName = "x".into();
release(name); // compiles
```

Right: the compiler refuses the mix.

```rust
struct FlowId(String);
struct LockName(String);
fn release(_flow: FlowId) {}
let name = LockName("x".into());
release(name); // error[E0308]
```

### 2. Kinds can be borne (measured)

An association such as `FlowId.[ Hashable ]`, a
custom datom form, or a standard kind like
Display needs a type of its own to attach to.

Wrong: an alias of String is String, and a
foreign kind cannot be given to a foreign type.

```rust
type FlowId = String;
impl std::fmt::Display for FlowId {}
// error[E0117]
```

Right:

```rust
struct FlowId(String);
impl std::fmt::Display for FlowId {}
```

### 3. Invariants held at construction (read)

Ethos Zero's own `Name` is a hand-written new
type: the one way in checks that the text is a
valid identifier, so every `Name` is valid and no
later code checks again.

Wrong:

```rust
type Name = String;
let name: Name = "r#bad name".into();
// any string is a Name
```

Right:

```rust
struct Name(String);
let name = Name::try_from("Lock")?;
// only a valid identifier is a Name
```

This is where an invariant the code enforces
lives; for the flow id, it is where the hash's
validity will live.

### 4. Zero cost (measured)

```rust
struct FlowId(String);
size_of::<FlowId>() // 24
size_of::<String>() // 24
```

A one-value struct has its value's layout; the
wrapping costs nothing at run time.

### 5. One derive for every declared type (read)

An alias carries no derive: today `FlowId` bears
rkyv, Hash and the datom kinds only because
String does. A new type carries the generated
derive like every struct and enum, so every
declared type bears both datom kinds with no
exception for aliases.

### Wrong shapes the records refuse

A struct of one position:

```
FlowId.{ String }   ; wrong: a one-field struct
FlowId.String       ; right: a new type
```

A new type over a new type:

```
Job.FlowId          ; wrong: Job adds no meaning
FlowId              ; right: the position itself
```

A new type over a complex type:

```
Pair.Lock           ; wrong: wraps a struct
Lock                ; right: the type itself
```

## Why one might not

Each cost below is shown in its concrete form; the
forks at the end rule on them.

### 1. Datom braces (measured)

Through today's derive, a new type reads as a
struct of one position:

```
abc123       ; FlowId as an alias
{ abc123 }   ; FlowId as a new type, today
```

Two braces in every flow id a machine writes,
against the cost of datom a machine outputs
(flows/d4ae97/vision/ethos.md, 2026-10-08).
Fork 3.

### 2. Access boilerplate (inference)

A new type does not open into its value; an
alias is its value. Reading the string inside
takes code, emitted or hand-written, for each
new type:

```rust
impl AsRef<str> for FlowId {
    fn as_ref(&self) -> &str { &self.0 }
}
impl From<FlowId> for String {
    fn from(id: FlowId) -> String { id.0 }
}
```

Fork 4.

### 3. Double wrapping (read)

Once every name is a new type, a name over a
name becomes easy to write, and each layer adds
a type and its conversions with no new meaning:

```
FlowId.String
Job.FlowId      ; Job(FlowId(String))
```

An alias of a declared type is the same double
name without the cost: Ethos Zero today emits
`DuplicateName.Lock` as `type DuplicateName =
Lock`. Fork 2.

### 4. Aliases of containers (measured)

A name over a vector is an alias today and keeps
every vector method. As a new type it keeps none
until they are emitted or written:

```rust
type Paths = Vec<LockPath>;
paths.push(path);      // works

struct Paths(Vec<LockPath>);
paths.push(path);      // error[E0599]
paths.0.push(path);    // E0616 outside;
                       // compiles inside
```

Confirmed on Prometheus (flows/1d0733/reports/
types-book-tests.md, 2026-10-09). Fork 1.

## Proposals

All five land in
psyche-skills/skills/vision-ethos.md. Proposal 1 asks its ruling now; the
others follow in order, each awaiting its turn.

### Proposal 1. The new type, replacing the alias

A new section after "Imports" (which ends at line
157), before "What a declaration turns into"
(line 159), and the comment on line 225.

The file as it stands around the new section:

> The generated code carries no `use` statements;
> each imported name is written fully qualified:
> `protos:String` appears as `protos::String`,
> `datom:Datom` as `datom::Datom`.
>
> ## What a declaration turns into
>
> A declaration turns into the Rust type with
> named fields, ...

Added, as prose:

> **## New types**
>
> A type written as its name, a period and one
> contained type, `FlowId.String` or
> `Age.Integer`, is a new type: a type of its own
> holding one value of the contained type. It is
> never an alias; Rust receives a distinct type,
> not a second name for the contained one.

Added, the section's example:

```diff
+ Library
+ []                ; imports
+ [ FlowId.String   ; types: a new type over String
+   Age.Integer ]   ;   a new type over Integer
+ []                ; kinds
+ []                ; associations
```

Line 225, in "A variant named as a defined type
carries that type":

```diff
- [ FilePath.String                          ; types: FilePath is an alias of String
+ [ FilePath.String ; types: a new type over
+                   ;   String
```

The block as it stands around line 225:

```
Library
[]                        ; imports
[ FilePath.String         ; (line 225)
  SyntaxError.Vector<FilePath>
  GenerationFailure.[ SyntaxError
                      Unwritable ] ]
[]                        ; kinds
[]                        ; associations
```

Sources, appended at the end of the file's
Sources list:

> ebbe30 ethos
>
> 8e9e77 single-field-structs

Distils flows/d4ae97/vision/ethos.md, 2026-10-06;
flows/ebbe30/vision/ethos.md, 2026-10-09;
flows/8e9e77/vision/single-field-structs.md,
2026-09-08.

**Ruling 1.** (a) Land as shown. (b) Amend, by
line.

### Proposal 2. What is refused (awaiting its turn)

Added at the end of the "New types" section of
Proposal 1, as prose:

> A struct of one position is refused: what holds
> one value is a new type, `FlowId.String`, never
> `FlowId.{ String }`; in Rust too, one value is
> held by a new type, never a one-field struct.
>
> A new type never wraps a new type: where `Job`
> would hold a `FlowId`, the position is a
> `FlowId`.
>
> A new type holds a plain value, a String, an
> Integer, a Decimal, a Boolean; a new type over
> a struct or an enum is refused.

Sources, appended:

> e4a40e archive-newtypeWrappingAndSingleFieldStructs

Distils flows/ebbe30/vision/ethos.md, 2026-10-09;
flows/d4ae97/vision/ethos.md, 2026-10-06;
flows/8e9e77/vision/single-field-structs.md,
2026-09-08; flows/e4a40e/vision/
archive-newtypeWrappingAndSingleFieldStructs.md,
2026-09-03.

### Proposal 3. What Ethos Zero generates for a new type (awaiting its turn)

Added at the end of the "New types" section, as
prose:

> Ethos Zero emits a new type as a Rust struct of
> one unnamed position, bearing the same derive as
> every struct and enum it emits.

Added, the Rust under the section's example:

```diff
+ #[derive(Datomizable, Compositional)]
+ pub struct FlowId(String);
+ #[derive(Datomizable, Compositional)]
+ pub struct Age(Integer);
```

In full, as the generator writes every struct
today, with the datom kinds behind the datom
feature:

```rust
#[derive(rkyv::Archive, rkyv::Serialize,
  rkyv::Deserialize, Clone, Debug,
  PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom",
  derive(datom_codec::Datomizable,
         datom_codec::Composing))]
pub struct FlowId(String);
```

Lines 435 and 436, the tuple rule, which a Rust
new type touches since Rust writes it as a
one-position tuple struct:

Removed:

> No tuple in the code we design; if some parts
> require it (standard traits, dependencies), then
> it is allowed at that contact point only.

Added:

> No tuple in the code we design, save the new
> type, which Rust writes as a one-position tuple
> struct; if other parts require a tuple (standard
> traits, dependencies), it is allowed at that
> contact point only.

When Ethos Zero emits this, the knowledge-ethos
skill (mind-skills/skills/knowledge-ethos.md,
which today says `Name.Type` is an alias and an
alias carries no derive) is brought in line with
it; knowledge lands without review.

### Proposal 4. The other alias sites (awaiting its turn)

Every example in vision-ethos that shows a
`Name.String` or `Name.Integer` as a Rust alias
changes to the new type of Proposal 3. Lines 226,
234, 269 to 271 and 275 are aliases of a vector;
they wait on fork 1 and are not touched here.

Lines 178 and 179, "What a declaration turns
into":

```diff
- pub type LockId = Integer;
- pub type LockName = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
+ #[derive(Datomizable, Compositional)]
+ pub struct LockName(String);
```

Lines 233 and 258:

```diff
- pub type FilePath = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Line 274, "Every declared type bears both kinds":

```diff
- pub type FilePath = String;                  // an alias: String already bears both
+ // a new type: derived like every type
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Line 303, "Shapes and placement":

Removed:

> Signal's first two sections, an alias in the types section. Where

Added:

> Signal's first two sections, a new type in the types section. Where

Lines 322 to 324:

```diff
- pub type LockId = Integer;
- pub type LockName = String;
- pub type FlowId = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
+ #[derive(Datomizable, Compositional)]
+ pub struct LockName(String);
+ #[derive(Datomizable, Compositional)]
+ pub struct FlowId(String);
```

### Proposal 5. The flow id stays a string, marked (awaiting its turn)

Line 315, in the Signal example of "Shapes and
placement":

```diff
-   FlowId.String
+   FlowId.String   ; a string for now, unideal:
+                   ;   the flow id is to be a hash
```

The block as it stands:

```
Signal
[]                        ; imports
[ Lock.LockRequest
  Release.LockId ]        ; queries
[ Locked.Lock
  Released.Lock ]         ; responses
[ LockId.Integer          ; types
  LockName.String
  FlowId.String           ; (line 315)
  LockRequest.{ LockName FlowId }
  Lock.{ LockId LockName } ]
```

The same comment goes on the flow id in «The
golden ethos», which today writes it
`FlowId.{ String }`.

Distils flows/ebbe30/vision/ethos.md, 2026-10-09;
flows/edf227/vision/identifiers.md, 2026-10-03.

## Open forks

Each is answered by its number and letter.

**Fork 1. A name over a container.**
`SyntaxError.Vector<FilePath>`,
`LockPaths.Vector<LockPath>`.
(a) a new type over the vector,
`struct SyntaxError(Vec<FilePath>)`.
(b) it stays an alias.
(c) refused; the vector is written inline where
it is used.
The same answer covers `Name.Option<T>`.

**Fork 2. A name over a declared type.**
`DuplicateName.Lock` in a types section, which
Ethos Zero emits today as
`type DuplicateName = Lock`.
(a) Ethos Zero refuses it as an error.
(b) it stays an alias for this case only.

**Fork 3. How a new type reads in datom.**

```
12232711     ; (a) as its value
{ 12232711 } ; (b) as a one-position struct
```

(a) is what the alias writes and what ebbe30's
audit assumed; today's derive writes (b). (a)
needs the derive or the generator to give a new
type its value's form.

**Fork 4. How the value inside is reached.**
`FlowId(String)`, with the string private.
(a) Ethos Zero emits `AsRef<str>` and `From`
both ways, as in "Access boilerplate" above.
(b) the way in is a hand-written `TryFrom` check,
as Ethos Zero's own `Name` has.
(c) the value is public, `FlowId(pub String)`,
as datom-codec's `Meaning(pub Opaque)` is.

**Fork 5. Every semantic string a new type.**
ebbe30's audit proposes, for the Curriculum book,
"Every semantic string has a new type":
`Text.String`, not `Text.{ String }` and not a
bare String position.
(a) vision-ethos carries this line too.
(b) it stays in the Curriculum book alone.
<!-- to-the-living:end -->
