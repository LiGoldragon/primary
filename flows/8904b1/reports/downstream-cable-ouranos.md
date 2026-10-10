# Downstream cable on Ouranos: Yggdrasil, USB downlink, and Zeus

Subflow of Psyche Fable 8904b1, 2026-09-28 (around 10:10 local). Read-only. Nothing was changed on any host. One SSH session was opened to Prometheus, as user `li`, and ran only observation commands. An earlier attempt failed locally on a bracketed-address syntax error before it made any connection. No SSH was made to Zeus.

Marks: **[O]** observed in this session · **[R]** claimed by a record · **[U]** unknown.

## Headline

- **[O]** Right now Yggdrasil *does* run over Ouranos's downstream cable. There is one established Yggdrasil TCP session, from `[fe80::48e0:7aff:fe6e:472a]%br-downlink:57353` on Ouranos to `[fe80::8647:9ff:fe75:8868]:10001`. Prometheus shows the same session from its side, on `eno1`. Prometheus's Yggdrasil address answers ping from Ouranos in 3–14 ms (average 7 ms). The records put the Wi-Fi path at about 92 ms, so this traffic is taking the cable.
- **[O]** Zeus is unreachable over Yggdrasil, both from Ouranos and from Prometheus: 100% loss to `200:17f7:4fad:e50b:a50c:2048:2169:41f7`.
- **[O]** The link that is down is **Prometheus's** downstream cable. Its USB NIC `enp199s0f0u1` is a `br-lan` port in state `NO-CARRIER`/`disabled`. Zeus's former LAN addresses `10.18.0.103` and `10.18.0.108` show `FAILED` in Prometheus's neighbour table.
- The living's picture, that Ouranos's cable is not carrying Yggdrasil, matches the record of 2026-09-24. It does not match what is running today (see §4).

## 1. The feature as the source defines it

Source: CriomOS `main` `d04257a` (matches the remote). Module: `modules/nixos/network/usb-downlink.nix`, plus the shared match in `modules/nixos/network/usb-ethernet-role.nix`.

- **Declaration [R source].** Horizon capability `UsbDownlink.{ <ipv4Network> }`. The gateway is the network's first address. The DHCP pool runs from .10 to the second-to-last address.
- **Matching [R source].** Links are selected by udev bus role (`Property=ID_BUS=usb`, `Type=ether`), never by name, MAC or driver. The same role file feeds a udev rule that sets `NM_UNMANAGED=1`.
- **On a node without the Router feature (Ouranos) [R source]:**
  - networkd enslaves every USB Ethernet link to bridge `br-downlink` (`05-usb-downlink.network`). The bridge gets the gateway address, IPv6 link-local only, and `IPv6AcceptRA=false` (`40-br-downlink.network`).
  - Kea DHCPv4 serves on the bridge, with routers and DNS both set to the gateway.
  - systemd-resolved listens on the gateway (`DNSStubListenerExtra`).
  - NixOS NAT uses `internalInterfaces = [ br-downlink ]` and no external interface, so it masquerades toward whichever link holds the default route.
  - The NixOS firewall opens UDP 53/67 and TCP 53 on the bridge.
  - NetworkManager is told to leave the USB links (through udev) and the bridge (through `unmanaged`) alone.
- **On a Router node (Prometheus) [R source].** The module adds only an assertion that the declared network equals the router LAN (`10.18.0.0/24`, from CriomOS-lib `lib/default.nix:89-91`). The router module (`modules/nixos/router/default.nix`) provides the downlink:
  - `05-usb-eth` puts every USB Ethernet link except the declared WAN into `br-lan`. That is the same bridge as the Wi-Fi AP, with address `10.18.0.1/24`.
  - Kea serves `br-lan`.
  - One nftables table owns the firewall and the masquerade (NixOS NAT and firewall are turned off).
  - The WAN input policy drops by default. It admits link-local UDP 9001 and TCP 10001, plus link-local NDP on the WAN (commit `73ba25c`, merged `a50e20c`).
