# Prometheus uplink and AP reliability: bounded rounds

Owner: Field `6db4fe` network runtime lane. Times below are 2026-09-21/22, Mexico City UTC−06:00. The `microvm@vm-testing` guest remains stopped under separate lock `4373`. No network configuration, service, profile, radio power, source pin, or VM was changed in Round 1. Private client identifiers and credentials are omitted.

```text
Internet ── Ouranos built-in Ethernet (working host route)
                 │
                 ├─ Ouranos USB ASIX/cdc_ncm 10.44.0.1/24
                 │       └─ Prometheus built-in eno1 (last proven 10.44.0.148)
                 │                ├─ Prometheus AP/bridge 10.18.0.1/24
                 │                │       └─ Ouranos/Zeus Wi-Fi clients (current reachability unproved)
                 │                └─ Prometheus USB bridge port → Zeus Ethernet (last proven)
                 └─ Ouranos Wi-Fi saved to Prometheus AP (currently disconnected)
Yggdrasil names are separate management routes, not proof of either Ethernet hop.
```

## Round 1 — distinguish current reachability and radio state

**Hypothesis.** The Mentci builder stall and living's AP complaint may share a Prometheus reachability loss. Test configured Ygg, previously proven USB and Wi-Fi paths once each; compare Ouranos NM/kernel with the prior successful chain. Do not infer peer power or cable state from a failed ping alone.

**Observed.** At 16:30–16:32 on Sep 21, configured Prometheus Ygg SSH timed out; its previously leased USB IP did not answer ARP (`INCOMPLETE`, strict-key SSH returned `No route to host`). Its known AP management IP also did not answer ARP even while Ouranos NM briefly claimed its saved SSID connected. The Prometheus binary cache timed out, while the public cache returned HTTP 200. At about 18:20–18:21, Ouranos's built-in Ethernet remained the Internet uplink and its exact USB ASIX interface was `UP,LOWER_UP` with `10.44.0.1/24`; shared NM profile remained selected. The USB lease file was zero bytes with last modification 17:08, and RX counters had not advanced from the earlier 16:30 sample, while TX advanced. USB carrier is therefore local link evidence, not evidence of current Prometheus IP service. A fresh scan from **Ouranos's disconnected client radio** did not list the saved Prometheus SSID; no Prometheus AP radio was scanned or reset.

Ouranos NM shows the Wi-Fi profile disconnected. Its journal has repeated automatic association timeouts between 17:00 and 18:11; kernel lines show authentication attempts followed by connection loss before completion. The saved profile names the expected SSID and autoconnects, so another manual reconnect would duplicate ongoing automatic attempts. One configured Zeus Ygg SSH also timed out. A one-shot request toward Zeus's previously observed AP address routed over Ouranos's built-in Internet after Ouranos Wi-Fi dropped; that attempt **does not** test Zeus Wi-Fi. The living's statement that Zeus Wi-Fi works is recorded as their report, not verified by this host.

**Conclusion/limit.** Prometheus is not currently reachable through any witnessed route from Ouranos. The immediate fault may be Prometheus power/OS, AP/radio/bridge, USB peer interface, cable, or a shared upstream dependency; these observations do not select one. The fresh Ouranos scan and authentication timeouts support a currently missing/unresponsive Prometheus AP from this vantage point, not the cause. No peer kernel, driver, regulatory, route, firewall, NAT, or DNS state can be claimed fresh until a peer route or console witness exists. No extra reconnect, SSH retry, or network mutation followed the failed distinct paths.

**Next discriminating evidence.** Use an already-working Zeus management route or Prometheus console/physical observation to establish each peer's uptime, carrier, AP/bridge/hostapd state, and current default route. A changed peer-state witness permits one strict-host-key read over the restored exact route. Do not alter Ouranos's known working wired default or deploy a new network controller to compensate for an unidentified peer failure.

## Round 2 — local kernel, USB hardware, and ownership audit

**Hypothesis.** An Ouranos USB driver reset, lost physical link, or competing local network owner may explain why Prometheus stopped responding. Inspect the installed kernel and device state without cycling the link. Compare the operational bridge with the authored candidate; do not equate a source branch with the running NixOS generation.

**Observed at 18:21–18:23 local.** Ouranos runs kernel `7.1.8` from its installed August generation. The exact USB adapter is ASIX `0b95:1790` on USB bus 004 port 001 at 5 Gbit/s bus speed, bound to `cdc_ncm`; its Ethernet PHY reports carrier 1 and 1000 Mbit/s. It has zero reported RX errors/drops and no new RX packets since the 16:30 snapshot, despite additional TX packets. No USB disconnect/reset or `cdc_ncm` error appeared in the bounded kernel window since 17:00. This supports a physically present local adapter and link indication while the peer is silent; it does **not** prove that Prometheus is powered, its OS is running, or the cable/peer NIC is healthy end to end. Ouranos client Wi-Fi uses `iwlwifi`; the bounded log showed repeated authentication loss, not a firmware crash/reset signature. Nothing here supports a kernel regression or hardware defect claim.

The saved operational NM share still has UUID `92eb01d2-…`, exact USB interface, `shared` IPv4 at `10.44.0.1/24`, autoconnect priority 200, and `never-default=yes`. NM and `firewall.service` are active; the installed firewall unit still includes the field USB script after start and reload. A previous reload completed successfully. This read did **not** inspect live iptables rules because this user lacks privilege, so duplicate-rule count and present NAT are carried as unverified in this round. The NM profile is the only observed selected USB profile; no second live controller was started.

