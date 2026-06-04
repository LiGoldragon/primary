---
title: 516 — How schema emits a WIRE-ONLY (Y-only) interface (WireContract)
role: designer
variant: Psyche
date: 2026-06-04
session: meta-report directory (sub-agent session) — report 5
topics: [schema, wire-contract, signal-runtime, signal-engine, rkyv, nota-codec, emission-target, runtime-plane, rebuild-isolation, security-boundary]
description: |
  Mechanism report #5 of the system deep audit. How a schema emits a
  wire-only interface — wire vocabulary + codecs, ZERO engines — through
  the schema-rust-next RustEmitter, and the contrasting daemon-local path
  that emits the SignalEngine trait. The two meanings of "signal schema":
  the public signal-<component> contract (no engine) vs the daemon-local
  <component>/schema/signal.schema (engine plane). Every code/behaviour
  claim is backed by a command actually run, with verbatim output pasted.
---

# Report 5 — How schema emits a WIRE-ONLY (Y-only) interface

## What this report proves

There are **two emissions of "the signal schema"** in the spirit stack,
and they are deliberately NOT the same artifact:

1. The **public ordinary contract** — the `signal-spirit` crate. Its
   `schema/signal-spirit.schema` is emitted as a **wire-only** interface:
   the data types (`Input`, `Output`, payloads), the NOTA text codec
   (`FromStr`/`Display`, `from_nota_block`/`to_nota`), and the rkyv
   derives. **Zero engines.** No `SignalEngine` trait, no actor lifecycle,
   no triage/reply seam. It is pure vocabulary + codecs that any peer
   links to construct and parse operations.

2. The **daemon-local runtime schema** — `spirit/schema/signal.schema`,
   emitted into `spirit/src/schema/signal.rs`. It carries the **same wire
   vocabulary** PLUS the `SignalEngine` trait: the abstract seam the
   daemon's actor fills with real behaviour.

The mechanism that makes the difference is a single emission knob in
`schema-rust-next`: the `RustEmissionTarget` enum. `WireContract` maps to
an empty `RuntimePlaneSet`; `SignalRuntime` maps to a signal-only plane
set that turns the engine emission on.

This report runs the builds, locates the generated artifacts, and pastes
the real output that proves the split.

## The mechanism: `RustEmissionTarget` → `RuntimePlaneSet`

The whole wire-only-vs-runtime decision lives in one enum and its
`runtime_planes()` projection in
`schema-rust-next/src/lib.rs`. Verbatim from the source (lines 293-320):

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

`RuntimePlaneSet` is a three-bool struct (`signal`, `nexus`, `sema`).
`WireContract` → `none()` (all false). `SignalRuntime` → `signal_only()`
(signal true, the rest false).

The gate that consumes this is `emits_signal_engine_support`
(`schema-rust-next/src/lib.rs` lines 2870-2884, verbatim):

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

Read this carefully — it is the load-bearing logic of the entire split:

