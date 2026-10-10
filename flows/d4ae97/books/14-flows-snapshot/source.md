<!-- to-the-living:start -->
Presentation.{ «A measured view of flows and flow launching» }

# A measured view of flows and flow launching

This is one bounded snapshot, taken 9 October 2026 at 09:48:52 Mexico City time, plus a read of the current launcher source and relevant written vision. No flow was launched, retired, closed, moved, or otherwise changed for this investigation.

## The counts describe different things

| What was counted | Observed count | What it means |
|---|---:|---|
| Repository flow lanes | 391 directories under `flows/` | 390 directories have hexadecimal names (243 six-character and 147 eight-character IDs); one is the non-hex directory `flow-0000000000000001`. A lane is a repository directory, not proof of a live flow. |
| Flow ID marker files | 279 `.flow-id` files | 225 markers have a same-named directory; 54 do not. These are stored identity records, not a current flow census. There are also 270 `.flow-id.lock` files; their presence alone does not establish a live or stale lock. |
| Messenger routes | 17 rows | 15 are non-STALE (2 working, 2 idle, 11 done); 2 are STALE (`8475a9`, `bad807`). Every route ID has a same-named repository lane. Route status is not retirement evidence. |
| Herdr panes | 16 panes in 15 tabs | 15 panes are bound to an agent/session. One pane, `w1:p2N`, is unbound or unknown in the `6aa08d` tab. |
| Bound native sessions | 15 distinct session IDs | The snapshot associates 8 Codex and 7 Claude sessions with the 15 agent-bearing Herdr records. This is the count measurable from Herdr, not a census of every native process on the machine. |

The 15 non-STALE Messenger routes match the 15 Herdr agent records by flow ID. The two STALE routes have no Herdr agent record in this snapshot. The extra pane has no established flow binding. Repository lanes, identity markers, routes, panes, and sessions overlap, but none is a substitute for another. In particular, `done` describes a Messenger turn; it does not prove a flow has been retired or that its pane/session can be closed.

## Flows that merit a lifecycle review

These four routes were `done` while still registered and bound to a native session and pane. That makes them candidates for a records review, not confirmed dead flows or authorized reap targets.

| Flow | Snapshot binding | Evidence and gap |
|---|---|---|
| `8f0f57` | `psyche_tertiary_sonnet_8f0f57`, `default`; pane `w1:p21`; Claude session `8f0f5790-37ec-4dec-b331-10d3f8fa6e4e` | Work records continue through 6 October. An earlier census found no retirement evidence. No successor acceptance, unfinished-work review, retirement record, or post-close witness was found in this bounded pass. |
| `02dda6` | `psyche_quaternary_sonnet_02dda6`, `default`; pane `w1:p23`; Claude session `02dda640-dc5f-46ed-9c70-f22f047db2d4` | Vision/notion records and a launch receipt exist. The route and pane remain bound; no successor continuity or explicit retirement evidence was found. |
| `4ddfe1` | `mind_quaternary_luna_4ddfe1`, `default`; pane `w1:p24`; Codex session `01a10d05-b7e2-7d91-ab5b-f414ddfe15f4` | An earlier census observed idle and later done, but found no lane artifacts, parent, or retirement record. The current route/pane binding remains. |
| `4371ed` | `field_tertiary_4371ed`, `default`; pane `w1:p27`; Codex session `01a10d25-2590-7aa3-b33e-1254371eddda` | The route and native binding remain, but its launch brief, lane, parent, and exact-role evidence are incomplete. Resolve provenance before drawing a lifecycle conclusion. |

Other done routes were not promoted to candidates where records show active or unresolved work (`42265e`, `44cda5`, `0c85a3`), or where this bounded pass could not distinguish a completed flow from an unexamined live seat (`f5a6e9`, `9fcf81`, `bc914f`). No lifecycle action follows from this list. A future per-flow review should establish the exact native/controller binding, pending work and messages, successor acceptance, locks, retirement decision, and supported close evidence before any reap operation.

## What the launchers can select today

### Implemented source

