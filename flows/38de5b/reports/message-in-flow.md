# Message in Flow: one path for a message from flow A to flow B

Subflow of Psyche High 38de5b, 2026-09-25. Design report only: no code, nothing sent, no lock taken.

The revisions read are Flow `LiGoldragon/flow` 5e1382f (0.10.5) with its ordinary contract `signal-flow` 83171f3 (4.0.1); messenger-clj `origin/main` 7474199 (0.2.2) and branch `m1-sender-aspect-model-38de5b` (f592ede, c72fc9d, 5171131); Message `LiGoldragon/message` 55657f4, the last 0.12.0 revision, with the `signal-message` it pins, 37c3e5b. Line numbers refer to those revisions.

Coinages are marked *(coinage)* where they first appear. Every other capitalized name is either in code or in a psyche record.

## Witnessed live state (2026-09-25)

- **Flow:** `flow-nexus.service` is active and runs flow-0.10.5, per 38de5b's log. Its sockets `/run/user/1001/flow/{flow,flow-meta}.sock` are present. Flow knows 13 flows: 5f38bc is Active and 12 are Pending (`receipts/flow-bind-live.md`).
- **`hm-*`:** `hm-send` resolves to `/nix/store/w6mcm7a4…-messenger-clj-0.2.0/bin/messenger-clj`. So the live messenger is **0.2.0, not main's 0.2.2**. Of the two main commits G1 (94895e9) and M6 (7474199), 00f95a reports neither as cut over.
- **Message:** `message-daemon.service` is active and has run `/nix/store/npnsww3f…-message-0.12.0/bin/message-daemon` since 2026-09-24 17:04 CST. Its sockets `/run/user/1001/message/{message,message-owner}.sock` are present. The daemon's name comes from its unit file; the nexus skill calls the long-running executable a Nexus. I did not observe whether any flow uses the daemon to send.

## 1. One message from flow A to flow B today

The table traces one message: A = 38de5b, B = b7da5d, body "Flow 0.10.6 landed".

