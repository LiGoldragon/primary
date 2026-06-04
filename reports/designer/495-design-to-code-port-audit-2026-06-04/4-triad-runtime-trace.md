---
title: "Slice 4 audit — triad-runtime and the trace interface"
role: designer
variant: Audit
date: 2026-06-04
topics: [triad-runtime, trace, typed-interface, strings-at-edges, lifecycle-hooks, symbol-path, doc-manifestation]
description: >
  Read-only design-to-code port audit of triad-runtime's trace
  substrate against the strings-at-edges, typed-trace-interface,
  lifecycle-hook, and SymbolPath intent (records 1487-1565). The
  trace runtime is correctly generic and binary-framed, but the
  closed-vocabulary, engine-trait-hook, and lifecycle-hook intent
  is not yet manifested in this crate, and the docs do not yet
  carry the strings-at-edges / SymbolPath contracts.
---

# Slice 4 — triad-runtime and the trace interface

## What this crate actually is today

The whole production surface is two files: `src/lib.rs` (15 lines,
re-exports only) and `src/trace.rs` (331 lines). There is no
Signal/Nexus/SEMA engine code, no lifecycle hook, no SymbolPath,
no signal transport. The crate is a single concern: a generic
trace-transport library parameterised over a component-owned
`Event` type. Build and tests both compile clean
(`cargo build` + `cargo test --no-run` green).

The central design decision — and it is a good one — is that the
runtime is generic over the event noun. The component owns the
typed event enum and its rkyv codec; the runtime owns only the
log sink, the length-prefixed binary frame, the Unix socket
listener, and a client that renders to text only at `print_events`.
`src/trace.rs:16-22`:

```rust
pub trait TraceEventFrame: Clone + Send + 'static {
    fn to_trace_archive(&self) -> Result<Vec<u8>, TraceError>;
    fn from_trace_archive(archive: &[u8]) -> Result<Self, TraceError>
    where
        Self: Sized;
}
```

This is the correct shape for `triad-runtime` to NOT smuggle
component meaning into the shared runtime: the runtime never sees a
variant name, never decodes NOTA, never holds a string except a
user-authored env var and the `Display` render at the client edge.

## Trace-edge intent: where the code lands and where the gap is

The audit-focus claim was that `ARCHITECTURE.md` describes GENERIC
trace logging while intent wants a typed schema-defined interface
with closed generated enum vocabularies. Reading the code against
the actual ratified intent sharpens this: the gap is real but it is
NOT in this crate's job to close it — the closed vocabulary belongs
to the *component's* schema emission, and triad-runtime is
correctly generic. The precise findings:

| Intent property | Code state | Verdict |
|---|---|---|
| Binary trace frames (rkyv), not text | `TraceFrame::to_bytes` writes a 4-byte big-endian length + rkyv archive bytes (`src/trace.rs:118-127`) | DONE |
| NOTA/text rendered only at the client display edge | Only `TraceClient::print_events` (`src/trace.rs:316-321`) touches `Display`; everything else is typed `Event` | DONE |
| Trace is its own typed interface, closed vocabulary | The runtime is generic over `Event: TraceEventFrame`; the *closed enum vocabulary* is the component's schema emission, not here | DONE-for-this-crate; closed-vocab is OPERATOR-ACTIVE in `schema-rust-next` |
| Instrumentation = hooks on the engine traits, not a side vocabulary (record 1365) | This crate carries NO engine traits and NO hooks; it is pure transport | UNRATIFIED-PROPOSE that a hook-bridge belongs here; conservatively OPERATOR-ACTIVE elsewhere |
| Tracing-of-tracing is not enabled (record 1491) | Trivially satisfied — the runtime cannot trace itself | DONE |

The vocabulary in the test fixture (`tests/trace.rs:43-49`,
`ExampleTraceEvent::new("SignalAdmitted")` etc.) is an *open
string* `struct { name: String }`. That is the test's own toy
type, NOT the production contract — production components supply a
closed schema-emitted enum per record 1400. So the open-string
shape in the test is acceptable, but it is also the only witness
the crate has, which means the crate has **no test proving the
closed-vocabulary path** (see §Constraint witnesses).

