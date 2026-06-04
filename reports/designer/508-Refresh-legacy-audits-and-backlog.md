---
title: 508 — Refresh: legacy audits and backlog
role: designer
variant: Refresh
date: 2026-06-04
topics: [upgrade-as-sema, schema-daemon, single-field-wrapper, alias-vs-newtype, closed-sum-rkyv, bead-staleness, operator-271, audit-retirement, context-maintenance]
description: |
  Agglomeration of a cluster of older designer audits and backlog
  snapshots (443, 447-452, 465, 470, 484, 488, 492) whose targets have
  mostly settled. Most were audits that retire with their audited
  target; their settled substance lives in production code, skills, and
  the current end-of-day state (494). What remains genuinely live is
  three pieces of design rationale — upgrade-as-SEMA-on-Asschema, the
  single-field-wrapper / alias-vs-newtype rule, and the closed-sum-enum
  honest-representation rule for rkyv — agglomerated here and proposed
  for manifestation into permanent surfaces as constraints.
---

# 508 — Refresh: legacy audits and backlog

## Why this Refresh exists

A cluster of older designer reports were point-in-time audits and
backlog snapshots. Audits retire with their audited target once the
target settles and the rationale has a permanent home; backlog
snapshots retire once a newer state report reissues the live handoffs.
This Refresh names where each cluster member's substance landed, keeps
the small residue of still-live design rationale in one dense place,
and proposes the leaned-on pieces for the permanent layer as
constraints. The current canonical workspace-state surface is
`494-Psyche-workspace-state-end-of-day` — that report, not this one,
carries the live open-decisions list.

## The three pieces of still-live design rationale

### 1 · Upgrade IS SEMA operations on the Asschema

The load-bearing realization (the upgrade-as-SEMA arc): the upgrade
mechanism is the same SEMA library applied to a different object type.
Today `spirit-next` applies SEMA operations to record-store `Entry`
values; the schema daemon applies SEMA operations to schema-store
`Asschema` values. [the upgrade mechanism is realized as SEMA
operations on the Asschema, sharing the same library] (Spirit 1308);
[the schema daemon IS the editor of the schema — it receives upgrade
messages, applies them, and derives both new data type code and
upgrade migration code] (Spirit 1309).

The shape, densely:

- The **schema daemon** receives a NOTA-encoded schema-edit operation
  (`AddField`, `RemoveField`, `ChangeFieldType`, `RenameField`,
  `AddVariant`, `RemoveVariant`, `AddDeclaration`, `RemoveDeclaration`),
  applies it as a SEMA write against its stored Asschema, and derives
  BOTH the new data-type Rust code AND the upgrade-migration Rust code
  from the (old Asschema, new Asschema, migration spec) triple.
- A separate **upgrade daemon** (the current `upgrade` triad runtime)
  consumes the derived code, shells out to the Nix build for a new
  daemon binary (new typed Rust requires recompilation — the daemon
  cannot live-patch types: [new Rust data types require recompiling the
  daemon binary; the new daemon spawns alongside the old for testing]
  (Spirit 1311)), spawns it alongside the old via the
  **transitory-database pattern** ([the daemon runs two databases
  concurrently as part of the SEMA interface] — Spirit 1310), and runs a
  two-tier acceptance test (minimal edge-case DB first, then a
  throwaway copy of production) before atomic socket-level cutover. The
  old database file is preserved as the rollback artifact.
- The migration emitter renders each `FieldMigration` variant from a
  fixed template — `WrapSingleton` becomes `vec![historical.field]`,
  and it is generic over the inner type (`String → Vec<String>`,
  `Topic → Vec<Topic>`, `QualifiedName → Vec<QualifiedName>` all share
  one spec). Migration specs are positional structural shapes, not
  type-specific incantations.

The deep principle this closes: [NOTA always corresponds to a specified
object; the goal is correspondence all the way down to NOTA-as-schema
specifying the objects themselves] (Spirit 1312). The chain — NOTA
tokens correspond to typed objects; NOTA schema source corresponds to
typed Asschema; NOTA upgrade operations correspond to typed schema-edit
operations; NOTA upgrade operations edit NOTA schema source, producing
new NOTA schema that corresponds to new typed objects. The recursion
closes when the schema daemon's OWN schema becomes editable by the
operations it serves: [design the self-editing system from the start,
not later] (Spirit 1314).

