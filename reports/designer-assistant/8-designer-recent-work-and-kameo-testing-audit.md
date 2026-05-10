# 8 - Designer recent work and Kameo testing audit

*Designer-assistant read-only audit of the designer's latest actor/Kameo
work, especially `reports/designer/106-actor-discipline-status-and-questions.md`
and `/git/github.com/LiGoldragon/kameo-testing`. No code or skill edits
were made for this report.*

---

## Scope

I reviewed:

- `reports/designer/106-actor-discipline-status-and-questions.md`
- the commit that deleted `reports/designer/104-actor-runtime-and-naming.md`
  and `reports/designer/105-actor-discipline-sweep.md`
- the `skills/reporting.md` addition about asking user questions with
  evidence inline
- `/git/github.com/LiGoldragon/kameo-testing`, especially commit
  `ea1d417f`
- `kameo-testing` docs, architecture, findings, and tests

I also ran:

- `cargo test` in `/git/github.com/LiGoldragon/kameo-testing`
- `nix flake check` in `/git/github.com/LiGoldragon/kameo-testing`
- `nix build .#checks.x86_64-linux.default --print-build-logs`

---

## What Looks Good

`reports/designer/106-actor-discipline-status-and-questions.md` is a
useful consolidation. Deleting 104/105 and carrying forward the live
questions into one report reduces drift. The report also follows the new
evidence-inline question rule well: the user can read the relevant code
shape, tradeoffs, and recommendation without opening five old reports.

The reporting skill change is high signal. `skills/reporting.md`
now says user-facing questions must include the evidence, options, and
tradeoffs in the question itself. That is correct for this workspace.

The `kameo-testing` self-fix was real:

- `Arc<Mutex<Vec<Trace>>>` in `tests/streams.rs` is gone.
- `std::convert::Infallible` was replaced with
  `kameo::error::Infallible`.
- the registry post-shutdown sleep was removed and replaced with a
  stronger FIFO/shutdown explanation.

Verification:

- `cargo test` passed: 29 tests.
- `cargo test` emitted one warning: unused `SupervisionStrategy` import
  in `tests/supervision.rs`.
- `nix flake check` reported all checks passed, though it also printed
  `running 0 flake checks`; the explicit `nix build
  .#checks.x86_64-linux.default` command succeeded.

---

## Problems I Found

### 1. `kameo-testing` still has magic sleeps

Designer/106 marks "magic delays" as done, but the test repo still has
sleep-based synchronization:

- `tests/links.rs:77-78` waits 100ms for link death to traverse.
- `tests/links.rs:98` waits 100ms to prove unlink prevented link death.
- `tests/supervision.rs:92-102` polls every 20ms until restart.
- `tests/supervision.rs:125-127` sleeps 200ms to prove no restart.
- `tests/supervision.rs:150-160` sleeps between crash/restart-limit
  steps.

Some sleeps are legitimate behavior-under-test delays:

- `tests/messages.rs` uses sleep to prove `tell` and `DelegatedReply`
  do not block the mailbox.
- `tests/mailbox.rs` uses a slow handler to saturate a bounded mailbox.

The remaining link/supervision sleeps should be replaced with
`oneshot`/`watch` witnesses or structured stop-reason checks, matching
the patterns already added to `skills/kameo.md`.

### 2. `kameo-testing` docs are stale after report deletion

`/git/github.com/LiGoldragon/kameo-testing/ARCHITECTURE.md:45` still
points to `~/primary/reports/designer/102-kameo-deep-dive.md`, which no
longer exists. The repo should point to `reports/designer/106...`,
`skills/kameo.md`, and `notes/findings.md`.

This is a general rule: when designer deletes superseded reports, active
repos and current skills need a reference sweep.

### 3. `kameo-testing` architecture overstates test coverage

`ARCHITECTURE.md` says `tests/spawn.rs` covers `prepare/run` and
`spawn_in_thread`, but the file currently only covers:

- `spawn`
- `spawn_with_mailbox`
- unbounded mailbox

No `PreparedActor::run` test exists in the designer repo. No
`spawn_in_thread` test exists there either. Those behaviors are in the
skill now, so the evidence repo should prove them.

The designer-assistant Kameo repo does cover `PreparedActor::run`, but
the designer repo's own architecture says *this* repo backs
`skills/kameo.md`. It should either add the tests or make the code map
honest.

### 4. `tests/topology.rs` still uses the old name `ClaimNormalize`

