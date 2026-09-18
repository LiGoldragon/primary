# The Vision Dependency Picture, Whole

Intermediary report from Psyche Fable (claude-fable-5-1, medium), subflow of Psyche Medium b05237, 2026-09-18. For the living to comment on. Mind Astra 0ab019 implements the proof of concept after your comments. Nothing here is decided; every numbered question is yours.

This picture covers the whole architecture, not one record type. The earlier picture from Fable c7128c and 056f6d proposed the psyche record as an ethos type and left six questions on that record; those six stand separately and are not repeated here.

## How to read this

Every edge in the graph carries one of two marks.

- **[recorded]** means the relation is stated in a psyche record: your words name the earlier thing, or the record's context names it and the quote bears it out.
- **[inferred]** means an agent read the relation into the records. It is my reading, pending your word.

Candidate operational vision is written in my wording, not yours. It is what I would put into a skill if you said yes. Each candidate names the records it condenses so you can check the drift.

Skill names follow your rule of 09-18: the concept name is the vision skill, `psyche extended` and `psyche vision` are its extended faces, and large topics split into balanced subtopics. Where a name breaks that rule I say so.

## The graph, layered

Authority runs down. Dependency mostly runs up: a raw statement of today refines a distilled statement of yesterday, which refines an Intent.

```
Spirit (the spirit skill)
  |
Intent: models (better models, not effort; two scales share high and medium)
  |
Distilled Vision: psyche, flowNexus, messaging, modelRoles, remembering, distillation,
                  datom, ethos, protos, signal, sema, nexus, orchestrate
  |
Raw 09-16 to 09-17 (flows f55ec8, 9993b5, 108ab0, 1ac573):
  psycheVsMind, mindMemory, flowAnatomy, flowIdLayers, easyFlowDispatch,
  transcriptArchive, transcriptOverFiles, structuredLog, powerLevels,
  skillsAreVision, skillIsVisionUnified, effortIsAlwaysMedium, modelRoles
  |
Raw 09-18 (flows b05237, c7128c, 33ba2b relays, artifact comments):
  theField, threeDataRepos, primaryNextPsycheLogging, mind, centralMessenger,
  messagingDatomSyntax, messagingToDeployment, transcriptAsLog, reportIsTranscript,
  reportWatcher, visualization, jobEffortLevels, fieldEnergyLevels,
  skillIsVisionPrefixed, skillTypesTriad, signalOriginHandshake, hardware, delegationChain
```

The clusters below are subgraphs of this. Each cluster is one topic of the brief.

## A. The triad: psyche, mind, field

```
psycheVsMind (09-17) --[recorded]--> mindMemory (09-17): "Flow's memory will live in mind"
theField (09-18)     --[recorded]--> psycheMindAndTheThirdComponent (09-18): field named from the Vedic options
threeDataRepos (09-18) --[inferred]--> theField: three repos because three components
mind (09-18, "legacy file system database") --[inferred, tension]--> mindMemory (mind as the memory Nexus)
```

**Candidate operational vision.** A thinking machine has three components. Psyche is the knower: the vision, spanning every layer, searched as one. Mind is the memory: every flow's transcripts, witnesses, and chronology, the component that grows fastest and needs a size discipline. Field is the ground: the machine, the files, the running code, with a Field Nexus as system monitor that an agent reaches through the field CLI, which signals with a traceback to its caller. The living talks to Psyche; Psyche dispatches.

Condenses: `9993b5/psycheVsMind`, `9993b5/mindMemory`, `b05237/operational-theField`, `b05237/operational-psycheMindAndTheThirdComponent`.

**Skills.** `psyche` exists and is updated with the triad. `field` already exists as a seat skill (Field Sol, Field Astra, reaping is one capability); the brief called it new, it is not. `mind` is new.

