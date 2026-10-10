<!-- to-the-living:start -->
Presentation.{ «Two heads, one name» }

## Two heads, one name

The vision of ethos says, in its Identity section,
that a trait is identified as a Rust trait is, by
its name and its constraints, and that two heads
which differ in a constraint are two traits. Rust
holds no two traits of one name in one module. So
the library below asks for something the vision
promises and its target cannot hold:

```
Library
[ std:[ Clonable Sendable ] ]  ; imports
[]                             ; types
; traits: one name, two heads, the
;   constraints differ
[ Processable<Clonable>.[ … ]
  Processable<Sendable>.[ … ] ]
[]                             ; associations
```

Ethos Zero, as it runs today, refuses this library as
`Duplicate.Processable`. The ethos-test statement
map records the Identity row as differing, a
tension within the vision itself; the judgement is
in flows/d5df1d/reports/ethos-test-judgement.md.

The two readings of the same library:

```
+----------------------------------+
| Processable<Clonable>            |
| Processable<Sendable>            |
+----------------------------------+
        |                  |
        v                  v
+----------------+  +----------------+
| (1) two traits |  | (2) one name   |
| two distinct   |  | is one trait   |
| generated      |  |                |
| Rust names     |  |                |
+----------------+  +----------------+
        |                  |
        v                  v
+----------------+  +----------------+
| both accepted  |  | second head    |
|                |  | refused as     |
|                |  | Duplicate      |
+----------------+  +----------------+
```

## Distillation

### D1. Two heads of one name, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the Identity section,
lines 104–118. Choose one reading.

The section as it stands:

```text
## Identity

A trait is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>. A constraint is a trait, or a bracket of traits: what
Rust writes as a generic parameter with its bounds, ethos writes as
the bounds alone, since in ethos there are no generics, only traits; a
constraint in a trait declaration is a trait, never a type. Two heads
that differ in a constraint are two traits. Which constraints belong
to the identity is not a decision to make: the ethos compiles to
Rust, and what identifies the trait identifies the trait. What else a
trait declares, its supertraits, its associated types and constants,
its capabilities, is its definition. Angle brackets hold the
constraints; they are a protos delimiter, recycled from Rust as
Result and Self are.
```

#### Reading (1): two heads are two traits

Lines 111–112 stand. The Rust-identity sentence at
line 114 gains that the generated name carries the
constraint.

Removed, line 114:

```text
Rust, and what identifies the trait identifies the trait. What else a
```

Added:

```text
Rust, and what identifies the trait identifies the trait. The Rust
name generated for a trait carries its constraints, so two heads of
one name become two distinct Rust traits. What else a
```

#### Reading (2): one name is one trait

Lines 111–112 are amended: a second head of the
same name is refused as a duplicate.

Removed, lines 111–112:

```text
constraint in a trait declaration is a trait, never a type. Two heads
that differ in a constraint are two traits. Which constraints belong
```

Added:

```text
constraint in a trait declaration is a trait, never a type. One name
is one trait: a second head of the same name is refused as a
duplicate. Which constraints belong
```

**Ruling D1.** (1) Two traits, two generated names.
(2) One name, one trait. Or amend, by line.
<!-- to-the-living:end -->
