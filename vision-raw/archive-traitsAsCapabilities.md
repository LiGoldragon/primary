Archived as superseded by "code/encoded dropped" and "textualize is approved" (transcodable vocabulary, 06196cc7/ba906ae2), "no Create alias over TryFrom/From" (aa4c7747), and qualifier-named kinds (Vision/ethos.md Naming), flow e996e8, 2026-09-04. The words are kept here.

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
