# Handover — Drop obsolete goldragon commit-format doctrine

## Focus
Remove the obsolete commit-message-format doctrine from `goldragon`'s
`AGENTS.md`. Tracked by bead `primary-6obv.11`.

## Settled intent (psyche decision)
The three-tuple commit-message format documented in `goldragon`'s `AGENTS.md`
is garbage and is to be dropped. Doctrine follows practice: the plain message
form actually in use stays, the unused three-tuple format goes.

## Confirmed facts
- `goldragon`'s `AGENTS.md` documents a three-tuple commit format
  `(("CommitType","scope"),("Action","what"),("Verdict","why"))`.
- `goldragon`'s actual commit history uses plain `goldragon: <summary>`
  messages; the three-tuple format was never adopted in practice.
- `goldragon` is a jj-only data repo with push-immediately discipline.
  Location: `/git/github.com/LiGoldragon/goldragon`.

## Open / tracking
- Bead `primary-6obv.11` (P3, open) tracks this; close it once the doctrine is
  removed.

## Pointer
- The divergence was surfaced during authoring of `goldragon`'s
  `ARCHITECTURE.md`.
