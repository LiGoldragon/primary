# Signal / Sema / Spirit Current Handoff

## Purpose

This report is the current operator handoff for the 2026-05-20 signal /
sema / executor redesign and the `persona-spirit` pilot. It tells later
agents which shape is current, which older reports are stale, and what can be
built next without reopening settled questions.

## Current Architecture

The current model has three layers:

```text
Contract Operation
  External wire vocabulary. Owned by signal-<component> and
  owner-signal-<component> contract crates.

Component Command
  Internal executable vocabulary. Owned by the daemon/component.

Sema Classification
  Universal payloadless observation vocabulary. Owned by signal-sema.
```

Flow:

```text
NOTA request
  -> CLI decodes one contract Operation
  -> signal-frame request frame
  -> daemon socket
  -> daemon lowers Operation to Component Command
  -> component executor commits Command atomically
  -> Component Effect projects to SemaObservation
  -> signal-frame reply frame
  -> CLI prints NOTA reply
```

Sema is **not** executable. Sema names cross-component observation classes:
`SemaOperation + SemaOutcome = SemaObservation`.

## Current Repo Truth

| Repo | Current truth |
|---|---|
| `signal-frame` | Wire kernel: frames, requests, replies, streams, observable macro, `BatchErrorClassification`, batch-abort metadata. No Sema verbs. |
| `signal-sema` | Payloadless `SemaOperation`, payloadless `SemaOutcome`, `SemaObservation`, pattern primitives, slot/revision identity values. |
| `signal-executor` | Shared library composing `Lowering`, `CommandExecutor`, `OperationPlan`, `BatchPlan`, observer publication, and reply shaping. Executes component-local commands, never Sema operations. |
| `signal-persona-spirit` | Ordinary spirit contract. Already on `signal-frame`; uses contract-local verbs and `OperationReceived` / `EffectEmitted`. |
| `owner-signal-persona-spirit` | Owner spirit contract. Now on `signal-frame`; uses contract-local owner verbs `Start`, `Drain`, `Reload`, `Register`, and `Retire`. |
| `persona-spirit` | Runtime daemon + thin `spirit` CLI. Has Kameo actor tree, ordinary/owner sockets, sema-engine-backed record store, provisional classifier, local command/effect projection to `SemaObservation`, migrated owner-signal handling, and constraint tests. |

## Commits To Know

| Repo | Commit | What landed |
|---|---|---|
| `signal-sema` | `f4d3fe51` | `SemaOutcome`, `ToSemaOutcome`, and `SemaObservation` with tests. |
| `signal-frame` | `68891f60` | `BatchErrorClassification` moved into the frame layer. |
| `signal-frame` | `fb53a6be` | Removed speculative `CommitStatus::Partial`; atomic batches expose only `NotCommitted` or `Unknown`. |
| `signal-executor` | `66b5ee48` | Executor uses frame-owned `BatchErrorClassification`. |
| `signal-executor` | `47961d12` | Bumped to the `signal-frame` revision without `Partial`. |
| `signal-persona-spirit` | `a1909872` | Observable event pair renamed to `OperationReceived` / `EffectEmitted`. |
| `signal-persona-spirit` | `2e7a69a0` | Bumped to the `signal-frame` revision without `Partial`. |
| `owner-signal-persona-spirit` | `10ff8731` | Migrated owner contract to `signal-frame` and contract-local owner verbs. |
| `persona-spirit` | `556bafcc` | `spirit` CLI became thin daemon client shape. |
| `persona-spirit` | `951603c3` | Explicit no-change command witnesses for valid-but-unimplemented observer requests. |
| `persona-spirit` | `0f0a82be` | Bumped to current frame/spirit contract pins without `Partial`. |
| `persona-spirit` | `97f4a138` | Consumes migrated owner contract; owner socket no longer uses old `signal-core` request wrappers. |

## Batch Failure Contract

`execute_atomic_batch` means all-or-nothing.

Current failed commit status:

```rust
pub enum CommitStatus {
    NotCommitted,
    Unknown,
}
```

`Partial` is intentionally absent. It contradicts the atomic batch contract.
If a future non-atomic executor lands, adding `Partial` back will be a
deliberate compile-error fan-out with real semantics.

Engine failures are accepted batch-abort replies:

```text
Reply::Accepted {
  outcome: BatchAborted { reason, retry, commit },
  per_operation: [Invalidated, ...]
}
```

They are not `Reply::Rejected`, because the frame was accepted and failure
happened after execution planning began.

## Observer Contract

Canonical event names:

```text
OperationReceived
EffectEmitted
```

`EffectEmitted` carries `SemaObservation` for generic observation in the
current spirit contract. Do not reintroduce `SemaEffect` or
`SemaEffectEmitted`.

For component internals, the executor's raw effect fact is:

```rust
CommandEffect<Command, ComponentEffect>
```

