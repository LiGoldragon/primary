# CriomOS / CriomOS-home Architecture Audit

## Scope

This audit covers the current production checkouts:

- `/git/github.com/LiGoldragon/CriomOS`
- `/git/github.com/LiGoldragon/CriomOS-home`

It also looks at `/git/github.com/LiGoldragon/CriomOS-lib` where the
two repos share constants and static inventory.

The horizon-reengineering worktree is intentionally out of scope except
where it explains a known destination. `system-assistant` is actively
working there.

## Current Architecture

CriomOS is correctly shaped as a network-neutral NixOS target. The
public flake surface is one `nixosConfigurations.target`; concrete
cluster, node, system tuple, deployment shape, and secrets enter through
flake inputs:

- `system` — target platform tuple.
- `pkgs` — the cached package axis.
- `horizon` — projected per-cluster/per-node data.
- `deployment` — operation shape, currently mostly `includeHome`.
- `secrets` — sops files supplied by the cluster repository.

The top module aggregate is `modules/nixos/criomos.nix`. It imports:

- hardware/base normalization: `disks`, `normalize`, `metal`, `edge`;
- deploy/runtime substrate: `nix`, `nspawn`, `secrets`;
- identity/trust bootstrap: `complex`;
- services: `network`, `router`, `llm`;
- users and optional Home Manager bridge: `users`, `userHomes`.

CriomOS-home is correctly split as a standalone Home Manager flake. It
consumes the same `horizon`, `system`, and `pkgs` inputs, and exports
`homeModules.default` plus `homeConfigurations.<user>` for direct
home-only activation. Its wrapper in `flake.nix` imports Stylix, Niri,
and Noctalia before the local modules and forces the correct
CriomOS-home `inputs` through `_module.args`.

The home profile ladder is:

- `min` — shell, desktop base, Niri, Chroma, Whisrs, Noctalia, Pi model
  config.
- `med` — coding tools, Codium, Emacs, Qutebrowser.
- `max` — heavier creative/multimedia/Chrome/OBS surfaces.

`CriomOS-lib` currently carries shared constants and `data/largeAI/llm.json`.
Both CriomOS `llm.nix` and CriomOS-home `pi-models.nix` read that model
inventory.

## Good Signals

Concrete node-name predicates are mostly gone from production Nix. The
audit did not find `node.name == "ouranos"` / `"prometheus"` style
feature gates in CriomOS or CriomOS-home. Remaining node-name use is
mostly identity rendering: hostname, SSH known-host entries, Wi-Fi
identity, and per-user GPG key lookup.

The system/home ownership boundary is much healthier than before:

- Whisrs package, keybindings, tray/bar state, history, and recall live
  in CriomOS-home.
- `/dev/uinput`, groups, and udev rules live in CriomOS.
- Chroma daemon and user-facing visual state live in CriomOS-home.
- dconf service is enabled system-wide only as a runtime prerequisite
  for Home Manager/Stylix activation.

Router Wi-Fi password handling has moved in the right direction.
`modules/nixos/router/default.nix` reads a `SecretReference`-shaped
Horizon field, resolves it through `inputs.secrets.sopsFiles`, and
wires `hostapd.authentication.saePasswordsFile`. The repo has
`checks/router-wifi-secret/default.nix` to prevent reintroducing inline
`saePasswords`.

Architecture truth checks now exist for several load-bearing system
claims:

- `nix-role-policy`
- `nspawn-role-policy`
- `resolver-role-policy`
- `router-wifi-secret`
- `headscale-selfsigned-cert`

CriomOS-home also has useful checks for recent user-critical behavior:

- `whisrs-dictation-bindings`
- `whisrs-recall`
- `whisrs-level-widget`

`nix flake check --no-build` passes in CriomOS-home. Direct
`nix flake check` in CriomOS still stops at the intentional stub boundary
unless a projected `system` and `horizon` are supplied.

## High-Signal Problems

### 1. CriomOS documentation is stale around lojix

`CriomOS/README.md` still describes an old flag/subcommand deploy
surface:

```text
lojix build|eval|deploy --cluster <C> --node <N> --source <C>/datom.nota
```

That conflicts with the current system-specialist rule: lojix-cli accepts
exactly one Nota request record, with no flags and no subcommands. This
is not harmless docs drift; it teaches agents the wrong operator surface.

