# 425 — Engine Audit Follow-up: Criome Majority Quorums

Operator follow-up to `reports/designer/690-engine-audit/10-synthesis.md`.

## Scope

I reviewed the designer audit and fixed the highest-value small safety gap it identified in criome: quorum declarations were satisfiable without being partition-safe. Before this patch, a `2-of-5` policy threshold and a `2-of-5` attested-time authority set were both structurally valid. That allowed two disjoint partitions to mint conflicting accepted results.

The fix landed on criome main:

- Commit: `22801af` — `criome: enforce majority quorums`
- Repo: `/git/github.com/LiGoldragon/criome`

## What Changed

Criome now has one shared quorum-shape check in [language.rs](/git/github.com/LiGoldragon/criome/src/language.rs:609):

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct QuorumShape {
    required: u16,
    authorities: usize,
}

impl QuorumShape {
    fn is_valid_majority(&self) -> bool {
        let required = usize::from(self.required);
        required != 0 && required <= self.authorities && required > self.authorities / 2
    }
}
```

That invariant is now used in both quorum-bearing paths:

- Contract threshold admission rejects non-majority thresholds as `ThresholdUnsatisfiable` in [language.rs](/git/github.com/LiGoldragon/criome/src/language.rs:407).
- Attested-moment verification rejects non-majority time-authority propositions as `TimeNotProven` in [language.rs](/git/github.com/LiGoldragon/criome/src/language.rs:572).

I updated the existing time-switch test away from its old `1-of-2` convenience shape and into valid majority quorums: `2-of-3` before the boundary, `3-of-3` after it.

## Tests Added

Two regression tests cover the exact audit gap:

- `admission_rejects_submajority_thresholds_before_evaluation` proves a `2-of-5` contract threshold is rejected before admission: [language.rs](/git/github.com/LiGoldragon/criome/tests/language.rs:444).
- `submajority_time_authority_rejects_attested_moment` proves a `2-of-5` attested-time proposition with two real BLS signatures is still rejected before policy evaluation: [language.rs](/git/github.com/LiGoldragon/criome/tests/language.rs:347).

## Verification

All verification passed:

- `cargo test --all-targets`
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --builders '' --no-write-lock-file --log-format bar-with-logs`

The Nix check used the repo's normal remote flake inputs. No local `path:/git/...` overrides were used.

## Remaining Audit Item

The designer audit's BLS aggregate verification item remains open. I inspected criome's crypto surface and found only the existing single-key `VerifyBls` path in [master_key.rs](/git/github.com/LiGoldragon/criome/src/master_key.rs:126), with single-signature callers in admission, policy evaluation, agreement verification, attested-time verification, and the actor verifier.

I did not implement aggregate verification in this patch because it needs a deliberate aggregate-verification noun, tests over same-message and rogue-key conditions, and a clear integration point for `AttestedMoment` signature verification. That is a separate crypto slice, not a local refactor.

