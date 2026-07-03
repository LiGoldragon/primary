# Mentci Live Session-View Window — Implementation Evidence

Bead: **primary-og38.5** — the payoff window. Role: general code implementer.

## Task and scope

Build a real egui window in `mentci-egui` that renders a Claude session's turns
**live** by consuming the push-based `ClaudeSessionObservation` subscription that
landed in `harness` main @ `fbb7d8cd` (the `ClaudeSessionObservation`
`HarnessStreamEvent` variant on `HarnessTranscriptStream`; contract in
`signal-harness` 0.3.0 @ `9f989d24`). Mentci stays the VIEW — no provider/mapping
logic re-enters it. Subscribe once, take the connect snapshot, then park on the
receiver (no polling). Render the turn fields; show `accumulated_context` as
`unknown / pending` (deferred, og38.1); don't foreclose multi-window.

## What was built and where it landed

Repo: `LiGoldragon/mentci-egui`. Branch: **`og38-live-session-view`** @
**`74bfcf10`** (pushed to origin). Worktree:
`/home/li/wt/github.com/LiGoldragon/mentci-egui/live-session-view` (jj workspace
`live-session-view` off `main` 8f9de29f).

New/changed files:

- `src/render/canvas/turn_row.rs` — `ObservedTurn`: holds the pushed
  `ClaudeSessionObservation` and projects its fields (response, model, launch
  provenance Fresh/Resumed/SelfHealed, end-of-turn, streamed-event / tool-call /
  status-transition counts, lifecycle, transcript path, session id, last
  activity). `accumulated_context_label()` returns `unknown / pending` when
  `None` and never fabricates a number.
- `src/render/canvas/mod.rs` — `SessionCanvas` (the pane): folds `SessionDelivery`
  events into view state and paints the status header + turn cards. Depends only
  on the `signal-harness` contract vocabulary (`HarnessStreamEvent`,
  `ClaudeSessionObservation`, `HarnessTranscriptSnapshot`), never the harness
  runtime.
- `src/render/session_stream.rs` — `SessionStreamSubscription`: the NO-POLL
  consumer. `open()` sends one `OpenTranscriptSubscription` (channel sink) and
  keeps the reply's token + connect snapshot; `next_delivery()` / `run()` park on
  `UnboundedReceiver::recv().await` and repaint on each push. The `harness`
  runtime type `TranscriptDeliveryEvent` is mapped to the view's `SessionDelivery`
  in one `From` impl here — the only place the runtime touches the view.
- `src/render/session_window.rs` — `SessionWindow` (one canvas + one
  subscription; self-contained per-window state) and `SessionViewApp`
  (`eframe::App` hosting a `Vec<SessionWindow>`; one today). No
  `request_repaint_after` — repaints are push-driven via `ctx.request_repaint()`.
- `src/bin/mentci-egui-session-window-demo.rs` — the psyche's launch command
  (`[[bin]]`). Opens the window subscription BEFORE any turn runs, then runs real
  headless `claude` turns (first Fresh, later Resumed), projects each via
  `harness::ObservedClaudeTurn`, and pushes it. Guards `/home/li/primary`.
- `src/render/mod.rs`, `src/lib.rs` (`pub mod render;`), `src/error.rs`
  (`SessionSubscription` variant), `Cargo.toml` (harness/signal-harness/kameo/
  serde_json deps + kameo patch; tokio `sync`,`macros`).
- `tests/session_canvas_render.rs` — the render witness (below).

`ARCHITECTURE.md` was NOT touched (docs lane owns it; the stale doc on the
`claude-artifact-session-integration` branch was not propagated).

## Render evidence — what is machine-asserted

`tests/session_canvas_render.rs` (`#[tokio::test]`):

1. Spawns the REAL producer plane (`harness::TranscriptSubscriptionManager` +
   `TranscriptDeltaPublisher`).
2. The window's `SessionStreamSubscription::open` subscribes once and takes the
   connect snapshot. Asserts the pane has **0 turns** before any push (no-poll
   witness: a turn appears only from a producer push).
3. The producer PUSHES a realistically-shaped `ClaudeSessionObservation` (the
   same fixture shape the harness witness uses: response `FINAL_MARKER done`,
   model `claude-3-5-haiku-latest`, launch Fresh, 9/2/4 counts, lifecycle
   Completed, `accumulated_context: None`).
4. The consumer receives it via `recv().await` into the canvas; asserts 1 turn.
5. **Real render:** the pane is painted headlessly through egui (`Context::run`),
   and the pushed observation's content is read BACK out of the paint output —
   the laid-out text galleys (`Shape::Text`) egui produced. Asserts the drawn
   text contains the response, model, `fresh`, `completed`, `unknown / pending`,
   the transcript path, session id, `reached`, and `streamed events: 9` /
   `tool calls: 2` / `status transitions: 4`; and asserts the deferred context is
   NOT synthesized to a token count.

