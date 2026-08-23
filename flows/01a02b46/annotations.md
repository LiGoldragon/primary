# fix_lojix_boot_ownership

2026-08-23 — The approved single-authority boot contract landed without a
runtime deployment. Lojix `0.19.0` main is
`0105f8d8f18dd91291e0a0fbe828e84ceda65714`: normal `SetBootProfile` and
`ActivateNow` clear EFI `LoaderEntryDefault` and `LoaderEntryOneShot`, while
`ScheduleBootOnce` and bootstrap preserve bootctl's actual current entry as
persistent fallback and take the candidate entry from generated `loader.conf`.
The old generation-number entry synthesis is removed. CriomOS main
`02ac43b193efd7ee542ab1a4d0594c76292edc53` and CriomOS-test-cluster main
`6e34f9e5db7dfa3c13209812b5a4270268a45ff3` pin that producer. Lojix's full
Rust suite passed. The test-cluster direct pin and lock reference passed
format/reference checks; its no-build Nix evaluation made partial progress but
did not return a terminal result to the runner, and its remote-builder
`lojix-deploy-smoke` made no progress within an explicit 45-second bound.
Neither is green evidence. No deployment, activation, reboot, EFI mutation,
or garbage collection was requested.
