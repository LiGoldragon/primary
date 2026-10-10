# Flow and Message basics: what works on ouranos now

Date: 2026-09-24, about 14:55 local. Read-only survey by a subflow of e51411. The only live requests sent were `ResolveRecipient`, which reads and changes nothing. No flow was messaged and no store or deployment was touched.

## What is deployed

- Flow: `flow-nexus.service` runs `/nix/store/x1mqkqx8…-flow-0.3.0/bin/flow-nexus`, started 09:52:49. It is built from Flow revision `4560453644c0` (`mind-sol-6288d1-gate-integration`), which the active CriomOS-home checkout pins (`flake.lock`, parent `90418576` "Compose green Flow and Message deployment"). That revision pins ordinary `signal-flow` `edfea8712513` (v2) and meta `meta-signal-flow` `192e1a8a7307`. Its sockets are `/run/user/1001/flow/flow.sock` and `flow-meta.sock`, and its store is `~/.local/state/flow/flow.sema`.
- Message: `message-daemon.service` runs `/nix/store/104qsfp8…-message-0.12.0/bin/message-daemon`, started 09:47:04. It is built from Message revision `a8c6a924d5d0` (`mind-sol-6288d1-message-v2-pending`), with `signal-message` 4.0.0 `37c3e5b75b05` and Flow v2 `edfea871`. Its sockets are `/run/user/1001/message/message.sock` and `message-owner.sock`. At 09:48:17 the journal shows `message-daemon[owner]: component: message archive: failed without error information`.
- Flow CLI grammar: `flow '<one inline Query datom>'`. For example, `flow ResolveRecipient.<id>` works. `flow --help` is rejected as an invalid Query.

## Requests the deployed Flow accepts

- Ordinary socket (`signal-flow` v2): `Start.StartRequest`, `Restart.RestartRequest`, `ResolveRecipient.RecipientResolutionRequest`. There are no others.
- Meta socket (`meta-signal-flow` 192e1a8): `Configure`, `ConsumeReset`, `RegisterFlow.FlowNode`. There are no others.

## Operations against the deployed system

