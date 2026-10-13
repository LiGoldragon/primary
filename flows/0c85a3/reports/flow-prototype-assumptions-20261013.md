# Flow prototype: assumptions and measured boundary

Mission: Fable's whole `flows/33752b/reports/mind-flow-mission.md`, living order of 2026-10-13. Astra authors; Field checks and deploys one main Flow/Message cohort through Home. This report is not a passing or deployed receipt.

## Prototype choices where detail is open

- Use local Unix sockets for the first paired Flow/Message prototype; network routing is not required for its first native launch.
- Keep a new explicitly selected Flow store separate from historical stores; do not infer compatibility or migrate old occupants.
- After an unclean Message exit, repair a shared-locked in-memory snapshot for exact Standard2 recognition before permitting the normal engine to open the original; an unknown original stays unchanged.
- Keep uncertain native launch outcomes pending for inspection of the original attempt instead of spawning a second harness.
- Qualify the installed harness, SYSTEM file, model, and actual invoking session/turn at the native launch boundary; a synthetic launch fixture is not the witness.

## Current departures from the vision, not assumed approval

- Flow currently starts from an explicit typed Start and has a configuration-only bootstrap path; this differs from the no-argument, built-in-default Nexus rule.
- Ordinary Message requests are durably queued by Flow; this does not yet prove waking, draining into a native harness, or delivery-event subscription.
- Some launch profile/composition work remains in the CLI and deployed launcher tools rather than wholly in the Nexus.
- Memory remains authored Rust instead of a complete generated Memory ethos; generated Library/Operation/Startup and their pins are preserved during compile reconciliation.
- Process identity and authorization must be judged per operation; the existence of the Message peer guard does not prove all Report/Stop/release paths.
- The retained recovery binary has no connected execution adapter and is not enabled as a service.

## Measured checkpoint

All enumerated Flow and Message branches were incorporated into main with explicit semantic dispositions; none were deleted. Field's successive changed-input builds now compile Flow production library and binary, then refuse test compilation. Exact test-only correction is Flow `e4c268097514bbb75d796ebdf47a0a9826fcc09e`; its checks are pending.

Message `8d44eef5121be3c00050fc67694e10b851e66abf` passed both recognition unit tests but failed the process restart integration because the fixture kills its writer and redb read-only open refuses pending repair. Changed Message `6d0784a16e33f064bf36f9ae82e2eb3b6d4e1b32` adds snapshot recognition and crash/no-mutation regression coverage; checks are pending. Existing restart assertions remain.

No real Flow Start or unified deployment is claimed. Field owns the serial checks and deployment; passing revision and actual behavior will be appended after its receipts.
