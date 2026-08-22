# The main function

## 2026-08-21 — main is a few lines; the program is a spec of objects tied by conversions; TryFrom lets you think end-result first

Design session `2b34fafa`, dictated (captured 2026-08-21). Bracketed
readings are agent transcription repairs; the psyche's own repair
note, sent immediately after: "some stt rest = rust".

> Okay, I didn't read everything you said because it's becoming clear
> to me and I just want to say this.
> We want to start from the top or the bottom, however you want to
> see it, the main function.
> And in the main function, it has to be very clear. It's only a few
> lines, right?
> So it's like result. So I think in the end we're going to have a
> whole bunch of implementations of try from [TryFrom] or just from
> [From] if it can't fail.
> So you get whatever the end result is and then try from and then
> the most high level type.
> So we're going to create an object for everything, basically,
> instead of...
> Because most programmers, most programs I guess you could say,
> create the schema in the code instead of creating the schema and
> then just tying it up with a few lines.
> So if you broke down like a main function and then the average
> program out there, you would see the schema like in between the
> lines.
> If you read between the lines, you would see, oh, he's creating an
> object to represent all of the source code or the program instead
> of creating a spec that is an object that is a fully compliant data
> tree, a graph of data that can yield the entire program or all of
> the source code of it.
> And then you break it down once you have the high level function,
> like here's how the program is going to start and end.
> Then you go into each type and you break it down. So what is the
> result, whatever that result is for that program?
> What is that? Right. And then you could break that down into
> several lines.
> Like, let's say the generated rest [Rust] comes from such and such.
> Like eventually, when we have the three demons [daemons], for
> example, in the Protoss [Protos] engine, the generated rest [Rust]
> comes from the logos, not just logos, right?
> It's specific. It's like a total program logos. It's like a full
> program of logos, a full logos program, which is going to have a
> spec.
> So we're specifying everything. And then we're creating the traits.
> Try from or whatever it is like the more specific traits are going
> to be when we delve deeper into it, like the import reference,
> right?
> Is resolved or the import is try from import reference. So you just
> have all of these conversions from this into this or into try into
> [TryInto] or try from [TryFrom].
> Usually you kind of want to try from because it allows you to think
> about the end result first, not that you have to write it like
> that.
> It's just. I don't know, you can you can give me your pushback on
> that.

Context (agent-authored): the program's shape — main is a few clear
lines; the knowledge lives in the types (the spec: an object, a fully
compliant data tree/graph that can yield the whole program); the code
between types is conversions, From when infallible, TryFrom when not;
TryFrom preferred because the end result is named first and asked
what it comes from; more specific traits appear deeper down. Example
given: generated Rust comes from a full Logos program (the eventual
three-daemon Protos engine). On import resolution: "the import is
try from import reference" — whether this names the resolved thing
an Import (revising "there are no Import's",
importResolution.md 2026-08-20, which concerned the authored side)
was posed back to the psyche as a question, unanswered at capture.
Pushback was invited and given in-session. Continues
worldModelBeforeCode.md 2026-08-20/21.

## 2026-08-21 — the top is the assembled source, which includes the manifest; two things make a new type; monolith first, not logos

Design session `2b34fafa` (captured 2026-08-21), answering the
Designer's pushback and correcting the Designer's main sketch (which
started from text loaded at a path, and staged through a Logos
program):

> Yeah, you kind of get it, but your program is absurd. What you're
> going for is not text. It's the assembled source, which would
> include the manifest. So, I mean, I understand that what you're
> saying, tryFrom only takes one argument. So, it's not necessarily
> always the best way to do it, I guess, unless, well, if you build a
> thing from two things, so then can't you just create a new type
> that can be created? So let's say like the assembled source takes,
> well, the assembled source takes the manifest, doesn't it? Like to
> me, that seems to be the most obvious thing. And then we're not
> going to do logos, right? Because we're doing, well, not right now,
> we're doing the monolithic ethos first. But yeah, not everything is
> a conversion, of course. Like I said, from a high level, you can
> look at most of this stuff as a tryFrom or a new type, but then
> eventually you have to go down into more specific behavior.

