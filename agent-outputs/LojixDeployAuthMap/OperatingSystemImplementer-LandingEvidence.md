# Operating-System Implementer — Guardian Landing + Activate-Bug Fix Evidence

Landed the sharpened Spirit guardian prompt live on `goldragon/ouranos` and
pinned + fixed the local home-activate bug. This report records the durable
findings, corrects the scout's leading root-cause hypothesis, and names what is
deferred to the deployment-decoupling audit. Companion:
`Scout-SituationalMap.md` (read-only recon this builds on).

## Headline

- Guardian prompt is LIVE: spirit `0.21.0` (rev `7b0770642ab1`) running in
  `spirit-daemon`, home generation past 835, guardian authorizes writes.
- The scout's leading hypotheses (`sd-switch` vs degraded user systemd; the
  daemon's session-less env; `session-bind@openssh.com`; `BuilderUnreachable`)
  were all WRONG. The TRUE cause was a home-manager file collision on
  `~/.ssh/config`.
- The durable fix is minimal and needs NO lojix user-service conversion; the
  daemon's own Home Activate now succeeds. User-service conversion /
  deployment-decoupling stays with the audit worker.

## Task 1 — Guardian prompt live (done)

Built current CriomOS-home `main` (`e319468fe6`, which carries the PATH-module
fix `81ad1c56` + `flake.lock` spirit pin `7b0770642ab1`) and activated it
through li's healthy login session (not the daemon path).

