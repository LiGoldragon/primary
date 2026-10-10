---
title: 63 — Sema-engine boundary conformance audit (who bypasses the database interface?)
role: system-designer
variant: Psyche
date: 2026-06-04
topics: [sema-engine, database, boundary, redb, conformance, component-daemon, dot-sema, architecture]
description: |
  Answers the psyche's question — is sema-engine intended as THE interface to the
  database, and have agents misunderstood that role? Triggered by finding the new
  schema-derived spirit opens redb directly in its daemon. Confirms the intended
  role (sema-engine is the exclusive database boundary; no daemon makes raw redb
  calls — Spirit 2563), then audits every LiGoldragon component for direct redb
  use versus sema-engine use. Finding: two cohorts along a clear fault line — the
  core Persona stack plus production Spirit go through sema-engine (redb 4); a
  second cohort (the new spirit, schema-next, chroma, orchestrator) bypasses it
  with raw redb (redb 2.x). The forward-to-production new spirit is in the bypass
  cohort. Records the .sema file-type decision (Spirit 2564) and the remediation.
---

# 63 — Sema-engine boundary conformance audit

Kind: psyche (architectural conformance audit answering a direct psyche question)
Topics: sema-engine, database, boundary, redb, conformance, dot-sema
Date: 2026-06-04

## Intent Anchors

[Sema-engine is the exclusive interface to the database — no component daemon may make direct redb calls; all durable database work goes through sema-engine, which owns the redb interaction. A daemon that opens redb and runs its own transactions directly is wrong, even as a pilot.] (Spirit 2563 Correction High)

[Component databases use a .sema file extension instead of .redb, hiding redb behind our own .sema file type so the file name states it is specifically a sema-redb database.] (Spirit 2564 Decision High)

[sema opens redb files and reads/writes typed rkyv tables; sema-engine executes signal-sema database operations over registered record families; component daemons own actors, sockets, authorization, domain validation, and their databases — through the engine.] (sema-engine ARCHITECTURE)

[Each component that needs durable state owns its own redb and its own engine/kernel handle; there is no shared sema daemon, no generic store component.] (active-repositories Truth Pin)

[SEMA means database work — the file extension may become .sema instead of .redb so the file name states its architectural role.] (Spirit 1007 Maximum)

## 1. The question

You asked: is sema-engine intended as THE interface to the database, and
have agents misunderstood that role? — after finding the new schema-derived
spirit opens a redb file and runs its own transactions inside its daemon.

## 2. Yes — sema-engine is the intended exclusive database boundary

This is not ambiguous in the existing intent. Three surfaces already say it:

- **sema-engine's own ARCHITECTURE:** sema opens redb and owns the rkyv
  tables; sema-engine executes database operations over registered record
  families; component daemons own actors, sockets, validation, and their
  databases — *through the engine*. The component's relationship to storage is
  `register_table` + `assert`/`mutate`/`retract`/`match`/`commit`, never raw
  redb.
- **The active-repositories Truth Pin:** each stateful component owns its redb
  via its *engine/kernel handle* — i.e., through sema-engine, not by hand.
- **Now Spirit 2563** makes it a hard rule: no daemon makes direct redb calls;
  a daemon that does is a fake of the intended architecture.

So a component daemon that opens `redb::Database` and runs `begin_write` /
`commit` itself is violating the intended boundary. The component is supposed
to be dumb about storage and speak only sema-engine operations.

## 3. The answer: two cohorts

I audited every LiGoldragon repo for a direct redb dependency and direct
`Database::open`/`begin_write` use versus a sema-engine dependency.

### Bypass cohort — raw redb, no sema-engine (the violation)

| Component | Evidence | redb |
|---|---|---|
| `spirit` (new schema-derived) | `src/store.rs` — `Database::open/create`, `begin_write`, hand-rolled commit-sequence | 2.6.3 |
| `chroma` | `src/state.rs:74` — `Database::open/create`, `begin_write` | 2.6.3 |
| `orchestrator` | `src/state.rs:26` — `Database::open/create` | 2 |
| `schema-next` | `src/store.rs:31` — `Database::open/create` | 2.6.3 |

(Excluded: `sema` itself — legitimately wraps redb; the dated `design-deep-*`
scratch repos; `persona` meta-repo which carries both deps for wiring.)

### Sema-engine cohort — through the kernel (correct)

