# Generated client trace shape audit

*Kind: implementation-shape audit · Topics: spirit-next, schema-rust-next, triad-runtime, client, trace, help, generated interfaces · 2026-06-03 · operator lane*

## Frame

Task: present the current code shape for CLI/client tracing and the clean
generated/generic target shape, with concrete file references and a recommended
implementation slice. No source code was edited.

Fresh intent records 1490-1496 are binding context for this audit:

- 1490: trace remains typed data until the client display boundary.
- 1491: do not enable tracing on the tracing interface itself yet; avoid trace
  recursion.
- 1492: tracing is its own schema-defined interface with closed generated enum
  vocabularies, not an ad hoc string log.
- 1493: help/documentation is schema data in a mirror description namespace.
- 1494: authored workspace data files should prefer typed NOTA data, with the
  file path/name defining the expected root type.
- 1495: daemons stay free of NOTA/string surfaces; clients translate NOTA text
  to binary protocol data and render typed replies/traces for users.
- 1496: context-maintenance agents can recommend intent supersession/removal,
  but deletion remains reviewable and justified.

Latest relevant design state:

- Designer 483 is now stale on where the reusable trace runtime lives: it said
  trace runtime was hand-written in `spirit-next`; operator 291 confirms that
  `triad-runtime` now owns generic trace log/frame/socket/listener mechanics.
- Designer 485 keeps engine traits as the current substrate and adds lifecycle
  hooks instead of full actor-trait promotion.
- Designer 486 chooses schema-carries for the engine mechanism: schema-rust
  plus shared runtime crates should make the daemon/client substrate a reusable
  template.
- Operator 291 leaves the next gap as interface-route trace use: generated
  object names already include routes, but the live runtime mostly records
  actor-boundary events.

## Current code shape

### `triad-runtime`: generic trace mechanics are already extracted

`/git/github.com/LiGoldragon/triad-runtime/src/trace.rs` is now the generic
runtime floor:

- `TraceEventFrame` is the component boundary. A component-generated event
  supplies `to_trace_archive` and `from_trace_archive`
  (`src/trace.rs:16-22`).
- `TraceLog<Event>` is generic over the event type and supports disabled,
  recording, and socket destinations (`src/trace.rs:32-48`,
  `src/trace.rs:145-190`).
- `TraceFrame<Event>` owns length-prefixed binary trace framing
  (`src/trace.rs:102-143`).
- `TraceSocketListener<Event>` owns Unix socket binding and event collection
  (`src/trace.rs:210-271`).
- `TraceClient<Event>` owns client-side optional listener setup from an
  environment variable and printing through the component-supplied display
  adapter at the client boundary
  (`src/trace.rs:64-70`, `src/trace.rs:273-321`).

This is clean relative to intent 1490/1495: the runtime stays generic and
binary; text rendering is only the client display edge. In the current
`spirit-next` adapter, that display edge renders generated NOTA.

Remaining weakness: `TraceEventFrame` still requires each component to provide
the tiny rkyv archive impl, and `TraceClient<Event>` requires a display adapter
for printing. That is acceptable as a transitional component-specific adapter,
but the generated event type is already known enough for schema-rust-next to
emit the rkyv frame impl plus the NOTA display/parse impls automatically.

### `schema-rust-next`: typed trace object names and route enums are generated

`/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs` emits the core typed
trace/interface support:

- NOTA text support for CLI roots is feature-gated via `FromStr` and
  `Display` emission (`src/lib.rs:1028-1057`).
- short headers and signal frame encode/decode are generated for root enums
  (`src/lib.rs:1065-1118`, `src/lib.rs:1163-1263`).
- route enums are generated for Signal roots and plane roots
  (`src/lib.rs:1121-1137`).
- typed trace support emits per-plane object-name enums, umbrella
  `ObjectName`, and `TraceEvent` (`src/lib.rs:1265-1339`).
- trace object-name rendering is still generated as a `name() -> &'static str`
  method for tests and compact inspection (`src/lib.rs:1341-1385`), but the
  client display target is now generated NOTA for the full `TraceEvent`.
