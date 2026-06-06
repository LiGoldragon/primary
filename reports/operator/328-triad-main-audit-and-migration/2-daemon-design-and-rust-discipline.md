# 328/2 — triad_main daemon design & Rust discipline audit

Operator-lane audit of the **emitted daemon module** (`triad_main`, design
542 / handoff 543) along the dimension **daemon design & Rust discipline**.
Read-only. Work audited on branch `origin/designer-daemon-emit-2026-06-06`
across schema-rust-next (the emitter), spirit (the pilot's emitted output +
hand-written hooks), and triad-runtime (`DaemonConfiguration` + `ExitReport`).

## What I checked

- The emitter source: `schema-rust-next-daemon-emit/src/daemon_emit.rs`
  (807 lines) — what shape it emits and how.
- The emitted result: spirit `src/schema/daemon.rs` (the generated module).
- The supporting traits: triad-runtime `src/process.rs`
  (`DaemonConfiguration`, `ExitReport`).
- The hand-written component side: spirit `src/daemon.rs`
  (`impl ComponentDaemon for SpiritDaemon`), `src/config.rs`,
  `src/bin/spirit-daemon.rs`.
- The non-daemon emission path in `src/lib.rs` (the `ToTokens` family + the
  `syn::parse2`/`prettyplease` finalize at lib.rs:2916-2919) to establish the
  4np2 baseline the daemon emitter is measured against.
- `skills/rust/methods.md`, `skills/rust/errors.md`, design 542, handoff 543.

## Verdict in one line

**The emitted SHAPE is sound** — the `ComponentDaemon` hook surface, the
decode→execute→encode spine, `DaemonConfiguration`, `DaemonError`, and
`ExitReport::from_result` are all discipline-faithful (methods on
data-bearing nouns, one typed `Error` enum, single-argument rule honoured,
no ZST namespaces in the emitted output). **The EMITTER that produces that
shape is not** — it is a 465-construct hand-rolled string code generator that
flatly violates 4np2, and it carries a dead-code stream-type computation. The
emitted output is also never parse-validated at emission time, unlike every
other target in the crate. So: ship the design, rewrite the emitter.

## Flaws

### BLOCKER — 4np2: the daemon emitter is a string code generator, not token-based

`daemon_emit.rs` emits the entire daemon module by pushing string literals
into a `String` buffer. Concretely:

- `quote!` occurrences in `daemon_emit.rs`: **0**.
- `self.line(...)` / `self.blank()` / `push_str` / `format!` constructs:
  **465** across 807 lines.
- The whole module is rendered by `DaemonModuleWriter` (daemon_emit.rs:197),
  whose fields are just `output: String` + `generator_name: String`
  (daemon_emit.rs:198-199), and whose `finish()` (daemon_emit.rs:219-221)
  hands back the raw `String`.

This is the *exact* construct 4np2 (VeryHigh, 2026-06-06) forbids, and it is
the construct Gap 1 (`4ac90de` on schema-rust-next main) already eliminated
everywhere else. The rest of the crate emits through `impl ToTokens` — there
are ~30 `ToTokens` impls in `src/lib.rs` (e.g. `RustStructTokens`,
`RustEnumTokens`, `NexusEngineTraitTokens`, `SignalEngineTraitTokens`,
`SemaEngineTraitTokens` at lib.rs:1478-2566) — and finalizes them at
`src/lib.rs:2916-2919`:

```rust
fn emit_item_tokens(&mut self, tokens: TokenStream) {
    let file = syn::parse2::<syn::File>(tokens).expect("generated Rust item tokens parse");
    let source = prettyplease::unparse(&file);
    self.output.push_str(source.trim_end());
    self.output.push('\n');
}
```

The daemon path bypasses all of it. At `src/build.rs:416-424` the daemon
shape branch calls `DaemonModule::new(...).to_generated_file()`, which routes
to `DaemonModule::render` → `DaemonModuleWriter` → raw string; the `None`
branch (every other target) routes through `RustEmitter` →
`emit_item_tokens` → `syn::parse2` + `prettyplease`. The daemon emitter is the
single remaining island of the old style.

**Fix:** port `daemon_emit.rs` to the same token discipline as the rest of the
crate. Each emitted item (`ComponentDaemon` trait, `DaemonCommand`,
`DaemonBinder`, `WorkingTransport`, `EmittedSubscriptions`,
`GeneratedDaemonRuntime`, `ListenerTier`, the `MultiListenerRuntime`/
`DaemonRuntime` impls, `DaemonError`, `DaemonEntry`) becomes its own
`…Tokens` struct carrying the data it needs (the shape, the stream presence,
the working-module identifier) with an `impl ToTokens`, emitted through
`emit_item_tokens` so it is `syn`-parsed and `prettyplease`-formatted like
everything else. The trait/struct *shape* this audit approves below is the
target; only the production mechanism changes.

### MAJOR — the emitted source is never parse-validated at emission time

