<!-- to-the-living:start -->
Presentation.{ «Signal» }

Ten proposals, each shown Now and Proposed, then the five rulings they rest on.

## How it is now
### The vision
`Vision/signal.md` has six headings: Name, What signal is, Query and response,
Text and signal, Meta signal, Protocol. It says the protocol "is to be decided".
Beside it, Signal also appears in three other vision files.
```
Vision/nexus.md      Sockets, Signal only, Routing, Repositories
Vision/protos.md     Signal is parallel
Vision/messaging.md  a message lands in the prompt as a datom
```

### The two harness contracts
One names its queries with nouns, the other with verbs.
```
signal-harness 8.0.0       7 queries, noun heads   20 responses
  MessageDelivery.MessageDelivery
  HarnessStatusQuery.HarnessStatusQuery
meta-signal-harness 1.0.1  3 queries, verb heads    7 responses, past tense
  Configure  ResolveModel  LaunchSession
```

### The frame they share
Both frame through `signal` 5.0.0. Nothing in the frame names the contract,
so the meta contract needs a socket of its own.
```
[ length: u32, big-endian, 4 bytes ][ rkyv archive of Query or Response ]
  at most 8 MiB, at most 64 levels deep, no contract discriminator
```

### What signal 8.0.0 adds
A greeting that settles the contract by the digest of its ethos source.
Exchange ids, so exchanges run concurrently on one connection.
```
manifests pinning signal              37
  pinning a revision with greeting    10
Orchestrate, Flow sources name        neither Handshake nor ExchangeId
```

### What ethos-zero reads
ethos-zero 16.0.0 reads four sections. Of 39 contracts, none declares
a simple or an extended form.
```
Signal [ imports ] [ queries ] [ responses ] [ types ]
```

### Sockets measured under /run
```
meta-named   orchestrate-meta  flow-meta  meta-harness  aggregator-meta  Lojix meta.sock
owner-named  message-owner.sock  repository-ledger-owner.sock
```

### Where datom is compiled in
The harness Nexus is one package with its CLIs; it compiles its contracts
with `datom` on. `flow-nexus` compiles its meta contract with `datom`
to type a message into a pane.

### Where the vision goes
On his order of today, vision migrates from Vision/ into the psyche
repository as Vision-type skills. Each [vision] proposal names
Vision/signal.md as its home today and travels with the migration.

## The path of a signal
<svg xmlns="http://www.w3.org/2000/svg" width="700" height="250" viewBox="0 0 700 250" font-family="sans-serif" font-size="15">
  <rect x="0" y="0" width="700" height="250" rx="8" fill="#ffffff"/><defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect x="10" y="70" width="110" height="90" rx="8" fill="#fff4d6" stroke="#a07800"/><text x="65" y="108" text-anchor="middle" font-weight="bold">CLI</text><text x="65" y="130" text-anchor="middle" font-size="13">datom ⇄ signal</text><line x1="140" y1="36" x2="140" y2="200" stroke="#a07800" stroke-width="2" stroke-dasharray="6 4"/><text x="140" y="26" text-anchor="middle" font-size="13" fill="#7a5c00">text ends here</text>
  <rect x="160" y="70" width="90" height="90" rx="8" fill="#eeeeee" stroke="#555"/><text x="205" y="108" text-anchor="middle" font-weight="bold">socket</text><text x="205" y="130" text-anchor="middle" font-size="13">frame</text><rect x="290" y="70" width="110" height="90" rx="8" fill="#dcebff" stroke="#2a5db0"/><text x="345" y="108" text-anchor="middle" font-weight="bold">signal</text><text x="345" y="130" text-anchor="middle" font-size="13">rkyv, typed</text><rect x="440" y="70" width="110" height="90" rx="8" fill="#e2f4e2" stroke="#2e7d32"/><text x="495" y="120" text-anchor="middle" font-weight="bold">operation</text>
  <rect x="590" y="70" width="100" height="90" rx="8" fill="#f3e5f5" stroke="#7b1fa2"/><text x="640" y="120" text-anchor="middle" font-weight="bold">memory</text><g stroke="#333" stroke-width="1.8" marker-end="url(#pa)"><line x1="120" y1="95" x2="158" y2="95"/><line x1="250" y1="95" x2="288" y2="95"/><line x1="400" y1="95" x2="438" y2="95"/><line x1="550" y1="95" x2="588" y2="95"/><line x1="588" y1="140" x2="552" y2="140"/><line x1="438" y1="140" x2="402" y2="140"/><line x1="288" y1="140" x2="252" y2="140"/><line x1="158" y1="140" x2="122" y2="140"/></g><text x="200" y="200" font-size="14" fill="#1b4d9c">Query in → (top arrows)</text>
  <text x="200" y="224" font-size="14" fill="#2e6b31">← Response out (bottom arrows)</text>
