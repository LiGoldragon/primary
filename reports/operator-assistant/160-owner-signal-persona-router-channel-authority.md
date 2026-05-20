# Owner Signal Persona Router Channel Authority

## What changed

Created `owner-signal-persona-router` as the router policy signal for
channel authority orders. It is a `signal-frame` contract repo with:

- `Grant(ChannelGrant)`
- `Extend(ChannelExtension)`
- `Revoke(ChannelRevocation)`
- `Deny(AdjudicationDenial)`

The contract also carries the replies, rejection reasons,
`OperationKind`, and a witness that owner-order names are not
`ChannelMessageKind` values.

Updated `signal-persona-mind` so the Mind working contract no longer
declares the moved authority orders:

- removed `ChannelGrant`
- removed `ChannelExtend`
- removed `ChannelRetract`
- removed `AdjudicationDeny`
- removed `ChannelReceipt`
- removed `AdjudicationDenyReceipt`

Mind still carries Router-to-Mind `AdjudicationRequest` and the
read-side `ChannelList` / `ChannelListView` shape.

Updated `signal-persona-router` documentation to point router
channel-policy writes at `owner-signal-persona-router` and keep the
ordinary router contract as the observation surface.

## Verification

Passed:

- `/git/github.com/LiGoldragon/owner-signal-persona-router`: `cargo fmt --check`
- `/git/github.com/LiGoldragon/owner-signal-persona-router`: `cargo test`
- `/git/github.com/LiGoldragon/owner-signal-persona-router`: `nix flake check --max-jobs 0`
- `/git/github.com/LiGoldragon/signal-persona-mind`: `cargo fmt --check`
- `/git/github.com/LiGoldragon/signal-persona-mind`: `cargo test`
- `/git/github.com/LiGoldragon/signal-persona-mind`: `nix flake check --max-jobs 0`

## Questions

1. Should `ChannelList` remain in `signal-persona-mind` as a temporary
   Mind-side read, or should channel views move fully to
   `signal-persona-router` / `owner-signal-persona-router` now that
   Router owns grant state?
2. Does Mind call the Router owner socket directly, or should Mind
   issue an order to Orchestrate and let Orchestrate call
   `owner-signal-persona-router` as Router's immediate owner?
3. Should `AdjudicationRequest` stay as Router calling Mind's working
   signal, or should it become a router observation/tap event once the
   mandatory persona observable surface lands?

