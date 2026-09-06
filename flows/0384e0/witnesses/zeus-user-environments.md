# Zeus User Environment Deployment Witness

Observed by subflow thread on 2026-09-06. Method: direct Lojix
deployment requests, SSH transport verification, and live profile
inspection on Zeus.

## Step 1 — Revision Decision

CriomOS `57ec0138e28d2c389a8d7d4d4424e6840af5acc0` is live on Zeus as
generation 207. Its `flake.lock` pins CriomOS-home
`08717ef8950e514c346cbdfbc69143e4369056fb`. The CriomOS-home tip
`654144d71a51f92bba56e405faab3243e2dce4ba` is 7 commits ahead, introducing
`lib/horizon-user.nix` from commit `b12e3dc` onward. That file depends on
Horizon user-vector plumbing that exists only on the unmerged branch
`origin/horizon-flake-integration-542442`, not on CriomOS main. CriomOS
`57ec0138` overrides `criomos-home.inputs.horizon.follows = "horizon"` to
an empty stub (`./stubs/no-horizon`, exporting `{ horizon.users = { }; }`).

Deployed revision: CriomOS umbrella
`57ec0138e28d2c389a8d7d4d4424e6840af5acc0` (which pins CriomOS-home
`08717ef8950e`), using the CriomOS-level `homeConfigurations` output. This
matches the host that is now live on Zeus.

### Prior generation source revisions

- **bird** gen 167: CriomOS `eefa86f117ee173670b82b49f1a60e86b94fac27`,
  which pins CriomOS-home `9c8ded53d56f8a24f1e90a5339678aa585bbaa03` — 25
  CriomOS-home commits behind `08717ef8950e`, 21 CriomOS commits behind
  `57ec0138`.
- **li** gen 49: source `756ce723ea7f1a58d20e2b6f153f15e30aa9b885`
  (CriomOS-home directly, not CriomOS umbrella) — 155 CriomOS-home commits
  behind `08717ef8950e`.

## Step 2 — Transport Verification

### li

SSH as li to zeus.goldragon.criome:

```
$ ssh -o BatchMode=yes li@zeus.goldragon.criome 'hostname && uname -n'
zeus
zeus
```

Nix store info:

```
$ nix store info --store 'ssh-ng://li@zeus.goldragon.criome'
Store URL: ssh-ng://li@zeus.goldragon.criome
Version: 2.35.1
Trusted: 1
```

Far side is `zeus`. Logical node and activation destination agree. Transport
proven.

### bird

SSH as bird to zeus.goldragon.criome:

```
$ ssh -o BatchMode=yes bird@zeus.goldragon.criome 'hostname'
bird@zeus.goldragon.criome: Permission denied (publickey,keyboard-interactive).
```

Nix store info:

```
$ nix store info --store 'ssh-ng://bird@zeus.goldragon.criome'
Store URL: ssh-ng://bird@zeus.goldragon.criome
bird@zeus.goldragon.criome: Permission denied (publickey,keyboard-interactive).
error: failed to start SSH connection to 'zeus.goldragon.criome'
```

Root cause: Lojix daemon runs as user `li` on ouranos (`User=li` in
`lojix-daemon.service`). Li's SSH agent provides one key:
`ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHEtxRF2wjSD1DzlYCW9BivOsz9X0P95msrbXvGATy/p`.
This key is in li's `authorized_keys` on zeus but NOT in bird's. Bird's
`authorized_keys` on zeus (`/etc/ssh/authorized_keys.d/bird`) contains two
different keys:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGhaPt/4ytqbJ9oPk5DE5WEK23N36pZRbvaEuqr/MtfF
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMioAruS5HbgT8hUOVAgKKUP0P6s4gXliVb+AcrtWr4V
```

Neither matches li's key. Transport NOT proven. Bird's user-scoped
deployment cannot proceed.

## Step 3 — Deployment

### li — Realize (deployment 208)

Request:

```
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon zeus li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://li@zeus.goldragon.criome li@zeus.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable Some.@/etc/nix/machines [])'
```

Reply:

```
DeployAccepted.(208 (5467 5467))
```

Terminal record:

```
Queried.([] [(208 208 (UserEnvironment.li goldragon zeus UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5467 5467) Completed Some.(5483 5483) Some.Succeeded)] (5487 5487))
```

### li — SetProfile (deployment 209)

Request:

```
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon zeus li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://li@zeus.goldragon.criome li@zeus.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 SetProfile RequireImmutable Some.@/etc/nix/machines [])'
```

Reply:

```
DeployAccepted.(209 (5488 5488))
```

Terminal record:

```
Queried.([] [(209 209 (UserEnvironment.li goldragon zeus UserEnvironment UserEnvironment.SetProfile ProfileOnly RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5488 5488) Completed Some.(5521 5521) Some.Succeeded)] (5525 5525))
```

### li — ActivateNow (deployment 210)

Request:

```
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon zeus li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://li@zeus.goldragon.criome li@zeus.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

