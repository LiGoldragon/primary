# Flow: voice addressing, Capsule launch, and one route

Status: proposed revision for Mind Sol planning and Field Sol build. It supersedes the prior `3ed255…` design shape, which Mind 41fa34 accepted for planning with runtime gates. This revision responds to Psyche 9fb0ad's fourteen-point vision review. It authorizes neither implementation nor a launch.

## Baseline

`flows/f1c841/reports/flow-next.md` names Flow 0.23 main `636214e5` and, at line 76, Flow 0.24 main `4ad596d466a45de56239c55d415474f8b35ab163`; inspected source matches 0.24. Its worktree pins `signal-flow@f95034de0b203d886ba574fcb513c691c64b8498` and `meta-signal-flow@54eb5618e1433b68520ba9644e0428ea0f9ed75d`. Preserve 0.24's durable attempt/origin ledger, exact-repeat idempotency, conflict handling, ambiguity settlement, Claude reservation/empty-claim protection, first-turn delivery, and successor/reap admission. Migrate them; do not recreate them.

The living asked:

> Right now I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow.

> I want you to design the "What are your most important questions?" proposition and design ethos for Flow. You don't have to base yourself on what already exists but I want to see the ethos and the example datom: examples in use, how it would be used, and what kind of queries and responses we would get.

> I asked for it so it should be done. That's how I want the system to work: if I ask for a new flow, when I come back there's a new flow. There never ever is a new flow.

The first two are psyche, typed 2026-10-02, [flowNexus.md](/home/li/primary/flows/91ea9f/vision/flowNexus.md:1). The third is psyche, typed 2026-10-02, relayed by fe945a, [flowLifecycle.md](/home/li/primary/flows/91ea9f/vision/flowLifecycle.md:1).

The naming ruling is likewise direct psyche, typed 2026-10-02 and relayed by 91ea9f:

> Actually no, it's not psyche Astra. It's psyche primary, psyche secondary, mind primary, mind secondary, because we're not going to expose all the models to all of the voices.
>
> For now there are 9 voices, 3 by 3. We might put tertiary but I think after this we'll just add these. They're sort of side flows. They're not long-lived. They're focused flows. They're not so much a voice that is reachable all the time as a job that gets done and then it returns and then it's not reachable anymore. Whatever message was sent to it goes back, I guess, to whoever sent it, with the notice that this flow has ended and so its mission is done, right?

Source: [voices.md](/home/li/primary/flows/3ec648/vision/voices.md:3). The `vision-*` materials below are editorial specifications, not further living quotations.

## Chosen correction shape

`Voice.[ Psyche.Rank Mind.Rank Field.Rank ]`, with `Rank.[ Primary Secondary Tertiary ]`, is the nine-slot sum. `State.[ Running Ended ]` and `Event.[ Started ToolUsed.String Stopped ]` remain exact. Rank, power, and model remain distinct. All slots initially exist unbound; explicit assignments are needed only to adopt existing live voices.

A FlowId is a run identity; voice is persistent address; native session is harness identity. Identity is on data-bearing kinds through an `Identifiable`/identity trait, defaulting to the rkyv-archive fingerprint. New opaque `FlowId.Integer` and `RequestId.Integer` references are not caller-selected strings, report IDs, or public generations. Retry reuses the same encoded request/envelope; a deliberately new occurrence has a distinct trusted origin/occurrence even when its brief matches. Brief hash alone is insufficient. The existing attempt ledger is migrated, not discarded. Live slot mutation stays under Flow's per-voice lock. CLI/ledger display uses a fixed, versioned, reversible full-identity word codec; historic hex IDs remain provenance, and examples below are illustrative.

Current Claude `Stop` may precede final native records and repeat during a continuing turn. Until Question 1 is ruled, hooks persist raw observations without terminal projection. Whole-run `Running` until confirmed retirement/exit is proposed, not implemented; no third State hides the ambiguity. A late turn completion updates only its matching turn, never a newer active turn; an Ended run is never revived by hints.

Every harness event reaches Flow through a harness hook invoking Flow CLI. Codex app-server is launch/control transport, not a Flow notification consumer. The required Codex hook may consume a native callback and invoke CLI, but is a harness-bound source hook. Runtime proof and harness work remain required.

