# 674.11 — Content-addressed policy objects + real BLS (designer ~/wt prototype)

*A design-pressure prototype rebasing criome's internal policy language onto the
two foundational fixes the critique named: G1 content-addressed composable
objects (critic F2) and G2 real BLS verification (critic F1). Built in a feature
worktree off criome main, evolving the in-tree `src/language.rs` the designer and
operator lanes converged on. This is **not landed** — it is the shape for operator
to rebase onto main. The attested-clock fix (G3) is deliberately deferred and
documented as such.*

Worktree: `/home/li/wt/github.com/LiGoldragon/criome/language-content-addressed-bls`
Branch: `language-content-addressed-bls` (off criome main `9719703`)

## What changed, in one line

The v0 module was an inline recursive `Rule` tree (`All(Vec<Rule>)`, `Box<Rule>`)
whose "verification" was `Vec::contains` over bare `Identity`s. This prototype makes
a `Contract` a **content-addressed object** whose composition arms reference
sub-contracts **by `ObjectDigest`**, resolved from an acyclic `ContractStore`, and
makes the `SignedBy` leaf **verify a real BLS12-381 signature** over the exact
operation content digest through criome's deployed `VerifyBls` path. No
honor-system membership check survives in the evaluation path.

## The design

### G1 — content-addressed composable objects

A `Contract` wraps a `Rule` and its identity *is* `blake3(canonical_bytes)`,
projected into the deployed `signal_criome::ObjectDigest` (whose `from_bytes` is
exactly blake3 — so the prototype reuses the deployed digest type rather than
inventing a `ContractDigest`). The canonical encoding is a domain-tagged,
length-delimited byte rendering of the policy, deterministic across runs (proven by
`digest_is_stable_and_distinguishes_contracts`).

Composition references sub-objects by digest, never inline:

```rust
pub enum Rule {
    SignedBy(Identity),                 // leaf — verifies a real BLS signature
    All(Vec<ObjectDigest>),             // AND over referenced contracts
    Any(Vec<ObjectDigest>),             // OR  over referenced contracts
    Threshold(Threshold),               // k-of-n over PolicyMembers
    ActiveAfter(TimedRule),             // timelock release  (leaf, inline)
    ActiveUntil(TimedRule),             // window close      (leaf, inline)
    TimeSwitch(TimeSwitch),             // two-phase quorum  (leaf, inline)
    Agreement(AgreementRule),           // signed reconciliation (logic shape)
    EscalateToPsyche,                   // operator's psyche rung, preserved
}

pub enum PolicyMember {
    KeyMember(Identity),                // a key whose signature is verified
    ObjectMember(ObjectDigest),         // another admitted object, by digest
}
```

Leaves (`SignedBy`, the timelock arms, `TimeSwitch`) stay inline as the critique
allows — only *composition* references other contracts. A `Threshold`'s
`PolicyMember` is the z9d6 hinge: a quorum member is either a key or another object
by digest, so a panel quorum can be defined once and referenced by many parents.

`ContractStore` maps `ObjectDigest -> Contract` and enforces **acyclicity at
admission**:

```rust
pub fn admit(&mut self, contract: Contract) -> Result<ObjectDigest, AdmissionError> {
    for reference in contract.rule().referenced_digests() {
        if !self.contains(&reference) {
            return Err(AdmissionError::DanglingReference(reference));
        }
    }
    // ... insert keyed by contract.digest()
}
```

A contract may only reference digests already present — a hash cannot name a
not-yet-computed hash — so the reference graph is a strict DAG by construction and
evaluation recursion is bounded by store size (this closes critic F6's
unbounded-recursion drift for free). The evaluator resolves each referenced digest;
a missing digest is a typed `EvaluationError::MissingContract`, never a panic.

(Implementation note: `signal_criome::ObjectDigest` and `Identity` are `Eq` but not
`Ord`/`Hash`, so the store and registry are `Vec`s of typed entries with
equality-keyed lookup rather than a `BTreeMap`/`HashMap`. Correct content-addressed
lookup is by digest equality; the linear scan is fine for a prototype and avoids
forcing trait impls onto the deployed wire types.)

### G2 — real BLS verification

`Evidence` now carries deployed `SignatureEnvelope`s (`{ scheme, public_key,
signature }`), not bare `Vec<Identity>`. The `SignedBy` leaf does what the critique
demands:

```rust
pub fn has_valid_signature_from(&self, identity: &Identity, registry: &KeyRegistry) -> bool {
    let Some(admitted_key) = registry.public_key(identity) else { return false; };
    let statement = OperationStatement::new(identity, &self.operation).to_signing_bytes();
    self.signatures.iter().any(|envelope| {
        matches!(envelope.scheme, SignatureScheme::Bls12_381MinPk)
            && &envelope.public_key == admitted_key
            && admitted_key.verify_bls(&envelope.signature, &statement)
    })
}
```

