# 101. Persona-mind full architecture proposal

## 1. Thesis

`persona-mind` should be Persona's central state component. It is not a
generic database, not a router, not a terminal controller, and not a
replacement for the signal contracts. It is the stateful actor tree that owns
the workspace coordination truth:

- role claims and releases
- handoffs
- activity logs
- work and memory graph items
- notes
- dependencies
- decisions
- aliases for imported or external identities
- ready-work views
- role state that replaces `<role>.lock` files

The short version:

```mermaid
flowchart LR
    contracts["signal-persona-mind"] --> mind["persona-mind"]
    sema["persona-sema"] --> mind
    mind --> db[("mind.redb")]
    mind --> roles["typed role state"]
    mind --> views["ready-work views"]
```

`signal-persona-mind` is the wire vocabulary. `persona-sema` is the typed
database library. `persona-mind` owns one database file through that library
and applies the contract as ordered state transitions.

## 2. Current Ground Truth

The current implementation already has the right direction but is still a
partial scaffold.

| Area | Current state | Target state |
|---|---|---|
| Contract | `signal-persona-mind` defines `MindRequest` and `MindReply` variants for role, activity, and memory/work operations. | Keep this as the only public protocol for mind operations. Extend only when a state transition cannot be expressed honestly. |
| Claims | `persona-mind` has in-memory claim scope logic and overlap tests. | Persist claims in `mind.redb`, with one writer actor deciding conflicts atomically. |
| Memory/work graph | `persona-mind` has an in-memory reducer with tests for open, note, link, status, alias, ready, blocked, and query behavior. | Preserve reducer semantics, but store items, edges, notes, aliases, and events in sema-backed tables. |
| Activity | Contract exists. | Implement as store-stamped append-only activity records. |
| CLI | Architecture names `mind` as one NOTA argv record to one NOTA reply. | Keep that. The CLI should translate text into a typed signal request, then submit to the same actor path used by any host. |
| Legacy coordination | `<role>.lock` files and BEADS exist today. | Replace lock files with typed mind state. Treat BEADS as transitional import input, not a live dependency. |

## 3. Component Boundary

`persona-mind` owns coordination state. Other Persona components must not
write that state directly.

```mermaid
flowchart TB
    agent["agent harness"] --> cli["mind CLI"]
    human["human"] --> cli
    shim["tools/orchestrate compatibility shim"] --> cli

    cli --> contract["signal-persona-mind"]
    contract --> ingress["IngressSupervisorActor"]
    ingress --> dispatch["DispatchSupervisorActor"]
    dispatch --> domain["DomainSupervisorActor"]
    domain --> store["StoreSupervisorActor"]

    store --> writer["SemaWriterActor"]
    writer --> sema["persona-sema"]
    sema --> db[("mind.redb")]

    store --> views_actor["ViewSupervisorActor"]
    views_actor --> views["ready-work and role views"]

    store --> events["post-commit event stream"]
    events --> subscribers["future subscribers"]
```

The important invariant is one state owner:

```mermaid
flowchart LR
    bad1["router"] -. must not write .-> db[("mind.redb")]
    bad2["harness"] -. must not write .-> db
    bad3["terminal"] -. must not write .-> db
    good["SemaWriterActor"] --> db
```

The router may route Persona messages. The harness may inject or observe a
terminal. The terminal layer may own pane/session handles. None of those
components owns role claims, handoffs, memory items, or work dependencies.

## 4. Actor-Dense Runtime

Every runtime form should use the same actor structure. For the first working
stack, the `mind` CLI can start the actors in-process for a single request. A
long-lived host can reuse the same actor tree later when post-commit
subscriptions become necessary.

The important correction is that mind is not one or two actors. Mind is an
actor system. Each phase of logic gets an actor so the architecture can be
inspected, tested, supervised, and expanded without turning into a hidden
service object.

