# Signal and Sema — psyche record candidates for distillation

Gathered by a read-demanding subflow of Fable main flow 056f6d, medium effort,
2026-09-18, at revision `6e59653a` (the revision of
`flows/056f6d/reports/vision-corpus-manifest.md`, used as the file index).

Per the `psyche-distillation` skill this subflow **only gathers candidates**.
Nothing here is a distilled statement; nothing here is re-articulated. Every
psyche quote is verbatim from its record file. Agent-authored context inside a
record is marked as the record itself marks it. Where a heading body exceeds 40
lines the first 40 are given and the cut is marked.

Searched: `Vision/`, `Vision/archive-*`, `Vision/sources/`, `Intent/`,
`vision-raw/` (and its `archive-` files), `flows/*/vision/` (and `archive-`
files), `flows/*/notion/`, and the two handoff bundles
`flows/b49251/handoff/psyche-medium-v1/modules/sources/` and
`flows/f55ec8/handoff/successors-v7/sources/`.

Two findings about coverage, stated before the groups:

- The `Vision/` copies inside **both** handoff bundles are byte-identical to
  the live `Vision/signal.md`, `Vision/sema.md` and `Vision/nexus.md`
  (`diff` witnessed, all three, both bundles). The bundles add nothing there.
- The bundles are **not** redundant for raw records: the flow `efa157` has no
  `flows/efa157/` directory in this repository at this revision, and its psyche
  records survive only inside
  `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/`.
  Two of them — `sema.md` (two records) and `callerIdentity.md` (one record) —
  are among the most load-bearing Sema and Signal records in the whole corpus
  and are **invisible to any search of `flows/*/vision/`**. They are marked
  `[handoff-only]` below.

`flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/ordersToCodex-2026-09-16.md`
was read and is **excluded**: it is agent-authored orders, not a psyche record.
Its `sema-<nexus>` contract-crate proposal is noted under Contradictions only
because a reader may mistake it for psyche.

---

## Group A — what signal is

### A1 — `vision-raw/archive-encodedFormIsTheCode.md`
Heading: `# "The encoded form is the code"` (file-level, undated heading)
Date: 2026-08-06 (captured 2026-08-08) · Level: raw (vision-raw, archived)
Provenance: `— psyche, 2026-08-06T21:53:42Z (Designer session 5abf3be8; entry captured 2026-08-08 from the session transcript during the rulings-audit backfill)`

> So we agreed that there would be a different type for every kind of
> ethos object, even all the way down to ethos mirroring the types
> that are needed to contain the particular nomos types, for now
> anyway. So that's, you know, the serialized RKYV payload of that
> filled data type is the body. The encoded form is the code. So the
> encoded form of ethos is ethos. The textual form is there so that
> our editors, our current editors, and our current LLM harnesses and
> models can actually make sense of it. Does that answer the question?

Record's own note: the file carries an archive banner — "Archived as superseded
by 'code/encoded dropped' (06196cc7) and 'textualize is approved' (ba906ae2),
flow ba906ae2, 2026-08-14."

### A2 — `flows/55d18f4f/vision/archive-signalIsOurMessagingLayer.md`
Heading: `## 2026-08-08T11:45:33.818Z — Signal is our messaging layer`
Date: 2026-08-08 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-08T11:45:33.818Z (Designer session 55d18f4f)`; transcript `/home/li/.claude/projects/-home-li-primary/55d18f4f-ea0b-43d8-88ae-f8f4bd3027d2.jsonl:636`

> thats old as fuck. very vague
>
> Signal is our messaging layer, and the CLI's role is to transform text into Signal. So we used to call it NOTA, now it's DOTOS. I don't even know if I like that new name actually. But yeah, yeah, I don't think it's a good name. I don't think it sticks. It's been bothering me for days. We can talk about a new name for it. Not a big deal. So it's the textual form, the CLI transforms the textual form into actual Signal. And Signal, you know, we need to flesh that out better too. It's kind of been really ad hoc. I feel like all the demons like use a different approach. But yeah, it's a RKYV, portable RKYV. And let's like start defining all of this properly, you know, in like a place where let's start making a clean reference point for everything. And I think that's the standards repo, but I don't even know if I like the name of that repo either. Not a big deal.

### A3 — `flows/55d18f4f/vision/archive-rustComponentArchitecture.md`
Heading: `## 2026-08-08T11:28:10.420Z — all the components had the same overall architecture`
Date: 2026-08-08 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-08T11:28:10.420Z (Designer session 55d18f4f)`; transcript `…/55d18f4f-….jsonl:460`

The body runs past 40 lines as one paragraph; the signal-bearing whole is given,
with the lead-in trimmed at the psyche's own turn to the terminology (marked):

> […] And all the components had the same overall architecture. They were a daemon that spoke signal. So you should send an agent to recover that. What's that architecture that we mistakenly thought was still understood by agents, but I never even really considered that my big, huge cleanup actually took that away. And now agents thought they were just writing like, they forgot that all my components have to be like this. So it's like, it's a bunch of signals speaking. And I want to actually be very clear about the terminology here so we don't fucking get lost again. So signal, right? Tell me what signal is. Let's start from the basics. What is SEMA? What is Nexus? I think everybody's completely fucking confused on what I'm actually meaning when I say these things because of how things have been brought up to me. […] And I mean, spirit should show you how this works, right? It's a daemon. It should have two CLIs, which are just proof of concept. All those CLIs are short-term shims that we use to talk to the daemons. But eventually this is all just going to be a giant sort of cluster of components that exchange signal messages with each other. And there will be like a few different entry points. But yeah, the CLI is just like, it's a way to work ourselves up. Like eventually the LLM models will be trained not in text anymore, but in signal, in binary signal, which is way more dense and carries way more information per bits than any of that text crap. So that's what's going to give rise. This is why I'm going to have to head a multi-billion dollar AI company to show the world how you do this properly because everybody's still doing text like monkeys. And it's wrong. And this is how we're going to get there, bits by bits and component by component. So the daemon doesn't really speak string. Although for now they're records that will hold string fields, but it doesn't think in strings at all. And eventually even all of the string part of language will be replaced by a completely specified, fully typed binary system of enums and structs and scalar values.

### A4 — `flows/55d18f4f/vision/everythingIsInTheDaemon.md`
Heading: `## 2026-08-08T11:12:45.472Z — "Everything is in the daemon"`
Date: 2026-08-08 · Level: raw (flow vision, live — not archived)
Provenance: `— psyche, 2026-08-08T11:12:45.472Z (Designer session 55d18f4f; full session UUID 55d18f4f-ea0b-43d8-88ae-f8f4bd3027d2)`

Body is 88 lines; the first 40 lines of the quote are given, **cut marked**:

> the parser is in the daemon right?
>
> Everything is in the daemon.
>
> So this is my vision from the very beginning. Well, I mean, this is the
> vision. This is the vision for a long time. You have the Ethos daemon,
> the Nomos daemon. I mean, they're just called Ethos, Nomos, and Logos.
> Those are the name of the repositories. They're all daemons. The same
> architecture as all my other components, right? There's the daemon,
> there's a CLI, there's a CLI for the metasocket. Everything is signal
> messages, meaning RKYV binary messages. That's what signal means. All of
> this you should be able to find out very, very easily. This should be
> absolutely standard. If any of this was lost and somebody has screwed up
> major, big time. So the whole engine working is the Ethos daemon loads
> the Ethos and then holds the whole thing. It has every object in its own
> specifically typed object, right? A specific type for every kind in
> Ethos, including the Nomos object. So those Nomos types are shared
> between the Nomos daemon. I mean, they're a bit different, arguably,
> because of how Nomos thinks about its own types. Well, they're not
> different, actually. It's just that Nomos uses it as an input for its
> transformer. But I guess, yes, they're the same thing as far as the
> input part. So Ethos doesn't need to think about the transformer. It
> just needs the input part that goes into the transformer. So it loads
> those into, like every transformer has its own particularly specified
> input type. So Ethos has those in the daemon. Everything is in the
> daemon. And then when Ethos wants to convert into logos or rest, which
> has to go through logos, then it sends a message. It communicates to the
> Nomos daemon and tells it, I need this converted into logos and then
> into rest or something. Or maybe it just says, I need this converted
> into logos. And then once that's done, then it gets a message back,
> possibly from the logos daemon directly, that says, oh, here I have your
> request. So the request should have a certain ID for a conversion and
> it's done. […]

**[cut at 40 lines — the remainder of this record is the operational-editing
passage, carried under Group G as G1, and the Logos/Nomos capsule passage]**

### A5 — `flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md`
Heading: `## 2026-08-13 — signal must be specified: portable rkyv; CapnProto as universal signal`
Date: 2026-08-13 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-13 (Designer session 6863ef19), dictated, from the Mentci front-end problem (mentci.md)`

> we have to also be specific about what signal is, because I don't
> want to have to specify, like, R-K-Y-V binary, you know, and we
> have certain standards on how we use this, like, it's portable, I
> think, is the right term, where the settings are set on R-K-Y-V
> to make the format consistent, because of BigEndian and
> SmallEndian and other things. And you can explain me the dialect
> there, too.

> So, the closest thing to R-K-Y-V for cross-platform is CapnProto,
> C-A-P-N-P-R-O-T-O. It's a zero-copy binary format. So,
> transcodable could mean also transcodable in CapnProto, which we
> would call, like, universal signal. So, maybe it's not the right
> term, and we don't have to be afraid to use more elaborate terms
> if we want to describe what this behavior is specifically.

Record's own agent note: "Designer-flagged naming tension: the router-enum
'universal signal repo' (threeStacks.md 2026-08-11, name unruled, bead
primary-xqb.8.3) and this CapnProto form now share the phrase."

Second heading in the same file, same date:
`## 2026-08-13 — universal signal is a capnp transcodable implementation of ethos; not there yet`

> right, which is why it would be a capnp transcodable
> implementation of ethos. we arent there yet

### A6 — `flows/6863ef19/vision/signalIsOurMessagingLayer.md`
Heading: `## 2026-08-13 — the router repo concept is routable signal`
Date: 2026-08-13 · Level: raw (flow vision, live)
Provenance: `— psyche, 2026-08-13T18:09+02:00 (Designer session 6863ef19), typed`

> routable signal then

### A7 — `vision-raw/archive-encodedFormIsTheCode.md`
Heading: `## 2026-08-13 — working form and signal form; code/encoded dropped`
Date: 2026-08-13 · Level: raw (vision-raw, archived)
Provenance: `— psyche, 2026-08-13 (Designer session 06196cc7), typed`

> ok, working form and signal form, drop code/encoded entirely

Record's own note: "Supersedes this file's 2026-08-06 'the encoded form is the
code' framing: code/encoded is no longer form vocabulary."

### A8 — `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md`
Heading: `## 2026-08-14 — signal is fully typed; both sides know the full schema; the "label" frame is confused`
Date: 2026-08-14 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-14T15:01+02:00 (Designer session ba906ae2), typed, on being shown Codex's Stage 2 question ("How does an operation label such as Record, Subscribe, or Recorded survive into Signal without generating single-field wrapper types? Does a Signal envelope own that identity, or do the Protos role traits carry it?")`

> this doesnt make any sense to me. signal is fully typed; both
> sides know the full schema. labels? that flow must be confused.
> and your answer worries me a bit too. lets talk about this in
> detail, because its really importand and you all seem to be
> missing the point.

### A9 — `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md`
Heading: `## 2026-08-14 — signal. signal. signal. — the serialized form's name is signal`
Date: 2026-08-14 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-14T15:12+02:00 (Designer session ba906ae2), typed, after the Designer glossed rkyv's "archive" term for the serialized zero-copy bytes`

> signal. signal. signal. that is what we call it. signal. lets
> find a place to explain that clearly

### A10 — `flows/ac1e9ec8/vision/archive-datomSyntax.md`
Heading: `## 2026-08-26 — curly quotes are the string delimiter; parentheses reserved for Meaning; datom is the edge form of signal` (the third quoted answer in that heading)
Date: 2026-08-26 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-26 (Design session ac1e9ec8), typed.`

On "Everything is datom: every data file and every wire message.":

> no, this is false. all our components speak signal, not datom;
> datom is only used at the edge to let text-based systems (LLMs and
> all existing editors) understand signal.

### A11 — `flows/564f55/vision/archive-signal.md`
Heading: `## 2026-09-09 — can Signal, the rkyv zero-copy memory-readable binary, be wedged in as a layer between the concept and the in-memory value`
Date: 2026-09-09 · Level: raw (flow vision, archived)
Provenance: `-- psyche, STT.`

Thinking out loud, while naming the layers of the datom conversion chain:

> Can we wedge in the concept of Signal here, which is rkyv, the zero-copy, memory-readable binary type that we use for Signal, and somehow this is the Signal layer? Maybe we need the Signal layer between the actual layer. ... Maybe we need another layer, the Signal layer, between the concept and the in-memory rest value.

### A12 — `flows/564f55/vision/archive-protos.md`
Heading: `## 2026-09-09 — composed is chosen: the four layers are textual, protoform, conceptual (datomic), composed; signal is a parallel structure beside them`
Date: 2026-09-09 · Level: raw (flow vision, archived)
Provenance: `-- psyche, STT.` Answering questionnaire items 1 and 2, the pair and the layer noun.

> Yes, we're picking "composed," and therefore the layer, I guess, can be called "composable." The "composed" thing is our term for a Rust value, or what Rust considers an instance of a type.
>
> We're just going to say a composed object, or when something becomes composed, right? When it reaches the in-memory structured layer, it's put together. Componer. That becomes the composition layer, I guess, right?
>
> You have:
> - the textual layer
> - the protoform [STT: protocol] layer
> - the conceptual layer, which in this case is the datomic layer
> - the composed layer, which is the densest form
>
> Signal is nowhere in there. That's a parallel structure. It's for exchanging compositions with a single step, basically, because from composed to signal is just an RKYV serialization with our own protocol in there, which we call a signal.

(The heading and body are duplicated verbatim twice in the file at this revision.)

### A13 — `flows/564f55/vision/archive-signal.md`
Heading: `## 2026-09-09 — the Nexus component never textualizes; only the CLI and the client do; the same signal library derives the datom kinds when compiled for the CLI and nothing of textualization when compiled for the Nexus`
Date: 2026-09-09 · Level: raw (flow vision, archived)
Provenance: `-- psyche, STT.`

> Actually, I just thought of something. The Nexus component is not going to do the textualization at all. That's only in the CLI and the client. I think, depending on what the type is being compiled for, it would derive different things, or that part of the derive would be optional. When the CLI uses the signal library, it would derive Datomizable and composable, but when the Nexus compiles the same signal library, it would compile it without any of the textualization capability.

