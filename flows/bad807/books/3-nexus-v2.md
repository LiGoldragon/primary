<!-- to-the-living:start -->
Presentation.{ «The Nexus» }

## Where it stands

Four nexuses run, each on an ordinary and a meta socket.

```
Orchestrate Nexus   0.37.0
Flow Nexus          0.23.0     flow-nexus on PATH resolves 0.12.2
Message Nexus       0.19.0     meta socket: message-owner.sock
Lojix Nexus         8.1.0
```

- ethos-zero 16.0.0 reads four roots: Library, Signal, Operation, Memory.
- Flow alone has a generated Operation root (`flow-nexus/ethos/operation.ethos`, 81 lines).
- Each Nexus writes its own `main`: Flow 111 lines, Orchestrate 39, Message 37, Lojix 21.
- The `nexus` library 0.5.0 has configuration, authority, situation and relocation types, no entry point; Orchestrate and Lojix use it, Flow and Message do not.
- Flow 0.24.0's store takes the signal straight in (`store.rs:673`, called from `lib.rs:122`).

`Vision/nexus.md` has no section on layers. `Vision/flowNexus.md` speaks of Flow alone.
Vision statements migrate into the psyche repository as Vision-type skills; each [vision] proposal names its `Vision/` file as its home today.

## The anatomy

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300" width="700" font-family="sans-serif" font-size="14">
<defs><marker id="n1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="300" fill="#fff"/>
<rect x="10" y="105" width="95" height="70" rx="6" fill="#eee" stroke="#555"/><text x="57" y="135" text-anchor="middle">CLI</text><text x="57" y="155" text-anchor="middle" font-size="12">datom text</text><rect x="135" y="15" width="555" height="275" rx="10" fill="#f4f7fc" stroke="#2b4a8b" stroke-width="2"/><text x="412" y="40" text-anchor="middle" font-weight="bold">One Nexus, entered only through its entry point</text>
<rect x="135" y="112" width="14" height="22" fill="#2b4a8b"/><rect x="135" y="146" width="14" height="22" fill="#8b2b4a"/><g stroke="#333"><rect x="175" y="100" width="130" height="80" rx="8" fill="#e3ecfb"/><rect x="365" y="100" width="130" height="80" rx="8" fill="#fdf0d8"/><rect x="545" y="100" width="130" height="80" rx="8" fill="#e2f4e6"/></g>
<g text-anchor="middle" font-weight="bold"><text x="240" y="135">Signal</text><text x="430" y="135">Operation</text><text x="610" y="135">Memory</text></g><g text-anchor="middle" font-size="12"><text x="240" y="155">what it says</text><text x="430" y="155">what it does</text><text x="610" y="155">what it remembers</text></g>
<g stroke="#333" stroke-width="2" marker-end="url(#n1)"><line x1="105" y1="123" x2="173" y2="123"/><line x1="305" y1="115" x2="363" y2="115"/><line x1="495" y1="115" x2="543" y2="115"/><line x1="545" y1="168" x2="497" y2="168"/><line x1="365" y1="168" x2="307" y2="168"/><line x1="175" y1="160" x2="107" y2="160"/></g><g font-size="12" text-anchor="middle"><text x="334" y="96">1 intend</text><text x="520" y="96">2 change</text><text x="520" y="196">3 Succeeded | Failed</text><text x="334" y="196">4 outcome</text><text x="120" y="96">query</text><text x="120" y="195">5 response</text></g>
<path d="M240,182 C240,265 610,265 610,182" fill="none" stroke="#b00" stroke-width="2" stroke-dasharray="6 5"/><text x="425" y="258" text-anchor="middle" fill="#b00" font-size="13">no path: Signal never holds Memory</text><text x="160" y="282" font-size="12">ordinary socket (blue), meta socket (red); rkyv inside, datom only at the CLI</text>
</svg>

Three parts, one path: signal → operation → memory → operation → signal.

## The anatomy in code

The whole Flow Nexus in the four roots, as proposed.

