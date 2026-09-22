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
- This round's read-only Ouranos `nmcli`, `ip` route/address/neigh/link counters, NM and kernel journal, NixOS generation and driver reads at 16:30–18:21 local; bounded known strict-host-key SSH attempts to Prometheus/Zeus.
- Source-only CriomOS `usb-gateway-consumer-6db4fe` revision `9842f51a`, exact module and check; installed operational bridge paths named above. No generated or installed projection acceptance is inferred.
