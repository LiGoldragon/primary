# 6 — orchestrate → production on the schema/triad-engine base

Per-component port map for the 75 session. READ-ONLY source sweep of
`/git/github.com/LiGoldragon/orchestrate` and its contract repos
(`signal-orchestrate`, `owner-signal-orchestrate`), the engine-management
surfaces (`signal-engine-management`, `owner-signal-persona`,
`signal-persona::engine_management`), and `mind/src/supervision.rs`, all read
2026-06-05. Grounded against the spirit-pilot recipe (report 3), the rulebook
(report 1, rules R1-R37), and the binding intent (report 2). Landed-vs-proposed
honesty is enforced throughout: where a port step depends on something not yet
in source, it is marked.

orchestrate is the **most advanced** of the three targets and the **furthest
from the runner shape in one specific way**: it is a `std::thread`-based
hand-daemon built out of **free functions**, carrying OLD versioned schemas
plus a concept schema — none of it the three-plane triad. It is also the
component the apex intent (`tq18`/`mazv`) says **runs the daemon set**, which
makes the supervision-ownership question (§7) the single most consequential
design decision in this map.

## 1. Current architecture (source-grounded)

### 1.1 The daemon shape — threads + free functions, three sockets

`orchestrate/src/daemon.rs` is a hand-written `std::thread` daemon, NOT a
Kameo actor and NOT the triad-runtime runner. `OrchestrateDaemon::run(self)`
binds three Unix sockets and spawns one OS thread per socket:

- `thread::spawn(move || accept_ordinary(ordinary_listener, ordinary_service))`
- `thread::spawn(move || accept_owner(owner_listener, owner_service))`
- `thread::spawn(move || accept_upgrade(upgrade_listener, ...))`

Every dispatch function is a **module-level free function** — `accept_ordinary`,
`accept_owner`, `accept_upgrade`, `handle_ordinary_stream`, `handle_owner_stream`,
`handle_upgrade_stream`, `bind_socket(path: &Path)`, `read_length_prefixed`,
`validate_ordinary_request_header`, `validate_owner_request_header`,
`validate_upgrade_request_header`, `reply_finalized_handover`,
`remove_socket_path`. This is a direct **R26 violation** (every function must be
a method/associated function on a non-ZST data-bearing type or a trait impl;
free functions forbidden outside `fn main()`/`#[cfg(test)]`). The same free-fn
pattern recurs in `lock_projection.rs` (`lock_line`, `scope_text`), `role.rs`
(`current_workspace_harness`, `create_report_lane`), `claim.rs` (`scopes_overlap`,
`scope_contains`, `path_contains`), `lane.rs` (`pascal_to_kebab`, `ordinal_word`),
`handover.rs` (`civil_date_from_unix_days`), `execution.rs` (`single_command`),
and `service.rs` (`reject_handover`, `first_committed_payload`).

The shared state is `Arc<OrchestrateService>` cloned into each thread, with
inner-handler-per-connection threads spawned per accepted stream
(`thread::spawn(move || { handle_ordinary_stream(...) })`). This is the OLD
hand-daemon concurrency model, not the runner's bind→start→serve loop and not
the engine-trait composition.

### 1.2 The wire surface — signal-frame / executor, not the engine traits

`OrchestrateService` (`service.rs`) is the dispatch core. It holds the sema
tables, the layout, and three mutexes (`sequence`, `next_observation_token`,
`handover`). It dispatches through the **`signal-executor`** machinery:
`execute_request` builds `Executor::new(OrdinaryLowering, command_executor,
ObserverSet::no_op())` and `futures::executor::block_on(executor.execute(request))`.
This is the pre-triad executor/lowering stack, NOT `SignalEngine`/`NexusEngine`/
`SemaEngine`. The crate does **not** depend on `triad-runtime` or
`schema-rust-next` (verified: zero matches in `Cargo.toml`). No engine trait is
implemented anywhere in `src/`.

The Layer-2 Component Commands exist as hand-written enums in `execution.rs`:
`OrdinaryCommand [Claim Release Handoff Observe Submit Query Watch Unwatch]` and
`OwnerCommand [Create Retire Refresh Register SetAuthority]`, each with a
`Lowering` impl (`OrdinaryLowering`/`OwnerLowering`) translating contract
operations to commands, and a `CommandExecutor` impl running them. This is
genuinely the richest internal-feature set of the three components — and ALL of
it is hand-written `match` logic invisible to any schema (the **R5/`z6qu`
violation**: not one of these features is a declared Nexus verb+object).

### 1.3 The schema form — concept schema PLUS legacy versioned generation

`orchestrate/schema/` carries the most schema debt of the three targets:

- `orchestrate.concept.schema` (the concept form — flat operation lists +
  trailing namespace; verified head is the OLD shape with `OperationKind`,
  `SemaObservation`, an `EffectEmitted (SemaObservation)` observation event)
