<!-- to-the-living:start -->
Presentation.{ «The inline import» }

## The colon today, and the form opened

A source is the name of a library a type comes
from; the head is the part of `a:B` before the
colon. The core built-ins are the types the core
library of the language declares. A registry is a
record of where each library lives; the loaded
environment is the set of libraries a run has
loaded, each found through that environment's
registry.

```
 TODAY: THE COLON IMPORT
 ┌──────────────────────────────────┐
 │ imports  core:Name               │
 │ types    Topic.Name              │
 └────────────────┬─────────────────┘
                  ▼
   the source core is read as a
   Rust path; Topic is a second
   name for core's Name

 TODAY: A COLON IN A TYPE POSITION
 ┌──────────────────────────────────┐
 │ types    Record.{ Topic:Name }   │
 └────────────────┬─────────────────┘
                  ▼
   the head Topic is read as a
   Rust path; no type Topic is
   declared

 THE FORM OPENED ON 2026-10-09
 ┌──────────────────────────────────┐
 │ types    Topic:Name              │
 └────────────────┬─────────────────┘
                  │ the head's case
          ┌───────┴────────┐
          ▼                ▼
   capital head     lowercase head
   from the core    from the registry
   built-ins        of the loaded
                    environment
```

The colon import is in production in Ethos Zero;
no registry exists.

Today, with an imports section:

```
Library
[ core:Name ]          ; imports: Name, from core
[ Topic.Name ]         ; types: Topic, over Name
[]                     ; traits
[]                     ; associations
```

The form opened, with none:

```
Library
[]                     ; imports: none
[ Topic:Name ]         ; types: Topic, from the
                       ;   core built-in Name
[]                     ; traits
[]                     ; associations
```

The registry key of 2026-10-09, as written:

```text
{ Subaspect.[Vision Knowledge ...] Topic:Name }
```

## Distillation

### 1. The inline import, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the ruled
path of the vision-ethos skill; the file is being
moved there, and the lines shown are its current
content. Place: the Imports section, after its
closing paragraph and before "## What a declaration
turns into".

Ethos Zero today parses `Topic:Name` in a type
position as a Rust path, with `Topic` taken as a
source. This line changes what the form means: the
case of the head decides where it resolves. What a
capital head declares, and what is emitted, stay
with Q1, Q2 and Q5.

Removed: none.

Above, unchanged:

```text
The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:String` appears as `protos::String`,
`datom:Datom` as `datom::Datom`.
```

Added, prose:

```text
A sourced reference, `head:Name`, may also stand where a type is
declared. The case of its head decides where it resolves: a capital
head from the core built-ins, the types the core library of the
language declares; a lowercase head from the registry of the loaded
environment, which records where each of its libraries lives. The
colon resolves, or is an error.
```

Added, the example that follows that prose:

```diff
+ Library
+ []                   ; imports: none
+ ; types: a capital head, from the core
+ ;   built-ins; a lowercase head, from the
+ ;   environment's registry
+ [ Record.{ Topic:Name
+            flow:Voice } ]
+ []                   ; traits
+ []                   ; associations
```

Added, the wrong form beside it:

```diff
+ Library
+ []                   ; imports: none
+ ; types: wrong, no registry entry named
+ ;   nowhere: an error, never a fallback
+ [ Record.{ nowhere:Voice } ]
+ []                   ; traits
+ []                   ; associations
```

Below, unchanged:

```text
## What a declaration turns into

A declaration turns into the Rust type with named fields, bearing the
datom traits through the derive, which Ethos Zero emits with the type.
```

The file's Sources list gains two lines at its
end, after `88475f ethos`:

```diff
  e51411 ethos
  88475f ethos
+ d5df1d ethos
+ 2b34fafa importResolution
```

Distils flows/d5df1d/vision/ethos.md, 2026-10-09,
and flows/2b34fafa/vision/importResolution.md,
2026-08-20.

**Ruling D1.** (a) Land as shown. (b) Amend, by
line.

## Questions

Each question carries a proposed answer. Answer
by number: accept, or amend.

### Q1. What a capital head means

1a. `Topic:Name` declares a type `Topic` over the
core built-in `Name`:

```
Library
[]                     ; imports: none
[ Topic:Name ]         ; types: declares Topic,
                       ;   over core's Name
