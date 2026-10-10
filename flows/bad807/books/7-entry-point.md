<!-- to-the-living:start -->
Presentation.{ «The standard entry point: three actors, one path» }

How a Nexus starts today: each of the four running Nexuses writes its own `main`.
Running, measured 2026-10-04: Flow 0.23.0, Message 0.19.0, Orchestrate 0.37.0, Lojix 8.1.0.
None keeps a signal away from its store by construction.

## Today's entry points

On origin/main, measured 2026-10-04:

- Flow 0.24.0: 111 lines in `crates/flow-nexus/src/main.rs` (version answer, directories, store, two serving threads); its store takes the signal `Query` directly (`store.rs:673`).
- Message 0.19.1: 37 lines.
- Orchestrate 0.37.1: 39 lines, a tokio runtime of two workers around one kameo 0.22 actor.
- Lojix 9.0.1: 21 lines, `Daemon::from_environment` then `run`; kameo 0.20 and triad-runtime, whose `Runner` types each step by a marker trait (`src/runner.rs`, `src/role.rs`).
- Flow and Message use no actor library.
- Each running Nexus is its own `/nix/store/…/bin/<nexus>-nexus`.
- The `nexus` core library 0.5.0 holds configuration, authority, situation and relocation types, with no entry point and no actor; Orchestrate and Lojix depend on it, Flow and Message do not.

## The rule

His words (typed, book comment, 2026-10-04): "Operations can talk to both. Signal can only talk to operation. Memory can only talk to operation. That way we have to go through this operation process."

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 340" width="700" font-family="sans-serif" font-size="14"> <defs><marker id="e1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs> <rect width="700" height="340" fill="#fff"/> <rect x="300" y="15" width="140" height="55" rx="8" fill="#eee" stroke="#555"/><text x="370" y="40" text-anchor="middle" font-weight="bold">Main actor</text><text x="370" y="58" text-anchor="middle" font-size="11">builds the three at start</text> <rect x="15" y="110" width="210" height="190" rx="10" fill="#f4f7fc" stroke="#2b4a8b" stroke-width="2"/><text x="120" y="135" text-anchor="middle" font-weight="bold">Signal actor</text> <g fill="#fff" stroke="#2b4a8b"><rect x="30" y="150" width="180" height="32" rx="5"/><rect x="30" y="192" width="180" height="32" rx="5"/><rect x="30" y="234" width="180" height="32" rx="5"/></g> <g font-size="12" text-anchor="middle"><text x="120" y="171">ordinary socket listener</text><text x="120" y="213">meta socket listener</text><text x="120" y="255">connection, one per peer</text><text x="120" y="290" fill="#555">sub-actors</text></g> <rect x="300" y="160" width="140" height="80" rx="8" fill="#fff" stroke="#333" stroke-width="2"/><text x="370" y="195" text-anchor="middle" font-weight="bold">Operation actor</text><text x="370" y="215" text-anchor="middle" font-size="11">holds the only memory handle</text> <rect x="545" y="160" width="140" height="80" rx="8" fill="#fff" stroke="#333"/><text x="615" y="195" text-anchor="middle" font-weight="bold">Memory actor</text><text x="615" y="215" text-anchor="middle" font-size="11">holds no handle</text> <g stroke="#333" stroke-width="2" marker-end="url(#e1)"><line x1="370" y1="70" x2="370" y2="158"/><line x1="225" y1="185" x2="298" y2="185"/><line x1="300" y1="218" x2="227" y2="218"/><line x1="440" y1="185" x2="543" y2="185"/><line x1="545" y1="218" x2="442" y2="218"/></g> <g font-size="11" text-anchor="middle"><text x="410" y="118">operation handle</text><text x="262" y="178">Operation</text><text x="262" y="234">Outcome</text><text x="492" y="178">change, read</text><text x="492" y="234">Changed, value</text></g> <text x="350" y="328" text-anchor="middle" font-size="12" fill="#555">every arrow is a handle the entry point gives out at start; no other edge exists</text> </svg>

Figure 1. The four actors and their only edges: signal and memory talk to operation alone; main keeps only the operation handle.

