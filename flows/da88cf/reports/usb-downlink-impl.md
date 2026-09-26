# USB downlink: the declared daisy-chain feature in CriomOS

Subflow of da88cf, 2026-09-25. Grades: **source-published** (on the remote), **eval-proven** (checks built), **not run** (awaiting "builds open"). Nothing was deployed, activated or restarted on any machine.

## Where it is

- CriomOS bookmark `usb-downlink-da88cf` = `946bcbd501f14050c04d6025bc879a4e72fc0122`, one commit on main `3e2cc8be`. Verified with `git ls-remote origin refs/heads/usb-downlink-da88cf`.
- Workspace: `~/wt/github.com/LiGoldragon/CriomOS/usbdownlink-da88cf`.
- It consumes the horizon-rs `tailnet-repair-da88cf` (`a3ddaf86`, Horizon 0.13.0) projection `{ kind = "usbDownlink"; ipv4Network = "10.44.0.0/24"; }`. horizon-rs was not modified.

## Files

- `modules/nixos/network/usb-downlink.nix` (new): the feature.
- `modules/nixos/network/usb-ethernet-role.nix` (new): the shared bus-role match. It is a plain value, not a module.
  - `networkdMatch { exclude }` gives `Type=ether`, `Property=ID_BUS=usb`, and `Name=!<excluded>` when something is excluded.
  - `udevMatch` gives the same selection for udev rules. It leaves out wlan and wwan.
- `modules/nixos/router/default.nix`: `05-usb-eth` now takes its match from the helper, excluding the WAN. The rendered rule is unchanged: `Name=!eno1` plus the same `Type` and `Property`.
- `modules/nixos/network/networkd.nix`: the center hotplug `05-usb-eth` (10.47.0.1) now uses the helper, and it steps aside when the node declares UsbDownlink.
- `modules/nixos/network/default.nix`: imports `usb-downlink.nix` instead of `usb-ipv4-gateway.nix`.
- **Removed:** `modules/nixos/network/usb-ipv4-gateway.nix` and `checks/usb-ipv4-gateway`. Nothing produces `usbIpv4Gateway`: horizon 0.13 has no such capability, and neither the lojix-pinned 0.10.1 nor goldragon main emit it. There is no compatibility path.
- `flake.nix`: drops the `usb-ipv4-gateway` check and registers `usb-downlink` and `usb-downlink-chain`.
- `checks/usb-downlink/default.nix`: the evaluation policy.
- `checks/usb-downlink-chain/default.nix`: the VM test.

## Decisions

### Selection by bus role

Every `ID_BUS=usb` Ethernet link is a downlink. The integrated NIC (PCI) never is. No names or MACs appear in the data or the module.

On a non-router node, **all USB Ethernet links join one bridge, `br-downlink`**. That bridge carries the network's first host address (10.44.0.1/24 for `10.44.0.0/24`). This is how any number of dongles, plugged into any port, share one subnet and one DHCP server.

### One manager per link

On a non-router node, systemd-networkd owns the bridge and the USB links. On a NetworkManager node:

- a udev rule, built from the helper's match, sets `NM_UNMANAGED=1` on USB Ethernet links;
- `networking.networkmanager.unmanaged` lists `br-downlink`.

So NetworkManager keeps the integrated uplink and never touches the downlink. networkd's `wait-online` is turned off by `mkDefault` where networkd is not the node's main manager.

### DHCP: Kea

Kea on `br-downlink` serves a pool from `.10` to the last host address, with router and DNS both set to the gateway.

I chose Kea because the router module already uses it on `br-lan` (`kea.dhcp4`, raw sockets, a memfile lease database). That gives one DHCP implementation across both hops, with the same lease-file shape and the same operational commands. networkd's DHCPServer is used only by the undeclared center hotplug rule.

### DNS

systemd-resolved answers on the gateway through `DNSStubListenerExtra`. NetworkManager desktop nodes and networkd center nodes already run resolved. An assertion fails a non-router node that does not.

### NAT

- The masquerade is `networking.nat` with `internalInterfaces = [ br-downlink ]` and no external interface. That means masquerade toward whichever link carries the route, which is the integrated uplink's default route.
- It works with either the iptables or the nftables backend.
- There is one NAT owner per node. The `firewall-backend=none` and the no-`networking.nat` constraints of the old NetworkManager-share design are gone.

### Firewall

UDP 53/67 and TCP 53 are opened on `br-downlink` only, through `networking.firewall.interfaces`.

### Router composition: the "two NAT owners" risk

The router module already bridges USB Ethernet into `br-lan` with the same helper match, runs Kea and dnsmasq there, and is the node's only NAT owner (its `table ip nat`, `oifname <wan> masquerade`).

On a node with Router, `usb-downlink.nix` therefore adds **nothing**:

- no bridge, no Kea, no `networking.nat` (the router forces `nat.enable = false`, so a stray enable would also fail evaluation);
- only an assertion that the declared network equals the router LAN (`constants.network.lan.subnet`, 10.18.0.0/24).

Prometheus keeps one NAT owner. The policy check asserts this. The VM test checks that Prometheus has exactly one `masquerade` in nftables and no iptables MASQUERADE.

### The undeclared ouranos hotfix

The module does not touch the hotfix. An activation script prints a warning naming `prometheus-share-temporary`, found by `id=` in `/etc/NetworkManager/system-connections/*` or `/run/...`. It prints a second warning naming `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf` if that exists.

With the module active, NetworkManager cannot bring the profile up, because the USB link is unmanaged. So the module is correct with the profile absent, and inert against it when it is present.

## Test results

