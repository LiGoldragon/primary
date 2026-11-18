# Codex Harness Nexus on the shared release 0.3.0: report

All logs are in /tmp/claude-1001/-home-li-primary/de62988f-3101-5031-9e14-5977310ff255/scratchpad/.

## Commits and gates

| Repository | Commit | Gate | Log |
|---|---|---|---|
| signal-codex-harness-nexus main, 0.3.0 | 68dafec69a6f733cbee74a7a990b9aeffd0c4873 | 7/7 green | r030-contract-gate-1.log |
| build-base main (contract 0.3.0 registered) | b35cb7bdf577b975dee2c0feba45d3879dc1c2c5 | 4/4 green | r030-bb-gate-1.log |
| codex-harness-nexus `daemon` (pushed, not merged) | d312b2ffec496855edbb095af63923393b03d212 | 9/9 green | r030-chn-gate-1.log |
| build-base main (daemon crates moved to d312b2f) | b175b98db04d616b714044b68ecc9374cead178f | 4/4 green | r030-bb-gate-2.log |
| codex-harness-nexus-tests main | 697cb793c336fc58afc9b23fa032c659cc4be40f | 6/6 green | r030-chnt-gate-1.log |

- **What the gates ran.**
  - The daemon's gate ran cargo-nix, crate-versions, crate-features, generated, fmt, the three members and default. Its daemon check passed bootstrap_order (2) and lane_failure (5).
  - The tests gate ran nexus.rs (14 passed), pair.rs (12 passed, 0 ignored) and transitions.rs (2 passed).
- **Repeated runs.** Before the tests gate, I ran pair.rs 15 times on the builder against the daemon package built from d312b2f. All 15 passed. Logs: r030-chnt-test-1.log and r030-chnt-repeat-1.log.
- **Pins.**
  - The workspace takes nexus-exchange and nexus-serving at a4bc0113c10c34ec9d92cde2d650eca9324144db, translator-client and translator-serving at 2739d586e1455a001661fc85a8a61b6219aa99df, and signal-codex-harness-nexus at 68dafec69a6f733cbee74a7a990b9aeffd0c4873.
  - The tests repository takes the same, plus the daemon crates at d312b2f.
  - Each lock holds one source per crate, and every crate is inside its base's set; the crate-versions and crate-features checks prove it.
  - On the contract, cargo first picked errno 0.3.15, libc 0.2.191 and rustix 1.1.6. I pinned them back to the base's 0.3.14, 0.2.189 and 1.1.4.
- **Base pins.** The contract's base is 555555e and the daemon's is b35cb7b. The tests' base is b175b98, and the daemon input follows it.

## Contract shape chosen (signal-codex-harness-nexus 0.3.0)

The contract imports `nexus_exchange:[ LaneFailure ]` (nexus-exchange 0.3.0, plain, with `datom` turning on `nexus-exchange/datom`). It adds two variants, in the existing style of a unit success and typed refusals:

```
[ Reported
  Subscribed.Stream<Observations Changed>
  ReportedLaneFailed.LaneFailure      ; recorded; the lane failed only where the record did not need it
  ReportRefused.ReportFailure ]
ReportFailure.[ … Unrecorded.Diagnostic
                LaneFailed.LaneFailure ]
```

- `ReportRefused(LaneFailed(..))` means nothing was recorded, because the effect needed the lane.
- `ReportedLaneFailed(..)` means the report is recorded and the lane failed only on a part the record did not need.
- ethos-zero pairs inputs with outputs by position, so `ReportedLaneFailed` has to come after `Subscribed`. In the generated `Answering::report`, it is answered on the `Err` side, the side for every answer other than Reported.
- In build-base, 0.3.0 is registered beside 0.2.x. Its datom set gains `nexus-exchange/datom`.

**The meta contract is unchanged.** None of its answers can carry a lane failure. Configure and Subscribe send no emission. A failure while the translator forwards to the Nexus is the translator's NexusFailure, not an emission lane failure.

## What changed in meaning

