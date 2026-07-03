# Coordinated Home Redeploy — declarative guardian PATH + spirit bump

## Task and scope
Psyche-approved heavier action: one coordinated criomos-home redeploy carrying
(1) a declarative/permanent guardian PATH fix (superseding the hand-placed
drop-ins) and (2) a spirit flake-input bump to main tip `7b0770642ab1` so the
rebuilt daemon carries the sharpened guardian prompt (compiled via
`include_str!`). Target: cluster goldragon, node ouranos, user li, shape Home,
action Activate.

## Changes committed and pushed (CriomOS-home main 81ad1c56532810ecfc9e52454228f2222ea633d6)
File `modules/home/profiles/min/spirit.nix`:
- Added `guardianServicePath = lib.concatStringsSep ":" [ "${config.home.homeDirectory}/.nix-profile/bin" "/run/current-system/sw/bin" "/run/wrappers/bin" ]`.
- Added `Environment = [ "PATH=${guardianServicePath}" ];` to BOTH
  `systemd.user.services.agent-daemon.Service` and `.spirit-daemon.Service`
  (neither previously set `Environment`; the guardian model call runs in
  agent-daemon, so both need it). No secret value is embedded — only the search
  path the daemon uses to fetch the secret itself from gopass at runtime.

File `flake.lock`:
- Bumped input `spirit` `05269499a928d54fe5f8e842e5f5436f1ca7bfbc` ->
  `7b0770642ab1ad7807f36c43c7e6b09935d169b2` via
  `nix flake lock --override-input spirit github:LiGoldragon/spirit/7b0770642ab1`
  (deterministic pin; not `nix flake update`).
- What else the bump pulls in: NOTHING unrelated. Diffing flake.lock nodes
  before/after, exactly one node changed (`spirit`). Shared/transitive inputs
  (`signal-spirit-source`, `meta-signal-spirit-source`, `agent`, `nixpkgs`)
  are unchanged, so the daemon rebuilds against the same schema/contracts; only
  the spirit source (guardian prompt + manual/docs on the same branch) changes.

## Pre-push validation (passed)
- `nix build github:LiGoldragon/spirit/7b0770642ab1#packages.x86_64-linux.default`
  -> success (store path `/nix/store/sk74z2605ld90zyf636j91ck1bscm1cy-spirit`),
  built on the prometheus remote builder via the nix-daemon.
- `nix build .#checks.x86_64-linux.spirit-deployment` -> success (validates the
  module edit + config generation; uses stub spirit/agent).

## Deploy attempt and FAILURE (live activation blocked)
Cautious two-phase via `meta-lojix`:
- `Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/81ad1c56... Build None []))` -> admitted `(Deployed (39 ...))`.
- `Deploy (Home (... Activate None []))` -> admitted `(Deployed (39 ...))`.

Result: the new generation BUILT (home-manager generation 836,
`/nix/store/gic8cd5h6avhyrcbwmzikl2iz2m0v253-home-manager-generation`, confirmed
to reference the new spirit `sk74z2605...`), the profile *generation* pointer
moved to 836, but the `activate` effect FAILED:
`lojix deploy pipeline effect failed at Activate: .../gic8cd5.../activate exited with exit status: 1`,
terminal `DeployRejected(... reason: BuilderUnreachable ...)`.

### Root cause of the deploy failure (diagnosed)
- `BuilderUnreachable` is lojix's GENERIC "an Activate effect failed" label, not
  a literal builder outage: the earlier system deploy 38 — a clear
  `status=4/NOPERMISSION` error — was labelled `BuilderUnreachable` too.
- Prometheus is NOT down: the spirit build copied from it successfully via the
  nix-daemon (root's builder key). The interactive `nix store info` "Permission
  denied" is only my shell lacking the builder key.
- Real signal (li-user journal 10:34:00-05): SSH sign-requests via gpg-agent
  with `ssh-agent extension 'session-bind@openssh.com' not supported` — an
  SSH/builder-auth step in the lojix home pipeline failed. lojix did NOT surface
  the activate stderr.
- The activate failed EARLY, before `linkGeneration`/service restart: no
  spirit/agent restart entries in the journal; `~/.config/systemd/user/*.service`
  symlinks are still the OLD gen (old spirit `52f52g45`, zero `Environment`
  lines); `NeedDaemonReload=no`. So NO live service was touched.

This blocker is in the lojix home-activate pipeline, not in the module change or
the spirit rev.

## Rollback performed (system restored to known-good)
`nix-env --switch-generation 835 -p ~/.local/state/nix/profiles/home-manager`
moved the profile pointer 836 -> 835 (the pre-deploy generation), restoring
consistency with the on-disk `~/.config` files. No activation was run.

## Current live state (safe)
- spirit-daemon PID 109842 and agent-daemon PID 112451 unchanged, running the
  OLD spirit rev with the hand-placed `10-guardian-secret-path.conf` drop-ins
  providing the guardian PATH.
- Reads healthy (`PublicRecords` returns records). Guardian proven working
  earlier this session.
- The sharpened guardian prompt (spirit 7b0770642ab1) is NOT yet live; the
  drop-ins remain the live PATH mechanism (the declarative module PATH is
  committed but not activated).
- The hand-placed drop-ins were NOT removed (the module fix did not go live, so
  removing them would reintroduce the original DaemonUnconfigured failure).

## Options to land it (recommendation)
1. RECOMMENDED: investigate/fix the lojix home-activate SSH/builder-auth step
   (gpg-agent ssh-agent lacks `session-bind@openssh.com`; the pipeline's
   copy/auth path for li), then re-run `Home Activate` against 81ad1c56... This
   is a lojix pipeline issue and heavier than a supervised restart, so it is
   surfaced rather than forced.
2. Land the built generation 836 via an activation path that does not depend on
   the failing SSH step (e.g. an operator-run `home-manager switch`/activate in
   li's interactive session), then verify and remove the drop-ins.
3. Defer: the declarative fix is committed; it will apply on the next successful
   full home deploy. The drop-ins keep the guardian working meanwhile.

After ANY successful activation: verify the daemon ExecStart references spirit
`sk74z2605...`, the unit carries the module `Environment=PATH`, reads work, a
write is authorized against the sharpened prompt, then `daemon-reload` + restart
after removing the now-redundant drop-ins and confirm PATH still resolves.

## Tracking
Bead `primary-7t97` (labels deploy, lojix, spirit, blocked).

## Secret hygiene
No token value written to any file, unit, log, bead, report, commit, or message.
The module change embeds only PATH, never a secret. gopass reads (earlier
session) used exit-status-only checks.
