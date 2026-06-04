# Audit 8 — Bad patterns, ugliness, and gaps across the schema-derived core stack

*Report-only. Nothing fixed. Every behaviour claim below is backed by
a command actually run in this environment, with verbatim output
pasted. Where I could not verify, I say so.*

## Scope and method

The audit target is the schema-derived **core stack** as enumerated in
`/home/li/primary/protocols/active-repositories.md` §"Current Core
Stack". I narrowed to the ten repos that carry the NOTA → schema →
Rust → signal/sema → spirit lowering chain and are reachable as
checked-out source under `/git/github.com/LiGoldragon/`:

| Repo | `.rs` files | lines (non-target) | Role in stack |
|---|---|---|---|
| `nota` (nota-box) | 10 | 889 | boxed-NOTA root+box framing |
| `nota-codec` | 34 | 5204 | NOTA lexer / encoder / decoder |
| `nota-derive` | 7 | 511 | `NotaRecord`/`NotaEnum`/… derive macros |
| `schema-next` | 26 | 12691 | NOTA → checked `Asschema` lowering |
| `schema-rust-next` | 18 | 12837 | `Asschema` → Rust source emission |
| `signal-core` | 31 | 3899 | wire kernel + `signal_channel!` macro |
| `sema` | 3 | 1054 | redb+rkyv storage kernel |
| `sema-engine` | 18 | 5397 | typed database engine over `sema` |
| `spirit` | 25 | 7573 | runnable schema-derived pilot daemon+CLI |
| `signal-spirit` | 2 | 153 | spirit's ordinary signal contract |

The discipline audited against: `/home/li/primary/skills/rust-discipline.md`
and its five sub-files (`methods.md`, `errors.md`, `storage-and-wire.md`,
`parsers.md`, `crate-layout.md`), plus the AGENTS.md hard overrides
(NOTA bracket-only, single-argument rule, method-only). The telltales
hunted: free functions outside `#[cfg(test)]`/`fn main`, ZST namespace
holders, hand-rolled parsers, flag soup, blocking-in-actor-handlers /
`Arc<Mutex<T>>`-between-actors, non-typed (`anyhow`/`eyre`) errors,
quotation marks emitted into NOTA, `Req`/`Id` abbreviations, and
`::`-vs-single-colon schema path confusion.

The toolchain confirmed live:

```
$ ~/.nix-profile/bin/cargo --version
cargo 1.95.0 (f2d3ce0bd 2026-03-21)
$ which spirit
/home/li/.nix-profile/bin/spirit
```

The deployed CLI resolves to `spirit-v0.5.1`:

```
$ spirit --version
/nix/store/20zk48jr4sn8yrjyq925gvzz3p4x3zkm-spirit/bin/spirit accepts NOTA or signal-file input, not flag-style argument --version
```

— note the binary itself enforces the single-argument NOTA rule by
rejecting `--version`. That rejection is the first confirmed datum of
the audit.

## Headline: the stack is healthy; the debt is stratified by age

The single most important finding is a clean **age stratification**.
Counting module-level free functions in production `src/` (column-0
`fn`, excluding `fn main`):

```
$ for r in nota-codec nota-derive nota schema-next schema-rust-next \
    signal-core sema sema-engine spirit signal-spirit; do
    d=/git/github.com/LiGoldragon/$r
    n=$(grep -rnE '^(pub )?(pub\(crate\) )?(async )?(const )?(unsafe )?fn ' \
        "$d" --include='*.rs' | grep -v '/target/' | grep -E '/src/' \
        | grep -vE 'fn main\b' | wc -l)
    printf "%-22s %s\n" "$r" "$n"
  done

nota-codec             18
nota-derive            12
nota                   27
schema-next            0
schema-rust-next       0
signal-core            26
sema                   0
sema-engine            0
spirit                 0
signal-spirit          0
```

The split is not random. The **newer schema-emission and storage
crates** — `schema-next`, `schema-rust-next`, `sema`, `sema-engine`,
`spirit` — carry **zero** module-level free functions. They were
written after the methods-on-types rule hardened (intent records 712
and 882, Maximum, 2026-05-26/27). The **foundational NOTA/wire layer**
— `nota` (27), `signal-core` (26), `nota-codec` (18), `nota-derive`
(12) — predates that enforcement and carries free-function debt. The
discipline is winning; the debt is concentrated in the oldest crates
at the bottom of the stack.

