# Raw psyche supersession inventory

Read-only inventory of `flows/*/vision/*.md`, `flows/*/notion/*.md` and `vision-raw/*.md`, produced by flow da2038 on 2026-10-14. No record was edited.

## How this was made, and what is witnessed

- Witnessed (a script parsed the files this turn): 1931 files, 3729 records. A record is a `## ` block; 251 files hold one record under a `# ` heading and count as one record each.
- Witnessed: every 'later words' quote in section 2 was checked as a substring of the later record's text by the same script. The earlier-record lists were chosen by reading; only the later quote is machine-checked.
- The flow's own inference, not witnessed as the living's meaning: that a later record 'overrules' an earlier one, the effect size, and every candidate list in sections 4 and 5. Section 2 lists only cases where the later words say so; the rest is under 'unclear'.
- Dates: 1258 records carry a date in their `-- psyche` line, 1148 in their heading, and 1323 have none, so their date is the first git commit of their file, marked `~` (a file may have grown after that commit). The repository history starts 2026-05-06; all records fall 2026-08 to 2026-10.
- Records in `archive-*.md` files are already crystallized (their text moved into a vision skill and the original kept). Deleting them is a different decision from deleting a live raw record; they are marked `[A]` below.
- Not witnessed: whether a rule was later re-landed in a skill in changed form. Where a group touches a skill I name it from a read of `/git/github.com/LiGoldragon/psyche-context/skills` (50 commits, small files).

## 1. Counts

- Records: 3729 total; vision 3475, notion 127, legacy `vision-raw` 127. In `archive-*` files: 447. Live: 3282.
- Topic file names: 1169 (counting `archive-x` and `x` as different names); 1118 after stripping `archive-` and `operational-` prefixes. Flows with raw records: 268.
- By month (date rule above): 2026-08 747, 2026-09 1777, 2026-10 1195, ? 10.
- Duplicates, same quoted words (25+ characters, punctuation and case ignored): 268 groups, 360 copy records (264 groups span several flows). Records whose whole quoted text sits inside a longer record of another flow: 259 (section 3b). Deletable as redundant: up to 619 records.
- Records with fewer than 25 characters of quoted words (not tested for duplicates): 114.

### Records per topic file name (top 60; flows in brackets)

| file name | records | flows |
|---|---|---|
| flow.md | 140 | 23 |
| books.md | 116 | 25 |
| ethos.md | 103 | 28 |
| skills.md | 77 | 22 |
| messaging.md | 76 | 27 |
| archive-kinds.md | 52 | 8 |
| nexus.md | 40 | 18 |
| skillDesigning.md | 39 | 15 |
| distillation.md | 39 | 15 |
| presentation.md | 38 | 9 |
| archive-datom.md | 34 | 8 |
| flashbooks.md | 31 | 5 |
| voices.md | 30 | 7 |
| gradientsOfAuthority.md | 28 | 7 |
| archive-datomSyntax.md | 28 | 9 |
| archive-protos.md | 28 | 6 |
| launch.md | 27 | 7 |
| archive-nexus.md | 26 | 7 |
| communication.md | 25 | 7 |
| layers.md | 23 | 10 |
| flowLifecycle.md | 22 | 13 |
| context-modules.md | 22 | 1 |
| datom.md | 21 | 7 |
| meaningLanguage.md | 21 | 4 |
| archive-ethos.md | 20 | 7 |
| subflows.md | 19 | 10 |
| designPractice.md | 19 | 6 |
| psycheLogStructure.md | 18 | 7 |
| deployment.md | 18 | 10 |
| identifiers.md | 18 | 8 |
| design.md | 17 | 3 |
| spirit.md | 17 | 6 |
| zeusUpdate.md | 16 | 2 |
| persona.md | 16 | 11 |
| seats.md | 16 | 7 |
| models.md | 16 | 8 |
| archive-threeStacks.md | 15 | 5 |
| network.md | 15 | 10 |
| rustComponentArchitecture.md | 15 | 7 |
| operational-herdrVoiceAccess.md | 15 | 1 |
| vocabulary.md | 14 | 8 |
| refresh.md | 14 | 7 |
| speech.md | 14 | 7 |
| contextModules.md | 14 | 7 |
| flowNexus.md | 13 | 6 |
| psyche.md | 13 | 6 |
| anatomy.md | 13 | 1 |
| logging.md | 12 | 7 |
| source.md | 12 | 2 |
| archive-traitsAsCapabilities.md | 12 | 4 |
| letsUseTheSameVocabulary.md | 12 | 5 |
| curriculum.md | 12 | 6 |
| flowArtifacts.md | 12 | 2 |
| messenger.md | 12 | 4 |
| hostEnvironmentRecovery.md | 11 | 3 |
| flowIdentity.md | 11 | 5 |
| operational-designMosaic.md | 11 | 1 |
| falseConfidence.md | 11 | 2 |
| transcriptNexus.md | 11 | 1 |
| message.md | 11 | 2 |

### Every topic file name with its record count (count; names with the same count are grouped)

- **52**: archive-kinds
- **40**: nexus
- **39**: distillation, skillDesigning
- **38**: presentation
- **34**: archive-datom
- **31**: flashbooks
- **30**: voices
- **28**: archive-datomSyntax, archive-protos, gradientsOfAuthority
- **27**: launch
- **26**: archive-nexus
- **25**: communication
- **23**: layers
- **22**: context-modules, flowLifecycle
- **21**: datom, meaningLanguage
- **20**: archive-ethos
- **19**: designPractice, subflows
- **18**: deployment, identifiers, psycheLogStructure
- **17**: design, spirit
- **16**: models, persona, seats, zeusUpdate
- **15**: archive-threeStacks, network, operational-herdrVoiceAccess, rustComponentArchitecture
- **14**: contextModules, refresh, speech, vocabulary
- **13**: anatomy, flowNexus, psyche
- **12**: archive-traitsAsCapabilities, curriculum, flowArtifacts, letsUseTheSameVocabulary, logging, messenger, source
- **11**: falseConfidence, flowIdentity, hostEnvironmentRecovery, message, operational-designMosaic, transcriptNexus
- **10**: archive-prospective, archive-protosIsTheSharedStyle, archive-signalIsOurMessagingLayer, building, prometheus, testTravesties
- **9**: actorLibrary, archive-portion, context, skillsRepository, stack, systemPrompt, vision
- **8**: awarenessIsGeneralUnderstanding, entryFiles, hijackRepositories, hooks, psycheLogging, quota, threeStacks, titles, tools
- **7**: archive-distillation, archive-ethosFileAnatomy, archive-meaningLanguage, archive-structuredStringType, archive-vocabulary, behavior, escalationHierarchy, flowTool, hook, importResolution, layerMatching, mainFunction, managementDelegation, messages, pairHierarchy, parallelSessions, psycheFlows, setupIndependentInterfaces
- **6**: archive-anatomy, archive-nexusTraits, authority, contextStrata, criome, flowAnatomy, flowOperatorNotes, highPowerAndUpgradePipeline, listenerWisprFlow, mainFlow, mainFlowRefreshAndRoles, metaHarness, metaflow, mind, ouranosRedeploy, questions, reporting, signal, skillPromotionAndLayering, skillSourceKinds, stableNext, subagents, topStratum, triad, tuples, visualDiffAndLeanComments, workspace
- **5**: Fable, archive-concept, archive-datomizable, archive-ethosMonolith, archive-ethosTraitSyntax, clojure, ethos-in-clojure, fieldTool, flashbookIllustration, flow-component, flowDeploy, flowKnowledge, flowLaunching, flowRefresh, flows, harnessModelOntology, infrastructure, intent, interfaces, layerVocabulary, layerZero, livingMessenger, locks, metaflowDimensions, modelFlows, negatives, operational-modelRoles, psycheLayers, quotas, remembering, remoteControl, remoteControlAllTheCodexTuiSessionsICreate, roles, sandbox, skillKindsTaxonomy, skillTraining, speechToText, worldModelBeforeCode
- **4**: addressing, agentIntercomGraphical, ai-model-placement, archive-encodedFormIsTheCode, archive-ethosSourceFiles, archive-ethosTypes, archive-spokenVocabulary, archive-textualTypes, archive-visionImpurities, callerIdentity, commitMessage, committing, correction, emacsPlugin, encapsulation, fableContext, flashbookMobile, flow-startup, flowDaemon, flowRole, flowSkills, hostUpdates, illustrations, incorrectness, integration, live-installation-image, livingInput, locking, meshNetwork, pairedFlows, permissions, promptCrafting, psycheCore, psycheDataArchitecture, psychePairAnatomy, relay, repoChecklist, reports, secrets, signalIsOurMessagingLayer, terminal, testing, thirdModel, trainingRepo, visionAsSkillSource, visionBooks, visualPublication, voice-relay
- **3**: actualProblemsWeAreSolving, agentIntercom, archive-designPractice, archive-ethosInterfaces, archive-meaning, archive-orchestrateDeployment, archive-protosizable, archive-remembering, archive-structuralParsing, archive-subflows, artifactMigration, aspects, assembly, audits, cause, clojure-flow, cloud, cluster, cluster-builds, codeIsLanguage, contactingTheLiving, curriculumSubagentGap, data, decomposable, ethosLibrary, finalResponse, flashbookBookShape, flowNaming, flowsNotAgents, hashes, herdrSessions, highLevelView, horizon, identifier, illustratedTranscriptPresentationAndPsycheLogging, itsATranslator, jev, kinds, livingHistoryCapture20260921, lojixOwnership, machineAnatomy, mainFlowMode, messagingUp, modelRoles, newtypeWrappingAndSingleFieldStructs, noctalia, openSourceHarness, operational-fieldReapingJudgmentAndExecution, operational-psycheClusters, packageAuditProtocol, paired-flows, polling, psycheMessages, publishing, remoteAccess, repositories, roleDescriptions, rollingDistillation, router, rust, skillTypes, skillVoice, softwareAnatomySkill, spokenVocabulary, stateful, surgicalDataEditor, terminology, testRepos, transcriptExtraction, transcriptOverFiles, verifiedInformation, visionNotification, visualCollaboration, visualization, visuals, wisprInteraction
- **2**: accounting, agentAuthentication, aiModels, annotation, archive-actorLibrary, archive-datum, archive-distillationNegatives, archive-dotosFiles, archive-firstPrompt, archive-flowDaemon, archive-headedAndContained, archive-highLevelView, archive-interactions, archive-interfaceRootEnumerators, archive-layers, archive-metaOrchestrate, archive-multiPass, archive-operational-openCodeRemoteAccess, archive-persona, archive-rustCodeFromTheData, archive-rustComponentArchitecture, archive-signal, asks, birdProfile, bookFlowcharts, browser-control, capability, capsule, claudeRemoteControl, cljTools, clusterData, clusterMonitoring, codeAnalysisTools, codex, codex-session-creation, codex-upgrades, codexAndClaude, commonalityBetweenTheOsAndHomeRepos, concept, contextVisibility, core, daisyChain, datomMessaging, declarative-features, delineate, designBook, deterministicWork, dispatches, distilledVision, domainKnowledgePlacement, draftIdeasForImprovement, durableAgentHost, effort, ethos-code-in-vision, ethos-json, everyConceptShouldHaveItsRepo, everythingIsInTheDaemon, fableRole, fieldMaintenanceAndRefresh, flashbook, flow-ids, flow-refresh, flowAspect, flowEffort, flowRestart, harness, heartbeat, hexis, homeEquivalence, independent-analysis, lateralThenUpRouting, living-messenger, llmUnderstanding, lojix, mainFlowWrites, majorRecoveryEffort, makeshift, mediumGraphicalNodes, mentci, mesh, metaflow-ethos, mindRoles, model-roles, names, namesOfFlows, nexusAnatomy, nexusTraits, node, nonIdealAgents, notification, observe, openCode, operational-ethosTypeRoot, operational-fableFlowAndOpusComparison, operational-fieldWorkersAreReapers, operational-flowVsMessage, operational-mentci, operational-nixBuiltTestingAndRustDataSeparation, operational-openCodeRemoteAccess, operational-visionLedAudit, orchestrate, orchestrateRealization, ouranos, overtalking, partnerChannel, pipeline, privateLayer, prometheus-wifi, prometheusBuilder, prometheusZeusInternetPropagationAndTailnetAlternatives, proposals, protosIsTheSharedStyle, psycheHonesty, psycheSonnet, psycheVoice, quotaTracking, reachingTheLiving, readingTheLiving, realizer, repositoryClassification, seat, sema, sessionLog, shastra, signalForms, single-field-structs, skillCorrectnessPrinciple, skillsRepoSourceOnly, soul, sourceNotCrate, speakingToTheLiving, speech-to-text, spirit-system-prompt, streamAsFourthKindMvpFirst, subflowBriefs, subflowIdentity, theBestShape, topics, transcriptNotFiles, transcriptTool, typedPrompts, unattributed-2026-09-24, uncommittedChanges, unity, usb-ethernet-sharing, useASubflowToPutTheReportTogether, v2, versionControl, virtualMachine, wake, witnesses, workPractice, workspace20, workspaces, zeus
- **1**: Luna-Flow, README, agent-intercom, agentToMachine, aiNode, anatomyOfCommunicatingThinkingAndReacting, approval, archive-colonConfusion, archive-colonFormTransformerSyntax, archive-colonLegalInStringPosition, archive-committing, archive-datomInteger, archive-datomIsData, archive-datomMaps, archive-datomNexus, archive-delimiters, archive-directionAsymmetry, archive-encodedFormFingerprintTraitDesign, archive-ethosDotosDivisionAndHelp, archive-ethosNamespaces, archive-ethosNonRepetitionLaw, archive-horizon, archive-jev, archive-metaCliIsComponentDashMeta, archive-metaSignalNotOptional, archive-newtypeWrappingAndSingleFieldStructs, archive-nexuses, archive-operational-asyncSubflowsAndMeaningLanguage, archive-operational-explicitFilePathCommits, archive-operational-fieldUltraLowRoutesSubflowRequests, archive-operational-horizonNexusAndNodeResources, archive-operational-meaningContentAddressedAnnotation, archive-operational-meaningDualSanskritEnglishNames, archive-operational-meaningGarbageCollectionAndOntology, archive-operational-meaningLanguageAnnotationLayers, archive-operational-meaningLanguageLogographic, archive-operational-pocSandboxIntent, archive-operational-pocSandboxVmFirst, archive-operational-subflowRequestIdAndAsync, archive-operational-vaisheshikaRuledAndSyntaxQuestion, archive-orchestrateSkill, archive-passes, archive-personaServiceAndNexusImagery-20260923, archive-schemaSyntax, archive-sema, archive-symbols, archive-text, archive-tuples, archive-x11, arity, artifacts, ashtadhyayiKnowledgeBase, aspect, aspect-topics, attunement, autoCommitOnWrite, automation, autonomousClusterOperation, autonomousOperation, awareness, basePrompt, billing, blockPropagation, blockedCallsAndOtherModel, blocks-for-the-living, book, bookRendering, bookTitles, books-as-web, booksAndProposals, bootstrap, build-placement, chainedNamesScrapped, checkboxes, checks, claude-persistence, claudeDesktop, claudeDesktopUsesOurClaudeCode, clojure-builds, cloudRemoteServer, cluster-survey, clusterNotBlocking, clusterSpec, clusterSurvey, codex-update, codexAsDoing, codexDerivation, codexModel, codexNeededHere, codexOnlySkill, codexRelaysPsyche, codexRemoteAccess, codexScarcity, codexTerminalReconnect, colonFormTransformerSyntax, commentary, commitQueue, commitSubflowScript, commits, commonGround, compensation, concentratedVision, containers, context-refresh, context-visibility, contextSize, contexts, continuous-names, continuous-names-messaging, continuousRecordingUsingWisprFlowChunks, cosmological-claims, council, criomOsUpgrade, criomos, curriculumAndTriadSkillGeneration, curriculumNexus, datom-messaging, datomMcp, datomStructuralEditing, datomSyntax, datomVocabulary, deepsekHarness, default-effort, defaultOpeningLogic, delimiters, demandDrivenDesign, deployIncludesUserEnvironment, deployment-accounting, deploymentSelection, design-by-astra, designExamples, designer, desktopCodexIntegration, dictation-vocabulary, dictationVocabulary, disavowAuthorNeverWrites, diskSpace, distillAnythingThatIsUsed, distillEveryTurn, distillationNegatives, distillationSources, dotOpensDelimiterEverythingIsData, dualingo-compositions, easyFlowDispatch, editCoordination, editNexusName, encodedFormIsTheCode, epicBranches, ethos-and-example-datom, ethosAndBookComments, ethosComments, ethosDelta, ethosInlineTypeDeclaration, ethosNames, ethosNextGeneration, ethosNexus, expands-vertically, explodedForm, fieldLifecycleOperator, fieldNexusSystemQuery, fieldOwnership, fieldScriptsAndAspectRepositories, fieldStack, finding-out, firstPrompt, fixMessagingApproval, flashbookDesignAndFormat, flashbookIllustrationStyle, flashbookImageryScope, flashbookResponsiveDesign, flashbookStylingAndCurriculum, flashbookVocabulary, flow-context-injection, flow-identifiers, flow-installation, flow-names, flow-registry, flow-retrieval, flowArmsItselfToWatchTheArtifact, flowClj, flowContextInjection, flowCorrections, flowGarbageCollection, flowIdLayers, flowLogging, flowModel, flowMovesBetweenGenerations, flowNexusUse, flowOriginClue, flowRefreshAndArchive, flowTypes, focus, focus-stability-fresh-flows-and-hygiene, forge, freshFieldFlow, freshFlowsAndArchive, fullAccessPermission, fullSystemAccess, garbageCollecting, gatedFlows, genericParametersAreTraits, ghostCollectionAndFlowMaintenance, google, haikuForPsycheUltraLow, handover, harnessBlockDocumentation, harnessNexus, harnessPurity, harnessReplacement, harnessResearchAndArchives, harnessSkills, harnessVisualIndicatorsAndRemoteControl, harnessVocabulary, harnesses, healingAspect, helpMenu, herdr, home, host-environment-recovery, hostTrust, iast-notation, ideaEditing, identifying-strings, if-i-ask-for-a-new-flow, illustration, independentReview, inlineReportAndMarkerSkill, installingSoftwareStatefully, integratorFlow, interflowMessaging, internetPropagation, interpretation, investigation, invocationSystem, jobEffortLevels, knowledge, landing, lastSuggestion, launchGovernance, launchOnMain, launchPrompt, law, layerNames, layerNaming, layerVocabularyAndReview, livingCommunication, low-power-mode, lowPsycheRole, lunaForUltraLowEverywhere, machine-generated-content, mainFlowShouldNeverTryToLocateAFile, mainForEverything, mainRoles, manualPostResetSkillRestoration, marker, memory, mentci-egui, mentciWeb, mergeQueue, messageAndFlow, messageSize, messagingBootstrap, messagingInterface, messagingIsScripts, messagingVerbatimAuthorization, meta-flow, metaCli, metaCliIsComponentDashMeta, metaOrchestrate, metaflow-naming, midLayerReview, middleLayerRouting, migration, mindMemory, minePreResetForImplementationStandard, minimalFlake, mobile, model-flow-emergency, modelComparison, modelGovernance, modelNamedSeatsAndAdaptiveRouting, modelPlacement, modelSpendEmergency, modifier, multiFormConcepts, namespace, naming, networking, nexus-configuration, nexusComponentDeploymentAndTriadRoles, nexusEntryPoint, nexusScaffolding, nightWork, nix-training, nixExecution, noHumanTypingOnKeyboards, noImagesInRepo, noMoreBranches, noRetryRefused, notifications, observerFixtureBlessed, obsoleteFlowsMustNotReawaken, oneSharedPrimary, ontology, openSourceModels, openSourceStack, openaiLacksTheFeatureIWant, operation, operational-abruptPerHarness, operational-agentToPsycheMessaging, operational-allPsychesRelayUpChain, operational-astraGoesWithItsProposal, operational-centralMessenger, operational-clusterDataAndHardwareAnatomy, operational-codexRemoteVersionRouter, operational-commentWithoutSendToClaude, operational-commitMessageIdentifiesEpic, operational-conversationAppRoutes, operational-coreAndExtendedVision, operational-coreSoulCluster, operational-criomeClusterIsTheTailnet, operational-criomosModularHardware, operational-curriculumAsModuleSystem, operational-curriculumSkillsRepo, operational-datomEverythingSystemPrompt, operational-datomFinalResponseLowJudgmentReap, operational-datomHackyMessagingAndLanguageUpgrade, operational-datomLanguageForNexusClis, operational-datomObservabilityAndMindLayer, operational-defaultModelPsycheMediumClaude, operational-delegationChain, operational-delegationTierRules, operational-deployOnTheHostYoureOn, operational-diskHygiene, operational-distillationHierarchy, operational-effortIntoIntent, operational-effortIsAlwaysMedium, operational-ethosEscapeDelimiter, operational-ethosSpecSkillAndTriadBranches, operational-fableRestartWithRecoveredVision, operational-fatPromptAndCustomSystemPrompt, operational-fieldEnergyLevels, operational-fieldFlowNotReaper, operational-fieldIsTheAggregateOfMachines, operational-fieldKeepsThingsWorking, operational-fieldLunaWatcherAndArchiving, operational-fieldMaintainsAndFixes, operational-fieldRefreshSuccession, operational-fieldTestingAndUltraLow, operational-fieldTwoSeatsAndRefreshNaming, operational-finalResponseDatomObject, operational-finalResponseLifecycleHook, operational-flowCLIStartsSessions, operational-flowCliListAttachProvenance, operational-flowDatomCLIAndSignalLibrary, operational-flowDatomLauncherLanguage, operational-flowHerdrMessageTriangle, operational-flowOwnsHerdr, operational-flowStartsFlows, operational-freshPrimary, operational-fullRefreshAndReorganize, operational-fullSignalCommunicationToPsyche, operational-hackyMessenger, operational-harnessSpecificRules, operational-herderMessagingReport, operational-herderMuxKeypress, operational-herderTriadSpaces, operational-herderUserExperience, operational-herderWindowManagement, operational-hooksAsEventSource, operational-lastResponseIsTheNextEvolution, operational-launcher, operational-logOnMainNowMigrateLater, operational-lowCognitiveReporting, operational-lowFrictionCommunication, operational-mainFlowStartupCorrection, operational-mainFlowUsesSubflows, operational-meaningStructureRootVariant, operational-mentciTalksToPersona, operational-mentciTopologyNotRouter, operational-mermaidThenSvg, operational-messageAsDatomInPrompt, operational-messagePriorityTiers, operational-messagingAccuracyAndFieldAwareness, operational-messagingDatomSyntax, operational-messagingSimpleSystem, operational-messagingToDeployment, operational-messengerGlanceApproval, operational-messengerPaneSyncFailure, operational-messengerSynchronizesRoster, operational-messengerUsesDatomNow, operational-mind, operational-mindMapsComponents, operational-mindMediumIsSol, operational-mirrorToEveryoneAndRoster, operational-mirrorToPsycheMedium, operational-mirroredMessagesAreAddressed, operational-modelDeclaredInOnePlace, operational-multiplexerInjection, operational-nameSessionAfterAncestor, operational-nexusProcessObjectsAndEthosInDatom, operational-nightWorkDirective, operational-olderOpusIs46, operational-ongoingAstraOpusInterraction, operational-ontologySurveyReady, operational-openCodeAndroidApp, operational-openCodeOnUranusNotZeus, operational-openCodeTestWithCodexSubscription, operational-openSourceRemoteAccess, operational-openStackOnCodex, operational-operationalSkillsRepo, operational-ownApp, operational-paneDeathAndMessagingIndex, operational-populateIntentWithTheAutomatic, operational-powerLevelDistillation, operational-prefixEverythingVisionAndOperational, operational-primaryIsPsyche, operational-primaryNextPsycheLogging, operational-privateLayerCoreLayer, operational-programmaticPromptComposition, operational-promptMosaicComposition, operational-psycheAndMind, operational-psycheGeneratedMessaging, operational-psycheIdleTimerHook, operational-psycheLogDuty, operational-psycheMindAndTheThirdComponent, operational-psycheMindAstra, operational-psychePropagation, operational-psychePropagationAndNamingAndInfrastructure, operational-pushMessagingForEmergency, operational-quotaAwarenessSystem, operational-quotaBurnRateHook, operational-quotaBurnRateVisualGraphs, operational-quotaVisualizationHook, operational-reapAndArchiveOldSessions, operational-reapReplacedSessions, operational-reaperIsForensic, operational-reaperSubflow, operational-reapingOnRefreshAndFlowEndHook, operational-recognizePsycheTyped, operational-refreshAndImplementClosestLayer, operational-refreshFlowAndMessageFlowCoordination, operational-refreshKeyProgrammaticallyInjected, operational-refreshOutboxAndMessageChannels, operational-releaseContribution, operational-remoteControlResearchReport, operational-renameEverythingAtomically, operational-reportFlow, operational-reportFormat, operational-reportIsTranscript, operational-reportWatcherAndIllustrator, operational-responseAnatomyAndPowerAllocation, operational-restartDirectives, operational-retiredResponseAndReaping, operational-sameTreeAndMerger, operational-signalOriginHandshake, operational-situationReportAndMediumLayerOperation, operational-skillIsVisionPrefixed, operational-skillIsVisionUnified, operational-skillLagsVisionObservability, operational-skillTypes, operational-skillTypesTriad, operational-skillsAreVision, operational-skillsAreVisionRepropagated, operational-skillsMissTheCliShape, operational-slideFlowAndFlowAuthorization, operational-standardMessagingSkill, operational-storageReportAndHomeDirectoryGuideline, operational-structuredEditingDatomEvolution, operational-testSkillForIllustration, operational-testTypeSkills, operational-theField, operational-threeDataReposAndPrimaryNext, operational-timeBasedMergeSlots, operational-toolsNotShellScripts, operational-transcriptAsLog, operational-transcriptAsLogDatomNotes, operational-transcriptBlockExtraction, operational-transcriptMustNotBeLost, operational-triadWorkDivision, operational-twelveFoldRolesOnly, operational-typedMessagesDistinguishPsyche, operational-unifiedVisionDocument, operational-unityIsMentciClient, operational-unityMarksPsyche, operational-unityTailnetApp, operational-unityWebNextToDaemon, operational-unityWebSpeaksSignal, operational-verticalRoutingThroughPsycheFirst, operational-visionIsSkill, operational-visionIsSkillThreeRepos, operational-visionReportVersusSituationReport, operational-visualizationToolkitAndTestingModules, operational-voicePsycheDesktopAccess, operational-webOfVisionVisualizations, operational-whoTalksToWhom, operational-wisprFlowCodexPaste, operational-xmppToPsyche, operationalNoteDatomPattern, operationalVision, operatorsNotes, oracle, orca, orchestrateCommitBinding, orchestrateDeployment, orchestrateInPath, orchestrateLocking, orchestrateSkill, orchestrator, outputNoise, pair, pairs, paneLifecycle, parserIsTheParser, pathLocks, perHarnessSkills, personaMetaHarness, personaServiceAndNexusImagery-20260923, philosophy, pi, piHarness, piper, pocShapeConfirmed, pod, pollingSystems, power, powerLevels, presentation-publication, presentationFlow, presentations, primaryNext, primarySeats, primarySkeleton, priorities, priority, private-data-separation, progression, prometheus-networking, prometheus-zeus-mesh-possibilities, prometheusBuildPolicy, prometheusWifiReliability, promptExplainsNothingTheHarnessDoesAutomatically, prototypes, psyche-role, psycheCaptureAudit, psycheChronology, psycheFacingModel, psycheGeneratedMessaging, psycheInSkills, psycheInjection, psycheInteraction, psycheIsDistillation, psycheIsntPerAspect, psycheMedium, psychePower, psychePropagation, psycheSharing, psycheSystem, psycheTool, psycheVersusMachineMessaging, psycheVsMind, publication, quota-gauge-program, quota-metrics, quotaAccounting, rating, rebootstrapWithPowers, recording, redeploying-the-operating-system-after-a-user-is-deployed, refresh-hooks, refreshAddendum, refreshAutomation, refreshHooks, refreshPurpose, refreshThresholdAndCacheSnapshot, registration, registry, relayUpChain, relaying, reminders, remoteControlAndCleanup, remoteFlag, remoteRotation, remoteTitlesAndSkillDeployment, repeatingLikeThis, replacementKillsOldSystem, reportFeedback, responsePresentation, retirement, reusing-a-commented-book, role, rollingCodexServices, routing-examples, runtime, rustLayering, rustTypes, sandboxedTest, seat-abstraction, seat-migration, seatNames, sectionsExistToConferTraits, security, seeds, selectiveImport, selfAudit, semaCommunication, semi-sandbox, senseMakingFlow, session-log, session-reaping, sessionAccess, sessionArchiving, sessionClosing, sessionNames, sharedCheckout, sharedWorkspace, shortHeaderNotNow, shortTermFixNotTheFullJob, signalAndSemaDistillation, simple-working-system, simpleWorkingSystem, skill-catch-up, skill-catch-up-wave-approved, skill-proposals, skillDesign, skillEditProposal, skillLandingBySubflow, skillProposals, skillsAsInterface, sonnet-comments, sources, specializedFlows, specificationUpdatesSkills, spending, spiritComponentAndFile, sprawlFix, startup-task, stateful-installation, statement, statusPresentation, storage, streamDisqualifiesBundling, streamSection, structuredLog, structuredStringType, stupidGuidance, subagentModel, subflowDispatch, subflowResponses, subjectivity, surveyingAllFlows, swiping-left-right, system, systemCheckupAgentAndAutoWake, systemPromptRepository, systemStatus, tailnet, tailscale, temporaryConditions, terminalCell, tests, theLiving, thingsHappening, thinkingMachine, thinkingMachineProcedures, thinkingPhases, thinkingProcess, threadNaming, tokenCosts, topic-flows, topicFlows, traitsAsCapabilities, transcriptAndMachineFlow, transcriptArchive, transcriptIndex, transcriptSelfReference, transcripts, transitiveNetworkTopologyAndCertificateWifi, transparentRefresh, tuiAndDesktopVersions, twelveMainsProportionalAssignment, typeEthos, typedString, types, unifiedWifiRoamingAndCertAuth, usage, userInterface, userOnlyFlagPurpose, userPromptLayer, versioning, vision-led-audit-and-fable, visionAccessibleToAll, visionAndTools, visionImpurities, visionPurity, visionUpkeep, visualizationPipelineAndFlowLifecycle, voice-registry, voiceLuna, voiceSession, vscodium, waiting, watching-skill, web-conversations, webAccess, webChatTranscripts, webInteraction, what-the-book-is, who-implements-skill-proposals, why-is-rust-analyzer-running, wifi, wisprFlow, wisprFlowService, witness-reuse, witnesses-and-reports, wordIdentifiers, wordIds, work, workEstimation, working-system, workspace-2.0, workspaceAndWhitelistIgnore, workspaceProvisioning, worktreeHygiene, writing