The current skill/report position is `ClaimNormalizer`, not
`ClaimNormalize`. `kameo-testing/tests/topology.rs:21` still defines
`struct ClaimNormalize`. This is small, but it is exactly the flagship
example drift that designer/105 identified.

### 5. Designer/106 is good, but it risks becoming "questions in a report"

The report asks the right questions, but reports do not execute work.
The application questions should become beads or explicit chat
questions. Otherwise we get a polished inventory and no owner.

The strongest case is Q-app-1: five data-type-shadowed actors. The rule
has already spoken. This should be one batched P2 bead, not another
round of design.

---

## Questions For Li

### Q1. Are trace-phase actors real actors, or should they collapse?

Evidence from `reports/designer/106...`: `DispatchSupervisor`,
`IngressSupervisor`, `DomainSupervisor`, and `ViewSupervisor` mostly hold
downstream `ActorRef<_>` fields and forward while recording trace events.
The current rule says forwarding helpers are not actors. The counterpoint
is that trace emission may itself be the domain: these phases witness
that the pipeline ran.

Options:

- Collapse them into `MindRoot`; trace emission becomes helper calls.
- Keep them, but rename `*Supervisor` to `*Phase` and document a
  trace-phase carve-out.

My recommendation: keep only if the trace is architecture truth, then
rename to `*Phase`. If the trace is just observability, collapse.

### Q2. Should designer file beads now for the rule-applications?

Evidence: Q-app-1 and Q-app-3 in designer/106 are no longer philosophical.
They are application work.

Options:

- File one batched P2 bead for the five data-type-shadowed actor
  collapses/deletes.
- File one P2 bead for the `ActorKind` split, blocked by the trace-phase
  decision.
- Wait for operator's natural cycle.

My recommendation: file beads now. The contract naming work can continue;
beads make the actor cleanup visible without forcing immediate execution.

### Q3. Should persona-mind be a daemon?

Evidence: designer/106 Q-dec-1 keeps the one-shot CLI vs daemon decision
open. A one-shot actor per CLI call is simpler but weakens the value of a
supervision tree and warmed state. A daemon makes the actor topology
observable across requests and better matches "central mind state."

My recommendation: daemon.

### Q4. Should contract types validate their wire invariants?

Evidence: designer/106 Q-dec-2 asks whether `WirePath` / `TaskToken`
validation lives in the contract or runtime.

My recommendation: contract validates shape and local invariants; runtime
validates world facts like "target exists." Contract repos are the typed
architecture that consumers cannot escape.

### Q5. Should state-owning actors default to `RestartPolicy::Never`
until durable recovery exists?

Evidence: Kameo restart reconstructs actors from `Args`, not from mutated
state. A state-owning actor with `Permanent` restart can silently lose
state and continue running.

My recommendation: yes. Add the workspace rule: state-owning actors use
`RestartPolicy::Never` unless the actor has an explicit durable recovery
story.

---

## Suggestions

### Designer should do next

1. Turn Q-app-1 into one batched bead:
   "apply data-type-shadowing rule across persona-* actors."

2. Ask Li Q1 directly, with the dispatch code inline:
   keep trace phases as actors and rename to `*Phase`, or collapse them
   into `MindRoot`.

3. Turn Q-dec-4 into a designer-assistant pre-pass:
   re-read `reports/designer/100-persona-mind-architecture-proposal.md`
   against current `persona-mind` code and verify which pins still
   matter after the Kameo topology changes.

4. Fix `kameo-testing` before using it as a strict citation source:
   remove the leftover sleeps, remove the unused import, rename
   `ClaimNormalize`, add `PreparedActor::run` and `spawn_in_thread`
   tests, and update stale report links.

### Skill changes worth landing after Li confirms

1. `actor-systems.md`: state-owning actors default to
   `RestartPolicy::Never` without durable recovery.

2. `naming.md`: clarify when `Subscriber` is a role noun vs a bad
   trait-participation suffix.

3. `actor-systems.md`: counter-only fields are allowed as test
   witnesses only when at least one test reads them.

4. `kameo.md`: document `OneForAll` / `RestForOne` restart-policy
   bypass behavior if a focused test proves it.

---

## Bottom Line

Designer is converging the workspace in the right direction. The latest
report is useful, and the Kameo test repo is healthy enough to trust for
many claims.

The main risk is that the work is still producing excellent reports
faster than it is producing closed decisions and tracked work. The next
move should be fewer reports, more beads, and a cleanup pass on
`kameo-testing` so the evidence repo is as strict as the skills now say
it is.
