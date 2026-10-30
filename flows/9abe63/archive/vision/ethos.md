# Ethos

## 2026-10-30 — A head over a type declares a new type, not an alias; Ethos Zero fixed
Context: the living, in the Psyche core Primary chat 9abe63, on the vision:ethos line `pub type FilePath = String;` generated from `FilePath.String`.

> pub type FilePath = String;

I just caught this, and this is wrong. It should make a new type, not a type alias. We're going to have to have ethos fixed.

## 2026-10-30 — The new type is a single-member tuple struct, a newtype
Context: the living, same chat, on the Primary proposing a named-field struct `pub struct FilePath { pub string: String }`.

No, no, it's not a struct. It uses a single-member tuple. You don't seem to know enough about Rust to understand what I mean.

Landed: vision:ethos, psyche-belief fcddd2.
