# 201 — Post-scan consolidation: where substance lives now

Date: 2026-05-16
Role: designer
Scope: Context-maintenance pass following the deep architecture scan. Consolidates still-load-bearing substance from earlier designer reports into one navigation surface; names retirement candidates whose substance has migrated to ARCH.

## 0. TL;DR

A deep architecture scan ran today across the Persona stack, the kernel pair, and the signal-persona contract family. The structural findings were migrated into ARCH files (Persona apex, persona-mind, persona-router, persona-message, persona-harness, persona-introspect, persona-terminal, terminal-cell, persona-system, plus 5 contract crates). Cross-cutting rule docs (`ESSENCE.md`, `skills/push-not-pull.md`) were updated with the reachability-probe clarification.

What this report holds:

- **§1** — where the substance from /176, /177, /179 now lives (it's in ARCH; reports are retire-candidates).
- **§2** — the eight cross-cutting structural moves that came out of the scan, in priority order. These are the operator/system-specialist pickup targets.
- **§3** — open questions and ratified decisions from the user, recorded for next session.
- **§4** — reports kept and why; reports recommended for retirement.

This is a **working artifact**, not a permanent doc. It retires once §2's moves land and §3's open questions resolve.

## 1. Where substance now lives

The substance of three earlier designer reports has migrated to ARCH files:

| Report | Substance migrated to | Status |
|---|---|---|
| `/176-signal-channel-macro-redesign.md` | `signal-core/ARCHITECTURE.md` §3 (channel macro grammar, validation, emission) + `signal-core/macros/` crate. | Retire candidate. |
| `/177-typed-request-shape-and-execution-semantics.md` | `signal-core/ARCHITECTURE.md` (six-root verb spine, Request/Reply shape, ExchangeFrame vs StreamingFrame, ExchangeIdentifier semantics, SubReply per-op typed sum) + `sema-engine/ARCHITECTURE.md` (CommitRequest, Subscribe initial-snapshot, delivery modes). | Retire candidate. |
| `/179-signal-core-sema-engine-lojix-readiness-audit.md` | Closed by operator/121 + OA/121. Kernel state is current: signal-core `25212c0` (proc-macro hardened, 4 compile-fail witnesses), sema-engine `d3809149` (fresh-Assert, fmt green, kernel-pinned). 9 contracts pinned green. | Retire candidate — substance is "what was wrong"; history in git log. |

The /178 engine visual reference holds value as cross-cutting orientation diagrams that don't fit a single ARCH; **keep**.

The /180 lojix daemon+CLI research is active operator/system-specialist consumer work (Waves 2–8 ongoing); **keep**.

## 2. Eight cross-cutting structural moves

The deep scan identified these. ARCH files describe the destination shape; this is the operator/system-specialist pickup order:

### Wave 1 — Per-component fixes (parallel, no cross-component coordination)

1. **Pin `persona-mind::StoreKernel` to a dedicated OS thread** (Kameo Template 2). Blocking redb/sema work moves off the shared tokio worker pool. Akka BlockingDispatcher + Erlang dirty schedulers are the precedent. ARCH: `persona-mind/ARCHITECTURE.md` §3 + §8 invariant.

2. **Spawn child-exit watcher in `DirectProcessLauncher`** (per-child task awaits `Child::wait()` and pushes `ComponentExited`). Erlang link semantics + daemontools `supervise`. ARCH: `persona/ARCHITECTURE.md` §1.7.

3. **Split `terminal-cell` into `control.sock` + `data.sock`**. Single `cell.sock` is transitional; ARCH names the destination split. ARCH: `terminal-cell/ARCHITECTURE.md` §1.

4. **Split `terminal-cell::TerminalOutputFanout` into `ViewerFanout` (real-time) + `TranscriptScriber` (decoupled)** with bounded queue + overflow-drop-oldest. Witness constraints: 1000 PTY bytes arrive at viewer in <100ms despite 50ms transcript-append; viewer attach completes in <10ms despite pending control. ARCH: `terminal-cell/ARCHITECTURE.md` §2 + §3.

5. **Materialize manager snapshot reducers** (`engine-lifecycle-snapshot`, `engine-status-snapshot`). Lazy on mutation, eager flush on shutdown, eager rebuild on startup. EventStoreDB + Akka Persistence + Kafka KTable patterns. ARCH: `persona/ARCHITECTURE.md` §1.7. Bead `primary-devn`.

### Wave 2 — Contract changes (designer drafts, operator implements)

6. **Close `Unknown` variants in wire enums**:
   - `signal-persona-router`: `RouterDeliveryStatus`, `RouterChannelStatus`
   - `signal-persona-introspect`: `DeliveryTraceStatus`
   - `signal-persona-mind`: extract `UnknownRoleName { role: String }` to closed `RoleName` enum or `RoleNotDefined` (dynamic-roles case)

   Forward-compat is coordinated schema evolution (major version bump + simultaneous consumer upgrade), not silent fallback. ARCHs of those three crates already name closed-enum constraints.

7. **Retire env-var fallback paths** in production daemons. Production binaries read configuration via `ConfigurationSource::from_argv()` only (per the nota-config library design). Test shims may opt in via the explicit `from_argv_with_test_env_fallback(named_env_var)` method. ARCH: `persona-message/ARCHITECTURE.md` §2 + invariants.

### Wave 3 — Subscription push + Path A uniform (cross-cutting)

8. **Implement subscription push delivery + adopt Path A uniformly**:
   - **persona-mind**: split `SubscriptionSupervisor` into `SubscriptionManager` + per-subscription `StreamingReplyHandler` + post-commit `SubscriptionDeltaPublisher`. Consumer-driven `SubscriptionDemand(n)` backpressure per Reactive Streams.
   - **persona-harness**: design observation push primitive in `signal-persona-harness`; harness emits typed transcript + worker-lifecycle deltas.
   - **persona-router**: serve `signal-persona-router` observation queries (Summary, MessageTrace, ChannelState) with streaming reply for channel-state deltas.
   - **persona-introspect**: wire `ManagerClient`/`RouterClient`/`TerminalClient` to make actual Signal calls (currently scaffolds returning hardcoded `Unknown`).
   - **Path A uniform**: `MindReply::SubscriptionRetracted`, `SystemReply::SubscriptionRetracted`, `HarnessReply::SubscriptionRetracted` as reply-side close events (replacing request-side `SubscriptionRetraction` / `FocusUnsubscription`).

   ARCHs of all five contracts name Path A discipline. Implementation is operator lane.

### Wave 4 — Choreography policy engine

9. **Build `ChoreographyAdjudicator` actor** inside `persona-mind`. Stateful actor owning `policy: ChoreographyPolicy`, `grants: HashMap<ChannelId, ChannelGrant>`, `log: Vec<AdjudicationLogEntry>`. Handles all 7 choreography request variants (currently routed to `unimplemented()`). Akka Typed behavior-based state machine + Erlang `gen_statem` are the references. ARCH: `persona-mind/ARCHITECTURE.md` §3 + §8 invariant. Beads `primary-hj4`, `primary-hj4.1`.

## 3. Open questions + ratified decisions

### Ratified by user

- **Polling for reachability is the carve-out**: cross-process socket-bind polling is permitted (no push primitive exists for "another process bound a Unix socket on a path I named"). The bounded retry shape stays. Documented in `skills/push-not-pull.md` §"Reachability probes — bounded retry across process boundaries" and `ESSENCE.md` §"Polling is forbidden" §"Named carve-outs". If a future component emits a `SocketBound` push, prefer that.

- **Build `ChoreographyAdjudicator` as new actor** in persona-mind (Wave 4, Move 9).

- **Subscription streaming surface**: within the streaming reply envelope (not a separate multiplex). Frame layer already supports `StreamingFrameBody::SubscriptionEvent`.

- **`HarnessKind::Fixture` variant** lands on next `signal-persona-harness` major bump.

- **`ReplySupervisor` → `ReplyShaper` rename** in persona-mind is acceptable; low priority; bundle with any mind refactor.

- **persona-system unpause triggered by real consumer**, not by schedule.

### Still pending

- **`MindAdjudicationOutbox` durability**: ARCH names it transitional. Destination is live router→mind Signal transport. No specific timing yet.

- **`ChannelTriple` typed migration** (from `ActorId` + `ChannelKind::DirectMessage` to `ChannelEndpoint` + `ChannelMessageKind`): named as destination in `persona-router/ARCHITECTURE.md`; gated on `signal-persona-mind`'s channel endpoint contract stabilizing.

- **Schema evolution discipline for sema-engine subscriptions**: how do durable subscription filters survive schema bumps. Not yet designed.

## 4. Reports kept + retirement candidates

### Keep (still load-bearing in their own right)

| Report | Why kept |
|---|---|
| `/139-wifi-pki-migration-designer-response.md` | Active horizon-rs / clavifaber arc; not Persona-engine scope |
| `/150-signal-network-design-draft.md` | Future cross-engine federation work; substance hasn't migrated |
| `/178-engine-visual-reference.md` | Cross-cutting orientation diagrams; useful for new agents reading the engine cold |
| `/180-lojix-daemon-cli-implementation-research.md` | Waves 2–8 active operator/system-specialist consumer work |

### Retirement candidates (substance migrated to ARCH)

| Report | Why retire-candidate |
|---|---|
| `/176-signal-channel-macro-redesign.md` | signal-core/ARCH §3 + macros/ crate carry the substance |
| `/177-typed-request-shape-and-execution-semantics.md` | signal-core/ARCH + sema-engine/ARCH carry the substance |
| `/179-signal-core-sema-engine-lojix-readiness-audit.md` | Closed (operator/121 + OA/121 landed the fixes); "what was wrong" is git-log history |

**Recommendation**: delete these three when you next prune. Their substance is canonical in ARCH; the reports are working-surface that has done its job.

## 5. Next-session targets

For designer:
- Watch for operator/system-specialist work on Wave 1 moves (Template 2 StoreKernel, child-exit watcher, terminal-cell socket split, snapshot reducers). When they land, add Update notes to relevant ARCHs marking "destination achieved."
- If a `signal-persona-harness` observation channel contract draft is needed (Wave 3 prerequisite), designer leads.
- Watch for `nota-config` crate scaffolding (per /183 substance, now in `persona-message/ARCHITECTURE.md` invariants).

For operator:
- Wave 1 moves are bounded per-repo; can parallel.
- Wave 2 contract changes (close Unknown, retire env-var fallback) need coordinated upgrade.

For system-specialist:
- Lojix-related Waves per `/180`.
- The new `nota-config` crate when designer + operator agree on the seed.

## 6. Discipline notes

- **No report references in ARCH files.** Every claim in this report's §1 corresponds to substance already inlined into the named ARCH. Future readers should find the rule/constraint there, not here.
- **Reachability-probe clarification** in `skills/push-not-pull.md` is the canonical home; this report only summarizes for next-session context.
- **/201 itself retires** once Wave 1 moves land and the eight structural moves close. At that point, designer's `reports/` subdir holds only what's still genuinely working-surface.

## 7. See also

- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` — apex engine architecture (snapshot reducers, child-exit watcher, capability envelope, reachability rationale)
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` — ChoreographyAdjudicator, subscription push split, Path A
- `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md` — control/data plane split, OutputFanout split
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` — wire kernel; six-root verb spine; channel macro
- `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md` — database engine library
- `/git/github.com/LiGoldragon/signal-persona-mind/ARCHITECTURE.md` — Path A SubscriptionRetracted; choreography vocabulary
- `/git/github.com/LiGoldragon/signal-persona-router/ARCHITECTURE.md` — closed-enum discipline
- `/git/github.com/LiGoldragon/signal-persona-introspect/ARCHITECTURE.md` — same; sema-engine integration landed
- `/git/github.com/LiGoldragon/signal-persona-harness/ARCHITECTURE.md` — observation channel; HarnessKind 4 variants
- `/git/github.com/LiGoldragon/signal-persona-system/ARCHITECTURE.md` — Path A; paused-state banner
- `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md` — MindAdjudicationOutbox transitional; ChannelTriple migration
- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md` — typed-config invariants
- `/git/github.com/LiGoldragon/persona-harness/ARCHITECTURE.md` — observation push; HarnessKind Fixture
- `/git/github.com/LiGoldragon/persona-introspect/ARCHITECTURE.md` — peer-query destination
- `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md` — control plane split
- `/git/github.com/LiGoldragon/persona-system/ARCHITECTURE.md` — paused-state banner
- `/home/li/primary/skills/push-not-pull.md` §"Reachability probes — bounded retry across process boundaries"
- `/home/li/primary/ESSENCE.md` §"Polling is forbidden" §"Named carve-outs"
