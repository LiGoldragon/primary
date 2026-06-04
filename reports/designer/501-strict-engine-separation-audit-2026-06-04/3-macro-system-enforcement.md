---
title: 501.3 - Can the macro system make strict engine separation structural?
role: designer
variant: Audit
date: 2026-06-04
slice: 3 (the CONCEPT slice)
topics: [triad-engine, strict-separation, schema-emission, triad-runtime, runner, triad_main, enforced-by-construction, record-2560, record-2561]
description: |
  Slice 3 of the strict-engine-separation audit. READ-ONLY: this slice
  produces a concept, it does not fix code. The question the psyche asked:
  can the schema-derived stack make record 2560's strict separation
  (SEMA owns ALL durable state, Nexus owns ALL decisions, Signal owns ALL
  communication; the daemon scaffolding owns NONE) STRUCTURALLY TRUE
  rather than a discipline an auditor must police? The answer is yes, and
  the lever is the runner — the ratified-but-unbuilt triad_main (records
  1574/1581). This slice reads how the engine traits are emitted today
  (schema-rust-next/src/lib.rs:2385-2491), what the daemon hand-writes
  around them (spirit/src/daemon.rs, engine.rs, transport.rs, config.rs,
  bin/main), and proposes the concrete runner shape that deletes every
  hand-written place a leak could live.
---

# 501.3 - Making record 2560 enforced-by-construction

## The constraint and the question

Record 2560 (VeryHigh): the triad engine separation is strict and absolute.
The SEMA engine owns ALL database/durable-state code; the Nexus engine owns
ALL decision-making; the Signal engine owns ALL communication. A component
daemon must contain NO database boilerplate, NO decision-making, and NO
communication code outside its respective engine. The Engine composer,
`daemon.rs`, `transport.rs`, `config.rs`, and `bin/main` are scaffolding —
they wire the engines together and run the loop, and must hold no
db/decision/comms LOGIC.

Slices 1 and 2 audit whether the *current* hand-written spirit pilot honours
that. This slice asks the deeper question the psyche posed: can the
schema-derived stack make the separation **structural rather than a discipline
an auditor must police?** Concretely — is there a shape in which there is no
*place* to put a leak, because the scaffolding that would host the leak is
generated and the component author only ever fills three trait impls?

The answer is yes. The mechanism already half-exists: the three engine traits
are emitted; the runner that would own the loop and the wiring is ratified
(records 1574/1581) but not built. This slice shows what the runner has to be
for record 2560 to become a compiler-and-codegen invariant.

## What the stack already enforces — the typed plane envelopes

The strong half is real today. The schema emits three engine traits with
typed-plane signatures, and the plane envelopes make cross-plane mis-wiring a
**type error**, not an audit finding.

The emission lives in `schema-rust-next/src/lib.rs:2385-2491`. The three
traits are gated on the schema declaring the matching root types — Signal
needs `Input`/`Output` roots plus `NexusWork`/`NexusAction`; Nexus needs
`NexusWork`/`NexusAction`; SEMA needs the four `Sema*` payload types
(`lib.rs:2370-2379`). When present, the emitter writes:

```rust
// SignalEngine — communication boundary (schema-rust-next/src/lib.rs:2408-2425)
fn triage_inner(&self, input: signal::Signal<signal::Input>) -> nexus::Nexus<nexus::Work>;
fn reply_inner(&self, output: nexus::Nexus<nexus::Action>) -> signal::Signal<signal::Output>;

// NexusEngine — decision boundary (schema-rust-next/src/lib.rs:2446)
fn decide(&mut self, input: nexus::Nexus<nexus::Work>) -> nexus::Nexus<nexus::Action>;

// SemaEngine — durable-state boundary (schema-rust-next/src/lib.rs:2474-2475)
fn apply_inner(&mut self, input: sema::Sema<sema::WriteInput>) -> sema::Sema<sema::WriteOutput>;
fn observe_inner(&self, input: sema::Sema<sema::ReadInput>) -> sema::Sema<sema::ReadOutput>;
```

