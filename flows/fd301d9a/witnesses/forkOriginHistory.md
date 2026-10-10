# Kameo fork origin history

Method: probe `git -C /git/github.com/LiGoldragon/kameo show -s --format=fuller <commit>` for the lifecycle commits and `git -C /git/github.com/LiGoldragon/kameo show --stat <commit>`.

Method: probe `git -C /git/github.com/LiGoldragon/kameo show <commit> -- tests/shutdown_order.rs tests/lifecycle_phases.rs src/actor/actor_ref.rs src/actor/spawn.rs src/actor/lifecycle.rs src/mailbox.rs`.

Method: probe `git -C /git/github.com/LiGoldragon/kameo show -s --format='%h %H %P %ad %cd %s' --date=iso-strict <commit>` and `git -C /git/github.com/LiGoldragon/kameo for-each-ref --format='%(refname) %(objectname) %(subject)'`.

Method: code read `reports/ActorForkAssessment-2026-08-14.md`, `reports/KameoForkReview-2026-08-21.md`, `reports/PreResetCorpus-2026-06-07/skills/actor-systems.md`, `flows/15b67974/log.md`, `flows/cc4105a6/reports/upstreamKameo.md`, `flows/fb50d4a5/reports/kameoForkUpstream.md`, and `flows/01a02929/reports/kameoForkAndUpstream.md`.

Method: code read `psyche-raw/Vision/actorLibrary.md`, `psyche-raw/Vision/rustComponentArchitecture.md`, `psyche-raw/Vision/nexus.md`, `psyche-raw/Vision/worldModelBeforeCode.md`, and `psyche-raw/Intent/mandatoryTraits.md`.

Method: probe `transcript search -i 'kameo|actor|fork|lifecycle|shutdown' --recent 200`; result: `transcript: command not found`.

## Repository and graph observations

The fork’s current `main` is `3486e4f63ea4e87123476cfbdefeb12403540306`, with lifecycle work rebased onto upstream commit `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`. The current fork-only lifecycle ancestry is `1325f6a` → `da0f64a` → `1980e34` → `8ea1e3f` → `f491b45`; the last two current commits are a rebase repair and documentation marker.

The earlier May 16 objects remain in `refs/jj/keep/`. `8f44e1a`, `4ba9c25`, and `1b918b0` all have `e5d07fd` as parent, so they are parallel first experiments, not a serial ancestry. The original prototype line then continues `1b918b0` → `1329a64` → `44c0552` (with equivalent preserved variants) → `04f6e2a` → `22514f7`. The current `1325f6a`, `da0f64a`, `1980e34`, and `8ea1e3f` are rebased equivalents on `4d2e2d02`, not descendants of those first experiment objects. This is a Git graph observation, not a claim about the author’s mental sequence.

The lifecycle commits have empty commit bodies. Their subjects are the only explicit commit-level descriptions:

- `8f44e1a` (2026-05-16 13:55:59 +02): `actor: make shutdown wait for hook result`.
- `4ba9c25` (2026-05-16 14:02:06 +02): `actor: release state before shutdown completion`.
- `1b918b0` (2026-05-16 14:10:13 +02): `actor: prototype push-based lifecycle phases`.
- `1329a64` / rebased `1325f6a` (2026-05-16 17:48:11 +02): `actor: publish terminal lifecycle outcomes`.
- `44c0552` / rebased `da0f64a` (2026-05-16 22:02:06 +02): `actor: split lifecycle control mailbox`.
- `04f6e2a` / rebased `1980e34` (2026-05-16 22:51:59 +02): `actor: cover lifecycle control edge cases`.
- `22514f7` / rebased `8ea1e3f` (2026-05-16 23:32:47 +02): `actor: gate weak shutdown result helpers`.
- `f491b45` (2026-06-19 10:38:07 +02): `fix lifecycle fork after upstream rebase`.

No subject or body names a production incident, a failing workspace consumer, an upstream issue, or a reason for selecting these exact mechanisms.

## Directly recorded problem sequence

The first two parallel experiments and their tests record the clearest sequence:

1. In `8f44e1a`, `ActorRef::wait_for_shutdown` changes from waiting on `mailbox_sender.closed().await` to waiting on `shutdown_result.wait().await`. `tests/shutdown_order.rs` names `threaded_actor_wait_for_shutdown_waits_for_on_stop`. Its fixture delays `on_stop` and `Drop`, and asserts `on_stop` completed before `wait_for_shutdown` returned. The same test says “short fix should not pretend wait_for_shutdown waits for actor drop.” A second test is named `threaded_actor_wait_for_shutdown_still_does_not_prove_resource_release`; after `wait_for_shutdown`, the listener cannot yet be rebound and the assertion text calls the result “hook-complete, not actor-state-drop.”

2. In the parallel `4ba9c25`, the implementation still changes the wait to `shutdown_result.wait()`, but also changes `PreparedActor::run`, `spawn`, and `spawn_in_thread` so they no longer return `A`. The lifecycle explicitly calls `drop(actor)` before setting `shutdown_result` and before link notification. Its test is named `threaded_actor_wait_for_shutdown_waits_for_actor_drop_and_resource_release`, and asserts the drop witness fired and the listener can be rebound when `wait_for_shutdown` returns.

3. In `1b918b0`, the source comment for `ActorLifecyclePhase` says phase watchers should wait for a pushed phase “rather than inferring lifecycle progress from a side-effect such as a closed mailbox.” The test `lifecycle_phase_waiters_are_push_driven_and_terminal_is_post_release` waits for `StateReleased`, verifies `on_stop` and `Drop`, verifies the listener can rebind, and only then waits for `Terminated`. This is a prototype object, not the current main ancestry.

