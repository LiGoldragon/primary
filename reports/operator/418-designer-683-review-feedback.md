# Operator Review - Designer 683

Reviewed:

- `reports/designer/683-design-review-and-networking/0-frame-and-method.md`
- `reports/designer/683-design-review-and-networking/3-review-and-networking.md`
- current `criome`, `signal-criome`, `signal-router`, and nearby signal-frame schemas/code

## Verdict

Designer 683 is worth keeping. The core architecture is the right shape:
criome has a direct peer lane for time-sensitive agreement, router remains the object and
component transport, and the split is by cargo, not by topology.

The most valuable corrections in the report are also real: the attested moment cannot
crystallize at the k-th signature after the fact, and sub-majority time quorums are not
fork-safe. Those should shape the next implementation slice.

One reported blocker is stale against current `criome`: duplicate quorum members are already
rejected at admission, and duplicate operation signatures do not count twice.

## Points To Keep

Keep the two-lane invariant.

The direct criome lane should carry only agreement-plane messages:

- quorum signature solicitation
- quorum signature contribution
- time-window attestation
- divergence/adjudicator agreement messages
- peer admission/handshake material

It should not carry component payloads or object bodies. Router remains the transport for
object/component delivery. This is the right implementation of `lt44`: criome gets a direct
agreement lane without becoming a general router.

Keep the attested-clock correction.

The current signed preimage includes the `TimeWindow { opens_at, closes_at }`. That means the
window must be proposed before the first signature. It cannot close at "the time the k-th
signature arrived" unless that close time was already in the signed proposition.

So the correct model is:

1. propose a forward-extending window
2. collect quorum signatures attesting "now is inside this window"
3. once accepted, use it as crystallized past: `now >= closes_at`

The direct lane still helps, but the claim changes. It helps by making the proposer confident
that a tighter window can collect signatures before expiry. It does not make the object
retroactively measure its own collection completion.

Keep the partition warning.

Current `AttestedMoment` validation checks non-empty threshold, threshold within authority
count, and duplicate authorities. It does not enforce `required > authorities.len() / 2`.
For a time authority that is supposed to prevent two disjoint groups from both producing
valid moments, majority quorum must be a typed invariant, or the object family must be
explicitly labeled sub-majority and not fork-safe.

Keep the "EscalateToPsyche is partial" warning.

`EscalateToPsyche` exists as an evaluation result, but there is no protocol yet for naming
an adjudicator, submitting a signed verdict, verifying that verdict, and completing the
ladder. Treat the three-valued decision as landed vocabulary, not a complete adjudication
system.

Keep the router-sole matcher lean.

For object-update fanout, the cleanest split remains:

- criome authorizes and stamps object references
- router owns subscription matching and delivery
- components subscribe by differentiator/interest

A criome-local registry can exist only as local observation/cache state. It should not be a
second operational matcher unless the psyche explicitly chooses duplicate ownership.

## Correction

Designer 683 says quorum-member distinctness is still uncorrected and that a duplicate key
can satisfy a 2-of-2. That is not true in current `criome`.

Current code already rejects duplicate `PolicyMember`s during contract admission through
`ThresholdEvaluation::validate_shape`, and the tests include:

- `admission_rejects_duplicate_quorum_members_before_evaluation`
- `threshold_contract_accepts_only_enough_distinct_admitted_authorities`

So the remaining threshold issue is not duplicate members. It is majority/fork-safety for
time authorities.

## Library Placement

I agree with Designer's three-layer split, with one placement lean:

- `signal-frame`: crypto-agnostic wire mechanics only, shared because router and direct
  criome both need the same frame discipline.
- `signal-standard`: cross-component nouns such as `ComponentKind`, differentiators,
  interest lattices, and likely `AttestedMoment` if every quorum-signed object carries one.
- `signal-criome`: criome-specific agreement verbs and direct-lane solicitation/contribution
  types.

The open seam is `PeerAttestation`.

My lean: do not put BLS-specific `PeerAttestation` in `signal-frame` first. A wire-frame
library should not silently inherit criome trust semantics. If the attestation is becoming
the shared authenticity standard for multiple components, put it in `signal-standard`. If it
is only criome/router for now, keep it in the specific signal libraries and extract after the
second real consumer proves the shared shape.

`signal-router` already has `RouterPeerAttestation`, which is evidence that a shared
attestation envelope may be coming. It is not, by itself, enough reason to make
`signal-frame` crypto-aware.

## Extra Risks

The direct peer listener makes verification and signing reachable over the tailnet. The
first implementation needs cheap rejection before expensive BLS verification, replay
tracking, peer quotas, and rate limits.

Key separation is worth deciding early. The peer lane should probably use a lane-specific
subkey or admitted peer-signing key rather than the same root key used for every policy
signature.

BLS aggregate verification is a good v1 goal for time-sensitive quorums, but performance
claims should be measured on the actual target hardware. Current code verifies signatures
sequentially, so quorum size directly affects the latency budget.

## Implementation Order

Recommended order:

1. Finish the current schema hygiene gate: migrate `signal-criome` and affected contract
   schemas to positional struct syntax, regenerate, and test.
2. Create or land `signal-standard` with the differentiator/interest vocabulary needed by
   router subscriptions.
3. Implement router `Attend` / `Withdraw` with a durable attendance table and router-sole
   matching.
4. Add the `AttestedMoment` majority invariant for fork-safe time authorities, or split the
   schema into majority-safe and explicitly sub-majority families.
5. Define the direct criome peer-lane schema with no payload-bearing nouns.
6. Decide `PeerAttestation` placement before widening it beyond criome/router.
7. Implement the direct lane with rate limiting, replay state, and measured quorum latency.

The report's most important keeper is this: criome is becoming the local agreement machine,
but it stays trustworthy only if every new lane preserves the auth-only boundary.
