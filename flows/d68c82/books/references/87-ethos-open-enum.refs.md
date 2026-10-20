# References: Ethos: the open enum

## The living's words

- flows/d68c82/vision/ethos.md, "An open enum, and the camel ID" (book comment on «Flow's vision», 2026-10-19T17:33): the open enum, the camel ID as a temporary name, the check long term, the metaflow topic as an open set with core, the word-based hash, a book and a review of Ethos architecture, a multiple-book series
- flows/d68c82/vision/ethos.md, "An extendable enum marked by uncapitalized user entries" (the same idea, first said); "Comments on the Ethos vision, 3rd edition" and "Comments on The Ethos syntax" (variants capitalized, obligatory; no one-variant enum; no example that is not real code); "A specification groups its items by variant"; "One Ethos file holds one main object"; "Imports start with a colon" and "White braces define a struct" (same date; not used here)

## Current modules

- psyche-context origin/main 1535807: vision/flow.md shown whole; vision/ethos.md context lines (section "Every declared type bears both traits"; the file read whole, 23ec573); vision/datom.md Syntax (a head is always a variant, capitalized); vision/book.md, vision/inquiry.md for form
- mind-context at 344f6c3 has no knowledge/ or inquiry/ directory (skills/ only); the paths of proposals 3 to 5 are the ones the order named
- flows/5578cc/vision/identifiers.md: a three-word camelCase flow id (abandonAbilityAble), approved by the living 2026-10-03, not landed; flows/445410/vision/flow.md: the origin of core:Name, camelCaseExpression

## Witnessed in code (read subflows, 2026-10-19)

- protos main 15b41da (0.32.2): src/core.rs, no case test; ethos-zero main 07714b0 (17.0.0): src/lib.rs, conception.rs, checking.rs (capital required on type and trait names, line ~521), generation.rs (alias is `pub type`); datom-codec main 4dff16b: src/composition.rs, crates/datom-codec-derive/src/lib.rs (derived enum matches exact spelling)
- flow crates/flow-ethos/ethos/library.ethos: Topic.String with the camelCase check as a comment; FlowId.String; crates/flow-nexus/src/title.rs: six hex characters
- Run by the author, ethos-zero 07714b0 Check: `Topic.[ core ethos ]` accepted; a trait with a capability whose input is a type refused (TraitWanted); every ethos block in the book accepted by the builder's check
- Not found: a registry of types in these repositories; a Rust check of a topic's camel case; any word-hash code; white braces on any main (branch ethos-proposals only)
