---
title: 492 — Psyche report: vision-architecture ratification queue
role: designer
variant: Psyche
date: 2026-06-03
topics: [psyche-report, ratification-queue, vision-architecture, designed-not-implemented, trace-client-library, help-namespace, nota-config-convention, substrate-maturation, schema-daemon, persona-supervisor, introspect, contract-repo-split, per-repo-manifestation, deferred-inner-nexus, symbol-path]
description: |
  A ratification-ready inventory of architecture that is designed but
  not yet implemented — designs you can ratify in place and hand to
  operator. Each item shows the actual code/schema/skill shape, where
  the design lives in the corpus, what blocks implementation, and the
  specific yes/no/redirect that would unblock it. Eleven items grouped
  A through K plus one explicitly-deferred item (J) carried so the
  boundary stays visible. The report is the chance to engage with the
  workspace's pending vision in one place.
---

# 492 — Psyche report: vision-architecture ratification queue

## 1. What this report is

This is the workspace's pending-vision inventory. Across the recent
designer + operator + skill corpus, a fair amount of architecture has
firmed up into concrete shape without yet crossing the threshold into
an operator implementation slice. Some of it is waiting on your
ratification. Some is waiting on prior work to land. Some is waiting
on context the report itself is the chance to supply. The point of the
report is to bring all of it in front of you at once, with the actual
code shapes where they exist, so you can ratify items in place or ask
for more before they move into operator queue.

The report follows the discipline that landed today — *"Psyche
reports must show actual code, not summarize as line counts or vague
references"* (Spirit 1515 Maximum) — and the bracket-quote citation
discipline — *"reference intent records in prose markdown by quoting
the description summary literally as bracketed text — the bracketed
form IS the citation"* (Spirit 1522 + 1526 Maximum + High). Where a
design has a code shape, the code is shown. Where the cite is
load-bearing, the substance is quoted alongside the number.

A few items reference reports that were retired during context
maintenance (designer 469, 478, 483). Where that happens, the report
sources the substance from current skills, ESSENCE, INTENT, or the
operator reports that the substance migrated into, and notes the
retired-report origin only as historical orientation.

## 2. A — Tracing-side designs

The tracing side is the most-firm of the inventory. The fresh intent
of the day refined trace into its own typed schema-defined interface,
with strings only at the client display surface. Several derived
designs surfaced; some are ratified, some lean-pending, some still
open.

### A.1 — `TraceCliSession` / `drain_to_stdout` on `triad-runtime` (Path B)

The current CLI-side trace wiring is hand-written per component. From
`/git/github.com/LiGoldragon/spirit-next/src/bin/spirit-next.rs:30-42`:

```rust
#[cfg(feature = "testing-trace")]
let trace_client =
    TraceClient::from_environment("SPIRIT_NEXT_TRACE_SOCKET", Duration::from_millis(200))?;
let (_route, output) = SignalTransport::connect(socket_path)?.exchange(&input)?;
println!("{output}");
#[cfg(feature = "testing-trace")]
trace_client.print_events(&mut std::io::stdout())?;
```

Each component CLI binary repeats this same shape; the only thing that
differs across `schema-daemon`, `introspect`, `persona`, etc. is the
env-var name (`SPIRIT_NEXT_TRACE_SOCKET`). Sub-agent A's Path B
proposal lifts the per-component repetition into the shared
substrate. Addition to
`/git/github.com/LiGoldragon/triad-runtime/src/trace.rs`, in the same
`impl<Event>` blocks where `from_environment` + `print_events` live:

```rust
impl<Event> TraceClient<Event>
where
    Event: TraceEventFrame,
{
    pub fn for_env(variable: impl Into<String>) -> Result<Self, TraceError> {
        Self::from_environment(variable, Duration::from_millis(200))
    }
}

impl<Event> TraceClient<Event>
where
    Event: TraceEventFrame + Display,  // becomes `+ ToNota` per the NOTA-codec refinement
{
    pub fn drain_to_stdout(&self) -> Result<(), TraceError> {
        self.print_events(&mut std::io::stdout())
    }
}
```

The CLI shape collapses to:

```rust
#[cfg(feature = "testing-trace")]
let trace_client = TraceClient::for_env("SPIRIT_NEXT_TRACE_SOCKET")?;
let (_route, output) = SignalTransport::connect(socket_path)?.exchange(&input)?;
println!("{output}");
#[cfg(feature = "testing-trace")]
trace_client.drain_to_stdout()?;
```

The hand-written `Duration::from_millis(200)` and `std::io::stdout()`
move into the library. A sibling `drain_to_sema_log(&self, store:
&SemaStore<...>)` method joins `drain_to_stdout` on the same library,
so the same two-line CLI shape covers both client sinks. Per Spirit
1503 (Principle High) — *"Trace client behavior belongs in a reusable
client library that can enable NOTA display or SEMA-backed trace
logging; the CLI should be a thin wrapper around that library."*

**Status.** In the 488 Psyche report you said *"I would go with Path
B but is there more context?"* The capture (Spirit 1511) was first
filed as a Decision and then your Correction Maximum (Spirit 1516)
named the discipline — *"a psyche statement that leans toward a
choice while explicitly asking for more information is NOT a
ratification"* — and 1511's certainty became Zero. The §2.1 code above
is the more context you asked for. With the two-method addition
visible (`for_env` + `drain_to_stdout`), Path B reduces per-component
CLI trace wiring from five lines to two with roughly ten new lines on
`triad-runtime`.

**Ratification ask.** Yes/no on Path B with the §2.1 code visible. Or
ask for further code — the `TraceCliSession`-typed variant (a small
struct holding the client + the listener context), the SEMA-log
method signature, or the schema-rust-next-emitted Path A shape for
comparison.

### A.2 — Trace-client library housing display + SEMA-log + thin CLI wrapper

