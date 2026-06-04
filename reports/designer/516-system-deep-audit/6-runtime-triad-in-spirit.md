---
title: "Runtime triad in spirit — three actors, the runner, the outcome algebra"
role: designer
variant: Psyche
date: 2026-06-04
topics:
  - spirit
  - triad-runtime
  - runtime-triad
  - runner
  - outcome-algebra
  - SEMA
  - Nexus
  - SignalActor
  - schema-derived-stack
---

# Runtime triad in spirit — three actors, the runner, the outcome algebra

This is mechanism report #6 of the schema-derived deep audit. It explains the
runtime that lives *inside* the spirit daemon: the three execution centers
(`SignalActor`, `Nexus`, `Store`), the shared driver in `triad-runtime`
(`Runner` and its five-outcome `NextStep` algebra), and the lifecycle that
starts the three centers SEMA→Nexus→Signal and stops them in reverse.

Every code claim below is backed by a command I actually ran. Run output is
pasted verbatim. Where I could not run something I say so explicitly. The
section "What I ran" at the end lists every load-bearing command with its
directory so a verifier can re-run it.

## Provenance of what I tested

I audited the working-tree source under `/git/github.com/LiGoldragon/spirit`
(crate version `0.1.0`) and `/git/github.com/LiGoldragon/triad-runtime`
(version `0.2.0`). The *deployed* CLI on this machine is a separate, older
artifact — `~/.nix-profile/bin/spirit` resolves to
`/nix/store/s6lycvzfi688qhv1814g7iwhv2x9mzdg-spirit-v0.5.1/bin/spirit-v0.5.1`.
Its schema may not match the source under audit, so for the live round-trip I
built the binaries from the exact source I am explaining and exercised those:

```
$ readlink -f ~/.nix-profile/bin/spirit
/nix/store/s6lycvzfi688qhv1814g7iwhv2x9mzdg-spirit-v0.5.1/bin/spirit-v0.5.1
$ grep -m1 '^version' /git/github.com/LiGoldragon/spirit/Cargo.toml
version      = "0.1.0"
```

The live daemon and CLI in this report are
`/git/github.com/LiGoldragon/spirit/target/debug/spirit-daemon` and
`.../spirit`, built with `cargo build --features nota-text --bins` from the
audited tree. cargo is the stable toolchain at `~/.nix-profile/bin/cargo`
(`cargo 1.95.0`).

## The shape: one daemon, three centers, one driver

`spirit` is a "component daemon" in the triad sense. Inside one process it runs
three execution centers, each owning one plane of the schema:

| Center | Type | Plane | Owns |
|---|---|---|---|
| `SignalActor` | `src/engine.rs` | Signal | admission: mint route + identifier, validate, frame reply |
| `Nexus` | `src/nexus.rs` | Nexus | the decision loop, the mail ledger, the stash table |
| `Store` | `src/store.rs` | SEMA | the durable `*.sema` database via `sema-engine` |

The three are composed by `Engine` (`src/engine.rs`), a thin holder. The
recursive consume→decide→act→re-consume cycle is NOT hand-written in spirit; it
lives once in `triad-runtime::Runner` and is shared by every component daemon.
spirit supplies only the per-component behavior hooks; the loop is generic.

The crate's own header states the boundary precisely
(`src/lib.rs:1-21`): the public wire types are *generated* from three plane
schemas through `schema-next`/`schema-rust-next`, and the hand-written code is
"the runtime shim around those generated interfaces." `build.rs` checks the
generated modules are fresh on every build (see "Schema freshness" below).

## The five-outcome algebra (triad-runtime)