- `orchestrate-v0-1.schema`, `orchestrate-v0-1-1.schema`,
  `orchestrate-types-v0-1.schema`, `orchestrate-storage-v0-1.schema` — the
  pre-`schema-next` versioned generation (the concept schema `Import`s
  `./orchestrate-types-v0-1.schema` and `./orchestrate-storage-v0-1.schema`).

None of these is `schema/{signal,nexus,sema}.schema` (the three-plane split,
R1). There is no `build.rs` emitting `src/schema/*.rs` (verified: no `build.rs`
in repo root). The wire types come from the **published contract crates** via
`signal_frame::signal_cli!` and direct `use signal_orchestrate::*` /
`use owner_signal_orchestrate::*`, NOT from local schema emission.

### 1.4 The contract repos — owner-signal, not meta-signal; concept stubs

- `signal-orchestrate` — `schema/signal-orchestrate.concept.schema` (concept
  form) + a 33KB hand-written `src/lib.rs`. The ordinary peer surface:
  `Claim Release Handoff Observe Submit Query Watch Unwatch`.
- `owner-signal-orchestrate` — `schema/owner-signal-orchestrate.concept.schema`
  + a 7KB `src/lib.rs`. The owner surface: `Create Retire Refresh Register
  SetAuthority`. **Named `owner-signal-*`** — the R14/`r9qy` rename to
  `meta-signal-orchestrate` is required and has NOT run (verified: no
  `meta-signal-orchestrate` checkout exists on disk).

Both contracts carry the **Sema classification vocabulary on the public wire**
(the R24/`7l7l` violation, which names `signal-orchestrate` directly):
`signal-orchestrate.concept.schema` declares `SemaObservation [Asserted
Retracted Mutated Matched Subscribed NoChange]` and an `EffectEmitted
(SemaObservation)` observation event, plus an `OperationKind` mirror. These must
move to domain-named events below the public contract.

### 1.5 The state plane — already on sema-engine (the one strong base alignment)

`tables.rs` opens ONE `orchestrate.redb`/`.sema` through `sema-engine`
exclusively (`Engine::open(EngineOpen::new(store.as_path(),
ORCHESTRATE_SCHEMA_VERSION))`), with no raw `redb::` anywhere. This satisfies
**R18** (one sema-engine DB per component) and the `fosp` correction
out-of-the-box. Eight tables exist: `claims`, `roles`, `lane_registry`,
`repositories`, `activities`, `activity_next_slot`, `divergences`,
`divergence_next_slot`. Stored types (`StoredClaim`, `StoredRole`,
`StoredRepository`, `StoredActivity`, `StoredDivergence`) are rkyv-archived. The
store is **mutex-held inside `OrchestrateService`**, not a single-writer Kameo
actor — same shape as spirit's `Store` limit; acceptable for the port, the
`e440` single-writer-actor target is deferred.

ARCHITECTURE.md §5 names FIVE more policy/working tables as **missing**
(`scheduling_policy`, `supervision_policies`, `agent_runs`, `spawn_plans`,
`agent_executors`, `scope_acquisitions`, `channel_grants`, `escalation_state`,
`claim_archive`). So the SEMA plane is real but partial relative to the
component's stated destination.

### 1.6 The Mirror upgrade-handover surface — a distinct third socket

`handover.rs` + `service.rs` implement a third "upgrade" socket speaking
`signal-version-handover`: `MirrorSnapshot::capture` (claims + lanes),
`into_mirror_payload`/`from_mirror_payload` (rkyv archive with component/kind/
target-version validation), and a `HandoverState [Active Ready Complete]` state
machine (`ask_handover_marker`/`ready_to_handover`/`handover_completed`/
`restore_mirror`/`recover_handover`). After `HandoverCompleted`, the daemon
retires its ordinary+owner socket paths (`remove_socket_path`). This is real,
working upgrade machinery — but it is the OLD `signal-version-handover` path, NOT
the schema-rust-next `UpgradeFrom`/`AcceptPrevious` traits (which report 3 marks
PROPOSED, nothing implements them). It maps to the `veqq`/sema-upgrade
deployment concern.

### 1.7 The CLI — clean, one-line, one peer

`src/bin/orchestrate.rs` is a single line:
`signal_frame::signal_cli!(orchestrate, signal_orchestrate);`. The daemon binary
`src/main.rs` reads exactly one NOTA config argument (`DaemonConfiguration`
decoded via `nota_codec`) and rejects flags. This satisfies **R19** (single
argument), **R21** (CLI has one Signal peer, no DB), and **R22** is handled by
the `signal_cli!` macro. The config record (`configuration.rs`) carries
`store_path`, three socket paths, `workspace_root`, `git_index_root` as
`WirePath` fields — already the right argv shape; the port keeps it.

