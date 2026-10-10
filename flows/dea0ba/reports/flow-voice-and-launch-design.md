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

`Voice.[ Psyche.Layer Mind.Layer Field.Layer ]`, with `Layer.[ Primary Secondary Tertiary Quaternary ]`, is the settled twelve-voice address sum. `State.[ Running Idle Ended ]` and `Event.[ Started ToolUsed.String Stopped ]` are the revised target. A Flow is one harness session/context: restarting whole context starts a new Flow. Layer, power, and model remain distinct. All twelve voice slots begin unbound; explicit assignments are needed only to adopt existing live voices.

The later layer-vocabulary record states:

> Well even saying Sol speaks to Opus and so on is wrong because we should be saying primary, secondary, tertiary, quaternary. We should be using the layer vocabulary and then another [skill] somewhere loads the current correspondence of which model is which layer.

This is psyche, typed 2026-10-03 and relayed by Psyche Opus 5578cc, [speech.md](/home/li/primary/flows/dea0ba/vision/speech.md:17). It separates normative Aspect.Layer speech from the configured model correspondence.

A FlowId is run identity and its word-bearing `FlowId.String` form is the address humans and models use; it is not a ledger-only hash alias. The selected interface shape is a camelCase three-word form, illustrated by `abandonAbilityAble`; this approves the interface shape, not an unwitnessed codec or collision claim. Voice is persistent address; native UUID is harness correlation, never the word identity. Identity is on data-bearing kinds through an `Identifiable`/identity trait, defaulting to rkyv-archive fingerprint. RequestId and CapsuleId remain opaque displayed strings, never caller-chosen strings or public generations. Trait fingerprint and textual rendering remain distinct. Examples are illustrative strings, never codec vectors.

A private `RequestOccurrence` holds authenticated caller FlowId, Flow-owned durable caller-scoped `Sequence.Integer`, and immutable actual request content. Its immutable fingerprint supplies RequestId; neither Admission nor brief alone supplies it. Flow allocates Sequence atomically with admission. Retries carry opaque issued RequestId but reauthenticate process caller; they match stored immutable payload or refuse conflict. No caller integer or timestamp supplies uniqueness. This is proposed identity contract, not implementation proof. Existing attempt ledger is migrated, not discarded; live slot mutation remains under per-voice lock.

Current Claude `Stop` may precede final native records and repeat during a continuing turn. Hooks persist raw observations rather than treating Stop alone as Ended. Running, Idle, and Ended describe one session; restart of whole context is a new Flow. A late turn completion updates only its matching turn, never a newer active turn; an Ended run is never revived by hints.

Every harness event reaches Flow through a harness hook invoking Flow CLI. Codex app-server is launch/control transport, not a Flow notification consumer. The required Codex hook may consume a native callback and invoke CLI, but is a harness-bound source hook. Runtime proof and harness work remain required.

Caller identity comes from peer process plus trusted ancestry/Capsule process association. Report FlowId is assertion checked against that identity, never authority. Provisional Capsule processes may report against their reserved run before routing but receive no general speaking privilege. Existing SO_PEERCRED/Herdr resolution is reusable only if it uniquely identifies the run; a shared app-server PID with threads does not. The target Codex boundary is one app-server instance and one managed thread per flow, under a Capsule-owned process tree. Capsule registers PID plus start-time/process-instance identity before reports. If isolation is impossible, no caller-claimed-thread fallback exists: return the engineering blockage.

Capsule makes the runtime home, process boundary, app-server socket and store; only credentials are copied and all else recreated. It is meta-configured; the light-model semi-sandbox is first. Volatile-key encryption is later capability only. Start requests Capsule and refuses `NoCapsule` before allocation or pane side effect. Herdr is Capsule's pane/TUI subordinate; Flow retains ledger and orchestration.