The core of the whole runtime is one enum. `triad-runtime/src/runner.rs:21-28`:

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum NextStep<Reply, SemaWrite, SemaRead, Effect, Work> {
    Reply(Reply),
    SemaWrite(SemaWrite),
    SemaRead(SemaRead),
    RunEffect(Effect),
    Continue(Work),
}
```

This is the fixed algebra of what a Nexus decision can produce. Every step the
decision center takes resolves to exactly one of these five:

- `Reply` — terminate; hand a typed reply back to Signal.
- `SemaWrite` — apply a durable write, then re-enter with the write completion.
- `SemaRead` — observe storage, then re-enter with the read completion.
- `RunEffect` — perform a component-local effect, then re-enter with the effect
  completion.
- `Continue` — re-enter Nexus directly with new work, no plane dispatch.

The task brief named these `ReplyToSignal / CommandSemaWrite / CommandSemaRead /
CommandEffect / Continue`. Those are spirit's *generated* `NexusAction` variant
names; `NextStep` is the *generic library* spelling. The generated glue maps one
onto the other — that mapping is shown in the next section and is the seam
between component meaning and shared loop.

The driver itself is `Runner::drive`. `triad-runtime/src/runner.rs:147-184`,
pasted verbatim:

```rust
    pub fn drive<Engines>(&self, engines: &mut Engines, first_work: Engines::Work) -> Engines::Reply
    where
        Engines: RunnerEngines,
    {
        let mut work = first_work;
        let mut budget = self.continuation_limit.budget();

        loop {
            match engines.decide_next_step(work) {
                NextStep::Reply(reply) => return reply,
                NextStep::SemaWrite(write) => {
                    if let Err(exhausted) = budget.spend_next_step() {
                        return engines.budget_exhausted_reply(exhausted);
                    }
                    work = engines.apply_sema_write(write);
                }
                NextStep::SemaRead(read) => {
                    if let Err(exhausted) = budget.spend_next_step() {
                        return engines.budget_exhausted_reply(exhausted);
                    }
                    work = engines.observe_sema_read(read);
                }
                NextStep::RunEffect(effect) => {
                    if let Err(exhausted) = budget.spend_next_step() {
                        return engines.budget_exhausted_reply(exhausted);
                    }
                    work = engines.run_effect(effect);
                }
                NextStep::Continue(next_work) => {
                    if let Err(exhausted) = budget.spend_next_step() {
                        return engines.budget_exhausted_reply(exhausted);
                    }
                    work = next_work;
                }
            }
        }
    }
```

Two properties to read off the loop directly:

1. **`Reply` is the only exit, and it spends nothing.** The match arm for
   `Reply` returns immediately *before* touching `budget`. A decision that
   replies on the first step costs zero budget. Every other outcome spends one
   continuation step before dispatching, and an exhausted budget short-circuits
   to `budget_exhausted_reply`, which is itself a `Reply`-shaped typed value.

2. **The loop never blocks and never recurses on the stack.** Each non-reply
   outcome dispatches to a `RunnerEngines` method that returns the *next* `Work`
   item, and control comes back to the top of `loop`. "Recursion" here is a
   tail loop with an explicit step budget, not stack recursion. The budget is a
   `ContinuationLimit` (default 32, `runner.rs:1`) carried in a
   `ContinuationBudget` that saturating-increments a completed-step count
   (`runner.rs:103-115`).

The adapter trait that `drive` is generic over is `RunnerEngines`
(`runner.rs:30-48`): five associated types (`Reply`, `SemaWrite`, `SemaRead`,
`Effect`, `Work`) and the methods `decide_next_step`, `apply_sema_write`,
`observe_sema_read`, `run_effect`, and `budget_exhausted_reply`. This is the
entire surface a component must fill to get the loop for free.

### Runner tests (real run)

`triad-runtime`'s `tests/runner.rs` proves the loop and budget mechanics on a
synthetic `TestEngines`. The budget-stop test, `runner.rs:163-177`, is the
clearest witness:

```rust
fn runner_stops_before_dispatching_action_past_budget() {
    let runner = Runner::new(ContinuationLimit::new(2));
    let mut engines = TestEngines::default();

    let reply = runner.drive(&mut engines, TestWork::Write);

    let TestReply::Exhausted(exhausted) = reply else {
        panic!("expected budget exhaustion reply");
    };
    assert_eq!(exhausted.limit(), ContinuationLimit::new(2));
    assert_eq!(exhausted.completed_step_count(), 2);
    assert_eq!(exhausted.attempted_step_count(), 3);
    assert_eq!(engines.cloned_actions(), ["write", "read", "exhausted"]);
}
```

Running the whole `triad-runtime` suite — `cargo test` in
`/git/github.com/LiGoldragon/triad-runtime` — passes 27 tests across 4
integration binaries (verbatim summary):

```
     Running unittests src/lib.rs (target/debug/deps/triad_runtime-07cdddb25afc2dd4)
