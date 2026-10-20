<!-- to-the-living:start -->
Presentation.{ «Flow in production: report» }

# Flow in production: report

Flow now runs in production, in its 0.35 line. Every claim below is Field's, from its own witnessed runs today; nothing here was tested by the main flow itself.

## What works, as Field witnessed it

A Codex flow started in production with every one of its startup modules arriving whole and once. Its title and its session were the ones Flow had recorded for it.

That Codex flow sent a message on its very first turn. The message reached the recipient's queue once, attributed to the flow that sent it.

A sleeping Claude flow was woken by that message. It woke as a fresh session, not a resumed old one, with every module whole and once and with the sender named on its task. It ran on the intended model and effort, answered as asked, and used no tools. Flow then put it back to sleep with an empty queue.

A restart cleaned up only what it should. When the finished Codex flow was stopped, its own window and process went away and its flow went to sleep. All other open connections, twenty-four of them, were left untouched.

Records came through each move intact. Before each change, Field closed the stores, backed them up, and checked a copy: every table kept its count and nothing was set aside. Records written after the services came back were kept, and nothing was rolled back over them.

## Limits

| Limit | Where it stands |
| --- | --- |
| Exactly-once delivery | Not proven. The wake test delivered one harmless message twice, by choice. |
| A crash in the middle of a launch | Tested only in a scratch setup, never in production. |
| Two side branches | Left out of production: the model-name check and the window-event recovery. |
| Harness extras | Some remain: a plugin suggestion Codex cannot switch off, and a title suffix. |

Three further gaps stay open. A startup too large for one message has not been witnessed. Older senders are not all brought under the new attribution. And a message being attributed to a flow does not prove who on the machine started that flow.

## Remaining work and who carries it

Flow's owner carries the code: the crash-mid-launch recovery, the two side branches, the oversized startup, older senders, and the harness extras. Field carries the witness: each of these needs its own production run before it counts as done. The main flow carries the reports between them and to you.

## Production is not the whole design

Working in production is not the same as the whole approved design being built. What runs today is the part that launches, names, wakes, messages and cleans up flows, witnessed one case at a time. The rest of the approved design is still ahead.
<!-- to-the-living:end -->
