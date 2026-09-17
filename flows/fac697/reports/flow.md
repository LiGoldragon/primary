# Flow Nexus delivery

Flow Nexus is published as three standalone repositories under the configured
repository root:

- `flow` main `415df4106fa1b89c8885ff271b34b56794b7bebe`
- `signal-flow` main `f3a0780be0d3f870bc0035857f657668ec0cf3a7`
- `meta-signal-flow` main `409f6c6c85e9cba6a21cc0c540d25a41fca9efb2`

The no-argument `flow-nexus` owns the ordinary and meta sockets and a single
Sema store. The ordinary `flow` client implements `flow start
<predefined-type>`, `flow restart <flow-id>`, and the Message-facing `flow
resolve <flow-id>` projection. Start stamps the caller Flow/session origin,
selects the predefined Codex medium instructions, and creates a daemon-owned
thread through `codex app-server proxy`, `thread/start`, and `turn/start`.
Restart succeeds only when caller provenance equals the target Flow ID.

`ResolveRecipient` returns the typed `FlowNode`: Flow ID, session ID, harness
kind, endpoint selection and readiness, origin clue, and lifecycle. Message
Nexus was given the exact signal-flow revision and default ordinary socket.

The privileged `flow-meta reset [credit-id]` operation maps to
`account/rateLimitResetCredit/consume` through the same Codex adapter. The
operation was tested with a mock app-server response; no real credit was
spent.

Rust format, clippy with warnings denied, and all 13 Flow workspace tests
passed. Both contract repositories passed their all-feature Signal/Datom
round-trip tests. A live no-argument Nexus accepted `flow start codex-medium`
as Flow `flow-0000000000000001`, returning daemon thread
`01a0b1bc-48a5-7a61-ab59-cddcdff1ef73`. Resolve returned that thread as a
ready Codex endpoint, and a restart carrying the child Flow's own provenance
returned generation 2. The original caller's Flow ID was `fac697` and was
recorded in the start origin clue.

## Sources

- `/home/li/primary/flows/da1e3f/reports/codex-brief-tools.md`
- `/home/li/primary/Vision/flowNexus.md`
- `/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/`
- `/home/li/.codex/sessions/2026/09/17/rollout-2026-09-17T12-05-01-01a0b08b-1950-7ee1-92e8-0c5562869d29.jsonl`
- `/tmp/da1e3f-schema/`
- `/git/github.com/LiGoldragon/flow`
- `/git/github.com/LiGoldragon/signal-flow`
- `/git/github.com/LiGoldragon/meta-signal-flow`
