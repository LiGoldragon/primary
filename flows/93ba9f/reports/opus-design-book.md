# Letters, Roles, Word Names, and the Field Tool

A design book, from the ground up. Psyche Opus 93ba9f, 2026-09-26. Written independently of Fable's book; compared afterwards.

## 1. Ground

These are the living's words the whole book stands on.

- "I want to specify an ethos type for our messages with different variants, and I want that to start becoming a standard way to communicate … It's going to be everywhere: all the CLIs, everything." (15 September)
- "You can have these shorthand types that are usually default, and then you have the more explicit longer name." Fields not needed "can just live in the database and be queryable." (15 September)
- "We need a very streamlined and aerodynamic messaging interface so that there is very little noise … I don't want all these hashes." (today)
- "Let's consider the flows as users. They're users of the messaging system. They don't need to know everything about how it works." (19 September)
- "The agents will know that it's me because of how the message is formatted. It won't be datom-formatted." (18 September)
- A message carries the psyche it rests on, because in the prompt "it reinforces the narrative better than just reading them." (25 September)

Four rules follow:
1. **Simple is the default.** Every message and every reply has a simple form. The full form is asked for by name.
2. **Nothing in a letter that the reader does not need.** No IDs, no timestamps, no empty or repeated fields.
3. **The sender is never written by the caller.** It is known from the process that called.
4. **The living is never a sender.** The living's own words arrive as plain text, not as datom. That difference is the mark.

## 2. The letter

### What exists today

On the rebuild branches (not on main, not in production):

```
Sender.[ Flow.FlowId Owner ]
Content.[ Text.String Psyche.{ PsycheContext PsycheVerbatim } ]
Letter.{ MessageId Sender Content }
Message.[ HardAbrupt.Letter MiddleAbrupt.Letter Soft.Letter ]
```

A real letter as it reaches a pane: `Soft.{ m-18d8eb22e06706ef001 Owner Text.«Hello from Message 0.16 …» }`. The message ID is a nanosecond clock plus a counter: it carries no information a reader can use.

### The redraw

```
Priority.[ HardAbrupt MiddleAbrupt Soft ]
Layer.[ Primary Secondary Tertiary Quaternary ]
Seat.[ Psyche.Layer Mind.Layer Field.Layer ]
Source.[ SpeechToText Typed Unknown ]
Age.[ Seconds.Integer Minutes.Integer Hours.Integer Days.Integer Months.Integer Years.Integer ]

Psyche.{ Context Verbatim }
FullPsyche.{ Context Verbatim Source Age Seat }

Kind.[ Order Question AuditRequest InformationRequest Report ]
Message.{ Kind Text }
FullMessage.{ Kind Text Vector<Psyche> }

Content.[ Message.Message Psyche.Psyche FullMessage.FullMessage FullPsyche.FullPsyche ]
Letter.{ Seat Content }
Delivery.[ HardAbrupt.Letter MiddleAbrupt.Letter Soft.Letter ]
```

- **The priority is the head.** "The soft message, the soft psyche" are the shorthand: the priority and the content's variant together say what arrived.
- **The sender is a seat,** `Psyche.Primary`, stamped by Message from the seat bound to the calling process.
- **A psyche is top-level.** Sharing a psyche is sharing something the living said. The simple psyche is context and verbatim. The full psyche adds how it was heard (`Source`), how long ago (`Age`), and which seat heard it.
- **Age is human time.** Seven minutes, three days: the unit chosen by scale.
- **A message has a kind:** an order, a question, a request for an audit, a request for information. `Report` is a proposed fifth, for returning work.
- **A full message carries its support:** the psyche entries it rests on.

In a pane:

```
Soft.{ Psyche.Primary Message.{ Question «Is Zeus deployed?» } }
Soft.{ Psyche.Primary Psyche.{ «context» «verbatim» } }
MiddleAbrupt.{ Psyche.Primary FullMessage.{ Order «Reap the old flows.» [ { «context» «verbatim» } ] } }
```

### Replies

Every operation answers in three registers, simple by default:

- **Simple:** one variant. `Delivered`, `Parked`, `Held.RecipientWorking`, `Refused.ComposerOccupied`.
- **Human:** one sentence, for display. `Human.«Delivered to Field Sol; he is working on it.»`
- **Full:** every field, asked for explicitly, never by default.

### History instead of IDs

No message ID in the letter; no acknowledging or fetching by ID. Message keeps its ledger. A flow asks for history by what it knows: "my last letters to Field Sol", "what Fable sent me in the last hour". The read witness is the recipient's reply.

## 3. Delivery

Already true in the rebuild: only Flow writes into panes, and only through its privileged socket. `Deliver` holds the pane's lock; `Command` sends `Compact` or `Interrupt`. Your comment asked for exactly this, and it is built. There is no unlocked raw typing operation; your comment on the book suggests one for the privileged socket beside the locked deliver.

