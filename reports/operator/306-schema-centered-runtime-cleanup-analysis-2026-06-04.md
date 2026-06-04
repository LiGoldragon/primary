# Schema-Centered Runtime Cleanup Analysis

Context-maintenance note, 2026-06-04: this report remains useful for the
frame/argument/thiserror rationale and sequencing, but the execution status is
stale. `triad-runtime` main commit `6daf2954` landed
`LengthPrefixedCodec`, `ComponentCommand`, and `ComponentArgument`, and
`spirit` main commit `6a339e20` consumes those while routing storage through
`sema-engine`. The remaining cleanup target here is the thiserror/error-boundary
work. See
`reports/operator/307-context-maintenance-spirit-schema-sema-current-state-2026-06-04.md`.

Date: 2026-06-04

Role: operator

Intent anchor: Spirit record `2548` captures the durable reporting direction:
operator and designer reports should increasingly foreground schema as an
explanatory lens, repeatedly showing authored schema input, generated output,
and the runtime implementation or trade each schema shape creates.

Scope: analyze the three cleanup targets from designer report 496, then name
the ideal future-oriented pattern for each:

- one length-prefixed frame codec;
- one typed component argument surface;
- `thiserror` / typed error cleanup;
- schema-centered reporting as an ongoing operator practice.

## Executive Result

None of the three cleanup targets is implemented on main today.

The right direction is not "deduplicate helper code" in the small sense. The
better future shape is a clear split of responsibilities:

- Schema creates component meaning: roots, variants, payloads, route identity,
  short headers, typed feedback, typed engine inputs/outputs.
- `triad-runtime` creates reusable runtime mechanics: byte envelopes, readers,
  writers, one-argument process edges, daemon runners, generic test harnesses.
- Component crates write the real decisions: validate a Spirit `Input`, decide
  the next `NexusAction`, persist through `Store`, shape domain replies.
- Text is a boundary projection: CLI/user/report display only. Machines should
  exchange rkyv archives, and reports should show how the typed value moves.

For the three concrete cleanups, the ideal order is:

1. `LengthPrefixedFrame` in `triad-runtime`.
2. `ComponentArgument` / `ComponentCommand` in `triad-runtime`, with explicit
   binary policy.
3. `thiserror` cleanup of hand-written runtime errors after the frame and
   argument error vocabulary is named.

That order matters. Error cleanup before frame/argument extraction only makes
the current wrong boundaries prettier.

## Schema In, Code Out: The Current Spirit Example

This is the concrete pattern the psyche asked to see repeatedly.

### Authored Schema In

`/git/github.com/LiGoldragon/spirit/schema/lib.schema` starts with Signal
roots:

```text
[Record Observe Lookup Count Remove LookupStash]
[RecordAccepted RecordsObserved RecordsStashed RecordFound RecordsCounted RecordRemoved Error Rejected]
```

Then namespace declarations define payloads:

```text
Record Entry
Observe Query
RecordAccepted SemaReceipt
Rejected SignalRejection
Entry { Topics * Kind * Description * Magnitude * Privacy * }
PrivacySelection [Any Exact AtMost AtLeast]
```

Meaning: `Record` is not a wrapper struct authored somewhere else. It is a
Signal input variant whose payload is the same-named namespace binding
`Record Entry`, which lowers to "variant Record carries Entry directly."

### Asschema Out

`schema/lib.asschema` records the lowered canonical shape:

```text
(Record (Some (Plain Record)))
(Public Record (Alias (Record (Plain Entry))))
(Public Entry (Struct (Entry {topics (Plain Topics) kind (Plain Kind) ...})))
```

Meaning: authored sugar is gone. The canonical object graph says exactly which
names are enum variants, aliases, structs, fields, and payload references.

### Generated Rust Out

`src/schema/lib.rs` then emits:

```rust
pub enum Input {
    Record(Record),
    Observe(Observe),
    Lookup(Lookup),
    Count(Count),
    Remove(Remove),
    LookupStash(LookupStash),
}

pub type Record = Entry;

pub struct Entry {
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub magnitude: Magnitude,
    pub privacy: Privacy,
}
```

It also emits:

- rkyv derives for binary wire/storage values;
- optional NOTA decode/encode under `nota-text`;
- route enums such as `InputRoute`;
- short-header methods;
- generated `SignalEngine`, `NexusEngine`, and `SemaEngine` traits;
- constructor methods such as `SemaWriteInput::record(payload)`.

