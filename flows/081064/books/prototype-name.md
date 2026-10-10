# The prototype name

## How names are cased

Datom and ethos are both Protos languages. A name in
either is one of two kinds. A defined object (a
type or a trait) and a variant are PascalCase. Any
other name, which is not a type or a trait, is
camelCase and uncapitalized. That second kind gets
a type of its own, the prototype name. It behaves
like a string, but each one is checked as it is
created: it must be uncapitalized and made of
words. In a datom string position, a plain string
may still start with a capital, since that position
holds a string, not a name.

```
┌────────────────────────────────────┐
│ a defined object: a type, a trait  │
│ a variant                          │
│ PascalCase   Registered   Checked  │
└────────────────────────────────────┘
┌────────────────────────────────────┐
│ every other name                   │
│ not a type, not a trait            │
│ camelCase    protosParser   core   │
└─────────────────┬──────────────────┘
                  │ is held as
                  ▼
┌────────────────────────────────────┐
│ the prototype name                 │
│ like a string                      │
│ uncapitalized, made of words       │
│ checked whenever one is created    │
└────────────────────────────────────┘
┌────────────────────────────────────┐
│ a string position in datom         │
│ may start with a capital           │
│ ProtosParser  stays a string       │
└────────────────────────────────────┘
```

Flow already follows this rule for one name.
vision-flow says a topic is a core:Name, a
camelCaseExpression checked when it is created, and
writes titles as { Psyche core Secondary <id> }.
None of the ethos or Rust sources read has a
prototype-name type yet. So the rule is not in
production, and no development branch carries it.

### The code

Ethos used here. `Library` is the root of a file of
shared types. Its four sections are imports, types,
traits and associations. In the types section,
`Name.String` declares a name over the intrinsic
`String`. A bracket declares an enum, whose variants
are PascalCase. A brace declares a struct of
positions. A trait is a bearer of capabilities. A
capability written `create:` takes no self. Its
brace holds an input bracket and a yield bracket.
`Result<Self Refusal>` yields either the new value
or the reason it was refused. An association says a
type bears a trait.

Wrong: the name is only a string, so nothing is
checked and any text gets in.

```
; ethos
Library
; imports: none
[]
; types: a name that is only a string
[ PrototypeName.String
  Reply.[ Registered.{ PrototypeName String }
          Pending ] ]
; traits: none, so nothing is checked
[]
; associations: none
[]
```
```
; datom, in a position expecting Reply
; all three are accepted, though only the
; first is a prototype name
Registered.{ protosParser ProtosParser }
Registered.{ ProtosParser ProtosParser }
Registered.{ prtzx_9 ProtosParser }
```

Right: a prototype name can only come from a
creation that checks it. A capitalized candidate or
one that is not made of words is refused.

```
; ethos
Library
; imports: none
[]
; types: the name, held as a string; why a
; candidate is refused; a reply holding a name
[ PrototypeName.String
  Refusal.[ Capitalized
            NotWords ]
  Reply.[ Registered.{ PrototypeName String }
          Pending ] ]
; traits: a name is made from a string, or
; refused
[ Checked.[ create:{ [ String ]
                     [ Result<Self Refusal> ] } ] ]
; associations: the name bears the check
[ PrototypeName.[ Checked ] ]
```
```
; datom, in a position expecting Reply
; head Registered: a variant, PascalCase
; first position: a prototype name, camelCase
; second position: a String; its capital is fine
Registered.{ protosParser ProtosParser }
; refused: Capitalized
Registered.{ ProtosParser ProtosParser }
; refused: NotWords
Registered.{ prtzx_9 ProtosParser }
```

In the current generator the right form is refused.
A capability's input position takes a trait, not a
concrete type, and the refusal names TraitWanted at
`[ String ]`. The form is kept as written because it
is the form the rule wants. The Finding below gives
the two forms the generator does accept.

There is an open point in the right form. As
vision-ethos stands, `PrototypeName.String` in the
types section reads as an alias, and an alias is not
a new type. With an alias, the association would
really be on String. The right form needs
PrototypeName to be a type of its own. A raw record
asks for that: flows/d4ae97/vision/ethos.md,
2026-10-06, "Newtypes, not type aliases". It has not
been distilled yet.

