# Flow Nexus implementation dossier

## 0. What is where

**Repository.** The canonical clone is `/git/github.com/LiGoldragon/flow`, with origin `github.com/LiGoldragon/flow`.
- Its local `main` is stale at `6043478`, ahead 1 and behind 59.
- `origin/main` is `a0ca88`, dated 2026-10-26, workspace version 0.40.0.
- `/home/li/primary/flow` is a stale detached, dirty checkout of 0.9.0 at `28a78d`. Ignore it.
- Crates are `flow`, `flow-meta`, `flow-nexus`, `flow-ethos`, `flow-defaults` and `flow-native`.

**Wire contracts.** `signal-flow` is pinned at `ddf27d` (ethos at `ethos/signal.ethos`, 576 lines) and `meta-signal-flow` at `c58cef` (397 lines). I read both from archives of those revisions in `/git/github.com/LiGoldragon/{signal-flow,meta-signal-flow}`. In the citations below, `sf:` means the signal-flow ethos and `msf:` the meta-signal-flow ethos.

**Deployed.**
- `command -v flow` is `~/.nix-profile/bin/flow`, which resolves to `/nix/store/nygs0aj2rb0caz6bdfjqm89h3qm1imm4-flow-0.40.0/bin/flow`. It reports `flow 0.40.0`.
- The CLI source is `/nix/store/rp2rih03qg0yb0prw8gvg4afyi0vbv45-source`. Every code file there is byte-identical to `origin/main` `a0ca88`. Only docs, `capsule/`, `launcher/` and `checks/` are stripped from the store copy.
- The running Nexus is the transient unit `flow-nexus-040.service`, started 2026-10-28 10:38. It runs `flow-0.40.4` (`/nix/store/9sjii9ynba06nbslwgfki4y83fzax98f-flow-0.40.4`) from commit `230b3b`, the branch `origin/queue-emergency`, on store `~/.local/state/flow-040/flow.sema`.
- `230b3b` is `origin/main` plus 4 commits (0.40.1 to 0.40.4). They change only `claude.rs`, `sending.rs`, `waking.rs` and tests.
- The persistent `flow-nexus.service` is failed. It points at 0.39.0, and `flow-nexus`/`flow-meta` on PATH are also 0.39.0.
- A newer integration branch, `origin/main-integration-851681` (head `be8115`, release 0.40.6 `29486a`, 2026-10-29), is unmerged. I did not read it.

**Citation form.** "main" means `origin/main` `a0ca88`, with paths under `crates/flow-nexus/src` unless noted. "dep" means `230b3b`. I mark every place where dep differs from main.

## 1. Hooks and configuration

**Hooks.**
- `/home/li/primary/.claude/settings.json` holds only `worktree.bgIsolation`. `settings.local.json` holds only three Bash permission allows. Neither calls Flow, and there is no hook script under `.claude`.
- Flow writes the hook into each Claude flow it launches. `herdr/launch.rs:433-478` installs `flow-hook` on SessionStart, PostToolUse, UserPromptSubmit, Stop and SessionEnd.
- `crates/flow/src/hook.rs:1-35` turns each event into a `Report.{ FlowId Event }` datom and hands it to the `flow` CLI.
- Codex flows are fed by app-server notifications: `codex_turns.rs:9-12,118-120` (turn started, turn completed, thread status changed).

**Configuration as deployed.** I read it with `flow-meta Configuration` on 2026-10-29, a read-only query.
- Models:
  - Psyche: Primary `claude-fable-5-1`, Secondary `claude-opus-5-5`, Tertiary `claude-sonnet-5-5`, Quaternary `claude-haiku-5-5`.
  - Mind and Field: Primary `gpt-6-astra`, Secondary `gpt-6.1-sol`, Tertiary and Quaternary `gpt-6-luna`.
- Refresh thresholds: Fable 280000, the other Claude models 200000, every OpenAI model 150000.
- Nexus settings: lease 60, MetaAspects `[Psyche]`, and the Curriculum socket `/run/user/1001/flow40-rt/curriculum/curriculum.sock`.
- Harness profiles:
  - Claude interrupt is `[esc esc]` and submit is `[enter]`.
  - Codex interrupt is `[esc]`.
- Per-metaflow declarations and leave-outs for every Psyche, Mind and Field address. Core addresses are `Maintained`.

**Where the configuration comes from.**
- The deployed `initialize-declared-flow` script (`/nix/store/y9a54lcjlgixjky02bgy8g77nrk46d2h-initialize-declared-flow`) sends `Configure.*` datoms at ExecStartPre.
- It builds the metaflow declarations from the EDN snapshot `/nix/store/flcfdsaf7ny4zc9n3fzh21vc5bkp0kgg-source/config/main-flow`, using a babashka script.
- Primary commit `983439d12` (2026-10-28) deleted the EDN in favour of "Flow's datom configuration". I did not find where that datom configuration now lives.
- The only datom configuration file in the Flow repo is `capsule/configure.datom`, for the test capsule.
- `/home/li/primary/config/` holds only `context-refresh.json` and `model-display-names.json`, which are not Flow configuration.

