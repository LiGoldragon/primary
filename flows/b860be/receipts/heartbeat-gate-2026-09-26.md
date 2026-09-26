# heartbeat-gate — field-luna-heartbeat declared off by default (2026-09-26)

Brief: gate the CriomOS-home Home unit `field-luna-heartbeat` behind a default-off option, on a new bookmark `heartbeat-gate-b860be` from `integration-2-da88cf` at 98255d10; no repin of `prompt-relay-source` (stays 9d144e3); `flake.nix`, `flake.lock`, `checks/flow-service-path` untouched.

## Revision

- Base: `98255d100e9627f30b2e66e0772801a100cdfc03` (integration-2-da88cf at launch).
- Bookmark `heartbeat-gate-b860be` → `9d72198444c58bd95d705e38c673d6674b20d50d`
  "Home: declare field-luna-heartbeat off unless criomosHome.fieldLunaHeartbeat.enable".
- Workspace: `jj workspace add --name heartbeat-gate-b860be -r 98255d100e /home/li/wt/github.com/LiGoldragon/CriomOS-home/heartbeat-gate-b860be`; forgotten and removed after the push (working copy was empty).

Scope proof (`jj diff -r @- --name-only`, run after commit and again before push):

    modules/home/profiles/min/field-luna-heartbeat.nix

Push and remote witness:

    jj git push --bookmark heartbeat-gate-b860be
    git ls-remote https://github.com/LiGoldragon/CriomOS-home refs/heads/heartbeat-gate-b860be refs/heads/integration-2-da88cf
    9d72198444c58bd95d705e38c673d6674b20d50d	refs/heads/heartbeat-gate-b860be
    8a60835c5cd24c9a0c712906f5603be1628573c6	refs/heads/integration-2-da88cf

`integration-2-da88cf` on the remote had moved on to 8a60835c (the other flow's work) by push time; this bookmark sits on 98255d10 as briefed and will need a rebase or merge onto it.

## Change

Option: `criomosHome.fieldLunaHeartbeat.enable`, `lib.mkEnableOption` (type bool, default `false`). This follows the convention of wave3-home-da88cf 182400f0: `criomosHome.fieldMonitoring.<monitor>.enable` and `criomosHome.herdr.server.enable` are both `mkEnableOption` under `criomosHome.*`, and their units are declared inside `mkIf`.

All of the module's `config` sits under `lib.mkIf cfg.enable`: `systemd.user.services.field-luna-heartbeat`, `systemd.user.timers.field-luna-heartbeat` (timers.target), and `systemd.user.paths.field-luna-heartbeat` (default.target). The runner `writeShellApplication` (its PATH is the runtimeInputs) is referenced only from the service's ExecStart, so it is not in the generation when the option is off. The module installs no other packages or links. Unit contents are unchanged.

## Evaluation evidence

Home configuration: `homeConfigurations.li` with ouranos's lojix user-environment inputs. `G=/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment`

    nix eval --json --option max-jobs 0 --override-input system path:$G/system --override-input horizon path:$G/horizon \
      path:.#homeConfigurations.li --apply "$(cat off.nix)"

off.nix reads `hc.config`: the option value, `systemd.user.{services,timers,paths} ? field-luna-heartbeat`, the `xdg.configFile` names matching `field-luna-heartbeat`, and whether a `field-luna-heartbeat` package is in `home.packages`.

Default (9d721984):

    {"enable":false,"path":false,"pkgInHome":false,"service":false,"timer":false,"unitFiles":[]}

Enabled. on.nix is the same query over `(hc.extendModules { modules = [ { criomosHome.fieldLunaHeartbeat.enable = true; } ]; }).config`:

    {"enable":true,"path":true,"pathWantedBy":["default.target"],"service":true,"timer":true,"timerWantedBy":["timers.target"],"unitFiles":["systemd/user/default.target.wants/field-luna-heartbeat.path","systemd/user/field-luna-heartbeat.path","systemd/user/field-luna-heartbeat.service","systemd/user/field-luna-heartbeat.timer","systemd/user/timers.target.wants/field-luna-heartbeat.timer"]}

Base, before the change (negative witness). The same inputs, evaluated from `github:LiGoldragon/CriomOS-home/98255d100e9627f30b2e66e0772801a100cdfc03#homeConfigurations.li`:

    {"hasOption":false,"path":true,"service":true,"timer":true}

Default-off generation drv (evaluation only, not built):

    nix eval --raw ... path:.#homeConfigurations.li.activationPackage.drvPath
    /nix/store/8gqfwd3cdvbk5iamjfn5kcz91wi89p3s-home-manager-generation.drv

Builder evidence: nothing was built. stderr showed only `copying path '/nix/store/…-source' from 'http://nix.prometheus.goldragon.criome'` (substitution of flake sources: 9 lines on the first eval, 1 on the second), and no `building` lines. `/etc/nix/machines` declares `ssh-ng://nix-ssh@prometheus.goldragon.criome`, and `max-jobs = 0`.

## Not run

- No focused check covers this module: `checks/` has no field-luna-heartbeat check, and adding one would mean registering it in `flake.nix`, which is off-limits tonight. The aggregate Home check was not run (known Blueprint blocker).
- Nothing was activated. A live `field-luna-heartbeat` unit on ouranos (if one is running) keeps running until the next Home activation from a generation containing this change. Stopping or removing it is an activation-window act.
