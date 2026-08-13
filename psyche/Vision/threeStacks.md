# The three stacks

## 2026-08-10 — "the three stacks"

> So currently we have... I've made a mess because I've tried to rename
> everything. I tried to rename Noda to Dothos and now I don't like the
> name Dothos. I still prefer Noda, although... Yeah, Noda is good. But
> I think because Noda, or whatever we call it, is going to be probably
> one of the most important or famous things that I'm making at first, I
> would like the name to be really good. Noda is going to become, or
> whatever we call it, is going to become the next JSON, but bigger than
> JSON. It's going to be how LLMs talk for a while until they get over
> the limitations of text and get into encoded meaning, binary format
> meaning. But I want to talk about what I'm going to call the three
> stacks. The legacy stack, which is the schema and the Noda from
> before, which the components that are, we're going to call it
> production with quotation marks because nothing is really working
> well, are using. And then we have the false stack, I'm going to call
> it, the false new stack, which was a misunderstanding by agents who
> thought that the components were not demons. And the real new stack,
> or the correct new stack, or we're going to say the incorrect new
> stack and the correct new stack. The old stack, the incorrect new
> stack, and the correct new stack. And as much as I want to go back to
> the correct new stack, I would like to replace the old stack so we
> could finish the incorrect new stack and make it clear, make the
> boundaries clear and make it clear in the incorrect new stack that
> this is temporary, so that we can replace the old syntax and start
> getting back to work because I feel like I've been doing nothing for
> a month and a half, I'm really frustrated and my creativity is
> hindered. So I want to be able to design and construct and use
> components and maintain them. And I don't like the old syntax, it's
> garbage to me now. So I want to talk about creating these parallel,
> these three parallel with distinct repositories. I think the old
> stack should just keep the old names, right? Schema and Noda. The
> new stacks have the new names so that they're distinguished from the
> old, which is Dothos, Ethos, Nomos, Logos, and Frotos. But like I
> said, I don't like Dothos, and I'm not that crazy about Noda, so we
> need another name for that. But maybe that's what the new correct
> stack is going to get, the right name. But it's the same syntax, so
> we could change the name anyway. So the repos would be separate, and
> we could even call the incorrect repos incorrect. We could just
> suffix them all with incorrect. And then the new stack would just be
> plainly named, you know, the Ethos.

— psyche, 2026-08-10T12:12Z (Designer session 13cfc23f), on the
three-stack model: old/legacy stack, incorrect new stack, and correct
new stack; and on naming the Noda successor.

Context, kept apart from the quote: spoken while redirecting the
session to the Protos engine. Listener transcription — probable
artifacts, marked as agent reading, unconfirmed: "Dothos" = Dotos,
"demons" = daemons, "Frotos" = possibly Protos.

## 2026-08-10 — names confirmed; the successor name must stick

> obviously protos

> obviously NOTA

> people wont remember dotos, eidos or rhetos. it just wont stick at
> all

— psyche, 2026-08-10T12:44Z (Designer session c6b71b4c), confirming
the fifth new-stack name is Protos and the old notation's name is
NOTA — resolving the transcription artifacts "Frotos" and "Noda"
above — and ruling on the NOTA-successor name: the criterion is that
people remember it; a name that "wont stick" is disqualified.

Context, kept apart from the quotes: "dotos, eidos or rhetos" answers
the existing name Dotos plus the Designer's two disposable sparks
`Rhetos` and `Eidos` — all three fail the stickiness criterion.

## 2026-08-10 — what the successor name must echo

> its data, strictly typed, super dense (no field names). something
> that echoes this

— psyche, 2026-08-10T12:53Z (Designer session c6b71b4c), directing
the successor-name search: the name should echo what the notation is
— data, strictly typed, super dense, field-name-less.

## 2026-08-10 — the successor name is Datom

> what about datom

> ok we'll use datom, and we'll get you started with a fresh session
> to look at how we spilt those 3 stacks so make yourself a restart
> prompt

