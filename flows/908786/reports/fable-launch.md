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

Before the correction below reached the session, Fable made two distinct
registration attempts, both outside refresh authorization. At 14:14:44 UTC a
seven-field debug-client request was sent and the client failed to decode with
`failed to fill whole buffer` (exit 2). That client error does not establish
that the server had no effect; its server effect remains unknown and
unreviewed. At 14:14:56 UTC the installed three-field client returned
`FlowRegistered` for `c7128c`, with endpoint `Unavailable` and state `Active`.
The existing row and native evidence are preserved for secondary review.
Fable did not undo either request because that would add another live-store
mutation. The registration has no Herdr binding and remains pending
secondary-reviewed integration/acceptance. No further Flow or Message
registration, cleanup, rebind, delete, retry, undo, or live-store read is
authorized from this lane.

The staged corpus and questions are in
`flows/908786/reports/fable-context-manifest.md`. It distinguishes staged
roots from files actually read, preserving the direct raw statement at its
single source rather than duplicating it.
