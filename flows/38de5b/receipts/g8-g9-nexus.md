# Receipt: Flow 0.9.0, Nexus side of G8 and G9

Opus implementation subflow of Psyche High 38de5b, 2026-09-25.

## Landed

- LiGoldragon/flow main 8f8a71a (0.8.1) to **28a78d2** "Flow 0.9.0: Replace, LaunchStatus and Observe.Launch". Branch `g8-g9-nexus-38de5b` is at the same revision. After the push, `git ls-remote origin main` returned 28a78d24f825e72e4d3e3073a57ef615e962a48d.
- The branch was started from 972d8d2. Main moved to 0.8.1 during the work: 470dcc4 and 8f8a71a are the G2/G3 composition and launch changes. I rebased onto 8f8a71a. The conflicts were in the version lines only. One fixture was adapted to `LaunchReceipt::MARKER`.
- Pins:
  - signal-flow 5ca97ce (4.0.0).
  - meta-signal-flow 4748cfa (6.0.0). I read meta-signal-flow's main at push time and it was still 4748cfa, so the announced `RecipientDisposition` patch had not landed and is not pinned.
- Version: 0.8.1 to 0.9.0 (wire change on both edges), in `Cargo.toml` and `flake.nix`. UPGRADES.md and DESIGN.md are updated.

## What it does

- **Replace** (`launching.rs`, `LaunchesFlows::replace`):
  - A missing predecessor is refused as `PredecessorAbsent`, an unknown one as `UnknownPredecessor`, and a Stopped one as `PredecessorStopped`. These checks run before any launch.
  - A `Replacement` record (request ID, predecessor) is stored, and then the one Start path runs.
  - On `Started`, `reap` runs in this order:
    1. The predecessor is recorded `Stopped`.
    2. Its pane is refreshed and closed.
    3. The `Replaced` outcome is recorded. This record is what releases the successor to routing.
  - Until then the successor is held: `ResolveRecipient` answers `FlowUnavailable` and `Send` answers `RouteUnavailable`.
  - If the close fails or the route is unavailable, the answer is `ReplaceRejected.ReapRefused.<StopRejection>`. The predecessor is Stopped and the successor is still held, so neither flow is routable. A repeated `Replace` of the same request picks up the reap again.
  - `ResolveRecipient` now refuses every `Stopped` flow. MetaBindExisting treats `FlowUnavailable` as `DuplicateFlowId`.
- **Launch outcomes:**
  - A new store table records `Started`, `Replaced`, `StartRejected` or `ReplaceRejected` once an attempt has been reserved for the request.
  - A repeated Start or Replace of a settled request answers the stored outcome.
  - A rejection before reservation (composition, adapter) is not stored, and the request may be sent again.
- **LaunchStatus:** answers the stored outcome, else `LaunchPending(attempt)`, else `LaunchStatusRejected.UnknownLaunchRequest`. It is served outside the dispatch gate, so it never waits behind a running Start.
- **Observe.Launch** (`ObservesLaunch`, served on the connection):
  - On open it sends the current answer. After that it sends one `LaunchPending` frame per phase change, then the outcome frame, and then the Nexus closes the exchange.
  - It waits on the store's `LaunchChanges`, a Mutex/Condvar count that every attempt or outcome write advances. There is no timer and no sleep.
  - At `PromptAmbiguous` it opens a `notify` watch (inotify) on the native transcript root, filtered to the session's `.jsonl` file. It checks once right after the watch opens, then on each file event. Each check takes the dispatch gate only for the promotion (`promote_ambiguous`, then `settle`).
- **Meta Configure** (meta-signal-flow 6.0.0):
  - `Configure` persists the socket paths and `RuntimeConfiguration` in one atomic commit.
  - `Configured` answers with the whole stored Configuration. `DefaultConfiguration::configuration()` fills the new fields.
  - The socket record is now a two-String struct, byte-identical to the former archive (there is a test for this), so existing stores open.
  - `flow-meta` takes `Configure.{ … }` as one inline datom. The two-argument `configure` word command is gone.
  - Left in place, as asked: the `DeploymentOverrides` `FLOW_*` exception. Also left: `Activation::NexusRestartRequired`, because the adapters read the configuration at open.
