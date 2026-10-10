# Slice A2 — spirit-next schema-derived parity gap

*Audit sub-agent report. READ-ONLY. Maps the schema-derived intent
thread onto the spirit-next pilot source as it actually stands at
`/git/github.com/LiGoldragon/spirit-next` on `HEAD` (working tree,
src last touched 2026-06-03/04). Honesty about state over fidelity to
brief: several brief assumptions (drawn from INTENT.md's tracing
snapshot and report 53) are now stale — the pilot moved past them.*

## Intent Anchors

[Tracing is its own schema-defined interface with closed generated
enum vocabularies — typed objects, typed events — not an ad hoc string
log; string rendering happens only when a client surface prints them]
(Spirit 1489-1492 High/Maximum)

[Schema-rust-next emits the trace object names and TraceEvent from the
component's schema; engine traits emit trace default hooks at every
actor boundary; component code overrides only the sink behavior]
(Spirit 1490 Maximum)

[Client-side tracing should be generated or generic from schema
interface definitions; the CLI stays a thin client and does not own
component-specific trace logic beyond enabling or displaying the
generic trace surface] (Spirit 1491 High)

[Every component runtime conducts its core logic through three
schema-emitted engine traits — SignalEngine triage-only, NexusEngine
heavy-logic + bidirectional translator + mail keeper, SemaEngine
durable single-writer with apply/observe split] (Spirit 1330-1332,
1327 Maximum)

[Help and documentation belong inside the schema substrate as a mirror
description namespace over the global symbol namespace, keyed by
SymbolPath, with a default generated from the schema declaration when a
slot is empty] (Spirit 1493 High)

[When the workspace writes data it might as well be a NOTA vector of
records; a file's directory plus its predictable name fixes the
expected root type by convention] (Spirit 1494 High)

[Spirit implements an explicit CollectRemovalCandidates operation as a
Signal root collecting reviewed Zero-certainty records and emitting
their summary form to a configurable output target, separating
discovery/extraction from the destruction concern in Remove]
(Spirit 1543, 1547 Maximum/High)

[Spirit defines a small-record data type carrying core load-bearing
fields — identifier, topics, kind, description summary, magnitude,
daemon-stamped date and time — what variant-ladder short-form reads
and CollectRemovalCandidates emit] (Spirit 1549 High)

[Spirit gains a RecordDefault short-form recording operation taking
only fields agents commonly customize, with defaults injected for the
rest; Record remains the canonical full-fidelity operation]
(Spirit 1550 High)

## The headline, in one paragraph

Two intent threads cross this slice. The **schema-derived runtime
thread** (1330-1332, 1489-1494) is the spirit-next pilot's actual
charter, and on the runtime-engine and trace axes the pilot is *ahead*
of the brief's snapshot: all three engine traits are schema-emitted,
the runtime is genuinely composed of the three trait impls on
data-bearing nouns, the full trace object-name vocabulary +
`TraceEvent` + the engine-trait trace default hooks are
schema-emitted, and the hand-written per-component trace adapter has
already shrunk to two small gated impls (one of which now delegates to
generated NOTA). The **production-Spirit removal/variant-ladder thread**
(1474, 1541-1556) lives entirely in the production `persona-spirit`
triad and is *absent* from spirit-next — which is correct by design
(spirit-next is the schema pilot, not the production daemon) but
produces the divergence the brief asks me to flag: two implementations
of "Spirit," and the production one carries an operation
(`CollectRemovalCandidates`), a small-record shape, and a short-form
ladder that the schema pilot has no equivalent for. The help/description
namespace (1493) and NOTA config-by-convention (1494) are pure-design —
no emitter, no resolver. The schema-source-header thread (1551-1556) is
substantially *implemented* in operator-owned `schema-next` already
(inline declarations + a namespace resolver), not pure-design.

## (a) Three-engine traits — present, schema-emitted, composed

