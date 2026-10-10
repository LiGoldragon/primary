# Psyche Ultra native bootstrap gate

The parent's one guarded retained continuation began at 2026-09-21 20:16:58 UTC with the canonical Haiku profile and the exact published `2ed8f5c90` launcher source. A local diff of the launcher, fixture, and Claude helper against that source revision was empty. The fresh environment nonce gate passed, and Claude started in the already reserved `wD:p8` pane with the same terminal and native session UUID. Herdr reported the agent idle and `interactive_ready: true`. Parent-observed process data showed Claude PID 3112231 with `--session-id` matching the retained UUID, `--model claude-haiku-4-5-20251001`, and `--effort medium`; helper PID was 3112381. The pane UI showed Haiku 4.5 at 0% context.

The separate state at `flows/03e825/psyche-ultra-marker-continuation/state.json` records failure in `claude-native-seat-refresh.py` line 369: the native Claude transcript JSONL for that UUID was unavailable. This occurred before rename, skill injection, or the source startup prompt. The manifest receipt file records intended profile fields and sources, but the expected native output receipt file is absent. Process arguments and Herdr interactivity are therefore not a transcript/model receipt, own Flow claim, canonical title, HM binding, skill/source-prompt acceptance, or full readiness.

The parent's scoped `process-isolation.json` witness records a job directory specific to the retained UUID in the running Claude process; `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_SESSION_KIND`, `CLAUDE_CODE_SESSION_ID`, and `CLISESSIONID` were unset. All three existing Psyche sibling titles and transcript inodes remained the same. Medium and Low transcript byte counts were unchanged; active High's byte count changed, with no cause attributed here. This process/environment witness is not native context acceptance.

The running native Claude process and retained pane must be preserved; no restart, new UUID, retry, transcript fabrication, or source repair was performed here. The three earlier failed states remain byte-identical to their committed versions. Any next action belongs to the launcher/source owner and must account for the already-running session.

## Sources

- `flows/03e825/psyche-ultra-marker-continuation/preflight.json`: rendered prompt sizes, scoped noise check, and sibling preflight snapshot.
- `flows/03e825/psyche-ultra-marker-continuation/state.json`: retained resource identities, environment marker, failed phase, and exact transcript-unavailable error.
- `flows/03e825/psyche-ultra-marker-continuation/receipts/psyche-haiku-of-b80e55.manifest.json`: intended native session/profile; expected output JSON receipt absent from the same directory.
- `flows/03e825/psyche-ultra-marker-continuation/process-isolation.json`: parent-collected exact process environment and sibling identity/size snapshot.
- Parent's direct Herdr agent, pane UI, and process observations at the 20:16:58 UTC continuation: idle interactive agent, Claude PID 3112231, helper PID 3112381, exact process arguments.
- `git diff 2ed8f5c90 -- tools/native-batch-refresh.mjs tools/native-batch-refresh.test.mjs tools/claude-native-seat-refresh.py`: empty in the active checkout.
- `flows/03e825/psyche-ultra-native/state.json`, `flows/03e825/psyche-ultra-native-attempt2/state.json`, and `flows/03e825/psyche-ultra-native-continuation/state.json`: current SHA-256 values compared equal to committed `HEAD` versions before this report.
