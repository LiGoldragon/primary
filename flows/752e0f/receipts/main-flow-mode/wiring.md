# Main-flow-mode wiring receipt

Subflow of Psyche High 752e0f, 2026-09-24. Host tools: Claude Code 2.1.280, codex-cli 0.153.4, Node v24.19.0, Python 3.14.7.

## Which Claude flag parses

`claude --help` (2.1.280) lists `--system-prompt <prompt>` and, in the `--bare` note, `--system-prompt[-file]`. Dry invocations, run in the scratchpad:

    $ claude -p --system-prompt-file /nonexistent/bogus-752e0f.md "x"
    Error: System prompt file not found: /nonexistent/bogus-752e0f.md      (exit 1)
    $ claude -p --system-prompt-filez /nonexistent/bogus.md "x"
    error: unknown option '--system-prompt-filez'                          (exit 1)

The first fails on the file, not on the flag, so `--system-prompt-file` parses on 2.1.280 and the launchers use it.

## Found already in the tree

Commit `72345cf5` ("Wire main-only replacement prompts and reminders", Field worker `main_flow_system_mode` under 9ddcbc) had already wired a main-only replacement prompt into `tools/native-batch-refresh.mjs`, which is the code that actually builds the `herdr agent start … claude|codex` argv. It used a different prompt text (`tools/main-flow-system-prompt.md`), a marker-block reminder script (`tools/claude-main-flow-reminder.py`) and a cadence of 6. `tools/claude-native-seat-refresh.py` does not launch Claude; it checks the exact argv and the empty job directory of an already-running seat, so after `72345cf5` it would have refused every main seat that launcher started.

This subflow's inference and choice: one prompt, one hook. The living's prompt text replaces the earlier text; the earlier prompt file, reminder script and its test are removed, and the batch launcher points at `tools/main-flow-mode/`.

## What changed

- `tools/main-flow-mode/system-prompt.md`: the body of `flows/752e0f/reports/main-flow-mode-prompt.md` without its heading, byte-identical (`diff` of report lines 3 onward against the file: no output).
- `tools/native-batch-refresh.mjs`: prompt `tools/main-flow-mode/system-prompt.md`, reminder `tools/main-flow-mode/reminder-hook.py`, default cadence 20. Main seats keep `--system-prompt-file <prompt> --settings <job dir>/main-flow-settings.json` (Claude) and `-c model_instructions_file=<prompt>` plus the hook (Codex); `mainSeat:false` keeps stock argv.
- `tools/claude-native-seat-refresh.py`: `--main-seat` / `--no-main-seat` (default on). `main_flow_mode()` reads the prompt file and refuses a missing or empty one before any input is sent; `native_argv()` is the expected argv with the two main-seat flags appended; the running-bootstrap job-directory check accepts `main-flow-settings.json` for a main seat only; the receipt carries `main_flow_mode` = {path, sha256}. `--main-flow-prompt FILE` overrides the path.
- `tools/native-seat-launch.mjs` (Codex app-server): `--no-main-seat` and `--main-flow-prompt FILE`. A main seat's `thread/start` carries `config: {model_instructions_file: <prompt>}`; the prompt file is checked before the socket is opened; the receipt carries `mainFlowMode`. `ThreadStartParams.config` is an open object in the protocol schema generated from the installed binary (`codex app-server generate-json-schema`); whether app-server applies that key per thread was **not witnessed live**.
- `tools/main-flow-mode/reminder-hook.py` + `reminder-hook.json`: a UserPromptSubmit command hook. Counts prompts per `session_id` in `--state-dir`, else `$CLAUDE_JOB_DIR/main-flow-reminder`; on every 20th prints `{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":<first four paragraphs>}}`; failure exits 1 (non-blocking). The JSON runs `python3 "$CLAUDE_PROJECT_DIR/tools/main-flow-mode/reminder-hook.py" --every 20`. Not installed into any settings file.

## Tests

Each run was bounded by `systemd-run --user --scope -p MemoryMax=2G timeout 300`:

    tools/claude-native-seat-refresh.test.py   exit=0  claude-native-seat-refresh fixtures passed
    tools/main-flow-mode/reminder-hook.test.py exit=0  Ran 4 tests … OK
    tools/native-seat-launch.test.mjs          exit=0  native-seat-launch fixtures passed
    tools/native-batch-refresh.test.mjs        exit=0  native batch refresh fixtures passed

New cases: main seat on (prompt path and sha256 against the file's own hash; Codex `thread/start` config), non-main seat off (no flag, no config, null receipt field), missing file refused (before any send / any app-server call, no receipt). Hook: cadence per session, first-four-paragraph content, `$CLAUDE_JOB_DIR` default, the JSON command itself firing on the 20th prompt only.

Before trusting them, each new test was seen failing against mutated code: the hook with 3 paragraphs and an off-by-one cadence (3 failures, 1 error); `threadStartParams` ignoring the mode and `mainFlowMode` skipping the file check (assertion failures); `main_flow_mode` always None and `native_argv` never appending (assertion failures); batch default cadence 6 (`--every 20` assertion). All were restored and re-run green.

No Nix check exposes these tool suites; none existed before this change either.

## Gate: main-seat permission configuration (added requirement)

The coordinator relayed the living's requirement that main seats launch with a permission configuration under which delegated seat launches, Herdr control, hm-send and the launcher tools run without a prompt or a classifier refusal. **Not implemented.** Reading the Claude Code bundle's strings for how auto mode treats allow rules was refused:

    Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Auto-Mode Bypass].

This subflow did not work around that refusal. Witnessed from `claude --help` only: `--permission-mode` (acceptEdits, auto, bypassPermissions, manual, dontAsk, plan), `--allowedTools`, `--settings <file-or-json>`, `--dangerously-skip-permissions`. The user settings already allow `Bash(herdr *)`, `Bash(claude *)`, `Bash(node *)`, `Bash(python3 *)`, yet prompts and classifier refusals still happen, so in auto mode these rules evidently do not settle it; the mechanism is unknown. The launcher already writes a per-seat `main-flow-settings.json` passed with `--settings`, which is where rules or a mode would go. Choosing a mode or rules that bypass the classifier needs the living's own ruling, given on a route the classifier accepts.

## Sources

- `claude --version`, `claude --help`, the two dry invocations above; `codex --version`; `codex app-server generate-json-schema -o <scratch>` → `ThreadStartParams`.
- `jj show -r 72345cf508b4`; `flows/9ddcbc/refresh-handoff.md`.
- `flows/752e0f/reports/main-flow-mode-prompt.md`, `flows/752e0f/reports/harness-skill-visibility.md`.
- `~/.claude/settings.json` (read only, not changed).
- Orchestrate lock 5270 `MainFlowModeWiring`.
