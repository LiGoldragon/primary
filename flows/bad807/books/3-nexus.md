<!-- to-the-living:start -->
Presentation.{ «The Nexus» }

How it is now. `Vision/nexus.md` (125 lines) holds A Nexus is the whole, A kind of thing, Library and daemon, Universal traits first, Processing is for the effect, Documents, Sockets, Default clients, Signal only, The graph, Routing, Configuration, First configuration, Repositories, Why everything is a Nexus, Actors, Splitting a Nexus, Observation by subscription, Polling is forbidden; it has no section on the three parts, the path between them, an entry point, or layers. `Vision/flowNexus.md` (59 lines, eight headings) speaks of Flow alone; `Vision/highLevelView.md` asks that the very high-level view be looked at routinely. ethos-zero 16.0.0 (`c2653dd`) reads four roots, Library, Signal, Operation, Memory. Measured 2026-10-04 from the process list and `PATH`: Orchestrate 0.37.0, Flow 0.23.0, Message 0.19.0 and Lojix 8.1.0 run, each on an ordinary and a meta socket (Message's is `message-owner.sock`); `flow-nexus` on `PATH` resolves 0.12.2 while the running server is 0.23.0. Flow is the one Nexus with a generated Operation root (`flow/crates/flow-nexus/ethos/operation.ethos`, 81 lines). No Nexus enters through a shared entry point: each writes its own `main` (on origin/main, Flow 111 lines, Orchestrate 39, Message 37, Lojix 21). The `nexus` library 0.5.0 (`c495f2a`) holds configuration, authority, situation and relocation types and no entry point; Orchestrate and Lojix depend on it, Flow and Message do not. In Flow 0.24.0 the store's `apply` takes the signal `Query` and returns `Response` (`crates/flow-nexus/src/store.rs:673`), and `lib.rs:122` hands a Query to it directly. On his order of today, vision statements migrate from Vision/ into the psyche repository as Vision-type skills; each [vision] proposal names its Vision/ file as its home today and travels with the migration.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300" width="700" font-family="sans-serif" font-size="14">
<defs><marker id="n1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<rect width="700" height="300" fill="#fff"/>
<rect x="10" y="105" width="95" height="70" rx="6" fill="#eee" stroke="#555"/><text x="57" y="135" text-anchor="middle">CLI</text><text x="57" y="155" text-anchor="middle" font-size="12">datom text</text>
<rect x="135" y="15" width="555" height="275" rx="10" fill="#f4f7fc" stroke="#2b4a8b" stroke-width="2"/>
<text x="412" y="40" text-anchor="middle" font-weight="bold">One Nexus, entered only through nexus::main!</text>
<rect x="135" y="112" width="14" height="22" fill="#2b4a8b"/><rect x="135" y="146" width="14" height="22" fill="#8b2b4a"/>
<g fill="#fff" stroke="#333"><rect x="175" y="100" width="130" height="80" rx="8"/><rect x="365" y="100" width="130" height="80" rx="8"/><rect x="545" y="100" width="130" height="80" rx="8"/></g>
<g text-anchor="middle" font-weight="bold"><text x="240" y="135">Signal</text><text x="430" y="135">Operation</text><text x="610" y="135">Memory</text></g>
<g text-anchor="middle" font-size="12"><text x="240" y="155">what it says</text><text x="430" y="155">what it does</text><text x="610" y="155">what it remembers</text></g>
<g stroke="#333" stroke-width="2" marker-end="url(#n1)"><line x1="105" y1="123" x2="173" y2="123"/><line x1="305" y1="115" x2="363" y2="115"/><line x1="495" y1="115" x2="543" y2="115"/><line x1="545" y1="168" x2="497" y2="168"/><line x1="365" y1="168" x2="307" y2="168"/><line x1="175" y1="160" x2="107" y2="160"/></g>
<g font-size="12" text-anchor="middle"><text x="334" y="96">1 intend</text><text x="520" y="96">2 change</text><text x="520" y="196">3 Succeeded | Failed</text><text x="334" y="196">4 outcome</text><text x="120" y="96">query</text><text x="120" y="195">5 response</text></g>
<path d="M240,182 C240,265 610,265 610,182" fill="none" stroke="#b00" stroke-width="2" stroke-dasharray="6 5"/>
<text x="425" y="258" text-anchor="middle" fill="#b00" font-size="13">no path: Signal never holds Memory</text>
<text x="160" y="282" font-size="12">ordinary socket (blue), meta socket (red); rkyv inside, datom only at the CLI</text>
</svg>

The anatomy of one Nexus: three parts, and the one enforced path signal → operation → memory → operation → signal.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300" width="700" font-family="sans-serif" font-size="14">
<rect width="700" height="300" fill="#fff"/>
<g stroke="#555" fill="#f4f7fc"><rect x="10" y="15" width="330" height="62" rx="6"/><rect x="10" y="85" width="330" height="62" rx="6"/><rect x="10" y="155" width="330" height="62" rx="6"/><rect x="10" y="225" width="330" height="62" rx="6" stroke-dasharray="6 4"/></g>
<g font-weight="bold"><text x="22" y="40">Primary</text><text x="22" y="110">Secondary</text><text x="22" y="180">Tertiary</text><text x="22" y="250">Quaternary</text></g>
<text x="22" y="272" font-size="12" fill="#b00">fourth layer: Ruling 8</text>
<g fill="#fff" stroke="#333"><rect x="165" y="27" width="70" height="34" rx="5"/><rect x="245" y="27" width="70" height="34" rx="5"/><rect x="165" y="97" width="70" height="34" rx="5"/><rect x="245" y="97" width="70" height="34" rx="5"/><rect x="165" y="167" width="70" height="34" rx="5"/><rect x="245" y="167" width="70" height="34" rx="5"/><rect x="165" y="237" width="70" height="34" rx="5"/><rect x="245" y="237" width="70" height="34" rx="5"/></g>
<g font-size="12" text-anchor="middle"><text x="200" y="49">Psyche</text><text x="280" y="49">Mind</text><text x="200" y="119">Psyche</text><text x="280" y="119">Mind</text><text x="200" y="189">Psyche</text><text x="280" y="189">Mind</text><text x="200" y="259">Psyche</text><text x="280" y="259">Mind</text></g>
<line x1="340" y1="150" x2="400" y2="150" stroke="#333" stroke-width="2"/><line x1="400" y1="40" x2="400" y2="262" stroke="#333" stroke-width="2"/>
<g stroke="#333" stroke-width="2"><line x1="400" y1="40" x2="430" y2="40"/><line x1="400" y1="114" x2="430" y2="114"/><line x1="400" y1="188" x2="430" y2="188"/><line x1="400" y1="262" x2="430" y2="262"/></g>
<g fill="#fff" stroke="#2b4a8b" stroke-width="2"><rect x="430" y="15" width="260" height="50" rx="6"/><rect x="430" y="89" width="260" height="50" rx="6"/><rect x="430" y="163" width="260" height="50" rx="6"/><rect x="430" y="237" width="260" height="50" rx="6"/></g>
<g font-weight="bold"><text x="442" y="36">Flow Nexus 0.23.0</text><text x="442" y="110">Message Nexus 0.19.0</text><text x="442" y="184">Orchestrate Nexus 0.37.0</text><text x="442" y="258">Lojix Nexus 8.1.0</text></g>
<g font-size="12"><text x="442" y="55">layer holder: Ruling 10</text></g>
</svg>

The four layers of authority, each holding flows (Psyche and Mind voices), beside the four nexuses that run today.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 330" width="700" font-family="sans-serif" font-size="13">
<defs><marker id="n3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<rect width="700" height="330" fill="#fff"/>
<g fill="#eef2f7" stroke="#333"><rect x="15" y="10" width="90" height="30" rx="5"/><rect x="145" y="10" width="100" height="30" rx="5"/><rect x="285" y="10" width="90" height="30" rx="5"/><rect x="425" y="10" width="90" height="30" rx="5"/><rect x="565" y="10" width="90" height="30" rx="5"/></g>
<g text-anchor="middle" font-weight="bold"><text x="60" y="30">socket</text><text x="195" y="30">entry point</text><text x="330" y="30">Signal</text><text x="470" y="30">Operation</text><text x="610" y="30">Memory</text></g>
<g stroke="#999" stroke-dasharray="4 4"><line x1="60" y1="40" x2="60" y2="320"/><line x1="195" y1="40" x2="195" y2="320"/><line x1="330" y1="40" x2="330" y2="320"/><line x1="470" y1="40" x2="470" y2="320"/><line x1="610" y1="40" x2="610" y2="320"/></g>
<g stroke="#333" stroke-width="1.6" marker-end="url(#n3)"><line x1="60" y1="65" x2="193" y2="65"/><line x1="195" y1="90" x2="328" y2="90"/><line x1="470" y1="165" x2="608" y2="165"/><line x1="195" y1="140" x2="468" y2="140"/><line x1="195" y1="240" x2="328" y2="240"/><line x1="195" y1="290" x2="62" y2="290"/></g>
<g stroke="#333" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#n3)"><line x1="330" y1="115" x2="197" y2="115"/><line x1="610" y1="190" x2="472" y2="190"/><line x1="470" y1="215" x2="197" y2="215"/><line x1="330" y1="265" x2="197" y2="265"/></g>
<g font-size="12"><text x="72" y="60">1 frame: rkyv Query</text><text x="203" y="85">2 intend(Query)</text><text x="215" y="110">3 Operation</text><text x="203" y="135">4 perform(Operation, Remembrance)</text><text x="478" y="160">5 change(Change)</text><text x="490" y="185">6 Succeeded | Failed</text><text x="215" y="210">7 Outcome</text><text x="203" y="235">8 answer(Outcome)</text><text x="215" y="260">9 Response</text><text x="80" y="285">10 frame: rkyv Response</text></g>
<text x="200" y="315" font-size="12" fill="#b00">every arrow is the entry point's; hand-written code fills only the boxes</text>
</svg>

The standard entry point's call sequence for one signal: ten steps, none of them hand-written.

## The anatomy in code

The whole Flow Nexus in the four roots, as proposed (sections as ethos-zero 16.0.0 reads them).

```
Library                                  ; what the three parts share
[]                                       ; imports: none
[ FlowId.Integer                         ; types
  Voice.[ Psyche.Layer                   ;   who a flow speaks for, and at which layer
          Mind.Layer ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Event.[ Started Stopped ] ]
[]                                       ; kinds
[]                                       ; associations

Signal                                   ; what Flow says, on its ordinary socket
[ flow:[ FlowId Voice Event ] ]          ; imports from the Library
[ Launch.{ Voice                         ; queries
           Brief.String }
  Report.{ FlowId Event } ]
[ Launched.FlowId                        ; responses
  Refused.[ NoCapsule
            VoiceBusy.Voice ]
  Reported ]
[]                                       ; types

Operation                                ; what Flow does: one operation for every effect
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Start.{ Voice Capsule }                ; operations
  Record.{ FlowId Event } ]
[ Started.FlowId                         ; outcomes
  Recorded
  Failed.[ CapsuleRefused StoreRefused ] ]
[ Capsule.{ Home.String                  ; types
            Login.Vector<String> } ]

Memory                                   ; what Flow remembers
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Flow.{ FlowId                          ; record types
         Voice
         State.[ Running Ended ]
         Vector<Event> } ]
```

Illustration: FlowId 7 and the brief text are invented values, and the ethos above has not been run through ethos-zero.

One signal passing through, written as datom (inside the Nexus each is an rkyv value; only the CLI and this page show text):

```
Launch.{ Psyche.Primary «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
Start.{ Psyche.Primary { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
Flow.{ 7 Psyche.Primary Running [ Started ] }         ; 3 the Change Operation hands Memory
Succeeded                                             ; 4 Memory's answer to Operation
Started.7                                             ; 5 Outcome
Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
```

## Proposals

**1. [vision] `Vision/nexus.md`, new section "Three parts and one path".**
Now: no such section.
Proposed:
> A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.

Grounded: 2026-10-02, 91ea9f, "signal, operation, and memory"; the path 2026-10-04, 5ed94b. Assumes Rulings 1(a), 2(a).

**2. [vision] `Vision/nexus.md`, new section "The standard entry point".**
Now: no such section.
Proposed:
> Every Nexus enters through one standard entry point, a macro that writes its `main`. The entry point owns the path: it receives the signal, hands it to operation, gives operation alone its memory, and sends the answer back as signal. Hand-written code implements each part and cannot reach around the path, so the code complies with its ethos.

Grounded: 2026-10-04, 28d847, "so that the rest doesn't bypass it". Assumes Rulings 5(b) and 6(b).

**3. [vision] `Vision/nexus.md`, section "Library and daemon".**
Now:
> Every component built from now on is a Nexus. The nexus repository is
> the library that defines the core of a Nexus component.

Proposed:
> The nexus repository is the core library of every Nexus. It defines the kinds of the three parts and the standard entry point, and it keeps the parts apart at compile time: only an operation's kind can touch a memory type, so no signal reaches memory except through an operation.

Grounded: 2026-09-14, 6cc91b, "an architecture guard basically". Assumes Ruling 5(b).

**4. [vision] `Vision/nexus.md`, section "Signal only".**
Now:
> Every client speaks to a Nexus in pure signal, fully binary. A Nexus
> speaks only the signal contracts it is compiled with; two of these
> are its own, one per socket. A Nexus thinks in typed values — enums,
> structs, scalars — and the string fields it still carries are
> records on the way to a fully typed form.

Proposed:
> Every client speaks to a Nexus in pure signal, fully binary. A Nexus speaks only the signal contracts it is compiled with; two of these are its own, one per socket. A Nexus never handles text: it decodes known types in their rkyv form, and every text form of a value, datom or an identifier's printed form, is made outside it, in a CLI or an interface.

Grounded: 2026-10-03, edf227, "so that it's not actually in the Nexus".

**5. [vision] `Vision/nexus.md`, section "Why everything is a Nexus".**
Now:
> Everything built from now on is a Nexus, and what was built in
> another shape is rewritten as one. The consistency creates
> reliability, quality, and clarity.

Proposed:
> Every runtime component is a Nexus, and what runs in another shape is rewritten as one. A library stays a library: kinds, datom and other code compiled into a Nexus are not themselves Nexuses. The consistency creates reliability, quality, and clarity.

Grounded: 2026-08-22, cff271af, "the runtime part of course". Assumes Ruling 4(a).

**6. [vision] `Vision/nexus.md`, new section "An operation may be a machine call".**
Now: no such section.
Proposed:
> An operation may be performed by a machine call. The call is given the ethos spec of what it is to answer, a few datom examples and a prose explanation, and is then told it speaks that spec. It answers in datom of the spec's response types; an answer outside the spec is returned to it naming the part of the spec it broke.

Grounded: 2026-09-19, b81560, "now we switch to this spec".

**7. [vision] `Vision/nexus.md`, new section "Layers".**
Now: no such section.
Proposed:
> Flows run in four layers of authority: Primary, Secondary, Tertiary, Quaternary. One Nexus holds each flow's layer and answers, for a calling process, which layer it belongs to. Spawning and messaging are controlled by the more highly permissioned nexuses.

Grounded: 2026-09-13, 6cc91b, "controlled by more highly permissioned nexuses". Assumes Ruling 8(b); the holder is Ruling 10.

**8. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`, line 6, on his yes to 1 to 3.**
Now:
> A Nexus is the long-running whole: its executable `<nexus>-nexus`, at least two sockets, one default CLI client per socket, and the signal contracts it is compiled with. It is a Nexus, never a daemon. Its three parts are the three layers of ethos: Signal is what it says, Operation is what it does, Memory is what it remembers. A Nexus is a vertex in the graph of nexuses; an edge joins two vertices and carries one contract; every connected pair has an ordinary edge, only some a meta edge.

Proposed: the same line, with after "what it remembers.":
> A signal reaches memory only through operation and returns through it. Every Nexus's `main` is the one line `nexus::main!(<Nexus>);`; the `nexus` library's entry point owns that path and its kinds keep the three parts apart.

Grounded: 2026-10-04, 5ed94b, the three-part path.

**9. [implementation] `/git/github.com/LiGoldragon/nexus/ethos/nexus.ethos`, the core library's types.**
Now: no such file.
Proposed:
```
Library                                  ; the nexus core library: what every Nexus shares
[]                                       ; imports: none
[ Part.[ Signal                          ; types: the three parts
         Operation
         Memory ]
  Step.[ Received                        ;   the path, in order
         Intended
         Changing
         Remembered
         Performed
         Answered ]
  Changed.[ Succeeded Failed ]           ;   every memory change answers one of these
  Socket.[ Ordinary Meta ] ]             ;   the two sockets every Nexus opens
; kinds: one per part, only the entry point calls them; Query, Operation, Outcome and
; Response are each Nexus's own types, generated from its Signal and Operation roots
[ Signaling.[ intend.[ Operation ]
              answer.[ Response ] ]
  Operating.[ perform.[ Outcome ] ]
  Remembering.[ change.[ Changed ] ] ]
[]                                       ; associations
```
Unchecked: not run through ethos-zero 16.0.0; the kind-capability syntax (`intend.[ Operation ]`) is the flow's guess.

Grounded: 2026-09-10, fe34eb, "expose the types used in core of the program (in ethos)".

**10. [implementation] `/git/github.com/LiGoldragon/nexus/src/entry.rs`, the standard entry point.**
Now: no such file (`nexus` 0.5.0 has `authority.rs`, `configuration.rs`, `lib.rs`, `relocation.rs`, `situation.rs`).
Proposed:
```rust
/// Signal: what the Nexus says. It is never handed memory.
pub trait Signaling {
    type Query; type Response; type Operation; type Outcome;
    fn intend(&self, query: Self::Query) -> Self::Operation;
    fn answer(&self, outcome: Self::Outcome) -> Self::Response;
}
/// Operation: what the Nexus does; the one part given memory.
pub trait Operating<M: Remembering> {
    type Operation; type Outcome;
    fn perform(&mut self, operation: Self::Operation, memory: &mut Remembrance<M>) -> Self::Outcome;
}
/// Memory: what the Nexus remembers. Opening needs an Admission.
pub trait Remembering: Sized {
    type Change;
    fn open(admission: Admission) -> Result<Self, Refusal>;
    fn change(&mut self, change: Self::Change) -> Changed;
}
/// Built only inside `enter`; its fields are private, so nothing else holds memory.
pub struct Admission { situation: Situation }
pub struct Remembrance<M: Remembering> { memory: M }
pub trait Changing<M: Remembering> { fn change(&mut self, change: M::Change) -> Changed; }
impl<M: Remembering> Changing<M> for Remembrance<M> {
    fn change(&mut self, change: M::Change) -> Changed { self.memory.change(change) }
}
/// A whole Nexus names its parts; their types are generated from its ethos.
pub trait Nexus {
    type Memory: Remembering;
    type Operation: Operating<Self::Memory>;
    type Signal: Signaling<Operation = <Self::Operation as Operating<Self::Memory>>::Operation,
                           Outcome = <Self::Operation as Operating<Self::Memory>>::Outcome>;
    fn parts(configuration: &Configuration) -> (Self::Signal, Self::Operation);
}
/// The one path, provided once; the blanket impl leaves no Nexus its own.
pub trait Entering: Nexus {
    fn enter() -> ExitCode {
        // defaults → open memory with the Admission → bind ordinary and meta sockets, then per frame:
        //   let operation = signal.intend(query);
        //   let outcome = operation_part.perform(operation, &mut remembrance);
        //   socket.send(signal.answer(outcome));
        Served::until_terminated()
    }
}
impl<N: Nexus> Entering for N {}
#[macro_export]
macro_rules! main {
    ($nexus:ty) => { fn main() -> std::process::ExitCode { <$nexus as $crate::Entering>::enter() } };
}
```
Unchecked: illustration only; not compiled.

Grounded: 2026-09-14, 6cc91b, "make Nexus sort of the only main call".

**11. [implementation] `/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/main.rs`, Flow first.**
Now: 111 hand-written lines on origin/main `5e0b1bf` (0.24.0), opening `use flow_nexus::{`, with `trait AnswersVersion` and the startup sequence; and `crates/flow-nexus/src/store.rs:673`, `fn apply(&self, query: Query) -> Result<Response, StoreError>;`.
Proposed: `main.rs` is
```rust
nexus::main!(flow_nexus::FlowNexus);
```
and the store implements `Remembering` with `fn change(&mut self, change: memory::Flow) -> Changed;`, taking no `Query`.

Grounded: 2026-09-19, b81560, "the main function is standard".

**12. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/knowledge-nexus.md`, line 8.**
Now:
> Field's retained Home 83 result reports the running server engines as Orchestrate Nexus 0.37, Flow Nexus 0.23, Message Nexus 0.19, and Lojix Nexus 8.1. It reports these stable socket pairs:

Proposed:
> On 2026-10-04 the process list shows Orchestrate Nexus 0.37.0, Flow Nexus 0.23.0, Message Nexus 0.19.0 and Lojix Nexus 8.1.0 running; `flow-nexus` on `PATH` resolves 0.12.2, not the running 0.23.0. None enters through the standard entry point; Flow alone writes one of the three parts in ethos (its Operation root), Lojix and Orchestrate hold Library roots only, Message none. Their socket pairs:

Grounded: measured 2026-10-04 by this flow (process list, `readlink` of each binary on `PATH`, `/run` socket listing).

## Rulings

1. What Nexus names, and what the middle part is called.
   (a) Nexus is the whole long-running component and its middle part is Operation: 2026-08-19, e06e4c07; 2026-09-10, fe34eb; `Vision/nexus.md`, approved 2026-09-11; 2026-10-02, 91ea9f; 2026-10-04, 5ed94b.
   (b) Nexus is the core inside, the whole being a metaNexus, and the middle part is Process: 2026-09-13, 024bc7; 2026-09-14, 6cc91b and e1953c; 2026-10-02, 91ea9f.
2. The keeping part's name.
   (a) Memory, with Sema freed for the meaning language: 2026-09-26, b7ba00; 2026-09-28, 8904b1; 2026-10-02, 91ea9f.
   (b) Sema, the database engine of a Nexus: 2026-09-10, fe34eb (`Vision/sema.md` undated).
3. The nexus core language.
   (a) Set aside, signal and memory types being enough: 2026-09-10, fe34eb (one record).
   (b) The core described in ethos: 2026-09-13, 024bc7; 2026-09-14, 6cc91b.
4. Everything a Nexus, and its limits.
   (a) Every runtime component is a Nexus, libraries excepted: 2026-08-19, e06e4c07; 2026-08-22, cff271af; 2026-08-26, b675f3d9.
   (b) Some tools start as a plain server or a Clojure tool: 2026-08-28, 01a047d2; 2026-09-29, 6f51ad (notion).
5. An architecture guard.
   (a) A guard written for one repository is foolish: 2026-08-18, 2b34fafa (one record).
   (b) The kinds and the entry point are the guard: 2026-09-14, 6cc91b; 2026-10-04, 5ed94b.
6. What the entry macro converts.
   (a) It takes a datom-derived type and writes the input conversion: 2026-08-22, bc05da32 (one record).
   (b) No datom in a Nexus; conversion lives in the CLI: 2026-10-03, edf227 (one record).
7. The messaging Nexus's name.
   (a) Message: 2026-09-17, da1e3f (one record).
   (b) Messenger: 2026-09-25, e51411 (one record).
8. Layers of authority: three or four.
   (a) Three, Primary, Secondary, Tertiary: 2026-09-14, 6cc91b (one record).
   (b) Four, with Quaternary: 2026-09-26, e167d8; 2026-09-27, 5ac3a3.
9. Layers of ethos: three or four.
   (a) Three specifications, one per part: 2026-10-02, 91ea9f (one record).
   (b) Four roots, Library beside the three parts: 2026-09-09, 564f55; ethos-zero 16.0.0 as deployed 2026-10-04.
10. Which Nexus holds a flow's layer.
    (a) Persona: 2026-09-14, 6cc91b; 2026-09-16, f55ec8.
    (b) Flow: 2026-09-16, f55ec8 (one record).
<!-- to-the-living:end -->
