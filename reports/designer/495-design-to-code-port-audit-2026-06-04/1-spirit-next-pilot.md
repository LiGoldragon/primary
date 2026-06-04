---
title: "spirit-next pilot — design-to-code port audit (slice 1)"
role: designer
variant: Audit
date: 2026-06-04
topics:
  - spirit-next
  - schema-derived-stack
  - strings-at-edges
  - lifecycle-hooks
  - constraint-witnesses
  - symbol-paths
description: >
  Completeness-and-quality audit of the landed spirit-next pilot against
  recent psyche intent (records 1486-1567). Alias lowering, lifecycle hooks,
  the daemon binary string boundary, and wrapper-free construction are all
  landed and clean. The audit finds the load-bearing gaps as missing
  constraint witnesses (the daemon-never-sees-a-non-payload-string intent has
  no test), the entirely-absent SymbolPath identity space, the hand-piloted
  (not generated) runner loop, and a small set of bad patterns.
---

# spirit-next pilot — design-to-code port audit

## What the slice is

`/git/github.com/LiGoldragon/spirit-next` is the runnable schema-derived
Spirit pilot: a CLI + daemon pair whose wire types are emitted from
`schema/lib.schema` through `schema-next` + `schema-rust-next` into the
checked-in `src/schema/lib.rs`, with hand-written runtime behavior attached as
methods on the generated nouns. The slice is the proving ground for
[strings only at the edges; the system is typed] (records 1490/1492/1495),
[lifecycle hooks on the engine traits] (record 1487), the
[Nexus mechanism substrate] (records 1486/1488), and the
[alias-vs-newtype lowering] family (records 1560/1561/1562).

The operator has already landed alias-vs-newtype lowering, bare-name header
namespace resolution, and the end-to-end alias-payload path. This audit is a
completeness-and-quality pass on that landed work, not a greenfield port.

## Headline: the landed mechanisms are clean

Four of the five focus areas are not just present but well-built:

| Mechanism | Intent | State | Verdict |
|---|---|---|---|
| Alias lowering, no wrapper-nesting | 1557/1560/1561 | `pub type Rejected = SignalRejection;` + `Output::rejected(SignalRejection { .. })` | DONE |
| Lifecycle hooks on engine traits | 1487 | `on_start`/`on_stop` on all three traits, wired into `Engine::start/stop` | DONE |
| Daemon binary string boundary | 1490/1492/1495 | binary-only daemon, NOTA gated behind `nota-text`, daemon never enables it | DONE (code) / GAP (witness) |
| Trace is a typed schema interface | 1489/1491 | `TraceEvent(ObjectName)` newtype over closed generated enums | DONE |
| SymbolPath identity space | 1506/1507 | absent entirely | UNRATIFIED-PROPOSE |

### Alias lowering and wrapper-free construction (1557/1560/1561) — DONE

The generated header lowers bare namespace bindings to type aliases exactly as
record 1560 ratifies. `src/schema/lib.rs:80` and `:66`:

```rust
pub type Rejected = SignalRejection;
pub type RecordAccepted = SemaReceipt;
```

and the enum carries the alias directly (`src/schema/lib.rs:403`):

```rust
pub enum Output {
    RecordAccepted(RecordAccepted),   // RecordAccepted = SemaReceipt
    ...
    Rejected(Rejected),               // Rejected = SignalRejection
}
```

The generated constructors take the payload, not a wrapper
(`src/schema/lib.rs:611`):

```rust
pub fn rejected(payload: Rejected) -> Self {
    Self::Rejected(payload)
}
```

The hand-written runtime construction sites are clean — no
`Output::Rejected(Rejected(SignalRejection(...)))` anywhere. `engine.rs:458`:

```rust
impl ValidationError {
    pub fn into_signal_output(self, database_marker: DatabaseMarker) -> Output {
        Output::rejected(SignalRejection {
            validation_error: self,
            database_marker,
        })
    }
}
```

