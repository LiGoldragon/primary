# Upgrade Triad Next-Stack Port Worker Report

Date: 2026-06-03

Lane: operator

## Summary

Started the upgrade triad next-stack port with a bounded generated-root slice across the ordinary signal contract, owner signal contract, and runtime repo. The slice creates real `schema/lib.schema` sources from the concept schemas, checks in generated `schema/lib.asschema` and `src/schema/lib.rs` artifacts, adds build freshness enforcement, adds flake checks for generated artifact presence, and lands executable witnesses for generated Signal/Nexus/SEMA roots.

The existing hand-written `signal_channel!` contracts and the current runtime `Command`/`Effect` executor remain load-bearing. This slice deliberately adds the generated next-stack surface beside them instead of rewriting daemon dispatch.

## Commits

- `signal-upgrade`: change `vsnnmwwsttsy`, commit `f863a8244429`, `schema: add generated upgrade signal roots`; pushed `main`.
- `owner-signal-upgrade`: change `mxvtvkqyoskl`, commit `a85b20528e74`, `schema: add generated owner upgrade roots`; pushed `main`.
- `upgrade`: change `tkmqzokmrlpx`, commit `9ee09e7c4cfa`, `schema: add generated runtime upgrade roots`; pushed `main`.

## Changed Files

`/git/github.com/LiGoldragon/signal-upgrade`:

- `Cargo.toml`, `Cargo.lock`: add optional `nota-next` feature path plus `schema-next` and `schema-rust-next` build dependencies.
- `build.rs`: lower `schema/lib.schema`, compare checked-in `schema/lib.asschema`, emit `src/schema/lib.rs`, and allow explicit regeneration through `SIGNAL_UPGRADE_UPDATE_SCHEMA_ARTIFACTS`.
- `schema/lib.schema`: real schema-next source for ordinary upgrade operations and generated Signal/Nexus/SEMA roots.
- `schema/lib.asschema`, `src/schema/lib.rs`: checked-in generated artifacts.
- `src/lib.rs`: expose `signal_upgrade::schema::lib` without replacing the current contract types.
- `tests/generated_schema.rs`: executable witness for frame round trip, Signal to Nexus to SEMA projection, SEMA to Signal projection, and trace naming.
- `flake.nix`: include schema artifacts in cleaned source and add generated-schema checks.
- `ARCHITECTURE.md`: document the started schema-next port and generated witness surface.

`/git/github.com/LiGoldragon/owner-signal-upgrade`:

- Same scaffold shape as `signal-upgrade`, with `OWNER_SIGNAL_UPGRADE_UPDATE_SCHEMA_ARTIFACTS`.
- `schema/lib.schema` covers the seven owner operations: `Register`, `Allow`, `Block`, `Query`, `ForceFlip`, `Rollback`, and `Quarantine`.
- `tests/generated_schema.rs` proves owner frame round trip, ForceFlip routing to SEMA write, owner SEMA reply projection, and trace naming.

`/git/github.com/LiGoldragon/upgrade`:

- Same schema generation scaffold with `UPGRADE_UPDATE_SCHEMA_ARTIFACTS`.
- `schema/lib.schema` combines ordinary and owner upgrade surfaces into the runtime-side generated root vocabulary.
- `tests/generated_schema.rs` proves ordinary AttemptUpgrade and owner ForceFlip generated projections plus SEMA-to-Signal reply projection.
- `ARCHITECTURE.md` now records that the generated module is executable but not yet the daemon dispatch path.

## Tests Run

- `SIGNAL_UPGRADE_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --test generated_schema` in `signal-upgrade`: passed, 4 tests.
- `OWNER_SIGNAL_UPGRADE_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --test generated_schema` in `owner-signal-upgrade`: first run exposed the generated `ContractVersion` tuple-newtype constructor shape; fixed the witness and reran successfully.
- `UPGRADE_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --test generated_schema` in `upgrade`: passed, 6 tests.
- `cargo fmt` in all three repos: passed.
- `cargo test` in `signal-upgrade`: passed, including 4 generated-schema tests and 8 round-trip tests.
- `cargo test` in `owner-signal-upgrade`: passed, including 4 generated-schema tests and 6 round-trip tests.
- `cargo test` in `upgrade`: passed, including migration unit tests, binary tests, generated-schema tests, handover tests, invocation tests, and runtime tests.
- `nix build .#checks.x86_64-linux.generated-schema-source-checked-in` in `signal-upgrade`: initially failed during a parallel remote-builder run with no useful builder log; rerun with `-L` passed.
- `nix build .#checks.x86_64-linux.test-generated-schema` in `signal-upgrade`: passed, 4 release tests.
- `nix build .#checks.x86_64-linux.generated-schema-source-checked-in` in `owner-signal-upgrade`: initially failed during the same parallel remote-builder run; rerun with `-L` passed.
- `nix build .#checks.x86_64-linux.test-generated-schema` in `owner-signal-upgrade`: passed, 4 release tests.
- `nix build .#checks.x86_64-linux.generated-schema-source-checked-in .#checks.x86_64-linux.test-generated-schema` in `upgrade`: passed.

## Remaining Blockers

- The generated modules are witnesses, not the load-bearing daemon dispatch path. The next slice needs to replace or bridge the current hand-written `Command`/`Effect` lowering with generated Nexus/SEMA roots.
- The daemon still returns placeholder replies and does not serve generated binary frames across a process boundary.
- There is no durable generated SEMA state engine for migration catalogue, event log, active version, quarantine, or handover state yet.
- The ordinary and owner schema split is represented in separate contract repos, but runtime negative tests for owner-only operations on the ordinary surface and ordinary operations on the owner surface still belong in the next contract-boundary slice.
- Mirror payloads are represented as schema-level raw integer vectors for now; a stricter byte-oriented schema scalar or generated wire adapter remains future work.
- No per-repo `INTENT.md` file exists in these three repos. I did not create one because this turn carried a bounded work order, not new durable psyche intent.

## Final State

All three edited repos have clean working copies after commit and push.
