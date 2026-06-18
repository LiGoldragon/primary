# The Predicate / Validator Family

Perspective 3 of report 676. The family criome belongs to: machinery that
**validates** (a pure predicate yields a verdict) rather than
**executes-and-mutates**. Web-grounded; sources inline and collected at the
foot.

## The thesis in one line

An execution VM (Ethereum-style) takes a program, runs it against mutable
global state, and *applies side effects* — it changes the world and bills you
gas for every step, even when it fails. A predicate/validator takes a proposed
state transition and *answers yes or no*: it never mutates anything itself. The
mutation (spending an output, transferring an object) is performed by the
protocol only **if** the predicate says yes. Three systems live squarely in
this family — Bitcoin Script, Cardano's EUTXO/Plutus, and Move/Sui — and each
buys three structural properties from it: **bounded halting without gas**
(for the bounded members), **determinism / pre-flight knowability**, and
**content/hash/ID addressing with immutability** as the natural state model.

## 1. Bitcoin Script — the pure authorizer

**Model.** Every coin lives in a UTXO carrying a *locking script*
(`scriptPubKey`). To spend it, a transaction supplies an *unlocking script*
(`scriptSig` / witness). The network concatenates them and evaluates: the spend
is authorized iff the stack machine terminates with true on top. The script's
entire job is to express the *conditions of spending* — "describe how the next
person wanting to spend the Bitcoins can gain access to them" (Bitcoin Wiki).
It is a predicate over a candidate transaction, not a program that moves money.

**Why it is a predicate, not a VM.** Bitcoin Script is *deliberately*
non-Turing-complete: "no loops or complex flow control capabilities other than
conditional flow control … This ensures that scripts have limited complexity
and predictable execution times" (Bitcoin Wiki). No loops, no recursion, no
persistent state. Because the program is loop-free, it provably terminates in
bounded time **structurally** — there is nothing to meter, so Bitcoin needs no
gas at all. Halting is a property of the language, not of a fuel counter. This
is the cleanest member of the family: a stateless boolean gate.

**Richer policies stay predicates.** P2SH commits a spend to the *hash* of a
redeem script; the spender later reveals the script whose hash matches and
satisfies it — hash-addressing of the spending condition itself. Taproot /
Tapscript (BIP-342) carry the same model into Schnorr-based script paths.
**Miniscript** (Wuille/Poelstra/Kanjalkar) is the giveaway: "A spending policy
is what you mean; Miniscript is its typed, analysable form; Bitcoin Script is
the bytecode the network actually validates" (Spark). The whole stack is
organized around *analyzable predicates over a transaction*, not execution.
**Covenants** (OP_CHECKTEMPLATEVERIFY / BIP-119, OP_VAULT) extend the predicate
to constrain *where funds may go next* — still a yes/no test the spending
transaction must satisfy, never a program that itself sends funds.

## 2. Cardano EUTXO + Plutus — validation, not execution

**Model.** Cardano extends Bitcoin's UTXO model (EUTXO): each UTXO at a script
address carries a **datum** (on-chain state attached to the output). A spending
transaction supplies a **redeemer**. The node runs the validator:

```haskell
mkValidator :: Datum -> Redeemer -> ScriptContext -> Bool
-- e.g.  mk42Validator :: () -> Integer -> ScriptContext -> Bool
```

A validator is a **pure function of (datum, redeemer, script context) returning
Bool** (Plutus Pioneer Program; Cardano Developer Portal). The `ScriptContext`
is the entire transaction being validated — all its inputs and outputs. If the
function returns true (does not error), the spend is allowed; if it errors, "the
transaction is rejected."

**Why it is a validator, not a VM.** The docs are emphatic: "UTxOs on the
blockchain are just data, they are absolutely passive … Only new transactions
change the state." The script does not run *to do something*; it runs *to judge
whether a proposed transaction is permitted*. This is "validation NOT
execution." Contrast the portal draws explicitly with Ethereum: account-based
scripts get "unlimited access" to mutate global state, creating
unpredictability; EUTXO validators are pure — "given identical inputs … they
always produce identical results," and validity "depends solely on the
transaction and its referenced UTXOs, not on external blockchain state that
might change."

**What the predicate model buys.** Determinism is the payoff. A transaction can
be fully validated *locally, off-chain, before submission*: "if a transaction
references an already-spent input, validation fails immediately off-chain before
reaching the network, costing you nothing" — versus Ethereum where you "pay fees
even for failed transactions." Costs are computed exactly at construction time.
And — the criome-relevant part — **scripts and datums are identified by hash**:
a script address contains the *validator's hash* (`ValidatorHash`), not the code;
the spending transaction reveals the actual code for nodes to verify, while the
producing transaction only commits to the hash. Content addressing of code, same
shape as Bitcoin P2SH.

