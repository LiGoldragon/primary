# Land + Pre-Deploy Validation Round — Evidence

## Scope (coordinator)

Land the guest-networking fix + reconcile test fixtures + prove the prometheus
toplevel BUILDS green + stage the single careful `BootOnce` deploy — but STOP
before the live switch (psyche is confirming switch timing; prometheus is also
their Wi-Fi router).

## 1. Landed: guest-networking fix → CriomOS main

CriomOS main is now **`ee49b203d565`** (rebased `vm-guest-networking` onto the
current main, which already carried the `/128` fix + peer commits; clean, no
conflict — the fix touches only `test-vm-host.nix` + `router/default.nix`).
Verified on main: `router/default.nix` carries the 6 `vmt*` rule lines; the
guest tap-binding + `fe80::1` gateway are in `test-vm-host.nix`. This is the
sandbox-proven fix (nested `runNixOSTest` green, ping+TCP A↔B).

## 2. Test-cluster fixtures — NOT reconciled (genuine rabbit hole; recorded as follow-up)

Per your "don't force it" instruction. Root cause found: the test-cluster's
`clusters/fieldlab.nota` is on the OLDER **4-root** ClusterProposal schema, but
horizon-rs main expects **5 roots** (`expected ClusterProposal to hold 5 root
objects, found 4`), and the branch's pinned (4-root-compatible) horizon-cli hits
the fenix rust-stable FOD hash bomb. Regenerating needs either fixing the fenix
pin or migrating `fieldlab.nota` to 5-root — both out of scope. The nested
reachability check itself already passed via `--override-input` and does NOT
depend on `projections-match`; the goldragon datom is already 5-root and projects
fine, so this is test-hygiene only, not a deploy blocker. Recorded as a follow-up
bead (label `follow-up`, `persistent-spirit-mirror`). The test-cluster branch
`nested-vm-reachability` @ `82e49807557d` stays pushed-but-unlanded.

## 3. Prometheus toplevel BUILD proof (build-only, non-activating)

Using the faithful, SAFE lever: `meta-lojix` System **`Build`** action = lojix
`HostDeployAction::Realize` (verified from lojix source: builds the full closure
on-target but does NOT copy/activate — touches no boot profile). This exercises
lojix's EXACT deploy pipeline (flake resolve → horizon materialize → eval →
build) minus activation, and stages the generated-inputs for the subsequent
BootOnce. Meta System-action atoms confirmed: `Eval/Build/Boot/Switch/Test/
BootOnce` (`Build`→Realize, `BootOnce`→ScheduleBootOnce).

Submitted (admitted, deployment id **38**):
```
meta-lojix "(Deploy (System (goldragon prometheus FullOs \
  /git/github.com/LiGoldragon/goldragon/datom.nota \
  github:LiGoldragon/CriomOS/ee49b203d565 Build None [] None)))"
-> (Deployed (38 (630 630)))
```
Builds on prometheus (build-on-target, lojix 0.3.10). Baseline generation
UNCHANGED throughout (`1 1 ... FullOs BootOnce Current`), confirming no
activation. **Build result: PENDING** (polling `lojix Query (ByNode ...)` for the
deployment-38 built-closure record). Result + closure path to be appended.

## 4. Staged BootOnce (DO NOT RUN until psyche confirms switch timing)

The single careful switch, ready to run next round (identical to the Build
command with `BootOnce` in place of `Build`):
```
meta-lojix "(Deploy (System (goldragon prometheus FullOs \
  /git/github.com/LiGoldragon/goldragon/datom.nota \
  github:LiGoldragon/CriomOS/ee49b203d565 BootOnce None [] None)))"
```
`BootOnce` (→ ScheduleBootOnce) is prometheus's established safe action (its only
prior lojix generation used it); it stages the new generation for one boot with
automatic rollback safety, matching the weave plan's "BootOnce, never Switch".

### Post-switch verification plan (next round, on the metal)
1. `lojix "(Query (ByNode (goldragon prometheus None)))"` until the new gen is
   `Current` with the expected closure path (the one the Build produced).
2. `ssh root@prometheus systemctl is-system-running` = running; confirm existing
   services healthy (tailnet, NixBuilder, NixCache, router Wi-Fi, sshd) — the
   `vmt*` firewall rules are additive/scoped and must not have disturbed them.
3. Boot the guests: `systemctl start microvm@mirror-alpha microvm@mirror-beta`.
4. Confirm A↔B on the metal: ping + TCP between `5::7` and `5::8` over the real
   taps (the exact thing the nested sandbox proved), plus the host reaches both.
5. Confirm the live `05-test-vm-vmt*.network` now shows `/128` routes + `fe80::1`,
   and the router forward chain carries the `vmt*` rules.

## Revs summary
- CriomOS main: **`ee49b203d565`** (fix landed).
- goldragon main: `824ffe6498c3` (mirror-alpha 5::7 / mirror-beta 5::8 — from the prior round).
- Test-cluster `nested-vm-reachability` @ `82e49807557d` (pushed, unlanded; fixture follow-up).
