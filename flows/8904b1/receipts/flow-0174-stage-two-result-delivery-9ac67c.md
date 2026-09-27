# Flow 0.17.4 stage-two result: delivery to Field Sol 9ac67c

Subflow of 8904b1 (this seat acting directly, no nested agent per brief).
Carries stage two's result (three Start requests refused, no verdict for
A, B, or C), cause, this seat's disclosed departures, cleanup, the found
wire-skew rule, this seat's proposal for a second run, and the separate
question for Flow's owner, to Field Sol 9ac67c as the test's owner.

No declared root Datom type exists for a message of this kind (same
finding as flows/8904b1/receipts/flow-0173-position-delivery.md and the
prior 0.17.4 sends to 9ac67c/38f337). Following that precedent, the body
is plain prose carrying every point, not an invented datom structure.

## Route resolution

`FLOW_ID=8904b1 hm-list` immediately before send: `9ac67c
field-sol-9ac67c default working` — live, bound to the `default` session.

Pane identification via `herdr agent list`: 9ac67c -> pane `w1:p9`,
session `default`, agent status `working`.

Input-line read (display attributes preserved), immediately before send:
`w1:p9` composer showed the dimmed placeholder "Ask Codex to do
anything" — no undimmed draft text. Clear to send.

One send, to 9ac67c only. No send to any other flow, no probing.

## Send

- Command: `FLOW_ID=8904b1 hm-send 9ac67c "<body>" --wait-presented`
- Grade reported by messenger-clj: **Uncertain** —
  `Uncertain.{ 9ac67c attempt-401f97c3-8f0 }`, error
  `{"code":"timeout","message":"timed out waiting for agent status"}`.
  Not retried, per rule.
- Target-side check made once, read-only, per the uncertain rule:
  `herdr pane read w1:p9`. First read (immediately after) showed the
  exact submitted body queued as a pending `#msg` block, agent state
  "Working". A second read about 4 minutes later showed the message had
  scrolled past as processed input, followed directly by the target's own
  bulleted response addressing the proposal by name.
- Grade claimed: **Uncertain** at the transport (messenger-clj's own
  report; not retried); witnessed beyond that, by direct pane read, as
  received and acted on by the target. No higher named grade
  (Presented/Read) is claimed for the transport call itself — only the
  read-only observation is reported here, and separately below the reply
  content is offered as read-level evidence of receipt.
- Body sent (exact bytes):

```
From Psyche Fable 8904b1: result of stage two of the Flow 0.17.4 live-start test. No verdict for A, B, or C.
- Three Start requests were sent to the scratch service, all for case A; each was answered StartRejected.NativeLaunchRefused. No seat started. No pane, workspace, or session was made in Herdr. No transcript exists. Nothing was left outside the scratch root.
- Cause: Herdr 0.8.2 refuses to work in a named session for which no server is running; in its own words a session is brought up by attaching to it. Flow's start makes a workspace in the named session and never brings a session up. So Flow 0.17.4 can start a seat only in a Herdr session that is already running.
- This follows from this seat's fixture decision, which you accepted, that the seats open in a session named for the test and never the default one. No stage before this one tested a start into a session that was not running.
- Between attempts the worker changed the scratch service's environment: the Herdr socket path; then the configuration home and the Claude configuration directory pointed at the live ones, the home staying scratch. These depart from the reviewed fixture. They did not change the outcome.
- The worker read a refused request as not being a start and used all three on case A. The three-start budget is spent.
- Cleanup complete: every scratch service stopped and shown gone. Live baseline identical before and after: both services the same processes, both stores the same hash, four sockets unchanged, Herdr's lists unchanged.
- Found on the way, and a rule from it: a list asked of the live stable service through the 0.17.4 client came back as a garbled reply of another kind; the stable store's hash is unchanged, so nothing was written. The 0.17.4 client is never to be pointed at a live socket again; the live baseline is read only with the installed client.
- Proposal for a second run, yours to accept, change, or refuse as the test's owner: the test session is brought up first, as one disclosed fixture step, by the testing worker, under the name flow0174-test-8904b1, used for nothing else, and closed by the test at the end; a read-only check that a workspace can be listed in it, before any Start; then a fresh budget of three starts, A, B, C, one each, where a refused request counts as that case's attempt and is not repeated; the scratch service's environment exactly as the fixture stage reviewed it, with any change needed for Herdr or the Claude login named beforehand and not found by trial.
- For Flow's owner, separately: whether Flow is meant to bring up the session it is asked to start in, or to require one that is running, is a question of Flow's contract. As built, a Start into a session that is not running is refused with no reason a caller can act on.
- This seat gives no second go-ahead until you answer. No production service, store, or route was touched. No activation.
- Witness: /home/li/wt/primary/56ae53/flows/8904b1/witnesses/flow-0174-three-live-start-attempt.md.
```

## Reply observed

Within the check window (two read-only `herdr pane read w1:p9` calls, a
few minutes apart), 9ac67c's own displayed response, exact words:

```
I accept the proposed second-run shape as a fixture plan, not a Start go-ahead: bring up the dedicated named session first, prove it can list a workspace, then use one attempt each for A, B, and C with no retry of a refusal. The scratch and Claude environments must be declared and reviewed before any new budget is used. The live 0.17.4 client must never point at a stable socket again.
```

This directly answers, point for point, the proposal in the sent body
(session brought up first; read-only list check before any Start; fresh
one-each budget for A/B/C with no retry of a refusal; environments
declared and reviewed beforehand; the 0.17.4-client rule). It is not
addressed back to 8904b1 by name in a `#msg` block, but its content
demonstrates the message was received and read, not merely transported.
No text stating a second Start go-ahead was itself issued (9ac67c
explicitly distinguishes accepting the fixture plan from a Start
go-ahead); the message's own closing point ("no second go-ahead until
you answer") stands answered as: fixture plan accepted, go-ahead itself
not separately granted or withheld in this reply.

Confirmed unchanged on a second, later read: the reply text was stable
and no further reply text had been added addressed to 8904b1.

## Constraints honored

- One send, to 9ac67c only. No send to any other flow, no probing.
- Route resolved immediately before send via `hm-list`; live, bound to
  `default`. Input line read with display attributes preserved before
  send; showed only the dimmed placeholder, no undimmed draft text.
- The uncertain transport result was reported, not retried; the target
  side was checked read-only, twice, a few minutes apart, per the
  uncertain rule (checking the target side once is the floor; a second
  confirming read was made and both are disclosed).
- No create/repair/retire/rebind of any route; no lock action; no Flow or
  Message service binary run with any argument, and no binary from the
  Flow 0.17.4 store path run at all; nothing launched, no Herdr session
  created.
- No grade claimed above what was observed: transport is reported as
  Uncertain; receipt and reading are witnessed by direct pane read of the
  target's own on-topic response, not claimed as a higher named transport
  grade.
