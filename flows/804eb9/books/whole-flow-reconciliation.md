Reconciliation of the whole-Flow Ethos inventory (whole-flow-ethos.md, 17 proposals) against the living's comments and the checker. Every Ethos example is run with Check, every datom example with Conform against its type, each in a directory of its own holding only the library the book pairs it with and, under its import's name, the library it imports; and Proposals 12 to 17 as applied to Flow's files at 67b80b3. This is evidence for the review, not book text. Nothing in it authorizes implementation. The records each proposal draws from are in references/whole-flow-ethos.md.

Sources: the flow vision records, the comment relay ledger 7c89aa, and the unrelayed-comments audit da2038. The live comment threads could not be listed from here.

| Proposals | Source book | Living's comments | Checker at c4d82bf |
|---|---|---|---|
| 1 (Flow's library and what Flow says, as vision/flow-ethos.md) | Flow: the design | none found. Effort holds Low and Medium only, as intent/models.md and vision/model-roles.md give them. | pass |
| 2 (the datom traits emitted; sealed type) | Sealed and shared types 2nd | none on sealed types. Each statement is one the checker enforces or the generated code shows; see whole-flow-evidence.md. | pass |
| 3 (empty yield) | same | none. Its example is a plain struct; the generated method is `fn bump(&mut self);`. | pass |
| 4, 5 (last response as a datom) | The last response as a datom object | none found | pass; Proposal 5's datom conforms with Proposal 4's library beside it as response.ethos, the name it imports |
| 6–11 (book 10: 6 names, 7 lowercase capabilities, 8 file form, 9 category vectors, 10 white sugar, 11 Role and Subagent library) | Book 10 (unpublished); it answers the 2026-10-17 16:41 comment on Today 2nd | 16:41: a category holds a vector of its entries; "First" is unclear; lowercase capability names are questioned; `library.` and `{` go on the same line; white brackets and braces; "fix ethos while we fix Flow" | pass; Proposal 10's example is written in the sugar and generates the same Rust as its plain form; 9's and 11's datoms conform with Proposal 1's library beside them as flow.ethos |
| 8 (file form) | same | 2026-10-16 on Ethos syntax 2nd: the brace does not open on its own line; a new line follows the brace; the first section is never on the brace's line; there is no indentation at the root; breaking after the dot is not canonical. Proposal 8 matches all of this. | pass |
| 12–17 (repairs to six of Flow's six Ethos files) | Flow on main | follow the same layout | pass after the repair; every file is refused as it stands |

## Removed from the book

- **Shared state** (the former Proposal 4).
  - Reason: no psyche record grounds shared mutable state. It came from Flow's implementation need for a lock around wake recovery's pane set, relayed by d68c82 (flows/65f93a/log.md:43).
  - Its access claims are not demonstrated. The book said a `.` capability reads under the lock and a `!` capability changes under the lock. The generated traits show only `&self` signatures; the bodies that would take the lock are hand-written.
  - Its examples do associate traits with each shared type, so the capabilities are declared in the Ethos. What is missing is a record that grounds them.
  - What would bring it back: the living's ruling on shared mutable state in Ethos. A mutex need is reported to the living as the implementer's finding. Then, each lock claim needs generated code or a test showing it.
- **A standard-library type, held only in shared state** (the former Proposal 6).
  - Reason: its rule names shared state as the only place such a type is held, and the checker refuses one anywhere else. With shared state removed, the proposal has no ground. No record speaks of standard-library imports.
  - What would bring it back: the ruling on shared state above, and a record on importing Rust standard-library types.
- **Claims cut from the sealed type** (Proposal 2). The proposal stays.
  - "Private to its own file; no code outside it reads or builds them." The positions are `pub(super)`, so the containing module reads and builds them.
  - "Built only by a capability with no self." The checker requires such a capability, but the containing module can still build the type directly.
  - "Cannot be forged; holding one is proof that its constructor ran." This is not demonstrated.
  - "No type read from data holds it." The checker refuses this only within the sealed type's own file.
  - What would bring them back: generation that keeps the positions private to the type's own module, and a test showing no other construction compiles.
- **The value High for Effort** (Proposals 1 and 11). No record grounds it. Harness calls default to medium, and effort is never raised to buy quality (intent/models.md).

## Still open

- Five other 2026-10-17 threads on Today 2nd (16:13 to 16:21) have no text in any record. Only the live threads can supply them.
- The trait demand of 2026-10-16 bears on the joint light book too: Coinage and Topic declare no traits. That needs a trait for the coinage check, which would expand the joint package; it is held for the living's ruling and is not added.
- The trait name: Ethos Zero emits `datom_codec::Composing` and nowhere `Compositional`. Proposal 2 names `Composing` in the section it changes; vision/ethos.md writes `Compositional` at lines 223, 225, 250, 252, 254, 278, 302, 304, 325, 332, 384 and 412, outside the book.
- The ephemeral-flow source is with the Flow seat and is not in this inventory.
- The crates/flow-ethos/ethos/library.ethos repair is withdrawn from this book: the joint book's Proposal 13 or 18 (joint-ethos-extendable-enum.md) carries the same change to that file; if both are rejected, the repair returns against 67b80b3.
- Proposals 2, 3 and 7 are machine proposals for the living's ruling: 2 and 3 have no psyche record, and 7 rests on a question.
- Five removed code lines are wider than 52 columns: one in Proposal 2, two in Proposal 8 and one each in Proposals 13 and 14. They quote the files exactly.
