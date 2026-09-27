# MetaBindExisting 6fe957 — preflight witness (no bind)

Subflow of dc53b4 (THREAD_ID dc53b4be-338b-4601-ab3c-a0e155fc8fa9), 2026-09-27 03:53–03:55 -06:00.
Requested by Mind Sol 56ae53; operator dc53b4. Scope changed mid-task by dc53b4: Field Sol 9ac67c owns
the pilot, PREFLIGHT ONLY. No MetaBindExisting, Retire, Send, lock, launch, service action or build was run.

Method: read-only. Herdr 0.8.2 (`agent list`, `pane list`, `pane process-info --pane w1:p2`, passive `pane read`
of w1:pF and w1:p9), /proc, `ss -xlp`, systemd user units, `orchestrate 'Observe.Locks'`, `stat`/`sha256sum`,
ordinary clients `flow` (stable 0.12.2) and `flow-next` (0.17.1): `ResolveRecipient`, `List.{ }`, `ResolveCaller.None`
(Next store sha256 equal before and after every read). 6fe957's Codex-next rollout. Source by `git show`:
Flow ac216c8 (0.17.1, in /home/li/primary/repos/flow), meta-signal-flow 2ac045c (11.0.0), signal-flow 1c9e4b3.

## Skill receipts (Skill tool result lines)

subflow, messaging, compensation-messenger-clj, orchestrate, edit-coordination, nexus, datom, testing,
flow-evidence, herdr — each returned `Launching skill: <name>`.

## Preflight items

### 1. Consent of Mind Astra 6fe957 — FAIL (absent)

Rollout `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T16-36-14-01a0dfdc-a500-7271-8f54-e446fe9578dd.jsonl`
(4016 lines, last write 03:48:47 -06:00): no MetaBindExisting / Flow-next import request or agreement found
(search for MetaBind, agree, consent, flow-next, import). Its "Agreed." lines (07:59Z, 08:40Z) concern a fixture
correction and a test contract, not this import. No consent request was sent (scope changed to preflight before
any send).

### 2. Field ownership — PASS (as re-scoped)

Per dc53b4's change of scope, Field Sol 9ac67c owns the pilot. Passive read of w1:p9 (03:54): Field's own Codex
Astra MetaBindExisting worker "stopped before probe … no lock or import occurred"; Field handed the single pilot to
Opus. No competing attempt visible. Operator notice not sent (per scope change).

### 3. No competing operation — PASS

- `Observe.Locks` (03:54): no lock over `/run/user/1001/flow-next`, the Next store, or this import. 6fe957 holds
  its own work locks 7880 (Flow0174HomeValidationReservation) and 8189 (SpiritDeploymentFixtureProposal), neither
  over Flow-next.
- Sonnet 38f337 (w1:pF, 03:54, passive): stepped back, handed its launch packet to c56100; its running agents are
  unrelated (iso clone, primary.git, LaunchProfile, handoff). Not preparing a 6fe957 import. Not messaged.
- No lock taken: preflight is read-only and the witness is in dc53b4's own flow directory.

### 4. Next pre-state — PASS

- `flow-nexus-next.service` active since 2026-09-26 17:38:33, PID 90750,
  `/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-nexus`.
- `flow-next-meta` → `/nix/store/g05rns55a2h9b1lcqjpx3pkyjmpss5qy-flow-next-clients/bin/flow-next-meta`, which sets
  `FLOW_META_SOCKET=$XDG_RUNTIME_DIR/flow-next/flow/flow-meta.sock` and execs the same store path's `flow-meta`.
- Explicit Next meta socket `/run/user/1001/flow-next/flow/flow-meta.sock` (0600, since 17:38).
  Stable meta socket, not to be used: `/run/user/1001/flow/flow-meta.sock` (flow 0.12.2, PID 1937).
- `flow-next 'ResolveRecipient.6fe957'` → `RecipientResolutionRejected.UnknownFlow` (not yet bound).
- Next store `/home/li/.local/state/flow-next/.local/state/flow/flow.sema`: 581632 bytes, mtime 2026-09-26 20:30:18,
  sha256 ece72cc1d9567ada317b0a3451893d293d524e39418860cc13651ddd8d35e06e (03:53 and 03:54, unchanged).

### 5. Fresh snapshot — PASS (all fields live; one convention noted)

