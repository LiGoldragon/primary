# Exact-916 source ledger — bounded author mapping

Basis: Flow `916b54574ae0024b893a9f4252f2e97704db48c1`; read-only. This maps observed symbols and planned obligations; it is not an exhaustive closure claim.

## Changed codec / Datom / Protos signatures

| observed symbol | exact location | intended route/type | planned test | status |
|---|---|---|---|---|
| `datom_codec::Budget { remaining, reader, depth, maximum_depth }` | pinned `datom-codec/src/core.rs:24-30`; Flow literals `crates/flow/src/main.rs:41-46`, `compose_invocation.rs:15-22`, `hook.rs:88-95`; Meta `crates/flow-meta/src/main.rs:27-34,50-57`, `compose_invocation.rs:15-22`; Nexus `crates/flow-nexus/src/main.rs:55-62,361-368,508-515,625-632`, `store/delivery/body.rs:367-374`, `store/queue_delivery.rs:2786-2793` | typed per-process `TextBudget` / explicit envelope; no live Nexus lookup in Flow/Meta/Hook | parse/compose under supplied values; missing/invalid values refuse | Exact all production literals above mapped; tests and Ethos fixtures remain to enumerate |
| `protos::ReaderBudget { remaining }` | pinned `protos/src/core.rs:85-103`; private depth `MAXIMUM_READER_DEPTH` and comparison `:254,291`; `protosize_with(&mut ReaderBudget)` `:558-576` | add owned reader-depth policy only if allocated API permits; retain one Reader implementation | depth/node exhaustion and lexical parity | exact dependency clone/custody and version allocation absent |
| `BoundedProtosizable::protosize_with` | `protos/src/core.rs:102-104,558-576`; call sites above | same API with supplied `ReaderBudget` | old syntax byte-for-byte equivalent | dependent repository all-literal audit not complete |
| canonical Datom integer composition | `datom-codec/src/composition.rs:741-761` | one exported canonical integer decoder reused by startup scanner/composer | plus, -0, leading zero, range | owner clone/version allocation absent |
| standalone Invocation shapes | `crates/flow/ethos/invocation.ethos:6-9`, generated `flow/src/generated/invocation.rs:5-14`; Meta equivalents `flow-meta/ethos/invocation.ethos:5-7`, generated invocation | typed invocation carries client policy snapshot | Flow/Meta/Hook parse before socket connect | exact new Ethos field allocation and generated regeneration missing |

## Configuration writers and one guard

| observed writer | exact location | intended single route | planned test |
|---|---|---|---|
| `ConfigurationStore::configure_change` configuration-only | `flow-nexus/src/store.rs:4390-4394` | `FlowStore::configure_meta_change` through one validated prepared guard | invalid policy rejects before write |
| running `FlowStore::configure_change` | `store.rs:5347-5359` | same guard; no legacy bypass | live replacement/reopen |
| legacy three-family configure | `store.rs:4432-4474` | route all declarations through validated snapshot plan | Nexus/Models/Metaflows atomic replacement |
| legacy runtime/meta configuration | `store.rs:5669-5674`, `5707` | one guard, preserving runtime row semantics | write/readback |
| central dispatcher `configure_meta_change` | `store.rs:8677-8770` | candidate v6 metaflow wrapper, policy rows and validation | all `ConfigurationChange` variants |
| delivery writer | `store/delivery.rs:324-329,387` | guard only where changed policy reaches delivery; retain delivery family | delivery admission |
| counters writer | `store/counters.rs:88-93,56` | guard/one transaction if policy row participates | counter commit |
| startup executable defaults | `lib.rs:702-704`; meta dispatch `lib.rs:352-363`; listener `main.rs:266` | explicit startup configuration; no implicit fallback | default startup refusal |
| internal Nexus setup | `store/metaflow.rs:740-744` | explicit configured declaration path | setup/reopen |

Exact config v5→v6 persistence: `store/metaflow_declaration.rs:21-48` current wrapper/key/version; V4 mirror/upgrade `:50-103`; descriptor/predecessors `:303-318`; readback `:391-419`; replacement write `store.rs:8758-8769`; descriptor construction/registration `store.rs:4308-4339`; catalog current identity `store.rs:7967-7970`. Retained Nexus v4: `store/nexus_configuration.rs:16-40,253-268`. Retained AddressHold descriptor/upgrades: `store.rs:3591-3594,3784-3828,4887-4934`.

