<!-- to-the-living:start -->
Presentation.{ «Operation» }

How it is now. `Vision/` holds no section named operation. `Vision/nexus.md` (last changed 2026-09-11) speaks of the middle part only under "Processing is for the effect" ("Conversion is the wrong frame for it. The name is open, Apply liked."), "Actors" and "Documents" ("The nexus and sema documents are undesigned"); `Vision/ethos.md` "Roots" names Library, Signal, Sema and no Operation root; `Vision/highLevelView.md` has two headings, "The very high-level view is looked at routinely" and "A view takes room", and nothing on the Nexus; `Intent/conversion.md` holds "A kind names one conversion". ethos-zero 16.0.0 (`/git/github.com/LiGoldragon/ethos-zero`, HEAD `c2653dd`, 2026-10-03) reads an `Operation` root of four sections, imports, operations, outcomes, types (`src/lib.rs`, `pub struct Operation`, documented "The section order is proposed, pending the living's word"), and generates from it two enums, `Operation` and `Outcome`, with no function and no kind. Of the 101 `.ethos` files under `/git/github.com/LiGoldragon` (four levels deep), one is headed `Operation`: the fixture `fixtures/print/flow-operation.ethos`. The `nexus` library 0.5.0 (`c495f2a`) holds no entry point. On his order of today, vision statements migrate from Vision/ into the psyche repository as Vision-type skills; each [vision] proposal names its Vision/ file as its home today and travels with the migration.

**1. Operation is what a Nexus does** [vision]
File: `Vision/nexus.md`, new section after "Processing is for the effect".
Now: no such section.
Proposed:
> ## Operation
>
> Operation is what a Nexus does. It stands between signal and memory: a signal reaches memory only through operation, and what memory answers comes back through operation before it leaves as signal. Anything that can have an effect has its operation, and that operation is the type the Nexus uses for it: one operation for every effect.

Grounded: 2026-10-02, 91ea9f, typed: "Anything that can have an effect is going to have a corresponding operation". Assumes Ruling 1 (a).

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 210" width="700" role="img" aria-label="The enforced path through a Nexus">
  <defs><marker id="op-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>
  <g font-family="sans-serif" font-size="14" fill="currentColor" text-anchor="middle">
    <rect x="10" y="40" width="120" height="70" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="70" y="68" font-weight="bold">Signal</text><text x="70" y="90" font-size="12">Launch.{ … }</text>
    <rect x="150" y="40" width="120" height="70" rx="8" fill="none" stroke="#c77d1a" stroke-width="2.5"/>
    <text x="210" y="68" font-weight="bold">Operation</text><text x="210" y="90" font-size="12">Start.{ … }</text>
    <rect x="290" y="40" width="120" height="70" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="350" y="68" font-weight="bold">Memory</text><text x="350" y="90" font-size="12">Flow record</text>
    <rect x="430" y="40" width="120" height="70" rx="8" fill="none" stroke="#c77d1a" stroke-width="2.5"/>
    <text x="490" y="68" font-weight="bold">Operation</text><text x="490" y="90" font-size="12">Started.7</text>
    <rect x="570" y="40" width="120" height="70" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="630" y="68" font-weight="bold">Signal</text><text x="630" y="90" font-size="12">Launched.7</text>
    <g stroke="currentColor" stroke-width="1.5" marker-end="url(#op-a)"><line x1="130" y1="75" x2="148" y2="75"/><line x1="270" y1="75" x2="288" y2="75"/><line x1="410" y1="75" x2="428" y2="75"/><line x1="550" y1="75" x2="568" y2="75"/></g>
    <path d="M70,40 C70,8 350,8 350,38" fill="none" stroke="#b03030" stroke-width="1.5" stroke-dasharray="5 4"/>
    <text x="210" y="12" font-size="12" fill="#b03030">no path: signal never reaches memory</text>
    <rect x="10" y="140" width="680" height="40" rx="8" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>
    <text x="350" y="165">the standard entry point calls the parts in this order and holds the memory</text>
  </g>
</svg>

*The enforced path: signal, operation, memory, operation, signal. Illustration of the flow, not his: the Flow Nexus's Launch and Start as the example.*

**2. Processing is for the effect** [vision]
File: `Vision/nexus.md`, section "Processing is for the effect".
Now:
> An object enters a Nexus for the effect; the response follows as an
> effect of it. Conversion is the wrong frame for it. The name is open,
> Apply liked.

