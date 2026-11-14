# dzs isolated candidate seal

Status: isolated staged candidate only. It has not been compiled, tested, built, committed, pushed, published, deployed, promoted, or applied to the production repository.

## Binding

- Candidate directory: `/tmp/belief-nexus-dzs-candidate-owned-567be7`
- Exact base commit: `c537aec8eaf6a4bea34ef022744d1df89283db97`
- Base `belief-pair.rs` blob: `db0e42d2883a77f3a43befedf76f2877805b394b`
- Staged candidate `belief-pair.rs` blob: `55a97e14059e31297f8cfbd7894ba3a5be8215f7`
- Staged candidate tree: `0f23753b668da8840a537cef73295ebeec49cf0b`
- Binary staged diff SHA-256: `f681ab1932e4c589049be26ef6feb7fa1b09356e929987c474323ef5323b63b7`
- Scope: `crates/translator/src/bin/belief-pair.rs` only, 460 insertions and 44 deletions
- Patch artifact: `candidate.patch`

The clone is detached at the exact base. The candidate file is staged in its isolated index. No commit object was created.

## Implemented candidate shape

The candidate introduces private `PairSupervisionError`, `PairedChildren`, `ChildLifetime`, and `PairedChildLifetime` types and traits.

After the second child spawns successfully, one `PairedChildren` value immediately owns both `Child` values as `Option<Child>`. Every later return drops this owner. Cleanup takes each live slot before attempting SIGTERM and blocking `waitpid`; both cleanup results remain ignored, matching the current best-effort behavior. Failure to spawn the second child retains the current single-Nexus stop and reap.

Both real bootstrap pipe accessors and every process-ID use go through the owner. Explicit duplicate cleanup branches after ownership are removed. Owner validation failure, bootstrap failure, socket appearance failure, Configure transport failure, Configure decoding failure, typed configuration refusal, and supervision wait failure all return through owner drop.

`wait_for_first_terminal` retains `waitpid(-1)` under the approved source-supported standalone two-direct-child scope. The source explicitly records that `waitpid(-1)` is not intrinsically owned-only and that an externally arranged tracer or child-subreaper can violate the scope.

Only a matching `WaitStatus::Exited` or `WaitStatus::Signaled` removes an owned slot. The already-reaped child is taken before returning, so cleanup can touch only the survivor. `Stopped`, `Continued`, ptrace stops, and `StillAlive` retain both slots and continue. A terminal PID outside both owned PIDs returns the named `PairSupervisionError::UnexpectedTerminal { observed_pid, observed_status }`; it is acknowledged as already reaped and neither owned slot is classified or removed. Native `Errno` is retained as `PairSupervisionError::Wait` and remains its error source.

The candidate adds no thread waiter, pidfd, timeout, escalation, polling interval, socket behavior, placement behavior, startup policy, default deployment, or runtime activation.

## Bounded staged tests

The staged tests have not been run.

- Two real-child cases exercise first Nexus terminal and first Translator terminal status, asserting the exact returned terminal PID and the Option ownership state. These are terminal/status and ownership-state claims only.
- Direct classifier cases prove representative nonterminal statuses retain both slots.
- A direct classifier case proves an unexpected terminal PID returns the typed error and is not classified as either owned child.
- Reachable production paths call the extracted private `run`: owner mismatch after spawn, second-child spawn failure, and Configure transport failure after a non-socket appears at the configured meta Translator path. The tests assert the returned failure boundaries.

The tests do not count kill or wait syscalls, do not claim reaper identity from process absence, do not use an injected wait implementation, and do not install a tracing framework. Take-before-cleanup and wait-error cleanup coverage are source-reviewed properties of the sealed implementation; independent execution remains required.

## Source review before seal

- Exactly one staged path is present.
- `git diff --cached --check` passed.
- The candidate contains no `PairMember`, pidfd, wait thread, or `WNOHANG` polling path.
- Production repository, bead state, prior reports, main/default refs, and runtime state were not changed.

## Independent review gate

An independent flow must review this exact base, blob, tree, and patch before using the reserved Nix slot. Any edit changes the blob/tree/diff hashes and invalidates this seal. No implementation publication is authorized by this artifact.
