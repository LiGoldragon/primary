# Orca agent communication and model-context semantics

Observed revision: `80b2a0237729af8c3c57c39cd94e087b698058b9` (`origin/main` and local `main` observed at this revision on 2026-08-22). Repository: `https://github.com/stablyai/orca`.

## Bottom line

Orca's ordinary agent-to-agent message is durable structured inbox mail, not direct model-context injection. `orca orchestration send` writes a SQLite `messages` row, notifies the recipient mailbox, and either wakes an existing `check --wait` call or, only when a recognized recipient agent is already at a live idle prompt, types a short pointer into that agent's PTY: `You have N orchestration message(s). Run \`orca orchestration check\`.` The pointer is submitted with Enter. The message body is not typed into the recipient PTY; the recipient's next `orca orchestration check` retrieves it.

The model-role conclusion is therefore split:

- For ordinary mail, Orca itself creates no system/developer/tool transcript item. The pointer is terminal input intended to start a new agent turn; the body is returned by an agent-invoked CLI/RPC call and is therefore observed by Orca only as command output. The provider's internal role assignment is outside this repository.
- For `dispatch --inject`, Orca directly bracketed-pastes a task preamble plus spec into the agent TUI and submits it. At Orca's boundary this is prompt-like terminal input intended as a new turn, not a system/developer API call. The source does not prove the provider's transcript role.

## Observations

### 1. Addressing and send RPC

The CLI resolves `--from` from the explicit flag/environment/current terminal and calls `orchestration.send` (`src/cli/handlers/orchestration.ts:563-611`). Local CLI transport is newline-delimited JSON over the runtime metadata's Unix socket or named pipe (`src/cli/runtime/client.ts:69-132`; `src/cli/runtime/transport.ts:9-196`; server `src/main/runtime/rpc/unix-socket-transport.ts:1-3,59-77,132-220`). Remote CLI calls use the pairing transport in `RuntimeClient.call`, but the same RPC method and parameters (`client.ts:97-120`).

`resolveMessageRun` derives a Dispatch from a payload `dispatchId` or `dispatch:<id>`, derives a Run from `--run`, `run:<id>`, Dispatch ownership, or the sender's pane (`src/main/runtime/rpc/methods/orchestration.ts:320-383`). A bare recipient handle is canonicalized to a Run or Dispatch mailbox by `resolveBareOrchestrationRecipient` (`src/main/runtime/rpc/methods/orchestration-recipient-routing.ts:29-90`). Groups fan out one row per resolved mailbox (`orchestration.ts:804-894`).

For a normal point-to-point message, `orchestration.send` inserts the row with body, type, priority, thread, payload, sender pane, and Run (`orchestration.ts:682-706`) and only then calls `runtime.notifyMessageArrived` (`:783-801`).

### 2. Durable state

The runtime lazily opens `<Electron userData>/orchestration.db` and schedules restored undelivered mail (`src/main/runtime/orca-runtime.ts:4232-4252`). The `messages` table stores `run_id`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `read`, monotonic `sequence`, `delivered_at`, and `sender_pane_key` (`src/main/runtime/orchestration/db/schema/create-core-tables-sql.ts:17-44`). Insertion is a normal SQLite insert (`src/main/runtime/orchestration/db/messages/message-insert.ts:26-55`).

Run/Dispatch identity is also durable: Tasks and Dispatch contexts are SQLite tables (`src/main/runtime/orchestration/db/schema/create-graph-tables-sql.ts:88-138`), and `createDispatchContext` atomically claims a ready Task, marks it dispatched, and records assignee handle/pane/process (`src/main/runtime/orchestration/db/dispatch-context/dispatch-context-store.ts:39-117`). Direct rows are atomically retargeted to canonical `run:`/`dispatch:` mailboxes when ownership is resolved (`src/main/runtime/orchestration/db/messages/direct-mailbox-routing.ts:38-113`).

### 3. How the recipient is resumed or invoked

`notifyMessageArrived` resolves the canonical mailbox and looks for `check --wait` waiters (`src/main/runtime/orchestration/mailbox-notification-coordinator.ts:42-69`). A matching waiter is resolved; it owns the read and no PTY injection occurs. Otherwise a microtask runs pointer delivery. `OrcaRuntimeService.notifyMessageArrived` also schedules a repoint (`src/main/runtime/orca-runtime.ts:34849-34867`).

Pointer delivery requires a live writable PTY and `lastAgentStatus === 'idle'` with a live observation (`src/main/runtime/orchestration/mailbox-pointer-delivery.ts:39-56`). It skips rows reserved by waiters, selects unread undelivered rows, stages the pointer, marks rows delivered, and after a 500 ms delay rechecks process/liveness/status before writing `\r` (`mailbox-pointer-delivery.ts:65-136,170-275`; `mailbox-pointer-submit.ts:25-90`). If the agent is working, the function returns without writing and leaves `read=0, delivered_at=NULL` for a later idle edge. Idle transitions and restored graph edges call `deliverPendingMessagesForLeaf` (`src/main/runtime/orca-runtime.ts:6944-6959,11850-11886`).