Context (agent-authored): the top-level thing the program goes for is
the **assembled source**, which includes the manifest — not raw text.
The one-argument answer: a thing built from two things gets a new
type that can be created (the assembled source taking the manifest is
"the most obvious thing"). The near-term chain targets the ethos
monolith, not Logos. High level reads as TryFrom/new-type;
deeper levels are more specific behavior. The Import-as-resolved-
thing question posed the previous turn was not answered; it stands
open.

## 2026-08-21 — assembled Rust, not generated: still-to-write is not yet generated; the assembled source comes from the manifest; maybe an assembly file

Design session `2b34fafa` (captured 2026-08-21), continuing the same
exchange, on the Designer's corrected main sketch:

> Also, I wouldn't call it generated Rust because if you need to
> still write it, it hasn't been generated yet. So it would be more
> like assembled Rust. And I don't know why you wouldn't do the
> assembled source from the manifest. The manifest should have
> everything you need. Like maybe we don't have the same idea of a
> manifest, maybe we need another type, kind of like how the cargo
> file works, but more specific, where it doesn't have more than one
> possible output. So it's a kind of an assembly file, if you will.

Context (agent-authored): two corrections and an opening. The Rust
value is **AssembledRust** — a thing that still needs writing has not
been "generated"; the name must be true of what exists at that
moment. **AssembledSource's TryFrom origin is the Manifest** — it
should have everything needed. And the manifest concept itself is
opened: the psyche's manifest may be more than the name→source
associations of importResolution.md 2026-08-20 — possibly another
type, like the cargo file but more specific, with no more than one
possible output: an **assembly file**. Whether the lookup table and
the assembly file are one thing or two was posed back to the psyche,
unanswered at capture. (Ruled two the same day: assembly.md
2026-08-21.)

## 2026-08-21 — From is better than Into; everything is demand-driven

Design session `2b34fafa`, typed (captured 2026-08-21). The full
statement is logged under worldModelBeforeCode.md 2026-08-21; the
line bearing on this topic:

> I think the From is better than Into, since in reality, we need to
> create things *from* other things; nobody harvests a material and
> then asks what this can be made into; everything is demand-driven.

Context (agent-authored): rules the conversion spelling: From (and
TryFrom), never Into, matching the end-result-first reading of the
chain. Rust's mechanics agree — implementing From yields Into for
free, and the ecosystem convention is to implement only From.

## 2026-08-22 — main's chain begins at the input: a strictly typed object coming in as datom

Design session `bc05da32`, typed (captured 2026-08-22), correcting
the software-design draft's main example, which began at loose
paths:

> in your main block, you forgot the input, which is a strictly
> typed object coming in as datom.

Context (agent-authored, separate from the psyche's words): the main
chain gains its first conversion — the typed input realized from the
arriving datom; the paths the example once took loose are the
input's contents. Continues flowDaemon.md 2026-08-18 (100% typed
datom messages in/out). The input type's exact name and the datom's
carrier (how it reaches main) remain undesigned, flagged in the
draft's provenance (choice 9).

## 2026-08-22 — maybe all we want is a simple macro: datom-derived type in, input selection and conversion boilerplate out

Design session `bc05da32`, typed (captured 2026-08-22), refining the
same exchange after the derive-for-config idea was ruled out
(interfaceRootEnumerators.md 2026-08-22 — configuration comes from
the datom's shape):

> maybe all we want is a simple macro that takes a datom derived
> type as argument and creates all the input selection and
> conversion boilerplate.

Context (agent-authored, separate from the psyche's words): the
entry machinery shrinks to a thin macro — given the datom-derived
input type (the interface's root enum), it generates the
OS-boundary boilerplate: selecting where the datom arrives and
converting it into the typed input. No UI generation — the shape is
already the interface. Tentative ("maybe"); tracked as a bead. Open
there: macro versus emission by the same generator that writes the
interface types; the channel set the selection covers.
