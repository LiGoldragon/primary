# 674.4 — Research: complex-identity primitives & divergence-reconciliation

Research support for criome's limited typed policy language (Spirit `vhs2`).
The brief: the language composes complex identity contracts over public-key
atoms (quorums, time-locks, time-varying thresholds) and carries explicit
divergence-reconciliation objects, where conflict resolution *may* be mediated
by an LLM-oracle call that itself resolves through one of those identity
contracts (a paid expert panel). This file surveys the cryptographic and
distributed-systems primitives that supply the *vocabulary* — it does not pick
a wire encoding (that is `5`/`6`) or build the PoC (`7`).

Constraint reminder (from `0`): criome stays **auth-only** (`wckt`); builds on
`z9d6` content-addressed composable authorization objects; is **triad-consistent**
(this is criome's Nexus object/verb vocabulary, not a fourth engine); is a
**limited** policy language, not a VM (`vhs2`). The primitives below are
read as *acceptance-policy shapes layered over composable objects*, not as a
transaction execution model.

## A. Complex-identity primitives

The atom is a public key. Above it the language must express: "who, how many,
with what aggregation, under what time conditions, can authorize this object."
Six primitive families cover the brief, ordered from criome's current ground
(BLS) outward.

### A.1 BLS threshold signatures + aggregation (criome already uses BLS)

BLS (Boneh–Lynn–Shacham) is a pairing-based scheme whose defining property for
this work is **aggregation**: "Multiple signatures generated under multiple
public keys for multiple messages can be aggregated into a single signature,"
and "aggregation can take place publicly by a simple multiplication, even long
after all the signatures have been generated and the signers are no longer
available" [Prysm; Stanford BLS-multisig]. Two further properties matter:

- **Uniqueness / determinism.** "For a given key and message, there is only one
  valid signature." This is load-bearing for a *content-addressed* policy
  language — a BLS signature over a fixed message is itself a deterministic,
  hashable object, so an aggregated quorum-proof is a stable content address.
- **Threshold form via Shamir.** "Combining the properties of BLS with Shamir's
  secret sharing, it is possible to construct a threshold signature scheme where
  once a client obtains at least 2f+1 signatures ... they can compute a unique
  master signature that is the same irrespective of which 2f+1 validators'
  signatures were used" [SafeStake]. The k-of-n proof collapses to one
  signature whose verification cost is independent of *which* k signed.

Ethereum's consensus layer "uses BLS to aggregate signatures from all
validators," which is the existence proof that BLS quorum-proofs scale to large
n in production [Wikipedia/BLS]. **Relevance to criome:** criome's existing BLS
attestation is already the right substrate for a `Quorum(k, [PublicKey])`
object — the proof of "k of these n attested" is a single aggregated BLS
signature, content-addressable, verifiable without the signers present.
Mysten's subset-optimized variant is worth noting for the n-is-large,
k-subset-changes-often case [Mysten Labs].

### A.2 FROST — threshold Schnorr (the alternative aggregation family)

FROST (Flexible Round-Optimized Schnorr Threshold), now **RFC 9591**, is the
Schnorr counterpart: "signatures can be issued after a threshold number of
entities cooperate to compute a signature." Key trade vs BLS:

- **Two interactive signing rounds** vs BLS's non-interactive public
  aggregation. FROST signers must coordinate (a preprocessing round + a signing
  round); BLS signers can sign independently and have a third party aggregate
  later. For criome — where attesters are distributed daemons that may not be
  simultaneously online — **BLS's non-interactive aggregation is the better fit**
  for the common quorum case; FROST is relevant only where a single
  Schnorr/Taproot-style output key must be indistinguishable from a single
  signer.
- "Depends only on a prime-order group and cryptographic hash function," no
  pairings — cheaper verify, but loses BLS's free aggregate-of-aggregates.

**Relevance:** FROST is the answer to "what if a complex identity must appear
*externally* as a single ordinary public key" (one quorum that signs as one
identity to an outside verifier). It is the natural backing for an
identity-contract that wants to be **opaque** to the relying party — useful for
the "expert-panel-as-one-identity" oracle case in §B.4. Note it as the
single-output-key option; BLS as the transparent-aggregate option.

