# Isolated installed-0.51 threshold witness — preparation packet

Owner f029f7 (Flow configuration/proof). Proposed operational executor: existing Field `book_gate_writer`, write-ordinary, available/no active job or locks, under Field core Primary d1b2d6; native ID and actual FlowId not yet supplied. Field reports corrected scope/custody ACK. Psyche core Secondary 2fa896 runs reading/native observation after an exact handoff ACK. NO execution has occurred. Primary must admit the final executable packet and actual executor identity/lock before effects. No 052 controller or source worker is used.

## Exact resources to reserve together before execution

- Runtime `/run/user/1001/flow-proof-f029f7` (ordinary `flow.sock`, meta `flow-meta.sock`, private Curriculum `curriculum/curriculum.sock`).
- State `/home/li/.local/state/flow-proof-f029f7` (Memory `flow.sema`, private Curriculum state/cache if required).
- Scratch `/home/li/flow-proof-f029f7` (workspace child `workspace`, synthetic reading corpus, own flow directories).
- Herdr session `flow-proof-f029f7` only; exact supported create/kill command must be witnessed by the executor before admission, never use default session.
- Transient units `flow-proof-f029f7.service` and `curriculum-proof-f029f7.service` only; setup must assert every named resource absent/unclaimed, reserve all paths/session/unit names in one fresh lock under ACTUAL executor FlowId. Existing names/conflicts STOP; no deletion/adoption of unknown resources.
- Test Address `{ Psyche thresholdWitness Quaternary }`, native model `claude-haiku-5-5`, no other model/flow.

## Installed artifacts and source facts

Package `/nix/store/5w5sqfmcndg8cr1dm72yr8iy591kmxsa-flow-configured-0.51.0/bin/{flow-nexus,flow,flow-meta,flow-hook}`.

Helper `/nix/store/b9czi957cxmhmmz197l9hgyddr5qb5vb-configure-flow-051/bin/configure-flow-051` takes INLINE Start text, meta socket, then query FILES (not a Start file). It runs `flow-nexus --configure-only "$start"` for one query per process, sends `flow-meta "{ «$socket» $body }"`, accepts Configured.Replaced/Unchanged. It does not run the normal Nexus loop during configuration.

Source `/nix/store/dz5dwigzydw2khv6wpgq3556hw83j4x7-source` main.rs confirms Start has FOUR positions including landing-watch Option; do not use the obsolete 3-position Start shown in a preparation helper report. Correct Start, inline:

```datom
{ /run/user/1001/flow-proof-f029f7/flow.sock
  /run/user/1001/flow-proof-f029f7/flow-meta.sock
  /home/li/.local/state/flow-proof-f029f7/flow.sema
  None }
```

`RunningNexus::open` constructs HerdrCli with this actual Start ordinary socket (lib.rs ~734), and launch.rs484ff shell-quotes sibling package flow-hook plus `HookConfiguration { ordinary_socket_path }`. All five Claude events receive the same command. hook.rs uses this typed socket and sibling package Flow CLI; no stable wrapper is used. Expected actual five commands therefore contain the full installed flow-hook path and the TEST socket argument. Record the launched settings/argv, not merely this expectation; any stable destination invalidates the fixture BEFORE reading.

## Proposed explicit private declarations

Never replay stable flow-051-nexus.datom or LIVE metaflows file. Write separate files in the report/config directory, each one Configure query. Exact schema field order independently witnessed from installed source tests and matching meta signal source:

```ethos
ConfigureNexus.{ SourceRoot StableCodex NextCodex HarnessProfiles MetaAspects Option<MessageNexusPath> Option<MessageNexusBinary> CurriculumNexusPath Lease Option<PresentationPrompt> }
CodexEndpoint.{ ClientPath Home ControlSocketPath Vector<ModelName> }
ConfigureModel.{ Layer Aspect ModelName }
ConfigureThreshold.{ ModelName Integer }
ConfigureMetaflow.{ Address Option<Root> SystemModules UserModules FlowKind ToolSet Continuity Purpose Records }
```

```datom
Configure.Nexus.{
 /home/li/flow-proof-f029f7/workspace
 { /home/li/flow-proof-f029f7/unused-codex /home/li/flow-proof-f029f7/unused-codex-home /run/user/1001/flow-proof-f029f7/unused-codex.sock [ unusedStableTestModel ] }
 { /home/li/flow-proof-f029f7/unused-next /home/li/flow-proof-f029f7/unused-next-home /run/user/1001/flow-proof-f029f7/unused-next.sock [ unusedNextTestModel ] }
 [ { Claude [ / ! # ] [ esc esc ] [ enter ] } ]
 [ Psyche ] None None
 /run/user/1001/flow-proof-f029f7/curriculum/curriculum.sock
 60 None }
Configure.Models.[ { Quaternary Psyche claude-haiku-5-5 } ]
Configure.Thresholds.[ { claude-haiku-5-5 16000 } ]
Configure.Metaflows.[
 { { Psyche thresholdWitness Quaternary }
   Some./home/li/flow-proof-f029f7/workspace
   [ spirit:core ] [] Regular Default Maintained
   «Read only the supplied benign test corpus when the witness owner asks. Make no edits, publication, network calls, children or configuration changes. Reply briefly and stop naturally. This is one disposable threshold witness.» [] } ]
```

