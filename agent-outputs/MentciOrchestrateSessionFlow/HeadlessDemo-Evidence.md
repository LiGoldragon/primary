# Headless Claude via Mentci — Proof-of-Concept Evidence

Task: prove, with a minimal real runnable demo, that a prompt drives a HEADLESS
`claude` run (no terminal-cell TUI, no attached terminal), that its output/events
surface through Mentci's view, and that the session is resumable with a follow-up
prompt while the harness is free to tear down between turns. Self-healing resume
on a "session gone" error is part of the proof.

## Verdict

Headless works end-to-end and is surfaced through Mentci's actual render path.
All six build points plus self-heal were exercised against real `claude`
v2.1.198 with a real subscription. Continuity and self-heal were reproduced with
the final binary.

The one honest caveat is about how much "Mentci's view" is today: see
"What is genuinely surfaced" below. The render path used IS Mentci's real
`RenderNota` projection (the same code the egui shell paints); what is NOT
exercised is a GUI window or a purpose-built Claude-session pane, because neither
exists yet.

## Confirmed headless invocation (`claude` 2.1.198)

Fresh turn (headless, streamed JSON events, our own session-id):

```
claude -p "<prompt>" --session-id <uuid> \
  --output-format stream-json --verbose --model haiku --allowedTools ""
```

Resume turn (continue the same session after full process teardown):

```
claude -p "<prompt>" --resume <session-id> \
  --output-format stream-json --verbose --model haiku --allowedTools ""
```

Verified facts against the real binary:

- `-p/--print` is headless (no TUI). `--output-format stream-json` requires
  `--print` and (in practice) `--verbose`; it emits one JSON object per line:
  `system/init`, `assistant`, ... and a final `{"type":"result", ...}` line.
- The final `result` line carries `"session_id"` and `"result"` (the assistant
  text). On a fresh turn `--session-id <uuid>` lets us choose and pre-track the
  id; it is echoed back in the result.
- Resume is CWD/PROJECT-SCOPED. `claude --resume <id>` only finds the session
  when run from the same working directory it was created in. Resuming a valid
  id from a different cwd yields "No conversation found with session ID: <id>".
  This is why the demo uses a stable per-lane sandbox directory.
- Not-found signalling: resuming an unknown id prints
  `No conversation found with session ID: <id>` on stderr AND emits a `result`
  line with `"subtype":"error_during_execution"`, `"is_error":true`,
  `"errors":[...]`. IMPORTANT: the process still exits 0, so not-found must be
  detected from the JSON/stderr, not the exit code.
- Headless `-p` runs write the normal transcript to
  `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`; a resume APPENDS to the
  same session file. So the harness `ClaudeArtifactObserver` (built for the
  terminal-cell proof) observes headless sessions unchanged, and sees both turns
  in one file.

## What landed (where)

- Repo: `LiGoldragon/mentci`, branch/worktree `claude-artifact-session-integration`
  at `/home/li/wt/github.com/LiGoldragon/mentci/claude-artifact-session-integration`.
- Commit `7a0c8e44c4b5` "mentci: headless Claude session demo bin ..." — pushed to
  `origin` (confirmed via `gh api repos/LiGoldragon/mentci/commits/7a0c8e44c4b5`).
- New file: `src/bin/mentci-headless-session-demo.rs` (the whole demo).
- `Cargo.toml`: added `serde_json = "1"` (already present in `Cargo.lock`, one-line
  lock delta) for disciplined stream-json parsing.
- Builds clean with plain `cargo build --bin mentci-headless-session-demo` (no
  `terminal-cell-runtime` feature — headless needs no PTY). No warnings.

The demo reuses existing plumbing: `harness::ClaudeArtifactObserver` (transcript
observation) and `mentci_lib::{RenderNota, RenderOrigin}` (the view projection).
mentci already depended on both crates.

## How the six build points are satisfied

