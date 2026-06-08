# Operator Handoff — Signal Terminal Contract Migration

## Why this handoff exists

The Codex quota is not enough to finish the full component migration sequence. This report is the takeover surface for Claude/operator to continue without losing the current investigation state.

No code edits were made after claiming `signal-terminal`; the checkout is clean. The work is at a clean analysis point.

## Current lock and repository state

Operator lock during investigation:

`/git/github.com/LiGoldragon/signal-terminal # migrate signal-terminal off signal_channel macro to schema-derived contract`

The lock is released at handoff so the next operator can claim it cleanly.

Primary state at handoff:

- `/home/li/primary` working copy clean.
- Parent commit: `4d5ae3df` on `main`, report 559 from designer.

`signal-terminal` state at handoff:

- Path: `/git/github.com/LiGoldragon/signal-terminal`
- Working copy clean.
- Parent commit: `46c92b58` on `main`, `signal-terminal: document terminal meta socket launch config`.
- No migration edits have been applied yet.

## User requirement being carried

The immediate user requirement is to keep replacing the old architecture, one component at a time, until all non-abandoned components are on the new stack. For this slice, that means:

- `signal_channel!` is deprecated and must be removed from published `signal-*` / `meta-signal-*` contracts.
- Valid migration means schema-derived published contract crates, not merely daemon-local schema mirrors.
- Do not preserve old scaffolding as a compatibility layer unless needed as a temporary compile bridge that is removed in the same migration chain.
- Component repos should be locked one at a time, not all at once.

## What was done immediately before this handoff

The previous completed component slice was `router` consuming the schema-derived `signal-message` contract.

Router commit pushed to `origin/main`:

`f06dc8ed2de6904c05717e019ca2e69a23920a55` — `router: consume schema-derived signal-message contract`

Router verification that passed:

- `cargo fmt --check`
- `cargo test` (67 tests)
- `cargo test --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `nix build .#checks.x86_64-linux.default --max-jobs 0`

## Current target: signal-terminal

Read before editing was completed:

- `signal-terminal/INTENT.md`
- `signal-terminal/AGENTS.md`
- `signal-terminal/ARCHITECTURE.md`
- `signal-terminal/skills.md`
- required workspace skills for contract/Rust/subscription/nix discipline.

Important local facts:

- `Cargo.toml` version is `0.1.0`.
- It still imports `signal_frame::signal_channel` at `src/lib.rs:17`.
- The macro is at `src/lib.rs:1143`.
- Public aliases are at `src/lib.rs:1194`:
  - `TerminalRequest = Operation`
  - `TerminalFrame = Frame`
  - `TerminalFrameBody = FrameBody`
  - `TerminalRequestBuilder = RequestBuilder`
  - `TerminalStreamKind = StreamKind`
- The current `schema/signal-terminal.concept.schema` is only a small sketch and is not a faithful representation of the live contract.

The port must author a real `schema/lib.schema` from the current Rust/macro surface. The concept schema should not be treated as source of truth.

## Live signal-terminal surface

Current request root is `TerminalRequest` via the macro-generated `Operation`.

Operations:

- `TerminalConnection`
- `TerminalInput`
- `TerminalResize`
- `TerminalDetachment`
- `TerminalCapture`
- `RegisterPromptPattern`
- `UnregisterPromptPattern`
- `ListPromptPatterns`
- `AcquireInputGate`
- `ReleaseInputGate`
- `WriteInjection`
- `SubscribeTerminalWorkerLifecycle`
- `TerminalWorkerLifecycleRetraction`
- `ListSessions`
- `ResolveSession`

Current reply root is `TerminalReply`.

Replies:

- `TerminalReady`
- `TerminalInputAccepted`
- `TranscriptDelta`
- `TerminalResized`
- `TerminalCaptured`
- `TerminalDetached`
- `TerminalExited`
- `TerminalRejected`
- `PromptPatternRegistered`
- `PromptPatternUnregistered`
- `PromptPatternList`
- `GateAcquired`
- `GateBusy`
- `GateReleased`
- `InjectionAck`
- `InjectionRejected`
- `TerminalWorkerLifecycleSnapshot`
- `SubscriptionRetracted`
- `SessionList`
- `SessionResolved`

