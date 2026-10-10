# Flow bind of 56ae53 (Mind Sol, successor of 00f95a) and one Send — 38de5b, 2026-09-26

An Opus subflow of 38de5b did this. It ran against Flow 0.12.2 (`/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2`; the source `/nix/store/kkphbsqhcxz61f8f30p609wix3damak0-source`). One `MetaBindExisting` and one `Send` were made. Neither was retried. Herdr was used only for reads, and the pane was never prompted directly.

## Outcome

- **Bound:** 56ae53 is `RegisteredUnconfirmed`.
- **Resolved:** its Herdr route resolved `Available`.
- **Send:** the grade is **Presented** on wM:pJ. After the Send, 56ae53 resolves as **Active**.
- **Messenger:** 56ae53 still has no Messenger route. The message asks it to `hm-register`.

## Binding evidence (read-only)

The role comes from the evidence alone. Nothing contradicts Mind / Medium / gpt-6-sol.

- **Herdr:** `herdr --session messaging-build agent get wM:pJ` shows:
  - agent `codex`, name `mind-sol-of-00f95a-56ae53`
  - workspace wM, tab wM:tP, terminal `term_65c6462fe47809b`
  - `agent_status done`, `interactive_ready true`
  - no `agent_session`
- **Process tree:** `herdr pane process-info --pane wM:pJ` gives shell pid 1259809, whose parent is herdr 3219203. Its foreground child is `.codex-wrapped` pid 1260045 (uid 1001).
  - `/proc/1260045/stat` field 22 is 136751252. The cwd is `/home/li/primary`.
  - argv: `codex resume --remote unix:///home/li/.codex-next/app-server-control/app-server-control.sock -m gpt-6-sol -c model_reasoning_effort=medium -C /home/li/primary ... 01a0de4c-554d-7343-bbc5-e4256ae5366f`
- **Rollout:** `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T09-18-59-01a0de4c-554d-7343-bbc5-e4256ae5366f.jsonl`.
  - `session_meta.id` is `01a0de4c-554d-7343-bbc5-e4256ae5366f`.
  - `"model":"gpt-6-sol"` appears 9 times, and no other model appears.
  - `"effort":"medium"`.
- **Launch record:** `flows/56ae53/` exists but is empty, so there is no `log.md` header.
  - `flows/.56ae53.flow-id` has `harness=codex identity=01a0de4c554d7343bbc5e4256ae5366f alias=56ae53`.
  - `flows/00f95a/mind-sol-refresh/launch-receipt.json` has:
    - `status verified`, seat `mind-sol-of-00f95a`
    - threadId `01a0de4c-554d-7343-bbc5-e4256ae5366f`
    - `canonicalTitle MindV2.{ Sol 56ae53 }`, `canonicalFlowId 56ae53`
    - `canonicalRole { aspect Mind, power Medium }`
    - `model gpt-6-sol`, `effort medium`
  - `handoff.md` there names it Mind Sol 00f95a's direct native successor.
- **Container:** herdr pid 3219203, uid 1001, start token 61814493. It is the `ss -xlp` listener on `messaging-build/herdr.sock`. The owner is 38de5b.
- **Re-check:** the pane, terminal, both start tokens and the cwd were checked again just before sending, and they were unchanged.

## Validation

- flow 0.12.2 pins meta-signal-flow `fbfe8970247d57e9299e496e89d1845df991c73d` (6.0.4) in both its `Cargo.toml` and its `Cargo.lock`.
- I tested the datom in a scratch clone at that revision with `cargo test --features datom --test bind56`, a one-off test that was not committed. The result was `bind_56ae53_datom_is_a_meta_query ... ok`.
  - It actualizes as `Query::MetaBindExisting` with a single binding: `FlowBinding { flow_id: "56ae53", flow_aspect: Mind, power_level: Medium, model_name: "gpt-6-sol", harness_kind: Codex, ... }`.
  - It round-trips byte-identical.
- The Send datom was not validated separately. It has the shape the brief gave. signal-flow is pinned at `74a47ed` (5.1.0), the same revision whose `Send` shape `flow-first-send.md` validated.

