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

## Ruling: the colon joins a name to its transformer head

Agent text answered: the manager's analysis agreeing that
`Name.Transformer.(...)` overloads the dot — a reader cannot classify
`A.B.C` as name chain or transformer application until `.(` arrives —
while a colon announces the transformer at the name boundary, restores
the guaranteed-plain dot-world, and reuses the colon's ruled
context-scoped qualification role.

Psyche ruling [psyche-verbatim]: "I think Name:TransformerName.( ... )
is the better syntax for named transformers. The other syntax will
create difficult parsing and reasoning." Confirmed after the analysis,
with the additions: "and : remains legal in a position expecting a
string", and — against the manager's description of the dot as
separating chained names (`Technology.Software.Programming`) — "no,
that is scrapped", and — against "it opens plain data" — "you mean, it
opens a delimiter. everything is data".

Seated:

- Transformer applications are `Name:Transformer.(payload)`. The colon
  separates the declared name from the transformer head; `.(` still
  opens the payload. This supersedes the head-joining dot of the
  2026-08-04 `.( )` ruling (notice placed there).
- The colon stays context-scoped: qualification separator in import
  space, name-to-transformer binding at declaration positions, and a
  legal interior character wherever a string is expected.
- Multi-segment dotted name chains are scrapped; the form leaves the
  grammar (notice placed in `dotosSyntaxCorrections-2026-08-02.md`).
- Language correction for the record: everything is data; the dot opens
  a delimiter. The dot/colon distinction is payload-opener versus
  transformer-head, not data versus non-data.

## Ruling: a stream is several source objects; the bundled expansion dies

Agent text answered: the manager's account of the shipped bootstrap
stream lifecycle family — one authored `Name.Stream.(Query Event)`
expanded at sealing into three declarations, with the authority minting
two hidden identity seats for the initiation and termination — defended
as the non-repetition law at work.

Psyche ruling [psyche-verbatim]: "When I explained that a stream is
several parts, I was disqualifying the object that tries to put all of
the components of the stream in one source object. So your whole
problem should probably go away. Like you say, does it go in input,
does it go in output, it's because you're trying to put two objects
into one, that doesn't work either. That's not non-repetition. That's
trying to fit a square block in a triangle hole." On the shipped
mechanism: "which means it must now be deleted".

Seated:

- No source object bundles a stream's components. The opening query,
  the stream, and any termination are separately authored objects, each
  in its natural position; roles remain positional.
- The shipped bootstrap family expansion — authority-supplied
  initiation/termination seats and the derived three-declaration
  family — is disqualified and must be deleted (bead filed on the
  cleanup car).
- Open, awaiting psyche: whether a stream is a regular output (its
  streamness carried by its type rather than by a special role), and
  whether Input/Output position items implement universal Input/Output
  traits — the psyche has reopened the marker-traits question ruled
  earlier this same day.