The flow's proposals in this book, none of them his words: the reading that the main actor talks only to operation; the actor names `MainActor`, `SignalActor`, `OperationActor`, `MemoryActor`; way (b); and the kameo dependency. Each is marked again where it appears. The sources of every block are in `flows/bad807/evidence/entry-point/`.

## The test subject

The candidates are drafted Nexuses that run nowhere. None appears in the process list of 2026-10-04 or in a CriomOS or CriomOS-home `.nix` file.

- Chronos 0.3.0 (`/git/github.com/LiGoldragon/chronos`): the local sky, location and solar events. 1485 lines of source. Its server is a skeleton: three `TODO(chronos-impl)` in `src/daemon.rs`, and `redb` declared but never opened.
- agent 0.3.0: machine calls to an OpenAI-compatible provider, 2626 lines, on triad-runtime. Every real query needs a live provider.
- mentci-nexus 0.1.0 (`primary-next/flows/0ab019/unity-local-poc`): a localhost proof of concept inside a flow's directory, with no repository of its own to branch.
- Persona 0.2.0 and router 0.12.0: about 16,000 and 20,000 lines; too large for a first test.

The flow proposes Chronos:

- Its store is unwritten, so the three parts are laid down rather than retrofitted.
- Its one-row memory (where the observer stands) gives a real write and a real read with no network.
- It is small enough to read whole, and useful once its sky is wired.

## Three ways to enforce the edges

All the code below is the flow's design. It was built in a scratch workspace with rustc 1.97.1, kameo 0.22.2, tokio 1.53.1 and redb 4.3.0. The sources are in `flows/bad807/evidence/entry-point/`; for what compiled, see the end of this section.

**(a) Typed handles.** An actor's fields are its edges. Memory is reached only through a `MemoryHandle` and operation only through an `OperationHandle`. Their fields are private, so outside code cannot build one.

Compiled in the scratch workspace crate `nexus-entry`.

```rust
/// The only way to memory. Given to the operation actor alone.
pub struct MemoryHandle<M: Remembering> { actor: ActorRef<MemoryActor<M>> }
impl<M: Remembering> MemoryHandle<M> {
    pub async fn change(&self, change: M::Change) -> Changed {
        self.actor.ask(Change(change)).await.unwrap_or(Changed::Failed)
    }
    pub async fn read(&self, reading: M::Reading) -> Option<M::Remembered> {
        self.actor.ask(Reading(reading)).await.ok()
    }
}
/// The only way to operation; held by main and signal.
pub struct OperationHandle<N: Nexus> { actor: ActorRef<OperationActor<N>> }

pub struct MainActor<N: Nexus> { operation: OperationHandle<N> }
pub struct SignalActor<N: Nexus> { signal: N::Signal, operation: OperationHandle<N> }
pub struct OperationActor<N: Nexus> { operation: N::Operation, memory: MemoryHandle<N::Memory> }
pub struct MemoryActor<M: Remembering> { memory: M }

impl<N: Nexus> Message<Frame> for SignalActor<N> {          // one frame in, one frame out
    type Reply = Result<Vec<u8>, Infallible>;
    async fn handle(&mut self, frame: Frame, _: &mut Context<Self, Self::Reply>) -> Self::Reply {
        let response = match self.signal.decode(&frame.0) {
            None => self.signal.undecodable(),
            Some(query) => {
                let operation = self.signal.intend(query);
                match self.operation.perform(operation).await {
                    Some(outcome) => self.signal.answer(outcome),
                    None => self.signal.undecodable(),
                }
            }
        };
        Ok(self.signal.encode(response))
    }
}
```

- For: the actor graph is visible in four struct definitions, and a wrong edge is a type error.
- Against: on its own, each Nexus's `main` builds the handles, so their constructors must be public to it. The guard then becomes a convention.
- Against: it says nothing about what an operation is, so the ethos is not read by the compiler.

**(b) The standard entry point.** The core library defines the three part kinds, builds the four actors and holds (a)'s handles. A Nexus writes only the three bodies, and its `main` is one line. Abridged below: the associated types' bounds and the three rkyv frame methods are left out, and `enter`'s body is shown as a comment. Compiled in the scratch workspace crate `nexus-entry`, unabridged.

