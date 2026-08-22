# Traits as "capabilities"

## 2026-08-13 — types first; traits are what types implement

> we need to think very carefully of what the types are. First,
> really, because the traits are something that the types implement.
> We don't look for traits and then think of types for that. So,
> what are all the types? Let's look at the types first. We have the
> things that are, like, once they're expressed, the datum [Datom]
> types that are being read into and out of. And these essentially
> implement a lot of the traits. Like, they're transcodable. That's
> a good one. But... Yeah, I guess, or to be more exact, they're
> textually transcodable. Or datomically transcodable.

— psyche, 2026-08-13 (Designer session 6863ef19), dictated;
bracketed readings are agent transcription repairs. Method ruled:
enumerate the types first; the trait cut follows from them.

*(2026-08-14 annotation, consistency audit: the "transcodable" vocabulary introduced in this entry was superseded later 2026-08-13 by the code/encoded drop and the ruling below ("transcodable falls with the drop"); see encodedFormIsTheCode.md 2026-08-13.)*

## 2026-08-13 — common traits are the right abstraction; all protos dialects are transcodable; qualification by module

> So, if we take all the common behavior, we want to have as many
> common traits as possible, because then we're creating the right
> abstraction. So, all protos dialects, whether it's datum [Datom],
> ethos, nomos, or logos, are transcodable.

> we don't have to be afraid to use more elaborate terms if we want
> to describe what this behavior is specifically. [...] if the trait
> is transcodable, yes, and if it lives in the protos module, then
> that's not ambiguous. Because if we fully qualify the name, it's
> self-describing that it's transcodable into protos. So, yeah, I
> think that's the right way to think about it.

— psyche, 2026-08-13 (Designer session 6863ef19), dictated.
Commonality is the abstraction test; Transcodable is shared by all
protos dialects (Datom, Ethos, Nomos, Logos). Ambiguity between
forms is resolved by fully-qualified module placement —
protos::Transcodable self-describes — and elaborate capability
names are welcome where specificity needs them.

*(2026-08-14 annotation, consistency audit: Transcodable and protos::Transcodable established in this entry were superseded later 2026-08-13 by the code/encoded drop and the entry below ("transcodable falls with the drop"); successor capability names are open per that entry.)*

*(2026-08-14 annotation: closed — the psyche approved textualize
2026-08-14 ("textualize is approved"); the successor pair is
protos::Realize / protos::Textualize. See encodedFormIsTheCode.md
2026-08-14.)*

## 2026-08-20 — trait methods that are regular functions pretending to be traits; a cornerstone of models not understanding the vision; research directed

Design session `2b34fafa`, typed (captured 2026-08-20), on the
Designer's proposed trait methods for import resolution:

> "You misunderstood the trait based approach. your trait methods are
> just regular functions pretending to be traits. if the type needs a
> 'name' to resove the import, then it's not resolvable. So we found
> one of the cornerstone of models not understand my vision. Do a
> research in this"

Context (agent-authored): "resove" reads resolve. The Designer's
reading, posed for review: a trait method that must be handed the very
subject of its capability as a parameter (here, a name to resolve) is
a regular function wearing a trait — the receiver is not the thing
that has the capability. The type that carries the name (the import
reference) is what is resolvable. This joins the trait-design
training-problem lineage (rustComponentArchitecture.md 2026-08-16,
2026-08-17, 2026-08-19 "placeholder traits for every function...
training for this to be understood better by agents"), now named a
cornerstone of models not understanding the psyche's vision. Research
directed.

## 2026-08-21 — ruling: infinitive verb form for action traits — Write, Read, Resolve, Create, Walk; the new-capability trait is Create

Design session `2b34fafa`, dictated (captured 2026-08-21). The full
statement is logged under assembly.md 2026-08-21; the lines bearing
on this topic, explicitly marked a ruling by the psyche ("we can
write this down as a ruling"):

> And I've had a discussion with this about how to name trait. And
> I've seen traits come up like writing, well, no, maybe that's not
> a good example, but walking or something like that. It would be
> walk. So we would use the sort of infinitive form of the word, of
> the verb, I mean. If it's an action that can be purely described
> as an action, like write, read, resolve, create. So that's how we
> would call this trait, I think, for the new is create.

Context (agent-authored): rules the form left open by 2026-08-14
("Yes, I accept verbs"): when the capability is an action purely
describable as an action, the trait name is the infinitive verb —
Walk, not Walking; Write, Read, Resolve, Create. The capability
behind Rust's `new` convention is the trait Create ("when something
has a new method, it means that it can be created. So that's a
property, that's a trait" — assembly.md 2026-08-21). The qualifier
reading of 2026-08-13/14 stands: a type implementing Create is
capable of being created.