## 2. What Flow does today (verified in code)

**Ethos files.**
- Present:
  - `flow-ethos/ethos/library.ethos` (96 lines) and `delivery.ethos` (10 lines).
  - `flow-nexus/ethos/{operation 130, memory 14, library 4, startup 20, curriculum 69, starter 147, send_tool 105, landing 106}.ethos`.
  - The Signal ethos lives in the signal-flow repo and the meta Signal ethos in the meta-signal-flow repo.
- `flow-nexus/build.rs:1-30` generates Rust from the Nexus ethos files and asserts the committed generated modules equal a fresh generation.
- The `memory.ethos` root declares only `LaunchOutcome` and `Replacement`. The real Memory families are hand-written in `store.rs`: table names at `:77-109`, the state record at `:1379`, and the `sema_engine` store at `:60`.
- There is no Signal/Operation/Memory split for Flow's own state beyond that, and the library is not split per part.

**Ordinary wire (sf:)**
- Queries (`:20-44`): Start, Refresh, ResolveRecipient, Stop, Replace, LaunchStatus, Observe, ResolveCaller, Report, Lock, Bind, Identify, Deliver, Release, Current, Metaflows, IdentifyThread, Send, ObserveSends, ObserveSender, DeliverAll, **Launch.{ Address Remembering InstructionPrompt }** (`~:238`), BindSeat (`:239`).
- Responses (`:45-82`): Started, LaunchPending, StartAmbiguous, Refreshed, RecipientResolved, Stopped, Listed, the various Rejected variants, Replaced, LaunchInspected, CallerResolved, AgentObserved, Reported, Locked, Bound, Identified, SendAccepted, SendsObserved, SendChanged, Drained, Woken, Released, Current, Refused, Sent and Failed.
- `Refusal` (`:511-527`) includes `Unidentified.Process`, `NoneAbove`, `Taken.Address`, `TopicRefused` and `NotSendServer`.

**Meta wire (msf:)**
- Queries (`:183-202`): Configure, ConsumeReset, RegisterFlow, MetaBindExisting, Retire, Deliver, Vet, Command (Compact or Interrupt), ResolvePeer, ReadEvents, ReadQueueDeliveries, ReadSendOutcomes, ObserveLegacyArchive, ResolveQueueDelivery, Inspect, Rebind and Withdraw.
- Configure payloads (`:278-284`): Models, Thresholds, LeaveOuts, Nexus, SendServers, Metaflows and Investigation.

**Store (Memory).**
- The store is `sema_engine` on redb, with `FLOW_SCHEMA_VERSION` 2 (`store.rs:231`).
- Record families are: flows, native owner proofs, state, configuration, Herdr routes, launch panes, launch attempts, launch outcomes, replacements, roles, quarantined attempts, metaflows, metaflow processes, metaflow locks, the meta configuration tables (nexus, model, threshold, investigation, leave-out, metaflow, send-server), compactions, context sizes, deliveries, pane leases, address holds, send calls, flow events, send outcomes, launch cleanup, successor intents, queue-delivery counters, requests and attempts, logical-delivery tables, opened threads and simplified replies.
- Definitions are at `store/*.rs` and `store.rs:77-109`.

**Launch composition.**
- Composition (`composition.rs:1-14`):
  - The system prompt is the verified text of spirit and intent, then an identity section: Address, Flow ID, native binding, predecessor and remembering (`:181`).
  - The first USER message is the USER text, the remembered flows' records, then the brief. It is split into numbered parts when it does not fit one message.
  - A Simplified flow keeps its USER modules in its own system prompt.
- The Psyche core Primary alone reads a presentation prompt from the env `FLOW_CORE_PRESENTATION_PROMPT` (`:72-90`).
- Modules come from the Curriculum Nexus over a socket (`context.rs:1-23`). Flow holds only module identities.
- Model per layer and aspect comes from the Configure.Models table (`store.rs:1134`).
- **Effort is hardwired**: medium, but low for an OpenAI Quaternary (`sending.rs:409-416`).
- Power per layer is hardwired (`waking.rs:126-132`).
- Leave-outs are a typed list that becomes harness flags.
- Configuration merge order, as the init script sends it: Nexus, Models, Thresholds, Investigation, Metaflows, SendServers, then per-metaflow leave-outs. A Start's leave-outs replace the metaflow default; `None` takes the default (sf comment on `LaunchProfile`).

