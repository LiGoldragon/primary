# Independent dzs candidate-v2 review

## Verdict

**PASS (A):** the sealed candidate is bound to the stated base and production
change, its complete child-process test inventory is serialized by one private
guard for each child-producing path, and the one authorized remote full flake
check passed. No source was edited by this review.

## Binding and production seal — A

- Detached base: `c537aec8eaf6a4bea34ef022744d1df89283db97`;
  base tree: `a55b4e35641e88e0bb8e1c2f58d42f0f02b97249`.
- The only staged path is
  `crates/translator/src/bin/belief-pair.rs`; there is no unstaged diff.
- Staged tree: `28187743c0d7e8f5876a37912123f0812a03673c`;
  staged/worktree file blob:
  `44aa10ba2f7a5c79fe078918e9c7489af74ec362`.
- Full patch SHA-256:
  `21e23d3289177042c9cd97241ca4e4fde668a6a0e9df8ecfc3002be5d11d594e`.
- Independent extraction compared the production prefix of prior blob
  `55a97e14059e31297f8cfbd7894ba3a5be8215f7` with the new blob byte-for-byte.
  Both hash to
  `8e8f2f6b50cf47bb77c442f4cd254083999cd661e9f07c83160bbaf93d190f65`.
  The delta is 13 test-only lines: the private mutex/helper and four guard
  acquisitions.
- `git diff --check` and the writer manifest checks passed. Pre- and post-check
  identities are identical.

Raw evidence: `INDEPENDENT-PREFLIGHT.log`, `INDEPENDENT-POST.log`.

## Complete child-test inventory and guard lifetime — A

The test module has exactly eight `#[test]` functions.

- Four Memory tests (source lines 509–558) neither spawn nor reap children.
- `first_owned_terminal_status_relinquishes_only_that_child` (559–591),
  `nonterminal_statuses_retain_both_owned_children` (593–614), and
  `unexpected_terminal_pid_is_typed_and_never_classified_as_owned` (616–636)
  acquire the shared private guard as their first local before using the only
  test-side spawn helpers. Child/owner locals are created later and therefore
  drop before the guard during normal return and unwind; the first test also
  explicitly drops its owner before return.
- `reachable_post_spawn_failures_return_through_the_pair_owner` (638–678)
  acquires that same guard first and calls production `run` three times.
  Each call owns its children and returns only after the local owner cleanup,
  while the caller still holds the guard.
- The only test-callable spawn sites are the guarded fixture helpers and
  production `run`; the only production `waitpid`/kill cleanup is reached under
  the guarded owner in these tests. No uncovered child-producing test path was
  found.

This is a source-order/lifetime proof. It does not infer syscall attempt counts
or reaper identity from process absence. The dynamic run below establishes
termination and returned test status, not those stronger claims.

Raw evidence: `INDEPENDENT-COVERAGE.log` (numbered source, searches, full test
inventory, and exact test-only delta).

## One authorized remote full check — A

From `/tmp/belief-nexus-dzs-candidate-owned-567be7`, exactly once:

```text
nix flake check -L --builders @/etc/nix/machines --max-jobs 0
```

Exit was `0`; Nix reported `all checks passed!`. The `belief-pair` unit target
ran all eight tests, including the four guarded child-process tests, with
`8 passed; 0 failed`. The check built the test derivation remotely on
`prometheus.goldragon.criome` and copied output
`/nix/store/0rlygrqd9f6hnm9w0kn5fdb1cj2vx94n-belief-nexus-test-test-0.1.0`
back. Nix reported that aarch64-darwin, aarch64-linux, and x86_64-darwin were
omitted as incompatible systems.

Raw command/output/exit: `INDEPENDENT-NIX.log`. Extracted store paths:
`INDEPENDENT-store-paths.txt`. Read-only derivation-to-output queries:
`INDEPENDENT-STORE-OUTPUTS.log`.

## Non-blocking limits / artifact correction

- The writer inventory's owner-rejection phrase “no child reached” is
  inaccurate: `run` spawns both children before owner validation. The guard
  still encloses that entire call, so this is an evidence-prose defect rather
  than a coverage or source blocker.
- Existing ignored best-effort cleanup can block; this review establishes no
  timeout, escalation, pidfd/poll, or arbitrary wait-error behavior.
- This review made no commit, push, runtime promotion, default change,
  deployment, bead mutation, closure, or acceptance decision.