`mind`, `persona-spirit` (production Spirit), `repository-ledger`,
`introspect`, `orchestrate`, `upgrade` — all declare `sema-engine`.
Verified consumer: `persona-spirit/src/store.rs` uses `Engine::open`,
`register_table`, `.assert(Assertion::new(...))`, `.retract(Retraction::new(...))`
— no raw redb. Production Spirit does it right.

### The fault line

The bypass cohort is the **redb-2 / schema-derived + peripheral** set; the
conforming cohort is the **core Persona stack + production**, on redb 4 via
sema-engine. The split is not random — it tracks the redb-2-versus-redb-4
generation drift operator 304 found. The newer schema-derived cohort grew its
own raw-redb storage instead of consuming the kernel.

## 4. The critical consequence

**The new spirit — your forward-to-production target (Spirit 2540) — is in the
bypass cohort.** Promoting it as-is would put a component that violates the
sema-engine boundary into production. It is also the most-developed member of
the bypass cohort (it reimplements by hand what sema-engine provides, including
its own `COMMIT_SEQUENCE_KEY` — a hand-rolled copy of sema-engine's
`CommitSequence` handover marker). So the kernel adoption is not optional polish;
it is the precondition for the new spirit being the real thing rather than a
fake of the intended architecture.

## 5. Was it a misunderstanding?

Honestly: not universally, but yes in the schema-derived cohort. The core
Persona stack understood and followed the boundary — sema-engine is in real
use across six components, production Spirit included. But a whole second
cohort diverged, and the new spirit *documented* its bypass in its own
ARCHITECTURE.md ("this pilot uses redb directly to keep the proof
self-contained") as though it were an acceptable choice. That documentation is
the tell: the cohort treated the sema-engine boundary as optional-for-now
rather than inviolable. Per Spirit 2563 it is inviolable — "self-contained
proof" is not a valid reason to bypass the database interface.

I own my part: in reports 61-62 I described the new spirit's raw redb as
acceptable documented pilot intent ("not a defect to discover"). Your
correction reframes it correctly — the architecture decision *itself* was the
misunderstanding, and the pilot is a fake of the intended layering until it
goes through sema-engine.

## 6. The .sema file type (Spirit 2564)

Component database files should carry a `.sema` extension, not `.redb`, hiding
redb behind our own file type so the name states it is specifically a
sema-redb database. This lands in `sema` (the kernel owns the file open/create
and the extension) and reinforces Spirit 1007. A useful side effect: once
`.sema` is the convention, a raw `.redb` file in a component tree becomes a
*visible* smell — it means someone opened redb without the kernel. The file
extension becomes a conformance signal for this very boundary.

## 7. Remediation (for the operator)

1. **New spirit — adopt sema-engine for its SEMA plane (priority).** It is
   promoting to production; replace the hand-rolled redb store + commit-sequence
   with sema-engine (`Engine` + `register_table` + the operation surface). This
   also resolves the redb-2-vs-4 split (report 62 §2) as a side effect.
2. **chroma, orchestrator, schema-next — adopt sema-engine, or justify
   exemption.** Each owning lane confirms whether its store is durable
   component state (→ must go through sema-engine) or something genuinely
   outside the kernel's scope (e.g. `schema-next`'s store may be a build/lowering
   cache rather than component state — confirm before forcing). The default is
   adoption; exemptions are explicit, not assumed.
3. **sema — add the `.sema` extension convention.** The kernel opens/creates
   `.sema` files; sema-engine consumers get it for free.
4. **Use `.sema` as the standing conformance check.** A stray `.redb` in a
   component repo flags a kernel bypass.

## See also

- `reports/system-designer/62-spirit-data-lifecycle-ladder-concept-and-new-spirit-readiness-2026-06-04.md` §2 — the new spirit's storage-kernel adoption as a pre-production item.
- `reports/operator/304-Psyche-repository-stack-state-2026-06-04.md` — the redb-2-vs-4 generation drift this fault line tracks.
- `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md` — the intended boundary (component → sema-engine → sema → redb).
- `/git/github.com/LiGoldragon/persona-spirit/src/store.rs` — the correct consumer (Engine + register_table + assert/retract).
- `/git/github.com/LiGoldragon/spirit/src/store.rs` — the bypass (raw redb + hand-rolled commit-sequence).
- Spirit 2563 (no raw redb in daemons), 2564 (.sema file type), 1007 (.sema architectural role), 2540 (new spirit is the forward target).