Three structural properties already follow from this and are worth naming as
the *existing* enforcement floor:

1. **The plane envelope types are distinct nouns.** `signal::Signal<...>`,
   `nexus::Nexus<...>`, and `sema::Sema<...>` are different generic types.
   `spirit/src/lib.rs:14-20` ships a `compile_fail` doctest proving a
   `nexus_plane::Nexus<Work>` cannot be handed to `Store::apply`, which wants
   `sema::Sema<WriteInput>`. So a SEMA write CANNOT be invoked with a Nexus
   value — the engines cannot reach into each other's plane by accident.

2. **The only durable-state verbs are `apply`/`observe` on `SemaEngine`.**
   The only way to touch the redb store through the typed surface is the SEMA
   engine's two methods. Nexus holds the `Store` handle but reaches it only by
   calling `SemaEngine` methods.

3. **The only decision verb is `decide` on `NexusEngine`.** Signal's
   `triage_inner` and `reply_inner` are *translations* (Input→Work,
   Action→Output), not decisions; the decision (which is the choice of
   `NexusAction`) is `NexusEngine::decide` and nowhere else.

That is genuinely structural. The gap is NOT in the engine boundaries — it is
in everything *around* them.

## Where the separation is still discipline, not structure

The weak half: the engines are typed, but the code that runs them is
hand-written, and nothing forbids that code from holding logic. Every concern
record 2560 says belongs to an engine currently has a hand-written host where
it could leak:

- **The accept-loop is hand-written** — `Daemon::run`
  (`spirit/src/daemon.rs:152-173`) binds the socket, loops `listener.incoming()`,
  and for each stream calls `handle_stream`. This is communication code that
  lives OUTSIDE `SignalEngine`. It is currently thin, but it is a hand-written
  function: an author could add admission throttling, per-connection auth, or a
  retry policy here, and the type system would not complain. The socket-bind +
  accept-loop is communication LOGIC sitting in scaffolding.

- **The per-request composition is hand-written** — `Engine::handle`
  (`spirit/src/engine.rs:114-128`) and `SignalAccepted::process_with`
  (`engine.rs:257-277`) wire admit → triage → execute → reply by hand. This is
  the record-970 flow as a hand-authored sequence. Today it correctly only
  *calls* engine methods, but it is the natural home for a leak: an author who
  wants "validate twice" or "skip the ledger for reads" or "cache the last
  reply" writes it here, in the composer, not in an engine.

- **Admission lives partly in the composer, not purely in Signal** —
  `SignalActor::admit` (`engine.rs:174-190`) mints the origin route, issues the
  identifier, and validates. It is *on* `SignalActor` (good) but it is a
  hand-written inherent method, not a `SignalEngine` trait method, and
  `Engine::handle` calls it directly (`engine.rs:115`). The admission decision
  about whether to admit is communication policy; that it is reachable as an
  inherent method called from the composer means the composer participates in
  admission.

- **Transport frames are hand-written** — `transport.rs` owns length-prefix
  socket I/O (`transport.rs:84-100`). ARCHITECTURE says it "owns only
  length-prefix socket I/O ... not route enums, short-header matching, or rkyv
  encode/decode" (`spirit/ARCHITECTURE.md:150-151`) — but "only by discipline":
  it is a hand-written module, and the discipline that keeps wire-shape logic
  out of it is exactly the auditor discipline record 2560 wants to retire.

- **The daemon `main` is hand-written** — `bin/spirit-next-daemon.rs:1-8` is
  already minimal (`DaemonCommand::from_environment().run()`), but it is
  hand-written per component, and `DaemonCommand`/`Daemon` are hand-written
  nouns in the component crate (`daemon.rs:104-206`).

ARCHITECTURE itself names this as a known waypoint, not a finished state
(`spirit/ARCHITECTURE.md:88-93`): "`DaemonCommand` is the current programmatic
startup noun ... This is the small live step toward the **generated component
runner**: startup behavior belongs to library nouns, while domain decisions
belong to generated engine trait implementations." The intent is already to
move the loop and the wiring out of the component — record 2560 is the
sharpened version of that intent.

