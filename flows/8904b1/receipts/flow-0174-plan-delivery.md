# Flow 0.17.4 three live-start witness plan: delivery to Mind Sol 56ae53

Subflow of 8904b1 (this seat acting directly, no nested agent per brief).
Delivers the three live-start witness plan (report:
/home/li/wt/primary/56ae53/flows/8904b1/reports/flow-0174-three-live-start-witness-plan.md)
to Mind Sol 56ae53, plus the four standing statements the brief requires.

No declared root Datom type exists for a message of this kind (same finding
as flows/8904b1/receipts/flow-0173-position-delivery.md). Following the
precedent already used for this recipient, the body is plain prose carrying
the plan in compact form with every case and limit, not an invented datom
structure.

## Route resolution

`FLOW_ID=8904b1 hm-list` immediately before sending:
- `56ae53 mind-sol-of-00f95a-56ae53 messaging-build STALE` — not live. Per
  the brief, reply is asked to go through Mind Luna 139366 for relay.
  Confirmed stale by this poll; message sent to 139366, marked for relay,
  not to 56ae53 directly.
- `139366 mind-luna-139366 default done` — live.
- `herdr pane read w1:pD --lines 60` immediately before sending: composer
  showed the placeholder "Ask Codex to do anything" — no unsent text.

One send made, to one recipient (139366). No send to any other flow.

## Send: Mind Luna 139366 (relay to Mind Sol 56ae53)

- Command: `FLOW_ID=8904b1 hm-send 139366 "<body>"`
- Grade observed: **Transported** — `Transported.{ 139366 done }`
- Body sent (exact bytes):

```
Relay to Mind Sol 56ae53 (its route is stale; this seat asks Mind Luna 139366 to relay). From Psyche Fable 8904b1: three live-start witness plan for the Flow 0.17.4 track, defined per your handoff. Full report: /home/li/wt/primary/56ae53/flows/8904b1/reports/flow-0174-three-live-start-witness-plan.md

Plan, compact, every case and limit:
Target: 0.17.4 tagged source, built and run as a scratch instance with its own socket and empty store -- not the installed next service, not stable, not their stores. Real Herdr, real Claude harness.
Seats: disposable, own Herdr workspace, test aspect (no real role), least-costly Claude model, medium effort, one at a time, each closed by its own pane/process, never by name or pattern.
Profile: small ordered skill set, spirit first, then two more.
Three starts: A -- two short lines, plain. B -- longer than 800 units, wrapped. C -- one short line, plain.
Pass, for each: Flow's row reaches started AND an oracle outside Flow shows the native transcript's first user entry matches the stored prompt, each selected skill expanded through the skill interface in order, model and effort as intended. Flow's verdict and the transcript must agree.
Must-fail cases, seen failing before the passes are trusted: D -- a profile selecting a skill that cannot load, must not reach started. E -- observed model differs from intended, must be refused. F -- first entry text does not match the stored prompt, must not be accepted.
Also recorded per start: any false-failed record against an actual held prompt; submit-to-started time; startup context spent.
Bounds: a timeout and a memory cap on every run; waits are on the observed event, not the clock.
Limits of authority: no live service started, stopped, or restarted; no live store read for writing; no real role taken; no Home edit; no activation.
Proves and does not: proves 0.17.4 starts a Claude seat by each of the three routes and tells good from bad; does not prove the installed service, the stable step, or the stores.
Owner of the run: Flow's owner, Mind Sol 56ae53, through an independent testing worker; evidence returns to this seat as gate evidence for activation condition 4.

Also, from this seat:
This seat accepts the living's quoted words, "You should use the newer Flow. You should just install it and use it.", as the order to install and use the newer Flow, and will not ask for that order again.
The override decision, activation condition 1 on the stable-Flow service override, stays open: those words were typed before anyone knew an activation following Home main would also restart stable Flow and Message.
The semantic review of the 0.17.3 to 0.17.4 delta is under way; its concerns will follow.
The run described above is the owner's, through an independent testing worker; its evidence returns to this seat as gate evidence.
No activation is authorized by this message.
```

- Reply seen within the check window: none. A bounded status poll of
  `139366` for ~2.5 minutes after send showed no status-line change from
  `done` (no `working`/`idle` transition observed, no reply text seen).

## Constraints honored

- One send, to one recipient. No send to any other flow, no probing.
- Route resolved immediately before sending via `hm-list` (56ae53) and
  `hm-list` + `herdr pane read` (139366, live and composer clear).
- No create/repair/retire/rebind of any route; no lock action; no
  repository touched; nothing launched.
- No grade claimed above what the transport itself reported (`Transported`).
