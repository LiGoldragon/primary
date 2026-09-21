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

## Attempt 3 — restore Ouranos's existing USB share

**Action:** Created a NetworkManager checkpoint for **only** USB device `enp0s20f0u1c2` with a 120-second automatic rollback timeout. Activated the existing in-memory `prometheus-share-temporary` connection by its exact UUID on that device with a 15-second NM wait. Checked postconditions, then destroyed the checkpoint to retain the successful state. No new profile, firewall rule, route, secret, or declarative source was written.

**Before:** USB device was disconnected or being retried under `Wired connection 2` (an ineffective DHCP client). It had no IPv4 address, no downstream DHCP/DNS listeners, and IPv4 forwarding `0`. Built-in `enp0s31f6` was preferred default via `192.168.1.1`, Wi-Fi secondary at metric 600.

**After:** NM reports the exact temporary share connected on USB with `10.44.0.1/24`. Its dnsmasq listens on UDP 67 and `10.44.0.1:53`, advertising DHCP `10.44.0.10–10.44.0.254` for one hour. USB IPv4 forwarding reads `1`; `ip route get 1.1.1.1` still selects built-in Ethernet via `192.168.1.1`. The USB RX counter rose from about 90 to 108 packets, but the DHCP lease file remained zero bytes and there was no identified IP neighbor. NM emitted a dnsmasq PID-file `CAP_CHOWN` warning while dnsmasq otherwise started and bound its listeners. NAT/firewall rules could not be read without root privilege, and **no peer-side Internet or USB hop is claimed**.

**Rollback:** `nmcli connection down uuid 92eb01d2-2087-44c9-a6ff-b2420df89d33`; if restoring the old USB state is desired, `nmcli connection up uuid 662995a5-4bbe-3598-bc1a-15e9535a25f1 ifname enp0s20f0u1c2` resumes its former DHCP attempt. The NetworkManager checkpoint was destroyed only after the successful postcondition check; it no longer provides automatic rollback. Built-in uplink and Wi-Fi profiles were never modified.

**Next:** One bounded IPv6 all-nodes solicitation on this exact USB link may identify the far peer without guessing an IPv4 address. If an exact peer address and host-key match emerge, use existing authenticated SSH to inspect Prometheus-side USB/DHCP and eventually its distinct Zeus downstream subnet. If the peer remains silent, keep the share in place but do not claim the chain or run remote Nix.

## Attempt 4 — identify Prometheus ports over its actual AP

**Action:** Sent one IPv6 all-nodes ICMP packet on the exact Ouranos USB link; there was no reply or neighbor, and the USB DHCP lease remained empty. The Ouranos share deliberately has IPv6 disabled, so that result is not proof the far peer is absent. A fresh bounded Wi-Fi scan showed the saved `goldragon.criome` AP again, and `iw` showed association at about -61 dBm. Built-in Ethernet remained the selected Internet route. The Wi-Fi gateway `10.18.0.1` answered one ping, its ARP MAC matched Prometheus's previously observed Ygg Wi-Fi peer, and a strict-host-key SSH connection using the known Prometheus host-key alias returned `prometheus`. One bounded SSH read then collected nonsecret peer interfaces, networkd state, bridge membership, and counters. No private key was read or copied, and nothing was changed.

**Prometheus result:** Built-in `eno1` (Realtek RTL8125, MAC `84:47:09:75:88:68`) has carrier at 1 Gbps and IPv6 link-local but **no IPv4 or default route**. `/etc/systemd/network/10-wan.network` matches `eno1` and already requests `DHCP=ipv4`; `networkctl` says it is still configuring. Prometheus's separate ASIX USB `enp199s0f0u1` (MAC `00:0e:c6:ad:21:5d`) has carrier and is intentionally bridged into `br-lan` alongside AP `wlp195s0`, not a WAN DHCP client. `br-lan` is `10.18.0.1/24`, with three observed LAN neighbors. This makes `eno1` the configured WAN client for the Ouranos USB share and leaves the Prometheus USB/bridge as the downstream Zeus candidate; **physical cable correspondence and Zeus identity are not yet proven**. Do not detach the downstream USB from the bridge or collapse the upstream `10.44.0.0/24` and downstream `10.18.0.0/24` subnets.

