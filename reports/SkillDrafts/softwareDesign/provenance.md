# Provenance: software-design skill draft

## v4 (2026-08-23)

v4 merges the nexus skill into software-design per psyche ruling
(flows/cff271af/vision/skillDesigning.md 2026-08-22/23): "we design
everything using a nexus going forward (the runtime part of course;
libraries are still needed sometimes like with datom)." Seven-section
anatomy adopted; all nine v3 flagged choices carry forward.

### What merged from where

- v3's "Backwards from the want" and "Types first; contents before
  behavior" -> section 1 (The want and the map).
- v3's "The three-part machine", "The spine is conversions", and
  "Names tell the truth" -> section 2 (The machine).
- v3's "Capabilities sit on their subjects" + the nexus skill's
  "Traits first" and "No free functions" -> section 3 (Traits),
  deduplicated. Nexus-specific scoping ("of a Nexus") generalized.
- The nexus skill's remaining sections (The Nexus, The daemon,
  Signal, The CLIs, The wire type repos, How nexuses fit together)
  -> section 4 (The Nexus), largely intact. Minor modality
  adjustments per ruling (c): "it never guesses" -> "it does not
  guess"; "never the Nexus's" -> "not the Nexus's"; "never appears"
  -> "does not appear."
- New section 5 (Libraries) per psyche direction: substrate
  libraries (protos, datom), trait libraries, wire vocabulary repos,
  engine libraries (sema-engine), dividing line.
- v3's "Actors mark the world's concurrency" -> section 6 (Actors),
  carried forward. "The conversion arrows are never actors" softened
  to "are not actors" per ruling (c). "Never for code organization"
  softened to "Not for code organization" (the Elixir quote within
  preserves its original wording).
- v3's "The diseases, named" -> section 7, carried forward. "never
  appear" -> "do not appear" in the schema-between-the-lines entry.
- v3's "The worked ground" -> dropped (it referenced a specific
  design exercise, not doctrine).
- Opening line: "tissue" -> "code" (no metaphors per skill-craft
  ruling); "the Nexus as the runtime shape" added.

### Rulings incorporated (2026-08-22/23, flow cff271af)

**(a) Tuple / struct / parameter rules** (tuples.md 2026-08-22).
Three lines replacing v3's "Multi-input creation is TryFrom on a
tuple" (v3 line 154):
- "What a trait consumes or yields is a named type; a tuple in a
  trait signature is a struct not yet named." -> section 3, Names
  and form.
- "A struct with several fields names its fields -- the multi-field
  tuple struct is refused. The newtype is allowed: its single unnamed
  field is technically a tuple form, the only one permitted." ->
  section 2, Conversions.
- "A long parameter list is a type not yet named -- often the
  method's missing owner." -> section 3, Names and form.
Sources: "tuples are a form of un-specification" (verbatim); "the
newtype is allowed. the fact that its a tuple is unfortunate for us,
so it would have to be mentionned in case" (verbatim); "do we have
to allow those? I really dont like tuples" (verbatim). All
tuples.md 2026-08-22.

**(b) Multi-input creation through named agglomerate.** Replaces
v3's TryFrom<(tuple)> pattern. The exemplar pair (Registry +
AssemblyFile -> ResolvedAssembly) has no ruled name for its input
agglomerate type. The code example marks the gap with
`/* agglomerate */`. Source: "don't we have a rule against tuples,
as they represent poorly specified struct?" (verbatim, tuples.md
2026-08-22).

**(c) From over Into: preference, not prohibition.** v3's "never
Into" (v3 line 149) removed; v4 reads "From is preferred." Source:
"I didn't really have that strong of an opinion on this" and "never
is a very strong word" (distillation.md 2026-08-22). Applied
broadly: modality not strengthened beyond what the psyche stated.

**(d) Main's input line.** Main begins at the typed input arriving
as datom. The psyche's actual words: "I dont see the arg input.
where is datom coming from?" (bc05da32 transcript L706; the
mainFunction.md "strictly typed object" phrasing is agent-
constructed, not psyche-verbatim). `Input` as a type name and the
datom's carrier remain undesigned.

