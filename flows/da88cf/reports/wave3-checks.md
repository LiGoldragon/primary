# Wave 3: CriomOS check set

CriomOS bookmark `wave3-checks-da88cf` is at `a28fadfe`. It is based on `integration-2-da88cf` `c5ddf3a8`, which was verified on the remote before work began. The bookmark holds six commits, one per check. Each commit message names which side was wrong and why. In all six the check or its fixture was wrong and the module was right. No module was changed.

Evaluation ran on ouranos. Builds were offloaded to Prometheus one at a time. Nothing was activated.

## Per check

### ms2130-uvc-aspect-quirk (`eac48e8c`)

- **Cause.** The check asserted `kernel.version == "7.0.1"` and threw "MS2130 UVC patch must be reviewed for the selected kernel". Three more stale parts sat behind that assertion:
  - it extracted `linux-7.0.1/` paths;
  - it ended its ID-table range at the old "Intel D410" comment;
  - it read `stdenv.hostPlatform.linux-kernel.target`, an attribute nixpkgs 26.11 removed.
- **Since.** `458f548c` (2026-08-14) moved nixpkgs to `0e251e24`, which brought kernel 7.1.8 and removed `linux-kernel`. An hour later `4cdd843d` moved the module to `linux-7.1.8.patch` and did not update the check.
- **Wrong side.** The check.
- **Fix.** The check now asserts the reviewed 7.1.8, extracts files by `kernel.version`, ends the range at the 7.1.8 "Intel Realsense D410" comment, and reads the image name from `kernel.target`.
- **Evidence.** Main `3e2cc8be` fails at evaluation. The fixed check **built on Prometheus**: `ww13309y…-ms2130-uvc-aspect-quirk-check.drv` produced `wwqcn7m6…-ms2130-uvc-aspect-quirk-check`, and the patched 7.1.8 source matched every grep.

### resolver-role-policy (`e09b3ffe`)

- **Cause.** The fixture built `routerNode` and `peerNode` as `baseNode // { network.nodeIp = …; keys.yggdrasil.address = …; }`. `//` merges only the top level, so the nested `network` and `keys.yggdrasil` records were replaced whole. That dropped `network.wireguardPublicKey`, which Horizon requires, and `modules/nixos/network/wireguard.nix` (correct) stopped with "attribute 'wireguardPublicKey' missing".
- **Since.** `c14074ac` (2026-09-12, "Consume the current Horizon deployment shape"). Bisect: the parent `c14074ac-` evaluates, `c14074ac` fails, and main `3e2cc8be` fails.
- **Wrong side.** The fixture.
- **Fix.** Both nodes are now built with `lib.recursiveUpdate`.
- **Evidence.** The fixed check evaluates to `vnbny34q…-resolver-role-policy.drv`, the same derivation `c14074ac-` produced. It **built on Prometheus**, producing `pbifc6x9…-resolver-role-policy`.

### router-non-router-lazy (`a566cc3b`)

- **Cause.** The check forced `system.build.toplevel` of a NixOS system that had no root file system and no boot loader. NixOS's own `fileSystems` and `grub.devices` assertions threw, `tryEval` reported a failure, and the check blamed the router module. The module is lazy as intended: its config is `optionalAttrs behavesAs.router`.
- **Since.** The check's creation in `73bc5fba` (2026-09-11). It fails at `73bc5fba` and at `3e2cc8be`, and the module was already gated at `73bc5fba`.
- **Wrong side.** The check.
- **Fix.** The fixture now has a tmpfs root, grub disabled and a `stateVersion`. Its Horizon also moves to the current flat `cluster` / `tailnetBaseDomain` shape.
- **Negative control.** Forcing `routerInterfaces` outside the router gate makes the fixed check fail with its own message.
- **Evidence.** It **built on Prometheus**: `d7vl5pqk…` produced `94k3xrzk…-router-non-router-lazy-check`.

### opencode-testing-policy (`a3c44a16`)

- **Cause.** Three faults, each found once the one before it was fixed:
  1. The module takes `horizon` and `inputs` as module arguments, and the check never supplied them, giving "attribute 'horizon' missing".
  2. `d8c765db` wrote the capability fixture as `horizon.node = …` inside a NixOS module. That defines config options, not module arguments.
  3. Its three service assertions parse as `assertMsg (a == (b "message"))`, which calls a string.
- **Since.** `de939516` (2026-09-19). Bisect: `e63dee63` evaluates, `de939516` fails, and `3e2cc8be` fails.
- **Wrong side.** The check.
- **Fix.** The node and `sopsFiles` now go in through `specialArgs`. The stub `sops.secrets` submodule gets a freeform type, and the comparisons are parenthesised.
- **Negative control.** Changing the expected share setting makes the check fail with its own message.
- **Evidence.** It **built on Prometheus**: `7wp475wy…` produced `v7r4dnwn…-opencode-testing-policy`.