## The lever already ratified: the runner (records 1574/1581)

The fleet-state reports converge on a single missing noun. Designer 498.4 and
499 both call the runner "the single most-repeated missing noun"
(`reports/designer/498-persona-engine-state-2026-06-04/4-engine-vision-and-architecture.md:289-294`;
`reports/designer/499-Psyche-persona-engine-state-and-vision-2026-06-04.md:161-163`):

> The runner — `triad_main!` / the generic triad runner. Today every
> schema-derived daemon would hand-write the same socket-bind + accept-loop +
> engine-dispatch (`spirit/src/daemon.rs:152` `fn run`). The vision is a
> schema-emitted runner so the daemon `main` reduces to one call. Ratified to
> extract (records 1574/1581); NOT yet in triad-runtime (only trace lives
> there). (designer 498.4)

So the runner is **ratified to extract but unbuilt**. `triad-runtime` today
ships `trace`, `argument`, and `frame` (`triad-runtime/src/lib.rs:10-21`) — the
generic mechanics — but no runner. Its ARCHITECTURE explicitly reserves the
slot: "Future extraction waves may add **generic daemon command scaffolding,
signal transport**, and trace-aware test harnesses. Those move here only when a
second component would otherwise copy the same mechanics."
(`triad-runtime/ARCHITECTURE.md:55-58`).

The concept below is what that extraction must be SHAPED LIKE for record 2560 to
become enforced-by-construction rather than audited. The key move: the runner
is not just "extract the duplicated loop" — it is "make the loop the ONLY home
for communication mechanics, generate it, and leave the component author with
exactly three trait impls and zero scaffolding."

## The concept — the runner as the enforcement mechanism

The principle: **separation becomes structural when the only thing a component
author can write is the three engine trait impls, and everything that runs them
is generated or library-owned.** If there is no hand-written composer, no
hand-written loop, no hand-written transport, and no hand-written `main` in the
component crate, then there is no place for db/decision/comms logic to leak
outside its engine — because there is no hand-written code outside the engines
at all. Record 2560 stops being an audit target and becomes a property of the
project's file layout.

This is achieved with two pieces working together — a runtime trait in
`triad-runtime` (the *generic* mechanics, written once) and a schema-emitted
`triad_main` glue (the *per-component* wiring, generated by schema-rust-next).

### Piece 1 — the `TriadComponent` trait in triad-runtime (written once)

`triad-runtime` gains one trait that names the three engines and their owned
config/state, plus a blanket `serve` method that IS the loop. The component
never writes the loop; it names its three engine types and how to build them
from config.

```rust
// triad-runtime/src/runner.rs (proposed) — written ONCE, generic over engines
pub trait TriadComponent {
    type Configuration;            // the rkyv binary config (record 2560: config is scaffolding data, not logic)
    type Signal: SignalEngine;     // communication engine
    type Nexus:  NexusEngine;      // decision engine
    type Sema:   SemaEngine;       // durable-state engine

    // The ONLY thing the component author writes besides the three impls:
    // how to construct the engines from validated config. No logic — just
    // open the store at a path, default the signal actor, build the nexus
    // over the store.
    fn assemble(config: Self::Configuration)
        -> Result<TriadEngines<Self::Signal, Self::Nexus, Self::Sema>, AssembleError>;

    // serve() is a DEFAULT method — the component cannot override it. It IS
    // the socket-bind + accept-loop + lifecycle + per-request composition.
    // All communication mechanics live here, generic over the engines.
    fn serve(config: Self::Configuration) -> Result<(), RunnerError> {
        let engines = Self::assemble(config)?;
        engines.start()?;                              // SEMA->Nexus->Signal on_start
        let listener = SocketListener::bind(/* from config */)?;   // comms: lives in runtime
        for stream in listener.incoming() {
            let mut transport = LengthPrefixedCodec::new(stream?); // comms: lives in runtime
            let input = transport.read_input()?;                   // comms: lives in runtime
            // the record-970 composition, generic over the three engines:
            let work   = engines.signal.triage(input);             // SignalEngine
            let action = engines.nexus.execute(work);              // NexusEngine (owns decide)
            let output = engines.signal.reply(action);             // SignalEngine
            transport.write_output(output)?;                       // comms: lives in runtime
        }
        engines.stop()
    }
}
```

