# Ethos objects — every snippet and ruling

Gathered by flow 4decf7 (child), 2026-09-03. Every snippet is quoted
verbatim with provenance. The living's words are quoted; flow
constructions are marked as such. Organized by object: Library,
Signal, Nexus, Sema, mixed file. Within each, chronological.

---

## Library

### 1. The Library file syntax — flow default, unseen by the living (db97561c, 2026-08-29)

The corrective prompt `flows/db97561c/reports/mapSyntaxCorrection.md`
specifies the Library file exactly. Its shape is a flow construction:
Header `Library.{major minor patch}`, imports `[]`, body
`{ [types] [kinds] [associations] }`. This prompt was authored by
flow db97561c and handed to the implementing flow; the living did not
write or review this particular file-level anatomy. It was the
default the flow prepared from accumulated rulings (sections confer
traits from 5abf3be8, three-section body from general ethos rulings).

### 2. The outer braces — ruled (e8c4cc61, 2026-08-29, typed)

The flow presented the db97561c Library file syntax
`{ [types] [kinds] [associations] }` alongside the psyche's
handwritten page.

> the outer {} should be omitted and always implied in any ethos file

-- psyche, typed, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: written by the living, ruled.

### 3. The sweet file form — written by the living (e8c4cc61, 2026-08-29, typed)

The living typed the Library in sweet file form and its corresponding
full (contained) form:

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

-- psyche, typed, session e8c4cc61 (2026-08-29T15:21:12Z).
Transcript: `e8c4cc61-6074-4467-b49c-fd2489b9b3ed.jsonl:422`.
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: written by the living, ruled.

The sweet form (`Library.{0 1 0}` then sections on separate lines) is
the file form — outer braces implied. The full form (`Library.{ {0 1 0} [] [types] [kinds] [associations] }`) is the contained form — a datom
of type Ethos. The corresponding type (needed for the sugar) is wanted
but unnamed ("EthosFile" disliked).

### 4. The Library sections — psyche's design

The sections are: **version** (the first member), **imports** (the
second, `[]` when empty), **types**, **kinds**, **associations**. This
anatomy is written by the living in snippet 3 above and restated in
the handwritten page and the STT:

> So for a signal type, it would have an import vector, a request
> vector, and a response vector, and so on for different types.

-- psyche, STT, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
The "and so on for different types" makes the Library's own sections
(types, kinds, associations) the "different types" counterpart.

### 5. Lock is a poor example; use an ethos Library and an ethos Signal (e8c4cc61, 2026-08-29, typed)

> lock is an extremely poor example when we are designing ethos. why
> not do the structure of an ethos Library and an ethos Signal Request?
>
> I also want to see the definition of the object that would/could
> contain such types. what about the anatomy of a kind, and what it
> would look like in terms of a datom object?
>
> Develop the notion much further, youre way too shallow right now.

-- psyche, typed, session e8c4cc61 (2026-08-29T15:58:57Z).
Transcript: `e8c4cc61-6074-4467-b49c-fd2489b9b3ed.jsonl:631`.
Record: `flows/e8c4cc61/vision/designExamples.md`.
Standing: written by the living. Directs the flow to use Library and
Signal as worked examples instead of Lock; wants the containing type
and the kind anatomy as datom objects.

### 6. The Ethos type — flow construction (62022e8f, 2026-08-30)

The protosLayers report (flow 62022e8f) constructed the Ethos
roster type that declares Library and Signal as its roots:

```
Types
Ethos.[ Library.{ Version Imports Types Kinds Associations } Signal.{ Version Imports Requests Responses } ]
```

This is a flow construction, not a psyche ruling. It extends the
living's snippets 3 and 8 (below) into a type declaration. The
living reviewed the protosLayers page and called it "really good" and
"almost word for word ready to go as vision" (62022e8f/vision/designPractice.md),
but did not specifically rule on this type line.

### 7. Exploded form — name wanted (995a164e, 2026-08-31, typed)

On an artifact comment anchored at the file-form block
(`Library.{ 0 1 0 }`, sections below, outer braces implied):

> We should have a name explicitly for this form where the ethos text
> can appear. I was thinking "exploded form," but it sounds a bit
> violent, although it kind of works. I would like you to offer some
> alternatives as well on how we could name that.

