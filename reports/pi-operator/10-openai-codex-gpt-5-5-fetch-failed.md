# OpenAI Codex GPT-5.5 `fetch failed` diagnosis

## Scope

Investigated repeated Pi interactive failures shown as `Retry failed after 3 attempts: fetch failed` for `openai-codex/gpt-5.5`, without printing OAuth tokens or performing remediation/deploy/session-live actions.

## Findings

- Active Pi settings select `openai-codex/gpt-5.5`; the local `openai-codex` OAuth record has access and refresh material, an account identifier, and an expiry in the future during the investigation.
- Basic DNS/TLS to OpenAI and ChatGPT hosts works. Authenticated non-generating probes reach ChatGPT backend endpoints; `https://chatgpt.com/backend-api/models` returns 200 with the stored OAuth token.
- A minimal Pi no-session request using `openai-codex/gpt-5.5` succeeded with `OK`, so the provider, model, and OAuth credential are not globally broken.
- The exact Codex responses endpoint is `https://chatgpt.com/backend-api/codex/responses` for SSE and the same URL upgraded to `wss:` for WebSocket. Non-generating `HEAD`/`OPTIONS` probes reach the endpoint and return HTTP 405, ruling out DNS/TLS/path outage for that host/path.
- The installed provider first tries WebSocket when transport is `auto`. A WebSocket failure before any model events records a session-wide SSE fallback flag. Once that flag is set, later attempts in that session skip WebSocket and go directly to SSE `fetch`.
- The screenshot-matching failure series is in `~/.pi/agent/sessions/--home-li-primary--/2026-06-06T08-49-16-602Z_019e9c1f-493a-7333-b245-cefca8ee9494.jsonl`, lines 9319-9322, at `2026-06-19T15:53:19Z` through `15:53:35Z`. All four assistant records are `provider=openai-codex`, `model=gpt-5.5`, `api=openai-codex-responses`, `stop=error`, `errorMessage='fetch failed'`, zero usage, and no content blocks.
- A related earlier line, 9174, shows the same version of Pi recording `provider_transport_failure` from WebSocket before message-stream start, then falling back to SSE. Its final visible error was `fetch failed`.
- Historical session data contains many WebSocket transport failures for this provider across Pi versions 0.75.3 through 0.79.1, often with large request payloads. Some failures happen after the stream starts; others happen before start and trigger SSE fallback.

## Cause boundary

The repeated screenshot failure is not explained by missing model configuration, expired local auth, global OpenAI reachability, or a normal HTTP API rejection. It is a transport-layer failure in Pi's OpenAI Codex Responses provider.

More precisely: in `auto` transport, a WebSocket failure can put the session into SSE fallback; the visible `fetch failed` is native Node/undici `fetch` failing before Pi receives an HTTP response from `https://chatgpt.com/backend-api/codex/responses`. Because the provider only stores `error.message`, the underlying socket/TLS cause is lost in the session record when the error is exactly `fetch failed`.

The remaining unknowable boundary from existing logs is the low-level `fetch` cause for the four screenshot attempts: Pi 0.79.1 did not persist `error.cause` for those SSE exceptions.

## Safe remediation and next diagnostics

- Immediate workaround: in Pi `/settings`, set Transport to `websocket` rather than `auto` if the current failure series is pure `fetch failed` after fallback. This avoids the sticky SSE fallback path. If WebSocket itself starts failing after stream start, start a fresh session or use a smaller/compacted branch.
- Alternative workaround: start a new Pi session or fork/clone the branch after compaction. The observed failures correlate with large long-running sessions and transport fallback state; a minimal no-session request succeeded.
- Provider hardening: Pi should persist diagnostic detail for SSE fetch exceptions, including `error.name`, `error.message`, and safe `error.cause` fields such as `code`, `errno`, `syscall`, `address`, and `port`, without headers or tokens. That would distinguish connection reset, timeout, proxy, IPv6, DNS, TLS, or remote close.
- Diagnostic if it recurs: capture the session line immediately after the failure and inspect whether a preceding `provider_transport_failure` diagnostic says WebSocket failed before message-stream start. If yes, the failure is the WebSocket-to-SSE fallback sequence, not auth.