```mermaid
flowchart TB
    root["MindRootActor"]
    root --> config["ConfigActor"]
    root --> ingress_supervisor["IngressSupervisorActor"]
    root --> dispatch_supervisor["DispatchSupervisorActor"]
    root --> domain_supervisor["DomainSupervisorActor"]
    root --> store_supervisor["StoreSupervisorActor"]
    root --> view_supervisor["ViewSupervisorActor"]
    root --> subscription_supervisor["SubscriptionSupervisorActor"]
    root --> reply_supervisor["ReplySupervisorActor"]

    ingress_supervisor --> cli_ingress["CliIngressActor"]
    ingress_supervisor --> session["RequestSessionActor"]
    ingress_supervisor --> nota_decode["NotaDecodeActor"]
    ingress_supervisor --> identity["CallerIdentityActor"]
    ingress_supervisor --> envelope["EnvelopeActor"]

    dispatch_supervisor --> router_actor["RequestDispatchActor"]
    dispatch_supervisor --> claim_flow["ClaimFlowActor"]
    dispatch_supervisor --> handoff_flow["HandoffFlowActor"]
    dispatch_supervisor --> activity_flow["ActivityFlowActor"]
    dispatch_supervisor --> memory_flow["MemoryFlowActor"]
    dispatch_supervisor --> query_flow["QueryFlowActor"]

    domain_supervisor --> claim_supervisor["ClaimSupervisorActor"]
    domain_supervisor --> memory_supervisor["MemoryGraphSupervisorActor"]
    domain_supervisor --> query_supervisor["QuerySupervisorActor"]

    store_supervisor --> writer["SemaWriterActor"]
    store_supervisor --> reader["SemaReadActor"]
    store_supervisor --> id_mint["IdMintActor"]
    store_supervisor --> clock["ClockActor"]
    store_supervisor --> event_append["EventAppendActor"]
    store_supervisor --> commit["CommitActor"]

    view_supervisor --> role_view["RoleSnapshotViewActor"]
    view_supervisor --> ready_view["ReadyWorkViewActor"]
    view_supervisor --> blocked_view["BlockedWorkViewActor"]
    view_supervisor --> activity_view["RecentActivityViewActor"]

    subscription_supervisor --> commit_bus["CommitBusActor"]
    subscription_supervisor --> subscriber["SubscriberActor"]

    reply_supervisor --> reply_encode["NotaReplyEncodeActor"]
    reply_supervisor --> error_shape["ErrorShapeActor"]
```

Top-level actor groups:

| Actor group | Owns | Does not own |
|---|---|---|
| `IngressSupervisorActor` | Input sessions, NOTA decode, caller identity, request envelope. | State transitions. |
| `DispatchSupervisorActor` | Request classification and operation flow actor selection. | Storage. |
| `DomainSupervisorActor` | Claim, handoff, activity, memory, and query domain actors. | Redb transactions. |
| `StoreSupervisorActor` | Sema access, IDs, time, event append, commit ordering. | Domain policy. |
| `ViewSupervisorActor` | Read views and cached summaries after commit. | Authoritative state. |
| `SubscriptionSupervisorActor` | Push events after commit. | Polling. |
| `ReplySupervisorActor` | Typed replies, NOTA reply rendering, error shape. | State transitions. |

Only `SemaWriterActor` opens write transactions. That does not mean it
contains the whole state machine. It means all operation actors send typed
write intents to one serialized writer.

```mermaid
flowchart LR
    claim_actor["ClaimDecisionActor"] --> write_intent["ClaimWriteIntent"]
    memory_actor["ItemOpenActor"] --> item_intent["ItemWriteIntent"]
    status_actor["StatusChangeActor"] --> status_intent["StatusWriteIntent"]
    activity_actor["ActivityAppendActor"] --> activity_intent["ActivityWriteIntent"]

    write_intent --> writer["SemaWriterActor"]
    item_intent --> writer
    status_intent --> writer
    activity_intent --> writer

    writer --> tx["single write transaction"]
    tx --> db[("mind.redb")]
```

The practical rule: if a phase has a name and a failure mode, it probably
deserves an actor.

### 4.1 Claim Write Scenario

