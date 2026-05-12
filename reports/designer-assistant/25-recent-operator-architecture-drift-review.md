# 25 - Recent Operator Architecture Drift Review

*Designer-assistant report, 2026-05-12. Scope: recent operator and
operator-assistant implementation work across the Persona stack, checked
against `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` and the
corresponding component `ARCHITECTURE.md` files. This report favors the
current architecture over older report history.*

---

## 0 - Short Read

The operator work is moving in the right direction: `persona` now has a
daemon-first CLI, manager/store actors, typed engine layout, resolved component
commands, a typed engine-event store, and an uncommitted `DirectProcessLauncher`
actor. The adjacent repos have also moved toward the current decisions:
`persona-message` dropped local proof assertions, `persona-router` has channel
grant machinery, `terminal-cell` accepts `signal-persona-terminal` control
frames, and `signal-persona-auth` now carries provenance vocabulary rather than
Persona-local proof material.

The problems are mostly truth-surface problems. A few docs and tests now claim
more than the implementation proves, and a few old architecture surfaces still
point agents toward retired designs.

Most important findings:

1. `persona`'s new direct-process launcher is a good primitive, but it is not
   yet wired into `EngineManager` or `persona-daemon`; the new tests prove a
   standalone launcher, not daemon-owned engine supervision.
2. `signal-persona` is the stalest active contract: its architecture still
   describes `ConnectionClass` / `EngineRoute` manager behavior, while its code
   carries open `ComponentName(String)` plus `ComponentKind::Message` instead of
   the closed `MessageProxy` vocabulary now used in `signal-persona-auth` and
   `persona`.
3. The typed engine event log landed, but its NOTA projection drops the event
   payload that the human explicitly wanted to see, and `ComponentOperation`
   is still a string bag.
4. The old system-owned input-buffer model is still live in
   `persona-system`, `signal-persona-system`, and `signal-persona-harness`
   docs/comments, even though the current architecture says prompt cleanliness
   is terminal-owned.
5. `persona-router` currently hard-codes inbound Signal messages as
   `ActorId("operator")` with `MessageOrigin::External(ConnectionClass::Owner)`;
   that can make provenance and channel-policy tests lie.
6. `persona-terminal` and `terminal-cell` both now hold prompt-pattern and
   input-gate Signal control state. That may be transitional, but production
   needs one explicit owner split.
7. `persona-harness` has a `Human` delivery endpoint that reports success
   without touching a terminal transport. That is acceptable only if it is
   named and fenced as a fixture path.

---

## 1 - Review Scope

Recent work read:

| Surface | Evidence |
|---|---|
| Meta architecture | `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` |
| Operator state report | `reports/operator/112-persona-engine-work-state.md` |
| Operator-assistant state report | `reports/operator-assistant/107-current-persona-implementation-state-survey.md` |
| Supervision design | `reports/designer/132-persona-engine-supervision-shape.md` |
| Skeleton/event-log handoff | `reports/designer-assistant/24-persona-daemon-skeletons-and-engine-event-log.md` |
| Designer event-log review | `reports/designer/134-component-skeletons-and-engine-event-log-review.md` |
| Current uncommitted operator work | `/git/github.com/LiGoldragon/persona/src/direct_process.rs`, `/git/github.com/LiGoldragon/persona/tests/direct_process.rs` |

Repos checked against their architecture files:

- `/git/github.com/LiGoldragon/persona`
- `/git/github.com/LiGoldragon/signal-persona`
- `/git/github.com/LiGoldragon/signal-persona-auth`
- `/git/github.com/LiGoldragon/persona-router`
- `/git/github.com/LiGoldragon/persona-system`
- `/git/github.com/LiGoldragon/signal-persona-system`
- `/git/github.com/LiGoldragon/persona-harness`
- `/git/github.com/LiGoldragon/signal-persona-harness`
- `/git/github.com/LiGoldragon/persona-terminal`
- `/git/github.com/LiGoldragon/terminal-cell`
- `/git/github.com/LiGoldragon/signal-persona-terminal`
- `/git/github.com/LiGoldragon/persona-message`
- `/git/github.com/LiGoldragon/persona-mind`

---

## 2 - Findings

### 2.1 - Direct-process launcher is a primitive, not supervision yet

Current operator work in `/git/github.com/LiGoldragon/persona` adds
`src/direct_process.rs` and `tests/direct_process.rs`. The shape is good:
`DirectProcessLauncher` is a real data-bearing Kameo actor with a
`HashMap<EngineComponent, RunningChild>`, launch/stop messages, process-group
setup through `setpgid`, and SIGTERM/SIGKILL cleanup.

