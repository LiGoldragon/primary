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

