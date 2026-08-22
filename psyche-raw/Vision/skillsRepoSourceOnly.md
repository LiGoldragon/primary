# Skills repo is source-only

> "I dont want to see any .claude or .agent in the skills repo"

— psyche, 2026-08-10, steward session

Context: the generator had been writing output into the source
checkout. The psyche confirmed generated output belongs only in
consumer workspaces (like primary), not in the skills source repo.

## 2026-08-14 — requires X in the description, nothing else

> ahh, thats wrong. it should only say "requires X" in the
> description, nothing else. get that fixed

— psyche, 2026-08-14T13:23+02:00 (Designer session ba906ae2),
typed, on learning that the generator realizes a skill's
"Requires: psyche" by inlining the required skill's full text into
each dependent skill's generated file. Ruled: a dependency is a
reference only — the generated dependent skill carries "requires X"
in its description and nothing else; the required skill's text is
never embedded.
