# Prometheus USB Ethernet router hotplug investigation

Date: 2026-06-06
Role: pi-operator

## Question

Prometheus has the router role and has USB Ethernet adapters attached. The desired behavior is that those USB Ethernet ports serve internet to connected clients, including when the adapters are plugged after boot.

## Intent captured

Spirit record `yker` captures the durable intent: Prometheus router-role USB Ethernet adapters should serve internet, and hotplugged adapters should automatically attach to the router network role without manual intervention.

## Repository state

CriOMOS already has a router-specific USB Ethernet LAN policy in `modules/nixos/router/default.nix`.

The generated router design is:

- WAN: Horizon-declared `routerInterfaces.wan`, currently `eno1` for Prometheus.
- LAN bridge: `br-lan`, statically addressed as `10.18.0.1/24`.
- Primary Wi-Fi AP: Horizon-declared `wlp195s0`, bridged into `br-lan` by hostapd.
- Backup Wi-Fi AP: Horizon-declared `wlp199s0f0u4`, hotplug-triggered by udev and bridged into `br-lan`.
- USB Ethernet LAN ports: generic systemd-networkd match by Ethernet type and USB NIC driver family, then `Bridge=br-lan`.
- DHCP: Kea listens on `br-lan` and leases `10.18.0.100-10.18.0.240`-range addresses.
- DNS: dnsmasq listens on `10.18.0.1:53` and loopback.
- NAT: nftables masquerades traffic leaving WAN `eno1`.
- Forwarding: IPv4 and IPv6 forwarding sysctls are enabled; nftables allows `br-lan` to `eno1` forwarding and established traffic back.

Prometheus Horizon currently declares only WAN, primary Wi-Fi, backup Wi-Fi, and secrets. It does not declare specific USB Ethernet ports. USB Ethernet policy is therefore a CriOMOS router default, not cluster data.

## Linux/networkd hotplug feasibility

systemd-networkd supports this shape. Upstream `systemd.network` documentation says `.network` files are applied to links whenever links appear. It also documents `[Match] Driver=` as a whitespace-separated list of driver globs, and `[Match] Type=ether` as a valid device-type match. That means the generic USB-Ethernet match should apply to adapters that appear after boot, as long as their drivers match the configured list and networkd is running.

The current CriOMOS `30-usb-eth.network` generated for Prometheus is:

```ini
[Match]
Driver=cdc_ether cdc_ncm r8152 ax88179_178a asix
Type=ether

[Link]
RequiredForOnline=no

[Network]
Bridge=br-lan
ConfigureWithoutCarrier=true
```

That is a plausible and intended systemd-networkd hotplug configuration.

## Live Prometheus evidence

Read-only checks on Prometheus showed:

- `systemd-networkd` is active.
- `kea-dhcp4-server` is active.
- `hostapd` is active.
- `dnsmasq` is active and listening on `10.18.0.1:53`.
- `systemd-resolved` is intentionally absent/inactive on router nodes because dnsmasq owns DNS.
- Router WAN `eno1` has an IPv4 address on upstream LAN and default route.
- Prometheus itself can resolve `example.com` and ping `1.1.1.1`.
- nftables NAT exists: `oifname "eno1" masquerade`.
- `br-lan` exists and has `10.18.0.1/24`.
- Kea is issuing leases on `br-lan`.

Two USB Ethernet devices are present:

- `enp197s0f4u1c2`, driver `cdc_ncm`, matched by `30-usb-eth.network`, master `br-lan`.
- `enp199s0f0u2`, driver `ax88179_178a`, matched by `30-usb-eth.network`, master `br-lan`.

Both drivers are included in the configured `Driver=` match list.

Both interfaces are currently enslaved to `br-lan`, but both currently have no carrier:

- `enp197s0f4u1c2`: `operstate=down`, `carrier=0`, master `br-lan`.
- `enp199s0f0u2`: `operstate=down`, `carrier=0`, master `br-lan`.

Kernel logs confirm both adapters were detected and added to the bridge. The bridge ports entered disabled state because the links had no carrier.

The live bridge forwarding database currently shows active client MACs behind `wlp195s0` — the primary Wi-Fi AP — not behind either USB Ethernet port. Kea's current visible leases likewise correspond to clients reachable via Wi-Fi, not via the USB Ethernet ports.

## Diagnosis

The current evidence does not show a missing hotplug policy. It shows the opposite: the USB adapters are detected, networkd matches them, and they are bridge members.

The immediate blocker visible now is physical link state: both USB Ethernet links report no carrier. In that state, the router cannot serve a wired client on those ports because the Ethernet link is not up at layer 1. Causes could include:

- no client or switch currently plugged into the adapter;
- cable not seated or bad cable;
- connected client/switch port down;
- adapter/hub power or compatibility issue;
- one of the adapters requiring a driver-specific fix for link detection.

If a client was plugged in during the failure, the next needed evidence is collected while the cable/client is plugged in and trying to use the port.

## What is already implemented

Already implemented and live on Prometheus:

- generic hotplug matching for USB Ethernet drivers;
- bridge attachment to `br-lan`;
- DHCP service on `br-lan`;
- DNS service on `10.18.0.1`;
- IPv4 forwarding and NAT from `br-lan` to WAN `eno1`;
- missing USB adapters do not block boot or network-online.

## What is not proven yet

Not yet proven:

- a USB Ethernet client can pass traffic end-to-end when the port has carrier;
- a USB Ethernet adapter newly plugged after boot gets matched without a networkd reload;
- the nftables `iifname "br-lan"` forward path sees routed traffic from a bridged USB port as `br-lan` under this kernel/network stack;
- every USB Ethernet driver family the psyche owns is covered by the current driver list.

## Next safe test

A safe read-only runtime test requires the user to plug a client or switch into one USB Ethernet adapter and keep it connected while the operator checks:

- `carrier` and `operstate` for the USB interface;
- `bridge link` state for the USB port;
- Kea DHCP logs for a lease issued through `br-lan`;
- bridge forwarding database to see the client MAC behind the USB interface;
- `nft` NAT/forward counters or packet trace, if needed;
- client-side IP, default route, DNS server, and test pings.

No deploy or restart is needed for that diagnostic pass.

## Live plugged-in follow-up

When the user connected the client, Prometheus reported carrier on `enp197s0f4u1c2` and the port moved to bridge forwarding state under `br-lan`.

Prometheus-side evidence after connection:

- `enp197s0f4u1c2` has `carrier=1`, `operstate=up`, and master `br-lan`.
- networkd state for `enp197s0f4u1c2` is `enslaved (configured)` with network file `/etc/systemd/network/30-usb-eth.network`.
- bridge state for that port is `forwarding`.
- Prometheus still has WAN route, forwarding, NAT, DHCP, and DNS active.

Client-side evidence on `ouranos`:

- local Ethernet `enp0s31f6` has kernel link up / carrier on;
- NetworkManager marks `enp0s31f6` as `disconnected`;
- `enp0s31f6` has no IPv4 address;
- the existing Ethernet profiles for `enp0s31f6` are DHCP profiles but both have `connection.autoconnect=no`:
  - `prometheus-lan`
  - `Wired connection 1`
- `ouranos` remains on Wi-Fi `wlp0s20f3` with address `10.18.0.101/24` and default route through Prometheus over Wi-Fi.

The plugged-in failure was therefore not a missing Prometheus hotplug attachment. The active client was not bringing up a usable wired default route.

Live fix applied on `ouranos`:

- activated the existing `prometheus-lan` profile on `enp0s31f6`;
- changed `prometheus-lan` to `connection.autoconnect=yes`;
- set `connection.autoconnect-priority=200`;
- changed `ipv4.never-default=no`;
- set `ipv4.route-metric=50`;
- set `ipv6.never-default=yes`.

After the fix:

- `enp0s31f6` has DHCP address `10.18.0.103/24`;
- the Ethernet default route is installed via `10.18.0.1` with metric `50`;
- Wi-Fi remains up with a higher-metric default route;
- ping to the router over Ethernet succeeds;
- ping to `1.1.1.1` over Ethernet succeeds;
- Prometheus learns the `ouranos` Ethernet MAC behind `enp197s0f4u1c2` on `br-lan`.

Durable client-side follow-up, if desired: CriOMOS/CriOMOS-home should make trusted Ethernet DHCP profiles autoconnect when carrier appears, while preserving the user's Wi-Fi fallback/routing policy when both links are available.

## Possible code hardening after the live test

If the live test shows the bridge/routing path works once carrier exists, no code change is required for the core behavior.

If the live test shows carrier exists and DHCP works but internet forwarding fails, likely hardening is in nftables: add counters and/or allow forwarding from known LAN bridge ports if the kernel reports the physical USB interface as `iifname` rather than `br-lan`.

If the live test shows a new adapter is not matched, the durable fix is to extend the driver match list or introduce a Horizon/cluster-data `routerInterfaces.usbLan` inventory for known adapters. Per horizon boundary rules, specific hardware/safety inventory may belong in cluster data; generic driver-family defaults belong in CriOMOS.

If the live test shows the adapter has no carrier despite a known-good connected client/switch, install `ethtool` on router nodes or add an equivalent diagnostic package so link mode, negotiation, and driver details can be inspected without ad-hoc tooling.
