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
