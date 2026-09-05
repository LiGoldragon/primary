# Terminal scopes get OOMPolicy=continue

Write subflow of flow 1a6ca4, 2026-09-05 11:00-11:55 CEST on host ouranos.
The living approved "the OOMPolicy change" (flows/1a6ca4/log.md, line 43).
Everything below is this subflow's own witness unless marked relayed.

## Read

- `reports/harnessExit.md`: the 04:08 kill inside
  `app-ghostty-surface-transient-3762188.scope`, `OOMPolicy=stop`,
  `KillMode=control-group`.
- Live host: `/etc/systemd/user.conf` is an empty `[Manager]`; `/etc/systemd/system.conf`
  sets no OOM policy; `systemctl --user show -p DefaultOOMPolicy` = `stop`
  (systemd's own default, not a CriomOS declaration); `systemctl show -p DefaultOOMPolicy`
  = `stop`; every running `app-ghostty-surface-transient-*.scope` shows
  `OOMPolicy=stop KillMode=control-group Slice=app.slice DropInPaths=`; the
  transient unit file at `/run/user/1001/systemd/transient/<scope>` carries only
  `[Scope] ManagedOOMMemoryPressure=kill`. systemd 261.1, Ghostty 1.3.1.
- Ghostty's documentation (`ghostty.5.md`, `linux-cgroup*`): one transient scope per
  surface; it exposes `MemoryHigh` (`linux-cgroup-memory-limit`) and `TasksMax`, no OOM
  policy. So the policy is systemd's to declare, not Ghostty's.
- CriomOS-home (owner of the terminal): `programs.ghostty` in
  `modules/home/profiles/min/default.nix`; the niri `Mod+Shift+Return` binding spawns
  `ghostty --gtk-single-instance=true` (`niri.nix`), whose surfaces are the scopes above
  (the Ghostty application itself runs in `app-niri-ghostty-<pid>.scope`); the rescue
  terminal `criomos-rescue-terminal` (`niri.nix`) is `systemd-run --user --scope` around
  `ghostty --gtk-single-instance=false`, so no per-surface scope: the shell shares the
  `criomos-rescue-terminal-*.scope` with Ghostty. Other terminals in the source:
  `foot` in `profiles/min/sway.nix`, and `ghostty -e` in `waybar.nix`/`hyprland.nix`;
  none of these three modules is imported (`modules/home/default.nix`), so ghostty is
  the only terminal in the live configuration.
- Mechanism witnessed on the host before editing (transient, removed within the same
  command): a runtime drop-in `/run/user/1001/systemd/user/app-oomtest-.scope.d/oom.conf`
  with `[Scope] OOMPolicy=continue` plus `daemon-reload`, then
  `systemd-run --user --scope --unit=app-oomtest-surface-1 sleep 20`:
  `DropInPaths=/run/user/1001/systemd/user/app-oomtest-.scope.d/oom.conf`,
  `OOMPolicy=continue`; a running ghostty scope stayed `OOMPolicy=stop`.
  systemd applies dash-prefix drop-ins to transient scopes.
- Deployment state (flows/58a86d/log.md, flows/acf06f/log.md, relayed; CriomOS
  `UPGRADES.md` "UserEnvironment deployment 190 partial-activation gate", read):
  deployment 190 (`ActivateNow`) failed at the VSCodium extension-registry hook after
  `run_profile` had already moved the Home profile to generation 1012; the gate says
  "do not manually repair the profile, roll back, or submit a superseding activation".
  Witnessed now: `~/.local/state/criomos/vscodium-claude/extensions-immutable.registry.json`
  still differs from `~/.vscode-oss/extensions/.extensions-immutable.json` (cmp: byte 738);
  Lojix `Current` UserEnvironment is 189 while `~/.local/state/nix/profiles/home-manager`
  points at `home-manager-1012-link` (190's generation). The gate is in force.
- Locks: `Observe.Locks` showed nothing on CriomOS or CriomOS-home (flow 58a86d holds
  no lock). Locked 762 (`TerminalOomPolicy`, 7 paths) and 763
  (`TerminalOomPolicyModule`, 2 paths), released after the commits.

## Changed

CriomOS-home commit `5be71211f668a210c99945e15a5d80ed388d8102` "Terminal scopes survive
a kernel OOM kill" (main, pushed), on top of d9bec96 (the working copy had sat on
6085671, six commits behind; rebased, one comment-placement conflict in niri.nix
resolved keeping both sides):

- `modules/home/profiles/min/terminal-scopes.nix` (new): the narrowest declaration --
  `xdg.configFile."systemd/user/app-ghostty-.scope.d/oom-policy.conf".text` =
  `[Scope]` / `OOMPolicy=continue`. The prefix matches
  `app-ghostty-surface-transient-*.scope` only; `app-niri-ghostty-*.scope` and the rest
  of the session keep `DefaultOOMPolicy=stop`.
- `modules/home/default.nix`: imports it.
- `modules/home/profiles/min/niri.nix`: the rescue terminal's `systemd-run` gains
  `--property=OOMPolicy=continue` (its scope is the terminal scope there).
- `checks/terminal-oom-policy/default.nix` (new) + `flake.nix` registration: a NixOS VM
  test. It evaluates the module through `homeManagerConfiguration`, installs the
  generated drop-in for a lingering user, starts
  `app-ghostty-surface-transient-4242.scope` with `MemoryMax=64M MemorySwapMax=0`
  running a script that backgrounds `sleep 600` (the harness) and then allocates 256 MiB
  in python (the test binary); asserts the script reports `overrun:137`, the scope shows
  `OOMPolicy=continue`, `ActiveState=active`, `Result=success`, the first pid in the
  scope's `cgroup.procs` is `sleep`, and a control scope `app-control-4242.scope` shows
  `stop`, as does `DefaultOOMPolicy`. `vm.panic_on_oom` is forced to 0 in the node (the
  test profile sets 2, which panicked the VM on the first run).
- `UPGRADES.md`: activation note (daemon-reload only; running surfaces keep `stop`).

CriomOS commit `f8cda8539d01b38ab689de44be2ec3195f34e6d4` "Pin CriomOS-home 5be7121
(terminal scope OOM policy)" (main, pushed): `flake.nix` line 36 URL and `flake.lock`
`criomos-home` d9bec96 -> 5be7121.

## Tests

All builds on the remote builder (`--max-jobs 0`, `@/etc/nix/machines`, prometheus),
with `--override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system`.

- `checks.x86_64-linux.terminal-oom-policy`: run 1 quoting defect (mine); run 2 kernel
  panic (`panic_on_oom`); run 3 the harness survived the OOM kill but its inherited stdout
  kept the step open for 600 s, so the scope was gone when queried; run 4 green
  (`/nix/store/mh2lhvbxjp01sfzh521ncc5w25vhsz5p-vm-test-run-terminal-oom-policy`, every
  step 0.09-1.30 s). Negative run with the drop-in set to `OOMPolicy=stop`: fails at the
  surface step, the scope is stopped on the OOM and the shell never reports the kill --
  the harness-death case. Restored to `continue`; green again on the rebased tree.
- `ghostty-primary-selection`, `wispr-status-niri-rule`, `desktop-shell-launch`: green.
- CriomOS materialized target (user-environment inputs system/horizon/secrets):
  `nixosConfigurations.target.config.home-manager.users.li.xdg.configFile."systemd/user/app-ghostty-.scope.d/oom-policy.conf".text`
  = `[Scope]\nOOMPolicy=continue`; `homeConfigurations.li.activationPackage.drvPath`
  evaluates (2:05).

## Deployment

Preflight: `git ls-remote origin main` = f8cda853; proposal
`/git/github.com/LiGoldragon/goldragon/proposal.datom` regular, not a symlink;
`CheckHostKeyMaterial.(goldragon ouranos <proposal>)` -> `KeyMaterialChecked.(ouranos [] (4997 4997))`.

Owner request (`LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix`):

```
Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=f8cda8539d01b38ab689de44be2ec3195f34e6d4 (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 Realize RequireImmutable Some.@/etc/nix/machines [])
```

-> `DeployAccepted.(192 (4998 4998))`. `Query.ByDeployment.(192)`: `Building` at 11:42:39
through 11:44:39, then at 11:45:09:

```
Queried.([] [(192 192 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.Realize ProfileOnly RequireImmutable Some.f8cda8539d01b38ab689de44be2ec3195f34e6d4) Some.(4998 4998) Completed Some.(5014 5014) Some.Succeeded)] (5018 5018))
```

The realized generation is in the local store:
`/nix/store/mjiqw0r7phz6676y5vyhv608dfzn5jzp-home-manager-generation`; its
`home-files/.config/systemd/user/app-ghostty-.scope.d/oom-policy.conf` reads
`[Scope]` / `OOMPolicy=continue`, and its `criomos-rescue-terminal` carries
`OOMPolicy=continue`. Against the live generation 1012 (`m09spn0…`) it differs in that
drop-in and in what acf06f landed and did not activate (niri config.kdl, noctalia
config.toml, the wispr-status plugin and `wispr-flow-status` binary, 10-hm-fonts.conf).

**Not activated.** Lojix `Current` stays 189; the live profile stays 1012; the gate
above forbids a superseding activation while the registry disagreement stands. An
activation of this generation would only link the drop-in and run `sd-switch`
(`activate` line 690: daemon-reload), no service restart from this change; the acf06f
carry-over is the part that needs the steward's decision.

## Live verification

Not possible through the declarative path: `~/.config/systemd/user/app-ghostty-.scope.d`
does not exist on the host, and every ghostty surface scope still shows
`OOMPolicy=stop`. The evidence that the declaration does what is wanted is the VM check
(same systemd mechanism, real kernel OOM kill, harness survives) and the transient
prefix-drop-in witness on this host at the start.

The immediate protection that needs no activation is a runtime mutation, so it was not
done without the living's word: `mkdir -p /run/user/1001/systemd/user/app-ghostty-.scope.d
&& printf '[Scope]\nOOMPolicy=continue\n' > /run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf
&& systemctl --user daemon-reload`. It is lost at logout/reboot, is byte-identical to the
declared file, and is superseded (same content, lower precedence) once the generation is
activated. Verification after either path: open a ghostty surface, then
`systemctl --user show app-ghostty-surface-transient-<pid>.scope -p OOMPolicy` = `continue`;
surfaces opened before keep `stop` until reopened.

## Left hanging

- Activation of generation 192 awaits the steward's registry reconciliation (primary-6f9,
  flow 58a86d) and the acf06f activation decision (primary-vx3).
- systemd-oomd is active on the host and monitors every ghostty surface scope
  (`ManagedOOMMemoryPressure=kill`, set by Ghostty in the transient unit; limit 60 % for
  30 s, `oomctl`). oomd kills the whole cgroup, harness included, on sustained pressure.
  It did not fire at 04:08 (no oomd journal entries); the kernel got there first. Whether
  a drop-in can override a property the transient unit itself sets is unverified.
  Not decided here.
- The `su`-based scope start in the VM check goes through pam; fine in the VM, noted in
  case a future systemd changes session handling.

## Sources

- `/home/li/primary/flows/1a6ca4/reports/harnessExit.md`, `reports/stackMap.md`,
  `log.md` lines 42-43
- `/home/li/primary/flows/58a86d/log.md`, `/home/li/primary/flows/acf06f/log.md`,
  `/home/li/primary/flows/acf06f/witnesses/realize-generation.md`
- `/git/github.com/LiGoldragon/CriomOS/UPGRADES.md` (partial-activation gate),
  `AGENTS.md` (materialized inputs, push-before-build)
- `/git/github.com/LiGoldragon/CriomOS-home`: `AGENTS.md`, `modules/home/default.nix`,
  `modules/home/profiles/min/{default,niri,sway,waybar,hyprland}.nix`,
  `modules/home/vscodium/vscodium/claude-lifecycle.sh`, `checks/*`
- `/nix/store/nymbjir3h6xr0g40dgv1shs418nxb3s3-ghostty-1.3.1/share/ghostty/doc/ghostty.5.md`
- Host: `/etc/systemd/user.conf`, `/etc/systemd/system.conf`, `systemctl --user show`,
  `/run/user/1001/systemd/transient/`, `oomctl`, `journalctl -u systemd-oomd`,
  `/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/`
- Build logs in the scratchpad: `oom-check-build{,2,3,4}.log`, `oom-check-negative.log`;
  `nix log` of the failed VM runs
- Lojix replies quoted above (`meta-lojix`, `lojix`)

## Runtime application

Write subflow of flow 1a6ca4, 2026-09-05 11:51-11:55 CEST on host ouranos, as user li,
no sudo. The main flow applied the runtime protection under the living's "unblock it,
and you can explain to me later". Deployment 192 untouched; no Lojix request; no
service restarted; no repository touched. Everything here is this subflow's own witness.

### 1. Drop-in and reload (11:51:29)

```
$ mkdir -p /run/user/1001/systemd/user/app-ghostty-.scope.d && printf '[Scope]\nOOMPolicy=continue\n' > /run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf && systemctl --user daemon-reload
$ cat /run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf
[Scope]
OOMPolicy=continue
```

Journal (`journalctl --user -b`): `Reload requested from client PID 4079439 ('systemctl')
(unit app-ghostty-surface-transient-4027617.scope)... Reloading... Reloading finished in
137 ms. Failed to adjust io pressure threshold, ignoring: Device or resource busy` (the
last line appears on every reload on this host; it is not from the drop-in).

### 2. Fresh probe scope, and the running surfaces

```
$ systemd-run --user --scope --unit app-ghostty-surface-transient-probe-4079432.scope sleep 5 &
Running as unit: app-ghostty-surface-transient-probe-4079432.scope; invocation ID: 9c3fa64fd69741a0a7ebfd850143b933
$ systemctl --user show app-ghostty-surface-transient-probe-4079432.scope -p OOMPolicy -p ManagedOOMMemoryPressure -p DropInPaths -p ActiveState
ActiveState=active
DropInPaths=/run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf
OOMPolicy=continue
ManagedOOMMemoryPressure=auto
```

(`auto` on the probe because `systemd-run` sets no oomd property; Ghostty's transient
unit files set `kill`.)

The running surface scopes did **not** keep `stop`. Every one of the 19 loaded
`app-ghostty-surface-transient-*.scope` units (ActiveEnterTimestamps from 2026-08-22
18:01 to 2026-09-05 11:33) showed, after the reload:

```
$ for u in $(systemctl --user list-units 'app-ghostty-surface-transient-*' --no-legend --plain | awk '{print $1}'); do echo "$u $(systemctl --user show $u -p OOMPolicy -p ManagedOOMMemoryPressure -p DropInPaths | tr '\n' ' ')"; done
app-ghostty-surface-transient-1013091.scope DropInPaths=/run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf OOMPolicy=continue ManagedOOMMemoryPressure=kill
... (identical for 1963206 2369609 2478201 2518768 2555558 2733663 2975022 3046624 3436028 3438041 3441455 3527898 3740057 3743853 3762188 4027617 4057498 4059234)
```

`DefaultOOMPolicy=stop` unchanged; `app-niri-ghostty-4917.scope` (the Ghostty
application) is not matched by the prefix and keeps the default.

Correction to the sections above: "surfaces opened before keep `stop` until reopened"
was an inference, not a witness -- the earlier transient test used the `app-oomtest-`
prefix, which never matched a ghostty scope, so it said nothing about reload behavior.
Observed now: `daemon-reload` re-reads the transient unit file plus its drop-ins for
running scopes and the shown property changes. Whether the kernel-OOM handler consults
the reloaded value at kill time is not witnessed on this host (no OOM was provoked on a
live surface); the VM check witnessed it only for a scope started after the drop-in.

### 3. oomd probe: `ManagedOOMMemoryPressure=auto` in the same drop-in (11:52:00)

Before: `oomctl` listed every ghostty surface scope under "Memory Pressure Monitored
CGroups" (limit 60 %, 30 s); `app.slice` shows `ManagedOOMMemoryPressure=auto
ManagedOOMMemoryPressureLimit=0`; no "Swap Monitored CGroups".

```
$ printf '[Scope]\nOOMPolicy=continue\nManagedOOMMemoryPressure=auto\n' > /run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf
$ systemctl --user daemon-reload
$ systemd-run --user --scope --unit app-ghostty-surface-transient-probe2-4079847.scope --property=ManagedOOMMemoryPressure=kill sleep 5 &
Running as unit: app-ghostty-surface-transient-probe2-4079847.scope; invocation ID: 6f6c940e067947e0aa5fc84f7e6e9cdf
$ cat /run/user/1001/systemd/transient/app-ghostty-surface-transient-probe2-4079847.scope
# This is a transient unit file, created programmatically via the systemd API. Do not edit.
[Unit]
Description=[systemd-run] /run/current-system/sw/bin/sleep 5

[Scope]
ManagedOOMMemoryPressure=kill
$ systemctl --user show app-ghostty-surface-transient-probe2-4079847.scope -p OOMPolicy -p ManagedOOMMemoryPressure -p DropInPaths -p ActiveState
ActiveState=active
DropInPaths=/run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf
OOMPolicy=continue
ManagedOOMMemoryPressure=auto
$ systemctl --user show app-ghostty-surface-transient-4059234.scope -p OOMPolicy -p ManagedOOMMemoryPressure
OOMPolicy=continue
ManagedOOMMemoryPressure=auto
$ oomctl
Dry Run: no
Swap Used Limit: 90.00%
Default Memory Pressure Limit: 60.00%
Default Memory Pressure Duration: 30s
System Context:
	Memory: Used: 12.4G, Total: 30.8G
	Swap: Used: 10.3G, Total: 39.7G
Swap Monitored CGroups:
Memory Pressure Monitored CGroups:
```

The drop-in wins over the property the transient unit itself sets (the probe's own
file says `kill`; the unit shows `auto`), for the fresh scope and for the running
surfaces after reload. systemd-oomd now monitors no cgroup in the user session
(`app.slice` is `auto` with limit 0, so `auto` inherits "not monitored"). The line is
left in. Trade-off this creates, for the main flow to weigh: a runaway surface is no
longer killed by oomd on sustained pressure; it runs until the kernel OOM killer picks a
process, and `OOMPolicy=continue` then keeps the rest of the scope (the harness) alive.
That is the shape the VM check proved.

### Health after both reloads

`journalctl -u systemd-oomd --since 11:50`: no entries. `systemctl --user
list-units --state=failed`: `app-ghostty-surface-transient-3762188.scope` (failed
2026-09-05 04:09:48, `Failed with result 'oom-kill'` -- the original event, still
loaded) and `agent-intercom-fleet-cleanup.service` (StateChangeTimestamp 11:46:54,
before this subflow's first command at 11:51:29). `is-system-running` = `degraded` for
those two, unchanged by this work.

### Final state

`/run/user/1001/systemd/user/app-ghostty-.scope.d/oom-policy.conf`:

```
[Scope]
OOMPolicy=continue
ManagedOOMMemoryPressure=auto
```

Runtime only: lost at logout/reboot. The declared file in generation 192 carries only
`OOMPolicy=continue`; when 192 is activated its `~/.config` drop-in (same name, higher
precedence than `/run`) replaces this one, and oomd monitoring of surfaces returns unless
the declaration is extended with the `ManagedOOMMemoryPressure=auto` line -- not done
here, no repository touched.