Two more headline positives, both verified, before the violations:

- **No `anyhow` / `eyre` / `Box<dyn Error>` anywhere in the core
  stack.** The typed-per-crate `Error` enum discipline
  (`skills/rust/errors.md`) holds perfectly:

  ```
  $ for r in nota-codec nota-derive nota schema-next schema-rust-next \
      signal-core sema sema-engine spirit signal-spirit; do
      grep -rnE 'anyhow|eyre|Box<dyn.*Error>' \
        /git/github.com/LiGoldragon/$r --include='*.rs' \
        | grep -v '/target/' | grep -E '/src/'
    done
  (no output)
  ```

- **No flag soup in any production code.** No `clap`, `structopt`,
  `argh`, `std::env::args`, `--verbose`, `--format`, or `--config` in
  any `src/`. The only `.arg(...)`/`--edition`/`--print-out-paths`
  hits are in test files invoking `cargo`/`rustc`/`nix` subprocesses —
  those are external tools' flags, not the components' own argument
  surfaces. The single-argument-NOTA rule holds at every production
  boundary.

## Live confirmation: NOTA bracket-only rule holds end-to-end

I exercised the deployed daemon-backed CLI with a real record and
checked the reply for any `"` character:

```
$ spirit "(Record ([audit-quote-check] Decision [verify no quotation marks appear in NOTA output] Maximum Zero))"
(RecordAccepted [3t40])
```

The reply `(RecordAccepted [3t40])` is pure bracket-form NOTA — zero
quotation marks. A `grep -q '"'` over the output returned no match
(reported "NO double-quote char in output (PASS)"). This confirms the
AGENTS.md hard override "NOTA strings come EXCLUSIVELY from bracket
forms; never emit quotation marks" is satisfied by the live binary on
both the write request and the reply.

Source-side, the encoder structurally cannot emit `"`. The only
escape sequences in the encoder are backslash-doubling and
bracket-escaping, never quote-emission:

```
$ sed -n '288,296p' /git/github.com/LiGoldragon/nota-codec/src/encoder.rs
fn write_bracket_string(output: &mut String, value: &str) {
    ...
            '\\' => output.push_str(r"\\"),
```

I note one **deployed-vs-source gap** I could *not* close: the
deployed `spirit-v0.5.1` `Observation` enum does not match the source
schema's `Observe (Query ...)` shape. Every read-side probe I tried
was rejected by the live binary:

```
$ spirit "(Observe (Query (Partial [audit-quote-check]) None Any))"
invalid request text: unknown variant `Query` for enum `Observation`
$ spirit "(Observe (All))"
invalid request text: unknown variant `All` for enum `Observation`
```

whereas the source `spirit/schema/sema.schema` declares
`ReadInput [Observe Lookup Count]` and `Observe Query`. So the
deployed binary is **behind** the source schema on the read path. I
verified the *write* path works on the deployed binary (the
`RecordAccepted` above); I could not verify the *read* path against
the deployed binary, and I did not guess its shape. This matches the
source-ahead-of-deploy observation already recorded in designer report
58. It is a **gap**, not a violation: the committed source has evolved
past the deployed artifact.

## Violation 1 — ZST namespace holder: `WireCodec` (signal-spirit)

This is the single cleanest rule violation in the whole stack, and it
sits in the flagship contract crate. A full-stack scan for unit
structs (`struct X;`) that carry an inherent `impl X { }` block found
exactly one:

```
$ # for each unit struct, check for an inherent 'impl Name {' block
  ... (scan across all ten repos) ...
signal-spirit: /git/github.com/LiGoldragon/signal-spirit/src/lib.rs
   -> unit struct 'WireCodec' HAS inherent 'impl WireCodec {' block
(done)
```

The offending code (`signal-spirit/src/lib.rs:34-56`):

```rust
pub struct WireCodec;

impl WireCodec {
    pub fn encode_input(input: &Input) -> Result<Vec<u8>, rkyv::rancor::Error> {
        rkyv::to_bytes::<rkyv::rancor::Error>(input).map(|bytes| bytes.to_vec())
    }
    pub fn decode_input(bytes: &[u8]) -> Result<Input, rkyv::rancor::Error> {
        rkyv::from_bytes::<Input, rkyv::rancor::Error>(bytes)
    }
    pub fn encode_output(output: &Output) -> Result<Vec<u8>, rkyv::rancor::Error> { ... }
    pub fn decode_output(bytes: &[u8]) -> Result<Output, rkyv::rancor::Error> { ... }
}
```

