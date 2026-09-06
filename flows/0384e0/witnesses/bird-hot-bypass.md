# Witness: Bird Hot Bypass Activation

**Method:** SSH as root to `zeus.goldragon.criome`, then `su - bird -c "..."` for all user-scoped commands. No rebuild. Store path sourced from Lojix query.

**Authorization:** Psyche-authorized hot bypass. The declarative source is unchanged; this activation does not survive a future `Realize`+`ActivateNow` cycle that re-deploys over it. The real fix — correcting bird's SSH authorized_keys so Lojix can deploy normally — is still owed.

---

## Step 1 — Query Lojix for deployment 211

```
$ lojix 'Query.ByDeployment.(211)'
Queried.([] [(211 211 (UserEnvironment.bird goldragon zeus UserEnvironment
  UserEnvironment.Realize ProfileOnly RequireImmutable
  Some.57ec0138e28d2c389a8d7d4d4424e6840af5acc0)
  Some.(5564 5564) Completed Some.(5580 5580) Some.Succeeded)] (5642 5642))
```

Deployment 211 is a Realize (ProfileOnly) for bird at CriomOS `57ec0138`. It succeeded. The realized store path was identified by tracing the nix-store referrer of the home-manager-files path already active in bird's dotfiles:

```
$ nix-store --query --referrers /nix/store/vqn3r86ddr7jkw8d9y896k5lh5hjylc2-home-manager-files \
    | grep home-manager-generation
/nix/store/a0f9p0gnsfq23hbbqw885xhmip9qmrn1-home-manager-generation
```

The closure was already present on zeus (deployed by Lojix during the Realize step).

---

## Step 2 — Activate as bird

```
$ ssh root@zeus.goldragon.criome \
    'su - bird -c "/nix/store/a0f9p0gnsfq23hbbqw885xhmip9qmrn1-home-manager-generation/activate"'
Starting Home Manager activation
Activating checkFilesChanged
Activating preparePiPackageSymlink
Activating checkLinkTargets
[skipped — files already symlinked by prior partial activation on Sep 6 14:47]
Activating writeBoundary
No change so reusing latest profile generation
[GC root current-home already pointed to new generation from prior partial run;
 nix-env --profile was skipped, leaving home-manager-31-link as the named link]
Activating linkGeneration
Cleaning up orphan links from /home/bird
Creating home file links in /home/bird
Activating installPackages
nix profile remove /nix/store/q9nxza9karnxgakzcll9p8kpz31n1czs-home-manager-path
removing 'home-manager-path'
removed 1 packages, kept 4 packages
Activating dconfSettings
Activating reloadSystemd
[orchestrate-nexus.service was already failed; continued]
Starting units: criomos-ui-priority.service, orchestrate-nexus.service, set-SSH_AUTH_SOCK.service
Activating reconcileNoctaliaSettings
Activating updateUserDesktopDatabase
```

The `writeBoundary` step said "No change" because a prior failed deployment (212/213) had already updated the GC root `~/.local/state/home-manager/gcroots/current-home` to point at `a0f9p0gnsfq23hbbqw885xhmip9qmrn1`. This caused `nix-env --profile --set` to be skipped, so `home-manager-32-link` was not created.

---

## Step 3 — Manually set the profile link

```
$ ssh root@zeus.goldragon.criome \
    'su - bird -c "nix-env --profile /home/bird/.local/state/nix/profiles/home-manager \
      --set /nix/store/a0f9p0gnsfq23hbbqw885xhmip9qmrn1-home-manager-generation"'
(no output — success)
```

Verified:

```
$ ssh root@zeus.goldragon.criome \
    'ls -la /home/bird/.local/state/nix/profiles/ | grep home-manager'
lrwxrwxrwx 1 bird users 20 Sep  6 15:36 home-manager -> home-manager-32-link
lrwxrwxrwx 1 bird users 67 Jul 29 16:58 home-manager-30-link -> /nix/store/z013ab5cszmn7v8m212f7dfg91kn7ckk-home-manager-generation
lrwxrwxrwx 1 bird users 67 Sep  4 16:41 home-manager-31-link -> /nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation
lrwxrwxrwx 1 bird users 67 Sep  6 15:36 home-manager-32-link -> /nix/store/a0f9p0gnsfq23hbbqw885xhmip9qmrn1-home-manager-generation
```

**Bird is now on home-manager generation 32** at store path `/nix/store/a0f9p0gnsfq23hbbqw885xhmip9qmrn1-home-manager-generation`.

---

## Step 4 — Noctalia restart

Pre-restart binary (PID 3707, running since Aug 28):

```
/proc/3707/exe -> /nix/store/dr2v7rd4himys11hmlq54ng0jwvqyb0c-noctalia-5.1.0/bin/.noctalia-wrapped
```

The new home-manager generation's `home-path/bin/noctalia` also resolves to the same store path (`dr2v7rd4himys11hmlq54ng0jwvqyb0c-noctalia-5.1.0`). The noctalia binary did not change between generations.

`noctalia msg config-reload` was sent; it acknowledged `ok` but a plugin list confirmed the new plugin set was not picked up (config-reload does not restart plugin loader). Noctalia was killed with SIGTERM (PID 3707) and restarted as bird:

```
$ ssh root@zeus.goldragon.criome \
    'su - bird -c "XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-1 \
      DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus noctalia --daemon" &'
[startup log — noctalia v5.1.0 — PID 2587359]
IPC socket at /run/user/1000/noctalia-wayland-1.sock
```

Post-restart binary:

```
/proc/2587359/exe -> /nix/store/dr2v7rd4himys11hmlq54ng0jwvqyb0c-noctalia-5.1.0/bin/.noctalia-wrapped
```

The binary path is unchanged. **Noctalia is NOT on a new binary** — `noctalia-5.1.0` is what both the old and new generations supply.

---

## Step 5 — Status bar functionality

The old bar config (`dhwq1j6ndp5kh47nqasmfblv2w93h82d` generation):

```toml
[bar.main]
end = ["listener-level", "tray", "battery", "volume", "brightness", "control-center"]
```

The new bar config (`vqn3r86ddr7jkw8d9y896k5lh5hjylc2-home-manager-files`, symlinked Sep 6 14:47):

```toml
[bar.main]
end = ["wispr-status-widget", "listener-level", "tray", "battery", "volume", "brightness", "control-center"]
```

`wispr-status-widget` was added. After restart, noctalia loaded the new config:

```
$ noctalia msg plugins list | grep -v community
criomos/wispr-status [local] 2.0.0 enabled
criomos/listener-level [local] 1.1.0 enabled
```

**Only that the process restarted with the new config is established.** Visual confirmation that `wispr-status-widget` is rendering in the bar is not available from CLI. The plugin is loaded and the bar config declares it in the `end` section; whether it is functioning correctly in the compositor can only be verified by direct observation of bird's screen.

---

## Summary

| Item | Value |
|------|-------|
| Generation | 32 |
| Store path | `/nix/store/a0f9p0gnsfq23hbbqw885xhmip9qmrn1-home-manager-generation` |
| Noctalia binary | `/nix/store/dr2v7rd4himys11hmlq54ng0jwvqyb0c-noctalia-5.1.0` (unchanged) |
| Status bar change | `wispr-status-widget` added to bar end; process restarted with new config |
| Functionality confirmed | No — only process restart, not visual bar state |
| Declarative state | Unchanged; this bypass will be overwritten by the next normal deployment |