### 1.8 ShortHeader validation — present on both sockets (a real base strength)

`validate_ordinary_request_header` / `validate_owner_request_header` /
`validate_upgrade_request_header` each compare the frame `ShortHeader` against
the decoded request root kind and reject mismatches before service state can
mutate (`OperationDispatchError::HeaderOperationMismatch`). This is exactly the
"ordinary socket rejects owner frame / owner socket rejects ordinary frame"
witness behavior (R12 witness shape) — already implemented, just in free-fn
form. The port preserves this behavior under the runner's per-listener handler.

### 1.9 Build/test status today

Tests exist: `tests/{architecture,daemon_cli,handover,ledger,schema_contract,
smoke}.rs` (production daemon + production CLI socket witnesses, handover
witnesses, sema-backed ledger witnesses, CLI-boundary source-scan witnesses).
No built binaries were found under `target/debug/` at sweep time, so I cannot
assert a fresh green (READ-ONLY discipline — I did not build or run). The
crate's deps are all pre-triad: `signal-orchestrate`, `owner-signal-orchestrate`,
`signal-executor`, `signal-frame`, `signal-sema`, `signal-version-handover`,
`sema`, `sema-engine`, `nota-codec`, `version-projection`. Status is best read
as: **the OLD-stack daemon is feature-complete and tested for its MVP slice;
the triad-engine port has not begun** (no triad-runtime/schema-rust-next deps,
no plane schemas, no engine traits).

### 1.10 INTENT.md / ARCHITECTURE.md alignment

Both repo files explicitly name the pending migration: INTENT.md "Pending
schema-engine upgrade" and ARCHITECTURE.md §"Pending schema-engine upgrade"
both describe converting to "a single `orchestrate/orchestrate.schema` file"
emitted by `primary-ezqx.1`. **This single-file framing is now STALE** — the
`lc2r` (VeryHigh) correction settles that a component is AT LEAST THREE separate
plane schema files (wire-only contracts + in-daemon `nexus.schema`+`sema.schema`),
and the spirit single-file schema is a named bootstrap exception, NOT the
template. Updating that framing is itself a porting-branch task (§9).

## 2. The gap to the base (vs the spirit-pilot recipe in report 3)

| Recipe element (report 3) | spirit (reference) | orchestrate today | Gap |
|---|---|---|---|
| Three plane schema files | `schema/{signal,nexus,sema}.schema` | concept + 4 legacy versioned schemas | **Author all three; delete legacy** (R1) |
| `build.rs` emits `src/schema/*.rs` | ~38-line driver | none | **Add build.rs + GenerationPlan** |
| `SignalEngine` impl (triage) | `SignalActor` | none (signal-frame dispatch in free fns) | **Implement on a data-bearing actor** (R6) |
| `NexusEngine` impl (heavy logic) | `Nexus` | none (logic in Lowering/CommandExecutor) | **Implement; enumerate features as Nexus verbs** (R5/R9) |
| `SemaEngine` impl (durable) | `Store` over sema-engine | `OrchestrateTables` over sema-engine (no trait) | **Wrap existing tables in SemaEngine** (R6) |
| `on_start`/`on_stop` lifecycle | all three engines | none | **Add; typed failures** (R7/`czw0`) |
| Runner loop (`NexusEngine::execute`) | emitted | none | **Wire via triad-runtime** (R9/R11) |
| Effects (`run_effect`) | `Stash`/`ClassifyState` | none (no NexusAction set) | **Declare effect catalog if needed** (R10) |
| Daemon shell | `SingleListenerDaemon` | `std::thread` + free fns | **Port to `MultiListenerDaemon`** (R13) |
| Two-tier authority | single-listener (spirit) | three threads/sockets | **Already two-tier; re-base on runner** (R12) |
| meta-signal contract | n/a | `owner-signal-orchestrate` | **Rename** (R14/`r9qy`) |
| No Sema words on wire | clean | `SemaObservation`/`EffectEmitted` on wire | **Move below contract** (R24/`7l7l`) |
| sema-engine DB boundary | yes | yes | **Already satisfied** (R18) — strongest alignment |
| Single NOTA argv, one-peer CLI | yes | yes | **Already satisfied** (R19/R21) |
| ShortHeader cross-socket reject | n/a (single) | yes | **Already satisfied** (R12 witness) |

The headline: orchestrate's **state plane, argv shape, CLI, and authority-tier
separation are already base-aligned**; the **engine-trait runtime, the
three-plane schemas, the Nexus feature catalog, and the meta-signal rename**
are the work. The free-function daemon is the largest mechanical violation.

## 3. The port plan — ordered concrete steps

### 3.1 Plane schemas to author

**Contract repos (WireContract emission, engine-free — `lc2r`/`l6zw`/R4):**

