# 680 · The integrated agreement-machine PoC — built, compiled, tested green

A self-contained, zero-dependency Rust crate that runs the whole loop from
design report `1-design.md`: admit a contract, evaluate it under a
membership-scoped quorum, stamp it with a crystallized-past attested moment,
pulse the *reference* (not the payload), and fan that reference out to
subscribed components by the single shared **component-differentiator**
vocabulary — plus the contract-scheduled heartbeat.

Crate: `/tmp/telos-poc` (throwaway, committed nowhere). 11 source modules +
5 integration-test files, ~1730 lines. Built and tested with the profile
toolchain (`cargo 1.96.0`, `clippy 0.1.96`).

## Result: 15 tests pass, 0 fail; clippy clean under `-D warnings`

```
test result: ok. 3 passed; 0 failed  (attested_moment.rs)
test result: ok. 3 passed; 0 failed  (differentiator_fanout.rs)
test result: ok. 1 passed; 0 failed  (end_to_end.rs)
test result: ok. 4 passed; 0 failed  (heartbeat.rs)
test result: ok. 4 passed; 0 failed  (quorum_membership.rs)
Doc-tests telos_poc: ok. 0 passed; 0 failed
```

`cargo clippy --all-targets -- -D warnings` → `Finished` (exit 0). Verbatim
output at the end of this report.

## What each test proves (the five demands)

| # | Demand | Test file | Tests |
|---|---|---|---|
| 1 | Quorum scoped by membership | `quorum_membership.rs` | self-quorum 2-of-3, multi-party 2-of-3, 1-sig fails, non-member sig doesn't count |
| 2 | Attested moment | `attested_moment.rs` | quorum-signed window proves a lower bound; sub-quorum is no proof; wrong-window sigs don't attest |
| 3 | Contract-scheduled heartbeat | `heartbeat.rs` | clock past T with no event fires; intervening event suppresses; not-yet-due retains; non-matching event doesn't suppress |
| 4 | Component-differentiator fan-out | `differentiator_fanout.rs` | match rule total over the lattice; reference delivered to matching subscribers only; close stops delivery |
| 5 | End-to-end | `end_to_end.rs` | admit → evaluate(quorum+stamp) → emit reference → fan by differentiator → matching component fetches; non-matching gets nothing |

## The design's core finding, in code

The differentiator is `(ComponentKind, AuthorizedObjectKind)` — and the match
is one total function over the closed interest lattice (`src/differentiator.rs`):

```rust
pub fn matches(&self, interest: &AuthorizedObjectInterest) -> bool {
    match interest {
        AuthorizedObjectInterest::AnyAuthorizedObject => true,          // the universe
        AuthorizedObjectInterest::Component(component) => self.component == *component, // a row
        AuthorizedObjectInterest::ObjectKind(kind) => self.kind == *kind,              // a column
        AuthorizedObjectInterest::ComponentObject(cell) => self == cell,               // one cell
    }
}
```

The reference projects to its differentiator for free — no new wire field, the
load-bearing observation of design §1 (`src/contract.rs`):

```rust
impl From<&AuthorizedObjectReference> for Differentiator {
    fn from(reference: &AuthorizedObjectReference) -> Self {
        Differentiator::new(reference.component, reference.kind)
    }
}
```

The load-bearing change — interest moved INTO the subscription token, turning
the router's table from fan-to-everyone into a matchable table
(`src/router.rs`):

```rust
pub fn publish(&self, update: &AuthorizedObjectUpdate) -> Vec<Delivery> {
    let differentiator = update.differentiator();        // computed once
    self.tokens
        .iter()
        .filter(|token| differentiator.matches(&token.interest()))
        .map(|token| Delivery { subscriber: token.subscriber(), reference: *update.object() })
        .collect()
}
```

One `Threshold` evaluator serves both quorum modes; only membership differs —
the evaluator counts *distinct satisfied members* and never branches on
self-vs-multi (`src/quorum.rs::Threshold::evaluate`). The heartbeat's
"intervening event" is literally a differentiator match against the check's
`absent` interest (`src/heartbeat.rs`):

```rust
pub fn was_contradicted(&self, log: &[AuthorizedObjectUpdate]) -> bool {
    log.iter().any(|update| update.differentiator().matches(&self.absent))
}
```

