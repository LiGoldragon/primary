# 130 — persona-mind triad audit

*Audit of the persona-mind triad: `signal-persona-mind` (working
contract) + `owner-signal-persona-mind` (policy contract) +
`persona-mind` (daemon with bundled thin CLI `mind`). Mind is the
worst-shaped remaining Persona contract per
`reports/operator/150-triad-signal-sema-migration-current-state.md`
§6.1; this audit confirms the extent.*

## 0 · TL;DR

The working contract is the most stale and worst-shaped contract in
the workspace: still on `signal-core`, still on universal-verb
shape, fifteen flat request variants, four redundant repeated-suffix
families, no observable block, doubling smells (`Match
Query(Query)`), grammatically wrong `Mutate StatusChange(StatusChange)`,
and a stale closed `RoleName` enum. The owner contract is on
`signal-frame` and cleaner but still violates several macro-target
patterns. The daemon does not depend on `signal-executor`, runs its
own bespoke `MindFrameCodec` over `signal-core` types, and the `mind`
binary uses argparse flags (`--socket`, `--store`, `--actor`,
`daemon` subcommand) — a hard single-argument-rule violation per
`intent/component-shape.nota` 2026-05-19T01:23:00Z and
`skills/component-triad.md` §"The single argument rule".

Priority for migration slice: (1) restructure the working contract
to contract-local verbs with lifted `Submission` / `Receipt` /
`Query` sums per psyche's directed shape (§2.1); (2) rewrite the
`mind` binary to the single-NOTA-argument shape (§2.2); (3)
swap the daemon onto `signal-executor` (§2.3); (4) add the
observable block (§2.4); the smaller cleanups absorb into these.

## 1 · /257 findings status

For each /257 finding that applies to persona-mind, with file:line
evidence:

### /257 §1.1 — old universal-verb shape

**Status: NOT FIXED.** `signal-persona-mind/src/lib.rs:1382-1400`:

```text
1385  Assert SubmitThought(SubmitThought),
1386  Assert SubmitRelation(SubmitRelation),
1387  Match  QueryThoughts(QueryThoughts),
1388  Match  QueryRelations(QueryRelations),
1389  Subscribe SubscribeThoughts(SubscribeThoughts) opens MindEventStream,
1390  Subscribe SubscribeRelations(SubscribeRelations) opens MindEventStream,
1391  Retract SubscriptionRetraction(SubscriptionId),
1392  Assert Opening(Opening),
1393  Assert NoteSubmission(NoteSubmission),
1394  Assert Link(Link),
1395  Mutate StatusChange(StatusChange),
1396  Assert AliasAssignment(AliasAssignment),
1397  Match  Query(Query),
1398  Assert AdjudicationRequest(AdjudicationRequest),
1399  Match  ChannelList(ChannelList),
```

Every variant is universal-verb-prefixed. The new
`operation Verb(Payload)` grammar from
`intent/component-shape.nota` 2026-05-19T19:30:00Z and
2026-05-20T02:00:00Z is not used.

### /257 §1.2 — doubling smell

**Status: NOT FIXED.** Two instances:

- `signal-persona-mind/src/lib.rs:1397` — `Match Query(Query)`.
  Exact psyche quote: *"match query query, but that is fucking ugly
  as fuck"* (`intent/component-shape.nota` 2026-05-19T19:30:00Z).
- `signal-persona-mind/src/lib.rs:1399` — `Match
  ChannelList(ChannelList)`.

### /257 §1.3 — `Mutate <Verb>` grammatically wrong

**Status: NOT FIXED.** `signal-persona-mind/src/lib.rs:1395`:

```text
Mutate StatusChange(StatusChange)
```