It (a) resolves the `Identity` to its admitted `BlsPublicKey` via a `KeyRegistry`,
(b) requires the envelope's key to equal the admitted key (so a real signature from
a non-admitted key claiming the identity fails), (c) rejects any scheme but the
implemented min-pk (no algorithm confusion), and (d) calls the **deployed**
`VerifyBls::verify_bls` from `src/master_key.rs` — real `blst` min-pk verification
under criome's `ATTESTATION_DST` domain tag — over the `OperationStatement`
preimage binding the exact 32-byte blake3 operation digest. The `OperationStatement`
mirrors the deployed `AttestationPreimage`/`RegistrationStatement` pattern
(domain-tag + length-delimited fields). Signatures in tests are produced by the
deployed `MasterKey::sign` path, so signer and verifier share the real crypto.

`Decision` keeps operator's three-way `Authorized / Rejected / EscalateToPsyche`
with the `All`/`Any` propagation intact, and enriches `Rejected` with a typed
`RejectionReason` (`SignatureMissing(Identity)`, `QuorumShort { required, satisfied }`,
`OutsideTimeWindow`, `AgreementMissing`) — a cheap step toward critic F10.

### Error discipline

A *denial* (`Decision::Rejected(reason)`) is a valid evaluation result and carries a
typed domain reason. An *error* (a malformed contract graph) is distinct:
`EvaluationError` and `AdmissionError` derive `thiserror::Error` (consistent with the
crate's existing `thiserror` use) and fold into the crate-level `crate::Error` via
`#[from]`, so the language module's failures join the one crate `Error` enum.

## Key code excerpts

The `SignedBy` evaluation arm — typed result, real verification, no set membership:

```rust
Self::SignedBy(identity) => Ok(match evidence.has_valid_signature_from(identity, registry) {
    true  => Decision::Authorized,
    false => Decision::Rejected(RejectionReason::SignatureMissing(identity.clone())),
}),
```

A quorum member that is itself an object by digest (the z9d6 composition recursion):

```rust
Self::ObjectMember(digest) => {
    let contract = store.resolve(digest)?;            // typed error if absent
    Ok(contract.evaluate(evidence, store, registry)?.is_authorized())
}
```

## Real cargo output (verbatim)

`cargo build` — clean:

```
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
```

`cargo test` — all suites, full crate (the 15 language tests are the new work; the
20 daemon + 2 actor + 11 lib tests are the deployed crypto still passing alongside):

```
     Running unittests src/lib.rs
test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/actor_discipline_truth.rs
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/daemon_skeleton.rs
test result: ok. 20 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/language.rs
running 15 tests
test acyclicity_enforced ... ok
test digest_is_stable_and_distinguishes_contracts ... ok
test explicit_policy_can_escalate_to_psyche ... ok
test missing_reference_during_evaluation_is_a_typed_error ... ok
test schema_sketch_names_every_construct ... ok
test escalation_composes_through_all_after_required_rules_authorize ... ok
test real_bls_authorizes ... ok
test any_prefers_authorization_before_escalation ... ok
test forged_signature_rejected ... ok
test agreement_requires_a_quorum_signed_reconciliation_fact ... ok
test timelock_release_with_real_signature ... ok
test quorum_two_of_three_with_real_signatures ... ok
test object_member_composes_a_sub_contract_into_a_quorum ... ok
test content_addressed_sharing ... ok
test time_switch_tightens_quorum_after_boundary ... ok
test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`cargo clippy --all-targets -- -D warnings` — clean:

```
    Checking criome v0.1.1 (/home/li/wt/github.com/LiGoldragon/criome/language-content-addressed-bls)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.10s
```

Nix verification skipped per task instruction (operator hit shared-daemon
contention; cargo is sufficient for design pressure).

## The mandated tests, mapped to the fixes

| Test | Proves |
|---|---|
| `content_addressed_sharing` | one quorum sub-contract admitted once, its digest referenced by two parents; both resolve and evaluate (composition-by-digest, G1) |
| `object_member_composes_a_sub_contract_into_a_quorum` | a `PolicyMember::ObjectMember` resolves a sub-object as a quorum member (z9d6 recursion) |
| `acyclicity_enforced` | admitting a contract that references an absent digest is `AdmissionError::DanglingReference` |
| `missing_reference_during_evaluation_is_a_typed_error` | a missing digest at evaluation is `EvaluationError::MissingContract`, not a panic |
| `digest_is_stable_and_distinguishes_contracts` | the content address is a deterministic function of policy bytes |
| `real_bls_authorizes` | a real blst keypair signs the operation digest; the admitted key verifies → Authorized (G2) |
| `forged_signature_rejected` | three attacks all → Rejected: real signature over the **wrong** digest; real signature from a **non-admitted** key claiming the identity; structurally **malformed** signature (the F1 fix) |
| `quorum_two_of_three_with_real_signatures` | k-of-n over real signatures, typed `QuorumShort` reason when short |
| `timelock_release_with_real_signature` | `ActiveAfter` gates a real signature on the time boundary |
| `time_switch_tightens_quorum_after_boundary` | two-phase quorum (1-of-2 before, 2-of-2 after) over real signatures |
| `agreement_requires_a_quorum_signed_reconciliation_fact` | reconciliation fact must be really signed by the resolver; impostor rejected |
| `explicit_policy_can_escalate_to_psyche` / `escalation_composes_through_all…` / `any_prefers_authorization_before_escalation` | operator's `EscalateToPsyche` + `All`/`Any` propagation preserved over the new store/Evidence shape |

## Proven vs in-test-registry vs deferred (honest)

| Mechanic | Status | Honest detail |
|---|---|---|
| Content-addressed `Contract` (digest = blake3 of canonical bytes) | **REAL** | reuses deployed `ObjectDigest::from_bytes` (blake3); deterministic, tested |
| Composition by digest (`All`/`Any`/`ObjectMember`) | **REAL** | resolved from `ContractStore`; shared sub-contract proven |
| Acyclicity at admission → strict DAG, bounded recursion | **REAL** | enforced in `admit`; dangling reference rejected (tested) |
| Missing-reference = typed error, not panic | **REAL** | `EvaluationError::MissingContract` (tested) |
| **BLS12-381 (min-pk) signature verification** | **REAL** | calls deployed `VerifyBls::verify_bls` (`blst`) under `ATTESTATION_DST`; signing via deployed `MasterKey::sign` |
| Signature bound to the exact operation content digest | **REAL** | `OperationStatement` preimage; wrong-digest signature rejected (tested) |
| Non-admitted-key / wrong-scheme / malformed-signature rejection | **REAL** | all three tested in `forged_signature_rejected` |
| k-of-n quorum, timelock, two-phase time-switch | **REAL** (logic) over real signatures | the time *comparison* is real; the clock is not (see deferred) |
| `Identity → BlsPublicKey` resolution (`KeyRegistry`) | **IN-TEST REGISTRY** | populated in-test from admitted keys; deployed model populates from `IdentityRegistry`/cluster-root admission (`ClusterRoot::admits`). The registry is a stand-in for the admission wiring, but the verification it gates is real |
| Signed reconciliation (`Agreement`) | **PARTIAL** — signature real, resolver-pinning deferred | the resolver's signature over the reconciliation preimage is really verified; the common-ancestor resolver-pinning + `Divergence`/`Fork` objects (G6/critic F3) are not built |
| **Attested clock (`observed_at`)** | **DEFERRED (G3)** | still caller-supplied, explicitly documented; the trusted-time fix (critic F4) is the next foundational step and is *not* solved here |
| Replay / branch binding (`ReplayBinding`) | **DEFERRED (G4)** | not in this prototype |
| Wire / SEMA (`criome-contract` family) | **DEFERRED (G10)** | schema sketch updated to the new shape; not on the wire |

## Diff-shape from operator's v0 (for the rebase)

- `Rule::All`/`Any` change from `Vec<Rule>` to `Vec<ObjectDigest>`; `TimedRule`/
  `TimeSwitch` drop `Box<Rule>` — `TimedRule` holds a `signed_by: Identity` leaf,
  `TimeSwitch` holds `before`/`after` `Threshold`s. `Box<Rule>` is gone entirely.
- `Threshold.authorities: Vec<Identity>` becomes `members: Vec<PolicyMember>`.
- New types: `Contract::digest()`/`canonical_bytes()`, `ContractStore` (+ `admit`/
  `resolve`), `KeyRegistry`, `PolicyMember`, `OperationDigest`, `OperationStatement`,
  `EvaluationError`, `AdmissionError`.
- `Evidence` gains an `operation: OperationDigest`; `signatures` becomes
  `Vec<SignatureEnvelope>`; `AgreementFact` gains an `envelope: SignatureEnvelope`.
- `Contract::evaluate` signature becomes
  `(&self, &Evidence, &ContractStore, &KeyRegistry) -> Result<Decision, EvaluationError>`.
- `Decision::Rejected` carries a typed `RejectionReason` (was a bare unit variant).
- `crate::Error` gains `PolicyEvaluation`/`ContractAdmission` `#[from]` arms.
- `schema/criome.language.schema` rewritten to the content-addressed vocabulary
  (digest references, `PolicyMember`, `SignatureEnvelope` in `Evidence`,
  `ContractStore`/`KeyRegistry`). The schema-construct-name test was updated to match.

This is a designer `~/wt` prototype. Operator owns criome main and the rebase;
G1/G2 touch the deployed crypto and are naturally operator-carried. The next
foundational step after this lands is G3+G4 (attested clock + replay binding) — one
signed `(object-digest, branch, monotonic-version, attested-moment)` anchor.
