---
title: 496 - Psyche - schema-stack state and the decisions waiting on you
role: designer
variant: Psyche
date: 2026-06-04
topics: [schema-stack, next-stack, abstraction, runner-loop, emission, symbol-path, constraint-witness, ratification]
description: |
  The psyche-facing low-down after a five-agent design-to-code port audit
  of the schema-derived next stack. How it is going (well — most recent
  intent is landed and clean), the one real bug, and the handful of
  abstraction decisions that are now waiting on your ratification, each
  shown with the actual code and a recommendation marked as a lean, not a
  fait accompli.
---

# 496 - Schema-stack state and the decisions waiting on you

This is the low-down after auditing the schema-derived next stack against
your recent intent, with five sub-agents each taking a slice. The full
audit and the per-slice detail live in the meta-report directory
`reports/designer/495-design-to-code-port-audit-2026-06-04/`; this report
is the part that needs *you*.

## How it is going: well, and that is the real headline

The honest top-line is reassuring. Over the last few days you poured a
dense run of intent into the schema stack — strings only at the edges,
trace as a typed interface, symbols as paths, alias-vs-newtype lowering,
bare-name headers, multi-pass parsing — and the operator has already
manifested almost all of it into clean code. The audit went in expecting
to find a backlog of unimplemented design and instead found the opposite:
the recent mechanisms are not just present, they are well-built and, in
most cases, already witnessed by behavioral tests.

Concretely, all of these are landed and clean: alias-vs-newtype lowering
end to end (a bare `Rejected SignalRejection` binding becomes
`pub type Rejected = SignalRejection;`, and a caller writes
`Output::rejected(reason)` with no wrapper nesting); the engine-trait
lifecycle hooks, wired in the SEMA→Nexus→Signal order; the daemon's binary
string boundary (the daemon never decodes NOTA — it is gated behind a
feature the daemon binary does not enable); trace as a typed schema
interface with binary frames and text only at the client edge; and typed
SymbolPaths with their role recovered from the schema. The witness
coverage is genuinely good.

So the work that remains is not "build the design." It is three things:
one real bug, some missing constraint witnesses, and a set of *abstraction
decisions that are now waiting on you*. The rest of this report is those
three, with the code.

## The one real bug: schema-next has two lowering engines and they disagree

This is the find I most want you to see. `schema-next` lowers an authored
schema two different ways through two bodies of code that share nothing:
the typed-source path (`SchemaSource::lower`, which is the only path
production actually uses) and the registry document path
(`lower_source`, which is what every test and the README exercise). Your
[bare root headers list exported object names, and a bare header variant
that resolves to a namespace declaration carries that same-named payload]
(records 1555/1562) intent is implemented on the source path only. The
registry path silently drops the payload:

```rust
// src/declarative.rs:1839 — the registry path
} else if self.object.qualifies_as_pascal_case_symbol() {
    Ok(EnumVariant {
        name: self.object.schema_name()?,
        payload: None,          // <-- no namespace lookup, no resolution
    })
}
```

Lowering the *same* schema both ways proves the divergence is real, not
theoretical: the source path returns `payload = Some(Lookup)` and the
registry path returns `payload = None`. The reason no test has ever caught
this is the quiet one — the equivalence test that asserts the two paths
agree (`schema_source_lowers_to_same_asschema_as_direct_source`) uses a
fixture that never contains a bare header name, so the two paths agree
there by construction. This is precisely the failure mode behind your
[audit implementation against intent for missing constraint witnesses; add
tests that prove the intended path instead of leaving the intent as prose]
(record 1565): the missing witness is the one that would have exposed the
bug.

**My lean, for your decision:** unify the two engines so `SchemaSource` is
the single lowering front end (it already owns multi-pass resolution and
is the only production caller), and add the both-paths-agree witness so
this cannot recur. I lean this way rather than "patch the registry path
too" because the duplication is the disease and the divergence is only its
first symptom — the same single-field→Newtype rule is currently spelled in
three places, and the collection-reference lowering in three more, each a
place the next change can drift. This is operator-tier3 work; I have not
touched it. I want your nod on *unify* versus *keep both paths and just
patch*, because it changes how much the operator reshapes.

## The decisions waiting on you

These are the abstractions the audit surfaced. Each is a real instance of
your [repeated construction signals bad design or a missing logic/emission
layer] (record 1557), generalized to the whole stack. For each I give the
code, a recommendation marked as a **lean** (not a ratification — you have
the context I do not), and the specific question.