**Tension to rule on.** On 09-18 you said: "There's psyche, there's the mind. Let's just start naming things properly: mind. This is the legacy file system database, and then we're going to update that into the Nexus, Psyche, and Mine." Read plainly, mind is the legacy file store, and the destinations are Nexus, Psyche, and Mine. Read against 09-17, mind is the memory Nexus itself. The two readings give different skills.

- **Q1.** Is "mind" the name of the memory component that will be a Nexus, or the name of today's file-based store that the Nexus replaces? What did "Mine" name in that sentence?
- **Q2.** Should the `field` skill stay a seat skill, or become the concept skill for the field, with seats as its extended face?

## B. Primary Next and three data repos

```
threeDataRepos (09-18) --[recorded]--> Vision/psyche.md: "Psyche data belongs in a dedicated repository symlinked into Primary"
primaryNextPsycheLogging (09-18) --[recorded]--> threeDataRepos: names the directories inside psyche data
logOnMainNowMigrateLater (09-18) --[recorded]--> primaryNextPsycheLogging: log on main now, migrate later
108ab0/operational-primaryIsPsyche (09-17) --[inferred]--> threeDataRepos: only Vision, Intent, Spirit belong in primary
threeDataRepos --[recorded]--> skillIsVisionUnified (09-17): "Harness takes vision data and creates the corresponding skills"
```

**Candidate operational vision.** Psyche data, mind data, and field data are three repositories, each with an expected structure. Psyche data holds `raw/<flow-id>` for what was heard in a flow, and `vision`, `intent`, `spirit`, `notion` by subject. Mind data holds witnesses and chronology: what landed, ran, tested, deployed. Primary Next is a template workspace, rarely touched, that expects these repositories mounted. Harness generates skills from psyche data. Until Primary Next runs, everything is logged on primary main.

Condenses: `b05237/operational-threeDataReposAndPrimaryNext`, `operational-primaryNextPsycheLogging`, `operational-logOnMainNowMigrateLater`, `Vision/psyche.md`.

**Skills.** `psyche` carries the psyche data structure. Propose `primary-next` for the workspace shape, or fold it into `psyche extended`. Your rule says a concept name; "primary next" is the concept you used.

**Ready for distillation.** Yes, into `Vision/psyche.md`, which already carries the target shape as reviewed. The new statements add the three repos and the directory names. Field data has one record; it enters as stated, no more.

- **Q3.** Where does the notion of the field data repo end and mind data begin? You placed "what landed, ran, tested, deployed" in mind. Is field data the hardware and cluster specification only?
- **Q4.** Is skill generation moving from Curriculum into Harness a decision or a maybe? Your words were "maybe we just rewrite all of that logic into Harness".

## C. Messaging and the central messenger

```
Vision/messaging.md (distilled): message is a datom; priority head; delivery per tier
centralMessenger (09-18)         --[inferred]--> Vision/messaging.md
messengerSynchronizesRoster      --[recorded]--> centralMessenger: "if he makes all the calls, he can stay aware of who's who"
messengerGlanceApproval (09-18)  --[recorded]--> centralMessenger: glance-approved for testing and deployment
messagingDatomSyntax (comment)   --[recorded]--> Vision/messaging.md: variant head, then struct or vector
typedMessagesDistinguishPsyche   --[recorded]--> messagingDatomSyntax: the reason for the format
messagingToDeployment (to c7128c)--[recorded]--> typedMessagesDistinguishPsyche: non-datom means psyche, means a log
standardMessagingSkill (relay)   --[inferred]--> messagingToDeployment: relay all living words with provenance
messengerSynchronizesRoster      --[recorded, supersedes]--> 1ac573/operational-mirrorToEveryoneAndRoster
```

**Candidate operational vision.** Every inter-flow message passes through one messenger, which judges whether it should reach its target, may annotate it with context, and by making every call stays aware of who is who. A machine message is a datom: a variant head, then a struct or vector. The living types normally, so a non-datom message is psyche input and is logged no matter what, sent to the psyche flow verbatim with the context of what the receiving flow was doing. A relaying flow passes the living's words whole, with context, marked as relayed by it. Flow owns Herder; the living does not drive Herder directly. Push to the living goes through XMPP if that remains the best candidate.

