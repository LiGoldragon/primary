# Intent removal — implementation audit and topic consolidation

> **Status update 2026-05-30:** GAP 1 (the nominate write path) is
> **closed** by production Spirit deploying `(ChangeCertainty (N Magnitude))`
> today. Witness commits: `signal-persona-spirit 1bb22635`,
> `persona-spirit c5a3eb9b`, `CriomOS-home cc6bb3d2`, `CriomOS 1cf0b747`,
> primary `skills 180e6f2b`. The `removalCandidates` query
> (`(Exact Zero)`) is now backed by an active soft-delete buffer —
> a record can be nominated to `Zero` (recoverable) and only later
> hard-removed. GAP 2 (sema discriminant-stability rule) and GAP 3
> (only Spirit interprets Zero) remain open. This report is kept
> under the `skills/context-maintenance.md` §3a design-rationale
> guard — its 19-record tombstone appendix is the sole copy outside
> git history, and the Zero-vs-`Option<None>` alternative weighing
> remains load-bearing rationale.

*Consolidates the intent-removal arc — reports 45 (removal audit + the
19-record tombstone), 46 (the 1157–1175 forensic dead-end), and 47
(redb deletion durability + the removalCandidates design) — and audits
the operator's `Magnitude::Zero` / removalCandidates implementation
against design intent. This report supersedes 45/46/47, which retire
into it; their permanent substance already lives in `sema`
ARCHITECTURE §"Deletion durability", `skills/intent-maintenance.md`
§"Removing a record", and Spirit records 1093/1103/1189/1191/1192/1215.
Per psyche 2026-05-29.*

## Topic arc

Record **1093** asked for explicit removal capability; **1103/1189**
granted it and confirmed it live. Report 45 audited the log and removed
19 psyche-approved records — tombstoned first. A separate block,
**1157–1175**, was removed *without* a tombstone and proved
unrecoverable (report 46): redb is copy-on-write and the freed pages
were overwritten within hours. Report 47 generalized that into the
deletion-durability finding and proposed a recoverable soft-delete —
mark a removal *candidate* by lowering its certainty to a new floor —
captured as records **1191** (filter by certainty), **1192**
(soft-removal mechanism), **1215** (the floor is a `Zero` variant, not
`None`/`Option`). The operator then implemented `Zero` and the candidate
query.

## Implementation audit

Operator commits: `signal-sema ee61fefb`, `signal-persona-spirit
ee49f410`, `persona-spirit 754a610d`, `CriomOS affd894c`, `primary
f73ca004`. Verified: `cargo test` green in signal-sema /
signal-persona-spirit / persona-spirit; `nix flake metadata` green.

### signal-sema — `Magnitude::Zero`: correct, and corrects the design

`magnitude.rs` adds `Zero = 7` **physically last** under `#[repr(u8)]`,
so the original seven keep discriminants 0–6 and **archived rkyv
records stay valid**. The derived `Ord`/`PartialOrd` were removed and
replaced with a manual `order_rank` (`Zero => 0`, then `Minimum`…
`Maximum` 1…7), giving the semantic order `Zero < Minimum < … <
Maximum`. The order is total and `Eq`-consistent. `as_record_head` /
`from_record_head` carry the `Zero` NOTA token.

