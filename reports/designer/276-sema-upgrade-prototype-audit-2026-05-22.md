# 276 - Sema-upgrade prototype audit (2026-05-22)

*Designer audit. Operator pushed the first sema-upgrade triad
prototype: ordinary contract `signal-sema-upgrade@7991a825`,
policy contract `owner-signal-sema-upgrade@9e61b034`, runtime
`sema-upgrade@408e9e24`. Headline: triad shape is clean and the
wire surface is honest, but the runtime is daemon-less and the
persona-spirit 0.1.0 → 0.1.1 migration module is a no-op stub
(`Ok(ModuleResult::unchanged())`) that does not yet read or write
the spirit sema database. Psyche record 102/103 (2026-05-22)
authorise the next slice — "migration logic with a temporary CLI
for testing the logic on the database, and do the actual
migration" — so the prototype's daemon-less shape is correct and
the next operator pass is migration logic that actually runs.
Three of operator/153's five Qs are now answered from intent (Q1
implicit Shape A via record 103; Q2 via records 6+71; Q4 via
record 70 as /275 noted); Q3 (commit-sequence scope) needs psyche
call; Q5 is /274 Path A. One new intent-clarity-critical point
emerges around schema-address discipline: the prototype uses
semver `Version (major minor patch)`, not the
content-addressable schema-address hashes from /263 and /270 —
divergence needs psyche call.*

## 1. Audit summary

Three repos pushed 2026-05-21 evening:

| Repo | Commit | Loc | Shape |
|---|---|---|---|
| `signal-sema-upgrade` | `7991a825` (22:19) | 166 src + 199 test | Ordinary: `Inspect`, `AttemptUpgrade`, `Report`, observer surface. |
| `owner-signal-sema-upgrade` | `9e61b034` (22:26) | 154 src | Policy: `Register`, `Allow`, `Block`, `Query`. |
| `sema-upgrade` | `408e9e24` (22:26) | 371 src + 118 test | Runtime: `Engine`/`MigrationIndex`/`MigrationModule`, signal-executor `Lowering`, one stub migration module. |

All three pass `cargo test -j 2` and `nix flake check
--max-jobs 0 -L` per bead `primary-eanf` (closed). Follow-up bead
`primary-l3h5` ("Add sema-upgrade daemon and thin upgrade CLI")
is open.

The prototype is wire-shape correct (signal-executor based,
ordinary + owner legs present, NotaRecord/NotaEnum derives,
canonical NOTA round-trips), wire-surface terser than /270 (the
six-op `Inspect/Plan/Migrate/Report/Tap/Untap` becomes a five-op
`Inspect/AttemptUpgrade/Report/Tap/Untap`), and runtime stubbed at
the migration layer.

## 2. signal-sema-upgrade audit

### 2a. Wire surface

`src/lib.rs` declares via `signal_channel!`: `Inspect(Inspection)`,
`AttemptUpgrade(Attempt)`, `Report(ReportQuery)`. Replies:
`InspectionReported`, `UpgradeCompleted`, `UpgradeRejected`,
`Reported`, `RequestUnimplemented`. Observable surface generates
`Tap`/`Untap` (matched in execution.rs:66).

`Inspection`/`ReportQuery` are enums (`All | Component(ComponentName)`).
`Attempt` is `(component, source: Version, target: Version)`.
`Version` is named-field `{major: u16, minor: u16, patch: u16}` —
NotaRecord, not tuple. Renders as `(0 1 0)`. `ComponentName` and
`MigrationIdentifier` are `NotaTransparent` newtypes.

### 2b. Comparison to /270

/270 §3a sketched six operations: **Inspect/Plan/Migrate/Report/
Tap/Untap**. The prototype has five: **Inspect/AttemptUpgrade/
Report/Tap/Untap**. Differences:

- **`Plan` absent.** No `MigrationPlan` record type; no diff
  classifier; no per-step structural typing. The prototype
  answers "is this version pair supported?" not "what would this
  plan do?". Major reduction.
- **`Migrate` → `AttemptUpgrade`.** Rename. New name reads
  cleaner (announces uncertainty).
