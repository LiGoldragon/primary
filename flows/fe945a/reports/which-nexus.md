# Which Nexus receives the to-the-living block

Question (the living, typed book comment, 2026-10-01, to 6997eb): "They're going to call the Nexus CLI so which Nexus do we use for this? Is this Flow, or is it Transcript, or is it something else?"

Ruled ground: a main flow wraps the block between `<!-- to-the-living:start -->` and `<!-- to-the-living:end -->`, with a metadata block carrying the book's title first. An end-of-turn hook picks the block and calls a Nexus CLI. The block reaches Psyche Sonnet, and Sonnet makes a book. How the hook fires is 6997eb's witness and is not covered here.

## 1. Candidates as they stand

| Candidate | Repo | Runs today | Ordinary operations (current contract) | Claimed domain |
|---|---|---|---|---|
| Flow Nexus | `flow`, `signal-flow` 7.0.0, `meta-signal-flow` 11.0.0 | Yes: `flow-nexus.service` and `flow-nexus-next.service` active; `flow` 0.12.2 on PATH | `Start` `Restart` `Replace` `Stop` `List` `LaunchStatus` `Observe` (Launch, Agent) `ResolveRecipient` `ResolveCaller`. Meta: `Configure` `ConsumeReset` `RegisterFlow` `MetaBindExisting` `Retire` `Deliver` `Vet` `Command` `ResolvePeer` | "starts, restarts, delivers to, stops, lists, and resolves flows, and is the only writer into their panes" (README) |
| Message Nexus | `message`, `signal-message` 7.0.0 (pinned) | Next only: `message-nexus-next.service` active (message 0.17.0); the stable `message-nexus.service` is inactive; `message` 0.14.0 on PATH | `Send` `Withdraw` `Acknowledge` `QueryReceipts` `Observe`; replies `Submitted` `Withdrawn` `Acknowledged` `Receipts` `ReceiptObserved` | "durable messages and receipts, delivered through Flow"; it reaches a pane only through Flow's `Deliver` |
| messenger-clj (hm-*) | `messenger-clj` | Yes (`hm-send` on PATH, `message-daemon.service`) | `#msg ["FLOW_ID" "text"]` EDN; not a Nexus | Live Flow routes in Herdr. The living calls it the hacky messenger, to be decommissioned (1b8ac0) |
| Transcript Nexus | `transcript` (Python shim; no `signal-transcript`) | No. The shim is an unpackaged flake, not on PATH; README: "Temporary, pending a Nexus" | Designed only (48cff7): `signal-transcript` with `Show`→`Shown` and an anchor-bounded `Block` (two short phrases mark a region); `meta-signal-transcript` | Harness transcripts: reading, searching and extracting from them |
| Curriculum Nexus | none; today `Curriculum` + `curriculum-deploy` (not a Nexus) | No | Designed (48cff7): `signal-curriculum` with skill-derivative kinds | Skills: generating, deploying and reseeding them (9993b5, 8904b1) |
| Psyche Nexus | `psyche`, `signal-psyche`, `meta-signal-psyche` | No. ARCHITECTURE.md: "intentionally empty quick-new MVP component scaffold"; no contract is defined | None | Psyche (and mind) logging (88475f) |
| Field Nexus | `field` (read-only inventory scripts), `field-clj` (commits); no `signal-field` | No | None | System monitoring and queries. The living left open whether transcript functionality goes here (b80e55) |
| Book nexus | none | No | None | I found nothing on a book nexus, either as a repository or in any vision. |

Mentci (a UI Nexus with a web front, 1b8ac0) is about displaying content and is listed only for completeness.

## 2. The living's words

Flow Nexus:

> We need proper messages and proper flow creation, which is controlled by a flow nexus that maybe uses some [Clojure] tools internally so this Rust code can call these [Clojure] tools, I guess by Nix paths.

-- psyche, STT, 2026-09-29, c64ee3 (`flows/c64ee3/vision/flowNexus.md`).

> We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it. In the last response, possibly we should also send that to Flow, and then Flow would send it to the reaping agent to decide if that's the end of Flow and if it should be reaped.

-- psyche, relayed verbatim by Field Astra cf3553 to b81560, 2026-09-19. Status there: a proposed `Report.EndOfTurn.{ … }` operation, "not implemented".

> Everybody, we're going to standardize the report. It's just the last response. That's what we're using: the transcript. Try using the transcript and making references to the transcripts in the logs. That's what the logs are: they're just references to transcripts. You find a way to address the transcript efficiently and make a tool to acquire that data quickly. That's what the Flow Nexus needs to do.

