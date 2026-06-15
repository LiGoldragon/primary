# Designer 648 Positional Cascade Review

## Findings

### P1: Spirit's full test gate is red on stale positional-syntax witnesses

The five-repo cascade is pushed and buildable, but it is not yet a green integration
candidate because Spirit's ordinary test suite fails on two stale claim witnesses.

Checked command at Spirit `structural-forms-integration` `9b3bb959`:

```sh
cargo test --features nota-text
```

Result: compile succeeds, then `tests/operator_271_closed_claims.rs` fails:

- `tests/operator_271_closed_claims.rs:102` still expects
  `Justification { Testimony * Reasoning * }`.
- The migrated signal schema now contains `Justification { Testimony Reasoning }`
  at `signal-spirit/schema/signal.schema:139`.
- `tests/operator_271_closed_claims.rs:193` still expects
  `VersionReport { VersionText * }`.
- The migrated signal schema now contains `VersionReport { VersionText }` at
  `signal-spirit/schema/signal.schema:147`.

This is not a semantic regression in the schema model; it is a stale textual witness
for the old name-value / `*` shorthand. It still blocks landing to main because the
branch cannot honestly be called test-green until these assertions are migrated to
the new positional syntax.

Recommended fix: update the two witness strings, and update the nearby comments if
they imply the retired body syntax. Then rerun `cargo test --features nota-text` in
Spirit before any Nix/deploy gate.

### P2: The `agent` dev-dependency skew is real, but it was not the failure I observed

Designer's caveat says Spirit `cargo test` is blocked by stale `agent` ecosystem pins.
The dependency skew is visible: the Spirit test build pulls the structural-forms
schema stack and also pulls `agent` / `signal-agent` / `meta-signal-agent` on main,
which in turn bring separate main-pinned `schema-next` / `schema-rust-next` versions.

However, in this review run that skew did not stop compilation. The build reached
the Spirit tests and failed only on the two stale claim strings above. So
`primary-opzy` remains valid as cleanup/hygiene, but it is not the current hard
blocker for this positional cascade.

## Verified

- Remote availability: `jj git push --dry-run --bookmark structural-forms-integration`
  reports that origin already matches the local bookmark in all five repos.
- `schema-next` at `1abdcd22`: `cargo test` passed, 173 tests.
- `schema-rust-next` at `ab9d16b7`: `cargo test` passed, 86 tests.
- `signal-spirit` at `e7a10e79`: `cargo test --features nota-text` passed, 12 tests.
- `meta-signal-spirit` at `c67ecd52`: `cargo test --features nota-text` passed, 7 tests.
- `spirit` at `9b3bb959`: `cargo build --features nota-text` passed.
- `spirit` at `9b3bb959`: `cargo test --features nota-text` failed as described above.

I did not run the Nix ignored integration tests after the ordinary Spirit cargo test
failed. The next correct gate order is: fix the stale claim witnesses, rerun Spirit
full cargo tests, then run the Nix integration gate.

## Read

The design move itself looks right. The positional form is doing what the reports
claim: it removes the retired `*` shorthand, keeps the generated model stable, and
pushes the real syntax change into schema text rather than generated Rust churn. The
consumer repo diffs are correspondingly small: schema text and lock pins, without
generated source drift.

So my review verdict is: accept the cascade shape, but do not land it to main until
the stale Spirit tests are fixed and the full Spirit plus Nix gates are green.