Result: **PASS** (`test result: ok. 1 passed`). Compiled and run against the
exact target revs: `signal-harness v0.3.0 #9f989d24`, `harness v0.1.0 #fbb7d8cd`,
`kameo v0.20.0 #f491b45d`.

Verification method note: the render test was built/run in an isolated,
conflict-free crate carrying only the harness-contract stack (harness,
signal-harness, kameo, egui, eframe, tokio; lib named `mentci_egui`) with the
same `src/render` source and the same test — because the full `mentci-egui` crate
does not currently resolve (see blocker). This is a genuine machine assertion of
the same source that is committed to the branch, not a hardcoded string.

Reproduce the isolated verification: copy `src/render`, `tests/
session_canvas_render.rs`, and a minimal `error.rs` (`SessionSubscription`
variant only) into a crate whose `[dependencies]` are harness + signal-harness +
kameo (git main, `[patch.crates-io] kameo`) + egui `0.27` + eframe `0.27`
(default-features=false, wayland/x11/glow/default_fonts) + tokio
(rt-multi-thread,macros,sync) + thiserror, dev-dep signal-persona; `[lib] name =
"mentci_egui"`. Then `nix develop --command cargo test --test
session_canvas_render` from a mentci-egui devshell.

## The psyche's launch command (needs a display + `claude` CLI + network)

From the mentci-egui devshell (which sets `LD_LIBRARY_PATH` for the dlopen'd
wayland/xkb libs), once the crate builds (see blocker):

```sh
cd <mentci-egui worktree>
nix develop --command cargo run --bin mentci-egui-session-window-demo -- \
  demo-session "say FINAL_MARKER then stop" "now say it again"
```

The window opens FIRST (subscription open before any turn — there is no replay on
connect), then each headless `claude` turn is pushed and appears live: turn 1
Fresh, turn 2 Resumed. It refuses any sandbox under `/home/li/primary`. Model
defaults to `haiku`; override with `--model <alias>`.

This step is NOT machine-verified here — it needs the psyche's display and the
`claude` CLI/network. Everything up to the paint is machine-verified by the
render witness above.

## Push-not-pull confirmation (consumer side)

The consumer's only wait is `UnboundedReceiver::recv().await`
(`SessionStreamSubscription::next_delivery` / `run`). There is no `sleep`, no
interval, no ticker, and no "what is it now?" re-query — the connect snapshot
seeds the view and deltas follow on the same stream. The eframe `update` has no
`request_repaint_after`; repaints happen only when the pump calls
`ctx.request_repaint()` on a push. The render witness encodes the no-poll
property: the pane has 0 turns until the producer pushes one.

## Blocker for the auditor / psyche

**Buildable in-tree landing in `mentci-egui` is blocked** (tracked:
**primary-sh4e**, linked as blocked-by of og38.5). The window code is complete
and isolated-verified; it is committed on the feature branch pending integration.

Cause: `signal-harness` 0.3.0 (consumed by harness `fbb7d8cd`) requires the newer
schema stack (signal-frame/schema-rust/schema/nota/signal-persona mains). The
stack is tightly coupled at main (reverting one dep re-bumps its siblings), so it
is all-or-nothing. `mentci-egui`'s current `signal-mentci` pin (`8376ee42`)
build.rs REJECTS the new schema-rust:
`Schema(OptionalVariantPayload { enum_name: "InterfaceProjection", variant_name:
"NotificationProjection" })`. Bumping the mentci-client stack (`signal-mentci`,
`mentci-lib`, `signal-criome`, `meta-signal-mentci-client`, the
`signal-mentci-client` hard rev-pin, and the `mentci`/`meta-signal-mentci`
dev-deps) forward to main then hits an upstream `signal-criome` links/version
conflict via `mentci` → `meta-signal-criome` (both `git branch=main`, but they
resolve `signal-criome` to incompatible versions; `links = "signal-criome"`
forbids two copies in one graph).

To land buildably, a workspace-integration pass must: (1) integrate the
mentci-client stack forward onto the same schema stack signal-harness 0.3.0 uses,
and (2) resolve the `signal-criome` links/version conflict upstream
(`mentci` / `meta-signal-criome` / `signal-criome` mains). Neither is fixable from
within `mentci-egui`'s manifest, and both are outside the window-implementation
scope. This is the closest the toolchain/workspace state allows without that pass.

## Follow-up requirements

- Integration pass to unblock primary-sh4e, then enable `nix flake check` on the
  branch (the render witness runs under `checks.default = craneLib.cargoTest`).
- og38.7 (live windowed proof) needs the psyche's display + the integrated build,
  then the launch command above.
- Auditor: review render module discipline (methods on data-bearing types; the
  view depends only on the contract; the one `From<TranscriptDeliveryEvent>`
  boundary) and confirm the isolated-verification method is acceptable evidence
  given the in-tree resolution blocker.