**(e) "Manifest" is dead as a name.** Registry (index of sources)
and assembly file (one possible output), both Datom;
ResolvedAssembly is the assembled source. No "manifest" appears in
the skill text. Source: "what manifest? There is no more manifest.
This vision is stale" (distillation.md 2026-08-22).

### Naming debts

- **"the map"** -- the psyche flagged the term as "very vague" and
  "overloaded" (tuples.md 2026-08-22), accepted "for now"
  (skillDesigning.md 2026-08-23). Debt stands.
- **The agglomerate type for (Registry, AssemblyFile) ->
  ResolvedAssembly** -- no ruled name. The code example marks the
  gap with `/* agglomerate */`.

### Skill-craft rulings applied

- "this is a skill not a history book" -- attribution and narration
  in provenance only.
- "a toy is not a good example" -- examples are witnessed code.
- Brutal minimalism.
- Rules as plain sentences, no metaphors ("grain" rejected as
  unclear, tuples.md 2026-08-22).
- Modality not strengthened: no "never"/"always" unless the psyche
  said it (distillation.md 2026-08-22).
- Research into established formulations of the unusual ideas
  authorized (skillDesigning.md 2026-08-23) but not performed in
  this version -- noted for a future pass.

### Flagged choices (v3 choices carried forward; actors section status)

1. **"Steps are walks" agent formulation** -- agent-coined from the
   approved world map; not psyche-verbatim.
2. **"Contents before behavior" as explicit step** -- agent inference
   from the worked example; no psyche statement in those words.
3. **Placement law's positive form** -- agent interpretation of the
   psyche's negative.
4. **Honest boundary + creation exemption** -- research-derived,
   unruled.
5. **`rust.write()` in the main example** -- emission call's exact
   form still undesigned.
6. **Earning-properties list for actors** -- agent assembly from
   convergent criteria; no source states them as one checklist.
7. **Actor-as-machine synthesis** -- unruled by the psyche. The
   actors section is NOT yet green'd; the actor-as-machine synthesis
   is unruled. The skill text stays clean; this flag is provenance
   only.
8. **"Agents translate, never invent"** -- positive half rests on
   thinner evidence than the negative.
9. **Input line in main** -- `Input`'s name and the datom's carrier
   still undesigned.

## v3 source tables (2026-08-21/22)

These tables document the per-line sources for doctrine carried into
v4. Section names are v3's; v4's section mapping is in the "What
merged from where" entry above.

### The map comes first

| Doctrine | Source |
|---|---|
| World model / ontology / anatomy / map before code; checklist = already failed | worldModelBeforeCode.md 2026-08-20 (verbatim ground) |
| Map of the world, not the process; steps are walks; process-named types excluded | worldModelBeforeCode.md 2026-08-20 + importResolutionWorldMap-2026-08-21.md -- flagged (choice 1) |
| Destination form: the Ethos interface file, written though unrunnable | worldModelBeforeCode.md 2026-08-21 ("yes, except that it isnt ready to use yet") |

### The three-part machine

| Doctrine | Source |
|---|---|
| agglomerate -> create coherent -> convert onward | machineAnatomy.md 2026-08-21 (verbatim: "agglomerate multiple types -> create a coherent type -> convert it to another type") |
| The shape is the law, not one spelling; method-body accumulation counts | machineAnatomy.md 2026-08-21 ("thats just one form of it... Im not investing into a single form") |
| Fractal; outer coherent output = inner coherent input; unix output innermost | machineAnatomy.md 2026-08-21 (3-part refinement statement) |
| Typed string blocks at the bottom (ImplString etc.) "if we want to be very correct" | machineAnatomy.md 2026-08-21 (verbatim) |
| Executable special case: OS forces the pre-output type | machineAnatomy.md 2026-08-21 (verbatim) |
| Emission reviewable in one place, under one trait; not sprawled | machineAnatomy.md 2026-08-21 (four-part statement, this clause carried forward) |
| GCC reach-back, LLVM only-interface, MIR centralized quotes | MachineAnatomyPriorArt-2026-08-21.md (witnessed quotes) |

### Backwards from the want

