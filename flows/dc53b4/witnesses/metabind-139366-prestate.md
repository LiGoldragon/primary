# MetaBindExisting 139366 — pre-state witness

Subflow of dc53b4 (THREAD_ID dc53b4be-338b-4601-ab3c-a0e155fc8fa9), 2026-09-27 03:17–03:21 -06:00.

Method: read-only. Shell observation of systemd user units, /proc, `ss`, Herdr 0.8.2
(`pane list`, `agent list`, `pane process-info`, `pane read` — passive), `orchestrate 'Observe.Locks'`,
`sha256sum`/`stat`, the Next ordinary client (`flow-next 'ResolveRecipient.139366'`, `flow-next 'List.{ }'`;
List is documented in source as writing nothing; Next store hash equal before and after), the Codex-next
rollout of 139366, and `git show` of Flow source at ac216c8 (the Flow 0.17.1 head) and meta-signal-flow
2ac045c (pinned by it). No import, lock, send, prompt, service action or build.

## Gate 1 — Sonnet 38f337 stand-down: FAIL

- 38f337 has NOT stood down. Its log (`/home/li/wt/primary/opus-sonnet-56ae53/flows/38f337/log.md`, last
  entries) and its pane w1:pF (read 03:20:38) show it accepted the same operator role from 9ac67c, completed
  preparation (witness `flows/38f337/witnesses/flow-next-import-139366-prep.md`, 03:19), and a backgrounded
  agent "Report prep receipts to Field" finished — reporting "ready for Field's own gate confirmation" to 9ac67c.
- No import operation of 38f337 is in flight: its prep witness states no MetaBind; Next still UnknownFlow at 03:20.
  Remaining background agent is unrelated ("Diagnosing failed fetch in iso-38f337/repo").
- Locks: 38f337's lock 8446 (scoped to its witness file only) acquired and released. `Observe.Locks` at 03:20:
  no lock held by 38f337, dc53b4 or 9ac67c; no lock covers `/run/user/1001/flow-next`, the Next store or this import.
- Consequence: two operators hold an acceptance for one consented import. 9ac67c must name exactly one.

## Gate 2 — Next Nexus: PASS

- `flow-nexus-next.service` active since 2026-09-26 17:38:33, PID 90750,
  ExecStart `/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-nexus`.
  `message-nexus-next.service` active (PID 90762, message-0.17.0). `flow-configuration-next` exited 0, MetaAspects `[ Psyche ]`.
- Client: `flow-next-meta` → `/nix/store/g05rns55…-flow-next-clients/bin/flow-next-meta`, a wrapper that
  execs `/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-meta` — same store path as the service.
- Explicit Next meta socket: `/run/user/1001/flow-next/flow/flow-meta.sock` (live, 0600).
  Stable meta socket, not to be used: `/run/user/1001/flow/flow-meta.sock` (flow 0.12.2).
- `flow-next 'ResolveRecipient.139366'` → `RecipientResolutionRejected.UnknownFlow` (03:18 and 03:20).
- Next store `/home/li/.local/state/flow-next/.local/state/flow/flow.sema`, 581632 bytes,
  sha256 ece72cc1d9567ada317b0a3451893d293d524e39418860cc13651ddd8d35e06e (unchanged across the reads).
  It is NOT empty: List holds 93ba9f, b7ba00, c56100 (origin 9ac67c meta-bind-existing), dc53b4
  (origin dc53b4 meta-bind-existing, pane w1:pC), e167d8.
- Meta gate (peer.rs): dc53b4's pane holds the Next row dc53b4; its role must be Psyche to be admitted
  (MetaAspects `[ Psyche ]`); a flow whose role Next does not know gets `MetaRefused.PeerUnknown`.
- Probed read-only: `flow-next 'ResolveCaller.None'` from dc53b4's process tree → `CallerResolutionRejected.CallerUnknown`
  (store hash unchanged). Cause, from caller.rs: a pane is located only from a process carrying both
  `HERDR_SESSION` and `HERDR_PANE_ID`; dc53b4's ancestry (zsh 2831735 → claude 128289 → zsh 128160 → herdr 4957)
  carries only `HERDR_PANE_ID=w1:pC`. So the meta gate would read dc53b4 as "in no pane: the owner" and admit it —
  admission would rest on the owner branch, not on the Psyche aspect. The same holds for any seat lacking `HERDR_SESSION`.

## Gate 3 — stable store: PASS (baseline taken)

`/home/li/.local/state/flow/flow.sema` (held open by stable flow-nexus 0.12.2, PID 1937):
1056768 bytes, mtime 2026-09-27 01:07:12 -0600,
sha256 9eb3487ca4f918dea2ee22bd67bd8be7af96bd6a49facae9d2da2222ab5e1887 (03:18 and 03:20). Matches 38f337's baseline.

## Gate 4 — template refresh: PASS, no drift in any live field

Type (meta-signal-flow 2ac045c): `MetaBindExisting.{ FlowContainer Vector<FlowBinding> }`;
`FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }`;
`FlowBinding.{ FlowId FlowAspect PowerLevel ModelName HarnessKind NativeSessionId HerdrWorkspaceId HerdrPaneId
HerdrTabId HerdrTerminalId HerdrAgentName ProcessIdentity WorkingDirectory }`;
`ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken }` (start token = /proc stat field 22).

