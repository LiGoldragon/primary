# Runtime emitter audit

## Completed subagent result

Hume audited `schema-rust-next/src/lib.rs` after the first token-lowering pass.
The important finding was that the declaration surface was tokenized, but large
runtime and plane-support clusters still used `self.line(...)` and `format!(...)`.
That matched the psyche's concern: the generator still contained too much
hand-formatted Rust source.

## Ranked clusters

Hume ranked the remaining string clusters by blast radius:

1. Trace object-name support and adjacent lifecycle surface. Small, local, and
   fixture-visible.
2. Nexus runner and action projection glue. Central to the shared runner and
   generic role-trait design.
3. Engine trait emission. Important, but tangled with plane-specific signatures.
4. Mail/envelope/namespaces. Broader and more likely to touch many fixtures.
5. Signal-frame routing and short-header support. Runtime-critical, so best left
   until the token pattern is proven on smaller runtime slices.

## Operator action

The first ranked slice was implemented:

- `schema-rust-next` commit `fd84aae2` tokenizes trace object-name enum emission
  and trace-support emission.
- The generated fixtures were refreshed through the fixture update tests.
- Full `cargo test` and `cargo clippy --all-targets -- -D warnings` passed.

This does not finish the emitter migration. It proves the pattern on another
runtime-adjacent slice and reduces the remaining debt surface.
