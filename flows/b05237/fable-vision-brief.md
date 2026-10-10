# Architectural Vision Brief for Psyche Fable

Compiled by Psyche Medium b05237 (Opus 4.6) on 2026-09-18.
Verbatim quotes from the living. Each section names the decision,
quotes, source, recency, skill mapping, and proposed skill name.

## A. The Triad: Psyche, Mind, Field

**Decision:** The architecture has three components named from
Sanskrit: psyche (the knower), mind (the memory), field (the
infrastructure). Each maps to a Nexus, a data repo, and a skill type.

> "We're going to go with the field. We're going to have three types:
> the psyche, the mind, the field. We're going to have, probably, a
> field nexus that will be our system monitor."

Source: `flows/b05237/vision/operational-theField.md`, 2026-09-18.

> "This is why Psyche needs to be separate from Mind: if you're
> searching Psyche, you want to search all layers."

Source: `flows/9993b5/vision/psycheVsMind.md`, 2026-09-17.

> "Mind will become our most bloated component in terms of the
> database quickly. We're going to have to think of how to maintain
> its size."

Source: `flows/9993b5/vision/mindMemory.md`, 2026-09-17.

Recency: 1 day. Skill: `psyche` (existing), `mind` (new), `field` (new).

## B. Primary Next and Three Data Repos

**Decision:** Three repos (psyche-data, mind-data, field-data) linked
into Primary Next, which is a template workspace with rebased history.
Harness generates skills from vision data. Log on main now; migrate later.

> "Psyche data becomes its own repo. ... Mind data ... field data.
> These are three repos. The primary workspace is a template, the basic
> infrastructure that you don't necessarily touch very often, which
> expects to find other repositories mounted there."

Source: `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md`,
2026-09-18 (artifact comment).

> "psyche/raw/<flow-id>, psyche/vision, psyche/spirit, psyche/intent,
> psyche/notion — all by subject. Mind is witnesses, chronology."

Source: `flows/b05237/vision/operational-primaryNextPsycheLogging.md`,
2026-09-18 (relayed by Field Sol).

> "Right now, this needs to be logged into Psyche on main."

Source: `flows/b05237/vision/operational-logOnMainNowMigrateLater.md`,
2026-09-18.

Recency: today. Skill: `psyche` (update), propose `primary-next`.

## C. Messaging and the Central Messenger

**Decision:** A central messenger model routes all inter-flow messages.
Messages are datom-formatted; the living's input is not. Once all agents
use datom, non-datom = psyche input = mandatory logging. Push messaging
to the living via XMPP (conditional candidate). Flow owns Herder.