-- psyche, typed (artifact comment), session 995a164e (2026-08-31).
Record: `flows/995a164e/vision/explodedForm.md`.
Standing: written by the living. The name is open.

---

## Signal

### 1. Signal is our messaging layer — definition (55d18f4f, 2026-08-08, typed)

> Signal is our messaging layer, and the CLI's role is to transform
> text into Signal. So we used to call it NOTA, now it's DOTOS. [...]
> it's the textual form, the CLI transforms the textual form into
> actual Signal. And Signal, you know, we need to flesh that out
> better too. It's kind of been really ad hoc. I feel like all the
> demons like use a different approach. But yeah, it's a RKYV,
> portable RKYV.

-- psyche, typed, session 55d18f4f (2026-08-08T11:45Z).
Record: `flows/55d18f4f/vision/signalIsOurMessagingLayer.md`.

### 2. Signal repos hold ethos describing the messaging layer (55d18f4f, 2026-08-08, typed)

> they will each have a signal-XXX and meta-signal-XXX repo, which
> will hold the ethos describing the types of the messaging layer,
> which we call signal, and always have.

-- psyche, typed, session 55d18f4f (2026-08-08T11:21Z).
Record: `flows/55d18f4f/vision/majorRecoveryEffort.md`.

### 3. The observer fixture — blessed (d63804f2, 2026-08-07)

> "the fixture is blessed, and / for imports"

-- psyche, spoken, session d63804f2 (2026-08-07T22:10Z).
Record: `vision-raw/observerFixtureBlessed.md`.

The blessed fixture:

```
Interface.{1 0 0}
[signal/domain.[ObserverFilter ObservationEvent]]
{
  [Tap.ObserverFilter
   Untap.ObservationTapToken]
  [ObservationTapped.ObservationTapToken
   ObservationUntapped.ObservationTapToken]
  [UnknownObservationTap.ObservationTapToken]
  [Observation.ObservationEvent]
}
```

This is the Interface dialect (the old signal object head), with
sections: [inputs] [outputs] [refusals] [streams]. The `Interface.{}`
head predates the Signal head. Standing: blessed (approved).

### 4. Stream is a section inside the object (d63804f2, 2026-08-07)

> "a section inside the object"
>
> "Yes, the initiation and termination live in the input."

-- psyche, spoken, session d63804f2 (2026-08-07T18:59Z).
Record: `vision-raw/streamSection.md`.

### 5. Version should be 0 1 0, not 1 0 0 (ba906ae2, 2026-08-14, typed)

> version should be 0 1 0 - well keep version 1 for the first
> stable release

