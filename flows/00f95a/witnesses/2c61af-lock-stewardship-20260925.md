# Stale lock 3830 stewardship witness

Captured 2026-09-25 before releasing Orchestrate lock 3830, under the
living's stale-lock authority relayed by Psyche High 38de5b and delegated to
Mind coordinator 00f95a.

The lock was:

```
3830 MindMediumFlowDeliveryGlue2c61af 2c61af
/home/li/wt/github.com/LiGoldragon/flow/mind-medium-delivery-2c61af/crates/flow-nexus/src/lib.rs
```

The owner was stale in HM (`flow-2c61af`); there was no matching Herdr pane or
process, and direct intercom delivery returned `Session not found`. The dirty
file was `crates/flow-nexus/src/lib.rs`, last modified
2026-09-22T08:51:53-06:00. The checkout's current change was
`4660aa0bbb14` (`Propose namespaced tester skill selection metadata`), with
parent `5afb64f2cdcc` (`Select authored testing skill for tester alias with
exact cardinality`).

No source was changed by this capture. The next action is an explicit
Orchestrate release followed by a new exact-path lock; this witness makes the
dirty dispatch state and lineage recoverable before that transfer.
