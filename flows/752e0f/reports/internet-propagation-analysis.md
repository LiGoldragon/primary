# Internet propagation: why ouranos to Prometheus works and Prometheus to Zeus does not

Subflow return of 2026-09-25, placed by Psyche High 752e0f (the reading subflow could not write). Claims carry the subflow's file and line references; grades: installed-running for Prometheus generation 54, source-published for the patch, not applied.

## Defect chain, observed live on Prometheus generation 54

- The downlink is declared and deployed as /etc/systemd/network/30-usb-eth.network (CriomOS modules/nixos/router/default.nix:442-452). It matches only on Driver=cdc_ether cdc_ncm r8152 ax88179_178a asix plus Type=ether.
- The dongle enp199s0f0u1 is an AX88179 using driver ax88179_178a, which is in that list. Yet networkctl status shows "Network File: n/a" and "unmanaged".
- In networkd's JSON, enp199s0f0u1, eno1 and wlp195s0 have no Driver value; all three were renamed from eth0/wlan0 at boot (journal 15:02:23). The links not renamed do have one: br-lan, yggTun, tailscale0.
- So the Driver match never succeeds. networkd leaves the link unmanaged, never brings it up and never adds it to br-lan. That is why the carrier reads fail and Zeus gets no DHCP.
- That the boot rename is why networkd lost the driver is inference, not proven. The link was UP on 09-23 and DOWN on 09-24 within one boot, which points at the same failure on hotplug (inference).

Ruled out: the schema mismatch (generation 54's horizon has node.network.routerInterfaces with wan eno1, wlan wlp195s0, backupWireless; top-level routerInterfaces is null); unit not applied (booted 15:02 with the file present); firewall (forward br-lan to eno1, masquerade out eno1, and the eno1 neighbour-discovery rule from 73ba25c are live; ouranos REACHABLE as a neighbour on eno1); interface naming (the match does not use names).

## 1. How ouranos to Prometheus works today

Ouranos side, all imperative: a NetworkManager profile prometheus-share-temporary on enp0s20f0u1c2 (ipv4 shared 10.44.0.1/24, never-default, ipv6 auto; read live with nmcli); a drop-in /etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf running /etc/systemd/field-prometheus-usb-firewall.sh (unreadable to the subflow); per-interface IPv4 forwarding 1, all/forwarding 0. Ouranos is declared Edge in the goldragon cluster-definition.datom with no UsbIpv4Gateway, so usb-ipv4-gateway.nix never activates (assertions at :117-138 require NetworkManager and the iptables firewall).

Prometheus side, declarative: 10-wan (router/default.nix:427-437) takes DHCPv4 on eno1 (10.44.0.148, gateway and DNS 10.44.0.1); masquerade out eno1 (:199-204); forward br-lan and eno1 (:188-189); Kea DHCP on br-lan 10.18.0.1 (:237-272); dnsmasq forwards to public resolvers (network/dnsmasq.nix:29-46).

The whole path is IPv4 only: nothing sends router advertisements or delegates prefixes anywhere in modules/. Zeus's traffic would be translated three times (Prometheus, ouranos, house router).

## 2. One feature or special cases

Three mutually exclusive implementations, each keyed to the node's role, none to "any USB is a downlink": router nodes, 30-usb-eth bridged into br-lan (router/default.nix:442-452); center nodes that are not routers, network/networkd.nix:30-48 (DHCPServer and IPMasquerade on 10.47.0.1/24), latent-broken because 10-main-eth (:20-27) matches every ether link and sorts first, claiming USB dongles too; edge nodes, usb-ipv4-gateway.nix, needing a per-node typed capability with interface name and MAC. Prometheus's Horizon routerInterfaces type has no downlink field; the USB downlink comes only from the driver match.

## 4. Patch sketch

- router/default.nix 30-usb-eth: replace the Driver match with `matchConfig = { Type = "ether"; Property = "ID_BUS=usb"; Name = "!${routerInterfaces.wan}"; }`.
- networkd.nix: the same match, and rename 20-usb-eth to 05-usb-eth so it sorts before 10-main-eth.
- Edge nodes: a NetworkManager shared profile with match.path "*-usb-*", or the UsbIpv4Gateway capability declared for ouranos in goldragon.

Acceptance, after a reboot and again after unplug and replug: enp199s0f0u1 configured by 30-usb-eth and a br-lan member; carrier on both ends; Zeus holds a Kea 10.18.0.x lease with default via 10.18.0.1; neighbours REACHABLE both sides; DNS resolves through 10.18.0.1; one curl from Zeus reaches the internet. Zeus itself UNKNOWN: SSH to it timed out.

## 5. A better version, for Mind

Route IPv6 downward, with DHCPv6 prefix delegation from ouranos and router advertisements on each downlink. Translate to IPv4 (NAT64/DNS64) once, at the node that has the internet. Choose the uplink from typed per-link roles verified by udev facts (bus, path), not by driver lists or the WAN name.

Sent by the subflow to Mind 00f95a and Field High 5f38bc, Transported.