## 3. Move / Sui — the object-centric validator surface

**Move's contribution: linear resources.** Move (Aptos, Sui) models assets as
**resources** — linear types that "cannot be copied, cannot be dropped
(deleted), must have a clear owner, and must be explicitly moved." The compiler
*statically verifies resource safety before deployment*, structurally
preventing double-spend and unauthorized minting. Unlike Solidity, which "treats
assets as mutable entries in a hash map," Move treats them as things that can
only be *moved*, never duplicated or silently discarded (Aptos docs; Zellic;
Pontem). This is the predicate spirit pushed into the *type system*: instead of
a runtime check that an asset wasn't duplicated, duplication is simply
**not expressible** — the bytecode verifier rejects it. Halting/safety as a
structural property again.

**Sui's object-centric model.** Sui is the strongest content/ownership-addressed
member. State is not account balances but **objects, each with a stable 32-byte
UID** "derived from the digest of the transaction that created the object and a
counter." Objects carry a monotonic 8-byte version and the digest of the last
modifying transaction, so any object is referenceable by an `(ID, version,
digest)` triple — *content + history addressing*. Ownership is explicit:
**owned** (single address), **shared** (`share_object`), **immutable** ("cannot
be mutated, transferred, or deleted … anyone can use it"), or wrapped.

**Why this is validator-shaped, not VM-shaped.** The transaction names exactly
the objects it touches; the system *validates* that the caller owns them, that
versions match, and that resource rules hold, then applies the move. The
decisive tell: transactions over **owned** objects "skip consensus entirely" —
processed by Byzantine Consistent Broadcast on a fast path "without requiring
validator agreement, since ownership ensures no conflicts." That parallelism is
only possible *because* the model is predicate-like: the validity of an
owned-object spend is a local, conflict-free check, exactly as a UTXO spend is.
Global sequencing is needed only for shared (contended) objects.

## The family, abstracted — and where criome sits

| | Bitcoin Script | Cardano Plutus | Sui/Move |
|---|---|---|---|
| Unit of state | UTXO | UTXO + datum | Object (UID) |
| The check | stack predicate → true | `(d,r,ctx) -> Bool` | resource + ownership/version validation |
| Halting | structural (no loops) | metered but pure/deterministic | static verifier + bounded |
| Gas needed? | none | priced but knowable pre-flight | priced, fast-path for owned |
| Addressing | P2SH script hash | script/datum **hash** | content/ownership **ID + digest** |
| Mutation | protocol spends if true | protocol consumes UTXO if true | protocol moves object if valid |

The unifying claim: **none of these *runs your code to change the world*. They
run a pure judgment over a proposed change and let the protocol apply it only on
a yes.** That yields halting for free (or near-free) on the bounded members,
determinism / pre-submission knowability, and a state model built on
immutability + content/hash/ID addressing rather than mutable global storage.
This is the family criome belongs to: a verdict-yielding predicate over
content-addressed, immutable inputs — validation, not an execution VM.

## Sources

- Bitcoin Wiki, *Script* — non-Turing-complete, no loops, locking/unlocking
  scripts as spend conditions: https://en.bitcoin.it/wiki/Script
- Bitcoin Optech, *OP_CHECKTEMPLATEVERIFY* (covenants, BIP-119):
  https://bitcoinops.org/en/topics/op_checktemplateverify/
- Spark, *Miniscript: Composable and Analyzable Bitcoin Scripts* (policy vs
  Script): https://www.spark.money/research/miniscript-bitcoin-spending-policies
- Spark Glossary, *BIP-342 (Tapscript)*: https://www.spark.money/glossary/bip-342
- Plutus Pioneer Program, *Week 02 — Validation* (validator signature, Bool
  verdict, hash identification):
  https://plutus-pioneer-program.readthedocs.io/en/latest/week2.html
- Cardano Developer Portal, *Extended UTXO Model* (purity, deterministic local
  validation, EUTXO vs Ethereum):
  https://developers.cardano.org/docs/learn/core-concepts/eutxo/
- Sui Documentation, *Object Model* (UID derivation, owned/shared/immutable,
  version+digest, fast-path consensus bypass):
  https://docs.sui.io/concepts/object-model
- Aptos Documentation, *Move — A Web3 Language and Runtime* (linear resources):
  https://aptos.dev/network/blockchain/move
- Zellic, *Move Fast & Break Things, Pt. 1: Move Security* (compile-time
  resource safety): https://www.zellic.io/blog/move-fast-and-break-things-pt-1/
- Pontem, *How the Move Programming Language Works* (resources vs Solidity hash
  map): https://pontem.network/posts/how-the-move-programming-language-works
