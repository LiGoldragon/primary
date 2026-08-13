# Traits as "capabilities"

## 2026-08-13 — all traits are qualifiers; reconsider traits as capabilities

> all traits will be qualifiers. I disagree with rust's convention
> (Write Read should be Writable and Readable).

> lets look at an update to the skills, and reconsider traits as
> "capabilities". Rethink the whole concept over and represent it
> this way

— psyche, 2026-08-13T17:17+02:00 (Designer session 6863ef19), typed,
during the from-scratch trait re-cut of the Datom/Protos walk.
Rules the open 2026-08-06 question (encodedFormFingerprintTraitDesign.md:
"are we using nouns or qualifiers for traits?"): qualifiers, always.
Directs a skill update (wording to be psyche-approved before landing)
and a re-representation of the whole trait concept with traits as
capabilities.

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
