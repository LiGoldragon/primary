# 674.7 — Rust proof-of-concept: criome's limited typed identity-policy language

*rust-poc agent. A self-contained, actually-compiling-and-running Rust crate
demonstrating the LOGIC of criome's internal engine (Spirit `vhs2`/`z9d6`/
`wckt`): public-key identity atoms; complex identity composition (k-of-n
quorum, time-lock, time-varying threshold); a typed authorization-evaluation
verb returning `Authorized | Denied(reason)`; and a divergence-reconciliation
interface with a stub LLM-oracle whose signed verdict re-enters the
deterministic path. All output below is REAL — the commands were run and the
output pasted verbatim. Nothing is faked.*

## Status note: this PoC was built against files 0/1/2/4, not file 5

The brief pointed me at `5-object-verb-design.md` ("read it first"). **That file
did not exist** when this agent ran — the directory held only `0`–`4`. Rather
than block, the PoC was built on the binding inputs that file 5 synthesizes
from: the frame's constraints (`0`), the existing-vocabulary inventory (`1`,
which crucially documents the already-started in-tree evaluator
`criome/src/language.rs` and its `Rule`/`Contract`/`Evidence`/`Decision`
vocabulary), and the primitives research (`4`, the quorum/time-lock/
time-varying/divergence-oracle shapes). The PoC therefore converges on the
**same object/verb vocabulary file 5 is expected to specify** — it is named
deliberately so the design author can confirm or adjust. The single open risk:
if file 5 renames or restructures the `Rule` tree, this PoC's type names move
with it (no production to protect; that is expected and cheap).

## The crate

Standalone at `/tmp/criome-poc`, `cargo new --lib`, **zero external
dependencies** (no `blst`, no criome repos, no `thiserror`). The signature
scheme is a deterministic stub: a `Signature` binds its signer `PublicKey` and
the `MessageDigest` it covers, and `verifies` is a pure equality check — the
same per-key/per-message determinism real BLS provides (report 4 §A.1), which
is the only property the policy logic depends on. Compiles in ~0.3s.

| File | Lines | Role |
|---|---|---|
| `src/lib.rs` | 32 | crate doc + module wiring |
| `src/error.rs` | 60 | the crate's one typed `Error` enum (hand-written `Display`/`Error`, no `thiserror` dep) |
| `src/identity.rs` | 91 | `PublicKey` atom, `MessageDigest`, deterministic `Signature` |
| `src/clock.rs` | 80 | typed time: `LogicalClock`, `Moment`, `Elapsed`; `RequiredSignatures` |
| `src/evidence.rs` | 127 | `Evidence` (sigs + clock + resolutions), typed `Authorization` / `DenialReason` |
| `src/reconciliation.rs` | 163 | `Divergence`, signed `Resolution`, `DivergenceReconciliation` trait, stub `OraclePanel` |
| `src/policy.rs` | 305 | the `Rule` tree, `Quorum`/`Timelock`/`TimeVaryingThreshold`/`Agreement`, `Contract::evaluate` |
| `tests/policy_language.rs` | 369 | 13 integration tests, one or more per demonstration |

## Discipline compliance (rust-discipline.md + abstractions.md)

- **Every function is a method or associated function on a data-bearing type,
  or a trait impl.** Verified mechanically: `grep -rE '^( {0,3})(pub )?(async
  )?fn ' src/` returns NONE — there is no module-scope `fn` in `src/`. Free
  helpers exist only in `#[cfg(test)]` (the `key`/`object` test fixtures), which
  the rule permits.
- **No ZST namespace holders.** `grep -rE 'struct [A-Z][A-Za-z]*;' src/`
  returns NONE — every struct carries data fields.
- **Typed domain values, not primitives.** `PublicKey`, `MessageDigest`,
  `Signature`, `LogicalClock`, `Moment`, `Elapsed`, `RequiredSignatures` are all
  newtypes with private fields and method-only construction/access. Distinct
  roles get distinct types: `Moment` (authored into a contract) is *not*
  `LogicalClock` (read from the engine) even though both wrap a tick count —
  newtype-per-role.
- **Typed `Error` enum per crate.** One `error::Error` with four structured
  variants (`UnsatisfiableQuorum`, `EmptyThresholdSchedule`, `ResolverMismatch`,
  `UnverifiedResolution`), each carrying the data its message needs. No
  `anyhow`/`eyre` (grep NONE).
- **Typed outcome, not a boolean.** `Authorization` is `Authorized |
  Denied(DenialReason)`; a denial always names the failing rule
  (`QuorumShort { required, satisfied }`, `OutsideTimeWindow`,
  `MissingSignature`, `NoBranchSatisfied`, `UnresolvedDivergence`).
- **One object in / one object out.** `Contract::evaluate(&Evidence) ->
  Authorization`; `Resolution::admit(&Divergence, &PublicKey) ->
  Result<ResolutionFact, Error>`. No multi-primitive boundaries, no tuple
  returns.