```rust
pub trait Signaling: Send + Sync + 'static {                // sees no memory
    type Query; type Response; type Operation; type Outcome;
    fn intend(&self, query: Self::Query) -> Self::Operation;
    fn answer(&self, outcome: Self::Outcome) -> Self::Response;
    // decode, encode, undecodable: the rkyv frame at the socket
}
pub trait Remembering: Sized + Send + 'static {              // opened only with an Admission
    type Change; type Reading; type Remembered;
    fn open(admission: Admission) -> Option<Self>;
    fn change(&mut self, change: Self::Change) -> Changed;
    fn read(&self, reading: Self::Reading) -> Self::Remembered;
}
pub trait Operating<M: Remembering>: Send + 'static {        // the one part handed memory
    type Operation; type Outcome;
    fn perform(&mut self, operation: Self::Operation, memory: &MemoryHandle<M>)
        -> impl Future<Output = Self::Outcome> + Send;
}
pub struct Admission { directory: PathBuf }                  // no public constructor
pub trait Nexus: Send + 'static {
    type Memory: Remembering;
    type Operation: Operating<Self::Memory>;
    type Signal: Signaling<Operation = <Self::Operation as Operating<Self::Memory>>::Operation,
                           Outcome = <Self::Operation as Operating<Self::Memory>>::Outcome>;
    fn signal() -> Self::Signal;
    fn operation() -> Self::Operation;
    fn directory() -> PathBuf;                               // the executable owns its default
}
pub trait Entering: Nexus + Sized {                          // the one path, written once
    fn open(directory: PathBuf) -> Option<(MainActor<Self>, Door<Self>)> {
        let memory = Self::Memory::open(Admission { directory })?;
        let memory = MemoryHandle { actor: MemoryActor::spawn(memory) };
        let operation = OperationHandle { actor: OperationActor::<Self>::spawn((Self::operation(), memory)) };
        let signal = SignalActor::<Self>::spawn((Self::signal(), operation.clone()));
        Some((MainActor { operation }, Door { signal }))
    }
    fn enter() -> std::process::ExitCode { /* runtime, open, serve until terminated */ }
}
impl<N: Nexus> Entering for N {}
#[macro_export]
macro_rules! main {
    ($nexus:ty) => { fn main() -> std::process::ExitCode { <$nexus as $crate::Entering>::enter() } };
}
```

Figure 2. What `Entering::open` does, in order: memory first, the signal actor last; each actor receives only the handle it may use.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 330" width="640" font-family="sans-serif" font-size="13" role="img" aria-label="Order in which open builds the actors"> <defs><marker id="e3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs> <rect width="640" height="330" fill="#fff"/> <g stroke="#333" stroke-width="1.6" fill="none" marker-end="url(#e3)"><line x1="215" y1="46" x2="215" y2="64"/><line x1="215" y1="112" x2="215" y2="130"/><line x1="215" y1="178" x2="215" y2="196"/><line x1="215" y1="244" x2="215" y2="262"/></g> <rect x="20" y="14" width="390" height="32" rx="5" fill="#f3efe0" stroke="#8a7a2b"/><text x="30" y="35" fill="#222">Admission { directory }: only the library can build it</text> <rect x="20" y="66" width="390" height="46" rx="5" fill="#f4f7fc" stroke="#2b4a8b"/><text x="30" y="86" fill="#222">1 Memory::open(admission), then spawn Memory actor</text><text x="30" y="104" font-size="11" fill="#444">gives out: MemoryHandle</text> <rect x="20" y="132" width="390" height="46" rx="5" fill="#eaf4ea" stroke="#2e7d32"/><text x="30" y="152" fill="#222">2 spawn Operation actor with (operation, MemoryHandle)</text><text x="30" y="170" font-size="11" fill="#444">gives out: OperationHandle</text> <rect x="20" y="198" width="390" height="46" rx="5" fill="#f4f7fc" stroke="#2b4a8b"/><text x="30" y="218" fill="#222">3 spawn Signal actor with (signal, OperationHandle)</text><text x="30" y="236" font-size="11" fill="#444">holds no MemoryHandle</text> <rect x="20" y="264" width="390" height="46" rx="5" fill="#eee" stroke="#555"/><text x="30" y="284" fill="#222">4 return (MainActor, Door)</text><text x="30" y="302" font-size="11" fill="#444">MainActor keeps the OperationHandle only</text> <text x="430" y="90" font-size="12" fill="#555">memory handle:</text><text x="430" y="106" font-size="12" fill="#555">operation actor only</text> <text x="430" y="224" font-size="12" fill="#555">signal reaches memory</text><text x="430" y="240" font-size="12" fill="#555">only through operation</text> </svg>