| Step | Flow's `Send` (0.10.5) | messenger-clj (main 7474199) | Message Nexus 0.12 (`Deliver`) |
|---|---|---|---|
| **Call** | `flow 'Send.{ b7da5d «Flow 0.10.6 landed» }'`. `SendRequest.{ FlowId BareInput }` (signal-flow `ethos/signal.ethos:26`); the query is listed at `:24`. | `FLOW_ID=38de5b hm-send b7da5d "Flow 0.10.6 landed"`. `main.clj:42-59` parses flags into `send!` (`core.clj:782`). | `DeliveryRequest.{ SourceEventIdentifier ClusterMessage TargetFlows }` (signal-message `ethos/signal.ethos:267-269`), where `ClusterMessage.[ Relay.ClusterRelay Peer.PeerEnvelope ]` (`:264`). |
| **Sender identity** | None. The request has no sender field (`:26`), and any socket peer can send. | Taken from the `FLOW_ID` environment variable without checking (`core.clj:744`). The attempt stores no sender (`DeliveryAttempt`, `core.clj:20`). Branch m1 resolves the sender from `HERDR_SESSION`/`HERDR_PANE_ID` against its own route registry and refuses a mismatching `FLOW_ID` (m1 `core.clj:711-743`); this is not on main. | Claimed inside the payload as `PeerSender.{ FlowIdentifier SessionIdentifier }` (`:254-263`). `validate_delivery_request` checks the body hash and the event id, but never checks the caller (`engine.rs:399-429`). |
| **Resolution** | From Flow's own store (`store.rs:1581-1596`). The route is then rechecked against `herdr api snapshot`: exact agent name, pane, terminal and harness (`herdr.rs:503-520`), plus the `.b7da5d.flow-id` claim marker (`herdr.rs:523-546`). The route counts as live only when the status is `idle`/`working` and `interactive_ready` (`herdr.rs:440-462`). That is why every Codex pane reported `done` resolves Unavailable (`flow-bind-live.md:84`). | From its own Datalevin route registry (`read-route`, `core.clj:197-202`). The exact route must match `herdr agent list` (`core.clj:377-383`). Otherwise it falls back to `--pane`, the stored name, or a title suffix (`core.clj:364-376, 384-389`). `verify-target!` accepts `idle`/`working`/`done` (`core.clj:334-348`). | It asks Flow `ResolveRecipient` over `/run/user/1001/flow/flow.sock` (`nexus_delivery.rs:26, 48-75`), then re-resolves just before prompting and requires the same route (`:145-154`). It pins **signal-flow 968ae3b** (`Cargo.toml:49`), which is 14 commits behind 83171f3; see O1. |
| **Transport** | `herdr --session S agent prompt <pane> <text>` (`herdr.rs:193-203`). A Pending recipient must be `idle` (`herdr.rs:182-189, 465`). | `herdr --session S agent prompt <pane> <envelope>`, with `--wait --until working/idle/done/blocked` when `--wait-presented` is given (`core.clj:214-219`). It holds an Orchestrate reservation over the state root while sending (`core.clj:451`). | The same `herdr agent prompt` (`nexus_delivery.rs:162-172`), guarded by a blank-composer screen read (`:187-229`). When no Herdr route is available, it uses the app-server endpoint for Claude or Codex (`:117-136`). |
| **Envelope (pane text)** | The bare input, verbatim. A Pending recipient also gets `\n\nFLOW_PRESENTED_b7da5d_<ms>_<seq>` appended (`herdr.rs:191-192, 290-294`). | `#msg ["38de5b" "Flow 0.10.6 landed"]`, built by `message-envelope` with an EDN round-trip check (`core.clj:135-147`; the `PaneMessage` tuple is at `:27`). The living's words go as `#psyche ["38de5b" "<context>" "1/2" "<piece>"]`, where each envelope is at most 800 characters and the verbatim is split on whitespace (`core.clj:28, 149-190`). A body that is itself one complete form is refused (`core.clj:669-676`). | The whole `ClusterMessage` as datom text (`nexus_delivery.rs:111`, `text.rs:37-44`). A Peer message therefore puts `PeerSourcePath` and `PeerBodySha256`, a full 64-hex hash, into the pane (`:259-263`). |
| **Ledger** | None for messages. A Send writes only the lifecycle promotion (`record_active`, `store.rs:1639-1651`; `lib.rs:203-208`). | Datalevin through the Babashka pod (`typed_store.clj:66-76`). The attempt is stored as `Submitting/Uncertain` before the prompt (`core.clj:764`) and rewritten to its grade afterwards (`core.clj:730-738`). A Held message leaves a pending intent (`core.clj:470-484`). | A sema store, `messenger.sema` (`tables.rs:1, 106`). An event-keyed identity row comes first; then a per-recipient row is written as a non-retryable in-flight Parked record before the harness is touched (`engine.rs:134-225`). |
| **Grade** | `SendOutcome.[ Accepted.FlowId Presented.PresentationReceipt ]` (`:26`). Accepted means Herdr accepted the prompt of an Active flow (`herdr.rs:205-207`). Presented means the marker was found in a pane read (`herdr.rs:208-259`). A failure **before** typing and a failure **after** typing both return `DeliveryRefused` (`herdr.rs:188` vs `:224, :247`; `lib.rs:198-202`). | `Transported`, `Presented`, `Fallback-Presented`, `Held`, `Uncertain` (`core.clj:13, 769`). A failure after typing is `Uncertain`, with the instruction "do not retry" (`core.clj:776-781`). | `ReceiptKind.[ Accepted TranscriptWitnessed Parked FileOnly ]` (`:270-273`). Accepted means transport submission only (`nexus_delivery.rs:81-83`). An ambiguous outcome stays Parked and is never retyped (`engine.rs:208-230`). |
| **Receipt** | `Sent.Accepted.b7da5d`, or `Sent.Presented.{ b7da5d <pane> FLOW_PRESENTED_… <ms> }`. The first Presented send promotes Pending to Active (`lib.rs:196-208`; UPGRADES.md 0.4.0 at `:137-150`). | Printed `Transported.{ b7da5d working }` (`core.clj:733`). `Held.{ b7da5d <Reason> attempt-<12hex> }` (`core.clj:483`). | `DeliveryRecorded.{ <event> [ { b7da5d Accepted } ] }` (`engine.rs:249-252`; `:274-278`). |

