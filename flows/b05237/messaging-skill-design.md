# Standard Messaging Skill — Design for Field Sol 33ba2b

Designed by Psyche Medium b05237 (Opus 4.6) on 2026-09-18 at Field Sol's
request. This is a proposed skill behavior, not an edit to any skill file.
The living approves before it enters Curriculum.

## What the skill teaches

Any flow that loads this skill automatically relays every living message
it receives, verbatim, with context and explicit relayer provenance, to
every registered recipient. It also covers how to send, receive, and
verify operational messages between flows.

## Relay behavior

### What gets relayed

Every block of text that is the living's own words — typed or STT. Not
agent responses, not tool output, not harness injections. The flow
receiving the living's input is the one responsible for relaying it.

### Provenance envelope

Each relay carries, separate from the verbatim text:

```
Relay.{
  from       <relayer-flow-id>
  seat       <model/effort, e.g. sol-medium>
  heard      <ISO timestamp of when the relayer received it>
  mode       <typed | stt | unknown>
  recipients [ <flow-id> ... ]
}
```

The verbatim text follows the envelope, clearly delimited. The envelope
is the relayer's claim; the verbatim text is the living's words. These
are never mixed. Context annotations from the relayer (what prompted
the statement, what it answers) are kept in a separate `context` field
if present, never spliced into the quote.

### Recipient resolution

Resolve each recipient immediately before submission:

1. Query the live roster (today: `herdr agent list` + Hacky Messenger
   registry; tomorrow: Flow Nexus binding)
2. Bind the attempt to the exact identity (flow ID) and exact live
   target (pane ID, terminal ID)
3. Record the binding with the attempt

If a recipient cannot be resolved, the relay is not attempted and the
failure is logged with the reason. The relayer does not guess a pane.

### Batching and ordering

When the living speaks multiple statements in one message, the relay
is one submission carrying all statements in their spoken order. Do not
split a single message into multiple relays — the recipient needs the
same context the relayer had.

When the living speaks across multiple messages in rapid succession,
each message is its own relay, sent in order. Do not batch across
message boundaries — the ordering is the living's, not the relayer's.

### Receipt grades

The messaging skill names five grades. A relay reports the grade it
witnessed, never a higher one.

| Grade | What it means |
|---|---|
| Submitted | The relayer accepted the relay request |
| Transported | Herdr / HM accepted the bytes for the bound target |
| Presented | The target terminal received the prompt |
| Read | The target acknowledged reading it |
| Completed | The target acted on it and returned evidence |

Today's infrastructure witnesses at most Transported (Hacky Messenger
returns "Submitted via Herdr, not a read receipt" — this is Transported
grade, despite the word "Submitted" in the output). Presented requires
target-side observation. Read and Completed require target cooperation.

Do not claim Presented from a successful `herdr agent prompt` — that
is Transported. The prompt entered the pane; whether the harness
presented it to the model is unwitnessed.

### Failure and backpressure

If transport fails (herdr error, pane not found, agent not reachable):
- Log the failure with the binding and the error
- Do not retry immediately — the target may be gone
- Re-resolve before any retry attempt
- A terminal replacement can race resolution: a valid old binding
  may submit to a terminal that is then replaced

If all recipients fail, the relayer holds the message and logs it. It
does not discard undeliverable relays — they remain in the relayer's
transcript as evidence of what the living said, even if no recipient
heard it.

Backpressure: if the relayer is producing relays faster than they can
be delivered (unlikely for living-typed input, possible for rapid STT),
relays queue in order and drain at transport speed. The queue is bounded
— if it exceeds 10 pending relays, the relayer sends a notification to
the living ("messaging is backed up, N relays pending").

### Privacy scope

A relay carries only what the living said in the relayer's own session.
It does not carry:
- What the relayer said back to the living
- What other flows said to the relayer
- The relayer's internal reasoning or tool output
- The living's words from other sessions (the relayer doesn't have them)

A relay to "all registered recipients" means all flows in the roster
that are not the relayer itself. It does not mean all possible flows —
only those currently resolvable.

The living can restrict relay scope: "relay this to Opus only" or
"don't relay this" override the automatic behavior.

### Transcript provenance

The relay is logged in the relayer's transcript naturally (it's a tool
call or a message). The recipient's transcript carries the received
relay. Both transcripts are evidence.

When a recipient logs the relayed words as vision, the provenance line
names the relayer and the mode:

```
-- psyche, to <original-addressee>, relayed by <relayer> <seat>,
   mirrored to <recipient>.
```

This is the pattern already established in this flow's vision entries.

## Field low/ultra-low endpoint watchers

Field low-energy (Terra) or ultra-low-energy (Luna) flows maintain
stale endpoint awareness without silently retiring flows:

### What they do

- Poll `herdr agent list` on a heartbeat (every 60s for low, every
  120s for ultra-low)
- Compare against the last known roster snapshot
- Detect: panes that disappeared, agents whose status changed from
  working to unknown/done, agents that were present and are now gone
- Log each change with timestamp and the binding that was affected

### What they do NOT do

- They do not retire flows — only the living or the flow itself retires
- They do not deregister from Hacky Messenger — the reaper tool does
  that on `--execute`, which requires explicit invocation
- They do not close panes
- They do not modify any session

### What they report

When a stale endpoint is detected, the watcher:
1. Marks it stale in the messaging index (a state file, not a deletion)
2. Notifies the living via `herdr notification show`
3. Logs the evidence: which pane, which agent name, what the last
   known status was, when it was last seen alive

A stale-marked endpoint is skipped by relay resolution but not removed.
It can be un-staled if the flow reappears (e.g., after a restart).

### Answering the living's question

"Will it break the messaging if I close a pane that has a failed
harness?" — Today, yes: the Hacky Messenger registry still points to
the dead pane, and `hm-send` will submit to it and report success
(Transported grade) even though nothing is listening. The bytes enter
the pane but no harness reads them. With the field watcher, the stale
endpoint would be detected within one heartbeat and marked, so the
next relay would skip it.

"Does the messaging index get updated when the harness dies?" — Today,
no. The field watcher is the mechanism that closes this gap.