The three engine traits are **generated** into
`src/schema/lib.rs` (not hand-written), and the runtime is a genuine
composition of the three trait impls attached to data-bearing nouns.
This satisfies Spirit 1327/1330-1332 at the pilot.

### The generated trait surface

`src/schema/lib.rs:1843-1937` defines all three traits. Verbatim
`SignalEngine` (triage-only with the inner/outer split + trace hooks):

```rust
pub trait SignalEngine {
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
    // ... rejected / triaged / replied hooks ...

    fn triage_inner(&self, input: signal::Signal<signal::Input>) -> nexus::Nexus<nexus::Work>;
    fn reply_inner(&self, output: nexus::Nexus<nexus::Action>) -> signal::Signal<signal::Output>;

    fn triage(&self, input: signal::Signal<signal::Input>) -> nexus::Nexus<nexus::Work> {
        let output = self.triage_inner(input);
        self.trace_signal_triaged();
        output
    }
    // reply() wraps reply_inner + trace_signal_replied likewise
}
```

`NexusEngine` (`:1881-1905`) carries `decide` (the heavy-logic hook the
component implements) plus an `execute` default that wraps it in
entered/decided trace hooks. `SemaEngine` (`:1907-1937`) carries the
**apply/observe split** Spirit 1332 demands — `apply_inner`
(`&mut self`, write) and `observe_inner` (`&self`, read) — each wrapped
by a public `apply`/`observe` default that fires the SEMA write/read
trace hook. The `&self` vs `&mut self` distinction is the durable
single-writer / parallel-reads property at the type level.

### The three impls on data-bearing nouns

| Trait | Impl on | Noun's data | Source |
|---|---|---|---|
| `SignalEngine` | `SignalActor` | `next_message_identifier`, `next_origin_route` counters | `src/engine.rs:208-235` |
| `NexusEngine` | `Nexus` | `store: Store`, `mail_ledger: MailLedger`, `stash_table: StashTable` | `src/nexus.rs:202-269` |
| `SemaEngine` | `Store` | `database: redb::Database`, `path` | `src/store.rs:40-149` |

None is a ZST namespace; each owns real data. The composition is the
`Engine` struct (`src/engine.rs:25-31`):

```rust
pub struct Engine {
    signal_actor: SignalActor,
    nexus: Mutex<Nexus>,
    #[cfg(feature = "testing-trace")]
    trace_log: TraceLog,
}
```

`Engine::handle` (`:114-128`) runs the record-970 flow as a
composition: Signal admits → `accepted.process_with(&signal_actor,
&mut nexus)` → inside, `signal_engine.triage` produces Nexus work,
`NexusEngine::execute(nexus, ...)` drives it, `signal_engine.reply`
frames the output. The `&mut Nexus` borrow held across `execute` is the
single-flight guard (`:257-277`).

### Nexus as mail keeper + translator (1331, 970) — present

`Nexus` owns the `MailLedger` and the mail enters BEING-PROCESSED via
`self.sent.push_to(&mut nexus.mail_ledger().hook())` *before* triage
(`src/engine.rs:265-267`), and the processed event pushes after the
reply (`:273-275`). The Signal↔SEMA translation is real: Nexus's
`decide` loop (`src/nexus.rs:222-268`) is the bidirectional translator —
`NexusWork::SignalArrived` → SEMA command, SEMA completion → Signal
reply or recursive effect. Nexus reaches SEMA **exclusively through the
trait surface** (`SemaEngine::apply` / `SemaEngine::observe` at
`:240`/`:245`), exactly as 1330 prescribes. Verdict: **implemented**.

## (b) Typed trace interface (1489-1492) — ahead of the brief's snapshot