## 2. Superseded: a later record says it rolls back, overrules or simplifies an earlier one

Order is by how much the change simplifies (large, medium, small), my judgment. `[A]` marks an earlier record that is already in an `archive-*` file. Each row is `path:line`, date, heading. Copies of the same words in other flows are in section 3; delete them with their original.

### S1. Voice and seat vocabulary replaced by the metaflow and the core topic (large)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/01e496/vision/seat.md:3` | 2026-10-02 | The abstraction of a seat, under a better term |
| `flows/01e496/vision/messaging.md:3` | 2026-10-02 | Seats talk by seat name |
| `flows/91ea9f/vision/addressing.md:15` | 2026-10-02 | A voice's name is two variants, not a string |
| `flows/3ec648/vision/voices.md:3` | 2026-10-02 | A voice is aspect and rank, nine voices, three by three |
| `flows/5578cc/vision/vocabulary.md:3` | 2026-10-03 | Voices, not seats |
| `flows/5578cc/vision/flow.md:27` | 2026-10-03 | Two registries: the true one with the ids, and the voices |
| `flows/edf227/vision/flowRole.md:3` | 2026-10-03 | Role is an enum: voice, system audit, live psyche interaction, impleme |
| `flows/edf227/vision/flowRole.md:20` | 2026-10-03 | Voice is a struct of Aspect and Layer |
| `flows/aa887c/vision/ethos.md:3` | 2026-10-04~ | Voice is a struct of aspect and layer; structs over chained variants |
| `flows/bad807/notion/voices.md:3` | 2026-10-04 | The design is evolving fast with Jev in the middle of typed communicat |
| `flows/8475a9/vision/voices.md:3` | 2026-10-05 | The format of a voice's name: a bare struct of aspect, layer and flow  |
| `flows/8475a9/vision/voices.md:13` | 2026-10-05 | A registry changes which flow is associated with a voice when there is |
| `flows/8475a9/vision/voices.md:71` | 2026-10-05 | The voice is a type of metaflow; there are specialized metaflows |
| `flows/8475a9/vision/messenger.md:3` | 2026-10-05 | The messenger identifies a message's originator by voice only, "Mind T |
| `flows/d66c26/vision/voices.md:17` | 2026-10-05 | 2026-10-05 — A flow ID and a role |
| `flows/f5a6e9/vision/flow.md:3` | 2026-10-07~ | A voice is a permanent metaflow, one that may sleep and is woken by a  |

Later record: `flows/875960/vision/flow.md:11` (2026-10-11) 2026-10-11 — the voice concept is gone; the default topic is core, the permanent topic, the last to stand

Why: later words "we've gotten rid of the voice concept".

Note: The 'seat' word was already dropped 2026-10-05 (8475a9 voices:63 'no seat'); d4ae97 flow:85 (2026-10-07) 'There's no voice'. The aspect+layer shape (Mind Tertiary) survives as the name; the concept 'voice' and its registry of voices do not. 3ec648 voices:3 (nine voices, three by three) is the earliest. Earlier records here: 16; exact copies of them in other flows: 18.

### S2. Curriculum/skill-generation machinery cut down to dirty-simple, then context repositories (large)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/48cff7/vision/skillKindsTaxonomy.md:3` | 2026-09-16 | 2026-09-16 — the kinds of skill and psyche-level; the future Curriculu |
| `flows/9993b5/vision/curriculumNexus.md:3` | 2026-09-17~ | This is where we want to go: towards Curriculum being a Nexus and taki |
| `flows/108ab0/vision/operational-curriculumAsModuleSystem.md:3` | 2026-09-17~ | Overhaul Curriculum. All this becomes a module system with modules for |
| `flows/108ab0/vision/operational-skillIsVisionUnified.md:3` | 2026-09-17~ | Unify. There is no separate Datom skill and Datom vision — same thing. |
| `flows/b80e55/vision/curriculumAndTriadSkillGeneration.md:3` | 2026-09-20~ | The curriculum generator is just a binary, a nexus with CLIs. Three ty |
| `flows/26c50c/vision/curriculum.md:2` | 2026-09-24 | Vision, skills, and typed generation — 2026-09-24 |

Later record: `flows/183ae0/vision/skills.md:11` (2026-09-29~) Skills leave the Curriculum; three skill repos

Why: later words "not supposed to be in the curriculum anymore".

Note: Chain after the later record: d4ae97 curriculum:12 (2026-10-07) 'We're going to make this really dirty just so that it works... really simple'; 91ea9f skills:19 (2026-10-02) 'get rid of the gold skills concept'; d68c82 context-modules:2 (2026-10-13) 'remove the trial context type'. Later records are kept as live vision; earlier ones overruled. Earlier records here: 6; exact copies of them in other flows: 0.

### S3. Flashbooks (SVG/image illustrations, swipe pages, buttons, Sonnet comments) reduced to red/green books (large)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/1b8ac0/vision/flashbooks.md:13` | 2026-09-20~ | We need illustration: the first page is always an illustration, then o |
| `flows/0625c3/vision/flashbookBookShape.md:5` | 2026-09-20 | "At least three pages to make a book" |
| `flows/0625c3/vision/flashbookBookShape.md:11` | 2026-09-20 | "It's like for kids, and each page has an image" |
| `flows/b80e55/vision/flashbookDesignAndFormat.md:3` | 2026-09-20~ | Each section is a component at a level, with explicit imagery, a flowc |
| `flows/b81560/vision/operational-twelveFoldRolesOnly.md:3` | 2026-09-20~ | You're not the Flashbook Renderer. You're the Psyche Low. The only rol |
| `flows/d8df70/vision/flashbooks.md:3` | 2026-09-23 | Illustrations are generated by an image model, not drawn as SVG |
| `flows/d8df70/vision/flashbooks.md:15` | 2026-09-23 | A new flashbook brings forward only the six to nine most important top |
| `flows/836818/vision/flashbooks.md:17` | 2026-09-23 | Six to nine, illustrations that pull the living in, one rolling flashb |
| `flows/d8df70/vision/flashbooks.md:74` | 2026-09-24 | Three levels of flashbook |
| `flows/1b8ac0/vision/mentciWeb.md:3` | 2026-09-21~ | Make our own web UI, Mentci Web, defined like a Nexus but a full web a |

Later record: `flows/fe945a/vision/books.md:31` (2026-10-01) The book maker is a light Sonnet subagent that makes the page mechanically; graphs instead of illustrations

Why: later words "No need for illustration".

Note: Further rollbacks: 6f51ad presentation:3 / 183ae0 presentation:3 (2026-09-28) 'get rid of the buttons'; 42265e flashbooks:51 and 91ea9f ethos:36 (2026-10-02) 'I don't want these Sonnet comments anymore'; 91ea9f books:77,:93 (2026-10-02) swipe UI forbidden; fe945a books:21 (2026-10-01) no images in the repository; d68c82 books:81 (2026-10-10) 'everything should either be red or green'. The word 'flashbook' survives as 'illustrated book' in the glossary, so only the machinery is overruled. Earlier records here: 10; exact copies of them in other flows: 2.

### S4. High/Medium/Low effort tiers of psyche flows, replaced by layers; effort is always medium (large)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/024bc7/vision/effort.md:3` | 2026-09-13 | 2026-09-13 — High effort is a waste; right now we are in medium mode |
| `flows/b49251/vision/psycheFlows.md:39` | 2026-09-16~ | Three levels of psyche flows, low, medium and high effort, with a Code |
| `flows/b49251/vision/psycheFlows.md:47` | 2026-09-16~ | The psyche stack on Claude: Fable on high power, the old Opus medium,  |
| `flows/b49251/vision/psycheFlows.md:66` | 2026-09-16~ | The psyche flows are the ones the living interacts with most; other fl |
| `flows/f55ec8/vision/psycheLayers.md:3` | 2026-09-17~ | The remote thread names say the type and the model: primary Psyche, th |
| `flows/f55ec8/vision/psycheMedium.md:3` | 2026-09-17~ | Psyche Medium online, the one the living talks to instead of the Fable |

Later record: `flows/1ac573/vision/operational-effortIsAlwaysMedium.md:3` (2026-09-18~) There's been confusion: when the living says "high," flows start Astra on high and Fable on high because it is

Why: later words "it's all medium".

Note: Same day-chain: da1e3f operational-psycheAndMind:3 (2026-09-17) 'The medium is not an effort level; it's a role'; 3ec648 voices:3 (2026-10-02) 'psyche primary, psyche secondary...'; e167d8 roles:3 (2026-09-26) 'not 12 anymore'. The Layer table is now in the base prompt. Earlier records here: 6; exact copies of them in other flows: 0.

### S5. Datom/Protos string and map delimiters: parentheses, curly quotes, guillemet maps, key-value, version number (large)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/a5587095/vision/archive-datomSyntax.md:2` [A] | 2026-08-11 | 2026-08-11 — parentheses must not be unused in Datom |
| `flows/a5587095/vision/archive-datomSyntax.md:14` [A] | 2026-08-11 | 2026-08-11 — parentheses delimit the structured string; one string typ |
| `flows/06196cc7/vision/archive-datomSyntax.md:2` [A] | 2026-08-13 | 2026-08-13 — Meaning postponed in datom; () or curly quotes both land  |
| `flows/06196cc7/vision/archive-datomSyntax.md:53` [A] | 2026-08-14 | 2026-08-14 — parentheses are the default string delimiter; Meaning-as- |
| `flows/06196cc7/vision/archive-datomSyntax.md:79` [A] | 2026-08-14 | 2026-08-14 — paren strings are balance-based; parentheses are markup i |
| `flows/ac1e9ec8/vision/archive-datomSyntax.md:29` [A] | 2026-08-26 | 2026-08-26 — or a dedicated delimiter for maps |
| `flows/ac1e9ec8/vision/archive-datomSyntax.md:95` [A] | 2026-08-26 | 2026-08-26 — curly quotes are the string delimiter; parentheses reserv |
| `flows/04db2fd2/vision/archive-datomMaps.md:7` [A] | 2026-09-03~ | Guillemets for maps; key and value separated by a space |
| `flows/ad19b1/vision/archive-ethos.md:4` [A] | 2026-09-04 | 2026-09-04 — an associated constant is CAPACITY, written with the key- |
| `flows/ad19b1/vision/archive-ethos.md:22` [A] | 2026-09-04 | 2026-09-04 — the constants in the key-value delimiter only works if th |
| `flows/ad19b1/vision/archive-ethos.md:31` [A] | 2026-09-04 | 2026-09-04 — key-value delimiters for sections that cannot have the sa |
| `flows/6329f1/vision/archive-ethos.md:12` [A] | 2026-09-04 | 2026-09-04 — proper ethos is variant-headed, a struct with its version |

Later record: `flows/ad19b1/vision/archive-protos.md:4` (2026-09-04) 2026-09-04 — drop the key-value delimiter and concept entirely from protos and its dialects

Why: later words "drop that delimiter and concept entirely".

Note: Confirmed by e996e8 archive-protos:20 (2026-09-04) 'we've abandoned the key value map delimiters everywhere' and e996e8 archive-ethos:4 'drop the version number altogether'; 564f55 archive-protos:3 (2026-09-08) moves strings to guillemets. All listed records are already in archive- files (crystallized into vision-datom/vision-protos). Earlier records here: 12; exact copies of them in other flows: 1.

### S6. Kinds (the 52-record naming of kinds as qualifiers, verbs and layer capabilities) renamed to traits (large)

Earlier records:

| record | date | heading |
|---|---|---|
| `vision-raw/archive-traitsAsCapabilities.md:21` [A] | 2026-08-13 | 2026-08-13 — common traits are the right abstraction; all protos diale |
| `flows/04db2fd2/vision/archive-kinds.md:5` [A] | 2026-09-04~ | Kinds as verbs not allowed; rust-imposed verbs tolerated as legacy unt |
| `flows/04db2fd2/vision/archive-kinds.md:11` [A] | 2026-09-04~ | Textual as a kind; Actual too strong; "it can take the form the runtim |
| `flows/4decf7/vision/archive-kinds.md:13` [A] | 2026-09-03 | 2026-09-03 — corrections to the first proposal: might imply; an exampl |
| `flows/62022e8f/vision/archive-kinds.md:20` [A] | 2026-09-04~ | The layer capabilities sit on the layer above: structure on Text, conc |
| `flows/e4a40e/vision/archive-kinds.md:14` [A] | 2026-09-04 | 2026-09-03 — what identifies a trait in Rust is what identifies a kind |

Later record: `flows/ebbe30/vision/ethos.md:9` (2026-10-09) The golden ethos is the ethos of ethos; kind is now trait

Why: later words "the kind has been changed to trait".

