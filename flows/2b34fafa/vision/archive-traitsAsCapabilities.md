Archived on landing: distilled into Vision/ethos.md (Naming, Kind), flow e996e8, 2026-09-04. The content is carried there; the words are kept here.

## 2026-08-18 — Realize and Textualize are never on the same type; the text realizes, the real textualizes

Design session `2b34fafa`, typed (captured 2026-08-18), on the
ontological map's proposal that the scoped block-level
realize/textualize pair be one or two traits implemented by the same
dialect type (as the current datom and ethos code does):

> "realize isnt implemented by the same type as textualize. if you
> cant find two different types, the implementation is wrong. You
> dont textualize the text, and you dont realize the realized data."

Context (agent-authored): the textual type carries Realize (it
realizes into the real type); the real type carries Textualize (it
textualizes into the textual type). Any type implementing both — as
every datom and ethos block-level type currently does with the
dialect-local pair — is a wrong implementation. This closes the map's
open question 1 (two capabilities, on two different types) and moves
the block-level realize side off the real types.