Unused Codex endpoints are explicit test data, disjoint model names, never launched. Lease60 and Claude profile reuse the installed declared values. Message path/binary None prevent stable Message calls; no stable SendServers/Heartbeat/Investigation are replayed. Threshold16000 is Primary-approved ONLY in this fresh test Memory; stable200000 unchanged. Metaflow Maintained is needed to prove automatic successor even without a queued task. Exact additional required configuration (default minutes/counters/leave-outs) must be taken from supported schema/runtime refusal, not fabricated as hidden defaults; no launch retry loop.

## Own session launch and readbacks

Ordinary declared `Launch` chooses caller's Herdr session or defaults to `default` (sending.rs561ff). Therefore an external CLI Launch is NOT an admissible shortcut. Supported `Start.LaunchProfile` explicitly carries HerdrSessionName, with actual schema:

```ethos
LaunchProfile.{ LaunchRequestId SystemModules UserModules Remembering Address ModelName Effort Option<FlowId> HerdrSessionName Option<LeaveOuts> FlowKind ToolSet InstructionPrompt }
```

Proposed exact Start profile after private Curriculum stands, own session is verified, and declaration/config readbacks match:

```datom
Start.{ proof-f029f7-launch [ spirit:core ] [] Predecessors.0
 { Psyche thresholdWitness Quaternary } claude-haiku-5-5 low None
 flow-proof-f029f7 None Regular Default
 «Acknowledge readiness briefly. Do not read the corpus until the witness owner sends its one task; do no other work.» }
```

Use installed Flow CLI with explicit invocation `{ TEST_SOCKET QUERY }`, never shell `flow` wrapper/stable sockets. Meta `Inspect.{ Psyche thresholdWitness Quaternary }` and `Configuration` use installed Flow-meta with explicit TEST_META_SOCKET. Capture actual Started/Launched/native binding, own Herdr route/session/settings, context and threshold. Automatic refresh must preserve its stored own-session profile; record successor route again. Do not call manual Refresh as proof.

## Witness and boundaries

2fa896 owns ONE reading task after setup handoff and native/idle guard. INITIAL actual context MUST be below16000. If initial context is already >=16000, fixture INVALID: stop, report; do not raise/reset threshold or claim a crossing. Read only a fixed benign local corpus under scratch. Proposed cap: 4 batches, each at most 32768 UTF-8 bytes, total131072 bytes, at most10min; owner records exact corpus hash and actual native context after each natural Stop. Token count is actual validated native measurement, never inferred from bytes. Stop inputs at first >=16000, successor or failure. Record real Stop→TEST socket→correlated context→threshold comparison→AUTOMATIC successor/native/051hooks/queue. No synthetic token injection, no 200000stable threshold manipulation. Batch bounds require admission/owner acceptance before execution.

## Isolation gates still OPEN (exact capabilities, not work delegated away)

1. **Private Curriculum startup/config.** Installed051 composer always requires a live configured Curriculum endpoint; fixture bypass is cfg(test) only. Merely naming a dead private socket will fail. Current installed Curriculum binary is `/nix/store/2zhjmdj7g8h4hagkjsl14zah3nwd97z3-curriculum-0.1.0/bin/curriculum-nexus`; stable unit has context-layout2, shared authored/cache repository dirs and a refresh program. Field/current Curriculum holder has been asked for supported private socket/cache/source/refresh configuration. Do NOT start it with shared refresh destinations. Need its exact isolated declaration before execution.
2. **Executor identity, own Herdr create/kill and auth boundary.** Field has available existing worker, but actual FlowId/native and exact supported session commands are not yet supplied. Do not invent them. No credential file is read/copied by this packet; if private Claude home/auth materialization is needed, use the authorized secrets-handling holder, never expose credentials. Actual hook settings must contain no inherited stable hook route.
3. **Offline parser/schema validation.** No binary, configure-only process, listener or test has run in this preparation. Proposed datoms must be checked by the executor under admitted setup scope against installed051 before launch. Stop exact refusal rather than guess variants.

## Exact teardown after evidence retention and authorization

Witness owner stops reading; executor verifies test unit/session/PIDs/paths are those it created. Stop ONLY transient flow-proof-f029f7.service and curriculum-proof-f029f7.service; kill ONLY its exact Herdr session with documented command; retain logs/native evidence/report first, then remove ONLY exact runtime/state/scratch trees above after symlink/identity guards. No broad pkill, no stable service stop, no existing declaration removal/replay, no deletes outside reserved paths. Release only its own lock. No threshold/config restoration needed because the whole test Memory is private/disposable.

## Feasibility and proof status

Setup is feasible on installed051 with an independent private Curriculum and own session; hook target is explicitly place-derived, no source fork needed. It does NOT stand yet. This packet is not execution authority or crossing evidence. Target04:19:37 remains; exact missing private Curriculum/session/executor facts must close before launch. Source remains unchanged; a Primary report/config evidence commit must be made by the standing committer after actual proof, not manufactured as a source correction.
