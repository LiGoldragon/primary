# Chronos standard-entry experiment

Status: landed only on the two `entry-point` experiment branches. Neither
`main` was moved, merged, deployed, or activated.

## Branches

| Repository | Base | Experiment commit | Branch |
|---|---|---|---|
| `nexus` | `c495f2ac` (0.5.0) | `ec097e31` | `entry-point` |
| `chronos` | `a5cf51f4` (0.3.0) | `68fa82ce` | `entry-point` |

Chronos pins the immutable Nexus experiment commit `ec097e315a3b0b99bc215a72f6c3f6d8b2b060cf` through its Git dependency. It has no path dependency.

`jj git push --bookmark entry-point` completed for both repositories. Its
GitHub response offered pull-request creation for each `entry-point` branch;
the local bookmarks remain at the immutable commits recorded in the table.

## Implemented boundary

`nexus/src/entry.rs` owns the private `Admission`, `MemoryHandle`, and
`OperationHandle` fields and builds the memory, operation, and signal actors
in that order. Its `Door` reads and writes the length-prefixed UDS frame and
holds only the signal actor address. The daemon macro invokes the standard
entry path.

Chronos supplies the concrete signal, operation, and redb memory bodies.
Only existing `SetLocation` and `GetLocation` requests are implemented:
`SetLocation` persists the location, then `GetLocation` returns it with the
existing `Response::Location` and `LocationSource::Manual` values. Other
existing requests receive the existing `Response::Error` form during this
bounded experiment.

`chronos/tests/entry.rs` opens a real Unix listener, sends `SetLocation` over
one socket connection, sends `GetLocation` over a second connection, and
asserts the returned location and existing manual source. The compile-fail
examples on `chronos::daemon::Chronos` demonstrate that signal-side code
cannot construct `Admission`, construct `MemoryHandle`, or read
`OperationHandle.actor`. This is a capability-boundary claim only; it does
not claim that arbitrary Rust cannot independently open a database.

## Validation receipt and limit

The exact remote command was:

```sh
nix flake check --option max-jobs 0 --builders '@/etc/nix/machines' --option fallback false
```

The configured builder file named only Prometheus. The command evaluated the
Chronos flake and its checks, fetched the published Nexus `entry-point`
branch, and dispatched dependency derivations to the Prometheus SSH builder.
The process was no longer present when inspected at
2026-10-04T16:28:30-06:00, but the terminal exit status and a complete
stdout/stderr log were not retained. The transcript retained cache failures:
the `nix.prometheus.goldragon.criome` binary cache timed out or reset while
retrieving narinfo and artifact resources, each reported as a 60-second
attempt. This is an infrastructure-limited remote receipt, not a completed
test result.

The one additionally authorized local command was `cargo test --offline` at
Chronos `68fa82ce5706bc68043d27cd88effbf1d5efcbe8`. It exited 101 during
dependency resolution because `async-recursion v1.2.0` was absent from the
local cache. The full bounded receipt is
`flows/d66c26/evidence/chronos-entry-cargo-test.txt`. No compilation, UDS
assertion, or compile-fail doctest ran, so no fixture has a passing or failing
result.

The intended Nix `test` check is `craneLib.cargoTest`; Cargo's default test
command includes rustdoc tests, so it would exercise the three `compile_fail`
examples as well as `tests/entry.rs` once it reaches execution. The separate
Nix `doc` check only builds documentation and does not substitute for that
doctest execution.

The bounded next step is to restore availability of the Prometheus remote
worker/cache or make the missing Cargo dependency available through the
approved build path, then run the existing check once. No system, cache, or
network configuration was changed here.

## Authorized online Cargo attempt

Before this attempt, Chronos was clean at immutable commit
`68fa82ce5706bc68043d27cd88effbf1d5efcbe8`, and its manifest and lockfile
pinned Nexus `ec097e315a3b0b99bc215a72f6c3f6d8b2b060cf`. `cargo fetch`
succeeded and left the checkout clean; its receipt is
`flows/d66c26/evidence/chronos-entry-cargo-fetch.txt`.

The one permitted following command, `cargo test`, exited 101 at Chronos
library compilation. `src/daemon.rs:69` passes `String` where the existing
`Response::Error` requires `ErrorMessage`; `src/daemon.rs:74` tries to create
that same type with `&str.into()`, but it has no such conversion. The receipt
is `flows/d66c26/evidence/chronos-entry-cargo-test-online.txt`.

This is a compile failure, neither a UDS assertion failure nor a compile-fail
doctest failure. `tests/entry.rs` and the three doctests were not executed.
Cargo left the tracked checkout clean, so the immutable identity remains the
same. No repair was made under this bounded test authorization.

## Typed-error repair and corrected-branch test

The two `ErrorMessage` construction errors were repaired, without changing the
signal contract or the pinned Nexus revision, in Chronos `entry-point` commit
`7899f0c996a72e7d9ed0bde0d524e5e62358dcb0`. The branch retains the failed
`68fa82ce` commit as its parent. `jj git push --bookmark entry-point` moved the
published branch from that parent to the corrected commit.

The one authorized post-repair `cargo test` exited 101 before any test harness
or doctest began. Rust reported E0446 because the public `Nexus` implementation
at `src/daemon.rs:158-160` exposes private associated types:
`ChronosMemory`, `ChronosOperation`, and `ChronosSignal`. The exact receipt is
`flows/d66c26/evidence/chronos-entry-cargo-test-corrected.txt`.

This is a new compilation blocker, not a UDS assertion or compile-fail
doctest failure. It is outside the authorized two-`ErrorMessage` repair, so no
further source change or test retry was made. The next action requires a
separate authorization to decide the visibility boundary for the three concrete
parts.

## Visibility repair and passing test

The public `Nexus` implementation requires public concrete associated-type
identities. Chronos `entry-point` commit
`500094596de495b81cf32b35e127905e7ab0fc42` therefore makes the three concrete
parts and their associated request/result identities public, while retaining
the private `ChronosMemory.database` field and Nexus library's private
`Admission`, `MemoryHandle.actor`, and `OperationHandle.actor` fields. No
signal vocabulary, request, response, or Nexus pin changed. The commit is
published on `entry-point` and descends from the two earlier failed experiment
commits.

At that commit, `cargo test` exited 0 with 66 integration tests passing. It
executed `tests/entry.rs`'s real Unix-socket `SetLocation` then `GetLocation`
round trip, and all three `daemon::Chronos` compile-fail doctests passed. The
complete result receipt is
`flows/d66c26/evidence/chronos-entry-cargo-test-visibility.txt`; one unrelated
documentation test was ignored. Cargo left the checkout clean and the Nexus
pin unchanged.

No provenance receipt handoff was supplied to this flow, so provenance receipt
evidence is unavailable.
