---
title: 516.4 — How schema EMITS AN ENGINE (SignalEngine / NexusEngine / SemaEngine)
role: designer
variant: Psyche
date: 2026-06-04
topics: [schema-rust-next, spirit, RustEmissionTarget, runtime_planes, SignalEngine, NexusEngine, SemaEngine, three-plane-split, component-triad, code-generation]
description: |
  Mechanism report #4 of the system deep audit. Explains how a schema
  emits an engine TRAIT rather than just data types: the
  RustEmissionTarget enum, the runtime_planes() projection, and the
  emitter gates that turn a plane flag into `pub trait SignalEngine`.
  Shows the daemon's three plane schemas (signal/nexus/sema) emitting
  three engine traits, each implemented by exactly one actor
  (SignalActor / Nexus / Store). Every claim is backed by a command
  actually run, with verbatim output. Verifies the SignalRuntime
  resolution live (now carried by report 527, the runner/SignalRuntime
  Refresh) — the signal.schema carries zero concrete Nexus types yet
  still emits an (abstract) SignalEngine.
---

# 516.4 — How schema EMITS AN ENGINE

## The thesis in one sentence

A schema does not merely emit *data types* (the wire vocabulary); when
its `RustEmissionTarget` carries a runtime plane, the generator also
emits a **behaviour contract** — a `pub trait` with default-method
bodies that own the plane's lifecycle and tracing, plus a small set of
`fn ..._inner(...)` holes the daemon must fill. The daemon supplies the
plane's *policy* by writing one `impl` block per trait. The three planes
of a component daemon (`signal`, `nexus`, `sema`) therefore emit three
engine traits, each implemented by exactly one actor.

This is the load-bearing move of the schema-derived stack: the recursive
runner loop, the trace-hook wiring, the budget-exhaustion reply framing,
and the Signal→Nexus→Sema handoff sequencing all live in *generated*
default method bodies. The daemon author cannot get the orchestration
wrong because they never write it — they write only the leaf decisions.

## 1. The five emission targets and `runtime_planes()`

`RustEmissionTarget` is the dial. It is a five-variant enum in
`schema-rust-next/src/lib.rs`. Read verbatim (lines 293-321):

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum RustEmissionTarget {
    /// External signal or meta-signal wire vocabulary plus codecs only.
    WireContract,
    /// Bootstrap all-in-one runtime emission for unsplit schemas.
    ComponentRuntime,
    /// Daemon-side Signal plane runtime support over signal roots.
    SignalRuntime,
    /// Daemon-side Nexus plane runtime support only.
    NexusRuntime,
    /// Daemon-side SEMA plane runtime support only.
    SemaRuntime,
}

impl RustEmissionTarget {
    fn emits_runtime_support(self) -> bool {
        self.runtime_planes().emits_any()
    }

    fn runtime_planes(self) -> RuntimePlaneSet {
        match self {
            Self::WireContract => RuntimePlaneSet::none(),
            Self::ComponentRuntime => RuntimePlaneSet::all(),
            Self::SignalRuntime => RuntimePlaneSet::signal_only(),
            Self::NexusRuntime => RuntimePlaneSet::nexus_only(),
            Self::SemaRuntime => RuntimePlaneSet::sema_only(),
        }
    }
}
```

`runtime_planes()` projects each target onto a three-bit struct
`RuntimePlaneSet { signal, nexus, sema }`. The constructors are
exhaustive and orthogonal (same file, lines 330-369): `none()` is all
false; `all()` is all true; `signal_only()` / `nexus_only()` /
`sema_only()` each set exactly one bit. The whole rest of the emitter
asks only three questions of this struct — `emits_signal()`,
`emits_nexus()`, `emits_sema()` (lines 371-381) — never the target
directly (with one named exception, §5). That indirection is the design:
*the emitter is plane-driven, not target-driven*, so a new target is
just a new row in the `match` above.

The mapping the task asks to confirm, verified against the verbatim
source above:

| Target | `runtime_planes()` | signal | nexus | sema |
|---|---|---|---|---|
| `WireContract` | `none()` | false | false | false |
| `ComponentRuntime` | `all()` | true | true | true |
| `SignalRuntime` | `signal_only()` | true | false | false |
| `NexusRuntime` | `nexus_only()` | false | true | false |
| `SemaRuntime` | `sema_only()` | false | false | true |

## 2. A daemon picks a target per plane in its build.rs

The target is chosen *per schema file* through `ModuleEmission`
constructors. spirit's `build.rs` is the canonical caller. Verbatim
(`spirit/build.rs`, lines 31-39):

```rust
let plan = GenerationPlan::new(&self.crate_root, "spirit", "0.1.0")
    .with_module(ModuleEmission::signal_runtime_module("signal"))
    .with_module(ModuleEmission::nexus_runtime())
    .with_module(ModuleEmission::sema_runtime());