Proposed:
> An object enters a Nexus for the effect; the response follows as an effect of it. Each effect is done by its operation, and each operation comes to an outcome: the effect took place, or it did not, and why, typed. Conversion is the wrong frame for it.

Grounded: 2026-10-02, 91ea9f: a response back "that the effect has taken place". Assumes Ruling 1 (a) and Ruling 2 (b).

**3. Operations compose** [vision]
File: `Vision/nexus.md`, new section after "Operation".
Now: no such section.
Proposed:
> ## Operations compose
>
> Work with more than one effect is done by more than one operation, one for each effect, in the order the work needs. Each operation comes to its outcome; the next takes what it needs from the outcomes before it; the outcomes together make the response. A change in memory comes back as a successful or unsuccessful change, and that change is an input to operation like any other.

Grounded: 2026-10-02, 91ea9f: memory has "a standard successful or unsuccessful change". The flow's proposal, not his: the order of composition, each operation taking the outcomes before it.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 260" width="700" role="img" aria-label="One request decomposed into its effects">
  <defs><marker id="op-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>
  <g font-family="sans-serif" font-size="13" fill="currentColor" text-anchor="middle">
    <rect x="10" y="100" width="120" height="60" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="70" y="119" font-weight="bold">Launch</text><text x="70" y="136" font-size="12">Mind.Primary</text><text x="70" y="152" font-size="12">and a brief</text>
    <rect x="170" y="30" width="150" height="60" rx="8" fill="none" stroke="#c77d1a" stroke-width="2.5"/>
    <text x="245" y="55" font-weight="bold">Start</text><text x="245" y="75" font-size="12">Mind.Primary, capsule</text>
    <rect x="360" y="30" width="150" height="60" rx="8" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
    <text x="435" y="55">effect:</text><text x="435" y="75" font-size="12">a machine launched</text>
    <rect x="170" y="170" width="150" height="60" rx="8" fill="none" stroke="#c77d1a" stroke-width="2.5"/>
    <text x="245" y="195" font-weight="bold">Record</text><text x="245" y="215" font-size="12">7, Started</text>
    <rect x="360" y="170" width="150" height="60" rx="8" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
    <text x="435" y="195">effect:</text><text x="435" y="215" font-size="12">Flow record in Memory</text>
    <text x="580" y="65" font-weight="bold">Started.7</text><text x="580" y="205" font-weight="bold">Recorded</text>
    <rect x="590" y="105" width="100" height="50" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="640" y="135" font-weight="bold">Launched.7</text>
    <g stroke="currentColor" stroke-width="1.5" fill="none" marker-end="url(#op-b)">
      <path d="M130,120 L168,62"/><path d="M130,140 L168,198"/>
      <line x1="320" y1="60" x2="358" y2="60"/><line x1="320" y1="200" x2="358" y2="200"/>
      <line x1="510" y1="60" x2="545" y2="60"/><line x1="510" y1="200" x2="545" y2="200"/>
      <path d="M560,72 C520,120 300,120 255,168" stroke-dasharray="4 3"/>
      <path d="M600,72 L630,103"/><path d="M600,192 L630,157"/>
    </g>
    <text x="410" y="132" font-size="12">the flow id 7 feeds Record</text>
  </g>
</svg>

*One request, two effects, two operations; Start's outcome feeds Record, and both outcomes make the response. Illustration of the flow, not his: the mapping of Launch to Start and Record.*

**4. The standard entry point** [vision]
File: `Vision/nexus.md`, new section after "Operations compose".
Now: no such section.
Proposed:
> ## The standard entry point
>
> Every Nexus enters through one standard entry point, written like a Rust macro, for its executable or its library; the Nexus is the only main call, and it loads its signal. The entry point calls the parts in one order: signal takes the query in; operation does the work; memory makes its change or answers; operation brings that answer to an outcome; signal sends the response. The entry point alone holds the memory, so code that would reach memory from signal does not compile. The ethos names every type on this path, so reading the ethos shows the main objects and processes; the operation bodies are written by hand.

Grounded: 2026-10-04, 5ed94b, typed: "a standard entry point for the main executable". Assumes Rulings 4 (a), 5 (a) and 7 (b).

