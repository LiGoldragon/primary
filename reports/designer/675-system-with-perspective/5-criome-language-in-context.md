# 675.5 — criome's policy language in context, now on main

Grounded wide-angle perspective for the 675 system-with-perspective session.
Everything below is read from real source: the 674 capstone, operator 408/409,
and the actual landed commits on `origin/main` of `signal-criome` and `criome`.

## 0. Confirmed landing (commit ids)

The brief's expected tips are **real and on `origin/main`** of both repos. The
local checkouts at `/git/...` are stale (detached HEAD at older commits:
signal-criome `374d833`, criome `9719703`), but the expected commits exist as
objects and `git branch -a --contains` puts both on `remotes/origin/main`.

| Repo | Expected main tip | Subject | Date |
|---|---|---|---|
| `signal-criome` | `f10fb54d` | `signal-criome: align attested moment evidence naming` | 2026-06-17 |
| `criome` | `cd1de18f` | `criome: repin policy stamp integration to signal-criome main` | 2026-06-17 |

Landed lineage on each main:

- **signal-criome main**: `fb3fa44 → 8c76cce → 455329b → 836393e → 20ed63d →
  947f271 (policy contract wire surface) → 8459fb4 (attested moment policy
  evidence) → f10fb54d (align naming)`.
- **criome main**: `865f8b3 (language POC) → 132f620 → a04157a → 9719703 (psyche
  escalation outcome) → 03d2b32 (evaluate schema-emitted contracts) → 92a703b
  (bind to attested moments) → d304b24 (align stamp semantics) → cd1de18f (repin
  to signal-criome main)`.

These are the **operator/criome-policy-triad-schema** (408) and
**operator/criome-attested-moment** (409) branch sequences, now integrated to
main — the schema-first landing plus the attested-moment stamp are both in.

### The two load-bearing landed facts the brief named

1. **`Evidence.stamp: AttestedMoment`** (replacing `observed_at`) is in the
   landed schema. From `signal-criome` `f10fb54d:schema/lib.schema` (verbatim):

   ```nota
   Evidence {
     operation OperationDigest
     stamp AttestedMoment
     signatures (Vector SignatureEnvelope)
     agreements (Vector AgreementFact)
   }
   ```

   Note: operator 409's report still showed the field named `observed_at`; the
   final `f10fb54d` "align naming" commit renamed it to `stamp`, matching the
   674.14 designer envelope vocabulary. The two lanes converged on the name.

2. **`TimeNotProven`** is a landed rejection reason. From the same schema:

   ```nota
   EvaluationRejectionReason [
     (SignatureMissing Identity)
     (QuorumShort QuorumShortfall)
     OutsideTimeWindow
     TimeNotProven
     AgreementMissing
   ]
   ```

   And the NEXUS body in `criome` `cd1de18f:src/language.rs` returns it from
   `AttestedMomentVerification::rejection_reason` (a real trait impl on
   `AttestedMoment`, line 551): a malformed or quorum-short / forged-signature
   stamp yields `Some(EvaluationRejectionReason::TimeNotProven)`. The evaluator's
   gate is `if let Some(reason) = evidence.stamp.rejection_reason(registry)`
   (line 134) — invalid time is rejected **before** the policy rule runs.

## 1. WHERE the policy language sits in the system

criome is the **Nexus authorization layer** of the component triad — the auth
step that signs and verifies, and nothing else. Its place is fixed by three
landed/recorded boundaries:

- **Auth-only (`wckt`, criome INTENT).** criome signs and verifies; it never
  transports (that is the router) and never version-controls or moves objects
  (that is the mirror). It also never runs an LLM or a human — it only *verifies*
  a signed verdict that one produced.
- **A limited typed policy language, never a VM (`vhs2`).** The language is a
  closed, acyclic combinator vocabulary over public-key identity atoms. The proof
  it stayed inside the line is the **absence of a gas meter**: a closed acyclic
  vocabulary buys guaranteed halting and bit-identical re-evaluation without
  metering. Discipline drawn from Ethereum/Tezos/Solana constrained VMs.
- **Built on content-addressed composable objects (`z9d6`).** A `Contract`'s
  identity *is* `blake3(canonical_bytes)`; composition references sub-objects by
  digest, never inline. A quorum member is a key **or** another object by digest
  (`PolicyMember::{KeyMember, ObjectMember}`) — the hinge that lets a panel be
  defined once and shared by many parents. Acyclic-at-admission makes the
  reference graph a strict DAG, so evaluation recursion is bounded for free.

The three sub-structures the brief named, located precisely:

1. **The limited typed policy language** — `signal_criome::{Contract, Rule,
   PolicyMember, Threshold, TimedRule, TimeSwitch, AgreementRule}`. SIGNAL owns
   the closed type vocabulary (schema-emitted); criome's NEXUS owns the
   hand-written `decide`/`validate` bodies that interpret it (`t5wx`/`d3r2`: logic
   is not schema-as-data). The combinator set is `SignedBy` (one real BLS verify),
   `Threshold` (k-of-n), `All`/`Any` (AND/OR over digests), `ActiveAfter` /
   `ActiveUntil` / `TimeSwitch` (time leaves over the stamp), `Agreement` (signed
   reconciliation), `EscalateToPsyche` (non-judgment outcome).

2. **The attested-clock stamped envelope (`ay3y`).** "Now" never comes from a
   system clock inside the language path. An `AttestedMoment` is a quorum-attested
   **crystallized-past** time object: a `TimeWindow [opens_at, closes_at]` under an
   `AttestedMomentProposition` (window + threshold + authorities), content-addressed
   by the proposition; `TimeSignature`s accrete; once enough distinct admitted
   authorities really-verify, it crystallizes into a monotonic lower bound proving
   `now >= closes_at`. Only the past is provable. Time-locks compare against
   `evidence.stamp.closes_at()` — `ActiveAfter(T)` holds iff `closes_at >= T`,
   `ActiveUntil(T)` iff `closes_at < T` (both landed in `language.rs` lines 288/297).

3. **The adjudicator / escalation ladder (`gc0n`).** criome itself stays at the
   bottom rung (L0 mechanical: it verifies a signed verdict, moves nothing).
   Above it: L1 quorum vote, L2 named adjudicator (mechanical quorum / default-LLM
   leaning to non-judgment / smarter agent / psyche) signing a content-addressed
   verdict against a pre-agreed fairness-model object, L3 terminal fork as honest
   non-resolution. Competence-gated not failure-gated; the psyche is the
   highest-authority, lowest-availability rung — escalate-to-psyche is the literal
   expression of intent-is-primordial. The right-to-escalate gate is itself a
   `Rule` (NEXUS); only the deliberation it authorizes is external.

## 2. LANDED on main vs DESIGNED / DEFERRED

### Landed on main (provably, in f10fb54d / cd1de18f)

- **Schema-first public policy surface in `signal-criome`** — `Contract`, `Rule`,
  `PolicyMember`, `Threshold`, `Evidence`, `SignatureEnvelope`, `ContractDigest`,
  `OperationDigest`, `EvaluationDecision`, `EvaluationRejectionReason`; verbs
  `AdmitContract` / `LookupContract` / `EvaluateAuthorization` with reply roots
  (`ContractAdmitted`, `AuthorizationEvaluated`, …). Generated to Rust. This
  **supersedes the hand-Rust `language.rs` split** the 674.11 designer prototype
  used — content-addressing and the type vocabulary now live in the schema
  (`xbc2`/`a71r` realized). The duplicate `criome.language.schema` is retired to a
  placement note pointing at signal-criome as the owner.
- **criome NEXUS evaluator over the generated nouns** — `criome/src/language.rs`
  evaluates `signal_criome::{Contract, Rule, Evidence, EvaluationDecision}`
  directly: content-addressed admission, dangling-reference rejection, duplicate
  quorum-member rejection, real BLS verify via deployed `MasterKey`/`VerifyBls`,
  quorum / time-window / object-member / agreement / `EscalateToPsyche`.
- **`Evidence.stamp: AttestedMoment`** — the attested-clock object is in the
  public schema and the evaluator's only source of "now"; no `SystemTime::now()`
  in the language path.
- **`TimeNotProven`** — a quorum-short or forged-signature stamp is distinguished
  from a stamp that merely misses the boundary (`OutsideTimeWindow`).
- **Replay binding to the attested moment** — `OperationStatement::to_signing_bytes`
  (landed, `language.rs` line ~516, called from `has_valid_signature_from`) builds
  the domain-tagged preimage `CRIOME-OPERATION-AUTHORIZATION-V1` covering the
  signer, the operation digest, **and the attested-moment proposition digest**, so
  a valid signature under one crystallized moment cannot be replayed under another.
  Test `operation_signature_is_bound_to_the_attested_moment` proves it.
- **Daemon-root request path** — `src/actors/root.rs` handles `AdmitContract` /
  `LookupContract` / `EvaluateAuthorization`, builds a `KeyRegistry` from the
  identity registry, and proves a real registered BLS key authorizes a
  schema-emitted contract through the actor, not only in unit tests. Nix
  `test-nota-text` green: 17 (signal-criome) + 51 (criome).

### Designed / deferred (not on main)