### Hand-Written Implementation

`Nexus` consumes the generated `Input`:

```rust
Input::Record(record) =>
    NexusAction::command_sema_write(SemaWriteInput::record(record))
```

`Store` consumes the generated `SemaWriteInput`:

```rust
SemaWriteInput::Record(record) => self.record(record)
```

`Store` adds semantics that schema intentionally does not own:

```rust
self.topic_match.matches(&entry.topics)
    && self.kind.as_ref().is_none_or(|kind| &entry.kind == kind)
    && self.privacy_selection.matches(&entry.privacy)
```

The trade: schema creates the typed nouns and routing surface; Rust code owns
the algorithms. This is the mental model to keep repeating.

## Cleanup 1: LengthPrefixedFrame

### What We Have Now

The 4-byte length prefix is repeated in three places.

In `triad-runtime/src/trace.rs`, `TraceFrame<Event>` owns:

- `LENGTH_PREFIX_BYTE_COUNT = 4`;
- `u32::try_from(archive.len())`;
- big-endian length bytes;
- read-exact prefix, allocate payload, read-exact body.

In `spirit/src/transport.rs`, `SignalTransport<Stream>` repeats the same
mechanics around generated Signal frames.

In `spirit/tests/socket_negative.rs`, a test-only `LengthPrefixedFrame` repeats
the same mechanics to feed negative wire bytes.

One nuance: generated `Input::encode_signal_frame()` and
`Output::encode_signal_frame()` do not add the 4-byte stream length. They
generate a short-header plus rkyv archive body. The stream envelope is outside
generated schema code.

So the real layers today are:

```text
schema-generated body: 8-byte short header + rkyv archive
transport envelope:    4-byte length prefix + body bytes
```

Trace currently skips the schema short header and frames only:

```text
trace envelope:        4-byte length prefix + trace rkyv archive
```

### Ideal World

`triad-runtime` should own a `frame` module with one binary envelope object.
It should know nothing about Spirit, Signal roots, trace event variants, NOTA,
or schema names. It should know:

- maximum frame length policy;
- byte order for the length prefix;
- how to write exactly one frame body;
- how to read exactly one frame body;
- how to surface typed frame errors.

The ideal type split:

```rust
pub trait BinaryFrameBody: Sized {
    type Error: std::error::Error + Send + Sync + 'static;

    fn encode_body(&self) -> Result<Vec<u8>, Self::Error>;
    fn decode_body(bytes: &[u8]) -> Result<Self, Self::Error>;
}

pub struct LengthPrefixedFrame<Body> {
    body: Body,
}

pub struct LengthPrefixedCodec {
    maximum_body_bytes: usize,
}
```

Then:

- `TraceEventFrame` can either become a `BinaryFrameBody` implementation or be
  bridged through a trace-specific adapter.
- Generated Signal roots can implement or be adapted into `BinaryFrameBody`
  through their generated `encode_signal_frame` / `decode_signal_frame`
  methods.
- Test helpers stop owning their own copy.

The codec should be synchronous first because the current surfaces are
synchronous `Read + Write`; async wrappers can come later if/when daemon runner
work needs them.

### Schema Role

Schema should not emit the 4-byte length prefix. The length prefix is a stream
transport envelope, not component meaning.

Schema should emit or enable the payload body:

```text
Input root -> short-header route -> rkyv archive body
```

The generated body is component-specific because `InputRoute`, short headers,
and payload variants come from schema. The length prefix is component-agnostic
because every binary stream needs the same "how many bytes follow" envelope.

Ideal report pattern:

```text
Schema creates: Input::Record + short_header + rkyv body.
Runtime creates: LengthPrefixedFrame(body_bytes).
Implementation creates: SignalTransport::exchange(input) using both.
Witness creates: process-boundary test rejects length-prefixed NOTA text.
```

### Best Next Implementation

1. Add `triad_runtime::frame`.
2. Move trace read/write internals to it.
3. Move Spirit `SignalTransport` read/write internals to it.
4. Replace the test-only `LengthPrefixedFrame`.
5. Add a test proving a `CounterTraceEvent` and a generated Signal body both
   use the same codec.

Do not move short-header logic into `triad-runtime`. That belongs to generated
schema code.

## Cleanup 2: ComponentArgument

### What We Have Now

New Spirit currently has two separate one-argument implementations.

The CLI:

