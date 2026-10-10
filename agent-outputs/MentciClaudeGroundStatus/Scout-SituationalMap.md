# Scout Situational Map

## Task And Scope

Read-only ground-status check for `/home/li/primary` against a pasted Mentci/Claude handoff. The handoff is treated as unverified. I did not edit source files, run Claude proof work, commit, push, inspect `private-repos/`, search `/nix/store`, or read user-level `~/.claude` contents. I wrote only this assigned scout output.

## Commands And Surfaces Consulted

- Workspace contract: `sed -n '1,220p' AGENTS.md`.
- Required skills for this turn: `/home/li/primary/.agents/skills/intent-led-orchestration/SKILL.md`, `/home/li/primary/.agents/skills/jj/SKILL.md`.
- Primary VCS state: `jj status --no-pager`, `jj bookmark list --no-pager`, `jj log -r 'main..@' --no-pager`.
- Process/session state: `pgrep -af 'claude|mentci|terminal-cell|orchestrate|tmux|zellij|screen'`, `ps -o pid,ppid,etime,%mem,rss,stat,command -p ...`, `readlink /proc/<pid>/cwd`.
- Task state: `bd --readonly status`, `bd --readonly ready --limit 20 --plain`, `bd --readonly list --status in_progress --flat --no-pager --limit 50`, `bd --readonly search ...`, `bd --readonly show ...`.
- Orchestrate state: `orchestrate '(Observe Lanes)'`, `orchestrate '(Observe Roles)'`, lock-file reads under `/home/li/primary/orchestrate/`.
- Reports/docs: `reports/mentciWeavePrep/1-Design-mentci-bead-weave-handoff.md`, `reports/operatingModeShift/0-Synthesis-agent-context-routing-brief.md`, `reports/operator/465-agent-memory-claude-gating-exploration.md`, `/home/li/primary/INTENT.md`, `/home/li/primary/ARCHITECTURE.md`, `/home/li/primary/orchestrate/ARCHITECTURE.md`.
- Component docs/code: `/git/github.com/LiGoldragon/mentci/{AGENTS.md,INTENT.md,ARCHITECTURE.md,schema/preflight-launch.nota.md,src/preflight.rs,src/harness_adapters.rs,src/harness_sessions.rs,src/harness_liveness.rs,tests/preflight.rs,tests/harness_sessions.rs}` and `/git/github.com/LiGoldragon/terminal-cell/{AGENTS.md,INTENT.md,ARCHITECTURE.md,src/lifecycle_cli.rs}`.
- CLI help: `claude --help`; `command -v terminal-daemon`, `command -v terminal-cell`, `terminal-daemon --help`.

## Observed Ground Truth

- Primary working copy is dirty before this scout output: `jj status --no-pager` reported modified `.codex/agents/*.toml` role packets and an added `agent-outputs/CodexInstructionSurfaces/Scout-SituationalMap.md`. Current `@` is `qryqmuvn 44f734f3 (no description set)`, parent/main is `yuqqnkwx b8dfa7d0`.
- Primary bookmarks include `main: yuqqnkwx b8dfa7d0`; many old operator/report bookmarks also exist. `jj log -r 'main..@'` shows only the current working-copy commit over main.
- Relevant component repos are clean:
  - `/git/github.com/LiGoldragon/mentci`: `jj status --no-pager` says no changes; `main: xtsuyuru 082b1481 mentci: use configured Claude command`; `@` is an empty no-description working copy above main.
  - `/git/github.com/LiGoldragon/terminal-cell`: `jj status --no-pager` says no changes; `main: szlszuzx 17b043c5 terminal-cell fix CloseCell process cleanup`; `@` is an empty no-description working copy above main.
