# 674.3 — What Ethereum, Tezos, and Solana teach a LIMITED identity policy language

Research-chain agent. Web access: WebSearch + WebFetch (both live). All claims
below are sourced to public documentation, cited inline. Where I extrapolate a
design transfer beyond what a source states, I mark it **[transfer]**.

## The frame this serves (and the line that is fixed)

criome's internal language is a **limited typed policy language over public-key
identity atoms — NOT a general-purpose VM** (Spirit `vhs2`). It takes the
*limited-operation discipline* of the EVM / Michelson / Solana runtime, not
their generality; it stays auth-only (`wckt`); it builds on z9d6
content-addressed composable authorization objects; it is criome's Nexus
object/verb vocabulary, not a fourth engine.

So the research question is narrow: from each chain, **what transfers to a
limited typed identity policy language over public keys** in four buckets —
(1) identity/account models, (2) multisig/threshold authorization, (3) timelock
primitives, (4) divergence/upgrade governance. Everything else (token transfer,
fee markets, consensus, generic computation) is explicitly out — criome never
transports and never runs arbitrary code.

The meta-lesson, stated up front: **all three chains separate a cheap, bounded,
side-effect-free "may this act?" check from the expensive, general "do the act"
step.** criome only ever wants the first half. That boundary — validation vs.
execution — is the single most important transfer, and ERC-4337 names it most
cleanly.

## 1. Ethereum

### 1a. Two account kinds: keyed atoms vs. code-controlled objects

