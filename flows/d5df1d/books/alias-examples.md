<!-- to-the-living:start -->
Presentation.{ «The alias examples» }

## What the examples show

In ethos, `LockId.Integer` is a declaration: the
name `LockId`, a period, and the one type it is
declared over, `Integer`. Under the ruling on
declarations over a plain value
(flows/d4ae97/vision/ethos.md, 2026-10-06), this
declares a new type: `LockId` is a type of its
own holding one `Integer`, and Rust receives a
distinct type, not a second name for `Integer`.

The vision-ethos skill still shows the same
declaration as an alias, in eleven lines of its
examples and their prose. «Type, new type, alias»
proposes the rule in its Proposal 1; these eleven
lines are its examples, and they say the opposite
until they change with it.

The `LockName` and `FlowId` example lines (211, 238,
355 to 356) are already carried by «Type, new type,
alias», Proposal 4, and the vector alias lines (266,
307) wait on that book's Fork 1, so after both books
every plain-value example reads as a new type.

```
  ethos           LockId.Integer
                        │
                        ▼
  the vision      an alias
  shows today     pub type LockId = Integer;
                  "an alias is not a new type"
                        │
                        ▼
  the ruling      a new type
                  LockId: a type of its own,
                  holding one Integer
```

The new-type form is built in a development
branch of Ethos Zero, the Ethos solution's item 1;
its main branch emits the alias. The line-by-line
reading of the vision against that work is in
flows/d5df1d/reports/ethos-test-judgement.md.

## Distillation

### D1. The eleven alias lines follow the ruling

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill.

This is the companion of «Type, new type, alias»,
Proposal 1: landing that proposal lands these
eleven lines with it, so one ruling covers both.
The added lines are the forms that book already
shows for the same sites: the Rust new type of its
Proposal 4, and its wording for lines 257 and 335.
The three `FilePath` lines (265, 290, 306) take the
same Rust new type.

#### Line 210, "What a declaration turns into"

Above, unchanged:

```text
[ LockId.Integer                              ; types
  LockName.String
  Lock.{ LockId LockName Vector<String> Option<Lock> }
  Generation.{ String String } ]
[]                                            ; traits
[]                                            ; associations
```

Removed and added:

```diff
- pub type LockId = Integer;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
```

Below, unchanged:

```text
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName, pub string_vector: Vec<String>, pub lock_option: Option<Lock> }
```

#### Line 237, "Inline types"

Above, unchanged:

```text
[ LockId.Integer                                         ; types
  LockName.String
  Lock.{ LockId LockName }
```

Removed and added:

```diff
- pub type LockId = Integer;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
```

Below, unchanged:

```text
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName }
```

#### Line 257, "A variant named as a defined type carries that type"

Above, unchanged:

```
Library
[]                                         ; imports
```

Removed:

```text
[ FilePath.String                          ; types: FilePath is an alias of String
```

Added:

```diff
+ [ FilePath.String ; types: a new type over
+                   ;   String
```

Below, unchanged:

```text
  SyntaxError.Vector<FilePath>             ;        SyntaxError is a vector of FilePath
  GenerationFailure.[ SyntaxError          ;        an enum: the variant SyntaxError is bare here,
                      Unwritable ] ]       ;        but SyntaxError is a defined type, so it carries one
```

#### Line 265, "A variant named as a defined type carries that type"

Above, unchanged:

````text
[]                                         ; associations
```
```rust
````

Removed and added:

```diff
- pub type FilePath = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Below, unchanged:

```text
pub type SyntaxError = Vec<FilePath>;
#[derive(Datomizable, Compositional)]
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```

#### Line 290, "A variant named as a defined type carries that type"

Above, unchanged:

````text
[]                                                        ; associations
```
```rust
````

Removed and added:

```diff
- pub type FilePath = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Below, unchanged:

```text
#[derive(Datomizable, Compositional)]
pub struct Unwritable_Data { pub file_path: FilePath, pub string: String }
#[derive(Datomizable, Compositional)]
```

#### Lines 301 to 303, "Every declared type bears both traits"

Above, unchanged:

```text
Ethos Zero emits `Datomizable` and `Compositional` on every struct and
enum it generates, so every ethos-declared type always bears both
```

Removed, prose:

```text
traits and no declared type can exist without them. An alias bears them
through the type it names: an alias is not a new type and cannot carry
a derive.
```

Added, prose:

```text
traits and no declared type can exist without them. A new type, such
as `FilePath.String`, is a type of its own and bears them through its
own derive.
```

Below, unchanged:

````text

```rust
````

#### Line 306, "Every declared type bears both traits"

Above, unchanged:

````text

```rust
````

Removed:

```text
pub type FilePath = String;                  // an alias: String already bears both
```

Added:

```diff
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Below, unchanged:

```text
pub type SyntaxError = Vec<FilePath>;        // an alias: Vec<T> bears both for any T that does
#[derive(Datomizable, Compositional)]        // a type: always derived
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```

#### Line 335, "Shapes and placement"

Above, unchanged:

```text
Each section has its own parsing context; placement carries the
meaning. Head then symbol is a variant of `Query` or `Response` in a
```

Removed, prose:

```text
Signal's first two sections, an alias in the types section. Where
```

Added, prose:

```text
Signal's first two sections, a new type in the types section. Where
```

Below, unchanged:

```text
types are defined a bracket is an enum, never a vector. Ethos may
generate default implementations for Query and Response, which is why
```

#### Line 354, "Shapes and placement"

Above, unchanged:

```text
[ LockId.Integer                                       ; types
  LockName.String
  FlowId.String
```
```text
pub enum Query    { Lock(LockRequest), Release(LockId) }
pub enum Response { Locked(Lock), Released(Lock) }
```

Removed and added:

```diff
- pub type LockId = Integer;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
```

Below, unchanged:

```text
pub type LockName = String;
pub type FlowId = String;
```

Distils flows/d4ae97/vision/ethos.md, 2026-10-06.

**Ruling D1.** (a) These eleven lines land with
«Type, new type, alias», Proposal 1. (b) Amend, by
line.
<!-- to-the-living:end -->
