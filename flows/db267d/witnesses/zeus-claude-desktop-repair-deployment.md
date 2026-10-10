# Witness — Zeus user-environment deployment repairing bird's Claude Desktop

Flow db267d. Method: direct execution of the commands below from ouranos
(the operator host) against Lojix's sockets and against Zeus over SSH.
Every reply and terminal record below is quoted from the actual output.

## 1. Node identity check (before any state change)

```sh
ssh -o BatchMode=yes root@zeus.goldragon.criome 'hostname; cat /etc/machine-id; readlink -f /run/current-system; ls -l /nix/var/nix/profiles/system; df -h /nix/store | tail -1'
```

```
zeus
c3d2385e2078489cb60b558135493b78
/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2
lrwxrwxrwx 1 root root 14 Sep  6 14:47 /nix/var/nix/profiles/system -> system-72-link
/dev/nvme0n1p2  468G  410G   35G  93% /nix/store
```

`lojix 'Query.ByNode.(goldragon zeus None)'` records generation 207 as the
`Current` `CompleteHost` for logical node `goldragon`/`zeus` with artifact
`/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11...`.
That is byte-identical to the live `/run/current-system` above, so the
logical node and the activation destination identify the same machine.
Proceeded.

Store was at 93% / 35G free throughout; no copy failed for space.

## 2. Advancing the CriomOS pin

Starting point on `origin/main`: `a48f9cb843f7107772b3b5405bdeadfef06fc038`,
pinning CriomOS-home `1ae5da86099e323cda8f79ab239ca4efaa12ce47`.

Orchestrate locks 947 and 948 acquired over `flake.nix`, `flake.lock` and
`checks/lojix-ownership/default.nix`; both released.

First pin, pushed as `1a2ce02b60e334f6e4827ef194b3bf4954d37561`:
`criomos-home.url` and `expectedHomeRevision` advanced `1ae5da86` →
`ceeaaf4272ea6df971eefbefc5bd60907fa6d998`. `nix flake lock --update-input
criomos-home` moved exactly one input and nothing else.

## 3. The pin did not evaluate — and the cause predates it

```sh
meta-lojix 'Deploy.UserEnvironment.(goldragon zeus bird /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=1a2ce02b60e334f6e4827ef194b3bf4954d37561 (ssh-ng://bird@zeus.goldragon.criome bird@zeus.goldragon.criome) Horizon (homeConfigurations.bird.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable Some.@/etc/nix/machines [])'
```

```
DeployAccepted.(214 (5643 5643))
```

Terminal:

```
Queried.([] [(214 214 (UserEnvironment.bird goldragon zeus UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.1a2ce02b60e334f6e4827ef194b3bf4954d37561) Some.(5643 5643) Failed Some.(5671 5671) Some.Failed.(Eval FlakeReferenceMalformed))] (5680 5680))
```

The same request for `li` (deployment 215) failed identically. Lojix
discards eval stderr and maps the stage failure to `FlakeReferenceMalformed`,
so the code is uninformative. `journalctl -u lojix-daemon` carried only
`lojix deploy pipeline effect failed at Eval`.

Reproduced the evaluation by hand using the horizon inputs Lojix had just
materialised in `/var/lib/lojix/generated-inputs/goldragon/zeus/user-environment`:

```sh
nix eval --no-write-lock-file --raw \
  "github:LiGoldragon/CriomOS?rev=1a2ce02b60e334f6e4827ef194b3bf4954d37561#homeConfigurations.bird.activationPackage.drvPath" \
  --override-input horizon path:$G/horizon --override-input system path:$G/system --override-input secrets path:$G/secrets
```

```
       … while evaluating the option `home-manager.users.bird.home.packages':
       error: attribute 'architecture' missing
       at «github:LiGoldragon/CriomOS-home/ceeaaf4272ea…»/modules/home/profiles/min/default.nix:240:20:
          240|     ++ (optionals (node.machine.architecture == "x86_64") [ i7z ]);
```

Re-ran the identical evaluation against `a48f9cb843f7` (the pin that was
already on `origin/main` before this flow touched anything):

```
       error: attribute 'architecture' missing
       at «github:LiGoldragon/CriomOS-home/1ae5da86…»/modules/home/profiles/min/default.nix:240:20:
```

So the breakage is **not** caused by advancing to `ceeaaf4272ea`. It was
introduced by CriomOS-home `8cda3bab9d497b900ccd746e7a5abaf2fa81ebab`
("CriomOS-home: read projected machine architecture", 2026-09-06 00:56),
which changed

```
-    ++ (optionals (node.machine.arch == "x86-64") [ i7z ]);
+    ++ (optionals (node.machine.architecture == "x86_64") [ i7z ]);
```

The projected Horizon node carries no `architecture` field. It carries
`arch`, verbatim from
`/var/lib/lojix/generated-inputs/goldragon/zeus/user-environment/horizon/horizon.json`:

```json
"machine": {"species": "Metal", "arch": "X86_64", "cores": 4, "model": "ThinkPadT14Gen2Intel", …}
```

The old form did not error, but it never matched either (`arch` is
`X86_64`, not `x86-64`). Every user-environment deployment on a real
projection has been dead since `8cda3bab` landed.

## 4. Repair and repin

Orchestrate lock 949 over `modules/home/profiles/min/default.nix`,
released after the edit.

CriomOS-home `fde8a2d2bf743a6d5d990f85a86263b7125593de`
("Flow db267d: read the projected machine arch field Horizon actually emits"):

```
    ++ (optionals (node.machine.arch == "X86_64") [ i7z ]);
```

Orchestrate lock 950; CriomOS `37149c316ad147f25e02e4b9ede42d8edb4724b6`
("Flow db267d: pin CriomOS-home fde8a2d2 …") advances `criomos-home.url`,
`flake.lock` and `expectedHomeRevision` together. Pushed to `origin/main`;
`git log -1 refs/remotes/origin/main` confirms the revision. Both repos
were rebased onto the concurrent subflow's work; nothing was force-pushed.

`checks/lojix-ownership` remains unsatisfiable for the reason the
concurrent subflow reported: root Orchestrate lock `5f016531e765…`, Home
Orchestrate lock `ac8a92666f4a…`, `expectedOrchestrateRevision`
`9585484738ce…`. I confirmed all three values and changed none of them.
Deployment does not evaluate `checks`, so it did not block this work.

## 5. Deployments through Lojix

All requests used the owner socket via `meta-lojix`, with
`R=37149c316ad147f25e02e4b9ede42d8edb4724b6`.

| Deployment | Subject | Action | Terminal |
|---|---|---|---|
| 217 | bird | `Realize` | `Some.Succeeded` |
| 218 | li | `Realize` | `Some.Succeeded` |
| 219 | bird | `SetProfile` | `Some.Failed.(Activate ActivationFailed)` |
| 220 | li | `SetProfile` | `Some.Succeeded` |
| 221 | li | `ActivateNow` | `Some.Succeeded` |

Request form (bird, `Realize`; the others differ only in user, transport
and action):

```sh
meta-lojix "Deploy.UserEnvironment.(goldragon zeus bird /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=$R (ssh-ng://bird@zeus.goldragon.criome bird@zeus.goldragon.criome) Horizon (homeConfigurations.bird.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable Some.@/etc/nix/machines [])"
```

Replies:

```
DeployAccepted.(217 (5700 5700))
Queried.([] [(217 217 (UserEnvironment.bird goldragon zeus UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.37149c316ad147f25e02e4b9ede42d8edb4724b6) Some.(5700 5700) Completed Some.(5716 5716) Some.Succeeded)] (5720 5720))

DeployAccepted.(218 (5721 5721))
Queried.([] [(218 218 (UserEnvironment.li … UserEnvironment.Realize ProfileOnly RequireImmutable Some.37149c31…) Some.(5721 5721) Completed Some.(5753 5753) Some.Succeeded)] (5770 5770))

DeployAccepted.(219 (5735 5735))
Queried.([] [(219 219 (UserEnvironment.bird … UserEnvironment.SetProfile ProfileOnly RequireImmutable Some.37149c31…) Some.(5735 5735) Failed Some.(5766 5766) Some.Failed.(Activate ActivationFailed))] (5770 5770))

DeployAccepted.(220 (5771 5771))
Queried.([] [(220 220 (UserEnvironment.li … UserEnvironment.SetProfile ProfileOnly RequireImmutable Some.37149c31…) Some.(5771 5771) Completed Some.(5804 5804) Some.Succeeded)] (5808 5808))

