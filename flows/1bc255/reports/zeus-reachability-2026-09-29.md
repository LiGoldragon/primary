# Zeus reachability witness — 2026-09-29

Prepared for Mind Sol `b666e7` from bounded read-only observations by Field Sol `1bc255`. No host, service, configuration, or file on Ouranos, Prometheus, or Zeus was changed. Field Luna `025548` confirmed it did not overlap this probe.

## Topology correction

The living corrected the earlier assumed topology:

> I've changed the topology a bit, but now Zeus is downstream of Uranus, and Uranus is downstream, or on the USB side, of Prometheus... It's the same problem again on the USB cable side.

The relevant current path is therefore Prometheus USB → Ouranos built-in `10.18.0.101` → Ouranos USB `enp0s20f0u1c2` / `br-downlink` (`10.44.0.1/24`) → Zeus. Earlier observations of `10.18.0.103` on Prometheus's `br-lan` do not identify Zeus under this topology.

## Commands and observations

All timestamps are America/Mexico_City (`-06:00`).

| Time | Read-only command group | Decisive output |
| --- | --- | --- |
| 15:24:22–15:24:27 | On Ouranos: `ip -br link`, `ip -br addr`, `ip route show`, `ip neigh show`, two ICMP probes. On Prometheus through normal noninteractive SSH: the corresponding link, route, neighbor, and two ICMP reads. | Ouranos `enp0s31f6` was `10.18.0.101/24`; Prometheus `br-lan` was `10.18.0.1/24` and reachable from Ouranos. The old `10.18.0.103` neighbor failed at both hosts. This is historical/topology-superseded context only. |
| 15:27:22 | On Ouranos: `ip -br link/addr`, `ip -d link`, `ethtool enp0s20f0u1c2`, `lsusb -t`, `bridge link/fdb`, `ip route get 10.44.0.148`, `ip neigh`, and relevant `systemctl is-active`. | `enp0s20f0u1c2` and `br-downlink` were both `UP,LOWER_UP`; the USB NIC is a 5 Gbit/s `cdc_ncm` device at USB parent `4-1:2.0`, and is the sole forwarding bridge member. `br-downlink` carries `10.44.0.1/24`. Its FDB had only bridge/local permanent entries, no downstream client MAC. |
| 15:27:22 | Ouranos: `systemctl is-active` and bounded `journalctl -u kea-dhcp4-server.service -n 80` filtered to `10.44`, `br-downlink`, and DHCP events. | `NetworkManager`, `systemd-networkd`, and `kea-dhcp4-server` were active; `dnsmasq`, `isc-dhcp-server`, and `dhcpd` were inactive. Kea repeatedly recorded MAC `84:47:09:75:88:68` requesting/reusing lease `10.44.0.148` on `br-downlink`, most recently shown at 14:45:21, and sent DHCPACKs from `10.44.0.1`. This identifies the last observed downstream client, but is not proof it is Zeus and does not show a current lease-database query. |
| 15:27:37 | Ouranos: `ip neigh show to 10.44.0.148`; then `ping -n -c 2 -W 2 10.44.0.148`; bounded TCP connect `</dev/tcp/10.44.0.148/22`; final neighbor readback. | The neighbor entry was absent before probing, became `10.44.0.148 dev br-downlink FAILED` afterward; both ICMP packets were lost and TCP/22 returned `No route to host`. |

## Capture before any physical intervention

At 15:29:21, still without intervention, the running Ouranos system was `/nix/store/dbhsh7wp18awjlfvl4061c6kfsj3w7hh-nixos-system-ouranos-26.11.20260813.0e251e2`. The following read-only commands captured the local side: `networkctl status enp0s20f0u1c2 br-downlink --no-pager`; `udevadm info --query=property --path=/sys/class/net/enp0s20f0u1c2`; `ip -s link`; `bridge link/fdb`; bounded kernel and `systemd-networkd` journals since 15:20; the current `10.44.0.148` neighbor; and the recent Kea journal filtered to the downstream identity.

`enp0s20f0u1c2` is the configured, enslaved USB Ethernet interface: ASIX AX88179A, driver `cdc_ncm`, USB path `4-1:2.0`, MAC `00:0e:c6:33:4f:97`, 100 Mbps, and master `br-downlink`. It and `br-downlink` were `UP,LOWER_UP`; the bridge was routable at `10.44.0.1`. The bridge had one forwarding member and no learned downstream FDB entry. Counters were nonzero but contain historic traffic; no fresh endpoint traffic attribution was established.

`systemd-networkd` records a carrier loss at 14:50:55 and a carrier gain at 15:26:41 for both the USB interface and bridge. The kernel records the bridge port returning through blocking to forwarding at 15:26:41. The interface had been observed `NO-CARRIER` at 15:24:22, then `LOWER_UP` at 15:27:22. The cause of that transition is not known from this host. At 15:29:21 the exact neighbor remained `FAILED` for `10.44.0.148`; no Kea event for that address appeared after the prior 14:45:21 lease record in the bounded journal window.

## DHCP identity correction