### Decision 1 — the component runner: extract `triad_main!` now, or wait?

Every schema-derived daemon will hand-write the same runner. Today
`spirit-next` writes all of it, and of this body only `self.engine()` and
`engine.handle(input)` are component-specific:

```rust
// spirit-next/src/daemon.rs:152 — the part every daemon will copy
pub fn run(&self) -> Result<(), DaemonError> {
    if let Some(parent) = self.configuration.socket_path().parent() {
        fs::create_dir_all(parent)?;
    }
    self.remove_stale_socket()?;
    let listener = UnixListener::bind(self.configuration.socket_path())?;
    let mut engine = self.engine()?;          // component-specific
    engine.start()?;
    let engine = Arc::new(engine);
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let engine = Arc::clone(&engine);
                if let Err(error) = self.handle_stream(stream, &engine) {  // handle() is component-specific
                    eprintln!("spirit-next-daemon: {error}");
                }
            }
            Err(error) => return Err(DaemonError::Io(error)),
        }
    }
    Ok(())
}
```

The missing noun is a generic `triad-runtime` runner the component's
engine plugs into:

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

Both `triad-runtime` and `spirit-next` already say in their ARCHITECTURE
files that this extracts "when a second component would otherwise copy the
same mechanics." That is the crux: there is exactly **one** consumer today
(`spirit-next`).

