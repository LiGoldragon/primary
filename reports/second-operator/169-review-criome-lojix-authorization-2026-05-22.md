# Review Criome Lojix Authorization

Report kind: review
Topic: Criome authorization and Lojix gate residue
Date: 2026-05-22
Lane: second-operator

## What This Review Supersedes

This report supersedes:

- `reports/second-operator/150-criome-authorization-slot-identity-follow-up-2026-05-17.md`
- `reports/second-operator/151-lojix-criome-authorization-gate-2026-05-17.md`
- `reports/second-operator/152-criome-authorization-expiry-replay-guard-2026-05-18.md`

The older reports recorded shipped slices. This report carries forward
only the remaining authorization work.

## Current State

Criome authorization has a useful skeleton:

- authorization requests have slot identity;
- pending authorization state can be observed as a snapshot;
- expiry and replay guards have a first implementation slice;
- Lojix has a policy actor boundary where deployment graph writes can
  ask for permission before preserving or publishing effects.

That is still not full authorization.

## Remaining Debt

Criome:

- `ObserveAuthorization` is snapshot-shaped; pending authorization
  still needs a pushed subscription or delta stream.
- `VerifyAuthorization` still needs real cryptographic verification,
  including BLS signature checks, signer registry status, policy class,
  threshold satisfaction, expiry, replay state, and canonical bytes.
- simple self-signed policy does not yet issue a master-key-signed
  grant.
- owner authorization surface still needs passphrase submission, policy
  mutation, peer-route mutation, and owner approval prompts.
- replay identity may need more than requester plus nonce once the
  canonical `SignedObject` bytes are settled.

Lojix:

- `CriomeAuthorization` is still a local policy actor, not a real
  signal-criome client.
- it creates the right effect boundary, but it does not yet send a
  routed authorization request to Criome.
- Arca artifact preservation remains downstream of the real
  authorization request/response shape.

## Next Useful Work

Do not resume this from the old reports. Resume from this shape:

1. design or implement the real signal-criome client path for Lojix;
2. finish Criome's pushed authorization observation stream;
3. implement full cryptographic verification and signed grants;
4. add owner-signal-criome policy and approval operations;
5. then wire Arca artifact preservation against the real grant path.

This is separate from the current `primary-c620` Orchestrate migration.
Pick it up when the user switches back to Criome/Lojix authorization or
the horizon/lojix re-engineering bead needs it.

