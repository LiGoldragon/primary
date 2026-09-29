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

At 15:24:22, the same downlink interface had been observed `NO-CARRIER` and `br-downlink` down. At 15:27:22, both reported `LOWER_UP`. The later carrier state is the current observation. It shows the Ouranos USB NIC and its immediate USB link are present; it does not prove the link onward from that USB peer to Zeus.

## Diagnosis

The configured corrected path is live through Ouranos's USB NIC and bridge, and Kea has a historical/recently logged downstream lease at `10.44.0.148`. The direct current targeted probe cannot resolve that address to a neighbor and cannot reach ICMP or TCP/22. The available evidence bounds the failure downstream of Ouranos's `br-downlink` L2 interface: Zeus may be off, disconnected beyond the USB peer, changed address/MAC, or otherwise not replying at L2. It does not support changing any network configuration.

## Remaining unknowns

- Whether `10.44.0.148` / MAC `84:47:09:75:88:68` is Zeus under the corrected topology.
- Zeus's power state, physical cable and USB-peer/switch state, NIC state, current address, and current MAC.
- Whether a host firewall suppresses ICMP and SSH after L2 resolution; the failed ARP/neighbor result prevents distinguishing that here.
- Whether the 15:24 `NO-CARRIER` to 15:27 `LOWER_UP` transition reflects a physical reconnect, and what lies beyond the currently enumerated USB peer.

## Safe immediate remedy

Perform a physical inspection of the downstream Ouranos-to-Zeus USB/cable/peer path and Zeus power, without changing network configuration. After the physical link is confirmed, use one targeted read-only check for carrier, neighbor resolution of the then-current Zeus address, and an SSH banner/connection. If the peer reports a different address or MAC, update the identification from direct evidence before any configuration or host action.
