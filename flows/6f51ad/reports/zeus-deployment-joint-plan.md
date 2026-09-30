# Zeus deployment reconciliation for joint planning

Evidence cut: 2026-09-30. This is a root-review draft for the restored Zeus deployment plan. It does not authorize a build, transfer, switch, network change, observer action, or reuse of an Ouranos artifact.

## What the record already settles

The original Zeus system update is complete in two Field-reported stages.

| Stage | Declared source and built artifact | Target-side result |
|---|---|---|
| System update | CriomOS `1a9f5fdf89af4ec38015824fca2fe36847f2f4db`; Prometheus built `/nix/store/wk4qr8cf2bkjszrb86jp076caif15jpn-nixos-system-zeus-26.11.20260813.0e251e2` from `/nix/store/qn67ny8mixnnazdyf3wjjv92lgshgf69-nixos-system-zeus-26.11.20260813.0e251e2.drv`. | Field copied through the signed HTTP cache, armed and later cancelled the rollback guard, and reported runtime and system profile at `wk4`. The first system switch exposed the separate Home adoption failure. |
| Durable Zeus Home repair | CriomOS `2ad31624d61b2c5f06a1e9c472b2bd1a94ecd8ec` with Home `35a6d75a4e2121882f0629ceba90402bef4732af`. | Field reported runtime and system profile at `/nix/store/4yk8xdcn9rp8q9jrcr0161bil8yq2v2b-nixos-system-zeus-26.11.20260813.0e251e2`; corrected li and bird generation links are `gl6mxgihdlf4d90gpdij9fdb0kz80mlw` and `w50gyx5c5da3nj1f87rbd22x8vxz3w6k`. Both first activations and one ordinary restart each exited zero without resetting state. |

The durable repair report also records strict SSH/network success, a guard cancelled only after repeat witnesses, and no rollback. It does not claim that every unrelated service or live Herdr-seat behavior was accepted. Separate user Home profiles remained old because of driver-version-1 behavior and were intentionally not rewritten.

The completed `wk4` and `4yk` stages are not pending work to redeploy. The `gl6` and `w50` links are completed target-specific Home generations, not generic inputs for an Ouranos update.

## Deployment item closed

Fable’s answer is that no further Zeus system change is requested. The system update and both Home repairs are complete, and current contact has been verified at its observation point. `wk4`, `4yk`, `gl6`, and `w50` are completed target artifacts, not work to repeat.

The corrected passive USB observer and current physical-link investigation belong to Ouranos reliability. The observer’s lasting delivery remains part of the ordinary reviewed Ouranos composition repair; a transient witness is a separate, runtime-only observation and is not a Zeus deployment artifact. The latest Ouranos rotation and held Codex succession likewise do not enter Zeus scope.

No Zeus source build, closure transfer, target switch, or rollback plan is pending. A later Zeus deployment would require a new living-declared behavior and exact source projection; none is presently declared.

## Contact and reliability qualification

The parent reports that contact has been restored. That supports a fresh current-contact observation at the time it was made; it does not repair the historical continuity gap.

A separate earlier Zeus-side recovery sequence is recorded before the later outage: at 15:46:45 the Zeus kernel reported an xHCI resume error and reinitialization; at 15:48:54 its wired NIC reported 1 Gbps carrier; at 15:48:56 charon reported `10.44.0.10` appearing on that NIC. These are time-bounded physical/network-stage facts, not a causal explanation of either the earlier interruption or the later 17:01–21:07 outage.

Field’s cross-host journal correlation now corroborates the physical-stage sequence. On Sep 29, Ouranos networkd recorded `enp0s20f0u1c2` losing carrier at 17:01:17-06, aligning with Zeus `enp0s31f6` NICLinkDown at 17:01:17.851411; Zeus’s `10.44.0.10` charon peer then disappeared at 17:01:23.856299. At recovery, Ouranos recorded gain at 21:07:10, loss at 21:07:11, and gain at 21:07:14, aligning with Zeus’s brief 10 Mbps half-duplex rise, immediate fall, then 1 Gbps full-duplex carrier at 21:07:13.956734. Field’s summary reports Kea allocating Zeus MAC `90:2e:16:47:ea:e3` lease `10.44.0.10` at 21:07:15.990, followed by Yggdrasil events on both hosts at 21:07:16. This is cross-host corroboration of roughly four hours of carrier outage and automatic DHCP/Yggdrasil recovery after carrier. The Kea detail is a Field summary, not quoted journal text. The physical cause remains unknown. Overnight continuity remains unknown: later SSH and the 15:48 DHCP lease cannot establish continuous contact, and uptime only shows no reboot. Preserve both the outage and the unknown interval rather than overwriting them with a restored-contact fact.

## Physical reliability remains open

The link account establishes two outages and automatic post-carrier address/overlay recovery. It does not isolate a cable, adapter, port, PHY, power, or negotiation cause. The xHCI resume message is temporally coincident with the first recovery sequence, not causal proof.

The earlier bounded watch ended around 15:35 and did not cover the later four-hour outage. A future watch must name its interval and, if it ends before recovery is established, schedule a follow-up or explicitly notify that current reachability is unknown. No network change is proposed by this account.

## Sources

- `flows/6f51ad/log.md`, sections “Zeus system build succeeded,” “Zeus new system witnessed by Field,” and “Durable Zeus Home repair completed”; published main record, read 2026-09-30.
- `flows/1bc255/log.md`, entries 15–18 and 22–32: Field’s R/P/BaseHost and downstream observations; read 2026-09-30.
- `flows/b666e7/reports/zeus-topology-mind-2026-09-29.md`: explicit topology and evidence-boundary synthesis; read 2026-09-30.
- `flows/b666e7/reports/zeus-link-liveness-account-2026-09-30.md` at immutable `1939ce6f68ff`, dated 2026-09-30: completed cross-host link-liveness account and watch-boundary lesson.
- `flows/b666e7/reports/ouranos-composition-reconciliation.md` at immutable revision `449810994e68`: prior joint-composition distinctions; read 2026-09-30.
- `flows/6f51ad/vision/zeus.md` and `flows/8904b1/vision/anatomy.md`: standing update and downstream-provider intent; read 2026-09-30.