- **Yggdrasil over the link [R source].** The module `modules/nixos/network/yggdrasil.nix` is identical on both hosts:
  - `MulticastInterfaces = [{ Regex = ".*"; Beacon; Listen; Port = 10001 }]`.
  - No static `Peers`. Record 9ddcbc also read both combined configs and found `Peers` and `InterfacePeers` empty.
  - Peering over the cable therefore depends only on link-local IPv6 plus NDP on both ends, and on TCP 10001 and UDP 9001 being admitted.

## 2. Prometheus and Ouranos side by side

| | Ouranos | Prometheus |
|---|---|---|
| Horizon (goldragon `dc57e80`) [R] | `UsbDownlink.{ 10.44.0.0/24 }`, no Router | `Router.{}` + `RouterInterfaces { eno1 wlp195s0 … MX }`; **no UsbDownlink** (UPGRADES.md: "its Router LAN already is 10.18.0.0/24") |
| Owning module | usb-downlink.nix (non-router branch) | router/default.nix |
| Bridge / subnet [O] | `br-downlink` 10.44.0.1/24, USB port only | `br-lan` 10.18.0.1/24, USB port **and** Wi-Fi AP |
| Uplink manager [O] | NetworkManager (`enp0s31f6` and `wlp0s20f3`, both 192.168.1.x) | networkd `10-wan.network` on `eno1` (DHCP; now 10.44.0.148 from Ouranos) |
| DHCP / DNS | Kea / resolved stub | Kea / dnsmasq |
| NAT / firewall | NixOS NAT + NixOS firewall | own nftables table |
| USB match [O] | `ID_BUS=usb`, `Type=ether` | same, plus `Name=!eno1` |
| Yggdrasil config [O Ouranos, R Prometheus] | multicast `.*`, port 10001, no peers | same module |
| Ygg firewall | TCP 10001 / UDP 9001 open on every interface | link-local 9001/10001 + WAN NDP only |

Neither host matches by MAC address or driver. The Ouranos NIC is an ASIX AX88179A (`cdc_ncm`, 00:0e:c6:33:4f:97) [O].

## 3. What Ouranos shows now [O]

- `enp0s20f0u1c2` is present, has carrier at 1 Gbps, and is enslaved to `br-downlink` in the forwarding state. The bridge holds 10.44.0.1/24.
- Downstream client: MAC `84:47:09:75:88:68` at 10.44.0.148. This is Prometheus's `eno1`: Prometheus shows `10.44.0.148/24` and `fe80::8647:9ff:fe75:8868` on it. IPv4 ping works at about 2 ms. Ping to its link-local IPv6 address fails, which fits Prometheus's WAN policy (it admits only ICMPv4 echo). The Kea lease file was unreadable (permission).
- Yggdrasil has a single established peer, the one over `br-downlink` described above. `yggdrasilctl` was refused (socket permission).
- Routes: `200::/7` goes to `yggTun`. There is **no route to 10.18.0.0/24**: `10.18.0.1` resolves through 192.168.1.1. That is expected, because every hop is NAT.
- **Defect:** NetworkManager still manages the USB port.
  - `nmcli` shows `Wired connection 2`, `NM-MANAGED yes`, stuck in "getting IP configuration".
  - The port carries NM's own address `fe80::4e94:9c8e:1256:ca8b`, and Yggdrasil listens on that too.
  - The resolved journal logs `LinkBusy`.
  - The `NM_UNMANAGED` udev rule is deployed in `99-local.rules`, but the device's udev properties do not carry it. The device was initialised about 110 s after boot, and the generation was activated later, on Sep 26 at 17:38. The rule has never run on this device.

On Prometheus [O]:
- Uptime is about 2.5 days.
- `05-usb-eth.network` is live.
- `enp199s0f0u1` has NO-CARRIER.
- `wlp195s0` is forwarding in `br-lan`.
- The only Yggdrasil session is to Ouranos over `eno1`.
- Zeus does not answer ping.

## 4. Why Zeus cannot be reached: causes that fit the evidence

