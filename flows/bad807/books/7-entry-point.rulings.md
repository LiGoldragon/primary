# «The standard entry point: three actors, one path»: rulings

## Summary

1. `Vision/nexus.md` new "The standard entry point": four actors, main, signal, operation, memory; signal and memory talk only to operation, main only to operation; one entry point builds them and gives out every handle.
2. `Vision/nexus.md` "Actors": Kameo actors are the four of the entry point and their sub-actors; an actor reaches another only through a handle it was given.
3. `nexus/src/entry.rs` new: the part kinds `Signaling`, `Operating`, `Remembering`, the `Nexus` and `Entering` kinds, the private handles and `Admission`, and `nexus::main!`; nexus 0.6.0 with kameo 0.22 and tokio.
4. `chronos` branch `entry-point`: four ethos roots, generated Rust, three hand-written parts on redb, `main` as `nexus::main!(chronos::Chronos);`, compile-failure and socket tests.
5. `Curriculum/skills/vision-nexus.md` line 6: adds the four actors and their edges.
6. `Curriculum/skills/knowledge-nexus.md` after line 13: names the drafted Nexuses that run nowhere.
7. `ethos-zero` generator: emits `Signaling` and `Operating` (one method per operation) with the `perform` dispatch.

## Rulings

1. Which way enforces the edges.
   (a) Typed handles alone, each Nexus wiring its own: 2026-10-04, his comment on «The Nexus», "Signal can only talk to operation".
   (b) The standard entry point, `nexus::main!`, carrying the handles: 2026-09-14, 6cc91b, "make Nexus sort of the only main call"; 2026-10-04, 5ed94b, "standard main flow, like a macro in Rust". The flow's recommendation.
   (c) Generated from ethos by ethos-zero: 2026-09-14, 6cc91b, "a kind becomes a higher-type kind compiler check: an architecture guard basically"; 2026-10-04, 5ed94b, "effective compliance with ethos".
2. Whether the core library is actor-based in name.
   (a) Yes: `MainActor`, `SignalActor`, `OperationActor`, `MemoryActor`: 2026-09-14, e1953c, "the Signal actor, the main Signal actor, or the Nexus actor"; 2026-10-04, "the operation actor".
   (b) No: the part kinds `Signaling`, `Operating`, `Remembering` carry the names, the actors stay inside: 2026-09-14, e1953c, "Maybe we even have to find a better term for that"; 2026-10-04, "whether it is an actor-based language or whether it is different", to be refined after practice.
3. The test subject.
   (a) Chronos, the flow's proposal: 2026-10-04, "one of our non-production-ready ideas".
   (b) agent, the machine-call Nexus: 2026-10-04, "Maybe let's do something useful".
   (c) A running Nexus on a branch, Flow or Orchestrate: 2026-10-04, "like Flow, Message [sic], or Orchestrate, on a branch", then "A toy, I mean".