Ethereum has exactly two account types. **Externally-Owned Accounts (EOAs)** are
"composed of cryptographic pairs of private and public keys," can *initiate*
transactions, and that is all they can do — "EOAs can only initiate simple
transactions and approvals since they can't understand or execute code."
**Contract accounts** have "associated code and data storage, but not private
keys," cannot initiate anything ("they can only react"), and "control themselves
in the way determined by their smart contract code"
([ethereum.org accounts](https://ethereum.org/developers/docs/accounts/),
[Ambire EOA vs SCA](https://blog.ambire.com/eoas-vs-smart-contract-accounts/),
[Ethereum Classic EOA/contract](https://ethereumclassic.org/blog/2024-07-23-what-are-externally-owned-addresses-and-contract-addresses-in-ethereum-classic/)).

**Transfer.** This is exactly criome's two-layer shape and validates `vhs2`'s
phrasing. The keyed account = criome's **public-key identity atom** (the
irreducible signing leaf). The code-controlled account = criome's **composable
authorization object / identity contract** (z9d6): no key of its own, "controls
itself" by a policy that references other accepted objects. Note what does *not*
transfer: a contract account's policy is arbitrary Turing-ish code. criome's is
a *closed vocabulary* of quorum + timelock + time-varying-threshold +
reconciliation. The split (keyed-leaf vs. policy-object-with-no-key) transfers;
the open-endedness of the policy does not.

### 1b. The EVM's bounded-operation discipline (the "not-a-VM" lesson, inverted)

The EVM is "quasi-Turing-complete because gas ensures that execution halts when
the budget runs out." Every opcode has a fixed gas cost; "execution is
guaranteed to halt deterministically when the budget runs out"; out-of-gas
"immediately halts execution and reverts all state changes." And determinism is
foundational: "given the same inputs and the same blockchain state, execution
results must be identical regardless of when or where the code runs"
([Gate: what is the EVM](https://www.gate.com/learn/articles/what-is-ethereum-virtual-machine-evm/16798),
[Cube: deterministic execution](https://www.cube.exchange/what-is/deterministic-execution)).

**Transfer.** Ethereum needed gas *because* it chose Turing-completeness and then
had to bolt on a halting bound. criome inverts the trade: by choosing a **closed,
non-recursive, structurally-bounded vocabulary** (a finite set of policy
combinators over a finite key set), evaluation is **total by construction** — it
terminates and is deterministic without any gas meter, fuel counter, or
step-limit. That is the precise payoff of "limited typed policy language, not a
VM": you get the EVM's two prized properties (guaranteed halting + bit-identical
re-evaluation across nodes) *for free*, and you should advertise the *absence* of
a gas mechanism as the proof you stayed inside the line. **[transfer]** Concretely:
no opcode loops, no unbounded recursion in object references (the
content-addressed reference DAG must be acyclic — a content hash cannot reference
its own future hash, which gives acyclicity for free), and a bounded fan-out so
a policy tree's evaluation cost is a static function of its size.

### 1c. Gnosis Safe / Safe — the canonical M-of-N object

A Safe "stores an array of owner addresses and a uint256 threshold. To execute a
transaction, the Safe verifies that signatures from at least `threshold` owners
are present, valid, and ordered correctly" — an **M-of-N** config where M is the
threshold and N the owner count. Owners and threshold are both mutable
configuration
([Bitbond Safe guide](https://www.bitbond.com/resources/gnosis-safe-multisig-guide-for-projects),
[Tally Gnosis Safe](https://docs.tally.xyz/set-up-and-technical-documentation/using-governor-with-gnosis-safe/gnosis-safe/)).

**Transfer.** This is criome's **k-of-n signature quorum** primitive verbatim
(vhs2: "signature quorums of k-of-n form"). Two design notes worth importing:
(i) signatures must be *ordered/canonicalized* so dedup and verification are
deterministic — adopt a canonical ordering of identity atoms by their public-key
bytes so a quorum proof has one normal form. (ii) An owner of a Safe can itself
*be another Safe* — Safes nest. That is exactly z9d6 "each component can decide
acceptance based on another accepted object": a criome quorum's members are
themselves identity atoms **or** other authorization objects, composing
recursively (acyclically, per 1b).

### 1d. ERC-4337 account abstraction — the validation/execution boundary

The single cleanest articulation of the boundary criome lives on. ERC-4337
mandates "a clean separation between validation (acceptance of UserOperation, and
acceptance to pay) and execution," enforced by the EntryPoint as "a strict
two-phase pattern: verification first, then execution." Accounts expose
`validateUserOp`, which "verifies the signature." Critically, the **validation
phase is deliberately restricted**: it "cannot read storage from arbitrary
contracts, cannot call CREATE2 ... cannot make external calls that read mutable
state," precisely so a bundler "can simulate the validation step, decide if the
UserOp is valid, and trust that on-chain validation will produce the same
result." The stated motivation is DoS safety — proving an op is acceptable
*without* running the whole op
([EIP-4337](https://eips.ethereum.org/EIPS/eip-4337),
[Hacken AA overview](https://hacken.io/discover/erc-4337-account-abstraction/)).

**Transfer (the keystone).** criome IS the restricted validation half, made into
the whole language. criome's authorization evaluation = `validateUserOp` with
the restrictions promoted from convention to *type-level law*: a criome policy
**cannot transport, cannot mutate external state, cannot call out** except
through the one explicit, typed escape hatch (the LLM-oracle reconciliation call,
§4) — and that hatch is itself resolved by another criome authorization object,
so the closure holds. "criome signs and verifies, never transports" (`wckt`) is
the same boundary ERC-4337 draws between validate and execute, made absolute.
The pure, simulatable, side-effect-free validation predicate is the model
criome's Nexus engine should match. **[transfer]**

### 1e. OpenZeppelin TimelockController — the timelock state machine

Operations follow a fixed lifecycle: `Unset → Pending → Ready → Done`. An
operation is "identified by a unique id (their hash)" computed over `{target,
value, data, predecessor, salt}`. `minDelay` "acts as a buffer from when a
proposer schedules an operation to the earliest point at which an executor may
execute." Three roles: **PROPOSER** (schedules and cancels), **EXECUTOR**
(executes after delay; may be the zero address = anyone), **ADMIN** (manages
roles, then renounces). **Predecessor** lets one op "depend on another operation,
forcing the execution order"; **salt** disambiguates otherwise-identical ops;
batches (`scheduleBatch`/`executeBatch`) run atomically
([OZ governance API](https://docs.openzeppelin.com/contracts/4.x/api/governance#TimelockController),
[OZ timelock roles](https://docs.openzeppelin.com/defender/guide/timelock-roles)).

**Transfer.** This gives criome a ready-made **timelock primitive** with the
right vocabulary: a scheduled authorization is a content-hash-identified object
(z9d6 native — the op id IS its content address) with a `not-before` time and a
four-state lifecycle. The role split (who may schedule vs. who may execute vs.
who may *cancel before maturity*) is itself a small policy — and cancellation
before maturity is the security purpose of a timelock (a window to react), so
criome's timelock object should carry an explicit *veto/cancel quorum* distinct
from the execute quorum. The **predecessor** mechanism is how you express
ordered, multi-step authorization (e.g. "rotate the master key only after the
quorum-change op has matured") without any loop or scripting — pure DAG
ordering, which stays inside the limited-language line. **[transfer]**

## 2. Tezos

### 2a. Michelson — restriction as a *positive* design choice

Michelson is "a stack-based language à la Forth with strict static type checking
and high-level data structures à la ML." It is "statically typed to ensure the
well-formedness of the stack at any point"; types of input/output stacks are
"fixed and monomorphic," and the program is "typechecked before being introduced
into the system." The payoff is stated as a guarantee: "No smart contract
execution can fail because an instruction has been executed on a stack of
unexpected length or contents," yielding "a rather simple interpreter with simple
cost model"
([Michelson docs](https://tezos.gitlab.io/active/michelson.html),
[docs.tezos.com Michelson](https://docs.tezos.com/smart-contracts/languages/michelson)).

**Transfer.** Michelson is the closest spiritual sibling to criome's intent:
*deliberately* restricted, typed-before-admission, with whole-program type
checking that rules out entire failure classes statically. The lesson is the
mindset — restriction is the feature, not a limitation grudgingly accepted. For
criome: a policy object should be **typechecked at content-addressing time**
(when it is hashed and admitted), so an admitted authorization object is
*statically known* to be a well-formed, total predicate over identity atoms.
"Typecheck before admission" maps onto "validate before content-address." The
monomorphic-stack discipline → criome's combinators have fixed, declared
input/output kinds (a quorum takes N member-objects + a threshold, yields a
verdict), so composition is checkable structurally. **[transfer]**

### 2b. Tezos built-in / generic multisig — keys, threshold, and replay binding

Owners "are represented by their cryptographic public keys, and a pre-defined
threshold (a natural number between 1 and the number of owners) of them must
agree." Agreement = a cryptographic signature of the action. Anti-replay is
explicit and three-part: signed data "needs to contain the address of the
multisig contract (to avoid replaying signatures meant for another contract), the
chain identifier of the current chain (to avoid replaying signatures between the
test chain and the main chain), and an always-increasing anti-replay counter."
The counter is "stored in the contract storage and incremented at each successful
call." The generic multisig can itself "change the threshold and the list of
owner public keys"
([Octez built-in multisig](https://octez.tezos.com/docs/user/multisig.html),
[docs.tezos.com multisig](https://docs.tezos.com/smart-contracts/multisig)).

**Transfer (and a direct hit on the divergence problem).** Beyond confirming the
k-of-n-over-public-keys model, the **three-part replay binding is a gift for the
divergence-reconciliation design.** Tezos already binds every signature to
*(contract identity, chain identity, monotonic counter)* precisely so a signature
valid on the main chain is **invalid on a forked/test chain**. That is the
network-divergence problem solved at the signature layer: a criome authorization
proof should bind to **(authorization-object content-hash, network/branch
identity, monotonic version)** so a quorum gathered on one side of a split
**cannot be replayed on the other** — which is exactly what makes a "divergence
object" meaningful rather than ambiguous. The monotonic counter also gives
criome a clean **time/version ordering** for time-varying-threshold policies
without a wall clock. **[transfer]**

### 2c. On-chain self-amendment — the canonical divergence-avoidance machine

This is the closest analog in all of crypto to criome's "reconcile when networks
diverge." Tezos is "self-amending ... without the need to hard fork," via a
five-period state machine, each ~14 days: **Proposal** (delegates submit and
upvote; up to 20 proposals each; top proposal by voting power advances if quorum
met) → **Exploration** (Yea/Nay/Pass vote; advances only if **both** a dynamic
**quorum** of all voting power participates **and** a **supermajority** — "the
total voting power of the Yea votes must be greater than 80% of the total voting
power of the Yea and Nay votes combined") → **Cooldown** (test the proposal on
temporary networks) → **Promotion** (final binding vote, same quorum +
supermajority) → **Adoption** (infrastructure window; "at the end of the Adoption
period, Mainnet automatically enables the new protocol"). Voting power = staked +
delegated tez
([docs.tezos.com governance](https://docs.tezos.com/architecture/governance),
[Arluck: Amending Tezos](https://medium.com/tezos/amending-tezos-b77949d97e1e),
[Octez voting](https://octez.tezos.com/docs/active/voting.html)).

**Transfer (the divergence model).** Tezos's whole reason to exist is "resolve
contention *on-chain* so the network never has to split." That is `vhs2`'s
divergence-reconciliation in mature form. Importable structure:
1. **A divergence/amendment object is itself a timed, multi-period state machine**
   — not a single vote. criome's reconciliation object should have explicit
   phases (propose a resolution → gather a weighted quorum → cooldown/contest →
   activate) rather than one instantaneous decision. Each phase boundary is a
   timelock (§1e) and each gate is a quorum (§1c/2b).
2. **Two gates, not one: participation (quorum) AND agreement (supermajority).**
   A criome reconciliation should require *both* "enough of the weighted identity
   set showed up" and "a supermajority of those agreed" — guards against a small
   faction reconciling unilaterally during a split.
3. **Weighted voting power** generalizes flat k-of-n: members carry weights
   (stake-analog). criome's quorum primitive should admit *weighted* thresholds,
   making flat k-of-n the unit-weight special case. **[transfer]**
4. **Automatic, deterministic activation** at the end of the window — no
   off-chain coordination — is what actually *prevents* the fork. criome's
   reconciliation must resolve to a single deterministic verdict that all honest
   replicas reach independently; the LLM-oracle (§4 / report 4) is invoked
   *inside* such a gate, and the oracle provider is itself selected by a criome
   identity contract (e.g. a paid expert panel as a weighted quorum), keeping the
   whole loop inside the limited language.

## 3. Solana

### 3a. Account model — single uniform account, ownership by program

Solana has one account type; differentiation is by **owner**: "only the account's
owner program can modify its data," and "by default, all accounts ... are owned
by the system program," with ownership transferable
([Chainstack account model](https://chainstack.com/solana-architecture-account-model-and-transactions/),
[Solana PDA docs](https://solana.com/docs/core/pda)).

**Transfer.** The clean idea: **identity = an address + a controlling authority,
where the authority is itself an object, not necessarily a key.** This reinforces
the z9d6 substrate — an authorization object's "owner"/controller is another
accepted object. Solana's "only the owner may modify" is the access-control
invariant criome wants: only the controlling policy may alter an identity
object's configuration (rotate keys, change threshold), and that controller is
expressed in the same vocabulary.

### 3b. Program-Derived Addresses — deterministic identity with NO private key

The standout transferable primitive. PDAs are "32-byte account addresses that are
deterministically derived from a program ID and a set of seeds," and are
"guaranteed to not lie on the Ed25519 curve, which means no private key exists
for them." Derivation: "hashing seeds + program ID + bump via SHA-256 until the
result is off the Ed25519 curve. The canonical bump is the first value that
produces an off-curve address" (≤16 seeds, ≤32 bytes each). Authority: "only the
program whose ID was used in the derivation can 'sign' for a PDA, and it does so
through `invoke_signed`"
([Solana PDA docs](https://solana.com/docs/core/pda),
[Solana PDA derivation](https://solana.com/docs/core/pda/pda-derivation)).

**Transfer (sharp).** A PDA is a **keyless identity whose "signature" is the
satisfaction of a program's rules** rather than possession of a private key. That
is *precisely* what a criome composable authorization object is: it has no key of
its own; it "authorizes" when its policy (quorum/timelock/etc.) is satisfied. Two
concrete imports: (i) **derive an authorization object's identity deterministically
from its content** — z9d6 content-addressing already does this (the hash of the
policy IS the address), giving criome the PDA's "same definition → same address,
everywhere, no key management" property natively. (ii) The **off-curve guarantee**
is the formal statement of "this identity can never be controlled by a stolen
key — only by its rules." criome should state the same invariant: a composable
authorization object's authority is *structurally* its policy, with no key
backdoor; the only keyed atoms are the leaves. **[transfer]**

### 3c. Squads v4 — production multisig with the exact criome feature set

Squads (formally-verified, ~$10B secured) offers configurable thresholds with
mutable members; **three composable roles** — Proposer ("only creating
transactions"), Voter ("only signing"), Executor ("can only execute"); **time
locks** ("a time delay between when a transaction is proposed and when it can be
executed, giving users time to react if they disagree" — and "sensitive
operations like changing signers or thresholds can be time-locked"); and
**spending limits** ("a multisig can allow certain members to withdraw ... without
needing to pass the multisig threshold ... any timeframe, maximum ... and a
specific whitelisted destination")
([Squads v4](https://squads.xyz/blog/v4-and-new-squads-app),
[Squads roles](https://squads.xyz/blog/permissions-roles-in-multisig),
[Squads time locks/spending limits](https://squads.xyz/blog/spending-limits)).

**Transfer.** Squads is the most direct prior art for criome's target object: it
**composes role-separation + threshold + timelock** in one auth object, and —
crucial design lesson — it **time-locks the meta-operations** (changing signers/
threshold) specifically. criome must do the same: *altering a policy is itself a
policy-gated, time-locked action*, so an attacker who captures a sub-quorum
cannot instantly rewrite the rules. The role decomposition (propose / vote /
execute as separate capabilities) maps onto criome's verb vocabulary — these are
distinct *verbs* over an identity object, each gated by a (possibly different)
quorum. The "spending limit" idea generalizes (drop the money) to a
**scoped/bounded delegated capability**: a sub-authority that may act within
declared bounds without re-clearing the full quorum — a useful pattern for
criome's lower-stakes authorizations, but explicitly bounded so it stays inside
the limited line. **[transfer]**

## Synthesis — the transferable primitive set (what feeds report 5)

| criome need | EVM/Ethereum | Tezos | Solana |
|---|---|---|---|
| **keyed identity atom** | EOA (key pair, initiates) | multisig owner = public key | system-owned keyed account |
| **keyless policy object (z9d6)** | contract account (code, no key) | generic multisig contract storage | **PDA (off-curve, no key, rules-authorized)** |
| **k-of-n quorum** | **Gnosis Safe M-of-N**, nestable | threshold 1..N over pubkeys | Squads threshold, mutable members |
| **weighted quorum / 2-gate** | — | **stake-weighted vote + quorum + 80% supermajority** | — |
| **timelock** | **OZ TimelockController** (Unset→Pending→Ready→Done, predecessor ordering, cancel-veto, salt) | (amendment periods) | **Squads time locks on meta-ops** |
| **role/verb separation** | proposer/executor/admin | — | **Squads proposer/voter/executor** |
| **bounded total evaluation** | gas-bounded halting + determinism (criome gets it *by construction*, no gas) | **typecheck-before-admission, monomorphic, can't fail on bad stack** | deterministic derivation |
| **side-effect-free validation** | **ERC-4337 validate/execute split** (no external reads, simulatable) | pure on-stack eval | runtime-checked ownership |
| **divergence reconciliation** | — | **5-period self-amendment, auto-activation, no hard fork** | — |
| **replay/branch binding** | (chainId in sigs) | **(contract-addr, chain-id, monotonic counter) bound into every signature** | — |

Five load-bearing transfers, ranked:

1. **Validation/execution split (ERC-4337) = criome's whole identity.** criome is
   the pure, simulatable, side-effect-free *validate* predicate, with the
   restriction promoted to type-level law. This is `wckt` "auth-only, never
   transports" expressed in EVM-native terms.
2. **PDA + content-addressing = keyless identity authorized by rules, not keys.**
   z9d6 objects ARE PDAs in spirit; the off-curve guarantee is the formal "no key
   backdoor, only policy" invariant. Identity address = content hash.
3. **Totality by construction beats gas.** Choosing a closed, acyclic,
   non-recursive combinator vocabulary (Michelson's restriction-as-feature)
   yields guaranteed halting + bit-identical re-evaluation with NO gas meter —
   the literal proof criome stayed inside the not-a-VM line.
4. **Tezos self-amendment = the divergence-reconciliation blueprint.** A
   multi-period state machine with two gates (quorum participation +
   supermajority agreement), weighted voting, and deterministic automatic
   activation — feeding report 4's oracle/arbitration design.
5. **Time-lock the meta-operations (Squads + OZ).** Changing a policy is itself a
   policy-gated, time-locked, separately-vetoable action; predecessor ordering
   expresses multi-step authorization without scripting.

Two cross-cutting imports for the schema (report 5/6): (a) **canonical ordering**
of identity atoms by public-key bytes so every quorum proof has one normal form
(Gnosis Safe ordered-signatures); (b) **per-proof replay/branch binding** —
*(object content-hash, branch/network id, monotonic version)* (Tezos three-part
counter) — which is also what makes divergence objects unambiguous across a split.

## Sources

- Ethereum accounts: [ethereum.org](https://ethereum.org/developers/docs/accounts/) · [Ambire](https://blog.ambire.com/eoas-vs-smart-contract-accounts/) · [ETC](https://ethereumclassic.org/blog/2024-07-23-what-are-externally-owned-addresses-and-contract-addresses-in-ethereum-classic/)
- EVM bounded/deterministic: [Gate](https://www.gate.com/learn/articles/what-is-ethereum-virtual-machine-evm/16798) · [Cube](https://www.cube.exchange/what-is/deterministic-execution)
- Gnosis Safe: [Bitbond](https://www.bitbond.com/resources/gnosis-safe-multisig-guide-for-projects) · [Tally](https://docs.tally.xyz/set-up-and-technical-documentation/using-governor-with-gnosis-safe/gnosis-safe/)
- ERC-4337: [EIP-4337](https://eips.ethereum.org/EIPS/eip-4337) · [Hacken](https://hacken.io/discover/erc-4337-account-abstraction/)
- OZ TimelockController: [OZ governance API](https://docs.openzeppelin.com/contracts/4.x/api/governance#TimelockController) · [OZ timelock roles](https://docs.openzeppelin.com/defender/guide/timelock-roles)
- Michelson: [Tezos gitlab](https://tezos.gitlab.io/active/michelson.html) · [docs.tezos.com](https://docs.tezos.com/smart-contracts/languages/michelson)
- Tezos multisig: [Octez](https://octez.tezos.com/docs/user/multisig.html) · [docs.tezos.com](https://docs.tezos.com/smart-contracts/multisig)
- Tezos governance: [docs.tezos.com](https://docs.tezos.com/architecture/governance) · [Arluck](https://medium.com/tezos/amending-tezos-b77949d97e1e) · [Octez voting](https://octez.tezos.com/docs/active/voting.html)
- Solana accounts/PDA: [Chainstack](https://chainstack.com/solana-architecture-account-model-and-transactions/) · [Solana PDA](https://solana.com/docs/core/pda) · [PDA derivation](https://solana.com/docs/core/pda/pda-derivation)
- Squads: [v4](https://squads.xyz/blog/v4-and-new-squads-app) · [roles](https://squads.xyz/blog/permissions-roles-in-multisig) · [time locks/spending limits](https://squads.xyz/blog/spending-limits)