— psyche, 2026-08-10T13:53Z (Designer session c6b71b4c). The NOTA
successor — the new-stack data notation, previously carrying the
rejected name Dotos — is named **Datom**, the psyche's own coinage.
Ruled after the psyche's naming criteria: it must stick, and it must
echo data, strictly typed, super dense, no field names. Same ruling
orders a fresh Designer session on how the three stacks get split
into parallel repositories.

## 2026-08-10 — completion output of the incorrect new stack

> just generate the rust code for types and generics/traits to define
> the wire types (signal), major internal engine operation types
> (nexus), and database types (sema). log this

— psyche, 2026-08-10T18:03+02:00 (Realizer session 019feb93), answering
what exact end-to-end result the incorrect new stack must produce before
the old Schema + NOTA stack can be retired.

## 2026-08-10 — the shortcut: freeze the incorrect stack, new repos emit Rust

> So, yeah, I still really much want the new ethos and datum [Datom]
> languages, even if we use the hacky incorrect new stack … we could
> take a lot of complexity out of the incorrect stack because we just
> want to emit rust. So we could just make a sort of like shortcut
> where it's just like schema rest [schema-rust], you know, it's ethos
> rest [ethos-rust]. And datum [Datom] is basically just like a
> different syntax than nota … I'm just going to use nota to talk
> about the old syntax and schema is the old syntax. And datum is the
> new syntax and ethos is the new syntax. … So he approved the
> proposed incorrect repository roaster [roster]. … We can even rename
> the old stack to like, you know, legacy. … And I'm not too concerned
> about like reusing code for the incorrect stack and use the new
> correct stack. AI is good at writing code. And I think it only was
> taking a lot of time to write this incorrect stack because what I
> was trying to build and what the sessions with the flows were
> building was like not they had a differing view. So I was making the
> flows job harder by trying to impose all this stuff on an
> architecture that didn't didn't really need it at all. … I think we
> should just keep all of the code that's been written on in on the
> incorrect stuff. I think we should just leave it there and create
> new repositories for this like shortcut ethos to rest. And the datum
> part is not really problematic in terms of like it's a fairly simple
> thing … because it's just a serialization and deserialization logic.
> Although I think it's probably has a lot of things about its code
> that I wouldn't like and that, you know, that's about me maybe
> enunciating how I want the code written and also maybe even looking
> at the code to find the patterns so that we could better write the
> standards. And then with our new hijacking of the LLM top layer, we
> could get some very good … flows over like passes over the code that
> just sort of brings it up to a better standard of what I have in
> view … I think that eventually when we do deep passes like that,
> we're basically just going to be talking about a rewrite.

— psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated;
bracketed readings are agent transcription repairs. Rulings carried:
the incorrect-stack code is kept and left in place, frozen — no
migration of it; new repositories carry a simplified ethos-to-Rust
shortcut in the shape of schema-rust; vocabulary fixed — Schema and
NOTA name the old syntax, Ethos and Datom the new; Datom is plain
serialization/deserialization with no incorrect variant; the old
stack may be renamed legacy; slowness of the incorrect stack came
from imposing daemon-era architecture on a pipeline that did not need
it; a standards-mining pass over the existing code comes soon, and
deep quality passes amount to rewrites.

## 2026-08-11 — transcription corrected: schema-rust, ethos-rust; the generator name confirmed

> I didnt say shchema rest, I said schema-rust. that should be
> corrected. so ethos-rust is the analogue, yes

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed.
Corrects the 2026-08-10T18:49Z listener transcription above: the
dictated words were "schema-rust" and "ethos-rust", not "schema
rest" / "ethos rest". The shortcut generator repository name
**ethos-rust** is confirmed.

## 2026-08-11 — Datom does not generate Rust; Ethos does

> datom doesnt generate rust. ethos does. so I dont know what youre
> trying to say there, but its a dangerous line, and should be rooted
> out, wherever you got tha idea

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed,
answering the shortcut dispatch's mission line "Datom text in,
generated Rust out". Generation belongs to Ethos; Datom is
serialization/deserialization. The line is corrected in the standing
dispatch and the round bead.

## 2026-08-11 — schema-next is a relic; schema should be called schema-old

