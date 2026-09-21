# Ouranos → Prometheus → Zeus network-chain attempts

Authorized 2026-09-21 by the living. This is a bounded operational record. Existing Ouranos built-in Ethernet must remain the upstream Internet route; USB is intended downstream to Prometheus, and Prometheus's separate USB downstream to Zeus needs its own subnet. No private key is read or copied. A command's successful submission is distinguished from peer-side proof.

## Attempt 1 — live Ouranos topology and share audit

**Action:** Read only. Inspected live NetworkManager devices/profiles and permissions, default routes, USB bus/driver/link/counters, DNS/DHCP listeners, lease file, IPv4 forwarding, rootless firewall read access, Wi-Fi state, Yggdrasil peer journal, and the configured Prometheus address. No profile, service, firewall, route, or file was changed.

**Before/observation:** Built-in Ethernet `enp0s31f6` retained preferred default via `192.168.1.1`; a newly connected Wi-Fi `wlp0s20f3` had `10.18.0.102/24` and secondary default via `10.18.0.1` at metric 600. `ip route get 1.1.1.1` selected the built-in wired route. The prior `prometheus-share-temporary` profile still had `ipv4.method shared`, `10.44.0.1/24`, `never-default yes`, but was **not active**: USB `enp0s20f0u1c2` was initially disconnected and then NetworkManager tried `Wired connection 2` DHCP, leaving no IPv4 address. There was no USB DHCP/DNS listener, lease file stayed zero bytes, and per-interface IPv4 forwarding read `0`. Thus the documented share was no longer providing the chain.

The USB device is ASIX AX88179A (`cdc_ncm`) on USB bus 004 port 001 with carrier and 1000 Mbps, no observed RX/TX errors. Unlike the earlier zero-RX snapshot, RX increased to roughly 90 packets while Wi-Fi rejoined; the far endpoint remains unidentified. Ouranos's Yggdrasil journal newly showed Prometheus and Zeus peers reconnecting over Wi-Fi link-local. One ICMPv6 packet to the configured Prometheus Yggdrasil address returned in about 27 ms. This is new evidence of a live peer route, not proof of SSH or USB sharing.

**Privileged-read limit:** The user `li` has NetworkManager network-control and checkpoint rollback permission. Noninteractive `sudo` and `run0` require authentication; raw `iptables`/nftables NAT inspection is unavailable to this account. NetworkManager's own active-state and listener/forwarding results are observable without reading secrets. No firewall or NAT pass is claimed.

**Change / rollback:** No change; rollback is not applicable. The existing temporary share's exact rollback remains in `flows/6db4fe/reports/prometheus-connectivity.md`. The old share may be reactivated reversibly only after the target and routing preflight; preserve the preferred wired default route.

**Next:** Use the newly reachable configured Prometheus path with existing SSH trust and key, boundedly; inspect peer USB identities and current downstream state. Then activate the existing Ouranos share with a NetworkManager checkpoint, verify DHCP/DNS/forward/NAT as far as permitted, and test from Prometheus. Do not use the alternate Wi-Fi route as evidence of USB chain success.

## Attempt 2 — transient authenticated Prometheus route

**Action:** With new Ygg peer and ICMP evidence, used one bounded SSH connection to the configured Prometheus name as existing user `li`, `BatchMode=yes`, `StrictHostKeyChecking=yes`, and a five-second connect limit. It returned `prometheus`. No key material was read or copied. Three bounded read-only SSH commands to inventory peer interfaces were then attempted and all timed out. The Ygg journal showed the Prometheus session reset and reconnect attempts. The Wi-Fi gateway `10.18.0.1` had previously been an ARP neighbor with the same MAC as the Prometheus Ygg link-local peer; a bounded ping and strict-host-key SSH using `HostKeyAlias=prometheus.goldragon.criome` then failed because ARP became `INCOMPLETE` / `No route to host`.

**Before/after:** Ouranos Wi-Fi briefly showed connected with `10.18.0.102/24`; after the failed peer reads, `iw dev wlp0s20f3 link` said `Not connected` and the kernel marked the interface `NO-CARRIER`, even while NetworkManager briefly retained stale connected state. Prometheus is demonstrably alive at least intermittently, but this path is flapping and did not support peer inventory. The USB share remained inactive. No remote command beyond `hostname` completed.

**Change / rollback:** No configuration change, no rollback. Existing host-key validation remained enabled. Do not repeat SSH on this route without new link evidence; proceed on the separate USB transport.

**Next:** Reactivate only the existing `prometheus-share-temporary` profile on ASIX USB `enp0s20f0u1c2` with a bounded timeout and explicit down/revert procedure, then verify that built-in Ethernet remains preferred default and the share actually starts DHCP/DNS/forwarding. A peer lease or identified link-local neighbor is required before claiming a working USB hop.