| Doctrine | Source |
|---|---|
| Demand-driven; work backwards; the demand chain is the type list | machineAnatomy.md 2026-08-21 ("we know what's going to come out of it...") + worldModelBeforeCode.md 2026-08-21 ("everything is demand-driven") |
| "Write the core as if its coherent inputs already existed; then ask what produces them" -- the SICP wishful-thinking and Beck output-tape attributions removed from the skill per the 2026-08-22 history-book ruling; the lineage lives here | MachineAnatomyPriorArt-2026-08-21.md (witnessed) |

### Types first; contents before behavior

| Doctrine | Source |
|---|---|
| Types first (quoted block) | traitsAsCapabilities.md 2026-08-13 |
| Turn every logical aspect into a type | protosIsTheSharedStyle.md 2026-08-18 |
| Contents before behavior; a table has, it does not do | inferred sequencing -- flagged (choice 2) |
| Two things make a nameable third | mainFunction.md 2026-08-21 |
| Lexer-crate example CUT 2026-08-22 ("cut the bad example") | DesignExemplars-Rust-2026-08-21.md incl. 2026-08-22 supplement |

### Capabilities sit on their subjects

| Doctrine | Source |
|---|---|
| Every method under a trait; comprehension surface | psyche/Intent/mandatoryTraits.md |
| Placement law (positive form) | traitsAsCapabilities.md 2026-08-20 -- flagged (choice 3) |
| Costume fingerprint (quoted) | importResolution.md / traitsAsCapabilities.md 2026-08-20 |
| Honest boundary (spans, callbacks, payloads); creation exempt | CostumeTraitFingerprint-2026-08-20.md + CreateTraitCrateSearch-2026-08-21.md -- flagged (choice 4) |
| Direction pairs (quoted) | traitsAsCapabilities.md 2026-08-18 |
| Fragmentation | rustComponentArchitecture.md 2026-08-17, 2026-08-19 |
| Infinitive verb names; qualifier reading | traitsAsCapabilities.md 2026-08-21 (ruled), 2026-08-14 |
| serde example (syn File cut 2026-08-22) | DesignExemplars-Rust-2026-08-21.md |

### The spine is conversions

| Doctrine | Source |
|---|---|
| From/TryFrom; From preferred (v3 "never Into" removed in v4) | worldModelBeforeCode.md 2026-08-21 (verbatim) + mainFunction.md 2026-08-21; modality corrected per distillation.md 2026-08-22 |
| Named agglomerate inputs (v4; replaces v3 tuple inputs) | tuples.md 2026-08-22 (psyche ruling) |
| Consume by value; no references into inputs; clone is the only doubling | assembly.md 2026-08-21 (memory direction) |
| Main as table of contents; schema between the lines (quoted) | mainFunction.md 2026-08-21 |
| Main example chain (Input/Registry/AssemblyFile/ResolvedAssembly/AssembledRust) | assembly.md + mainFunction.md 2026-08-21; input line per mainFunction.md 2026-08-22. `ResolvedAssembly::try_from(/* agglomerate */)` per tuple dissolution; `rust.write()`'s exact form undesigned -- flagged (choice 5); `Input`'s name and the datom's carrier undesigned -- flagged (choice 9); agglomerate type name undesigned -- naming debt |
| Input's type = the interface's root enum; configuration from the datom's shape | interfaceRootEnumerators.md 2026-08-07 + 2026-08-22 |
| Spine original; surveyed projects | DesignExemplars-Rust, DesignExemplars-Haskell, MachineAnatomyPriorArt (all 2026-08-21) |
| walrus, cargo, Elm, gleam, Dhall examples | the three exemplar reports (witnessed code) |

### Nexus sections (new in v4)

| Doctrine | Source |
|---|---|
| All nexus sections (The Nexus, The daemon, Signal, The CLIs, The wire type repos, How nexuses fit together) | Authored nexus skill: /git/github.com/LiGoldragon/Curriculum/skills/nexus.md (deployed, psyche-approved) |
| Merge direction: nexus INTO software-design | skillDesigning.md 2026-08-22 (verbatim: "I think nexus becomes software-design") |
| "The runtime shape of everything we design is a Nexus" -- framing line | Agent formulation from the psyche's "we design everything using a nexus going forward (the runtime part of course)" |

### Libraries (new in v4)

