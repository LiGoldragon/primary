# 676.4 — Criome's contract machinery, from the landed code

The perspective file for the contract-machinery comparison: what criome's
authorization machine *is*, grounded in the code that actually exists in the
checkout (not only the reports), and the properties that distinguish it from a
blockchain/smart-contract machine. Every claim is cited to a file+line, a
commit, or a Spirit record. One grounding correction to the briefing/reports is
flagged in §8.

## 0. The one-sentence machine

criome is a **pure validation predicate over content-addressed, immutable policy
objects**: a `Contract` is a closed combinator tree (`Rule`) whose evaluation
against signed `Evidence` yields exactly one of `Authorized | Rejected |
EscalateToPsyche`, with no side effect, no external call, no gas, and no mutation
of anything outside the daemon's own per-user store. It *verifies*; it never
executes, transports, or mutates external state (`wckt`, criome `INTENT.md`).

## 1. Immutable, content-addressed contract objects (identity = digest)

A `Contract` wraps a single `Rule`
(`src/language.rs:10-13`). The full `Rule` vocabulary
(`src/language.rs:15-26`):

```
SignedBy(Identity) | All(Vec<Rule>) | Any(Vec<Rule>) | Threshold | ActiveAfter
| ActiveUntil | TimeSwitch | Agreement | EscalateToPsyche
```

The object model is immutable-by-construction: a contract's identity is the blake3
hash of its canonical bytes (674.15 C4.2, 675 Zoom 5 `z9d6`). The schema reuses
the deployed newtype `ObjectDigest { value String }`
(`signal-criome/schema/lib.schema:47`) as the address type; the same digest type
names composition references inside `AgreementRule`
(`divergence`/`resolution`, `src/language.rs:47-52`). Because the address *is* the
content, there is **no `UpdateContract` verb** — a "change" is a different object
with a different digest. The wire schema confirms this by absence: the entire verb
list (`lib.schema:7-23`) has `RegisterIdentity` / `RevokeIdentity` / `Sign` /
`VerifyAttestation` / `AuthorizeSignalCall` and so on, but no mutate-in-place
operation for any signed object. Revocation is a *new* `IdentityRevocation` record
(`lib.schema:284-288`), not an edit. This is the smart-contract `SELFDESTRUCT` /
storage-slot-write model's exact opposite: nothing is overwritten; identity is
permanent.

