# Mind book source provenance

This appendix supports `mind-book.html`; it is for review and integration. No secret material is included.

- Superseding composition artifact: Primary `449810994e68`, bookmark `push-mrrtvqrzpxoy`, `flows/b666e7/reports/ouranos-composition-reconciliation.md`, 2026-09-29. It supersedes `330c04218841`. Its 18:05–18:06 cable observation originates with Field Sol `1bc255`; relays through Mind and Field are the same witness, not independent confirmation.
- Field source: `flows/d5b96b/reports/observer-deployment-handoff.md`, 2026-09-29. It supplies R/P distinction, BaseHost limits, dry-activation/residue corrections, transient-witness boundary, and the 18:04 transient procedure blocker.
- Current local record: `flows/6f51ad/log.md`, 2026-09-28–30, for Zeus, Home, messenger, Claude and Codex staging context.
- Exact Zeus-side critical lines relayed 2026-09-30, paraphrased here: xHCI resume error/reinitialization at 2026-09-29T15:46:45.798591-06:00; wired NIC carrier at 15:48:54.391684; charon observed `10.44.0.10` at 15:48:56.576894. They establish timing only, not cause.
- Field’s cross-host journal correlation relayed 2026-09-30: Ouranos networkd recorded `enp0s20f0u1c2` carrier loss at 17:01:17-06; Zeus `enp0s31f6` recorded NICLinkDown at 2026-09-29T17:01:17.851411-06:00; Ouranos gain/loss/gain at 21:07:10/11/14 aligns with Zeus’s 10 Mbps rise/fall and 1 Gbps carrier at 21:07:13.956734. Field summarized, rather than verbatim-quoted, Kea allocating Zeus MAC `90:2e:16:47:ea:e3` lease `10.44.0.10` at 21:07:15.990; both-host Yggdrasil events followed at 21:07:16. This corroborates the carrier-outage/recovery sequence across hosts, not its physical cause. Overnight reachability remains unobserved.
- Current source inspected: CriomOS `0fe91588d60b642de851dee3f08073082989de2b`, plus stale Agent Intercom consumer removal `76d78172277de82d00bed4c32397d2207ef6eec9`.

## Source findings used

- CriomOS gates Home Manager and `userHomes.nix` through `deployment.includeHome`; BaseHost Home omission is expected.
- `userHomes.nix` selects projected node-local users and applies the Home default module.
- The current Home default declares stable Codex remote control for Min+ users and imports the Next module. This requires an exact target unit-delta review; it does not prove automatic Codex promotion.
- The observer is a passive service after networkd/Kea, constrained to local Unix/NETLINK use with no network ownership.

## Boundaries

Observer test success is not deployment. R, P, L, and C are distinct. The dry residue proves runtime metadata writes, not any secret-content claim. The Codex catalog statement is scoped to the authenticated catalog query used here.