- Live process state matters:
  - `pgrep` found an orchestrate daemon: `/home/li/.nix-profile/bin/orchestrate-daemon /home/li/primary/orchestrate/orchestrate-daemon.signal`.
  - `pgrep` found mentci/criome daemon test processes under `/tmp/mentci-egui-sandbox` and `/tmp/mentci-introspect-live-systemd-*`.
  - Three long-running `claude --dangerously-skip-permissions` processes exist. `readlink /proc/<pid>/cwd` for PIDs `3502734`, `3540722`, and `3918319` all returned `/home/li/primary`. They should not be used for any sandbox proof.
  - Two terminal-daemon sessions exist for the live Claude proof. The active child Claude under PID `4137992` has cwd `/tmp/mentci-primary-swex-live-fixed2/work` and command `claude --add-dir /tmp/mentci-primary-swex-live-fixed2/scaffold --name primary-swex-claude-live-fixed`. That child was not launched with `--dangerously-skip-permissions` or `--model`.
- `/tmp/mentci-primary-swex-live` and `/tmp/mentci-primary-swex-live-fixed2` contain proof artifacts: `terminal.sema`, control/data sockets, `viewer.ready`, transcript/capture/log files, scaffold/work dirs. `find .../work -maxdepth 4` returned no files in either work directory. The only scaffold file observed was `/tmp/mentci-primary-swex-live/scaffold/README.md`. Existing live-proof artifacts do not show Claude file writes in the sandbox work dirs.
- Claude CLI local help supports:
  - interactive default behavior;
  - `--dangerously-skip-permissions`;
  - `--model <model>`;
  - `--bare`, with help text saying it skips auto-memory and keychain/CLAUDE discovery and uses API-key style auth;
  - `--print`, with output formats and non-interactive behavior.
  The help examples list aliases `fable`, `opus`, and `sonnet`; help did not prove a `haiku` alias.
- `terminal-daemon` and `terminal-cell` are not on `PATH` (`command -v` failed; `terminal-daemon --help` returned command not found). The running terminal-daemon binaries are Nix-store paths, but I did not search `/nix/store`.
- Task database state:
  - `bd --readonly status`: 902 total issues; 247 open; 7 in progress; 52 blocked; 645 closed; 195 ready.
  - `bd --readonly ready --limit 20 --plain` lists `primary-iy51.13` and other Mentci/component tasks as ready, but not the specific Claude sandbox proof.
  - `bd --readonly list --status in_progress` shows 7 in-progress tasks; none are this Claude/Mentci proof.
  - Parallel `bd` reads often failed with `embeddeddolt: another process holds the exclusive lock`; serialize `bd` reads.
- Specific task records:
  - `primary-swex` is closed: "Live-visible Claude round trip through persistent session" with close reason saying a named terminal-cell session can launch configured Claude subscription TUI, accept prompt input, surface output/events, and remain inspectable. It explicitly lists non-goals: not asking Claude to change files or run jj work.
  - `primary-0bax` is open: "Sandboxed work proof in ephemeral jj repo after live Claude round trip"; it requires a fresh sandbox jj repo outside `/home/li/primary`, normal subscription TUI, no API/headless/`--print`/`--bare`, live visible terminal, and retained inspectable state or explicit close reason.
  - `primary-57ce` is open: "Initial lifecycle policy for persistent harness sessions"; it requires typed close reasons and says one prompt turn completing is not a close reason.
  - `primary-7e7a` and `primary-xj1y` are open for shakeout and failure classification after `primary-0bax`.
- Orchestrate state:
  - `/home/li/primary/orchestrate/ARCHITECTURE.md` says orchestrate owns coordination, lane registry, worktree registry, and lock-file projections; it does not own process liveness.
  - `orchestrate '(Observe Lanes)'` lists lanes including `mentci-weave-prep-designer`, `primary-egbn-operator`, and other structural/support lanes.
  - `orchestrate '(Observe Roles)'` shows active claims for `cloud-maintainer`, `cloud-operator`, and `system-designer`; no active role claim for this Claude sandbox proof.
  - Nonempty lock files agree: `cloud-maintainer.lock`, `cloud-operator.lock`, and `system-designer.lock` hold unrelated repo scopes.
