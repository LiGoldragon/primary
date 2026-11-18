# Proposal 2 native matrix — proposed sequential schedule

Field executes only after green exact whole gate, reviewed bootstrap and native
resource admission. The selected binary, private place/functions, addresses and
retained evidence root are those in `bootstrap.md`. This is a proposed20-minute
wall budget, two Luna flows, at most12 instructed turns per address, no automatic
retry. If these limits cannot complete the proof, stop and report the unfinished
case rather than silently extending them. Core must accept this budget first.

## Observation before stimulus

Start a supported `pflow 'ObserveSends.None'` subscriber before matrix sends,
with its stdout retained as evidence/sends.datom. Its PID is owned and recorded;
stop only it at cleanup. Each source request receipt supplies its RequestId.
Use `pmeta 'DebugDelivery.<id>'` at the named cuts to record actual delivered/read
status. A returned Sent/placed/native submission is not a transcript read proof.
Capture only private transcripts and first prompts; retain native tool arguments,
results and the recipient's reply naming the marker and id as the consumption
witness. Neither a request id nor a successor FlowId is invented in this packet.
`<id>` below is substituted only from the immediately named captured receipt.

The two Launch commands in bootstrap use Predecessors.0. Only the explicit
successor refresh changes that native identity. Confirm both initial native
turns ended using Observe.TurnEnds or the actual Herdr state before stimuli.

## Phase A: each request and answer admission

One operator Question to sender instructs this exact bounded work, in order;
its Result closes the operator instruction after the sender returns receipts:

1. Through the actual native `send` tool send to Mind/proposalTwoReceiver/Luna,
   priority Soft, kind Order, body `P2-order-before: record this marker and its
   request id; give no Result.` Record **O**.
2. Native send, same target/priority, Question body `P2-question-before: keep
   unanswered until explicitly authorized in phase A.` Record **Q**.
3. From the sender's native terminal tool invoke the absolute candidate CLI,
   with explicit private XDG_CONFIG_HOME, not a production wrapper:
   `flow 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Task.{ 15 «P2-task-before: hold until phase A authorization.» } }'`.
   Record **T**. The launch's private environment applies; Field records actual
   process/address association, not an operator-shell send mislabelled native.
4. Native send Notice body `P2-notice-before: record marker; no answer.` Record
   **N**.
5. Same private native terminal CLI:
   `flow 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Living.{ «Proposal 2 isolated matrix» «P2-living-before: record this statement.» } }'`.
   Record **L**. This released contract has two Living fields; the future
   Reading contract is outside this release.

The native send JSON shape is exactly the source declaration: target object
`{"aspect":"Mind","topic":"proposalTwoReceiver","model":"Luna"}`,
`priority:"Soft"`, `kind`, `body`; `request` exists exactly for Result.
Task/Done/Living are not added to this tool.

After recipient consumption evidence for O/Q/T/N/L, send an operator Question
to receiver instructing this order and asking it to return all observed outcomes:

- Native Result naming **O**: expect typed Unresolved; no routed or kept answer.
- Native Result naming **T**: expect Unresolved (wrong kind).
- Candidate ordinary CLI Done naming **Q**: expect Unresolved (wrong kind).
- Native Result naming **Q**, unique body `P2-result-before`: admitted and
  routed to the original sender, which acknowledges reading this marker.
- Candidate CLI `Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ <T> «P2-done-before» } }`:
  admitted and delivered to the original sender, which acknowledges it.
- Repeat Result(Q) and Done(T) as new native calls: each Unresolved. These are
  new calls, not a native call-id replay falsely presented as duplicate admission.

This covers Order, Question, Task, Result, Done, Notice and Living without new
types. Keep the command-Question id distinct from O/Q/T and close it by Result
only after its assigned actions; report the control request separately.

For kept-answer coverage, an unbound private operator `pflow Send.Question`
to receiver supplies **K**. Receiver's native Result(K) must be kept; the same
unbound operator's `pflow 'Answer.<K>'` must return Answered carrying its exact
body and sender. Answer(O) is not used as an obligation oracle: its historical
Open-bit behavior is the explicitly accepted exception.

## Phase B: successor carry

Ask the same native sender to send three new marked requests to receiver,
with the same routes as phase A and no replies yet:
- Order `P2-order-carry-excluded-7a97`: **O2**.
- Question `P2-question-carry-required-7a97`: **Q2**.
- Task,15minutes, `P2-task-carry-required-7a97`: **T2**.

Record all IDs and the actual Task deadline from admitted evidence; keep it
well inside the15-minute interval. Receiver acknowledges that it has read each,
without answering Q2/T2. Use a Notice for any operator marker that requires no
open control request. Finish/close any control Question before refreshing.

Record `pflow 'Current.{ Mind proposalTwoReceiver Luna }'` and private
`pmeta 'Inspect.{ Mind proposalTwoReceiver Luna }'`. Then exactly once:

```datom
Refresh.{ Mind proposalTwoReceiver Luna }
```

Observe the successor event; a RefreshQueued receipt is not a successor. Record
new FlowId/native session, actual first prompt/transcript and the old identity's
closure. First prompt must contain Q2 and T2 with **original** IDs and deadline,
and contain neither O2 nor marker `P2-order-carry-excluded-7a97`. Native source
fixtures cover both harness compositions; this isolated native matrix proves
this actual Codex path only, not a Claude native execution.

Ask successor (one bounded Question) to report the carried IDs without
answering them, then authorize Result(Q2) and Done(T2). Original sender must
receive them; duplicate new-call replies refuse. Result(O2) remains Unresolved
after refresh. Existing delivery/history ids remain available; no ID is
repurposed or migration history rewritten.

## Verdict and cleanup

Record each outcome separately as PASS/FAIL/UNOBSERVED, including source/native
harness boundary. Stop immediately on wrong identity, production route/home,
unknown receipt or deadline overrun. No retry or production intervention. Keep
all private marker/id bindings and first-prompt evidence in the final packet.
Field cleans up exactly the synthetic sessions/processes as bootstrap specifies.
One nonwriter audits final candidate plus wholegate/native evidence against
Overrides.2 before Psyche acceptance, merge or switch. Task a8fa remains open.