**Before/after:** Ouranos's USB share stayed at `10.44.0.1/24` with no DHCP lease. Its RX rose from 108 to about 125 packets; Prometheus `eno1` had 351 RX / 101 TX packets and carrier. These counters are suggestive but not a packet-level cable proof. Neither host has a proven end-to-end Internet path through this chain. Prometheus's Ygg route had flapped, but the direct AP management route succeeded while associated.

**Change / rollback:** Read-only and one bounded link-local packet; no configuration change or rollback. Both SSH paths kept strict known-host-key checking. Prometheus `sudo -n` and `run0 --no-ask-password` also require interaction, so privileged peer packet capture/firewall reads were not available to this account.

**Next:** On Prometheus, attempt a bounded DHCP renewal of the already-configured `eno1` client through a supported unprivileged networkd control path if available. Compare its TX with Ouranos USB RX, look for an Ouranos DHCP lease, and inspect the exact link. If no DHCP exchange occurs, investigate physical cable or firewall/NAT via an authorized privileged path. Preserve the AP/USB bridge and management route.

## Attempt 5 — prove cable and diagnose DHCP suppression

**Action:** An unprivileged `networkctl renew eno1` was denied by Polkit. CriomOS `users.nix` explicitly projects admin SSH public keys to root; one bounded, strict-known-host-key SSH with the existing default identity reached `root@prometheus`, and the same existing-key method reached `root@ouranos`. No private key was read, copied, forwarded, or printed. Root-scoped read/capture then compared both sides of the intended cable. An initial root `networkctl renew eno1` exited 0 but emitted no observed DHCP packet during an eight-second capture. One root `networkctl reconfigure eno1` on that exact interface then caused two DHCP requests visible **both** leaving Prometheus `eno1` and arriving on Ouranos USB. No DHCP offer was observed.

For a separate exact MAC witness, one bounded Ouranos USB ARP request for `10.44.0.2` was captured on Prometheus `eno1`: frames from Ouranos ASIX MAC `00:0e:c6:33:4f:97` requested the address while `eno1` RX rose. This proves the Ouranos USB-to-Prometheus built-in-Ethernet cable mapping; the lack of an IP reply is expected before Prometheus obtains a lease. The Prometheus USB remains downstream in `br-lan` and was not touched.

**Causal finding:** On Ouranos, root `iptables` inspection showed the `nixos-fw` INPUT chain has no ingress allowance on the USB interface for DHCP UDP/67 or DNS TCP/UDP/53 and ends in a drop. IPv4 NAT `POSTROUTING` has no masquerade rule. `FORWARD` policy is ACCEPT. The NetworkManager shared profile had started dnsmasq and enabled per-interface forwarding, but its necessary firewall/NAT policy was absent in the installed ruleset. This explains requests arriving at USB while dnsmasq records no discover/offer and predicts that peer Internet would fail even after DHCP without NAT.

**Before/after:** Prometheus `eno1` still had only IPv6 link-local and no default route; Ouranos USB lease file remained empty. The networkd reconfigure was scoped to `eno1` and kept the AP/br-lan management path intact. No firewall rule, profile, source, or route was changed in this attempt.

**Rollback:** None for the read/capture. The `eno1` reconfigure only re-applied its existing networkd file; the intended DHCP-client state was already present. No daemon restart occurred.

**Next:** Temporarily add exact USB-interface DHCP and DNS accept rules in `nixos-fw`, plus `10.44.0.0/24` masquerade **only** out built-in `enp0s31f6`, with duplicate checks and exact delete rollback. Trigger one bounded DHCP reconfigure, then verify lease, peer address/default route, DNS, and Internet egress from Prometheus. Only after runtime proof should the firewall/NAT policy be made declarative.

## Attempt 6 — scoped runtime firewall/NAT repair and first-hop proof

**Action:** With exact root SSH, checked that four proposed rules were absent, then added only: DHCP UDP/67 ingress on Ouranos USB `enp0s20f0u1c2`; DNS UDP/53 and TCP/53 ingress on that USB from `10.44.0.0/24`; and IPv4 NAT masquerade for `10.44.0.0/24` **only** when exiting Ouranos's built-in upstream `enp0s31f6`. Rules have unique `field-6db4fe-*` comments, are runtime-only, and were checked after insertion. The script would delete only the rules it added if insertion/postchecks failed. No firewall policy was disabled and no Wi-Fi/AP or other route changed. One Prometheus `networkctl reconfigure eno1` then triggered its existing DHCP client.

