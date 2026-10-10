<!-- to-the-living:start -->
Presentation.{ «Metaflow kinds, the title, the word id» }

## 1. `flow/crates/flow-nexus/ethos/memory.ethos`, the `Name` block of «The metaflow record», second edition

Lines removed:

```
      Name.[
         Voice.{                 ; permanent
            FlowAspect
            Layer.[
               Primary
               Secondary
               Tertiary
               Quaternary ] }
         Goal.String ]           ; camelCase; ends
```

Lines added:

```
      Kind.[
         Voice.{                 ; Psyche, Mind, Field:
            FlowAspect           ; one payload, the
            Layer }              ; aspect a field of it
         Implementation.{        ; a job: its own kind
            Name.String          ; camelCase
            Layer } ]            ; Primary, Secondary…
```

Written, three metaflows:

```
{  Voice.{ Psyche Primary }
   Awake.startInputVital
   [ zooWrongYouth ] }

{  Voice.{ Psyche Primary }     ; a second thread
   Asleep                       ; of the same voice
   [ ] }

{  Implementation.{ flowRefresh Secondary }
   Awake.aboutBlanketBoat
   [ ] }
```

Ruling 1: (a) one name, Voice, for the three similar kinds, the aspect a field of its payload. (b) three kinds, Psyche, Mind, Field, each carrying Layer. (c) amend.

## 2. `signal-flow/ethos/signal.ethos`, after line 151

Line 151 today:

```
PowerLevel.[ High Medium Low UltraLow ]
```

Lines removed: none. Line added after it:

```
Layer.[ Primary Secondary Tertiary Quaternary ]
```

Ruling 2: yes, or amend.

## 3. `mind-skills/skills/operation-main-flow.md`, line 29

Line removed:

```
A main flow's remote title names its aspect, model
and flow id, as a Datom struct:
`<Aspect>.{ <Model> <FLOW_ID> }`, for example
`Mind.{ Astra 6f51ad }`.
```

Lines added:

```
A main flow's remote title is its metaflow's kind
written short, then its flow id in words, never
the model: `Psyche.{ Primary startInputVital }`,
`Implementation.{ flowRefresh Secondary
aboutBlanketBoat }`.
```

Ruling 3: yes, or amend.

## 4. `psyche-skills/skills/vision-flow.md`, line 22, third sentence

Line removed:

```
Voices are addressed by name; a flow id is for the
ledger and the archive, and is written in words.
```

Lines added:

```
Voices are addressed by name; a flow id is for the
ledger and the archive. It is written as three
words of the BIP-39 list in camelCase, carrying
33 bits of the harness session id, and is read
back as bits, not as a respelling of characters:
the words give eight hex characters and one bit,
so the transcript is found by that prefix and a
range on the ninth character.
```

Measured, for the ruling: 275 flows exist today. Three words are 33 bits, even odds of a clash near 109,000 flows. Two words are 22 bits, even odds near 2,400 flows, with the existing rule of growing by one word on a clash.

Ruling 4: (a) three words. (b) two words, growing to three on a clash. (c) amend.
<!-- to-the-living:end -->