- **SEMA contract family** — the contract store is **in-memory** in the landed
  slice (a `Vec` stand-in). The `criome-contract` family keyed by `ContractDigest`
  — persist the admitted DAG, restore across restart, make `LookupContract` /
  `EvaluateAuthorization` read durable state — is the one genuine in-triad gap
  (capstone §5/§6 step 2; `C9.5`). `tables.rs` has nine families today, none for
  contracts/policy.
- **Replay / branch binding full anchor** — the *attested-moment* leg of the
  replay anchor is landed; the full `(object-digest, branch, monotonic-version,
  attested-moment)` quad (branch + monotonic version in the signed preimage) is
  deferred (`C8.6`, capstone G4).
- **Output-side stamping** — both lanes stamped only the *input* `Evidence`.
  `ay3y` says "every triad input AND output." Operator 409's explicit next step:
  not hand-adding `AttestedMoment` to every root, but a shared **stamped frame/
  envelope** in the signal-frame / generated triad-frame layer so every
  Input/Output/Event carries the stamp uniformly; migrate deployed
  `Attestation.issued_at`/`expires_at` off `SystemClock` (`C6.6`).
- **Full named-adjudicator ladder** — only `EscalateToPsyche` is landed as a
  rung. The named-adjudicator ladder beyond psyche (mechanical-quorum /
  abstaining-default-LLM / smarter-agent), the two-gate quorum vote, the
  divergence/oracle/fork objects with resolver pinned to a pre-fork ancestor, and
  the terminal fork are **designed** (capstone §3.4/§3.5, `gc0n`, 674.9), signature
  path proven, objects not built.
- **Window-expiry close path, partition gap-widening** — descriptive only; no
  wall-clock and no network in the PoC.
- **Meta-policy surface** — `meta-signal-criome` unchanged; a future
  `DefineContract` / `AmendContract` governance surface would live there (`7sx6`:
  exactly two contracts, no third).

## 3. How it plugs into the e2e chain (the criome auth step of `d6he`)

`d6he` fixes the first end-to-end milestone order: **spirit → vcs → criome →
router → mirror** (capstone C3.6; confirmed in
`reports/system-designer/126` line 152 and `128` line 29). criome is the
**third step — the authorization gate**. The clarified `d6he` flow (system-designer
128): Spirit accepts a log object, asks the **local** criome to authenticate the
exact content-addressed object/event; criome trusts the local structural request
boundary, validates the Spirit-shaped request, **signs/authorizes** it; then
propagation goes through Router to remote criome/mirror participants.

Concretely the plug-in point is `EvaluateAuthorization(AuthorizationEvaluation {
contract: ContractDigest, evidence: Evidence })`: the caller (Spirit/vcs) submits
the content-addressed operation digest plus the stamp and signatures; criome
returns `AuthorizationEvaluated { decision }` where `decision` is `Authorized` /
`Rejected(reason)` / `EscalateToPsyche`. criome authenticates the **submitter**
(SO_PEERCRED caller → registered Identity, after-the-fact non-blocking
attestation; `2st7`) and authorizes the **exact content-addressed digest**
(`w2g3`). On `Authorized`, the router transports the signed object onward; criome
moves nothing. On `EscalateToPsyche`, the auth step defers up the ladder rather
than forcing a verdict.

So criome's landed policy language is exactly the typed, deterministic,
content-addressed, attested-time-stamped **authorization step** that sits between
the version-control substrate and the transport layer in the d6he chain — auth
only, verify-don't-decide, with the past (and only the past) provable.

## Sources (real paths + commit ids)

- `reports/designer/674-criome-internal-engine/15-implementation-architecture-and-constraints.md` (capstone).
- `reports/operator/408-criome-policy-triad-schema-branches.md` (schema-first landing).
- `reports/operator/409-criome-attested-moment-architecture-and-poc.md` (attested-moment PoC; note: report shows the pre-rename `observed_at`).
- `reports/system-designer/126-mirror-notify-worker.md` (d6he order, line 152), `reports/system-designer/128-spirit-criome-router-mirror-poc-push-2026-06-17.md` (d6he clarified, line 29).
- `signal-criome` `f10fb54d:schema/lib.schema` — `Evidence.stamp`, `AttestedMoment`, `TimeNotProven` (verified verbatim).
- `criome` `cd1de18f:src/language.rs` — `AttestedMomentVerification` trait impl, `rejection_reason` → `TimeNotProven`, `OperationStatement::to_signing_bytes` replay binding, `ActiveAfter`/`ActiveUntil` over `stamp.closes_at()` (verified verbatim).
- Both expected commits confirmed via `git branch -a --contains` on `remotes/origin/main` (local checkouts are stale detached HEADs).
