# Lifecycle test matrix witness

Read-only source witness for `/git/github.com/LiGoldragon/kameo/tests/lifecycle_phases.rs` at fork `3486e4f63ea4e87123476cfbdefeb12403540306` and current upstream test files at `main@upstream` (`b4aaee797cc3fd12e8194db406d9d73a6bc021ce`). Tests were not run.

| Mechanism | Fork test and direct observation | What it does not prove |
|---|---|---|
| Terminal wait and state destruction | `lifecycle_phases.rs:466-501`: delayed `on_stop`, delayed `Drop`, weak/strong waits, resource rebind, `Dropped/Stopped`. | It does not independently prove every internal ordering edge; the source order is supplied by `src/actor/spawn.rs`. |
| Weak result visibility | `:503-552`: after `on_stop` but before `Drop`, `is_terminated` and weak result helpers remain unavailable; after wait they are available. | No panic in `on_stop` is tested. |
| Admission vs terminal | `:554-600`: admission false and ordinary send rejected while cleanup is blocked; terminal false until cleanup release. | Control signals other than Stop are not all tested here. |
| Link outcome | `:602-631`: linked observer hook receives equal `ActorTerminalOutcome`. | The test waits for source outcome and then target hook, so it does not establish target hook completion before source lifecycle cell publication in every scheduler interleaving. |
| Bounded saturation | `:633-706`: bounded capacity fills, link/control and Stop still progress, ordinary work does not run. | No stress bound for unbounded control accumulation. |
| Pending ordinary send | `:708-790`: blocked send remains pending before stop, then returns `ActorNotRunning` after admission closes. | No direct atomic race instrumentation; the source double-check is the evidence. |
| Blocking receive | `:792-813`: a blocking receiver wakes for late Stop. | No blocking send race beyond the tested Stop path. |
| Queued ask | `:815-869`: queued ask is not handled and caller receives `ActorStopped`. | No queued tell hook exists in the fork to observe/drop payloads. |
| Startup/cleanup failure | `:871-901`: `NeverAllocated/StartupFailed`; `Dropped/CleanupFailed`; compatibility result error. | No `on_stop` panic test. |
| Restart resource order | `:903-996`: async and thread-spawned replacements observe prior resource drop. | It does not directly observe source lifecycle-cell publication; “terminal outcome” in the test name is operationally witnessed by state drop. |
| Restart mailbox preservation | No fork test found. | Whether callers intended tells to survive fork restart is unresolved by fork tests; code generation invalidation indicates they do not. |

Current upstream comparison tests:

- `tests/stop_gracefully_closes_mailbox.rs`: one-channel graceful stop processes messages queued before Stop, rejects later tells/asks through an accepting flag, and reports `is_alive=false` while draining.
- `tests/supervision_mailbox.rs`: tells survive panic and normal supervised restart, including an actor with children; asks during restart return `ActorRestarting`, and ask-to-stopping-supervisor paths avoid deadlock.
- `tests/on_undelivered.rs`: terminal leftover tells reach `on_undelivered`; pending asks bounce to callers; restart leftovers are preserved rather than sent to the hook; exhausted restart budgets send leftovers to the hook.
- `tests/actor_ref_counts.rs`: current upstream single-`Arc` actor-ref clone/count behavior.

These upstream tests are source observations only; no test command was run.