Chronos's hand-written operation body, and its whole `main.rs`. Compiled in the scratch workspace crate `chronos-toy` against ethos-zero 16.0.0's output and redb 4.3.0; its test ran and passed.

```rust
impl Operating<ChronosMemory> for ChronosOperation {
    type Operation = Operation;
    type Outcome = Outcome;
    async fn perform(&mut self, operation: Operation, memory: &MemoryHandle<ChronosMemory>) -> Outcome {
        match operation {
            Operation::Keep(placement) => match memory.change(placement).await {
                Changed::Succeeded => Outcome::Kept,
                Changed::Failed => Outcome::Failed(Failed_Data::StoreRefused),
            },
            Operation::Recall => match memory.read(Latest).await {
                Some(Some(placement)) => Outcome::Recalled(placement),
                Some(None) => Outcome::Failed(Failed_Data::NothingKept),
                None => Outcome::Failed(Failed_Data::StoreRefused),
            },
        }
    }
}
```
```rust
nexus_entry::main!(chronos_toy::Chronos);
```

- For: the edges live in one library, so no Nexus can wire them differently. The handle constructors and `Admission` stay private to that library.
- For: it works today on ethos-zero 16.0.0's output, which is enums only.
- Against: `perform` is one method over the whole `Operation` enum, so the match is hand-written. And Rust cannot stop a signal body from opening a second store with `redb` by hand; the guard covers every path through the Nexus's own memory type.

**(c) Generated from ethos.** ethos-zero would emit, beside the enums, a `Signaling` kind with no memory in it and an `Operating` kind with one method per operation. Memory's constructor would be visible only inside the operation module. Compiled in the scratch workspace crate `chronos-generated`, written by hand in the shape ethos-zero would emit; its round-trip test ran and passed.

```rust
pub mod operation {                                          // emitted
    pub struct Memory { placing: Option<Placement> }
    impl Memory {
        pub(in crate::operation) fn open() -> Self { Self { placing: None } }
        pub fn change(&mut self, placing: Placement) -> Changed { self.placing = Some(placing); Changed::Succeeded }
        pub fn placing(&self) -> Option<&Placement> { self.placing.as_ref() }
    }
    pub trait Operating {                                    // one method for every operation
        fn keep(&mut self, placement: Placement, memory: &mut Memory) -> Outcome;
        fn recall(&mut self, memory: &Memory) -> Outcome;
    }
    impl Operation {
        pub fn perform<O: Operating>(self, operating: &mut O, memory: &mut Memory) -> Outcome {
            match self {
                Operation::Keep(placement) => operating.keep(placement, memory),
                Operation::Recall => operating.recall(memory),
            }
        }
    }
    pub struct Entry<S: Signaling, O: Operating> { signal: S, operating: O, memory: Memory }
    impl<S: Signaling, O: Operating> Entry<S, O> {
        pub fn new(signal: S, operating: O) -> Self { Self { signal, operating, memory: Memory::open() } }
        pub fn receive(&mut self, query: Query) -> Response {
            let operation = self.signal.intend(query);
            let outcome = operation.perform(&mut self.operating, &mut self.memory);
            self.signal.answer(outcome)
        }
    }
}
pub mod signal {                                             // emitted
    pub trait Signaling {
        fn intend(&self, query: Query) -> Operation;
        fn answer(&self, outcome: Outcome) -> Response;
    }
}
```

- For: the ethos becomes the guard. A new operation in `operation.ethos` is a missing method until it is written, which is his "effective compliance with ethos".
- Against: ethos-zero 16.0.0 emits no kind, no trait and no module privacy, so the generator must grow first.
- Against: a generated memory holds its store in generated code, so any change to the store engine goes through the generator.