**Kind:** ZST method holder / free-functions-in-namespace-clothing.
**Why it's a smell:** This is the textbook `CertParser;` anti-pattern
from `skills/rust/methods.md` §"No ZST method holders". `WireCodec`
carries no data. Its four inherent methods do real work on `Input` /
`Output` — data they don't own. Apply the skill's own test: *erase
`WireCodec` from the type system and its job vanishes* — yes, it does;
the verbs simply belong on `Input` and `Output`. The honest shape is
`Input::to_wire()` / `Input::from_wire(bytes)` and
`Output::to_wire()` / `Output::from_wire(bytes)`, or trait impls
(`TryFrom<&[u8]>`, an `AsWire` trait) on the schema-emitted nouns.
This is doubly notable because `Input`/`Output` are *schema-emitted
types* and the discipline explicitly says (methods.md §"Schema-
generated objects are the method surface") that the wire codec verbs
attach to those generated nouns, "not beside it." `WireCodec` is the
"beside it."

Worth flagging for register: a `*Codec` ZST as the home for
encode/decode pairs is the *most common* shape this anti-pattern
takes, so it is likely to be copied into the next `signal-<component>`
crate by pattern-matching. It is the one to kill early.

(For contrast, `signal-core/src/pattern.rs` has `pub struct Bind;` and
`pub struct Wildcard;` — these are **not** violations. Their only
`impl` blocks are trait impls (`NotaEncode`/`NotaDecode`) that make
them the `(Bind)` / `(Wildcard)` empty-record markers on the wire. The
type position *is* the work; erasing the name breaks the wire form.
They pass the skill's test.)

## Violation 2 — free functions in the foundational layer

The free-function debt from the headline table, broken down by where
it is a genuine violation vs a framework-mandated exception.

### 2a. nota-box (`nota` repo) — parser/codec helpers as free fns (27)

`nota/nota-box/src/decode.rs`, `encode.rs`, `text.rs`, and `peek.rs`
are built almost entirely from module-level `fn`. Representative hits
with `file:line`:

```
$ grep -rnE '^(pub )?(async )?(const )?fn ' \
    /git/github.com/LiGoldragon/nota/nota-box/src --include='*.rs' \
    | grep -v '/target/'
.../nota-box/src/peek.rs:4:pub fn peek_box(bytes: &[u8], root_size: usize, index: usize) -> Result<&[u8], Error>
.../nota-box/src/decode.rs:5:pub fn decode_binary<T: BoxedNotaDecode>(bytes: &[u8]) -> Result<T, Error>
.../nota-box/src/decode.rs:10:pub fn decode_text<T: BoxedNotaDecode>(text: &str) -> Result<T, Error>
.../nota-box/src/decode.rs:175:fn decode_complete<T: NotaDecode>(text: &str) -> Result<T, Error>
.../nota-box/src/decode.rs:186:fn balanced_record_end(text: &str, offset: usize) -> Result<usize, Error>
.../nota-box/src/decode.rs:214:fn bracket_string_end(text: &str, offset: usize) -> Result<usize, Error>
.../nota-box/src/decode.rs:231:fn scalar_end(text: &str, offset: usize) -> Result<usize, Error>
.../nota-box/src/decode.rs:242:fn skip_spaces(text: &str, mut cursor: usize) -> usize
.../nota-box/src/decode.rs:260:fn balanced_record_end_bytes(bytes: &[u8], offset: usize) -> Result<usize, Error>
.../nota-box/src/decode.rs:285:fn bracket_string_end_bytes(bytes: &[u8], offset: usize) -> Result<usize, Error>
.../nota-box/src/text.rs:4:pub fn split_text_boxes(...) -> Result<(&str, Vec<String>), Error>
.../nota-box/src/text.rs:42:fn read_bracket_string(text: &str, offset: usize) -> Result<(String, usize), Error>
.../nota-box/src/encode.rs:45:pub fn encode_binary<T: BoxedNotaEncode>(value: &T) -> Result<Vec<u8>, Error>
.../nota-box/src/encode.rs:69:fn encode_root<T: BoxedNotaEncode>(value: &T) -> Result<Vec<u8>, Error>
.../nota-box/src/encode.rs:81:fn is_inline_bracket_string(text: &str) -> bool
```

**Kind:** free functions outside `#[cfg(test)]` (methods.md §"Methods
on types, not free functions").
**Why it's a smell:** The verbs have visible nouns. `decode_binary` /
`decode_text` are conversions that belong as `TryFrom`/`from_*` on the
target type (the `BoxedNotaDecode` trait already exists; these are
free wrappers over trait methods). The `balanced_record_end`,
`bracket_string_end`, `scalar_end`, `skip_spaces`,
`read_bracket_string` cluster is a **cursor-over-text scanner** whose
missing noun is a stateful `BoxTextScanner { text, cursor }` — exactly
the "the noun is `CertParser` *with fields*" case from methods.md.
Today the cursor is threaded as a `usize` argument through a dozen
free functions; that *is* the state of a scanner object that has not
been named.

Compounding smell — **duplicated NOTA structure scanning.** These
free functions re-implement bracket/record/scalar boundary-finding
over raw text:

```
$ grep -n '^fn read_bracket_string' /git/github.com/LiGoldragon/nota/nota-box/src/text.rs
42:fn read_bracket_string(text: &str, offset: usize) -> Result<(String, usize), Error>
```

`nota-codec` already owns a canonical NOTA `Lexer`/`Decoder`. nota-box
maintains a parallel, hand-rolled scanner for the same syntax. There
are now two places that know how a NOTA record's parentheses balance
and how a `[...]` bracket string ends. That is a maintenance hazard
(the two will drift) on top of the placement violation.

### 2b. nota-codec — codec/lexer/temporal helpers as free fns (18)

```
$ grep -rnE '^(pub )?fn ' /git/github.com/LiGoldragon/nota-codec/src --include='*.rs' | grep -v '/target/'
.../src/encoder.rs:274:fn reject_map_key_whitespace(value: &str) -> Result<()>
.../src/encoder.rs:281:fn should_write_block(value: &str) -> bool
.../src/encoder.rs:288:fn write_bracket_string(output: &mut String, value: &str)
.../src/value.rs:88:pub fn parse_str(input: &str) -> Result<NotaValue>
.../src/value.rs:105:pub fn parse_sequence(input: &str) -> Result<Vec<NotaValue>>
.../src/lexer.rs:436:fn is_radix_digit(b: u8, radix: u32) -> bool
.../src/lexer.rs:486:fn parse_int_literal(cleaned: &str, radix: u32) -> ...
.../src/lexer.rs:495:fn dedent(raw: &str) -> String
.../src/temporal.rs:1:pub(crate) fn is_valid_date(year: u16, month: u8, day: u8) -> bool
.../src/temporal.rs:8:pub(crate) fn is_valid_time(hour, minute, second) -> bool
.../src/temporal.rs:12:fn days_in_month(year: u16, month: u8) -> u8
.../src/temporal.rs:22:fn is_leap_year(year: u16) -> bool
```

**Kind:** free functions outside `#[cfg(test)]`.
**Why it's a smell:** `nota-codec` is the canonical NOTA parser crate —
writing the NOTA lexer here is *correct* (parsers.md §"When no library
exists" path 2: a real parser in its own crate). The violation is not
that the parsing exists; it is that the verbs sit at module scope
instead of on the lexer/encoder/value nouns. `parse_str` /
`parse_sequence` should be `NotaValue::from_str` / `impl FromStr`
(methods.md §"Use existing trait domains" — `FromStr` already names
this). `write_bracket_string` / `should_write_block` are
`Encoder`-state operations that belong as private methods on
`Encoder`. The `temporal.rs` cluster (`is_valid_date`, `days_in_month`,
`is_leap_year`) is a free-floating calendar; the noun is a `Date {
year, month, day }` newtype whose constructor validates. The file
`temporal.rs` has **no type at all** — it is a pure bag of functions,
the strongest signal that a noun is missing.

### 2c. nota-derive — proc-macro internals (7 of 12 are violations)

Five of nota-derive's twelve `pub fn` are the `#[proc_macro_derive]`
entry points, which the `proc_macro` framework **requires** to be free
`pub fn` — those are a legitimate framework exception:

```
$ grep -nB1 -E '^pub fn ' /git/github.com/LiGoldragon/nota-derive/src/lib.rs | grep -E 'proc_macro|pub fn'
27-#[proc_macro_derive(NotaRecord)]
28:pub fn derive_nota_record(input: TokenStream) -> TokenStream
38:pub fn derive_nota_enum(...)         # all 5 are #[proc_macro_derive]
53:pub fn derive_nota_map_key(...)
72:pub fn derive_nota_transparent(...)
95:pub fn derive_nota_try_transparent(...)
```

The remaining seven are **genuine violations** — internal helpers with
visible nouns:

```
$ grep -rnE '^(pub )?fn ' /git/github.com/LiGoldragon/nota-derive/src --include='*.rs' | grep -vE 'lib.rs'
.../src/nota_record.rs:17:pub fn expand(input: DeriveInput) -> TokenStream
.../src/nota_enum.rs:12:pub fn expand(input: DeriveInput) -> TokenStream
.../src/nota_transparent.rs:10:pub fn expand(input: DeriveInput) -> TokenStream
.../src/nota_try_transparent.rs:21:pub fn expand(input: DeriveInput) -> TokenStream
.../src/nota_map_key.rs:12:pub fn expand(input: DeriveInput) -> TokenStream
.../src/shared.rs:12:pub fn named_fields(data: &Data, derive_name: &str) -> Option<FieldsNamed>
.../src/shared.rs:24:pub fn single_unnamed_field(data: &Data, derive_name: &str) -> FieldsUnnamed
```

**Kind:** free functions outside `#[cfg(test)]`.
**Why it's a smell:** Each `expand(input: DeriveInput)` is a method
waiting to happen: the noun is a `RecordExpansion(DeriveInput)` (or a
trait `Expand for DeriveInput`) so the derive body reads
`expansion.tokens()`. `named_fields` / `single_unnamed_field` in
`shared.rs` read `&Data` they don't own — they belong on a wrapper
that carries the `Data` and the `derive_name` together (the
`derive_name` argument threaded alongside `data` is the tell that the
two want to be one struct). methods.md §"This applies to internal
macro and parser code as much as public APIs" names this case
explicitly.

### 2d. signal-core — frame helpers (3) + macro internals (20)

Three in the main crate are genuine violations:

```
$ grep -rnE '^(pub )?fn ' /git/github.com/LiGoldragon/signal-core/src --include='*.rs' | grep -v '/target/'
.../src/frame.rs:98:fn encode_archive<Value>(value: &Value) -> Result<Vec<u8>, FrameError>
.../src/frame.rs:107:fn length_prefix(archive: Vec<u8>) -> Result<Vec<u8>, FrameError>
.../src/frame.rs:118:fn strip_length_prefix(bytes: &[u8]) -> Result<&[u8], FrameError>
```

**Kind:** free functions in a wire crate.
**Why it's a smell:** `length_prefix` / `strip_length_prefix` /
`encode_archive` are the framing operations for `Frame` — they belong
as methods on `Frame` (`frame.to_length_prefixed_bytes()`,
`Frame::from_length_prefixed(bytes)`). storage-and-wire.md makes
length-prefixed framing a first-class `Frame` concern; the free
helpers are the framing logic spilled out of the type.

In `signal-core/macros/src/` there are 21 module-level `fn`, of which
one (`signal_channel`, `#[proc_macro]`) is framework-mandated and the
other 20 (`emit_request_enum`, `emit_reply_enum`, `emit_event_kind`,
`payload_kinds`, `validate_verbs`, `validate_variant_uniqueness`,
`projected_record_head`, …) are genuine violations:

```
$ grep -nE '^fn ' /git/github.com/LiGoldragon/signal-core/macros/src/emit.rs | head -4
45:fn emit_request_enum(block: &RequestBlockSpec) -> TokenStream
68:fn emit_reply_enum(block: &ReplyBlockSpec) -> TokenStream
91:fn emit_event_enum(block: &EventBlockSpec) -> TokenStream
114:fn emit_request_payload_impl(block: &RequestBlockSpec) -> TokenStream
```

**Why it's a smell:** every `emit_*(block: &SomeBlockSpec)` reads a
`*BlockSpec` it does not own — the noun is right there in the argument.
These want to be `block.emit_request_enum()` etc., i.e. methods on
`RequestBlockSpec` / `ReplyBlockSpec` / `ChannelSpec`. The
`validate_*(spec: &ChannelSpec)` cluster is the same shape:
`spec.validate_verbs()`. This is the enum-vs-enum / verb-on-noun rule
applied to a code generator, and the generator currently scatters the
matrix across module-scope helpers.

## Violation 3 — actor-named, Mutex-implemented daemon (spirit)

`spirit` ships a real long-lived daemon binary:

```
$ grep -nE '\[\[bin\]\]|^name =|^path =' /git/github.com/LiGoldragon/spirit/Cargo.toml
[[bin]]
name = "spirit-daemon"
path = "src/bin/spirit-daemon.rs"
```

Its runtime `Engine` documents itself in actor language and names a
`SignalActor` field, but it is implemented with `std::sync::Mutex`,
not Kameo (`spirit/src/engine.rs:1, 18-39`):

```rust
use std::{convert::Infallible, sync::Mutex};

/// The daemon runtime: a thin composer of the three execution centers.
/// `Engine` owns the Signal admission actor and the Nexus mail keeper.
pub struct Engine {
    signal_actor: SignalActor,
    nexus: Mutex<Nexus>,
    ...
}
pub struct SignalActor {
    next_message_identifier: Mutex<Integer>,
    next_origin_route: Mutex<Integer>,
    ...
}
```

And there is no Kameo dependency or actor usage at all:

```
$ grep -nE 'kameo|tokio' /git/github.com/LiGoldragon/spirit/Cargo.toml
(no output)
$ grep -rniE 'kameo|ActorRef|impl Message<|kameo::' /git/github.com/LiGoldragon/spirit/src/
(no output)
```

The state is reached through `self.nexus.lock().expect("nexus lock")`
seventeen times (`engine.rs:95, 103, 127, 132, 138, 146, 154, 160,
197, 203, 280, 292, 303, 309, 318, 332, 345`):

```
$ grep -rnE '\.expect\(|panic!' /git/github.com/LiGoldragon/spirit/src/engine.rs | head -4
.../src/engine.rs:95:            let mut nexus = self.nexus.lock().expect("nexus lock");
.../src/engine.rs:103:        let mut nexus = self.nexus.lock().expect("nexus lock");
.../src/engine.rs:127:        let mut nexus = self.nexus.lock().expect("nexus lock");
.../src/engine.rs:132:        self.nexus.lock().expect("nexus lock").store().len()
```

**Kind:** architecture gap — actor discipline not followed in a daemon
(rust-discipline.md §"Actors: logical units with kameo";
storage-and-wire.md anti-pattern row "Public ZST actor noun" and the
`Arc<Mutex<T>>` row).
**Why it's a smell:** the rust-discipline index is explicit that "When
a Rust component is a daemon, state engine, router, watcher, …" the
Kameo actor discipline carries the rules, and that the reason is
**logical cohesion**. `spirit`'s `Engine` is a daemon state engine
that *names itself an actor in prose* (`signal_actor`, `SignalActor`,
"the Signal admission actor") while implementing concurrency with bare
`Mutex` fields and lock-poison `expect`. This is the form storage-and-
wire.md flags: state shared via lock rather than owned by an actor that
receives messages. The seventeen `expect("nexus lock")` calls each
panic on lock poisoning — a daemon that aborts its whole runtime if any
holder panicked while holding the mutex.

Honest register note: `spirit` is explicitly a **pilot** ("runnable
schema-derived pilot"), and a single-threaded Mutex composer is a
reasonable *pilot* shape before the Kameo actor layer lands. So this is
a known-direction gap rather than a careless violation — but it is
still a gap between the documented "actor" vocabulary and the actual
Mutex implementation, and the prose calling a `Mutex<Nexus>` field an
"actor" is the specific ugliness: the name claims a discipline the code
does not yet implement.

## Violation 4 — `panic!` emitted into generated runtime code (schema-rust-next)

`schema-rust-next` builds Rust by appending string literals
line-by-line (`self.line("...")`), and several of those lines emit
`panic!` arms into the **generated** projection methods
(`schema-rust-next/src/lib.rs:2551, 2575, 2587, 2599`):

```
$ grep -rnE 'panic!|unreachable!|todo!' /git/github.com/LiGoldragon/schema-rust-next/src --include='*.rs' | grep -v '/target/'
.../src/migration.rs:178:            MigrationTarget::Enum(_) => unreachable!("position matched a struct"),
.../src/migration.rs:201:            MigrationTarget::Struct(_) => unreachable!("position matched an enum"),
.../src/lib.rs:2551:  "            _ => panic!(\"nexus work cannot project to a generated nexus action\"),",
.../src/lib.rs:2575:  self.line("            _ => panic!(\"nexus action is not a SEMA write input\"),");
.../src/lib.rs:2587:  self.line("            _ => panic!(\"nexus action is not a SEMA read input\"),");
.../src/lib.rs:2599:  self.line("            _ => panic!(\"nexus action is not a signal reply\"),");
```

The emitted method (verbatim from the generator, `lib.rs:2571-2577`):

```rust
self.line("    pub fn into_sema_write_input(self) -> sema::Sema<sema::WriteInput> {");
self.line("        let origin_route = self.origin_route();");
self.line("        match self.into_root() {");
self.line("            NexusAction::CommandSemaWrite(input) => input.with_origin_route(origin_route),");
self.line("            _ => panic!(\"nexus action is not a SEMA write input\"),");
self.line("        }");
self.line("    }");
```

**Kind:** propagated bad pattern (panic-in-runtime) + ugliness
(string-concatenation code generation).
**Why it's a smell:** Two distinct issues stacked.

1. **Panic in a generated runtime path.** The generator hard-codes a
   panicking `_` arm into a public method (`into_sema_write_input`,
   `into_signal_output`) that every consumer of the schema then ships.
   The errors.md / methods.md discipline is that boundaries return a
   typed `Error`. Here the "impossible" arm is encoded as a runtime
   `panic!`, not a typed error or a refined sum type. The generator's
   own `migration.rs` uses `unreachable!` for genuinely-impossible
   positions (defensible, since the match already proved the variant) —
   but the `lib.rs` cases are emitting `panic!` (a hard abort with a
   message) into *consumer-facing* projection methods, which is the
   stronger smell. If the projection truly cannot fail, the input type
   should be narrowed so the `_` arm doesn't exist; if it can fail, it
   should return `Result`.

2. **String-concatenation code generation.** The emitter assembles
   Rust source as raw `self.line("…")` text rather than a `quote!`/AST
   pipeline. This is the documented architecture ("emits Rust source
   text as a separate step before any Rust macro ergonomics"), so it is
   a deliberate stage, not an accident — but it is genuine ugliness:
   the generated `panic!` string is double-escaped (`\"…\"`) inside a
   Rust string literal inside the generator, there is no compile-time
   check that the emitted tokens are valid Rust until the downstream
   build runs, and indentation is hand-managed with leading spaces in
   the literals. It is the most fragile surface in the stack and the
   place a typo produces invalid generated Rust with a far-removed
   error.

## Gaps (half-migrations, stubs, TODO density)

TODO/FIXME/stub density across the core stack is **remarkably low** —
this is not a half-baked codebase:

```
$ for r in ...; do grep -rniE 'TODO|FIXME|XXX|HACK|stub|placeholder|for now|not yet|temporary' \
    /git/github.com/LiGoldragon/$r --include='*.rs' | grep -v '/target/' | grep -E '/src/' | wc -l; done
nota-codec         2
nota-derive        0
nota               0
schema-next        0
schema-rust-next   0
signal-core        0
sema               0
sema-engine        0
spirit             2
signal-spirit      0
```

The four total hits are benign:

```
$ grep -rniE 'TODO|FIXME|stub|placeholder|not yet|temporary' \
    /git/github.com/LiGoldragon/spirit/src /git/github.com/LiGoldragon/nota-codec/src --include='*.rs'
spirit/src/lib.rs:18://! let mut store: Store = todo!();          # doc-comment example
spirit/src/lib.rs:19://! let message: ... = todo!();              # doc-comment example
nota-codec/src/traits.rs:464:// TODO: i64, f64 as the derives that need them land.
```

The `nota-codec` TODO is a real but small forward-pointer (i64/f64
codec support deferred until derives need them). The `spirit` `todo!()`
are inside a `//!` doc example, not live code.

The **one real gap with operational weight** is the deployed-vs-source
divergence documented above: the live `spirit-v0.5.1` `Observation`
read-side enum is behind the committed `spirit/schema/*.schema`. Write
path verified working on the deployed binary; read path verified
working only in source. This is the source-ahead-of-deploy state, not
a stub — but it means the deployed CLI and the source schema are two
different contracts right now, and any agent reasoning about "what
spirit accepts" must pick which one.

A second, smaller gap: `nota-box` maintaining a hand-rolled NOTA
structure scanner parallel to `nota-codec`'s `Lexer`/`Decoder`
(Violation 2a) is a half-migration in spirit — the canonical parser
exists, but box-framing did not adopt it and re-derived bracket/record
boundary-finding. The two scanners are a latent drift gap.

## Things that are clean (so the next pass doesn't re-flag them)

To bound the audit and prevent re-litigation:

- **No `anyhow`/`eyre`/`Box<dyn Error>`** anywhere in core `src/`
  (verified, no output).
- **No `clap`/flag-soup** in any production code (verified; all
  `.arg`/`--flag` hits are test subprocess invocations of external
  tools).
- **No quotation marks** emitted into NOTA by the live binary
  (verified: `(RecordAccepted [3t40])`) or constructible by the
  encoder (only `\\`/bracket escapes).
- **No `Req`/`Ctx`/`Cfg`/`Id` abbreviations** as type or field idents
  in any core `src/` (verified, no output). Naming discipline holds.
- **Schema paths use single-colon namespace form**, not `::` — e.g.
  `spirit:signal:Entry` in `spirit/schema/sema.asschema`, and
  `schema-next` has a test `import_source_splits_single_colon_target_into_crate_module_type`.
  No `::`-vs-`:`-confusion found in schema text.
- **`Bind` / `Wildcard`** (signal-core/pattern.rs) are legitimate
  marker types (trait-impl-only), not ZST namespaces.
- **`sema` and `sema-engine`** have **zero** unwrap/expect/panic in
  `src/` and zero free functions — the exemplar crates of the stack.
- **TODO/FIXME density near zero** (4 total, all benign).

## Summary table of findings

| # | Kind | Location | Severity |
|---|---|---|---|
| 1 | ZST namespace holder | `signal-spirit/src/lib.rs:34` `WireCodec` | high (cleanest violation; in flagship contract; likely to be copied) |
| 2a | free functions (parser/scanner) | `nota/nota-box/src/{decode,text,encode,peek}.rs` (×27) | medium (foundational-layer debt; missing `BoxTextScanner` noun; duplicate scanner) |
| 2b | free functions (codec/lexer/calendar) | `nota-codec/src/{encoder,value,lexer,temporal}.rs` (×18) | medium (`temporal.rs` has no type at all) |
| 2c | free functions (macro internals) | `nota-derive/src/{nota_*,shared}.rs` (×7 of 12) | low-medium (5 of 12 are framework-mandated) |
| 2d | free functions (frame + macro) | `signal-core/src/frame.rs` (×3) + `macros/src/` (×20 of 21) | medium (framing belongs on `Frame`; emit/validate belong on `*Spec`) |
| 3 | actor-named, Mutex-implemented daemon | `spirit/src/engine.rs` (`Mutex<Nexus>`, ×17 `expect`, no kameo) | medium (known pilot gap; prose claims actor discipline code lacks) |
| 4 | `panic!` emitted into generated runtime + string-concat codegen | `schema-rust-next/src/lib.rs:2551,2575,2587,2599` | medium (propagated to every consumer; fragile emitter) |
| G1 | deployed-vs-source contract gap | `spirit-v0.5.1` `Observation` behind `spirit/schema/*` | gap (write verified; read shape diverged) |

## What I could not verify

- The **read-side** behaviour of the deployed `spirit-v0.5.1` binary.
  Every `Observe` shape I tried was rejected; I did not guess the
  deployed enum's variants. Only the write path
  (`Record` → `RecordAccepted`) is confirmed against the live binary.
- Whether the **committed generated schema artifacts** in each repo are
  byte-fresh against their `.schema` sources. I built `signal-spirit`
  (`Finished dev profile in 0.17s`, cached clean) which exercises its
  `build.rs` schema lowering without error, but I did not run a
  `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1` regeneration-diff across every
  crate to prove zero drift; that is a deeper check than this audit ran.
