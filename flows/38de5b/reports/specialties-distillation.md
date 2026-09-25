# Specialties — a distillation proposal for the living's review

Composed by Psyche Fable 38de5b, 2026-09-25. Nothing here lands in Vision until the living accepts it. Sources are listed at the end; every statement re-articulates the living's words, none quotes them.

## Distilled statements (proposed for Vision/specialties.md)

1. **A specialty is what a flow is for.** Every flow has an aspect — Psyche, Mind or Field — which gives it its place in the hierarchy and its area of concern. A specialty narrows that concern to one job. A flow without a specialty is a general flow of its aspect; a specialized flow is preprogrammed with everything its job needs, so starting it means giving it only the job.

2. **A specialty is a different kind of start call, carried as a variant.** Flow's ordinary Start takes a launch profile. A specialized start takes the same profile plus one Specialty variant whose payload holds what that specialty needs. The specialty is not a field on the profile; it is the head of the call.

3. **A specialized flow loads only the vision that concerns its specialty.** Intent and Spirit guide every flow; Vision is loaded by concern. A Field flow does not load design records; a designer may hand it a guideline.

4. **Each model in each aspect has its own specialized roles.** The set of specialties is a function of aspect and model together: Fable in Psyche designs and distills vision; Fable monitors; Luna in Mind illustrates — documentation with imagery; Luna in Field monitors at light effort; Sol in Mind implements.

5. **Specialties known today.** Monitor (Field; keeps track of who is doing what and answers quickly; woken by a hook when a watched flow's final response or a message arrives, never by polling; Luna at light effort, later Jev). Voice (Psyche; relays and summarizes to the living through a voice medium; Luna at light effort). Implementation (Mind; makes something new from an ethos — a -clj tool or a nexus). Design (Psyche, Fable). Illustrator (Mind, Luna). VisionDistillation (Psyche, Fable; loaded with basic vision and the vision of its field, it produces a full document, a spec and example code; the living's acceptance turns that into distilled vision, which Mind then implements).

6. **Design the ethos first; the parallel nexus follows.** For every nexus the ethos is designed first, and the -clj tool is written from the ethos faster than the rest.

7. **A -clj tool** is a prototype of a nexus in Clojure: EDN emulating datom, Malli for the types, pseudo-traits for the kinds. It is named with the nexus's name and the suffix -clj, is a standalone CLI, may be developed in Babashka and is compiled for deployment through Nix. It is later rewritten in Ethos and Rust from its Malli types and pseudo-traits.

8. **-clj tools are packaged by a shared Nix library**, the way the nexuses are packaged by a shared Rust build library.

## The Ethos

Written in the Library form ethos-zero parses today. The Signal change belongs in signal-flow, where Start lives; it is shown after.

```
Library
[]
[ Specialty.[ Monitor.MonitorProfile
              Voice.VoiceProfile
              Implementation.ImplementationProfile
              Design.DesignProfile
              Illustrator.IllustratorProfile
              VisionDistillation.DistillationProfile ]
  MonitorProfile.{ Trigger Vector<FlowId> }
  Trigger.[ FinalResponse Message ]
  FlowId.String
  VoiceProfile.{ Medium }
  Medium.[ ChatGptVoice Unity ]
  ImplementationProfile.{ EthosPath Target }
  EthosPath.String
  Target.[ Clj Rust ]
  DesignProfile.{ Subject }
  Subject.String
  IllustratorProfile.{ Subject }
  DistillationProfile.{ Subject Vector<RecordRef> }
  RecordRef.{ FlowId Topic }
  Topic.String ]
[]
[]
```

In signal-flow's Signal, Start gains a sibling query rather than a fourteenth field:

```
[ Start.StartRequest  StartSpecialized.SpecializedStartRequest  Restart.RestartRequest  ResolveRecipient.RecipientResolutionRequest  Send.SendRequest  Stop.StopRequest  List.ListRequest ]
SpecializedStartRequest.{ LaunchProfile Specialty OriginClue }
```

The launch profile is unchanged: launch request id, sources, skills, aspect, power, harness, model, effort, predecessor, remembered flows, Herdr session, system-prompt bundle file, instruction prompt.