Caller identity comes from peer process plus trusted ancestry/Capsule process association. Report FlowId is assertion checked against that identity, never authority. Provisional Capsule processes may report against their reserved run before routing but receive no general speaking privilege. Existing SO_PEERCRED/Herdr resolution is reusable only if it uniquely identifies the run; a shared app-server PID with threads does not. The target Codex boundary is one app-server instance and one managed thread per flow, under a Capsule-owned process tree. Capsule registers PID plus start-time/process-instance identity before reports. If isolation is impossible, no caller-claimed-thread fallback exists: return the engineering blockage.

Capsule makes the runtime home, process boundary, app-server socket and store; only credentials are copied and all else recreated. It is meta-configured; the light-model semi-sandbox is first. Volatile-key encryption is later capability only. Start requests Capsule and refuses `NoCapsule` before allocation or pane side effect. Herdr is Capsule's pane/TUI subordinate; Flow retains ledger and orchestration.

Flow Memory holds model policy once per voice, altered only by meta Configure. Ordinary Start carries Voice and Brief, never model/harness/power/menu. Flow builds its current LaunchProfile internally. Unsupported or unconfigured policy is rejected by meta validation; no model-to-rank inference and no exposure of every model to every voice.

Refresh is one durable operation. Behind the per-voice lock it prepares successor while old run remains current, validates readiness, reaps predecessor, then publishes new name binding as one externally completed `Refreshed` transition. Address/send requests serialize behind persisted pending delivery/subscription; no polling and no dead old route. This is logical atomic publication, not claim of one OS syscall. Crash recovery resumes persisted intent/prepared successor; pre-reap failure retains old run and evidence. A prior resolved FlowId is ledger reference, not a voice-send bypass.

Side flows are independent Capsule/Start harness flows, not harness subagent threads. An ultra-low-power Field router takes ending flow questions/requests under captured authority; requester holds only RequestId, not job ownership. Results may return to requester successor by provenance. Ended-job messages return notice. Router cannot escalate authority and is not inferred to any Rank.

Speech is enforced at Resolve, Send, and job dispatch using authenticated caller voice plus explicit delegation. Vertical edges are one rung within aspect; no diagonal shortcut or FlowId bypass. Privileged recovery is separate meta authority. Same-rank Field/Psyche is Question 2.

Context hook calls typed `RecordContext`; meta threshold issues handover notice; flow writes handover; actual idle/settled-turn hook calls `Yield`; Flow executes the same Refresh. Stop alone is not proven idle. Hooks recognize only complete marked blocks in authoritative assistant-output transcript records and submit trusted-occurrence `Action`; user quotes, tool outputs and incomplete blocks are inert. Dispatcher may create Book without source-flow tool call. No filesystem polling. Retain handover/action evidence on failure.

## Codex route: failed witness and selected candidate

Field 42265e witnessed a failure, corroborated by relays from 5578cc and 41fa34: installed `codex-next 0.158.0-alpha.9`, disposable root `/tmp/flow-codex-witness-8Ld87N`, and `thread/start` returned `01a101ed-05a5-7fa0-83f8-12f536ed1a80` with zero turns. Native `skills/list` lacked `trial-contact-discipline`; empty-thread `thread/resume` returned JSON-RPC `-32600`, `no rollout found for thread id`; there was no attach, turn, or fallback, and listener stopped. Retained `uuid.json` and `server.log` do not record request frames or connection lifetime, so cause is unknown. This does not establish general Codex unsupportedness. HERDR_ENV/policy restrictions block production Herdr control; no bypass is proposed.

0. Capsule creates isolated per-flow runtime and reconstructs required launch-skill bundle/native-discovery configuration before user turn. Credentials alone are copied; generated skill/runtime inputs are recreated from pinned sources/manifests, never host working tree. Existing evidence does not show thread/start config magically installs skills/hooks; hook setup is separate verified Capsule/harness integration.

1. Flow admits and persists immutable `Admission.{ RequestId CapsuleId }`. Its trait-derived identity supplies FlowId **before** Codex native UUID. It claims/reserves lane from Flow identity; native UUID is later binding. This deliberately changes 0.24 Codex native-UUID-dependent ordering while reusing ledger/reservation principles. Retry reuses persisted request/Capsule/Flow identity, never fresh allocation, caller-selected UUID, or parent-flow test ID.

