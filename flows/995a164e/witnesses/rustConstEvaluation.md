# Rust const evaluation of trait data

Method: probe rustc --edition 2021 <minimal .rs files> (via subflow, 2026-08-31; rustc 1.96.0 stable, Nix-provided; no nightly reachable on this machine).

Witnessed on stable 1.96.0:
- An associated const declared in a trait and defined in impls is fully
  readable in const evaluation: `const _: () = assert!(A::N + B::N < 10)`
  compiles; with a violated invariant the build fails with
  `error[E0080]: evaluation panicked: <custom message>` (probe 4: a
  three-impl coherence check failed the build on conflict, passed
  without).
- A trait method call in a const context fails:
  `error[E0015]: cannot call non-const method` … `const traits are not
  yet supported on stable Rust`.
- A const fn can construct a throwaway struct instance and call const
  methods on it at compile time (probe 3 used an inherent impl, which
  our rules forbid; the pattern itself is witnessed).
- `#![feature(const_trait_impl)]` / `impl const Trait` syntax is
  recognized by stable's error messages but nightly-gated; no nightly
  toolchain was reachable, so const trait impls are unverified
  end-to-end here.

Inference: the compile-time coherence check is feasible today — data in
associated consts, the check a const assert whose evaluation walks
them. Expressing the walk purely as trait capabilities (no free const
fn) rests on nightly const_trait_impl: it exists, is unverified on this
machine, and needs a nightly toolchain brought in.
