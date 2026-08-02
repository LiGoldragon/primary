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
