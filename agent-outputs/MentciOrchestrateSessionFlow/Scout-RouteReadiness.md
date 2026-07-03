# Scout — Route Readiness (Current Mentci prompt→Claude ground truth)

Task: Determine whether the CURRENT (monolithic) Mentci can take a user prompt,
route it (preflight), and launch/drive a live Claude session end-to-end today,
and what the minimal path to a testable running instance is. Read-only; no
edits, no build, no deploy, no proof run.

## Checkout Under Inspection

- Container: `/home/li/wt/github.com/LiGoldragon/mentci/` holds two jj worktrees
  and no base checkout of its own.
- Active worktree for this path: **`claude-artifact-session-integration`**
  (jj `@` empty; head commit `f96f016e` "mentci stabilize Claude artifact
  terminal proof", 2026-06-29 02:14). This is the checkout all `path:line`
  witnesses below refer to unless noted.
- Sibling worktree `criome-authorization-push` (head `f1dcbdb9`, 2026-06-28) has
  an **identical `src/lib.rs`** and the same engine files + proof binary
  (`diff` of both `lib.rs` = identical; `ls` of both `src/bin` match).
- Crate: `mentci` 0.4.1, edition 2024. All non-std deps are git remotes
  (`criome`, `harness`, `kameo`, `signal-*`, `mentci-lib`, `terminal-cell`
  optional). Feature `terminal-cell-runtime` gates the real terminal driver.
  No `flake.nix` / Nix module in the worktree (`find` empty) — plain cargo.

## Observed Facts

### A. The daemon is an approval surface, NOT a prompt router

- `ARCHITECTURE.md:1-4`: "Mentci is a first-class component daemon that hosts
  the programmable approval surface for the local criome." `Cargo.toml`
  description: "programmable human approval surface over signal-mentci."
- `daemon.rs:121-154` `handle_connection` decodes one `MentciRequest`, routes it
  to `State::apply_with_context` via a Kameo `StateOwner` actor
  (`daemon.rs:137-148`). The request variants it handles are the interface /
  criome surface only: `PushUpdate`, `ObserveInterfaceState`, `AnswerQuestion`,
  `Create/Replace/Cancel/ListInterceptPolicies`, `Fetch/AnswerParkedRequest`
  (`daemon.rs:205-244`, `client.rs:164-210`). There is **no** request variant
  for "submit a user prompt / launch a session."
- The daemon and its neighbors (`daemon.rs`, `state.rs`, `client.rs`,
  `command.rs`, `main.rs`, `bin/mentci-daemon.rs`) contain **zero references**
  to `preflight`, `harness_adapters`, `harness_sessions`, or `harness_liveness`
  (grep over those files returned only the `pub mod` lines in `lib.rs:14-18`).
  The launch engines are compiled into the crate but not wired into the daemon.

### B. Preflight routing model call is a trait seam with no production impl

- `preflight.rs:43-52` defines `trait PreflightApi { model_availability(..);
  complete(..) }`. `complete()` is the prompt-routing model call.
- `preflight.rs:335-348` `PreflightEngine::launch()` builds an `api_prompt`
  (`preflight.rs:234-250`, "Emit exactly one NOTA MentciPreflightLaunch
  record...Prompt: <user prompt>"), calls `self.api.complete()`
  (`preflight.rs:344`), then parses + validates the NOTA into
  `MentciPreflightLaunch`.
- **The only `impl PreflightApi` is `FakePreflightApi` in `tests/preflight.rs:28`**
  (grep for `impl PreflightApi` across `src/` + `tests/` = that one hit). No
  HTTP / Anthropic / `reqwest` / `ureq` / `hyper` / api-key client exists in
  `src/` (grep for those = only a comment in the proof binary). So the routing
  decision can be exercised only with a hand-fed fake; no real model is wired.

### C. The launch/drive engine IS real (and feature-gated)

- `harness_adapters.rs:51-77` `ClaudeCodeAdapter::launch` builds a real `claude`
  command. Program default `"claude"` (`harness_adapters.rs:25`); arguments
  (`harness_adapters.rs:118-135`): `--dangerously-skip-permissions --add-dir
  <scaffold> --name <lane> [--model <model>]`; working dir = jj sandbox.
  `close_request()` sends `"/exit\r"` (`:83-85`).
- `EphemeralJjRepository` (`harness_adapters.rs:810-888`) creates a real
  `jj git init --colocate` sandbox and **hard-refuses `/home/li/primary`**
  (`:879-887`, `PRIMARY_WORKSPACE` const `:21`).
- `harness_sessions.rs`: `NamedHarnessSessions<Directory, Launcher>` with real
  `register_or_reuse` (`:527-585`), `launch` (`:711-735`), `open_or_reuse`
  (`:737-758`), and `feed`/`read`/`close` routing to the live session
  (`:777-817`). Directory is `InMemoryHarnessSessionDirectory`.
- `harness_liveness.rs:718-894` (`mod terminal_cell_runtime`, `#[cfg(feature =
  "terminal-cell-runtime")]`): `TerminalCellLauncher` (`:737-746`) spawns a real
  PTY via `TerminalCell::spawn_session` (`:757-780`), subscribes to the
  transcript, sends input, and reads until a stop condition. Without the
  feature, `TerminalCellLauncher`/`TerminalCellSurface` are not compiled
  (`:464-465` re-export is cfg-gated) and there is no other production launcher.

### D. The "Claude live proof" is harness-level with a hardcoded prompt

- `src/bin/mentci-claude-proof-test.rs:1-6`: prints "skipped" unless built with
  `terminal-cell-runtime`. Runtime-gated by env `MENTCI_RUN_REAL_CLAUDE_PROOF=1`
  (`:36,:115-118`); witness path from `MENTCI_REAL_CLAUDE_WITNESS` (`:37,:119`).
- It **hardcodes** the launch spec: `ProofPreflight::launch_nota()`
  (`:380-388`) is a fixed `MentciPreflightLaunch` NOTA parsed directly
  (`:375-377`). **`PreflightEngine` / `PreflightApi::complete` are never called**
  — the routing step is bypassed.
- It then drives the real engine: `ClaudeCodeAdapter::launch` with model haiku
  (`:166-176`, `ClaudeCodeModelCommand::haiku`) → `NamedHarnessSessions::new(
  InMemoryHarnessSessionDirectory, TerminalCellDriver::<TerminalCellLauncher>
  ::default())` (`:196-201`) → real `claude`. It feeds three fixed turns
  (`:211-259`: ready marker, create `mentci-proof.txt`, `jj commit`), observes
  artifacts, verifies the file + commit, and guards `/home/li/primary` unchanged
  (`:285-291`).
- **Evidence it actually ran:** `/home/li/.claude/projects/
  -tmp-mentci-real-claude-proof-*` — six session dirs whose names match the
  proof's temp-path scheme exactly, latest 2026-06-29 02:13. The latest holds a
  real 48-line Claude Code session `.jsonl` (14 `assistant` messages, tool use /
  attachments / skill listing). The five worktree binaries (`mentci`,
  `mentci-daemon`, `mentci-claude-proof-test`, ...) are all built in
  `target/debug/` dated 2026-06-29 02:14, so the crate compiles with the
  feature. `terminal-cell` is present in `Cargo.lock:1364`.

### E. Run / deploy surfaces

- Daemon entry: `mentci-daemon <config-file>` → `DaemonCommand::run`
  (`command.rs:42-44`) → `Daemon::run` → `bind` (`daemon.rs:62-97`). The config
  file is a length-prefixed `meta-signal-mentci` `Configure` frame, **not** NOTA
  (`command.rs:29-40`, `configuration.rs:21-30`). A helper binary
  `mentci-write-configuration` exists to author it.
- CLI: `mentci <request>` (`main.rs`, `client.rs:53-105`). Socket path from
  `$MENTCI_SOCKET`, else `$XDG_RUNTIME_DIR/mentci.socket`, else
  `/tmp/mentci.socket` (`client.rs:153-161`).
- **Not part of any host deployment**: grep for `mentci` in
  `/home/li/primary/CriomOS` and `/home/li/primary/flake.nix` = no hits. No
  `services.mentci` / `mentci-daemon` NixOS module in the non-generated primary
  tree. "Deploy" here can only mean a local cargo dev-run today.
- Tools present: `claude` v2.1.198 (`/home/li/.nix-profile/bin/claude`),
  `jj` 0.40.0.

## Interpretation

1. **End-to-end prompt→route→Claude today: NO wired path.** Two independent gaps
   sit between a user prompt and a routed live session:
   - the routing half (`PreflightApi::complete`) has no production
     implementation — only a test fake (fact B);
   - nothing connects the daemon's request loop (or any prompt entry point) to
     `PreflightEngine` or to the `adapter → sessions → driver` launch engine
     (facts A, D). The daemon speaks only the approval/interface surface.
   What *is* real and proven is the **launch/drive half**: given a launch spec,
   the adapter+sessions+terminal-cell engine spawns and multi-turn-drives a real
   `claude` session in a jj sandbox. The proof demonstrates this — but with a
   **hardcoded** launch NOTA and a **hardcoded** prompt, not a routed user
   prompt (fact D).

2. **Run/deploy model:** standalone cargo daemon (`mentci-daemon`) + thin CLI
   (`mentci`), git-dependency workspace, no Nix, not in CriomOS. The daemon is
   runnable but exposes no prompt routing; the only real prompt→Claude exercise
   today is the harness-level proof binary, not the daemon.

3. **Live-test requirements (real conditions):** `claude` must be logged in with
   a working subscription (it is present and prior proof runs on 2026-06-29
   succeeded, implying auth was valid then — not re-verified today). `jj` must be
   present (it is). Model is haiku, hardcoded in the proof. The psyche does **not
   type a prompt** anywhere — the "prompt" is fixed in the proof source; the
   psyche runs the proof and reads the witness file plus the sandbox transcript
   under `~/.claude/projects/-tmp-mentci-real-claude-proof-*`. There is no
   interactive prompt-entry surface in the current code.

## Verdict

- **For "psyche types a prompt → mentci routes it → live Claude session,
  end-to-end": NOT READY.** Single biggest blocker: there is no production
  `PreflightApi` (routing model client) and no wiring from any prompt entry
  point to the launch engine — the routing half is a bare trait and the daemon
  is not connected to `preflight`/`harness_*` at all.
- **For "run a real, live Claude session driven by mentci's harness engine
  today": ALREADY DONE (harness-level), with a fixed prompt.** Reproducible via
  the proof binary.

### If the psyche wants the proven harness-level live run (fixed prompt)

Concrete steps (local dev-run; spawns real `claude` in a temp jj sandbox,
guards `/home/li/primary`):

1. `cd /home/li/wt/github.com/LiGoldragon/mentci/claude-artifact-session-integration`
2. Build/run with the feature and run gate:
   `MENTCI_RUN_REAL_CLAUDE_PROOF=1 MENTCI_REAL_CLAUDE_WITNESS=/tmp/mentci-witness.md
   cargo run --features terminal-cell-runtime --bin mentci-claude-proof-test`
3. Preconditions: logged-in `claude` (present) and `jj` (present). Output: a
   witness file at the given path plus a Claude session transcript under
   `~/.claude/projects/-tmp-mentci-real-claude-proof-*`.
   (This confirms the launch/drive engine, not routing. Read-only scout did NOT
   run this.)

### Smallest path to a genuine prompt→route→Claude demo

Implement one real `PreflightApi` (a `complete()` that calls a model to emit the
`MentciPreflightLaunch` NOTA) plus a thin driver that pipes a typed user prompt
through `PreflightEngine::launch` → `ClaudeCodeAdapter::launch` →
`NamedHarnessSessions`, reusing exactly the proof binary's adapter/session
plumbing. No daemon change is strictly required for a demo; a daemon-integrated
version additionally needs a new prompt-submit `MentciRequest` variant and
daemon→engine wiring (fact A).

## Unknowns / Not Checked

- Whether `claude`'s subscription auth is valid **right now** (only inferred
  from present binary + successful 2026-06-29 runs; proof not re-run today).
- Whether the crate rebuilds cleanly today (binaries dated 2026-06-29; no build
  run this session; git deps may need network).
- `Design-SessionFlowSpec.md` in this session dir (the future decomposition
  design) was intentionally **not** read — brief scope is "map what is real."
- `/home/li/git-archive/mentci-fractal/components/*` (an archived component
  split) was not inspected; it is not the current monolith.
- Did not open the criome/introspection bridges' runtime behavior beyond the
  request-routing surface relevant to prompt flow.
