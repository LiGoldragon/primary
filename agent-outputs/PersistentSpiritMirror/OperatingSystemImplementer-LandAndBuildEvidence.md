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
(`(Deployed (38 …))`).

### Activation state (IMPORTANT — BootOnce stages for next boot; it did NOT go live)

- Running system: **gen 49** (`/nix/store/2j08dj66…`, the OLD config) — HEALTHY
  (`is-system-running` = running; sshd, tailscaled, nix-daemon, nix-serve,
  hostapd, yggdrasil all active; no failed units; uptime 2d13h — no reboot).
- New **gen 50** (`/nix/store/61bajpa7…`, built 10:05 from `1bf35f801a07`) is the
  latest system profile generation and fully defines the guests
  (`microvm@mirror-alpha/beta`, `install-microvm-*`, tap-interfaces).
- Bootloader: `Current = gen 49`, `OneShot = gen 50`, `Default = gen 49`
  (`bootctl`). So gen 50 is staged for the NEXT boot ONCE, then reverts to gen 49.

**Consequence:** lojix `BootOnce` = `ScheduleBootOnce` = build + set the new gen as
the boot-once entry. It does NOT run `switch-to-configuration switch`, so the
running system is unchanged and the guests + networking fix are NOT live. This is
the inverse of "activate now, revert on reboot": here a REBOOT ACTIVATES gen 50
(booting it once), and a SECOND reboot reverts to gen 49. To boot
`mirror-alpha`/`mirror-beta` and run the on-metal A↔B proof, prometheus must
reboot into gen 50.

### ON-METAL RESULT (psyche-approved boot-once reboot done)

prometheus rebooted (new boot_id) and **booted gen 50** (`/run/current-system` =
`61bajpa7…`), NOT the old gen 49. Health: `is-system-running` = running; sshd,
tailscaled, nix-serve, hostapd, yggdrasil active; `nix-daemon.socket` active
(the daemon is socket-activated — `nix-daemon` inactive-until-used is normal); no
failed units. Both guests started; each has a persistent **40 GiB** host-side
`root.img` (auto-created), and each is a real `nixos-system-mirror-alpha/beta`.

**Guest-networking fix LIVE + verified on the metal:**
- taps `vmt0`/`vmt1` UP, each with the `fe80::1/64` gateway (the fix) + its sliced
  IPv4 endpoint;
- host `/128` routes `5::7 dev vmt0`, `5::8 dev vmt1`;
- nftables (live): `iifname "vmt*" oifname "vmt*" accept` (forward) +
  `iifname "vmt*" meta l4proto ipv6-icmp accept` (input); IPv6 forwarding = 1.

**host↔guest reachability (both guests):** `ping 5::7` 2/2, `ping 5::8` 2/2, 0%
loss; neighbor table shows `5::7 → 02:00:00:00:00:01 REACHABLE`,
`5::8 → 02:00:00:00:00:02 REACHABLE`. So both guests booted, bound their node IPs,
and the guest-side binding + host route + `fe80::1` gateway + NDP all work live.

**Guest-ORIGINATED A→B (ping+TCP from within alpha): NOT directly shown on the
metal — access limitation, not a networking gap.** The production guest is
minimal (`test-vm-host.nix` emits microvm + hostname + stateVersion + the
networking; NO sshd, no listening service, root locked; the microvm `-c` console
is broken on CriomOS — assumes `/etc/nixos`). So there is no way to get a shell
inside a guest to originate the packet. The guest console IS captured in the host
`microvm@<guest>` journal (clean multi-user boot seen), so the sandbox's
probe-via-journal method would work — but that needs a probe/sshd injected into
the guest config, which on the metal means a real guest-enterability change
(fuller guest built with sshd + keys) + another build/reboot. Every component of
the A→B path is live and verified on the metal (above), and the IDENTICAL config
proved guest→guest ping+TCP end-to-end in the nested sandbox
(`OperatingSystemImplementer-NestedReachabilityEvidence.md`).

**Persistence note:** gen 50 is boot-once — it reverts to gen 49 on the NEXT
reboot. NOT promoted to default (per the coordinator). The guests' `root.img`
persist regardless.

### ROUND: first-class nodes (standard SSH) + right-sized resources

