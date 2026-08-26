# Datom syntax

## 2026-08-26 — a map in an expected position carries no Map head

The flow's view showed a map as `Map.[ k.v k.(v) … ]`. The correction:

> If a position expects a map, the data will be [ k.v ... ], no Map.

— psyche, 2026-08-26 (Design session ac1e9ec8), typed.

Asked in the same message, not ruled:

> Is there a scenario in which a Head. isnt a variant?

## 2026-08-26 — considering positional key/values in a map

> Im considering making key/values resolve by position in a map
>
> [ key value second-key second-value ... ]
>
> that looks cleaner and makes the Head. always a variant; lower
> cognitive cost

— psyche, 2026-08-26 (Design session ac1e9ec8), typed. Under
consideration, not ruled.

## 2026-08-26 — or a dedicated delimiter for maps

> or we could use one of the unused delimiters for maps, making them
> easy to spot visually

— psyche, 2026-08-26 (Design session ac1e9ec8), typed. Under
consideration, not ruled.

## 2026-08-26 — guillemets delimit a map

> let use the guillemets.

— psyche, 2026-08-26 (Design session ac1e9ec8), typed, choosing
between positional pairs in brackets and a dedicated map delimiter
(guillemets or angle brackets). Entries resolve by position inside;
a Head is thereby always a variant.

## 2026-08-26 — corrections to the first full-vision draft

On "Datom is the psyche's own coinage for the data notation":

> dont be so apologetic. Datom is the most advanced textual data
> format in the world.

On "Generics and Rust generation belong to Ethos":

> I said no negatives. This is useless. Do we say "JSON doesnt
> support generics"?

On "like JSON":

> Let's keep this noise out. Totally unecessary.

On "All naming and self-description live in the type":

> this is ambiguous. Try explaining it properly. You might have to
> understand it first. Apply this to the whole proposal; understand
> then explain clearly and unambiguously. Separate statements that
> make a sentence confusing when you try to say them together. Split
> everything up then re-assemble <- there's something to extract into
> distillation skill from this.

On bare strings:

> re: bare strings: make sure it's clear that a string is a string
> only in a position where the type defines a string.

On the glyph question (typed « » or ASCII << >>):

> I dont understand. those are completly different things. <> is
> used in ethos, and those two must remain compatible in case datom
> is ever eventually embedded into some ethos positions.

On "each delimiter shows its container's kind":

> this conflicts with ethos vocabulary.

On whether "the root text" opens with the variant or the type name:

> "the root text" - what are you talking about? If we are reading an
> enum, then it'll start with a variant. if not, it wont. I feel like
> you really still dont understand the datom vision. the
> implementation must be pretty bad

— psyche, 2026-08-26 (Design session ac1e9ec8), typed.

## 2026-08-26 — curly quotes are the string delimiter; parentheses reserved for Meaning; datom is the edge form of signal

On "Consistency comes first: datom's syntax is fixed before the rest.":

> what does this mean? the rest of what?

On "Curly quotes are the legacy string delimiter, read and landing as String.":

> not legacy. In fact I think they should be positioned as the
> default string delimiter. the vision is that parenthesis will
> become the delimiter for structured strings, still to be designed.
> So let's switch it all to curly quotes first, with parenthesis
> reserved for structured strings, which we currently designate as
> Meaning

On "Everything is datom: every data file and every wire message.":

> no, this is false. all our components speak signal, not datom;
> datom is only used at the edge to let text-based systems (LLMs and
> all existing editors) understand signal.

— psyche, 2026-08-26 (Design session ac1e9ec8), typed. Supersedes the
2026-08-14 ruling that parentheses are the default string delimiter.
