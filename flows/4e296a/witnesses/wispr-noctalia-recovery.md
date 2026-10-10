# Wispr/Noctalia recovery witness

## Method

I used read-only repository inspection (`jj log`, `jj show`, `jj git fetch`,
and source reads), typed ordinary Lojix queries, process/socket/configuration
inspection, one passive status-socket snapshot, and `niri msg -j windows`.
I did not run a recorder, invoke a hands-free control, restart a service, or
activate a deployment.

## Repository observations

- The producer product revision is `5e6156aa235fa17d6a3e34d1c97ad1d3f6999b9a`;
  its commit changes the Linux status-bridge patch and its executable
  verification tests.
- Home revision `8021ae5d4428343624920330098641f772c9eece` pins that producer
  revision. OS revision `840ed01d1c73bb373fd694a49cca9d3007014f8b` pins that
  Home revision.
- The producer remote-main query returned `5e6156aa…` at observation time.
  This is a source revision observation, not a claim that it can never gain a
  later Beads-only descendant.

## Test observations and claims

- The producer contains the recovery verification surface, but I did not run
  it in this final state.
- **Historical claim:** the provider implementation subflow reported 41
  failing executable tests before the fix, then 44 passing tests and an
  independent immutable-remote check. The preserving source is
  `flows/4e296a/log.md`; this witness does not independently verify the past
  red/green result.
- **Historical claim:** the target and Home activation outputs built remotely;
  the official OS check attributes stopped before derivation due to the
  unrelated eager MS2130 policy. The source code confirms the eager MS2130
  assertion shape, but this witness did not rerun those remote outputs.

## Deployment observations

- Typed Lojix records show 188 (`Realize`) and 189 (`ActivateNow`) for
  immutable OS revision `840ed01d…`, both terminal `Succeeded`.
- The current ledger entry for 189 names
  `/nix/store/4idm37b4awlkk1yj3w6j61cn3a0hinih-home-manager-generation`.
- Event positions 661–676 are event-log positions for deployments 184–187;
  the separate 4,8xx values are state markers.

## Live observations

- The Wispr executable path is
  `wispr-flow-1.6.774+criomos.5`; its status/control sockets exist.
- The passive status snapshot said `idle` and `hands_free: false`.
- Noctalia has `wispr-status` enabled and owns a continuing consumer connected
  to the status socket.
- Niri shows only the non-floating `Wispr Flow` window; it shows no `Status`
  window.

## Inference

The current status consumer and absence of the floating `Status` window are
consistent with the recovery's intended idle integration. They do not prove
recording behavior, shortcut behavior, or microphone operation.

## Unknowns

- No recording or hands-free verification was invoked.
- The historical 41-to-44 test transition, immutable remote check, and remote
  output builds remain claims until independently rerun.
