# Flow Nexus delivery

Flow Nexus is published as three standalone repositories under the configured
repository root:

- `flow` main `51cfc00e3c34c7e42739fe42b3dd3715dda5b2a4`
- `signal-flow` main `5334763fe61513f4cd8d58160e411c9e8315d1b9`
- `meta-signal-flow` main `8ba99d5ff8dc384f5786231956a6f77d07be69b9`

The no-argument `flow-nexus` owns the ordinary and meta sockets and one Sema
store. The ordinary `flow` client implements `flow start <predefined-type>`,
`flow restart <flow-id>`, and the Message-facing `flow resolve <flow-id>`.
Start stamps the caller Flow/session origin, creates the Flow workspace, and
creates a daemon-owned Codex thread through `codex app-server proxy`,
`thread/start`, and `turn/start`. The child thread receives `FLOW_ID` and
`FLOW_DIRECTORY` in its shell environment. Restart requires both the target
Flow ID and its registered harness session before resuming the same thread.

`ResolveRecipient` returns a typed `FlowNode`: Flow ID, session ID, harness
kind, endpoint selection/readiness, origin clue, and lifecycle. A typed meta
registration operation imports flows created before this Nexus. The live
registry now resolves the current primary Psyche and all five role Codex
sessions:

| Flow | Harness session | Live route |
|---|---|---|
| `da1e3f` | `da1e3f9d-857f-49ab-8c6f-3aa0a9db826b` | Claude daemon control, Ready |
| `d9961c` | `01a0aacb-ac84-71a1-88a0-05ed9961ca9d` | Codex app-server, Ready |
| `348e7b` | `01a0a11f-6130-70e2-80b1-796348e7b086` | Codex app-server, Ready |
| `5c2896` | `01a0a132-9be2-76e0-bf0d-57c5c28961ca` | Codex app-server, Ready |
| `2ff1c4` | `01a0a132-9b27-77e2-bcc6-d8b2ff1c456c` | Codex app-server, Ready |
| `098c76` | `01a0a132-9c6f-7de0-b067-1ed098c76c38` | Codex app-server, Ready |

Claude readiness is advisory and recomputed on every resolution from the job
state, daemon roster, full session identity, rendezvous/control sockets, and
worker process. Permission waits, terminal lifecycle states, dead workers, or
mismatched daemon evidence return `Parked`; ordinary `state: blocked` remains
routable. The current state file has no separate `status` field, so absent
status is bounded by the other daemon evidence; when present, only `idle` and
`busy` are Ready. Message Nexus was given the exact contract and Flow revisions
and re-resolves immediately around native Claude attach/delivery.

The privileged reset operation is `flow-meta reset <idempotency-key>
[credit-id]`. It maps to `account/rateLimitResetCredit/consume` through the
same Codex adapter, and the caller-owned key is stable across retries. The
operation was tested with a mock app-server response; no real credit was
spent. Ordinary and meta frames are bounded to 1 MiB. Both sockets are `0600`;
the meta edge separates protocol surfaces within the owning Unix account and
does not distinguish processes running as the same UID.

The tracked unit is `deployment/flow-nexus.service`. Release binaries were
installed in `/home/li/.local/bin`, the tracked unit was copied into
`/home/li/.config/systemd/user/flow-nexus.service`, and the enabled user
service is active. This is a local user-service installation rather than a
declarative Nix deployment. The incompatible prototype v4 store was preserved
as `/home/li/.local/state/flow/flow.sema.pre-v5-20260917T1749`; the active v5
store is `/home/li/.local/state/flow/flow.sema`.

Rust format, clippy with warnings denied, and all 16 Flow workspace tests
passed. Both contract repositories passed their all-feature Signal/Datom
round-trip tests. Against the installed final build, `flow start codex-medium`
created `flow-0000000000000001` and daemon thread
`01a0b1c9-e276-7881-989f-54cbd370dbb6`; resolve returned that exact Ready
endpoint and restart returned generation 2. The caller `fac697` and its actual
harness session were persisted as the origin clue.

## Sources

- `/home/li/primary/flows/da1e3f/reports/codex-brief-tools.md`
- `/home/li/primary/Vision/flowNexus.md`
- `/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/`
- `/home/li/.codex/sessions/2026/09/17/rollout-2026-09-17T12-05-01-01a0b08b-1950-7ee1-92e8-0c5562869d29.jsonl`
- `/git/github.com/LiGoldragon/flow`
- `/git/github.com/LiGoldragon/signal-flow`
- `/git/github.com/LiGoldragon/meta-signal-flow`