A direct consequence of the BLOCKER, but worth calling out on its own because
it changes the failure mode. Every token-based target is guaranteed to be
syntactically valid Rust *at emission time* by the `syn::parse2::<syn::File>`
call at lib.rs:2917 — a malformed emission panics the generator, not the
downstream `cargo build`. The daemon emitter has **no such gate**: a typo in
any of the 465 string fragments emits silently and only surfaces as a
`cargo build` failure (or, worse, a freshness-check diff) in the *consuming*
component. The handoff itself records that "the agent fixed three real emitter
bugs to get spirit compiling" (543, §schema-rust-next) — string emission is
precisely why those bugs reached compile time instead of emission time.

**Fix:** subsumed by the BLOCKER fix — `emit_item_tokens`'s `syn::parse2`
gate gives emission-time validation for free once the daemon module is
token-based. If, for any reason, the port is staged, add an interim
`syn::parse_file(&rendered).expect(...)` at the end of `DaemonModule::render`
as a stopgap parse gate.

### MAJOR — `DaemonStreamShape` is dead-code machinery; its computed type is thrown away

`DaemonStreamShape` (daemon_emit.rs:127-156) exists to carry one field,
`event_type: String` (daemon_emit.rs:128), computed by the 18-line recursive
`reference_type_name` (daemon_emit.rs:138-155) over a `TypeReference`. That
string is **never emitted into the source**. Both of its only two read sites
discard it:

- daemon_emit.rs:354 `let event = &stream.event_type;` … then
  daemon_emit.rs:377 `let _ = event;` (bound and immediately dropped).
- daemon_emit.rs:527 `let _event = &stream.event_type;` (bound to a
  `_`-prefixed name, i.e. deliberately unused).

The emitted code names the event type through the component's
`type StreamEvent` associated type, not through this string — so the entire
`DaemonStreamShape` struct, its `from_stream` constructor, and the
`reference_type_name` recursion are computing a value the emitter then throws
on the floor. The only thing the emitter actually needs from the stream is the
*boolean* "does the schema declare a stream?" (used as `stream.is_some()`
throughout). This is dead code wearing the costume of a typed model noun, and
it inverts de8i: a model noun that carries no information the emission reads.

**Fix:** delete `DaemonStreamShape`, `from_stream`, and `reference_type_name`.
Replace the `stream: Option<DaemonStreamShape>` field on `DaemonModule` with a
`emits_stream: bool` (or, better, keep an `Option` of a *zero-field* marker
only if a future field is imminent). If a later first-class-streaming step
(design 542 fork 4) genuinely needs the event type name in the emitted source,
re-introduce it *then*, emitting it — not as speculative dead state now.

### MINOR — `DaemonModuleWriter` is a god-struct that reads none of its own data

Even setting 4np2 aside, `DaemonModuleWriter` (daemon_emit.rs:197) is the
god-struct de8i warns against. Its 18 `emit_*` methods (daemon_emit.rs:251-805)
take `shape: &NexusDaemonShape` and `stream: Option<&DaemonStreamShape>` as
*arguments* and write to the shared `output` buffer; the only data the struct
itself carries is the output accumulator and `generator_name`. The cross-object
lowering logic (how a `NexusDaemonShape` becomes a `ComponentDaemon` trait,
how it becomes a `DaemonError`, etc.) lives on a writer that owns neither the
shape nor the stream. de8i wants that lowering as methods/`ToTokens` *on the
model nouns* (`NexusDaemonShape`, the stream model), with any genuinely
cross-object glue as its own named type — not 18 verbs parked on a string
buffer. This dissolves naturally under the BLOCKER fix (each `…Tokens` type
carries its own data and implements `ToTokens`), so I tag it MINOR rather than
MAJOR: it is the same root cause as 4np2, viewed through the de8i lens.

**Fix:** as the BLOCKER fix lands, place each item's emission as `ToTokens`
on a data-bearing `…Tokens` noun that owns the slice of shape/stream it reads,
mirroring `RustStructTokens` / `NexusEngineTraitTokens` in lib.rs. No
`DaemonModuleWriter`-style buffer-with-verbs survives.

### MINOR — emitted `DaemonError::Component(#[error("{0}")])` flattens the component error's prefix

In the emitted `DaemonError` (daemon_emit.rs:756-757, visible in spirit's
output), the `Component` arm renders as bare `#[error("{0}")]`. The other
three arms self-describe (`"daemon argument error: {0}"`,
`"daemon configuration error: {0}"`, `"daemon listener error: {0}"`), but the
`Component` arm prints the inner error verbatim with no "component" framing.
In spirit's case the inner `SpiritDaemonError` variants already prefix
themselves ("daemon frame error: …" etc.), so the output reads fine — but the
emitter can't rely on that for every future component, and the asymmetry is a
latent stringly-error smell. Not a typed-error violation (the enum is properly
typed, one-per-crate, thiserror-derived, structured) — purely a message-shape
nit.