### 2. CriomOS devshell still assumes the retired `~/git` layout

`CriomOS/devshell.nix` says sibling repos are under `~/git` and creates
symlinks from `$HOME/git/${name}`. The workspace standard is
`/git/<host>/<owner>/<repo>` via `ghq`; `~/git` is retired. The devshell
therefore no longer refreshes the meta-repo symlink farm on this machine.

This is a clear fix: replace the hard-coded `$HOME/git` lookup with the
canonical `/git/github.com/LiGoldragon/<repo>` paths or a small ghq-based
resolver.

### 3. `modules/nixos/chroma.nix` is compatibility scaffolding

The file exists only to retain `/run/chroma` and group `chroma` for old
Home Manager generations. The current Chroma uses the per-user
`$XDG_RUNTIME_DIR/chroma.sock`.

That retention conflicts with the workspace's current "no backward
compatibility for systems being born" discipline and with the previous
Chroma hard constraint that old apply/socket paths are not retained.
After confirming no active generation points at `/run/chroma`, this
module should be deleted and removed from `modules/nixos/criomos.nix`.

### 4. Router Wi-Fi still contains hard-coded site policy

`modules/nixos/router/default.nix` hard-codes:

- `countryCode = "PL"`
- `ssid = "criome"`

The password is now secret-managed, but the radio/regulatory policy and
SSID are still engine-side literals. The country code especially is not
a CriomOS constant; it is deployment/site truth and should come from
Horizon or a site/cluster policy record.

### 5. Wi-Fi PKI is scaffolded, not architecture-complete

The current EAP-TLS path expects manually placed certificate files:

- router server key under the Wi-Fi server path;
- client certificate under the Wi-Fi PKI cert directory;
- NetworkManager connection written by a oneshot service.

That is useful migration scaffolding, but it is not the intended
Clavifaber + Horizon flow yet. The missing pieces are:

- Horizon data naming Wi-Fi SSID, country/regulatory policy, CA/public
  cert material, and per-node client cert publication state.
- Clavifaber producing or publishing the certificate material through
  typed verbs.
- Tests proving router and client modules consume the Horizon/Clavifaber
  path rather than manual files.

### 6. `network/wireguard.nix` has a likely latent bug

The untrusted-proxy mapper takes an argument named `untrustedProxy` but
then inherits `publicKey` and `endpoint` from `wireguardUntrustedProxies`,
which is the list, not the element:

```nix
mkUntrustedProxy = untrustedProxy: {
  inherit (wireguardUntrustedProxies) publicKey endpoint;
  allowedIPs = [ "0.0.0.0/0" ];
};
```

If this path is ever exercised with a non-empty proxy list, it should
fail or evaluate incorrectly. Since WireGuard may not be in use, the
right next step is either delete/retire the module or fix this with a
role-policy check that includes an untrusted proxy fixture.

### 7. NordVPN key handling is still manual and split awkwardly

CriomOS system code expects `/etc/nordvpn/privateKey`; CriomOS-home ships
a `nordvpn-seed` helper that pulls from gopass and writes that system
path. That crosses the system/home boundary in a way the architecture is
trying to remove.

This should move to the same pattern as router Wi-Fi:

- a Horizon `SecretReference`;
- sops-nix materialization on the system side;
- no home-profile tool writing `/etc`.

### 8. CriomOS-lib lacks the normal repo architecture files

`CriomOS-lib` is an active flake input carrying constants and shared
static data, but it has no root `ARCHITECTURE.md` or `skills.md`. Its
`AGENTS.md` also says long-form architecture docs go in consuming repos,
which conflicts with the workspace-level canonical rule that every
canonical repo carries an `ARCHITECTURE.md`.

Because CriomOS-lib is small, the fix can be small: one architecture
file that states "shared constants and static cross-repo data only; no
nixpkgs dependency; no host-specific secrets; no one-consumer data."

### 9. Home docs understate the current implementation

`CriomOS-home/README.md` still says status is "scaffold"; the roadmap
still says modules are verbatim legacy copies and references a stale
`/home/li/git/horizon-rs/docs/DESIGN.md` path. The implementation is
well past that: Chroma, Whisrs safety, Noctalia, HeXis, Codium, and Pi
model plumbing are live.

This doc drift is agent-risky because it makes a future agent treat live
modules as scaffolding.

