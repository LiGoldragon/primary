## 674 — design-critic (adversarial) findings on criome's internal-language object/verb design

### Method note — what was critiqued, and why

The assigned target, `5-object-verb-design.md`, **had not been written** when this
critique ran (Phase 2 design synthesis did not land before the Phase-3 critic was
dispatched; my task input carried `Design summary: null`). I waited on the file
(two background waiters, ~17 min wall clock) and it never appeared. Rather than
return empty, I critiqued the **authoritative concrete design that file 5 is
mandated to formalize**: the in-tree, already-compiled-and-tested policy POC

- `criome/src/language.rs` (the `Contract` / `Rule` / `Threshold` / `TimedRule` /
  `TimeSwitch` / `AgreementRule` / `Evidence` / `Decision` tree + evaluator), and
- `criome/schema/crayome.language.schema` (its concept-schema mirror),

which file `1-ground-criome-vocabulary.md` (gap-list item 1) names as exactly the
artifact file 5 must lift into "the contract + SEMA + verbs." Findings are stated
against that design **and** against the design transfers files 3 and 4 hand to
file 5, so they bind whatever final shape file 5 takes. **The orchestrator should
re-run this critic against file 5 once it exists** — but the structural findings
below are not artifacts of the POC's incompleteness; they are about the *shape*
of the `Rule`-tree model, which is the design decision file 5 inherits.

Every finding is tagged to the binding constraints in `0-frame-and-method.md` and
`2-ground-intent-constraints.md` (C1–C19).

### Severity summary

| # | Finding | Severity | Constraint |
|---|---|---|---|
| F1 | Evidence carries bare identities, not verified signatures — no crypto anywhere in evaluation | **blocker** | C9, C11, C14 |
| F2 | `Rule` is an inline recursive tree, NOT content-addressed composable objects | **blocker** | C1, C2, z9d6 |
| F3 | `Agreement` reconciliation is unverified fact-matching — the LLM-oracle/trust hole, meta-divergence regress | **blocker** | C15, C16, C11 |
| F4 | No timelock clock source — `observed_at` is caller-supplied, timelocks forgeable | **major** | C4, C9 |
| F5 | No replay / branch binding — quorum gathered on one fork replays on the other | **major** | (Tezos transfer, file 3 §2b) |
| F6 | `Rule` recursion is unbounded by construction; totality is claimed but not enforced | **major** → minor | C5, C6 |
| F7 | Missing objects/verbs for a credible v1 (weighted quorum, per-verb binding, revocation, cancel-veto, define-contract verb, divergence object proper) | **major** | C4, C8, C15, file-1 gaps |
| F8 | Quorum-member churn / key-compromise not modeled; no rotation gating | **major** | C13, file-3 Squads transfer |
| F9 | Auth-only line honored by the evaluator, but `Agreement` invites a transport drift | **minor** | C7 |
| F10 | `Decision` is a bare Authorized/Rejected boolean — discards the cryptographic proof the consumer needs | **minor** | C11 |

### F1 — BLOCKER — "verification" is `Vec::contains`, not cryptography (C9, C11, C14)

`Evidence.signatures: Vec<Identity>` and the evaluator's leaf rule is
`SignedBy(identity) => evidence.has_signature_from(identity)`, which is literally
`self.signatures.contains(identity)`. `Threshold::satisfied_count` is a `filter` +
`contains`. **There is no BLS verification, no signature object, no message
binding anywhere in the evaluation path.** The whole "did this principal actually
sign these exact bytes" question — the entire point of criome (C9: "binding the
caller to the exact per-operation content-addressed digest"; C11: "criome verifies
the bytes and principal") — is absent. Anyone who can construct an `Evidence`
value asserts any identity signed. This is a `criome-auth-pilot`-branch regression:
`master_key.rs` / `admission.rs` already do real `blst` min-pk verification over an
`AttestationPreimage`; the language POC throws that away and trusts a list of
names.

**Fix.** `Evidence` must carry `SignatureEnvelope { scheme public_key signature }`
(the deployed type, file-1 §a), not `Identity`. The evaluator's leaf must (a)
resolve the `Identity` to its cluster-root-admitted `BlsPublicKey` via the registry
(C13), and (b) `VerifyBls` the envelope over the **exact content-addressed digest
of the authorized operation** (the 32-byte blake3 `EntryDigest`, C9 / report 112
Map 3) under the criome attestation domain-tag. A quorum proof should be the
aggregated BLS signature (file-4 §A.1), verifiable without signers present. Until
the leaf verifies a signature over a digest, this is not an authorization
language — it is an honor-system set-membership check.

