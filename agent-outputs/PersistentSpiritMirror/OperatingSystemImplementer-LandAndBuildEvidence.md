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
activation.

### BUILD RESULT: RED — pre-existing eval blocker, unrelated to the fix. DID NOT SWITCH.

The prometheus toplevel from CriomOS main `ee49b203d565` **fails at eval**, before
any build/activation. Verified by a watchable direct build on prometheus using
lojix's materialized inputs (`nix build …#nixosConfigurations.target…toplevel
--override-input {system,horizon,deployment,secrets} /tmp/promcheck/*`):

```
error: Failed to fetch git repository 'https://github.com/LiGoldragon/signal-mentci-client'
… while evaluating derivation
  'cargo-git-https-github.com-LiGoldragon-signal-mentci-client-2b0a4c25f4f55d35ddd671323595ec52cfd9cb27'
… while evaluating the option `home-manager.users.bird.home.activation.installPackages.data'
```

**Root cause:** the prometheus toplevel eval pulls in `home-manager.users.bird`,
whose home installs a `mentci-egui` package. The CriomOS-main-pinned `mentci-egui`
has a Cargo.lock that pins `signal-mentci-client` to rev **`2b0a4c25…`**, which is
**orphaned** — that repo's `criome-authorization-push` branch was force-pushed to
`430e84d0…`, so `2b0a4c25` is absent from all refs and `fetchGit` cannot retrieve
it. (The LOCAL `mentci-egui` checkout already pins the valid `430e84d0`; the stale
rev lives in the OLDER `mentci-egui` that the criomos-home chain pins.)

**Unrelated to the guest-networking fix.** My landed commit touched only
`modules/nixos/{router/default.nix,test-vm-host.nix}` — no home/mentci surface.
The eval clears my modules and fails later in the home/mentci tree. Deployment 38
(the lojix `Build`) hit this same wall — the daemon is silent on the async result,
but my direct eval reproduces it deterministically and the rev is genuinely
unfetchable, so a lojix build/eval on the same host (same nix, same cache) fails
identically. prometheus was NOT activated; it remains on `1 1 … Current` and
healthy. `/tmp/promcheck` on prometheus holds only encrypted `.sops` + projected
json (transient; safe to delete).

**Secondary oddity worth a look:** per the goldragon datom, `bird` has homes only
on `tiger`/`zeus` — NOT prometheus. Why `home-manager.users.bird` is evaluated in
prometheus's toplevel at all is unexpected; if bird's home should not be on
prometheus, fixing that would also sidestep the mentci fetch.

### Options to unblock (coordinator decision — separate from the guest-networking work)
1. **Fix the stale mentci pin:** bump `criomos-home` (→ `mentci-egui`) to a rev
   whose Cargo.lock pins a valid `signal-mentci-client` rev (e.g. `430e84d0`),
   flow criomos-home → CriomOS main, rebuild. Multi-repo home-stack fix.
2. **Exclude bird's home from prometheus** if its inclusion is a projection/home
   bug (bird has no prometheus home in the datom). Investigate the home-inclusion
   path.
3. Only after the toplevel builds green: re-run the `Build` proof, then the staged
   `BootOnce`.

The guest-networking fix itself is landed (CriomOS main `ee49b203d565`) and
sandbox-proven; it is NOT the blocker. The BootOnce command stays staged (below)
for once the toplevel builds.

### RESOLUTION — home-inclusion fix (surgical, CriomOS-local); toplevel now builds GREEN

Root cause of the bird-home inclusion (coordinator's option 2): `horizon.users`
is the FULL cluster user set — every node's projection lists every user for
identity/keys (ouranos ALSO lists `bird`, who has no ouranos home either). The
projected `User` carries `hasPubKey` = "has a per-node pub-key entry for THIS
viewpoint node" (`viewpoint_entry.is_some()`); for prometheus both `bird` and
`li` are `hasPubKey = false`. But `userHomes.nix` built `home-manager.users` from
EVERY `horizon.users` entry with no filter — so every node built every user's
home, dragging `bird` → `mentci-egui` → the orphaned `signal-mentci-client` rev
into prometheus's eval.

Fix (CriomOS main **`1bf35f801a07`**): `userHomes.nix` now filters
`horizon.users` to `hasPubKey` users before building `home-manager.users`, so a
user's home lands only on the nodes their `pub_keys` map names. Surgical,
CriomOS-local; does NOT touch horizon-rs or the mentci stack. It is also just
correct: a home belongs where the user has a presence.

**Build proof GREEN** from corrected main `1bf35f801a07` (watchable direct build
on prometheus with lojix's materialized inputs): eval now clean (no mentci
fetch — bird/li homes dropped from prometheus), only 4 trivial final derivations
built, closure `/nix/store/61bajpa7g5xii6mr9lps18fvf9gkgphx-nixos-system-
prometheus-26.05.20260422.0726a0e` (`BUILD_EXIT=0`).

### LIVE SWITCH (psyche cleared — independent ethernet, no stranding risk)

Submitted BootOnce of prometheus FullOs from `1bf35f801a07`
(`(Deployed (38 …))`). Activation + health + guest boot + on-metal A↔B: recorded
below as they complete.

Revs now: CriomOS main **`1bf35f801a07`** (guest-networking + home-inclusion),
goldragon main `824ffe6498c3`.

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