## Example: starting this seat's own specialty

Datom, as the CLI takes it:

```
StartSpecialized.{ { request-9 [ { Vision/flowNexus.md 54c08e71… } ] [ spirit main-flow psyche psyche-interraction ] Psyche High Claude claude-fable-5-1 medium None [] messaging-build /abs/bundle.md «Distill the specialty vision.» } VisionDistillation.{ specialties [ { e51411 flowAspect } { e51411 stack } ] } { 38de5b session-1 turn-1 } }
```

EDN, as flow-clj takes it — the tag chain mirrors the Datom variant chain, positions mirror positions:

```
#start-specialized [ ["request-9" [["Vision/flowNexus.md" "54c08e71…"]] ["spirit" "main-flow" "psyche" "psyche-interraction"] :psyche :high :claude "claude-fable-5-1" :medium nil [] "messaging-build" "/abs/bundle.md" "Distill the specialty vision."] #vision-distillation ["specialties" [["e51411" "flowAspect"] ["e51411" "stack"]]] ["38de5b" "session-1" "turn-1"] ]
```

A variant carrying nothing is a keyword (:psyche, :high, :claude, :medium); a tag is a variant carrying data (#start-specialized, #vision-distillation). The same rule gives the message its three-tag form, mirroring Msg.Psyche.Fable.{ id «text» }: `#msg #psyche #fable ["38de5b" "text"]`, and for the living's words `#living #psyche #fable ["38de5b" "words"]`.

A monitor: `#start-specialized [ <profile> #monitor [:final-response ["38de5b" "e51411" "00f95a"]] <origin> ]` — Field, Luna, light effort, woken when any of three flows ends a turn.

## Roles by aspect and model, as named today

| Aspect | Fable | Opus | Sonnet | Sol | Astra | Luna |
|---|---|---|---|---|---|---|
| Psyche | Design, VisionDistillation, Monitor (proposed) | general | general, low | — | — | Voice (proposed) |
| Mind | — | — | — | Implementation | Implementation (proposed) | Illustrator |
| Field | — | — | — | general | Implementation (proposed) | Monitor |

Cells the living named stand; cells marked proposed are this seat's reading; blank cells are not ruled.

## The Nix library for -clj tools (with Mind)

Today no Clojure or Babashka packaging exists on the cluster; the messenger's -clj commands are bash shims calling Babashka from PATH, and the nexuses inline crane while rust-build is the shared Rust library. The shape proposed, for Mind to build as clj-build beside rust-build:

```
clj-build.lib.${system}.mkCljCli pkgs { name, src, main, deps, bin ? name }
# a wrapped Babashka script with pinned deps for development, one derivation
clj-build.lib.${system}.mkCljUberjar pkgs { name, src, main, deps }
# the deployable form, jar or native image, same inputs
clj-build.lib.${system}.mkCljChecks pkgs { src, tests }
# the flake check running the Clojure tests, so a -clj tool's tests gate its flake
```

HackyMessenger is the first consumer; flow-clj the second. Its check.nix today runs only the Python tests; the Clojure tests join through mkCljChecks.

## Open before the living

- Whether Specialty is a sibling query (StartSpecialized) or the ordinary Start with an Option<Specialty> — the statement above takes the living's words "a different kind of call" literally.
- The payload of each specialty profile is a first cut; Monitor's cadence and watched flows, Voice's medium, Implementation's ethos and target are the minimum each needs.
- Whether the roles table is per model or per model-and-effort (Luna light is named twice).

## Sources

e51411 flowAspect (Specialized flows; specialized roles per model, 2026-09-25); e51411 stack (The -clj tools; Hacky Field and Clojure as the prototyping language, 2026-09-25); e51411 notion/v2 (A monitor flow); e51411 notion/stack (Subflows started by Flow); fd0f97 flowTypes; d8df70 flowTool (typed flows, subtypes); e71dab psycheVoice; 752e0f psycheVoice; 752e0f awareness; 108ab0 operational-skillTypes. Code: signal-flow ethos/signal.ethos (LaunchProfile, StartRequest); flow crates/flow/src/main.rs (Start example); rust-build lib/default.nix; HackyMessenger bin and bb.edn.
