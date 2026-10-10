# Letters, Roles, Monikers — a design book from the ground up

Fable b7ba00, Psyche, 2026-09-26. Written on the living's request (via Psyche Opus 93ba9f) as one of two independent books; the next distilled vision is drawn from both. Every rule below is a proposal until the living rules; the living's own words are quoted where they bind, and each fork is marked **Fork**.

Ground the living has laid (all verbatim in `flows/b7ba00/vision/`):

> We need a very streamlined and aerodynamic messaging interface so that there is very little noise. I don't want resistance, I don't want all these hashes, and I don't want all this extra unnecessary information. Even if the ordinary message API is complex, we create a shorthand version which has a shorthand response type or display type.

> Datom doesn't have tags, has variants.

> Ultimately everything becomes a type because everything is a variant of a set.

> A lot of this data that you're spreading over this single [struct] actually is data that belongs in the data portion of a variant.

## Part 1 — Letters

### 1.1 What a reader needs

A flow reading its pane needs four things: who speaks, what kind of speech act it is, the words, and how old they are. Nothing else belongs on the pane. Delivery grades, receipts, and identifiers are machinery; they answer the sender's call and the history interface, never the reader's eye.

> I saw one message coming from it and it had a bunch of fields in there that I don't want to see.

### 1.2 The psyche as a top-level shareable thing

The living's words are the highest-value content a message can carry. A psyche is its own type, shareable on its own, and comes in a short and a full form. The short form is what a reader needs to act; the full form is the record.

```
Source.[ Stt Typed Unknown ]                       ; how the living's words were captured
Psyche.{ Context Verbatim Source }                 ; short: the context, the whole verbatim, its source
Moment.{ Date Time }
PsycheRecord.{ Psyche Moment Heard Topic }         ; full: + when it was said, which seat heard it, which record holds it
```

`Heard` is a `Seat` (Part 2); `Topic` is the record's topic name (`messaging`, `wordIds`). Nothing else is metadata yet.

> Maybe the short psyche is not so much that the date is missing, but maybe there are other fields too that are not there. It could be in the metadata but we don't need to obsess over metadata. Let's just put it in as we need it.

**Fork 1.** Should `Source` carry the transcription-correction marks (`[sic]`, bracketed corrections) as a separate variant `Stt.Corrected` / `Stt.Raw`, or stay three bare variants? Proposed: three bare variants; corrections live inside the verbatim as today.

### 1.3 Age

Time on the pane is an age, not a timestamp. The unit is the scale the age has reached.

```
Age.[ Seconds.Int Minutes.Int Hours.Int Days.Int Months.Int Years.Int ]
```

`Age.Minutes.3` renders as `3m`. The `Moment` stays in the full forms and in history.

### 1.4 The sender

The sender is a seat, or the living. "Owner" is gone. For now the seat is named by the caller; eventually the machinery derives it from the process that called.

```
Layer.[ Primary Secondary Tertiary Quaternary ]
Seat.[ Psyche.Layer Mind.Layer Field.Layer ]
Sender.[ Living Seat.Seat ]
```

Written out, `Seat.Psyche.Primary` is spoken as PsychePrimary. The set of all senders is the closed set `Living ∪ 3×4 seats`.

> The message has to be able to figure out who the sender is programmatically eventually from the process that called, but for now the sender is psyche primary or psyche secondary, etc. … We could make a set of all of them and variants.

**Fork 2.** The record holds two layer vocabularies from the same day: `Primary … Quaternary` (the latest correction, to 93ba9f) and "3 power levels … high, medium, low; ultra-low roles are usually temporary" (to e167d8, `flows/e167d8/vision/roles.md`). Proposed: the four layer words are the type; whether a Quaternary seat is normally live is a roster question, not a type question.

### 1.5 Kinds of message

A message is a speech act; its kind is the head, so a reader sees it first.

```
Kind.[ Order Question AuditRequest InformationRequest ]
```

These four are the living's. A report, an answer, a readiness notice are common today and need a home.

**Fork 3.** Add `Report` and `Answer` (an `Answer` carries nothing more; a reply is a message whose kind answers a `Question`), or leave replies typeless as a `Simple` whose kind is `InformationRequest` answered? Proposed: add `Report` and `Answer`; the living names any further kind.

### 1.6 Simple and full

```
Simple.{ Sender Kind Text }
Full.{ Sender Kind Text Vector<Psyche> Age Moment }
Letter.[ Simple.Simple Full.Full Psyche.Psyche PsycheRecord.PsycheRecord ]
Delivery.[ Soft.Letter MiddleAbrupt.Letter HardAbrupt.Letter ]
```