</svg>

*Text stops at the CLI; inside, a query runs signal → operation → memory and the response comes back.*

## Proposals
### 1. Queries are verbs, responses their past tense [vision]
`Vision/signal.md`, section "Query and response". Assumes Rulings 1 (a) and 2 (a).
Grounded 2026-08-26: the slot is the request, so the head is "an imperative voice".
The forms section and the names `Deliver`, `Observe` are the flow's, not his.

Now:
```
A Signal declares queries and responses; input and output are too low-level for it.

Signal
[]                                     ; imports
[ Lock.LockRequest  Release.LockId ]   ; queries
[ Locked.Lock  Released.Lock ]         ; responses
[ LockId.Integer  LockName.String  LockRequest.{ LockName }  Lock.{ LockId LockName } ]   ; types
```
Proposed:
> A Signal declares queries and responses. A query is an imperative verb, because
> its slot already says it is a request: `Deliver`, `Observe`. A response is that
> verb's past tense: `Delivered`, `Observed`. A refusal is a response that names
> itself, never a string. Input and output are too low-level for a Signal.
>
> ```
> Signal                                   ; the Message Nexus's ordinary contract
> [ flow:[ FlowId Voice ] ]                ; imports: flow id and Voice.{ Aspect Layer }, from Flow's Library
> [ Deliver.{ Voice Body.String }          ; queries: imperative verbs
>   Observe.Voice ]
> [ Delivered.Voice                        ; responses: each verb's past tense
>   Observed.{ Voice State.[ Idle Working ] }
>   Refused.[ NoSuchVoice.Voice ] ]        ; a refusal names itself
> [ Simple  Extended.FlowId ]              ; forms: the extended container adds the flow id
> []                                       ; types: none beyond the inline ones
> ```

### 2. Simple and extended forms [vision]
`Vision/signal.md`, new section. Grounded 2026-10-03: the same data "cast into a different container".
The forms section and its container names are the flow's, not his. Now: no such section.

Proposed:
> ## Simple and extended forms
>
> One datum travels in one of two containers, declared in the Signal's forms section.
> The simple form carries no flow id: a query names a voice, and whichever flow
> holds that voice now receives it.
>
> The extended form carries the same datum with the flow id beside it.
> Common queries and responses use the simple form. The extended form serves
> debugging and components that need more of each other; a CLI uses it rarely.

