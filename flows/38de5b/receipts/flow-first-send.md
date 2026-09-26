# Flow 0.12.1: the first real Send (38de5b → 88475f)

An Opus subflow of 38de5b did this on 2026-09-25 (local; 2026-09-26 UTC). One Send, no retry, nothing else sent.

## Method

- The type came from a fresh GitHub clone of flow at `fe709c7e20efc2dc5f4c7bac5969f3be57c610b4` (0.12.1). Its workspace pins signal-flow `74a47edc39a94e39cfbe7f4619340f257b11cecd` (5.1.0), which was also cloned fresh. In that contract: `Send.SendRequest`, `SendRequest.{ FlowId BareInput }`, `SendOutcome.[ Accepted.FlowId Presented.PresentationReceipt Uncertain.FlowId ]`, `SendRejection.[ UnknownFlow FlowStopped RouteUnavailable NotDelivered PersistenceRefused ]`.
- Validation: a scratch test in the signal-flow clone, which was not committed. It ran `Potential::<Query>::from(text).actualize` on the datom. It checked that the result is `Query::Send` with flow_id `88475f`, that bare_input equals the brief's body byte for byte, and that the datom round-trips to identical text. 1 passed.
- Before the send: `herdr --session messaging-build agent get w17:p1` showed `agent_status: done`, `interactive_ready: true`, name `psyche-opus-88475f` and terminal `term_65c5883e612c88a`. In `flow 'List.{}'`, 88475f was Active.

## The datom sent (verbatim, one `flow` call)

```
Send.{ 88475f «#msg ["38de5b" "From 38de5b through Flow 0.12.1 Send, the first real one: you are Active in Flow's registry; the Codex flows still resolve Pending pending 0.12.2. Reply to me through hm-send with one line: what arrived in your pane and how it looked."]» }
```

## The reply (verbatim)

```
Sent.Presented.{ 88475f w17:p1 1790390569525 }
```

- Exit 0. The call started at 2026-09-26T02:42:48.995Z and returned at 02:42:49.540Z.
- The grade is **Presented**: Flow observed a reaction on the exact pane w17:p1, at 1790390569525 ms. This is not a read. The read witness is the reply from 88475f.

## Pane observation (`herdr --session messaging-build agent read w17:p1`, read-only)

- The body arrived as one plain prompt line, exactly the BareInput, with no `pasted_content` wrapper and no appended marker. It was soft-wrapped only by pane width:

  ```
  ❯ #msg ["38de5b" "From 38de5b through Flow 0.12.1 Send, the first real one: you are Active in Flow's registry; the Codex flows still resolve Pending pending 0.12.2. Reply to me through hm-send
    with one line: what arrived in your pane and how it looked."]
  ```

- Immediately after, the pane showed `Running 1 shell command…`, and its status turned to `working`.
- A second read showed 88475f's own log line 75: "arrived as one plain-text line, #msg ["38de5b" "..."] envelope, not wrapped as pasted content. Replying via hm-send." It had backgrounded a `write-trivial(Reply to Fable on Flow Send)` agent.
- The reply through hm-send goes to 38de5b's own pane, not to this subflow. This subflow did not observe it arriving.

## Flow state after (`flow 'List.{}'`)

```
{ 88475f 88475fd7-e328-4e11-9094-db2139a08fe0 Claude Unavailable Available.{ messaging-build claude-86b6e54cb9618d95d6d8ceaa w17:p1 term_65c5883e612c88a } { e51411 e5141130-9a4a-4b8f-b405-67d941a7b320 handover-successor } Active }
```

- 88475f remains Active, with no change.
- Its endpoint selection is `Unavailable`: there is no socket endpoint, and the Herdr route is what carried the Send.
- The Herdr agent name in Flow's route is `claude-86b6e54cb9618d95d6d8ceaa`, while Herdr names the pane's agent `psyche-opus-88475f`. The pane and terminal match, and the Send resolved.

## Sources

- `receipts/flow-l2-send-grades.md` (the grades).
- signal-flow `ethos/signal.ethos` at `74a47ed`.
- flow `Cargo.toml` at `fe709c7`.
- Live `flow` CLI output: `/nix/store/42xmmsnnsjr6pq7q8jj7p0mx9mqxf3cw-flow-0.12.1/bin/flow`.
- `herdr agent get` and `herdr agent read` on w17:p1.