**Metaflows, topics and flow ids.**
- `Address { Aspect Topic Layer }`, `Recipient [Address Up]` and `Metaflow { Address State[Awake.FlowId Asleep] Past Queue }` are at `flow-ethos library.ethos:35,36,50-53`.
- Topic is a `String`. It is checked as an uncapitalized ASCII camelCase identifier at `launching.rs:97-111,146`, and again in the send tool (`send_tool.rs:417`) and in Configure (`msf:293`).
- A Primary is refused unless its Secondary is Awake (`launching.rs:~120-160`, `NoSecondary`).
- Flow ids come from an external `flow-id` helper that writes a claim marker `.{id}.flow-id` (`herdr/launch.rs:587-680`). The alias is the first six characters of the session identity (`herdr.rs:1084`).
- For Claude, Flow chooses the native session id and claims the id before the harness runs. For Codex, Bind claims it from the reported session (`operation.ethos:6-14`).
- The title is the datom `{ Aspect topic Layer FlowId }` and requires the six-character id (`title.rs:1-17`).

**Queueing, waking and delivery.**
- A message is `Message.[HardAbrupt Soft MiddleAbrupt].Request` (`delivery.ethos:5-7`). The request kinds are `Order Question Psyche Psyches Result Notice` (`library.ethos:23-30`). `Delivery` is `[Queue Wake]` (`delivery.ethos:8`).
- The message kind never decides waking; the sender's `Delivery` does (sf comment `:14-16`).
- An abrupt message for a live pane is typed under a pane lease. If the pane refuses it, it is queued instead (sf comment `:16-17`; `delivery.rs:458,491`, `sending.rs:205-265`).
- A Wake of an Asleep metaflow starts a fresh flow that carries the whole queue, oldest first, in its first prompt (`waking.rs:45`, `wake` at `:1657`).
- Drain on **main** hands over the oldest request, one at a time (`waking.rs:~1796`). Drain on **dep** hands the whole queue over as one payload (dep `waking.rs:1351,1819-1893`, `park_cohort :2009`).
- Queue ordering relies on a lock: `waking.hold` (`waking.rs:1475`) and `Locked` (`sf:511`).
- A flow past its refresh threshold is given no new message (`waking.rs:1750`, `delivery.rs:216-218`, `sending.rs:869`).
- Since 0.40, a Send is never refused for route or seat state (`UPGRADES.md`).

**Refresh thresholds and reaping.**
- Only one threshold exists per model: `Refresh` (`msf:249,279`; `store/context.rs:130-196`).
- The context size is recorded when the Stop hook fires (`operation.ethos` `Record.Context`).
- `refresh_due` (`waking.rs:2462`) leads to a successor started first via Replace, then the predecessor reaped (`:2515-2527`, `refresh_successor_first :711/2243`). That happens when the metaflow is Maintained or the queue holds a Wake. Otherwise the harness is closed at rest and the metaflow is left Asleep (`:2528-2539`).
- An outside `Refresh` takes the metaflow lock and writes no handover (`waking.rs:1440-1530`).
- An OnDemand metaflow with nothing queued closes its harness once it is resting (`:2548-2557`). A Maintained one stays awake.
- Compact is refused below the threshold, or when unmeasured or unconfigured (`store/context.rs:173-196`; `delivery.rs:247`). Compactions are detected and logged as warnings (`compacting.rs:1-22`).

**Herdr and the Capsule.**
- Herdr is driven through the `herdr` CLI (`herdr.rs:158`, `herdr/*.rs`), with one pane per flow.
- Codex is driven through its app-server (`codex.rs`).
- The "capsule" is a babashka test script, `capsule/flow-capsule.clj` (762 lines on main, not in the store source). It has its own runtime directory, store, Herdr session `flow-testing`, a Curriculum Nexus, an empty source root and a clean environment. It is not a Flow component.

**Seat binding and caller identification.**
- The caller is identified from the kernel's `SO_PEERCRED` plus the Herdr pane environment. The pane must hold exactly one routable flow, and the live Herdr snapshot must still show its binding (`caller.rs:1-22`).
- `BindSeat` (`sending.rs:~631-720`) returns `Refused(Unidentified)` for a missing or dead peer, a pane that is not found, or an unknown harness or session. I read this in code; I did not call it.
- Meta socket authorization is by aspect: the caller's aspect must be in `MetaAspects`, which is deployed as `[Psyche]` (`peer.rs:9,61-87`; `msf:364-365`).

## 3. What the code lacks against the designed features

