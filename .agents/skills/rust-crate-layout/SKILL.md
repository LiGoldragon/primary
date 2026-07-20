---
name: rust-crate-layout
description: 'Rust crate layout rules.'
---

# Rust crate layout

- Keep stateful runtime behind a daemon and thin CLI.
- Keep contract crates free of runtime state.
- Put substantial tests in owned test files.