- generated engine traits include lifecycle hooks plus trace hooks/wrappers
  (`src/lib.rs:2140-2307`).

The current tests prove this generated shape, especially
`/git/github.com/LiGoldragon/schema-rust-next/tests/emission.rs:270-436`
for engine/route/trace emission and
`tests/emission.rs:438-455` for typed trace identity archiving.

Remaining weakness: this generator still emits no generic client trait or
client adapter surface. It emits `Input::FromStr`, `Output::Display`,
`TraceEvent`, and signal frame methods as separate pieces, but it does not
assemble them into a generated client interface like "parse one NOTA request,
send one binary Signal frame, print one typed Output, optionally print typed
trace events." That composition is still hand-written in component CLI code.

### `spirit-next`: current component-specific client trace adapter is small but real

`/git/github.com/LiGoldragon/spirit-next/src/trace.rs` now contains only the
component adapter:

- `TraceLog` and `TraceSocketListener` are type aliases to
  `triad-runtime` instantiated with generated `TraceEvent`
  (`src/trace.rs:3-7`).
- `TraceEventFrame` is implemented by archiving/decoding the generated
  `TraceEvent` through rkyv (`src/trace.rs:9-20`).
- `Display for TraceEvent` renders generated NOTA, and `FromStr` parses that
  NOTA back into `TraceEvent` (`src/trace.rs:21-35`).

This is the right boundary, but it is mechanically derivable from the generated
event type. It should become generated support rather than repeated per
component.

`/git/github.com/LiGoldragon/spirit-next/src/bin/spirit-next.rs` still owns the
component CLI template:

- `SpiritNextCli` reads argv and enforces exactly one argument
  (`src/bin/spirit-next.rs:17-29`, `src/bin/spirit-next.rs:44-49`).
- it decides inline NOTA vs path by checking whether the argument starts with
  `(` or exists on disk, then reads text (`src/bin/spirit-next.rs:51-58`).
- it parses that text into generated `Input` via `FromStr`, connects through
  `SignalTransport`, prints generated `Output`, then optionally prints trace
  events (`src/bin/spirit-next.rs:31-40`).

This satisfies the current live component, but the shape is a component-local
copy of the generic client template. It also hard-codes the trace environment
variable name and collection duration in the component binary
(`src/bin/spirit-next.rs:35-36`).

`/git/github.com/LiGoldragon/spirit-next/src/schema/lib.rs` shows what the
generated side already knows:

- `InputRoute`, `OutputRoute`, all plane route enums, and route methods are
  generated (`src/schema/lib.rs:1227-1493`).
- `SignalObjectName`, `NexusObjectName`, `SemaObjectName`, `ObjectName`, and
  `TraceEvent` are generated typed trace data (`src/schema/lib.rs:1495-1654`).
- `SignalEngine`, `NexusEngine`, and `SemaEngine` carry lifecycle and trace
  hook wrappers (`src/schema/lib.rs:2026-2120`).

Runtime use in `spirit-next` is still mostly actor-boundary trace:

- `SignalActor::trace_signal_activation` records generated object names
  (`src/engine.rs:209-235`).
- `Nexus::trace_nexus_activation` records generated object names, while the
  hand-piloted recursive runner handles NexusWork/NexusAction
  (`src/nexus.rs:202-270`).
- instrumentation tests assert typed actor-boundary events like
  `SignalAdmitted`, `NexusEntered`, and `SemaWriteApplied`
  (`tests/instrumentation_logging.rs:40-109`), and lifecycle events
  (`tests/instrumentation_logging.rs:111-142`).

The generated route object names such as `SignalObjectName::Input(InputRoute)`
and `NexusObjectName::Action(NexusActionRoute)` exist, but the live runtime
does not yet consistently record them around interface route activation.

## Clean generated/generic target shape

The target should split responsibilities this way:

1. `schema-rust-next` emits component-specific typed nouns and component-specific
   adapter impls for those nouns.
