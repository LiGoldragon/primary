# Receipt: ouranos daisy-chain hotfix removal, declared (b860be subflow, 2026-09-26)

Grades: **source-published** (bookmark on the real remote), **check-built** on Prometheus. Not deployed. Not activated on any machine.

## Revision

- CriomOS bookmark `hotfix-removal-b860be` = `d9f808ec8b50c994ce7e3b121f4005bbcb13fb9f`. It is one commit on `integration-2-da88cf` `fd0be3f0271b07aa40ee7758b31b98a65e911e5a`.
- Workspace: `/home/li/wt/github.com/LiGoldragon/CriomOS/hotfix-removal-b860be`. It was created with `jj workspace add --name hotfix-removal-b860be -r fd0be3f0 …` and is kept until the bookmark is integrated.
- Push: `jj git push --bookmark hotfix-removal-b860be`.
- Remote check: `git ls-remote ssh://git@github.com/LiGoldragon/CriomOS refs/heads/hotfix-removal-b860be` returned `d9f808ec8b50c994ce7e3b121f4005bbcb13fb9f	refs/heads/hotfix-removal-b860be`.
- Scope: `jj diff -r @- --name-only` was run after the commit and again after the bookmark was set. Both listed the same three files:
  ```
  checks/usb-downlink/default.nix
  modules/nixos/network/usb-downlink-hotfix.nix
  modules/nixos/network/usb-downlink.nix
  ```
  None of the other flow's checks (`lojix-ownership`, `ms2130`, `opencode-testing-policy`, `resolver-role-policy`, `router-non-router-lazy`, `wireguard-untrusted-proxy`) was touched.

## Change

- **`modules/nixos/network/usb-downlink-hotfix.nix` (new).** This is a plain value, like `usb-ethernet-role.nix`, not a module. It holds the `writeShellApplication` `usb-downlink-remove-hotfix ROOT`, which removes:
  - `ROOT/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf`;
  - `ROOT/etc/systemd/field-prometheus-usb-firewall.sh`;
  - every file in `ROOT/etc/NetworkManager/system-connections/` that has the exact line `id=prometheus-share-temporary`.

  It is idempotent and leaves other drop-ins and profiles alone. On the live root, if a profile was removed and NetworkManager is active, it runs `timeout 30 nmcli connection reload`. That makes NetworkManager forget the profile, and with it the profile's shared-mode dnsmasq and NAT. A reload failure is only a warning.
- **`modules/nixos/network/usb-downlink.nix`.** Inside `config = mkIf declared (…)`, in the capability's common block (which Router nodes also get), the warning-only activation script was replaced by `system.activationScripts.usbDownlinkLegacyHotfix = { text = "${hotfixRemoval}/bin/usb-downlink-remove-hotfix /"; deps = [ ]; }`. A node without UsbDownlink does not get the attribute.
- **`checks/usb-downlink/default.nix`.**
  - The old assertion only searched the warning text for the names. It is replaced by an assertion that the gateway node's activation text equals the removal program's invocation on `/`. That program is built from the node's own `pkgs`, `systemd.package` and `networkmanager.package`.
  - The builder now fills a fixture root with the hotfix as it was inventoried on ouranos: the drop-in, the script, and the profile with UUID `92eb01d2-…`. It adds decoys: `50-other.conf`, `Wired connection 1`, and a profile with `id=prometheus-share-temporary-2`.
  - It runs the removal twice (for idempotence) and requires the hotfix paths gone and the decoys kept.
  - The earlier assertions still hold:
    - the declared NAT, firewall, Kea, resolved and NetworkManager-unmanaged rules are present;
    - `!(plainNode.system.activationScripts ? usbDownlinkLegacyHotfix)`, so nothing is removed without the capability.

## Mechanism and why

I chose an activation snippet over tmpfiles `r` rules and over a oneshot unit. The reasons:

1. **Order within one switch.** switch-to-configuration runs the activation script first, then `daemon-reload`, then the unit reloads and restarts. Removing the drop-in in activation means firewall.service is reloaded in that same switch with no hotfix `ExecStartPost`.
   - tmpfiles runs through `systemd-tmpfiles-resetup` after the daemon-reload. The drop-in would stay loaded until the next reload.
   - A oneshot "before firewall" would be a unit that runs on every boot, and it still could not unload a drop-in systemd has already read.
2. **Consistency with the module.** The module already reached the same hotfix through `system.activationScripts.usbDownlinkLegacyHotfix`. The removal replaces that warning in place.
3. **The profile is a match on content, not a fixed path.** tmpfiles `r` needs known paths, and the profile's filename is unknown. The profile is found by its `id=` line.

## Check results (ouranos, `--option max-jobs 0`, builder `/etc/nix/machines` = `ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux … 6 10 big-parallel,kvm,nixos-test`)