- **A meta Subscribe stays open.**
  - The daemon accepts with `accept_meta` and spawns `MetaConnection::<Daemon>::serve` on the runtime.
  - `MetaAnswering` answers through the core's configuration publisher, `Reply::Subscribed`, and `subscribed(frame)` is `Output::Subscribed(frame)`.
  - The open subscription carries each Nexus setting, each change in the awaited directories (from Configure, from the watch at startup, and from the watch's follow), and the translator's TextBudget sets, which translator-serving writes in.
  - **New refusal:** a meta Subscribe before the subscriber capacity is set is now refused CapacityUnset. That is what the core's subscribe and the contract always said; before, the daemon answered it with one readout. `ListenerFailure::Meta` now carries the io::Error.
- **Memory path.** The core's own MemoryPlacing is deleted, and the daemon uses `nexus_exchange::MemoryPlacing`. Named gives `codex-harness`, so the file is still `codex-harness.memory` in the place's state directory. The pair test checks it through the shared trait.
- **Lane failures (change A).** A lane fault reaches the caller as `ReportFailure::LaneFailed(LaneFailure)`, never as Unrecorded. LaneReporting is deleted.
- **Recorded whatever the lane does (change B).**
  - New types carry the failure: Outcome gains `ReportedLaneFailed.{ EventBatch LaneFailure }`, and `perform` returns `Performed.{ Vector<Changed> Option<LaneFailure> }`. Both are declared in Ethos and regenerated with ethos-zero 415c370.
  - The watch thread logs a committed operation with a lane failure as "committed; its lane failed".
  - How each operation now behaves:
    - **SessionStart, new session:** if the identity claim's lane fails, it is refused LaneFailed and nothing is recorded, since the record needs the flow id. If only the rollout lookup's lane fails, the session is recorded, its rollout Unlocated, and the answer is ReportedLaneFailed. The watch finds the rollout by its first row at its next write.
    - **SessionStart, known session not yet watched, naming no path:** this is the lookup alone. The session is recorded, its rollout is left as the Memory holds it (a Pending path stays Pending), and the answer is ReportedLaneFailed.
    - **PermissionRequest, PostToolUse, PostCompact:** they use no lane, so nothing changes.
    - **Discovery of a rollout a hook named:** the attachment needs no lane. It stays committed when the lane fails its first read; that read is answered with the lane failure and retried at the next write.
    - **These still need the lane and are refused LaneFailed:** a rollout read, and identifying an unnamed rollout by its first row. Both are internal to the watch, which logs them.

## Tests

- **Un-ignored:** `a_launcher_ended_by_sigterm_ends_its_pair`. It now also asserts that the launcher fails, and it passes.
- **Added, tests repository:** `an_open_meta_subscription_carries_each_change_of_the_translator_and_the_nexus`. It passes.
  - It reads one open `codex-harness-meta` Subscribe answer by answer, with no sleeps, each wait bounded by a deadline.
  - The answers it checks, in order: Opened, which carries a text budget; `Changed(Set(TextBudget))` after the translator sets one; `Changed(Set(SessionsDirectories))` and `Changed(AwaitedDirectories([dir]))` for an absent directory; and `Changed(AwaitedDirectories([]))` once the directory is made.
- **Changed, tests repository:**
  - The readout is the first answer of a meta subscription, and `Subscription` is generic over its answer.
  - The invalid-setting test now shows CapacityUnset before any capacity is set, then sets one and reads the rest back.
  - The text-budget readout test configures first.
  - nexus.rs reads `Performed` through a `performed` helper that asserts no lane failure.
- **Pair test under a lane fault: it cannot be induced on the real pair.** The real translator answers FindRollout Unfound at once. The ClaimIdentity emission comes first, so ending or stopping the translator fails the claim, or the CLI's own request, before the lookup. The in-process tests are in the daemon crate's tests/lane_failure.rs:
  - `a_session_start_whose_rollout_lookup_lane_failed_is_recorded_unlocated_and_answered_with_it`. The translator claims the identity and leaves the lookup unanswered. The answer is `ReportedLaneFailed(Unanswered)`, the record exists with flow 4c85ce and rollout Unlocated, and `woken` of a written rollout yields Discovering.
  - `a_new_session_whose_identity_claim_lane_failed_is_refused_lane_failed_and_never_recorded`. The answer is `ReportRefused(LaneFailed(Unsubmitted))`, and nothing is recorded.
  - Both pass. The daemon crate gains `flow` as a dev-dependency.

## Open questions

1. **Meta Subscribe before the capacity.** It is now refused CapacityUnset, so nothing can read the configuration before a capacity is set. I took this as part of adopting the stream, since a publisher needs a capacity. The alternative is to answer one readout and end when no capacity is set. Is the refusal what is wanted?
2. **The known-session case.** A SessionStart of a known session under a lane fault leaves its rollout as it was (Pending stays Pending), rather than forcing Unlocated. For a new session the two are the same.
3. **Default features do not build.** translator-serving has no gating for its `text` feature, so codex-harness-translator does not compile with default features alone; this was already so at 0.2.0. The flake builds it only with text, so the gate is unaffected.
4. **Still standing from the handover:**
   - an unwatchable directory that is created stays awaited, with the failure shown only on stderr;
   - moving an ancestor away is not detected;
   - Configured does not name awaited directories;
   - the 0.2.x removal note for Mind flowNexus Opus.

   The gap "meta Subscribe answers only one Opened frame" is closed.
5. **Not done here, left to the lane:** telling Field, the Done to Psyche core Opus, and the audit and merge of `daemon`.

## Builder processes

Everything I started on prometheus ran in the foreground over ssh, and each has ended:
- the ethos-zero generations;
- cargo update, rustfmt, clippy, build and test under `nix develop`, including the 15 repeated runs and the pair processes they started;
- the crate2nix generate runs;
- one `nix build` of the daemon package.

The five nix-fast-build gates removed their own temporary directories, and I checked that none remains. At the end, pgrep matched no codex-harness, crate2nix, nix-fast-build or ethos-zero process of mine. The only cargo process was another flow's, PID 1302159 in /tmp/offload-7b5174/flow, which I left alone. I removed my scratch, /tmp/offload/r030-de6298.
