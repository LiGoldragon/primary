# Ethereum / Solidity — the account-VM mainline

Perspective for the contract-machinery comparison (report 676). This
document describes the machinery of a "contract" on Ethereum: what it is,
how it is deployed and addressed, how contracts compose, what hazards
that composition creates, and how the whole thing is held together by
global consensus. All claims web-verified; sources inline and collected
at the end.

## 1. The account model — two kinds of account, one address space

Ethereum's state is a flat map from 20-byte **addresses** to **accounts**.
The Yellow Paper defines exactly two account kinds, sharing one address
space:

- **Externally Owned Account (EOA)** — controlled by a private key held
  off-chain (person, HSM, custody service). It has **no code** and an
  **empty storage trie**; it carries a balance and a nonce. Only an EOA
  can *originate* a transaction by signing it. ([eco.com EOA](https://eco.com/support/en/articles/12005956-what-is-an-eoa-externally-owned-accounts),
  [Alchemy accounts](https://www.alchemy.com/docs/ethereum-accounts))

- **Contract account** — controlled internally by its **deployed
  bytecode**, which runs when the account receives a message. It owns
  balance, nonce, **code**, and a populated **storage trie**. A contract
  cannot start a transaction; it can only send *messages* (internal
  calls) once an EOA-originated transaction has set execution in motion.
  ([eco.com EOA](https://eco.com/support/en/articles/12005956-what-is-an-eoa-externally-owned-accounts),
  [Ambire EOA vs SCA](https://blog.ambire.com/eoas-vs-smart-contract-accounts/))

So a **"contract" = a contract account = code + mutable storage living at
an address**. The address is the identity; the code at that address is
the program; the storage at that address is the program's persistent
heap. Every transaction's origin chains back to some EOA signature, even
when the visible work is a deep tree of contract-to-contract calls.
([eco.com EOA](https://eco.com/support/en/articles/12005956-what-is-an-eoa-externally-owned-accounts))

## 2. The EVM — a stateful, quasi-Turing-complete VM with gas metering

Ethereum is a **distributed state machine**, not a ledger: a single
global data structure (the world state) evolves by a deterministic
transition function `Y(S, T) = S'` — old valid state `S` plus
transactions `T` yields new valid state `S'`. The EVM is the engine that
computes that function, "execut[ing] code consistently and securely
across all Ethereum nodes." ([ethereum.org EVM](https://ethereum.org/en/developers/docs/evm/))

The EVM is a **stack machine** with several memory regions: a volatile
stack and memory scoped to one call, and **persistent storage** (the
contract account's storage trie) that survives across transactions.

### Why gas exists — the halting bound

The EVM's instruction set is expressive enough to be Turing-complete in
principle, which collides with the **Halting Problem**: a node cannot, in
general, decide in advance whether an arbitrary program will terminate.
Turing proved (1936) no machine can solve this, so a validator can never
know up front that a transaction won't loop forever.
([Medium: halting + gas](https://medium.com/@ksiddharth346/understanding-turing-completeness-the-halting-problem-and-how-gas-solves-it-in-ethereum-cf4f36e617ed),
[Edge: fees, gas, halting](https://edge.app/blog/market-updates/ethereum-fees-gas-and-the-halting-problem/))

Ethereum sidesteps this by **metering**: every opcode costs **gas**, and
each transaction carries a **gas limit** (an upper bound the sender sets)
and a **gas price**. When cumulative gas exceeds the limit, the EVM
throws an **out-of-gas exception**, aborts, and **rolls back** the
transaction's effects (fees still paid). Because every execution is
bounded by a finite gas budget, all executions terminate — the EVM is
therefore **quasi-Turing-complete**: Turing-complete in expressiveness,
but bounded so the chain as a whole cannot be hung by a runaway program.
([arxiv: out-of-gas typing](https://arxiv.org/pdf/2407.15676),
[Consensys: guide to gas](https://consensys.io/blog/a-guide-to-gas),
[Chainlink: what is the EVM](https://chain.link/article/ethereum-virtual-machine-evm))
Gas thus does double duty: it is the **halting bound** and the **fee /
anti-DoS pricing** mechanism in one.

## 3. Mutable storage — SSTORE changes world state in place

A contract account's data lives in its **account storage trie**, a
256-bit → 256-bit key/value map. The EVM exposes exactly two opcodes:
**`SLOAD`** (read a word from storage onto the stack) and **`SSTORE`**
(write a word back to storage). ([calnix EVM storage opcodes](https://calnix.gitbook.io/eth-dev/evm-storage-opcodes/evm),
[Medium: Ethereum structures](https://medium.com/@ricore77.eth/understanding-ethereum-structures-world-state-trie-transaction-trie-receipts-and-account-d96ab74bb2ac))

This is the defining property to contrast against other models: **storage
is mutable in place**. `SSTORE` overwrites the value at a slot; the
account's storage trie is "mutable with each block because the execution
of transactions in each block can alter the values stored in accounts,"
and the world-state trie that links every account is "an always changing
structure." Writing a slot forces the affected trie nodes to be
re-hashed up the path to the root, so every mutation is reflected in a
new state root. `SSTORE` gas was re-priced (EIP-2200) precisely because
in-place persistent writes are the most expensive state operation.
([Medium: Ethereum structures](https://medium.com/@ricore77.eth/understanding-ethereum-structures-world-state-trie-transaction-trie-receipts-and-account-d96ab74bb2ac),
[calnix EVM storage opcodes](https://calnix.gitbook.io/eth-dev/evm-storage-opcodes/evm))

## 4. Deployment and addressing — CREATE vs CREATE2

A contract comes into existence when **init code** runs and returns the
**runtime bytecode** that gets stored at a fresh address. Two derivation
schemes:

- **`CREATE`** (the default): the new address is a hash of the
  **deployer address + the deployer's nonce**. Sequential and
  history-dependent — you cannot know the address before deploying, and
  the same code redeployed later lands elsewhere.
  ([RareSkills address derivation](https://rareskills.io/post/ethereum-address-derivation))

- **`CREATE2`** (content-ish addressing): the address is
  `keccak256(0xff ++ deployer ++ salt ++ keccak256(init_code))[12:]`.
  Because it folds the **hash of the init code** plus a chosen 32-byte
  **salt** into the address, the same inputs produce the **same address
  on any EVM chain**, independent of nonce or order. The `0xff` prefix is
  a domain separator so a CREATE2 address can never collide with a valid
  CREATE (RLP) preimage. This enables **counterfactual deployment** —
  you can compute, fund, and reference an address *before* the contract
  exists, then deploy known code there on demand.
  ([Foundry deterministic CREATE2](https://www.getfoundry.sh/guides/deterministic-deployments-using-create2),
  [RareSkills address derivation](https://rareskills.io/post/ethereum-address-derivation),
  [ChainScore CREATE2](https://chainscorelabs.com/en/glossary/smart-contracts/cross-contract-communication/create2))

This is "content-ish," not pure content addressing: the address binds the
init-code hash *and* the deployer *and* a salt, so identical code from
different deployers (or salts) gets different addresses.

## 5. Composition — CALL / DELEGATECALL and the reentrancy hazard

Contracts compose by sending messages to other addresses at runtime.
Two opcodes matter:

- **`CALL`** — invokes code at the target address **in the target's own
  context**: the callee's storage is modified, and `msg.sender` becomes
  the caller. Ordinary contract-to-contract interaction (and value
  transfer). ([Halborn delegatecall](https://www.halborn.com/blog/post/delegatecall-vulnerabilities-in-solidity),
  [Kush: call/delegatecall](https://kushgoyal.com/ethereum-solidity-how-use-call-delegatecall/))

- **`DELEGATECALL`** — runs the target's **code in the caller's
  context**: it reads and writes the **caller's storage**, and preserves
  the original `msg.sender` and `msg.value`. The callee is borrowed logic
  operating on the caller's state. This is what makes upgradeable proxies
  possible (next section), but it also means a **storage-layout mismatch**
  between caller and callee silently corrupts the caller's state.
  ([Metana delegatecall](https://metana.io/blog/delegatecall-in-solidity-simplified-guide/),
  [Halborn delegatecall](https://www.halborn.com/blog/post/delegatecall-vulnerabilities-in-solidity))

### The reentrancy hazard

Because a `CALL` hands control to (possibly attacker-controlled) code
*before* the caller has finished updating its own state, the callee can
**call back in** ("reenter") and observe stale state — the canonical
example being a withdraw function that sends ether before zeroing the
balance, letting the recipient's fallback re-invoke withdraw repeatedly
(the 2016 DAO class of bug). The standard defenses:
**checks-effects-interactions** (update all state *before* any external
call), **reentrancy guards / mutex locks**, and **pull-over-push**
withdrawals. Reentrancy and delegatecall exploits "share a common
thread — both exploit the dangers of external calls." External
composition is the source of Ethereum's power and its sharpest footgun.
([Alchemy security best practices](https://www.alchemy.com/overviews/smart-contract-security-best-practices),
[arxiv: Sereum reentrancy](https://arxiv.org/pdf/1812.05934),
[AuditFirst delegatecall](https://medium.com/@auditfirst.io/understanding-delegatecall-vulnerabilities-in-solidity-a-comprehensive-guide-82995c7e7af8))

## 6. Immutability of deployed code + the proxy-upgrade pattern

Once runtime bytecode sits at an address it is **immutable** — "Ethereum
contracts are immutable by design; once the bytecode is there, it can't
be changed." (`SELFDESTRUCT` can remove a contract, but you cannot patch
its code in place.) To get upgradeability the ecosystem adds a layer of
indirection: ([OpenZeppelin proxies](https://docs.openzeppelin.com/upgrades-plugins/proxies),
[ThreeSigma upgradeable](https://threesigma.xyz/blog/web3-security/upgradeable-smart-contracts-proxy-patterns-ethereum))

- A **proxy** contract holds the **address and all state**, and never
  moves. Its fallback **`DELEGATECALL`s** to a separate **implementation
  (logic) contract**. Because delegatecall runs in the proxy's context,
  **state stays in the proxy** while the **logic lives in a swappable
  implementation**. Upgrading = pointing the proxy at a new
  implementation address; the user-facing address and stored state are
  preserved. ([OpenZeppelin proxies](https://docs.openzeppelin.com/upgrades-plugins/proxies))

- **EIP-1967** fixes well-known storage slots
  (`keccak256("eip1967.proxy.implementation") - 1`, plus admin/beacon)
  so the implementation pointer can't collide with the logic's own
  variables. Variants: **Transparent proxy** (separate admin call-path)
  and **UUPS / EIP-1822** (upgrade logic lives in the implementation,
  leaner proxy). ([Medium: transparent proxy EIP-1967](https://medium.com/@andrey_obruchkov/proxies-and-upgradability-transparent-proxy-eip-1967-6a972ef226c7),
  [RareSkills transparent proxy](https://rareskills.io/post/transparent-upgradeable-proxy))

The conceptual move: code is immutable, but a *pointer to code* stored in
mutable storage is not — upgradeability is rebuilt on top of mutable
state + delegatecall, not granted by the platform.

## 7. World state as a Merkle-Patricia trie under global consensus

The world state is "an enormous data structure called a modified
**Merkle Patricia Trie**, which keeps all accounts linked by hashes and
reducible to a single **root hash** stored on the blockchain." Each
account in turn has its own storage trie with its own root, nested inside
the world trie. ([ethereum.org EVM](https://ethereum.org/en/developers/docs/evm/),
[arxiv: Ethereum data structures](https://arxiv.org/pdf/2108.05513))

Two consequences matter for the comparison:

1. **The entire global state collapses to one 32-byte root.** Any
   mutation (`SSTORE`, balance change, new account) re-hashes the path to
   the root, so two nodes agree on the whole world iff their state roots
   match — cheap, cryptographic equality over gigabytes of state.

2. **The state is replicated by global consensus.** Every full node runs
   the EVM to re-execute every transaction and "must adhere to the
   specification described in the Ethereum Yellowpaper"; independent
   client implementations (Rust, Go, etc.) must compute byte-identical
   results. Consensus is over the *transition*: nodes agree on the
   ordered transactions, each re-derives `S'` and its root, and the
   network rejects any block whose claimed state root doesn't match
   honest re-execution. **There is one shared mutable world, redundantly
   computed by thousands of machines.** ([ethereum.org EVM](https://ethereum.org/en/developers/docs/evm/))

This is the deep cost/property of the model: mutable in-place state is
globally legible and consensus-checked, but every write is paid for by
every node re-executing and re-hashing.

## 8. ERC-4337 — account abstraction and the validate / execute split

EOAs hardwire one authentication scheme (ECDSA over the txn) and require
the sender to hold ether for gas. **ERC-4337** brings programmable
accounts *without* an L1 protocol change by adding an off-protocol layer
above the EVM: ([EIP-4337](https://eips.ethereum.org/EIPS/eip-4337),
[Alchemy: account abstraction](https://www.alchemy.com/overviews/what-is-account-abstraction))

- A **UserOperation** is "a higher-layer pseudo-transaction object that
  represents the intent of the account" (sender, nonce, calldata, gas
  fields, optional factory, optional paymaster, signature). Users sign
  these and submit them to a dedicated **alt-mempool**, not the normal
  txn pool. ([EIP-4337](https://eips.ethereum.org/EIPS/eip-4337))

- **Bundlers** watch the alt-mempool, pack many UserOperations into one
  real transaction, and submit it to a singleton **EntryPoint** contract
  via `handleOps()`. ([cobo ERC-4337](https://www.cobo.com/post/what-is-erc-4337))

### The validate / execute split — and why it exists

The EntryPoint enforces a **strict two-phase pattern over the whole
batch**: ([EIP-4337](https://eips.ethereum.org/EIPS/eip-4337),
[OpenZeppelin AA](https://docs.openzeppelin.com/contracts/5.x/account-abstraction))

1. **Validation phase** — for each op the EntryPoint calls the account's
   **`validateUserOp(...)`**: the account checks the signature (any
   scheme — multisig, passkey, session key) and confirms it (or its
   paymaster, via `validatePaymasterUserOp`) can pay. **No business logic
   runs here.**

2. **Execution phase** — only **after every op in the bundle validates**
   does the EntryPoint loop back and call each account's **`execute(...)`**
   with the op's calldata.

The split is a direct economic-security fix. The EIP frames the problem:
"how can a block builder including an operation make sure that it will
actually pay fees, without having to first execute the entire
operation?" Without separation "an attacker could easily send many
operations that pretend to pay a fee but then revert at the last moment
after a long execution," a DoS on bundlers. Forcing **verification
(acceptance + agreement to pay) strictly before execution** lets a
bundler cheaply confirm every op is fee-backed before spending gas on the
expensive part. ([EIP-4337](https://eips.ethereum.org/EIPS/eip-4337))

The comparison-relevant abstraction: ERC-4337 **separates
*authorization* from *effect*** at the account boundary —
`validateUserOp` decides "is this allowed and paid for?", `execute` does
the work — making the account itself a programmable contract rather than
a fixed-key EOA.

## Key properties (the comparison handles)

- **Identity = address; program = code at that address; heap = storage at
  that address.** EOAs (keyed, codeless) vs contract accounts (code +
  storage) share one address space.
- **Gas = halting bound + fee.** Metered execution makes the
  quasi-Turing-complete VM provably terminating and DoS-priced.
- **Mutable in-place storage.** `SSTORE` overwrites world state;
  re-hashing propagates to a single state root.
- **Addressing.** `CREATE` (nonce-based, sequential) vs `CREATE2`
  (init-code-hash + salt → deterministic, cross-chain, counterfactual).
- **Composition + reentrancy.** `CALL` (callee context) / `DELEGATECALL`
  (caller context); handing control to external code before finishing
  state updates is the reentrancy footgun → checks-effects-interactions,
  guards, pull-over-push.
- **Immutable code, mutable indirection.** Deployed bytecode can't
  change; proxies (delegatecall → swappable impl, EIP-1967/UUPS) rebuild
  upgradeability on top of mutable storage.
- **Global consensus over one mutable world.** State is a modified
  Merkle-Patricia trie reduced to a root hash; every full node
  re-executes every transaction to agree on `Y(S,T)=S'`.
- **validate / execute split (ERC-4337).** Authorization (`validateUserOp`)
  is strictly separated from effect (`execute`), batched and verified
  before execution to guarantee fee payment / prevent bundler DoS, and to
  make accounts programmable.

## Sources

- Ethereum.org, *Ethereum Virtual Machine (EVM)* — https://ethereum.org/en/developers/docs/evm/
- EIP-4337, *Account Abstraction Using Alt Mempool* — https://eips.ethereum.org/EIPS/eip-4337
- eco.com, *What Is an EOA?* — https://eco.com/support/en/articles/12005956-what-is-an-eoa-externally-owned-accounts
- Alchemy Docs, *What are Ethereum Accounts?* — https://www.alchemy.com/docs/ethereum-accounts
- Ambire, *EOA vs. Smart Contract Account* — https://blog.ambire.com/eoas-vs-smart-contract-accounts/
- Medium (Deno/Siddharth), *Turing Completeness, the Halting Problem, and Gas* — https://medium.com/@ksiddharth346/understanding-turing-completeness-the-halting-problem-and-how-gas-solves-it-in-ethereum-cf4f36e617ed
- Edge, *ETH Fees, Gas, & The Halting Problem* — https://edge.app/blog/market-updates/ethereum-fees-gas-and-the-halting-problem/
- arXiv 2407.15676, *Preventing Out-of-Gas Exceptions by Typing* — https://arxiv.org/pdf/2407.15676
- Consensys, *A Guide to Gas* — https://consensys.io/blog/a-guide-to-gas
- Chainlink, *What Is the EVM?* — https://chain.link/article/ethereum-virtual-machine-evm
- Medium (R. Santos), *Understanding Ethereum Structures (World State / Storage Trie / MPT)* — https://medium.com/@ricore77.eth/understanding-ethereum-structures-world-state-trie-transaction-trie-receipts-and-account-d96ab74bb2ac
- calnix gitbook, *EVM Storage Opcodes* — https://calnix.gitbook.io/eth-dev/evm-storage-opcodes/evm
- arXiv 2108.05513, *Ethereum Data Structures* — https://arxiv.org/pdf/2108.05513
- Foundry, *Deterministic Deployments with CREATE2* — https://www.getfoundry.sh/guides/deterministic-deployments-using-create2
- RareSkills, *How Ethereum addresses are derived* — https://rareskills.io/post/ethereum-address-derivation
- ChainScore, *Create2: Deterministic Contract Addresses* — https://chainscorelabs.com/en/glossary/smart-contracts/cross-contract-communication/create2
- Metana, *Mastering Delegatecall in Solidity* — https://metana.io/blog/delegatecall-in-solidity-simplified-guide/
- Halborn, *Delegatecall Vulnerabilities In Solidity* — https://www.halborn.com/blog/post/delegatecall-vulnerabilities-in-solidity
- Kush Goyal, *call / delegatecall in Solidity* — https://kushgoyal.com/ethereum-solidity-how-use-call-delegatecall/
- AuditFirst, *Understanding Delegatecall Vulnerabilities* — https://medium.com/@auditfirst.io/understanding-delegatecall-vulnerabilities-in-solidity-a-comprehensive-guide-82995c7e7af8
- Alchemy, *Smart Contract Security Best Practices* — https://www.alchemy.com/overviews/smart-contract-security-best-practices
- arXiv 1812.05934, *Sereum: Protecting Against Re-Entrancy Attacks* — https://arxiv.org/pdf/1812.05934
- OpenZeppelin Docs, *Proxy Upgrade Pattern* — https://docs.openzeppelin.com/upgrades-plugins/proxies
- ThreeSigma, *Upgradeable Smart Contracts: Proxy & UUPS* — https://threesigma.xyz/blog/web3-security/upgradeable-smart-contracts-proxy-patterns-ethereum
- Medium (Obruchkov), *Transparent Proxy (EIP-1967)* — https://medium.com/@andrey_obruchkov/proxies-and-upgradability-transparent-proxy-eip-1967-6a972ef226c7
- RareSkills, *Transparent Upgradeable Proxy Pattern* — https://rareskills.io/post/transparent-upgradeable-proxy
- cobo, *ERC-4337 Explained* — https://www.cobo.com/post/what-is-erc-4337
- OpenZeppelin Docs, *Account Abstraction* — https://docs.openzeppelin.com/contracts/5.x/account-abstraction
- Alchemy, *What is ERC-4337?* — https://www.alchemy.com/overviews/what-is-account-abstraction
