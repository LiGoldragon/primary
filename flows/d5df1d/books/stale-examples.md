<!-- to-the-living:start -->
Presentation.{ «Two stale examples» }

## Two examples against their rules

The vision-ethos skill, as it stands in production,
carries two examples that its own rules refuse.

The first is in Trait syntax. A trait's capability
speaks in `Self`, the trait's own parameters and
other traits; a concrete type in an input is a trait
not yet named. The `Fillable` example takes a
`String` as its input. In the capability below,
`push!` takes a mutable receiver (`!`); the first
bracket holds its inputs, the second its yield, here
`Result<Integer SinkError>`, an Integer or a
`SinkError`. `Self` is the type that bears
`Fillable`.

```ethos
; wrong: a concrete type as an input
push!{ [ String ] [ Result<Integer SinkError> ] }
; right: the input is the bearer itself
push!{ [ Self ] [ Result<Integer SinkError> ] }
```

The second is in Imports. An explicit import and an
intrinsic name mean the same thing, and `String` is
intrinsic. The full-qualification example shows
`protos:String` written as `protos::String`, a name
protos does not provide. `Textualizable` is a trait
protos does provide, so `protos:Textualizable` as
`protos::Textualizable` shows full qualification
with no collision.

```text
 Trait rule: an input speaks in
 Self, parameters, traits
            |
            v
 example: push!{ [ String ] ... }
            |
            v
 Ethos Zero refuses: TraitWanted.String
            |
            v
 with Self in place of String: accepted

 Imports rule: explicit import and
 intrinsic name mean the same
            |
            v
 example: protos:String -> protos::String
            |
            v
 String is intrinsic; protos has none
            |
            v
 protos:Textualizable
   -> protos::Textualizable: no collision
```

Both rows are the ethos-test statement map's
"differs" rows; the judgement is in
flows/d5df1d/reports/ethos-test-judgement.md.

## Distillation

### D1. Two examples, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Two line pairs, one in Trait
syntax and one in Imports.

#### 1. Trait syntax, the Fillable example

Above, unchanged:

~~~text
```
Library
[]                                                            ; imports
[ SinkError.[ Closed Full ] ]                                 ; types
~~~

Removed:

```text
[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] } ; traits
```

Added:

```text
[ Fillable.[ push!{ [ Self ] [ Result<Integer SinkError> ] } ; traits
```

Below, unchanged:

~~~text
             drain![ Vector<String> ]
             create:[ Self ] ] ]
[]                                                            ; associations
```
~~~

#### 2. Imports, the full-qualification example

Above, unchanged:

~~~text
[]                                                 ; associations
```

The generated code carries no `use` statements; each imported name is
~~~

Removed:

```text
written fully qualified: `protos:String` appears as `protos::String`,
```

Added:

```text
written fully qualified: `protos:Textualizable` appears as `protos::Textualizable`,
```

Below, unchanged:

```text
`datom:Datom` as `datom::Datom`.

## What a declaration turns into
```

Rests on flows/d5df1d/reports/ethos-test-judgement.md.

**Ruling D1.** (a) Land both. (b) Land one, by
number. (c) Amend, by line.
<!-- to-the-living:end -->