### A.3 k-of-n multisig (the base quorum object)

Plain k-of-n multisig is the floor: n named public keys, any k of which
authorize. It is *not* a signature scheme — it is an **acceptance policy**, which
is exactly the z9d6 framing ("threshold, majority, or time-window acceptance
policies are criome contract logic layered on those composable authorization
objects"). Threshold BLS/FROST are the *cryptographic compression* of multisig
(one proof instead of k); naive multisig (k separate signatures, all checked)
is the *uncompressed* form. The policy language should treat them uniformly: a
`Quorum` object declares `k`, the member set, and a *proof discipline*
(aggregated-BLS, FROST, or list-of-signatures) chosen by the verifier's needs,
not by the policy author. This is the cleanest mapping of the primitive onto
z9d6's "each component can decide acceptance based on another accepted object."

### A.4 Social-recovery wallets (quorum *over a different action than use*)

The Argent/Buterin design contributes a structural insight the others lack: a
single identity has **two different authorization policies for two different
actions**. "Only the owner's single signature is needed for normal
transactions, and the guardian quorum is only invoked during the recovery
process" — i.e. *use* is 1-of-1, *re-keying* is k-of-n guardians, where "a set
of at least 3 ... guardians, of which a majority can cooperate to change the
signing key" [ueex; gate.com]. Buterin's framing: guardians can be "arbitrary
addresses ... with no expectation that those addresses use the same wallet"
[VitalikButerin/X]. Crucially the recovery action is typically gated by a
**time-delay** with owner-veto, which is the bridge to §A.5/§A.6.

**Relevance to criome:** this is the model for criome's **master-key rotation /
host re-admission** under quorum, distinct from the everyday auth path. It says
the policy language needs to bind a quorum object *to a specific verb* (re-key,
admit, revoke), not to the identity as a whole — different verbs carry different
quorums. This directly informs the object/verb split in `5`.

### A.5 Time-locks and verifiable delay functions (VDFs)

A time-lock makes an authorization valid/invalid as a function of elapsed time.
Two distinct mechanisms:

- **VDF**: "a function that is slow-to-compute, but is quickly verifiable given a
  short proof," with **sequentiality** ("no matter how much hardware ... they
  cannot finish faster than the time dictated"), **efficient verifiability**, and
  **evaluation uniqueness** ("only one valid proof passes verification")
  [Ledger; arxiv 2211.08162]. The unique-proof property again gives a
  *content-addressable* time witness.
- **Time-lock puzzle (TLP)**: "quickly generated, but slow-to-solve" — most VDFs
  are built on TLPs. They "act as a time-lock that prevents participants from
  seeing the outcome ... until it is too late to manipulate the inputs."

**Caveat for criome (important):** a VDF measures *computational* elapsed time,
not wall-clock. For a policy language whose conditions are "thresholds that
increase/decrease over elapsed time" (`vhs2`), the natural time source is the
**attested clock of the consuming engine / SEMA state**, not a VDF — VDFs are
overkill and import a sequential-compute dependency criome should not carry.
VDFs are worth citing as the *trustless-delay* option for the adversarial case
(no trusted clock, e.g. inside a divergence dispute where time itself is
contested), but the default time atom should be a signed timestamp / block-or-
epoch height the daemon already trusts. Flag this as an open design choice in §5.

### A.6 Time-varying quorum / threshold (the `vhs2`-specific requirement)

`vhs2` explicitly names "thresholds that increase or decrease over elapsed
time." Prior art:

- **Dead-man's-switch / escalation**: "an automated system designed to trigger a
  specific action if it doesn't receive a regular 'alive' signal ... within a
  predetermined time frame"; escalating designs "progress through escalating
  stages before triggering automated actions" [metafunctor/Posthumous;
  Coinmonks]. This is a **decreasing** threshold: as the owner's silence
  lengthens, the k required from guardians falls (eventually guardians alone can
  act).
