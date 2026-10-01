# Prometheus AP Internet path — bounded diagnosis, 2026-09-30

## Scope and boundary

This is a read-only, host-side diagnosis for the Prometheus Wi-Fi AP. It
records observations at 23:43–23:44 local (`UTC−06:00`) and source/history
context. It does **not** establish Internet access for a particular phone,
repair a client, or authorize AP, firewall, DHCP, DNS, or routing changes.

No host command, configuration change, service restart, source edit, client
probe, or induced connection attempt was performed by Field for this report.

## Current observations

### Ordinary-user witness — 2026-09-30 23:43:14−06:00

- AP radio and `br-lan` were `UP,LOWER_UP`.
- `hostapd`, `dnsmasq`, and Kea were active since 29 September.
- Two clients were associated and had completed WPA handshakes. Kea allocated a
  `10.18.0.x` lease at 23:42:32; identities are deliberately omitted.
- The wired upstream default route via `192.168.1.1` was present on a
  lower-up interface. An HTTPS request from Prometheus to `example.com`
  returned HTTP 200.
- `resolvectl` was unavailable because the systemd-resolved socket/unit was
  absent. This describes the host's resolver interface; it does not show a
  client DNS failure. `dnsmasq` was active with configured upstream resolvers.
- Unprivileged firewall rules/counters could not be read. No conclusion about
  client packet traversal follows from that limitation.

### Root read-only witness — 2026-09-30 23:44:29−06:00

- `net.ipv4.ip_forward=1`.
- The nftables forward chain had default drop plus explicit `br-lan → eno1`
  acceptance and `eno1 → br-lan` established/related acceptance. NAT
  postrouting masqueraded traffic leaving `eno1`.
- `br-lan`, the AP radio, and two USB members were forwarding; the wired
  default remained via `eno1`.
- `hostapd`, `dnsmasq`, and Kea were active. Kea logged two allocations in the
  23:42:00–23:43:30 window; client identities are omitted.
- In the last 300 dnsmasq journal lines, failure/error/refused/unreachable/
  timeout count was zero and query-line count was zero. That supplies no
  per-client DNS-use witness.
- nft counter evidence was not supplied. `conntrack` was unavailable. The TCP
  port-53 listener count was four; the attempted UDP counting command had
  incompatible `ss` formatting and must not be read as absence of UDP DNS.

## What this supports

At the two observation times, the declared host-side prerequisites for an AP
client Internet path were present: radio/bridge link, WPA association, DHCP
allocation, wired default route, IPv4 forwarding, forwarding policy, and WAN
masquerade. Prometheus itself reached HTTPS.

This **disfavors** a simple current host-side WAN-route, disabled-forwarding,
or missing-NAT/firewall-rule explanation. It does not prove that a client
received DHCP, used DNS, sent traffic through NAT, or received Internet
responses. It therefore does not fix or disprove the reported phone problem.

## Source and deployment context

At inspected source heads Goldragon `dc57e801`, CriomOS `6485b64e`, and
CriomOS-home `0025894f`, the Prometheus record in Goldragon
`proposal.datom` declares a router with WAN `eno1`, WLAN `wlp195s0`, 2.4 GHz
channel 6, WiFi4, MX regulatory country, and a WPA3 secret reference.

CriomOS `modules/nixos/router/default.nix` derives the intended path:
`br-lan`/`10.18.0.1`, hostapd WPA3-SAE bridged to `br-lan`, Kea leases with
router/DNS option `10.18.0.1`, dnsmasq DNS, IPv4 forwarding, nftables
`br-lan → WAN` policy with stateful return traffic, and WAN masquerade. Its
networkd `10-wan` DHCPv4 configuration follows the declared WAN.

The same module declares `router-wan-lease-recovery`: after two minutes and
then every two minutes it acts only if the declared WAN has carrier but lacks
an IPv4 default route, calling `networkctl reconfigure` for that WAN only.
See `modules/nixos/router/wan-lease-recovery.sh` and
`checks/router-wan-recovery/default.nix`.

These source observations do not prove that the present host generation came
from those heads. The live witness above independently establishes the main
runtime path elements at its timestamps.

## Relevant history, kept separate

- `flows/753e69/reports/prometheus-phone-wifi-2026-09-21.md` earlier witnessed
  an AP client Internet path and also a roughly 23-minute boot interval before
  the WAN DHCP/default route appeared. Its WAN recovery branch was source-only
  at that time.
- `flows/d8df70/reports/prometheus-recurring-outage.md` records prior whole-host
  freezes attributed from pstore to the MT7925/mt76 AP receive path. It is
  historical evidence, not a fresh driver diagnosis. Current router source
  contains panic-reboot/watchdog settings, but deployment parity was not
  established here.
- Historical reports of low transmitted power, authentication failure, and
  unidentified stations do not identify the present phone and do not justify a
  power or hostapd change from this witness.

## Remaining unknowns and next safe witness

The decisive missing evidence is one **natural, identified phone connection**:
its randomized Wi-Fi MAC or displayed lease, local time, and failure stage
(visibility, WPA, DHCP, DNS, or Internet). Correlate it with bounded hostapd,
Kea, dnsmasq, and firewall/NAT counter reads at the same time.

Until that occurs, do not restart hostapd/dnsmasq/Kea, adjust radio power,
change firewall/NAT, reconfigure the WAN, or activate a new generation. The
smallest reversible host-side action, if a later witness specifically finds
`eno1` carrier with no IPv4 default, is the already-declared WAN recovery
oneshot, which reconfigures only `eno1`; capture route/service state before
and after. Its blast radius is that interface's DHCP lease and routes; it does
not itself restart AP, LAN DHCP, DNS, or networkd.
