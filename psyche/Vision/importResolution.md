# Import resolution

## 2026-08-20 — the first path segment resolves from a datom manifest, else the document's directory

Design session `2b34fafa`, typed (captured 2026-08-20), on what
`signal/domain` in an import position denotes:

> "signal in signal/domain must be resolved from a manifest (which we
> must spec obviously), which uses datom. if signal has no entry, it
> will look in the directory of the document where the import takes
> place. signal/domain would be signal/domain.ethos. if the manifest
> resolves, signal will point at a source root (need to discuss the
> naming; lets brainstorm on this), and domain will be the file
> (domain.ethos)."

Context (agent-authored): the manifest is written in datom and is to
be specced. Fallback: no manifest entry means the path is relative to
the importing document's directory. The name for what a manifest entry
points at ("source root") is open for brainstorm.
