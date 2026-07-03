# Deploy — primary-h945.2 ouranos live System Switch Landing Evidence

Autonomous overnight run, Wave 2 (deploy). Bead `primary-h945.2`. Role:
operating-system-implementer / deploy. Actor: Claude Opus 4.8 (1M context).
Target: CriomOS `main` @ `e4277192a53bb62ca1e909ad6c6017383468295f` deployed to
`goldragon`/`ouranos` via the live lojix System Switch. Deploy admitted
2026-07-04 01:48:27 CEST; switch finished 01:49:20 CEST.

## Verdict

SUCCESS. The System Switch activated cleanly (exit 0, no failed units,
`mirror.service` gone), the host lojix daemon self-upgraded 0.3.10 -> 0.4.1 and
is active, and the newly-persisted system generation 137 structurally carries
the guardian (spirit rev `7b0770642ab1`). Host reachable over SSH throughout.
One honest nuance on lojix's own ledger view (item 4) documented below; it is a
bookkeeping/observability gap, not a deploy failure — the OS-level source of
truth (running system, boot default, system profile) is fully on gen 137.

## Environment / precondition (STOP-gate cleared)

- `hostname` = `ouranos`. This primary environment IS the target host; the
  `User=li` lojix daemon drives the `root@ouranos` self-switch (same path as
  prior deploy id 25/38). Precondition satisfied.
- SSH preflight (exact daemon path, user li -> root@ouranos BatchMode key)
  returned `REACHED ouranos as root` before submit.
- Target confirmed pushed: `git ls-remote git@github.com:LiGoldragon/CriomOS.git`
  -> `refs/heads/main` = `e4277192a53bb62ca1e909ad6c6017383468295f` (deploy
  flake ref resolves from GitHub, not a local checkout).

## Deploy interface used

Running `meta-lojix`/`lojix` = `/nix/store/2a719h33...-lojix-0.3.10` (CLI ==
daemon version at submit time). Exact submitted request (9-field
`SystemDeployment`; shape verified against lojix source + prior working id-25/38
invocation; `Switch` is a recognized SystemAction on the 0.3.10 parser):

```
meta-lojix "(Deploy (System (goldragon ouranos FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/e4277192a53bb62ca1e909ad6c6017383468295f Switch None [] None)))"
```

Admission response: `(Deployed (41 (682 682)))` — deployment id 41, exit 0.
meta-lojix returns on admission; the daemon then ran build -> activate.

## Closure build result

Built at deploy time by the daemon (local build on ouranos; `builder = None`).
The deploy-time eval uses the real proposal source
`/git/github.com/LiGoldragon/goldragon/datom.nota`, so it built where local
flake eval cannot. Result closure (new toplevel):
`/nix/store/gdzdiv282ab7yigl0pzp45183fb4kmsj-nixos-system-ouranos-26.05.20260422.0726a0e`.
Build was fast (~90s admission-to-switch) — most store paths already present;
only the deltas (mirror removal, lojix 0.4.1, home input) realised. No build
failure.

## Verification checklist (1-5)

### 1. Switch exit 0, no failed units, mirror.service absent — CONFIRMED
Host-side switch journal (transient unit `lojix-self-switch-deploy-41.service`,
runs detached via `systemd-run --collect`):

- `01:49:20 nixos[...]: finished switching to system configuration /nix/store/gdzdiv282ab7...`
  (the success line; the failed id-38 showed `failed (status 4)` here instead).
- `lojix-self-switch-deploy-41.service: Deactivated successfully.` and the
  systemd-run script reported `Finished` (not Failed), including its
  `bootctl set-default nixos-generation-137.conf` step.
- NO `the following units failed` line (mirror.service is removed from the new
  generation, so nothing failed to start).
- `systemctl --failed` -> `0 loaded units listed`.
- `mirror.service`: `is-active` = inactive, `is-enabled` = `not-found`
  (`Unit mirror.service could not be found`) — the unit is gone from gen 137.
- `keyd.service` = active (keyboard input intact through the switch).

