# messagingUp

## 2026-09-16 — the messaging should go up so the living gets notified of important stuff

Context: while dispatching the transcript-nexus build to Codex, the living asked for the notification channel to be turned on.

> I also want the messaging to go up so I can get messages and get notified of important stuff.

-- psyche, typed.

Prior anchors this connects to:

- `flows/6cc91b/vision/messenger.md` (2026-09-13) — the messenger is the small-model job on the open-source harness that fires when a prompt arrives and mirrors to the other harnesses. "Messaging up" is the other direction of the same idea: the flows push notable events to the living.
- `flows/6cc91b/vision/interflowMessaging.md` (2026-09-14) — inter-layer messages ride tool-call returns and async signals; lower layers' messages never appear as user prompts, except relays which are deliberately visible in the primary's transcript.

Flow reading, not the living's words: the messaging-up channel is separate from the transcript-nexus. It is the outbound side of the messenger — a delivery channel for the living, not another flow-to-flow wire. What "important stuff" means (Codex build finishing, an open question needing an answer, a psyche flow escalating, a HIGH-only alert) is the living's call and would live in the meta-signal of whichever Nexus owns this channel. This flow does not set up notifications; it records the direction so the messenger design carries it.

## Open questions worth the living's word

1. Which channel — mobile push, Slack, SMS, email, something else — is the "up" endpoint.
2. Which flows are allowed to notify — every flow, only MEDIUM+, only on explicit main-flow ask.
3. What counts as "important stuff" — an enum in the meta signal of the messenger.
4. Whether this is a separate `messenger-nexus` or piggybacks on an existing one.
