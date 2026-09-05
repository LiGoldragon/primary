# Ethos Zero audit-closure candidate after review fixes

## Candidate state

This candidate follows `341c5c57e45d` (`Make Ethos ascent structurally
infallible`) and `a0c919189d6a` (`Close Ethos Zero migration audit`). It is
not yet the final closure: the independent review of `341c5c57e45d` found four
concrete generator defects, all corrected in `b2d63f4f00e0`
(`Fix reviewed generator invariants`). That commit is pushed on `main` and the
working copy is clean. A bounded recheck and the reserved remote
`nix flake check` remain pending.

The public version remains 5.0.0. Cargo and the flake pin Protos
`2d999f173334` (0.26.0) and datom-codec `41a3c073d5c5` (0.21.0). No substrate
source changed. Full crate lock 839 was released after the candidate committed
and pushed.

## Implemented closure

- F4 follows Protos 0.26 directly: headed form head at child 0, body at child
  1, and qualified-head arguments under child 0. Actualization does not remap
  paths. The four required malformed inputs locate the literal `Bogus` source
  slice in `Vector<Bogus>`, `K<Bogus>`, `K<Sized Bogus>`, and `Item<Bogus>`.
- F5 refuses repeated simple parameter bounds, a reference that actually
  matches multiple parameters, alias-only generic cycles, and superkind
  cycles. Alias cycling now substitutes actual generic arguments while it
  follows an alias body: the exact
  `Types [] [ A<Sized>.Sized B.A<B> ] []` input faults as `Cycle(B)` rather
  than emitting the recursive `type B = A<B>`. Recursive structs and enums
  with finite indirection remain supported and compile.
- F2 fully qualifies standard containers and retains the existing `Result`,
  `Box`, and recursive `Self` fixture. The exact nested collision input
  `Types [] [ X.[ A.[ V ] ] XA.{ Text } ] []` now generates the internal enum
  `XEthosNestedA` while retaining authored `XA`; its generated fixture is
  compiled. Generated parameter identifiers allocate away from authored types:
  a constrained declaration that carries both its parameter and authored `A`
  emits `AEthosParameter` for the parameter and preserves the authored field
  type `A`.
- Grouped imports use the supported Protos spelling
  `std:clone:[ Clonable.Clone ]`; direct ascent preserves each source segment
  and generated Rust writes `std::clone::Clone`.
- F3 projects `File` structurally through Protos without textualizing and
  reparsing. `Name` validates Protos symbols and Rust identifiers. `Source`
  retains validated segments, rejects generic paths, and now rejects contextual
  `Self` so a public source value cannot emit module-level `Self::Text`.
- Public `File::generate` now validates the whole file before token creation
  and returns `Result<String, Fault>`. Programmatic invalid files therefore
  receive typed faults: a declaration named `Self` and an identity with 27
  constraints no longer reach `syn` or `Ident` panics. Declaration, variant,
  associated-item, capability, import, and sourced-reference name positions
  reject `Self`; an unsourced `Self` reference remains the intrinsic.
- F9 keeps the named internal anatomy (`Headed`, `Pending`,
  `DeclarationSite`, `ReferenceRequirement`, and `KindContents`) and homes
  helpers in traits. The authored no-free-functions and no-inherent-methods
  scripts pass.
- The explicit flat declaration budget applies to `Types` only: more than 512
  type declarations fault with `Depth`. A witness reads 513 `Kinds`
  declarations successfully, matching the documented supported envelope and
  the separate structural reader bounds. This does not introduce a new
  all-roots declaration cap.
- Nix applies the 8 GiB virtual-memory limit inside Cargo derivations,
  `cargoFmt`, and each `runCommand`; the README documents that policy and the
  current path, import, generation, naming, and declaration-budget behavior.

## Witnesses

All commands used `ulimit -v 8388608`, one Cargo job for Cargo commands, and
bounded timeouts. The exact reviewer nested collision, generic alias cycle,
programmatic `Self` declaration, 27-constraint identity, and `Source::try_from
("Self")` cases were observed failing before their matching corrections and
then passing. The generic-name capture witness also failed before allocation
and then passed.

- `cargo fmt --all -- --check` passed.
- `cargo test --locked` passed: 55 Ethos tests, 15 generated-code tests, 7
  CLI tests, and 3 freshness tests.
- `cargo clippy --locked --all-targets -- -D warnings` passed.
- `RUSTDOCFLAGS=-D warnings cargo doc --locked --no-deps` passed.
- The authored `checks/dependency-ethos.sh` generated all four declarations
  from the exact pinned store checkouts for Protos and datom-codec. The
  authored `checks/no-free-functions.sh` and `checks/no-inherent-methods.sh`
  passed.
- `tests/generated/nested-collision.rs` and
  `tests/generated/generic-shadow.rs` were regenerated through the CLI and
  compile with the generated-code suite; freshness covers both.
- The ordinary `target/debug/ethos-zero` binary was rebuilt from
  `b2d63f4f00e0`; fresh CLI probes for both new fixtures byte-match their
  committed generated modules.

The independent recheck and final remote `nix flake check` have not run on
this corrected candidate and remain required.

## Remaining language-scope questions

Ethos kind identity (bare name plus constraints) remains separate from the
Rust namespace. This work does not select a mangling rule for distinct Ethos
kinds with the same bare name, and it does not claim a specialized
emitted-namespace refusal for that unresolved case. It also does not settle
omitted `Types` associations or introduce Nexus work.

## Sources

- Main-flow brief and follow-up requirements for F2, F3, F4, F5, F9, and the
  review fixes.
- `flows/1a6ca4/reports/auditEthosZeroAstra.md`.
- `flows/da223f/reports/rewrite.md`.
- `flows/84eb1e/reports/independentAudit.md`.
- `Vision/ethos.md`, `Vision/protos.md`, `Vision/datom.md`, and
  `Intent/mandatoryTraits.md`.
- Candidate code and tests under `/git/github.com/LiGoldragon/ethos-zero`.
- Capped command witnesses recorded during this subflow.
