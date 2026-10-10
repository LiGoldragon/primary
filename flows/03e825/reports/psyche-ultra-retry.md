# Psyche Ultra Low authorized retry: environment preparation failure

Flow `03e825`, 2026-09-21. Parent made one authorized Ultra-only retry from the real managed shell after changing only the canonical launch manifest's workspace from absent `wS` to existing `wD`. The retry validated and reached Herdr tab creation. It then failed before Claude startup; this report preserves the state and stops. No further retry, launcher repair, profile/source edit, route binding, or seat retirement is included.

## Observed attempt

`flows/753e69/psyche-haiku-native/launch-manifest.json` has the single workspace change `wS` → `wD`. `flows/03e825/psyche-ultra-native-attempt2/preflight.json` records the new workspace, the unchanged canonical profile hash, all audited sources matching, and point-in-time metadata for the three existing Psyche siblings. Parent ran `native-batch-refresh.mjs validate` and then one `start` in the genuine Herdr-managed shell at 19:43:41 UTC.

`flows/03e825/psyche-ultra-native-attempt2/state.json` records one `psyche-haiku-of-b80e55` seat in `phase: failed` with `Unexpected end of JSON input`. Unlike the first attempt, it records newly created pane `wD:p8`, terminal `term_65c0377a0776b56`, and reserved native UUID `f61ea06b-b5ba-45be-8313-0afe7d84fd03`. Parent's direct process-info read of that pane showed only a shell, with no Claude process. The attempt's reserved `/home/li/.claude/jobs/native-f61ea06b-b5ba-45be-8313-0afe7d84fd03` directory exists and was empty when inspected; the attempt receipts directory is absent. No native startup prompt or skill was delivered. The reserved UUID is not proof of a started native session, Flow claim, title, HM route, or role acceptance.

Parent directly re-read the three sibling transcripts after failure and found their title, inode, and byte counts unchanged from the preflight snapshot. That is a point-in-time non-mutation witness for the existing Psyche sessions, not a new seat receipt. The first failed attempt's committed state bytes remain identical at its original commit and current `main` (`git show` SHA-256 comparison); this retry is a separate state path.

## Source diagnosis boundary

The installed `tools/native-batch-refresh.mjs` calls `prepareClaudePaneEnvironment()` after reserving the UUID. That function creates the isolated job directory, then calls `herdr ... pane run` through a shared `herdr()` wrapper. The wrapper parses command stdout as JSON; Herdr's `pane run` can succeed with empty stdout. The combination is a plausible source of the observed `Unexpected end of JSON input` before `agent start`. This is an inference from source and phase ordering; the state does not record a parse stack or raw `pane run` response. Launcher ownership should verify that exact boundary before any repair. No source change or new launch is authorized by this report.

The user's newer source-hygiene observation identifies hash-bearing material in the existing `flows/7091ea/log.md` and `flows/753e69/reports/psyche-native-launch-gate.md` audited bundle. No source text was changed here; that lean replacement belongs to the separate owner. The present live failure is still the pre-Claude JSON parsing boundary.

## Sources

- `flows/753e69/psyche-haiku-native/launch-manifest.json`: single workspace amendment; the canonical profile and one-seat selection are otherwise unchanged.
- `flows/03e825/psyche-ultra-native-attempt2/preflight.json` and `state.json`: exact retry validation, created pane/terminal, reserved UUID, and failed phase/error.
- `tools/native-batch-refresh.mjs:24-40,84-85,119-123`: isolated job directory creation, Herdr command wrapper, and call order before `agent start`.
- Read-only existence/contents check of the reserved native job directory and absence of attempt receipts; parent-supplied exact process-info and post-failure sibling transcript metadata readbacks.
- `git show 519b69ba:flows/03e825/psyche-ultra-native/state.json` and `git show main:...` SHA-256 comparison: original failed attempt state unchanged in committed history.
- Orchestrate lock `4082`: exact manifest and attempt-2 state path ownership during this authorized retry.