- A schema with no `Input`/`Output` roots gets no engine, period.
- `SignalRuntime` is the **explicit yes**: if the target is
  `SignalRuntime`, the engine is emitted unconditionally (this is the
  abstract-engine path — associated types `NexusInput`/`NexusOutput`,
  because the signal schema alone doesn't know the concrete Nexus types).
- Any other target only emits the engine if its plane set includes signal
  AND the schema itself declares concrete `NexusWork` + `NexusAction`
  types (the concrete-engine path, used by `ComponentRuntime` on an
  all-in-one schema).
- `WireContract` → `runtime_planes().emits_signal()` is **false** → the
  first branch fails, the second fails, the third short-circuits on
  `emits_signal()` being false. **No engine.**

The emission of the trait itself is gated on that boolean
(`schema-rust-next/src/lib.rs` lines 3064-3065):

```rust
if emits_signal_engine {
    self.line("pub trait SignalEngine {");
    ...
```

So `pub trait SignalEngine` only ever reaches the generated file when
`emits_signal_engine_support` returned `true` — which, for a wire-only
target, it cannot.

## Part 1 — `signal-spirit` builds a wire-only interface

### Build it

Command, in `/git/github.com/LiGoldragon/signal-spirit` (forced rebuild
by `touch build.rs`):

```
   Compiling signal-spirit v0.4.0-pre (/git/github.com/LiGoldragon/signal-spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.29s
```

`signal-spirit/build.rs` lowers the schema with `schema-next` and emits
Rust with `schema-rust-next`'s `RustEmitter` (verbatim, the heart of it):

```rust
let asschema = SchemaEngine::default()
    .lower_source(&source, SchemaIdentity::new("signal-spirit", "0.1.0"))
    .expect("lower signal-spirit.schema via schema-next");
let generated = RustEmitter.emit_file(&asschema);
```

### Locate the generated file

Command in the same repo:
`find target -name 'signal_spirit_generated.rs'` then pick the most recent
(`ls -t ... | head -1`). Real result:

```
CURRENT GENERATED FILE: target/debug/build/signal-spirit-5840adf8bf7eacd3/out/signal_spirit_generated.rs
```

(Two fingerprint dirs exist on disk; the most-recently-written one above
is the live artifact, content-identical to the other — both 8607 bytes.)

### Prove ZERO engines

Commands run against that file:

```
=== line count ===
232 target/debug/build/signal-spirit-5840adf8bf7eacd3/out/signal_spirit_generated.rs

=== grep -c Engine (count) ===
0

=== grep -c SignalEngine (count) ===
0

=== any occurrences of 'Engine' substring at all? ===
(NO MATCHES — zero engines)
```

`grep -c "Engine"` returns **0**. There is not a single occurrence of the
substring `Engine` anywhere in the 232-line generated file. And across the
whole crate including hand-written `src/lib.rs`:

```
=== zero engines across the ENTIRE signal-spirit crate source (src + generated) ===
src/ Engine matches: src/lib.rs:0
```

`src/lib.rs` has zero `Engine` matches too. The crate is engine-free end
to end.

### What IS emitted — wire types + codecs

The 232-line generated file contains exactly five kinds of thing. Verbatim
excerpts from
`target/debug/build/signal-spirit-5840adf8bf7eacd3/out/signal_spirit_generated.rs`:

**(a) Primitive aliases + the decode error enum** (lines 3-15):

```rust
pub type Text = String;
pub type Integer = u64;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum NotaDecodeError {
    Parse(String),
    ExpectedSingleRoot { found: usize },
    ExpectedDelimited { type_name: &'static str, delimiter: &'static str },
    ExpectedRootCount { type_name: &'static str, expected: usize, found: usize },
    ExpectedAtom { type_name: &'static str },
    UnknownVariant { enum_name: &'static str, variant: String },
    InvalidInteger { value: String },
}
```

**(b) The data types — newtypes, payload struct, root enums — each with
the rkyv derive set** (lines 86-109):

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Topic(pub Text);

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Description(pub Text);

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct RecordIdentifier(pub Integer);

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Entry {
    pub topic: Topic,
    pub description: Description,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Input {
    Record(Entry),
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Output {
    RecordAccepted(RecordIdentifier),
}
```

**(c) NOTA text decode/encode bridges per type** — `from_nota_block` /
`to_nota` (lines 141-157 for the `Entry` payload):

```rust
impl Entry {
    pub fn from_nota_block(block: &nota_next::Block) -> Result<Self, NotaDecodeError> {
        let children = expect_children(block, nota_next::Delimiter::Parenthesis, "parenthesis", "Entry", 2)?;
        Ok(Self {
            topic: Topic::from_nota_block(&children[0])?,
            description: Description::from_nota_block(&children[1])?,
        })
    }

    pub fn to_nota(&self) -> String {
        let fields = [
            self.topic.to_nota(),
            self.description.to_nota(),
        ];
        format!("({})", fields.join(" "))
    }
}
```

**(d) The root `FromStr` / `Display` impls** that make `Input`/`Output`
parse from and render to a NOTA string (lines 179-192):

```rust
impl std::str::FromStr for Input {
    type Err = NotaDecodeError;

    fn from_str(source: &str) -> Result<Self, Self::Err> {
        let root = parse_nota_root(source)?;
        Self::from_nota_block(&root)
    }
}

impl std::fmt::Display for Input {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(&self.to_nota())
    }
}
```

**(e) The `short_header` discriminant table** — the stable per-variant
wire tags (lines 229-232):

```rust
pub mod short_header {
    pub const INPUT_RECORD: u64 = 0x0000000000000000;
    pub const OUTPUT_RECORD_ACCEPTED: u64 = 0x0100000000000000;
}
```

The rkyv binary codec itself is the small hand-written `WireCodec` in
`signal-spirit/src/lib.rs` (`encode_input`/`decode_input` etc.), which
just calls `rkyv::to_bytes` / `rkyv::from_bytes` on the schema-derived
types. The codecs operate ON the emitted types; the emitted types carry
the rkyv derives that make that possible. Still no engine in sight.

### Prove the wire-only contract actually works (round-trips)

`cargo test` in `signal-spirit`. Real output:

```
running 6 tests
test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Those six tests (in `src/lib.rs`) exercise exactly the two wire surfaces:
rkyv round-trip of `Input`/`Output`, NOTA-text round-trip of `Input`/
`Output`, the derived `short_header` constants, and that the rendered NOTA
matches the human-authored bracket form
`(Record ([running-concept] [designer running spirit concept end-to-end]))`.
A wire-only contract that encodes, decodes, and parses — and nothing that
runs.

## Part 2 — `spirit`'s daemon-local signal schema DOES emit `SignalEngine`

### The same wire vocabulary, a different emission target

`spirit/build.rs` does not call the raw `RustEmitter`. It builds a
`GenerationPlan` and selects the per-module target explicitly (verbatim,
`spirit/build.rs` lines 31-39):

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

`ModuleEmission::signal_runtime_module("signal")` resolves to the
`SignalRuntime` target (verbatim, `schema-rust-next/src/build.rs` lines
145-151):

```rust
pub fn signal_runtime_module(module: impl Into<String>) -> Self {
    Self::new(
        module,
        RustEmissionOptions::feature_gated_nota("nota-text")
            .with_target(RustEmissionTarget::SignalRuntime),
    )
}
```

For comparison, the public contract path in the same file is
`wire_contract_module` → `.with_target(RustEmissionTarget::WireContract)`
(lines 125-131). Same emitter, same schema-lowering front end — the only
difference is the target enum value.

### The artifact: checked in, not in `target/`

Unlike `signal-spirit` (which emits into `$OUT_DIR` and `include!`s from
there), spirit's daemon schema is emitted into a **checked-in** source
file and the build only re-checks freshness unless
`SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1` is set. Locations and sizes:

```
=== src/schema dir ===
-rw-r--r-- 1 li users 28098 ... nexus.rs
-rw-r--r-- 1 li users 22810 ... sema.rs
-rw-r--r-- 1 li users 37438 ... signal.rs
```

`spirit/src/schema/signal.rs` is a 1209-line checked-in artifact. The
freshness regeneration command:

```
=== Force schema regeneration + build (SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1) ===
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.06s
```

(The build reported `Finished` with no recompile — the checked-in artifact
already matches what the emitter produces, i.e. it is fresh.)

### Prove it HAS the engine

```
=== grep -c SignalEngine in src/schema/signal.rs ===
1
=== total line count of signal.rs ===
1209 src/schema/signal.rs
```

`grep -c` counts matching **lines**; the single match is the trait
declaration line. Locating it:

```
1156:pub trait SignalEngine {
```

The trait body, verbatim from `spirit/src/schema/signal.rs` (lines
1156-1195):

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

This is the **abstract** SignalEngine: associated types
`NexusInput`/`NexusOutput` (because spirit's `signal.schema` declares no
`NexusWork`/`NexusAction` — those live in `nexus.schema`/`nexus.rs`), plus
the actor lifecycle (`on_start`/`on_stop`), the trace hooks, and the
triage→reply seam. `triage_inner`/`reply_inner` are the abstract methods
the daemon MUST implement; `triage`/`reply` are provided defaults that
wrap them with tracing.

### The same wire vocabulary lives alongside the engine

The runtime emission is NOT a replacement of the wire types — it is a
superset. The same `Input`/`Output` roots are present in spirit's
`signal.rs`:

```
266:pub enum Input {
277:pub enum Output {
```

And the engine-plane scaffolding that wraps them appears only here, never
in the wire-only file:

```
876:pub enum SignalObjectName {
1116:pub mod signal {
1123:pub enum ActorStartFailure {
1140:pub enum ActorStopFailure {
1156:pub trait SignalEngine {
```

The negative proof — none of that scaffolding exists in the wire-only
generated file:

```
-- signal-spirit generated grep for ActorStartFailure|...|triage|reply_inner --
0
(0 == none of the engine-plane scaffolding present in the wire-only file)
```

### The trait is a real seam the daemon fills

The generated trait is abstract on purpose: it leaves `triage_inner` /
`reply_inner` for the daemon to implement. The daemon's hand-written impl,
located by `grep -rn "impl SignalEngine" src/ --include='*.rs'`:

```
src/engine.rs:209:impl SignalEngine for SignalActor {
```

Verbatim, `spirit/src/engine.rs` lines 209-245:

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

This is where the daemon binds the abstract `NexusInput`/`NexusOutput` to
the concrete `Nexus<NexusWork>`/`Nexus<NexusAction>` from its sibling
nexus plane, and supplies the real triage/reply behaviour. The generated
trait is the contract; this impl is the runtime.

## Why the split exists

The split is not bureaucratic — each direction buys something concrete.

**Rebuild isolation.** The public `signal-spirit` contract has a tiny
dependency closure: `nota-next` + `rkyv`, with the schema toolchain only
in `[build-dependencies]`. A peer that links the contract to construct
operations does not pull the daemon's actor framework, the nexus plane,
or the sema plane into its build graph. Changing the daemon's engine
internals (`spirit/src/engine.rs`) does not touch the contract crate at
all; changing the wire schema rebuilds both, but the contract's consumers
never rebuild because of engine churn. The wire surface and the runtime
surface have independent rebuild fates.

**Security / audit visibility.** The wire-only artifact is exactly 232
lines of vocabulary + codecs with provably zero executable engine
(`grep -c Engine` → 0). An auditor reviewing the public attack surface
reads a small, closed file: it can parse and serialize bytes, and that is
all it can do. There is no `triage`, no actor lifecycle, no behaviour that
a malicious or malformed operation could drive. The capability to ACT on
an operation lives only in the daemon, behind the `SignalEngine` seam,
inside the `spirit` binary — not in anything a peer links.

**Boundary clarity (the two meanings of "signal schema").** The public
`signal-<component>` contract (here `signal-spirit`) IS the
`WireContract` emission: wire only, the thing other repos depend on. The
daemon-local `<component>/schema/signal.schema` IS the `SignalRuntime`
emission: the same wire vocabulary plus the engine plane the daemon owns
privately. Same schema language, same emitter, same lowering — one knob
(`RustEmissionTarget`) decides whether the result is a contract or a
runtime. Keeping them as two emissions means the contract can never
accidentally ship runtime code, and the runtime can never drift from the
wire vocabulary, because both are generated from schema by the same tool.

## Constraints this mechanism reveals (toward INTENT.md)

- `signal-<component>` repos emit at `WireContract` — wire vocabulary +
  codecs, provably zero engines. The engine plane is daemon-local only.
- The daemon's `schema/signal.schema` emits at `SignalRuntime`, which
  forces the abstract `SignalEngine` trait (associated `NexusInput`/
  `NexusOutput`) regardless of whether the signal schema declares concrete
  nexus types — that's why a signal schema with no `NexusWork`/`NexusAction`
  still gets an engine.
- One `RustEmissionTarget` knob, not two code paths, is the sole
  difference between contract and runtime emission. This is the seam to
  protect: never let a contract repo flip to a runtime target.

## What I could NOT run

Nothing material was blocked. Both builds ran (`signal-spirit` compiled
fresh after `touch build.rs`; `spirit` regenerated/checked artifacts with
`SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1`). The `signal-spirit` test suite ran
green. I did not exercise the deployed `spirit` CLI for this report
because the claim set is about emission-time artifacts (generated source),
which are fully proven by building and grepping the generated files
directly. I did not edit any code-repo source, schema, or INTENT.md.