**5. The Operation root** [vision]
File: `Vision/ethos.md`, new section after "Roots".
Now: no such section.
Proposed:
> ## The Operation root
>
> An Operation file declares what a Nexus does, in four sections: imports; the operations, one variant for every effect, named as verbs; the outcomes, what each operation comes to, named in the past tense, a failure naming itself; the types they carry. It yields one `Operation` type and one `Outcome` type.
>
> ```
> ; What the Flow Nexus does: one operation for every effect
> Operation
> ; the shared types this root uses, from the Flow Library
> [ flow:[ FlowId Voice Event ] ]
> ; the operations: Start launches a flow, Record appends an event
> [ Start.{ Voice
>           Capsule }
>   Record.{ FlowId
>            Event } ]
> ; what each operation comes to
> [ Started.FlowId
>   Recorded
>   Failed.String ]
> ; the types the operations carry
> [ Capsule.{ Home.String
>             Login.Vector<String> } ]
> ```

Grounded: 2026-10-02, 91ea9f: "When we define its operation we define all of the operation types". The four sections are ethos-zero 16.0.0's, not his word; assumes Ruling 3 (b).

Witness, ethos-zero at `c2653dd`, `target/debug/ethos-zero`: the file above answers `Checked.…/flow-operation.ethos` and `Generate` writes Rust byte-identical to `tests/generated/flow-operation.rs`. The signatures it generates for `Start` (derives, `#[rustfmt::skip]` and `Capsule` omitted, each condensed to one line):

```rust
pub struct Start_Data { pub voice: flow::Voice, pub capsule: Capsule }
pub enum Operation { Start(Start_Data), Record(Record_Data) }
pub enum Outcome { Started(flow::FlowId), Recorded, Failed(String) }
```

The datom of this operation, of its outcome, and of the Flow record that Record leaves in memory (`flow-memory.ethos`), each printed by `datomize(..).protosize().textualize()` in a scratch copy of `tests/generated.rs`:

```
Start.{ Mind.Primary
        { /home/flow
          [ claude ] } }
Started.7
{ 7
  Mind.Primary
  Running
  [ Started ] }
```

**6. A machine call is an operation** [vision]
File: `Vision/nexus.md`, new section after "The standard entry point".
Now: no such section.
Proposed:
> ## A machine call is an operation
>
> A call to a machine is an operation, programmed with an ethos spec. It receives the spec of what it is expected to say, a few examples, a prose explanation, and the word that it now speaks the spec; it answers in datom of the spec's response types. An answer that breaks the spec is refused naming the part it broke, and the call is corrected against it. Its outcome is typed like any other.

Grounded: 2026-09-19, b81560, STT: "It could involve a subflow, calling a subflow that's trying to use this spec".

**7. Deterministic work is done by code** [vision]
File: `Intent/deterministicWork.md`.
Now: no such file.
Proposed:
> # Deterministic work
>
> ## Deterministic work is done by code
>
> Whatever is deterministic is done in code, never by a machine call, to save the context, cost and noise a machine would spend on it. A machine call is kept to the choice a machine is needed for, among a few typed options, and the rest is automated.

Grounded: 2026-10-03, 5578cc, typed: "a deterministic cheap program can do"; he asked for it as Intent.

**8. The nexus skill names the path** [implementation]
File: `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`, line 6, the sentence beginning "Its three parts".
Now:
> Its three parts are the three layers of ethos: Signal is what it says, Operation is what it does, Memory is what it remembers.

Proposed:
> Its three parts are the three layers of ethos: Signal is what it says, Operation is what it does, Memory is what it remembers. A signal reaches memory only through operation and comes back through it; there is one operation for every effect, each coming to a typed outcome; the standard entry point calls the parts in that order and holds the memory; operation bodies are hand-written, and deterministic work is never given to a machine call.

Grounded: 2026-10-04, 5ed94b. Follows on his yes to proposals 1, 4 and 7.

**9. The ethos skill's Operation example carries comments** [implementation]
File: `/git/github.com/LiGoldragon/Curriculum/skills/vision-ethos.md`, lines 45 to 53.
Now:
```
Operation                                 ; sections proposed, not yet his word
[ flow:[ FlowId Voice Event ] ]
[ Start.{ Voice Capsule }
  Record.{ FlowId Event } ]
[ Started.FlowId
  Recorded
  Failed.String ]
[ Capsule.{ Home.String
            Login.Vector<String> } ]
```
Proposed:
```
; What the Flow Nexus does: one operation for every effect
Operation
; the shared types this root uses, from the Flow Library
[ flow:[ FlowId Voice Event ] ]
; the operations: Start launches a flow, Record appends an event
[ Start.{ Voice
          Capsule }
  Record.{ FlowId
           Event } ]
; what each operation comes to
[ Started.FlowId
  Recorded
  Failed.String ]
; the types the operations carry
[ Capsule.{ Home.String
            Login.Vector<String> } ]
```