```
Library                                  ; what the three parts share
[]                                       ; imports: none
[ FlowId.Integer                         ; types
  Voice.{ Aspect Layer }                 ;   who a flow speaks for: an aspect at a layer
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Event.[ Started Stopped ] ]
[]                                       ; kinds
[]                                       ; associations

Signal                                   ; what Flow says, on its ordinary socket
[ flow:[ FlowId Voice Event ] ]          ; imports from the Library
[ Launch.{ Voice Brief.String }          ; queries
  Report.{ FlowId Event } ]
[ Launched.FlowId                        ; responses
  Refused.[ NoCapsule VoiceBusy.Voice ]
  Reported ]
[]                                       ; types

Operation                                ; what Flow does: one operation for every effect
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Start.{ Voice Capsule }                ; operations
  Record.{ FlowId Event } ]
[ Started.FlowId                         ; outcomes
  Recorded
  Failed.[ CapsuleRefused StoreRefused ] ]
[ Capsule.{ Home.String Login.Vector<String> } ]   ; types

Memory                                   ; what Flow remembers
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Flow.{ FlowId Voice State.[ Running Ended ] Vector<Event> } ]   ; record types
```

Illustration only: not run through ethos-zero; FlowId 7 below and the brief are invented.

## One signal's path

```
Launch.{ { Psyche Primary } «Draft the Nexus book» }   ; 1 Query, typed at the CLI
Start.{ { Psyche Primary } { /home/li/primary [] } }   ; 2 Operation, from Signal's intend
Flow.{ 7 { Psyche Primary } Running [ Started ] }      ; 3 the Change handed to Memory
Succeeded                                              ; 4 Memory answers Operation
Started.7                                              ; 5 Outcome
Launched.7                                             ; 6 Response, back to the CLI
```

Shown as datom; inside the Nexus each is an rkyv value.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 330" width="700" font-family="sans-serif" font-size="13">
<defs><marker id="n3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect width="700" height="330" fill="#fff"/>
<g stroke="#333"><rect x="15" y="10" width="90" height="30" rx="5" fill="#eee"/><rect x="145" y="10" width="100" height="30" rx="5" fill="#eee"/><rect x="285" y="10" width="90" height="30" rx="5" fill="#e3ecfb"/><rect x="425" y="10" width="90" height="30" rx="5" fill="#fdf0d8"/><rect x="565" y="10" width="90" height="30" rx="5" fill="#e2f4e6"/></g><g text-anchor="middle" font-weight="bold"><text x="60" y="30">socket</text><text x="195" y="30">entry point</text><text x="330" y="30">Signal</text><text x="470" y="30">Operation</text><text x="610" y="30">Memory</text></g>
<g stroke="#999" stroke-dasharray="4 4"><line x1="60" y1="40" x2="60" y2="320"/><line x1="195" y1="40" x2="195" y2="320"/><line x1="330" y1="40" x2="330" y2="320"/><line x1="470" y1="40" x2="470" y2="320"/><line x1="610" y1="40" x2="610" y2="320"/></g><g stroke="#333" stroke-width="1.6" marker-end="url(#n3)"><line x1="60" y1="65" x2="193" y2="65"/><line x1="195" y1="90" x2="328" y2="90"/><line x1="470" y1="165" x2="608" y2="165"/><line x1="195" y1="140" x2="468" y2="140"/><line x1="195" y1="240" x2="328" y2="240"/><line x1="195" y1="290" x2="62" y2="290"/></g>
<g stroke="#2b4a8b" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#n3)"><line x1="330" y1="115" x2="197" y2="115"/><line x1="610" y1="190" x2="472" y2="190"/><line x1="470" y1="215" x2="197" y2="215"/><line x1="330" y1="265" x2="197" y2="265"/></g><g font-size="12"><text x="72" y="60">1 frame: rkyv Query</text><text x="203" y="85">2 intend(Query)</text><text x="215" y="110">3 Operation</text><text x="203" y="135">4 perform(Operation, Remembrance)</text><text x="478" y="160">5 change(Change)</text><text x="490" y="185">6 Succeeded | Failed</text><text x="215" y="210">7 Outcome</text><text x="203" y="235">8 answer(Outcome)</text><text x="215" y="260">9 Response</text><text x="80" y="285">10 frame: rkyv Response</text></g>
<text x="200" y="315" font-size="12" fill="#b00">every arrow is the entry point's; hand-written code fills only the boxes</text>
</svg>

