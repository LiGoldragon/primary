# 0384e0 — Deploy the latest CriomOS to Zeus

Psyche's request: get the latest version of CriomOS deployed to Zeus on the
cluster; remember past flows that did this recently for direction and to avoid
past mistakes; propose a skill edit at the end.

Remembered: past Zeus deployment flows — depth 1
(01a02b46, 01a030b7, 01a02fe5, 01a05833, 01a05cd5, 966be8, 5a3ee4, acf06f).

## Established by subflow

- Target: cluster `goldragon`, node `zeus`, composition `CompleteHost`.
- Current live: generation 181, deployment 181, `Host.ActivateNow`
  `LiveActivation` `Succeeded`, source revision `59d12e6f`.
- Daemon active on Ouranos; `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock`,
  `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock`; both clients decode inline Dotos.
- Proposal source: `/git/github.com/LiGoldragon/goldragon/proposal.datom`.
- Transport: `(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)`.
  The psyche's 2026-08-24 Ethernet preference for `192.168.18.95` is superseded
  by later evidence — Zeus left that LAN; five deployments failed
  `Failed.(CopyClosure BuilderUnreachable)` on the stale address.

## Past mistakes to avoid

- Stale LAN IP in the transport → `Failed.(CopyClosure BuilderUnreachable)`.
  Lojix maps every CopyClosure failure to that reason and discards real stderr.
- Slash flake form `github:Owner/Repo/<sha>` → `FlakeReferenceMalformed`.
  Accepted form is `github:Owner/Repo?rev=<40-hex>`.
- Legacy parenthesized ClaviFaber syntax in `complex-init.service` →
  `Failed.(Activate ActivationFailed)`.
- Deployment 49: logical node `zeus` with an Ouranos transport installed Zeus
  Home on Ouranos. Verify node and destination identify the same machine.
- `DeployAccepted` is admission only; each action is its own deployment id.

## Pending hazard

Flow 542442 is migrating Lojix from Dotos to Datom syntax. The live daemon
still speaks Dotos and `horizon-definition.datom` does not exist on disk, so
this flow uses the current parenthesized form and `proposal.datom`.

## Outcome

Zeus came back online on the psyche's word. Transport witnessed first — SSH,
`nix store info` over `ssh-ng://root@zeus.goldragon.criome`, and far-side
hostname confirmed `zeus` — then deployed.

Lojix deployments 205 `Evaluate`, 206 `Realize`, 207 `ActivateNow`, each polled
to its own terminal record, all `Some.Succeeded`, all at source revision
`57ec0138e28d2c389a8d7d4d4424e6840af5acc0`.

Lojix Current generation 207. Zeus's own NixOS system profile is generation 72,
`/run/current-system` and `system-72-link` both resolving to
`/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2`.
Default boot entry is generation 72; the boot profile persisted without a
separate `SetBootProfile`. `complex-init.service` active, no failed units. No
reboot needed and none performed.

Live state and Lojix state agree.

## Left open

- The user environments on Zeus are untouched: bird `home-manager-31-link`
  (Lojix generation 167), li `home-manager-28-link` (Lojix generation 49). Host
  scope only, as briefed.
- CriomOS `57ec0138` pins CriomOS-home `08717ef8`, seven commits behind Home's
  tip `654144d7`. Closing that needs the unmerged
  `horizon-flake-integration-542442` branch on main. Not this flow's scope;
  presented to the psyche.
- Skill edit proposed to the psyche: a transport-witness line for the `lojix`
  skill's deployment contract. Awaiting approval.