| Feature | Status | Witness |
|---|---|---|
| Capsule semi-sandbox (credentials-only copy, recreate the rest, encrypted volatile key) | Not found. Only a test-script capsule exists, with its own runtime directory, store and Herdr session. | `capsule/flow-capsule.clj:1-25` |
| Ephemeral flows (ceiling 300k/250k) | Not found | grep `ephemeral`: only Codex thread flags (`codex.rs:349,1066,1443`) |
| Heartbeat and reminders (`Remind`) | Not found | `grep Remind` hits only the attribution leave-out |
| Simplified flows | Partly built. Wire type and composition exist, but 0.40 removed the tool restriction. | `sf:318`; `composition.rs:556-568`; `UPGRADES.md` |
| Module hash checks | Partly built. Flow verifies the composer's payload and per-module SHA-256 (rendered text vs Curriculum provenance), not source-repo hashes. | `context.rs:226,248-251` |
| Three-word flow ids | Not found | no word form in Nexus, signal or title |
| `remembering` field on Launch | Built, but `Predecessors` and `Custom` only. No `Open`. | `sf:~238,289` |
| kameo actors | Not found. Zero hits in `Cargo.lock`. The Nexus uses a dispatch-gate mutex and `thread::spawn`. | `Cargo.lock`; `recovery.rs`, `codex.rs`, `delivery/lease.rs` |
| Signal/Operation/Memory ethos split | Partly built. Signal and meta Signal are in separate repos. Operation (130 lines) and a Library exist. Memory root holds two records only. | see section 2 |

## 4. Per-line status: vision:flow (`psyche-context` `vision/flow.md`, c386f58)

Each statement is quoted by its opening words, since many are long paragraphs. The line numbers are the module's. Status is built, partly built (the part given) or unbuilt.

