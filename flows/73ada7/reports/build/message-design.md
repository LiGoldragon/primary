# Message Nexus, buildable design

For Mind, which builds it, and Field, which deploys it. Message
carries a typed request from one flow to the flow that is current
for a metaflow, by way of Flow's time-bound lock. Flow's own half is
f5a6e9's buildable Flow design
(`/home/li/primary/flows/f5a6e9/reports/flow-buildable-design.md`).
This design imports that design's Library and Signal types as they
stand. Where Message needs something that design lacks, section 10
names the need. None of what follows is in production.

Markers on each point:

- **[R]** ruled: a line in a distilled skill (psyche-skills authored
  source).
- **[V]** a raw vision record, not yet distilled.
- **[P]** an unruled proposal in a book or in f5a6e9's design.
- **[N]** a notion; it binds nothing.
- **[I]** this flow's own choice or inference.

## 1. What Message does

A flow writes one datom naming a metaflow by its Address and a request.
Message learns which metaflow the caller runs in, asks Flow for the
lock on the recipient metaflow, and hands Flow the request under that
lock. Flow then places the request by the waking rule: delivered now
if the metaflow is awake, queued if it is asleep and the request does
not wake it, and woken if the request does wake it. Flow refuses any
request that leaves the vision-aspects routes. Message holds no
messages, no queue and no message ids.

- "message, not flow-send. use the message nexus!" [V]
  (`flows/da1e3f/vision/operational-flowVsMessage.md`, 2026-09-17).
- The Nexus is named message ("message should be called message") [V]
  (d4ae97, 2026-10-09; cited in missed-context entry 21).
- Flow holds the lock on flows [R] (vision-flow). Message asks for a
  time-bound lock, talks in metaflows, and Flow holds no messages [V]
  (`flows/f5a6e9/vision/flow.md:51-61`, 2026-10-07). The same rule
  is stated as «Flow, a passable vision» proposal 5 [P].
- Flow keeps the queue and applies the waking rule [P] (f5a6e9's
  design §2; book 11). This differs from the living's raw "I don't
  think that it's Flow's job to hold messages" (same f5a6e9 record):
  see fork F1.
- Flow refuses a request that leaves the vision-aspects routes [R]
  (vision-flow, psyche-skills 850fd27). The routes themselves are in
  vision-aspects [R].