```mermaid
sequenceDiagram
    participant CLI as "mind CLI"
    participant Session as "RequestSessionActor"
    participant Decode as "NotaDecodeActor"
    participant Identity as "CallerIdentityActor"
    participant Dispatch as "RequestDispatchActor"
    participant Flow as "ClaimFlowActor"
    participant Normalize as "ClaimNormalizeActor"
    participant Conflict as "ClaimConflictActor"
    participant Writer as "SemaWriterActor"
    participant Event as "EventAppendActor"
    participant Views as "RoleSnapshotViewActor"
    participant Reply as "NotaReplyEncodeActor"

    CLI->>Session: one NOTA argv record
    Session->>Decode: decode text
    Decode->>Identity: typed MindRequest
    Identity->>Dispatch: MindEnvelope
    Dispatch->>Flow: RoleClaim
    Flow->>Normalize: normalize scope
    Normalize->>Conflict: normalized claim
    Conflict->>Writer: ClaimWriteIntent
    Writer->>Event: append ClaimAccepted event
    Writer->>Views: post-commit role view refresh
    Writer-->>Flow: ClaimAcceptance
    Flow-->>Reply: typed reply
    Reply-->>CLI: one NOTA reply record
```

This path has many actors because every stage can be tested separately:
decode failure, identity failure, scope normalization, conflict detection,
write failure, event append, view refresh, and reply shape.

### 4.2 Ready-Work Query Scenario

```mermaid
sequenceDiagram
    participant CLI as "mind CLI"
    participant Session as "RequestSessionActor"
    participant Decode as "NotaDecodeActor"
    participant Dispatch as "RequestDispatchActor"
    participant Query as "QueryFlowActor"
    participant Plan as "QueryPlanActor"
    participant Reader as "SemaReadActor"
    participant Ready as "ReadyWorkViewActor"
    participant Graph as "GraphTraversalActor"
    participant Shape as "QueryResultShapeActor"
    participant Reply as "NotaReplyEncodeActor"

    CLI->>Session: Query ReadyWork
    Session->>Decode: decode NOTA
    Decode->>Dispatch: MindRequest::Query
    Dispatch->>Query: query request
    Query->>Plan: choose read strategy
    Plan->>Ready: ask cached ready-work view
    Ready->>Reader: read view snapshot
    Reader-->>Ready: candidate item IDs
    Ready->>Graph: validate dependencies
    Graph->>Reader: read item and edge snapshot
    Reader-->>Graph: typed graph rows
    Graph-->>Shape: ready item set
    Shape-->>Reply: MindReply::View
    Reply-->>CLI: NOTA reply
```

Query actors are allowed to use read snapshots. They are not allowed to repair
state while answering. If a query detects stale views, it returns that fact as
a typed reply or emits a push-triggered refresh request after the read.

### 4.3 Blocked Item Query

```mermaid
flowchart TB
    cli["mind CLI"] --> session["RequestSessionActor"]
    session --> decode["NotaDecodeActor"]
    decode --> dispatch["RequestDispatchActor"]
    dispatch --> query["QueryFlowActor"]
    query --> plan["QueryPlanActor"]

    plan --> blocked_view["BlockedWorkViewActor"]
    blocked_view --> read_a["SemaReadActor"]
    read_a --> blocked_rows["blocked candidate rows"]

    blocked_rows --> graph["GraphTraversalActor"]
    graph --> edge_read["EdgeReadActor"]
    graph --> item_read["ItemReadActor"]
    edge_read --> sema_read["SemaReadActor"]
    item_read --> sema_read

    graph --> explain["BlockerExplainActor"]
    explain --> shape["QueryResultShapeActor"]
    shape --> reply["NotaReplyEncodeActor"]
```

This is intentionally more actorful than a normal in-process query. The point
is to make each internal promise testable: the blocked view finds candidates,
the graph traversal validates them, and the explanation actor turns the graph
facts into a reply without mutating state.

### 4.4 Open Item Scenario