- **No hand-rolled parsers.** There are none — the PoC builds objects through
  typed constructors, not text parsing (NOTA encoding is file 6's surface).

## The vocabulary realized (objects + verbs)

### (1) Identity atom — `PublicKey`

```rust
pub struct PublicKey(Vec<u8>);

impl PublicKey {
    pub fn from_bytes(bytes: impl Into<Vec<u8>>) -> Self { Self(bytes.into()) }
    pub fn sign(&self, message: &MessageDigest) -> Signature { /* deterministic stub */ }
}
```

The key signs; the signature verifies against the key and message — the noun
that owns the verb is the key (mirrors deployed criome's `VerifyBls` on the wire
`BlsPublicKey`, report 1 §a).

### (2) Complex identity composition — the `Rule` tree

The limited, closed vocabulary. No general computation: only composition of
acceptance policies over identity atoms, time, and divergence facts (Spirit
`vhs2`: "NOT a general-purpose virtual machine"). It converges on the
already-started `criome/src/language.rs` `Rule` enum (report 1 §f).

```rust
pub enum Rule {
    SignedBy(PublicKey),
    Quorum(Quorum),                              // k-of-n
    Timelock(Timelock),                          // active_after / active_within
    TimeVaryingThreshold(TimeVaryingThreshold),  // k = step-function over elapsed time
    All(Vec<Rule>),                              // logical AND
    Any(Vec<Rule>),                              // logical OR
    Agreement(Agreement),                        // divergence must be resolved
}
```

- **`Quorum`** — k-of-n acceptance policy (Spirit `z9d6` composable object;
  report 4 §A.3). Unsatisfiable quorums (`required > members`) are rejected at
  construction with a typed error.
- **`Timelock`** — a window `[not_before, not_after)` around an inner rule. Time
  is a comparison against the engine's attested `LogicalClock`, not a VDF
  (report 4 §A.5).
- **`TimeVaryingThreshold`** — the `vhs2`-specific requirement: required count
  is a **step function over a declared schedule** of `(Elapsed, RequiredSignatures)`
  phases (report 4 §A.6). Decreasing schedule = recovery / dead-man's-switch;
  increasing = decaying delegation. Time enters only as interval selection — the
  language stays limited.

```rust
fn required_at(&self, elapsed: Elapsed) -> RequiredSignatures {
    let mut active = self.schedule[0].required;
    for phase in &self.schedule {
        if elapsed.ticks() >= phase.from.ticks() {
            active = phase.required;
        }
    }
    active
}
```

### (3) The authorization-evaluation verb — `Contract::evaluate`

```rust
pub struct Contract { controller: PublicKey, rule: Rule }

impl Contract {
    pub fn evaluate(&self, evidence: &Evidence) -> Authorization { self.rule.evaluate(evidence) }
}
```

`Evidence` is the one object weighed: the message under authorization, the
gathered signatures, the engine's `LogicalClock`, and any divergence-resolution
facts that re-entered. This is the method the deployed `AuthorizationCoordinator`
would call in place of its current two-class `AuthorizationPolicyClass` stub
(report 1 §b). Counting is duplicate-safe — `satisfied_among` counts each member
at most once, so one member signing twice does not satisfy a 2-of-n quorum.

### (4) Divergence reconciliation — the LLM-oracle re-entry path

The discipline (report 4 §B.2/§B.4): the policy language **never invokes a
model**. It verifies a signed, content-addressed verdict whose signer is itself
a criome identity contract.

```rust
pub trait DivergenceReconciliation {
    fn resolve(&self, divergence: &Divergence) -> Resolution;
}

impl Resolution {
    // Admit a verdict back into the deterministic path: verify it was signed by
    // the named resolver over the divergence's verdict message, then mint the
    // ResolutionFact the Agreement rule looks for. Failure is typed, never silent.
    pub fn admit(&self, divergence: &Divergence, expected: &PublicKey)
        -> Result<ResolutionFact, Error> { /* ... */ }
}
```

`OraclePanel` is the stub LLM/expert-panel resolver: it holds the resolver's
signing identity, does its (fixed, reproducible) verdict selection inside
`resolve`, and emits only a signed verdict. The non-determinism of a real model
is replaced by a fixed choice; the **shape** — opaque resolver, signed verdict,
verified deterministic re-entry — is the production one. The test
`oracle_panel_authority_is_a_quorum_contract` closes the loop: the panel's own
authority to issue a verdict is itself a 2-of-3 `Quorum` contract (Spirit
`vhs2`: "resolves through one of those identity contracts").

## Tests — what each one proves (13 total, all pass)

| Test | Proves |
|---|---|
| `public_key_is_the_identity_atom` | (1) a key's signature verifies against it + the message, and against nothing else |
| `quorum_two_of_three` | (2a) 2-of-3 authorizes with 2 sigs; denies with 1, reason `QuorumShort{required:2, satisfied:1}` |
| `unsatisfiable_quorum_is_a_construction_error` | k>n rejected at construction, typed error |
| `duplicate_signatures_do_not_satisfy_quorum` | one member signing twice ≠ 2 distinct signers |
| `timelock_denies_before_and_allows_after` | (2b) denied at tick 49 (`OutsideTimeWindow`), authorized at tick 50 |
| `timelock_window_closes` | window also expires at `not_after` |
| `time_varying_threshold_relaxes_over_elapsed_time` | (2c) needs 3 sigs early, 1 sig after 100 ticks elapsed |
| `time_varying_threshold_can_tighten_over_time` | mirror: 1 early, 3 late (decaying delegation) |
| `empty_schedule_is_a_construction_error` | empty schedule rejected, typed error |
| `composed_rule_reports_typed_reasons` | (3) `All(quorum, timelock)` reports the first failing reason; authorizes when both hold |
| `divergence_resolves_via_stub_oracle` | (4) unresolved → denied; oracle resolves; signed verdict re-enters via `admit` → authorized |
| `resolution_from_wrong_signer_is_rejected` | impostor verdict rejected at re-entry, `ResolverMismatch` |
| `oracle_panel_authority_is_a_quorum_contract` | the oracle panel's own authority is a 2-of-3 quorum contract |

## Real cargo output (verbatim)

```
===== cargo --version =====
cargo 1.96.0 (30a34c682 2026-05-25)
===== cargo build (clean) =====
     Removed 173 files, 32.0MiB total
   Compiling criome-poc v0.1.0 (/tmp/criome-poc)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.28s
===== cargo test =====
   Compiling criome-poc v0.1.0 (/tmp/criome-poc)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.28s
     Running unittests src/lib.rs (target/debug/deps/criome_poc-2b5fb0ad7e89430c)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/policy_language.rs (target/debug/deps/policy_language-512d5daa262a7dcc)

running 13 tests
test composed_rule_reports_typed_reasons ... ok
test divergence_resolves_via_stub_oracle ... ok
test empty_schedule_is_a_construction_error ... ok
test duplicate_signatures_do_not_satisfy_quorum ... ok
test oracle_panel_authority_is_a_quorum_contract ... ok
test public_key_is_the_identity_atom ... ok
test quorum_two_of_three ... ok
test resolution_from_wrong_signer_is_rejected ... ok
test time_varying_threshold_can_tighten_over_time ... ok
test time_varying_threshold_relaxes_over_elapsed_time ... ok
test timelock_denies_before_and_allows_after ... ok
test timelock_window_closes ... ok
test unsatisfiable_quorum_is_a_construction_error ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests criome_poc

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

===== cargo clippy --all-targets =====
    Checking criome-poc v0.1.0 (/tmp/criome-poc)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.21s
```

Clippy runs under `[lints.clippy] all = "deny"` in `Cargo.toml`, so the clean
finish means zero clippy findings across lib and all test targets. (One finding
was caught and fixed during development: a `collapsible_if` in `Timelock::
evaluate`, resolved with an edition-2024 let-chain.)

## What this PoC does and does not claim

- **Does:** demonstrate the full evaluation LOGIC of the limited policy
  language — atoms, quorum, time-lock, time-varying threshold, typed outcome,
  divergence re-entry — as runnable, tested, clippy-clean Rust under the
  workspace discipline.
- **Does not:** use real BLS (stubbed deterministically), persist to a SEMA
  family, expose a wire verb, or parse NOTA. Those are integration steps:
  swapping `identity` for `blst` min-pk over criome's `AttestationPreimage`,
  adding a `criome-contract` SEMA family (report 1 gap #1), wiring a
  define/amend-contract verb on the meta plane (gap #5), and generating the
  types from the file-6 NOTA schema so these methods attach to schema-emitted
  nouns. The PoC's type shapes are chosen to make that swap mechanical.

## Open questions carried forward (to file 8)

1. **File 5 is missing.** This PoC stands in for its vocabulary; the design
   author should confirm the `Rule` variant set and naming
   (`TimeVaryingThreshold` vs the in-tree binary `TimeSwitch`;
   `Agreement`/`Resolution`/`ResolutionFact` naming).
2. **Determinism strength of the oracle (report 4 §B.4 residual).** The PoC
   takes the attestation-first posture: verify a signed verdict, never
   re-execute. Whether criome needs bit-reproducible re-execution as a dispute
   backstop is unresolved and sets the cost of the whole reconciliation path.
3. **Time source.** The PoC uses an engine-supplied `LogicalClock`. Confirm this
   maps to criome's `TimestampNanos` / SEMA-stamped clock and that no VDF is
   wanted for the adversarial dispute case.
```