running 0 tests
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/argument.rs (target/debug/deps/argument-9886468e867b69e4)
running 6 tests
test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/frame.rs (target/debug/deps/frame-1fcffb96aa768cb7)
running 4 tests
test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/runner.rs (target/debug/deps/runner-61c549fb9a071357)
running 6 tests
test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/trace.rs (target/debug/deps/trace-f2edcdca4073534a)
running 11 tests
test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.10s
```

The six `runner.rs` test names (from `grep`):
`runner_returns_direct_reply_without_spending_budget`,
`runner_drives_all_non_reply_paths_until_reply`,
`runner_accepts_each_non_reply_entry_shape`,
`runner_stops_before_dispatching_action_past_budget`,
`runner_exhausts_continue_loop_without_plane_dispatch`,
`continuation_budget_reports_remaining_and_exhausted_counts`.

## How spirit plugs into the runner (the generated seam)

The generated module `src/schema/nexus.rs` carries the mapping from spirit's
`NexusAction` to the library `NextStep`, plus the `NexusEngine::execute` method
that builds a `Runner` and drives an adapter. This is the load-bearing seam.

`src/schema/nexus.rs:698-710` — the projection of component variants onto the
generic algebra:

```rust
pub type NexusRunnerNextStep = triad_runtime::NextStep<ReplyToSignal, CommandSemaWrite, CommandSemaRead, CommandEffect, NexusWork>;

impl NexusAction {
    pub fn into_runner_next_step(self) -> NexusRunnerNextStep {
        match self {
            Self::CommandSemaWrite(input) => triad_runtime::NextStep::SemaWrite(input),
            Self::CommandSemaRead(input) => triad_runtime::NextStep::SemaRead(input),
            Self::ReplyToSignal(output) => triad_runtime::NextStep::Reply(output),
            Self::CommandEffect(effect) => triad_runtime::NextStep::RunEffect(effect),
            Self::Continue(work) => triad_runtime::NextStep::Continue(work),
        }
    }
}
```

This is exactly the five-element correspondence the brief named. `ReplyToSignal`
→ `Reply`, `CommandSemaWrite` → `SemaWrite`, `CommandSemaRead` → `SemaRead`,
`CommandEffect` → `RunEffect`, `Continue` → `Continue`.

`src/schema/nexus.rs:739-752` — `NexusEngine::execute`, the default trait method
that constructs and drives the runner:

```rust
    fn execute(&mut self, input: nexus::Nexus<nexus::Work>) -> nexus::Nexus<nexus::Action>
    where
        Self: Sized,
    {
        self.trace_nexus_entered();
        let origin_route = input.origin_route();
        let first_work = input.into_root();
        let runner = triad_runtime::Runner::new(self.continuation_limit());
        let mut runner_adapter = NexusRunnerAdapter::new(self, origin_route);
        let reply = runner.drive(&mut runner_adapter, first_work);
        let output = NexusAction::reply_to_signal(reply).with_origin_route(origin_route);
        self.trace_nexus_decided();
        output
    }
```

The `NexusRunnerAdapter` (`src/schema/nexus.rs:755-799`) is the generated impl of
`RunnerEngines`. Its `decide_next_step` calls the component's hand-written
`NexusEngine::decide` and pipes the resulting action through
`into_runner_next_step`; its `apply_sema_write`/`observe_sema_read`/`run_effect`
call the component's hooks and wrap the typed completion back into a `NexusWork`
fact (`sema_write_completed`, `sema_read_completed`, `effect_completed`). So the
generated adapter does the plumbing; the component fills decision + the three
plane handlers + the budget-exhausted reply.

## Center 1 — SignalActor (admission / triage / reply)

`SignalActor` (`src/engine.rs:33-39`, impl at `164-245`) is the Signal-plane
center. Its job is admission, before any deeper layer sees the request. Three
acts:

1. **Mint an origin route and a message identifier.** `admit`
   (`src/engine.rs:175-191`):

```rust
    pub fn admit(&self, input: Input) -> Result<SignalAccepted, SignalRejected> {
        let origin_route = self.issue_origin_route();
        let signal_input = input.with_origin_route(origin_route);
        let identifier = self.issue_message_identifier();
        if let Err(validation_error) = signal_input.root().validate() {
            return Err(SignalRejected {
                origin_route,
                validation_error,
            });
        }
        ...
        Ok(SignalAccepted {
            sent: signal_input.message_sent(identifier),
            input: signal_input,
        })
    }
