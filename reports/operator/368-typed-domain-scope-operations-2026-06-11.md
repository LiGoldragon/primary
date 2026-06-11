# Typed DomainScope Operations

Operator correction report for the second recursive `DomainScope` issue on 2026-06-11.

## Correction

The prior `0.9.2` fix removed the forbidden hand-rolled NOTA codec, but the operation layer was still wrong: scope matching and guardian equivalence expansion still converted enum values into `Vec<String>` paths, including `Debug`-stringified enum variants in Spirit runtime code.

That was not a typed domain model. The fix in this round removes the path API from generated scope enums and moves scope operations to structural enum methods.

## Implemented

- `schema-rust-next` commit `bf3ed24e` (`schema-rust-next: emit typed scope operations`)
  - Removed generated `from_path`, `try_from_path`, and `path_segments` for scope enums.
  - Added generated `impl From<Domain> for DomainScope` and child `From<...>` conversions.
  - Added generated `contains_scope` and root `contains_domain` methods.
  - Changed generated relation entries from string paths to nested enum constructors.

- `schema-rust-next` commit `d3bc2289` (`schema-rust-next: emit clippy-clean scope containment`)
  - Made generated leaf-scope containment use typed `matches!` patterns so clippy stays clean without suppressions.

- `spirit` commit `603a9628` (`spirit: make domain scope operations typed`)
  - Repinned `schema-rust-next` to `d3bc2289`.
  - Regenerated `src/schema/domain.rs`.
  - Bumped Spirit to `0.9.3`.
  - Replaced runtime scope matching with generated enum containment.
  - Replaced guardian domain expansion with `DomainScope::from(domain.clone()).expand()`.
  - Updated tests to construct scope values with enums instead of fake string paths.

- `CriOMOS-home` commit `2a3626ef` (`home: pin typed spirit domain scopes`)
  - Pinned Spirit to `603a9628`.
  - Pinned Spirit's nested `schema-rust-next-source` to `d3bc2289`.
  - Activated the corrected generation locally on `ouranos`.

## Verification

Generator:

```text
cargo test
```

Spirit:

```text
cargo test --features nota-text
cargo test --no-default-features
cargo test --features production-migration
cargo test --features agent-guardian
cargo clippy --all-targets --features agent-guardian,production-migration,testing-trace -- -D warnings
nix build .#default
```

Forbidden residual grep:

```text
rg -n "from_path|try_from_path|path_segments|DomainScope::from_path|format!\\(\"\\{value:\\?\\}\"|two_segment_path|segment<|std::fmt::Debug" \
  src/schema/domain.rs src/engine.rs src/store.rs tests/generated_signal_plane.rs tests/runtime_triad.rs
```

No matches.

CriOMOS-home:

```text
nix build .#checks.x86_64-linux.spirit-deployment
lojix-run '(HomeOnly goldragon ouranos li [/git/github.com/LiGoldragon/goldragon/datom.nota] [github:LiGoldragon/CriOMOS-home/main] Activate None None)'
```

Live daemon:

```text
spirit Version
(VersionReported (0.9.3 (1458 9985447145768440856)))

spirit '(Count ((Full [(Technology All)]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
(RecordsCounted (13 (1458 9985447145768440856)))

spirit '(Count ((Full [(Technology (Software All))]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
(RecordsCounted (13 (1458 9985447145768440856)))

spirit '(Count ((Full [(Technology (Software (Engineering SoftwareArchitecture)))]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
(RecordsCounted (5 (1458 9985447145768440856)))

spirit '(Count ((Full [(Technology Software)]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
spirit: invalid NOTA input: unknown TechnologyScope variant Software
```

Services:

```text
agent-daemon.service: active/running, NRestarts=0, ExecMainStatus=0
spirit-daemon.service: active/running, NRestarts=0, ExecMainStatus=0
```