-- psyche, spoken, 2026-09-18, b05237.

> Essentially we want to avoid polling, which means we're going to make this hook-based. When an order comes in, this will be controlled by Flow obviously.

-- psyche, STT, 2026-09-30, 7328f4 (about harness-upgrade orders).

> Basically, Flow is in charge of herder. I shouldn't interact with it directly.

-- psyche (af762b, 056f6d and others).

> ... this brings me to the fact that the word flow is kind of getting overloaded if we have a flow nexus.

-- psyche, dictated, 2026-08-19, e06e4c (about the name).

On transcripts as a domain:

> obviously another nexus. But we might want a small clever tool to help search those files more efficiently for now.

-- psyche, typed, 2026-08-19, e06e4c, "answering whether the harness transcripts belong to the flow Nexus".

> The transcript component is misimplemented. We need to make a nexus out of it and use datom syntax with the CLIs.

> It needs to be a nexus with Signal and Datom syntax only.

-- psyche, typed, 2026-09-16, 48cff7.

> I don't think the transcript tool does what we want ... but we could develop that and let Flow use it. It's a different functionality and lets us rebuild it without rebuilding Flow if we don't change the signal.

-- psyche, STT, 2026-09-21, 1b8ac0.

> We could even put all the transcript stuff in there, unless we keep that as a separate nexus, which the field could also access to expose the same functionality or to enhance its own. Here we see the concept of either reusing another Nexus or merging a function of it, basically aggregating or splitting up functionality.

-- psyche, spoken, 2026-09-20, b80e55 (about the Field Nexus).

> Start using your transcript more and then develop the field tool to extract transcript, or maybe even its own.

-- psyche, STT, 2026-09-26, 93ba9f.

On the transcript as the place content is owned:

> Actually, the report becomes everything is in the transcript. We don't want to make files anymore. We don't want to avoid making files and move things into Nexus databases that are efficient.

-- psyche, typed, 2026-09-17, 9993b5. The log notes the double negative as a speech stutter.

> What do you mean the prompt is committed? It's in your transcript. / Why would you spend twice as many tokens for the same thing?

-- psyche, typed, 2026-09-29, 183ae0.

On the book pipeline:

> Let's focus on hooks and using hooks to do an event-based infrastructure in terms of sending notifications that there's a certain kind of message that has landed in the transcript somewhere. Maybe that means it needs to be made into a book, or maybe it means that there's an update to an existing book. We can do all of this without requiring the flow to make tool calls because the hook will just pick up the output and create actions based on that.

-- psyche, typed, 2026-10-01, 7328f4.

> ... I'd like to get a Psyche Sonnet flow going ... Obviously be registered with the messenger

-- psyche, typed, 2026-09-29, to bea031.

On the nexuses in general:

> They're the nexuses. Psyche Nexus is going to replace how we log Psyche and Mind. Mind Nexus is going to replace how we log the Mind and the field ...

-- psyche, relayed by e51411, 2026-09-25 (88475f).

Tension to raise with the living: the e06e4c record says transcripts belong to "obviously another nexus", while the b05237 record says addressing transcripts is "what the Flow Nexus needs to do". The 1b8ac0 record ("develop that and let Flow use it") can be read as joining the two: a separate transcript component that Flow uses. That reading is mine, not his.

## 3. The fork, without a verdict

Flow Nexus.
- Fits:
  - The hook is a lifecycle event at the end of a turn, and the cf3553 hook record names the Flow CLI as its receiver.
  - Flow already identifies the calling process (`ResolveCaller`), so it can say which flow wrote the block.
  - Flow can start the Sonnet flow or deliver to it through `Deliver`.
- Does not fit:
  - Flow's claimed domain is flow lifecycle and pane writes. Book content is neither.
  - The e06e4c record puts transcripts in another nexus.
  - The living has already called Flow "overloaded" as a word.
  - No current operation takes content.
- Operation it would need: a new ordinary verb, for example `Report.EndOfTurn.{ … }` (the 2026-09-19 proposal) replied `Reported`. `Present` is not usable as the verb because its past tense, `Presented`, is already a delivery grade in Flow.

Transcript Nexus.
- Fits:
  - The block is transcript content, and the living has ruled that the transcript is the record ("It's in your transcript").
  - The designed anchor-bounded `Block` is the same shape as the start/end markers.
  - The hook could send a pointer instead of a copy, which avoids the "twice the tokens" problem.
