# Ethos Zero 6.0.0 release

Ethos Zero 6.0.0 is published on `main` at
`409ea065a714ba3ad6946d50f3f5d0b1ddbccbcb`.

The release establishes Library, Signal, and Sema as the only public roots,
with Query/Response Signal generation, named fields, Error vocabulary, public
`File: Protosizable<Output = Protos>`, infallible shared canonical extent
assignment, and typed structural/conceptual errors. It removes retired
Types/Kinds and Fault surfaces. Generated fixtures are current products of the
library generator.

The runtime Cargo pins are Protos
`aac95b0d08a4c7eb7f73c8ea18309f9e2e89315f` and Datom
`35d26d822870356af9b04cacfec40d85600b541d`. The flake producer declaration
pins are Protos `d5616342f5c4654deda3af3858bad68af8b68ce8` and Datom
`35d26d822870356af9b04cacfec40d85600b541d`.

## Gates

Local `cargo test` passed 37 tests: 17 library behavior, 7 CLI, 4 public
integration, 3 freshness, 5 generated-module compilation, and 1 isolated
Signal-without-Datom build. `cargo check --all-targets`, `cargo fmt --check`,
`cargo clippy --all-targets -- -D warnings`, and `cargo doc --no-deps` passed.

Configured-remote `nix flake check -L` passed package, build, test, format,
clippy, docs, policy, and dependency-ethos. The latter generated Protos root
and kinds plus Datom root and kinds on the remote builder.

Producer checkpoint after release: Protos `e198ccdd4235916de970c083742ffe5a322d264e`
passed its 10 remote Nix checks, including generated-contract and 16 tests;
Datom `2dad91afce6237d772767bd4ab19f31276e6999e` passed 12 remote Nix checks,
including generated-contract and 26 tests. Both pin this Ethos revision.
Reservation 1021 was released with the typed receipt
`Released.{ 1021 EthosZeroRecovered 857335 [ /git/github.com/LiGoldragon/ethos-zero ] “Complete Ethos Zero migration” }`.

## Sources

- `/home/li/primary/Vision/ethos.md`
- `/home/li/primary/Intent/anatomy.md`
- `/home/li/primary/flows/857335/reports/implementation.md`