### A14 — `flows/fe34eb/vision/signal.md`
Heading: `## 2026-09-10 — signal is portable rkyv plus whatever protocol is standardized; the protocol is TBD for now`
Date: 2026-09-10 · Level: raw (flow vision, live)
Provenance: `-- psyche, typed.` Context: the flow asked whether "universal signal is a CapnProto implementation of Ethos" stood beside "portable rkyv".

> signal: portable rkyv + whatever protocol we decide to standardize (talked about before but just mark as TBD for now)

### A15 — `flows/05c604/vision/nexus.md`
Heading: `## The Nexus only gets Signal; the CLI translates datom into Signal; this must be clear in the skill and the vision`
Date: 2026-09-15 (file first committed) · Level: raw (flow vision, live)
Provenance: `-- psyche, typed.` Context: correction of the primary's minimal Persona anatomy proposal, which said "one inline datom per call" at the Nexus socket. Logged directly by the main flow, before acting.

> Sorry, you're saying here I started reading proposal minimal persona, and you say one inline datom per call, but there's something wrong with that because the Nexus only gets signal. The CLI translates datom into signal, so that has to be clear everywhere in the skill, in the vision. It seems it isn't because you haven't gotten that right.

### A16 — already distilled
- `Vision/signal.md` · `## Name`, `## What signal is`, `## Text and signal` · Level: Vision
- `Vision/protos.md` · `## Signal is parallel` · Level: Vision
- `Vision/datom.md` · `## Nature` (the sentence "Datom is signal's form at the edge…") · Level: Vision

`Vision/signal.md`, `## What signal is`:

> Signal is the messaging layer: fully binary, portable rkyv fixed
> across endianness, fully typed with both sides knowing the full
> schema, nothing on the wire labeling itself. It is one step from the
> composition, beside the text chain.

`Vision/protos.md`, `## Signal is parallel`:

> Signal is not a layer of the chain: a parallel structure exchanging
> compositions in one step, an rkyv serialization carrying our own
> protocol.

---

## Group B — queries and responses and refusals

### B1 — `flows/01a03d6e/vision/archive-ethosInterfaces.md`
Heading: `## 2026-08-26T14:22:01.126Z — the interface has to be designed in a verb-oriented, an imperative approach`
Date: 2026-08-26 · Level: raw (flow vision, archived)
Provenance: `— psyche, source-event timestamp 2026-08-26T14:22:01.126Z; typed message record timestamp 2026-08-26T14:22:01.126Z; root session UUID 01a03d6e-5cb8-7b60-b573-7f59413bc18e; transcript provenance /home/li/.codex/sessions/2026/08/26/rollout-2026-08-26T11-37-18-01a03d6e-5cb8-7b60-b573-7f59413bc18e.jsonl, records 2268 (typed user message) and 2269 (user-message event).`

> the interface has to be designed in a verb-oriented, an imperative approach

> When we're designing a signal interface, the input maybe should be even called commands or requests, because they could be refused. So to say request, first of all, is redundant, because this is a request by virtue of being in that slot. And it should be an imperative voice, right, as in list.

### B2 — `flows/01a03d6e/vision/archive-ethosInterfaces.md`
Heading: `## 2026-08-26T15:04:27.982Z — that is obsolete nota/dotos format`
Date: 2026-08-26 · Level: raw (flow vision, archived)
Provenance: same transcript, records 2696 / 2697.

Agent-proposed forms corrected by the psyche:

> (Lock LockSpecification.{name flow-id paths description})
> (Release LockId.42)
> (Observe (Locks Current))

The correction is:

> that is obsolete nota/dotos format

### B3 — `flows/e8c4cc61/vision/archive-ethosFileAnatomy.md`
Heading: `## Handwritten page: Ethos File Anatomy`
Date: 2026-08-29 · Level: raw (flow vision, archived)
Provenance: `-- psyche, handwritten (photo), 2026-08-29.` Photo `ethosFileAnatomy.jpg` in the same directory; comments after `;` are the psyche's.

> Ethos File Anatomy
>
> Signal.{0 2 0}               ; Variant and version
>                              ; This example is Signal
> [ethos:[Registry ...]]       ; Imports
> [Generate.{                  ; Requests
>     Registry Target
>   }
> ]
>
> [Generated.{Vector<RustFile> ...}
>  GenerationFailure.[SyntaxError.Vector<FilePath>
>                     MissingImport.Vector<ImportName>
>                     ...
>                    ]         ; Responses
> ]
> ─────────────────────────────
> Type/Version [Imports] [Requests] [Responses]

Two further headings in the same file, same flow, same era:

`## The signal type is very simple, in terms of ethos types` — `-- psyche, STT.`

> I think we should make the signal type very simple, if only for clarity and to encourage the use of a library file. So we would have the signal type in terms of ethos files or ethos types ...
>
> So for a signal type, it would have an import vector, a request vector, and a response vector, and so on for different types.

`## The page's example is a brainstorm; its anatomy and number of objects stand` — `-- psyche, STT.`

> as you can see in the example, which should not be taken too literally, this is really just a brainstorm. So I'm not set on the particular example. The anatomy is good. The number of objects is good. But I'm not 100% on this Generate [STT: generate ticket] registry or a target or more than that or less than that. And obviously I haven't specified what the registry would look like.

### B4 — `flows/6329f1/vision/archive-ethos.md`
Heading: `## 2026-09-04 — proper ethos is variant-headed, a struct with its version and fields: kinds, types, signal, sema variants with implied kind associations`
Date: 2026-09-04 · Level: raw (flow vision, archived — distilled into `Vision/ethos.md` Declaration)
Provenance: `-- psyche, STT.`

> That way, the ethos parser uses proper ethos, which is variant-headed and is a properly defined struct with its version and all of its different fields. There would be:
>
> * a `kinds` variant, which only holds kinds
> * a `types` variant, which only holds types
> * a `signal` variant, which holds certain specialized types that automatically have kind associations
>
> You would have a query type and a response type, and these would each have their own respective implied associations, implied kind associations. The same would be true of a sema ethos type, which would have a storage type or a record type (whatever you want to call it) that would have associated kinds, implied associated kinds.
>
> It's sort of just a shorthand syntax. Instead of just manually always adding the associations, it's just implied because these types always need to implement those kinds in these ethos variants, essentially different kinds of structs.

### B5 — `flows/564f55/vision/archive-ethos.md`
Heading: `## 2026-09-09 — the version number comes out of Ethos; the sema root type defines database record types; the roots are signal, sema, and nexus; a signal file has query and response; input and output belong to the nexus core`
Date: 2026-09-09 · Level: raw (flow vision, archived)
Provenance: `-- psyche, STT.`

> When we finally define the SEMA object type for Ethos, I want to take the version number out of Ethos. I don't know if I said that. I just want to make sure that that's clear. When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types.
>
> I guess you're asking me about input and output because of the signal interface file, or I guess you're calling it the interface file, but it's a signal file. You have the signal, sema, and nexus type. That's what the type is going to be: signal, and we're going to have query and response.
>
> Input and output are too low-level to really describe what's happening because there's communication there: signal, so it's a query and a response. Maybe input and output are actually good names for nexus, because then we're at a lower level, we're in the runtime, and we're talking about inputs and outputs in terms of computing things inside the logic engine, the engine, the core, right? The nexus of the nexus core, really, not the nexus as a demon component, but the core logic of the nexus, which is the nexus core, the nexus kernel. We can use those terms interchangeably.

Record's own agent-authored landing note, flow fe34eb, 2026-09-10: "the two
entries above are superseded. The living ruled the nexus-core runtime concept
overthinking… Ethos's roots are Library, Signal and Sema."

### B6 — `flows/564f55/vision/archive-ethos.md`
Heading: `## 2026-09-09 — the derived name for the data-carrying variant: yes; Signal's root enums are Query and Response, and Ethos may create default implementations for them, which is why the root is specialized; Nexus's sections are input and output; Sema's to be decided`
Date: 2026-09-09 · Level: raw (flow vision, archived)
Provenance: `-- psyche, STT.`

> Yes, on the derived name for the data-carrying variant, that's a yes. Yes, the signal's root-level enums are `query` and `response`. These are different, so then you have each definition there. It is intrinsically at the variant, and potentially we're going to have Ethos create some default implementations for `query` and `response`, which is why we have this specialized Ethos file type. Well, Nexus's sections are input and output, so it's kind of similar to Signal. Also, Sema, I guess, is going to have some kind of communication, or maybe not. I'm not sure. Database logic: what do we want to have there? Anyway, sort of to be decided later. Let's not get into it right now.

### B7 — `flows/024bc7/vision/signal.md`
Heading: `## 2026-09-13 — It's a request, not a configuration request; the root type of each definition is an enum`
Date: 2026-09-13 · Level: raw (flow vision, live)
Provenance: `-- psyche, STT.`

> They're not like the configuration requests. We don't need to call them configuration requests because when you describe a signal ethos file, you're describing the requests and the responses. When you look at signal, let's say ethos, when we make ethos in nexus or orchestrate: signal: request, it's a request.
>
> The root type of each definition is an enum. The structs represent an enum, and each thing can come in as an object.

Duplicate of the first paragraph only: `flows/bcd02a/vision/signal.md`,
`## 2026-09-13 — Requests and responses`, same date, same level, `-- psyche, STT.`

### B8 — `flows/692df8/vision/signal.md`
Heading: `## Minimal response types by default, with truncated hashes; the full explicit type by an explicit call; a design standard in a skill for specifying Signal`
Date: 2026-09-15 (file first committed) · Level: raw (flow vision, live)
Provenance: `-- psyche, typed.` Context: answer to the Message signal sketch shown whole as a Signal file. Ends with a question, answered in the reply: whether a signal skill exists (it does not). Logged directly by the main flow.

> Your spec is good for the messages, but we need a small response. We need an efficient system, like a summary style or minimal style. You could have this minimal provenance response, which has a truncated hash in place of a hash. These hashes are too expensive.
>
> We need to start putting that in one of our skills for designing systems where there are long hashes or IDs, and we need to have a minimal format for them. If there are fields that aren't necessarily needed, they can just live in the database and be queryable. The flow can query for them, and then we don't need to include all of those fields in these minimal response types. You would have an explicit type of call to get the full explicit response type.
>
> You can have these shorthand types that are usually default, and then you have the more explicit longer name. Let's make this a design standard in the skill for specifying signal. Do we have a skill for signal? Maybe we should.

### B9 — `flows/f426777b/vision/archive-nexusTraits.md`
Heading: `## 2026-08-26 — TryFrom may not be how to think about processing: the effect is the point, the response an effect of it; the returned object may be a generic, which in ethos is a trait`
Date: 2026-08-26 · Level: raw (flow vision, archived)
Provenance: dictated during the nexus/sema document-kind design round, on the Designer's proposed carrying map `PathLockRegistered.TryFrom.Registration`.

> I don't know if try from is the right way to think about something
> that we are processing. I know that, conceptually, it could work
> because we're we're getting a response out of it. But if only before
> cognition to better understand... because what we're doing when
> we're processing something or when we're... when an object is going
> into the nexus for an effect to take place, what... conceptually,
> we're not really trying to get the response. We will get a response
> as an effect of that, but it's kind of like you wouldn't punch
> somebody to try and break your own knuckles. The whole point is to
> hit him and damage him, not to hurt your fist. Although you might
> hurt your fist. So... and also, we would probably need the object
> returned to be... I don't know if we need the object returned to be
> a [generic], in which case? It's a trait because in ethos, generics
> and traits are essentially the same thing. If you understand what
> I'm saying or you're welcome to push back on that also.

Paired heading, same file, same date: `## 2026-08-26 — Apply liked, not certain; the returned-generic trait prompts a need for new terminology`

> I like apply but I'm not certain and the trait suggested for the
> returned generic made me think of something; we need a new
> terminology.

### B10 — already distilled
- `Vision/signal.md` · `## Query and response` · Level: Vision

> A Signal declares queries and responses; input and output are too
> low-level for it.
>
> ```
> Signal
> []                                     ; imports
> [ Lock.LockRequest  Release.LockId ]   ; queries
> [ Locked.Lock  Released.Lock ]         ; responses
> [ LockId.Integer                       ; types
>   LockName.String
>   LockRequest.{ LockName }
>   Lock.{ LockId LockName } ]
> ```

- `Vision/ethos.md` · `## Roots`, `## Shapes and placement` · Level: Vision
- `Vision/nexus.md` · `## Processing is for the effect` · Level: Vision

---

## Group C — the wire: frames, rkyv, handshake, router, versioning

### C1 — `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md`
Heading: `# "encodedform trait must implement the fingerprint trait"` (file-level)
Date: 2026-08-06 (captured 2026-08-08) · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-06T21:58:07Z (Designer session 5abf3be8; entry captured 2026-08-08 from the session transcript during the rulings-audit backfill)`

> so encodedform trait must implement the fingerprint trait. the
> fingerprint trait by default uses the rkyv of that object and gets
> the hash of it. all references use the encodedid of the thing it
> refers to. does that make sense? or is it encodable and
> fingerprintable? are we using nouns or qualifiers for traits? Id
> really like to talk about traits more, how we design them and name
> them, and use them

Record's own 2026-08-14 audit annotation: "this entire 2026-08-06 entry is in
dead vocabulary — encodedform, encodable, and EncodedName all carry
code/encoded, which was dropped 2026-08-13." The **rkyv-hash fingerprint
mechanism itself is not marked dead** — only its vocabulary.

### C2 — `flows/98fbfa47/vision/shortHeaderNotNow.md`
Heading: `# The short header — "a great idea, but it's quite low level" — not now` (file-level)
Date: 2026-08-09 · Level: raw (flow vision, live)
Provenance: `— psyche, 2026-08-09T12:30Z (Designer session 98fbfa47, reviewing the component architecture standard draft)`

> Yeah, the signal header idea, the short header, is a great idea, but
> it's quite low level, and right now we don't need to really... I
> feel like if I let agents implement it, it's going to be kind of
> useless, because they don't really understand what I want to do with
> it and what's possible with it, and it would take me too much effort
> to explain that one small part, and the benefits aren't great
> enough.

Context, kept apart from the quote by the record: "the u64 constant-time
discriminant header proposed as part of the Signal wire baseline (draft section
2). Removed from the standard's present shape; preserved as a marked draft idea
for future improvement (see draftIdeasForImprovement.md)."

### C3 — `flows/012fbf07/vision/archive-threeStacks.md`
Heading: `## 2026-08-11 — the router sorts signals; a universal signal repo wraps them`
Date: 2026-08-11 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed, on the agent-coined numeric "Signal contract ID" scheme`

> the signal ID must be how agents interpreted my vision for an
> ability for the router to differentiate between signal types for
> sorting them out. router is for signals to go across the network.
> it should be an enum in a universal signal repo that all components
> depend on, which wrap the objects. that universal-signal repo could
> also serve other functions that all signals need to deal with
> (handshake payload basically)

**This is the sole raw origin of the handshake payload sentence in
`Vision/nexus.md` `## Routing`.**