Psyche corrections: (1) make the guests first-class goldragon nodes with standard
SSH (they were the stripped minimal test-VM profile — no sshd); (2) right-size
resources (40 GiB disk excessive).

**(1) How standard nodes get SSH — and the fix.** A standard CriomOS node gets
sshd keys-only from `normalize.nix` (`services.openssh` `PasswordAuthentication =
false`) and root's authorized keys from `users.nix`
(`root.openssh.authorizedKeys.keys = adminSshPubKeys`). The host-emitted TestVm
guest was minimal and imported neither. This is now fixed on CriomOS main —
commit **`17caaf88`** ("make TestVm guests loginable — sshd keys-only + admin keys
on the boot image") lifts exactly that standard access identity into the guest
boot image: `services.openssh.enable` + `PasswordAuthentication = false` +
`root authorizedKeys = horizon.node.adminSshPubKeys` (the host's projected admin
keys — an ex_node projection carries none of its own, and the operator who governs
the VM host governs its guests; `openFirewall` opens 22 on the guest tap). It is
generic to every TestVm guest. (This commit was authored in a parallel lane; the
delta from my prior deployed rev `1bf35f801a07` to `17caaf88` is exactly this one
clean commit — verified.) Deploying from `17caaf88` gives the guests standard SSH.

**(2) Right-sized resources** (goldragon main **`2fe644be`**): `mirror-alpha` /
`mirror-beta` shrunk from 4c / 8 GiB / 40 GiB to **2 cores / 4 GiB RAM / 8 GiB
disk** (lean but comfortable for a Spirit + criome + mirror node). `vm-testing`
left unchanged. Projection verified: both mirror nodes now `cores 2, ramGb 4,
diskGb 8`. NOTE: the existing 40 GiB `root.img` are removed before restart so
`autoCreate` recreates them at 8 GiB (the guests hold no data yet).

**Reactivation — NO host reboot (guest-only + firewall-only live activation).**
Build green from `17caaf88` + resized datom (closure `rjzsh3…`). Per the psyche's
guest-only observation, avoided a host reboot: dry-activate showed the plan would
only stop/start `microvm@mirror-alpha/beta` (router services NOT in the plan), so
activated live via `switch-to-configuration test` (no bootloader change, reverts
on reboot). Router services' `ActiveEnterTimestamp` identical before/after — NONE
restarted. Stopped guests → removed the 40 GiB root.img → activated → started
guests → root.img recreated at exactly **8 GiB** (resize confirmed).

**Host-input firewall gap found + fixed (tcpdump-diagnosed).** After activation,
host→guest ssh timed out though sshd was up. tcpdump on `vmt0` showed the guest
SENDS the SYN-ACK but the host never accepts it — my `vmt*` input rule only
allowed ICMPv6, so the guest's TCP return traffic hit the router's default-drop
INPUT (ping worked precisely because ICMPv6 was allowed). Fixed on CriomOS main
**`3aa4780971e4`**: `iifname "vmt*" ct state { established, related } accept` on
input (return traffic for host-initiated guest connections; scoped to `vmt*`).
Its live activation (closure `j1362…`) dry-activated to **`reload nftables.service`
only** — no router-service restart, no guest restart; verified router timestamps
unchanged. host→guest ssh then completed the TCP handshake.

**ON-METAL GUEST-ORIGINATED A→B PROOF (the payoff).** SSH'd into `mirror-alpha`
(ouranos → prometheus jump → alpha, authenticated with the cluster admin key —
`hostname=mirror-alpha`, `inet6 5::7/128`, `default via fe80::1 dev eth0`). From
inside alpha to beta `5::8` over the tap path:
- **ping:** `3 packets transmitted, 3 received, 0% packet loss`;
- **TCP connect to beta:22:** `Connecting to 5::8 port 22` → `Connection
  established` → `Server host key: ssh-ed25519 SHA256:HnASStrFOeQU…` (auth then
  declined, as expected — the TCP + ssh handshake to beta completed over the tap).

**Final health:** prometheus `is-system-running` = running, no failed units, all
router services active; both guests active with 8 GiB root.img. NOT promoted —
running config is a `test` activation, bootloader default unchanged, reverts on
reboot. Revs: CriomOS main **`3aa4780971e4`**, goldragon main **`2fe644be`**.

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