| Operation (the living's basic list) | Deployed binary | Newer source only | Missing everywhere | Evidence |
|---|---|---|---|---|
| Start a flow (Claude or Codex, in a new Herdr pane, with a startup prompt, model, effort, skills) | Yes: `Start`. It creates a Herdr workspace and pane, runs `herdr agent start --kind claude\|codex -- --model … --effort …`, claims the Flow ID with `flow-id --flows-root`, and sends one composed first prompt | 149120f8 routes Codex through the pinned codex-next app-server endpoint | | `launch.rs` at 4560453. Deployed Codex Start targets `~/.codex/app-server-control`, but the live Codex flows run on `~/.codex-next`. No live `Started` receipt from the deployed binary was found. |
| Give the flow a title at Start | No. `LaunchProfile` has no title field. The Herdr label is a hash-derived agent name | No: not in the v2 or v3 `LaunchProfile`. v3 `Title` covers only the refresh handover title | Yes | `signal-flow` ethos at edfea871 and fa326ac0 |
| Stop a flow | No | Partial: the v3 refresh line (`flow/refresh-runtime-47764b`, 22c4141b; `signal-flow` fa326ac0) runs `herdr pane close` on a predecessor, but only inside `Refresh` | A standalone `Stop` request is missing | ethos request lists. `"close"` appears only in 22c4141b. |
| List flows | No | No | Yes. The only per-ID read is `ResolveRecipient` | ethos request lists at every signal-flow and flow head |
| Resolve one flow (the lookup Message needs) | Yes: `ResolveRecipient` | v3 returns a typed `RecipientDisposition` (`flow/message-lifecycle-v3-47764b`) | | Live: 5f38bc gives `RecipientResolved … Codex Available.{ …/.codex-next/…sock Parked } Unavailable … Active`. e51411, 00f95a and 752e0f give `UnknownFlow`. |
| Send raw input to a flow's pane through Flow | No | No | Yes. No Flow request carries text to a pane. Herdr has the primitive (`herdr agent prompt`, `pane send-text`, `send-keys`), and today only Message calls it | `message` src at a8c6a924: `deliver_herdr` runs `herdr --session S agent prompt PANE DATOM` |
| Bind already-running flows into Flow (bootstrap) | Only `RegisterFlow` (meta), one flow at a time. It needs a valid `flow-id` claim marker | `MetaBindExisting` at 6ed7d174 and 149120f8 (published, Flow 0.4, fresh store). `MetaConfirmExisting` at 18b03f5e and d5e1305b (unsafe per 00f95a, undeployed). Recovery admission at 87e41bc6 and 279fcdc0 | | `flows/6288d1/reports/meta-bind-existing-v2-source-handoff.md`, `flows/00f95a/log.md` |
| Message: accept a message | Yes: `Submit`, `SubmitStamped`, `Deliver`, `FlowDeliver`, `QueryInbox`, `QueryThread(s)`, `SubscribeThread`, agent registry, `FlowAnnounceIdle` | | | `signal-message` ethos at 37c3e5b7. Owner socket: `Configure` only. |
| Message: deliver into a real pane | Code yes, live no. Message asks Flow `ResolveRecipient`. It needs `FlowLifecycle::Active` plus `HerdrRouteSelection::Available`, and that route must be idle or working and `interactive_ready`. Then it checks for a blank composer and runs `herdr agent prompt`. Otherwise it uses the Claude daemon-attach or Codex `turn/start` endpoint, and a `Parked` endpoint means it holds the message | v3 disposition consumer at a283368d | | Live: no flow has an Available Herdr route, so every delivery today would be Parked or fail with UnknownFlow |

## What Message needs from Flow to deliver into a real pane

Message needs a Flow row that is `Active` and has `HerdrRouteSelection::Available`. The only live row that resolves is 5f38bc, and its Herdr route is `Unavailable` and its endpoint `Parked`. Rows imported by BindExisting are Pending, or RegisteredUnconfirmed, and Message holds them by design. They become deliverable only after a confirmation that reads native evidence. That slice is `MetaConfirmExisting`. Its source exists, but 00f95a has marked it unsafe and it is not deployed. A flow that the deployed Flow `Start`s itself would come out Active with a Herdr route. No such Start has been witnessed.

## Gaps and owners

- Start with a title: missing from the contract. No one owns it in any log.
- Stop: missing as a request. Its closest code is refresh retirement (`pane close`) on the 47764b v3 line, which is unintegrated and has no seat now that 47764b has handed off. No one owns a standalone Stop.
- List: missing. No owner.
- Raw send through Flow: missing. It is the smallest gap: one ordinary request, `(FlowId, text)`, that resolves the Herdr route and runs `herdr agent prompt`, which is the code Message already has in `deliver_herdr`. No owner. One contradiction: the psyche said on 2026-09-17 that "flow is to start or refresh a flow" and that messages go through `message` (`flows/da1e3f/vision/operational-flowVsMessage.md`). On 2026-09-24 the living asked to "send messages with Flow … use it raw" (`flows/752e0f/vision/flowDeploy.md`). The newer word governs.
- Binding the live flows, so Message has targets: owned by Mind Sol 00f95a (source: confirm, recovery), with Field Astra 5f38bc as deploy executor. Astra's CriomOS-home commit `5b36ff26` (`field-astra-5f38bc-flow-pins`) pins Flow `149120f8` (BindExisting plus codex-next routing) with Message still at `a8c6a924`. It is committed but not activated: the running Nexus is still 4560453.
- Message archive failure at 09:48:17: 47764b named it a priority before handing off. No current owner is logged.

## The basic spec, as recorded

- `Vision/flowNexus.md`: Flow Nexus "sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt". A replaced session is reaped by the refresh itself. The requester asks by request ID for status and sends messages to a subflow.
- `flows/752e0f/vision/flowDeploy.md` and `flows/e51411/vision/authority.md` (living, 2026-09-24): start flows, stop flows, send messages with Flow ("bare input"). Flow deploys first and is used raw. Message builds on it. No more features.
- `flows/d8df70/vision/flowTool.md`: anybody may call Flow, and the CLI checks the calling process so a flow can refresh itself. A meta socket binds the existing Herdr session and then a vector of its flows.
- `flows/d8df70/vision/flowLifecycle.md`: a new flow receives as soon as it has its start prompt. The old flow stops receiving, is killed, and its conversation archived. Refresh needs a recent handover in the transcript.
- `flows/e51411/vision/launch.md`: one start prompt, with `/main-flow` in it. The Flow ID is claimed by code at start.
- `flows/da1e3f/vision/operational-flowVsMessage.md` (2026-09-17): `flow` starts or refreshes. `message` sends. Meta features such as usage reset go through `flow-meta`.
- Flow `README.md` at 4560453 names: Start, provenance-authorized Restart, ResolveRecipient, Configure, reset consumption, register-codex and register-claude.
- Basic operations named across these records: start, stop (kill and archive), refresh or restart, resolve, raw send, bind existing, and Message deliver. List appears in no record.

## Shortest path to all basics working

1. Deploy Astra's pinned Flow `149120f8` with a fresh store, then bind the live flows with `MetaBindExisting`. This is already assigned.
2. Add three thin ordinary requests to `signal-flow` v2 and Flow on the same line, each a wrapper over a Herdr command Flow already runs: `Send (FlowId, text)` → `herdr agent prompt`; `Stop (FlowId)` → `herdr pane close` plus the lifecycle row, lifting the retirement code from 22c4141b; `List` → the store rows. Add an optional title to `LaunchProfile`.
3. Let a successful `Send` round-trip stand as the confirmation, or deploy a corrected `MetaConfirmExisting`, so bound rows become `Active`. Then Message's existing `deliver_herdr` delivers unchanged.

## Sources

- Live: `ps`, `systemctl --user cat flow-nexus.service message-daemon.service`, `journalctl --user -u flow-nexus -u message-daemon` (2026-09-24), `/run/user/1001/{flow,message}`, `flow ResolveRecipient.{e51411,00f95a,5f38bc,752e0f}`, `herdr agent --help`, `herdr pane --help`.
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock` (flow `4560453644c0`, message `a8c6a924d5d0`); worktree `field-astra-5f38bc-flow-pins` commit `5b36ff26` (flow `149120f8`).
- `/git/github.com/LiGoldragon/flow` at `4560453644c0`: `README.md`, `crates/flow/src/main.rs`, `crates/flow-nexus/src/herdr.rs`, `crates/flow-nexus/src/herdr/launch.rs`, `Cargo.lock`. Heads `149120f82c35`, `6ed7d1742995`, `18b03f5e8b9c`, `d5e1305bf22f`, `87e41bc664d1`, `279fcdc07a25`, `22c4141be5b4`, `61d765e48140` (main).
- `/git/github.com/LiGoldragon/signal-flow` `ethos/signal.ethos` at `edfea8712513`, `fa326ac00b47`, `f03ffc784199`, `5180d929bbbb`. `/git/github.com/LiGoldragon/meta-signal-flow` at `192e1a8a7307`, `2e25563fc6bb`, `11a757435ed1`.
- `/git/github.com/LiGoldragon/message` at `a8c6a924d5d0`: `README.md`, `src/**` (`LiveNexusDelivery::deliver_herdr`), `Cargo.lock`. `/git/github.com/LiGoldragon/signal-message` at `37c3e5b75b05`. `/git/github.com/LiGoldragon/meta-signal-message` at `87a54b0a1cbc`.
- `/home/li/primary/flows/6288d1/reports/meta-bind-existing-v2-source-handoff.md`, `/home/li/primary/flows/00f95a/log.md`, `/home/li/primary/flows/5f38bc/log.md`, `/home/li/primary/flows/752e0f/log.md`, `/home/li/primary/flows/836818/log.md`.
- Vision: `/home/li/primary/Vision/flowNexus.md`, `/home/li/primary/flows/752e0f/vision/flowDeploy.md`, `/home/li/primary/flows/e51411/vision/authority.md`, `/home/li/primary/flows/e51411/vision/launch.md`, `/home/li/primary/flows/d8df70/vision/flowTool.md`, `/home/li/primary/flows/d8df70/vision/flowLifecycle.md`, `/home/li/primary/flows/da1e3f/vision/operational-flowVsMessage.md`.
