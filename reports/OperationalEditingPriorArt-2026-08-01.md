# Operational Editing: Prior Art and Terminology — 2026-08-01

TENTATIVE research, [agent-inference] throughout. Commissioned by the psyche
after ruling the atomic operation editing model
(`design/ProtosEngine/atomicOperationEditing-2026-08-01.md`): engines hold
encoded form in slots; every change is one atomic operation arriving as a
signal message; the per-engine change log IS the version control system;
true name = content address = identity.

## Headline

No prior system covers the full model. Protos combines: Unison's
content-addressed identity with names as metadata, event sourcing's
operation-log-as-source-of-truth, projectional editors' text-as-rendered-
projection, and ACID's atomicity — a combination that appears to be novel.
The psyche has ALREADY ruled the paradigm's name in his own words:
"operational editing" (ProtosEngineDesign-2026-07-29 section 5: "You're
going to be doing operational editing. You're going to send operations, and
it'll all be atomically edited in the daemon.").

## Prior art, by genuineness of match

| System | Identity | Op-log-as-VCS | Typed/structural | Atomic |
|---|---|---|---|---|
| Unison | HIGH | LOW | MEDIUM | MEDIUM |
| Event sourcing/CQRS | LOW | HIGH | LOW | HIGH |
| Datomic | LOW | HIGH | MEDIUM | HIGH |
| ACID/WAL/log-structured | n/a | HIGH | MEDIUM | HIGH |
| Projectional editors (MPS, Hazel) | LOW | LOW | HIGH | MEDIUM |
| Smalltalk image+changes | LOW | MEDIUM | LOW | LOW |
| Patch theory (Darcs/Pijul) | LOW | MEDIUM | LOW | n/a |
| OT/CRDTs | LOW | LOW | LOW | n/a |
| Git (contrast) | HIGH | LOW | LOW | MEDIUM |

- **Unison** — closest living relative for identity: definitions are AST
  hashes, names are metadata bindings; rename (repoint name, no new hash)
  vs edit (new hash, dependents propagated) maps directly onto visible-name
  vs true-name changes, and its `update` + propagation pair maps to the
  atomic operation with cascaded regeneration. Diverges: snapshot-based
  history, text-mediated editing, records resulting state rather than the
  operation.
- **Event sourcing / CQRS** — the strongest operation-log match: command
  (signal message, may fail) vs event (recorded fact, irrevocable); state
  as projection over the log. Diverges: untyped payloads, no content
  addressing, multi-aggregate eventual consistency protos does not need.
- **Datomic** — queryable transaction log as first-class truth, immutable
  snapshots, time travel, ACID. Diverges: allocation-based entity ids,
  generic assert/retract rather than typed structural operations.
- **ACID / write-ahead logs / log-structured storage** — the atomicity
  vocabulary source; log-structured storage (log is primary, state is a
  materialized view) is the exact pattern; protos's log differs from a WAL
  in being permanent (it IS the VCS), which log-structured systems match.
- **Projectional editors (MPS, Hazel)** — the editing-model match: edit
  the tree, text is a projection; Hazel's every-intermediate-state-well-
  typed maps to "it either works and goes through or doesn't." Diverge:
  external VCS, UI-first rather than daemon-first.
- **Smalltalk** — image + append-only changes file (replayable for
  recovery) is the dual-write ancestor; per-method granularity, no
  transactions, no content addressing.
- **Patch theory** — shares "history is a set of operations, not
  snapshots"; its machinery (commutation, conflicts) exists for
  multi-authority distribution, irrelevant under protos's single authority.
- **OT/CRDTs** — vocabulary overlap only; their whole substance is
  concurrent-write reconciliation protos doesn't have.
- **Git** — the contrast: content-addressed but type-blind bytes;
  snapshots with diffs reconstructed after the fact; reflog explicitly not
  the source of truth. Terms to avoid importing: commit, diff, rebase,
  cherry-pick — each drags the wrong mental model.

## Terminology proposals (nothing settled)

Existing vocabulary honored: Signal (transport), Sema (data at rest),
Spirit, Psyche, Capsule (compilation unit), Transformer (Nomos unit);
-os names reserved for the language family (Ethos/Nomos/Logos/Protos/Dotos)
— operational terms are a different stratum and need not end in -os.

**Recommended set (A): Praxis + Mneme, paradigm stays "operational editing".**

- **Praxis** (πρᾶξις, deed, enacted practice) — the single atomic
  operation. Precise: praxis is the *doing* (vs theoria and poiesis);
  the operation is the deed, the changed state is its result. No CS or
  in-system collision; clean in English and French; plural praxeis.
- **Mneme** (μνήμη, memory) — the change log. The log is not merely a
  timeline: it is the memory from which all current state can be
  reconstructed — source-of-truth status that "memory" captures and
  "chronicle" does not. Sits inside Sema without conflict (Sema is data at
  rest broadly; Mneme is specifically the operation record).
- **Operational editing** — the paradigm name, retained: it is the
  psyche's own ruled phrase; a Greek formalization would add ceremony, not
  meaning.

Alternates evaluated: Chronikon (chronicle — accurate but ornate, captures
ordering not truth-status), Ergon (work — names the result, not the doing),
Metabole (withdrawn: collides conceptually with Transformer), transaction
(drags database isolation machinery), patch (drags text-diff model),
operation/log (safe, instantly understood, zero design-language
distinctiveness).

Sentence test for set A: "a Praxis arrives as a signal message, is applied
atomically to the encoded form, and is recorded in the Mneme."
