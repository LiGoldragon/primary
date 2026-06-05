# Area 5 — The Shared Triad Runtime Runner (triad-runtime + spirit pilot)

Read-only area map for the engine-forward exploration. Scope: the shared
triad runtime runner — the LEVER named by intent 7ca4 (extract the generic
triad runtime runner NOW). Repos: `triad-runtime` and `spirit` (the
reference component / pilot daemon). All citations verified against source
on 2026-06-05.

## Bottom line up front

The runner extraction is **further along than the intent framing suggests,
and that is the central finding**. The Nexus loop is already extracted AND
its adapter is already generated glue — rpr5's hardest claim ("the runner
adapter is generated glue, not an author-written fourth engine") is
**LANDED** for the Nexus plane. `triad-runtime` is no longer just "generic
trace logging + rkyv frame transport + Unix trace socket"; it is a 6-module
crate owning frame, argument, single-listener daemon, the recursive Nexus
`Runner`, the plane-role marker traits, and trace. The spirit pilot consumes
all of it. The remaining hand-written boilerplate in the pilot is the
**Signal-plane accept bridge** (read frame → engine.handle → write frame)
and the per-component `SignalTransport`. Those are the next extraction, and
they are the highest-leverage move because they are what every *new* daemon
(persona, introspect, schema, cloud) would otherwise copy by hand.

## 1. CURRENT STATE — landed vs scaffold/doc-only

### triad-runtime — what is LANDED (compiles clean, has witness tests)

`triad-runtime` is at version `0.2.1` (`Cargo.toml`). Six source modules,
each backed by a test file. The crate built clean on 2026-06-05 with its
current in-flight changes (`cargo build --offline` → `Finished`).

Module-by-module landed surface (all `src/lib.rs:10-32` re-exported):

- **`frame.rs` (LANDED).** `LengthPrefixedCodec` + `FrameBody` +
  `MaximumFrameLength` — a 4-byte big-endian length-prefix envelope
  (`frame.rs:5,90-122`). Body is opaque bytes; the codec never interprets
  schema/NOTA/rkyv. This is the genuinely-generic transport primitive.
  Witnessed by `tests/frame.rs`.
- **`argument.rs` (LANDED).** `ComponentCommand` + `ComponentArgument`
  (`InlineNota` / `NotaFile` / `SignalFile`) — owns the single-argument
  process-edge rule (`argument.rs:57-104`). Classifies argv into inline
  text vs file path (existence check, `argument.rs:130-136`). Enforces
  exactly-one-argument (`argument.rs:96-103`). This is the AGENTS.md
  single-argument rule, extracted.
- **`daemon.rs` (LANDED).** `SingleListenerDaemon<Runtime>` +
  `DaemonRuntime` trait + `BoundSingleListenerDaemon` + `RequestErrorLog`.
  Owns parent-dir creation, stale-socket removal, bind, the accept loop
  (`serve_streams`, `daemon.rs:149-161`), request-error isolation
  (`daemon.rs:143-146`), and the start/stop lifecycle (`daemon.rs:104-117`).
  The `DaemonRuntime` trait (`daemon.rs:11-21`) is the component boundary:
  `start` / `stop` / `handle_stream`. Explicitly documented as "the first
  production slice, not the final concurrency model"
  (`ARCHITECTURE.md:99`). Witnessed by `tests/daemon.rs`.
- **`runner.rs` (LANDED).** `Runner` + the recursive five-outcome Nexus
  loop. `Runner::drive` (`runner.rs:149-185`) is the canonical
  consume→decide→act→re-consume cycle dispatching the fixed
  `NextStep::{Reply,SemaWrite,SemaRead,RunEffect,Continue}`
  (`runner.rs:23-30`). `RunnerEngines` (`runner.rs:32-50`) is the adapter
  surface the generated glue implements. Typed continuation budget
  (`ContinuationLimit`/`ContinuationBudget`/`ContinuationExhausted`,
  default 32 non-reply steps, `runner.rs:3,65-69`). Six witness tests in
  `tests/runner.rs` including budget-exhaustion and continue-loop
  exhaustion.
- **`role.rs` (LANDED-BUT-UNCOMMITTED — see caveat).** Marker traits
  `NexusWork` / `SemaWriteInput` / `SemaReadInput` / `NexusEffectCommand`
  + the `NexusAction` projection trait with `into_next_step`
  (`role.rs:3-21`). This is the most recent extraction wave: it tightens
  `RunnerEngines`' associated types with trait bounds (`runner.rs` diff:
  `type SemaWrite: SemaWriteInput`, etc.). **This sits in the working copy
  uncommitted** (`git status`: `M src/lib.rs`, `M src/runner.rs`,
  `M tests/runner.rs`, `?? src/role.rs`). It compiles, but it is not yet
  in a commit and not yet documented in `ARCHITECTURE.md`'s Code Map
  (which lists only argument/frame/daemon/runner/trace, `ARCHITECTURE.md:151-159`).