Note: Confirmed: d5df1d ethos:19 (2026-10-09) 'Trait: rename every place'; ebbe30 ethos:29 (2026-10-09) 'we can use traits... kind might be used to also mean traits'. The base prompt's protos section still says 'kind' (read this turn), so the landing in vision-protos/vision-ethos is stale and the rename itself is a landing, not a deletion. Earlier records here: 6; exact copies of them in other flows: 0.

### S7. Message envelope: timestamps, machine relay, empty fields, 800-character pieces, part numbers, message id (medium)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/88475f/vision/message.md:17` | 2026-09-25~ | Psyche messages split into 800-character pieces for Claude |
| `flows/88475f/vision/message.md:9` | 2026-09-25~ | Big messages and the psyche message type |

Later record: `flows/88475f/vision/message.md:33` (2026-09-25~) No 800-character limit, no part numbers in psyche messages

Why: later words "remove the 800-character limit".

Note: Same flow, same day: 88475f message:1 and e51411 messaging:51 'A message is really just a message'; e51411 messaging:63 no repeated or empty fields; e51411 messaging:71 'this tag, Flow ID, and text'; b7ba00 messaging:25 (2026-09-26) 'We shouldn't get the message ID'; b7da5d layerVocabularyAndReview:15 (2026-09-26) remove the limit 'from everywhere'. Earlier records here: 2; exact copies of them in other flows: 1.

### S8. Mentci GUI (Qt/egui/Web) abandoned for Unity as the interface (medium)

Earlier records:

| record | date | heading |
|---|---|---|
| `vision-raw/mentci.md:3` | 2026-08-13 | 2026-08-13 — the daemon is the central logic; front-ends are not Rust; |
| `flows/1b8ac0/vision/mentciWeb.md:3` | 2026-09-21~ | Make our own web UI, Mentci Web, defined like a Nexus but a full web a |

Later record: `flows/6f51ad/vision/mentci.md:2` (2026-09-28) 2026-09-28 — Mentci and Unity

Why: later words "the Menchi you're referring to is obsolete now".

Note: Same words in 8904b1 presentation:21 (copy). 840e42 mobile:3 (2026-10-01) still says 'A Mentci app embedding a very minimal CriomOS' -- listed as unclear, not deleted. Earlier records here: 2; exact copies of them in other flows: 0.

### S9. Opus 4.6 preferred over Opus 5, then Opus 4.6 phased out (medium)

Earlier records:

| record | date | heading |
|---|---|---|
| `vision-raw/gradientsOfAuthority.md:3` | 2026-08-10 | 2026-08-10 — the fence meme, instruction hierarchy, and search compuls |
| `flows/58a86d/vision/subagentModel.md:3` | 2026-09-05 | 2026-09-05 — Opus 4.6, not Opus 5 |
| `flows/5851f4/vision/psycheFacingModel.md:3` | 2026-09-08~ | Opus 4.6 for the interlocutor, Opus 5 for subagents |
| `flows/f55ec8/vision/layers.md:13` | 2026-09-16~ | The model for the lower layers: Opus 4.7, or 4.6 with the million cont |
| `flows/f55ec8/vision/modelRoles.md:3` | 2026-09-16~ | Two Opus models, named by role: the older Opus, the wiser one, and the |
| `flows/1ac573/vision/operational-defaultModelPsycheMediumClaude.md:3` | 2026-09-18~ | Make that the default for psyche medium Claude, being Opus 4.6 — which |
| `flows/1ac573/vision/operational-olderOpusIs46.md:3` | 2026-09-18~ | I would like 4.6 even better than 4.7 — the 4.6 1 million token. Let's |

Later record: `flows/b80e55/vision/retirement.md:3` (2026-09-24) You shouldn't be running anymore

Why: later words "We are phasing out Opus 4.6".

Note: 8475a9 voices:79 (2026-10-05) 'Opus 5.5 replaces the old Opus models'. The system skills now pin model names in one declaration, so the per-model rulings are stale. Earlier records here: 7; exact copies of them in other flows: 0.

### S10. Nota/Dotos syntax and its files, replaced by Datom (medium)

Earlier records:

| record | date | heading |
|---|---|---|
| `vision-raw/archive-ethosDotosDivisionAndHelp.md:4` [A] | 2026-08-02 | 2026-08-02 — "the two main syntaxes most agents will face" |
| `flows/55d18f4f/vision/archive-signalIsOurMessagingLayer.md:1` [A] | 2026-08-08 | 2026-08-08T11:45:33.818Z — Signal is our messaging layer |
| `flows/c6b71b4c/vision/archive-threeStacks.md:2` [A] | 2026-08-10 | 2026-08-10 — names confirmed; the successor name must stick |
| `flows/012fbf07/vision/archive-threeStacks.md:84` [A] | 2026-08-11 | 2026-08-11 — datom is just a renamed dotos; no new repo was needed |

Later record: `flows/01a03d6e/vision/archive-ethosInterfaces.md:21` (2026-08-26) 2026-08-26T15:04:27.982Z — that is obsolete nota/dotos format

Why: later words "that is obsolete nota/dotos format".

Note: Also 01a03d6e archive-dotosFiles:7 (2026-08-26) 'There should be no Dodos files anymore'; 01a02a34 archive-datum:16 'use datom instead of dotos'. The earlier setupIndependentInterfaces:13 keeps its rule (no flags) but names the stale 'nota/dotos'. Earlier records here: 4; exact copies of them in other flows: 0.

### S11. Training daemon / Rust curriculum daemon replaced by Flow; awareness files; persona-spirit (medium)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/358f143a/vision/trainingRepo.md:1` | 2026-08-17 | 2026-08-17 — Athena is deployment specific; the successor is a Rust da |

Later record: `flows/358f143a/vision/trainingRepo.md:35` (2026-08-18) 2026-08-18 — superseded: the daemon is flow, not training

Why: later words "isnt training anymore".

Note: Companions: 358f143a awarenessIsGeneralUnderstanding:1 (2026-08-17) 'awareness files are the obsolete protocol'; fd301d9a actorLibrary:41 (2026-08-21) 'persona-spirit is abandoned'. Copy: 358f143a archive-flowDaemon:3. Earlier records here: 1; exact copies of them in other flows: 0.

### S12. Flow titles with V2 and per-model names (medium)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/e51411/vision/titles.md:19` | 2026-09-25 | Test flows through the new Flow, titled in the V2 form as a Datom stru |
| `flows/e51411/notion/v2.md:3` | 2026-09-25 | A test network: a second flow container, fully Flow-controlled, whose  |
| `flows/5ac3a3/vision/flow.md:2` | 2026-09-27 | 2026-09-27 — Model name, power levels, and Mind Astra panes |

Later record: `flows/d4ae97/vision/flow.md:160` (2026-10-08) Flow titles in the old convention

Why: later words "completely obsolete now".

Note: Also e167d8 names:3 (2026-09-26) 'We can remove the V2'; 6f51ad namesOfFlows:2 (2026-09-28) 'get rid of the V2'; d8df70 titles:4 (2026-09-24) 'Drop the version from the title'. Earlier records here: 3; exact copies of them in other flows: 0.

### S13. Flow artifacts protocol: origin marks, subflow marking, handoff file (small)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/5c8be3ca/vision/flowArtifacts.md:11` | 2026-08-21 | 5c8be3ca-1 — 2026-08-21 — the directory gives the flow; only subflows  |
| `flows/5c8be3ca/vision/flowArtifacts.md:1` | 2026-08-21 | 5c8be3ca-2 — 2026-08-21 — no handoff file; the flow reads its previous |

Later record: `flows/5c8be3ca/vision/flowArtifacts.md:20` (2026-08-21) 5c8be3ca-3 — 2026-08-21 — subflow marking dropped

Why: later words "then we should drop the idea".

Note: Same day. :1 'no handoff file' is itself a simplification of the first draft; keep as the live ruling. Earlier records here: 2; exact copies of them in other flows: 0.

### S14. Psyche log ids: 8-hex hash, 4-hex hash, then increasing numeric ids (small)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/06196cc7/vision/psycheLogStructure.md:21` | 2026-08-14 | 2026-08-14 — distillation corrections: re-articulation, many-to-many,  |

Later record: `flows/06196cc7/vision/psycheLogStructure.md:94` (2026-08-14) 2026-08-14 — ids are increasing numerics; archives are date-based append-only files

Why: later words "I've changed my mind on hashing the IDs".

Note: Same day. :110 then says 'the id scheme is unresolved'. The present rule (record id = session short id + count) is in the base prompt, so all 2026-08-14 id schemes are stale. Earlier records here: 1; exact copies of them in other flows: 0.

### S15. Ethos Monolith (shortcut stack with Nomos and Logos left out) is just Ethos Zero (small)

Earlier records:

| record | date | heading |
|---|---|---|
| `flows/ba906ae2/vision/archive-threeStacks.md:2` [A] | 2026-08-14 | 2026-08-14 — the shortcut stack becomes a daemon; renamed ethos monoli |
| `vision-raw/mainFunction.md:74` | 2026-08-21 | 2026-08-21 — the top is the assembled source, which includes the manif |

Later record: `flows/fe34eb/vision/ethos.md:11` (2026-09-10) 2026-09-10 — Ethos Monolith and Ethos Zero are the same thing; Zero as in version 0, no daemon yet, no Nexus

Why: later words "it's not relevant anymore".

Note: The vision-archive-ethos-monolith skill already exists as an archive; the later record says the name 'Ethos Monolith' need not be talked about. Earlier records here: 2; exact copies of them in other flows: 0.

### Unclear (do not delete without the living's ruling)

- **Subagent facility: 'get rid of the subagents facility' (2026-09-20) against main flows delegating to subagents (2026-09-24).** Records: flows/b81560/vision/archive-operational-asyncSubflowsAndMeaningLanguage.md:3, flows/f38926/vision/archive-subflows.md:3 against flows/e51411/vision/mainFlow.md:5, flows/d8df70/vision/mainFlowMode.md:3, flows/1b8ac0/vision/skills.md:13. The 2026-09-20 line is landed as vision-flow 'Subflows replace the harness subagent facility'; the 2026-09-24 records order subagent use inside the harness. Two readings: the harness facility is replaced, or main flows still use it for now.
- **Messages as Datom: 'forced to be datom syntax' (2026-09-19/21) against 'we're not going to enforce Datom syntax on a messenger that doesn't need it' (2026-09-27).** Records: flows/b05237/vision/operational-messengerUsesDatomNow.md:3, flows/1b8ac0/vision/transcriptTool.md:3 against flows/8904b1/vision/datom.md:3. vision-messaging lands 'A message is a datom, and it arrives as one'. The 2026-09-27 line may be a short-term posture for the Clojure messenger (see S6 and section 4b).
- **Skill manifest: 'get rid of the manifest' (2026-08-21) against 'a manifest that gives it a bunch of paths' (2026-09-17).** Records: vision-raw/skillsRepository.md:3 against flows/108ab0/vision/operational-curriculumAsModuleSystem.md:3. Reversed in the other direction, so neither can be deleted as the older of a rollback; the 2026-10-07 'dirty first' record (S2) is later than both.
- **Mentci after Unity: 'a Mentci app embedding a very minimal CriomOS' (2026-10-01) against 'Menchi ... is obsolete now' (2026-09-28).** Records: flows/840e42/vision/mobile.md:3 against flows/6f51ad/vision/mentci.md:2. 'Mentci is just a nexus' may be what the 2026-10-01 record means.
- **Flow lock: 'a seat starts receiving, the old seat stops receiving first, that's how we get a lock' (2026-09-24) against 'I've actually changed my mind... the flow should not give the lock to message' (2026-10-11).** Records: flows/d8df70/vision/flowLifecycle.md:3, flows/836818/vision/flowNexus.md:21 against flows/875960/vision/flow.md:35. The 2026-10-11 record names a change of mind but not what it was changed from; the earlier proposal may have been a machine proposal.
- **Voice remnant: the base prompt still defines 'Flow: one run of a voice' (read this turn) while flows/875960/vision/flow.md:11 says the voice concept is gone.** Records: flows/875960/vision/flow.md:11. Either the base-prompt term list is stale or the 2026-10-11 comment meant one narrow use. Ask before deleting the S1 records.
- **Flow-id length: first four characters (2026-09-14) against six characters (2026-08-26, 2026-10-01) against words from the first 33 bits (2026-10-03).** Records: flows/e1953c/vision/flowIdentity.md:13, flows/06196cc7/vision/psycheLogStructure.md:21 against flows/01a03d6e/vision/flowIdentity.md:3, flows/fe945a/vision/hashes.md:3, flows/5578cc/vision/identifiers.md:19. Likely each is a different identifier (psyche record id, session, display); not a rollback.
- **Refresh payload and addendum (2026-09-21) against handover at cache expiry (2026-10-14).** Records: flows/1b8ac0/vision/refresh.md:3 against flows/d68c82/vision/flow.md:114, flows/33752b/vision/flow.md:19. Compaction-as-emergency is consistent; whether the handover replaces the refresh payload is not said.
- **Reports and logs as files: 'the report becomes everything is in the transcript; we don't want to make files anymore' (2026-09-17) against the live flows/<id>/log.md, reports/ and witness files protocol (2026-08-21).** Records: flows/9993b5/vision/transcriptOverFiles.md:3, flows/fd0f97/vision/psyche.md:3, flows/c64ee3/vision/recording.md:3 against flows/5c8be3ca/vision/flowArtifacts.md (whole file). The file protocol is what runs today; the later words read as a long-term target (a Psyche component replaces the makeshift file logging). Candidate for the long-term mark, not for deletion.
- **Value layer in Datom: a brainstorm the living reclassified as a notion (2026-09-09).** Records: flows/564f55/notion/datom.md:3, flows/564f55/notion/datom.md:13, flows/564f55/vision/datom.md:19. The vision record :19 is itself the reclassification; the notion records stay notions.

### Working corrections that reject a machine proposal (not a psyche-on-psyche rollback)

These are the living's rulings on what an agent proposed; none overrules an earlier psyche record. They read as working instructions and are the likeliest vision impurities when crystallization reaches them. Listed for the living to rule on, not recommended for deletion by this inventory:

- flows/01a02fe5/vision/skillTraining.md:9 and :21 (2026-08-24/25: 'way too complex. start with ultra minimal')
- flows/01a02b46/vision/zeusUpdate.md:120 (2026-08-23: 'your skill is too complicated')
- flows/db97561c/vision/promptCrafting.md:21 (2026-08-29: 'your remember prompt is too complicated')
- flows/aa4c7747/vision/sessionLog.md:3 (2026-08-24: 'lets simplify it')
- flows/2b34fafa/vision/rustComponentArchitecture.md:1 and :40 (2026-08-18: the per-repo architecture guard)
- flows/7c3f0c1d/vision/testTravesties.md:1 and flows/98fbfa47/vision/testTravesties.md:1 (2026-08-10/19: remove the bad tests)
- flows/f426777b/vision/skillDesigning.md:22 (2026-08-26: the protos skill draft is too intellectual)
- flows/b7465e71/vision/remembering.md:50 (2026-08-22: 'delete the reports since they could induce a pattern')
- flows/fe34eb/notion/reports.md:3 (2026-09-11: too many reports and witnesses)
- flows/8e9e77/vision/single-field-structs.md:9 (2026-09-08: 'Never mind that' inside the record)
- flows/058f16/vision/source.md:31 (2026-10-10: 'Actually never mind all this' inside the record)
- flows/38dec9/vision/piHarness.md:1 (2026-09-04: abandon the Pi harness) and flows/58a86d/vision/vscodium.md:3 (2026-09-05: vscodium obsolete)

## 3. Duplicates

Rule used: keep the earliest hearing (record date, ties to the live file over an archive file, then path); every other row is a copy. `[A]` marks a copy in an `archive-*` file.

### 3a. Exact duplicates (268 groups, 360 copies)

Format: keep `path:line` (date) <- copies.

