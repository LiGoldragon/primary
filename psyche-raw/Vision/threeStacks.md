# The three stacks

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

## 2026-08-11 — move forward; everything migrates to datom; the old repo is not a worry

> we don't need to worry about the old repo. We're just going to
> move forward and migrate everything to datum [Datom].

— psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07),
dictated; bracketed reading is an agent transcription repair.
Supersedes the same-day rename direction ("datom is just a renamed
dotos"): the fresh datom repository stands, dotos/nota stays behind,
the rename dispatch is withdrawn. Datom syntax work continues in
psyche/Vision/datomSyntax.md.

