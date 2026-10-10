# Kameo fork

Method: probe `git -C /git/github.com/LiGoldragon/kameo remote -v; git -C /git/github.com/LiGoldragon/kameo rev-list --count main..upstream/main; git -C /git/github.com/LiGoldragon/kameo merge-base main upstream/main; git -C /git/github.com/LiGoldragon/kameo show -s --format=... main upstream/main`.

Method: code read `/git/github.com/LiGoldragon/kameo/Cargo.toml`, `src/actor/lifecycle.rs`, `src/actor.rs`, and `src/mailbox.rs`.

Method: code read `reports/KameoForkReview-2026-08-21.md`, `reports/ActorForkAssessment-2026-08-14.md`, and `reports/ActorLibraryNexusSkillReview-2026-08-21.md`.

## Local repository observations

- Checkout: `/git/github.com/LiGoldragon/kameo`.
- Remotes: `origin = git@github.com:LiGoldragon/kameo.git`; `upstream = git@github.com:tqwewe/kameo.git`.
- Local fork `main`: commit `3486e4f63ea4e87123476cfbdefeb12403540306`, dated 2026-06-19, subject `docs: mark Protos estate status`.
- Local merge-base with `upstream/main`: `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`.
- Local `upstream/main`: `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`, dated 2026-07-21, subject `chore(deps): update syn requirement from 2.0.52 to 3.0.2 (#383)`.
- Local `git rev-list --count main..upstream/main` returned `49`. The earlier Kameo fork reports record `64` as of their capture; this is a freshness/count discrepancy, not a resolved design fact.
- The fork package is version `0.20.0`, Rust `1.88.0`, with default features `macros` and `tracing`; optional `remote`, `otel`, `metrics`, and `hotpath` are present in the fork manifest.

## Fork feature observations

The fork’s added lifecycle module defines `ActorStateAbsence`, `ActorTerminalReason`, `ActorTerminalOutcome`, and an `ActorLifecycle` backed by `tokio::sync::SetOnce`.

The fork’s `ActorTerminalReason` includes `StartupFailed`, `Stopped`, `SupervisorRestart`, `Killed`, `Panicked`, `LinkDied`, `CleanupFailed`, and feature-gated `PeerDisconnected`.

The fork’s `Actor::on_link_died` accepts an `ActorTerminalOutcome` in addition to the older `ActorStopReason`. `wait_for_shutdown()` waits for and returns the terminal outcome. The fork’s spawn path drops actor state before notifying links, and link notification is awaited rather than fire-and-forget. Spawn/run no longer return the actor value.

The fork’s mailbox creates separate ordinary-message and lifecycle-control channels, uses an admission `AtomicBool`, and carries a message-generation counter. Control signals are not placed behind the bounded ordinary-message lane.

The prior fork reports observe upstream overlap on admission gating in v0.22.0, while reporting no upstream equivalent for typed terminal outcomes, split control lanes, or release-before-notify ordering. Those are claims in prior reports; the local source read directly verifies the fork side only.

## Consumer-coupling observations

- Production consumers call `wait_for_shutdown()` extensively, but almost all discard its result.
- No production consumer in the inspected set supplies a custom `on_link_died`; the Kameo testbed does, and records terminal outcomes.
- Persona’s `tests/manager_store.rs` directly asserts `ActorStateAbsence::Dropped` and `ActorTerminalReason::Stopped` after graceful shutdown.
- The strongest direct exercise of the fork-specific API is therefore in `kameo-testing` and Persona’s test suite, while the wider estate depends on the changed lifecycle implementation through ordinary stop/wait behavior.
