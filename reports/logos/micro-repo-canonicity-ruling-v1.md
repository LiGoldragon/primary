# micro-repo canonicity — psyche ruling (v1)

Status: RECORD. This is a decision record of a psyche ruling made on 2026-07-24. It
records an already-made decision so it is preserved forward; it does not re-open or
re-argue the ruling.

Recording note: this ruling concerns the placement of the four family
micro-repos and of protos.git, which sit across several repositories rather than
inside any single component's intent file. It is therefore recorded here, in the
established home for logos-family architectural records, alongside the
core-logos ratification it is a peer of.

## The ruling

The July-19 consolidation of the four family micro-repos — content-identity,
name-table, structural-codec, and raw-discovery — into protos.git was never
approved and DOES NOT STAND.

The "deprecate — consolidated into LiGoldragon/protos" notices placed on the
tips of those four repos are part of the same unauthorized consolidation and
are void.

The micro-repo approach is canonical. In the psyche's words: "we dont use the
monorepo style; destroy the duplication by keeping the micro-repo approach." The
duplication is removed by keeping each concern in its own micro-repo, not by
folding the four into a single repository.

## Consequences

The ruling is corrected forward, never by history rewrite:

- The deprecation notices on the four micro-repo tips are lifted by forward
  commits, not by rewriting the tips that carried them.
- Substance produced inside protos.git since July 19 is kept as work product,
  not discarded: the capsule, the short-identifier work, the name-table slice
  snapshot, and the delegation work. It ports forward into the micro-repos
  producer-first, each port carrying identity-lock witnesses.
- protos.git remains. It becomes the home of the common daemon-contract traits
  only — the separately ruled scope of the same day — not the home of the four
  consolidated concerns.
- protos.git commit `a3550f2b`'s ownership text is target-state until the ports
  land. It describes where the concerns are headed, and holds as the intended
  end state while the producer-first ports into the micro-repos are still in
  flight.

## Not ratified (contrast)

This record draws an explicit contrast with the core-logos `e0cec411`
ratification of the same day, so neither reads as precedent for the other.

- core-logos `e0cec411` was explicitly RATIFIED: an unapproved placement that
  the psyche chose to accept after the fact as a ruled exception.
- This July-19 consolidation is explicitly NOT RATIFIED: an unapproved placement
  that the psyche declines to accept, and that is therefore lifted forward.

The two together fix the default. Unauthorized placement does not stand by
default. Acceptance is a deliberate, case-by-case psyche act, as with
`e0cec411`; absent that act, an unapproved placement is undone, as with this
consolidation. Ratification is the exception, not the rule, and silence is not
ratification.