DeployAccepted.(221 (5809 5809))
Queried.([] [(221 221 (UserEnvironment.li … UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.37149c31…) Some.(5809 5809) Completed Some.(5842 5842) Some.Succeeded)] (5846 5846))
```

### The bird SSH gap, now witnessed rather than hypothesised

```sh
ssh -o BatchMode=yes -o ConnectTimeout=10 bird@zeus.goldragon.criome 'echo BIRD_SSH_OK'
```

```
bird@zeus.goldragon.criome: Permission denied (publickey,keyboard-interactive).
```

`/etc/ssh/authorized_keys.d/bird` holds two keys; `/etc/ssh/authorized_keys.d/li`
holds three; the operator key is in li's file and not in bird's. Lojix
reaches a user environment by SSHing **as that user** with the operator
key, so `SetProfile` and `ActivateNow` for bird cannot succeed, and Lojix
collapses the failure to `Some.Failed.(Activate ActivationFailed)`.
`Realize` succeeds because a build needs no target SSH.

### bird activated by the authorised fallback route

The psyche authorised deploying by whatever route works. The closure
Lojix realised was already present on Zeus. Activation was run as bird
from a root SSH invocation that exits:

```sh
ssh -o BatchMode=yes root@zeus.goldragon.criome 'su -s /bin/sh bird -c "export HOME=/home/bird USER=bird XDG_RUNTIME_DIR=/run/user/1000 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus PATH=/run/current-system/sw/bin:/usr/bin:/bin; /nix/store/7hnqikaqghyd8a5fxdq3778hy933z3ii-home-manager-generation/activate"'
```

It ran to completion — `Activating dconfSettings` … `Activating
updateUserDesktopDatabase`, with `Starting units: chroma-daemon.service,
criomos-ui-priority.service, orchestrate-nexus.service,
set-SSH_AUTH_SOCK.service`. It noted the pre-existing degraded unit
`orchestrate-nexus.service` and continued.

Live result:

```
readlink -f /home/bird/.local/state/nix/profiles/home-manager
/nix/store/7hnqikaqghyd8a5fxdq3778hy933z3ii-home-manager-generation
```

## 6. Lojix state and live state, stated separately

**Lojix state.** li's user environment is deployment/generation 221,
`LiveActivation`, `Some.Succeeded`, at source revision `37149c31…`. bird's
user environment has no successful record at this revision: 219 is
`Failed.(Activate ActivationFailed)`, and Lojix's `Current` for bird's
`UserEnvironment` is still generation 167
(`/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation`,
source `eefa86f117ee…`), left there by flow 0384e0.

**Live state.** bird's home-manager profile is
`/nix/store/7hnqikaqghyd8a5fxdq3778hy933z3ii-home-manager-generation`,
profile links `profile-254-link` and `profile-255-link` written at 17:14.
li's is `/nix/store/aicm5x2lc58k56r22gh9y9hh4k7g0jpc-home-manager-generation`.

**Lojix's ledger and Zeus's live state disagree for bird, and will keep
disagreeing until the operator key is added to bird's authorized keys in
the OS source and bird is redeployed through Lojix.** Nothing in this
witness closes that gap.

## 7. claude-remote-control

Neither new generation carries the unit:

```
ls <bird generation>/home-files/.config/systemd/user/ | grep -i remote  →  codex-remote-control.service
ls <li generation>/home-files/.config/systemd/user/   | grep -i remote  →  codex-remote-control.service
```

For bird:

```sh
su -s /bin/sh bird -c "XDG_RUNTIME_DIR=/run/user/1000 systemctl --user disable --now claude-remote-control.service"
Failed to disable unit: Unit claude-remote-control.service does not exist
```

For li, Zeus reports `User ID 1001 is not logged in or lingering`; li has
no user manager on Zeus, so no unit of hers was running there.

`pgrep -af claude-remote-control` on Zeus matched nothing but the grep
itself. Nothing of that service is running on Zeus for either account.

## 8. Verifying bird's Claude Desktop

Packaging, on the generation bird's profile now points at
(`claude-desktop` resolves to
`/nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2`,
where the broken generation was `y08k9q372w81jyczclkpji77c0rw5ihn`):

- The asar header marks the native module unpacked. Parsing
  `resources/app.asar`'s JSON header gives, for
  `node_modules/node-pty/prebuilds/linux-x64/pty.node`:
  `{'size': 75976, 'unpacked': True, 'integrity': {…}}`. Three entries in
  the header carry `unpacked: true`.
- The file is real on disk:
  `-r--r--r-- 5 root root 84799 … /nix/store/ynk1b2pn8…/lib/claude-desktop/resources/app.asar.unpacked/node_modules/node-pty/prebuilds/linux-x64/pty.node`.
  (The on-disk size exceeds the header's recorded 75976 because Nix
  patchelfs the unpacked copy; asar integrity covers packed content, not
  unpacked files.)

Restart. The old process was PID 5918, running from `y08k9q37…` inside
the transient scope `app-com.anthropic.Claude-5918.scope` — not a unit,
so it was stopped with `kill 5918` after `main.log` was copied aside to
`main.log.pre-db267d`, then relaunched as bird from a root SSH command
that exits:

```sh
ssh … root@zeus 'su -s /bin/sh bird -c "… systemd-run --user --scope --unit=claude-desktop-db267d --setenv=DISPLAY=:0 --setenv=WAYLAND_DISPLAY=wayland-1 --setenv=XDG_SESSION_TYPE=wayland --setenv=XDG_CURRENT_DESKTOP=niri:GNOME --setenv=XDG_RUNTIME_DIR=/run/user/1000 --setenv=HOME=/home/bird --setenv=USER=bird /home/bird/.nix-profile/bin/claude-desktop > /dev/null 2>&1 &"'
```

It came up from the new build:

```
36817 /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/lib/claude-desktop/claude-desktop
```

Log, `/home/bird/.config/Claude/logs/main.log`.

Before (old generation, 15:53):

```
2026-09-06 15:53:04 [error] [CCD] Failed to warm session local_13f7f512-…: [CCD] LOCAL OVERRIDE: declared binary unavailable at /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude … at POn.initLocalBinary (…/y08k9q37…/resources/app.asar/.vite/build/index.chunk-DrnJEXHK.js:13:2233546)
2026-09-06 15:53:05 [info]  [pty-host] at loadNativeModule (…/y08k9q37…/resources/app.asar/node_modules/node-pty/lib/utils.js:36:11)
2026-09-06 15:53:05 [error] [pty-host] worker exited (1) with 1 live PTY(s) before a real spawn ack; backing off 30000ms before refork
```

After (new generation, 17:15):

```
2026-09-06 17:15:15 [info] [CCD] Passing 1 plugin(s) to SDK (skills: 1, remote: 0, local: 0)
2026-09-06 17:15:15 [info] Using Claude Code binary at: /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude
2026-09-06 17:15:15 [info] [CCD] Session local_2a5140ca-f237-4f4c-a94d-990fe889177c warmed successfully in 99ms
```

`grep -a "LOCAL OVERRIDE"` and `grep -a "pty-host"` restricted to lines at
or after `2026-09-06 17:15` return **nothing** — no override failure, no
pty-host worker exit. The same session id `local_2a5140ca-…` that failed
to warm at 15:52 now warms in 99 ms.

Limit of this verification, stated plainly: the pty-host worker forks
lazily on a real PTY spawn, and no PTY had been spawned in the new
process at the time of observation, so the absence of a pty-host crash is
the absence of the old startup crash rather than a positive spawn. I
tried to load `pty.node` directly under the app's own Electron with
`ELECTRON_RUN_AS_NODE=1`; the build's Electron fuses refuse that mode
(`Trace/breakpoint trap (core dumped)`), so that direct proof is not
available from outside the app. What is established: the module is
unpacked in the header, the real file exists at the unpacked path, the
app runs from that build, and the failure that used to appear within one
second of startup no longer appears.

## 9. Root-session verification on Zeus

Every SSH invocation in this witness was a single non-interactive command
that exits; bird was reached only as `su -s /bin/sh bird -c …`. No
interactive shell was opened and no reboot was performed.

Final check, quoted verbatim:

```sh
ssh -o BatchMode=yes root@zeus.goldragon.criome 'echo "=== who ==="; who; echo "(empty = no login sessions)"; echo "=== loginctl list-sessions ==="; loginctl list-sessions'
```

```
=== who ===
(empty = no login sessions)
=== loginctl list-sessions ===
SESSION  UID USER SEAT  LEADER CLASS         TTY  IDLE SINCE
      3 1000 bird seat0 2071   user          tty1 no   -
      4 1000 bird -     2139   manager       -    no   -
     92    0 root -     40794  manager-early -    no   -
     93    0 root -     40841  user          -    no   -

4 sessions listed.
```

`who` is empty: no root login session remains. Sessions 92 and 93 are the
root systemd user manager that each SSH command spawns and tears down —
their LEADER pids were 33316/33371 on an earlier check and 40794/40841 on
this one, i.e. they are recreated per invocation and carry no seat and no
TTY. bird's sessions 3 and 4 are her own tty1 login, untouched.
