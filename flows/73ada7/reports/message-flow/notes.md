# message-flow: grounds and pulls

F = `/home/li/primary/flows/`, PS = `/git/github.com/LiGoldragon/psyche-skills/skills/`.
Records were read as quoted in `F/d4ae97/reports/topic-nexus/context.md`;
`F/edf227/vision/identifiers.md`, `F/8475a9/vision/datom.md` and
`F/d4ae97/vision/datom.md` were read at their source.

Files, each one root, each checked by ethos-zero 16.0.0
(`/git/github.com/LiGoldragon/ethos-zero/target/debug/ethos-zero`) as `Checked`:

- Library: `address.library.ethos` (FlowId, Process, Aspect, Topic, Layer, Metaflow, Sender, Recipient), `lock.library.ethos` (Deadline, Lock), `request.library.ethos` (Request).
- Message: `message.signal.ethos`, `message.operation.ethos`, `message.memory.ethos`.
- Flow: `flow.signal.ethos`, `flow.operation.ethos`, `flow.memory.ethos`.

A file imports another by its library's name (`address:`, `lock:`, `request:`). Three drafts rest on books that await the living's rulings, each marked "proposal, pending ruling":

- `Request.[ Order.String Question.String Result.String Notice.String ]`, one layer of variants over a string, in place of `Meaning`: «The queue and the waking rule», proposal 1 (https://claude.ai/artifact/HUA3QJiFyVErW12sgJ79wC). `Meaning` and the datom-codec dependency are gone. The flow's own inference: this one type replaces `Message`, `Body` and `Psyche`, so the vector of supporting psyche and the audit and information kinds are not carried.
- Message asks Flow for a time-bound lock on the metaflow and hands Flow the request; Flow places the request in the current flow and holds no messages: «Flow, a passable vision», proposal 5 (https://claude.ai/artifact/LFKcRWAPzj1FdG1Em1TbJ4). Datom appears only at the edge, behind a datom feature that the CLI enables and the Nexus does not; no file here declares it.
- `FlowId.Integer`, three words, in place of the pending `Hash`: «Stored type and datom form», proposal 3 (https://claude.ai/artifact/6cgk7UGUTyK9gCFULNtfLC). The same book's `Encodable` kind and `Bytes<32>` holding a `Sha256` as hex serve a module content hash, which no file here holds; `FlowId` is not declared `Encodable` here; whether Library can bear that kind is unwitnessed.

One-field newtypes are written `Name.Type` (`FlowId.Integer`, `Process.Integer`, `Deadline.Integer`), never as a one-field struct. ethos-zero 16.0.0 generates an alias for that form (`pub type FlowId = i64;`, `pub type Deadline = i64;`), witnessed by Generate on the two library files. That alias is the generator's defect, awaiting ruling (e5a0bc «Ethos: inline, layout, expansion», point 3).

## Types and the records they rest on

Library (`address`, `lock` and `request` files)

- `FlowId.Integer` (proposal, pending ruling, «Stored type and datom form», proposal 3): "it's not an integer, it's a hash" and "The flow ID is not a string, it's a hash" (F`edf227/vision/identifiers.md`, 2026-10-03); "Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive" (PS`vision-nexus.md`).
- `Process.Integer`: "it identifies the process that called it and carries that identity in the message" (PS`vision-nexus.md`); "It figures out the process that's calling" (F`b7ba00/vision/callerIdentity.md`, 2026-09-26).
- `Aspect.[ Psyche Mind Field ]`: "The variants are all of the different voice aspects directly. They're called by name: psyche, mind, field" (F`d4ae97/vision/flow.md`, 2026-10-07); "There are three aspects to every topic" (F`ebbe30/vision/aspects.md`, 2026-10-09).
- `Topic.[ Core Testing ]`, a placeholder: the topic type's name is unsettled ("a new type which I talked about yesterday ... I'm trying to come up with a name", F`73ada7/notion/metaflow.md`, 2026-10-09, notion). Its variants: "Subjects, topics and subtopics ... will even become variants in actual Nexus components" (F`edf227/vision/topics.md`, 2026-10-03); "the non-topiced flows would just be the topic of core" and "I also want this topic. The whole topic is testing." (F`d4ae97/vision/flow.md`, 2026-10-08). No other topic is named as wanted.
- `Layer.[ Primary Secondary Tertiary ]`: "They're separated by layer" (F`d4ae97/vision/flow.md`, 2026-10-07); "from tertiary to primary" (same file, 2026-10-07); "Psyche, Mind, Field by Primary, Secondary, Tertiary" (PS`vision-flow.md`). PS`vision-nexus.md`'s example adds Quaternary; no record of the living's names it.
- `Metaflow.{ Aspect Topic Layer }`: "A flow is aspect, topic and layer ... it's a struct. It's just a struct. The first field is the aspect" (F`d4ae97/vision/flow.md`, 2026-10-08); "The aspect is now, I think, part of any metaflow" (F`ebbe30/vision/aspects.md`, 2026-10-09).
  Suggestion only, from a notion that rules nothing: "each one uh, variant of either psyche, mind, or field. So all metaflows will essentially have an aspect. And then the struct, will contain their details, such as ... the name of their topic" (F`73ada7/notion/metaflow.md`, 2026-10-09). That shape is an enum of the three aspects, each carrying one struct of details; it is not written here.
- `Sender.{ Metaflow }`: "The message has to be able to figure out who the sender is programmatically eventually from the process that called" (F`b7ba00/vision/messaging.md`, 2026-09-26); "The messenger identifies the originator only by its voice" (F`d4ae97/vision/messenger.md`, 2026-10-05); "A voice is a permanent Metaflow" (F`f5a6e9/vision/flow.md`, 2026-10-07).
- `Recipient.[ Metaflow Up ]`: "The message doesn't have to know about the flows. It can also just talk in terms of metaflows." (F`f5a6e9/vision/flow.md`, 2026-10-07); "it would be bad practice to try to send to a flow ID" (F`d4ae97/vision/datom.md`, 2026-10-07); "If you say 'send up' it means message higher layer" (F`b7ba00/vision/messaging.md`, 2026-09-26).
- `Lock.{ Metaflow Deadline }`, `Deadline.Integer`: "The message is going to ask for a lock, which should be time-bound so that it doesn't lock forever. ... Flow told the message that it has the lock for that flow or that metaflow." (F`f5a6e9/vision/flow.md`, 2026-10-07).
- `Request.[ Order.String Question.String Result.String Notice.String ]` (proposal, pending ruling, «The queue and the waking rule», proposal 1): "the head is ... where the message type is ... It's a new type and it carries all the data." (F`b7ba00/vision/messaging.md`, 2026-09-26). Priority is absent: "We don't even do the soft or hard, actually. That was the wrong approach." (same file).

Message Signal (`message.signal.ethos`)

- `Send.{ Process Recipient Request }`: "message, not flow-send. use the message nexus!" (F`da1e3f/vision/operational-flowVsMessage.md`, 2026-09-17); the process as above.
- `Delivered`, `Undelivered`: "the Flow would say successful or not" (F`1b8ac0/vision/messaging.md`, 2026-09-21).
- `Queued`: "every topic has its own flow; messages queue, and only a waking message wakes it" (F`d4ae97/vision/messenger.md`, 2026-10-08). Which message wakes is left out (open).
- `Refused.Unidentified`: caller identity as above. `Unknown`: "we need a registry to know which flow is active" (F`d4ae97/vision/flow.md`, 2026-10-07). `Held`: the lock "will be useful in order to know whether the messages can or cannot reach a certain flow" (F`e5a0bc/vision/flow.md`, 2026-10-07). `OutOfLevel`: "he cannot message from tertiary to primary or from tertiary to secondary of another aspect ... horizontally, [one] level up, or any level down and across" and "I want that hard-enforced" (F`d4ae97/vision/flow.md`, 2026-10-07).
- Typed refusals at all: "errors are vocabulary, never strings" (PS`vision-nexus.md`).

Message Operation (`message.operation.ethos`)

- `Identify`, `Lock`, `Deliver`, `Enqueue` and their outcomes: "Every effect has a matching operation type" (PS`vision-nexus.md`); the lock, deliver and queue records above; "it can use that to talk to Flow to figure out which Flow used the CLI" (F`b7ba00/vision/callerIdentity.md`, 2026-09-26). `StoreRefused`: "memory answers operation that the change succeeded or failed" (PS`vision-nexus.md`).

Message Memory (`message.memory.ethos`)

- `Waiting.{ Sender Metaflow Request }`: "the whole queue is checked in order, from the first received to the last" (F`d4ae97/vision/messenger.md`, 2026-10-08). No message id: "We shouldn't get the message ID." (F`b7ba00/vision/messaging.md`, 2026-09-26).

Flow Signal (`flow.signal.ethos`)

- `Identify.Process` / `Identified.Metaflow` / `Unidentified`: "talk to Flow to figure out which Flow used the CLI" (F`b7ba00/vision/callerIdentity.md`, 2026-09-26); "Message can get the data from Flow" (F`c7128c/vision/messageAndFlow.md`, 2026-09-18).
- `Lock.Metaflow` / `Locked.Lock` / `LockRefused.[ Held Unknown ]`: the time-bound lock (F`f5a6e9/vision/flow.md`, 2026-10-07); the rollover lock "we need in order to roll over a metaflow" (F`e5a0bc/vision/flow.md`, 2026-10-07); "Flow can put a lock on some stuff" (F`c7128c/vision/messageAndFlow.md`, 2026-09-18).
- `Deliver.{ Lock Sender Request }` / `Delivered` / `Undelivered`: "If it does get a lock then the message nexus can send that object over to Flow with the message" (F`f5a6e9/vision/flow.md`, 2026-10-07); "a more lock-enabled deliver message" (F`b7ba00/vision/messaging.md`, 2026-09-26).

Flow Operation (`flow.operation.ethos`)

- `Identify`, `Lock`, `Write` (places the request in the current flow; proposal, pending ruling, «Flow, a passable vision», proposal 5), `Release`: "It locks the message for the session to send the message, then it sends the message, then it removes the lock." and "it is the only process that can write in that herder session" (F`1b8ac0/vision/messaging.md`, 2026-09-21).

Flow Memory (`flow.memory.ethos`)

- `Current.{ Metaflow FlowId }`: "a reference in the meta flow memory to ... current for it" (F`f5a6e9/vision/flow.md`, 2026-10-07); "we need a registry to know which flow is active" (F`d4ae97/vision/flow.md`, 2026-10-07).
- `Running.{ FlowId Process }`: "Refresh Flow, who called it?" (F`b7ba00/vision/callerIdentity.md`, 2026-09-26); "the Flow CLI will check the process that called it" (F`836818/vision/flowNexus.md`, 2026-09-24).
- `HeldLock.{ Metaflow Deadline }`: the time-bound lock, as Flow's own record; "Storage vocabulary never appears on the public wire" (PS`vision-nexus.md`).

Left out as notion or open: the metaflow's predecessor ("maybe its predecessor", F`f5a6e9/vision/flow.md`); the role string ("I'm not even sure that a flow always has a role", same file); the verbatim's input mode ("maybe even has an inner variant", F`b7ba00/vision/messaging.md`); the full psyche's date; age; the waking rule; who resolves `Up`; the side-flow broker (F`8475a9/notion/messenger.md`); the raw send on Flow's meta socket, which Message does not use (F`b7ba00/vision/messaging.md`, 2026-09-26); the fixed-size metaflow record (F`d4ae97/notion/flow.md`).

## Pulls against the constraints

1. Message text is a string. "A better version of message should be redone and redeployed with just a string as the basic form." (F`b7ba00/vision/messaging.md`, 2026-09-26) against "It's going to be forbidden for string handling to be in the Nexus." (F`8475a9/vision/datom.md`, 2026-10-05). Written as `Request`, whose variants each hold a `String`; the string stays in the Nexus pending the living's ruling on «The queue and the waking rule».
2. Datom at the edge only. Datom appears behind a datom feature that the CLI enables and the Nexus does not (proposal, pending ruling, «Flow, a passable vision», proposal 5); against "There should be no datom in any Nexus." (F`8475a9/vision/datom.md`, 2026-10-05) it holds. Nothing here rests on vision-messaging's "the message body is a datom that lands in the recipient's prompt", whose removal is being proposed.
3. Flow writes text into a terminal. "a request to send this text into a particular harness" and "Flow would even be the part that sends the text" (F`1b8ac0/vision/messaging.md`, 2026-09-21): Flow's `Write` places the request in the current flow, as text inside the Flow Nexus.
4. How the text reaches a prompt is open: the living's own question, "how does Nexus send datom to places without needing to know how to deserialize and serialize datom itself?" (F`5578cc/notion/nexus.md`, 2026-10-03).
5. Topic as a PascalCase string. "The topic is a string but it's a certain type of string. ... It's basically PascalCase of a certain number of words" (F`d4ae97/vision/flow.md`, 2026-10-08), against "these will even become variants" (F`edf227/vision/topics.md`, 2026-10-03). Written as variants; only `Core` and `Testing` are named.
6. Role as a camel-case string. "we describe a role as maybe some kind of short camelcase expression, a string" (F`f5a6e9/vision/flow.md`, 2026-10-07). Left out.
7. Flow id as an integer. Resolved by «Stored type and datom form», proposal 3 (pending ruling): `FlowId.Integer`, 33 bits written as three words. "The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits" and "If 33 bits, for me, I think it is enough entropy" (F`edf227/vision/identifiers.md`, 2026-10-03).
8. Sender in the message kind. "field report, psyche report, field question, psyche question" (F`b7ba00/vision/messaging.md`, 2026-09-26) names the sender's aspect inside the kind, which the caller identity already carries. Written as the request kinds.
9. Sender as voice only. "for now the sender is psyche primary or psyche secondary, etc." (F`b7ba00/vision/messaging.md`, 2026-09-26) has no topic, while a metaflow has one; and "not every message will come from a voice" (F`8475a9/vision/messenger.md`, 2026-10-05): a job flow has no `Sender` here.
10. Simple and full as two forms. "A simple message, a simple psyche" and "A full message that can have many fields" (F`b7ba00/vision/messaging.md`, 2026-09-26) pull toward two types for one datum; ethos-zero has no formats section. Written as `Request`, one string per kind.
11. Each kind a new type. "It's a new type and it carries all the data." (F`b7ba00/vision/messaging.md`, 2026-09-26) pulls toward one enum of kinds each wrapping a payload. Written as `Request.[ Order.String ... ]`: one variant layer over a string.
12. One file, many roots. ethos-zero reads one root per file, and two Signals or two Operations in one module would each generate `Query`/`Response` or `Operation`/`Outcome`. vision-ethos: "The unit is File: one file, one Rust module." Written as one file per root.
13. Time-bound lock without a time type. "which should be time-bound so that it doesn't lock forever" (F`f5a6e9/vision/flow.md`, 2026-10-07) needs a time; no record names a unit or clock, so `Deadline.Integer` has none.
14. Send up without a resolver. "The message logic has to figure out where ... or maybe the flow figures it out. I don't know" (F`b7ba00/vision/messaging.md`, 2026-09-26): `Recipient.Up` is declared and no operation resolves it.
15. Level enforced or not. "I want that hard-enforced" against "the messaging program is imperfect and it cannot actually enforce this" (F`d4ae97/vision/flow.md`, 2026-10-07). Written as the refusal `OutOfLevel`.
16. A lock referenced by value. "every reference names its target by that name" (PS`vision-nexus.md`) pulls `Deliver` toward a lock name; `Deliver` carries the `Lock` itself.