Composition is **by digest reference**, never inline mutable state (`z9d6`: deps
"refer to each other's content-addressed contract objects rather than ad hoc
mutable state", 674.15 C4.1). The report-described `PolicyMember::{KeyMember,
ObjectMember}` hinge (a quorum member is a key *or* another object by digest,
674.15 §4.1, 675 Zoom 5) lets a sub-contract be defined once and shared by many
parents — a DAG, not a tree of copies.

## 2. A limited CLOSED combinator language — not a VM, no gas

Per Spirit `vhs2` (Decision): criome's language is "a limited typed policy
language over public-key identity atoms — NOT a general-purpose virtual machine —
drawing its limited-operation discipline from the constrained VMs of Ethereum,
Tezos, and Solana." The discipline shows up structurally:

- **The vocabulary is closed and acyclic.** `Rule` is a fixed enum
  (`language.rs:15-26`); there is no opcode dispatch, no user-supplied bytecode,
  no extension point. A `grep` for `gas|loop|while` in `language.rs` finds **zero**
  loops and zero metering — only the bounded `for` folds inside `Decision::all` /
  `Decision::any` (`language.rs:172-204`) and `Threshold::satisfied_count`
  (`language.rs:222-227`), each over a finite already-materialized `Vec`.
- **Halting is structural, not metered.** The proof the design stayed inside the
  "limited, not a VM" line is precisely the **absence of a gas meter** (674.15
  §1, C2.4; 675 Zoom 5). A closed acyclic combinator vocabulary buys guaranteed
  termination and bit-identical re-evaluation *for free* — there is nothing to
  meter because there is nothing unbounded. Compare Ethereum/Solana, which *must*
  meter (gas / compute units) because their VMs are Turning-expressive and could
  otherwise loop forever.
- **Recursion is bounded by the store.** Acyclic-at-admission (a contract may
  reference only already-admitted digests, since a hash cannot name a
  not-yet-computed hash) makes the reference graph a strict DAG by construction;
  evaluation recursion is bounded by store size (674.15 §3.2, C4.4). No
  reachability analysis, no cycle detector at runtime — the hash ordering enforces
  it.
- **Logic is not schema-as-data.** The combinator *types* are the interface
  (SIGNAL); *interpreting* them is hand-written (`d3r2`, `t5wx`; 674.15 C2.6).
  This is the inverse of EVM, where the contract bytecode IS the data the chain
  stores and the VM interprets arbitrary uploaded logic.

## 3. Evaluation = a pure `validate` predicate (verify, never execute)

`Contract::evaluate(&self, evidence) -> Decision` (`language.rs:80-82`) delegates
to `Rule::decide` (`language.rs:130-156`), a pure recursive match:

- `SignedBy` → `evidence.has_signature_from(identity)` (`language.rs:132`,
  `332-334`) — set-membership in the PoC; the landed/operator path makes this a
  **real BLS12-381 min-pk verify** over the exact operation digest (674.15 §4.1,
  C8.4). The admission gate's `ClusterRoot::admits` is the proof real BLS is wired
  (`src/admission.rs:86-101`): it rejects any non-min-pk scheme
  (`admission.rs:93`), requires the envelope key to equal the configured root key
  (`admission.rs:97`), and calls `verify_bls` over a domain-tagged statement
  (`admission.rs:100`, `CRIOME-REGISTRATION-ADMISSION-V1`).
- `All` / `Any` → folds over child decisions (`language.rs:133-134`).
- `Threshold` → k-of-n count vs `required_signatures` (`language.rs:135`,
  `218-220`).
- `ActiveAfter` / `ActiveUntil` / `TimeSwitch` → compare the evidence's *own*
  timestamp against a boundary (`language.rs:136-150`); never a system clock.
- `Agreement` → membership of a signed reconciliation fact (`language.rs:151-153`,
  `336-338`).
- `EscalateToPsyche` → returns `Decision::EscalateToPsyche` (`language.rs:154`).

The three-valued `Decision` (`language.rs:68-73`) propagates an escalation as a
distinct outcome from rejection: `All` returns `Rejected` on any reject but
surfaces `EscalateToPsyche` if any child escalated and none rejected
(`language.rs:172-187`); `Any` returns `Authorized` on any authorize, else
`EscalateToPsyche` if any child escalated (`language.rs:189-204`). This is the
machine-level expression of "criome verifies; Persona/psyche decides" (`wckt`,
674.15 C3.3): the language can *route to* a human/LLM judgment but cannot *render*
one. criome stays **auth-only** — signs and verifies, never transports (router's
job), never moves objects (mirror's job), never runs an LLM (`wckt`, 675 Zoom 2
table).

## 4. No external calls → no reentrancy possible

Composition is by **digest reference into a local store**, evaluated by reading
already-admitted immutable objects (674.15 §3.2). There is no equivalent of
EVM `CALL`/`DELEGATECALL`: `decide` never invokes another contract's *code* mid-
evaluation, it reads a referenced contract's *value* and folds it. Because (a)
referenced objects are immutable, (b) the graph is a strict acyclic DAG, and (c)
evaluation has no side effects and makes no outbound call, the entire class of
**reentrancy attacks is structurally impossible** — there is no callback surface,
no mutable balance to re-enter, no interleaving of partial state. The DAO-style
bug cannot be expressed in this vocabulary. (This is the sharpest single
distinction from Solidity for the comparison.)

## 5. State lives in a per-daemon SEMA family — not a global ledger

The contract DAG persists in criome's own **SEMA** engine (redb + rkyv), a
single-writer durable store private to that daemon (675 Zoom 1 storage, Zoom 2
runtime triad; engine separation per `3d5z`). criome is **per-Unix-user**: there
is no global consensus chain, no shared world-state, no miners/validators
agreeing on one canonical history. Each criome instance holds its own contract
store and its own key registry. Multi-party trust is achieved by **cross-criome
quorum** — peers trust keys chained to a shared cluster-root (`ermr`, see
`admission.rs` module doc lines 1-18 and §6 below) and co-sign quorum objects —
not by all writing to one ledger. Honest grounding (674.15 C9.5, §4.3, 675 Zoom 5
SEMA box): the `criome-contract` SEMA family keyed by `ObjectDigest` is **the one
genuine in-triad gap** — today the store is an in-memory `Vec` stand-in; `tables.rs`
has nine families and none yet for contracts. So "persisted DAG" is the designed
target; "in-memory DAG with the right shape" is what exists.

## 6. The crystallized-past, quorum-attested clock — no block-clock

There is no block height standing in for time. Per `ay3y` (674.15 §2.6, §3.3,
675 Zoom 5): time is a **decentralized quorum-attested coarse time**, and it is
**crystallized PAST**. An `AttestedMoment` begins as a *proposition* of a forward
window `[start, end]` under a `TimeQuorum`; its identity is the blake3 address of
`(window, quorum)` (signatures are NOT in the address); a quorum co-signs it with
real BLS over a domain-tagged `TimeWindowStatement`; it **crystallizes** when the
count of distinct admitted authorities with a verifying signature reaches the
threshold, yielding a non-forgeable **monotonic lower bound** on now (`now >=
end`). Only the past is provable. A time authority is "just another criome quorum
object." Every quorum-signed object therefore carries an attested moment — the
time-lock leaves compare the operation's *own* proof-of-when, never an ambient
`SystemTime::now()` (674.15 C6.6). In the landed/operator path `Evidence.stamp:
AttestedMoment` is the evaluator's only source of "now," and `TimeNotProven`
distinguishes a sub-quorum stamp from one that merely misses the boundary (675
Zoom 5 §2). This replaces Ethereum's `block.timestamp` (miner-set, trust-the-
proposer) and Bitcoin's median-of-11 block-time with a quorum-signed lower bound.
(The in-tree `language.rs` PoC still carries the simpler `Evidence.observed_at:
TimestampNanos`, `language.rs:55-59`, `328-330` — the attested-moment envelope is
the operator/G3-G4 reshape, not yet in this file.)

## 7. Divergence → an adjudicator ladder ending in escalate / terminal fork

Network splits are not resolved by mining/staking fork-choice (longest chain /
heaviest stake). criome resolves them by an **adjudicator ladder** (`gc0n`,
`vhs2`; 674.15 §3.4-3.5, 675 Zoom 5 §3):

- **L0 mechanical** — quorum / timelock / attested-time / threshold; criome stays
  here, *verifying* a signed verdict and moving nothing.
- **L1 quorum vote** — two-gate participation + supermajority.
- **L2 named adjudicator** — a quorum, a default-LLM (trained to lean to
  *non-judgment*: abstain + escalate, `gc0n` C7.2-C7.3), a smarter agent, or the
  psyche, signing a content-addressed verdict against a *pre-agreed fairness-model
  object* the signature covers. criome verifies the quorum proof; it **never runs
  the model** (the Chainlink-oracle pattern; the provider is itself a criome quorum
  object, closing authority into the same vocabulary, `vhs2` C7.6).
- **L3 terminal fork** — two named realities, honest non-resolution, when nothing
  converges and no pre-fork-anchored authority can rule.

The `Agreement` rule (`language.rs:47-52`, `277-303`) is the in-code seed:
it carries `divergence`, `resolution`, and a `resolver` identity, and is satisfied
only by a matching signed `AgreementFact` (`language.rs:286-290`, `336-338`). The
top rung is `EscalateToPsyche` — the psyche is the highest-authority,
lowest-availability adjudicator, the literal expression of intent-is-primordial
(`gc0n` C7.4). Where a blockchain's regress ("who decides who decides?") bottoms
out in economic majority, criome's bottoms out by pinning the resolver to a
**pre-fork common ancestor** both sides accepted before the split — a judge cannot
rule on its own legitimacy, so governance schisms terminate honestly at L3 rather
than being decided by whoever has more hash power.

## 8. Grounding correction to the briefing/reports

The briefing and reports 674.15 §7 / 675 Zoom 5 / the 675 "Closing" diagram state
the schema-first policy surface (`AdmitContract` / `LookupContract` /
`EvaluateAuthorization`, `Contract` / `Rule` / `PolicyMember` as schema-emitted
SIGNAL types) **landed on criome main**. In *this* checkout it has **not**:
`grep -liE 'AdmitContract|EvaluateAuthorization|PolicyMember'` over
`signal-criome/schema/` returns nothing; `lib.schema` carries only the auth /
attestation / authorization-grant surface (verbs `lib.schema:7-23`). The contract
language lives entirely in the **hand-Rust PoC** `src/language.rs` (committed
`865f8b3` "add Crayome language policy POC", `a04157a` naming fix, `9719703`
"add explicit psyche escalation outcome"; HEAD `9719703`, detached). So for the
comparison: the *machinery shape* is exactly as described and grounded above, but
its current embodiment is the in-tree `language.rs` enum + `decide` evaluator, not
a generated schema surface. The reports' "landed" status reflects operator 408/409
work on a branch not present in this working tree (or since diverged). Whoever
synthesizes 676 should describe criome's contract machine from `language.rs` +
`admission.rs` as the ground truth and treat the schema-emitted surface as the
designed-not-here-landed target.

## 9. The distinguishing properties, condensed (for the comparison table)

| Property | criome | typical blockchain/smart-contract VM |
|---|---|---|
| Contract identity | `blake3(canonical bytes)` = digest; immutable; no update verb | deployed address; mutable storage; upgradeable proxies |
| Language | closed acyclic combinator enum (`Rule`) | Turing-expressive bytecode (EVM/BPF/Michelson) |
| Halting | structural (closed vocabulary) — **no gas** | metered (gas / compute units) |
| Evaluation | pure `validate` predicate → `Authorized\|Rejected\|EscalateToPsyche` | stateful execution mutating world-state |
| External calls | none (digest reads of immutable objects) → **no reentrancy** | `CALL`/`DELEGATECALL` → reentrancy class exists |
| State | per-daemon SEMA family (redb+rkyv), per-Unix-user; cross-criome quorum | one global consensus ledger / world-state |
| Clock | quorum-attested crystallized-PAST lower bound (`ay3y`) | block height / `block.timestamp` |
| Fork resolution | adjudicator ladder → escalate-to-psyche / terminal fork | mining/staking fork-choice (longest/heaviest) |
| Role | auth-only: verifies signed verdicts, runs/transports nothing (`wckt`) | executes arbitrary uploaded logic, holds value |

## Sources

Code (checkout `/git/github.com/LiGoldragon/criome`, HEAD `9719703`, detached):
`src/language.rs:10-357` (the whole `Rule`/`Contract`/`Decision`/`Evidence`
model + `decide`), `src/admission.rs:1-101` (real BLS cluster-root admission gate,
`CRIOME-REGISTRATION-ADMISSION-V1`); `signal-criome/schema/lib.schema:1-362`
(wire surface, `ObjectDigest:47`, verb roots `7-23`, no contract/update verb).
Reports: `674-criome-internal-engine/15-implementation-architecture-and-constraints.md`,
`675-system-with-perspective/6-system-map.md`. Spirit records cited inline:
`vhs2` (limited-not-a-VM), `wckt` (auth-only), `z9d6` (content-addressed composable
objects), `ay3y` (crystallized-past quorum clock), `gc0n` (adjudicator ladder),
`ermr` (cluster-root admission), `3d5z` (engine separation), `d3r2`/`t5wx`
(logic hand-written, not schema-as-data). Web (concept grounding only, confirms
the blockchain-side framing): content-addressing keyed by BLAKE3 immutable stores
(S5 / Lore VCS), capability authorization lifecycle (BlendCAC, arXiv 1804.09267).