1. **No link on Prometheus→Zeus [O symptom, U cause].** Prometheus's USB NIC has no carrier. Possible reasons: Zeus is powered off or asleep, the cable is unplugged or bad, or Zeus's port is administratively down. The way to tell them apart is Zeus's console (`ip -br link`) or checking the cable or port LEDs.
2. **Zeus is off, or its Yggdrasil is not running.** Zeus is absent from Prometheus's AP too (FAILED neighbours), and no multicast peer appears on Ouranos's home LAN. Seeing Zeus's power state separates this from cause 1.
3. **Zeus's uplink profile has IPv6 disabled (as Ouranos's once did).** This is only possible, not shown [U]: it would stop Yggdrasil even with carrier present. The test is `ip -6 addr` on Zeus's built-in port once it has carrier.
4. **The living's cable statement describes 09-24 [R].** 9ddcbc and d8df70 found that Ouranos's USB profile had IPv6 disabled and that Prometheus's WAN dropped NDP, so Yggdrasil rode Wi-Fi. Both are fixed; the fix is now deployed and the cable session is up [O]. The living's typed words of 09-26, "I can only ping Prometheus from Zeus. I cannot ping Uranus" (9ac67c/log.md), have no witness from Zeus's side.

The NetworkManager co-management on Ouranos (§3) does not explain Zeus's absence. It is a live divergence that could disturb the port after a replug or a restart of NM.

## 5. Smallest change toward one feature, same way (not made)

- **goldragon `cluster-definition.datom`:** add `UsbDownlink.{ 10.18.0.0/24 }` to Prometheus's capabilities. The module's router branch already asserts it equals the router LAN. Also update the note in UPGRADES.md and optionally the jq check in `flake.nix`.
- **CriomOS `modules/nixos/router/default.nix`:** make `05-usb-eth` exist only when the node declares `UsbDownlink`. Then on both hosts the feature is switched on by the same declaration and matched by the same bus role.
- **CriomOS `usb-downlink.nix` (Ouranos side):** make the NM exclusion take effect on devices already present. For example, add `networking.networkmanager.unmanaged = [ "type:ethernet,..." ]`, or a match keyed on the udev property, or an activation `udevadm trigger` for net devices. Short of a source change, replugging the dongle or rebooting would apply the rule.

**What prevents full sameness:**
- Prometheus is a Router. Its USB downlink shares one L2 and subnet with its Wi-Fi AP (`br-lan`, 10.18), under one nftables owner, with networkd owning the WAN.
- Ouranos is a NetworkManager laptop. Its uplink is chosen by NM, so it gets a separate bridge, NixOS NAT and the NixOS firewall.
- Unifying fully means either making Ouranos's downlink use the router module's nftables and bridge code without the AP, or factoring the router module's LAN, DHCP and NAT pieces into the shared downlink module.
- Either is a design change, not a one-liner. It should go to the living.

## 6. Prometheus [O]

Prometheus answered at once, over Yggdrasil by name `prometheus.goldragon.criome` → `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f`. It is running `nixos-system-prometheus-26.11.20260813.0e251e2` (`/nix/store/7f8kpzcn…`).

## Earlier work [R]

- **753e69 (09-22):** the living set the pattern: built-in port is uplink, USB is downlink. It became the `testing-transitive-network-topology` skill.
- **836818 (09-23):** Zeus was seen on `br-lan` at 10.18.0.103–108.
- **d8df70 / 9ddcbc (09-24):** found Ouranos's NM USB profile with IPv6 disabled (repaired live) and Prometheus dropping WAN NDP. Fixed in CriomOS `73ba25c` / `a50e20c`. Deployment was blocked then by a Horizon shape mismatch.
- **da88cf / b860be (09-25/26):** wrote `usb-downlink.nix`, the hotfix-removal script and the checks. They declared `UsbDownlink` on Ouranos only. They issued `da88cf/reports/daisy-chain-test-brief.md`; no record of it being run was found.
- **9ac67c (09-26):** the living plugged Zeus into Prometheus's cable and got no IP.
- **Where it stopped:** Zeus's Lojix deployment and the daisy-chain test.

## Sources

