# Sources rewrite: psyche-skills

Repository `git@github.com:LiGoldragon/psyche-skills.git`, rewritten 2026-10-11 for flow d68c82.

- Old main: `f776683bdf8b78e996151e6023ae7ddd5eff3a7c`
- Backup branch: `backup/pre-sources-rewrite-20261011` at the old main
- New main and `sources-in-commits`: `d0d194c8d1bef78874c8aad842d70047978c4bac`
- Commits rewritten: 19 of 19 (linear history, no merges); messages extended: 4; reference lines moved: 243

## Rule applied

Every `## Sources` section (heading to end of file; it is the last section in every file at every commit) is removed together with the blank lines before it. Each commit whose Sources sections gained lines over its parent (renames followed with `diff-tree -M`) gets those lines inserted into its message before the trailer paragraph, grouped under the file path when more than one file contributes. A whole newly introduced section is moved as written, prose paragraphs included; `flows/445410/vision/books.md, 2026-10-09` is normalized to `445410 books`. Lines a message already carried are not added again. Authors, committers, dates and parents are kept; every new commit is signed with the configured key (`%G?` = G).

## Diff proof

`verify.py` checked every old/new pair: identical path sets and modes; each new blob equals the old blob with its Sources section stripped by the same function; no Sources section left in any new tree; `git diff --unified=0 old new` has no added line; every old message line survives in the new message; author, committer, dates and mapped parents equal. Result: OK.

| old | new | blobs changed | lines removed | message lines added |
|---|---|---|---|---|
| 9cd7d98 | 76d28f1 | 0 | 0 | 0 |
| fef9864 | 72149ef | 27 | 318 | 291 |
| 4312cc0 | a33ac94 | 27 | 318 | 0 |
| 6714d95 | ca88769 | 28 | 322 | 2 |
| f9d74b9 | be95bb6 | 28 | 322 | 0 |
| 5c19220 | 525d620 | 28 | 322 | 0 |
| 9407b7e | 2b6be03 | 28 | 322 | 0 |
| c3f8eeb | d867ed1 | 29 | 327 | 3 |
| 71e9e4d | 0ab729b | 29 | 327 | 0 |
| 850fd27 | b95e977 | 29 | 327 | 0 |
| 9fb0433 | 97874fb | 29 | 328 | 2 |
| 7a6b130 | 2956ee6 | 30 | 334 | 0 |
| 82c92fa | 69d7424 | 29 | 328 | 0 |
| 4014086 | 01937a4 | 29 | 328 | 0 |
| 19f7f0e | 988800b | 29 | 328 | 0 |
| 6261fb6 | 8df833f | 29 | 328 | 0 |
| 63a71c6 | f35c83a | 29 | 328 | 0 |
| 925cf59 | ae0bc79 | 29 | 328 | 0 |
| f776683 | d0d194c | 29 | 328 | 0 |

## No-loss map

Each reference line, the old commit that introduced it, and the new commit whose message carries it. All 243 found.

