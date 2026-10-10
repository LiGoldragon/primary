## 2026-08-20 — source is the name we use instead of crate

Design session `2b34fafa`, typed (captured 2026-08-20), closing the
source-root naming brainstorm:

> "so lets look at all the major types to represent the textual code.
> source will be the name we use instead of crate"

Context (agent-authored): a Source is the unit a manifest name points
at — the tree of documents Rust would call a crate. External pulls
(`name:...`) resolve a manifest name to a Source.
