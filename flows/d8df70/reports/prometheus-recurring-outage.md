# Prometheus recurring outage: cause

## Cause (confidence: high)

Prometheus does not lose its address. Its whole kernel panics, and the panic
is inside the MediaTek MT7925 Wi-Fi driver (mt7925e / mt76), in the receive
thread of the Wi-Fi access point (`napi/phy0-0`, phy0 = wlp195s0, the hostapd
AP). The kernel is set to `kernel.panic = 0`, so after the panic the machine
sits frozen forever: power on, Ethernet PHY still shows link, no packets, no
ARP, no Yggdrasil, no journal. Only a power cycle brings it back.

Five panics are saved in pstore (archived at `/var/lib/systemd/pstore` on
Prometheus), one per outage, all the same shape:

    list_add corruption. prev->next should be next (...)
    kernel BUG at lib/list_debug.c:32!
    CPU: 22 PID: 1188 Comm: napi/phy0-0 Tainted: G U 7.0.1 #1-NixOS
    mt76_wcid_add_poll+0x95/0xd0 [mt76]
    mt7925_queue_rx_skb+0x155/0xe70 [mt7925_common]
    mt76_dma_rx_poll ... mt792x_poll_rx ... __napi_poll ... napi_threaded_poll
    Kernel panic - not syncing: Fatal exception in interrupt

(One variant is `list_del corruption` in `mt7925_mac_sta_poll`; same list,
same thread.)

| boot that died | started (local, -06) | panic uptime | panic time (local) | journal last line |
|---|---|---|---|---|
| earlier | ~09-14 | 560546 s | ~09-20 | - |
| -5 | 09-20 21:34:58 | 12636 s | 09-21 01:05 | 01:05:00 |
| -3 | 09-21 12:05:08 | 15071 s | 09-21 16:16 | 16:15:29 |
| -2 | 09-22 13:07:07 | 39299 s | 09-23 00:02 | 00:00:06 |
| -1 | 09-23 11:50:44 | 76382 s | 09-24 09:03:49 (15:03 UTC) | 09:01:44 |

Every outage matches a panic. Intervals vary from 3.5 h to 6.5 days, so it is
not a timer or lease.

## Lead hypothesis refuted: DHCP lease

- Prometheus's WAN eno1 (Realtek RTL8125, r8169) gets its address by
  systemd-networkd's DHCPv4 client (`/etc/systemd/network/10-wan.network`)
  from ouranos's NetworkManager "shared" connection
  `prometheus-share-temporary` (dnsmasq, `--dhcp-range=10.44.0.10,10.44.0.254,3600`).
- Lease: LIFETIME=1h, T1=30min, T2=52min30s, server 10.44.0.1.
- ouranos's dnsmasq log shows a clean DHCPREQUEST/DHCPACK every ~27 minutes
  for the whole 21 h boot, last one 09-24 08:46:08 local (14:46 UTC); the next
  was due ~09:13; the panic came at 09:03:49. Then silence until the DISCOVER
  of the new boot at 13:45:03. Same pattern for the 09-23 outage (last ACK
  23:37:06, panic ~00:02).
- The dnsmasq process (pid 695445) ran continuously since 09-23 16:45 local;
  no NetworkManager restart, no USB re-enumeration on ouranos in the window.
- DHCP on WAN is not blocked by nftables (renewals worked for 21 h; networkd
  uses a raw socket anyway). NDP and IPv6 are irrelevant: the host is halted.
- No r8169 errors or link-down in any dying boot. The NIC driver is not it.

## Trigger (confidence: medium)

The only client of Prometheus's AP is ouranos's Intel Wi-Fi (dc:90:09:ee:e4:a4),
which keeps losing the AP ("missed beacons ... Connection to AP
dc:56:7b:fb:76:1f lost") and reassociating: hostapd logged 165
AP-STA-CONNECTED in boot -1 alone. Three of the four panics fall within
seconds of such a drop and reassociation on ouranos:

- 09-24 09:03:37 lost, 09:03:41 authenticate; panic 09:03:49.
- 09-23 00:01:44 lost, 00:02:02-00:02:09 reauth; panic ~00:02:06.
- 09-21 01:04:13 associate, 01:04:17 lost; panic ~01:05.
- 09-21 16:16: no ouranos Wi-Fi event found.

So the station add/remove churn races the driver's station poll list; the
list corrupts and the kernel BUGs. This is a kernel driver bug (Linux 7.0.1,
`linuxPackages_latest`), not a CriomOS configuration error.

## Smallest durable fix in CriomOS (proposal only)

1. Reboot on panic instead of freezing. In `modules/nixos/router/default.nix`,
   in the existing `boot.kernel.sysctl` block, add
   `"kernel.panic" = 10;` (and `"kernel.panic_on_oops" = 1;` so an oops in a
   non-interrupt path also reboots rather than leaving a half-dead kernel).
   An outage becomes about one minute, with no human step. The board has an
   AMD SP5100 TCO hardware watchdog (`/dev/watchdog0`, `RuntimeWatchdogUSec=0`
   now); setting systemd's `RuntimeWatchdogSec` (for example 30s) also covers
   hangs that never panic.
2. Remove the trigger. Either stop ouranos from joining Prometheus's AP (it
   has the cable; its Wi-Fi to that AP is what churns), or keep the AP but
   expect panics until a kernel with a fixed mt7925 AP path is deployed.
   Disabling the AP (or the mt7925e module on the EVO-X2) removes the crash
   entirely but also removes Wi-Fi service; that is the living's choice.

Step 1 alone stops the "I have to reboot it" symptom; step 2 stops the crashes.

## What to capture if it happens again

Nothing on the console is needed: the panic is written to EFI pstore and
systemd-pstore archives it on the next boot. After the reboot:

    ls /var/lib/systemd/pstore/
    grep -h -A25 'list_.* corruption' /var/lib/systemd/pstore/<newest>/*/dmesg.txt
    journalctl -b -1 -n 50
    journalctl -b -1 -u hostapd | grep AP-STA | tail

## Sources

- ouranos: `nmcli con show prometheus-share-temporary`; dnsmasq process
  arguments; `/var/lib/NetworkManager/dnsmasq-enp0s20f0u1c2.leases`;
  `journalctl` dnsmasq-dhcp lines 09-15 to 09-24; kernel wlp0s20f3 lines.
- Prometheus (read-only ssh over the cable, uptime 1 min, 09-24 19:46 UTC):
  `ip addr show eno1`, `networkctl status eno1`,
  `/run/systemd/netif/leases/2`, `journalctl --list-boots`,
  `journalctl -b -1/-2/-3 -n 45`, `/var/lib/systemd/pstore/*/*/dmesg.txt`,
  `sysctl kernel.panic kernel.panic_on_oops`, `/sys/class/watchdog`,
  `/sys/class/net/wlp195s0/phy80211`, `lspci`, `journalctl -b -1 -u hostapd`.
- CriomOS: `modules/nixos/router/default.nix` (sysctl block, networkd,
  nftables WAN rules), `modules/nixos/metal/default.nix` (EVO-X2 loads
  mt7925e), `modules/nixos/normalize.nix` (`linuxPackages_latest`).