### 2. Host lojix daemon now 0.4.x and ACTIVE — CONFIRMED
The switch restarted `lojix-daemon.service` in place:
- Before: `/nix/store/2a719h33...-lojix-0.3.10`.
- After: `/nix/store/w36xr9rl5qhfaxj1ww7xn1pp5rkmg998-lojix-0.4.1`,
  `ActiveState=active`, `SubState=running`, started `01:49:19` (pid 1436297),
  clean start log, no errors.
Note: the user-profile CLI (`~/.nix-profile/bin/lojix`) still resolves to
0.3.10 — that is criomos-home's separate transitive lojix input (tracked by
`primary-7ile`), independent of the system daemon this item concerns.

### 3. Structural reboot-persistence (guardian) — CONFIRMED (no reboot performed)
- CriomOS `e4277192` `flake.lock` pins input `spirit` at rev
  `7b0770642ab1ad7807f36c43c7e6b09935d169b2` (`LiGoldragon/spirit`) and
  `criomos-home` at `329c93ec...`. So gen 137, built deterministically from that
  lock, carries the guardian rev `7b0770642ab1` by construction.
- Host corroboration: gen 137's home closure
  (`/nix/store/qcnqvqfra4pf4y33g2s51ylchyajsh0a-home-manager-generation`,
  = the current `home-manager-li.service` generation) contains `spirit-0.21.0`
  store paths.
- Boot persistence at the boot-profile level: system profile ->
  `system-137-link` -> `gdzdiv282...`; `bootctl` Default Entry =
  `nixos-generation-137.conf` ("Generation 137 ... built on 2026-07-04"). A
  reboot boots gen 137 by construction. (`/run/booted-system` still shows the
  old `c4kfjxxvb269...` only because the host was deliberately NOT rebooted.)

### 4. Host reachable over SSH + fresh ByNode Current record — MIXED (honest)
- Reachable over SSH: CONFIRMED. Post-switch
  `ssh -o BatchMode=yes root@ouranos.goldragon.criome` returned
  `POST-SWITCH-REACH ouranos gen=system-137-link`. Networking/ssh not broken.
- Fresh lojix ByNode Current record: NOT present. The 0.4.1 daemon answers
  `(Query (ByNode (goldragon ouranos None)))` with
  `(QueryRejected (GenerationUnknown (0 0)))` — its live generation ledger is
  empty (state marker 0/0). Cause: the switch stopped `lojix-daemon.service` at
  01:49:13 (mid-pipeline) BEFORE the driving 0.3.10 daemon committed deploy 41's
  activation record, and the successor 0.4.1 daemon came up on fresh generation
  state (0.4.x also changed the query vocabulary: old `FullOs` DeploymentKind arg
  is now an unknown `GenerationArtifact` variant; `Selection` no longer has
  `AllNodes`/`ByCluster`). This EXTENDS the scout's pre-existing "ByNode
  staleness" finding — the ledger was already diverged from the booted system
  before this deploy. It is a lojix-internal observability gap only; the OS-level
  source of truth (running system, boot default, system profile) is correctly
  and persistently on gen 137, and future deploys are unaffected (the pipeline
  records new generations regardless). Suggested follow-up: a lojix ledger
  reconcile / 0.3.10->0.4.x state migration, tracked separately (candidate note
  on `primary-usqs` or a new bead).

### 5. Running guardian = the persisted one (rev 7b0770642ab1) — CONFIRMED
- `spirit "(Version)"` -> `(VersionReported 0.21.0)`.
- Running `spirit` CLI resolves to
  `/nix/store/9p1px18v6clxa9ahf8l51arz31955c1j-spirit/bin/spirit`, which is one
  of the spirit store paths inside gen 137's persisted home closure
  (`qcnqvqfra...`). So the live guardian is the generation-137-pinned build, not
  merely the earlier transient home-path activation (that one was home gen 39
  `z26qd5...`; gen 137 pins its own home `qcnqvqfra...`). Combined with item 3's
  flake.lock proof, the running guardian is spirit rev `7b0770642ab1`.

## Safety

No connectivity loss; no rollback needed; host NOT rebooted (structural
persistence used, per brief). No host-state hack, no mirror-ledger op.

## Bead

`primary-h945.2` set in_progress at start; deploy executed and verified. Final
epic closure left to audit/closeout bead `primary-usqs` per the execution plan.