- Mentci docs/code:
  - `/git/github.com/LiGoldragon/mentci/INTENT.md` states Mentci grows toward prompt-to-work routing where a prompt enters Mentci, API preflight emits fixed-schema NOTA, persistent named sessions are core, terminal-cell owns liveness, and orchestrate owns naming/addressing/lookup.
  - `/git/github.com/LiGoldragon/mentci/ARCHITECTURE.md` marks prompt-to-bead-weave as possible future/target architecture, not current daemon behavior. It states the preflight launch schema is canonical and that adapter identity, terminal-cell driver identity, provider model identifiers, and terminal launch policy are downstream adapter/session launch-plan details.
  - `/git/github.com/LiGoldragon/mentci/schema/preflight-launch.nota.md` defines the fixed positional `MentciPreflightLaunch` schema and says it is a schema artifact, not implementation of preflight engine, terminal-cell driver, adapter, or scaffold cache.
  - `/git/github.com/LiGoldragon/mentci/src/preflight.rs` builds a prompt asking for exactly one `MentciPreflightLaunch` NOTA record and validates model profiles. It only verifies semantic profiles `cheap-contained-preflight` and `cheap-harness-session`, not concrete provider IDs.
  - `/git/github.com/LiGoldragon/mentci/tests/preflight.rs` has a boundary test that forbids Claude/provider terms such as `claude-haiku`, `subscription-tui`, `permission-mode`, `apiKeyHelper`, `--print`, and `--bare` from `preflight.rs` and `harness_sessions.rs`.
  - `/git/github.com/LiGoldragon/mentci/src/harness_adapters.rs` currently contains a `ClaudeCodeAdapter`. That means Claude-specific code currently lives inside the Mentci repo, although outside the front-door/preflight/session-boundary files.
  - The current `ClaudeCodeAdapter::arguments()` returns only `--add-dir <scaffold>` and `--name <lane>`. It does not add `--dangerously-skip-permissions` or `--model`.
  - The current model knob is `ClaudeCodeModelCommand::haiku()`, which sends interactive text `/model haiku`, not the CLI `--model` flag.
  - `/git/github.com/LiGoldragon/mentci/src/harness_adapters.rs` maps permission/confirmation-looking transcript text into an adapter interaction event.
  - `/git/github.com/LiGoldragon/mentci/tests/harness_sessions.rs` proves open-or-reuse, reuse without relaunch, address mismatch rejection before terminal launch, non-persistent rejection, unknown-session diagnosis, and closed-session diagnosis.
  - `/git/github.com/LiGoldragon/mentci/src/harness_liveness.rs` shows liveness stop reasons for completion signal, turn cap, close report, terminal exit, and timeout/stalled-output style deadlines.
- Terminal-cell docs/code:
  - `/git/github.com/LiGoldragon/terminal-cell/INTENT.md` says terminal-cell is the low-level PTY/transcript primitive; Persona-facing session ownership, naming, registry, and policy stay in `terminal`.
  - `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md` says terminal-cell owns one child PTY, append-only transcript truth, disposable viewers, typed input/capture messages, plane isolation, input gate, one active viewer, and worker lifecycle. It explicitly says it does not define Persona message semantics, harness identity, or provider usage policy.
  - `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md` says the root NOTA CLI variants are `LaunchCell`, `SendLine`, `AttachViewer`, `CloseCell`, and `ObserveCell`.
  - `/git/github.com/LiGoldragon/terminal-cell/src/lifecycle_cli.rs` parses exactly stdin or `--file` as NOTA into `CellRequest`; unknown CLI arguments are rejected. This supports strict NOTA input for the root `terminal-cell` CLI, although the current live proof used a lower `terminal-daemon` command line.

## Handoff Claims Status

Supported by local docs/tasks/code:

- Mentci as front door for persistent harness sessions: supported as intended/target shape by `mentci/INTENT.md` and `mentci/ARCHITECTURE.md`; not fully current daemon behavior.
- Do not call that role "router": supported by current docs calling the preflight a routing/prompt-building engine but avoiding "router" as the named Mentci role. Older report `reports/operatingModeShift/...` still used "PreflightRouter", so the term is stale in older design text.
- Prompt flow prompt -> Mentci -> preflight launch packet -> orchestration/session -> terminal/session driver -> TUI -> adapter -> result while session may persist: supported as target shape by `reports/mentciWeavePrep/...`, `mentci/INTENT.md`, `mentci/ARCHITECTURE.md`, and `primary-swex`/`primary-0bax` beads. It is not yet proven end-to-end for file-changing work.
- Preflight output strict fixed-schema NOTA: supported by `mentci/schema/preflight-launch.nota.md`, `src/preflight.rs`, and tests.
- terminal-cell for TUI hosting/injection: supported by live terminal-daemon proof artifacts, `primary-swex`, terminal-cell docs, and Mentci liveness/session code.
- terminal-cell strict NOTA input: supported for the root `terminal-cell` CLI by `terminal-cell/src/lifecycle_cli.rs`; not how the current live proof was launched.
- Orchestrate can hold orchestration only: supported by `/home/li/primary/orchestrate/ARCHITECTURE.md` and Mentci architecture separating lane/address lookup from liveness.
- Test Claude first / use normal Claude subscription TUI / proof live-visible: supported by closed `primary-swex` and open `primary-0bax`.
- Do not use `--bare`, `--print`, API-key/API-style path, or `apiKeyHelper`: supported as constraints in tasks and a Mentci boundary test; Claude help confirms these are real alternative modes to avoid.
- Proof must run in ephemeral sandbox repo outside primary: supported by `primary-0bax` constraints and Mentci adapter sandbox validation fields.
- Sessions should not close at turn completion; closing needs reason/policy; resource pressure plausible close reason: supported by `primary-57ce` as open policy work and by liveness code naming explicit stop/close paths. The exact policy is not complete.
- Permission/confirmation prompts are interaction events; decisions may come from policy/components, not only human: supported by Mentci adapter event classification and task constraints.
- Question discipline claims ("one yes/no at a time", "other questions one at a time", "offer one or two suggestions", "plain English, not bead IDs", "do not make chronology main artifact"): supported by the active role/instruction doctrine in this prompt and by the requested report shape, not by code.

Unsupported, stale, or only partially supported:

- "Claude-specific behavior needs a home outside Mentci": not currently true in source layout. `ClaudeCodeAdapter` lives in `/git/github.com/LiGoldragon/mentci/src/harness_adapters.rs`. The front-door/session boundary is kept clean, but the adapter code is still in the Mentci repo.
- "Launch Claude with `claude --dangerously-skip-permissions`": local Claude help supports the flag, and three primary-cwd Claude processes are using it, but the current Mentci adapter and live terminal-daemon child do not launch Claude with that flag.
- "Use `--model` CLI argument": local Claude help supports `--model`, but current Mentci adapter uses interactive `/model haiku`, not CLI `--model`.
- "Use Haiku for cheap proof runs": current source has `ClaudeCodeModelCommand::haiku()` sending `/model haiku`; local `claude --help` did not prove `haiku` as a valid CLI model alias. This remains unverified.
- "If Claude JSONL/session-file watching works, TUI scraping is not needed": unknown. I did not inspect `~/.claude` or session JSONL contents for privacy reasons, and no proof task has yet established JSONL/file watching as a state signal.
- "Find out what Claude writes to files" and "whether file writes or another push signal can track Claude state": not done yet. Existing `/tmp/mentci-primary-swex-live*/work` dirs were empty, and `primary-swex` explicitly did not ask Claude to change files.

## Active Sessions, Tasks, Reports, Artifacts

