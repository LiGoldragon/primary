# Skill — Rust errors (typed enums via thiserror)

*Each crate defines its own Error enum. Variants are structured.
`thiserror` handles the Display impl. Never `anyhow`/`eyre` at
component boundaries.*

---

## What this skill is for

When writing or reviewing Rust error types in this workspace, this
skill is the discipline. Pairs with `skills/rust/methods.md`
(typed boundaries need typed errors) and `skills/abstractions.md`
§"Perfect specificity at boundaries".

For the index pointing at the wider Rust discipline, see
`skills/rust-discipline.md`.

---

## Typed enum per crate via thiserror

Each crate defines its own `Error` enum in `src/error.rs`,
derived with `thiserror`. Variants are structured — carry the data
needed to render a useful message. Foreign error types convert
via `#[from]`.

```rust
use thiserror::Error;

#[derive(Debug, Clone, Error)]
pub enum Error {
    #[error("chunk not found: {0}")]
    ChunkNotFound(Hash),

    #[error("deserialization failed: {0}")]
    DeserializationFailed(String),

    #[error("invalid node: {0}")]
    InvalidNode(String),

    #[error("merge conflict on key ({} bytes)", key.len())]
    MergeConflict { key: Vec<u8> },

    #[error("network: {0}")]
    Network(#[from] reqwest::Error),
}
```

Public APIs return `Result<T, Error>` with the crate's own enum.
**Never** `anyhow::Result`, `eyre::Result`, or `Result<T, Box<dyn
Error>>` — they erase the error type at the boundary, which loses
the typed-failure discipline the rest of the rules build up.
Callers can no longer pattern-match on what went wrong.

---

## See also

- `skills/rust-discipline.md` — Rust discipline index.
- `skills/rust/methods.md` — typed boundaries (where errors return).
- `skills/abstractions.md` — perfect specificity at boundaries.
- `ESSENCE.md` §"Perfect specificity at boundaries" — the apex
  rule about typed boundaries this skill enforces in Rust.
