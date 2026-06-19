# Cloud-maintainer browser profile

Cloud-maintainer browser automation uses a dedicated Chrome profile with native Chrome DevTools Protocol, not the real daily Chrome profile and not the experimental CDP bridge.

## Profile

- Profile directory: `/home/li/.local/state/cloud-maintainer/chrome-profile`
- CDP endpoint: `http://127.0.0.1:9223`
- Launcher: `/home/li/.local/bin/cloud-maintainer-chrome`
- Log: `/home/li/.local/state/cloud-maintainer/cloud-maintainer-chrome.log`
- PID file: `/home/li/.local/state/cloud-maintainer/cloud-maintainer-chrome.pid`

The profile is user-local state. It is not tracked by git and is not a Nix store path. It persists login sessions for cloud-maintainer work only.

## Starting it

```sh
cloud-maintainer-chrome https://cloud.digitalocean.com/login
```

The launcher starts Google Chrome with:

```sh
--user-data-dir=/home/li/.local/state/cloud-maintainer/chrome-profile
--remote-debugging-address=127.0.0.1
--remote-debugging-port=9223
--no-first-run
```

If the CDP endpoint is already listening, the launcher opens the requested URL in the existing profile and exits successfully.

## Verification

```sh
curl -fsS http://127.0.0.1:9223/json/version
```

A healthy profile returns Chrome version JSON with a `webSocketDebuggerUrl` rooted at `127.0.0.1:9223`.

## Agent use

Agents attach browser-use or Playwright-style tooling directly to `http://127.0.0.1:9223`. This is the production-ish path for browser automation because Chrome provides the browser-level CDP shape natively.

The experimental real-profile bridge remains a diagnostic path only. It is not the default for cloud account setup, token creation, billing, or provider-console work.

## Secret handling

Tokens are transient working material under `skills/secrets.md`. Keep token values out of chat, reports, commit messages, shell traces, and durable plaintext files. Store the DigitalOcean personal access token at:

```text
digitalocean/api-token
```

Prefer piping to `gopass insert -f digitalocean/api-token` when blind handling is enough; inspect only when the task requires it.