The companion direction to A.1. Per Spirit 1501 (Decision High) +
1503 (Principle High): *"a trace-client library lives in the repo and
owns the display plus SEMA-log features. The CLI becomes a thin
wrapper that enables and calls the library features rather than
reimplementing trace listener and decoder logic per component."*

Three candidate locations surfaced in the 487.5 overview:

- **Inside `triad-runtime`** (designer lean) — already hosts the
  trace transport mechanics; adding the display + SEMA-log methods
  there keeps the substrate together. This is what Path B in A.1
  realises concretely.
- **A dedicated `trace-client` crate** — separates the client-side
  library from the rest of `triad-runtime`. Cost is one more crate;
  benefit is narrower compile scope for code that doesn't need
  trace.
- **A workspace-level `signal-trace` crate** — treats trace as a
  first-class contracted signal-tier interface, aligning with Spirit
  1492 (Decision Maximum) — *"tracing is its own schema-defined
  interface with closed generated enum vocabularies for trace names
  and events, not an ad hoc string log."* If trace becomes a real
  signal channel between components (introspect ingests typed
  trace), this is its natural home.

The three are not mutually exclusive in the long arc: ratifying Path
B at `triad-runtime` first does not foreclose a later promotion to
`signal-trace` once trace becomes its own contracted channel.

**Ratification ask.** Confirm library location for the first
landing. Designer lean: `triad-runtime`. Promotion to `signal-trace`
remains a future-open redirect.

### A.3 — Trace-event rendering via the type's derived NOTA codec

Per Spirit 1499 (Clarification High) + 1502 (Correction Maximum) +
1497 (Correction Maximum): *"trace display at the client edge should
render the typed trace event as NOTA when the trace type has the
generated NOTA surface; the client should not invent a custom string
log format for trace events."* The rendered string IS NOTA text,
the workspace's standard typed-data text projection.

Today, `TraceClient::print_events` uses `Display`:

```rust
impl<Event> TraceClient<Event>
where
    Event: TraceEventFrame + Display,
{
    pub fn print_events(&self, writer: &mut impl Write) -> Result<(), TraceError> {
        for event in self.events()? {
            writeln!(writer, "{event}")?;
        }
        Ok(())
    }
}
```

Refined shape:

```rust
impl<Event> TraceClient<Event>
where
    Event: TraceEventFrame + ToNota,  // bound swap
{
    pub fn print_events(&self, writer: &mut impl Write) -> Result<(), TraceError> {
        for event in self.events()? {
            writeln!(writer, "{}", event.to_nota())?;  // one-line swap
        }
        Ok(())
    }
}
```

This is a one-line swap after `TraceEvent` carries the derived NOTA
codec under the `testing-trace` feature scope. The schema-rust-next
emission needs a small addition to derive `NotaEncode`/`NotaDecode`
on `TraceEvent` when the `testing-trace` feature is enabled — that's
the prerequisite that gates the swap.

**Ratification ask.** Confirm the bound swap direction (it follows
directly from Spirit 1502 Maximum), and ratify the small
schema-rust-next emission addition that makes the swap possible. The
substance of the direction is already ratified at Maximum; what's
pending is the operator slice that lands the schema-rust-next side.

### A.4 — Per-variant interface-route trace identity emission

The current `schema-rust-next` emission produces `SignalObjectName`,
`InputRoute`, `NexusObjectName`, etc. as schema-emitted enums.
Operator 291's audit identified that the per-route trace-identity
emission — `SignalObjectName::Input(InputRoute::Record)` style
identities — is in place at the type level but the per-method
emission inside the engine traits doesn't yet always carry the
specific route. Spirit 1492 ratified the closed-vocabulary direction;
the per-variant emission completes it.

The substance previously sat in retired designer 483 §Q4b; the live
home is now operator 291's "What Still Needs Work" + the
`schema-rust-next` emission's per-engine-method trace hook
generation.

**Ratification ask.** Confirm the per-variant emission completion is
in scope for the next schema-rust-next slice; the substance follows
from Spirit 1492 Maximum. This is more of a "yes, do this next" than
an open design question.

### A.5 — Schema-daemon honoring the daemon-NOTA-free boundary day-one

Per Spirit 1495 (Principle Maximum) — *"daemons should stay free of
NOTA decoding and avoid string surfaces except for actual
user-authored string payloads; clients translate NOTA text into
binary protocol data and render typed replies or traces for users."*
The modern reference stack (`spirit-next` + `triad-runtime`) honors
this on the binary side. The deployed legacy persona-spirit does not
(NOTA-at-startup remains a known migration arc per A.4 in 487.5).
The question: when the schema-daemon pilot's binary lands, does it
honor 1495 from day one?

Designer lean: yes. Schema-daemon is being designed fresh; carrying
NOTA decoding into the daemon would replicate the legacy-persona-
spirit problem on a new component. Every signal handler decodes
binary; the CLI client translates NOTA to binary.

**Ratification ask.** Confirm: yes, schema-daemon honors 1495
day-one when its binary lands.

## 3. B — Help / description namespace

Sub-agent B (designer 487.2) designed `Description` as a fourth
schema kind alongside Signal / Nexus / SEMA, with one
`.description.schema` sibling file per component bound to the same
schema identity. The shape composes cleanly with the canonical
SymbolPath you elevated at Spirit 1506 (Clarification Maximum) +
1507 (Principle High). Per Spirit 1493 (Principle High) — *"help and
documentation should be schema data in a mirror description
namespace over the global symbol namespace, with generated defaults
when no explicit description entry exists for a fully qualified
symbol."*

### B.1 — `SymbolPath` as the canonical identity type

The path mechanism is workspace-canonical, not per-design. The shape
sub-agent B proposed:

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize,
         Clone, Debug, Eq, Hash, PartialEq)]
pub struct SymbolPath {
    component: Name,
    plane: SchemaPlane,
    variant: Option<Name>,
    payload: Option<Name>,
    field: Option<Name>,
}

