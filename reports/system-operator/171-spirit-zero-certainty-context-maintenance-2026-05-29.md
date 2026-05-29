# Spirit Zero certainty — operator context-maintenance audit

## Scope

This report audits my prior Spirit removal-candidate work and
agglomerates the relevant reports around it. It focuses on the
`Magnitude::Zero` implementation, the intent-removal reports, the live
production surface, and the design gap between "query candidates" and a
complete recoverable-removal workflow.

Primary predecessor reports:

- `reports/system-operator/168-spirit-signal-surface-bad-pattern-audit-2026-05-28.md`
- `reports/system-designer/45-intent-log-removal-audit-2026-05-28.md`
- `reports/system-designer/46-intent-block-1157-1175-forensic-recovery-2026-05-29.md`
- `reports/system-designer/47-sema-redb-deletion-durability-2026-05-29.md`
- `reports/system-designer/48-intent-removal-implementation-audit-and-consolidation-2026-05-29.md`

## Current finding

The implementation direction is right, but the production system is not
yet at the intended design state.

What exists in repositories:

- `signal-sema` main has `Magnitude::Zero`.
- `signal-persona-spirit` main has `CertaintySelection` with
  `Exact`, `AtMost`, and `AtLeast`.
- `persona-spirit` main can filter observed records by certainty.
- tests passed in all three repos during the implementation pass.

What is live in the installed local Spirit CLI:

```sh
spirit "(Observe (Records ((Any []) None (Exact Zero) SummaryOnly)))"
```

returns:

```text
invalid request text: unknown variant `Zero` for enum `Magnitude`
```

while:

```sh
spirit "(Observe (Records ((Any []) None (AtMost Low) SummaryOnly)))"
```

does work. So the installed production binary has the certainty-filter
shape but not the `Zero` variant. Any document or skill saying production
Spirit currently supports `(Exact Zero)` is ahead of the deployed state.

## Intent spine

The durable design arc is:

1. Spirit gained hard removal capability (`Remove`) after records 1093,
   1103, and 1189.
2. The 1157-1175 incident proved hard removal is unsafe without a
   recoverable staging step: redb copy-on-write page reuse makes deleted
   records unrecoverable after later writes.
3. Records 1190-1192 introduced removal-candidate review: lower a
   record's certainty to the floor, review the floor set, then hard
   remove only after review.
4. Records 1212 and 1213 proposed `Option<Magnitude>` / `None`.
5. Record 1214 superseded that: use a shared, policy-neutral
   `Magnitude::Zero` bottom rung, not `Option::None`.

Report 48 correctly consolidates much of this, but it repeatedly names
record `1215`. The live Spirit query shows the actual `Zero` decision is
record `1214`. That number mismatch has already leaked into
`skills/intent-maintenance.md`; it should be corrected when the docs are
edited next.

## Design fit

`Zero` is the right conceptual move because `Magnitude` is shared
vocabulary, not Spirit-only policy. A field name supplies the dimension:
`certainty: Magnitude` in Spirit, `priority: Magnitude` in another
component, `severity: Magnitude` elsewhere. `Zero` means the bottom rung
of that dimension. Spirit interprets `certainty == Zero` as "removal
candidate"; another component can interpret the same rung differently.

My implementation deliberately deviated from the initial "declare Zero
first and derive Ord" design. `signal-sema` stores `Zero = 7` physically
last and implements semantic ordering manually, so existing archived
rkyv discriminants for `Minimum..Maximum` remain stable. That correction
is load-bearing: inserting a new enum variant at the front would have
silently reinterpreted persisted data.

The broader rule should be permanent: persisted rkyv enums must not
shift existing discriminants. Append new variants and express semantic
ordering separately.

## What landed

Repository state observed in this audit:

| Repository | Commit | State |
|---|---:|---|
| `signal-sema` | `ee61fefb` | `Magnitude::Zero`, manual semantic ordering, storage-discriminant tests |
| `signal-persona-spirit` | `ee49f410` | certainty selection in `RecordQuery`, `removal_candidates()` = `Exact(Zero)` |
| `persona-spirit` | `754a610d` | boundary behavior for `Exact Zero` and `AtMost Low` in repo tests |
| `primary` | `71e2983a` | designer consolidation report 48 and updated removal docs |

Verification that was previously run:

- `cargo test` in `signal-sema`
- `cargo test` in `signal-persona-spirit`
- `cargo test` in `persona-spirit`
- `nix flake metadata --json >/dev/null` in `CriomOS` during the earlier
  repin attempt

Live verification run in this audit:

- `spirit "(Observe (Records ((Any []) None (Exact Zero) SummaryOnly)))"`
  fails with unknown `Zero`
- `spirit "(Observe (Records ((Any []) None (AtMost Low) SummaryOnly)))"`
  succeeds

## Gaps

### 1. Zero is not deployed

