# Ouranos Lojix self-upgrade execution

## Outcome

Stopped before the Evaluate gate. No self-upgrade deployment was admitted or
run.

The required `(ssh-ng://root@ouranos.goldragon.criome
root@ouranos.goldragon.criome)` route reached the host `ouranos`, passed strict
known-host verification, and Nix reported the ssh-ng store as trusted. The
controller was still Lojix 0.17.5 and healthy enough to answer the ordinary
node query. However, that query has two unrelated nonterminal CompleteHost
`ActivateNow` records, IDs 5 and 7, both at `Copying`; their state markers are
`(62 62)` and `(98 98)`. The durable re-query retained them and returned marker
`(687 687)`.

This fails the brief's no-unrelated-active-job precondition. The live schema
could also not be independently inspected because the active daemon owns the
store lock. No Evaluate, Realize, ActivateNow, TestActivation, reset, reboot,
hot fix, user-environment deployment, garbage collection, or failed-stage
retry occurred.

## Live state at stop

The persistent and runtime system links match one another at the previous
Ouranos closure. Lojix remained `active (running)` with `NRestarts=0`, and SSH
continuity held after the probes. The boot default and current boot entry were
already different entries, and `complex-init.service` plus
`home-manager-li.service` were already failed; neither was changed by this
work.

The requested candidate source and the explicit new builder posture
`Some.@/etc/nix/machines` were not submitted. This brief supersedes the older
planning witness's historical `None` builder only for a future authorized
attempt; it did not need to be exercised because the gate stopped first.

## Coordination

Before writing these flow records, the prescribed Orchestrate lane and path
claim commands were attempted. The installed clients rejected the documented
parenthesized shapes because their current contracts require brace products;
the updated exact invocation is not documented in the applicable skill.
Therefore no lane or claim was registered. This is advisory coordination
failure only; the report avoids asserting exclusive ownership.

## Sources

- [preflight witness](../witnesses/ouranosLojixSelfUpgradePreflight.md)
- [self-upgrade plan](lojixSelfUpgrade.md)
- [self-upgrade mechanism witness](../witnesses/lojixSelfUpgrade.md)
- [timeout-removal source closure](lojixTimeoutRemovalImplementation.md)
- [written psyche record](../vision/zeusUpdate.md)
