---
variant: Audit
slice: spirit-pilot
repo: github.com/LiGoldragon/spirit
branch: main (no next branch created — no clear violation to fix)
date: 2026-06-04
constraint: psyche record 2560 (VeryHigh) — strict-absolute triad-engine separation
---

# Slice 1 — strict engine separation in the spirit pilot

## The constraint being audited

Per psyche record 2560 (VeryHigh): the triad engine separation is
strict and absolute. The SEMA engine owns ALL database and
durable-state code; the Nexus engine owns ALL decision-making; the
Signal engine owns ALL communication. A component daemon must contain
NO database boilerplate, NO decision-making, and NO communication code
outside its respective engine.

In the spirit pilot the three engines are:

- `SignalEngine` on `SignalActor` (src/engine.rs) — communication /
  wire / admission.
- `NexusEngine` on `Nexus` (src/nexus.rs) — decisions / the decide loop.
- `SemaEngine` on `Store` (src/store.rs) — the redb durable state.

The scaffolding — `Engine` composer + `daemon.rs` + `transport.rs` +
`config.rs` + `bin/*` — must wire the engines and run the loop, and
must NOT contain db / decision / comms LOGIC.

## Verdict: the separation holds. No clear violation. No next branch.

All three engines are clean against the strict constraint. The two
items worth surfacing are design-questions, not leaks, so per the
audit discipline (*"If a fix is a design judgment rather than a clear
violation, surface it as a design-question, do not force it"*) no
`next` branch was created and no edit was forced. The crate builds
clean on `main` (`cargo build` finished with no diagnostics).

## SEMA engine — clean

ALL redb / durable-state code lives inside `Store` (src/store.rs):

- The `redb` imports, `TableDefinition` constants (`RECORDS`,
  `LEDGER`), the ledger key constants — store.rs:3, store.rs:16-22.
- Every write/read transaction — `record` (store.rs:210),
  `observe` (store.rs:234), `lookup` (store.rs:249), `count`
  (store.rs:261), `remove` (store.rs:276), `ensure_tables`
  (store.rs:194), `committed_record_count` (store.rs:303),
  `commit_sequence` (store.rs:318), `state_digest` (store.rs:332).
- The `.sema` file path handling and `Database::open`/`create`
  (store.rs:156-174).
- The rkyv archive/dearchive of the durable `Entry` rows
  (store.rs:211, 240, 255, 267).
- `StoreError` + all its `From<redb::*>` conversions
  (store.rs:357-415).

Nothing outside `Store` touches redb, the `.sema` file, or a durable
transaction. Grep confirms `redb` appears only in store.rs and the
generated schema. The `database_marker()` value is consumed in
`nexus.rs:164` (`self.store.database_marker()`) and reached through
Nexus by `engine.rs:159`, but those are **reads of a value the SEMA
engine computes**, not durable-state code living outside Store. That
is exactly the read-the-marker boundary the architecture describes:
the marker flows out of SEMA into the reply; the durable code stays
in.

One in-memory state holder outside Store is worth naming so it is not
mistaken for a SEMA leak: the `StashTable` (nexus.rs:55-102) is a
`HashMap` handle store, and `MailLedger` (engine.rs:53-56) is a
`Vec` behind a `Mutex`. Both are **in-memory Nexus-owned** bookkeeping,
not durable `.sema` state, so neither is a SEMA-engine concern. The
architecture explicitly places the mail ledger as *"the ledger Nexus
owns"* (ARCHITECTURE.md:310). Clean.

## Nexus engine — clean

ALL decision-making lives inside `Nexus` (src/nexus.rs):

- The decide loop — `NexusEngine::decide` (nexus.rs:222-268) is the
  runner that cycles consume → decide → act → re-consume.
- `step_decide` (nexus.rs:279) and the per-fact deciders:
  `decide_signal_arrival` (nexus.rs:288), `decide_sema_write_completion`
  (nexus.rs:316), `decide_sema_read_completion` (nexus.rs:328),
  `decide_effect_completion` (nexus.rs:351).
- The Observe → Stash → Reply recursion decision (nexus.rs:328-340):
  a non-empty read result becomes a `CommandEffect(Stash(...))`
  recursion rather than a direct reply — a genuine domain decision,
  correctly inside Nexus.
- The `ContinuationBudget` policy (nexus.rs:22-47) and the
  budget-exhausted error reply (nexus.rs:259-265).
- The `apply_effect` Stash dispatch (nexus.rs:169-179).

The crucial composer check: does `Engine::handle` (engine.rs:114-128)
or anywhere in the scaffolding **make a decision** — branch on domain
state to choose an action? No. `Engine::handle` admits via Signal,
then `SignalAccepted::process_with` (engine.rs:257-277) runs the
fixed composition `triage → NexusEngine::execute → reply`. There is no
domain branch in the composer that picks an action; it is pure
sequencing of the three engine calls. The `match self.signal_actor
.admit(input)` at engine.rs:115-125 branches only on accepted-vs-
rejected admission, which is a Signal-admission outcome (see below),
not a domain decision over store state.

## Signal engine — clean, with one structurally-unreachable defensive branch (design-question 2)

ALL communication lives in `SignalActor` (SignalEngine, src/engine.rs)
plus the schema-emitted frame codec it owns:

- Admission — `SignalActor::admit` (engine.rs:174-190): mints the
  origin route, issues the message identifier, runs validation.
- Triage and reply framing — `SignalEngine::triage_inner`
  (engine.rs:227) and `reply_inner` (engine.rs:232).
- The wire frame codec is **schema-emitted** on the Signal types:
  `Input::encode_signal_frame`/`decode_signal_frame` (schema/lib.rs:1145,
  1154) and the matching `Output` pair (schema/lib.rs:1213, 1222). The
  daemon does NOT hand-roll wire frames; it calls the generated codec.
  This is the strongest single signal that comms logic is owned by the
  Signal contract, not scattered.
- The admission validation rules (`Input::validate` engine.rs:334,
  `Entry::validate` engine.rs:345, `Query`/`TopicMatch::validate`
  engine.rs:360-376) sit in free `impl` blocks in engine.rs but are
  logically Signal-admission predicates — the architecture states
  *"invalid `Input` is rejected ... before mail is sent or SEMA is
  touched"* (ARCHITECTURE.md:290-291), placing admission in the Signal
  engine by design. They are co-located with the Signal admission
  object, which is correct ownership.

The one item to flag: `into_signal_output` on
`nexus_plane::Nexus<NexusAction>` (engine.rs:466-478):

```rust
impl nexus_plane::Nexus<NexusAction> {
    pub fn into_signal_output(self) -> signal_plane::Signal<Output> {
        let origin_route = self.origin_route();
        match self.into_root() {
            NexusAction::ReplyToSignal(output) => output.with_origin_route(origin_route),
            _ => Output::error(ErrorReport {
                error_message: String::from("nexus returned non-signal action"),
                database_marker: DatabaseMarker::zero(),
            })
            .with_origin_route(origin_route),
        }
    }
}
```

This branches on a `NexusAction` and, in the `_ =>` arm, fabricates an
error reply — which reads like a decision. Two facts soften it to a
design-question rather than a clear Nexus-leak:

1. It is invoked ONLY from `SignalActor::reply_inner` (engine.rs:232-234)
   — Signal-engine territory translating a finished Nexus action into a
   Signal output. Framing a Nexus action as a wire reply is legitimately
   a Signal-engine job.
2. The `_ =>` arm is **structurally unreachable**: the Nexus runner loop
   (nexus.rs:230-268) exits ONLY via `NexusAction::ReplyToSignal` — every
   loop exit at nexus.rs:236, 260 wraps `reply_to_signal`. The
   `CommandSema*` / `CommandEffect` / `Continue` variants are consumed
   inside the loop and never returned. So at the Signal boundary the
   action is always `ReplyToSignal`; the error arm cannot fire.

This is the audit's design-question 2.

## Design-question 1 (assigned) — the accept loop and frame codec: Signal-engine comms, or runtime-runner scaffolding?

The grey zone: the daemon accept loop (`Daemon::run`, daemon.rs:152-173)
and the `transport.rs` length-prefix codec.

What they actually do:

- `Daemon::run` (daemon.rs:152): create socket dir, remove stale socket,
  `UnixListener::bind`, `engine.start()`, then
  `for stream in listener.incoming()` dispatching each to
  `handle_stream`.
- `handle_stream` (daemon.rs:194-200): wrap the stream in
  `SignalTransport`, `read_input()`, `engine.handle(input)`,
  `write_output(...)`.
- `SignalTransport` (transport.rs): a length-prefixed framer
  (`write_frame`/`read_frame`, transport.rs:84-100) that delegates the
  actual wire encode/decode to the **schema-emitted**
  `encode_signal_frame`/`decode_signal_frame` (transport.rs:69, 73, 76,
  81).

Reasoned recommendation: **this is runtime-runner scaffolding, not
Signal-engine domain comms — leave it where it is for now and extract it
into the (unbuilt) `triad-runtime` runner, NOT into `SignalEngine`.**
The reasons:

- The accept loop contains ZERO domain logic: it constructs no replies,
  parses no wire semantics, makes no decision. It is socket lifecycle +
  connection iteration + a fixed three-call hand-off to `engine.handle`.
  That is precisely the "run the loop" scaffolding the constraint allows
  in the composer / daemon layer.
- The actual communication SEMANTICS — what a frame IS, how an `Input`
  or `Output` becomes bytes — already lives in the schema-emitted codec
  on the Signal types, i.e. inside the Signal contract, not in
  `transport.rs`. `transport.rs` only adds the transport-level length
  prefix and the `UnixStream` plumbing. Length-prefix framing and socket
  I-O are runner mechanics shared by every component, which is exactly
  what `triad-runtime` is meant to own per the INTENT/ARCHITECTURE
  runner direction (INTENT.md:66-71 — *"Daemon startup should move
  toward a generated/programmatic triad runner ... the eventual
  component runner surface belong[s] on data-bearing library nouns"*;
  ARCHITECTURE.md:91-93 — *"This is the small live step toward the
  generated component runner"*).
- This ties to records 1574/1581 (runner extraction): the accept loop +
  socket framer is the per-component plumbing that should be lifted into
  the shared runner so it is written once, not re-hand-written in each
  daemon. Folding it into `SignalEngine` instead would push transport
  plumbing into the per-component Signal impl — the wrong direction,
  because socket lifecycle is component-agnostic.

So the boundary I recommend:

- Wire SEMANTICS (frame encode/decode of `Input`/`Output`) — already
  Signal-engine, schema-emitted. Correct, leave as is.
- Socket lifecycle + accept loop + length-prefix transport
  (daemon.rs:152 `run`, transport.rs framer) — runtime-runner
  scaffolding. Correct to be outside `SignalEngine`; the future move is
  INTO `triad-runtime`'s generated runner, not into the Signal engine.

No edit forced: extracting the runner is a cross-repo build
(`triad-runtime`), well beyond the strict-separation fix scope, and the
current placement does not VIOLATE the constraint — it holds no domain
comms logic. It is a scaffolding-relocation design-question for the
runner slice.

## Why no next branch was created

Both surfaced items are design-questions (engine-ownership judgment
calls), not clear strict-separation violations:

1. The accept-loop / transport placement is correct-as-scaffolding and
   awaits the `triad-runtime` runner extraction (records 1574/1581) —
   a cross-repo design move, not a spirit-pilot fix.
2. The `_ =>` non-signal-action error arm (engine.rs:471-475) is
   structurally unreachable and lives on the Signal-reply path, so its
   engine ownership is a judgment call, not a leak.

Per the audit instruction to not force design-judgment edits, no
`next` branch was created and `main` is untouched.