One signal through the entry point: ten steps, none hand-written (calls solid, returns dashed).

## The layers

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 300" width="700" font-family="sans-serif" font-size="14">
<rect width="700" height="300" fill="#fff"/><g stroke="#555" fill="#f4f7fc"><rect x="10" y="15" width="380" height="62" rx="6"/><rect x="10" y="85" width="380" height="62" rx="6"/><rect x="10" y="155" width="380" height="62" rx="6"/><rect x="10" y="225" width="380" height="62" rx="6" stroke-dasharray="6 4"/></g>
<g font-weight="bold"><text x="22" y="50">Primary</text><text x="22" y="120">Secondary</text><text x="22" y="190">Tertiary</text><text x="22" y="252">Quaternary</text></g><text x="22" y="272" font-size="12" fill="#b00">Ruling 8</text><g stroke="#333"><g fill="#e3ecfb"><rect x="140" y="29" width="76" height="34" rx="5"/><rect x="140" y="99" width="76" height="34" rx="5"/><rect x="140" y="169" width="76" height="34" rx="5"/><rect x="140" y="239" width="76" height="34" rx="5"/></g><g fill="#fdf0d8"><rect x="224" y="29" width="76" height="34" rx="5"/><rect x="224" y="99" width="76" height="34" rx="5"/><rect x="224" y="169" width="76" height="34" rx="5"/><rect x="224" y="239" width="76" height="34" rx="5"/></g><g fill="#e2f4e6"><rect x="308" y="29" width="76" height="34" rx="5"/><rect x="308" y="99" width="76" height="34" rx="5"/><rect x="308" y="169" width="76" height="34" rx="5"/><rect x="308" y="239" width="76" height="34" rx="5"/></g></g>
<g font-size="12" text-anchor="middle"><text x="178" y="51">Psyche</text><text x="262" y="51">Mind</text><text x="346" y="51">Field</text><text x="178" y="121">Psyche</text><text x="262" y="121">Mind</text><text x="346" y="121">Field</text><text x="178" y="191">Psyche</text><text x="262" y="191">Mind</text><text x="346" y="191">Field</text><text x="178" y="261">Psyche</text><text x="262" y="261">Mind</text><text x="346" y="261">Field</text></g><g stroke="#333" stroke-width="2"><line x1="390" y1="150" x2="410" y2="150"/><line x1="410" y1="40" x2="410" y2="262"/><line x1="410" y1="40" x2="430" y2="40"/><line x1="410" y1="114" x2="430" y2="114"/><line x1="410" y1="188" x2="430" y2="188"/><line x1="410" y1="262" x2="430" y2="262"/></g>
<g fill="#fff" stroke="#2b4a8b" stroke-width="2"><rect x="430" y="15" width="260" height="50" rx="6"/><rect x="430" y="89" width="260" height="50" rx="6"/><rect x="430" y="163" width="260" height="50" rx="6"/><rect x="430" y="237" width="260" height="50" rx="6"/></g><g font-weight="bold"><text x="442" y="36">Flow Nexus 0.23.0</text><text x="442" y="110">Message Nexus 0.19.0</text><text x="442" y="184">Orchestrate Nexus 0.37.0</text><text x="442" y="258">Lojix Nexus 8.1.0</text></g><text x="442" y="55" font-size="12">layer holder: Ruling 10</text>
</svg>

Four layers of authority, each holding voices (`Voice.{ Aspect Layer }`), beside the four running nexuses.

## Proposals

### 1. Three parts and one path — landed
Landed in `Vision/nexus.md` with example code.

### 2. The standard entry point — pointer
Now designed as actors in «The standard entry point: three actors, one path»; rule there.

### 3. [vision] `Vision/nexus.md`, "Library and daemon"

Now:
> Every component built from now on is a Nexus. The nexus repository is the library that defines the core of a Nexus component.

Proposed:
> The nexus repository is the core library of every Nexus. It defines the kinds of the three parts and the standard entry point, and it keeps the parts apart at compile time: only an operation's kind can touch a memory type, so no signal reaches memory except through an operation.