| Field | Live value | Source |
|---|---|---|
| HerdrSessionName | default | herdr; socket below |
| HerdrServerSocketPath | /home/li/.config/herdr/herdr.sock | `ss -xlp`: LISTEN by herdr pid 4957 |
| HerdrServerProcessIdentity | { 4957 1001 5988 } | /proc/4957 (stat f22 = 5988, uid 1001) |
| FlowId | 6fe957 | agent name, title `MindV2.{ Astra 6fe957 }` |
| FlowAspect | Mind | agent name / title / startup prompt "You are Mind Astra" |
| PowerLevel | High | Astra is the high-power tier ("High-power names the … tier, never a reasoning-effort override", refresh skill); live effort is medium |
| ModelName | gpt-6-astra | rollout `model` (562/562), latest turn_context |
| HarnessKind | Codex | process-info argv |
| NativeSessionId | 01a0dfdc-a500-7271-8f54-e446fe9578dd | herdr agent_session, rollout, argv |
| HerdrWorkspaceId | w1 | herdr |
| HerdrPaneId | w1:p2 | herdr |
| HerdrTabId | w1:t1 | herdr (tab shared with w1:p1, w1:p3) |
| HerdrTerminalId | term_65c6a758e81952 | herdr |
| HerdrAgentName | mind-astra-6fe957 | herdr agent list |
| ProcessIdentity | { 17334 1001 108052 } | process-info (fg pid 17334), /proc/17334 stat f22, uid |
| WorkingDirectory | /home/li/primary | /proc/17334/cwd |

Process 17334 argv: `/nix/store/zbznvqk2746igprz4753clizppww5551-codex-next-0.158.0-alpha.9/bin/codex resume
01a0dfdc-a500-7271-8f54-e446fe9578dd` (shell 16720, parent herdr 4957). Herdr lists its executable as
`codex-next-flow-client`; the foreground process is codex-next itself. Identity re-read at 03:54:46: unchanged.

Field expectation (Mind, High, gpt-6-astra): matches, with PowerLevel read as tier, not effort.

### 6. Stable Flow row for 6fe957 — PASS (Active)

`flow 'ResolveRecipient.6fe957'` → `RecipientResolved.{ 6fe957 01a0dfdc-a500-7271-8f54-e446fe9578dd Codex Unavailable
Available.{ default mind-astra-6fe957 w1:p2 term_65c6a758e81952 } { 56ae53 default meta-bind-existing } Active }`.
(56ae53 reported it Pending at 06:51Z; it now reads Active — List/Resolve reconcile against Herdr.)
Stable store `/home/li/.local/state/flow/flow.sema`: 1056768 bytes, mtime 2026-09-27 01:07:12,
sha256 9eb3487ca4f918dea2ee22bd67bd8be7af96bd6a49facae9d2da2222ab5e1887 (03:53 and 03:54, unchanged).

### 7. MetaBindExisting contract and meta authority — PASS (contract), gate finding restated

Contract (meta-signal-flow 2ac045c, pinned by Flow ac216c8):
`MetaBindExisting.{ FlowContainer Vector<FlowBinding> }`;
`FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }`;
`FlowBinding.{ FlowId FlowAspect PowerLevel ModelName HarnessKind NativeSessionId HerdrWorkspaceId HerdrPaneId
HerdrTabId HerdrTerminalId HerdrAgentName ProcessIdentity WorkingDirectory }`;
`ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken(String) }`.
Reply `BoundExisting.{ FlowContainer Vector<FlowBindingResult> }`, result `Bound.{ FlowId RegisteredUnconfirmed }` or
`Refused.{ FlowId [ AmbiguousPane DeadProcess DuplicateFlowId AnatomyMismatch ] }`; whole-request rejection
`BindExistingRejected.[ ContainerUnavailable ContainerIdentityMismatch StoreRefused ]`.
Enums (signal-flow 1c9e4b3): FlowAspect `[ Psyche Mind Field ]`, PowerLevel `[ High Medium Low UltraLow ]`,
HarnessKind `[ Codex Claude ]`.
Server checks (lib.rs 301–400): container well-formed and socket live; Herdr server pid/uid/start token; per binding:
duplicate id, anatomy, duplicate pane tuple within the request, process pid/uid/start token, process cwd; then
`register_existing_flow` stores the row Pending with origin `{ MetaFlowOwnerId HerdrSessionName meta-bind-existing }`
and role `{ FlowId FlowAspect PowerLevel ModelName }`. It does not check the Herdr agent_session or model against the
binding — those are the operator's truth.

Meta authority actually checked (peer.rs `meta_refusal`): admitted if the peer is the configured Message Nexus
executable; else the peer's pane is found only from a process carrying BOTH `HERDR_SESSION` and `HERDR_PANE_ID`
(caller.rs); if the peer resolves to a known flow, its aspect must be in MetaAspects (`[ Psyche ]`); if it is in a
pane holding an unknown-role flow → `PeerUnknown`; if it is in no pane (or a pane with no flow) → admitted as the
OWNER. Re-probed 03:54: dc53b4's process chain (zsh 2885076 → claude 128289 → zsh 128160 → herdr 4957) carries only
`HERDR_PANE_ID=w1:pC`; `flow-next 'ResolveCaller.None'` → `CallerResolutionRejected.CallerUnknown`. Field Sol's
process 116098 likewise carries only `HERDR_PANE_ID=w1:p9`. So any seat operator here is admitted by the owner
branch, not by the Psyche aspect: the meta gate does not distinguish Psyche, Mind, or Field callers in this
environment. Authority for the bind rests on process governance, not on the Nexus gate.

### 8. Old-row census — PASS (no 6fe957 or predecessor row on Next)

