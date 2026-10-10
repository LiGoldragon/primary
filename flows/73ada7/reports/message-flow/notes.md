# message-flow: grounds and pulls

F = `/home/li/primary/flows/`, PS = `/git/github.com/LiGoldragon/psyche-skills/skills/`.
Records were read as quoted in `F/d4ae97/reports/topic-nexus/context.md`;
`F/edf227/vision/identifiers.md`, `F/8475a9/vision/datom.md` and
`F/d4ae97/vision/datom.md` were read at their source.

Files, each one root, each checked by ethos-zero 16.0.0
(`/git/github.com/LiGoldragon/ethos-zero/target/debug/ethos-zero`) as `Checked`:

- Message: `message.library.ethos`, `message.signal.ethos`, `message.meta.signal.ethos`, `message.operation.ethos`, `message.memory.ethos`. The shared types (FlowId, Request, Address, Recipient, Lock, Process, Sender) are Flow's Library, f5a6e9's design at main e17a62ca, and are imported as `flow_ethos`; Flow's own files are f5a6e9's.

A file imports another by its library's name (`address:`, `lock:`, `request:`). Three drafts rest on books that await the living's rulings, each marked "proposal, pending ruling":

- `Request.[ Order.String Question.String Result.String Notice.String ]`, one layer of variants over a string, in place of `Meaning`: «The queue and the waking rule», proposal 1 (https://claude.ai/artifact/HUA3QJiFyVErW12sgJ79wC). `Meaning` and the datom-codec dependency are gone. The flow's own inference: this one type replaces `Message`, `Body` and `Psyche`, so the vector of supporting psyche and the audit and information kinds are not carried.
- Message asks Flow for a time-bound lock on the metaflow and hands Flow the request; Flow places the request in the current flow and holds no messages: «Flow, a passable vision», proposal 5 (https://claude.ai/artifact/LFKcRWAPzj1FdG1Em1TbJ4). Datom appears only at the edge, behind a datom feature that the CLI enables and the Nexus does not; no file here declares it.
- `FlowId.String`, a string for now with a comment that a hash-based id is wanted, in place of the pending `Hash`. Ground: `flows/ebbe30/vision/ethos.md:39-55` (2026-10-09) and Fable's second edition. This change is pending the living's ruling. It replaces the earlier `FlowId.Integer` draft of «Stored type and datom form», proposal 3 (https://claude.ai/artifact/6cgk7UGUTyK9gCFULNtfLC). The same book's `Encodable` kind and `Bytes<32>` holding a `Sha256` as hex serve a module content hash, which no file here holds; `FlowId` is not declared `Encodable` here; whether Library can bear that kind is unwitnessed.

One-field newtypes are written `Name.Type` (`FlowId.String`, `Process.Integer`, `Deadline.Integer`), never as a one-field struct. ethos-zero 16.0.0 generates an alias for that form (`pub type FlowId = i64;` for the earlier integer draft, `pub type Deadline = i64;`), witnessed by Generate on the two library files. That alias is the generator's defect, awaiting ruling (e5a0bc «Ethos: inline, layout, expansion», point 3). In Rust, an impl written for an alias is an impl for the aliased type, so `Encodable` on `FlowId` would land on `i64` itself and collide with any other `i64` alias that needs its own encoding (a Rust rule, not witnessed in this code).

## Types and the records they rest on

Message Signal (`message.signal.ethos`)

- `Send.{ Recipient Request }`, `Recipient.[ Address Up ]` being Flow's: "message, not flow-send. use the message nexus!" (F`da1e3f/vision/operational-flowVsMessage.md`, 2026-09-17); the process as above.
- `Delivered`: "the Flow would say successful or not" (F`1b8ac0/vision/messaging.md`, 2026-09-21).
- `Queued`: "every topic has its own flow; messages queue, and only a waking message wakes it" (F`d4ae97/vision/messenger.md`, 2026-10-08). Which message wakes is left out (open).
- `Refused.Unidentified`: caller identity as above. `Unknown`: "we need a registry to know which flow is active" (F`d4ae97/vision/flow.md`, 2026-10-07). `Held`: the lock "will be useful in order to know whether the messages can or cannot reach a certain flow" (F`e5a0bc/vision/flow.md`, 2026-10-07). `OffRoute`: "he cannot message from tertiary to primary or from tertiary to secondary of another aspect ... horizontally, [one] level up, or any level down and across" and "I want that hard-enforced" (F`d4ae97/vision/flow.md`, 2026-10-07).
- Typed refusals at all: "errors are vocabulary, never strings" (PS`vision-nexus.md`).

Message Operation (`message.operation.ethos`)

- `Identify`, `Lock`, `Deliver`, `Release` and their outcomes: "Every effect has a matching operation type" (PS`vision-nexus.md`); the lock, deliver and queue records above; "it can use that to talk to Flow to figure out which Flow used the CLI" (F`b7ba00/vision/callerIdentity.md`, 2026-09-26). `StoreRefused`: "memory answers operation that the change succeeded or failed" (PS`vision-nexus.md`).

Message Memory (`message.memory.ethos`)

- The queue is Flow's, not Message's: "the whole queue is checked in order, from the first received to the last" (F`d4ae97/vision/messenger.md`, 2026-10-08). No message id: "We shouldn't get the message ID." (F`b7ba00/vision/messaging.md`, 2026-09-26).

Left out as notion or open: the metaflow's predecessor ("maybe its predecessor", F`f5a6e9/vision/flow.md`); the role string ("I'm not even sure that a flow always has a role", same file); the verbatim's input mode ("maybe even has an inner variant", F`b7ba00/vision/messaging.md`); the full psyche's date; age; the waking rule; the side-flow broker (F`8475a9/notion/messenger.md`); the raw send on Flow's meta socket, which Message does not use (F`b7ba00/vision/messaging.md`, 2026-09-26); the fixed-size metaflow record (F`d4ae97/notion/flow.md`).

## Pulls against the constraints

1. Message text is a string. "A better version of message should be redone and redeployed with just a string as the basic form." (F`b7ba00/vision/messaging.md`, 2026-09-26) against "It's going to be forbidden for string handling to be in the Nexus." (F`8475a9/vision/datom.md`, 2026-10-05). Written as `Request`, whose variants each hold a `String`; the string stays in the Nexus pending the living's ruling on «The queue and the waking rule».
2. Datom at the edge only. Datom appears behind a datom feature that the CLI enables and the Nexus does not (proposal, pending ruling, «Flow, a passable vision», proposal 5); against "There should be no datom in any Nexus." (F`8475a9/vision/datom.md`, 2026-10-05) it holds. Nothing here rests on vision-messaging's "the message body is a datom that lands in the recipient's prompt", whose removal is being proposed.
3. Flow writes text into a terminal. "a request to send this text into a particular harness" and "Flow would even be the part that sends the text" (F`1b8ac0/vision/messaging.md`, 2026-09-21): Flow's `Write` places the request in the current flow, as text inside the Flow Nexus.
4. How the text reaches a prompt is open: the living's own question, "how does Nexus send datom to places without needing to know how to deserialize and serialize datom itself?" (F`5578cc/notion/nexus.md`, 2026-10-03).
5. Topic as a PascalCase string. "The topic is a string but it's a certain type of string. ... It's basically PascalCase of a certain number of words" (F`d4ae97/vision/flow.md`, 2026-10-08), against "these will even become variants" (F`edf227/vision/topics.md`, 2026-10-03). Written as variants; only `Core` and `Testing` are named.
6. Role as a camel-case string. "we describe a role as maybe some kind of short camelcase expression, a string" (F`f5a6e9/vision/flow.md`, 2026-10-07). Left out.
7. Flow id as an integer. Now `FlowId.String`, pending the living's ruling (`flows/ebbe30/vision/ethos.md:39-55`, 2026-10-09; Fable's second edition); a hash-based id is wanted. "The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits" and "If 33 bits, for me, I think it is enough entropy" (F`edf227/vision/identifiers.md`, 2026-10-03).
8. Sender in the message kind. "field report, psyche report, field question, psyche question" (F`b7ba00/vision/messaging.md`, 2026-09-26) names the sender's aspect inside the kind, which the caller identity already carries. Written as the request kinds.
9. Sender as voice only. "for now the sender is psyche primary or psyche secondary, etc." (F`b7ba00/vision/messaging.md`, 2026-09-26) has no topic, while a metaflow has one; and "not every message will come from a voice" (F`8475a9/vision/messenger.md`, 2026-10-05): a job flow has no `Sender` here.
10. Simple and full as two forms. "A simple message, a simple psyche" and "A full message that can have many fields" (F`b7ba00/vision/messaging.md`, 2026-09-26) pull toward two types for one datum; ethos-zero has no formats section. Written as `Request`, one string per kind.
11. Each kind a new type. "It's a new type and it carries all the data." (F`b7ba00/vision/messaging.md`, 2026-09-26) pulls toward one enum of kinds each wrapping a payload. Written as `Request.[ Order.String ... ]`: one variant layer over a string.
12. One file, many roots. ethos-zero reads one root per file, and two Signals or two Operations in one module would each generate `Query`/`Response` or `Operation`/`Outcome`. vision-ethos: "The unit is File: one file, one Rust module." Written as one file per root.
13. Time-bound lock without a time type. "which should be time-bound so that it doesn't lock forever" (F`f5a6e9/vision/flow.md`, 2026-10-07) needs a time; no record names a unit or clock, so `Deadline.Integer` has none.
14. Who resolves send up. "The message logic has to figure out where ... or maybe the flow figures it out. I don't know" (F`b7ba00/vision/messaging.md`, 2026-09-26). f5a6e9's ruling, current best and not before the living: `Send.{ Recipient.[ Address Up ] Request }`, with Flow's lock `Lock.Recipient`: Flow resolves `Up` on the lock itself, from the sender it identifies by process, and answers `Locked.Lock` carrying the resolved Address, or refuses `NoneAbove` at the top layer. There is no `ResolveUp` query; the lock is one round trip. `Up` is the layer above within the sender's aspect. `Deliver` stays Address-only. The living's ruling on «Who works out where send up goes» may move the resolving to Message without changing the wire.
15. Level enforced or not. "I want that hard-enforced" against "the messaging program is imperfect and it cannot actually enforce this" (F`d4ae97/vision/flow.md`, 2026-10-07). Written as the refusal `OffRoute`.
16. A lock referenced by value. "every reference names its target by that name" (PS`vision-nexus.md`) pulls `Deliver` toward a lock name; `Deliver` carries the `Lock` itself.
