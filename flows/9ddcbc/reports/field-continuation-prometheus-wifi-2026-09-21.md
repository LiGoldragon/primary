# Field continuation and Prometheus Wi-Fi, 2026-09-21

Owner of this observation: Field Medium `9ddcbc`. The living requested a refreshed Field continuation, a distinct four-power Field role map, Prometheus phone Wi-Fi diagnosis, and durable project/topic continuity. This report is an operational handoff and proposal, not a new Flow identity or a network change.

## Seat and launcher observation

At the bounded HM read, Field High `6db4fe` was working, Field Medium `753e69` was working, and this older Field Medium `9ddcbc` was working. `753e69` has a native identity, read-back title `Field Medium 753e69`, and accepted ongoing work from Field High, as recorded in its log. A third Medium launch would add another claimant to the one Medium cell of the twelve-cell structure. Messages to `753e69` and `6db4fe` were submitted through HM from `9ddcbc`; submission is not a recipient read receipt.

Installed `flow --help` exposes `flow start <predefined-type>`, `flow restart <flow-id>`, and `flow resolve <flow-id>`. The predefined start visible in the current Flow source is generic `codex-medium`; it does not declare the Field Medium role/profile. Direct installed `flow resolve` rejected `9ddcbc`, `753e69`, `6db4fe`, and `03e825` as unknown. Thus this CLI does not currently supply a witnessed route to mint a typed Field Medium successor or transfer the current managed seats. The existing native Field launcher is separate, receipt-first, and requires exact profile, native context, Flow identity, Herdr/HM binding, title, target acceptance, and predecessor continuity. No launch, restart, or reaping occurred here.

Field authority is scoped to its aspect and current seat. `6db4fe` is the observed active High; `753e69` is the newer active Medium. This Medium does not claim to be the highest-powered Field or override the active High. The living's request establishes project priority, while current routes and accepted ownership remain observable gates. Field fixes, debugs, releases, and deploys; Mind knows component structure and viability; Psyche considers design and interacts with the living (`flows/b81560/vision/operational-triadWorkDivision.md`).

## Proposed Field power categories

These are a responsibility list to refine with Field High and Mind, not a claim that all twelve seats or a typed duty policy are deployed. Every power level carries the same Field core: current system state, exact ownership and route evidence, safe lifecycle, and reporting of actual test/deployment grade. The layer adds work suited to its power; it can omit details needed only by another layer.

| Power | Primary categories | Escalation and handoff |
| --- | --- | --- |
| High | Field-wide coordination, conflicting authority, irreversible or broad rollout decisions, cross-aspect integration, architecture-to-deployment acceptance | Delegates bounded investigations and implementation; remains the current highest Field when alive and accepted. |
| Medium | Project coordination, implementation and debugging, bounded rollout planning, native refresh and exact acceptance evidence, integration of lower-power reports | Takes a project through evidence and scoped changes; escalates unresolved authority or broad system risk to High; hands routine monitoring to Low. |
| Low | One-at-a-time lifecycle work, service and route repair, routine deployment operations, exact ghost and gap preflights, targeted host checks | Reports concrete failures or unsafe ambiguity to Medium/High. |
| Ultra Low | Frequent census/checkup, liveness and receipt observation, deduped status notices, inexpensive checks and routing of questions | Wakes or routes only within a typed duty and accepted delivery policy; does not infer reaping or launch from an absent response. |

The tier mapping is a proposed duty map, not an invented numeric workload ratio. `Vision/modelRoles.md` describes power as an energy tier and delegates Luna/Terra/Sol under Astra ceilings; canonical seat titles use explicit power rather than model nickname. A distinct profile may load common Field instructions plus only the modules relevant to that tier. The requested topic/subtopic memory should be a Mind-owned indexed project record: topic ID, subtopic ID, owner Flow and successor chain, state, source/evidence pointers, open decision, next action, and receipt grade. Field writes operational observations and work transitions; Mind owns the knowledge structure and keeps it queryable across refresh.

## Prometheus live read-only evidence

`ssh li@prometheus.goldragon.criome` succeeded over the current route. `hostapd`, `kea-dhcp4-server`, and `dnsmasq` were active. `wlp195s0` was an AP broadcasting `goldragon.criome` on 2.4 GHz channel 6, 20 MHz, with reported transmit power **3.00 dBm**. `br-lan` was up at `10.18.0.1/24`; the Wi-Fi interface was forwarding through that bridge. Two associated clients reported approximately -46 and -57 dBm signal. Kea logged DHCP acknowledgments/renewals for those clients at `10.18.0.108` and `10.18.0.102`. This shows AP association and DHCP worked for those devices, not that the living's phone connected.

At local Prometheus 13:25:25–26, hostapd logged four `did not acknowledge authentication response` events for an unidentified randomized-looking station `5a:47:10:23:ef:12`, followed by inactivity deauthentication at 13:30:25. It is not proven to be the living's phone. Another client repeatedly connected and disconnected around 12:13–12:16 before remaining associated; that is a separate observation. No phone MAC, phone OS, failure text, distance, or current retry witness was available. The low reported transmit power is a plausible range contributor, not a proven root cause. The configured primary security is WPA3-SAE in `CriomOS/modules/nixos/router/default.nix`; the specific phone compatibility is unknown. No service, radio, network, secret, or configuration was changed.

The host's reported `NetworkManager` absence is consistent with this NixOS router design; the AP is managed by hostapd. The older Ouranos report's missing saved SSID concerns an Ouranos-side scan, not proof that Prometheus AP is down. Prometheus itself had its AP live at this observation. The Zeus Speedtest result is not evidence of phone association to this SSID or successful current phone Internet path; the exact route used by Zeus must be attached to any such claim.

## Next bounded sequence

1. Have the current Field Medium `753e69` and Field High `6db4fe` acknowledge exact project/seat ownership and protect `9ddcbc` as a crossover until its Message/Flow consumer deployment scope and this handoff are accepted. Avoid a duplicate Medium start. A later refresh of the current Medium needs a single distinct successor with native, HM, title, readiness, and acceptance receipts before retiring a predecessor.
2. Correlate a fresh phone attempt with hostapd events and station identity, and record whether failure is SSID visibility, authentication, DHCP, or Internet after association. Check actual phone-to-AP distance and the 3 dBm power setting with the network owner. Use a bounded reversible intervention only after the failure stage and current service owner are known.
3. Verify current AP source and runtime parity, then test association, DHCP, DNS, and phone Internet separately. Preserve the working two-client service during diagnosis. Coordinate any declarative/router change with the active Field network owner and ordinary rollout/rollback gates.
4. Ask Mind to hold a durable topic/subtopic entry for this project and the wider Flow refresh/role map, with exact owner, evidence, and pending decisions. Transfer new evidence to the successor's first native context rather than replaying a predecessor transcript.

## Other retained scope

`9ddcbc` holds consumer preparation lock `3776` for five exact CriomOS-home paths and has a source-only branch at `e1096a164b68f3b03ad7777efd344cd1ea4679df`; its rollback plan is published at `f55eb48d4bb1c9880af2b53cf64816eca767d2bf`. Remote builder handshake to Prometheus was restored, but no immutable Flow/Message pair build or runtime activation is inferred. That project remains a separate accepted scope to transfer explicitly before retiring this route. Stable app server, protected locks, records, and existing routes remain preserved.