pub enum SchemaPlane {
    Operation,
    Reply,
    NexusWork,
    NexusAction,
    SemaWriteInput,
    SemaWriteOutput,
    SemaReadInput,
    SemaReadOutput,
    Effect,
    Type,
}

impl SymbolPath {
    pub fn type_only(component: Name, type_name: Name) -> Self { /* ... */ }
    pub fn variant(component: Name, plane: SchemaPlane, variant: Name) -> Self { /* ... */ }
    pub fn field(component: Name, plane: SchemaPlane,
                 variant: Name, payload: Name, field: Name) -> Self { /* ... */ }

    pub fn parent(&self) -> Option<SymbolPath> { /* field → payload → variant → plane */ }
    pub fn humanized(&self) -> Description { /* default-generator fallback */ }
}
```

`SymbolPath` is a data-bearing struct, not a ZST namespace — per the
method-only hard override. The bracket-vector NOTA form renders the
same path at user-facing edges: `[tiny-keystore Operation Put
KeyValue key]` reads as component `tiny-keystore`, plane
`Operation`, variant `Put`, payload type `KeyValue`, field `key`.

Trace identity already reuses this — `SignalObjectName::Input(
InputRoute::Record)` is a `SymbolPath` rendered through one client's
projection. NOTA config-by-convention (section 4) uses it. Future
introspection surfaces inherit it.

### B.2 — `HelpRegistry` as the schema-emitted runtime noun

```rust
pub struct HelpRegistry {
    component: Name,
    explicit: std::collections::BTreeMap<SymbolPath, Description>,
    schema_summary: SchemaSummary,
}

pub enum DescribedSymbol {
    Explicit(Description),
    Generated(Description),  // came from humanizing the path
}

impl HelpRegistry {
    pub fn for_component() -> Self { /* schema-emitted constant, one per component */ }

    pub fn describe(&self, symbol: &SymbolPath) -> DescribedSymbol {
        match self.explicit.get(symbol) {
            Some(description) => DescribedSymbol::Explicit(description.clone()),
            None => DescribedSymbol::Generated(self.default_for(symbol)),
        }
    }

    pub fn main(&self) -> MainHelp { /* assembles the (Help Main) reply */ }
    pub fn verb(&self, name: &Name) -> Option<VerbHelp> { /* assembles (Help (Verb <name>)) */ }

    fn default_for(&self, symbol: &SymbolPath) -> Description {
        symbol.humanized()  // six-branch rule by symbol shape
    }
}
```

A `(Help (Verb Put))` request runs `registry.verb(&Name::from("Put"))`
and returns a typed `VerbHelp` carrying the operation's `Description`,
the payload type's `Description`, and each field's `Description`.
Strings appear only when the CLI renders the typed `VerbHelp`.

### B.3 — The companion `.description.schema` sibling file

```schema
. tiny-keystore.description

descriptions {
  [Operation Put]
    [Insert or replace a value at the given key.]
  [Operation Put KeyValue key]
    [The key under which to store the value.]
  [Operation Put KeyValue value]
    [The bytes to store at the key.]
  [Operation Get]
    [Read the value stored at the given key, if any.]
}
```

Each entry pairs a `SymbolPath` (bracket-vector form) with a typed
`Description` (bracket-string). Unspecified symbols fall through to
the humanizer.

### B.4 — The decisions

All six remain open from 487.2. Designer leans across all six:

- **B.1 — Schema location**: sibling `.description.schema` file
  alongside the working schema, bound to the same
  `SchemaIdentity`.
- **B.2 — Default-generator algorithm**: lazy at lookup time,
  six-branch humanization keyed on symbol shape.
- **B.3 — Rendering surfaces**: CLI `(Help (Verb))` first; HTML site
  deferred.
- **B.4 — Mandatory vs optional per component**: optional — a
  component ships without a `.description.schema` and Help still
  works via pure-generated defaults.
- **B.5 — SymbolPath shape**: five-segment structured path
  (component, plane, variant, payload, field) — canonical now per
  Spirit 1506/1507.
- **B.6 — Help operation auto-injection timing**: first slice ships
  `Description` + `HelpRegistry` for the tiny-keystore pilot;
  auto-injection of `Help` into the macro is the second slice after
  pilot ratification.

**Ratification ask.** Each of B.1–B.6 wants a yes/redirect.
Designer leans can stand as defaults if you don't dispute them. The
substantive ones are B.1 (file convention) and B.2 (the humanization
algorithm) — the others mostly track from the design's own logic.

## 4. C — NOTA config-by-convention

Per Spirit 1494 (Principle High) — *"authored workspace data files
should prefer typed NOTA data: predictable file names and
directories define the expected root type, usually a struct or
sometimes a top-level enum selection or vector of records."*
Sub-agent C (designer 487.3) designed the substrate.

### C.1 — The schema and registry shape

```rust
pub struct NotaConfigConvention {
    name: Name,                       // identifying handle for the convention
    pattern: PathPattern,             // glob over directory + filename
    root_type: RootType,              // the typed declaration
    decoder_descriptor: DecoderDescriptor, // how to decode raw NOTA into the typed root
}

pub enum RootType {
    Struct(StructDescriptor),
    Enum(EnumDescriptor),
    VectorOfRecords(RecordDescriptor),
}

pub struct NotaConfigRegistry {
    conventions: Vec<NotaConfigConvention>,
    decoder_lookup: ResolvedDecoderTable,
}

pub enum TypedNotaValue {
    Skills(Vec<SkillEntry>),
    Intent(Vec<IntentEntry>),
    BootstrapPolicy(Vec<BootstrapEntry>),
    // ... one variant per registered RootType
}

impl NotaConfigRegistry {
    pub fn from_bootstrap_file(path: &Path) -> Result<Self, NotaConfigLoadError> {
        let conventions = Self::decode_bootstrap(path)?;
        let decoder_lookup = ResolvedDecoderTable::resolve(&conventions)?;
        Ok(Self { conventions, decoder_lookup })
    }

