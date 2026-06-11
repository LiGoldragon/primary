# The component two-client pattern — library + generated binding

Ratified (`8bwo`): every component exposes its two contracts as two thin CLI clients —
`<component>` (working signal) and `meta-<component>` (meta policy signal) — as one extracted
pattern across all components, minimal per-component hand-coding. Spirit's `spirit`/`meta-spirit`
is the first instance. The psyche's question: macro, library, or both?

## Answer: both — but they're layers, not alternatives

- **Library = the engine. It holds 100% of the logic.** Connect to the daemon socket, encode the
  typed signal (NOTA → rkyv), send the frame, receive, decode (rkyv → NOTA), render to stdout,
  handle errors and subscription streams. Generic over the component's `<Signal, Reply>` types.
  Written and tested **once**.
- **Generation = the per-component binding.** Each component's two `fn main()`s —
  `<component>` and `meta-<component>` — are emitted by schema-rust-next from the component's
  signal and meta-signal schemas. Each binding supplies only four things: the Signal type, the
  Reply type, the socket path, and the name. **Per-component hand-coding is zero.**
- **A declarative macro is the *shape* of that binding, not a place logic lives.** The generator
  can emit a one-line `signal_client_main!(SpiritSignal, SpiritReply, …)` (or the expanded `main`
  directly). A macro that expanded the whole engine would duplicate code per binary, resist unit
  testing, and violate the workspace rule that schema emits into impls over real types — so the
  macro/main is a thin call into the library, never the engine.

Single mental model: **one shared client library + a generator that stamps each component's two
mains over it.** "Macro" is just the convenient form the stamped-out main can take.

## This is mostly factoring what already exists

The current `spirit` bin already imports `SignalTransport` (the connect/send/receive engine) and
`ComponentArgument` (the "one NOTA string / NOTA file / rkyv file" parser, per the
exactly-one-argument override). So the engine nucleus is built — it's just bound into the
`spirit` bin rather than lifted into a cross-component crate generic over `<Signal, Reply>`. The
extraction:

1. **Promote** `SignalTransport` + `ComponentArgument` into a standalone `signal-client` library
   crate, generic over the signal/reply types.
2. **Generate** the two mains per component from its two schemas, calling that library.
3. **Retire** the hand-written per-component bins — including `spirit-write-configuration`, which
   the generated `meta-spirit` replaces.

## Fit with the hard rules

- **Method-only rule:** the engine is methods on a data-bearing `Client<Signal, Reply>` (it owns
  the socket/transport/codec state) — not free functions. Each client binary is a `fn main()`,
  which is one of the two explicit free-function exemptions. Clean fit.
- **Exactly-one-argument:** each client takes one NOTA string, one `.nota` file, or one rkyv file
  (the existing `ComponentArgument`). No flags.
- **Daemons never parse NOTA:** the *client* encodes NOTA → rkyv and sends a binary frame; the
  daemon only ever sees rkyv. The two-client split is exactly the NOTA-stays-client-side boundary
  made structural — `meta-<component>` encodes meta-signals to rkyv just as `<component>` encodes
  working signals.

## What it produces — a uniform component surface

Every component becomes: **one daemon + two generated thin clients (working + meta) over one
shared library.** The triad's two contracts each get a first-class client, generated, identical
in shape across `spirit`, `agent`, and every future component. Adding a component means writing
its two schemas; the daemon, the two clients, and their codecs all follow from generation.

## Ownership

Spans the schema stack: the new `signal-client` library (promote existing transport types),
schema-rust-next (emit the two mains from the signal + meta-signal schemas), and each component
(drop hand-written client bins for generated ones). Operator + schema-stack implementation against
this designer spec. Independent of the corpus rebuild — it's the mechanism that makes
`meta-spirit` (hence the privileged `Import`) exist, so it sequences *before* the re-import step.