- Live on Ouranos: `ip -d link`, `ip addr`, `ip route`, `ip neigh`, `bridge link/fdb`, `networkctl status`, `nmcli dev show`, `udevadm info`, `ss -tan/-tln/-uln`, `ping`, `/etc/systemd/network/*`, `/etc/udev/rules.d/99-local.rules`, `/etc/NetworkManager/NetworkManager.conf`, the yggdrasil unit and `/nix/store/qjz7i39v…-yggdrasilConf.json`, `journalctl -u NetworkManager`.
- Live on Prometheus (one SSH): `ip -br addr`, `bridge link`, `ip neigh dev br-lan`, `ss -tn`, `ping`, `/etc/systemd/network/05-usb-eth.network`.
- `/git/github.com/LiGoldragon/CriomOS` main `d04257a`: `modules/nixos/network/usb-downlink.nix`, `usb-ethernet-role.nix`, `yggdrasil.nix`, `modules/nixos/router/default.nix`.
- `/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix:89-91`.
- `/git/github.com/LiGoldragon/goldragon` main `dc57e80`: `cluster-definition.datom`, `UPGRADES.md`, `flake.nix`.
- Flow records: `flows/752e0f/reports/zeus-link-and-mesh-2026-09-25.md`, `flows/9ddcbc/reports/usb-yggdrasil-durable-repair-2026-09-24.md`, `flows/9ac67c/log.md`, `flows/b860be/reports/handoff.md`, `flows/b7da5d/reports/refresh-handoff-2026-09-26.md`, `flows/da88cf/reports/daisy-chain-test-brief.md`, `flows/8904b1/vision/anatomy.md`.

## Zeus switched on, 2026-09-28

Subflow of Psyche Fable 8904b1. Read-only, one SSH session to Prometheus plus direct probes from Ouranos. Picture settled on the first pass (~10:25 local), well inside the ten-minute window; no repeat polling was needed.

1. **[O] Carrier and lease, on Prometheus.** `enp199s0f0u1` (the USB adapter toward Zeus) shows `UP` with `LOWER_UP`, enslaved to `br-lan` in forwarding state. Kea's journal shows a DHCP exchange at 10:23:39–10:23:41 for client MAC `90:2e:16:47:ea:e3`: `DHCP4_LEASE_ALLOC` granted `10.18.0.103` for 4000 seconds. `ip neigh` confirms `10.18.0.103 dev br-lan lladdr 90:2e:16:47:ea:e3 REACHABLE`.
2. **[O] Zeus peers over the cable, not the Wi-Fi AP.** `bridge fdb show` places MAC `90:2e:16:47:ea:e3` on `dev enp199s0f0u1 master br-lan` — the USB port, not `wlp195s0`. `ss -tn` on Prometheus shows an established Yggdrasil TCP session on port 10001 between `fe80::4435:5dff:fecb:10a2%br-lan` (Prometheus's bridge address) and `fe80::9ca9:3db7:4354:3cd1`, and `ip neigh` ties that link-local address to the same MAC `90:2e:16:47:ea:e3`. Since that MAC's only FDB entry is the USB port, this Yggdrasil session rides the cable. This is the outcome the living wants: no dependency on Wi-Fi was observed to be in play for this peering.
3. **[O] From Ouranos, Zeus answers.** Zeus's Yggdrasil address is `200:17f7:4fad:e50b:a50c:2048:2169:41f7` (resolved on Prometheus via `getent hosts zeus.goldragon.criome`, unchanged from the earlier record). Ping from Ouranos: 4/4 received, 2.9–29.1 ms. SSH from Ouranos to `li@zeus.goldragon.criome` answered within the timeout and ran the two permitted read commands:
   - `uname -a` → `Linux zeus 7.1.8 #1-NixOS SMP PREEMPT_DYNAMIC Sun Aug 9 18:26:58 UTC 2026 x86_64 GNU/Linux`
   - generation → `/run/current-system` → `/nix/store/kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2`, `VERSION="26.11 (Zokor)"`, `VERSION_CODENAME=zokor`.
4. **Not applicable.** Yggdrasil did peer over the cable, so the fourth branch (diagnosing why it would not) was not needed. No firewall-counter, link-local, or multicast investigation was performed since there was nothing to explain.

Unknowns: whether `yggdrasilctl` on Prometheus would show Zeus by its persistent Yggdrasil identity rather than by link-local — `getself`/`getpeers` were refused by socket permission (`dial unix .../yggdrasil.sock: connect: permission denied`), not attempted with elevated privilege since this session is read-only. Zeus's own view of its interfaces and Yggdrasil state was not read (no SSH command beyond the two specified was run).