- A request is a typed value, never a letter [V] (f5a6e9 record
  above). Its kinds are Order, Question, Psyche.Said, Psyches.Vector<Said>,
  Result and Notice [P] (book 17; f5a6e9's design Library). `Said.{ Context
  Verbatim }` is the type carrying the living's words; see section 10.
- "We shouldn't get the message ID." [V]
  (`flows/b7ba00/vision/messaging.md:29`, 2026-09-26).

## 2. Repositories and crates

These follow vision-nexus [R]: `<nexus>`, `signal-<nexus>`,
`meta-signal-<nexus>`, one CLI per socket, and the meta CLI named
`<component>-meta`. All three repositories already exist. They are
rewritten in place; no compatibility path is kept [R] (spirit).

| Repository | Holds |
|---|---|
| `message` | crates `message-nexus` (lib + bin `message-nexus`), `message` (bin, ordinary CLI), `message-meta` (bin, meta CLI), `message-defaults` (the default configuration constant) |
| `signal-message` | `ethos/library.ethos` (Message's Library), `ethos/signal.ethos` (ordinary socket), generated Rust |
| `meta-signal-message` | `ethos/signal.ethos` (meta socket), generated Rust |
| `signal-flow` (f5a6e9's) | Flow's Library, `flow_ethos` (see note), and Flow's ordinary Signal. Message depends on it as the edge contract. |
| `message-test` | new; integration scenarios (section 9) |

`message-nexus` carries `ethos/operation.ethos` and
`ethos/memory.ethos`, and generates both Rust modules with ethos-zero.
A `build.rs` freshness check guards them, as the signal repositories
do today.

Note [I]: f5a6e9's design names the Library `flow_ethos` but does not
say which repository holds it. Message needs it on the wire, and
peers depend on each other's wire repositories, never on each other's
Nexuses [R] (vision-nexus). So this design places it in
`signal-flow/ethos/library.ethos`.

Every generated type derives rkyv. Its datom forms sit behind the
`datom` feature, which the CLIs enable and `message-nexus` does not
[R] (vision-nexus; knowledge-ethos).

## 3. Sockets, store, startup configuration

| | Path |
|---|---|
| Ordinary socket | `$XDG_RUNTIME_DIR/message/message.sock` |
| Meta socket | `$XDG_RUNTIME_DIR/message/message-meta.sock` |
| Flow edge | `$XDG_RUNTIME_DIR/flow/flow.sock` (Flow's ordinary socket; see fork F2) |
| Store | `$HOME/.local/state/message/message.sema` (sema-engine) |

- Both sockets are mode 0600, framed as a 4-byte big-endian length
  followed by an rkyv archive, one request per connection. This is
  kept from what is deployed.
- `message-nexus` starts with no arguments. Its default
  configuration is a constant in `message-defaults`, written relative
  to the user runtime and state directories and resolved at start
  [R] (vision-nexus «Configuration»). A store that exists holds the
  configuration. A store created new is seeded from the constant.
- First configuration [R] (vision-nexus): Memory's `Standard` record
  has `MetaConfigured`. While it is false, `Configure` is answered on
  the ordinary socket too. A meta `Configure` sets it true, after
  which an ordinary `Configure` is refused `AlreadyConfigured`.
- Startup payloads [V][P]: configuration lives in datom files in the
  repositories that own it, one file per concern, and the meta CLI
  sends them in succession. Each payload lands whole or is refused
  whole. Sources: `flows/73ada7/vision/nexus.md` (2026-10-09, raw)
  and «The Nexus starts» [P]. Message has one payload file, in The
  user environment (skill variable). The user service runs
  `message-meta '<payload>'` once per file after the Nexus starts.
  Example:

  ```
  Configure.{ /run/user/1001/message/message.sock
              /run/user/1001/message/message-meta.sock
              /run/user/1001/flow/flow.sock }
  ```

  This file is setup-specific and lives in the user-environment
  repository, never in `message` [R] (the skill-variable rule).
- When a socket path changes, Configure answers `RestartRequired`.
  This is kept from what is deployed.
- Meta admission [I]: only a process that runs in no flow (the
  owner) is admitted. The deployed MetaAspects list is dropped,
  although f5a6e9's Library now has `Aspect`, because no
  record asks for Psyche flows to configure Message.

## 4. Ethos

Message's five files are in
`/home/li/primary/flows/73ada7/reports/message-flow/`. Each passes
`ethos-zero Check` (ethos-zero 16.0.0), checked alone with its
imports unresolved. Message declares no shared type: it imports them
from Flow's Library, `flow_ethos`, as f5a6e9's design at main e17a62ca
declares them: `FlowId`, `Request` (with `Psyche.Said` and
`Psyches.Vector<Said>`), `Said`, `Address.{ Aspect Topic Layer }`,
`Lock.{ Address Until }`, `Process` and `Sender.Address`.
`Topic` and `Blake3` are Flow's. Until ethos-zero reads them, the
build carries `Topic.String` (designed: `Topic:Name`, the Ethos
topic's inline import) and `Blake3.String`, 64 hex characters
(designed: `Blake3.Bytes<32>`, Encodable). Message holds neither
directly.

Flow's requests are on the Flow edge exactly as its Signal gives
them: `Identify.Process`, `Lock.Address`, `Deliver.{ Lock Sender
Request }`, `Release.Lock`. Flow answers `Identified.Address`,
`Locked.Lock`, `Delivered`, `Queued`, `Woken.FlowId`, `Released`
and the refusals `Locked`, `Held.Lock`, `Lapsed`, `Unknown.Address`,
`Ended.Address`, `OffRoute` and `Unidentified.Process`. For a send up
Flow also resolves `Up` (`ResolveUp.Process`, answered
`ResolvedUp.Address` or `NoneAbove`), a request that f5a6e9's design
does not yet carry (section 10, N14). An Address is
written short: `{ Psyche flow Primary }`. Message's
Operation names these as its effects, with the imported types as
payloads.

### 4.1 Message's Library — `signal-message/ethos/library.ethos`

```
Library
[]
[ Configuration.{
     Ordinary.String            ; socket paths: records on the way
     Meta.String                ; to a typed path
     Flow.String } ]            ; the Flow edge
[]
[]
```

### 4.2 Ordinary Signal — `signal-message/ethos/signal.ethos`

```
Signal
[ flow_ethos:[ Address Request Process Lock ]
  message_library:Configuration ]
[ Send.{ Recipient.[ Address   ; a named metaflow
                       Up ]     ; the layer above the sender's
         Request }
  Configure.Configuration ]     ; only until MetaConfigured
[ Delivered                     ; placed in the awake flow
  Woken                         ; it woke the sleeping metaflow
  Queued                        ; waits in the metaflow's queue
  Configured
  Refused.[
     Unidentified.Process       ; the caller runs in no metaflow
     Unknown.Address            ; no such metaflow
     Ended.Address              ; returned to its sender
     NoneAbove                  ; Up from the top layer
     OffRoute                   ; off the vision-aspects routes
     Held.Lock                  ; another lock holds the metaflow
     Locked                     ; a refresh is under way
     Lapsed                     ; the lock ran out before delivery
     FlowUnreachable
     AlreadyConfigured ] ]
