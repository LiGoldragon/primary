# Contract version bump — one label, one wire format

Subflow of 38de5b, 2026-09-25. Fresh clones in the subflow scratchpad
(`bump-5a1c/`); Orchestrate lock 6349 on both clone paths, released.

## Rule applied

Versioning skill: "Update the version surface changed by public behavior, wire,
storage, package, or deployment changes." It names no number for a
required-field addition; a required field breaks the wire, so the major moves
(signal-flow 3.0.0, meta-signal-flow 5.0.0), as the brief proposed.

## signal-flow

- Before: origin/main 0d4ed64, 2.2.0 (same label as 7ba21d0, different wire).
- 54f09c1 "Bump to 3.0.0 for required LaunchProfile SystemPromptBundleFile".
- f881ab3 "Gate datom contract tests on the datom feature".
- After: origin/main f881ab35ee5ffe30090502b10ba8f2878399c1c3, 3.0.0.
- `git diff --stat ab70332 f881ab3`: Cargo.toml, Cargo.lock, tests/contract.rs
  only — wire identical to ab70332.
- `cargo test --features datom`: contract 5 passed, lib 0, doc 0; 0 failed.
- `cargo test`: 0 run, 0 failed (compiles now).

## meta-signal-flow

- Before: origin/main a34bc65, 4.1.0 (same label as 85a5d40), pin ab70332.
- 6a3830c "Repin signal-flow 3.0.0 and bump to 5.0.0" (both dependency and
  build-dependency pins to f881ab3; Cargo.lock follows).
- a1316a0 "Gate datom contract tests on the datom feature".
- After: origin/main a1316a08e70a985e741e4a9ab663811f59b6e68b, 5.0.0.
- `cargo test --features datom`: contract 3 passed, lib 0, doc 0; 0 failed.
- `cargo test`: 0 run, 0 failed (compiles now).

## Plain `cargo test`

Neither repo has CI, README, or flake declaring the datom feature for tests.
Fix applied: `#![cfg(feature = "datom")]` as the first line of each
`tests/contract.rs`. The library and its `default = []` feature set are
unchanged, so the Nexus's non-datom build is untouched. Plain `cargo test`
now passes but runs no contract tests; they still need `--features datom`.

## Flow repo

Untouched. Its 0.7.0 pin to ab70332 stays valid: `git branch -r --contains
ab70332` lists origin/main. That pin now resolves to a revision whose
Cargo.toml says 2.2.0; the 3.0.0 label is carried by f881ab3.
