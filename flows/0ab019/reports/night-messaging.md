# Night messaging POC

This bounded writer (`f72ab7`, native child thread
`01a0bca2-56da-7ac2-9d52-205f72ab7ecc`) converted the isolated Flow CLI to a
single inline compiled Datom query. The pushed candidate is Flow commit
`e387576f` on `night-messaging-0ab019`; its origin bookmark was fetched and
observed at that same commit. It starts from the verified Flow `main`/
`main@git` `61d765e4`.

`flow 'ResolveRecipient.fac697'` parses to the typed Flow Signal query.
Multiple arguments, the prior `flow start codex-medium` form, and `--help` are
rejected. The binary reads only process arguments: it has no stdin parser and
does not silently retain the prior positional grammar. The complete query now
carries its origin fields. This candidate therefore does not yet implement a
convenience `Start`/`Ensure` operation that independently stamps the invoking
OS/process identity, nor a duplicate guard.

The first bounded remote Nix gate found the expected source failure after the
new parser attempted to stringify `datom_codec::Error`; that error is
structural and does not implement `Display`. The failure stdout and `exit=1`
are retained as `night-messaging-flow-cli-build-attempt1.{stdout,exit}`. The
repair textualizes the error through its Datom representation. A second
foreground Python-supervised Nix build, bounded to 20 minutes with
`--option max-jobs 0 --option fallback false`, exited `0`. Its combined stdout
and exit receipt are `night-messaging-flow-cli-build.{stdout,exit}`. The log
records the remote result copied from
`ssh-ng://nix-ssh@prometheus.goldragon.criome`; the Flow workspace suite
passed, including the new parser acceptance and legacy/flag rejection tests.

Two follow-on isolated workspaces are reserved but deliberately unchanged:
`/home/li/wt/github.com/LiGoldragon/signal-flow/night-messaging-0ab019`
(lock 2862) and
`/home/li/wt/github.com/LiGoldragon/message/night-messaging-0ab019` (lock
2864). The actual current Message source already has typed `Submit`,
`SubmitStamped`, `FlowDeliver`, `FlowAnnounceIdle`, `Deliver`, durable receipt
queries, and agent registry operations. Its Flow delivery is a durable park of
a typed envelope followed by an idle-time compact landing receipt. Receipt
grades therefore remain bounded: `Accepted`, `TranscriptWitnessed`, `Parked`,
and `FileOnly` do not prove a task completed.

The requested request-ID lifecycle (status, detail, requester message,
completion) requires new `signal-flow` vocabulary. That repository checks its
generated Rust source against `ethos/signal.ethos` in `build.rs`. Local source
generation is prohibited for this run, while a remote Nix build validates a
checked-out source and does not return generated edits. The next integration
step therefore needs a Field-authorized remote generation-and-return route (or
an already generated contract change) before a sound Signal change can be
written. No untyped text has been classified as human, no native-main launch,
Flow registration, route binding, successor relay, or deployment was claimed.

## Sources

- `flows/b81560/vision/operational-flowDatomCLIAndSignalLibrary.md`
- `flows/f38926/vision/subflows.md`
- `flows/b81560/vision/operational-refreshOutboxAndMessageChannels.md`
- Flow `README.md`, `crates/flow/src/main.rs`, and remote Nix receipts named above
- Message `src/flow_delivery.rs`, `src/nexus_delivery.rs`, and `signal-message` `ethos/signal.ethos`