[]
```

- The simple form names the recipient by `Recipient.[ Address Up ]`,
  never a flow id [P] (book 15 proposal 4; f5a6e9's ruling, current
  best, not before the living: `Send.{ Recipient.[ Address Up ]
  Request }`). That a simple message never names a flow id rests on
  [V]: "it would be bad practice to try to send to a flow ID"
  (`flows/d4ae97/vision/datom.md`, 2026-10-07).
- `Up` means the layer above within the sender's aspect [V] ("you
  go up your own stack, not another aspect",
  `flows/6aa08d/vision/fieldStack.md`, 2026-10-07). For tonight's
  build Flow resolves it, because only Flow knows the sender's
  address, from Identify; at the top layer Flow refuses with
  `NoneAbove`, and Message answers `Refused.NoneAbove`. Who resolves
  `Up` is the living's ruling on «Who works out where send up goes»
  (fork F7); a ruling for Message moves the resolving into Message
  and leaves this wire unchanged. `Deliver` stays Address-only,
  because `Up` is resolved before delivery.
- Refusals are vocabulary [R] (vision-nexus). Those Flow answers
  keep Flow's name and payload; `FlowUnreachable` and `AlreadyConfigured`
  are Message's own.
- `Woken` drops the flow id, because Message speaks in metaflows [V].
- `Ended` returns the request to its sender [P] (book 11 proposal 3;
  f5a6e9's design §2).
- No caller field: Message reads the caller from the socket
  (section 6). The CLI's datom is therefore exactly the wire `Send`.
- No priority: see fork F6.

### 4.3 Meta Signal — `meta-signal-message/ethos/signal.ethos`

```
Signal
[ message_library:Configuration ]
[ Configure.Configuration ]
[ Configured
  RestartRequired               ; a socket path changed
  Refused.[ StoreRefused ] ]
[]
```

A meta signal is never optional [R] (vision-signal). Message keeps no
privileged send. The raw pane send is a Flow meta operation [V]
(`flows/b7ba00/vision/messaging.md:11-17`), not Message's.

### 4.4 Operation — `message/crates/message-nexus/ethos/operation.ethos`

```
Operation
[ flow_ethos:[ FlowId Address Request Lock Process Sender ]
  message_library:Configuration ]
[ Identify.Process              ; ask Flow which metaflow runs it
  ResolveUp.Process             ; ask Flow for the layer above
  Lock.Address                  ; ask Flow for the time-bound lock
  Deliver.{ Lock                ; hand Flow the request under it
            Sender
            Request }
  Release.Lock                  ; give the lock back after a failure
  Store.Configuration ]         ; write Memory
[ Identified.Address
  ResolvedUp.Address
  Locked.Lock
  Delivered
  Woken.FlowId
  Queued
  Released
  Stored
  Failed.[
     Unidentified.Process
     NoneAbove
     Unknown.Address
     Ended.Address
     OffRoute
     Held.Lock
     Locked
     Lapsed
     FlowUnreachable
     StoreRefused ] ]
[]
```

Every effect has an operation [R] (vision-nexus). 
### 4.5 Memory — `message/crates/message-nexus/ethos/memory.ethos`

```
Memory
[ message_library:Configuration ]
[ Standard.{                    ; the standard metadata tree
     Configuration
     MetaConfigured.Boolean } ]
```

Message's Memory holds only its configuration. No record is written
on the send path [I], because the queue is Flow's [P] and message ids
are refused [V].


## 5. CLIs

Each CLI takes one inline datom, with no flags and no subcommands. It
turns the datom into Signal, prints the typed reply as datom, and
opens no store [R] (vision-nexus). The client environment variables
`MESSAGE_SOCKET` and `MESSAGE_META_SOCKET` are dropped [I]. A CLI
reads its socket path from the same `message-defaults` constant the
Nexus starts from.

The datom prints below are illustrative. The exact print is whatever
datom-codec gives the generated types.

```
message 'Send.{ { Mind nexus Secondary } Order.«Build the lock path.» }'
Delivered

message 'Send.{ { Mind nexus Primary } Result.«message-flow passes on 4f2a1c.» }'
Queued

message 'Send.{ { Psyche core Primary } Psyches.[ { «on the queue» «…» } ] }'
Refused.OffRoute