Reply:

```
DeployAccepted.(210 (5526 5526))
```

Terminal record:

```
Queried.([] [(210 210 (UserEnvironment.li goldragon zeus UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5526 5526) Completed Some.(5559 5559) Some.Succeeded)] (5563 5563))
```

### bird — Realize (deployment 211)

Request:

```
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon zeus bird /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://bird@zeus.goldragon.criome bird@zeus.goldragon.criome) Horizon (homeConfigurations.bird.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable Some.@/etc/nix/machines [])'
```

Reply:

```
DeployAccepted.(211 (5564 5564))
```

Terminal record:

```
Queried.([] [(211 211 (UserEnvironment.bird goldragon zeus UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5564 5564) Completed Some.(5580 5580) Some.Succeeded)] (5584 5584))
```

Realize succeeded — the build does not require target SSH.

### bird — SetProfile (deployment 212) — FAILED

Request:

```
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon zeus bird /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://bird@zeus.goldragon.criome bird@zeus.goldragon.criome) Horizon (homeConfigurations.bird.activationPackage) HomeManagerNixProfileV1 SetProfile RequireImmutable Some.@/etc/nix/machines [])'
```

Reply:

```
DeployAccepted.(212 (5585 5585))
```

Terminal record:

```
Queried.([] [(212 212 (UserEnvironment.bird goldragon zeus UserEnvironment UserEnvironment.SetProfile ProfileOnly RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5585 5585) Failed Some.(5609 5609) Some.Failed.(Activate ActivationFailed))] (5613 5613))
```

**Failed at Activate stage: ActivationFailed.** SSH as bird to
zeus.goldragon.criome is not authenticated for li's SSH key, which is the
only key available to the Lojix daemon.

### bird — ActivateNow (deployment 213) — FAILED

Request:

```
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon zeus bird /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://bird@zeus.goldragon.criome bird@zeus.goldragon.criome) Horizon (homeConfigurations.bird.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

Reply:

```
DeployAccepted.(213 (5614 5614))
```

Terminal record:

```
Queried.([] [(213 213 (UserEnvironment.bird goldragon zeus UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5614 5614) Failed Some.(5638 5638) Some.Failed.(Activate ActivationFailed))] (5642 5642))
```

**Failed at Activate stage: ActivationFailed.** Same root cause as
deployment 212.

## Step 4 — Refresh

### li

SSH as li to zeus, ran `systemctl --user daemon-reload`:

```
$ ssh li@zeus.goldragon.criome 'systemctl --user daemon-reload'
(success, exit 0)
```

Systemd picked up the new unit files from the activated home-manager
generation.

### bird

Bird's deployment failed. No new environment was installed to refresh.
Bird's profile remains at `home-manager-31-link` pointing to
`/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation`
(Lojix gen 167, CriomOS `eefa86f1`).

## Step 5 — Live Verification

### li — Lojix state

Generation 210, UserEnvironment, LiveActivation, Current. Source revision
`57ec0138e28d2c389a8d7d4d4424e6840af5acc0`. Store path
`/nix/store/b5rdn1kjbqc6304q3r0jbxfv4rxbr869-home-manager-generation`.

### li — Live state on Zeus

```
$ ssh li@zeus.goldragon.criome 'readlink ~/.local/state/nix/profiles/home-manager'
home-manager-29-link