The brief (echoing INTENT.md §"Tracing … Current implementation
status") says spirit-next "supplies the component-specific adapter
(one `TraceEventFrame` impl + one `Display for TraceEvent` impl)" and
that the open work is "generating the CLI/client trace adapter so the
per-component adapter shrinks to zero." Reading the source, that
snapshot is **partly stale**:

### Schema-emitted (not hand-rolled) — confirmed

`src/schema/lib.rs:1356-1497` emits `SignalObjectName`,
`NexusObjectName`, `SemaObjectName`, the umbrella `ObjectName`, and
`TraceEvent(pub ObjectName)` — each with a generated `name()` and each
deriving `nota_next::NotaDecode, NotaEncode` under the `nota-text`
feature. The object-name enums carry both the route variants
(`SignalObjectName::Input(InputRoute::Record)` →
`"SignalInputRecord"`) and the lifecycle variants (`Started`,
`Admitted`, `Triaged`, `Replied`, etc.). This is the
schema-defined-path trace identity Spirit 1492 + INTENT.md
§"Symbols are paths" call for. The engine-trait trace default hooks
(quoted in (a)) are also generated. Verdict: **implemented**.

### Hand-written adapter — already smaller than the brief states

`src/trace.rs` (the whole file, 36 lines, gated `testing-trace` per
`src/lib.rs:29-30`) is the *entire* hand-written adapter:

```rust
impl TraceEventFrame for TraceEvent {
    fn to_trace_archive(&self) -> Result<Vec<u8>, TraceError> {
        rkyv::to_bytes::<rkyv::rancor::Error>(self)
            .map(|archive| archive.to_vec())
            .map_err(|_| TraceError::ArchiveEncode)
    }
    fn from_trace_archive(archive: &[u8]) -> Result<Self, TraceError> {
        rkyv::from_bytes::<Self, rkyv::rancor::Error>(archive)
            .map_err(|_| TraceError::ArchiveDecode)
    }
}

#[cfg(feature = "nota-text")]
impl std::fmt::Display for TraceEvent {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(&<Self as crate::schema::lib::NotaEncode>::to_nota(self))
    }
}
```

Two corrections to the brief's framing: (1) the `Display` impl is **no
longer a hand-rolled string render** — it delegates to the generated
`NotaEncode::to_nota`, so the trace string surface is schema-owned NOTA,
matching 1489's "string rendering happens only when a client surface
prints them, from the typed value." (2) The `TraceEventFrame` impl is a
two-method rkyv round-trip wrapper — mechanical, identical in shape for
every component, and the only genuinely hand-written trace code left.

### Client path — generic, not per-component — confirmed

The CLI does not own trace logic. `src/bin/spirit-next.rs:34-40` just
constructs a generic `TraceClient` and calls `print_events`:

```rust
let trace_client =
    TraceClient::from_environment("SPIRIT_NEXT_TRACE_SOCKET", Duration::from_millis(200))?;
// ...
trace_client.print_events(&mut std::io::stdout())?;
```

`TraceClient`, `TraceLog`, `TraceSocketListener` are generic type
aliases over `triad_runtime::trace::*<TraceEvent>` (`src/trace.rs:4-6`).
The listen/decode/print path lives in `triad-runtime`
(`src/trace.rs:312-322`, `print_events` is `impl<Event> TraceClient<Event>
where Event: TraceEventFrame + Display`). So the generic client trace
path **is** the shared-runtime substrate the brief asked about — it is
generic, just not *generated*.

### What remains genuinely open

The residual `TraceEventFrame` rkyv-roundtrip impl is the last
hand-written boundary. It is the same 12 lines for every component, so
it is the natural candidate to emit from schema (a
`#[derive(TraceEventFrame)]` or a schema-rust-next blanket emission
keyed on the `TraceEvent` newtype). That is the "shrink the
per-component adapter to zero" open work — but it is **not field-level
decided**: the psyche has not specified whether it lands as a derive
macro, a schema-rust-next emission, or a blanket impl in triad-runtime
over a `NotaEncode`-bound type. See Portability ledger.

## (c) Help / description namespace (1493) — pure design, not implemented

No description-mirror, no SymbolPath-keyed description map, no
default-from-schema humanizer exists anywhere in the slice. Searching
`schema-rust-next/src` for `Description`/`Help`/`SymbolPath`/`humaniz`
returns only an unrelated migration doc-comment. In spirit-next,
`Description` (`src/schema/lib.rs:210`) is just a `String` alias used as
a *record field* (`Entry.description`) — it is the intent record's body,
not a help-text mirror over the symbol namespace. Help today is still
Rust doc-comments on the generated types (e.g. the daemon doc-comments
in `src/engine.rs:18-24`). Verdict: **missing**, and **blocked** — the
mirror's storage shape, the SymbolPath type's home, and the
default-generator's humanization rules are all open (designer 487.2 is a
design, not a field-level decision in source).