The key intent to weigh against the ARCHITECTURE.md framing:
[traceability is expressed as traits on schema-derived interfaces —
and where possible, as methods on the Signal/Nexus/SEMA engine
traits themselves — not as a hand-written or generated event enum
living beside the engines] (record 1365), and [trace names are
macro-emitted from the schema-defined enum variant structure, not
free-floating strings] (record 1400). Both place the *closed typed
vocabulary* and the *engine-trait hooks* upstream of this crate (in
`schema-rust-next` emission and the component crates). triad-runtime
is the transport leg: it carries the archived typed event and never
re-derives the name. That is exactly what the code does. The honest
classification is therefore: the trace-as-typed-interface intent is
**largely DONE for this crate's scope**, and the missing pieces
(closed enum emission, engine-trait hook methods) live in OTHER
slices and are OPERATOR-ACTIVE.

The one genuine within-crate gap is documentary: ARCHITECTURE.md and
INTENT.md do not state the binary-frame / strings-at-edges / NOTA-at-
client-edge contract as a *constraint*; they describe the surface.
That is the highest-value manifestation target (§Doc manifestation).

## Strings-at-edges in the runtime

The directive: find any triad-runtime code that touches strings
that are not user-authored payloads or user-facing display. The
sweep (`grep -n String\|&str\|Display\|writeln` over `src/`):

| Location | String touch | Edge-legitimate? |
|---|---|---|
| `src/trace.rs:79,293-301` `TraceError::Environment { variable: String }` + `from_environment` reads `env::var` | the trace socket path comes from an environment variable | YES — env var is a user-authored configuration edge |
| `src/trace.rs:314-321` `TraceClient::print_events` over `Event: Display` | renders typed events to text | YES — this IS the client display edge |

No string touches the typed interior. `record`, `record_result`,
the frame codec, and the socket listener are all typed-`Event` or
raw bytes. This crate passes the strings-at-edges audit cleanly.
One refinement worth noting under the [Authored data files prefer
typed NOTA, by path convention] (record 1494) and the single-
argument-rule lens: `from_environment(variable: impl Into<String>,
...)` takes the env-var NAME as a runtime string. That is config —
per the NOTA-only-argument-language override, a component's
configuration belongs in its schema, not a free-floating env-var
name. This is a small UNRATIFIED-PROPOSE smell, not a violation
(triad-runtime is a library, not a component binary, so the
single-argument rule does not bind it directly).

## Lifecycle hooks (record 1487)

[Each engine trait carries two lifecycle methods plus typed
failure: on_start -> Result<(), ActorStartFailure>, on_stop ->
Result<(), ActorStopFailure>] (record 1487, component-triad.md
§"Lifecycle hooks on the engine traits"). triad-runtime defines
NO engine traits, so the lifecycle hooks and the
`ActorStartFailure` / `ActorStopFailure` vocabulary are simply
absent here. That is correct: the engine traits are schema-emitted
in `schema-rust-next` and live in component crates (`spirit-next`
is the canonical example). triad-runtime owns transport, not the
engine contract. Classification: DONE-by-absence for this crate;
the lifecycle-hook implementation is OPERATOR-ACTIVE in
`schema-rust-next` / `spirit-next`, audited in those slices.

The one observation worth carrying: the `TraceSocketListener`
(`src/trace.rs:55-62`) is a long-lived resource owner (it binds a
Unix socket, holds the listener handle, cleans up on `Drop` at
`src/trace.rs:324-331`). Under the actor discipline this is exactly
the kind of exclusive-resource owner that release-before-notify and
the lifecycle hooks govern. Today it is a plain struct with a
blocking `accept()` poll loop (`collect_available_event`,
`src/trace.rs:257-268`, with `thread::sleep`). That is acceptable
for a synchronous test-collection client, but if/when the trace
client becomes a supervised daemon plane, this is where the
lifecycle/no-blocking-handler discipline binds. Noted, not a
present violation — the crate is explicitly a sync test/CLI
collection surface.

## SymbolPath (records 1506/1507)

[Every typed symbol has a fully-qualified identity expressed as a
SymbolPath; the path mechanism is canonical, not per-design]
(record 1506). triad-runtime has no SymbolPath and no reference to
it. The trace event identity flows as the component's own typed
`Event` value — which, in the destination design, IS a projection
of a symbol-path identity (a `<Plane>ObjectName` enum variant per
record 1400). The crate is generic over that `Event` and therefore
neither needs nor should hold a SymbolPath. Classification: not
this crate's concern; the SymbolPath manifestation is
OPERATOR-ACTIVE in the schema emission slice.

