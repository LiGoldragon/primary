# Provenance: software-design skill draft (v3, 2026-08-21)

Maps the draft's doctrine to its ruling sources. v2 supersedes v1
(git history holds v1); written by the Design flow 2b34fafa directly,
after the psyche's 2026-08-21 corrections. v3 (same day) adds the
actors section and the two actor diseases, written by Design flow
bc05da32 from the three actor researches ordered by the psyche
(ActorDataflowDesignSkills, ActorSystemBoundaries,
AgentBuiltActorMachines, all 2026-08-21). Reading choices flagged at
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
| "Write the core as if its coherent inputs already existed; then ask what produces them" — the SICP wishful-thinking and Beck output-tape attributions removed from the skill per the 2026-08-22 history-book ruling; the lineage lives here | MachineAnatomyPriorArt-2026-08-21.md (witnessed) |

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
| Spine original; fifteen projects, seven traditions (survey detail trimmed from the skill per the 2026-08-22 history-book ruling; the finding lives here) | DesignExemplars-Rust (incl. supplement), DesignExemplars-Haskell, MachineAnatomyPriorArt (all 2026-08-21) |
| walrus, cargo, Elm, gleam, Dhall examples | the three exemplar reports (witnessed code) |

## Actors mark the world's concurrency

| Doctrine | Source |
|---|---|
| Actor = thing on the map; the earning properties (state, lifecycle, failure domain, world concurrency, pacing) | ActorSystemBoundaries-2026-08-21.md (convergent criteria; no surveyed source assembles them as one list — the assembly is ours, flagged choice 6) |
| Armstrong 1:1 mapping law (quoted) | ActorSystemBoundaries-2026-08-21.md (witnessed quote) |
| Never for code organization (quoted) | ActorSystemBoundaries-2026-08-21.md (witnessed quote, Elixir language documentation) |
| Arrows never actors; machine pure inside the actor shell (sans-io) | ActorSystemBoundaries-2026-08-21.md three-part assessment + ActorDataflowDesignSkills-2026-08-21.md — flagged (choice 7) |
| Actor read as the machine continued (state = coherent type, handler = conversion) | Designer synthesis — flagged (choice 7) |
| Closed message enum as the interface; effects as data | ActorDataflowBeauty-2026-08-14.md (TEA analysis) + ActorDataflowDesignSkills-2026-08-21.md rules 3 and 8 |
| The eight convergent conventions | ActorDataflowDesignSkills-2026-08-21.md (origin-weighted; stated independently, no cross-citation) |
| Supervision drawn on the map; agents translate, never invent | AgentBuiltActorMachines-2026-08-21.md (practitioner claims, origins noted there) + worldModelBeforeCode.md 2026-08-20 — flagged (choice 8) |
| Granularity is a runtime question (WhatsApp, Orleans) | ActorSystemBoundaries-2026-08-21.md (claims witnessed in their sources) |

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
| Actor costume | ActorSystemBoundaries-2026-08-21.md (Armstrong, Erlang Programming Rules 5.2; Elixir docs) |
| Ask chain | ActorSystemBoundaries-2026-08-21.md (Sypytkowski ask-vs-tell weight; Akka docs timeout-race) |

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
6. **The earning-properties list** — assembled by us from convergent
   criteria across traditions; no surveyed source states it as one
   checklist (the nearest is the Orleans best-practices page). The
   boundaries report also lists a sixth property, distribution /
   location transparency, left out of the draft as not yet load-
   bearing for us.
7. **The actor as the machine continued** (state = coherent type,
   handler = conversion; arrows never actors; pure machine inside
   the actor shell) — Designer synthesis resolving the map-law
   tension (actors persist, but steps are walks); unruled by the
   psyche.
8. **"Agents translate, never invent"** — inference from practitioner
   testimony (claims, not witnessed code); the surveyed public record
   holds no inspectable agent-built actor system, so the positive
   half rests on thinner evidence than the negative half.

Resolved from v1: the passive "capable of being resolved" wording is
gone (active qualifier reading kept per 2026-08-14 Run precedent);
the weak opening line replaced; the machine-equals-TryFrom
overclaim never entered v2 (corrected by the psyche before writing:
"Im not investing into a single form like this").
