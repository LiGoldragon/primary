# Provenance: software-design skill draft

Maps every doctrine line in draft.md to its ruling source. Where a reading choice was made between possible interpretations, it is flagged.

## Section: The map

| Doctrine line | Source | Entry date |
|---|---|---|
| The first act of design is the world model: an ontology, an anatomy, an object-and-capabilities-oriented layout | psyche/Vision/worldModelBeforeCode.md "could we say this is about building ontology, anatomy .. a *map*" | 2026-08-20 |
| Code comes after the map is approved | psyche/Vision/worldModelBeforeCode.md "the model is trying to write code before it has a *model of the world*" | 2026-08-20 |
| A checklist that catches bad code means the failure already happened upstream | psyche/Vision/worldModelBeforeCode.md "training the model to catch themselves before creating a fake trait means we have already failed" | 2026-08-20 |
| The map is of the world, not the process. It contains what exists, what each thing contains, and what each thing can do | Synthesis of worldModelBeforeCode.md 2026-08-20 ("object/capability-oriented layout") + the import-resolution world map (design/ProtosEngine/importResolutionWorldMap-2026-08-21.md: "a map of the world, not of the process") | 2026-08-20/21 |
| Steps are walks across the map, never things on it | importResolutionWorldMap-2026-08-21.md section 4 ("the process falls out of the map; it is not on it") + the Non-Things table entry for Resolver ("a step of the walk dressed as a thing"). Agent interpretation: the world-map draft was ordered by the psyche ("of course") and is the first worked example of this principle; the "step dressed as a thing" wording is agent-authored in that map, not psyche verbatim. **Reading choice: the principle is inferred from the approved framing and its worked application, not from a single psyche statement naming it.** |
| A service is a step dressed as a thing | importResolutionWorldMap-2026-08-21.md Non-Things table. Agent wording applied to the rejected Resolver design, consistent with the psyche's "your trait methods are just regular functions pretending to be traits" (traitsAsCapabilities.md 2026-08-20). **Flag: "service is a step dressed as a thing" is the agent's compact formulation, not the psyche's verbatim words.** |
| The map's destination form is the Ethos interface file | psyche/Vision/worldModelBeforeCode.md 2026-08-21 "yes, except that it isnt ready to use yet, so the model writes the ethos but has no way to run it (yet)" | 2026-08-21 |

## Section: Types first

| Doctrine line | Source | Entry date |
|---|---|---|
| Design begins with the types (quoted block) | psyche/Vision/traitsAsCapabilities.md "we need to think very carefully of what the types are. First, really, because the traits are something that the types implement" | 2026-08-13 |
| Every logical aspect of the domain that has identity becomes a type | psyche/Vision/protosIsTheSharedStyle.md "turn every logical aspect into a type. ontology of source code" | 2026-08-18 |

## Section: Contents before behavior

| Doctrine line | Source | Entry date |
|---|---|---|
| List what each type contains before asking what it does | Inferred from the types-first ruling (traitsAsCapabilities.md 2026-08-13) and the world-map structure (importResolutionWorldMap-2026-08-21.md section 1, which lists contents before capabilities for every type). **Reading choice: no single psyche statement says "contents before behavior" in those words; the principle is the structural consequence of "types first" applied in the worked example.** |
| When two things always appear together, they are the contents of a third thing | psyche/Vision/mainFunction.md 2026-08-21 "if you build a thing from two things, so then can't you just create a new type that can be created?" | 2026-08-21 |

## Section: Capabilities

