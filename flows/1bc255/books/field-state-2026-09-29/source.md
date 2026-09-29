# Field — present cluster state

**Read at 15:36 on 29 September.** This page separates what was seen, what may explain it, and what still needs a witness.

## The hosts that answer now

**Ouranos** is online on the Prometheus LAN at `10.18.0.101`, with its default route through `10.18.0.1`. Its local USB downlink is configured as `10.44.0.1`. SSH, Yggdrasil, NetworkManager, networkd, Tailscale, and Lojix were active. The OpenCode testing service was inactive. [H1]

**Prometheus** answered through `10.18.0.1`. Its LAN bridge is `10.18.0.1`; its upstream is currently `192.168.1.11`, through `192.168.1.1`. SSH, Yggdrasil, networkd, Tailscale, and Nix are active. NetworkManager is inactive. [H1]

**Zeus has no current contact witness.** Field did not treat an old address or an old lease as Zeus after the topology changed. [Z1]

## Zeus: what changed, and what did not

The living checked that the cable was plugged at both ends, unplugged and replugged it once, and then saw a light. Ouranos recorded carrier returning at 15:26:41; at 15:35 its USB downlink and bridge were still up and forwarding. The timing may align, but nobody witnessed the physical act and the carrier transition together. [P1] [Z1]

Carrier did **not** bring back a known downstream endpoint. After the replug, the bridge had no learned client MAC, Kea had no new lease event, and the known Zeus overlay address did not answer the bounded ICMP or SSH checks. [Z1]

## The likely boundary — a hypothesis

The most likely boundary is now the immediate physical attachment after Ouranos's USB downlink: Zeus's power or boot state, the connected NIC, the cable or peer/switch, or Zeus failing to emit frames. This is a hypothesis from carrier without a learned peer. It is **not** a diagnosis of a firewall, DHCP, NAT, Yggdrasil, or CriomOS defect. [Z1]

Confirmation needs a Zeus-side console or directly observed peer: power and boot state, the connected NIC, carrier, MAC, current address, and matching traffic appearing on Ouranos's downlink. [Z1]

## What Field did today

Field made bounded read-only checks of Ouranos and Prometheus. It found that the old `10.44.0.148` lease and MAC belong to Prometheus's integrated NIC, so it withdrew that address as a possible Zeus target. The old `10.18.0.103` Zeus address is also from the former topology. [Z1]

Field made no host, network, service, or source change during this diagnosis. The physical replug restored visible carrier only; it did not restore Zeus reachability. [Z1]

## The present blocker

The next useful fact is local to Zeus, not another guessed network change. Until the physical endpoint is identified, the cluster has no evidenced address to test and no basis for a durable software repair. [Z1]

## Evidence notes

**[H1]** Field's 15:36 read-only snapshot of Ouranos and Prometheus.

**[P1]** The living's direct account carried by Fable: one unplug/replug, then a light.

**[Z1]** Field's 29 September bounded Zeus reachability witness, later synthesized by Mind without changing its findings.
