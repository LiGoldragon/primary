# Criome / Lojix / Arca Context Maintenance Handoff

Date: 2026-05-18  
Role: system-specialist  
Status: context preserved before switching to repository-ledger production work

## What Was Preserved

The current Criome / Lojix / Arca context was checked against
`skills/context-maintenance.md` and the designer compendium
`reports/designer/215-workspace-state-of-art-2026-05-18.md`. No new
cross-lane compendium was needed: designer/215 is already the durable
state-of-art artifact. This report records the system-specialist pickup
points that were in chat so the thread can move on without losing them.

## Current Architecture State

The workspace has converged on the component triad pattern:

- runtime component daemon owns durable state through sema-engine;
- thin CLI has exactly one Signal peer, its own daemon;
- typed `signal-*` contract owns request vocabulary and verb mapping;
- privileged authority moves to `owner-signal-*` surfaces;
- daemon-to-daemon composition happens through Signal, not through CLI
  fanout or direct database access.

The active deploy architecture has four cooperating daemons per relevant
node:

- `criome-daemon`: authorization, identities, signatures, quorum, owner
  approval;
- `lojix-daemon`: deployment planning, job state, actors, observations;
- `arca-daemon`: content-addressed artifacts and propagation;
- `nix-daemon`: builds, store import, substituter trust, activation.

Production is still the old `lojix-cli` stack on `main`. The lean rewrite
on `horizon-leaner-shape` reached an end-to-end smoke milestone but is not
deployed. Do not merge the two stacks piecemeal.

## Criome Decisions Captured

The latest user corrections were:

- the regular non-owner `signal-criome` socket is reachable by anyone;
- the regular socket is unencrypted;
- the signature is Criome-owned, not Lojix-owned;
- the signature grants permission to another `criome-daemon` to authorize
  an action in that daemon's environment;
- Lojix deploy approval is likely the first useful owner-approval case;
- owner approval should probably be an asserted signing decision, with the
  daemon mutating pending authorization state after the fact.

The design reports still need reconciliation where older text says the
regular socket is `0660 group criome-peers`.

## Best Open Questions

1. What exactly is the signed Criome permission object?

   Current lean: call it `CriomePermissionGrant`. It signs issuer Criome
   identity, target environment, action scope, canonical request/content
   digest, expiry, replay nonce, policy satisfaction, and signature set.

2. What exactly is `target_environment`?

   It probably needs to name at least cluster, host, Unix user, component,
   and capability scope. Node name alone is too weak.

3. Does Criome receive content bytes, or digest plus Arca reference?

   Verification needs canonical bytes. Large objects should likely move as
   digest plus Arca locator, with Criome fetching and checking the bytes.

4. What is the first owner approval surface?

   Current lean: approve one Lojix deployment plan before any local Nix,
   store, cache, GC-root, or activation effect starts.

5. How does unattended system Criome bootstrap?

   Current lean: v1 unencrypted master key protected by filesystem
   permissions; v2 TPM-sealed key. Mark v1 explicitly as bootstrap debt.

## System-Specialist Implementation Backlog

- Update stale `signal-criome` / Criome architecture text to reflect the
  public unencrypted regular socket.
- Add the real `signal-criome` socket client to Lojix so production-like
  paths fail closed until a grant exists.
- Implement `NixDaemonConfigurationActor`: own a small mutable include file,
  restart lock, last-applied hash, health observations, and lease cleanup.
- Implement Arca's daemon path at `/arca`, not `~/.arca`, with stable daemon
  locators and full BLAKE3 identity.
- Keep Stack A production fixes on `main`; keep Stack B lean rewrite work on
  `horizon-leaner-shape` worktrees until coordinated cutover.