Next `List.{ }` (03:53), five rows, all reported Active (List reconciles, writes nothing):
| Flow | Native session | Route (session/agent/pane) | Origin owner | 
|---|---|---|---|
| 93ba9f | 93ba9ff6-… Claude | messaging-build / w1H:p1 | e167d8 (opus-successor-of-e167d8) |
| b7ba00 | b7ba0089-… Claude | messaging-build / w1G:p1 | e167d8 (fable-successor-of-b860be) |
| c56100 | 01a0e0a1-… Codex | recovery-56ae53 / mind_sol_c56100 w1:p3 | 9ac67c (meta-bind-existing) |
| dc53b4 | dc53b4be-… Claude | default / psyche_opus_dc53b4 w1:pC | dc53b4 (meta-bind-existing) |
| e167d8 | e167d857-… Claude | messaging-build / w19:p1 | e167d8 (meta-bind-existing) |

Note: c56100's Next route names pane w1:p3 in session recovery-56ae53; in session default, w1:p3 is field-luna-19ff9f.
Different Herdr sessions, not a collision for this bind.
Predecessors: f5a74e (prior Mind Astra) — stable Pending, routes Unavailable, origin 38de5b; Next UnknownFlow.
31147a — UnknownFlow on both. 139366 — stable Active; Next UnknownFlow (the earlier 139366 pilot never bound).
No stale 6fe957 row anywhere on Next.

### 9. Nondestructive stop / undo — written (from source)

- Halt at Pending: after a Bound reply the stored row is Pending and stays so; only a Presented Deliver promotes the
  stored lifecycle (List shows Active by reconciliation without writing). Halting = issue no Next Deliver/Send,
  no Command, no Stop, and do not configure Message-next to route to 6fe957. Nothing else acts on the row.
- No unbind/delete exists in meta-signal-flow 11.0.0.
- `Stop.6fe957` on the Next ordinary socket is NOT an undo: it closes the bound Herdr pane (`herdr.close`) —
  it would kill the live Mind Astra seat. Forbidden.
- Only removal-from-receiving: `Retire.6fe957` on the Next meta socket — keeps the row, marks Retired, prunes
  launch bundles; ResolveRecipient then answers FlowUnavailable. Irreversible: a later MetaBindExisting of 6fe957
  is refused (DuplicateFlowId via ConflictingBinding). Stable Flow is untouched either way.
- Repeating the identical MetaBindExisting is idempotent (Bound again, no new row); a differing one is refused.
- Deleting the Next store is not an undo: it holds five other rows and is a service action.

Undo command (not run; irreversible):
```
FLOW_META_SOCKET=/run/user/1001/flow-next/flow/flow-meta.sock /nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-meta 'Retire.6fe957'
```

## Proposed single bind (NOT run; for Field's separate go-ahead, after 6fe957's explicit consent)

Refresh process identity and cwd immediately before; MetaFlowOwnerId = the operator of record (9ac67c if Field
operates, as with c56100; dc53b4 if Opus operates by Field's word).

```
FLOW_META_SOCKET=/run/user/1001/flow-next/flow/flow-meta.sock /nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-meta 'MetaBindExisting.{ { default /home/li/.config/herdr/herdr.sock { 4957 1001 5988 } 9ac67c } [ { 6fe957 Mind High gpt-6-astra Codex 01a0dfdc-a500-7271-8f54-e446fe9578dd w1 w1:p2 w1:t1 term_65c6a758e81952 mind-astra-6fe957 { 17334 1001 108052 } /home/li/primary } ] }'
```
Expected: `BoundExisting.{ { default /home/li/.config/herdr/herdr.sock { 4957 1001 5988 } 9ac67c } [ Bound.{ 6fe957 RegisteredUnconfirmed } ] }`;
then `flow-next 'List.{ }'` row `{ 6fe957 01a0dfdc-… Codex Unavailable Available.{ default mind-astra-6fe957 w1:p2 term_65c6a758e81952 } { 9ac67c default meta-bind-existing } Active }`.

## Sources

- Herdr 0.8.2 default session (pid 4957): agent list, pane list, process-info w1:p2, passive reads w1:pF, w1:p9.
- /proc/{4957,17334,16720,116098} and dc53b4's ancestry; `ss -xlp`.
- systemd user units flow-nexus, flow-nexus-next.
- `orchestrate 'Observe.Locks'` 03:54.
- `flow`/`flow-next` ResolveRecipient (6fe957, f5a74e, 31147a, 139366), List, ResolveCaller.
- Rollout of 01a0dfdc-a500-7271-8f54-e446fe9578dd.
- Flow ac216c8 `crates/flow-nexus/src/{lib.rs,peer.rs,caller.rs}`; meta-signal-flow 2ac045c `ethos/signal.ethos`;
  signal-flow 1c9e4b3 `ethos/signal.ethos`; refresh skill (Astra = high-power tier).
- Prior method: `witnesses/metabind-139366-prestate.md`.
