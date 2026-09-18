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

