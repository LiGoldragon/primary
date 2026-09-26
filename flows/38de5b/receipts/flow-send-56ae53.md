# Flow Send to 56ae53 (Mind Sol): not sent, because Flow does not know it

An Opus subflow of 38de5b did this on 2026-09-26. Everything below was read-only. Nothing was sent.

## Flow 0.12.2 (`/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow`)

- `flow 'List.{}'`: there is no record for 56ae53, so it is not bound in any state.
- `flow 'ResolveRecipient.56ae53'` returned `RecipientResolutionRejected.UnknownFlow` (exit 0).
- Flow resolves no Herdr route for 56ae53. Per the brief, no `Send` was issued and no datom was submitted.

## Herdr (all three sessions searched: default, fms-9bc4f7, messaging-build)

Only one pane carries 56ae53:

```
session messaging-build  pane wM:pJ  tab wM:tP  workspace wM
name mind-sol-of-00f95a-56ae53  agent codex  agent_status done  interactive_ready true
terminal term_65c6462fe47809b  terminal_title "primary"  revision 3
```

- There is **no `agent_session` field**, so Herdr exposes no official Codex session identity for this pane.
- The title is the generic `primary`, and "Mind Sol" does not appear in it. The only match is the pane name.

## Messenger (read-only)

- `hm-list` shows `-  mind-sol-of-00f95a-56ae53  messaging-build  done`. The pane is seen live, but no FLOW is registered to it.
- `hm-heartbeat-state` has no route or retirement for 56ae53.
- An `hm-repair` onto wM:pJ would need the typed `agent_session`, which is missing. This matches the earlier `Held RepairRequired, no candidates`.

## Standing

- 56ae53 exists only as a Herdr pane. Neither Flow nor Messenger has registered it.
- Reaching it takes one of three things:
  - 56ae53 registers itself (Flow bind and/or `hm-register`).
  - The main flow decides to prompt wM:pJ directly through Herdr, naming the refusal.
  - The seat is relaunched with a registered route.
- The intended body is unsent. It is in the 38de5b brief.