## Ordinary/meta CLI, generated, hook, compose, Nix

- Flow parser: `crates/flow/src/main.rs:30-58`; response frame reader `:67-83`; compose `compose_invocation.rs:8-31`; hook parser/config `hook.rs:47-98`; hook fixture parse `:226-244`.
- Meta parser: `crates/flow-meta/src/main.rs:39-66`; response frame reader `:71-81`; compose `compose_invocation.rs:8-31`.
- Hook constructor: `flow-nexus/src/herdr/launch.rs:484-496` constructs HookConfiguration from `HerdrCli.ordinary_socket`.
- Nix constructor: `nix/mk-flow-package.nix:89-117,149-200` emits ConfigureNexus and executable defaults; no existing policy envelope.
- Ethos/generated source pairs: Flow `flow/ethos/invocation.ethos:6-9` → `flow/src/generated/invocation.rs:5-14`; Meta `flow-meta/ethos/invocation.ethos:5-7` → generated invocation. Exact changed field names and generated regeneration are missing prebody input.

## Resume ordinary/meta/Observe

Exact 916 has no public Resume operation/type. Observed native-only symbols:

- `flow-nexus/src/launching.rs:1157-1181`, trait `ResumesReplacement`;
- `flow-nexus/src/codex_turns.rs:58-59,194-206`, `TurnEvent::Resumed`;
- `flow-nexus/src/send_tool.rs:617-624`, emits resumed event;
- `flow-nexus/src/codex.rs:1013-1025,1234-1246`, native thread resume;
- `flow-nexus/src/herdr/launch.rs:1945`, launch path.

Proposed `ResumeHead`, `ResumeAttempt`, Observe vocabulary has no observed source symbol. Missing prebody inputs: exact Ethos/generated ordinary/meta dispatch, observation projection, admission mutation transaction, key constructors, and all new table coordinates. Do not infer lifecycle migration.

## Runtime leaf consumers

| leaf / observed consumer | exact source | planned ownership/test |
|---|---|---|
| Effort (`ChoosesEffort::effort_of`) | `flow-nexus/src/sending.rs:472-483`, materialization `:580`; wake projections `waking.rs:2691,2869`; Codex readback `codex.rs:809-813,877,927-972` | policy owner/precedence unresolved; test all 12 aspect/layer pairs and Codex readback |
| Reminder timing | `store/reminder.rs:25-55`; `reminding.rs:15-16,93-99` | ReminderPolicy; firing/stop tests |
| Delivery cap/slices/deadline | `sending.rs:59-101,1363`; `send_tool.rs:708-810,909-955` | separate delivery leaves; admission/replay tests |
| Retry | `send_tool.rs:535-612` | RetryPolicy reconnect/reset test |
| History | `codex.rs:258-261`; `codex_turns.rs:72,159-174`; `claude.rs:443` | distinct Codex/Claude leaves; retention tests |
| Ancestry | `caller.rs:172,302` | AncestryPolicy depth test |
| Polling | `heartbeat.rs:338`; `observe_agent.rs:217`; `compacting.rs:43,58-66` | distinct loop leaves; each missing/invalid test |
| Transport | `lib.rs:768-784`; `main.rs:254-256`; `context.rs:50,128-129`; `herdr/launch.rs:375,411-412` | separate exchange limits; adapter tests |
| Title/pane | `herdr/launch.rs:1447-1453,1528-1579,2261-2279`; `herdr/pane.rs:51-64,87-140,368-405` | TitlePolicy/PanePolicy; retry/interrupt tests |
| Frame/parser | `lib.rs:1389`; `codex.rs:29-30`; `context.rs:52,141`; `composition.rs:181-205`; parser literals listed above | bounds remain policy/unproven; supplied-budget parity tests |
| Launch fallback | `herdr.rs:143-198`; `sending.rs:485-568`; `waking.rs:1470-1477` | LaunchPolicy; missing startup refusal tests |
| Existing configured Minutes | `store.rs:1154-1205`, default family and descriptor | retain `DefaultMinutes` family/value 30; do not absorb into new policy; configure/readback test |
| Existing leave-outs | `store.rs:1295-1421`, configuration dispatch `8677+` | retain family/predecessor and harness validation; unchanged archive fixture |
| Existing harness profiles | `store.rs:298,342`; Nexus configuration shapes `nexus_configuration.rs:21-40` | retain ConfigureNexus/harness profile rows; no new policy propagation assumed |