Against proposal 1, with `FlowId.String` from `signal-flow` 10.0.0 and the voice `Psyche.Primary`:
```
Deliver.{ Psyche.Primary «the bead is closed» }                      ; query, simple
Extended.{ bad807 Deliver.{ Psyche.Primary «the bead is closed» } }  ; query, extended
Delivered.Psyche.Primary                                             ; response, simple
Extended.{ bad807 Delivered.Psyche.Primary }                         ; response, extended
```

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="200" viewBox="0 0 700 200" font-family="sans-serif" font-size="15">
  <rect x="0" y="0" width="700" height="200" rx="8" fill="#ffffff"/><rect x="10" y="20" width="300" height="130" rx="10" fill="#e8f1ff" stroke="#2a5db0" stroke-width="1.5"/><text x="25" y="46" font-weight="bold" fill="#1b4d9c">Simple</text><text x="25" y="68" font-size="13" fill="#333">common queries and responses</text><rect x="25" y="82" width="270" height="50" rx="6" fill="#ffffff" stroke="#333"/><text x="160" y="112" text-anchor="middle" font-family="monospace" font-size="13">Deliver.{ Psyche.Primary «…» }</text><text x="335" y="114" text-anchor="middle" font-size="24" fill="#333">=</text>
  <rect x="360" y="20" width="330" height="130" rx="10" fill="#fff1e0" stroke="#c06000" stroke-width="1.5"/><text x="375" y="46" font-weight="bold" fill="#9a4d00">Extended</text><text x="375" y="68" font-size="13" fill="#333">debugging, component to component</text><rect x="375" y="82" width="62" height="50" rx="6" fill="#ffd9a8" stroke="#c06000"/><text x="406" y="112" text-anchor="middle" font-family="monospace" font-size="13">bad807</text><rect x="445" y="82" width="232" height="50" rx="6" fill="#ffffff" stroke="#333"/><text x="561" y="112" text-anchor="middle" font-family="monospace" font-size="13">Deliver.{ Psyche.Primary «…» }</text>
  <text x="350" y="180" text-anchor="middle" font-size="14" fill="#333">same inner datum; the extended container adds only the flow id</text>
</svg>

*One datum, two containers: the extended one adds the flow id, nothing else.*

### 3. "Meta signal" becomes "Sockets" [vision]
`Vision/signal.md`. Assumes Ruling 3 (a).
Grounded 2026-08-26: "create an interface on the meta socket" to change configuration.

Now:
```
## Meta signal
The meta signal is never optional: the daemon is configured only over its meta surface.
```
Proposed:
> ## Sockets
>
> Each socket speaks exactly one contract: the ordinary socket its signal contract,
> the meta socket its meta signal contract. The meta signal is never optional:
> a Nexus is configured only over its meta socket, and a raw write into a pane
> is a meta operation. The meta socket is reached only locally.

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="170" viewBox="0 0 700 170" font-family="sans-serif" font-size="15">
  <rect x="0" y="0" width="700" height="170" rx="8" fill="#ffffff"/><defs><marker id="sa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs><rect x="10" y="20" width="200" height="50" rx="8" fill="#dcebff" stroke="#2a5db0"/><text x="110" y="50" text-anchor="middle">signal contract</text><rect x="10" y="95" width="200" height="50" rx="8" fill="#fde2e2" stroke="#b02a2a"/><text x="110" y="125" text-anchor="middle">meta signal contract</text><rect x="260" y="20" width="160" height="50" rx="8" fill="#eeeeee" stroke="#555"/><text x="340" y="50" text-anchor="middle">ordinary socket</text>
  <rect x="260" y="95" width="160" height="50" rx="8" fill="#eeeeee" stroke="#555"/><text x="340" y="118" text-anchor="middle">meta socket</text><text x="340" y="137" text-anchor="middle" font-size="12" fill="#8a1f1f">local only</text><rect x="490" y="20" width="200" height="125" rx="10" fill="#e2f4e2" stroke="#2e7d32"/><text x="590" y="70" text-anchor="middle" font-weight="bold">Nexus</text><text x="590" y="94" text-anchor="middle" font-size="13">configured only over meta;</text><text x="590" y="112" text-anchor="middle" font-size="13">a raw pane write is meta</text><g stroke="#333" stroke-width="1.8" marker-end="url(#sa)"><line x1="210" y1="45" x2="258" y2="45"/>
  <line x1="420" y1="45" x2="488" y2="45"/><line x1="210" y1="120" x2="258" y2="120"/><line x1="420" y1="120" x2="488" y2="120"/></g>
</svg>

*One socket, one contract; configuration enters only through the local meta socket.*

### 4. "Protocol" becomes "The frame" [vision]
`Vision/signal.md`. Assumes Ruling 4 (a).
Grounded 2026-08-11: the signal repository carries what every signal needs, the "handshake payload basically".

Now:
```
## Protocol
Signal is portable rkyv plus whatever protocol is standardized on top of it.
The protocol is to be decided.
```
Proposed:
> ## The frame
>
> A frame is a four-byte big-endian length and then the rkyv archive of one root
> value, validated on receive. Nothing in the frame labels the contract.
>
> A connection opens with one greeting that names the contract by the digest of
> its ethos source; peers built from different sources do not talk.
>
> After the greeting a connection carries many exchanges, each named by an id the
> querying side mints: a query with one response ends its exchange, a subscription
> keeps answering.

