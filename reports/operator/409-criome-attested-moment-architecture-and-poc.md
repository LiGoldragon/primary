# Criome attested moment architecture and POC

Operator meta report for the stacked branches:

- `signal-criome` branch `operator/criome-attested-moment`, commit `8459fb4e` — `signal-criome: add attested moment policy evidence`
- `criome` branch `operator/criome-attested-moment`, commit `92a703b5` — `criome: bind policy evaluation to attested moments`

This is stacked on report `408`'s policy-contract branches. The policy branch made contract evaluation schema-first. This branch adds the first concrete G3+G4 proof: crystallized time is carried in the policy input, and operation signatures are bound to that time object.

## Architecture

The design splits cleanly across the triad:

- Signal: public attested-time nouns and policy evidence live in `signal-criome`.
- Nexus: criome evaluates the generated nouns, verifies signatures, checks windows, and decides.
- SEMA: durable persistence is still future work; the POC store remains in-memory.

The important correction from the old shape is this:

```nota
Evidence {
  operation OperationDigest
  observed_at AttestedMoment
  signatures (Vector SignatureEnvelope)
  agreements (Vector AgreementFact)
}
```

`observed_at` is no longer a caller-supplied integer. It is a quorum-signed time object.

## Schema shape

`signal-criome` now defines the time proof:

```nota
AttestedMomentDigest { value ObjectDigest }

TimeWindow {
  opens_at TimestampNanos
  closes_at TimestampNanos
}

AttestedMomentProposition {
  window TimeWindow
  required_signatures RequiredSignatureThreshold
  authorities (Vector Identity)
}

TimeSignature {
  signer Identity
  envelope SignatureEnvelope
}

AttestedMoment {
  proposition AttestedMomentProposition
  signatures (Vector TimeSignature)
}
```

The proposition is the content-addressed object: window + threshold + authorities. The signatures accrete onto that proposition. Once enough valid signatures exist, the moment crystallizes as a proof that the window has passed.

The canonical request example now looks like:

```nota
(EvaluateAuthorization
  (contract-digest-1
    (operation-digest-1
      (((10 20) 1 [(Developer timekeeper)])
       [((Developer timekeeper) (Bls12_381MinPk public-key-1 signature-1))])
      [(Bls12_381MinPk public-key-1 signature-1)]
      [])))
```

Same structure in plain English:

- evaluate `contract-digest-1`
- for operation `operation-digest-1`
- at the attested window `[10, 20]`
- with threshold `1`
- authority `Developer timekeeper`
- carrying that authority's BLS signature over the proposition
- plus the actor's operation signature

## Nexus evaluation

Criome now rejects invalid time before evaluating the policy:

```rust
let contract = self.resolve(digest)?;
if let Some(reason) = evidence.observed_at.rejection_reason(registry) {
    return Ok(EvaluationDecision::Rejected(reason));
}
contract.rule().decide(evidence, self, registry)
```

The verifier checks:

- `opens_at < closes_at`
- required signature count is non-zero
- required signature count is not greater than the authority set
- authority identities are distinct
- signatures are from listed authorities
- signatures are distinct by signer
- public keys resolve through the admitted key registry
- BLS signatures verify over the attested-moment proposition

If the time object is malformed, evaluation returns `InvalidTimeAttestation`. If the object is well-formed but quorum-short, evaluation returns `TimeQuorumShort`.

## Replay binding

The operation signature now covers the attested moment digest:

```rust
pub fn to_signing_bytes(&self) -> Result<Vec<u8>, StatementError> {
    let mut bytes = b"CRIOME-OPERATION-AUTHORIZATION-V1".to_vec();
    self.signer.encode_into(&mut bytes);
    self.operation.object_digest().encode_into(&mut bytes);
    self.observed_at
        .proposition
        .digest()?
        .object_digest()
        .encode_into(&mut bytes);
    Ok(bytes)
}
```

That means a valid operation signature under one crystallized moment cannot be replayed under another moment. The test `operation_signature_is_bound_to_the_attested_moment` proves this.

## Time semantics

Time rules compare against the close of the crystallized window:

- `ActiveAfter(T)`: authorized only when `observed_at.closes_at >= T`
- `ActiveUntil(T)`: authorized only when `observed_at.closes_at < T`
- `TimeSwitch(T)`: uses the `before` threshold before `T`, and the `after` threshold at or after `T`

This matches the clarified `ay3y` model: only the past can be crystallized. A closed attested window is a lower bound on now, and an operation carries its own proof-of-when.

## Constraints

The implemented POC is deliberately narrower than the full stamped-envelope architecture.

Implemented now:

- attested time object in the public signal schema
- `Evidence.observed_at` uses that object
- policy evaluation rejects invalid time attestations
- operation signatures bind to the attested moment
- daemon-root request path registers a timekeeper and evaluates through `EvaluateAuthorization`

Not implemented yet:

- shared triad envelope stamp for every request/reply/event root
- durable SEMA storage for admitted contracts
- durable SEMA storage for attested moments
- branch / monotonic-version binding in the signed preimage
- meta-policy operations for defining/changing time authorities

The next architecture step is not to hand-add `AttestedMoment` to every current root. The better shape is a shared stamped frame/envelope in the signal-frame or generated triad frame layer, so every Input/Output/Event carries the imported stamp uniformly.

## Test proof

Local `signal-criome`:

- `SIGNAL_CRIOME_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text`
- `cargo test --features nota-text`
- `cargo clippy --all-targets --features nota-text -- -D warnings`

Local `criome`:

- `cargo test`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --features nota-text`
- `cargo clippy --all-targets --features nota-text -- -D warnings`

Remote Nix, remote refs only:

```sh
nix build --builders '' --log-format bar-with-logs --print-out-paths --no-link \
  'git+https://github.com/LiGoldragon/signal-criome.git?ref=operator/criome-attested-moment#checks.x86_64-linux.test-nota-text'

nix build --builders '' --log-format bar-with-logs --print-out-paths --no-link \
  'git+https://github.com/LiGoldragon/criome.git?ref=operator/criome-attested-moment#checks.x86_64-linux.test-nota-text'
```

Results:

- `signal-criome` Nix `test-nota-text`: green, 17 tests
- `criome` Nix `test-nota-text`: green, 51 tests

No `path:` overrides were used.

## Operator read

This validates the design direction. Time fits the triad as signal vocabulary plus Nexus verification, not as a hidden daemon clock or a fourth engine. The remaining work is mostly placement and durability: move from policy-evidence stamping to a generated shared stamped envelope, and persist both contracts and moments through SEMA.