**What compiled.** Every block above comes from three crates, all built:

- `nexus-entry` holds (a) and (b).
- `chronos-toy` holds Chronos on (b): the four files ethos-zero 16.0.0 generated from the ethos below, datom-codec 0.32.2 with `rkyv`, and redb. Its test `a_placement_goes_through_operation_to_memory_and_back` passes: through one door, on a redb file in a temporary directory, `Locate` answers `Refused.Unplaced`, `Place` answers `Placed`, and `Locate` then answers `Located` with the same placement.
- `chronos-generated` holds (c) by hand in the emitted shape; its round-trip test passes.

Figure 3. Which handle a signal body can reach (green) and the four it cannot (red), each with the compiler's error code.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 330" width="700" font-family="sans-serif" font-size="13" role="img" aria-label="Signal body reaches operation only; four reaches for memory are refused"> <defs><marker id="g4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2e7d32"/></marker><marker id="r4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#b00020"/></marker></defs> <rect width="700" height="330" fill="#fff"/> <rect x="15" y="20" width="150" height="290" rx="10" fill="#f4f7fc" stroke="#2b4a8b" stroke-width="2"/><text x="90" y="50" text-anchor="middle" font-weight="bold" fill="#222">Signal body</text><text x="90" y="68" text-anchor="middle" font-size="11" fill="#444">hand-written</text> <line x1="165" y1="60" x2="440" y2="60" stroke="#2e7d32" stroke-width="2.4" marker-end="url(#g4)"/> <rect x="442" y="38" width="243" height="44" rx="6" fill="#eaf4ea" stroke="#2e7d32"/><text x="452" y="57" fill="#222">OperationHandle.perform</text><text x="452" y="74" font-size="11" fill="#444">allowed: the one edge</text> <g stroke="#b00020" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#r4)"><line x1="165" y1="130" x2="440" y2="130"/><line x1="165" y1="190" x2="440" y2="190"/><line x1="165" y1="250" x2="440" y2="250"/><line x1="165" y1="300" x2="440" y2="300"/></g> <g fill="#fdecee" stroke="#b00020"><rect x="442" y="108" width="243" height="44" rx="6"/><rect x="442" y="168" width="243" height="44" rx="6"/><rect x="442" y="228" width="243" height="44" rx="6"/><rect x="442" y="278" width="243" height="40" rx="6"/></g> <g fill="#222"><text x="452" y="127">build an Admission</text><text x="452" y="187">build a MemoryHandle</text><text x="452" y="247">read OperationHandle.actor</text><text x="452" y="296">call (c)'s Memory::open</text></g> <g font-size="11" fill="#b00020" font-weight="bold"><text x="452" y="144">E0451: private field</text><text x="452" y="204">E0451: private field</text><text x="452" y="264">E0616: private field read</text><text x="452" y="311">E0624: private method</text></g> </svg>

Four signal-side reaches for memory fail to compile, each error confirmed by its own build in the scratch workspace (rustc 1.97.1; `compile_fail` doctests in `chronos-toy` and `chronos-generated`):

- building an `Admission`: E0451;
- building a `MemoryHandle`: E0451;
- reading `OperationHandle.actor`: E0616;
- calling (c)'s `Memory::open`: E0624.

Where the sources are: `flows/bad807/evidence/entry-point/`, with a `README.md` listing the files and the commands that built and tested them.

The socket listeners are drawn but not built: `Door::knock` stands where a connection sub-actor will hand in frames, and `enter()` opens the actors and waits for termination.

**The flow's proposal: (b), carrying (a)'s handles.** Only (b) keeps the handle constructors private, because only there does the library, not each Nexus, build them. It needs nothing ethos-zero lacks today. (c) is where (b) goes once ethos-zero emits kinds: the same traits, written from the ethos instead of by hand.

## Chronos in the four roots

Ran: ethos-zero 16.0.0 checked these four roots and generated the four files in `chronos-toy/src/generated/` from them, comments included. The design is the flow's.

