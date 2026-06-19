# Kameo Lifecycle Fork Benefit POC

## Question

The rebased `LiGoldragon/kameo` lifecycle fork changes shutdown from "the
mailbox is gone" to "the actor reached a terminal lifecycle outcome." The
operator question was where that behavior benefits components enough to adopt or
at least document as an experiment.

## New Behavior Worth Using

| Behavior | Benefit | Best fit |
|---|---|---|
| `wait_for_shutdown() -> ActorTerminalOutcome` | Shutdown can prove why actor state is absent: `Dropped`, `NeverAllocated`, or `Ejected`, plus terminal reason. | Actors owning redb, sockets, child process handles, or filesystem locks. |
| Separate lifecycle/control mailbox | Stop/restart/control signals are not blocked behind a full ordinary message queue. | Router, message delivery, subscription fanout, busy bounded mailboxes. |
| Message admission closes before cleanup finishes | New work cannot enter while shutdown is already committed, but cleanup can still finish. | Durable stores and daemon shutdown paths. |
| Link notifications carry terminal outcome | Supervisors can distinguish killed/panicked/restarted/cleanup-failed peers and whether state dropped. | Component roots and restart policy actors. |
| `is_accepting_messages()` vs `is_terminated()` | Readiness can distinguish "not accepting work" from "fully gone." | Daemon readiness, process supervisors, restart orchestration. |

## Candidate Ranking

| Component | Fit | Reason |
|---|---:|---|
| `persona` `ManagerStore` | High | Uses `spawn_in_thread`, owns an exclusive SEMA/redb path, and already has a resource-release witness. |
| `router` | High later | Uses `spawn_in_thread` and many child shutdown waits; also benefits from lifecycle/control signals under bounded load. It currently has unrelated in-flight changes, so I did not touch it. |
| `mind` | Medium | Store/root shutdown can use terminal outcomes, but the visible resource-release test is less direct than `persona`. |
| `spirit` / `mirror` / `criome` | Medium | Daemon/store actors should eventually benefit, especially around store reopen and authenticated shutdown, but the current best POC is cleaner in `persona`. |

## POC Implemented

Repo: `/git/github.com/LiGoldragon/persona`

Changes:

- `Cargo.toml` now points persona's direct `kameo` dependency at
  `https://github.com/LiGoldragon/kameo.git`, branch `main`.
- `Cargo.lock` pins that fork at `f491b45d` (`fix lifecycle fork after upstream
  rebase`).
- `tests/manager_store.rs` strengthens
  `constraint_manager_store_close_protocol_releases_storage_lock_before_shutdown`:
  after `CloseManagerStore` and `stop_gracefully`, the test now observes
  `wait_for_shutdown()` and asserts:
  - `shutdown.state == ActorStateAbsence::Dropped`
  - `shutdown.reason == ActorTerminalReason::Stopped`
  Only then does it reopen the same manager store path and read the persisted
  event.

This turns the previous implicit statement "waited, then reopen succeeded" into
the explicit lifecycle contract "actor state was dropped for a normal stop, then
the store path reopened."

## Verification

Run under a Nix-provided Rust toolchain:

- `cargo fmt --all -- --check`
- `cargo test --test manager_store constraint_manager_store_close_protocol_releases_storage_lock_before_shutdown -- --exact`
- `cargo test --tests --no-run`

All passed.

## Caveat

The POC revealed a dependency-source split:

- `persona` directly uses fork Kameo.
- `triad-runtime` still uses crates.io Kameo, and reaches persona through
  `message` and `upgrade`.

That is acceptable for this narrow POC because the `ManagerStore` actor is in
persona and uses the fork directly. It is not the final adoption shape. A proper
rollout should repin `triad-runtime` and its consumers so a component graph does
not carry two Kameo packages with the same version but different sources.

## Recommendation

Keep the POC. The lifecycle fork is promising for any actor that owns an
exclusive resource. The next adoption slice should be dependency convergence:
`triad-runtime` first, then router/mind/persona users, with at least one bounded
mailbox control-signal witness in router once its current in-flight work lands.