At 15:33:20, the exact downstream L2 reads still showed `10.44.0.148 FAILED`, no learned nonlocal FDB entry, and only failed IPv6 neighbors. A bounded `arping -c 2 -w 4 -I br-downlink 10.44.0.148` could not run because the unprivileged process returned `socket: Operation not permitted`; it made no network change. The ordinary ICMP/TCP probes above remain the available targeted reachability evidence.

The Kea lease identity must not be treated as Zeus. At 15:33:51, direct noninteractive SSH to the already reachable Prometheus LAN address `10.18.0.1`, using the existing Prometheus host-key alias, returned host `prometheus` and showed MAC `84:47:09:75:88:68` belongs to its `eno1`. At 15:34:00, Prometheus `networkctl status eno1` identified that NIC as the Realtek WAN interface with current DHCP address `192.168.1.11/24`, gateway `192.168.1.1`, and DUID suffix `0000ab119d5da3f8deef223f`. That DUID suffix and MAC exactly match the Ouranos Kea record for `10.44.0.148`. Prometheus currently routes `10.44.0.1` through its WAN gateway, not through a directly assigned `10.44` address.

This proves the recorded `10.44.0.148` lease was Prometheus's `eno1` identity at the time it was issued. It does not identify a current Zeus address, MAC, or attachment. It is consistent with the living's statement that topology changed, but it does not itself establish the historical physical wiring.

## Post-replug readback

The living subsequently reported that the downstream cable was plugged at both ends and had been unplugged/replugged once, after which a light appeared. No agent repeated that physical action. This may coincide with the locally witnessed 15:26:41 carrier gain, but the exact causal relationship was not observed and is not claimed.

At 15:35:27, a new read-only post-event readback found `enp0s20f0u1c2` and `br-downlink` still `UP,LOWER_UP`. It found no learned nonlocal bridge FDB entry, no Kea DHCP entries since 15:26:00, and the prior IPv4/IPv6 neighbors still failed. The known Zeus DNS name continued to resolve to its existing Yggdrasil IPv6 record, but one ICMP probe lost all packets and a bounded SSH connection timed out. The light/carrier state therefore does not yet establish a functioning Zeus endpoint or a current Zeus identity.

At 15:24:22, the same downlink interface had been observed `NO-CARRIER` and `br-downlink` down. At 15:27:22, both reported `LOWER_UP`. The later carrier state is the current observation. It shows the Ouranos USB NIC and its immediate USB link are present; it does not prove the link onward from that USB peer to Zeus.

## Passive snapshot after the reported replug

At `2026-09-29T15:38:15-06:00`, before any further ICMP, SSH, or Yggdrasil probe, Field ran only local read commands on Ouranos: `date -Is`; `ip -br link show dev enp0s20f0u1c2`; `ip -br link show dev br-downlink`; `ethtool enp0s20f0u1c2` filtered for link state; `bridge link show master br-downlink`; `bridge fdb show br br-downlink`; IPv4 and IPv6 `ip neigh` reads for `br-downlink`; `systemctl show kea-dhcp4-server.service`; a bounded recent Kea journal read; and a local Kea socket listing.

`enp0s20f0u1c2` and `br-downlink` were both `UP,LOWER_UP`; the USB NIC remained the sole forwarding bridge member. The FDB again contained only local/permanent entries and no learned downstream MAC. The IPv4 table contained only the failed legacy `10.44.0.148` entry; the IPv6 table contained only failed link-local entries. Kea was active (main PID `94939`), but its bounded recent records were historical `10.44.0.148` events, with no post-replug client/lease event; no Kea control socket was listed. As established above, that legacy address and its MAC belong to Prometheus `eno1`, so neither supplies a Zeus identity.

No active network probe, physical action, configuration change, service action, or other host mutation followed this snapshot. The present blocker is still a physical or console witness identifying Zeus's current downstream attachment and MAC/address; without it, no bounded reachability test or reversible remedy is justified.

## Diagnosis

The configured corrected path is live through Ouranos's USB NIC and bridge. The only observed `10.44.0.148` lease belongs to Prometheus's WAN identity and is stale for identifying Zeus; it cannot be used as a Zeus target. The available evidence proves only that Ouranos's bridge lacks a currently learned downstream peer, not where Zeus is attached or what address it now has. No network configuration change is justified by this evidence.

## Remaining unknowns

- Zeus's power state, physical cable and USB-peer/switch state, NIC state, current address, and current MAC.
- Which live endpoint, if any, is downstream of Ouranos's USB bridge after the topology change.
- Whether a host firewall suppresses ICMP and SSH after L2 resolution; no current Zeus L2 identity is known to test.
- Whether the 15:24 `NO-CARRIER` to 15:27 `LOWER_UP` transition reflects a physical reconnect, and what lies beyond the currently enumerated USB peer.

## Safe immediate remedy

Obtain a physical or console witness that identifies the live downstream Zeus attachment and its current MAC/address. Inspect the Ouranos-to-Zeus USB/cable/peer path and Zeus power without changing network configuration. Once that identity is known, use one targeted read-only carrier, neighbor, and SSH-banner/connection check. Do not use the historical Prometheus `10.44.0.148` lease as a Zeus target, and do not reconfigure the host before the identity witness exists.