Observations, kept separate from hypotheses:

- **O1: contract drift (inference, not witnessed).** Message 0.12 decodes Flow replies with signal-flow 968ae3b. In that revision the Response enum is `[ Started Restarted RecipientResolved … ]` (968ae3b `ethos/signal.ethos:4`). In 83171f3 it is `[ Started LaunchPending StartAmbiguous Restarted RecipientResolved … ]` (`:25`). A `RecipientResolved` from Flow 0.10.5 therefore carries a different discriminant from the one Message 0.12 expects. The `ResolveRecipient` query keeps index 2 in both. I did not test whether the reply misdecodes or is refused against the live Flow.
- **O2: one refusal, two meanings.** Flow's `DeliveryRefused` covers both "nothing was typed" and "typed, presentation unobserved". The grades Held and Uncertain cannot be kept through Flow until these are split.
- **O3: the marker and the idle gate.** Promotion types a `FLOW_PRESENTED_…` marker into the recipient's prompt, and it requires `idle`. A send to a working Pending flow is refused, and the test says so by name: `queued_send_cannot_promote_a_pending_working_flow` (`lib.rs:1064`). Today 12 flows are Pending.
- **O4: three registries.** There are three records of who is where: Flow's store, messenger-clj's Datalevin routes (43 routes, 31 stale, per `reports/audit-messenger.md:23`), and Flow's `.flow-id` claim markers, which Flow also reads (`herdr.rs:532`). Message 0.12 kept its own marker index only as a SEAM (`flow_registry.rs:3-8`). Its live delivery already asks Flow.
- **O5: no role data.** Flow's store keeps no aspect, power, model or process identity (`FlowRecord`, `store.rs:311-320`). The aspect, power and model sent in `MetaBindExisting` do not reach `FlowNode`, whose fields are `FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle` (`:26`).

## 2. The target, in the living's words

The order (the living to Psyche Medium e51411, 2026-09-25 16:46:38Z; typed or STT not established; e51411 transcript `e5141130-….jsonl`; not found logged in any `flows/*/vision/`):

> And you probably have a huge context. You should get restarted on the V2 if it's working. If it's working right away let's just move everybody over and start working on making Flow better and then incorporating the Nexus message.

