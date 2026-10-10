# core-logos e0cec411 — psyche ratification (v1)

Status: RECORD. This is a decision record of a psyche ruling made on 2026-07-24. It
records an already-made decision so it is preserved forward; it does not re-open or
re-argue the ruling.

Recording note: the release-train intent at
`release-trains/language-family-slice-three.nota` is a typed contract decoded at
runtime by the release-train tooling, with slots only for its member components and
immutable externals; core-logos is not a member of that train, and the file carries
no slot for a ruling. This ruling is therefore recorded here, in the established home
for core-logos architectural records, not in that intent file.

## The ruling

The published core-logos main tip `e0cec411` STANDS as accepted architecture.

- Commit: `e0cec411` ("core-logos: migrate canonical encoded form").
- Version: `0.2.0`.
- Archive layout: `7`.
- Pins: protos `d2912838`, core-schema `90e71212`.

The psyche ruled this revision accepted as the canonical published architecture for
core-logos.

## Procedural gaps ratified after the fact

The published revision landed with three procedural gaps. The psyche ratified each
after the fact as an explicitly ruled exception, corrected forward and never by
history rewrite:

- No attribution trailer on the commit.
- Absent from the release-train record.
- Landed ahead of the id-namespace-slicing design's sequencing.

This ratification is recorded precisely so it does not read as silent precedent. It
is a ruled exception for this one revision, not a standing rule that running ahead of
the train gets accepted. Any correction is made forward; the accepted history is not
rewritten.

## Attachments to the ruling

Two revisions are attached to the ruling:

- Divergent rev `22b12a47` (bookmark `SpiritLineageBTrain`, "rename encoded form
  types") is retired: never pin, never merge.
- The local divergent main `0ba0d641` in the core-logos checkout ("add fast
  development guidance") requires reconciliation by its owning lane before further
  work builds on it. That reconciliation belongs to the owning lane, not to this
  record.

## Correction (2026-07-24)

This section corrects the record forward. The original text above is retained
unchanged for the record; nothing is rewritten or removed.

The attachment claiming that local main `0ba0d641` ("add fast development
guidance") is DIVERGENT from accepted `e0cec411` — and "must be reconciled onto
`e0cec411` or discarded by its owning lane" — is WITHDRAWN as factually wrong.
The premise was a false observation repeated by two agents without revset proof.

Explicit jj revset ancestry checks in `/home/li/primary/repos/core-logos` prove
`0ba0d641` is the DIRECT PARENT of `e0cec411`:

- `0ba0d641 & ::e0cec411` is non-empty (0ba0d641 is an ancestor of e0cec411).
- The reverse, `e0cec411 & ::0ba0d641`, is empty.
- `e0cec411-` resolves to `0ba0d641`.

`0ba0d641`'s single-file AGENTS.md addition is therefore already inside accepted
main's linear history, and `main@origin` is `e0cec411` itself. There is no
divergence and no reconciliation to perform: `0ba0d641` requires NO action.

The core ruling is UNAFFECTED. `e0cec411` STANDS as accepted architecture, and
divergent rev `22b12a47` remains retired — never pin, never merge. Only the
`0ba0d641` divergence claim in the attachments is corrected; it was proven wrong
by the explicit jj revset ancestry checks recorded above.
