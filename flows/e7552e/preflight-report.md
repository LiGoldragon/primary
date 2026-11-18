# Proposal 2 writer preflight — fe5a6930, terminal failure

Core4o4p/qanl admitted one serialized offline preflight before another whole
gate. Exact candidate `fe5a6930871707a7086c9a647867a519734220ef`, sole parent
`d44ce7f8d1cef27fc0af3340d298571ab010399c`; clean worktree
`/git/worktrees/flow-order-lifetime-2b25fa`. Independent mechanical assertion
review fstq passed; that is not execution acceptance.

## Inputs / execution

Immutable git archive SHA256
`f8a38c69033f97cf47e71d38db43cecabb014b126cb162678d4712558e8853c6`, copied once
to Prometheus `/tmp/flow-preflight-e7552e.rEz7eMNp/source`.
Existing toolchain paths were read from the actual Nix test derivation:
Rust m3avjwfs2crh6gk1xy2aky9k52nd0ham,1.99.1; GCC wrapper
3d1c302vw7kc8a5vknhmn34c0pd7zm6m,15.3; Git8wxs6573l730vxkqd6wp58kvxa19csll.
Existing Cargo home registry/git caches were present and no Cargo config file
was found. Cargo was locked and offline, one job; taskset restricted the remote
phase to two available CPUs. No source, manifest, lock, feature, dependency,
build configuration or credential change was performed. Existing matching
Nix-built flow/flow-meta binaries were symlinked next to the test executable,
matching the flake's already-declared actual-CLI fixture environment.

Commands, once and fail-fast:
1. `cargo clippy --all-targets --locked`
2. `cargo test -p flow-nexus --locked`

30-minute local controller bound,29-minute remote work bound, INT then KILL60s.
The local controller initially waited on a FIFO; Core bomq and Field1i1d
received exact START metadata before release. Coreqanl confirmed one release,
not a duplicate controller. Remote phase began21:10:03Z, ended21:30:49Z.
Local PID/PGID1133285; remote phase bash1954206 in group1954205.

## Observed outcome

Clippy **PASS**, one existing warning `clippy::type_complexity` at
`crates/flow/src/hook.rs:546`; no claim of a warnings-denied gate. Flow tests
**EXIT101:1042 passed,18 failed,8 ignored**; test runtime1032.81s.
Both corrected queue_operations fixtures passed, including the exact
Order→Result refusal and separate positive Question/closed-answer setup.

Seventeen failure blocks explicitly report EMFILE/TooManyOpenFiles opening
an eventfd or Unix socket. The remaining test,
`tests::waking::an_order_wakes_an_asleep_primary_fresh`, reports
HerdrUnreadable with no recorded Herdr call. Its cause remains unknown.
Current later SSH metadata observed soft/hard nofile1024/524288. Actual test
process limits were not captured before exit, so the earlier effective limit
is not proved. Resource exhaustion is evidence; its cause, including whether
a low inherited limit or fixture handle retention produced it, is not ruled.
No failing test is disabled or reclassified as an accepted environment failure.

## Terminal / cleanup

After controller exit, a bounded own-root process scan found fixture shell and
coreutils descendants in the remote source directory/original group. Most ended
before targeted cleanup; two remained: bash1995749 and coreutils1995753.
Opened kernel pidfds for those actual matching identities, sent TERM through
those handles, and witnessed both exits. No KILL escalation or numeric stale
PID/group kill. Final own-root scan zero. Local controller group absent.
Only then removed the exact remote source and target workloads. Logs, scripts,
exits, timestamps and cleanup evidence remain at local
`/tmp/flow-preflight-e7552e.GEWEoRbf` and the retained remote root. This is bounded
attribution evidence, not a census of every unrelated host process.

Local evidence hashes:
- clippy.log `663d3156ead6eb06deeae0de07a9a6d1bc815c0fcb564f8776032f0b94ec607a`
- tests.log `5dbefe88196530e199827b56d8d7678f5cb9cefa4dbb2152495a1932e97941ce`
- cleanup.json `73885a77be798df9d3dd12e9467b0999eec0a43307e9f042c45199d5cac79894`

Core received terminal jvy8, cleanup66lk (Uncertain, not resent), then the
additional per-failure analysis/proposed next scope. Allocation release remains
Core's decision. No retry, whole gate, source edit, publication, native test,
merge or switch follows automatically.

## Proposed next bounded step

Read-only comparison of the known Nix gate runner/source and current daemon
LimitNOFILE metadata against SSH/current limits; preserve the unknown historical
test limit. Then propose the smallest environment correction/instrumentation for
separate approval. A new job, test retry, test-thread change, file-limit change
or source change requires a fresh grant. Native bootstrap driver assembly and
final immutable review remain owed independently; no native admission exists.

## Superseding decision

Coreh8aj relays Psychednft: clippyPASS is sufficient; do not pursue the proposed
environment diagnosis. Cleanup66lk/x6be accepted, allocation released. Since
the owned Cargo target was removed, do not rebuild it for18 selective reruns.
Proceed exactfe5a whole gate under the existing Nix policy; this does not
reclassify preflight failures or prove their unknown causes. Gate4 started
21:35:50UTC; its independent result and cleanup are still awaited.
