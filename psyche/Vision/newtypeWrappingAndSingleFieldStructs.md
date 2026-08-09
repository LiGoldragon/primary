# Double newtype wrapping and single-field structs

> "and im trying to understand what Submit.Request is? is it a newtype
> around another newtype? Looks really confusing to me."

> "And what are the double new type wrapping about? I don't like it.
> I don't like the single field struct."

— psyche, 2026-08-07, captured 2026-08-07T18:59Z (Designer session d63804f2)

Context, kept apart from the quotes: spoken while reviewing the Codex
draft fixture for the observer interface, which declared `Submit.Request`
over `Request.String` — a newtype around a newtype — and
`Rejected.{String}`, a single-field struct.