### 10. Architecture docs still use brittle HTTPS cross-repo links

Both repos still have permanent docs with direct GitHub links where the
workspace contract prefers repo-name prose or `github:<owner>/<repo>`.
Examples:

- `CriomOS/ARCHITECTURE.md` links to `lojix-cli` by HTTPS.
- `CriomOS-home/ARCHITECTURE.md` links to CriomOS and CriomOS-emacs by
  HTTPS.
- both READMEs use several HTTPS repo links.

This is lower operational risk than the items above, but it is a
standing architecture-doc hygiene violation.

## Medium-Risk Shape Debt

`modules/nixos/metal/default.nix` is too broad. It owns battery,
graphics, firmware, kernel modules, model quirks, geoclue, lock before
sleep, udev, input, virtualization, printing, and audio button handling.
The logic is mostly role/gate driven, but the file has become the
hardware-monolith. The clean split is likely:

- `metal/hardware-models.nix`
- `metal/power.nix`
- `metal/input.nix`
- `metal/graphics.nix`
- `metal/desktop-prerequisites.nix`

The split should preserve existing Horizon gates and add checks around
the high-risk policies: all-firmware, model-specific kernel modules, and
edge-only uinput.

`headscale.nix` and `tailscale.nix` are phase-1 surfaces. Headscale uses
a self-signed cert generator; Tailscale client enrollment remains manual.
That is acceptable only if treated as scaffolding toward a typed
tailnet/headscale role design. It should not become permanent hidden
trust architecture.

`llm.nix` and `pi-models.nix` still read model inventory from
CriomOS-lib JSON. Li has already accepted that open-source model
inventory is less cluster-specific than secrets, so this is not as bad
as Wi-Fi passwords in Nix. Still, endpoint/provider availability is
cluster topology and should remain Horizon-owned. The reengineering
branch appears to be moving this toward `horizon.cluster.aiProviders`;
production should not deepen the JSON inventory path.

Stylix theme sources are still Base16 YAML files in
`modules/home/visual-theme.nix`. That is probably acceptable as an
adapter to Stylix, but if "no YAML inputs" is meant workspace-wide
rather than Chroma-only, this is a known exception that needs either a
conversion plan or an explicit carve-out.

## Testing Gaps

The existing checks are useful but mostly source/eval witnesses. Missing
architecture witnesses:

- No test proves CriomOS has no concrete cluster node predicates outside
  test fixtures.
- No test proves `devshell.nix` uses the `/git/...` ghq layout.
- No test proves Chroma legacy socket support is absent.
- No test proves router Wi-Fi country/SSID come from Horizon rather than
  literals.
- No test exercises WireGuard untrusted proxy configuration.
- No test proves NordVPN private key comes from sops rather than manual
  `/etc` seeding.
- No test exercises the Clavifaber Wi-Fi PKI path end to end.
- No projected-input smoke test exists in this repo for a fake full
  `nixosConfigurations.target` evaluation; direct `flake check` stops
  at the intentional `system`/`horizon` stubs.

The right testing direction is a small `CriomOS-test-cluster` fixture
that supplies projected Horizon + system + secrets flakes, then runs
named Nix checks against production CriomOS and CriomOS-home inputs.
The existing BEADS items for test-cluster negative fixtures, nspawn/DNS
smokes, and Wi-Fi PKI are aligned with this need.

## Recommended Next Moves

1. Fix stale docs that can actively mislead agents:
   - update `CriomOS/README.md` to the Nota-record lojix surface;
   - update `CriomOS-home/README.md` and roadmap status.

2. Fix the production meta-repo devshell:
   - replace `$HOME/git` with `/git/github.com/LiGoldragon/<repo>` or
     ghq resolution.

3. Delete the Chroma legacy system module once runtime confirms no active
   generation uses `/run/chroma`.

4. Move router `countryCode` and `ssid` into Horizon/site policy, then add
   a check that fails if `router/default.nix` contains those literals.

5. Decide WireGuard's fate:
   - if unused, retire the module and close the audit bead;
   - if kept, fix `mkUntrustedProxy` and add a fixture check.

6. Move NordVPN private key handling to sops-nix with a Horizon
   `SecretReference`.

7. Give CriomOS-lib a tiny `ARCHITECTURE.md` and `skills.md`, or record an
   explicit workspace-level exception for dependency-free constants flakes.