**Division of labor (load-bearing):** the schema daemon owns the
Asschema store and the edit/derive step and NEVER triggers a build; the
upgrade daemon owns the migration history, active-version event log,
quarantine list, build invocation, spawn coordination, and cutover
authority, and NEVER mutates the schema. They cooperate over the wire
via a `SchemaEdited` event stream. The upgrade ARCHITECTURE.md still
frames its future state through the older 324/326 reports and a
"brilliant macro library" cutover; the SEMA framing above is the
current direction and is proposed for manifestation below.

**Open questions that remain genuinely open** (each is a psyche call or
a follow-up, not settled): one merged daemon vs two; whether the schema
daemon edits its own schema and how bootstrap-bricking is prevented;
who authors the migration test databases; how the
`criomos-horizon-config` deploy stack reconciles with hot-spawned
binaries that do not land in `/run/current-system/sw/bin`; typed
handling for migrations that cannot total-convert every record
(`Drop`, fallible `Cast`) and the quarantine path; cross-component
atomicity when a shared substrate type changes; the migration-history
grain; and the authority class for sending schema edits (owner socket
by default). These were the eight open questions of the original
design; they survive into the implementation slices.

### 2 · The single-field wrapper, and alias-vs-newtype

The single-field struct wrapper (`struct CodecDerive { input:
DeriveInput }` and 27 peers across the next-stack repos) is the
workspace's method-only-rule answer to "the verb needs a noun the inner
type cannot provide." It is a load-bearing pattern, not a smell, when
it pays its way through one of these reasons:

- **Orphan-rule workaround** — the inner type is foreign (`syn`, std,
  another workspace crate's primitive) or a generic parameter, so
  inherent methods cannot attach to it; the local newtype hosts the
  methods. Structurally necessary: free functions are forbidden, and an
  extension trait is legal but indirect.
- **Named container** — the inner type is a collection (`Vec<T>`,
  `BTreeMap`) but the role the collection plays (`Pattern`,
  `MacroRegistry`, `StructFieldMap`) has its own name and methods.
- **Semantic-distinction newtype** — workspace-owned inner type, but
  the wrapper makes "this Asschema is being used as an artifact"
  type-enforced and hosts the concern-specific methods.
- **Internal builder / parser / CLI state** — the wrapper IS the state
  machine; idiomatic Rust.
- **Typestate phase carrier** — zero inherent methods is the EXPECTED
  shape; methods live on the parameterized container (`Mail<Phase>`).
  The phase carrier is not a ZST because it carries payload data.

The keystroke code-review test: **method count > 0 OR trait impl > 0 OR
typestate phase marker.** Absence of all three is the anti-pattern. A
valid wrapper can coexist with a ZST anti-pattern in the same file
(`CodecDerive` was valid; sibling `FieldEncode` was a `struct
FieldEncode;` ZST namespace — since fixed at nota-next commit
`f5906bae`). The audit-methodology note: after validating single-field
wrappers, ALSO grep for ZST method holders in the same scope.

This pattern's production refinement landed as the **alias-vs-newtype
emission distinction**: schema entries that merely alias another type
lower to a Rust `pub type` (not a wrapping newtype), so callers do not
hand-write triple-wrapping. [generated APIs should not force callers to
hand-write that repetition] (Spirit 1557); single-field newtype
lowering refined to struct-body-only (Spirit 1535). The mechanism is
live in `schema-next` (`TypeDeclaration::Alias`), `schema-rust-next`
(emit `pub type`, skip conflicting `From` impls for alias payloads),
and `spirit-next` (alias payloads end-to-end with a process-boundary
witness). The rule worth keeping permanent: a schema entry that is a
bare alias emits `pub type`; a single-field struct that hosts methods
emits a newtype.

### 3 · Closed-sum enum is the honest rkyv representation

When a schema-emitter produces a Rust type whose values can take N
structurally-different shapes that must be archived in rkyv storage,
the emitter produces a **closed-sum enum with one variant per shape**.
[closed-sum enums make the variant-set known at type-system level; the
archived bytes recover the variant via a tag; open type erasure cannot
have this property] (Spirit 1324). Verified holds-with-caveats on a
`MacroPatternObject` pilot:

- rkyv 0.8 requires every archived value to have a known archive size
  up-front; closed-sum enums satisfy this because every variant pays the
  width of the widest payload (the honest tax — 32 bytes on x86-64 for
  the 4-variant `String`/`Box` pilot).
- Recursive variants MUST be emitted as `Box<T>` — without it, the type
  is infinite-size and the compiler refuses; rkyv archives `Box`
  transparently. Deep nesting then scales linearly (~18 bytes per level;
  depth-80 archives in 1,449 bytes), not exponentially.
- The variant tag survives the wire essentially free (1.29x archive
  cost vs raw payload bytes), so same-shape siblings
  (`Capture(String)` / `RestCapture(String)` / `Atom(String)`) do not
  collide.
- The trait-object alternative is structurally excluded: `Box<dyn
  Archive>` does not compile (the `Archive` associated types make the
  trait not dyn-compatible).

The refinement the witnesses license: same-payload-type sibling
variants should consolidate under one variant whose payload is a typed
sub-enum WHEN (and only when) they share a semantic family — not by
payload type alone (`Capture` and `Atom` both wrap `String` but are
different families). And the emitter SHOULD insert `Box<T>` around a
recursive variant automatically rather than making every schema author
hit the compile error. Open tension (no action, named): the closed-sum's
static closure conflicts with eventual hot-reload, since
`SchemaEdit::AddVariant` adds a variant only by recompiling a new binary
per Spirit 1311.

## What retired and where its substance lives

| Source report | Disposition | Landing that absorbed it |
|---|---|---|
| 443 design-improvements-audit (dir) | Drop | Substrate-audit findings absorbed by 445 next-stack audit + the skill migrations tracked in 494; the §"#1" envelope-duplication finding survives as designer 444 §5 H1 (schema-core extraction). |
| 447 upgrade-as-sema-design | Drop after this Refresh | §"1" above carries the live rationale; manifestation into `upgrade/ARCHITECTURE.md` proposed below. |
| 448 single-field-wrapper-audit | Drop after this Refresh | §"2" above; the rule is proposed for `skills/rust/methods.md`. |
| 449 bead-staleness-audit | Drop | A working-order audit proposal; the recommended close-sweep is a task, not durable intent. Bead hygiene lives in `skills/beads.md` §"Periodic audit". |
| 450 operator-271-closed-claims-verification | Drop | Audit verification; all five claims VERIFIED with witnesses on feature branches and merged via the operator pipeline. Audit retires with its target. |
| 451 operator-271-falsifiable-specs | Drop | The falsifiable-spec branches were the contract; precise claims (1-3) were small cleanups now landed, scaffold claims (4-8) are the horizon work tracked elsewhere (444 §5, 446, and §1 above). The designer-sub-agent-as-feature-branch pattern is now standard practice (`skills/designer.md`). |
| 452 rkyv-enum-wrapping-audit | Drop after this Refresh | §"3" above; the rule is proposed for `skills/rust/storage-and-wire.md`. The pilot branch lives in git history. |
| 465 recent-decision-landscape | Drop | A point-in-time decision snapshot superseded by 494's end-of-day state; the proof-of-usage ladder it referenced lives in `skills/architectural-truth-tests.md`. |
| 470 psyche-backlog-top-6-visual | Drop | A backlog snapshot reissued by 492 then 494; the live pending items are in 494 §4. |
| 484 production-readiness-meta (dir) | Drop | Component-readiness audit superseded by the production landings tracked in 494 (schema-source codec, alias lowering, process-boundary witnesses) and the 484-era skill migrations. |
| 488 Psyche-487-overview | Drop | A Psyche orientation snapshot; its decisions (eprintln removal, per-crate trace, Path B) are ratified-and-landed per 494 §3. |
| 492 vision-architecture-ratification-queue | Drop | The ratification queue is reissued by 494, which records which items resolved and surfaces the genuine remainder in §4. 494 is the live surface. |

## For the psyche

Most of this cluster was audits whose targets settled — operator-271
claims closed with witnesses, the single-field-wrapper question
resolved into the live alias-vs-newtype lowering, the rkyv closed-sum
hypothesis verified. Those retire cleanly. Three pieces of design
rationale are still load-bearing and are proposed for the permanent
layer rather than left in reports: the **upgrade-as-SEMA-on-Asschema**
direction (into `upgrade/ARCHITECTURE.md`, where the current text still
frames the future state through older reports), the **single-field
wrapper / alias-vs-newtype** rule (into `skills/rust/methods.md` as a
review constraint), and the **closed-sum-enum honest-representation**
rule for rkyv (into `skills/rust/storage-and-wire.md` as a constraint).
The orchestrator applies those manifestations. The live open-decisions
list stays in 494, not here.