- **`trace.rs` (LANDED).** `TraceLog` / `TraceFrame` / `TraceSocketListener`
  / `TraceClient` / `TraceEventFrame` / `TraceSocketPath`. The original
  "first live scope" (`INTENT.md:20`). Generic over the component event
  noun; renders only at the `Display` edge. Witnessed by `tests/trace.rs`.

The Nexus feature-catalog discipline (z6qu, VeryHigh) is **documented and
load-bearing** in both `INTENT.md:9-14` and `ARCHITECTURE.md:64-70`: the
fixed five-outcome loop is "mechanics, not feature vocabulary"; any computed
operation / filter / conditional write is first declared as a Nexus
verb/object in the component schema. This is a discipline statement, not a
mechanical enforcement — the runtime cannot *prevent* a component from
hiding a feature, but the architecture is written to make the Nexus schema
the visible catalog.

### spirit pilot — what is LANDED

The spirit pilot (`spirit` crate, version `0.1.0`) is a **real running
daemon**, not a documentation artifact. Evidence:

- `tests/process_boundary.rs` has **7 `#[test]` functions** that
  `Command::new(env!("CARGO_BIN_EXE_spirit-daemon"))` actually spawn the
  compiled daemon binary, bind a Unix socket, and exchange
  length-prefixed rkyv frames with the compiled `spirit` CLI binary
  (`process_boundary.rs:32-54,158-542`). Tests cover: NOTA-over-rkyv
  exchange, State→provisional-record classification, change-certainty,
  alias-payload rendering, SEMA persistence across restart, candidate
  daemon handover preserving the original DB, and trace-event delivery.
- The schema-derived build is real and checked: `build.rs` runs
  `GenerationDriver` over the three plane schemas and `write_or_check`s
  the generated `src/schema/{signal,nexus,sema}.rs` for freshness
  (`build.rs:28-37`). **asschema removal is CONFIRMED COMPLETE**: a sweep
  of `*.rs`/`*.schema`/`*.toml` found zero `.asschema`/`AsSchema`
  references except one INTENT.md sentence stating ".asschema is no longer
  a checked component artifact" (`spirit/INTENT.md:9`). triad-runtime has
  zero asschema references. The schema pipeline runs
  `schema/*.schema → SchemaSource → src/schema/*.rs` directly, matching
  the foundation claim.

The pilot **consumes the extracted runtime everywhere it can**:

- Daemon shell: `Daemon::run` builds a `SingleListenerDaemon` over a
  `SpiritDaemonRuntime` and calls `.run()` (`spirit/src/daemon.rs:97-106`).
  `SpiritDaemonRuntime` implements `triad_runtime::DaemonRuntime`
  (`spirit/src/daemon.rs:148-164`). The accept loop, socket prep, and
  lifecycle are NOT hand-written in spirit anymore.
- Argument edge: `DaemonCommand` wraps `triad_runtime::ComponentCommand`
  and uses `signal_file_argument()` (`spirit/src/daemon.rs:51-86`).
- Frame transport: `SignalTransport` delegates the length prefix to
  `LengthPrefixedCodec::default()` (`spirit/src/transport.rs:63-73`).
- **Nexus runner: FULLY EXTRACTED AND GENERATED.** The generated
  `NexusEngine::execute` (`spirit/src/schema/nexus.rs:805-818`) constructs
  a `triad_runtime::Runner`, wraps the engine in a **generated**
  `NexusRunnerAdapter` (`nexus.rs:821-865`) that implements
  `triad_runtime::RunnerEngines`, and calls `runner.drive(...)`. The
  adapter is `@generated by schema-rust-next` (`nexus.rs:1`). The
  hand-written `Nexus` (`spirit/src/nexus.rs:208-274`) only supplies the
  component hooks: `decide` (one step), `apply_sema_write`,
  `observe_sema_read`, `run_effect`, `budget_exhausted_reply`. **This is
  exactly the rpr5 target shape — authors write 3 plane engines + effect
  handler + budget reply; the adapter is generated glue — and it is
  LANDED for the Nexus plane.**

### What is still HAND-WRITTEN in the pilot (the remaining boilerplate)

This is the gap between today and "no hand-written boilerplate" (7ca4):

- **The Signal-plane accept bridge.** `SpiritDaemonRuntime::handle_stream`
  (`spirit/src/daemon.rs:139-145`) hand-writes the request flow:
  `transport.read_input()` → `engine.handle(input)` →
  `transport.write_output(output.root())`. Every daemon needs this exact
  three-line bridge. It is NOT generated and NOT in triad-runtime.
