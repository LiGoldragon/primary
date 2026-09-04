# Traits as "capabilities"

## 2026-08-20 — trait methods that are regular functions pretending to be traits; a cornerstone of models not understanding the vision; research directed

Design session `2b34fafa`, typed (captured 2026-08-20), on the
Designer's proposed trait methods for import resolution:

> "You misunderstood the trait based approach. your trait methods are
> just regular functions pretending to be traits. if the type needs a
> 'name' to resove the import, then it's not resolvable. So we found
> one of the cornerstone of models not understand my vision. Do a
> research in this"

Context (agent-authored): "resove" reads resolve. The Designer's
reading, posed for review: a trait method that must be handed the very
subject of its capability as a parameter (here, a name to resolve) is
a regular function wearing a trait — the receiver is not the thing
that has the capability. The type that carries the name (the import
reference) is what is resolvable. This joins the trait-design
training-problem lineage (rustComponentArchitecture.md 2026-08-16,
2026-08-17, 2026-08-19 "placeholder traits for every function...
training for this to be understood better by agents"), now named a
cornerstone of models not understanding the psyche's vision. Research
directed.
