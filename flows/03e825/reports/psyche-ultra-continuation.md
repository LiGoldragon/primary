# Psyche Ultra retained continuation attempt

The one authorized `continue-retained` attempt ran from the parent's real managed shell at 2026-09-21 20:03:58 UTC using the exact published launcher source and canonical one-seat Haiku profile. Its new state is `flows/03e825/psyche-ultra-native-continuation/state.json`. The preflight prompt render is `flows/03e825/psyche-ultra-native-continuation/prompt-preflight.json`; both `role_prompt` and `custom_system_prompt` recorded zero matches for the targeted long hash/revision noise pattern. This render check is limited to that pattern.

The continuation failed at `herdr pane wait-output` with `timed out waiting for output match`, before `agent start`. It retained the same `wD:p8` pane, terminal, and reserved UUID from the failed second attempt. The parent directly read the pane: the standalone exact `CLAUDE_ENV_READY_UUID` marker was visible in pane history (twice), while a recent read was empty. That does not prove a fresh marker for this continuation; historical output for the same UUID may satisfy a less specific observation. The parent's process check found only the shell. There was no Claude process, startup prompt delivery, receipt, native identity, HM route, canonical title readback, readiness, or Ultra acceptance.

The original first and second failed attempt states remain byte-identical to committed versions. This report records the new failure without authorizing a retry or changing source. The 6db4fe launcher owner must address marker freshness and wait-output behavior before another continuation can be evaluated.

## Sources

- `flows/03e825/psyche-ultra-native-continuation/state.json`: controller's separate failed continuation state and exact wait-output error.
- `flows/03e825/psyche-ultra-native-continuation/prompt-preflight.json`: render sizes, digests, and scoped noise-match counts.
- `flows/03e825/psyche-ultra-native-attempt2/state.json` and `flows/03e825/psyche-ultra-native/state.json`: current bytes compared with committed `HEAD` versions; both equal.
- Parent's direct managed-shell execution at 20:03:58 UTC, pane read showing marker in history and empty recent output, and process observation of shell only.
- `tools/native-batch-refresh.mjs`, `tools/native-batch-refresh.test.mjs`, and `flows/6db4fe/reports/ultra-retained-continuation.md`: canonical bytes installed from published remote `main` and verified equal before execution.