2. `triad-runtime` owns generic runtime/client machinery over traits.
3. `spirit-next` keeps only domain algorithm code plus one-line or near-one-line
   binaries.

Concrete target surfaces:

### Generated trace adapter

For every generated `TraceEvent`, schema-rust-next emits:

- `impl triad_runtime::trace::TraceEventFrame for TraceEvent`, using the same
  rkyv archive/decode body now hand-written in `spirit-next/src/trace.rs:9-20`.
- `impl Display for TraceEvent`, rendering through the generated NOTA encoder,
  plus `impl FromStr for TraceEvent` through the generated NOTA decoder.
  `TraceEvent::name()` remains only a compact inspection/test helper, not the
  client display surface.

That lets a component delete its local `src/trace.rs` except possibly for
public type aliases. If type aliases are still useful, the generator can emit:

```text
pub type TraceLog = triad_runtime::trace::TraceLog<TraceEvent>;
pub type TraceClient = triad_runtime::trace::TraceClient<TraceEvent>;
pub type TraceSocketListener = triad_runtime::trace::TraceSocketListener<TraceEvent>;
```

Those aliases belong in the generated schema module or a generated
`trace_runtime` module, not hand-written component source.

### Generic text client through `triad-runtime`

Spirit 1514 chooses the generic CLI trace-siting path: the reusable client
helper lives in `triad-runtime`, not as a schema-rust-next emitter mixin and not
as per-component CLI code. `triad-runtime` should own a generic client object
over the generated traits:

- request root: `FromStr` under the text-client feature;
- reply root: `Display` under the text-client feature;
- binary transport: generated frame encode/decode or a small `SignalFrame`
  trait;
- optional trace client: `TraceClient<TraceEvent>` when tracing is enabled.

The component binary should collapse toward:

```text
fn main() {
    client_main!(spirit_next::Input, spirit_next::Output, spirit_next::SignalTransport);
}
```

or a data-bearing generated `ClientCommand<Input, Output, TraceEvent>` call.
The exact syntax can be macro or data-bearing object; the important point is
that the component does not re-implement argv shape, NOTA/path reading,
socket-env lookup, binary exchange, output printing, and trace printing.

Intent 1495 says daemons avoid NOTA and strings; it does not prohibit clients
from parsing NOTA. So the generic client lives at the text boundary and remains
feature-gated. The daemon path remains binary configuration plus binary Signal
frames.

Trace enablement is per case, not global. Lean packages collect no trace;
trace-enabled daemon packages may emit binary trace frames but never print
fallback strings; trace-enabled clients render typed trace events as generated
NOTA or store them through a trace/introspect SEMA surface; the trace interface
itself remains untraced unless a future recursion policy explicitly enables it.

### Generated help/documentation data

Intent 1493 changes the help target: help is not a CLI-only string table. The
schema should carry a mirror description namespace over fully qualified
symbols, with generated defaults when explicit descriptions are absent.

Target shape:

- schema-rust-next emits a typed `DescriptionNamespace` or `HelpCatalog`
  generated from schema symbols and optional description data;
- each root/route can expose a help/documentation object such as
  `InputRoute::Record.description(&HelpCatalog) -> Description`;
- the client renders help from typed help objects only at the display boundary;
- daemons do not parse help NOTA or render help strings.

This pairs with intent 1494: typed NOTA data files can hold authored help
descriptions, with file paths defining the expected root type. The help data
should be loaded by schema/build/client-side support, not by daemon runtime.

### Trace as its own schema-defined interface

Intent 1492 says trace is its own schema-defined interface. The target is not
"trace is just an extra log stream." Trace should eventually have a generated
trace interface with closed request/reply/event vocabularies, but intent 1491
requires not recursively tracing that interface yet.

Near target:

- keep `TraceEvent` as generated closed typed data;
- keep `triad-runtime` as generic transport over that event;
- add a generated marker/configuration path that says the trace interface does
  not itself emit trace events in this slice.

Do not add trace-of-trace hooks until the recursion policy is designed.

## Recommended implementation slice

