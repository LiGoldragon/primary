# Order 7: Sema contracts and low-power thinking

Proposal only, 2026-09-16. Source: efa157 order 7 at `76247035`, and its
`vision/sema.md` and `vision/modelRoles.md`, read whole.

## Sema: yes, with a precise boundary

Use `sema-message` for Message's durable record contract, analogous to
`signal-message` for its wire contract. Author `sema.ethos`; generate record
types, stable family/schema identities and sealed kind implementations in that
crate. Message's database process consumes those types. A separate Git
repository is a packaging choice, not the mechanism enforcing Rust isolation.

Rust's orphan rules alone do not prevent another crate implementing your trait
for its own local type. A private supertrait supplies that additional restriction:

```rust
mod private {
    pub trait Sealed {}
}
pub trait MessageRecordKind: private::Sealed {
    const FAMILY_ID: u32;
    const LAYOUT_VERSION: u32;
}
pub struct LedgerRecord { /* generated fields */ }
impl private::Sealed for LedgerRecord {}
impl MessageRecordKind for LedgerRecord {
    const FAMILY_ID: u32 = 1;
    const LAYOUT_VERSION: u32 = 4;
}
```

Only the defining crate supplies these implementations. An external database
process type cannot implement the sealed trait either: it should use a generic
store accepting `T: MessageRecordKind`, or a generated process wrapper owned by
the contract crate. Keep runtime backend operations separate. Sealing is an
API/build-time restriction, not process isolation, credential protection or a
barrier to someone modifying and recompiling the crate.

### Proposed Ethos shape

The following is a design sketch using the existing `Sema.1` envelope and a
typed migrations record family. It is not a parser/generator pass or adopted
grammar. Imported record definitions and sealing code generation still need
implementation. `spirit-ethos/sema.ethos` already demonstrates ordinary records
and a migrations family; executable migration semantics are additional work.

```text
Sema.1
[interface.{LedgerRecord InboxRecord ThreadRecord AgentRegistryEntry RelayRecord}]
{
  [
    RecordIdentifier.Integer
    MigrationIdentifier.Integer
    SchemaVersion.Integer
    FamilyIdentifier.Integer
    LayoutVersion.Integer
    RowCount.Integer
    ContentDigest.String
    SourceSnapshot.{ContentDigest SchemaVersion}
    FamilyLayout.{FamilyIdentifier LayoutVersion}
    MigrationStep.[
      Preserve.SourceSnapshot
      DecodeLegacyRegistry
      DecodeLegacyLedger
      DecodeLegacyInbox
      DecodeLegacyThreads
      ValidateReferences
      AddRelayFamily
      VerifyCounts
      PublishVersion.SchemaVersion
    ]
    MigrationSteps.Vector<MigrationStep>
    MigrationPlan.{SchemaVersion SchemaVersion MigrationSteps}
    MigrationState.[Prepared Running Verified Committed Failed]
    MigrationRecord.{MigrationIdentifier MigrationPlan MigrationState RowCount ContentDigest}
  ]
  [
    ledger.{LedgerRecord RecordIdentifier}
    inbox.{InboxRecord RecordIdentifier}
    threads.{ThreadRecord RecordIdentifier}
    registry.{AgentRegistryEntry RecordIdentifier}
    relay.{RelayRecord RecordIdentifier}
    migrations.{MigrationRecord MigrationIdentifier}
  ]
}
```

Before code generation, give repeated source/target version fields distinct
named types and specify per-family key types from the existing store. Digest
representation should become fixed bytes when the contract supports it; do not
duplicate message text or logs in migration records. Sealing belongs to the
generated Rust projection; this sketch does not invent a working Ethos `sealed`
keyword. Migration steps enumerate reviewed algorithms, not arbitrary shell or
SQL strings executed from a database row.

### First migration: preserve the unreadable row

Witnessed source at Message `fe0d0456`: `tables.rs` sets store schema **5**,
family layouts **4**, and permits only **4 → 5** as additive. Its comments
explicitly prohibit re-stamping **3 → 4**: archived contract layouts changed.
The current code preserves the file before the additive version update.
“Deployed schema 3, one pending row unreadable” is efa157's operational report,
not a new inspection of production by this flow.

1. Secondary preserves a consistent source store and identifies its actual
   schema and producer revision. Keep the original unreadable bytes.
