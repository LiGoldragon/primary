# Witness -- Ouranos host and user environment deployed from CriomOS 07d2cf95

Flow 7dc7cc. Method: direct execution of Lojix owner and ordinary requests
from ouranos against its own sockets, and direct filesystem inspection on
ouranos. Every reply and file listing below is quoted from actual output.

Target line:

- CriomOS main = `07d2cf95abb34d32d0305abefd2cb096137ab412`
- CriomOS-home pinned at `2c4975027af1a3fd9d1da3a2c86e4b195c0b0472`

Both confirmed at origin before deployment:

```
cd /git/github.com/LiGoldragon/CriomOS && git rev-parse origin/main
07d2cf95abb34d32d0305abefd2cb096137ab412
```

Proposal source: regular file `/git/github.com/LiGoldragon/goldragon/proposal.datom`.

## 1. Node identity check

```
hostname
ouranos

getent hosts ouranos.goldragon.criome
201:6de1:5500:7cac:2db9:759e:42d2:fb1d ouranos.goldragon.criome

ip addr show | grep 201:6de1
    inet6 201:6de1:5500:7cac:2db9:759e:42d2:fb1d/7 scope global
```

The logical node (goldragon/ouranos) and the activation destination
(ouranos.goldragon.criome) identify the same machine -- this one. Proceeded.

## 2. Pre-deployment state

System: generation 179, store path `62a1y03jdl1pc0cbdf4xw52a2cahziax-nixos-system-ouranos-26.11.20260813.0e251e2`.

User HM profile: `wzwhrk42i4iimd1xmhi84xxkm300xgad-home-manager-generation`.

Lojix Current before deployment:
- CompleteHost generation 138, artifact `sd0h59z66mggbqnnd5r8am5ai3hbbd34-nixos-system-ouranos`, source `7cd12262874fc5f6c1ed133dc3ef56c669d29959`.
- UserEnvironment generation 204, artifact `wzwhrk42i4iimd1xmhi84xxkm300xgad-home-manager-generation`, source `a66c93816c9a0bbd0660f979b26bb9c552b0e2b0`.

Divergence: Lojix CompleteHost Current (gen 138, `sd0h59z66mgg...`) did not match the live system (gen 179, `62a1y03jdl1p...`). Lojix UserEnvironment Current (gen 204) matched live.

## 3. Deployments through Lojix

All owner requests via `meta-lojix` on `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock`.
All queries via `lojix` on `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock`.

Request template for CompleteHost:

```
R=07d2cf95abb34d32d0305abefd2cb096137ab412
meta-lojix "Deploy.Host.(goldragon ouranos CompleteHost /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=$R (ssh-ng://root@ouranos.goldragon.criome root@ouranos.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 <ACTION> RequireImmutable Some.@/etc/nix/machines [])"
```

Request template for UserEnvironment:

```
R=07d2cf95abb34d32d0305abefd2cb096137ab412
meta-lojix "Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=$R (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 <ACTION> RequireImmutable Some.@/etc/nix/machines [])"
```

| Deployment | Kind | Action | Admission | Terminal |
|---|---|---|---|---|
| 227 | CompleteHost | Realize | `DeployAccepted.(227 (5994 5994))` | `Completed Some.(6010 6010) Some.Succeeded` |
| 228 | CompleteHost | SetBootProfile | `DeployAccepted.(228 (6015 6015))` | `Completed Some.(6048 6048) Some.Succeeded` |
| 229 | CompleteHost | ActivateNow | `DeployAccepted.(229 (6053 6053))` | `Completed Some.(6086 6086) Some.Succeeded` |
| 230 | UserEnvironment | Realize | `DeployAccepted.(230 (6091 6091))` | `Completed Some.(6107 6107) Some.Succeeded` |
| 231 | UserEnvironment | SetProfile | `DeployAccepted.(231 (6112 6112))` | `Completed Some.(6145 6145) Some.Succeeded` |
| 232 | UserEnvironment | ActivateNow | `DeployAccepted.(232 (6150 6150))` | `Completed Some.(6183 6183) Some.Succeeded` |

All six succeeded. SetBootProfile (228) was completed before ActivateNow (229),
so the boot profile was written first -- even if activation had failed, the
machine would boot into the correct generation.

Terminal query replies, verbatim:

```
Queried.([] [(227 227 (HostEnvironment goldragon ouranos CompleteHost Host.Realize LiveActivation RequireImmutable Some.07d2cf95abb34d32d0305abefd2cb096137ab412) Some.(5994 5994) Completed Some.(6010 6010) Some.Succeeded)] (6014 6014))

Queried.([] [(228 228 (HostEnvironment goldragon ouranos CompleteHost Host.SetBootProfile BootProfile RequireImmutable Some.07d2cf95abb34d32d0305abefd2cb096137ab412) Some.(6015 6015) Completed Some.(6048 6048) Some.Succeeded)] (6052 6052))

Queried.([] [(229 229 (HostEnvironment goldragon ouranos CompleteHost Host.ActivateNow LiveActivation RequireImmutable Some.07d2cf95abb34d32d0305abefd2cb096137ab412) Some.(6053 6053) Completed Some.(6086 6086) Some.Succeeded)] (6090 6090))

Queried.([] [(230 230 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.07d2cf95abb34d32d0305abefd2cb096137ab412) Some.(6091 6091) Completed Some.(6107 6107) Some.Succeeded)] (6111 6111))

Queried.([] [(231 231 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.SetProfile ProfileOnly RequireImmutable Some.07d2cf95abb34d32d0305abefd2cb096137ab412) Some.(6112 6112) Completed Some.(6145 6145) Some.Succeeded)] (6149 6149))

Queried.([] [(232 232 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.07d2cf95abb34d32d0305abefd2cb096137ab412) Some.(6150 6150) Completed Some.(6183 6183) Some.Succeeded)] (6187 6187))
```

