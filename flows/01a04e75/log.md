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

Implementation completed in isolated feature bookmarks `listener-wispr-01a04e75`; main was not moved. Listener final head `71a194df8dc6dfb232049473481e67b405153e49`, version 0.17.0. Portable producer heads: meta-signal-listener `0330642948d0070b57d693f211d6846d055c16c8`, signal-listener `b44a9e7a2161e1fd77df6ecde64bb824f2dd2069`, schema-rust `5c743ee5cab80db66fa1f21708792983aa73929f`, triad-runtime `428cb2fcdbf5d5c9cd4fb8ea83255beab60f9155`.

Realized: Kameo/Tokio ListenerCore and provider workers; privileged durable meta provider policy; Wispr-first/OpenAI fallback; private Wispr gRPC framing and request-time gopass boundary; degradation/recovery circuit and redacted notification; durable job/result/history/delivery intent/receipt; pause-aware committed-PCM segmentation with 5:50 hard cap, overlap and conservative stitching; genuine pre-Stop chunk scheduling with catch-up from durable offsets.

Proof: terminal remote Nix full test gate exit 0; remote listener 0.17.0 package build exit 0; feature worktree clean; bead listener-a9b closed; all feature Locks released. Main integration, downstream activation, gopass provisioning, and live Wispr interoperability were not performed. No real credential or provider call entered the flow.

Operational witness: installed Orchestrate 0.26 accepts scalar `Release.<id>`; the loaded orchestrate skill's `Release.{<id>}` form failed in the client parser before the socket. No skill edit was authorized or made.

Correction: the Linux `~/.config/Wispr Flow/session.json` path is produced only by the unofficial Linux repackaging of Wispr's proprietary desktop application (or a deliberately copied profile). Wispr does not provide an official Linux client, and the reconstructed clients are not logging into a Wispr web app.