## Coverage and remaining exact gaps

Covered source queries: config v5/v4 persistence, descriptor/catalog/read/write, Nexus/AddressHold retention, all affected writer entry points listed in held inventory, Flow/Meta/Hook invocation constructors/parsers, current native Resume symbols, codec budget declarations/call sites, and runtime leaf rows above. Grouping is only mechanical and locations are explicit.

Still missing before a complete ledger: (1) exact changed Protos/Datom/Engine API consumers outside this workspace and all `ReaderBudget` literals in dependency tests; (2) concrete generated/Ethos fields and adapter constructors after allocation; (3) every ordinary/meta Resume/Observe dispatch and admission writer, because no such public type exists in exact 916; (4) final 12-pair Effort owner/precedence; (5) exact profile/Minutes/leave-out oracle assertions; (6) allocated coordinates and coherent dependency revisions. No source edits or design decisions are claimed.

## Workspace manifest/ref metadata (observation only)

Observed workspace root manifest: `Cargo.toml:6` package version `0.51.0`; root dependencies `signal-flow` rev `ce083f2ba9cc0bd928735ba4cc09e59965982e30` and `meta-signal-flow` rev `281f5aa1b88cd43609c127cdf6f3c12645faf58b` (`Cargo.toml:18-19`). Workspace package manifests all use `version.workspace = true`: `flow-defaults`, `flow-ethos`, `flow-meta`, `flow-native`, `flow-nexus`, `flow` (`crates/*/Cargo.toml:2-3`). Binary/package names include `flow-meta`, `flow-meta-compose-invocation` (`flow-meta/Cargo.toml:10-13`) and `flow`, `flow-hook`, `flow-compose-invocation` (`flow/Cargo.toml:10-16`).

Codec companion references observed in manifests: `datom-codec` rev `4dff16b4f7412febc3b71aac8b49680cd20988cb` and `protos` rev `15b41da8f2579e73ead59bc0c2b97529b8ac32d3` in `flow-ethos/Cargo.toml:16-17`, `flow-meta/Cargo.toml:17,19`, `flow-nexus/Cargo.toml:23-24`, `flow/Cargo.toml:21-22`; `ethos-zero` rev `07714b0171802787bea1eefe4caa2d826d9c4030` in `flow-ethos:21`, `flow-meta:25`, `flow:29`, `flow-nexus:40`. Sema and Engine refs are `sema` `51d7927c872f0df12791bad8d39a4db6433b01a1` and `sema-engine` `9884905ff9c660ad97a35c524e42532d5c7bac90` (`flow-nexus/Cargo.toml:30-31`). No redb git/fork reference is present in workspace manifests; redb is registry dependency. No raw-ref observation timestamp was recorded: UNKNOWN (no mtime substituted).

Suggested versions `44/60`, `Flow/shared 0.52`, `Sema 0.2`, `Engine 0.19`, codec `0.33`, and redb `4.3.0-flow.052` remain proposal suggestions only, not allocations or free namespaces (`/tmp/d05351-namespace-summary.md:12`).

## Corrected API query coverage (exact commands/results)

Read-only queries were run against `/git/worktrees/flow-config-d05351-independent/crates` and pinned dependency worktree `/git/worktrees/sema-engine-config-d05351-independent/src`:

- `rg 'struct EngineOpen'`: `sema-engine/src/open.rs:16`.
- `rg 'fn open'`: `sema-engine/src/engine.rs:121,133,142`; Flow wrappers `store.rs:4260-4285,4510-4519,4743-4758,5040`.
- `rg 'fn begin_atomic_commit'`: `sema-engine/src/atomic.rs:302`; Flow call results are 217 total `begin_atomic_commit|commit_atomic|upgrade_table|Engine::open` matches across Flow Nexus plus Engine source (full machine result captured in `/tmp/enginehits`; production paths include `store.rs`, `store/{address_hold,counters,delivery,logical_delivery,metaflow,queue_delivery,repair,send_call,send_outcome,successor}.rs`).
- `rg 'fn commit_atomic'`: `sema-engine/src/atomic.rs:308`; receipt consumers are `store.rs` and the store submodules above; exact call locations are in the query result and affected-consumer inventory.
- `rg 'fn upgrade_table'`: `sema-engine/src/memory/upgrade.rs:39,61`; Flow family consumers include `metaflow_declaration.rs:339,352,365,378`, `nexus_configuration.rs:284,294,304`, `queue_delivery.rs:611-682`, `send_outcome.rs:446-478`, `logical_delivery.rs:417-490`, `successor.rs:153`, `delivery.rs:231`, plus lifecycle families intentionally retained.
- `rg 'struct AtomicCommit'`: `sema-engine/src/atomic.rs:27`; receipt `:108`; preparation/materialization is private, so no existing public combined plan consumer exists.
- `rg 'ReaderBudget|protosize_with'`: pinned Protos declarations `protos/src/core.rs:85,102-103,254,291,558-576`; workspace production literals are Flow `main.rs:41-46`, `compose_invocation.rs:15-22`, `hook.rs:88-95,226-233`; Meta `main.rs:27-34,50-57`, compose `:15-22`; Nexus `main.rs:55-62,361-368,508-515,625-632`, `delivery/body.rs:367-374`, `queue_delivery.rs:2786-2793`. Test/fixture literals are separate and remain to be mechanically regenerated.
- `rg 'Budget|actualize|datom_form'`: Datom `Budget` is `datom-codec/src/core.rs:24-64`; `Potential::actualize` trait/impl `:424,449-460`; `DatomForming` signature `composition.rs:5-6` and implementation `:160`. No alternate `datom_form` implementation was found in Flow workspace.

The pinned codec refs are present in prepared dependency worktrees/caches and local refs were observed. Datom package `datom-codec` is 0.32.2 with companion `datom-codec-derive` 0.32.0; Protos package manifest is the pinned checkout. The proposed successor revision still requires Core allocation/authorization. No redb fork ref exists locally; registry redb 4.3.0 is the observed dependency.

## Explicit Effort matrix

Core approved EffortPolicy has 12 required Aspect/Layer entries. All twelve mechanically use the same observed selector `ChoosesEffort::effort_of` at `flow-nexus/src/sending.rs:472-483`; each is materialized at `sending.rs:580`, wake projections at `waking.rs:2691,2869`, and verified in Codex launch readback `codex.rs:927-972`:

`Psyche/Primary`, `Psyche/Secondary`, `Psyche/Tertiary`, `Psyche/Quaternary`; `Mind/Primary`, `Mind/Secondary`, `Mind/Tertiary`, `Mind/Quaternary`; `Field/Primary`, `Field/Secondary`, `Field/Tertiary`, `Field/Quaternary`.

The current function’s exact branch source is `sending.rs:475-482`; proposed test oracle is one configured value per all twelve coordinates, duplicate/missing coordinate refusal, and unchanged `LaunchProfile.effort` through send/wake/Codex readback. No stale unresolved claim remains about whether Effort is in RuntimePolicy: proposal `052-runtime-policy-shape.md:113` approves it.

## New Resume dispatch target obligations (source absence is expected)

Proposal `052-resume-lifecycle.md` names these planned ordinary additions: `Resume.FlowId`, `Resumed.FlowId`, `ResumeRejected.ResumeRejection`, `ResumeUncertain.FlowId`; Observe nested `ObserveSelection.Resume` with `ResumeSelection::{Flow,Attempt}`; replies `ResumeObserved.ResumeInspection` and `ResumeObserveRejected.ResumeObservationRejection`. Exact-916 source has no these symbols, as verified by `rg 'ResumeHead|ResumeAttempt|ResumeSelection|ResumeObserved|ResumeRejected' crates/flow-ethos crates/flow crates/flow-meta crates/flow-nexus/src` (only native `ResumesReplacement`, `TurnEvent::Resumed` hits listed earlier). Planned route is ordinary Query/Response generated projections → Nexus dispatch → one store-private admission owner; absence is an authored-change obligation, not a missing source consumer.

