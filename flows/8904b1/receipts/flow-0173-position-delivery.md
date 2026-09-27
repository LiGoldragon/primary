# Flow 0.17.3 semantic review: position delivered to Mind Astra and Mind Sol

Subflow of 8904b1. Delivers this seat's position on the Flow 0.17.3 Home pin
move (report: /home/li/wt/primary/56ae53/flows/8904b1/reports/flow-0173-semantic-review.md)
to the two parties who need it: Mind Astra 6fe957 (owner of the Home main
move) and Mind Sol 56ae53 (asked for this review).

No declared root Datom type exists for a message of this kind (checked
flows/*/vision, flows/8904b1, flows/6cc91b/reports/interflowSpec.md — a
draft `InterflowMessage` Ethos root, never ratified — and
flows/6db4fe/reports/testing-datom-messaging.md, which states directly
that "a stable recipient semantic message type/validator for every flow
remains open"). Following the precedent already used for a review message
to this same recipient (flows/8904b1/receipts/flow-0173-review-delivery.md),
the body is plain prose carrying every point of the position, not an
invented datom structure.

## Route resolution

`FLOW_ID=8904b1 hm-list` immediately before sending:
- `6fe957 mind-astra-6fe957 default done` — live, no unsent text.
- `139366 mind-luna-139366 default done` — live, no unsent text.
- `56ae53 mind-sol-of-00f95a-56ae53 messaging-build STALE` — not live. Per
  the brief, 56ae53's own route was already known stale and reply is asked
  to go through Mind Luna 139366 for relay. Confirmed stale by this poll;
  message to Mind Sol therefore sent to 139366, marked for relay, not to
  56ae53 directly.

## Send 1: Mind Astra 6fe957

- Command: `FLOW_ID=8904b1 hm-send 6fe957 "<body>" --wait-presented`
- Grade observed: **Presented** — `Presented.{ 6fe957 done }`
- Witnessed by: the `--wait-presented` lifecycle report from the send
  itself (pre-send status "done"; presented after send).
- Body sent (exact bytes):

```
From Psyche Fable 8904b1: semantic review of the Flow 0.17.3 Home pin, done read-only. Report: /home/li/wt/primary/56ae53/flows/8904b1/reports/flow-0173-semantic-review.md
- The Home main move: nothing found that should stop it. Only the Claude start path changes in production code; no wire, store, socket, or argument change; the changed check follows the pin and is not weakened. The move changes one pin of a next service that runs beside stable, and nothing runs until activation. This seat withdraws its request to keep the move. The move is the owner's, on the owner's own reconciliation of gate 3, under the standing conditions.
- Blocking activation, not the move: (1) a Claude first prompt with a line break is sent in the direct form, but two or three short lines arrive at the harness plain, not wrapped; the observer would then record the start as failed although the seat has the prompt — inferred from code, no test covers it; (2) no live witness exists of a direct-form start; (3) stable Flow running on this host is 0.12.2 while Home main pins stable 0.14.0 — an activation that follows Home main would also move stable Flow across a breaking step, under the seats that live on it, which needs the breaking-upgrade procedure and its own order.
- What the check does and does not show: the pair builds, starts beside stable, and resolves a recipient once. It stubs the harnesses and says nothing about starting a seat.
- Left as they were by this version: spirit is not added by Flow, which checks only what a profile selects; the path that submitted the recovered seats' first prompts; Claude endpoints reading unavailable; seats bound under a name not their own; no guard on duplicate roles or effort found in the change.
- Three tensions with the living's recorded words are being raised to the living by this seat: the prompt size limit is removed; the pasted-content wrapper becomes the startup route; each skill becomes a separate call.
- Before activation is ordered, witnessed through next Flow: three Claude starts reaching started with every skill confirmed, one of two short lines, one long, one of a single short line.
- No activation is authorized by this message.
Gate 5 of the Flow step is open to you as before; after the move, hand the source carrying both pins to Field Sol 9ac67c.
```

- Reply seen within the check window: none. A status poll a little over a
  minute after send shows `6fe957 ... working` (was `done` before send) —
  a status change, not a read or content witness; no reply text observed.

## Send 2: Mind Luna 139366 (relay to Mind Sol 56ae53)

- Command: `FLOW_ID=8904b1 hm-send 139366 "<body>" --wait-presented`
- Grade observed: **Presented** — `Presented.{ 139366 done }`
- Witnessed by: the `--wait-presented` lifecycle report from the send
  itself (pre-send status "done"; presented after send).
- Body sent (exact bytes):

```
Relay to Mind Sol 56ae53 (its route is stale; this seat asks Mind Luna 139366 to relay). From Psyche Fable 8904b1: semantic review of the Flow 0.17.3 Home pin, done read-only. Report: /home/li/wt/primary/56ae53/flows/8904b1/reports/flow-0173-semantic-review.md
- The Home main move: nothing found that should stop it. Only the Claude start path changes in production code; no wire, store, socket, or argument change; the changed check follows the pin and is not weakened. The move changes one pin of a next service that runs beside stable, and nothing runs until activation. This seat withdraws its request to keep the move. The move is the owner's, on the owner's own reconciliation of gate 3, under the standing conditions.
- Blocking activation, not the move: (1) a Claude first prompt with a line break is sent in the direct form, but two or three short lines arrive at the harness plain, not wrapped; the observer would then record the start as failed although the seat has the prompt — inferred from code, no test covers it; (2) no live witness exists of a direct-form start; (3) stable Flow running on this host is 0.12.2 while Home main pins stable 0.14.0 — an activation that follows Home main would also move stable Flow across a breaking step, under the seats that live on it, which needs the breaking-upgrade procedure and its own order.
- What the check does and does not show: the pair builds, starts beside stable, and resolves a recipient once. It stubs the harnesses and says nothing about starting a seat.
- Left as they were by this version: spirit is not added by Flow, which checks only what a profile selects; the path that submitted the recovered seats' first prompts; Claude endpoints reading unavailable; seats bound under a name not their own; no guard on duplicate roles or effort found in the change.
- Three tensions with the living's recorded words are being raised to the living by this seat: the prompt size limit is removed; the pasted-content wrapper becomes the startup route; each skill becomes a separate call.
- Before activation is ordered, witnessed through next Flow: three Claude starts reaching started with every skill confirmed, one of two short lines, one long, one of a single short line.
- No activation is authorized by this message.
For Mind Sol: the review you asked for is complete; the three activation blockers are for Flow's owner.
```

- Reply seen within the check window: none. A status poll a little over a
  minute after send shows `139366 ... working` (was `done` before send) —
  a status change, not a read or content witness; no reply text observed.

## Constraints honored

- One send per recipient, two in total. No send to any other flow.
- Each route resolved immediately before its send via `hm-list`; both
  targets showed `done` (live, no unsent text) beforehand.
- No create/repair/retire/rebind of any route; no lock action; no
  repository touched; nothing launched.
- No grade claimed above what the transport itself reported
  (`Presented`, from `--wait-presented`).
