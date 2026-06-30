# CriomosImplementer Evidence — Lojix Accidental Request Audit

## Task and scope

Read-only audit of the accidental live Lojix daemon request reported by the skill-editor worker:

- request: `Deploy System goldragon/ouranos FullOs Switch` using proposal source `/proposal` and `github:LiGoldragon/CriomOS`;
- reported immediate daemon reply: `(Deployed (25 (430 430)))`;
- determine what deploy id 25 did, whether running/active system or home generations changed, and what cleanup/follow-up is recommended.

No deploy, switch, activation, reboot, commit, or source edit commands were run. This output file is the only file written for the audit protocol.

## Guidance and surfaces consulted

- `/home/li/primary/AGENTS.md` from the supplied project context.
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md` and `/git/github.com/LiGoldragon/CriomOS/README.md` for CriomOS/Lojix repo role and deployment constraints.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix` for daemon service name and state directory.
- `/git/github.com/LiGoldragon/lojix/README.md` for daemon/read client architecture.
- `/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema` and `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema` for query/deploy request shapes.
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs` for query routing behavior while interpreting read-only surfaces.
- `agent-outputs/LojixDeploymentDoctrineFix/SkillEditor-Acceptance.md` for the exact accidental request and reported daemon reply.

## Commands run

All commands were read-only:

- `lojix '(Query (ByNode (goldragon ouranos None)))'`
- `lojix '(Query (ByGeneration 25))'`
- `lojix '(Query (ByEventLog (420 433)))'`
- `lojix '(Query (ByNode (goldragon ouranos (Some FullOs))))'`
- `lojix '(Query (ByNode (goldragon ouranos (Some HomeOnly))))'` with store hashes redacted in display for home output.
- `systemctl is-active lojix-daemon` and `systemctl show lojix-daemon ...`
- `journalctl -u lojix-daemon --since ...` filtered around the accidental request.
- `systemctl show lojix-self-switch-deploy-25.service ...` and `journalctl -u lojix-self-switch-deploy-25.service ...`.
- Read-only symlink/status checks for `/nix/var/nix/profiles/system`, `/run/current-system`, `/run/booted-system`, `/home/li/.local/state/nix/profiles/home-manager`, and `nixos-version`.
- `bootctl status --no-pager` and a read-only check for `/boot/loader/entries/nixos-generation-134.conf`.
- `systemctl is-active mirror.service` and `systemctl show mirror.service ...`.
- `find /var/lib/lojix -maxdepth 3 -type f ...`.
- `jj status --no-pager`.

## Observed facts

### Lojix daemon/query state

- `lojix-daemon` is active/running; `ExecMainStartTimestamp` is `Sat 2026-06-20 13:55:18 CEST`.
- The Lojix database marker observed by ordinary queries is `(432 432)`.
- `Query ByGeneration 25` returned an empty generation list at marker `(432 432)`.
- `Query ByNode goldragon/ouranos Some FullOs` returned only FullOs current entries with generation/deployment identifiers `19` and `20`; id `25` is not listed current.
- `Query ByNode goldragon/ouranos Some HomeOnly` returned HomeOnly current entries through id `24`; no id `25` HomeOnly entry exists.
- `/var/lib/lojix/lojix.sema` is the daemon state file and was last modified at `2026-06-30 00:25`.

### Deploy id 25 journal evidence

- The daemon journal shows deploy id 25 reached the activation phase, not merely admission.
- At `2026-06-29 16:23:31 CEST`, `lojix-daemon` logged `lojix deploy pipeline effect failed at Activate` for `lojix-self-switch-deploy-25`.
- The activation command included:
  - `nix-env -p /nix/var/nix/profiles/system --set ...`;
  - `switch-to-configuration switch` for the same redacted system closure;
  - boot entry default/oneshot update commands that would have run after switch success.
- The same daemon log then recorded terminal output `DeployRejected(... BuilderUnreachable ... marker 430)`. The rejection reason appears misleading for an activation failure, but it is the daemon's recorded terminal output.
- `journalctl -u lojix-self-switch-deploy-25.service` shows the transient unit started at `16:23:24`, ran `switch-to-configuration switch`, stopped/restarted units including `home-manager-li.service`, then failed with `status=4/NOPERMISSION` at `16:23:31`.
- The switch failure was associated with `mirror.service` failure during activation; `mirror.service` is currently still `activating (auto-restart)` with `Result=exit-code`.

### Current system and boot state

- `/nix/var/nix/profiles/system` currently points to `system-134-link`.
- `/run/current-system` and `/nix/var/nix/profiles/system` resolve to the same system closure basename observed in the deploy-25 activation logs, with the store hash redacted here.
- `/run/booted-system` resolves to a different system closure, so the booted generation and the currently switched generation differ.
- `nixos-version` reports `26.05.20260422.0726a0e (Yarara)`.
- `bootctl status` reports:
  - current boot loader entry: `nixos-generation-131.conf`;
  - default entry: `nixos-generation-133.conf`.
- `/boot/loader/entries/nixos-generation-134.conf` exists, but boot default remains generation 133. The deploy-25 activation did not make generation 134 the default boot entry.

### Current home state

- `/home/li/.local/state/nix/profiles/home-manager` currently points to `home-manager-823-link`.
- `home-manager-823-link` was created at `2026-06-29 16:21`, before the deploy-25 transient unit at `16:23`.
- The current home profile basename matches the Lojix HomeOnly generation/deployment id `24` closure from the ordinary query, with the store hash redacted here.
- `home-manager-li.service` was restarted by the deploy-25 switch and completed successfully from `16:23:26` to `16:23:31`, but no new home-manager profile generation was observed from deploy id 25.

### Event-log read surface limitation

- `lojix '(Query (ByEventLog (420 433)))'` did not return event-log entries; it returned the live generation listing.
- Source inspection explains this: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1535-1541` routes every ordinary `Query` selection except `ByTestRun` to `QueryGenerations`, and `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:2750` makes `ByEventLog` match every live generation. `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1751-1754` would reject `EventLogRead` even if reached.
- Therefore, journal evidence was the usable read-only event surface for this audit.