### Terms

camelCaseExpression is not a flow's coinage. It
appears in the living's typed record of 2026-10-09
(flows/445410/vision/flow.md). The flow coined these
names: the type spelling `PrototypeName`, and the
example names `Refusal`, `Capitalized`, `NotWords`,
`Checked`, `Reply`, `Registered`, and the section
heading Names. "Prototype name" is his own term.
Two questions: is "prototype name" the name he
keeps, and is it the same type as core:Name?

## Finding: a capability cannot take a concrete type

A capability input is the bracket that opens a
capability's brace. It lists what the caller hands
in, and in ethos each entry there is a kind, a trait,
or Self. A concrete type such as `String` in that
position is a kind not yet named, and the current
generator refuses it. So ethos cannot today say
"create a prototype name from a String, by name".
This is reported as a finding, not worked around.

`PrototypeName.String` also generates an alias, not
a new type: Rust sees `String`.

Form (a) takes Self.

```
; ethos, traits section
[ Checked.[ create:{ [ Self ]
                     [ Result<Self Refusal> ] } ] ]
```
```rust
pub trait Checked: Sized {
    fn create(input: Self)
        -> Result<Self, Refusal>;
}
```

Form (a) gives up the name of the input. With
PrototypeName an alias, Self is String in fact, but
the signature says Self, so the alias hides what is
taken.

Form (b) declares a trait and takes it.

```
; ethos, traits section
[ StringKind.[ ]
  Checked.[ create:{ [ StringKind ]
                     [ Result<Self Refusal> ] } ] ]
```
```rust
pub trait StringKind {}
pub trait Checked: Sized {
    fn create<N: StringKind>(input: N)
        -> Result<Self, Refusal>;
}
```

Form (b) gives up String itself. The check runs on
any bearer of StringKind, not on String.

No accepted form takes a concrete String by name.

## Proposal: where the casing rule lands

This distils flows/081064/vision/ethos.md,
2026-10-10, "uncapitalized names in Protos
languages: the prototype name". It also draws on
flows/445410/vision/flow.md, 2026-10-09, "Topic
names are camelCase expressions", which agrees with
it.

The statement says datom and ethos, and calls them
Protos languages. So it can land in two shapes.

### Choice 1: one shared rule in vision-protos

The statement becomes a new section of
vision-protos.
vision-ethos and vision-datom each get one line that
points to it. In vision-protos, "What Protos knows"
already shows capitalization as part of textual
structure. The same section also says protos does
not know what anything is, and a prototype name is a
type.

Target: psyche-skills/skills/vision-protos.md,
between
the end of "## Structure" and "## String, escape,
error".

Above, as it stands:

real protos delimiter. The key-value map, which the guillemets once
delimited, is dropped entirely from protos and its dialects.

Added:

```diff
+## Names
+
+In the Protos languages, datom and ethos among
+them, a defined object, a type or a trait, and a
+variant are named in PascalCase; every other name
+is camelCase, uncapitalized, and is a prototype
+name: a type like a string, an uncapitalized
+identifier composed of words, checked whenever one
+is created. A string position in datom takes a
+string that starts with a capital; it stays a
+string.
+
+```
+; ethos
+Library
+; imports: none
+[]
+; types: the name, held as a string; why a
+; candidate is refused; a reply holding a name
+[ PrototypeName.String
+  Refusal.[ Capitalized
+            NotWords ]
+  Reply.[ Registered.{ PrototypeName String }
+          Pending ] ]
+; traits: a name is made from a string, or
+; refused
+[ Checked.[ create:{ [ String ]   ; <- question 3
+                     [ Result<Self Refusal> ] } ] ]
+; associations: the name bears the check
+[ PrototypeName.[ Checked ] ]
+```
+```
+; datom, in a position expecting Reply
+Registered.{ protosParser ProtosParser }
+```
+
```

Below, as it stands:

## String, escape, error

Target: psyche-skills/skills/vision-protos.md, at
the
end of "## Sources".

564f55 datom
564f55 signal

```diff
+081064 ethos
+445410 flow
```