A `Simple` is the shorthand: one head, three positions. A `Full` carries its supporting psyches — the record it rests on — and is what a flow sends when it acts on the living's words. A `Psyche` alone is the living's words shared without commentary. The tier stays the outer head, as in the Ethos today, because the tier is the first thing delivery must know.

> A simple message, a simple psyche. A full message that can have many fields, one of which is a vector of psyches that are essentially the support for that message.

There is no message identifier anywhere in a letter. History is its own interface (1.8).

### 1.7 The display type

The API type above is what the machinery moves. What lands on a pane is a display type: a rendering chosen by the reader's harness, not a second schema. Two renderings, one per audience.

Human (the living's pane, and any flow's pane when it reads):

```
PsychePrimary · Order · 3m
Regenerate the ouranos proposal against goldragon main.
```

Machine (a flow that parses):

```
Soft.Simple.{ Psyche.Primary Order «Regenerate the ouranos proposal against goldragon main.» }
```

A psyche shared on its own renders in the human form as the context line, then the verbatim as a quotation, then `Stt · 2h`.

**Fork 4.** Does the living want the human rendering on every pane by default, with the machine form only on request, or the machine form on flow panes? Proposed: human by default everywhere; the machine form is what `History` returns.

### 1.8 History, receipts, and the raw send

History replaces the message id: a letter is addressed by who and when.

```
History.[ Last.Int Since.Age Between.{ Seat Seat } From.Sender ]
```

Receipts (`Submitted … Read`) stay in signal-message as they are; they return to the sender's call and to `History`, never to the recipient's pane.

The raw pane send — typing into a harness — is a meta-socket operation of Flow; ordinary messages go through the lock-enabled `Deliver` of Message.

> A raw flow send (as in typing directly into the pane, into the harness) I think should be a meta socket operation and then we have a more lock-enabled deliver message.

What changes against the Ethos on `s1-e167d8` / `s2-e167d8`: `MessageId` leaves `Letter`; `Sender.Owner` becomes `Living`; `Sender.Flow.FlowId` becomes `Seat.Seat`; `Content.[ Text Psyche ]` becomes `Letter.[ Simple Full Psyche PsycheRecord ]` with `Kind` and `Age`; `Acknowledge.MessageId` and `QueryReceipts.MessageId` become `History` queries. Every consumer is updated; nothing is kept for compatibility.

## Part 2 — Roles

### 2.1 Data in the variant's data

Effort is a property of a model, so it is the model variant's data; each model carries its own scale.

```
Effort.[ Low Medium High ]
Model.[ Fable.Effort Opus.Effort Sonnet.Effort Haiku.Effort Astra.Effort Sol.Effort Luna.Effort ]
```

> When you're talking about the effort, there are different effort levels for different models so it's a property, the data of the model variant.

The harness is derived from the model (Fable, Opus, Sonnet, Haiku run in Claude; Astra, Sol, Luna in Codex); it is written only when one model runs in more than one harness.

**Fork 5.** Write `Harness` now as a field of `Role` (the living: "I guess you can put it in"), or derive it until a second harness for one model exists? Proposed: derive; the roster's model table names the harness once per model.

### 2.2 Role, roster, addendum

```
Addendum.[ File.Path Vision.Topic Skill.Name Mind.Reference ]
Role.{ Seat Model Vector<Addendum> }
Roster.Vector<Role>
```

A role is a seat with its model and its addenda: the extra prompt material fed to a new flow from files, from a vision topic, from a skill, or from the Mind once the Mind Nexus exists. The roster is the list of configured flows; it is the only set anything may launch from.

> We should have a list of flows all programmed with their datom configuration. That's one of the inputs it gets, fed into a new flow, plus addendum things that are added into the prompt from files, I guess, or from a certain reference in mind when we have the Mind Nexus or whatever (different sources). Different variants.

Shorthand names are the roster's own names for its roles: PsycheFable is `Role.{ Psyche.Primary Fable.Medium [...] }`; PsycheSecondary is the Opus role at the secondary layer.

**Fork 6.** Is "the psyche fable" a role above Primary (a fifth layer), or the Primary role whose model is Fable? Proposed: the Primary's model; there is no layer above Primary.

### 2.3 Launch, and what the code forbids

```
Predecessor.[ None Flow.FlowId ]
Launch.{ Role Predecessor }
LaunchRejected.[ UnknownRole SeatOccupied.FlowId EffortUndeclared ]
```

The code refuses a launch when the role is not in the roster; when a live flow already holds the seat (one live flow per seat — a refresh names its predecessor and takes the seat over); and when the effort asked for is not the one the role declares. High effort is not forbidden; no role declares it today, so none launches at it.

> Sometimes it's not that all launches are frozen; it's that somebody launched too many flows that were on the same role and then launched the flow with too high an effort. … let's make sure the code makes sure it doesn't happen again.