Flow sends, and Message uses Flow (the living to e51411, 2026-09-24; relayed as #psyche into `flows/88475f/vision/flow.md`):

> I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input. Flow basically exposes everything from the harness, and then message makes use of it. So Flow deploys first, and we can use it raw to send messages, even.

Flow owns Herdr, and Message asks Flow for the position (108ab0, 2026-09-17, typed, `flows/108ab0/vision/operational-flowHerdrMessageTriangle.md`):

> Flow uses Herder sessions to keep track of these flows, and then Message can ask it for the Herder position, and then it can send it a message through Herder.

The same division (056f6d, 2026-09-18, relayed by c7128c, `flows/056f6d/vision/messaging.md`):

> Message can get the data from Flow, and Flow can put a lock on some stuff.
>
> Basically, Flow is in charge of herder. I shouldn't interact with it directly. Should create a way for me to send messages to certain layers eventually, but for now, the agents will know that it's me because of how the message is formatted. It won't be datom-formatted.

A message is one datom (distilled `Vision/messaging.md`, "A message is a datom, and it arrives as one"):

> The message body is a datom that lands in the recipient's prompt as a datom-formatted object. There is no envelope around it.

The sender's role, the size of a message, and the psyche variant (e51411, 2026-09-25, STT, `flows/e51411/vision/messaging.md`):

> It knows which pane the call came from so we can use the database to know the aspect and the model.

> A message is really just a message.

> Oh right, that's why I wanted to include this psyche-type message. Instead of "message [msg]" being like "psyche" or something, it's verbatim "psyche" with context. I guess first is the context and then the verbatim.

> We split it up into pieces so we can have a broken-up psyche verbatim if we need more room.

The EDN pane form and the living's own input (e51411, 2026-09-25):

> We can get a fully actually real concept on the ground instead of just making the agents pretend that they're talking through datom but it's not processed. And then we still get the differentiation from real Psyche input messages, which are not in EDN syntax.

Grades (the messaging skill): "Never upgrade one grade into another."

### The target shape (this report's reading, to be confirmed)

The *one path* *(coinage)* runs as follows:

1. The sender's harness calls one CLI with one inline datom.
2. The receiving component learns **who is calling** from Flow, by process. The caller's word is not trusted.
3. It asks Flow for the **exact live binding** of the recipient (`ResolveRecipient`).
4. It durably records the attempt against that binding **before** anything is typed.
5. It hands the rendered text to **Flow's `Send`**, which alone drives Herdr.
6. Flow's reply carries a grade that names what was observed.

The message itself is one typed value: `Machine` text, or the living's words with context. Only at the pane is it rendered as text.

The pane text is the *compensation envelope* *(coinage)*: `#msg ["38de5b" "…"]` or `#psyche ["38de5b" "<context>" "1/1" "…"]`. It exists because the Claude and Codex panes take only text, and it stays EDN so that machine words differ on sight from the living's own input, which "is not in EDN syntax". The grades carried end to end are Held, Transported, Presented, Uncertain and, per ruling R4, Fallback-Presented. None is upgraded.

Tensions to put to the living, not resolved here:

- **T1.** da1e3f, 2026-09-17, typed: "no, message, not flow-send. use the message nexus!" and "flow is to start or refresh a flow". Against this stands 88475f's 2026-09-24 record above: "send messages with Flow … use it raw". The two agree if Flow's `Send` is the raw transport and Message is where messaging lives. That reading is mine.
- **T2.** `Vision/messaging.md` says "There is no envelope around it." `#msg [...]` is an EDN tagged form, and whether it counts as the datom or as an envelope around one is unsettled. The living confirmed the shape "tag, Flow ID, text" at 19:20Z (`flows/e51411/log.md:115`, paraphrased there, not verbatim).
- **T3.** "incorporating the Nexus message" can be read two ways. It may mean bringing Message Nexus into use on top of Flow; the 108ab0/056f6d/88475f triangle supports this reading. Or it may mean incorporating messaging into Flow itself. The words do not decide. Section 4 turns on this.
- **T4.** The name. "Even the nexus should be called Messenger." (e51411, 2026-09-25). The repo, contract and binaries are still `message`, `signal-message` and `message-daemon`.

## 3. Landings

Each landing is one task for one Opus. They land in order, and none adds a second route alongside an old one. L1 and L2 are common to every branch of the fork in section 4. Landings L3–L6 are written for the proposed branch. The alternatives list what they would replace.

### L1. Flow knows the caller and the caller's role

- **Repos:** `signal-flow` (major bump, 5.0.0), `meta-signal-flow` (repin), `flow` (0.11.0).
- **Files:**
  - `signal-flow/ethos/signal.ethos`: `FlowNode` gains `FlowAspect PowerLevel ModelName`. A new query `ResolveCaller.ProcessId` *(coinage)* answers `CallerResolved.FlowNode` or `CallerResolutionRejected.[ Unbound Ambiguous ]` *(coinage)*.
  - `flow/crates/flow-nexus/src/store.rs`: `FlowRecord` keeps aspect, power, model and `ProcessIdentity`, from `MetaBindExisting` and from the Start profile.
  - `flow/crates/flow-nexus/src/lib.rs`: the new query arm walks `/proc/<pid>` parents to the one bound `ProcessIdentity` (pid, uid, start token).
  - `flow/crates/flow-nexus/src/herdr.rs`: unchanged.
  - The same query covers Flow's own `Send`, which reads `SO_PEERCRED` itself.
- **Acceptance:**
  - A fixture child of a bound pane process resolves to that flow, with its aspect and model.
  - An unbound process gets `Unbound`, and a process under two bindings gets `Ambiguous`.
  - `List` shows aspect and model.
  - The 105 existing tests stay green.
  - The 12 live Pending flows must be re-bound with their process identity, because the store was written without it (Field's deploy step).

### L2. Flow's `Send` grades are exact, and no marker is typed

- **Repos:** `signal-flow`, `flow`.
- **Files:**
  - `ethos/signal.ethos`: `SendRequest.{ FlowId BareInput Presentation.[ Transport Observe ] }` *(coinage)*. `SendRejection.DeliveryRefused` splits into `NotDelivered` (nothing typed) and `Uncertain` (typed, outcome unobserved) *(coinage)*.
  - `herdr.rs:170-261`: Observe uses `herdr agent prompt … --wait --until working …` bound to the exact pane, the same observation messenger-clj uses (`core.clj:214-226`). `presentation_marker` (`:290-294`) and its append (`:191-192`) are removed.
  - `lib.rs:162-209`: a Pending working flow accepts a Transport send. Promotion follows ruling R3.
- **Acceptance:**
  - A readiness failure returns `NotDelivered` and zero prompts.
  - A prompt that returns success but whose wait fails returns `Uncertain`, with exactly one prompt and no retry.
  - The pane text equals `BareInput` byte for byte.
  - The four marker tests are rewritten to the Observe method.
- **Depends on:** Flow 0.10.6 (done panes available), already dispatched by 38de5b.

### L3. messenger-clj goes through Flow (proposed branch B, first step)

- **Repo:** `messenger-clj`.
- **Files:**
  - `core.clj`: `read-route`, `resolve-send-route`, `exact-live-route?`, `verify-target!` and the `ShellHerdr` prompt/agent calls are replaced by `flow 'ResolveCaller…'`, `flow 'ResolveRecipient.<id>'` and `flow 'Send.{ <id> «<envelope>» Observe|Transport }'`.
  - Grade mapping:

    | Flow reply | messenger-clj grade |
    |---|---|
    | `Sent.Accepted` | Transported |
    | `Sent.Presented` | Presented |
    | `NotDelivered`, `UnknownFlow`, `FlowStopped` or `RouteUnavailable` | Held, with reason |
    | `Uncertain` | Uncertain |

  - `typed_store.clj`: the route and retirement schema is removed, so attempts and pending intents remain, and each attempt gains the sender and the `FlowNode` it was bound to.
  - `main.clj`: `hm-register`, `hm-deregister`, `hm-rebind`, `hm-move`, `hm-retire` and `hm-heartbeat-state` are removed, because Flow's meta socket owns binding. `hm-list` becomes a projection of `flow 'List.{}'`.
  - `skills/compensation-messenger-clj.md` in Curriculum changes in the same landing.
  - Branch m1's pane registry is superseded, not merged.
- **Acceptance:** a fake `flow` executable replays the four Flow replies and checks the four grades.
  - A `Held` types nothing and leaves a pending intent.
  - An `Uncertain` is never resent.
  - `FLOW_ID` is dropped as input.
  - The `#msg`/`#psyche` rendering tests stay unchanged.
  - The build passes a local `nix flake check`.
- **Deploy:** by Field. `hm-*` must never have two transports at once.

### L4. Message 0.12's parallel delivery is stopped

- **Repo:** CriomOS-home (`The user environment`), where the `message-daemon` unit is declared.
- **Files:** the unit declaration only.
- **Change:** until L5 lands, the daemon is disabled, or it answers `Deliver`, `FlowDeliver` and `FlowAnnounceIdle` with a typed refusal. Its Herdr and endpoint delivery (`nexus_delivery.rs:106-185`) is then no longer a second route to the panes.
- **Acceptance:**
  - `systemctl --user is-active message-daemon` reports inactive, or a refusal is witnessed.
  - No flow's send path references `message`, checked by grepping Curriculum skills.
- **Owner:** Field, on the living's word, because it is a deployed service.

### L5. The Messenger contract carries the message as a type (branch A step, gated on the ruling in section 4)

- **Repos:** `signal-message` (major bump) and `meta-signal-message` (repin).
- **Files:** `ethos/signal.ethos`. Queries: `Send.{ FlowId Message }` with `Message.[ Machine.MachineText Psyche.{ Context Verbatim } ]` *(coinage)*. The shape of the living's words follows R2.
  - It replaces `Deliver`, `DeliveryRequest`, `ClusterMessage`, `ClusterRelay`, `PeerEnvelope` and `ReceiptKind`, and `FlowDeliver` goes with its park.
  - Replies are `Sent.{ FlowId Grade }` with `Grade.[ Transported Presented ]`, `Held.{ FlowId HeldReason }` and `Uncertain.{ FlowId AttemptId }` *(coinages)*.
  - Every consumer is updated in the same landing: `message/src/bin/relay.rs` and `message_cluster.rs`, or they are removed.
- **Acceptance:** every record kind has a round-trip text example, per the nexus skill. It is repinned to L2's `signal-flow`.

### L6. The Messenger Nexus absorbs messenger-clj (branch A step)

- **Repo:** `message`, renamed if the living so rules (T4).
- **Files:**
  - `src/engine.rs`: the `Send` arm resolves the caller by `SO_PEERCRED` pid through `ResolveCaller`. It then records the attempt in `messenger.sema` bound to the `FlowNode`, renders the compensation envelope (a port of `core.clj:135-190`, including the 800-character psyche split), and calls Flow `Send`.
  - `src/nexus_delivery.rs`: Herdr, endpoint and blank-composer code are removed, because Flow owns the pane.
  - `src/flow_registry.rs` and `src/flow_delivery.rs` are removed.
  - The Datalevin attempts are imported read-only into sema, or archived with their path recorded.
  - `hm-send` becomes the shorthand for `message 'Send.…'`.
  - messenger-clj is archived, and the compensation skill is replaced by the messaging skill.
- **Acceptance:**
  - The messenger-clj rendering fixtures produce byte-identical pane text from Rust.
  - The four-grade fake-Flow test is ported.
  - An `hm-send` after cutover shows up in the sema ledger and nowhere else.

Alternative sequences:

- **Branch A direct:** skip L3 and L4 and land L5–L6. `hm-*` then keeps its own Herdr route until L6, which is a longer period with two routes, because Message 0.12's delivery keeps running too.
- **Branch C:** Flow's `SendRequest` carries `Message` in place of `BareInput`, and Flow renders the envelope and keeps the ledger. L3–L6 collapse into two Flow landings, and both messenger-clj and Message retire.

## 4. What happens to messenger-clj: the fork

**A. Absorbed into the Messenger Nexus.** Messenger-clj's semantics move to Rust, on sema, behind Flow's `Send`: the envelope, the psyche split, holds, Uncertain, and the attempt recorded before the prompt. Messenger-clj then retires.

- *Support:* "incorporating the Nexus message" (the first reading in T3); 108ab0/056f6d/88475f, where Message uses Flow; the nexus skill (typed, sema, signal only); "Even the nexus should be called Messenger."
- *Cost:* two landings of porting, and the Clojure proof of concept ends.

**B. Kept as the pane-typing compensation behind Flow.** Messenger-clj keeps rendering and its attempt ledger. It loses its registry and its Herdr transport to Flow (L3), and Message 0.12 is stopped (L4).

- *Support:* the living set Clojure as the proof of concept: "a fully actually real concept on the ground"; "The registry becomes Datalevin". It is also the shortest way to one live route and to real messages reaching the 12 Pending flows.
- *Cost:* the Messenger Nexus contract waits, and the proof of concept's registry work (m1) is dropped.

**C. Retired into Flow.** Flow's `Send` takes the typed message and renders the envelope, and neither messenger nor Message remains.

- *Support:* the second reading in T3; the living's own pattern with flow-clj, 2026-09-25: "Well if we're using Flow then we don't need Flow CLJ." (relayed by e51411; 38de5b log).
- *Cost:* Flow grows a message domain. That runs against "Flow basically exposes everything from the harness, and then message makes use of it" and against the 09-17 record "no, message, not flow-send".

**Proposal:** do B now (L1–L4), then A (L5–L6) when the living says the proof of concept has done its work. At every point there is exactly one route. B's work is small and is not wasted: L3's grade mapping and rendering tests become L6's acceptance fixtures. I am not deciding this; it goes to the living.

## 5. Open rulings for the living

**R1. The pane envelope: one tag or three.** The same message is shown here in each candidate shape, as pane text:

- Today (main 7474199): `#msg ["38de5b" "Flow 0.10.6 landed"]`
- The aspect-as-tag proposal (38de5b, `receipts/pane-shape.md`, not ruled): `#psyche [Fable 38de5b «Flow 0.10.6 landed»]`. This **collides** with today's `#psyche`, which marks the living's words: the same tag would mean "sent by a Psyche flow" and "the living said".
- The three-tags notion (e51411 `notion/message.md`, "There should be three hashtags there, right?"): `#msg #psyche #fable ["38de5b" "Flow 0.10.6 landed"]`. In EDN this reads as nested tagged forms. messenger-clj's nesting check refuses nested complete forms in a *body* (`core.clj:669-676`), but an envelope written this way would itself be nested.

The question: does the pane show the sender's aspect and model, now that Flow will know them (L1)? If it does, which tag does which job? The same answer fixes the Messenger's `Message` type in L5.

**R2. Where the living's words travel.** Example: e51411 relayed the 16:46Z order to 38de5b as machine prose: `s 38de5b "From Psyche Opus e51411, the living: 'If it's working right away …'"` (e51411 transcript).

- **(a)** As today's own variant: `#psyche ["e51411" "the living to e51411, 16:46Z, on the V2 move" "1/1" "If it's working right away let's just move everybody over and start working on making Flow better and then incorporating the Nexus message."]`
- **(b)** As a section inside a machine message: "the message syntax will have a section for verbatim psyche words" (e51411, 2026-09-25).
- **(c)** As a separate `#living` tag (38de5b proposal).

Two further parts of the question:

- In the Messenger contract, is the variant `Psyche.{ Context Verbatim }` next to `Machine`, or a field on a machine message?
- Do the living's words ever pass through Flow's `Send` in typed form, or only as rendered text?

Medium's approval "Okay yeah, that's good" did not cover this shape (38de5b log, 15:57Z).

**R3. How a Pending flow becomes Active.** 12 flows are Pending, and they include e51411, b7da5d and 00f95a.

- **(a) The first real Send, which is Flow's current design and 38de5b's decision.** A message to e51411 while it is `working` is refused today (`lib.rs:1064`). When e51411 is idle, it receives the real message with `FLOW_PRESENTED_e51411_1790371234567_1` appended. The living has objected to noise of this kind: "There's a bunch of hashes in there, full length … Take all of that out." (d8df70 via 836818, 2026-09-24). After L2 the marker is gone, and a Transport send to a working Pending flow succeeds without promoting it. Promotion waits for an Observe send.
- **(b) A bind confirmation** *(coinage)*. This is a meta query that promotes a Pending flow when its bound process, pane and native session are all witnessed live again, with nothing typed. `MetaBindExisting` already checks all three at bind time (`flow-bind-live.md:26-32`). UPGRADES 0.4.0 made "no binding becomes Active through this request" a rule, so choosing (b) reverses a recorded design choice.

Which does the living want? And is "Active" still needed, once the route check at every Send is exact?

Smaller points that also need the living:

- **R4.** Does Fallback-Presented, a prompt straight into a pane outside Flow's binding, stay a Messenger grade? Or is it only the living's "bypass failing messages and send each other straight into your panes" (2026-09-24), done by hand and named as such?
- **R5.** The name: Message or Messenger (T4). The living's words: "Even the nexus should be called Messenger."

## Sources

- **38de5b:**
  - `log.md` lines 28-45 and 68, and the tail: the 16:46Z relay, Medium's approval scope, the bind outcome, 38de5b's decisions on 0.10.6 and promotion.
  - `receipts/flow-bind-live.md`: the bind datom, List/ResolveRecipient replies, the promotion rule.
  - `receipts/pane-shape.md`: the aspect-tag proposal.
  - `receipts/living-words-view.md`: two Transported sends.
  - `reports/audit-messenger.md`: gaps G1-G6, the route count, the unknowns.
  - `reports/route-manifest.md`: 12 live rows, m1's register syntax.
- **e51411 (messaging, speech, and the V2 move):**
  - `vision/messaging.md`: fallback, EDN, own system prompt, maximize the message, Datalevin, "A message is really just a message", sender role from the pane, Messenger not Message, big messages and the psyche type, 800-character split, spreading the psyche.
  - `vision/speech.md`: STT failures.
  - `notion/message.md`: sender role, one datom call, three tags.
  - `log.md:110, 115`: the approval scope, "tag, Flow ID, text".
  - Transcript `e5141130-9a4a-4b8f-b405-67d941a7b320.jsonl`: the user turn at 2026-09-25T16:46:38Z, verbatim.
- **88475f (Flow first):** `vision/flow.md`, "send messages with Flow"; `vision/message.md`.
- **108ab0 (the Flow, Herdr and Message triangle):** `vision/operational-flowHerdrMessageTriangle.md`, `vision/operational-messageAsDatomInPrompt.md`.
- **056f6d (Message gets data from Flow; Flow in charge of Herdr):** `vision/messaging.md`. Also c7128c `vision/messageAndFlow.md`.
- **da1e3f (flow is not message):** `vision/operational-flowVsMessage.md`.
- **836818 (no hashes in messages):** `vision/messaging.md`.
- **Distilled:** `Vision/messaging.md`, on message as datom, priority and delivery witnesses.
- **Code:**
  - `LiGoldragon/signal-flow` 83171f3 and 968ae3b: `ethos/signal.ethos`.
  - `LiGoldragon/flow` 5e1382f: `crates/flow-nexus/src/{lib,herdr,store}.rs`, `crates/flow/src/main.rs`, `README.md`, `DESIGN.md`, `UPGRADES.md`.
  - `LiGoldragon/messenger-clj` 7474199: `src/messenger_clj/{core,main,typed_store}.clj`, `src/data_readers.clj`. The m1 branch at 5171131: `src/messenger_clj/core.clj`.
  - `LiGoldragon/message` 55657f4: `Cargo.toml`, `src/{engine,nexus_delivery,flow_delivery,flow_registry,text,tables}.rs`.
  - `LiGoldragon/signal-message` 37c3e5b: `ethos/signal.ethos`.
- **Skills, loaded through the Skill tool:** psyche, nexus, nexus-rationale, messaging, flow-communication, compensation-messenger-clj, datom, ethos, spirit, subflow, flow-evidence.
- **Live, 2026-09-25:** `readlink -f $(which hm-send)`, `systemctl --user list-units`, `systemctl --user show message-daemon.service`, `ls /run/user/1001/{flow,message}`.
