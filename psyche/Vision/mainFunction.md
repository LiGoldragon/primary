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