The smallest useful slice is not the full `triad_main!`/`client_main!` system.
It is a generated trace-client adapter slice that removes the last mechanical
component-specific trace code while preserving the current runtime behavior.

### Slice 1: generated `TraceEventFrame` + NOTA display/parse

Implement in `schema-rust-next`:

- extend `emit_trace_support` so after generated `TraceEvent` it emits:
  `impl triad_runtime::trace::TraceEventFrame for TraceEvent`;
- emit `impl Display for TraceEvent` through the generated NOTA encoder and
  `impl FromStr for TraceEvent` through the generated NOTA decoder;
- feature-gate or dependency-gate this only for schemas/components that opt into
  trace runtime support, so non-trace components do not need `triad-runtime`;
- add an emission test alongside
  `tests/emission.rs:438-455` proving generated `TraceEvent` archives through
  the emitted trait, formats as canonical NOTA, and parses that NOTA back into
  the same typed event.

Then in `spirit-next`:

- delete the hand-written `TraceEventFrame`, `Display`, and `FromStr` impls in
  `src/trace.rs`;
- keep only aliases if needed, or replace uses with generated aliases;
- run the existing `testing-trace` tests, especially
  `tests/instrumentation_logging.rs` and
  `tests/process_boundary.rs::cli_receives_testing_trace_events_from_daemon_trace_socket`.

This slice is safe because it changes only mechanical adapter code. It does
not change runtime trace emission, event content, socket framing, CLI
collection, or the daemon binary boundary.

### Slice 2: generic `ClientCommand` / `TraceClient` wiring

After Slice 1, move the component CLI template out of `spirit-next`:

- add a data-bearing `ClientCommand<Request, Reply, Event, Transport>` in
  `triad-runtime` or generated support;
- make it own argv/env reading, NOTA/path read, binary exchange, reply print,
  and optional trace print;
- generate or require a small trait for request parse/reply display/transport
  exchange;
- convert `src/bin/spirit-next.rs` from `SpiritNextCli` to one generated or
  generic call.

Witness: process-boundary tests still parse CLI stdout through generated
`Output::FromStr`, and trace-enabled CLI still prints typed trace names after
the ordinary Signal reply.

### Slice 3: route trace wiring

Once the client adapter is generic, wire existing route object names into the
runtime trace path:

- `SignalEngine::triage` can record `SignalObjectName::Input(input.root().route())`
  before or alongside `Triaged`;
- `SignalEngine::reply` can record `SignalObjectName::Output(output.root().route())`;
- `NexusEngine::execute` can record `NexusObjectName::Work(input.root().route())`
  and `NexusObjectName::Action(output.root().route())`;
- `SemaEngine::apply/observe` can record write/read input/output routes.

This should be generated wrapper behavior, not per-runtime actor code. Tests
should assert both actor-boundary and interface-route events. That directly
closes operator 291's remaining gap.

### Slice 4: typed help catalog

Only after the trace/client substrate is less component-specific, add help:

- extend schema data with a description namespace;
- emit default help objects from symbol names;
- add explicit fixture data for descriptions;
- make client help rendering consume generated help objects.

Do not add daemon help parsing or string tables.

## Recommendation

Take Slice 1 first. It is the cleanest pressure-relief point:

- it directly manifests intent 1490 and 1492 by keeping trace typed and closed;
- it respects intent 1491 by not changing trace recursion;
- it moves code in the direction designer 486 chose (schema-carries) without
  reopening the engine substrate;
- it is a small, testable replacement for exactly the component adapter now
  visible in `spirit-next/src/trace.rs`;
- it sets up Slice 2, where the `spirit-next` CLI stops being a local template.

Do not start with help. Help depends on the schema description namespace design
from intent 1493 and needs a typed data-file convention from 1494. Trace adapter
generation is already fully specified by the current generated `TraceEvent`
and existing `triad-runtime` trait.

Do not start with route trace wiring either. The existing route object names
are ready, but the generic client/trace adapter should land first so later
route traces do not require more component-specific print/listen/test glue.
