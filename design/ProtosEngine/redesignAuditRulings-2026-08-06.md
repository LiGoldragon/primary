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

## Ruling: the bootstrap commit is atomic

Agent text answered: codex reset-audit question 1 — should one commit
journal the authorized identity/metadata transition and install
canonical Ethos plus generated Rust atomically, closing the current
split-authority and partial-install defect (schema-rust
`write_or_check`, bootstrap.rs:276-283, installs source then Rust
sequentially with a partial-failure window)?

Psyche ruling: approved on managerial recommendation [psyche-verbatim:
"go with your recommendation ... I did not understand what your
question #1 is about, but trust your recommendation"]. One commit
journals the authorized identity/metadata transition and installs the
canonical Ethos source and the generated Rust together, atomically —
all or nothing. This applies the standing atomicity law at the
bootstrap boundary; `CommitBootstrap` is the committer the
`PreparedBootstrapTransaction` model already anticipated. Callers
cannot manufacture authority proofs, receipts, seats, or fixture
vocabularies.

## Ruling: role memberships stay positional; no universal marker traits

Agent text answered: codex reset-audit question 2, presented against
the standing 2026-08-02 ruling that homed universal
Input/Output/Refusal/StreamOpen/StreamEvent traits in the `protos`
crate, while the shipped bootstrap model derives memberships
positionally.

Psyche ruling (on managerial recommendation, same approval): Input,
Output, and Refusal remain encoded positional role relations that
generate component-specific traits. Universal empty Rust marker traits
are not created; any that exist die. The 2026-08-02 "universal traits
home — protos crate" ruling is superseded (notice placed in
`ethosProductionFirstTargets-2026-08-02.md`).

Management extension, low seniority until countersigned: the same
ground covers StreamOpen and StreamEvent — the stream lifecycle stays
encoded family seats generating component-specific surfaces; no
universal stream marker traits either.

## Ruling: WholeLogosPreservedSemaFamily dies

Agent text answered: codex reset-audit question 3. Verification found a
stored-state adoption record (core-logos src/whole.rs:884, exported
lib.rs:81) whose constructor is test-only — production never attaches
one — while its read path sits in the production codec (rust-logos
src/codec.rs:1024,1029) rendering nothing living.

Psyche ruling (on managerial recommendation, same approval): it dies
with the rest. Consistent with the replacement-kills ruling and the
FrozenMagic precedent: stored-state readability is not grounds for
survival, and a record nothing living constructs has no claim. A future
store-adoption need returns as designed work at its stage, not as a
survivor. The Legacy-naming option is moot on this evidence.