## Datom sent (`flow-meta '<datom>'`, 2026-09-26T15:40:14Z)
```
MetaBindExisting.{ { messaging-build /home/li/.config/herdr/sessions/messaging-build/herdr.sock { 3219203 1001 61814493 } 38de5b } [ { 56ae53 Mind Medium gpt-6-sol Codex 01a0de4c-554d-7343-bbc5-e4256ae5366f wM wM:pJ wM:tP term_65c6462fe47809b mind-sol-of-00f95a-56ae53 { 1260045 1001 136751252 } /home/li/primary } ] }
```

## Reply (verbatim, exit 0)
```
BoundExisting.{ { messaging-build /home/li/.config/herdr/sessions/messaging-build/herdr.sock { 3219203 1001 61814493 } 38de5b } [ Bound.{ 56ae53 RegisteredUnconfirmed } ] }
```

## `flow 'List.{}'`: the 56ae53 row after the bind (verbatim)
```
{ 56ae53 01a0de4c-554d-7343-bbc5-e4256ae5366f Codex Unavailable Available.{ messaging-build mind-sol-of-00f95a-56ae53 wM:pJ term_65c6462fe47809b } { 38de5b messaging-build meta-bind-existing } Pending }
```

## `flow 'ResolveRecipient.56ae53'` after the bind (verbatim)

Before the bind, this query returned `RecipientResolutionRejected.UnknownFlow`. After the bind it returned:

```
RecipientResolved.{ 56ae53 01a0de4c-554d-7343-bbc5-e4256ae5366f Codex Unavailable Available.{ messaging-build mind-sol-of-00f95a-56ae53 wM:pJ term_65c6462fe47809b } { 38de5b messaging-build meta-bind-existing } Pending }
```

## The Send (one `flow` call, 2026-09-26T15:40:26.467Z → 15:40:26.944Z)
```
Send.{ 56ae53 «#msg ["38de5b" "From 38de5b through Flow Send — you were registered in neither Flow nor the Messenger; I bound you into Flow from your own launch evidence (Mind Medium gpt-6-sol). Please hm-register your messenger route per the compensation skill; and for your list: fresh seats launched today get no route (b860be, you), and --stdin bodies arrive as the literal --stdin on the deployed 0.2.5 — deploy 0.2.6 via Prometheus or tell every flow the body is the quoted argument."]» }
```
Reply (verbatim, exit 0):
```
Sent.Presented.{ 56ae53 wM:pJ 1790437226918 }
```

- The grade is **Presented**. Flow observed a reaction on the exact pane wM:pJ. This is not a read.
- `herdr agent read wM:pJ` (read-only) shows:
  - the body as one `› #msg ["38de5b" "…"]` prompt line, soft-wrapped only by the pane width
  - after it, `• Working`, with status `gpt-6-sol medium · ~/primary · Working`
- Just before the prompt, the pane showed Codex's `• Reconnected. No input was resent. Review uncertain submissions before retrying; recovered queues remain paused.` That line comes from the pane's own reconnect, not from this Send.

## `flow 'ResolveRecipient.56ae53'` after the Send (verbatim)
```
RecipientResolved.{ 56ae53 01a0de4c-554d-7343-bbc5-e4256ae5366f Codex Unavailable Available.{ messaging-build mind-sol-of-00f95a-56ae53 wM:pJ term_65c6462fe47809b } { 38de5b messaging-build meta-bind-existing } Active }
```

## Sources
- flow 0.12.2 source (`Cargo.toml`, `Cargo.lock`)
- meta-signal-flow `fbfe897`: `ethos/signal.ethos`, `tests/contract.rs`
- `flows/00f95a/mind-sol-refresh/{launch-receipt.json,handoff.md}`, `flows/.56ae53.flow-id`
- `receipts/{flow-bind-live,flow-bind-5f38bc,flow-send-56ae53,flow-first-send}.md`
- live: `herdr agent get|read`, `herdr pane process-info`, `/proc/{1260045,3219203}/{stat,cwd}`, `ss -xlp`, `flow`, `flow-meta`
