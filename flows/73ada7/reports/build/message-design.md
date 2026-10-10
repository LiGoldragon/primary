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
| `signal-message` | `ethos/message_library.ethos` (Message's Library), `ethos/signal.ethos` (ordinary socket), generated Rust |
| `meta-signal-message` | `ethos/signal.ethos` (meta socket), generated Rust |
| `signal-flow` (f5a6e9's) | Flow's Library, imported as `signal_flow` (see note), and Flow's ordinary Signal. Message depends on it as the edge contract. |
| `message-test` | new; integration scenarios (section 9) |

`message-nexus` carries `ethos/operation.ethos` and
`ethos/memory.ethos`, and generates both Rust modules with ethos-zero.
A `build.rs` freshness check guards them, as the signal repositories
do today.

Note [I]: f5a6e9's design names the Library `flow_ethos` but does not
say which repository holds it. Message imports it by the crate name,
`signal_flow`. Message needs it on the wire, and
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
  has `MetaConfigured`. A new store is seeded with the constant's
  configuration and `MetaConfigured` false [I]. While it is false,
  `Configure` is answered on the ordinary socket too. A meta
  `Configure` sets it true, after which an ordinary `Configure` is
  refused `AlreadyConfigured`. A meta `Configure` answered
  `RestartRequired` sets it as well [I]: the configuration is
  persisted before that answer, and the answer says only that a
  socket path changed. This is this flow's choice, not a ruling.
- Store schema [I]: sema-engine `SchemaVersion::new(2)`; one table,
  `TableName::new("message_nexus_standard")`, family
  `FamilyName::new("message-nexus-standard")`, schema hash
  `SchemaHash::for_label("message-nexus-standard-v2")`, holding the
  one `Standard` record. The names follow old Message at 6fa4d0
  (`store.rs`: version 1, table `message_nexus_configuration`, family
  `message-nexus-configuration`, label `message-nexus-configuration-v1`).
  Flow's design at d84997 names no table, family or schema hash, so
  there is nothing of Flow's to follow. Version 2 marks the break from
  old's version 1.
- A store at the path whose schema version is not 2 is refused at
  start, naming the path and the version found (fork F14); Message
  reads nothing from it and writes nothing to it.
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
`ethos-zero Check` (ethos-zero 16.0.0) one file at a time;
ethos-zero resolves no import across files, so the imports are
cross-read against Flow's sources separately (see X5). Message declares no shared type: it imports them
from Flow's Library, as f5a6e9's design at main e17a62ca
declares them: `FlowId`, `Request` (with `Psyche.Said` and
`Psyches.Vector<Said>`), `Said`, `Address.{ Aspect Topic Layer }`,
`Lock.{ Sender Address Until.Integer }`, `Process`,
`Recipient.[ Address Up ]` and `Sender.Address`.
`Topic` and `Blake3` are Flow's. Until ethos-zero reads them, the
build carries `Topic.String` (designed: `Topic:Name`, the Ethos
topic's inline import) and `Blake3.String`, 64 hex characters
(designed: `Blake3.Bytes<32>`, Encodable). Message holds neither
directly.

Flow's requests are on the Flow edge exactly as its Signal gives
them: `Bind.{ Address Process }` (once, at start; section 7.6),
`Identify.Process`, `Lock.{ Sender Recipient }`,
`Deliver.{ Lock Request }`, `Release.Lock`. Flow answers
`Identified.Address`, `Locked.Lock`, `Delivered`, `Queued`,
`Woken.FlowId`, `Released`, `Bound.FlowId` and the refusals `Locked`, `Held.Lock`,
`Lapsed`, `Unknown.Address`, `Unknown.Lock`, `Ended.Address`,
`OffRoute`, `Unidentified.Process`, `Taken.Address` (a Bind) and
`NotMessage`. Flow accepts `Lock`, `Deliver` and `Release` only from the
Message Nexus's own process, which Message registered with `Bind` at
its start; any other peer is refused `NotMessage` (f5a6e9, current best,
not before the living). Every other Flow query stays open to any local
peer the socket admits. The lock request is
`Lock.{ Sender Recipient }`: Message identifies the sender by process
through `Identify` and passes that `Sender` with the `Recipient` it was
given. Flow's Library `Lock` is `{ Sender Address Until.Integer }`,
`Until` the second, since the epoch, at which the lock lapses. Flow
resolves `Up` relative to the sender, refuses `OffRoute` and
`NoneAbove` at the request, before any lock exists, and answers
`Locked.Lock` with the record it keeps: the resolved Address and
`Until`. There is no separate query for `Up`; the lock is one round
trip. Message knows when the lock lapses and does not deliver after
`Until`. An Address is
written short: `{ Psyche flow Primary }`. Message's
Operation names these as its effects, with the imported types as
payloads.

### 4.1 Message's Library — `signal-message/ethos/message_library.ethos`

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
[ signal_flow:[ Address Recipient Request Process Lock ]
  message_library:Configuration ]
[ Send.{ Recipient              ; Address, or Up: the layer above
         Request }
  Configure.Configuration ]     ; only until MetaConfigured
[ Delivered                     ; placed in the awake flow
  Woken                         ; it woke the sleeping metaflow
  Queued                        ; waits in the metaflow's queue
  Configured
  Refused.[
     Unidentified.Process       ; the caller runs in no metaflow
     Unknown.[ Address          ; no such metaflow
               Lock ]           ; the lock is not held any more
     Ended.Address              ; returned to its sender
     NoneAbove                  ; Up from the top layer
     OffRoute                   ; refused at Lock; off the routes
     Held.Lock                  ; another lock holds the metaflow
     Locked                     ; a refresh is under way
     Lapsed                     ; Until passed; nothing delivered
     NotMessage                 ; Flow does not take this process
                                ; as the Message Nexus
     FlowUnreachable
     AlreadyConfigured ] ]
[]
```

- The simple form names the recipient by Flow's `Recipient.[ Address
  Up ]`, never a flow id [P] (book 15 proposal 4; f5a6e9's ruling, current
  best, not before the living: `Send.{ Recipient.[ Address Up ]
  Request }`). That a simple message never names a flow id rests on
  [V]: "it would be bad practice to try to send to a flow ID"
  (`flows/d4ae97/vision/datom.md`, 2026-10-07).
- `Up` means the same topic, one layer above, within the sender's
  aspect [V] ("you go up your own stack, not another aspect",
  `flows/6aa08d/vision/fieldStack.md`, 2026-10-07). For tonight's
  build Flow resolves it relative to the `Sender` of the lock request,
  and answers `Locked.Lock` carrying the resolved Address; at
  Primary Flow refuses the request with `NoneAbove`, and Message
  answers `Refused.NoneAbove`. Who resolves
  `Up` is the living's ruling on «Who works out where send up goes»
  (fork F7); a ruling for Message moves the resolving into Message
  and leaves this wire unchanged. `Deliver` carries the lock, which
  holds the sender, the resolved Address and `Until`.
- Refusals are vocabulary [R] (vision-nexus). Those Flow answers
  keep Flow's name and payload (`NotMessage` among them: Flow's answer
  to a Lock, Deliver or Release from a process it has not bound as
  Message, which Message reports as it came); `FlowUnreachable` and `AlreadyConfigured`
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
[ signal_flow:[ FlowId Address Request Lock Sender Recipient Process ]
  message_library:Configuration ]
[ Bind.{ Address                ; at start: register this process as
         Process }              ; the Message Nexus; section 7.6
  Identify.Process              ; ask Flow which metaflow runs it
  Lock.{ Sender                 ; Flow resolves Up relative to the
         Recipient }            ; Sender; OffRoute is refused here
  Deliver.{ Lock                ; hand Flow the request under the
            Request }           ; lock, never after its Until
  Release.Lock                  ; give the lock back after a failure
  Store.Configuration ]         ; write Memory
[ Bound.FlowId
  Identified.Address
  Locked.Lock                   ; { Sender Address Until.Integer }
  Delivered
  Woken.FlowId
  Queued
  Released
  Stored
  Failed.[
     Unidentified.Process
     Taken.Address              ; a Bind of an address already awake
     NotMessage
     NoneAbove
     Unknown.[ Address Lock ]
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
   with the start time of `/proc/<pid>/stat` field 22, intended to tell
   a reused pid apart. No concrete atomic algorithm for this pid-reuse
   guard is specified or proven yet (see finding X4).
2. Operation `Identify.Process` goes to Flow as `Identify.Process`.
   Flow walks the process's ancestors to the harness process and
   compares both the pid and the start time of a Flow record's
   `Process`, returning that flow's metaflow Address:
   `Identified.Address`, or `Unidentified.Process`. No environment
   variable is read and Message knows no pane (Flow's design F 559-563;
   f5a6e9 confirms it, current best). How deep the walk goes is Flow's.
3. That Address becomes the `Sender` of the lock (`Sender.Address`),
   and the lock carries it to Flow and back.

A flow that is no metaflow,
such as a side job or the living's own terminal, gets `Unidentified`
[I]; see fork F11. vision-nexus words this as the CLI carrying the
identity, while the kernel read is stronger; see fork F8.

## 7. Paths, signal → operation → memory

`M` is the recipient's Address and `S` the sender's (the `Sender` inside the lock). Every
step that talks to Flow is a Message Operation whose effect is a
Signal on the Flow edge. Flow's own operation and memory steps belong
to f5a6e9's design and are shown only as far as Message sees them.

### 7.1 Send, recipient awake

```
1  CLI     Send.{ { Mind nexus Secondary } Order.«…» }   ; text → Query::Send
2  Message Identify.{ 4127 88231904 }              ; Operation, Process.{ Pid Started }
           → Flow Identify.Process → Identified.{ Psyche nexus Secondary }
3  Message Lock.{ S { Mind nexus Secondary } }              ; Operation, Sender and Recipient
           → Flow Lock.{ Sender Recipient }                 ; checks the route; Memory: lock record, Until = now + lease
           → Locked.{ S { Mind nexus Secondary } U }        ; the Library Lock; U is Until
4  Message Deliver.{ L Order.«…» }                          ; Operation, L the lock of step 3; not sent once now ≥ U
           → Flow Deliver.{ Lock Request }                  ; Flow trusts the route; checks the lock, the state
           ; Awake: Flow places the request in the current flow's pane,
           ; removes the lock record (one delivery per lock)
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
«Actors»). Only Message takes locks at Flow (`NotMessage` refuses every
other peer), so `Held` arises only from a lock Message itself took and
did not end, such as one left by a Message that stopped between `Lock`
and `Deliver`.

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
2  Message Identify.{ 4127 88231904 }              ; Operation, Process.{ Pid Started }
           → Identified.{ Mind nexus Secondary }  ; the sender S
3  Message Lock.{ S Up }                          ; Operation
           → Flow Lock.{ Sender Recipient }       ; Flow resolves Up relative to S
           → Locked.{ S { Mind nexus Primary } U }
4  Message Deliver.{ L Request }, as in 7.1
```

`Up` is the same topic, one layer above, within the sender's aspect
("you go up your own stack, not another aspect" [V],
`flows/6aa08d/vision/fieldStack.md`, 2026-10-07; the same topic
follows vision-aspects [R]). For tonight's build Flow resolves it
relative to the `Sender` on the lock [I], and answers `Locked.Lock`,
the lock carrying the resolved Address M as its Recipient. At Primary
Flow refuses the lock request with `NoneAbove`, Message answers
`Refused.NoneAbove`, and no lock is held. `Deliver` carries the
answered lock. If the resolved metaflow does
not exist, `Lock` answers `Unknown.Address` as in 7.5. See fork F7.

### 7.5 Refusal

Each refusal is a typed response. When a lock is held and still live, Message
sends `Release.Lock` before it answers.

| Where | Flow's answer | Message answers | Release? |
|---|---|---|---|
| Identify | Unidentified.Process | Refused.Unidentified.Process | no |
| Lock | NoneAbove | Refused.NoneAbove | no |
| Lock | OffRoute | Refused.OffRoute | no (no lock exists) |
| Lock | Unknown.Address | Refused.Unknown.Address | no |
| Lock | Ended.Address | Refused.Ended.Address | no |
| Lock | Refused.Held.Lock | Refused.Held.Lock | no |
| Lock | Refused.Locked | Refused.Locked | no |
| Deliver | Unknown.Lock (never granted, or no longer held) | Refused.Unknown.Lock | no (the lock ended) |
| Deliver | a refusal of the waking rule | that refusal | no (a refusal at Deliver ends the lock) |
| before Deliver | Message's clock is at or past `Until` | Refused.Lapsed | no (the lock lapsed; Release would answer Lapsed) |
| Lock, Deliver, Release | NotMessage | Refused.NotMessage | no (Flow does not take this process as Message; nothing is held by it) |
| any | connect or frame failure | Refused.FlowUnreachable | yes, if Locked was received |

A lock ends by Deliver (one delivery per lock), by Release, by lapse,
or by a refusal at Deliver. Message sends `Release` only where the
table says yes. `Release` answers `Released`; `Lapsed` for a lapsed
lock; `Unknown.Lock` for a lock Flow does not hold, among them a
lock already used by Deliver. Message ignores these answers after a
failure.

The sender gets the refusal and resends it if it chooses. Message
neither retries nor holds the request [I]; see fork F3.

### 7.6 Start, and the Bind

At start, after the store is opened and before either socket listens,
Message registers itself with Flow [P] (f5a6e9, current best, not
before the living):

```
Bind.{ { Field message Primary } P }
```

`{ Field message Primary }` is Message's own Address. A Nexus is
Field's body, not a flow of a layer, so Message binds under Field and
not under Mind (f5a6e9, current best). `P` is
`Process.{ Pid.Integer Started.Integer }` of Message's own process: its
pid and the start time of `/proc/<pid>/stat` field 22. Flow holds the
binding. At the gate it compares the connecting peer's kernel pid and
start time with the bound process's; they must be equal. This pid
plus start time comparison is the pid-reuse guard, and no concrete
atomic algorithm for it is specified or proven yet. No ancestor
walk happens at the gate, so a process that descends from Message is
refused. Message itself is therefore the process that connects to Flow
for `Lock`, `Deliver` and `Release`; no helper process and no CLI
connects for it.

- `Bound.FlowId`: Message listens and serves. A restart after the
  earlier Message process is gone replaces the old binding and is
  answered `Bound`.
- `Bind` goes to Flow's ordinary socket, the path Message already
  holds as `Flow` in its Configuration (f5a6e9, current best).
- Flow unreachable at start (connect or frame failure), or `Bind`
  refused (`Unidentified.Process`, or `Taken.Address` while the process
  bound under that address lives): Message does not
  start. It exits with a nonzero status after writing the cause to its
  trace. It retries nothing and listens on no socket [I]; restarting it
  is the service manager's, outside this design. Neither the design
  nor Flow's gives a retry.
- After a start that bound, a `NotMessage` from Flow means the binding
  was lost; Message answers `Refused.NotMessage` to the sender and
  does not rebind [I].

## 8. The lock protocol with Flow

As f5a6e9's design has it [P] (rulings current best, not before the
living), with Message's side made exact:

```
Message                         Flow
Lock.{ S R }      ─────────▶    route off → OffRoute; R is Up at Primary → NoneAbove (no lock)
                                no record, or record lapsed (Until ≤ now) → write { S M U }, U = now+Lease
                  ◀─────────    Locked.{ S M U }   (M = R, or Up resolved relative to S)
                                record live → Refused.Held.Lock
                                refresh under way → Refused.Locked
Deliver.{ L R }   ─────────▶    L equals the live record and now < U → place by the waking rule,
                                delete the record (one delivery per lock)
                  ◀─────────    Delivered | Queued | Woken.FlowId
                                a lock never granted, or no longer held → Refused.Unknown.Lock
Release.L         ─────────▶    delete the record if it equals L
                  ◀─────────    Released | Lapsed (a lapsed lock) | Unknown.Lock (not held)
```

- A lock ends by Deliver, by Release, by lapse, or by a refusal at
  Deliver. Release after Deliver answers `Unknown.Lock`.
- Flow's gate: `Lock`, `Deliver` and `Release` are accepted only from
  the process bound as Message at start (section 7.6), whose pid and
  start time must equal the connecting peer's; there is no ancestor
  walk at the gate. Any other peer is refused `NotMessage` (f5a6e9,
  current best).
- Flow's `Refresh` or `End` while a lock is held is refused
  `Refused.Held.Lock`, and proceeds after release or lapse.
- `OffRoute` is refused at Lock, before any lock exists; Deliver
  trusts its lock and checks no route.
- A lapse is judged when the next request arrives, by comparing
  `Until` with now. No timer and no sweep run, because polling is
  forbidden [R] (vision-nexus).
- The lock is time-bound "so that it doesn't lock forever" [V]
  (`flows/f5a6e9/vision/flow.md:59`). `Until` is a field of the
  lock, `Until.Integer`, in seconds since the epoch [P]. Flow's
  answer `Locked.Lock` carries it, and Flow keeps the same record.
- Message's rule [I]: it does not deliver after `Until`. Before it
  sends `Deliver`, Message compares its clock with the `Until` in
  the lock it holds; at or past `Until` it answers `Refused.Lapsed`
  and sends nothing.
- Lease [P]: Flow's own setting, `Lease.Integer` in seconds, added to
  `Configure.Nexus`, 60 by default (f5a6e9's ruling, current best,
  pending the living's ruling on «How long Flow's lock lasts», which
  is still open). A pane delivery today takes up to about 10 seconds
  with its waits.
- `Up` is the same topic, one layer above, within the sender's
  aspect; at Primary it is refused `NoneAbove`.
- Deliver carries the whole `Lock`, with the sender inside it, not a lock name [I]. vision-nexus
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
Flow (`Bind.{ Address Process }`). Whether Herdr runs headless inside the
test VM is unwitnessed. If it does not, these scenarios that read a
pane move to the semi-sandbox below.

| # | Drive | Expect |
|---|---|---|
| 1 | Psyche.{nexus Secondary} sends Order to awake Mind.{nexus Secondary} | `Delivered`; trace Identified → Locked → Delivered; the pane shows the sender datom and the request |
| 2 | Notice to an asleep metaflow | `Queued`; Flow `Current` shows Asleep; the queue holds one request |
| 3 | Send to a metaflow that does not exist | `Refused.Unknown.Address`; no lock record |
| 4 | Send to an Ended metaflow | `Refused.Ended.Address` |
| 5 | Field.{nexus Tertiary} → Psyche.{nexus Primary} | `Refused.OffRoute` from the lock request; no lock record; no `Deliver` or `Release` in the trace |
| 6 | Field.{nexus Secondary} → Mind.{nexus Secondary} | `Delivered` (same layer, same topic) |
| 7 | Mind.{nexus Secondary} sends to `{ Mind nexus Primary }` | `Delivered` to Mind.{nexus Primary} |
| 8 | `Up` from Mind.{nexus Secondary} | `Delivered` to Mind.{nexus Primary}; trace Identified → Locked (carrying Mind.{nexus Primary}) → Delivered |
| 9 | `Up` from Mind.{nexus Primary} | `Refused.NoneAbove` from the lock; no `Deliver` call in the trace |
| 10 | `message` run from a shell outside every flow's process tree | `Refused.Unidentified.Process` |
| 11 | A Flow stand-in holds `Deliver`; `message-nexus` is stopped after `Locked`, started again, and a send to M follows | `Refused.Held.Lock`; after the lease ends, the same send is `Delivered` (the restart's Bind replaces the dead process's binding and is answered `Bound`) |
| 12 | Flow stopped, then a send | `Refused.FlowUnreachable` |
| 13 | Fresh store, `Configure` on the ordinary socket; then meta Configure; then ordinary Configure again | `Configured`, `Configured`, `Refused.AlreadyConfigured` |
| 14 | Message restarted with no arguments | the send in test 1 succeeds with no new Configure |
| 15 | An unreadable datom given to `message` | the CLI refuses; no connection appears in the Nexus trace |
| 16 | `message-nexus` started | Flow's trace shows `Bind` with `{ Field message Primary }` and Message's own pid and start time before the first listen; a send then succeeds |
| 17 | A plain client (not the Message process) sends Flow `Lock`, `Deliver` and `Release` on Flow's ordinary socket | each `Refused.NotMessage`; no lock record; an `Identify` from the same client is answered |
| 18 | Flow stopped, then `message-nexus` started; separately, a second `message-nexus` started while the first lives | in both, no socket listens, the exit is nonzero, the trace names the cause (`FlowUnreachable`; `Taken.Address`, the first process still serving), and no retry appears |
| 19 | `message-nexus` killed, then started again | Flow's trace shows `Bind` answered `Bound`; the send of test 1 succeeds |
| 20 | A fresh store; a meta `Configure` that changes a socket path | `RestartRequired`; an ordinary `Configure` is then `Refused.AlreadyConfigured` (the marker is set); the seed before it was false |
| 21 | A version-1 store of old Message at the store path | start refused naming the path and version 1; the file's checksum is unchanged (fork F14) |

Flow's own lock contract is tested in `flow-test`, not here: a `Deliver`
under a lock never granted, `Release` after `Deliver` or after a lapse,
a lock whose `Until` is already past, `Refresh` or `End` refused while
a lock is held, and the 60-second default lease. This table keeps what
is observable through Message.

**Semi-sandbox `packages/message-flow-claude.nix`**, run with
`nix run .#message-flow-claude`, Haiku:

| # | Drive | Expect |
|---|---|---|
| 22 | Notice, then Order, to an asleep metaflow | `Queued`, then `Woken`; the woken flow's first prompt ends with `[ Notice.«…» Order.«…» ]`, the Order last |
| 23 | Order to an awake, working Claude flow | placed by Flow's rule (N8, fork F4); the recipient's transcript holds it once |

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
- **C3 `Lock.{ Sender Recipient }`.** The lock is time-bound, resting
  on the living's "time-bound so that it doesn't lock forever"
  (`flows/f5a6e9/vision/flow.md:59`, 2026-10-07) [V]. The request is
  `Lock.{ Sender Recipient }`; Flow's Library `Lock` is
  `{ Sender Address Until.Integer }`, `Until` in seconds since the
  epoch, and Flow answers `Locked.Lock` with that record and keeps
  the same record. Message therefore knows when the lock lapses and
  does not deliver after `Until`. These shapes are f5a6e9's ruling,
  current best, not before the living; `Recipient` is declared in
  Flow's Library (e846c2).
- **C4 `Sender.Address`.** f5a6e9's ruling (log line 148). The living
  has said only that routes bind sender and recipient by aspect and
  layer (speech across aspects, approved 2026-10-09, psyche-skills
  850fd27) [R]; that a Sender is an Address is not his word.
- **C5 `Identified`, `Taken`, `Unknown` and `Ended` carry Address.**
  Consequence of C2, same ruling (log line 148). The refusals
  themselves ground in "we need a registry to know which flow is
  active" (`flows/d4ae97/vision/flow.md`, 2026-10-07) [V].
- **C6 `Deliver.{ Lock Request }`.** The sender is inside the lock.
  f5a6e9's ruling, current best, not before the living; no word of the
  living.
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
- **N14** (Bind and gate, f5a6e9, current best, not before the living.)
  Who may call `Lock`, `Deliver` and `Release` on Flow's
  ordinary socket: answered by f5a6e9 (current best, not before the
  living). Flow reads the peer's kernel credentials and accepts these
  three only from the exact process Message bound at its start (pid and
  start time equal, no ancestor walk), refusing any other peer
  `NotMessage`. `Bind` is taken on Flow's ordinary socket, so Message
  keeps only Flow's ordinary path. A `Bind` under an address whose bound
  process is gone (its pid and start time no longer name a live
  process; how that is read atomically is not specified or proven)
  replaces the binding and is answered `Bound`; `Taken.Address`
  comes only while the old process lives.
- **N8** Where a request lands in an awake flow: ruling 3 of
  «The Flow Nexus vision», third edition (book 17), (a) end of the
  prompt, (b) a tool-call return, (c) other. This is fork F4.
- **N11** The lease is Flow's own setting: `Configure.Nexus` gains
  `Lease.Integer`, in seconds, 60 by default (f5a6e9's ruling,
  current best). The living's book «How long Flow's lock lasts» is
  still open; the value waits on it.
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
  become one `Standard` record in schema version 2. The new store path is
  the old one, which holds the version 1 store; it is not read, not
  reset and not migrated until fork F14 is ruled, and Message refuses to
  start on it, naming it. The ledger is not carried [I].
- **Meta admission.** The MetaAspects list goes; the meta socket
  admits the owner only [I].
- **Flow's gate.** Flow accepts `Lock`, `Deliver` and `Release` only from
  the Message process bound at start; today it admits peers on its meta
  socket by a list.
- **Tests.** Today they run the real message-nexus against a
  scripted fake Flow, and no test runs Message with a real Flow or a
  real Herdr. `message-test` runs both real Nexuses.
- **Kept.** Framing and the 1 MiB limit, sockets at mode 0600, the
  `SO_PEERCRED` and start-time read, Flow's ancestor
  walk matching a Flow record's `Process`, Flow's body check that refuses a sigil command such as
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
  `Up` relative to the `Sender` on the lock (`Lock.{ Sender Recipient }`;
  f5a6e9's ruling, current best, not before the living). The living
  said "I don't know" who resolves it. A ruling for Message moves the
  resolving into Message, which has the sender's Address from
  `Identify` and writes the layer above itself, without changing the
  wire: `Send.{ Recipient.[ Address Up ] Request }` and
  `Deliver.{ Lock Request }` stay as they are, and the lock Message
  passes carries the resolved Address.
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

- **F14** The old store. The new store path
  (`$HOME/.local/state/message/message.sema`) is the path old Message
  used. A store there holds schema version 1 with four tables, among
  them `message_nexus_configuration` with the five-field
  `MessageConfiguration` (ordinary, meta, flow, flow_meta, meta_aspects).
  Options: (a) refuse an old store for good and require the owner to
  remove it; (b) move it aside under a name and start a new store;
  (c) migrate its configuration into `Standard`. No option resets it
  silently, and none infers `MetaConfigured` for it. Until the living
  rules, Message refuses to start on it and names the path and the
  version; the file is left as found. Needs the living.

## 13. Findings for Mind

- **X1** ethos-zero 16.0.0 refuses f5a6e9's Library as written.
  `Topic:Name` is rejected `Expected.Declaration` and
  `Blake3.Bytes<32>` is rejected `Name.32` (witnessed by Check on
  one-line files). Until the generator reads both, `Topic` is
  `Topic.String` (designed `Topic:Name`) and `Blake3.String`, 64 hex
  characters (designed `Blake3.Bytes<32>`).
- **X5** One enum cannot hold two variants of one name: ethos-zero
  16.0.0 rejects `Unknown.Address` beside `Unknown.Lock` with
  `Duplicate.Unknown` (witnessed by Check). Message writes
  `Unknown.[ Address Lock ]`, which prints `Refused.Unknown.Address`
  and `Refused.Unknown.Lock`; Flow's own refusals must take the same
  shape or name the two differently. Flow's to rule.
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
  the kernel's start time of the pid. Message reads the pid from
  `SO_PEERCRED` and the start time from `/proc/<pid>/stat` field 22.
  The pid-reuse guard (pid plus start time) has no concrete atomic
  algorithm specified or proven yet: the two reads are separate
  steps, and what makes the pair belong to one process is open.
  Nothing in this design is proven about it.
- **X5** ethos-zero 16.0.0 `Check` reads one file and does not resolve
  an import across files, so the five files do not Check together as
  a unit. The imports were read against the published sources, fetched
  from GitHub into a scratch clone: Flow 0.25.0 is
  `LiGoldragon/flow` 962ad12, which pins `signal-flow` 11.0.0 at
  068f0e and `meta-signal-flow` 15.0.0 at 88f375
  (`Cargo.toml:17-18`). Each name the five files import, and where it
  is declared at those exact revisions (a version number alone proves
  no import resolves):

  | Name | Imported from | Declared at |
  |---|---|---|
  | `FlowId` | `signal_flow` (message.operation) | signal-flow 068f0e `ethos/signal.ethos:123`, `FlowId.String` |
  | `Address` | `signal_flow` (operation, signal) | absent from all three; waits on Mind's next Library candidate |
  | `Request` | `signal_flow` (operation, signal) | absent from all three; waits on Mind's next Library candidate |
  | `Lock` | `signal_flow` (operation, signal) | absent from all three; waits on Mind's next Library candidate |
  | `Recipient` | `signal_flow` (operation, signal) | absent from all three; waits on Mind's next Library candidate |
  | `Process` | `signal_flow` (operation, signal) | absent from all three; waits on Mind's next Library candidate |
  | `Sender` | `signal_flow` (message.operation) | not declared in signal-flow 068f0e or flow 962ad12; meta-signal-flow 88f375 `ethos/signal.ethos:132` declares a different `Sender.[ Flow.FlowId Owner ]`, which is not in `signal_flow` and not the `Sender.Address` Message uses; waits on Mind's next Library candidate |
  | `Configuration` | `message_library` (memory, meta.signal, operation, signal) | Message's own `message_library.ethos:5`; not imported from Flow (meta-signal-flow 88f375 `ethos/signal.ethos:94` declares an unrelated `Configuration`) |

  No file imports from `meta_signal_flow`. Flow 962ad12 declares
  only `crates/flow-nexus/ethos/operation.ethos`, which imports from
  `signal_flow` and declares none of these names. Of the eight
  imported names, one (`FlowId`) is declared in a published
  revision, one (`Configuration`) is Message's own, and six (`Address`,
  `Request`, `Lock`, `Recipient`, `Process`, `Sender`) are absent
  from all three and wait on Mind's next Library candidate. Each
  declaration was witnessed by grep at the stated file and line.

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
- Witnessed by this flow: `ethos-zero Check` on the five ethos
  blocks in section 4 and on the five draft files in
  `reports/message-flow/`, after the `Bind`, `Bound`, `NotMessage` and
  `Taken.Address` additions (all `Checked`); and on the `Topic:Name`
  and `Bytes<32>` lines (both `Rejected`).
- Provenance receipt: unavailable; no PROVENANCE handoff exists for
  this run.
