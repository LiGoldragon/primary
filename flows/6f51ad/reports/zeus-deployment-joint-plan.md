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

## Declared versus deployed gap

No later record identifies a new, scoped Zeus desired revision or feature that is absent from `4yk`. The currently active work divides cleanly:

- The corrected passive USB observer package is an **Ouranos runtime-only witness**. It is not a Zeus system artifact and does not justify a Zeus switch.
- The latest Ouranos rotation and Codex succession work belong to Ouranos. They must not enter a Zeus projection by implication.
- The rebuilt observer, contact observations, and the physical downstream path are evidence work. They do not establish a desired Zeus configuration delta.

Accordingly, the current gap is not a missing transfer or unrun old activation. It is a missing declaration of any post-`2ad` Zeus change: source revision, target projection inputs, intended feature/unit delta, and the corresponding exact closure. Without those facts, selecting current main merely because it is newer would redeploy unrelated work and violate the scoped deployment record.

## Contact and reliability qualification

The parent reports that contact has been restored. That supports a fresh current-contact observation at the time it was made; it does not repair the historical continuity gap.

A separate earlier Zeus-side recovery sequence is recorded before the later outage: at 15:46:45 the Zeus kernel reported an xHCI resume error and reinitialization; at 15:48:54 its wired NIC reported 1 Gbps carrier; at 15:48:56 charon reported `10.44.0.10` appearing on that NIC. These are time-bounded physical/network-stage facts, not a causal explanation of either the earlier interruption or the later 17:01–21:07 outage.

Field’s cross-host journal correlation now corroborates the physical-stage sequence. On Sep 29, Ouranos networkd recorded `enp0s20f0u1c2` losing carrier at 17:01:17-06, aligning with Zeus `enp0s31f6` NICLinkDown at 17:01:17.851411; Zeus’s `10.44.0.10` charon peer then disappeared at 17:01:23.856299. At recovery, Ouranos recorded gain at 21:07:10, loss at 21:07:11, and gain at 21:07:14, aligning with Zeus’s brief 10 Mbps half-duplex rise, immediate fall, then 1 Gbps full-duplex carrier at 21:07:13.956734. Field’s summary reports Kea allocating Zeus MAC `90:2e:16:47:ea:e3` lease `10.44.0.10` at 21:07:15.990, followed by Yggdrasil events on both hosts at 21:07:16. This is cross-host corroboration of roughly four hours of carrier outage and automatic DHCP/Yggdrasil recovery after carrier. The Kea detail is a Field summary, not quoted journal text. The physical cause remains unknown. Overnight continuity remains unknown: later SSH and the 15:48 DHCP lease cannot establish continuous contact, and uptime only shows no reboot. Preserve both the outage and the unknown interval rather than overwriting them with a restored-contact fact.

## Proposed source-to-Field handoff when a Zeus change is actually named

1. The source owner records the desired immutable CriomOS revision, exact Goldragon/Horizon/system inputs, and a concise unit or feature delta against deployed `4yk`.
2. The source owner evaluates and realizes exactly that Zeus composition on Prometheus, retaining the resulting system closure and its source binding. A current-source rebuild is not started until step 1 names the intended change.
3. Field Sol `1bc255`, as sole deployment executor, compares the new closure with the deployed `4yk` system and `gl6`/`w50` Home generations, witnesses its signed transfer path, and prepares a rollback guard anchored to the actual currently running/profile identities.
4. Field runs the scoped target deployment only after the delta and recovery plan are reviewable. The acceptance record distinguishes new runtime/profile paths, Home-service result, and current contact from any historical reachability claim.

This retains the deployed repair and keeps a future Zeus change attributable. It does not reuse the earlier BaseHost observer closure, replace target-specific rollback evidence with an Ouranos profile, or include the held Codex activation.

## Decisions still required before another Zeus deployment

- What exact post-`2ad` Zeus behavior is desired now, if any?
- Which immutable source and target materialization express that behavior?
- Does its generated unit delta preserve the repaired li/bird Home services and exclude held Codex/Ouranos-only work?
- What target-proven recovery state will Field restore if the new scoped switch fails?

Until those are answered by a concrete source declaration, Field’s next action is contact/reliability observation under its existing authority, not a speculative Zeus rebuild or deployment.

## Sources

- `flows/6f51ad/log.md`, sections “Zeus system build succeeded,” “Zeus new system witnessed by Field,” and “Durable Zeus Home repair completed”; published main record, read 2026-09-30.
- `flows/1bc255/log.md`, entries 15–18 and 22–32: Field’s R/P/BaseHost and downstream observations; read 2026-09-30.
- `flows/b666e7/reports/zeus-topology-mind-2026-09-29.md`: explicit topology and evidence-boundary synthesis; read 2026-09-30.
- `flows/b666e7/reports/ouranos-composition-reconciliation.md` at immutable revision `449810994e68`: prior joint-composition distinctions; read 2026-09-30.
- `flows/6f51ad/vision/zeus.md` and `flows/8904b1/vision/anatomy.md`: standing update and downstream-provider intent; read 2026-09-30.
