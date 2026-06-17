# 674.13 — triad fit: every policy-language part mapped to exactly one engine

*Maps EVERY part of criome's policy language to exactly one of the three triad
engines — SEMA (all durable state), NEXUS (all decision-making), SIGNAL (all
communication) — or marks it as not-criome's. The triad rule is Spirit `3d5z`:
a daemon has no logic outside its engines. The decision rule for the hand-written
boundary is Spirit `t5wx` (only `decide`/`validate` bodies stay hand-written) and
`d3r2` (logic is NOT schema-as-data). The grounding artifacts are the proven
prototype `language-content-addressed-bls/src/language.rs`, the deployed
`signal-criome` wire types, the deployed `master_key.rs` BLS path
(`ATTESTATION_DST`, `verify_bls` blst min-pk), and `src/tables.rs` (nine SEMA
families, no contract/policy family yet).*

## The four-way decision, stated

- **(a) SIGNAL** — public wire vocabulary or a request/reply root. Defined once in
  `signal-criome:lib`; the other engines USE it as a type. A SIGNAL part is a data
  *shape* on the contract, never a behavior.
- **(b) SEMA** — durable state. The contract store, key registry, replay/nonce
  guard, monotonic version/slot counter — anything that must survive a restart and
  be re-loaded by SEMA from persisted state. Today these are the hand-written
  `CriomeTables` families.
- **(c) NEXUS** — decision logic. The hand-written `decide`/`validate` body that
  computes a `Decision` over `Evidence`: evaluate `Rule`, admission/acyclicity
  check, BLS verdict verification, the escalate/non-judgment choice. NEXUS owns the
  *behavior*; it operates over SIGNAL-emitted types and SEMA-loaded state. Per
  `t5wx`/`d3r2` this body is the one part that legitimately stays hand-written —
  it is logic, not schema-as-data.
- **(d) NOT criome's** — belongs to another component. Router transports and
  solicits cross-peer signatures (`wckt`: criome signs/verifies, moves nothing);
  the external adjudicator/Persona runs the LLM/human deliberation; criome only
  verifies the returned signed verdict (auth-only).

## The mapping table