`signal-orchestrate/schema/signal-orchestrate.schema` — wire-only. Keep the
eight domain operation roots (`Claim Release Handoff Observe Submit Query Watch
Unwatch`) and all payload/reply nouns, but **drop `SemaObservation`,
`EffectEmitted`, and the `OperationKind` mirror from the public wire**
(R24/`7l7l`). The observation event keeps `OperationReceived` but re-labels the
effect event to a domain noun (e.g. `OutcomeRecorded` carrying a domain
classification, not the six Sema words). Root enum already has ≥2 variants (R3
satisfied). Emit as `WireContract` (types + NOTA codec only).

`meta-signal-orchestrate/schema/meta-signal-orchestrate.schema` — the renamed
owner surface (was `owner-signal-orchestrate`). Keep `Create Retire Refresh
Register SetAuthority`. Per `cgd8` this is where daemon-configuration verbs
live; the existing five owner verbs ARE policy/configuration mutations, so they
belong here unchanged. Emit as `WireContract`.

**In-daemon plane schemas (inside the orchestrate crate):**

`orchestrate/schema/signal.schema` — emits `SignalEngine` (SignalRuntime
target). Its `Input` root is the UNION of the two wire surfaces tagged by
listener so one runner handles both sockets (the `MultiListener` pattern from
report 3): the ordinary eight verbs + the meta five verbs, each importing the
wire-contract IO from `signal-orchestrate` and `meta-signal-orchestrate`. The
triage methods are `triage_inner` (admission + ShortHeader validation +
identity-stamping — porting the existing `validate_*_request_header` behavior)
and `reply_inner`.

`orchestrate/schema/nexus.schema` — emits `NexusEngine` (NexusRuntime). **This
is the load-bearing authoring step (R5/`z6qu`): every internal feature becomes
a declared Nexus verb+object.** See §3.2.

`orchestrate/schema/sema.schema` — emits `SemaEngine` (SemaRuntime). Declares
`WriteInput`/`ReadInput`/`WriteOutput`/`ReadOutput` over the existing eight
tables. See §3.3.

### 3.2 The Nexus feature catalog (R5/`z6qu`) — the verbs+objects to declare

orchestrate has the richest decision logic of the three; today it is hidden
inside `ClaimLedger`, `RoleRegistry`, `LaneRegistry`, `ActivityLedger`,
`RepositoryRegistry`, `DivergenceLedger`. Each named internal feature must
become a declared Nexus verb+object BEFORE its Rust body. The catalog (one
verb+object per feature, grouped):

Claim/scope adjudication (from `claim.rs`):
- `(AdjudicateClaim RoleClaim)` — the conflict check (`conflicts_for`,
  `scopes_overlap`, `scope_contains`, `path_contains` — the directory-containment
  rule "claiming a dir claims all below it" is a Nexus feature, not inline)
- `(ApplyRelease RoleRelease)`
- `(AdjudicateHandoff RoleHandoff)` — source-holds-all + target-conflict check
- `(SnapshotRoles Observation)` — role status + recent-activity-limit (the
  `ROLE_OBSERVATION_ACTIVITY_LIMIT = 20` is a declared filter, not a magic const)

Role registry (from `role.rs`):
- `(CreateRole CreateRoleOrder)` — the existence checks (role/repo/lane already
  exists) each become a declared rejection branch
- `(RetireRole RetireRoleOrder)`
- `(SeedWorkspaceRoles WorkspaceSeed)` — the startup seeding (currently a
  hardcoded `current_workspace_harness` match) becomes a declared feature

Lane registry (from `lane.rs`):
- `(RegisterLane LaneRegistrationRequest)` — including `derive_identifier`
  (pascal→kebab, authority suffix, ordinal disambiguation) as a declared
  derivation
- `(RetireLane LaneIdentifier)`, `(SetLaneAuthority LaneAuthorityChange)`,
  `(ObserveLanes Observation)`

Activity (from `activity.rs`):
- `(SubmitActivity ActivitySubmission)`, `(QueryActivity ActivityQuery)` — the
  `ActivityFilter` evaluation is a declared filter feature

Repository refresh + divergence:
- `(RefreshRepositoryIndex RefreshRepositoryIndexOrder)`
- `(RecordDivergence PartialApplied)` — the partial-application recovery rule

The `NexusWork` enum carries `SignalArrived`, `SemaWriteCompleted`,
`SemaReadCompleted`, `EffectCompleted`; `NexusAction` carries the 5-variant set
(`ReplyToSignal`, `CommandSemaWrite`, `CommandSemaRead`, `CommandEffect`,
`Continue`). The lock-file projection (`lock_projection.rs`) is the main
effect candidate (§3.4).

### 3.3 The SEMA plane (state — already on sema-engine)