- Build method (validated to reproduce the daemon's drv exactly): `nix build`
  of `github:LiGoldragon/CriomOS-home/<rev>#homeConfigurations.li.activationPackage`
  with `--override-input horizon|system|secrets path:/var/lib/lojix/generated-inputs/goldragon/ouranos/home/*`
  (the local `stubs/no-horizon` has empty `users`, so the real horizon override
  is required). Building `81ad1c56` this way reproduced gen-836's exact deriver
  `qgrdrqi0…-home-manager-generation.drv`, proving the method matches the daemon.
- New generation: `home-manager-837-link` → `/nix/store/z26qd5vmwxdvz31a30cbnnbdbzhm7dmk-home-manager-generation`.
- `spirit-daemon` + `agent-daemon` restarted onto the new build with the module
  `Environment=PATH=/home/li/.nix-profile/bin:/run/current-system/sw/bin:/run/wrappers/bin`;
  `gopass` resolves on that PATH.
- Verification:
  - `spirit "(Version)"` → `(VersionReported 0.21.0)`.
  - live daemon store `70ngyprxb069…-spirit` (built from the `7b0770642ab1` lock).
  - reads: `spirit "(Count …)"` returns; `Lookup` returns real records.
  - write authorized: a probe `Record` returned `(GuardianRejected
    (MissingTestimony …))` — the guardian resolved its key, called the provider,
    reasoned over existing intent (cited `jlo7`,`c5nq`,`obo5`), and rejected the
    agent-issued testimony. That is the guardian ALIVE (not `DaemonUnconfigured`),
    and it created no record.
- Removed the redundant hand-placed `10-guardian-secret-path.conf` drop-ins
  (spirit + agent) after confirming the module PATH; re-verified the guardian
  still authorizes on the module PATH alone.

## Task 3 — True activate failure (pinned)

Reproduced the activate under li's healthy session with a full trace. It aborted
early, well before `reloadSystemd`:

```
Activating checkLinkTargets → checkNewGenCollision
Existing file '/home/li/.ssh/config' would be clobbered
+ exit 1
```

`/home/li/.ssh/config` existed as a REAL file (`-rw-------`, mtime Jul 2 18:46)
holding the prometheus builder ssh alias — the hand hack that commit `3738e2f`
("declare prometheus builder ssh alias (fold local hack)") folded into
declarative config. The new generation manages `.ssh/config`, so home-manager's
`checkNewGenCollision` refused to clobber the un-managed file and exited 1
(under `set -euo pipefail`), before `nix-env --set`. The daemon captured empty
stderr and mislabeled it `BuilderUnreachable`.

This is NOT `sd-switch`/degraded-systemd, NOT the daemon's missing
`XDG_RUNTIME_DIR`/DBUS, NOT orchestrate, NOT SSH/`session-bind`. The gpg-agent
`session-bind` journal lines were coincidental, as the scout suspected.

## Task 4 — Durable fix (applied, safe scope only)

Two minimal, intended changes — both completing declarative transitions already
committed to `main`, so neither is duct-tape:

1. `~/.ssh/config`: moved the now-redundant real file to
   `~/.ssh/config.hm-backup-20260703`; home-manager now manages `.ssh/config`
   as a store symlink (the declared version is a superset — the same prometheus
   alias plus the standard `Host *` block).
2. `orchestrate-daemon`: transitioned from the hand-started process
   (`setsid nohup`, PID 58903, held the `orchestrate.redb` write-lock, `lsof`
   FD `6uW`) to its systemd `--user` unit added in `faf8c23`. This was a
   SECONDARY blocker: with the manual process holding the redb lock, `sd-switch`
   could not start the new `orchestrate-daemon.service` (redb is single-writer),
   which would have failed any full activate at `reloadSystemd` regardless of
   session health. Stopped 58903 so the systemd unit binds cleanly; durable
   claims in redb survive; orchestrate healthy after (`Observe Roles` returns).

Verification that the daemon path is durably unblocked: re-submitted the deploy
THROUGH the daemon — `meta-lojix "(Deploy (Home (goldragon ouranos li … e319468fe6… Activate None [])))"`
→ `Deployed(AcceptedDeploy id 39)`, no `effect failed` line, daemon gen tracking
re-synced to `z26qd5…`. So the daemon's own local activate now succeeds; NO
user-service conversion was required.

Host-safety note: home activation only touches li's USER services + files. The
`lojix-daemon` is a SYSTEM unit; its working operations (build, boot-once,
admission, `ssh root@node` SYSTEM deploys) were never in the blast radius and
were not touched.

## Task 2 — Mislabel fix (LANDED + pushed, source-only)

Typed cross-repo fix, both commits on `main == main@origin`, verified:

- `meta-signal-lojix` `4a8e79112d71` "add ActivationFailed deploy rejection
  reason". `DeployRejectionReason` gains `ActivationFailed` appended LAST
  (rkyv discriminants preserved → wire-compatible). `build.rs` GENERATES
  `src/schema/lib.rs` from `schema/lib.schema` (source of truth); the schema
  list + comment blocks were edited and `lib.rs` regenerated via
  `META_SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`. Added test
  `tests/round_trip.rs::activation_failed_reason_round_trips_through_nota_text`.
  `cargo build` (runs write_or_check) + `cargo test --features nota-text` pass.
- `lojix` `a35533348112` "map Activate-stage deploy failure to ActivationFailed".
  `src/schema_runtime.rs:2611` → `Activate => ActivationFailed`; `2610`
  (`CopyClosure => BuilderUnreachable`) unchanged. No detail field added —
  `fail_pipeline` already `eprintln!`s `failure.detail`. No exhaustive-match
  arms needed (verified by grep; no `match` scrutinises a `DeployRejectionReason`
  value). `cargo build/test --locked --offline` pass; `nix build
  .#checks.x86_64-linux.build` exit 0 (crane vendored the pushed contract rev
  `4a8e7911`, built `lojix-0.4.0` on prometheus).

Source-only; the running daemon stays 0.3.10 (NOT redeployed). A `cargo update
-p meta-signal-lojix` was blocked by upstream `nota-next` main drift past the
workspace pin `c43d04a1`; the meta-signal-lojix rev was instead bumped via a
surgical `Cargo.lock` edit (equivalent to `--precise`), confirmed by
`--locked --offline` build + the crane `nix build`. Reconciling `nota-next`'s
pin drift is out of scope.

## Deferred (owned elsewhere)

- User-service conversion of lojix / deployment-agnostic decoupling → audit
  worker's proposal. Not needed for THIS bug; the daemon path is already fixed.
- Reboot persistence: a live home activation still needs a matching SYSTEM
  generation pinning the same home input; not in this safe scope.
- Recurring hygiene: hand-placed dotfiles (e.g. `~/.ssh/config`) that a later
  commit declares will collide on the next activate. Worth a standing cleanup
  discipline (back up + let home-manager adopt) or a `-b backup` deploy path.
- Observation: `spirit "(Count …)"` reports 20 live records (store file ~964 KB,
  not wiped; guardian cites real records). Likely the Jul-2 v10→v11
  strict-positional migration (`c5a0312`) semantics, predating this work — flag,
  not caused here.

## Evidence pointers

- Activate trace: scratchpad `activate-all.log` (collision), `activate-run2.log`
  (clean exit 0).
- `journalctl -u lojix-daemon.service` — 10:34 failure (`BuilderUnreachable`,
  empty stderr) vs 16:20 success (`AcceptedDeploy 39`).
- `~/.ssh/config` (now a home-manager symlink), `~/.ssh/config.hm-backup-20260703`.
- Bead `primary-7t97` (closed, annotated).