`StatusChange` is verb-form (act of changing status), so this reads
as "mutate a status-change" — incoherent per
`intent/component-shape.nota` 2026-05-19T19:30:00Z (*"you mutate a
noun, you don't mutate a verb"*).

### /257 §1.4 — repeated-suffix smell

**Status: NOT FIXED. THE WORST IN THE WORKSPACE.** Four overlapping
families in this contract:

**Submit\* family** (`signal-persona-mind/src/lib.rs:1385-1396`):
`SubmitThought`, `SubmitRelation`, `Opening`, `NoteSubmission`,
`Link`, `StatusChange`, `AliasAssignment`, `AdjudicationRequest` —
eight semantically-Submit-shaped operations, two with literal
`Submit*` prefix.

**Query\* / Subscribe\* parallel family**
(`signal-persona-mind/src/lib.rs:1387-1390`): `QueryThoughts`,
`QueryRelations`; `SubscribeThoughts`, `SubscribeRelations`. Two
classes of plural-suffixed siblings.

**\*Receipt family** (`signal-persona-mind/src/lib.rs:1408-1412`):
`OpeningReceipt`, `NoteReceipt`, `LinkReceipt`, `StatusReceipt`,
`AliasReceipt` — five `*Receipt` siblings. Plus `*Committed` family
on the same reply: `ThoughtCommitted`, `RelationCommitted`. Plus
`*List` family: `ThoughtList`, `RelationList`. Plus `View`,
`Rejection`, `AdjudicationReceipt`, `ChannelListView`,
`SubscriptionAccepted`, `SubscriptionRetracted`,
`MindRequestUnimplemented` — total of 16 flat reply variants.

Per `intent/component-shape.nota` 2026-05-20T00:07:55+02:00 (the
canonical ledger correction) and
`reports/second-operator-assistant/11` §2, all of these want
lifting into typed sums (`Submission`, `Query`, `Subscription`,
`Receipt`, etc.) — symmetric on the request and reply sides.

### /257 §1.5 — ancestry-prefixed type names

**Status: MIXED.**

- `Mind` prefix on macro-emitted types
  (`signal-persona-mind/src/lib.rs:1383, 1401, 1417, 1419, 1422`):
  `MindRequest`, `MindReply`, `MindEvent`, `MindEventStream`,
  `MindRequestUnimplemented`, `MindUnimplementedReason`,
  `MindOperationKind`, `MindDelta`, `MindSnapshot`. Closes once
  bead `primary-77hh` (drop channel-name prefix from macro) lands
  and the macro target from /150 §1.1 is consumed.
- Domain types are mostly clean — `Item`, `Note`, `Edge`, `View`,
  `Title`, `TextBody`, `Opening`, `Link`, `StatusChange`,
  `AliasAssignment`, `Query`, `ChannelEndpoint`, `ChannelMessageKind`,
  `ChannelDuration`, `ChannelFilter`, `ChannelList`, `ChannelView`,
  `ChannelListView`, `AdjudicationRequest`, `AdjudicationReceipt`,
  `Thought`, `Relation` (in `graph.rs`). Good ✓
- `AdjudicationRequestId` (`signal-persona-mind/src/lib.rs:1135`) —
  the type is just an identifier under the `Adjudication` domain;
  the full ancestry name reads heavy. Same /257 §2 finding flagged
  for `owner-signal-persona-router::AdjudicationRequestIdentifier`.
- `RoleName` (`signal-persona-mind/src/lib.rs:67-127`) — `Name` is
  redundant. `Role` works as the bare name; the context is the
  domain noun. (Also fundamentally stale; see §2.7 below.)

### /257 §1.6 — `*RequestUnimplemented { operation, reason }`

**Status: ALREADY CLEAN on the request side.**
`signal-persona-mind/src/graph.rs:910-913`:

```rust
pub struct MindRequestUnimplemented {
    pub reason: MindUnimplementedReason,
}
```

Only `reason`. ✓

**Status: NOT FIXED on the owner side.**
`owner-signal-persona-mind/src/lib.rs:131-134`:

```rust
pub struct RequestUnimplemented {
    pub operation: OperationKind,
    pub reason: UnimplementedReason,
}
```

The `operation` field is redundant per
`reports/operator/150-triad-signal-sema-migration-current-state.md`
§3 ("RequestUnimplemented carries the reason only"). Drop
`operation`. Then drop the `OperationKind` enum itself (it exists
only to feed this field) — though that enum is currently emittable
by the macro (per /257 §3.1's bead) so it'll move anyway.

### /257 §1.7 — empty marker records

**Status: NOT PRESENT.** No empty struct payloads observed.

### /257 §1.9 — single-variant enums

**Status: NOT PRESENT.** No speculative single-variant enums; the
sums all have ≥2 variants today.

### /257 §1.10 — frame type alias boilerplate

**Status: NOT FIXED (cross-workspace bead `primary-77hh`).**
Working contract has no manual alias dance because the macro emits
`Mind*`-prefixed names that nothing in the contract crate aliases
away. Owner contract has the full dance —
`owner-signal-persona-mind/src/lib.rs:149-154`:

```rust
pub type OwnerMindRequest = OwnerMindOperation;
pub type Frame = OwnerMindFrame;
pub type FrameBody = OwnerMindFrameBody;
pub type ChannelRequest = OwnerMindChannelRequest;
pub type ChannelReply = OwnerMindChannelReply;
pub type RequestBuilder = OwnerMindRequestBuilder;
```

Five aliases plus the `OwnerMindRequest = OwnerMindOperation`
post-three-layer compat alias. Both retire when the macro emits
unprefixed names by default
(`intent/component-shape.nota` 2026-05-21T10:30:00Z — modules-not-
options).

### /257 §1.11 — no observable block

**Status: NOT FIXED.** Neither contract declares an `observable
{ ... }` block. Per `intent/component-shape.nota`
2026-05-20T02:00:00Z (*"Tap/Untap is mandatory for persona
components, no author override"*) and `intent/persona.nota`
2026-05-21T10:00:00Z (*"debug the debugger"*), Mind is a persona
component and must support Tap/Untap on its working socket.

Required addition on
`signal-persona-mind/src/lib.rs` inside the channel block:

```text
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

Per `intent/persona.nota` 2026-05-20T20:00:00Z, live fanout is
deferred until persona-introspect lands; until then Tap/Untap
return RequestUnimplemented / SemaOutcome::NoChange. The contract
declaration is still mandatory — the placeholder behaviour lives
in the daemon, not in the contract.

### /257 §1.12 — single-field timestamps (and excess precision)

**Status: NOT FIXED.** `signal-persona-mind/src/lib.rs:346-356`
defines `pub struct TimestampNanos(u64);` and uses it for
`occurred_at` on every receipt
(`graph.rs:854, 860`), for `ChannelDuration::TimeBound`
(`lib.rs:1216`), and for `ByThoughtTimeRange.start`/`end`
(`graph.rs:797-798`).

Per `intent/persona.nota` 2026-05-20T18:44:49+02:00 (*"seriously,
fuck nanoseconds - fucking ridiculous"*), nanosecond precision is
suspect at every protocol surface. Spirit moved to seconds.
**Open question** (carry as a Q for psyche): are mind work-graph
event timestamps a runtime stamping (single-field) or intent
records (two-field per workspace.nota 2026-05-19 18:30)? Mind is
not the intent log; spirit owns that. So single-field seconds is
the safer bet; confirm.

### /257 §1.13 — `supervision::` namespace stale

**Status: NOT FIXED here, BUT not Mind's call.** The
`supervision::` references in `persona-mind/src/supervision.rs:12-17`
come from the `signal-persona` crate (the engine-manager
contract). Mind imports them as a downstream consumer:

```rust
use signal_persona::{
    ComponentHealth, ComponentHealthQuery, ComponentHealthReport, ...
    GracefulStopAcknowledgement, SupervisionFrame, SupervisionFrameBody, ...
    SupervisionProtocolVersion, SupervisionReply, SupervisionRequest,
};
```

The /252 engine-management rename of these types
(`intent/persona.nota` 2026-05-20T14:30:00Z + 14:50:00Z) propagates
into this file when signal-persona executes the rename; the
mechanical edit here is `s/Supervision/EngineManagement/g` plus
the file rename `supervision.rs` → `engine_management.rs`. Not
Mind's design call.

### Three building-block beads from /257 §3 — coverage

- **`primary-77hh`** (drop channel-name prefix from macro) — would
  affect both the working contract (`MindFrame` etc.) and the owner
  contract's alias dance.
- **`primary-k3bu`** (UnknownKindForVerb rename) —
  `signal-persona-mind/src/lib.rs` has 5 sites of
  `Error::UnknownKindForVerb` (lines 206, 671, 741, 789, 836,
  990, 1186, 1259, 1358) across the hand-written codec impls;
  `graph.rs` has more (lines 142+). All hand-written codecs.
- **`primary-u0lh`** (extend nota-codec derive coverage) — every
  one of those hand-written impls is structurally derivable.
  `signal-persona-mind/src/lib.rs` has 8 hand-written
  `impl NotaEncode/NotaDecode` blocks; `graph.rs` has more
  (`MindUnimplementedReason` at lines 942 and 967, plus the various
  sum types).

## 2 · New findings specific to this triad

### 2.1 — broad flat operation tree must split

The fifteen-variant request enum
(`signal-persona-mind/src/lib.rs:1383-1400`) mixes four logical
planes under one channel:

1. **Mind graph plane** — submit/query/subscribe typed
   Thought/Relation records (`SubmitThought`, `SubmitRelation`,
   `QueryThoughts`, `QueryRelations`, `SubscribeThoughts`,
   `SubscribeRelations`, `SubscriptionRetraction`).
2. **Work memory plane** — work-item lifecycle (`Opening`,
   `NoteSubmission`, `Link`, `StatusChange`, `AliasAssignment`,
   `Query`).
3. **Channel choreography plane** — adjudication
   (`AdjudicationRequest`, `ChannelList`).
4. **Subscription plumbing plane** — `SubscriptionRetraction`.

The agreed target shape per
`reports/operator/150-triad-signal-sema-migration-current-state.md`
§6.1 + `reports/designer/257-signal-contracts-names-and-shape-audit.md`
§2 (`signal-persona-mind` worked example) collapses to ~7 root
verbs:

```text
operation Submit(Submission)              -- typed sum across all submit-shaped ops
operation Query(Query)                    -- typed sum across all read-shaped ops
operation Watch(Subscription) opens DomainStream
operation Unwatch(SubscriptionToken)
operation ChangeStatus(StatusTransition)  -- or operation Transition
operation Adjudicate(AdjudicationRequest)
operation ListChannels(ChannelFilter)
```

`Submission` becomes the typed sum:

```text
Submission ::= Thought(Thought)
            | Relation(Relation)
            | Opening(Opening)
            | Note(NoteSubmission)
            | Link(Link)
            | Alias(AliasAssignment)
```

`Query` becomes the typed sum across both work-memory and graph
read targets (or, if the planes are truly distinct, split into a
work `Query` and a mind-graph `Query` under different operation
roots — a design call worth surfacing).

**Open psyche question**: is the mind-graph plane (typed
Thought/Relation) genuinely the same logical contract as the work
memory plane (Item/Note/Edge), or are they two separate planes
that historically share one channel? The contract's surrounding
prose
(`signal-persona-mind/src/lib.rs:1-19`) frames them as two parallel
substrates. If they are two planes, the right shape may be two
channels in one crate using the module disambiguation from
`intent/component-shape.nota` 2026-05-21T10:30:00Z:

```text
pub mod graph {
    signal_channel! { channel Graph { operation Submit(...), Query(...), ... } observable { ... } }
}
pub mod memory {
    signal_channel! { channel Memory { operation Submit(...), Query(...), ... } observable { ... } }
}
```

Designer lean: one channel with lifted sums is simpler and the
graph/memory split inside `Submission` / `Query` reads cleanly.
But the two-channel option is the one that lets each plane carry
its own filter shape and observability surface. **Confirm with
psyche.**

### 2.2 — `mind` binary is not the workspace-universal thin CLI

`persona-mind/src/main.rs:1-6`:

```rust
use persona_mind::{MindCommand, Result};

#[tokio::main]
async fn main() -> Result<()> {
    MindCommand::from_env().run(std::io::stdout().lock()).await
}
```

`MindCommand::into_action`
(`persona-mind/src/command.rs:40-53`) accepts a `daemon` subcommand
keyword, then `MindCommand` parses `--socket`, `--store`, `--actor`
flags via a full `OptionParser`
(`persona-mind/src/command.rs:224-283`). Five error variants live
in `error.rs:53-75`:

```text
MissingCommandInput
UnknownCommandLineOption
MissingCommandLineOptionValue
InvalidCommandLineArgument
MissingSocketPath
MissingActorName
MissingStorePath
WrongRequestArgumentCount
```

**This violates the workspace's single-argument rule with maximum
force.** Per `intent/component-shape.nota` 2026-05-19T01:23:00Z
(*"we never ever use things like command line flags"*) and the
narrowed CLI rule at 2026-05-20T13:00:00Z + 13:00:30Z (*"The CLI
only takes two kinds of arguments... a NOTA string that starts
with `(` ... or it's a file path"*) and the constraint at
2026-05-20 21:53 (*"the CLI doesn't do anything, it's just a thin
client to speak the signal"*).

Compounding violations:

- `mind` is **both** the CLI and the daemon entry point through a
  subcommand keyword. Per
  `intent/component-shape.nota` 2026-05-20T13:00:00Z, the daemon
  binary is `mind-daemon` and the CLI is `mind`; these are two
  separate binaries.
- The CLI takes `--actor` to attach caller identity from argv.
  That is mechanical infrastructure work that does not belong in
  the CLI surface; agent identity comes from socket auth or
  envelope construction, not from a user-supplied flag (per
  `intent/component-shape.nota` 2026-05-20 21:53: *"No request
  payload mints authority. Actor identity ... are
  infrastructure/store concerns."* Mind's own ARCH says this at
  `ARCHITECTURE.md:130-131`, then violates it in `command.rs:253`).
- The CLI takes `--socket` and `--store` as flags. Socket-path
  override is allowed but only via env var per
  `intent/component-shape.nota` 2026-05-20T13:00:00Z (*"the CLI is
  the only place where we allow the use of an environment variable
  to make it easy for testing"*); store is daemon-only state and
  has no business being on the CLI.
- The CLI does not use the generated signal-CLI dispatch macro
  from `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`.
  Working/policy dispatch is not implemented at all — the CLI
  speaks only to the working socket.

Target shape (`persona-mind/src/main.rs` + a separate
`persona-mind/src/bin/mind-daemon.rs`):

```text
// mind.rs  (CLI; minimal — one NOTA argument, dispatch via macro)
signal_frame::signal_cli! {
    cli mind;
    working signal_persona_mind::Operation;       // post-rename
    policy  owner_signal_persona_mind::Operation;
    socket  "persona-mind";
}

// mind-daemon.rs  (daemon; reads NOTA config record)
fn main() -> Result<()> { MindDaemonConfig::from_argv()?.run() }
```

This is the largest single piece of rework in the triad.

### 2.3 — daemon does not use `signal-executor`

`persona-mind/Cargo.toml` has no `signal-executor` dependency. The
daemon runs its own framing path via
`persona-mind/src/transport.rs:5` (uses `signal_core::*`,
`MindFrameCodec`, `synthetic_exchange`, hand-rolled Reply
construction in `transport.rs:132-140`).

Same gap /255 surfaced for spirit pre-migration; spirit has been
migrated; mind has not. Per
`intent/component-shape.nota` 2026-05-20T02:00:00Z + 15:00:00Z and
`reports/operator/150-triad-signal-sema-migration-current-state.md`
§1.4/§7, the daemon should:

```text
struct MindLowering { ... }
impl Lowering for MindLowering {
    type Operation = Operation;          // post-rename, no Mind prefix
    type Reply = Reply;
    type Command = MindCommand;          // local enum
    type ComponentEffect = MindEffect;    // local enum
}
impl CommandExecutor for MindCommandExecutor { ... }
impl ToSemaOperation for MindCommand { ... }
impl ToSemaOutcome for MindEffect { ... }
impl BatchErrorClassification for MindError { ... }
```

Then `signal_executor::Executor::execute(request)` replaces the
current `serve_next` body
(`persona-mind/src/transport.rs:286-312`).

Naming collision watch: today the runtime crate has a
`MindCommand` type for argv parsing
(`persona-mind/src/command.rs:13-16`). That name is taken by the
ergonomic Layer-2 enum
(`MindCommand::RecordItem`, `MindCommand::OpenSubscription`,
etc.). The argv struct retires when the CLI is rewritten per §2.2,
so the name frees up.

### 2.4 — neither contract is observable

(Same as /257 §1.11 but stating the destination shape.) After the
operation tree splits per §2.1, the channel needs:

```text
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

This applies to the working contract. **Open psyche question**:
should the owner contract (`owner-signal-persona-mind`) also
declare an observable block? Spirit's owner contract did not;
`reports/designer/258-persona-signal-triad-audit-2026-05-21.md`
§2.3 designer-lean was to skip the policy/owner channel and add
observable only on the working surface. Apply the same lean here;
confirm.

### 2.5 — Mind→Router authority verbs have been removed (CORRECTLY)

The contract used to carry `ChannelGrant`, `ChannelExtend`,
`ChannelRetract`, `AdjudicationDeny` as Mind-inbound request
variants. Per
`intent/component-shape.nota` 2026-05-20T13:09:13Z (Decision:
*"Mind-to-Router channel authority orders move out of
signal-persona-mind and into owner-signal-persona-router"*) and the
2026-05-20T13:30:00Z Correction (the orchestrate-owns-router
revision: chain is Mind → Orchestrate → Router, not Mind → Router),
those variants must NOT exist on Mind's contract.

**Verified GONE:** the working contract at
`signal-persona-mind/src/lib.rs:1383-1400` has no `ChannelGrant`,
`ChannelExtend`, `ChannelRetract`, or `AdjudicationDeny` variants
in `MindRequest`. ✓ The last commit on local (`859f803`,
*"signal-persona-mind: route router authority through orchestrate"*)
is the rename that removed them.

**However:** the daemon still pattern-matches on those gone
variants —
`persona-mind/src/actors/dispatch.rs:92-98`:

```rust
MindRequest::AdjudicationRequest(_)
| MindRequest::ChannelGrant(_)
| MindRequest::ChannelExtend(_)
| MindRequest::ChannelRetract(_)
| MindRequest::AdjudicationDeny(_)
| MindRequest::ChannelList(_)
| MindRequest::SubscriptionRetraction(_) => self.unimplemented(trace),
```

This compiles only because `persona-mind/Cargo.toml` pins
`signal-persona-mind = { ... }` against an older revision
(`115eb908`, on the `main` branch as it was before the
authority-removal commit). The daemon's view of the contract is
older than the local working tree. The fix is mechanical: refresh
the git rev in `persona-mind/Cargo.toml`, drop the four gone
pattern arms; the remaining `MindRequest::AdjudicationRequest /
ChannelList / SubscriptionRetraction` are still valid match arms.

This is a transitional pinning drift, not a design issue, but it
will surface as a compile break the moment the pin is refreshed —
note as a sub-step of any migration slice.

### 2.6 — `RoleName` is a stale closed enum

`signal-persona-mind/src/lib.rs:67-127` defines a closed enum of
eleven role names — `Operator, OperatorAssistant,
SecondOperatorAssistant, Designer, DesignerAssistant,
SecondDesignerAssistant, SystemSpecialist, SystemAssistant,
SecondSystemAssistant, Poet, PoetAssistant` — with a hand-written
wire-token table and three impl blocks.

Per `intent/persona.nota` 2026-05-19T15:04:19Z (Decision: roles
are dynamic, named by the work) and 2026-05-19 21:45 (Decision:
beads do not get role labels; agents can pick up any bead) and
`reports/designer/257-signal-contracts-names-and-shape-audit.md`
§2 (signal-persona-mind: *"Stale `RoleName` enum (lines 67-127) —
should align with signal-persona-orchestrate's dynamic
`RoleIdentifier` (String)"*), this enum is the wrong shape and
the wrong owner.

Fix:
- Drop the enum from `signal-persona-mind`.
- Import `RoleIdentifier` (or rename to `Role` per the
  no-ancestry rule — *role* already is the noun) from
  `signal-persona-orchestrate` if mind needs to refer to a role at
  all.
- If mind does NOT need a typed role surface (now that role
  identity lives in orchestrate), drop the import entirely.

The dead `RoleName::ALL` array
(`signal-persona-mind/src/lib.rs:82-94`) and the lookup helpers
also retire.

### 2.7 — daemon reads env vars for runtime configuration

`persona-mind/src/transport.rs:64-69`:

```rust
pub fn from_environment() -> Option<Self> {
    std::env::var("PERSONA_SOCKET_MODE")
        .ok()
        .and_then(|value| u32::from_str_radix(value.as_str(), 8).ok())
        .map(Self::new)
}
```

`persona-mind/src/supervision.rs:80-88`:

```rust
pub fn from_environment(_profile: SupervisionProfile) -> Option<Self> {
    let socket = std::env::var_os("PERSONA_SUPERVISION_SOCKET_PATH")?;
    let mode = std::env::var("PERSONA_SUPERVISION_SOCKET_MODE")
        .ok()
        ...
}
```

Per `intent/component-shape.nota` 2026-05-20T13:00:00Z (*"Daemons
never read environment variables; all daemon configuration is
NOTA"*), the daemon must not read env vars. These socket-path
and socket-mode values belong on the daemon's NOTA config record
(per `skills/component-triad.md` §"The single argument rule" —
daemons take a NOTA config record or signal-encoded config file).

The CLI env-var carve-out (socket-path override) applies only to
the CLI surface, not to the daemon.

### 2.8 — `GracefulStopAcknowledgement` propagates the engine-manager smell

`persona-mind/src/supervision.rs:15` imports
`GracefulStopAcknowledgement` from `signal-persona`. Per
`reports/designer/258-persona-signal-triad-audit-2026-05-21.md`
§2.1, the `Graceful` prefix is redundant and the engine-manager
contract should rename it to `StopAcknowledgement`. That rename
propagates through every supervised daemon's supervision-import
line — Mind's is one of them. Not Mind's design call; flag for
the engine-manager rename pass.

### 2.9 — `signal-persona-auth::ChannelId` vs Mind-local
`SubscriptionId` / `AdjudicationRequestId` / etc.

The contract imports `ChannelId, ComponentName, ConnectionClass,
MessageOrigin` from `signal-persona-auth`
(`signal-persona-mind/src/lib.rs:27`) ✓. But Mind also mints its
own opaque identifiers:

- `StableItemId(String)` (`lib.rs:363`)
- `DisplayId(String)` (`lib.rs:378`)
- `ExternalAlias(String)` (`lib.rs:393`)
- `BeadsToken(String)` (`lib.rs:408`)
- `OperationId(String)` (`lib.rs:423`)
- `ActorName(String)` (`lib.rs:438`)
- `EventSeq(u64)` (`lib.rs:462`)
- `SubscriptionId(String)` (`graph.rs:42`)
- `AlternativeId(String)` (`graph.rs:57`)
- `RecordId(String)` (`graph.rs:12`)
- `RelationId(String)` (`graph.rs:27`)
- `AdjudicationRequestId(String)` (`lib.rs:1135`)
- `HarnessId(String)` (`graph.rs:132`)

Thirteen newtype identifier wrappers. Per psyche
`intent/naming.nota` 2026-05-19T18:20:00Z (*"identifier is always
better than id"*) every `*Id` needs to expand: `StableItemId →
StableItemIdentifier`, `SubscriptionId →
SubscriptionIdentifier`, etc. (`OperationId → OperationIdentifier`,
`RecordId → RecordIdentifier`, `RelationId → RelationIdentifier`,
`AdjudicationRequestId → AdjudicationRequestIdentifier`,
`HarnessId → HarnessIdentifier`, `AlternativeId →
AlternativeIdentifier`, `DisplayId → DisplayIdentifier` — though
`DisplayIdentifier` itself reads heavy and may want a structural
rethink: `Display` of what?).

This is mechanical but workspace-wide. The `Identifier` expansion
applies to spirit's `RecordIdentifier` already — same rule, same
pattern.

### 2.10 — `BeadsToken` is named after a workspace artefact about to retire

`signal-persona-mind/src/lib.rs:408-417` defines `BeadsToken` for
referencing BEADS task identifiers. Per
`INTENT.md` §"BEADS is transitional; persona-mind is the
destination" and `intent/persona.nota` 2026-05-19T17:30 (loose
roles + beads transition), BEADS is the substrate Mind is meant
to replace.

The contract baking in a `BeadsToken` type at the wire layer is a
transitional concession; long-term it retires. The name should
land as `BeadsTaskToken` (less ambiguous when read in context)
during the rename pass, or — better — be folded into
`ExternalReference::BeadsTask(token)` only and dropped as a
distinct top-level type. (It already lives inside
`ExternalReference::BeadsTask`; making it bare on the contract is
the over-declaration.)

### 2.11 — hand-written codecs for every sum type

Twelve hand-written `NotaEncode` / `NotaDecode` impl blocks across
`signal-persona-mind/src/lib.rs` (`ScopeReference` at 173;
`ItemReference` at 627; `ExternalReference` at 687; `LinkTarget`
at 756; `EdgeTarget` at 803; `QueryKind` at 899; `ChannelEndpoint`
at 1153; `ChannelDuration` at 1219; `ChannelFilter` at 1314) and
more in `graph.rs` (`MindUnimplementedReason` at 942/967, plus
several `NotaSum` derives).

Most of these are now mechanically derivable via `#[derive(NotaSum)]`
since mixed enum support landed (per /150 §3 "Empty marker records
become unit variants" + `intent/component-shape.nota`'s mixed-enum
direction). Same /257 §3.1 bead (`primary-u0lh`) covers this.

The hand-written codecs are not bugs — they pre-date mixed-enum
support and were the right shape at that time. They retire on
derive coverage.

### 2.12 — closed `ChannelMessageKind` enum

`signal-persona-mind/src/lib.rs:1195-1210` defines
`ChannelMessageKind` as a closed 12-variant enum enumerating every
typed channel message in the workspace
(`MessageIngressSubmission`, `MessageSubmission`, `InboxQuery`,
`FocusObservation`, `PromptBufferObservation`, `MessageDelivery`,
`TerminalInput`, `TerminalCapture`, `TerminalResize`,
`TranscriptEvent`, `AdjudicationRequest`, `DeliveryNotification`).

Per /257 §2 (owner-signal-persona-router): *"closed enum mirroring
every typed channel message in the workspace. This is
agent-design-cultivated (per /249 gap #22); confirm with psyche
whether the closed enum is the right shape vs data-table."* Same
question applies here. Since channel authority moved to
owner-signal-persona-router (§2.5), and Mind's `ChannelFilter` /
`ChannelView` still reference `ChannelMessageKind`, the enum has
to either stay (mirror router's) or get extracted to a shared
type owned by router.

**Open psyche question**: is `ChannelMessageKind` a closed enum
(every channel-using component recompiles when a new kind appears)
or open data (token string)? The closed-enum-with-twelve-variants
shape is the agent-cultivated answer; settle.

### 2.13 — owner contract uses Mode-suffixed enums

`owner-signal-persona-mind/src/lib.rs:37-62` defines
`AuthorityMode`, `ChoreographyMode`, `IntentSynchronizationMode`.
Per `reports/second-operator-assistant/11` §4 (covering psyche's
naming intent in `intent/naming.nota` 2026-05-19T18:20:00Z),
`*Mode` is a framework-category suffix in the
`*Kind/*Type/*Info/*Details` family. Drop the suffix:

```text
Authority { ObserveOnly, ProposeOrders, IssueOrders }
Choreography { RecordOnly, Recommend, Decide }
IntentSynchronization { Disabled, SummaryOnly, FullRecord }
```

The `Configuration` struct's field types update automatically:
`authority: Authority`, `choreography: Choreography`,
`intent_synchronization: IntentSynchronization`. The variant names
already read as the kind of authority/choreography/synchronization.

### 2.14 — `Configure` and `Inspect` reads cleanly

The owner contract's two operations
(`owner-signal-persona-mind/src/lib.rs:136-147`) are
`operation Configure(Configuration)` and
`operation Inspect(Inspection)`. Reads cleanly per the cognitive-vs-
mechanical owner-verb principle from
`reports/second-operator-assistant/11` §7 — these are Spirit's
cognitive ordering surface on Mind, not Router-level mechanics.

The reply set (`Configured`, `PolicySnapshot`,
`ConfigurationRejected`, `RequestUnimplemented`) is well-shaped
modulo the §1.6 fix.

`PolicyRevision`, `PolicySection`, `ConfigurationRejectionReason`
all clean. ✓

### 2.15 — supervisor file is a sibling component's concern

`persona-mind/src/supervision.rs` is a 200+ line file implementing
the engine-manager-facing supervision socket. The whole file is
boilerplate that every supervised daemon repeats. The
`SupervisionListener::from_environment` env-var read (`supervision.rs:80`)
violates the no-daemon-env-vars rule (§2.7).

Long term, this lifts into a shared `persona-component-runtime`
helper crate consumed by every supervised daemon. Not Mind's
design call; flag as a follow-on for the engine-manager / shared-
runtime work. Mind's local concern is the env-var read.

## 3 · Owner signal audit

`owner-signal-persona-mind/src/lib.rs` (199 lines) is the
recently-created owner contract — per `intent/persona.nota`
2026-05-20T12:11:26Z, the repo was created to give PersonaSpirit
the authority surface for managing/configuring PersonaMind.

### 3.1 — macro target compliance

- ✓ Uses `signal-frame::signal_channel` (`lib.rs:9`).
- ✗ Manual alias dance present (`lib.rs:149-154`) — closes when
  bead `primary-77hh` lands and the macro emits unprefixed names.
- ✗ Hand-written `OperationKind` enum (`lib.rs:113-119`) — closes
  when the macro auto-generates it per /257 §3.1 second bead.
- ✗ Hand-written `From<Payload> for Reply` impls
  (`lib.rs:165-198`) — same macro generation bead.
- ✗ Missing observable block. Designer lean (per §2.4) is to skip
  observable on owner contracts; confirm with psyche.

### 3.2 — operations match the policy/configuration authority surface

- `operation Configure(Configuration)` ✓ — owner sets durable
  policy.
- `operation Inspect(Inspection)` ✓ — owner reads policy state.

Both align with `reports/second-operator-assistant/11` §6 (policy
signal verb shapes: Configure, Inspect, lifecycle). Lifecycle
verbs (Start/Drain/Stop/Reload) are absent — per
`intent/component-shape.nota` 2026-05-20T13:45:00Z (open
clarification), Mind's lifecycle may live out-of-band on the
infrastructure supervisor channel rather than on the policy signal.
Designer lean: keep them off until the engine-manager rename
settles whether per-component lifecycle migrates to the owner
contract.

### 3.3 — no ordinary-signal operations have leaked in

Configure / Inspect are owner-only by nature (configuration is
always owner authority per `intent/component-shape.nota`
2026-05-19T01:25:00Z). Nothing peer-callable has accidentally
ended up here. ✓

### 3.4 — fields and types

- `PolicyRevision(u64)` newtype ✓.
- `Configuration` carries the three Mode-suffixed enums (see §2.13
  — drop Mode).
- `PolicySnapshot { revision, configuration }` reads cleanly. ✓
- `PolicySection { Authority, Choreography, IntentSynchronization,
  All }` — closed enum mirroring the Configuration fields plus an
  `All` variant. Clean shape; if the Configuration's enum names
  rename per §2.13, `PolicySection` follows.
- `ConfigurationRejectionReason` with three variants
  (`SpiritAuthorityRequired`, `PolicyWouldBreakChoreography`,
  `IntentSynchronizationUnavailable`) ✓.
- `RequestUnimplemented` has the redundant `operation` field per
  §1.6 — drop.

### 3.5 — `OperationKind` propagates outward

`owner-signal-persona-mind/src/lib.rs:113-119` defines
`OperationKind` with two variants (`Configure`, `Inspect`). Only
populates the `RequestUnimplemented.operation` field. With both
the field dropped (§1.6) and the enum macro-generated (§3.1), this
manual enum retires.

### 3.6 — net assessment of owner contract

Cleaner than the working contract. Compliant with the working/policy
split and the cognitive-verb shape. Carries the recurring macro-
boilerplate smells (alias dance, hand-written OperationKind, hand-
written From impls) but none of the bigger structural issues.
After the macro fixes (`primary-77hh`, `primary-u0lh`, and the
auto-generation of OperationKind/Frame names per /150 §1.1) and
the Mode-suffix and RequestUnimplemented cleanups, this contract is
close to current best shape.

## 4 · Recommended next slice

Prioritized order. **No beads filed per audit constraint.** Where
work substance is named in existing beads (`primary-77hh`,
`primary-k3bu`, `primary-u0lh`) those are referenced for cross-
visibility, not filed-against.

1. **Refresh `persona-mind/Cargo.toml` git pin on
   signal-persona-mind**. Drop the four dead pattern arms in
   `persona-mind/src/actors/dispatch.rs:92-98`. Mechanical; closes
   the §2.5 drift.
2. **Restructure the working contract operations and replies** to
   contract-local verbs with lifted typed sums. The full §2.1
   shape — 7 operation roots, `Submission`/`Receipt`/`Query` sums,
   `ChangeStatus(StatusTransition)` instead of
   `Mutate StatusChange(StatusChange)`. Replaces /257 §1.1 + §1.2
   + §1.3 + §1.4 in one pass for this contract. **Largest pure
   design move.** Surface the two-channel-vs-one-channel question
   for psyche before committing (§2.1 open question).
3. **Migrate the working contract to `signal-frame`** and drop
   `signal-core` from its Cargo.toml. Bead `primary-77hh` covers
   the macro side; this contract just consumes the new shape.
4. **Add observable block** to the working contract per §2.4 +
   `intent/persona.nota` 2026-05-20T20:00:00Z (deferred-fanout
   placeholder shape).
5. **Rewrite the `mind` binary as the workspace-universal thin CLI**
   per §2.2. New layout:
   - `persona-mind/src/main.rs` becomes the CLI (one NOTA
     argument, dispatch via `signal_cli!` macro from /129).
   - `persona-mind/src/bin/mind-daemon.rs` becomes the daemon
     binary, takes one NOTA config record.
   - `persona-mind/src/command.rs` retires entirely.
   - `Error::Missing*Path` / `UnknownCommandLineOption` /
     `MissingCommandLineOptionValue` variants retire from
     `error.rs`.
6. **Move daemon env-var reads to NOTA config** per §2.7. The
   `MindSocketMode::from_environment` and
   `SupervisionListener::from_environment` paths get replaced by
   fields on the daemon's NOTA config record.
7. **Migrate the daemon onto `signal-executor`** per §2.3. Define
   the local `MindCommand` / `MindEffect` enums (after the argv
   `MindCommand` retires per step 5); implement `Lowering`,
   `CommandExecutor`, `ToSemaOperation`, `ToSemaOutcome`,
   `BatchErrorClassification`; wire
   `signal_executor::Executor::execute` into the socket actor.
   **Largest implementation move; structurally identical to
   spirit's migration that landed in /255/256.**
8. **Drop the `RoleName` enum** per §2.6. Either consume orchestrate's
   `RoleIdentifier` (if Mind needs the type) or drop the import.
9. **Drop `Mode` suffix from owner contract enums** per §2.13.
   Small mechanical pass.
10. **Drop `RequestUnimplemented.operation`** on the owner contract
    per §1.6 / §3.5. Then drop the manual `OperationKind` enum.
11. **Rename `*Id` → `*Identifier`** per §2.9. Mechanical workspace-
    wide. Pairs with whatever rename bead covers identifier-naming.
12. **Macro derivation pass** — replace hand-written codecs with
    `#[derive(NotaSum)]` / `#[derive(NotaEnum)]` where the mixed-
    enum support now suffices (§2.11). Bead `primary-u0lh`.

Items 2-5 are the load-bearing work; items 6-12 mostly absorb into
those passes once they're underway.

## 5 · References

### Intent records (the design substrate this audit operates against)

- `intent/persona.nota` 2026-05-18T12:08:41Z — Mind owns STATE,
  Orchestrate owns MACHINERY.
- `intent/persona.nota` 2026-05-19T15:04:19Z — dynamic roles.
- `intent/persona.nota` 2026-05-19 21:45 — beads don't get role
  labels.
- `intent/persona.nota` 2026-05-20T12:11:26Z — owner-signal-persona-
  mind creation; PersonaSpirit owns PersonaMind.
- `intent/persona.nota` 2026-05-20T13:09:13Z — Mind-to-Router
  authority orders move out of `signal-persona-mind`.
- `intent/component-shape.nota` 2026-05-20T13:30:00Z (Correction) —
  Orchestrate owns Router, not Mind; chain is Mind → Orchestrate →
  Router.
- `intent/persona.nota` 2026-05-20 17:30 — mind talks to orchestrate
  in abstract concept terms; channel authority lives in router-owner.
- `intent/persona.nota` 2026-05-20T20:00:00Z — Tap/Untap fanout
  deferred until persona-introspect lands; the contract declaration
  stays mandatory.
- `intent/persona.nota` 2026-05-21T10:00:00Z — debug the debugger
  (every persona component is observable).
- `intent/component-shape.nota` 2026-05-19T01:23:00Z — single
  argument rule, no flags.
- `intent/component-shape.nota` 2026-05-19T19:30:00Z — contract-
  local verbs at the public layer; `Match Query(Query)` rejected.
- `intent/component-shape.nota` 2026-05-20T00:07:55+02:00 — lift
  repeated suffix into typed sums (symmetric request/reply).
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer
  model; Tap/Untap mandatory for persona.
- `intent/component-shape.nota` 2026-05-20T13:00:00Z — six
  CLI-design records (binary name, two argument shapes, pure
  translation, env-var carve-out, two-socket dispatch, universality).
- `intent/component-shape.nota` 2026-05-20 21:53 — CLI is just a
  thin client to speak the signal; daemons never read env vars.
- `intent/component-shape.nota` 2026-05-21T10:30:00Z — modules-
  not-options for macro disambiguation.
- `intent/naming.nota` 2026-05-19T18:20:00Z — identifier > id;
  drop most abbreviations.
- `intent/naming.nota` 2026-05-19T15:46:23Z — names don't carry
  full ancestry.

### Reference reports

- `reports/operator/150-triad-signal-sema-migration-current-state.md` §6.1 —
  *"Mind is the worst-shaped remaining Persona contract"* —
  enumerates the design direction this audit confirms.
- `reports/designer/258-persona-signal-triad-audit-2026-05-21.md` —
  engine-manager template audit (the structural shape this audit
  follows).
- `reports/designer/257-signal-contracts-names-and-shape-audit.md`
  §2 (signal-persona-mind) — the workspace-wide audit; lists the
  same findings consolidated here with file:line evidence.
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md` —
  signal-type naming/shape design guideline; principles 1-8 apply.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md` —
  the `signal_cli!` macro sketch that the new `mind` binary
  consumes (§2.2 target shape).

### Files under audit

- `signal-persona-mind/src/lib.rs` (1451 lines).
- `signal-persona-mind/src/graph.rs` (999 lines).
- `signal-persona-mind/Cargo.toml`.
- `owner-signal-persona-mind/src/lib.rs` (199 lines).
- `owner-signal-persona-mind/Cargo.toml`.
- `persona-mind/src/main.rs`, `src/command.rs`, `src/transport.rs`,
  `src/supervision.rs`, `src/error.rs`, `src/actors/dispatch.rs`.
- `persona-mind/ARCHITECTURE.md`, `AGENTS.md`.
- `persona-mind/Cargo.toml`.

### Workspace authority cited

- `AGENTS.md`, `ESSENCE.md`, `INTENT.md`.
- `skills/component-triad.md` §"The single argument rule",
  §"The five invariants", §"Authority chain — worked example".
- `skills/naming.md` §"Anti-pattern: framework-category suffixes on
  type names", §"Anti-pattern: repeated category words across
  sibling names".
- `skills/reporting.md`.

This report retires when (a) the working contract is restructured
per §2.1, the `mind` binary is rewritten per §2.2, the daemon is
on `signal-executor` per §2.3, the observable block lands per
§2.4, and the smaller cleanups absorb; or (b) a successor audit
supersedes once a partial migration has shifted the surface.