2. Capsule selects one paired `client_path`/`app_server_socket`. Flow opens one initialized ProxySession through `client_path app-server proxy --sock app_server_socket`. `thread/start` supplies full `FLOW_ID`, `FLOW_DIRECTORY`, `FLOW_SOCKET` shell_environment_policy at creation, Capsule cwd, paired model, `ephemeral:false`, and no user turn. FLOW_SOCKET means Flow ordinary socket, never app-server socket. Current source sets FLOW_ID/FLOW_DIRECTORY at start; this candidate adds FLOW_SOCKET. Schema permits policy structurally; actual values require witness.

3. Persist native UUID and bind it to Admission/FlowId. Keep the same initialized ProxySession alive. Validate actual native `skills/list` and empty thread; missing required manual contact skill refuses first-turn admission. Do not use `thread/resume` for environment and do not close/reopen control proxy between start and first turn. `codex.rs:918` already has initialize→thread/start→turn/start within one ProxySession; reuse/refactor it, not an invented RPC.

4. Through that session submit exactly one authorized actual first user turn, native skill objects first then text, under persisted delivery intent. No dummy/persistence-priming turn, implicit TUI turn, or missing trial-contact-discipline. Capsule process association and persisted UUID bind delivery. Move Herdr-ready condition to later visible-launch gate. Existing composition, skill/prompt, empty-thread and idempotency guards are reused; source does not yet implement this ordering.

5. After real first turn, establish native persistence/attach readiness once in isolated witness, then Capsule/Herdr runs `client_path resume UUID --remote unix://SAME_app_server_socket`. UUID, `ephemeral:false`, turn acceptance, or schema is not rollout proof. One evidence-triggered native read/attach attempt, never polling/repeated repair, is required. If attach fails, retain admitted attempt/UUID/turn evidence and return blockage; never create another thread or replay possibly delivered turn.

6. Herdr Bind verifies pane/terminal/harness/native UUID equals persisted UUID; only then satisfies existing visible Start readiness and, for Refresh, completed predecessor reaping/name transition. Control proxy, TUI process and app-server listener are distinct objects; both clients use same server socket. Hooks remain sole lifecycle Report ingress; raw app-server responses only confirm operations and never bypass Report.

Before actual first turn, cleanup covers only proven empty/unregistered artifacts under declared policy. After first-turn admission or ambiguous response, never delete claim/thread or retry fresh. Existing protected Release is Claude-only; no Codex cleanup witness is claimed.

Field 42265e also observed a distinct private Herdr attempt: private session `flow-witness-42265e` with private HOME/XDG/config/socket and experimental `allow_nested=true` started its own nested server; Claude 2.1.284 UUID `8e20d5b9-70b8-4756-9ef6-5c792da91d8a` opened sign-in under isolated HOME. Prepared first user input/contact/environment request was **not** proved admitted or executed, and private runtimes stopped. This proves private pane launch only, not tool, environment, native skill, or turn delivery.

Field separately reports positive baseline evidence from canonical `flow-test/hook-socket-f1c841@b18ce4ea`: `FLOW_TEST_LIVE=1 nix run .#flow-claude-hook` succeeded. Its runner recreates a `mktemp` home/store/socket, copies only the Claude credential file program-to-program with mode 600, runs a bounded cheapest-model Claude session, and verifies SessionStart/PostToolUse/Stop reports to its own Nexus. No credential bytes reach the flow or output. This witnesses supported isolated credential handoff and baseline hook route **in that runner**. It uses fixture Herdr and Claude `-p --output-format stream-json`; it does not prove an actual Herdr pane attachment, revised authenticated caller mapping, or a manual native first user `trial-contact-discipline` delivery. Applying this handoff to the interactive Capsule/Herdr candidate remains unproved. Neither observation authorizes a new probe, credential operation, or runner extension.

## Target Ethos (uncompiled)