```

   Note the route base: `issue_origin_route` adds `ORIGIN_ROUTE_BASE`
   (`1_000_000`, `engine.rs:16`) to a monotonic counter, so routes and
   identifiers are deliberately *different* number spaces — a test asserts the
   two never coincide (`runtime_triad.rs:200-203`).

2. **Validate against schema-emitted rules** *before* anything durable. The
   `Entry` validator rejects empty topics / empty description
   (`src/engine.rs:362-375`); a rejection becomes an `Output::Rejected` carrying
   the validation error and the *current* database marker — no SEMA touched.

3. **Triage and reply** through the generated `SignalEngine` trait
   (`src/engine.rs:209-245`): `triage_inner` turns a `Signal<Input>` into a
   `Nexus<NexusWork>` fact (`NexusWork::signal_arrived(...)`), and `reply_inner`
   turns the `Nexus<NexusAction>` back into a `Signal<Output>`. The
   `into_signal_output` impl (`engine.rs:483-495`) extracts `ReplyToSignal` and
   treats any other terminal action as an internal error — the loop is supposed
   to terminate in a reply.

The composition lives in `SignalAccepted::process_with` (`src/engine.rs:267-294`):
the **sent hook fires at the Signal→Nexus handoff before any SEMA state changes**,
then `NexusEngine::execute` runs (driving the runner), then the **processed hook
fires after the reply is framed**. The comment is explicit that the `&mut Nexus`
exclusive borrow held across `execute` "is the single-flight guard" — one request
is in flight through Nexus at a time.

## Center 2 — Nexus (decide / execute, mail keeper)

`Nexus` (`src/nexus.rs:82-89`) owns three things: the `Store` (SEMA), the
`MailLedger`, and the `StashTable`. It is the decision center.

The hand-written behavior is `step_decide` (`src/nexus.rs:228-235`): consume one
`NexusWork` fact, emit one `NexusAction`:

```rust
    fn step_decide(&self, work: NexusWork) -> NexusAction {
        match work {
            NexusWork::SignalArrived(input) => self.decide_signal_arrival(input),
            NexusWork::SemaWriteCompleted(output) => self.decide_sema_write_completion(output),
            NexusWork::SemaReadCompleted(output) => self.decide_sema_read_completion(output),
            NexusWork::EffectCompleted(result) => self.decide_effect_completion(result),
        }
    }
```

Routing of an arriving Signal (`src/nexus.rs:237-263`): `Record`/`Remove` become
`CommandSemaWrite`; `Observe`/`Lookup`/`Count` become `CommandSemaRead`;
`LookupStash` is resolved directly from the in-memory stash table and replies
immediately (no plane dispatch — a `ReplyToSignal` on the first step, which the
runner returns without spending budget).

The interesting case is the **recursive Observe→Stash→Reply** flow, which is
the pilot proof that the loop is genuinely recursive rather than a single
read-then-reply. `decide_sema_read_completion` (`src/nexus.rs:277-298`) does NOT
reply with the records on a successful observe; it issues an *effect*:

```rust
            SemaReadOutput::Observed(observed) => {
                // Observe's slim-output path per Spirit 1389: recurse
                // through Stash effect so the wire reply carries a
                // handle, not the full record set.
                let database_marker = observed.database_marker;
                let records = observed.record_set;
                NexusAction::command_effect(NexusEffectCommand::stash(StashRequest {
                    records,
                    database_marker,
                }))
            }
