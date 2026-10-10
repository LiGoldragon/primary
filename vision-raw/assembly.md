# Assembly

## 2026-08-21 — two things: the registry (index of sources) and the assembly file; combined by new into a resolved assembly; both datom

Design session `2b34fafa`, dictated (captured 2026-08-21), ruling the
one-thing-or-two fork on the manifest. Bracketed readings are agent
transcription repairs ("REST" reads Rust, "datum" reads Datom, per
the session's established STT repairs):

> We should have two things. One is an index of all the sources. That
> way we can have different indexes when we have an epic branch or a
> train that points at different branches for certain things. And
> then so that I don't know what is the canonical way to call that
> sort of registry. And then the assembly file. So both of them are
> in datum [Datom] format, obviously, like when they're read. So that
> agents and humans can author them and read them. And so you would
> have the assembly file. I think I like that better than manifest.
> And then the registry. And then you would have an assembled or a
> particular assembly file. Which would combine both the registry and
> the assembly file or something like that. Or resolved, yeah, a
> resolved assembly file. Which is created, so it's not from, right?
> It's not try from. You just create a new resolved assembly file or
> a resolved assembly, rather. And this takes a registry and a plain
> assembly file. And this creates a resolved assembly. Which then,
> yeah, that's the assembled source. So you don't have to, we don't
> have to always do try from. We can do new, right? The new method.
> And I think the new method, right, is, I think there's an
> abstraction in REST [Rust] which is missing. Maybe somebody made a
> crate for it. But when something has a new method, it means that it
> can be created. So that's a property, that's a trait. So maybe
> somebody has made a crate for this. You can look. If not, we can
> come up with our own concept. And maybe even make a separate crate
> as sort of like corrected REST [Rust], right? Or, yeah, completed
> REST [Rust] or something like that. Where all of the abstractions
> that are kind of missing are added. And, yeah, I think that that
> trait would be create, right? So this thing can be created. So I
> like, by the way, and we can write this down as a ruling. And I've
> had a discussion with this about how to name trait. And I've seen
> traits come up like writing, well, no, maybe that's not a good
> example, but walking or something like that. It would be walk. So
> we would use the sort of infinitive form of the word, of the verb,
> I mean. If it's an action that can be purely described as an
> action, like write, read, resolve, create. So that's how we would
> call this trait, I think, for the new is create. And that would
> also be a sort of common way to do things. And let's do it
> efficiently so that we don't keep doubling the memory size. If we
> create something from certain objects and then these objects are
> dropped, let's make sure that we didn't use references to these
> objects so that these objects can be properly dropped. If that
> makes sense, make sure that I'm actually in line with how Rust
> works when I say that and you can explain it back to me.

Context (agent-authored): rulings and directions carried —
(a) two things, not one: the **registry** (an index of all the
sources; different indexes possible for an epic branch or a train
pointing at different branches; the canonical name for such a thing
was asked) and the **assembly file** (liked better than "manifest" —
manifest is dead as the name); both are Datom when read/authored, by
agents and humans alike;
(b) a **ResolvedAssembly** is created — new, not TryFrom — taking a
registry and a plain assembly file; the resolved assembly is the
assembled source ("that's the assembled source");
(c) not everything is TryFrom; new is fine — and creatability is a
missing Rust abstraction: a **Create** trait ("when something has a
new method, it means that it can be created. So that's a property,
that's a trait"); a crate search ordered ("You can look"), else our
own concept, possibly a separate crate of the missing abstractions —
"corrected Rust" / "completed Rust";
(d) the trait-naming ruling is logged in traitsAsCapabilities.md
2026-08-21 (infinitive verb form);
(e) efficiency direction: creation must not double memory; the
created thing must not hold references into its inputs so the inputs
can drop — Rust confirmation asked of the Designer and given
in-session (move semantics: consume by value, no heap duplication).

## 2026-08-21 — no crate; new from a tuple works

Design session `2b34fafa`, typed (captured 2026-08-21), on the
crate-search verdict (the lane is vacant; the tuple encoding is
available today, reports/CreateTraitCrateSearch-2026-08-21.md):

> "nevermind the crate, if we can do new from a tuple, that will
> work."

Context (agent-authored): supersedes this topic's completed-Rust
crate direction — no separate crate. The Create capability is defined
in our own code with tuple-encoded inputs, e.g.
`Create<(Registry, AssemblyFile)>` for ResolvedAssembly. Which repo
homes the trait is undecided.

## 2026-08-21 — Create dissolves: it would just be TryFrom

Design session `2b34fafa`, typed (captured 2026-08-21). The full
statement is logged under worldModelBeforeCode.md 2026-08-21; the
line bearing on this topic:

> it would just be TryFrom, not create, so theres nothing to make.

Context (agent-authored): supersedes this topic's Create-trait
entries entirely. With tuple-encoded inputs, multi-input creation is
`TryFrom<(Registry, AssemblyFile)> for ResolvedAssembly` — the
standard trait family covers it; no new trait, no crate, nothing to
make.
