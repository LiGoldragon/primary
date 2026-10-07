<!-- to-the-living:start -->
Presentation.{ «Levels, tests, traits» }

## Proposal 1: new skill `intent-levels` (psyche-skills)
Nothing there now. Proposed whole:
```
A Primary designs and implements, with its own
subflows. Its Secondary keeps track of all the
Primary works on and is its secretary.

A message goes across aspects only at the
sender's own layer; within an aspect, one
layer up or any layer down. A Secondary
reaches another aspect's Primary only through
that aspect's Secondary.

A lower layer is parented by the layer above:
it acts on a mandate, and when unsure it asks
above and admits what it does not know. Its
model infers less well; the layer above holds
more context and decides.
```

## Proposal 2: `operation-testing`, how a test proves
Lines removed: none. Added:
```
A test never searches production code for a
string. It runs the whole system under normal
use, in a developer build with tracing, and
passes when the expected trace appears, in
order where order matters. A dummy load, a
build alone, or a fragment run proves nothing.
```

## Proposal 3: `vision-ethos`, variant order and traits
Lines removed: none. Added:
```
Variants are ordered by seniority, the first
most senior: spirit before intent before
vision; compensation before trial.

Every trait is written in ethos. Code not
generated from ethos declares no trait, and a
mechanical check enforces it.
```

## Proposal 4: `operation-skill-designing`, code in skills
Lines removed: none. Added:
```
Code in a skill is generated into the code
base, compiled and used in production: a type
is used, a condition runs at build time. A
block without a file name goes to its kind's
default place. The model may write the
implied boilerplate around it so it compiles.
An audit fails code that is not used.
```

## Rulings
1. Proposal 1: (a) land (b) amend.
2. Proposal 2: (a) land (b) amend.
3. Proposal 3: (a) land (b) amend.
4. Proposal 4: (a) land (b) amend.
<!-- to-the-living:end -->
