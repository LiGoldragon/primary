# Runtime shutdown checkpoint

This checkpoint was written on 2026-09-10 when the user requested that all
implementation and builders wind down before the server stops. No production
service was stopped, restarted, reconfigured, or queried through its socket.
No protected CriomOS Home path was edited.

## Clean releases

Lojix 1.0.1 is released at
`b8f7a8cc834c90e08918410ea32f28d1b4c6949c`. Its focused Nexus tests passed
3/3, offline-tool tests passed 19/19, workspace check/format/clippy passed, and
the final remote `nix flake check --print-build-logs` exited 0 after evaluating
39 checks including VM behavior. The registry and durable Lojix/Horizon
witness are committed on primary main at
`70d693268006122da55d88756506b3b95a877270`.

The previously released producer and consumer revisions remain recorded in
`reports/release-registry.json`. They are clean releases; the Orchestrate WIP
below is not part of that registry.

## Preserved Orchestrate WIP

- `/git/github.com/LiGoldragon/signal-orchestrate`:
  `flow857335-orchestrate-lifecycle-wip` at
  `e3ea414c624b4431489446b6371f4f05b7cddbe6`. It adds ordinary Configure and
  typed lifecycle receipts, regenerates from authored Ethos, and updates the
  final Datom/Protos/Ethos pins. Local default tests passed 2/2 and Datom tests
  passed 4/4.
- `/git/github.com/LiGoldragon/meta-signal-orchestrate`:
  `flow857335-orchestrate-lifecycle-wip` at
  `eb6df08ef3fa392a4776f475cc145ebe9899c9e1`. It imports the shared ordinary
  configuration, adds privileged reversal and lifecycle receipts, and
  regenerates from authored Ethos. Local default tests passed 1/1 and Datom
  tests passed 2/2. The default test build still reports one unused-import
  warning and no release gates were run.
- `/git/github.com/LiGoldragon/orchestrate`:
  `flow857335-nexus-lifecycle-wip` at
  `cf0dfef298e20e0733f142c3a74a9b16aced7fd9`. This is an intentionally
  unfinished, uncompiled checkpoint. It begins the Nexus 0.1.1 lifecycle state,
  ordinary/meta transition routing, final substrate pins, and qualifier trait
  renames. It is not suitable for main or deployment.

The clean Orchestrate main remains 0.31.0 at
`1bc55af1859e41a7a8310f05c6b3588b8da47a65`. The live
`orchestrate-nexus.service` was left serving that pre-WIP deployment.

## Remaining Orchestrate work

Resume only after reacquiring whole-repository locks for the three paths above.
Continue from the three WIP bookmarks, first compiling and completing the
store lifecycle schema and copy-only historical migration. Then implement the
Kameo-owned effect processor; explicit ordinary/meta socket modes and owner
peer authorization; and `Observe.Locks` as a long-lived subscription that
writes the initial state followed by every successful Lock mutation. The
ordinary CLI must consume that stream. Add isolated zero-argument restart,
marker transition, unauthorized-meta, subscription, no-Datom Nexus graph, and
exact historical archive witnesses. Release the ordinary Signal before the
meta Signal, replace development path dependencies with immutable revisions,
and only then gate and release Orchestrate.

Ethos Zero still lacks its required long-running Nexus, ordinary/meta Signal
contracts, and separate clients. That implementation follows the Orchestrate
closure and must also begin with fresh locks.

## Shutdown state

The only long remote builder started by this subflow, the final Lojix 1.0.1
Nix gate, completed with exit 0 before shutdown. No command or process group
started by this subflow remains active. The live Orchestrate process was not
stopped. After all WIP commits were pushed, locks 1024, 1031, 1033, 1054, 1059,
1064, and 1065 were released. After the other active worker confirmed its WIP
was pushed and its builders were stopped, including Spirit bookmark
`wip-flow857335-spirit-port` at
`5c53df2a94123794c597443a2fdd67bf45a045bd`, the remaining flow-857335 locks
1025, 1026, 1027, 1028, 1029, 1034, 1040, 1043, 1045, 1050, 1051, 1061,
1062, 1063, 1068, and 1069 were released. A final typed observation found no
remaining lock owned by flow 857335.

## Sources

- Tool outputs and repository states observed by `/root/runtime_complete` on
  2026-09-10.
- The three immutable WIP bookmarks and revisions listed above.
- Lojix 1.0.1 `b8f7a8cc834c90e08918410ea32f28d1b4c6949c`.
- Primary evidence revision `70d693268006122da55d88756506b3b95a877270`.
- The typed `Released` and final `Observed.Locks` replies from the live
  Orchestrate service.
