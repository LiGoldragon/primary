# Prior flow state: software-design skill, nexus skill, datom library, ethos-monolith Nexus

Assembled by flow cff271af from flows e06e4c07, 15b67974, 2b34fafa, 5c8be3ca, and b7465e71.

## What is settled (ruled by the psyche)

### Nexus vocabulary and architecture (e06e4c07, 2026-08-19)

All rulings are verbatim in `psyche-raw/Vision/nexus.md`.

The whole component — daemon, at least two sockets, one default CLI client per socket, its signal contracts — is a Nexus. The execution engine inside it is Nexus Core. Every Nexus speaks only pure binary signal and never textualizes it; it is compiled with its own signal contracts and those of peer Nexuses it talks to. The meta-socket is the privileged socket. Not all edges carry meta access — it is case by case. Edge names the link between two vertices; contract names the compiled artifact. Both terms are kept.

Verbatim ruling on the edge/contract line (nexus.md, 2026-08-19, session e06e4c07):

> "the nexus line is good."

The proposed line approved: "A Nexus is a vertex in the graph of nexuses. An edge joins two vertices and carries one contract: every connected pair has an ordinary edge; only some pairs have a meta edge. A Nexus is compiled with the contracts of its own sockets and of every edge it has."

The skill is renamed `nexus` (from `rust-component-architecture`). A nexus repo is wanted but is "a possibility, under discussion." The `core-<component>` library split was already killed (threeStacks 2026-08-11; confirmed e06e4c07). Traits lines for the nexus skill were deployed (e06e4c07).

Everything built from now is a Nexus; what was built otherwise is rewritten. (nexus.md 2026-08-19, verbatim: "anything that has already been built that did not take the shape of The nexus is going to be rewritten.")

### Software-design doctrines (2b34fafa, psyche-raw/Vision/ files)

These rulings are logged verbatim in their respective Vision topic files and traced in the draft's provenance:

- **worldModelBeforeCode**: map before code; checklist = already failed upstream; world model is the map; steps are walks; process-named types (Resolver, Controller, Manager) do not belong on the map; destination form of the map is the Ethos interface file.
- **machineAnatomy**: agglomerate multiple types → create a coherent type → convert it onward; the shape is the law, not one spelling; machine is fractal; emission reviewable in one place, under one trait; four-part machine shape.
- **traitsAsCapabilities**: types first (verbatim: "we need to think very carefully of what the types are. First, really, because the traits are something that the types implement. We don't look for traits and then think of types for that."); costume-trait fingerprint verbatim: "if the type needs a 'name' to resove the import, then it's not resolvable."; direction pairs never share a type (verbatim: "You dont textualize the text, and you dont realize the realized data."); infinitive verb trait names; fragmentation is failure.
- **assembly / mainFunction**: From/TryFrom, never Into; multi-input creation is TryFrom on a tuple; consume by value; main is a few lines; the input is a strictly typed datom object.
- **worldModelBeforeCode 2026-08-21**: everything is demand-driven; design runs backwards.

### nexus/software-design overlap (15b67974, 2026-08-22)

Verbatim ruling in `psyche-raw/Vision/skillDesigning.md` line 356, session 15b67974:

> "dont worry about the skill overlap for now. we'll probably end up merging them."

This closes the concern that a map-doctrine line in nexus would repeat what the software-design skill holds. A merger is probable, timing unspecified.

### flow daemon ruling (15b67974, 2026-08-22)

Verbatim in `psyche-raw/Vision/flowDaemon.md`, session 15b67974: flow launches an existing harness (Claude Code / Codex) for now; the own 100%-typed-datom harness comes later. This settles Question 1 that e06e4c07 left open.

### Nexus port doctrine (15b67974, 2026-08-22)

Landed in the deployed nexus skill (Curriculum 1fa939a8, primary 469512d1): "A port starts from the map of what is being created; old code is at most inspiration for that map." — in the traits section, between reuse-or-extend and the exceptions paragraph.

## The software-design skill draft (2b34fafa)

