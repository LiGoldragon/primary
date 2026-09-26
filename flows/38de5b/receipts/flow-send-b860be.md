# Flow 0.12.2: Send to b860be held, because its pane was gone

An Opus subflow of 38de5b did this on 2026-09-26 at about 15:30Z. **No Send was made.** Nothing was typed into any pane.

## Validation

- The contract came from a fresh clone of flow at `34aaf7875af11cb539218c61cf2fc51996db271b` (0.12.2, the live `/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow`). Its `Cargo.lock` pins signal-flow 5.1.0 at `74a47edc39a94e39cfbe7f4619340f257b11cecd`, which was also cloned fresh.
- Validation used a scratch test in that clone, which was not committed. It ran `Potential::<Query>::from(text).actualize`.
- **The brief's literal datom does not parse.** It has no closing `»` before ` }`. The error was `Error { layer: Protos, path: [], kind: Structural(Error { extent: Extent { start: 14, end: 566 }, problem: Unclosed('«') }) }`.
- **The corrected datom validates.** I added `»` before ` }`, which is the shape in `flow-first-send.md`. It parses as `Query::Send` with flow_id `b860be`, its bare_input equals the brief's body byte for byte, and it round-trips to identical text. 1 passed.

## Why no Send was made

The brief's premise was that b860be is Active with a live Herdr pane, w1A:p1. Just before the send, at 15:30:41Z and 15:30:52Z, that premise was false:

- `flow 'ResolveRecipient.b860be'` →
  ```
  RecipientResolved.{ b860be b860be42-d89d-4eee-a0c2-216ec0107a86 Claude Unavailable Unavailable { e167d8 e167d857-17e7-441b-b38b-54941a77a77a fable-successor-of-da88cf } Active }
  ```
  The Herdr route came back `Unavailable`. The stored route in `flow 'List.{}'` is still `Available.{ messaging-build claude-bccd531237a4454d86f45447 w1A:p1 term_65c5d073c6e318f }`, so the refresh found the pane gone.
- `herdr --session <s> agent get w1A:p1` returned `agent_not_found` in all three sessions: default, fms-9bc4f7 and messaging-build.
- `agent list` in all three sessions showed no pane w1A:p1, no terminal `term_65c5d073c6e318f`, and no agent whose session is `b860be42-…`.
- `ps` showed no process carrying `b860be42`.

What this means:

- Field Monitor 98eb43's 15:27Z call that b860be is dead matches what I observed.
- The body tells b860be "you are alive (this pane)", and that is now false.
- A Send would at best be refused with `RouteUnavailable`, and it would spend the one attempt.

So the Send was held and the decision goes back to 38de5b.

## Held datom (validated, not sent)

```
Send.{ b860be «#msg ["38de5b" "From 38de5b (crossover), through Flow Send because hm-send to you is Held RepairRequired with no candidates — your messenger route is broken and every flow's messages to you are being held; rebind it (hm-rebind/hm-register per the compensation skill) or route replies through Flow. Also: Field Monitor 98eb43 called you, 00f95a and 88475f dead at 15:27Z; you are alive (this pane), but 00f95a's and 88475f's panes are absent — the Psyche Opus seat is empty and Flow still lists 88475f Active until a Stop or Replace clears it."]» }
```

## Reply grade

None. No Send was made, so there is no reply.

## Also observed

- Flow still lists b860be as `Active`, even though its pane is gone.
- 88475f is also still listed as `Active`, with stored pane w17:p1, and w17:p1 is absent from Herdr's agent list.
- e167d8 (w19:p1) is working, and da88cf (w18:p1) is idle.