- **Liveness-renewed quorum certificates** (USPTO 11258593 / 11736278 /
  12120223, "dynamic and unpredictable changes to quorum memberships"): a
  subordinate quorum "periodically ... send[s] a quorum-signed proof of liveness
  to the master quorum," which returns "a signed certificate of operation that
  validates the subordinate quorum operations for an additional amount of time";
  a member that "does not see a new certificate ... within the specified time
  period can erase its quorum secret share and leave." This is the **increasing**
  direction: authority *decays* unless actively renewed, raising the effective
  bar over time.

**Relevance:** these two patterns are the concrete shapes of the `vhs2`
"time-varying threshold." The policy primitive is a `Quorum` whose required `k`
is a **function of elapsed time** against a phase schedule — a piecewise step
function over time intervals, each interval naming a `k`. Decreasing schedule =
recovery/inheritance/dead-man; increasing schedule = decaying delegation that
must be renewed. Both reduce to: *evaluate elapsed-time → select the active
threshold → evaluate the quorum*. This keeps the language **limited** (no
arithmetic VM): time enters only as interval selection over a declared
schedule, not as general computation.

## B. Divergence-reconciliation patterns

`vhs2`: "explicit divergence-reconciliation objects for when two networks
split, where conflict resolution may be mediated by an LLM-oracle call." This is
two problems: (1) what *is* a divergence object and how do distributed systems
pick a winner; (2) how an external fact (here, an LLM/expert-panel verdict)
enters a deterministic policy evaluation without poisoning its determinism.

### B.1 Fork-choice and finality (the divergence-detection / winner model)