GenerationDriver::new(plan)
    .generate()
    .expect("generate spirit schema artifacts")
    .write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")
    .expect("checked-in spirit schema artifacts are fresh");
```

Each `ModuleEmission` constructor binds a target. From
`schema-rust-next/src/build.rs` (lines 133-159):

```rust
pub fn nexus_runtime() -> Self {
    Self::new(
        "nexus",
        RustEmissionOptions::feature_gated_nota("nota-text")
            .with_target(RustEmissionTarget::NexusRuntime),
    )
}

pub fn signal_runtime_module(module: impl Into<String>) -> Self {
    Self::new(
        module,
        RustEmissionOptions::feature_gated_nota("nota-text")
            .with_target(RustEmissionTarget::SignalRuntime),
    )
}

pub fn sema_runtime() -> Self {
    Self::new(
        "sema",
        RustEmissionOptions::feature_gated_nota("nota-text")
            .with_target(RustEmissionTarget::SemaRuntime),
    )
}
```

So spirit's three plane schemas map to three targets:

- `schema/signal.schema` → `SignalRuntime` → emits `signal.rs` carrying `pub trait SignalEngine`
- `schema/nexus.schema` → `NexusRuntime` → emits `nexus.rs` carrying `pub trait NexusEngine`
- `schema/sema.schema` → `SemaRuntime` → emits `sema.rs` carrying `pub trait SemaEngine`

The build is a **write-or-check**: with `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1`
the generator overwrites the checked-in `src/schema/*.rs`; without it, it
regenerates in memory and *asserts the checked-in files are byte-identical*,
panicking otherwise. That is what makes the generated files trustworthy to
read — CI fails if they drift from the schema.

Schema files present, confirmed by directory listing
(`ls /git/github.com/LiGoldragon/spirit/schema/`):

```
nexus.asschema
nexus.schema
sema.asschema
sema.schema
signal.asschema
signal.schema
```

and the generated outputs (`ls /git/github.com/LiGoldragon/spirit/src/schema/`):

```
nexus.rs
sema.rs
signal.rs
```

## 3. Live build proof — the three engines compile

A fresh compile of spirit (forced by touching `src/engine.rs`), run in
`/git/github.com/LiGoldragon/spirit`:

```
$ cargo check --message-format=short
   Compiling spirit v0.1.0 (/git/github.com/LiGoldragon/spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.82s
```

(Command: `~/.nix-profile/bin/cargo check --message-format=short`,
cwd `/git/github.com/LiGoldragon/spirit`. The `Compiling spirit v0.1.0`
line confirms this is a genuine recompile of the crate, not a cache hit.)

And the **freshness check** path — re-running the build with `build.rs`
touched and `SPIRIT_UPDATE_SCHEMA_ARTIFACTS` *unset*, which re-invokes
the generator and asserts the checked-in `src/schema/*.rs` match:

```
$ cargo check --message-format=short
   Compiling spirit v0.1.0 (/git/github.com/LiGoldragon/spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.61s
```

This `Finished` (no panic) is the proof that the checked-in generated
files I read below are exactly what the generator emits from the schemas
*today* — the `.expect("checked-in spirit schema artifacts are fresh")`
in `build.rs` did not fire.

## 4. From plane flag to `pub trait` — the emitter gate

The actual `pub trait ...Engine {` token text is written by the emitter,
gated by a per-plane boolean. In `schema-rust-next/src/lib.rs`, the gates
are computed once (lines 3043-3049):

```rust
let emits_signal_engine = self.emits_signal_engine_support(declarations, root_enums);
let emits_concrete_signal_engine =
    emits_signal_engine && self.emits_concrete_signal_engine_support(declarations);
let emits_nexus_engine = self.emits_nexus_engine_support(declarations);
...
let emits_sema_engine = emits_sema_apply || emits_sema_observe;
```

and each gate guards a literal `self.line("pub trait ...Engine {")` block.
The three guards, verbatim:

```rust
// lib.rs:3064-3065
if emits_signal_engine {
    self.line("pub trait SignalEngine {");
// lib.rs:3134-3135
if emits_nexus_engine {
    self.line("pub trait NexusEngine {");
// lib.rs:3218-3219
if emits_sema_engine {
    self.line("pub trait SemaEngine {");
```

The gates resolve back to `runtime_planes()`. `emits_nexus_engine_support`
(lib.rs:2892-2896) is the clean case:

```rust
fn emits_nexus_engine_support(&self, declarations: &[RustDeclaration]) -> bool {
    self.runtime_planes().emits_nexus()
        && self.has_type(declarations, "NexusWork")
        && self.has_type(declarations, "NexusAction")
}
```

So: `NexusRuntime` → `runtime_planes().emits_nexus() == true` → and
because `nexus.schema` *does* declare the concrete `NexusWork` /
`NexusAction` roots, the trait is emitted. The `sema` gate is
analogous, keyed on `emits_sema()` plus the presence of write/read roots.

This is the complete causal chain the task asked to trace:

```
ModuleEmission::nexus_runtime()
  → RustEmissionTarget::NexusRuntime
    → runtime_planes() == nexus_only()  (RuntimePlaneSet{ nexus: true })
      → emits_nexus() == true
        → emits_nexus_engine_support() == true
          → self.line("pub trait NexusEngine {")  EMITTED into nexus.rs
```

## 5. The SignalRuntime resolution — verified live (report 527)

The SignalRuntime resolution (carried by report 527, the runner/SignalRuntime
Refresh) records that the three-plane split originally emitted
*no* `SignalEngine`, because the daemon's `signal.schema` is the
*runtime* signal schema and does **not** carry the concrete `NexusWork`
/ `NexusAction` types — those live in `nexus.schema`. The fix was the
fifth target, `SignalRuntime`, plus a special-case in the signal gate.
I verified this live rather than taking the resolution on faith.

The signal gate, `emits_signal_engine_support` (lib.rs:2870-2884):

```rust
fn emits_signal_engine_support(
    &self,
    declarations: &[RustDeclaration],
    root_enums: &[RustEnum],
) -> bool {
    if !self.has_root_enum(root_enums, "Input") || !self.has_root_enum(root_enums, "Output") {
        return false;
    }
    if matches!(self.target, RustEmissionTarget::SignalRuntime) {
        return true;
    }
    self.runtime_planes().emits_signal()
        && self.has_type(declarations, "NexusWork")
        && self.has_type(declarations, "NexusAction")
}
```

Line 2878 is **the one place the emitter inspects `self.target`
directly** rather than going through `runtime_planes()`. For
`SignalRuntime` it short-circuits to `true` even though the signal
schema has no concrete Nexus types. The fall-through branch (the
`ComponentRuntime` all-in-one case) still requires the concrete types,
because there the signal and nexus planes share one schema.

Live confirmation, run in `/git/github.com/LiGoldragon/spirit`:

```
$ grep -c "NexusWork\|NexusAction" schema/signal.schema
0
$ grep -n "type NexusInput;\|type NexusOutput;" src/schema/signal.rs
1157:    type NexusInput;
1158:    type NexusOutput;
```

`signal.schema` mentions `NexusWork`/`NexusAction` **zero** times, yet
the generated `SignalEngine` *is* emitted — and emitted in its
**abstract** form: instead of naming concrete Nexus types it carries two
associated types, `type NexusInput` / `type NexusOutput`. That is the
`!emits_concrete_signal_engine` branch (lib.rs:3066-3070). The daemon
binds those associated types to the real Nexus types in its `impl`
(§6.1). This is exactly report 515's mechanism, observed in the live
artifacts.

## 6. The three emitted traits and their single implementor

Each plane schema emits one engine trait into `src/schema/<plane>.rs`,
and the daemon supplies exactly one `impl`. The pattern is identical
across planes: the trait carries default-bodied lifecycle hooks
(`on_start`/`on_stop`), default-bodied trace fan-out
(`trace_..._activation` + per-event helpers), and a public
default-bodied entry method that wraps a required `..._inner` /
required leaf method. The daemon overrides only the leaves.

### 6.1 SignalEngine — implemented by `SignalActor`

Generated trait, `spirit/src/schema/signal.rs` (lines 1156-1195):

```rust
pub trait SignalEngine {
    type NexusInput;
    type NexusOutput;

    fn on_start(&mut self) -> Result<(), ActorStartFailure> {
        Ok(())
    }
    fn on_stop(&mut self) -> Result<(), ActorStopFailure> {
        Ok(())
    }

    fn trace_signal_activation(&self, _object_name: SignalObjectName) {}
    fn trace_signal_admitted(&self) {
        self.trace_signal_activation(SignalObjectName::Admitted);
    }
    fn trace_signal_rejected(&self) {
        self.trace_signal_activation(SignalObjectName::Rejected);
    }
    fn trace_signal_triaged(&self) {
        self.trace_signal_activation(SignalObjectName::Triaged);
    }
    fn trace_signal_replied(&self) {
        self.trace_signal_activation(SignalObjectName::Replied);
    }

    fn triage_inner(&self, input: signal::Signal<signal::Input>) -> Self::NexusInput;
    fn reply_inner(&self, output: Self::NexusOutput) -> signal::Signal<signal::Output>;

    fn triage(&self, input: signal::Signal<signal::Input>) -> Self::NexusInput {
        let output = self.triage_inner(input);
        self.trace_signal_triaged();
        output
    }

    fn reply(&self, output: Self::NexusOutput) -> signal::Signal<signal::Output> {
        let signal_output = self.reply_inner(output);
        self.trace_signal_replied();
        signal_output
    }
}
```

Note the shape: `triage`/`reply` are the public, *generated*, trace-wired
methods; `triage_inner`/`reply_inner` are the two required holes. The
daemon implements only the holes (and binds the associated types). From
`spirit/src/engine.rs` (lines 209-245):

```rust
impl SignalEngine for SignalActor {
    type NexusInput = nexus_schema::nexus::Nexus<NexusWork>;
    type NexusOutput = nexus_schema::nexus::Nexus<NexusAction>;

    fn on_start(&mut self) -> Result<(), ActorStartFailure> {
        #[cfg(feature = "testing-trace")]
        self.trace_signal_activation(SignalObjectName::Started);
        Ok(())
    }

    fn on_stop(&mut self) -> Result<(), ActorStopFailure> {
        #[cfg(feature = "testing-trace")]
        self.trace_signal_activation(SignalObjectName::Stopped);
        Ok(())
    }

    #[cfg(feature = "testing-trace")]
    fn trace_signal_activation(&self, object_name: SignalObjectName) {
        self.trace_log
            .record(TraceEvent::new(ObjectName::Signal(object_name)));
    }

    fn triage_inner(
        &self,
        input: signal_schema::signal::Signal<Input>,
    ) -> nexus_schema::nexus::Nexus<NexusWork> {
        let origin_route = input.origin_route();
        NexusWork::signal_arrived(input.into_root()).with_origin_route(origin_route.into())
    }

    fn reply_inner(
        &self,
        output: nexus_schema::nexus::Nexus<NexusAction>,
    ) -> signal_schema::signal::Signal<Output> {
        output.into_signal_output()
    }
}
```

The two associated types from the abstract trait (`NexusInput` /
`NexusOutput`) are bound here to the *cross-schema* concrete types
`nexus_schema::nexus::Nexus<NexusWork>` and `...<NexusAction>` — this is
the literal seam between the signal plane and the nexus plane, made
type-safe by the associated-type binding rather than a generated coupling.

### 6.2 NexusEngine — implemented by `Nexus`

Generated trait, `spirit/src/schema/nexus.rs` (lines 712-753). The
required leaves are the decision and the SEMA/effect dispatch hooks; the
default `execute` owns the recursive runner loop:

```rust
pub trait NexusEngine {
    fn on_start(&mut self) -> Result<(), ActorStartFailure> {
        Ok(())
    }
    fn on_stop(&mut self) -> Result<(), ActorStopFailure> {
        Ok(())
    }

    fn trace_nexus_activation(&self, _object_name: NexusObjectName) {}
    fn trace_nexus_entered(&self) {
        self.trace_nexus_activation(NexusObjectName::Entered);
    }
    fn trace_nexus_decided(&self) {
        self.trace_nexus_activation(NexusObjectName::Decided);
    }

    fn continuation_limit(&self) -> triad_runtime::ContinuationLimit {
        triad_runtime::ContinuationLimit::default()
    }

    fn apply_sema_write(&mut self, origin_route: OriginRoute, input: CommandSemaWrite) -> SemaWriteCompleted;
    fn observe_sema_read(&self, origin_route: OriginRoute, input: CommandSemaRead) -> SemaReadCompleted;
    fn run_effect(&mut self, input: CommandEffect) -> EffectCompleted;
    fn budget_exhausted_reply(&self, exhausted: triad_runtime::ContinuationExhausted) -> ReplyToSignal;

    fn decide(&mut self, input: nexus::Nexus<nexus::Work>) -> nexus::Nexus<nexus::Action>;

    fn execute(&mut self, input: nexus::Nexus<nexus::Work>) -> nexus::Nexus<nexus::Action>
    where
        Self: Sized,
    {
        self.trace_nexus_entered();
        let origin_route = input.origin_route();
        let first_work = input.into_root();
        let runner = triad_runtime::Runner::new(self.continuation_limit());
        let mut runner_adapter = NexusRunnerAdapter::new(self, origin_route);
        let reply = runner.drive(&mut runner_adapter, first_work);
        let output = NexusAction::reply_to_signal(reply).with_origin_route(origin_route);
        self.trace_nexus_decided();
        output
    }
}
```

`execute` is the most important *generated* body in the stack: the
daemon never writes the runner loop, the continuation budget plumbing, or
the reply framing — it writes only `decide` (one step) plus the four
dispatch leaves. The daemon impl, `spirit/src/nexus.rs` (lines 153-217):

```rust
impl NexusEngine for Nexus {
    fn on_start(&mut self) -> Result<(), NexusActorStartFailure> {
        SemaEngine::on_start(&mut self.store)?;
        #[cfg(feature = "testing-trace")]
        self.trace_nexus_activation(NexusObjectName::Started);
        Ok(())
    }

    fn on_stop(&mut self) -> Result<(), NexusActorStopFailure> {
        #[cfg(feature = "testing-trace")]
        self.trace_nexus_activation(NexusObjectName::Stopped);
        SemaEngine::on_stop(&mut self.store)?;
        Ok(())
    }
    ...
    fn decide(
        &mut self,
        input: nexus_schema::nexus::Nexus<nexus_schema::nexus::Work>,
    ) -> nexus_schema::nexus::Nexus<nexus_schema::nexus::Action> {
        let origin_route = input.origin_route();
        self.step_decide(input.into_root())
            .with_origin_route(origin_route)
    }

    fn apply_sema_write(
        &mut self,
        origin_route: nexus_schema::OriginRoute,
        input: SemaWriteInput,
    ) -> SemaWriteOutput {
        SemaEngine::apply(
            &mut self.store,
            input.with_origin_route(origin_route.into()),
        )
        .into_root()
    }

    fn observe_sema_read(
        &self,
        origin_route: nexus_schema::OriginRoute,
        input: SemaReadInput,
    ) -> SemaReadOutput {
        SemaEngine::observe(&self.store, input.with_origin_route(origin_route.into())).into_root()
    }

    fn run_effect(&mut self, input: NexusEffectCommand) -> NexusEffectResult {
        self.apply_effect(input)
    }

    fn budget_exhausted_reply(&self, exhausted: ContinuationExhausted) -> Output {
        Output::error(ErrorReport { ... })
    }
}
```

Observe the *nesting of engines*: `Nexus::apply_sema_write` and
`observe_sema_read` call straight into `SemaEngine::apply` /
`SemaEngine::observe` on `self.store`. The Nexus engine is the only
caller of the Sema engine — the SEMA plane is reached *through* Nexus,
never directly from Signal. And `Nexus::on_start`/`on_stop` chain to
`SemaEngine::on_start`/`on_stop`, so the lifecycle cascades down the
plane stack.

### 6.3 SemaEngine — implemented by `Store`

Generated trait, `spirit/src/schema/sema.rs` (lines 692-722):

```rust
pub trait SemaEngine {
    fn on_start(&mut self) -> Result<(), ActorStartFailure> {
        Ok(())
    }
    fn on_stop(&mut self) -> Result<(), ActorStopFailure> {
        Ok(())
    }

    fn trace_sema_activation(&self, _object_name: SemaObjectName) {}
    fn trace_sema_write_applied(&self) {
        self.trace_sema_activation(SemaObjectName::WriteApplied);
    }
    fn trace_sema_read_observed(&self) {
        self.trace_sema_activation(SemaObjectName::ReadObserved);
    }

    fn apply_inner(&mut self, input: sema::Sema<sema::WriteInput>) -> sema::Sema<sema::WriteOutput>;
    fn observe_inner(&self, input: sema::Sema<sema::ReadInput>) -> sema::Sema<sema::ReadOutput>;

    fn apply(&mut self, input: sema::Sema<sema::WriteInput>) -> sema::Sema<sema::WriteOutput> {
        let output = self.apply_inner(input);
        self.trace_sema_write_applied();
        output
    }

    fn observe(&self, input: sema::Sema<sema::ReadInput>) -> sema::Sema<sema::ReadOutput> {
        let output = self.observe_inner(input);
        self.trace_sema_read_observed();
        output
    }
}
```

Same shape as SignalEngine: public trace-wired `apply`/`observe`,
required leaves `apply_inner`/`observe_inner`. The daemon impl,
`spirit/src/store.rs` (lines 51-...), fills the write leaf with the
actual durable-store mutation:

```rust
impl SemaEngine for Store {
    fn on_start(&mut self) -> Result<(), SemaActorStartFailure> {
        #[cfg(feature = "testing-trace")]
        self.trace_sema_activation(SemaObjectName::Started);
        Ok(())
    }
    ...
    fn apply_inner(
        &mut self,
        command: sema_schema::sema::Sema<sema_schema::sema::WriteInput>,
    ) -> sema_schema::sema::Sema<sema_schema::sema::WriteOutput> {
        let origin_route = command.origin_route();
        let output = match command.into_root() {
            SemaWriteInput::Record(record) => match self.record(record) {
                Ok(identifier) => SemaWriteOutput::recorded(SemaReceipt {
                    record_identifier: identifier,
                    database_marker: self.database_marker(),
                }),
                Err(error) => SemaWriteOutput::missed(ErrorReport { ... }),
            },
            SemaWriteInput::Remove(remove) => { ... }
        };
        ...
    }
}
```

`Store::apply_inner` is where the schema-derived stack finally touches
the durable database — every layer above it (`SignalEngine::triage` →
`NexusEngine::execute`/`decide` → `NexusEngine::apply_sema_write` →
`SemaEngine::apply`) is generated orchestration converging on this one
leaf.

## 7. How the daemon composes the three engines

The three traits are not independent islands; the daemon's `Engine`
struct owns the actors and runs the generated entry methods in sequence.
`spirit/src/engine.rs` (lines 25-31):

```rust
#[derive(Debug)]
pub struct Engine {
    signal_actor: SignalActor,
    nexus: Mutex<Nexus>,
    #[cfg(feature = "testing-trace")]
    trace_log: TraceLog,
}
```

And the pipeline that composes the three plane engines, `engine.rs`
(lines 282-285):

```rust
let nexus_input = signal_engine.triage(self.input);
let origin_route = nexus_input.origin_route();
let nexus_output = NexusEngine::execute(nexus, nexus_input);
let signal_output = signal_engine.reply(nexus_output);
```

This is the whole request lifecycle in four lines, and every method
called is a *generated* default body:
`SignalEngine::triage` (trace-wired, calls daemon's `triage_inner`) →
`NexusEngine::execute` (the generated runner loop, which calls daemon's
`decide` + `apply_sema_write`/`observe_sema_read` → `SemaEngine::apply`/
`observe`) → `SignalEngine::reply` (trace-wired, calls daemon's
`reply_inner`). The daemon wrote none of this orchestration — it wrote
five leaf methods total across the three impls plus the bound associated
types.

## 8. What this mechanism is, stated plainly

"Schema emits an engine" means: a `RustEmissionTarget` carrying a runtime
plane causes the generator to emit a `pub trait <Plane>Engine` whose
default method bodies encode the plane's *invariant orchestration*
(lifecycle cascade, trace fan-out, recursive runner, reply framing,
budget exhaustion) and whose required methods (`*_inner`, `decide`, the
dispatch leaves) are the *variant policy* holes the daemon fills with one
`impl` per trait. A three-plane daemon emits three engine traits, each
with exactly one implementor — `SignalActor`, `Nexus`, `Store`. The
boundary between generated-mechanism and hand-written-policy is the trait
boundary itself: default bodies are the schema's, required methods are
the daemon's.

## 9. Commands run (for re-verification)

Every claim above traces to one of these, all run during this audit:

1. `~/.nix-profile/bin/cargo check --message-format=short` in
   `/git/github.com/LiGoldragon/spirit` (after `touch src/engine.rs`) →
   `Compiling spirit v0.1.0 ... Finished dev profile ... in 1.82s`. Proves
   the three engine impls + generated traits compile together.
2. `~/.nix-profile/bin/cargo check --message-format=short` in
   `/git/github.com/LiGoldragon/spirit` (after `touch build.rs`,
   `SPIRIT_UPDATE_SCHEMA_ARTIFACTS` unset) → `Finished ... in 0.61s` with
   no panic. Proves the checked-in `src/schema/*.rs` are byte-fresh vs the
   generator, so reading them is reading what the schema emits.
3. `grep -c "NexusWork\|NexusAction" schema/signal.schema` →
   `0`; `grep -n "type NexusInput;\|type NexusOutput;" src/schema/signal.rs`
   → lines 1157-1158. Proves report 515's SignalRuntime resolution live:
   signal schema has no concrete Nexus types yet emits an abstract
   SignalEngine.
4. `grep -n "impl SignalEngine\|impl NexusEngine\|impl SemaEngine" src/engine.rs src/nexus.rs src/store.rs`
   → `engine.rs:209 impl SignalEngine for SignalActor`,
   `nexus.rs:153 impl NexusEngine for Nexus`,
   `store.rs:51 impl SemaEngine for Store`. Proves one implementor per
   engine.
5. `grep -n "pub trait SignalEngine\|pub trait NexusEngine\|pub trait SemaEngine" src/schema/*.rs`
   → `signal.rs:1156`, `nexus.rs:712`, `sema.rs:692`. Proves three emitted
   traits, one per plane file.

## 10. Naming note for the verifier

The task brief named the implementors `SignalActor` / `NexusRuntime` /
`SemaRuntime` actors, and the impl files as
"engine.rs / nexus.rs / store.rs". The live source confirms the files
exactly (`engine.rs`, `nexus.rs`, `store.rs`) and confirms the
*implementing types* are `SignalActor`, `Nexus`, and `Store`
respectively (not literally `NexusActor`/`SemaActor` — the daemon names
its nexus actor `Nexus` and its sema actor `Store`). `NexusRuntime` /
`SemaRuntime` are the *emission-target* names, not the actor names; the
actor that implements `NexusEngine` is `Nexus`, and the actor that
implements `SemaEngine` is `Store`. This is a naming clarification, not a
discrepancy in the mechanism.