- **CLI:** `flow` prints every frame of an `Observe` until EOF. `LaunchStatus.<id>`, `Observe.Launch.<id>` and `Replace.{…}` parse (there is a test for each).

## Tests

- Before, at 972d8d2: 69 passed.
- After, at 28a78d2: 85 passed (6 flow, 3 flow-meta, 74 flow-nexus lib, 1 main, 1 default_start).
- `cargo clippy --all-targets -D warnings`: clean. `rustfmt` is clean on the files I touched. composition.rs and herdr/launch.rs are not rustfmt-clean on main; I left them alone.
- New fixtures in `crates/flow-nexus/src/lib.rs`:
  - `replace_stops_the_predecessor_before_the_successor_is_routable`:
    - While the successor's receipt is unseen: the predecessor is routable, the successor is not, and Send to the successor is refused.
    - After the receipt: `Replaced`. List shows fac697 Stopped and 908786 Active. ResolveRecipient on fac697 is refused, and Send to it answers `FlowStopped`.
    - Exactly one `pane close w1:p3` call. A repeated Replace answers the same outcome and closes nothing.
  - `a_refused_reap_leaves_neither_flow_routable_until_it_is_retried`: the answer is `ReapRefused.CloseRefused` and neither flow routes. After a retry, the result is `Replaced`.
  - `replace_refuses_an_absent_unknown_or_stopped_predecessor`: no Herdr call is made and no LaunchStatus entry is created.
  - `launch_status_answers_pending_and_every_outcome_once`: covers Unknown, Pending, Started, StartRejected (and that it is not relaunched), and ReplaceRejected.LaunchRefused with the predecessor still Active. Replaced is covered by the first fixture.
  - `a_launch_observer_receives_each_phase_once_and_the_outcome_last`:
    - Over a real socket, the observer receives Reserved, NativeLaunchIntentRecorded, NativeBound, RegistrationAcknowledged, PromptIntentRecorded and PromptAmbiguous, each exactly once.
    - Only a transcript write then yields `Started`, followed by EOF. No Start is sent and no `agent prompt` call is made.
    - A late observer gets exactly one `Started` frame.
- Flakiness: an ETXTBSY ("Text file busy") race already exists between fixture shell scripts. Full lib-suite runs failed 1 time in 30 at baseline and 3 times in 30 on the branch, in older fixtures and codex tests. My new tests alone passed 15 times out of 15.
- **Nix was not built.** `nix build .#default` could not run: local builds are disabled (`max-jobs = 0`) and the remote builder prometheus.goldragon.criome timed out. Cargo.lock gained `notify` 8.2.0 and `inotify`; crane vendors them from the lock.

## Choices a reviewer may overturn

- A predecessor whose pane is absent from the Herdr snapshot counts as `ReapRefused.RouteUnavailable`, not as already reaped. This follows the contract strictly, but a crashed predecessor leaves its successor held until someone intervenes.
- A successor is held because a `Replacement` record without a `Replaced` outcome points at it; this avoids a flow-record schema change. The check is a scan of the replacements table on every ResolveRecipient and Send.
- A launch that settled before 0.9.0 has no stored outcome, so LaunchStatus answers `LaunchPending` at its last phase.
- If an observer's client disconnects, its thread lingers until that launch's next change or outcome.
- I used an in-process Condvar rather than sema-engine `subscribe`. sema-engine subscriptions persist their registrations and have no unsubscribe.

## Lock

Orchestrate lock 6382 on the clone path, released.

## Sources

- /home/li/primary/flows/38de5b/receipts/signal-flow-4.0.0.md
- /home/li/primary/flows/38de5b/receipts/meta-signal-flow-6.0.0.md
- /home/li/primary/flows/38de5b/reports/audit-flow.md (G8, G9)
- LiGoldragon/flow 972d8d2, 8f8a71a, 28a78d2