> thats so old! schema *is* schema-next, so it should be called
> schema-old now. the old-old-schema doesnt exist anymore. those
> terms are relics and should be rooted out too

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed,
answering the workspace manifest's schema-next / schema-rust-next
ghost entries: the current schema repo is what schema-next named; the
old-old schema no longer exists; the -next terms leave the living
documents.

## 2026-08-11 — no core-* split; three repos per component

> I dont know if we need a core-* repo. I dont see much point. so
> ethos can have all the code, minus the two signal repos, and so on
> (3 repos per component). other than reusable libraries of course,
> which we want to encourage for shared traits especially.

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed,
ruling the placement fork of the shortcut round: generated Nexus and
Sema types live in the component repository itself — no
core-<component> split, no central generated-types repository.
Component anatomy: the component repo plus its two signal repos,
three repos per component. Reusable shared libraries — shared traits
especially — are encouraged.

## 2026-08-11 — a new component named psyche; spirit-ethos should not have existed

> I have a better approach now, for a new component which will
> include spirit, named psyche, which will hold spirit, intent and
> vision, and be used to feed the hijacked llm calls (we need a name
> for that... you know what im talking about?)

> I dont even know why we made that repo. the ethos code can live
> with the component. like all components (component + 2 signal
> repos)

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed.
The first quote redirects the first-fixture fork: a new component
named **psyche** will include Spirit and hold Spirit, Intent, and
Vision, feeding the hijacked LLM calls. The second answers the
spirit-ethos repository: a component's ethos code lives in the
component repository; the anatomy is component plus two signal
repos. The psyche component's anatomy is not yet fleshed out.

## 2026-08-11 — datom confirmed; psyche is the fixture; the top-level layer enum

> 1 yes. 2 psyche is the fixture. we re-use much of spirit, and
> introduce a top-level enum; Spirit, Intent, Vision, which
> differentiates which layer records belong to. 3 yes

— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed,
ruling the remaining shortcut-round forks: (1) the Datom repo is
plain `datom`, no -incorrect variant; (2) the psyche component is the
first ethos-rust fixture, reusing much of Spirit, with a top-level
enum — Spirit, Intent, Vision — marking which layer a record belongs
to; (3) the two signal repos per component are the ordinary-socket
and metasocket ones (agent framing confirmed by the psyche).

## 2026-08-11 — the router sorts signals; a universal signal repo wraps them

> the signal ID must be how agents interpreted my vision for an
> ability for the router to differentiate between signal types for
> sorting them out. router is for signals to go across the network.
> it should be an enum in a universal signal repo that all components
> depend on, which wrap the objects. that universal-signal repo could
> also serve other functions that all signals need to deal with
> (handshake payload basically)

— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed,
on the agent-coined numeric "Signal contract ID" scheme: the real
vision is the router — which carries signals across the network —
differentiating signal types to sort them. The mechanism is an enum
in a universal signal repo all components depend on, wrapping the
signal objects; that repo may also carry what every signal must deal
with, essentially the handshake payload. The numeric ID/registry
scheme is superseded. The repo's name is not yet ruled.

## 2026-08-11 — generated Rust is committed so language servers work

> rust generated from ethos; it should probably be committed, so
> tools like language servers can work normally. we can work out a
> way to ensure freshness

— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed,
ruling the checked-in-versus-build-time fork: generated Rust is
committed, so ordinary tooling — language servers — works normally.
A freshness mechanism is deliberately left open for later.

## 2026-08-11 — the de/serializer: positional, direct to typed structs, no self-describing tags

> 1 yes, direct to typed structs. 3 what is reflection? no
> self-describing tags

— psyche, 2026-08-11T13:53+02:00 (Designer session 012fbf07), typed,
ruling the Datom de/serializer anatomy. "1 yes" confirms the
Designer's framing: schema-driven positional reading — the reader
walks the expected type, text never names fields, writing is the
exact reverse projection. Decoding lands directly in the typed Rust
structs, no intermediate document tree. No self-describing tags in
the text. "what is reflection?" awaits the Designer's plain
explanation before any ruling on codec frameworks.

## 2026-08-11 — datom is just a renamed dotos; no new repo was needed