## Bad-pattern hunt

The crate is small and clean. The honest list:

### No free functions, no ZST namespaces

Every function is a method on a data-bearing type or trait. The
`LENGTH_PREFIX_BYTE_COUNT` const (`src/trace.rs:14`) is a module
constant, not a function — fine. `TraceSocketPath::write_event`
(`src/trace.rs:199-205`) is a method on a real noun (`TraceSocketPath`
carries the `path`). No violations.

### `TraceEventFrame` trait name carries a category suffix smell

`src/trace.rs:16`. The trait is named `TraceEventFrame` but it does
NOT describe a frame — it describes the codec affordance of an
event: "I can archive myself to bytes and back." The `Frame` word
belongs to `TraceFrame` (`src/trace.rs:24-30`), which is the actual
length-prefixed wire object. The trait is really
`TraceEventArchive` or simply the archive-codec affordance. Naming
two adjacent types `TraceFrame` (the wire envelope) and
`TraceEventFrame` (the codec trait) forces the reader to
disambiguate two `*Frame` names that mean different things. Per
`skills/naming.md` §"Anti-pattern: repeated category words across
sibling names": the repeated `Frame` suffix signals the trait's
name took the wrong word. Proposed: rename the trait to
`TraceArchive` (or `ArchivableTraceEvent`) so `Frame` uniquely
names the wire envelope. This is a tier3 rename for the operator.

### `record` / `record_result` is a paired-method shape worth a glance

`src/trace.rs:174-187`. `record` is the silent path; `record_result`
is the fallible path; `record` is literally `let _ =
self.record_result(event);`. This pairing is intentional and
documented in INTENT.md ([The default TraceLog::record path is
silent on delivery failure; callers that need proof use the
fallible record_result method]). It is a legitimate two-method
shape, not repetition — one delegates to the other. No action;
flagged only to confirm it was examined and is sound.

### `TraceClient` split impl blocks

`src/trace.rs:271-310` (the `Event: TraceEventFrame` impl) and
`312-322` (the `Event: TraceEventFrame + Display` impl). This is
the correct Rust idiom for conditioning `print_events` on the
extra `Display` bound — it keeps the typed-collection surface
usable without `Display` and gates only the render method. Good
shape, not a smell.

## Constraint witnesses (record 1565)

[Audit implementation against intent for missing constraint
witnesses; add tests that prove the intended path instead of
leaving intent as prose] (record 1565). The existing test file
`tests/trace.rs` is genuinely good — it has eight tests covering
in-memory recording, disabled-drop, fallible socket-miss, binary
frame round-trip, socket collection (both modes), partial timeout,
disabled client, and the display-boundary render. Notably
`trace_client_prints_typed_events_at_display_boundary`
(`tests/trace.rs:159-181`) IS a strong witness for [rendered to
NOTA only at the client display edge] — it proves typed events
flow over the socket and become text only at `print_events`.

The missing witnesses, against the load-bearing intent:

| Intent | Witness present? | Proposed witness |
|---|---|---|
| Frame bytes are binary, not text — the wire never carries a decodable string | Partial: round-trip proves equality but not that the frame is binary | A test asserting the frame bytes are NOT valid UTF-8 / contain the rkyv archive, proving the wire is binary not text |
| NOTA/text appears ONLY at the client edge, never on the wire | Implicit only | A negative witness: read raw frame bytes off the socket and assert they do not contain the event's `Display` string |
| The runtime is generic and holds no component vocabulary | Compile-time only (the toy `ExampleTraceEvent`) | A second distinct event type in tests, proving the runtime is genuinely generic over the event noun (one type is not a generic-ity proof) |

The first two are the highest-value: they convert the
strings-at-edges intent from prose into a falsifiable test. They
are low-risk tier2 witnesses (see portProposals).

## Doc manifestation — the highest-value target

INTENT.md (30 lines) and ARCHITECTURE.md (66 lines) are thin and,
critically, describe the surface without stating the load-bearing
*constraints* as constraints. The strings-at-edges contract, the
binary-wire contract, and the NOTA-at-client-edge contract are the
crate's reason to exist and are not written as the rule they are.
Proposed substantial additions in portProposals — these are
tier1, RATIFIED-PORTABLE (they manifest records 1490/1492/1495
and 1489/1491, all Maximum/ratified, into the crate's own docs).
```