**Fix:** emit `#[error("daemon component error: {0}")]` for the `Component`
arm to match the other three, OR consciously document that the component
error owns its own self-description and the daemon deliberately does not
double-prefix. Either is fine; the current silent asymmetry is the only
issue.

### NIT — emitted `EmittedSubscriptions::deliver` is a multi-arg associated fn, not a method on a noun

In the emitted streaming plumbing (daemon_emit.rs:603-616), `deliver` is an
associated function taking three explicit arguments
(`writers: &mut HashMap<…>`, `token`, `frame`). It reads/writes the writers
map that lives on `SubscriptionState`, so by the one-object-in/methods-on-nouns
rule it ideally is `&mut self` on `SubscriptionState` (`self.writers` in
scope), called as `state.deliver(token, frame)`. The current form passes the
borrow explicitly to dodge the `publish` borrow-split — a real constraint, but
one that wants the method on `SubscriptionState`, not a 3-arg associated fn on
`EmittedSubscriptions`. Low severity because it is private emitted plumbing
inside one module and the borrow-split rationale is real.

**Fix (optional):** when re-emitting via tokens, move `deliver` to
`impl SubscriptionState` as `&mut self`, leaving `publish` to orchestrate.
Acceptable to leave as-is given the borrow-split comment already documents why.

## What is sound (verified, not assumed)

These passed and should be preserved verbatim through the emitter rewrite:

- **`ComponentDaemon` hook surface (daemon_emit.rs:298-379).** Minimal and
  well-named: `build_runtime` is the one REQUIRED escape hatch (record 1488),
  `load_configuration` / `handle_working_input` are typed and named by
  direction, `start`/`stop` default to no-op, the meta and streaming hooks are
  conditionally emitted only when the shape declares those tiers. Verbs sit on
  the trait the component implements; no god-trait. Good.
- **The decode→execute→encode spine (`handle_working_stream`,
  daemon_emit.rs:641-664).** Well-factored as a method on
  `GeneratedDaemonRuntime` (a data-bearing noun owning `engine` +
  `subscriptions`), threading `WorkingTransport` (its own noun) for the wire.
  Reads top-to-bottom: clone writer → read frame → decode `Input` → handle →
  encode `Output` → register/publish. Not a free-function chain. Good — this
  is the design's core claim and it holds.
- **Single-argument rule (daemon_emit.rs:409-418 + spirit config.rs).**
  `DaemonCommand::configuration` accepts only `ComponentArgument::SignalFile`
  and rejects `InlineNota`/`NotaFile` with `ExpectedSignalFile`. Spirit's
  `Configuration` is a typed rkyv struct (config.rs:13-18) loaded by path; no
  flags anywhere. Honoured.
- **`DaemonConfiguration` (triad-runtime process.rs:33-52).** A clean accessor
  trait — `socket_path` required, `meta_socket_path`/`trace_socket_path`/
  `meta_socket_mode` defaulting to `None`. Not leaky: it names only the uniform
  socket/storage surface the emitter reads, no component meaning. Good.
- **`DaemonError` (daemon_emit.rs:742-792).** One typed enum, thiserror-derived,
  structured arms, `From` conversions for `ArgumentError` and the
  `{Single,Multi}ListenerDaemonError`. Three of four arms self-describe (see
  the MINOR on the fourth). No `anyhow`/`eyre`, no `Box<dyn Error>`. Compliant.
- **`ExitReport::from_result` (triad-runtime process.rs:62-90).** 543's claim
  is verified: it is a method on a data-bearing noun (`ExitReport` owns
  `process_name`), not a free `run_to_exit_code`. `DaemonEntry::run_to_exit_code`
  (daemon_emit.rs:798-803) is a default *trait* method, and the bin
  (spirit-daemon.rs) is a true one-liner `SpiritDaemon::run_to_exit_code()`.
  Discipline-faithful.
- **Single/Multi listener selection (daemon_emit.rs:426-448, 667-740).**
  Chosen from `shape.is_multi_listener()` (meta tier presence), emitting the
  `DaemonRuntime` impl for single and the `MultiListenerRuntime` + `ListenerTier`
  enum for multi. `ListenerTier` is a real enum with a `Display`, the dispatch
  is `match listener {…}` — enum-vs-enum contact point, not string predicates.
  Good.
- **No ZST namespace holders in the EMITTED output.** `SpiritDaemon`
  (spirit/src/daemon.rs:36) is a marker selecting associated types — a
  legitimate type-level selector under methods.md §"Legitimate ZST uses", not
  a verb parking lot (its job is carried by the type system, not erasable).
  The supporting `SocketModeBits`/`WorkingListenerTier`/`MetaListenerTier`
  newtypes (daemon_emit.rs:72-122) are all data-bearing. Clean.

The discipline problem is entirely in the **production mechanism** (the
string emitter + its dead stream model), not in the **product**. Bring the
emitter to tokens (BLOCKER), delete the dead `DaemonStreamShape` (MAJOR), and
the daemon module is discipline-clean end to end.
