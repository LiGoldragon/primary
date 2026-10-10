# The Ouranos–Prometheus cable fault, 26–27 September

Subflow of Psyche Fable 8904b1, written 2026-09-28 around 10:45 local (CST, UTC−6). Read-only. The only actions taken were journal reads on both hosts, one read-only SSH command batch to Prometheus (`journalctl`, `ip neigh`, `ip -br link`, `networkctl status`, `systemctl --version`), and local reads of `ip`, `bridge`, `udevadm`, flow records, agent transcripts and the shell history. Nothing was changed on either host.

Marks: **[O]** observed in a record · **[I]** inferred by me · **[U]** unknown.

## Answer

- **[O]** From 26 Sep 17:38:35 until 27 Sep between 18:35 and 18:46:42, **unicast frames sent from Prometheus to Ouranos's bridge did not arrive**. Broadcast and multicast frames did arrive, and frames from Ouranos to Prometheus got through.
- **[O]** Everything that failed needed that direction:
  - ping and TCP 22/80 to 10.44.0.148;
  - IPv6 neighbour discovery toward Prometheus;
  - Prometheus's unicast DHCP renewals;
  - the Yggdrasil session over the cable, and with it `prometheus.goldragon.criome`.
- **[O]** Ouranos's Wi-Fi was off for that whole period, so Ouranos had **no Yggdrasil peer at all** for about 25 hours.
- **[O]** The fault began at the activation of 26 Sep 17:38. It cleared when the living ran `ssh root@localhost -- systemctl restart yggdrasil` (journal 27 Sep 18:46:31–32). The cable peering came up 10 seconds later, and IPv4 unicast worked from then on.
- **[I]** The most likely cause is this. When the activation started NetworkManager at 17:38:35, NetworkManager still managed the USB port (the adapter was present before the new udev rule existed). It pulled the port out of the new bridge, and networkd put it back within the same second. The adapter's hardware receive filter was left not accepting frames addressed to the bridge's MAC, which is not the adapter's own MAC. Restarting Yggdrasil changed the port's multicast memberships, which makes the kernel send the adapter's filter again. The records do not show the filter itself. So this mechanism is inference, and it is the leading candidate, not a proven cause.

## 1. Timeline (local time, CST)