$ ssh li@zeus.goldragon.criome 'readlink ~/.local/state/nix/profiles/home-manager-29-link'
/nix/store/b5rdn1kjbqc6304q3r0jbxfv4rxbr869-home-manager-generation

$ ssh li@zeus.goldragon.criome 'readlink -f ~/.local/state/nix/profiles/home-manager'
/nix/store/b5rdn1kjbqc6304q3r0jbxfv4rxbr869-home-manager-generation
```

**Lojix and live state agree.** Profile `home-manager-29-link`, store path
`b5rdn1kjbqc6304q3r0jbxfv4rxbr869`, source `57ec0138`. A fresh login gets
this generation.

### bird — Lojix state

Generation 167, UserEnvironment, LiveActivation, Current (unchanged).
Source revision `eefa86f117ee173670b82b49f1a60e86b94fac27`. Store path
`/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation`.

### bird — Live state on Zeus

```
$ ssh root@zeus.goldragon.criome 'readlink /home/bird/.local/state/nix/profiles/home-manager'
home-manager-31-link

$ ssh root@zeus.goldragon.criome 'readlink /home/bird/.local/state/nix/profiles/home-manager-31-link'
/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation

$ ssh root@zeus.goldragon.criome 'readlink -f /home/bird/.local/state/nix/profiles/home-manager'
/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation
```

**Lojix and live state agree** (both reflect the old generation). Profile
`home-manager-31-link`, store path `dhwq1j6ndp5kh47nqasmfblv2w93h82d`,
source `eefa86f1`. Bird was NOT updated.

## Noctalia Shell Reload

Bird's deployment failed. The Noctalia binary in bird's current profile is:

```
/nix/store/dr2v7rd4himys11hmlq54ng0jwvqyb0c-noctalia-5.1.0/bin/noctalia
```

This is from the old generation (gen 167, CriomOS `eefa86f1`). The new
CriomOS-home commits between `9c8ded53` and `08717ef8950e` include:

- `6f71a8b` Add Noctalia Wispr status consumer
- `1fe5cb6` Separate Wispr Noctalia entry identifiers
- `976ab3c` Preload managed Noctalia plugins
- `4d29776` Test Noctalia plugin-state reconciliation
- `d9bec96` Adopt Wispr status v2 microphone meter
- `b692b52` Harden Wispr status freshness checks
- `3f58325` Pin Wispr meter handler repair
- `0b56376` Pin repaired Wispr control bridge
- `adc53c3` Deploy Wispr reconnect without Codex upgrade
- `9d39e2e` Increase Wispr meter visibility for quiet speech
- `3c08f1c` Correct Wispr meter clipping expectations

These changes are NOT installed in bird's profile on Zeus because bird's
SetProfile and ActivateNow deployments both failed. Reloading Noctalia
would restart the same old binary from the same old store path. The new
status bar functionality (Wispr status v2 microphone meter, visibility
improvements, plugin preloading) cannot be made live until bird's
user-environment deployment succeeds.

**Not reloaded.** Reloading would achieve only a process restart of the old
version — it cannot deliver the new status bar functionality the psyche
asked for. The old Noctalia is still running and functional; restarting it
risks disrupting bird's live session for no gain.

## Summary

| User | Outcome | Lojix gen | Profile link | Source revision |
|------|---------|-----------|--------------|-----------------|
| li | Succeeded | 210 | home-manager-29-link | 57ec0138 |
| bird | Failed | 167 (unchanged) | home-manager-31-link | eefa86f1 (unchanged) |

### Blocker for bird

Li's SSH key (the only key available to the Lojix daemon, which runs as
user `li`) is not in bird's `authorized_keys` on Zeus. The user-scoped
transport `ssh-ng://bird@zeus.goldragon.criome` cannot authenticate. Bird's
`authorized_keys` on Zeus contains two keys, neither of which matches li's
agent key.

Resolution requires adding li's SSH public key to bird's `authorized_keys`
in the CriomOS NixOS configuration and redeploying the host, or providing a
separate SSH identity that matches one of bird's existing authorized keys.