The source-level tests are unusually explicit: the idle test expects the pointer and CR but asserts the body is not written (`src/main/runtime/orca-runtime.test.ts:35275-35317`); the Run mailbox test asserts no write while working and a pointer after idle (`:35320-35364`); the working test asserts no write and no `delivered_at` (`:35727-35755`); the waiter test asserts notification without PTY injection (`:36252-36289`).

With a current Dispatch, `orchestration.check` reads from `dispatch:<id>`, marks consumed messages read, or waits for `runtime.waitForMessage` (`src/main/runtime/rpc/methods/orchestration.ts:1144-1303`). Run mailbox wait/ack uses durable Delivery rows (`:920-1141`). The skill guide confirms that `check --peek --format` returns locally formatted mail and never writes terminal input, while a follow-up is structured inbox mail received by the worker's next `orchestration check` (`skill-guides/orchestration.md:139-149,227-228`).

### 4. Tracked task dispatch and direct prompt injection

`dispatch --inject` is a separate path. It requires a ready Task and recognized agent, creates a Dispatch context and capability, builds a preamble, and calls `sendTerminalAgentPrompt` (`src/main/runtime/rpc/methods/orchestration.ts:1586-1711`). The preamble includes coordinator/worker handles, Task/Dispatch IDs, lifecycle commands, and the task spec (`src/main/runtime/orchestration/preamble.ts:47-145`).

`sendTerminalAgentPrompt` writes bracketed-paste bytes to the PTY and then CR after render or the submit delay (`src/main/runtime/orca-runtime.ts:18637-18691,19356-19447`; bytes `src/shared/agent-prompt-injection.ts:3-5,38-43`). The dispatch test proves this uses the agent-prompt path rather than raw terminal send (`src/main/runtime/rpc/methods/orchestration-tasks-dispatch.test.ts:355-379`). This is the only inspected orchestration path that directly sends the task content to the agent TUI.

### 5. Federated workers

Coordinator-to-remote-worker control mail is first persisted in a source-side `federation_relay_items` row (`src/main/runtime/rpc/methods/orchestration.ts:625-681`; enqueue transaction `src/main/runtime/orchestration/db/federation/federation-relay-enqueue.ts:10-175`). A one-second relay timer invokes federation sync (`src/main/runtime/orca-runtime.ts:5836-5860`), which calls remote `orchestration.federationImport`; the remote imports the message and calls `notifyMessageArrived` for `dispatch:<id>` (`src/main/runtime/orchestration/federation-sync.ts:78-196`; `src/main/runtime/rpc/methods/orchestration-federation-relay.ts:145-214`). Thus remote mail is also structured inbox mail, not a cross-server direct prompt injection. The worker's local idle pointer/check path is unchanged.

## Claims

1. Orca's current structured communication primitive is a durable mailbox row plus notification, not a model-context API. This is directly established by the send insert/notify path and the schema.
2. Ordinary mailbox body content does not enter an active agent's context mid-turn through Orca. A working recipient gets no PTY write; a waiting `check` gets the RPC result through its existing command call; an idle recipient gets a pointer and must issue `check`.
3. Ordinary mail is intended as a new bottom turn only for the idle-pointer case. The content of that PTY turn is the pointer, not the mail body.
4. `dispatch --inject` is prompt-like direct PTY input. It is intended to be a fresh task turn when the documented `tui-idle` precondition is honored, but the implementation does not enforce idle status before writing.

## Inferences and unknowns

- It is reasonable to infer that an idle pointer becomes a provider-side user prompt because Orca writes ordinary terminal input and submits CR to the interactive agent. This is an inference about provider behavior, not a source-level transcript witness.
- It is reasonable to infer that the body returned by `orca orchestration check` appears to the model as command/tool output, because the agent must invoke the CLI and Orca returns the RPC result to that CLI. Orca never constructs a provider tool-result item itself.
- The exact provider transcript role (user, system, developer, tool, harness/synthetic) is unknown from Orca. No inspected path calls a provider SDK or constructs transcript items; the external agent CLIs own that mapping.
- `dispatch --inject` can technically write while the target agent is active: `orchestration.dispatch` checks agent recognition and stable pane/process authority, while `sendTerminalAgentPrompt` checks generation/permission safety but not idle status. The guide says to wait for `tui-idle` (`skill-guides/orchestration.md:379`), so a compliant call is bottom/new-turn intended; a noncompliant call may be mid-context and provider handling is unknown.
- A terminated or unreachable recipient is not resumed by `send`; the row remains durable for explicit `check`/restore. The inspected code schedules restored rows but does not launch an agent process as part of notification.

## Sources

- Witness record: `flows/4b7c9e21/witnesses/orcaCommunication.md`.
- Upstream revision: [stablyai/orca at 80b2a023](https://github.com/stablyai/orca/tree/80b2a0237729af8c3c57c39cd94e087b698058b9).
- [Orca orchestration skill guide](https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/skill-guides/orchestration.md).
- [orchestration RPC methods](https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/rpc/methods/orchestration.ts), [mailbox pointer delivery](https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/orchestration/mailbox-pointer-delivery.ts), [formatter](https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/orchestration/formatter.ts), [runtime tests](https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/orca-runtime.test.ts), and [dispatch preamble](https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/orchestration/preamble.ts).
