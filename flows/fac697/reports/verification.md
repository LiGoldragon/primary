# Independent final verification — fac697

## Published topology

Real remote `main` heads matched the local reviewed heads:

| Repository | Remote | Main SHA |
|---|---|---|
| primary | `git@github.com:LiGoldragon/primary.git` | `82136c7a2b367bdcef1d5adfe4734b353d73046d` |
| message | `git@github.com:LiGoldragon/message.git` | `3e0582c25fb83982f7808c86549f94ddb42d42dd` |
| signal-message | `git@github.com:LiGoldragon/signal-message.git` | `37c3e5b75b05f86b7dc27198bb4523ccbd495e4b` |
| flow | `git@github.com:LiGoldragon/flow.git` | `51cfc00e3c34c7e42739fe42b3dd3715dda5b2a4` |
| signal-flow | `git@github.com:LiGoldragon/signal-flow.git` | `5334763fe61513f4cd8d58160e411c9e8315d1b9` |
| meta-signal-flow | `git@github.com:LiGoldragon/meta-signal-flow.git` | `8ba99d5ff8dc384f5786231956a6f77d07be69b9` |

Message and Flow remain separate Nexuses. `message`/`message-nexus` use the
standalone `signal-message` contract; `flow`/`flow-nexus` use standalone
`signal-flow`; privileged Flow operations use standalone `meta-signal-flow`.
Message resolves recipients through Flow's ordinary typed Signal socket before
crossing the selected Claude or Codex harness protocol.

## Flow witness

Flow formatting, clippy with warnings denied, and its full workspace suite
passed: 16 tests. The installed release binaries matched the reviewed release
artifacts by SHA-256. `flow-nexus.service` is enabled and active/running; its
ordinary and meta sockets are mode `0600`.

Read-only `flow resolve` calls returned `Available/Ready` for the live Claude
flow `da1e3f` and all five protected Codex roles:

- `d9961c` → `01a0aacb-ac84-71a1-88a0-05ed9961ca9d`
- `348e7b` → `01a0a11f-6130-70e2-80b1-796348e7b086`
- `5c2896` → `01a0a132-9be2-76e0-bf0d-57c5c28961ca`
- `2ff1c4` → `01a0a132-9b27-77e2-bcc6-d8b2ff1c456c`
- `098c76` → `01a0a132-9c6f-7de0-b067-1ed098c76c38`

The reviewed implementation imports existing identities through a typed meta
operation, creates a launched child's workspace, injects its Flow environment,
binds restart to both Flow and harness-session identity, bounds Signal frames
at 1 MiB, and accepts a caller-supplied reset idempotency key. Claude
resolution dynamically rechecks the full session in job state and roster,
daemon ownership, lifecycle, permission fields, process and socket liveness,
and endpoint identity. Message repeats that Flow resolution immediately before
its Claude paste.

## Message witness

Message formatting, clippy with warnings denied, and all workspace targets
passed, including 39 tests. `message-daemon.service` now runs the reviewed
`~/.local/bin/message-nexus`; both sockets are present at mode `0600`.
The former v3 store remains intact at
`/home/li/.local/state/message/messenger.sema`; the activated 0.12 service uses
the fresh v6 store `messenger-v6.sema`.

The actual ordinary Signal request was preserved in the sending Codex rollout:

```datom
Deliver.{ fac697-signal-acceptance Peer.{ { fac697 codex-primary } fac697-signal-acceptance flows/fac697/reports/message.md 8e1a5272bdd1d3e31686395747952c2384871c7f71f73dc660dcd0999f934582 SIGNAL } [ da1e3f ] }
```

The live Message reply was:

```datom
DeliveryRecorded.{ fac697-signal-acceptance [ { da1e3f Accepted } ] }
```

The recipient witness is
`/home/li/.claude/projects/-home-li-primary/da1e3f9d-857f-49ab-8c6f-3aa0a9db826b.jsonl`,
line 1560: UUID `a87458dc-3593-4037-a87f-3900a49724c6`, timestamp
`2026-09-18T00:00:06.340Z`. Its user content is exactly the canonical
`Peer.{ ... SIGNAL }` Datom. It contains no interim JSON provenance wrapper.
The v6 Sema file changed immediately before that transcript record, consistent
with the implementation's durable admission followed by acknowledgment
transition.

The final published acknowledgment handling was checked directly. In
`message/src/engine.rs`, lines 215–228, failure of the post-adapter
`replace_nexus_delivery` returns `Response::Error("delivery acknowledgment
could not be persisted")`; it does not return a false `Accepted`. An earlier
review note that the error was ignored applied to an intermediate working diff
and is corrected here.

## Known limits

- Flow's meta socket separates protocol surfaces but is not a security
  boundary between processes with the same Unix UID. Caller provenance still
  relies on non-cryptographic harness environment/session conventions. Both
  limits are documented by Flow.
- Message persists a harness attempt as nonretryable `Parked` before the
  external write, preventing automatic duplicate delivery after an ambiguous
  timeout. A crash before or during that write can leave the payload durable
  but parked indefinitely because no transcript-reconciliation/meta-retry
  operation exists yet. This is a reliability follow-up; it did not affect the
  witnessed acceptance, and such a row is not reported as delivered.
- The full historical transcript extraction/archive request remains pending
  corpus scope. The extractor, permanent live-session protections, one Luna
  smoke extraction, and one hash-verified stale archive are complete; bulk
  processing was deliberately not claimed complete.

At report creation, primary had two external working-tree changes already in
progress: added `flows/1ac573/handoff.md` and modified
`flows/fac697/reports/message.md`. This report did not alter either path.