The decisive properties:

- `serve` is a **non-overridable default method** — there is no `fn serve` in
  the component crate to put a leak into. Today `Daemon::run`
  (`daemon.rs:152-173`) is a hand-written method ON the component crate; under
  this concept it moves to `triad-runtime` and the component crate has no loop.

- The accept-loop, the transport read/write, and the socket bind ALL live in
  `triad-runtime` — generic, component-agnostic, written once. That satisfies
  record 2560's "ALL communication in the Signal/runtime communication surface"
  by relocation: the component crate physically cannot contain comms code
  because the comms code is in a different crate it only calls into.

- The per-request composition (`triage` → `execute` → `reply`) is in `serve`,
  generic over the three engine traits. The component cannot insert a step
  between them. Today that composition is hand-written in
  `SignalAccepted::process_with` (`engine.rs:257-277`) where a step COULD be
  inserted; the runner deletes that authored seam.

- The SEMA invocation does not appear in `serve` at all — it is reached only
  through `NexusEngine::decide`/`execute` returning `CommandSemaWrite` actions,
  which the Nexus engine itself applies via `SemaEngine`. The runner never
  touches the store. That is record 2560's "ALL durable state in SEMA" made
  structural: the loop has no store handle.

### Piece 2 — `triad_main` emitted by schema-rust-next (generated per component)

The component author should not even write the `impl TriadComponent` boilerplate
that names the three engine types, nor the `bin/main`. schema-rust-next already
emits the three engine traits; it gains a sibling emission that wires them.

When a schema declares the full triad (the same condition that gates the engine
traits — `schema-rust-next/src/lib.rs:2370-2381`), the emitter writes:

```rust
// EMITTED by schema-rust-next into the component's generated module:
// the component noun whose three associated types the author fills by
// implementing SignalEngine/NexusEngine/SemaEngine on their runtime objects.
pub struct Component;

impl triad_runtime::TriadComponent for Component {
    type Configuration = Configuration;  // the emitted/typed config noun
    type Signal = SignalActor;           // author's type that impls SignalEngine
    type Nexus  = Nexus;                 // author's type that impls NexusEngine
    type Sema   = Store;                 // author's type that impls SemaEngine
    fn assemble(config: Configuration) -> Result<_, _> { /* emitted from schema */ }
}

// And the daemon main reduces to one generated call — emitted into bin:
fn main() {
    if let Err(error) = <Component as triad_runtime::TriadComponent>::serve(
        triad_runtime::ComponentCommand::from_environment().configuration()?
    ) {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
```

`triad-runtime` already owns `ComponentCommand` / `ComponentArgument` for the
single-argument rule (`triad-runtime/src/lib.rs:14-16`) — the argument-parsing
half is built; this concept connects it to the runner.

### What the component author is allowed to write — the whole surface

After both pieces land, the ENTIRE hand-written surface of a triad component is:

1. `impl SignalEngine for <their signal actor>` — `triage_inner` + `reply_inner`
   (translation only) plus optional admission policy. Communication logic, in
   the communication engine.
2. `impl NexusEngine for <their nexus>` — `decide` (the decision loop). Decision
   logic, in the decision engine.
3. `impl SemaEngine for <their store>` — `apply_inner` + `observe_inner`. Durable
   redb logic, in the durable-state engine.
4. The three runtime nouns those impls hang on (their `SignalActor`, `Nexus`,
   `Store` — data-bearing types) and the domain algorithms as methods on them.