- **Built through the remote builder**, with the log lines `building '…-usb-downlink-policy.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'` and `building '…-router-usb-downlink-binding.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`: `usb-downlink` policy, `router-usb-downlink-binding`, `router-wan-recovery`, `router-declared-tcp-ports`. All passed.
- The `usb-downlink` check file was re-formatted with nixfmt after that build (layout only), so the committed revision's drv differs from the one built.
- The policy covers:
  - selection by bus role, with PCI never matching;
  - address, pool and options;
  - DNS listener, NAT, firewall;
  - NetworkManager unmanaged;
  - no shared NetworkManager profile;
  - the hotfix warning text;
  - nothing when the capability is absent;
  - a center node's hotplug rule replaced;
  - Router: a single owner, and the helper-rendered `05-usb-eth`;
  - refusal of a Router downlink network other than the LAN, host bits, /33, /30, an octet above 255, and duplicates.
- **`usb-downlink-chain` (VM test): evaluated (drv produced), NOT RUN.**
  - I started it once, and it was still only substituting locally when the main flow ordered builds held. I stopped it. The log has no `on 'ssh-ng…'` line: nothing reached Prometheus. It awaits "builds open".
  - Command: `nix build --impure --no-link -L --max-jobs 0 --expr "(import <scratch>/checks.nix).usb-downlink-chain"`, where `checks.nix` does `callPackage`s each check from `builtins.getFlake "path:<workspace>"`.
  - Topology:
    - `upstream`: DHCP on vlan1, DNS/HTTP as 1.1.1.1, no routes inward;
    - `ouranos`: NetworkManager + resolver.nix + usb-downlink, uplink virtio eth1, downlink QEMU `usb-net` on `qemu-xhci`;
    - `prometheus`: router + dnsmasq + usb-downlink, WAN virtio eth1, downlink `usb-net`, hostapd and sops forced off;
    - `client`: networkd DHCP.
  - Subtests:
    - each hop gets its lease on the integrated NIC;
    - gateway ping, then DNS (`dig @gateway`), then HTTP;
    - the leaf runs `curl -4 --interface eth1 http://example.test/`, and upstream's access log must show ouranos's uplink address;
    - USB `device_del`/`device_add` on both hops converges back to bridge membership, with the USB link still NetworkManager-unmanaged;
    - after the upstream link goes down, the leaf fails.
  - Unproven until it runs:
    - whether QEMU `usb-net` on xHCI enumerates in the guest (the fallback is `usb-ehci`);
    - whether resolved's extra stub listener answers non-local clients.

## Pre-existing breakage on main (not this change)

- `nix eval .#checks…` fails for the whole checks attribute set: `checks/lojix-ownership` expects lojix `c4bba4f…` but main pins `a67f577…`. That is why the checks above were evaluated one by one.
- `router-non-router-lazy` and `resolver-role-policy` fail to evaluate on pristine main `3e2cc8be` exactly as they do on this branch.

## What the deploy window must clean up on ouranos

1. Delete the NetworkManager profile `prometheus-share-temporary` (UUID `92eb01d2-2087-44c9-a6ff-b2420df89d33`) **after** acceptance. Until then it is inert under the module.
2. Remove `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf` and `/etc/systemd/field-prometheus-usb-firewall.sh`, then run `systemctl daemon-reload` and restart the firewall. While they exist, their iptables rules are a second NAT/filter owner beside `networking.nat`.
3. Check that no `nm-shared` NAT is left from NetworkManager's shared mode, and that NetworkManager's dnsmasq for `enp0s20f0u1c2` is gone.
4. Expect Prometheus's WAN lease to move from NetworkManager's dnsmasq to Kea. It stays within 10.44.0.0/24, but the address may change (the old pool is .10–.254, and so is the new one).

## What remains

- Run `usb-downlink-chain` on "builds open".
- goldragon data:
  - ouranos `UsbDownlink.{ 10.44.0.0/24 }`;
  - Prometheus `UsbDownlink.{ 10.18.0.0/24 }` (optional: its router already serves the downlink; declaring it adds the LAN-agreement check).
  - This needs horizon 0.13 (`a3ddaf86`) landed on main, and lojix plus goldragon repinned.
- Merge `usb-downlink-da88cf` into CriomOS main. Merging also brings in e92a336's `router-usb-ethernet-reconcile` if that is still wanted.
- **Nested NAT remains:** Prometheus → ouranos → ISP. The skill's single egress NAT at ouranos would need a routed 10.18.0.0/24 via Prometheus on ouranos. That is not done here.
- **Stopping at "router is just a feature":** the router LAN network still comes from `constants`, and the module only checks that it agrees. Deriving it from UsbDownlink, and splitting out the AP as its own feature, is later work.
- **A consequence of the living's rule:** a phone USB tether on ouranos (RNDIS/CDC, `ID_BUS=usb`) becomes a downlink, never an uplink.

## Sources

- `flows/da88cf/reports/daisy-chain-plan.md`.
- horizon-rs `a3ddaf86` (`lib/ethos/horizon.ethos`, `lib/src/model.rs`, `lib/src/projection/views.rs`, `lib/tests/contract.rs`, `UPGRADES.md`).
- CriomOS main `3e2cc8be`: `modules/nixos/router/default.nix`, `modules/nixos/network/{networkd,dnsmasq,resolver,usb-ipv4-gateway}.nix`, `checks/router-usb-downlink-binding`.
- nixpkgs `nixos/modules/services/networking/nat-iptables.nix` and `nixos/lib/testing/network.nix`.
- Build logs in the subflow scratchpad `usbdownlink-impl/{small-build,vm-build-1}.log`.
