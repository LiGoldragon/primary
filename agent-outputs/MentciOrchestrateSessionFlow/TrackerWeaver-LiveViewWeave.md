# Tracker Weave — Live Mentci GUI view of a headless Claude session's turns

## Task and scope

Weave and sequence the bead graph for the feature build: turn the proven headless
demo's per-turn NOTA render into a **live Mentci egui view** of a session's turns.
Advance tracker state from named evidence, contracts-before-consumers.

This file is the tracker-weaver deliverable. It records the graph, the sequence,
what is in the tracker-weaver lane versus what is downstream, the tracker state,
and the one design fork that needs the psyche.

## Lane boundary (important — read before executing)

This was produced by the **tracker-weaver** role. Its unconditional boundaries:
it does not audit, verify implementation, edit code or docs, or author code
commits — including via spawned build workers, since owning their commits and
verification is exactly the excluded work. So the dispatch's execution phases
(dispatch implementation workers per bead, run the audit, resolve the statusline
question by running headless code, drive the egui build to a live proof) are
**filed as beads, not executed here.** They are ready for an orchestration /
implementation lane to pick up. The graph is built so that lane can execute it
directly: each bead carries goal, done-criteria, evidence signal, doctrine, an
out-of-scope boundary, and a recommended executor with strength.

The design docs (`ARCHITECTURE.md`, `Design-SessionFlowSpec.md`) are a separate
lane's and were not touched.

## Sources consulted (read-only)

- `agent-outputs/MentciOrchestrateSessionFlow/Design-SessionFlowSpec.md` — accepted,
  audited design. Migration spine §7, flow §6 step 8, contract §2d, staleness §4b.
- `agent-outputs/MentciOrchestrateSessionFlow/HeadlessDemo-Evidence.md` — demo
  evidence; the four view gaps are named in its "What is genuinely surfaced" and
  "Blockers / follow-ups" sections. Demo bin `mentci-headless-session-demo.rs`,
  LiGoldragon/mentci commit `7a0c8e44` on branch `claude-artifact-session-integration`.
- `bd` tracker (existing graph; related umbrella `primary-iy51`).

## The bead graph (ids + sequence)

Epic: **primary-og38** — Live Mentci GUI view of a headless Claude session's turns.

| Bead | Title | Gap | Blocked by | Executor (recommended) |
|---|---|---|---|---|
| primary-og38.1 | Investigate headless statusline / context-size source | (spike) | — | scout / general-code-implementer, sonnet |
| primary-og38.2 | Assistant-text getter on harness `RecoveredTurn` | gap 1 (mechanical) | — | general-code-implementer, sonnet |
| primary-og38.3 | `ClaudeSessionObservation` contract in signal-harness | gap 2 (contract) | — | rust implementer, strong |
| primary-og38.4 | Push-based streaming transcript subscriber `WatchHarnessTranscript` | gap 3 (substantial) | .1, .2, .3 | strong rust implementer, opus |
| primary-og38.5 | Actual egui window in mentci-egui | gap 4 (substantial UI) | .3, .4 | strong rust+egui implementer, opus |
| primary-og38.6 | Audit: contract + subscriber | (audit) | .3, .4 | rust-auditor, opus |
| primary-og38.7 | Live e2e proof: egui rendering a real headless session live | (verify) | .5, .6 | general-code-implementer w/ GUI-run, strong |

Dependency shape (contracts/investigation → subscriber → egui/audit → live proof):

```
.1 spike ─┐
.2 getter ┼─→ .4 subscriber ─┬─→ .5 egui ──┐
.3 contract ┘                └─→ .6 audit ──┴─→ .7 live proof
   .3 contract ───────────────→ .5 egui
```

Verified: no cycles; ready frontier is exactly **{.1 spike, .2 getter, .3 contract}**;
consumers (.4, .5, .6, .7) correctly blocked. This is the design's migration spine
(§7 step 1 contracts → step 3 harness wiring → §6 step 8 subscriber → the view) and
the dispatch's stated order (getter + contract first, then subscriber, then egui).

## Sequencing rationale

- **Contracts before consumers.** Gap 1 getter and gap 2 `ClaudeSessionObservation`
  are roots; both feed the subscriber and the window. The contract carries the
  `accumulated-context?` field as an `Option` — its *shape* does not depend on the
  spike, only its *sourcing* does, so the contract is a root, not blocked by the spike.
- **Spike is a root and blocks the subscriber**, not the contract: the statusline /
  context-size question governs how the subscriber *wires the live figure*, per design
  §2d. It is cheap; resolve it early.
- **Subscriber before window**: the egui view sources live turns from the subscription
  (dispatch order; §6 step 8).
- **Audit witnesses the two substantial pieces** (contract + subscriber) after they are
  built (verification-after-build), and with the egui window gates the live proof.
- **Live proof is real, not mocked**: the egui window shown rendering a real headless
  claude session, building on the demo plumbing at mentci `7a0c8e44`; guard `/home/li/primary`.

## Tracker state advanced

- **Created:** epic primary-og38 + seven children primary-og38.1 … primary-og38.7;
  nine `blocks` edges wired.
- **Closed:** none. None of the four gaps are built yet; no named evidence supports
  any closure, so nothing was closed (evidence-only closure discipline).
- **Left open (all):** primary-og38 and .1–.7. The three roots are ready; the four
  consumers are blocked as intended.
- Persistence: written via `bd` into its own store (queryable via `bd show`/`bd list`/
  `bd dep`). No repository commits were authored (tracker-weaver boundary; worker-output
  carve-out from the editing-closeout rule).

## Design fork to surface to the psyche (do NOT guess — it may fork the design)

Bead **primary-og38.1** carries the open question the dispatch flagged. State it plainly
so the executing lane escalates rather than silently redesigning:

- The design (§2d, §4b) makes the Claude Code **statusline JSON payload**
  (`context_window` / `exceeds_200k_tokens`) the **primary, always-on** source of the
  context-size staleness figure — precisely because it is the only source that reports
  **mid-turn** — with `/context` injection as an **at-rest-only** fallback, and it
  **explicitly rejects** summing `message.usage` tokens out of the transcript.
- The demo proved headless works via `claude -p ... --output-format stream-json`. It is
  **unverified whether headless `-p` mode invokes a configured statusline command at all**
  (statusline is a TUI affordance; `-p` is non-interactive). If headless `-p` does **not**
  emit the statusline payload, the design's primary source is unavailable in exactly the
  mode this build uses, the rejected stream-json `usage` option comes back onto the table
  (revisiting the "don't self-calculate" call), and the `/context`-at-rest fallback may
  behave differently headless.
- **Ask:** resolve from real evidence (run headless, check for statusline emission). If it
  changes the staleness sourcing, this is a genuine fork for the psyche — surface it before
  the subscriber (og38.4) wires `accumulated_context`. It does **not** block gaps 1, 2, or
  the window; only the live-context wiring depends on it.

## Blockers / follow-ups

- No tracker blocker: all `bd` writes succeeded, no lock contention, no cycles.
- The execution of every bead (implementation, audit, live proof) and the resolution of
  the statusline spike are **downstream of this lane** and need an orchestration /
  implementation lane. This file + the graph are the pickup surface.
- Relation to `primary-iy51` ("Realize mentci as a live component") noted in the epic
  description; kept as a distinct epic rather than folded in, to keep this narrow
  live-view slice cleanly scoped.
