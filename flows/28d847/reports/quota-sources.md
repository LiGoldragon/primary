# Quota sources: requirements for the quota component

Subflow of 28d847, 2026-10-03. Requirements for the Nexus component a Mind Astra flow will build: one call returning every subscription's quota windows and each live flow's context use. Everything marked witnessed was observed on this host at 2026-10-03T20:45Z. Nothing was built, and no repository was created or changed.

## Subscriptions in use

| Subscription | Evidence | Plan |
|---|---|---|
| Anthropic Claude (Claude Code 2.1.284) | `~/.claude/.credentials.json`, key `claudeAiOauth`; five interactive sessions live | `subscriptionType: max`, `rateLimitTier: default_claude_max_20x` |
| OpenAI ChatGPT (Codex) | `~/.codex/auth.json`, `~/.codex-next/auth.json`, `~/.codex-next-8mkkxq293hk2/auth.json`, all `auth_mode: chatgpt`. All three hold the **same** account ID, so they are one subscription. Pi's `openai-codex` OAuth entry is the same subscription too. | `planType: pro` |

Not subscriptions, or not in use:
- Gemini CLI. `~/.gemini/oauth_creds.json` (`oauth-personal`) was last written 2026-08-07, and the newest history is from 2026-08-07. It is dormant: whether a paid plan stands behind it is unknown, and its token has expired.
- Pi's `criomos-largeai`, `criomos-local` and `prometheus` entries. These are API keys for local or self-hosted model servers, not vendor quotas.
- opencode and kilo have no provider configured. The GitHub Copilot config holds only `versions.json`, and there is no evidence the subscription is in use.

## Claude: quota windows and resets

**Source:** `GET https://api.anthropic.com/api/oauth/usage` with headers `Authorization: Bearer <claudeAiOauth.accessToken>` and `anthropic-beta: oauth-2025-04-20`. This is the endpoint Claude Code's own `/usage` view calls. The 2.1.284 binary has the table `{plain:"/api/oauth/usage", at_wall:"/api/oauth/usage?at_wall=1&skip_spend=1", ...}` in `fetchUtilization`. **Witnessed:** HTTP 200.

The response gives, per window, `utilization` (a percent) and `resets_at` (ISO 8601 UTC):
- `five_hour`: 20.0, resets 2026-10-03T23:20Z
- `seven_day`: 11.0, resets 2026-10-10T13:00Z
- `limits[]`: a normalized list (`kind`, `group`, `percent`, `resets_at`, `scope`, `is_active`). It includes `weekly_scoped` with `scope.model.display_name: "Fable"` at 10%. **The component should read `limits[]` as the primary list**, because it carries model-scoped weekly windows that have no fixed top-level key.
- `extra_usage` and `spend`: overage credits (disabled here).
- `seven_day_breakdown`: share of usage by surface (Claude Code 100%).
- Many other top-level keys are null codenames (`seven_day_opus`, `tangelo`, ...). Treat any key that is not null and not recognized as "unknown window present" and do not drop it.

The endpoint gives **no absolute limit** (tokens or dollars), only percentages; the `limit_dollars` fields are null. The output must say so rather than invent one.

**Credentials:** the program reads `~/.claude/.credentials.json` itself, and the token must never pass through a model. The secret must go no further than the HTTP request header: not in argv, not in the environment, not in the output. The witness piped `jq` straight into `curl -H @-`.
- `expiresAt` (epoch ms) has to be checked first. If the token has expired, report "token expired; a running Claude Code refreshes it" and **do not refresh it yourself**. A refresh rotates the refresh token, and writing a rotated token back would race Claude Code's own writes to the file.
- The access token lives for hours, and the live sessions keep it fresh.

**Rejected alternative:** the status-line JSON (`rate_limits.five_hour/seven_day.used_percentage`, `resets_at`). It is the same data, but Claude Code pushes it only into the status-line process on each render. `~/.claude/statusline.sh` does not save it, so a separate CLI cannot pull it.

## Codex: quota windows and resets

**Source:** the app-server JSON-RPC method `account/rateLimits/read` (no params). This is the call Codex's own client makes. **Witnessed** over `~/.codex/app-server-control/app-server-control.sock`, in 557 ms:

- `rateLimits.primary`: `usedPercent` 21, `windowDurationMins` 10080 (the seven-day window), `resetsAt` 1791580388 (epoch seconds)
- `secondary`: null
- `planType`: pro
- `rateLimitReachedType`: null

`rateLimitsByLimitId` returns one entry per limit ID. Earlier witnesses also saw a `codex_bengalfox` sub-limit (Spark) with five-hour and seven-day windows (`primary-next/flows/6cc91b/reports/quotaProtocol.md`), so the component must iterate over every limit ID. The window comes from `windowDurationMins`; do not assume it.

**Transport:** WebSocket over a Unix socket. Send `initialize` and then `initialized` before the request. A working client already exists in `primary-next/tools/field-census/codex-context.mjs` (`appServerRequest`). An alternative needs no running daemon: spawn `codex app-server` and speak JSON-RPC over stdio. That has not been witnessed here.