```
Library                                    ; what Chronos's three parts share
[]                                         ; imports: none
[ Location.{ Latitude.Decimal              ; types: where the observer stands, in degrees
             Longitude.Decimal }
  Voice.{ Aspect Layer }                   ;   who set it: an aspect at a layer
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Placement.{ Location Voice } ]           ;   a location and the voice that set it
[]                                         ; kinds: none yet
[]                                         ; associations: none yet

Signal                                     ; what Chronos says on its ordinary socket
[ chronos:[ Placement ] ]                  ; imports from the Library
[ SetLocation.Placement                    ; queries: set where the observer stands
  GetLocation ]                            ;   ask where the observer stands
[ Placed                                   ; responses
  Located.Placement
  Refused.[ Unplaced                       ;   refusals are vocabulary, never strings
            StoreRefused ] ]
[]                                         ; types: none of its own

Operation                                  ; what Chronos does: one operation for every effect
[ chronos:[ Placement ] ]                  ; imports from the Library
[ Keep.Placement                           ; operations: keep a placement in memory
  Recall ]                                 ;   read the kept placement back
[ Kept                                     ; outcomes
  Recalled.Placement
  Failed.[ NothingKept                     ;   memory holds no placement yet
           StoreRefused ] ]                ;   memory answered Failed
[]                                         ; types: none of its own

Memory                                     ; what Chronos remembers
[ chronos:[ Placement ] ]                  ; imports from the Library
[ Placing.Placement ]                      ; record types: the one placement kept
```

The queries are the real Chronos 0.3.0 contract, `SetLocation` and `GetLocation`; the evidence directory's toy used the illustrative names `Place` and `Locate`.

The import `chronos:` resolves because the crate names itself: `extern crate self as chronos;`. `Recall` is an operation although it changes nothing, because under his edges signal reaches memory only through operation, reads included.

One placement through the path, as datom (inside the Nexus each is an rkyv value). Illustration, not run: these lines were written by hand and were not run through datom-codec.

