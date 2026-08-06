# Redesign Audit Rulings — 2026-08-06

Rulings from the psyche session that reacquired the Protos engine vision
and commissioned the 2026-08-06 PM redesign-discipline audit of codex's
work.

## Ruling: a replacing design kills the replaced system

Agent text answered: the audit closed with two questions on
content-identity. (1) The crate co-exports the new whole-capsule
`ContentAddressedHash` and the old domain-separated per-item
`ContentHash<Domain>`, with ARCHITECTURE.md explicitly deferring removal
— is the old hash a superseded form that dies, or a parallel concern
that lives on its own merits? (2) `DomainSeparation::FrozenMagic` exists
solely to reproduce sema-engine's historical on-disk domain strings so
already-stored digests stay readable — does "anything old must die"
extend to mechanisms whose only job is keeping existing stored state
readable?

Psyche ruling [psyche-verbatim]: "any new design that replacess the
functionality of an existing system kills the old system."

Scope and consequences:

- This generalizes the anything-old-must-die ruling
  (`deepCenterVision-2026-08-05.md`, appended 2026-08-06): the trigger
  is functional replacement. The moment a new design replaces the
  functionality of an existing system, the old system dies — no
  coexistence, no deferred removal, no compatibility mechanism kept for
  stored state.
- Applied to content-identity: `ContentHash<Domain>` dies;
  `ContentAddressedHash` is the sole hash. `FrozenMagic` dies with it —
  readability of already-stored sema-engine digests is not grounds for
  survival, consistent with the spirit precedent of no data-migration
  machinery and manual re-entry. The byte-compatibility evidence
  harness dies (evidence harnesses were already barred by
  anything-old-must-die). The ARCHITECTURE.md deferral prose dies.
- The raw-discovery older recognizer (tracked as primary-hqu.23) falls
  under the same rule: the live source-bounded path replaced its
  functionality; the old path dies producer-first.