- Does not fit:
  - The Nexus is not built; only a Python shim exists.
  - Its designed domain is reading. Routing to Sonnet and making books sit outside it, so a second hop to Message or Flow would still be needed.
- Operation: a write-side verb that records a marked block by session and range, for example `Mark.{ session start end }` replied `Marked`. Sonnet would later read it with `Block` (replied, for example, `BlockShown`). Both verbs are illustrations; neither is designed.

Message Nexus.
- Fits:
  - It runs today, though only as next.
  - Taking text to a flow is its domain.
  - Psyche Sonnet is to be "registered with the messenger".
- Does not fit:
  - Sending the block copies transcript content into a letter.
  - The sender is resolved from the peer through Flow's `ResolvePeer`, and a hook process may not resolve to a flow.
  - The metadata block (the title) has no typed place in `Send.{ [ recipients ] Priority Content }` beyond the text.
- Operation: `Send.{ [ <Sonnet flow> ] Soft Text.«…» }` replied `Submitted`. `hm-send` would be the hacky equivalent the living wants retired.

Curriculum Nexus. Its domain is skills, not books, and it is not built. The only link is that a book could seed a skill. Its operation would be unspecified.

Psyche Nexus.
- Fits: Sonnet's aspect is knowing the psyche, and the living described the questions pipeline as "like how we log psyche".
- Does not fit: the block is the machine's presentation, not the living's words, and the repo has no contract.
- Operation: none to name.

Field Nexus. The living left open whether transcript functionality is merged into Field (b80e55, 93ba9f). It has no Nexus and no contract.

New book nexus. There is no record of one. The domain would be books: create one, revise one, record the living's comments. The operation would be, for example, `Submit.{ title block-pointer }` replied `Submitted`. The living has not spoken on this option.

## Sources

- /git/github.com/LiGoldragon/flow/README.md; /git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos at bookmark s1-e167d8 (7.0.0, the rev `flow` pins); /git/github.com/LiGoldragon/meta-signal-flow/ethos/signal.ethos at s1-e167d8 (11.0.0)
- /git/github.com/LiGoldragon/message/README.md; /git/github.com/LiGoldragon/signal-message/ethos/signal.ethos at the 7.0.0 rev `message` pins
- /git/github.com/LiGoldragon/messenger-clj/README.md
- /git/github.com/LiGoldragon/transcript/README.md
- /git/github.com/LiGoldragon/psyche/ARCHITECTURE.md
- /git/github.com/LiGoldragon/field/README.md, /git/github.com/LiGoldragon/field-clj/README.md, /git/github.com/LiGoldragon/curriculum-deploy/README.md
- `systemctl --user list-units` and `which` on 2026-10-01, giving service and PATH state
- /home/li/primary/flows/c64ee3/vision/flowNexus.md
- /home/li/primary/flows/cf3553/vision/operational-finalResponseLifecycleHook.md; /home/li/primary/flows/b81560/vision/operational-reapingOnRefreshAndFlowEndHook.md
- /home/li/primary/flows/b05237/vision/operational-reportIsTranscript.md
- /home/li/primary/flows/7328f4/vision/hooks.md, /home/li/primary/flows/7328f4/vision/books.md
- /home/li/primary/flows/e06e4c07/vision/flowKnowledge.md, /home/li/primary/flows/e06e4c07/vision/archive-flowDaemon.md
- /home/li/primary/flows/48cff7/vision/transcriptNexus.md, /home/li/primary/flows/48cff7/vision/skillKindsTaxonomy.md, /home/li/primary/flows/48cff7/vision/mind.md
- /home/li/primary/flows/1b8ac0/vision/transcriptTool.md, /home/li/primary/flows/1b8ac0/vision/mentciWeb.md
- /home/li/primary/flows/b80e55/vision/fieldNexusSystemQuery.md; /home/li/primary/flows/93ba9f/vision/fieldTool.md
- /home/li/primary/flows/9993b5/vision/transcriptOverFiles.md, /home/li/primary/flows/9993b5/vision/curriculumNexus.md
- /home/li/primary/flows/fe945a/vision/transcriptOverFiles.md, /home/li/primary/flows/fe945a/vision/psycheSonnet.md, /home/li/primary/flows/fe945a/log.md
- /home/li/primary/flows/88475f/vision/nexus.md
- /home/li/primary/flows/6997eb/vision/pipeline.md, /home/li/primary/flows/6997eb/vision/presentation.md, /home/li/primary/flows/6997eb/vision/questions.md
- /home/li/primary/flows/af762b/vision/operational-flowOwnsHerdr.md
