# 694 — cluster-propagation PoC: adversarial verification

Independent verification of the implement phase's claim that the
cluster-propagation PoC at `/tmp/cluster-propagation-poc` is built and green.
Method: run the suite myself; read every test and the upstream component source
at the pinned revs; mutation-probe each load-bearing assertion in a throwaway
copy (`/tmp/cpp-verify`, since deleted) to confirm the green is falsifiable, not
hollow.

## Observed suite result (run by the verifier)

`cargo build` → `Finished dev profile` clean, **0 warnings**.
`cargo test` → **4 passed, 0 failed, 0 ignored** across 4 binaries:

```
lib unittests                                                  0 passed
criome_quorum::criome_authorizes_two_of_three_and_rejects_one_of_three  ok
end_to_end::cluster_propagation_three_spirits_interchangeable           ok
router_fanout::router_fans_authorized_head_by_type_to_matching_attendees_only  ok
spirit_propagation::spirit_a_accepts_ships_and_b_c_acquire_interchangeable     ok
doc-tests                                                      0 passed
```

The reported green is real and reproducible. No `#[ignore]`, no `should_panic`,
no `assert!(true)`, no `todo!()`/`unimplemented!()` in `src/` or `tests/` (the
one `todo!` string is a stale doc-comment in `end_to_end.rs:12`; the actual stub
was removed and the e2e wires `producer.head_digest()` at `end_to_end.rs:79`).

## Per-hop verdict (real vs shimmed)

### HOP 1 — criome 2-of-3 root-contract authorize — PROVEN REAL

Verified against criome `22801af` source:

- `is_valid_majority` is a genuine k>n/2 guard:
  `required != 0 && required <= authorities && required > authorities / 2`
  (`criome/src/language.rs:623-626`). 2-of-3 passes (`2 > 1`); 2-of-5 fails
  (`2 > 2` false). Fired at admission `validate_shape` (`:414`) and at the
  time-quorum (`:577`).
- `Threshold::decide` is a real **distinct-signer** tally
  (`language.rs:371-395`): counts `is_satisfied(member) && !already_counted`,
  authorizes only on `satisfied >= required`, else `QuorumShort{required,
  satisfied}`.
- `has_valid_signature_from` (`language.rs:520-535`) requires the signer's key
  to be **admitted in the registry**, reconstructs the canonical
  `OperationStatement` bytes bound to `(identity, operation_digest, stamp)`, and
  calls `verify_bls`. A signature over digest X cannot satisfy a quorum
  evaluating digest Y.
- `verify_bls` (`master_key.rs:130`) is real `blst` BLS12-381 min-pk:
  `parsed_signature.verify(...) == BLST_ERROR::BLST_SUCCESS`. Not a stub.
- The `ermr` admission gate is enforced in the registration handler
  (`actors/registry.rs:100-104`): with a cluster root configured, an
  un-admitted identity is rejected `UnauthorizedRegistration`. `ClusterRoot::
  admits` (`admission.rs:86-100`) verifies the cluster-root BLS signature over
  the `RegistrationStatement`.
- The criome unit test additionally asserts `reference.digest ==
  head.object_digest()` (`criome_quorum.rs:118-122`) — the criome authorized
  **exactly** the digest D it was given. `OperationDigest::from_bytes` is
  `blake3::hash(bytes).to_hex()` (signal-criome `521a8ed` lib.rs:59-60,79).

Mutation probe (verifier): made the 2-of-3 evidence sign with member A **twice**
instead of A+B. OBSERVED: the real tally returned
`Rejected(QuorumShort{required:2, satisfied:1})` and the `Authorized` assert
FAILED at `src/criome_quorum.rs:340`. This proves the quorum dedups by distinct
signer — it is not a raw-signature count and not a hard-coded `true`. Combined
with the test's own two negatives (2-of-5 rejected `ThresholdUnsatisfiable` at
admission; 1-of-3 rejected `QuorumShort`), the 2-of-3 is genuinely falsifiable.

### HOP "router by type" — PROVEN REAL

Verified against router `ce578f1` + signal-standard `0b7ae20`:

- `RouterRuntime` forwards `AttendAuthorizedObjects` and
  `PublishAuthorizedObjectReference` to the real `AuthorizedObjectFanout`
  (`router/src/router.rs:1580,1610`).
- `AuthorizedObjectFanout::publish` (`authorized_object.rs:118-135`) **filters**
  subscriptions by `publication.reference.matches_interest(&token.interest)` and
  returns only the matched set in `publication.deliveries`. Not a broadcast.
- `matches_interest` (signal-standard `lib.rs:70-79`) is a real type-lattice:
  `Any => true`, `Component(c) => component-eq`, `ObjectKind(k) => kind-eq`,
  `ComponentObject => both-eq`.

The standalone `router_fanout` test exercises all four match rungs + a
load-bearing negative (Mirror control excluded), asserts an exact count (4 of
5), asserts reference-not-payload, and a second adversarial witness ({Mirror,
Contract} head fans to a *different* set of 2). This is a strong, real
type-matcher proof — the design's "shim the lattice match" RED-fallback was not
needed.

### HOP "spirit accept → ship" and "B/C acquire → interchangeable" — PROVEN REAL (in-process)

