# Ethos Zero audit-closure final-gate evidence

## Candidate state

The reviewed candidate is pushed `main` at
`b2d63f4f00e09f51c83dcac2a2943b06ab987d9f` (`Fix reviewed generator
invariants`). Its working copy is clean and its full-crate lock 839 is
released. The public version is 5.0.0. Cargo and the flake pin Protos
`2d999f173334` (0.26.0) and datom-codec `41a3c073d5c5` (0.21.0). No substrate
source changed.

The first independent review found four concrete generator defects at
`341c5c57e45d`. The focused independent recheck rebuilt the ordinary CLI from
`b2d`, re-ran each defect probe and reserved allocation controls, and found no
surviving targeted defect. The single authorized final remote Nix gate then
completed successfully.

## Implemented closure

- F4 follows Protos 0.26 directly: headed form head at child 0, body at child
  1, and qualified-head arguments under child 0. Actualization does not remap
  paths. The four required malformed inputs locate literal `Bogus` slices in
  `Vector<Bogus>`, `K<Bogus>`, `K<Sized Bogus>`, and `Item<Bogus>`.
- F5 refuses repeated simple parameter bounds, a reference that actually
  matches multiple parameters, applied alias cycles, and superkind cycles.
  Alias cycling substitutes actual generic arguments while following an alias
  body, so `Types [] [ A<Sized>.Sized B.A<B> ] []` faults as `Cycle(B)` rather
  than emitting a recursive Rust alias. Recursive structs and enums with
  finite indirection remain supported and compile.
- F2 fully qualifies standard containers and retains the existing `Result`,
  `Box`, and recursive `Self` fixture. The exact nested collision input
  `Types [] [ X.[ A.[ V ] ] XA.{ Text } ] []` now generates internal
  `XEthosNestedA` while retaining authored `XA`; it compiles. When that
  reserved synthetic name is authored too, allocation extends it with `X`.
  Generated parameter identifiers similarly allocate away from authored types:
  the generic-shadow fixture emits `AEthosParameter` while preserving authored
  field type `A`; its reserved-name control extends that identifier and
  compiles.
- Grouped imports use supported Protos spelling
  `std:clone:[ Clonable.Clone ]`; direct ascent preserves source segments and
  generated Rust writes `std::clone::Clone`.
- F3 projects `File` structurally through Protos without textualizing and
  reparsing. `Name` validates Protos symbols and Rust identifiers. `Source`
  retains validated segments, rejects generic paths and contextual `Self`, so
  a public source cannot emit module-level `Self::Text`.
- Public `File::generate` validates the whole file before token creation and
  returns `Result<String, Fault>`. Publicly constructed declarations named
  `Self` and identities with 27 constraints return typed faults instead of
  reaching `syn` or `Ident` panics. Declaration, variant, associated-item,
  capability, import, and sourced-reference name positions reject `Self`; an
  unsourced `Self` reference remains intrinsic.
- F9 retains named internal anatomy (`Headed`, `Pending`, `DeclarationSite`,
  `ReferenceRequirement`, and `KindContents`) and homes helpers in traits.
  The authored no-free-functions and no-inherent-methods gates pass.
- The flat declaration budget intentionally applies to `Types`: more than 512
  type declarations fault with `Depth`. A durable witness reads 513 `Kinds`
  declarations successfully. That is the documented supported envelope; this
  work does not introduce a global declaration-count cap.
- Nix applies an 8 GiB virtual-memory bound inside each Cargo derivation,
  `cargoFmt`, and every `runCommand`. The README records the path, import,
  generation, naming, and declaration-budget behavior.

## Independent recheck

The focused recheck at `b2d` force-rebuilt the ordinary CLI under the local
8 GiB, 900-second, one-Cargo-job bound. It confirmed all of the following:

- original nested collision compiles with `XEthosNestedA`, and its reserved
  name control compiles with `XEthosNestedAX`;
- applied generic alias input faults `Cycle.B` and writes no recursive alias;
- public `Self` and 27-constraint files return typed `Err(Conceptual(...))`
  results without panic;
- direct and textual `Source` uses of `Self` return typed `Name.Self` refusals;
- generic-shadow and its reserved-parameter control compile with allocated
  parameter names.

## Final remote gate

Before the final run, bounded Nix evaluation found exactly these eight check
outputs: `build`, `test`, `fmt`, `clippy`, `doc`, `dependency-ethos`,
`no-free-functions`, and `no-inherent-methods`. Derivation inspection found
`ulimit -v 8388608` in every actual Cargo phase or `runCommand` body; the
`dependency-ethos` derivation names the four declarations from the exact
pinned Protos and datom-codec store inputs.

The single `nix flake check --keep-going --print-build-logs` exited 0 and
printed `all checks passed!`. Its local client used an 8 GiB address-space
limit and an outer 1,800-second timeout. The accepted transient Nix options
were `max-jobs = 0`, `fallback = false`, `timeout = 900`,
`max-silent-time = 300`, and the existing SSH remote-builder specification
with concurrency changed from 6 to 2. The output log shows builds dispatched
to that remote builder. All eight final output paths materialized locally.

The remote `test` check passed 55 Ethos tests, 15 generated-code tests, 7 CLI
tests, and 3 freshness tests. The other final check outputs passed Cargo
build, format, clippy with warnings denied, docs with warnings denied, the
four exact dependency declarations, and both authored trait-ontology scripts.

## Remaining language-scope limits

These items are stated as limits rather than resolved policy decisions:

- Same-bare-name kinds with different constraints still have distinct Ethos
  identities. Bare reference resolution can report ambiguity, while Rust
  emission still derives a bare identifier from the name. No Rust-name
  mangling or specialized emitted-name refusal has been selected for that
  case; it remains an open language-policy decision.
- The supported `Types` grammar has three required sections: imports, type
  declarations, and associations. Omitting the association section receives a
  typed arity fault; this work does not infer an empty association section.
- Nexus architecture was outside this task and received no implementation or
  closure claim.
- The direct structural ascent witness covers `File`. No separate claim is
  made here that the `Canonical` wrapper itself bears a direct Protosizable
  implementation.

## Sources

- Main-flow brief and follow-up requirements for F2, F3, F4, F5, F9, focused
  review fixes, and final-gate configuration.
- `flows/1a6ca4/reports/auditEthosZeroAstra.md`.
- `flows/da223f/reports/rewrite.md`.
- `flows/84eb1e/reports/independentAudit.md`.
- `Vision/ethos.md`, `Vision/protos.md`, `Vision/datom.md`, and
  `Intent/mandatoryTraits.md`.
- Candidate code and tests under `/git/github.com/LiGoldragon/ethos-zero`.
- `/tmp/ethos-zero-b2d63f4f-final-flake-check.log` and capped local-command
  witnesses recorded during this subflow.