- keep `flows/019fe641/vision/hostEnvironmentRecovery.md:1` (2026-08-09) <- `flows/01a02b46/vision/zeusUpdate.md:73` (2026-08-09)
- keep `flows/b7ba00/vision/meaningLanguage.md:131` (2026-08-11) <- `flows/a5587095/vision/archive-protosIsTheSharedStyle.md:3` [A] (2026-08-11); `flows/a5587095/vision/archive-structuredStringType.md:37` [A] (2026-08-11)
- keep `flows/a5587095/vision/archive-datomSyntax.md:14` (2026-08-11) <- `flows/a5587095/vision/archive-structuredStringType.md:18` [A] (2026-08-11)
- keep `flows/a5587095/vision/archive-structuredStringType.md:82` (2026-08-11) <- `flows/a5587095/vision/archive-threeStacks.md:2` [A] (2026-08-11)
- keep `flows/01a01a93/vision/hostEnvironmentRecovery.md:23` (2026-08-19) <- `flows/01a02b46/vision/zeusUpdate.md:41` (2026-08-19)
- keep `flows/15b67974/vision/hexis.md:1` (2026-08-21) <- `flows/fd301d9a/vision/actorLibrary.md:48` (2026-08-21)
- keep `flows/fd301d9a/vision/actorLibrary.md:18` (2026-08-21) <- `flows/15b67974/vision/archive-actorLibrary.md:3` [A] (2026-08-21)
- keep `flows/fd301d9a/vision/actorLibrary.md:25` (2026-08-21) <- `vision-raw/actorLibrary.md:3` (2026-08-21)
- keep `flows/fd301d9a/vision/actorLibrary.md:41` (2026-08-21) <- `vision-raw/spiritComponentAndFile.md:14` (2026-08-21)
- keep `flows/15b67974/vision/worldModelBeforeCode.md:11` (2026-08-22) <- `flows/fd301d9a/vision/archive-nexusTraits.md:3` [A] (2026-08-22)
- keep `flows/fd301d9a/vision/actorLibrary.md:3` (2026-08-22) <- `flows/15b67974/vision/archive-actorLibrary.md:12` [A] (2026-08-22)
- keep `flows/01a03eda/vision/observe.md:3` (2026-08-26) <- `flows/01a03eda/vision/archive-datomInteger.md:7` [A] (2026-08-26)
- keep `flows/5851f4/vision/anatomyOfCommunicatingThinkingAndReacting.md:3` (2026-09-08~) <- `flows/b7ba00/vision/meaningLanguage.md:121` (2026-09-26~)
- keep `flows/5851f4/vision/ashtadhyayiKnowledgeBase.md:3` (2026-09-08~) <- `flows/b7ba00/vision/meaningLanguage.md:109` (2026-09-26~)
- keep `flows/564f55/vision/archive-protos.md:73` (2026-09-09) <- `flows/564f55/vision/archive-protos.md:91` [A] (2026-09-09)
- keep `flows/024bc7/notion/ethosDelta.md:3` (2026-09-13) <- `flows/bcd02a/notion/ethos.md:11` (2026-09-13)
- keep `flows/024bc7/vision/effort.md:11` (2026-09-13) <- `flows/bcd02a/notion/prometheus.md:3` (2026-09-13)
- keep `flows/024bc7/vision/network.md:3` (2026-09-13) <- `flows/bcd02a/vision/network.md:3` (2026-09-13)
- keep `flows/024bc7/vision/nexus.md:13` (2026-09-13) <- `flows/bcd02a/notion/ethos.md:3` (2026-09-13)
- keep `flows/024bc7/vision/parallelSessions.md:31` (2026-09-13) <- `flows/bcd02a/vision/paired-flows.md:15` (2026-09-13)
- keep `flows/024bc7/vision/soul.md:3` (2026-09-13) <- `flows/bcd02a/notion/persona.md:3` (2026-09-13)
- keep `flows/024bc7/vision/soul.md:9` (2026-09-13) <- `flows/bcd02a/notion/persona.md:9` (2026-09-13)
- keep `flows/024bc7/vision/storage.md:3` (2026-09-13) <- `flows/bcd02a/notion/nexus.md:3` (2026-09-13)
- keep `flows/e1953c/vision/terminal.md:3` (2026-09-14~) <- `flows/eae736/vision/sessionAccess.md:3` (2026-09-14~)
- keep `flows/cf7879/vision/cluster.md:3` (2026-09-15) <- `flows/840e42/vision/messages.md:11` (2026-10-01~)
- keep `flows/108ab0/vision/operational-flowDatomLauncherLanguage.md:3` (2026-09-17) <- `flows/6852f4/vision/communication.md:3` (2026-09-17~)
- keep `flows/b7ba00/vision/meaningLanguage.md:101` (2026-09-17) <- `flows/9993b5/vision/typedString.md:3` (2026-09-17~)
- keep `flows/33ba2b/vision/psycheDataArchitecture.md:51` (2026-09-18~) <- `flows/b05237/vision/operational-logOnMainNowMigrateLater.md:3` (2026-09-18~)
- keep `flows/b7ba00/vision/meaningLanguage.md:47` (2026-09-19) <- `flows/b81560/vision/operational-meaningStructureRootVariant.md:3` (2026-09-19~); `flows/f38926/vision/meaningLanguage.md:3` (2026-09-19~)
- keep `flows/b7ba00/vision/meaningLanguage.md:55` (2026-09-19) <- `flows/b81560/vision/archive-operational-meaningLanguageLogographic.md:3` [A] (2026-09-20~); `flows/f38926/vision/archive-meaningLanguage.md:15` [A] (2026-09-20~)
- keep `flows/b7ba00/vision/meaningLanguage.md:63` (2026-09-19) <- `flows/b81560/vision/archive-operational-meaningLanguageAnnotationLayers.md:3` [A] (2026-09-20~); `flows/f38926/vision/archive-meaningLanguage.md:23` [A] (2026-09-20~)
- keep `flows/b7ba00/vision/meaningLanguage.md:73` (2026-09-19) <- `flows/f38926/vision/archive-meaningLanguage.md:3` [A] (2026-09-20~)
- keep `flows/b7ba00/vision/meaningLanguage.md:85` (2026-09-19) <- `flows/b81560/vision/archive-operational-vaisheshikaRuledAndSyntaxQuestion.md:3` [A] (2026-09-20~); `flows/f38926/vision/archive-meaningLanguage.md:59` [A] (2026-09-20~)
- keep `flows/b7ba00/vision/meaningLanguage.md:93` (2026-09-19) <- `flows/b81560/vision/archive-operational-meaningDualSanskritEnglishNames.md:3` [A] (2026-09-20~); `flows/f38926/vision/archive-meaningLanguage.md:67` [A] (2026-09-20~)
- keep `flows/b81560/vision/operational-deployOnTheHostYoureOn.md:3` (2026-09-19~) <- `flows/f38926/vision/archive-operational-openCodeRemoteAccess.md:11` [A] (2026-09-20~)
- keep `flows/b81560/vision/operational-nightWorkDirective.md:3` (2026-09-19~) <- `flows/f38926/vision/nightWork.md:3` (2026-09-19~)
- keep `flows/b81560/vision/operational-openCodeOnUranusNotZeus.md:3` (2026-09-19~) <- `flows/f38926/vision/archive-operational-openCodeRemoteAccess.md:3` [A] (2026-09-20~)
- keep `flows/b81560/vision/operational-openCodeTestWithCodexSubscription.md:3` (2026-09-19~) <- `flows/f38926/vision/operational-openCodeRemoteAccess.md:3` (2026-09-19~)
- keep `flows/f38926/vision/operational-openCodeRemoteAccess.md:13` (2026-09-19~) <- `flows/b81560/vision/archive-operational-pocSandboxVmFirst.md:3` [A] (2026-09-20~)
- keep `flows/1b8ac0/vision/roles.md:3` (2026-09-20~) <- `flows/b81560/vision/operational-twelveFoldRolesOnly.md:3` (2026-09-20~)
- keep `flows/1b8ac0/vision/roles.md:11` (2026-09-20~) <- `flows/b81560/vision/operational-allPsychesRelayUpChain.md:3` (2026-09-20~)
- keep `flows/b81560/vision/archive-operational-explicitFilePathCommits.md:3` (2026-09-20~) <- `flows/f38926/vision/archive-committing.md:3` [A] (2026-09-20~)
- keep `flows/b81560/vision/archive-operational-fieldUltraLowRoutesSubflowRequests.md:3` (2026-09-20~) <- `flows/f38926/vision/archive-subflows.md:13` [A] (2026-09-20~)
- keep `flows/b81560/vision/archive-operational-horizonNexusAndNodeResources.md:3` (2026-09-20~) <- `flows/f38926/vision/archive-horizon.md:3` [A] (2026-09-20~)
- keep `flows/b81560/vision/archive-operational-meaningContentAddressedAnnotation.md:3` (2026-09-20~) <- `flows/f38926/vision/archive-meaningLanguage.md:33` [A] (2026-09-20~)
- keep `flows/b81560/vision/archive-operational-subflowRequestIdAndAsync.md:3` (2026-09-20~) <- `flows/f38926/vision/archive-subflows.md:21` [A] (2026-09-20~)
- keep `flows/1b8ac0/vision/autonomousOperation.md:3` (2026-09-21~) <- `flows/b80e55/vision/autonomousClusterOperation.md:3` (2026-09-21~)
- keep `flows/00f95a/vision/prometheus-zeus-mesh-possibilities.md:1` (2026-09-24) <- `flows/5f38bc/vision/prometheusZeusInternetPropagationAndTailnetAlternatives.md:8` (2026-09-24~); `flows/e71dab/vision/meshNetwork.md:26` (2026-09-24~)
- keep `flows/836818/vision/flowNexus.md:47` (2026-09-24) <- `flows/d8df70/vision/deployment.md:9` (2026-09-24)
- keep `flows/836818/vision/flowNexus.md:55` (2026-09-24) <- `flows/d8df70/vision/flowTool.md:9` (2026-09-24)
- keep `flows/b7ba00/vision/meaningLanguage.md:39` (2026-09-24) <- `flows/b7da5d/vision/meaningLanguage.md:1` (2026-09-24)
- keep `flows/d8df70/vision/flashbooks.md:64` (2026-09-24) <- `flows/e51411/vision/flashbooks.md:3` (2026-09-24)
- keep `flows/d8df70/vision/flashbooks.md:74` (2026-09-24) <- `flows/e51411/vision/flashbooks.md:13` (2026-09-24)
- keep `flows/d8df70/vision/launch.md:12` (2026-09-24) <- `flows/e51411/vision/launch.md:3` (2026-09-24)
- keep `flows/d8df70/vision/launch.md:20` (2026-09-24) <- `flows/e51411/vision/launch.md:11` (2026-09-24)
- keep `flows/d8df70/vision/titles.md:4` (2026-09-24) <- `flows/e51411/vision/titles.md:3` (2026-09-24)
- keep `flows/e51411/vision/authority.md:3` (2026-09-24) <- `flows/88475f/vision/asks.md:1` (2026-09-25~)
- keep `flows/e51411/vision/authority.md:21` (2026-09-24) <- `flows/88475f/vision/asks.md:9` (2026-09-25~)
- keep `flows/e51411/vision/speech.md:3` (2026-09-24) <- `flows/88475f/vision/speechToText.md:1` (2026-09-25~)
- keep `flows/26c50c/vision/build-placement.md:2` (2026-09-25) <- `flows/504461/vision/cluster-builds.md:2` (2026-09-25); `flows/da88cf/vision/clusterData.md:3` (2026-09-25)
- keep `flows/504461/vision/cluster-builds.md:8` (2026-09-25) <- `flows/b7da5d/vision/prometheusBuildPolicy.md:9` (2026-09-25); `flows/da88cf/vision/prometheus.md:47` (2026-09-25); `flows/e71dab/vision/tailscale.md:10` (2026-09-25)
- keep `flows/b7da5d/vision/flowClj.md:1` (2026-09-25) <- `flows/e51411/vision/stack.md:18` (2026-09-25)
- keep `flows/b7da5d/vision/prometheusBuilder.md:9` (2026-09-25) <- `flows/da88cf/vision/prometheus.md:11` (2026-09-25)
- keep `flows/da88cf/vision/daisyChain.md:11` (2026-09-25) <- `flows/e51411/vision/network.md:11` (2026-09-25)
- keep `flows/df159a/vision/books.md:23` (2026-09-25) <- `flows/17ac8a/vision/communication.md:45` (?~)
- keep `flows/e51411/vision/launch.md:91` (2026-09-25) <- `flows/88475f/vision/flow.md:9` (2026-09-25~)
- keep `flows/e51411/vision/launch.md:105` (2026-09-25) <- `flows/88475f/vision/power.md:1` (2026-09-25~)
- keep `flows/e51411/vision/mainFlow.md:29` (2026-09-25) <- `flows/88475f/vision/psycheInteraction.md:1` (2026-09-25~)
- keep `flows/e51411/vision/messaging.md:99` (2026-09-25) <- `flows/88475f/vision/message.md:17` (2026-09-25~)
- keep `flows/56ae53/vision/model-flow-emergency.md:1` (2026-09-26) <- `flows/b7ba00/vision/modelFlows.md:3` (2026-09-26); `flows/b7da5d/vision/modelSpendEmergency.md:2` (2026-09-26); `flows/e71dab/vision/modelGovernance.md:2` (2026-09-26)
- keep `flows/93ba9f/notion/semaCommunication.md:1` (2026-09-26) <- `flows/b7ba00/notion/sema.md:3` (2026-09-26)
- keep `flows/93ba9f/vision/automation.md:1` (2026-09-26) <- `flows/e71dab/vision/paneLifecycle.md:10` (2026-09-26)
- keep `flows/93ba9f/vision/callerIdentity.md:1` (2026-09-26) <- `flows/b7ba00/vision/callerIdentity.md:3` (2026-09-26)
- keep `flows/93ba9f/vision/datomVocabulary.md:1` (2026-09-26) <- `flows/b7ba00/vision/messaging.md:63` (2026-09-26)
- keep `flows/93ba9f/vision/fableRole.md:1` (2026-09-26) <- `flows/b7ba00/vision/fableRole.md:3` (2026-09-26); `flows/b7da5d/vision/fieldOwnership.md:2` (2026-09-26)
- keep `flows/93ba9f/vision/fieldTool.md:1` (2026-09-26) <- `flows/b7ba00/vision/designBook.md:11` (2026-09-26)
- keep `flows/93ba9f/vision/mindRoles.md:1` (2026-09-26) <- `flows/b7ba00/vision/mindRoles.md:3` (2026-09-26)
- keep `flows/93ba9f/vision/primarySeats.md:1` (2026-09-26) <- `flows/b7ba00/vision/reachingTheLiving.md:9` (2026-09-26)
- keep `flows/93ba9f/vision/psycheSharing.md:1` (2026-09-26) <- `flows/b7ba00/vision/designBook.md:3` (2026-09-26)
- keep `flows/b7ba00/vision/meaningLanguage.md:31` (2026-09-26) <- `flows/e167d8/vision/layerVocabulary.md:3` (2026-09-26)
- keep `flows/b7ba00/vision/modelFlows.md:19` (2026-09-26) <- `flows/e71dab/vision/launchGovernance.md:10` (2026-09-26)
- keep `flows/b7da5d/vision/layerVocabularyAndReview.md:15` (2026-09-26) <- `flows/b860be/vision/messageSize.md:3` (2026-09-26); `flows/e167d8/vision/psycheMessages.md:3` (2026-09-26); `flows/f5a74e/vision/independent-analysis.md:16` (2026-09-26)
- keep `flows/b7da5d/vision/mainFlowRefreshAndRoles.md:3` (2026-09-26) <- `flows/b860be/vision/mainRoles.md:3` (2026-09-26)
- keep `flows/b7da5d/vision/mainFlowRefreshAndRoles.md:31` (2026-09-26) <- `flows/b860be/vision/fieldTool.md:3` (2026-09-26)
- keep `flows/b7da5d/vision/mainFlowRefreshAndRoles.md:43` (2026-09-26) <- `flows/b860be/vision/fieldTool.md:15` (2026-09-26); `flows/e167d8/vision/fieldTool.md:13` (2026-09-26)
- keep `flows/b7da5d/vision/mainFlowRefreshAndRoles.md:51` (2026-09-26) <- `flows/b860be/vision/openCode.md:3` (2026-09-26); `flows/e167d8/vision/openCode.md:3` (2026-09-26)
- keep `flows/b7da5d/vision/modelPlacement.md:1` (2026-09-26) <- `flows/b860be/vision/aiModels.md:3` (2026-09-26); `flows/e167d8/vision/prometheus.md:3` (2026-09-26); `flows/31147a/vision/ai-model-placement.md:2` (2026-09-26~)
- keep `flows/b7da5d/vision/piper.md:1` (2026-09-26) <- `flows/31147a/vision/ai-model-placement.md:10` (2026-09-26~); `flows/31147a/vision/ai-model-placement.md:18` (2026-09-26~)
- keep `flows/b860be/vision/layerVocabulary.md:1` (2026-09-26) <- `flows/f5a74e/vision/independent-analysis.md:2` (2026-09-26)
- keep `flows/6f51ad/vision/communication.md:3` (2026-09-28) <- `flows/caf622/vision/Fable.md:16` (2026-09-28)
- keep `flows/6f51ad/vision/communication.md:11` (2026-09-28) <- `flows/c02c0d/vision/seats.md:3` (2026-09-28); `flows/caf622/vision/Fable.md:2` (2026-09-28)
- keep `flows/6f51ad/vision/home.md:3` (2026-09-28) <- `flows/8904b1/vision/deployment.md:3` (2026-09-28)
- keep `flows/6f51ad/vision/namesOfFlows.md:2` (2026-09-28) <- `flows/b666e7/vision/namesOfFlows.md:2` (2026-09-28)
- keep `flows/6f51ad/vision/presentation.md:3` (2026-09-28) <- `flows/c02c0d/vision/presentation.md:3` (2026-09-28)
- keep `flows/c02c0d/vision/seats.md:11` (2026-09-28) <- `flows/caf622/vision/Fable.md:9` (2026-09-28)
- keep `flows/6f51ad/vision/clusterSurvey.md:3` (2026-09-29) <- `flows/d5b96b/vision/cluster-survey.md:2` (2026-09-29)
- keep `flows/6f51ad/vision/network.md:3` (2026-09-29) <- `flows/c64ee3/vision/network.md:3` (2026-09-29)
- keep `flows/6f51ad/vision/transcripts.md:3` (2026-09-29) <- `flows/c64ee3/vision/presentation.md:3` (2026-09-29)
- keep `flows/bd0019/vision/hook.md:3` (2026-09-29) <- `flows/b666e7/notion/hook.md:2` (2026-09-29~)
- keep `flows/caf622/vision/Luna-Flow.md:2` (2026-09-29) <- `flows/b666e7/vision/flows.md:2` (2026-09-29~)
- keep `flows/7328f4/vision/seats.md:3` (2026-09-30) <- `flows/b666e7/vision/communication.md:2` (2026-10-01~)
- keep `flows/1bc255/vision/pollingSystems.md:1` (2026-09-30~) <- `flows/b666e7/vision/polling.md:1` (2026-10-01~)
- keep `flows/b666e7/vision/declarative-features.md:8` (2026-09-30~) <- `flows/7328f4/vision/stateful.md:3` (2026-10-01)
- keep `flows/b666e7/vision/seat-migration.md:1` (2026-09-30~) <- `flows/7328f4/vision/seats.md:11` (2026-10-01)
- keep `flows/b666e7/vision/usb-ethernet-sharing.md:8` (2026-09-30~) <- `flows/7328f4/vision/network.md:11` (2026-10-01)
- keep `flows/6997eb/vision/presentation.md:3` (2026-10-01) <- `flows/e2a70a/vision/blocks-for-the-living.md:3` (2026-10-01)
- keep `flows/6997eb/vision/presentation.md:105` (2026-10-01) <- `flows/91ea9f/vision/books.md:11` (2026-10-01); `flows/fe945a/vision/presentation.md:22` (2026-10-01)
- keep `flows/6997eb/vision/questions.md:3` (2026-10-01) <- `flows/fe945a/vision/questions.md:3` (2026-10-01)
- keep `flows/6997eb/vision/repositoryClassification.md:3` (2026-10-01) <- `flows/fe945a/vision/repositoryClassification.md:3` (2026-10-01)
- keep `flows/91ea9f/vision/books.md:3` (2026-10-01) <- `flows/bd0019/vision/marker.md:3` (2026-10-01)
- keep `flows/bd0019/vision/skillProposals.md:3` (2026-10-01) <- `flows/fe945a/vision/skills.md:3` (2026-10-01)
- keep `flows/e2a70a/vision/identifying-strings.md:3` (2026-10-01) <- `flows/fe945a/vision/hashes.md:13` (2026-10-01)
- keep `flows/01e496/vision/books.md:3` (2026-10-02) <- `flows/91ea9f/vision/books.md:25` (2026-10-02)
- keep `flows/01e496/vision/books.md:11` (2026-10-02) <- `flows/41fa34/vision/what-the-book-is.md:1` (2026-10-02); `flows/91ea9f/vision/books.md:33` (2026-10-02)
- keep `flows/01e496/vision/books.md:19` (2026-10-02) <- `flows/91ea9f/vision/books.md:41` (2026-10-02)
- keep `flows/01e496/vision/design.md:3` (2026-10-02) <- `flows/41fa34/vision/design-by-astra.md:9` (2026-10-02); `flows/42265e/vision/flow-component.md:19` (2026-10-02); `flows/42265e/vision/flow-component.md:27` (2026-10-02); `flows/91ea9f/vision/roles.md:3` (2026-10-02)
- keep `flows/01e496/vision/flashbook.md:3` (2026-10-02) <- `flows/edf227/vision/illustrations.md:9` (2026-10-03)
- keep `flows/01e496/vision/flowIdentity.md:3` (2026-10-02) <- `flows/41fa34/vision/continuous-names.md:1` (2026-10-02); `flows/91ea9f/vision/addressing.md:3` (2026-10-02)
- keep `flows/01e496/vision/flowNexus.md:3` (2026-10-02) <- `flows/fe945a/vision/flowNexus.md:3` (2026-10-02)
- keep `flows/01e496/vision/flowNexus.md:11` (2026-10-02) <- `flows/42265e/vision/flow-component.md:3` (2026-10-02); `flows/42265e/vision/flow-component.md:11` (2026-10-02); `flows/91ea9f/vision/flowNexus.md:3` (2026-10-02)
- keep `flows/01e496/vision/messaging.md:3` (2026-10-02) <- `flows/41fa34/vision/continuous-names-messaging.md:1` (2026-10-02); `flows/91ea9f/vision/addressing.md:9` (2026-10-02)
- keep `flows/01e496/vision/seat.md:3` (2026-10-02) <- `flows/91ea9f/vision/seat.md:3` (2026-10-02)
- keep `flows/01e496/vision/simpleWorkingSystem.md:3` (2026-10-02) <- `flows/41fa34/vision/working-system.md:1` (2026-10-02); `flows/91ea9f/vision/priority.md:3` (2026-10-02)
- keep `flows/01e496/vision/skills.md:3` (2026-10-02) <- `flows/41fa34/vision/presentation-publication.md:1` (2026-10-02); `flows/91ea9f/vision/skills.md:3` (2026-10-02)
- keep `flows/3ec648/vision/voices.md:3` (2026-10-02) <- `flows/91ea9f/vision/addressing.md:23` (2026-10-02)
- keep `flows/41fa34/vision/checkboxes.md:1` (2026-10-02) <- `flows/42265e/vision/flashbooks.md:27` (2026-10-02~)
- keep `flows/41fa34/vision/expands-vertically.md:1` (2026-10-02) <- `flows/42265e/vision/flashbooks.md:59` (2026-10-02~)
- keep `flows/41fa34/vision/semi-sandbox.md:2` (2026-10-02) <- `flows/42265e/vision/capsule.md:2` (2026-10-02)
- keep `flows/41fa34/vision/simple-working-system.md:2` (2026-10-02) <- `flows/42265e/vision/system.md:2` (2026-10-02)
- keep `flows/41fa34/vision/skill-catch-up.md:1` (2026-10-02) <- `flows/91ea9f/vision/skills.md:9` (2026-10-02)
- keep `flows/41fa34/vision/sonnet-comments.md:1` (2026-10-02) <- `flows/42265e/vision/flashbooks.md:51` (2026-10-02~)
- keep `flows/41fa34/vision/swiping-left-right.md:1` (2026-10-02) <- `flows/42265e/vision/flashbooks.md:35` (2026-10-02~)
- keep `flows/41fa34/vision/who-implements-skill-proposals.md:1` (2026-10-02) <- `flows/42265e/vision/skill-proposals.md:3` (2026-10-02)
- keep `flows/6997eb/vision/metaHarness.md:3` (2026-10-02) <- `flows/bd0019/vision/metaHarness.md:3` (2026-10-02); `flows/fe945a/vision/metaHarness.md:3` (2026-10-02)
- keep `flows/91ea9f/vision/flowLifecycle.md:3` (2026-10-02) <- `flows/fe945a/vision/flowLifecycle.md:12` (2026-10-02)
- keep `flows/41fa34/vision/flowLifecycle.md:2` (2026-10-03) <- `flows/dea0ba/vision/flowLifecycle.md:2` (2026-10-03)
- keep `flows/41fa34/vision/flowLifecycle.md:10` (2026-10-03) <- `flows/dea0ba/vision/flowLifecycle.md:8` (2026-10-03)
- keep `flows/41fa34/vision/identifiers.md:2` (2026-10-03) <- `flows/9fb0ad/vision/identifiers.md:3` (2026-10-03)
- keep `flows/41fa34/vision/layers.md:2` (2026-10-03) <- `flows/5578cc/vision/layers.md:3` (2026-10-03)
- keep `flows/41fa34/vision/publication.md:2` (2026-10-03) <- `flows/5578cc/vision/publishing.md:3` (2026-10-03); `flows/dea0ba/vision/publishing.md:1` (2026-10-03); `flows/edf227/vision/workspaces.md:3` (2026-10-03)
- keep `flows/41fa34/vision/skills.md:2` (2026-10-03) <- `flows/41fa34/vision/speech.md:18` (2026-10-03); `flows/5578cc/vision/skills.md:11` (2026-10-03); `flows/dea0ba/vision/speech.md:14` (2026-10-03)
- keep `flows/41fa34/vision/skills.md:10` (2026-10-03) <- `flows/5578cc/vision/skills.md:19` (2026-10-03)
- keep `flows/41fa34/vision/speech.md:2` (2026-10-03) <- `flows/5578cc/vision/flow.md:39` (2026-10-03); `flows/9fb0ad/vision/speech.md:9` (2026-10-03); `flows/dea0ba/vision/speech.md:8` (2026-10-03)
- keep `flows/41fa34/vision/speech.md:10` (2026-10-03) <- `flows/9fb0ad/vision/speech.md:3` (2026-10-03)
- keep `flows/41fa34/vision/speech.md:26` (2026-10-03) <- `flows/5578cc/vision/behavior.md:11` (2026-10-03); `flows/edf227/vision/readingTheLiving.md:3` (2026-10-03); `flows/42265e/vision/routing-examples.md:1` (2026-10-03~)
- keep `flows/41fa34/vision/subflows.md:2` (2026-10-03) <- `flows/9fb0ad/vision/subflows.md:3` (2026-10-03)
- keep `flows/41fa34/vision/subflows.md:10` (2026-10-03) <- `flows/5578cc/vision/skills.md:39` (2026-10-03); `flows/edf227/vision/subflowBriefs.md:3` (2026-10-03)
- keep `flows/5578cc/vision/flashbook.md:3` (2026-10-03) <- `flows/6e782c/vision/bookRendering.md:1` (2026-10-03); `flows/dea0ba/vision/illustrations.md:1` (2026-10-03)
- keep `flows/5578cc/vision/flow.md:19` (2026-10-03) <- `flows/9fb0ad/vision/identifiers.md:15` (2026-10-03); `flows/dea0ba/vision/titles.md:1` (2026-10-03)
- keep `flows/5578cc/vision/flow.md:27` (2026-10-03) <- `flows/9fb0ad/vision/identifiers.md:21` (2026-10-03)
- keep `flows/5578cc/vision/flow.md:47` (2026-10-03) <- `flows/9fb0ad/vision/deterministicWork.md:3` (2026-10-03); `flows/dea0ba/vision/deterministicWork.md:1` (2026-10-03)
- keep `flows/5578cc/vision/flow.md:55` (2026-10-03) <- `flows/9fb0ad/vision/systemPrompt.md:3` (2026-10-03)
- keep `flows/5578cc/vision/identifiers.md:3` (2026-10-03) <- `flows/9fb0ad/vision/identifiers.md:9` (2026-10-03)
- keep `flows/5578cc/vision/identifiers.md:11` (2026-10-03) <- `flows/9fb0ad/vision/ethosLibrary.md:3` (2026-10-03)
- keep `flows/5578cc/vision/identifiers.md:19` (2026-10-03) <- `flows/9fb0ad/vision/identifiers.md:31` (2026-10-03)
- keep `flows/5578cc/vision/locking.md:3` (2026-10-03) <- `flows/dea0ba/vision/locking.md:1` (2026-10-03)
- keep `flows/5578cc/vision/writing.md:3` (2026-10-03) <- `flows/9fb0ad/vision/speakingToTheLiving.md:3` (2026-10-03); `flows/dea0ba/vision/speakingToTheLiving.md:1` (2026-10-03)
- keep `flows/5ed94b/vision/infrastructure.md:3` (2026-10-03) <- `flows/28d847/vision/infrastructure.md:3` (2026-10-03~)
- keep `flows/5ed94b/vision/seats.md:3` (2026-10-03) <- `flows/d66c26/vision/layers.md:3` (2026-10-03); `flows/edf227/vision/layers.md:3` (2026-10-03); `flows/28d847/vision/layers.md:3` (2026-10-03~); `flows/dea0ba/vision/subflows.md:13` (2026-10-03~)
- keep `flows/5ed94b/vision/visionBooks.md:11` (2026-10-03) <- `flows/28d847/vision/books.md:11` (2026-10-03~)
- keep `flows/9fb0ad/vision/clusterMonitoring.md:3` (2026-10-03) <- `flows/dea0ba/vision/clusterMonitoring.md:1` (2026-10-03)
- keep `flows/9fb0ad/vision/contactingTheLiving.md:3` (2026-10-03) <- `flows/dea0ba/vision/contactingTheLiving.md:1` (2026-10-03)
- keep `flows/9fb0ad/vision/ethosLibrary.md:9` (2026-10-03) <- `flows/dea0ba/vision/ethosLibrary.md:1` (2026-10-03)
- keep `flows/9fb0ad/vision/messaging.md:3` (2026-10-03) <- `flows/dea0ba/vision/messaging.md:2` (2026-10-03)
- keep `flows/9fb0ad/vision/permissions.md:3` (2026-10-03) <- `flows/dea0ba/vision/permissions.md:1` (2026-10-03)
- keep `flows/d66c26/vision/quota-metrics.md:3` (2026-10-03) <- `flows/28d847/vision/quotas.md:17` (2026-10-03~)
- keep `flows/dea0ba/vision/books.md:1` (2026-10-03) <- `flows/edf227/vision/topics.md:3` (2026-10-03)
- keep `flows/28d847/vision/books.md:17` (2026-10-03~) <- `flows/5ed94b/vision/visionBooks.md:33` (2026-10-04)
- keep `flows/28d847/vision/books.md:25` (2026-10-03~) <- `flows/bad807/vision/presentations.md:3` (2026-10-04); `flows/d66c26/vision/books.md:2` (2026-10-04)
- keep `flows/28d847/vision/layers.md:11` (2026-10-03~) <- `flows/41fa34/vision/layers.md:18` (2026-10-03~); `flows/dea0ba/vision/voices.md:15` (2026-10-03~)
- keep `flows/28d847/vision/layers.md:19` (2026-10-03~) <- `flows/5ed94b/vision/seats.md:11` (2026-10-04)
- keep `flows/28d847/vision/nexus.md:3` (2026-10-03~) <- `flows/5ed94b/vision/nexusEntryPoint.md:3` (2026-10-04)
- keep `flows/28d847/vision/skills.md:39` (2026-10-03~) <- `flows/bad807/vision/skills.md:3` (2026-10-04)
- keep `flows/bad807/notion/topicFlows.md:3` (2026-10-04) <- `flows/d66c26/notion/topic-flows.md:2` (2026-10-04)
- keep `flows/bad807/vision/distillation.md:12` (2026-10-04) <- `flows/d66c26/vision/proposals.md:2` (2026-10-04)
- keep `flows/bad807/vision/distillation.md:20` (2026-10-04) <- `flows/aa887c/vision/distillation.md:3` (2026-10-04~)
- keep `flows/bad807/vision/ethos.md:3` (2026-10-04) <- `flows/aa887c/vision/ethos.md:3` (2026-10-04~)
- keep `flows/bad807/vision/flowContextInjection.md:3` (2026-10-04) <- `flows/d66c26/vision/flow-context-injection.md:2` (2026-10-04)
- keep `flows/bad807/vision/messaging.md:3` (2026-10-04) <- `flows/d66c26/vision/messaging.md:2` (2026-10-04)
- keep `flows/bad807/vision/nexus.md:3` (2026-10-04) <- `flows/aa887c/vision/nexus.md:3` (2026-10-04~)
- keep `flows/bad807/vision/nexus.md:11` (2026-10-04) <- `flows/aa887c/vision/nexus.md:11` (2026-10-04~)
- keep `flows/bad807/vision/nexus.md:19` (2026-10-04) <- `flows/aa887c/vision/nexus.md:23` (2026-10-04~)
- keep `flows/bad807/vision/nexus.md:27` (2026-10-04) <- `flows/aa887c/vision/nexus.md:31` (2026-10-04~)
- keep `flows/bad807/vision/voices.md:3` (2026-10-04) <- `flows/d66c26/vision/voices.md:2` (2026-10-04)
- keep `flows/bad807/vision/workspace.md:3` (2026-10-04) <- `flows/28d847/vision/workspace.md:3` (2026-10-04~); `flows/dea0ba/vision/workspace.md:3` (2026-10-05~)
- keep `flows/8475a9/vision/messenger.md:3` (2026-10-05) <- `flows/d66c26/vision/messaging.md:9` (2026-10-05); `flows/f768df/vision/messenger.md:3` (2026-10-05); `flows/d4ae97/vision/messenger.md:3` (2026-10-06~)
- keep `flows/8475a9/vision/messenger.md:11` (2026-10-05) <- `flows/f768df/vision/messenger.md:13` (2026-10-05)
- keep `flows/8475a9/vision/voices.md:3` (2026-10-05) <- `flows/d66c26/vision/voices.md:8` (2026-10-05); `flows/f768df/vision/voices.md:3` (2026-10-05); `flows/d4ae97/vision/voices.md:3` (2026-10-06~)
- keep `flows/8475a9/vision/voices.md:13` (2026-10-05) <- `flows/d66c26/vision/voice-registry.md:2` (2026-10-05); `flows/f768df/vision/voices.md:14` (2026-10-05); `flows/d4ae97/vision/voices.md:13` (2026-10-06~)
- keep `flows/8475a9/vision/voices.md:29` (2026-10-05) <- `flows/f768df/vision/voices.md:23` (2026-10-05)
- keep `flows/8475a9/vision/voices.md:39` (2026-10-05) <- `flows/f768df/vision/layers.md:3` (2026-10-05)
- keep `flows/8475a9/vision/voices.md:63` (2026-10-05) <- `flows/f768df/vision/voices.md:35` (2026-10-05); `flows/d4ae97/vision/vocabulary.md:3` (2026-10-06~)
- keep `flows/8475a9/vision/voices.md:71` (2026-10-05) <- `flows/f768df/vision/voices.md:44` (2026-10-05); `flows/d4ae97/vision/voices.md:21` (2026-10-06~)
- keep `flows/8475a9/vision/voices.md:91` (2026-10-05) <- `flows/f768df/vision/voices.md:52` (2026-10-05)
- keep `flows/d66c26/vision/books.md:9` (2026-10-05) <- `flows/d4ae97/vision/books.md:3` (2026-10-06~)
- keep `flows/d66c26/vision/voices.md:17` (2026-10-05) <- `flows/d4ae97/vision/flow.md:3` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:16` (2026-10-06) <- `flows/f768df/vision/flow.md:2` (2026-10-06); `flows/d4ae97/vision/flow.md:11` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:24` (2026-10-06) <- `flows/d4ae97/vision/books.md:36` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:32` (2026-10-06) <- `flows/f768df/vision/flow.md:10` (2026-10-06); `flows/d4ae97/vision/flow.md:19` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:42` (2026-10-06) <- `flows/f768df/vision/flow.md:20` (2026-10-06); `flows/d4ae97/vision/flow.md:29` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:50` (2026-10-06) <- `flows/d4ae97/vision/flow.md:37` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:58` (2026-10-06) <- `flows/f768df/vision/flow.md:28` (2026-10-06); `flows/d4ae97/vision/ethos.md:3` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:66` (2026-10-06) <- `flows/f768df/vision/books.md:12` (2026-10-06); `flows/d4ae97/vision/books.md:44` (2026-10-06~)
- keep `flows/8475a9/vision/flow.md:74` (2026-10-06) <- `flows/f768df/vision/flow.md:36` (2026-10-06); `flows/d4ae97/vision/flow.md:45` (2026-10-06~)
- keep `flows/8475a9/vision/livingMessenger.md:3` (2026-10-06) <- `flows/f768df/vision/living-messenger.md:2` (2026-10-06); `flows/d4ae97/vision/livingMessenger.md:3` (2026-10-06~)
- keep `flows/e5a0bc/vision/books.md:19` (2026-10-06~) <- `flows/f768df/vision/books.md:20` (2026-10-07)
- keep `flows/02dda6/vision/books-as-web.md:1` (2026-10-07) <- `flows/d4ae97/vision/books.md:95` (2026-10-07); `flows/6aa08d/vision/books.md:2` (2026-10-09~); `flows/4ddfe1/vision/books.md:3` (2026-10-10~)
- keep `flows/d4ae97/vision/books.md:60` (2026-10-07) <- `flows/f5a6e9/vision/books.md:3` (2026-10-07~)
- keep `flows/d4ae97/vision/flow.md:131` (2026-10-07) <- `flows/f5a6e9/vision/flow.md:87` (2026-10-07~)
- keep `flows/d4ae97/vision/skills.md:86` (2026-10-07) <- `flows/ebbe30/vision/vision.md:1` (2026-10-07)
- keep `flows/d4ae97/vision/skills.md:93` (2026-10-07) <- `flows/ebbe30/vision/vision.md:9` (2026-10-07)
- keep `flows/db38f8/vision/booksAndProposals.md:1` (2026-10-07) <- `flows/f5a6e9/vision/books.md:11` (2026-10-07~)
- keep `flows/f5a6e9/vision/books.md:23` (2026-10-07~) <- `flows/ebbe30/vision/books.md:1` (2026-10-09)
- keep `flows/f5a6e9/vision/flow.md:103` (2026-10-07~) <- `flows/445410/vision/flow.md:1` (2026-10-09); `flows/4ddfe1/vision/core.md:3` (2026-10-10~)
- keep `flows/f5a6e9/vision/flow.md:119` (2026-10-07~) <- `flows/1d0733/vision/ethos.md:1` (2026-10-09); `flows/445410/vision/flow.md:33` (2026-10-09); `flows/9fed42/vision/flow.md:1` (2026-10-09)
- keep `flows/f5a6e9/vision/flow.md:127` (2026-10-07~) <- `flows/0c85a3/vision/startup-task.md:2` (2026-10-09); `flows/73ada7/vision/flow.md:3` (2026-10-09); `flows/9fed42/vision/flow.md:9` (2026-10-09); `flows/ebbe30/vision/flow-startup.md:25` (2026-10-09)
- keep `flows/f5a6e9/vision/flow.md:135` (2026-10-07~) <- `flows/9fed42/vision/flow.md:17` (2026-10-09)
- keep `flows/f5a6e9/vision/flow.md:143` (2026-10-07~) <- `flows/9fed42/vision/flow.md:25` (2026-10-09)
- keep `flows/f5a6e9/vision/messaging.md:11` (2026-10-08~) <- `flows/445410/vision/messaging.md:25` (2026-10-09); `flows/ebbe30/vision/messaging.md:1` (2026-10-09)
- keep `flows/0c85a3/vision/aspect-topics.md:2` (2026-10-09) <- `flows/73ada7/vision/flow.md:11` (2026-10-09)
- keep `flows/1d0733/notion/ethos.md:1` (2026-10-09) <- `flows/d5df1d/notion/ethos.md:3` (2026-10-09)
- keep `flows/1d0733/vision/ethos.md:39` (2026-10-09) <- `flows/d5df1d/vision/ethos.md:46` (2026-10-10~)
- keep `flows/445410/notion/metaflow-ethos.md:1` (2026-10-09) <- `flows/dcd651/notion/metaflow.md:3` (2026-10-09); `flows/f5a6e9/notion/flow.md:3` (2026-10-09~); `flows/4ddfe1/notion/metaflow-ethos.md:3` (2026-10-10~)
- keep `flows/445410/vision/books.md:1` (2026-10-09) <- `flows/4ddfe1/vision/books.md:8` (2026-10-10~)
- keep `flows/445410/vision/messaging.md:1` (2026-10-09) <- `flows/4ddfe1/vision/voice-relay.md:9` (2026-10-10~)
- keep `flows/445410/vision/messaging.md:9` (2026-10-09) <- `flows/4ddfe1/vision/voice-relay.md:15` (2026-10-10~)
- keep `flows/445410/vision/messaging.md:17` (2026-10-09) <- `flows/4ddfe1/vision/voice-relay.md:21` (2026-10-10~)
- keep `flows/73ada7/vision/messaging.md:3` (2026-10-09) <- `flows/9fed42/vision/messaging.md:1` (2026-10-09)
- keep `flows/d5df1d/vision/ethos.md:27` (2026-10-09) <- `flows/f5a6e9/vision/contextModules.md:3` (2026-10-09~)
- keep `flows/058f16/notion/ethos.md:3` (2026-10-10) <- `flows/081064/notion/ethos.md:3` (2026-10-10); `flows/23824a/notion/rustTypes.md:3` (2026-10-10~); `flows/d68c82/notion/ethos.md:3` (2026-10-10~)
- keep `flows/058f16/vision/book.md:3` (2026-10-10) <- `flows/d68c82/vision/books.md:3` (2026-10-10~)
- keep `flows/058f16/vision/source.md:3` (2026-10-10) <- `flows/d68c82/vision/source.md:42` (2026-10-10~)
- keep `flows/058f16/vision/source.md:23` (2026-10-10) <- `flows/23824a/vision/registry.md:3` (2026-10-10~)
- keep `flows/058f16/vision/source.md:31` (2026-10-10) <- `flows/d68c82/vision/source.md:20` (2026-10-10~)
- keep `flows/081064/vision/ethos.md:18` (2026-10-10) <- `flows/23824a/vision/sources.md:3` (2026-10-10~)
- keep `flows/081064/vision/ethos.md:26` (2026-10-10) <- `flows/23824a/vision/names.md:3` (2026-10-10~)
- keep `flows/081064/vision/ethos.md:72` (2026-10-10) <- `flows/875960/vision/distillation.md:3` (2026-10-10)
- keep `flows/081064/vision/ethos.md:92` (2026-10-10) <- `flows/23824a/vision/commitMessage.md:13` (2026-10-10~); `flows/d68c82/vision/commitMessage.md:15` (2026-10-10~)
- keep `flows/875960/vision/distillation.md:11` (2026-10-10) <- `flows/d68c82/vision/distillation.md:11` (2026-10-10~)
- keep `flows/875960/vision/harness.md:3` (2026-10-10) <- `flows/d68c82/vision/metaHarness.md:3` (2026-10-10); `flows/9519a1/vision/metaHarness.md:1` (2026-10-10~)
- keep `flows/875960/vision/persona.md:3` (2026-10-10) <- `flows/d68c82/vision/persona.md:3` (2026-10-10~)
- keep `flows/875960/vision/persona.md:19` (2026-10-10) <- `flows/d68c82/vision/persona.md:11` (2026-10-10~)
- keep `flows/d68c82/vision/books.md:16` (2026-10-10~) <- `flows/875960/vision/books.md:11` (2026-10-11)
- keep `flows/d68c82/vision/distillation.md:18` (2026-10-10~) <- `flows/d55c56/vision/spirit.md:11` (2026-10-11)
- keep `flows/875960/vision/flow.md:35` (2026-10-11) <- `flows/9519a1/vision/messaging.md:1` (2026-10-11~)
- keep `flows/081064/notion/ethos.md:12` (2026-10-12) <- `flows/d68c82/notion/ethos.md:13` (2026-10-12); `flows/23824a/notion/delimiters.md:3` (2026-10-12~)
- keep `flows/33752b/vision/design.md:67` (2026-10-12) <- `flows/875960/vision/nexus.md:3` (2026-10-12); `flows/d68c82/vision/design.md:20` (2026-10-12)
- keep `flows/d68c82/vision/seats.md:2` (2026-10-12) <- `flows/ee57fb/vision/launch.md:3` (2026-10-12)
- keep `flows/081064/vision/correction.md:3` (2026-10-13) <- `flows/d68c82/vision/psyche.md:54` (2026-10-13)
- keep `flows/d55c56/vision/makeshift.md:21` (2026-10-13) <- `flows/d68c82/vision/psyche.md:29` (2026-10-13)
- keep `flows/17ac8a/vision/communication.md:70` (2026-10-14) <- `flows/3960eb/vision/communication.md:37` (2026-10-14); `flows/d68c82/vision/books.md:157` (2026-10-14)
- keep `flows/17ac8a/vision/communication.md:77` (2026-10-14) <- `flows/3960eb/vision/communication.md:45` (2026-10-14); `flows/7c89aa/vision/ethos-in-clojure.md:11` (2026-10-14); `flows/d68c82/vision/books.md:149` (2026-10-14); `flows/da2038/vision/books.md:22` (2026-10-14); `flows/df159a/vision/books.md:31` (2026-10-14~)
- keep `flows/3960eb/vision/communication.md:3` (2026-10-14) <- `flows/17ac8a/vision/communication.md:13` (?~)
- keep `flows/3960eb/vision/communication.md:11` (2026-10-14) <- `flows/17ac8a/vision/communication.md:20` (?~)
- keep `flows/3960eb/vision/communication.md:29` (2026-10-14) <- `flows/17ac8a/vision/communication.md:27` (?~)
- keep `flows/55a2b4/vision/flow.md:3` (2026-10-14) <- `flows/d68c82/vision/flow.md:164` (2026-10-14); `flows/da2038/vision/flow.md:78` (2026-10-14)
- keep `flows/7c89aa/vision/ethos-in-clojure.md:3` (2026-10-14) <- `flows/d68c82/vision/ethos.md:21` (2026-10-14); `flows/da2038/vision/ethos.md:2` (2026-10-14); `flows/df159a/vision/clojure.md:3` (2026-10-14~)
- keep `flows/d68c82/vision/context-modules.md:154` (2026-10-14) <- `flows/da2038/vision/skills.md:2` (2026-10-14)
- keep `flows/d68c82/vision/ethos.md:47` (2026-10-14) <- `flows/da2038/vision/flow.md:102` (2026-10-14)
- keep `flows/d68c82/vision/flow.md:140` (2026-10-14) <- `flows/da2038/vision/flow.md:36` (2026-10-14)
- keep `flows/d68c82/vision/flow.md:148` (2026-10-14) <- `flows/da2038/vision/flow.md:62` (2026-10-14)
- keep `flows/d68c82/vision/flow.md:156` (2026-10-14) <- `flows/da2038/vision/flow.md:70` (2026-10-14)
- keep `flows/d68c82/vision/visualization.md:11` (2026-10-14) <- `flows/da2038/vision/books.md:30` (2026-10-14)
- keep `flows/da2038/vision/books.md:2` (2026-10-14) <- `flows/df159a/vision/books.md:3` (2026-10-14~)
- keep `flows/da2038/vision/books.md:12` (2026-10-14) <- `flows/df159a/vision/books.md:13` (2026-10-14~)
- keep `flows/da2038/vision/flow.md:18` (2026-10-14) <- `flows/df159a/vision/flow.md:3` (2026-10-14~)
- keep `flows/da2038/vision/models.md:2` (2026-10-14) <- `flows/df159a/vision/models.md:3` (2026-10-14~)
- keep `flows/5b9075/vision/clojure.md:2` (?~) <- `flows/e4b7d7/vision/clojure.md:1` (?~)

### 3b. Contained copies (259): the whole quoted text of the first record sits inside the longer record of another flow

Keep the longer record; the shorter one is an excerpt of it. Format: excerpt `path:line` (date) inside longer `path:line` (date).

- `flows/019fe121/vision/hostEnvironmentRecovery.md:11` (2026-08-08) inside `flows/01a02b46/vision/zeusUpdate.md:11` (2026-08-08)
- `flows/019fe121/vision/hostEnvironmentRecovery.md:25` (2026-08-08) inside `flows/01a02b46/vision/zeusUpdate.md:11` (2026-08-08)
- `flows/019fe121/vision/hostEnvironmentRecovery.md:36` (2026-08-08) inside `flows/01a02b46/vision/zeusUpdate.md:11` (2026-08-08)
- `flows/019fe121/vision/hostEnvironmentRecovery.md:46` (2026-08-08) inside `flows/01a02b46/vision/zeusUpdate.md:11` (2026-08-08)
- `flows/019fe121/vision/hostEnvironmentRecovery.md:71` (2026-08-08) inside `flows/01a02b46/vision/zeusUpdate.md:11` (2026-08-08)
- `flows/fd301d9a/vision/actorLibrary.md:33` (2026-08-14) inside `vision-raw/archive-rustComponentArchitecture.md:3` [A] (2026-08-14)
- `vision-raw/lojixOwnership.md:19` (2026-08-14) inside `flows/01a02b46/vision/zeusUpdate.md:47` (2026-08-13)
- `vision-raw/setupIndependentInterfaces.md:1` (2026-08-14) inside `flows/01a02b46/vision/zeusUpdate.md:57` (2026-08-14)
- `vision-raw/setupIndependentInterfaces.md:7` (2026-08-14) inside `flows/01a02b46/vision/zeusUpdate.md:57` (2026-08-14)
- `vision-raw/setupIndependentInterfaces.md:13` (2026-08-14) inside `flows/01a02b46/vision/zeusUpdate.md:57` (2026-08-14)
- `flows/fd301d9a/vision/nexusTraits.md:15` (2026-08-19) inside `flows/e06e4c07/vision/archive-nexus.md:125` [A] (2026-08-19)
- `vision-raw/setupIndependentInterfaces.md:31` (2026-08-19) inside `flows/01a02b46/vision/zeusUpdate.md:57` (2026-08-14)
- `flows/fd301d9a/vision/archive-nexusTraits.md:9` [A] (2026-08-19) inside `flows/e06e4c07/vision/archive-nexus.md:79` [A] (2026-08-19)
- `flows/01a03eda/vision/archive-datomSyntax.md:4` [A] (2026-08-26) inside `flows/ac1e9ec8/vision/archive-datomSyntax.md:95` [A] (2026-08-26)
- `flows/024bc7/vision/speechToText.md:3` (2026-09-13) inside `flows/bcd02a/notion/speech.md:3` (2026-09-13)
- `flows/bcd02a/notion/models.md:3` (2026-09-13) inside `flows/024bc7/vision/parallelSessions.md:13` (2026-09-13)
- `flows/bcd02a/notion/router.md:11` (2026-09-13) inside `flows/024bc7/vision/router.md:3` (2026-09-13)
- `flows/bcd02a/notion/sandbox.md:3` (2026-09-13) inside `flows/024bc7/vision/sandbox.md:3` (2026-09-13)
- `flows/bcd02a/notion/sandbox.md:11` (2026-09-13) inside `flows/024bc7/vision/sandbox.md:3` (2026-09-13)
- `flows/bcd02a/vision/context.md:11` (2026-09-13) inside `flows/024bc7/vision/context.md:3` (2026-09-13)
- `flows/bcd02a/vision/council.md:3` (2026-09-13) inside `flows/024bc7/vision/parallelSessions.md:19` (2026-09-13)
- `flows/bcd02a/vision/nexus.md:3` (2026-09-13) inside `flows/024bc7/vision/nexus.md:3` (2026-09-13)
- `flows/bcd02a/vision/paired-flows.md:3` (2026-09-13) inside `flows/024bc7/vision/parallelSessions.md:25` (2026-09-13)
- `flows/bcd02a/vision/paired-flows.md:9` (2026-09-13) inside `flows/024bc7/vision/parallelSessions.md:13` (2026-09-13)
- `flows/bcd02a/vision/runtime.md:3` (2026-09-13) inside `flows/024bc7/vision/nexus.md:19` (2026-09-13)
- `flows/bcd02a/vision/signal.md:3` (2026-09-13) inside `flows/024bc7/vision/signal.md:3` (2026-09-13)
- `flows/056f6d/vision/messaging.md:3` (2026-09-18) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/056f6d/vision/psycheGeneratedMessaging.md:3` (2026-09-18) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/c7128c/vision/messageAndFlow.md:3` (2026-09-18) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/c7128c/vision/psycheVersusMachineMessaging.md:3` (2026-09-18) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/1ac573/vision/operational-fableFlowAndOpusComparison.md:3` (2026-09-18~) inside `flows/908786/vision/vision-led-audit-and-fable.md:1` (2026-09-18~)
- `flows/1ac573/vision/operational-visionLedAudit.md:3` (2026-09-18~) inside `flows/908786/vision/vision-led-audit-and-fable.md:1` (2026-09-18~)
- `flows/b05237/vision/operational-fieldEnergyLevels.md:3` (2026-09-18~) inside `flows/893603/vision/claude-persistence.md:11` (2026-09-18)
- `flows/b05237/vision/operational-fieldKeepsThingsWorking.md:3` (2026-09-18~) inside `flows/33ba2b/vision/operational-fieldRefreshSuccession.md:3` (2026-09-18~)
- `flows/b05237/vision/operational-fieldTwoSeatsAndRefreshNaming.md:3` (2026-09-18~) inside `flows/33ba2b/vision/operational-fieldRefreshSuccession.md:3` (2026-09-18~)
- `flows/b05237/vision/operational-primaryNextPsycheLogging.md:3` (2026-09-18~) inside `flows/33ba2b/vision/psycheDataArchitecture.md:18` (2026-09-18~)
- `flows/b05237/vision/operational-typedMessagesDistinguishPsyche.md:3` (2026-09-18~) inside `flows/33ba2b/vision/psycheDataArchitecture.md:18` (2026-09-18~)
- `flows/b7ba00/vision/meaningLanguage.md:73` (2026-09-19) inside `flows/b81560/vision/archive-operational-asyncSubflowsAndMeaningLanguage.md:3` [A] (2026-09-20~)
- `flows/1f96fc/vision/fieldMaintenanceAndRefresh.md:8` (2026-09-19~) inside `flows/b81560/vision/operational-psychePropagationAndNamingAndInfrastructure.md:3` (2026-09-19~)
- `flows/f38926/vision/archive-subflows.md:3` [A] (2026-09-20~) inside `flows/b81560/vision/archive-operational-asyncSubflowsAndMeaningLanguage.md:3` [A] (2026-09-20~)
- `flows/d8df70/vision/flashbooks.md:15` (2026-09-23) inside `flows/836818/vision/flashbooks.md:17` (2026-09-23)
- `flows/d8df70/vision/flashbooks.md:21` (2026-09-23) inside `flows/836818/vision/flashbooks.md:17` (2026-09-23)
- `flows/d8df70/vision/flashbooks.md:27` (2026-09-23) inside `flows/836818/vision/flashbooks.md:17` (2026-09-23)
- `flows/d8df70/vision/flashbooks.md:33` (2026-09-23) inside `flows/836818/vision/flashbooks.md:17` (2026-09-23)
- `flows/d8df70/vision/building.md:9` (2026-09-24) inside `flows/836818/vision/flowNexus.md:21` (2026-09-24)
- `flows/d8df70/vision/deployment.md:3` (2026-09-24) inside `flows/836818/vision/flowNexus.md:39` (2026-09-24)
- `flows/d8df70/vision/flashbooks.md:51` (2026-09-24) inside `flows/836818/vision/flashbooks.md:31` (2026-09-24)
- `flows/d8df70/vision/flowLifecycle.md:3` (2026-09-24) inside `flows/836818/vision/flowNexus.md:21` (2026-09-24)
- `flows/d8df70/vision/flowLifecycle.md:9` (2026-09-24) inside `flows/836818/vision/flowNexus.md:21` (2026-09-24)
- `flows/d8df70/vision/flowTool.md:3` (2026-09-24) inside `flows/836818/vision/flowNexus.md:21` (2026-09-24)
- `flows/d8df70/vision/messaging.md:58` (2026-09-24) inside `flows/836818/vision/flowNexus.md:9` (2026-09-24)
- `flows/d8df70/vision/messaging.md:64` (2026-09-24) inside `flows/836818/vision/flowNexus.md:21` (2026-09-24)
- `flows/b7da5d/vision/prometheusBuilder.md:17` (2026-09-25) inside `flows/da88cf/vision/prometheus.md:19` (2026-09-25)
- `flows/da88cf/vision/prometheus.md:39` (2026-09-25) inside `flows/26c50c/vision/build-placement.md:2` (2026-09-25)
- `flows/88475f/vision/flow.md:1` (2026-09-25~) inside `flows/e51411/vision/authority.md:27` (2026-09-24)
- `flows/88475f/vision/integration.md:25` (2026-09-25~) inside `flows/da88cf/vision/prometheus.md:55` (2026-09-25)
- `flows/88475f/vision/nexus.md:1` (2026-09-25~) inside `flows/e51411/vision/nexus.md:3` (2026-09-25)
- `flows/88475f/vision/titles.md:1` (2026-09-25~) inside `flows/e51411/vision/titles.md:19` (2026-09-25)
- `flows/88475f/vision/waiting.md:1` (2026-09-25~) inside `flows/e51411/vision/authority.md:11` (2026-09-24)
- `flows/6fe957/vision/prometheus-networking.md:2` (2026-09-26) inside `flows/19ff9f/vision/prometheus-wifi.md:1` (2026-10-01~)
- `flows/93ba9f/vision/automation.md:1` (2026-09-26) inside `flows/b7ba00/vision/modelFlows.md:35` (2026-09-26)
- `flows/93ba9f/vision/sessionClosing.md:1` (2026-09-26) inside `flows/b7ba00/vision/modelFlows.md:35` (2026-09-26)
- `flows/b7ba00/vision/flowAnatomy.md:3` (2026-09-26) inside `flows/93ba9f/vision/flowLaunching.md:1` (2026-09-26)
- `flows/b7ba00/vision/meaningLanguage.md:5` (2026-09-26) inside `flows/93ba9f/vision/meaningLanguage.md:1` (2026-09-26)
- `flows/b7ba00/vision/meaningLanguage.md:19` (2026-09-26) inside `flows/93ba9f/vision/ethosNames.md:1` (2026-09-26)
- `flows/b7ba00/vision/meaningLanguage.md:31` (2026-09-26) inside `flows/b860be/vision/layerVocabulary.md:1` (2026-09-26)
- `flows/b7ba00/vision/meaningLanguage.md:139` (2026-09-26) inside `flows/93ba9f/vision/meaningLanguage.md:1` (2026-09-26)
- `flows/b7ba00/vision/meaningLanguage.md:155` (2026-09-26) inside `flows/93ba9f/vision/meaningLanguage.md:1` (2026-09-26)
- `flows/b7ba00/vision/meaningLanguage.md:161` (2026-09-26) inside `flows/93ba9f/vision/meaningLanguage.md:1` (2026-09-26)
- `flows/b7ba00/vision/messaging.md:3` (2026-09-26) inside `flows/93ba9f/vision/messagingInterface.md:1` (2026-09-26)
- `flows/b7ba00/vision/messaging.md:11` (2026-09-26) inside `flows/93ba9f/vision/messagingInterface.md:1` (2026-09-26)
- `flows/b7ba00/vision/messaging.md:19` (2026-09-26) inside `flows/93ba9f/vision/messagingInterface.md:1` (2026-09-26)
- `flows/b7ba00/vision/messaging.md:25` (2026-09-26) inside `flows/93ba9f/vision/messagingInterface.md:1` (2026-09-26)
- `flows/b7ba00/vision/messaging.md:39` (2026-09-26) inside `flows/93ba9f/vision/messagingInterface.md:1` (2026-09-26)
- `flows/b7ba00/vision/messaging.md:77` (2026-09-26) inside `flows/93ba9f/vision/messagingInterface.md:1` (2026-09-26)
- `flows/b7ba00/vision/messaging.md:97` (2026-09-26) inside `flows/93ba9f/vision/messagingInterface.md:1` (2026-09-26)
- `flows/b7ba00/vision/modelFlows.md:11` (2026-09-26) inside `flows/93ba9f/vision/flowLaunching.md:1` (2026-09-26)
- `flows/b7ba00/vision/modelFlows.md:19` (2026-09-26) inside `flows/93ba9f/vision/flowLaunching.md:1` (2026-09-26)
- `flows/b7ba00/vision/modelFlows.md:27` (2026-09-26) inside `flows/93ba9f/vision/flowLaunching.md:1` (2026-09-26)
- `flows/b7ba00/vision/reachingTheLiving.md:3` (2026-09-26) inside `flows/93ba9f/vision/presentation.md:1` (2026-09-26)
- `flows/b7ba00/vision/types.md:3` (2026-09-26) inside `flows/93ba9f/vision/ethosNames.md:1` (2026-09-26)
- `flows/b7ba00/vision/wordIds.md:3` (2026-09-26) inside `flows/93ba9f/vision/wordIdentifiers.md:1` (2026-09-26)
- `flows/b7da5d/vision/piper.md:1` (2026-09-26) inside `flows/b860be/vision/ouranos.md:3` (2026-09-26)
- `flows/b7da5d/vision/refreshHooks.md:11` (2026-09-26) inside `flows/b860be/vision/refreshAutomation.md:3` (2026-09-26)
- `flows/b860be/vision/datomSyntax.md:3` (2026-09-26) inside `flows/f5a74e/vision/datom-messaging.md:2` (2026-09-26)
- `flows/e167d8/vision/deployment.md:3` (2026-09-26) inside `flows/b860be/vision/deployment.md:3` (2026-09-26)
- `flows/e167d8/vision/independentReview.md:3` (2026-09-26) inside `flows/b860be/vision/layerVocabulary.md:1` (2026-09-26)
- `flows/e167d8/vision/psycheMessages.md:13` (2026-09-26) inside `flows/f5a74e/vision/datom-messaging.md:2` (2026-09-26)
- `flows/e167d8/vision/refresh.md:3` (2026-09-26) inside `flows/b860be/vision/refreshAutomation.md:3` (2026-09-26)
- `flows/f5a74e/vision/refresh-hooks.md:2` (2026-09-26) inside `flows/b860be/vision/refreshAutomation.md:3` (2026-09-26)
- `flows/6f51ad/vision/communication.md:3` (2026-09-28) inside `flows/c02c0d/vision/seats.md:19` (2026-09-28)
- `flows/6f51ad/vision/mentci.md:2` (2026-09-28) inside `flows/8904b1/vision/presentation.md:21` (2026-09-28)
- `flows/6f51ad/vision/zeus.md:3` (2026-09-28) inside `flows/8904b1/vision/deployment.md:9` (2026-09-28)
- `flows/183ae0/vision/presentation.md:3` (2026-09-28~) inside `flows/6f51ad/vision/presentation.md:3` (2026-09-28)
- `flows/bd0019/vision/hook.md:3` (2026-09-29) inside `flows/6f51ad/vision/clusterSurvey.md:3` (2026-09-29)
- `flows/bd0019/vision/userPromptLayer.md:3` (2026-09-29) inside `flows/6f51ad/vision/clusterSurvey.md:3` (2026-09-29)
- `flows/c64ee3/notion/hooks.md:3` (2026-09-29) inside `flows/6f51ad/vision/clusterSurvey.md:3` (2026-09-29)
- `flows/c64ee3/vision/aspects.md:3` (2026-09-29) inside `flows/6f51ad/vision/clusterSurvey.md:3` (2026-09-29)
- `flows/caf622/vision/stateful-installation.md:2` (2026-09-29) inside `flows/b666e7/vision/stateful.md:2` (2026-09-29~)
- `flows/d5b96b/vision/prometheus-wifi.md:2` (2026-09-29) inside `flows/6f51ad/vision/network.md:3` (2026-09-29)
- `flows/183ae0/vision/messaging.md:3` (2026-09-29~) inside `flows/6f51ad/vision/registration.md:3` (2026-09-29)
- `flows/b666e7/vision/network.md:2` (2026-09-29~) inside `flows/6f51ad/vision/network.md:3` (2026-09-29)
- `flows/b666e7/vision/triad.md:22` (2026-09-29~) inside `flows/6f51ad/vision/clusterSurvey.md:3` (2026-09-29)
- `flows/b666e7/vision/triad.md:30` (2026-09-29~) inside `flows/6f51ad/vision/clusterSurvey.md:3` (2026-09-29)
- `flows/7328f4/vision/hooks.md:3` (2026-09-30) inside `flows/b666e7/notion/hook.md:10` (2026-09-29~)
- `flows/bd0019/vision/aspect.md:3` (2026-09-30) inside `flows/7328f4/vision/books.md:13` (2026-09-30)
- `flows/fe945a/vision/stableNext.md:31` (2026-09-30) inside `flows/d5b96b/notion/codex-update.md:2` (2026-09-30)
- `flows/1bc255/vision/pollingSystems.md:1` (2026-09-30~) inside `flows/7328f4/vision/polling.md:3` (2026-09-30)
- `flows/b666e7/vision/hook.md:22` (2026-09-30~) inside `flows/7328f4/vision/polling.md:3` (2026-09-30)
- `flows/bd0019/vision/clusterNotBlocking.md:3` (2026-10-01) inside `flows/fe945a/vision/cluster.md:3` (2026-10-01)
- `flows/fe945a/vision/books.md:3` (2026-10-01) inside `flows/bd0019/vision/transcriptNotFiles.md:3` (2026-10-01)
- `flows/af762b/vision/operational-flowOwnsHerdr.md:3` (2026-10-01~) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/af762b/vision/operational-psycheGeneratedMessaging.md:3` (2026-10-01~) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/af762b/vision/operational-psycheLogDuty.md:3` (2026-10-01~) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/af762b/vision/operational-refreshAndImplementClosestLayer.md:3` (2026-10-01~) inside `flows/b05237/vision/operational-messagingToDeployment.md:3` (2026-09-18~)
- `flows/01e496/vision/books.md:3` (2026-10-02) inside `flows/41fa34/vision/living-messenger.md:1` (2026-10-02)
- `flows/01e496/vision/books.md:11` (2026-10-02) inside `flows/41fa34/vision/living-messenger.md:1` (2026-10-02)
- `flows/01e496/vision/books.md:19` (2026-10-02) inside `flows/41fa34/vision/reusing-a-commented-book.md:1` (2026-10-02)
- `flows/01e496/vision/flashbook.md:3` (2026-10-02) inside `flows/d86ec0/vision/bookFlowcharts.md:3` (2026-10-02)
- `flows/01e496/vision/flowNexus.md:11` (2026-10-02) inside `flows/41fa34/vision/flow-component.md:9` (2026-10-02)
- `flows/01e496/vision/seat.md:3` (2026-10-02) inside `flows/41fa34/vision/seat-abstraction.md:9` (2026-10-02)
- `flows/41fa34/vision/checkboxes.md:1` (2026-10-02) inside `flows/91ea9f/vision/books.md:87` (2026-10-02)
- `flows/41fa34/vision/ethos-and-example-datom.md:2` (2026-10-02) inside `flows/91ea9f/vision/flowNexus.md:9` (2026-10-02)
- `flows/41fa34/vision/if-i-ask-for-a-new-flow.md:2` (2026-10-02) inside `flows/91ea9f/vision/flowLifecycle.md:3` (2026-10-02)
- `flows/41fa34/vision/semi-sandbox.md:2` (2026-10-02) inside `flows/3ec648/vision/capsule.md:3` (2026-10-02)
- `flows/41fa34/vision/simple-working-system.md:2` (2026-10-02) inside `flows/01e496/vision/simpleWorkingSystem.md:3` (2026-10-02)
- `flows/41fa34/vision/sonnet-comments.md:1` (2026-10-02) inside `flows/91ea9f/vision/ethos.md:36` (2026-10-02)
- `flows/41fa34/vision/who-implements-skill-proposals.md:1` (2026-10-02) inside `flows/01e496/vision/skills.md:3` (2026-10-02)
- `flows/42265e/vision/flashbooks.md:3` (2026-10-02) inside `flows/91ea9f/vision/books.md:77` (2026-10-02)
- `flows/42265e/vision/flashbooks.md:11` (2026-10-02) inside `flows/91ea9f/vision/books.md:77` (2026-10-02)
- `flows/42265e/vision/flashbooks.md:19` (2026-10-02) inside `flows/91ea9f/vision/books.md:69` (2026-10-02)
- `flows/41fa34/vision/flowLifecycle.md:2` (2026-10-03) inside `flows/9fb0ad/vision/flowLifecycle.md:3` (2026-10-03)
- `flows/41fa34/vision/flowLifecycle.md:10` (2026-10-03) inside `flows/9fb0ad/vision/flowLifecycle.md:3` (2026-10-03)
- `flows/41fa34/vision/identifiers.md:2` (2026-10-03) inside `flows/dea0ba/vision/identifiers.md:2` (2026-10-03)
- `flows/41fa34/vision/subflows.md:2` (2026-10-03) inside `flows/dea0ba/vision/subflows.md:2` (2026-10-03)
- `flows/5578cc/notion/permissions.md:3` (2026-10-03) inside `flows/9fb0ad/vision/permissions.md:3` (2026-10-03)
- `flows/5578cc/vision/behavior.md:3` (2026-10-03) inside `flows/dea0ba/vision/quotaTracking.md:1` (2026-10-03)
- `flows/5578cc/vision/behavior.md:19` (2026-10-03) inside `flows/edf227/vision/incorrectness.md:9` (2026-10-03)
- `flows/5578cc/vision/ethos.md:3` (2026-10-03) inside `flows/edf227/vision/contextModules.md:19` (2026-10-03)
- `flows/5578cc/vision/flow.md:27` (2026-10-03) inside `flows/dea0ba/vision/identifiers.md:2` (2026-10-03)
- `flows/5578cc/vision/flow.md:55` (2026-10-03) inside `flows/dea0ba/vision/systemPrompt.md:1` (2026-10-03)
- `flows/5578cc/vision/identifiers.md:19` (2026-10-03) inside `flows/dea0ba/vision/identifiers.md:2` (2026-10-03)
- `flows/5578cc/vision/permissions.md:3` (2026-10-03) inside `flows/9fb0ad/vision/permissions.md:3` (2026-10-03)
- `flows/9fb0ad/vision/identifiers.md:37` (2026-10-03) inside `flows/dea0ba/vision/identifiers.md:2` (2026-10-03)
- `flows/9fb0ad/vision/quotaTracking.md:3` (2026-10-03) inside `flows/dea0ba/vision/quotaTracking.md:1` (2026-10-03)
- `flows/edf227/vision/contextModules.md:29` (2026-10-03) inside `flows/5578cc/vision/curriculum.md:3` (2026-10-03)
- `flows/edf227/vision/flow.md:3` (2026-10-03) inside `flows/dea0ba/vision/flowCorrections.md:1` (2026-10-03)
- `flows/edf227/vision/flow.md:9` (2026-10-03) inside `flows/dea0ba/vision/flowCorrections.md:1` (2026-10-03)
- `flows/edf227/vision/flow.md:14` (2026-10-03) inside `flows/dea0ba/vision/flowCorrections.md:1` (2026-10-03)
- `flows/edf227/vision/flowRole.md:3` (2026-10-03) inside `flows/dea0ba/vision/subflows.md:2` (2026-10-03)
- `flows/edf227/vision/flowRole.md:14` (2026-10-03) inside `flows/dea0ba/vision/flowCorrections.md:1` (2026-10-03)
- `flows/edf227/vision/visionNotification.md:3` (2026-10-03) inside `flows/dea0ba/vision/visionNotification.md:1` (2026-10-03)
- `flows/edf227/vision/visionNotification.md:8` (2026-10-03) inside `flows/dea0ba/vision/visionNotification.md:1` (2026-10-03)
- `flows/28d847/vision/books.md:3` (2026-10-03~) inside `flows/5ed94b/vision/visionBooks.md:3` (2026-10-03)
- `flows/28d847/vision/curriculum.md:3` (2026-10-03~) inside `flows/5ed94b/vision/skills.md:3` (2026-10-03)
- `flows/28d847/vision/infrastructure.md:11` (2026-10-03~) inside `flows/5ed94b/vision/infrastructure.md:11` (2026-10-03)
- `flows/28d847/vision/skills.md:27` (2026-10-03~) inside `flows/5ed94b/vision/skills.md:3` (2026-10-03)
- `flows/28d847/vision/skills.md:33` (2026-10-03~) inside `flows/5ed94b/vision/skills.md:3` (2026-10-03)
- `flows/28d847/vision/subflows.md:3` (2026-10-03~) inside `flows/edf227/vision/subflowBriefs.md:9` (2026-10-03)
- `flows/28d847/vision/subflows.md:11` (2026-10-03~) inside `flows/edf227/vision/subflowBriefs.md:9` (2026-10-03)
- `flows/42265e/vision/finding-out.md:1` (2026-10-03~) inside `flows/dea0ba/vision/quotaTracking.md:1` (2026-10-03)
- `flows/8475a9/vision/voices.md:21` (2026-10-05) inside `flows/dea0ba/vision/voices.md:22` (2026-10-03~)
- `flows/d66c26/vision/books.md:9` (2026-10-05) inside `flows/8475a9/vision/voices.md:29` (2026-10-05)
- `flows/d66c26/vision/voices.md:17` (2026-10-05) inside `flows/8475a9/vision/voices.md:29` (2026-10-05)
- `flows/f768df/vision/layers.md:14` (2026-10-05) inside `flows/8475a9/vision/voices.md:79` (2026-10-05)
- `flows/f768df/vision/layers.md:23` (2026-10-05) inside `flows/8475a9/vision/voices.md:79` (2026-10-05)
- `flows/e5a0bc/vision/books.md:27` (2026-10-06~) inside `flows/db38f8/vision/ethosAndBookComments.md:1` (2026-10-06)
- `flows/e5a0bc/vision/ethos.md:3` (2026-10-06~) inside `flows/db38f8/vision/ethosAndBookComments.md:1` (2026-10-06)
- `flows/0c85a3/notion/memory.md:2` (2026-10-07) inside `flows/02dda6/notion/ethos-code-in-vision.md:1` (2026-10-07)
- `flows/0c85a3/notion/spirit.md:2` (2026-10-07) inside `flows/02dda6/vision/spirit-system-prompt.md:15` (2026-10-07)
- `flows/0c85a3/vision/ethos.md:1` (2026-10-07) inside `flows/d4ae97/vision/ethos.md:106` (2026-10-07)
- `flows/0c85a3/vision/shastra.md:1` (2026-10-07) inside `flows/02dda6/vision/spirit-system-prompt.md:1` (2026-10-07)
- `flows/0c85a3/vision/shastra.md:9` (2026-10-07) inside `flows/02dda6/vision/spirit-system-prompt.md:1` (2026-10-07)
- `flows/0c85a3/vision/spirit.md:2` (2026-10-07) inside `flows/02dda6/vision/spirit-system-prompt.md:15` (2026-10-07)
- `flows/0c85a3/vision/spirit.md:10` (2026-10-07) inside `flows/02dda6/vision/spirit-system-prompt.md:15` (2026-10-07)
- `flows/0c85a3/vision/spirit.md:18` (2026-10-07) inside `flows/02dda6/vision/spirit-system-prompt.md:15` (2026-10-07)
- `flows/0c85a3/vision/vision.md:2` (2026-10-07) inside `flows/02dda6/vision/ethos-code-in-vision.md:1` (2026-10-07)
- `flows/41fa34/vision/flow-registry.md:2` (2026-10-07) inside `flows/f5a6e9/vision/flow.md:71` (2026-10-07~)
- `flows/d4ae97/vision/skills.md:58` (2026-10-07) inside `flows/8f0f57/vision/skillsAsInterface.md:1` (2026-10-07)
- `flows/d4ae97/vision/skills.md:65` (2026-10-07) inside `flows/8f0f57/vision/skillsAsInterface.md:1` (2026-10-07)
- `flows/d4ae97/vision/skills.md:72` (2026-10-07) inside `flows/8f0f57/vision/skillsAsInterface.md:1` (2026-10-07)
- `flows/d4ae97/vision/skills.md:81` (2026-10-07) inside `flows/8f0f57/vision/skillsAsInterface.md:1` (2026-10-07)
- `flows/d4ae97/vision/skills.md:86` (2026-10-07) inside `flows/8f0f57/vision/visionAndTools.md:1` (2026-10-07)
- `flows/d4ae97/vision/skills.md:93` (2026-10-07) inside `flows/8f0f57/vision/visionAndTools.md:1` (2026-10-07)
- `flows/ebbe30/vision/skills.md:1` (2026-10-07) inside `flows/8f0f57/vision/skillsAsInterface.md:1` (2026-10-07)
- `flows/f5a6e9/vision/flow.md:95` (2026-10-07~) inside `flows/d4ae97/vision/flow.md:165` (2026-10-08)
- `flows/f5a6e9/vision/flow.md:143` (2026-10-07~) inside `flows/445410/vision/nexus.md:1` (2026-10-09)
- `flows/41fa34/notion/clojure-flow.md:2` (2026-10-08) inside `flows/d4ae97/vision/flow.md:153` (2026-10-08)
- `flows/41fa34/vision/clojure-flow.md:2` (2026-10-08) inside `flows/d4ae97/vision/flow.md:153` (2026-10-08)
- `flows/41fa34/vision/codex-upgrades.md:2` (2026-10-08) inside `flows/d4ae97/vision/deployment.md:3` (2026-10-08)
- `flows/41fa34/vision/compensation.md:2` (2026-10-08) inside `flows/d4ae97/vision/skills.md:102` (2026-10-08)
- `flows/f5a6e9/vision/messaging.md:3` (2026-10-08~) inside `flows/d4ae97/vision/messenger.md:11` (2026-10-08)
- `flows/0c85a3/vision/aspect-topics.md:2` (2026-10-09) inside `flows/f5a6e9/vision/flow.md:135` (2026-10-07~)
- `flows/0c85a3/vision/deployment-accounting.md:2` (2026-10-09) inside `flows/445410/vision/deployment.md:1` (2026-10-09)
- `flows/0c85a3/vision/nexus-configuration.md:2` (2026-10-09) inside `flows/445410/vision/nexus.md:1` (2026-10-09)
- `flows/445410/vision/books.md:9` (2026-10-09) inside `flows/ebbe30/vision/ethos.md:39` (2026-10-09)
- `flows/445410/vision/ethos.md:1` (2026-10-09) inside `flows/ebbe30/vision/ethos.md:39` (2026-10-09)
- `flows/445410/vision/flow.md:9` (2026-10-09) inside `flows/ebbe30/vision/metaflow-naming.md:1` (2026-10-09)
- `flows/445410/vision/flow.md:17` (2026-10-09) inside `flows/ebbe30/vision/metaflow-naming.md:1` (2026-10-09)
- `flows/73ada7/vision/nexus.md:3` (2026-10-09) inside `flows/d5df1d/vision/ethos.md:27` (2026-10-09)
- `flows/73ada7/vision/nexus.md:11` (2026-10-09) inside `flows/445410/vision/nexus.md:1` (2026-10-09)
- `flows/ebbe30/vision/clojure.md:1` (2026-10-09) inside `flows/0c85a3/notion/flow-identifiers.md:2` (2026-10-09)
- `flows/ebbe30/vision/flow-startup.md:9` (2026-10-09) inside `flows/f5a6e9/vision/vision.md:3` (2026-10-09~)
- `flows/ebbe30/vision/vision.md:27` (2026-10-09) inside `flows/f5a6e9/vision/flow.md:111` (2026-10-07~)
- `flows/f5a6e9/vision/vision.md:11` (2026-10-09~) inside `flows/ebbe30/vision/metaflow-naming.md:1` (2026-10-09)
- `flows/058f16/vision/source.md:23` (2026-10-10) inside `flows/081064/vision/ethos.md:3` (2026-10-10)
- `flows/058f16/vision/source.md:53` (2026-10-10) inside `flows/d68c82/vision/naming.md:3` (2026-10-10~)
- `flows/081064/vision/ethos.md:18` (2026-10-10) inside `flows/058f16/vision/source.md:41` (2026-10-10)
- `flows/081064/vision/ethos.md:26` (2026-10-10) inside `flows/d68c82/vision/naming.md:3` (2026-10-10~)
- `flows/081064/vision/ethos.md:72` (2026-10-10) inside `flows/9519a1/vision/distillationSources.md:1` (2026-10-10~)
- `flows/875960/vision/distillation.md:11` (2026-10-10) inside `flows/9519a1/vision/distillationSources.md:1` (2026-10-10~)
- `flows/875960/vision/persona.md:3` (2026-10-10) inside `flows/9519a1/vision/persona.md:1` (2026-10-10~)
- `flows/875960/vision/persona.md:11` (2026-10-10) inside `flows/9519a1/vision/persona.md:1` (2026-10-10~)
- `flows/875960/vision/persona.md:19` (2026-10-10) inside `flows/9519a1/vision/persona.md:1` (2026-10-10~)
- `flows/23824a/vision/typeEthos.md:3` (2026-10-10~) inside `flows/081064/vision/ethos.md:80` (2026-10-10)
- `flows/d68c82/vision/books.md:11` (2026-10-10~) inside `flows/9519a1/vision/books.md:1` (2026-10-11~)
- `flows/d68c82/vision/books.md:16` (2026-10-10~) inside `flows/9519a1/vision/books.md:1` (2026-10-11~)
- `flows/d68c82/vision/ethos.md:3` (2026-10-10~) inside `flows/081064/vision/ethos.md:3` (2026-10-10)
- `flows/d68c82/vision/ethos.md:16` (2026-10-10~) inside `flows/875960/vision/flow.md:3` (2026-10-11)
- `flows/875960/vision/books.md:3` (2026-10-11) inside `flows/9519a1/vision/books.md:1` (2026-10-11~)
- `flows/875960/vision/flow.md:11` (2026-10-11) inside `flows/9519a1/vision/flow.md:1` (2026-10-11~)
- `flows/875960/vision/flow.md:19` (2026-10-11) inside `flows/9519a1/vision/flow.md:1` (2026-10-11~)
- `flows/875960/vision/flow.md:27` (2026-10-11) inside `flows/9519a1/vision/flow.md:1` (2026-10-11~)
- `flows/875960/vision/flow.md:43` (2026-10-11) inside `flows/9519a1/vision/flow.md:1` (2026-10-11~)
- `flows/33752b/vision/books.md:3` (2026-10-12) inside `flows/d68c82/vision/books.md:30` (2026-10-12)
- `flows/33752b/vision/design.md:11` (2026-10-12) inside `flows/d68c82/vision/design.md:13` (2026-10-12)
- `flows/33752b/vision/design.md:19` (2026-10-12) inside `flows/d68c82/vision/design.md:13` (2026-10-12)
- `flows/33752b/vision/design.md:27` (2026-10-12) inside `flows/d68c82/vision/design.md:13` (2026-10-12)
- `flows/33752b/vision/questions.md:3` (2026-10-12) inside `flows/d68c82/vision/books.md:30` (2026-10-12)
- `flows/9519a1/notion/identifier.md:1` (2026-10-12~) inside `flows/875960/vision/flow.md:51` (2026-10-12)
- `flows/9519a1/vision/callerIdentity.md:1` (2026-10-12~) inside `flows/875960/vision/flow.md:51` (2026-10-12)
- `flows/9519a1/vision/nexus.md:1` (2026-10-12~) inside `flows/33752b/vision/design.md:67` (2026-10-12)
- `flows/d68c82/vision/psyche.md:23` (2026-10-13) inside `flows/d55c56/vision/relaying.md:3` (2026-10-13)
- `flows/d68c82/vision/context-modules.md:53` (2026-10-13~) inside `flows/33752b/vision/books.md:51` (2026-10-13)
- `flows/d68c82/vision/context-modules.md:65` (2026-10-13~) inside `flows/33752b/vision/books.md:51` (2026-10-13)
- `flows/d68c82/vision/context-modules.md:77` (2026-10-13~) inside `flows/da2038/vision/data.md:3` (2026-10-13)
- `flows/d68c82/vision/context-modules.md:83` (2026-10-13~) inside `flows/da2038/vision/correction.md:3` (2026-10-13)
- `flows/d68c82/vision/context-modules.md:89` (2026-10-13~) inside `flows/da2038/vision/correction.md:11` (2026-10-13)
- `flows/d68c82/vision/flow.md:50` (2026-10-13~) inside `flows/33752b/vision/flow.md:3` (2026-10-13)
- `flows/d68c82/vision/flow.md:56` (2026-10-13~) inside `flows/33752b/vision/flow.md:11` (2026-10-13)
- `flows/d68c82/vision/flow.md:64` (2026-10-13~) inside `flows/33752b/vision/flow.md:19` (2026-10-13)
- `flows/d68c82/vision/flow.md:70` (2026-10-13~) inside `flows/33752b/vision/flow.md:19` (2026-10-13)
- `flows/d68c82/vision/flow.md:76` (2026-10-13~) inside `flows/33752b/vision/flow.md:29` (2026-10-13)
- `flows/3960eb/vision/communication.md:19` (2026-10-14) inside `flows/17ac8a/vision/communication.md:34` (?~)
- `flows/3960eb/vision/communication.md:53` (2026-10-14) inside `flows/d68c82/vision/visualization.md:11` (2026-10-14)
- `flows/55a2b4/vision/flow.md:3` (2026-10-14) inside `flows/7c89aa/vision/ethos-in-clojure.md:37` (2026-10-14)
- `flows/d68c82/vision/books.md:141` (2026-10-14) inside `flows/17ac8a/vision/communication.md:52` (?~)
- `flows/d68c82/vision/ethos.md:37` (2026-10-14) inside `flows/7c89aa/vision/ethos-in-clojure.md:37` (2026-10-14)
- `flows/d68c82/vision/flow.md:130` (2026-10-14) inside `flows/7c89aa/vision/ethos-in-clojure.md:25` (2026-10-14)
- `flows/d68c82/vision/nexus.md:2` (2026-10-14) inside `flows/7c89aa/vision/ethos-in-clojure.md:37` (2026-10-14)
- `flows/d68c82/vision/seats.md:29` (2026-10-14) inside `flows/7c89aa/vision/ethos-in-clojure.md:37` (2026-10-14)
- `flows/d68c82/vision/visualization.md:3` (2026-10-14) inside `flows/7c89aa/vision/books.md:3` (2026-10-14)
- `flows/da2038/vision/books.md:2` (2026-10-14) inside `flows/7c89aa/vision/books.md:3` (2026-10-14)
- `flows/da2038/vision/books.md:12` (2026-10-14) inside `flows/17ac8a/vision/communication.md:34` (?~)
- `flows/da2038/vision/flow.md:26` (2026-10-14) inside `flows/7c89aa/vision/ethos-in-clojure.md:25` (2026-10-14)
- `flows/da2038/vision/subflows.md:2` (2026-10-14) inside `flows/d68c82/vision/context-modules.md:142` (2026-10-14)
- `flows/da2038/vision/subflows.md:12` (2026-10-14) inside `flows/d68c82/vision/context-modules.md:142` (2026-10-14)
- `flows/da2038/vision/usage.md:2` (2026-10-14) inside `flows/d68c82/vision/seats.md:37` (2026-10-14)
- `flows/e4b7d7/vision/designer.md:1` (?~) inside `flows/d68c82/vision/ethos.md:47` (2026-10-14)

