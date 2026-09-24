# Messaging and the Nexus

## Page 1 · Flowchart — How a message travels today

**What this flowchart shows:** the send path in use now, and where the new services sit beside it.

- "Sending flow" → `hm-send <flow> "text"` (one call) → "check: is the pane there, is it the same harness and session, is it ready?"
  - yes → "typed into the flow's pane" → grade "Transported".
  - no, or the flow is being replaced → "held a few seconds for a declared successor" → either "sent once to the successor", or "Held: nothing typed" (no retry, no reroute).
- Alongside, in grey: "Flow (identity) — live, fresh store" and "Message (durable inbox) — live, fresh store". An arrow between them is dashed and labelled "not connected to real flows yet: binding pending".

## Page 2 · What you said

> You can just make a single CLI call and send a message. If there is a match for what you want and the pain still exists, then it just sends the message.

-- living, typed, 2026-09-23, to d8df70. ("pain" is read as "pane".)

> If there's no registry or if the registry says "in transition" or something, then the message can sort of be held ... We can wait a few seconds at least to see if there's a new flow.

-- living, 2026-09-23, to d8df70.

> If a message can't be delivered, then we try a higher power. ... If there's nothing higher then we try lower. ... Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.

-- living, 2026-09-24, comment on "What Waits for the Living".

## Page 3 · Flowchart — Where the Nexus services stand

**What this flowchart shows:** each service from source to live, as a row of stations with a marker where it stands.

- Stations: "source" → "tested" → "built" → "deployed" → "bound to live flows" → "delivering".
- "Flow": its marker is at "deployed" (live since 15:35, 09-24). The next station, "bound to live flows", is marked "meta socket: bind the Herdr session and its flows, by hand now, with an import tool later".
- "Message": its marker is at "deployed" (live since 15:47 on a fresh store). One test message was accepted into an inbox; that isn't delivery to a flow.
- "hm-send (the bridge)": its marker is at "delivering". It's in use.

*(Deploy facts relayed from Field eb7bae; not re-witnessed by this flow.)*

## Page 4 · Rules in force

- Every send is one call; the check runs inside it.
- The receipt grade is never upgraded. "Transported" means Herdr accepted the text. It doesn't mean the flow read it.
- A held message is never retried or rerouted.
- No hashes or long IDs in messages. Exact values go in receipt files.
- Session hooks register a flow at start. The process ending is the signal to unregister it.
- `/clear` isn't supported for now.

## Page 5 · Flowchart — Your escalation rule, as designed

**What this flowchart shows:** what happens to a message that can't be delivered, per your 09-24 words. It's being coded; it isn't live.

- "Message for Psyche Medium" → "delivered?" → yes → done.
- no → "try Psyche High" → delivered? → done.
- no, and nothing higher → "try lower".
- A side branch: "the target is missing and crucial (all Medium and High are crucial)" → "start the flow" → deliver.
- The result goes back to the caller: "what happened".

## Page 6 · Still open

- Binding the live flows into Flow through the meta socket. Field and Mind own it; its current state is in the overview.
- The escalation rule and the lifecycle answers are being coded as the next Flow and Message deploy.

## Page 7 · Proposals

1. ☐ Bind the live Herdr session as a flow container, with its typed flows, by hand, so that Message can deliver to real flows.
2. ☐ Then move hm-send's checks onto Flow and Message, and retire the bridge.
