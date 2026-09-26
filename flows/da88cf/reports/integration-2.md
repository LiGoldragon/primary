# Integration step 2: wifi, fixes, usb-downlink, tailnet; Home fixes

Integrator subflow of da88cf, on ouranos, 2026-09-25 23:40 to 2026-09-26 00:12 CST. Nothing was deployed or activated, and no `main` was moved. Evaluation ran on ouranos with `max-jobs 0`. Builds were offloaded to `ssh-ng://nix-ssh@prometheus.goldragon.criome`, one at a time. Grades: **W** = witnessed here, **C** = claimed by another flow.

## Result

| Repo | Bookmark | Revision (verified with `git ls-remote`) | Base |
|---|---|---|---|
| CriomOS | `integration-2-da88cf` | `c5ddf3a80f0a0d8b3a79bef165a692704bec9bde` | main `3e2cc8be`, then merged with the new main `e6a83edc` |
| CriomOS-home | `integration-2-da88cf` | `98255d100e9627f30b2e66e0772801a100cdfc03` (= `home-fixes-da88cf`) | main `4a9d85d7` |

CriomOS main `e6a83edc` is a descendant of neither step-2 branch. `c5ddf3a8` descends from `e6a83edc`, so main can fast-forward to it.

Workspaces: `~/wt/github.com/LiGoldragon/{CriomOS,CriomOS-home}/integration-2-da88cf`. Locks 7002 and 7003 are released.

## Revisions used (each verified on the remote before use, W)

- `wifi-country-da88cf` = `71ab4707` (742f03d3 and 71ab4707)
- `criomos-fixes-da88cf` = `30c7cbac` (9cafc0c6, 7556680b, 66aad7c9, 30c7cbac)
- `usb-downlink-da88cf` = `946bcbd5`
- `tailnet-repair-da88cf` = `216b4035`. Its base is `d193bafc`, an ancestor of `3e2cc8be`.
- `home-fixes-da88cf` = `98255d10`. This was the head when I reached it, after the Herdr settlement (3e49e714, 98255d10) landed on top of `bdc215d0`.
- goldragon `tailnet-repair-da88cf` = `a3fdb232`. It was still the head at 00:00; no CA was recorded yet. goldragon main has moved to `0d462a33` ("secrets: add Ouranos OpenCode password recipient"), which is not on the tailnet bookmark.
- horizon-rs main = `tailnet-repair-da88cf` = `a3ddaf86` (0.13.0)
- lojix main = `f090da07` (8.0.0)

## CriomOS merge order and conflicts (W)

jj merge commits, with no branch commit rewritten:

1. `72c34d09`: 71ab4707 merged with 30c7cbac. Clean.
2. `336a6228`: the above plus 946bcbd5. Clean.
3. `e106e6b2`: the above plus 216b4035. Clean.
4. `94479ca6`: `criomos-home.url` moved to `98255d10`, then `nix flake update criomos-home`. The lock diff touches only the criomos-home node.
5. `c5ddf3a8`: merged with main `e6a83edc` (lojix 8.0.0). Clean. The result is `lojix.url` = `f090da079f71…` (flake.nix line 105) and lock lojix = `f090da07`; `nix flake lock --no-update-lock-file` makes no change.

**Rebase or merge.** The main flow asked for a rebase onto `e6a83edc`. I merged instead. A rebase would have rewritten the pushed branch commits, which are immutable remote bookmarks. The merge gives the same tree, and the result is a descendant of main.

**No textual conflicts.** Overlaps that I checked by reading the merged diff:
- `flake.nix` check list: `tailnet-declaration` and `tailnet-enrollment` replace `headscale-selfsigned-cert`; `flake-registry-shape` and `router-wifi-radio` are added; `usb-downlink` and `usb-downlink-chain` replace `usb-ipv4-gateway`.
- `modules/nixos/router/default.nix`: the country throw, the regdom kernel param, hostapd `logLevel` 1 and the backup logger lines, and the `Wifi4/6/7` spelling (all from wifi) sit together with the `usbEthernet.networkdMatch` 05-usb-eth rule (from usb-downlink).
- `modules/nixos/network/default.nix`: `tailnet-trust.nix` and `usb-downlink.nix` are both imported.

