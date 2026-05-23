# signal-frame foundation implementation

## Result

Implemented `primary-li0p` and the adjacent `primary-avog` helper.

`primary-li0p` is complete: `signal_frame::NamespaceSection`, `signal_frame::SECTION_CUTOFF`, and `signal_frame::namespace::classify` now define the golden-ratio byte-0 split. `NamespaceSection::classify` is also available as an associated const fn.

`primary-avog` is complete at the helper layer: `signal_frame::assert_triad_sections!(ordinary_contract, owner_contract)` performs a const-time daemon-side check that two crates or modules exposing `CONTRACT_SECTION: signal_frame::NamespaceSection` claim opposite sections. The downstream macro bead still needs to make `signal_channel!` emit `CONTRACT_SECTION` automatically.

`context.md` and `plan.md` were requested but are not present in this checkout. The existing dirty `ARCHITECTURE.md` change was inspected and left untouched.

## Changed files

- `src/lib.rs`
- `src/namespace.rs`
- `tests/namespace.rs`
- `tests/namespace_sections_compile_fail.rs`
- `tests/ui/namespace_sections/same_section.rs`
- `tests/ui/namespace_sections/same_section.stderr`

## Validation

Commands run:

- `BEADS_DIR=/home/li/primary/.beads bd show primary-li0p` → exit 0
- `BEADS_DIR=/home/li/primary/.beads bd show primary-avog` → first attempt exit 1 due an embedded-dolt lock, retry exit 0
- `cargo fmt` → exit 0
- `cargo test -p signal-frame --test namespace` → exit 0, 3 tests passed
- `cargo test -p signal-frame --test namespace_sections_compile_fail` → first run exit 101 while generating the new trybuild stderr, accepted stderr, rerun exit 0
- `cargo test -p signal-frame` → exit 0, all package tests passed including the new trybuild compile-fail case
- `cargo check --workspace` → exit 0
- `nix flake check --option max-jobs 0 -L` → exit 0, all checks passed

## Commit

Committed the implementation with `jj` and did not push.

- Commit: `c18a3fda055d41f6b8aeb140b11aebb5479ebc21`
- Change: `tnrtsmqzpnqktmxomytlqkkroxwmnotn`
- Message: `namespace section split foundation`

A separate local report commit was made after the implementation commit. The local `main` bookmark points at the report commit, with the implementation commit as its parent. The working copy still contains the pre-existing dirty `ARCHITECTURE.md` change only.

## Blockers and next steps

No blocker remains for these two beads. Recommended close: `primary-li0p` and `primary-avog` after parent review.

Next implementation bead: `primary-v5n2` should teach `signal-frame-macros` to parse `contract_section`, emit `CONTRACT_SECTION`, and allocate discriminators within the claimed section.
