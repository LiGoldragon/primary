# 368 — Running spirit concept on new architecture

*Designer-assistant track per psyche 2026-05-26 (intent record 845).
Proves end-to-end communication through the schema-derived stack for
ONE operation. NOT v0.3 capability parity — minimum-viable substrate
demonstrating the chain: psyche NOTA argv → CLI → rkyv on Unix socket
→ daemon → Recorder actor → rkyv reply → CLI → NOTA stdout.
Empirically closes /366 truth claims 2, 3, 4, 5, 6.*

## Summary

| Repo | Feature branch | HEAD commit | Tests passing | Nix check |
|---|---|---|---|---|
| `LiGoldragon/signal-spirit` | `designer-running-concept-2026-05-26` | `710b628eddf1` | 6/6 | green |
| `LiGoldragon/spirit` | `designer-running-concept-2026-05-26` | `643978cfb326` | 4 unit + 2 integration = 6/6 | green |

The full chain runs in one shell pipeline. The daemon spawns and binds
a Unix socket; the CLI sends a NOTA-encoded request; the daemon
replies; the CLI prints the result. Both repos pass
`nix flake check --option max-jobs 0` end-to-end.

## What works end-to-end

Live shell transcript from the running concept (release-build binaries
on the spirit feature branch):

```text
$ spirit-daemon "[/tmp/spirit.sock]" &
spirit-daemon: listening on /tmp/spirit.sock

$ spirit-cli "(Request [/tmp/spirit.sock] (Record ([running-spirit-concept] [designer ships end-to-end])))"
(RecordAccepted 1)

$ spirit-cli "(Request [/tmp/spirit.sock] (Record ([second-topic] [second-record])))"
(RecordAccepted 2)
```

The shell-visible substance:

- The argument is a single NOTA bracket-form record per AGENTS.md "NOTA
  is the only argument language." No flags. The CLI's argument carries
  both the socket path `[<path>]` AND the typed `(<Input variant>)` to
  send.
- The CLI parses the request, decodes the inner `(Record (...))` block
  via the schema-emitted `Input::from_str` (NOTA codec from
  schema-rust-next), encodes it to rkyv via the
  schema-emitted `signal_spirit::WireCodec`, and ships the length-
  prefixed frame over the Unix socket.
- The daemon's per-connection thread reads the frame, decodes via
  rkyv, and dispatches through the `Recorder` actor. Today the actor
  is the engine for the one operation; per /366 §6 it generalises to a
  schema-emitted dispatch table.
- The actor appends to an in-memory `Vec<RecordedEntry>` keyed by a
  monotonic `RecordIdentifier`. It returns
  `Output::RecordAccepted(RecordIdentifier(n))`.
- The daemon encodes the reply via rkyv and writes a length-prefixed
  frame back. The CLI reads the frame, decodes, and prints the reply
  via the schema-emitted `Output::Display` impl.

## The 5 truth claims now empirically verified

From /366's table — the running concept moves the following rows from
"NOT YET" to "empirically tested":

| Claim | Status before | Status after | Evidence |
|---|---|---|---|
| **2 — The CLI is NOTA** | NOT YET (no CLI on new substrate) | demonstrated | `spirit-cli` binary takes one NOTA bracket-form argument; emits NOTA on stdout. End-to-end shell transcript above. |
| **3 — Binary rkyv between components** | NOT YET (schema-rust-next emission gap) | demonstrated | `signal_spirit::WireCodec::{encode,decode}_{input,output}` round-trip tests pass (4 tests in `signal-spirit/src/lib.rs`); `spirit::wire::Wire` framed round-trip tests pass on an in-memory pipe (2 tests in `spirit/src/wire.rs`). |
| **4 — Engine matches Input variants to actions** | NOT YET | demonstrated | `Recorder::handle` (`spirit/src/actor.rs`) matches `Input` variants; appends and returns an identifier. Integration test `one_request_round_trips_through_unix_socket` proves dispatch over a real socket. |
| **5 — SEMA = command → response reaction object** | NOT YET | demonstrated for the in-memory shape | The Recorder is the engine + the substrate; the action ("append entry") produces a response ("identifier N") that the engine reshapes into `Output::RecordAccepted`. The redb-backed at-rest layer remains future work, but the reaction-object shape is now empirically present. |
| **6 — Signal IN/OUT with rkyv binary on wire** | NOT YET | demonstrated | The end-to-end test (`tests/end_to_end.rs::one_request_round_trips_through_unix_socket`) spawns the daemon on a tempfile Unix socket and exchanges length-prefixed rkyv frames. The shell transcript demonstrates the same on real binaries. |

