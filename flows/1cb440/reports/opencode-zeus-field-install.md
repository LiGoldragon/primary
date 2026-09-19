# Zeus OpenCode Field installation status

## Scope and authority

Field owns the bounded Zeus source, installation, service, and authentication-rejection witnesses. Mind owns provider/model, API, mobile, permission, and share testing after the living completes manual Codex subscription login. Sol retains CriomOS-home input pins and Field Luna deployment work.

The living required Zeus only; no Prometheus, reboot, phone pairing, notification, GoPass, API key, provider inference, or model execution. The listener must use only the trusted Criome Tailnet address and port 4096. A service credential is supplied with systemd `LoadCredential`; if OpenCode accepts only `OPENCODE_SERVER_PASSWORD`, a private wrapper may read the credential file and set that variable only for the OpenCode child. Credential bytes must not enter arguments, logs, model context, or this record.

## Witnessed Zeus state

Read-only SSH to `li@zeus.goldragon.criome` reached host `zeus`. It has OpenCode `1.18.16` at `/home/li/.nix-profile/bin/opencode`. Its installed `opencode serve --help` witnesses `--hostname` and `--port`; the defaults are `127.0.0.1` and port `0`. Its installed `opencode auth login --help` supports `--provider` and `--method`, but does not enumerate provider or method labels. It does not establish password, OAuth, API route, or permission policy. Remote non-building `nix eval nixpkgs#opencode.version` also returned `1.18.16`, but it is a registry resolution, not the target flake pin. The registry package derivation and active profile derivation resolved without exposing their paths.

No `opencode-zeus.service`, timer, or path unit is installed. No OpenCode share configuration exists. No service was started and no listener, health result, or unauthenticated rejection exists.

The living defines the Criome cluster's trusted network as the Tailnet in [operational-criomeClusterIsTheTailnet.md](../../c8d79f/vision/operational-criomeClusterIsTheTailnet.md). Zeus's observed Ygg address is `200:17f7:4fad:e50b:a50c:2048:2169:41f7`, which matches the Zeus address in `/git/github.com/LiGoldragon/goldragon/proposal.datom`. The LAN address `10.18.0.108` is excluded.

## Source and deployment boundary

CriomOS's existing `modules/nixos/testing/opencode.nix` supplies a default-off `criomos.testing.opencode.enable` package flag only. CriomOS-home's agent-intercom package copies an OpenCode plugin source, but its active agent-intercom module has no OpenCode configuration activation.

A Zeus-only enablement cannot be encoded as a `node.name` conditional: both OS and Home require projected role/capability selection. Zeus has no existing OpenCode-specific capability. Reusing `TailnetClient` changes unrelated Tailscale behavior; reusing `PersonaDevelopment` would activate unrelated persona-development services. A dedicated projected enablement capability or another authorized configuration input is therefore required before writing the service/module selection.

Lojix query currently has no durable Zeus generation or deployment record. Retained Zeus `complete-host` materialized inputs exist from 2026-09-06 and declare `includeHome = true`, but are retained generated evidence rather than a current deployment request. No immutable source revision, exact Lojix transport, remote builder selection, output selector, or deployment request has been established. No remote Nix build or activation was attempted.

## Manual login boundary

The provided upstream source claim, not an installed-CLI witness, is:

```text
opencode auth login --provider openai --method "ChatGPT Pro/Plus (browser)"
```

The living runs it interactively on Zeus after the installed version's `auth login --help` confirms the syntax. Field will not perform the login or inspect its resulting credentials.

## Next safe actions

1. Establish the projected Zeus-only enablement source without node-name logic.
2. Reserve the exact CriomOS/CriomOS-home paths, add the generic user service and its private credential wrapper, and push immutable revisions.
3. Submit the exact remote-only Lojix deployment after its transport, builder, selector, and activation contract are witnessed.
4. Verify the installed CLI's login and password interface; only then obtain service readiness, `GET /health`, and unauthenticated-rejection witnesses. Mind begins its owned tests only after manual login.