### C4 — `flows/012fbf07/vision/archive-threeStacks.md`
Heading: `## 2026-08-11 — the de/serializer: positional, direct to typed structs, no self-describing tags`
Date: 2026-08-11 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-11T13:53+02:00 (Designer session 012fbf07), typed`

> 1 yes, direct to typed structs. 3 what is reflection? no
> self-describing tags

### C5 — `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md`
Heading: `## 2026-08-14 — version should be 0 1 0; version 1 is the first stable release`
Date: 2026-08-14 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-14T15:24+02:00 (Designer session ba906ae2), typed, on the `Interface.{1 0 0}` header in Codex's proposed signal.ethos`

> version should be 0 1 0 - well keep version 1 for the first
> stable release

File banner: "Archived as superseded by 'drop the version number altogether'
(e996e8, 2026-09-04). The words are kept here."

### C6 — `flows/01a02a34/vision/epicBranches.md`
Heading: `## 2026-08-22T21:43:54.512Z — and youll need to branch the two signal repos as well.`
Date: 2026-08-22 · Level: raw (flow vision, live)
Provenance: `— psyche, 2026-08-22T21:43:54.512Z, typed; Codex realization transcript`

> and youll need to branch the two signal repos as well.

### C7 — `flows/fe34eb/vision/signal.md`
Heading: `## 2026-09-10 — the universal signal repository: shouldn't it just be "signal"?`
Date: 2026-09-10 · Level: raw (flow vision, live)
Provenance: `-- psyche, typed.` Context: the flow asked whether the agent-named crate signal-standard is the "universal signal repository every component depends on" of the Nexus vision's Routing statement.

> 3. shouldnt it just be "signal"?

### C8 — `flows/fe34eb/vision/signal.md`
Heading: `## 2026-09-10 — merge the signal repositories into signal, starting with the recently written code, not unused code; archive the old signal repo, rename signal-standard to it; old git history not needed`
Date: 2026-09-10 · Level: raw (flow vision, live)
Provenance: `-- psyche, STT.`

> Yeah, I think you understand the Signal repository, so we could merge all of that there, but let's not just throw a bunch of code that no one's using in there. Start with the code that was written recently ... Let's make sure that whatever depends on Signal standard is then depending on it, or just archive the old Signal repo and then rename the Signal Standard repo to it. We don't need the old Git history unless you think there's something useful there. I don't know. Maybe let's talk about this further, or give me a better view of everything.

### C9 — `flows/024bc7/vision/router.md`
Heading: `## 2026-09-13 — The router becomes the manifest; the enum is the router signal`
Date: 2026-09-13 · Level: raw (flow vision, live)
Provenance: `-- psyche, STT.`

> You have this object, which is orchestrate. That's the router layer. The router has the orchestrate part, so the router becomes the manifest. You can almost call the router the manifest or find a concept there, like the mail or the messenger, kind of. The messenger also can mean taking care of delivery of messages, whereas the router is deciding where this needs to go.
>
> In a sense, when you're compiling code, you can even make these layers merge so that the router becomes how the ethos code is compiled. That's the enum. That's where you get the enum from: the router signal, or from the router. It's the router signal. That's the concept, and then you're putting a layer of namespace in there for your code and for your messages. They all correspond.

The **same words** are logged a second time at **Notion** level in
`flows/bcd02a/notion/router.md`, split across two headings
(`## 2026-09-13 — The router becomes the manifest` and
`## 2026-09-13 — They all correspond`), with the added context: "Exploratory
naming and correspondence. 'The structs represent an enum' is preserved as
spoken; its precise type relationship is unresolved." **The same utterance
therefore sits at two different psyche levels — Vision in 024bc7, Notion in
bcd02a.** Flagged under Contradictions.

### C10 — `flows/e1953c/vision/mesh.md`
Heading: `## The crypto component does the network handshake, combined with the tailnet-based networking protocol; maybe called Mesh`
Date: 2026-09-14 · Level: raw (flow vision, live)
Provenance: `-- psyche, STT.` Named as a suggestion ("maybe it's called Mesh, right? That's a good name").

> This crypto thing needs to be able to also do the handshake on the network. Basically, it can combine itself with the networking protocol that we're going to do, tailnet-based. However, we do it as some kind of component. Maybe it's called Mesh, right? That's a good name, Mesh. Everybody loves the Mesh network.

Paired heading: `## Mesh creates the identity using criome and hooks up the connections and routing rules`

> Yeah, I think you're pretty much on the money with the mesh. It creates the identity using the criome, and it just takes care of hooking up the connections and making sure the routing rules are correct.

### C11 — `flows/6cc91b/vision/criome.md`
Heading: `## 2026-09-14 — It's criome, C R I O M E; CriomOS; a cryptographic biome; criome.net; the Unity client on Slint; a Linux-based sandbox security model` (the wire-bearing final paragraph)
Date: 2026-09-14 · Level: raw (flow vision, live)
Provenance: `-- psyche, typed, artifact comment.`

> We basically create our own sort of Linux-based security model of all these sandboxed, containerized processes. In a sandbox that runs in the app, it has its own file system and network, and all the network that isn't local to the sandbox is going through our own transport signal, like crypto signal. I guess you could call it noise in a way, or signal noise. Give me some ideas here.

### C12 — `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/callerIdentity.md` **[handoff-only]**
Heading: `## A Nexus knows who talks to it: the CLI's process identified through the socket, Flow knowing which process belongs to which flow, the messaging and orchestrate nexuses the same; a standard identity part of the signal, optional in the signal library, so whoever talks to a socket knows to say whether it has the process id`
Date: 2026-09-16 · Level: raw (flow vision, live, but only inside the handoff bundle)
Provenance: `-- psyche, typed.` Context: typed to the primary Claude efa157 on 2026-09-16 at 17:1xZ, the second half of the message whose first half is in transcriptReporting.md. Logged by the main flow before acting.

> I guess we're going to have to have some kind of wrapper that has this information, but it's actually really simple. It just means: have I checked the socket of the process? Can I identify the process that used this CLI, so we can know for sure? The Nexus can know if it's Flow, and Flow would know what process is associated with Flow. It's perfect for that, or the messaging one also, right? The orchestrate all of these things that need to know who's talking to them. They could do that and put that as a standard macro or object. I guess it's a standard signal, you could say. There's a standard part of this, which is a signal. There's this optional part of the signal library to let us add that to it. It would have to be added in the signal library, because then whoever talks to that socket needs to know to tell it if it has the process ID or not, right?

### C13 — `flows/9993b5/vision/callerIdentity.md`
Heading: `## A way to identify the process that called the CLI that created the call; implemented in the CLI part; the chain of events kept: which process launched the CLI call that created the signal that created this request for Flow to refresh itself; discussed as a feature to put in the CLIs and implemented before in older versions of the long quest for the perfect thinking machine system`
Date: 2026-09-17 · Level: raw (flow vision, live)
Provenance: `-- psyche, typed.` Logged by the main flow before acting.

> We need a way to identify the process that called the CLI that created the call, which means it's something that's implemented in the CLI part of things, right? We can make sure that it was that exact executable that ran. We could be thorough with the security, but we keep the chain of events: which process launched the CLI call that created the signal that created this request for Flow to refresh itself.
>
> This is a feature that we've discussed putting in the CLIs, and I think it's been implemented before, in older versions of my long quest for the perfect thinking machine system.

### C14 — `flows/b05237/vision/operational-signalOriginHandshake.md`
Heading: `## We have two standard signal handshakes. One checks the origin process of the call for the message to know where the message came from. Put that in the signal. Show the anatomy in a report`
Date: 2026-09-18 · Level: raw (flow vision, live, operational-prefixed)
Provenance: `-- psyche, direct to primary Psyche opus b05237.` Logged by the main flow before acting.

> We have two standard signal handshakes. One checks the origin process of the call for the message to know where the message came from. We should put that in the signal. You should show me the anatomy of that in the report: how you think that can be done, how it is done, or how it could be done better, and ask me what I think.

**This is the newest and most specific record on the handshake, and the only one
that says there are two standard signal handshakes. Nothing in the corpus names
the second one.**

### C15 — `flows/b05237/vision/operational-theField.md`
Heading: `## We're going to go with the field. Three types: the psyche, the mind, the field. A field nexus will be our system monitor. If the agent needs to know something about the system, he can just call the field CLI`
Date: 2026-09-18 · Level: raw (flow vision, live, operational-prefixed)
Provenance: `-- psyche, direct to primary Psyche opus b05237.`

> Yeah, the field is good. We're going to go with the field. We're going to have three types: the psyche, the mind, the field. We're going to have, probably, a field nexus that will be our system monitor. If the agent needs to know something about the system, he can just call the field CLI, which will create a signal with a traceback to its caller, right?

### C16 — symbols and identifiers on the wire
- `flows/692df8/vision/identifiers.md` · `## A readable alphabet, perhaps words, since the only cost is the token cost; security levels by how bad a collision is; what a legal symbol is, defined in Signal` · 2026-09-15 · raw · `-- psyche, typed.`

The signal-bearing closing paragraph:

> We should probably clarify what the bare string is. What would be a legal symbol, or I don't know, what do we mean by that? An ethos object identifier, right? What we can use as an identifier for an object. What is legal there as a symbol, basically, or what I call a symbol in ethos, something that symbolizes an object, like a data variant or whatever. That would probably live in ethos core or ethos standard, or I guess Signal could have it because we're going to think in terms of Signal. Essentially, sema is storing Signal, so it's all Signal. The data itself, we're going to refer to it as Signal when it's binary and it's typed. Signal is a good place to put that.

**"sema is storing Signal, so it's all Signal" is the single sentence in the
corpus that joins the two roots. It belongs to both Group C and Group E.**

- `flows/692df8/vision/identifiers.md` · `## Identifiers are real types, not strings: an ethos library of identifier types on datom's own hashing types, a UTF-8 base legal in datom, bit-typed ids` · 2026-09-15 · raw · `-- psyche, typed.`

> Why are we saying that the ID is a string? It seems to me that we could maybe create an ethos library for this, but those are real types, like a SHA-256. Yes, in a way, it's a string when you print it, but it's not a string per se.
>
> Your flow ID is, let's say, what? Maybe we don't need to go hexadecimal. We can expand our bit range, our bit efficiency. Whatever is legal in datom is what we should use for our hashing base: a UTF-8 base for hashes. We should probably type them like, "This ID is a 36-bit identifier," or whatever we want to say that.
>
> We have our own protocol for all these identifiers, which uses datom's own standard hashing types that are in the library that we use to create these complex ID types.

- `flows/fd0f97/vision/identifiers.md` · `## The name-based hash goes in the signal library, with a sensible name and anatomy, shown whole; close to a proof of concept, rewritten later where it does not fit` · 2026-09-15 · raw · `-- psyche, typed.`

> Let's do the name-based hash thing in the signal library. Give it a sensible name, give it a sensible anatomy, and then show me everything. We can always change it and rewrite it later. It's fine.

### C17 — already distilled
- `Vision/nexus.md` · `## Routing`, `## The graph`, `## Signal only` · Level: Vision
- `Vision/signal.md` · `## Protocol` · Level: Vision

`Vision/nexus.md`, `## Routing`:

> Signals cross the network through a router. The router tells signal
> types apart by an enum that wraps the objects, held in the signal
> repository, which every component depends on. That repository also
> holds what every signal needs in common — the handshake payload
> among it.

`Vision/signal.md`, `## Protocol`:

> Signal is portable rkyv plus whatever protocol is standardized on top
> of it. The protocol is to be decided.

**No distilled statement exists for the origin-process handshake (C14), the
short header (C2), the version rule as it applies to a Signal file (C5), or the
caller-identity signal part (C12/C13).**

---

## Group D — meta signal and configuration

### D1 — `flows/55d18f4f/vision/majorRecoveryEffort.md`
Heading: `## 2026-08-08T11:21:29.377Z — do a major recovery effort right now`
Date: 2026-08-08 · Level: raw (flow vision, live)
Provenance: `— psyche, 2026-08-08T11:21:29.377Z (Designer session 55d18f4f)`; transcript `…/55d18f4f-….jsonl:454`

> im too angre to read all this right now. do a major recovery effort right now. I want the repos to be called ethos nomos and logos
>
> they will each have a signal-XXX and meta-signal-XXX repo, which will hold the ethos describing the types of the messaging layer, which we call signal, and always have.
>
> we can still have a core-XXX repo for each, if you think that wise or useful, otherwise all the logic can live in the main repo.
>
> Ask me your most important questions while you have agents get started on that

### D2 — `flows/98fbfa47/vision/archive-metaSignalNotOptional.md`
Heading: `## "the metasignal is not optional"`
Date: 2026-08-09 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-09T12:30Z (Designer session 98fbfa47, reviewing the component architecture standard draft)`

> I'm looking at your draft and I would like to say that the
> metasignal is not optional because otherwise there's no way to
> configure the daemon.

Context kept apart by the record: "supersedes the pre-reset doctrine
(component-triad.md, record 2605) that `meta-signal-<component>` is optional
where no owner relationship exists."

### D3 — `flows/98fbfa47/vision/archive-metaCliIsComponentDashMeta.md`
Heading: `## "the meta-cli is obviously just the name of the component dash meta"`
Date: 2026-08-09 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-09T12:30Z (Designer session 98fbfa47, reviewing the component architecture standard draft)`

> And the meta-cli is obviously just the name of the component dash
> meta.

### D4 — `flows/e06e4c07/vision/archive-nexus.md`
Heading: `## 2026-08-19 — core-<component> was already killed; vertices if the word fits; at least two sockets; a default CLI client per socket; the nexus repo is a possibility; first design universal nexus traits from first principles; traits lines deployed` (the socket excerpts)
Date: 2026-08-19 · Level: raw (flow vision, archived)
Provenance: `Design session e06e4c07, typed (captured 2026-08-19T14:51+02:00). Excerpts from one message; trims between.`

On "A Nexus is a daemon with two sockets":

> we should say *at least* two sockets. some nexus might need more
> than 2 levels of access.

On "its two default CLI clients":

> then this would become a default cli client per socket. the cli is
> for bootstrap and later on can be used for debugging and testing
> even after it isnt used in production anymore

And from the sibling heading `## 2026-08-19 — the Nexus part confirmed; …`,
on "and those of every peer Nexus it talks to":

> some vertices will not have the meta access. its case by case. so
> that statement is incorrect

On "A Nexus speaks only the contracts it is compiled with":

> how about "signal contracts"?

### D5 — `flows/01a02fd5/vision/archive-nexuses.md`
Heading: `## 2026-08-23T20:28:43+02:00 — all nexuses have a meta socket`
Date: 2026-08-23 · Level: raw (flow vision, archived)
Provenance: `— psyche, 2026-08-23T20:28:43+02:00, typed; Codex realization flow 01a02fd5.`

