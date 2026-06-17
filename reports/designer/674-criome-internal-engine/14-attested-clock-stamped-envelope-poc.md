# 674.14 — attested-clock stamped envelope (crystallized-past time, G3/G4 PoC)

*Builds the one genuine triad misfit from 674.13 — the clock — into the
content-addressed + real-BLS policy-language prototype. Implements Spirit `ay3y`'s
crystallized-past attested time: every operation carries its own quorum-attested
crystallized time stamp, and the evaluator reads no ambient `SystemTime::now()`.
Worktree: `~/wt/github.com/LiGoldragon/criome/language-content-addressed-bls`
(branch `language-content-addressed-bls`, off criome main, G1+G2 at `b97db6b`).
Not pushed; criome main untouched.*

## The misfit this closes

674.13's adversarial pass overturned the optimistic rating of the clock (#34): the
deployed daemon reads `SystemTime::now()` from a held `SystemClock`, an ambient
non-deterministic side-input the triad models as *no engine*, sitting inside a
NEXUS verify body with no owner. The G1+G2 prototype papered over it with a
caller-supplied `Evidence.observed_at` — which a verifier cannot trust: a caller can
assert any time it likes. This rung removes both.

## The model (`ay3y`, crystallized past)

An **`AttestedMoment`** is a quorum-attested *crystallized past* time object:

1. It begins as a **proposition** of a forward-extending window `[start, end]`
   (`TimeWindow`) under a `TimeQuorum` (a set of admitted authority identities + a
   k-of-n threshold). "A time authority is just another criome quorum object."
2. Its **identity** is the blake3 content address of the `(window, quorum)`
   proposition — `AttestedMoment::digest`, tagged `CRIOME-ATTESTED-MOMENT-V1`. The
   signatures are *not* part of the address: the same proposition has one identity
   whether sub-quorum or crystallized, and a tampered window is a different object.
3. A **quorum signs** it — each authority a real BLS `SignatureEnvelope` over a
   domain-tagged `TimeWindowStatement` preimage (`CRIOME-TIME-WINDOW-V1`), produced
   by the deployed `MasterKey::sign` and verified by the deployed
   `VerifyBls::verify_bls`. No honor-system membership anywhere.
4. It **crystallizes** once the count of *distinct admitted authorities with a
   really-verifying signature* reaches the threshold. A crystallized moment is a
   non-forgeable **monotonic lower bound**: it proves `now >= end`, because real time
   is always farther than the window every quorum member could sign before it closed.
   Only the past is provable — a sub-quorum, an unsigned, or a forged-signature
   window is **not** a time proof.

`Evidence` drops `observed_at` and instead carries an `AttestedMoment` stamp. The
evaluator's only source of "now" is `Evidence::crystallized_now(registry)`, which
returns `Option<CrystallizedMoment>` — `None` when the stamp's quorum is not met by
verifying signatures. There is no `SystemTime::now()` in the evaluation path.

## Key code

The crystallization gate — the whole non-forgeability claim lives here:

```rust
pub fn crystallize(&self, registry: &KeyRegistry) -> Option<CrystallizedMoment> {
    let statement = TimeWindowStatement::new(&self.window).to_signing_bytes();
    let mut satisfied: Vec<&Identity> = Vec::new();
    for attestation in &self.signatures {
        if !self.quorum.admits(&attestation.authority) { continue; }     // non-member: ignored
        if satisfied.contains(&&attestation.authority) { continue; }     // dedup distinct authorities
        if attestation.verifies(&statement, registry) {                  // real BLS over the window
            satisfied.push(&attestation.authority);
        }
    }
    let reached = satisfied.len() as u64 >= u64::from(self.quorum.required_signatures.into_u16());
    reached.then_some(CrystallizedMoment { window_end: self.window.end })
}
```

`TimeAttestation::verifies` reuses the exact `SignedBy` discipline — resolve the
authority to its admitted key, require envelope key == admitted key, require the
implemented scheme, then deployed `verify_bls`:

```rust
fn verifies(&self, statement: &[u8], registry: &KeyRegistry) -> bool {
    let Some(admitted_key) = registry.public_key(&self.authority) else { return false; };
    matches!(self.envelope.scheme, SignatureScheme::Bls12_381MinPk)
        && &self.envelope.public_key == admitted_key
        && admitted_key.verify_bls(&self.envelope.signature, statement)
}
```

The time-lock arms now check the operation's OWN crystallized stamp; an unproven
stamp is `TimeNotProven`, distinct from a stamp that simply does not clear the
boundary (`OutsideTimeWindow`):

```rust
Self::ActiveAfter(timed_rule) => match evidence.crystallized_now(registry) {
    None => Ok(Decision::Rejected(RejectionReason::TimeNotProven)),
    Some(now) => if now.proves_at_or_after(timed_rule.boundary()) {
        Ok(timed_rule.decide(evidence, registry))
    } else { Ok(Decision::Rejected(RejectionReason::OutsideTimeWindow)) },
},
```

## The after/until asymmetry — and why it resolves cleanly

A crystallized stamp proves only a **lower bound** on now (`now >= end`). The two
time-lock directions therefore read the *same* `window_end`, but ask different
questions of it, both honestly answerable from a lower bound:

| Rule | Holds iff | Method | Why a lower bound can answer it |
|---|---|---|---|
| `ActiveAfter(T)` (release-after-T) | stamp proves `now >= T` | `window_end >= T` | The proven lower bound already sits at/past T, so `now >= T` is established. |
| `ActiveUntil(T)` (active-until-T) | the operation's window **closed** at/before T | `window_end <= T` | The stamp is honest about its own closing edge: a window that closed at `window_end <= T` is a proof-of-when that sits within the still-active interval. |

The resolution is that **the operation carries its own proof-of-when**. We never ask
"is the live present before T?" — a lower bound cannot prove that, and crystallized
past is explicitly only-the-past. We ask "did this operation's *attested window*
close before T?", which is a statement about the past edge the stamp does prove.
`TimeSwitch` selects the tighter `after` threshold only when the stamp proves the
boundary is past, defaulting to the looser `before` regime otherwise — the
tightening fires on genuine proof, never on an unproven gap.

## Verification — verbatim

`cargo build`:

```
   Compiling criome v0.1.1 (/home/li/wt/github.com/LiGoldragon/criome/language-content-addressed-bls)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.00s
```

`cargo test` (all suites):

```
     Running unittests src/lib.rs
test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running unittests src/bin/criome-daemon.rs
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/actor_discipline_truth.rs
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
     Running tests/daemon_skeleton.rs
test result: ok. 20 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.05s
     Running tests/language.rs
running 20 tests
test acyclicity_enforced ... ok
test digest_is_stable_and_distinguishes_contracts ... ok
test explicit_policy_can_escalate_to_psyche ... ok
test missing_reference_during_evaluation_is_a_typed_error ... ok
test schema_sketch_names_every_construct ... ok
test forged_signature_rejected ... ok
test any_prefers_authorization_before_escalation ... ok
test agreement_requires_a_quorum_signed_reconciliation_fact ... ok
test escalation_composes_through_all_after_required_rules_authorize ... ok
test real_bls_authorizes ... ok
test forged_time_signature_rejected ... ok
test subquorum_moment_is_not_a_time_proof ... ok
test object_member_composes_a_sub_contract_into_a_quorum ... ok
test content_addressed_sharing ... ok
test quorum_two_of_three_with_real_signatures ... ok
test timelock_release_with_real_signature ... ok
test active_until_t_via_stamp ... ok
test crystallized_moment_is_a_lower_bound ... ok
test timelock_release_after_t_via_stamp ... ok
test time_switch_tightens_quorum_after_boundary ... ok
test result: ok. 20 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
   Doc-tests criome
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Total **53 tests, 0 failures**. The five required new tests are
`crystallized_moment_is_a_lower_bound`, `subquorum_moment_is_not_a_time_proof`,
`forged_time_signature_rejected`, `timelock_release_after_t_via_stamp`,
`active_until_t_via_stamp`; the two prior time tests
(`timelock_release_with_real_signature`, `time_switch_tightens_quorum_after_boundary`)
were rewritten onto real crystallized stamps; all prior G1/G2 tests stay green.

`cargo clippy --all-targets -- -D warnings`:

```
    Checking criome v0.1.1 (/home/li/wt/github.com/LiGoldragon/criome/language-content-addressed-bls)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.12s
