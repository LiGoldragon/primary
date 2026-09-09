# Codex desktop and report transport

The implementation landed in CriomOS-home commits `6fb30e0f1441` and
`9548d7d353dd`. It extends
the existing `codex-remote` Unix-socket attachment with `codex-desktop`; it does
not create another app-server.

`codex-desktop fresh PROMPT_FILE WORKING_DIRECTORY` opens a dedicated Ghostty
window through a bounded user scope, attaches through `codex --remote unix://`,
and explicitly selects `gpt-6-astra`. `codex-desktop resume THREAD_UUID
WORKING_DIRECTORY` accepts only a UUID and passes that exact identifier to
`resume`; there is no picker, list, name, or latest-session fallback. `status`
and `restart-service` address only the existing
`codex-remote-control.service`. The matching Niri rule focuses the new desktop
window.

The artifact gateway is a reusable HTTPS package and Home module. It accepts
only `GET /v1/artifacts/{opaqueArtifactId}` on the standard IPv4 or IPv6
Tailnet ranges and forwards `Authorization: Capability <opaqueToken>` to a
configured Unix HTTP broker. It has no filesystem-path or upload route, does
not log artifact request targets, bounds broker responses, and forwards only
status, content type, and body. The broker remains responsible for capability
scope, audience, resource, expiry, and revocation decisions from its trusted
peer identity. The gateway service is disabled by default and cannot evaluate
enabled without an explicit Tailnet address, TLS certificate, TLS private key,
and broker socket.

The synthetic launcher check exercised the exact fresh, resume, status, and
restart argv and rejected `resume latest`. The gateway check exercised the
Unix HTTP request, capability header, opaque artifact route, path and upload
rejection, and standard Tailnet address restriction. The module check observed
that the service is absent by default and hardened when fully configured. All
three focused Nix checks evaluated and built through the configured remote
builder. A fourth check pins Plannotator origin commit `013912e008ff`, starts
its actual synthetic capability broker on a Unix socket, retrieves the exact
synthetic artifact through the gateway, and proves an invalid capability does
not return it; that check also built through the remote builder. An independent
flow reran the four Python gateway cases and separately witnessed rejection of
a public bind address.

No Codex session, service restart, phone enrollment, phone round trip, or
private-artifact request was performed. The installed Codex package and live
service are both 0.153.3; the earlier 0.153.4 observation was historical, so no
upgrade was needed to repair a version mismatch. After the deployment attempt,
the service remained active with PID 2316 and invocation
`ab4fbb3002334e908462c354cd75ffe0`.

The gateway cannot be activated yet: no actual Tailnet address, certificate,
private key, or production broker socket is present in the declarative Home
configuration. The present Headscale controller source generates a self-signed
leaf certificate at runtime. The Tailnet client source enables `tailscaled`
but projects no controller CA or certificate into the system trust store.
Secure activation therefore requires a scoped declarative source for a trusted
CA plus the controller certificate/private-key provisioning, followed by
client enrollment. A public repository cannot synthesize that private key, and
trusting an arbitrary runtime self-signed endpoint would remove the TLS
identity property the transport needs.

The HTTPS route is currently an authenticated API surface rather than an
ordinary browser flow. A direct browser navigation cannot attach
`Authorization: Capability`, and the gateway has no login, HttpOnly session,
or credential-custody UI. Scripted clients and browser code that already holds
a scoped token can send the header, but that does not provide a safe way for a
person to acquire or retain it. A later browser surface must exchange a scoped
capability for a secure same-site HttpOnly session, or use another isolated
credential holder, without placing capabilities in URLs or request logs.

The public Horizon proposal supplies node `ouranos`, user `li`, internal suffix
`goldragon.criome.net`, and the node SSH host key. It establishes the canonical
pair `ssh-ng://li@ouranos.goldragon.criome.net` and
`li@ouranos.goldragon.criome.net`. DNS resolved that name to the proposal IPv6,
and strict host-key probes with the proposal key and the already configured SSH
agent authenticated both `li` and `root`. No private key material was read.

CriomOS commit `31e222da1428` pinned the tested Home implementation. Lojix
deployment 239 realized its exact materialized Home activation package and
terminally succeeded without mutation. Deployment 240 then attempted the same
immutable source with `SetProfile`, but terminally failed at `CopyClosure` with
`BuilderUnreachable`; `codex-desktop` remains absent from the live profile.

That attempt exposed an independent Lojix contract defect. The 0.20.3 runtime
rewrote every request-owned Nix store login to `root`, contrary to its public
verbatim-transport contract. A red remote integration check witnessed both
synthetic UserEnvironment routes being rewritten. Lojix 0.21.1 commit
`cf231859d689` removes the rewrite and preserves the exact supplied URI; its
remote test, formatting, and clippy checks pass. CriomOS commits
`8052d62cc644`, `c872fd1e637b`, `3070a49d03a3`, and `efe70c14be98` pin that
producer, document the breaking crossing, and configure a distinct v5 store
so the existing v4 bytes are not reset or overwritten.

CompleteHost deployment 241 terminally realized the pin-only candidate, and
deployment 242 terminally realized final CriomOS commit `efe70c14be98` through
the configured remote builder. Both were build-only: neither copied a closure
to the target nor ran system activation.

This repair is not live. Lojix 0.21 replaces both socket contracts and cannot
open the v4 store. The distinct v5 path preserves the old bytes but starts an
empty active ledger with no v4 current generation, jobs, or event history. A
self-targeted activation submitted to the v4 daemon cannot be terminally
adopted by the new v5 daemon after the service restarts. The candidate may be
realized, but activation requires a documented migration/adoption mechanism or
explicit approval of that active-state discontinuity plus an externally
observable, continuity-independent crossing. No daemon, system profile,
app-server, or Home profile was activated here.

## Sources

- CriomOS-home commits `6fb30e0f1441` and `9548d7d353dd` and their focused Nix checks.
- Plannotator origin commit `013912e008ff`.
- Lojix commit `cf231859d689` and its remote Rust checks.
- CriomOS commits `31e222da1428`, `8052d62cc644`, `c872fd1e637b`,
  `3070a49d03a3`, and `efe70c14be98`.
- Public deployment source `/git/github.com/LiGoldragon/goldragon/proposal.datom`.
- `flows/564f55/reports/codexLaunch.md`, authorized operational reference.
- `flows/219191/log.md`, authorized operational reference.
- `flows/bc3530/log.md`, authorized operational reference.
- CriomOS `modules/nixos/network/headscale.nix` and
  `modules/nixos/network/tailscale.nix`.
- Lojix deployments 239–242 and their typed observations in this flow.