> all nexuses have a meta socket

Sibling record, `flows/01a02fd5/vision/archive-metaOrchestrate.md`, same date:

> if meta-orchestrate was removed, the work was done incorrectly

> restore the meta-orchestrate binary.

### D6 — `flows/01a02fd5/vision/interfaces.md`
Headings: `## 2026-08-24T00:32:11+02:00 — the interfaces should be written in schema`; `## 2026-08-24T00:32:28+02:00 — the interfaces for meta-signal and signal orchestrate repos should be schema or ethos`; `## 2026-08-24T00:36:16+02:00 — we'll just say ethos`; `## 2026-08-24T00:36:44+02:00 — use the line you proposed without schema`
Date: 2026-08-24 · Level: raw (flow vision, live)
Provenance: `— psyche, typed; Codex realization flow 01a02fd5.` (four consecutive timestamps)

> the interfaces should be written in schema (or ethos if ethos-monolith can already emit working rust)

> this means the interfaces for meta-signal and signal orchestrate repos should be schema or ethos

> we'll just say ethos, which will motivate everyone to get ethos working.

> use the line you proposed without schema

The last approves the exact owning line `Write every wire interface in Ethos.`

### D7 — `flows/01a03d6e/vision/archive-nexus.md`
Headings, all `2026-08-26T11:38:49.521Z` and `2026-08-26T11:51:46.649Z`
Date: 2026-08-26 · Level: raw (flow vision, archived)
Provenance: `— psyche, source-event timestamp 2026-08-26T11:38:49.521Z; … root session UUID 01a03d6e-5cb8-7b60-b573-7f59413bc18e; transcript provenance /home/li/.codex/sessions/2026/08/26/rollout-2026-08-26T11-37-18-01a03d6e-….jsonl, records 683/684 and 869/870.`

`## — there should be no bootstrap binary; default configuration is a constant in the executable`

> only problem is the bootstrap binary. There should be no bootstrap binary.
>
> So, in terms of configuring the Nexus, obviously, well it's going to have default configuration.
>
> And we can make that more sophisticated later on but it can just have a constant in the executable with a default configuration.

`## — create an interface on the meta socket to change configuration`

> But yeah, so it has a default configuration by default and create an interface on the meta socket to allow for changing that configuration.

`## — new values must be accepted`

> this is a problem; new values must be accepted otherwise it's not doing what we want.

> there is a valid idea behind this however; on a never configured nexus, the ordinary socket could get a configure interface which works but rejects if already configured.

`## 2026-08-26T10:10:32.842Z — the daemons are called Nexus; Orchestrate Nexus; all Nexuses follow that naming invariant`

> Also, we should make an invariant that the demons are not called demons but Nexus.
>
> So it should be Orchestrate Nexus, and all Nexuses should be like that.
>
> So we should make that clear in the Nexus skill.