Flow Memory holds launch policy once per voice. The designated knowledge skill supplies the aspect × layer × harness-stack model/effort correspondence; no Primary, Secondary, or Tertiary assignment is inferred here. Meta Configure changes stored policy, while ordinary Start carries Voice and Brief, never model/harness/power/menu. Flow builds its current LaunchProfile internally. Unsupported or unconfigured policy is rejected by meta validation; no model-to-layer inference and no exposure of every model to every voice.

Refresh is one durable operation. Flow's per-voice/session lock protects session lifecycle; Orchestrate's path locks protect files, and neither substitutes for the other. Behind the per-voice lock it prepares successor while old run remains current, validates readiness, reaps predecessor, then publishes new name binding as one externally completed `Refreshed` transition. Address/send requests serialize behind persisted pending delivery/subscription; no polling and no dead old route. This is logical atomic publication, not claim of one OS syscall. Recovery may resume only the same persisted authorized attempt with its same Voice, Capsule, and native identities; pre-reap failure retains old run and evidence. It cannot adopt, reassign, or reap an unrelated process. A prior resolved FlowId is ledger reference, not voice-send bypass.

Side flows are independent Capsule/Start harness flows, not harness subagent threads. An ultra-low-power Field router takes ending flow questions/requests under captured authority; requester holds only RequestId, not job ownership. Results may return to requester successor by provenance. Ended-job messages return notice. Router cannot escalate authority and is not inferred to any Layer.

Speech carries authenticated caller authority and explicit delegation at Resolve, Send, and job dispatch. Normative topology uses Aspect.Layer addresses, never model names: “Speech climbs one layer at a time, never skipping a layer, and the Primary layer is spoken to least.” Field normally reaches Psyche through Mind, with rare reasoned direct exceptions; this is briefing guidance, not a wire refusal. Model correspondence comes from the separate knowledge skill and may revalidate pending dispatch as an additional configured constraint without changing layer topology. Administrative adoption is only explicit authenticated meta Assign under configured administrative-process authority, rejected otherwise; twelve unbound slots are initialization, not privilege, and Assign is optional live-flow adoption with no all-slot assignment gate.

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

This is target syntax, not a complete generator input or a claim of supported kinds. Four-root layout is vision example; Operation layout remains expressly proposed in `vision-ethos`. Manifest owns version. Shared types appear in Library; public wire never exposes Memory rows/counters. The target text uses direct CapsuleId, not a Capsule wrapper. Its four listed Layer variants and twelve voices are the settled inventory. The uncompiled layout is not generator witness.

```ethos
Library
[]
[ FlowId.String
  RequestId.String
  CapsuleId.String
  Sequence.Integer
  Layer.[ Primary
          Secondary
          Tertiary
          Quaternary ]
  Voice.[ Psyche.Layer
          Mind.Layer
          Field.Layer ]
  Recipient.[ Voice.Voice
              Request.RequestId ]
  Body.String
  Event.[ Started
          ToolUsed.String
          Stopped ]
  State.[ Running
          Idle
          Ended ]
  Request.[ Question.String
            Work.String ]
  Action.[ Book.{ Title.String
                  Body.Body }
           Handover.{ Body.Body }
           Requests.Vector<Request> ] ]
[]
[]

Signal
[ flow:[ FlowId
         RequestId
         Voice
         Recipient
         Body
         Event
         State
         Request
         Action ] ]
[ Start.{ Voice
          Brief.String }
  Refresh.Voice
  Report.{ FlowId
           Event }
  Resolve.Voice
  List
  Send.{ Recipient
         Body }
  Ask
  Observe.Recipient
  RecordContext.{ Used.Integer
                  Capacity.Integer }
  Yield
  Submit.Vector<Request>
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
  Asked.Vector<{ Subject.String
                 Choices.Vector<String> }>
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
          CapsuleId
          Brief.String }
  Refresh.{ Voice
            CapsuleId }
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
[]

Memory
[ flow:[ FlowId
         RequestId
         CapsuleId
         Sequence
         Voice
         Event
         State
         Request ] ]
[ Admission.{ RequestId
              CapsuleId }
  RequestOccurrence.{ RequestId
                      FlowId
                      Sequence
                      Request }
  Run.{ FlowId
        State
        Vector<Event> }
  Flow.[ Voice.{ Run
                 Voice }
         Job.{ Run
               RequestId } ]
  Slot.{ Voice
         Option<FlowId> } ]
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
  ConfigureContext.Integer ]
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

Memory also retains attempts, authority/policy, handovers/actions and report receipts in its private domain narrative; public references remain identities, never storage rows. No parallel old-format runtime path: migration updates contract, storage and consumers while retaining historic evidence.

## Target datom examples (illustrative opaque words)

All word identifiers are quoted Datom strings, schematic only, and not codec/hash fixtures. Caller identity is process-derived prose context, never encoded as destination.

```text
Start.{ Mind.Primary «Review this design.» }
=> Accepted.«Three Pine Glass»
Observe.Request.«Three Pine Glass»
=> Started.«Cedar River Quartz»

