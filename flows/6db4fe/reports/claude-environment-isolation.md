# Claude native environment isolation

Status: source patch and focused fixtures passed; existing live Claude seats have not been resumed or renamed by this change. Runtime same-session and sibling-title proof remains a separate acceptance gate.

## Incident and causal evidence

The one `herdr agent prompt` `/rename` to Psyche High reached one exact pane. Installed Herdr 0.8.2 resolves that pane to one terminal runtime and writes to one PTY actor. The three Claude native processes used different PTYs and bridge session IDs, yet each wrote its own `custom-title` event and file within 27 ms. Their per-process session registry records identified the intended target as `nameSource: user` and the two siblings as `nameSource: peer`.

All three processes inherited the same `CLAUDE_JOB_DIR=/home/li/.claude/jobs/108ab020`. Its `state.json` title changed at the incident time. Installed Claude Code 2.1.263 writes a user rename into that job state (`l$e` → `uB`), while `g8t` watches the job state and applies changed names to each attached process through `tnt(..., "peer", ...)`. This is the observed fan-out mechanism. The bundled source and selected live metadata were read-only; no credentials or conversation bodies were copied into this report.

## Source behavior

`tools/native-batch-refresh.mjs` now reserves a UUID-specific job directory for each new Claude seat. Herdr 0.8.2 `agent start` has no environment field and types the executable into the target pane's shell, so the runner first executes a guarded shell command in that **new pane** to clear inherited Claude child/session identity variables and export only the new job directory. It waits for a marker assembled by the shell, preventing echo from counting as completion. After `agent start`, it checks the exact `--session-id` process in the exact pane and reads back its job directory and identity variables from `/proc`. A foreign job directory or foreign `CLAUDE_CODE_SESSION_ID` fails before native skill refresh. The job directory is reserved empty; this does not claim Claude background-job state.

`tools/claude-bootstrap-controller.py` uses direct `claude --bg` execution. Its launch environment now clears inherited job and child/session identity variables; Claude itself allocates the background job. The retired `tools/claude-single-turn-start.py` Herdr launch path fails closed before touching a pane because it cannot verify isolated job state. Existing native sessions are untouched by these source changes.

## Tests and boundaries

The changed batch fixture executes the generated shell command in a disposable zsh with a deliberately contaminated parent environment, and verifies the new job path and cleared inherited identity variables. Direct-bootstrap and retired-path fixtures pass locally and in a scoped remote Nix derivation on Prometheus. The first repository-wide remote `native-seat-fixtures` check failed before the changed batch fixture: its existing `native-seat-launch.test.mjs` could not find `herdr` in that check's build closure. Its owner published a separate fixture correction; a coherent rerun on that revision remains to be recorded. No local Nix fallback was used.

Same-native-session resumption must retain the native UUID, model, effort, context, Herdr terminal/route, and exact owner acceptance. Claude CLI 2.1.263 documents `--resume <session-id>` as continuing the same ID unless `--fork-session` is chosen. Runtime owner should checkpoint an idle seat, exit it gracefully, prepare an isolated job directory in the same Herdr shell, resume the exact UUID, and verify its native transcript/registry and sibling titles before declaring isolation accepted. Busy seats require owner checkpoint before exit. No transcript edit, process environment surgery, or second native UUID is authorized by this source patch.

The Ultra profile input was restored separately by its owner. Ultra launch remains gated on live same-session isolation proof. Current source fixtures are not a runtime acceptance receipt.
