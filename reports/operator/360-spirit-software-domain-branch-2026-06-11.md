# Spirit Software Domain Branch

Operator report for the Spirit main update landed on June 11, 2026.

## Result

Spirit main now includes commit `c30bed38` (`spirit: add software domain branch`).

The old guardian feature bookmark was deleted after its work merged. Spirit `main` had already moved through the guardian hardening commit, and this session advanced it again with the software domain vocabulary.

## Implemented

- Added `Software` as a top-level `Domain` branch with 12 nested clusters: `Languages`, `Theory`, `Systems`, `Distributed`, `Data`, `Intelligence`, `Security`, `Quality`, `Operations`, `Observability`, `Surfaces`, and `Engineering`.
- Moved software subjects out of `Craft`; `Craft` now stays physical: electronics, construction, carpentry, metalworking, sewing, manufacturing, repair, engineering, handicraft, and invention.
- Updated the automatic domain classifier so schema, programming, testing, architecture, intelligence, and infrastructure labels map into concrete `Software` leaves.
- Bumped the durable Spirit store schema from 7 to 8.
- Added a production store upgrade path from schema 7 to 8. It decodes schema-7 records with private schema-7 archive types, maps old software-like `Craft` leaves into the new `Software` branch, and writes a fresh schema-8 store.
- Updated public NOTA examples and tests to use nested enum value syntax such as `(Software (Data SchemaEvolution))`.
- Added schema witness coverage proving software vocabulary lives under `Software` and is no longer listed under `Craft`.

## Syntax Note

The correct NOTA value spelling for nested domain enum payloads is nested:

```nota
(Software (Data SchemaEvolution))
(Software (Operations InfrastructureAsCode))
(Software (Engineering SoftwareArchitecture))
```

The flat adjacent form `(Software Data SchemaEvolution)` is not the generated value syntax for this shape.

## Verification

Passed in the Spirit repo:

- `cargo test --features production-migration,agent-guardian,nota-text`
- `cargo test`
- `cargo clippy --features production-migration,agent-guardian,nota-text -- -D warnings`
- `nix flake check`

`nix flake check` passed all checks for the Linux system set and omitted incompatible Darwin/aarch64 systems as usual.

## Deployment State

This is pushed to Spirit `main`, but not deployed by this operator turn. The live `spirit Version` response showing `0.8.1` means production is still running the previous deployed package and store schema 7. The new pushed source is package `0.9.0` with store schema 8 and a schema-7-to-schema-8 upgrade tool.