**Before:** Prometheus DHCP requests were captured on both `eno1` and Ouranos USB, but Ouranos `nixos-fw` dropped input to UDP/67, dnsmasq logged no discover, Prometheus had no IPv4/default route, and NAT POSTROUTING had no masquerade.

**After:** Ouranos dnsmasq logged DISCOVER, OFFER, REQUEST, and ACK for Prometheus `eno1` MAC `84:47:09:75:88:68`, leasing `10.44.0.148/24`; the lease file names `prometheus`. Prometheus networkd reports `10.44.0.148/24` and default route `10.44.0.1` on `eno1`; `ip route get 1.1.1.1` selects that route. Prometheus resolved `cache.nixos.org` and `curl -4 -I https://cache.nixos.org` returned HTTP/2 200. Ouranos itself still sends Internet traffic over built-in `enp0s31f6` via `192.168.1.1`. Its DHCP rule counter reached 2 packets and scoped MASQUERADE reached 91 packets, proving actual egress through the new NAT rule. DNS-accept counters were still zero; DNS resolution is proven from Prometheus, but use of Ouranos DNS listener specifically is not. **The Ouranos built-in Ethernet → USB share → Prometheus first hop is now working.**

**Exact rollback:** As root on Ouranos, delete only these four runtime rules:

```sh
iptables -w 2 -D nixos-fw -i enp0s20f0u1c2 -p udp --dport 67 -m comment --comment field-6db4fe-dhcp -j ACCEPT
iptables -w 2 -D nixos-fw -i enp0s20f0u1c2 -s 10.44.0.0/24 -p udp --dport 53 -m comment --comment field-6db4fe-dns-udp -j ACCEPT
iptables -w 2 -D nixos-fw -i enp0s20f0u1c2 -s 10.44.0.0/24 -p tcp --dport 53 -m comment --comment field-6db4fe-dns-tcp -j ACCEPT
iptables -w 2 -t nat -D POSTROUTING -s 10.44.0.0/24 -o enp0s31f6 -m comment --comment field-6db4fe-nat -j MASQUERADE
```

The preexisting in-memory NM share can separately be taken down via its exact UUID in Attempt 3. Deleting the rules or a firewall reload before the declarative repair is active breaks this first hop; do not treat runtime success as durable deployment.

**Next:** Verify Zeus's actual downstream presence on Prometheus's existing `br-lan`/USB side, exact host identity, DHCP/default/DNS/Internet and routed egress through Prometheus. Independently prepare persistent Ouranos USB-only sharing/autoconnect and authored firewall/NAT source under an exact owner lock; do not collapse the two subnets or touch Prometheus AP management.

## Attempt 7 — configured builder handshake and full downstream chain proof

**Action:** Read-only, bounded checks after the first hop worked. Read `/etc/nix/machines` on Ouranos, then used its existing configured host identity with `NIX_SSHOPTS`, batch SSH, strict known-host-key checking, and ten-second limits to run `nix store info --store ssh-ng://nix-ssh@prometheus.goldragon.criome`. No key material was read, copied, printed, or forwarded. A first generic root-identity store probe was denied; the configured identity probe succeeded. No derivation was built and no local fallback occurred.

Independently used strict known-host-key SSH to the exact configured Zeus Yggdrasil name, then read its live interfaces/routes and Prometheus's bridge FDB/neighbors. One bounded Zeus DNS lookup and HTTPS HEAD checked downstream Internet reachability. No interface, firewall, profile, key, or route changed in this attempt.

**Builder result:** The configured `ssh-ng` remote store returned `Store URL: ssh-ng://nix-ssh@prometheus.goldragon.criome`, `Version: 2.34.6`, `Trusted: 1`. This proves the configured SSH/Nix-store handshake at this moment, not a Nix evaluation, build, remote test, or durable builder deployment. The initial generic identity denial was an identity mismatch, not a builder outage.