## (d) NOTA config-by-convention (1494) — pure design, no resolver

There is **no** `nota-config` crate in the slice and **no**
path-to-typed-root resolution. spirit-next's `Configuration`
(`src/config.rs:8-13`) is a hand-written rkyv-only struct loaded from a
**binary** path:

```rust
pub fn from_binary_path(path: impl AsRef<Path>) -> Result<Self, ConfigurationError> {
    let bytes = fs::read(path).map_err(ConfigurationError::Read)?;
    Self::from_binary_bytes(&bytes)
}
```

The doc-comment is explicit that "the daemon intentionally does not
decode NOTA at startup" (`src/config.rs:5-6`) — which is consistent with
the daemon-gets-binary rule, but the *convention registry* (directory +
predictable name → expected root type) that 1494 describes does not
exist. `Configuration` is also not schema-emitted; it is a hand-written
struct, a small Pattern-C deviation (boundary type that is not a
generated noun). Verdict: **missing**, **blocked** — the convention
patterns, the registry's home, and the loader's typed-failure contract
are open.

## (e) Schema-source-header thread (1551-1556) — partly implemented in schema-next

This thread is NOT pure-design. The relevant machinery already lives in
operator-owned `schema-next` (`/git/github.com/LiGoldragon/schema-next`,
main):

- **Inline declarations** — `src/source.rs:294-805` carries
  `public_inline_declarations`, `private_inline_declarations`,
  `inline_declaration_names`, `inline_declaration_name`, and
  `engine.rs:766-769` drains inline declarations during lowering. So a
  variant can declare its payload type inline at use-site, and lowering
  hoists it.
- **Namespace resolution of bare variant names** — `src/source.rs:955-986`
  defines a `SourceVariantResolver` trait and a `SourceTypeResolver`
  that collects every namespace entry name **plus** the inline
  declaration names from input/output bodies, then answers
  `resolves_variant_payload(name)`. This is the "bare variant name
  resolved via namespace" mechanism (1551).

spirit-next already *consumes* the header form: `schema/lib.schema:2-3`
is exactly a root header listing bare variant names —
`[Record Observe Lookup Count Remove LookupStash]` (input root) and the
output root on line 3 — resolved against the namespace brace on lines
4-94. So the header-with-bare-names + namespace-resolution shape is
**implemented and in use**.

What I could NOT positively confirm as a distinct, named mechanism is a
*multi-pass identifier resolution* loop (1556) beyond the single
collect-then-resolve the `SourceTypeResolver` does (it pre-collects all
names, so forward references resolve in one pass — which may be exactly
what 1556 intends, or may be short of a fuller multi-pass design). I am
flagging this as a partial with a blocked-reason rather than asserting
either way, per the bias-to-blocked rule. nota-next carries none of
this header machinery (search returned nothing) — it lives in
schema-next. Note: any port here is a **feature branch on
operator-owned main**, not a designer worktree free-for-all.

## The divergence the brief asks me to flag

The production removal/variant-ladder thread (1474, 1541-1556) is
**fully present in the production `persona-spirit` triad and absent from
the schema pilot**. Concrete witnesses in production:

- `signal-persona-spirit::RemovalCandidateCollection` and the
  `CollectRemovalCandidates` operation root —
  `persona-spirit/src/observation.rs:24,43,62-63`,
  `src/actors/dispatch.rs:243,331-336`,
  `src/store.rs:128-130` (`fn collect_removal_candidates ->
  Result<RemovalCandidatesCollected>`).
- The output-target enum (1548) — production tests exercise
  `(File [{}])` as the final field of the collection request:
  `tests/boundary.rs:409`, `tests/actor_runtime.rs:272`.
- The small-record summary shape (1549) — the emitted summary tuple
  `(1 [workspace] Correction [candidate description] Zero Zero)` in
  `RemovalCandidatesCollected` (`tests/boundary.rs:422`,
  `tests/actor_runtime.rs:290`) carries identifier, topics, kind,
  description, magnitude, and the daemon stamp.
- `persona-spirit/ARCHITECTURE.md:52-59` documents the
  archive-then-retract lifecycle (1542/1543) and the `ArchiveFailed`
  skip path.

spirit-next has **none** of these: no `CollectRemovalCandidates`, no
`RemovalCandidate`, no `OutputTarget`/`Stdout`/`Stderr`/`File`, no
`RecordDefault`, no small-record/summary type, no variant ladder, no
date/time stamping on `Entry` (`schema/lib.schema:89` —
`Entry { Topics * Kind * Description * Magnitude * Privacy * }`, no
`RecordedTime`). This is the **two-implementations-of-Spirit**
repetition: the production daemon (`persona-spirit` + `signal-`/
`meta-signal-persona-spirit`, hand-written actor stack on `signal-frame`/
`nota-codec`) and the schema pilot (`spirit-next`, schema-emitted on
`schema-next`/`nota-next`) are two living realizations of the same
component. The removal-candidate thread is the newest production
feature; the schema pilot has no path to it yet. Whether the pilot
should grow these is a **psyche decision** (the eventual cutover, per
INTENT.md §"Two deploy stacks coexist"), not something to port now.

## Abstractions worth naming

1. **The per-component `TraceEventFrame` rkyv-roundtrip impl is
   copy-paste across every component** — spirit-next's
   `src/trace.rs:8-19` is two methods that just call
   `rkyv::to_bytes`/`from_bytes` and map the error. Every schema
   component that traces will write the identical 12 lines. This is the
   single named pattern that should resolve into one schema emission or
   one blanket impl. (Beauty: repetition resolves into a single named
   pattern.)

2. **Plane-envelope `with_origin_route` / `into_root` / `origin_route`
   threading** recurs at every engine boundary
   (`engine.rs:229,233,236,240,245`; `store.rs:63,93,101,147`). It is
   already generated, but worth naming as the canonical cross-plane
   envelope discipline so future components don't re-derive it.

## Bad patterns / deviations from essence

1. **`Configuration` is a hand-written boundary struct, not a
   schema-emitted noun** (`src/config.rs:8-26`). Pattern C
   (methods-on-schema-generated-types) and the schema-IS-the-architecture
   direction want config to be a schema type too — especially once 1494
   (NOTA config-by-convention) lands, since the convention registry
   needs the root type to be a known schema symbol. Fix: declare
   `Configuration` in `schema/lib.schema` and let it emit.