The user profile still runs a Spirit binary that does not know
`Magnitude::Zero`. The earlier repo implementation cannot be treated as
production behavior until the Home/CriomOS pins are updated and the
profile is activated.

This also means `skills/spirit-cli.md` currently overstates the live
production query shape by documenting `(Exact Zero)` as available.

### 2. The nominate/mutate path is missing

The design is two-phase:

1. nominate by lowering existing record certainty to `Zero`;
2. review `certainty == Zero`;
3. hard-remove after tombstone capture.

The implementation covers step 2 only. `persona-spirit` still has create
and hard-remove surfaces, but no operation that mutates an existing
record's certainty to `Zero`. Until that exists, removalCandidates is a
query shape without a normal way to populate candidates.

The open design choice is whether nomination is a dedicated operation
such as `NominateRemoval`, or a general owner-channel certainty mutation
such as `SetCertainty(record, Zero)`.

### 3. Hard removal has no guardrail

`Remove` remains a direct hard delete. The intended discipline is:
observe with provenance, paste the tombstone into a report, then remove.
That is now documented in `skills/intent-maintenance.md`, but not
enforced by Spirit. A future owner-policy surface should make accidental
hard deletion harder, especially before `Zero` nomination is live.

### 4. Report and skill references use the wrong record number

Report 48 and `skills/intent-maintenance.md` refer to record `1215` for
the Zero decision. The actual Spirit record is `1214`:

```text
1214 [spirit certainty magnitude] Decision
Spirit removal-candidate certainty should use a shared neutral Magnitude
bottom rung named Zero, not Option None...
```

This is small but dangerous because record numbers are used as exact
locators in later reports.

### 5. `signal-sema` has an architecture/dependency mismatch

`signal-sema/ARCHITECTURE.md` says the crate does not depend on
`signal-frame`, but `Cargo.toml` currently does:

```toml
signal-frame = { git = "https://github.com/LiGoldragon/signal-frame.git", branch = "operator-full-schema-spirit-2026-05-26" }
```

That mismatch matters because `signal-persona-spirit` now locks two
different `signal-frame` and `schema` branches at once: its direct
dependencies use `main`, while `signal-sema` pulls the operator feature
branch. This is not a good long-term substrate shape.

### 6. Downstream consumers were not swept

The immediate Spirit path was updated, but other `Magnitude` consumers
were not audited in this pass. Rust will catch exhaustive matches after
repins, but that only helps when each consumer updates. The wider schema
stack still needs a deliberate "what does Zero mean here?" pass.

### 7. Report 168 is adjacent, not retired

The bad-surface audit in report 168 covers `SummaryOnly`,
`DescriptionOnly`, wrapper record shape, and observation naming. It is
the same Spirit observation surface family, but not the same lifecycle
problem. It should stay active until the observation output/schema shape
is cleaned up.

## Context-maintenance disposition

| Report | Disposition |
|---|---|
| `reports/system-designer/45-intent-log-removal-audit-2026-05-28.md` | Keep as historical tombstone source; report 48 copied the appendix, so normal readers can start at 48/171. |
| `reports/system-designer/46-intent-block-1157-1175-forensic-recovery-2026-05-29.md` | Retired into report 48 for ordinary context; keep for forensic detail. |
| `reports/system-designer/47-sema-redb-deletion-durability-2026-05-29.md` | Retired into report 48 for ordinary context; still useful for the original reasoning. |
| `reports/system-designer/48-intent-removal-implementation-audit-and-consolidation-2026-05-29.md` | Current designer consolidation, but needs correction: record `1215` should be `1214`, and live deployment is still absent. |
| `reports/system-operator/168-spirit-signal-surface-bad-pattern-audit-2026-05-28.md` | Keep active as a separate observation-surface cleanup report. |
| `reports/system-operator/171-spirit-zero-certainty-context-maintenance-2026-05-29.md` | This report is the operator-side fresh status: implementation, live gap, dependency gap, and next work. |

## Next work

1. Repin/deploy the Spirit stack so `(Exact Zero)` is actually live.
2. Correct `1215` to `1214` in report 48 and
   `skills/intent-maintenance.md`.
3. Add the nomination path: preferably owner-policy signal, either
   dedicated `NominateRemoval` or general `SetCertainty`.
4. Decide whether `Remove` should require `certainty == Zero` or at
   least emit a stronger guard/confirmation path.
5. Fix the `signal-sema` dependency mismatch and eliminate the duplicate
   `signal-frame`/`schema` lock branches.
6. Manifest the rkyv enum-discriminant stability rule into the relevant
   architecture files.
7. Sweep downstream `Magnitude` consumers after repinning.

## Operator assessment

The core implementation choice is correct: `Zero` should be a shared
neutral bottom rung, and physical-discriminant stability matters more
than derived-order convenience. The project is not yet complete because
the recoverable-removal workflow needs an actual mutation/nomination
operation and a deployment pass. Right now the repositories contain the
query-side mechanics, but the live system still behaves like the older
hard-removal world.