**Zeus identity and route:** Zeus returned hostname `zeus`. Its built-in Ethernet `enp0s31f6` has MAC `90:2e:16:47:ea:e3` and DHCP address `10.18.0.103/24`; that exact MAC appears in Prometheus's `br-lan` FDB **on USB bridge port `enp199s0f0u1`**, and Prometheus's neighbor table maps `10.18.0.103` to it. Zeus's Wi-Fi `wlp0s20f3` is also on the LAN at `10.18.0.108/24`, but its metric-600 default is secondary. `ip route get 1.1.1.1` on Zeus selects built-in Ethernet via Prometheus `10.18.0.1` at metric 100. Prometheus itself routes outward on `eno1` from `10.44.0.148` via Ouranos USB `10.44.0.1`. Zeus resolved `cache.nixos.org`, and `curl -4 -I --max-time 8 https://cache.nixos.org` returned HTTP/2 200. Together with Attempt 6's Prometheus lease/HTTPS and Ouranos NAT counter, this proves live Ouranos built-in Internet → Ouranos USB share → Prometheus built-in Ethernet → Prometheus USB bridge → Zeus built-in Ethernet egress. Zeus's secondary Wi-Fi was present but was not the selected egress route.

**Limit:** Prometheus has IPv4 forwarding enabled; its shell did not have `iptables` in root's command path, so this attempt did not read its NAT/firewall rules or their counters. The endpoint route and HTTPS result establish functional egress, not the exact internal Prometheus NAT implementation. Ouranos's DHCP/DNS/NAT accept rules and shared NM profile remain runtime-only/in-memory; a firewall reload, profile loss, or host restart may break the chain. Declarative durability and an actual remote Nix build/test remain open separate gates.

**Change / rollback:** No change in Attempt 7, so no new rollback. To undo the temporary first-hop repair if needed, use Attempt 6's four exact rule deletions and Attempt 3's exact share-profile down command. Do not run that rollback while this working chain is required and no durable replacement is active.

**Next:** Land and deploy an interface-specific Ouranos NM share/autoconnect plus scoped firewall/NAT declaration, then validate after reactivation without disturbing its built-in default route or Prometheus's AP/bridge. Run the actual configured remote build gate only for an approved candidate, with local fallback disabled; the successful store handshake alone does not mark the pending Nix gate passed.

## Attempt 8 — persist the exact working Ouranos USB share profile

**Action:** Coordinated the exact desired values with the sole source owner. Read only the NetworkManager profile's nonsecret fields and its D-Bus `Unsaved` property: the active `prometheus-share-temporary` UUID `92eb01d2-2087-44c9-a6ff-b2420df89d33` was in memory, `autoconnect=no`, priority 0, pinned by interface name but not MAC. The competing ineffective `Wired connection 2` on the same USB interface had autoconnect yes. Created a 120-second NetworkManager checkpoint for **only** Ouranos USB `enp0s20f0u1c2`, then modified **that existing UUID in place** with `connection.autoconnect yes`, `connection.autoconnect-priority 200`, and `802-3-ethernet.mac-address 00:0e:c6:33:4f:97`. No clone, new UUID, Wi-Fi, built-in uplink, other host, or firewall change. Destroyed the checkpoint after postconditions.

**After:** The same active share retained `ipv4.method shared`, `10.44.0.1/24`, `ipv4.never-default yes`, exact USB interface and MAC, and now autoconnect yes/priority 200. D-Bus `Unsaved` became false; root filesystem metadata showed `/etc/NetworkManager/system-connections/prometheus-share-temporary.nmconnection` mode 600. No keyfile contents or secrets were read. USB still reports the same active connection, and Ouranos `ip route get 1.1.1.1` still selects built-in `enp0s31f6` via `192.168.1.1`. This proves the profile is now saved and configured for auto-selection; no cable disconnect or reboot was performed, so cold reactivation is not yet directly witnessed. The live NAT/firewall rules of Attempt 6 remain runtime-only.

**Rollback:** Before this change, the same UUID was in-memory with `autoconnect no`, priority 0, and no MAC constraint. For an intentional revert, modify that exact UUID to `connection.autoconnect no connection.autoconnect-priority 0 802-3-ethernet.mac-address ''`; remove only `/etc/NetworkManager/system-connections/prometheus-share-temporary.nmconnection` if restoring the old unsaved-only state is also required, after ensuring the active profile is no longer needed. The temporary checkpoint was destroyed after verification and is not an active rollback timer. Do not revert while the working chain is required.

**Next:** The CriomOS source owner is authoring an exact same-UUID/interface/MAC/priority profile plus firewall/NAT declaration, with replacement of this one saved keyfile rather than a second DHCP profile. Validate its narrow activation and resulting firewall/profile survival before declaring durability; do not infer firewall persistence from this NM-only step.