```rust
match self.arguments.as_slice() {
    [argument] => Ok(argument),
    _ => Err("expected exactly one NOTA argument or path".into()),
}

if argument.trim_start().starts_with('(') {
    Ok(argument.to_owned())
} else if Path::new(argument).exists() {
    Ok(fs::read_to_string(argument)?)
} else {
    Err("inline operation must be a parenthesized NOTA value".into())
}
```

The daemon:

```rust
match self.arguments.as_slice() {
    [argument] => Ok(argument),
    _ => Err(DaemonCommandError::ArgumentCount { count: self.arguments.len() }),
}

Configuration::from_binary_path(single_argument)
```

The error vocabulary diverges. The CLI returns boxed string errors; the daemon
has typed `DaemonCommandError`.

There is also a documentation mismatch. `spirit/README.md` says the daemon can
start from a NOTA argument containing socket/database paths, but
`spirit/ARCHITECTURE.md` and the actual code say the daemon takes a path to a
binary rkyv `Configuration` object.

### Ideal World

The ideal abstraction is not "a function that checks `starts_with('(')`."
It is a typed process-edge object:

```rust
pub struct ComponentCommand {
    arguments: Vec<String>,
}

pub enum ComponentArgument {
    InlineNota(NotaText),
    NotaFile(NotaFilePath),
    SignalFile(SignalFilePath),
}

pub enum ArgumentPolicy {
    TextOrFile,
    SignalFileOnly,
}
```

`ComponentCommand` owns the exactly-one-argument rule. `ComponentArgument`
owns the classification. A component-specific command then declares what policy
it accepts.

The key design point: different binaries can share the same argv discipline
without sharing the same decoding policy.

- A normal CLI accepts `InlineNota`, `NotaFile`, and possibly `SignalFile`.
- A lean binary daemon may accept `SignalFileOnly` so `nota-next` never enters
  the daemon dependency tree.
- A developer launcher can accept NOTA config and write a signal-encoded config
  file before starting the daemon.

That keeps all three true:

- every binary takes exactly one argument;
- NOTA is still the human/agent invocation language;
- production daemons can stay binary-only internally.

### No String Sniff

The better classifier should not decide "inline NOTA" by checking the first
non-whitespace character. It should do this:

1. If the argument names an existing path, classify it as a file path.
2. If it is not a path, try to parse it as a NOTA value using the NOTA parser.
3. If parsing succeeds, return `InlineNota`.
4. If parsing fails, return a typed `ArgumentError::UnknownSingleArgument`
   carrying parse and path context.

For a path:

- text command policy can read the file and parse as NOTA;
- signal-file policy can read bytes and pass them to the expected rkyv decoder;
- optional extension or magic checks can be added later, but correctness comes
  from the component-specific decoder, not a filename suffix.

One dependency constraint matters: the argument layer must not force
`nota-next` into every daemon build. There are two acceptable shapes:

- `triad-runtime` owns only exact-one-argument counting, file-path
  classification, and typed errors; each text-enabled CLI supplies the NOTA
  parser.
- Or `triad-runtime` has an explicit optional `nota-argument` feature used by
  CLI builds, while binary-only daemon builds keep it disabled.

The bad shape would be a convenient shared helper that makes `nota-next`
non-optional in every runtime crate.

### Schema Role

Schema should define the request/config shape. It should not parse argv.

For the current `spirit` CLI:

```text
Schema creates: Input root + NOTA parser/display under nota-text.
Runtime creates: ComponentArgument::InlineNota or NotaFile.
CLI creates: Input::from_str(argument_text) then SignalTransport::exchange.
```

For the current `spirit` daemon:

```text
Schema should eventually create: Configuration root or config signal root.
Runtime creates: ComponentArgument::SignalFile.
Daemon creates: Configuration::from_binary_bytes(bytes), then Daemon::run.
```

The current `Configuration` is hand-written. In the future, it should either be
schema-emitted or live in a small generated config contract. The daemon should
not silently grow a hand-written argument language around it.

### Best Next Implementation

1. Add `triad_runtime::argument`.
2. Move exactly-one-argument counting there.
3. Add typed errors with thiserror.
4. Replace the CLI's boxed string errors with a `SpiritCliError`.
5. Replace `DaemonCommand::single_argument` with `ComponentCommand`.
6. Update README so it matches the actual binary rkyv config path, or implement
   the documented NOTA launcher explicitly.

The policy object is what keeps this reusable. A single helper that always
reads strings would be wrong for the daemon.

## Cleanup 3: thiserror and Error Boundaries