```

Then `decide_effect_completion` (`src/nexus.rs:300-312`) turns the `Stashed`
result into the slim `Output::RecordsStashed` (handle + count + marker). So one
Observe drives at least four runner steps: `SignalArrived` → `CommandSemaRead`
→ (SEMA read) → `SemaReadCompleted` → `CommandEffect(Stash)` → (effect) →
`EffectCompleted(Stashed)` → `ReplyToSignal`. That exercises *all five* outcome
shapes on one real request path. The effect itself is applied by `apply_effect`
(`src/nexus.rs:136-146`), which mints a handle in the `StashTable`
(`src/nexus.rs:33-51`).

Nexus's `NexusEngine` impl (`src/nexus.rs:153-217`) wires the component into the
generated trait: `decide` calls `step_decide`; `apply_sema_write` /
`observe_sema_read` delegate to `SemaEngine` on the store; `run_effect` calls
`apply_effect`; and `budget_exhausted_reply` builds an `Output::error` naming the
step count and limit. Its `on_start`/`on_stop` start and stop the SEMA store
(this is what makes the lifecycle ordering work — see below).

## Center 3 — Store (SEMA durable state)

`Store` (`src/store.rs:34-49`) is the SEMA-plane center: an identified
`sema-engine` table persisted to a `*.sema` file. SEMA means database work. The
store maps generated SEMA roots onto sema-engine operations. The
`SemaEngine::apply_inner` (`src/store.rs:70-105`) handles writes
(`Record`→`assert_identified`, `Remove`→`retract_identified`);
`observe_inner` (`src/store.rs:107-159`) handles reads (`Observe`/`Lookup`/`Count`),
with predicate semantics (`Query::matches`, `src/store.rs:323-329`) kept here
because they are Spirit-specific, not generic plumbing.

The durable marker is real, not a counter fiction. `database_marker`
(`src/store.rs:260-294`) is `(commit_sequence, state_digest)` where the digest is
a blake3 hash folded over the commit sequence and every committed record's
`(identifier, archived rkyv bytes)`, truncated to the schema `Integer` width. An
empty store digests to `(0, 0)`. This is why every reply below carries a
`(1, 16589728118828494936)` marker after the first write — commit sequence 1, a
real content hash.

## Lifecycle — start SEMA→Nexus→Signal, stop reverse

`Engine::start`/`Engine::stop` (`src/engine.rs:93-106`) start the centers
innermost-first and stop them outermost-first:

```rust
    pub fn start(&mut self) -> Result<(), ActorStartFailure> {
        {
            let mut nexus = self.nexus.lock().expect("nexus lock");
            NexusEngine::on_start(&mut *nexus)?;
        }
        SignalEngine::on_start(&mut self.signal_actor)
    }

    pub fn stop(&mut self) -> Result<(), ActorStopFailure> {
        SignalEngine::on_stop(&mut self.signal_actor)?;
        let mut nexus = self.nexus.lock().expect("nexus lock");
        NexusEngine::on_stop(&mut *nexus)?;
        Ok(())
    }
```

`NexusEngine::on_start` first calls `SemaEngine::on_start` on the store
(`src/nexus.rs:154-159`) *before* tracing its own start — so the observable order
is SEMA, then Nexus, then Signal on the way up; Signal, then Nexus, then SEMA on
the way down. The `instrumentation_logging` test asserts exactly this sequence
(`tests/instrumentation_logging.rs:128-138`):

```rust
    assert_activation_names(
        &trace_log.events(),
        &[
            "SemaStarted",
            "NexusStarted",
            "SignalStarted",
            "SignalStopped",
            "NexusStopped",
            "SemaStopped",
        ],
    );
```

I ran this one test under `--features testing-trace` and it passes (verbatim):

```
running 1 test
test testing_trace_records_lifecycle_hooks_from_generated_engine_traits ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 3 filtered out; finished in 0.01s
```

## spirit test suite (real run)

`cargo test` in `/git/github.com/LiGoldragon/spirit` (default features) runs the
runtime-triad coverage. Verbatim per-binary results:

```
     Running tests/daemon_command.rs
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/dependency_surface.rs
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.18s
     Running tests/generated_signal_plane.rs
test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/operator_271_closed_claims.rs
test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/runtime_triad.rs
test result: ok. 20 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
     Running tests/socket_negative.rs
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