This is target syntax, not a complete generator input or a claim of supported kinds. The four-root layout is a vision example; `Operation` layout is expressly proposed in `vision-ethos`. Manifest owns version. Shared types appear in Library; public wire never exposes Memory rows/counters. `CapsuleId` is a trait-derived reference to the concrete Capsule runtime object, not caller-provided runtime text. Runtime process/socket/home/store fields belong to Capsule's domain specification and are not claimed generated by this minimal Flow example. A one-use named wrapper here is an operation/variant payload or typed identity, not a payload-holder alias. The uncompiled root layouts are not generator witnesses.

```ethos
Library
[]
[ FlowId.Integer
  RequestId.Integer
  CapsuleId.Integer
  Rank.[ Primary
         Secondary
         Tertiary ]
  Voice.[ Psyche.Rank
          Mind.Rank
          Field.Rank ]
  Event.[ Started
          ToolUsed.String
          Stopped ]
  State.[ Running
          Ended ]
  Request.[ Question.String
            Work.String ]
  Action.[ Book.{ Title.String
                  Body.String }
           Handover.{ Body.String }
           Requests.Vector<Request> ]
  Question.{ Subject.String
             Choices.Vector<String> } ]
[]
[]

Signal
[ flow:[ FlowId
         RequestId
         Voice
         Event
         State
         Request
         Action
         Question ] ]
[ Start.{ Voice
          Brief.String }
  Refresh.Voice
  Report.{ FlowId
           Event }
  Resolve.Voice
  List
  Send.{ To.[ Voice.Voice
              Request.RequestId ]
         Message.String }
  Ask
  Observe.[ Voice.Voice
            Request.RequestId ]
  RecordContext.{ Used.Integer
                  Capacity.Integer }
  Yield
  Submit.{ Requests.Vector<Request> }
  RecordAction.Action ]
[ Started.FlowId
  Refreshed.FlowId
  Reported
  Resolved.FlowId
  Listed.Vector<Voice>
  Sent
  Returned.{ RequestId
             Reason.[ Ended
                      Unroutable ] }
  Asked.Vector<Question>
  Observed.{ Voice
             State }
  ContextRecorded
  Yielded
  Submitted.RequestId
  ActionRecorded
  Accepted.RequestId
  Refused.[ NoCapsule
            VoiceBusy.Voice
            CallerUnknown
            CallerMismatch
            SpeechDenied.Voice
            UnconfiguredVoice.Voice
            UnknownRequest
            NotIdle
            InvalidAction
            LaunchFailed
            ReapFailed ] ]
[]

Operation                              ; vision-level proposed layout
[ flow:[ FlowId
         RequestId
         CapsuleId
         Voice
         Event
         Action ] ]
[ Start.{ Voice
          Capsule
          Brief.String }
  Refresh.{ Voice
            Capsule }
  Record.{ FlowId
           Event }
  Dispatch.RequestId
  Deliver.RequestId
  Act.Action ]
[ Started.FlowId
  Refreshed.FlowId
  Recorded
  Dispatched
  Delivered
  Acted
  Failed.[ NoCapsule
           StartFailed
           ReapFailed
           DeliveryFailed
           InvalidAction ] ]
[ Capsule.{ CapsuleId } ]

Memory
[ flow:[ FlowId
         RequestId
         CapsuleId
         Voice
         Event
         State
         Request
         Action
         Question ] ]
[ Admission.{ RequestId
              CapsuleId }
  Run.{ FlowId
        State
        Vector<Event> }
  Flow.[ Voice.{ Run
                 Voice }
         Job.{ Run
               RequestId } ]
  Slot.{ Voice
         Option<FlowId> } ]
[]
```

```ethos
Signal
[ flow:[ Voice
         FlowId ] ]
[ Configure.{ Voice
              Model.[ Claude.String
                      Codex.String ] }
  Assign.{ Voice
           FlowId }
  ConfigureCapsule.{ Root.String
                     CredentialFiles.Vector<String> }
  ConfigureContext.{ Limit.Integer } ]
[ Configured.Voice
  Assigned.Voice
  CapsuleConfigured
  ContextConfigured
  Refused.[ VoiceBusy.Voice
            UnknownFlow
            AspectMismatch
            UnsupportedModel
            InvalidPolicy
            CallerUnknown ] ]
[]
```