**The flake's checks attribute does not evaluate.** `nix build "path:$PWD#checks.x86_64-linux.usb-downlink"` fails with `error: CriomOS: no system input was provided.` This is the known Blocker B. So each check was called through the scratch expression `scratchpad/checks.nix`:

```nix
{ workspace ? "/home/li/wt/github.com/LiGoldragon/CriomOS/hotfix-removal-b860be" }:
let
  flake = builtins.getFlake "path:${workspace}";
  inherit (flake) inputs;
  pkgs = import inputs.nixpkgs { system = "x86_64-linux"; };
in
{ usb-downlink = pkgs.callPackage (workspace + "/checks/usb-downlink") { inherit inputs; }; … }
```

The command was `nix build --impure --option max-jobs 0 --no-link --print-out-paths -L --expr "(import <scratch>/checks.nix {}).usb-downlink"`.

1. **First attempt, with the activation script given as a string: evaluation error.** `expected a set but found a string with context`. The check reads `.text`, so the module now declares `{ text; deps = [ ]; }`.
2. **Pass.** Builder evidence:
   ```
   building '/nix/store/sjfv15dif4i4v6iyp9x04h8pnrqx11pr-usb-downlink-remove-hotfix.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
   building '/nix/store/1azb0qmpl51dhfavsa1ljrn10fr9azyz-usb-downlink-policy.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
   usb-downlink-policy> usbDownlink: removed undeclared hotfix file /etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf
   usb-downlink-policy> usbDownlink: removed undeclared hotfix file /etc/systemd/field-prometheus-usb-firewall.sh
   usb-downlink-policy> usbDownlink: removed undeclared hotfix file /etc/NetworkManager/system-connections/prometheus-share-temporary.nmconnection
   copying path '/nix/store/s44f3azr3r86s7f1x98757py3i3lmvg4-usb-downlink-policy' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
   /nix/store/s44f3azr3r86s7f1x98757py3i3lmvg4-usb-downlink-policy
   ```
3. **Seen failing (removal sabotaged).** The line removing the script was commented out temporarily, then restored:
   ```
   building '/nix/store/sq6mlw6nk4xr8jkhha8b37y726pnis7a-usb-downlink-policy.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
   usb-downlink-policy> usb-downlink-policy: the hotfix firewall script survived
   error: build of '/nix/store/sq6mlw6nk4xr8jkhha8b37y726pnis7a-usb-downlink-policy.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome' failed: … builder failed with exit code 1.
   ```
4. **Seen failing (gating sabotaged).** The activation script was moved outside `mkIf declared`, temporarily, then restored. Evaluation failed with `error: a node without the capability gets no downlink`.
   - A first variant defined the script both inside and outside the gate. It failed on the doubled activation text (`activation runs the hotfix removal on the live root`) before reaching the gating assertion.
5. **Restored tree rebuilt.** It gave the same output, `/nix/store/s44f3azr3r86s7f1x98757py3i3lmvg4-usb-downlink-policy` (drv `1azb0qmp…`), and the committed files are identical to that tree.
6. **`router-usb-downlink-binding`.** Result: `/nix/store/qq157pm53cjv3i9s6pxyrhlc14mf5f45-router-usb-downlink-binding`. No build line was printed because the output was already valid, so this is not new builder evidence.
7. **`usb-downlink-chain` (VM test): evaluated only.** It gave `/nix/store/g2izzkcc20czj99hcczlnqjq8mqmhwzc-vm-test-run-usb-downlink-chain.drv` and was **not run**.

## Unresolved

- **The hotfix script's kernel rules stay until reboot.** The script (root 0700) was never read, so its rules are unknown. The NixOS firewall's start and reload flush only its own `nixos-*` chains. Any rule the script added directly to base chains (`FORWARD`, nat `POSTROUTING`) stays in the kernel until reboot or a manual flush. Files are removed declaratively. Live rules left in base chains are not. [I]: most likely a duplicate MASQUERADE or ACCEPT, which is harmless beside `networking.nat`.
- **The old rollback path no longer works.** The deploy plan's rollback was: boot or switch to 188, then `nmcli con up prometheus-share-temporary`. That relied on keeping the profile until acceptance. The same generation now deletes it, so rolling back to 188 leaves Prometheus without an uplink until the profile is recreated by hand. Ouranos's own Internet is unaffected.
- **Nothing happens until goldragon declares it.** Ouranos gets no removal until goldragon declares `UsbDownlink.{ 10.44.0.0/24 }` for ouranos, which also needs the horizon 0.13 repin train. This is intended, because of the capability gate.
- **Not proven live.** The `nmcli connection reload` branch is not run by the check (the fixture root is not `/`), and nothing was activated.
