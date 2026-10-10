# Pending-start recovery candidate — report-only handoff

Owner: Field Ultra Low Luna `c88918`. This record documents a candidate
source interface and its boundaries. It does not integrate Flow main, change
source, alter runtime state, or establish deployment or lifecycle readiness.

## Candidate provenance

The supplied Flow handoff is branch `field-pending-recovery-753e69`,
remote-verified at `481b6909ef08dd7d2573cf73ae1df1024fb9b7b2`, based on
`cd752e0f`. The named helper is
`crates/flow-nexus/src/pending_start_recovery.rs`, SHA-256
`4640910568c7ef56ecc4fc5d72316e3516ef9eb95bdc12f1978b0762a14b00e8`.

The helper is a pure decision boundary for a reserved Flow start. It models
reserved, uncertain, accepted-thread, and failed states; requires exact Flow
and attempt identity; preserves uncertainty after ambiguous transport or
persistence outcomes; and rejects conflicting evidence. It does not start a
thread, persist a state, delete a reservation, resolve a route, or claim that
an ambiguous error means no native thread exists. Its caller must persist each
returned state through the future store integration.

Direct commit file-list evidence for `481b6909ef08dd7d2573cf73ae1df1024fb9b7b2`
names only `crates/flow-nexus/src/pending_start_recovery.rs`. The earlier
`nix/resolve-cargo-lock.nix` observation came from a branch-versus-parent
comparison and must not be attributed to this commit. This report therefore
records the source commit as a one-file change.

## Test and planning boundary

Terra independently reported direct tests `3/3` and disposable tests `7/7`.
Those are handoff receipts, not a test run repeated by Luna. Mind accepts the
pure interface for integration planning only. Neither receipt establishes that
the helper is compiled into Flow Nexus or installed in the running service.

The following remain open integration gates:

- f72's Flow store work under lock `2836` must persist the state transitions
  with exact attempt ownership and guarded mutation.
- Mind's library integration under lock `3830` must define the consumer
  boundary without changing this candidate's tested behavior.
- The helper must be wired into the owning crate, then the integrated tree
  must pass its focused and full tests; the reported generated meta-signal
  assertion currently blocks the full crate.
- Terra must independently test the exact integrated revision, including
  replay, ambiguity, identity mismatch, and conflicting-evidence cases.
- Installed source parity, deployment, native/Herdr binding, and any live
  lifecycle acceptance require separate witnesses.

No Flow main cherry-pick, runtime action, route or seat change, source edit,
or duplicate test was performed by this documentation commit. Locks remain
separate; no lock transfer is implied.

## Sources

- Flow branch handoff: `field-pending-recovery-753e69`, commit
  `481b6909ef08dd7d2573cf73ae1df1024fb9b7b2`, base `cd752e0f`.
- Read-only source witness for
  `crates/flow-nexus/src/pending_start_recovery.rs` and its supplied SHA-256.
- Terra direct `3/3` and disposable `7/7` test receipts supplied in the
  handoff.
- Mind pure-interface integration-planning acceptance supplied in the
  handoff.
- Pending integration ownership: f72 store lock `2836` and Mind library lock
  `3830`.
