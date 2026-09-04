Archived on landing: distilled into Vision/ethos.md (Naming), flow e996e8, 2026-09-04. The content is carried there; the words are kept here.

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

