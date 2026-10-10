# Witness-location delivery to Mind Astra 6fe957 — receipt

Subflow of 8904b1, 2026-09-27. Task: tell 6fe957 the absolute location of the
stale-lock witness (receipts/stale-lock-witness-7359-31147a.md) and what it
holds/lacks, since 6fe957 reported the previously supplied path is not
present in its own checkout.

## Witness file check (read-only)

- Path: `/home/li/wt/primary/56ae53/flows/8904b1/receipts/stale-lock-witness-7359-31147a.md`
- Present and readable: yes (read directly).
- Holds: §1 direct `Observe.Locks` record of lock 7359 (BuildZeus31147a,
  holder 31147a, single Zeus path, authorization reason); §2 holder 31147a's
  stale state independently witnessed (hm-list STALE, no live Herdr pane, one
  held `hm-send` with exact receipt `Held.{ 31147a RepairRequired
  5c544fc1-314b-4e08-af17-f2997fe309cf } candidates=[]`); §3 process/open-handle
  check (`pgrep -af 31147a` and `lsof +D` on the workspace both empty).
- Lacks: §5 the failed Zeus evaluation's exact error text — found in no record
  searched (only Field Sol 9ac67c's quoted claim, unconfirmed); §4 confirms
  absence of local/orchestrating-side build activity only — Prometheus itself
  was not reached, so "no active build" is not independently confirmed there.

## Route check (read-only, immediately before send)

- `FLOW_ID=8904b1 flow 'List.{}'` → `6fe957` row: control socket Unavailable,
  Flow row Pending, messenger route Available.{ default mind-astra-6fe957
  w1:p2 term_65c6a758e81952 } in the running `default` session.
- `FLOW_ID=8904b1 hm-list` → `6fe957  mind-astra-6fe957  default  working`.
- `herdr session list` → `default` running, `messaging-build` stopped.

Route judged live for the messenger transport; sent.

## Sent

One send only. Command:
`FLOW_ID=8904b1 hm-send 6fe957 "WitnessLocation.«...»" --wait-presented`

Body sent (single guillemet-string datom variant, full text):

```
WitnessLocation.«From Psyche Fable 8904b1. Your acceptance of the Zeus evaluate/build gate and the stale-lock takeover of 7359 is recorded. The preserved observations you asked for are at the absolute path /home/li/wt/primary/56ae53/flows/8904b1/receipts/stale-lock-witness-7359-31147a.md in this checkout — not a path relative to yours, since your checkout is different. It holds: the direct Observe.Locks record of lock 7359 (BuildZeus31147a, holder 31147a, the one Zeus path, the authorization reason), 31147a's stale state independently witnessed here (hm-list STALE, no live Herdr pane, and the held hm-send with its exact receipt Held.{ 31147a RepairRequired 5c544fc1-314b-4e08-af17-f2997fe309cf } candidates=[] — you do not need to send to 31147a again), and the process/open-handle check (pgrep and lsof on the workspace both empty). It does NOT hold: the failed Zeus evaluation's exact error text, found in no record searched here (only Field Sol's quoted claim, unconfirmed); and it does not confirm absence of an active build on Prometheus — only the local/orchestrating side was witnessed, Prometheus was not reached. Release under the stale-lock procedure is authorized to you alone; then lock the path anew as yourself. Report to 8904b1 the release and the new lock with what the lock service answered, then the frozen source identity or a blocker, before evaluation.»
```

Receipt printed (exact):

```
messenger-clj: Uncertain.{ 6fe957 attempt-751b7bff-450 } prompt failed or is uncertain: {"error":{"code":"timeout","message":"timed out waiting for agent status"},"id":"cli:agent:prompt"}
```

Exit code 1.

## Delivery grade

Uncertain — not Submitted, not Transported, not Presented, not Read. The
transport itself reported a timeout waiting for agent status; no confirmation
that the bytes reached the target pane. Per the messaging skill and the
one-send constraint, this attempt is not retried, rerouted, or escalated to
another channel by this subflow. The held/uncertain attempt and its declared
successor rule own any later delivery.

## Reply seen

None within the observation window of this subflow.

## Left undone

- No confirmation the message reached 6fe957's pane or was read.
- No second send attempted (one-send constraint).
- No lock action of any kind taken or requested (out of scope here; reserved
  for 6fe957 alone per the ruling).
- The frozen-source/blocker report and the release-and-relock report remain
  6fe957's own subsequent work to send back to 8904b1.
