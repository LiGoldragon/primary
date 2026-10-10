# Database Evolution Engine — 2026-08-02

Ruling from the psyche-interaction session presenting the high-level
understanding report
(`reports/ProtosEngineHighLevelUnderstanding-2026-08-02.md`). The psyche's
original statement of this concept survived in no transcript; the manager
reconstructed it from surviving pieces and presented the reconstruction for
review.

Agent text answered: the manager's reconstruction — the database-focused
part of Ethos (Schema/Family/SEMA lineage) is just another file kind, so a
database schema lives as encoded form in a slot under the change log; two
schema versions diff structurally and exactly, renames invisible by
construction because encoded names persist; the migration (typed fold, old
layout to new) is derived from that diff rather than authored — ending with
two confirmation questions: (a) is the diff input the Ethos-encoded schema
itself rather than storage-layer snapshots, and (b) are schema edit and data
evolution one atomic operation rather than a separately triggered migration
step?

Psyche ruling [psyche-verbatim]: "exactly; the edit operation of the
database schema automatically gives us the database migration logic. so the
database editing operation produces the migration code, which could either
be compiled in the next version, or compiled in a db migration executable"

## Seated meaning

- The reconstruction is **confirmed**: the diff input is the Ethos-encoded
  database schema itself; derivation, not authoring, is the migration
  model; encoded-name persistence makes renames migration-free by
  construction.
- **Sharpening beyond the reconstruction**: the schema-edit operation does
  not merely apply an internal migration plan — it **produces the migration
  code as an output artifact**. Deriving that code is part of the atomic
  operation's cascade.
- **Two sanctioned compilation vehicles** for the produced migration code:
  1. compiled into the next version of the program (the next version
     carries the old-to-new fold), or
  2. compiled into a standalone database migration executable.
- Precision on atomicity [agent-inference, consistent with the ruling]: the
  atomic operation covers the schema edit plus the production of the
  migration logic. Applying that logic to a particular live database is a
  deployment act through one of the two vehicles, not necessarily inside
  the editing operation itself.
- Continuity with seated SEMA universals [agent-inference]: the produced
  code is the derived typed fold — the receipt-graph `From` lineage of the
  frozen `schema-language` donor generalized into the engine's change log,
  executing under the existing one-way-fold, reject-not-coerce shape.

## Appended 2026-08-02, later same session: two routes into a schema edit

Agent text answered: the manager's restated confirmation questions — (a) is
the diff input the Ethos-encoded schema itself, (b) are schema edit and
data evolution one atomic operation — and the seated flow in which the diff
of two encoded schema versions produces the migration.

Psyche ruling [psyche-verbatim]: "yes, sorry; I think those are two routes;
if we upgrate the code by editing text ethos, then we derive the edit
operation from diffing the two (possibly aided by an LLM if there is
ambiguity), but it is that atomic edit operation which yields the database
update logic"

Seated meaning:

- There are **two routes** into a schema change. Native operational route:
  the edit arrives as an atomic operation through the operation interface.
  Textual bootstrap route: the edit arrives as edited Ethos text, and the
  engine **derives the edit operation** by diffing the old and new encoded
  forms, LLM-aided where the diff alone is ambiguous.
- The diff is a means of recovering the operation, not a parallel migration
  mechanism. In both routes it is the **atomic edit operation** that yields
  the database update logic (the migration code, per the vehicles ruling
  above).
- [agent-inference, consistent with the ruling] The ambiguity the LLM
  resolves is exactly the class the operational route never has: whether a
  textual change is a rename of an existing slot or a removal plus a new
  thing — the operational route names the slot it edits.

## Appended 2026-08-02: retired names out of definitions

Agent text answered: this entry's own opening phrase "the database-focused
part of Ethos (Schema/Family/SEMA lineage)" and the manager's chat defense
of keeping the ancestor name in the lineage framing.

Psyche challenge [psyche-verbatim]: "is the stuff in the parenthesis
beneficial? what is 'Family' anyway?" and then "why are you trying to keep
the schema name alive?"

Seated: retired names — the ancestor language's name and the retired
`Family` construct — do not appear in present-tense definitions. The
database-focused part of Ethos is defined by what it declares: record
types, tables, keys, feeding SEMA. Retired names survive only inside
verbatim quotes and explicitly historical evidence. This entry's opening
parenthetical is superseded accordingly; the report's section 6.1 has been
rewritten to match.
