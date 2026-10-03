# Flow contracts repin: ethos-zero 16, signal 7, protos and datom-codec 0.32.2

Subflow of f1c841, 2026-10-03. Everything is on main and pushed. Nothing
deployed. The running nexuses and the nix profile were not touched.

## Versions

| Repository | Before | After | Main commit |
| --- | --- | --- | --- |
| signal-flow | 7.1.0 (5860383) | 8.0.0 | c297d987c549 |
| meta-signal-flow | 11.0.0 (2ac045c) | 12.0.0 | 69f9c146188a |
| flow | 0.18.0 (ae05027) | 0.19.0 | 4f3670ef75fe |

## Pins after

- signal-flow 8.0.0: ethos-zero 0edfc0c3 (16.0.0, build), signal 66e7b153
  (7.0.0), protos 15b41da8 (0.32.2, optional), datom-codec 4dff16b4 (0.32.2,
  optional).
- meta-signal-flow 12.0.0: the same four, plus signal-flow c297d987 (8.0.0).
  The signal-flow build-dependency was never used by build.rs, so it is
  removed.
- flow 0.19.0: signal-flow c297d987, meta-signal-flow 69f9c146, protos
  15b41da8, datom-codec 4dff16b4. sema-engine stays at 516f01fe (0.16.0)
  because the build does not need 0.18.0.

## What changed and why

- **Generated Rust is byte-identical.** Both contracts are Signal roots.
  ethos-zero 16.0.0 changed only Library, Operation and Memory output, so
  each build.rs freshness assertion passes against the committed
  `src/generated/signal.rs` without regenerating. Datom derives sit behind
  `#[cfg_attr(feature = "datom", ...)]`, as before, and that gating is kept.
- **`signal::Contracted` for `Query`** in both contracts, over `ETHOS`. This
  follows the pattern signal-orchestrate 4.0.0 set. One correction to the
  brief: signal-orchestrate 4.0.0 pins ethos-zero cf7dd128 (the 13.x line),
  not 15 or later. It also pins protos and datom-codec at 0.31.0. So it is the
  pattern for signal 7, but not for ethos-zero 16.
- **The `datom` feature no longer enables `signal/datom`.** signal 7.0.0's own
  `datom` feature pins datom-codec and protos at 0.31.0, which would put a
  second codec in the runtime graph. Neither contract holds a signal type.
  0.31.0 remains only as a build-dependency of signal's own build script
  (`cargo tree -i protos@0.31.0`).
- **protos 0.32 `textualize` prints vertically.** One-line inline datom is now
  `Compactable::compact`. The contract tests use it, and so does flow in
  three places: the `flow` and `flow-meta` reply printing, and the Nexus
  rendering a `Message` into a pane (`delivery/body.rs`). Without this change
  a letter would be typed into a pane across several lines.
- **flow-nexus answers `QueueTurnEnd`.** signal-flow 7.1.0 (merged
  vocabulary) had never reached flow. Flow holds no turn-end queue: the hook
  is not installed, and the Flow-or-Transcript choice is unruled (flow 91ea9f
  report `6997eb-open-work.md`). So both dispatch paths answer
  `TurnEndRejected.QueueRefused`, and `ReservesPendingStart` returns `None`.
  A new test covers this, and it was seen failing once.
- **Wire and store.** The archives of `Query` and `Response` changed against
  the deployed 7.0.0 because new variants were appended. The Nexus and both
  CLIs must be rebuilt and restarted together. No stored record holds `Query`
  or `Response`, so the store opens unchanged.
- Each repository's `UPGRADES.md` documents the deploy. signal-flow and
  meta-signal-flow did not have this file until now.

## Tests

| Command | Where | Result |
| --- | --- | --- |
| `cargo test --all-features` | signal-flow | contract 14, presentation_turn_end 3, greeting 2: green |
| `cargo test` | signal-flow | greeting 2 green; the datom suites are cfg'd out |
| `nix flake check` | signal-flow | all checks passed (test, test-datom, fmt) |
| `cargo test --all-features` | meta-signal-flow | contract 9, greeting 3: green |
| `cargo test` | meta-signal-flow | greeting 3: green |
| `nix flake check` | meta-signal-flow | all checks passed |
| `cargo test --workspace` | flow | flow-nexus lib 165, all other suites: green |
| `nix flake check` | flow | 33 checks passed (test, fmt, clippy `-D warnings`, no-free-functions, no-inherent-methods, …) |

New tests:
- `tests/greeting.rs` in both contracts. A greeting built from the contract's
  own source is `Greeted`, and one built from another source is refused with
  this side's digest. In meta-signal-flow, the ordinary contract's greeting
  is refused on the meta contract. These tests were seen failing (failing to
  compile) before the `Contracted` impl existed.