> datom is just a renamed dotos, so there was no need to create a new
> repo. unless I missed something.

— psyche, 2026-08-11T13:53+02:00 (Designer session 012fbf07), typed.
The Datom repository is the existing dotos repository renamed — not a
fresh creation; the fresh datom repo made earlier this day was
unnecessary. Aligns with the standing rename-over-recreate rule and
with parserIsTheParser.md: one parser, nothing else implements its
own parsing logic.

## 2026-08-11 — Datom and Ethos are different languages; a shared substrate, not a shared parser

> no, I dont think so. they share an approach, but are different
> languages. they could have a shared substrate (traits with a shared
> implementation and types)

— psyche, 2026-08-11T14:06+02:00 (Designer session 012fbf07), typed,
rejecting the Designer's inference that ethos-rust consumes datom's
parser. parserIsTheParser.md governs one language's parser;
cross-language it does not apply: Datom and Ethos share an approach
but are different languages. What they may share is a substrate —
traits with a shared implementation and types. Coheres with the
same-day ruling encouraging reusable shared-trait libraries.

## 2026-08-11 — move forward; everything migrates to datom; the old repo is not a worry

> we don't need to worry about the old repo. We're just going to
> move forward and migrate everything to datum [Datom].

— psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07),
dictated; bracketed reading is an agent transcription repair.
Supersedes the same-day rename direction ("datom is just a renamed
dotos"): the fresh datom repository stands, dotos/nota stays behind,
the rename dispatch is withdrawn. Datom syntax work continues in
psyche/Vision/datomSyntax.md.

## 2026-08-11 — ethos depends on datom; Meaning goes in datom

> Meaning will be seen in datom and ethos. ethos will depend on
> datom if only because of the need to intake data for signals, so
> it can go in datom

— psyche, 2026-08-11T22:04+02:00 (Designer session a5587095), typed,
during the structured-string design (structuredStringType.md). A
dependency edge is ruled: Ethos depends on Datom, at minimum to
intake data for signals; the Meaning context therefore lives in the
datom repository, seen by both languages.

## 2026-08-13T23:11:37+02:00 — "I need to see a visual of the repo dep graphs"

> I need to see a visual of the repo dep graphs, and that there is no crossover. spirit is the only component were considering for the mvp, and since its being reworked and renamed to psyche, then there is no problem. the new correct stack is out of scope for now, but it should be clearly marked and not abandnned or otherwise modified with the wrong design while we do the quick-new stack

— psyche, 2026-08-13T23:11:37+02:00 (session 019ffc53), typed.
Agent-authored context: this rules MVP scope and preservation boundary.

## 2026-08-14 — signal repo names confirmed: always the same prefix + component name

> names are good. theyre always the same prefix + component name.
> isnt that in the skill?

— psyche, 2026-08-14 (Designer session 06196cc7), typed, confirming
the agent-coined signal-psyche and meta-signal-psyche: the pattern
is signal-<component> and meta-signal-<component>. It is indeed in
the rust-component-architecture skill, which names both forms —
the Designer verified in-session.

## 2026-08-14 — universal stuff lives in protos; the protos repo opens for the substrate

> what shared framework? I want universal stuff in protos, since
> all dialects will use it. Im not worried about rewriting whatever
> is in protos right now since nothing works anyway. we can just
> leave a big non_idea_agents.md note in its repo. But id like to
> know what you mean by Codec

— psyche, 2026-08-14 (Designer session 06196cc7), typed, answering
the Designer's shared-engine fork. The universal substrate — walk
machinery, Shape vocabulary, ShapeDefined, Head, protos::Realize
and protos::Textualize, the first-pass block scanner, string
carriers — is homed in the protos repository; all dialects ride
it; datom is the pure-data dialect on top. Existing protos content
may be rewritten; a prominent NON_IDEAL_AGENTS.md note in the
protos repo marks the quick-new occupancy. Qualifies the
2026-08-13T23:11 terminal-stack protection for the protos repo
specifically. "Codec" identified as agent jargon carrying the
dropped code vocabulary — the word dies; the Designer's
explanation given in-session.
