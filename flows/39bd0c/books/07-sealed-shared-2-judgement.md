Judgement on «Sealed and shared types in Ethos, 2nd edition», every example and trait.

Proposal 1: right and whole; the never-read-from-data line closes the forging path through data. Good.
Proposal 2: right; the amended standing line and the no-self builder are in. Good.
Proposal 3: the rule is right, and touch![] and wait!{ [ Paned ] [] } read cleanly. The example repeats Proposal 2's block with two lines changed, so he reads it twice; amend to the smaller block below, which shows nothing else than a capability that only acts.
Proposal 4: the import path is right and Clock bears Clocking. One fault: Lapping is declared and taken as an input, but no type in the file bears it, so the example shows a trait nobody has; amend as below, a Lap type that bears Lapping, as Address bears Titled in Proposal 1.

### Proposal 3, amended example · psyche-context › vision/ethos.md

```ethos
Library.
{
[]                                ; imports
[ Counter.Shared.{ Integer } ]    ; types
[ Counting.[ count.[ Integer ]    ; traits
             bump![]
             create:[ Self ] ] ]
[ Counter.[ Counting ] ] }        ; associations
```

### Proposal 4, amended example · psyche-context › vision/ethos.md

```ethos
Library.
{
[ std:time:[ Instant ] ]          ; imports
[ Lap.Integer                     ; types
  Clock.Shared.
     { Instant Vector<Lap> } ]
[ Lapping.[ lap.[ Lap ] ]         ; traits
  Clocking.
     [ started.[ Instant ]
       lap!{ [ Lapping ] [] }
       start:[ Self ] ] ]
[ Lap.[ Lapping ]                 ; associations
  Clock.[ Clocking ] ] }
```

No further proposal added. Parse both amended blocks on the branch before publishing; if one is rejected, keep the original and send me the line.
