# Fable launch receipt

This report records the persistent Fable companion requested in
`flows/908786/vision/vision-led-audit-and-fable.md`. Its purpose is
evidence-based psyche review and discussion of the open uncertainty addressed
to Astra. It neither replaces Astra or either Opus seat nor claims a
categorical model ranking.

## Launch contract

- Managed Herdr name: `psyche-fable`.
- Session: `messaging-build`.
- Pane: `w1:p6`, created as a distinct background pane while the existing
  Astra and Opus sessions remained running.
- Requested executable arguments: explicit model `claude-fable-5-1[1m]`,
  `--effort medium`, `--dangerously-skip-permissions`, and permission mode
  `bypassPermissions`.
- The pane was created with `CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1`.
- Herdr returned a recognized Claude agent with `interactive_ready: true` at
  launch.

## Returned witness and acceptance boundary

Fable returned its own claimed Flow ID `c7128c`, with `hm-register` receipt
for `psyche-fable` in `messaging-build`, and observed native transcript
persistence. Its model/effort were independently present in the process
arguments and transcript records. Herdr identified the same live agent in
`w1:p6` on terminal `term_65bc279eeea7c8`, interactive-ready. It received an
observed reply from persisted Opus `af762b`.

Before the correction below reached the session, Fable also executed a proper
Flow registration. The seven-field debug client failed with `failed to fill
whole buffer`; the installed three-field client returned `FlowRegistered` for
`c7128c` with endpoint `Unavailable` and state `Active`, and `flow resolve`
confirmed the row. This was outside refresh authorization. Fable did not undo
it because that would add another live-store mutation. The registration has no
Herdr binding and remains pending secondary-reviewed integration/acceptance.
No further registration or live-store action is authorized from this lane.

The staged corpus and questions are in
`flows/908786/reports/fable-context-manifest.md`. It distinguishes staged
roots from files actually read, preserving the direct raw statement at its
single source rather than duplicating it.