1. Headless invocation — confirmed above against the real binary.
2. Prompt entry point — the `submit <lane> "<prompt>"` subcommand is the thin
   driver (Mentci has no real `SubmitPrompt` request surface yet; that is the
   deferred preflight/daemon work). Each `submit` is a separate OS process.
3. Launch headless + capture response + session-id — `HeadlessRun::execute`
   spawns `claude`, `StreamJsonEvents` parses the stream, the `result` line
   yields response text + session-id.
4. Surface through Mentci's view — the turn is folded into a `ClaudeTurnObservation`
   (a `NotaEncode` record) and rendered with `observation.render_nota(RenderOrigin::Event)`,
   printing the exact `RenderedObject` block a Mentci shell would paint.
5. Resume — a second `submit` for the same lane (a NEW process; the "harness"
   fully tore down) reads the tracked session-id and runs `--resume`.
6. Track the session-id — `SessionTracker` is a one-line-per-lane TSV file
   (`<base>/session-tracker.tsv`), the minimal stand-in for the orchestrate
   session store.

Self-heal: if the tracked id is one `claude` no longer knows,
`HeadlessRun::execute_with_self_heal` detects the not-found result, mints a fresh
session, re-runs the same prompt, and updates the tracker.

## Reproduce

Preconditions: logged-in `claude` v2.1.198 (real subscription). Guarded against
`/home/li/primary`; runs in a temp per-lane sandbox.

```
cd /home/li/wt/github.com/LiGoldragon/mentci/claude-artifact-session-integration
cargo build --bin mentci-headless-session-demo
export MENTCI_HEADLESS_DEMO_BASE=/tmp/mentci-headless-demo
BIN=./target/debug/mentci-headless-session-demo

# Turn 1 (fresh) — process A, seeds a codeword
"$BIN" submit topic "Remember this secret codeword for later: OBSIDIAN. Reply with only the single word ACKNOWLEDGED."

# Turn 2 (resume) — process B; the harness (process A) is long gone.
# Recalls the codeword from turn 1 => continuity across a torn-down harness.
"$BIN" submit topic "What was the secret codeword I gave you earlier? Reply with only that one word."

# Self-heal — poison the tracker with an id claude never saw, then submit again.
sed -i 's/^topic\t.*/topic\t00000000-0000-4000-8000-000000000000/' "$MENTCI_HEADLESS_DEMO_BASE/session-tracker.tsv"
"$BIN" submit topic "Reply with only the single word HEALED."
```

Guard proof (must refuse, create nothing):

```
MENTCI_HEADLESS_DEMO_BASE=/home/li/primary/x ./target/debug/mentci-headless-session-demo submit g "hi"
# => MentciHeadlessSessionDemoBlocked refused: sandbox ".../lane-g" is inside the primary workspace /home/li/primary ; exit 2 ; no dir created
```

## Observed real output (final binary, canonical run)

Turn 1 (fresh), Mentci view block — fields are
`(lane session plan model stop_end_turn streamed_events tool_calls status_transitions transcript response)`:

```
plan      : fresh (session f27acd22-1013-48d8-987c-99eeff218faa)
---- MENTCI VIEW (event) ----
(topic f27acd22-1013-48d8-987c-99eeff218faa fresh claude-haiku-4-5-20251001 True 10 0 6 .../f27acd22-....jsonl ACKNOWLEDGED)
```

Turn 2 (resume, separate process) — same session-id, recalls OBSIDIAN, and the
observer's status-transition count grew 6 -> 12 as it now sees both turns:

```
plan      : resume (session f27acd22-1013-48d8-987c-99eeff218faa)
---- MENTCI VIEW (event) ----
(topic f27acd22-1013-48d8-987c-99eeff218faa resume claude-haiku-4-5-20251001 True 9 0 12 .../f27acd22-....jsonl OBSIDIAN)
```

Self-heal — bogus tracked id, re-resumed fresh, tracker updated:

```
plan      : resume (session 00000000-0000-4000-8000-000000000000)
self-heal: tracked session 00000000-0000-4000-8000-000000000000 is gone (claude reported "No conversation found with session ID"); re-resuming as a fresh session
---- MENTCI VIEW (event) ----
(topic 5b532291-52c3-43b3-b91b-e3449b2b063d self-healed-fresh claude-haiku-4-5-20251001 True 9 0 6 .../5b532291-....jsonl HEALED)
```

## What is genuinely surfaced through Mentci vs. still raw stdout

This is the finding the psyche's headless decision hangs on.

- Mentci's "view" today is exactly one thing: `mentci_lib::RenderNota`, a blanket
  impl over any `NotaEncode` object producing `RenderedObject{origin, body:<NOTA>}`.
  The egui shell (`mentci-egui`) only PAINTS that `body` string; its
  `src/render/canvas/` is empty (no purpose-built pane). So "render through
  Mentci" == "project the typed object to its NOTA block and display it." The
  demo does exactly that with the real trait, printing the same block the GUI
  would paint. This is genuinely through Mentci's view, not a hand-rolled format.
- What the psyche SEES via Mentci in the demo: lane, session-id, fresh/resume/
  self-healed plan, model, end-turn stop, streamed-event count, tool-call count,
  observer status-transition count, transcript path, and the assistant response
  text. That is "everything you'd want to see" for a turn-level view.
- Gaps (does NOT hold as "Mentci shows everything," precisely):
  1. No live/streaming view — the block is rendered once per completed turn, not
     token-by-token. Live streaming would need a subscriber rendering
     `stream-json`/observer deltas as they arrive (design §6 step 8's
     `WatchHarnessTranscript`), which is not built.
  2. No egui window in this run — rendering is to stdout. The GUI shell needs a
     display; the render CONTENT is identical, but pixels were not painted here.
  3. No dedicated `ClaudeSessionObservation` contract type — the design's §2d
     typed surface that Mentci would ideally render is deferred; the demo renders
     a local `NotaEncode` observation record instead.
  4. The assistant response text comes from the `result` line (parsed with
     serde_json), not from the harness observer — the observer exposes
     structured metadata (session-id, model, stop reason, tool/status counts)
     but has no public getter for assistant text. Worth a small observer
     addition later if the view should source text purely from the transcript.

Net: the render PATH is real and shared; the "view" it feeds is a per-turn NOTA
block, not yet a live GUI transcript. Nothing here blocks the headless direction —
headless is fully proven; the remaining work is view richness (streaming, a pane,
the typed observation contract), which is downstream UI work, not a headless
feasibility question.

## Blockers / follow-ups (provisional recommendations)

- None blocking the concept. Headless + resume + self-heal are proven real.
- To make "Mentci shows everything live": build the streaming subscriber
  (design §6 step 8 `WatchHarnessTranscript`) and render observer deltas as they
  arrive; add the `ClaudeSessionObservation` contract (design §2d) as the object
  rendered; optionally add a `RecoveredTurn` assistant-text getter to the harness
  observer so text is sourced from the transcript, not the `result` line.
- The demo's `SessionTracker` (TSV) is deliberately minimal; the real store is
  orchestrate's session store (design §3), deferred.

## Files / commands consulted

- `harness/src/claude.rs` (ClaudeArtifactObserver / transcript recovery).
- `mentci-lib/src/render.rs`, `src/event.rs`, `src/lib.rs` (RenderNota view path).
- `mentci-egui/src/app.rs`, `src/render/` (confirmed the shell only paints the
  rendered NOTA body; canvas empty).
- `mentci/src/bin/mentci-claude-proof-test.rs` (reused the /home/li/primary guard
  pattern and the observer usage; the OLD path drives a terminal-cell PTY).
- `Design-SessionFlowSpec.md` §6 (Mentci renders the harness transcript
  observation; the locked design still drove terminal-cell — this demo proves the
  headless alternative).
- Real `claude --help` and live trial runs for flag verification.