| Field | Template | Live | Source |
|---|---|---|---|
| HerdrSessionName | default | default | herdr pane list |
| HerdrServerSocketPath | /home/li/.config/herdr/herdr.sock | same, LISTEN by herdr pid 4957 | ss -xlp |
| HerdrServerProcessIdentity | { 4957 1001 5988 } | { 4957 1001 5988 } | /proc/4957 |
| MetaFlowOwnerId | 56ae53 | no live value; provenance only | see note |
| FlowId | 139366 | 139366 | agent name, rollout id suffix |
| FlowAspect | Mind | Mind | agent name mind-luna-139366 |
| PowerLevel | Medium | Medium | rollout effort "medium" (24/24) |
| ModelName | gpt-6-luna | gpt-6-luna | rollout "model" (99/99) |
| HarnessKind | Codex | Codex | process-info argv codex resume … --remote codex-next |
| NativeSessionId | 01a0e032-e8aa-7131-90c4-a54139366ece | same | herdr agent_session, rollout |
| HerdrWorkspaceId | w1 | w1 | herdr |
| HerdrPaneId | w1:pD | w1:pD | herdr |
| HerdrTabId | w1:tB | w1:tB | herdr |
| HerdrTerminalId | term_65c6bcfd5cea0d | same | herdr |
| HerdrAgentName | mind-luna-139366 | same | herdr agent list |
| ProcessIdentity | { 129350 1001 685202 } | { 129350 1001 685202 } | process-info, /proc/129350 |
| WorkingDirectory | /home/li/primary | /home/li/primary | /proc/129350/cwd |

Owner note: MetaFlowOwnerId is written only as the row's `origin_clue.flow_id` (turn_id "meta-bind-existing").
Next precedent: dc53b4's own row carries owner dc53b4; c56100's carries 9ac67c. 56ae53's route is recorded stale.
If dc53b4 operates, the truthful provenance is dc53b4 (old 56ae53 → new dc53b4); a choice, not a drift.

## Gate 5 — undo: PARTIAL (from source)

- Undo is `Retire.139366` on the same Next meta client/socket (lib.rs:259–299). It keeps the row, its origin and
  history, sets lifecycle Retired, prunes launch bundles, and takes the flow out of receiving. It is not a delete:
  afterwards ResolveRecipient answers FlowUnavailable, not UnknownFlow.
- After Retire, a new MetaBindExisting for 139366 is refused (assert_role_of_matching_binding requires a live
  stored flow → ConflictingBinding → DuplicateFlowId). Retire is one-way for this FlowId in this store.
- No unbind/delete request exists in meta-signal-flow 11.0.0.
- 38f337's fallback undo (stop Next, delete Next's store, restart) is unsafe: the store holds five other rows
  (dc53b4 and c56100 among them) and it is a service action.
- A repeated identical MetaBindExisting is idempotent (same route/thread/role → Bound again, no new row).

## Gate 6 — Mind Luna consent: PASS (witnessed natively)

Rollout `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T18-10-27-01a0e032-e8aa-7131-90c4-a54139366ece.jsonl`:
- 09:12:22.721Z user (from Field Sol 9ac67c): "…do you agree to ONE supported no-launch MetaBindExisting import of
  your existing native seat into Flow-next 0.17.1? … Please reply explicitly agree or decline; do not execute the import yourself."
- 09:12:38.528Z assistant: "139366 MainFlow «I explicitly agree to one supported, no-launch MetaBindExisting import
  of my existing native seat into Flow-next 0.17.1. Stable Flow and Messenger remain authoritative. No Next Send,
  service switch, seat launch, or activation is authorized.» [] [] []"
Consent names no operator.

## Proposed command (not run)

```
FLOW_META_SOCKET=/run/user/1001/flow-next/flow/flow-meta.sock /nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-meta 'MetaBindExisting.{ { default /home/li/.config/herdr/herdr.sock { 4957 1001 5988 } dc53b4 } [ { 139366 Mind Medium gpt-6-luna Codex 01a0e032-e8aa-7131-90c4-a54139366ece w1 w1:pD w1:tB term_65c6bcfd5cea0d mind-luna-139366 { 129350 1001 685202 } /home/li/primary } ] }'
```

Expected: `BoundExisting.{ { default … dc53b4 } [ Bound.{ 139366 RegisteredUnconfirmed } ] }`.

Undo (not run):

```
FLOW_META_SOCKET=/run/user/1001/flow-next/flow/flow-meta.sock /nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-meta 'Retire.139366'
```

## Sources

- systemd user units flow-nexus, flow-nexus-next, flow-configuration-next, message-nexus-next, orchestrate-nexus.
- /proc/{1937,90750,4957,129350}; `ss -xlp`.
- Herdr 0.8.2 default session: pane list, agent list, process-info w1:pD, passive read w1:pF.
- `orchestrate 'Observe.Locks'` at 03:17 and 03:20.
- `/home/li/wt/primary/opus-sonnet-56ae53/flows/38f337/log.md` and its witness `flow-next-import-139366-prep.md`.
- Flow ac216c8 (`crates/flow-nexus/src/lib.rs`, `store.rs`, `peer.rs`, `crates/flow-meta/src/main.rs`);
  meta-signal-flow 2ac045c `ethos/signal.ethos`; signal-flow 1c9e4b3 enums.
- Codex-next rollout of 01a0e032-e8aa-7131-90c4-a54139366ece.
