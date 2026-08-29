# Listener adapted to Wispr Flow

Research Wispr Flow's unofficially used service surface and Linux clients, understand the current Listener/Demon code, recover prior visual-report attempts, and synthesize an end-shape for separate speech-to-text providers with an ASCII high-level view.

Vision recorded: one Wispr Pro subscription should practically serve Android and Linux; Listener may need explicit listener/provider boundaries so Wispr Flow now and a self-owned Wispr-like server later are separate backends.

Subflows returned: current code map, Wispr protocol/client research, and prior Listener/visual-report memory. Repository policy reserved Terra for implementation, so the read-only investigations ran under Luna/xhigh.

Remembered: 01a0439f, 019fe121, e06e4c07, f426777b, 01a04236, 01a0428b — depth 2 — Listener durability/vocabulary/anomaly evidence, Nexus vocabulary, and the Claude Artifact versus Codex Sites report paths.

Found: current Listener already has a backend-neutral batch-transcriber seam and durable retryable media, but production construction/configuration/errors remain OpenAI-shaped. Wispr exposes a separately billed official Voice API; unofficial clients reconstruct a private desktop gRPC/Supabase protocol; wispr-flow-linux repackages the proprietary Electron client and implements Linux input glue rather than the cloud protocol. Pro entitlement does not establish authorization for private protocol use.

Visual-report recovery: Claude used its built-in Artifact publisher. Codex's separate Sites report hub ultimately deployed successfully, but its proposed reusable skill, browser/screenshot QA, navigation/update/rollback contract, and lasting ACL proof were left unfinished.

Open for psyche anatomy: official-versus-private Wispr authority; batch-only versus live provider contract; provider selection/configuration authority; safe credential ownership; whether to complete the Codex Sites reporting skill later.

Correction: current Listener does not use Kameo or Tokio; its mailbox, concurrent finalizations, and transcription workers use standard channels and threads with blocking reqwest. A Kameo/Tokio realization would replace this machinery rather than merely add another adapter.

Vision added: an ordered first-choice/fallback provider policy is data-configured through a meta-listener operation; Wispr Flow failure falls back to OpenAI and produces a provider-failure notification.

Notion added: continuous recording may segment around a natural pause after four to five minutes and use overlapping audio chunks with transcript reassembly. This remains brainstorming, not a ruling.

20-minute claim reconciled: Wispr documents a 20-minute desktop-app dictation session, while the official Voice API still documents six minutes/25 MB and private gRPC limits remain unproved.