Condenses: the nine records above plus `Vision/messaging.md`.

**Skills.** `messaging` exists; update it. The relay duty is a section of `messaging`, not a separate skill, unless you want it loadable alone.

**Ready for distillation.** The messenger, the datom form, and the psyche distinction: yes, into `Vision/messaging.md`. XMPP: no, it is conditional in your own words.

- **Q5.** Is the messenger a model, as in "he's the messenger", or a Nexus program with specified message types, as in "implement the proper nexus that uses specified messages"? Both are recorded on the same day. A model that routes and a Nexus that carries can coexist; say which holds the judgment.
- **Q6.** Should "relay all my words with context and provenance" be Intent? It guides every flow that ever hears you.

## D. Flow dispatch and flow anatomy

```
Vision/flowNexus.md (distilled): sets up and starts a flow; session named after its ancestor; reaped by refresh
easyFlowDispatch (09-17) --[inferred]--> Vision/flowNexus.md
flowAnatomy (09-17)      --[recorded]--> mindMemory: "it's not going to be where the memory lives, so the mind is going to use it"
flowIdLayers (09-17)     --[recorded]--> callerIdentity (09-17): Creo rests on the caller-identity chain
fieldTwoSeatsAndRefreshNaming (09-18) --[recorded]--> Vision/flowNexus.md: "of" means descendant of; core skill vision for refresh
reportIsTranscript (09-18) --[recorded]--> flowAnatomy: "That's what the Flow Nexus needs to do"
```

**Candidate operational vision.** Flow is the interface; Mind holds the memory. Starting and restarting a flow takes one command and a short goal; the flow's own instructions carry how to find the rest of its context. A flow identifies itself by its flow ID, semi-secure for now, becoming the Creo when caller identity is authenticated. A refreshed flow is named `<role> of <ancestor-id>`. The Flow Nexus serves transcript data quickly.

Condenses: `9993b5/easyFlowDispatch`, `flowAnatomy`, `flowIdLayers`, `callerIdentity`, `b05237/operational-fieldTwoSeatsAndRefreshNaming`, `operational-reportIsTranscript`, `Vision/flowNexus.md`.

**Skills.** Propose `flow` as the concept skill, with `Vision/flowNexus.md` folded in as its core. `refresh` exists and already carries the "of" naming.

**Ready for distillation.** The "of" naming and Flow-versus-Mind roles: yes, into `Vision/flowNexus.md`. Creo: no, one record, one new term.

- **Q7.** Is the vision topic `flowNexus` or `flow`? Your naming rule says the concept name; the distilled file says `flowNexus`.

## E. Transcript as log

```
transcriptOverFiles (09-17) --[recorded]--> transcriptArchive (09-17): archive what matters, clean up
transcriptAsLog (09-18)     --[recorded]--> transcriptOverFiles: "We use the transcript now"
reportIsTranscript (09-18)  --[recorded]--> transcriptAsLog: same message, completes it
transcriptAndMachineFlow (c7128c, 09-18) --[recorded]--> reportIsTranscript
transcriptBlockExtraction (09-18) --[recorded]--> reportIsTranscript: the tool that addresses the transcript
reportWatcherAndIllustrator (09-18) --[recorded]--> reportIsTranscript: watcher backs up the last response
78c93c/witnesses-and-reports (09-05) --[inferred, tension]--> reportIsTranscript: "what is a report but hearsay put into a file"
```

**Candidate operational vision.** The transcript is the log. The report is the flow's last response. What was a log entry is now a reference into a transcript. The files under a flow directory are the flow archive, in the current directory shape, developed from there. A per-harness object fetches a transcript and returns cognitively cohesive blocks, the model judging where a block ends; a mismatch shows only the mismatch. A watcher notices a flow going idle with a report, backs it up, creates the archive, marks it main-flow or subflow, and dispatches illustration to the most qualified flow.

