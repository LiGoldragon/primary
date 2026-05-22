## 10 — Component migration plan: onto the v4 three-layer architecture

**Lane:** second-operator-assistant
**Reads against:** /144 (the landed v4 alignment in signal-frame +
signal-executor + signal-sema + signal-persona-spirit + persona-spirit),
/254 (operator-facing direction with five psyche-affirmed gaps), the
v3→v4 per-crate diff and engine-manager rename (both since dropped;
substance in `skills/contract-repo.md` + `skills/component-triad.md`),
/253 (ToSemaOutcome two-trait shape), /247 (converge-vs-rethink verdict),
/143 (pivot to pilot), /237 (schema-as-tree investigation), /14 + /15
+ /16 (authority-chain corrections);
`intent/component-shape.nota` records 2026-05-20T02:00:00Z through
2026-05-20T15:00:00Z; `intent/persona.nota` 2026-05-19T15:30:00Z
(canonical authority chain) and 2026-05-20T15:00:00Z (spirit as
first pilot, spirit CLI replaces intent-log substrate).

## 0 · TL;DR

The lower-level infrastructure is settled and in code (`signal-frame
68891f60`, `signal-executor 66b5ee48`, `signal-sema a1715949`).
Persona-spirit is the canonical worked example
(`signal-persona-spirit a1909872`, `persona-spirit 6aeea3fd +
951603c3`) and the first pilot. Every other component migrates by
applying the same recipe.

The migration breaks into two independent passes per component:

- **Pass A — contract migration.** Update `signal-<component>` and
  `owner-signal-<component>` to contract-local verbs on the v4 macro
  grammar; drop the Sema-verb prefix; lift repeated-category-word
  siblings into parent enums; declare `observable` blocks with the
  new three-line shape.
- **Pass B — daemon migration.** Define the daemon's Layer-2
  `Command` + `ComponentEffect` enums; impl `ToSemaOperation` +
  `ToSemaOutcome`; impl `Lowering` with the four associated types;
  impl `CommandExecutor`; impl `BatchErrorClassification` on the
  engine error; impl `ObservedLowering` if the component is a
  persona component (so `Tap`/`Untap` is mandatory); wire the
  `Executor` at startup.

Sequencing across the persona ecosystem follows the canonical
authority chain `spirit → mind → orchestrate →
router/harness/terminal` with three carveouts: (1) spirit goes
first because it's the pilot and the workspace needs the substrate
replacement; (2) `owner-signal-persona-*` repos that are
intentionally missing (`mind` and `router` exist now; `harness`,
`message`, `auth` still deliberately absent) emerge as their
owner discipline crystallizes — don't backfill speculatively; (3)
`repository-ledger` migration is deferred but valid future pilot
work.

## 1 · The substrate (what's landed)

These commits define the architecture every component migrates onto.
Treat them as the version-pinned target.

| Crate | Commit | What it provides |
|---|---|---|
| `signal-sema` | `a1715949` (docs reframe) + `f4d3fe51` (functional landing) | Payloadless `SemaOperation` (6 variants); payloadless `SemaOutcome`; `SemaObservation { operation, outcome }`; `ToSemaOperation` + `ToSemaOutcome` traits with tests |
| `signal-frame` | `68891f60` + `fb53a6be` (`Partial` removed) | `Reply<Payload>` with `AcceptedOutcome { Committed, OperationAborted, BatchAborted }`; `SubReply { Ok, Invalidated, Failed { detail }, Skipped }`; `BatchFailureReason / RetryClassification / CommitStatus { NotCommitted, Unknown }`; `BatchErrorClassification` trait; `ObserverFanout` primitive; `observable` block grammar with mandatory `Tap`/`Untap` injection; `OperationReceived` / `EffectEmitted` event-pair names |
| `signal-executor` | `66b5ee48` + `47961d12` (Partial-free bump) | `Lowering` trait with `Operation / Reply / Command / ComponentEffect` associated types; `OperationPlan<Command>` + `BatchPlan<Command>` structural ownership; `CommandExecutor` trait per-daemon; `ObservedLowering: Lowering` extension trait; `Executor` orchestration; `RecordedEvent::{OperationReceived, EffectEmitted}` |
| `signal-persona-spirit` | `a1909872` + `2e7a69a0` (Partial-free bump) | First contract on the new macro grammar; observable event pair is `OperationReceived` / `EffectEmitted` |
| `persona-spirit` | `556bafcc` (thin CLI shape) + `6aeea3fd` + `951603c3` + `0f0a82be` (Partial-free bump) | First daemon implementing the full pattern: `SpiritCommand` + `SpiritEffect` enums, `ToSemaOperation` + `ToSemaOutcome` impls, `Lowering` + `CommandExecutor`, `Tap`/`Untap` with explicit no-change commands, constraint witnesses for unimplemented observer requests |