**My lean:** ratify the *shape* now (so the operator builds toward it and
`spirit-next`'s runner is written as the reference implementation), but do
not extract into `triad-runtime` until the second component — `upgrade` or
`repository-ledger` — actually needs it. Premature extraction with one
consumer tends to bake in the wrong seams. **Question for you:** is that
the right call, or do you want the runner extracted now because the
`triad_main!` macro is itself a design you want to pin early?

### Decision 2 — the emission core: ratify the `RustItem` token model?

`schema-rust-next` builds Rust source by calling one primitive,
`self.line(...)`, **504 times**, almost always as
`self.line(format!("..."))` with the indentation counted out by hand:

```rust
self.line(format!("impl {name} {{"));
self.line(format!("    pub fn new(payload: {payload_type}) -> Self {{"));
self.line("        Self(payload)");
self.line("    }");
// ... 500 more like this, including escaped Rust inside Rust string fragments
```

Your own intent for this repo already names the destination —
[Rust emission is data before it is text; the emitter maps Asschema into a
typed RustModule object, and rendering RustModule produces RustCode]. The
*type declarations* honor that (they are real `RustModule` / `RustEnum`
data). But the ~80% of output that is impl blocks, trait bodies, and match
arms never reaches a data model — it is string-templated directly. The
hand-counted `"    "` / `"        "` indentation is the symptom; the
duplication (the `route()` match emitted verbatim twice, the
`TypeReference` recursion written three times, the lifecycle preamble
three times) is the cost.

**My lean:** yes, ratify a small `RustItem` / `RustImplBlock` / `RustMatch`
token model that the writer renders once, with the writer owning
indentation depth. It is a meaningful operator refactor, but it is the
honest completion of a discipline you already stated, and it makes the
four-space miscounts structurally impossible. **Question:** do you want
this as a near-term operator priority, or parked until the schema grammar
itself settles (since the emitter changes whenever the grammar does)?

### Decision 3 — confirm the SymbolPath shape as canonical

You raised SymbolPath as [every typed symbol has a fully-qualified
identity expressed as a path; the path mechanism is canonical, not
per-design] (records 1506/1507). What landed is a flat segment vector with
the structural role recovered separately from the schema:

```rust
// schema-next/src/asschema.rs:85
pub struct SymbolPath(Vec<Name>);
// role is data-derived, not guessed from segment count:
// Asschema::symbol_path_position(&self, &SymbolPath) -> SymbolPathPosition
//   { Type | RootVariant | EnumVariant | Field }
```

An earlier open question was whether SymbolPath should instead be a
structured five-field record (`component / plane / variant / payload /
field`). The audit's read is that the flat-vector-plus-schema-derived-role
shape is the *better* realisation of your intent: the stored path stays a
plain segment vector so deeper schema positions can grow without changing
the binary object, and the role is read from the schema rather than
guessed — which is exactly [role is data-derived from the schema] rather
than encoded in the type's arity. The one thing not yet true is
canonicality: SymbolPath is constructed and read only inside `schema-next`
today; the trace / help / emission consumers that would make it the one
identity space across the stack live downstream and do not consume it yet.

**My lean:** confirm the flat-`Vec<Name>`-plus-position-recovery shape as
the ratified canonical form and close the structured-record alternative.
**Question:** do you agree, or do you still want the structured record —
the tradeoff is role-opacity when a path crosses a boundary without its
schema (a bare SymbolPath cannot report its own role), which the structured
record would carry inline.

### The smaller abstractions (no decision needed, listed for completeness)

Three more repetitions are clear enough that they are operator cleanup, not
ratification questions: the 4-byte length-prefix framing is implemented
three times (trace, transport, schema-emitted frame) and wants one
`LengthPrefixedFrame` codec; the single-NOTA-argument rule is hand-rolled
twice with divergent error vocabularies and wants a `ComponentArgument`
typed sum (inline-NOTA / NOTA-file / rkyv-file) instead of a
`starts_with('(')` string sniff; and four `spirit-next` error enums
hand-write the `Display`+`Error`+`From` ceremony that `thiserror` (already
used in `triad-runtime`) dissolves.

## What I built as a concept this session

To engage the directive to port missing design into implementation
concretely rather than only proposing, I built a demo/concept — the audit's
highest-value manifestation target — in `triad-runtime`, on the concept
branch `designer-strings-at-edges-2026-06-04` (commit `0c079c79`), pushed
for the operator to review and integrate. Per record 1568 this is **not
landed**: it has no material existence until an operator integrates it to
main — it is a concept awaiting that integration. It does two things.

First, it turns your [strings only at the edges] intent into falsifiable
tests for the trace wire, where before it was prose. The binary-frame
witness:

```rust
#[test]
fn trace_frame_is_length_prefixed_binary_not_the_display_text() {
    let event = ExampleTraceEvent::new("SemaWriteApplied");
    let frame = TraceFrame::new(event.clone()).to_bytes().expect("frame bytes");
    let archive_length = u32::from_be_bytes(frame[..4].try_into().expect("length prefix")) as usize;
    assert_eq!(archive_length, frame.len() - 4,
        "the frame is a four-byte length prefix followed by that many rkyv archive bytes");
    let archive = &frame[4..];
    assert_ne!(archive, event.to_string().as_bytes(),
        "the wire carries the rkyv archive, not the Display text");
    let decoded = ExampleTraceEvent::from_trace_archive(archive).expect("decode archive");
    assert_eq!(decoded, event);
}
```

plus a second witness that drives a `u32`-only `CounterTraceEvent` (no
string field at all) through the same generic surface, proving the runtime
holds no vocabulary of its own. Second, it states the three trace-edge
invariants as constraints with their witnesses in the crate's
ARCHITECTURE.md and anchors INTENT.md to the apex records. Verified:
`cargo fmt` clean, `cargo clippy -D warnings` clean, all 11 trace tests
pass.

One honest correction worth flagging: the sub-agent first proposed a
witness asserting the frame bytes *do not contain* the event's display
string. Reading the real code, that would fail — rkyv archives a `String`
field as its UTF-8 bytes, so the name *is* present in the frame. The
correct witness is structural (length-prefix shape and round-trip), which
is what I landed. It is a small thing, but it is the kind of thing that
only surfaces by reading the actual types, and I would rather show you the
correction than a confident-but-wrong test.

## Why I did not scatter more code

Most of the remaining surface is either operator-tier3 (production feature
code and the bug fix — the implementing half of the dance) or
unratified (the runner, the token model — design that needs your nod before
it is built). I held those as ready-to-apply code in the slice reports
rather than pushing concept branches across four of the operator's active
repos right after their last session froze. The designer's half here was
to manifest, witness, and surface the decisions; the operator implements,
and you ratify. If you would rather I push the witness branches for the
other repos too (they are written and ready), say so and I will.

## The short version, if you read only this

The schema stack is in good shape — your recent intent is landed and clean.
There is one real bug (two lowering engines disagree on bare headers; I
lean: unify them). There are three decisions waiting on you: extract the
component runner now or on the second consumer; ratify the emission token
model; and confirm the flat SymbolPath shape as canonical. Everything else
is operator cleanup with ready code. One verified concept is pushed to a
triad-runtime branch — awaiting operator integration, not landed — as the
concrete demonstration.
