# Nomos Train — Overnight Authorization Addendum

**Addendum to:** `NomosTrainCodexDispatch-2026-07-29.md`

**Authority:** `PsycheVisionReacquisition-2026-07-29.md` Entry 7 (protos-engine
main commit `b0e47e43`, "design: record overnight leans at not-understood-by-psyche
grade").

**Grade banner:** every decision in this addendum is **not-understood-by-psyche**.
The managing agent's leans, taken under the psyche's explicit authorization to
keep the train moving overnight: "go with your leans, mark those topic as
not-understood by psyche, and produce an addendum for codex to be able to keep
slicing while I sleep." The psyche has not reviewed the substance of any decision
below. All are reversible on his review. None may ever be cited as psyche ruling,
psyche conviction, or psyche endorsement. Code and documentation referencing
these decisions must carry the grade marker specified in section 1.

## 1. Grade Marker

Every bead note, commit message, design comment, or code comment that relies on
a decision from this addendum must carry the following marker:

**`[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`**

This marker means: the decision was taken on the managing agent's lean, the
psyche authorized the lean without reviewing the substance, the decision is
reversible on his morning review, and the psyche's morning-review section in
bead notes may reverse it.

## 2. The Nine Decisions

### Decision 1 — ScopeOf helper identity

**Lean:** recursive helper scope types are implementation structure under the
single authored result identity. Scope values are typed paths of existing
source-variant encodedIDs. No translator IDs are minted for helpers.

**Concrete semantics** (from `ScopeOfIdentityBriefing-2026-07-29.md`):

- Scope values are paths of already-existing Domain variant encodedIDs. A scope
  selecting "all of Programming" is the path `[Technology, Software,
  Programming]` — each element is the encodedID of a variant that already exists
  in the authored Domain tree.
- `[Domain::All]` matches only entries tagged `Domain::All` specifically. It does
  NOT mean "match everything." **This is a legacy behavior change:** in the
  legacy system, `DomainScope::All` matched everything. Under this lean,
  root-level catch-all ("match everything") is expressed outside the scope value
  itself (e.g. by an empty scope set meaning "no filter"). Flag with:
  `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30 — legacy behavior change: All matches only itself]`
- Ending a path after a payload-bearing variant without extending into its
  children represents that child level's synthesized catch-all (truncation as
  catch-all).
- Expansion refuses atomically on: missing source tree, stale source tree
  (structural mismatch), cyclic source trees, unsupported source structures
  (a source type that is not an enum tree), unresolved variant references, and
  unrepresentable source graphs.
- Archive decode refuses: unknown IDs (a variant encodedID not found in the
  current Domain tree), invalid paths (an encodedID sequence that does not follow
  the tree's parent-child relationships), bad All semantics (misusing the All
  variant), corrupt descriptors, and version mismatches. Any failure is a hard
  refusal — no partial decoding.
- Migration folds the old nested enums into encodedID paths without a
  dual-format runtime adapter. The fold belongs to the migration lane, not to the
  ScopeOf implementation bead.

**What this unblocks:** `protos-engine-po2.7` (ScopeOf) — the first of its two
psyche-ruling blockers (helper identity) is now a graded lean.

**What the worker builds to:** implement ScopeOf expansion producing typed
source-encodedID paths, not durable Universal declarations. No translator
identity for helpers. The worker must carry the grade marker on every commit
and bead note that relies on this decision.

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

### Decision 2 — Escape-vocabulary growth

**Lean:** the transformer template algebra grows two typed members:

1. **Fold** — a construct for tree recursion with fresh typed parameters bound
   per step, leaf termination, and termination checkable at transformer-compile
   time. This is the mechanism for ScopeOf's walk over a variable-depth Domain
   tree (the second of po2.7's two blockers).

2. **Targeted positional insertion** — Splice cannot express inserting at a
   specific slot in a vector. A construct for typed positional insertion is
   needed (the psyche's own "a particular spot in a vector where a certain item
   gets inserted" from Entry 5).

Both are typed data, not runtime escape-hatches. Both are checked pre-evaluation
in the po2.15 pattern: typed pre-evaluation refusal for anything the widened
positions cannot accept, and transformer-compile-time-checkable Fold termination.

**What this unblocks:** `protos-engine-po2.7` (ScopeOf) — the second of its two
psyche-ruling blockers (the recursion mechanism) is now a graded lean.

**What the worker builds to:** implement Fold as a typed escape variant
(`Escape::Fold`) and targeted positional insertion as a typed construct. Both
participate in the Template(X) derivation's widening logic (section 11.3 of
`NomosAuthoredRulesDesign-2026-07-29.md`). Both submit to the po2.15 typed
pre-evaluation refusal discipline: a Fold whose recursion cannot be proven to
terminate at transformer compile time is refused, and a positional insertion
whose target slot is not a valid position in the widened landing type is refused.

**Dependency:** the escape-algebra growth is a prerequisite for po2.7. A
dedicated bead carries it (see section 4, bead wiring).

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

### Decision 3 — Positional-fields law scope

**Lean:** the positional-fields law ("all fields are positional, field names are
illegal everywhere") binds the wire always and all new Rust data shapes. Existing
named-field rkyv-archived structs (name-table, content-identity) are tolerated as
predating the law and migrate opportunistically, not by churn.

**What this unblocks:** law-scope ambiguity from the 2026-07-29 morning audit.
Workers can proceed without asking whether to rewrite legacy structs.

**What the worker builds to:** every new struct in the po2 train uses positional
fields. Do not introduce new named-field structs. Do not rewrite existing
named-field structs in name-table or content-identity as part of this train —
that migration is separate work, triggered when those crates have other changes
to make.

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

### Decision 4 — Alias law scope

**Lean:** bans renaming shims and compatibility aliases (`pub use X as Y`,
simple type renames for compatibility). Domain-specific instantiations of
generics (`type SnapshotDigest = IntegrityDigest<Domain>`) are permitted — they
are not aliases; they are a concrete application of a generic to a specific
domain type.

**What this unblocks:** law-scope ambiguity from the 2026-07-29 morning audit.

**What the worker builds to:** do not introduce `pub use X as Y` or rename
shims. Generic instantiation type aliases are fine.

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

### Decision 5 — syn/quote/prettyplease law scope

**Lean:** the syn/quote/prettyplease prohibition binds direct dependencies and
active transformation code paths. Transitive proc-macro dependencies via
rkyv/thiserror are an accepted cost (those crates are deep dependencies used
everywhere, and removing them is not part of this train). prettyplease leaves
with the legacy module retirement already lined up (po2.13 changed the consumer
edge; its departure is sequenced with the textual-rust pin's eventual removal).

**What this unblocks:** law-scope ambiguity from the 2026-07-29 morning audit.

**What the worker builds to:** do not add syn, quote, or prettyplease as direct
dependencies to any crate touched by this train. Do not worry about their
transitive presence via rkyv/thiserror. prettyplease retires when the
textual-rust pin retires, not before.

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

### Decision 6 — StoreSchema naming in compatibility tests

**Lean:** the `StoreSchema` naming in content-identity's byte-compatibility tests
is exempt from the schema-to-ethos rename. These tests are frozen compatibility
witnesses reproducing historical domain strings — they reproduce what was stored,
not what the system calls things now.

**What this unblocks:** law-scope ambiguity. Workers do not need to rename frozen
test data.

**What the worker builds to:** leave existing `StoreSchema` naming in frozen
compatibility witnesses as is.

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

### Decision 7 — Cross-package Invoke

**Lean:** v1 transformer packages are self-contained. An `Invoke` targeting a
transformer not defined in the same package is a typed refusal at seal time. The
design of cross-package invocation is deferred — it is not part of this train.

**What this unblocks:** removes ambiguity about whether po2.3 (manifest) or
po2.4 (seal) must support cross-package references.

**What the worker builds to:** a sealed `MacroPackage` resolves all Invoke
targets within itself. An unresolved Invoke target (one whose durable encodedID
does not match any declared transformer in the sealed package) refuses
atomically at seal time. Do not design or build cross-package resolution.

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

### Decision 8 — Conformance Law 5 gate enforcement

**Lean:** structural-codec and raw-discovery test suites get wired into
protos-engine's check-all gate. This is implementation hygiene completing
po1.8's acceptance criteria — Law 5 is homed (structural-codec
tests/conformance_harness.rs since commit 38c037d8) but not gate-enforced
(both structural-codec and raw-discovery are absent from
`identityCapsuleProducerChecks` in flake.nix).

**Grade:** this is normal-grade hygiene work, not a not-understood-by-psyche
lean. It completes an existing acceptance criterion (po1.8 required "repo AND
engine gate; only the repo half is verifiable"). Entry 7 lists it for
completeness.

**What this unblocks:** closing the Law 5 gate gap. A dedicated bead carries it
(see section 4).

**What the worker builds to:** add structural-codec and raw-discovery checks to
`identityCapsuleProducerChecks` in protos-engine's flake.nix. Verify the gate
passes with `nix run .#check-all`.

### Decision 9 — sema-engine "macro" wording

**Lean:** sema-engine's ARCHITECTURE.md carries "macro" usage for its unrelated
redb table-descriptor generator. This is out of the transformer-naming ruling's
scope. The ruling (Entry 5) retires "macro" from prose about the Nomos
transformation; sema-engine's table-descriptor generator is not a Nomos
transformer and its use of "macro" is a different, unrelated usage. Left as is.

**What this unblocks:** removes ambiguity about whether the rename sweep must
cover sema-engine's own unrelated usage.

**What the worker builds to:** do not rename "macro" in sema-engine's
architecture documentation.

**Grade marker:** `[not-understood-by-psyche, Entry 7, NomosTrainAddendum-2026-07-30]`

## 3. Standing Laws — UNCHANGED

The following standing laws from `NomosTrainCodexDispatch-2026-07-29.md` section
4 are restated for reference. None are modified by this addendum. All bind every
bead unconditionally:

- **Strictly encoded-form transformation.** No string manipulation,
  introduction, or reading of any kind in the Nomos transformation path. Every
  identifier is resolved through the nametree.
- **No string templates.** "Template" means a typed Logos skeleton — typed
  encoded data with typed placeholder (escape) positions.
- **Computed twins.** Template(X) landing types are computed by the derivation
  function, never handwritten per transformer or per Logos type (Entry 6,
  delegated assent).
- **Translator-only allocation.** Only the sema-translator allocates encodedIDs,
  and only when it receives a word it has not seen. No second allocation
  authority.
- **Transformer vocabulary.** The unit is named transformer, not macro (Entry 5).
  Existing Rust type names (`MacroDefinition`, `MacroPackage`, etc.) stay
  literal.
- **No psyche-log edits.** Append-only logs remain read-only from agents.
- **Stop-line discipline.** Anything genuinely new — a real gap, an
  unanticipated dependency, a design question not covered by the nine decisions
  above — stops the line. These leans must not be extended by analogy. If the
  worker encounters something that looks similar to a lean above but is not
  directly covered by it, that is a new question, not an implied answer.
  Record it precisely and surface it for morning review.

## 4. Work Order for the Night

Continue the po2 chain as sequenced. The current state (as of this addendum):

**Completed:** po2.1, po2.11, po2.12, po2.13, po2.14, po2.15 (6/17 closed).

**In progress:** po2.17 (P0 bug: receipt-binding integrity) — its completion
unblocks 4ph, which unblocks po2.2.

**po2.2** has substantially progressed: core-nomos 0.19.0 published at
de2518cd, language-engine-witness 0.10.0 at c6f36495, umbrella integration at
dac4a8a7 ("integrate authored Nomos naming authority"). All nix gates passed.
However, po2.2's bead is not formally closed because it depends on po2.17
(receipt-binding bug) and 4ph (allocation-free planning). The integration work
has landed; the formal closure gates have not.

### Sequence

1. **po2.17** (if not yet closed) — complete the receipt-binding bug fix.
   This unblocks 4ph.
2. **4ph** — complete the allocation-free planning consumer integration.
   This formally unblocks po2.2.
3. **po2.2** — close with evidence-bearing reason once po2.17 and 4ph close.
4. **po2.3** — manifest and entry-point file resolution.
5. **po2.4** — seal into a content-identified MacroPackage with
   Capsule<NomosKind>.
6. **po2.5** — prove authored source equivalent to fixture packages (with the
   hardened full-structural-equivalence acceptance from the audit finding: full
   structural comparison, not the po2.1 coarse fingerprint).
7. **po2.6** — nomos-engine loads authored, slotted, versioned packages.

Then, with decisions 1-2 unblocking:

8. **Escape-algebra growth bead** (new, see below) — implement Fold and
   targeted positional insertion. This is a prerequisite for po2.7.
9. **po2.7** — ScopeOf as the first complex authored transformer.
10. **po2.8** — enriched-generation surface migration, class by class.

Parallel-anytime:

- **Law 5 gate bead** (new, see below) — wire structural-codec and
  raw-discovery into check-all.
- **po2.9** — standard machinery documentation.

### Recording progress

Record progress in bead notes as you go. Open questions for the psyche
accumulate in a "morning review" section of bead notes rather than stopping
work, unless the stop-line genuinely bites (something genuinely new that is not
covered by the nine decisions above).

### Morning-review section format

When appending to a bead's notes, open questions for the psyche's morning review
go under a clearly marked section:

```
MORNING REVIEW (for psyche):
- [topic]: [what was decided under the lean, what alternative exists, what the
  psyche might want to reverse]
```

## 5. Bead Wiring Summary

This addendum directs the following bead changes (performed at addendum
publication time, not by the overnight worker):

1. `protos-engine-po2.7` — status changed from BLOCKED to OPEN (still
   dependency-gated behind po2.6). Note appended with decisions 1-2 at the
   not-understood-by-psyche grade, citing Entry 7 and this addendum. The two
   former blockers (helper identity, recursion mechanism) are now graded leans.

2. New bead under protos-engine-po2: Law 5 gate enforcement — wire
   structural-codec and raw-discovery test suites into protos-engine's check-all
   gate. Normal grade (hygiene work, not a lean).

3. New bead under protos-engine-po2 (or as a dependency of po2.7): escape-algebra
   growth — typed Fold + targeted positional insertion, per decision 2. Wired as
   a dependency of po2.7.

4. Note appended to the `protos-engine-po2` epic pointing at Entry 7 and this
   addendum as the overnight authorization record.