Grounded: "an architecture guard basically". Assumes Ruling 5(b).

### 4. [vision] `Vision/nexus.md`, "Signal only"

Now:
> Every client speaks to a Nexus in pure signal, fully binary. A Nexus speaks only the signal contracts it is compiled with; two of these are its own, one per socket. A Nexus thinks in typed values — enums, structs, scalars — and the string fields it still carries are records on the way to a fully typed form.

Proposed:
> Every client speaks to a Nexus in pure signal, fully binary. A Nexus speaks only the signal contracts it is compiled with; two of these are its own, one per socket. A Nexus never handles text: it decodes known types in their rkyv form, and every text form of a value, datom or an identifier's printed form, is made outside it, in a CLI or an interface.

Grounded: "so that it's not actually in the Nexus".

### 5. [vision] `Vision/nexus.md`, "Why everything is a Nexus"

Now:
> Everything built from now on is a Nexus, and what was built in another shape is rewritten as one. The consistency creates reliability, quality, and clarity.

Proposed:
> Every runtime component is a Nexus, and what runs in another shape is rewritten as one. A library stays a library: kinds, datom and other code compiled into a Nexus are not themselves Nexuses. The consistency creates reliability, quality, and clarity.

Grounded: "the runtime part of course". Assumes Ruling 4(a).

### 6. [vision] `Vision/nexus.md`, new "An operation may be a machine call"

Now: no such section.
Proposed:
> An operation may be performed by a machine call. The call is given the ethos spec of what it is to answer, a few datom examples and a prose explanation, and is then told it speaks that spec. It answers in datom of the spec's response types; an answer outside the spec is returned to it naming the part of the spec it broke.

Grounded: "now we switch to this spec".

### 7. [vision] `Vision/nexus.md`, new "Layers"

Now: no such section.
Proposed:
> Flows run in four layers of authority: Primary, Secondary, Tertiary, Quaternary. One Nexus holds each flow's layer and answers, for a calling process, which layer it belongs to. Spawning and messaging are controlled by the more highly permissioned nexuses.

Grounded: "controlled by more highly permissioned nexuses". Assumes Ruling 8(b); the holder is Ruling 10.

### 8. [implementation] `Curriculum/skills/vision-nexus.md`, line 6

On his yes to 1 to 3. Now:
> A Nexus is the long-running whole: its executable `<nexus>-nexus`, at least two sockets, one default CLI client per socket, and the signal contracts it is compiled with. It is a Nexus, never a daemon.
>
> Its three parts are the three layers of ethos: Signal is what it says, Operation is what it does, Memory is what it remembers. A Nexus is a vertex in the graph of nexuses; an edge joins two vertices and carries one contract; every connected pair has an ordinary edge, only some a meta edge.

Proposed, after "what it remembers.":
> A signal reaches memory only through operation and returns through it. Every Nexus's `main` is the one line `nexus::main!(<Nexus>);`; the `nexus` library's entry point owns that path and its kinds keep the three parts apart.

Grounded: the three-part path.

### 9. [implementation] `nexus/ethos/nexus.ethos`, new

The core library's types and part kinds.

```
Library                                  ; the nexus core library: what every Nexus shares
[]                                       ; imports: none
[ Part.[ Signal Operation Memory ]       ; types: the three parts
  Step.[ Received Intended Changing      ;   the path, in order
         Remembered Performed Answered ]
  Changed.[ Succeeded Failed ]           ;   every memory change answers one of these
  Socket.[ Ordinary Meta ] ]             ;   the two sockets every Nexus opens
; kinds: one per part, only the entry point calls them; Query, Operation, Outcome and
; Response are each Nexus's own types, generated from its Signal and Operation roots
[ Signaling.[ intend.[ Operation ] answer.[ Response ] ]
  Operating.[ perform.[ Outcome ] ]
  Remembering.[ change.[ Changed ] ] ]
[]                                       ; associations
```

Unchecked by ethos-zero 16.0.0; the kind-capability syntax is the flow's guess. Grounded: "expose the types used in core of the program (in ethos)".

