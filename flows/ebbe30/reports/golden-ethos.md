# Golden ethos

```
Library                         ; Flow Nexus types
[]                              ; imports: none
[                               ; types
  FlowId.{ String }             ; one flow, by id
  Layer.[                       ; decides the model
    Primary
    Secondary
    Tertiary
    Quaternary ]
  Details.{                     ; a metaflow's state
    Layer
    Topic.{ String }            ; Core when none
    State.[                     ; where it stands
      Awake.FlowId              ; its current flow
      Asleep                    ; a request wakes it
      Ended ]
    Past.{ Vector<FlowId> } }   ; oldest first
  Metaflow.[                    ; one per aspect
    Psyche.Details
    Mind.Details
    Field.Details ] ]
[                               ; kinds
  Layered.[ layer.[ Layer ] ]   ; sits at a layer
  Wakeable.{                    ; can be woken
    [ Layered ]                 ; superkinds
    []                          ; associated types
    []                          ; constants
    [ wake![ FlowId ] ] } ]     ; yields its flow
[                               ; associations
  Metaflow.[ Wakeable ] ]       ; a metaflow wakes
```

Witness: ethos-zero 16.0.0, local build at c2653dd, answered
`Checked.` and generated 7 types, 2 traits and 1 assertion from
this file; no line exceeds 52 characters (awk length check).

## What the file instantiates

- psyche-skills/skills/vision-ethos.md:25, :30 (four roots) → the `Library` root.
- psyche-skills/skills/vision-ethos.md:109-110 (sweet form) → `Library`, then four sibling sections.
- psyche-skills/skills/vision-ethos.md:117 (no version) → no version anywhere in the file.
- psyche-skills/skills/vision-ethos.md:120-122 (Library sections in order) → imports, types, kinds, associations.
- psyche-skills/skills/vision-ethos.md:145-146 (intrinsics need no import) → imports `[]`; String and Vector are intrinsic.
- flows/d4ae97/vision/ethos.md:82 (new types, not aliases) → `FlowId.{ String }`, `Topic.{ String }`, `Past.{ Vector<FlowId> }`.
- psyche-skills/skills/vision-ethos.md:436 (no tuple) → each new type is a one-field named struct, not a tuple struct.
- psyche-skills/skills/vision-ethos.md:162-166 (field named after its type) → generated fields `layer`, `topic`, `state`, `past`, `flow_id_vector`.
- psyche-skills/skills/vision-ethos.md:189-192, :216 (used once: inline; used more than once: declared once, named) → `Topic`, `State`, `Past` inline in `Details`; `FlowId`, `Layer`, `Details` named at top level.
- psyche-skills/skills/vision-ethos.md:220-221 (a variant named as a defined type carries it) → `Psyche.Details`, `Mind.Details`, `Field.Details`, `Awake.FlowId`.
- psyche-skills/skills/vision-ethos.md:305 (in types, a bracket is an enum) → `Layer`, `State`, `Metaflow`.
- psyche-skills/skills/vision-ethos.md:243-247 (payload variants) → `Metaflow` (each variant carries Details), `State` (`Awake` carries FlowId).
- psyche-skills/skills/vision-ethos.md:67 (qualifier-named kinds) → `Layered`, `Wakeable`.
- psyche-skills/skills/vision-ethos.md:354-358 (simple kind, receivers, one-type yield) → `Layered.[ layer.[ Layer ] ]`, receiver `.`.
- psyche-skills/skills/vision-ethos.md:379-382 (complex kind: superkinds, associated types, constants, capabilities) → `Wakeable`, superkind `Layered`, receiver `!`.
- psyche-skills/skills/vision-ethos.md:63 (no concrete type in an input) → neither capability takes an input.
- psyche-skills/skills/vision-ethos.md:330-332, :409-413 (explicit association, fourth section) → `Metaflow.[ Wakeable ]`.
- psyche-skills/skills/vision-ethos.md:34 (no repetition) → `Details` written once, carried three times.
- psyche-skills/skills/vision-ethos.md:441-443 (space inside non-empty brackets, empty tight) → `{ String }`, `[]`.
- psyche-skills/skills/vision-ethos.md:445 and flows/e5a0bc/vision/ethos.md:7 (vertical; elements begin on the next line, indented; closer ends the last line) → every multi-element structure.
- psyche-skills/skills/vision-ethos.md:447 (comment on every section and every line with a next layer) → the `;` column.
- flows/f5a6e9/books/12-the-metaflows-ethos.md (added lines) → `Metaflow` as one variant per aspect, `Details` with Layer, Topic, State, Past.

## Open questions

1. The syntax of a new type. I chose `FlowId.{ String }`, a one-field struct, which ethos-zero accepts today. The other option is `FlowId.String` read as a new type, which is how book 12 writes `Topic.Dense ; a new type`. vision-ethos does more than stay silent here: its lines 171-172, 179-180, 226, 275 and 304 still describe `Name.Type` as an alias, against the ruling at d4ae97:82.
2. How a one-position new type is written in datom. With the brace form, a datom becomes `{ Core }` and `Awake.{ startInputVital }`. Book 12 writes them bare: `Core` and `Awake.startInputVital`. Should a new type print as its inner form (transparent), or as a one-position struct?
3. Does a one-position vector (`Past`) count as a one-position type that must be a new type, or does it stay a plain `Vector<FlowId>` position?
4. Does an association list the superkinds (`Metaflow.[ Layered Wakeable ]`), or only the kind that implies them? I listed only `Wakeable`.
5. Does a one-element structure whose element has its own next layer stay on one line? Examples are `Layered.[ layer.[ Layer ] ]` and `[ wake![ FlowId ] ]`. Line 445 says "more than one element" and also "nothing that has a next layer sits on one line". I kept them on one line.
6. Indent width and comment column. I chose 2 spaces and column 33; book 12 uses 3. Should a section's opening `[` also stand alone, with its elements on the next line? I applied that to sections too.
7. Does a `Name.Type` variant line (`Psyche.Details`) count as having a next layer, so that it needs a comment? I left those lines and the bare variants uncommented.
8. Must a complex kind write its empty `[]` for associated types and constants, or can they be left out? I wrote them, since the positions are fixed.
9. Book 12's ruling 1 is still pending. The open points are Aspect as Metaflow's variants (there is no Aspect type), Topic over `String` rather than `Dense`, and `Queue.Vector<Request>`, which I left out because `Request` has no shape there.
10. What a capability means. `wake!` yielding the woken flow's FlowId is my choice. I found no stated syntax for a capability that yields nothing.