message-meta 'Configure.{ …message.sock …message-meta.sock …flow.sock }'
Configured
```

A datom the CLI cannot read is refused in the CLI and nothing is
sent. The Nexus never sees text [R].

## 6. Caller identity

"a Nexus knows its caller by the process, never by a claim" [R]
(vision-nexus).

1. Message reads the peer's pid with `SO_PEERCRED` on the accepted
   connection, kept from what is deployed. That pid is the
   `Process.{ Pid.Integer Started.Integer }` of Flow's Library: the pid
   with the start time of `/proc/<pid>/stat` field 22, so a reused pid
   is told apart (see finding X4).
2. Operation `Identify.Process` goes to Flow as `Identify.Process`.
   Flow walks the process's ancestors for its harness pane
   and returns the Address of the metaflow whose current flow owns that
   pane: `Identified.Address`, or `Unidentified`. Today Flow walks
   `/proc/<pid>/environ` for `HERDR_PANE_ID`, up to 64 ancestors; this
   design keeps that mechanism inside Flow.
3. That Address becomes the `Sender` of the delivery (`Sender.Address`).

A flow that is no metaflow,
such as a side job or the living's own terminal, gets `Unidentified`
[I]; see fork F11. vision-nexus words this as the CLI carrying the
identity, while the kernel read is stronger; see fork F8.

## 7. Paths, signal → operation → memory

`M` is the recipient's Address and `S` the sender's (the `Sender`). Every
step that talks to Flow is a Message Operation whose effect is a
Signal on the Flow edge. Flow's own operation and memory steps belong
to f5a6e9's design and are shown only as far as Message sees them.

### 7.1 Send, recipient awake

```
1  CLI     Send.{ { Mind nexus Secondary } Order.«…» }   ; text → Query::Send
2  Message Identify.4127                          ; Operation
           → Flow Identify.Process → Identified.{ Psyche nexus Secondary }
3  Message Lock.{ Mind nexus Secondary }                    ; Operation
           → Flow Lock.Address                              ; Flow Memory: Lock record, Until = now + lease
           → Locked.{ { Mind nexus Secondary } 1760050000 }
4  Message Deliver.{ Lock S Order.«…» }                     ; Operation
           → Flow Deliver.{ Lock Sender Request }           ; Flow checks the route, the lock, the state
           ; Awake: Flow places the request in the current flow's pane,
           ; removes the lock record
           → Delivered
5  Message Response Delivered → CLI prints Delivered
```

Message Memory is untouched; its configuration is read at start.

What reaches the pane [I]: the sender and the requests, as one datom.

```
{ { Psyche nexus Secondary } [ Order.«…» ] }
```

Whether this lands at the end of the prompt or as a tool-call return
is open (fork F4).

### 7.2 Lock

Covered in section 8. Message takes the lock only while it handles
one Send, and serialises its own Sends per recipient metaflow with an
in-process mutex [I]. Arc-Mutex is permitted [R] (vision-nexus
«Actors»). So `Held` arises only from a lock that Message did not
take.

### 7.3 Deliver, recipient asleep

The steps are as in 7.1, up to step 4. Flow applies the waking rule
[P]:

- **Result or Notice:** Flow appends the request to the metaflow's
  `Queue`, removes the lock, and answers `Queued`. The CLI prints
  `Queued`.
- **Order, Question, Psyche.Said or Psyches.Vector<Said>:** Flow runs its wake. It
  launches the next flow with the drained queue, oldest first, and
  this request last, in the first prompt. It answers `Woken.FlowId`.
  Message answers `Woken` and drops the id, because Message speaks in
  metaflows [V].

Flow's Deliver answers `Queued` and `Woken.FlowId` as well as
`Delivered`.

### 7.4 Send up

```
1  CLI     Send.{ Up Order.«…» }
2  Message Identify.4127                          ; Operation
           → Identified.{ Mind nexus Secondary }  ; the sender S
3  Message ResolveUp.4127                         ; Operation
           → Flow ResolveUp.Process
           → ResolvedUp.{ Mind nexus Primary }    ; M
4  Message Lock.M, then Deliver.{ Lock S Request }, as in 7.1
```

`Up` is the layer above within the sender's aspect and topic
("you go up your own stack, not another aspect" [V],
`flows/6aa08d/vision/fieldStack.md`, 2026-10-07; the same topic
follows vision-aspects [R]). For tonight's build Flow resolves it,
because only Flow knows the sender's address from Identify [I]. At the
top layer Flow answers `NoneAbove`, Message answers
`Refused.NoneAbove`, and no lock is taken. `Deliver` carries the
resolved Address, so it is unchanged. If the resolved metaflow does
not exist, `Lock` answers `Unknown.Address` as in 7.5. See section 10,
N14, and fork F7.

### 7.5 Refusal

Each refusal is a typed response. When a lock is held, Message sends
`Release.Lock` before it answers.

| Where | Flow's answer | Message answers | Release? |
|---|---|---|---|
| Identify | Unidentified.Process | Refused.Unidentified.Process | no |
| ResolveUp | NoneAbove | Refused.NoneAbove | no |
| Lock | Unknown.Address | Refused.Unknown.Address | no |
| Lock | Ended.Address | Refused.Ended.Address | no |
| Lock | Refused.Held.Lock | Refused.Held.Lock | no |
| Lock | Refused.Locked | Refused.Locked | no |
| Deliver | OffRoute | Refused.OffRoute | yes |
| Deliver | Refused.Lapsed | Refused.Lapsed | yes (Flow already dropped it; Release is idempotent) |
| any | connect or frame failure | Refused.FlowUnreachable | yes, if Locked was received |

The sender gets the refusal and resends it if it chooses. Message
neither retries nor holds the request [I]; see fork F3.

## 8. The lock protocol with Flow

As f5a6e9's design has it [P], with Message's side made exact:

```
Message                         Flow
Lock.M            ─────────▶    no record, or record lapsed (Until ≤ now) → write Lock{M, now+lease}
                  ◀─────────    Locked.{ M Until }
                                record live → Refused.Held.Lock
                                refresh under way → Refused.Locked
