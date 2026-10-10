# Signal and Sema: a distillation proposal

Composed by Fable 056f6d, 2026-09-18, from the candidate gathering at `reports/signal-sema-candidates.md` (revision 6e59653a, about 75 records). This is a proposal. Nothing here stands in Vision until the living approves each statement. Every statement names the topic it lands in. Every example is written from the vision, not from running code, as the living asked; where the example goes past what any record says, it is marked as this flow's proposal for the living's word.

Authority note: most of what follows rests on raw living records not yet distilled. Their authority is unchanged by that. Vision/signal.md today carries six headings from seven references; Vision/sema.md carries one heading of four sentences. The gathering found about thirty qualifying Signal records and at least ten Sema records.

## Part one: the questions the living must answer first

Five contradictions in the raw block any statement that assumes their answer. Each gives both dates.

**Q1. Is there a Nexus layer described in ethos, or only Signal and Sema?** On 2026-09-10 the living said the nexus-core runtime concept was overthinking: signal gives the main types, sema the database types. On 2026-09-13 and 2026-09-14 the living said the signal layer, the nexus layer and the sema layer are described in ethos, named Nexus, core and metaNexus as the explicit terms, and asked whether the compiler can enforce that the signal actor never talks to the sema actor except through the Nexus. The later words reassert what the earlier correction removed, and they name a Nexus ethos type file that Vision/ethos.md says does not exist. Reading: the 09-14 words were exploratory, in artifact comments, ending in a question. Until ruled, the statements below assume two ethos roots, Signal and Sema, and say nothing about a Nexus root. Which is it?

**Q2. Observe: flat or nested?** On 2026-08-26 at 14:22 the living said Observe is the root variant containing another enum. At 17:54 the same day: "Actually, Observe.Locks is best. If another kind of lock comes, then we can add it as such; Observe.ExpiredLocks." The statement below takes the later, flat form. Confirm?

**Q3. Where does sema.ethos live?** On 2026-08-25: when designed, the nexus and sema ethos live in the Nexus's main repository. On 2026-09-16 the living asked whether a special repository is needed for trait isolation, or whether build-time crate paths suffice, and an agent-authored orders file has since answered it as a fourth repository named sema-<nexus> with no approval. The statement below keeps the 08-25 ruling. Does the 09-16 question change it?

**Q4. Universal signal: is CapnProto still on the table?** On 2026-08-13 the living named a CapnProto transcodable form as universal signal for non-Rust front-ends. On 2026-09-10, asked directly, the living said portable rkyv plus a protocol to be decided, marked TBD. Vision/signal.md carries only the 09-10 shape, and the non-Rust front-end problem has no answer anywhere in the corpus. Does the 09-10 answer retire CapnProto, or defer it?

**Q5. The router words of 2026-09-13: Vision or Notion?** The same utterance, "the router becomes the manifest; the enum is the router signal", is logged at Vision level by one flow and at Notion level by another. The statement below on routing draws only on the 2026-08-11 record, which is unambiguous. Which level do the 09-13 words hold?

Three smaller questions sit beside their statements: Q6 on the second standard handshake, Q7 on the record-type name, Q8 on Lock as the worked example.

## Part two: proposed statements for Vision/signal.md

Each heading is a proposed statement. Existing headings in Vision/signal.md that stand unchanged are not repeated: Name, What signal is, Meta signal, Protocol.

### Every component speaks signal; datom only at the edge

All components speak signal, never datom. Datom is used only at the edge, so that text-based systems, thinking machines and existing editors, can read and write what a Nexus says. The Nexus never textualizes. The same signal library compiled for the CLI derives the datom kinds; compiled for the Nexus it carries no textualization at all.

Sources: 2026-08-26 ac1e9ec8 datomSyntax; 2026-09-09 564f55 signal; 2026-09-15 05c604 nexus. The Rust of the compile split already stands in Vision/ethos.md; this statement gives the rule its home in the signal topic.

### A query is an imperative verb, and may be refused

A query is a verb in the imperative: Send, Start, Observe. It is a request by virtue of its slot, so the word request is never part of its name. Because it can be refused, every query has a typed refusal beside its reply: the reply is the verb's past tense, the refusal names itself and carries the reason as a variant. Errors are vocabulary, never strings.

