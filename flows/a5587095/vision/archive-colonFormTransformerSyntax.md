Archived on landing: distilled into Vision/datom.md (Syntax), flow e996e8, 2026-09-04. The content is carried there; the words are kept here.

## 2026-08-11 — transformer payloads take `.[` or `.{`; parentheses freed in Ethos

> I think we are wrongly using parenthesis in ethos now, since we
> introduced X:Transformer syntax, which differentiates transformers
> (and some transformers might expect a single vector, in which case
> .[ is better, and for the rest expecting a structured input .{ is
> the right delimiter). This would free patenthesis completly, and I
> have an idea for a revolutionary type; a structured string type -
> something that would revolutionize LLM performance by exposing the
> emphasis and other structural aspects which a plain string simply
> doesnt have. think of it as an annotated string

— psyche, 2026-08-11T18:53+02:00 (Designer session a5587095), typed,
during the Datom syntax round's parentheses fork.

Context, kept apart from the quote: supersedes the `.(` payload
opener of 2026-08-06 — the colon already differentiates transformers,
so after `Name:Transformer` a payload that is a single vector takes
`.[` and a structured payload takes `.{`. Parentheses then carry no
Ethos duty. The structured string idea is carried in
structuredStringType.md.
