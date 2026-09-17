# Message Nexus evidence — fac697

## Installed 0.11.1 input surface

The installed `/nix/store/2yspp3zdfymnml9ff1msdzrdi3bs0q6j-message-0.11.1/bin/message`
was built from `/nix/store/93bgbzas5klix318pknjgb84g1kvp0qs-source` (the source
path recorded by its derivation). That source's `Cargo.lock` pins
`signal-message` 0.8.1 at
`dff3fbf3f9e2cd018f06bcf96a06c8367d3e7f31`. Its generated `Input` enum has
exactly these nine variants:

1. `Submit`
2. `SubmitStamped`
3. `QueryInbox`
4. `AssignAgentIdentity`
5. `BindAgentEndpoint`
6. `QueryAgentRegistry`
7. `QueryThread`
8. `SubscribeThread`
9. `QueryThreads`

Every command below was run against the live ordinary socket. `MESSAGE_BIN`
means the exact store binary above and `MESSAGE_SOCKET` was
`/run/user/1001/message/message.sock`.

```sh
MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'Submit.(fac697-input-probe Send (variant probe) None)'
# SubmissionRejected.StoreRejected

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'SubmitStamped.((fac697-input-probe Send (variant probe stamped) None) External.Owner 1)'
# MessageRequestUnimplemented.(SubmitStamped NotInPrototypeScope)

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'QueryInbox.fac697-input-probe'
# InboxListing.([])

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'AssignAgentIdentity.(fac697-input-probe None None)'
# AgentIdentityAssigned.(fac697-input-probe Seated)

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'BindAgentEndpoint.(nonexistent-fac697 (HarnessSocket /tmp/fac697-probe.sock) 1 1)'
# AgentRegistryRejected.UnknownAgentIdentifier

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'QueryAgentRegistry.ByAgent.fac697-input-probe'
# AgentRegistryListing.([])

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'QueryThread.fac697-input-thread'
# ThreadRejected.UnknownThread

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'SubscribeThread.(fac697-input-thread fac697-input-probe None)'
# ThreadSubscribed.(fac697-input-thread fac697-input-probe)

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'QueryThreads.All'
# ThreadIndexListing.([])
```

These are working parser/wire examples, not nine successful operations. The
comments preserve the witnessed operation result: `Submit` hit the live
store rejection, `SubmitStamped` is explicitly unimplemented, endpoint binding
used an unknown identity intentionally, and the absent thread query returned a
typed refusal. All nine actualized, crossed the live Signal socket, and produced
a typed reply. `ClusterMessage.Peer` and `ClusterMessage.Relay` are payload
variants in the later wire proposal, not top-level inputs accepted by 0.11.1.

## Published Message work

Message `main` is pushed at
`5707f1191bd105c10966d4a640a630bf9a3004b9`. It includes the predecessor typed
`ClusterMessage.Peer` and `ClusterMessage.Relay` validation/delivery work, the
busy-Claude route fix at `ec776b24071f`, canonical `message-nexus` and
`message-meta` executable names (with compatibility names retained), and one
Datom from argv or stdin. `cargo test --workspace --all-targets` passed,
including a busy-Claude queued-delivery fixture.

The current cluster delivery leg still invokes the promoted prompt-relay
adapter from the ordinary `message` process and prints that adapter's JSON
acknowledgment. It does not yet cross the Message Nexus Signal socket or return
the proposed typed `DeliveryRecorded` receipt. Therefore this is published
progress, not a claim that Job 1 is complete.

The source-reviewed gate in `tools/prompt-relay` now accepts `idle` or `busy`
status, including the ordinary `state: blocked` used when Claude is awaiting
the next user turn. It refuses terminal `done`/`concluded`/`killed` lifecycle
states and explicit permission fields such as `waitingFor: permission prompt`.
It re-queries the roster after attaching and verifies the same full session
identity and readiness immediately before the bracketed paste. Its fixture
suite passes with idle, busy, and blocked-waiting-user acceptance plus terminal
and permission refusals. Those primary changes are intentionally left for the
root flow to commit.

## Acceptance send

The attempted one-word peer marker was `NEXUS`, source event
`fac697-acceptance`, addressed to Claude flow `da1e3f`, session short
`da1e3f9d`. The typed header was:

```datom
Peer.{ { fac697 codex-primary } fac697-acceptance /tmp/fac697-marker-body 52b797a276d825aaa28f449f1d35682bd4d271f6455be84e3869cdd7aed2ca03 NEXUS }
```

The first real attempt was refused by the obsolete idle-only gate. The
source-reviewed readiness correction established that this target's
`status: idle, state: blocked` means it is awaiting ordinary user input; real
permission prompts additionally carry `status: waiting` and a permission
`waitingFor` value. The corrected attempt wrote the marker once. The wrapper
CLI then misclassified the full session UUID in the adapter receipt because
its route contained the short ID; that acknowledgment bug is fixed locally and
the event was deliberately not retried.

The transcript witness is
`/home/li/.claude/projects/-home-li-primary/da1e3f9d-857f-49ab-8c6f-3aa0a9db826b.jsonl`,
line 1522: UUID `788e3c96-8248-439c-8f7b-6fc297afda18`, timestamp
`2026-09-17T23:37:00.212Z`. Its user content ends in the exact one-word body
`NEXUS`. This proves the direct cc-daemon PTY mechanism and the requested
recipient transcript acceptance. Its content still includes the interim JSON
provenance wrapper before the blank line, so it is not evidence that the proper
one-Datom Message Nexus wire path is complete.

## Coordination state

Orchestrate locks `1837` (Message implementation/report), `1839` (wire repos),
and `1903` (prompt-relay busy gate/tests) remain owned by flow `fac697` while
the transcript witness and primary commit are unresolved. The predecessor
files named in the brief were absent at their stated direct paths; the two
f55ec8 reports were recovered from the predecessor's nested flow-9993b5
worktree and used. No missing file was silently treated as read.
