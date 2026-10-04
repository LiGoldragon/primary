<!-- to-the-living:start -->
Presentation.{ «Signal» }

How it is now. `Vision/signal.md` (43 lines, landed 2026-09-09, edited 2026-09-10) stands under six headings: Name, What signal is, Query and response, Text and signal, Meta signal, Protocol; it says the protocol "is to be decided". Beside it, `Vision/nexus.md` holds Sockets, Signal only, Routing and Repositories, `Vision/protos.md` holds "Signal is parallel", and `Vision/messaging.md` says a message lands in the prompt as a datom. The authored contracts today: `signal-harness` 8.0.0 (`/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos`, 203 lines, HEAD `25a2d18`, 2026-10-03) declares 7 queries headed by nouns (`MessageDelivery.MessageDelivery`, `HarnessStatusQuery.HarnessStatusQuery`) and 20 responses; `meta-signal-harness` 1.0.1 (`ethos/signal.ethos`, 26 lines, HEAD `939bdf7`, 2026-10-03) declares 3 verb queries (`Configure`, `ResolveModel`, `LaunchSession`) and 7 past-tense responses. Both frame through `signal` at `7bcb094` (5.0.0): a four-byte big-endian length, then the bare rkyv archive of `Query` or `Response`, at most 8 MiB and 64 levels deep, with no contract discriminator, which is why the meta contract has a socket of its own (`signal-harness/ARCHITECTURE.md`, "Frames"). `signal` 8.0.0 (`0cad1d1`, 2026-10-03) adds a greeting that settles the contract by the digest of its ethos source and exchange ids for concurrent exchanges; 10 of the 37 manifests that pin `signal` pin a revision carrying it, and the Orchestrate and Flow sources name neither `Handshake` nor `ExchangeId`. ethos-zero 16.0.0 reads `Signal [ imports ] [ queries ] [ responses ] [ types ]`. Of 39 contracts with an `ethos/signal.ethos`, none declares a simple or an extended form. Deployed sockets measured under `/run`: five meta-named (`orchestrate-meta`, `flow-meta`, `meta-harness`, `aggregator-meta`, Lojix `meta.sock`), two owner-named (`message-owner.sock`, `repository-ledger-owner.sock`). The harness Nexus is one package with its CLIs and compiles its contracts with `datom` on; `flow-nexus` compiles its meta contract with `datom` to type a message into a pane. On his order of today, vision statements migrate from Vision/ into the psyche repository as Vision-type skills; each [vision] proposal names Vision/signal.md as its home today and travels with the migration.

A signal's path, from the CLI through the socket into the Nexus and back:

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="250" viewBox="0 0 700 250" font-family="sans-serif" font-size="14">
  <rect x="0" y="0" width="700" height="250" fill="#ffffff"/>
  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
  <rect x="10" y="70" width="110" height="90" rx="8" fill="#fff4d6" stroke="#a07800"/>
  <text x="65" y="105" text-anchor="middle">CLI</text>
  <text x="65" y="128" text-anchor="middle" font-size="12">datom ⇄ signal</text>
  <line x1="140" y1="30" x2="140" y2="230" stroke="#a07800" stroke-dasharray="6 4"/>
  <text x="140" y="22" text-anchor="middle" font-size="12" fill="#a07800">text ends here</text>
  <rect x="160" y="70" width="90" height="90" rx="8" fill="#eeeeee" stroke="#555"/>
  <text x="205" y="110" text-anchor="middle">socket</text>
  <text x="205" y="130" text-anchor="middle" font-size="12">frame</text>
  <rect x="290" y="70" width="110" height="90" rx="8" fill="#dcebff" stroke="#2a5db0"/>
  <text x="345" y="110" text-anchor="middle">signal</text>
  <text x="345" y="130" text-anchor="middle" font-size="12">rkyv, typed</text>
  <rect x="440" y="70" width="110" height="90" rx="8" fill="#e2f4e2" stroke="#2e7d32"/>
  <text x="495" y="120" text-anchor="middle">operation</text>
  <rect x="590" y="70" width="100" height="90" rx="8" fill="#f3e5f5" stroke="#7b1fa2"/>
  <text x="640" y="120" text-anchor="middle">memory</text>
  <g stroke="#333" stroke-width="1.6" marker-end="url(#a)">
    <line x1="120" y1="95" x2="158" y2="95"/><line x1="250" y1="95" x2="288" y2="95"/>
    <line x1="400" y1="95" x2="438" y2="95"/><line x1="550" y1="95" x2="588" y2="95"/>
    <line x1="588" y1="140" x2="552" y2="140"/><line x1="438" y1="140" x2="402" y2="140"/>
    <line x1="288" y1="140" x2="252" y2="140"/><line x1="158" y1="140" x2="122" y2="140"/>
  </g>
  <text x="345" y="195" text-anchor="middle" font-size="13">Query in →</text>
  <text x="495" y="195" text-anchor="middle" font-size="13">← Response out</text>
  <text x="350" y="225" text-anchor="middle" font-size="12" fill="#555">no text crosses the dashed line inward; the Nexus decodes only the types it was compiled with</text>
