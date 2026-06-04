---
title: 495/5 - Cross-cutting repetition and abstraction sweep
role: designer
variant: Audit
date: 2026-06-04
topics: [audit, repetition, abstraction, triad-runtime, runner-loop, meta-signal-rename, component-triad, next-stack]
description: |
  Slice 5 of the design-to-code port audit. Read-only cross-repo sweep of the
  schema-derived next stack (schema-next, schema-rust-next, spirit-next,
  triad-runtime, nota-next) and the contract fleet for repetition that signals
  a missing abstraction. The dominant finding: the runner / transport /
  single-argument scaffolding that triad-runtime is meant to own is
  hand-written inside spirit-next, with length-prefix framing already copied
  three times and the single-NOTA-argument rule copied twice. Also: meta-signal
  rename status (12 owner-signal-* repos remain) and triad-shape conformance.
---

# Slice 5 — cross-cutting repetition and abstraction sweep

The psyche's named agent for this slice: [look for bad patterns, code that is
winded, repetition, any kind of repetition showing up in the code, which means
we could create another abstraction]. This is a read-only sweep across the
whole next stack. Every finding below is a proposal; nothing is ported here.

## Top abstraction opportunities, ranked by leverage

| Rank | Opportunity | Where it repeats today | Classification |
|---|---|---|---|
| 1 | The component runner: transport + runner loop + single-NOTA-argument command | `spirit-next` hand-writes all of it; `triad-runtime` is the intended home | UNRATIFIED-PROPOSE |
| 2 | Length-prefixed binary frame mechanics | 3 independent copies (triad-runtime trace, spirit-next transport, schema-emitted signal frame) | UNRATIFIED-PROPOSE |
| 3 | Single-NOTA-argument parsing (the AGENTS.md single-argument rule) | `DaemonCommand` and `SpiritNextCli`, both inside spirit-next | RATIFIED-PORTABLE (the rule; the noun is unratified) |
| 4 | Hand-written `Display`/`Error`/`From` per error enum vs thiserror | config.rs, daemon.rs, transport.rs hand-write it; triad-runtime uses thiserror | RATIFIED-PORTABLE (thiserror is the named discipline) |
| 5 | Schema-emitted Rust built by raw string concatenation | one 2688-line `RustWriter` in schema-rust-next | UNRATIFIED-PROPOSE (slice 3 owns the detail) |

## 1 — The component runner is hand-written where triad-runtime should own it

This is the slice's headline. `triad-runtime`'s own ARCHITECTURE names the
trigger precisely:

> Future extraction waves may add generic daemon command scaffolding, signal
> transport, and trace-aware test harnesses. Those move here only when a second
> component would otherwise copy the same mechanics.

And spirit-next's ARCHITECTURE names the same intent from the other side
(`spirit-next/ARCHITECTURE.md:88`):

> `DaemonCommand` is the current programmatic startup noun. ... This is the
> small live step toward the generated component runner: startup behavior
> belongs to library nouns, while domain decisions belong to generated engine
> trait implementations.

So both repos agree the runner should be a shared library noun. Today it is
not. `spirit-next` hand-writes the entire runner surface and `spirit-next` is
the **only** consumer of `triad-runtime` (confirmed: only `triad-runtime` and
`spirit-next` carry `triad-runtime` in Cargo.toml). The duplication is
therefore *latent across components* but **already real inside the framing
layer** (finding 2).

The hand-written runner pieces in `spirit-next/src/daemon.rs` that a second
component would copy almost verbatim — the accept loop, stale-socket cleanup,
per-connection handling, and the `DaemonCommand` argv wrapper:

```rust
// spirit-next/src/daemon.rs:152
pub fn run(&self) -> Result<(), DaemonError> {
    if let Some(parent) = self.configuration.socket_path().parent() {
        fs::create_dir_all(parent)?;
    }
    self.remove_stale_socket()?;
    let listener = UnixListener::bind(self.configuration.socket_path())?;
    let mut engine = self.engine()?;
    engine.start()?;
    let engine = Arc::new(engine);
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let engine = Arc::clone(&engine);
                if let Err(error) = self.handle_stream(stream, &engine) {
                    eprintln!("spirit-next-daemon: {error}");
                }
            }
            Err(error) => return Err(DaemonError::Io(error)),
        }
    }
    Ok(())
}
```

