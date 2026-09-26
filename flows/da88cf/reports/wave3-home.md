# Wave 3 — Home declarations for the Field monitors and the Herdr server

CriomOS-home bookmark `wave3-home-da88cf`, commit `182400f0d469f2e464c52823e53560f50c078283`, on top of `integration-2-da88cf` (`98255d10`, the same commit as `home-fixes-da88cf`). Pushed; `git ls-remote` shows the bookmark at `182400f0`.

Nothing was activated and no live unit was touched.

## Units declared

All are off unless enabled. No host or profile enables any of them. The enable wiring is `criomosHome.fieldMonitoring.<monitor>.enable` and `criomosHome.herdr.server.enable`, and where each one is turned on is a data question left open.

`modules/home/profiles/min/field-monitoring.nix` (imported from `modules/home/default.nix`):

| Option | Units | Script source (pinned flake input) | Kept from the live unit | Changed from the live unit |
| --- | --- | --- | --- | --- |
| `coreCheckup` | `core-checkup.{service,timer}` | `core-checkup-source` = primary `d3002f4b`, which is the same store path the live unit runs (`63iv1hcr…-source`) | every setting and timing; `ExecStartPre test -r <roster>`; the argument order | the roster is now the option `roster` (JSON attrs, required when enabled; the live copy is the store file `8xgi8bjm…-core-checkup-roster.json`); `PATH` is store paths (node, iputils, systemd, codex, claude) instead of `~/.nix-profile/bin`; `policyPath` defaults to `~/.config/core-checkup/policy.json` (the file the operator keeps, as now) |
| `fieldCensus` | `field-census.{service,timer}` | `field-monitoring-source` = primary main `1e8eee26`, whose files are byte-identical to the working copy | `--observe-only` (option `observeOnly`, default true), the environment, the 5-minute timer, `UMask`, and the limits | `PATH` is node, herdr, messenger-clj (hm-*), systemd, and coreutils; `WorkingDirectory` is the option `primaryRoot` (default `~/primary`), used as the data root only |
| `fieldCheckupShadow` | `field-checkup-shadow.{service,timer}` | the same source | `After=field-census.service`, the environment, and the 7-minute and 30-minute timings | the roster path is an option |
| `fieldLunaResearch` | `field-luna-research.{service,timer}` | `field-luna-research-source` = field main `34fe6c88`, byte-identical to the working copy | `--once`, `FIELD_PRIMARY_ROOT`, a 610-second timeout, and the flock guard | the runner is now a packaged `writeShellApplication` that does what `bin/field-luna-research-run` did, but with store node, codex, herdr, and flock. The live script hard-codes `/home/li/.nix-profile/bin/node`. `WorkingDirectory` is the pinned field source. |
| `fieldMonitor98eb43` | `field-monitor-98eb43.{service,timer}` | primary `1e8eee26` `flows/98eb43/monitor/census.mjs` | the timings and the behaviour | the six absolute-path constants are replaced at build time (`substituteInPlace --replace-fail`): root is `primaryRoot`, state is `$XDG_STATE_HOME`, and herdr, hm-list, hm-send, and jj are store paths. It is scoped to the flow: drop it when 98eb43 ends. |

**`agent-intercom-fleet-cleanup` is not declared.** Its target, `~/.pi/agent/packages/agent-intercom-orchestrator/src/agent-fleet-cleanup.mjs`, no longer exists: `~/.pi/agent/packages/` holds only `pi-mcp-adapter`. That is why the service fails. Discard it as wave2 row 13 says.

Hand-made unit guard: when any monitor is enabled, the activation entry `fieldMonitoringHandMadeUnits` runs before `checkLinkTargets`. It prints a `warnEcho` for each declared unit name that still exists under `~/.config/systemd/user` and is not a home-manager-files link. It is a warning, not an assertion, because evaluation cannot see the home directory. Home Manager's own link check then refuses the collision.

`modules/home/profiles/min/herdr.nix`:

- `criomosHome.herdr.server.enable` (default false) declares `herdr-server.service`. It copies the observed transient `psyche-fable-herdr.service`: `ExecStart=<herdr pkg>/bin/herdr server`, `Type=exec`, `Restart=no`, `KillMode=control-group`, `Slice=app.slice`, `WorkingDirectory=%h`, and no `Environment=` of its own (the transient unit has none; the process inherits the user manager's environment). It adds `WantedBy=default.target`.
- `criomosHome.herdr.versionPin = "0.8.2"` is read-only, and an assertion refuses a Herdr package of any other version. The declared package is `9x03bz0q…-herdr-0.8.2`, which is the path `~/.nix-profile/bin/herdr` points to today.
- The activation entry `herdrServerHandoverGuard` runs before `writeBoundary`. If any `herdr` process with argv[1] `server` is running and is not `herdr-server.service`'s MainPID, it fails activation and names the PID and its cgroup unit.

## Checks

These are wired explicitly in `flake.nix` next to the Herdr checks:

- `checks/field-monitoring`: with every monitor off there are no units and no guard, and `agent-intercom-fleet-cleanup` is absent. With every monitor on, it checks each unit's fields against the live unit. At build time it checks that the pinned sources contain every script (including `harness-facts.mjs` and `field-structure.mjs`), that the patched 98eb43 script contains no `/home/li`, and that the Luna runner keeps `flock -n 9` and the pinned script.
- `checks/herdr-server`: off means no unit and no guard. It checks that the version pin equals the package version, and the unit fields, the absence of `Environment=`, and `WantedBy`. It checks that the guard is ordered before `writeBoundary` and exits non-zero. At build time it runs `herdr --version` and expects `herdr 0.8.2`.

## Evidence

- Both checks evaluate on ouranos with `--override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system`. The results are `zk4sc32n…-field-monitoring.drv` and `hp21myqz…-herdr-server.drv`.
- The checks were tested against deliberate breakage, at evaluation only, and the source was restored afterwards:
  - With `OnBootSec` at 8min, field-monitoring fails.
  - With `Restart=always`, herdr-server fails.
  - With the server enable defaulting to true, herdr-server fails on the default-off assertion.
- The real `homeConfigurations.li` for ouranos (system and horizon from lojix `user-environment`) has none of the new units and `herdr.server.enable = false`. Its activation derivation is `7r0zq3k3vbp2cf4xjr5r52phcbwzn2xp-home-manager-generation.drv`, the same derivation the base `integration-2-da88cf` produces. The default-off change is therefore byte-neutral for the deployed generation.

Both checks were built on Prometheus, one after the other. The builds ran with `--max-jobs 0`, and each log shows `building '…' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`. Neither had to queue for a slot.

- `checks.x86_64-linux.herdr-server` built to `/nix/store/q4lx2498nvig8iz2gnlfa6an8kp9h7jq-herdr-server`.
- `checks.x86_64-linux.field-monitoring` built to `/nix/store/p51fiz0k2cz2j5v5sbkpmsi93mq4zymd-field-monitoring`. Its closure includes `field-luna-research-run`, messenger-clj 0.2.5, and the patched `field-monitor-98eb43-census.mjs`, all built remotely.

## Unproven

- None of the declared units has run. Nothing was activated, and the module's behaviour next to live state (the policy, recipients and roster files, and Herdr sessions) was not exercised.
- The core-checkup roster: the module does not reproduce the live store roster, which lists Yggdrasil endpoints for ouranos, prometheus, tiger, and zeus plus four units. Whoever enables it must supply it from data, either the Horizon projection or a host file.
- The Herdr handover guard was not executed. Its shell logic is checked only by string at evaluation.
- The `PATH` sets are inferred by reading each script's spawned commands: core-checkup uses claude, codex, ping, and systemctl; the census uses herdr and systemctl, plus hm-send when not observe-only; Luna uses codex and herdr, and probes opencode, which is absent in both the live PATH and the declared one. A tool spawned only on a path I did not read would be missing.
- The running Herdr server executes `n4fsjxkyn…-herdr-0.8.2` (started 09-19). The declared unit would run `9x03bz0q…-herdr-0.8.2`: the same version, a different store path (the patched Home package).

## What the activation window must do

For each monitor the living keeps: set its enable in data for the chosen host or profile. Before activating, remove the hand-made `~/.config/systemd/user/<name>.{service,timer}` and their `timers.target.wants` links. Some are symlinks into `~/primary/tools/…`. Then `systemctl --user daemon-reload` and activate. The warning names any file still left. The monitors the living drops simply stay off, and their hand-made units are removed.

For Herdr:
1. Choose the window, because every pane closes.
2. Set `criomosHome.herdr.server.enable = true` in data.
3. Stop the transient unit: `systemctl --user stop psyche-fable-herdr.service`.
4. Activate. The guard refuses until step 3 is done.
5. Confirm that `herdr-server.service` is active and on 0.8.2.
6. Relaunch or reattach the panes.

Discard `agent-intercom-fleet-cleanup.{service,timer}` by hand (wave2 row 13).

## Sources

- `systemctl --user cat` for core-checkup, field-census, field-checkup-shadow, field-luna-research, field-monitor-98eb43, and agent-intercom-fleet-cleanup (2026-09-26), and `ls -la ~/.config/systemd/user`.
- `systemctl --user show psyche-fable-herdr.service`, `/run/user/1001/systemd/transient/psyche-fable-herdr.service`, `/proc/807384/{environ,exe}`, and `herdr --version`.
- Scripts: `/nix/store/63iv1hcr…-source/tools/core-checkup.mjs` (matched to primary `d3002f4b` with `cmp`), `~/primary/tools/field-census-cycle.mjs`, `field-census.mjs`, `field-checkup-shadow-cycle.mjs`, `~/primary/flows/98eb43/monitor/census.mjs`, `/git/github.com/LiGoldragon/field/bin/field-luna-research{-run,.mjs}`, and the `~/.config/core-checkup/policy.json` and census and checkup configuration.
- `flows/da88cf/reports/inventory-system.md` (C rows, D2) and `flows/da88cf/reports/wave2-plan.md` (rows 13–18 and 21, Q5, Q6).
- The earlier proposal `proposal/cf7879-core-checkup-home` (`b8ec0f10`), used as a shape reference.
