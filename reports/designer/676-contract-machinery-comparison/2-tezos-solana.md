# Tezos (Michelson) + Solana — contract machinery and transferable ideas

Research perspective for report 676 (contract-machinery comparison). All
claims web-verified June 2026; sources inline and collected at the end.

## Why these two together

They sit at two opposite extremes of the design space and each contributes
a distinct, cleanly-isolable idea:

- **Tezos** answers *"how does a typed machine stay verifiable, and how does
  the system upgrade itself without forking?"* — the typed-restricted VM and
  on-chain self-amendment.
- **Solana** answers *"what if code and state were fully separated, addresses
  were content-derived, and parallelism fell out of declared access?"* — the
  programs-vs-accounts split, PDAs, and parallel-by-declared-access.

The EVM-style "contract = code + its own private storage, executed serially"
model is the foil both reject in different ways.

## Tezos — the machinery

### Michelson: a typed, stack-based VM

Michelson is the on-chain language/VM of Tezos — "to Tezos what the EVM is to
Ethereum." It is **stack-based with strict static type checking**: there are
no variables; instructions consume and push typed values on a stack (e.g.
`ADD` pops two and pushes their sum). The instruction set is small and the
syntax/typing is "defined with a dependent inductive type to rule out
ill-typed instructions" — ill-typed programs are simply not representable.

Crucially it is **not a bag of bytes like EVM bytecode** — it ships
**high-level typed data structures as first-class machine types**: integers,
`mutez` (tez amounts), strings, addresses, plus composites `pair`, `list`,
`set`, `option`, `or`, `big_map` (a lazily-loaded on-chain key-value store),
and `lambda` (code as a storable/pushable value, with partial application via
`APPLY`). The type system carries domain meaning (a tez amount is not just an
int), which is the key contrast with EVM's untyped 256-bit words.

### Formal-verification-friendliness is a design goal, not an afterthought

Because the machine is small and typed, Michelson "was designed to facilitate
formal verification." Concretely there are **two formally-verified
implementations** of the semantics (one in **Coq**, one in **F\***), plus
verifier tooling: **Mi-Cho-Coq** (a Coq framework certifying functional
correctness of Michelson contracts), **Helmholtz** (a refinement-type checker
that takes a Michelson program annotated with a refinement-type spec, then
discharges verification conditions to the **Z3** SMT solver), and a K-semantics
(Runtime Verification). The lesson: *restrict the machine enough that the
semantics fit in a proof assistant.*

### Gas