- **`Inspect` reply restructured.** /270's `Inspected` carried
  `Decision = Proceed | PlanRequired | UnknownStoredAddress |
  Quarantined`. Prototype's `InspectionReported` carries
  `Vec<SupportedMigration>` — daemon advertises what migrations
  it *carries*, rather than what each component *needs to do*.
  Boot-time consult-before-serve protocol not implemented.

### 2c. The schema-address divergence — intent-clarity-critical

/270 §3 grounded sema-upgrade in /263's schema-spec language:
schema-address (Blake3 of canonical schema-layout encoding)
identifies the data shape; migration is the path between
addresses. Prototype replaces schema-address with **semver
`Version (major minor patch)` records**. No content-addressable
identity in the wire surface; no schema-layout language
consumption. Legitimate prototype simplification (/263 unimplemented)
but opens load-bearing question — see §10a.

### 2d. Quality

Names spell English. `RejectionReason`/`UnimplementedReason` are
unit-variant enums (final leaves per record 73).
`RequestUnimplemented` is the workspace's honest no-op pattern.
`examples/canonical.nota` has seven lines verified by round-trip
tests. Born triad-shaped per /270 §2.

## 3. owner-signal-sema-upgrade audit

### 3a. Policy surface

`src/lib.rs`: `Register(Registration)`, `Allow(PolicyRange)`,
`Block(Block)`, `Query(Query)`. Replies: `Registered`, `Allowed`,
`Blocked`, `PolicyReported`, `PolicyRejected`,
`RequestUnimplemented`. `Registration` records component +
source + target + migration identifier + state (Enabled |
Disabled). `Block` adds `BlockReason (Unsafe | Superseded |
NotReviewed)`.

### 3b. Comparison to /270

/270 §3c sketched seven operations: `ApprovePlan/RejectPlan/
Quarantine/Release/ConfigureThrottle/RegisterSchema/RetractSchema`.
The prototype's four collapses:

- `Register` ↔ `RegisterSchema`. Rename. Reads cleaner — noun is
  *migration registration*, not *schema*.
- `Allow` + `Block` ↔ `ApprovePlan` + `RejectPlan`. Per-range
  (component + source + target), not per-plan-identifier —
  policy is stated against the migration range, not a specific
  plan instance.
- `Query` ↔ catalogue introspection. Same shape.
- **Absent**: `Quarantine`/`Release`, `ConfigureThrottle`,
  `RetractSchema`. Deferred until daemon ships.

### 3c. Quality

Owner reuses ordinary's `Attempt`/`ComponentName`/
`MigrationIdentifier`/`Version` (`impl From<Attempt> for
PolicyRange`); the two sockets cannot drift on migration naming.
`BlockReason::Superseded` names the "next version pair
supersedes this one" case the daemon needs once migrations
chain. Minor gap: no `tests/round_trip.rs` and no
`examples/canonical.nota`.

## 4. sema-upgrade runtime audit

### 4a. signal-executor usage

`src/execution.rs` implements `Lowering` correctly: `Operation`
type from `signal_sema_upgrade`, `Reply` likewise, `Command` is a
private mirror (component-local intent type), `ComponentEffect`
is the component-local outcome. `Lowering::lower` maps wire
operations to commands; `Tap/Untap` returns
`RequestUnimplemented(NotBuiltYet)`.

`Engine` implements `CommandExecutor::execute_atomic_batch`:
operations process serially, effects accumulate
(`staged_completions`/`staged_rejections` buffers), batch
commits atomically (staged buffers overwrite engine state at
batch end). Per signal-executor's atomic-batch model.