```
SetLocation.{ { 47.6 -122.3 } { Psyche Primary } } ; 1 Query, at the CLI, sent as signal
Keep.{ { 47.6 -122.3 } { Psyche Primary } }       ; 2 Operation, from Signal's intend
{ { 47.6 -122.3 } { Psyche Primary } }            ; 3 the Placing, handed by Operation to Memory
Succeeded                                         ; 4 Memory's answer
Kept                                              ; 5 Outcome
Placed                                            ; 6 Response, from Signal's answer
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="700" font-family="sans-serif" font-size="13"> <defs><marker id="e2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs> <rect width="700" height="320" fill="#fff"/> <g fill="#eef2f7" stroke="#333"><rect x="20" y="10" width="100" height="30" rx="5"/><rect x="195" y="10" width="130" height="30" rx="5"/><rect x="395" y="10" width="110" height="30" rx="5"/><rect x="570" y="10" width="110" height="30" rx="5"/></g> <g text-anchor="middle" font-weight="bold"><text x="70" y="30">peer (CLI)</text><text x="260" y="30">Signal actor</text><text x="450" y="30">Operation actor</text><text x="625" y="30">Memory actor</text></g> <g stroke="#999" stroke-dasharray="4 4"><line x1="70" y1="40" x2="70" y2="295"/><line x1="260" y1="40" x2="260" y2="295"/><line x1="450" y1="40" x2="450" y2="295"/><line x1="625" y1="40" x2="625" y2="295"/></g> <g stroke="#333" stroke-width="1.6" marker-end="url(#e2)"><line x1="70" y1="70" x2="258" y2="70"/><line x1="260" y1="125" x2="448" y2="125"/><line x1="450" y1="155" x2="623" y2="155"/></g> <g stroke="#333" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#e2)"><line x1="625" y1="185" x2="452" y2="185"/><line x1="450" y1="215" x2="262" y2="215"/><line x1="260" y1="270" x2="72" y2="270"/></g> <g fill="#fff" stroke="#2b4a8b"><rect x="200" y="82" width="120" height="30" rx="4"/><rect x="200" y="227" width="120" height="30" rx="4"/></g> <g font-size="12"><text x="78" y="64">1 frame: rkyv Place</text><text x="268" y="119">3 perform(Keep)</text><text x="458" y="149">4 change(Placing)</text><text x="490" y="179">5 Succeeded</text><text x="300" y="209">6 Kept</text><text x="78" y="264">8 frame: rkyv Placed</text></g> <g font-size="11" text-anchor="middle"><text x="260" y="101">2 decode, intend</text><text x="260" y="246">7 answer, encode</text></g> <text x="350" y="312" text-anchor="middle" font-size="12" fill="#b00">the memory handle exists only inside the operation actor; steps 4 and 5 are its only path</text> </svg>

Figure 4. One signal in and its answer out: Signal decodes and intends, Operation performs against Memory, and the answer leaves the way it came.

## The test on a branch (the flow's plan)

1. `nexus`, branch `entry-point` from `main`: add `src/entry.rs` as in (b), with kameo 0.22 and tokio; version 0.6.0.
2. `chronos`, branch `entry-point` from `main`: add `ethos/` with the four roots and `src/generated/`, plus a test that regenerates with ethos-zero 16.0.0 and compares.
3. Write the three parts on redb at `<state>/chronos.redb`; `src/bin/chronos_daemon.rs` becomes `nexus::main!(chronos::Chronos);`.
4. Compile-time assertion: four fixture crates, each a signal body reaching for memory. Each must fail with its code (E0451, E0451, E0616, and E0624 once (c) lands); the test reads the compiler's error code, since stable rustdoc does not check `compile_fail` codes.
5. Run-time assertion: start `chronos-nexus` on a temporary directory and send `SetLocation`, then `GetLocation`, over its ordinary socket. Expect `Placed`, then `Located` with the same placement. Restart it and expect `GetLocation` to answer `Located` again.
6. Chronos `main` and every running Nexus stay untouched.

## Proposals

Each is the flow's proposal, written under the rulings at the end; none is landed.

**1. [vision] `/home/li/primary/Vision/nexus.md`, section "Three parts and one path", after its first paragraph.**
Now:
> A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.

Proposed:
> Every Nexus runs four actors: a main actor, a signal actor, an operation actor and a memory actor. The signal actor holds sub-actors, one for each socket and each connection. Signal talks only to operation; memory talks only to operation; operation talks to both; the main actor builds the three and then talks only to operation. Every Nexus enters through one standard entry point, which builds the actors and gives each the handles of its edges, and nothing else does. So every signal goes through the operation process to reach memory and comes back the same way. Hand-written code implements the three parts and cannot reach around the path: the compiler refuses it.

Grounded: 2026-10-04, bad807, "Signal can only talk to operation" (typed, book comment, 2026-10-04). Flow's proposal: the main-actor sentence and the actor names are the drafter's. Assumes Ruling 1(b).

**2. [vision] `/home/li/primary/Vision/nexus.md`, section "Actors".**
Now:
> The engine inside a Nexus is driven by Kameo actors. The standards
> of their use are still to be designed. Arc-Mutex is permitted.

Proposed:
> The engine inside a Nexus is driven by Kameo actors: the four of the standard entry point and the sub-actors each holds. An actor reaches another only through a handle it was given, and the entry point gives out every handle. Arc-Mutex is permitted.

Grounded: 2026-08-22, fd301d9a, "we are definitely using kameo actors in nexus". Assumes Ruling 2(a).

**3. [implementation] `/git/github.com/LiGoldragon/nexus/src/entry.rs` and `Cargo.toml`.**
Now: `src/entry.rs` does not exist; `Cargo.toml` of 0.5.0 reads:
> [dependencies]
> rkyv = { version = "0.8", default-features = false, features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"] }
> thiserror = "2"

Proposed: `src/entry.rs` is `flows/bad807/evidence/entry-point/nexus-entry/src/lib.rs` (8391 bytes) verbatim; `Cargo.toml` gains
> kameo = { version = "0.22", default-features = false, features = ["macros"] }
> tokio = { version = "1", features = ["rt-multi-thread", "macros", "net", "io-util", "signal", "sync"] }

and the version becomes 0.6.0. Flow's proposal: the kameo dependency is the drafter's choice, following Orchestrate's use of kameo 0.22. Assumes Ruling 1(b).

Grounded: 2026-10-04, 5ed94b, "standard main flow, like a macro in Rust".

**4. [implementation] `/git/github.com/LiGoldragon/chronos/src/bin/chronos_daemon.rs`, on branch `entry-point` from `main`.**
Now:
> #[tokio::main(flavor = "multi_thread")]
> async fn main() -> chronos::Result<()> {
>     chronos::daemon::run().await
> }

Proposed: the file is the one line `nexus::main!(chronos::Chronos);`; beside it, `ethos/` holds the four roots above, `src/generated/` the four generated files, and `src/lib.rs` the three parts, as in `chronos-toy` in the evidence directory. Assumes Ruling 3(a).

Grounded: 2026-10-04, bad807, "one of our non-production-ready ideas" (typed, book comment, 2026-10-04).

**5. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`, line 6.**
Now:
> Its three parts are the three layers of ethos: Signal is what it says, Operation is what it does, Memory is what it remembers. A Nexus is a vertex in the graph of nexuses;

