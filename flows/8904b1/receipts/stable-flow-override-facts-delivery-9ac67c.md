# Stable Flow override and clients facts: delivery to Field Sol 9ac67c

Subflow of 8904b1 (this seat acting directly, no nested agent per brief).
Carries a read-only companion's findings on the drop-in override and
Flow clients — the evidence for 9ac67c's chosen route, a withdrawn
hazard, the real hazard this flow itself caused, and a post-switch
consideration — plus the absolute location of the saved report, to
Field Sol 9ac67c as owner of the override, the activation's proof, and
the stable transition.

## Route resolution

`FLOW_ID=8904b1 hm-list` immediately before send: `9ac67c
field-sol-9ac67c default working` — live, bound to the `default`
session.

Pane identification via `herdr agent list`: 9ac67c -> pane `w1:p9`,
session `default`, agent_status `working`, interactive_ready `true`.

Input-line read (display attributes preserved), immediately before
send: `herdr pane read w1:p9 --source visible --format ansi` showed
the composer with only the dimmed (`\x1b[2m`) placeholder "Ask Codex
to do anything" — no undimmed draft text. Clear to send.

One send, to 9ac67c only. No send to any other flow, no probing.

## Send

- Command: `FLOW_ID=8904b1 hm-send 9ac67c "<body>" --wait-presented`
- Grade reported by messenger-clj: **Uncertain** —
  `Uncertain.{ 9ac67c attempt-3ae25ec7-775 }`, error
  `{"code":"timeout","message":"timed out waiting for agent status"}`.
  Not retried, per rule.
- Target-side check made once, read-only, per the uncertain rule:
  `herdr pane read w1:p9 --source visible --format ansi`. That single
  read showed the exact submitted body as processed input in the
  pane's scrollback, followed directly by the target's own bulleted
  response addressing the content by name (the Form-1 route, the
  unmanaged override, the undeclared profile entry, next-generation
  clients kept off the stable socket).
- Grade claimed: **Uncertain** at the transport (messenger-clj's own
  report; not retried). Witnessed beyond that, by the one read-only
  pane read, as received and acted on by the target. No higher named
  transport grade (Presented/Read) is claimed; the reply content below
  is offered separately as read-level evidence of receipt.
- Body sent (exact bytes):

```
From Psyche Fable 8904b1: facts established read-only that bear on the route you chose, and a hazard.
- Evidence for your first gate. The running stable service's command and the drop-in's command are the same 0.12.2 executable. The drop-in is an ordinary unmanaged file. The live generation's own stable unit says 0.14.0 and carries no drop-in directory, so the drop-in is what keeps stable at 0.12.2 today. The drop-in has already come through three activations of generations whose stable unit said 0.14.0, on 2026-09-26 at 09:24, 17:17, and 17:38 local; the first stopped and started the stable service with the drop-in in place. The activation's cleanup removes only links into an earlier generation, and its collision check looks only at declared targets. Neither the live nor the candidate generation links anything into the drop-in's directory. These are this flow's observations; your own proof stands on its own witness.
- A second undeclared artifact that stable depends on. Both generations put the 0.14.0 Flow clients on the path. What runs is 0.12.2, because an undeclared entry in the user's profile outranks the generation's. Your baseline should hold that entry beside the drop-in, and your rollback should restore it if it is disturbed.
- Correction of this seat. It raised to Mind Sol 56ae53 a hazard of a 0.14.0 client speaking to the 0.12.2 service. That is not happening, for the reason above, and the ordinary request vocabulary is the same in both versions. It is withdrawn as a condition.
- The hazard that is real. The 0.17 line removed one request from the ordinary vocabulary, so every later request is numbered one lower. A list sent by a 0.17 client to the 0.12.2 stable service is read by it as a stop. This flow's stage-two worker did that twice while taking its baseline. Witnessed afterwards: the stable store's hash unchanged, the stable service the same process with no restart, Herdr's sessions and agents unchanged; so no row changed and no seat stopped. It is this flow's act and is recorded as such.
- What follows for activation, for you to weigh as owner: after the switch two lines of clients exist on this host, the stable ones and the next ones. Any next client pointed at the stable socket can stop a flow while meaning to list. Your post-switch checks and the notice to the seats should say which client speaks to which socket, and that the next client is never given the stable socket.
- This seat's design of moving Home's stable pin back to 0.12.2 stays on record as a design. It does not contest your choice, which the evidence supports.
- The findings in full: /home/li/wt/primary/56ae53/flows/8904b1/reports/stable-flow-override-and-clients-facts.md.
- No reply is required. No activation.
```

## Reply observed

Within the single read-only check, 9ac67c's own displayed response,
exact words:

```
Fable's read-only witness strengthens the Form-1 route: the unmanaged stable override survived three prior activations, including a stable service restart. It also found an undeclared profile entry that keeps the stable client aligned with the stable service. I'm adding that entry to the baseline and rollback scope, and keeping next-generation clients away from the stable socket.
```

This directly addresses the sent body's first two points (the override
evidence, the undeclared profile entry) and states an action taken
(adding the entry to baseline/rollback scope, keeping next-generation
clients off the stable socket) that matches the "What follows for
activation" point. It does not restate every point (e.g. the withdrawn
hazard, the 0.17 List/Stop hazard, or the design-on-record note) and is
not addressed back to 8904b1 by name in a `#msg` block, but its content
demonstrates the message was received and read, not merely
transported.

## Constraints honored

- One send, to 9ac67c only. No send to any other flow, no probing.
- Route resolved immediately before send via `hm-list`; live, bound to
  `default`. Input line read with display attributes preserved before
  send; showed only the dimmed placeholder, no undimmed draft text.
- The uncertain transport result was reported, not retried; the target
  side was checked read-only, once, per the uncertain rule.
- No create/repair/retire/rebind of any route; no lock action; no Flow
  or Message service binary run with any argument, and no binary from
  any Flow 0.17 store path run at all; nothing launched.
- No grade claimed above what was observed: transport is reported as
  Uncertain; receipt and reading are witnessed by the one direct pane
  read of the target's own on-topic response, not claimed as a higher
  named transport grade.
