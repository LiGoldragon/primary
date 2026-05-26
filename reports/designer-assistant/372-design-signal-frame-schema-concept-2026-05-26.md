# 372 — design-signal-frame-schema concept

*Designer-assistant concept proving a root-level `signal-frame.schema`
can declare frame primitives (framing + short-header dispatch + route
enum + codec object) that component schemas inherit via ImportAll.
Closes the P1 gap from
`reports/operator/208-schema-stack-missing-implementation-audit-2026-05-26.md`:
spirit-next hand-writes the route table and frame codec in
`transport.rs`; with this concept those become schema-derived.
Per psyche 2026-05-26 (intent records 860-861).*

## Frame

Two intent records this turn:

- **Record 860**: *"a proper signal-frame defined in a root-level
  schema frame — can it live in signal repo, if it's not used now?
  or something else? — do a concept that uses this approach."*
- **Record 861**: *"do a concept"* (operational directive).

The `/208 P1` gap (cited verbatim from operator's audit):

> `spirit-next/src/transport.rs:13` defines `InputRoute` manually, and
> `spirit-next/src/transport.rs:97` through `:127` hand-map generated
> `Input` / `Output` variants to short-header constants. The frame
> encoder and decoder are also hand-written in `:137` through `:211`.
> ... **the runtime route table still needs manual edits. That is the
> main interface-generation gap.**

This concept proves the route table + frame codec CAN be derived from
schema, and recommends a production home for the schema declaring them.

## What landed

**Repo**: `https://github.com/LiGoldragon/design-signal-frame-schema`
(public; per `skills/double-implementation-strategy.md` `design-`
prefix; deletes when the concept integrates into operator's
`schema-rust-next` main).

**Commit**: `91248f86aa39` on `main` — pushed to origin.

**File inventory**:

| Path | Role |
|---|---|
| `schema/signal-frame.schema` | The root-level frame-primitives schema |
| `schema/spirit-min-with-frame.schema` | Example consumer (`ImportAll`) |
| `src/hand_rolled_emission.rs` | What `schema-rust-next` WOULD emit (line-annotated with emission state) |
| `tests/round_trip.rs` | 8-test demonstration of the codec chain |
| `INTENT.md` | Repo intent + deletion target |
| `ARCHITECTURE.md` | Shape of the concept |
| `README.md` | Provenance + status |

**Empirical witness**: `cargo test` — 8/8 passing locally.

## signal-frame.schema declaration (the actual NOTA)

```nota
;; signal-frame.schema — root-level frame-primitives schema.
;; Four-section root struct (record 805 + /361 §5 + /367 §3.1):
;;   1. Imports     — empty (no external dependencies)
;;   2. Inputs      — empty (signal-frame declares no surfaces)
;;   3. Outputs     — empty (same)
;;   4. Namespace   — frame primitives + macro signatures

{}

[]

[]

{
  Frame (LengthPrefix ShortHeader Payload)

  LengthPrefix (BigEndianU32)
  ShortHeader (LittleEndianU64)
  Payload (Bytes)

  Bytes (Vec U8)
  BigEndianU32 (U32)
  LittleEndianU64 (U64)
  U8 (Scalar)
  U32 (Scalar)
  U64 (Scalar)

  Route (Macro SurfaceEnum RouteEnum)
  SignalCodec (Macro Surface Codec)

  FrameError (FrameTooShort FrameTooLarge UnknownShortHeader HeaderMismatch ArchiveEncode ArchiveDecode)
}
```

Key choices:

- **Frame** is declared as a positional struct (`LengthPrefix ShortHeader Payload`) — three fields in wire order. Operator's existing four-section root pattern (record 805) applies; the `Frame` declaration is just one entry in the namespace.
- **Route** and **SignalCodec** are declared as `Macro` variants. Per record 843 macros live in the namespace alongside ordinary types — this entry tells the schema engine "when you see a surface enum, derive a Route enum; when you see a component schema importing me, derive a SignalCodec object."
- **FrameError** is an ordinary enum-variant emission. Nothing engine-special.

## Example consumer (spirit-min-with-frame.schema)

```nota
{
  SignalFrame (ImportAll [../signal-frame/signal-frame.schema])
}

[
  (Input (Record Entry) (Observe Query))
]

[
  (Output (RecordAccepted RecordIdentifier) (RecordsObserved RecordSet) (Error ErrorMessage))
]

{
  Topic [Text]
  Description [Text]
  ErrorMessage [Text]
  RecordIdentifier [Integer]
  Entry [Topic Description]
  Query [Topic]
  RecordSet [Entry]
}
```

The consumer authors **only the data shape**. The Route enums + the
SignalCodec object materialise from the imported macros. The
consumer's `transport.rs` shrinks to a thin caller of the generated
codec (or disappears entirely if the codec is the only frame surface).

## Emitted Rust (what schema-rust-next would produce, hand-rolled now)

The full hand-rolled emission is at
`/git/github.com/LiGoldragon/design-signal-frame-schema/src/hand_rolled_emission.rs`.
Each section is annotated with one of three emission-state tags:

- `@emitted-today` — operator's `schema-rust-next` HEAD already produces this (data types, short-header module, NOTA codec impls).
- `@hand-rolled-new` — proposed new emission from this concept (Route enums, SignalCodec object, FrameError, method blocks on Input/Output).
- `@manual-stand-in` — substituted-for-rkyv glue (this repo uses a trivial length-prefixed string encoder so the test compiles without rkyv; the codec method SHAPES are the design intent, not the payload encoder).

The new emission, in shape:

```rust
// @hand-rolled-new : Route<Surface> enums
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum InputRoute { Record, Observe }

impl InputRoute {
    pub fn short_header(self) -> u64 { /* match -> short_header::* */ }
    pub fn try_from_short_header(header: u64) -> Result<Self, FrameError> { /* inverse */ }
}

// @hand-rolled-new : method block on Input (frame-aware)
impl Input {
    pub fn route(&self) -> InputRoute { /* variant -> route */ }
    pub fn short_header(&self) -> u64 { self.route().short_header() }
    pub fn encode_frame(&self) -> Result<Vec<u8>, FrameError> { ... }
    pub fn decode_frame(frame: &[u8]) -> Result<(InputRoute, Self), FrameError> { ... }
}

// @hand-rolled-new : SignalCodec object (the apex codec)
#[derive(Clone, Copy, Debug, Default)]
pub struct SignalCodec;

impl SignalCodec {
    pub fn encode_input(self, input: &Input) -> Result<Vec<u8>, FrameError> { ... }
    pub fn decode_input(self, frame: &[u8]) -> Result<(InputRoute, Input), FrameError> { ... }
    pub fn encode_output(self, output: &Output) -> Result<Vec<u8>, FrameError> { ... }
    pub fn decode_output(self, frame: &[u8]) -> Result<(OutputRoute, Output), FrameError> { ... }
    pub fn write_length_prefixed(self, writer: &mut impl Write, frame: &[u8]) -> Result<(), FrameError> { ... }
    pub fn read_length_prefixed(self, reader: &mut impl Read) -> Result<Vec<u8>, FrameError> { ... }
}
```

The codec is a unit struct following the same shape as
`schema-rust-next::RustEmitter`. State-aware variants (e.g. a codec
carrying a process-origin tag) become a future extension when the
caller-identification library lands (record 854 sub-claim).

## Round-trip test demonstration

`tests/round_trip.rs`, 8 tests, all passing:

| Test | Asserts |
|---|---|
| `input_record_round_trip` | `Input::Record` encodes, decodes, route matches, header matches constant |
| `input_observe_round_trip` | Same for `Input::Observe` |
| `output_record_accepted_round_trip` | Same for `Output::RecordAccepted` |
| `output_records_observed_round_trip` | Same for `Output::RecordsObserved` |
| `output_error_round_trip` | Same for `Output::Error` |
| `route_enum_encoding_matches_short_header_constants` | EVERY route's `short_header()` equals the corresponding `short_header::*` constant |
| `try_from_short_header_round_trips` | Every header decodes back to its route |
| `length_prefixed_codec_round_trip` | The wire-format `write_length_prefixed` + `read_length_prefixed` chain round-trips through `Cursor` |

```text
running 8 tests
........
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

The route-enum-matches-short-header test (test #6 in the table)
is the critical structural witness: it pins the contract that the
Route emission and the existing `short_header` module emission stay
in lock-step. If the emitter ever drifts on either side, this test
fails.

## Home recommendation

The psyche asked: existing `signal` repo, existing `signal-frame`
repo, new dedicated repo, or built into `schema-rust-next` as
primitives?

**Designer recommendation: option (b) — the existing
`LiGoldragon/signal-frame` repo, after retiring its current
contents.**

Reasoning, with the rejected alternatives' tradeoffs:

| Option | Verdict | Reasoning |
|---|---|---|
| (a) Existing `signal` repo | Reject | `signal.concept.schema` is a one-file stub covering signal-channel concepts not yet load-bearing. Moving signal-frame INTO this repo conflates two distinct concepts (the channel + the frame protocol). Per intent record 856's runtime triad framing, the signal LAYER and the signal FRAME are different — the repo's name should reflect just one. |
| **(b) Existing `signal-frame` repo (retire current contents)** | **RECOMMENDED** | Repo name already matches the concept. Current contents (the `signal_channel!` macro infrastructure) are being retired per the migration to the schema-driven stack. Retiring those alongside introducing the schema-derived approach is structurally clean: one repo's purpose shifts from "macro-based signal-frame protocol" to "schema-derived signal-frame protocol." The git history preserves the predecessor for archaeological reference. |
| (c) New dedicated repo (`signal-frame-schema`) | Defer | Adds a repo to the workspace surface every agent reads. The name overlap with `signal-frame` is confusing. Justified ONLY if `signal-frame` repo carries production traffic that can't retire cleanly — verified-false: current `signal-frame` carries no production consumer per `/208 P1` (everything spirit-next-side is hand-rolled). |
| (d) Built into `schema-rust-next` as primitives | Reject for the macros + schema; partial-accept for scalars + Vec/Option | Per record 843 the SCALAR primitives (U8, U32, U64, Vec, Option) ARE engine built-ins — those belong in `schema-rust-next` (or its sibling `schema-next`). But the FRAME primitives (Frame struct, Route macro signature, SignalCodec macro signature) are not engine-universal — they're specific to the signal layer. Mixing them into `schema-rust-next` couples the emitter to one transport pattern; keeping them in a schema file keeps them introspectable as NOTA and replaceable when the transport pattern evolves. |

**Migration shape if psyche approves (b)**:

1. Retire `signal-frame` repo's current `macros/`, `src/`, `schema-rust/`, `signal_channel!` infrastructure (per `/208`'s implicit retirement of hand-rolled approaches).
2. Replace with the `signal-frame.schema` from this design repo plus an `INTENT.md` documenting the shift.
3. `schema-rust-next` learns to consume `signal-frame.schema` per the ImportAll pattern.
4. `spirit-next/build.rs` updates to import `signal-frame.schema` into its schema-engine namespace before lowering `spirit.schema`.
5. `spirit-next/src/transport.rs` shrinks to a thin caller of the generated `SignalCodec` methods.
6. This design repo (`design-signal-frame-schema`) deletes per the deletion discipline.

## What's built-in vs importable

Per record 843 + `/367 §4` (macros are variants in the same namespace
as scalars), the engine's namespace already mixes built-ins and
imports. The cut for signal-frame primitives:

| Primitive | Layer | Why |
|---|---|---|
| `U8`, `U32`, `U64`, `Vec`, `Option` | **Built-in macros of the schema engine** (i.e. `schema-next` / `schema-rust-next` knows these without import) | They're universal scalar plumbing. Every schema needs `Vec` and `Option`; making them imports adds boilerplate without flexibility (per `/206 P0 #1` — vector + option type references are the immediate next emission slice). |
| `Frame` struct (length-prefix + short-header + payload positional shape) | **Importable from `signal-frame.schema`** | Specific to the wire protocol; not universal. Future federation may want alternate framings; keeping the shape in NOTA makes it replaceable. |
| `ShortHeader` (u64 newtype) | **Importable from `signal-frame.schema`** | The 64-bit per-surface-per-variant convention is one specific dispatch encoding. Keep it inspectable. |
| `Route` macro (per-surface derivation) | **Importable from `signal-frame.schema`** | The macro signature is signal-frame-specific; the derivation rule (variant name → constant name → header value) is the whole point of declaring it in NOTA. |
| `SignalCodec` macro (per-component object emission) | **Importable from `signal-frame.schema`** | Same — the macro emits methods specific to the imported surfaces; declaring it in NOTA documents the contract. |
| `FrameError` enum | **Importable from `signal-frame.schema`** | Ordinary enum-variant emission; nothing engine-special; lives with the other frame primitives. |

The designer-lean: **the schema engine knows scalars + Vec + Option
as built-ins; everything frame-shaped lives in `signal-frame.schema`**.
This keeps the engine's built-in surface minimal and the frame protocol
introspectable as ordinary NOTA.

## Open shape questions for psyche

### Q1 — Is option (b) (retire current `signal-frame` repo contents + adopt the schema) the right move?

Verified false alternatives: (a) signal repo conflates concepts; (c)
new repo adds workspace surface; (d) `schema-rust-next` couples the
emitter to one transport pattern. Designer-lean is (b). Psyche locks.

### Q2 — Does the `Macro` declaration form (`Route (Macro SurfaceEnum RouteEnum)`) match the intended NOTA syntax for declaring macro signatures?

Per record 843 macros live in the namespace as ordinary entries. This
concept proposes the form `<MacroName> (Macro <InputShape> <OutputShape>)`
— the Macro tag tells the engine "this is a macro, not an alias." An
alternative form is `<MacroName> (...)` where the engine resolves the
shape contextually (record 842's shape-driven node-type matching).
The current concept goes with the explicit `Macro` tag for
introspectability; the contextual form is also viable. **Psyche pick**.

### Q3 — Should the `Frame` shape (length-prefix + short-header + payload) ITSELF be declared in `signal-frame.schema`, or be a built-in macro of the engine?

The concept declares it in the schema. The argument for built-in: the
length-prefix-then-header-then-payload pattern is so universal it
might as well be engine-known. The argument for schema: keeps the
wire format inspectable in NOTA + replaceable if federation later
introduces alternate framings.

### Q4 — Does the SignalCodec's surface-agnostic `write_length_prefixed` + `read_length_prefixed` belong on the codec, OR is the codec strictly typed-surface-only and the wire I/O lives elsewhere?

The concept attaches them to the codec for ergonomic colocation. An
alternative: the codec is strictly type-level (encode/decode bytes ↔
typed values) and the wire I/O is a separate `FrameWriter` / `FrameReader`
emitted from `signal-frame.schema`. Both work; the concept's choice
keeps the consumer's `transport.rs` to the smallest surface.

### Q5 — Does the codec need state for caller/process-origin (record 854 sub-claim) NOW, or does state-awareness wait until the caller-identification library lands?

Concept defers: the `SignalCodec` is a unit struct. State-aware variants
attach per the future library. Psyche may want to scope the caller-id
substrate alongside the schema-derived codec; carry as Medium-uncertainty.

## Worktrees touched

This subagent was dispatched from the designer prime; it did NOT
create a new worktree. The work landed:

- `/git/github.com/LiGoldragon/design-signal-frame-schema` — new design repo (commit `91248f86aa39` on `main`, pushed to origin)
- `/home/li/primary/reports/designer-assistant/372-design-signal-frame-schema-concept-2026-05-26.md` — this report (commits to `primary` main)

No edits to `spirit-next`, `signal-frame`, `signal`, or `schema-rust-next`
repos. The concept is non-invasive by design — it exists for psyche
to evaluate the shape before any operator-track integration.

## References

- `/home/li/primary/reports/operator/208-schema-stack-missing-implementation-audit-2026-05-26.md` §P1 — the gap being closed (hand-rolled InputRoute + input_short_header + frame encoder/decoder)
- `/home/li/primary/reports/designer/371-signal-executor-sema-runtime-triad-and-federation-2026-05-26.md` §2 — the signal layer's responsibilities (where the frame lives)
- `/home/li/primary/reports/designer/367-nota-as-specification-superset-of-capnproto-2026-05-26.md` §4 — macros as variants in the same namespace
- `/home/li/primary/reports/designer/370-implementation-gap-audit-designer-side-2026-05-26.md` §4.3 + §4.4 — record 854 (signal-frame protocol on root object) + record 855 (change-loop)
- `/git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/spirit_generated.rs` — the empirical baseline this concept extends
- `/git/github.com/LiGoldragon/spirit-next/src/transport.rs` — the hand-rolled code this concept proposes to replace
- `/home/li/primary/skills/double-implementation-strategy.md` — the design-prefix discipline this repo follows
- `/home/li/primary/skills/major-break-via-new-repo.md` — discipline for the production home migration (if psyche approves option (b))
- Intent records 860-861 (this turn's captures driving the concept)
- Intent records 805, 843, 853, 854, 855 (the schema-shape lineage)