orchestrate is NOT a stateless carve-out — it has the richest durable state.
The port wraps the existing `OrchestrateTables` in a `SemaEngine` impl. The
SEMA roots map onto the existing operations:
- `WriteInput [(RecordClaim ...) (RemoveClaims ...) (InsertRole ...)
  (RemoveRole ...) (ReplaceLanes ...) (ReplaceRepositories ...)
  (AppendActivity ...) (AppendDivergence ...)]`
- `ReadInput [(ObserveClaims ...) (ObserveRoles ...) (ObserveLanes ...)
  (ObserveRepositories ...) (ObserveActivities ...) (ObserveDivergences ...)
  (CountActivities ...)]`
- matching `WriteOutput`/`ReadOutput` reply enums.

`apply_inner(&mut self)` serializes writes; `observe_inner(&self)` runs parallel
reads — the existing `storage_kernel().write`/`.read` closures map straight onto
these. The existing `current_commit_sequence()` feeds the handover marker. The
slot-allocation logic (`ActivitySlot`, `next_activity_slot`) stays inside SEMA.
**Note (`ox7e`):** if the role-registry / claim-key storage shapes don't map
cleanly onto the generated SEMA surface (the `ClaimKey`/`ScopeKey` string-format
keys are an R27 smell — typed identity hidden in `format!` strings), the right
move is to improve the shared sema-engine identified-table surface so generated
SEMA expresses real storage identity, not to bend orchestrate.

### 3.4 Effects

The one clear effect is **lock-file projection** (`LockProjection::project`
writes `orchestrate/<role>.lock` files). This is a filesystem side-effect after
accepted state mutation — exactly a `CommandEffect`. Declare
`NexusEffectCommand [(ProjectLocks ...)]` / `NexusEffectResult [(LocksProjected
...)]`. `create_report_lane` (symlink creation in `role.rs`) and the
`create_dir_all` calls in `RoleRegistry::create_role` are also filesystem
effects that should become declared effects rather than inline `std::fs` calls
inside the decision path. `Stash` (the universal candidate, R10) is likely not
needed.

### 3.5 The runner wiring — MultiListenerDaemon (R13)

orchestrate already runs three sockets, so it is the natural **first real
`MultiListenerDaemon` consumer**. Define the listener-tag enum
`OrchestrateListener [Ordinary Meta Upgrade]`. Implement
`MultiListenerRuntime` with `type Listener = OrchestrateListener`,
`start`/`stop` (calling the engine `on_start`/`on_stop`), and
`handle_stream(&mut self, listener, stream)` routing each tagged stream into the
unified `SignalEngine` triage → `NexusEngine::execute` runner. Construct via
`MultiListenerDaemon::new([ListenerSocket::new(Ordinary, ordinary_path),
ListenerSocket::new(Meta, meta_path), ListenerSocket::new(Upgrade,
upgrade_path)], runtime, RequestErrorLog::new("orchestrate-daemon"))`.

**HONESTY (R13):** there is NO worked two-socket triad-engine daemon yet —
spirit is single-listener; `MultiListenerDaemon` is committed in triad-runtime
(`28d03c3`) with 2 passing witness tests but **unexercised by any reference
daemon**. A porter wiring orchestrate's three sockets onto `MultiListenerRuntime`
is doing it for the first time. orchestrate's existing three-thread daemon is
the only same-component precedent, but it is the OLD shape, not the runner.

The **upgrade socket** is a wrinkle: it speaks `signal-version-handover`, not an
orchestrate plane contract. Two readings (open decision, §8): (a) keep it as a
third listener tag routed to the existing handover state machine outside the
Nexus loop; or (b) fold handover into the meta-signal surface as
configuration/lifecycle verbs. Reading (a) preserves working behavior with least
risk for the first port.

### 3.6 The CLI

Keep the one-line thin CLI. After the rename, it stays
`signal_cli!(orchestrate, signal_orchestrate)` for the ordinary surface; a
separate owner CLI path (or an owner mode on the same binary) connects to the
meta socket. No direct-store path (R21) — already satisfied.

### 3.7 Bootstrap policy (R16/R17/`7x50`)

ARCHITECTURE.md §5 references `bootstrap-policy.nota` as the first-start policy
seed, but **it does NOT exist on disk** (verified: no `bootstrap-policy.nota` in
the repo root — invariant-on-paper only). The five policy tables it would seed
(`scheduling_policy`, `supervision_policies`, lane-registry seed) are also
mostly the "missing" tables from §1.5. Per `7x50` the production form is a
PRE-ENCODED binary artifact consumed once at first start, not NOTA parsed at
runtime. **The port establishes this pattern in code** (no worked example exists
in the base — report 3 R17 confirms spirit has none). For the first port slice,
the working state (claims/activities) needs no bootstrap; the lane-registry seed
(`seed_current_workspace_roles`, currently a hardcoded match in `role.rs`) is
the candidate for bootstrap-once policy. This is a real new-pattern step, not a
copy.