This is precisely the [generated APIs should not force callers to hand-write
that repetition] shape (record 1557) realised, and
[handwritten spirit code avoids nested alias wrapper construction]
(record 1561) holds across `engine.rs`, `nexus.rs`, and `store.rs`. A grep for
double-wrap constructions (`Rejected(Rejected(`, `Output::Rejected(crate`,
`Sent(Sent(`) returns nothing in handwritten code.

### Lifecycle hooks (1487) — DONE, and actually wired

The hooks are not present-but-unused. The generated traits carry default-no-op
`on_start`/`on_stop` returning `Result<(), ActorStartFailure>` /
`Result<(), ActorStopFailure>` (`src/schema/lib.rs:1843-1937`), and `Engine`
wires them in the record-1487 inner-to-outer / outer-to-inner order
(`engine.rs:93`):

```rust
pub fn start(&mut self) -> Result<(), ActorStartFailure> {
    {
        let mut nexus = self.nexus.lock().expect("nexus lock");
        NexusEngine::on_start(&mut *nexus)?;       // Nexus starts its owned SEMA store inside
    }
    SignalEngine::on_start(&mut self.signal_actor)
}
```

`Nexus::on_start` cascades into `SemaEngine::on_start(&mut self.store)`
(`nexus.rs:203`), so the durable-inward ordering (SEMA, then Nexus, then
Signal) is real. `engine_lifecycle_runs_generated_trait_hooks_without_actor_mailboxes`
(`runtime_triad.rs:275`) is the witness that `start`/`stop` run and the engine
still handles a record — though it asserts the Result is `Ok`, it does not
assert the hook *order* (see gaps).

The error types `ActorStartFailure`/`ActorStopFailure` are the real
data-bearing engine-type return per record 1487; they live on real nouns
(`SignalActor`, `Nexus`, `Store`), not on a ZST.

### Daemon binary string boundary (1490/1492/1495) — code DONE, witness GAP

The daemon path touches no string that is not a user-authored payload field.
`daemon.rs` reads a binary `Configuration` (rkyv, `config.rs:68`), opens a
socket, and `handle_stream` reads a length-prefixed binary frame and writes a
binary frame (`daemon.rs:194`):

```rust
fn handle_stream(&self, stream: UnixStream, engine: &Engine) -> Result<(), DaemonError> {
    let mut transport = SignalTransport::new(stream);
    let (_route, input) = transport.read_input()?;     // Input::decode_signal_frame (binary)
    let output = engine.handle(input);
    transport.write_output(output.root())?;            // Output::encode_signal_frame (binary)
    Ok(())
}
```

A grep for `NotaDecode`/`from_nota`/`FromStr`/`Display` across the
daemon-reachable modules (`daemon.rs`, `config.rs`, `store.rs`, `nexus.rs`,
`engine.rs`, `transport.rs`) returns only error-`Display` impls. The
NOTA derives in the generated module are all `#[cfg_attr(feature = "nota-text", ...)]`
gated, and the daemon binary build does not enable `nota-text`. The only
strings the daemon constructs are `ErrorReport.error_message` (a generated
`ErrorMessage = String` payload field) and the user's `Entry.description` — both
[a user-authored payload field], which records 1490/1492/1495 explicitly carve
out.

The witnesses that *exist* are adjacent but indirect:
`tests/dependency_surface.rs` proves `nota-next` is absent from the
`--no-default-features` tree, and `tests/socket_negative.rs` proves the binary
decoder rejects raw NOTA bytes. Neither directly states the intent
[the daemon never decodes NOTA text or sees a string except a user-authored
payload field]. That load-bearing intent has no direct constraint witness (see
gaps + portProposals).

### Trace is a typed schema interface (1489/1491) — DONE

`TraceEvent` is a transparent generated newtype over a closed
generated-enum vocabulary (`src/schema/lib.rs`):

```rust
pub struct TraceEvent(pub ObjectName);

pub enum ObjectName {
    Signal(SignalObjectName),
    Nexus(NexusObjectName),
    Sema(SemaObjectName),
}
```

`trace.rs` implements `TraceEventFrame` (rkyv binary trace frame) and gates the
NOTA `Display`/`FromStr` rendering behind `nota-text` — text only at the
display edge. `triad-runtime` owns the generic in-memory log + socket; spirit
owns the typed `TraceEvent`. This matches [tracing is its own typed
schema-defined interface ... rendered to NOTA only at the client display edge]
(records 1489/1491). Tracing-of-tracing is not enabled. The
process-boundary trace test decodes typed `TraceEvent` frames and asserts an
event *sequence*, not a source grep.

