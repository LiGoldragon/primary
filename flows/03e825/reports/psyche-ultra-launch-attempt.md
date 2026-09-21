# Psyche Ultra Low single launch attempt

Flow `03e825`, 2026-09-21. The authorized Ultra-only launch was attempted once from the existing real Herdr-managed shell in `messaging-build/w0:p3` after the unchanged canonical one-seat manifest validated. The attempt stopped at Herdr tab creation with `workspace_not_found` for `wS`. This failed state is retained for diagnosis; there was no retry or manifest edit.

## Exact attempted boundary

`flows/03e825/psyche-ultra-native/preflight.json` records the pre-start validation of `flows/753e69/psyche-haiku-native/launch-manifest.json`, exact canonical profile, all eleven audited source matches, and the executor shell's pane, terminal, PID, and genuine `HERDR_ENV=1`. Its phase `validated-not-started` is a preflight snapshot, not a later launch-success claim. The profile selects a fresh `Psyche Ultra Low` Claude Haiku 4.5 seat at medium effort, with no predecessor, preserving existing Low `0625c3`.

`flows/03e825/psyche-ultra-native/state.json` is the controller's version-1 state from the one `start`. It records one seat at `phase: failed` and the exact Herdr `cli:tab:create` error `workspace_not_found` (`workspace wS not found`). No `paneId`, `terminalId`, or `nativeThreadId` was recorded in that seat state. The attempted receipts directory is absent. Parent's direct post-failure read of Herdr workspace list also found `wS` absent. Manifest `validate` checks the profile, source hashes, skills, and declared workspace field; it does not establish that the named workspace exists live. The controller failed before creating a pane, reserving a native UUID, starting Claude, injecting a skill, or generating a native receipt. No own Flow identity, title, HM route, role acceptance, or predecessor retirement occurred.

## Source and fixture grade

The currently installed `tools/native-batch-refresh.mjs` and `tools/claude-native-seat-refresh.py` are byte-equal to those at commit `bcb6117e2a57e1b50457a7dbc3fa103f83789b69` (`git show` source hash comparison). The report at that exact commit says its coherent third remote `native-seat-fixtures` run passed on Prometheus after test-only interpreter fixes; that is the original fixture owner's reported remote result, distinct from this failed live launch. The current working-tree copy of that report is older and must not override the committed `bcb6117e` statement. No duplicate remote fixture build was run here. Fixtures do not prove live workspace existence, native startup, or isolation acceptance.

The failure is specifically at live workspace lookup. Any future work needs an explicit, separately authorized path after the current failed state is reviewed; this record does not request or perform a retry. Existing Psyche Low and every other native seat and route remain untouched.

## Sources

- `flows/03e825/psyche-ultra-native/preflight.json`: point-in-time exact profile/source and real managed-shell preflight.
- `flows/03e825/psyche-ultra-native/state.json`: persisted single failed controller state and exact `cli:tab:create` error; absence of pane, terminal, and native ID fields.
- `flows/753e69/psyche-haiku-native/launch-manifest.json` and `profile.json`: canonical unchanged one-seat Ultra input.
- `tools/native-batch-refresh.mjs`: `validate` and `start` boundary, state creation, tab-create first live step; `tools/claude-native-seat-refresh.py`: downstream native refresh path that was not reached.
- `git show bcb6117e2a57e1b50457a7dbc3fa103f83789b69` for both runtime sources and `flows/6db4fe/reports/claude-environment-isolation.md`; `sha256sum` comparison to currently installed runtime files.
- Parent's read-only post-failure `herdr --session messaging-build workspace list` witness of missing `wS`, as relayed in this delegated task. No Herdr operation was performed by this reporting subflow.
- Orchestrate lock `4066` reserved this Flow's failed state, receipt directory, and preflight artifacts during the one attempt.