The mismatch is in what the new checks prove.

Evidence:

- `/git/github.com/LiGoldragon/persona/src/manager.rs` still handles
  `ComponentStartup` / `ComponentShutdown` by changing `EngineState` and
  persisting status. It does not hold or call `DirectProcessLauncher`.
- `/git/github.com/LiGoldragon/persona/tests/direct_process.rs` starts
  `DirectProcessLauncher` directly. The check named
  `persona-component-launcher-does-not-block-manager-mailbox` asks the launcher
  for `ReadLauncherSnapshot`; it does not ask `EngineManager` while a launcher
  operation is active.
- The check named `persona-component-launcher-reaps-process-group` launches one
  shell process. It proves the shell PID stops; it does not prove a child tree
  or process group is reaped.
- `DirectProcessLauncher::Drop` sends SIGKILL to process groups but does not
  wait for children. The explicit `StopComponentProcess` path waits; abnormal
  actor drop is not yet the reverse-order shutdown path described by the meta
  architecture.

Recommendation:

- Keep `DirectProcessLauncher`.
- Do not treat these checks as proving full daemon supervision yet.
- Next witness should wire `EngineManager` to the launcher and prove the
  manager remains responsive while launch/stop work is happening.
- Strengthen the process-group test with a command that spawns a child/grandchild
  in the same process group, then prove the whole group is gone.
- Add a reverse-order shutdown witness once a real `ComponentSupervisor` exists.

### 2.2 - `signal-persona` is stale relative to the meta architecture

`signal-persona` is supposed to be the management contract for the top-level
`persona` engine manager. Right now it is split between old architecture and
narrower source.

Evidence:

- `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md` still says the
  manager classifies incoming connections by `ConnectionClass` and mediates
  `EngineRoute` records.
- The same architecture file still lists `ConnectionClassQuery`,
  `EngineRouteRequest`, `EngineRouteApprove`, `EngineRouteReject`,
  `EngineRouteRemove`, and `EngineRouteList`.
- `/git/github.com/LiGoldragon/signal-persona/src/lib.rs` has
  `pub struct ComponentName(String)`, while
  `/git/github.com/LiGoldragon/signal-persona-auth/src/names.rs` has a closed
  `ComponentName` enum with `Mind`, `MessageProxy`, `Router`, `Terminal`,
  `Harness`, and `System`.
- `signal-persona/src/lib.rs` has `ComponentKind::Message`; `persona/src/engine.rs`
  and `signal-persona-auth` use `MessageProxy`.
- `signal-persona` has no management-surface records for the new engine event
  log, launch catalog, resolved component command view, or first-stack skeleton
  health/readiness replies.

Why this matters:

The full-topology witness will route through the top-level manager contract.
If operators build against the stale `signal-persona` architecture, they can
reintroduce the retired in-band class/route machinery or keep the component
vocabulary split.

Recommendation:

- Clean `signal-persona` before using it as the skeleton-supervision contract.
- Either reuse the closed component vocabulary from `signal-persona-auth`, or
  make `signal-persona`'s component names closed in the same way.
- Rename `Message` to `MessageProxy` unless there is a deliberate distinction.
- Remove or banner the old `ConnectionClass` / `EngineRoute` sections as
  historical.

### 2.3 - Engine event log is typed internally, but the projection is too thin

The event log direction is right. `/git/github.com/LiGoldragon/persona/src/engine_event.rs`
has typed `EngineEvent`, `EngineEventBody`, lifecycle events,
`ComponentUnimplemented`, restart events, and state-change events.

Two issues stand out.

First, `ComponentOperation` is still `struct ComponentOperation(String)`.
`reports/designer/134-component-skeletons-and-engine-event-log-review.md`
already identifies this as the key typed-boundary gap. The operation should
come from closed per-contract request-kind projections, not free text.

Second, `/git/github.com/LiGoldragon/persona/src/schema.rs` projects an
`EngineEvent` into:

```rust
pub struct EngineEventReport {
    pub sequence: u64,
    pub engine: TextEngineId,
    pub source: EngineEventSourceKind,
    pub body: EngineEventBodyKind,
}
```

That drops the component name, operation, unimplemented reason, exit code,
restart attempt, and engine phase. It cannot show the concrete fact the user
asked for: "such daemon replied to such a request and said unimplemented yet."

Recommendation:

- Keep the durable typed event log.
- Replace `ComponentOperation(String)` with closed operation identity.
- Make NOTA projection a full event projection, not only a kind projection.
  A compact view can still exist, but the default truth projection should carry
  the payload.

### 2.4 - System-owned input-buffer vocabulary is still misleading agents

The meta architecture now says prompt cleanliness and input-gate safety belong
to `persona-terminal` / `terminal-cell`, not `persona-system`. However, old
system-driven prompt gating remains in multiple places.

Evidence:

- `/git/github.com/LiGoldragon/persona-system/ARCHITECTURE.md` still lists
  prompt/input-buffer observations and says focus-state plus prompt-buffer
  state are system observations.
- `/git/github.com/LiGoldragon/persona-system/ARCHITECTURE.md` still says
  force-focus and focus-drift suppression require
  `ConnectionClass = System(persona)`.
- `/git/github.com/LiGoldragon/signal-persona-system/src/lib.rs` still exposes
  `InputBufferSubscription`, `InputBufferSnapshot`, `InputBufferObservation`,
  and `InputBufferState`.
- `/git/github.com/LiGoldragon/signal-persona-system/ARCHITECTURE.md` still
  says router consumes focus plus input-buffer state to gate message delivery.
- `/git/github.com/LiGoldragon/signal-persona-harness/src/lib.rs` says the
  router has already verified "focus not human-owned + input buffer empty"
  before `MessageDelivery`.

Recommendation:

- Remove the input-buffer relation from `signal-persona-system`, or add a very
  explicit status banner saying it is shelved and not part of the current
  injection-safety path.
- Update `persona-system` to focus-only/deferred-system authority language.
- Update `signal-persona-harness` comments so harness delivery no longer
  assumes router/system prompt gating.

### 2.5 - Router ingress currently forges provenance

`persona-router` has moved toward the current channel model, but inbound Signal
messages are still stamped too casually.

Evidence:

- `/git/github.com/LiGoldragon/persona-router/src/router.rs` reads a
  `signal-persona-message` frame and calls
  `SignalMessageInput::from_frame_with_sender(frame, ActorId::new("operator"))`.
- `SignalMessageInput::new` defaults origin to
  `MessageOrigin::External(ConnectionClass::Owner)`.

That means a message entering over the router socket is treated as owner-origin
operator traffic regardless of the actual socket path, proxy, or future ingress
context.

Why this matters:

The current trust model says local access is enforced by filesystem/socket
boundaries, while `MessageOrigin` / `ConnectionClass` are provenance and policy
inputs. Hard-coding `Owner` turns provenance into a test fixture hidden inside
production code.

Recommendation:

- Make router ingress receive `IngressContext` / `MessageOrigin` from the
  accepted socket boundary or from the message-proxy relation.
- If the current owner stamp is only a fixture, name it as a fixture-only path.
- Do not let channel authorization tests pass through hard-coded owner origin.

### 2.6 - Terminal control ownership is duplicated

`signal-persona-terminal` now has the right contract records for prompt
patterns, input gates, write injection, prompt state, and worker lifecycle.
Both consumers have started to implement them.

Evidence:

- `/git/github.com/LiGoldragon/persona-terminal/src/signal_control.rs` has a
  `TerminalSignalControl` Kameo actor with `prompt_patterns` and `signal_leases`.
- `/git/github.com/LiGoldragon/terminal-cell/src/bin/terminal-cell-daemon.rs`
  has a separate `TerminalSignalControlState` behind `Arc<Mutex<_>>` with its
  own prompt pattern and signal lease maps.
- `/git/github.com/LiGoldragon/terminal-cell/src/bin/terminal-cell-daemon.rs`
  also handles the same `RegisterPromptPattern`, `AcquireInputGate`,
  `ReleaseInputGate`, and `WriteInjection` control frames directly.

This duplication may be acceptable during transition, but production needs a
clear owner split. Otherwise agents will not know whether `persona-terminal` or
`terminal-cell` owns prompt-pattern registry state and lease state.

Recommended split:

- `terminal-cell` owns the primitive, latency-sensitive PTY/input gate and raw
  data plane.
- `persona-terminal` owns named terminal registry, policy, prompt-pattern
  lifecycle, delivery attempts, session metadata, and any durable Sema state.
- `signal-persona-terminal` frames may go to terminal-cell for primitive cell
  control, but `persona-terminal` should be the engine-facing component that
  decides when and why to do that.

