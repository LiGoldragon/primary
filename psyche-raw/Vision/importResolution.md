# Import resolution

## 2026-08-20 — a type that needs a name handed in to resolve the import is not resolvable

Design session `2b34fafa`, typed (captured 2026-08-20), rejecting the
Designer's trait sketch for import resolution:

> "if the type needs a 'name' to resove the import, then it's not
> resolvable."

Context (agent-authored): "resove" reads resolve. Part of the
trait-approach correction logged in traitsAsCapabilities.md
2026-08-20 ("your trait methods are just regular functions pretending
to be traits"); research directed there.

## 2026-08-21 — the manifest should have everything needed to assemble; maybe an assembly file, no more than one possible output

Design session `2b34fafa` (captured 2026-08-21). The full statement
is logged under mainFunction.md 2026-08-21; the lines bearing on this
topic:

> And I don't know why you wouldn't do the assembled source from the
> manifest. The manifest should have everything you need. Like maybe
> we don't have the same idea of a manifest, maybe we need another
> type, kind of like how the cargo file works, but more specific,
> where it doesn't have more than one possible output. So it's a kind
> of an assembly file, if you will.

Context (agent-authored): may broaden this topic's 2026-08-20
manifest (name→source associations for colon pulls) or introduce a
second thing beside it — an assembly file defining exactly one
output. Unresolved at capture.
