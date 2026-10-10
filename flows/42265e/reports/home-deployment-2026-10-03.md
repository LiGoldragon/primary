# Home deployment evidence — 2026-10-03

## Pre-switch rollback anchor

- Active Home Manager profile: `/home/li/.local/state/nix/profiles/home-manager-1039-link`.
- The `home-manager` profile resolved to that same immutable generation when
  observed on 2026-10-03.
- Protected rollback activation path: `/home/li/.local/state/nix/profiles/home-manager-1039-link/activate`.
- Rollback command (only if the authorized switch demonstrably fails):
  `rollback_generation=/home/li/.local/state/nix/profiles/home-manager-1039-link; "$rollback_generation/activate"`.

## Initial deployment witness

- Orchestrate `Observe.Locks` returned an empty lock set before work began.
- The requested source revision is local commit
  `9497e4fb249004cd53c14fa97c981830e26a5a3b` on
  `f1c841-regular` in the canonical CriomOS-home checkout.
- The active regular Flow unit was still executing Flow 0.12.2 through its
  user-unit override; the declared regular unit referenced Flow 0.14.
- A next Flow and next Message pair were already active.  The requested
  f1c841 regular/next tuple still needs a coherent source derivation and a
  remote-builder activation witness.

## Source and evaluation boundary

- `9497e4fb249004cd53c14fa97c981830e26a5a3b` already contains the two
  requested predecessor changes: `61abe3fb` supplies Orchestrate 0.37 and
  `4b863bb5` supplies the Flow 0.23 / Message 0.19 stable-and-next inputs.
  Its own explicit policy leaves the next slot off.
- Candidate `91a6640ce06dc27a03a0399cb638768b892c7e6f` has that revision as
  its only parent and changes only `flow-message.nix`, enabling the already
  staged next pair for `li` while retaining the authored separate anchors.
- Generation 1040 exists but is not the active profile generation and resolves
  to a different immutable generation than 1039.  It has not been treated as
  a rollback or activation witness.
- The configured remote builder is the sole Prometheus entry in
  `/etc/nix/machines`.  A direct Home check is intentionally rejected because
  the Home flake has no OS `system` input.  A clean CriomOS consumer projection
  with a transient candidate override reaches the next intended boundary: it
  rejects the missing Lojix-materialized `horizon` input.  No local fallback
  build occurred.
- The running Lojix Nexus exposes `/run/lojix/ordinary.sock` and
  `/run/lojix/meta.sock`.  The supported activation route is a typed
  UserEnvironment request against an immutable CriomOS consumer revision that
  pins the reviewed Home candidate; neither source revision is yet published.

## Pre-switch seat and socket witness

- The regular Flow client reached its ordinary socket and listed 26 stored
  records.  This is process-and-socket availability, not a delivery witness.
- The Next Flow client reached its ordinary socket and listed five records:
  `93ba9f`, `b7ba00`, `c56100`, `dc53b4` (already `Exited`), and `e167d8`.
  The four non-exited entries require targeted post-switch message and lock
  witnesses through their current owners; none will be woken or replaced for
  this deployment.
- `flow-nexus`, `flow-nexus-next`, `message-nexus-next`, and
  `orchestrate-nexus` were active, and their tested ordinary/meta socket paths
  existed.  `message-nexus` regular was not active or declared by the current
  profile, which is the concrete regular-pair deployment gap.