## 4. Long term and short term

Rule from the living (flows/d55c56/vision/makeshift.md, 2026-10-13): the vision is short-term (for now, the makeshift) or long-term (the goalpost); an unmarked vision is long-term; when the long-term is implemented and documented, the short-term goes. The living's 2026-10-14 order (flows/da2038/vision/psyche.md:2): push the more advanced material to explicit long-term, and name the makeshift: Clojure, Malli, EDN.

### 4a. Records that already say short-term, long-term or makeshift (34 unique records)

- **flow** (14): `flows/d4ae97/vision/flow.md:62` 2026-10-07 A flow is not always a metaflow; `flows/33752b/vision/flow.md:3` 2026-10-13 A guarded compaction request on the short-term F; `flows/33752b/vision/flow.md:29` 2026-10-13 "Meta socket" in the short-term proposal is not ; `flows/d68c82/vision/flow.md:8` 2026-10-13 Flow starting configured in EDN, per aspect and ; `flows/d68c82/vision/flow.md:14` 2026-10-13 Clean specialized flows for quality; `flows/d68c82/vision/flow.md:50` 2026-10-13~ A compaction request refuses a small or young fl; `flows/d68c82/vision/flow.md:76` 2026-10-13~ The short term and the long term are not mixed; `flows/d68c82/vision/flow.md:82` 2026-10-13~ Short-term prototypes are written in Clojure; `flows/d68c82/vision/flow.md:114` 2026-10-14 2026-10-14 — refresh thresholds, idle harnesses,; `flows/d68c82/vision/flow.md:130` 2026-10-14 2026-10-14 — A full Flow Nexus proposal, short-t; `flows/d68c82/vision/flow.md:148` 2026-10-14 2026-10-14 — No Primary without a Secondary; que; `flows/da2038/vision/flow.md:18` 2026-10-14 A needed flow is started, running or not; `flows/da2038/vision/flow.md:26` 2026-10-14 A full Flow Nexus proposal: short-term, and long; `flows/da2038/vision/flow.md:44` 2026-10-14 Vertical communication is not strictly short-ter
- **psyche** (4): `flows/fd0f97/vision/psyche.md:3` 2026-09-15~ Each Flow's own transcripts are its record; a Ps; `flows/183ae0/notion/psyche.md:3` 2026-09-29~ Psyche injected along with a message; `flows/d68c82/vision/psyche.md:8` 2026-10-13 The envisioned and the makeshift; `flows/da2038/vision/psyche.md:2` 2026-10-14 Mass-delete overruled raw psyche; long term made
- **ethos** (2): `flows/aa4c7747/vision/archive-ethos.md:3` 2026-08-24 2026-08-24 — the biggest short-term gain: mental; `flows/d68c82/vision/ethos.md:29` 2026-10-14 2026-10-14 — Ethos/datom-to-Clojure prototyping,
- **communication** (2): `flows/fe945a/vision/communication.md:3` 2026-09-29 Field asks Mind, Mind asks Psyche, Psyche makes ; `flows/3960eb/vision/communication.md:11` 2026-10-14 No speech in the book now; real-time speech is l
- **makeshift** (2): `flows/d55c56/vision/makeshift.md:3` 2026-10-13 2026-10-13 — the goalpost and the makeshift; `flows/d55c56/vision/makeshift.md:21` 2026-10-13 2026-10-13 — short-term vision and long-term vis
- **rustComponentArchitecture** (1): `flows/55d18f4f/vision/archive-rustComponentArchitecture.md:3` 2026-08-08 2026-08-08T11:28:10.420Z — all the components ha
- **shortTermFixNotTheFullJob** (1): `flows/7b4d4c/vision/shortTermFixNotTheFullJob.md:1` 2026-09-05~ A short-term fix, not the full job
- **prometheus-networking** (1): `flows/6fe957/vision/prometheus-networking.md:2` 2026-09-26 2026-09-26 — Prometheus AP/cable and transfer di
- **skills** (1): `flows/8904b1/vision/skills.md:108` 2026-09-28 8904b1-31 — 2026-09-28, the living, typed as com
- **prometheus-wifi** (1): `flows/19ff9f/vision/prometheus-wifi.md:1` 2026-10-01~ Prometheus Wi-Fi access point reliability
- **persona** (1): `flows/05c604/vision/archive-persona.md:3` 2026-10-10~ By default Persona manages all the clusters and
- **deployment** (1): `flows/d68c82/vision/deployment.md:29` 2026-10-13 The meta-flow identifier everywhere; declarative
- **prototypes** (1): `flows/da2038/vision/prototypes.md:3` 2026-10-13 Short-term prototypes are written in Clojure
- **ethos-in-clojure** (1): `flows/7c89aa/vision/ethos-in-clojure.md:25` 2026-10-14 A full Flow Nexus proposal, short-term and long-
- **context-modules** (1): `flows/d68c82/vision/context-modules.md:119` 2026-10-14 2026-10-14 — a proposal checks the higher module