```mermaid
sequenceDiagram
    participant CLI as "mind CLI"
    participant Dispatch as "RequestDispatchActor"
    participant Flow as "MemoryFlowActor"
    participant Open as "ItemOpenActor"
    participant Id as "IdMintActor"
    participant Clock as "ClockActor"
    participant Writer as "SemaWriterActor"
    participant Items as "ItemTableActor"
    participant Events as "EventAppendActor"
    participant Ready as "ReadyWorkViewActor"
    participant Reply as "NotaReplyEncodeActor"

    CLI->>Dispatch: MindRequest::Open
    Dispatch->>Flow: memory mutation
    Flow->>Open: open item command
    Open->>Id: mint item ID and display ID
    Open->>Clock: store timestamp
    Open->>Writer: ItemOpenWriteIntent
    Writer->>Items: write item row
    Writer->>Events: append ItemOpened event
    Writer->>Ready: refresh ready-work view
    Writer-->>Open: Opened
    Open-->>Reply: MindReply::Opened
```

The item opener does not mint IDs itself. It asks the ID actor. The caller does
not supply time. It asks the clock actor through the write path.

### 4.5 Dependency Link Scenario

```mermaid
flowchart LR
    cli["mind CLI"] --> session["RequestSessionActor"]
    session --> dispatch["RequestDispatchActor"]
    dispatch --> memory_flow["MemoryFlowActor"]
    memory_flow --> link_actor["LinkActor"]
    link_actor --> resolve_source["SourceResolveActor"]
    link_actor --> resolve_target["TargetResolveActor"]
    resolve_source --> read_actor["SemaReadActor"]
    resolve_target --> read_actor
    link_actor --> edge_validate["EdgeValidateActor"]
    edge_validate --> writer["SemaWriterActor"]
    writer --> edge_table["EdgeTableActor"]
    writer --> event_append["EventAppendActor"]
    writer --> ready_view["ReadyWorkViewActor"]
    writer --> blocked_view["BlockedWorkViewActor"]
    ready_view --> reply["NotaReplyEncodeActor"]
    blocked_view --> reply
```

This is where actor granularity matters. Source resolution, target resolution,
edge validation, edge write, event append, and view refresh are separate
failures.

### 4.6 Handoff Scenario

```mermaid
sequenceDiagram
    participant CLI as "mind CLI"
    participant Flow as "HandoffFlowActor"
    participant From as "FromRoleActor"
    participant To as "ToRoleActor"
    participant Claim as "ClaimConflictActor"
    participant Writer as "SemaWriterActor"
    participant Handoffs as "HandoffTableActor"
    participant Claims as "ClaimTableActor"
    participant Events as "EventAppendActor"
    participant Views as "RoleSnapshotViewActor"
    participant Reply as "NotaReplyEncodeActor"

    CLI->>Flow: MindRequest::RoleHandoff
    Flow->>From: validate source role owns scope
    Flow->>To: validate target role
    Flow->>Claim: validate no third-role conflict
    Claim->>Writer: HandoffWriteIntent
    Writer->>Handoffs: append handoff row
    Writer->>Claims: move claim ownership
    Writer->>Events: append RoleHandoff event
    Writer->>Views: refresh source and target role views
    Writer-->>Reply: HandoffAcceptance
```

A handoff is still one state transition, but the validation phases are actors.

### 4.7 Error Reply Scenario

```mermaid
flowchart TB
    cli["mind CLI"] --> decode["NotaDecodeActor"]
    decode -->|decode error| error_shape["ErrorShapeActor"]
    error_shape --> reply_encode["NotaReplyEncodeActor"]
    reply_encode --> cli_reply["Rejected reply"]

    decode -->|valid request| identity["CallerIdentityActor"]
    identity -->|unknown caller| error_shape
    identity -->|known caller| dispatch["RequestDispatchActor"]
    dispatch -->|unsupported operation| error_shape
```

Errors are also actor-shaped. A rejected reply should be just as typed as an
accepted reply.

### 4.8 Actor Multiplicity Pattern

Mind should be designed so hundreds of actors are normal, not exceptional.
Many of them can be short-lived request actors. Others can be long-lived
supervisors, role actors, view actors, or table actors.