## 4. Witness tests (specialized to orchestrate)

From the component-triad witness table + the architectural-truth-test discipline
(R35/R36), positive-proves-the-path + negative-guards-the-shortcut, cheapest
sufficient layer:

- `orchestrate-signal-nexus-sema-chain-records-then-observes-a-claim` —
  Layer-2 chain witness: drive a `Claim` through `SignalEngine` →
  `NexusEngine::execute` → `SemaEngine::apply`, then `Observe` through to
  `SemaEngine::observe`, asserting via generated root types (R36). The
  testing-trace socket records prove the engine-trait methods were actually
  called (not a re-implementation bypass).
- `orchestrate-ordinary-socket-rejects-meta-frame` /
  `orchestrate-meta-socket-rejects-ordinary-frame` — the two-tier authority
  witnesses (R12). The existing `validate_*_request_header` behavior already
  proves this on the OLD daemon (`tests/daemon_cli.rs`); the port re-asserts it
  on the `MultiListener` handler.
- `orchestrate-claim-adjudication-rejects-overlapping-path-scope` (positive) +
  `orchestrate-directory-claim-covers-paths-below-it` — proves the
  scope-containment Nexus feature is driven through the declared verb, not
  inline.
- `orchestrate-handoff-requires-source-holds-exact-scope` — the handoff
  adjudication Nexus feature.
- `orchestrate-lock-projection-effect-fires-after-accepted-mutation` — proves
  `ProjectLocks` runs as a declared `CommandEffect`, and a negative guard that a
  REJECTED claim does NOT project (removal-breaks-behavior, Layer 3).
- `orchestrate-binary-rejects-flag-style-arguments` (R19) +
  `orchestrate-cli-cannot-open-any-database-or-peer-socket` (R21) — the existing
  `tests/architecture.rs` source-scan witnesses, kept and strengthened to
  runtime.
- `orchestrate-daemon-rejects-non-signal-traffic-on-its-socket` (R20).
- `orchestrate-sema-persists-claims-across-reopen` — mirror spirit's persistence
  witness over `orchestrate.sema`.
- `orchestrate-no-sema-vocabulary-on-public-wire` — negative grep/compile guard
  that the renamed `signal-orchestrate.schema` carries no `Assert/Mutate/Retract/
  Match/Subscribe/Validate` request roots and no `SemaObservation` mirror (R24).
- `orchestrate-mirror-snapshot-round-trips-claims-and-lanes` — keep the existing
  handover witnesses (`tests/handover.rs`).
- `orchestrate-no-free-functions-outside-main-and-tests` — a compile/source-scan
  witness proving the R26 cleanup landed (the most-violated rule today).
- (If supervision lands, §7) `orchestrate-answers-engine-management-announce-
  readiness-health-stop` — proves the engine-management child surface.

## 5. Blockers — real foundation dependencies (honest)

1. **The `owner-signal-orchestrate` → `meta-signal-orchestrate` rename has not
   run.** `meta-signal-orchestrate` does not exist on disk. `r9qy` calls the
   fleet rename "active work" across 13 named repos (INCLUDING
   `owner-signal-orchestrate`), but it is a PENDING operation, not done. The
   two-listener wiring naming a "meta socket" describes a repo that must first be
   created/renamed. **Hard prerequisite for the meta-tier port step** (R13/R14).
2. **No worked two-socket triad-engine daemon exists.** `MultiListenerDaemon` is
   committed + tested in triad-runtime but unexercised by any reference daemon
   (spirit is single-listener). orchestrate's port is the first — establishing
   the pattern, not following it (R13).
3. **`triad_main!` macro does not exist** — the daemon shell + listener wiring is
   hand-written every time (R11; verified empty grep in report 3). Budget real
   (small) code.
4. **`bootstrap-policy.nota` is invariant-on-paper** — not present in spirit OR
   orchestrate; the port introducing policy bootstrap establishes the pattern
   (R17/`7x50`).
5. **The payload-less-variant dual-lowering concern is NOT cleared for
   orchestrate's own schema.** Report 3 could not confirm/deny a `primary-vllc`
   dual-lowering defect from the base repos. orchestrate has MANY payload-less
   variants (`Observation [Roles Lanes]`, `LaneAuthority [Structural Support]`,
   `HarnessKind [Codex Claude]`, `RoleCreationRejectionReason [...]`,
   `OwnerOrchestrateUnimplementedReason [...]`, the handover-rejection reasons).
   A porter MUST verify schema-rust-next emits these payload-less variants
   correctly before assuming the schema authoring step is unblocked.
