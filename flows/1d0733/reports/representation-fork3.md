# Fork 3 candidates: a Represented type whose Representation is a newtype

Build host: `hostname` over ssh returned `prometheus` for every cargo and nix run. The scratch trees are on Prometheus in `/tmp`. Nothing was pushed, and nothing in Primary was committed.

## Bases

- datom-codec main is 4dff16b. Branch 445410 is 776cf4b, which is 4ac7873 ("Represented: the special representation…") then 776cf4b ("Format the overflow case of the ticket refusals"). The parent of 4ac7873 is 4dff16b, the same commit as main, so the rebase onto main changed nothing (git printed "Current branch braced is up to date"). There were no conflicts.
- Scratch clone: `/tmp/dc-f3`, with worktrees `/tmp/dc-f3-braced` (branch `braced`, 440e5d8) and `/tmp/dc-f3-bare` (branch `bare`, 6f137d6). Both branches are unpushed.
- **braced** = 776cf4b plus one commit that adds `tests/newtype-representation.rs`.
- **bare** = 776cf4b plus one commit that applies `item12-on-item5-datom-codec.patch` and adds the bare version of the same test. `git apply` applied the patch cleanly. Its +/- lines are identical to the held patch's lines; only the index lines differ, because the base is different.
- ethos-zero: 07714b0, cloned from GitHub.
  - `/tmp/ez-f3-braced` (96c0382) is 07714b0 with only the datom-codec pin moved.
  - `/tmp/ez-f3-bare` (b968fa8) is 07714b0 plus `item12-on-item5-ethos-zero.patch`, which applied cleanly, and the datom-codec pin moved.
  - In both, `Cargo.toml` and `Cargo.lock` pin datom-codec to `git+file:///tmp/dc-f3` at the candidate's commit (lock source checked). Moving the pin was needed: the flake's `datom-codec` input only feeds `dependency-ethos`, and crane builds the Rust from the Cargo.lock pin. With `--override-input` alone, build, test, clippy and doc would still compile the old datom-codec.

## The test

Both candidates use the same file, `tests/newtype-representation.rs`. Only the expected texts differ.

- `pub struct R(pub String)` (Composing, Datomizable) is the Representation of `Number(u32)`.
- The worked case is `pub struct FlowId(pub String)` holding `"1d0733"`. It has the same derives as ethos-zero's generated `FlowId`, which comes from `FlowId.String` in `fixtures/orchestrate.ethos`. The set's fixture carries no comment saying the String is unideal or that a real hash-based id is needed: a grep of the patched ethos-zero tree for "unideal", "hash-based" and "real hash" finds nothing. The test's doc comment therefore names only the declaration it mirrors.
- The file has four tests:
  - The print equals the expected text exactly. It also equals the Representation's own print, and it contains no `{ {`.
  - The expected text reads back to `Number(42)` and to `R("42")`.
  - Each shape the answer does not print is refused with an error, both as `Number` and as `R`. A doubled brace `{ { 42 } }` is refused too.
  - `FlowId("1d0733")` prints its expected text, contains no doubled brace, and reads back. Each shape that answer does not print is refused with an error.

## Observed text

| | braced | bare |
|---|---|---|
| `Number(42)` / `R("42")` | `{ 42 }` | `42` |
| `FlowId("1d0733")` | `{ 1d0733 }` | `1d0733` |

The worked case under each answer:

- braced: `{ 1d0733 }`
- bare: `1d0733`

Refusals were observed as printed `Debug` output:

- braced:
  - `42`: `Composition, path [], Form { expected: "Struct", found: "Bare" }`
  - `{ { 42 } }`: `Composition, path [0], Form { expected: "String", found: "Struct" }`
  - `FlowId` refuses `1d0733` and `{ { 1d0733 } }` with the same two errors.
- bare:
  - `{ 42 }`: `Composition, path [], Form { expected: "String", found: "Struct" }`
  - `{ { 42 } }`: `Composition, path [], Form { expected: "String", found: "Struct" }`
  - `FlowId` refuses `{ 1d0733 }` and `{ { 1d0733 } }` with the same error.

Neither answer coerces the other's shape.

## Checks, datom-codec

| | braced | bare |
|---|---|---|
| `cargo test --workspace` | 13 composition, 33 core, 1 hygiene, 0 kinds, 4 newtype-representation, 9 represented: 60 pass | 14 composition, 33 core, 1 hygiene, 0 kinds, 4 newtype-representation, 9 represented: 61 pass |
| `nix flake check --keep-going` | exit 0, "all checks passed!" | exit 0, "all checks passed!" |

Both candidates have the same 12 check attributes, and both pass all of them after the worked case changed: archival, build, checked-anatomy, clippy, doc, fmt, generated-kinds, no-forbidden-vocabulary, no-production-free-functions, no-production-inherent-methods, no-zst-behavior and test. The extra composition test in bare is the set's `a_new_type_prints_and_reads_as_the_value_it_holds`.

## Checks, ethos-zero at 07714b0

The 8 check attributes are build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods and test.

- **braced**:
  - `nix flake check --keep-going --override-input datom-codec "git+file:///tmp/dc-f3?rev=440e5d8…"` exited 0 with "all checks passed!".
  - `cargo test` passes: lib 21, cli 17, ethos 32, flow_contract 1 (inner 2), freshness 4, generated 19, print 9, signal_without_datom 2.
  - The represented change does not break ethos-zero.
- **bare** (with the set's ethos-zero patch):
  - Run with the set's protos patch, as the held set ran: `--override-input protos path:/tmp/protos-i5 --override-input datom-codec "git+file:///tmp/dc-f3?rev=6f137d6…"`. It exited 0 with "all checks passed!".
  - `cargo test` passes: lib 21, cli 17, ethos 33, flow_contract 1 (inner 2), freshness 4, generated 20, print 9, signal_without_datom 2.
  - The represented change does not break ethos-zero.
- **bare without the protos override** exited 1. Only `dependency-ethos` failed: `protos.ethos { 17 3 } Conceptual.{ [ 1 1 8 ] SinglePosition }`, the unpatched `ReaderBudget.{ Integer }`. All the other checks passed. The bare answer therefore needs the set's protos patch (`ReaderBudget.Integer`) as well. Represented does not cause this failure.

`nix flake metadata` with each run's overrides shows datom-codec resolved to the candidate's rev, and protos to `path:/tmp/protos-i5` for bare.

## Files touched

Against datom-codec main 4dff16b:

- **braced** (9 files, +460 / -6): README.md, crates/datom-codec-derive/src/lib.rs, datom-codec-kinds.ethos, generated/datom-codec-kinds.rs, src/core.rs, src/lib.rs, tests/kinds.rs, tests/represented.rs, and the new tests/newtype-representation.rs. Against 776cf4b, only the new test is added (+101).
- **bare** (10 files, +531 / -6): the braced files plus tests/composition.rs. crates/datom-codec-derive/src/lib.rs also carries the set's newtype hunk. Against 776cf4b: the derive, tests/composition.rs and the new test (+172).

Patches, each a `git diff 4dff16b <candidate>`:

- `representation-fork3-braced.patch`
- `representation-fork3-bare.patch`

The ethos-zero pin is still the scratch `file:///tmp/dc-f3`. It moves to the released datom-codec revision when one lands.

Provenance receipt: unavailable.
