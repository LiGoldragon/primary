# Message recipient-selection source note

## Finding

The inspected canonical Message source processes every member of
`DeliveryRequest.target_flows` and records a receipt for each selected target.
Its generated signal contract defines `TargetFlows` as a generic vector of
`FlowIdentifier`; `MessageRecipient` and `TargetFlowName` are each string
scalars. `ClusterMembers` is also an array, but this inspection establishes no
broadcast authorization from that representation.

No dedicated typed codec expressing the required semantic of exactly one
recipient was found in this bounded source review. The active implementation
scope should therefore require explicit, bounded, single-recipient selection,
record the codec gap, and omit broad or broadcast delivery and status tests.
Use passive status observation and local codec or disposable-recipient tests.

## Boundary and uncertainty

This is source evidence from the canonical `/git` checkouts. It is not proof
that retained writer f72ab7's night candidate is at parity. The task named
Message revision `55657f4`; direct Jujutsu inspection found that revision and
also found canonical working-copy `@` at `f28c8b60002e`, with differences in
`src/engine.rs`, `src/nexus_delivery.rs`, and `flake.nix`. No parity claim is
made.

## Sources

- `/git/github.com/LiGoldragon/message`, revision `55657f4e9071`,
  `src/engine.rs:160-249` and `src/engine.rs:399-403`: per-target loop,
  per-target `RecipientReceipt`, and only a nonempty target-vector check.
- `/git/github.com/LiGoldragon/signal-message`,
  `src/generated/signal.rs:23`, `:484`, `:570`, `:643-650`:
  `MessageRecipient`, `TargetFlowName`, `ClusterMembers`, and `TargetFlows`.
- Retained candidate reference only, not parity evidence:
  `/home/li/wt/github.com/LiGoldragon/message/night-messaging-0ab019`,
  parent revision `8a6e88ff183c`.