**Source comparison.** The source-only CriomOS `9842f51a` module already expresses exact interface/MAC/uplink matching, high-priority shared NM autoconnect, disabled NM firewall backend, and one NixOS iptables NAT/filter owner. Its focused check covers absent/duplicate/invalid services and ownership conflicts. These are useful fail-closed declarations; no specific defect demanding a new hostname or hotplug hook is established by the current outage. The source is not in CriomOS main or the installed Ouranos generation. Horizon USB producer and Signal Lojix/meta producer pins have moved, but Lojix main still points to older Horizon/Signal/meta, Goldragon USB data and this CriomOS consumer are not main, and no current materialized JSON/configuration has been witnessed. Sol owns that graph/integration lane. A source-only test that simply repeats `autoconnect=true` would not prove actual unplug/replug behavior, so no mirror test or source mutation was made.

**Next bounded action.** Obtain a Prometheus/Zeus peer or console witness; if Prometheus is alive, read its `eno1` carrier/address/networkd, AP hostapd/bridge, USB port and kernel logs before selecting any reversible per-interface action. If the peer is not alive, its power/console state must be resolved before changing Ouranos's already functioning wired/default and USB share. Separately, Sol must supply coherent materialized producer-to-CriomOS pins before a remote build, same-UUID profile migration, or declarative activation. No kernel upgrade, link bounce, radio reset, or service restart is justified yet.

## Existing, temporary, and candidate configuration

| Grade | State |
| --- | --- |
| Installed on Ouranos | NixOS generation `nixos-system-ouranos-26.11.20260813.0e251e2`, kernel `7.1.8`; built-in wired remains upstream. The USB ASIX AX88179A uses `cdc_ncm`; Ouranos Wi-Fi uses `iwlwifi`. These are live host facts, not a new deployment. |
| Operational bridge | Saved `prometheus-share-temporary` NetworkManager shared profile serves the exact ASIX USB interface. A scoped `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf` runs `/etc/systemd/field-prometheus-usb-firewall.sh` after firewall start/reload. Prior rounds proved the full Ouranos → Prometheus → Zeus path and the configured SSH builder once; current peer reachability has regressed. The bridge is operational state, not accepted declarative CriomOS deployment. |
| Authored candidate, not installed | CriomOS branch `usb-gateway-consumer-6db4fe` at `9842f51a` has `modules/nixos/network/usb-ipv4-gateway.nix` and focused checks. It consumes the accepted `NodeService::UsbIpv4Gateway` fields, pins downstream interface/MAC and explicit uplink, declares a single NM shared profile, disables NM's firewall backend, and scopes NixOS iptables DHCP/DNS/forward/NAT rules. It rejects duplicate service and NM/networkd/generic-NAT ownership conflicts. Its source grade does not prove the current materialized Horizon/Lojix/Goldragon graph, main merge, system generation, hotplug, or migration. |
| Critical activation gap | The saved `/etc` NM profile and future generated `/run` profile use the same UUID; coexistence/replacement must be proved under checkpoint. Existing operational firewall drop-in must be compared and retired only when the declarative owner is active and verified, to avoid duplicate rules. Unplug/replug, boot, uplink-down behavior, and exact no-Wi-Fi-escape remain untested. The unrelated generic `networkd` hotplug `10.47.0/24` service is not this USB gateway. |

## Later bounded rounds (not yet run)

1. On a verified peer/console route, compare Prometheus and Zeus live interfaces, carrier, kernel/firmware errors, AP hostapd, regulatory/power/channel, DHCP/DNS/NAT, and exact Internet egress. Record before/after and rollback for any smallest reversible repair. Do not treat the living's phone as an unidentified station without identity evidence.
2. Have Sol's current source/integration owner supply the coherent materialized `UsbIpv4Gateway` producer → Lojix → Goldragon → CriomOS pins and exact locks. Test candidate source remotely with fallback disabled; inspect a proposed generation for unrelated changes before activation. No parallel source merge or new hostname hook.
3. Only after runtime route stability and source parity, checkpoint same-UUID NM profile migration and sole firewall ownership. Boundedly verify USB disappear/reappear, wrong-MAC refusal, no uplink/Wi-Fi NAT escape, one DHCP/DNS listener, unique scoped firewall rules after reload, and working peer route. Record exact rollback. No reboot or broad radio reset is part of these rounds.

## Sources

- Living's current network reliability request as relayed by Field High; prior chain receipts `flows/6db4fe/reports/network-chain-attempts.md` and `flows/6db4fe/reports/network-durable-source.md`.
- Rounds 1–2 read-only Ouranos `nmcli`, `ip` route/address/neigh/link counters, NM and kernel journal, NixOS generation, sysfs driver/carrier/speed, `lsusb -t`, installed firewall unit, and bounded known strict-host-key SSH attempts to Prometheus/Zeus at 16:30–18:23 local. Privileged live iptables read was unavailable and is not claimed.
- Source-only CriomOS `usb-gateway-consumer-6db4fe` revision `9842f51a`, exact module and check; installed operational bridge paths named above. No generated or installed projection acceptance is inferred.
