# Operator-Assistant 108 - Signal-Criome Foundation Self-Review

Date: 2026-05-13  
Role: operator-assistant  
Work item: `primary-5rq` - `criome: implement Spartan BLS auth substrate (per designer/141)`

## Scope

This report reviews my latest `signal-criome` work after reading:

- `reports/designer/141-minimal-criome-bls-auth-substrate.md` - reframes today's `criome` as a minimal Spartan BLS12-381 authentication and attestation daemon. The key architectural sentence is: **Criome verifies; Persona decides.**
- `reports/designer-assistant/30-minimal-criome-persona-auth-research.md` - confirms the same split: Criome should provide small, cryptographic truth records and should not become Persona's policy, prompt-audit, or authority model.

The actual implementation landed in the new repository:

- `/git/github.com/LiGoldragon/signal-criome`
- GitHub: `https://github.com/LiGoldragon/signal-criome`
- Commit: `cc6dfa4e` - `signal-criome contract foundation`

I also made a narrow primary-workspace map update:

- `/home/li/primary/protocols/active-repositories.md`
- Commit/bookmark: `af03b5d6` - `protocols: add signal-criome active map`
- Pushed as bookmark: `push-signal-criome-active-map`

## What I Built

I created `signal-criome` as a pure Signal contract crate. It has no daemon, no storage, no actor runtime, and no Persona policy gate.

The contract vocabulary currently includes:

- principal and key identity records;
- BLS-only signature scheme names;
- signature envelopes;
- out-of-band attestations;
- signed object references;
- delegation grants;
- component release records;
- signed Persona requests;
- identity registration, revocation, lookup, and subscription requests;
- attestation requests for archive, channel grant, and authorization use cases;
- sign and verify request/reply variants;
- root `CriomeRequest` / `CriomeReply` Signal channels.

The central file is:

- `/git/github.com/LiGoldragon/signal-criome/src/lib.rs`

The local architectural statement is:

- `/git/github.com/LiGoldragon/signal-criome/ARCHITECTURE.md`

The test surface is:

- `/git/github.com/LiGoldragon/signal-criome/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/signal-criome/flake.nix`

## Architecture I Intended

The intended split is:

1. `signal-criome` names the wire vocabulary.
2. `criome` will be the daemon that owns identity/revocation state, BLS signing, verification, and subscriptions.
3. Persona components consume Criome verification facts but do not delegate policy decisions to Criome.
4. Attestations stay out-of-band: content records point to digests and purposes; they do not carry embedded proof blobs that turn every application record into an auth protocol.
5. The dangerous old names are absent: no `AuthProof`, no `LocalOperatorProof`, no in-band authority gate.

That matches the designer direction as I understand it.

## Verification

I ran:

```sh
nix develop -c cargo fmt
nix flake check -L
```

The flake check passed. The checks include:

- Cargo build;
- Cargo tests;
- round-trip test target;
- doctests;
- docs;
- formatting;
- clippy;
- rkyv feature discipline;
- no runtime/storage/daemon surface in the contract crate.

## Best Parts

The useful part of the work is that it gives the stack a concrete contract boundary for the new Criome direction. Before this slice, the new architecture existed in reports but did not have a crate that other components could depend on.

The crate also locks in several naming decisions that matter:

- `SignatureEnvelope`, not `AuthProof`;
- `Attestation`, not embedded proof fields;
- `VerificationResult`, not policy approval;
- `PrincipalStatus` / `IdentityUpdate`, not Persona-owned authorization state.

Those names should reduce the chance that later agents re-create the old proof/gate model inside Persona records.

## Worst Parts

The worst part is that this is still mostly vocabulary. I did not implement the `criome` daemon, the BLS signer, the verifier, the identity registry, redb tables, subscriptions, or any integration with Persona components. So the work is useful as a contract seed, but it does not yet prove the system can verify a real signature or move a real attestation through the stack.

The second worst part is that the BLS dependency is present but not exercised. `blst` is in `Cargo.toml`, and the vocabulary is BLS-only, but there is no test that generates a keypair, signs a digest, and verifies it. That means the contract shape may still be awkward once real `blst` ergonomics enter the implementation. Designer/141 explicitly deferred G1/G2 layout decisions to implementation; I preserved that deferral instead of resolving it.

The third weak point is that the round-trip tests are necessary but shallow. They prove that the Signal/NOTA frame surface can encode and decode representative values. They do not prove semantic constraints like replay prevention, revocation behavior, subscription ordering, timestamp windows, or delegation scope boundaries.

The fourth weak point is that the contract may be too broad for a first cut. I included several record families at once: identity records, delegation, component releases, signed Persona requests, channel grant attestations, archive attestations, and authorization attestations. That is aligned with the report's direction, but it creates a bigger API surface before there is daemon pressure from real handlers.

The fifth weak point is that I updated `/home/li/primary/protocols/active-repositories.md` from the implementation lane. The update was narrow and correct as a drift fix, but it is still a workspace protocol document. I pushed it as its own bookmark instead of mixing it into another line of work, but it should be reviewed before treating it as merged workspace truth.

The sixth weak point is naming around `SignedPersonaRequest`. It is probably useful, but it is close enough to Persona policy that it deserves scrutiny. If this type becomes "Criome decides whether Persona may act," that would violate the architecture. It must stay a signed content/request envelope whose verification fact is consumed by Persona-owned policy.

The seventh weak point is that the no-runtime/no-storage check is a text scan. That is a cheap architectural smoke test, not a deep guarantee. It can catch obvious drift, but it cannot prove the crate will stay pure if future dependencies smuggle runtime behavior behind innocent names.

## What I Would Redo

I would make the first implementation smaller and sharper:

1. Start with only identity registration, identity revocation, signature envelope, attestation, sign request, verify request, and verification result.
2. Add one real BLS fixture test immediately, even if it lives as a daemon-facing test binary rather than a pure contract test.
3. Add the specialized attestation families only after the `criome` daemon has handlers that need them.
4. Keep `SignedPersonaRequest` out until Persona has a concrete consuming path.

That would produce less surface area and more cryptographic proof earlier.

## What Should Happen Next

The next high-signal work is not more contract vocabulary. It is the daemon skeleton in `/git/github.com/LiGoldragon/criome`:

1. Rewrite `criome` away from the stale sema-record validator shape.
2. Add the `signal-criome` dependency.
3. Create a Kameo actor topology with real data-bearing actors:
   - identity registry actor;
   - attestation signer actor;
   - verifier actor;
   - subscription broadcaster actor;
   - root runtime actor.
4. Add redb-backed Sema state for identities and revocations.
5. Add a Nix-wired cryptographic smoke test:
   - generate or load a deterministic test identity;
   - sign a digest;
   - verify the signature;
   - revoke the identity;
   - prove verification changes after revocation.

That test should be artifact-oriented, not just a round trip. It should leave inspectable outputs for identity state, signed attestation, verification result before revocation, revocation record, and verification result after revocation.

## Current Status

`signal-criome` is a useful first foundation, but it is not enough to call the Criome auth substrate implemented.

The honest status is:

- contract foundation: landed;
- workspace map: updated on a reviewable bookmark;
- daemon rewrite: not started by me;
- real BLS signing/verification: not implemented;
- persistent identity/revocation state: not implemented;
- Persona integration: not implemented;
- meaningful end-to-end security witness: missing.

The work is worth keeping, but it needs immediate pressure from the real daemon and BLS tests before the vocabulary hardens into accidental architecture.