Rules from your words:
- **Soft** waits until the recipient is at rest. **Middle abrupt** lands at the next tool call. **Hard abrupt** interrupts. (17 September)
- **An undeliverable letter escalates:** the higher seat of the same aspect, then the lower. The sender is told what happened. A missing crucial flow is started; every medium and high seat is crucial. (24 September)
- **After a replacement,** the reply goes to the successor, and the successor knows what its predecessor sent. (19 September)
- **A quiet channel** carries small information, like remaining quota, without arriving as a user prompt. (19 September)

## 4. Roles

```
Effort.[ Low Medium High Xhigh ]
Model.[ Fable.Effort Opus.Effort Sonnet.Effort Haiku.Effort Astra.Effort Sol.Effort Luna.Effort ]
Source.[ File.Path Vision.Topic Skill.SkillName Mind.Reference ]
Role.{ Seat Model Vector<Model> Vector<Source> }
Roster.Vector<Role>
```

- A role is a seat, its model carrying its effort, the models it may launch as subflows, and what is added to its first prompt.
- A launch names a seat. Flow refuses a second live flow on a seat, and refuses a model or effort not in the roster. Replacing a seat stops the old flow first, and a refresh reaps its ancestor.
- Fable is a model, not a seat: "Psyche Fable and Psyche High are synonymous for now." Today's Psyche Primary runs Fable.

```
{ Psyche.Primary Fable.Medium [ Opus.Medium Sonnet.Medium Haiku.Medium ] [ Skill.main-flow ] }
{ Psyche.Secondary Opus.Medium [ Sonnet.Medium Haiku.Medium ] [ Skill.main-flow ] }
{ Field.Quaternary Luna.Low [ Luna.Low ] [ Skill.main-flow ] }
```

## 5. Word names

The living: "replace hashes with words … a PascalCase series of words … a converter … into the hash."

### Already built, unused

On an unmerged branch of the signal library, an earlier flow built what you asked for then:

```
LocalNameReference.{ Integer Integer Integer }
ClusterNameReference.{ Integer Integer Integer Integer Integer Integer }
PublicNameReference.{ Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer }
```

Three security levels by how bad a collision is: local 3 words, cluster 6, public 12. The words come from BIP-39 (2048 words, 11 bits each). The name is read from a BLAKE3 digest, and it displays in camelCase: `quietRiverStone`.

### What the research adds

- A six-hex flow ID costs 4.3 tokens on average, up to 7. Three words from a single-token list cost exactly 3.
- About 1,024 capitalized words are single tokens once words that sound alike or look alike are removed: 10 bits a word. BIP-39's 11 bits cost more tokens per word.
- Almost nothing in daily use is really a hash. Flow IDs are 24 random bits cut from the session's ID. Message IDs are a clock. Lock IDs are a counter. A flow ID has already collided with a commit name in the repository.

### Proposal

- **Keep the built anatomy** — three levels, real types, camelCase display — and merge it.
- **Swap the list** for a 1,024-word single-token list without homophones: local 3 words = 30 bits, enough for flow IDs.
- **Name the standard.** Candidates: Wordprint, Saybits, Mnemonid, Tokenword, Hashspeak. (Fable proposes Monikers.)
- **One converter** in the field tool, word name ↔ hash bits ↔ the thing it names (a transcript, a commit).

## 6. The field tool

What exists:
- **field-clj** has three operations: commit, commit to a named remote, observe. Its commit is unsafe (a refusal rewinds other flows' work) and the safe rebuild has not landed. The installed build is two commits behind.
- **No Field Nexus** exists: no repository, no Ethos, nothing deployed.
- **No transcript tool on the path.** The one the skills name was never installed. A Claude-only script works when run by its path. Only one tool reads Codex transcripts, and it needs a model.

Proposal: field-clj grows now, the Field Nexus is written from its Ethos later.
- **Commit:** the safe rebuild, one landing workspace, fast-forward only.
- **Transcripts:** find a flow's transcript by its word name or flow ID, in both harnesses; read its tail; search the living's words.
- **Observe:** Flow, Message, Herdr panes, locks, in one view.
- **An Ethos index of the calls,** one API per harness underneath.

## 7. Found on the way

- **Any flow can release any other flow's lock** by guessing its number: Orchestrate checks no owner, and lock numbers are a counter.
- **Two instructions contradict:** one requires full forty-character commit hashes to prove a push, another forbids a helper from returning any hash that long.
- **The messaging tool refuses most sends** to Codex panes and to Fable, while accepting sends to Claude panes.

## Questions

1. Is the letter redraw the shape you meant — priority as head, the seat as sender, four content variants (message, psyche, full message, full psyche)?
2. Is `Report` a fifth message kind, beside order, question, audit request and information request?
3. Three registers for replies — simple, human, full — with simple the default?
4. Merge the built word-name anatomy, swapping in a 1,024-word single-token list? And which name?
5. Should the lock, instruction and messaging-tool faults go to the Field now?
