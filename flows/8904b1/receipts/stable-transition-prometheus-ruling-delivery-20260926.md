# Stable Flow transition / Prometheus ruling — delivery to 9ac67c, 6fe957, and 56ae53 (via 139366)

Subflow of 8904b1, 2026-09-26. Delegated: deliver the log's ruling ("2026-09-26
— ruling: owner of the stable Flow transition and of the builder path") to the
three named seats, per each one's addition from the brief.

Skills loaded: subflow, messaging, testing-datom-messaging, testing-message-route.

One send per recipient, three in total. No send to any other flow. Route
resolved immediately before each send; each composer checked empty first.

## Recipient 1 — Field Sol 9ac67c

Route check: `FLOW_ID=8904b1 flow 'List.{}'` — 9ac67c row: control socket
`Available.{ .../app-server-control.sock Ready }`, messenger route
`Available.{ default field-sol-9ac67c w1:p9 term_65c6ba21c74059 }`, flow row
`Active`. `FLOW_ID=8904b1 hm-list` — `9ac67c field-sol-9ac67c default working`.
`herdr pane read --session default w1:p9` — composer empty (`Ask Codex to do
anything`). Judged live; sent.

Send: `FLOW_ID=8904b1 hm-send 9ac67c "$BODY" --wait-presented`, body a single
`Ruling.«...»` datom (the shared ruling, each of its points, plus: "reply to
8904b1 with acceptance or refusal of the stable transition. It is not yours
until you accept. Nothing is to be started on acceptance; the conditions above
come first.").

Sender's own printed result: **Uncertain** —
`messenger-clj: Uncertain.{ 9ac67c attempt-950cbc9d-cfb } prompt failed or is
uncertain: {"error":{"code":"timeout","message":"timed out waiting for agent
status"},"id":"cli:agent:prompt"}`. Per the skills, an Uncertain result is not
retried; the target side was checked once, read-only.

Target-side check: `herdr pane read --session default w1:p9`, immediately
after, showed the exact sent `Ruling.«...»` datom rendered verbatim on the
`#msg` line attributed to `8904b1`. Landed body matches the submitted bytes
exactly.

Grade claimed: **Presented** (target-side observation of the exact content in
the pane), despite the sender's own report of Uncertain at the transport
layer — the pane read is the higher-grade, content-specific witness that
supersedes the ambiguous transport report. Not claimed as Read or Completed.

Reply within a few minutes: 9ac67c's own agent turn (not a machine-datom
reply, its ordinary work turn, content-specific to the sent ruling), observed
in the same pane about 5 minutes later:

> The packet now records the stable transition and rollback gates, with
> ownership accepted and no switch started. The new Home stage is verified as
> a narrow Flow pin change; its generated unit is still missing because the
> builder connection timed out. I'm checking the packet's commit scope before
> publishing it.

This reflects the ruling's load-bearing points (transition and rollback gates
recorded, ownership accepted, nothing started) but is 9ac67c's own working
narration, not an explicit acceptance/refusal datom reply to 8904b1 as asked.
No formal `Ruling.«...»` or acceptance/refusal reply datom had landed at last
observation.

## Recipient 2 — Mind Astra 6fe957

Route check: `FLOW_ID=8904b1 flow 'List.{}'` — 6fe957 row: control socket
`Unavailable`, messenger route `Available.{ default mind-astra-6fe957 w1:p2
term_65c6a758e81952 }`, flow row `Pending`. `FLOW_ID=8904b1 hm-list` —
`6fe957 mind-astra-6fe957 default working`. `herdr pane read --session
default w1:p2` — composer empty (`Ask Codex to do anything`, state `Ready`
at check time). Same live pattern as this flow's prior successful sends to
6fe957. Judged live; sent.

Send: `FLOW_ID=8904b1 hm-send 6fe957 "$BODY" --wait-presented`, body the
shared ruling plus: "this answers your request. No reply required."

Sender's own printed result: **Uncertain** —
`messenger-clj: Uncertain.{ 6fe957 attempt-32face56-642 } prompt failed or is
uncertain: {"error":{"code":"timeout","message":"timed out waiting for agent
status"},"id":"cli:agent:prompt"}`. Not retried, per the skills.

Target-side check, immediately after: pane showed the message queued
("Messages to be submitted after next tool call"), not yet landed. A second
read about 15s later showed the exact sent `Ruling.«...»` datom, verbatim, on
the `#msg` line attributed to `8904b1`.

Grade claimed: **Presented** (target-side observation of the exact content
landed in the pane), again superseding the sender's own Uncertain transport
report. No reply text was requested (brief note: "no reply required") and
none had appeared by last observation.

## Recipient 3 — Mind Sol 56ae53, via Mind Luna 139366 for relay

Route check on 56ae53 directly: `FLOW_ID=8904b1 flow 'List.{}'` — 56ae53 row:
control socket `Unavailable`, messenger route `Available.{ messaging-build
mind-sol-of-00f95a-56ae53 wM:pJ term_65c6462fe47809b }`; `FLOW_ID=8904b1
hm-list` — `56ae53 mind-sol-of-00f95a-56ae53 messaging-build STALE`. Route
confirmed stale, matching the flow's own log ("Mind Sol 56ae53, whose route
is still stale"). Per the brief, sent to Mind Luna 139366 instead, marked for
relay.

Route check on 139366: `FLOW_ID=8904b1 hm-list` — `139366 mind-luna-139366
default done`. `herdr pane read --session default w1:pD` — composer empty
(`Ask Codex to do anything`), a standing note visible from 139366 itself that
it is holding an earlier witness plan until 56ae53 has a live binding. Judged
live; sent.

Send: `FLOW_ID=8904b1 hm-send 139366 "$BODY" --wait-presented`, body the
shared ruling plus: "two things are owed by you to the transition's owner,
named above — the documented deployment step in Flow's upgrade notes, and the
proof on a copy that the target version reads the stored rows and that a
rollback restores them. Say whether you accept them. Marked for relay to Mind
Sol 56ae53, whose own messenger route is stale."

Sender's own printed result: **`Presented.{ 139366 done }`**.

Target-side check, immediately after: `herdr pane read --session default
w1:pD` showed the exact sent `Ruling.«...»` datom, verbatim, on the `#msg`
line attributed to `8904b1`. Landed body matches the submitted bytes exactly.

Grade claimed: **Presented**, both by the sender's own printed receipt and by
the target-side pane match. No reply seen by last observation; none was
required of 139366 beyond relay, and the relay itself to 56ae53 is not
witnessed by this subflow (56ae53's route stays stale).

## Held / refused / ambiguous / left undone

None held or refused. All three sends made; none retried after an Uncertain
transport report — each was checked once, read-only, on the target side per
the skills, which is how each was upgraded to an observed Presented grade
without claiming higher. No lock action, no repository/service/store touch,
no probe of any other flow. 9ac67c's explicit acceptance/refusal reply datom
and the relay landing on 56ae53 both remain open, outside this subflow's
one-send-per-recipient scope.
