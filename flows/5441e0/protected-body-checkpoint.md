# Protected replacement draft checkpoint

Exact immutable source head: `16b1303b294d05f23483e67945c617056caaf983`, descended from accepted handover guard2a260. Owned worktree350 is clean. This is NOT a complete or accepted release candidate: dependencies still64/83 and Cargo.nix metadata remains old. No compilation, test execution, new generation, uptake, publication or runtime action occurred. Existing rustfmt and diff whitespace checks pass.

## Authorized scope and authored work
Core0pby released protecting/restarting/waking/launching/reaping plus corresponding fixtures and narrow metadata. Core8rgv additionally authorized lib.rs ConfiguresFromMeta::configure_meta plus existing config/reaping race fixtures, without wire/Memory/timer/receipt changes.

The draft appends internal KeptAtStop::Protected and PaneWatchLapse::Protected, reports ordinary typed protection refusals, and checks protection before direct Refresh/Replace/Restart, successor and ordered replacement recovery, interrupted-launch cleanup, restart phase recovery and derived/pending reap advancement. Reaping checks the obligation Address even when its predecessor is no longer current. A native reap close now revalidates under the dispatch boundary. At-rest protection deliberately preserves ordinary receipt reconciliation, Simplified reply and queued-message draining; only replacement/reap progress and empty OnDemand closing are held. Protected stored-ended bindings are not reinterpreted as fresh recovery wakes.

Only flow-nexus gets explicit version0.56.3; unchanged members retain workspace0.56.2. Its lock self-version and flake identity change accordingly, but generated metadata is still owed after dependency review.

## Configuration ordering and events: draft argument, not yet proved
Only the typed ProtectedAddresses edit acquires dispatch_gate before the configuration snapshot and engine commit. The guard is dropped before apply_configuration, rearm and announcements. Other configuration capabilities preserve existing ordering. Thus effect boundaries that already acquire dispatch_gate and check protection immediately before the native effect are ordered with the policy commit; an earlier read outside that gate is NOT sufficient.

The lock order is dispatch→short engine read/write for the protection commit; it does not take a pane lease, join workers or call Herdr while holding that guard. Reaping's destructive boundary uses dispatch→obligation validation→Herdr close. After a committed protection change, only changed-address pending reaps are asked to rearm, and existing launch_changes is announced. No timer or durable held phase is added. Tests for concurrent configuration/close ordering, event rearm and absence of join/dispatch deadlock remain owed.

## Concrete remaining gaps before review acceptance
- Resume occurs outside the dispatch guard after durable Opening/Spawning preparation. The current entry checks do not prove atomic policy ordering across that external effect; fix and test the actual boundary without introducing callback deadlock.
- Restart recovery's phase transitions and failure/abandon paths need the same scrutiny when protection changes after the initial read; a snapshot-only guard must not consume an obligation after a protected commit.
- Audit every protected asleep/startup identity and successor/reap route; no universal old-Memory proof is claimed yet.
- Add successor/ordered/reap obligation archive-byte retention and no-native-effect fixtures, protection removal/rearm and store-read-failure cases, and actual old Stop fixture.
- Frozen ordinary64→66 archive compatibility, including StoredLaunchOutcome width/tag/validation and old Memory reopen, is still owed. No no-Memory-impact assertion.
- Verify the four accepted receipt bodies/retained-attempt source and fixtures remain unchanged in the full final delta; no SendSeveral union.

## Fixtures authored but UNRUN
In tests/unit/restarting.rs only protected cases changed: another-flow, self and meta Restart now expect exact Protected refusal and assert zero closes/resumes, original process alive and node unchanged. Nonprotected regressions and explicit Stop/Retire cases are untouched. One new fixture reopens all six existing restart phase categories while protected and compares full restart-record archive bytes, record identity, node identity and native no-close/no-resume. This is not the separate frozen ordinary64 LaunchOutcome proof. No source or execution acceptance is inferred from these fixture bodies.

Ordinary66 generated immutable9eb7eec is a separate clean producer checkpoint awaiting Core independent generated-diff review; meta86 remains untouched until actual ordinary publication/fetchability authority. Field generation-only slot5q1b completed0 and was released/cleaned; no heavy slot remains owned here.