(`demons` → `daemons`, the record's own speech-to-text correction.)

### D8 — `flows/acbb6006/vision/archive-nexus.md`
Heading: `## First configuration: a standard nexus metadata tree records whether meta Configure was ever done`
Date: 2026-08-27 · Level: raw (flow vision, archived)
Provenance: `2026-08-27T15:20:37Z, the psyche, typed, on tension 2 (Configure on the ordinary socket of a never-configured Nexus)`

> 2. its a valid concept. standard nexus meta-data tree which has a type to know if the meta configure was ever done, which can only be reversed on the meta socket. if unset, the ordinary socket configure is accessible. this is independant of the builtin default configuration, which are needed since otherwise we wouldnt have a socket path to even fall back on to even allow the configure signal to come in.

Sibling heading, same file: `## The standard metadata tree holds socket paths and all standard nexus configuration data`, `2026-08-27T15:38:13Z, the psyche, typed`:

> and lets add to that metadata anything standard: socket paths (its own and the paths of all its other edge-sockets), and anything else that comes up as standard nexus configuration data.

### D9 — `flows/da1e3f/vision/operational-flowVsMessage.md`
Heading: `## Some features on Flow Nexus require the meta socket, like consuming a usage reset — those go through `flow-meta`, not the ordinary `flow``
Date: 2026-09-17 · Level: raw (flow vision, live, operational-prefixed)
Provenance: `-- psyche, typed.` First named example of a meta-socket feature. Logged by the main flow before acting.

> or to access some other features, some require the meta socket like using a usage reset

Preceding heading, same file, same date:

> no, message, not flow-send. use the message nexus!

> flow is to start or refresh a flow

### D10 — `flows/da1e3f/vision/operational-psycheAndMind.md`
Heading: `## The medium is not an effort level; it's a role. The psyche cluster mirrors the mind cluster; Codex runs the mind cluster from primary for now; the psyche cluster is the only one instructed to touch the meta psyche socket`
Date: 2026-09-17 · Level: raw (flow vision, live, operational-prefixed)
Provenance: `-- psyche, typed. ("mine" reads "mind", left as typed and marked.)`

The meta-socket-bearing part:

> We have this cluster that is basically in charge of psyche and mind. I think they should be the ones with the meta access to psyche. Meta psyche access is to the psyche cluster, and maybe only on medium or higher. I don't know if we even have that concept yet. Anyway, only the psyche cluster can use the meta socket. Conceptually, we don't have to enforce that now, but they're the only ones that are instructed for now to do that.
>
> The mine cluster, which Codex runs, is, for now, in primary. We have a Codex mine cluster. It takes care of the meta mine socket and the building and maintaining mine in the system, which mine operates on and which also psyche operates on, but psyche is about changing the psyche, which is what drives the mind to evolve, right, to change itself. The mind component changes the system and stuff, makes proof of concept, and deploys it.

### D11 — already distilled
- `Vision/signal.md` · `## Meta signal` · Level: Vision

> The meta signal is never optional: the daemon is configured only over
> its meta surface.

- `Vision/nexus.md` · `## Sockets`, `## Default clients`, `## Configuration`, `## First configuration`, `## Repositories` · Level: Vision

`Vision/nexus.md`, `## Configuration`:

> A Nexus starts with no arguments and there is no bootstrap binary.
> Its executable holds a default configuration as a constant. On start
> it looks for its Sema database at the default location: a database
> that exists holds the configuration; a database created new is
> seeded with the defaults. The meta socket carries a Configure
> interface, and changed values are accepted through it.

---

## Group E — what sema is

### E1 — `flows/55d18f4f/vision/archive-rustComponentArchitecture.md`
Heading: `## 2026-08-08T11:28:10.420Z — all the components had the same overall architecture` (the question)
Date: 2026-08-08 · Level: raw (flow vision, archived) — full body under A3

> So signal, right? Tell me what signal is. Let's start from the basics. What is SEMA? What is Nexus? I think everybody's completely fucking confused on what I'm actually meaning when I say these things because of how things have been brought up to me.

**The oldest Sema record in the corpus is the psyche asking what Sema is.**

### E2 — `flows/019feb93/vision/threeStacks.md`
Heading: `## 2026-08-10 — completion output of the incorrect new stack`
Date: 2026-08-10 · Level: raw (flow vision, live)
Provenance: `— psyche, 2026-08-10T18:03+02:00 (Realizer session 019feb93), answering what exact end-to-end result the incorrect new stack must produce before the old Schema + NOTA stack can be retired.`

> just generate the rust code for types and generics/traits to define
> the wire types (signal), major internal engine operation types
> (nexus), and database types (sema). log this

**The compactest statement of the three roots in the corpus.**

### E3 — `vision-raw/archive-rustComponentArchitecture.md`
Heading: `## 2026-08-14 — reconsider everything; keep the Signal Nexus SEMA vocabulary and principles, not their past implementation`
Date: 2026-08-14 · Level: raw (vision-raw, archived)
Provenance: `— psyche, 2026-08-14T20:48+02:00 (Designer session ba906ae2), dictated, after the miner's report on the pre-reset skill corpus (reports/PreResetCorpus-2026-06-07/skills/).`

The body is a 120-line single dictation. The **Sema-bearing passage** is quoted
in full; the surrounding passages are Group G and the impurities list:

> And then the same thing with sema, sema being the database engine, which I
> never really looked at close enough. I think that it's probably
> not designed to my standard at all. So that was the whole point
> was to see what, you know, to, and now we can design this better
> to see, to author the database basically. It's actually, you
> could say sema was way more important than nexus because the
> whole point of creating a real code evolution engine was that
> because through the operational editing, we could have database
> migration operations come out instantly or along with the editing
> operation because it would be this essentially sort of parallel,
> almost, you know, almost the exact same thing. And so, yeah, to
> expose the types that the database stores and for the agent, for
> both the human and the agents to easily reason about this, which
> would allow me to read it more easily and understand it. And also
> it would allow the agent to more easily understand how to
> upgrade, how to do a database migration.

And the closing sentence of the same dictation:

> And we can keep the
> Signal, Nexus, SEMA vocabulary and principles, but we aren't tied
> to how they were used and implemented in the past.

**[the remainder of this 120-line body is not reproduced; it is the ethos/datom
rationale, the actor-library direction, the schema-explanation mechanism, and
the ethos-monolith rename — marked cut]**

### E4 — `flows/f426777b/vision/archive-ethosSourceFiles.md`
Heading: `## 2026-08-25 — sema and nexus in the signal repos: a problem`
Date: 2026-08-25 · Level: raw (flow vision, archived)
Provenance: spoken during the audit of 01a03603, on seeing the authored-interfaces layout — the diagram is quoted from the material the psyche was reading.

> I can see a problem already:
>
>      AUTHORED INTERFACES
>       +--------------------------+       +--------------------------+
>       | signal-orchestrate       |       | meta-signal-orchestrate  |
>       |                          |       |                          |
>       | signal.ethos             |       | signal.ethos             |
>       | nexus.ethos              |       | nexus.ethos              |
>       | sema.ethos               |       | sema.ethos               |
>       +------------+-------------+       +-------------+------------+
>                    |                                   |
>                    +----------------+------------------+
>
> sema and nexus in the signal repos.

Sibling heading, same file, same date:
`## 2026-08-25 — nexus and sema ethos are not designed yet; when designed they live in the nexus' main repo`

> lets make it clear first; the nexus and sema ethos arent designed
> yet, but when they are they will live in the nexus' main repo

### E5 — `flows/564f55/vision/archive-sema.md`
Heading: `## 2026-09-09 — sema is the database engine; its Ethos root type defines database record types`
Date: 2026-09-09 · Level: raw (flow vision, archived)
Provenance: `-- psyche, STT.`

> Yes, SEMA is the database. ... When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types. Yes, SEMA is the database engine.

**This is the entire content of `flows/564f55/vision/archive-sema.md` — the only
file in `flows/*/vision/` whose topic is sema, and it holds one record.**

### E6 — `flows/fe34eb/vision/nexus.md`
Heading: `## 2026-09-10 — the nexus-core runtime concept was overthinking; signal gives the main types, sema the database types`
Date: 2026-09-10 · Level: raw (flow vision, live)
Provenance: `-- psyche, typed.` Context: the flow presented the fork of no Nexus root versus a Nexus root that is a Library plus the core's operations.

> I think I was overthinking the whole "nexus-core" runtime concept. As you said, signal defines the requests and the replies, and that sort of gives us all of the main types that we want to be concerned with, other than the database types, which would be the sema types.

### E7 — `flows/024bc7/vision/nexus.md`
Headings: `## 2026-09-13 — The signal layer, the nexus layer, and the sema layer are described in ethos; the database stores that namespace`; `## 2026-09-13 — Three different layers of the runtime; decide on the language by beauty and correctness`
Date: 2026-09-13 · Level: raw (flow vision, live)
Provenance: `-- psyche, STT.`

> Like I explained, you have the signal layer, the nexus layer, and the sema layer, and these are described in ethos. That's what that database is: it stores that namespace.

> We approach this anatomically by describing what kind of objects we need and a problem with Signal, Nexus, and Sema. There are basically three different layers of the runtime:
> - The Nexus: the process or Nexus core, which is the process part.
> - The Sema: the storage part.
> - Signal: sending and receiving requests and responses or replies or whatever.
>
> We have to decide on the language, which words are best based on beauty and correctness.

The **same two utterances** are logged again: the first at **Notion** level in
`flows/bcd02a/notion/ethos.md` (`## 2026-09-13 — It stores that namespace`),
the second at Vision level in `flows/bcd02a/vision/runtime.md`
(`## 2026-09-13 — Three different layers of the runtime`, without the final
beauty-and-correctness sentence). **Level split flagged under Contradictions.**

### E8 — `flows/6cc91b/vision/nexus.md`
Heading: `## 2026-09-14 — Nexus, core, and metaNexus are the explicit terms; the core library guards that the signal actor never talks to the sema actor`
Date: 2026-09-14 · Level: raw (flow vision, live)
Provenance: `-- psyche, typed, artifact comment.` Context: comment on the gap "almost nothing runs". "Sima" is speech-to-text for Sema; corrected in the quote. "demon" left as written.

> Yeah all these things have to be re-anatomized. Also I was thinking the Nexus core library could be how the signal actor, the Nexus actor, and the Sema actor (the main actors in a metaNexus, as we could call it, or the whole of what people call a demon) could be. If we want to be explicit we can say metaNexus and core Nexus but if we say Nexus we sort of have to let the context imply which one we are talking about. If the context isn't obvious then the speaker is blamed for not being clear enough: which part he means by Nexus.
>
> Nexus, core, and metaNexus are the explicit terms. The Nexus core library has all of the interfaces and kinds defined for how to build metaNexus and it has the machinery to make sure, ideally at compile time, that there is no signal-actor-to-sema-actor communication possible. All interaction between the signal actor has to go through the Nexus and then the Nexus ethos type file.
>
> We have this Nexus type, the sema type, and the signal type and they each have their own intrinsic kinds applied to the types so that they're of that specific actor. Only this kind of actor can react with this type of object. It's like a kind becomes a higher-type kind compiler check: an architecture guard basically.

### E9 — `flows/e1953c/vision/nexus.md`
Heading: `## The metaNexus is the whole daemon; the Nexus, Sema, and Signal meta-actors each hold sub-actors that must run inside them; the trait enforces it at the compiler`
Date: 2026-09-14 · Level: raw (flow vision, live)
Provenance: `-- psyche, STT.` Context: correction of this flow's reading of the previous entry. "SEMA" is speech-to-text for Sema, corrected in the quote; "demon" is left as transcribed. Ends with a question to be answered: whether the compiler can enforce the separation.

> Well, what I meant was that the MetaNexus is the whole demon, right? That is what we replace the concept of demon with. What I meant was that there's a meta actor also: the Nexus meta actor, the Sema, and the Signal. We talked about this, but we never actually reviewed it together: how the trait enforces that it can only be used inside of a particular meta actor, like either the Signal actor, the main Signal actor, or the Nexus actor. The Nexus actor, the Sema actor, and the Signal actor have their sub-actors, or possibly their implementations, that need to run inside these actors.
>
> We can prioritize which part of the three we should eventually be able to do, but also because it forces a certain part of the logic in a certain actor, where it's declared. We have the processes in the Nexus runtime that act as the only way to a Sema transformation. We separate the logics in the code, and we enforce it on the compiler. Is that possible?

### E10 — `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/sema.md` **[handoff-only]**
Heading: `## Git repositories that hold data become nexuses that hold databases with an update and upgrade system like version control; Sema is that self-version-controlling, append-only database, the way the store already works; the Sema module is involved, a version control system too`
Date: 2026-09-16 · Level: raw (flow vision, live, handoff-only)
Provenance: `-- psyche, typed.` Context: typed to the primary Claude efa157 on 2026-09-16, the end of the message whose parts are in cloudHosts.md and lojix.md, same date. Logged by the main flow before acting.

> Instead of Git repos that hold data, they will become nexuses that hold databases and that have an update/upgrade system, kind of like version control. That is the system that we're developing on Sema, this sort of version-controling, self-version-controlling database, like an append-only style thing. That's how the system we use to store works anyway, so we might as well build that into it. The Sema module can get quite involved, actually. It's kind of like a version control system too.

**Nothing in `Vision/sema.md` carries any of this: append-only, self-version-controlling, or Sema as a version control system.**

### E11 — already distilled
- `Vision/sema.md` · `## What sema is` (the whole file) · Level: Vision

> Sema is the database engine of a Nexus, authored in Ethos so the
> stored types are visible; its root, Sema, declares record types. It
> matters more than nexus, because operational editing should yield the
> migration with the edit.
>
> ```
> Sema
> []                                                        ; imports
> [ Lock.{ LockId LockName FlowId LockPaths LockReason } ]  ; record types
>                                                           ; the remaining sections are to be decided
> ```

- `Vision/ethos.md` · `## Roots` · Level: Vision
- `Vision/archive-ethosMonolith.md` · `## Vocabulary carried` · Level: Vision (retired 2026-09-10)

> The Signal, Nexus, SEMA vocabulary and principles are kept; nothing
> is bound to how they were used and implemented in the past. Nexus is
> authored in ethos so its main operations are visible. Sema is the
> database engine, authored in ethos so the stored types are visible;
> it matters more than nexus, because operational editing should yield
> database migration operations along with the editing operation.

`Vision/sources/sema.md` lists five references: `564f55 sema`, `564f55 ethos`,
`f426777b ethosSourceFiles`, `62022e8f designPractice`, `aa4c7747 ethosMonolith`.
**E2, E6, E7, E8, E9 and E10 are not among them.**

---

## Group F — record types and the Sema root

### F1 — `flows/e06e4c07/vision/archive-nexus.md` (and `flows/fd301d9a/vision/archive-nexusTraits.md`)
Heading: `## 2026-08-19 — core-<component> was already killed; …` (the nexus-repo excerpt) / `## 2026-08-19 — universal Nexus traits are the ontology of an actor/dataflow system`
Date: 2026-08-19 · Level: raw (flow vision, archived, logged twice)
Provenance: `Design session e06e4c07, typed and captured 2026-08-19T14:51+02:00.` fd301d9a's copy cites `psyche-raw/Vision/nexus.md` as its source.

> potentially. let's keep that as an possibility under discussion. We
> need to first design universal nexus traits, which would be the
> basic ontology of an actor/dataflow software system. lets look at
> signal and sema with that, without giving much credit to the
> existing code, approaching it as if we were designing it for the
> first time (the current code being compared to it, which will show
> the gaps as we design further)

Paired, `flows/fd301d9a/vision/archive-nexusTraits.md`, `## 2026-08-22 — old code is at most inspiration for the map`, source `psyche-raw/Vision/worldModelBeforeCode.md`, typed 2026-08-22T15:19+02:00:

> old code is at most inspiration for that map. (no "never ...")

### F2 — `flows/6329f1/vision/archive-ethos.md`
Heading: `## 2026-09-04 — proper ethos is variant-headed, …` (the sema portion; full body at B4)
Date: 2026-09-04 · Level: raw (flow vision, archived)

> The same would be true of a sema ethos type, which would have a storage type or a record type (whatever you want to call it) that would have associated kinds, implied associated kinds.

**The record-type name is explicitly left open here: "storage type or a record
type (whatever you want to call it)". `Vision/sema.md` chose "record types"
without a later record settling it.**

### F3 — `flows/564f55/vision/archive-ethos.md`
Heading: `## 2026-09-09 — the version number comes out of Ethos; the sema root type defines database record types; …` (full body at B5)
Date: 2026-09-09 · Level: raw (flow vision, archived)

> When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types.

### F4 — `flows/564f55/vision/archive-sema.md` — full body at E5
Date: 2026-09-09 · Level: raw

> When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types.

### F5 — `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/sema.md` **[handoff-only]**
Heading: `## Document how the databases are updated between versions when a component's Sema database changes; document the Sema database in Ethos; the kinds used on the database process are defined with that kind and can only be implemented in the signal, or a special repository, persona signal or signal persona, the same for Sema; trait isolation by a special repository or at build time by crate path names; the Ethos that generates the Sema lives in a special place; like a trait-based library`
Date: 2026-09-16 · Level: raw (flow vision, live, handoff-only)
Provenance: `-- psyche, typed.` Context: typed to the primary Claude efa157 on 2026-09-16 mid-turn, with the fill-the-gaps instruction (deployment.md) and the report request (log.md). "semaphores" is speech-to-text for Sema, corrected in the quote and marked. The questions (does it make sense, which name, special repo or build time) are answered in the reply. Logged by the main flow before acting.

> You start documenting how you update the databases between versions when you change a component SEMA database. Make sure you start also using Ethos to document the SEMA database and that those traits are used on the database process that takes care of the database. You have to define them with that trait, and that these traits can only be implemented in the signal or whatever. Maybe we need a special repository. For that, do we say persona signal or signal persona? Anyway, whatever it is, the same thing with SEMA, right?
>
> Do we need a special repo for the trait isolation, or do we just do that at build time? We define these crates with these path names, and we say that the trait has to be defined in here, which is the Ethos that generates the Sema [transcribed "semaphores"], which lives in a special place. That's all that you need for these traits. It's kind of like a trait-based library.

**This asks, unanswered, whether Sema's Ethos needs its own repository — which
stands against `Vision/nexus.md` `## Repositories` ("A component has three
repositories") and against E4's 2026-08-25 ruling that sema.ethos lives in the
Nexus's main repository. Flagged under Contradictions.**

### F6 — already distilled
- `Vision/sema.md` · the `Sema` ethos block (record types; remaining sections TBD)
- `Vision/ethos.md` · `## Roots` ("Sema's are record types, the rest to be decided") and `## Associations` ("In the Signal and Sema roots the associations of the query, response and record types are implied and never written")

`Vision/ethos.md`, `## Associations`, verbatim:

> An association declares that a type bears a kind: the type's name, a
> dot, a bracket of its kinds. In the Signal and Sema roots the
> associations of the query, response and record types are implied and
> never written. In a Library they are the fourth section, after the
> kinds.
>
> ```
> Library
> []                                                       ; imports
> [ Sink.{ String Integer } ]                              ; types
> [ Summarizable.[ summarize.[ String ] ]                  ; kinds
>   Fillable.[ create:[ Self ] ] ]
> [ Sink.[ Summarizable Fillable ] ]                       ; associations
> ```

---

## Group G — migration from operational editing

### G1 — `flows/55d18f4f/vision/everythingIsInTheDaemon.md`
Heading: `## 2026-08-08T11:12:45.472Z — "Everything is in the daemon"` (the operational-editing passage; the record's first 40 lines are at A4)
Date: 2026-08-08 · Level: raw (flow vision, live)
Provenance: `— psyche, 2026-08-08T11:12:45.472Z (Designer session 55d18f4f)`

> And then all of the
> daemons hold that language in memory, in their database. Not in memory,
> in their database. So they can fetch it back. It's there. They can edit
> it. We're going to do operational editing, right? So we can't do
> operational editing if there isn't a daemon with the database, with the
> entire, whatever we call it, the capsule or whatever of that program or
> that universe, if you will, that world that has been loaded through
> Ethos and through Nomos […]
>
> So Nomos is going to use Logos strictly through
> operational editing because it's literally giving it stuff, right?
> Here's a new object, here's a new object, here's a new object, here's a
> new object. It's transforming everything in, you know, in a world, in a
> capsule.

**This is the oldest operational-editing record and the only one that states
its precondition: operational editing is impossible without a daemon holding
the whole thing in its database. It is the argument for Sema.**

### G2 — `vision-raw/archive-rustComponentArchitecture.md`
Heading: `## 2026-08-14 — reconsider everything; …` (the migration sentence; full context at E3)
Date: 2026-08-14 · Level: raw (vision-raw, archived)

> because the
> whole point of creating a real code evolution engine was that
> because through the operational editing, we could have database
> migration operations come out instantly or along with the editing
> operation because it would be this essentially sort of parallel,
> almost, you know, almost the exact same thing.

**This is the sole raw origin of `Vision/sema.md`'s "operational editing should
yield the migration with the edit".**

### G3 — `flows/bcd02a/notion/ethos.md`
Heading: `## 2026-09-13 — Ethos Delta`
Date: 2026-09-13 · Level: **Notion** (the bottom level; binds nothing)
Provenance: `-- psyche, STT.` The record's own context: "The living relayed a message sent to the parallel Claude session, and framed the discussion as exploratory design."

> Oh my god, right, because it holds the last version of the code that's running now, which means now, when you update, we're going to be able to submit the new Ethos Delta, which we're going to create, some kind of Ethos Delta language thing. It's the difference between the spec and the spec, so it's like a structured data diff, basically fully typed. It's crazy. I don't even know if we have the concept already. I just can't even see it. It's going to maybe come in 5 minutes when I send you this. Yeah, we're in design-crazy realization mode.

### G4 — `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/specificationVersionControl.md` **[handoff-only]**
Heading: `## A specification version control system: in the schema, which objects changed and how, a structured diff, data moved when it changes size, an upgrade operation; every schema change a typed operation, which is why the language becomes a nexus; editing is operational editing in the Ethos that generates the Rust, sending a recompilation to test the component now`
Date: 2026-09-16 · Level: raw (flow vision, live, handoff-only)
Provenance: `-- psyche, typed.` Context: typed to the primary Claude efa157 on 2026-09-16, continuing the Sema statement in sema.md; the testing half of the message is in testing.md, same date. "the rest" is speech-to-text for the Rust, corrected in the quote. Logged by the main flow before acting.

> And then you have a specification version control system, too, where, in the schema, the objects changed and how. A structured diff for changing certain types of data that might have to be moved because they change size. It's like an upgrade operation. Whenever we change the schema spec, it's a typed operation. That's why it becomes a nexus. The data, the language becomes a nexus, and the editing becomes an operational editing in the ethos that generates the Rust that sends a recompilation in the system to test this component now, and no-nonsense testing either.

**G3 (Notion, 2026-09-13) and G4 (Vision, 2026-09-16) describe the same thing —
a typed structured diff between two versions of a specification. G4 is later,
typed, and at Vision level, and it adds what G3 lacks: data moved when it
changes size, the upgrade operation, and the recompile-and-test loop.**

### G5 — `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/sema.md` **[handoff-only]** — full body at F5
Date: 2026-09-16 · Level: raw

> You start documenting how you update the databases between versions when you change a component SEMA database.

### G6 — already distilled
- `Vision/sema.md` · "It matters more than nexus, because operational editing should yield the migration with the edit."
- `Vision/archive-ethosMonolith.md` · `## Vocabulary carried` (retired 2026-09-10; full text at E11)

**Nothing distilled carries the structured typed diff (G3/G4), the
append-only/self-version-controlling shape (E10), or the recompile-and-test
loop. `Vision/sema.md` is a single heading of four sentences and one code block
— the smallest Vision topic in the corpus on the subject the psyche called
"way more important than nexus".**

---

## Group H — store location, defaults, first configuration

### H1 — `flows/01a03d6e/vision/archive-nexus.md`
Heading: `## 2026-08-26T11:38:49.521Z — try the default Sema database location and initialize new databases with defaults`
Date: 2026-08-26 · Level: raw (flow vision, archived)
Provenance: `— psyche, source-event timestamp 2026-08-26T11:38:49.521Z; … records 683 (typed user message) and 684 (user-message event).` Speech-to-text correction beside the quote: `SEMA` → `Sema`.

> And because it has a default, well first it should try to get its state from the default location for its Sema database.
>
> And then if that database doesn't exist or if, well, if the database exists then it should have the configuration in it.
>
> Because the default configuration when creating a new database should set the configuration as the defaults in the database.

**This is the only record in the corpus that speaks of a store location. It says
"the default location for its Sema database" and never says where that is. No
record anywhere names a path, a directory, an XDG base, or a `.sema` extension.
The term `.sema` in the brief has no occurrence in the psyche corpus at this
revision.**

### H2 — `flows/acbb6006/vision/archive-nexus.md` — full bodies at D8
Date: 2026-08-27 · Level: raw

The metadata tree and the socket paths it holds. It is the nearest thing to a
statement of *what* is stored at first configuration, and it stores
configuration, not a location.

### H3 — `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/sema.md` **[handoff-only]** — full body at E10
Date: 2026-09-16 · Level: raw

> That's how the system we use to store works anyway, so we might as well build that into it.

("the system we use to store" is the only description of the existing store in
the corpus; the psyche does not name it.)

### H4 — already distilled
- `Vision/nexus.md` · `## Configuration` and `## First configuration` (verbatim at D11 and below)

`Vision/nexus.md`, `## First configuration`:

> A Nexus keeps a standard metadata tree. In it a type records whether
> the meta Configure was ever done; that record is reversed only on the
> meta socket, and while it is unset Configure is accessible on the
> ordinary socket. The tree holds everything standard about the Nexus:
> its socket paths — its own and those of every edge-socket it connects
> to — and whatever else comes up as standard nexus configuration data.
> The built-in default configuration is independent of this and is
> what gives the socket path on which the Configure signal arrives.

---

## Group I — subscription and observation

### I1 — `flows/5abf3be8/vision/streamAsFourthKindMvpFirst.md`
Heading: `## 2026-08-06T18:01:48.557Z — I think we make stream a forest kind`
Date: 2026-08-06 · Level: raw (flow vision, live)
Provenance: `— psyche, 2026-08-06T18:01:48.557Z (Designer session 5abf3be8)`; transcript `…/5abf3be8-….jsonl:530`. The record's own note: "The contemporaneous audit read 'forest' as 'fourth'; that is agent context, not a separate psyche utterance."

> I think we make stream a forest kind and we could even... Yeah. Yeah. Eventually, I mean, not now, we could potentially write a transformer that also creates the required input objects to initiate and end the stream, although it's not necessary for now. And it would also mean that we have transformers that can name things, obviously synthetically create names, so that if the stream is called observer, then it would create an object called observer stream initiation, and then another object called observer stream termination, or something like that. But yeah, for now we could just create, write it all by hand and wire it up in the implementation. I'm more interested in getting the syntax right, getting the concepts right, and getting to minimum viable product.

### I2 — `vision-raw/observerFixtureBlessed.md`
Heading: `# The fixture is blessed` (file-level)
Date: 2026-08-07 · Level: raw (vision-raw, live)
Provenance: `— psyche, 2026-08-07, captured 2026-08-07T22:10Z (Designer session d63804f2)`

> "the fixture is blessed, and / for imports"

The fixture the blessing lands on, quoted by the record as the Designer's
counter-proposal of 2026-08-07 evening:

>     Interface.{1 0 0}
>     [signal/domain.[ObserverFilter ObservationEvent]]
>     {
>       [Tap.ObserverFilter
>        Untap.ObservationTapToken]
>       [ObservationTapped.ObservationTapToken
>        ObservationUntapped.ObservationTapToken]
>       [UnknownObservationTap.ObservationTapToken]
>       [Observation.ObservationEvent]
>     }
>
> with, in signal-domain:
>
>     ObservationEvent.[OperationObserved.OperationKind
>                       EffectObserved.EffectKind
>                       ObservationLagged.DiscardedOperationCount
>                       ObservationEnded.ObservationEndReason]

Record's own note on what the blessing carries: "stream-section entries are
element-type only (the filter rides the Input initiation entry); the version
stays the typed triple `{Major Minor Patch}`; `Tap`/`Untap` naming; the typed
`ObservationTapToken.Integer` newtype; `EffectObserved` implies effects become
recorded; refusals sit in the Refusal section per the universal-sections
ruling."

**This is the only blessed subscription contract in the corpus. Its root is
`Interface`, not `Signal`; it carries a version; it has five sections including
a Refusal section. All three are superseded by later rulings (see
Contradictions).**

### I3 — `flows/01a03d6e/vision/archive-ethosInterfaces.md`
Heading: `## 2026-08-26T14:22:01.126Z — observe is the root variant`
Date: 2026-08-26 · Level: raw (flow vision, archived)
Provenance: `— psyche, source-event timestamp 2026-08-26T14:22:01.126Z; … records 2268 / 2269.`

> observe is more universal, and reuse is good, because there's going to be multiple nexuses, and if they sort of standardize around a set of commands that are more universal, then the models might even be able to instinctively use a tool or a nexus that they weren't even explicitly trained for, just because of the reuse of these primaries, these primordial principles.

> the better design would be observe with a, observe is the root variant, and then it has, it contains another, maybe a list, or sorry, another enum, right, which is represented as a list in that particular spot in the ethos syntax of the subcommand for that observe.

### I4 — `flows/01a03eda/vision/observe.md`
Heading: `# Observe.Locks is best` (file) / `## 2026-08-26T17:54:13Z` and `## 2026-08-26T17:54:57Z`
Date: 2026-08-26 · Level: raw (flow vision, live)
Provenance: `current Codex history, session 01a03eda-0e08-7451-a5bf-ab48a2f67328, physical lines 7385 and 7386, transcript ordinals 7384 and 7385. This source carries no per-message ID.`

First, on the proposed `Observe -> Locks -> Current` nesting:

> 1. yes
> 2. I dont understand why Current needs an entire struct. Locks.Current should be enough. But Observe.CurrentLocks is even better.

Then, 44 seconds later, superseding both:

> Actually, Observe.Locks is best. If another kind of lock comes, then we can add it as such; Observe.ExpiredLocks, etc

**Note the tension with I3 from the same day (14:22Z): I3 rules that Observe is
the root variant *containing another enum*; I4 (17:54Z) flattens it —
`Observe.Locks`, `Observe.ExpiredLocks` — a flat variant per observable. I4 is
later by three and a half hours and is the psyche's own explicit
"Actually, … is best". Flagged.**

### I5 — `flows/acbb6006/vision/archive-nexus.md`
Heading: `## Observation by subscription: make the core idea dead simple`
Date: 2026-08-27 · Level: raw (flow vision, archived)
Provenance: `2026-08-27T15:38:13Z, the psyche, typed, on claim 2 ("Observation flows up, authority flows down: state is observed through push subscriptions — a typed snapshot on open, typed deltas after")`

> 2. I dont like the wording here, even if some of it is true. See if you can make the core idea dead simple, and strip out the complexity and details which we can add back later. so the line is either removed or replaced with a better one

Sibling heading, same file: `## Polling is forbidden; a correct system goes quiet when nothing changes`, `2026-08-27T15:38:13Z, the psyche, typed, on claim 4`:

> 4. this is true and approved as vision

### I6 — `flows/108ab0/vision/operational-pushMessagingForEmergency.md`
Heading: `## We need the push server style for time-type system emergencies — time-based things that have to come in. That is why the reachability requirement bites: without push, a time-based emergency signal cannot reach an agent that is not polling`
Date: 2026-09-17 · Level: raw (flow vision, live, operational-prefixed)
Provenance: `-- psyche, typed.` Logged by the main flow before acting.

> That's why we need the push server style for that time type of system emergency time-based thing that has to come in.
>
> We need the push stuff message.

### I7 — `flows/6cc91b/vision/interflowMessaging.md`
Heading: `## 2026-09-14 — Up-and-down communication on fences: a lower layer's message arrives as a tool-call return or an asynchronous signal, never as the user prompt`
Date: 2026-09-14 · Level: raw (flow vision, live)
Provenance: `-- psyche, STT.` Context: "fences" is the living's reference to Steve Yegge's term. The living asks "What can work best here? Is this just our universal MCP datom ethos spec?"

> Have the up-and-down communication system, even if it's just based on trust on fences, what Steve Yegge calls fences.
>
> Your code is basically your instructions to the agents. It's permissive, but still, because the top layer knows that the third layer doesn't have authority over it, when it gets messaged from that layer, it doesn't treat it as authority. It doesn't come in through the third layer, or I mean, to the middle layer. It doesn't come through the user prompt. It comes in some kind of tool call return that all the agents have running, or some kind of MCP signal that can come in asynchronously. What can work best here? Is this just our universal MCP datom ethos spec? In Interflow messaging format, it's like the different types of messages. If you can have a vector, it's basically just a bunch of messages with different types, and it can probably easily know where that came from. That's not hard to do because we trust the system. We're writing it, we're running it, so we're programming that into our components to do all this.

### I8 — already distilled
- `Vision/nexus.md` · `## Observation by subscription`, `## Polling is forbidden` · Level: Vision

> State is observed by subscription: the subscriber receives the state
> on open, then each change as it happens.

> Polling is forbidden; a correct system goes quiet when nothing
> changes.

**`Vision/signal.md` says nothing about subscription. The `Observe` root
variant (I3, I4), the Tap/Untap contract (I2), and the stream kind (I1) have no
distilled statement anywhere, and `Vision/sources/signal.md` does not reference
any of them.**

---

## Group J — examples already written in datom or ethos, anywhere in the corpus

Listed oldest first. Each is reproduced exactly as the record carries it.

### J1 — 2026-08-07 · `vision-raw/observerFixtureBlessed.md` · raw · **blessed**
The `Interface.{1 0 0}` observer fixture and the `ObservationEvent` enum in
`signal-domain`. Full text at I2. **Root `Interface`; version triple present.**

### J2 — 2026-08-14 · `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md` · raw
Heading `## 2026-08-14 — the placement carries the meaning; inline struct and enum shapes are shorthands deriving named types`. Provenance: `— psyche, 2026-08-14T18:01+02:00 (Designer session ba906ae2), typed.`

The psyche's rulings on the shapes of a Signal variant section, with the shapes
named inline:

On the Designer's logged title "head-and-symbol is a data-carrying variant":

> no. that particular placement is. what is the placement? lets
> look at the ethos schema of an interface file. The type found in
> that field (Vec<Something>) is what implementes ShapeDefined
> (the Something). Lets look at what that code should look like

On the head-`.{…}` inline-struct shape in a variant section:

> if the anonymous struct is a bad idea, which I think it is, it
> could be a shorthand for two types, where the struct would get a
> derived name (RecordData?)

On the Designer's vector reading of head-`.[…]` in a variant section:

> A vector makes no sense; we are defining types not creating
> instances of them. that would be an enum, and as with the
> struct, it could create a derived-name type.

> In simple cases, that syntax will be much easier to read and
> write than referring to another type and using a whole other
> line for that type.

On head-and-symbol meaning a type definition in the types section:

> of course, the input and typedef section are for different
> types. show me you understand this in code (not the current
> code, but using your understanding of what it should be.). you
> can mine past sessions for more context if you need

And the earlier heading the same day, `## 2026-08-14 — head and a symbol means a data-carrying variant; the data is the type the symbol refers to`:

> Right, so that section in the interface file is shape defined.
> And one of the shapes is this head and a symbol. And that means
> a data carrying variant with the data being the type that the
> symbol refers to. And let's make sure together so that we
> understand all of this. What are the other shapes that could
> live in that section and in other similar sections? And how
> could we make, if those different sections have the same shape
> defined options, then how could this code be reused between
> them?

**`Record.Entry` is the worked example throughout; the derived name
`RecordData` is floated with a question mark, never ruled.**

### J3 — 2026-08-20 · `flows/2b34fafa/vision/importResolution.md` · raw
Heading `## 2026-08-20 — external pulls are explicit: colon after the source name; lib.es is the default file`. Provenance: Design session `2b34fafa`, typed.

> "`signal-pysche:Object` pulls Object from lib.es in signal-psyche
> source"

> "`signal-pysche:[Object Thing]` multiple imports"

> "`signal-pysche:stream.[Stream Termination]` from stream.es in
> signal-psyche source"

> "`signal-pysche:external/helper.[Start Modify]` from external/helper.es
> in signal-psyche source"

And from the morning heading, `## 2026-08-20 — the first path segment resolves from a datom manifest, else the document's directory`:

> "signal in signal/domain must be resolved from a manifest (which we
> must spec obviously), which uses datom. if signal has no entry, it
> will look in the directory of the document where the import takes
> place. signal/domain would be signal/domain.ethos. if the manifest
> resolves, signal will point at a source root (need to discuss the
> naming; lets brainstorm on this), and domain will be the file
> (domain.ethos)."

("pysche" is the psyche's typing of psyche, per the record. Note the extension
is `.es` in the examples and `.ethos` in the morning entry — the record marks
the extension as an open side question.)

### J4 — 2026-08-26 · `flows/01a03d6e/vision/archive-ethosInterfaces.md` · raw · **negative example**
Full text at B2. The three agent-written lines and the one-line refusal:

>     (Lock LockSpecification.{name flow-id paths description})
>     (Release LockId.42)
>     (Observe (Locks Current))

> that is obsolete nota/dotos format

### J5 — 2026-08-29 · `flows/e8c4cc61/vision/archive-ethosFileAnatomy.md` · raw · **handwritten by the psyche**
The `Signal.{0 2 0}` page. Full text at B3.

Two more example blocks in the same file, `## The sweet file syntax has a
corresponding type; the full form and mixed ethos`, `-- psyche, typed.`:

> if we want the "sweet" ethos file syntax, we need a corresponding type, like EthosFile (I dont like that name)
>
> then we would convert the text where
>
> ```
> Library.{0 1 0}
> []                            ; imports
> [types]
> [kinds]
> [associations]
> ```
>
> becomes
>
> ```
> Library.{
>   {0 1 0}
>   []                            ; imports
>   [types]
>   [kinds]
>   [associations]
> }
> ```
>
> this also gives us a way to write mixed-ethos
>
> ```
> [
>   Library.{
>     {0 1 0}
>     []                            ; imports
>     [types]
>     [kinds]
>     [associations]
>   }
>
>   Signal.{
>     {0 1 0}
>     []                            ; imports
>     [requests]
>     [responses]
>   }
> ]
> ```
>
> or perhaps variations of this. in any case it lets a model be specific when creating a standalone object

And `## The outer braces are omitted in any ethos file`, `-- psyche, typed.`:

> Library file syntax
>
> { [types] [kinds] [associations] }
>
> the outer {} should be omitted and always implied in any ethos file

### J6 — 2026-09-04 · `flows/b675f3d9/vision/archive-kinds.md` · raw
Heading `## Identity head preferred; existing Rust traits perhaps kept as-is; capabilities need real thought`, `2026-08-26, the psyche, typed`:

> I prefer
>
> Processable<[Clonable Sendable]  Serializable>
>
> what did I say about the <> syntax in ethos?

And `## Different structures may be different types; the delimiter after the head discriminates`, `2026-08-27, the psyche, dictated, on `len.Count` beside `register.{[PathLock] Registered Refused}``:

> It's perfectly acceptable to have different structures, uh, that result in slightly different types. We use the same mechanism in the, uh, ethos signal interfaces and others to differentiate between things like an enum and a struck [struct] by, uh, checking the, uh, delimiter after the head. And this mechanism is used even for a other things. So we could have... and I think this is appropriate for this part of the machinery. We could have different types represented structurally in the context of describing a kind's capabilities.

**`register.{[PathLock] Registered Refused}` is the corpus's only worked example
that carries a refusal alongside a response, and it is a *kind capability*
example, not a Signal example.**

### J7 — 2026-09-09 · `flows/564f55/vision/archive-ethos.md` · raw
Heading `## 2026-09-08 — a struct has named fields; Ethos generates the names deterministically in Rust, after the type names, distinguished when types repeat`, `-- psyche, typed.` Answering the generated Rust `pub struct Generation(pub protos::Text, pub protos::Text);` shown for the ethos line `Generation.{ Text Text }`:

> This makes no sense at all. That's not a struct. A struct has field names, and because the two types of the two fields are the same type, it would do some kind of deterministic distinction of name. First text, second text would be the names of the fields. That probably would be the most sensible thing to do, so that makes zero sense.
>
> You're showing me a tuple there. That's not a struct, so that's not how Ethos should behave. Ethos should create a struct with actually named fields, but the field names don't show up in Ethos. They show up in Rust, deterministically. If all the fields have different types, then the field names are after the type names.

And `## 2026-09-09 — field naming as proposed; a constructed type names its field type-first, text_vector, lock_option; the sugar-derived type name carries an underscore so it can never collide and is seen as inferred`, `-- psyche, STT.`:

> The field naming, like you have it, yes. In a vector of text, the field name is vector of text, right? Option lock is an optional, or maybe it's better to say a text vector, because then you can say a lock option, and it should just work.
>
> On your path overlap the derived name struct, I think what we should do here is introduce something that would make conflict almost impossible, which is `path_overlap_data`. The underscore is seen as non-idiomatic in Rust for Rust type names, which is kind of good for us because then it means that it's never going to happen. At a glance, somebody reading the code would know that this is sort of like it's not a user-written explicit type. It is an explicit type, but it's sort of inferred by the sugar syntax.

**`path_overlap_data` supersedes the `RecordData?` float of J2 as the shape of
a sugar-derived payload type name. Note it is spelled snake_case, which the
psyche states is deliberately non-idiomatic so it can never collide.**

### J8 — 2026-09-09 · `flows/564f55/vision/archive-ethos.md` · raw · the contextualization rule for every example
Heading `## 2026-09-09 — a variant already defined as a type carries that type; the inline payload is a separate phenomenon; every ethos example must be contextualized, since ethos is positional`, `-- psyche, STT.`

> Your named type variants, I think, is where you got confused. If a variant is already defined as a type somewhere else, then that other type becomes the data it carries. There's that, and then there's the phenomenon which I think you were trying to allude to, which is poorly explained because every time you present ethos, you have to contextualize it. Ethos is very positional, so you can't just give a single line of ethos and confusing concepts together there, so the reader won't know what he's reading.

And, from 2026-09-09, `flows/62022e8f/vision/archive-designPractice.md`,
`## Every ethos block presented needs its proper context: a root variant naming its species; layers never mixed in one block`, `-- psyche, STT.` (artifact
comment, cut by the tool's size cap at "waste its time trying to par…"):

> This reminds me that we need to have a standard way to make it a requirement that every time ethos code is presented, it needs to have its proper context. So, we can create many different kinds of ethos root objects to facilitate the expression of ethos code. ... So, the first line nominal dot, and then bracket, right? This is the syntax for a kind declaration. But then below that are sort of like examples of how this would be ... We're talking about how this nominal kind, right, would be represented when used in textual form. ... So, we have different layers that are mixed up in the same block of code, which is problematic. So, either we need to make it very clear with comments that these are different sections. Well, no, yeah, or we need to use different blocks. ... at least we need a variant. ... so far we've had ethos file, or yeah, we could say ethos root types, which have mixed ... sections. So each section contains only a certain, you know, species, like a type declaration, or even a more specific type declaration, like a request type declaration and a response type declaration, and then a kind declaration. And then we're going to have like other specific type, like a storage type declaration when we have the SEMA file type, and we'll have some other specialized type when we talk about nexus declaration files. Maybe. This is all just to be decided ... But we could have a single species type ethos root, like kinds. So you could start a block, an ethos block, right? ... I think it would be a good idea for us to know what language, what dialect we're dealing with here every time we see a block. ... the first non-comment line would say kinds, capitalize of course, because it's a variant. And then, like I said, you know, we could put the version number, but that's sort of optional ... and we could even accept files without version numbers. It's just that the version number could make it more explicit and therefore could allow the runtime to, you know, know ahead of time if it's just going to waste its time trying to par

Sibling heading in the same file, `## The protos skill shows datom, not ethos; ethos always has to be situated`, `-- psyche, STT.`:

> The ethos that's in the protos skill is inappropriate for multiple reasons, one of which is that it always has to be situated. Also, datom [STT: datum] would be more appropriate just because it's a more basic form of protos and it's more predictable, or it's not so situational. I don't think it's situational at all. I think you should verify that. I think that datom [STT: datum] and its structure are very consistent.

**These two records are the governing constraint on any Signal or Sema example
a distillation writes: the block must carry its root variant, its species must
not be mixed, and datom is preferred over ethos where a *predictable* example is
wanted.**

### J9 — 2026-08-29 · `flows/e8c4cc61/vision/designExamples.md` · raw
Heading `## When designing Ethos, the examples are Ethos's own objects`, `-- psyche, typed.` Context: the flow's Datomizable page used Lock as its worked example.

> lock is an extremely poor example when we are designing ethos. why not do the structure of an ethos Library and an ethos Signal Request?

**Directly relevant to this distillation: `Vision/signal.md` and
`Vision/sema.md` both use Lock as their worked example, and this record calls
Lock an extremely poor example when designing Ethos. Whether it also applies
when designing *Signal and Sema* (rather than Ethos itself) is not ruled.
Flagged.**

### J10 — already distilled (the standing examples)
- `Vision/signal.md` · the `Signal` block under `## Query and response` (verbatim at B10)
- `Vision/sema.md` · the `Sema` block (verbatim at E11)
- `Vision/ethos.md` · `## Shapes and placement` — the fullest Signal example in Vision, with its Rust:

> ```
> Signal
> []                                                     ; imports
> [ Lock.LockRequest  Release.LockId ]                   ; queries
> [ Locked.Lock  Released.Lock ]                         ; responses
> [ LockId.Integer                                       ; types
>   LockName.String
>   FlowId.String
>   LockRequest.{ LockName FlowId }
>   Lock.{ LockId LockName } ]
> ```
> ```rust
> pub enum Query    { Lock(LockRequest), Release(LockId) }
> pub enum Response { Locked(Lock), Released(Lock) }
> pub type LockId = Integer;
> pub type LockName = String;
> pub type FlowId = String;
> ```

- `Vision/ethos.md` · `## The datom kinds are compiled in only where text is spoken` — the only distilled example of the Nexus/CLI compile split (the raw record is A13):

> ```rust
> // emitted by Ethos Zero into the signal crate
> #[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]
> pub enum Query { Lock(LockRequest), Release(LockId) }
> ```
> ```toml
> # the CLI's manifest
> signal-orchestrate = { version = "…", features = ["datom"] }
> # the Nexus's manifest
> signal-orchestrate = { version = "…" }
> ```

- `Vision/ethos.md` · `## Associations` — the Library block (verbatim at F6)

**No distilled example anywhere shows: a refusal, a subscription, a meta Signal,
a Sema with more than one record type, a Sema migration section, or a handshake
payload.**

---

## Same-subject contradictions and supersessions

Every one gives both dates. Where a record itself declares the supersession,
that is quoted. Where the tension is this flow's own reading, it is marked as
this flow's inference.

### X1 — The Nexus root and the "nexus layer": removed 2026-09-10, reasserted 2026-09-13 and 2026-09-14
- **2026-08-19** `flows/e06e4c07/vision/archive-nexus.md`: "We could rename the current Nexus … as NexusCore; the heart of this nexus". **2026-08-27** `flows/acbb6006/vision/archive-nexus.md`: "1. core".
- **2026-09-09** `flows/564f55/vision/archive-ethos.md` and `archive-nexus.md`: "Nexus's sections are input and output"; "the nexus core, the nexus kernel. We can use those terms interchangeably."
- **2026-09-10** `flows/fe34eb/vision/nexus.md`: "I think I was overthinking the whole 'nexus-core' runtime concept." Four archive files carry the agent-authored landing note: "there is no Nexus root, no input and output sections, and no nexus core or nexus kernel as a named part. Ethos's roots are Library, Signal and Sema."
- **2026-09-13** `flows/024bc7/vision/nexus.md`: "we need to reintroduce the nexus core language"; "you have the signal layer, the nexus layer, and the sema layer, and these are described in ethos."
- **2026-09-14** `flows/6cc91b/vision/nexus.md`: "Nexus, core, and metaNexus are the explicit terms. The Nexus core library has all of the interfaces and kinds defined… All interaction between the signal actor has to go through the Nexus and then the Nexus ethos type file." `flows/e1953c/vision/nexus.md`: "the MetaNexus is the whole demon… the Nexus meta actor, the Sema, and the Signal."

**The later words (2026-09-13, 2026-09-14) reassert exactly what the earlier
correction (2026-09-10) removed, and they name a *Nexus ethos type file* that
`Vision/ethos.md` `## Roots` says does not exist ("Library, Signal, Sema").
This flow does not resolve it: per the `psyche` skill, a newer record on the
same subject carries weight, but the 2026-09-10 words were an explicit
self-correction and the later ones are exploratory design in artifact comments.
This must go to the living before any distilled statement on Sema or Signal
assumes either shape.**

### X2 — Universal signal: CapnProto (2026-08-13) versus rkyv-plus-TBD (2026-09-10)
- **2026-08-13** `flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md`: "transcodable could mean also transcodable in CapnProto, which we would call, like, universal signal"; and "it would be a capnp transcodable implementation of ethos. we arent there yet".
- **2026-09-10** `flows/fe34eb/vision/signal.md`, asked precisely whether the CapnProto line still stood beside portable rkyv: "signal: portable rkyv + whatever protocol we decide to standardize (talked about before but just mark as TBD for now)".
- `Vision/signal.md` `## Protocol` carries only the 2026-09-10 shape.

**Reading (this flow's): the 2026-09-10 answer does not repudiate CapnProto; it
defers the protocol. But `Vision/signal.md` now reads as though the cross-platform
problem (a non-Rust front-end — `vision-raw/mentci.md`, 2026-08-13 — cannot
speak rkyv signal) had gone away. It has not been answered anywhere in the
corpus.**

### X3 — The repository name: "routable signal" (2026-08-13) versus just "signal" (2026-09-10)
- **2026-08-13** `flows/6863ef19/vision/signalIsOurMessagingLayer.md`: "routable signal then" — assigning the router-enum repo concept that name, with universal signal staying with the CapnProto form.
- **2026-09-10** `flows/fe34eb/vision/signal.md`: "3. shouldnt it just be 'signal'?" and, the same day, "just archive the old Signal repo and then rename the Signal Standard repo to it."
- `Vision/nexus.md` `## Routing` says "held in the signal repository", carrying the 2026-09-10 shape and dropping "routable signal".

### X4 — The version number: present 2026-08-07/08-14/08-30, dropped 2026-09-04/09-09
- **2026-08-07** `vision-raw/observerFixtureBlessed.md`: the blessed fixture is `Interface.{1 0 0}`.
- **2026-08-14** `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md`: "version should be 0 1 0 - well keep version 1 for the first stable release." The file's own banner: "Archived as superseded by 'drop the version number altogether' (e996e8, 2026-09-04)."
- **2026-08-29** `flows/e8c4cc61/vision/archive-ethosFileAnatomy.md`: the psyche's handwritten page reads `Signal.{0 2 0}  ; Variant and version`.
- **2026-08-30** `flows/62022e8f/vision/archive-designPractice.md`: "we could put the version number, but that's sort of optional … and we could even accept files without version numbers."
- **2026-09-04** (cited supersession) and **2026-09-09** `flows/564f55/vision/archive-ethos.md`: "I want to take the version number out of Ethos."
- `Vision/ethos.md` `## Roots`: "No version in a file."

**Consequence for a Signal example: every psyche-authored example of a Signal
file in the corpus carries a version; no psyche-authored versionless example
exists. `Vision/signal.md`'s versionless `Signal` block is agent-composed under
the 2026-09-09 ruling.**

### X5 — The root name: `Interface` (2026-08-07 → 2026-08-26) versus `Signal` (2026-09-04 →)
- **2026-08-07** blessed fixture: `Interface.{1 0 0}`.
- **2026-08-25** `flows/f426777b/vision/archive-ethosSourceFiles.md` records nexus.ethos and sema.ethos existing as "exact empty Interface documents" in both wire repos, and the psyche flags it: "sema and nexus in the signal repos."
- **2026-08-14** `flows/ba906ae2/…`: the psyche still says "lets look at the ethos schema of an interface file"; **2026-09-09** `flows/564f55/vision/archive-ethos.md` corrects the word: "I guess you're calling it the interface file, but it's a signal file."
- `Vision/ethos.md` `## Roots`: Library, Signal, Sema.

### X6 — `Observe` nested (14:22Z) versus flat (17:54Z), the same day
Both **2026-08-26**, three and a half hours apart, in two different flow records
(`flows/01a03d6e/vision/archive-ethosInterfaces.md` and
`flows/01a03eda/vision/observe.md`). Full text at I3 and I4. The later is the
psyche's own "Actually, Observe.Locks is best."

**Neither is distilled. `Vision/nexus.md` carries the subscription principle
with no shape at all.**

### X7 — The meta signal: optional before 2026-08-09, never optional after
Pre-reset doctrine `component-triad.md` record 2605 (undated here; pre-reset)
made `meta-signal-<component>` optional where no owner relationship exists.
**2026-08-09** `flows/98fbfa47/vision/archive-metaSignalNotOptional.md` ends it.
The record itself states the supersession. Landed in `Vision/signal.md`
`## Meta signal` and `Vision/nexus.md` `## Sockets`. **Not a live tension — noted
because the superseded doctrine is still cited in the record.**

### X8 — Where sema.ethos lives: the main repository (2026-08-25) versus "maybe a special repository" (2026-09-16)
- **2026-08-25** `flows/f426777b/vision/archive-ethosSourceFiles.md`: "the nexus and sema ethos arent designed yet, but when they are they will live in the nexus' main repo". Landed in `Vision/nexus.md` `## Documents` and `## Repositories` (three repositories: main, plus one signal repository per socket).
- **2026-09-16** `…/efa157/vision/sema.md` **[handoff-only]**: "Maybe we need a special repository. For that, do we say persona signal or signal persona? … Do we need a special repo for the trait isolation, or do we just do that at build time?"

**The 2026-09-16 words are a question, not a ruling, and per the `psyche` skill
a newer uncertainty does not silently withdraw an earlier specific rule. But
the question is live and unanswered, and
`…/efa157/ordersToCodex-2026-09-16.md` (agent-authored, not psyche) has already
answered it in the agents' own voice — "Naming contract-first: `sema-<nexus>`,
as `signal-<nexus>`" — which would give a component four repositories. That
proposal has no psyche approval in the corpus.**

### X9 — Datom as a Nexus: "stays a library for now" versus "Every component built from now on is a Nexus"
- **2026-09-03 landing** `flows/04db2fd2/vision/archive-datomNexus.md`: "this can just stay in a library for now" — with "eventually … a nexus to translate certain datum objects back and forth between different formats."
- `Vision/nexus.md` `## Library and daemon`: "Every component built from now on is a Nexus."
- **2026-09-16** `…/efa157/vision/specificationVersionControl.md`: "That's why it becomes a nexus. The data, the language becomes a nexus".

**Reading (this flow's): not a contradiction — the psyche's own words carry the
exception and its expiry. Recorded so a distillation does not state the Nexus
rule without it.**

### X10 — The same utterance logged at two levels on 2026-09-13
Three utterances of 2026-09-13 are logged twice by two flows, at **different
psyche levels**:
- the router/manifest words: Vision in `flows/024bc7/vision/router.md`, **Notion** in `flows/bcd02a/notion/router.md`;
- "it stores that namespace": Vision in `flows/024bc7/vision/nexus.md`, **Notion** in `flows/bcd02a/notion/ethos.md`;
- "three different layers of the runtime": Vision in both `flows/024bc7/vision/nexus.md` and `flows/bcd02a/vision/runtime.md`.

**Per the `psyche` skill, Notion binds nothing and Vision is the default level.
The level of the router words is therefore unsettled, and a distillation drawing
on them must say which reading it takes.**

### X11 — `Text` versus `String` in Signal type examples
**2026-09-09** `flows/564f55/vision/archive-ethos.md`: "Why are we not just saying `string` everywhere? … make it `string` and not `text`. Drop the `text` for just the textual layer". The same file's earlier 2026-09-08 example is `Generation.{ Text Text }`. `Vision/ethos.md` and `Vision/signal.md` use `String`. **Superseded cleanly; noted because the older example is still the fullest worked struct in the corpus.**

### X12 — Lock as the worked example
**2026-08-29** `flows/e8c4cc61/vision/designExamples.md`: "lock is an extremely poor example when we are designing ethos. why not do the structure of an ethos Library and an ethos Signal Request?" Yet `Vision/signal.md`, `Vision/sema.md` and `Vision/ethos.md` `## Shapes and placement` all use Lock. **The ruling is scoped to "when we are designing ethos"; whether it reaches Signal and Sema examples is unruled. If the living wants the examples changed, this is the record to put to them.**

---

## Working instructions found inside these records (impurities)

Per the `psyche-distillation` skill a vision impurity is destroyed, not
archived, and the proposal that discards it points it out. Nothing is deleted
here — this subflow only lists them, quoted, in the record where they sit, so
the main flow's proposal can name them.

1. `flows/55d18f4f/vision/majorRecoveryEffort.md` — "do a major recovery effort right now"; "Ask me your most important questions while you have agents get started on that"
2. `flows/55d18f4f/vision/archive-rustComponentArchitecture.md` — "So you should send an agent to recover that."; "go dig in the past. Find out when that big, huge cutoff happened when I decided I need to clean all my skills and change everything and find everything before that."
3. `vision-raw/signalIsOurMessagingLayer.md` — "we need to clarify the skill. get the miner to dig in the old skill set (we have a file somewhere with that)"
4. `vision-raw/archive-rustComponentArchitecture.md` — "send some high powered researchers and investigators and thinkers to just sort of contemplate everything and present me with a proposal for the skill"; "just go deep, look at everything, maybe put together a report or two"; "you can even send an agent to do the rename for both on the remote and the local for the shortcut ethos"
5. `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md` — "lets talk about this in detail, because its really importand"; "let me know how that works on the Rust side"; "show me you understand this in code (not the current code, but using your understanding of what it should be.). you can mine past sessions for more context if you need"; "lets find a place to explain that clearly"
6. `flows/e06e4c07/vision/archive-nexus.md` — "this is good. deploy it"
7. `flows/aa4c7747/vision/orchestrate.md` — "our first work will be a simple orchestrate nexus that reserves paths to make dead-simple datom-syntax path reservation possible for edit coordination."
8. `flows/01a02fd5/vision/archive-metaOrchestrate.md` — "restore the meta-orchestrate binary."
9. `flows/62022e8f/vision/archive-designPractice.md` — "I think you should verify that."
10. `flows/564f55/vision/archive-ethos.md` — "You can land it as is."
11. `flows/fe34eb/vision/signal.md` — "Maybe let's talk about this further, or give me a better view of everything."
12. `flows/692df8/vision/signal.md` — "We need to start putting that in one of our skills…"; "Let's make this a design standard in the skill for specifying signal. Do we have a skill for signal? Maybe we should."
13. `flows/fd0f97/vision/identifiers.md` — "Let's do the name-based hash thing in the signal library. Give it a sensible name, give it a sensible anatomy, and then show me everything." (the record's own context already marks "Show me everything" as a working instruction recorded in log.md)
14. `flows/6cc91b/vision/nexus.md` — "You can show me what you think this could look like, potentially."
15. `flows/6cc91b/vision/migration.md` — "Start setting up a migration system"
16. `flows/e1953c/vision/nexus.md` — "Is that possible?"; "please show me the options if you think that we have them" (the latter in `flows/62022e8f/notion/layerMatching.md`)
17. `flows/b05237/vision/operational-signalOriginHandshake.md` — "You should show me the anatomy of that in the report: how you think that can be done, how it is done, or how it could be done better, and ask me what I think."
18. `…/efa157/vision/deployment.md` **[handoff-only]** — "I want you to use your common sense to fill in the small gaps on the things I want to deploy in production."
19. `…/efa157/vision/sema.md` **[handoff-only]** — "You start documenting how you update the databases between versions when you change a component SEMA database. Make sure you start also using Ethos to document the SEMA database…"
20. `flows/6cc91b/vision/criome.md` — "Give me some ideas here."
21. `flows/a5587095/vision/archive-protosIsTheSharedStyle.md` — "Lets flesh it out in detail with examples then we can make it intent."; "We need to work with visuals, examples, and traits with main types. that must become our design pattern."

**Item 21's second clause is not only an impurity: it is the design-practice rule
that governs how a distilled Signal or Sema statement must be written — visuals,
examples, and traits with main types — and it agrees with the
`psyche-distillation` requirement that a statement about code carries the code.
The main flow should consider whether that clause is an impurity to discard or a
statement to distill into a design-practice topic.**

---

## What a distillation on these two roots is missing

Stated as this flow's own reading, marked as such, and offered only so the main
flow knows what it cannot compose from what exists.

- **Signal has no distilled statement on refusal**, though B1 (2026-08-26) rules that a command "could be refused" and the blessed fixture (I2) has a Refusal section. `Vision/signal.md` names only queries and responses.
- **Signal has no distilled statement on subscription**, though the whole of Group I exists.
- **Signal has no distilled statement on the handshake** beyond the half-sentence inside `Vision/nexus.md` `## Routing`. C14 (2026-09-18) is one day old and unanswered.
- **Sema has one distilled heading in the entire Vision corpus.** Group E holds eleven raw records, Group F six, Group G six, Group H four. The psyche said Sema "was way more important than nexus" (E3, 2026-08-14); `Vision/nexus.md` has nineteen headings and `Vision/sema.md` has one.
- **`Vision/sources/sema.md` carries five references; this gathering found at least ten qualifying records.** `Vision/sources/signal.md` carries seven; this gathering found at least thirty.
- **No record anywhere names a store location, a path, or a `.sema` file extension.** H1 is the only record on the subject and it says "the default location" without saying what it is.
- **No record anywhere describes a frame** — the word does not occur in the corpus in the wire sense. The nearest is the short header (C2), deferred 2026-08-09.
- **"Meta socket" is abundantly ruled; "meta signal" as a *signal contract shape* is ruled only by D2's one sentence.** What a meta Signal file looks like — whether Configure is a query in it, what its responses are — has no record.

---

## Sources

Read in full at revision `6e59653a`. Paths are absolute from the repository
root `/home/li/primary`.

Distilled psyche (Vision):
`Vision/signal.md`, `Vision/sema.md`, `Vision/nexus.md`, `Vision/ethos.md`,
`Vision/datom.md`, `Vision/protos.md`, `Vision/archive-ethosMonolith.md`,
`Vision/sources/signal.md`, `Vision/sources/sema.md`, `Vision/sources/ethos.md`,
`Vision/sources/protos.md`.

Intent: `Intent/protosParsing.md`.

Legacy raw (vision-raw):
`vision-raw/signalIsOurMessagingLayer.md`,
`vision-raw/archive-rustComponentArchitecture.md`,
`vision-raw/archive-encodedFormIsTheCode.md`,
`vision-raw/archive-threeStacks.md`, `vision-raw/archive-colonConfusion.md`,
`vision-raw/observerFixtureBlessed.md`, `vision-raw/mentci.md`,
`vision-raw/draftIdeasForImprovement.md`,
`vision-raw/everyConceptShouldHaveItsRepo.md`.

Flow raw vision:
`flows/012fbf07/vision/archive-threeStacks.md`,
`flows/012fbf07/vision/threeStacks.md`,
`flows/019feb93/vision/threeStacks.md`,
`flows/01a02a34/vision/epicBranches.md`,
`flows/01a02b4b/vision/emacsPlugin.md`,
`flows/01a02fd5/vision/archive-metaOrchestrate.md`,
`flows/01a02fd5/vision/archive-nexuses.md`,
`flows/01a02fd5/vision/interfaces.md`,
`flows/01a03d6e/vision/archive-ethosInterfaces.md`,
`flows/01a03d6e/vision/archive-nexus.md`,
`flows/01a03d6e/vision/archive-dotosFiles.md`,
`flows/01a03eda/vision/observe.md`,
`flows/024bc7/vision/signal.md`, `flows/024bc7/vision/router.md`,
`flows/024bc7/vision/nexus.md`, `flows/024bc7/vision/criome.md`,
`flows/04db2fd2/vision/archive-textualTypes.md`,
`flows/04db2fd2/vision/archive-datomNexus.md`,
`flows/05c604/vision/nexus.md`,
`flows/06196cc7/vision/threeStacks.md`,
`flows/06196cc7/vision/archive-traitsAsCapabilities.md`,
`flows/06196cc7/vision/archive-encodedFormIsTheCode.md`,
`flows/108ab0/vision/operational-pushMessagingForEmergency.md`,
`flows/2b34fafa/vision/importResolution.md`,
`flows/55d18f4f/vision/everythingIsInTheDaemon.md`,
`flows/55d18f4f/vision/archive-signalIsOurMessagingLayer.md`,
`flows/55d18f4f/vision/archive-rustComponentArchitecture.md`,
`flows/55d18f4f/vision/itsATranslator.md`,
`flows/55d18f4f/vision/majorRecoveryEffort.md`,
`flows/564f55/vision/archive-signal.md`, `flows/564f55/vision/archive-sema.md`,
`flows/564f55/vision/archive-ethos.md`, `flows/564f55/vision/archive-nexus.md`,
`flows/564f55/vision/archive-protos.md`, `flows/564f55/vision/archive-datom.md`,
`flows/5abf3be8/vision/streamAsFourthKindMvpFirst.md`,
`flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md`,
`flows/62022e8f/vision/archive-designPractice.md`,
`flows/6329f1/vision/archive-ethos.md`,
`flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md`,
`flows/6863ef19/vision/signalIsOurMessagingLayer.md`,
`flows/692df8/vision/signal.md`, `flows/692df8/vision/identifiers.md`,
`flows/6cc91b/vision/nexus.md`, `flows/6cc91b/vision/criome.md`,
`flows/6cc91b/vision/interflowMessaging.md`,
`flows/6cc91b/vision/notifications.md`, `flows/6cc91b/vision/secrets.md`,
`flows/6cc91b/vision/migration.md`,
`flows/98fbfa47/vision/archive-metaSignalNotOptional.md`,
`flows/98fbfa47/vision/archive-metaCliIsComponentDashMeta.md`,
`flows/98fbfa47/vision/shortHeaderNotNow.md`,
`flows/9993b5/vision/callerIdentity.md`,
`flows/9993b5/vision/curriculumNexus.md`,
`flows/9993b5/vision/editNexusName.md`, `flows/9993b5/vision/mindMemory.md`,
`flows/a5587095/vision/archive-protosIsTheSharedStyle.md`,
`flows/a5587095/vision/archive-structuredStringType.md`,
`flows/aa4c7747/vision/archive-ethosMonolith.md`,
`flows/aa4c7747/vision/orchestrate.md`,
`flows/ac1e9ec8/vision/archive-datomIsData.md`,
`flows/ac1e9ec8/vision/archive-datomSyntax.md`,
`flows/acbb6006/vision/archive-nexus.md`,
`flows/b05237/vision/operational-signalOriginHandshake.md`,
`flows/b05237/vision/operational-theField.md`,
`flows/b49251/vision/flowLaunching.md`, `flows/b49251/vision/psycheFlows.md`,
`flows/b675f3d9/vision/archive-kinds.md`,
`flows/b675f3d9/vision/archive-distillation.md`,
`flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md`,
`flows/ba906ae2/vision/archive-encodedFormIsTheCode.md`,
`flows/bcd02a/vision/signal.md`, `flows/bcd02a/vision/runtime.md`,
`flows/cff271af/vision/distillation.md`,
`flows/da1e3f/vision/operational-flowVsMessage.md`,
`flows/da1e3f/vision/operational-psycheAndMind.md`,
`flows/e06e4c07/vision/archive-nexus.md`,
`flows/e06e4c07/vision/rustComponentArchitecture.md`,
`flows/e1953c/vision/nexus.md`, `flows/e1953c/vision/mesh.md`,
`flows/e4be1c4a/vision/codeAnalysisTools.md`,
`flows/e8c4cc61/vision/archive-ethosFileAnatomy.md`,
`flows/e8c4cc61/vision/designExamples.md`,
`flows/f426777b/vision/archive-ethosSourceFiles.md`,
`flows/f426777b/vision/archive-nexusTraits.md`,
`flows/f426777b/vision/skillDesigning.md`,
`flows/fd0f97/vision/identifiers.md`, `flows/fd0f97/vision/flowLifecycle.md`,
`flows/fd301d9a/vision/archive-nexusTraits.md`,
`flows/fe34eb/vision/signal.md`, `flows/fe34eb/vision/nexus.md`.

Flow raw notion:
`flows/62022e8f/notion/layerMatching.md`, `flows/6cc91b/notion/datomMcp.md`,
`flows/bcd02a/notion/ethos.md`, `flows/bcd02a/notion/router.md`.

Handoff bundles (the psyche records of flow `efa157`, which has no
`flows/efa157/` directory at this revision):
`flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/sema.md`,
`…/efa157/vision/callerIdentity.md`,
`…/efa157/vision/specificationVersionControl.md`,
`…/efa157/vision/deployment.md`, `…/efa157/vision/lojix.md`,
`…/efa157/vision/subflowDispatch.md`, `…/efa157/vision/harnessRepositories.md`,
`…/efa157/vision/cloudHosts.md`.
Read and **excluded as agent-authored, not psyche**:
`flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/ordersToCodex-2026-09-16.md`.
Verified byte-identical to the live files and therefore adding nothing:
`flows/f55ec8/handoff/successors-v7/sources/Vision/{signal,sema,nexus}.md`,
`flows/b49251/handoff/psyche-medium-v1/modules/sources/Vision/{signal,sema,nexus}.md`.

File index used instead of re-enumerating the corpus:
`flows/056f6d/reports/vision-corpus-manifest.md` (revision `6e59653a`).

Method: `grep -rlniE` over the six trees named in the brief for the terms
`signal|sema|rkyv|meta.?socket|sema-engine`, then a second pass for
`handshake|subscri|migration|record type|Observe|Configure|wire|frame|\.sema|meta signal|metasignal`
differenced against the first, to catch records that speak of the wire without
using either root's name. 110 files matched the first pass; 34 more the second,
of which 7 carried psyche speech on these subjects. Every matched file was read
in full. The term `.sema` returned no occurrence in any psyche record.