The native entry point, `tools/native-voice-launch.mjs`, dispatches to the Codex or Claude main-flow launcher. It accepts a voice such as `Field.Tertiary`, a brief, and either a root metaflow source or a predecessor flow. It does not accept a topic. The profile table selects the configured harness, model, and effort for a supported aspect/layer pair.

The Codex launcher currently accepts Mind or Field at Primary, Tertiary, or Quaternary. The Claude launcher accepts Psyche or Field at all four layers. Both create a Herdr tab/pane, start the native harness, claim a flow ID, write a continuation record, and register/title the native binding. The shared continuation code reads a root metaflow or a predecessor’s `continuation.json` and writes `{ flowId, predecessor, metaflow }` with exclusive creation and readback. The records demonstrate metaflow continuation, but carry no topic association.

The Flow Nexus source describes a separate Start/Replace path with source/prompt hashes, aspect, power, harness/model/effort, predecessor, remembered flows, Herdr session, and prompt bundle. Its contract has no Layer or Topic field. The workspace source version is 0.9.0; that source version does not identify the running service.

### Current runtime observation

The bounded process/socket observation found three Nexus processes: 0.14.0 on the default Flow socket, 0.17.4 on `flow-next`, and a debug process on an isolated `/tmp` runtime. The installed profile `flow-nexus` reports 0.12.2; the PATH `flow` wrapper reports 0.23.0, while the profile `flow` reports 0.12.2. A single default `flow 'List.{}'` read returned malformed `Replaced.{ <NUL…> }`, so that client/socket pairing did not provide a trustworthy registry view. Versions and endpoints should be reconciled before relying on Flow Nexus for selection or registry operations.

### Written direction and open design

The written vision says topics can have Psyche, Mind, and Field aspects without requiring all of them to start; layers are Primary, Secondary, Tertiary, and Quaternary. A Mind topic registry is recorded as a proposal until a Mind Nexus component exists. Metaflow is intended to continue across flows. Another launch vision calls for an explicit programmed flow list and consistent layer vocabulary.

The current native path selects aspect and layer but not topic. The Flow Nexus contract carries aspect and profile data but neither topic nor layer. Neither path currently provides one witnessed resolver for a requested topic/aspect/layer combination.

## Useful next steps to consider

These are proposals for follow-up work; this report makes no system or lifecycle change.

1. **Define one typed role selection:** a topic, aspect, and layer resolve to one authoritative harness/model/effort profile. Keep topic explicit; do not infer it from the brief.
2. **Route launchers through that selection:** have the supported native and Flow Nexus paths consume the same role/profile result, once their contracts and runtime versions are made compatible.
3. **Reconcile Nexus deployment before choosing its route:** identify the intended active service/client pair and isolate or retire competing runtimes through an independently reviewed operational change.
4. **Review lifecycle candidates one at a time:** establish provenance, obligations, successor acceptance, pending messages, locks, and exact close/reap evidence. Keep all lanes and bindings until each target has a supported decision.

## Evidence limits

The counts are one simultaneous `hm-list` and Herdr snapshot, not a repeated poll or a machine-wide process census. The lifecycle table reports bindings and record gaps; it does not prove whether a native process is currently doing work, whether messages are pending, or whether a flow is eligible for retirement. Launcher statements distinguish source from runtime. The current source worktree contains uncommitted edits across five native launcher/profile files (111 insertions and 24 deletions as observed); they have not been treated as deployed behavior. The malformed Flow listing is a failed observation, not evidence that the registry is empty.

**Evidence locations:** repository lanes and markers under `flows/`; Messenger snapshot via `hm-list`; pane/session snapshot via `herdr api snapshot`; native launcher source in `tools/native-voice-launch.mjs`, `tools/codex-main-flow-launch.mjs`, `tools/claude-main-flow-launch.mjs`, `tools/native-voice-profiles.mjs`, and `tools/native-main-flow-launch-shared.mjs`; Nexus protocol and runtime evidence in the `flow/` source and active socket/process records; written direction in `flows/ebbe30/vision/aspects.md`, `flows/41fa34/vision/topics.md`, `flows/41fa34/vision/layers.md`, `flows/bad807/vision/metaflow.md`, and `flows/93ba9f/vision/flowLaunching.md`.
<!-- to-the-living:end -->