The draft is at `/home/li/primary/reports/SkillDrafts/softwareDesign/draft.md`. It is 123 lines, at version 3 (v1 in git history; v2 written by 2b34fafa after the psyche's 2026-08-21 corrections; v3 by flow bc05da32, which added the actors section and two actor diseases from three actor research reports).

The draft's provenance is at `/home/li/primary/reports/SkillDrafts/softwareDesign/provenance.md`.

**Status: awaiting psyche re-review.** The log records "awaiting psyche re-review — five flagged wordings need pronouncement." The provenance lists nine reading choices, of which these are unruled:

1. "Steps are walks... a service is a step dressed as a thing" — agent formulation from the approved world map; not psyche-verbatim.
2. "Contents before behavior" as an explicit step — the sequencing is observed in the worked example; no psyche statement in those words.
3. The placement law's positive form ("placed on the type that contains its subject") — the psyche's words are the negative.
4. The honest boundary + creation exemption — research-derived, unruled.
5. `rust.write()` in the main example — the emission call's exact form (inherent method vs a trait) is undesigned.
6. The earning-properties list for actors — assembled from convergent criteria; no surveyed source states it as one checklist.
7. The actor as the machine continued (state = coherent type, handler = conversion; arrows never actors; pure machine inside the actor shell) — Designer synthesis; unruled.
8. "Agents translate, never invent" — inference from practitioner testimony; the positive half rests on thin evidence.
9. The input line in main — `Input`'s exact name and the datom's carrier undesigned.

The draft sections with settled rulings behind every doctrine line: the map comes first, the three-part machine, backwards from the want, types first, capabilities sit on their subjects (mostly), the spine is conversions, names tell the truth, and the diseases list.

## The datom library and ethos-monolith Nexus

Both repos exist under `/home/li/primary/repos/`:
- `/home/li/primary/repos/datom`
- `/home/li/primary/repos/ethos-monolith`

Flow 2b34fafa opened as "datom/ethos-monolith reacquisition (08-14) and overnight Realization audit (08-15)." The import-resolution world map (`design/ProtosEngine/importResolutionWorldMap-2026-08-21.md`) is described in the 2b34fafa log as "the protocol's first full exercise: the things and their contents drawn first, one capability placed by the law, resolution as a walk, the rejected Resolver as the recorded counter-example." This map was live, absorbing rulings as they landed, during 2b34fafa.

Ethos is named in the nexus ruling (nexus.md 2026-08-19) as the language to let the main traits and types of a Nexus be designed coherently. The ethos-monolith Nexus is the context in which the import-resolution design work was done.

The datom library is the typed input format: input enters every machine as a strictly typed datom object (mainFunction.md 2026-08-22; note appended by cff271af: that entry's quoted sentence was witnessed against the bc05da32 transcript to be agent-constructed — the psyche's actual typed words were "I dont see the arg input. where is datom coming from?").

No further state about the current code shape of either repo was read in these flows; 2b34fafa was grounding-and-design work, not implementation review. The Realization audit on 08-15 is mentioned but its content is not reproduced in the log.

## What is in flight or unanswered

### Universal nexus traits (e06e4c07, carried to 15b67974)

The design of universal nexus traits — "the basic ontology of an actor/dataflow software system" — was identified as the first question to answer after the vocabulary settled. Flow e06e4c07 left it open. Flow 15b67974 carried it forward in its Open section: "Universal nexus traits (e06e4c07's thread): untouched." Signal and sema are to be compared against the designed traits map; the nexus repo as the home for these traits is "a possibility under discussion."

### Open forks in 2b34fafa awaiting pronouncement

From the 2b34fafa log:
- Does creating a ResolvedAssembly resolve every import (fallible creation) or does resolution follow?
- The resolved thing's name (Import?).
- Local vs external ImportReference — one universal thing or two?
- Registry and assembly-file datom specs and homes.
- The skill draft's five flagged wordings (reading choices 1–5 above).
- The `.es` extension.
- The colon tension with 2026-08-07.

### Remembering design (b7465e71, 2026-08-22)

Flow b7465e71 was designing Remembering as an extension of the flows skill. Its design report (`flows/b7465e71/reports/rememberingDesign.md`) is marked draft with evidence in flight and four open questions for the psyche:

1. Filed as a report or context-only?
2. Deep-work depth number: fixed once, or stated per occasion?
3. Resolution of the 5c8be3ca-2 tension (layer one always fresh, deeper layers as claims, deepest-mining fresh throughout) — confirm.
4. Annotations stay as they are — confirm.

The 15b67974 remembering by b7465e71 was still in flight when b7465e71's log ends.

### Standing open items from 5c8be3ca (recorded in remembering5c8be3ca.md)

- "pronouncement" vocabulary entry: delayed by the psyche to a new session; still undelivered.
- VISION-2026-08-07.md line 566 ("The awareness file supersedes the reset bead as the session carrier"): still present, unmarked as superseded.
- skill-designing description-leak line ("Nothing of the skill's body appears in the description."): not yet in the skill (the existing inverse-direction line does not cover the same failure class).
- The deployed flows skill is stale (missing the log-creation/index-append paragraph); regeneration owed.
- Migration flow 01a02a06 was running with no migration begun (as of the b7465e71 remembering).

## Sources

- Method: code read `/home/li/primary/flows/e06e4c07/log.md`
- Method: code read `/home/li/primary/flows/2b34fafa/log.md`
- Method: code read `/home/li/primary/flows/5c8be3ca/log.md`
- Method: code read `/home/li/primary/flows/15b67974/log.md`
- Method: code read `/home/li/primary/flows/b7465e71/log.md`
- Method: code read `/home/li/primary/flows/15b67974/annotations.md`
- Method: code read `/home/li/primary/flows/b7465e71/reports/rememberingDesign.md`
- Method: code read `/home/li/primary/flows/b7465e71/reports/remembering5c8be3ca.md`
- Method: code read `/home/li/primary/reports/SkillDrafts/softwareDesign/draft.md`
- Method: code read `/home/li/primary/reports/SkillDrafts/softwareDesign/provenance.md`
- Method: code read `/home/li/primary/psyche-raw/Vision/nexus.md`
- Method: code read `/home/li/primary/psyche-raw/Vision/skillDesigning.md` (lines 340–374)
- Method: probe `ls /home/li/primary/flows/e06e4c07/` etc. (directory listings)
- Method: probe `find /home/li/primary/repos -name "datom" -o -name "ethos-monolith"` (repo existence confirmed)
- Flows: e06e4c07, 15b67974, 2b34fafa, 5c8be3ca, b7465e71 (all read directly)
