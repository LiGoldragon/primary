## 2026-08-16 — single-implementor traits: a trait design training problem

Design session `e4be1c4a` (captured 2026-08-16T18:13+02:00; source
messages earlier the same session). Context: probing protos, the
Designer showed `Headed` — a public single-method trait whose only
implementor is `Block`. The psyche, typed:

> "i dont see the purpose, as in needing a trait specifically for
> this one impl. what other traits does block implement? if it
> implements any other related trait, we have a trait design
> training problem"

The fetched matrix then met the psyche's stated criterion: Block
implements `Headed`, `BlockRendering` (private), and `Textualize` —
`BlockRendering` and `Textualize` are related (both produce Block's
textual form); crate-wide, 24 of protos' 30 src traits have exactly
one implementor, including five private single-method traits all
implemented only by `StructuralWalk`. The psyche then directed a
new session on trait design via a deliberately vague prompt
(unseeded, per the seek-disconfirming-evidence spirit). The
Designer's fusion-law fork (mandate scope: public-surface-only vs
everything-with-justification vs unrestricted) was posed but is
UNRULED.

## 2026-08-17 — the problem is fragmentation: many single-function traits on one type are probably one trait

Design session `e4be1c4a`, typed (captured 2026-08-17T11:28+02:00),
correcting the Designer's single-implementor framing of the trait
design training problem:

> "the problem isnt that it only has one implementor, but that many
> of those traits should be one. if one type implements a bunch of
> single function traits (or is that what you meant by one
> implementor), then all those traits are probably only one trait"

Context (agent-authored, separate from the psyche's words): the
Designer's metric was trait-side (a trait with exactly one
implementing type); the psyche's is type-side — one type carrying
a pile of single-function traits signals those traits should fuse
into one. On the protos matrix this reads: StructuralWalk's five
private single-method traits (plus its Walk/WalkObserving) are the
prime case; BlockScanner's three private traits and Block's
Headed/BlockRendering/Textualize likewise. Traits genuinely shared
across types (Walk, WalkObserving, CursorObserving) are not the
target.