| Line | Statement | Status | Witness |
|---|---|---|---|
| 8 | "The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt." | built | `composition.rs:1-14`; `Configure.Nexus` source root |
| 11 | "Flow is the Nexus that manages flows… Flow holds the lock on flows." | built | `waking.rs:1475`; `store.rs:94` metaflow locks |
| 13 | "Flow is for starting flows cheaply… taken down as easily as it is started." | built (mechanisms) | Start, Launch, Refresh, Stop, Replace (`sf:20-44`) |
| 15 | "A flow runs one model… not always a language model." | unbuilt (harness kinds are Claude and Codex only) | `library.ethos` `HarnessKind` |
| 17 | "The Capsule is the component that makes where a flow runs… semi-sandbox… encrypts…" | unbuilt (a test script only) | `flow-capsule.clj:1-25` |
| 19 | "Herdr is one backend of the Capsule… the backend may be exchanged." | partly (Herdr used; no backend abstraction, Herdr ids in the wire) | `herdr.rs:158`; `sf:HerdrPaneId` |
| 21 | "Flow manages metaflows… { Aspect Topic Layer }… The default topic is core…" | partly (address and metaflow built; core is only the Maintained default) | `library.ethos:35,50-53`; `store/metaflow_declaration.rs:6,53` |
| 23 | "A topic is an open enum…" | partly (String, camelCase checked, no open enum) | `launching.rs:97-111` |
| 25 | "Psyche, Mind and Field… go under one: the metaflow." | built | `library.ethos:34-53` |
| 27 | "A topic lives on… judgment, made by a small model; a topic is bound to its belief modules…" | partly (the declaration binds modules and idle flows are closed; no small-model wake judgment) | `msf:276`; `waking.rs:2548` |
| 29 | "A metaflow sleeps…" | built | `waking.rs:2548-2557` |
| 31 (name) | "A topic's name is a camelCase identifier… kept exactly as written." | built | `launching.rs:97-146`; `msf:293` |
| 31 (id) | "A flow's id is the hash of the harness's session id, six characters, lengthened when two collide" | partly (id comes from the external `flow-id` helper; collision lengthening not seen in the Nexus) | `herdr/launch.rs:592-680` |
| 31 (long) | "Long term, the flow id is also written in three words" | unbuilt | none |
| 31 (choice) | "Where the harness lets Flow choose the session id, Flow chooses it…" | built | `operation.ethos:6-14` |
| 31 (caller) | "Every call to Flow is identified by the calling process… a flow refreshes itself safely." | built | `caller.rs:1-22`; `sf:522` |
| 33 | "In the chat a flow is named by its metaflow…" | outside Flow's code (the title still carries the id) | `title.rs:1-8` |
| 35 | "A request… one of a closed set of types, each with its waking effect" | partly (kinds exist; waking effect comes from the sender's Delivery, not the kind) | `library.ethos:23`; `sf` comment `:14-16` |
| 35 (Message/lock) | "Message asks Flow to send… Flow owns the lock and the delivery, answers sent or queued, and Message subscribes…" | built | Send, ObserveSends (`sf`), `MessageNexusPath` config |
| 35 (asleep) | "A metaflow asleep is woken… receives its whole queue, oldest first, in the first prompt" | built | `waking.rs:45` |
| 35 (waking kinds) | "…a result or a notice waiting there until a waking" | unbuilt | the sender's Delivery decides |
| 35 (refresh) | "a metaflow under refresh or waking queues what arrives…" | built | `waking.rs:1440-1530` |
| 35 (start) | "A metaflow a request needs is started whether or not it is running…" | partly (a Wake starts a declared, Asleep metaflow; an undeclared one is refused) | `sf` `StartRejection.Undeclared` |
| 37 | "A flow woken for a metaflow is almost always a fresh flow, an old one only when…" | partly (fresh built; resuming an old one not found) | `operation.ethos` Wake |
| 39–40 | "What has been queued for an idle metaflow, the vision touching its topic among it…" | partly (queue injection built; vision routing into queues not found) | `waking.rs:45` |
| 42 | "Flow exposes everything from the harness, the bare input…" | built | Start, Stop, Send (`sf`) |
| 44 | "The flow that finishes messages the flow that needs to know." | outside Flow's code (flow behavior) | none |
| 46 | "A flow gives a presentation…" | partly (Psyche core Primary only, via an env-file prompt) | `composition.rs:72-90` |
| 50 | "A Nexus component decides the system prompt and everything about a launch…" | built | `composition.rs`; leave-outs (`sf:315`); `lean.rs` |
| 54 | "A layer is Primary… the layer decides the model. A launch names… the Nexus composes the prompt from its module registry." | partly (model per layer built; modules come from the declaration; the registry is the Curriculum's) | `store.rs:1134`; `context.rs:1-23` |
| 56 | "Flow's configuration holds, for each metaflow, its purpose and the records of the living it rests on…" | built | `msf:276` |
| 58, 60–64 | "A fresh flow's first prompt carries the raw psyche… spirit and intent sit in the system prompt." | built | `composition.rs:1-14` |
| 66 | "…all loaded at its start… so that its start is one model call." | built | `composition.rs:1-14` numbered parts |
| 68 | "A simplified flow…" | partly (wire type built; no regular-tool restriction since 0.40) | `sf:318`; `UPGRADES.md` |
| 70 | "A flow is specified whole, in Datom… The flow ethos holds the specification." | unbuilt (no ethos of system prompt, default modules and variations) | n/a |
| 72 | "Short term, the Secondary starts first, then its Primary." | built | `launching.rs:~120-160` |
| 74 | "Long term, a Primary is a simplified flow…" | unbuilt (long term) | n/a |
| 76 | "To the Nexus, a module's location is its registry entry." | partly (Flow holds only identities) | `context.rs:1-23` |
| 78–80 | "The system prompt is composed of modules of several types… not passed down to its subagents." | unbuilt (leave-outs exist; no anatomy study, no subagent-private part) | n/a |
| 82 | "Every flow has a topic… A flow's title is one datom struct…" | built (title); core default not applied automatically | `title.rs:1-8` |
| 84 | "Flow refuses a request that leaves those routes." | unbuilt (0.40 removed route refusal) | `UPGRADES.md` |
| 88 | "Long term, every module… checked by its hash… short term, no check is made." | partly (see section 3) | `context.rs:226,248-251` |
| 92–94 | "The flow repository holds the machinery… Every belief module lives outside it…" | built | Curriculum composer |
| 98–100 | "Reaping belongs to the refresh event…" | built | `waking.rs:2515-2527`; stopped flows refused in resolution |
| 102 (hooks) | "Every harness event reaches Flow through the harness's hooks calling the Flow CLI…" | built (Claude via hooks, Codex via app-server events) | `herdr/launch.rs:433-478`; `codex_turns.rs:118` |
| 102 (marked block) | "a marked block landing in a transcript becomes an action, a book among them" | unbuilt | not found |
| 102 (idle refresh) | "a flow past its context threshold is refreshed as it goes idle" | built | `waking.rs:2462-2539` |
| 102 (poller) | "A poller that must exist is registered and reported." | not found | n/a |
| 104 | "A flow is refreshed when its context passes its model's threshold… OpenAI lower than Claude." | built (single Refresh threshold; deployed 280000, 200000, 150000) | `store/context.rs:130-196` |
| 106 | "A flow refreshes before compaction; a compaction is a refresh that was missed." | partly (compaction detected and warned) | `compacting.rs:1-22` |
| 108 | "A flow that keeps working without being given more work may compact. Its compaction raises a warning, and a flow investigates…" | partly (warning built; the Investigation address is configured; launching the investigation not verified) | `compacting.rs:1-22`; `msf:284` |
| 110 | "An ephemeral flow is a continuous job flow…" | unbuilt | n/a |
| 114 | "An abandoned, duplicated or superseded flow is closed, archived and deregistered." | partly (Stop, and Retire that keeps the row; Codex thread archived on a refused start) | `msf:188`; `operation.ethos` |
| 118 | "Herdr is the third-party terminal workspace every flow runs in…" | built | `herdr.rs`; `caller.rs`; pane lease in `delivery.rs` |
| 122 | "A build of Flow is tested in a testing capsule of its own…" | partly (the capsule exists; its config disables Codex seats) | `capsule/configure.datom` |
| 124 | "The stable Flow keeps running while variants are tested." | built (the 0.40.4 service runs beside a separate store) | `flow-nexus-040.service` |
| 128 | "A permission prompt reaching the living is a launch failure." | not found | n/a |
| 132, 134 | "The heartbeat reminds every flow…", "The heartbeat reaches only a flow for which something changed…" | unbuilt | n/a |
| 136 | "The number of running flows is kept low: a topic flow no longer used is retired." | unbuilt (Retire exists; no policy) | `msf:188` |
| 140 | "A flow can be restarted without being woken… A restart meant to leave the flow asleep is done from outside…" | built | `waking.rs:1440-1458`; `UPGRADES.md` |
| 144 | "A refresh carries the flow's important presentations and illustrations, the raw psyche given to it, and the basic skills." | partly (raw records remembered through the Curriculum; presentations and illustrations not found) | `waking.rs:1447-1453` |

## 5. Per-line status: "Flow, whole" (`flows/30fc30/books/flow-whole.md`, 1118 lines)

The sentences listed are the proposed `+` lines of each proposal. Retained module lines (book lines 9–149) are the section 4 table. The ethos and datom blocks in the book are proposed types, so I compare them as shapes.

**P1 What Flow is** (`:155-199`)
- "Flow is the Nexus that starts, names, tracks, refreshes and ends flows… Flow holds the lock…" is built (same witnesses as section 4, lines 11 and 13).
- "Starting a standard flow is one short call." is partly built: `Launch.{ Address Remembering Brief }` and `launcher/flow-start.mjs`.
- "A flow is one run of a harness… A main flow has an address; a subflow has a flow id and no address." is partly built; I did not find subflow handling in the Nexus.
- "A metaflow holds its declaration, its queue, its past flows and its current flow, if any." is built (`library.ethos:50-53`, declaration tables).
- "A topic lives on… The default topic is core… a topic no longer touched is retired." is partly built; the retirement policy is unbuilt.
- The block `QueueEntry.{ Delivery Request }` is partly built: the main shape is `{ LogicalDeliveryId SentBy Delivery Message }` (`library.ethos:44`).

**P2 Names** (`:229-237`)
- "A topic is an open enum: core is its fixed variant… camel ID." is partly built (String, camelCase checked).
- "A flow id is six characters, the earliest random part of the harness's session id, lengthened when two collide…" is partly built (see section 4, line 31).
- "…Flow chooses it before the flow starts… Either way the flow reads its id in its first prompt and its environment" is built.
- "Every pane, tab and title that represents a flow is one datom of its address and id" is partly built: the title is built (`title.rs`); pane and tab labels are set, but I did not verify their form.
- "Every call to Flow is identified by the calling process: a caller is a flow, resolved to its address, or a process Flow does not know." is partly built: `Caller{ FlowId Aspect PowerLevel ModelName }` and `CallerUnknown` exist, but no process-only caller shape.
- "In the long term the id is also written as three camelCase words" is unbuilt.

**P3 Starting a flow** (`:291-301`)
- "A metaflow is declared in Flow's configuration, as datom: address, system and first-prompt modules, purpose, left-out harness modules, continuity, default task, remembering" is partly built. `ConfigureMetaflow` (`msf:276`) has Address, SystemModules, UserModules, FlowKind, ToolSet, Continuity, Purpose and Records. Leave-outs are a separate `ConfigureLeaveOut`. Default task and remembering are not in the declaration.
- "A launch names an address, a remembering and a brief" is built (`sf:~238`), with `Open` missing.
- "Flow composes the system prompt whole, replacing the harness's own: spirit and intent, with the flow's address, model and id." is built (`composition.rs:1-14,181`).
- "The first prompt is one message… the belief modules of every other kind, the raw vision and notion records the remembering names, the open beads of the address, then the brief." is partly built; open beads are not found.
- "A flow launched without a brief has its declaration's default task." is unbuilt.
- "A main flow is started with its subflow tool and every tool its declaration leaves in; Flow limits nothing the configuration does not name." is built (0.40, `UPGRADES.md`).
- "A permission prompt reaching the living is a launch failure." is not found.
- "the layer and the aspect decide the model and its effort through Flow's configuration" is partly built: model configured, effort hardwired (`sending.rs:409-416`).
- "A Primary is started after its Secondary." is built.

**P4 Requests and the queue** (`:383-391`)
- "Everything the machine puts into a flow's prompt is one datom." is partly built; rendering is in `delivery/body.rs`, which I did not read in detail.
- "A request is its sender, as an address, and its content, headed by its kind: Order, Question, Result, Notice, or Psyche." is partly built: the kinds exist, but the request is `{ SentBy… Message }` and carries a `LogicalDeliveryId` (`library.ethos:23,44`).
- "The living's words are the only text in a transcript that is not datom… a tool finds them" is unbuilt.
- "A request names its recipient by address, or Up" is built (`library.ethos:36`; `NoneAbove`).
- "Queue… Wake… Abrupt interrupts… answered Sent or Failed, never Queued." is partly built, and the Abrupt part contradicts today's behavior. `Delivery` is `[Queue Wake]` and abrupt is a message priority; a refused abrupt pane queues instead (`sf` comment `:16-17`).
- "Every request is queued for its metaflow… delivered whole, oldest first, as one datom, a vector… in one turn" is partly built. Main is oldest first, one at a time. Dep is the whole cohort as one payload (dep `waking.rs:1819-1893`); vector datom form not verified. Idle-at-once and sleeping-first-prompt are built.
- "A metaflow being refreshed receives nothing more; its queue waits." is built.
- "An Order, a Question and Psyche wake a sleeping metaflow; a Result and a Notice wait" is unbuilt.
- "Flow refuses no route" is built (0.40, `UPGRADES.md`).
- "Flow is the one writer into a pane… Message sends through Flow… fall back to typing… through Herdr" is partly built: the pane lease serialises writers (`delivery.rs:221`, `delivery/lease.rs`); the Message-to-Flow route exists (`MessageNexusPath`).

**P5 Sleeping, waking and refreshing** (`:450-477`)
- "A Maintained metaflow, core among them, is kept awake… an OnDemand metaflow sleeps as soon as its turn ends with nothing queued." is built (`waking.rs:2548-2557`; `metaflow_declaration.rs:6,53`).
- "A metaflow woken for a request starts a fresh flow… Its last flow is resumed only when the request is the literal continuation… under the model's young threshold; the judgment is a small model's." is unbuilt (the fresh start is built).
- "Flow measures a flow's context at every turn's end." is built (Record.Context on the Stop hook).
- "Past its model's refresh threshold the flow is refreshed as it goes idle: Flow holds the queue, starts the successor, closes the predecessor's pane and its native thread in the same event, and delivers the queue" is built for the pane. Closing the native thread in the same event is not verified.
- "The successor receives its belief modules and the raw records named, and no summary or handover" is built (`waking.rs:~2460`).
- "A flow is refreshed from outside without being woken, or refreshes itself through Flow" is built.
- "below the young threshold a flow is refreshed only on a dramatic change of direction" is unbuilt.
- "Each model's thresholds, young, refresh and ceiling, are configuration." is partly built; only `Refresh` exists.
- "A refresh comes before the harness's compaction; a compaction is an emergency, ordered through the meta socket and refused under the threshold" is built (`msf:355-362`; `store/context.rs:173-196`).
- "a flow that compacted is investigated for working too long" is partly built (warning plus the Investigation config).
- "An abandoned… flow is closed, its pane and native thread with it, archived and deregistered." is partly built.
- "An ephemeral flow is a job flow that is not woken again" is unbuilt.

**P6 Harness events, reminders, the heartbeat** (`:535-537`)
- "a Claude flow's hooks call the Flow CLI at session start, prompt, tool use, turn end and session end; a Codex flow's app-server sends its turn events" is built.
- "Flow decides from its configuration where each event goes; nothing polls, and a poller that must exist is registered and reported." is partly built; no polling timers were found, and the registration is not found.
- "In the long term Flow keeps the account of usage from these events" is unbuilt.
- "A flow that must look again after a time asks Flow for a reminder: a Notice… delivered at the time it names" is unbuilt.
- "The heartbeat is such a reminder, never shorter than an hour… The number of running flows is kept low." is unbuilt.

**P7 Behavior is configuration** (`:561-565`)
- "Flow hardwires no behavior a person might want otherwise… typed datom, kept in Flow's Memory, changed through the meta socket, and authored as datom files… A value absent from configuration leaves its behavior off." is partly built. Configure is built (`msf:278-284`, tables `store.rs:95-109`). Hardwired: effort (`sending.rs:409`), power (`waking.rs:126`), the Curriculum exchange timeout of 30 s (`context.rs`). Datom files exist only for the capsule.
- "Every situation has its operation… rebinding, releasing its lock, delivering its queue, compacting, closing, importing a running Herdr session, reading any record." is built: Rebind, Release, Deliver, Command Compact, Retire, MetaBindExisting, Inspect and ReadEvents (`msf:183-202`).
- "The meta socket is open locally to every flow." is unbuilt (aspect-gated, `peer.rs:87`).
- "A harness is defined per version in configuration… A harness-blacklisted module…" is partly built: harness profiles and leave-outs exist (`msf`, `sf:315`); per-version harness and blacklist are unbuilt.

**P8 The capsule, Herdr and the versions of Flow** (`:644-646`)
- "The Capsule is where flows run: a Herdr session holding one pane per flow, with its own sockets and store." is partly built: the capsule is a test script (`flow-capsule.clj`), and a `HerdrSessionName` field exists on launch (`sf`).
- "Flow serves several capsules: a query that names none takes the default, and a variant with one more field names one." is unbuilt.
- "A running Herdr session is imported into Flow through the meta socket" is built as `MetaBindExisting` (`msf:187,305-315`).
- "Flow runs as stable, last and next, each under its own name, socket and store; a testing binary never opens the stable store." is partly built: parallel Nexuses exist as deployment practice (`flow39`, `flow-meta39`, `flow-040`, `flow-next` state directories); the capsule uses its own store.

**P9 The Flow ethos** (`:672-974`)
- "Flow is specified whole in Ethos: the Library, the Signal of its ordinary socket, the Signal of its meta socket, its Operation and its Memory… the Rust is generated from it; the bodies are hand-written." is partly built. Generation is built (`build.rs:1-30`). The proposed Operation (Compose, Start, Give, Measure, Replace, Close, Sleep, Record) differs from the actual Operation (Compose, Reserve, Record, Register, Confirm, Open, Spawn, Bind, Title, Submit, Close, Release, Wake, Drain). The proposed Memory (Flow, Delivery, Answer) differs from the actual two-record Memory.
- "In the long term every trait Flow uses is declared here too." is partly built: `starter.ethos` declares traits that generate `generated/starter.rs`.
- "One path: a query enters as signal, becomes an operation, changes Memory, and leaves as a response." is partly built in structure, not in these types.

**P10 Delivery replaces priority** (`:993-1007`)
- "Queue… Wake… Abrupt… The message itself carries no priority." is unbuilt (HardAbrupt, MiddleAbrupt and Soft remain, `delivery.ethos:5-7`, `msf:333-335`).
- "Abrupt on Codex is one Escape… Abrupt on Claude is two Escapes… then the prompt, then an explicit Enter." is built as configuration (Claude `[esc esc]` plus `[enter]`, Codex `[esc]`, from the deployed Configuration output).
- "A Wake or Queue delivery is typed into the pane, or sent as the Codex turn, as the recipient's turn ends, and at once when it is idle; it carries everything queued, as one datom." is partly built: whole payload on dep, one at a time on main.

**P11 What a remembering carries** (`:1016-1018`)
- "Open, the open records of its address up to a cap" is unbuilt. `Predecessors` and `Custom` are built (`sf:289`).
- "The remembering is a field of the launch and of the declaration" is partly built: it is on Launch only.
- "A refreshed flow receives its beliefs, the raw vision and notion logs its remembering names and the open beads of its address, and those alone: no summary and no handover." is partly built; open beads are not found.
- Renaming `InstructionPrompt` to `Brief` is unbuilt (the wire still says `InstructionPrompt`).

**P12 Presentation line moves to collaboration.** This is a psyche-context change, with no Flow code. The present Flow code does carry a presentation prompt for Psyche core Primary (`composition.rs:72-90`).

**P13 No flow claims its id** (`intent/main-flow.md`)
- "your Flow ID is given to you at launch" is built for Claude (the id is chosen before the flow starts and FLOW_ID is exported) and for the Codex bind.

**P14 Versions side by side** (`nix-builds.md`)
- "A Nexus is built in its versions, stable, last and next, each a Nix output under its own name" is not found in Flow's flake. `flake.nix` has `flow-capsule` and `curriculum` packages plus checks; I did not find stable, last or next outputs.
- "a testing binary runs raw from its build, against its own store, until it is proven" is partly built: the capsule does this.

**P15 Configuration is data, sent at activation** (`nix-workflow.md`)
- "activation sends them to the running Nexus through its meta CLI, in succession… reads no other notation" is partly built. The deployed unit sends Configure datoms through `flow-meta` in succession, but the metaflow declarations are read from EDN by babashka. Primary commit `983439d12` deleted that EDN, and where the datom replacement lives is not found.
- "A testing build runs raw against a testing store and never the stable one" is built for the capsule.

## 6. Summary for the committer

1. The Flow Nexus today is a real, working launcher, messenger and reaper: Launch, Refresh, Replace, Send and BindSeat on the ordinary socket, plus Configure, Rebind, Inspect and Compact on the meta socket. Kernel-identified callers, the metaflow lock, per-model refresh thresholds and queue-carrying wakes are all built.
2. The designed features that are absent are the Capsule semi-sandbox and encryption, ephemeral flows, the heartbeat and reminders, three-word ids, kameo actors, `Open` remembering, young and ceiling thresholds, and kind-decided waking.
3. Some pieces exist only partly. Simplified flows have the wire type and composition but lost their tool restriction in 0.40. Module hash checks verify against the composer's hashes, not source repositories. Operation and Memory ethos exist but do not match the book's types.
4. The deployed CLI is 0.40.0 (identical to `origin/main` `a0ca88`). The running Nexus is 0.40.4 (`230b3b`, `queue-emergency`), which hands the whole queue over as one payload where main does not.
5. Effort, power per layer and several timeouts are hardwired against the "behavior is configuration" line. The meta socket is aspect-gated, not open to every flow.