Generic observation comes from:

```rust
command_effect.sema_observation()
```

where:

```rust
Command: ToSemaOperation
ComponentEffect: ToSemaOutcome
```

## Spirit Runtime State

Implemented:

- `spirit` CLI accepts exactly one raw NOTA argument or one path to a NOTA
  request file.
- The CLI requires a daemon socket and does not open the store or run the
  actor tree in-process.
- `persona-spirit-daemon` accepts one NOTA daemon configuration record.
- The daemon binds an ordinary `signal-persona-spirit` socket and an owner
  `owner-signal-persona-spirit` socket.
- Ordinary and owner sockets reject each other's frame families.
- Raw `State` statements route through `ClassifierPlane` before storage.
- `Record` stores one top-level `Entry` and mints `RecordIdentifier`.
- `Observe(Records)` supports summary and provenance modes.
- `Observe(State)` and `Observe(QuestionsPending)` use `StatePlane`.
- `Watch` / `Unwatch` for state and record streams have typed open/close
  acknowledgements.
- `OwnerPlane` handles current owner lifecycle and identity requests.
- `PolicyPlane` parses and reloads bootstrap policy.
- Owner socket handling consumes `owner-signal-persona-spirit` through
  `signal-frame`, matching the ordinary socket frame model.
- Local `Command` / `Effect` values project to payloadless
  `SemaObservation` through tested traits.

Not implemented:

- LLM-backed classification.
- Subscription event delivery after stream open.
- Owner-Mutate forwarding to `persona-mind`.
- Import/cutover from `intent/*.nota`.
- Filesystem intent projection.

## Spirit CLI Cutover Reality

The `spirit` CLI is not yet a full replacement for manual
`intent/*.nota` edits.

It can already be used for typed capture/query experiments when:

- `persona-spirit-daemon` is running,
- `PERSONA_SPIRIT_SOCKET` points to its ordinary socket,
- the caller supplies a complete ordinary contract request.

It is not yet the canonical intent substrate because existing intent files
have not been imported, subscription delivery is not live, and spirit-to-mind
forwarding is absent.

## Stale Or Superseded Surfaces

Treat the following as stale when they conflict with current code:

| Surface | Stale point |
|---|---|
| `reports/designer/248-three-layer-changes-for-operators.md` | Its example still lists `CommitStatus::Partial`; the current code and report 144 removed it. |
| `reports/designer/246-v4-bundled-fix-deep-design-with-examples.md` | Same `Partial` example is stale; use the current frame code for the enum. |
| `signal-persona-orchestrate` | Still has `SemaEffectObserved` / `SemaEffectEmitted` wording. Migrate when that contract is next touched. |
| `signal-persona-introspect/ARCHITECTURE.md` | Still mentions `SemaEffectEmitted`. Migrate when introspect is next touched. |
| `signal-persona-orchestrate` and `signal-persona-introspect` | Some text still reflects the pre-`EffectEmitted` vocabulary. Treat current `signal-frame` / `signal-sema` / `signal-persona-spirit` code as newer truth. |

## Safe Next Work

Highest-signal spirit tasks:

1. Keep the CLI thin: one NOTA input, one signal-frame exchange, one NOTA
   reply.
2. Add the first explicit daemon-level test that runs `persona-spirit-daemon`
   and `spirit` as binaries, not only through in-process clients.
3. Decide whether subscription event delivery or spirit-to-mind forwarding is
   the next pilot slice.

Do not start filesystem intent-log replacement until the import/cutover
semantics are explicit.

## Current Open Questions

These still need psyche/designer clarification before becoming durable
implementation constraints:

1. Should agents start using `spirit '(Record ...)'` as soon as the daemon is
   available, or should there be an explicit dual-write/import window for
   existing `intent/*.nota` files?
2. Must `Tap` / `Untap` observer operations be live before `spirit` becomes
   the replacement for intent logging, or is the current typed `NoChange`
   placeholder acceptable until introspection integration?
3. Should `signal-persona-orchestrate` migrate immediately away from
   `SemaEffectObserved`, or wait for the orchestrate contract redesign?
4. Is `EffectEmitted` mandatory for every Persona observable contract, or is
   it the default generated name when a contract has no more specific
   observable event vocabulary?

## Verification Baseline

The last verified lower-layer slice passed:

```text
signal-frame: cargo test --locked; nix flake check -L --max-jobs 0
signal-executor: cargo test --locked; nix flake check -L --max-jobs 0
signal-persona-spirit: cargo test --locked; nix flake check -L --max-jobs 0
owner-signal-persona-spirit: cargo test --locked; nix flake check -L --max-jobs 0
persona-spirit: cargo test --locked; nix flake check -L --max-jobs 0
```

Use `--max-jobs 0` on Nix checks so the remote builder is used, and
`CARGO_BUILD_JOBS=2` on cargo commands.