| Doctrine line | Source | Entry date |
|---|---|---|
| A trait is a capability a type has | psyche/Vision/traitsAsCapabilities.md 2026-08-13 "lets look at an update to the skills, and reconsider traits as 'capabilities'" | 2026-08-13 |
| Every method call in the code lives under a trait | psyche/Intent/mandatoryTraits.md "Every method call in our Rust code lives under a trait, because traits are the comprehension surface" | 2026-08-13 |
| Traits are the comprehension surface | psyche/Intent/mandatoryTraits.md (same entry) | 2026-08-13 |
| A capability is placed on the thing that contains its subject | Synthesis: traitsAsCapabilities.md 2026-08-20 "if the type needs a 'name' to resove the import, then it's not resolvable" + importResolutionWorldMap-2026-08-21.md "the capability sits on the thing that contains its subject". **Reading choice: the "placement law" name and the "contains its subject" wording come from the agent-authored world map, which applies the psyche's rejection of the costume trait. The psyche's own words are the negative form ("it's not resolvable"); the positive form is agent interpretation.** | 2026-08-20/21 |
| Action traits take the infinitive verb | psyche/Vision/traitsAsCapabilities.md 2026-08-21 "we would use the sort of infinitive form of the word, of the verb" + "we can write this down as a ruling" | 2026-08-21 |
| A type implementing Walk is capable of walking | psyche/Vision/traitsAsCapabilities.md 2026-08-14 "I accept verbs. now I can see why rust went with verbs; it is easy to understand that a thing that which implements Run is CapableOfRunning" | 2026-08-14 |

## Section: The costume-trait fingerprint

| Doctrine line | Source | Entry date |
|---|---|---|
| A trait method that must be handed its own subject as a parameter is a regular function wearing a trait | psyche/Vision/traitsAsCapabilities.md 2026-08-20 "your trait methods are just regular functions pretending to be traits" | 2026-08-20 |
| If the type needs a name handed in to resolve the import, it is not resolvable | psyche/Vision/importResolution.md 2026-08-20 "if the type needs a 'name' to resove the import, then it's not resolvable" | 2026-08-20 |
| Honest boundary: parameters that narrow or direct an operation the receiver already owns are legitimate | reports/CostumeTraitFingerprint-2026-08-20.md section 2 "Honest boundary summary". **Flag: the honest boundary is agent research, not psyche-ruled. The psyche directed the research and has not explicitly ruled on the boundary. The examples (query ranges, callbacks, event payloads) are from analysis of protos conforming cases.** |
| Creation is exempt | reports/CostumeTraitFingerprint-2026-08-20.md + reports/CreateTraitCrateSearch-2026-08-21.md "the subject does not exist yet". Agent interpretation consistent with the psyche's acceptance of Create/new as a trait (assembly.md 2026-08-21, later dissolved into TryFrom). |

## Section: Direction pairs

| Doctrine line | Source | Entry date |
|---|---|---|
| A direction pair never sits on one type | psyche/Vision/traitsAsCapabilities.md 2026-08-18 "realize isnt implemented by the same type as textualize. if you cant find two different types, the implementation is wrong" | 2026-08-18 |
| You do not textualize the text, and you do not realize the realized data | psyche/Vision/traitsAsCapabilities.md 2026-08-18, same statement | 2026-08-18 |

## Section: Fragmentation

| Doctrine line | Source | Entry date |
|---|---|---|
| One type implementing many single-function traits is probably one trait not yet seen | psyche/Vision/rustComponentArchitecture.md 2026-08-17 "the problem isnt that it only has one implementor, but that many of those traits should be one" | 2026-08-17 |
| Placeholder traits for every function create no sensible ontology | psyche/Vision/rustComponentArchitecture.md 2026-08-19 "the first implementation just simply created placeholder traits for every function, and just sort of mindlessly created traits that don't create a sensible ontology" | 2026-08-19 |

## Section: The spine is conversions

| Doctrine line | Source | Entry date |
|---|---|---|
| From when infallible, TryFrom when not. Never Into | psyche/Vision/worldModelBeforeCode.md 2026-08-21 "I think the From is better than Into" + psyche/Vision/mainFunction.md 2026-08-21 "try from or just from if it can't fail" | 2026-08-21 |
| Creation is demand-driven | psyche/Vision/worldModelBeforeCode.md 2026-08-21 "nobody harvests a material and then asks what this can be made into; everything is demand-driven" | 2026-08-21 |
| Multi-input creation is TryFrom on a tuple | psyche/Vision/worldModelBeforeCode.md 2026-08-21 "it would just be TryFrom, not create, so theres nothing to make" + psyche/Vision/assembly.md 2026-08-21 "if we can do new from a tuple, that will work" | 2026-08-21 |
| Conversions consume their inputs by value | psyche/Vision/assembly.md 2026-08-21 "lets do it efficiently so that we don't keep doubling the memory size... make sure that we didn't use references to these objects so that these objects can be properly dropped" | 2026-08-21 |

