# High-Level View: Software-Design and Nexus Skills Against Datom and Ethos-Monolith

Synthesis by flow cff271af, 2026-08-22, from this flow's three
acquisition reports. Quotes are the psyche's verbatim words; source
paths are in the underlying reports.

## The vision, briefly

Traits are the comprehension surface — the psyche reads traits and
main types, never all the code (Intent, mandatoryTraits). Types come
first; trait/types design is ontology in code; the map — destined to
be the Ethos interface file — precedes any body. Every machine is the
3-part fractal: agglomerate multiple types → create a coherent type →
convert it onward, demand-driven, designed backwards from the want,
with From/TryFrom as the spine and main as a few lines tying a
strictly typed datom input through the chain. Everything built is a
Nexus: a vertex in a graph, at least two sockets, one CLI per socket,
pure binary signal only. Ethos will eventually replace everything;
ethos-monolith is the bootstrap that commits Ethos straight to Rust
so writing and reading ethos and datom can start as soon as possible.

## Settled ground

- **Nexus vocabulary and architecture** — fully ruled (e06e4c07,
  2026-08-19). The nexus and nexus-rationale skills are authored,
  deployed, and in sync with their sources.
- **Software-design doctrines** — settled across
  worldModelBeforeCode, machineAnatomy, traitsAsCapabilities,
  assembly, mainFunction: map before code; steps are walks;
  process-named types off the map; the 3-part machine ("thats just
  one form of it… Im not investing into a single form"); types
  first; costume-trait fingerprint ("if the type needs a 'name' to
  resove the import, then it's not resolvable"); direction pairs
  never share a type; infinitive verb trait names; From over Into
  ("everything is demand-driven"); main's input arriving as a
  strictly typed datom object (the mainFunction.md sentence quoting
  this is agent-constructed — actual typed words: "I dont see the
  arg input. where is datom coming from?"; see the flow log,
  2026-08-22).
- **Skill overlap** — ruled ignorable for now: "dont worry about the
  skill overlap for now. we'll probably end up merging them."
  (skillDesigning, 2026-08-22).
- **Skill craft rulings** — "this is a skill not a history book";
  "a toy is not a good example"; "old code is at most inspiration
  for that map."

## Built reality

| Artifact | State |
|---|---|
| software-design skill | Does not exist anywhere. Draft v3 (123 lines, `reports/SkillDrafts/softwareDesign/draft.md`) awaits psyche re-review; nine reading choices unruled. |
| nexus + nexus-rationale skills | Authored in Curriculum, deployed, bodies match sources. |
| datom | v0.1.0, builds, complete for scope. Deferred: structured string meaning (bead primary-xqb.8.5); dot-containing map keys (pending ruling). |
| ethos-monolith | v0.2.0, library. Emission boundary types and the Interface fixture dialect complete and tested. The central generator — reading `.ethos`, writing signal.rs/nexus.rs/sema.rs — declared "a later phase", unbuilt. |

## The gap map

1. **Ethos-monolith's shape.** The psyche named it a daemon
   (2026-08-14: "it's going to be a daemon also… So we can think of
   it as more of a monolith… an incremental implementation slash
   bootstrap process"). The built thing is a generator library whose
   consumers commit emitted Rust and never depend on it at runtime.
   The 2026-08-19 ruling says what was not built as a Nexus is
   rewritten. Whether the library phase is legitimate bootstrap or
   already owes its Nexus shape is a fork for the psyche.
2. **The generator has no map.** The central purpose of
   ethos-monolith is unbuilt, and no Ethos-interface map of the
   generator machine itself exists in the record. By the settled
   doctrine, that map is the next design artifact, before any
   generator body.
3. **Universal nexus traits** — "the basic ontology of an
   actor/dataflow software system" — ordered in e06e4c07, untouched
   since. Signal and sema are to be compared against this map once
   designed. The floated nexus repo as its home is "a possibility
   under discussion."
4. **Sema.** Called "way more important than nexus" (operational
   editing yields database migrations), wanted authored in ethos —
   yet its trait surface and interface are almost entirely
   undesigned. The largest stated-importance/design-attention gap.
5. **Actor standards.** Kameo confirmed; "I just havent designed the
   standards of use"; "Distrust it all, including our fork." A
   dedicated flow is wanted and does not yet exist.
6. **The software-design skill's nine unruled choices** (from the
   draft's provenance), plus the standing 2b34fafa forks
   (ResolvedAssembly fallibility, resolved thing name,
   ImportReference locality, datom specs and homes, `.es` extension,
   colon tension) and 5c8be3ca leftovers.

## Proposed sequencing (proposal only; the psyche rules)

1. Rule the software-design draft's nine choices; author the skill
   into Curriculum and deploy (or hold for the merge with nexus).
2. Rule ethos-monolith's shape (bootstrap library now vs Nexus
   design now); either way, draw the generator's map as the Ethos
   interface — the protocol's second full exercise after
   import-resolution.
3. Design universal nexus traits with datom and ethos-monolith as
   the two concrete machines held against the map.
4. Engage sema's design, or explicitly defer it again.
5. Datom's two deferrals ride along when their subjects surface.

Realization of any ruled design goes to a codex flow via crafted
prompts (prompt-crafting skill), not done here.

## Sources

- `flows/cff271af/reports/psycheOnSoftwareDesignAndNexus.md` (own
  subflow; verbatim psyche words with paths)
- `flows/cff271af/reports/priorFlowStateOnSkillsAndMachines.md` (own
  subflow; flow-state and rulings with paths)
- `flows/cff271af/reports/currentArtifactsSurvey.md` (own subflow;
  witnessed artifact state, methods recorded)
- Flows: e06e4c07, 15b67974, 2b34fafa, 5c8be3ca, b7465e71 (via the
  above)