4. In the original descendant `1329a64` and rebased `1325f6a`, the phase experiment is represented by a terminal outcome. The source publishes `ActorTerminalOutcome` after `on_stop`, `drop(actor)`, awaited link notification, unregister, and compatibility shutdown-result publication. The tests call the public contract `wait_for_shutdown_returns_after_cleanup_drop_and_notifications`; assert `Dropped`/`Stopped`; and assert both stop and drop witnesses plus resource rebind before returning. Other tests cover `NeverAllocated`/`StartupFailed`, `Dropped`/`CleanupFailed`, link delivery of the same outcome, and supervisor replacement only after the prior child’s `Drop` witness.

5. In `44c0552` / `da0f64a`, ordinary messages and lifecycle control are placed in separate channels. The tests `control_signals_do_not_wait_for_bounded_user_mailbox_capacity` and `pending_bounded_user_send_cannot_cross_closed_admission` fill or block ordinary work, send stop or link control, then assert control completes, queued work is not processed, and pending ordinary sends resolve as rejected. The control lane’s implementation uses an unbounded channel; ordinary queued messages carry a generation and are checked against admission and generation before acceptance.

6. In `04f6e2a` / `1980e34`, the source documents that lifecycle/control signals remain accepted while ordinary message admission is closed, that an in-flight ordinary message may finish, and that ordinary queued messages are discarded rather than drained after stop control wins. `blocking_recv_wakes_for_late_control_signal` asserts a late stop wakes a blocking receive. `queued_ask_dropped_by_stop_reports_actor_stopped` asserts a queued ask resolves with `ActorStopped` and is not handled.

7. In `22514f7` / `8ea1e3f`, weak shutdown-result helpers are gated by terminal publication. The source checks `is_terminated()` before exposing the compatibility result. The added test is named `weak_shutdown_result_helpers_wait_for_terminal_lifecycle`; it observes that weak helpers are empty before terminal publication and become available after `wait_for_shutdown` reports `Dropped`/`Stopped`.

These observations support a causal chain from an insufficient mailbox-closure wait, through a hook-complete but state-live wait, to explicit state release, terminal publication, control-plane priority, and helper visibility. They do not identify the event that caused the author to begin the experiments.

## Explicitly recorded motivation

The commit subjects explicitly record these intended changes: wait for the hook result; release state before shutdown completion; prototype pushed lifecycle phases; publish terminal outcomes; split the lifecycle control mailbox; cover lifecycle control edge cases; gate weak shutdown-result helpers; and repair the fork after rebase.

The historical actor-systems report explicitly states a “release before notify” contract and describes resource races such as a redb handle, socket, or file lock held when a supervisor starts a replacement. That report is agent-authored evidence in `reports/PreResetCorpus-2026-06-07/skills/actor-systems.md`, not a commit body or a psyche-approved record. It can explain why the tests use delayed `Drop`, TCP rebind, and supervised replacement as probes, but it cannot establish that this was the original human motivation.

The written psyche explicitly records only the later design context: Kameo is definitely the actor layer in Nexus; the main engine is to be actor-driven and the actor library was forked; actor standards have not been designed; and prior actor work, including the fork, is distrusted. None of those records names the May 16 lifecycle failure or says why the fork was created.

## Code/test-inferred rationale

The tests and implementation make these rationales plausible, without making them explicit historical causes:

- Waiting on mailbox closure was an unreliable terminal fact; a shutdown result made the wait hook-complete, but the delayed-drop test showed that still did not prove state/resource release.
- Dropping actor state before publishing completion or notifying links establishes a synchronization point for resource release and supervisor restart. The TCP listener and replacement-bind tests directly exercise this property.
- A pushed lifecycle signal or terminal cell avoids inferring lifecycle from incidental channel state and makes terminal state observable through one shared cell.
- A physically separate unbounded control lane avoids a bounded ordinary-message queue delaying stop and link-death signals; admission and generation checks reject ordinary messages that race with shutdown.
- Gating weak compatibility helpers avoids exposing a shutdown result before the terminal lifecycle has been published.

The word “rationale” here means an explanation of what the code/tests enforce. It is not evidence that the author stated this explanation when creating the fork.

## Unknown causes and evidence limits

- No commit body, issue reference, pull request reference, code comment, or prior flow record inspected here identifies the originating production failure or decision meeting.
- It is unknown whether any workspace consumer had actually observed a mailbox-closure race, a held-resource restart race, a control-lane deadlock, or premature weak-result visibility. Existing tests prove the scenarios are exercised, not that they came from a live incident.
- It is unknown whether the early `8f44e1a`, `4ba9c25`, and `1b918b0` commits were competing designs, rapid experiments, or parallel snapshots. The graph proves they shared a parent but not the author’s intent.
- It is unknown whether the terminal outcome types, split mailbox, generation counter, and awaited notification were all required by one original contract or accumulated as separate concerns during the May 16 work.
- It is unknown whether `Ejected` was intended for a future state-extraction API; no path producing it was found in the fork source inspected.
- Typed transcript search could not be performed because the documented `transcript` command is unavailable in this workspace. No transcript line can therefore be cited for the fork’s origin.
- The fork’s later written-psyche context settles neither retention nor replacement of the fork; actor standards and the desired lifecycle contract remain open.