```

(Two lints — `manual_contains`, `unnecessary_lazy_evaluations` — surfaced and were
fixed before this clean run.) Nix skipped per brief.

## Proven vs deferred — honest table

| Claim | Status | Evidence / note |
|---|---|---|
| A quorum-signed window crystallizes into a lower bound `now >= end` | **PROVEN** | `crystallized_moment_is_a_lower_bound` (full + exact-threshold quorum). |
| A sub-quorum window is not a time proof | **PROVEN** | `subquorum_moment_is_not_a_time_proof` → `TimeNotProven`. |
| A forged / non-admitted-key window signature does not count | **PROVEN** | `forged_time_signature_rejected` — same no-honor-system path as `SignedBy`. |
| `ActiveAfter(T)` over the carried stamp (release-after-T) | **PROVEN** | `timelock_release_after_t_via_stamp` (before/at/after T). |
| `ActiveUntil(T)` over the carried stamp (window closed before T) | **PROVEN** | `active_until_t_via_stamp` (within/at/expired). |
| Evaluator reads no ambient `SystemTime::now()` | **PROVEN** | No clock in the evaluation path; "now" = `Evidence::crystallized_now`. The daemon's `SystemClock` in `master_key.rs` is untouched and out of the language path. |
| Moment identity = content address of `(window, quorum)` | **PROVEN** | `crystallized_moment_is_a_lower_bound` asserts digest equality across signature counts and inequality across windows. |
| Window-end binding is non-malleable | **PROVEN** | `TimeWindowStatement` covers both bounds under a domain tag; moving `end` breaks every signature. |
| Stamp is on the language `Evidence` (a triad *input*) | **PROVEN** | `Evidence.stamp: AttestedMoment`. |
| Stamp on triad *outputs* (replies/attestations carry their own crystallized time) | **DEFERRED** | `ay3y` says "every triad input and output"; this PoC stamps the input. Output-side stamping (and the deployed `Attestation.issued_at`/`expires_at` migration off `SystemClock`) is the next step. |
| Window **expiry** close (close at window-end if quorum not yet reached) | **DEFERRED** | Crystallization here is purely quorum-reached. The "closes at last signature OR at window expiry" expiry path is modeled in prose only; no wall-clock exists in the language to enforce expiry, and that is correct — expiry is itself a later attested-moment comparison. |
| Partition/divergence widening the tolerance gap | **NOT MODELED** | `ay3y` notes the gap widens under partition; the PoC has no network, so this is descriptive only. |
| `criome-contract` / attested-moment SEMA family | **DEFERRED (G10)** | The store is still the in-memory `ContractStore`/`KeyRegistry` `Vec` stand-in from 674.13 #14; no SEMA family minted. The time-authority quorum reuses the same in-test `KeyRegistry`. |
| Schema is *generated* code | **DEFERRED** | `schema/criome.language.schema` is updated as design-pressure (now naming `TimeWindow`/`TimeQuorum`/`AttestedMoment`/`TimeAttestation`/`TimeNotProven`); the Rust is still hand-written, not emitted. Matches `t5wx`/`d3r2`: the evaluator body is legitimately hand-written; the *types* being hand-written is the deferred part. |

## Files

- `src/language.rs` — `TimeWindow`, `TimeQuorum`, `TimeWindowStatement`,
  `AttestedMoment`, `TimeAttestation`, `CrystallizedMoment`; `Evidence` re-shaped
  (`stamp` replaces `observed_at`); time-lock + `TimeSwitch` arms over the stamp;
  `TimeNotProven` rejection reason.
- `tests/language.rs` — `TimeAuthorities` test harness; five new tests; two time
  tests rewritten; non-time tests carry an honest `untimed()` proposition.
- `schema/criome.language.schema` — attested-clock nouns + `TimeNotProven`.
- `INTENT.md` — the settled design direction (vhs2 / z9d6 / t5wx,d3r2,xbc2 / gc0n /
  ay3y).