Verified against spirit `fe04c12` / mirror `b26c139` / sema-engine `73eea24`:

- A real `spirit::Engine` accepts `Input::record`, commits to the
  content-addressed log; real `Store::checkpoint`; real
  `ship_unshipped_to_mirror` over **real loopback TCP** to a **real mirror
  daemon**; real `publish_checkpoint_to_mirror`.
- B and C each call `acquire_into` → a real mirror `Restore` exchange
  (`mirror/src/store.rs:510` `load_restore` returns the latest checkpoint row +
  entry suffix, rejects `NoCheckpoint`/`UnknownStore` when nothing is shipped)
  → `Store::import` (`spirit/src/store/mod.rs:382`) which opens a **brand-new**
  SemaDatabase and ingests the bundle. B/C are NOT pre-set to A's state.
- The interchangeability witness `Store::database_marker()`
  (`store/mod.rs:1138`) is a real content hash: `state_digest` is blake3 over
  every committed record's `(identifier, archived bytes)` + referents folded
  with the commit sequence; empty store → 0.

Mutation probe (verifier): moved B/C's `acquire_into` to run **before** A ships.
OBSERVED: `RestoreRejected(RestoreRejection { reason: NoCheckpoint })` and the
test FAILED at `src/spirit_propagation.rs:102`. This proves the acquire genuinely
depends on A having shipped — B/C are restored from A's data, not pre-loaded. The
spirit test's own falsifiability guards (post-accept marker ≠ genesis; acquired
marker ≠ genesis) are load-bearing, consistent with the implementer's reported
`marker(B)==genesis` mutation (`StateDigest(2236392434272497022)`).

## The one real architectural seam (honest gap, not fakery)

**The router type-fanout and the acquire are decoupled in the e2e.** The test
asserts two facts that are each individually real, but as **co-occurrence, not
causation**:

1. The router delivers the D-bearing reference to B and C **by type**
   (`end_to_end.rs:118-137`, against the real matcher).
2. B and C **can** acquire from the mirror and become interchangeable with A
   (`end_to_end.rs:140-155`, against the real engine/mirror).

But `acquire_into(&self, path: PathBuf)` takes **only a path** — it restores by
the constant `SPIRIT_STORE_NAME` (`spirit_propagation.rs:37,92-119`) and never
consults the router-delivered reference or the digest D. The digest D flows
through the AUTHORIZE half (spirit head → `head_digest()` → criome evidence →
authorized reference → glue → router fan) and is what the 2-of-3 quorum signs;
it is **not** the key the mirror restore looks up on.

Mutation probe (verifier): gave B and C **non-matching** router interests
(Mirror / Time) in the e2e. OBSERVED: the test FAILED at the router-delivery
assertion (`end_to_end.rs:131`, "attendee B matched the Spirit head") and
panicked **before** reaching the acquire — confirming (a) the router-match
asserts are load-bearing, and (b) the acquire is not gated on the router
delivery. If the acquire had been driven by the delivery set, the failure would
have surfaced at the interchangeable asserts instead.

This is a faithfully-disclosed cut, not a deception: the implementer named it in
three of five step blockers ("the acquire path restores by store-name … D is
load-bearing for the criome AUTHORIZE side … not itself the key the mirror
restore lookups on"). Every hop runs against real component code; what the e2e
does **not** prove is the end-to-end **causal wiring** "router delivery of the
D-bearing reference drives B/C to fetch exactly D." Closing it is an operator
bead: make `acquire_into` consume the delivered reference's digest and restore
by D (content-addressed), so a wrong/absent delivery would break the acquire.

## Other cuts (disclosed, consistent with the design / 684)

Single host (3 in-process instances), loopback in place of cross-host sockets;
local self-quorum in place of cross-criome peer signature solicitation (p3td,
keys co-resident); harness-minted cluster-root admissions through the real ermr
gate (684 Woe 6); fresh `Store::import` in place of live `Store::adopt_head`;
main-HEAD synchronous delivery in place of the durable attendance-fanout-139
branch; per-signature verify in place of BLS aggregation. The whole loop is
pinned to the OLD schema chain (schema-rust-next `733b76d3`) via a path-`[patch]`
table to `/tmp/cpp-deps`; the NEW-chain `bb4dfe29` in `cargo tree -d` is
**build-deps-only** (proc-macro/codegen), zero runtime reverse-deps (verified
`cargo tree -i … --edges normal` prints nothing) — benign, the runtime type
graph is a single OLD-chain source.

## Verdict — PartialGreen

The suite is genuinely green (4/4, verified) and every individual hop is proven
real against the pinned component crates with falsifiable mutation probes:
criome 2-of-3 is a real distinct-signer BLS quorum bound to the head digest;
the router fans strictly by type; spirit ship→acquire moves real
content-addressed state and B/C are restored from A's data, not pre-set. No
fakery (no stubbed asserts, no hard-coded equality, no broadcast masquerading as
a match). The one honest shortfall is the e2e's third→fourth **coupling**: the
type-fanout and the acquire are asserted as co-occurring real facts rather than
a wired causal chain (the acquire restores by store-name, ignoring the delivered
D-bearing reference). That single seam is why this is PartialGreen rather than
fully LoopProvenGreen — and it is exactly the operator harvest bead the design
already anticipated.
