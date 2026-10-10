# Gate 5 lock-refusal findings delivered to Mind Astra 6fe957

Subflow of 8904b1, delegated: deliver the findings and decisions in
`receipts/gate5-lock1805-duplicate-name-witness.md` to Mind Astra 6fe957,
who is blocked on Home main move (gate 5) by an Orchestrate `DuplicateName`
lock refusal. No lock action, no probe, no repository touch by this
subflow.

## Route check immediately before send

`FLOW_ID=8904b1 flow 'List.{}'` — 6fe957's row:
`{ 6fe957 01a0dfdc-a500-7271-8f54-e446fe9578dd Codex Unavailable
Available.{ default mind-astra-6fe957 w1:p2 term_65c6a758e81952 }
{ 56ae53 default meta-bind-existing } Pending }` — control socket
Unavailable, messenger route Available in the `default` session, same
pattern as this flow's earlier successful sends to 6fe957.

`FLOW_ID=8904b1 hm-list` — `6fe957  mind-astra-6fe957  default  done`.

Judged live. One send made, to 6fe957 only. No other flow contacted.

## Send

```
FLOW_ID=8904b1 hm-send 6fe957 "Ruling.«From Psyche Fable 8904b1, on your gate 5 lock refusal.

Witnessed, read-only: the existing lock the refusal points at is named, literally, the word Name. It is held by cf7879 over paths and for a reason unrelated to Home or the messenger. cf7879 has no messenger binding and no live pane. The lock service requires a lock's name to be unique across all locks by exact equality, whatever the holder or paths.

This flow's inference, not witnessed: the service read your requested name as the word Name as well, so a field's label went where its value belongs. Your exact request as submitted was not recovered, so check it against the lock request's type before resubmitting.

What clears the block is your own act: resubmit with a distinct real name for the lock. No stale-lock release is needed for the Home move, and none is authorized by this message. Leave the old lock as it is.

Gate 5 stays open to you under the standing ruling and conditions: fast-forward only, stop and report if Home main has moved, show the revision on the real remote, then hand the source to Field Sol 9ac67c. No activation.

Report the lock service's exact answer and the move, or the next blocker.

Full witness: /home/li/wt/primary/56ae53/flows/8904b1/receipts/gate5-lock1805-duplicate-name-witness.md»" --wait-presented
```

Receipt printed: `Presented.{ 6fe957 done }`.

## Landed-body check

`herdr pane read --session default w1:p2` immediately after the send showed
the exact sent `Ruling.«...»` datom, verbatim, on the `#msg` line attributed
to `8904b1`. Landed body matches the submitted bytes exactly — no
truncation, no mangling.

## Reply observed

Within under a minute, 6fe957's pane showed (its own words, via the
Herdr-visible agent turn, not a machine-datom reply):

> I'll have the worker recover the submitted lock request and check it
> against the actual request type before resubmitting with a distinct
> name. The unrelated lock will remain untouched. After acquiring the
> lock, it must recheck remote main before the fast-forward.

This is a Read-grade witness (pane-observed, content-specific: it restates
the exact resubmission plan and leaves cf7879's lock untouched, matching
the ruling). The turn was still `Working` when last observed; no further
machine-datom report (e.g. a fresh `LockResult` or `Gate5` outcome) had
landed yet.

## Grades, exact

- Submitted: accepted by `hm-send`.
- Transported: implied by `Presented.{ 6fe957 done }` (Herdr accepted for
  the checked binding).
- Presented: confirmed by the printed receipt `Presented.{ 6fe957 done }`.
- Read: confirmed by the pane-observed reply text above, specific to this
  message's content.
- Completed: not yet — 6fe957's own resubmission and main-move work were
  still in progress at last observation.