Target: psyche-skills/vision/ethos.md, at the end of
"## Naming".

and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

```diff
+
+Name casing is stated in vision-protos, Names.
```

## Identity

Target: psyche-skills/skills/vision-datom.md, at the
end of "## Strings", after its example block.

cannot be mistyped for it, and point, so the ends are visible at any
size.

\`\`\`
Ada     TheBuildPassedOnTheThirdTry     «12 Rue de la Paix»
\`\`\`

```diff
+
+Name casing is stated in vision-protos, Names.
```

## Syntax

### Choice 2: the rule lands in each language

The statement lands in vision-ethos and in
vision-datom, each time with that language's code.
vision-protos does not change.

Target: psyche-skills/vision/ethos.md, at the end of
"## Naming".

and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

```diff
+
+A defined object, a type or a trait, and a variant
+are named in PascalCase; every other name is
+camelCase, uncapitalized, and is a prototype name:
+a type like a string, an uncapitalized identifier
+composed of words, checked whenever one is created.
+
+```
+Library
+; imports: none
+[]
+; types: the name, held as a string; why a
+; candidate is refused; a reply holding a name
+[ PrototypeName.String
+  Refusal.[ Capitalized
+            NotWords ]
+  Reply.[ Registered.{ PrototypeName String }
+          Pending ] ]
+; traits: a name is made from a string, or
+; refused
+[ Checked.[ create:{ [ String ]   ; <- question 3
+                     [ Result<Self Refusal> ] } ] ]
+; associations: the name bears the check
+[ PrototypeName.[ Checked ] ]
+```
```

## Identity

Target: psyche-skills/vision/ethos.md, at the end of
"## Sources".

e51411 ethos
88475f ethos
d5df1d ethos

```diff
+081064 ethos
+445410 flow
```

Target: psyche-skills/skills/vision-datom.md, at the
end of "## Strings", after its example block.

cannot be mistyped for it, and point, so the ends are visible at any
size.

\`\`\`
Ada     TheBuildPassedOnTheThirdTry     «12 Rue de la Paix»
\`\`\`

```diff
+
+A head is a variant, PascalCase; every other name
+is camelCase, uncapitalized, and is a prototype
+name: a type like a string, an uncapitalized
+identifier composed of words, checked whenever one
+is created. A string position takes a string that
+starts with a capital; it stays a string.
+
+```
+; Reply: an enum of
+;   Registered.{ PrototypeName String }, Pending
+Registered.{ protosParser ProtosParser }
+```
```

## Syntax

Target: psyche-skills/skills/vision-datom.md, at the
end of "## Sources".

542442 datom
f38926 meaningLanguage

```diff
+081064 ethos
+445410 flow
```

## Distillation

Proposed skill lines, per choice:

Choice 1.
- psyche-skills/skills/vision-protos.md: new section
  "## Names" (the statement, the ethos declaration,
  the datom line), placed before "## String, escape,
  error"; Sources gets `081064 ethos` and
  `445410 flow`.
- psyche-skills/vision/ethos.md: one line at the end
  of "## Naming": Name casing is stated in
  vision-protos, Names.
- psyche-skills/skills/vision-datom.md: the same
  line
  at the end of "## Strings".

Choice 2.
- psyche-skills/vision/ethos.md: the statement and
  the ethos declaration at the end of "## Naming";
  Sources gets `081064 ethos` and `445410 flow`.
- psyche-skills/skills/vision-datom.md: the
  statement and the datom example at the end of
  "## Strings"; Sources gets `081064 ethos` and
  `445410 flow`.

Sources:

081064 ethos
445410 flow

## Ruling

1. Choice 1: the shared rule in vision-protos, with
   one pointer line each in vision-ethos and
   vision-datom.
2. Choice 2: the rule in vision-ethos and in
   vision-datom separately.

3. May an ethos capability input name a concrete
   type? Then the right form stands as the vision.
   Or is the prototype name's check written over Self
   (form a), or over a trait (form b)? The line
   `[ String ]` marked `<- question 3` in the
   proposal blocks is the line this decides; the
   marker is the book's and does not land.

Also: is "prototype name" the name you keep, and is
the prototype name the type core:Name?