Sources: 2026-08-26 01a03d6e ethosInterfaces; 2026-09-13 024bc7 signal; 2026-08-27 b675f3d9 kinds (register.{[PathLock] Registered Refused}).

```
; Signal — the ordinary socket of a message Nexus. Sections in order: imports, queries, responses, types.
; Every query is a verb; its reply is the past tense; its refusal names itself.
Signal
[ signal:[ FlowId Origin ] ]                                      ; imports: shared types from the signal library
[ Send.Message  Describe.MessageId  Observe.Selection ]           ; queries
[ Sent.Receipt  SendRejected.SendRejection                        ; responses, reply beside refusal
  Described.MessageRecord  DescribeRejected.DescribeRejection
  Observed.Observation ]
[ MessageId.Hash256                                               ; types
  ShortId.Hash32                                                  ;   the truncated form of a MessageId
  Sender.FlowId
  Recipient.FlowId
  Body.String
  Message.{ Sender Recipient Body }
  Receipt.{ ShortId Origin }                                      ;   minimal by default
  MessageRecord.{ MessageId Sender Recipient Body Origin }        ;   the full form, by explicit call
  SendRejection.[ UnknownRecipient.Recipient  RecipientUnavailable.Recipient ]
  DescribeRejection.[ UnknownMessage.MessageId ]
  Selection.[ Inbox.FlowId ]
  Observation.[ Inbox.Vector<Receipt> ] ]
```

```
; datom, in a position expecting Query, then the Response each receives
Send.{ 056f6d 0ab019 «Manifest landed at revision 6e59653a» }
Sent.{ 9f3ac1e0 Cli.{ 3727637 message } }

Send.{ 056f6d efa157 «Are you there?» }
SendRejected.UnknownRecipient.efa157

Describe.9f3ac1e0b7c2d4a6f19e8d3c5b7a2f4e6d8c0b1a3f5e7d9c1b3a5f7e9d1c3b5a7
Described.{ 9f3ac1e0b7c2… 056f6d 0ab019 «Manifest landed at revision 6e59653a» Cli.{ 3727637 message } }
```

Hash256 and Hash32 are the typed identifier forms of the statement on identifiers below.

### A response is minimal by default; the full form by explicit call

Replies are small. Long hashes and identifiers appear truncated in the default reply, and fields not needed to act stay in the store, queryable. A separate query, with the explicit longer name, returns the full record. This is a design standard for every Signal.

Source: 2026-09-15 692df8 signal. In the example above, Sent carries a ShortId and Describe returns the MessageRecord.

### Identifiers are typed, and the type lives in signal

An identifier is a real type, never a string: a hash of a stated bit width, in a base legal as a bare datom run. The identifier types, and the definition of a legal symbol, live in the signal library, because sema stores signal, so it is all signal.

Sources: 2026-09-15 692df8 identifiers; 2026-09-15 fd0f97 identifiers.

```
; Library — the identifier types of the signal library, imported by every Signal
Library
[]
[ Hash256.Bits<256>            ; a full identifier; printed as a bare run in a datom-legal base
  Hash32.Bits<32>              ; a truncated identifier, the default in a minimal reply
  FlowId.Hash32
  ProcessId.Integer ]
[]
[]
```

The Bits<n> intrinsic is this flow's proposal for how a bit-typed identifier is declared; no record names it.

### Observe opens a subscription; the connection is the subscription

Observe is a query whose reply repeats: one Observed frame carrying the state on open, then one for every later change, on the same connection, until the peer closes it. There is no token and no Unwatch; a peer that stops reading has unsubscribed. Each observable is its own flat variant: Observe.Inbox, Observe.Locks, Observe.ExpiredLocks. A correct system goes quiet when nothing changes.

Sources: 2026-08-26 01a03eda observe; 2026-08-27 acbb6006 nexus; Vision/nexus.md Observation by subscription. Pending Q2.

```
; datom: the query once, the response as many times as the inbox changes
Observe.Inbox.056f6d
Observed.Inbox.[]
Observed.Inbox.[ { 9f3ac1e0 Cli.{ 3727637 message } } ]
Observed.Inbox.[ { 9f3ac1e0 Cli.{ 3727637 message } } { 2c7b44d1 Nexus.flow } ]
```

