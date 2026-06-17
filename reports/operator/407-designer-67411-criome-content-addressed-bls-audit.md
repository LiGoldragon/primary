# 407 — Audit of designer 674.11: criome content-addressed BLS prototype

Audit target: `reports/designer/674-criome-internal-engine/11-content-addressed-bls-prototype.md`

Code target: `/home/li/wt/github.com/LiGoldragon/criome/language-content-addressed-bls`, branch `language-content-addressed-bls`, commit `b97db6b`.

## Verdict

Designer is right that the prototype materially improves the v0 Criome language shape: content-addressed composition is real, real BLS verification is wired through the deployed `MasterKey` / `VerifyBls` path, and the claimed cargo tests pass.

It is not merge-ready. There is one security blocker in quorum evaluation and one basic hygiene blocker: quorum members are not counted distinctly despite the code claiming they are, and `cargo fmt --check` fails. Treat the branch as valid design evidence, not an operator integration candidate until those are fixed.

## Findings

### Blocker: duplicate quorum members count multiple times

Location: `/home/li/wt/github.com/LiGoldragon/criome/language-content-addressed-bls/src/language.rs:460`

The `Threshold::decide` comment says it counts distinct satisfied members:

```rust
/// A member is satisfied when its key really signed the operation, or when the
/// referenced sub-object authorizes. Counts distinct satisfied members.
fn decide(...)
```

The implementation increments once per vector entry:

```rust
let mut satisfied: u16 = 0;
for member in &self.members {
    if member.is_satisfied(evidence, store, registry)? {
        satisfied = satisfied.saturating_add(1);
    }
}
```

That means a policy can repeat the same member twice and satisfy a 2-of-2 quorum with one signature:

```rust
Threshold::new(
    RequiredSignatureThreshold::new(2),
    vec![
        PolicyMember::key_member(alice.identity.clone()),
        PolicyMember::key_member(alice.identity.clone()),
    ],
)
```

I confirmed with an audit-only test. Expected rejection:

```text
Rejected(QuorumShort { required: 2, satisfied: 1 })
```

Actual result:

```text
Authorized
```

This is not cosmetic. It breaks the quorum security property. Fix options:

- Reject duplicate `PolicyMember`s at contract admission.
- Canonicalize/deduplicate members before hashing/evaluation.
- Track satisfied member identities/digests during evaluation and count each member key only once.

The first or second option is cleaner because it makes the policy object itself valid or invalid, rather than letting malformed policy survive into evaluation.

### Blocker: branch is not fmt-clean

Location: `src/language.rs`, `tests/language.rs`.

`cargo fmt --check` fails with formatting diffs. The branch passes `cargo test`, `cargo test --test language`, and clippy, but it is not at the normal merge bar. Because the flake has a `fmt` check, a normal Nix check would reject this branch.

Designer's report did not claim fmt, but it did say "verified and green." In our repo discipline, fmt is part of green.

### Integration gap: the schema file is a concept sketch, not the implemented wire

Location: `/home/li/wt/github.com/LiGoldragon/criome/language-content-addressed-bls/schema/criome.language.schema:8`

The schema says it is "concept schema documenting the intended nouns while the Rust POC in src/language.rs proves the evaluator shape." `rg` confirms the schema is only included by `tests/language.rs` for a construct-name smoke test:

```text
tests/language.rs:535: let schema = include_str!("../schema/criome.language.schema");
```

That is acceptable for a design-pressure prototype, but it means this is not yet a schema-generated Criome contract, not on `signal-criome`, and not persisted through SEMA. Operator integration should keep that boundary explicit.

### Deferred gaps are real and still load-bearing

The report is honest that these are deferred:

- G3 attested clock: `Evidence::observed_at` is caller-supplied.
- G4 replay / branch binding: operation authorization is not bound to branch, monotonic version, or attested moment.
- G6 resolver pinning: `Agreement` checks a real resolver signature but does not yet anchor the resolver to a pre-fork accepted object.
- G10 wire / SEMA: no contract-store persistence or signal contract.

These do not invalidate G1/G2 as prototype proofs. They do mean this cannot be described as the full Criome language foundation.

## Verified Good

The good parts are substantial.

Content-addressed composition exists in code: `Rule::All`, `Rule::Any`, and `PolicyMember::ObjectMember` hold `ObjectDigest` references; `ContractStore::admit` rejects dangling references; `ContractStore::resolve` returns typed `EvaluationError::MissingContract` instead of panicking.

Real BLS verification exists in code: `Evidence::has_valid_signature_from` resolves `Identity -> BlsPublicKey`, requires the envelope key to equal the admitted key, requires `SignatureScheme::Bls12_381MinPk`, and calls `VerifyBls::verify_bls` over an `OperationStatement` preimage. The tests sign through `MasterKey::sign`.

The reported tests are real:

```text
cargo build                          pass
cargo test                           pass, 48 tests total
cargo test --test language           pass, 15 tests
cargo clippy --all-targets -- -D warnings   pass
cargo fmt --check                    fail
```

The branch is one commit ahead of criome main and clean after audit:

```text
b97db6b criome: content-addressed policy objects + real BLS verification (designer prototype)
base 9719703 criome: add explicit psyche escalation outcome
```

## Recommendation

Do not land this branch as-is.

The next operator-quality slice should be:

1. Fix quorum distinctness at admission or canonicalization time.
2. Add tests for duplicate `KeyMember`, duplicate `ObjectMember`, and threshold zero / empty-member semantics.
3. Run `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`, and the flake fmt/test checks.
4. Only then rebase the prototype onto criome main as the G1/G2 foundation.
5. Keep G3+G4 as the next security slice: attested time plus replay/branch binding as one signed anchor.