</svg>

*A query enters as text at the CLI, crosses the socket as a frame, and passes signal → operation → memory and back out as a response.*

1. **[vision] `/home/li/primary/Vision/signal.md`, section "Query and response".** Assumes Ruling 1 (a) and Ruling 2 (a).
   The forms section in the Signal root and the verb names `Deliver`, `Observe` are the flow's proposal, not his.
   Grounded: 2026-08-26, 01a03d6e, the slot is the request, so the head is "an imperative voice".
   Now:
   ~~~~
   A Signal declares queries and responses; input and output are too
   low-level for it.

   ```
   Signal
   []                                     ; imports
   [ Lock.LockRequest  Release.LockId ]   ; queries
   [ Locked.Lock  Released.Lock ]         ; responses
   [ LockId.Integer                       ; types
     LockName.String
     LockRequest.{ LockName }
     Lock.{ LockId LockName } ]
   ```
   ~~~~
   Proposed:
   > A Signal declares queries and responses. A query is an imperative verb, because its slot already says it is a request: `Deliver`, `Observe`. A response is that verb's past tense: `Delivered`, `Observed`. A refusal is a response that names itself, never a string. Input and output are too low-level for a Signal.
   >
   > ```
   > Signal                                   ; the Message Nexus's ordinary contract
   > [ flow:[ FlowId Voice ] ]                ; imports: the flow id and the voice, from Flow's Library
   > [ Deliver.{ Voice                        ; queries: imperative verbs; Deliver carries a voice and a body
   >             Body.String }
   >   Observe.Voice ]
   > [ Delivered.Voice                        ; responses: each verb's past tense
   >   Observed.{ Voice                       ; Observed carries the voice and its state
   >              State.[ Idle Working ] }
   >   Refused.[ NoSuchVoice.Voice ] ]        ; a refusal names itself
   > [ Simple                                 ; forms: the containers one datum travels in
   >   Extended.FlowId ]                      ; the extended container adds the flow id before the datum
   > []                                       ; types: none beyond the inline ones
   > ```

2. **[vision] `/home/li/primary/Vision/signal.md`, new section "Simple and extended forms".**
   Grounded: 2026-10-03, edf227 (comment relayed by 6e782c), the same data "cast into a different container".
   The forms section and its container names are the flow's proposal, not his.
   Now: no such section.
   Proposed:
   > ## Simple and extended forms
   >
   > One datum travels in one of two containers, declared in the Signal's forms section. The simple form carries no flow id: a query names a voice, and whichever flow holds that voice now receives it. The extended form carries the same datum with the flow id beside it. The common queries and responses use the simple form; the extended form serves debugging and the components that need more of each other, and a CLI uses it rarely.

   One query and its response, in both forms, against the Signal of proposal 1 (`FlowId` as `signal-flow` 10.0.0 declares it, `FlowId.String`):
   ```
   Deliver.{ Psyche.Primary «the bead is closed» }                      ; query, simple
   Extended.{ bad807 Deliver.{ Psyche.Primary «the bead is closed» } }  ; query, extended
   Delivered.Psyche.Primary                                             ; response, simple
   Extended.{ bad807 Delivered.Psyche.Primary }                         ; response, extended
   ```

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="210" viewBox="0 0 700 210" font-family="sans-serif" font-size="14">
  <rect x="0" y="0" width="700" height="210" fill="#ffffff"/>
  <rect x="10" y="40" width="300" height="130" rx="10" fill="#e8f1ff" stroke="#2a5db0" stroke-width="1.5"/>
  <text x="25" y="65" font-weight="bold">Simple</text>
  <text x="25" y="85" font-size="12" fill="#444">common queries and responses</text>
  <rect x="25" y="100" width="270" height="50" rx="6" fill="#ffffff" stroke="#333"/>
  <text x="160" y="130" text-anchor="middle" font-family="monospace" font-size="12">Deliver.{ Psyche.Primary «…» }</text>
  <rect x="360" y="40" width="330" height="130" rx="10" fill="#fff1e0" stroke="#c06000" stroke-width="1.5"/>
  <text x="375" y="65" font-weight="bold">Extended</text>
  <text x="375" y="85" font-size="12" fill="#444">debugging, component to component</text>
  <rect x="375" y="100" width="60" height="50" rx="6" fill="#ffe0b8" stroke="#c06000"/>
  <text x="405" y="130" text-anchor="middle" font-family="monospace" font-size="13">bad807</text>
  <rect x="445" y="100" width="230" height="50" rx="6" fill="#ffffff" stroke="#333"/>
  <text x="560" y="130" text-anchor="middle" font-family="monospace" font-size="12">Deliver.{ Psyche.Primary «…» }</text>
  <text x="335" y="130" text-anchor="middle" font-size="20">=</text>
  <text x="350" y="195" text-anchor="middle" font-size="13" fill="#555">the inner datum is the same value; only the container differs</text>
