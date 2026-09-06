# Zeus CriomOS Deployment Witness

Observed by flow 0384e0, 2026-09-06.
Method: direct SSH verification and Lojix query against live state.

## Transport Verification

```
$ ssh -o StrictHostKeyChecking=yes -o BatchMode=yes root@zeus.goldragon.criome echo 'SSH_OK'
SSH_OK

$ nix store info --store ssh-ng://root@zeus.goldragon.criome
Store URL: ssh-ng://root@zeus.goldragon.criome
Version: 2.35.1
Trusted: 1

$ ssh root@zeus.goldragon.criome hostname
zeus

$ ssh root@zeus.goldragon.criome 'df -h /nix/store'
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  468G  408G   37G  92% /nix/store
```

## Deployment Requests and Replies

### Evaluate (Deployment 205)

Request:
```
Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 Evaluate RequireImmutable Some.@/etc/nix/machines [])
```

Reply:
```
DeployAccepted.(205 (5388 5388))
```

Terminal record:
```
(205 205 (HostEnvironment goldragon zeus CompleteHost Host.Evaluate LiveActivation RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5388 5388) Completed Some.(5403 5403) Some.Succeeded)
```

### Realize (Deployment 206)

Request:
```
Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 Realize RequireImmutable Some.@/etc/nix/machines [])
```

Reply:
```
DeployAccepted.(206 (5408 5408))
```

Terminal record:
```
(206 206 (HostEnvironment goldragon zeus CompleteHost Host.Realize LiveActivation RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5408 5408) Completed Some.(5424 5424) Some.Succeeded)
```

### ActivateNow (Deployment 207)

Request:
```
Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=57ec0138e28d2c389a8d7d4d4424e6840af5acc0 (ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])
```

Reply:
```
DeployAccepted.(207 (5429 5429))
```

Terminal record:
```
(207 207 (HostEnvironment goldragon zeus CompleteHost Host.ActivateNow LiveActivation RequireImmutable Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0) Some.(5429 5429) Completed Some.(5462 5462) Some.Succeeded)
```

## Boot Profile Persistence

ActivateNow wrote the boot profile. No separate SetBootProfile was needed.

```
$ bootctl list | head -8
         type: Boot Loader Specification Type #1 (.conf)
        title: NixOS (Generation 72 NixOS Zokor 26.11.20260813.0e251e2 (Linux 7.1.8), built on 2026-09-06) (default) (not reported/new)
           id: nixos-98bdfcb76427c30de9057d23bdd5734372aae11df95ba1bf95dbc0585ba2be05.conf
       source: /boot//loader/entries/nixos-98bdfcb76427c30de9057d23bdd5734372aae11df95ba1bf95dbc0585ba2be05.conf (on the EFI System Partition)
     sort-key: nixos
      version: Generation 72 NixOS Zokor 26.11.20260813.0e251e2 (Linux 7.1.8), built on 2026-09-06
   machine-id: c3d2385e2078489cb60b558135493b78
        linux: /boot//EFI/nixos/wqqv4n961xfskl4k03mwagj5g8ahh13k-linux-7.1.8-bzImage.efi
```

Boot entry init path: `init=/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2/init`

## Live Verification (independent of Lojix)

```
$ readlink /run/current-system
/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2

$ readlink /nix/var/nix/profiles/system
system-72-link

$ ls -la /nix/var/nix/profiles/system-72-link
lrwxrwxrwx 1 root root 84 Sep  6 14:47 /nix/var/nix/profiles/system-72-link -> /nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2

$ cat /run/current-system/nixos-version
26.11.20260813.0e251e2
```

## Lojix State vs Live State

Lojix Current generation for Zeus CompleteHost:
```
(207 207 goldragon zeus CompleteHost LiveActivation Current Some./nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2 Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0)
```

Live state on Zeus:
- `/run/current-system` -> `/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2`
- System profile: `system-72-link` -> same store path
- Default boot entry: Generation 72 -> same store path

**Lojix state and live state agree.**

## Activation-Critical Units

```
$ systemctl status complex-init.service
● complex-init.service - Clavifaber publication assembly
     Loaded: loaded (/etc/systemd/system/complex-init.service; enabled; preset: ignored)
     Active: active (exited) since Fri 2026-08-28 15:11:56 CEST; 1 week 1 day ago
   Main PID: 1227 (code=exited, status=0/SUCCESS)
```

No failed units on Zeus after activation (`systemctl list-units --state=failed` returned empty).

## User Environment State (not changed by this deployment)

- bird: `home-manager-31-link` (Lojix generation 167, Current)
- li: `home-manager-28-link` (Lojix generation 49, Current)

Neither was redeployed. This flow's scope is the host only.