### 4b. Records that name Clojure, Malli, EDN or Babashka: the makeshift prototype stack (59 unique records, 23 flows)

Explicit rulings among them: flows/d68c82/vision/flow.md:82 and flows/da2038/vision/prototypes.md:3 (2026-10-13, short-term prototypes are written in Clojure), flows/e51411/notion/stack.md:23 (2026-09-25, the Clojure messenger is a proof of concept on EDN emulating Ethos, no porting), flows/d4ae97/vision/tools.md:20 (2026-10-08, Babashka first), flows/d68c82/vision/flow.md:8 (2026-10-13, flows configured in EDN). Malli appears only in flows/e51411/vision/launch.md:77 and the landed vision-clojure skill. All of the rest are candidates to mark short-term. Statements that the Clojure tool shows datom is better than escaped strings (b860be datomSyntax:3, e167d8 psycheMessages:13, f5a74e datom-messaging:2) are long-term datom vision that cites the prototype; keep those as long-term.

- `flows/995a164e/vision/data.md:12` 2026-09-01~ The Spirit suggestion is to be very broad; the clojure/lisp crowd got it a bit better than
- `flows/df159a/vision/books.md:23` 2026-09-25 On «His words, 2026-09-25, flows/88475f/...» in the Clojure-migration book
- `flows/e51411/notion/message.md:20` 2026-09-25 Three tags in a row
- `flows/e51411/notion/stack.md:3` 2026-09-25 Typed Clojure as a fallback script layer; Datom as an evolved EDN
- `flows/e51411/notion/stack.md:11` 2026-09-25 Lisp's homoiconicity may suit AI; Ethos and Protos are close to it; synergy in keeping mod
- `flows/e51411/notion/stack.md:17` 2026-09-25 A Clojure HM could use the Datomic syntax and libraries for our messaging
- `flows/e51411/notion/stack.md:23` 2026-09-25 Correction: the Clojure HM is a proof of concept on EDN and the Datomic libraries, emulati
- `flows/e51411/notion/stack.md:35` 2026-09-25 Subflows started by Flow, with their own system prompt, in place of the harness's subagent
- `flows/e51411/vision/flowAspect.md:2` 2026-09-25 Specialized flows
- `flows/e51411/vision/flowAspect.md:14` 2026-09-25 Every aspect's models have their own specialized roles
- `flows/e51411/vision/launch.md:77` 2026-09-25 HackingMessenger in Clojure: an object-oriented version of our Rust approach, typed with M
- `flows/e51411/vision/messaging.md:23` 2026-09-25 The Clojure HM makes machine messages real EDN, actually processed; the living's input sta
- `flows/e51411/vision/messaging.md:85` 2026-09-25 Messenger, not Message
- `flows/e51411/vision/speech.md:11` 2026-09-25 "Clojure" comes through as "closure" or "enclosure"
- `flows/e51411/vision/stack.md:2` 2026-09-25 Hacky Field, and Clojure as the prototyping language
- `flows/e51411/vision/stack.md:10` 2026-09-25 The -clj tools
- `flows/88475f/vision/cljTools.md:1` 2026-09-25~ Just CLJ, as a suffix: simple standalone CLIs
- `flows/88475f/vision/cljTools.md:9` 2026-09-25~ Clojure prototypes, then Ethos and Rust
- `flows/88475f/vision/speechToText.md:9` 2026-09-25~ "In closure" means "in Clojure"
- `flows/93ba9f/vision/datomVocabulary.md:1` 2026-09-26 Datom vocabulary
- `flows/b7da5d/vision/datomMessaging.md:15` 2026-09-26 Correct word
- `flows/b860be/vision/datomSyntax.md:3` 2026-09-26 Superior to escaped strings, seen in the Clojure messaging tool
- `flows/e167d8/vision/landing.md:3` 2026-09-26 The Clojure tool's database holds the landing lock
- `flows/e167d8/vision/psycheMessages.md:13` 2026-09-26 Datom syntax is superior for messaging (seen in the Clojure tool's escapes)
- `flows/f5a74e/vision/datom-messaging.md:2` 2026-09-26 2026-09-26 — Datom syntax and Clojure messaging
- `flows/8904b1/vision/presentation.md:3` 2026-09-28 8904b1-27 — 2026-09-28, the living, direct to this pane
- `flows/6f51ad/notion/clojure.md:3` 2026-09-29 2026-09-29 — bootstrap its tooling in Clojure
- `flows/c64ee3/vision/flowNexus.md:3` 2026-09-29 c64ee3-11 — proper messages and proper flow creation, controlled by a flow nexus
- `flows/183ae0/vision/skills.md:41` 2026-09-29~ Three skill repos, and log repos beside them
- `flows/e71dab/vision/midLayerReview.md:16` 2026-10-01~ Datom and Clojure in the messaging tool
- `flows/d4ae97/vision/books.md:88` 2026-10-07 Code extracted from Markdown books into its targets
- `flows/41fa34/vision/clojure-builds.md:2` 2026-10-08 mkCljUberjar
- `flows/41fa34/vision/clojure-flow.md:2` 2026-10-08 Clojure flow prototype
- `flows/41fa34/vision/ethos-json.md:10` 2026-10-08 JSON and Datom both ways
- `flows/41fa34/vision/topics.md:2` 2026-10-08 Registry of the topics
- `flows/d4ae97/vision/datom.md:33` 2026-10-08 A checked bridge between JSON and datom, adaptable to other formats
- `flows/d4ae97/vision/flow.md:153` 2026-10-08 A Clojure Flow prototype, with its own database, addressed by metaflow name, specified in
- `flows/d4ae97/vision/tools.md:8` 2026-10-08 The framework: correct, expressive, homoiconic, data-centred
- `flows/d4ae97/vision/tools.md:20` 2026-10-08 The Clojure stack is vision: Babashka first, a Nix-built image when deployed
- `flows/d4ae97/vision/tools.md:35` 2026-10-08 Clojure builds under Nix; Ethos to JSON; the mind keeps a registry of topics
- `flows/0c85a3/notion/flow-identifiers.md:2` 2026-10-09 Word-based flow ID — 2026-10-09
- `flows/ebbe30/vision/clojure.md:1` 2026-10-09 Clojure developed data-oriented, as ethos is; an ethos anatomy comes first
- `flows/ebbe30/vision/metaflow-naming.md:1` 2026-10-09 Topic flows: psyche::{topic}, the layer, then the word-based flow id
- `flows/33752b/vision/flow.md:29` 2026-10-13 "Meta socket" in the short-term proposal is not understood; the short-term solution is not
- `flows/d68c82/vision/flow.md:8` 2026-10-13 Flow starting configured in EDN, per aspect and per metaflow
- `flows/da2038/vision/prototypes.md:3` 2026-10-13 Short-term prototypes are written in Clojure
- `flows/d68c82/vision/flow.md:76` 2026-10-13~ The short term and the long term are not mixed
- `flows/d68c82/vision/flow.md:82` 2026-10-13~ Short-term prototypes are written in Clojure
- `flows/17ac8a/vision/communication.md:63` 2026-10-14 The references blocks in the Flow Clojure book are approved
- `flows/7c89aa/vision/ethos-in-clojure.md:3` 2026-10-14 A standard translation from ethos and datom to Clojure and EDN (2026-10-14)
- `flows/7c89aa/vision/ethos-in-clojure.md:17` 2026-10-14 Side question: objects with methods in Clojure (2026-10-14)
- `flows/7c89aa/vision/ethos-in-clojure.md:25` 2026-10-14 A full Flow Nexus proposal, short-term and long-term/universal; a Clojure topic (2026-10-1
- `flows/7c89aa/vision/ethos-in-clojure.md:37` 2026-10-14 The Clojure translation lands; fleshed out with the flow graph, examples, a knowledge skil
- `flows/d68c82/vision/ethos.md:29` 2026-10-14 2026-10-14 — Ethos/datom-to-Clojure prototyping, a Mind Clojure topic
- `flows/d68c82/vision/ethos.md:37` 2026-10-14 2026-10-14 — The Clojure translation, fleshed out
- `flows/d68c82/vision/flow.md:114` 2026-10-14 2026-10-14 — refresh thresholds, idle harnesses, and handover at cache expiry
- `flows/d68c82/vision/tools.md:8` 2026-10-14 2026-10-14 — tools live in their own repositories
- `flows/d68c82/vision/tools.md:14` 2026-10-14 2026-10-14 — a repeated use case grows an existing tool; EDN in Clojure, datom in Nexus
- `flows/da2038/vision/psyche.md:2` 2026-10-14 Mass-delete overruled raw psyche; long term made explicit; makeshift is Clojure, Malli, ED

### 4c. Records that name Ethos or Rust: the long-term implementation language (424 unique records)

Ethos is the authored language and Rust is generated from it; the Clojure stack above is a prototype derived from Ethos (flows/da2038/vision/flow.md:26, 2026-10-14). By subject: ethos 80, kinds 23, datom 14, flow 13, threeStacks 10, nexus 10, designPractice 8, skills 8, books 8, rustComponentArchitecture 5, ethosFileAnatomy 5, protos 5, meaningLanguage 5, vision 5, datomSyntax 4, traitsAsCapabilities 4, signalIsOurMessagingLayer 4, mainFunction 4, negatives 4, layerMatching 4, ethosTypes 4, identifiers 4, transcriptNexus 4, stack 4, ethos-in-clojure 4. None of these needs a separate mark unless it describes how things work today; those that do describe today's makeshift are in 4a.

### 4d. Advanced machinery with no short-term or long-term marker: candidates to mark long-term

Records matching a theme and carrying none of the words short-term, long-term, makeshift, goalpost, prototype, proof of concept or for now. Counts are of unique records; sample refs are the three earliest. The match is keyword-based (the flow's inference); each theme needs the living's read before any mark.

- **Models trained on binary signal; Datom as the language models speak**: 3 records, 3 flows, 2026-09-04 to 2026-09-28. Examples: `flows/04db2fd2/vision/archive-textualTypes.md:11` The type is a prospective datom [STT: datum]; the ; `flows/b7ba00/vision/meaningLanguage.md:39` The meaning language in Datom across all layers; P; `flows/8904b1/vision/anatomy.md:15` 8904b1-6 — 2026-09-28, the living, direct to this
- **Meaning language: Pāṇini, Sanskrit, ontology, content-addressed links, linked-data garbage collection**: 48 records, 27 flows, 2026-08-14 to 2026-10-07. Examples: `vision-raw/archive-rustComponentArchitecture.md:3` 2026-08-14 — reconsider everything; keep the Signa; `flows/2b34fafa/vision/protosIsTheSharedStyle.md:1` 2026-08-18 — define the block: start with the text; `flows/2b34fafa/vision/rustComponentArchitecture.md:23` 2026-08-18 — mechanical tests will not create good
- **Typed storage, typed strings and structured enum logs**: 3 records, 2 flows, 2026-09-17 to 2026-10-01. Examples: `flows/b7ba00/vision/meaningLanguage.md:101` Meaning as the successor of the string: variants a; `flows/b7ba00/vision/meaningLanguage.md:155` Sema's first version: one or two layers of variant; `flows/840e42/vision/logging.md:3` A simple enum-based log with no string payload: in
- **Topics that go idle and are woken by a judgment call; system-1 models; queuing**: 6 records, 4 flows, 2026-09-30 to 2026-10-14. Examples: `flows/7328f4/vision/hooks.md:11` Seats move to a new harness by hooks, one at a tim; `flows/b666e7/vision/hook.md:10` Full page comment recovered; `flows/d4ae97/vision/ethos.md:135` Ethos is designed with the datom payload's cost in
- **Event hooks instead of polling, a registry of polling systems**: 8 records, 7 flows, 2026-08-27 to 2026-10-03. Examples: `flows/acbb6006/vision/archive-nexus.md:51` Polling is forbidden; a correct system goes quiet ; `flows/108ab0/vision/operational-pushMessagingForEmergency.md:3` We need the push server style for time-type system; `flows/7328f4/vision/polling.md:3` Flow state through hooks, as cheaply as possible,
- **Unity, Mentci, tailnet mesh and phone clients**: 32 records, 15 flows, 2026-08-13 to 2026-10-01. Examples: `vision-raw/mentci.md:3` 2026-08-13 — the daemon is the central logic; fron; `vision-raw/mentci-egui.md:3` 2026-08-19T15:06:42+02:00 — Remove Mentci-egui fro; `flows/6cc91b/vision/network.md:3` 2026-09-13 — Tailnet identity-based network, IPv6
- **Open-source models, private layer, local model hosting**: 22 records, 13 flows, 2026-08-29 to 2026-10-04. Examples: `flows/01a04e75/notion/continuousRecordingUsingWisprFlowChunks.md:3` Natural pauses and overlapping chunks; `flows/024bc7/vision/parallelSessions.md:13` 2026-09-13 — A paired flow between Claude and Code; `flows/024bc7/vision/soul.md:3` 2026-09-13 — The private layer, the soul, the priv
- **Criome identity, authenticated updates, own sandbox and security**: 19 records, 12 flows, 2026-08-22 to 2026-10-09. Examples: `flows/01a02b46/vision/zeusUpdate.md:88` 2026-08-22T21:27:17.954Z — use the hostname for ac; `flows/024bc7/vision/context.md:3` 2026-09-13 — My words go in the middle layer; the ; `flows/024bc7/vision/criome.md:3` 2026-09-13 — Criome takes over the authentication
- **Nexus component architecture (Signal, Sema, CLI and daemon sockets)**: 258 records, 91 flows, 2026-08-08 to 2026-10-14. Examples: `flows/55d18f4f/vision/everythingIsInTheDaemon.md:1` 2026-08-08T11:12:45.472Z — "Everything is in the d; `flows/55d18f4f/vision/archive-signalIsOurMessagingLayer.md:1` 2026-08-08T11:45:33.818Z — Signal is our messaging; `flows/019feb93/vision/threeStacks.md:1` 2026-08-10 — completion output of the incorrect ne

## 5. Crystallization candidates: many consistent records, no contradiction found

Counts are of unique records (copies not counted). 'Landed' names the psyche-context skill that already carries the idea. None of these subjects appears in section 2 as rolled back, except where noted.

| records | line to crystallize | backing | landed or not |
|---|---|---|---|
| 106 | The book is the only way the living is spoken to; it holds proposals only, visual first with minimal text, no restated words of his, code shown as the proposed landing in green, nothing read twice, a first edition mostly questions | 106 records in topic files books.md and communication.md, 27 flows, 2026-09-25 to 2026-10-14 | Landed: vision-book (18 lines: red/green, figures, no verbatim quote, references file, first edition, center of development). Not landed: the book as sole channel, visual-first, nothing read twice, code as the proposal, 'a new edition shows only what is open'. Excluded as rolled back: swipe pages, buttons, Sonnet comments, illustration machinery (S3). |
| 60 | The metaflow: a long-lived addressable topic over a succession of flows, named aspect, topic and layer, with the core topic permanent, topics going idle and woken by judgment | 60 records from 2026-10-01 naming metaflow, 17 flows, 2026-10-04 to 2026-10-14 | Landed: vision-flow (88 lines) and vision-model-roles. The voice and seat records before 2026-10-11 are S1 and excluded. |
| 59 | The short-term prototype stack: Clojure under Babashka, Malli types, EDN data, translated from Ethos and Datom, tools in their own repositories, each tool a standalone CLI | 59 records naming Clojure/Malli/EDN, 23 flows, 2026-09-01 to 2026-10-14 | Landed: vision-clojure (8 lines, the translation). Not landed: that prototypes are Clojure (.clj, not .mjs), Babashka first, EDN flow configuration, tools as -clj standalone CLIs, the Clojure tool being a proof of concept with no porting. |
| 16 | Words, not hashes, address a flow: the word id converts back to the harness hash, one generic word-id library, hashes are shortened or absent in prompts and messages | 16 records, 13 flows, 2026-09-15 to 2026-10-10; refs: `flows/05c604/vision/identifiers.md:11`, `flows/692df8/vision/identifiers.md:15`, `flows/41fa34/vision/identifiers.md:2`, `flows/dea0ba/vision/identifiers.md:2`, `flows/5578cc/vision/identifiers.md:11`, `flows/5578cc/vision/identifiers.md:19`, `flows/9fb0ad/vision/ethosLibrary.md:9`, `flows/9fb0ad/vision/identifiers.md:37`, `flows/b7ba00/vision/wordIds.md:3`, `flows/fe945a/vision/hashes.md:3`, `flows/4ddfe1/vision/flow-names.md:3`, `flows/01e496/vision/flowIdentity.md:3`, `flows/01e496/vision/flowNexus.md:3`, `flows/d8df70/vision/messaging.md:72`, `flows/e51411/vision/launch.md:27`, `flows/058f16/vision/identifier.md:3` | Landed: vision-flow line 22 says the flow id is the hash of the harness session id; no psyche-context skill I grepped (vision-flow, vision-messaging, vision-model-roles) names word ids. Variance: PascalCase (b7ba00) against camelCase (05c604, 058f16) for the word casing; ask. |
| 16 | Flow state and events come from harness hooks; nothing polls; a registry lists any polling system; hooks add to a message as it arrives | 16 records, 5 flows, 2026-09-29 to 2026-10-01 (three days) | Landed: nothing named in vision-flow headings. Narrow date span; the living's 2026-10-14 comment 'Flow decides where hooks talk' (flows/da2038/vision/flow.md) refines it. |
| 12 | A test checks behaviour: it does not bring its own data to test against production, does not search text of code or skills, and does not pin prose; the testing line was approved and landed in August | 12 records, 8 flows, 2026-08-10 to 2026-10-07; refs: `flows/98fbfa47/vision/testTravesties.md:1`, `flows/13cfc23f/vision/testTravesties.md:1`, `flows/7c3f0c1d/vision/testTravesties.md:1`, `flows/e06e4c07/vision/testTravesties.md:1`, `flows/e06e4c07/vision/testTravesties.md:16`, `flows/e06e4c07/vision/testTravesties.md:26`, `flows/e06e4c07/vision/testTravesties.md:43`, `flows/e06e4c07/vision/testTravesties.md:56`, `vision-raw/testTravesties.md:3`, `flows/01a01bac/vision/testTravesties.md:3`, `flows/d4ae97/vision/testing.md:3`, `flows/840e42/vision/testing.md:3` | Landed: not found. intent-testing (read, 10 lines) is about sandboxing a proof of concept, not test quality; its dependency compensation-testing is a machine skill I did not read. |
| 12 | Ethos type discipline: everything is a type, no key-value, structs over chained variants, a one-position type is a new type and not an alias, inline declaration unless too deep, traits only where load-bearing, variants ordered by seniority | 12 records, 6 flows, 2026-09-08 to 2026-10-09; refs: `flows/aa887c/vision/ethos.md:3`, `flows/91ea9f/vision/ethos.md:9`, `flows/d4ae97/vision/ethos.md:27`, `flows/d4ae97/vision/ethos.md:37`, `flows/d4ae97/vision/ethos.md:45`, `flows/d4ae97/vision/ethos.md:79`, `flows/d4ae97/vision/ethos.md:86`, `flows/d4ae97/vision/ethos.md:115`, `flows/d4ae97/vision/ethos.md:125`, `flows/ebbe30/vision/ethos.md:39`, `flows/8e9e77/vision/single-field-structs.md:9`, `flows/b7ba00/vision/types.md:3` | Landed: vision-datom (318 lines) and a vision-ethos skill reached through the base prompt; I did not read vision-ethos. The kind-to-trait rename (S) is excluded. d4ae97 ethos:125 is itself a speech-to-text correction. |
| 11 | A message carries a tag, the sender, and the text: no hashes, timestamps, repeated or empty fields, no size limit, no message id | 11 records, 6 flows, 2026-09-24 to 2026-10-03; refs: `flows/d8df70/vision/messaging.md:72`, `flows/e51411/vision/messaging.md:51`, `flows/e51411/vision/messaging.md:63`, `flows/e51411/vision/messaging.md:71`, `flows/88475f/vision/message.md:1`, `flows/88475f/vision/message.md:33`, `flows/5578cc/vision/messaging.md:3`, `flows/fe945a/vision/hashes.md:3`, `flows/b7ba00/vision/messaging.md:3`, `flows/b7ba00/vision/messaging.md:25`, `flows/e51411/vision/launch.md:27` | Landed: vision-messaging 'Only messages that act, deliver, or block' and the datom body. Not landed: the fields rule. Tension: the Datom-enforcement line (unclear list, section 2). |

Backing that is wide but not cross-flow, so held back: context-modules.md (22 records, 1 flow, d68c82, 2026-10-13/14); flashbooks/presentation (rolled back, S3); skillDesigning (39 records 2026-08-14 to 09-02, written for the skill system that S2 retires).

## Deletion arithmetic (from this inventory, before any ruling)

- Redundant copies: 360 exact plus 259 contained = 619 records (some overlap), none losing a word if the keep rows in section 3 stay.
- Earlier records named in section 2 groups: 79 (of which in `archive-*` files: 23). Whole archive files that section 2 says are superseded: archive-kinds (all 52 records), archive-datomSyntax, archive-protos, archive-threeStacks, archive-traitsAsCapabilities, archive-datomMaps.
- Total archive-file records: 447 of 3729; the living said crystallized originals keep every original word, so removing them is a separate ruling.