Condenses: the seven records above.

**Skills.** Propose `transcript` as the concept skill. `transcript-search` exists as a procedure and becomes its extended face or stays a tool skill. `remembering` stays, since it is about one subjectivity, not storage.

**Ready for distillation.** Yes, into a new `Vision/transcript.md`, with the 09-05 hearsay tension surfaced beside it, not resolved by silence.

- **Q8.** On 09-05 you questioned reports as hearsay in a file. On 09-18 the report is the last response and the watcher backs it into the archive. Does the 09-18 statement retire the 09-05 doubt, or does a report remain suspect unless it carries a witness?
- **Q9.** "We don't want to make files anymore" (09-17) and "the files are the flow archives, use the current directory structure" (09-18). Are archive files the one kind of file that stays?

## F. Signal origin and the Field Nexus

```
signalOriginHandshake (09-18) --[recorded]--> theField: "immediately after naming the Field Nexus"
signalOriginHandshake         --[recorded]--> Vision/signal.md: "We should put that in the signal"
callerIdentity (09-17)        --[inferred]--> signalOriginHandshake: same mechanism, kernel peer credentials
clusterDataAndHardwareAnatomy --[recorded]--> theField: "Field could run a check after boot"
```

**Candidate operational vision.** Signal has two standard handshakes. One checks the origin process of the call, so a Nexus knows where a message came from; this lives in the signal layer. Field verifies hardware at boot against the model table.

**Skills.** `signal` is a Vision topic, not a skill directory today. Propose `signal` as a concept skill generated from `Vision/signal.md`; the handshake is a section.

**Ready for distillation.** Not yet. You asked for the anatomy in a report and to give input on the design. The handshake enters Vision after that round.

- **Q10.** What is the second standard handshake? Only one is described.

## G. Skills are vision

```
skillsAreVision (108ab0, 09-17)     : skills are vision; operational skills carry glance approval
skillIsVisionUnified (108ab0, 09-17) --[recorded]--> skillsAreVision: "Let's just unify it all"
skillIsVisionPrefixed (comment, 09-18) --[recorded]--> skillIsVisionUnified: prefixes tell the type; extended faces; balanced subtopics
skillTypesTriad (voice, 09-18)       --[recorded]--> theField: operational is mind, testing is field
testSkillForIllustration (comment)   --[recorded]--> skillIsVisionPrefixed: test skills need no review
threeDataRepos                       --[recorded]--> skillIsVisionUnified: Harness generates skills from vision
Vision/psyche.md (distilled)         : operational- prefix, testing- prefix, pure vision unprefixed
```

**Candidate operational vision.** A skill is vision. The concept name is its core skill; `<concept> extended`, `<concept> vision`, `<concept> spirit` are its faces; a topic that grows too large splits into balanced subtopics, each its own skill file. A prefix tells the skill's type. Operational skills are mind skills: the agent-made knowledge base, written on a light proposal with glance approval. Testing skills are field work: fixes in production, the system's new appendages, needing no review. Raw vision and raw notion are the good source; distillation makes them skills.

Condenses: the six records above plus `Vision/psyche.md`.

**Skills.** `skill-designing` exists and is updated. Under your rule its concept name would be `skills`.

**Ready for distillation.** Yes, into `Vision/psyche.md` or a new `Vision/skills.md`. This is the most repeated statement in the corpus this week: three records over two days, plus two comments.

**Tension to rule on.** `Vision/psyche.md` says pure vision skills carry no prefix and operational skills carry `operational-`. Your 09-18 comment says an operational skill that is not vision "is just the name of a concept, like psyche". And the voice record says operational skills are mind skills. So an unprefixed `psyche` is either pure vision or an operational concept skill, depending on which record is read.

