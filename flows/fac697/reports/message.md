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

A later bounded success probe used the seated `fac697-input-probe` identity and
a real temporary listener:

```sh
MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'BindAgentEndpoint.(fac697-input-probe (HarnessSocket /tmp/fac697-input-probe.sock) 3261659 62002006)'
# AgentEndpointBound.fac697-input-probe

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'QueryAgentRegistry.ByAgent.fac697-input-probe'
# AgentRegistryListing.([ ... Bound.(HarnessSocket /tmp/fac697-input-probe.sock) ... Pinned.{ 3261659 62002006 } ])

MESSAGE_SOCKET=/run/user/1001/message/message.sock "$MESSAGE_BIN" 'QueryThread.fac697-input-thread'
# ThreadListing.(fac697-input-thread None [fac697-input-probe] [])
```

The temporary listener was stopped, its socket removed, and the probe identity
reseated to clear the endpoint. Its PID and start ticks are a witnessed
ephemeral prerequisite, not reusable values.

These are working parser/wire examples, not nine successful operations. The
comments preserve the witnessed operation result: `Submit` hit the live
store rejection, `SubmitStamped` is explicitly unimplemented, endpoint binding
used an unknown identity intentionally, and the absent thread query returned a
typed refusal. All nine actualized, crossed the live Signal socket, and produced
a typed reply. `ClusterMessage.Peer` and `ClusterMessage.Relay` are payload
variants in the later wire proposal, not top-level inputs accepted by 0.11.1.

## Published Message work

Message `main` is published at
`6751ec128c686e9e5d1cba83025c919d5dd90db8` (remote main has the same tree plus
empty bookkeeping commit `3e0582c25fb83982f7808c86549f94ddb42d42dd`).
`signal-message` main `37c3e5b75b05f86b7dc27198bb4523ccbd495e4b`
owns `Deliver`, `DeliveryRecorded`, and the four receipt kinds. The ordinary
CLI accepts one Datom, actualizes it to Signal, and calls the ordinary socket.
Message Nexus resolves recipients through `signal-flow`
`5334763fe61513f4cd8d58160e411c9e8315d1b9`, persists immutable event identity
and per-target state in the v6 Sema family, and uses native Claude attach or
Codex app-server protocols. The cluster wrapper/prompt-relay CLI bypass and its
extra binaries were removed. `cargo test --workspace --all-targets` passed.

An event's payload fingerprint is global across every target. Peer delivery
requires matching outer/inner event IDs and a SHA-256 over the exact body.
Resolution parks are retryable. Before an external harness write the complete
payload is durably recorded as nonretryable Parked; only a positive harness
acknowledgment promotes it to Accepted, and failure to persist that final
transition returns an error. This avoids automatic duplicates after an
ambiguous timeout. One reliability gap remains: no privileged recovery
operation yet inspects and resolves a nonretryable Parked attempt left by a
crash before or during the harness write. The row and complete payload remain
durable, but require a future transcript-reconciliation/meta retry path; such a
row is not claimed as delivered.

The predecessor prompt-relay readiness correction and its tests were committed
to primary at `d8e8b574`. The final Message delivery does not invoke that tool;
the equivalent readiness decision now comes from Flow Nexus and is rechecked
by Message immediately after the authenticated attach and before the paste.

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
its route contained the short ID; that predecessor acknowledgment bug was
fixed before publication and the event was deliberately not retried.

The transcript witness is
`/home/li/.claude/projects/-home-li-primary/da1e3f9d-857f-49ab-8c6f-3aa0a9db826b.jsonl`,
line 1522: UUID `788e3c96-8248-439c-8f7b-6fc297afda18`, timestamp
`2026-09-17T23:37:00.212Z`. Its user content ends in the exact one-word body
`NEXUS`. This proves the direct cc-daemon PTY mechanism and the requested
recipient transcript acceptance. Its content still includes the interim JSON
provenance wrapper before the blank line, so it is not evidence that the proper
one-Datom Message Nexus wire path is complete.

The proper-path acceptance used the fresh source event
`fac697-signal-acceptance` and one-word body `SIGNAL`. The full ordinary command
was:

```sh
MESSAGE_SOCKET=/run/user/1001/message/message.sock FLOW_SOCKET=/run/user/1001/flow/flow.sock \
  /home/li/.local/bin/message 'Deliver.{ fac697-signal-acceptance Peer.{ { fac697 codex-primary } fac697-signal-acceptance flows/fac697/reports/message.md 8e1a5272bdd1d3e31686395747952c2384871c7f71f73dc660dcd0999f934582 SIGNAL } [ da1e3f ] }'
```

It returned:

```datom
DeliveryRecorded.{ fac697-signal-acceptance [ { da1e3f Accepted } ] }
```

Flow dynamically resolved `da1e3f` as full Claude session
`da1e3f9d-857f-49ab-8c6f-3aa0a9db826b` with control endpoint
`/tmp/cc-daemon-1001/a88e833a/control.sock` and `Ready`, and Message re-resolved
the same identity immediately after attach and before paste. The recipient
transcript witness is the da1e3f JSONL at line 1560, UUID
`a87458dc-3593-4037-a87f-3900a49724c6`, timestamp
`2026-09-18T00:00:06.340Z`. Its user content is exactly the canonical
`Peer.{ ... SIGNAL }` Datom, with no JSON provenance wrapper.

The active service PID at witness time was `3296111`; after the final tracked
Nix build it restarted as PID `3297488`. `/home/li/.local/bin/message`,
`message-meta`, and `message-nexus` now point to
`/nix/store/ngd6pk288arywg5kcjkf4chp01484pvp-message-0.12.0/bin/`. Both
ordinary and meta sockets were recreated; a post-restart typed inbox query
passed. The prior v3 `messenger.sema` and preservation files remain on disk;
the activated 0.12 service uses a fresh v6 store.

## Coordination state

The implementation and wire repos are published and the 0.12 service produced
the typed live receipt above. The predecessor files named in
the brief were absent at their stated direct paths; the two f55ec8 reports
were recovered from the predecessor's nested flow-9993b5 worktree and used.
No missing file was silently treated as read.
