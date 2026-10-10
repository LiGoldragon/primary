# Tailscale trust witness

Observed 2026-09-25; bounded read-only collection.

## Method

Read the first and last retained `tailscaled` journal entries matching `x509` and `unknown authority`, queried current `tailscale status --json` selected fields, inspected the effective service definition, and performed a targeted certificate-name scan under `/etc` and `/var/lib`. No state file, credentials, full journal, or certificate private material was read.

## Observations

- First retained matching journal line:
  `2026-06-05T07:00:47-06:00 ouranos tailscaled[3337]: Received error: fetch control key: Get "https://127.0.0.1:8443/key?v=133": x509: certificate signed by unknown authority`
- Latest matching journal line:
  `2026-09-25T21:20:23-06:00 ouranos tailscaled[1482]: Received error: fetch control key: Get "https://127.0.0.1:8443/key?v=142": x509: certificate signed by unknown authority`
- Current selected status fields: `BackendState` is `NoState`; `TailscaleIPs` is null; `Online` is null; `CurrentTailnet` is null.
- The witnessed control endpoint is local HTTPS at `127.0.0.1:8443` (the journal request path is intentionally not used as a configuration assertion).
- The effective service is generated from the system Tailscale package and uses its standard state/socket paths.
- No Headscale/Tailscale CA or server-certificate file was found by the targeted `/etc` and `/var/lib` filename scan; therefore no certificate subject, issuer, validity, or trust-anchor metadata was witnessed.

## Inference

The repeated unknown-authority failures together with `NoState` and no address show that this node has not established a usable trusted control-plane state at observation time. They do **not** identify the intended trust anchor, certificate owner, or safe repair; those remain unknown.

## Sources

- `journalctl -u tailscaled --no-pager -o short-iso`, bounded to first/latest matching error lines.
- `tailscale status --json`, selected fields only.
- `systemctl cat tailscaled.service`.
- Targeted certificate-name metadata scan under `/etc` and `/var/lib`.