### F2 — BLOCKER — `Rule` is an inline recursive tree, not z9d6 content-addressed composable objects (C1, C2)

`Rule::All(Vec<Rule>)`, `Any(Vec<Rule>)`, `TimedRule { rule: Box<Rule> }`,
`TimeSwitch { before: Box<Rule>, after: Box<Rule> }` embed their sub-rules **inline
by value**. This is precisely the "ad hoc mutable state" z9d6 forbids (C1: "every
reference between objects must be a content-address reference, never a name/handle
into mutable state"). The whole language is one monolithic blob; there is no
object-references-object-by-digest, no sharing, no independent admission of a
sub-policy, no content address for a quorum that another contract can cite. C1
calls object-references-object-by-digest "the mechanism that makes the language a
language" — and it is missing. Equally, C2 requires threshold/time-window policies
to **emerge from composition of addressable objects**; here they are inline enum
arms bolted into one tree, exactly the "primitives beside them" C2 rules out.

This is not a cosmetic encoding choice. It defeats:
- **composability** — a panel quorum cannot be defined once and referenced by both
  an oracle-authority object and a recovery object;
- **the PDA/content-address invariant** (file 3 §3b, the #2 ranked transfer): an
  authorization object's identity should *be* the hash of its policy;
- **acyclicity-for-free** (file 3 §1b): the research leans on content-addressing to
  guarantee the reference DAG is acyclic; an inline `Box<Rule>` tree gets
  acyclicity only because Rust values can't cycle, not because the design enforces
  it — and the moment file 5 adds a stored/named contract that another contract
  references (it must, per file-1 gap 1), nothing prevents a digest cycle.

**Fix.** Split into two layers. A `Contract` is a content-addressed object whose
digest is `blake3(canonical_bytes(contract))`. Composition arms hold **`ObjectDigest`
references to other admitted contracts**, not inline `Box<Rule>`. `All`/`Any`/
`Threshold` reference member objects by digest; the evaluator resolves each digest
from the SEMA `criome-contract` family (file-1 gap 1's missing family). Enforce
acyclicity at admission: a contract may only reference digests that already exist
in the store (a hash cannot name a not-yet-computed hash — file 3 §1b), giving a
strict DAG by construction. This is the single change that turns the POC from "a
recursive predicate tree" into "z9d6 composable authorization objects."

### F3 — BLOCKER — `Agreement` is unverified fact-matching: the trust hole and the meta-divergence regress (C15, C16, C11)

`AgreementRule { divergence, resolution, resolver }` is satisfied by
`evidence.has_agreement_for(...)`, which is true iff an `AgreementFact` with a
**byte-equal** `(divergence, resolution, resolver)` triple sits in the evidence.
There is **no signature on the fact, no quorum on the resolver, no oracle
attestation, no determinism guard, no two-network model.** Three distinct
blocker-level holes:

1. **It is a trust hole, not an oracle.** vhs2/C16 require the reconciliation to be
   "mediated by an LLM-oracle call to a provider which itself resolves through one
   of those identity contracts." The POC's resolver is a bare `Identity` and the
   fact is unsigned: whoever builds the `Evidence` asserts the resolution. File 4
   §B.4 spells out the *only* sound posture — "the policy language never *calls* an
   LLM; it *verifies a quorum-signed attestation object* recording the verdict …
   the signer must itself be one of criome's identity contracts." The design must
   verify (a) the oracle verdict is a content-addressed attestation, and (b) the
   resolver is a **quorum/threshold contract** (the paid expert panel = a k-of-n
   BLS-aggregated identity, file 4 §B.3), whose proof verifies. As written, none of
   that exists — the verdict is taken on faith. **This is exactly the trust hole the
   task names.**

2. **The meta-divergence regress is real and unaddressed.** The task's sharpest
   question: if two diverged networks disagree on *which* oracle / identity-contract
   to consult, the resolver reference is itself contested. `AgreementRule` pins a
   single `resolver: Identity` inside the contract — but the contract is itself
   content-addressed, so the two forks may carry *different* contract digests
   naming *different* resolvers, and there is no rule for which resolver wins. The
   regress does not bottom out. **Fix:** the resolver authority must be **pinned to
   a pre-divergence common ancestor object** — the resolver contract digest must be
   one that *both* forks accepted *before* the split (a Tezos-style replay/branch
   binding to a pre-fork monotonic version, file 3 §2b, F5 below). The divergence
   object must reference the resolver by a digest that is provably in the shared
   history, not chosen post-split. If no common-ancestor resolver exists, the only
   sound terminal state is an explicit recorded **fork** (Augur's fork-as-last-
   resort, file 4 §B.3) — two named realities — not a forced verdict. The design
   must make this terminal fork a first-class object, which it currently cannot
   express.

3. **LLM nondeterminism vs. a total/deterministic language (C5).** Even with a
   signed verdict, the contract must treat it as an **opaque input object verified
   by signature**, never re-run inference inside evaluation (file 4 §B.4: "no LLM
   runtime ever lives inside criome's evaluator"). The POC's structure happens to
   respect this (it only matches a fact), but file 5 must state the discipline
   explicitly and answer file 4's load-bearing open question: *signed-verdict-only,
   or full bit-reproducible re-execution on dispute?* Leaving this unanswered leaves
   the determinism guarantee undefined.

**Fix (summary).** Replace `AgreementRule`/`AgreementFact` with: a `Divergence`
object (two branch identifiers + the pre-fork common-ancestor digest), a
`ResolutionAttestation` (content-addressed verdict + the oracle/panel quorum proof
over it), and an evaluator arm that *verifies the quorum proof of the resolver
contract resolved at the common ancestor*. Make the no-common-ancestor case an
explicit `Fork` terminal object.

### F4 — MAJOR — no trusted clock; timelocks are forgeable (C4, C9)

Every time-based arm (`ActiveAfter`, `ActiveUntil`, `TimeSwitch`) compares against
`evidence.observed_at()` — a `TimestampNanos` the **caller puts into the Evidence**.
Whoever constructs the evidence picks "now," so a decreasing-threshold recovery
(dead-man's-switch, file 4 §A.6) can be triggered early by lying about the time,
and an `ActiveUntil` window can be re-opened by backdating. vhs2/C4 require
"thresholds that increase or decrease over elapsed time"; a time-varying threshold
whose clock is attacker-supplied is security theater. The task explicitly asks:
*who supplies trusted time in a system with no global clock?* — the POC's answer is
"the caller," which is no answer.

**Fix.** The time atom must be **attested**, not asserted. Options, in order of
preference for criome:
- a **signed timestamp / epoch from the consuming engine's SEMA state** (file 4
  §A.5 recommends exactly this over VDFs), i.e. the time enters as an attested fact
  carrying a signature from a trusted clock identity (the cluster-root or a
  designated time-authority contract);
- a **monotonic version counter** bound into each proof (Tezos, file 3 §2b),
  giving ordering "without a wall clock" — sufficient for *ordering* time-varying
  phases even if absolute wall-time is unavailable;
- a **VDF witness** only for the adversarial no-trusted-clock case (file 4 §A.5
  flags VDFs as overkill for the default path; reserve for divergence disputes
  where time itself is contested).
File 5 must pick one and make `Moment`/`observed_at` an *attested* type, not a free
integer. This is a flagged open design choice in file 4 §A.5 — file 5 owes the
decision.

### F5 — MAJOR — no replay or branch binding (file 3 §2b transfer, ignored)

File 3 ranks "per-proof replay/branch binding — *(object content-hash, branch/
network id, monotonic version)*" as a load-bearing cross-cutting import, and file 3
§2c calls it "exactly what makes a divergence object meaningful rather than
ambiguous." The POC has **none of it**: an `Evidence` of signatures over an identity
carries no nonce, no branch id, no version. Consequences: (a) a quorum gathered on
one side of a network split **replays verbatim on the other side** (the named fork
hazard, file 4 §B.1); (b) an attestation is replayable across operations since the
signature isn't even bound to a digest (compounds F1). Note the deployed criome
already has `ReplayNonce` and `put_new_authorization_state` replay enforcement
(file 1 §d) — the language POC, again, drops a protection the daemon already has.

**Fix.** Bind every signature/proof to `(authorized-object content-digest, branch/
network identifier, monotonic version)` — Tezos's three-part counter. This also
supplies F3's common-ancestor anchor and F4's monotonic-version clock, so one
mechanism closes three findings.

### F6 — MAJOR→MINOR — totality is asserted, not enforced (C5, C6)

C5 (FIXED) requires evaluation "total and terminating **by construction**," and
file 3 §1b sells "totality by construction beats gas" as the proof criome stayed
inside the not-a-VM line. The POC's `Rule` is freely recursive (`All(Vec<Rule>)`,
`Box<Rule>`); today it terminates only because a Rust value tree is finite and
acyclic *by accident of being an owned value*. The moment file 5 does what file-1
gap 1 demands — store contracts and let them reference each other — recursion
becomes **reference-following**, and nothing in the design forbids a cycle or
bounds depth/fan-out. There is no stated structural bound, no depth limit, no
acyclicity proof. This is the exact drift toward a VM that vhs2 forbids: not via
loops/opcodes (good — none exist), but via **unbounded recursive object reference**.

**Smell-test of operations for VM-drift (per task ask 1):** `SignedBy`, `Threshold`,
`ActiveAfter/Until`, `TimeSwitch` are all bounded, total, non-recursive leaves —
clean. `All`/`Any` are the only recursive arms. `Agreement` is a lookup. **No
operation is Turing-complete, none loops, none meters gas — the operation *set* is
disciplined.** The single VM-drift vector is unbounded recursion-by-reference once
composition becomes by-digest (F2). Severity is major as a design risk, minor today
because the value tree can't cycle.

**Fix.** State and enforce: (a) the content-address DAG is acyclic by admission
order (F2 fix gives this for free); (b) a declared maximum reference depth and
fan-out so evaluation cost is a static function of contract size (file 3 §1b); (c)
typecheck-at-admission (Michelson, file 3 §2a) so an admitted contract is *statically
known* total. Advertise the **absence of a gas meter** as the proof of the line
(file 3 §1b).

### F7 — MAJOR — missing objects/verbs for a credible first version (C4, C8, C15)

The POC vocabulary is the floor; a credible v1 (per files 1, 3, 4) is missing:

- **Weighted quorum / two-gate (participation + supermajority).** `Threshold` is
  flat k-of-n only. File 3 §2c (Tezos) and file 4 §B.1 both require weighted
  thresholds (flat = unit-weight special case) and a *two-gate* divergence vote
  (quorum participation AND supermajority agreement). Missing entirely. Without the
  second gate a small faction reconciles unilaterally during a split (file 3 §2c).
- **Per-verb quorum binding.** File 3 §3c (Squads) and file 4 §A.4 (social
  recovery) both insist *altering a policy is itself a policy-gated, time-locked
  action*, and that a quorum binds **to a verb** (use ≠ re-key ≠ admit ≠ revoke),
  not to the identity as a whole. The POC has a single `Contract.rule` with no verb
  dimension. **This is the biggest vocabulary gap** — the define/amend/revoke verbs
  and their distinct quorums are the operational core.
- **A define-contract / amend-contract verb on the meta plane.** File 1 gap 5:
  `meta-signal-criome` has only `Configure`; there is no verb to mint, store, or
  amend a contract. Without it the language is unreachable from the wire.
- **A revocation / status arm.** Deployed criome has `PrincipalStatus
  [Active Revoked]` and a revocation SEMA family (file 1 §a/§d); the `Rule` tree
  ignores it — a revoked member still counts toward a threshold. Blocker-adjacent
  for a security language; placed here as part of the v1 gap set.
- **Cancel/veto quorum on timelocks.** File 3 §1e (OZ) and §3c (Squads): the
  security *purpose* of a timelock is the reaction window; a timelock needs an
  explicit veto quorum distinct from the execute quorum. Absent.
- **A proper `Divergence` object** (two branch ids + ancestor), distinct from the
  `Agreement` fact (F3). C15 makes "the divergence fact AND how reconciliation is
  determined" a first-class object class; the POC collapses both into one unsigned
  triple.
- **Graduated/piecewise time-varying threshold.** File 1 gap 3: `TimeSwitch` is a
  single before/after boundary; vhs2 asks for thresholds that *increase or
  decrease* over elapsed time — a piecewise step-function over a phase schedule
  (file 4 §A.6). The binary switch is the degenerate two-phase case.

**Fix.** File 5 must add: weighted `Quorum` with two-gate divergence voting; a
verb dimension (`Use`/`ReKey`/`Admit`/`Revoke`/`Amend`) each with its own quorum;
meta-plane `DefineContract`/`AmendContract`; revocation-aware membership; timelock
veto quorum; a first-class `Divergence` object; and a `Schedule` (vector of
`(boundary, k)` phases) replacing the binary `TimeSwitch`.

### F8 — MAJOR — key compromise & quorum-member churn unmodeled (C13, file-3 Squads transfer)

The task asks specifically about key compromise and quorum-member churn. The POC
has **no rotation, no membership-change gating, no liveness/decay**. File 3 §3c is
explicit: "an attacker who captures a sub-quorum cannot instantly rewrite the
rules" only if *changing signers/threshold is itself time-locked*. File 4 §A.6's
liveness-renewed certificates (members erase shares and leave when no fresh cert
arrives) are the churn model. None of this exists, so: a compromised member key is
permanent (no revocation arm, F7); changing the member set is ungated (no amend
verb, F7); a departed member still counts.

**Fix.** Membership amendment is a time-locked, veto-able, quorum-gated verb (F7);
member status is revocation-aware (F7); optionally a liveness-decay schedule (file
4 §A.6) so stale members lose weight. Tie compromised-key handling to the deployed
`RevokeIdentity` path + cluster-root re-admission (C13).

### F9 — MINOR — auth-only line is honored by the evaluator, but `Agreement` invites drift (C7)

Credit where due: the evaluator computes a `Decision` and moves no bytes — wckt/C7
("signs and verifies, never transports") is respected by `Contract::evaluate`. The
risk is in F3's fix: a naive "oracle call" implementation would have criome *fetch*
the verdict, which **would** make criome transport. The design must keep the verdict
arriving as an already-present, out-of-band, content-addressed attestation object
(C10: after-the-fact, non-blocking, out-of-band) that criome only *verifies* — the
oracle call happens outside criome (router transports it, mirror moves it). State
this boundary explicitly in file 5 so the reconciliation feature does not smuggle
transport into criome.

### F10 — MINOR — `Decision [Authorized Rejected]` discards the proof (C11)

The evaluator returns a bare boolean-equivalent. But C11 says criome "verifies the
bytes and principal while the consumer keeps the full content verdict" — the
consumer needs the *cryptographic facts* (which signers satisfied which policy,
over which digest, the aggregated proof) to keep its own semantic verdict, mirroring
the deployed `AuthorizationGrant`'s `policy_satisfaction` + `signatures` +
`authorized_object_digest` (file 1 §b). A naked Authorized/Rejected throws that
away.

**Fix.** `Decision::Authorized` should carry an `AuthorizationProof` (the satisfied
member set, the threshold met, the content-digest authorized, the aggregated BLS
proof) — converging on the deployed `AuthorizationPolicySatisfaction`/
`AuthorizationGrant` shape rather than inventing a thinner one (C14: extend, don't
replace).

### What the design gets right (to preserve in file 5)

- The leaf operation set (`SignedBy`, `Threshold`, time arms) is genuinely
  *limited* — no loops, no gas, no arbitrary code. The not-a-VM line is respected
  at the operation level (only F2/F6's recursion-by-reference threatens it).
- The atoms are already the wire identity types (`Identity`, `ObjectDigest`,
  `TimestampNanos`, `RequiredSignatureThreshold` imported from `signal_criome`),
  satisfying C3 (public key as atom) and C14 (extend the deployed model) — file 5
  must keep importing, not fork, these.
- The evaluator is a pure total predicate today — the right *shape* for the
  ERC-4337 validate-only model (file 3 §1d, the #1 transfer). Keep it pure and
  side-effect-free.

### Top open questions for file 5 / synthesis (file 8)

1. **Time source (F4):** SEMA-attested timestamp, monotonic version counter, or VDF?
   File 4 §A.5 flags this as the load-bearing choice; file 5 owes a decision.
2. **Oracle determinism (F3.3):** signed-verdict-only, or bit-reproducible
   re-execution on dispute? Sets the entire cost of the reconciliation path
   (file 4 §B.4).
3. **Meta-divergence anchor (F3.2):** confirm the resolver must be pinned to a
   pre-fork common-ancestor contract digest, and that the no-ancestor case
   terminates in an explicit recorded `Fork`, never a forced verdict.
4. **Composition encoding (F2):** content-addressed `ObjectDigest` references with
   admission-order acyclicity — is this accepted as the substrate (it must be, per
   z9d6/C1), replacing inline `Box<Rule>`?
