# Registry-repair designation to Field Luna 184bd8, and reply to c56100

Subflow of 8904b1, dispatched to deliver the designation ruled in log.md
("owner asked for the messenger registry repair, by c56100") and the reply
answering c56100's request. Two sends made, one per recipient, no others.

## Pre-send registry readback (immediately before sending)

`FLOW_ID=8904b1 hm-list`:

```
FLOW    AGENT              SESSION           STATE
184bd8  field-luna-184bd8  default           done
c56100  mind_sol_c56100    recovery-56ae53   idle
56ae53  mind-sol-of-00f95a-56ae53  messaging-build  STALE
```

Both target rows: not STALE, bound to a session `herdr session list` shows
`running` (`default`, `recovery-56ae53`). `herdr agent list --session default`
confirmed 184bd8's binding names a live pane, `w1:p7` (agent name
`field-luna-184bd8`, terminal `term_65c6b830d861b7`, `agent_status: done`).
c56100's binding names live pane `w1:p3` in session `recovery-56ae53` (agent
`mind_sol_c56100`, `agent_status: idle`). Both qualify: live, bound to a
running session.

## Input-line check before send (untested-route caution for 184bd8)

`herdr pane read w1:p7 --source visible --format ansi`: input line showed
`Ask Codex to do anything`, entirely under a dim (`\x1b[2m`) SGR attribute —
a placeholder, not undimmed draft text. Status line read `Ready`. Send not
blocked.

`herdr pane read w1:p3 --session recovery-56ae53 --source visible --format
ansi`: input line showed `Ask Codex to do anyth`, also dim — a placeholder.
Send not blocked.

## Sends (one per recipient, two total)

1. `FLOW_ID=8904b1 hm-send 184bd8 "<body>" --wait-presented`
   Body: the designation text exactly as given in this seat's brief, in full
   (ground, scope, how, excluded, adjacent points), positional argument.
   Result: `Presented.{ 184bd8 done }`.

2. `FLOW_ID=8904b1 hm-send c56100 "<body>" --wait-presented`
   Body: the reply exactly as given in this seat's brief — one datom line
   (`Designated.{ FieldLuna.184bd8 «...» }`) followed by the six points,
   positional argument.
   Result: `Presented.{ c56100 idle }`.

No higher grade is claimed for either. Neither is a read acknowledgment by
itself; both are corroborated below by target-pane observation.

## Target-side observation after send

Pane `w1:p7` (Field Luna 184bd8), read after her agent finished working:
her own final response reads, in full:
"I accept ownership within the stated scope; the acceptance message is
being sent to current Fable 8904b1. No registry change is authorized or
made."
Immediately before that, her own log line: "I'll record the designation and
accept ownership within its stated limits. I'll send that acceptance only
to the current Fable flow; the designation itself authorizes no registry
change." She invoked a local action named `/root/accept_registry_repair`;
the exact bytes of the message that action sent to 8904b1 are not visible
in the pane transcript (the tool's own send call is collapsed in her
harness's display) and are not witnessed here — this subflow cannot read
8904b1's own inbox. So: her acceptance is witnessed by pane read, in the
words above; whether/what exact-text message has separately landed in
8904b1's own prompt is for the main flow to confirm when it resumes. No
registry mutation was made by her, by her own words, and the post-send
registry readback (above) still shows her row unchanged (`done`, `default`).

Pane `w1:p3` (c56100), read after its agent went idle: the visible
scrollback is limited to a 9-row viewport with no retrievable scrollback
beyond it (`max_offset_from_bottom: 0`); the only content visible is the
tail of a structured response, `[] }`, consistent with a completed
datom-shaped reply, and the idle prompt. The fuller text of any reply is
not recoverable from this pane by this subflow. Landing of the sent body
is corroborated only by the `Presented` grade and the agent's transition
from `working` back to `idle` immediately after the send.

## Registry state, unchanged

Post-send `hm-list` for both rows matches pre-send: 184bd8 `done`/`default`,
c56100 `idle`/`recovery-56ae53`, 56ae53 still `STALE`/`messaging-build`. No
registry mutation, retire, rebind, or lock action was taken by this
subflow.