There is NO hand-written `main`, NO hand-written `Daemon`/`DaemonCommand`, NO
hand-written accept-loop, NO hand-written transport, NO hand-written composer in
the component crate. `daemon.rs`, `transport.rs`, and `bin/main` as they exist
in spirit today (`spirit/src/daemon.rs`, `transport.rs`, `bin/spirit-next-daemon.rs`)
disappear into `triad-runtime` + the generated `triad_main`. `config.rs` becomes
a schema-emitted typed config noun (it is already pure rkyv data with no logic —
`config.rs:1-106` — so it is the easiest to generate).

This is the structural answer to record 2560: **the auditor's job (slices 1-2)
is to find db/decision/comms logic outside its engine; under the runner concept
there is no hand-written code outside the engines for that logic to live in, so
the audit becomes vacuous by construction.** The separation is enforced by the
file layout the codegen produces, not by a human re-reading the composer.

## Why this is enforced-by-construction, not just convention

Three independent structural locks, each a compiler or codegen fact rather than
a discipline:

1. **Type lock (already real).** The plane envelope types make cross-engine
   calls a type error (`spirit/src/lib.rs:14-20` `compile_fail`). An engine
   cannot invoke another engine's plane.

2. **Layout lock (the runner adds this).** The loop, transport, and composer
   physically live in `triad-runtime`, a different crate. The component crate
   has no module in which to write comms/loop logic. You cannot leak into a file
   that does not exist in your crate.

3. **Codegen lock (the `triad_main` emission adds this).** The `impl
   TriadComponent` wiring and `bin/main` are generated by schema-rust-next, not
   hand-written. Regenerating overwrites them, so a hand-edited leak in the glue
   is non-durable — the next emit erases it. This is the same property the stack
   already relies on for the wire types: `build.rs` verifies the generated module
   is fresh (`spirit/src/lib.rs:6-7`), so a hand-edit drifts and fails the build.

The combination means a would-be leak has nowhere to live: not in a cross-plane
call (type error), not in a component-crate scaffolding file (does not exist),
and not in the generated glue (overwritten + freshness-checked). That is the
precise sense in which record 2560 becomes structural.

## What is genuinely a design judgment, not yet decided

Two questions the runner concept surfaces that the psyche should rule on, rather
than have me force:

- **Where does admission policy live — in the runner or in `SignalEngine`?**
  Today `SignalActor::admit` (`engine.rs:174-190`) mints route + identifier +
  validates as an inherent method the composer calls. Record 2560 says ALL
  communication is in the Signal engine. The clean reading is that admission
  becomes a `SignalEngine` trait method (`admit`/`on_admit`) that the runner's
  `serve` calls, so route-minting and validation are Signal-engine concerns, not
  runner concerns. But identifier/route minting is arguably generic monotonic
  bookkeeping the runner could own. This is the one seam where "comms" plausibly
  splits between engine and runtime, and it wants an explicit ruling.

- **Does the runner own concurrency, or does the schema?** `Engine::handle`
  takes `&self` and `process_with` holds `&mut Nexus` as the single-flight guard
  (`engine.rs:257`, ARCHITECTURE:177-179). A generic `serve` loop is sequential
  by construction (one stream at a time), which is the strongest possible
  single-flight guarantee but also the weakest throughput. Whether the runner
  stays single-flight or grows a generated mailbox/actor surface is the
  "full actor mailbox ... remains future work" question ARCHITECTURE flags
  (`spirit/ARCHITECTURE.md:85-86`). The runner concept is correct either way,
  but the concurrency model is a real design decision, not a mechanical extract.

## Verification note

This slice is the CONCEPT slice and is READ-ONLY by instruction: it produces a
concept and proposes no code change, so there is no fix to cargo-verify. The
concept is grounded in read-only inspection of the live source
(`schema-rust-next/src/lib.rs`, `spirit/src/{engine,daemon,transport,config,lib}.rs`,
`spirit/src/bin/spirit-next-daemon.rs`, `triad-runtime/src/lib.rs` +
`ARCHITECTURE.md`) and the ratifying reports (designer 498.4, 499, 500.3) which
cite records 1574/1581. No branch was created and nothing was written outside
this entry file.