### What We Have Now

New Spirit hand-writes several error enums:

- `TransportError`;
- `ConfigurationError`;
- `DaemonError`;
- `DaemonCommandError`;
- `StoreError`;
- generated support errors such as `SignalFrameError`,
  `ActorStartFailure`, and `ActorStopFailure`.

The hand-written component errors manually implement:

- `Display`;
- `std::error::Error`;
- `From<...>` conversions.

The CLI uses `Box<dyn std::error::Error>` and string errors for its argument
edge.

`triad-runtime` already uses `thiserror` for `TraceError`, so the dependency
and idiom are already accepted in the stack.

### Ideal World

There are two different error classes, and they should not be collapsed.

1. Runtime/process errors:
   - IO failure;
   - frame too large;
   - config file cannot be read;
   - redb fails;
   - rkyv archive cannot encode/decode;
   - wrong argument kind.

2. Component/domain feedback:
   - `ValidationError::EmptyTopic`;
   - `ValidationError::StashHandleNotFound`;
   - future privacy/archive rejection reasons;
   - user-facing typed outcomes.

Runtime/process errors should use `thiserror`.

Component/domain feedback should be schema-emitted typed values that can cross
the Signal boundary as rkyv and render as NOTA at the client edge.

The ideal rule:

```text
If the caller is another program edge, return a Rust error.
If the caller is the component protocol, return a generated typed reply.
If a human sees it, Display is only the final projection.
```

### Best Runtime Error Shape

For hand-written errors:

```rust
#[derive(Debug, thiserror::Error)]
pub enum TransportError {
    #[error("transport IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("signal frame error: {0}")]
    SignalFrame(#[from] SignalFrameError),

    #[error("frame too large for u32 prefix: {found} bytes")]
    FrameTooLarge { found: usize },
}
```

For `StoreError`, the current boxed `redb::Error` choice may stay because redb
error enums are large. `thiserror` can still own the `Display` and `From`
ceremony:

```rust
#[derive(Debug, thiserror::Error)]
pub enum StoreError {
    #[error("sema store IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("sema database error: {0}")]
    Database(#[from] Box<redb::Error>),
}
```

The exact conversion may need small wrapper methods because the current code
converts several redb error types into `redb::Error` first. The important point
is that the ceremony belongs to the derive macro, not hand-written match
blocks.

### Schema Role

Schema should own protocol-visible feedback.

Current schema:

```text
ValidationError [EmptyTopic EmptyDescription EmptyQueryTopic StashHandleNotFound]
SignalRejection { ValidationError * DatabaseMarker * }
ErrorReport { ErrorMessage * DatabaseMarker * }
Output [... Error Rejected]
```

Generated code creates:

```rust
pub enum ValidationError {
    EmptyTopic,
    EmptyDescription,
    EmptyQueryTopic,
    StashHandleNotFound,
}

pub struct SignalRejection {
    pub validation_error: ValidationError,
    pub database_marker: DatabaseMarker,
}
```

That is the right direction. Future typed feedback should expand this schema
tree rather than hide domain failures in runtime strings.

Runtime errors can use `thiserror`, but schema-visible errors should remain
data. The danger is making `thiserror` feel like a substitute for typed
feedback. It is not; it is a Rust-process ergonomics tool.

### Best Next Implementation

1. Add `thiserror` as a direct dependency to `spirit` if it is not already
   direct.
2. Convert `TransportError`, `ConfigurationError`, `DaemonError`,
   `DaemonCommandError`, and `StoreError`.
3. Replace the CLI's `Box<dyn Error>` with `SpiritCliError`.
4. Do not touch generated `SignalFrameError` until schema-rust-next has an
   explicit generated-error policy.
5. For future archive/privacy features, add schema-emitted typed rejection and
   outcome enums first; use `thiserror` only for filesystem/redb/process
   failures underneath.

## Schema-Centered Reporting Pattern

The psyche asked to see schema "backward and forward, up and down, left and
right." The operator report pattern should make that mechanical.

For every schema-affecting implementation report, include this chain:

1. Authored schema in: the exact `schema/*.schema` lines.
2. Asschema out: the lowered canonical declarations that matter.
3. Generated Rust out: enum/struct/alias/trait/method excerpts.
4. Hand-written implementation: the match arm or method that consumes the
   generated type.
5. Wire/text witness: rkyv frame, NOTA render, process-boundary test, or
   compile-fail witness.