    pub fn load(&self, path: &Path) -> Result<TypedNotaValue, NotaConfigLoadError> {
        let entry = self.decoder_lookup.match_path(path)
            .ok_or_else(|| NotaConfigLoadError::PathNotRegistered { path: path.to_path_buf() })?;
        let raw_nota = std::fs::read_to_string(path)
            .map_err(|source| NotaConfigLoadError::IoFailure { path: path.to_path_buf(), source })?;
        entry.decoder.decode_typed(&raw_nota)
    }

    pub fn register(&mut self, convention: NotaConfigConvention)
        -> Result<(), NotaConfigLoadError>
    { /* ... */ }
}
```

The convention entry for `skills/skills.nota`, expressed as a NOTA
value:

```nota
(NotaConfigConvention
  [skills-index]
  (PathPattern [/home/li/primary/skills] [skills.nota])
  (VectorOfRecords (RecordDescriptor [SkillEntry]))
  (DecoderDescriptor [primary-workspace skills SkillEntry]))
```

A call site after registration:

```rust
let registry = NotaConfigRegistry::from_bootstrap_file(
    Path::new("/home/li/primary/nota-conventions.nota"))?;

let skills = match registry.load(
    Path::new("/home/li/primary/skills/skills.nota"))?
{
    TypedNotaValue::Skills(entries) => entries,
    other => return Err(NotaConfigLoadError::root_type_mismatch_observation(other)),
};
```

### C.2 — The decisions

- **C.1 — Registry location**: designer lean is schema-emitted from
  per-component schemas PLUS a workspace-root file for workspace-only
  conventions like `skills/skills.nota`. The harder sub-question
  inside this is whether `skills/skills.nota` is workspace-level (the
  lean) or belongs to a hypothetical workspace-meta-component.
- **C.2 — Eager vs lazy**: designer lean is eager (compile-time
  static) for production builds, lazy (start-up file-read) for dev
  iteration.
- **C.3 — Error vs warning on mismatch**: designer lean hard error
  per the closed-world discipline.
- **C.4 — Glob syntax + overlap handling**: designer lean shell-style
  globs; overlapping conventions error at registry-validation.

**Ratification ask.** C.1 is the substantive one — registry location
shapes how schema registries compose across the workspace boundary.
Designer-lean default holds if you don't push back. C.2–C.4 mostly
follow from existing disciplines.

## 5. D — Substrate maturation (post-1486)

Spirit 1486 (Decision Maximum) ratified the engine-mechanism
substrate from designer 482 — *"NexusWork/NexusAction asymmetric
pair + 5-variant action set (ReplyToSignal, CommandSemaWrite,
CommandSemaRead, CommandEffect, Continue); macro-generated runner
loop (triad_main! emitted from schema-rust-next); effects per-
component declared in schema with Stash as first universal
candidate; Continue as in-process immediate recursion; cross-
component invocation via Signal contracts not Nexus-internal
access."* Several pieces of this substrate exist in shape but are
not yet uniformly implemented across the workspace.

### D.1 — `triad_main!` macro emission from `schema-rust-next`

Per Spirit 1419 (Decision High) — *"triad engine wiring should be
defined programmatically by the schema-generated engine substrate,
with daemon main reduced to a very small macro or generated call
that instantiates the component."*

Today `triad_main!` does NOT exist in schema-rust-next. Each
component's `main` is hand-written; spirit-next's is the worked
example, and the engine-trait composition lives in `engine.rs`
inside the daemon crate. The substrate-ratification at Spirit 1486
named this as part of the canonical substrate; the operator slice
to land it is still pending.

The destination shape (illustrative; not in any source today):

```rust
// In spirit-next/src/bin/spirit-next-daemon.rs, after triad_main! lands:
triad_main!(spirit_next);  // emits the whole runner loop + signal listener + nexus driver + sema store wiring
```

Compare with today's spirit-next daemon `main` which assembles the
signal listener, the nexus actor, the sema store, the runner loop,
and the lifecycle by hand — substantial code per component that
should be once-emitted.

**Ratification ask.** Confirm `triad_main!` lands as the next
substrate maturation slice (the substance is already ratified at
Maximum via 1486; the slice is the operator's; this is asking you
to confirm scheduling).

### D.2 — `NexusAction` 5-variant pattern in production components beyond spirit-next

Per Spirit 1486 the 5-variant `NexusAction` set is workspace
canonical. Spirit-next has it (verified in
`/git/github.com/LiGoldragon/spirit-next/src/nexus.rs:197` — `Continue
(input)` is wired). Other components that will run on the substrate —
the schema-daemon pilot (section 6), the introspect pilot (section
8), eventually persona (section 7) — need the same vocabulary.

For schema-daemon, the `SchemaEdit` apply operations and `Stash` of
upgrade receipts would each be a `NexusAction` variant. For
introspect, the trace ingest path emits `CommandSemaWrite` to
persist; query path emits `CommandSemaRead`.

**Ratification ask.** Confirm: every new daemon comes up on the
5-variant substrate from day one; no per-component hand-rolled
runtime loop variation. This follows from 1486 Maximum but worth
naming as an explicit constraint applied at every new-daemon entry
point.

### D.3 — Engine-trait lifecycle hooks across components

Per Spirit 1487 (Decision High) — *"generated Signal, Nexus, and
SEMA engine traits should carry minimal lifecycle hooks: on_start
and on_stop with typed start and stop failure results."*

Spirit-next has them today
(`/git/github.com/LiGoldragon/spirit-next/src/engine.rs:94-107` plus
the trait impls at lines 210, 216, 203). The next consumer is
persona-system supervision (section 7). Until persona-system exists
as a daemon, the lifecycle hooks are there but no one's using them.

```rust
pub trait NexusEngine {
    fn on_start(&mut self) -> Result<(), ActorStartFailure> { Ok(()) }
    fn on_stop(&mut self) -> Result<(), ActorStopFailure> { Ok(()) }
    fn execute(&mut self, input: NexusWork) -> NexusAction;
    // ... trace and lifecycle hooks
}
```

Default `Ok(())` bodies mean a component with no setup/teardown
needs no override. Components that bind sockets, open databases,
register listeners override `on_start`; the typed failure carries
reasons persona supervision reads to decide retry / escalate / fail.

**Ratification ask.** Confirm the hooks stay at this minimum shape
until persona-system lands as their concrete consumer (per A.1
section 7). The hooks are correctly minimal; broader actor-mailbox /
backpressure / runtime-control trait surface stays deferred per
Spirit 1483 (section J below).

### D.4 — Effects per-component declared in schema, with `Stash` as the first universal

Spirit 1486 named *"effects per-component declared in schema with
Stash as first universal candidate."* Spirit-next has `Stash` wired
today as a `NexusEffectCommand`. The wider substrate — where each
component declares its own effect vocabulary in schema and the
`schema-rust-next` emitter generates the effect-handler trait — is
designed but not yet generated across the workspace.

The shape spirit-next emits today
(`/git/github.com/LiGoldragon/spirit-next/schema/lib.schema:15-16`):

```schema
NexusEffectCommand [(Stash StashRequest)]
NexusEffectResult [(Stashed StashResult)]
```

The wider pattern: every component's `NexusEffectCommand` /
`NexusEffectResult` vector declares the effects that component
honors. `Stash` is the universal one; per-component additions
(file-write for one daemon, external-process-call for another) get
declared in the same vector and dispatched by the runner loop.

**Ratification ask.** Confirm that effects-per-component is the
shape for each new daemon's schema, with `Stash` as the universal
inheritance. This follows from 1486 Maximum.

### D.5 — Cross-component invocation via Signal contracts, not Nexus-internal access

Per Spirit 1486 *"cross-component invocation via Signal contracts
not Nexus-internal access."* This is the design discipline ratified;
the first cross-component pair built on it is still pending. The 484
overview named **spirit-next + introspect** as the first pair to
actually talk — *"narrowest typed dependency (one-way push, no
bidirectional). Both schema-next-based (no legacy compat)."*

The shape: introspect declares a Signal endpoint
`IngestTraceEvents(TraceBatch)` in its contract; spirit-next (when
trace is enabled) opens a signal client to introspect's endpoint and
pushes typed trace batches. Spirit-next's Nexus never reaches into
introspect's internals. Persona later supervising both does it via
each component's owner-signal contract, not via reaching into their
Nexus.

**Ratification ask.** Confirm spirit-next + introspect as the first
cross-component pair on the new substrate. This was named in 484
overview as Decision 5 with designer recommendation to ratify; it
hasn't been explicitly ratified yet.

## 6. E — Schema-as-daemon (the pilot direction)

Designer 481 (Design, 2026-06-02) landed the schema-daemon's
upgradable-runtime substrate as a coordinated feature-branch pilot:
the typed `UpgradeObject`, `SchemaEdit` enum (with `AddField`,
`ChangeFieldType`, `AddVariant`), the `AsschemaEdit::apply`
pipeline, and the `MigrationEmitter` that consumes an
`UpgradeObject` and emits a Rust module containing `mod historical`,
`mod current`, and `impl From<historical::T> for current::T`. The
end-to-end witness in
`schema-rust-next/tests/upgrade_emission.rs::emitted_source_compiles_and_migrates_a_value`
constructs an `UpgradeObject` with both `AddField` (default-filled)
and `ChangeFieldType` with `WrapSingleton`, emits Rust source,
writes it, invokes `rustc` to compile a harness, and runs the
compiled harness — asserting the migrated value has `last_modified
== 0_i64` and `score == vec![7_i64]`.

Per Spirit 1309 (Decision Maximum) — *"the schema daemon IS the
editor of the schema. It receives upgrade messages, applies them to
its Asschema, derives both the new data type code and the upgrade
migration code. The system becomes self-editing through this flow."*

What 481 deferred per Spirit 1469: the daemon binary, the socket,
the `SchemaSemaEngine` actor, the `signal-schema` contract repo, and
operator 287's `NexusWork`/`NexusAction` vocabulary integration.
These are the production-readiness pieces.

The 484 overview's Decision 1 (Maximum) sub-divided this further:
**schema-daemon owns EDIT** (apply UpgradeObject to Asschema; record
in SEMA upgrade-history); **the existing upgrade-daemon retains
BUILD** (rustc compilation of migration code; new artifact
production) **and COMPILE-CUTOVER** (deploying the new binary; client
handover). The two daemons coordinate via signal contracts.

**Ratification ask.** Confirm the schema-daemon EDIT vs upgrade-
daemon BUILD-COMPILE-CUTOVER split, plus the production-readiness
pieces 481 deferred (daemon binary, socket, SchemaSemaEngine,
`signal-schema` contract repo) move into operator queue as the next
schema-side slice. The substance is designed; the slice is waiting.

## 7. F — Persona-as-supervisor

The 484 overview's Decision 3 (Maximum) — **persona itself runs on
the triad-engine substrate**. Persona's SEMA = manager event log +
reducer snapshots. Nexus owns four substantive decisions: restart-
decide, orphan-relaunch, FD-handoff route, quarantine acceptance.
Signal exposes `owner-signal-persona` + `signal-engine-management`.
*"Persona is not a special case; it's a regular triad-engine daemon
supervising other triad-engine daemons."*

The 484 overview's Decision 4 (Maximum) — **separate universal
`signal-persona-supervision` contract**. Persona supervising any
component needs a shared SUPERVISION VOCABULARY: `LaunchEngine`,
`StartComponent`, `StopComponent`, `Query(ComponentStatus)`,
`RegisterReady`, `HandoffClient`, `RequestQuiesce`, `ReportHealth`.
Designer recommendation: ratify option (a) — one universal
`signal-persona-supervision` contract every supervised component
implements, not (b) — reuse each component's existing owner-signal
contract for lifecycle Mutate operations.

This is the **concrete consumer of D.3 lifecycle hooks**. The hooks
on `NexusEngine` / `SignalEngine` / `SemaEngine` traits with their
typed `ActorStartFailure` / `ActorStopFailure` failure types exist
so persona-system supervision can decide retry / escalate / fail on
typed reasons.

The whole shape is designed across designer 484.2 (sub-agent B) and
the four sub-decisions in 484.6. The repo doesn't exist yet
(`persona-system-daemon` / `signal-persona-supervision`) and no
operator slice has touched it.

**Ratification ask.** Three things to confirm:

- Persona runs on the triad-engine substrate (Decision 3 Maximum
  designer recommendation).
- Universal `signal-persona-supervision` contract (Decision 4
  Maximum designer recommendation, option a).
- Schedule timing: after D.3 lifecycle hooks are exercised somewhere
  (today they sit unused), persona-system becomes their first
  consumer. Sequence: ratify F now; build it after at least one
  supervised-component example exists.

## 8. G — Introspect

Per Spirit 1398 (Decision High) — *"the new introspection component
should be named introspect, dropping the persona prefix from
persona-introspect, and should use schema-next based triad engine
interfaces. It should be a configurable trace destination for all
components, decide what and how to log, and provide a queriable
source of tracing-derived intelligence."*

Per Spirit 1500 (Decision High) — *"trace events may also be logged
into a SEMA database purpose-built for trace storage, as an
alternative client-side trace sink alongside NOTA display. The
daemon continues to emit typed binary trace frames regardless;
client-side options are display-to-stream or persist-to-sema. This
reinforces the introspect-style direction."*

The repos exist as scaffolds — `/git/github.com/LiGoldragon/introspect`
and `/git/github.com/LiGoldragon/signal-introspect` are checked out
with `AGENTS.md`, `ARCHITECTURE.md`, `schema/`, `src/`, `tests/` — but
the concrete signal contract and the daemon-side ingest + storage +
query are not yet built. This is the second leg of A.2's SEMA-log
direction at the consumer end: spirit-next's trace client opens a
signal client to introspect's ingest endpoint and pushes typed
trace batches; introspect persists them in a purpose-built SEMA.

Two threads of overlap:

- **SEMA-log location.** Spirit 1500 keeps the SEMA-log option
  available at the client library too (`drain_to_sema_log` on
  `TraceClient`). The trace-client library could either persist
  locally to its own SEMA, or push the trace events as a Signal
  request to introspect's ingest endpoint where introspect persists
  them in introspect's SEMA. The first is simpler; the second is
  the cross-component proof.
- **First cross-component pair.** Per Decision 5 in 484 overview,
  spirit-next + introspect is the recommended first pair. This is
  the same pair as section D.5; introspect is the destination
  component.

**Ratification ask.** Three things:

- Confirm introspect's signal contract: typed trace ingest endpoint
  (`IngestTraceEvents(TraceBatch)` shape), typed query endpoints
  (filter by component / time-range / event kind).
- Confirm the SEMA-log shape: introspect's SEMA is purpose-built for
  trace storage (Spirit 1500 Maximum direction).
- Confirm the operator slice schedule: introspect comes up after the
  trace-client library lands at `triad-runtime` (A.1 / A.2) and
  before persona-system (section F).

## 9. H — Contract repo split + fleet-rename

Per Spirit 1422 (Decision Maximum) — *"component triad pipeline
split — Signal interface declaration lives in the signal-<component>
contract repository because clients depend on the Signal contract;
the daemon imports all Signal types from the contract crate. Nexus
and SEMA interface declarations live in the daemon repository
because they are daemon-internal runtime concerns. Exception/
extension — when a daemon grows a separate scale-out database the
SEMA interface may also extract to a contract repository for the
database client. The contract repository IS the canonical source for
client-facing Signal types; daemon-internal Nexus/SEMA stay local
until separation is needed for scale."*

Per Spirit 1427 (Decision Maximum) — *"spirit triad canonical
naming — retire core-signal-spirit; the spirit triad legs are spirit
(daemon) + signal-spirit (ordinary signal contract; already exists)
+ meta-signal-spirit (policy/meta signal contract; new)."* The
`owner-signal-<component>` shape is renamed `meta-signal-<component>`.

**Current state.** `signal-spirit` exists at
`/git/github.com/LiGoldragon/signal-spirit`. `meta-signal-spirit`
does NOT yet exist as a repo. The cross-fleet sweep — renaming every
`owner-signal-<component>` to `meta-signal-<component>` (cloud,
persona-spirit, etc.) — is partly done. Workspace template is set;
the migration across existing components is incremental.

**Ratification ask.** Confirm the fleet-rename sweep is in scope as
its own operator slice (or several). Substance is ratified at
Maximum; the schedule is pending. Designer lean: rename happens as
each component is touched for other reasons, with explicit
cross-fleet sweep when no other reason brings the component into
scope before too long.

## 10. I — Help / discoverability surfaces (auto-injection)

Distinct from section 3 (which is the description schema substrate),
section I is the **auto-injection** of `(Help Main)` and `(Help
(Verb <name>))` into every contract's Signal operation set without
per-component boilerplate.

Per Spirit 263 (Decision Maximum) — *"every component supports (Help
Main) and (Help Verb) operations in its NOTA argument vocabulary;
help documentation likely auto-wired via the signal-channel macro."*
Per Spirit 1396 (Decision High) — *"every root enum emitted by
schema-rust-next gets a Help action variant generated automatically
by the macro — Help uses the schema interface description as the
source to generate help messages."*

The legacy signal stack auto-injection lives in
`signal-system/skills.md` §"signal_channel! macro" — the
`signal_channel!` macro emits Help into every contract. The
schema-derived stack equivalent — schema-rust-next emitting Help
into every root enum — is designed (per 1396 Decision High) but not
yet generated. Spirit-next's `lib.schema` doesn't include Help
operations today; verified at
`/git/github.com/LiGoldragon/spirit-next/schema/lib.schema:2` —
operations are `[(Record Entry) (Observe Query) (Lookup ...) ...]`
with no Help arm.

The dependency: auto-injection needs section 3's `Description` +
`HelpRegistry` substrate first. After 3 lands as the tiny-keystore
pilot, the second slice is auto-injection — every component picks up
Help on the next schema-rust-next rebuild with no per-contract
boilerplate.

**Ratification ask.** Confirm the second-slice scheduling: after the
description substrate lands, schema-rust-next gets a small emission
addition that wires `(Help Main)` and `(Help (Verb <name>))` into
every root enum's Operation enum + the `HelpRegistry` lookup. The
substance is ratified across Spirit 263 + 1396 + 1493; the slice is
the operator's after section 3.

## 11. J — DEFERRED — inner Nexus engine + runtime control + actor scheduling

Per Spirit 1483 (Decision High) — *"workspace explicitly defers
backpressure handling runtime control layer inner Nexus engine actor
scheduling/prioritization and related deeper-runtime work. These
are future-deeper-runtime that won't be touched for a while. Spirit
1465 (inner Nexus engine) + designer 478 (recursive runtime control)
+ operator 289 (NexusControlCommand backpressure) all carry the
deferred-future label going forward. Production-orientation focuses
on the substrate (NexusWork/NexusAction + effects per component +
Stash) and component interaction (spirit-next + introspect first
pair). Runtime control extensions land later if/when overload
evidence appears in real production load."*

This item is in the inventory ONLY so the deferred boundary stays
visible. Designer 478 covered the recursive runtime control direction
(retired during context maintenance; substance lives in current
skills as the deferred future direction). No ratification ask —
the deferral itself is the ratified position. The boundary surfaces
again if/when overload evidence appears at the deferral's threshold;
until then, the substrate without the inner engine carries
production work.

## 12. K — Per-repo `INTENT.md` / `ARCHITECTURE.md` manifestation pass

Today's ESSENCE.md and INTENT.md gained substantial additions:
*"Strings only at the edges; the system is typed"*, *"NOTA is a
typed text user interface"*, *"Symbols are paths through the schema
namespace"*, *"Tracing is its own typed schema-defined interface"*,
*"Help and documentation are schema data in a mirror description
namespace"*, *"Authored data files prefer typed NOTA, by path
convention"*. These are workspace-level manifestations of the day's
Spirit captures.

The per-repo manifestation pass — reflecting these workspace-level
additions into each component's `INTENT.md` + `ARCHITECTURE.md` —
is the next manifestation cycle. Per spirit record 944 (Maximum,
2026-05-27): *"per-repo files are the canonical agent-context surface
for the repo — READ them on entry AND UPDATE them as relevant
intent lands. Manifestation of psyche intent into a repo's
INTENT.md and ARCHITECTURE.md is part of the work cycle, not a
deferred pass."*

But this manifestation is **gated**. Per the 488 §8 closing — *"the
per-repo INTENT.md and ARCHITECTURE.md updates remain deferred —
they should track ratified shape rather than draft, so they wait for
B and C ratifications before the manifestation pass."* Manifesting
the draft shape of B (help-namespace) and C (NOTA config) into
per-repo files before you ratify locks in possibly-wrong shape.

**Ratification ask.** Confirm the gating: per-repo manifestation
pass runs after sections B (help) and C (NOTA config) are ratified
in this report. The repos that absorb the most substance — `nota`,
`nota-codec`, `schema-next`, `schema-rust-next`, `triad-runtime`,
`spirit-next` — are the first targets when manifestation runs.

## 13. The ratification queue

Each item with designer lean and ratification ask, in one table the
psyche can scan and engage with:

| Item | Designer lean | What you'd be ratifying |
|---|---|---|
| **A.1** TraceCliSession / Path B | Yes (with §2.1 context) | Two-method addition to `TraceClient<Event>` reducing per-component CLI trace wiring from 5 lines to 2 |
| **A.2** Trace-client library location | `triad-runtime` first | Library home for display + SEMA-log + thin CLI wrapper, with future-open promotion to `signal-trace` |
| **A.3** Trace render via derived NOTA codec | Yes (substance ratified) | Schema-rust-next emission addition: derive NOTA codec on `TraceEvent` under `testing-trace` feature |
| **A.4** Per-variant trace identity | Yes (next slice) | Schema-rust-next per-engine-method trace hook emission completion |
| **A.5** Schema-daemon honors 1495 day-one | Yes | Schema-daemon's binary stays NOTA-free from day one when it lands |
| **B.1** Description schema location | Sibling `.description.schema` | One file per component bound to the same `SchemaIdentity` |
| **B.2** Default-generator algorithm | Lazy + six-branch | Humanize at lookup time, six branches keyed on symbol shape |
| **B.3** Rendering surfaces | CLI Help first | HTML site deferred |
| **B.4** Mandatory vs optional | Optional | Component ships without `.description.schema` and Help still works via defaults |
| **B.5** SymbolPath shape | Five-segment structured path | Canonical now per Spirit 1506/1507 |
| **B.6** Help auto-injection timing | Second slice | First slice tiny-keystore pilot; second slice macro auto-injection |
| **C.1** Registry location | Both per-component + workspace-root | `skills/skills.nota` is workspace-level convention |
| **C.2** Eager vs lazy | Eager production, lazy dev | Compile-time static for production; start-up file-read for dev iteration |
| **C.3** Error vs warning on mismatch | Hard error | Closed-world discipline |
| **C.4** Glob syntax + overlap | Shell-style + overlap-error | Overlapping conventions error at registry-validation |
| **D.1** `triad_main!` emission | Next substrate slice | Schema-rust-next emits the runner loop; daemon `main` reduces to one macro call |
| **D.2** 5-variant NexusAction in new daemons | Yes (constraint) | Every new daemon comes up on the 5-variant substrate from day one |
| **D.3** Lifecycle hooks stay minimal | Yes (until consumer) | `on_start` / `on_stop` only; broader actor surface stays deferred per 1483 |
| **D.4** Effects per-component with Stash universal | Yes | Each component declares effects in schema; `Stash` is universal inheritance |
| **D.5** Spirit-next + introspect first pair | Yes | Cross-component invocation via Signal contracts, not Nexus-internal |
| **E** Schema-daemon EDIT split | Yes | Schema-daemon owns EDIT; upgrade-daemon retains BUILD + COMPILE-CUTOVER |
| **F** Persona-as-supervisor | Yes | Persona runs on triad substrate; separate `signal-persona-supervision` contract; build after first supervised example |
| **G** Introspect | Yes | Typed trace ingest + query endpoints; purpose-built SEMA for trace storage |
| **H** Fleet-rename + contract split | Yes (incremental sweep) | `owner-signal-<component>` → `meta-signal-<component>` as each component is touched, plus explicit sweep |
| **I** Help auto-injection | Yes (after B) | Schema-rust-next emits Help into every root enum after description substrate lands |
| **J** Deferred — inner Nexus engine | Stays deferred per 1483 | No ratification ask; boundary visible only |
| **K** Per-repo manifestation | Yes (after B + C) | Per-repo INTENT.md / ARCHITECTURE.md update pass runs after B + C ratifications |

Twenty-six items total, of which J is the deferred boundary marker
and the others are ratification candidates. Many cluster: A.3 + A.4
+ A.5 follow from already-ratified Maximum substance and just need
"yes, next slice" confirmation. D.2 + D.3 + D.4 + D.5 follow from
Spirit 1486 Maximum. B.1–B.6 and C.1–C.4 are designer leans that
hold as defaults unless you push back. The substantive engagements
are A.1, A.2, E, F, G, K — each shapes how the workspace composes
across the next few weeks.

## 14. What this report itself demonstrates

The report uses the YAML front matter discipline from Spirit 1527,
the bracket-quote citation form from Spirit 1522 + 1526, the
narrative-voice shape from Spirit 1521, and the show-the-code
discipline from Spirit 1515. No `---` horizontal-rule lines in the
markdown body — section structure comes from headings. Mermaid
diagrams are kept to 5-node cap per Spirit 1282 (this report does
not use mermaid; the substance is text + code excerpts). All
identifier choices in code excerpts follow the full-English-word
naming rule and the method-only no-ZST-namespace hard override.

The report is also the chance to verify a particular discipline —
*"psyche reports should let the psyche follow the line of thought
all the way back to the basics: when a report refreshes or audits
prior work, it should re-ground the current issues from first
principles instead of assuming the reader already has the whole
context loaded"* (Spirit 1529 Principle High). Each item carries
enough first-principles context that the psyche can engage with it
in place without needing to open prior reports — sections A and B
inline the load-bearing code from 488's §3a + §4a; sections E + F +
G + H quote the load-bearing Spirit records' substance directly.

## 15. Cross-references

The ratification-ready inventory draws on these surfaces:

- `/home/li/primary/ESSENCE.md` §"Strings only at the edges", §"NOTA
  is a typed text user interface", §"Symbols are paths through the
  schema namespace" — universal manifestation of the day's
  clarifications, upstream of the items in this report.
- `/home/li/primary/INTENT.md` §"Tracing is its own typed schema-
  defined interface", §"Help and documentation are schema data",
  §"Authored data files prefer typed NOTA", §"Symbols are paths
  through the schema namespace" — workspace-prose manifestation,
  the per-repo gating in section K is about these.
- `/home/li/primary/skills/component-triad.md` §"Runtime triad
  engine traits", §"Lifecycle hooks", §"Nexus mechanism substrate",
  §"Trace enablement is explicit per case" — the substrate the items
  in section D refine; A.2 builds on the trace-enablement section.
- `/home/li/primary/reports/designer/488-Psyche-487-overview-context-and-decisions-2026-06-03.md` —
  the immediate prior Psyche report; the §3a code excerpts in A.1
  are sourced from there.
- `/home/li/primary/reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/` —
  the meta-report directory carrying sub-agent A (trace audit), B
  (help namespace), C (NOTA config), D (context maintenance); the
  designs in sections 2-4 of this report are 487's sub-designs.
- `/home/li/primary/reports/designer/484-Audit-production-readiness-meta-2026-06-02/6-overview.md` —
  the production-readiness audit that named the five cross-cutting
  decisions; sections E + F + G of this report draw on 484's
  Decisions 1 + 3 + 4 + 5.
- `/home/li/primary/reports/designer/481-schema-daemon-upgradable-runtime-pilot-2026-06-02.md` —
  the schema-daemon pilot landing; section E draws on this for
  the EDIT-vs-BUILD-COMPILE-CUTOVER split.
- Recent Spirit records — the bracket-quoted citations throughout
  the report: 263 (Help auto-injection), 1309 (schema-daemon IS the
  editor), 1396 (Help variant generated), 1398 (introspect),
  1419 (triad runner via macro), 1422 (contract-repo split), 1427
  (spirit-triad fleet-rename), 1483 (deferred inner Nexus), 1486
  (substrate ratification), 1487 (lifecycle hooks), 1488
  (schema-source carries), 1489–1497 (trace + help + config band),
  1499–1503 (trace render as NOTA, SEMA-log, library),
  1505 + 1509 + 1510 + 1511 + 1512 + 1514 (trace eprintln removal +
  per-crate documentation + Path B + daemon string boundary), 1515
  (psyche reports show code), 1516 (lean vs ratification), 1521 +
  1522 + 1526 (narrative voice + bracket-quote citation), 1527
  (YAML front matter), 1529 (refresh from first principles).
