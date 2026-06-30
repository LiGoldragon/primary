# Situational Map: Mind, Orchestrate, And Change Closure

## Task And Scope

Read-only scout task for `/home/li/primary`: map how Mind should fit with Orchestrate and the version-control/change-closure layer. The approved alignment is that Mind, not Mine, is the non-Spirit knowledge substrate for non-intent system knowledge such as reports, architecture, specs, rationale, and eventually many comments. Spirit remains only for psyche intent. This map focuses on local source truth for Orchestrate, version-control components, claim/access authority, change event detection, commit/closure concepts, inter-component contracts, typed event schemas, actor/message patterns, and relevant tests.

Additional psyche answer incorporated during scouting: prioritize making existing architecture/report knowledge queryable first. Full multi-component integration for code/spec sync remains important but should be treated as later because it is involved.

No source files were edited, no commits were made, and no destructive commands were run. The only write was this assigned scout output under `agent-outputs/MindOrchestrateChangeClosure/`.

## Locations Inspected

- Workspace guidance: `/home/li/primary/AGENTS.md`, `/home/li/primary/ARCHITECTURE.md`, `/home/li/primary/orchestrate/AGENTS.md`, `/home/li/primary/orchestrate/ARCHITECTURE.md`, `/home/li/primary/protocols/active-repositories.md`.
- Read-only public intent queries: `spirit "(PublicTextSearch [Mind Orchestrate version control spec implementation])"`, `spirit "(PublicTextSearch [non Spirit knowledge substrate reports architecture specs rationale])"`, and `spirit "(PublicTextSearch [claim authority closure change set])"`.
- Mind surfaces: `/git/github.com/LiGoldragon/mind/AGENTS.md`, `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/mind/src/actors/choreography.rs`, `/git/github.com/LiGoldragon/mind/src/actors/subscription.rs`, `/git/github.com/LiGoldragon/mind/src/technical_seed.rs`, `/git/github.com/LiGoldragon/mind/tests/orchestrate_caller.rs`, `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`, `/git/github.com/LiGoldragon/mind/tests/daemon_wire.rs`, `/git/github.com/LiGoldragon/mind/tests/weird_actor_truth.rs`.
- Mind contracts: `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/signal-mind/src/graph.rs`, `/git/github.com/LiGoldragon/signal-mind/src/technical.rs`, `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`, `/git/github.com/LiGoldragon/meta-signal-mind/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/meta-signal-mind/schema/lib.schema`.
- Orchestrate surfaces: `/git/github.com/LiGoldragon/orchestrate/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/orchestrate/src/claim.rs`, `/git/github.com/LiGoldragon/orchestrate/src/execution.rs`, `/git/github.com/LiGoldragon/orchestrate/src/tables.rs`, `/git/github.com/LiGoldragon/orchestrate/src/divergence.rs`, `/git/github.com/LiGoldragon/orchestrate/src/repository.rs`, `/git/github.com/LiGoldragon/orchestrate/tests/ledger.rs`, `/git/github.com/LiGoldragon/orchestrate/tests/worktree.rs`.
- Orchestrate contracts: `/git/github.com/LiGoldragon/signal-orchestrate/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/signal-orchestrate/schema/lib.schema`, `/git/github.com/LiGoldragon/meta-signal-orchestrate/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/meta-signal-orchestrate/schema/lib.schema`.
- Version/change surfaces: `/git/github.com/LiGoldragon/repository-ledger/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/repository-ledger/src/lib.rs`, `/git/github.com/LiGoldragon/repository-ledger/tests/store.rs`, `/git/github.com/LiGoldragon/signal-repository-ledger/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/signal-repository-ledger/src/lib.rs`, `/git/github.com/LiGoldragon/meta-signal-repository-ledger/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/version-projection/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/signal-version-handover/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/meta-signal-version-handover/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/upgrade/ARCHITECTURE.md`.
- Version-control doctrine: `/home/li/primary/.agents/skills/version-control/SKILL.md`, `/home/li/primary/.agents/skills/repository-closeout/SKILL.md`, `/home/li/primary/.agents/skills/work-tracking/SKILL.md`, `/home/li/primary/.agents/skills/versioning/SKILL.md`.

Commands used for discovery included `sed`, `find`, `ls`, and `rg`. No tests were run; existing test files were read as evidence.