6. Trade: what schema owns, what runtime owns, what component code owns.

This should appear even when the code change is not itself in schema, because
the question is often "why is this not schema?" The length-prefix case is the
perfect example:

```text
Schema owns: Input route + short header + rkyv body.
Runtime owns: 4-byte length envelope.
Component owns: what to do after decode.
```

That split teaches schema by showing its boundary, not only its output.

## Report Examples To Repeat

### Example A: Input Root

Schema:

```text
[Record Observe Lookup Count Remove LookupStash]
Record Entry
```

Generated:

```rust
pub enum Input {
    Record(Entry),
    Observe(Query),
    Lookup(RecordIdentifier),
    Count(Query),
    Remove(RecordIdentifier),
    LookupStash(StashHandle),
}
```

Implementation:

```rust
Input::Record(record) =>
    NexusAction::command_sema_write(SemaWriteInput::record(record))
```

Trade: schema creates the callable surface; Nexus decides the operational
translation.

### Example B: PrivacySelection

Schema:

```text
PrivacySelection [Any Exact AtMost AtLeast]
Exact Privacy
AtMost Privacy
AtLeast Privacy
```

Generated:

```rust
pub enum PrivacySelection {
    Any,
    Exact(Privacy),
    AtMost(Privacy),
    AtLeast(Privacy),
}
```

Implementation:

```rust
Self::AtMost(maximum) => privacy.weight() <= maximum.weight()
```

Trade: schema creates the selector vocabulary; implementation defines the
ordering semantics over `Magnitude`.

### Example C: Signal Frame

Schema:

```text
[Record Observe Lookup Count Remove LookupStash]
```

Generated:

```rust
pub fn short_header(&self) -> u64 { ... }
pub fn encode_signal_frame(&self) -> Result<Vec<u8>, SignalFrameError> { ... }
```

Runtime:

```rust
LengthPrefixedFrame::new(input.encode_signal_frame()?)
```

Trade: schema creates route identity and payload bytes; runtime creates stream
framing.

### Example D: Nexus Action

Schema:

```text
NexusAction [CommandSemaWrite CommandSemaRead ReplyToSignal CommandEffect Continue]
CommandSemaWrite SemaWriteInput
ReplyToSignal Output
```

Generated:

```rust
pub enum NexusAction {
    CommandSemaWrite(SemaWriteInput),
    CommandSemaRead(SemaReadInput),
    ReplyToSignal(Output),
    CommandEffect(NexusEffectCommand),
    Continue(NexusWork),
}
```

Implementation:

```rust
match action {
    NexusAction::CommandSemaWrite(command) => SemaEngine::apply(...),
    NexusAction::ReplyToSignal(reply) => return ...,
}
```

Trade: schema creates recursive control data; the runner should be generic;
Spirit keeps only `step_decide`.

## Open Decisions

1. Should `ComponentArgument` live in `triad-runtime` or a smaller
   `component-runtime` crate?

My operator lean: `triad-runtime` for now. The same crate is already becoming
the shared process-edge substrate for schema-derived triad daemons.

2. Should generated roots implement a generic `BinaryFrameBody` trait directly?

My operator lean: yes eventually, but not as the first slice. First land the
runtime codec and use small adapters in Spirit. Then teach `schema-rust-next`
to emit the impl once the trait shape proves stable.

3. Should generated support errors use `thiserror`?

My operator lean: later. Hand-written runtime errors should use `thiserror`
now; generated protocol feedback should stay schema data. Generated support
errors can use `thiserror` after the emitter has a deliberate error model.

4. Should the daemon accept NOTA config directly?

My operator lean: not in the lean daemon binary. Keep daemon startup as a
signal-encoded rkyv config file until a schema-generated config launcher exists.
If a human wants to type config as NOTA, the launcher translates it to binary.

## Implementation Slice

If the psyche says "implement this cleanup now," the clean operator slice is:

1. Add `triad_runtime::frame::LengthPrefixedCodec`.
2. Convert `triad-runtime` trace to use it.
3. Convert `spirit` `SignalTransport` and socket negative tests to use it.
4. Add `triad_runtime::argument::ComponentCommand` and typed argument errors.
5. Convert Spirit CLI/daemon command argument handling.
6. Convert hand-written Spirit errors to `thiserror`.
7. Update `spirit` README/ARCHITECTURE so daemon startup docs match code.

That sequence keeps schema, runtime, and component responsibilities separate
while making the repeated code disappear.
