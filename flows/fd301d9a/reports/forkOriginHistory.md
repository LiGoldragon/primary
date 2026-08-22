# Why the Kameo fork exists: historical reconstruction

The repository does not state the fork’s originating human or production cause. It does preserve a same-day sequence of lifecycle experiments whose tests expose the problems the fork mechanics address. The strongest defensible account is therefore: the fork’s recorded history establishes a problem sequence around shutdown completion, state/resource release, lifecycle publication, and control-signal delivery; it does not establish what first prompted that work.

## Causal anatomy from direct evidence

```text
mailbox closure used as shutdown wait
  [8f44e1a test: hook completes, but Drop/resource release is not proven]
        |
        v
wait on shutdown result
  [8f44e1a: hook-complete wait]
        |
        v
actor state can still be alive after the wait
  [8f44e1a test: “hook-complete, not actor-state-drop”]
        |
        v
drop actor before completion / notification
  [4ba9c25 test: Drop witness and TCP rebind precede return]
        |
        v
publish an explicit terminal lifecycle fact
  [1b918b0 prototype phases; 1329a64/1325f6a terminal outcome]
        |
        +--> supervisors/links receive state-absence + terminal reason
        |    [1329a64/1325f6a link and restart tests]
        |
        +--> ordinary queue cannot delay lifecycle control
        |    [44c0552/da0f64a control-lane tests]
        |
        +--> weak compatibility results wait for terminal publication
             [22514f7/8ea1e3f helper test]
```

The arrows are a compact rendering of test and source order. They are not a claim that a commit message spelled out this entire design.

## What the history directly records

### Chronology and ancestry

The current fork `main` is `3486e4f6`, with its lifecycle work rebased onto upstream `4d2e2d02`. The current lifecycle commits are `1325f6a`, `da0f64a`, `1980e34`, `8ea1e3f`, followed by `f491b45` and the docs-only `3486e4f`.

The May 16 origin objects are retained under `refs/jj/keep/`. The first three experiments, `8f44e1a`, `4ba9c25`, and `1b918b0`, all have `e5d07fd` as parent. They are parallel snapshots, not one Git ancestry. The original prototype line continues from `1b918b0` through `1329a64`, `44c0552`, `04f6e2a`, and `22514f7`; the current six-commit fork line contains rebased equivalents with new parents. This graph distinction matters: temporal order and similar subjects support a development sequence, but Git does not prove the author’s internal reasoning.

Every lifecycle commit body inspected is empty. The only explicit commit-level descriptions are:

| Commit | Subject | Directly recorded change |
|---|---|---|
| `8f44e1a` | `actor: make shutdown wait for hook result` | wait on `shutdown_result` instead of mailbox closure |
| `4ba9c25` | `actor: release state before shutdown completion` | drop actor state before completion; stop returning `A` from run/spawn |
| `1b918b0` | `actor: prototype push-based lifecycle phases` | push monotonic lifecycle phases |
| `1329a64` / `1325f6a` | `actor: publish terminal lifecycle outcomes` | typed state absence/reason and terminal publication |
| `44c0552` / `da0f64a` | `actor: split lifecycle control mailbox` | separate ordinary and control lanes |
| `04f6e2a` / `1980e34` | `actor: cover lifecycle control edge cases` | test control priority, admission, and queued-message fate |
| `22514f7` / `8ea1e3f` | `actor: gate weak shutdown result helpers` | hide compatibility result until terminal publication |
| `f491b45` | `fix lifecycle fork after upstream rebase` | rebase fixups |

No subject or body names a production incident, workspace consumer, upstream issue, or human requirement.

### Test-recorded sequence

`8f44e1a` begins with `ActorRef::wait_for_shutdown` waiting on `mailbox_sender.closed().await` and changes it to `shutdown_result.wait().await`. Its new `tests/shutdown_order.rs` contains a `ResourceActor` with a delayed `on_stop`, delayed `Drop`, and a TCP listener. The test `threaded_actor_wait_for_shutdown_waits_for_on_stop` asserts that `on_stop` completes before the wait returns, but also says “short fix should not pretend wait_for_shutdown waits for actor drop.” The test `threaded_actor_wait_for_shutdown_still_does_not_prove_resource_release` asserts that the listener still cannot be rebound after the wait and describes the wait as “hook-complete, not actor-state-drop.”