Of this body, only `self.engine()` (which `Engine` to build) and
`engine.handle(input)` inside `handle_stream` are component-specific. The
accept loop, the parent-directory creation, the stale-socket removal
(`SocketPath` at `daemon.rs:208`), the `Arc` sharing, and the eprintln error
sink are identical for every schema-derived daemon. This is the
`triad_main!`-shaped duplication the frame called the canonical example: there
is **no** `triad_main!` macro or `DaemonRunner<Engine>` noun anywhere in the
fleet today (grep across triad-runtime, spirit-next, repository-ledger, upgrade
returns nothing).

**Proposed abstraction.** A generic `triad-runtime` noun
`SignalDaemon<Engine>` (or a `triad_main!` macro over it) that owns the accept
loop, socket lifecycle, and per-connection frame exchange, parameterised over
a trait the component's `Engine` implements:

```rust
// triad-runtime — proposed
pub trait SignalDaemonEngine {
    type Input;
    type Output;
    type Error: std::error::Error;
    fn start(&mut self) -> Result<(), Self::Error>;
    fn handle(&self, input: Self::Input) -> Self::Output;
}

pub struct SignalDaemon<Engine: SignalDaemonEngine> { /* socket path + engine */ }
```

This is **UNRATIFIED-PROPOSE**: the runner extraction is named as a *future*
wave in both ARCHITECTURE files, not ratified-now. With one consumer, the right
discipline is to extract on the second consumer, not preemptively — exactly
what triad-runtime's boundary text says. The proposal belongs in the psyche
report as the top abstraction lean; it is production feature code (tier-3,
operator's hand), not a designer port.

## 2 — Length-prefixed framing copied three times

The 4-byte big-endian length prefix is implemented independently in two crates,
and a third (different-but-parallel) framing lives in the schema emitter:

| Site | Constant + framing |
|---|---|
| `triad-runtime/src/trace.rs:14` | `const LENGTH_PREFIX_BYTE_COUNT: usize = 4;` + `to_be_bytes` write at `:124`, `read_exact` at `:135` |
| `spirit-next/src/transport.rs:10` | `const LENGTH_PREFIX_BYTE_COUNT: usize = 4;` + identical `write_frame`/`read_frame` at `:84`/`:93` |
| schema-emitted `encode_signal_frame`/`decode_signal_frame` (`schema-rust-next/src/lib.rs:1456`) | 8-byte short header instead of length, but the same "fixed prefix then rkyv archive bytes" shape |

The first two are byte-identical framing logic with the same constant declared
twice. `SignalTransport::write_frame`/`read_frame` and
`TraceFrame::to_bytes`/`read_from` are the same algorithm: write a u32 length
prefix, write the archive, read the prefix, read that many bytes. The trace
path also re-implements the FrameTooLarge guard that `transport.rs` has
(`transport.rs:24` vs `trace.rs:89`).

**Proposed abstraction.** A single `triad-runtime` `LengthPrefixedFrame` noun
(or `FrameCodec`) owning the u32-be prefix discipline and the FrameTooLarge
guard, consumed by both the trace socket and the signal transport. This pairs
with finding 1 — when the runner extracts into triad-runtime, the transport
extracts with it, and at that point the trace frame and the signal frame both
sit on one prefix codec. **UNRATIFIED-PROPOSE.** Note the schema-emitted
signal-frame (8-byte short header) is deliberately a *different* prefix (it
carries routing identity, not just length), so it does not fold into the same
codec — but the length-prefix layer underneath a stream still wraps it, so
there is real shared structure to name.

## 3 — The single-NOTA-argument rule is hand-rolled twice

AGENTS.md is explicit: [NOTA is the only argument language. Every component
binary (CLI and daemon) takes exactly one argument]. That rule is implemented
twice inside spirit-next, divergently:

```rust
// spirit-next/src/daemon.rs:133 — DaemonCommand (typed error, good)
fn single_argument(&self) -> Result<&str, DaemonCommandError> {
    match self.arguments.as_slice() {
        [argument] => Ok(argument),
        _ => Err(DaemonCommandError::ArgumentCount { count: self.arguments.len() }),
    }
}
```

```rust
// spirit-next/src/bin/spirit-next.rs:44 — SpiritNextCli (Box<dyn Error>, string literal)
fn single_argument(&self) -> Result<&str, Box<dyn std::error::Error>> {
    match self.arguments.as_slice() {
        [argument] => Ok(argument),
        _ => Err("expected exactly one NOTA argument or path".into()),
    }
}
```

Same `match self.arguments.as_slice()` shape, two error vocabularies. The CLI
version violates `skills/rust/errors.md` (returns `Box<dyn std::error::Error>`
at a binary boundary and builds errors from string literals). The CLI also
sniffs NOTA-vs-path by string prefix at `spirit-next.rs:52`
(`argument.trim_start().starts_with('(')`), which is the
`skills/rust/methods.md` §"Don't hide typification in strings" anti-pattern —
the single argument is *one of three typed kinds* (inline NOTA string, NOTA
file path, rkyv file path per AGENTS.md), and that distinction wants a
`ComponentArgument` enum, not a `starts_with('(')` test.

**Proposed abstraction.** A shared `ComponentArgument` noun in triad-runtime (or
nota-next) that parses argv into the one-typed-argument the rule mandates, with
a crate `Error` enum and the inline-vs-NOTA-file-vs-rkyv-file discrimination as
a typed sum, consumed by both daemon and CLI of every component. The *rule* is
RATIFIED (AGENTS.md hard override); the *noun* is UNRATIFIED-PROPOSE. The CLI's
`Box<dyn Error>` + string-literal-error is a clean tier-3 fix the operator
should make regardless of the extraction.

## 4 — Hand-written error-enum ceremony vs thiserror

`triad-runtime/src/trace.rs:72` uses `thiserror` (`#[derive(Error)]` +
`#[from]`) — the named discipline in `skills/rust/errors.md`. But the three
error enums in spirit-next hand-write the full `Display` + `std::error::Error`
+ `From` ceremony:

- `DaemonError` (`daemon.rs:17`) — 5 variants, hand-written `Display` (`:26`),
  empty `impl std::error::Error` (`:38`), and **five** hand-written `From` impls
  (`:40`-`:68`).
- `DaemonCommandError` (`daemon.rs:71`) — same shape, two `From` impls.
- `TransportError` (`transport.rs:13`) and `ConfigurationError` (`config.rs:85`)
  — same shape again.

Every one of these is the boilerplate `thiserror` exists to dissolve: the
`#[error("...")]` attribute replaces the `Display` match arm, `#[from]` replaces
each `From` impl, and `#[derive(Error)]` replaces the empty `impl
std::error::Error`. The repetition is ~30 lines per enum, four enums, all
mechanical. `triad-runtime` already proves the crate can use thiserror; the
spirit-next side is inconsistent with its own dependency.

**Proposed fix.** Convert the four spirit-next error enums to `thiserror`,
matching triad-runtime. **RATIFIED-PORTABLE discipline** (`skills/rust/errors.md`
is canonical), but the edit lands in component production source, so it is a
tier-3 operator fix, returned as a bad pattern below, not a port I make.

## 5 — schema-rust-next builds Rust by raw string concatenation

Slice 3 owns the emitter in depth; flagging it here only as the largest
within-repo winded-code instance and because it is a *cross-cutting* shape
(every emitted artifact in the stack flows through it). `schema-rust-next` is a
single 2688-line file whose `RustWriter` builds Rust source through hundreds of
`self.line(format!("..."))` calls — for example the signal-frame impl from
`lib.rs:1390` emits ~100 lines of Rust as quoted string fragments, including
escaped Rust inside Rust (`"            Self::ArchiveEncode => formatter.write_str(\"failed to encode rkyv archive\"),"` at `:1325`).

This is hand-rolled code generation where a token-builder library (`quote` /
`proc-macro2` `TokenStream`, or at minimum a small typed `RustItem` AST that
renders itself) is the named-tool answer — the same spirit as
`skills/rust/parsers.md` (if the format has a name, use the library; Rust source
*has* a name). The repetition signal is strong: `emit_route_impl` (`:1366`) and
the route arm inside `emit_signal_frame_impl` (`:1393`) emit the **identical**
`match self { Self::X(_) => Route::X, ... }` body twice. **UNRATIFIED-PROPOSE**;
deferred to slice 3's detailed proposal.

## Method-owner and ZST scan — clean

No free-function or ZST-namespace violations found in the slice's hand-written
runtime code. Positive observations:

- `SocketPath` (`daemon.rs:208`) is a real data-bearing noun (`path: &Path`)
  owning `remove_stale` — the stale-socket verb is correctly on a noun, not a
  free function.
- The projection verbs are correctly `impl From` or direction-named methods:
  `RustImport::from_resolved_import`, `RustField::from_asschema_field`, the
  newtype `From<Payload>` impls. No `fn project_x_to_y` free functions.
- `CollectionScan<'asschema>` (`schema-rust-next/src/lib.rs:621`) is the one
  borderline ZST-shaped type — it holds `asschema: &Asschema` (a borrow, so
  non-zero-sized) and its `map_key_type_names` reads that field, so it passes
  the §"No ZST method holders" test (erase its name and the borrow it carries
  disappears). Its private `collect_*` helpers are associated functions on the
  same type, which is acceptable, though they could be methods reading
  `self.asschema`. Minor; not a violation.
- The `EnumConstructorPayload` / `SplitSemaProjection` / `TraceInterfaceRoot`
  helper structs (`lib.rs:711`-`749`) are real data-bearing aggregates that
  satisfy one-object-in/out, not tuple smuggling. Good.

## meta-signal rename status (record 1567)

Status reporting only, not a port. Operator report 300
(`reports/operator/300-meta-signal-rename-pass-2026-06-03.md`) landed the
upgrade triad rename (`owner-signal-upgrade` → `meta-signal-upgrade`) and the
canonical guidance, and explicitly scoped the rest as a remaining gap. My sweep
confirms the fleet state:

Twelve `owner-signal-*` repos remain on disk under `/git/github.com/LiGoldragon/`:
`owner-signal-agent`, `owner-signal-cloud`, `owner-signal-domain-criome`,
`owner-signal-mind`, `owner-signal-orchestrate`, `owner-signal-persona`,
`owner-signal-persona-spirit`, `owner-signal-repository-ledger`,
`owner-signal-router`, `owner-signal-sema-upgrade`, `owner-signal-terminal`,
`owner-signal-version-handover`. Plus `core-signal-spirit` (legacy predecessor
name, report 300 says it should move to `meta-signal-spirit` in its own slice).

`protocols/active-repositories.md` **still lists** the `owner-signal-*` repos by
name (e.g. `owner-signal-version-handover`, `owner-signal-persona`,
`owner-signal-router`, etc.). Per report 300 this is **intentional and
consistent**: [the live repo map should stay accurate until each repo is
renamed]. So the map is not stale — it correctly mirrors disk. The
inconsistency would be the *reverse* (renaming the map before the repos). No
action for this audit; the rename is OPERATOR-ACTIVE fleet work.

One worth flagging to the psyche: the rename is a 12-repo + 1-legacy cascade
with per-repo remote-rename ordering and dependency edges (report 300 hit a
transitive `signal-persona-spirit` schema-parse failure from a broad
`cargo update`). That is a meaningful chunk of OPERATOR-ACTIVE work still
outstanding, not a one-pass sweep.

## Component-triad shape conformance

The next-stack contract fleet does broadly follow daemon + `signal-<c>` +
`meta-signal-<c>` (the policy leg in transition from `owner-signal-<c>`).
Observed divergences worth noting, none blocking:

- `signal-persona` is a **retired compatibility shim** (per active-repositories)
  — fine, it is named as retired and new code depends on `owner-signal-persona`
  / `signal-engine-management`. Triad-shape exception is documented.
- The next-stack pilot (`spirit-next`) is a single runnable daemon repo, not yet
  split into the three-leg triad — appropriate, it is a pilot proving the
  schema→emit→daemon path, not a production component. No meta-signal/working-
  signal split is expected of it yet.
- `core-signal-spirit` is the one genuinely-off name (neither `signal-` nor
  `meta-signal-` nor `owner-signal-`); report 300 already flags it for a
  dedicated rename slice.

No new triad-shape violation found beyond what report 300 already tracks.