Score moves from /366's 4/12 → 9/12. Claims still untested:
async unique-ID mail delivery (7), synchronous fast-response option (8),
emit_all_schemas single-call entry (record 844's aspirational shape).

## What's still hand-rolled (with reason)

The point of the concept is to show how much the schema substrate
already covers. Most of the substance is emitted; the remainder is
named here precisely.

| Layer | Source | Status |
|---|---|---|
| `Topic` / `Description` / `RecordIdentifier` newtypes | emitted by schema-rust-next from `schema/signal-spirit.schema` | EMITTED |
| `Entry` struct | emitted | EMITTED |
| `Input` / `Output` surface enums | emitted | EMITTED |
| `rkyv::Archive` / `Serialize` / `Deserialize` derives | emitted (`emit_struct`, `emit_enum`, `emit_surface` lines in `schema-rust-next/src/lib.rs`) | EMITTED |
| `from_nota_block` / `to_nota` methods | emitted (`emit_nota_*_impl` lines) | EMITTED |
| `FromStr` + `Display` on `Input` and `Output` surfaces | emitted (`emit_nota_surface_impl`) | EMITTED |
| `short_header` module constants | emitted (`emit_short_headers`) | EMITTED |
| `NotaDecodeError` enum + Display + Error | emitted (`emit_nota_support`) | EMITTED |
| `WireCodec` (rkyv encode/decode entry-points) | hand-rolled in `signal-spirit/src/lib.rs` | HAND-ROLLED — thin wrapper around `rkyv::to_bytes` / `rkyv::from_bytes`. Migration target: schema-rust-next emits a `WireCodec` per surface, parameterised on the surface name. |
| `Wire` length-prefixed framing | hand-rolled in `spirit/src/wire.rs` | HAND-ROLLED — 4-byte big-endian length prefix + payload. Migration target: this is the body of /199 Layer 5 (signal envelope). Today it has no `message_id`, no short-header dispatch, no async-mail tagging — those are named follow-ups. |
| `Recorder` actor + `RecordedEntry` storage | hand-rolled in `spirit/src/actor.rs` | HAND-ROLLED — this is engine-internal substrate, not user-facing schema. Per /366 §6 + record 730-732 it stays hand-authored (the engine's mapping logic is not authored schema content). |
| `Daemon` listener + per-connection thread | hand-rolled in `spirit/src/daemon.rs` | HAND-ROLLED — runtime substrate. Not a schema concern. |
| `Client` one-shot request | hand-rolled in `spirit/src/client.rs` | HAND-ROLLED — runtime substrate. |
| Daemon binary's socket-path arg parser | hand-rolled in `src/bin/daemon.rs::parse_socket_path` | HAND-ROLLED — uses `nota_next::Document` directly because the argument is a primitive bracket-string, not a typed Asschema record. Migration target: schema-rust-next emits a `NotaArg<T>` for any primitive-payload single-argument binary. |
| CLI binary's `(Request [<socket>] (<Input>))` parser | hand-rolled in `src/bin/cli.rs::parse_request` | HAND-ROLLED — composite shape blending a primitive (socket) and a typed Input. Migration target: an emitted `Request` record schema with a `[Socket Input]` pair declaration. |
| `build.rs` lowering schema → Rust source at compile time | hand-rolled in `signal-spirit/build.rs` | HAND-ROLLED — invokes `SchemaEngine::lower_source` + `RustEmitter::emit_file` directly. This realises the eventual `emit_schema!()` proc-macro (record 844) via build-script means while the macro front-end is not yet shipped. |

The pattern: **everything inside `signal-spirit`'s data plane is
emitted**; the hand-rolled pieces all live at the runtime + framing
boundary (`spirit`'s socket/actor substrate + the CLI/daemon arg
parsers). Schema-rust-next at HEAD `f76d6483` is already a richer
emitter than /366 §10's named-next-slices anticipated — the rkyv and
NOTA codec emission are landed.

## Code excerpts — the chain

The whole chain in ~10-line slices, layer by layer:

### Layer A — schema authoring (the spec)

`signal-spirit/schema/signal-spirit.schema`:

```nota
{}
[
  (Input (Record Entry))
  (Output (RecordAccepted RecordIdentifier))
]
{
  Topic [Text]
  Description [Text]
  RecordIdentifier [Integer]
  Entry [Topic Description]
}
```

### Layer B — schema → Rust at build time (the emitter)

`signal-spirit/build.rs`:

```rust
let source = fs::read_to_string(&schema_path).expect("read signal-spirit.schema");
let asschema = SchemaEngine::default()
    .lower_source(&source, SchemaIdentity::new("signal-spirit", "0.1.0"))
    .expect("lower signal-spirit.schema via schema-next");
let generated = RustEmitter.emit_file(&asschema);
fs::write(&out_path, generated.code.as_str()).expect("write generated Rust source");
```

### Layer C — schema-emitted types (in `signal-spirit/target/.../signal_spirit_generated.rs`)

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Entry { pub topic: Topic, pub description: Description }

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Input { Record(Entry) }

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Output { RecordAccepted(RecordIdentifier) }

impl std::str::FromStr for Input { /* schema-emitted NOTA decode */ }
impl std::fmt::Display for Input { /* schema-emitted NOTA encode */ }
```

### Layer D — rkyv on the socket (the wire framing)

`spirit/src/wire.rs::Wire`:

```rust
pub fn send_input<W: Write>(writer: &mut W, input: &signal_spirit::Input) -> Result<(), WireError> {
    let payload = signal_spirit::WireCodec::encode_input(input)
        .map_err(|error| WireError::Rkyv(error.to_string()))?;
    Self::send_frame(writer, &payload)
}
```

### Layer E — the engine (the one-arm dispatch)

`spirit/src/actor.rs::Recorder::handle`:

```rust
pub fn handle(&self, input: Input) -> Output {
    match input {
        Input::Record(entry) => {
            let identifier = self.append(entry);
            Output::RecordAccepted(identifier)
        }
    }
}
```

### Layer F — the CLI shell binary (the human boundary)

`spirit/src/bin/cli.rs`:

```rust
let Request { socket_path, input } = parse_request(&raw)?;
let output = Client::request(&socket_path, &input)?;
println!("{output}");           // schema-emitted Display → NOTA text
```

`spirit/src/client.rs::Client::request`:

```rust
pub fn request(socket_path: &Path, input: &Input) -> Result<Output, WireError> {
    let mut stream = UnixStream::connect(socket_path)?;
    Wire::send_input(&mut stream, input)?;
    Wire::receive_output(&mut stream)
}
```

## Open questions surfaced

Per /735 "ask the psyche when intent is unclear" — substance the
running concept brushed up against that's not yet decided:

1. **Signal envelope shape** — the running concept uses a bare 4-byte
   big-endian length prefix as the only framing. The eventual envelope
   (/199 Layer 5) carries `message_id`, short-header dispatch, and
   sender/receiver tags. Open: does that envelope move into
   schema-rust-next's emitted `Wire` substrate, or does it live in a
   shared `signal-frame` crate per /361 §10's repo strategy?
2. **`Input` / `Output` naming for one-operation contracts** — the
   running schema uses `Input` and `Output` (from operator's MVP
   fixture) rather than the v0.3 `Operation` / `Reply`. Open: pick one
   pair before the next slice. The /366 component view uses
   Operation/Reply; the schema-rust-next fixture uses Input/Output.
3. **`build.rs` vs `emit_schema!` proc-macro** — the running concept
   uses a build script that calls `schema-rust-next` at compile time
   and writes to `$OUT_DIR`. Per record 844 the eventual shape is a
   single proc-macro call in `src/lib.rs`. /367 §9 asked the same
   question: build-time emission (a) vs committed generation (b). The
   running concept proves (a) works; (b) is a content-addressing
   future.
4. **CLI compound-argument shape** — the running CLI takes
   `(Request [<socket>] (<Input>))`. This blends a primitive (socket
   path) with a typed Input. Open: is the connection a CLI-level
   concept ("which daemon am I talking to?") or should the CLI ship a
   single `Input` and discover the socket through workspace config
   (which itself would be a NOTA file)? The running concept took the
   first cut; psyche could prefer either.
5. **Cargo dependency on a designer feature branch** — `spirit/Cargo.toml`
   depends on `signal-spirit` at branch
   `designer-running-concept-2026-05-26`. This is fine for the running
   concept; operator's integration would normally rebase the
   signal-spirit work into operator's `main` and update spirit's
   dependency. Per `skills/double-implementation-strategy.md` this is
   the expected designer→operator handoff shape.

## What this means for /361 §12 + /366 truth table

For /361 §12 ("Empirically demonstrated vs aspirational"), the running
concept moves these rows from aspirational/partial to demonstrated:

- "Header derivation from Asschema" — was 🔵 ASPIRATIONAL → ⚪ now
  empirically present in `signal_spirit::short_header` constants
  (verified by `short_headers_are_derived_in_surface_variant_order`
  test); still simple 16-bits-per-slot encoding per /203 §"Known
  limits".
- "Schema-derived signal contract on the wire" — newly empirically
  present.

For /366 §9 (the 12-claim truth table), the running concept brings five
new rows green:

```text
2. CLI is NOTA                            ✅
3. Binary rkyv between components         ✅
4. Engine matches Input variants → Action ✅
5. SEMA reaction object Action → Response ✅
6. Signal IN/OUT rkyv binary on wire      ✅
```

Three claims remain (async mail delivery, sync-fast-response, single-
call `emit_all_schemas!()`) — all named follow-ups, not blocked by
substrate gaps.

## Worktrees touched

| Worktree | Purpose |
|---|---|
| `~/wt/github.com/LiGoldragon/signal-spirit/designer-running-concept-2026-05-26/` | signal-spirit feature branch (schema, build.rs, codec wrappers, tests) |
| `~/wt/github.com/LiGoldragon/spirit/designer-running-concept-2026-05-26/` | spirit feature branch (daemon, CLI, actor, wire framing, end-to-end test) |

Both feature branches are pushed to origin. Per
`skills/double-implementation-strategy.md`: designer feature branches
do not push to main; operator's lane integrates.

## References

- Psyche 2026-05-26 — intent records 839-845 (NOTA-as-specification +
  running-concept request)
- `/366` — component view + truth verification (the 12-claim table)
- `/203` — operator's schema-next interface implementation baseline
- `/367` — NOTA-as-specification, schema-as-CapnProto-superset framing
- `/361` §6-§9 — the architectural pattern (Asschema, Layer 4 headers,
  composer, schema diff)
- `skills/double-implementation-strategy.md` — designer feature
  branches off operator main
- `skills/component-triad.md` — daemon + signal + owner-signal triad
  shape (this concept exercises the first two legs)
- Operator repos at the verified commits:
  `nota-next@6b4364d9`, `schema-next@19591a7a`,
  `schema-rust-next@f76d6483`
- Designer feature branches:
  `LiGoldragon/signal-spirit@710b628e`,
  `LiGoldragon/spirit@643978cf`
- Spirit record 848 (this session's capture per the running-concept
  start)
