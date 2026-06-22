# WebHost Testing Worktree

## Scope

The psyche asked for an operator-owned stable worktree branch from `CriomOS` main for the WebHost system, with emphasis on the testing side. I did not touch the locked `/git/github.com/LiGoldragon/CriomOS` main checkout; I created a separate jj workspace at:

`/home/li/wt/github.com/LiGoldragon/CriomOS/pi-operator-web-host-testing`

Bookmark:

`pi-operator-web-host-testing`

Current pushed head:

`297d7e0f` — `CriomOS: add WebHost fixture template witness`

## Implemented slice

The branch adds an inert-by-default `modules/nixos/web-host.nix` module and imports it from `modules/nixos/criomos.nix`.

The module reads the typed `NodeService::WebHost` payload from `horizon.node.services` using the existing `node-services.nix` helper. With no `WebHost` service, it emits nothing. With sites, it:

- resolves reproducible build-time sources via `flake-input:<name>`;
- renders `MarkdownStatic` sites with Zola inside a Nix derivation;
- serves the resulting immutable artifact through nginx virtual hosts;
- enables ACME TLS and HTTP→HTTPS forcing;
- opens ports 80 and 443;
- sets basic hardening headers and disables nginx server tokens.

Unsupported site sources or renderer variants fail evaluation loudly rather than falling back to runtime fetching or dynamic execution.

## Testing side

The branch adds a named pure check:

`checks.x86_64-linux.web-host-policy`

The check owns a tiny Zola fixture site under `checks/web-host-policy/site/`. It constructs two NixOS configurations directly:

- a base node with no `WebHost` service;
- a WebHost node with one `MarkdownStatic` site sourced from `flake-input:web-host-fixture`.

The check verifies:

- the base node does not enable nginx or open HTTP(S) ports;
- the WebHost node enables nginx;
- nginx server tokens are disabled;
- the virtual host forces SSL and enables ACME;
- ACME email is derived from the served domain;
- ports 80 and 443 are open;
- the Zola-rendered immutable artifact exists and contains the fixture markdown content.

## Validation

Touched-file formatting check passed:

`nix fmt -- --check modules/nixos/web-host.nix modules/nixos/criomos.nix checks/web-host-policy/default.nix flake.nix`

The pure check passed after supplying the synthetic `system` and `horizon` inputs required by CriomOS's default stub discipline:

`nix build --refresh --override-input system path:/tmp/criomos-system-x86_64 --override-input horizon path:/tmp/criomos-horizon-minimal .#checks.x86_64-linux.web-host-policy --no-link`

The branch was committed and pushed before Nix builds, matching CriomOS process discipline.

## Notes

This is not the final doris deployment. It deliberately avoids `goldragon` and live provisioning while system-designer holds the relevant locks. It gives the next phase a stable, test-backed CriomOS-side module branch to integrate with doris's cluster data once those locks clear.