**Credentials:** none in the component. The app-server reads `auth.json` itself. Query one socket only, because all homes are one account.

## Context use per live flow

**Enumerating live Claude flows:** `~/.claude/sessions/<pid>.json` is Claude Code's registry of live sessions, with `pid`, `sessionId`, `cwd`, `name` (for example `Psyche.{ Opus 28d847 }`), `kind` and `status`. The flow ID is the first six hex characters of `sessionId`. Check that the pid is alive before trusting an entry.

**Claude context use:** there are two sources.
- **Best, with an installer change:** a status-line wrapper that saves `context_window` (`used_percentage`, `context_window_size`, `total_input_tokens`) per session. This is exact, but needs a change to the user environment. `primary-next/tools/field-census/claude-statusline-publish.mjs` already does this but is **not installed**: `statusLine` is still `bash ~/.claude/statusline.sh`, and the snapshot directory is absent. Saving `rate_limits` as well would give a second Claude quota source.
- **Available now:** the tail of `~/.claude/projects/<cwd-slug>/<sessionId>.jsonl`. Take the last assistant `message.usage`: `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` is the context of that request. This is a proxy. It goes stale after a user turn or a compaction. The transcript gives the model ID but **not** the context window size, because `[1m]` is not visible, so the percent is unknown without the status-line snapshot. `claude-context.mjs` in field-census does this already, with bounded reads that never touch message content.

**Enumerating live Codex flows:** run `thread/loaded/list` on each live app-server control socket. **Witnessed:** `~/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock` returned the loaded thread IDs, and that is the socket the running `codex --remote` TUIs use. `~/.codex-next/...` and `~/.codex/...` returned empty lists. So the component has to discover the sockets, from the `--remote unix://...` argument of each live `codex` process or by globbing `~/.codex*/app-server-control/*.sock`. It must not hard-code one.

**Codex context use:** call `thread/read` (`includeTurns:false`) to get the rollout `path` and `model`, then take the last `event_msg` `token_count` in the rollout tail. `info.last_token_usage.input_tokens` is the context used, and `info.model_context_window` is the window, so the percent is exact for the window. Mark the value superseded when a user message or compaction follows it. `collectCodexContext` in field-census does this. Mapping a thread to a flow ID needs the HM or Herdr registry, which `field-census.mjs --overview` reads; the thread name may carry the flow ID.

## Existing code

- `github.com/LiGoldragon/primary-next/tools/field-census/` (Node). It has the Codex app-server WebSocket client, `account/rateLimits/read`, thread context from the rollout, Claude context from the transcript tail, an uninstalled status-line publisher, and tests against recorded inputs (`*.test.mjs`). It does **not** call the Claude `/api/oauth/usage` endpoint, and it has no Claude quota source except the uninstalled publisher.
- `field-census.mjs --overview`: a Herdr and HM roster with per-route context and one Codex `account_quota`. It runs on a five-minute timer and writes `~/.local/state/field-census/latest.json`.
- Prior design records: `primary-next/flows/b05237/reports/quota-anatomy.md` (sensor, ledger and metrics design; it said Codex had no source, which `account/rateLimits/read` has since answered), `flows/6cc91b/reports/quotaProtocol.md`, `flows/5f4fea/reports/quota-accounting.md` (relayed ruling: accounting in Persona "for now"), and `flows/6db4fe/reports/codex-context-usage.md`.

## Unavailable, and why

- **Absolute limits:** neither vendor exposes tokens or dollars per window, only percent used, so the limit is unavailable.
- **Claude context percent for a live session:** unavailable until a status-line snapshot is installed, because the transcript lacks the window size.
- **Claude quota when the access token has expired and no session is refreshing it:** unavailable. Refreshing it ourselves is not safe.
- **Gemini:** a dormant credential with an expired token. Whether a subscription exists at all is unknown.
- **Codex thread to flow ID:** needs the HM or Herdr registry. App-server data alone does not give it reliably.

## Sources

- Live call to `api.anthropic.com/api/oauth/usage`, HTTP 200, 2026-10-03T20:45:26Z (response `as_of`).
- Live `account/rateLimits/read` on `~/.codex/app-server-control/app-server-control.sock`, 2026-10-03T20:45:29Z. Live `thread/loaded/list` on the `~/.codex`, `~/.codex-next` and `~/.codex-next-8mkkxq293hk2` sockets. The method list came from the app-server's unknown-variant error.
- Claude Code 2.1.284 binary strings (`fetchUtilization`, the `/api/oauth/usage` table, the status-line `rate_limits` schema).
- Structure of the credential files, keys and plan fields only: `~/.claude/.credentials.json`, `~/.codex*/auth.json`, `~/.pi/agent/auth.json`, `~/.gemini/oauth_creds.json`.
- `~/.claude/sessions/*.json`, `~/.claude/settings.json` (`statusLine`), and `pgrep -a codex`.
- `primary-next/tools/field-census/` (README, `claude-context.mjs`, `codex-context.mjs`, `claude-statusline-publish.mjs`), and the `primary-next` reports named above.
