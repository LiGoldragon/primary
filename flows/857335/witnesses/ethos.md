# Ethos Zero release witness

Method: execute library, CLI, integration, freshness, generated-module, and
isolated Signal-without-Datom tests locally; then separately evaluate and run
all Nix checks only through the configured remote builder.

Release revision: `409ea065a714ba3ad6946d50f3f5d0b1ddbccbcb` on `main`.

Exact local gates:

- `cargo test`: 37 passed
- `cargo check --all-targets`: passed
- `cargo fmt --check`: passed
- `cargo clippy --all-targets -- -D warnings`: passed
- `cargo doc --no-deps`: passed

Exact remote gate: `nix flake check -L` passed package, build, test, fmt,
clippy, doc, no-free-functions, no-inherent-methods, and dependency-ethos.
The dependency gate generated four producer declarations: Protos root/kinds
and Datom root/kinds.

The qualified-Self generated Rust witness is
`fixtures/self-kinds.ethos` and `tests/generated/self-kinds.rs`: direct,
Option, Vector, Result, and imported `crate::Wrapper<Self>` occurrences emit
method-level `where Self: Sized`; `Mixed::inspect` remains callable through
`&dyn Mixed`.

Producer final checkpoint: Protos `e198ccdd4235916de970c083742ffe5a322d264e`
passed 10 remote Nix checks (generated-contract, 16 tests included); Datom
`2dad91afce6237d772767bd4ab19f31276e6999e` passed 12 (generated-contract,
26 tests included). Both pin Ethos `409ea065a714ba3ad6946d50f3f5d0b1ddbccbcb`.

Reservation receipt: `Released.{ 1021 EthosZeroRecovered 857335
[ /git/github.com/LiGoldragon/ethos-zero ] “Complete Ethos Zero migration” }`.
