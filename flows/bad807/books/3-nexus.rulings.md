# The Nexus: rulings

Summary of the proposals in `3-nexus.md`:

- 1 `Vision/nexus.md` new Three parts and one path: Signal, Operation, Memory; signal reaches memory only through operation.
- 2 `Vision/nexus.md` new The standard entry point: one macro writes every `main` and owns the path.
- 3 `Vision/nexus.md` Library and daemon: the nexus library defines the part kinds and keeps them apart at compile time.
- 4 `Vision/nexus.md` Signal only: a Nexus never handles text; every text form is made in a CLI or an interface.
- 5 `Vision/nexus.md` Why everything is a Nexus: every runtime component; libraries stay libraries.
- 6 `Vision/nexus.md` new An operation may be a machine call, programmed with an ethos spec and corrected against it.
- 7 `Vision/nexus.md` new Layers: four layers of authority, held by one Nexus, reach following layer.
- 8 `Curriculum/skills/vision-nexus.md` line 6: adds the path and the one-line `nexus::main!`.
- 9, 10 `nexus/ethos/nexus.ethos` and `nexus/src/entry.rs`, new: the core library's types, part kinds and entry macro.
- 11 `flow/crates/flow-nexus/src/main.rs` and `store.rs:673`: Flow's main becomes `nexus::main!`, its store takes no Query.
- 12 `Curriculum/skills/knowledge-nexus.md` line 8: the versions measured 2026-10-04 and the entry-point status.

## Rulings

1. The middle part's name.
   (a) Operation: 2026-10-02, 91ea9f; 2026-10-04, 5ed94b.
   (b) Process, or the Nexus core: 2026-09-13, 024bc7; 2026-10-02, 91ea9f (earlier the same day).
2. The keeping part's name.
   (a) Memory, with Sema freed for the meaning language: 2026-09-26, b7ba00; 2026-09-28, 8904b1; 2026-10-02, 91ea9f.
   (b) Sema, the database engine of a Nexus: 2026-09-10, fe34eb; `Vision/sema.md`.
3. What Nexus names.
   (a) The whole long-running component: 2026-08-19, e06e4c07; 2026-09-10, fe34eb; `Vision/nexus.md`, approved 2026-09-11.
   (b) The core inside it, the whole being a metaNexus: 2026-09-14, 6cc91b and e1953c.
4. The nexus core language.
   (a) Set aside, signal and memory types being enough: 2026-09-10, fe34eb.
   (b) Reintroduced, the core described in ethos: 2026-09-13, 024bc7; 2026-09-14, 6cc91b.
5. Everything a Nexus, and its limits.
   (a) Every runtime component is a Nexus, libraries excepted: 2026-08-19, e06e4c07; 2026-08-22, cff271af; 2026-08-26, b675f3d9.
   (b) Some tools start as a plain server or a Clojure tool: 2026-08-28, 01a047d2; 2026-09-29, 6f51ad (notion).
6. An architecture guard.
   (a) A guard written for one repository is foolish: 2026-08-18, 2b34fafa.
   (b) The kinds and the entry point are the guard: 2026-09-14, 6cc91b; 2026-10-04, 5ed94b.
7. What the entry macro converts.
   (a) It takes a datom-derived type and writes the input conversion: 2026-08-22, bc05da32.
   (b) No datom in a Nexus; conversion lives in the CLI: 2026-10-03, edf227.
8. The messaging Nexus's name.
   (a) Message: 2026-09-17, da1e3f.
   (b) Messenger: 2026-09-25, e51411.
9. Layers of authority: three or four.
   (a) Three, Primary, Secondary, Tertiary: 2026-09-14, 6cc91b.
   (b) Four, with Quaternary: 2026-09-26, e167d8; 2026-09-27, 5ac3a3.
10. Layers of ethos: three or four.
    (a) Three specifications, one per part: 2026-10-02, 91ea9f.
    (b) Four roots, Library beside the three parts: 2026-09-09, 564f55; ethos-zero 16.0.0.
11. Which Nexus holds a flow's layer.
    (a) Persona: 2026-09-14, 6cc91b; 2026-09-16, f55ec8.
    (b) Flow: 2026-09-16, f55ec8.