The two `lib.rs`/`spirit-daemon.rs` unit harnesses report 0 tests (no unit
tests; this crate's tests are integration tests). Three further test files —
`instrumentation_logging`, `nix_integration`, `process_boundary` — are gated by
`required-features` in `Cargo.toml` (`testing-trace`, `nota-text`, `nota-text`
respectively) and so do not run under default features. I ran them separately
below; this is a real gating fact, not a skipped test.

The 20 `runtime_triad` tests are the heart of the audit. Representative names
(from `grep`): `nexus_runner_loop_routes_record_input_to_sema_write_command_then_back_to_reply`,
`signal_actor_pushes_accepted_message_through_sent_hook_before_nexus_holds_mail`,
`nexus_step_decide_routes_signal_arrival_to_sema_command_without_committing`,
`engine_lifecycle_runs_generated_trait_hooks_without_actor_mailboxes`,
`sema_read_miss_completion_routes_through_runner_loop_to_error_reply`,
`full_runtime_triad_records_then_observes_through_durable_sema_with_stash`,
`full_runtime_triad_looks_up_and_counts_through_signal_nexus_and_sema`,
`sema_store_persists_records_across_reopen_of_the_same_sema_file`.

The keystone, `runtime_triad.rs:771-849`, asserts the full recursive flow:
record an entry, observe it (gets a slim `RecordsStashed` reply, NOT the full
set), then `LookupStash` the handle to recover the full records — with mail
ledger counts checked at each step (Sent + Processed = 6 events for 3
round-trips).

## Live CLI↔daemon round-trip (real, end to end)

I ran a genuine round-trip against a live daemon over a real Unix socket, using
the binaries built from the audited source. I started the daemon in the
background:

```
$ /git/.../spirit/target/debug/spirit-daemon /tmp/spirit-live/spirit.config.rkyv &
daemon pid=2760411
$ ls -la /tmp/spirit-live/spirit.sock
srwxr-xr-x 1 li users 0 Jun  4 20:13 /tmp/spirit-live/spirit.sock
```

The daemon takes exactly one argument: a path to a binary (rkyv) `Configuration`
file. It refuses inline NOTA and refuses zero arguments — I verified both:

```
$ spirit-daemon
spirit-daemon: daemon argument error: expected exactly one component argument, received 0
$ spirit-daemon "(Configuration [x] [y])"
spirit-daemon: daemon argument error: expected a signal-encoded file path, received inline text
```

(I produced the rkyv config with a 12-line throwaway crate in `/tmp`, *outside*
the repo, that path-depends on the spirit checkout and calls
`Configuration::new(...).write_binary_file(...)`. I did not edit any repo
source.)

Then I drove the CLI (`spirit`), which parses one NOTA argument, connects to
`$SPIRIT_SOCKET`, exchanges length-prefixed rkyv frames, and prints the typed
`Output` as NOTA. Verbatim CLI output for the four core operations:

```
=== 1. Record (Signal admit -> CommandSemaWrite -> SEMA write -> ReplyToSignal) ===
(RecordAccepted (1 (1 16589728118828494936)))
=== 2. Count (Signal -> CommandSemaRead -> SEMA read -> ReplyToSignal) ===
(RecordsCounted (1 (1 16589728118828494936)))
=== 3. Observe (Signal -> CommandSemaRead -> Observed -> CommandEffect(Stash) -> EffectCompleted -> RecordsStashed) ===
(RecordsStashed (1 1 (1 16589728118828494936)))
=== 4. LookupStash 1 (slim handle resolves to full records) ===
(RecordsObserved ([([[runtime-triad]] Decision [audit report 6 live round trip] Medium Zero)] (1 16589728118828494936)))
```

Read these against the algebra:

- `(RecordAccepted (1 (1 16589728118828494936)))` — record identifier `1`,
  marker `(commit_sequence 1, state_digest 16589728118828494936)`. The write
  drove `SignalArrived(Record)` → `CommandSemaWrite` → SEMA `assert_identified`
  → `SemaWriteCompleted(Recorded)` → `ReplyToSignal(RecordAccepted)`.
- `(RecordsCounted (1 ...))` — a `CommandSemaRead` path; count `1`.
- `(RecordsStashed (1 1 ...))` — `stash_handle 1`, `record_count 1`. This is the
  **recursive** path: a read that found records did not reply; it issued
  `CommandEffect(Stash)` and only the `EffectCompleted(Stashed)` produced the
  reply. The slim reply carries the handle, not the records.
- `(RecordsObserved ([(...full Entry...)] ...))` — the follow-up `LookupStash 1`
  resolves the handle from the in-memory `StashTable` back to the full record
  set, reproducing the very Entry I recorded.

I also exercised the two non-success paths live:

```
=== Empty-topic Record: SignalActor rejects BEFORE Nexus/SEMA ===
(Rejected (EmptyTopic (1 16589728118828494936)))
=== Lookup a nonexistent record id 999 (SEMA read miss -> error reply) ===
(Error ([record not found] (1 16589728118828494936)))
```

`(Rejected (EmptyTopic ...))` proves admission validation fires in `SignalActor`
before any plane dispatch — and the marker is still the pre-existing `(1, ...)`,
confirming no write happened. `(Error ([record not found] ...))` proves a SEMA
read *miss* routes back through the runner loop to an error reply
(`SemaReadOutput::Missed` → `ReplyToSignal(Error)`), matching the test
`sema_read_miss_completion_routes_through_runner_loop_to_error_reply`.

The daemon wrote a real `*.sema` file (durable):

```
$ ls -la /tmp/spirit-live/spirit.sema
-rw-r--r-- 1 li users 561152 Jun  4 20:14 /tmp/spirit-live/spirit.sema
```

The daemon's stderr log was empty (clean run), and I stopped the process
cleanly afterward (`kill` → "daemon stopped").

This is a real CLI↔daemon round-trip, not a description. I additionally ran the
in-repo `process_boundary` integration test, which spawns the *same* daemon
binary and drives the *same* CLI binary over a socket — verbatim:

```
     Running tests/process_boundary.rs (target/debug/deps/process_boundary-225b7cba928652f3)
running 4 tests
test cli_renders_alias_payload_outputs_without_wrapper_repetition ... ok
test cli_and_daemon_exchange_nota_over_rkyv_socket ... ok
test daemon_persists_sema_file_across_a_restart ... ok
test candidate_daemon_handover_from_production_copy_preserves_original_sema_database ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.10s
```

(The 5th `process_boundary` test,
`cli_receives_testing_trace_events_from_daemon_trace_socket`, additionally
requires `testing-trace`; it does not run under `nota-text` alone.)

## Schema freshness — build.rs checks, does not silently regenerate

`build.rs` (`spirit/build.rs`) constructs a `GenerationPlan` for the three
plane modules and calls `.write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")`.
Without that env var, the build *checks* that the checked-in `src/schema/*.rs`
match what the schemas would generate; with it set, it writes them. A plain
`cargo build` therefore fails loudly if generated source drifts from the schema.
I confirmed the check passes on the current tree:

```
$ cargo build      # in /git/.../spirit, no SPIRIT_UPDATE_SCHEMA_ARTIFACTS
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

and the artifacts (both the generated Rust and the `.asschema` machine schema)
are present:

```
schema/:    nexus.asschema nexus.schema sema.asschema sema.schema signal.asschema signal.schema
src/schema/: nexus.rs (28098 b)  sema.rs (22810 b)  signal.rs (37438 b)
```

## What I could NOT run / honest gaps

- I did **not** test the *deployed* `spirit-v0.5.1` binary's round-trip. Its
  schema may differ from the audited source, so testing it would not validate
  the code I am explaining. I deliberately built and exercised the binaries
  from the exact audited tree instead, and I flagged the version mismatch.
- The `nix_integration` test (which builds binaries through Nix and exchanges
  rkyv frames against nix-built artifacts) I did NOT run. It requires a Nix
  build of the flake; the `process_boundary` test covers the same CLI↔daemon
  socket round-trip against cargo-built binaries, which I ran. Running the Nix
  path is a larger, network-and-store-touching operation I judged out of scope
  for safe execution here.
- The throwaway config-writer crate in `/tmp/spirit-cfg-helper` is mine, not
  part of either repo. It exists only to serialize a `Configuration` rkyv file
  so I could start the daemon by hand; it edits nothing in the repos.

## What I ran (for the verifier)

All commands used cargo at `~/.nix-profile/bin/cargo` (1.95.0). Directories are
absolute.

1. `cargo test` in `/git/github.com/LiGoldragon/triad-runtime` — 27 tests pass
   (argument 6, frame 4, runner 6, trace 11).
2. `cargo test` in `/git/github.com/LiGoldragon/spirit` — default-feature suite
   passes (runtime_triad 20, generated_signal_plane 6, operator_271 6,
   socket_negative 3, dependency_surface 3, daemon_command 2).
3. `cargo build --features nota-text --bins` in `/git/.../spirit` — builds the
   `spirit` + `spirit-daemon` binaries from the audited source.
4. `cargo test --features nota-text --test process_boundary` in `/git/.../spirit`
   — 4 real CLI↔daemon socket round-trip tests pass.
5. `cargo test --features testing-trace --test instrumentation_logging testing_trace_records_lifecycle_hooks_from_generated_engine_traits`
   in `/git/.../spirit` — lifecycle ordering test passes.
6. `cargo build` in `/git/.../spirit` — build.rs schema freshness check passes.
7. Live daemon start + 6 CLI invocations (Record / Count / Observe /
   LookupStash / empty-topic Record / Lookup 999) against
   `target/debug/spirit-daemon` + `target/debug/spirit` over a Unix socket in
   `/tmp/spirit-live` — typed NOTA replies as pasted above; daemon stopped
   cleanly.
