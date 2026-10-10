# Kameo consumer and design-pressure map

This report separates direct observations from interpretations and unresolved questions. It maps the current repository estate and records what the written psyche has said; it does not decide actor standards or the fork’s future.

## Direct observations

The workspace has a LiGoldragon Kameo fork at `/git/github.com/LiGoldragon/kameo`, tracking `tqwewe/kameo`. The local fork is version `0.20.0`. Its local `main` is `3486e4f6`; local `upstream/main` is `b4aaee7`; the local merge-base is `4d2e2d02`; and the local refs report 49 commits from fork `main` to `upstream/main`. Earlier reports captured 64, so the count is state/freshness-sensitive.

Twenty-one repository manifests mention Kameo, excluding the fork itself. Eighteen production crates directly declare the LiGoldragon fork: `chroma`, `clavifaber`, `criome`, `ethos-engine`, `harness`, `introspect`, `logos-engine`, `mentci`, `mind`, `persona`, `persona-spirit`, `repository-ledger`, `router`, `sema-storage`, `system`, `terminal`, `terminal-cell`, and `triad-runtime`. `kameo-testing` is the dedicated testbed. `lojix` directly declares crates.io Kameo 0.20. `upgrade` contains only a fork patch entry and has no direct Kameo source usage.

The checked lockfiles resolve ordinary `branch = "main"` fork declarations to `f491b45d7dcb55e5837eddde3d5d7ca8ceaa9f01`. The feature branch used by `persona-spirit` resolves to `22514f7c6900da00703a4a0ef096f21a45c95a99`. `lojix` has both registry Kameo and fork Kameo in its lock graph because `triad-runtime` is also present.

The API shape is Kameo’s data-bearing actor model: `Actor` implementations on domain structs, per-message `Message<T>` implementations, typed `ActorRef`, `Spawn`, `Context`, and `ask`. `DelegatedReply`, `ReplySender`, `WeakActorRef`, `spawn_in_thread`, and graceful stop/wait occur where the runtime needs them.

The three-plane crates (`ethos-engine`, `logos-engine`, `sema-storage`) each implement `SignalPlane`, `NexusPlane`, and `SemaPlane`. `triad-runtime` owns `RequestGate` actors. Persona has eight actors and manual lifecycle. Persona-Spirit has thirteen actors and a supervised `SpiritRoot` tree. Mind and Criome also explicitly supervise child trees. Chroma, Clavifaber, Harness, Introspect, Lojix, Mentci, Repository-Ledger, Router, System, Terminal, and Terminal-Cell each contain data-bearing actor topologies.

The fork-specific terminal outcome is not broadly consumed: most production `wait_for_shutdown()` calls ignore the returned value, no inspected production consumer overrides `on_link_died`, and direct terminal-outcome assertions occur in `kameo-testing` and Persona’s `manager_store` test.

## Fork shape

The fork adds a terminal lifecycle type system (`ActorTerminalOutcome`, `ActorTerminalReason`, `ActorStateAbsence`, `ActorLifecycle`), separate lifecycle-control and ordinary-message mailbox lanes, admission/generation gating, release-before-link-notification shutdown ordering, synchronous link notification, and API changes to `on_link_died`, `wait_for_shutdown`, and spawn/run return values.

Prior fork reports record that upstream v0.22.x added admission gating and several unrelated lifecycle, drain, tracing, and ergonomics changes, but does not provide the fork’s typed terminal outcome, split control lane, or release-before-notify contract. Those upstream comparisons remain prior-report claims; the fork side is directly witnessed here.

## Psyche levels

Intent: `psyche-raw/Intent/mandatoryTraits.md` says:

> Every method call in our Rust code lives under a trait, because
> traits are the comprehension surface — the layer where concepts
> become visible and implementations are constrained to think within
> them.

Vision: `psyche-raw/Vision/actorLibrary.md` says:

> re actors: we are definitely using kameo actors in nexus. I just
> havent designed the standards of use

The same Vision record says:

> I want to dedicate a flow to the actor question. Everything was
> done by previous flows that received little to no guidance on design
> in this respect. Distrust it all, including our fork.

The Nexus Vision says universal Nexus traits are to be designed as “the basic ontology of an actor/dataflow software system,” and the world-model Vision says:

> old code is at most inspiration for that map. (no "never ...")

These words settle that Kameo is the selected actor layer and that actor standards and universal actor/dataflow ontology remain open. They do not settle whether the fork is retained, rebased, returned upstream, or replaced.

## High-level design pressures

1. Kameo is a settled runtime choice for Nexus, while its usage rules are explicitly not designed yet.
2. The current fork has substantial lifecycle machinery, but production code mostly treats it as ordinary Kameo and does not inspect the richer outcome.
3. The estate contains multiple supervision shapes: manual Persona lifecycle, explicit Mind/Criome/Persona-Spirit supervision, and many root-owned shutdown sequences.
4. Branch declarations and lockfiles create a pinning split: mutable `main` declarations currently resolve to `f491b45`, explicit pins use the same commit, and Persona-Spirit uses a separate feature branch.
5. Actor topology must be re-evaluated from a type/trait ontology rather than copied from old code, because the psyche explicitly distrusts prior actor work and calls old code only possible inspiration.
6. The current Nexus skill documents no Kameo identity, actor conventions, supervision, mailbox, or lifecycle contract, despite the repositories relying on them.

## Unknowns

- Whether the 49-versus-64 upstream count reflects stale local refs, different counting, or both.
- Whether `f491b45` is intentionally frozen or merely inherited through stale lockfiles.
- Whether split control lanes, generation tracking, and release-before-notify are load-bearing for any deployed consumer.
- Whether upstream’s lifecycle fixes address the same failures as the fork’s terminal outcome design.
- Whether Persona-Spirit remains in any deployable graph despite the psyche calling it abandoned.
- Whether Lojix’s simultaneous registry/fork Kameo packages are intentional and compatible in every build mode.
- The final actor ontology, actor boundary rules, supervision policy, and standards of use have not been recorded as psyche-approved design.

## Sources

- `flows/fd301d9a/witnesses/kameoConsumers.md`
- `flows/fd301d9a/witnesses/kameoFork.md`
- `flows/fd301d9a/witnesses/psycheActorDirection.md`
- `flows/fd301d9a/vision/actorLibrary.md`
- `flows/fd301d9a/vision/nexusTraits.md`
- `reports/ActorLibraryNexusSkillReview-2026-08-21.md`
- `reports/KameoForkReview-2026-08-21.md`
- `reports/ActorForkAssessment-2026-08-14.md`
- `reports/ActorSystemBoundaries-2026-08-21.md`
- `flows/15b67974/log.md`
- `flows/cff271af/reports/psycheOnSoftwareDesignAndNexus.md`
- `/git/github.com/LiGoldragon/kameo/Cargo.toml`
- `/git/github.com/LiGoldragon/kameo/src/actor/lifecycle.rs`
- `/git/github.com/LiGoldragon/kameo/src/actor.rs`
- `/git/github.com/LiGoldragon/kameo/src/mailbox.rs`
- `/git/github.com/LiGoldragon/Curriculum/skills/nexus.md`