Internal Memory additionally retains attempts, request provenance/authority, policies, handovers/actions, report receipts, launch intents, and typed Question values directly. FlowId is immutable Admission trait identity: mutable run state/native binding is excluded, so events do not change identity. `Run` is shared across Voice/Job variants; `Slot` and `Run` are not wire payloads. No old-format parallel runtime path: migration updates contract, storage, and every consumer while retaining historical evidence.

## Target datom examples (illustrative codec words)

Word values are schematic renderings pending fixed codec, not executable fixtures. Caller identity is process-derived prose context, never a destination encoding.

```text
Start.{ Mind.Primary «Review this design.» }
=> Accepted.Three-Pine-Glass
Observe.Request.Three-Pine-Glass
=> Started.Cedar-River-Quartz
```

```text
Start.{ Mind.Secondary «Inspect the test result.» }
=> Refused.NoCapsule
```

```text
Configure.{ Mind.Primary Codex.«illustrative-model» }
=> Configured.Mind.Primary
```

Authenticated caller Mind.Secondary resolving an allowed vertical neighbor:

```text
Resolve.Mind.Primary
=> Resolved.Cedar-River-Quartz
Send.{ Voice.Mind.Primary «Review is ready.» }
=> Sent
```

Authenticated caller Field.Secondary attempting a denied diagonal:

```text
Send.{ Voice.Psyche.Primary «message» }
=> Refused.SpeechDenied.Psyche.Primary
```

A hook attributed to Cedar-River-Quartz, followed by that same hook asserting a different existing run:

```text
Report.{ Cedar-River-Quartz ToolUsed.«Bash» }
=> Reported
Report.{ Maple-Stone-Lake ToolUsed.«Bash» }
=> Refused.CallerMismatch
```

```text
Ask
=> Asked.[ { «When does a run end?»
             [ «whole run»
               «answer» ] }
           { «May Field speak to Psyche at equal rank?»
             [ «through Mind»
               «direct» ] } ]
```

Separate ended-job request scenario, using its own request identity:

```text
Send.{ Request.Birch-Sand-Dawn «follow-up» }
=> Returned.{ Birch-Sand-Dawn Ended }
```

Fresh refresh occurrence: Cedar-River-Quartz is predecessor and Maple-Stone-Lake is distinct successor. Retransmission keeps its trusted request identity; deliberate new occurrence receives another.

```text
Refresh.Mind.Primary
=> Accepted.Oak-Wind-Star
Observe.Request.Oak-Wind-Star
=> Refreshed.Maple-Stone-Lake
```

`Accepted` is admission, not failed unsolicited start; final completion appears through Observe. Examples do not witness live contracts.

## Questions for Psyche's existing book

These remain parameters in **Two meanings for Flow**: <https://claude.ai/artifact/1LhLZg92hyrjXQsT3f6Yc1>. No duplicate book or new query round. Opus 5578cc attributes the following bounded-context record to [vision-raw/gradientsOfAuthority.md:141](/home/li/primary/vision-raw/gradientsOfAuthority.md:141): “A flow is one bounded LLM context. A fresh context started from the same continuity is a successor flow. Concurrent contexts using the same aspect are sibling flows.” It supports option 1 but is not final choice.

1. **Q1 state meaning.** `1=Running/Ended only, idle not public`; `2=Idle recorded as a third readable state`; `3=each answer ends a flow`. Existing target `State.[ Running Ended ]` is proposed option 1 branch, not a hidden ruling against 2/3. Records lean 1; raw Claude Stop is not permanent-end proof. No public termination projection lands as settled policy before selection/review.
2. **Q2 equal-rank speech.** `4=Flow refuses Field→Psyche on wire except an authentic relay of living's words`; `5=norm not enforced, direct contact with stated reason`; `6=all same-rank aspects direct`. Keep vertical one-rung/no diagonals. Sources lean 4 but remain unresolved; “rare” attaches Field→Psyche, not Mind→Psyche. A caller cannot unlock exception by naming its own text living words: trusted provenance/effective authority must validate. Ordinary Send covers normal messages; option 4 relay metadata and option 5 reason-bearing shape are conditional deltas after branch choice. Examples use only uncontested edges/denied diagonals.

## Authority and acceptance

