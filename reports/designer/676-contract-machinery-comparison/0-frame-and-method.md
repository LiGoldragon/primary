# 676 — criome contract machinery vs. the chains: frame and method

The psyche asked how criome's contract machinery (the content-addressed policy
language + the SEMA-backed contract DAG operator is now landing) compares to how
Solidity/Ethereum, Tezos, Solana, and the rest do their contract machinery.

The thesis to test by grounding: **criome is in the *predicate/validator* family
(Bitcoin Script, Cardano EUTXO/Plutus, ERC-4337 `validateUserOp`), not the
*stateful-execution-VM* family (EVM, Michelson, Solana BPF).** A criome contract is
a policy *evaluated to a verdict*, never code that *runs and mutates state*.

## Method — 4 grounded perspectives + 1 synthesis

| File | Perspective | Grounding |
|---|---|---|
| `1-ethereum-solidity.md` | the account-VM mainline: EVM, gas, mutable storage at an address, deploy/CREATE2, calls + reentrancy, proxy upgrades, ERC-4337 | web |
| `2-tezos-solana.md` | Michelson (typed stack VM, on-chain self-amendment) + Solana (account model, programs-vs-accounts, PDAs, BPF, parallel exec) | web |
| `3-predicate-family.md` | the family criome actually belongs to: Bitcoin Script (no loops, no gas), Cardano EUTXO/Plutus validators (pure yes/no), Move/Sui objects | web |
| `4-criome-machinery.md` | criome's model from the landed code: content-addressed immutable contract DAG, SEMA family, limited combinator language, pure validate, attested clock, divergence adjudication, per-daemon not global consensus | criome code + 674.15/675 |
| `5-comparison.md` | **the synthesis: the comparison table + the deep architectural forks** | all of the above |

The deep forks to draw out: validation-vs-execution; no-gas-via-structural-bounding
vs gas-metering; content-addressed-immutable-objects vs mutable-storage-at-an-address;
composition-by-digest-reference (acyclic, no reentrancy) vs runtime contract calls;
per-daemon durable state + cross-party quorum vs global consensus ledger;
quorum-attested time vs block-clock; divergence-by-adjudication vs fork-choice;
identity-specialized vs general-purpose computation.
