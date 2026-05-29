# Intent block 1157–1175 — forensic recovery attempt

*While recovering the report-45 intent-log removal audit (the rewound
session), a SECOND missing block surfaced: records 1157–1175 (19
consecutive ids) are gone from the live Spirit daemon, beyond the 19
the audit deliberately removed. This report records the recovery
attempt — what sources exist, what was tried, and the verdict — plus
a process-gap finding. Triggered by the psyche's question 2026-05-29:
"do we keep old version databases? maybe you can read it with an
older spirit version."*

## The missing-id landscape

The live production daemon is `spirit -> spirit-v0.3.0`, database
`~/.local/state/persona-spirit/v0.3.0/persona-spirit.redb`. Live
record ids run 1–1179. Missing ids in that range fall in three
classes:

| Class | Ids | Status |
|---|---|---|
| Audit removals (report 45, psyche-approved) | 109, 550, 736, 905, 913, 1005, 1009, 1024, 1048, 1055, 1056, 1058, 1061, 1065, 1073, 1074, 1075, 1088, 1091 | Expected; **tombstoned** in report 45 appendix |
| Pre-existing gaps | 1098, 1099 | Removed before the audit; noted in report 45 |
| **Unexplained block** | **1157–1175** | **No tombstone; this report's subject** |

The block was born and removed today. Its live neighbours bound it
tightly: record 1156 stamped `2026-05-29 06:58:59`, record 1176
stamped `2026-05-29 07:00:57` — a ~2-minute window.

## What the block was — bounded by its surviving siblings

Records 1153–1156 and 1176–1179 — the live records flanking the gap —
are **all** of one family: `Decision`/`Constraint` records topic-tagged
`[schema nota …]`, every description opening "Gap-fill from forwarded
designer exchange…". They are the intent-capture of a forwarded
designer exchange on the NOTA/Schema type-vocabulary split. The
deleted 1157–1175 sit inside that contiguous burst, so they are the
same family: intermediate gap-fill captures from the same forwarded
exchange.

The substance of that exchange is preserved independently of the
removed records:

- Surviving siblings 1153–1156, 1176–1179 (the kept gap-fills).
- `reports/designer/421-nota.md`, `422-schema.md`,
  `423-signal-nexus-sema.md` — the consolidated NOTA/Schema design
  spec.
- Bead `primary-8vzk` ("Implement consolidated NOTA/Schema spec
  (designer reports 421/422/423)") — the build program.

## Recovery avenues — all closed

### 1. Old version databases — kept, but cannot contain these records

Spirit is deployed side-by-side. On disk: `spirit-v0.1.0`,
`spirit-v0.1.1`, `spirit-v0.2.0`, `spirit-v0.3.0` (production), plus a
`spirit-next` pilot — each with its **own segregated** redb under
`~/.local/state/persona-spirit/<version>/`, plus several
cutover/migration backups dated **2026-05-22 … 2026-05-25**.

So yes, we keep old databases — but they cannot hold 1157–1175. The
databases never share files; at each version cutover records migrate
**forward** (old → new), leaving older databases frozen subsets ending
at their cutover time. Records 1157–1175 were born today under v0.3.0;
they never existed in any older database. Reading with an older
`spirit-vX` binary queries only that version's frozen db.

### 2. Filesystem snapshots — none

Home is `ext4` on `/dev/nvme0n1p2`. No btrfs/zfs/timeshift snapshot
mechanism. No filesystem-level copy of the v0.3.0 db from before the
removal exists. There is no today-dated backup of the v0.3.0 db
anywhere under the state directory.

### 3. Freed-page forensics — method works, but pages overwritten

redb is copy-on-write, so a removed record's bytes can linger in freed
pages until reused. The technique is viable: on a read-only copy of
the live db, `strings` surfaces record descriptions as readable UTF-8
(verified against a known-live record). But subtraction of the live
record set from the raw strings yields **no uniquely-recoverable
deleted description** — every substantial description in the file maps
to a live record.

Confirmed why: the five most distinctive phrases from the report-45
removals (e.g. record 109's "does not use feature branches by
default", record 550's "redb file is COPYABLE WHILE") are **entirely
absent** from the raw bytes. The ~74 records added since this morning's
removals (the db grew to id 1179) have **overwritten the freed
pages**. The same mechanism erased 1157–1175. A type-aware (rkyv)
redb scanner would read the same overwritten bytes — it cannot do
better.

*Method note: all forensics ran on `/tmp/spirit-v030-forensic.redb`, a
read-only copy. The live daemon and its database were never written.*

## Verdict

Records 1157–1175 are **not byte-recoverable** — no backup, no
snapshot, freed pages overwritten. But the block was a burst of
forwarded-designer-exchange gap-fill captures that closely restated
intent already held live (their text overlaps the surviving siblings),
and the design substance is preserved in records 1153–1156 / 1176–1179,
reports 421–423, and bead `primary-8vzk`. The most consistent reading
is **intentional dedup of an over-capture** — an agent logging ~27
gap-fill records from a forwarded exchange, then removing the ~19
duplicative ones and keeping the 8 genuinely-new. That matches the
forwarded-prompt discipline in `AGENTS.md` ("don't blindly duplicate")
and the just-granted removal capacity (record 1103). No unique design
intent appears to have been lost.

Uncertainty held honestly: there is no record of **who** removed the
block or that it was deliberate. The duplicative-cleanup reading is
inferred from the surviving evidence, not proven.

## Process-gap finding — tombstone before remove

Report 45 captured the full text + provenance of its 19 removals into a
tombstone appendix **before** removing them — which is exactly why
those 19 remain reconstructable while 1157–1175 do not. Whoever removed
1157–1175 did **not** tombstone them, and redb's page reuse then made
the loss permanent within hours.

Recommendation: make **tombstone-before-remove** a mandatory step of
intent removal, not an ad-hoc courtesy. Before any `spirit "(Remove
N)"`, capture `(Observe (RecordIdentifiers ((Exact N) WithProvenance)))`
into the removing agent's report. This belongs in
`skills/intent-maintenance.md` alongside the removal-capacity note that
record 1103 introduced. (Proposal — awaiting psyche affirmation before
it becomes discipline.)

## See also

- `reports/system-designer/45-intent-log-removal-audit-2026-05-28.md`
  — the audit being recovered; its appendix is the model tombstone.
- Record 1103 (removal capacity, psyche-authorized, conservative).
- `skills/spirit-cli.md` §"Deployment slots" — the side-by-side
  segregated-database model that rules out older-version recovery.
- `skills/intent-maintenance.md` — where tombstone-before-remove
  should land.
- Bead `primary-8vzk` + `reports/designer/421-423` — where the
  forwarded-exchange substance is consolidated.