- Active live sessions:
  - `/tmp/mentci-primary-swex-live` and `/tmp/mentci-primary-swex-live-fixed2`, with control/data sockets, terminal stores, captures/transcripts/logs, and scaffold/work dirs.
  - Active terminal-daemon PIDs `4035948` and `4137977`; active child Claude PID `4137992` in `/tmp/mentci-primary-swex-live-fixed2/work`.
  - Three unrelated or not-yet-classified `claude --dangerously-skip-permissions` processes with cwd `/home/li/primary`.
- Active tasks:
  - `primary-0bax` open: sandboxed work proof in ephemeral jj repo.
  - `primary-57ce` open: lifecycle policy.
  - `primary-7e7a` open: failure-mode shakeout.
  - `primary-xj1y` open: failure classification.
  - `primary-swex` closed: live-visible round trip done, no file-changing work.
- Relevant reports:
  - `reports/mentciWeavePrep/1-Design-mentci-bead-weave-handoff.md`
  - `reports/operatingModeShift/0-Synthesis-agent-context-routing-brief.md`
  - `reports/operator/465-agent-memory-claude-gating-exploration.md`
- Relevant component artifacts:
  - `/git/github.com/LiGoldragon/mentci/schema/preflight-launch.nota.md`
  - `/git/github.com/LiGoldragon/mentci/src/{preflight.rs,harness_adapters.rs,harness_sessions.rs,harness_liveness.rs}`
  - `/git/github.com/LiGoldragon/terminal-cell/src/lifecycle_cli.rs`

## Next Concrete Options

1. Run `primary-0bax` exactly as scoped: create a fresh ephemeral jj repo outside `/home/li/primary` and descendants, launch a normal Claude subscription TUI through terminal-cell, keep it live-visible, and ask for a tiny controlled file-changing task inside the sandbox only.
2. Before launch, decide whether the proof should use the current implemented adapter behavior or change/override it for the psyche's desired flags:
   - current adapter behavior: `claude --add-dir <scaffold> --name <lane>` plus optional interactive `/model haiku`;
   - handoff-desired behavior: add `--dangerously-skip-permissions` and use `--model <model>` on the CLI.
3. Instrument file-write discovery in the sandbox without reading private Claude state:
   - snapshot `find <sandbox> <scaffold> -type f -printf '%T@ %s %p\n'` before and after;
   - watch only the sandbox/scaffold directories with filesystem events if a watcher is available;
   - separately list new files under the proof runtime directory, not `~/.claude`, unless psyche authorizes user-level Claude state inspection.
4. Track non-file push signals from surfaces already in-bounds:
   - terminal-cell transcript deltas and worker lifecycle events;
   - terminal process exit/close/timeout/stall events;
   - adapter-classified permission/completion events.
5. Treat Claude JSONL/session-file watching as a separate privacy-gated check. It may remove the need for TUI scraping, but proving it likely requires explicit authorization to inspect Claude's session storage or a run configured to write session artifacts inside the ephemeral sandbox.

## Risks And Decisions For The Lead/Psyche

- Decide whether to follow the current landed adapter (`/model haiku`, no dangerous-skip flag) or the handoff's requested CLI flags (`--dangerously-skip-permissions`, `--model`). This is a real divergence.
- Decide whether "Claude-specific behavior outside Mentci" is an immediate refactor requirement. Current code keeps the front door clean but keeps the Claude adapter in the Mentci repo.
- Do not use the existing primary-cwd `claude --dangerously-skip-permissions` processes for proof work. They are active in `/home/li/primary`, which violates the proof boundary.
- Ask explicitly before inspecting `~/.claude` or Claude JSONL/session files. Existing policy and report 465 treated that as private user-level state.
- Serialize `bd` reads in workers; parallel reads hit the embedded Dolt lock.
- No current evidence proves what Claude writes when asked to edit files. The closed live proof did not exercise that behavior.

## Not Checked

- No tests were run.
- No Claude proof prompt was sent.
- No `~/.claude` files, credentials, history, paste cache, or session JSONL contents were opened.
- No `private-repos/` content was inspected.
- No `/nix/store` search was performed.
