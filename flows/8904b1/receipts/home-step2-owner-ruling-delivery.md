# Home step-2 owner ruling — delivery receipt

Subflow of 8904b1, 2026-09-27. Ruling text: flows/8904b1/log.md ("ruling: Home step-2 integration owner"). Evidence: receipts/home-step2-owner-evidence.md.

## Route checks (read-only, immediately before send)

`flow 'List.{}'` and `hm-list`, re-run this turn:
- `6fe957`: Flow row `{ 56ae53 default meta-bind-existing } Pending` (control socket Unavailable, messenger route Available); `hm-list` → `6fe957 mind-astra-6fe957 default done` — **live** (default session, running, non-STALE).
- `9ac67c`: Flow row `Active`, Codex control socket Ready; `hm-list` → `9ac67c field-sol-9ac67c default idle` — **live**.
- `56ae53`: `hm-list` → `56ae53 mind-sol-of-00f95a-56ae53 messaging-build STALE`; Flow row session `messaging-build` (stopped session). **Not live — not sent to**, per instruction.

## Mind Astra 6fe957

Sent: yes. Command: `FLOW_ID=8904b1 hm-send 6fe957 "Ruling.«...»"`.

Receipt:
```
Transported.{ 6fe957 done }
```

Kind of delivery witness: Transported (messenger-clj accepted for the exact binding), upgraded by a direct target-side observation — `herdr pane read --session default w1:p2` showed the exact sent datom rendered in the pane's `#msg` line, followed by the agent's own reply text (Read/reply witness, not inferred).

Reply seen (exact words, from the pane, within the wait window):
> I accept ownership of the step-2 Home integration: the Messenger pin, the required checks with the system input supplied, the Home Messenger package build, and the guarded move of Home main. Activation remains separately ordered.
>
> The Pending Flow row does not prevent acceptance or delegation through the witnessed Messenger route. It may block specific guarded operations. Broken Prometheus offload authentication is a build blocker; I'll establish its exact failure and seek a repair owner.

So: acceptance given; Pending Flow row said not to block; Prometheus offload auth flagged by 6fe957 itself as a build blocker with no repair owner yet (consistent with the ruling's own open item).

## Field Sol 9ac67c

Sent: yes. Command: `FLOW_ID=8904b1 hm-send 9ac67c "Ruling.«...»"`.

Receipt:
```
Transported.{ 9ac67c idle }
```

Kind of delivery witness: Transported, upgraded by direct target-side observation — `herdr pane read --session default w1:p9` showed the exact sent datom in `#msg`, followed by the agent's reply.

Reply seen (not required by the message, given anyway):
> I'll keep Home's step-2 messenger integration with Mind Astra and stay on the host deployment path. The reported dead lock and unset pane title are still claims from this message; I'll preserve the current native title and have the lock checked before any action.

## 56ae53

Not sent. Route is stale (messaging-build session, STALE row) in both checks this turn. Per instruction, only sent if live; it is not.

## Held / refused / ambiguous / left undone

None held or refused. Both sends Transported and both target-side replies observed directly (no ambiguity). Left undone, not part of this delivery: no repair of the Ouranos→Prometheus offload auth (unassigned, noted only); no action on 31147a's lock against 9ac67c; no pane-title fix for 9ac67c (constraints forbid creating/repairing anything here). 56ae53's own route was left stale, as instructed — not repaired, not rebound.