| # | Part | Engine | Why |
|---|---|---|---|
| 1 | Content-addressed `Contract` object (Rule wrapper, identity = blake3(canonical_bytes)) | **SIGNAL** | The composable authorization object IS the wire/state value type. Its address reuses deployed `signal_criome::ObjectDigest`. The *shape* is SIGNAL; computing/checking the address is NEXUS (see #18, #19). |
| 2 | `Rule` enum (closed combinator taxonomy) | **SIGNAL** | The closed not-a-VM operation vocabulary is a public, schema-emitted enum — define-once, shared. Interpreting it is NEXUS; the type itself is SIGNAL. |
| 3 | `SignedBy(Identity)` leaf | **SIGNAL** | A `Rule` variant — wire vocabulary. The verify it triggers is NEXUS (#28). |
| 4 | `All(Vec<ObjectDigest>)` combinator | **SIGNAL** | `Rule` variant (composition by digest). Type only; the AND-fold is NEXUS (#31). |
| 5 | `Any(Vec<ObjectDigest>)` combinator | **SIGNAL** | `Rule` variant (OR by digest). Type only; the OR-fold is NEXUS (#31). |
| 6 | `Threshold` (k-of-n quorum) | **SIGNAL** | A composite wire type (`required_signatures` + `members`). Counting satisfied members is NEXUS. |
| 7 | `PolicyMember` enum (Key/Object member, z9d6 hinge) | **SIGNAL** | Closed enum; the composition-by-digest hinge as a type. |
| 8 | `RequiredSignatureThreshold` leaf (k value) | **SIGNAL** | Already a deployed `signal-criome` newtype. Reused, not re-minted. |
| 9 | `TimedRule` (ActiveAfter / ActiveUntil) | **SIGNAL** | `Rule` variant + composite (boundary + signer). The window comparison is NEXUS. |
| 10 | `TimeSwitch` leaf (two-phase quorum) | **SIGNAL** | Composite wire type (boundary + before/after `Threshold`). The interval-select is NEXUS. |
| 11 | `TimestampNanos` boundary leaf | **SIGNAL** | Deployed `signal-criome` newtype. The comparison against `observed_at` is NEXUS. |
| 12 | `AgreementRule` (divergence/resolution/resolver naming) | **SIGNAL** | `Rule` variant + composite; names three references. Matching + verifying the fact is NEXUS (#33). |
| 13 | `EscalateToPsyche` variant | **SIGNAL** | A `Rule` variant AND a `Decision` variant — non-judgment as first-class output. Type only; choosing to emit it is NEXUS. |
| 14 | `ContractStore` (acyclic DAG, digest→Contract) | **SEMA** | The durable store of admitted contracts — must survive restart and reload. This is the missing `criome-contract` SEMA family (G10). The `Vec`-of-entries in the prototype is the in-memory stand-in. |
| 15 | `ContractStore::admit` (acyclicity/admission check) | **NEXUS** | A `validate` body — rejects a contract referencing an unadmitted digest (`DanglingReference`), guaranteeing a strict DAG. Decision logic over the SEMA store; the *write* it gates lands in SEMA, the *check* is NEXUS. |
| 16 | `referenced_digests` (per-Rule enumeration) | **NEXUS** | Pure logic deriving the directly-referenced sub-objects from a `Rule`; the input the admission check folds over. A `decide`-adjacent helper, hand-written. |
| 17 | `KeyRegistry` (Identity → admitted BlsPublicKey) | **SEMA** | Durable identity↔key bindings (deployed model: cluster-root admission). This is the existing `criome-identity` family — the registry already exists in `tables.rs`; the prototype's in-test `KeyRegistry` is a stand-in for it. |
| 18 | `Identity` enum (Persona/Agent/Host/Developer/Cluster) | **SIGNAL** | Deployed closed `signal-criome` enum — the named identity atom. Resolution to a key is NEXUS-over-SEMA. |
| 19 | Canonical encoding (`CanonicalBytes` trait + domain tags) | **NEXUS** | NOT a fourth concern and NOT a property of the SIGNAL type. It is a deterministic *function* — the `decide`/`validate`-side rendering of a SIGNAL value into its `CRIOME-CONTRACT-V1` preimage. Logic, not data (`d3r2`): the same `Contract` value renders the same bytes by a hand-written method, the way `verify` is hand-written. It belongs to whatever NEXUS body needs the address (admit, evaluate, sign). |
| 20 | blake3 content-addressing itself (`digest = ObjectDigest::from_bytes(canonical_bytes)`) | **NEXUS** | Computing the address is the same NEXUS function family as #19 — `ObjectDigest::from_bytes` IS blake3 (deployed). The *output* (`ObjectDigest`) is a SIGNAL type; the *act of hashing* is decide-side logic. |
| 21 | `OperationDigest` (32-byte blake3 of the authorized operation) | **SIGNAL** | A content-address newtype wrapping the deployed `ObjectDigest` — the wire content the caller's signature covers (carried in `Evidence`). The hashing that mints it is NEXUS (#20). |
| 22 | `OperationStatement` preimage (`CRIOME-OPERATION-AUTHORIZATION-V1`) | **NEXUS** | The domain-tagged signer+operation byte rendering — a signing/verification preimage built identically by signer and verifier. Same canonical-encoding logic family as #19; hand-written decide-side. |
| 23 | `Evidence` (operation digest, observed_at, signatures, agreements) | **SIGNAL** | The evaluation-context input message — a request payload carried on the wire to the evaluator. Type only; consuming it is NEXUS. |
| 24 | `SignatureEnvelope` (`{ scheme, public_key, signature }`) | **SIGNAL** | Deployed `signal-criome` composite, carried in `Evidence`. Replaces honor-system identity lists with verifiable cryptographic material. |
| 25 | `SignatureScheme` guard (reject all but `Bls12_381MinPk`) | **NEXUS** | The *enum* `SignatureScheme` is SIGNAL (#deployed); the *guard* (`matches!(scheme, Bls12_381MinPk)` rejecting algorithm-confusion) is a `validate` predicate inside the verify body. Logic. |
| 26 | `AgreementFact` (reconciliation fact w/ resolver `SignatureEnvelope`) | **SIGNAL** | A composite carried in `Evidence` — the resolver-signed reconciliation datum. Type only; matching+verifying is NEXUS (#33). |
| 27 | BLS verification step (`has_valid_signature_from`) | **NEXUS** | The core verify body: resolve identity→key (SEMA), require envelope key == admitted key, scheme match, deployed `VerifyBls::verify_bls` (blst min-pk, `ATTESTATION_DST`). This is the canonical hand-written `decide`/`validate` (`t5wx`). |
| 28 | (SignedBy verify — same as #27) | **NEXUS** | The leaf evaluation calls #27. |
| 29 | Agreement verification (`has_valid_agreement_for`) | **NEXUS** | Verifies the resolver signed the `CRIOME-RECONCILIATION-V1` preimage — a verify body over `AgreementFact` + `KeyRegistry`. Logic. |
| 30 | `Decision` enum (Authorized / Rejected / EscalateToPsyche) | **SIGNAL** | The typed three-way outcome IS the reply value type. Producing it is NEXUS; the shape is SIGNAL. |
| 31 | `RejectionReason` (SignatureMissing / QuorumShort / OutsideTimeWindow / AgreementMissing) | **SIGNAL** | Typed denial cause carried on the `Decision::Rejected` reply. Type only; deciding which fires is NEXUS. |
| 32 | All/Any propagation (`Decision::all` / `Decision::any`) | **NEXUS** | The short-circuit AND/OR fold that remembers escalation — pure decision logic over `Decision` values. The `decide` body of `All`/`Any`. |
| 33 | `EvaluationError` / `AdmissionError` (folded into crate `Error`) | **NEXUS** | Typed errors distinguishing a malformed graph from a denial — products of the admission/evaluation `decide`/`validate` bodies. (As deployed wire-surfaced reasons they project onto SIGNAL replies like `RequestUnimplemented`, but the distinction is made in NEXUS.) |

### The deferred / divergence parts

| # | Part | Engine | Why |
|---|---|---|---|
| 34 | Attested clock (`ay3y`, DEFERRED G3) | **SEMA + SIGNAL + NEXUS** (no fourth engine) | It reduces cleanly: the monotonic time-period *sequence/counter* is **SEMA** (a slot counter like the existing `criome-attestation-slot`); the quorum-signed *time-period attestation object* the parties co-sign is a **SIGNAL** content-addressed object (verified exactly like any other quorum object); the *comparison* of `observed_at` against the attested window is **NEXUS**. A time authority is "just another criome quorum" — so it needs nothing new. (Prototype: `observed_at` still caller-supplied.) |
| 35 | Replay / branch binding (`ReplayBinding`, DEFERRED G4) | **SIGNAL** (shape) + **SEMA** (state) | The `(object-digest, branch, monotonic-version, attested-moment)` anchor is a **SIGNAL** composite; the durable monotonic-version counter and the consumed-nonce set it anchors against are **SEMA** (the existing `criome-authorization-replay-nonce` family generalizes to it). Binding-check at evaluation is NEXUS. |
| 36 | `Divergence` object (common_base + branches + observed_at) | **SIGNAL** | First-class content-addressed wire/state object describing a network split. Type only. |
| 37 | `ReconciliationPolicy` / `ReconciliationMethod` (Heaviest/Quorum/Oracle/TerminalFork + finality_quorum) | **SIGNAL** | Closed enum + composite — wire vocabulary. Selecting + applying a method is NEXUS. |
| 38 | Signed verdict object (`OracleVerdict` / `Agreement`) | **SIGNAL** | A quorum-signed, content-addressed reconciliation outcome criome only VERIFIES. The verify is NEXUS (#27/#29 family); the object is SIGNAL. criome never recomputes it. |
| 39 | `TerminalFork` object (two named realities) | **SIGNAL** | The honest terminal non-resolution as a recorded wire/state object. Type only. |
| 40 | Fairness-model object (pre-agreed content-addressed spec) | **SIGNAL** | Data criome CARRIES but never interprets — a content-addressed object the verdict's signature covers. The verdict's authority is the signature over THIS object (NEXUS verifies that signature), never raw model output. criome never reads the model semantics → it is purely a SIGNAL-carried, NEXUS-verified blob. |

### The parts that are NOT criome's (engine (d))

| # | Part | Owner | Why not criome |
|---|---|---|---|
| 41 | `EscalateToPsyche` / named-adjudicator OUTCOME (the L2 rung naming an adjudicator) | **SIGNAL (the naming) — boundary** | The *naming* of a quorum/default-LLM/smarter-agent/psyche adjudicator is a SIGNAL value criome emits (#13). But the rung's *action* — actually adjudicating — is (d): criome only emits the escalation outcome and later verifies the returned verdict. |
| 42 | Adjudicator deliberation itself (LLM inference / human judgment) | **(d) — external adjudicator / Persona** | Off-band, non-blocking judgment OUTSIDE criome. criome never runs the model or the human. Verifying the signed result is NEXUS; running it is not criome's. (`auth-only`, `wckt`.) |
| 43 | Default-LLM abstaining posture (non-judgment, competence-gated) | **(d) — external adjudicator** | A property of how the external judge is trained to lean toward escalation. criome neither trains, runs, nor inspects the model's confidence — it only sees a signed verdict or an absence of one. |
| 44 | Cross-peer quorum signature solicitation (panel members signing into a BLS-aggregated proof) | **(d) — Router** | Soliciting and collecting cross-peer signatures is transport/coordination (`wckt`). criome VERIFIES the aggregated quorum proof (NEXUS) but does not solicit or move it. The two-gate (participation + supermajority) check, once the proof arrives, is NEXUS; carrying the solicitation is Router's. |
| 45 | Right-to-escalate gate (New B) | **NEXUS** (criome's) | A correction to the prompt's framing: this is NOT (d). "Who may pull the escalation lever" is itself a policy-gated authority — and gating an authority by policy is exactly a `Rule` evaluation (a `SignedBy`/`Threshold` guarding the escalate path). It is decision logic over SIGNAL types → NEXUS. The thing it gates (the deliberation) is (d); the gate is criome's. |
| 46 | Escalation transport (Router moving query out + signed verdict back via SubmitVerdict) | **(d) — Router** | The off-criome carrier. criome signs/verifies and moves nothing (`auth-only`, `wckt`). The `SubmitVerdict` request head where the verdict re-enters is a SIGNAL input root on criome's contract; the *transport* that delivers it is Router's. |

## What does not fit Signal/Nexus/SEMA, and why that is correct (or a real gap)

Two categories of "does not fit," and they are different in kind.

### Genuinely NOT criome's — and that is correct (engine (d), by design)

These are the auth-only line (`wckt`) and verify-don't-decide line (criome INTENT)
holding exactly where they should. None of them is a gap:

- **Adjudicator deliberation (#42)** — the LLM inference or human judgment. criome
  must never run a model or a human; if it did, it would be non-deterministic and
  would violate auth-only. Correct that it is external.
- **Default-LLM abstaining posture (#43)** — a training/operating property of the
  external judge. criome cannot and must not inspect model confidence; it sees only
  a signed verdict. Correct that it is external.
- **Cross-peer signature solicitation (#44)** and **escalation transport (#46)** —
  moving the query out and the signed verdict back is Router's job. criome verifies
  the returned proof; it carries nothing. This is the single feature that most
  tempts an auth-only violation, and putting transport in (d) is what holds the
  line.

The clean test all four pass: erase criome and the deliberation/transport still has
an owner (the adjudicator, the Router); erase the adjudicator/Router and criome can
still verify a verdict that arrives by any means. The verify is criome's; the
produce-and-carry is not.

### Cross-cutting calls resolved (the ones the brief flagged)

- **Content-addressing / canonical encoding (#19, #20, #22) is NOT a fourth
  concern.** It splits cleanly: the *output type* (`ObjectDigest`) is SIGNAL; the
  *act of rendering canonical bytes and hashing them* is NEXUS logic (a
  hand-written method, like `verify`, per `t5wx`/`d3r2` — logic is not
  schema-as-data). It does not need its own engine and it is not a property of the
  data alone.
- **The attested clock (#34) needs nothing new.** It reduces to a SEMA monotonic
  sequence + a SIGNAL-carried quorum-signed attestation object + a NEXUS comparison.
  A time authority is just another criome quorum — the existing slot-counter and
  quorum-verify machinery already cover it.
- **The fairness-model object (#40) is pure SIGNAL.** criome carries it and lets the
  verdict's signature cover it, but never interprets it. That non-interpretation is
  what keeps criome deterministic and auth-only.

### One genuine GAP inside criome's engines (SEMA, not built)

- **`criome-contract` SEMA family (#14) does not exist in `tables.rs`** (G10). The
  nine deployed families are identity, revocation, attestation, authorization-state,
  authorization-replay-nonce, signature-solicitation, submitted-signature, and two
  slot counters — but the **contract/policy store the language requires is missing**,
  and `ARCHITECTURE` §"Owned" also promises a **policy table** and a **peer-routing
  table** that are likewise absent. The prototype's in-memory `ContractStore`
  `Vec`-of-entries is the stand-in; promoting it to a real SEMA family keyed by
  `ObjectDigest`, with acyclicity enforced at admission, is the concrete
  next-foundational SEMA work. This is the one real, internal gap — everything else
  either fits an engine today or is correctly outside criome.

### One framing correction to the brief

- **The right-to-escalate gate (New B, #45) is NEXUS, not (d).** The brief grouped
  it with the cross-cutting (d) candidates, but gating *who may escalate* is a
  policy evaluation over SIGNAL types — decision logic criome owns. Only the
  deliberation the gate authorizes is (d). The gate is the lever's lock (criome's);
  the deliberation is what happens after the lever is pulled (not criome's).

## Adversarial verification — the corrections that stand

A separate skeptic pass, grounded in the DEPLOYED daemon (not the prototype),
confirmed three of the four cross-cutting calls above and OVERTURNED one. This
section is authoritative where it differs from the optimistic ratings.

- **Content-addressing (#19/#20/#22) — confirmed clean.** Ground truth:
  `RegistrationStatement::to_signing_bytes` (`admission.rs:45`) and
  `AttestationPreimage::to_signing_bytes` (`master_key.rs`) are already hand-written
  domain-tagged byte-renderers, and `ObjectDigest::from_bytes` IS blake3. Calling the
  *act* NEXUS and the *type* SIGNAL is exactly how `verify` is already factored.
- **Escalation output (#13/#30/#45) — confirmed clean.** In `language.rs` the
  evaluator only *returns* `Decision::EscalateToPsyche` — no state write, no emission.
  The durable park + Router prompt lives in the daemon's `AuthorizationStateRecord`
  SEMA family + `meta-signal-criome`: a three-engine *composition*, not a fourth
  concern.
- **Fairness-model blob (#40) — confirmed clean.** Same pattern as the deployed
  `ContentReference.digest`: SIGNAL-carried, signature-covered, never interpreted.
- **The attested clock (#34) — OVERTURNED; this is the one genuine misfit as the code
  stands.** The deployed daemon reads `SystemTime::now()` from a daemon-held
  `SystemClock` (`verifier.rs:95`, `signer.rs:103`) — an ambient, non-deterministic
  side-input the triad models as *no engine*, sitting inside a NEXUS verify body with
  no owner. The prototype papers over it with caller-supplied `Evidence.observed_at`,
  which a verifier cannot trust. `ay3y`'s reduction (time = a SIGNAL attestation
  object + a SEMA sequence + a NEXUS comparison) is the *fix*, but it is **not built**
  — so #34 is downgraded from "fits cleanly" to **fits-awkwardly, conditional on
  building the attested-clock object**. Until that object exists, criome's "now" is
  the one place the triad does not actually hold.

Confirmed gaps: the `criome-contract` SEMA family (#14) is genuinely absent from
`tables.rs` (nine families, none for contracts/policy/peer-routing, though
ARCHITECTURE promises the latter two), and the in-memory `ContractStore` exists only
in the `~/wt` prototype, not in criome main. Both are the next foundational SEMA work.

The bottom line, grounded: nothing in the policy language needs a fourth engine. Of
the parts that "don't fit," the deliberation and transport are correctly other
components (auth-only holding), and the single genuine in-triad misfit is **time** —
which `ay3y` is precisely the plan to fold back in.