This **deviates from the design** (record 1215 / report 47 said "declare
`Zero` first so derived `Ord` places it below `Minimum`") — and the
deviation is correct. Declaring first would renumber the rkyv
discriminants (`Minimum` 0→1, …) and silently reinterpret every
persisted record (`Minimum`'s byte 0 would decode as `Zero` — i.e.
every existing intent record would read as a removal candidate). The
operator caught a real corruption flaw in the design intent. See GAP 2.

### signal-persona-spirit — certainty filter: done (record 1191)

`CertaintySelection { Any, Exact(c), AtMost(c), AtLeast(c) }` with a
`removal_candidates()` constructor = `Exact(Magnitude::Zero)` and a
`matches()` using the new ordering. `RecordQuery` gains
`certainty_selection`. This is record 1191, cleanly delivered.

### persona-spirit — query side done, nominate side missing

The daemon's `matches_certainty` applies the selection, so
`removalCandidates` queries resolve end-to-end. New records get
`Minimum` (classifier fallback). But `SpiritStore`'s write API is
`assert_entry` (create) and `remove_entry` (hard `Retract`) only — there
is **no `mutate`/`set_certainty`**, and neither contract exposes a
`Mutate`/`Nominate`/`SetCertainty` operation. See GAP 1.

### Deployment — built, not live

The whole stack compiles and tests green, but it is **not deployed**:
CriomOS-home is locked by cloud-designer, so the user profile was not
repinned. The installed `spirit` remains pre-`Zero`; in production,
removal is still hard-only and no `Zero` rung exists yet.

## Gaps in design intent

### GAP 1 — the nominate path is missing; removalCandidates is inert (load-bearing)

The design (records 1192/1215, report 47) is a two-phase soft process:
*nominate* a candidate by lowering its certainty to `Zero` (recoverable,
stays in the store) → *review* the candidate set → *hard-remove* only
the confirmed ones. The implementation built the floor (`Zero`), the
query (`Exact(Zero)`), and the filter (`CertaintySelection`) — but **not
the write path that lowers an existing record to `Zero`.** The store can
only assert and hard-`Retract`; certainty is fixed at capture.

Consequence: no record can ever *become* a candidate (the classifier
assigns `Minimum` or higher; nothing sets `Zero`), so
`removal_candidates()` always returns empty. The recoverable soft-delete
buffer — the entire reason for the `Zero` design — is not usable. Only
the irreversible hard `(Remove N)` is live. This is plausibly a
deliberate phased landing (it is item 4 of bead `primary-m89k`), but the
operator's "Implemented and pushed" framing does not flag it, so it is
called out here: the lifecycle is **query-ready, not nominate-ready**.

Still-open sub-decisions from report 47 that the nominate path must
settle: the operation's **channel** (owner-only vs ordinary) and whether
nomination is a general certainty-`Mutate` or a dedicated `Nominate` op.

### GAP 2 — "declare first" was archive-unsafe; the corrected rule is durable

Record 1215 / report 47 specified the `Zero`-declared-first / derived-Ord
shape, which is archive-unsafe (above). The operator's append-at-end +
manual-order approach is the correct pattern, and it generalizes to a
**durable constraint**: a derived-`Archive` (rkyv) enum that has
persisted data must never reorder or insert variants in a way that
shifts existing discriminants — append new variants at the end and
express semantic order separately (manual `Ord`/`order_rank`). This
belongs in `sema` ARCHITECTURE (e.g. a "Schema evolution / discriminant
stability" note); recommend the operator land it there since they own
the repo and the magnitude.rs change.

### GAP 3 — only spirit interprets `Zero` (minor, expected)

The other Magnitude consumers (`signal-mind`, `mind`, `schema-next`,
`spirit-next`) took the compiler-guided variant addition but do not yet
*interpret* `Zero` (e.g. mind as "forgettable", sema as "no signal").
That is consistent with the per-component-consumption intent (record
#11/1191), so it is acceptable — but the "universal rung across
spirit/mind/sema" framing is aspirational until those consumers act on
it.

## Greater picture — what this fits into

- **The schema-derived Spirit migration.** `Magnitude` is the shared,
  payload-free vocabulary across the persona stack (NOTA → Schema → sema
  → Spirit/mind). `Zero` is its first cross-component "bottom" rung; the
  removalCandidates work is the first consumer to use it semantically.
- **The removal lifecycle.** Hard `(Remove N)` is irreversible (redb
  copy-on-write; reports 46/47). The intended safety architecture is:
  `Zero` soft-delete as the recoverable buffer, plus tombstone-before-
  remove (`skills/intent-maintenance.md`) guarding the final hard delete.
  **Currently only the hard delete + the tombstone discipline are
  live**; the soft buffer is not (GAP 1). So the system is *less* safe
  than the design intends until the nominate path lands.
- **Deployment gating.** The entire `Zero` stack is built but blocked
  behind the CriomOS-home lock (cloud-designer). Production intent
  removal remains hard-only with no `Zero` until that lock moves and the
  profile is repinned.

## Forensic finding — 1157–1175 (carried from report 46)

Nineteen records — a "Gap-fill from forwarded designer exchange" burst,
same family as the surviving siblings 1153–1156 / 1176–1179 — were
removed without a tombstone and are **not byte-recoverable**: redb's
freed pages were overwritten within hours by ~74 later writes (confirmed
by forensic `strings`/byte scan of a read-only copy; even the distinct
text of the report-45 removals is gone). Old version databases are
segregated and frozen pre-today; the filesystem is ext4 with no
snapshots. The substance survives in the siblings, `reports/designer/421-423`,
and bead `primary-8vzk`. **Open question (unresolved):** who removed the
block and whether it was deliberate. Most-consistent reading: intentional
dedup of an over-captured forwarded-exchange burst — but inferred, not
proven. This loss is what motivated the tombstone-before-remove rule.

## Design rationale preserved (carried from report 47, per context-maintenance §3a)

The model sub-decision weighed **(A)** a new bottom variant on
`Magnitude` vs **(B)** `certainty: Option<Magnitude>` with `None` =
candidate. Chosen: **(A)**, named `Zero` (record 1215). Rationale: keeps
the shared `Magnitude` vocabulary bare and payload-free (no `Option`
ripple across every consumer); a universal zero rung reads coherently as
spirit-removal-candidate / mind-forgettable / sema-no-signal; rkyv cost
is unchanged. **(B)** would have won only if "absence of confidence"
were a genuinely different axis than strength, or if forcing every
consumer to handle absence explicitly were wanted — neither held. (The
implementation realized (A) with append-at-end + manual ordering, not
the declare-first form the decision originally imagined — GAP 2.)

## Context-maintenance disposition

Reports 45, 46, 47 **retire** into this report. Landing evidence (per
`skills/context-maintenance.md` §2 staleness gate):

| Retired | Substance | Permanent / successor home |
|---|---|---|
| 45 | redb-COW finding | `sema`/`sema-engine`/`persona-spirit` ARCHITECTURE §"Deletion durability" (committed) |
| 45 | tombstone discipline | `skills/intent-maintenance.md` §"Removing a record — tombstone first" |
| 45 | the 19 removed records | **Appendix below** (verbatim — the only copy outside git history) |
| 46 | 1157–1175 forensic verdict + open question | §"Forensic finding" above |
| 47 | removalCandidates design + (A)/(B) rationale | records 1191/1192/1215; §"Design rationale preserved"; bead `primary-m89k` |
| 47 | deletion durability | `sema` ARCHITECTURE §"Deletion durability" |

This report is the canonical intent-removal surface. It retires when the
removalCandidates implementation completes (the nominate path) and a
successor records the live, deployed state.

## Appendix — tombstone of the 19 records removed 2026-05-29 (carried verbatim from report 45)

*Removal loses the record and its provenance from the active store.
This appendix is the surviving record of what was removed, captured via
`(Observe (RecordIdentifiers ((Exact N) WithProvenance)))` before removal.*

- **109** (Decision, Maximum, 2026-05-22) [workspace] — "The workspace does not use feature branches by default. Merges go directly to main. Version tracking happens via semver tags… Branches are exceptional…" — *superseded by 515 (worktree workflow, an AGENTS.md hard override).*
- **550** (Clarification, Maximum, 2026-05-25) [redb-copyable-while-open] — "The redb file is COPYABLE WHILE the writing daemon holds it open… cutover works AS DESIGNED without any drain-the-writer prerequisite…" — *corrected as premature/unsafe by 568.*
- **736** (Decision, Maximum, 2026-05-26) [workspace] — "Intent log audit policy: agents may FLAG… but never delete or supersede unilaterally. Only the psyche supersedes intent…" — *superseded by 1103 (removal capacity).*
- **905** (Decision, Maximum, 2026-05-27) [criomos lojix horizon] — "Audit production CriomOS changes that have not been ported to the next Lojix and Horizon rewrite stack, create a report, and use the findings to guide the port." — *working order; done.*
- **913** (Decision, High, 2026-05-27) [system-operator reports criomos nota-schema-next] — "Audit and critique the production-to-lean CriomOS reconciliation report after refreshing the latest NOTA/schema-next design context." — *working order; done.*
- **1005** (Constraint, Maximum, 2026-05-27) [schema-stack e2e-tests audit truth-tests] — "Audit the schema-at-heart prototype and report whether the tests genuinely prove the concept by building real packages through Nix…" — *working order; durable principle is 1006 (kept).*
- **1009** (Decision, High, 2026-05-28) [schema-next cargo cross-crate-import nix] — "Research and prototype whether schema-next can reuse Cargo crate-resolution to find schema libraries by the single-colon module naming…" — *working order; report 39 (proven).*
- **1024** (Decision, High, 2026-05-28) [horizon lojix schema-next nota-next port feasibility] — "Audit the current state of the new-logic horizon/lojix rewrite and assess the feasibility of porting schema-next plus nota-next to be the MAIN driver…" — *working order; report 40 (feasibility = YES).*
- **1048** (Decision, High, 2026-05-28) [horizon schema-pipeline concept] — "Build a working concept prototype that generates all needed Horizon datatypes from a PURE schema, demonstrated step-by-step end to end…" — *working order; report 41 + horizon-next (built).*
- **1055** (Constraint, High, 2026-05-28) [horizon lojix criomos audit implementation] — "Psyche asks this lane to review report 42, research the broader intent of the lojix/horizon/CriomOS reworking, audit the implementation, become expert in the question, and write an independent report." — *working order; report 43.*
- **1056** (Decision, High, 2026-05-28) [horizon lojix criomos implementation] — "Psyche asks this lane to fix the concrete issue shown in the attached screenshot as part of the audit/fix pass." — *working order; the ConnectionRefused fix.*
- **1058** (Decision, High, 2026-05-28) [lojix horizon criomos audit reports] — "Psyche asks this lane to review report 42, research the full intent behind the lojix/horizon/CriomOS reworking, audit the implementation, and write an independent report." — *near-duplicate of 1055; working order.*
- **1061** (Decision, High, 2026-05-28) [horizon-next finish subagent schema-deep] — "Dispatch a subagent to FINISH the horizon-next schema-driven Horizon concept completely - create and push the remote, land the nix flake check hermetic witness, and close the carried-forward divergences from report 42…" — *working order; done (commit 1b64d1b).*
- **1065** (Decision, High, 2026-05-28) [spirit signal surface bad-pattern audit] — "Audit production Spirit for bad patterns similar to the misleading DescriptionOnly mode and the nested RecordsObserved vector wrapper…" — *working order; report 43 / system-operator/168.*
- **1073** (Decision, High, 2026-05-28) [context-maintenance skills subagent] — "Psyche asks this lane to create or update skills/context-maintenance.md from report 44, and to use a subagent for the work." — *working order; the skill exists.*
- **1074** (Decision, Maximum, 2026-05-28) [context-maintenance skills] — "Create a workspace skills/context-maintenance.md skill from the cross-lane context maintenance report, using a subagent…" — *duplicate of 1073.*
- **1075** (Decision, High, 2026-05-28) [context maintenance with subagent] — "Run the context-maintenance discipline using a subagent, grounded in report 44, while preserving the current in-progress production Spirit work state…" — *duplicate of 1073/1074.*
- **1088** (Decision, High, 2026-05-28) [schema schema-language language-design production-test report] — "Create a full schema-language design report from the current clarified grammar… Then test the design through the production Spirit path…" — *adjudicated a capture-error by 1090.*
- **1091** (Correction, High, 2026-05-28) [intent-maintenance intent-capture append-only provenance] — "Intent records are append-only provenance. A later Spirit record cannot cancel delete or erase an earlier Spirit record…" — *superseded by 1103 (removal capacity).*

## See also

- `sema` ARCHITECTURE §"Deletion durability"; `skills/intent-maintenance.md`
  §"Removing a record — tombstone first"; `skills/intent-log.md`
  §"When a working order slips in anyway".
- Spirit records 1093/1103/1189 (removal capacity), 1191/1192/1215
  (removalCandidates design).
- bead `primary-m89k` (the build program; GAP 1 is its item 4).
