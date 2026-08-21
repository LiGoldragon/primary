# Provenance: software-design skill draft (v2, 2026-08-21)

Maps the draft's doctrine to its ruling sources. v2 supersedes v1
(git history holds v1); written by the Design flow 2b34fafa directly,
after the psyche's 2026-08-21 corrections. Reading choices flagged at
the end.

## The map comes first

| Doctrine | Source |
|---|---|
| World model / ontology / anatomy / map before code; checklist = already failed | worldModelBeforeCode.md 2026-08-20 (verbatim ground) |
| Map of the world, not the process; steps are walks; process-named types excluded | worldModelBeforeCode.md 2026-08-20 + importResolutionWorldMap-2026-08-21.md — flagged (choice 1) |
| Destination form: the Ethos interface file, written though unrunnable | worldModelBeforeCode.md 2026-08-21 ("yes, except that it isnt ready to use yet") |

## The three-part machine

| Doctrine | Source |
|---|---|
| agglomerate → create coherent → convert onward | machineAnatomy.md 2026-08-21 (verbatim: "agglomerate multiple types -> create a coherent type -> convert it to another type") |
| The shape is the law, not one spelling; method-body accumulation counts | machineAnatomy.md 2026-08-21 ("thats just one form of it... Im not investing into a single form") |
| Fractal; outer coherent output = inner coherent input; unix output innermost | machineAnatomy.md 2026-08-21 (3-part refinement statement) |
| Typed string blocks at the bottom (ImplString etc.) "if we want to be very correct" | machineAnatomy.md 2026-08-21 (verbatim) |
| Executable special case: OS forces the pre-output type | machineAnatomy.md 2026-08-21 (verbatim) |
| Emission reviewable in one place, under one trait; never sprawled | machineAnatomy.md 2026-08-21 (four-part statement, this clause carried forward) |
| GCC reach-back, LLVM only-interface, MIR centralized quotes | MachineAnatomyPriorArt-2026-08-21.md (witnessed quotes) |

## Backwards from the want

| Doctrine | Source |
|---|---|
| Demand-driven; work backwards; the demand chain is the type list | machineAnatomy.md 2026-08-21 ("we know what's going to come out of it...") + worldModelBeforeCode.md 2026-08-21 ("everything is demand-driven") |
| SICP wishful thinking; Beck output tape | MachineAnatomyPriorArt-2026-08-21.md (witnessed) |

## Types first; contents before behavior

| Doctrine | Source |
|---|---|
| Types first (quoted block) | traitsAsCapabilities.md 2026-08-13 |
| Turn every logical aspect into a type | protosIsTheSharedStyle.md 2026-08-18 |
| Contents before behavior; a table has, it does not do | inferred sequencing — flagged (choice 2) |
| Two things make a nameable third | mainFunction.md 2026-08-21 |
| logos example | DesignExemplars-Rust-2026-08-21.md §10 |

## Capabilities sit on their subjects

| Doctrine | Source |
|---|---|
| Every method under a trait; comprehension surface | psyche/Intent/mandatoryTraits.md |
| Placement law (positive form) | traitsAsCapabilities.md 2026-08-20 — flagged (choice 3) |
| Costume fingerprint (quoted) | importResolution.md / traitsAsCapabilities.md 2026-08-20 |
| Honest boundary (spans, callbacks, payloads); creation exempt | CostumeTraitFingerprint-2026-08-20.md + CreateTraitCrateSearch-2026-08-21.md — flagged (choice 4) |
| Direction pairs (quoted) | traitsAsCapabilities.md 2026-08-18 |
| Fragmentation | rustComponentArchitecture.md 2026-08-17, 2026-08-19 |
| Infinitive verb names; qualifier reading | traitsAsCapabilities.md 2026-08-21 (ruled), 2026-08-14 |
| syn/serde examples | DesignExemplars-Rust-2026-08-21.md §2, §8 |

## The spine is conversions

| Doctrine | Source |
|---|---|
| From/TryFrom, never Into; demand-driven reason | worldModelBeforeCode.md 2026-08-21 (verbatim) + mainFunction.md 2026-08-21 |
| Tuple inputs; nothing else to make | worldModelBeforeCode.md 2026-08-21 ("it would just be TryFrom") + assembly.md 2026-08-21 |
| Consume by value; no references into inputs; clone is the only doubling | assembly.md 2026-08-21 (memory direction) |
| Main as table of contents; schema between the lines (quoted) | mainFunction.md 2026-08-21 |
| Main example chain (Registry/AssemblyFile/ResolvedAssembly/AssembledRust) | assembly.md + mainFunction.md 2026-08-21. `ResolvedAssembly::try_from((…))` per the TryFrom dissolution; `rust.write()`'s exact form undesigned — flagged (choice 5) |
| Spine original; fifteen projects, seven traditions | DesignExemplars-Rust (incl. supplement), DesignExemplars-Haskell, MachineAnatomyPriorArt (all 2026-08-21) |
| walrus, cargo, Elm, gleam, Dhall examples | the three exemplar reports (witnessed code) |

## Names tell the truth

| Doctrine | Source |
|---|---|
| Name true at the moment of existence; AssembledRust | mainFunction.md 2026-08-21 (verbatim) |
| Extension down to ImplString | machineAnatomy.md 2026-08-21 |

## The diseases

| Disease | Source |
|---|---|
| Service object (bat) | DesignExemplars-Rust-2026-08-21.md §12 |
| Sprawled emission (bat, ruff, GCC) | DesignExemplars-Rust supplement + MachineAnatomyPriorArt |
| Costume trait | traitsAsCapabilities.md 2026-08-20 + CostumeTraitFingerprint |
| Placeholder traits | rustComponentArchitecture.md 2026-08-19 |
| Schema between the lines | mainFunction.md 2026-08-21 + bat main (report §12) |

## Reading choices flagged

1. **"Steps are walks... a service is a step dressed as a thing"** —
   agent formulation from the approved world map; not psyche-verbatim.
2. **"Contents before behavior"** as an explicit step — the sequencing
   is observed in the worked example; no psyche statement in those
   words.
3. **The placement law's positive form** ("placed on the type that
   contains its subject") — the psyche's words are the negative
   ("then it's not resolvable"); positive form is interpretation.
4. **The honest boundary + creation exemption** — research-derived,
   unruled by the psyche.
5. **`rust.write()` in the main example** — the emission call's exact
   form (inherent method vs a trait) is undesigned; the line stands
   as a placeholder for the output machine.

Resolved from v1: the passive "capable of being resolved" wording is
gone (active qualifier reading kept per 2026-08-14 Run precedent);
the weak opening line replaced; the machine-equals-TryFrom
overclaim never entered v2 (corrected by the psyche before writing:
"Im not investing into a single form like this").