The bounds `signal` 8.0.0 declares (`src/frame.rs`, `src/portable.rs`):
```rust
pub const FRAME_PREFIX_BYTES: usize = 4;
pub const MAXIMUM_SIGNAL_BYTES: usize = 8 * 1024 * 1024;
pub const MAXIMUM_SIGNAL_DEPTH: usize = 64;
```

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="270" viewBox="0 0 700 270" font-family="sans-serif" font-size="15">
  <rect x="0" y="0" width="700" height="270" rx="8" fill="#ffffff"/><text x="10" y="26" font-weight="bold" fill="#333">One frame</text><rect x="10" y="38" width="170" height="54" fill="#fff4d6" stroke="#a07800"/><text x="95" y="62" text-anchor="middle">length n, u32, BE</text><text x="95" y="82" text-anchor="middle" font-size="13">4 bytes</text><rect x="180" y="38" width="510" height="54" fill="#dcebff" stroke="#2a5db0"/><text x="435" y="62" text-anchor="middle">rkyv archive of Query, Response, or a form</text><text x="435" y="82" text-anchor="middle" font-size="13">n bytes, at most 8 MiB, at most 64 levels deep</text><text x="10" y="130" font-weight="bold" fill="#333">One connection</text>
  <line x1="20" y1="150" x2="680" y2="150" stroke="#555" stroke-width="2"/><rect x="20" y="162" width="150" height="44" rx="6" fill="#f3e5f5" stroke="#7b1fa2"/><text x="95" y="182" text-anchor="middle">greeting</text><text x="95" y="199" text-anchor="middle" font-size="12">digest of ethos source</text><rect x="190" y="162" width="220" height="44" rx="6" fill="#e2f4e2" stroke="#2e7d32"/><text x="300" y="182" text-anchor="middle">exchange 1: query</text><text x="300" y="199" text-anchor="middle" font-size="12">one response, then ended</text><rect x="430" y="162" width="250" height="44" rx="6" fill="#e2f4e2" stroke="#2e7d32"/>
  <text x="555" y="182" text-anchor="middle">exchange 2: subscription</text><text x="555" y="199" text-anchor="middle" font-size="12">keeps answering</text><text x="350" y="244" text-anchor="middle" font-size="14" fill="#333">exchange ids are minted by the querying side; exchanges interleave</text>
</svg>

*A frame is a length and an archive; a connection is one greeting, then many exchanges.*

### 5. Text and signal [vision]
`Vision/signal.md`, section "Text and signal". Assumes Ruling 5 (a).
Grounded 2026-09-15: "the Nexus only gets signal".

Now:
```
The textual form is datom; a CLI actualizes it and sends signal; a Nexus never textualizes.
```
Proposed:
> The textual form is datom; a CLI actualizes it and sends signal; a Nexus never
> textualizes. The same contract library compiles the datom kinds into the CLI
> and compiles them out of the Nexus, which decodes only the types it was compiled with.
> A Nexus is a package of its own, apart from its CLIs, so nothing of datom reaches it.

### 6. The caller [vision]
`Vision/signal.md`, new section. Now: no such section.
Grounded 2026-09-26: a standard "that we need to put in Signal".

Proposed:
> ## The caller
>
> The CLI identifies the process that called it and carries that identity in the
> signal, so a Nexus learns which flow called by the process, through Flow.
> No flow says who it is.

### 7. ethos-zero reads a forms section [implementation]
`ethos-zero/README.md`, "File variants", line 47 and lines 54 to 56. Built on a yes to 1 and 2.
The forms section and the generated `Form<T>` are the flow's, not his.