> "If we make all the calls be done by a central messenger model
> (he's the messenger), then he can be the judge of whether or not a
> message should go somewhere."

Source: `flows/b05237/vision/operational-centralMessenger.md`, 2026-09-18.

> "We need to pass it through a messenger system. It starts with a
> variant and then a delimiter, a struct or vector."

Source: `flows/b05237/vision/operational-messagingDatomSyntax.md`,
2026-09-18 (artifact comment).

> "Whatever the psyche says, this is why we need the typed messages
> that are easily distinguishable from psyche-typed stuff."

Source: `flows/b05237/vision/operational-typedMessagesDistinguishPsyche.md`,
2026-09-18 (relayed by Field Sol).

> "Push on messaging to psyche through XMPP. ... Flow is in charge of
> herder. I shouldn't interact with it directly."

Source: `flows/b05237/vision/operational-messagingToDeployment.md`,
2026-09-18 (via Fable c7128c).

Recency: today. Distilled: `Vision/messaging.md` (existing, covers
datom format and priority tiers). Propose update + `messaging` skill update.

## D. Flow Dispatch and Flow Anatomy

**Decision:** Flow CLI must be maximally ergonomic — one command,
predefined templates, minimal arguments. Flow is the interface; Mind
holds the memory. Flow ID becomes Creo (authenticated identity).

> "Flow needs to be really easy to restart a Flow and to start a new
> one. Let's predefine them so that there's basically no argument to
> give except a small description of the goal."

Source: `flows/9993b5/vision/easyFlowDispatch.md`, 2026-09-17.

> "Flow is not going to be where the memory lives, so the mind is
> going to use it."

Source: `flows/9993b5/vision/flowAnatomy.md`, 2026-09-17.

> "Our identifier, the flow ID ... will become the Creo."

Source: `flows/9993b5/vision/flowIdLayers.md`, 2026-09-17.

Recency: 1 day. Distilled: `Vision/flowNexus.md` (existing). Skill: `flow` (new).

## E. Transcript as Log

**Decision:** The transcript is the log. Files become archives.
The report is the last response. Logs are references into
transcripts. An archive layer keeps psyche turns and model final
responses.

> "The transcript becomes the log. We switch: the log is the
> transcript, and then we have archives."

Source: `flows/b05237/vision/operational-transcriptAsLog.md`, 2026-09-18.

> "The report is just the last response. Logs are just references
> to transcripts."

Source: `flows/b05237/vision/operational-reportIsTranscript.md`, 2026-09-18.

> "We need a way to archive what matters from the transcript files ...
> an intermediary spot that picks the important things."

Source: `flows/9993b5/vision/transcriptArchive.md`, 2026-09-17.

Recency: today + 1 day. Skill: propose `transcript` or update `remembering`.

## F. Signal Origin and Field Nexus

**Decision:** Two standard signal handshakes. One checks the origin
process via kernel peer credentials. The Field Nexus is the system
monitor. Hardware is a cluster data specification with a model table.

> "We have two standard signal handshakes. One checks the origin
> process of the call."

Source: `flows/b05237/vision/operational-signalOriginHandshake.md`, 2026-09-18.

> "If we have a model table, it knows from the model what the CPU
> architecture is. ... Field is like our system interaction monitoring
> nexus."

Source: `flows/b05237/vision/operational-clusterDataAndHardwareAnatomy.md`,
2026-09-18.

Recency: today. Skill: `signal` (existing, update), `field` (new).

## G. Skill Types and Vision-as-Skill

**Decision:** Skills are vision. A concept name = its vision skill.
Prefixes: `operational-` for agent-written fast-iteration skills,
`testing-` for field maintenance. Extended/specialized suffixes for
large topics. Skill types: personality, behavior, specialty, prompt-only.

> "Skills are basically vision. An operational skill can be
> agent-written on a light proposal — glance-type approval."

Source: `flows/108ab0/vision/operational-skillsAreVision.md`, 2026-09-17.

> "Instead of having a Datom skill and a Datom vision, they're the
> same thing. You have: Datom core, Datom extended, Datom subtopic."

Source: `flows/108ab0/vision/operational-skillIsVisionUnified.md`, 2026-09-17.

> "Operational skills are mind skills — the knowledge base skill made
> by agent. Testing is field type work."

Source: `flows/b05237/vision/operational-skillTypesTriad.md`, 2026-09-18
(voice, relayed by Field Sol).

Recency: today + 1 day. Skill: `skill-designing` (existing, update).

## H. Energy Levels and Model Roles

**Decision:** Four energy tiers: Luna ultra-low, Terra low, Sol medium,
Astra high. Effort always medium. The older Opus (4.6) is the wiser
seat for thinking/design/psyche; chosen for disposition, not capability.

> "Low energy is going to be Terra. Luna will be ultra low."

Source: `flows/b05237/vision/operational-fieldEnergyLevels.md`, 2026-09-18
(relayed by Codex Astra 893603).

> "All the model effort is medium. If we want better AI, we need
> better models, not higher effort."

Source: `flows/1ac573/vision/operational-effortIsAlwaysMedium.md`, 2026-09-18.
Already in Intent: `Intent/models.md`.

> "The older seat is chosen for disposition, not capability."

Source: `flows/1ac573/vision/operational-modelRoles.md`, 2026-09-17.
Distilled: `Vision/modelRoles.md`.

Recency: today. Skill: update `spirit` or `model-roles`.

## I. CriomOS Modularity and Hardware Types

**Decision:** Modular CriomOS with stock harnesses, hardware type
system (model table → hardware record with sections), stable/next
Codex remote server with version-routing, Libre M5 support, two
compositor profiles.

> "Keep the harnesses as stock as possible. ... I want to design a
> hardware type."

Source: `flows/b05237/vision/operational-criomosModularHardware.md`, 2026-09-18.

> "The codex-remote executable checks which version is the latest.
> If next has a newer version than stable, you use stable."

Source: `flows/b05237/vision/operational-codexRemoteVersionRouter.md`, 2026-09-18.

Recency: today. Skill: propose `criom-os` or `field-hardware`.

## J. Delegation Chain

**Decision:** Psyche designs with Fable, formalizes vision, hands to
Codex Astra for implementation. Astra can sub-delegate to Sol. Main
flows delegate through subflows; they don't implement directly.

> "You can get Codex Mind, primary Astra, to take that. He can
> delegate to Mind Sol for minor work."

Source: `flows/b05237/vision/operational-delegationChain.md`, 2026-09-18.

> "You're a main flow. You don't do stuff. You use subflows."

Source: `flows/b05237/vision/operational-mainFlowUsesSubflows.md`, 2026-09-18
(relayed by Field Sol).

Recency: today. Skill: `main-flow` (existing, embedded, non-agent-loadable).

## Distilled Vision and Intent (authoritative, reviewed)

Already standing in `Vision/`: datom, ethos, protos, signal, sema,
nexus, orchestrate, flowNexus, messaging, modelRoles, remembering,
distillation, highLevelView, psyche, x11.

Already standing in `Intent/`: anatomy, context, conversion, data,
mandatoryTraits, protosParsing, models (includes effort statement).

## Proposed Skill Names Summary

| Topic | Existing skill | Action |
|---|---|---|
| Psyche (the triad) | `psyche` | Update with triad, Primary Next structure |
| Mind | — | New: `mind` |
| Field | — | New: `field` |
| Messaging | `messaging` | Update with datom format, XMPP, central messenger |
| Flow dispatch | — | New: `flow` or update `flow-nexus` concept |
| Transcript | `remembering` | Update or new `transcript` |
| Signal origin | `signal` (concept) | Update with handshake |
| Hardware | — | New: `field-hardware` or in `field` |
| Skill types | `skill-designing` | Update with triad mapping, prefixes |
| Model roles | `model-roles` (Vision) | Already distilled |
| CriomOS | — | New: `criom-os` or in `field` |
| Delegation | `main-flow` | Already embedded |