## Section: Names

| Doctrine line | Source | Entry date |
|---|---|---|
| A name tells the truth at the moment the thing exists | psyche/Vision/mainFunction.md 2026-08-21 "I wouldn't call it generated Rust because if you need to still write it, it hasn't been generated yet. So it would be more like assembled Rust" | 2026-08-21 |

## Section: Main

| Doctrine line | Source | Entry date |
|---|---|---|
| Main is a few lines (quoted block) | psyche/Vision/mainFunction.md 2026-08-21 "most programs... create the schema in the code instead of creating the schema and then just tying it up with a few lines" | 2026-08-21 |
| The schema is stated as objects | psyche/Vision/mainFunction.md 2026-08-21 "creating a spec that is an object that is a fully compliant data tree, a graph of data that can yield the entire program" | 2026-08-21 |

## Section: Deeper levels

| Doctrine line | Source | Entry date |
|---|---|---|
| Deeper levels carry specific behavior beyond conversions | psyche/Vision/mainFunction.md 2026-08-21 "not everything is a conversion, of course... eventually you have to go down into more specific behavior" | 2026-08-21 |

## Section: Illustration (Import Resolution)

| Element | Source | Entry date |
|---|---|---|
| The world map structure and all named types | design/ProtosEngine/importResolutionWorldMap-2026-08-21.md, ordered by the psyche ("of course", worldModelBeforeCode.md 2026-08-21) | 2026-08-21 |
| Registry and AssemblyFile as two things | psyche/Vision/assembly.md 2026-08-21 "We should have two things" | 2026-08-21 |
| "Manifest" is dead as a name | psyche/Vision/assembly.md 2026-08-21 "the assembly file. I think I like that better than manifest" | 2026-08-21 |
| Source is the crate-unit name | psyche/Vision/sourceNotCrate.md 2026-08-20 "source will be the name we use instead of crate" | 2026-08-20 |
| File is the type; "document" is dead | psyche/Vision/ethosSourceFiles.md 2026-08-20 "What's wrong with File?" | 2026-08-20 |
| ImportReference, not Import | psyche/Vision/importResolution.md 2026-08-20 "there are no Import's; what exists is an import reference" | 2026-08-20 |
| No namespace inside a file | psyche/Vision/ethosNamespaces.md 2026-08-20 "this concept is ridiculous in ethos" | 2026-08-20 |
| Colon resolves or errors, no fallback | psyche/Vision/importResolution.md 2026-08-20 "confirmed, kill the fallback" | 2026-08-20 |
| Rejected design (Resolving/FileYielding/ReferenceResolving) | psyche/Vision/traitsAsCapabilities.md 2026-08-20 rejection + reports/CostumeTraitFingerprint-2026-08-20.md analysis | 2026-08-20 |

## Reading choices flagged

1. **"Steps are walks, not things" / "A service is a step dressed as a thing"**: The positive principle is inferred from the world-map structure the psyche ordered and from the negative rulings (rejected Resolver, rejected costume traits). No single psyche statement names it in this form. The draft states it as doctrine; if it overreaches, it can be softened to an observation.

2. **"Contents before behavior"**: The types-first ruling is psyche-ruled; the "contents before behavior" sequencing is the structural consequence observed in the worked example. No psyche statement says these words. The draft presents it as a step in the protocol.

3. **The placement law (positive form)**: The psyche's words are the negative: "it's not resolvable." The positive form -- "a capability sits on the thing that contains its subject" -- is agent interpretation from the same ruling and its application. The draft states the positive form as doctrine.

4. **Honest boundary for costume-trait fingerprint**: The boundary distinguishing legitimate parameters (query ranges, callbacks) from costume-trait violations is from agent research (CostumeTraitFingerprint-2026-08-20.md), not from psyche ruling. The psyche directed the research; the boundary itself is unruled.