Michelson uses a gas-based cost model; e.g. naturals are arbitrary-precision
and "the only size limit is gas." Standard metered-execution story (shared
with EVM and Solana's CUs).

### On-chain self-amendment — the cleanest governance/divergence analog

This is the standout idea. Tezos splits its node into a **shell** (network,
storage, the amendment machinery — stays fixed) and a hot-swappable
**economic protocol** (consensus rules, the Michelson interpreter, gas costs,
governance parameters themselves). The protocol is a set of **OCaml modules**
identified by a **b58check hash of its source code**, compiled by a restricted
OCaml compiler that statically sandboxes the available modules.

The chain **votes to replace its own protocol** through five automatic
periods — **Proposal → Exploration → Cooldown → Promotion → Adoption** — each
~14 cycles (~14 days), ~2.5 months total. Delegates submit/upvote the *hash*
of candidate protocol source; passing requires both a **quorum** and an **80%
supermajority** of Yea over Yea+Nay. Voting power = staking balance (own stake
+ delegated tez).

The payoff is the part that matters for divergence-handling: **the upgrade is
not a manual hard fork.** "If a proposal is accepted, nodes need not stop and
restart: the new code is downloaded from other peers, dynamically compiled and
hot-swapped." The amendment rules — including how to amend the amendment rules
— live *inside* the thing being amended. This is the cleanest existing example
of a system that resolves "we disagree about the rules" *on-chain and
in-band*, instead of by social-coordination forks (Ethereum/Bitcoin style).

## Solana — the machinery

### Programs vs. accounts: stateless code over separate data

Solana's defining move is **total separation of code and state**. Unlike
EVM/most chains where a contract holds its own internal storage, Solana
**programs are stateless pure logic** — they own no persistent storage. All
mutable state lives in **accounts**: flat on-chain data containers managed by
the runtime. Two categories: **program accounts** (hold executable code) and
**data accounts** (hold state, no code). A transaction's instruction names a
program plus the accounts it operates on; **all data a program touches is
passed in by reference**, never read implicitly.

Ownership is the access-control primitive: every account has an `owner` field
(a program's pubkey); **only the owning program may mutate an account's data
or deduct its lamports.** Because the same code operates over many independent
data accounts, you deploy logic once and instantiate state arbitrarily — no
redundant per-instance contract deployment.

### Program-Derived Addresses (PDAs): keyless, content/seed-derived addresses

PDAs are **32-byte addresses deterministically derived from a program ID plus
developer-chosen seeds** (up to 16 seeds, ≤32 bytes each) and a **bump** byte.
Their defining property: they are **guaranteed off the Ed25519 curve**, so
**no private key exists** — the address is controlled purely by program logic,
not by a keypair.

Derivation: hash(program_id ‖ seeds ‖ bump); if the result lands *on* the
curve the bump is decremented and retried. `find_program_address` starts at
255 and counts down, returning the first off-curve hit — the **canonical
bump**. Because the same seeds + program ID always yield the same address,
PDAs act as a **deterministic, hashmap-like namespace**: e.g. seeds
`["user", user_pubkey]` give a predictable per-user account with no on-chain
index. A program "signs" for its PDA via **`invoke_signed`** during a
cross-program invocation — the runtime grants authority without any signature,
purely because the program supplied the seeds that derive the address it owns.

### SBF/BPF VM + compute units

Programs are written (typically in Rust), compiled through a Solana fork of
LLVM's BPF backend into **sBPF bytecode** packaged as an ELF `.so`. The runtime
serializes the named accounts into a flat parameter buffer, spins up an sBPF VM
(stack/heap/memory regions), and runs the code, **metering compute units** as
it goes (default ~200,000 CU/transaction; tighter bytecode = cheaper).
BPF-derived bytecode (vs. a bespoke stack machine) is the design choice here —
a general register VM with mature compiler tooling.

### Parallel-by-declared-access (Sealevel)

The throughput innovation. **Every Solana transaction must declare up front
every account it will read or write.** Because access is declared, the
**Sealevel** runtime can statically partition transactions: those touching
disjoint account sets run **concurrently with no locks on global state**;
transactions that write the *same* account are serialized to avoid races.
Parallelism is therefore *derived from the declared access set* — the developer
states intent (which accounts), and concurrency falls out mechanically. This is
the single most transferable scheduling idea: **declared read/write sets →
free, safe parallelism.**

## Transferable ideas (the deliverable)

1. **Typed-restricted VM (from Michelson).** Make the machine's value types
   carry domain meaning (typed amounts, typed maps, code-as-value) and keep the
   instruction set small enough that ill-typed programs are unrepresentable and
   the whole semantics fits in a proof assistant. Restriction *buys*
   verifiability — the opposite of the "Turing-complete bag of bytes" reflex.
   (Directly resonant with this workspace's typed-domain-values discipline.)

2. **On-chain self-amendment (from Tezos).** Split an "always-fixed shell"
   from a "hot-swappable, content-hash-identified policy core," and put the
   rules for changing the core — including the rules for changing those rules —
   *inside* the core, swapped in-band by a deterministic multi-period vote with
   quorum + supermajority. The cleanest model for handling divergence/upgrade
   without out-of-band forking.

3. **Programs-vs-accounts separation (from Solana).** Keep code stateless and
   pure; put all mutable state in separate, individually-owned data containers
   passed in explicitly by reference. Logic deploys once; state instantiates
   freely; the owner field is the access-control primitive. Eliminates the
   "contract = code + hidden private storage" coupling.

4. **PDAs — content/seed-derived keyless addresses (from Solana).** Derive
   stable identities deterministically from (authority + seeds), guaranteed to
   have no key, controlled only by the deriving logic. Gives a deterministic,
   index-free, hashmap-like namespace where the address *is* the lookup key and
   authority is proven structurally (supply-the-seeds) rather than by signature.

5. **Parallel-by-declared-access (from Solana/Sealevel).** Require each unit of
   work to declare its read/write set in advance; let the scheduler run
   non-overlapping units in parallel and serialize only true conflicts.
   Concurrency becomes a *consequence of declared intent* rather than a manual,
   lock-based concern.

## Cross-cut: the spectrum

Tezos optimizes for **provable correctness + governed evolution** (small typed
machine, in-band protocol swap). Solana optimizes for **throughput + flexible
state** (separated state, declared-access parallelism, keyless derived
identities). EVM is the shared foil: untyped serial code with self-owned hidden
storage. The five ideas above are individually liftable and largely orthogonal.

## Sources

- Michelson / typed stack VM: <https://docs.tezos.com/smart-contracts/languages/michelson>,
  <https://octez.tezos.com/docs/active/michelson.html>
- Formal verification (Coq/F\*, Mi-Cho-Coq, Helmholtz, K):
  <https://link.springer.com/chapter/10.1007/978-3-030-72013-1_14> (Helmholtz),
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC7984548/>,
  <https://github.com/spruceid/mi-cho-coq>,
  <https://runtimeverification.github.io/michelson-semantics/michelson/>
- Self-amendment / governance periods: <https://docs.tezos.com/architecture/governance>,
  <https://octez.tezos.com/docs/active/voting.html>,
  <https://opentezos.com/tezos-basics/governance-on-chain/>,
  <https://medium.com/tezos/amending-tezos-b77949d97e1e>
- Protocol shell/economic split, hash-identified OCaml protocol, hot-swap:
  <https://research-development.nomadic-labs.com/how-to-write-a-tezos-protocol.html>,
  <https://tezos.gitlab.io/whitedoc/the_big_picture.html>,
  <https://tezos.com/whitepaper.pdf>
- Solana account model / stateless programs: <https://solana.com/docs/core/programs>,
  <https://solana.com/docs/core/accounts>,
  <https://www.helius.dev/blog/the-solana-programming-model-an-introduction-to-developing-on-solana>
- PDAs: <https://solana.com/docs/core/pda>,
  <https://ackee.xyz/solana/book/latest/chapter3/program-derived-address/>
- SBF/BPF VM + compute units + Sealevel: <https://solana.com/docs/core/programs/program-execution>,
  <https://solana.com/news/sealevel---parallel-processing-thousands-of-smart-contracts>,
  <https://www.alchemy.com/overviews/what-is-the-solana-virtual-machine>,
  <https://chainstack.com/solana-architecture-parallel-transactions/>