## Remaining bounded gaps at checkpoint

1. The 217 Engine API matches are machine-captured, but a row-by-row semantic classification of every test-only match versus production caller is still not written.
2. Exact changed generated fields and adapter constructors cannot be named before Core’s allocations/codegen revisions.
3. Resume public symbols are intentionally absent in 916; planned dispatch names above are complete from the controlling proposal, but generated consumer lines do not exist yet.
4. Runtime leaf rows cover proposal’s concrete source anchors; remaining work is per-leaf oracle/test naming and twelve-pair configuration validation, not additional broad source search.
5. Allocated coordinates and coherent successor revisions remain Core-owned gates.

## Query artifact custody

The complete Engine query output is copied immutably as `/home/li/primary/flows/e60c75/reports/engine-api-query-results.txt` (217 lines; SHA-256 recorded below). It came from exact command:
`grep -R -n "\\.begin_atomic_commit\\|\\.commit_atomic\\|\\.upgrade_table::<\\|Engine::open\\|Engine::open_recovering" crates/flow-nexus/src /git/worktrees/sema-engine-config-d05351-independent/src --include='*.rs'`.
Production paths are under `crates/flow-nexus/src`; sema-engine source declarations are `src/open.rs:16`, `src/engine.rs:121,133,142`, `src/atomic.rs:27,302,308`, and `src/memory/upgrade.rs:39,61`. The output contains no `/tests?/` paths; tests were not included in this production-scoped query and are a declared remaining classification gap.

## Engine 217-match classification

The artifact contains 217 matches: 214 Flow production source matches and 3 pinned Engine declaration/error matches; no test paths (`grep -E '/tests?/|cfg\\(test\\)'` returned 0). Mechanical owner/oracle groups, with every full filename/line retained verbatim in `engine-api-query-results.txt`:

- `store.rs` — 96 matches: FlowStore open/configuration/lifecycle owners; one-transaction guard oracle covers configuration/open rows and existing lifecycle commits.
- `store/queue_delivery.rs` — 25: queue admission/delivery owner; queue atomicity and predecessor upgrade tests.
- `store/logical_delivery.rs` — 26: logical-delivery/event owner; conversion and delivery commit tests.
- `store/metaflow.rs` — 16: declared metaflow mutation/seed owner; declaration readback and mutation atomicity tests.
- `store/send_outcome.rs` — 17: send outcome owner; outcome upgrade/counter receipt tests.
- `store/address_hold.rs` — 4: AddressHold admission/release owner; hold correlation tests.
- `store/metaflow_declaration.rs` — 4: configuration v1–v4 upgrade owner; frozen V5→V6 fixture/readback tests.
- `store/nexus_configuration.rs` — 3: retained Nexus v1–v3 upgrade owner; byte/schema-preservation fixture.
- `store/send_call.rs` — 5: send-call owner; commit/open fixtures.
- `store/successor.rs` — 5: successor ownership; stale receipt/atomic successor tests.
- `store/delivery.rs` — 3: delivery configuration upgrade/write owner; configured delivery oracle.
- `store/counters.rs` — 2: counter commit owner; counter receipt oracle.
- `store/repair.rs` — 4: repair owner; repair atomicity oracle.
- `store/events.rs` — 3: event family upgrade/open owner; archived event fixture.
- `store_check.rs` — 1: verifier/open owner; schema/catalog verification oracle.
- sema-engine `src/engine.rs` — 2 declarations/engine paths; Engine API contract tests.
- sema-engine `src/error.rs` — 1 error declaration; error classification oracle.

The exact intended route is unchanged Engine `begin_atomic_commit → typed assertions/mutations → commit_atomic` for writes, and `EngineOpen.with_family → register/upgrade_table` for opening. The candidate combined opening plan must be introduced above these existing owners; no existing caller is silently bypassed.