The parallel `4ba9c25` keeps the result wait, adds `drop(actor)` before shutdown completion and link notification, and changes `PreparedActor::run`, `spawn`, and `spawn_in_thread` to consume the actor state instead of returning `A`. Its test `threaded_actor_wait_for_shutdown_waits_for_actor_drop_and_resource_release` requires the drop witness and TCP rebind before `wait_for_shutdown` returns. This is direct evidence that the earlier hook-complete wait was insufficient for the tested resource-release property.

`1b918b0` adds monotonic `ActorLifecyclePhase` values. The source comment says phase watchers wait for a pushed phase “rather than inferring lifecycle progress from a side-effect such as a closed mailbox.” Its test waits for `StateReleased`, observes the `on_stop` and `Drop` witnesses, verifies rebind, and then waits for `Terminated`. This is an explicitly labeled prototype and is not the current main ancestry.

`1329a64` and rebased `1325f6a` turn that lifecycle observation into `ActorTerminalOutcome { state, reason }`. The terminal path in `src/actor/spawn.rs` runs `on_stop`, drops actor state, awaits link notification, unregisters the actor, publishes the compatibility shutdown result, and sets the terminal outcome. The tests cover:

- `wait_for_shutdown_returns_after_cleanup_drop_and_notifications`: a `Dropped`/`Stopped` outcome, both witnesses, and resource rebind;
- `message_admission_stops_before_cleanup_finishes`: ordinary admission closes while cleanup is still running, without claiming terminal state;
- `link_signal_delivers_terminal_outcome_to_actor_hook`: the linked observer receives the same terminal outcome;
- `startup_failure_returns_never_allocated_outcome` and `stop_error_returns_cleanup_failed_outcome`;
- `supervisor_restart_waits_for_terminal_outcome_before_replacement_start`: replacement startup sees the old child’s drop first.

`44c0552` and rebased `da0f64a` put ordinary messages and lifecycle signals on separate channels. The tests `control_signals_do_not_wait_for_bounded_user_mailbox_capacity` and `pending_bounded_user_send_cannot_cross_closed_admission` fill or block ordinary work, send lifecycle control, and assert control completion, rejection of racing ordinary sends, and no processing of ordinary work after stop wins. The mailbox implementation carries a generation on ordinary messages, gates admission, and uses an unbounded control lane.

`04f6e2a` and rebased `1980e34` record edge semantics in both code comments and tests: ordinary admission closes as shutdown starts; lifecycle/control signals remain accepted until terminal outcome; the in-flight ordinary message can finish; queued ordinary messages are discarded rather than drained once stop is processed; and a blocking receive wakes for a late control signal. `22514f7` and rebased `8ea1e3f` then gate weak shutdown-result helpers on `is_terminated()`, with `weak_shutdown_result_helpers_wait_for_terminal_lifecycle` proving they remain empty before terminal publication.

## Motivation classification

### Explicitly recorded

The commit subjects explicitly record mechanisms and API changes, as listed above. The tests explicitly state the properties they enforce: hook completion; state drop; resource release; terminal outcome classification; control signal delivery despite ordinary saturation; rejection of stale or racing ordinary messages; and compatibility-result visibility only after terminal lifecycle publication.

The historical agent-authored actor-systems report records a broader “release before notify” contract and names possible resource races involving redb handles, sockets, and file locks. That is a prior report, not a commit body or a psyche-approved motivation. It is evidence of a written workspace rule that matches the tests, not proof of the fork’s original cause.

### Rationale inferable from code and tests

The code/test shape supports these explanations:

1. Mailbox closure was an insufficient public terminal fact. Waiting on a shutdown result made the wait hook-complete, while delayed `Drop` showed that hook completion alone did not prove state/resource release.
2. Dropping state before completion and link notification creates a happens-before point for resources and supervisors. TCP rebind and replacement-start tests exercise that point directly.
3. A pushed phase or terminal cell avoids using incidental channel closure as lifecycle evidence and gives references one shared terminal fact.
4. A separate control lane prevents a full or blocked ordinary queue from delaying stop and link-death signals. Admission/generation checks define the fate of ordinary messages racing with shutdown.
5. Gating weak helpers prevents an older compatibility result from becoming visible between hook completion and full terminal publication.

These are explanations of observed design behavior, not claims that the author wrote or consciously used these words at fork creation.