2. A version-pinned legacy decoder reads schema 3 using its old types. Convert
   to schema 4 records in a separate destination; do not read v3 bytes with v4
   types or change only the schema stamp.
3. Validate family counts, identities, inbox/ledger/thread references and the
   pending delivery's source key/state. A row that still cannot be decoded
   blocks successful promotion; report its identity and digest without dropping
   it or claiming delivery.
4. Add the v5 relay family. Persist step/progress receipts so interruption can
   resume or restart idempotently. A migration ID identifies the exact plan and
   source snapshot, preventing accidental replay against a different store.
5. Verify the complete destination, then secondary performs atomic activation
   under its gates. Keep the prior store/generation for rollback; never point
   an old binary at an incompatible new store. Rollback after new writes needs
   an explicit replay/reconciliation plan.

Required proof before activation: real legacy fixtures, semantic conversion of
the pending row, crash/restart at each publication boundary, duplicate-run
idempotence, reference/count invariants, refusal of unknown versions and an
external-crate compile-fail test for sealed kinds. These are proposed tests,
not tests run in this design-only turn. The migration journal can be append-only;
that does not mean the existing redb file is physically append-only or that
bounded message retention has been removed.

## Model witness

Installed Claude Code: **2.1.263**. CLI help documents aliases `fable`, `opus`,
`sonnet`, and full model names. The `agents` help exposes `--model` but provides
no enum. The peer-reported Agent-tool list `opus|sonnet|haiku|fable` has not been
independently verified from that tool's schema here. A CLI selector is not a
proof of backend availability, and an alias can resolve differently over time.

Root ran one bounded, tools-disabled, nonpersistent call from `/tmp`:

```text
claude -p --model claude-opus-4-6 --tools ""
  --system-prompt "Reply with exactly OK. Do not use tools."
  --no-session-persistence --output-format json -- "Reply OK."
```

Structured subprocess arguments, detached stdin, 45-second deadline. Exit **0**,
result **OK**, `subtype: success`, `is_error: false`; `modelUsage` reported
`claude-opus-4-6`, `canonicalModel: claude-opus-4-6`, first-party provider,
1,906 input tokens and 4 output tokens. This proves a real call with the exact
Opus 4.6 ID on this installation/account. It does not prove Agent-tool subflow
dispatch, Opus 4.7/5 availability, or a comparison with Fable. No automatic model
substitution or benchmark claim.

## Low-power dispatch: small typed request, mechanical execution

Propose `LowPowerThinking` as an explicit request with a bounded model enum
(initial exact member `Opus46` → `claude-opus-4-6`), job/source-turn IDs,
context-snapshot digest, deadline and output limit. “Low power” describes the
role; it is not a demonstrated cost/performance property of Opus.

The main emits the datom header and a delimited task payload. A trusted harness
event marks that assistant output as an intentional dispatch. Flow reads the
event, resolves the exact model and source context, and starts one bounded job.
Do not scan arbitrary tool output, quoted transcript text or incoming peer
messages for a marker and execute it. Deduplicate by source Flow, turn and
dispatch block; repeated output must not launch repeated jobs.

Conceptual contract:

```text
ThinkingModel.[Opus46]
ThinkingRole.[LowPowerThinking]
ThinkingRequest.{JobIdentifier SourceTurnIdentifier ThinkingRole ThinkingModel ContextDigest Deadline OutputLimit}
ThinkingResult.[Completed.ThinkingAnswer Failed.ThinkingFailure Expired Cancelled]
```

The delimited payload remains verbatim task text, associated with the header
by digest and byte length. The amplified lane log is a frozen, provenance-marked
context snapshot; arbitrary log text does not grant new permissions. Set the
job's tools/permissions explicitly, default read-only for this thinking role.
Begin with one outstanding job per main and no automatic fallback to a larger
model. Failure is a typed result, not a reason to relaunch indefinitely.

Flow owns identity, membership and idleness. Message transports the request and
result and parks the result while the main is busy. When the main can receive,
resume it with the result reference and receipt; do not paste into a busy PTY.
Keep request, worker-completion, transport and recipient-turn receipts distinct.
The first proof should dispatch one real bounded Opus46 job and witness its
result in the main transcript, with a duplicate event test. No hook, timer,
dispatch parser or new MCP surface is installed by this proposal.