### 10. [implementation] `nexus/src/entry.rs`, new

Now: `nexus` 0.5.0 has `authority.rs`, `configuration.rs`, `lib.rs`, `relocation.rs`, `situation.rs`.

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
/// Built only inside `enter`; private fields, so nothing else holds memory.
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
        // defaults → open memory with the Admission → bind both sockets, then per frame:
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

Illustration only; not compiled. Grounded: "make Nexus sort of the only main call".

### 11. [implementation] `flow/crates/flow-nexus/src/main.rs`, Flow first

Now: 111 hand-written lines (0.24.0) with `trait AnswersVersion` and the startup sequence, and in `store.rs:673`:

```rust
fn apply(&self, query: Query) -> Result<Response, StoreError>;
```

Proposed: `main.rs` becomes one line, and the store takes no `Query`.

```rust
nexus::main!(flow_nexus::FlowNexus);
// store.rs implements Remembering:
fn change(&mut self, change: memory::Flow) -> Changed;
```

Grounded: "the main function is standard".

### 12. [implementation] `Curriculum/skills/knowledge-nexus.md`, line 8

Now:
> Field's retained Home 83 result reports the running server engines as Orchestrate Nexus 0.37, Flow Nexus 0.23, Message Nexus 0.19, and Lojix Nexus 8.1. It reports these stable socket pairs:

Proposed:
> On 2026-10-04 the process list shows Orchestrate Nexus 0.37.0, Flow Nexus 0.23.0, Message Nexus 0.19.0 and Lojix Nexus 8.1.0 running; `flow-nexus` on `PATH` resolves 0.12.2, not the running 0.23.0.
>
> None enters through the standard entry point; Flow alone writes one of the three parts in ethos (its Operation root), Lojix and Orchestrate hold Library roots only, Message none. Their socket pairs:

Grounded: measured by this flow (process list, `readlink` of each binary on `PATH`, `/run` socket listing).

## Rulings
1. What Nexus names, and the middle part's name.
   - (a) Nexus is the whole; the middle part is Operation. 2026-08-19 to 2026-10-04; `Vision/nexus.md` approved 2026-09-11.
   - (b) Nexus is the core inside, the whole a metaNexus; the middle part is Process. 2026-09-13 to 2026-10-02.
2. The keeping part's name.
   - (a) Memory, Sema freed for the meaning language. 2026-09-26 to 2026-10-02.
   - (b) Sema, the database engine of a Nexus. 2026-09-10 (`Vision/sema.md` undated).
3. The nexus core language.
   - (a) Set aside, signal and memory types being enough. 2026-09-10 (one record).
   - (b) The core described in ethos. 2026-09-13, 2026-09-14.
4. Everything a Nexus, and its limits.
   - (a) Every runtime component, libraries excepted. 2026-08-19 to 2026-08-26.
   - (b) Some tools start as a plain server or a Clojure tool. 2026-08-28; 2026-09-29 (notion).
5. An architecture guard.
   - (a) A guard written for one repository is foolish. 2026-08-18 (one record).
   - (b) The kinds and the entry point are the guard. 2026-09-14, 2026-10-04.
6. What the entry macro converts.
   - (a) It takes a datom-derived type and writes the input conversion. 2026-08-22 (one record).
   - (b) No datom in a Nexus; conversion lives in the CLI. 2026-10-03 (one record).
7. The messaging Nexus's name.
   - (a) Message. 2026-09-17 (one record).
   - (b) Messenger. 2026-09-25 (one record).
8. Layers of authority: three or four. Settled at four, by the tertiary/quaternary ruling.
   - (a) Three: Primary, Secondary, Tertiary. 2026-09-14 (one record).
   - (b) Four, with Quaternary. 2026-09-26, 2026-09-27.
9. Layers of ethos: three or four.
   - (a) Three specifications, one per part. 2026-10-02 (one record).
   - (b) Four roots, Library beside the three parts. 2026-09-09; ethos-zero 16.0.0 as deployed.
10. Which Nexus holds a flow's layer.
   - (a) Persona. 2026-09-14, 2026-09-16.
   - (b) Flow. 2026-09-16 (one record).
<!-- to-the-living:end -->