## Gaps — design present in intent, absent or incomplete in code

The numbered gaps below are returned in the structured payload with
classification and concrete proposals. Summary of the load-bearing ones:

1. **Daemon-never-sees-a-non-payload-string has no constraint witness**
   (record 1565). The strongest version of records 1490/1492/1495 is provable
   today and is the kind of constraint record 1565 says to witness. Proposed as
   a tier2 test (a `nm`/symbol scan of the daemon binary asserting no NOTA-decode
   symbol, plus an assertion the binary-only dep tree lacks `nota-next` — the
   latter is half-present). RATIFIED-PORTABLE.

2. **SymbolPath identity space is entirely absent** (records 1506 Maximum /
   1507 High). [Every typed symbol has a fully-qualified identity expressed as a
   SymbolPath; the path mechanism is canonical, not per-design]. Grep for
   `SymbolPath` across `src/`, `schema/`, `build.rs` returns nothing. The
   generated module expresses namespace through Rust module nesting
   (`signal::Input`, `nexus::Work`) and the single-colon import paths in the
   schema (`signal:sema:Magnitude`), but there is no first-class
   `SymbolPath` type that is the [one symbol-path identity space] with the
   schema-Rust and NOTA renderings as two projections. This is a substrate-level
   design (it belongs in `schema-next`/`schema-rust-next`, not hand-written in
   the pilot), so it is OPERATOR-ACTIVE / tier3 — propose, do not port.

3. **Lifecycle hook ORDER is not witnessed** (records 1487 + 1565). The code
   orders SEMA→Nexus→Signal on start and the reverse on stop, but
   `engine_lifecycle_runs_generated_trait_hooks_without_actor_mailboxes` only
   asserts `start()`/`stop()` are `Ok`. In `testing-trace` builds the hooks
   emit `SemaStarted`/`NexusStarted`/`SignalStarted`; a witness asserting that
   exact prefix order proves the record-1487 ordering. The
   process-boundary trace test *tolerates* the prefix
   (`assert_trace_sequence_after_optional_lifecycle_start`) rather than
   asserting it. `instrumentation_logging.rs` is the better home. RATIFIED-PORTABLE
   (tier2 witness over existing typed trace objects).