</svg>

*The same datum in two containers: the extended one adds the flow id, nothing else.*

3. **[vision] `/home/li/primary/Vision/signal.md`, section "Meta signal" becomes "Sockets".** Assumes Ruling 3 (a).
   Grounded: 2026-08-26, 01a03d6e, "create an interface on the meta socket" to change configuration.
   Now:
   ```
   ## Meta signal

   The meta signal is never optional: the daemon is configured only over
   its meta surface.
   ```
   Proposed:
   > ## Sockets
   >
   > Each socket speaks exactly one contract: the ordinary socket its signal contract, the meta socket its meta signal contract. The meta signal is never optional: a Nexus is configured only over its meta socket, and a raw write into a pane is a meta operation. The meta socket is reached only locally.

4. **[vision] `/home/li/primary/Vision/signal.md`, section "Protocol" becomes "The frame".** Assumes Ruling 4 (a).
   Grounded: 2026-08-11, 012fbf07, the signal repository carries what every signal needs, the "handshake payload basically".
   Now:
   ```
   ## Protocol

   Signal is portable rkyv plus whatever protocol is standardized on top
   of it. The protocol is to be decided.
   ```
   Proposed:
   > ## The frame
   >
   > A frame is a four-byte big-endian length and then the rkyv archive of one root value, validated on receive. Nothing in the frame labels the contract. A connection opens with one greeting that names the contract by the digest of its ethos source; peers built from different sources do not talk. After the greeting a connection carries many exchanges, each named by an id the querying side mints: a query with one response ends its exchange, a subscription keeps answering.

   The frame on the wire, and the bounds `signal` 8.0.0 declares (`src/frame.rs`, `src/portable.rs`):
   ```
   ┌──────────────────────┬─────────────────────────────────────────────┐
   │ length n, u32, BE    │ rkyv archive of Query, Response, or a form  │
   │ 4 bytes              │ n bytes                                     │
   └──────────────────────┴─────────────────────────────────────────────┘
   ```
   ```rust
   pub const FRAME_PREFIX_BYTES: usize = 4;
   pub const MAXIMUM_SIGNAL_BYTES: usize = 8 * 1024 * 1024;
   pub const MAXIMUM_SIGNAL_DEPTH: usize = 64;
   ```

5. **[vision] `/home/li/primary/Vision/signal.md`, section "Text and signal".** Assumes Ruling 5 (a).
   Grounded: 2026-09-15, 05c604, "the Nexus only gets signal".
   Now:
   ```
   The textual form is datom; a CLI actualizes it and sends signal; a
   Nexus never textualizes.
   ```
   Proposed:
   > The textual form is datom; a CLI actualizes it and sends signal; a Nexus never textualizes. The same contract library compiles the datom kinds into the CLI and compiles them out of the Nexus, which decodes only the types it was compiled with. A Nexus is a package of its own, apart from its CLIs, so nothing of datom reaches it.

6. **[vision] `/home/li/primary/Vision/signal.md`, new section "The caller".**
   Grounded: 2026-09-26, b7ba00 (relayed by 93ba9f), a standard "that we need to put in Signal".
   Now: no such section.
   Proposed:
   > ## The caller
   >
   > The CLI identifies the process that called it and carries that identity in the signal, so a Nexus learns which flow called by the process, through Flow. No flow says who it is.

7. **[implementation] `/git/github.com/LiGoldragon/ethos-zero/README.md`, section "File variants", line 47 and lines 54 to 56.** Built on a yes to proposals 1 and 2.
   Grounded: 2026-10-03, edf227, the same data "cast into a different container".
   The forms section and the generated `Form<T>` are the flow's proposal, not his.
   Now:
   ```
   Signal     [ imports ] [ queries ] [ responses ] [ types ]     ; Query and Response implied
   ```
   ```
   A Signal generates `pub enum Query` and `pub enum Response` from its
   first two sections, so those two names are the ones a Signal may not
   also declare; an Operation likewise generates `pub enum Operation` and
   ```
   Proposed:
   ```
   Signal     [ imports ] [ queries ] [ responses ] [ forms ] [ types ]     ; Query, Response and Form implied
   ```
   ```
   A Signal generates `pub enum Query` and `pub enum Response` from its
   first two sections and `pub enum Form<T>` from its third, one variant
   per declared form, `Simple(T)` carrying the datum alone and each other
   form carrying its payload before the datum; those three names are the
   ones a Signal may not also declare; an Operation likewise generates
   `pub enum Operation` and
   ```