```mermaid
flowchart TB
    root["MindRootActor"] --> roles["RoleSupervisorActor"]
    root --> items["ItemSupervisorActor"]
    root --> queries["QuerySupervisorActor"]
    root --> tables["TableSupervisorActor"]

    roles --> operator_role["RoleActor operator"]
    roles --> designer_role["RoleActor designer"]
    roles --> assistant_role["RoleActor assistant"]
    roles --> system_role["RoleActor system-specialist"]

    items --> item_a["ItemActor item-a"]
    items --> item_b["ItemActor item-b"]
    items --> item_c["ItemActor item-c"]

    queries --> query_a["QuerySessionActor A"]
    queries --> query_b["QuerySessionActor B"]
    queries --> query_c["QuerySessionActor C"]

    tables --> claim_table["ClaimTableActor"]
    tables --> item_table["ItemTableActor"]
    tables --> edge_table["EdgeTableActor"]
    tables --> note_table["NoteTableActor"]
    tables --> alias_table["AliasTableActor"]
    tables --> activity_table["ActivityTableActor"]
```

This keeps the implementation honest. If a future agent claims "the item graph
is actor-based" but there is no `ItemActor`, no `EdgeActor`, and no
`GraphTraversalActor`, the architecture truth tests should fail.

## 5. Signal Boundary

All public operations enter through `signal-persona-mind`.

```mermaid
flowchart LR
    text["NOTA text"] --> cli["mind CLI"]
    cli --> request["MindRequest"]
    request --> frame["rkyv signal frame"]
    frame --> ingress["MindIngressActor"]
    ingress --> reply["MindReply"]
    reply --> text_reply["NOTA reply"]
```

The CLI is a convenience layer. It must not become a second command language.
Human and agent-facing text is NOTA. Internally, requests and replies are typed
signal records serialized with rkyv where a wire boundary exists.

The contract should remain domain-shaped, not database-shaped. Good examples:

- `RoleClaim`
- `RoleRelease`
- `RoleHandoff`
- `ActivitySubmission`
- `Open`
- `AddNote`
- `Link`
- `ChangeStatus`
- `AddAlias`
- `Query`

Bad examples:

- `InsertRow`
- `UpdateTable`
- `StoreMessage`
- `RawMutation`

Mind accepts intent. It decides the storage mutation.

## 6. Storage Model

`persona-mind` owns one sema-backed redb file:

```text
mind.redb
```

The file should live in a workspace-local state directory at first, because
Persona coordination is workspace-scoped today. A system-level Persona OS
deployment can later move the location behind configuration without changing
the contract.

Recommended tables:

| Table | Purpose |
|---|---|
| `CLAIMS` | Current active role claims. |
| `HANDOFFS` | Pending and completed handoffs. |
| `ACTIVITIES` | Store-stamped activity log. |
| `ITEMS` | Work, memory, decision, and issue items. |
| `EDGES` | Typed dependencies and references between items or external targets. |
| `NOTES` | Notes attached to items. |
| `ALIASES` | External identifiers such as imported BEADS IDs. |
| `EVENTS` | Append-only event log for every state mutation. |
| `META` | Schema version, store identity, migration marker. |

The event log is the audit trail. The tables are materialized views optimized for
current-state queries.

```mermaid
flowchart TB
    req["MindRequest"] --> reducer["typed reducer"]
    reducer --> event["Event"]
    event --> commit["single redb write transaction"]
    commit --> tables["current-state tables"]
    commit --> log["EVENTS"]
    commit --> views["post-commit read views"]
```

Store-minted data:

- activity timestamps
- event sequence
- operation IDs
- item IDs
- display IDs
- imported-alias records

Agent-minted data should be treated as user content, not authority. This is
especially important for IDs and timestamps.

## 7. Claim And Handoff Semantics

Role claims are the replacement for ad hoc lock editing. Mind does not keep
lock files alive as projections. Old lock files are migration artifacts only.

```mermaid
sequenceDiagram
    participant A as "operator"
    participant C as "mind CLI"
    participant D as "RequestDispatchActor"
    participant F as "ClaimFlowActor"
    participant N as "ClaimNormalizeActor"
    participant X as "ClaimConflictActor"
    participant W as "SemaWriterActor"
    participant V as "RoleSnapshotViewActor"

    A->>C: RoleClaim path + reason
    C->>D: MindRequest::RoleClaim
    D->>F: start claim flow
    F->>N: normalize scope
    N->>X: normalized claim
    X->>W: conflict-checked write intent
    alt accepted
        W->>V: post-commit role view refresh
        W-->>F: ClaimAcceptance
        F-->>C: ClaimAcceptance
    else rejected
        X-->>C: ClaimRejection with conflicting role and scope
    end
```

