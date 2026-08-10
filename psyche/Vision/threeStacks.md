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