6. **sema-upgrade / `veqq` gates DEPLOY-and-iterate, not compile.** orchestrate
   is stateful; a deployed daemon coming up against an existing
   `orchestrate.sema` after a contract edit needs schema stability OR a migration
   path. The existing `signal-version-handover` Mirror machinery partially
   addresses this, but the schema-rust-next `UpgradeFrom`/`AcceptPrevious` path
   is PROPOSED (report 3). This gates the running-system target (`mazv`), not the
   port-to-compile.
7. **Authority-chain sequencing (INTENT.md + ARCHITECTURE.md §2 + `ojuh`).**
   orchestrate's outbound owner calls go to `owner-signal-persona-router` and
   `owner-signal-persona-harness`; INTENT.md says orchestrate cuts over AFTER
   Spirit and mind because the authority chain is `mind → orchestrate →
   router/harness`. So orchestrate's full integration depends on the contracts at
   both ends being on the schema engine. The standalone triad port can proceed
   independently, but the running-system wiring waits.

## 6. Open decisions for the psyche

(See also report 2 §E for the session-wide open forks.)

1. **Does the engine-management supervision surface belong in orchestrate, and is
   porting mind's template the right move?** §7 argues NO for the manager surface
   and YES (deferred) for the child surface — but this is the directive question
   and needs psyche confirmation.
2. **The upgrade socket: keep as a third listener tag, or fold handover into the
   meta-signal surface?** (§3.5). Reading (a) keep-separate is lowest-risk for
   the first port; (b) fold-in is cleaner long-term but couples handover to the
   meta contract.
3. **Is `signal-version-handover` (the OLD Mirror path) the durable upgrade
   mechanism, or does it get replaced by schema-rust-next `UpgradeFrom`/
   `AcceptPrevious`?** orchestrate has the most invested in the OLD path of the
   three; the answer shapes how much of `handover.rs` survives the port.
4. **The five "missing" policy/working tables** (`scheduling_policy`,
   `supervision_policies`, `agent_runs`, `spawn_plans`, `agent_executors`,
   `scope_acquisitions`, `channel_grants`, `escalation_state`): port the
   existing slice first (claims/roles/lanes/activities/divergences) and add these
   incrementally, or design the full SEMA plane up front? Recommendation:
   port-the-slice-first per `ojuh` (make it usable enough to replace
   `tools/orchestrate`).
5. **The string-formatted storage keys** (`ClaimKey`/`ScopeKey` via `format!`)
   are an R27 typed-identity-in-strings smell. Fix during the port (typed
   composite keys / improve sema-engine identified-table surface per `ox7e`), or
   carry forward? Recommendation: fix during the SEMA-plane authoring.

## 7. The supervision-ownership decision (the directive question)

**Finding: the engine-management MANAGER surface does NOT belong in orchestrate.
Orchestrate should implement the engine-management CHILD surface (like mind),
deferred to the running-system slice. Porting mind's `supervision.rs` template is
the right move ONLY for that child surface, not as a manager.**

The source resolves this cleanly. There are TWO distinct surfaces:

- `signal-engine-management` (and the bundled `signal_persona::engine_management`
  module that `mind/src/supervision.rs` actually imports) is the **ordinary
  peer-callable lifecycle contract** — `Announce(Presence)` /
  `Query(ReadinessStatus)` / `Query(HealthStatus)` / `Stop`. Its INTENT.md is
  explicit: this is "the lifecycle relation that makes a process a Persona
  component: the Persona manager talks to each supervised child over this
  channel." `mind/src/supervision.rs` is the **child-side** template: a
  `SupervisionPhase` actor whose `reply()` answers `Announce →
  Identified(ComponentIdentity)`, `Query(Readiness) → Ready`, `Query(Health) →
  HealthReport`, `Stop → StopAcknowledged`. Every supervised daemon implements
  this child side.
- `owner-signal-persona` is the **privileged engine-manager command surface** —
  `Engine [Launch Retire Query]` / `Component [Start Stop Query]` /
  `Selector [ActiveVersion]`. Its INTENT.md states the privileged
  launch/retire/start/stop authority lives HERE, and `signal-engine-management`
  "is not an owner socket." This is the surface the MANAGER issues.