-- psyche, typed, session ba906ae2 (2026-08-14T15:24Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.
Corrects the blessed fixture's `Interface.{1 0 0}` to `{0 1 0}`.

### 6. Signal is fully typed; the "label" frame is confused (ba906ae2, 2026-08-14, typed)

> this doesnt make any sense to me. signal is fully typed; both
> sides know the full schema. labels? that flow must be confused.

-- psyche, typed, session ba906ae2 (2026-08-14T15:01Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.

### 7. The ethos generates the type in Rust (ba906ae2, 2026-08-14, typed)

> deleted the name from the type system? what the hell is going on
> here? The ethos *generates the type in rust*

-- psyche, typed, session ba906ae2 (2026-08-14T15:09Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.

### 8. "Signal. signal. signal." — the serialized form's name (ba906ae2, 2026-08-14, typed)

> signal. signal. signal. that is what we call it. signal. lets
> find a place to explain that clearly

-- psyche, typed, session ba906ae2 (2026-08-14T15:12Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.

### 9. Each section has its own parsing context; the input section is an enum (ba906ae2, 2026-08-14, dictated)

> So what we're talking about here is the body section [...] each
> section has its own, I need to know what the vocabulary here is.
> [...] each section has its own parsing context. So the first
> section where record.entry is, in that section, we're 100% going
> to deal with shape-defined entries. [...] I think that this section
> is an enum that we're looking at. So those are different kinds of
> queries that this interface can receive. So these are all the
> variants. Record is a variant, subscribe is a variant. And the
> entry type, [...] essentially [...] record essentially is a data
> carrying variant.

-- psyche, dictated, session ba906ae2 (2026-08-14T15:24Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.

### 10. Head-and-symbol = data-carrying variant (ba906ae2, 2026-08-14, typed)

> Right, so that section in the interface file is shape defined.
> And one of the shapes is this head and a symbol. And that means
> a data carrying variant with the data being the type that the
> symbol refers to.

-- psyche, typed, session ba906ae2 (2026-08-14T15:32Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.

### 11. Placement carries the meaning; inline struct/enum deriving named types (ba906ae2, 2026-08-14, typed)

> no. that particular placement is. what is the placement? lets
> look at the ethos schema of an interface file.

On inline struct: shorthand declaring a derived-name type.
On inline enum: not a vector — "sections define types, not
instances."

> In simple cases, that syntax will be much easier to read and
> write than referring to another type and using a whole other
> line for that type.

-- psyche, typed, session ba906ae2 (2026-08-14T18:01Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.

### 12. Input is not the same type as output (ba906ae2, 2026-08-14, dictated)

> Something right off the bat, in your interface file, there's no
> way that input is the same type as the output or that anything
> is the same type as anything else. Because then why do we have
> different fields? Because they're different things.

-- psyche, dictated, session ba906ae2 (2026-08-14T18:40Z).
Record: `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`.

### 13. Input/Output/Refuse floated; maybe Process trait (ba906ae2, 2026-08-14, typed)

> why not Input Output Refuse, like Write and Read?
>
> but actually, it might be better to have a shared Process trait?
>
> because input.input() is a bit weird? input.process() feels more
> appropriate. but process is overloaded. lets look at some word
> choices

-- psyche, typed, session ba906ae2 (2026-08-14T20:17Z).
Record: `vision-raw/signalIsOurMessagingLayer.md`.
Standing: floated, not ruled.

### 14. Interfaces written in ethos — ruled (01a02fd5, 2026-08-24, typed)

> the interfaces should be written in schema (or ethos if
> ethos-monolith can already emit working rust)

Then, superseding the conditional:

> we'll just say ethos, which will motivate everyone to get ethos
> working.
>
> use the line you proposed without schema

-- psyche, typed, session 01a02fd5 (2026-08-24T00:32-00:36Z).
Record: `flows/01a02fd5/vision/interfaces.md`.
Standing: written by the living, ruled.

### 15. The interface is verb-oriented; "commands or requests" (01a03d6e, 2026-08-26, STT)

> the interface has to be designed in a verb-oriented, an imperative
> approach

> When we're designing a signal interface, the input maybe should be
> even called commands or requests, because they could be refused. So
> to say request, first of all, is redundant, because this is a
> request by virtue of being in that slot. And it should be an
> imperative voice, right, as in list.

-- psyche, STT, session 01a03d6e (2026-08-26T14:22Z).
Record: `flows/01a03d6e/vision/ethosInterfaces.md`.
Standing: ruled. The section name "requests" appears here as the
living's word. "Redundant" refers to labeling something "request"
when it is a request by position — the section confers.

### 16. Observe is the root variant (01a03d6e, 2026-08-26, STT)

> observe is more universal, and reuse is good, because there's going
> to be multiple nexuses, and if they sort of standardize around a set
> of commands that are more universal, then the models might even be
> able to instinctively use a tool or a nexus that they weren't even
> explicitly trained for

> the better design would be observe with a, observe is the root
> variant, and then it has, it contains another, maybe a list, or
> sorry, another enum, right, which is represented as a list in that
> particular spot in the ethos syntax of the subcommand for that
> observe.

-- psyche, STT, session 01a03d6e (2026-08-26T14:22Z).
Record: `flows/01a03d6e/vision/ethosInterfaces.md`.

### 17. Obsolete nota/dotos format rejected (01a03d6e, 2026-08-26, typed)

Agent-proposed forms:

```
(Lock LockSpecification.{name flow-id paths description})
(Release LockId.42)
(Observe (Locks Current))
```

> that is obsolete nota/dotos format

-- psyche, typed, session 01a03d6e (2026-08-26T15:04Z).
Record: `flows/01a03d6e/vision/ethosInterfaces.md`.
Standing: corrected — the parenthesized S-expression form is dead.

### 18. The handwritten page: Ethos File Anatomy (e8c4cc61, 2026-08-29, handwritten)

Photo: `flows/e8c4cc61/vision/ethosFileAnatomy.jpg`. The living's own
hand; transcription:

```
Ethos File Anatomy

Signal.{0 2 0}               ; Variant and version
                             ; This example is Signal
[ethos:[Registry ...]]       ; Imports
[Generate.{                  ; Requests
    Registry Target
  }
]

[Generated.{Vector<RustFile> ...}
 GenerationFailure.[SyntaxError.Vector<FilePath>
                    MissingImport.Vector<ImportName>
                    ...
                   ]         ; Responses
]
─────────────────────────────
Type/Version [Imports] [Requests] [Responses]
```

-- psyche, handwritten (photo), 2026-08-29.
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: written by the living. The anatomy summary at the bottom:
**Type/Version [Imports] [Requests] [Responses]**. No Channel line.

### 19. Signal type is very simple (e8c4cc61, 2026-08-29, STT)

> I think we should make the signal type very simple, if only for
> clarity and to encourage the use of a library file. So we would
> have the signal type in terms of ethos files or ethos types ...
>
> So for a signal type, it would have an import vector, a request
> vector, and a response vector, and so on for different types.

-- psyche, STT, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.

### 20. The page's example is a brainstorm; anatomy and number of objects stand (e8c4cc61, 2026-08-29, STT)

> as you can see in the example, which should not be taken too
> literally, this is really just a brainstorm. So I'm not set on the
> particular example. The anatomy is good. The number of objects is
> good. But I'm not 100% on this Generate [STT: generate ticket]
> registry or a target or more than that or less than that. And
> obviously I haven't specified what the registry would look like.

-- psyche, STT, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: the anatomy (Type/Version, Imports, Requests, Responses)
and the number of objects (two sections: requests and responses)
stand. The specific example (Generate, Generated, GenerationFailure)
is a brainstorm — not settled.

### 21. The sweet file form with Signal — written by the living (e8c4cc61, 2026-08-29, typed)

```
Signal.{
  {0 1 0}
  []                            ; imports
  [requests]
  [responses]
}
```

-- psyche, typed, session e8c4cc61 (2026-08-29T15:21Z).
Transcript: `e8c4cc61-6074-4467-b49c-fd2489b9b3ed.jsonl:422`.
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: written by the living. This is the Signal's full
(contained) form. The sweet file form is:

```
Signal.{0 1 0}
[]
[requests]
[responses]
```

with the outer braces implied by the file-omission ruling.

### 22. Channel is agent hallucination (e8c4cc61, 2026-08-29, typed)

The flow asked whether the `Channel.{Orchestrate 1 5}` line is part
of the interface file:

> I have no idea what this is, so its agent hallucination. What is it
> used for?

-- psyche, typed, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: rejected — Channel was introduced by Codex flow 01a03603
as an autonomous decision, never by the living.

### 23. Inline type declaration on variants (e8c4cc61, 2026-08-29, STT)

> But one thing that I did do, and I have been doing, is to specify a
> type inline [...] So I'm specifying a new type inline. Instead of
> just saying syntax error and then importing syntax error from a
> library, I'm saying syntax error is a vector of file path. And that
> is something that I want to allow in ethos [...] It's a syntactic
> sugar that allows him... So that these types will essentially become
> full types of their own

-- psyche, STT, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosTypes.md`.

### 24. A variant named as an already-defined type = data-carrying variant (e8c4cc61, 2026-08-29, STT)

> when a variant is actually an already defined type somewhere else,
> we can just say syntax error, for example, and if it was specified
> somewhere else in the library, the same name, syntax error, then the
> ethos runtime has to make the leap and understand that syntax error
> is actually a data carrying variant.
>
> But there's no need to write syntax error dot syntax error data. We
> don't need that syntax. That's just repetitive

-- psyche, STT, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosTypes.md`.

### 25. The Interface file shape — flow default (db97561c, 2026-08-29)

The corrective prompt `flows/db97561c/reports/codexCorrection.md`
carries the Interface file form as a flow default:

> Interface files keep their ruled shape: `Interface.{v}`,
> `Channel.{Name contract wire}`, imports,
> `{ [inputs] [outputs] [refusals] [streams] [types] }`.

This is a flow-stated "ruled shape." The psyche's own handwritten page
(snippet 18) uses different section names — [Requests] [Responses] —
and has no Channel. The Interface.{} head with [inputs]/[outputs]
sections predates the Signal.{} head.

**Relationship between Interface and Signal**: the Interface dialect
used in the blessed fixture (snippet 3) and the realized signal repos
predates the living's Signal file anatomy (snippet 18-21). Whether
`Interface.{}` is superseded by `Signal.{}` or whether they name
different things is unaddressed by the living. The handwritten page's
anatomy line says "Type/Version" — implying the head is the variant
name (Signal, Library, etc.), not a fixed `Interface` keyword.

---

## Nexus

### 1. "Nexus and sema ethos arent designed yet" (f426777b, 2026-08-25, typed)

> lets make it clear first; the nexus and sema ethos arent designed
> yet, but when they are they will live in the nexus' main repo

-- psyche, typed, session f426777b (2026-08-25).
Record: `flows/f426777b/vision/ethosSourceFiles.md`.
Standing: written by the living. The nexus document kind does not
exist yet. When designed, it lives in the Nexus's main repository.

### 2. Sema and nexus in the signal repos: a problem (f426777b, 2026-08-25, typed)

> I can see a problem already:
>
> ```
>      AUTHORED INTERFACES
>       +--------------------------+       +--------------------------+
>       | signal-orchestrate       |       | meta-signal-orchestrate  |
>       |                          |       |                          |
>       | signal.ethos             |       | signal.ethos             |
>       | nexus.ethos              |       | nexus.ethos              |
>       | sema.ethos               |       | sema.ethos               |
>       +------------+-------------+       +-------------+------------+
> ```
>
> sema and nexus in the signal repos.

-- psyche, typed, session f426777b (2026-08-25).
Record: `flows/f426777b/vision/ethosSourceFiles.md`.
Standing: the living identifies the problem — sema.ethos and
nexus.ethos are in the wrong repos. The placeholder files are empty
Interface-skeleton documents, not designs.

### 3. "So sema and nexus is implemented in rust?" (f426777b, 2026-08-25, typed)

> so sema and nexus is implemented in rust?

-- psyche, typed, session f426777b (2026-08-25).
Record: `flows/f426777b/vision/ethosSourceFiles.md`.
Standing: a question, not a ruling. The psyche asking whether nexus
and sema are currently hand-written Rust (as opposed to being authored
in ethos). They are.

### 4. Show understanding of what nexus and sema interfaces should look like (f426777b, 2026-08-25, typed)

> make a prompt for codex to fix this, and show me how you understand
> what nexus and sema interfaces should look like; their role and
> anatomy, with some ethos examples.

-- psyche, typed, session f426777b (2026-08-25).
Transcript: `f426777b-cfc5-41f9-8b2b-a7ca3e36c812.jsonl:467`.
Record: `flows/f426777b/vision/ethosSourceFiles.md`.

### 5. "Too many heads in a row" — nexus document syntax corrected (f426777b, 2026-08-26, typed)

The flow had proposed a dotted carrying chain for the nexus document:
`PathLockRegistered.try_from.registration` (and variants). The living
rejected it:

> And I don't like the syntax, by the way, that you've been developing
> for Nexus, which -- okay, so let's look at, for example,
> "PathLockRegistered.try_from.registration".
>
> It's too difficult to make out what this is, and also it's too many
> heads in a row. It's very unrefined. This is a very unrefined
> syntax.

> I don't think we can just define traits implicitly, meaning if we
> only declare traits in our own version of implementations, of how we
> implement them, then it'll be difficult. It's going to be complex to
> try to extract what that trait actually is and how many interactions
> it has.

-- psyche, typed (own transcription of audio), session f426777b
(2026-08-26).
Record: `flows/f426777b/vision/nexusTraits.md` and
`flows/f426777b/vision/spokenVocabulary.md`.
Standing: written by the living, corrected. The dotted carrying chain
is rejected. Traits require explicit declarations.

### 6. The protos philosophy was not understood in the nexus/sema prototype (f426777b, 2026-08-26, STT)

> One thing really worth noting here is that you did not understand
> the proto's [protos] philosophy or way of doing things in how you
> presented me your first prototype. for Nexus and Sema. So training
> is lacking there.

-- psyche, STT, session f426777b (2026-08-26).
Record: `flows/f426777b/vision/skillDesigning.md` (via
`flows/b675f3d9/reports/rememberF426777b.md`).

### 7. Apply liked, not certain; new terminology needed (f426777b, 2026-08-26, typed)

On the effect-verb for nexus processing:

> I like apply but I'm not certain and the trait suggested for the
> returned generic made me think of something; we need a new
> terminology.

-- psyche, typed, session f426777b (2026-08-26).
Record: `flows/f426777b/vision/nexusTraits.md`.
Standing: leaning, not ruled. "Apply" is not settled.

### 8. TryFrom is not the right way to think about processing (f426777b, 2026-08-26, STT)

> I don't know if try from is the right way to think about something
> that we are processing. [...] what we're doing when we're processing
> something or when we're... when an object is going into the nexus
> for an effect to take place, what... conceptually, we're not really
> trying to get the response. We will get a response as an effect of
> that, but it's kind of like you wouldn't punch somebody to try and
> break your own knuckles. The whole point is to hit him and damage
> him, not to hurt your fist.

-- psyche, STT, session f426777b (2026-08-26).
Record: `flows/f426777b/vision/nexusTraits.md`.
Standing: TryFrom questioned for the nexus processing model. The
effect on state is the point; the response is a side-effect.

### 9. Nexus.{0 1 0} document proposal — flow construction, never judged (f426777b/b675f3d9)

Flow b675f3d9's `reports/rememberF426777b.md` shows the flow's
proposed nexus document:

```
Nexus.{0 1 0}
[signal-orchestrate:[PathLock PathLockName PathLockRegistered PathLockReleased]]
[
  ActiveLocks.Vector<PathLock>
  Registration.{PathLock ActiveLocks}
  Release.{PathLockName ActiveLocks}
]
[
  Performable.[
    Registration.PathLockRegistered
    Release.PathLockReleased
  ]
]
```

This is a flow construction ("ideas for your eye"), framed by the
flow as responding to the "too many heads" correction. The living
never judged this proposal. It was produced by b675f3d9 after the
living had already said nexus and sema ethos "arent designed yet"
(snippet 1).

### 10. Nexus kind declaration — flow construction (62022e8f, 2026-08-30)

The protosLayers report constructs a Nexus kind (not a document type):

```
Kinds
Nexus.{ [] [ Request.Protoformed Response.Protoformed ] [] [ handle.{ [ Request ] [ Response ] } ] }
;   complex form: [ superkinds ] [ associated kinds ] [ associated values ] [ capabilities ]
```

And the corresponding Rust:

```rust
pub trait Nexus { type Request: Protoformed; type Response: Protoformed; fn handle(&self, r: Self::Request) -> Self::Response; }
```

This is a flow construction. It is a **kind** (a trait), not a
**document file type**. The living reviewed the protosLayers page
favorably but did not specifically rule on the Nexus kind declaration.

### 11. "Species roots to come: ... a Nexus definition" (62022e8f, 2026-08-30)

The protosLayers report names the future ethos species:

> Species roots to come: request and response declarations of a
> Signal, storage declarations of a Sema file, a Nexus definition.

This is flow-authored context, not the living's words. It aligns with
the living's designPractice ruling (62022e8f): "we'll have some other
specialized type when we talk about nexus declaration files. Maybe.
This is all just to be decided."

### 12. "A Nexus definition" as a specialized type — tentative (62022e8f, 2026-09-01, STT)

> And then we're going to have like other specific type, like a
> storage type declaration when we have the SEMA file type, and we'll
> have some other specialized type when we talk about nexus
> declaration files. Maybe. This is all just to be decided

-- psyche, STT, session 62022e8f (2026-09-01).
Record: `flows/62022e8f/vision/designPractice.md`.
Standing: tentative ("Maybe. This is all just to be decided").

### 13. Nexus authored in ethos so main operations are visible (ba906ae2, 2026-08-14, dictated)

> the whole point of exposing nexus and sema as another, back then it
> was schema, but now ethos authored interfaces was that so that I
> could see what the main operations were inside nexus, right? What
> the main functionality was

-- psyche, dictated, session ba906ae2 (2026-08-14T20:48Z).
Record: `vision-raw/archive-rustComponentArchitecture.md`.
Standing: distilled into Vision/ethosMonolith.md ("Nexus is authored
in ethos so its main operations are visible").

### 14. Universal nexus traits: design from first principles (e06e4c07, 2026-08-19, typed)

> We need to first design universal nexus traits, which would be the
> basic ontology of an actor/dataflow software system. lets look at
> signal and sema with that, without giving much credit to the
> existing code, approaching it as if we were designing it for the
> first time

-- psyche, typed, session e06e4c07 (2026-08-19T14:51Z).
Record: archived into Vision/nexus.md.

### 15. Ethos trait syntax: use the ethos-zero nexus as first example (aa4c7747, 2026-08-24, STT)

> And so we need to define what the trait syntax for Ethos is and use
> the Ethos zero nexus as a first example.

> When I said traits I just meant trait declaration.

-- psyche, STT then typed, session aa4c7747 (2026-08-24).
Record: `flows/aa4c7747/vision/ethosTraitSyntax.md`.

---

## Sema

### 1. "Nexus and sema ethos arent designed yet" (f426777b, 2026-08-25, typed)

Same ruling as Nexus snippet 1:

> lets make it clear first; the nexus and sema ethos arent designed
> yet, but when they are they will live in the nexus' main repo

-- psyche, typed, session f426777b (2026-08-25).
Record: `flows/f426777b/vision/ethosSourceFiles.md`.

### 2. "SEMA probably is the most unusual" (ba906ae2, 2026-08-14, dictated)

> SEMA probably is the most unusual.

> on the signal nexus SEMA separation, I don't know, I'll do some
> research, see what this feels like in terms of the most beautiful
> software ever made in the actor or data flow space.

-- psyche, dictated, session ba906ae2 (2026-08-14T20:48Z).
Record: `vision-raw/archive-rustComponentArchitecture.md`.

### 3. Sema = database types (019feb93, 2026-08-10, typed)

> just generate the rust code for types and generics/traits to define
> the wire types (signal), major internal engine operation types
> (nexus), and database types (sema). log this

-- psyche, typed, session 019feb93 (2026-08-10).
Record: `flows/019feb93/vision/threeStacks.md` (via sema.md report).
Standing: the clearest three-part naming: signal = wire types, nexus =
internal engine operation types, sema = database types.

### 4. Sema is the database engine, more important than nexus (ba906ae2, 2026-08-14, dictated)

> the same thing with sema, sema being the database engine, which I
> never really looked at close enough. I think that it's probably not
> designed to my standard at all.

> you could say sema was way more important than nexus because the
> whole point of creating a real code evolution engine was that because
> through the operational editing, we could have database migration
> operations come out instantly or along with the editing operation

> to expose the types that the database stores and for the agent, for
> both the human and the agents to easily reason about this

-- psyche, dictated, session ba906ae2 (2026-08-14T20:48Z).
Record: `vision-raw/archive-rustComponentArchitecture.md`.
Standing: distilled into Vision/ethosMonolith.md ("Sema is the
database engine, authored in ethos so the stored types are visible;
it matters more than nexus, because operational editing should yield
database migration operations along with the editing operation").

### 5. Schema explanation mechanism — wanted (ba906ae2, 2026-08-14, dictated)

> if I was to ask about a certain object through the CLI [...] I could
> point at a certain object and it would print out its schema and
> ethos syntax, which is very self-describing and very self-evident

-- psyche, dictated, session ba906ae2 (2026-08-14T20:48Z).
Record: `vision-raw/archive-rustComponentArchitecture.md`.

### 6. "A storage type declaration when we have the SEMA file type" — tentative (62022e8f, 2026-09-01, STT)

> And then we're going to have like other specific type, like a
> storage type declaration when we have the SEMA file type, and we'll
> have some other specialized type when we talk about nexus
> declaration files. Maybe. This is all just to be decided

-- psyche, STT, session 62022e8f (2026-09-01).
Record: `flows/62022e8f/vision/designPractice.md`.
Standing: tentative. The SEMA file type is envisioned as a specific
ethos root variant — a "storage type declaration" species. Not ruled.

### 7. Sema.ethos files in signal repos — problem identified (f426777b, 2026-08-25)

Same as Nexus snippet 2. The placeholder sema.ethos files in the
signal repos are empty Interface-skeleton documents, not designs.
The living identified this as a problem and ruled they would move to
the nexus's main repo when designed.

---

## Mixed file

### 1. Mixed ethos — written by the living (e8c4cc61, 2026-08-29, typed)

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
> or perhaps variations of this. in any case it lets a model be
> specific when creating a standalone object

-- psyche, typed, session e8c4cc61 (2026-08-29T15:21Z).
Transcript: `e8c4cc61-6074-4467-b49c-fd2489b9b3ed.jsonl:422`.
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: written by the living. A vector of Ethos objects (full/contained form) is the mixed-ethos form.

### 2. A file is one sweet Ethos or a full datom (e8c4cc61, 2026-08-29, typed)

> yes, youre right there, and I forgot that I used to envision an
> additional step where everything was first read as a datom.
>
> Im not sure how well that would play with the dynamic
> "structure-based" reading, but maybe there is a way to do it

-- psyche, typed, session e8c4cc61 (2026-08-29).
Record: `flows/e8c4cc61/vision/ethosFileAnatomy.md`.
Standing: approved. A file is either one sweet Ethos (file form) or a
full-form datom (an Ethos or Vector<Ethos>) — never mixed syntaxes.
The datom-first reading is recalled as an older vision; compatibility
with structure-based reading is open.

### 3. Mixed ethos in the Ethos type — flow construction (62022e8f, 2026-08-30)

The protosLayers report constructs:

```
Datom
Library.{ { 0 1 0 } [] [ ... ] [ ... ] [ ... ] }                       ; the same file in full, contained form: a datom of type Ethos
[ Library.{ ... } Signal.{ ... } ]                                    ; mixed ethos: a vector of Ethos
```

This is a flow rendering of the living's snippet 1, not independently
ruled.

---

## Sources

### What was read, in order

1. Parent reports: `flows/4decf7/reports/nexusAndClis.md`, `sema.md`,
   `ethos.md`, `signalDesign.md`
2. Originating vision records:
   - `flows/f426777b/vision/nexusTraits.md`
   - `flows/fd301d9a/vision/nexusTraits.md`
   - `flows/01a03d6e/vision/ethosInterfaces.md`
   - `flows/01a02fd5/vision/interfaces.md`
   - `flows/f426777b/vision/ethosSourceFiles.md`
   - `flows/f426777b/vision/spokenVocabulary.md`
   - `flows/ba906ae2/vision/signalIsOurMessagingLayer.md`
3. Vision-raw:
   - `vision-raw/archive-rustComponentArchitecture.md` (ba906ae2)
   - `vision-raw/observerFixtureBlessed.md`
   - `vision-raw/signalIsOurMessagingLayer.md`
   - `vision-raw/streamSection.md`
4. Session e8c4cc61 vision records:
   - `flows/e8c4cc61/vision/ethosFileAnatomy.md`
   - `flows/e8c4cc61/vision/ethosTypes.md`
   - `flows/e8c4cc61/vision/prospective.md`
   - `flows/e8c4cc61/vision/kinds.md`
   - `flows/e8c4cc61/vision/designPractice.md`
   - `flows/e8c4cc61/log.md`
5. Other flow records:
   - `flows/62022e8f/reports/protosLayers.md`
   - `flows/62022e8f/vision/designPractice.md`
   - `flows/62022e8f/vision/kinds.md`
   - `flows/62022e8f/vision/vocabulary.md`
   - `flows/62022e8f/vision/ethosTypes.md`
   - `flows/995a164e/vision/explodedForm.md`
   - `flows/aa4c7747/vision/ethosTraitSyntax.md`
   - `flows/db97561c/reports/mapSyntaxCorrection.md`
   - `flows/db97561c/reports/codexCorrection.md`
   - `flows/b675f3d9/reports/rememberF426777b.md`
6. Transcripts searched:
   - `e8c4cc61-6074-4467-b49c-fd2489b9b3ed.jsonl` (user-typed messages
     for Library.{, Signal.{, sweet, outer braces, requests/responses,
     Lock poor example)
   - `ba906ae2-6257-4045-a264-2c85de7933bb.jsonl` (signal interface)
   - `f426777b-cfc5-41f9-8b2b-a7ca3e36c812.jsonl` (too many heads,
     PathLockRegistered, Configure)
   - `62022e8f-3210-4a55-bb88-91b60117d97c.jsonl` (Nexus kind)

### What was written

- `flows/4decf7/reports/ethosObjects.md` (this file)
