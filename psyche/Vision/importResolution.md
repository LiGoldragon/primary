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

## 2026-08-20 — external pulls are explicit: colon after the source name; lib.es is the default file

Design session `2b34fafa`, typed (captured 2026-08-20), later the same
conversation, revising the morning entry:

> "actually, I think the syntax should be explicit when pulling an
> external source."

> "`signal-pysche:Object` pulls Object from lib.es in signal-psyche
> source"

> "`signal-pysche:[Object Thing]` multiple imports"

> "`signal-pysche:stream.[Stream Termination]` from stream.es in
> signal-psyche source"

> "`signal-pysche:external/helper.[Start Modify]` from external/helper.es
> in signal-psyche source"

Context (agent-authored): "pysche" is the psyche's typing of psyche.
The colon marks an external-source pull; the name before it resolves
through the datom manifest; `/` stays the directory separator inside
the source; `.` separates the file (or the source name) from the
imported type or `[...]` list; the fileless form reads from `lib.es`.
Revises the morning entry's `signal/domain` reading — a bare `/` path
with no colon is document-relative. The `.es` extension appears in the
psyche's examples; the extension itself was posed as an open side
question, not ruled. Tension noted for review: 2026-08-07 moved
imports off `:` ("I would rather not create confusion with :");
placement law may resolve it — question posed to the psyche.

## 2026-08-20 — the worry behind the explicit syntax: a manifest name shadowing a local module

Design session `2b34fafa`, typed (captured 2026-08-20), on why
external pulls became explicit:

> "hmmm. my worry was if the manifest contains signal and the source
> has a signal module"

## 2026-08-20 — fallback killed: colon resolves from the manifest or errors; bare paths are local only

Design session `2b34fafa`, typed (captured 2026-08-20), confirming the
Designer's restatement ("colon → manifest or error; bare path → local
only"):

> "confirmed, kill the fallback."

Context (agent-authored): supersedes the morning entry's
document-directory fallback for manifest misses.
