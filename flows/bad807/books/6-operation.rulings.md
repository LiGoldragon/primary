# «Operation»: rulings

## Summary

1. `Vision/nexus.md` new "Operation": operation stands between signal and memory, one operation for every effect.
2. `Vision/nexus.md` "Processing is for the effect": each effect done by its operation, each coming to a typed outcome; "The name is open, Apply liked" leaves.
3. `Vision/nexus.md` new "Operations compose": one operation per effect in order; outcomes feed the next and make the response.
4. `Vision/nexus.md` new "The standard entry point": the call order signal, operation, memory, operation, signal; the entry point alone holds memory.
5. `Vision/ethos.md` new "The Operation root": four sections, imports, operations, outcomes, types, with the commented Flow example.
6. `Vision/nexus.md` new "A machine call is an operation": programmed with an ethos spec, corrected against it.
7. `Intent/deterministicWork.md` new: deterministic work is done by code, never by a machine call.
8. `Curriculum/skills/vision-nexus.md` line 6: adds the path, outcomes, entry point, hand-written bodies, deterministic work.
9. `Curriculum/skills/vision-ethos.md` lines 45 to 53: the Operation example gains its comments.
10. `nexus/src/entry.rs` new: `Signaling`, `Remembering`, `Operating` and `Entry`, which alone holds the memory.

## Rulings

1. What the middle part is called.
   (a) operation: 2026-10-02 (91ea9f, typed, "signal, operation, and memory") and 2026-10-04 (5ed94b, "the operation actor/system").
   (b) process, or the Nexus core: 2026-09-13 (024bc7, STT, "the process or Nexus core") and 2026-10-02, earlier the same day (91ea9f, "Maybe we call it the process").
2. Processing as conversion or as effect.
   (a) conversion, TryFrom chains: 2026-08-21 (`vision-raw/mainFunction.md`, STT).
   (b) effect, one operation per effect: 2026-08-26 (f426777b, STT) and 2026-10-02 (91ea9f, typed).
3. Whether operation has its own ethos root.
   (a) no: roots Library, Signal, Sema (`Vision/ethos.md` "Roots", distilled 2026-09-09).
   (b) yes: 2026-09-13 (024bc7, STT, the three layers "described in ethos") and 2026-10-02 (91ea9f, "the actual ethos of the three layers").
4. A standard main.
   (a) wanted: 2026-08-22 (bc05da32), 2026-09-19 (b81560) and 2026-10-04 (5ed94b).
   (b) set aside: 2026-09-10 (fe34eb, "overthinking the whole nexus-core runtime concept").
5. Who writes the operation bodies.
   (a) by hand, the structure enforced: 2026-10-04 (5ed94b) and `Vision/ethos.md` "Kinds are explicit; bodies are hand-written".
   (b) the whole program in ethos within months: 2026-09-25 (e51411) and 2026-09-29 (c64ee3, STT).
6. Whose conversion the entry point's macro generates.
   (a) the macro generates "input selection and conversion boilerplate": 2026-08-22 (bc05da32, typed).
   (b) no text serialization logic in the Nexus: 2026-09-28 (8904b1).
7. An architecture guard.
   (a) refused, as a tool written for one repository: 2026-08-18 (2b34fafa, typed).
   (b) wanted, as a compile-time check through kinds and the entry point: 2026-09-14 (6cc91b) and 2026-10-04 (5ed94b).