## 4. Post-deployment state

### System

```
readlink -f /run/current-system
/nix/store/8y15ayy7dhr2gra53rnq3ml39vns8j65-nixos-system-ouranos-26.11.20260813.0e251e2

ls -la /nix/var/nix/profiles/system
lrwxrwxrwx 1 root root 15 Sep  7 02:09 /nix/var/nix/profiles/system -> system-180-link
```

System generation advanced from 179 to 180.

### User environment

```
readlink -f /home/li/.local/state/nix/profiles/home-manager
/nix/store/942sd1dx7rif6y4qmp7lrsrm7rwdv95g-home-manager-generation
```

### Lojix Current after deployment

```
(229 229 goldragon ouranos CompleteHost LiveActivation Current Some./nix/store/8y15ayy7dhr2gra53rnq3ml39vns8j65-nixos-system-ouranos-26.11.20260813.0e251e2 Some.07d2cf95abb34d32d0305abefd2cb096137ab412)
(232 232 goldragon ouranos UserEnvironment LiveActivation Current Some./nix/store/942sd1dx7rif6y4qmp7lrsrm7rwdv95g-home-manager-generation Some.07d2cf95abb34d32d0305abefd2cb096137ab412)
```

Lojix CompleteHost Current artifact matches live `/run/current-system`. Lojix
UserEnvironment Current artifact matches live home-manager profile. Both record
source `07d2cf95abb34d32d0305abefd2cb096137ab412`. The pre-deployment
divergence is closed.

### Embedded home-manager-li.service

```
cat /run/current-system/etc/systemd/system/home-manager-li.service | grep ExecStart
ExecStart=/nix/store/9c1cmravm0i70qpdi82wfjhfkvwv418c-hm-setup-env /nix/store/942sd1dx7rif6y4qmp7lrsrm7rwdv95g-home-manager-generation
```

The system generation 180's embedded home-manager-li.service activates
`942sd1dx7rif6y4qmp7lrsrm7rwdv95g-home-manager-generation`, the same artifact
as the standalone user environment profile. On the next reboot,
home-manager-li.service will activate the correct generation, preventing the
symptom from recurring.

## 5. Verification

### Wispr-status widget

The noctalia config.toml in the HM generation declares:

```toml
[plugins]
enabled = ["criomos/wispr-status", "criomos/listener-level"]

[widget.wispr-status-widget]
type = "criomos/wispr-status:wispr-status-widget"

[bar.main]
end = ["wispr-status-widget", "listener-level", "tray", "battery", "volume", "brightness", "control-center"]
```

Plugin files present in the HM generation at `.local/share/noctalia/plugins/wispr-status/`:
- `BarWidget.luau`
- `plugin.toml`
- `WisprStatusService.luau`
- `WisprStatusState.luau`

Live home directory symlinks were written at 02:09 by the HM activation:

```
ls -la ~/.local/share/noctalia/plugins/wispr-status/
lrwxrwxrwx 1 li users  120 Sep  7 02:09 BarWidget.luau -> /nix/store/3dp2vrswapxjk9whfzdj8b4kmsxav2ky-home-manager-files/...
lrwxrwxrwx 1 li users  117 Sep  7 02:09 plugin.toml -> ...
lrwxrwxrwx 1 li users  129 Sep  7 02:09 WisprStatusService.luau -> ...
lrwxrwxrwx 1 li users  127 Sep  7 02:09 WisprStatusState.luau -> ...
```

The wispr-status widget is declared in the bar config and its plugin files are
on disk and symlinked into the home directory.

### Claude Code

```
claude --version
2.1.263 (Claude Code)

readlink -f $HM/home-path/bin/claude
/nix/store/zh1h1zpcqrh447252d9gcg96h1fygzb5-claude-code-2.1.263/bin/claude
```

### Claude Desktop

```
claude-desktop --version
1.46388.2

readlink -f $HM/home-path/bin/claude-desktop
/nix/store/mr8pj69hq4n8i97jmfwrp12i75xqky1d-claude-desktop-1.46388.2/bin/claude-desktop
```

asar unpack verified:

```
ls -la /nix/store/mr8pj69hq4n8i97jmfwrp12i75xqky1d-claude-desktop-1.46388.2/lib/claude-desktop/resources/app.asar.unpacked/node_modules/node-pty/prebuilds/linux-x64/pty.node
-r--r--r-- 15 root root 84799 Jan  1  1970 .../pty.node
```

### Graphical session and the wispr widget

The running noctalia-shell process (PID 3166) was started at boot
(01:07:44), before this deployment. The home-manager activation at 02:09
wrote the plugin files and config into the home directory, but noctalia was
not restarted by the activation. No `journalctl --user -u 'noctalia*'`
entries appear after 02:10.

Whether noctalia hot-reloads plugins from the changed symlinks is not
established by this witness. The plugin files and config are in place; the
running process predates them. If noctalia does not hot-reload, a new login
is needed for the psyche to see the wispr-status widget in her bar. No
logout, compositor restart, or reboot was performed.

## 6. Constraints observed

- No reboot.
- No compositor restart or forced logout.
- No boot-once scheduled.
- Flow 542442's renovation was not introduced; CriomOS main is the
  rolled-back line plus the Claude Code 2.1.263 bump.
- RequireImmutable was used for all deployments.
- SetBootProfile was completed before ActivateNow for the host.

## Sources

- Lojix ordinary and owner socket replies, quoted verbatim.
- Filesystem inspection on ouranos, quoted verbatim.
- Process listing (`pgrep`, `ps`) on ouranos.
- `journalctl --user` on ouranos.