- **Q11.** Does the unprefixed concept name mean pure vision, or the operational knowledge-base skill? Which gets the prefix?
- **Q12.** The test prefix: `testing-` as distilled in `Vision/psyche.md`, or `test-` as in your 09-18 comment?
- **Q13.** Should "skills are vision" be Intent? It shapes how every skill in the system is written.

## H. Energy levels and model roles

```
Intent/models.md (distilled)      : better models, not effort; two scales share high and medium
effortIsAlwaysMedium (1ac573)     --[recorded]--> Intent/models.md: "Let's put that in the intent somewhere"
effortIntoIntent (comment, 09-18) --[recorded]--> effortIsAlwaysMedium: "I want to put something in intent from this"
jobEffortLevels (c7128c, 09-18)   --[recorded]--> Intent/models.md: "a different model, not a different thinking effort"
powerLevels (9993b5, 09-17)       --[recorded]--> layers: power is literally energy spent
powerLevelDistillation (comment)  --[recorded]--> powerLevels: "distill some vision for that"
fieldEnergyLevels (relay, 09-18)  --[inferred]--> powerLevels: Luna ultra-low, Terra low, Sol medium, Astra high
Vision/modelRoles.md (distilled)  : older Opus is the wiser seat, chosen for disposition
```

**Candidate operational vision.** Power level is how much energy a job spends, and it is chosen by model, never by effort setting: harness effort stays medium. Four levels: Luna ultra-low, Terra low, Sol medium, Astra high. The field uses ultra-low flows for testing and watching; Field Sol is the primary field seat, Field Astra its high-power companion. Design, thinking, and psyche interaction run on the wiser seat, the older Opus or the newest Fable.

Condenses: the eight records above.

**Skills.** Under your rule the concept skill is `models` (matching `Intent/models.md`) with `modelRoles` and the energy levels as its faces. No `model-roles` skill directory exists today.

**Ready for distillation.** The effort statement already stands in `Intent/models.md` as reviewed. The four energy levels: yes, into `Vision/modelRoles.md` or a new `Vision/powerLevels.md`, which you asked for. "Astra high" is inferred from the field seat records; you named only three tiers and said "I guess we can have four".

- **Q14.** Does `Intent/models.md` as it stands satisfy "I want to put something in intent from this", or is there a further sentence you want there?
- **Q15.** Are the four levels Luna, Terra, Sol, Astra, in that order?

## I. CriomOS modularity and hardware types

```
criomosModularHardware (09-18)        : stock harnesses; hardware type; stable and next; Libre M5
clusterDataAndHardwareAnatomy (09-18) --[recorded]--> criomosModularHardware: refines the hardware type
codexRemoteVersionRouter (09-18)      --[recorded]--> criomosModularHardware: refines stable and next
clusterDataAndHardwareAnatomy         --[recorded]--> theField: Field verifies at boot
```

**Candidate operational vision.** Harnesses and their desktop apps stay stock in at least one version. Hardware is a cluster data specification: a model table derives architecture and form factor from the model string, a manual override covers unknown hardware, Field verifies at boot. A hardware record has sections for audio, visual, and interface; form factors are variants. Codex remote runs as stable and next; the executable routes to stable when next is newer and to next when stable has moved ahead, so flows migrate without switching by hand.

Condenses: the three records above.

**Skills.** Propose `hardware` as the concept skill, the noun an agent would guess. `operating-system` exists for changing the OS; the version router belongs with `codex-harness`.

**Ready for distillation.** Not yet. All three are single, same-day records, one cut off mid-sentence, and you said "I don't know how to best do this". Design round first.

- **Q16.** Is the hardware record a struct with typed sections, or a vector of capabilities? You offered both.

## J. Delegation chain

```
delegationChain (09-18)        : design with Fable, formalize, hand to Codex Astra, sub-delegate to Sol
mainFlowUsesSubflows (relay)   --[inferred]--> delegationChain: same principle at the main-flow level
situationReportAndMediumLayer  --[recorded]--> delegationChain: medium-layer counterparts as peers
fableRestartWithRecoveredVision (comment) --[recorded]--> delegationChain: this very report is its product
```