- **`SignalTransport`** (`spirit/src/transport.rs:24-74`) is hand-written
  per-component (read_input/write_input/read_output/write_output +
  connect). It is thin (delegates framing to the codec) but it is
  copy-paste surface for the next daemon. The signal-frame encode/decode
  *methods* themselves ARE generated (`spirit/src/schema/nexus.rs:474-558`
  and the signal module), but the transport object that calls them is hand
  code.
- **`Engine::handle` Signal admission composition**
  (`spirit/src/engine.rs:115-129`): mint origin route, issue identifier,
  validate, fire the sent/processed mail-ledger hooks, lock the Nexus
  mutex, run `process_with`. The generated `SignalEngine` trait
  (`spirit/src/schema/signal.rs:1271-1310`) provides `triage`/`reply`
  default methods (with trace hooks), but the **admission actor itself**
  (route minting, identifier issuance, validation, single-flight mutex,
  mail-ledger hook firing) is all hand code in `engine.rs`. There is no
  generated `SignalEngine::serve` analogous to `NexusEngine::execute`.

So the picture is: **Nexus loop = generated runner (done). Signal loop =
hand-written bridge (the next lever).** No `TriadComponent::serve` type
exists anywhere yet (grep found only `serve_streams`/`serve_next_stream`
on the daemon) — the unified "component owns accept loop + transport +
Nexus loop behind one generated entry point" is the proposed-not-built
target.

## 2. MOVE-FORWARD WORK ITEMS (ordered)

Toward the running-orchestrated-system target (persona supervises
introspect + schema daemon + triad components, mazv), the runner is the
shared substrate every daemon plugs into. Ordered work:

**WI-1. Commit the in-flight `role.rs` extraction and document it.**
`triad-runtime`. Add `src/role.rs` to the Code Map in `ARCHITECTURE.md`,
write the role-trait rationale into `INTENT.md`, commit the working-copy
changes (`role.rs` + the `RunnerEngines` bound tightening). Tiny. Depends
on nothing. This closes an open, uncommitted extraction so the foundation
others build on is in a commit, not a working copy.

**WI-2. Extract the Signal-plane accept bridge into generated glue.**
Generate a `SignalEngine::serve` (or equivalent) that owns
read-frame → admit/triage → `NexusEngine::execute` → reply → write-frame,
mirroring the already-generated `NexusEngine::execute`. Emit it from
`schema-rust-next` into the signal module; have `SpiritDaemonRuntime::
handle_stream` call the generated entry point instead of hand-writing the
three-line bridge. Repos: `schema-rust-next` (emitter) + `spirit`
(consumer). Medium. Depends on WI-1 (role traits) and on the signal-plane
generation path being stable. This is the rpr5 "generated adapter" claim
extended from Nexus to Signal.

**WI-3. Move `SignalTransport` into triad-runtime as a generic
`SignalTransport<Frame>`.** The codec is already shared; lift the
read_input/write_input/read_output/write_output object so the next daemon
doesn't copy it. The component supplies the generated frame
encode/decode via a trait (analogous to `TraceEventFrame`). Repos:
`triad-runtime` (new generic transport) + `spirit` (consume). Medium.
Depends on WI-2's framing decisions. This is the literal "daemons plug
into shared Signal/Nexus/SEMA runner objects" of 7ca4 for the Signal leg.

**WI-4. Define the `TriadComponent` umbrella that owns
accept-loop + transport + Nexus-loop behind one generated `serve`.** This
is the rpr5 end state: a component author declares 3 plane schemas, writes
3 plane engines + effect handler + budget reply, and the generated
`TriadComponent::serve` wires `SingleListenerDaemon` + `SignalTransport`
+ `SignalEngine::serve` + `NexusEngine::execute` together. Repos:
`triad-runtime` (the trait) + `schema-rust-next` (the glue) + `spirit`
(reference). Large. Depends on WI-1/2/3. This is the thing that makes a
*second* daemon (persona/introspect/schema) cheap.

**WI-5. Bootstrap policy as pre-encoded binary (7x50) plumbed through the
runner's startup.** The daemon already takes a binary rkyv `Configuration`
as its single argument (`spirit/src/daemon.rs:72-81`,
`README.md` "Run"). Extend that path so meta-policy bootstrap NOTA is
authored as NOTA and consumed as pre-encoded binary at first start, wired
through the generic daemon startup. Repos: `triad-runtime` +
the signal/meta-signal contracts. Medium. Depends on WI-4 for the
component shape and on the meta-signal plane shape settling.