8. **[implementation] `/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos`, lines 3 to 9 (the queries section); version 8.0.0 becomes 9.0.0.** Built on a yes to proposal 1.
   Grounded: 2026-08-26, 01a03d6e, the head is "an imperative voice".
   The verb names for the harness queries are the flow's proposal, not his.
   Now:
   ```
   [ MessageDelivery.MessageDelivery
     InteractionPrompt.InteractionPrompt
     DeliveryCancellation.DeliveryCancellation
     HarnessStatusQuery.HarnessStatusQuery
     WatchHarnessTranscript.WatchHarnessTranscript
     UnwatchHarnessTranscript.HarnessTranscriptToken
     UsageSnapshotQuery ]
   ```
   Proposed:
   ```
   [ Deliver.MessageDelivery                          ; queries: imperative verbs, payload types unchanged
     Prompt.InteractionPrompt
     CancelDelivery.DeliveryCancellation
     ReadStatus.HarnessStatusQuery
     WatchTranscript.WatchHarnessTranscript
     UnwatchTranscript.HarnessTranscriptToken
     ReadUsage ]
   ```

9. **[implementation] `/git/github.com/LiGoldragon/message/crates/message-nexus/src/configuration.rs` line 69 and `crates/message-meta/src/main.rs` line 28.** Built on a yes to proposal 3.
   Grounded: 2026-08-26, 01a03d6e, "create an interface on the meta socket".
   Now:
   ```
               meta_socket_path: self.runtime("message/message-owner.sock"),
   ```
   ```
                   .unwrap_or_else(|_| format!("{runtime}/message/message-owner.sock")),
   ```
   Proposed:
   ```
               meta_socket_path: self.runtime("message/message-meta.sock"),
   ```
   ```
                   .unwrap_or_else(|_| format!("{runtime}/message/message-meta.sock")),
   ```

10. **[implementation] `/git/github.com/LiGoldragon/Curriculum/skills/vision-nexus.md`, line 12, its first sentence (the rest of the line is unchanged).** Built on a yes to proposals 2 and 4.
    Grounded: 2026-08-11, 012fbf07, the "handshake payload basically".
    Now:
    ```
    Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire.
    ```
    Proposed:
    ```
    Signal is the messaging layer: a four-byte big-endian length, then the rkyv archive of one root value, typed and validated on receive; a connection is greeted once by the digest of its contract's ethos source and then carries exchanges named by ids the querying side mints; a datum travels in the simple form, or in the extended form that adds the flow id; nothing else rides the wire.
    ```

## Rulings

1. What a Signal's two sections are called.
   (a) Queries and responses: 2026-09-09, 564f55, "it's a query and a response"; 2026-09-26, b7ba00, asked again as "Queries and responses".
   (b) Requests and replies, or requests and responses: 2026-09-10, fe34eb, "signal defines the requests and the replies"; 2026-09-13, 024bc7, "the requests and the responses".
2. What input and output name.
   (a) Too low-level for signal, good names for the computing inside the core: 2026-09-09, 564f55.
   (b) No part: the middle part is operation, whose sections ethos-zero 16.0.0 reads as operations and outcomes, marked "not yet the living's word": 2026-10-04, 5ed94b, his three-part words.
3. What the privileged socket is called.
   (a) Meta socket: 2026-08-26, 01a03d6e, and "fairly reasonable for now" on 2026-10-03, edf227.
   (b) Owner socket: in no record of his; in code since 2026-06-05 (Lojix `LOJIX_OWNER_SOCKET`) and 2026-09-26 (Message 0.15.0, `message-owner.sock`).
4. Whether the wire protocol is decided.
   (a) Decided as built, resting on code only, not on his words: the length-prefixed rkyv frame and the digest greeting, in `signal` since 2026-09-12 (`e1a8302`).
   (b) To be decided: `Vision/signal.md` "Protocol", landed 2026-09-09; 2026-08-08, 55d18f4f, "we need to flesh that out better too".
5. Whether any Nexus touches datom.
   (a) Never: 2026-09-09, 564f55, the Nexus "is not going to do the textualization at all".
   (b) A Nexus that hands a datom into a prompt must make the text: 2026-10-03, 5578cc (a notion), "how does Nexus send datom to places"; `flow-nexus` does so today.
<!-- to-the-living:end -->