## Interpretation

- Actual state mutation occurred. Deploy id 25 did not stop at daemon admission; it attempted activation on `goldragon/ouranos` and ran enough of `switch-to-configuration switch` to make generation 134 the live current system.
- Lojix did not record deploy/generation id 25 as current in its ordinary generation listing, because the pipeline ended in a rejection/failure after activation partially succeeded.
- Home state was reactivated as part of the system switch, but the durable/current home profile appears to remain the pre-existing HomeOnly generation 823 / Lojix id 24.
- Reboot persistence was not changed to the accidental generation: boot default remains generation 133, while current live/profile generation is 134 and current booted generation is 131.

## Changed files

- `agent-outputs/LojixAccidentalRequestAudit/CriomosImplementer-Evidence.md` — this audit evidence file.

No source files, cluster files, daemon state files, or deployment files were edited by this audit.

## Recommended cleanup and follow-up

- Operator should decide whether to keep the currently switched system generation 134 or intentionally return to a known-good generation using the normal authorized deployment/rollback path. I did not run rollback or switch commands.
- Treat Lojix state for deploy id 25 as inconsistent with host reality: the host is live on the deploy-25 closure, but Lojix lists only prior FullOs ids 19/20 as current.
- Investigate/fix the Lojix ordinary event-log query surface so `ByEventLog` can return actual deployment events; current behavior hides exactly the evidence needed for this audit.
- Investigate the deploy pipeline's terminal rejection reason for activation failures: `BuilderUnreachable` does not describe the observed `switch-to-configuration`/unit failure.
- Investigate `mirror.service` failure separately; it caused or contributed to the non-zero switch result and is still auto-restarting.

## Residual risks

- I did not read or decode `/var/lib/lojix/lojix.sema` directly, so durable internal tables were inferred through ordinary queries plus daemon journal logs.
- Because no rollback/switch was authorized, the machine remains live on system profile/current generation 134 at the end of this audit.
- Boot default is still generation 133; a reboot may not preserve the currently live generation 134 unless an operator intentionally changes boot state.
