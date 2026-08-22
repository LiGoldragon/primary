# Kameo fork and upstream progress

As of 2026-08-22, our Kameo fork and upstream are not two versions of the same lifecycle design. Upstream has advanced substantially in message fate, restart accounting, supervision, diagnostics, and ergonomics. The fork still uniquely encodes terminal-state publication, state-absence evidence, a separate lifecycle-control lane, and deterministic link-notification ordering. A routine rebase would therefore combine competing lifecycle models before the desired contract has been designed.

## High-level view

```text
upstream v0.20.0
       |
       +-- upstream work through merge base 4d2e2d02 (2026-06-19)
             |\
             | +-- our fork: 6 commits -> 3486e4f6 (package still 0.20.0)
             |      explicit terminal outcomes
             |      split message/control mailbox
             |      state dropped before awaited link notification
             |
             +---- upstream: 49 commits -> b4aaee79
                    releases v0.21.0 ... v0.22.2
                    restart-aware drain and ask errors
                    on_undelivered, deadlock/panic fixes, console/tracing
```

The earlier `64`-commit figure and today's `49`-commit figure use different starting points: `64` was counted from tag `v0.20.0`; `49` is counted from the later merge base. They are not conflicting freshness observations.

## Repository state

| Boundary | Observed state |
|---|---|
| Fork | `LiGoldragon/kameo`, `main` at `3486e4f63e...`; six fork-only commits |
| Upstream | `tqwewe/kameo`, `main` at `b4aaee797c...`; 49 upstream-only commits |
| Common ancestor | `4d2e2d02cc...`, 2026-06-19 |
| Fork release identity | no GitHub releases; manifest and latest root tag remain `0.20.0`; fork head is untagged |
| Upstream release identity | latest release `v0.22.2`, published 2026-07-18; current `main` is a 2026-07-21 `syn` update |

The fork's first four unique commits are its lifecycle design. `f491b45d` repaired that design after the upstream rebase; `3486e4f6` is a later documentation-only commit.

## The two lifecycle contracts

### What the fork makes explicit

- `ActorTerminalOutcome`, `ActorTerminalReason`, and `ActorStateAbsence`, published through a lifecycle `SetOnce` cell.
- `wait_for_shutdown() -> ActorTerminalOutcome`, rather than using mailbox closure as the only completion fact.
- Startup and cleanup failures as terminal categories, and the terminal outcome supplied to link-death and restart decisions.
- Actor state is dropped before death notification; link notification is awaited rather than detached.
- Ordinary messages and lifecycle control use separate physical channels. Admission closes and a generation changes when shutdown starts; stale messages are discarded while control remains deliverable.
- Spawn/run consume the actor state rather than returning the actor value after shutdown.

These are externally meaningful semantics plus one concrete mechanism. The two-channel mailbox and generation counter are a way to achieve control priority and stale-message rejection; they are not themselves yet a psyche-approved design requirement.

### What upstream added after the fork point

Released upstream now provides:

- lifecycle deadlock fixes and panic-safe shutdown;
- preservation of tell messages when a restart is expected;
- explicit `ActorRestarting` versus `ActorNotRunning` results for pending asks during drain;
- `on_undelivered` for tells that cannot survive terminal shutdown;
- rejection of new messages after `stop_gracefully` begins;
- shared restart-intensity state, three restart policies, and three supervision strategies;
- per-actor reply timeout, `Context::pipe`/`pipe_with`, cheaper `ActorRef` cloning, richer `SendError`, `FutureActor`, console/TUI, and tracing improvements.

Upstream still has one signal channel, `wait_for_shutdown() -> ()`, no terminal-outcome/state-absence type, and detached parent/sibling link notification. Its admission gate overlaps with only part of the fork's mailbox design.

Current open work is not usable contract: PRs propose serialized supervised restarts, release of terminal child ownership, relaxed message bounds, a `0.22.3` release, and replacement of core libp2p remote actors with a separate chitchat/TCP `kameo_remote` crate plus optional mTLS. None of those proposals is merged into the observed `main` or released.

## Consumer reality

Eighteen production crates directly declare the fork: thirteen track `branch = "main"`, four pin `f491b45d`, and `persona-spirit` names `persona-lifecycle-terminal-outcome`. `kameo-testing` is the dedicated testbed. `upgrade` has only a patch entry. `lojix` directly declares registry Kameo 0.20 while its graph also contains the fork through `triad-runtime`.