Mind accepted prior `3ed255…` for planning. Opus 5578cc's amended grant holds wire/registry/hook changes pending Mind review of this revised hash. Only isolated native witnesses are authorized; retained `43b1f66/4cc58229` remain unpushed scope hold. This route is design candidate for Mind/Field, not authority to retry production or claim witness passes. Any build grant attaches after Mind acceptance; unresolved policy branches remain explicit.

Preserve 0.24 tests/features. Add caller-process-before-target comparison, shared-server misattribution negative case, Capsule isolation, hook→CLI-only event route, exact inline/verb/identity generation, codec roundtrip, model policy isolation, side-router authority/successor delivery, atomic observed Refresh/crash recovery/no stale route, context handover, and transcript action occurrence/dedup plus quote/tool/incomplete negatives. Add isolated native route witnesses: skill reconstruction, same ProxySession start→turn, policy values, real-turn attach readiness, and failure retention. No launcher deletion until Claude and Codex Flow Start witnesses plus consumer migration; guard removal is independent. No all-nine assignment gate.

Claude witness acceptance requires applying the runner-witnessed opaque credential handoff to the interactive candidate, plus admitted first user turn, native skills, tool/environment, and contact proof; the cited private pane observation alone satisfies none of those delivery checks.

## Sources

- GENERATED editorial specification evidence: [vision-flow](/home/li/primary/.agents/skills/vision-flow/SKILL.md:6), [vision-nexus](/home/li/primary/.agents/skills/vision-nexus/SKILL.md:6), [vision-ethos](/home/li/primary/.agents/skills/vision-ethos/SKILL.md:6). These are not attributed above as living quotations.
- Living records/provenance: [Flow questions/launch/hooks](/home/li/primary/flows/91ea9f/vision/flowNexus.md:1), [lifecycle](/home/li/primary/flows/91ea9f/vision/flowLifecycle.md:1), [voices](/home/li/primary/flows/3ec648/vision/voices.md:3), [hook refresh/action](/home/li/primary/flows/7328f4/vision/hooks.md:13), [Field router](/home/li/primary/flows/b81560/vision/archive-operational-fieldUltraLowRoutesSubflowRequests.md:3), [Capsule](/home/li/primary/flows/3ec648/vision/capsule.md:3), [Flow identity](/home/li/primary/flows/f55ec8/vision/flowIdentity.md:3).
- Baseline/pins: [flow-next report](/home/li/primary/flows/f1c841/reports/flow-next.md:76), [Flow Cargo pins](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/Cargo.toml:17), [ordinary contract](/home/li/.cargo/git/checkouts/signal-flow-688d1620dbb6a864/f95034d/ethos/signal.ethos:82), [meta contract](/home/li/.cargo/git/checkouts/meta-signal-flow-d6ff5e00f45b353b/54eb561/ethos/signal.ethos:31).
- Current implementation evidence: [Codex proxy/endpoint](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/codex.rs:1) (`:238` proxy byte bridge, `:56` endpoint selection, `:912/:918/:931/:1033` helpers), [Herdr launch](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/herdr/launch.rs:1255) (`:1337` same-endpoint TUI, `:1403` exact binding), [caller resolver](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/caller.rs:1) (`:42/:114` kernel PID/ancestor resolver). Start/resume helpers currently open separate ProxySessions; start itself has thread/start→turn/start in one. Field connection lifetime is unknown. Current source proves no per-thread Codex hook process; isolated Capsule hook route is requirement. Offline schema at `/tmp/codex-app-server-schema-dea0ba.uhcC1A` is accepted shape only, not environment-runtime proof; turn response does not prove durable rollout.
- Field failure witness: `/tmp/flow-codex-witness-8Ld87N` retained; witness facts above are attributed to Field 42265e and relays 5578cc/41fa34.
- Field positive baseline: canonical `flow-test/hook-socket-f1c841@b18ce4ea`, attributed Field 42265e; `FLOW_TEST_LIVE=1 nix run .#flow-claude-hook` witnessed program-to-program mode-600 credential handoff and baseline SessionStart/PostToolUse/Stop hook reports in its own Nexus. Fixture Herdr/Claude `-p --output-format stream-json` scope does not prove interactive Capsule/Herdr behavior.
- Claude witness limitation: Field 42265e private runtime/session evidence as stated above; private runtimes stopped, and no user-turn/tool/environment/native-skill proof was obtained.