Sema classification: `Inspect`/`Report` → `Match`;
`AttemptUpgrade` → `Mutate`. Effects: `Inspected`/`Reported` →
`Matched`; `Completed` → `Mutated`; `Rejected` → `NoChange`
(correct — rejection didn't mutate).

### 4b. MigrationIndex design

```rust
pub struct MigrationModule {
    supported: SupportedMigration,
    run: fn(&Attempt) -> Result<ModuleResult, RejectionReason>,
}
pub struct MigrationIndex { modules: Vec<MigrationModule> }
```

`MigrationIndex::prototype()` hard-codes the module list.
`MigrationIndex::attempt(&Attempt) -> Result<Completion,
Rejection>` finds matching module by (component, source, target)
triple, calls `run`, wraps the outcome.

**Compile-time module index** pattern: modules register their
triple at compile time; new migrations land by editing the list.
No dynamic loading; no `Box<dyn>`; `fn(&Attempt) -> ...`
function-pointer field is the right indirection. Owner policy
is a separate concern the daemon will overlay. Reads cleanly.

### 4c. Daemon-less runtime — correct per psyche directive

Runtime ships: library + `Engine::executor()` wrapping engine in
signal-executor + in-process tests. No daemon binary, no CLI
binary, no `bootstrap-policy.nota`, no socket binding, no
inspect-before-serve protocol. /270 triad shape not complete;
only library scaffolding is. Correct under psyche record 103:
*"Sema-upgrade implementation sequence — migration logic comes
first, then daemon/socket/thin CLI. A temporary CLI is used to
test the migration logic directly against the sema database
before the formal triad daemon wraps it."*

## 5. The persona-spirit 0.1.0 → 0.1.1 migration

### 5a. What the module actually does

`src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs`:

```rust
fn run(attempt: &Attempt) -> Result<ModuleResult, RejectionReason> {
    if attempt.component.as_str() != COMPONENT {
        return Err(RejectionReason::ComponentMismatch);
    }
    Ok(ModuleResult::unchanged())
}
```

The module is a **stub**. It checks the component name matches
("persona-spirit"), then returns `ModuleResult::unchanged()` —
zero records changed. No file is opened; no redb is touched; no
Certainty value is translated to Magnitude. The
`changed_records: 0` ends up in the `Completion` reply.

The migration does not actually run. It declares it exists (via
`SupportedMigration` in the index), accepts a matching attempt
without rejection, and reports zero records changed — that is
the entire body.

### 5b. What 0.1.0 → 0.1.1 should mean

- 0.1.0 = deployed Spirit, `Entry::certainty: Certainty`,
  three-variant.
- 0.1.1 = post-Magnitude, `Entry::certainty: Magnitude`,
  seven-variant.

Transformation: each stored record's `certainty` field maps
`Certainty::Minimum/Medium/Maximum` onto `Magnitude::Minimum/
Medium/Maximum`. **Discriminator positions differ**:
Certainty's are 0/1/2; Magnitude's are 0/3/6 (order: `Minimum,
VeryLow, Low, Medium, High, VeryHigh, Maximum`). Not zero-cost —
stored Certainty bytes need discriminator rewritten. This is a
structural migration in /263's classifier.

Stub does NOT do this. Implementation requires: open spirit
sema database; read StoredRecord with v0.1.0 type bindings
(Certainty-bearing); translate Certainty → Magnitude; write
StoredRecord back with v0.1.1 type bindings (Magnitude-bearing);
update schema-version tag (Approach C, record 21). The migration
logic for this transformation does not yet exist in code anywhere
in the workspace.

### 5c. Approach C vs copy-migrate-verify-switch

The signature is neutral on shape. `ModuleResult
{ changed_records }` nudges toward eager-copy (counting implies
enumerating). Psyche record 102 verbatim: *"create the migration
logic modul with a temporary cli to test the logic on the
database, and do the actual migration"*. Settles next slice
toward copy-migrate-verify-switch (or simpler
stop-old-start-new) rather than pure Approach C read-side
lifting. Approach C remains the long-term boot-path shape; first
sema-upgrade migration is the copy-side variant.

## 6. operator/153 question state

| Q | Subject | Source | Disposition |
|---|---|---|---|
| Q1 | Shape A vs B | Records 102 + 103 | **Answered from intent.** Operator already built triad first (Shape A). Record 103 verbatim: *"This implicitly sequences operator/153 Q1 toward Shape A (universal sema-upgrade triad first) AND adds a temp-CLI testing step ahead of daemon assembly."* |
| Q2 | Spirit primary, intent/*.nota historical fallback | Records 6 + 71 | **Answered from intent.** Record 6 verbatim: *"Begin using the Spirit CLI as the substrate for intent logging immediately, to work out the kinks of the deployed pilot while the legacy intent/*.nota append flow is in the process of being retired."* Record 71 verbatim: *"Its first concrete migration test case is the legacy intent file log → spirit migration: treat the legacy intent/*.nota substrate as a 0.01 version of the spirit database..."* Operator's flagged check (records 74/75 in spirit, missing in workspace.nota) is correct. |
| Q3 | sema-engine commit sequence scope; stop-old-start-new acceptable | No intent record | **Needs psyche decision.** See §10b. Designer lean per /273 §6b: per-database. Per /273 §6c: allow stop-old-start-new for first production migration. |
| Q4 | ItemPriority → Magnitude | Record 70 | **Answered from intent** — same as /275's point 2. Record 70 parenthetical *"(and any other small-vocabulary ordinal enum reaching for the same concept)"* authorises directly. No psyche call needed on the "whether"; only sequencing. |
| Q5 | Forge keep existing as criome executor | /274 Path A | **Answered from designer report.** /274 §4 Path A reframes existing `forge` as a per-component forge for criome's authority chain; existing `signal-forge` is the criome ↔ forge wire. Both keep names. Operator's lean matches. |

## 7. /275 six-critical-points state

| /275 point | Subject | State |
|---|---|---|
| 1 | Spirit-Magnitude branch merge cadence | **Progressing.** sema-upgrade `Cargo.toml` depends on `signal-persona-spirit` at `branch = "operator/spirit-response-protocol"` — operator treats the Magnitude branch as already-current. Merge to main becomes the next concrete blocker. Designer lean unchanged: merge now (/275 §9c). |
| 2 | ItemPriority collapse | **Restate.** Record 70 authorises. No new psyche decision required. Same answer as Q4. |
| 3 | Sema-upgrade boot order (first to start?) | **Open.** Prototype is daemon-less; question concrete only when daemon ships (bead `primary-l3h5`). See §10c. |
| 4 | Sema-upgrade self-upgrade | **Open.** Not in intent. See §10d. |
| 5 | Magnitude collapse extension to Health/Readiness | **Open.** Not in intent. See §10e. |
| 6 | Engine-manager rename internal axis | **Open.** Persona main still ships `src/supervisor.rs`, `src/supervision_readiness.rs`, seventeen `supervision_socket_*` identifiers per /275 §2b. No new commits since /275. |

## 8. New patterns observed (the good)

1. **Compile-time MigrationIndex.** Modules register their triple
   at compile time. No dynamic registration; no `Box<dyn>`;
   function-pointer field is the right indirection.

2. **Honest no-op `RequestUnimplemented`** with `NotBuiltYet |
   IntegrationNotLanded`. Returned for `Tap/Untap` per the
   universal no-op-as-explicit-command rule.

3. **Triad-from-day-one.** Ordinary + owner shipped 8 minutes
   apart; runtime depends on both. Matches /270 §2.

4. **NotaTransparent newtypes for identifiers** (`ComponentName`,
   `MigrationIdentifier`). Wire form is the inner string.

5. **Atomic batch staging** via `staged_completions`/
   `staged_rejections` buffers — tested via
   `multi_operation_request_is_atomic_unit_for_executor`.

6. **Conservative semver `Version` shape.** Named-field record,
   not tuple struct. Renders as `(0 1 0)` per record 42.

7. **`BlockReason::Superseded`** — names the "next version pair
   supersedes this one" case the daemon needs once migrations
   chain.

## 9. Ugly patterns / philosophy deviations (the bad)

1. **Stub migration module advertised as supported.** Load-bearing
   ugliness. `InspectionReported` carries the migration as
   supported; `AttemptUpgrade` returns `UpgradeCompleted (...
   0 changed_records)` — but no records were touched. Per
   `skills/beauty.md`: declares success on a no-op. Honest
   scaffolding only if next slice (real migration per record
   102) lands soon.

2. **`supported_migration` is a free function** (`src/index.rs:96`).
   Should be `SupportedMigration::new` or
   `MigrationModule::new_with(...)`. Per `skills/abstractions.md`:
   every reusable verb belongs to a noun. Minor.

3. **No `tests/round_trip.rs` and no `examples/canonical.nota`
   in owner-signal-sema-upgrade.** Coverage gap.

4. **Plan-shape divergence undocumented in ARCHITECTURE.md.**
   Future readers reach for /270 expecting Plan/Approve/Run and
   won't find it; the gap-naming would help.

5. **`MigrationIndex::prototype()` transitional name.** Rename
   trigger underspecified. Minor.

Counts: **7 good, 5 ugly.** Net positive.

## 10. Intent-clarity-critical points still needing psyche decision

Extensive context per point.

### 10a. Schema-address vs semver — long-term identity?

**Question.** /270 §3 grounded sema-upgrade in /263's
schema-spec language: data shape identified by Blake3 of canonical
schema-layout encoding (schema-address); migration is the path
between addresses. Prototype replaces with semver `Version
(major minor patch)`. Long-term identity uses:
- **(a)** Schema-address (content-addressable, full /270 design).
  Prototype's semver becomes transitional shape retiring when
  /263 lands.
- **(b)** Semver only. /263 + /270 §3's path is over-engineered;
  semver IS the destination.
- **(c)** Both, layered — semver as wire-friendly surface,
  schema-address as layout-correctness back-stop.

**Intent.** Records 29 + 30 presuppose schema-address; prototype's
semver makes (b) live without retracting (a). Designer lean: **(c).**

**Load-bearing fork.** Three months of /263 + /270 schema-address
machinery becomes deliverable or speculative based on the answer.

### 10b. Commit sequence scope; stop-old-start-new acceptable?

**Question.** /273 §3 introduces durable monotonic commit-sequence
as live-copy high-water mark. (1) Per-database (sema-engine
maintains one sequence per sema database) or per-component (each
daemon owns its own)? (2) Stop-old-start-new acceptable for the
first production migration (persona-spirit 0.1.0 → 0.1.1)?

**Intent.** Nothing — no record covers commit-sequence scope.

**Designer lean** per /273 §6b: per-database. Per /273 §6c: allow
stop-old-start-new for first production migration. Both designer
leans only.

**Load-bearing fork.** Per-component multiplies across daemons;
per-database centralises in sema-engine. Stop-old-start-new for
migration 1 plus commit-sequence for migration 2 is the fast-cadence
path per record 56 ("moving fast").

### 10c. Sema-upgrade boot order (carry-forward /275 §9a)

Does sema-upgrade-daemon start before persona-daemon? /270 §5
puts sema-upgrade in inspect-before-serve path — only works if
sema-upgrade is up before inspector. Record 17 orders spirit
last; symmetric Q is whether sema-upgrade is **first**. Designer
lean per /275 §9a: first to start, owned by engine manager.

### 10d. Sema-upgrade self-upgrade (carry-forward /275 §9b)

Recursive self-application vs hand-written bootstrap path. /270
§9.3 lean: hand-written until contracts stabilise, then dogfood
once. Bottom-of-stack asymmetry is real.

### 10e. Health/Readiness collapse onto Magnitude (carry-forward /275 §9d)

Four ordinal enums in `signal-persona-{system,harness}`
(SystemHealth, SystemReadiness, HarnessHealth, HarnessReadiness)
reach for the same concept. Record 70's parenthetical authorises
"any other small-vocabulary ordinal enum reaching for the same
concept" — but health/readiness reach for slightly different
concepts than rank. Designer lean: collapse with
field-name-carries-dimension.

### 10f. Live witness on the migration — success criterion?

**Question.** Record 102/103 settle "migration is actually run".
Three concrete options:
- **(a)** Temp CLI takes v0.1.0 spirit redb path, produces v0.1.1
  redb in temp dir; original untouched. Success: open new redb
  with v0.1.1 bindings, all records decode, certainty carries
  Magnitude.
- **(b)** Temp CLI **replaces** production spirit redb in-place.
  Success: deployed spirit binary (post-merge plus CriomOS-home
  rebump) accepts queries against migrated redb.
- **(c)** Temp CLI **copies** to sibling path; runs v0.1.1 spirit
  binary against copy; psyche verifies via spirit CLI; separate
  manual cutover replaces production redb.

**Intent.** /273 §3a's copy-migrate-verify-switch points at (c);
/270 §5 Approach C points at (b) at boot rather than migration
time. Record 103's phrasing doesn't pin the shape. Designer lean:
**(c)** — copy-first preserves original through verification;
cutover is its own gated step. Matches /273 §3a and is
conservative-by-default.

**Load-bearing fork.** Determines temp CLI success criterion →
test fixture → whether next slice ships deployed-binary cutover
(b) or side-by-side verification (c).

## 11. Recommended next operator slice

Per records 102/103: migration logic + temporary CLI, then daemon.

1. **Land the persona-spirit 0.1.0 → 0.1.1 migration body.**
   Replace `Ok(ModuleResult::unchanged())` with actual Certainty
   → Magnitude transformation. Needs: v0.1.0 type bindings
   (copy inline as `legacy/` module or pull
   `signal-persona-spirit@v0.1.0` under crate alias); v0.1.1
   bindings (on `operator/spirit-response-protocol`); per-record
   translator (`Certainty::{Minimum,Medium,Maximum} →
   Magnitude::{Minimum,Medium,Maximum}`); redb read/write loop;
   real `ModuleResult { changed_records: N }`.

2. **Build the temporary CLI** per record 103. Source redb path +
   target redb path; calls `MigrationIndex::prototype()`
   in-process; runs module; reports count. Maintenance binary
   the daemon eventually replaces.

3. **Run the migration on a copy of the live spirit redb** per
   record 102 ("do the actual migration"). Subject to 10f's
   psyche call on success-criterion shape.

4. **Merge `operator/spirit-response-protocol` to main** on both
   spirit repos per /275 §9c. v0.1.1 tag lands post-verification;
   CriomOS-home rebump follows.

5. **Then** ship sema-upgrade daemon (bead `primary-l3h5`).
   Awaits 10c/10d/10f answers.

Slices 1-3 authorised by 102/103. Slice 4 is /275 §9c. Slice 5
awaits 10c/10d/10f.

## 12. References

**Operator commits.** `signal-sema-upgrade@7991a825`,
`owner-signal-sema-upgrade@9e61b034`, `sema-upgrade@408e9e24`,
`signal-persona-spirit@d7b22bfb`, `persona-spirit@d1c76108`
(Magnitude branch tips).

**Designer reports.** `/260` Approach C; `/263` schema-spec
language (10a); `/269` Magnitude; `/270` sema-upgrade design;
`/273` schema-migration synthesis; `/274` forge reconciliation
(Q5); `/275` operator-work audit (extended §7 + §10).

**Operator reports.** `/151` deployed migration proposal;
`/153` intent-questions (answered §6).

**Intent records (spirit sema database).** 6 (Spirit CLI as
intent substrate), 21 (Approach C), 26 (Spirit canonical
substrate), 29 (content-addressable schema layout), 30
(rkyv-headroom), 41 (Nix-flake upgrade protocol), 42 (no-tuples),
70 (Magnitude — authorises ItemPriority via parenthetical), 71
(sema-upgrade as universal mechanism), 72 (sema vocabulary), 73
(branches/leaves), 101 (prototype target), 102 (temp CLI), 103
(migration logic before daemon; actually run; implicit Shape A).

**Beads.** `primary-eanf` closed; `primary-l3h5` open.

**Workspace artefacts.** `skills/component-triad.md`,
`skills/abstractions.md`, `skills/beauty.md`.

**Live deployed state.** Per /275 §3d:
`/home/li/.nix-profile/bin/spirit` at `persona-spirit@694452a`
(pre-Magnitude). `spirit '(Record (test Decision "test" "test"
High "test"))'` returns `Error: InvalidSpiritRequest { reason:
"unknown variant 'High' for enum 'Certainty'" }`. Deployed
substrate is the v0.1.0 form the stub claims to handle.