Start.{ Mind.Secondary «Inspect the test result.» }
=> Refused.NoCapsule

Configure.{ Mind.Primary Codex.«illustrative-model» }
=> Configured.Mind.Primary
```

Authenticated Mind.Secondary resolving/sending to an allowed vertical neighbor:

```text
Resolve.Mind.Primary
=> Resolved.«Cedar River Quartz»
Send.{ Voice.Mind.Primary «Review is ready.» }
=> Sent
```

Field.Secondary ordinarily routes design discussion through Mind; direct Field→Psyche requires a rare stated reason under authenticated authority. This is guidance, not a default hard wire refusal.

A hook attributed to one run asserting a different run:

```text
Report.{ «Cedar River Quartz» ToolUsed.«Bash» }
=> Reported
Report.{ «Maple Stone Lake» ToolUsed.«Bash» }
=> Refused.CallerMismatch
```

```text
Ask
=> Asked.[ { «When does a run end?»
             [ «whole run»
               «answer» ] }
           { «May Field speak to Psyche at equal layer?»
             [ «through Mind»
               «direct» ] } ]

Send.{ Request.«Birch Sand Dawn» «follow-up» }
=> Returned.{ «Birch Sand Dawn» Ended }

Refresh.Mind.Primary
=> Accepted.«Oak Wind Star»
Observe.Request.«Oak Wind Star»
=> Refreshed.«Maple Stone Lake»
```

Accepted is admission; Observe reports completion. Examples do not witness live contracts.

## Resolved living guidance

The prior numbered policy parameters are revised by the 2026-10-03 book comments recorded in this flow. Flow is a session; a whole-context restart is a different Flow, and an inactive session is Idle. Flow IDs are word-bearing addressable identifiers for humans and models, while native UUIDs remain correlation. Communication remains authenticated and authority-bound. Its normative speech rule uses Aspect.Layer addresses: speech climbs one layer at a time without skipping, and the Primary layer is spoken to least. The settled address inventory is three aspects × four Layers, or twelve voice slots. Model correspondence belongs to a separate knowledge skill, never topology or inferred layer mapping.

## Authority and acceptance

Mind accepted prior `3ed255…` for planning. Opus 5578cc's amended grant holds wire/registry/hook changes pending Mind review of this revised hash. Only isolated native witnesses are authorized; retained `43b1f66/4cc58229` remain unpushed scope hold. This route is design candidate for Mind/Field, not authority to retry production or claim witness passes. Any build grant attaches after Mind acceptance. Lifecycle, word addressing, four-Layer inventory, and layer-based speech guidance are recorded here.

Preserve 0.24 tests/features. Add caller-process-before-target comparison, shared-server misattribution negative case, Capsule isolation, hook→CLI-only event route, exact inline/verb/identity generation, codec roundtrip, model policy isolation, side-router authority/successor delivery, atomic observed Refresh/crash recovery/no stale route, context handover, and transcript action occurrence/dedup plus quote/tool/incomplete negatives. Add isolated native route witnesses: skill reconstruction, same ProxySession start→turn, policy values, real-turn attach readiness, and failure retention. No launcher deletion until Claude and Codex Flow Start witnesses plus consumer migration; guard removal is independent. No every-defined-slot assignment gate.

Claude witness acceptance requires applying the runner-witnessed opaque credential handoff to the interactive candidate, plus admitted first user turn, native skills, tool/environment, and contact proof; the cited private pane observation alone satisfies none of those delivery checks.

## Sources

- GENERATED editorial specification evidence: [vision-flow](/home/li/primary/.agents/skills/vision-flow/SKILL.md:6), [vision-nexus](/home/li/primary/.agents/skills/vision-nexus/SKILL.md:6), [vision-ethos](/home/li/primary/.agents/skills/vision-ethos/SKILL.md:6). These are not attributed above as living quotations.
- Living records/provenance: [Flow questions/launch/hooks](/home/li/primary/flows/91ea9f/vision/flowNexus.md:1), [lifecycle](/home/li/primary/flows/91ea9f/vision/flowLifecycle.md:1), [voices](/home/li/primary/flows/3ec648/vision/voices.md:3), [hook refresh/action](/home/li/primary/flows/7328f4/vision/hooks.md:13), [Field router](/home/li/primary/flows/b81560/vision/archive-operational-fieldUltraLowRoutesSubflowRequests.md:3), [Capsule](/home/li/primary/flows/3ec648/vision/capsule.md:3), [Flow identity](/home/li/primary/flows/f55ec8/vision/flowIdentity.md:3), [session/idle](/home/li/primary/flows/dea0ba/vision/flowLifecycle.md:1), [speech guidance](/home/li/primary/flows/dea0ba/vision/speech.md:1), [word identifiers](/home/li/primary/flows/9fb0ad/vision/identifiers.md:1), [session/file locks and voices](/home/li/primary/flows/9fb0ad/vision/locking.md:1), [four Layers](/home/li/primary/flows/5578cc/vision/layers.md:1), [knowledge-skill correspondence](/home/li/primary/flows/5578cc/vision/skills.md:1).
- Baseline/pins: [flow-next report](/home/li/primary/flows/f1c841/reports/flow-next.md:76), [Flow Cargo pins](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/Cargo.toml:17), [ordinary contract](/home/li/.cargo/git/checkouts/signal-flow-688d1620dbb6a864/f95034d/ethos/signal.ethos:82), [meta contract](/home/li/.cargo/git/checkouts/meta-signal-flow-d6ff5e00f45b353b/54eb561/ethos/signal.ethos:31).
- Current implementation evidence: [Codex proxy/endpoint](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/codex.rs:1) (`:238` proxy byte bridge, `:56` endpoint selection, `:912/:918/:931/:1033` helpers), [Herdr launch](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/herdr/launch.rs:1255) (`:1337` same-endpoint TUI, `:1403` exact binding), [caller resolver](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/caller.rs:1) (`:42/:114` kernel PID/ancestor resolver). Start/resume helpers currently open separate ProxySessions; start itself has thread/start→turn/start in one. Field connection lifetime is unknown. Current source proves no per-thread Codex hook process; isolated Capsule hook route is requirement. Offline schema at `/tmp/codex-app-server-schema-dea0ba.uhcC1A` is accepted shape only, not environment-runtime proof; turn response does not prove durable rollout.
- Field failure witness: `/tmp/flow-codex-witness-8Ld87N` retained; witness facts above are attributed to Field 42265e and relays 5578cc/41fa34.
- Field positive baseline: canonical `flow-test/hook-socket-f1c841@b18ce4ea`, attributed Field 42265e; `FLOW_TEST_LIVE=1 nix run .#flow-claude-hook` witnessed program-to-program mode-600 credential handoff and baseline SessionStart/PostToolUse/Stop hook reports in its own Nexus. Fixture Herdr/Claude `-p --output-format stream-json` scope does not prove interactive Capsule/Herdr behavior.
- Claude witness limitation: Field 42265e private runtime/session evidence as stated above; private runtimes stopped, and no user-turn/tool/environment/native-skill proof was obtained.