### A Nexus knows who speaks to it: the origin handshake

There are two standard signal handshakes. One checks the origin process of the call, so the Nexus knows where a message came from: which process ran the CLI that made the signal. It is a standard, optional part of the signal library, so whoever speaks to a socket knows to say whether it carries the process identity. The chain is kept: the process that launched the CLI call that created the signal that created this request.

Sources: 2026-09-16 efa157 callerIdentity (handoff-only); 2026-09-17 9993b5 callerIdentity; 2026-09-18 b05237 operational-signalOriginHandshake.

```
; Library — the origin part of the signal library. This shape is this flow's proposal;
; the living asked to be shown how it could be done and to be asked.
Library
[]
[ Executable.String
  Origin.[ Cli.{ ProcessId Executable }      ; the CLI's own process, read through the socket
           Nexus.ComponentName               ; another Nexus on an edge
           Unstated ]                        ; the peer did not say
  Handshake.{ Origin } ]
[]
[]
```

**Q6.** The record names two standard handshakes and describes one. What is the second?

### Signals cross the network through a router; the router enum lives in the signal repository

Across the network a router tells signal types apart by an enum, held in the signal repository every component depends on, that wraps the objects. That repository also holds what every signal needs in common, the handshake payload among it.

Source: 2026-08-11 012fbf07 threeStacks. Already in Vision/nexus.md Routing; proposed here so the signal topic carries its own wire statement. Pending Q4 and Q5.

## Part three: proposed statements for Vision/sema.md

The existing heading, What sema is, stands. These are added.

### Sema stores signal

What a Nexus stores is signal: typed, binary, the same types its contracts carry. A record type is declared in the Sema root the way a query is declared in the Signal root, and it bears its kinds by implication, never written.

Sources: 2026-09-15 692df8 identifiers; 2026-09-04 6329f1 ethos; 2026-09-09 564f55 sema.

```
; Sema — the store of the message Nexus. Sections: imports, record types; the rest to be decided.
; Associations are implied: every record type bears the storage kinds.
Sema
[ signal_message:[ MessageId Sender Recipient Body Origin ]        ; imports from the Nexus's own Signal
  signal:[ Instant ] ]
[ StoredMessage.{ MessageId Sender Recipient Body Origin }        ; record types
  Delivery.{ MessageId Grade Instant }
  Grade.[ Submitted Transported Presented Read Completed ]
  Configuration.{ OrdinarySocketPath MetaSocketPath }
  Metadata.{ MetaConfigureDone } ]
```

**Q7.** The living left the name open: "a storage type or a record type (whatever you want to call it)". Vision/sema.md chose record type without a ruling. Record type, storage type, or another word?

### Sema is append-only and version-controls itself

A Sema is an append-only store that carries its own history, the way a version control system does. Repositories that hold data become nexuses that hold such databases, with an update and upgrade system built in.

Source: 2026-09-16 efa157 sema (handoff-only).

### A schema change is a typed operation: the migration comes with the edit

Editing the ethos that declares a Sema is operational editing. Every change to the specification is a typed operation, a structured, fully typed diff between the old spec and the new: which objects changed and how, data moved when it changes size, an upgrade operation. The migration comes out with the edit, and the edit sends a recompilation to test the component now.

Sources: 2026-08-08 55d18f4f everythingIsInTheDaemon; 2026-08-14 vision-raw rustComponentArchitecture; 2026-09-16 efa157 specificationVersionControl; 2026-09-13 bcd02a notion Ethos Delta, drawn on as a notion only.

```
; datom, in a position expecting SemaDelta — the typed diff one edit yields. Shape is this flow's proposal.
Upgrade.{ 3 4                                                   ; from schema generation 3 to 4
  [ AddedField.{ Delivery Attempts Integer 0 }                  ; record, field, type, default for existing rows
    WidenedField.{ StoredMessage Body String Meaning }          ; data moved: every Body re-encoded
    AddedRecord.Receipt ] }
```

### Configuration lives in the store

