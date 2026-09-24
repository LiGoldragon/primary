# HM to Message ordinary dispatch inspection — 2026-09-24

## Scope and ownership

Field Medium `9ddcbc` holds Orchestrate lock `5118`, named
`HackyMessengerMessageOrdinary9ddcbc`, over exactly:

- `/home/li/primary/tools/hacky-messenger/hm.py`
- `/home/li/primary/tools/hacky-messenger/test_hm.py`
- `/home/li/primary/tools/hacky-messenger/README.md`

The latest pre-change commits touching these paths are
`96d48f7dc6b83e6896cefc6c1cec0092112fded5`,
`5fbc42ef0db35874aa86a0a36ee2a91ed56fc3ab`, and
`7408f3d00ffcf8c63661ea8e2858840d41422705`, authored by `li`.
No other current Orchestrate lock names these paths. Lock `3776` remains the
separate CriomOS-home Flow/Message consumer reservation.

## Live prerequisite received from EB

EB reported that Flow was stopped, two authorized stale store files were
removed, and packaged Flow was restarted once at 2026-09-24 09:52:49 CST as
PID 1635310. The fresh store is
`/home/li/.local/state/flow/flow.sema`, birth time
`2026-09-24 09:52:49.804-0600`, inode `52451029`, size `1056768`, SHA-256
`f524772dbfe554b7df8f265d4e7547cda6df590c4514aab4eb5dff3d99030b46`;
PID 1635310 fd 3 holds that path. Both ordinary and owner Flow sockets listen.
The typed current probe `ResolveRecipient.dead00` returned
`RecipientResolutionRejected.UnknownFlow`. This proves the fresh live store and
a current typed resolution result for an unbound fixture; it does not prove a
working binding for an intended recipient.

## Installed ordinary Message contract

The inspected immutable Message source is
`a8c6a924d5d04fbfcbf0a7e2e1b145076d327a53`. It pins ordinary
`signal-message` v4 at
`37c3e5b75b05f86b7dc27198bb4523ccbd495e4b`.

The ordinary CLI accepts exactly one Datom through `MESSAGE_SOCKET`. The
supported route dispatch operation is:

`Query::Deliver(DeliveryRequest { source_event_identifier, cluster_message, target_flows })`

`cluster_message` is `ClusterMessage::Peer` or `ClusterMessage::Relay`.
`Deliver` resolves each target through Flow Nexus, stores the source event and
per-target attempt before invoking the harness adapter, and returns
`Response::DeliveryRecorded`. In this v4 contract each recipient receipt has
only `flow_identifier` and `ReceiptKind`.

- `Accepted` means the harness adapter positively acknowledged transport
  submission. It does not prove presentation, reading, interpretation, or work.
- `Parked` can mean unresolved target or an ambiguous harness outcome. A
  nonretryable in-flight park prevents automatic replay after ambiguity.
- Reusing one source event with different payload conflicts.

`Query::FlowDeliver` is a separate durable inbox/queue operation. Its queue
acceptance is not route transport and cannot be used as the hm-send success
receipt.

At inspection, `message-daemon.service` was active as PID 1599873 since
2026-09-24 09:47:04 CST. Its ExecStart was
`/nix/store/104qsfp8bpp551y7glxc2zsda2axmljm-message-0.12.0/bin/message-daemon`
with configuration `/home/li/.local/state/message/message-daemon.signal`.
PID 1599873 listened on `/run/user/1001/message/message.sock`.
No send, restart, or service mutation was performed.

## Concrete switch gap

The v4 `PeerEnvelope` requires `peer_body_sha256`, and Message sends the full
canonical `ClusterMessage::Peer` Datom to the recipient harness. Therefore an
hm-send switch to ordinary `Deliver` would put a full SHA-256 digest into the
recipient-visible turn. This conflicts with the living's 2026-09-24 rule to
remove hashes and other machine evidence from seat messages. `Relay` also
contains full prompt hashes and does not solve this.

The smallest safe wrapper change is therefore held until the supported
ordinary contract or Message adapter keeps integrity fields in the durable
ledger while presenting a hash-free provenance header and prose body to the
recipient. The eventual switch must remain explicit until its receipt semantics
match native prompt transport; it must use `Deliver`, one target, one stable
source event, treat only `Accepted` as transport submission, hold `Parked`, and
never fall back or retry after uncertainty.

## Landed wrapper correction and proof

The current source change removes the random 32-hex message ID from the
recipient-visible `Machine.Relay` line. The line begins with `machine`, sender
Flow, UTC time, and seat. The unique attempt ID remains in the sender-side
`attempts.jsonl` only. Native Herdr remains the only wrapper transport.

Focused test evidence:

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/hacky-messenger -v`

Result: 32 tests passed. The focused send test proves the visible header has no
32-hex ID, the ledger retains a 32-hex attempt ID, and that ID is absent from
the delivered prompt. `git diff --check` passed.
