# Items 1 and 2, final patch set

Build host: `hostname` returned `prometheus` for every cargo and nix run. Scratch copies in `/tmp` on Prometheus, remotes removed; nothing pushed, nothing in Primary committed.

## Landing order

Land as one set, in this order: protos with a release, then datom-codec, then ethos-zero. ethos-zero's Cargo pins and flake input move to the released protos and datom-codec revisions when they land (the scratch pins are `file:///tmp/datom-codec-item12b` rev 296b25 and the `--override-input` for protos).

**Types book claim 5, a newtype printing as `{ abc123 }`, becomes false on landing.** A newtype prints and parses as its inner value: `abc123`.

## Base commits

- protos: 15b41da, patch `item12-final-protos.patch`.
- datom-codec: 4dff16b, patch `item12-final-datom-codec.patch` (the dry-run-2 patch, unchanged; its scratch commit 296b25 is only a Cargo pin).
- ethos-zero: b2fa8b0 ("Test sourced reference in Memory record position", parent 9ea7c80, changes only tests/ethos.rs), patch `item12-final-ethos-zero.patch`. `git apply --check` against a clone at b2fa8b0 succeeds. The rebase had no conflict.

## Change this pass

Fixture R's `Z.String` stays a newtype, so no `Z_Data` struct is generated. No test expected `Z_Data` (tests/generated.rs builds `R::Z(authored.0)`); the fixture comment in fixtures/inline-collision.ethos claimed a unique payload keeps its short name, and now says R.Z is a newtype with no payload struct. The generated modules are unchanged by this.

## Checks

- ethos-zero, `cargo test`: all pass; lib 21, cli 17, ethos 33, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2.
- ethos-zero, `nix flake check --keep-going --override-input protos path:/tmp/protos-item12b`: 8 of 8 attributes pass (build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods, test); nix reports "running 9 flake checks", "all checks passed!".
- datom-codec and protos: nothing changed there, so not rerun; dry-run-2 results stand (datom-codec 12 of 12, protos 12 of 12).

## Files touched

- protos (1): protos.ethos.
- datom-codec (2): crates/datom-codec-derive/src/lib.rs, tests/composition.rs.
- ethos-zero (35, +359 / -240): Cargo.lock, Cargo.toml, error.ethos; fixtures composition-types, empty-signal, generic-shadow, inline-collision, nested-collision, signal-decimal, tree-types (.ethos); src checking, conception, error, generation, lib, location, protosization, sectioning (.rs); tests cli, ethos, flow_contract, generated (.rs); tests/generated/ alias-format, composition-types, empty-signal, flow-library, flow-operation, flow-signal, generic-shadow, inline-collision, multi-types, nested-collision, orchestrate, signal-decimal, tree-types (.rs).

Provenance receipt: unavailable.
