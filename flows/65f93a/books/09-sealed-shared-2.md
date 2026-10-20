<!-- to-the-living:start -->
Presentation.{ «Sealed and shared types in Ethos, 2nd edition» }

# Sealed and shared types in Ethos, 2nd edition

### Proposal 1: A sealed type, a new section after Traits are explicit; bodies are hand-written · psyche-context › vision/ethos.md

+ A sealed type keeps its positions private to its own file: no code outside it reads or builds them.
+ It is built only by a capability with no self that yields the type or a refusal, borne by a trait the type is associated with in the same file.
+ A sealed type cannot be forged, so holding one is proof that its constructor ran.
+ A sealed type is never read from data: it is printed and archived, but no datom or archive builds it, and no type read from data holds it.
+ A sealed type is declared with `Sealed` between its name and its shape, and only a struct is sealed.

```ethos
Library.
{
[]                                ; imports
[ Address.String                  ; types
  Refusal.[ Mismatch Unknown ]
  VerifiedContext.Sealed.
     { Address Vector<String> } ]
[ Titled.[ title.[ String ] ]     ; traits
  Requested.[ address.[ Address ] ]
  Composed.[ modules.[ Vector<String> ] ]
  Verifying.
     [ verified:
          { [ Requested Composed ]
            [ Result<Self Refusal> ] }
       text.[ String ] ] ]
[ Address.[ Titled ]              ; associations
  Refusal.[ Titled ]
  VerifiedContext.[ Verifying ] ] }
```

Ruling: land, amend, or reject.

### Proposal 2: Shared state, a new section after the sealed type · psyche-context › vision/ethos.md

+ Shared mutable state is declared with `Shared` between a type's name and its shape: its positions live behind one lock, and every holder sees the same state.
+ A shared type never travels: it bears no datom traits, no query or response carries it, and no type that travels holds it.
+ It is reached only through the traits it is associated with in the same file: a `.` capability reads it under the lock, and a `!` capability changes it under the lock, on any holder of its handle.
- Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates, so every ethos-declared type always bears both traits and no declared type can exist without them.
+ Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates but a shared one, so every ethos-declared type that travels bears both traits and no such type can exist without them.
+ A shared type, like a sealed one, is built only by a capability with no self, borne by a trait it is associated with in the same file.

```ethos
Library.
{
[]                                ; imports
[ PaneId.String                   ; types
  WakeWaits.Shared.
     { Vector<PaneId> Integer } ]
[ Paned.[ pane.[ PaneId ] ]       ; traits
  Waiting.
     [ waits.[ Vector<PaneId> ]
       wait!{ [ Paned ] [ Integer ] }
       create:[ Self ] ] ]
[ PaneId.[ Paned ]                ; associations
  WakeWaits.[ Waiting ] ] }
```

Ruling: land, amend, or reject.
### Proposal 3: A capability that yields nothing, in Trait syntax · psyche-context › vision/ethos.md

- A capability with inputs is a headed brace: inputs in a bracket, yield in a bracket. A yield bracket holds one type.
+ A capability with inputs is a headed brace: inputs in a bracket, yield in a bracket. A yield bracket holds one type, or nothing when the capability only acts.

```ethos
Library.
{
[]                                ; imports
[ Counter.Shared.                 ; types: a count
     { Integer Boolean } ]        ;   and a pause
[ Counting.[ count.[ Integer ]    ; traits
             bump![]
             create:[ Self ] ] ]
[ Counter.[ Counting ] ] }        ; associations
```

Ruling: land, amend, or reject.

### Proposal 4: A type from Rust's standard library, held only in shared state, in Imports · psyche-context › vision/ethos.md

+ A type from Rust's standard library is imported through its path, a colon at each step: `std:time:[ Instant ]`.
+ Such a type is held only in a shared type's state, since it bears no datom traits and never travels.

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

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