Rules:

- Claims are advisory coordination state, but the workspace treats them as a
  hard social protocol.
- Path claims must be normalized by `persona-mind`, not trusted from callers.
- Parent/child overlap is a conflict across roles.
- Redundant child claims under the same role collapse into the parent claim.
- A handoff is not a release plus a claim. It is a typed transition with one
  event that preserves provenance.
- No new code should write `<role>.lock`. The migration path is to read old
  files once if needed, commit equivalent mind state, then stop using them.
- View refresh failure is not allowed to silently hide a successful claim. The
  reply must surface view status or the view actor must retry by push-driven
  scheduling.

## 8. Activity Semantics

Activity is not chat history. It is a typed operational log.

Examples:

- role claimed a scope
- role released a scope
- role created a work item
- role linked a dependency
- role added a note
- role changed item status
- role imported a BEADS task

The caller can submit activity content, but the store supplies time and slot.

```mermaid
flowchart LR
    submitted["ActivitySubmission without timestamp"] --> flow["ActivityFlowActor"]
    flow --> clock["ClockActor"]
    flow --> writer["SemaWriterActor"]
    clock --> stamped["store-stamped Activity"]
    writer --> stamped
    stamped --> activities["ACTIVITIES"]
    stamped --> events["EVENTS"]
```

Open design issue: current memory mutations need a reliable actor identity.
The clean solution is a common request envelope:

```text
MindEnvelope {
    actor,
    request,
}
```

If the CLI derives actor identity from the role configuration, the actor field
must still enter the typed state transition before persistence. Otherwise
memory/work events cannot be audited correctly.

## 9. Memory And Work Graph

The folded `persona-work` concept belongs inside mind. Work is not separate
from memory; it is a graph of things the Persona knows, intends, blocks on, or
has decided.

```mermaid
flowchart LR
    item1["Item: implement router guard"] -->|DependsOn| item2["Item: system focus fact"]
    item1 -->|RefersTo| doc["Report"]
    item3["Decision"] -->|Supersedes| item4["Old proposal"]
    note["Note"] --> item1
```

Core item kinds:

- task
- issue
- decision
- note-backed memory
- imported external item
- report reference

Core edge kinds:

- depends on
- blocks
- refers to
- supersedes
- duplicates
- follows up

The current in-memory `MemoryState` already proves the basic reducer shape:

- open item
- attach note
- link dependency
- change status
- add alias
- query ready work
- query blocked work
- resolve imported BEADS alias

The next step is not to redesign those semantics. The next step is to move the
truth from `RefCell<Graph>` into sema-backed tables while preserving the tests.

## 10. BEADS Transition

BEADS is transitional and never a lock.

```mermaid
flowchart LR
    beads["BEADS task"] --> import["one-time import"]
    import --> item["Mind Item"]
    import --> alias["ExternalAlias"]
    item --> mind["mind.redb"]
    alias --> mind
```

Rules:

- Do not build a live Persona to BEADS bridge.
- Do not deepen BEADS investment.
- Do import BEADS entries when useful.
- Preserve old BEADS IDs as aliases so historical references remain
  searchable.
- New work should be represented as mind items, not BEADS tasks, once the CLI
  is available.

## 11. CLI Shape

The `mind` binary should be boring and strict:

```text
mind '<NOTA record>'
```

It returns exactly one NOTA reply record.

Compatibility tools can remain:

```mermaid
flowchart LR
    old["tools/orchestrate claim ..."] --> shim["shim builds NOTA request"]
    shim --> mind["mind CLI"]
    mind --> reply["typed reply"]
```

The CLI must not grow flag-shaped alternate semantics. If a convenience command
is needed, it should lower into the same typed request and should be tested as
a typed lowering.

Examples of acceptable CLI responsibilities:

- parse one NOTA request
- decode it into `MindRequest`
- attach configured caller identity
- start or connect to the mind actor tree
- print one `MindReply`

