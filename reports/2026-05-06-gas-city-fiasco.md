# Gas City Fiasco Report

Date: 2026-05-06

## Summary

The last several days of trying to run Criopolis on Gas City exposed a
structural failure, not a single bad commit. We tried variants around upstream
main, v1.0.0, and local fork patches. Each pass uncovered another way for the
system to consume CPU, write to Dolt, spawn sessions, or get stuck in hidden
lifecycle state. The pattern is consistent: Gas City composes several
reconcilers, metadata fields, shell-backed stores, and terminal sessions into a
state-machine stack that is hard to reason about and easy to put into a hot
loop.

The project has useful primitives, but the implementation around them is not a
foundation we should keep extending. The next system should preserve the
primitive shape and reject the state-machine monster.

## What Happened

Criopolis hit sustained idle load from Dolt. The local incident report records
`dolt sql-server` at 93-307% CPU over hours, `.beads/dolt/hq` growing to
3.1 GB, `.gc/events.jsonl` growing rapidly, and repeated `nothing to commit`
warnings. A live trace caught the supervisor repeatedly spawning:

```text
bd update --json cr-a6dk5 --set-metadata quarantined_until= --set-metadata wake_attempts=0
```

The Dolt history showed consecutive `bd: update cr-a6dk5` commits, while
`dolt_diff_issues` showed the content and metadata were identical and only
`updated_at` advanced. In plain terms: an idle city was paying full Dolt commit
cost to restate state it already had.

That was only one layer. Earlier and later tests also exposed:

- managed bd initialization failures where `issue_prefix` existed in YAML but
  not in the SQL config table;
- prebuilt `v1.0.0` start-lock failures;
- no-op metadata writes that stopped disk growth after patching but still left
  high Dolt CPU from connection churn;
- lifecycle wake-loss after a suspended or closed session;
- dog and pool demand surprises from stale routing or default scale checks;
- config-drift loops after startup reload changed the hash of sessions that had
  already been started;
- supervisor demand paths that repeatedly ran store scans, work queries, and
  shell commands even when no meaningful work existed.

This means the experience was not "we found the bug." It was "we fixed one
surface and the next hidden loop became visible."

## Why It Was So Bad

Gas City has too many sources of truth:

- TOML config and layered pack config.
- Runtime provider state.
- Session beads.
- Metadata hashes such as `started_config_hash`.
- Live tmux or subprocess state.
- Dolt SQL state under Beads.
- File events in `.gc/events.jsonl`.
- Cached store state.
- Controller in-memory state.

The system then tries to reconcile all of them by polling, scanning, and
writing markers. When the states disagree, the controller frequently responds
by writing more metadata, starting more sessions, or deferring more work. That
is exactly the wrong failure mode for an orchestration engine. An orchestrator
should make state transitions explicit and externally visible; Gas City often
turns uncertainty into more hidden mutation.

The Beads/Dolt boundary made this worse. The bd provider shells simple store
operations out through `bd` subprocesses. Each repeated metadata update can
become process startup, Dolt connection setup, SQL work, event recording, and a
commit attempt. Even when no data changes, the system can still spend real CPU
and I/O proving that nothing changed.

The implementation also leans heavily on polling. Some push primitives exist
in Gas City, especially bead events and `gc events --watch`, but the live city
still behaved like a polling stack. That violates the design direction we care
about: producers should push, consumers should subscribe, and absent push
support should block the feature rather than invite a polling loop.

## tmux

tmux also belongs in the rejection list for the next system. It was useful as a
cheap way to keep interactive processes alive, but it is a poor substrate for a
modern agent harness. It degrades terminal presentation, including color
behavior, and it exposes a 1990s terminal-multiplexer interface as if that were
a clean process API.

For the next system, terminal display should be a client concern. The runtime
core should own process lifecycle, streams, resize/control messages, and exit
status directly. It should not depend on tmux as the truth of what an agent is
doing.

## Useful Parts To Salvage

The useful parts are the primitives Li already named:

- a city as a directory;
- declarative harness definitions;
- code harnesses presented as a small API;
- work as durable records;
- routing work to an executor;
- prompt templates as user-supplied behavior;
- event emission as the observation substrate;
- an inspectable way to ask what happened.

Those are worth carrying forward. The current implementation around them is
not.

## What We Should Build Instead

The replacement should start small:

1. One city directory.
2. One harness definition.
3. One durable work item.
4. One route from work to an executor.
5. One executor process with direct stream capture.
6. One append-only event log.
7. One subscription surface that pushes state transitions.

No tmux as the runtime substrate. No Dolt-backed write path in the hot loop. No
periodic reconciliation as the default answer. No metadata field should be
allowed to become hidden control flow.

Every state transition should have an owner, an input event, an output event,
and a durable record. If a transition is uncertain, the system should expose
that uncertainty instead of writing another timestamp and trying again next
tick.

## Source Material Read

- `/git/github.com/LiGoldragon/test-city/REPORT-2026-05-05-dolt-amp-investigation.md`
- `/git/github.com/LiGoldragon/test-city/REPORT-2026-05-05-test-city-testing-log.md`
- `/home/li/Criopolis/_intake/findings/2026-05-05-dolt-amp-live-trace.md`
- `/home/li/Criopolis/_intake/reports/2026-05-05-city-investigation-status.md`
- `/home/li/Criopolis/research/answers/dolt-write-amplification.md`
- `/home/li/Criopolis/research/answers/gascity-fork-stability.md`
- `/home/li/Criopolis/gascity-manual/runbook/dolt-high-cpu-when-idle.md`