A Nexus's configuration is a record in its own Sema. A new store is seeded from the executable's constant defaults; an existing store holds the configuration that resumes. The standard metadata tree lives there too: whether the meta Configure was ever done, the socket paths, and everything standard about the Nexus.

Sources: 2026-08-26 01a03d6e nexus; 2026-08-27 acbb6006 nexus. Already in Vision/nexus.md Configuration and First configuration; proposed here as the sema-side statement so the store topic says what it holds. If the living prefers one home, it stays in nexus.

```
; datom, the meta socket: configuring, and reversing first configuration
Configure.{ /run/user/1001/message/message.sock /run/user/1001/message/message-meta.sock }
Configured.{ { /run/user/1001/message/message.sock /run/user/1001/message/message-meta.sock } true }
ReverseMetaConfiguration
OrdinaryConfigurationReopened.{ { … } false }
```

### The meta Signal is a Signal

The meta socket's contract is an ordinary Signal file: Configure as a query, its receipt as the reply, the reversal of first configuration as a second query. It imports the configuration type from the Nexus's ordinary Signal rather than redeclaring it.

Sources: 2026-08-09 98fbfa47 metaSignalNotOptional; 2026-08-26 01a03d6e nexus; 2026-08-27 acbb6006 nexus. The shape is this flow's articulation; no record draws a meta Signal file.

```
; Signal — the meta socket of the message Nexus
Signal
[ signal_message:[ Configuration ConfigurationReceipt ] ]
[ Configure.Configuration  ReverseMetaConfiguration ]
[ Configured.ConfigurationReceipt  OrdinaryConfigurationReopened.ConfigurationReceipt
  ConfigurationRejected.ConfigurationRejection ]
[ ConfigurationRejection.[ InvalidConfiguration ] ]
```

## Part four: a design-practice statement, new topic

One clause the gathering listed as an impurity is a rule about how design is done, and it governs this very report.

### Design works with visuals, examples, and traits with main types

Design is fleshed out with visuals, examples, and the traits with their main types; that is the design pattern. Every ethos block presented carries its root variant on its first line, mixes no species, and is situated in a comment saying what position it fills. Datom is preferred where a predictable example is wanted.

Sources: 2026-08-13 a5587095 protosIsTheSharedStyle; 2026-09-09 564f55 ethos; 2026-09-09 62022e8f designPractice. Proposed topic: Vision/designPractice.md.

**Q8.** On 2026-08-29 the living called Lock an extremely poor example when designing ethos. Vision/signal.md, Vision/sema.md and Vision/ethos.md all use Lock. This proposal uses a message Nexus instead. Should the standing Lock examples be replaced?

## Part five: what this proposal does not state

- No statement on the frame: no record describes a length prefix or a frame in the wire sense. The short header of 2026-08-09 was deferred by the living.
- No statement on the store's location or file extension: the one record says "the default location" and never names it.
- No statement on the architecture guard between signal, Nexus and sema actors, pending Q1.
- No statement on the router beyond the 2026-08-11 words, pending Q5.

## Part six: impurities this proposal discards on landing

Twenty-one working instructions sit inside the gathered records; the gathering lists each, quoted. They are instructions of their day (recover, dig, deploy, show me, restore the binary) and rule nothing; on landing they are destroyed with the archive move, not carried. One is not discarded: "visuals, examples, and traits with main types must become our design pattern" is proposed as the design-practice statement above.

## Sources

`reports/signal-sema-candidates.md` at revision 6e59653a, and through it the ~75 records it quotes, in particular: flows/55d18f4f, 6863ef19, ba906ae2, ac1e9ec8, 564f55, fe34eb, 05c604, 01a03d6e, 01a03eda, acbb6006, 024bc7, bcd02a, 692df8, fd0f97, 9993b5, b05237, 98fbfa47, e06e4c07, 01a02fd5, 6329f1, f426777b, 6cc91b, e1953c, 62022e8f, e8c4cc61, a5587095, 012fbf07, vision-raw/rustComponentArchitecture, and the handoff-only records of efa157 under flows/b49251/handoff. Existing distilled text: Vision/signal.md, Vision/sema.md, Vision/nexus.md, Vision/ethos.md, Vision/datom.md.
