# OpenAI Subscription Route Evidence

Date: 2026-07-03

## Scope

Set up or verify a local OpenAI-compatible server route for later Mind live judge eval with `gpt-5.5`.

Target bind: `127.0.0.1:18080`

Target base URL: `http://127.0.0.1:18080/v1`

Preferred project: `hotchpotch/openai-api-server-via-codex`

## Source And Tooling Observations

- No existing local clone named `openai-api-server-via-codex` was found under `/home/li/primary`, `/home/li/primary/repos`, or `/home/li/primary/private-repos`.
- Upstream README for `hotchpotch/openai-api-server-via-codex` documents `uvx openai-api-server-via-codex`, default server URL `http://127.0.0.1:18080`, `/v1` OpenAI-compatible endpoints, and Codex auth from `~/.codex/auth.json`.
- Local `uv`, `pipx`, and Python `pip` were not available on PATH.
- Temporary Nix-provided `uv` worked: `nix run nixpkgs#uv -- --version` reported `uv 0.11.7`.
- Package command help via `nix run nixpkgs#uv -- tool run openai-api-server-via-codex --help` reported subcommands `serve`, `start`, `stop`, `status`, and `config-generate`.
- Installed package version reported by `openai-api-server-via-codex --version`: `0.1.3`.

## Auth Check

Checked `~/.codex/auth.json` without printing secret values.

Observed JSON shape:

- top-level keys: `auth_mode`, `OPENAI_API_KEY`, `tokens`, `last_refresh`
- `OPENAI_API_KEY`: `null`
- `tokens`: object with keys `id_token`, `access_token`, `refresh_token`, `account_id`

Server auth preflight reported OK and `account_id_present=True`.

## Commands Used

Secret-bearing values were not printed. The only auth reference passed to the server was the path `~/.codex/auth.json`.

```sh
find /home/li/primary -path /home/li/primary/repos -prune -o -path /home/li/primary/private-repos -prune -o -maxdepth 4 -type d -name openai-api-server-via-codex -print
find /home/li/primary/repos /home/li/primary/private-repos -maxdepth 5 -type d -name openai-api-server-via-codex -print 2>/dev/null
test -f ~/.codex/auth.json && node -e '[JSON shape check only; no secret values printed]' || echo auth_exists=false
command -v uv && uv --version
command -v python3 && python3 --version
command -v pipx && pipx --version
python3 -m pip --version
nix run nixpkgs#uv -- --version
nix run nixpkgs#uv -- tool run --refresh-package openai-api-server-via-codex openai-api-server-via-codex --help
nix run nixpkgs#uv -- tool run openai-api-server-via-codex serve --help
nix run nixpkgs#uv -- tool run openai-api-server-via-codex start --help
nix run nixpkgs#uv -- tool run openai-api-server-via-codex --version
nix run nixpkgs#uv -- tool run openai-api-server-via-codex start --host 127.0.0.1 --port 18080 --auth-json "$HOME/.codex/auth.json" --default-model gpt-5.5
ss -ltnp 'sport = :18080'
nix run nixpkgs#uv -- tool run openai-api-server-via-codex status --host 127.0.0.1 --port 18080
curl -sS http://127.0.0.1:18080/v1/models
curl -sS http://127.0.0.1:18080/v1/responses -H 'Content-Type: application/json' -H 'Authorization: Bearer local-probe-redacted' --data '{"model":"gpt-5.5","input":"Reply with OK only.","max_output_tokens":16}'
ps -o pid,ppid,comm,args -p 709780,709942
```

## Server Result

Started successfully:

- Status command: `running: PID 709780`
- Listener: `127.0.0.1:18080`
- Listening process observed by `ss`: PID `709942`
- PID file: `/home/li/.config/openai-api-server-via-codex/run/server-127.0.0.1-18080.pid`
- Log file: `/home/li/.config/openai-api-server-via-codex/run/server-127.0.0.1-18080.log`

The daemon supervisor PID is `709780`; the serving child PID is `709942`.

## Endpoint Probes

`GET http://127.0.0.1:18080/v1/models`

- HTTP status: `200`
- response object: `list`
- model count: `3`
- `gpt-5.5` visible: `true`
- first model IDs observed: `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`

`POST http://127.0.0.1:18080/v1/responses`

Request used model `gpt-5.5`, a harmless prompt, and dummy incoming bearer token `local-probe-redacted`.

- HTTP status: `200`
- response ID present: `true`
- response object: `response`
- status: `completed`
- output item count: `2`
- content type observed: `output_text`
- first text: `OK`

## Current State

The local OpenAI-compatible route is running for later eval use:

```text
OPENAI_BASE_URL=http://127.0.0.1:18080/v1
model=gpt-5.5
```

No blocker remains for local use from an OpenAI-compatible client pointed at the base URL above.
