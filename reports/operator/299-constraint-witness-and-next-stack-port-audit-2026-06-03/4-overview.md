# Overview

[Audit implementation against intent for missing constraint witnesses; when load-bearing intent is not expressed in constraints, add tests that prove the intended path instead of leaving the intent as prose.]

## What Landed In Spirit Next

The immediate implementation slice landed in `spirit-next`, the current runnable next-stack control component.

Code changes:

- `tests/generated_signal_plane.rs` now has a direct type witness that bare schema bindings such as `Record Entry` and `Rejected SignalRejection` are Rust aliases and direct enum payloads, not wrapper structs.
- `tests/process_boundary.rs` now has a CLI/daemon process witness that the text edge renders direct payload NOTA like `(Rejected (EmptyTopic (0 0)))` and `RecordAccepted` with the direct `SemaReceipt` payload.
- `scripts/check-local-schema-stack` now overrides `triad-runtime` in addition to `nota-next`, `schema-next`, and `schema-rust-next`.
- `scripts/run-nix-integration-tests` now builds with the same four local stack inputs.
- `flake.nix` no longer carries the positive source-grep proof for generated schema content or the local patch text-presence check. Build/test freshness remains the positive proof; grep remains only for retired-surface absence.

## Why This Slice

The newest design thread corrected repeated wrapper output such as `Output::Rejected(Rejected(SignalRejection { ... }))`. The schema-level fix is alias-vs-newtype lowering:

```text
Record Entry
Rejected SignalRejection
```

means exported aliases and direct payloads:

```rust
pub type Record = Entry;
pub type Rejected = SignalRejection;

pub enum Input {
    Record(Record),
}

pub enum Output {
    Rejected(Rejected),
}
```

The new tests prove that shape both at compile/runtime type level and across the real CLI/daemon boundary.

## Verification

Cargo verification passed:

- `cargo test`
- `cargo test --features nota-text`
- `cargo test --features testing-trace`
- `cargo test --features "nota-text testing-trace"`
- `cargo fmt --check`
- `cargo clippy --all-targets --features "nota-text testing-trace" -- -D warnings`

The local Nix stack check was started with path overrides for:

- `nota-next`
- `schema-next`
- `schema-rust-next`
- `triad-runtime`

Result: blocked by the remote-builder phase. The command reached evaluation,
rewrote the four inputs to local `path:` overrides, and began copying sources
to `ssh-ng://nix-ssh@prometheus.goldragon.criome`, then stayed silent for
several minutes. The process was terminated manually so the session would not
end with a live command. This needs a clean rerun when the builder is
responsive:

```sh
scripts/check-local-schema-stack
```

## Sidecar Findings

The schema/triad audit found that the strongest missing upstream witnesses are:

- canonical `SymbolPath`;
- generated trace runtime adapter emission instead of `spirit-next/src/trace.rs`;
- help/description namespace as typed schema data;
- replacing positive flake grep checks in schema repos with cargo/type witnesses;
- a local consumer-style generated engine trait test in `schema-rust-next`;
- generic-boundary checks for `triad-runtime`.

The component-port audit recommends this port order:

1. `upgrade` + `signal-upgrade` + `owner-signal-upgrade`;
2. `introspect` + `signal-introspect`;
3. `persona`.

The `upgrade` triad is next because it exercises schema edits, generated migration code, handover, and last-version compatibility without requiring Persona's full supervision surface.

## Current Work In Flight

Worker `Planck` is independently starting the `upgrade` triad port and will write:

```text
reports/operator/299-constraint-witness-and-next-stack-port-audit-2026-06-03/3-upgrade-port-worker-report.md
```

The main slice does not depend on that worker returning.

## Remaining Gaps

Immediate next implementation gaps:

- Add `SymbolPath` as real schema data and round-trip it through NOTA and rkyv.
- Move trace adapter emission into `schema-rust-next`, then shrink or remove `spirit-next/src/trace.rs`.
- Convert schema repo positive grep checks to cargo/type witnesses.
- Start the `upgrade` triad with real schema files and one process-boundary `AttemptUpgrade` witness.

Deferred but important:

- typed help/description namespace;
- generated help action on every root enum;
- minimal `introspect` as typed trace sink;
- Persona on the triad substrate after upgrade/introspect prove the template.