> It's not that we don't allow high effort. It's just that we haven't made any flow. We haven't designed a flow that uses high effort so there shouldn't be any launched.

Refresh and reap are the two movements the roster admits: a flow with a big context is refreshed into a successor on the same seat; an abandoned flow is reaped. Field executes both once told; the decision is not Field's.

**Fork 7.** Is the roster itself Ethos (a type with twelve fixed roles), or data (a datom file of roles that the living edits)? Proposed: the types are Ethos; the roster is a datom file — the living changes a model or an addendum without a type change.

## Part 3 — Monikers: words in place of hashes

### 3.1 Name

The standard is called a **Moniker**: a PascalCase series of two or three words that stands for the random prefix of a hash. `b7ba00` becomes something like `AmberFalcon`; a title becomes `PsycheV2.{ Fable AmberFalcon }`.

> They would become a PascalCase series of words instead of hashes, which would actually be lighter on LLMs.

Earlier records hold the same thought: BIP-39 called "genius", a wish for more bit density, camelCase for ids against PascalCase for typed objects "if the LLM tokenizes it efficiently" (`flows/05c604/vision/identifiers.md`), identifiers as real types with security levels by collision cost (`flows/692df8`), and the name-based hash placed in the signal library (`flows/fd0f97`).

### 3.2 Entropy per use

Formula: `k` words from a list of `N` carry `k · log2 N` bits; `n` hex digits carry `4n`.

| use | bits needed | form |
|---|---|---|
| Flow ID (today six hex) | 24 | 2 words, list of 4096 |
| commit / transcript prefix | 36 | 3 words, list of 4096 |
| secure identifiers | ≥ 128 | stay hashes; a moniker is only a handle |

A 4096-word list gives exactly 24 bits for two words and 36 for three; BIP-39's 2048 gives 22 and 33, which is why the living asked for more density. The list is a power of two, fixed and versioned once a moniker is minted against it, and vetted as BIP-39 and the PGP word list are: no homophones, no confusable pairs, unique short prefixes.

### 3.3 Measured cost (local Llama-3 BPE tokenizer, 20 samples each)

| form | tokens |
|---|---|
| six hex (`b7ba00`) | 3.5 |
| twelve hex | 6.9 |
| forty hex | 22.3 |
| two words (`AmberFalcon`) | 3.8 |
| three words (`QuietRiverStone`) | 5.4 |

At Flow-ID length the two are equal; from twelve hex up, words win. The list must be chosen for single-token words: this sample's "Crimson" and "Meadow" split, so a vetted list measures each candidate word's token count and keeps only the ones at one token. That is the measurable criterion the living asked for.

### 3.4 The converter

The hash is authoritative; the moniker is a projection of its random prefix.

```
WordList.{ Version Vector<Word> }                 ; 4096 words, fixed order
Moniker.[ Two.{ Word Word } Three.{ Word Word Word } ]
ToMoniker.{ Hash Width }                          ; Width.[ Two Three ]: take the leading 24 or 36 random bits, slice by 12, index the list
ToHash.{ Moniker }                                ; concatenate the indices; resolve the full hash by prefix lookup in the store that minted it
```

For a Flow ID the random prefix is the first 24 bits of the session identifier, which is what the six-hex alias already is. For a commit or a transcript the prefix is the leading 36 bits; a collision inside one store is resolved as short hex prefixes are today — by lookup — and, when ambiguous, by one more word. The converter lives in the signal library, and every tool that prints an identifier prints the moniker and accepts either form.

**Fork 8.** Word case: the living has said both "PascalCase series of words" (today) and, earlier, camelCase for ids against PascalCase for typed objects (`05c604`). Proposed: PascalCase, as the latest word; a moniker never collides with a type because it stands in a value position.

## What this book asks the living to rule

1. The four message kinds, and whether `Report` and `Answer` join them (Fork 3).
2. The human rendering as the default on every pane (Fork 4).
3. The four layer words as the type, with ultra-low as a roster matter (Fork 2).
4. The roster as a datom file over Ethos types (Fork 7).
5. "Moniker" as the name, PascalCase, a 4096-word list vetted by token count (Forks 8, 3.3).

Sources: `flows/b7ba00/vision/{messaging,modelFlows,flowAnatomy,wordIds,types,designBook}.md`; the Ethos on `signal-message@s2-e167d8` and `meta-signal-flow@s1-e167d8`; `flows/93ba9f/reports/letter-anatomy-2.md`, `roles-anatomy-2.md`; `flows/e167d8/vision/{roles,layerVocabulary}.md`; `flows/e51411/vision/messaging.md`; `flows/d8df70/vision/messaging.md`; `flows/05c604`, `692df8`, `fd0f97`, `9993b5` identifier records; measurement by a subflow of b7ba00 with llama-tokenize on the Llama-3 BPE vocabulary.