[]                     ; traits
[]                     ; associations
```

1b. `Topic:Name` imports the core built-in `Name`
in place; nothing is declared, and the position
holds core's `Name` itself:

```
Library
[]                     ; imports: none
; types: Record holds core's Name; no Topic
[ Record.{ Topic:Name } ]
[]                     ; traits
[]                     ; associations
```

What the inline form adds, under either reading:
no imports section entry is needed, and the source
resolves through the core built-ins or a registry
rather than as a Rust path.

Proposed: 1a, since the form was opened as
another place where a type can be declared.

### Q2. A new type, or the imported one under a new name?

```
Library
[]                     ; imports: none
[ Topic:Name ]         ; types: is Topic its own
                       ;   type, or Name again?
[]                     ; traits
[]                     ; associations
```

The types book («Type, new type, alias»,
Proposal 1) proposes that `Name.Type` is a new
type: a type of its own holding one value of the
contained type, never an alias.

Proposed: `Topic:Name` is a new type over core's
`Name`, as `Topic.Name` would be. A `Topic` is
made by making a `Name`, so it keeps `Name`'s
runtime check, and never passes for another type
over `Name`.

### Q3. The entry of the file-location registry

The Nexus's file-location registry is his: it
stores, under the key above, the containing source
with its hash and the relative path of each file;
the payloads that change it live on the meta
signal; and Curriculum gets or checks the hash
when a query comes in, according to the operation,
write or read (flows/d5df1d/vision/ethos.md,
2026-10-09). The book proposes this entry for it:

```
Library
; imports: Name from core; Blake3, a hash type,
;   from a hash library (book's own)
[ core:Name
  hash:Blake3 ]
; types: one entry, its key and its location
[ Entry.{ Key.{ Subaspect.[ Vision
                            Knowledge ]
                Topic:Name }
          Location.{ Source.Name
                     Hash.Blake3
                     RelativePath.String } } ]
[]                     ; traits
[]                     ; associations
```

Proposed: the entry as drawn, the hash a blake3
digest held as its own type. Blake3 is already a
dependency of content-identity, sema-engine and
eleven other LiGoldragon crates, and of none of
ethos-zero, protos, datom-codec or Curriculum.

### Q4. The ethos import registry: one or two

Beyond the registry for files, he named a registry
for where all the libraries live, and one for the
loaded environment. What follows is the book's own
proposal.

```
Library
[]                     ; imports: none
; types: Topic from the core library's registry,
;   Voice from the environment's registry
[ Launch.{ Topic:Name
           flow:Voice } ]
[]                     ; traits
[]                     ; associations
```

Proposed (book's own): two registries. The core
library's registry ships with the core library and
is the same in every environment. The
environment's registry belongs to the loaded
environment. Each entry keys a source name to the
`Location` of Q3: the containing source, its hash,
and the relative path of the library file.

### Q5. What is emitted, and whether the imports section survives

```
Library
; imports: Voice, used in two places
[ flow:Voice ]
; types: Voice named bare in both
[ Launch.{ Voice
           Topic:Name }
  Retire.{ Voice
           Reason.String } ]
[]                     ; traits
[]                     ; associations
```

Today a source is emitted as written, and
`core:Name` emitted that way does not compile,
since `core` is already the name of Rust's own
core library.

Proposed: each registry entry also names what its
source compiles to, and the generator emits that,
never the source name itself. The imports section
survives for a source used in more than one place,
as above; a source used once is named inline,
matching the rule for types used once.

Held for the next book: Core built-ins against
intrinsics; What `core:Name` accepts; What a
lookup returns; What the isos environment is; The
meta signal payloads; Whether a declaration can
pull from a registry source.
<!-- to-the-living:end -->