### wireguard-untrusted-proxy (`4489251f`)

- **Cause.** The fixture still used the retired flat shape: `hasWireguardPubKey`, `wireguardUntrustedProxies`, and a node-level `nodeIp`. The module reads `node.network.{wireguardPublicKey, wireguardProxies, nodeIp}`. That matches horizon-rs `NodeNetworkView` / `WireguardProxyView` and the Lojix-materialised ouranos `horizon.json`. The check stopped with "attribute 'network' missing".
- **Since.** `c14074ac`. Bisect: the parent evaluates, `c14074ac` fails, and `3e2cc8be` fails.
- **Wrong side.** The fixture.
- **Fix.** The fixture is now a `node.network` record.
- **Evidence.** The fixed check evaluates to `j9cy64x6…`, the same derivation as `c14074ac-`. It **built on Prometheus**, producing `qhlhlnvp…-wireguard-untrusted-proxy-check`.

### lojix-ownership (`a28fadfe`)

- **Cause.** The fixture node had no `machine` record. Horizon projects `machine` on every node, and CriomOS-home `0176de5f` (2026-09-11) reads `node.machine.architecture` in the min profile. The check stopped with "attribute 'machine' missing".
- **Since.** CriomOS has pinned a Home that contains `0176de5f` since `c14074ac`. The failure was hidden behind other failures:
  - at `2985c813` and `c14074ac`, behind Home's unfree `platform-tools` error;
  - on main `3e2cc8be` and `e6a83edc`, behind the retyped lojix-revision assertion;
  - on `integration-2`, `7556680b` made that assertion lock-derived, and this error surfaced.
- **Wrong side.** The fixture.
- **Fix.** The fixture declares `machine` (Metal, x86_64) in the shape Horizon projects.
- **Evidence.** It evaluates to `f098f4m9…-lojix-ownership.drv`. It **built on Prometheus**, producing `djd8873s…-lojix-ownership`. That build brought lojix 8.0.0, Home's `system-projection-boundary` and the li Home activation with it. Every one of the 61 derivations was offloaded; none was built locally.

## The whole checks attrNames set

- **With only `--override-input system`, it cannot evaluate, by the flake's design.** Blueprint adds `nixos-target`, which is `nixosConfigurations.target`'s toplevel, to the checks set. Blueprint's own `filterAttrs (x: x.pkgs.stdenv.hostPlatform.system == system)` then forces that configuration's module arguments. Those need a Horizon, so evaluation stops with "CriomOS: no horizon input was provided" in `modules/nixos/disks/preinstalled.nix`. Blueprint does this before CriomOS's own filter runs, so excluding the check in `flake.nix` does not help.
- **With the Lojix-materialised ouranos complete-host inputs** (system, horizon, deployment and secrets; the horizon was materialised at 2026-09-26 00:45), it stops in `nixos-target` at `modules/nixos/network/tailnet-roles.nix:64` with "attribute 'tlsCertificateReference' missing". That `horizon.json` predates the tailnet schema: its `tailnetController` capability has no certificate or key references. The input is stale; the module is not at fault.
- **With `nixos-target` removed** (a temporary, uncommitted edit, reverted afterwards) and the ouranos inputs, the set **evaluates**. All 48 names are listed, including all six fixed checks.

## Found beyond the six (not fixed)

- `criome-daemon-config-roundtrip` imports from a derivation, the pinned criome. Building `criome-deps-0.9.0` failed on Prometheus with exit 101 during a Cargo build. The failure was seen once, during the first probe evaluation. `attrNames` does not force that build, but building the check needs it.
- `flow-id-home`, `laptop-keyboard-keyd`, `persona-router-role-policy`, `repository-receive-role-policy` and `spirit-role-policy` also import from derivations. None of them was built here.

## Sources

- CriomOS commits `eac48e8c`, `e09b3ffe`, `a566cc3b`, `a3c44a16`, `4489251f`, `a28fadfe` on `wave3-checks-da88cf`. `git ls-remote` shows `a28fadfec724…` on the remote.
- History: `jj log` over each check, the module it exercises, and `flake.lock` (the nixpkgs and criomos-home pins).
- Scratchpad `wave3-checks/`:
  - `per-check.txt`: the per-check evaluation with import-from-derivation off;
  - `probe/flake.nix`: evaluates each `checks/<name>` against a CriomOS revision, with the system override;
  - `build-*.log`;
  - `attrnames.log`, `attrnames-full.log`, `attrnames-no-target-full.log`.
- `flows/da88cf/reports/step2-fixes.md`, `tailnet-repair-slice.md`, `usb-downlink-impl.md`: the earlier reports of these failures.
- `/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/horizon/horizon.json` (read only).
- horizon-rs main `a3ddaf86`, `lib/src/model.rs`: `WireguardProxyView`.