| Doctrine | Source |
|---|---|
| Libraries as a category; datom named; trait libraries suggested | skillDesigning.md 2026-08-22 (verbatim: "libraries are still needed sometimes like with datom, and maybe others you can name (trait libraries)") |
| Substrate libraries (protos, datom) | Agent categorization from existing repos |
| Wire vocabulary repos (signal-<nexus>, meta-signal-<nexus>) | Nexus skill's wire type repos section (already described there) |
| Engine libraries (sema-engine) | Agent categorization from existing repos |
| Dividing line: libraries = vocabulary/substrate; runtime authority = Nexus only | Agent synthesis of the psyche's "the runtime part of course" |

### Actors mark the world's concurrency

| Doctrine | Source |
|---|---|
| Actor = thing on the map; the earning properties (state, lifecycle, failure domain, world concurrency, pacing) | ActorSystemBoundaries-2026-08-21.md (convergent criteria; the assembly is ours, flagged choice 6) |
| Armstrong 1:1 mapping law (quoted) | ActorSystemBoundaries-2026-08-21.md (witnessed quote) |
| Not for code organization (quoted) | ActorSystemBoundaries-2026-08-21.md (witnessed quote, Elixir language documentation) |
| Arrows not actors; machine pure inside the actor shell (sans-io) | ActorSystemBoundaries-2026-08-21.md + ActorDataflowDesignSkills-2026-08-21.md -- flagged (choice 7) |
| Actor read as the machine continued (state = coherent type, handler = conversion) | Designer synthesis -- flagged (choice 7) |
| Closed message enum as the interface; effects as data | ActorDataflowBeauty-2026-08-14.md + ActorDataflowDesignSkills-2026-08-21.md |
| The eight convergent conventions | ActorDataflowDesignSkills-2026-08-21.md (origin-weighted) |
| Supervision drawn on the map; agents translate, not invent | AgentBuiltActorMachines-2026-08-21.md + worldModelBeforeCode.md 2026-08-20 -- flagged (choice 8) |
| Granularity is a runtime question (WhatsApp, Orleans) | ActorSystemBoundaries-2026-08-21.md (claims witnessed in their sources) |

### Names tell the truth

| Doctrine | Source |
|---|---|
| Name true at the moment of existence; AssembledRust | mainFunction.md 2026-08-21 (verbatim) |
| Extension down to ImplString | machineAnatomy.md 2026-08-21 |

### The diseases

| Disease | Source |
|---|---|
| Service object (bat) | DesignExemplars-Rust-2026-08-21.md |
| Sprawled emission (bat, ruff, GCC) | DesignExemplars-Rust supplement + MachineAnatomyPriorArt |
| Costume trait | traitsAsCapabilities.md 2026-08-20 + CostumeTraitFingerprint |
| Placeholder traits | rustComponentArchitecture.md 2026-08-19 |
| Schema between the lines | mainFunction.md 2026-08-21 + bat main (report) |
| Actor costume | ActorSystemBoundaries-2026-08-21.md (Armstrong, Erlang Programming Rules 5.2; Elixir docs) |
| Ask chain | ActorSystemBoundaries-2026-08-21.md (Sypytkowski ask-vs-tell weight; Akka docs timeout-race) |

### Traits first / No free functions (nexus content merged into section 3)

| Doctrine | Source |
|---|---|
| Every method in a trait; inherent = trait not yet extracted | Nexus skill (deployed) + psyche/Intent/mandatoryTraits.md |
| Trait pass before body; traits = specification | Nexus skill (deployed) |
| One ontology before bodies; one type + many single-function traits = one trait unseen | Nexus skill (deployed) |
| Defaults + sub-trait chains | Nexus skill (deployed) |
| Reuse or escalate | Nexus skill (deployed) |
| Port from map, not old code | Nexus skill (deployed) |
| Exceptions noted at site | Nexus skill (deployed) |
| Traits on data-bearing types; ZST with behavior = namespace | Nexus skill (deployed) |
| Identity trait-borne | Nexus skill (deployed) |
| No free functions; fn main() is the only one | Nexus skill (deployed) |

## Resolved from earlier versions

v1 -> v2: passive "capable of being resolved" wording gone (active
qualifier reading kept per 2026-08-14 Run precedent); weak opening
line replaced; machine-equals-TryFrom overclaim corrected before
writing v2 (psyche: "Im not investing into a single form like this").