Grounded: 2026-10-02, 91ea9f. Follows on his yes to proposal 5.

**10. The standard entry point in the nexus library** [implementation]
File: `/git/github.com/LiGoldragon/nexus/src/entry.rs`.
Now: no such file.
Proposed (compiles with rustc, edition 2024, as a library on its own):
```rust
/// What a Nexus says: its query and response types.
pub trait Signaling { type Query; type Response; }

/// What a Nexus remembers: an edit goes in, a change comes out.
pub trait Remembering {
    type Edit;
    type Change; // a successful or unsuccessful change, typed
    fn change(&mut self, edit: Self::Edit) -> Self::Change;
}

/// What a Nexus does, between its signal and its memory; bodies by hand.
pub trait Operating<S: Signaling, M: Remembering> {
    type Operation;
    type Outcome;
    fn operation(query: S::Query) -> Self::Operation;  // signal → operation
    fn edit(operation: &Self::Operation) -> M::Edit;     // operation → memory
    fn outcome(operation: Self::Operation, change: M::Change) -> Self::Outcome; // memory → operation
    fn response(outcome: Self::Outcome) -> S::Response;  // operation → signal
}

/// The standard entry point: it alone holds the memory.
pub struct Entry<M> { memory: M }

impl<M: Remembering> Entry<M> {
    pub fn open(memory: M) -> Self { Entry { memory } }

    pub fn answer<S: Signaling, O: Operating<S, M>>(&mut self, query: S::Query) -> S::Response {
        let operation = O::operation(query);
        let change = self.memory.change(O::edit(&operation));
        O::response(O::outcome(operation, change))
    }
}
```

Grounded: 2026-10-04, 5ed94b. Follows on his yes to proposal 4. The flow's proposal, not his: the traits Signaling, Remembering, Operating and Entry, and their method names. It carries one operation per query; composition (proposal 3) widens `operation` to a sequence on his yes to 3.

## Rulings

1. What the middle part is called.
   (a) operation: 2026-10-02 (91ea9f, typed, "signal, operation, and memory") and 2026-10-04 (5ed94b, "the operation actor/system").
   (b) process, or the Nexus core: 2026-09-13 (024bc7, STT, "the process or Nexus core") and 2026-10-02, earlier the same day (91ea9f, "Maybe we call it the process").
2. Processing as conversion or as effect.
   (a) conversion, TryFrom chains: 2026-08-21 (`vision-raw/mainFunction.md`, STT).
   (b) effect, one operation per effect: 2026-08-26 (f426777b, STT) and 2026-10-02 (91ea9f, typed).
3. Whether operation has its own ethos root.
   (a) no: roots Library, Signal, Sema (`Vision/ethos.md` "Roots", distilled 2026-09-09).
   (b) yes: 2026-09-13 (024bc7, STT, the three layers "described in ethos") and 2026-10-02 (91ea9f, "the actual ethos of the three layers").
4. A standard main.
   (a) wanted: 2026-08-22 (bc05da32), 2026-09-19 (b81560) and 2026-10-04 (5ed94b).
   (b) set aside: 2026-09-10 (fe34eb, "overthinking the whole nexus-core runtime concept").
5. Who writes the operation bodies.
   (a) by hand, the structure enforced: 2026-10-04 (5ed94b), and `Vision/ethos.md` "Kinds are explicit; bodies are hand-written" (undated in the file).
   (b) the whole program in ethos within months: 2026-09-25 (e51411) and 2026-09-29 (c64ee3, STT).
6. Whose conversion the entry point's macro generates.
   (a) the macro generates "input selection and conversion boilerplate": 2026-08-22 (bc05da32, typed).
   (b) no text serialization logic in the Nexus: 2026-09-28 (8904b1).
7. An architecture guard.
   (a) refused, as a tool written for one repository: 2026-08-18 (2b34fafa, typed).
   (b) wanted, as a compile-time check through kinds and the entry point: 2026-09-14 (6cc91b) and 2026-10-04 (5ed94b).
<!-- to-the-living:end -->