| Time | Host | Event | Mark |
|---|---|---|---|
| 25 Sep 21:15:44 | Prometheus | Current boot begins. No reboot, suspend or activation happened on Prometheus after this. | O |
| 26 Sep 16:18:53 | Ouranos | Current boot. The USB NIC was renamed `enp0s20f0u1c2` at 16:20:39. No suspend or reboot happened after this. | O |
| 26 Sep 16:20:45–46 | Prometheus | `eno1` link up at 1 Gb/s. DHCP gives 10.44.0.148 from 10.44.0.1, which was NetworkManager's shared connection, with the address on the NIC itself. | O |
| 26 Sep 16:20:46 | both | Yggdrasil session on the cable: Ouranos `fe80::c730…%enp0s20f0u1c2` ↔ Prometheus `eno1`. | O |
| 26 Sep 17:38:29 | Ouranos | `switch-to-configuration test` of `dbhsh7wp…-nixos-system-ouranos`. It stops NetworkManager. | O |
| 26 Sep 17:38:30 | Ouranos | The usbDownlink activation removes the hotfix NM profile `prometheus-share-temporary`, the firewall drop-in and the script. | O |
| 26 Sep 17:38:35 | Ouranos | networkd enslaves the port to `br-downlink` (bridge MAC `4a:e0:7a:6e:47:2a`, NIC MAC `00:0e:c6:33:4f:97`). The kernel logs the port entering promiscuous mode. 10.44.0.1 appears on the bridge. | O |
| 26 Sep 17:38:35 | Ouranos | NetworkManager starts. In the same second the port **leaves** promiscuous and allmulticast mode, the bridge port goes to "disabled", and charon logs "interface enp0s20f0u1c2 deleted". networkd then reconfigures the port, and it **enters** promiscuous mode and forwarding again. | O |
| 26 Sep 17:38:35 | Ouranos | NetworkManager warns `LinkBusy: Link enp0s20f0u1c2 is managed` (it is still managing the port). | O |
| 26 Sep 17:38:36 | Ouranos | NetworkManager's address `fe80::4e94…` is on the bridged port, and Yggdrasil listens on it. Yggdrasil's listener on `br-downlink` starts at 17:38:38. | O |
| 26 Sep 17:39:35 | Ouranos | Kea starts on `br-downlink`. The switch itself finishes with **status 4** (failed) at 17:41:36. | O |
| 26 Sep 17:39:50 / 17:40:50 | Ouranos / Prometheus | The cable Yggdrasil session drops (read timeout). **No** new cable session is logged by either side until 27 Sep 18:46:42. | O |
| 26 Sep 18:08:36 → 27 Sep 18:35 | Ouranos (Kea) | Every DHCPREQUEST from Prometheus's MAC arrives as **broadcast, "from 0.0.0.0 to 255.255.255.255"**, every 33.3 minutes, and Kea ACKs each one. | O |
| (same period) | Kea config | `renew-timer 1000`, `rebind-timer 2000`, `valid-lifetime 4000` (source `usb-downlink.nix` at d04257a). | O |
| (same period) | — | So Prometheus's unicast RENEWs, sent at T1 = 1000 s, never reached Kea. Only the broadcast REBIND at T2 = 2000 s arrived. | I |
| 26 Sep 19:16 | Ouranos (Field probe) | Neighbours `fe80::8647:9ff:fe75:8868` (Prometheus) show **FAILED** on both `br-downlink` and the port. 10.44.0.148 is STALE. `nc -zvw3 10.44.0.148 22` times out at 19:17. | O |
| 26 Sep 19:28 | Ouranos (probe) | `curl http://10.44.0.148/` times out. SSH to `prometheus.goldragon.criome` and to `100.64.0.1` both exit 255 with a timeout. | O |
| 27 Sep 00:12 | Ouranos (probe) | `ping -c1 -W2 10.44.0.148`: 0 of 1 received. The neighbour goes STALE→DELAY (the frame went out). `arping` refused (raw socket). | O |
| 27 Sep 00:24 | Ouranos (probe) | Strict SSH to the Yggdrasil FQDN, to 10.44.0.148 and to the tailnet each time out on TCP 22. | O |
| 27 Sep 07:36:55 | Ouranos (Mind probe) | `ssh … root@prometheus.goldragon.criome 'hostname'` → exit 255, "Connection timed out". This is the "strict root SSH TCP22 exit255". | O |
| 26 Sep 17:xx → 28 Sep 09:xx | Prometheus sshd | **No connection from Ouranos arrives, not even a pre-auth one.** Before and after this window sshd accepts Ouranos over Yggdrasil. | O |
| whole window | Prometheus | Alive throughout: its Kea serves Zeus on br-lan, hostapd is active, the lease-recovery timer runs every 2 minutes, and it keeps renewing its lease with Ouranos. | O |
| 26 Sep 17:39 → 27 Sep 18:47 | Ouranos | Wi-Fi not associated. The first Wi-Fi connection is 27 Sep 18:47:15. | O |
| 27 Sep 18:42:07 | Ouranos | A USB card reader is plugged in (bus 2-2; the Ethernet adapter is on bus 4-1). | O |
| 27 Sep 18:44:39 | Prometheus | Its USB port toward Zeus loses carrier. | O |
| 27 Sep ≈18:46 | Ouranos (shell history, untimed) | The living runs `ping prometheus.goldragon.criome` (fails), then `ssh root@localhost -- systemctl restart yggdrasil`, then pings again. | O (order), I (exact time) |
| 27 Sep 18:46:31–32 | Ouranos | A root SSH login from ::1, then yggdrasil stops and starts. This is the living's command. | O / I (link) |
| 27 Sep 18:46:42 | both | Cable Yggdrasil session up over `br-downlink` (source port 57353). It is the same session that is still up today. | O |
| 27 Sep 18:47–18:53 | Ouranos | The living brings up Wi-Fi (goldragon.criome, then Mega_2.4G_1896). Yggdrasil also peers over Wi-Fi. | O |
| 27 Sep 18:51 onward | Ouranos (Kea) | DHCPREQUESTs arrive **unicast "from 10.44.0.148 to 10.44.0.1"** every 16.7 minutes (T1). They continue to now. | O |
| 27 Sep 23:14–23:15 | Prometheus | Zeus cable flaps, then Zeus goes off. | O |
| 28 Sep 09:xx–10:xx | Prometheus sshd | nix-ssh and li sessions from Ouranos over Yggdrasil succeed. | O |
| 28 Sep 10:29 (now) | both | Prometheus has 10.44.0.1 at `4a:e0:…` REACHABLE and `fe80::48e0…` REACHABLE. The port is in `promiscuity 1`. NetworkManager still manages the port (`NM_UNMANAGED` absent in udev; initialised about 110 s after boot). Prometheus still shows `fe80::4e94…` (NetworkManager's address on the port) as FAILED. | O |

These events never occurred in the window, on either host [O]:
- a carrier change on the Ouranos USB port or on Prometheus `eno1` after 17:38:35;
- a bridge-port change after 17:38:35;
- a suspend or resume;
- a reboot;
- a Prometheus activation;
- a firewall drop log line.

The NetworkManager journal holds warnings only, so its info-level actions are not recorded [O].

## 2. What was true at each failure

- **26 Sep 19:16–19:28 (probes to 10.44.0.148, TCP 22 and 80, IPv6 neighbour):**
  - [O] The link had carrier and the bridge was forwarding. Kea was still exchanging broadcast DHCP with Prometheus. Prometheus was up.
  - [I] Ouranos's SYN and echo reached Prometheus; its reply, addressed to the bridge MAC, did not come back in.
- **27 Sep 00:12 and 00:24 (ping and SSH over the cable, Yggdrasil and tailnet):**
  - [O] The same state. There was no Yggdrasil peer at all, and the Wi-Fi was off.
  - [O] Tailnet: Prometheus has been offline in the tailnet for 197 days, so that path could not work regardless.
- **27 Sep 07:36 (Mind's root SSH, exit 255):**
  - [O] It went to the Yggdrasil address. Ouranos had no Yggdrasil peer, so it failed for the same reason.
- **"No direct Ouranos route to Zeus 10.18":**
  - [O] 10.18.0.0/24 is Prometheus's NATed LAN. Ouranos routes it via 192.168.1.1. This is true by design at every time, and it is not part of the fault.
  - [O] Zeus over Yggdrasil failed because Ouranos had no peers.
- **The living's "couldn't ping Prometheus through the cable" (27 Sep evening, before 18:46:31):**
  - [O] The command was `ping prometheus.goldragon.criome`, that is, the Yggdrasil address.
  - [O] With the Wi-Fi off, the cable was its only possible path, and the cable was down for unicast.
  - The living's account is accurate.

## 3. Causes that fit, one by one

**A. After the NetworkManager–networkd tug at 17:38:35, the USB NIC accepted no unicast frames addressed to the bridge MAC. [I, leading]**
- *For:*
  - [O] It began exactly at the enslavement, and the old session (on the NIC's own address and MAC) died 75 seconds later.
  - [O] Only frames toward Ouranos that had to pass the NIC's unicast filter failed. Broadcasts (DHCP rebind, ARP requests) and multicast (Yggdrasil beacons) passed, and so did everything Ouranos sent.
  - [O] Kea receives on a packet socket before any firewall, and it never saw a unicast RENEW until 18:51 on the 27th. So the frames were not reaching the bridge; the host's firewall did not drop them.
  - [O] ARP and NDP are not filtered by nftables or iptables, yet NDP toward Prometheus FAILED.
  - [O] Recovery coincided with the Yggdrasil restart, which leaves and rejoins multicast groups on the port.
  - [O] It works now, with Prometheus holding the bridge MAC.
- *Against:*
  - [U] The adapter's filter state was never read, and nothing in the kernel log shows it.
  - [U] Why a Yggdrasil restart would reset it: the chain (a multicast-list change calls `set_rx_mode`, which re-sends the CDC packet filter) is my inference. So is the claim that the enter/leave/enter sequence within one second left it wrong.
- *Would confirm:* next time it fails, before touching anything:
  - `ip -s link show enp0s20f0u1c2` RX counters, compared with Prometheus `eno1` TX counters while pinging;
  - on Prometheus, whether `ip neigh` holds 10.44.0.1 at `4a:e0:…`;
  - whether traffic addressed to the NIC's own MAC works (for example Prometheus pinging with a neighbour entry pinned to `00:0e:c6:33:4f:97`).
  - Record NetworkManager at info level. Note that `tcpdump` without `-p` would itself change the filter and erase the evidence.

**B. NetworkManager periodically seizing or resetting the port. [O against]**
- One seizure is observed, at 17:38:35 when NetworkManager started.
- No later bridge-port or carrier change appears in 41 hours. The `LinkBusy` warnings at 18:53, 05:38, 05:45 and 10:27 are DNS pushes and come with no link change.
- It is not periodic. Its one act at start-up is the trigger in A.

**C. Adapter plugged in before the activation. [O as a precondition]**
- Because of this the udev `NM_UNMANAGED` rule never ran on the device, NetworkManager kept the port, and the tug in A happened. This is the root condition, not the direct fault.

**D. Suspend and resume. [O ruled out]** Neither host suspended; each host stayed on one boot throughout.

**E. The attempts used a path that does not go over the cable. [O partly true, not the cause]**
- The FQDN resolves to Yggdrasil (`/etc/hosts`), 10.18 routes to the home LAN, and the tailnet peer is 197 days stale.
- But direct attempts on 10.44.0.148 over the cable failed too, and so did the DHCP unicast.

**F. Prometheus down or SSH refusing. [O ruled out]**
- Prometheus was on one boot and was logging throughout.
- It renewed its lease with Ouranos all night.
- No SSH attempt reached sshd.
- SSH over the same Yggdrasil address resumed without any change on Prometheus.

**G. Yggdrasil fell back to Wi-Fi. [O ruled out]**
- The Wi-Fi was off, so there was no fallback.
- The total loss came from having no other path.
- The Yggdrasil outage alone would not explain the IPv4 failures.

**H. The loss of Yggdrasil's own state was the cause. [O against]** It cannot explain the IPv4 ping, TCP and DHCP-unicast failures on 10.44.

## 4. Is it still there, and the mend

**Still present [O]:**
- NetworkManager still manages the port (the `Wired connection 2` profile, stuck "getting IP configuration"). Its address `fe80::4e94…` sits on a bridge port where it cannot be reached. Yggdrasil beacons it, and Prometheus keeps a FAILED neighbour for it.
- The bridge MAC still differs from the NIC's MAC, so receiving through the bridge still depends on the NIC's promiscuous filter.

**[I]** A restart of NetworkManager, or any activation that restarts it, can repeat the tug and bring the fault back. A replug or a reboot would apply the udev rule, which removes the tug but not the dependence on promiscuous mode.

**Smallest mend, in `CriomOS/modules/nixos/network/usb-downlink.nix` (not made):**
1. Make the NetworkManager exclusion take effect on devices already present. After the rule is installed at activation, re-trigger udev for net devices that match the feature's own bus-role match (`udevadm trigger --action=change --subsystem-match=net --property-match=ID_BUS=usb`, then wait for `udevadm settle`). This uses no name, MAC or driver; the feature already carries the match in `usb-ethernet-role.nix`.
2. Stop depending on the NIC's promiscuous mode: let the bridge take its port's MAC (`netdevConfig.MACAddress = "none"` on the `br-downlink` netdev) instead of networkd's generated one. This contains no host fact. Whether it suits a bridge with several dongles needs the living's or Mind's judgement.
3. Optionally, a check in `checks/usb-downlink` that no USB bridge port is managed by NetworkManager. The Router path (Prometheus's `br-lan`) has the same bridge-MAC-versus-port-MAC shape and would be judged together with it.

The cluster data (goldragon) needs no change for this.

## Sources

- Ouranos journal, boot `a77a0db5…` (26 Sep 16:18 to now): kernel, systemd-networkd, NetworkManager, kea-dhcp4, yggdrasil, sshd-session, wpa_supplicant, charon/ipsec, `switch-to-configuration` lines. The saved extract is in this subflow's scratchpad.
- Prometheus journal, boot `638be1a9…`, since 26 Sep 12:00: kernel, systemd-networkd, kea-dhcp4, yggdrasil, sshd-session, hostapd, router-wan-lease-recovery.
- Live now: Ouranos `ip -d link`, `bridge fdb`, `ip neigh`, `udevadm info`, `/etc/udev/rules.d/99-local.rules`, `systemctl cat kea-dhcp4-server`; Prometheus `ip neigh dev eno1`, `networkctl status eno1`, `systemctl --version` (systemd 261).
- CriomOS `origin/main` d04257a: `modules/nixos/network/usb-downlink.nix` (Kea timers, bridge netdev, NM exclusion). The local checkout e6a83ed: `modules/nixos/router/default.nix` (Prometheus firewall: `tcp dport ssh accept`, ICMP echo on the WAN), `wan-lease-recovery.sh`.
- Codex transcripts, `~/.codex-next/sessions/2026/09/`:
  - `26/rollout-2026-09-26T18-41-47-01a0e04f…` (19:16–19:17 neighbour, ping, nc);
  - `26/…T18-53-50-01a0e05a…` (19:28 SSH, curl, nix store);
  - `26/…T23-16-05-01a0e14a…` (00:11–00:12 arping, ping);
  - `26/…T18-00-00-01a0e029…` (Field Sol 9ac67c, 00:24 access witness);
  - `27/…T07-35-58-01a0e314…` (07:36 root SSH, exit 255).
- The living's shell history `~/.config/zsh/.zsh_history`, entries 10504–10537 (untimed; order only).
- Flow records: `flows/8904b1/log.md` (HostAccessFreshWitness; the c56100 messages; the fifteenth message), `flows/8904b1/reports/downstream-cable-ouranos.md`, `flows/9ac67c/log.md`.