**Three discipline rules locked alongside the substrate (per
psyche affirmations 2026-05-20T15:00:00Z):**

- `BatchErrorClassification` is the canonical engine-error
  classification surface; daemons impl it on their engine error
  type rather than letting the executor hardcode classification
  constants.
- Every accepted operation lowers to `NonEmpty<Command>` — no-ops
  and idempotent applies lower to explicit named commands (e.g.,
  `RecordIdempotentApply { reason: AlreadyCurrent }`), not empty
  plans. The structural type (`NonEmpty`) already says this; named
  commands make semantics explicit and preserve introspection
  coverage.
- Observable event-pair is `OperationReceived` / `EffectEmitted`
  (no `Sema` prefix on the effect side because the typed event
  carries the component effect, not the universal Sema
  classification).

## 2 · The canonical pilot — persona-spirit

Persona-spirit is the worked example. Any component author reads
its code as the template, not the v3 examples in older designer
reports.

Read in this order:

1. **`signal-persona-spirit/src/lib.rs`** (commit `a1909872`) for
   the contract shape: contract-local operation verbs, observable
   block in the new three-line grammar, no Sema-verb prefixes on
   operations.
2. **`persona-spirit/src/lowering.rs`** for the `Lowering` impl
   with all four associated types; the explicit no-op commands
   (`Tap` lowers to a real command projecting as
   `SemaOperation::Subscribe + SemaOutcome::NoChange` while
   subscriptions aren't implemented; `Untap` lowers to a real
   command projecting as `SemaOperation::Retract +
   SemaOutcome::NoChange`).
3. **`persona-spirit/src/effect.rs`** for the `SpiritEffect` enum
   and `ToSemaOutcome` impl.
4. **`persona-spirit/src/executor.rs`** for the `CommandExecutor`
   impl against the daemon's tables.
5. **`persona-spirit/tests/`** for the constraint witnesses,
   especially
   `persona_spirit_unimplemented_observer_request_uses_reply_shaper_not_store`
   — the architectural-truth test that proves the unimplemented
   path goes through `ReplyShaper`, not `RecordStore`.

When implementing pass B on another component, mirror these files
structurally. Naming follows the per-component domain; shape
follows persona-spirit.

## 3 · Pass A — contract migration recipe

For each component's `signal-<component>` and
`owner-signal-<component>`:

### 3.1 — Switch the dependency

Bump from `signal-core` (the pre-/238 name) to `signal-frame`. If
the contract was on `signal-core` already with the SignalVerb-tagged
grammar, the macro will fail to compile after the bump; that's the
expected gate that drives the rest of this pass.

### 3.2 — Drop the Sema-verb prefix on operations

The pre-/238 grammar was `Match Query(Query)` / `Mutate
Configure(Configuration)`. The new grammar is `operation
Query(Query)` / `operation Configure(Configuration)` — contract-
local verbs only. The macro infers nothing from the verb name
about Sema lowering; that lives in the daemon's `Lowering` impl.

Specifically: replace `Mutate <Verb>(<Payload>)` with `operation
<Verb>(<Payload>)` and `Match <Verb>(<Payload>)` likewise. The
psyche-affirmed correction at 2026-05-19T19:30Z (intent log)
rejected the "verb-state-effect-label compromise" — public verbs
describe the client's action; database verbs (Assert/Match/etc.)
stay execution-layer.

### 3.3 — Lift repeated-category-word siblings into parent enums

When the contract has multiple sibling variants carrying the
same suffix (`*Query`, `*Listing`, `*Selection`, `*Order`), that
suffix is the schema asking for a parent type. Replace flat
siblings with a parent enum and a single root variant carrying
the parent as payload.

`signal-repository-ledger`'s pre-migration shape (the canonical
case study) has five `*Query` siblings on the request side and
five `*Listing` siblings on the reply side. The migration
collapses them to:

```rust
signal_channel! {
    channel Ledger {
        operation ReceiveHookNotification(ReceiveHookNotification),
        operation PushObservation(PushObservation),
        operation Query(Query),
    }
    reply Reply {
        EventRecorded(EventRecorded),
        QueryResult(QueryResult),
        RequestUnimplemented(RequestUnimplemented),
    }
}

pub enum Query {
    Events(EventSelection),
    RecentRepositories(RecentRepositorySelection),
    ChangedFiles(ChangedFileSelection),
    CommitMessages(CommitMessageSelection),
    Catalog(CatalogSelection),
}

pub enum QueryResult {
    Events(EventListing),
    RecentRepositories(RecentRepositoriesListing),
    ChangedFiles(ChangedFileListing),
    CommitMessages(CommitListing),
    Catalog(CatalogListing),
}
```

The threshold is behavioral, not numeric: when adding the third
sibling with the same suffix, stop and lift the parent.

### 3.4 — Drop redundant-ancestry prefixes on payload types

If types inside `signal-persona-spirit` carry an `Intent*` prefix
(the contract's domain), drop the prefix — the crate's namespace
supplies it. The pair-of-rules from ESSENCE §"Naming" requires both
(a) full English words and (b) no ancestry-restating. The pre-spirit-
migration list of 16 `Intent*` types collapses to bare names
(`Entry`, `Topic`, `Quote`, `Context`, `Timestamp`, etc.) inside
the spirit contract.

### 3.5 — Update the `observable` block (three lines)

The new grammar is exactly three lines plus the brace:

```rust
observable {
    filter <FilterType>;                 // or `filter default;`
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

No `open` / `close` lines — the macro injects `Tap(<FilterType>)`
and `Untap(<TokenType>)` automatically. If the contract's domain
verbs collide with `Tap`, rename the domain verb (not the
observability verb).

Use `EffectEmitted` (no `Sema` prefix) — the event carries the
typed component effect, not the universal Sema classification.

### 3.6 — Apply the reply discipline

Past-tense outcome variants (`Configured`, `EventRecorded`,
`Stated`); `*Rejected` for typed domain rejections that ride in
`SubReply::Failed.detail`; `RequestUnimplemented` (no contract
prefix) for the skeleton-honesty fallback.

### 3.7 — Round-trip test the rename

Every contract carries a round-trip test asserting the wire form
matches the contract-local verb name. The spirit contract's
`tests/round_trip.rs` checks that the encoded NOTA contains the
new verb names and explicitly does NOT contain `Mutate` or
`Match` prefixes. Mirror this test in every migrated contract.

## 4 · Pass B — daemon migration recipe

For each daemon implementing the contract:

### 4.1 — Bump signal-frame, signal-executor, signal-sema, and the contract dep

Use the locked commits from §1. `cargo update -p signal-frame -p
signal-frame-macros -p signal-executor -p signal-sema -p
signal-<component>` per /144's verification recipe.

### 4.2 — Define the Layer-2 `Command` enum

This is the daemon's own executable vocabulary. Each variant
carries the typed payload the engine needs (table identifier,
record, slot, read plan, etc.). The enum is component-local; the
contract doesn't see it.

Naming: `<Component>Command` enum; variants are imperative
domain verbs (`RecordEntry`, `ReadEntries`, `OpenObserver`,
`CheckProposalAgainstCurrent`, `RecordIdempotentApply`).

### 4.3 — Define the `ComponentEffect` enum

This is what the engine returns after executing a command.
Variants carry the typed result data (receipt, listing, token,
verdict).

Naming: `<Component>Effect` enum; variants are past-tense
outcomes mirroring the commands (`EntryRecorded`, `EntriesRead`,
`ObserverOpened`, `ProposalVerdict`, `IdempotentApplyRecorded`).

### 4.4 — Impl `ToSemaOperation` on `Command`

Each command projects to its Sema class. The match is mechanical:

```rust
impl ToSemaOperation for SpiritCommand {
    fn to_sema_operation(&self) -> SemaOperation {
        match self {
            Self::RecordEntry(_)        => SemaOperation::Assert,
            Self::ReadEntries(_)        => SemaOperation::Match,
            Self::OpenObserver(_)       => SemaOperation::Subscribe,
            Self::CloseObserver(_)      => SemaOperation::Retract,
            // ...
        }
    }
}
```

### 4.5 — Impl `ToSemaOutcome` on `ComponentEffect`

Symmetric — each effect projects to its Sema outcome:

```rust
impl ToSemaOutcome for SpiritEffect {
    fn to_sema_outcome(&self) -> SemaOutcome {
        match self {
            Self::EntryRecorded(_)      => SemaOutcome::Asserted,
            Self::EntriesRead(_)        => SemaOutcome::Matched,
            Self::ObserverOpened(_)     => SemaOutcome::Subscribed,
            Self::ObserverClosed(_)     => SemaOutcome::Retracted,
            Self::NoChange              => SemaOutcome::NoChange,
            // ...
        }
    }
}
```

`SemaOutcome::NoChange` is the right outcome for explicit-no-op
commands and validate-only paths.

### 4.6 — Impl `Lowering`

The four associated types are `Operation` (the contract operation
type), `Reply` (the contract reply type), `Command` (the daemon's
command enum from §4.2), `ComponentEffect` (the daemon's effect
enum from §4.3).

```rust
impl Lowering for SpiritLowering {
    type Operation = SpiritOperation;
    type Reply = SpiritReply;
    type Command = SpiritCommand;
    type ComponentEffect = SpiritEffect;

    fn lower(
        &self,
        operation: &SpiritOperation,
    ) -> Result<OperationPlan<SpiritCommand>, SpiritReply> {
        match operation {
            SpiritOperation::State(statement) => {
                if !self.psyche_policy.accepts(statement) {
                    return Err(SpiritReply::StateRejected(
                        StateRejectionReason::PolicyDenied,
                    ));
                }
                Ok(OperationPlan::single(
                    SpiritCommand::RecordEntry(statement.into_entry()),
                ))
            }
            // ...
        }
    }

    fn reply_from_effects(
        &self,
        operation: &SpiritOperation,
        effects: &OperationEffects<SpiritCommand, SpiritEffect>,
    ) -> SpiritReply {
        // match operation, build reply from effects
    }
}
```

Apply the no-op-as-explicit-command rule: validate-only operations
lower to explicit `CheckProposalAgainstCurrent` (not empty plans);
idempotent applies lower to `RecordIdempotentApply { reason }`
with `SemaOutcome::NoChange` projection.

### 4.7 — Impl `ObservedLowering` (if persona component)

Persona components must declare `observable`; that means the
daemon impls `ObservedLowering` (extension of `Lowering`) with
projection methods:

```rust
impl ObservedLowering for SpiritLowering {
    type OperationEvent = OperationReceived;
    type EffectEvent = EffectEmitted;

    fn project_operation(&self, op: &SpiritOperation) -> OperationReceived {
        OperationReceived::new(op.kind(), self.timestamp_source.now())
    }

    fn project_effect(&self, effect: &SpiritEffect) -> EffectEmitted {
        EffectEmitted::new(effect.kind(), effect.outcome().clone())
    }
}
```

Non-persona small utilities don't declare `observable` at all and
impl `Lowering` only.

### 4.8 — Impl `CommandExecutor`

Each daemon's executor knows its own tables/indexes:

```rust
impl CommandExecutor for SpiritExecutor {
    type Command = SpiritCommand;
    type ComponentEffect = SpiritEffect;
    type Error = SpiritEngineError;

    fn execute_atomic_batch(
        &mut self,
        plan: BatchPlan<SpiritCommand>,
    ) -> Result<BatchEffects<SpiritCommand, SpiritEffect>, SpiritEngineError> {
        // open redb transaction; execute each command; collect effects; commit
    }
}
```

### 4.9 — Impl `BatchErrorClassification` on the engine error

Bound: `CommandExecutor::Error: BatchErrorClassification`. The
engine error type self-classifies for the wire reply:

```rust
impl BatchErrorClassification for SpiritEngineError {
    fn batch_failure_reason(&self) -> BatchFailureReason {
        match self {
            Self::LockContention   => BatchFailureReason::EngineUnavailable,
            Self::ConstraintViolation => BatchFailureReason::EngineRejected,
            Self::PartialCommitRecovery => BatchFailureReason::EngineRejected,
            // ...
        }
    }

    fn retry_classification(&self) -> RetryClassification {
        match self {
            Self::LockContention   => RetryClassification::Retryable,
            Self::ConstraintViolation => RetryClassification::NotRetryable,
            Self::PartialCommitRecovery => RetryClassification::Unknown,
        }
    }

    fn commit_status(&self) -> CommitStatus {
        match self {
            Self::LockContention   => CommitStatus::NotCommitted,
            Self::ConstraintViolation => CommitStatus::NotCommitted,
            Self::PartialCommitRecovery => CommitStatus::Unknown,
        }
    }
}
```

Workspace-universal execution metadata flows through the wire;
the contract reply stays domain-typed.

### 4.10 — Wire the `Executor` at daemon startup

For persona components (observable mandatory):

```rust
let executor = Executor::observable(
    lowering,                       // impls ObservedLowering
    command_executor,               // impls CommandExecutor
    macro_generated_observer_set,   // impls ObserverFanout<OperationReceived, EffectEmitted>
);
```

For non-persona utilities:

```rust
let executor = Executor::new(lowering, command_executor);
```

### 4.11 — Update the CLI to two-socket dispatch

Per the six 2026-05-20T13:00:00Z CLI intent records, every CLI:
takes one of two argument shapes (raw NOTA starting with `(`, or
file path); is a pure NOTA↔Signal translation bridge; reads exactly
one env var (socket-path override, checked first); connects to two
sockets (working + policy) and dispatches by which contract the
incoming NOTA request belongs to.

The CLI binary name equals the daemon binary minus the `-daemon`
suffix: `mind-daemon` ↔ `mind`, `orchestrate-daemon` ↔
`orchestrate`, `spirit-daemon` ↔ `spirit`.

### 4.12 — Verify against the constraint witnesses

Mirror persona-spirit's constraint tests in the new daemon:

- Round-trip witness: operation in → typed reply out matches
  contract shape.
- Domain-rejection witness: invalid operation → `SubReply::Failed`
  with typed `detail`.
- Engine-failure witness: engine error → `BatchAborted` with
  classification metadata (not `Reply::Rejected`).
- Successful-commit witness: observer subscription sees
  `OperationReceived` before execution and `EffectEmitted` after.
- No-op witness: validate-only and idempotent paths use explicit
  commands and produce `SemaOutcome::NoChange`.
- Unimplemented witness: `Tap`/`Untap` (or any other unimplemented
  variant) returns through `ReplyShaper`, not the store.

Run `cargo test` + `nix flake check -L --max-jobs 0` to use the
remote builder per workspace discipline.

## 5 · Sequencing across the persona ecosystem

The canonical authority chain (`intent/persona.nota`
2026-05-19T15:30:00Z) is:

```text
engine-manager → spirit → mind → orchestrate → router / harness /
terminal
```

(Engine-manager is the name landed in /252 for what some surfaces
still call "the supervisor.")

Migration follows the chain with three carveouts:

### 5.1 — Persona-spirit first (the pilot)

In progress per /144 + /145. Spirit-CLI replaces the file-based
intent log is the major workspace direction; the pilot proves
the full pattern AND lands the substrate replacement.

Per /145 the immediate next pilot work is migrating
`owner-signal-persona-spirit` to `signal-frame` + contract-local
owner verbs, then updating the persona-spirit owner socket
handling to consume the migrated owner contract. Constraint
tests required: owner requests use verb-form heads; owner frames
rejected on ordinary socket; ordinary frames rejected on owner
socket; owner route still through `OwnerPlane`; bootstrap reload
still through `PolicyPlane`.

Pilot completion checklist (full):

- `owner-signal-persona-spirit` migrated to `signal-frame` with
  contract-local owner verbs (immediate next per /145).
- Persona-spirit owner socket handling consumes the migrated
  owner contract.
- Spirit accepts intent-record submission via CLI as a core
  operation; spirit's `Submit` (or equivalent) takes a
  `PsycheStatement` payload with the five-kind taxonomy
  (Decision/Principle/Correction/Clarification/Constraint).
- Spirit's query returns intent records by topic + filter.
- Round-trip witness end-to-end: CLI NOTA → frame → daemon →
  typed reply → CLI NOTA. Already covered by /145's verified
  baseline (`cargo test --locked` + `nix flake check -L --max-jobs 0`
  green across the four crates).
- Observer subscription witness: `Tap` → emit on submit
  (subscription event delivery is not yet implemented per /145;
  `Tap`/`Untap` produce `SemaOutcome::NoChange` placeholders
  through valid commands).
- Restart witness: durable state survives daemon restart.
- Import/cutover semantics from `intent/*.nota` (not yet
  designed; explicit psyche direction needed before starting).

### 5.2 — Persona-mind second

`signal-persona-mind` is the next contract to migrate. Current
shape (per /159):

- Still on `signal-core` with the old `Mutate <Verb>` grammar.
- Mega-`MindRequest` enum mixes three relations: typed mind-graph
  (thoughts + relations), work/memory graph, channel choreography.
- Channel-choreography variants (`ChannelGrant` / `ChannelExtend`
  / `ChannelRetract` / `AdjudicationDeny`) need to move OUT per
  /15's correction — these are outbound authority orders, not
  inbound mind operations. Destination: `owner-signal-persona-
  router` (already created in /160) with caller =
  Orchestrate (NOT Mind, per /15).

Mind migration is therefore a two-step pass:

1. **Split the mega-enum.** Tree the schema. Operation roots
   become `Submit(Submission)` / `Query(Query)` / `Watch(Watch)` /
   etc., with sum payloads carrying the relation-specific records.
   The repeated-category-words rule applies — don't flatten back
   into siblings.
2. **Migrate to v4 lower-level components.** Apply passes A + B
   per §3 + §4.

`owner-signal-persona-mind` exists already (per /159) with
`Configure(Configuration)` + `Inspect(Inspection)` on the v4
macro grammar. The `*Mode` suffix on the three Configuration
fields (per /14) should be dropped during the next contract edit.
Mind lifecycle verbs (`Start` / `Stop` / `Drain` / `Reload`) are
an open intent question (`intent/component-shape.nota`
2026-05-20T13:45:00Z, Minimum) — wait for psyche before adding.

### 5.3 — Persona-orchestrate grows Mind→Orchestrate cognitive verbs

Per /15 + /16, the authority chain `Mind → Orchestrate → Router`
requires `owner-signal-persona-orchestrate` to grow new verbs at
the cognitive level — not low-level Grant/Extend/Revoke (those
belong on `owner-signal-persona-router`). Open research question
per /16 §10:

- `AuthorizeChannel(ChannelAuthorization)` — Mind orders
  Orchestrate to authorize a channel for cognitive purpose;
  Orchestrate translates to Router-level `Grant`.
- `RetractChannelAuthorization(Token)` — symmetric.
- `SpawnAgent(AgentSpawnIntent)` — Mind orders Orchestrate to
  spawn an agent; Orchestrate decides spawn plan + harness
  orders.
- `EscalateBlockedWork(EscalationIntent)` — Mind override of
  routine work flow.

This is designer-lane research; operator-lane work waits on the
verb-set settling before implementing.

`signal-persona-orchestrate` itself also has residual `SemaEffect`
references per /144 §"Remaining Drift" — migrate when next
touched.

### 5.4 — Persona-router scaffold exists; Router daemon migration after orchestrate

`owner-signal-persona-router` has `Grant` / `Extend` / `Revoke` /
`Deny` per /160 (with caller correction: Orchestrate, not Mind).
The Router daemon's `Lowering` impl waits until
`owner-signal-persona-orchestrate` settles the cognitive verbs
it'll receive from Mind — payload shapes on the Router side
should reflect the Orchestrate-as-caller assumption per /15
("Anything that implicitly assumed Mind as caller… should be
Orchestrate-shaped — Orchestrate carries its own machinery
correlation").

### 5.5 — Persona-harness / message / terminal — emerge as their owner discipline crystallizes

Per `intent/component-shape.nota` 2026-05-19T20:30:00Z, the
missing `owner-signal-persona-harness`, `-message`, `-auth` repos
are intentionally missing. Don't backfill speculatively. Before
instantiating any of these, surface to psyche: "is now the time?"
per /15's process correction.

The working signals (`signal-persona-harness`,
`signal-persona-message`, `signal-persona-terminal`) still need
the v4 migration; they remain on the older grammar. Migrate when
each component is otherwise being touched.

### 5.6 — Persona-introspect waits for the universal-observer-hook
question

`/249` Gap #4 asks whether `Tap`/`Untap` IS the universal
observer-hook intent at 2026-05-19T20:00:00Z, or a separate
mechanism. Per /144 §"Effect On Higher Components" + /254, the
working assumption is yes — `Tap`/`Untap` is the universal hook.
But the psyche-clarification has not landed. Persona-introspect
doesn't migrate until the answer settles (designer-lane).

### 5.7 — Persona-system stays paused

Per persona/ARCH §0.7, persona-system is paused until a real
consumer surfaces. Skip during this migration arc.

### 5.8 — Repository-ledger deferred but valid future pilot

Per /143 + /247, repository-ledger was the originally-named
pilot, displaced by spirit per /254 §3.4. Future migration follows
the same recipe; the request-side tree-shape work from /237 + the
operator-assistant feedback at intent 2026-05-20T00:07:55+02:00
(symmetric reply-side `QueryResult(QueryResult)`) lands during
that migration.

## 6 · Per-component migration status table

| Component | Working signal | Owner signal | Daemon | Recipe stage |
|---|---|---|---|---|
| spirit | migrated (`a1909872`) | exists | migrated (`6aeea3fd`, `951603c3`) | finishing pilot (intent-record submission + CLI) |
| mind | OLD shape | exists, `Configure`/`Inspect` only | not migrated | next — passes A + B per §5.2 |
| orchestrate | residual `SemaEffect` per /144 | needs cognitive verbs (Mind→Orchestrate) | not migrated | wait on §5.3 designer work |
| router | unknown | exists, `Grant`/`Extend`/`Revoke`/`Deny` per /160 | not migrated | wait on orchestrate per §5.4 |
| harness | OLD shape (verify) | MISSING (deliberate) | OLD shape | passes A + B when otherwise touched; owner emerges later |
| message | OLD shape (verify) | MISSING (deliberate) | OLD shape | same |
| terminal | OLD shape (verify) | exists | OLD shape (verify) | passes A + B when otherwise touched |
| system | paused | MISSING (deliberate) | paused | wait |
| introspect | OLD shape | n/a | OLD shape | wait on §5.6 |
| auth | OLD shape (verify) | n/a (types-only) | n/a | refresh during next touch |
| repository-ledger | OLD shape | n/a today | not migrated | deferred valid pilot |

`exists` means a contract repo at the path; `MISSING (deliberate)`
means intent at 2026-05-19T20:30:00Z marks it intentionally missing
until owner discipline crystallizes.

## 7 · Open items

These open items affect implementation choices below the migration
recipe — surface them when they bite:

- **`CommitStatus::Partial`** — RESOLVED per /145. Removed in
  `signal-frame fb53a6be`; `execute_atomic_batch` is all-or-nothing
  so `Partial` contradicted the contract. The shape is now
  `CommitStatus { NotCommitted, Unknown }`. If a future non-atomic
  executor lands, adding `Partial` back is a deliberate compile-
  error fan-out with real semantics. Operator's Q1 from /144
  closes.
- **Tap/Untap before vs after spirit's intent-log substrate
  replacement** (operator Q3 from /144). The current implementation
  uses `NoChange`-projecting placeholders for `Tap`/`Untap`; the
  workspace direction (per /254 §3.5) is spirit replaces intent-log
  ASAP. Whether observer support must precede the substrate cutover
  is a sequencing question, not a recipe question.
- **`signal-persona-orchestrate` immediate vs deferred** (operator
  Q4 from /144). The /144 verification skipped orchestrate's
  residual `SemaEffect`; depending on when orchestrate is next
  touched, this falls into §5.3 or deferred-migration.
- **`EffectEmitted` mandatory vs default** (operator Q5 from /144).
  The macro emits it by default; whether contracts can rename is
  open. Designer call.
- **Mind lifecycle on owner contract vs out-of-band** (intent
  2026-05-20T13:45:00Z Minimum). Affects `owner-signal-persona-
  mind`'s eventual verb set; today it's `Configure` + `Inspect`
  only.
- **`owner-signal-persona-orchestrate` cognitive verb set** (per
  /16). Open research question; gates Mind migration's
  channel-choreography move (§5.3).

## 8 · What to read; what to ignore

The substrate is settled; older designer reports describing pre-v4
shapes are historical residue:

**Authoritative (read):** /144, /248, /252, /253, /254 — and the
landed code in the five commits per §1.

**Historical (do not implement literally):**
- /245 — pre-v4 design alternatives; superseded.
- /246-v1 / v2 / v3 — interim spec revisions; v4 is canonical and
  superseded too once /144 + /253 + /254 absorbed. Per /145, the
  `CommitStatus::Partial` example in /246-v4 is now stale —
  `Partial` was removed in `fb53a6be`.
- /141 — early correction examples; absorbed into /246 + /144.
- /140 — predecessor hole analysis.
- /239 / /241 — pre-three-layer migration plan + guide.
- /143 / /247 — pivot rationale (still useful as design context;
  pilot-target affirmation in /254 supersedes the literal
  repository-ledger-as-first-pilot choice).
- /237 §5 — proposed skill edits that haven't landed (the
  underlying principles are still load-bearing; the proposed
  edits should be revisited in pair with the report 11
  guideline).
- /248 — three-layer-changes-for-operators; substance is
  current except the `CommitStatus::Partial` example per /145.

## 9 · References

### Code substrate (read these)

- `signal-sema a1715949` — payloadless Sema + projection traits.
- `signal-frame 68891f60` — wire types + `BatchErrorClassification` + macro.
- `signal-executor 66b5ee48` — `Lowering` + `CommandExecutor` + `Executor` orchestration.
- `signal-persona-spirit a1909872` — first migrated contract.
- `persona-spirit 6aeea3fd` + `951603c3` — first migrated daemon.

### Designer / operator reports

- `reports/operator/144-signal-sema-executor-refresh-2026-05-20.md` — the landed-state report.
- `reports/operator/145-signal-sema-spirit-current-handoff-2026-05-20.md` — current operator handoff naming the spirit-pilot's immediate-next work (owner-signal-persona-spirit migration), `CommitStatus::Partial` removal, the consumer-bump commits, and the four open psyche questions.
- `reports/designer/254-signal-executor-sema-refresh-audit.md` — operator-facing direction with five affirmed gaps.
- `reports/designer/253-tosemaoutcome-trait-shape.md` — two-trait shape.
- `reports/designer/251-supervisor-identity-disambiguation.md` — disambiguation analysis.
- `reports/designer/237-signal-type-naming-and-schema-tree-investigation.md` — naming/schema-tree principles (proposed but unlanded).
- `reports/operator-assistant/159-persona-mind-signal-tree-owner-contract-vision.md` — Mind contract refactor proposal.
- `reports/operator-assistant/160-owner-signal-persona-router-channel-authority.md` — router policy contract.
- `reports/second-designer-assistant/14-audit-of-operator-assistant-159-owner-signal-persona-mind.md` — Mind audit + auth-chain disambiguation.
- `reports/second-designer-assistant/15-clarification-for-operator-assistant-on-orchestrate-router-authority.md` — Mind→Orchestrate→Router correction.
- `reports/second-designer-assistant/16-mind-orchestrate-boundary-research-mind-body-analogy.md` — cognitive vs mechanical seam research.
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md` — sibling guideline report.

### Intent records (canonical)

- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer model affirmation.
- `intent/component-shape.nota` 2026-05-20T13:00:00Z — six CLI-design records.
- `intent/component-shape.nota` 2026-05-20T13:30:00Z — Mind/Orchestrate/Router authority correction.
- `intent/component-shape.nota` 2026-05-20T13:45:00Z — mind/body analogy + Mind lifecycle open question.
- `intent/component-shape.nota` 2026-05-20T15:00:00Z — `BatchErrorClassification`, `OperationReceived`/`EffectEmitted`, no-op-as-explicit-command affirmations.
- `intent/persona.nota` 2026-05-19T15:30:00Z — canonical authority chain.
- `intent/persona.nota` 2026-05-20T15:00:00Z — spirit-first pilot + spirit CLI replaces intent-log substrate.

### Skills (apply during the migration)

- `skills/component-triad.md` — daemon + working signal + policy signal triad shape.
- `skills/contract-repo.md` — wire-contract crate discipline (reply discipline § codified at `a7f3a0ee`).
- `skills/naming.md` — full English words + no ancestry restating.
- `skills/language-design.md` — closed enums; structural beauty.
- `skills/jj.md` — version control.
- `skills/testing.md` — Nix-backed test surfaces; `--max-jobs 0`.

This report retires when (a) every persona-component contract in
§6's table is on v4 with passes A + B applied, OR (b) a successor
migration report subsumes it. Whichever sooner.