Deliver.{ L S R } ─────────▶    L equals the live record and now < Until → place by the waking rule,
                                delete the record
                  ◀─────────    Delivered | Queued | Woken.FlowId
                                otherwise → Refused.Lapsed
Release.L         ─────────▶    delete the record if it equals L
                  ◀─────────    Released (also when absent)
```

- A lapse is judged when the next request arrives, by comparing
  `Until` with now. No timer and no sweep run, because polling is
  forbidden [R] (vision-nexus).
- The lock is time-bound "so that it doesn't lock forever" [V]
  (`flows/f5a6e9/vision/flow.md:59`). Its unit is seconds since the
  epoch [P] (f5a6e9's Memory `Until.Integer`).
- Lease [I]: 30 seconds as Flow's default constant. A pane delivery
  today takes up to about 10 seconds with its waits. f5a6e9's
  Configure has no lease field (need N11).
- Deliver carries the whole `Lock`, not a lock name [I]. vision-nexus
  "every reference names its target by that name" [R] pulls toward a
  hash name once the Library has Blake3 (finding X1).
- Flow's refresh holds the same lock, and a Lock request during it is
  refused `Locked` [P].

## 9. Acceptance tests — `message-test`

The repository follows compensation-nix: blueprint layout,
`lib/components/{message,flow}.nix`, inputs `message` and `flow`
following `nixpkgs`, and the lint gate. Each test runs the real
`message-nexus` and the real `flow-nexus` from their flake inputs,
started with no arguments and configured by their meta CLIs from
payload files in `fixtures/`. Both are developer builds with tracing.
A test passes when the expected reply prints and the expected trace
lines appear in order (compensation-testing). Builds and checks run
on NixBuilder against pushed revisions.

**Pure check `checks/message-flow.nix`** (`pkgs.testers.runNixOSTest`,
one machine, both Nexuses as user services, a real Herdr session).
Its stand-in harnesses are plain shells, bound to metaflows through
Flow's meta socket (`Bind.{ Address Process }`). Whether Herdr runs headless inside the
test VM is unwitnessed. If it does not, these scenarios that read a
pane move to the semi-sandbox below.

| # | Drive | Expect |
|---|---|---|
| 1 | Psyche.{nexus Secondary} sends Order to awake Mind.{nexus Secondary} | `Delivered`; trace Identified → Locked → Delivered → lock removed; the pane shows the sender datom and the request |
| 2 | Notice to an asleep metaflow | `Queued`; Flow `Current` shows Asleep; the queue holds one request |
| 3 | Send to a metaflow that does not exist | `Refused.Unknown.Address`; no lock record |
| 4 | Send to an Ended metaflow | `Refused.Ended.Address` |
| 5 | Field.{nexus Tertiary} → Psyche.{nexus Primary} | `Refused.OffRoute`; lock released |
| 6 | Field.{nexus Secondary} → Mind.{nexus Secondary} | `Delivered` (same layer, same topic) |
| 7 | Mind.{nexus Secondary} sends to `{ Mind nexus Primary }` | `Delivered` to Mind.{nexus Primary} |
| 8 | `Up` from Mind.{nexus Secondary} | `Delivered` to Mind.{nexus Primary}; trace Identified → ResolvedUp → Locked → Delivered |
| 9 | `Up` from Mind.{nexus Primary} | `Refused.NoneAbove`; no `Lock` call in the trace |
| 10 | `message` run from a shell in no flow's pane | `Refused.Unidentified.Process` |
| 11 | Flow `Lock.M` taken directly, then a send to M | `Refused.Held.Lock`; after the lease ends, the same send is `Delivered` |
| 12 | Flow stopped, then a send | `Refused.FlowUnreachable` |
| 13 | Fresh store, `Configure` on the ordinary socket; then meta Configure; then ordinary Configure again | `Configured`, `Configured`, `Refused.AlreadyConfigured` |
| 14 | Message restarted with no arguments | the send in test 1 succeeds with no new Configure |
| 15 | An unreadable datom given to `message` | the CLI refuses; no connection appears in the Nexus trace |

**Semi-sandbox `packages/message-flow-claude.nix`**, run with
`nix run .#message-flow-claude`, Haiku:

| # | Drive | Expect |
|---|---|---|
| 16 | Notice, then Order, to an asleep metaflow | `Queued`, then `Woken`; the woken flow's first prompt ends with `[ Notice.«…» Order.«…» ]`, the Order last |
| 17 | Order to an awake, working Claude flow | placed by Flow's rule (N8, fork F4); the recipient's transcript holds it once |

## 10. Needs against f5a6e9's Flow design

f5a6e9's design at main e17a62ca answers N1, N2, N5, N6, N7 and N13,
and part of N8: a busy awake flow queues. N4 is answered: the shared
types are declared once in Flow's Library, and the two shapes of the
metaflow are replaced by `Address.{ Aspect Topic Layer }` and the
record `Metaflow.{ Address State Past Queue }`.

Where each change since eaab24fa rests, read in
`flows/f5a6e9/log.md` (lines 147-149), `flows/f5a6e9/vision/` and
`flows/73ada7/vision/`. None of the seven is recorded there as
the living's ruling. The log words them "Ruled" and "four rulings
given", given by f5a6e9 on a
candidate; the design says of them "current best, not before the
living". Where the living has spoken on the matter, it is named.

- **C1 `Said.{ Context Verbatim }`, `Psyche.Said`, `Psyches.Vector<Said>`.**
  The living's own words ground the content: a psyche-type message
  that conveys his words, kept apart from the message type
  (`flows/73ada7/vision/messaging.md`, 2026-10-09, typed). That the
  request kind carries context and verbatim and that Psyches is a
  vector is f5a6e9's reading of eight records of this flow's package
  (f5a6e9 log line 118) and book 17 [P], pending. The name `Said` is
  the build's, ruled by f5a6e9 (log line 148). The Aspect variant
  `Psyche` and the Request variant `Psyche` clash by name; the design
  reports that to the living, and no answer was found.
- **C2 `Address.{ Aspect Topic Layer }` replaces `Details`; every
  query takes Address.** The living said the metaflow is a struct
  whose first field is the aspect, with topic, and that the topic is a
  dense string (`flows/d4ae97/vision/flow.md:181`, 2026-10-08, relayed
  in `flows/f5a6e9/vision/flow.md`). The living also thought aloud
  that each metaflow is a variant of psyche, mind or field with a
  struct of details (`flows/f5a6e9/notion/flow.md`, 2026-10-09, a
  notion). The type's name `Address`, the short form every query
  carries, and the loss of `Details` are f5a6e9's rulings (log line
  147), pending the living's ruling 1 of «The Flow Nexus vision»,
  third edition. This is fork F5.
- **C3 `Lock.{ Address Until }`.** The lock as a time-bound record
  rests on the living's "time-bound so that it doesn't lock forever"
  (`flows/f5a6e9/vision/flow.md:59`, 2026-10-07) [V]. Its fields,
  `Address` and `Until.Integer` seconds, are f5a6e9's ruling and
  f5a6e9's design.
- **C4 `Sender.Address`.** f5a6e9's ruling (log line 148). The living
  has said only that routes bind sender and recipient by aspect and
  layer (speech across aspects, approved 2026-10-09, psyche-skills
  850fd27) [R]; that a Sender is an Address is not his word.
- **C5 `Identified`, `Taken`, `Unknown` and `Ended` carry Address.**
  Consequence of C2, same ruling (log line 148). The refusals
  themselves ground in "we need a registry to know which flow is
  active" (`flows/d4ae97/vision/flow.md`, 2026-10-07) [V].
- **C6 `Deliver.{ Lock Sender Request }`.** Shape asked for by this
  flow's N1 and N2 and given by f5a6e9 (log, eaab24fa); f5a6e9's line
  148 keeps it with no repeated Address. No word of the living.
- **C7 `Send.{ Recipient.[ Address Up ] Request }`.** "Bind and Send as chosen"
  (log line 148), f5a6e9's choice. Its ground is book 15 ruling 4
  (simple and extended forms) [P], pending; the living's
  2026-10-03 "simple form, not short form" is cited in log line 106.

What remains is Flow's to rule, or the living's where marked.