**criomos-lib** is unchanged at `6db67c3b`.

**Lojix pin.** It is now `f090da07` (8.0.0), inherited from main `e6a83edc` as the main flow ordered. The earlier instruction to keep `a67f5773` is superseded.

## Stale-lock candidate (W)

- Lock 907 `CriomosRemainingHorizonFixtureMigration` belongs to flow **542442**, which is **not in `hm-list`**. So are its locks 846, 850, 851, 856, 868–870, 890, 898, 900, 902, 903, 905, 908, 910, 911, 914, 925, 937, 940, 844, 845 and 847.
- Lock 907 covers `…/CriomOS/horizon-flake-integration-542442/checks/headscale-selfsigned-cert/default.nix`, which the tailnet merge deletes. It lies in 542442's own worktree, not in the paths I used, so nothing was refused.

## Composed Horizon (W)

- The goldragon `a3fdb232` build of `#horizon-definition` gave `/nix/store/437hq4kc…-horizon-definition`.
- The `#horizon-cli` build gave `/nix/store/ahf5fwg8…-horizon-0.13.0` (horizon-rs `a3ddaf86`, from goldragon's lock).
- Both were already in the store, so there are no fresh offload lines.
- `horizon-cli --node <n> < horizon-definition.datom` produced `scratchpad/integrate-2/horizon-{ouranos,prometheus}/horizon.json`. Each has the generated `flake.nix` shape.
- Prometheus projects `country "MX"` and `wlanStandard "Wifi4"`.
- The tailnet controller has `certificateAuthority: null`.

## Evaluations of `c5ddf3a8` (W)

Overrides:
- `horizon` = the scratch dir above;
- `system` and `deployment` = `/var/lib/lojix/generated-inputs/goldragon/<n>/complete-host/…`;
- `secrets` as stated for each run.

**1. Toplevel with the generated secrets inputs: both fail.**
- **ouranos** fails with two assertions:
  - `tailnet: the TailnetController on ouranos carries no cluster CA certificate (base64 DER beginning MII); mint it and record it in cluster data`
  - `OpenCode testing requires inputs.secrets.sopsFiles.opencodeServerPassword`. The generated ouranos secrets input has an empty map.
- **prometheus** fails on the same CA assertion only. Prometheus is a TailnetClient, so it is blocked by design too.

**2. ouranos with a secrets override listing goldragon main `0d462a33`'s four files.**
- The override is `scratchpad/integrate-2/secrets-goldragon-main/`. It copies the ciphertexts (`localLlmApiToken`, `opencodeServerPassword`, `routerBackupWifiPassword`, `routerWifiSaePasswords`) with a `sopsFiles` flake, the way the generated Prometheus input is shaped.
- The OpenCode assertion clears. Only the CA assertion remains.
- **ouranos stops here** per the brief.

**3. Values below the assertions** (probe expressions `probe-{ouranos,prometheus}.nix`).
- **ouranos:**
  - UsbDownlink: networkd `05-usb-downlink` and `40-br-downlink`, netdev `20-br-downlink`, Kea on `br-downlink`, NAT internal `br-downlink`, NetworkManager unmanaged `interface-name:br-downlink`.
  - `tailnet-enroll` unit present; headscale enabled.
  - Home activation: `/nix/store/v0niixzgdsg0zahc1440is5v5hzr3f3v-home-manager-generation.drv`.
  - `security.pki.certificateFiles` fails to evaluate, because the CA is None.
- **prometheus:**
  - `cfg80211.ieee80211_regdom=MX`.
  - Radio `wlp195s0`: country MX, 2g, channel 6, `wifi4 = true`, `wifi6`/`wifi7` false, log level 1.
  - Router: `br-lan`, Kea, `networking.nat` off.
  - `llm-presets.ini` and `llm-models-dir` contain exactly `gemma-4-26b-a4b` and `qwen3.5-122b-a10b` (llama-router-start drv `lczry2s4…`).
  - It has no Home users.

**4. Probe only, not deployable.** This run shows what remains after minting.
- The inputs:
  - the tailnet-enrollment snakeoil fixture CA injected into scratch copies of both horizon.json;
  - the fixture sops files named as `headscaleTlsCertificate`, `headscaleTlsKey`, `tailnetPreauthKeyOuranos` and `tailnetPreauthKeyPrometheus`;
  - goldragon main's four files.
- With only the CA injected, the next stops are:
  - ouranos: `tailnet: inputs.secrets.sopsFiles.headscaleTlsCertificate is required …`;
  - prometheus: `… tailnetPreauthKeyPrometheus is required …`.
- With both injected, both toplevels evaluate:
  - ouranos `/nix/store/ys3hkz53sj0rk1shrf95858m8fng2hkb-nixos-system-ouranos-26.11.20260813.0e251e2.drv`
  - prometheus `/nix/store/3bd9jqwjisjcs0yw7bm6s0pfq80jm7md-nixos-system-prometheus-26.11.20260813.0e251e2.drv`
- **Consequence for deploy:** once Field records the CA and mints the secrets, Lojix's generated secrets input must carry the four goldragon files plus the tailnet secrets. Today's ouranos input is empty.

## Checks

**Check-set evaluation (`--apply builtins.attrNames`, with the system override):**
- **CriomOS-home `98255d10`: evaluates (W).** It lists 92 checks. The unfree and Herdr failures are gone.
- **CriomOS `c5ddf3a8`: fails (W)** with `MS2130 UVC patch must be reviewed for the selected kernel`. `checks/ms2130-uvc-aspect-quirk` pins kernel `7.0.1`; `linuxPackages_latest` is now `7.1.8` under both Home `4a9d85d7` and `98255d10`. The same error occurs on main `e6a83edc`, so it is **pre-existing** and was masked earlier by lojix-ownership.

**Per-check evaluation.** Each check was called through a scratch wrapper flake (`scratchpad/integrate-2/wrap`) that locks this workspace with a system override and uses the flake's own `pkgs`. These fail to evaluate on both `c5ddf3a8` and main `e6a83edc`, so all are pre-existing:
- `ms2130-uvc-aspect-quirk` (kernel pin);
- `opencode-testing-policy`: `attribute 'horizon' missing`;
- `resolver-role-policy`: `wireguardPublicKey` missing;
- `router-non-router-lazy`;
- `wireguard-untrusted-proxy`: `network` missing;
- `lojix-ownership`:
  - On main it fails on the old hard-coded lojix rev.
  - On the integration it passes every lock assertion.
  - It then fails at `attribute 'machine' missing` in Home `modules/home/profiles/min/default.nix:244`, because the check's own fixture horizon has no `node.machine`. This is a CriomOS fixture defect and is **not built**.

**Builds (W).** One at a time; each offload line reads `building '<drv>' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`.

| Check | Result | Drv built on Prometheus |
|---|---|---|
| router-wifi-radio | pass | `pgj135pl…-router-wifi-radio-check.drv` |
| router-wifi-horizon-policy | pass | `igr8lizs…-router-wifi-horizon-policy-check.drv` |
| router-usb-downlink-binding | pass | `2l528bwz…-router-usb-downlink-binding.drv` |
| flake-registry-shape | pass | `xq21maca…-criomos-flake-registry.json.drv`, `75rxymsk…-flake-registry-shape.drv` |
| tailnet-declaration | pass | `y68gfk8r…-tailnet-declaration.drv` (plus enroll script, headscale verify) |
| usb-downlink (policy) | pass | `0ap9dlra…-usb-downlink-policy.drv` |
| **usb-downlink-chain** (VM) | **FAIL** | `pi8s3v3c…-vm-test-run-usb-downlink-chain.drv` |
| **tailnet-enrollment** (VM) | **pass** | `ln58mdl4…-vm-test-run-tailnet-enrollment.drv` → `/nix/store/l1v3zl23…-vm-test-run-tailnet-enrollment`; the log shows `already enrolled, not re-registering` |

**usb-downlink-chain failure** (its first run anywhere). It fails at the first subtest, `upstream: the stand-in Internet is up`:
- Upstream's dnsmasq loops on `failed to create listening socket for 1.1.1.1: Cannot assign requested address`.
- The fixture puts `1.1.1.1/32` on `lo` through `networking.interfaces.lo`, with `bind-interfaces` and `listen-address 1.1.1.1`. dnsmasq starts before the address exists.
- This is a defect in the test's upstream fixture, not the module under test, and not a merge artifact: the check file is byte-identical to `946bcbd5`.
- A likely fix is `bind-dynamic` or ordering after the address, but that is **not applied**, because I commit only what I merge.
- It answers one of the open questions: QEMU `usb-net` on `qemu-xhci` **does enumerate** in both hop guests (`cdc_subset … usb0: register`).

## Blockers

1. Field must record the CA on goldragon `tailnet-repair-da88cf`. Until then every tailnet node refuses to evaluate, by design.
2. Field must mint the tailnet secrets, and they must reach Lojix's generated secrets input. That input is empty for ouranos today; it also lacks the goldragon-main OpenCode file.
3. goldragon main `0d462a33` (the OpenCode recipient) is not on the tailnet bookmark. The bookmark needs that merged before its data lands.
4. The usb-downlink-chain upstream fixture: dnsmasq binds `1.1.1.1` too early.
5. The CriomOS check set still fails to evaluate, on five pre-existing checks plus the lojix-ownership fixture's missing `node.machine`.

## Sources

Scratchpad `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/integrate-2/`:
- `eval-*.err` and `probe-*.{nix,json,err,out}`
- `per-check-eval.txt`, `failing-checks{,-main}.txt`
- `builds-small.txt`, `builds-vm.txt`, `build-*.log`
- `criomos-checks-names.log`
- `wrap/`, `wrap-main/`, `horizon-*/`, `secrets-goldragon-main/`, `probe-ca-horizon-*/`, `probe-secrets/`

Other sources: `git ls-remote` of `LiGoldragon/{CriomOS,CriomOS-home,goldragon,horizon-rs,lojix}`; `hm-list`; `orchestrate 'Observe.Locks'`.

## usb-downlink-chain fix (W)

- Fix (test fixture only): upstream `systemd.services.dnsmasq` now has `after` + `requires` on `network-addresses-lo.service` and `network-addresses-eth1.service`, so dnsmasq binds `1.1.1.1` and `192.168.1.1` only once they exist. Evaluation confirmed both units exist and the ordering took effect. No assertion is changed.
- Commit `fd0be3f0` on bookmark `integration-2-da88cf` (parent `c5ddf3a8`); `git ls-remote` shows `fd0be3f0271b07aa40ee7758b31b98a65e911e5a refs/heads/integration-2-da88cf`. Workspace `~/wt/github.com/LiGoldragon/CriomOS/chain-test-da88cf`; lock 7017 released.
- Run (once), offloaded: `building '/nix/store/57j4ajwkrhqvjrjglmps4bpwp54lbv1s-vm-test-run-usb-downlink-chain.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'` → `/nix/store/62cmcfmym2cx6zzx1sn6gbpf0v3xwvjm-vm-test-run-usb-downlink-chain`, rc=0.
- **PASS**: all seven subtests passed. They cover: the upstream is up; hop A is the ouranos uplink; hop B is the ouranos USB downlink plus Prometheus's lease, DNS and forced-`eth1` fetch; hop C is the Prometheus br-lan and a single nft masquerade; hop D is the client's lease, DNS and forced-`eth1` fetch, with upstream seeing ouranos's uplink address; then hotplug; then no upstream means no Internet. The log is at `scratchpad/chain-test-fix/build.log`.
- This clears blocker 4.