Also, `protocols/active-repositories.md` lists `persona-terminal` and
`terminal-cell` but not `signal-persona-terminal`, even though the symlink
`repos/signal-persona-terminal` exists and the repo is central to this wave.
That omission should be fixed.

### 2.7 - Harness has a production-shaped fake delivery path

`persona-harness` is close to the desired direction, but one path can make
tests lie.

Evidence:

- `/git/github.com/LiGoldragon/persona-harness/src/terminal.rs` defines
  `HarnessTerminalEndpoint::Human`.
- `HarnessTerminalDelivery::deliver_text` returns a successful
  `TerminalDeliveryReceipt::human()` for that endpoint without sending bytes
  to any terminal, socket, or `signal-persona-terminal` contract.
- `/git/github.com/LiGoldragon/persona-harness/src/transcript.rs` stores raw
  `TranscriptLine(String)` with no sequence pointer shape yet.

Recommendation:

- Rename `Human` to an explicit fixture/test endpoint, or remove it from the
  production delivery type.
- Make production delivery go through the terminal contract/socket path.
- Keep raw transcript lines local; cross-component transcript fanout should be
  typed observations plus sequence pointers.

### 2.8 - Sandbox and Nix-command witnesses still have two known gaps

The sandbox runner architecture now says dedicated credential roots hidden by
`ProtectHome=tmpfs` must be exposed with `BindPaths=` or `LoadCredential=`.
The script still has the known gap:

- `/git/github.com/LiGoldragon/persona/scripts/persona-engine-sandbox` uses
  `ReadWritePaths="$credential_root"` when the credential root directory exists.

That is already tracked by the operator lane, but it remains real.

Separately, the check named `persona-component-commands-resolve-from-nix-closure`
currently uses fake paths under `/tmp/.../nix-closure/...` in
`/git/github.com/LiGoldragon/persona/tests/engine.rs`. It proves "explicit
catalog, no ambient PATH fallback." It does not prove "actual Nix-built
component commands from this flake closure."

Recommendation:

- Keep the existing test, but name its actual claim precisely.
- Add a separate Nix-level witness that the resolved catalog is generated from
  actual flake package outputs.
- Close the credential-root visibility gap before Codex/Claude live sandbox
  smokes are treated as trustworthy.

### 2.9 - Smaller consistency notes

- `/git/github.com/LiGoldragon/persona/src/engine.rs` gives `MessageProxy` a
  `message-proxy.redb` state file, while the meta architecture calls
  `persona-message` a stateless proxy. This may just be uniform layout, but it
  should be deliberate.
- `/git/github.com/LiGoldragon/persona/src/manager_store.rs` bumped manager
  schema to version 2. If any long-lived v1 manager store exists, it will need
  an intentional migration or reset story.
- `ManagerStore::engine_events` scans the global event table and filters by
  engine. Fine for the first witness, but multi-engine is load-bearing, so an
  engine-indexed event view will probably be needed.

---

## 3 - Suggested Priority

1. Fix truth surfaces before more implementation: clean or banner
   `signal-persona`, `persona-system`, `signal-persona-system`, and
   `signal-persona-harness`.
2. Tighten the `persona` event-log implementation: typed
   `ComponentOperation`, full NOTA event projection, and manager-written event
   flow.
3. Reframe the direct-process checks so they do not overclaim, then wire
   `DirectProcessLauncher` into `EngineManager` / `persona-daemon`.
4. Decide the terminal control owner split and document it in
   `persona-terminal`, `terminal-cell`, and `signal-persona-terminal`.
5. Fence or remove fixture-like production paths, especially
   `HarnessTerminalEndpoint::Human` and hard-coded router owner ingress.
6. Add `signal-persona-terminal` to `protocols/active-repositories.md`.

---

## 4 - Questions Worth User Attention

1. Should `signal-persona` be cleaned before the first full daemon-skeleton
   witness? My recommendation: yes. It is the manager contract; stale manager
   vocabulary will poison the skeleton work.
2. Should `signal-persona-system` remove input-buffer records now, or carry a
   status banner that they are shelved? My recommendation: remove if cheap;
   otherwise banner loudly before another agent implements the old path.
3. Should `HarnessTerminalEndpoint::Human` be renamed to a fixture endpoint?
   My recommendation: yes. "Human" sounds production-real, but it is currently
   a success-without-transport path.
4. For terminal control, should prompt-pattern registry state live in
   `persona-terminal` only, with terminal-cell holding only primitive active
   leases? My recommendation: yes. It preserves terminal-cell as the low-level
   PTY primitive and keeps Persona policy in `persona-terminal`.