**WI-6 (NOT this area, named as the unblock target).** Stand up a SECOND
daemon (introspect or schema) on the WI-4 `TriadComponent::serve` to prove
the runner generalizes beyond spirit. This is where persona-supervised
orchestration begins. Out of this area's repos but it is the *reason*
WI-1..4 are critical-path.

## 3. FOUNDATION-STABILITY VERDICT per item

The load-bearing column. The psyche wants to port now WITHOUT rework. What
is stable under this area: (a) the rkyv length-prefixed wire frame
(`LengthPrefixedCodec`, 8-byte short header + rkyv body) — proven across a
real process boundary by 7 tests; (b) the five-outcome Nexus runner shape
and typed continuation budget — proven by 6 witness tests and consumed by
the generated adapter; (c) asschema-removal-done — confirmed by sweep; (d)
plane separation — three separate `schema/*.schema` files, generated into
three modules, with `compile_fail` cross-plane mis-wiring guard
(`spirit/src/lib.rs:14-21`). What is still shifting: the meta-signal plane,
the concurrency/multi-listener model (explicitly deferred,
`ARCHITECTURE.md:99-102`, `INTENT.md:68-73`), and the exact generated
Signal-serve shape.

- **WI-1 (commit role.rs): [SAFE-NOW].** It already compiles and is
  consumed by the runner's own bound tightening. The only risk is leaving
  it uncommitted. Committing a working, building extraction is pure
  derisking — zero rework potential because it is already the chosen shape.
- **WI-2 (generate Signal-serve): [PREP].** The *target* (a generated
  serve mirroring `NexusEngine::execute`) is sound and the Nexus precedent
  proves the pattern. But the Signal admission actor still carries
  component-specific identity (origin-route minting, mail-ledger hooks)
  that must be cleanly split into generated-glue vs author-hooks before
  emission freezes. Structure and scaffold the trait now; finalize the
  emitted method once the author-hook boundary is drawn. Justification for
  not [WAIT]: the wire contract and the Nexus-loop entry it calls are both
  stable, so the glue is built on rock; only the *split line* is open.
- **WI-3 (generic SignalTransport): [SAFE-NOW] for the object, [PREP] for
  the frame trait.** The length-prefix codec it wraps is stable and
  already shared; lifting the read/write object that calls generated
  encode/decode is safe — it is mechanically identical to the trace
  transport already extracted. The only open piece is the
  `TraceEventFrame`-style trait that lets the component supply its frame
  codec; that mirrors an existing pattern, so risk is low. Justify
  SAFE-NOW: the spirit transport is already a thin wrapper over a stable
  codec; generalizing it cannot regress the wire format.
- **WI-4 (TriadComponent::serve umbrella): [PREP].** This is the right end
  state and every piece under it (daemon shell, runner, codec) is stable,
  so it will not be built on sand. But it composes WI-2 and WI-3, whose
  split lines are still open, and it touches the deferred concurrency
  model. Scaffold the trait and prove it against spirit; do NOT freeze the
  public `serve` signature until a second daemon exercises it. Mark PREP,
  not WAIT, because the blocker is "needs WI-2/3 first," not "foundation
  is moving."
- **WI-5 (bootstrap policy binary): [WAIT].** Named blocker: the
  meta-signal / meta-policy plane shape (lc2r: meta-signal-<component> is a
  separate leg) is not settled in this area's repos. The daemon already
  consumes a binary config, so the *transport* of pre-encoded binary is
  safe — but authoring bootstrap policy as NOTA → pre-encoded binary
  depends on the meta-policy schema, which is shifting foundation. Porting
  the policy schema now risks rework. Do the binary-config plumbing
  (already done) but WAIT on the policy schema.

## 4. THE ONE highest-leverage first step

**Generate the Signal-plane accept bridge as glue (WI-2), after
committing the in-flight `role.rs` (WI-1) as the trivial unblock.**

Reasoning: the Nexus loop is already a generated runner adapter — that half
of 7ca4/rpr5 is LANDED and proven. The *only* remaining hand-written
boilerplate that every future daemon would copy is the Signal accept
bridge (`handle_stream`: read → handle → write) plus its admission
composition. Extracting/generating that is what turns "spirit hand-writes
its accept loop" into "daemons plug into shared runner objects." It is the
single move that converts the second daemon (persona / introspect / schema)
from "copy spirit's daemon.rs + transport.rs + engine.rs admission code"
into "declare 3 schemas + write the hooks." Because the wire frame and the
Nexus-loop entry it calls are both already stable (verdict above), this is
PREP-on-rock, not porting onto sand — the only open decision is where the
author-hook boundary sits, which the Nexus precedent already shows how to
draw. Commit `role.rs` first (SAFE-NOW, ~minutes) so the runner foundation
others build on lives in a commit rather than a working copy.