- **N3** Lock and Deliver sit on Flow's ordinary socket. The living's
  raw word puts the features Message needs on Flow's meta socket
  ("we're not going to want to allow anything to just write into
  panes", `flows/88475f/vision/message.md`, 2026-09-25), and so does
  what is deployed. This is fork F2.
- **N8** Where a request lands in an awake flow: ruling 3 of
  «The Flow Nexus vision», third edition (book 17), (a) end of the
  prompt, (b) a tool-call return, (c) other. This is fork F4.
- **N11** The lease length is in no Configure payload; Lock carries
  `Until` and nothing sets its span.
- **N14** `ResolveUp.Process`, answered `ResolvedUp.Address` or
  `NoneAbove`, on Flow's edge. f5a6e9's ruling is `Send.{
  Recipient.[ Address Up ] Request }`, with Flow resolving `Up` for
  tonight's build (current best, not before the living). Flow's own
  Signal is f5a6e9's to extend.
- **U1** `Up` is the layer above within the sender's aspect. The
  living said "If you say 'send up' it means message higher layer"
  (`flows/b7ba00/vision/messaging.md:109`, 2026-09-26) [V] and "The
  message logic has to figure out where ... or maybe the flow figures
  it out. I don't know" (same file, 2026-09-26) [V]. Who resolves it
  is fork F7.


## 11. What changes from what is deployed

What is deployed, read at `main@origin` by this flow's reading
subflow: message `6fa4d0` 0.19.1, signal-message `b94d90` 10.0.0,
meta-signal-message `81e12b` 0.10.0, flow `ac6ab6` 0.24.0, signal-flow
`ecdce2` 10.0.0. Field reports that Message 0.19 and Flow 0.23 are
running (knowledge-nexus; this is Field's claim, and no receipt was
witnessed here).

- **Who carries messages.** Flows message each other today through
  messenger-clj (`hm-send`, its own Datalevin ledger, typing into
  Herdr). With this design, `message` replaces it. Retiring the
  `hm-*` commands follows, and is not part of this build.
- **Message's job.** Today Message keeps a ledger of messages with
  ids (`m-<hex>`), receipts with grades (Submitted, Parked,
  Transported, Presented, Uncertain, Read, Withdrawn, Refused),
  parks, Withdraw, Acknowledge, QueryReceipts, Observe, meta Send as
  Owner, and Redeliver. All of it is removed. Message keeps caller
  identity, the lock exchange and its configuration.
- **Priority.** `Priority.[ HardAbrupt MiddleAbrupt Soft ]` goes. The
  request kind and the waking rule decide instead (fork F6).
- **Recipients.** These were flow ids, with fan-out to several. They
  become one Address.
- **Flow edge.** Today Message calls Flow meta `ResolvePeer`, `Vet`
  and `Deliver` (a letter with a MessageId) and watches
  `Observe.Agent`. It now calls `Identify`, `Lock`, `Deliver` and
  `Release` on the socket of fork F2. Flow gains the lock, the
  waking rule and the queue; today Flow has no lock and no queue.
- **Socket.** `message-owner.sock` becomes `message-meta.sock`.
  `MESSAGE_SOCKET` and `MESSAGE_META_SOCKET` are dropped.
- **Source.** message-nexus is hand-written Rust today. Its
  Operation and Memory become ethos-generated, and signal-message
  gains a Library.
- **Memory.** Four tables (messages, receipts, parks, configuration)
  become one `Standard` record. The store starts fresh; no migration
  of the ledger [I].
- **Meta admission.** The MetaAspects list goes; the meta socket
  admits the owner only [I].
- **Tests.** Today they run the real message-nexus against a
  scripted fake Flow, and no test runs Message with a real Flow or a
  real Herdr. `message-test` runs both real Nexuses.
- **Kept.** Framing and the 1 MiB limit, sockets at mode 0600, the
  `SO_PEERCRED` and start-time read, Flow's pane-ancestry caller
  walk, Flow's body check that refuses a sigil command such as
  `/compact` [V] (`flows/88475f/vision/message.md`), the seeded
  store, `RestartRequired`.

## 12. Forks only the living can rule on

- **F1** Who holds the queue. Flow (book 11 [P], f5a6e9's design),
  or not Flow ("I don't think that it's Flow's job to hold messages"
  [V], 2026-10-07). This design follows Flow.
- **F2** Lock and Deliver on Flow's ordinary socket [P], or on its
  meta socket [V] (2026-09-25) as deployed.
- **F3** A send refused Held or Locked (during a refresh). Returned
  to the sender (this design), or Flow signals Message when it may
  send ("Flow's job to tell the message component later on ... that
  a message can now be sent" [V]), or Flow queues it.
- **F4** Where a request lands in an awake flow: the end of the
  prompt, or a tool-call return (book 17 ruling 3 [P]; see also
  `flows/6cc91b/vision/interflowMessaging.md` [V]).
- **F5** `Address` as the struct `{ Aspect Topic Layer }` (this
  design, f5a6e9's e17a62ca, [V] 2026-10-08), or the metaflow as aspect
  variants each holding topic and layer (book 17 [P], notion [N]).
- **F6** Priority tiers. vision-messaging's `Priority` [R], or none,
  with the kind deciding ("We don't even do the soft or hard ...
  wrong approach" [V], 2026-09-26). This design drops them. The
  distilled line's record date was not read.
- **F7** Who works out where send up goes (the living's question
  «Who works out where send up goes»). This design has Flow resolve
  `Up`, because only Flow knows the sender's address from Identify
  (f5a6e9's ruling, current best, not before the living). The living
  said "I don't know" who resolves it. A ruling for Message moves the
  resolving into Message, which has the sender's Address from
  `Identify` and writes the layer above itself, without changing the
  wire: `Send.{ Recipient.[ Address Up ] Request }` and the
  Address-only `Deliver` stay as they are, and only `ResolveUp` leaves
  Message's Operation.
- **F8** Caller identity. Message reads the kernel peer (deployed,
  this design), or the CLI carries the identity in the message, as
  vision-nexus words it [R].
- **F9** Request text as `String` inside the Nexus, or "forbidden for
  string handling to be in the Nexus" [V] (2026-10-05).
- **F10** Typing into a pane needs text. Flow textualizes, though "a
  Nexus never textualizes" [R]. The alternatives are a helper binary
  with the datom feature, or the harness hook pulling the request.
- **F11** Senders that are no metaflow (side jobs, the living's own
  terminal) are refused `Unidentified` for now.
- **F12** "unless Psyche has just spoken to Field" [R]: how long
  "just" lasts. For example, one reply to the Psyche metaflow that
  last delivered to that Field metaflow.
- **F13** No record of sent messages. Message history would come
  from "a different kind of interface" [V] (2026-09-26) that no
  design has yet.

## 13. Findings for Mind

- **X1** ethos-zero 16.0.0 refuses f5a6e9's Library as written.
  `Topic:Name` is rejected `Expected.Declaration` and
  `Blake3.Bytes<32>` is rejected `Name.32` (witnessed by Check on
  one-line files). Until the generator reads both, `Topic` is
  `Topic.String` (designed `Topic:Name`) and `Blake3.String`, 64 hex
  characters (designed `Blake3.Bytes<32>`).
- **X2** `Name.Type` generates a Rust alias. The living wants
  newtypes [V] (`flows/ebbe30/vision/ethos.md:39-55`). As a result
  `Topic`, `FlowId` and `Until` cannot carry their own checks or
  traits. This defect awaits e5a0bc's ruling.
- **X3** Whether a bare declared type in an enum (`Psyche.Said`
  carries the type; a bare `Psyche` would be a unit variant or a
  carrier) is not stated in knowledge-ethos. f5a6e9 writes
  `Psyche.Said` for the Request variant, so Message imports `Said`
  only through `Request`.
- **X4** Flow's Library gives `Process.{ Pid.Integer Started.Integer }`,
  the kernel's start time of the pid. Message reads both from
  `SO_PEERCRED` and `/proc/<pid>/stat` field 22.

## Sources

- f5a6e9 buildable Flow design:
  `/home/li/primary/flows/f5a6e9/reports/flow-buildable-design.md`.
- f5a6e9 books, in `/home/li/primary/flows/f5a6e9/books/`:
  `17-the-flow-nexus-vision-third-edition.md`,
  `18-the-nexus-starts.md`, `18-speech-across-aspects.md`,
  `15-stored-type-and-datom-form-second-edition.md`,
  `11-the-queue-and-the-waking-rule.md`,
  `10-flow-a-passable-vision.md`.
- This flow's draft and notes:
  `/home/li/primary/flows/73ada7/reports/message-flow/`. Records:
  `/home/li/primary/flows/73ada7/vision/`, `notion/metaflow.md`,
  `log.md`, and `reports/package/missed-context.md`.
- Raw records cited by path above, read in
  `flows/f5a6e9/vision/flow.md`, `flows/b7ba00/vision/messaging.md`
  and `flows/d4ae97/vision/flow.md`.
- Skills: vision-nexus, vision-signal, vision-messaging, vision-sema,
  knowledge-ethos, knowledge-nexus, knowledge-flow,
  compensation-testing, compensation-nix. Authored sources read:
  `psyche-skills/skills/vision-flow.md` and `vision-aspects.md` at
  850fd27.
- Deployed source: a reading subflow of this flow read message,
  signal-message, meta-signal-message, flow, signal-flow,
  meta-signal-flow and flow-test at `main@origin`. That account is a
  claim; this flow did not read the code itself.
- Witnessed by this flow: `ethos-zero Check` on the six ethos files
  in section 4 (all five `Checked`) and on the `Topic:Name` and
  `Bytes<32>` lines (both `Rejected`).
- Provenance receipt: unavailable; no PROVENANCE handoff exists for
  this run.