## Public Intent Grounding

Observed public Spirit records relevant to this judgment:

- `qjrf`: the intent layer holds psyche intent only, not information or belief; design-surface gaps should not be filled by agent inference and captured as psyche-authorized intent.
- `gni3`: agent-authored content is not psyche-authorized design surface by default.
- `10pz`: replace a wrong design shape rather than preserving parallel compatibility paths for systems being born.

Interpretation for this task: Mind should be the non-intent technical knowledge substrate, but Mind records should not be treated as psyche intent. Mind can hold reports, architecture facts, specs, rationale, evidence, and derived synchronization obligations, while Spirit remains the source for durable psyche direction.

## Confirmed Observations

### Workspace And Active Repo Map

- `/home/li/primary/ARCHITECTURE.md` identifies `primary` as a coordination workspace, not shipping software. Active code lives in `/git/github.com/LiGoldragon/...` and is surfaced through `repos/`.
- `/home/li/primary/protocols/active-repositories.md` lists `mind`, `signal-mind`, `meta-signal-mind`, `orchestrate`, `signal-orchestrate`, `meta-signal-orchestrate`, `repository-ledger`, version handover contracts, `version-projection`, and `upgrade` as relevant active stack pieces.
- Some active repository entries were not symlinked under `/home/li/primary/repos/` during this scout (`meta-signal-mind`, `meta-signal-orchestrate`, `version-projection`, version handover, repository-ledger), but the real repositories exist under `/git/github.com/LiGoldragon/`.

### Mind Current Surface

- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md` states that `mind` owns central workspace state: work items, typed Thought and Relation records, notes, dependencies, decisions, aliases, event history, subscriptions, channel choreography policy, and ready/blocked views.
- The same architecture explicitly says ordinary role claims, handoffs, and activity live in `orchestrate`, and that lock files are not part of the Mind implementation.
- `signal-mind` already has a typed technical dependency memory. `/git/github.com/LiGoldragon/signal-mind/src/technical.rs` defines technical node families for `Component`, `Repository`, `Crate`, `Contract`, `WorkItem`, `SourceArtifact`, `Report`, `TechnicalClaim`, `Witness`, `StorageResource`, `SchemaFamily`, and `Table`.
- `signal-mind` technical relations include `OwnsRepository`, `DefinesContract`, `DefinesCrate`, split dependency kinds, `Blocks`, `Implements`, `Documents`, `ClaimsAbout`, `ProvenBy`, `Supersedes`, and `LocatedAt`.
- The technical graph has query surfaces for about-node neighborhoods, relation neighborhoods, dependency closure, and provenance chains. The implementation and tests in `mind/tests/actor_topology.rs` exercise technical closure and provenance query behavior.
- Mind has post-commit subscription machinery for graph deltas. `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md` describes `SubscriptionSupervisor`, and `mind/tests/weird_actor_truth.rs` asserts that sema-engine deltas must become typed actor messages rather than raw table notifications.
- `signal-mind/src/graph.rs` can represent observations such as `ClaimStarted`, `ClaimReleased`, `ChannelGranted`, `ChannelRetracted`, `SessionEnded`, and a `ClaimBody` with paths/tasks and activity state. This is a Mind-side representational vocabulary, not evidence of automatic ingestion from Orchestrate.
- `/git/github.com/LiGoldragon/meta-signal-mind/schema/lib.schema` defines `AuthorityMode` as `ObserveOnly`, `ProposeOrders`, or `IssueOrders`, plus `ChoreographyMode` and `IntentSynchronizationMode`. This is the closest existing authority-grant vocabulary for whether Mind observes, proposes, or issues orders.
- `/git/github.com/LiGoldragon/mind/src/actors/choreography.rs` implements `MindOrchestrateCaller` and `ChoreographyAdjudicator` for three `OrchestrateDecision` variants: `Create`, `Retire`, and `Refresh`.
- `/git/github.com/LiGoldragon/mind/tests/orchestrate_caller.rs` proves those three injected decisions become real `meta-signal-orchestrate` frames over a Unix socket and return typed meta replies.
- The upstream policy that derives an Orchestrate decision from observations is not built. `mind/ARCHITECTURE.md` says current tests use manual decision injection and that policy derivation remains a missing slice.

### Orchestrate Current Surface

- `/git/github.com/LiGoldragon/orchestrate/ARCHITECTURE.md` says Orchestrate owns machinery: claims, handoffs, activity, agent-run lifecycle, spawn plans, scope acquisition, scheduling, escalation, lane registry, and lock-file projection. It says Mind owns state and policy truth.
- `signal-orchestrate/schema/lib.schema` defines ordinary operations: `Claim`, `Release`, `Handoff`, `Observe`, `Submit`, `Query`, `RunWorkflow`, `ObserveWorkflowRun`, `WorkflowRunObservationRetraction`, `Watch`, and `Unwatch`.
- `meta-signal-orchestrate/schema/lib.schema` defines meta operations: `Create`, `Retire`, `Refresh`, `Register`, `SetAuthority`, `RegisterWorktree`, and `RefreshWorktreeIndex`.
- Orchestrate state tables in `orchestrate/src/tables.rs` include `claims`, `roles`, `lane_registry`, `repositories`, `worktrees`, `activities`, activity slots, `divergences`, and divergence slots. They are opened through `sema-engine` with versioning policy store name `orchestrate`.
- Claim/release/handoff logic is in `orchestrate/src/claim.rs`. `apply_release` deletes the role's claim rows and returns `ReleaseAcknowledgment` with released scopes.
- Workspace protocol text in `/home/li/primary/orchestrate/AGENTS.md` says release should refuse if a claimed tracked repository contains local-only `push-*` bookmarks not ancestors of `main`. That behavior was not found in `orchestrate/src/claim.rs`; it appears documented but not implemented in the inspected release path.
- `orchestrate/src/execution.rs` handles `Watch` by allocating an observation token and `Unwatch` by returning `ObservationClosed`. `signal-orchestrate` declares `ObservationEvent` with `OperationReceived` and `EffectEmitted`, but the inspected implementation only opens/closes tokens; no event delivery path was found.
- `orchestrate/tests/ledger.rs` tests observation token allocation/closure, claim conflict/release/handoff, activity submission/query, lane registration, lane authority set, and partial downstream failure divergence recording.
- `orchestrate/tests/worktree.rs` tests `RegisterWorktree` and `RefreshWorktreeIndex`; the daemon re-derives `last_activity` and `pushed_state` instead of trusting request seed values. `PushedState` includes `Unpushed`, `Pushed`, and `AncestorOfMain` in the contract schema.
- `orchestrate/src/divergence.rs` records `PartialApplied` replies in a `divergences` table. This is a closure/recovery surface for fanned-out downstream mutations, not a spec/implementation synchronization surface.

### Repository-Ledger And Version-Control Closure

- `/git/github.com/LiGoldragon/repository-ledger/ARCHITECTURE.md` says `repository-ledger` records repository changes after they are pushed to the local Gitolite server.
- `signal-repository-ledger/src/lib.rs` defines `ReceiveHookNotification`, `PushObservation`, `CommitObservation`, `FileChange`, `Event`, `EventRecorded`, `ChangedFiles`, `CommitMessages`, and related query result types.
- `repository-ledger/src/lib.rs` stores hook notifications as typed events and push observations as event rows plus per-commit records, then answers recent repository, changed-file, and commit-message queries.
- `repository-ledger/tests/store.rs` proves typed event commit, push observation queries, fallback spool ingestion, meta repository registration, and daemon socket query behavior.
- This repository-ledger surface is post-push. It does not observe local dirty work, unpushed commits, proposed change sets, or Orchestrate claims before closure.
- Version-control doctrine in `.agents/skills/version-control/SKILL.md` and `.agents/skills/repository-closeout/SKILL.md` defines human/agent closure: inspect status, commit with `jj`, set bookmark, push, verify clean status, and close beads only with evidence. That ritual is not itself a typed runtime component.
- `version-projection` is a library for adjacent type projection and policy (`Mirror`, `DivergenceRecord`, `Reject`). `signal-version-handover` is the private daemon-to-daemon handover protocol, and `upgrade` is the runtime leg for schema/store migration and handover. These are closure surfaces for version/schema migration, not direct repo commit closure or spec synchronization.

## Current Orchestrate / Change-Closure Surfaces

Confirmed current surfaces:

- **Claim/access authority:** Orchestrate ordinary `Claim`, `Release`, and `Handoff`; scopes are paths and tasks. The daemon checks scope conflicts and owns lock-file projections. It does not currently prove cryptographic authority in the request payload; role/lane identity is data at this surface.
- **Lane authority:** `meta-signal-orchestrate` has `LaneAuthority` values `Structural` and `Support`, plus `SetAuthority`.
- **Mind authority mode:** `meta-signal-mind` has `AuthorityMode` values `ObserveOnly`, `ProposeOrders`, and `IssueOrders`. This is a policy grant surface but is not yet a proposed-change-set workflow.
- **Change activity:** Orchestrate `Submit(ActivitySubmission)` and `Query(ActivityQuery)` record/query activity by role, scope, reason, and store timestamp.
- **Worktree state:** Orchestrate `RegisterWorktree`, `RefreshWorktreeIndex`, and `Observe Worktrees` provide branch/worktree inventory and `PushedState`.
- **Post-push closure:** Repository-ledger records pushed repository events, commits, commit messages, and changed files after Gitolite receive.
- **Agent closeout doctrine:** `jj` commit/push plus bead closure evidence is documented in skills, but this is not yet a component event stream.
- **Version/schema closure:** `version-projection`, `signal-version-handover`, and `upgrade` handle daemon/store version transition, mirror, divergence, rollback/quarantine, and handover completion.
- **Partial downstream closure:** Orchestrate `PartialApplied` records successful and failed downstream mutation legs for recovery.

Likely closure points by current evidence:

- **Claim release:** end of edit ownership in Orchestrate. Implemented as claim deletion and `ReleaseAcknowledgment`; documented release gating against unpushed work is missing in code.
- **Commit/push:** human-agent closeout in version-control doctrine; post-push becomes runtime-visible through repository-ledger.
- **Repository-ledger event sequence:** durable post-push observation sequence for changed files and commit messages.
- **Bead close:** durable work-item closeout in current tracker doctrine; future target is Mind work items, per `/home/li/primary/orchestrate/AGENTS.md` "Blocked Work".
- **Version handover completion:** daemon-version closure point for storage/wire migrations.

## Existing Or Missing Event Boundaries Mind Can Consume

Existing consumable boundaries:

- `signal-mind` can accept technical nodes/relations for reports, artifacts, claims, witnesses, repositories, contracts, work items, and dependency/provenance links.
- Mind graph subscriptions can push post-commit deltas out to consumers.
- Mind can issue a small implemented set of meta Orchestrate orders (`Create`, `Retire`, `Refresh`) through `MindOrchestrateCaller`.
- Orchestrate has an ordinary `Watch`/`Unwatch` observer contract and schema-level `ObservationEvent` variants.
- Repository-ledger has queryable post-push events, commit messages, and changed files.

Missing or incomplete boundaries:

- Orchestrate observer delivery is not implemented beyond token open/close in the inspected code. Mind cannot yet subscribe to a real stream of claim/release/handoff/activity/worktree events from Orchestrate.
- The documented release gate for local-only `push-*` bookmarks was not found in the Orchestrate release implementation.
- There is no typed proposed change-set object tying together claimed scopes, intended implementation changes, required spec/doc updates, validation evidence, commit identifiers, and final closure.
- There is no direct runtime bridge from repository-ledger push events into Mind technical graph records.
- There is no observed event that says "implementation changed and spec now requires review" or "spec changed and implementation work is required." Existing technical graph relations can model this once an ingest/adjudication policy creates the nodes/relations.
- `meta-signal-mind` policy modes exist, but `mind/ARCHITECTURE.md` says meta policy storage/evaluation remains destination work. The current Mind-to-Orchestrate path is manual decision injection, not policy-derived authority.
- Repository-ledger is post-push only. It cannot detect uncommitted local changes or local-only commits before push.

## Interpretation

Mind already has the right substrate shape for non-Spirit system knowledge. The strongest fit is to use `signal-mind` technical memory as the canonical graph for specifications, architecture reports, technical claims, rationale, evidence, source artifacts, repositories, contracts, and work items. Spirit should not receive those facts unless the psyche states durable intent.

Orchestrate should remain the owner of active coordination and access control. Claims, releases, handoffs, lane authority, and worktree inventory belong there. Mind should consume Orchestrate facts as observations and issue Orchestrate meta orders only through a configured authority mode.

Repository-ledger should remain the post-push source for what actually changed in version control. It can feed Mind with commit/file evidence after closure. It should not be stretched into pre-commit work ownership, because Orchestrate already owns active work and worktree state.

The missing middle is a typed closure/change-set boundary. Today the lifecycle is split across Orchestrate release, `jj` commit/push doctrine, repository-ledger post-push facts, and tracker closeout. None of those alone expresses "this implementation change affects these specs" or "this spec/rationale change requires implementation." Mind can represent the resulting obligations, but the current stack does not yet emit them as first-class events.

## Recommended First Integration Slice

First slice: make existing architecture/report knowledge queryable in Mind, without coupling Orchestrate, repository-ledger, and version-control closure yet.

Suggested shape:

1. Select a small public corpus: current repo `ARCHITECTURE.md` files, existing public reports relevant to Mind/Orchestrate, and perhaps `protocols/active-repositories.md`. Avoid private report paths.
2. Ingest that corpus into `signal-mind` technical graph records using existing node families: `Report`, `SourceArtifact`, `Repository`, `Component`, `Contract`, `TechnicalClaim`, and `Witness`.
3. Use existing relations to make the corpus navigable: `Documents` for reports/source artifacts to documented nodes, `ClaimsAbout` for extracted technical claims, `ProvenBy` for evidence links, `LocatedAt` for path/source location, `DefinesContract` and dependency relations where already explicit in architecture docs.
4. Keep extraction evidence-backed and conservative. A first pass can record coarse claims and source locators rather than trying to parse every section into perfect semantic atoms.
5. Prove queryability through existing Mind query surfaces: `QueryTechnicalNodes`, about-node neighborhoods, relation neighborhoods, dependency closure, and provenance chains. The acceptance proof should be "a fresh agent can ask Mind what is known about a component/contract/report and receive linked source-backed records."
6. Keep Mind in a knowledge-store role for this slice. Do not implement Orchestrate event ingestion, repository-ledger ingestion, release gates, or automatic spec/implementation work creation in the first slice.

Later coupling points to name but not include in the first slice:

- Orchestrate observer delivery: implement real `Watch` events for claim/release/handoff/activity/worktree/divergence changes, then have Mind consume them as observations and technical graph updates.
- Orchestrate release closure: either implement or explicitly defer the documented release-time unpushed-bookmark gate; later link accepted release facts to Mind work items and technical claims.
- Repository-ledger post-push ingestion: map pushed commits and changed files into Mind source artifacts/witnesses after repository-ledger records them.
- Proposed change sets: introduce an explicit typed object only after the queryable knowledge graph proves useful. Until then, use existing `WorkItem`, `TechnicalClaim`, `Witness`, and relation records.
- Authority escalation: start later coupling in `AuthorityMode::ObserveOnly` or `ProposeOrders`; reserve `IssueOrders` for a policy-backed phase after observation/proposal behavior is trustworthy.

This revised slice honors the approved direction while keeping the first implementation tractable: Mind becomes useful as a queryable non-Spirit knowledge substrate before it tries to synchronize live code/spec change loops across multiple components.

## Risks And Unknowns

- I did not inspect private repositories or private reports. No private-sensitive details are included.
- I did not run any tests; all test evidence is from source inspection.
- I did not inspect every active Persona component. Router/harness/meta-signal-router may add authority details relevant to channel grants, but the requested Orchestrate/version-control/change-closure path is covered by the inspected sources.
- The Orchestrate observer contract may need richer event payloads than current `OperationReceived(OperationKind)` and `EffectEmitted { operation, outcome }` if Mind must build precise technical graph facts without polling follow-up snapshots.
- The term "proposed change set" is not represented in the current contracts. The closest existing nouns are Mind work items/technical claims, Orchestrate claims/activities/workflows, and repository-ledger push observations.
- `repository-ledger` source and architecture differ from its `schema/signal-repository-ledger.concept.schema`, which is much thinner than the implemented Rust contract. I treated `src/lib.rs`, tests, and architecture as stronger source truth for current behavior.
- Current `mind` architecture still references eliminated old paths such as `~/primary/ESSENCE.md` in text. That does not affect the mapped runtime surfaces, but it is stale documentation around context references.