- `a_turn_end_is_refused_while_flow_holds_no_queue` in flow-nexus.

All checks ran for x86_64-linux only. aarch64-linux was omitted by
`nix flake check`.

## Red and open items

- Nothing is red.
- **Flow does not speak the exchange layer.** It is pinned to signal 7.0.0,
  but its sockets still carry the plain `Signal` frame. There is no greeting,
  no `Dispatch`/`Delivery`, and no exchange ids. The `Contracted` impls are
  ready for that work. Orchestrate needed a whole release for the same move
  (0.36.0: GreetingGate, SessionLedger, Feeder). That release is the pattern,
  and it is a design task, not a repin.
- **QueueTurnEnd is refused, not implemented.** It waits on the
  Flow-or-Transcript ruling.
- sema-engine was not moved to 0.18.0 because nothing required it.

## Vision conflicts (for the psyche seat; not redesigned)

Both `ethos/signal.ethos` files were judged against vision-ethos:

1. **Not vertical.** Each section is written on a single line. vision-ethos
   says nothing that has a next layer sits on one line. Reprinting would also
   change `ETHOS`, and with it the contract digest.
2. **Variant payloads are not written in the variant and do not bear its
   name.** Holder types were invented: `Start.StartRequest`,
   `Restart.RestartRequest`, `Stop.StopRequest` (itself `FlowId`),
   `ResolveRecipient.RecipientResolutionRequest`, `List.ListRequest` (`{}`),
   `Observe.ObserveSelection`, `Listed.FlowList`, `Configure.ConfigureRequest`
   (itself `Configuration`), `ConsumeReset.ResetRequest`,
   `Command.CommandRequest`. Rejection payloads are also declared apart:
   `RestartRejected.RestartRejection`, `StopRejected.StopRejection`,
   `ListRejected.ListRejection`, and the rest. The same holds for replies that
   repeat their own name as a separate type: `Started.Started`,
   `Restarted.Restarted`, `Replaced.Replaced`, `Configured.Configured`,
   `BoundExisting.BoundExisting`.
3. **Types used once are declared apart, not inline.** A rough token count
   puts this at about 60 names in signal-flow and about 60 in
   meta-signal-flow. Examples in signal-flow: `LaunchSource`,
   `RememberedFlow`, `TargetReceiptRequest`, `FirstPromptPayload`,
   `AgentObservation`, `TurnEndRejection`. Examples in meta-signal-flow:
   `HarnessProfile`, `CreditSelection`, `Content`, `Sender`, `BodyRefusal`.
   Many are String aliases (`TranscriptInode`, `HerdrTabId`) that could be
   declared in position.
4. **Two roots are missing.** Each repository holds only a Signal file. There
   is no Library for the shared names (`FlowId`, `FlowAspect` and others,
   which meta-signal-flow imports from signal-flow's Signal), no Operation and
   no Memory. The vision's Flow example puts these shared names in a Library.
5. **The name `FlowLifecycle` means two things.** signal-flow's is
   `[ Pending Active Stopped Retired Exited ]`. meta-signal-flow's is
   `[ RegisteredUnconfirmed ]`. They are different types with the same name
   in two contracts that import from each other.
6. **The vision-nexus naming rule is not met.** Under that rule, operations
   are verbs and replies are the past tense. `LaunchStatus` is a noun query.
   `LaunchPending`, `StartAmbiguous` and `TurnEndQueued.TurnEndRequest`
   echo a request type rather than naming the past act.

## Sources

- Repositories under `/git/github.com/LiGoldragon/`. The work was done in
  workspaces at `~/wt/github.com/LiGoldragon/{signal-flow,meta-signal-flow,flow}/contracts-repin-f1c841`.
- ethos-zero `UPGRADES.md` at 0edfc0c (16.0.0, 15.0.0, 14.0.0 entries).
- signal `UPGRADES.md` at 66e7b15 (7.0.0) and `src/accord.rs` (`Contracted`).
- signal-orchestrate 4.0.0 `Cargo.toml` and `src/lib.rs` at 4e68345.
- orchestrate history: b56f264 (0.36.0, exchange layer), bc5cd36 (0.36.1).
- `flows/3ec648/reports/branches-to-main.md` (signal-flow 7.1.0 merge).
- `flows/91ea9f/reports/6997eb-open-work.md` (QueueTurnEnd is declared only;
  Flow-or-Transcript is open).
- Skills: knowledge-ethos, vision-ethos, vision-nexus.
- Orchestrate lock 11629 (FlowContractsRepin), acquired and released.
