# Prometheus Wi-Fi: evidence brief for Psyche Sonnet

**Observation:** 2026-09-21 15:39 Mexico City time (21:39 UTC). **Mode:** read-only SSH to Prometheus. **Presentation owner:** Psyche Sonnet. No network service, radio setting, or guest was changed.

## Finding

The access point is operating, and the suspected failure is **not a demonstrated general Wi-Fi outage**. An unidentified device that failed to acknowledge authentication responses earlier today later completed WPA authentication twice and received DHCP acknowledgments. At the current read it was still associated, although the host's neighbor entry for its offered address had failed. Prometheus itself resolved DNS and fetched an HTTPS page through its wired uplink. None of those observations identifies the device as the living's phone or proves that phone-to-Internet traffic works. The failure stage for the phone remains unconfirmed.

```text
Phone (identity unconfirmed)
   │  Wi-Fi: association → WPA → data
   ▼
Prometheus AP (wlp195s0, channel 6, 2.4 GHz)
   │
   ▼
br-lan 10.18.0.1/24 ── Kea DHCP, dnsmasq DNS
   │  routing/NAT from a client: not yet witnessed
   ▼
eno1 10.44.0.148 → Ouranos 10.44.0.1 → Internet
                       Prometheus host HTTPS: passed
```

## What happened

All times below are Prometheus local time (UTC−06:00). The first event and earlier power reading come from the prior Field observation; later events were checked in current hostapd/Kea logs. Station identity is deliberately omitted because it has not been tied to the phone.

| Time | Observation | What it establishes |
| --- | --- | --- |
| 13:25 | An unidentified station did not acknowledge several Wi-Fi authentication responses. | A radio/authentication-stage failure occurred then; it does not establish that the phone was involved. |
| 14:42 | Kea sent that station a DHCP acknowledgment for `10.18.0.100`. | DHCP server issued a lease; client use of it remains unproven. |
| 15:17 | The same station associated, completed the WPA four-way handshake, and Kea sent another acknowledgment. | This station passed Wi-Fi security and reached DHCP at least once. |
| 15:22 | It disconnected for inactivity about five minutes later. | Disconnect observed; cause of inactivity is unknown. |
| 15:36 | It again associated, completed WPA, and Kea sent a DHCP acknowledgment. | The earlier authentication failure was not persistent for this station. |
| 15:39 | Hostapd still showed that station authorized at about −63 dBm, with packet counters. Its `10.18.0.100` neighbor entry was `FAILED`. Two other stations were associated with active traffic. | AP is serving clients. `FAILED` means the host did not recently resolve that IPv4 neighbor; it does not alone prove the device has no Internet. |

## Current evidence and limits

| Question | Observed result | Confidence and boundary |
| --- | --- | --- |
| Is the AP up? | `hostapd` active since 12:05; radio and bridge up; hostapd status `ENABLED`, channel 6, three authorized stations at 15:39. | High for current AP operation; coverage at the phone's location unknown. |
| Is DHCP/DNS configured and listening? | Kea alone owns UDP/67; dnsmasq owns DNS/53 on `10.18.0.1`; both active since 12:05. Kea sent fresh acknowledgments. | High for server availability; an ACK does not prove a client applied its lease. |
| Does Prometheus have Internet? | Default route uses wired `eno1` via `10.44.0.1`; host DNS resolution and HTTPS request returned HTTP 200. | High for the host only; client forwarding/NAT and phone Internet have not been tested end to end. |
| Is Wi-Fi transmit power the cause? | Prior Field read measured 3 dBm while the channel/regulatory ceiling was 20 dBm. Current hostapd reported a 20 dBm maximum, but this check did not remeasure actual transmitted power. | Low as a causal claim. Low power may affect range, but later WPA/DHCP success weakens a persistent radio-failure explanation. No setting was changed. |
| Is the station the living's phone? | No confirmed phone MAC, IP, retry time, or on-phone error was supplied. | Unknown. Do not label the station as the phone. |
| Did the driver fail? | Boot log shows `mt7925e` firmware loaded and bridge forwarding at 12:05; the bounded current kernel log showed no later Wi-Fi driver error. | No observed driver failure in this window; absence of a log is not a health proof. |

The living's reported experience was that the phone seemed to obtain an IP address, then disconnected and had no Internet. That report is compatible with several stages: unstable association, client lease/application, local DNS, forwarding/NAT, or client-side captive-network assessment. Host data now rules out only a total AP outage and a total Prometheus upstream outage. It does not select one of those remaining causes.

## Next discriminating test

**First correlate the phone with one station, without changing the AP.** The smallest useful input is the phone's displayed address or randomized Wi-Fi MAC for this SSID, or the exact time and on-phone error from its next *ordinary* connection attempt. Field can then compare that single client's hostapd handshake, Kea lease, neighbor/traffic, DNS, and forwarding evidence. There is no need to ask for a forced retry yet: a current lease/address shown on the phone may already establish the identity. If the matched phone passes WPA and DHCP but still lacks Internet, inspect client-specific DNS and forwarding/NAT; if it fails before WPA, investigate radio range and the measured 3 dBm setting. Do not adjust transmit power solely from the historical reading.

## Sources

- Living's recorded report: `flows/753e69/vision/prometheusWifiReliability.md`.
- Prior Field diagnosis and power measurement: `flows/9ddcbc/reports/field-continuation-prometheus-wifi-2026-09-21.md`.
- Read-only Prometheus SSH on 2026-09-21 at 15:37–15:39 local: `hostapd_cli status`/`all_sta`, bounded `journalctl -u hostapd -u kea-dhcp4-server`, `systemctl show`, `ss`, `ip addr/route/neigh`, `getent ahostsv4`, `curl -4` to `https://example.com/`, and bounded kernel journal. Raw station identifiers are retained only in host logs, not this presentation brief.
