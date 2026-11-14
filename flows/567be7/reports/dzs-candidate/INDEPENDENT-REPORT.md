# Independent dzs candidate review

Status: STOPPED before build on a test-scope blocker. The sealed production implementation is source-sound against the stated constraints, but the candidate's dynamic terminal test does not preserve the production `waitpid(-1)` scope under the default parallel Rust test harness.

## Exact sealed binding

Verified before and after review:

- detached base commit: `c537aec8eaf6a4bea34ef022744d1df89283db97`
- base tree: `a55b4e35641e88e0bb8e1c2f58d42f0f02b97249`
- base pair blob: `db0e42d2883a77f3a43befedf76f2877805b394b`
- staged candidate pair blob: `55a97e14059e31297f8cfbd7894ba3a5be8215f7`
- staged candidate tree: `0f23753b668da8840a537cef73295ebeec49cf0b`
- candidate patch SHA-256: `f681ab1932e4c589049be26ef6feb7fa1b09356e929987c474323ef5323b63b7`
- sole staged path: `crates/translator/src/bin/belief-pair.rs`, `+460/-44`
- no unstaged candidate diff; production repository remained clean
- writer `MANIFEST.sha256` verified all three writer artifacts

The first independent preflight log contains a reviewer command error: it queried the pair blob at a nonexistent `crates/daemon/...` path and exited 128. This was not a candidate compile/test failure. The corrected path and every binding were then verified in `INDEPENDENT-PREFLIGHT-2.log`; no source or test was changed.

## Source review grades

- **A — owner shape:** after the second spawn succeeds, one `PairedChildren` immediately owns both `Child` values as `Option<Child>` (`belief-pair.rs:280-295`). Every later error returns through its `Drop` cleanup. Second-spawn failure retains explicit cleanup of the sole Nexus (`282-290`).
- **A — private evidence and native error:** private `PairSupervisionError`, traits, and owner are local to the binary (`98-169`); native `Errno` is retained and exposed as error source (`121-133`).
- **A — access and ownership transition:** both bootstrap stdin accesses and later PID reads go through owner methods (`158-190`, `302-359`, `377-387`). Matching terminal `Exited`/`Signaled` takes the owned slot before return (`192-210`). Nonterminal statuses retain both (`211-216`). Unexpected terminal PID is typed with its already-reaped status and removes neither slot (`204-209`).
- **A with stated conditional scope — supervision:** `waitpid(-1)` loops through nonterminal statuses and returns only an owned terminal (`219-227`). Source explicitly limits this to the standalone directly-two-child process and names tracer/subreaper violation (`220-222`).
- **A — bounded behavior:** cleanup preserves ignored SIGTERM/wait outcomes and possible blocking (`151-155`, `228-244`); no pidfd, waiter thread, polling, timeout, escalation, socket, placement, or deployment policy was added.

## Blocking test finding

`first_owned_terminal_status_relinquishes_only_that_child` invokes the real global `waitpid(-1)` (`551-579`). In the same unit-test binary, `reachable_post_spawn_failures_return_through_the_pair_owner` independently spawns child processes (`626-665`). No shared serialization exists; repository search found no `RUST_TEST_THREADS`, `--test-threads`, serial-test guard, or test lock. The Nix check uses `cargoTestExtraArgs = "--workspace --all-features"` (`flake.nix:61`) and therefore does not constrain the Rust harness to one thread.

Under default parallel test execution, the first test can reap a terminal child belonging to the reachable-failures test. Production then correctly returns `UnexpectedTerminal`, but the test unwraps success at line 571. This makes the test nondeterministic and, more importantly, runs the `waitpid(-1)` proof outside its stated standalone two-direct-child scope.

Smallest writer revision: serialize every child-spawning unit test in this binary with one private test-only guard, or move the real `waitpid(-1)` case into its own process/test binary. The correction must preserve the existing prohibition on inferring syscall attempts or reaper identity from PID absence. No production change is indicated by this review.

## Dynamic evidence

No Nix command was run. Per the review-first gate, the blocker stopped the task before consuming the one authorized remote check. There are no new derivations, store outputs, or dynamic pass/fail claims. Existing test claims remain unexecuted for this sealed candidate.

Raw evidence: `INDEPENDENT-PREFLIGHT.log`, `INDEPENDENT-PREFLIGHT-2.log`, and `INDEPENDENT-REVIEW.log`. Writer artifacts remain untouched.
