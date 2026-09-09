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
upgrade was needed to repair a version mismatch.

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

Declarative activation also remains unsubmitted. Lojix reports a current
ouranos user environment, but the available query does not establish the exact
proposal source, flake reference, transport, and materialized inputs required
to construct a new typed deployment request. Guessing those fields would risk
activating the wrong composition and restarting the shared app-server. The
source and focused remote checks are complete; the live user profile still
lacks `codex-desktop`.

## Sources

- CriomOS-home commits `6fb30e0f1441` and `9548d7d353dd` and their focused Nix checks.
- Plannotator origin commit `013912e008ff`.
- `flows/564f55/reports/codexLaunch.md`, authorized operational reference.
- `flows/219191/log.md`, authorized operational reference.
- `flows/bc3530/log.md`, authorized operational reference.
- CriomOS `modules/nixos/network/headscale.nix` and
  `modules/nixos/network/tailscale.nix`.
- Lojix `Query.ByNode.(goldragon ouranos None)` observation in this flow.