Examples of unacceptable CLI responsibilities:

- directly edit lock files
- directly mutate redb tables
- create untyped JSON/TOML/YAML side channels for operations
- generate authoritative timestamps or IDs

## 12. Rust Module Shape

Recommended crate layout:

```text
persona-mind/
  src/
    lib.rs
    main.rs
    actors/
      root.rs
      ingress.rs
      dispatch.rs
      claim.rs
      handoff.rs
      activity.rs
      memory.rs
      query.rs
      store.rs
      view.rs
      subscription.rs
      reply.rs
    service.rs
    state.rs
    store.rs
    tables.rs
    claim.rs
    activity.rs
    memory.rs
    view.rs
    config.rs
```

| Module | Responsibility |
|---|---|
| `actors/root.rs` | Runtime supervision tree. |
| `actors/ingress.rs` | CLI sessions, NOTA decode, caller identity, request envelopes. |
| `actors/dispatch.rs` | Request classification and operation flow selection. |
| `actors/claim.rs` | Claim normalization, conflict detection, claim write intents. |
| `actors/handoff.rs` | Source role validation, target role validation, atomic handoff intent. |
| `actors/activity.rs` | Activity shaping before store-stamped append. |
| `actors/memory.rs` | Item, note, edge, status, and alias operation actors. |
| `actors/query.rs` | Query planning, view reads, graph traversal, result shaping. |
| `actors/store.rs` | Sema read/write actors, ID mint, clock, event append, commit ordering. |
| `actors/view.rs` | Role snapshot, ready-work, blocked-work, and activity view actors. |
| `actors/subscription.rs` | Push-only post-commit notifications. |
| `actors/reply.rs` | Typed reply and error rendering. |
| `service.rs` | Runtime bootstrap object used by CLI and tests. |
| `state.rs` | Data-bearing reducer state types; no hidden runtime ownership. |
| `store.rs` | Sema-backed persistence wrapper. |
| `tables.rs` | Typed table definitions and migration/version checks. |
| `claim.rs` | Claim normalization and conflict reducer. |
| `activity.rs` | Activity append reducer. |
| `memory.rs` | Item/edge/note/alias reducer. |
| `view.rs` | Read-view and cached-summary refresh logic. |
| `config.rs` | Workspace-local paths and caller identity configuration. |

The style constraint is important: reducers should be methods on data-bearing
objects. Free functions should be avoided except where Rust traits require
them. Zero-sized types should not become fake services.

## 13. Test Plan

Persona needs tests that prove architectural behavior, not just local function
behavior.

### 13.1 Contract tests

In `signal-persona-mind`:

- every request variant round-trips through rkyv
- every reply variant round-trips through rkyv
- invalid wire data fails closed
- contract examples remain small enough for agents to read

### 13.2 Reducer tests

In `persona-mind`:

- parent and child claim overlap is detected
- same-role redundant claims collapse
- cross-role overlap rejects
- handoff preserves provenance
- item open creates exactly one event
- dependency controls ready and blocked views
- alias resolves imported identity
- unknown item mutation rejects

### 13.3 Storage truth tests

These are the tests most likely to catch agent slop.

```mermaid
flowchart LR
    step1["process A writes claim"] --> db[("mind.redb")]
    db --> step2["process B reads snapshot"]
    step2 --> assert["assert same typed claim"]
```

Required cases:

- write in one process, read in another
- event append and view table update happen in one transaction
- store, not caller, supplies timestamp
- store, not caller, supplies item ID
- failed read-view refresh does not erase a committed event

### 13.4 Actor ordering tests

```mermaid
flowchart TB
    a["RoleClaim A"] --> flow_a["ClaimFlowActor A"]
    b["RoleClaim B"] --> flow_b["ClaimFlowActor B"]
    flow_a --> writer["SemaWriterActor"]
    flow_b --> writer
    writer --> result["one accepted, one rejected"]
```

Required cases:

- concurrent overlapping claims produce deterministic conflict results
- non-overlapping claims can both commit
- query after commit sees committed state
- query before commit never observes speculative state

### 13.5 Architecture truth tests

