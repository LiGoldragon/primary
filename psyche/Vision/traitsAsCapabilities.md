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

## 2026-08-13 — one protos representation per type; no dialect-qualified trait; a constant could name the dialect

> Any type will only have one protos representation. so the datom::
> version isnt necessary. look for flaws in my logic. It could even
> have a constant variant to give the protos dialect it is
> transcodable into

— psyche, 2026-08-13T18:09+02:00 (Designer session 6863ef19), typed,
correcting the Designer's dialect-qualified sketch
(datom::Transcodable beside protos::Transcodable): one textual
representation per type, so protos::Transcodable alone, with the
type's dialect possibly an associated constant on the capability.
Flaw search requested of the Designer; returned in the session
conversation.

*(2026-08-14 annotation, consistency audit: protos::Transcodable and the dialect-constant idea were superseded by the drop entry below ("transcodable falls with the drop") in the same session; the one-representation-per-type principle stands, now applied to the successor trait pair protos::Realize and protos::Textualize.)*

## 2026-08-13 — a type for the text block; textualize on the true type; maybe drop code/encoded

> I see a problem myself; when reading text, we dont know what we're
> reading, so how do we call a method without a type?
>
> Conceptually, we need to give a type to the text block, then we
> can have an encode trait on that, and textualize on the true type.
>
> I dont know about encode/decode; which is code and which isnt? The
> way I see it, the binary form (in rust memory, which is
> essentially the rkyv format) is the most code-like. But I think we
> might even want to drop the whole concept of code/encoded to make
> it very clear. textual/textualize is clear, so what term could we
> use for the in-memory/signal form? Is the in-memory data actually
> the same format as the rkyv in reality anyway?

— psyche, 2026-08-13 (Designer session 06196cc7), typed, answering
the Designer's fork-one proposal of a single two-way
protos::Transcodable. Open: the term for the in-memory/working
form; whether code/encoded vocabulary is dropped — which would bear
on encodedFormIsTheCode.md 2026-08-06 ("the encoded form is the
code") and the 2026-08-06 EncodedName lineage; the factual
rkyv-versus-native-memory question, answered by the Designer
in-session (two distinct layouts — the portable rkyv buffer is not
working memory).

## 2026-08-13 — transcodable falls with the drop; maybe verbs are acceptable for traits

> 1. I dont think it survives. I think we end up with things like
> WorkingFormCastable, but I want to see you make a shot at a bunch
> of different naming options
>
> Or maybe we need to accept verbs for traits, since theyre
> capitalized and therefore not a function

— psyche, 2026-08-13 (Designer session 06196cc7), typed, answering
the Designer's boundary question on the code/encoded drop.
Transcodable does not survive; the common capability and the
directional capabilities need new names — option batches requested
of the Designer, likewise for the ShapeDefined rename ("Think of a
bunch of names for that too"). A `<Form>Castable` compound pattern
is floated; verb-form trait names are opened as a possibility,
which would soften the 17:17 all-traits-are-qualifiers ruling —
unruled either way. "cast" is the psyche's live verb for
form-to-form movement throughout this exchange.

## 2026-08-14 — verbs accepted for traits

> Yes, I accept verbs. now I can see why rust went with verbs; it
> is easy to understand that a thing that which implements Run is
> CapableOfRunning.

— psyche, 2026-08-14 (Designer session 06196cc7), typed. Verb-form
trait names are accepted: the qualifier reading stays — a type
implementing Run is capable of running — while the spelling may be
the verb. Qualifies the 2026-08-13T17:17 all-traits-are-qualifiers
ruling.

## 2026-08-14 — no umbrella capability; the directional traits live in protos

> none of this makes sense if we use a trait for each direction.
> The traits should live in protos regardless (Textualize and
> whatever we pick for Materialize)

— psyche, 2026-08-14 (Designer session 06196cc7), typed, rejecting
the Designer's common-capability batch (Expressible / Formed /
Representable) that would have carried the dialect constant above
the directional pair. The two directional traits are themselves
protos-homed: protos::Textualize and the still-unnamed
text-to-form direction. The 2026-08-13T18:09 dialect-constant idea
stays floated; its home is now to be found on the pair.

## 2026-08-14 — Textualize confirmed; ShapeDefined stays

> Textualize is good

> ShapeDefined is good

— psyche, 2026-08-14 (Designer session 06196cc7), typed. The
form-to-text trait is Textualize; the discrimination trait keeps
the name ShapeDefined (fork closed). The text-to-form trait name
waits on the form name — "The right term will depend on what we
pick for working" — and Native was declined with further proposals
requested.

## 2026-08-14 — RealizeWalk, TextualizeWalk, and the Walk trait accepted

> fine. im not crazy about it but its good enough

— psyche, 2026-08-14 (Designer session 06196cc7), typed, on the
Designer's proposal: the direction-drivers are RealizeWalk and
TextualizeWalk, their conduct methods (enter, close, position,
resume) homed under the protos trait Walk. Accepted with explicit
reservation — a better name remains welcome if one appears.