**Candidate operational vision.** Psyche designs with Fable and formalizes the operational vision. Codex Astra, the Mind primary, implements and may give design input; valid input changes the vision before implementation starts, not during. Astra sub-delegates minor work to Sol. A main flow does not do the work; it uses subflows. Psyche Medium, Mind Sol, and Field Sol operate as medium-layer peers.

**Skills.** `main-flow` exists and is not agent-loadable; you asked whether it was made important. The peer operating model is a section there.

**Ready for distillation.** "A main flow uses subflows" is repeated across 09-18 records and corrections. Candidate for Intent.

- **Q17.** Should "a main flow does not do the work, it uses subflows" be Intent?

## Distillation readiness

| Topic | Destination | Status | Blocker |
|---|---|---|---|
| Triad | Vision/psyche.md | ready | Q1 on "mind" |
| Three data repos, Primary Next | Vision/psyche.md | ready | none |
| Messenger, datom form, psyche distinction | Vision/messaging.md | ready | Q5 |
| Flow roles, "of" naming | Vision/flowNexus.md | ready | Q7 names the topic |
| Transcript as log | Vision/transcript.md (new) | ready | Q8 tension surfaced |
| Skills are vision | Vision/psyche.md or skills.md | ready | Q11, Q12 |
| Energy levels | Vision/powerLevels.md (new) | ready | Q15 |
| Effort | Intent/models.md | done | Q14 confirms |
| Main flow uses subflows | Intent | proposed | Q17 |
| Relay all living words | Intent | proposed | Q6 |
| Signal handshake | Vision/signal.md | not yet | design round |
| Hardware, CriomOS | Vision/hardware.md (new) | not yet | design round |
| Private layer | none | not active | charter only |

## What Mind Astra builds first

The proof of concept from the earlier picture stands: a reader that walks every heading in Vision, Intent, vision-raw, and the flows, emits one record per statement, and leaves edges empty where nothing states them. This picture adds the marks: a record's edge is `Recorded` when the source states it and `Inferred` when an agent read it. Its first witness is cluster H, whose edges are named above and mostly recorded. Astra owns this; Fable implements nothing.

## Where this picture is thin

- Every 09-18 record was heard by one flow or relayed once. No statement this week has a second, independent hearing.
- Nine relays came through Field Sol 33ba2b. A relay is verbatim by instruction, not by witness.
- The artifact comments were read by Psyche Medium from the earlier report. I have not seen the comment surface myself.
- The `field` skill exists and diverges from the brief, which called it new. Other brief claims were checked against the records; that one was wrong.
- "Astra high" as the fourth level is inferred.

## Sources

Brief: `flows/b05237/fable-vision-brief.md`. Dependency report: `flows/b05237/vision-dependency-report.md`. Earlier picture: `flows/056f6d/reports/vision-dependency-picture.md`. Raw records read whole: all 48 files under `flows/b05237/vision/`; `flows/9993b5/vision/` psycheVsMind, mindMemory, easyFlowDispatch, flowAnatomy, flowIdLayers, transcriptArchive, powerLevels, callerIdentity, transcriptOverFiles, structuredLog; `flows/108ab0/vision/` operational-skillsAreVision, operational-skillIsVisionUnified, operational-primaryIsPsyche, operational-distillationHierarchy; `flows/1ac573/vision/` operational-effortIsAlwaysMedium, operational-modelRoles; `flows/c7128c/vision/` visualization, jobEffortLevels, transcriptAndMachineFlow; `flows/78c93c/vision/witnesses-and-reports.md`; `flows/6cc91b/vision/privateLayer.md`. Distilled: `Vision/psyche.md`, `distillation.md`, `messaging.md`, `modelRoles.md`, `flowNexus.md`, `remembering.md`; `Intent/models.md`. Skill directories listed under `.claude/skills/`.
