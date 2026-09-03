# Overnight dispatch: ProtosEngine Codex — 2026-08-01

The psyche is asleep. This is an autonomous work package. The cautionary
tale governing it is the NomosTrainAddendum: nine overnight leans, two
reversed within a day. So the standing rule tonight: **no design leaps.**
Where a ruling is missing, state an explicit `[assumption]`, build the
smallest thing consistent with it, keep it revisitable, and list it in the
morning report. Prefer stopping at a gate over inventing past it.

## New rulings since your last sync (read the entries, not just this list)

- `design/ProtosEngine/dependencyDagLaw-2026-08-01.md` — transformation and
  derivation dependencies form a DAG; cycles refuse with a typed error;
  atomic operations order cascades by topological walk. Fixpoint machinery
  is permanently out.
- `design/ProtosEngine/atomicOperationEditing-2026-08-01.md` — the
  operational editing model: engines hold encoded form in slots; every
  change is one atomic operation through the operation interface (signal
  message); the per-engine change log IS the VCS; same true name = same
  thing. Terminology ruled plain English: operation, operation interface,
  change log, slot. Do NOT build this infrastructure tonight — it is
  orientation, not work order.
- `design/ProtosEngine/ethosNonRepetitionLaw-2026-08-01.md` — any inferable
  repetition in authored Ethos is an implementation failure. Acceptance
  gate for every fixture you write.
- `design/ProtosEngine/genericParametersAreTraits-2026-08-01.md`,
  `capsuleIsCompilationUnit-2026-08-01.md` — as previously relayed.
- `reports/DesignConsistencyAudit-2026-08-01.md` — read before the
  salvageability assessment.
- `reports/OperationalEditingPriorArt-2026-08-01.md` — background only.

## Hard stops (violating any of these voids the night's work)

- No recursion surface (po2.19 unruled).
- No escape-spelling invention: keyword forms (Realize/Splice/Invoke) only,
  flagged provisional in every fixture.
- No identity/slot/change-log infrastructure.
- No Dotos rename execution (rides the train landing deliberately).
- No standards/skills work (other lane).
- No syn/quote/prettyplease; tuple ban (newtype exception); no strings in
  transformation; translator-only allocation; traits are always the first
  pass, exceptions noted at site per the seated standard.

## Work queue, in order

1. **The owed first deliverable** (bead primary-36y): provenance-graded
   salvageability assessment (raw-discovery, structural-codec seal-time
   disjointness, TemplateValue substrate, six-slot root) + proposed ScopeOf
   trait signatures with every unruled truth-table cell (reflexivity,
   operand symmetry, domain-side All) as a named `[assumption]`. Write it,
   then proceed consistent with it — do not block on review overnight.
2. **Slice 1** (primary-36y): the ScopeOf trait target. Contract traits
   first, hand-written reference implementation over the Domain fixture,
   tests proving All-matches-all whole-tree semantics. Generic parameters
   are traits — no bare type variables in any contract you design.
3. **Slice 2** (bead primary-pjm): minimal types-only Ethos file kind
   through the shared machinery — new root type + simple trait impl, zero
   new parsing code, round-trip test. Retire the SixSlot API naming residue
   in its wake. The root's shape is an `[assumption]` for psyche review.
4. **Tuple remediation** (register:
   `reports/RustTupleViolationsRegister-2026-07-30.md`, all 27 confirmed
   still present by the audit): follow the register's own sequencing —
   archive-compatibility check FIRST; then the mechanical sweep; defer any
   case where archive risk is unclear and say so. The misnamed 4-field
   `*Newtype` types get correct shapes, not just names.
5. **Slice 3 to the gates** (bead primary-zjo): non-recursive transformer
   parts with the handwritten mirror pair per the NON_IDEAL entry. Stop at
   the recursion gate and at any need for generated-output identity;
   document exactly where and why each gate bit — that documentation is the
   material the psyche's next rulings land on.
6. **If time remains**: supersession banners on the protos-engine design
   docs the audit flagged (NomosTrainAddendum reversed decisions, the
   compilation's capsule and imports sections — banner + pointer to the
   superseding entry, no content rewrites); prep notes for retiring the
   native.rs bounded projection indices (po2.8).

## Morning report (single file, reports/ in your worktree or primary)

Four sections: (1) built and test results, honestly, failures included;
(2) the assumption register — every `[assumption]` taken, with site;
(3) gate encounters — where slice 3 stopped and what ruling each stop
needs; (4) questions for the psyche, ranked, each explained fully enough
to answer without opening code.