These should look strange to a conventional team, but they are right for an
agent-written codebase:

- `persona-mind` depends on `signal-persona-mind`
- `persona-mind` depends on `persona-sema`
- `persona-mind` does not depend on router, harness, terminal, or WezTerm
- `persona-mind` does not import BEADS as a live backend
- no production code writes `<role>.lock` files
- CLI code does not open redb write transactions directly
- no polling loops exist in mind
- every mutation appends an event

## 14. Implementation Phases

```mermaid
flowchart TB
    p0["Phase 0: current scaffold"] --> p1["Phase 1: actor-backed service"]
    p1 --> p2["Phase 2: sema persistence"]
    p2 --> p3["Phase 3: typed read views"]
    p3 --> p4["Phase 4: compatibility shim"]
    p4 --> p5["Phase 5: post-commit subscriptions"]
```

### Phase 0: Current scaffold

Already present:

- signal contract
- claim reducer tests
- memory/work reducer tests
- apex architecture naming mind as central

### Phase 1: Actor-backed service

Add ractor dependency and actor tree.

Deliverables:

- `MindRootActor`
- `IngressSupervisorActor`
- `DispatchSupervisorActor`
- `DomainSupervisorActor`
- `StoreSupervisorActor`
- `ViewSupervisorActor`
- first pass of per-operation actors for claim, query, activity, and memory
- in-process CLI path using the actor tree
- no persistent daemon required yet

### Phase 2: Sema persistence

Move state truth into sema-backed redb tables.

Deliverables:

- `mind.redb` path config
- typed table setup
- migration/version marker
- persisted claims
- persisted activities
- persisted memory graph
- separate-process storage tests

### Phase 3: Typed read views

Generate typed read views from committed state. This replaces the old lock-file
workflow instead of preserving it.

Deliverables:

- view actor
- role snapshot view
- ready-work view
- view refresh failure behavior
- tests proving `<role>.lock` files are ignored by production code

### Phase 4: Compatibility shim

Rewrite `tools/orchestrate` as a caller of `mind`.

Deliverables:

- claim/release/handoff compatibility
- old orchestration protocol examples updated
- docs stating lock files are retired and replaced by mind state

### Phase 5: Post-commit subscriptions

Add push-driven change delivery.

Deliverables:

- subscription actor
- no polling
- view refresh retry triggered by commit or filesystem error recovery event
- future router/system integration points

## 15. Decisions Needed

These are the decisions I would bring back before implementation locks in the
wrong shape.

| Decision | Recommendation | Why |
|---|---|---|
| Database location | Workspace-local state path first. | Current coordination is workspace-scoped and must be easy to inspect. |
| Runtime form | Short-lived actor tree in `mind` CLI first; long-lived host only when subscriptions need it. | Gives actor discipline now without inventing daemon lifecycle too early. |
| Caller identity | Add or confirm a common request envelope carrying actor identity. | Memory/work mutations need accountability. Current reducer uses a placeholder actor. |
| View failure reply | Surface read-view failure or retry state in typed replies/events. | A committed claim with a stale role view must not look fully settled. |
| BEADS import | One-shot import only, with aliases. | Matches the workspace rule that BEADS is transitional. |
| Activity auto-logging | Every state mutation should append an event; user-visible activity may be a selected view of those events. | Avoids duplicate truth while preserving auditability. |

## 16. Final Shape

When finished, the first usable `persona-mind` stack should make this true:

```mermaid
flowchart LR
    request["typed MindRequest"] --> ingress["RequestSessionActor"]
    ingress --> dispatch["RequestDispatchActor"]
    dispatch --> operation["operation flow actor"]
    operation --> writer["SemaWriterActor"]
    writer --> transaction["single sema transaction"]
    transaction --> db[("mind.redb")]
    transaction --> event["typed Event"]
    event --> views["role and ready-work views"]
    operation --> reply["typed MindReply"]
```

If an agent wants to claim a path, hand off work, record a decision, open a
task, mark work blocked, or query ready work, it goes through mind. The
workspace can then stop using lock files as coordination state. BEADS becomes
imported history; lock files become retired migration debris.
