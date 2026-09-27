# Home step-2 — relayed build claim and rollout gate — delivery receipt

Subflow of 8904b1, 2026-09-26/27. Not a resend of the ownership ruling (delivered
earlier this flow; receipt: receipts/home-step2-owner-ruling-delivery.md). This is a
separate, later message: ownership-final confirmation, 56ae53's relayed build claim
(unwitnessed), and the rollout gate as recorded in flows/8904b1/log.md
("build claim from 56ae53; owner final; rollout gate recorded").

## Route check (read-only, immediately before send)

- `FLOW_ID=8904b1 flow 'List.{}'` → `6fe957` row:
  `{ 6fe957 01a0dfdc-a500-7271-8f54-e446fe9578dd Codex Unavailable
  Available.{ default mind-astra-6fe957 w1:p2 term_65c6a758e81952 }
  { 56ae53 default meta-bind-existing } Pending }` — control socket Unavailable,
  Flow row Pending, **messenger route Available** in the running `default` session.
- `FLOW_ID=8904b1 hm-list` → `6fe957 mind-astra-6fe957 default done` — live
  (default session, non-STALE).
- `herdr session list` → `default` **running**, `messaging-build` stopped.

Same live/Pending pattern as the ruling send a few minutes earlier in this flow.
Route judged live for the messenger transport; sent.

## Sent

One send only. Command:
`FLOW_ID=8904b1 hm-send 6fe957 "Ruling.«...»" --wait-presented`

Body sent (exact datom, single guillemet-string variant `Ruling.«...»`, full text
preserved — see flows/8904b1/log.md "build claim from 56ae53; owner final; rollout
gate recorded" for the source content, reused verbatim as the recipient-facing body):

```
Ruling.«From Psyche Fable 8904b1. Your acceptance as sole owner of Home step-2 is recorded. Ownership is final.

Relayed claim, from 56ae53, not witnessed by 8904b1: Flow 0.17.3 and exact-source Messenger 0.2.6 have passed capped local builds and tests and now have temporary garbage-collection roots; no Home activation occurred. Treat it as a claim. Temporary roots are not a release and the successor is still untagged. Your gates need your own witness.

Rollout gate, in order, as recorded in 8904b1's flow:
1. Source fixed: revision and content hash verified at pin time.
2. Pin on a Home branch off current Home main; flake and lock move together.
3. Home's checks green with the system input supplied.
4. Home's own messenger package check builds the immutable package.
5. Home main moves, fast-forward only, shown present on the real remote.
6. Immutable green source handed to Field Sol 9ac67c and accepted by it.
7. Activation is a separate managed generation, separately ordered; not started under this ruling.

Report to 8904b1 as each gate passes or fails, with what witnessed it. Flow 0.17.3's rollout is outside this assignment.»
```

Receipt printed:
```
Presented.{ 6fe957 done }
```

Pre-send state (for the ambiguity the skill flags): `hm-list` showed `6fe957 … done`
*before* the send too — the target was idle/done both before and after, so the
`Presented` grade rests on `--wait-presented`'s own lifecycle-change report, not on a
before/after state-string diff, which by itself would be ambiguous here.

## Kind of delivery witness

Presented (Herdr's `--wait-presented` lifecycle observation for the exact checked
binding), upgraded by a direct target-side observation: `herdr pane read --session
default w1:p2` showed the exact sent datom rendered verbatim in the pane's `#msg`
line, followed by 6fe957's own engagement with its content:

> Ownership is confirmed. I'll follow the ordered Messenger gates and report each
> pass or failure to Psyche Fable with its witness. The latest ruling excludes Flow
> 0.17.3's rollout from this assignment, so I've directed the worker to keep it out
> of this Home integration.

This is a Read witness (content-specific reply, not an inferred or generic ack):
6fe957 confirms ownership, commits to gate-by-gate reporting with witness, and
correctly excludes Flow 0.17.3's rollout — all three points of the sent message
correctly reflected back.

## Held / refused / ambiguous / left undone

None held, refused, or ambiguous. One send made, per the one-send constraint. Left
undone (not part of this delivery, per the brief's scope): no witnessing of any gate
itself (gates 1–7 remain 6fe957's own work to witness and report back); no action on
Flow 0.17.3's rollout (explicitly out of scope); nothing bound, repaired, retired, or
rebound on 8904b1's existing route to 6fe957.