The binding intent names PERSONA, not orchestrate, as the manager/supervisor:
`tq18` [persona is the engine manager; orchestrate is the runtime that runs them
together], `mazv` [persona — the manager and supervisor of the whole thing —
runs and supervises the introspector, the schema daemon, and the other triad
components], `kzk5` [Persona runs as a permissioned system daemon, privileged,
supervising component daemons], `my4g` [Persona uses systemd template units for
component daemon management]. So the OS-process launch/retire/health-supervise
authority (owner-signal-persona) is PERSONA's. orchestrate is the **work-layer
runtime** — its INTENT.md scope is "role claims, activity log, agent-run
lifecycle, spawn plans, executor capacity, scheduling, escalation, lane
registry," while persona-mind owns "policy truth, channel-grant authority." The
synthesis that holds (report 2 open-question #2): persona start/stop/health-
supervises DAEMONS (the OS-process layer); orchestrate manages AGENT-RUNS and
roles (the work layer). orchestrate's "agent-run lifecycle / spawn plans /
escalation" are work-coordination machinery, NOT OS-process supervision of peer
daemons.

Therefore:
- orchestrate should **NOT** own a manager command surface (no
  `owner-signal-persona`-shaped surface, no `signal-engine-management` manager
  role). The frame's suggestion that the engine-management surface might belong
  in orchestrate is **answered NO** by source + intent.
- orchestrate **SHOULD** implement the engine-management **child** surface so
  persona can supervise it as one of the daemons in the running set (`mazv`).
  This is exactly mind's `supervision.rs` template — a `SupervisionPhase`-style
  child handler answering Announce/Readiness/Health/Stop. It maps directly onto
  the `czw0` minimal `on_start`/`on_stop` lifecycle hooks the engine traits
  already carry. **This is the right move, but it is the running-system-slice
  step (report 74 P1), not the core triad port** — it should land after
  orchestrate is on the engine traits, because the child surface is most cleanly
  built ON TOP of the `on_start`/`on_stop` lifecycle the port introduces.

Caveat (report 2 open #2): the boundary between "persona manages/supervises" and
"orchestrate runs them together" is not crisply drawn in intent — this synthesis
is inferred, not stated verbatim. It is the #1 open question for the psyche
(§6.1).

## 8. What lands in this repo's INTENT.md / ARCHITECTURE.md on the porting branch

Per C4 (continuous manifestation, `repo-intent.md` §"Continuous manifestation
discipline" / spirit 944), updated ON THE PORT BRANCH alongside the code:

- **INTENT.md "Pending schema-engine upgrade":** replace the STALE single-file
  framing ("convert to a single `orchestrate/orchestrate.schema` file") with the
  three-plane reality (`lc2r`): wire-only `signal-orchestrate` +
  `meta-signal-orchestrate` contracts, in-daemon `nexus.schema` + `sema.schema`,
  engine traits via triad-runtime/schema-rust-next. Drop the `primary-ezqx.1`
  emitter reference (superseded by schema-rust-next per report 3).
- **INTENT.md "Goals":** rename the owner contract reference from
  `owner-signal-orchestrate` to `meta-signal-orchestrate` (R14/`r9qy`).
- **ARCHITECTURE.md §"Pending schema-engine upgrade":** same single-file→three-
  plane correction; note the `MultiListenerDaemon` runner shape replaces the
  thread/free-fn daemon; note the Nexus feature catalog as the new visibility
  surface.
- **ARCHITECTURE.md §2 Authority Chain + §4 Owner Wire Surface:** rename
  `owner-signal-orchestrate` → `meta-signal-orchestrate`; the downstream
  `owner-signal-persona-router`/`owner-signal-persona-harness` references are
  also `owner-signal-*` rename candidates (separate fleet slices).
- **ARCHITECTURE.md §3 Ordinary Wire Surface + §"Migration history":** remove the
  Sema-classification-on-wire description (`SemaObservation`/`ToSemaOperation`
  observation labels) per R24/`7l7l`; the Sema class is derived internally below
  the contract.
- **ARCHITECTURE.md §5 State:** if `bootstrap-policy.nota` is introduced as a
  pre-encoded binary artifact (`7x50`), document the bootstrap-once one-shot
  table; otherwise note bootstrap is not-yet-implemented honestly.
- Add the supervision-child surface to the destination list (§7) framed as a
  running-system-slice step gated on the psyche decision (§6.1).

## Sources (read in full or in relevant part)

orchestrate: `INTENT.md`, `ARCHITECTURE.md`, `Cargo.toml`, `src/{daemon,lib,
service,tables,lowering,handover,execution,role,claim,lane,lock_projection,
configuration,main,error}.rs`, `src/bin/orchestrate.rs`,
`schema/orchestrate.concept.schema`, `tests/` listing.
Contracts: `signal-orchestrate/schema/signal-orchestrate.concept.schema`,
`owner-signal-orchestrate/schema/owner-signal-orchestrate.concept.schema`
(meta-signal-orchestrate verified ABSENT).
Engine-management: `signal-engine-management/{schema,INTENT.md,ARCHITECTURE.md}`,
`owner-signal-persona/schema/owner-signal-persona.concept.schema`,
`mind/src/supervision.rs` (imports `signal_persona::engine_management`).
Spirit: `tq18`, `mazv`, `kzk5`, `my4g`, `b9ao`, `ojuh`, `29s6`, `q402` (queried
2026-06-05). Base recipe + rulebook + intent: reports 1, 2, 3 of this session.