The checked branch-based lockfiles largely resolve to `f491b45d`; their source behavior matches fork `main` because the only later fork commit is documentation, but the manifests are mutable while the locks are snapshots. The Persona-Spirit branch is now absent from the forge, although its locked commit remains addressable.

Most production shutdown calls ignore the fork's returned terminal outcome. No inspected production consumer overrides `on_link_died`; direct assertions of terminal outcomes were found in `kameo-testing` and one Persona test. This proves light direct API consumption, not that the semantics are unnecessary: control priority, state release, and notification ordering can matter without callers pattern-matching the outcome.

## Design assessment

The fork should not be preserved because it exists, and upstream should not be adopted because it is newer. The right sequence is:

1. Design the observable actor lifecycle contract from first principles: startup completion, message admission, queued tell fate, pending ask fate, restart identity, terminal reason, actor-state absence, link notification, and supervisor observation order.
2. Decide which observations are guaranteed and which are deliberately unavailable. In particular, decide whether a supervisor must know that child state has been dropped before receiving link death, and whether lifecycle control must be able to bypass a saturated ordinary mailbox.
3. Map that contract onto current upstream. Keep upstream's released drain/error/supervision work where it fits; add only the missing semantics required by the contract.
4. Then choose the implementation home: an upstream contribution, a smaller forward fork, or—only if Kameo cannot express the contract—a deliberate deeper fork.

The likely best base is current released upstream because it already solves several 0.20-era lifecycle problems and carries the maintained ecosystem. That is a design hypothesis, not a ruling: it is disconfirmed if the desired contract fundamentally conflicts with upstream's single-channel, mailbox-closure, or notification-order model.

## Written-psyche boundary

The written psyche settles two things and leaves the decisive work open:

> I want to dedicate a flow to the actor question. Everything was done by previous flows that received little to no guidance on design in this respect. Distrust it all, including our fork.

> re actors: we are definitely using kameo actors in nexus. I just havent designed the standards of use

Together with the mandatory-traits Intent and the Nexus ontology Vision, this means Kameo is the selected actor layer, while lifecycle, supervision, actor boundaries, and standards of use must be designed rather than inherited from either code line.

## Unknowns

- Which incident or invariant originally made terminal outcomes, state absence, split control, and synchronous notification necessary.
- Whether any deployed workload depends on control bypass under mailbox saturation or on release-before-notify ordering.
- Whether upstream's deadlock/restart changes remove part of the original need.
- Whether the deleted Persona-Spirit branch and Lojix's dual Kameo graph still resolve in clean builds; no Cargo-resolution probe was run.
- Which open upstream lifecycle changes will merge and what their final API will be.

## Research-state note

The fork checkout was inspected without ref or source changes. The upstream-research subflow ran `git fetch --tags --prune origin` in `/git/github.com/tqwewe/kameo`, refreshing that clone's remote-tracking refs and tags; no source checkout, fork ref, configuration, or live service was changed.

## Sources

- `flows/fb50d4a5/reports/kameoForkUpstream.md`
- `flows/fb50d4a5/witnesses/repositoryRelationship.md`
- `flows/fb50d4a5/witnesses/forkApiArchitecture.md`
- `flows/fb50d4a5/witnesses/consumerPins.md`
- `flows/fb50d4a5/witnesses/upstreamIdentity.md`
- `flows/fb50d4a5/witnesses/releaseTags.md`
- `flows/cc4105a6/reports/upstreamKameo.md`
- `flows/cc4105a6/witnesses/upstreamState.md`
- `flows/fd301d9a/reports/kameoContext.md`
- `flows/fd301d9a/witnesses/kameoConsumers.md`
- `flows/fd301d9a/witnesses/psycheActorDirection.md`
- `psyche-raw/Vision/actorLibrary.md`
- `psyche-raw/Intent/mandatoryTraits.md`
- `psyche-raw/Vision/nexus.md`
- https://github.com/tqwewe/kameo/releases/tag/v0.22.2
- https://github.com/tqwewe/kameo/compare/4d2e2d02cc1ba59f05123d79f73eb47dd819ef92...main
- https://github.com/LiGoldragon/kameo/compare/3486e4f63ea4e87123476cfbdefeb12403540306...b4aaee797cc3fd12e8194db406d9d73a6bc021ce
- https://github.com/tqwewe/kameo/pull/373
- https://github.com/tqwewe/kameo/pull/376
- https://github.com/tqwewe/kameo/pull/380
- https://github.com/tqwewe/kameo/pull/387
- https://github.com/tqwewe/kameo/pull/394
- https://github.com/tqwewe/kameo/pull/396
