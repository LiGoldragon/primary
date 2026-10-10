# The ethos-zero contracts onto signal 7.0.0's exchange layer

Flow 3ec648, 2026-10-02. Both contract repositories are at 1.0.0 on main, and
`nix flake check` passed for each, run as a detached unit against the commit.
Neither is deployed, and nothing serves them yet.

## Per repository

| Repo | Version | Commit on main | Gate | Duration |
|---|---|---|---|---|
| signal-ethos-zero | 1.0.0 | `d2a98d3f` (on top of `4876e4d9`) | `nix flake check` green, 11 checks | 15 s |
| meta-signal-ethos-zero | 1.0.0 | `d61bb37c` | `nix flake check` green, 11 checks | 32 s |

The two runs were short because Prometheus already held the dependency
derivations from the orchestrate work. The checks are `build`, `test`,
`test-generated-contract`, `test-exchange-envelope`, `test-datom-contract`,
`test-doc`, `doc`, `fmt`, `clippy`, `no-free-functions` and
`no-inherent-methods`.

The first gate on `4876e4d9` failed in one check, `test-datom-contract`. The
Nix source filter dropped `examples/round-trip.datom`, which that test reads.
`d2a98d3f` adds a `.datom` filter. Meta had the filter from the start.

## What moved, in both

- signal-frame 0.3.2 is gone. Both crates now depend on signal 7.0.0
  `66e7b153`, and each has `impl signal::Contracted for Query` with
  `ETHOS = include_str!("../ethos/signal.ethos")` as the contract source. The
  ethos text opens with a paragraph on the exchange layer: the greeting, then
  one exchange per query, and Subscribe answering on its exchange until it
  is abandoned.
- Removed: the `*Wire` binding enums (ContractId 7 and 8, revision 4), the
  frame aliases, `ExchangeDecodeFault`, `WireConversion` and its impls, and
  the orphaned `src/codec.rs`.
- The eight free functions the survey counted were the public
  `encode_request`, `encode_response`, `decode_request` and `decode_response`,
  four in each crate. Each crate also had private `request_route` and
  `response_route`, and the orphaned `codec.rs` had `validate`. All of them
  are gone. The behaviour they carried now belongs to data-bearing types in
  signal: `Signalizable` and `Restorable` on `Dispatch<Query>` and
  `Delivery<Response>`. The Query root carries the contract identity through
  `Contracted`.
- Added `checks/no-free-functions.sh` and `checks/no-inherent-methods.sh`,
  copied from meta-signal-orchestrate and wired as flake checks. I ran
  no-free-functions against each old `src/`. It failed both, listing 7 free
  functions in each.
- The flake now has the meta-signal-orchestrate shape: rust-build,
  `rust-toolchain.toml`, and its `flake.lock` copied so the inputs are
  identical.
- Pins:
  - datom-codec 0.32.2 `4dff16b4` and protos 0.32.2 `15b41da8`, the current
    main of each. Both are optional, behind a new `datom` feature.
  - ethos-zero 15.0.0 `3d330276`, main, as a build dependency only.
  - `build.rs` holds `src/generated/signal.rs` byte-identical to the
    generated output. I dropped the duplicate `tests/regeneration.rs` and
    `examples/regenerate.rs`, along with the ethos-zero dev dependency.
- The lock has three protos and three datom-codec versions, but only 0.32.2
  is a runtime dependency. 0.32.1 comes in through ethos-zero 15 and 0.31.0
  through signal's own ethos-zero 10 build dependency; both are build-only.

## ethos-zero 15 against the two files

- Neither file has a `Sema` or `Memory` head; both are `Signal` files, so no
  rename was needed.
- Refusal: under 15.0.0 both files were refused with
  `Conceptual.{ [ 1 3 0 1 ] Undeclared.Text }` (ordinary at `{ 5 14 }`, meta
  at `{ 5 22 }`). `Text` is not an intrinsic, so every `.Text` alias is now
  `.String`.
- A change in meaning that 15 does not refuse: a bare variant that names a
  declared type now carries that type. `ObservationSelection.[ Assemblies ]`
  generated `Assemblies(Assemblies)`, and
  `MetaObservationSelection.[ Configuration Sources ]` generated
  `Configuration(Configuration)` and `Sources(Sources)`. Under the old
  generator these were bare selections. To keep them bare, I made two changes:
  - The single-use vector aliases became inline `Vector<…>` in
    `AssemblySnapshot` and `SourceIndex`. The Rust fields are
    `assembly_summary_vector` and `source_vector`.
  - Meta's `Configuration` struct is renamed `EthosNexusConfiguration`, after
    `OrchestrateNexusConfiguration`.

  Datom text does not change, because it names variants and not types. The
  living may prefer other names.
- The files are written in the vertical form.
- Datom shape: a one-field struct is braced, as in
  `Generate.{ { ethos-zero ethos/signal.ethos } }`. The old example lines did
  not have the braces and did not read. They have been rewritten, and a new
  `datom` test reads every line as a Query or a Response and reads the
  printed form back equal: 2 queries and 7 responses for ordinary, 3 and 7
  for meta.

## Tests

- `tests/exchange_envelope.rs`:
  - Ordinary has 5 tests: the digest, a foreign source refused, the greeting
    and a Generate as dispatches, a refusal answered and then ended, and a
    Subscribe told apart from a Generate by exchange, with Abandon.
  - Meta has 4 tests: the digest, the ordinary ethos-zero peer refused at the
    meta socket (signal-ethos-zero `d2a98d3f` is a dev dependency), a
    Configure answered and ended, and a Sources subscription told apart by
    exchange.
- The digest oracle is FNV-1a over the ethos file, computed in Python:
  - ordinary `423590495342270605`
  - meta `2800736205933196315`
- Seen failing: with `CONTRACT_SOURCE = ""`, the two digest tests in each
  crate failed. The envelope-only tests passed in that state; I did not see
  them fail.
- `tests/generated_contract.rs` holds the portable rkyv round trip, and the
  datom example test under `datom`.
- clippy `-D warnings`, `cargo fmt --check` and `cargo doc` with
  `-D warnings` are clean locally.

## For whoever follows

- `Unsubscribe` is still in both vocabularies even though signal's `Abandon`
  now ends a subscription. Removing it is a vocabulary decision, so I left it.
- No checkout under `/git` has a Cargo.toml that names either crate. Remote
  ethos-zero branches (`ethos-binding-542442`) pin the 0.5.0 revisions, and
  they keep working until they repin.
- Lock 11579 was taken on both checkouts and has been released.

## Sources

- signal 7.0.0 `66e7b153`: `src/accord.rs`, `src/exchange.rs`,
  `src/portable.rs`
- ethos-zero 15.0.0 `3d330276`: `UPGRADES.md`, the CLI's `Check` and
  `Generate` against both files, before and after the edits
- signal-orchestrate 4.0.0 `4e683453` and meta-signal-orchestrate 4.0.0
  `972a3b03`, used as the shape
- `/home/li/primary/flows/3ec648/reports/orchestrate-signal7.md`
- The `nix flake check` logs for `4876e4d9`, `d2a98d3f` and `d61bb37c`,
  run by this subflow