2. **`ConfigurationPath(String)` and `LocalPath/PublicPath/SourcePath`
   as bare `String` aliases** (`schema/lib.schema:5-7`,
   `src/config.rs:16`). These are filesystem paths at a schema position —
   `String` at the edge is fine, but a path is a typed-domain value
   (the essence's "strings only at the edges; everything else typed").
   Minor; the production triad has the same shape, so it is a shared
   convention, not a pilot regression. Fix candidate, not a defect.

## Open decisions for the psyche

Three field-level decisions gate the portable-looking work in this
slice. All are surfaced rather than ported, per the standing
ask-don't-infer override.

1. **Generated `TraceEventFrame` — derive, schema-emission, or blanket
   impl?** The last hand-written trace code is the 12-line rkyv
   roundtrip. Landing the generated form requires picking ONE of:
   (a) a `#[derive(TraceEventFrame)]` proc-macro in nota-next/a new
   crate; (b) schema-rust-next emitting the impl whenever the schema
   declares a `TraceEvent` newtype; (c) a blanket
   `impl<T: NotaEncode + rkyv-roundtrip> TraceEventFrame for T` in
   triad-runtime. Recommendation: (b), since the trace object names are
   already emitted there and 1490 explicitly assigns the trace
   vocabulary to schema-rust-next.

2. **Help/description namespace home + SymbolPath type home.** 1493 +
   designer 487.2 are a design; the field-level shape (where the
   description map lives, where `SymbolPath` is declared, the
   humanization rules for the default generator) is undecided. This
   blocks any code.

3. **NOTA config-by-convention registry shape.** 1494 + designer 487.3
   are a design; the convention patterns (which directory + name → which
   root), the registry's home crate, and whether `Configuration` becomes
   a schema-emitted type are all open. This blocks the resolver.

## Portability ledger

| Design (intent) | Status in spirit-next | Portable? / blocked-reason |
|---|---|---|
| Three engine traits, schema-emitted (1327, 1330-1332) | implemented — all three generated, composed on data-bearing nouns | n/a (already landed) |
| Nexus mail-keeper + Signal↔SEMA translator (1331, 970) | implemented — MailLedger owned by Nexus; decide-loop translates both ways via SEMA trait surface | n/a (already landed) |
| Schema-emitted trace ObjectName / TraceEvent + engine trace hooks (1490, 1492) | implemented — generated in `src/schema/lib.rs:1356-1497` + trait hooks | n/a (already landed) |
| Generic client trace path (1491) | implemented — generic `TraceClient` in triad-runtime; CLI is thin | n/a (already landed) |
| Per-component trace adapter shrinks to zero (1490 open work) | partial — only the 12-line `TraceEventFrame` rkyv impl remains hand-written | **blocked** — psyche must pick derive vs schema-emission vs blanket impl (Open decision 1) |
| Help/description mirror namespace (1493) | missing — only doc-comments; `Description` is a record field, not a help mirror | **blocked** — mirror storage shape, SymbolPath home, humanizer rules undecided |
| NOTA config-by-convention + nota-config crate (1494) | missing — `Configuration` is hand-written rkyv-binary; no path→root registry | **blocked** — convention patterns, registry home, schema-vs-handwritten config undecided |
| Schema-source-header: bare-variant names resolved via namespace + inline declarations (1551-1554) | implemented in schema-next; consumed by spirit-next `lib.schema` header | n/a (already landed in operator-owned schema-next) |
| Schema-source multi-pass identifier resolution (1556) | partial — single collect-then-resolve via `SourceTypeResolver`; no distinct multi-pass loop confirmed | **blocked** — unclear if single-pass collect satisfies 1556 or a fuller multi-pass design is intended; ask psyche |
| CollectRemovalCandidates Signal root (1543, 1547) | missing in pilot (present in production persona-spirit) | **blocked** — pilot-vs-production cutover is a psyche decision; do not port the production thread into the schema pilot unbidden |
| Customizable output-target enum Stdout/Stderr/File (1548) | missing in pilot (present in production tests) | **blocked** — same cutover decision |
| Small-record summary data type with daemon stamp (1549) | missing in pilot — `Entry` has no RecordedTime/Date/Time | **blocked** — same cutover decision; plus stamping is a schema addition the psyche has ordered for production, not the pilot |
| RecordDefault short-form + variant ladder (1474, 1545, 1550) | missing in pilot | **blocked** — same cutover decision |
| Explicit archival-before-deletion lifecycle (1542) | missing in pilot (documented in production ARCHITECTURE.md) | **blocked** — same cutover decision |
</content>