| file | reference | as in message | old | new |
|---|---|---|---|---|
| skills/intent-anatomy.md | 1a6ca4 datom | same | fef9864 | 72149ef |
| skills/intent-context.md | 564f55 datom | same | fef9864 | 72149ef |
| skills/intent-context.md | 564f55 protos | same | fef9864 | 72149ef |
| skills/intent-conversion.md | 564f55 protos | same | fef9864 | 72149ef |
| skills/intent-conversion.md | 564f55 datom | same | fef9864 | 72149ef |
| skills/intent-data.md | Provenance: wording flow-drafted from the psyche's typed words | same | fef9864 | 72149ef |
| skills/intent-data.md | (flows/995a164e/vision/data.md: "everything is data. … Code is | same | fef9864 | 72149ef |
| skills/intent-data.md | data. a type is declared with code, so a type is data. a trait is | same | fef9864 | 72149ef |
| skills/intent-data.md | data. an impl is data. *everything* is data, but protolanguages | same | fef9864 | 72149ef |
| skills/intent-data.md | make it more obvious."), broadened on the psyche's direction after | same | fef9864 | 72149ef |
| skills/intent-data.md | research of the code-as-data lane (flow 995a164e, 2026-09-01). | same | fef9864 | 72149ef |
| skills/intent-data.md | Proposed as Spirit; redirected and approved as Intent by the | same | fef9864 | 72149ef |
| skills/intent-data.md | psyche 2026-09-02 ("make that intent, not spirit", the proposed | same | fef9864 | 72149ef |
| skills/intent-data.md | wording quoted back verbatim, flow 995a164e). Earlier raw record: | same | fef9864 | 72149ef |
| skills/intent-data.md | flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md. | same | fef9864 | 72149ef |
| skills/intent-models.md | 1ac573 operational-effortIsAlwaysMedium | same | fef9864 | 72149ef |
| skills/intent-models.md | 024bc7 effort | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | Provenance: wording Designer-drafted through the two-way | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | structural transcoding flesh-out | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | (design/ProtosEngine/twoWayStructuralTranscoding-2026-08-11.md); | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | approved as Intent by the psyche 2026-08-13T00:19+02:00 ("the | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | intent is good", Designer session a5587095). The ruling trail — | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | context-switching parse, the stack keeping the parent's position, | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | a child context taking the shapes' meaning — is in | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | psyche/Vision/protosIsTheSharedStyle.md. | same | fef9864 | 72149ef |
| skills/intent-protos-parsing.md | *(2026-08-14 annotation, consistency audit: "two-way structural transcoding" in this provenance paragraph is dead vocabulary — code/encoded was dropped 2026-08-13 per encodedFormIsTheCode.md 2026-08-13; the two-way walk concept stands under the real/signal/textual forms frame. The Intent body itself is unaffected.)* | same | fef9864 | 72149ef |
| skills/intent-psyche-interaction.md | e51411 mainFlow | same | fef9864 | 72149ef |
| skills/intent-startup-prompt.md | 752e0f firstPrompt | same | fef9864 | 72149ef |
| skills/intent-testing.md | f38926 operational-openCodeRemoteAccess | same | fef9864 | 72149ef |
| skills/intent-testing.md | f38926 horizon | same | fef9864 | 72149ef |
| skills/vision-archive-ethos-monolith.md | vision-raw threeStacks | same | fef9864 | 72149ef |
| skills/vision-archive-ethos-monolith.md | vision-raw rustComponentArchitecture | same | fef9864 | 72149ef |
| skills/vision-archive-ethos-monolith.md | aa4c7747 ethosMonolith | same | fef9864 | 72149ef |
| skills/vision-committing.md | f38926 committing | same | fef9864 | 72149ef |
| skills/vision-committing.md | b81560 operational-explicitFilePathCommits | same | fef9864 | 72149ef |
| skills/vision-datom.md | ac1e9ec8 datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | ac1e9ec8 datomIsData | same | fef9864 | 72149ef |
| skills/vision-datom.md | 01a03eda datomInteger | same | fef9864 | 72149ef |
| skills/vision-datom.md | 04db2fd2 datomMaps | same | fef9864 | 72149ef |
| skills/vision-datom.md | 04db2fd2 datomNexus | same | fef9864 | 72149ef |
| skills/vision-datom.md | 04db2fd2 text | same | fef9864 | 72149ef |
| skills/vision-datom.md | 04db2fd2 textualTypes | same | fef9864 | 72149ef |
| skills/vision-datom.md | 04db2fd2 anatomy | same | fef9864 | 72149ef |
| skills/vision-datom.md | 04db2fd2 portion | same | fef9864 | 72149ef |
| skills/vision-datom.md | 04db2fd2 directionAsymmetry | same | fef9864 | 72149ef |
| skills/vision-datom.md | e8c4cc61 datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | e8c4cc61 datomizable | same | fef9864 | 72149ef |
| skills/vision-datom.md | e8c4cc61 protos | same | fef9864 | 72149ef |
| skills/vision-datom.md | 62022e8f datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | 62022e8f kinds | same | fef9864 | 72149ef |
| skills/vision-datom.md | 62022e8f symbols | same | fef9864 | 72149ef |
| skills/vision-datom.md | 62022e8f headedAndContained | same | fef9864 | 72149ef |
| skills/vision-datom.md | 995a164e datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | 01a04339 datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | 01a035d3 rustCodeFromTheData | same | fef9864 | 72149ef |
| skills/vision-datom.md | 01a03d6e dotosFiles | same | fef9864 | 72149ef |
| skills/vision-datom.md | 01a03d6e ethosInterfaces | same | fef9864 | 72149ef |
| skills/vision-datom.md | a5587095 structuredStringType | same | fef9864 | 72149ef |
| skills/vision-datom.md | 5abf3be8 colonLegalInStringPosition | same | fef9864 | 72149ef |
| skills/vision-datom.md | 06196cc7 datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | b675f3d9 structuralParsing | same | fef9864 | 72149ef |
| skills/vision-datom.md | 4decf7 datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | e4a40e datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | e4a40e vocabulary | same | fef9864 | 72149ef |
| skills/vision-datom.md | e4a40e newtypeWrappingAndSingleFieldStructs | same | fef9864 | 72149ef |
| skills/vision-datom.md | 06196cc7 encodedFormIsTheCode | same | fef9864 | 72149ef |
| skills/vision-datom.md | a5587095 datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | a5587095 threeStacks | same | fef9864 | 72149ef |
| skills/vision-datom.md | a5587095 colonFormTransformerSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | a5587095 protosIsTheSharedStyle | same | fef9864 | 72149ef |
| skills/vision-datom.md | 01a03eda datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | vision-raw datomSyntax | same | fef9864 | 72149ef |
| skills/vision-datom.md | ad19b1 meaning | same | fef9864 | 72149ef |
| skills/vision-datom.md | ad19b1 datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | ad19b1 protos | same | fef9864 | 72149ef |
| skills/vision-datom.md | e996e8 datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | 564f55 datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | 564f55 protos | same | fef9864 | 72149ef |
| skills/vision-datom.md | 4d5fc7da datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | 1a6ca4 datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | fe34eb datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | 542442 datom | same | fef9864 | 72149ef |
| skills/vision-datom.md | f38926 meaningLanguage | same | fef9864 | 72149ef |
| skills/vision-deployment.md | f38926 operational-openCodeRemoteAccess | same | fef9864 | 72149ef |
| skills/vision-deployment.md | b81560 operational-pocSandboxVmFirst | same | fef9864 | 72149ef |
| skills/vision-deployment.md | b81560 operational-pocSandboxIntent | same | fef9864 | 72149ef |
| skills/vision-distillation.md | b675f3d9 visionImpurities | same | fef9864 | 72149ef |
| skills/vision-distillation.md | acbb6006 distillation | same | fef9864 | 72149ef |
| skills/vision-distillation.md | b675f3d9 distillation | same | fef9864 | 72149ef |
| skills/vision-distillation.md | ac1e9ec8 distillationNegatives | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 01a02a34 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 01a02a34 schemaSyntax | same | fef9864 | 72149ef |
| skills/vision-ethos.md | vision-raw ethosDotosDivisionAndHelp | same | fef9864 | 72149ef |
| skills/vision-ethos.md | vision-raw ethosNonRepetitionLaw | same | fef9864 | 72149ef |
| skills/vision-ethos.md | f426777b spokenVocabulary | same | fef9864 | 72149ef |
| skills/vision-ethos.md | b675f3d9 kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 6863ef19 traitsAsCapabilities | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 06196cc7 traitsAsCapabilities | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 2b34fafa traitsAsCapabilities | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 04db2fd2 kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 5abf3be8 encodedFormFingerprintTraitDesign | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 4decf7 kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 2ef42163 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | e8c4cc61 kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | b675f3d9 structuralParsing | same | fef9864 | 72149ef |
| skills/vision-ethos.md | ac1e9ec8 datomSyntax | same | fef9864 | 72149ef |
| skills/vision-ethos.md | e4a40e kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | ad19b1 kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | e8c4cc61 ethosFileAnatomy | same | fef9864 | 72149ef |
| skills/vision-ethos.md | e8c4cc61 kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 995a164e ethosTypes | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 62022e8f ethosTypes | same | fef9864 | 72149ef |
| skills/vision-ethos.md | aa4c7747 interactions | same | fef9864 | 72149ef |
| skills/vision-ethos.md | aa4c7747 tuples | same | fef9864 | 72149ef |
| skills/vision-ethos.md | aa4c7747 ethosTraitSyntax | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 2b34fafa ethosSourceFiles | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 2b34fafa ethosNamespaces | same | fef9864 | 72149ef |
| skills/vision-ethos.md | b675f3d9 kinds | same | fef9864 | 72149ef |
| skills/vision-ethos.md | b675f3d9 structuralParsing | same | fef9864 | 72149ef |
| skills/vision-ethos.md | ad19b1 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | ad19b1 designPractice | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 6329f1 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | e996e8 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | ad19b1 protos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 564f55 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 564f55 datom | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 564f55 signal | same | fef9864 | 72149ef |
| skills/vision-ethos.md | aa4c7747 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | e8c4cc61 ethosTypes | same | fef9864 | 72149ef |
| skills/vision-ethos.md | ba906ae2 signalIsOurMessagingLayer | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 62022e8f designPractice | same | fef9864 | 72149ef |
| skills/vision-ethos.md | fe34eb ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | d4ae97 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 8325c1 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | e51411 ethos | same | fef9864 | 72149ef |
| skills/vision-ethos.md | 88475f ethos | same | fef9864 | 72149ef |
| skills/vision-flow.md | 358f143a flowDaemon | same | fef9864 | 72149ef |
| skills/vision-flow.md | e06e4c07 flowDaemon | same | fef9864 | 72149ef |
| skills/vision-flow.md | acbb6006 nexus | same | fef9864 | 72149ef |
| skills/vision-flow.md | 1a6ca4 nexus | same | fef9864 | 72149ef |
| skills/vision-flow.md | 1ac573 operational-nameSessionAfterAncestor | same | fef9864 | 72149ef |
| skills/vision-flow.md | 1ac573 operational-reapReplacedSessions | same | fef9864 | 72149ef |
| skills/vision-flow.md | f38926 subflows | same | fef9864 | 72149ef |
| skills/vision-flow.md | b81560 operational-asyncSubflowsAndMeaningLanguage | same | fef9864 | 72149ef |
| skills/vision-flow.md | b81560 operational-fieldUltraLowRoutesSubflowRequests | same | fef9864 | 72149ef |
| skills/vision-flow.md | b81560 operational-subflowRequestIdAndAsync | same | fef9864 | 72149ef |
| skills/vision-high-level-view.md | vision-raw highLevelView | same | fef9864 | 72149ef |
| skills/vision-high-level-view.md | b675f3d9 highLevelView | same | fef9864 | 72149ef |
| skills/vision-horizon.md | f38926 horizon | same | fef9864 | 72149ef |
| skills/vision-horizon.md | b81560 operational-horizonNexusAndNodeResources | same | fef9864 | 72149ef |
| skills/vision-meaning.md | f38926 meaningLanguage | same | fef9864 | 72149ef |
| skills/vision-meaning.md | b81560 operational-asyncSubflowsAndMeaningLanguage | same | fef9864 | 72149ef |
| skills/vision-meaning.md | b81560 operational-meaningLanguageLogographic | same | fef9864 | 72149ef |
| skills/vision-meaning.md | b81560 operational-meaningLanguageAnnotationLayers | same | fef9864 | 72149ef |
| skills/vision-meaning.md | b81560 operational-meaningContentAddressedAnnotation | same | fef9864 | 72149ef |
| skills/vision-meaning.md | b81560 operational-meaningGarbageCollectionAndOntology | same | fef9864 | 72149ef |
| skills/vision-meaning.md | b81560 operational-vaisheshikaRuledAndSyntaxQuestion | same | fef9864 | 72149ef |
| skills/vision-meaning.md | b81560 operational-meaningDualSanskritEnglishNames | same | fef9864 | 72149ef |
| skills/vision-meaning.md | 5851f4 ashtadhyayiKnowledgeBase | same | fef9864 | 72149ef |
| skills/vision-messaging.md | 108ab0 operational-messageAsDatomInPrompt | same | fef9864 | 72149ef |
| skills/vision-messaging.md | 108ab0 operational-messagePriorityTiers | same | fef9864 | 72149ef |
| skills/vision-messaging.md | 108ab0 operational-abruptPerHarness | same | fef9864 | 72149ef |
| skills/vision-messaging.md | 108ab0 operational-herderMuxKeypress | same | fef9864 | 72149ef |
| skills/vision-messaging.md | 1ac573 operational-modelRoles | same | fef9864 | 72149ef |
| skills/vision-messaging.md | d66c26 messaging | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | f55ec8 modelRoles | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | f55ec8 layers | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | 1ac573 operational-modelRoles | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | 1ac573 operational-olderOpusIs46 | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | 1ac573 operational-defaultModelPsycheMediumClaude | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | 1ac573 operational-modelDeclaredInOnePlace | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | 4a2502 operational-delegationTierRules | same | fef9864 | 72149ef |
| skills/vision-model-roles.md | b05237 operational-fieldEnergyLevels | same | fef9864 | 72149ef |
| skills/vision-nexus.md | e06e4c07 nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | 01a03d6e nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | acbb6006 nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | 98fbfa47 metaCliIsComponentDashMeta | same | fef9864 | 72149ef |
| skills/vision-nexus.md | 012fbf07 threeStacks | same | fef9864 | 72149ef |
| skills/vision-nexus.md | 15b67974 actorLibrary | same | fef9864 | 72149ef |
| skills/vision-nexus.md | 564f55 nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | 01a05487 nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | db97561c nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | fd301d9a nexusTraits | same | fef9864 | 72149ef |
| skills/vision-nexus.md | f426777b nexusTraits | same | fef9864 | 72149ef |
| skills/vision-nexus.md | f426777b ethosSourceFiles | same | fef9864 | 72149ef |
| skills/vision-nexus.md | b675f3d9 ethosMonolith | same | fef9864 | 72149ef |
| skills/vision-nexus.md | fe34eb nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | aa887c nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | aa887c ethos | same | fef9864 | 72149ef |
| skills/vision-nexus.md | bad807 nexus | same | fef9864 | 72149ef |
| skills/vision-nexus.md | bad807 ethos | same | fef9864 | 72149ef |
| skills/vision-orchestrate.md | 01a03d6e orchestrateDeployment | same | fef9864 | 72149ef |
| skills/vision-orchestrate.md | 01a03d6e orchestrateSkill | same | fef9864 | 72149ef |
| skills/vision-protos.md | a5587095 protosIsTheSharedStyle | same | fef9864 | 72149ef |
| skills/vision-protos.md | ba906ae2 protosIsTheSharedStyle | same | fef9864 | 72149ef |
| skills/vision-protos.md | ba906ae2 encodedFormIsTheCode | same | fef9864 | 72149ef |
| skills/vision-protos.md | e4a40e protos | same | fef9864 | 72149ef |
| skills/vision-protos.md | 04db2fd2 anatomy | same | fef9864 | 72149ef |
| skills/vision-protos.md | 04db2fd2 multiPass | same | fef9864 | 72149ef |
| skills/vision-protos.md | 04db2fd2 portion | same | fef9864 | 72149ef |
| skills/vision-protos.md | 04db2fd2 delimiters | same | fef9864 | 72149ef |
| skills/vision-protos.md | e8c4cc61 protos | same | fef9864 | 72149ef |
| skills/vision-protos.md | e8c4cc61 prospective | same | fef9864 | 72149ef |
| skills/vision-protos.md | e8c4cc61 kinds | same | fef9864 | 72149ef |
| skills/vision-protos.md | 62022e8f kinds | same | fef9864 | 72149ef |
| skills/vision-protos.md | 62022e8f layers | same | fef9864 | 72149ef |
| skills/vision-protos.md | 62022e8f concept | same | fef9864 | 72149ef |
| skills/vision-protos.md | 62022e8f passes | same | fef9864 | 72149ef |
| skills/vision-protos.md | 62022e8f vocabulary | same | fef9864 | 72149ef |
| skills/vision-protos.md | 2ef42163 kinds | same | fef9864 | 72149ef |
| skills/vision-protos.md | b675f3d9 structuralParsing | same | fef9864 | 72149ef |
| skills/vision-protos.md | b675f3d9 kinds | same | fef9864 | 72149ef |
| skills/vision-protos.md | 1c282d protosizable | same | fef9864 | 72149ef |
| skills/vision-protos.md | 1c282d vocabulary | same | fef9864 | 72149ef |
| skills/vision-protos.md | ad19b1 ethos | same | fef9864 | 72149ef |
| skills/vision-protos.md | 6329f1 protos | same | fef9864 | 72149ef |
| skills/vision-protos.md | 6329f1 vocabulary | same | fef9864 | 72149ef |
| skills/vision-protos.md | 04db2fd2 directionAsymmetry | same | fef9864 | 72149ef |
| skills/vision-protos.md | ad19b1 protos | same | fef9864 | 72149ef |
| skills/vision-protos.md | e996e8 protos | same | fef9864 | 72149ef |
| skills/vision-protos.md | 564f55 protos | same | fef9864 | 72149ef |
| skills/vision-protos.md | 564f55 datom | same | fef9864 | 72149ef |
| skills/vision-protos.md | 564f55 signal | same | fef9864 | 72149ef |
| skills/vision-remembering.md | b675f3d9 remembering | same | fef9864 | 72149ef |
| skills/vision-sema.md | 564f55 sema | same | fef9864 | 72149ef |
| skills/vision-sema.md | 564f55 ethos | same | fef9864 | 72149ef |
| skills/vision-sema.md | f426777b ethosSourceFiles | same | fef9864 | 72149ef |
| skills/vision-sema.md | 62022e8f designPractice | same | fef9864 | 72149ef |
| skills/vision-sema.md | aa4c7747 ethosMonolith | same | fef9864 | 72149ef |
| skills/vision-signal.md | 564f55 signal | same | fef9864 | 72149ef |
| skills/vision-signal.md | 564f55 protos | same | fef9864 | 72149ef |
| skills/vision-signal.md | 55d18f4f signalIsOurMessagingLayer | same | fef9864 | 72149ef |
| skills/vision-signal.md | 6863ef19 signalIsOurMessagingLayer | same | fef9864 | 72149ef |
| skills/vision-signal.md | ba906ae2 signalIsOurMessagingLayer | same | fef9864 | 72149ef |
| skills/vision-signal.md | 98fbfa47 metaSignalNotOptional | same | fef9864 | 72149ef |
| skills/vision-signal.md | fe34eb signal | same | fef9864 | 72149ef |
| skills/vision-book.md | flows/445410/vision/books.md, 2026-10-09 | 445410 books | 6714d95 | ca88769 |
| skills/vision-aspects.md | 445410 flow | same | c3f8eeb | d867ed1 |
| skills/vision-aspects.md | 445410 messaging | same | c3f8eeb | d867ed1 |
| vision/ethos.md | d5df1d ethos | same | 9fb0433 | 97874fb |
| skills/vision-persona.md | 05c604 persona | same | 7a6b130 | 2956ee6 |
| skills/vision-persona.md | 6fb948 personaServiceAndNexusImagery-20260923 | same | 7a6b130 | 2956ee6 |
| skills/vision-persona.md | aa887c persona | same | 7a6b130 | 2956ee6 |

## Notes

- `vision-persona.md`: its three references (`05c604 persona`, `6fb948 personaServiceAndNexusImagery-20260923`, `aa887c persona`) entered at 7a6b130, whose message already carried them, so nothing was added. Commit 82c92fa (new 69d7424, "the source references move to this message") had removed that section; after the rewrite its tree equals its parent's and it is kept as an empty commit with its message unchanged, so those three lines appear in two messages, as before.
- Other branches on origin (`spirit-terminology`) were not rewritten.

## Sources

- Scripts: `/tmp/claude-1001/-home-li-primary/d68c8272-6db0-47dd-9c8e-538d95ff12a6/scratchpad/bin/srclib.py`, `rewrite.py`, `verify.py`
- Map and verification data: `/tmp/claude-1001/-home-li-primary/d68c8272-6db0-47dd-9c8e-538d95ff12a6/scratchpad/psyche-map.json`, `psyche-verify.json`