Proposed: after "what it remembers.":
> Four actors run it, main, signal, operation and memory: signal and memory talk only to operation, main only to operation, and the standard entry point builds them and gives out every handle.

Grounded: 2026-10-04, bad807, "Signal can only talk to operation" (typed, book comment, 2026-10-04). Assumes his yes to 1.

**6. [implementation] `/git/github.com/LiGoldragon/Curriculum/skills/knowledge-nexus.md`, after line 13.**
Now (line 13):
> - Lojix: `/run/lojix/ordinary.sock` and `/run/lojix/meta.sock`.

Proposed:
> Drafted Nexuses that run nowhere, measured 2026-10-04: Chronos 0.3.0, agent 0.3.0, Persona 0.2.0, router 0.12.0, and mentci-nexus 0.1.0 in `primary-next/flows/0ab019`. None enters through a standard entry point.

Grounded: 2026-10-04, bad807, measured by the flow from the process list, a `.nix` search and each `Cargo.toml`.

**7. [implementation] `/git/github.com/LiGoldragon/ethos-zero`, generator: the kinds of (c).**
Now: 16.0.0 emits, for Chronos's Operation root, only the enums of `chronos-toy/src/generated/operation.rs` (`Operation`, `Failed_Data`, `Outcome`), each opening:
> #[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]

Proposed: emit `Signaling` from the Signal root, and from the Operation root `Operating` with one method per operation plus the `perform` dispatch, both shaped as in (c), so that (b)'s hand-written match is generated. Assumes Ruling 1(c), or (b) first and (c) after.

Grounded: 2026-10-04, 5ed94b, "effective compliance with ethos".

## Rulings

Dated; options only, no verdict. Date of this book: 2026-10-04.

1. Which way enforces the edges.
   (a) Typed handles alone, each Nexus wiring its own: 2026-10-04, bad807, typed, book comment on «The Nexus», "Signal can only talk to operation".
   (b) The standard entry point, `nexus::main!`, carrying the handles: 2026-09-14, 6cc91b, "make Nexus sort of the only main call"; 2026-10-04, 5ed94b, "standard main flow, like a macro in Rust".
   (c) Generated from ethos by ethos-zero: 2026-09-14, 6cc91b, "a kind becomes a higher-type kind compiler check: an architecture guard basically"; 2026-10-04, 5ed94b, "effective compliance with ethos".
2. Whether the core library is actor-based in name.
   (a) Yes: `MainActor`, `SignalActor`, `OperationActor`, `MemoryActor`: 2026-09-14, e1953c, "the Signal actor, the main Signal actor, or the Nexus actor"; 2026-10-04, "the operation actor".
   (b) No: the part kinds `Signaling`, `Operating`, `Remembering` carry the names, and the actors stay inside: 2026-09-14, e1953c, "Maybe we even have to find a better term for that"; 2026-10-04, "whether it is an actor-based language or whether it is different", to be refined after practice.
3. The test subject.
   (a) Chronos: 2026-10-04, "one of our non-production-ready ideas".
   (b) agent, the machine-call Nexus: 2026-10-04, "Maybe let's do something useful".
   (c) A running Nexus on a branch, Flow or Orchestrate: 2026-10-04, "like Flow, Message [sic], or Orchestrate, on a branch", then "A toy, I mean".
<!-- to-the-living:end -->