Now:
```
Signal     [ imports ] [ queries ] [ responses ] [ types ]     ; Query and Response implied

A Signal generates `pub enum Query` and `pub enum Response` from its
first two sections, so those two names are the ones a Signal may not
also declare; an Operation likewise generates `pub enum Operation` and
```
Proposed:
```
Signal     [ imports ] [ queries ] [ responses ] [ forms ] [ types ]     ; Query, Response and Form implied

A Signal generates `pub enum Query` and `pub enum Response` from its
first two sections and `pub enum Form<T>` from its third, one variant
per declared form, `Simple(T)` carrying the datum alone and each other
form carrying its payload before the datum; those three names are the
ones a Signal may not also declare; an Operation likewise generates
`pub enum Operation` and
```

### 8. Harness queries become verbs [implementation]
`signal-harness/ethos/signal.ethos`, the queries section; version 8.0.0 becomes 9.0.0.
Built on a yes to 1. The verb names are the flow's, not his. Payload types are unchanged.
```
Now                                               Proposed
MessageDelivery.MessageDelivery                   Deliver.MessageDelivery
InteractionPrompt.InteractionPrompt               Prompt.InteractionPrompt
DeliveryCancellation.DeliveryCancellation         CancelDelivery.DeliveryCancellation
HarnessStatusQuery.HarnessStatusQuery             ReadStatus.HarnessStatusQuery
WatchHarnessTranscript.WatchHarnessTranscript     WatchTranscript.WatchHarnessTranscript
UnwatchHarnessTranscript.HarnessTranscriptToken   UnwatchTranscript.HarnessTranscriptToken
UsageSnapshotQuery                                ReadUsage
```

### 9. The owner socket becomes the meta socket [implementation]
`message`: `crates/message-nexus/src/configuration.rs` line 69 and `crates/message-meta/src/main.rs` line 28. Built on a yes to 3.
```diff
-            meta_socket_path: self.runtime("message/message-owner.sock"),
+            meta_socket_path: self.runtime("message/message-meta.sock"),
-                .unwrap_or_else(|_| format!("{runtime}/message/message-owner.sock")),
+                .unwrap_or_else(|_| format!("{runtime}/message/message-meta.sock")),
```

### 10. The Signal sentence in vision-nexus [implementation]
`Curriculum/skills/vision-nexus.md`, line 12, its first sentence; the rest of the line is unchanged. Built on a yes to 2 and 4.

Now:
```
Signal is the messaging layer: an rkyv binary archive, typed, validated on receive,
length-prefixed on the socket; nothing else rides the wire.
```
Proposed:
```
Signal is the messaging layer: a four-byte big-endian length, then the rkyv archive of
one root value, typed and validated on receive; a connection is greeted once by the
digest of its contract's ethos source and then carries exchanges named by ids the
querying side mints; a datum travels in the simple form, or in the extended form that
adds the flow id; nothing else rides the wire.
```

## Rulings
### 1. What a Signal's two sections are called
- (a) Queries and responses. 2026-09-09: "it's a query and a response"; asked again 2026-09-26 as "Queries and responses".
- (b) Requests and replies, or requests and responses. 2026-09-10: "signal defines the requests and the replies"; 2026-09-13: "the requests and the responses".

### 2. What input and output name
- (a) Too low-level for signal; good names for the computing inside the core. 2026-09-09.
- (b) No part: the middle part is operation, whose sections ethos-zero 16.0.0 reads as operations and outcomes, marked "not yet the living's word". 2026-10-04, his three-part words.

### 3. What the privileged socket is called
- (a) Meta socket. 2026-08-26; "fairly reasonable for now" on 2026-10-03.
- (b) Owner socket. In no record of his; in code in Lojix (`LOJIX_OWNER_SOCKET`) and Message 0.15.0 (`message-owner.sock`).

### 4. Whether the wire protocol is decided
- (a) Decided as built, resting on code only, not on his words: the length-prefixed rkyv frame and the digest greeting, in `signal` since 2026-09-12.
- (b) To be decided: `Vision/signal.md` "Protocol"; 2026-08-08: "we need to flesh that out better too".

### 5. Whether any Nexus touches datom
- (a) Never. 2026-09-09: the Nexus "is not going to do the textualization at all".
- (b) A Nexus that hands a datom into a prompt must make the text. 2026-10-03, a notion: "how does Nexus send datom to places"; `flow-nexus` does so today.
<!-- to-the-living:end -->