A fork-choice rule "tells a node which branch of a block tree to treat as the
canonical chain when more than one branch is available," while finality "tells
you ... which part of history should no longer be reverted" [Cube; ethereum.org/
Gasper]. Ethereum's **Gasper** = **LMD-GHOST** (liveness: "selects the fork with
the greatest accumulated weight of attestations," latest-message-only) +
**Casper FFG** (safety: "justifies and finalizes checkpoints based on validator
votes") [ethereum.org; eth2book]. The split of concerns is the lesson:

- **liveness / preference** (which fork is currently heaviest) is *automatic and
  weight-based* — for criome this is "which divergent branch has the most
  attestation weight from admitted identities."
- **finality** (what can never be reverted) is a *stronger, slower, quorum-gated*
  property. Divergence-reconciliation objects should distinguish a **tentative
  winner** (weight) from a **finalized resolution** (quorum + irreversibility).

Forks split into **accidental/temporary** (auto-resolved: "the network continues
on the longer chain and abandons the shorter") vs **permanent/contentious** (the
DAO → ETH/ETC split, resolved by *social consensus*, not the protocol)
[CoinTracker; SysTutorials]. Replay protection is a named hazard: "without it, a
transaction on one chain can repeat on the other." **Relevance:** criome's
divergence object needs (a) an automatic weight rule for the common case, and
(b) an escalation path to a *quorum/oracle adjudication* for the contentious
case the weight rule cannot settle — which is exactly where the LLM-oracle
enters.

### B.2 Oracle pattern — how off-chain facts enter deterministically (Chainlink)

The determinism problem is the whole game. Chainlink's model: a contract
"sends a request ... specifying the data type, precision, and return
conditions"; "multiple nodes independently carry out the same task"; nodes
"submit their results to an on-chain aggregation contract, which combines
multiple responses according to predefined rules to produce a single output
value"; and crucially "the data feed aggregator contract must receive responses
from a **minimum number of oracles** or the latest answer will not be updated"
[gate.com; Chainlink docs]. Off-Chain Reporting (OCR) compresses this: many
nodes agree off-chain, then **a single signed report carrying a quorum of node
signatures** is submitted in one transaction; on-chain only verifies the
threshold of signatures, not the data-gathering.

The determinism is preserved because **the chain never does the nondeterministic
work** — it verifies a *quorum-signed attestation of a result*. "The system
allows contracts to rely on off-chain data ... while still preserving
deterministic execution" by "distributing trust among numerous participants"
[Chainlink docs]. **This is the template for criome's LLM-oracle**: the policy
language never *calls* an LLM; it *verifies a quorum-signed attestation object*
recording the LLM/panel's result. The oracle call happens outside; only its
signed, content-addressed verdict re-enters.

### B.3 Decentralized arbitration / Schelling-point adjudication (Kleros, Augur)

Two designs for "a panel adjudicates the fairest resolution":

- **Kleros** draws jurors randomly (staked PNK = probability of selection) and
  pays for **coherence with the majority**: "Incentives are based on ... a
  Schelling Point ... the strategy people choose by default in absence of
  communication"; "jurors whose vote is within the 25th–75th percentile ... are
  considered to have voted coherently and are rewarded," incoherent jurors "lose
  their stakes" [Kleros/Medium; gate.com]. The honest answer is the focal point;
  deviating is punished.
- **Augur** uses staked **REP** reporting with escalating dispute bonds, and a
  nuclear option — **forking**: "if more than 2.5% of all REP files the
  dispute, the market forks," REP "splits into multiple versions, one for each
  possible outcome; versions ... which do not correspond to the real-world
  outcome will become worthless" [Gemini; Augur whitepaper]. The dispute
  ultimately resolves by *making token-holders choose which reality to inhabit*.

**Relevance:** these are the concrete model for `vhs2`'s "paid expert panel
adjudicating the fairest resolution model." The panel is a **quorum identity
contract** (§A.1/§A.3) whose members are staked experts; its verdict is the
Schelling-coherent answer; payment/slashing is the incentive. Critically,
**Augur's fork-as-last-resort directly mirrors criome's divergence object**: when
adjudication itself cannot converge, the principled outcome is an explicit,
recorded *split into two named realities*, each self-consistent — not a forced
false consensus. criome's divergence-reconciliation object should make this an
explicit terminal state, not a failure.

### B.4 The LLM-oracle: staying deterministic/verifiable inside a policy language

This is the sharpest design question and the brief flags it directly. An LLM
call is, by default, **nondeterministic** — disqualifying it from sitting
*inside* a deterministic policy evaluation. The resolution is to **never put the
inference inside the language**; put only a *signed, content-addressed
attestation of the result* inside. Three reinforcing techniques from the
verifiable-AI literature:

1. **Deterministic inference (EigenAI).** Nondeterminism is concrete and
   removable: "Floating-point non-associativity, kernel scheduling, variable
   batching"; "cuBLAS can produce different results across runs unless you
   explicitly disable certain optimizations." By controlling the stack —
   "operators and verifiers must use identical GPU SKUs," "replace vendor
   kernels with custom implementations," "fixed-seed PRNGs with canonical
   iteration order" — they reach "100% reproducibility across 10,000 test runs."
   The payoff: "Given identical inputs (model, prompt, seed, decode policy), the
   output is a pure function." A pure function of declared inputs is exactly what
   a content-addressed object needs [EigenAI blog/whitepaper].

2. **Attested / signed result (TEEs).** "The hardware enclave keeps prompts,
   model weights, and intermediate activations confidential while **signing the
   final output with a key bound to the loaded code's measurement**"; a verifier
   can "check that a specific model ran on a specific input even if the operator
   is unknown" [eco.com TEE; Oasis]. The signed `(model_measurement, input_hash,
   output, signature)` tuple is a content-addressable attestation — it re-enters
   criome as an ordinary signed object verifiable against the enclave's PKI.

3. **Optimistic verification + dispute (EigenAI / fraud-proof model).** Results
   "are accepted by default but can be challenged during a dispute window"; on
   challenge "a committee re-executes the inference inside TEEs. Because
   execution is deterministic, **verification collapses to a simple question: do
   the bytes match?**"; mismatches "trigger slashing" [EigenAI]. This is the same
   weight-then-finality split as §B.1 and the same dispute-bond structure as
   Augur/Kleros — the LLM verdict gets the *same* adjudication machinery as any
   other divergence.

**Critical assessment — can an LLM-oracle sit inside a limited policy language?**
Yes, but only under a strict discipline, and the discipline is *the same one
that lets Chainlink prices sit inside a deterministic contract*:

- The policy language must treat the LLM result as an **opaque input object**,
  never as a computation it performs. The verb is *verify-attestation*, not
  *invoke-model*. This keeps `vhs2`'s "limited, not a VM" line intact — no LLM
  runtime ever lives inside criome's evaluator.
- The attestation must be **content-addressed and pure-of-declared-inputs**:
  `(model id+measurement, exact prompt/input hash, decode policy/seed, output,
  signing identity)`. Determinism (technique 1) makes re-derivation possible;
  the content address makes the verdict immutable and quotable by other objects
  — satisfying z9d6 composability ("each component can decide acceptance based on
  another accepted object").
- The **signer must itself be one of criome's identity contracts** — precisely
  the brief's "resolves through one of those identity contracts." The expert
  panel signs as a §A.1 BLS-aggregated quorum (transparent) or a §A.2
  FROST single-key (opaque); the attestation is accepted iff that quorum proof
  verifies. The LLM-oracle is thus *not a trusted external service* but a
  **quorum-signed object produced by a paid panel identity** — Chainlink's
  "minimum number of oracles" + Kleros's staked-panel + EigenAI's
  attested-determinism, composed.
- **Disputes use the existing divergence machinery** (§B.1/§B.3): optimistic
  acceptance, a challenge window, re-execution-or-re-adjudication, and — when
  even the panel cannot converge — Augur-style **explicit fork** as the recorded
  terminal divergence object, not a silent guess.

The honest residual risk: deterministic inference (technique 1) is operationally
heavy (locked GPU SKUs, custom kernels) and TEE attestation (technique 2)
inherits the chip-vendor PKI as a trust root. criome does not need bit-exact
re-execution for *most* policy decisions — it needs the verdict to be a
**signed, content-addressed object whose signer is a criome quorum**, with
re-execution available only as the dispute-resolution backstop. That is the
recommended posture: attestation-first (always), determinism-and-re-execution
second (only on challenge). Carry this as the load-bearing open question into
`5`/`8`: *how strong a determinism guarantee does criome require of the oracle —
signed-verdict-only, or full bit-reproducible re-execution?* The answer sets the
cost of the whole reconciliation path.

## Mapping summary (primitive → criome policy object)

| Primitive | criome policy-object role | z9d6 fit |
|---|---|---|
| BLS threshold + aggregation | `Quorum` proof, transparent aggregate, content-addressed | acceptance proof over composable objects |
| FROST (RFC 9591) | `Quorum` appearing as a single opaque key | quorum-as-one-identity |
| k-of-n multisig | base `Quorum` acceptance policy (uncompressed) | "threshold/majority acceptance policy" |
| Social-recovery guardians | per-**verb** quorum (re-key/admit/revoke ≠ use) | object accepts based on another object + action |
| Time-lock / VDF | trustless-delay witness (adversarial case only) | content-addressed time witness |
| Time-varying quorum | `Quorum.k` = step-function over a time schedule | "time-window acceptance policy" |
| Fork-choice / finality | divergence object: tentative-weight vs finalized | composable: branch = accepted-object set |
| Chainlink OCR | oracle verdict as quorum-signed attestation object | external fact as accepted object |
| Kleros / Augur | paid expert panel = staked quorum identity; fork as terminal | adjudication-as-identity-contract |
| Deterministic+attested LLM | opaque attestation object; verb = verify, never invoke | LLM verdict as content-addressed accepted object |

## Sources

- [Prysm — BLS cryptography](https://prysm.offchainlabs.com/docs/learn/dev-concepts/bls-cryptography/)
- [Stanford — BLS Multi-Signatures with Public-Key Aggregation](https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html)
- [Wikipedia — BLS digital signature](https://en.wikipedia.org/wiki/BLS_digital_signature)
- [SafeStake — Why SafeStake Uses a BLS Threshold Signature](https://medium.com/ethereum-on-steroids/why-safestake-uses-a-bls-threshold-signature-67ba4bbf9d1e)
- [Mysten Labs — Subset-optimized BLS Multi-signature with Key Aggregation](https://www.mystenlabs.com/blog/new-bls-aggregation-for-proof-of-stake)
- [RFC 9591 — FROST (Flexible Round-Optimized Schnorr Threshold)](https://www.rfc-editor.org/rfc/rfc9591.html)
- [CrySP (Waterloo) — FROST](https://crysp.uwaterloo.ca/software/frost/)
- [Komlo & Goldberg — FROST (eprint 2020/852)](https://eprint.iacr.org/2020/852.pdf)
- [Vitalik Buterin — Why we need wide adoption of social recovery wallets](https://vitalik.ca/general/2021/01/11/recovery.html)
- [Vitalik Buterin (X) — arbitrary-address guardians request](https://x.com/VitalikButerin/status/1196253160567922688)
- [ueex — Social Recovery Wallet](https://blog.ueex.com/crypto-terms/social-recovery-wallet/)
- [gate.com — What Is a Social Recovery Wallet?](https://www.gate.com/learn/articles/what-is-a-social-recovery-wallet/676)
- [Ledger — Verifiable Delay Function (VDF)](https://www.ledger.com/academy/glossary/verifiable-delay-function-vdf)
- [arXiv 2211.08162 — Single Squaring VDF from Time-lock Puzzle](https://arxiv.org/abs/2211.08162)
- [metafunctor — Posthumous: A Federated Dead Man's Switch](https://metafunctor.com/post/2026-02-14-posthumous/)
- [Coinmonks — Dead Man's Switch](https://medium.com/coinmonks/dead-mans-switch-1e9120d4797b)
- [USPTO 11258593 / 11736278 / 12120223 — Dynamic/unpredictable quorum memberships](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11258593)
- [ethereum.org — Gasper](https://ethereum.org/developers/docs/consensus-mechanisms/pos/gasper/)
- [eth2book — Casper FFG](https://eth2book.info/latest/part2/consensus/casper_ffg/)
- [Cube — What is Fork Choice Rule?](https://www.cube.exchange/what-is/fork-choice-rule)
- [CoinTracker — What is a fork in blockchain?](https://www.cointracker.io/learn/fork)
- [SysTutorials — Temporary Forks and Reorganization](https://www.systutorials.com/understanding-temporary-forks-and-reorganization-in-blockchain/)
- [Chainlink — Decentralized Data Model](https://docs.chain.link/architecture-overview/architecture-decentralized-model)
- [gate.com — How Chainlink Works](https://www.gate.com/learn/articles/how-chainlink-works-decentralized-oracle-mechanism/16676)
- [Kleros — Decentralized Justice Protocol](https://medium.com/kleros/kleros-a-decentralized-justice-protocol-for-the-internet-38d596a6300d)
- [gate.com — What Is Kleros (PNK)?](https://www.gate.com/learn/articles/what-is-kleros-all-you-need-to-know-about-pnk/3335)
- [Gemini — Augur Prediction Market & REP](https://www.gemini.com/cryptopedia/augur-prediction-market-rep-coin-augur-betting)
- [Augur whitepaper v2.0 (arXiv 1501.01042)](https://arxiv.org/pdf/1501.01042)
- [EigenAI — Deterministic AI Inference](https://blog.eigencloud.xyz/deterministic-ai-inference-eigenai/)
- [arXiv 2602.00182 — EigenAI: Deterministic Inference, Verifiable Results](https://arxiv.org/html/2602.00182)
- [eco.com — TEEs for AI Agents: Verifiable Compute](https://eco.com/support/en/articles/14796365-tees-for-ai-agents-verifiable-compute)
- [Oasis — Verifiable AI with TEEs](https://oasis.net/blog/verifiable-ai-with-tees)