4. **The runner loop is hand-piloted, not generated** (INTENT.md +
   record 1486/1488). `Nexus::decide` (`nexus.rs:222`) is a hand-written
   `loop` over the 5-variant `NexusAction` (Continue included, matching
   record 1486's [5-variant NexusAction with Continue]). The doc comments are
   honest — [A future schema-rust-next slice should emit this loop directly from
   the schema; today the runner lives here] (`nexus.rs:182`). There is no
   `triad_main!`-style generated runner; the daemon is hand-wired in `Daemon`
   + `DaemonCommand`. INTENT.md §"Daemon startup should move toward a
   generated/programmatic triad runner" already records the destination. This is
   OPERATOR-ACTIVE substrate work (the generated runner lives in
   `schema-rust-next`), tier3 — propose, do not port.

5. **Manifestation: spirit-next/INTENT.md + ARCHITECTURE.md do not name the
   strings-at-edges / trace-edge / SymbolPath / lifecycle intent by its recent
   record framing.** The INTENT.md captures the *mechanics* (binary-only
   daemon, trace as typed `TraceEvent`, lifecycle hooks) thoroughly, but
   pre-dates the apex framing of records 1490/1492/1495/1508
   ([NOTA is a typed text user interface]; [strings only at the edges]) and
   does not mention SymbolPath at all. A small tier1 doc delta naming the
   apex intent is genuinely-missing recent intent. RATIFIED-PORTABLE (doc).

## Bad patterns hunted (the psyche named this explicitly)

1. **`SchemaSourceWitness::must_contain` source-text grep over generated Rust**
   (`tests/operator_271_closed_claims.rs:180-210`). This witnesses alias
   lowering (record 1560) by string-scanning the generated artifact
   (`Rejected(Rejected)`, `pub type Rejected = SignalRejection;`). It is *not*
   the trace-via-source-grep anti-pattern (it scans a build artifact, not
   runtime behavior), and a behavioral twin already exists at
   `process_boundary.rs:217`. But a grep-for-`pub type X = Y` is brittle to
   whitespace/formatting and re-encodes the emitter's spelling into the
   consumer's test. The cleaner witness is a *type-level* assertion that the
   alias is the same type — e.g. a `const _: fn(SignalRejection) -> Rejected = |x| x;`
   identity coercion, which fails to compile if `Rejected` ever becomes a
   newtype. That moves the witness from text to the type system. See badPatterns
   in the payload.

2. **`Daemon::run` constructs the engine and then `Arc`s it but discards
   `stop`** (`daemon.rs:152`). `engine.start()` is called, the engine is
   wrapped in `Arc`, and the accept loop runs forever; `engine.stop()` is never
   reachable (the loop only exits on a listener error, after which `stop` is
   skipped). The lifecycle stop hook (record 1487) is dead on the daemon path —
   it is exercised only in tests. Not a correctness bug for the pilot (process
   exit releases redb), but the [release before notify] discipline
   (`skills/actor-systems.md`) says the stop sequence is part of the design.
   Naming-owner: a `Daemon` shutdown path (signal handler → `engine.stop()`)
   would make the hook live. tier3.

3. **`SpiritNextCli::run` returns `Box<dyn std::error::Error>`**
   (`src/bin/spirit-next.rs:28`). `skills/rust/errors.md` forbids
   `Box<dyn Error>` at boundaries — it erases the typed failure. `main` is the
   one free-function exemption, but `SpiritNextCli::run` is a method and should
   return a crate `Error` enum (the CLI has at least: argument-count,
   not-a-NOTA-value, NOTA parse, transport). The daemon side already does this
   right with `DaemonCommandError`. tier3 (operator feature; the CLI wants a
   typed `Error`).

4. **`ConfigurationPath(String)` has a private field but no validation and a
   lossy constructor** (`config.rs:16`). `ConfigurationPath::new` does
   `path.as_ref().to_string_lossy().into_owned()` — a non-UTF-8 path is silently
   corrupted. `storage-and-wire.md` §"Newtype the wire form" prescribes
   `WirePath(Vec<u8>)` for platform-fragile path types on the wire precisely
   because `to_string_lossy` is non-deterministic across platforms. The
   wire/disk form here is rkyv `Configuration`, so the lossy `String` is a real
   (if narrow) wire hazard. tier3.

5. **`Engine`/`SignalActor`/`Nexus` carry per-field `Mutex` rather than being
   Kameo actors** (`engine.rs:26`, `:34`; `nexus.rs:116`). The pilot is
   explicitly self-contained (ARCHITECTURE.md §"Known limits" names
   `sema-engine`/kameo as the destination), so this is a *named, deferred*
   deviation from `skills/actor-systems.md`, not an unflagged one. No action —
   recorded for completeness; the intent already carries the uncertainty.

## Witness coverage map

| Load-bearing intent | Record | Behavioral witness | Verdict |
|---|---|---|---|
| Alias renders without wrapper repetition | 1560/1561 | `process_boundary.rs:217` | covered |
| Binary decoder rejects NOTA text | 1490 | `socket_negative.rs` | covered |
| `nota-next` absent from daemon dep tree | 1492 | `dependency_surface.rs` | covered |
| SEMA durable across restart | 1007/1008 | `process_boundary.rs:271` | covered |
| Nexus 5-variant runner loop incl. Continue | 1486 | `runtime_triad.rs:153` | covered |
| Lifecycle hooks run | 1487 | `runtime_triad.rs:275` | partial (no order) |
| Daemon never sees a non-payload string | 1490/1492/1495 | none direct | GAP |
| Lifecycle hook ORDER (SEMA→Nexus→Signal) | 1487 | none asserting order | GAP |
| SymbolPath identity space | 1506/1507 | n/a (absent) | GAP |
