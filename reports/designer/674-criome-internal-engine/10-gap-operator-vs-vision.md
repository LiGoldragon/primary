# 674.10 — Gap: what operator landed vs. the vision

*Operator shipped commit `9719703c` ("criome: add explicit psyche escalation
outcome") on criome main — `Rule::EscalateToPsyche` + `Decision::EscalateToPsyche`,
typed decisions replacing bool, composed through `All`/`Any`, tests, concept-schema,
INTENT/ARCHITECTURE, fmt/test/clippy + remote Nix green, no duplicate Spirit. This
file maps that against the vision in 674.8/674.9 and records `vhs2`/`ay3y`/`gc0n`.*

## Verdict in one line

Operator advanced the **leaf feature** (psyche escalation as a first-class typed
outcome) cleanly and correctly — but on the **v0 shape the critique already named**
(inline `Rule` tree, set-membership "verification," caller-supplied time). The
foundational rebase the vision and critic require (content-addressing, real BLS,
attested time, signed reconciliation, verb dimension) is untouched. The gap is not
a mistake; it is the next, larger move.

## What operator got right (and where their grounding beats the workflow's)

- **Typed `Decision` (Authorized / Rejected / EscalateToPsyche), not bool** — matches
  the vision and the file-7 PoC; the `All`/`Any` propagation is correct (`All`
  escalates only after the required rules authorize; `Any` prefers a real
  authorization over escalation).
- **`EscalateToPsyche` is exactly `gc0n`'s psyche rung**, and ARCHITECTURE frames it
  precisely the way 674.9 demands: *"a contract-level decision result, not a
  daemon-side prompt mechanism … the judgment and any later signed verdict happen
  outside the finite evaluator."* That is the auth-only / criome-verifies-never-runs
  discipline, encoded.
- **Better-grounded than the workflow's file-6 schema.** Operator's model is built on
  the *deployed* criome: the two policy classes (simple self-signed / complex quorum),
  the existing *escalation-to-sign* and *escalation-to-approve* kinds, and the
  operative principle [Criome verifies; Persona decides]. The workflow's file-6
  invented `OracleResolution`/`ReconciliationPolicy` nouns; operator's `Agreement` +
  escalation-kinds say the same thing closer to what already exists. **The vision
  should converge onto operator's grounding, then apply the structural fixes** —
  not the other way round.
- **Process is exemplary:** remote-Nix verification with no local path overrides,
  intent reflected into INTENT.md/ARCHITECTURE.md, and the guardian-confirmed
  no-duplicate (gc0n already holds the idea).

## The gap, by dimension

| # | Dimension | Operator landed (main) | The vision (674.8/9, `vhs2`/`ay3y`/`gc0n`, critic) | Priority |
|---|---|---|---|---|
| G1 | **Composition shape** | inline `Rule` tree — `All(Vec<Rule>)`, `Box<Rule>`, members are `IdentityHandle` | content-addressed composable objects: rules reference sub-objects by `ObjectDigest`; a contract's id IS the digest of its bytes (z9d6, critic F2) | **foundational** |
| G2 | **Verification** | `evidence.has_signature_from` = `Vec::contains` over bare `Identity` — no crypto | leaf resolves `Identity`→admitted `BlsPublicKey` and `VerifyBls`es a `SignatureEnvelope` over the operation digest (criome already does this in `admission.rs`; critic F1) | **foundational** |
| G3 | **Time** | `Evidence.observed_at` is a caller-supplied `TimestampNanos` — forgeable | quorum-attested coarse-time window with tunable tolerance (`ay3y`), tighter when healthy / wider under divergence; the gap-widening itself bounded + policy-gated (critic F4) | **high** |
| G4 | **Replay / branch binding** | none — Evidence carries no nonce, branch, or version | bind every proof to (object-digest, branch-id, monotonic version); same mechanism supplies G3's clock and G6's anchor (critic F5) | **high** |
| G5 | **Adjudicator ladder** | `EscalateToPsyche` only — single hardcoded target | generalize to a *named adjudicator* (quorum / meta-authority / LLM-panel / **smarter-agent** / psyche), unifying with operator's existing *escalation-to-approve*; "non-judgment" parameterized by target, and the **default LLM trained to abstain** toward it (`gc0n`, 674.9) | **high** |
| G6 | **Divergence / oracle / fork** | `AgreementRule`/`AgreementFact` = unsigned byte-equal triple match | first-class `Divergence` (branches + pre-fork common-ancestor), quorum-**signed** resolution verdict (Chainlink shape, criome never runs the model), resolver pinned to the common ancestor, explicit terminal `Fork` when none (critic F3 — the trust hole + meta-divergence regress) | **high** |
| G7 | **Quorum richness** | flat k-of-n `Threshold` | weighted members + two-gate divergence vote (participation AND supermajority) (critic F7) | medium |
| G8 | **Verb dimension** | one `Contract.rule`, no verb | per-verb quorums (use ≠ rekey ≠ admit ≠ revoke ≠ amend) + a meta `DefineContract`/`AmendContract` verb (schema roots are empty `[] []` today); revocation-aware membership (deployed `PrincipalStatus`) — the biggest vocabulary gap (critic F7/F8) | medium |
| G9 | **Time-varying threshold** | `TimeSwitch` = single before/after boundary | piecewise step-function over a phase schedule — thresholds that *increase or decrease* over elapsed time (`vhs2`); the binary switch is the degenerate two-phase case | medium |
| G10 | **Wire / SEMA** | concept schema only, empty roots `[] []`; library evaluator, not on the wire | Input/Output verb roots + a `criome-contract` SEMA family keyed by digest, acyclic-at-admission | medium (POC-deferred, acknowledged) |
| G11 | **Denial detail** | `Rejected` carries no reason | typed denial naming the failing rule + an `AuthorizationProof` on success (deployed `AuthorizationGrant` shape; critic F10) | minor |

## The prioritized path (a structural rebase, then enrichment)

The two foundational gaps gate everything; do them first, in order, because each
later gap is cheap once they land and incoherent before:

1. **G1 content-addressing** — split into a content-addressed `Contract` object whose
   composition arms hold `ObjectDigest` references resolved from a store; acyclicity
   by admission order. This is the single change that turns "a recursive predicate
   tree" into "z9d6 composable objects," and it also closes the unbounded-recursion
   drift (critic F6) for free.
2. **G2 real BLS** — `Evidence` carries `SignatureEnvelope`, the leaf verifies a
   signature over the content digest via the deployed `admission.rs`/`master_key.rs`
   path. Until this lands the language is an honor-system membership check, not auth.
3. **G3+G4 attested time + replay binding** — one mechanism: a signed (object-digest,
   branch, monotonic-version, attested-moment) anchor on every proof.
4. **G6+G5 signed reconciliation + adjudicator ladder** — `Agreement` becomes a
   `Divergence` + a quorum-signed verdict; `EscalateToPsyche` generalizes to a named
   adjudicator (psyche / meta-authority / smarter-agent / panel), unifying with the
   existing escalation-to-approve, with the abstaining default and timelock fallbacks.
5. **G7–G9 vocabulary** — weighted/two-gate quorum, verb dimension + define/amend,
   revocation-aware membership, piecewise time-varying threshold.
6. **G10–G11 wire/SEMA + denial detail** — lift onto the signal-criome wire.

Lane note: criome main is **operator's**; G1/G2 touch the deployed crypto and are
naturally operator-carried. Designer can prototype the content-addressed + attested
shape in a `~/wt` branch as design pressure (the same role the file-7 PoC played),
then operator rebases. The two lanes have *converged on the same artifact* (the
in-tree `language.rs`), which is good — the next move is agreeing the rebase shape
before piling more leaf features on the v0 tree.

## One naming question for the psyche

Operator de-Crayome'd: renamed `crayome.language.schema` → `criome.language.schema`,
calls it "the Criome internal language," and **removed the `Crayome` referent from
`ay3y` and `gc0n`** as stale (Crayome lookups now return nothing). But the psyche
has said "Crayome" deliberately and repeatedly for *the language*. So: is **Crayome**
a distinct intended name for the language (worth keeping / even canonical), or a
transcription artifact of "criome" that operator is right to retire? Designer reports
still carry "Crayome" text; I'm holding the cleanup until this is settled rather than
erase a possibly-deliberate name.
