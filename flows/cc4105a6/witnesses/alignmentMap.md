# Kameo fork/upstream alignment witness

Observed 2026-08-22 from read-only local clones and the authored psyche records. This witness records observations and the causal comparisons used by `reports/alignmentMap.md`; it does not recommend a merge or migration.

## Repositories and comparison boundary

- Fork: `/git/github.com/LiGoldragon/kameo`, `main` at `3486e4f63ea4e87123476cfbdefeb12403540306`.
- Upstream: `/git/github.com/tqwewe/kameo`, fetched `origin/main` at `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`.
- Merge base: `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92` (2026-06-19).
- Fork-specific lifecycle commits after the base: `1325f6a` (terminal outcomes), `da0f64a` (split lifecycle mailbox), `1980e34` (control edge cases), `8ea1e3f` (weak shutdown helper gating), and `f491b45` (post-rebase adaptation).

The classifications below use these meanings:

- **Equivalent**: same observable guarantee and causal mechanism for the named behavior.
- **Partial overlap**: same concern or some outcome, but a different boundary, ordering, or coverage.
- **Complementary**: addresses another layer and can compose without claiming the same contract.
- **Orthogonal**: no material causal relationship to the named fork mechanism.
- **Conflicting**: one shape permits or requires an outcome the other forbids, loses, or orders differently.

## Fork observations

1. `ActorTerminalOutcome` has `ActorStateAbsence` (`Dropped`, `NeverAllocated`, plus an `Ejected` variant with no observed constructor/use) and `ActorTerminalReason`. The fork stores one terminal outcome in a shared `SetOnce`; `wait_for_shutdown` returns it. The normal and cleanup-failure paths drop actor state, await link notification, unregister, set the compatibility shutdown result, then publish terminal outcome. Startup failure publishes `NeverAllocated`.
2. The fork adds `is_accepting_messages` and `is_terminated` as separate observations. Stop closes ordinary-message admission before `on_stop` finishes; terminal publication is later. All `ActorRef`/`WeakActorRef` clones share the lifecycle cell.
3. The fork splits bounded/unbounded mailbox storage into an ordinary-message lane plus an unbounded lifecycle/control lane. A generation/admission gate rejects ordinary sends after stop begins, including pending bounded sends that later acquire capacity. Control signals can be received despite a full ordinary lane. The fork’s stop documentation/test contract allows the in-flight ordinary handler to finish but discards ordinary messages queued behind the stop control signal.
4. Link notifications carry `ActorTerminalOutcome`; notification is dispatched after actor state is dropped. The fork’s supervision tests require a replacement child to start only after the previous child’s resource has dropped.
5. Weak shutdown-result helpers return `None` until the terminal lifecycle cell is published, even if `on_stop` has already run. After terminal publication they expose the compatibility shutdown result. This is a visibility/order gate, not a new stop reason.
6. The fork’s teardown loop drains incoming signals while waiting for child channels, but does not implement upstream’s later tell-preservation/`on_undelivered`/ask-bounce policy. Its lifecycle test expects a queued ask discarded by stop to report `ActorStopped`.

Evidence: fork commits [1325f6a](https://github.com/LiGoldragon/kameo/commit/1325f6aef7e13996f929d17447ddd2abaa514444), [da0f64a](https://github.com/LiGoldragon/kameo/commit/da0f64af20a4f3002a79a1a5aa2efae416eadfd6), [1980e34](https://github.com/LiGoldragon/kameo/commit/1980e34b5e694b4eb268f24d75fcfa8e527d1472), [8ea1e3f](https://github.com/LiGoldragon/kameo/commit/8ea1e3fab5350ddd86b1bfd18dd3cbd4a0002164), [f491b45](https://github.com/LiGoldragon/kameo/commit/f491b45d7dcb55e5837eddde3d5d7ca8ceaa9f01), and the fork’s [lifecycle tests](https://github.com/LiGoldragon/kameo/blob/3486e4f63ea4e87123476cfbdefeb12403540306/tests/lifecycle_phases.rs).

## Upstream observations at the comparison boundary

- Released upstream after the base is `v0.21.0` through `v0.22.2`; `origin/main` is newer than the latest tag and has merged `syn` 3.0.2 source changes. The current core remains one mailbox channel with an admission flag, not the fork’s two physical lanes.
- `stop_gracefully` stops admission before sending `Signal::Stop`, but its documented contract is to process all messages already queued. The current channel can therefore make control delivery wait on bounded capacity; admission rejection is shared, control-lane priority is not.
- During supervised teardown, upstream preserves tell signals for a predicted restart and requeues them; it bounces asks with `ActorRestarting` for a predicted restart and `ActorNotRunning` for terminal stop. On terminal stop it passes leftover tells to `on_undelivered` and bounces leftover asks as `ActorNotRunning`.
- Upstream still exposes shutdown-result waiters/accessors, but no `ActorTerminalOutcome`. `wait_for_shutdown` waits on mailbox closure; link notification occurs before `on_stop` and before the returned actor state is necessarily dropped. The compatibility result is not the fork’s post-drop/post-notification publication boundary.
- Released remote actors remain a libp2p/Kademlia/request-response core feature. The chitchat/TCP/MessagePack `kameo_remote` work, core-remote removal, TLS/auth, serialized restarts, terminal child ownership, and non-`'static` messages are open proposals/branches, not `main` behavior.

Evidence: upstream [CHANGELOG](https://github.com/tqwewe/kameo/blob/main/CHANGELOG.md), [spawn lifecycle](https://github.com/tqwewe/kameo/blob/main/src/actor/spawn.rs), [actor refs](https://github.com/tqwewe/kameo/blob/main/src/actor/actor_ref.rs), [mailbox](https://github.com/tqwewe/kameo/blob/main/src/mailbox.rs), [links](https://github.com/tqwewe/kameo/blob/main/src/links.rs), [request errors](https://github.com/tqwewe/kameo/blob/main/src/error.rs), and the released [v0.22.2](https://github.com/tqwewe/kameo/releases/tag/v0.22.2).

## Psyche/design authority read

The current written actor-library record says Kameo will be the Nexus actor layer but that “I just havent designed the standards of use”; it also says to distrust prior work, including the fork. Sources read: `flows/fd301d9a/vision/actorLibrary.md`, `flows/fd301d9a/vision/nexusTraits.md`, `psyche-raw/Intent/mandatoryTraits.md`, `psyche-raw/Vision/nexus.md`, `psyche-raw/Vision/rustComponentArchitecture.md`, `psyche-raw/Vision/traitsAsCapabilities.md`, and `psyche-raw/Vision/testTravesties.md`.

The authored design authority establishes: ontology/types before implementation; every Rust method call under a trait because traits and main types are the comprehension surface; Nexus boundaries use typed binary signals and at least two sockets/clients; peers depend on wire-type repositories rather than daemons; tests use external expected values, await the tested event rather than a clock, and avoid shared mutable state. Spirit supplies process/authority discipline, not an actor lifecycle contract. No read psyche record settles the fork’s exact stop ordering, terminal outcome taxonomy, supervision restart contract, or distributed transport.