— resolving design open-question Q3 ("no intervening event" = "no update
matching that interest") concretely in the test
`a_non_matching_event_does_not_suppress`.

## Module map

```
src/
  differentiator.rs  ComponentKind, AuthorizedObjectKind, Differentiator,
                     AuthorizedObjectInterest + the total matches() rule        [§1]
  quorum.rs          Threshold + membership-blind evaluate(); Principal scopes
                     self vs multi; counts distinct satisfied members           [§2]
  moment.rs          TimeWindow, AttestedMoment::attest() (quorum-gated),
                     proven_lower_bound / proves_reached — crystallized past    [ay3y]
  contract.rs        Contract/Rule, AuthorizedObjectReference + From → Differentiator,
                     AuthorizedObjectUpdate::differentiator()                    [§1,§3]
  criome.rs          CriomeCore: admit_contract, store_object,
                     evaluate_authorization (quorum + stamp + emit reference)   [§0,wckt]
  router.rs          SubscriptionTable: open/close (per-(id,interest)) / publish
                     (fan reference to matched only)                            [§1,wckt]
  component.rs       Component: receive(reference) then fetch(body by digest)   [m0p2]
  heartbeat.rs       ContractTimeCheck + Heartbeat: schedule / observe / run_due
                     (fire on absence, suppress on intervening match)           [§3,m0p2]
  store.rs           ObjectStore: content-addressed get/put; FNV digest         [z9d6]
  signature.rs       PublicKey/SecretKey/Signature — deterministic stub
  error.rs           one typed crate Error enum (hand-written Display/Error)
```

## What is stubbed (honestly)

- **The signature scheme** (`signature.rs`). NOT cryptography: a "signature" is
  a deterministic mix of (secret, message); verify recomputes it. This mirrors
  the router's own `AcceptFixedTestIdentity` test signer. What is real and
  load-bearing: a signature binds a specific signer to a specific message, and a
  wrong signer / wrong message fails — which is all the quorum evaluator needs to
  count distinct satisfied members honestly. Production swaps in BLS.
- **The store** (`store.rs`). In-memory `HashMap<ObjectDigest, _>`, not redb +
  rkyv. The content address is a real FNV-1a digest over the bytes, so equal
  bodies share a digest — the push-reference / pull-body shape is genuine.
- **The router / fan-out** (`router.rs`, `component.rs`). In-process: `publish`
  returns a `Vec<Delivery>` the test hands to components, rather than a socketed
  daemon. The match-and-deliver LOGIC is exactly the deployed shape; only the
  transport is collapsed.
- **CriomeCore as a struct, not a kameo actor.** Zero-dep constraint. It is
  still a single data-bearing noun owning the contract table + store, one method
  per verb — the same logical shape an actor would carry.

Nothing about the *logic* the design turns on is faked: membership-scoped
quorum, attested-moment lower bound, heartbeat fire/suppress, and
differentiator fan-out are all real and tested.

## Discipline adherence

Methods on data-bearing types only (no free fns outside `#[cfg(test)]`); typed
domain newtypes (`ObjectDigest`, `TimestampNanos`, `PublicKey`,
`RequiredSignatures`, `SubscriberIdentity`); private wrapped fields with
method access; one typed per-crate `Error` enum (hand-written `Display`/`Error`
since zero-dep precludes `thiserror`); the match rule named as the
enum-vs-enum contact point. Clippy clean under `-D warnings`.

## Open questions for the psyche (unchanged from design, now grounded)

1. **Differentiator granularity** — PoC built coarse:
   `(ComponentKind, AuthorizedObjectKind)`. A third named-function axis would
   make `Differentiator` a triple; trivial to add (one field + one match arm).
2. **Token identity / retraction** — PoC implements per-(identity, interest)
   retraction (`SubscriptionTable::close` removes the whole token); test
   `closing_a_subscription_stops_its_deliveries` confirms.
3. **Heartbeat "intervening event" scope** — PoC implements "no update matching
   `absent`'s interest"; test `a_non_matching_event_does_not_suppress` confirms
   a different-class event does not suppress.

## Verbatim — `cargo test`

```
   Compiling telos-poc v0.1.0 (/tmp/telos-poc)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.56s
     Running unittests src/lib.rs

running 0 tests
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/attested_moment.rs

running 3 tests
test a_sub_quorum_window_is_not_a_valid_time_proof ... ok
test quorum_signed_window_proves_a_lower_bound_on_now ... ok
test signatures_over_the_wrong_window_do_not_attest ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/differentiator_fanout.rs

running 3 tests
test closing_a_subscription_stops_its_deliveries ... ok
test fanout_delivers_the_reference_to_matching_subscribers_only ... ok
test the_match_rule_is_total_over_the_lattice ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/end_to_end.rs

running 1 test
test admit_evaluate_stamp_pulse_fan_fetch ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/heartbeat.rs

running 4 tests
test a_non_matching_event_does_not_suppress ... ok
test a_check_not_yet_due_does_not_fire_and_is_retained ... ok
test an_intervening_event_before_t_suppresses_the_firing ... ok
test clock_advancing_past_t_with_no_intervening_event_fires_acceptance ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/quorum_membership.rs

running 4 tests
test multi_party_quorum_two_of_three_distinct_principals_authorizes ... ok
test a_non_member_signature_does_not_count ... ok
test one_signature_falls_short_of_two_of_three ... ok
test self_quorum_two_of_three_of_one_principal_authorizes ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests telos_poc

running 0 tests
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

## Verbatim — `cargo clippy --all-targets -- -D warnings`

```
    Checking telos-poc v0.1.0 (/tmp/telos-poc)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
```

(exit 0)