Current event root is `TerminalEvent`.

Events:

- `TerminalWorkerLifecycleEvent`

Current stream:

- `TerminalWorkerLifecycleStream`
- token: `TerminalWorkerLifecycleToken`
- opened: `TerminalWorkerLifecycleSnapshot`
- event: `TerminalWorkerLifecycleEvent`
- close: `TerminalWorkerLifecycleRetraction`

Important helper methods:

- `TerminalRequest::operation_kind()` at `src/lib.rs:1200`.
- `impl From<TerminalWorkerLifecycleEvent> for TerminalEvent` at `src/lib.rs:1228`.
- `impl From<Payload> for TerminalRequest` for each request payload at `src/lib.rs:1236`.
- `TerminalDaemonConfiguration::{from_rkyv_bytes,to_rkyv_bytes}` at `src/lib.rs:1352`.

## Generator capability confirmed by subagent

`schema-rust-next` can emit a published single-stream wire contract, but the schema must use the newer stream model:

- A namespace stream declaration:
  `TerminalWorkerLifecycleStream (Stream { token TerminalWorkerLifecycleToken opened TerminalWorkerLifecycleSnapshot event TerminalEvent close TerminalWorkerLifecycleToken })`
- An input variant with a stream relation:
  `(SubscribeTerminalWorkerLifecycle SubscribeTerminalWorkerLifecycle opens TerminalWorkerLifecycleStream)`
- An output variant literally named `Event` whose payload is the stream event type:
  `(Event TerminalEvent)`
- Event enum variants marked as belonging to the stream:
  `TerminalEvent [(TerminalWorkerLifecycleEvent TerminalWorkerLifecycleEvent belongs TerminalWorkerLifecycleStream)]`

The narrow generator condition is in `schema-rust-next/src/lib.rs`:

- `streaming_event_payload` uses `streams.first()`.
- It requires an `Output` variant named `Event`.
- It requires that variant payload to exactly equal the stream event type.

So `signal-terminal` can migrate now because it has one stream. If a later contract needs multiple independent stream event roots, schema-rust-next needs a generator extension first.

## Schema shape to implement

Create the same build layout used by `signal-message`:

- `build.rs` using `schema_rust_next::build::ContractCrateBuild`.
- `schema/lib.schema` as the source contract.
- `src/schema/mod.rs` and generated `src/schema/lib.rs`.
- `src/lib.rs` reduced to re-export generated schema nouns plus hand-written inherent methods that are genuinely contract-local.
- `Cargo.toml` build dependency on `schema-rust-next`, `links = "signal-terminal"`, and no `signal_channel!` dependency path.

Use `signal-message` as the pattern:

- `/git/github.com/LiGoldragon/signal-message/build.rs`
- `/git/github.com/LiGoldragon/signal-message/schema/lib.schema`
- `/git/github.com/LiGoldragon/signal-message/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-message/tests/dependency_boundary.rs`

Recommended `signal-terminal` schema root naming:

- `Input` root for the 15 request variants.
- `Output` root for the existing replies plus `(Event TerminalEvent)`.
- Namespace types for all existing payloads.
- `TerminalOperationKind` remains a contract-local enum.
- `TerminalDaemonConfiguration` remains in this contract for now because downstream `terminal`/`persona` use it, but its helper types should be schema-local.

Important residue to remove from this contract:

- `signal_channel!`
- direct `signal-engine-management` dependency if possible.
- direct `signal-persona-origin` dependency if possible.

Those two helper dependencies are old shared-helper residue. `signal-message` already localizes `WirePath`, `SocketMode`, `UnixUserIdentifier`, `OwnerIdentity`, etc. `signal-terminal` should do the same unless an immediate compile blocker is discovered.

## Tests that pin behavior

Main tests to port rather than delete:

- `tests/round_trip.rs`
  - request/reply/event frame round trips.
  - operation head order.
  - stream open/close mapping.
  - request/reply payload `From` lifts.
  - daemon config rkyv helpers.
- `tests/canonical_examples.rs`
  - canonical NOTA examples.
- `tests/introspection.rs`
  - introspection records that contain `TerminalReply`.

Likely needed test changes:

- `TerminalRequest` becomes generated `Input` unless a short alias is intentionally retained during the same consumer migration.
- `TerminalReply` becomes generated `Output`, but terminal streaming needs an `Output::Event(TerminalEvent)` variant for `schema-rust-next` streaming support. That is a real target-shape change from the old macro, where event was separate from reply root.
- `TerminalEvent` remains a generated event enum.
- Generated `Frame` becomes `signal_frame::StreamingFrame<Input, Output, TerminalEvent>` when stream metadata is present.

## Downstream consumer impact

Subagent audit found the direct downstream breakpoints.

Recommended order after `signal-terminal`:

1. `meta-signal-terminal`
2. `terminal`
3. `terminal-cell`
4. `harness`
5. `persona`

Important files in `terminal`:

- `terminal/src/daemon.rs`
- `terminal/src/supervisor.rs`
- `terminal/src/contract.rs`
- `terminal/src/signal_control.rs`
- `terminal/src/signal_cli.rs`
- `terminal/src/config.rs`
- `terminal/src/pty.rs`

Important files in `terminal-cell`:

- `terminal-cell/src/client.rs`
- `terminal-cell/src/socket.rs`
- `terminal-cell/src/bin/terminal-cell-daemon.rs`
- `terminal-cell/tests/daemon_witness.rs`

Important files in `harness`:

- `harness/src/terminal.rs`
- `harness/tests/smoke.rs`
- `harness/tests/daemon.rs`
- `harness/tests/message_router_harness_e2e.rs`
- `harness/tests/actor_runtime_truth.rs`

Important files in `persona`:

- `persona/src/engine_event.rs`
- `persona/src/direct_process.rs`
- `persona/tests/direct_process.rs`

## Recommended immediate next commands

In `signal-terminal`, inspect before editing:

```sh
sed -n '1,220p' src/lib.rs
sed -n '1120,1385p' src/lib.rs
sed -n '1,260p' schema/signal-terminal.concept.schema
rg -n "signal_channel!|TerminalRequest|TerminalReply|TerminalEvent|TerminalFrame|TerminalFrameBody|TerminalRequestBuilder|TerminalWorkerLifecycleStream|signal_engine_management|signal_persona_origin" src tests schema Cargo.toml
```

Copy the contract-build pattern:

```sh
sed -n '1,220p' /git/github.com/LiGoldragon/signal-message/build.rs
sed -n '1,220p' /git/github.com/LiGoldragon/signal-message/schema/lib.schema
sed -n '1,220p' /git/github.com/LiGoldragon/signal-message/src/lib.rs
```

Check generator stream syntax:

```sh
sed -n '1,90p' /git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/daemon-stream.schema
sed -n '1,80p' /git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/big-schemas/triad-reactive-large.schema
```

## Verification target for signal-terminal

After edits:

```sh
SIGNAL_TERMINAL_UPDATE_SCHEMA_ARTIFACTS=1 cargo build
cargo fmt --check
cargo test
cargo test --all-features
cargo clippy --all-targets --all-features -- -D warnings
nix build .#checks.x86_64-linux.default --max-jobs 0
```

If `nix build` is unavailable or too slow, report that explicitly, but do not call a migration finished without at least cargo test/clippy and artifact freshness.

## Commit/push discipline

For code repos under `/git`, operator owns `main`.

Use the repo's VCS state. This repo is currently in a detached git view through jj. Follow local repo discipline if jj is configured; otherwise use the existing repo flow carefully. Do not path-scope commits. Do not leave the current operator lock stale.

For primary:

```sh
jj commit -m 'operator 340: handoff signal-terminal contract migration'
jj bookmark set main -r @-
jj git push --bookmark main
```

## Current open risk

The largest risk is trying to preserve old `TerminalRequest` / `TerminalReply` aliases as a compatibility shell and calling that migrated. That would violate the user's latest architecture direction. If aliases are used temporarily to keep downstream compiling, they should be treated as a short-lived bridge and removed as downstream repos migrate.

The better migration shape is to move consumers to generated `Input` / `Output` and schema-derived `Frame` directly.

## Takeover recommendation

Do `signal-terminal` first and finish it to green. Then release its lock and immediately claim `meta-signal-terminal`. Only after both contract crates are schema-derived should the `terminal` daemon be migrated, because `terminal` consumes both ordinary and meta terminal contracts.
