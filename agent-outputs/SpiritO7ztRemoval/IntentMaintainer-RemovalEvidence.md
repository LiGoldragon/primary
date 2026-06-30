# Spirit Record o7zt Removal — Execution Evidence (2026-06-30)

## Task and scope

Psyche ruled Spirit record `o7zt` is not intent (its durable kernel is already
carried by live `jlo7`). Remove it archive-first and fully recoverable,
consistent with the prior strict-cleanup pattern (removal commit `d3e2fd34`).
Touch ONLY `o7zt`. Privacy Zero/public. Do not judge, remove, or recapture any
other record. Do not touch Guardian code/config or deploy.

## Outcome

- `o7zt` removed. `(Lookup o7zt)` returns `(Error [record not found])`.
- Live active count dropped by exactly one: baseline 22 -> 21.
- Zero-certainty set returned to 0 after the sweep (nothing else caught).
- Kernel survivor `jlo7` still live (untouched).
- Record body archived into the live archive store (recoverable).

## What o7zt was

`o7zt`: domain `[(Language Rhetoric)]`, kind `Correction`, certainty/importance
`VeryHigh`/`VeryHigh`, privacy `Zero`, referent `[psyche reporting identifiers
plain-language]`. Substance: when communicating with the psyche, lead with a
short plain-language description; an opaque identifier is at most a quiet
trailing reference and in reports is always paired with a description; state the
concrete referent before naming it; prefer plain English over jargon. The
psyche ruled this kernel is already carried by live `jlo7` (Principle: "State
everything positively: name what a thing is, what we want from it, and why we
want it... The why carries more weight than the what-not-to-do.").

## Operation used (archive-first, psyche-direct, same as the 631 removal)

1. Soft-remove to Zero certainty via the signal socket:
   `spirit "(ChangeCertainty (o7zt Zero))"` -> `(CertaintyChanged (o7zt Zero))`.
2. GUARD before the physical sweep: confirmed the Zero-certainty set was EXACTLY
   `o7zt` and nothing else (count 1; the single member observed was `o7zt`).
   Pre-op Zero set was empty (0), so no concurrent record was at risk.
3. Physical archive-then-retract via the meta socket over the guarded Zero set:
   `meta-spirit "(CollectRemovalCandidates ((Any Any Any Any None Any (ExactCertainty Zero) Any) ([(<verbatim psyche ruling> None)] <reasoning>)))"`
   -> `(RemovalCandidatesCollected (... [o7zt] ...))`. Archive happens first;
   retract only on archive Ok. This is the same archive-first physical-deletion
   path the earlier 631-record removal used.

Wire-shape note (verified against canonical source
`/git/github.com/LiGoldragon/signal-spirit/schema/signal.schema`):
`RemovalCandidateCollection { RecordQuery Justification }`;
`Justification { Testimony Reasoning }`; `Testimony (Vector VerbatimQuote)`;
`VerbatimQuote { QuoteText OptionalAntecedent }`. Testimony is therefore a
vector of `([quote] None)` entries. Reasoning is a plain `String`; canonical
bracketed text without inner parentheses parsed cleanly.

## Backups and recovery location

Pre-op sha256-verified snapshots (taken before any mutation), both under
`/home/li/.local/state/spirit/`:

- Live store:    `spirit.sema.preremoval-o7zt-20260630T141137`
- Archive store: `spirit.archive.sema.preremoval-o7zt-20260630T141137`

Primary recovery surface: the live archive store
`/home/li/.local/state/spirit/spirit.archive.sema` now holds the archived
`o7zt` record (sha256 changed from the pre-op snapshot; the
`RemovalCandidatesCollected` reply returned the full archived `o7zt` body).
Full pre-op rollback: swap the live store back to
`spirit.sema.preremoval-o7zt-20260630T141137` with the daemon stopped.

## Coordination

- Claimed `(intent-maintainer [(Path /home/li/.local/state/spirit/o7zt)])`
  before any write -> `ClaimAcceptance`.
- Released after completion -> `ReleaseAcknowledgment`.

## Checks run (exact results)

- `(Lookup o7zt)` before: `RecordFound` (live, VeryHigh certainty).
- `(Lookup jlo7)` before: `RecordFound` (kernel carrier confirmed).
- Baseline `(Count ... (AtLeastCertainty Minimum) ...)`: 22.
- Baseline `(Count ... (ExactCertainty Zero) ...)`: 0.
- `(ChangeCertainty (o7zt Zero))`: `CertaintyChanged`.
- Guard `(Count ... (ExactCertainty Zero) ...)`: 1; member observed = `o7zt`.
- `meta-spirit CollectRemovalCandidates`: `RemovalCandidatesCollected ([o7zt])`.
- `(Lookup o7zt)` after: `(Error [record not found])`.
- `(Count ... (AtLeastCertainty Minimum) ...)` after: 21.
- `(Count ... (ExactCertainty Zero) ...)` after: 0.
- `(Lookup jlo7)` after: still `RecordFound`.
- Archive store sha256 changed; backups present on disk.

## Blockers / follow-up

- None. Removal complete and reconciled. Only `o7zt` was touched.