### Unknown

The originating event remains unknown. Specifically, the inspected record does not establish:

- whether a production failure or only a design concern initiated the May 16 work;
- whether any workspace consumer experienced a held-resource restart race, control deadlock, premature result race, or mailbox-closure race;
- whether all fork mechanisms were required by one initial contract or accumulated through experiments;
- why a terminal outcome includes `Ejected`, which has no producing path found in the fork source;
- whether the early parallel commits were competing designs, rapid snapshots, or another workflow artifact;
- whether upstream’s later lifecycle fixes overlap the same original problem;
- what the living psyche would choose as the final actor lifecycle contract.

The documented transcript search could not run: `transcript` is not installed or otherwise unavailable in this workspace. No typed-transcript line is therefore cited as fork-origin evidence.

## Written-psyche boundary

The written psyche gives current design context, not May-origin evidence. It says:

> re actors: we are definitely using kameo actors in nexus. I just
> havent designed the standards of use

Source: `psyche-raw/Vision/actorLibrary.md`, 2026-08-22.

It also says:

> I want to dedicate a flow to the actor question. Everything was
> done by previous flows that received little to no guidance on design
> in this respect. Distrust it all, including our fork.

Source: `psyche-raw/Vision/actorLibrary.md`, 2026-08-22.

Earlier context says:

> I want the main engine to be driven by actors. And we did actually even fork the actor
> library that we were using.

Source: `psyche-raw/Vision/rustComponentArchitecture.md`, 2026-08-14.

These words settle Kameo’s current role as the Nexus actor layer and leave standards of use open. They do not say why the fork was created, and they do not approve any specific terminal-lifecycle mechanism.

## Result for the consumer/design map

Consumers inherit a fork whose direct historical pressure is lifecycle correctness around shutdown, state/resource release, supervision notification, and control-vs-ordinary message ordering. Most production consumers call `wait_for_shutdown()` but ignore its returned outcome; direct outcome assertions are concentrated in the Kameo testbed and a Persona test, and no inspected production consumer implements `on_link_died`. This means the fork’s semantics may matter transitively even where its richer API is not inspected, but the workspace evidence does not show which semantics are load-bearing in deployment.

The design-pressure map should therefore show a known lifecycle-test sequence feeding the fork API, a separate branch of written-psyche pressure selecting Kameo while distrusting inherited standards, and an unresolved node for the original human/production cause. It should not draw a causal edge from the current psyche to the May implementation beyond the later statement that Kameo was forked.

## Sources

- Witness: `flows/fd301d9a/witnesses/forkOriginHistory.md`
- Witness: `flows/fd301d9a/witnesses/kameoFork.md`
- Witness: `flows/fd301d9a/witnesses/kameoConsumers.md`
- Witness: `flows/fd301d9a/witnesses/psycheActorDirection.md`
- `/git/github.com/LiGoldragon/kameo` commits `8f44e1a`, `4ba9c25`, `1b918b0`, `1329a64`, `44c0552`, `04f6e2a`, `22514f7`, `1325f6a`, `da0f64a`, `1980e34`, `8ea1e3f`, `f491b45`, and `3486e4f`
- `/git/github.com/LiGoldragon/kameo/tests/shutdown_order.rs`
- `/git/github.com/LiGoldragon/kameo/tests/lifecycle_phases.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor/actor_ref.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor/lifecycle.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor/spawn.rs`
- `/git/github.com/LiGoldragon/kameo/src/mailbox.rs`
- `reports/ActorForkAssessment-2026-08-14.md`
- `reports/KameoForkReview-2026-08-21.md`
- `reports/PreResetCorpus-2026-06-07/skills/actor-systems.md`
- `flows/15b67974/log.md`
- `flows/cc4105a6/reports/upstreamKameo.md`
- `flows/fb50d4a5/reports/kameoForkUpstream.md`
- `flows/01a02929/reports/kameoForkAndUpstream.md`
- `psyche-raw/Vision/actorLibrary.md`
- `psyche-raw/Vision/rustComponentArchitecture.md`
- `psyche-raw/Vision/nexus.md`
- `psyche-raw/Vision/worldModelBeforeCode.md`
- `psyche-raw/Intent/mandatoryTraits.md`
- `transcript-search` skill instruction at `.agents/skills/transcript-search/SKILL.md` (command unavailable)
