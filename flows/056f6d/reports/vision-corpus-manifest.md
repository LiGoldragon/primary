# Vision corpus manifest — whole-corpus grounding of the written psyche

Repository: `/home/li/primary`
Revision: `6e59653af467dd099f6a0f95ebe4ab33eeb4219c` (`git rev-parse HEAD`; `jj log -r @-`
reports the same commit id)
Date compiled: 2026-09-18 (UTC)
Compiled by: Fable subflow of main flow 056f6d, read-demanding, medium effort.

## What this is and what it is not

This manifest enumerates every psyche record file at the revision above, gives each
a SHA-256 and a count of `## ` headings, and lists separately every relationship
between records that a record *itself states*. Heading counts are **candidate node
counts only**. A heading is never an edge. Nothing in section 2 may be read as a
relationship; only section 3 carries relationships, and each one is quoted from the
file that states it.

Section 4 is explicitly marked as this flow's own inference and is not grounded.

## 1. Coverage and exclusions

### Enumerated (section 2)

The globs the brief named, resolved at this revision:

| glob | files |
|---|---|
| `Vision/*.md` | 16 |
| `Vision/sources/*.md` | 14 |
| `Vision/archive-*.md` | 1 (counted inside the 16 above) |
| `Intent/*.md` | 7 |
| `Intent/sources/*.md` | 4 |
| `vision-raw/*.md` | 90 |
| `flows/*/vision/*.md` | 794 |
| `flows/*/notion/*.md` | 28 |
| **total distinct files** | **953** |

All 953 were read: none was empty, none failed a UTF-8 decode, none was unreadable.

### Deliberately excluded

- Skills (`.claude/skills/`, `.agents/`, `.codex/`, `.pi/`) — generated read-only
  evidence, and skill text is not a psyche record.
- `flows/*/log.md`, `flows/*/reports/*.md` (552 report files), `flows/*/witnesses/`,
  `flows/*/handoff/` bundles, `agent-outputs/`, `design/`, `awareness/`,
  `ARCHITECTURE.md`, `AGENTS.md`, `CLAUDE.md`, `NON_MANAGEMENT_AGENTS.md`,
  `SKILL_VARIABLES.md` — flow machinery and agent-authored prose, not psyche records.
- The spirit skill's text, which the `psyche` skill names as Spirit's current home.
  Spirit therefore contributes **zero files** to this enumeration: there is no
  `Spirit/` directory at this revision.

### Excluded by the brief's globs but found, and material

`find flows -path '*/vision/*.md'` returns **89 files that the glob
`flows/*/vision/*.md` does not reach**, because they sit deeper:

| directory | files |
|---|---|
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/` | 32 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/` | 29 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/` | 10 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/` | 9 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/` | 9 |

They carry 55 distinct SHA-256s; 15 of those hashes also occur in the enumerated
corpus, so the remainder are content that exists only there. **18 topic basenames
appear nowhere in the enumerated 953**: `authority.md`, `branches.md`,
`cloudHosts.md`, `codexAccess.md`, `domains.md`, `harnessRepositories.md`,
`incrementalRuntime.md`, `lojix.md`, `mcp.md`, `operation.md`,
`parallelContext.md`, `scripts.md`, `skillApproval.md`,
`specificationVersionControl.md`, `syntaxHighlighting.md`, `testing.md`,
`tokenEfficiency.md`, `transcriptReporting.md`.

This matters because there is **no `flows/efa157*` directory at this revision**,
while enumerated records cite `efa157/vision/...` by path (section 3.5). A graph
built from the brief's globs alone would carry dangling citations into flow efa157.
Their inventory is section 2.11, kept apart from the enumerated corpus.

## 2. Record inventory

Counts per level:

| level | files | `## ` headings |
|---|---|---|
| Vision | 15 | 108 |
| archive (Vision) | 1 | 6 |
| sources (Vision) | 14 | 0 |
| Intent | 7 | 6 |
| sources (Intent) | 4 | 0 |
| raw | 81 | 69 |
| archive (raw) | 9 | 12 |
| Vision (raw) | 662 | 1034 |
| archive (Vision raw) | 132 | 397 |
| Notion (raw) | 28 | 36 |
| **total** | **953** | **1668** |

Heading counts are candidate nodes. 127 of the 953 files carry no `## ` heading at all
(they are single-statement records whose only heading is the `# ` topic line).

### 2.1 Vision — 15 files

| path | sha256 | `## ` headings |
|---|---|---|
| `Vision/datom.md` | `7a097b0ed047c205aa12a31b8f8fcf9e8bf8dca88d98bbf917eccaffcc9f3003` | 17 |
| `Vision/distillation.md` | `d917dd9d7b538e0466abcc426ad6d1e3d7334407234436fec25dd33924cd47a9` | 7 |
| `Vision/ethos.md` | `4d47f4451825209acf53de9354b105eeacbf1f9d49e44dd25919bf4df4ea4f91` | 24 |
| `Vision/flowNexus.md` | `bf1bd2c4f3eb134a0afaed81a8b11dc79f1323e6d6bca5dcf0ce6612d105217f` | 5 |
| `Vision/highLevelView.md` | `c76eda3c7ff903db90ce95a618c4708d8a714994f64a259c0c4d95afcf31b4a8` | 2 |
| `Vision/messaging.md` | `c8907401db9f57d19c26c0e0f76186080bd77aa5997f5fb4344381ee4aff0476` | 4 |
| `Vision/modelRoles.md` | `21de6c965c450ccfc1e14e4c6b67bc8b5e94d8b6a3314b9d8fd2b838111a30a5` | 7 |
| `Vision/nexus.md` | `8a40043950dd475963ca3b901f0c3eb37bc8041d280f2e46a0331262ce1d2676` | 19 |
| `Vision/orchestrate.md` | `9cced928c8bdc0e9ab58ca50053d00c5a0e6081f599d240ac927b97ba29f93d9` | 2 |
| `Vision/protos.md` | `8cc31f5aa370a49278541f930a5bb498060400ccfabcf8355995722d306f6f68` | 11 |
| `Vision/psyche.md` | `a95e10ede5a92a780e093dd3ddbbb371c0b501df4fd4d3eec7dbd37411dc8cd8` | 0 |
| `Vision/remembering.md` | `71e721d3de29a6810e73f851e439341ec39771d8f161579a6d177c710f43baa3` | 3 |
| `Vision/sema.md` | `c673c38efc010080907d016d59ba6d461995621041e713a92b78ab3504ac5258` | 1 |
| `Vision/signal.md` | `26bca161c8cad99f50ed7d7d77fa4f95dbce30ca55d8b90a29d1a436ec619e90` | 6 |
| `Vision/x11.md` | `06d9b3099998bef5bacaa483e4f8e5327d23dcb2f6716f1ecbc2d5bd805d3563` | 0 |

### 2.2 archive (Vision) — 1 files

| path | sha256 | `## ` headings |
|---|---|---|
| `Vision/archive-ethosMonolith.md` | `9970b110f78e7ace24c17112cc023cf38350babb2f8d3c874e63ee37b47b17c7` | 6 |

### 2.3 sources (Vision) — 14 files

| path | sha256 | `## ` headings |
|---|---|---|
| `Vision/sources/datom.md` | `ae821e143862043950d2d4f0b9dcd40a7111890be25cdc18e3f9e2e4e537e3aa` | 0 |
| `Vision/sources/distillation.md` | `3bcea4e8a574b5afd79b4abd2aa79ca4141e2c1fae7c492d3a1e7379c7944f5c` | 0 |
| `Vision/sources/ethos.md` | `7efd24c6c5903f52b9890efd0a24576f728c361737a7a1b2c99a5d940e7677aa` | 0 |
| `Vision/sources/ethosMonolith.md` | `a40f43470f212976717a52f5586fdb1eeddf235ebedbe3bffa89f7df3f093582` | 0 |
| `Vision/sources/flowNexus.md` | `53bb55256315a13e5b8c3e9e8fd82c160828ccfe83dc7a3908c2d8d2b360d7e2` | 0 |
| `Vision/sources/highLevelView.md` | `ae1b5460aeecb6b64524eabe8097cebf6a60c5bef5173f1886bdceca57cb66d4` | 0 |
| `Vision/sources/messaging.md` | `e4a49e299dcfbf2cbc5ae06232f9a55c704fca42efb6363209b60d43f802d526` | 0 |
| `Vision/sources/modelRoles.md` | `d739597cf0747d7df955fb371e07796645b8c6d7f5a8d5cfea93b906aa72ddb0` | 0 |
| `Vision/sources/nexus.md` | `cb9665adf65077b5147b8c7c601a64803877c9b4ca99cff8cbc1c8881e029d6e` | 0 |
| `Vision/sources/orchestrate.md` | `3a625cff551f363b7fd2c2a88f3896e911e1284055eed8954c6e152f6cd77966` | 0 |
| `Vision/sources/protos.md` | `aeda08d1a48472cb0421b697ad0e8c2017f6e44702af10c3927be836abc90b43` | 0 |
| `Vision/sources/remembering.md` | `cb3e5cdc145c718a2796b0e84f9e4030043147fceed11e736417b724454d8338` | 0 |
| `Vision/sources/sema.md` | `3057fd8e1a80b49c6b58e59443294b4e8f52d5623165f5da02e1d322ee6c0ad1` | 0 |
| `Vision/sources/signal.md` | `7a46e7b5ab3e375db3f45ae6030423100dcf5baf8b1560a33e7bfb21aadca598` | 0 |

### 2.4 Intent — 7 files

| path | sha256 | `## ` headings |
|---|---|---|
| `Intent/anatomy.md` | `7e85b973e5e94c022295f41ecdb438ce8b6854a89224e38f2681b6d4b5129ec3` | 1 |
| `Intent/context.md` | `f3c12491f9bb235b2ddbfb91d32d4cfb6677db1911f7ddaa455dbb5021e00df7` | 1 |
| `Intent/conversion.md` | `7ef61f1632bee7472dc2c940a1f29f79f970d50b5e26365b4fab4ec840946d4b` | 1 |
| `Intent/data.md` | `28f5b5666e3fa596ad1b395f91c2753603a77727ca00e9fd9af119ea807f9ed7` | 0 |
| `Intent/mandatoryTraits.md` | `7de34d9471ae067570802b12d7d158fb3771c2e1e303aed3fef4cd1cebed9f18` | 1 |
| `Intent/models.md` | `91263a938bdf245e4669934f06b92f716e754ca4ab2596e94ccac333be103cfb` | 2 |
| `Intent/protosParsing.md` | `a43b4d1f4ed960e6eacb1a06b55fb500cbff0eae1634739b62b9d75e70c09bb0` | 0 |

### 2.5 sources (Intent) — 4 files

| path | sha256 | `## ` headings |
|---|---|---|
| `Intent/sources/anatomy.md` | `a7a0ae6bdca0f1e7591a3b045e57bdf261875d0529045ebcea89ac6114502775` | 0 |
| `Intent/sources/context.md` | `2f22e77ebff92797c177a599796a34c88fdedd506f9982148dddc8f21ecc264c` | 0 |
| `Intent/sources/conversion.md` | `0bae2d89040fe109e4881c36cb94f41c5b5115ed42c64603e12322aee033a656` | 0 |
| `Intent/sources/models.md` | `5dbd112463a2fef2b20bf257982f33ef5d95533c2e4cf52acd3b470fa7fb43c3` | 0 |

### 2.6 raw — 81 files

| path | sha256 | `## ` headings |
|---|---|---|
| `vision-raw/README.md` | `bbad04b388309fe3610633bf117c2baf81467343be545d91daf8a55ccbe4d665` | 0 |
| `vision-raw/actorLibrary.md` | `a9d4f3fd122f9e81073e3b1f05b46a73273082ea5abab2fb443bfcadb70d5ce4` | 1 |
| `vision-raw/agent-intercom.md` | `e227ddb06ebc70f0588372268606af5407de911ecf5c5ea1ed0091ee91fe3ed7` | 0 |
| `vision-raw/assembly.md` | `25cd80f37729dcc587526c0d56b1367af00b1cbfe96281cdb35df91a4d33ac84` | 3 |
| `vision-raw/attunement.md` | `3859f0cdfaf62056078ea109f918d332a400b3fa07e9e7a85c6d4d9ad760cec5` | 0 |
| `vision-raw/awarenessIsGeneralUnderstanding.md` | `728ba6608eadd2ab38e74d2f25d7f7401ec472918ef5e60234174fdb42482c8f` | 0 |
| `vision-raw/behavior.md` | `fda97bf07a90a7d18f69ae04bc19936fc9b0169b1c4ff0b7f4befe6fa6d8220f` | 0 |
| `vision-raw/codeAnalysisTools.md` | `c22ea346b7c00fd0bf1f8d3b6fb0a94220276ecbd323fefd9ad9e04582c82b27` | 0 |
| `vision-raw/codeIsLanguage.md` | `7a1ab4d7da44a6c62e93bce5bfe7a40bb2c33fa68a8f76c694c0457dd2a3dce9` | 0 |
| `vision-raw/colonFormTransformerSyntax.md` | `b81431a3bb69eda91e1de238ca4e6f10dcdcdf487c7afdbd0dc1a04d4482cf1d` | 0 |
| `vision-raw/context.md` | `3af486b74d7fc0a0c109873d34e56384b2cc4fe356079b747e73c228a9cfb91f` | 1 |
| `vision-raw/dictation-vocabulary.md` | `8ee2452a031e53930b8530e14a5cfbb6db38e707e487cedbd468369abb802de4` | 0 |
| `vision-raw/domainKnowledgePlacement.md` | `d45b94f659ec87c7b90fbc5098713f3a7d808ff8d932cd0cab55348da38131af` | 0 |
| `vision-raw/draftIdeasForImprovement.md` | `c770ad64f8983cd9f3ac906de89b875fa15569b923ebb3f36156c0aaa0207bb3` | 0 |
| `vision-raw/entryFiles.md` | `3950ef9eb997c589e8c41d3783d51e8bc25486eba02d3c40d1336e700c2a4058` | 1 |
| `vision-raw/everyConceptShouldHaveItsRepo.md` | `6d68adb1c4af5a84a660e6648b816b2cff35d2c7be3ac4c2467d351d9ed936c4` | 0 |
| `vision-raw/everythingIsInTheDaemon.md` | `98c66193fea5396abf601c1cde0ce3c59a0c8c6d8a34bc64ec78eb25c093098e` | 0 |
| `vision-raw/falseConfidence.md` | `91d9f1268ee40791943258251d9ca71ec7b5548f55195a171b628e1cdb3dee00` | 0 |
| `vision-raw/flowArtifacts.md` | `72a390c34421815201059dea4f8f32fbb62079fc44aff0a221a93f692449bcd9` | 0 |
| `vision-raw/flowDaemon.md` | `86749570094b5c6df004b8304aff6b5c987f08088a563613d648c32c080cab13` | 0 |
| `vision-raw/flowKnowledge.md` | `83cdccb3fdc3ace8f9a9924d5288372e20f70932760260c95dad6c52adb10a1d` | 0 |
| `vision-raw/flowNaming.md` | `5b37cb72dfd7237aacf2040680d810578d2cdac4810caa4941306bf68e35a60f` | 0 |
| `vision-raw/flowsNotAgents.md` | `f8378ba0a156259a2754997d1f4bae9b10c8611b8611aa4abebd2a30909b7fa7` | 2 |
| `vision-raw/genericParametersAreTraits.md` | `25951f2228d6aa1f2294d2852c7f365f6db63fe3ba133d528a90cb14e5db26b1` | 1 |
| `vision-raw/gradientsOfAuthority.md` | `cc97cf475d1a43cd019b8a7f78200002a5219796c7a03a82f0592bcca6138bdc` | 11 |
| `vision-raw/healingAspect.md` | `66773efebd91fbce47c6ff73aecf5324003020de77e47ea9a94c3488a43d471a` | 0 |
| `vision-raw/hexis.md` | `8b13eeea5d03125d67eb40b27ed1bba826f0b86ece890db054d1429f6f03d941` | 0 |
| `vision-raw/highLevelView.md` | `16d03ba82cd5ee0d2449c210b293cb6c250d8a3437336e6ba59c80aa864096ca` | 0 |
| `vision-raw/host-environment-recovery.md` | `03ea8878c9649aa2f64e1f9db88f6bf48652aad97f3cc6bdc6fff790ede046e4` | 1 |
| `vision-raw/importResolution.md` | `2cd6efacff2de0dc001ef5770a4860e344bd5285ec2b789985a389985db809f6` | 2 |
| `vision-raw/investigation.md` | `aedf93594dd9ae4a52ef49ab31f7d9b33f1f6edc09ac74993042d61b1d1c034d` | 0 |
| `vision-raw/itsATranslator.md` | `c001b0ec936ad523402e5beec7e7c8724cecc7b7fcced81f040130ec79b05807` | 1 |
| `vision-raw/letsUseTheSameVocabulary.md` | `00c94aebb1cabab218f79b2f83a4d659af8bd202bdfd2c5b15e77ae8dfa53461` | 1 |
| `vision-raw/lojixOwnership.md` | `a95b3fd3e1929621ed3e4436c9b626d23fc3c6111a35fe513f7de283b0c39d7b` | 3 |
| `vision-raw/machineAnatomy.md` | `2e3f9d2ff5b945160760d21902b88ece7c9632f427a0de4c06e9a9f625c836b9` | 3 |
| `vision-raw/mainForEverything.md` | `776b001697e32a7ba7d69610d3e9d065250ada46a7c10094739f7645a940384b` | 1 |
| `vision-raw/mainFunction.md` | `eae5a61bf0d46ed28209e1ff7ae3d6fa97dbb0d5b9940a909a26cd9eaf71e895` | 5 |
| `vision-raw/majorRecoveryEffort.md` | `b7706ed23e96e3a8dae94cb03f48129e6c2b511883b31e97d893b5258b078508` | 0 |
| `vision-raw/managementDelegation.md` | `7603e3212cca4a2feabae0b8f1db1932efd10427d002d31ce25fa7b9d6da2a47` | 0 |
| `vision-raw/manualPostResetSkillRestoration.md` | `1d11a66f0af845a46fa2365509514ab12ab86764780cf97d2135639c22d34039` | 0 |
| `vision-raw/mentci-egui.md` | `5036e240092ba73646d2c265e2d0b07ecb3bbf31f5829e7dac10218b33f71d4b` | 1 |
| `vision-raw/mentci.md` | `809149d9a58c7773131147bb18c6f031e1714ac1bd928c8bd757e191c5d096b9` | 1 |
| `vision-raw/minimalFlake.md` | `5237542f73597c83dd57e7b2bad94f1fc1131e95bd61cc14e7cee4a90878a097` | 1 |
| `vision-raw/modifier.md` | `fe0b92897e214c755e99ca6b04658bc70ef38f86c086808311fabe2824ecab7a` | 0 |
| `vision-raw/newtypeWrappingAndSingleFieldStructs.md` | `d4578a6d3928875aac70a4f2c5a75670037eb3cf7c600148ca15323ab4ddbb0e` | 0 |
| `vision-raw/noctalia.md` | `e2f2ada79004a09adeced434db58acbd38e90ca9d869db576b62b1f55801602e` | 2 |
| `vision-raw/nonIdealAgents.md` | `4fe4514492aca3bb24c52f9cf22d340d5004e322a4c620ab2b0e94245c07ed4a` | 0 |
| `vision-raw/observerFixtureBlessed.md` | `e1ae507b4b1097eb701253f98631dbfc730dd45c898b49c4ed36adbf51a21fa3` | 0 |
| `vision-raw/parserIsTheParser.md` | `bee7a23e2a2fc093654240901c0616228f68eb65aa9349174c85e8ba39cecd11` | 0 |
| `vision-raw/persona.md` | `78c99918ade467c9e214a8e4467302dac7d62cb924a9d9c7f83bfeacba8c1dc8` | 0 |
| `vision-raw/protosIsTheSharedStyle.md` | `c2b875eac932be55e810e45b8d47367a16cb44ac6118da5893c1343a24485de6` | 0 |
| `vision-raw/psycheIsntPerAspect.md` | `282cc2ae77c44e2418aedcd8bba7fe35afc4c82dd1630bc61af6b01ce07f21f1` | 0 |
| `vision-raw/psycheLogStructure.md` | `819e03b4c75becc64bb13e2a19a8720f616a3a29dc2d1858975b5b804e296fae` | 2 |
| `vision-raw/realizer.md` | `15091393b52d32acfa169e57495119977a2c3568b41ba7e7b5856546204d4e28` | 0 |
| `vision-raw/roleDescriptions.md` | `be8b1f4857b904c24a63f21f39caa84ac11200c3619bc1a5f67d00384831cb67` | 1 |
| `vision-raw/rustComponentArchitecture.md` | `480a7e4cb127530c4e7b1d42befa4e0d989aa368f261bd9569595fbc6648662b` | 1 |
| `vision-raw/session-log.md` | `590fdee4aebf5980bcf6a17a3467567abac3ff9cf82faf48ad427dd050ccad25` | 0 |
| `vision-raw/setupIndependentInterfaces.md` | `cc6d89e1cf452b05cf64a0fde24752974b9ed614bb5a426dc8c681a6b078c002` | 6 |
| `vision-raw/signalIsOurMessagingLayer.md` | `7139fc901f71498a2118c770a2a25ace252667ce1f0a1af1d9fd888691f68ac1` | 1 |
| `vision-raw/skillDesigning.md` | `bb56a44f8e7fe400398a5af814d76e6878507988252d76770a99695a655c3e1b` | 1 |
| `vision-raw/skillTypes.md` | `4cd0eaf4612d9777fd83845b5f8326c214f8b9672d879900cce875da82155c84` | 0 |
| `vision-raw/skillVoice.md` | `5580860a5d70a5b26c122efae3a098037e7e67a543231e39b39c6d0d166abd92` | 0 |
| `vision-raw/skillsRepoSourceOnly.md` | `459d4b1addb30571de99e52cb7a8f0cd8dcedee50f209f2b8dfe15b60b8bf0e7` | 0 |
| `vision-raw/skillsRepository.md` | `1d9f18a75583a449c848b150cb6d556a29be2e5bd1ea212fd26eaf8c81176404` | 1 |
| `vision-raw/sourceNotCrate.md` | `5b457c3bbd8d03ac22c3fa96ea7bf556d2f69115194593057b026c64c240a188` | 0 |
| `vision-raw/spirit.md` | `9dba681dc4d636fc8122fc608fc714bc8a6673d1f08fc5cde64706ec27135a49` | 3 |
| `vision-raw/spiritComponentAndFile.md` | `c02d621db0680aff7e47e2212ec10e589c0b9c72c2ab98ed6800764e0c8218df` | 1 |
| `vision-raw/streamAsFourthKindMvpFirst.md` | `fb818c3cedd949afe5163ea8ea054bc3bb94007f342e8a9635ac814b7bc2b237` | 0 |
| `vision-raw/streamSection.md` | `5b2b8a2360e3db90f91eb3f30a787d555a235cc38c9a5e14e9d6348818ccb685` | 0 |
| `vision-raw/structuredStringType.md` | `1d5b640ab6fe118479b030fad1f2b770e0d543b1cd7ed55e3e04be9ac6d4204b` | 1 |
| `vision-raw/surgicalDataEditor.md` | `61bc34808bfbc992c6ffaf818cee7ac806b34a03e0c355bc2cdc786e05dd6fe9` | 0 |
| `vision-raw/surveyingAllFlows.md` | `2c50da02c17a23124a875bca1250e4b97b2d609d6837640d812d465666e071ae` | 1 |
| `vision-raw/testTravesties.md` | `3dacffcb7d168151fecf2d0d72619e14a328c3666ea71105a11bcc94c12b2283` | 1 |
| `vision-raw/theBestShape.md` | `bc5f7059b278c7b201da63a97d35b24c8445a6204c4383e32c97c21ffea10cfe` | 0 |
| `vision-raw/trainingRepo.md` | `481ca627e1c5969818fce54cb5acdc0c71f20d39251f069de6e02f0488f2e580` | 0 |
| `vision-raw/traitsAsCapabilities.md` | `1cea302a447f042bfca50f1bd28fb9440c9026fee46859102bc593cad2f208e5` | 1 |
| `vision-raw/verifiedInformation.md` | `386cf7249d20c5b1f42f43c20f14a6741c879fc702eb80e2e51afd1d6433b81f` | 1 |
| `vision-raw/visuals.md` | `fb25b18ff577557f11837f5de1daf1737f2b53cccce878f625d212e0b1f0a17c` | 1 |
| `vision-raw/why-is-rust-analyzer-running.md` | `3656a53a4bdf814d0df45276d6e2e440397e0ddcb74b4fb57b84b928eae6ebdd` | 1 |
| `vision-raw/workspace-2.0.md` | `f8bf7fe6f718bb0ccf296304010f4ced5d249a93b39dbdd4742a85da4ddbf324` | 0 |
| `vision-raw/worldModelBeforeCode.md` | `832abdfe5676d54f6a4362aaf4472f2fd3bf8d5bd3a4d99fd7039c78a0421857` | 3 |

### 2.7 archive (raw) — 9 files

| path | sha256 | `## ` headings |
|---|---|---|
| `vision-raw/archive-colonConfusion.md` | `6dc6cef453fb1fe9a0b21995ebe915047e5b2090dbefb5c0ccbf4af4a06c2c9f` | 0 |
| `vision-raw/archive-datomSyntax.md` | `ed2aef078f261cc63ae3462ba5d765db9d1e98f2af7ac8b388a2004bccf49012` | 2 |
| `vision-raw/archive-encodedFormIsTheCode.md` | `6589c8b356f240cacda1aa1016ecfc298394d42b431ba603860c09787bbf3c89` | 1 |
| `vision-raw/archive-ethosDotosDivisionAndHelp.md` | `01352df34f7aeeb24540f7ecf39c94d0b7c3f4d9285afb01e7e3f760f9982d34` | 1 |
| `vision-raw/archive-ethosNonRepetitionLaw.md` | `ad31e35a0de40f05f0c7ba0b52e470d600e340a66ac42be7b634e146bf9e7ac9` | 1 |
| `vision-raw/archive-highLevelView.md` | `4c191682b0ca0ba6e889d0fcf1b6fa1704650b314c8fe5a289b926910ba0cef1` | 1 |
| `vision-raw/archive-rustComponentArchitecture.md` | `2396f53dfbeb1a0fca3eb4ca44814b72419017b0279673adbd78031a470be6fb` | 1 |
| `vision-raw/archive-threeStacks.md` | `666521e96825afed063dffa04c50343c161ba2bcf6062e7cf63a6a06f81c64db` | 2 |
| `vision-raw/archive-traitsAsCapabilities.md` | `b4073dbe60b5b1b63c997c3def77f661c6a11f7973bb8ad57875ec0d792e2f4a` | 3 |

### 2.8 Vision (raw) — 662 files

| path | sha256 | `## ` headings |
|---|---|---|
| `flows/0062e8/vision/horizon.md` | `d73e30ec826122883e5bcb2a6c64594239d352d071eeab3dbbb393c31d4a4cde` | 3 |
| `flows/0062e8/vision/live-installation-image.md` | `4ae642eb35e79df2dac5cd2fa00a7049dd81a36db9e696bf45e3e9afc26c470f` | 4 |
| `flows/012fbf07/vision/gradientsOfAuthority.md` | `52fddddce8fd984b62255cd8e5b3ca94d5fdc89386b7fd3afbbde3dd389c2b3d` | 2 |
| `flows/012fbf07/vision/psycheLogStructure.md` | `6932abba1b78d4c53b97b72067c60b6b44513c592c65be1a6049451ba5a28a5c` | 1 |
| `flows/012fbf07/vision/threeStacks.md` | `0da4085efe5891c78dfe95546eba492cfc28628d8d1f978b606aa890a68bd8aa` | 3 |
| `flows/019fe121/vision/agentIntercom.md` | `2b9dd06796e5959c3a6316f4b2b604492b2bfabbc477de1a74ece82df481f557` | 1 |
| `flows/019fe121/vision/dictationVocabulary.md` | `05c80a62f332e4784fcac7a7084d8f38633e8aaf7516ed108ddadf057e32572c` | 1 |
| `flows/019fe121/vision/hostEnvironmentRecovery.md` | `0f310b3fa9136d682e1181c921ac9bf766cc10fce3f4849265d0a56cc9b8dbde` | 7 |
| `flows/019fe121/vision/nonIdealAgents.md` | `e3277b72d9a691c359c2249b02e2b830b29ee479e67c172bc075878313c70383` | 1 |
| `flows/019fe121/vision/surgicalDataEditor.md` | `0d3f777f790939788f2d04d2d89946f4b9843ede93fa79c14a851f64b05eb6b6` | 1 |
| `flows/019fe641/vision/hostEnvironmentRecovery.md` | `0735985a3209e5bd01018e97a212d027f7d838a867c8dd1627f7b00e3d3b829f` | 1 |
| `flows/019fe728/vision/agentIntercom.md` | `52a008b4d2ec3bd378409136a7097ae78686a62c8444b0af47dfc340edd5eb13` | 2 |
| `flows/019feb93/vision/threeStacks.md` | `fa7469461f89728c8f1598f6a59b6e46fbb1d7ae9c921f3975366753c117e1fb` | 1 |
| `flows/019ffc53/vision/threeStacks.md` | `364a9684aef9781279cc99664acd6796f5d03e51e52aecf056df406a644b1864` | 1 |
| `flows/01a01046/vision/noctalia.md` | `96c93bfdc7caf045cddfa0d7e01d9519a9ea23a70037ddf8082376365b2d21d4` | 1 |
| `flows/01a01046/vision/setupIndependentInterfaces.md` | `5bb6ace93f51dec7f3d744ec6c6dba3d37caa63fabb132b5657f2e8aa7168bd2` | 1 |
| `flows/01a01046/vision/surgicalDataEditor.md` | `c880c924a8af18e095219aecc29d97da36462bd5a5f2afe040d8667673a3506b` | 1 |
| `flows/01a01a93/vision/hostEnvironmentRecovery.md` | `7226176ea1ba23041b394238ea6f9ee48b3ca82c252df073d19bf7deb7295061` | 3 |
| `flows/01a01a93/vision/skillDesigning.md` | `801daff00f604c27fff642ef6e70453f3840f8a26f5a421b591b7afbd1c28754` | 1 |
| `flows/01a01bac/vision/skillDesigning.md` | `c6f39e56cece0c7c21e2c68d4129aa1bd27b9327a55bf1bad8edbd2631b8eea2` | 8 |
| `flows/01a01bac/vision/testTravesties.md` | `02bf39204b681f37de221f8b0eaf56eb5db7f427916545ac7661abb227e26c13` | 1 |
| `flows/01a0238b/vision/emacsPlugin.md` | `6357e8b14f97d459df3367cb8abb2b950f3fee85774b9ad736c0a13d08c870ae` | 3 |
| `flows/01a02400/vision/defaultOpeningLogic.md` | `9bf6798dc473d35cdd0edbf896968a8e0f9cbf1d1c2c9789083380cabcd0eab5` | 0 |
| `flows/01a02a06/vision/artifactMigration.md` | `b57bc9301924f18b39a44d7db23904aedcd5e872fcf6a37e4c746b2b80f4bf2a` | 3 |
| `flows/01a02a34/vision/epicBranches.md` | `09d1356e71f601aaa6e90b01eec0757e28a585fda336a4955c7ce11f62ca1761` | 1 |
| `flows/01a02a34/vision/focus.md` | `892f12602ff0aa9405728f250225fc45204b04784e5a6995bb0ec7b5f80e0b04` | 1 |
| `flows/01a02a34/vision/pathLocks.md` | `c90a560e9f2e998bdbe9d58f41fed4d48148e3c838fe592a589a0a337926eb6a` | 1 |
| `flows/01a02a34/vision/progression.md` | `782e86b1149cc66acfaec722669d9c1eed8159360c43b9f9d0d5007c603d261f` | 1 |
| `flows/01a02a34/vision/sandboxedTest.md` | `8fc0df796093b90d7e11bb56c932298320ba94cf563df04a3109218259cb5382` | 1 |
| `flows/01a02a34/vision/skillDesigning.md` | `1dac070bd985bf9dce22afc0ca5e28bd7e0705556c6157d36ab9d66a8fb686a8` | 1 |
| `flows/01a02b46/vision/zeusUpdate.md` | `431a1520df21ddcf792e211847360e9d1ab19ffabd4f28c78cd4d7700018ccf6` | 15 |
| `flows/01a02b4b/vision/emacsPlugin.md` | `59958b5e2e0b16945e31701e4406571e29398e7492230d90583b2049a34fb3e1` | 1 |
| `flows/01a02b4b/vision/homeEquivalence.md` | `42a28b06df594467b49539d996b60ea88458e1ecd7002ce7bbaeccd0debe483c` | 2 |
| `flows/01a02b4d/vision/actualProblemsWeAreSolving.md` | `0377dc682f96a053e14023d466798e63c9d817d3ee3d9788207b27fb05058a73` | 3 |
| `flows/01a02f23/vision/orca.md` | `dcc7bcb420a337b6ffdf6e1b42b998173c79ad25f33a34dd72a0563d9548f0e8` | 1 |
| `flows/01a02fd5/vision/interfaces.md` | `26774edaecb31d4b4f239d5e7e6f873ddc8f5a731d470b0cc5f3c17c0db4fe07` | 4 |
| `flows/01a02fd5/vision/metaOrchestrate.md` | `2658c461b8434d0fe4d4b5ff699aa7870486300b83c22f2b7055fa5e39f41c77` | 0 |
| `flows/01a02fe5/vision/skillTraining.md` | `c40eef4743a369965a7d454c700b243eaa1ccc453599929793a185eb5bc40d40` | 5 |
| `flows/01a030a1/vision/commonGround.md` | `7390112d5d3bcf137046aefaab075722f2b5f8bf23e591ee5624eb5f594fee51` | 1 |
| `flows/01a030aa/vision/herdr.md` | `b257487942a063452412d7ad6767884217f36dda001a6e89b05b5d876bacfe15` | 1 |
| `flows/01a030b7/vision/zeusUpdate.md` | `7b6b74d753691ce32354473292d1b6511b456498c89b315cbda3fa20645eb2f1` | 1 |
| `flows/01a030df/vision/subagents.md` | `846d4e890860dfb0a285988fb5ae4df39f15cf0555936076441644a36c71839c` | 1 |
| `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md` | `7985a36c5ec80fc10fa554a32556dc290304dc7f0084fffcb5b89828ee406758` | 2 |
| `flows/01a0338f/vision/mediumGraphicalNodes.md` | `a88c5f2c43e0fecfbb5a313e89a9e38585b33d7fc4bcd1c8fe60110194a3ef8f` | 2 |
| `flows/01a0338f/vision/packageAuditProtocol.md` | `757ed93dffe8edea2b5e284ae11567477a45289c6f277c8b876a2391da2b0f54` | 3 |
| `flows/01a0338f/vision/tuiAndDesktopVersions.md` | `d92a9332b3803f58810d1b329892ea3296676c5b43da3a33b92ccd3b2bcd24ed` | 1 |
| `flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md` | `db8b951c1bc6eef2a8e1cb23f23782e84f290a1fd118aa03ae244c4254125af6` | 1 |
| `flows/01a038be/vision/codexDerivation.md` | `91da14f99c4a674ad4c3fd66f27bb2afa14c82a5930c20a683ba5f013f913630` | 1 |
| `flows/01a038be/vision/installingSoftwareStatefully.md` | `98874ba2918da04c3f35d6d5296c244604887db7f4ba74786f07000394a5d876` | 1 |
| `flows/01a03952/vision/orchestrateInPath.md` | `0609f7726902584e394eebb47303ca7d8e25f22a600ea2af62a4f02db4212a4c` | 0 |
| `flows/01a03d6e/vision/flowIdentity.md` | `927de3a57dad39cf299585d3ee35fb223837d9355b61f163f423d2f41b6cb8bd` | 1 |
| `flows/01a03d6e/vision/flows.md` | `665a866c43ea6f5302a293cb2444befd118dea855498fb67aefd7b04104574f9` | 1 |
| `flows/01a03d6e/vision/locks.md` | `0e4ea89c8e1eb07fcd89fe2ac46b299ada16e4b1380ac8a2f70fea8f41d184bb` | 3 |
| `flows/01a03d6e/vision/orchestrateDeployment.md` | `e28de1dd6dd6bd12a8453cb227e825d59118162c8aff8297fb90b117a8f3da5d` | 0 |
| `flows/01a03d6e/vision/orchestrateSkill.md` | `3e5e233d316f730d9aa2454ecdf17acbfc652f79295b13e41c727e8e830cf23a` | 1 |
| `flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md` | `9dbf20de1cf13a01012e4fae8aa6acfd4eb30c561166648d33c479e50102ddb0` | 1 |
| `flows/01a03e39/vision/lastSuggestion.md` | `efc16f561301b3b5ecbd7519a7312306413b93b183a652581591412f8ba8a528` | 1 |
| `flows/01a03eda/vision/observe.md` | `a493d6c6d925e68892c734b10defe53be4dfabc36a6e0f0848232bdcaf580f0e` | 2 |
| `flows/01a03eda/vision/orchestrateRealization.md` | `bdf2475097b130ab92fb8a2fbb4c1e5b325c681765aedbb321ccbbc3ed08c5fa` | 1 |
| `flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md` | `17606c77228c76ee11043c1073ebab182ef53722bbf0e28e4764f4d42dbd0541` | 4 |
| `flows/01a0428b/vision/codexOnlySkill.md` | `ba24ac69bfac3fc8edf282864a448680a0277e027a9011957df390d6f350a6c9` | 1 |
| `flows/01a0428b/vision/useASubflowToPutTheReportTogether.md` | `917be7bd89385fbe43fa154f182529995c662ac8e9e493bbb150a851544f195b` | 2 |
| `flows/01a04336/vision/remoteFlag.md` | `ea2f993a401342041a7e046e4a96dede11311dd895ee30318ca71be17f914e0a` | 1 |
| `flows/01a0437d/vision/codexAndClaude.md` | `b10ee936b4b005c23b7286d926ef299d78bce1db3b9a0111ef5fc6b3a3dde31f` | 2 |
| `flows/01a04524/vision/claudeRemoteControl.md` | `952916f1bf43bf678da736f44c9e6fafd315a66af42ed9a549f94261393daca4` | 2 |
| `flows/01a047d2/vision/remoteControl.md` | `cc65e76c23b22c7207b5375f0a418abc162639c83cd08c413c54b8b073f4dfbb` | 3 |
| `flows/01a04881/vision/agentIntercomGraphical.md` | `ffd2d1ef28cea9048374ac15ad621529e08e134c7d4bd5d156f939c77faa433e` | 1 |
| `flows/01a04881/vision/cause.md` | `3b1bbafb2dcd2af44dd9aa1725bd6c5b7aae4cec4d8aeaa9f6f2aa315fa5bb1b` | 2 |
| `flows/01a04881/vision/repeatingLikeThis.md` | `a1c275e743741c916181f30b6d798b13a4c22cf74aeace20cc76a9172fba263e` | 1 |
| `flows/01a04881/vision/subflows.md` | `54d7ef0b53f4e3c58c1cc8a468dcdf0118352e4f942088df88834da09e821674` | 1 |
| `flows/01a048a6/vision/agentIntercomGraphical.md` | `05b1c32d86745349a98f9c73b0456ec7bdd8b203eb78609b16e199a69cf39a26` | 3 |
| `flows/01a048a6/vision/deploymentSelection.md` | `9e16cc35f07d8d04d387d800f0f9d67e42229948437a308077cd49ee9b9a08c4` | 1 |
| `flows/01a04e75/vision/listenerWisprFlow.md` | `097fbb3c9f36729d282373b61befa3282093e788bcdeca2eafb971752bdaad06` | 3 |
| `flows/01a052b6/vision/ideaEditing.md` | `2e902c89c2b1cc5eb12afff3c0fa2ce5838b6f21e91f25f4d28d989f814fd3b3` | 1 |
| `flows/01a052b6/vision/reportFeedback.md` | `03393a271e44a6c01c5804243d3f96b70240e67fee29ea6e0be5373557f131b3` | 1 |
| `flows/01a052b6/vision/visualCollaboration.md` | `05bdce0703cb5b2ca66bafcbfb5b37375e08e3fba57461eec2bc80f9975b9a5a` | 3 |
| `flows/01a052b6/vision/vocabulary.md` | `651e2a8c3dd150105544ad9a5653427fc6fa4e12abf1272888181cb8ba7a6f2c` | 1 |
| `flows/01a0539e/vision/listenerWisprFlow.md` | `ec1813dd9fca85a23b3ba4cea04f3b0327e305d4528f4344cd86dac2dc2a1f84` | 0 |
| `flows/01a0539e/vision/wisprInteraction.md` | `a4469d94d334d2afac4d3100775db689fad4c00df3d36061f2ea6045cac32d54` | 0 |
| `flows/01a05487/vision/flowMovesBetweenGenerations.md` | `093e1b214ca48f4f82891ec0f570d33a681b04b29813d8ca8d26a94e5e57abec` | 0 |
| `flows/01a05487/vision/skillEditProposal.md` | `494a7746b5be51a593f4b8a66406514c1c72abb57f9a131dbd432945a0b02343` | 0 |
| `flows/01a05487/vision/thinkingMachine.md` | `8610ab751bcffef766411cf6a30250e40acc7af3bb3f990c1d0d403a627ec32e` | 0 |
| `flows/01a05826/vision/flowIdentity.md` | `e9c05a4cc6eb4272a53054e12248b4c8e76b387ca3e9ca1d0692adc46ac9594b` | 6 |
| `flows/01a05826/vision/subflowIdentity.md` | `f101a3c873d600b27fa5cc79ae5260f4f603248d07f09eef688bc215b3e650b7` | 1 |
| `flows/01a05cd5/vision/birdProfile.md` | `0d74aba4df5610d6ea70daafe4a7598d8f1b31e702e861dc0dff1732b323bbbf` | 2 |
| `flows/01a05d17/vision/fullAccessPermission.md` | `029198c3556cf0978f5e4b96a7ca6fbb93c59972d4fecec746628fbe4db761ad` | 0 |
| `flows/01a05e53/vision/correction.md` | `c7c3f05057aff256a3dc748e742d9e7f61403bbc566b659799b6bff586e69743` | 0 |
| `flows/01a05e53/vision/hostTrust.md` | `8be42577eabab739fbda26a6356af2d70ddbcba28183955fe058d9bd8243ee83` | 0 |
| `flows/01a05e53/vision/nixExecution.md` | `3b54aeaf97bdd63048f061797ef5365f6a46d299d1cf9cf9aeb4a2626f5c4e29` | 0 |
| `flows/01a05e95/vision/flowSkills.md` | `d7f4b644bd34c6d41393b5806f55af404a051259c98a02ad68c7e984cfb39224` | 4 |
| `flows/01a05e95/vision/logging.md` | `3b3459f98ad1e54fe3b12d00b19438189a920244bac6a5a9ef3f746eebeb6911` | 3 |
| `flows/01a05e95/vision/subflows.md` | `e714128f4a3ac1c6e83298daa9a4aeb88a73d535e170c944835702c6581e1232` | 1 |
| `flows/024bc7/vision/bootstrap.md` | `ab32974e051ae80035bf3cef04770666b7faf8383a3001cf8d4b9da1120e4e90` | 1 |
| `flows/024bc7/vision/context.md` | `39cec7dc51688af82fa95e26d913cd9fdfa4859a6c2523ee2d09303a7be91f8e` | 1 |
| `flows/024bc7/vision/criome.md` | `adb0ebaa6a51ee68f1c3402a23d08616e53019d9586711a3025ab3f639211a36` | 1 |
| `flows/024bc7/vision/effort.md` | `f5b7a6c8b08f2110c49baaf454859c1c081649e341d45972b77a15c629463d42` | 2 |
| `flows/024bc7/vision/network.md` | `f3444b8d2536536bac1c60f2454140ee130d850e9381d7d6df2e166551f09211` | 1 |
| `flows/024bc7/vision/nexus.md` | `5c278a2e85bac957dba8b29a7f496a052300deb57831f3ae0952021c54ff41e1` | 3 |
| `flows/024bc7/vision/parallelSessions.md` | `02c73a2fd558f2e6b853a2ca0521fd2982aeb1165fd6488ffe880329d926c4a2` | 7 |
| `flows/024bc7/vision/router.md` | `03bd61b1eba81b20d06d835db66786208e70dbaa05fd37399699172df80fbbe6` | 1 |
| `flows/024bc7/vision/sandbox.md` | `43086b51aa99e9584aa20933d0b1ed379d41877d3def9835f04d6a9256cb3f27` | 1 |
| `flows/024bc7/vision/signal.md` | `4e377537659bf7d2cc89cc16b38ef4d202910dc4a9fcea21c4bc7ebad9ee19d2` | 1 |
| `flows/024bc7/vision/soul.md` | `d973104f5315293117c0f032910a89287ddff4edaad90a0ac276af4e3e5f693d` | 2 |
| `flows/024bc7/vision/speechToText.md` | `e9962a04f05c11514beef80f1d3a5c45e92aab6d25c60d7d8d1258766dd29a56` | 1 |
| `flows/024bc7/vision/storage.md` | `3104bce87b31ddaa6335d1b4dfc681cfb2ef0e65c70844fb95a9096094823043` | 1 |
| `flows/024bc7/vision/thirdModel.md` | `f4b3ed8b6f172947d428fdd66b88af91ab575c1d7427af2be31c15ffc36624ad` | 1 |
| `flows/024bc7/vision/webChatTranscripts.md` | `751c0b35b8b0d99077e86fdea79647c0962a72aeb3aa5912c5272abf32da50c3` | 1 |
| `flows/0384e0/vision/deployIncludesUserEnvironment.md` | `8ad243c4edf59115a39494bb8adf4b771d326b1868802f16291f795eb9585ed3` | 0 |
| `flows/04db2fd2/vision/artifacts.md` | `522d7f7def76dd8245ddb711fdad3f260712ba9a91752546c79aa2b01f86cdff` | 1 |
| `flows/04db2fd2/vision/decomposable.md` | `64e8b43c83be4586431cb1575a9134b48baf85667bb2ba6eda7731876c4f5eac` | 2 |
| `flows/04db2fd2/vision/delineate.md` | `59f2ceb88c6d0ae215fb7c9b5b8ad72e6ec51ce45a9bb342c6c3f36875a90dd8` | 2 |
| `flows/04db2fd2/vision/overtalking.md` | `32f6279e84b2dfe2399e3867551e4dd5ff4cfd1908ae723e861b572c94e3a317` | 2 |
| `flows/04db2fd2/vision/psycheLogging.md` | `cafb9abbbff5e7a6efca6d9b66dcdfd98b4efb050694d2a7ed2fa48397f91a57` | 3 |
| `flows/04db2fd2/vision/rollingDistillation.md` | `60e0c5ce6f22d89c76ae1a6e7f549e238a87afe424eac1a982baaf3c7e7672a0` | 2 |
| `flows/04db2fd2/vision/softwareAnatomySkill.md` | `13b07bf161e4b3c0d44f8a28257a434cc302ce4ee26618d69f16ac2acd373ec8` | 2 |
| `flows/056f6d/vision/messaging.md` | `09ea9479f49fe18e442b912ded7b2ba99c9322184ea231a45bbd9415a15f0655` | 1 |
| `flows/056f6d/vision/psycheGeneratedMessaging.md` | `ede3a3058d97d5173f4c6f7e1ed797bb6baf0e2d2d7de3055af5b8bb133e3244` | 1 |
| `flows/05c604/vision/cluster.md` | `9a57d66d767c82569ad35fa2a22aac3f8287dae585f3b035314933915c80656e` | 1 |
| `flows/05c604/vision/deployment.md` | `a50a5171c8b2f9d9e7c8dd2bfd9f27afea44d39aaadd510da800daf4e5048b7d` | 1 |
| `flows/05c604/vision/identifiers.md` | `5a9f015676b0f05ff624b45231aef70794f51cc72098c0d888ba1ab12bdc3e4f` | 2 |
| `flows/05c604/vision/launch.md` | `ee5a77f03233d539065c89dc15d389dde973559c376b6d5799a2dacf5a4cd5f5` | 1 |
| `flows/05c604/vision/layers.md` | `ab64054e59cb38b69a769b822ddfc302a5075af17fba7d5c6b5604493f369841` | 1 |
| `flows/05c604/vision/messages.md` | `7dadd1a40dec1aae62f9d29eeee36efb5760f0c8cdd86ff4167143e26be02e34` | 1 |
| `flows/05c604/vision/nexus.md` | `d5aafbc63aa7b90968ecb83951a871e2bb4a3c9dc5fb4a81dd2d96b4e5005966` | 1 |
| `flows/05c604/vision/persona.md` | `8b08311aac53a06f73bceba37a1ea49d91f7fac37d770ef0fa33181f3c0264e7` | 1 |
| `flows/05c604/vision/quota.md` | `acdb1e767d799ecda73e5b39e27fddcf504090543a833820caabad899eaa734b` | 1 |
| `flows/06196cc7/vision/codeIsLanguage.md` | `8355a4b74f5ce0f4cad4768017990306975f53ae7ef14bef9fa72092be5e9133` | 1 |
| `flows/06196cc7/vision/psycheLogStructure.md` | `798e8e0526ebb244f724d7fcc7634c6da8cf71b428f37990afb6bb7a65538204` | 5 |
| `flows/06196cc7/vision/threeStacks.md` | `1042a9a26cf8f16491555d8794dd4026364628cdfb7ba8d2a4c7aefeec7e2c28` | 2 |
| `flows/1030529c/vision/awarenessIsGeneralUnderstanding.md` | `70e1e8487dac0e8ed0efeb49582636fa90344751647d1825a0e24a3976760071` | 5 |
| `flows/1030529c/vision/flowNaming.md` | `4fce1345c8563a49e1c1cb3c5c865d106e2a940078d1f1c8c69837b6effe046f` | 1 |
| `flows/1030529c/vision/gradientsOfAuthority.md` | `873f916aeb5ba1e4d307f950fb09258f38d37f9e4b6c7c025c869cbd775c1f94` | 4 |
| `flows/1030529c/vision/psycheLogStructure.md` | `1f8449d6aac4caa65c24b739c4f64664dc275f6873c4b09903be3fe007da6d26` | 1 |
| `flows/1030529c/vision/workspace20.md` | `1f507567153719708e7a0f331b265c1ce2c7dc6349a87de27b01711a730ccdf0` | 1 |
| `flows/108ab0/vision/operational-abruptPerHarness.md` | `d5c3930b9ca5661990537ed1275642333f70e79290859af3f0ed3bdd98491e58` | 1 |
| `flows/108ab0/vision/operational-coreAndExtendedVision.md` | `e3721b422063da31498edb1cfd124a48d9451dc8634f6d74a1a205c1462ec2ab` | 1 |
| `flows/108ab0/vision/operational-curriculumAsModuleSystem.md` | `d481329b027e0cb25d0f62c3b87044f4e94f5aecbc5fa1bf748fc144119e4613` | 1 |
| `flows/108ab0/vision/operational-curriculumSkillsRepo.md` | `dc91e335b08f55240c4b64e8ca52f8a196b6aec7e0691d0b6fa0f9409f0f4bb0` | 1 |
| `flows/108ab0/vision/operational-designMosaic.md` | `f9308e1a04ba826b43083afd80d3add6a5f3001efa68d120dfb0cf577b778848` | 11 |
| `flows/108ab0/vision/operational-diskHygiene.md` | `1d2763775aeff749a2df0ff83082af69a9f63b97f6c02bce72701275ee4d40ef` | 1 |
| `flows/108ab0/vision/operational-distillationHierarchy.md` | `2f9773fb5b5aca658ef84313a691b3358f0286ddf63847e1cd26eb2d04514a73` | 1 |
| `flows/108ab0/vision/operational-flowCliListAttachProvenance.md` | `cbcc3a95e01097ff307f148408f5ade4987ed23663942f755337d21b207867fe` | 1 |
| `flows/108ab0/vision/operational-flowDatomLauncherLanguage.md` | `b1dd41367fb249ecfc198748384d86c090c54ecbd35dbfebb9752af0e56143e3` | 1 |
| `flows/108ab0/vision/operational-flowHerdrMessageTriangle.md` | `bcd3992c2354a53d0bd43e855e8f862a2fcbecb70fc219639cb4bc081e0ddd2d` | 1 |
| `flows/108ab0/vision/operational-flowStartsFlows.md` | `74f0521daad1ad3f202139fdfccc02788274d86429c70c52bebb658c69f46765` | 1 |
| `flows/108ab0/vision/operational-freshPrimary.md` | `489fa3bed5e8e07072084db4896001b537f326c4b0408ec20ca0a7e9b631129e` | 1 |
| `flows/108ab0/vision/operational-hackyMessenger.md` | `ddd1b7e3fc968121adcf7ad36c26dc0d4529ce602ab2f2a9b940636dfca74e26` | 1 |
| `flows/108ab0/vision/operational-herderMuxKeypress.md` | `b3cdc021ecfee6ec03c7a958cd271ec9de13c4256450abadd951ce630ccfc266` | 1 |
| `flows/108ab0/vision/operational-messageAsDatomInPrompt.md` | `8181504e013794f378f4c2a417c789fef2066e53e03a8d25d2317998e3844057` | 1 |
| `flows/108ab0/vision/operational-messagePriorityTiers.md` | `673e1a534ad7b136159b1c29b0d768cd5efc8d637d95996ac027f6ec44ddd090` | 1 |
| `flows/108ab0/vision/operational-mirrorToPsycheMedium.md` | `02a16f61d42eaa9d7c542f77c7dd2005889a871c09774c734c6d37eed6caccec` | 1 |
| `flows/108ab0/vision/operational-multiplexerInjection.md` | `70b0a9605739aedf90f1819c83f084b42aedda3017cec2dbbb6fec51d32ab63b` | 1 |
| `flows/108ab0/vision/operational-operationalSkillsRepo.md` | `97a04953a6dbb2e537a2e75057126a0ceab12bc3d283ce32cdc41689d9f270d9` | 1 |
| `flows/108ab0/vision/operational-primaryIsPsyche.md` | `32f3c367c5dece14b4ceea68be55882490cb84bc2cadebfb528ddcabb835de19` | 1 |
| `flows/108ab0/vision/operational-programmaticPromptComposition.md` | `f78b3e40a15683bb0505c1908c009cf5d7d671990d9b69656da0d84b7ebb9957` | 1 |
| `flows/108ab0/vision/operational-promptMosaicComposition.md` | `7ab1de0bb3910eb07de51ed629961a7243ff04fb492eb2d26e3bc8a034dd971f` | 1 |
| `flows/108ab0/vision/operational-psychePropagation.md` | `2603f63fb7443215bf2a908be5251d1ac3210ea4426fa5f15ccc68df98321d2a` | 1 |
| `flows/108ab0/vision/operational-pushMessagingForEmergency.md` | `783d748050ea794f81c168be8c5849f0b1affd9d908fa6e625f28e7f6b62fb59` | 1 |
| `flows/108ab0/vision/operational-sameTreeAndMerger.md` | `e8dfe2455921068acfc2b9e35a81f203f7fe859d1310928c797c8f2a45bb498b` | 1 |
| `flows/108ab0/vision/operational-skillIsVisionUnified.md` | `90430004a7054dbad2b9c07c64663d297ead53b38dfdb336f4e11089b7899469` | 1 |
| `flows/108ab0/vision/operational-skillLagsVisionObservability.md` | `8dd715e03b84d9be38d0deba8818521f4c7c66ca43ba42a8e8e6d71a4de771d8` | 1 |
| `flows/108ab0/vision/operational-skillTypes.md` | `8ad29b779395e0dfb623197fb16bec0d1a11438d739354cc3615eb938605e3f4` | 1 |
| `flows/108ab0/vision/operational-skillsAreVision.md` | `0dee64ca5c86b9eec6c9b3a945109dcf6f15d6f17a9018ce1c655885347100bf` | 1 |
| `flows/108ab0/vision/operational-timeBasedMergeSlots.md` | `4fc8d94e149e5c75f231ae8bbaaf02d122c68801d9fb7a55e425f2feda5969ab` | 1 |
| `flows/108ab0/vision/operational-visionIsSkill.md` | `8663bf3488f4e9141b9a64c1618a2d9ed329933c36c7b81e2b67a2e6d3da9db4` | 1 |
| `flows/13cfc23f/vision/testTravesties.md` | `9c6de3c062f4991a12fb63dea9c4538650a7b35d87a8b24d5966f465a1d58f00` | 1 |
| `flows/13cfc23f/vision/threeStacks.md` | `f93faad1001c9c7ee835e6600bea02b817f850bbce72a4bcaa8146799d9642d5` | 1 |
| `flows/15b67974/vision/actorLibrary.md` | `c9986bcca9d55d85d6507734f28f3b027b901fda6129809baa0f7e03d18425dc` | 0 |
| `flows/15b67974/vision/domainKnowledgePlacement.md` | `cf8d38bacebf386730c200f51644a19d6f2deddd3056f4f1735c4e3e23f3da8f` | 1 |
| `flows/15b67974/vision/entryFiles.md` | `5e0b9bb7166de60d6315ea529feaaa5a9e5a0e28d81e9165c48fe4a6379e6ba1` | 1 |
| `flows/15b67974/vision/flowDaemon.md` | `fba89c8d1e815fea9c8f1a814b146b3069dd5bf3cf2f492a1eebed2007993cfb` | 1 |
| `flows/15b67974/vision/flowKnowledge.md` | `e12468450f89666ce512d008de2df201b59d26690c4995d8d8f4549f0c844d98` | 1 |
| `flows/15b67974/vision/hexis.md` | `118ac0621c53f87328d20d2ade031ef5b9aef8e2b0126220636c56a94d259eb1` | 1 |
| `flows/15b67974/vision/letsUseTheSameVocabulary.md` | `8b37ee03a98add3748a2b1f7b8404a1e2a4d7ca7a1114e0e9f60b4bee7f09ef5` | 1 |
| `flows/15b67974/vision/persona.md` | `f6fef950763c71cc7197875051e541976bf4b58d71b91dae3ef033ca140fe202` | 1 |
| `flows/15b67974/vision/psycheLogStructure.md` | `2cd0ff7d78e4e18cf3ed640e3e158fd90586bf275cd20c4d00f2314cfbc8aa96` | 5 |
| `flows/15b67974/vision/skillDesigning.md` | `7860a7e65f649cef9fe75a77f3cacc4e78c3cbf620d94279cc92397404ef0de8` | 1 |
| `flows/15b67974/vision/skillsRepository.md` | `4985d9de9e76f29d6b316dd637349b38bc983a52c4f9ef735dc49154170ed198` | 4 |
| `flows/15b67974/vision/worldModelBeforeCode.md` | `23b4ce57259539dd81eb0f72e8b178bd1b2b1d6737e51fca1187752ff1b1e2ab` | 2 |
| `flows/162eb3/vision/subflows.md` | `e84302f1663cb10bee18963b0d0ab1fef0782fcfb78c3403e5b2ff31573d94e8` | 5 |
| `flows/1a6ca4/vision/flow.md` | `649e2b07d00cf50cd4d6b3960310145753d61762280f6a75b28d79eb2f3d231e` | 1 |
| `flows/1a6ca4/vision/mind.md` | `8cc83d3e3c593d7fcf84354effafdd865de43bcd4160f37d8d8a15259158ed32` | 1 |
| `flows/1a6ca4/vision/personaMetaHarness.md` | `d9383276644ec24a4d344a28b2054d9828ac1203cb0409673b2f7153b0e1de58` | 1 |
| `flows/1a6ca4/vision/psyche.md` | `aaacb9566e0bc11c9a948a8e05f6c9ab102c428bbead2de548d0e374e5c83ab9` | 1 |
| `flows/1a6ca4/vision/thinkingMachineProcedures.md` | `20b56ad7117573fe01241ab996809a50b15e72eb9875fdb7fd92d0dc1e766db7` | 1 |
| `flows/1ac573/vision/operational-agentToPsycheMessaging.md` | `79ade03f32d12ffd1690834806d3b3b23c93a288edd9bc8cd6469c4b172af99d` | 1 |
| `flows/1ac573/vision/operational-commitMessageIdentifiesEpic.md` | `4698b6398b3461f9bac24d1bbf0d12bf8c7636c27adfbe8d31fefb5432f633d9` | 1 |
| `flows/1ac573/vision/operational-defaultModelPsycheMediumClaude.md` | `d2ba50a099a2afe76b49c2a264818ef8915056d05fccb78ac9c85c2634af4de5` | 1 |
| `flows/1ac573/vision/operational-effortIsAlwaysMedium.md` | `4c2f9a78fc53c7847552c2fb2aa7a1840a2ecd7f49317e719bebb0ec9688f6b1` | 1 |
| `flows/1ac573/vision/operational-fableFlowAndOpusComparison.md` | `bf5f05e911f1774231e1aa8fd816138e78ce043768e3aeeeb6b60723b1fa4a7e` | 1 |
| `flows/1ac573/vision/operational-mirrorToEveryoneAndRoster.md` | `93b7e90b044d1962b2771c9ae77fe725765498acdc0ddf6fd4f545b0fa6402a4` | 1 |
| `flows/1ac573/vision/operational-mirroredMessagesAreAddressed.md` | `311f86b2b7689dcb7e7c912d6225b0815ad06b486b37a47edd8d28e6f0064af6` | 1 |
| `flows/1ac573/vision/operational-modelDeclaredInOnePlace.md` | `61d25ea9dcc67cd7b83f763b1bbbd716e747481b3ad1103e0f4cd440685f5b43` | 1 |
| `flows/1ac573/vision/operational-modelRoles.md` | `b2f8a56b7cdcc341a219e6ed2d329e067f7592b6a6730c01fca14252d651ccf4` | 5 |
| `flows/1ac573/vision/operational-nameSessionAfterAncestor.md` | `3226fe6a9fb0d1bb9030ce68762594c763c8deff5848bdb159bb3961d76b7e46` | 1 |
| `flows/1ac573/vision/operational-olderOpusIs46.md` | `5a5542b3fe215f6b041edc5db457407d0733faae10b2acf7bf47d0f5be6b1f3e` | 1 |
| `flows/1ac573/vision/operational-ongoingAstraOpusInterraction.md` | `11edcd6b8c1f47c8e5f9a9640d01827eb7252133d9f67c9cba1284d410af2c7f` | 1 |
| `flows/1ac573/vision/operational-openStackOnCodex.md` | `c3b73ca7f3658e5154af97d297364a03ac3e15f9bb0287e506f2006977a25457` | 1 |
| `flows/1ac573/vision/operational-populateIntentWithTheAutomatic.md` | `137f70bd7dc45fdae6cd99721662a1792bab6f8c9edccddd4ad94ec28858c888` | 1 |
| `flows/1ac573/vision/operational-privateLayerCoreLayer.md` | `53d7d23343cb9f9e86390592863fa84543a703dff64a9ede72262e7ff3cb8711` | 1 |
| `flows/1ac573/vision/operational-psycheMindAstra.md` | `240f68862ec413d2855f45462d430747046a57ed8b152fc8e70d3091772f7974` | 1 |
| `flows/1ac573/vision/operational-reapAndArchiveOldSessions.md` | `f42e34ee28a00a986355373d96070583e139ef857f93cdc80ba168d87138ccdc` | 1 |
| `flows/1ac573/vision/operational-reapReplacedSessions.md` | `5d0ff3effb36c8a5e2c005a089f1ccec5bda5815dd7cea00393da4244623dc71` | 1 |
| `flows/1ac573/vision/operational-reaperIsForensic.md` | `56418120ac80b49d9adbb621568f2f80c288e61ce1eb2ef714cd78693ab64529` | 1 |
| `flows/1ac573/vision/operational-refreshKeyProgrammaticallyInjected.md` | `6ce25d8431be3dfe2b73d757224f660c58517aa6b9964d50f05050f4895a6b7a` | 1 |
| `flows/1ac573/vision/operational-reportFlow.md` | `6e83fe8f7f8276ce5be0836afb82c0f9d56d5502fecd6434e27c91a1f67f8c06` | 1 |
| `flows/1ac573/vision/operational-testTypeSkills.md` | `11b6e2533f2d9b9ce95fc46d2294a96fe645928857e62438a16e9ea02cba7081` | 1 |
| `flows/1ac573/vision/operational-visionLedAudit.md` | `f22a062204efc302f7e7b8f27f1c8575edaea06390d8f934d790d5b5674b54cf` | 1 |
| `flows/2b34fafa/vision/importResolution.md` | `eb50e738ee0806be24d35d0d15b10cdf6ff5d69c1eb9e7f035bdfe83a564eed5` | 5 |
| `flows/2b34fafa/vision/protosIsTheSharedStyle.md` | `28fbc3e1207014b91250991d77639234935d7d9f66c24e0b3aa66a05a4cf4490` | 1 |
| `flows/2b34fafa/vision/rustComponentArchitecture.md` | `78eca1bdbd3c97b0da89e936159efdf74887d424b32f70e2b7380174b9cdcfa8` | 4 |
| `flows/2b34fafa/vision/sourceNotCrate.md` | `44e06a4a94ae55e5175803e7bfc10bb84a3f977b503b3a07a361b8d65ef3ac96` | 1 |
| `flows/2ef42163/vision/psycheLogging.md` | `a23cb632cc259d1db3e22f8dc77ca51a3c062a84eb35d7ec97747424b12bfc36` | 1 |
| `flows/2f6b1dc5/vision/contextStrata.md` | `37a5c3c129d2e08188848c9e5090c8b32d85168cd9907f3707d59dd611653aa2` | 2 |
| `flows/2f6b1dc5/vision/systemPrompt.md` | `6709320b5c27f8560b620be24288533fbb9bec4b41546461c1aad102b23c0685` | 3 |
| `flows/2f6b1dc5/vision/vocabulary.md` | `f87edce397af45a75d58a8e46e03bc4ccf33456036a1d14b88c118ea1ee1741b` | 3 |
| `flows/33ba2b/vision/operational-fieldRefreshSuccession.md` | `bdbd21bc9a1f4c8255259477117a0421ad07ce7aaee81684523fe6e719ae5ff9` | 1 |
| `flows/33ba2b/vision/psycheDataArchitecture.md` | `b87184227dcbb3ae41cfb8f5a21ff35badca185fa1c02c67092571ebca3fa4dc` | 4 |
| `flows/358f143a/vision/awarenessIsGeneralUnderstanding.md` | `8ce2a4a0d854c4aea7a3258ff9b7cd66bc1230b6a500b2b0349c160f14426777` | 1 |
| `flows/358f143a/vision/behavior.md` | `0290f542e518362444423dc53704c14a30a0ff9f3ae638c1318e0369f91056fa` | 2 |
| `flows/358f143a/vision/entryFiles.md` | `6a2b80f988f414c296415e97b73b22cbc6d03d2246696373b3f5353bd6d76825` | 5 |
| `flows/358f143a/vision/falseConfidence.md` | `382ee179a524767100b17218f7f797ac189d6823565c39968871ffc4e5da008d` | 10 |
| `flows/358f143a/vision/flowDaemon.md` | `0bf11232a162eb7339db44993a90f011d2ed0ef4e074ab03b0ae5894c0d3b69e` | 1 |
| `flows/358f143a/vision/gradientsOfAuthority.md` | `b7c8bc65366451610e65efc0853e91dbc78a6758788e0fb1c6737eb2e705fdf8` | 3 |
| `flows/358f143a/vision/letsUseTheSameVocabulary.md` | `20150ce88af339fcbabb1bc99eb84994bb1e6c7ca049dae3a0ea37d0b47bb742` | 7 |
| `flows/358f143a/vision/managementDelegation.md` | `25ec6401429a6a8706b426ff8f6f8a1a601bc722fd0230a6edca058585386b06` | 3 |
| `flows/358f143a/vision/realizer.md` | `69a8f5e45fa453042db7ddd40a1f1b019618da094269b22587f97391bd1ab602` | 1 |
| `flows/358f143a/vision/skillDesigning.md` | `dc6e4771ffdd3628dcdc3bad43ec86efe413b00bd6bd8a7879973daa0c546313` | 3 |
| `flows/358f143a/vision/skillVoice.md` | `5c4d8e1ad6682192120130187f14103bf6efbb8eb51eb19377fbe6d47fbfd5b5` | 2 |
| `flows/358f143a/vision/skillsRepository.md` | `25d02ad30c4355bf8c8293a3140ae3561d9b09742405f0248fdca9934e9f15e3` | 1 |
| `flows/358f143a/vision/trainingRepo.md` | `8aad15a11bec9230b2253f93df8de9d0438ed67a0504902aa549d59776d5aae6` | 3 |
| `flows/358f143a/vision/workspace20.md` | `babd2ec45c7ac7e3c63128172a3279e92d880f0d718058759d2a4dd5a4c62058` | 1 |
| `flows/38dec9/vision/agentToMachine.md` | `94c28f0014fcc6cf48a29c5603f543b3ba86635210a3998a51b8cd28049321f5` | 0 |
| `flows/38dec9/vision/deepsekHarness.md` | `9349f45505af639ecf3e1a330be5997c04332e0fcbe9f0b871e9573b139d57aa` | 0 |
| `flows/38dec9/vision/harnessVocabulary.md` | `b57af83842e146f85b90abe73325f3bff5499aa8d88601ed38d084e3518e31ef` | 0 |
| `flows/38dec9/vision/invocationSystem.md` | `31b875063d2f02d5eb09b07dbd3fe554314e1014dbe5e60ea818f7bcf410e995` | 0 |
| `flows/38dec9/vision/perHarnessSkills.md` | `54b46f0b2e665b79655ec455cccaaa054c3877f76f98a13a7a9ce69c417a6732` | 0 |
| `flows/38dec9/vision/piHarness.md` | `2fa95c5409bb44b09674b1cbf9d47939379f27b63d1f67b1382464b5c27805b6` | 0 |
| `flows/38dec9/vision/skillLandingBySubflow.md` | `375ee28009fccc458249574e98e99ffd64c8628ceaf9c36680a08c19bd2844e4` | 0 |
| `flows/38dec9/vision/systemPromptRepository.md` | `d094f10be60ce8ee47a510901361408038c75ac64f41db2f70d371ccea373c89` | 0 |
| `flows/403a1a/vision/flowLogging.md` | `941ff746b41e020f465fee1a13df1f602795136f9dda757678e0cf452037a527` | 1 |
| `flows/4647d2/vision/listenerWisprFlow.md` | `13097de43286cfdea8626e0db78eb8b0c2cab5b87d45f63bde382c3829af981e` | 2 |
| `flows/4ddc321d/vision/contextStrata.md` | `98d41f028bcd89e5d8698f10033ec7d4ec1d18ec62d00b3f292f4423d79502d7` | 3 |
| `flows/4ddc321d/vision/flow.md` | `b3cac7e65622d42346e437247e043387ff6285f828629b2504df64e1a1f1020e` | 1 |
| `flows/4ddc321d/vision/hijackRepositories.md` | `b47a8e086422e2b82c2ec36967dbd5ceeddfce197eae0c5b49455c8898d844f5` | 6 |
| `flows/4ddc321d/vision/skillDesigning.md` | `0ba546913a166ded964fe36a5b346b41b162fe0c90fb5fe87a2e9d395a62fe27` | 1 |
| `flows/4ddc321d/vision/subjectivity.md` | `39746eb90e6fc901bacc0d085afab5ad3c450f63c4d3ab43050a3446629f60d3` | 1 |
| `flows/542442/vision/node.md` | `2c92850590c4893cd6f6d813c7fafbc234975844590c77802b05a48c13062349` | 2 |
| `flows/55d18f4f/vision/everythingIsInTheDaemon.md` | `48908a92e087c696c63c5cf6c11853fde0ae03632ad83c33760f96d0494cbd75` | 1 |
| `flows/55d18f4f/vision/highLevelView.md` | `6f136a2d36ed3457bd914d557106ca10180c3640eae91b5b4ed52dcb2fcc9d95` | 1 |
| `flows/55d18f4f/vision/itsATranslator.md` | `59f6616d365e9f4e800c306f62487a06d2410672b87ee7785c04d1b75929c312` | 2 |
| `flows/55d18f4f/vision/majorRecoveryEffort.md` | `5692e241439855042ab18368a97d9780aee9aedb1adb6fd5b19c92e1eb05ab57` | 1 |
| `flows/55d18f4f/vision/minePreResetForImplementationStandard.md` | `4d0895f16bb29a81867b218fda63afdea75daf1d161ec8ac47e0200c4a794bfe` | 0 |
| `flows/55d18f4f/vision/rustComponentArchitecture.md` | `4f5606645618418335c5571ce1b88c1135aa1d5b616161058990c3637f59888b` | 0 |
| `flows/564f55/vision/datom.md` | `d85dff4adb583d7deb73d2bebba42ad6a8ddbbb34c8433d424f2ddfe6dd4bce9` | 3 |
| `flows/564f55/vision/designPractice.md` | `15fbf34774358728a0019edbe0062c339655fc06bb736f16478dc4758be164f4` | 2 |
| `flows/564f55/vision/ethos.md` | `b295786d3971d9fc0d478eda2312f33449a556b39edf2729491085c9443b7855` | 2 |
| `flows/5851f4/vision/anatomyOfCommunicatingThinkingAndReacting.md` | `d9795465847c759d41b770ff77e4e2372d5b3b13d6e4f7f9868bcddc78713e15` | 1 |
| `flows/5851f4/vision/ashtadhyayiKnowledgeBase.md` | `5b26f89bacd46f315ccd6fa52f803cdce58f5eaf0bf9e85cf11c0477e97ac5f6` | 1 |
| `flows/5851f4/vision/psycheFacingModel.md` | `740f47e3afdde911389d96268c1281d377f3f8e22c71d83f19140c25fab9761f` | 1 |
| `flows/5851f4/vision/skills.md` | `1ca974bb3488e3b11fb81dc5ac3296f08152034d7d3817f654d1c27f5a74b8c1` | 1 |
| `flows/5851f4/vision/subagents.md` | `ea608e501a865f367ec1ed11625f0db639b9456502e53a3dd7c601b3dd80f6cd` | 3 |
| `flows/5851f4/vision/thinkingPhases.md` | `1235678a1e81d04f8f403096127d1d8af4935efb57fd1587b3d8117042730f04` | 1 |
| `flows/58a86d/vision/claudeDesktop.md` | `b94971265312ca70a14f1ecaf9965164bf1bad19b0ab7f8659ad06455d5db901` | 1 |
| `flows/58a86d/vision/codexModel.md` | `d8e248ecbb9336ff88bba052f99675de65269510b4f92718e82e2711a140a002` | 1 |
| `flows/58a86d/vision/subagentModel.md` | `98042d90c0edddf7a753bdb3fdf604c836b463f9d87a64d7983300631310fbb3` | 1 |
| `flows/58a86d/vision/visuals.md` | `feb3015f4701803f05340d9326bd9841fc54f0135763dd03fe086140652c2abb` | 1 |
| `flows/58a86d/vision/vscodium.md` | `665c852d86642a87cde751ffbff9dc73ffe5f82838c72e20953f79ef6636c292` | 1 |
| `flows/5a3ee4/vision/pi.md` | `a4af5a5dbed2bac39cd828835fa032d56e50e72e65f72d41867195e5f2d244ea` | 0 |
| `flows/5abf3be8/vision/chainedNamesScrapped.md` | `42a27c40f7f674385dec8014a9570545825deb652614cfcda97be52b8806ebc5` | 0 |
| `flows/5abf3be8/vision/disavowAuthorNeverWrites.md` | `7e3d04344ea85116438afc9be34d87604ea501a36a9619875a189c7608d925e3` | 0 |
| `flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md` | `45c6dcf81b000ed3e6df5aaaebbc6acda85f5b57e289e16012623432e7b44a8c` | 0 |
| `flows/5abf3be8/vision/letsUseTheSameVocabulary.md` | `d4d950fbd5bbaadaf74cf4a362249fdf8ede4e92586a9f39dbbc2236d30c4337` | 1 |
| `flows/5abf3be8/vision/replacementKillsOldSystem.md` | `1984ac417aea4a8f2251891453382667eb9e697e9bbfb5909ff97109a45fb2be` | 0 |
| `flows/5abf3be8/vision/sectionsExistToConferTraits.md` | `84ad2a0ee6367b30df01d6730e9e14a9acd29fd3ba10f9175b557f1861e3909e` | 0 |
| `flows/5abf3be8/vision/streamAsFourthKindMvpFirst.md` | `705e00ed2c7638b3ea4f88cac1201d9e54915db7ba5fd35fba08b96b8f98f12b` | 1 |
| `flows/5abf3be8/vision/streamDisqualifiesBundling.md` | `461b52b74b24ff7792c2a0d0f233bee7ce5d642bcb164eb017f1f911a56d06d4` | 0 |
| `flows/5c8be3ca/vision/flowArtifacts.md` | `f3a3425d91573e9af3236b6cc15ec06bebbd3af0de9ae9b692d0720a629c2908` | 11 |
| `flows/5f4fea/vision/quotaAccounting.md` | `82acb1bc6defb48d8af74e23fd005f9211a1ff1097450949f22b79370047cd02` | 0 |
| `flows/62022e8f/vision/designPractice.md` | `77f9b941792ebfbaccccdce7c395514e21a75df986131392da8a3c7791aaf5da` | 4 |
| `flows/62022e8f/vision/distilledVision.md` | `0df88cb65c74f6344ffa0f4b26f0b27a5d891753e3b8b05cede3eb7200e5df1e` | 2 |
| `flows/62022e8f/vision/multiFormConcepts.md` | `662a3bb043733491ec872f61adac6205ef26bd2e7375edc96b5ae3e7b29418ef` | 1 |
| `flows/68512643/vision/negatives.md` | `9300d14480747e7e39683cbe3fa5da3dbc4cfca3098ac729a1744f7df7da1e89` | 3 |
| `flows/6852f4/vision/communication.md` | `90c539384a7c0a4c32ac8b7a37806b249959dd842a8e873f414cac5daa14ec11` | 1 |
| `flows/6852f4/vision/flow.md` | `22497e9110eb8d6f333be17fe7732de4d4f654f95cb6f3b9d561f672cd6e8471` | 1 |
| `flows/6852f4/vision/versionControl.md` | `3d0af5477fb68397aef8fd7f1fea6870e2b2543e045dd30f0ccf63ca4f8d8ea7` | 1 |
| `flows/6863ef19/vision/codeIsLanguage.md` | `f3afa0aeee198ce3d5fc2fbae22c3411ae87bb31f0e6bf05d3e055c42fbe760b` | 1 |
| `flows/6863ef19/vision/encodedFormIsTheCode.md` | `a7846894d47c87c1db8f8800e945dbef4281bfa6be886b6dc82da5ff6de63051` | 1 |
| `flows/6863ef19/vision/gradientsOfAuthority.md` | `99e21a8193209791683e30f17da5c2a7267dbad645a9d1cdced455b2279b2d01` | 2 |
| `flows/6863ef19/vision/signalIsOurMessagingLayer.md` | `60c7b0d9d212d1b420a114af1fceac9b1dd25c7f9ca9426153f6ed01127ccf14` | 1 |
| `flows/6863ef19/vision/theBestShape.md` | `c99862c9d65c3e9c5c0105262bf0d53aeef71049dc7e136213a2c3c18a25e9fa` | 1 |
| `flows/692df8/vision/ethos.md` | `6d7b81e2a74a5de0071f40fbc973f800f6e2bc4f24fb7d3fe22aff580c26eac9` | 1 |
| `flows/692df8/vision/flowLifecycle.md` | `9516b22a35fd4d69d94fed860d792176ac015adf99fb66c7245b34aa2b68fea4` | 2 |
| `flows/692df8/vision/identifiers.md` | `59977d710a2f9bc1f5b745517319373a426325d8e3cc5455aac5ba0ac0391578` | 2 |
| `flows/692df8/vision/logging.md` | `3c463188ec36f195f60b15939edb46580293cdd8a6080980b39b12a962ad3084` | 2 |
| `flows/692df8/vision/messages.md` | `c3456589af3840531cef6712a58630dd3cf34d67a1d4bcf916a3b10fff286125` | 1 |
| `flows/692df8/vision/pair.md` | `a8ee1e1a7bd55e815e49f57cca50cf83e6a4acc0ec5c35def3c3a1231e6b0cb5` | 1 |
| `flows/692df8/vision/quota.md` | `c373f81cb9a400b9b8a25471456c9127aa07f636de48be52ae5f8892f973fa29` | 1 |
| `flows/692df8/vision/relay.md` | `867354e33f198ab1044ad43662cace6e0ebcb1c4c665f0e96191f7643d8a02f8` | 1 |
| `flows/692df8/vision/sessionNames.md` | `319dad809141558645e958643248d13ab4fadd31b3d95c3c1398e62db84ab0d6` | 1 |
| `flows/692df8/vision/signal.md` | `0d5167cf6103bf9b35689d92203d9c1748462f3f9e8820388d855d58d5a88756` | 1 |
| `flows/6cc91b/vision/agentAuthentication.md` | `c5165ee168a1846b1fd22742fd8afed365669065ee3f9f354faa543f3aa27b58` | 2 |
| `flows/6cc91b/vision/billing.md` | `a93d3a603ab39abae4a672880fc8aaca1f8ebaeedc369e4d652eb9426d8e0354` | 1 |
| `flows/6cc91b/vision/criome.md` | `0b16206f199b17a90d7bf74cc086d667381ecbfd4ce36e46cdbeb5d108e29279` | 1 |
| `flows/6cc91b/vision/flowLifecycle.md` | `6c96752b825aab80dd296f64dca67fee0b5fccabccba9b8ba73782656af364e8` | 2 |
| `flows/6cc91b/vision/forge.md` | `00f80c01573976ee56e41752a0d356339feec98cc7b62f2c3b9a7a3f5a497183` | 1 |
| `flows/6cc91b/vision/interflowMessaging.md` | `bff7d052f1103ad32f2aadf88d57367153315ad07dc883bb0913ac1c1e2ba0bd` | 1 |
| `flows/6cc91b/vision/law.md` | `97dd615ac36ab1f6b9cb95e26b8bd95a8edb423126e3bdb5587aeaab7f639aad` | 1 |
| `flows/6cc91b/vision/layerZero.md` | `925cc722f2e897362e597257f85e55450bfcac98f74ba3c4d38b2e5d50cefa0a` | 5 |
| `flows/6cc91b/vision/mainFlow.md` | `09abab9b2fb44a2f3a0b17cbbf69695fd0c9168ddc8a3fe47b4f795ce30a9531` | 2 |
| `flows/6cc91b/vision/messenger.md` | `4bdc35b30b28e157ab7f3dd2b3e167a3f5068774d99c064988d883871b0352c0` | 4 |
| `flows/6cc91b/vision/migration.md` | `ed12f9059fd1b87e457e40a31f5272ddf8f26bcc321278cbc1bf50db0a981cf6` | 1 |
| `flows/6cc91b/vision/network.md` | `16b78cd60b766bd2eb39628a464d67fb0ca76917e8e1d3127cfabef625987d1e` | 1 |
| `flows/6cc91b/vision/nexus.md` | `33410e0df4b630ac8c9dbd70f60d72b50b707c91d8c17220ccbb7e2394bb6e53` | 3 |
| `flows/6cc91b/vision/notifications.md` | `3fe596dacbeac4d4253be9cf3b51ad632495496d5d50e94d87e6e570cd8cd9f8` | 1 |
| `flows/6cc91b/vision/openSourceHarness.md` | `838957a5b8c5545747abe3b88a313f873159b63f598677ea863976076953ec24` | 3 |
| `flows/6cc91b/vision/openSourceStack.md` | `0c1f17c8503e31a91af2987d10e60ae4f40a5ad7f08f84b73ec958e8e5b42eba` | 1 |
| `flows/6cc91b/vision/pairHierarchy.md` | `fe17719f740d3bf558ebe89e93053b8011e3bcd128e51a88e6dfa2bb32fe4e95` | 7 |
| `flows/6cc91b/vision/pairedFlows.md` | `7823a5631b9b28b9f6bf8946fee60ec4f2437ffbeb1c741c09e581a42637f6d4` | 4 |
| `flows/6cc91b/vision/privateLayer.md` | `8a4826684f08fe23600c6c8f9b8c3b8e00f184e9555ee23741cc1862912b7708` | 1 |
| `flows/6cc91b/vision/quotas.md` | `f895a0497d7266a04664e078873d47e9d0d9a06fbca28806f1173ba48bbad1f2` | 2 |
| `flows/6cc91b/vision/relay.md` | `c0d5bdee83c45ca03fbbf118f46e6c7baba8e9e164c0ac3bfb1ac9f20c51bc99` | 2 |
| `flows/6cc91b/vision/reporting.md` | `e450e77134763743d820f90ac3bae7139460528465232784302698c805ab6952` | 1 |
| `flows/6cc91b/vision/rustLayering.md` | `8dc3c5b810ae10ab16bb96302d495b174f70f4aeff4bc36e247d26adea2a255a` | 1 |
| `flows/6cc91b/vision/sandbox.md` | `47cdc823d27431e86b1b106383cec9aa2778dd589873bb16a2023638c1acb45e` | 2 |
| `flows/6cc91b/vision/secrets.md` | `7e95008c00daab3c2581cc1af1706572c92128f7e3f6c969d34f535f8fb8629b` | 1 |
| `flows/6cc91b/vision/seeds.md` | `e2c048d99b20996216295c2222fb01e333b4137e14db5981a8acbca815dcfced` | 1 |
| `flows/6cc91b/vision/sessionArchiving.md` | `0dee7bee4d408291fbfcf4e12b62cbeb1bf86539c8898b5776a89b0139b0c6db` | 1 |
| `flows/6cc91b/vision/skills.md` | `11ebb684108ee90474abf3fa25c4bbec503a9ea3fef941964d2f9d149ada67fa` | 1 |
| `flows/6cc91b/vision/terminal.md` | `4f192daae66784ca4e67799fea1a70a8adb454fb6d32974f6e0da0da80e6ebda` | 2 |
| `flows/6cc91b/vision/terminalCell.md` | `c48389aae16820119c601b85f5e9be786e7726973351fb4c20b61c6fc2f5dd8f` | 1 |
| `flows/6cc91b/vision/thirdModel.md` | `f23c332f1c517f45e7780bdcc3b449d55842b0c7066b54d4d5db6502daacde18` | 2 |
| `flows/6cc91b/vision/transcriptExtraction.md` | `813ed9c7d7e049f3bd66e9d089076d698f0306f0610308f393536d5b5ccae7fb` | 3 |
| `flows/6cc91b/vision/typedPrompts.md` | `196734b3ec7bd28348cc0644667067852aadf35ff0c4e5d22c8b96ae60fce78b` | 2 |
| `flows/6cc91b/vision/unity.md` | `4f12d5333c68be82e852755222221067f22f169516434916bd17ffc3dcc616ec` | 1 |
| `flows/6cc91b/vision/virtualMachine.md` | `b21ac98bc1643ae1deb47a28bbffabc2881932d20ed4ba74fd8dbbc008b2ca17` | 2 |
| `flows/6cc91b/vision/webInteraction.md` | `6fc721f53713712251e9af21cb29f1a2cbeae55ff2c1bb002ec92a4e3d9ca7cd` | 1 |
| `flows/6cc91b/vision/wisprFlow.md` | `c109cce21600637b81f763326ee14335fd74383be26f74200632eb2a3e4355b1` | 1 |
| `flows/78c93c/vision/machine-generated-content.md` | `dd0020ea268f8e4065eb8ec80508a7ed71b40db5d843ff22855897b0226b3892` | 0 |
| `flows/78c93c/vision/witness-reuse.md` | `50c1e799f1b92dc5b86d0e29c9565549698a23f243b69472e62d16fc73921371` | 0 |
| `flows/78c93c/vision/witnesses-and-reports.md` | `6a5420186c980ae422202e76217cf41d62f1388b45715e521c1783857d061203` | 0 |
| `flows/7b4d4c/vision/flowArmsItselfToWatchTheArtifact.md` | `ffc22f48bdeaead07f4e4897e0c152eaa3e59ef423a39097145da51aa9dcce84` | 0 |
| `flows/7b4d4c/vision/shortTermFixNotTheFullJob.md` | `238a813969f2e4b50efefee98fead5e358db23ac140b04addaebd4304fc66f47` | 0 |
| `flows/7c3f0c1d/vision/gradientsOfAuthority.md` | `a9d1496d7dc689beadbfda3bf54e7f7e770b8dfc8d21e3a63e5197b8b0409f1c` | 4 |
| `flows/7c3f0c1d/vision/psycheLogStructure.md` | `35ff1794d7364a3fbb108e9ad3fdf5fe1d8d72936158fd9519088a686a5285d5` | 3 |
| `flows/7c3f0c1d/vision/roleDescriptions.md` | `4b5b0dd57b6783bc6cd93776d03fc12d67b84bfd721848ee69dd21d00aa590db` | 2 |
| `flows/7c3f0c1d/vision/sessionLog.md` | `c8ef6497b6580fa75d0f136530d0c12f85cbc3c528196e36e47e8af87d5be0fd` | 1 |
| `flows/7c3f0c1d/vision/testTravesties.md` | `044af0cdae75f38d07c65ca73b9a2c072b704a544099266f6bb8dd045e67f9ea` | 1 |
| `flows/7c3f0c1d/vision/verifiedInformation.md` | `93b8664e4091c8288db54a07f7e7b9ca721cb6f1b2c319ed643475515a5a0e65` | 2 |
| `flows/7dc7cc/vision/redeploying-the-operating-system-after-a-user-is-deployed.md` | `e5a3b3b1db7eb38571ab9c43141d0cb696c4fe99c99cc975529d07d22a8eaf46` | 0 |
| `flows/7fba5f/vision/annotation.md` | `52df895094427b2cb368b4ab9c8e10311017d6f6bed0da51f8b75137fc6c0a8c` | 2 |
| `flows/7fba5f/vision/harnessSkills.md` | `53fc58c85f12d5e7717d62c9816bd9e592dff82ebcff4484a51446e7e4940a18` | 1 |
| `flows/7fba5f/vision/mainFlowWrites.md` | `0aa184eb0fd1682f0d9ebe7132f8c7cc31b99d735a453d5a4cb1c4684aa43362` | 2 |
| `flows/7fba5f/vision/reporting.md` | `3c74b5d43138b1c4184020ee56f794d50c296dcd8a59ed6b27e6af2c214c361f` | 4 |
| `flows/81c0dc/vision/wisprInteraction.md` | `bad58cbb718c32b8460c434add4488f61734136a13ee259a46ee116c9d4489d4` | 0 |
| `flows/8325c1/vision/audits.md` | `21b2f7637d72c365085278d568da98db4440d9e2573bef35acfc000b0b28e175` | 3 |
| `flows/8325c1/vision/ethos.md` | `4336ae2311e3e5b35798701cf9bd5b5c83611331c560ac9a9079140470342a02` | 2 |
| `flows/8393ca/vision/operational-herdrVoiceAccess.md` | `447971144324894ae6a1b6c5f08ec37df0a69f9aa862f0a7945fe4e30cb9593e` | 15 |
| `flows/893603/vision/claude-persistence.md` | `f4fc8449d1ea65423d30027ba9ee248fee3483578a7f2791be930ab8f9a6dde1` | 1 |
| `flows/8a5caa/vision/codex.md` | `7063c5b2f40b9258391bc4ece76bb05fb37b1390d79036613d0c543bce81345f` | 2 |
| `flows/8e9e77/vision/containers.md` | `fadff8c5a5cfcf92de002af499c163a4675918a5531ac1d7f437d0b1bf110f8b` | 1 |
| `flows/8e9e77/vision/flow-retrieval.md` | `142a114ddf5f071e65eae777c933014a825e79a7cd90bc7886ac656fc322d171` | 1 |
| `flows/8e9e77/vision/single-field-structs.md` | `e2e8dd66f6602667b7fdc490e9bda3275a30594dcb1dbba0d360627a1e59ba39` | 2 |
| `flows/8e9e77/vision/tests.md` | `1a764a01b88539daa3d202d550973726f1da05df9c2c707eb2088708dde8e23e` | 1 |
| `flows/908786/vision/context-refresh.md` | `fed0a0e620e4a25faf86a9e4d9a1529b4ffa5587d953df8fdba59cbeb76ae0cf` | 0 |
| `flows/908786/vision/default-effort.md` | `8bd43c2e90141ac5a68df083d97e316e8a30f3530a923c6b7238ad2c0b953a40` | 0 |
| `flows/908786/vision/vision-led-audit-and-fable.md` | `248aef1a334af69c06dffd31b56d99c95a426e13f1d26647068950ee424539a7` | 0 |
| `flows/966be8/vision/clusterData.md` | `33e240229db141750e7b71903d30c0f219d2f7f705829e9fd10a21890b62bb52` | 1 |
| `flows/98fbfa47/vision/draftIdeasForImprovement.md` | `f242e4854c0d03db27cfe26e198624423e39fb890900a46c62694757fc2fdf3c` | 1 |
| `flows/98fbfa47/vision/everyConceptShouldHaveItsRepo.md` | `c250f51e0eb065125101eb419ec8d1ce7b3e4c00bad0441bbb1f21a7780e4bb7` | 1 |
| `flows/98fbfa47/vision/metaCliIsComponentDashMeta.md` | `c93fcf86122e093212d7c852d5f84b9b6b75da07c451ee751480f2f6ae688197` | 0 |
| `flows/98fbfa47/vision/rustComponentArchitecture.md` | `59e77a2655c1397fdd5aac8ff1a72a7b3b101b357882e134ad82d75d20a88859` | 1 |
| `flows/98fbfa47/vision/shortHeaderNotNow.md` | `b23570ed61160080af4e1bcfd9083724a8a4eceb89c02f8426c18e509328cfad` | 0 |
| `flows/98fbfa47/vision/testTravesties.md` | `d6d0be1786cccc41bad945cb4f77be72ca70400d6d52ee03c0a9c517fe6d5fb9` | 1 |
| `flows/995a164e/vision/concept.md` | `4c48e2d8093aa875a830682344571c71d0b2a02f6ee546e754ff46b9093c7402` | 2 |
| `flows/995a164e/vision/contexts.md` | `ec0bc6042031fc6f89b993a90cfddcf480a8486b423bd2fb310939c15a57967d` | 1 |
| `flows/995a164e/vision/data.md` | `d10efa2b15cdbc98341537e7e04a97c9c21d92aad6f7d94098989cb7d43e7be9` | 2 |
| `flows/995a164e/vision/designPractice.md` | `a0f5bc3b75fe136fcab80026af04f1f20965ec76b88b195dd47da0bc67f8585b` | 3 |
| `flows/995a164e/vision/entryFiles.md` | `988cb62339ca05b1363a5b121af0b3bd8d48bfcc4aae780f4ae565d9abdc4d86` | 1 |
| `flows/995a164e/vision/explodedForm.md` | `830f709d373bf6793dea0beaebfcf3df160032b4084dfa7abae320b795218532` | 1 |
| `flows/995a164e/vision/intent.md` | `bd65cd3f300913f3a1430d78ee65eda9ac0917afd2f7de7d0e699af126e63d41` | 3 |
| `flows/995a164e/vision/kinds.md` | `0ff1c21ecea7502373de5edb513cfc36e8f7cbef792471279a33a9287edb7ed0` | 3 |
| `flows/995a164e/vision/layerMatching.md` | `b7620bdcba1217b582fd7154d25a6766b1773fba58be8ac9c8ef9b3f861784da` | 3 |
| `flows/995a164e/vision/rust.md` | `5a10a8f6412eedf3c2a189b5d796d9ca1b049b101fb338f8c7a031c818939358` | 3 |
| `flows/995a164e/vision/tokenCosts.md` | `89b9e40daf03792bfd7103e62f3f3217faf31fca9862168e988f00273764d2b6` | 1 |
| `flows/995a164e/vision/vocabulary.md` | `411e81527bd53f8a5d1f959a21448d31425e201394a323733ba07fee66d27493` | 3 |
| `flows/9993b5/vision/autoCommitOnWrite.md` | `a0a95337d678064a512d76a05a904b0d50ae785e0d6ec1db8d7b090a9d74c58a` | 1 |
| `flows/9993b5/vision/blockPropagation.md` | `11ea1a13173262459e31d6e52f8fe2613742b891c7ac20195e4674806ce2c342` | 1 |
| `flows/9993b5/vision/blockedCallsAndOtherModel.md` | `14f788559d30dd6c12a7e92aed381cda499f07a3c05cdd74f23d167a7ec29ad8` | 1 |
| `flows/9993b5/vision/callerIdentity.md` | `7899b4c32e7c9ee83099ccff03609d2b582a1f03bb0b41aba78d863deaf102c8` | 1 |
| `flows/9993b5/vision/codexAsDoing.md` | `0aa560cdf723b7d983e9e969f365f10569588dd2ce591124bd5f8d260f22b616` | 1 |
| `flows/9993b5/vision/codexNeededHere.md` | `0fe16db2433a8e21ce201159e0841439da8df394200b560836ec67055f281966` | 1 |
| `flows/9993b5/vision/codexRelaysPsyche.md` | `327405d6666c9f513f105172d0ec0f1468c6623d2c8a2a983d7edfd301efbe67` | 1 |
| `flows/9993b5/vision/codexRemoteAccess.md` | `8136c5f9d98d11921723b540ee385b25a720b8f264979662805add1018072dea` | 1 |
| `flows/9993b5/vision/codexScarcity.md` | `6a7a2d3d0bc496ced8af13dd9dd5520b17ed0ff7b36d29ed336cb8287cb1d753` | 1 |
| `flows/9993b5/vision/criomOsUpgrade.md` | `bb017ac8f4230abe75a958e71b79e642c5ad02af4787924480e2c1303d0ffc71` | 1 |
| `flows/9993b5/vision/curriculumNexus.md` | `c8f03e24fcad64853a0426d74bc13a2f359302bef2cf5e393034deefc0803552` | 1 |
| `flows/9993b5/vision/datomStructuralEditing.md` | `72cffda5419261d0baa6393cfc3a1c618253908cd5fb2af56eed0aea561e85e7` | 1 |
| `flows/9993b5/vision/distillEveryTurn.md` | `d1c0c11d7be596841f0c2f42be0afaeb05caa63acaca3fd247c29d3f579636a1` | 1 |
| `flows/9993b5/vision/easyFlowDispatch.md` | `31e917e53f283ca35c2d6679769f3629be0f3cdb5d398bc5e69f4f9a55269a3c` | 1 |
| `flows/9993b5/vision/editNexusName.md` | `6071c8fb61e1ea0e5c65e0d3027c93e1b42766278d589bd0d99bf284046cc02b` | 1 |
| `flows/9993b5/vision/fixMessagingApproval.md` | `2451ab96c71585ac80a6cbb1f7eec2fc9aee116419f4c0777a03457476340641` | 1 |
| `flows/9993b5/vision/flowAnatomy.md` | `c28847f433b4bc01c1c952b60000277f8ba31cceefc63bd7f4c939539361a91c` | 1 |
| `flows/9993b5/vision/flowIdLayers.md` | `0e828d9beb54aedf3e1c729c568673cd46db3f2e7f8452a22ea4829d26c1aa6a` | 1 |
| `flows/9993b5/vision/flowOriginClue.md` | `f57df22e88482fe4228d1164c8b63be00742fbc2e9cc2d9be8114c8bee1b02e9` | 1 |
| `flows/9993b5/vision/flowRestart.md` | `624bf90c3017c39bcdd1f18e6c8a01925c9c4d7777173e756b31343a433223e0` | 1 |
| `flows/9993b5/vision/fullSystemAccess.md` | `1df1dabaf2950f5489c9bbde6a2f7cf4b492cea410bf071f79f7959efdb000a2` | 1 |
| `flows/9993b5/vision/harnessBlockDocumentation.md` | `304bf466450ef560c6a9975af7625f2490d9b3402eddd2b3d0265e0a9f01ff5a` | 1 |
| `flows/9993b5/vision/harnessReplacement.md` | `758f164166b8db5df209e7dce31f42bcaaa038cbd6610ec32b06ed339ec3283c` | 1 |
| `flows/9993b5/vision/integratorFlow.md` | `5691c450bb80c1a8ef996dfc78ed56e38ba005f77689a3eeb97257c16f207ca6` | 1 |
| `flows/9993b5/vision/launchOnMain.md` | `9d358bfbca0cf67bab220673c8f89d7ee48a8f7392f5020cc37465a175d54449` | 1 |
| `flows/9993b5/vision/mergeQueue.md` | `a9dbd6d72a344a77f4aacf3888ef96ed96ef8570d09a7be4af14c0194e6e5610` | 1 |
| `flows/9993b5/vision/messagingBootstrap.md` | `137716c4fc24697e357fd67fc8a2c88c953daf2fa1b5de7779d337e76c3b2e63` | 1 |
| `flows/9993b5/vision/messagingIsScripts.md` | `88cd7071a6afdd9f6bae1f0b0b7e6ff9e2451a7c0a919cdf83c3089d04f8a074` | 1 |
| `flows/9993b5/vision/middleLayerRouting.md` | `6100216dcf90e95e5ec8c99a3de5ae44731d75a053244e85ecc8704fabca7650` | 1 |
| `flows/9993b5/vision/mindMemory.md` | `cec12b3dea6e714df5ed24f2e295871f8fe034dc2d78a2ddac055b88f207a5b1` | 1 |
| `flows/9993b5/vision/noMoreBranches.md` | `d7e54bd838316b3e229c0eb4eec021c46a9088222fb0b54d4fa0f06e059f2dd5` | 1 |
| `flows/9993b5/vision/noRetryRefused.md` | `213f126ca51316868546a731019de71c587b2cb999bfed91b4d7f07dd3be6f36` | 1 |
| `flows/9993b5/vision/oneSharedPrimary.md` | `39375ace30874c4fdb25018e6d1f1a59589e8513f1007f613f535f284adf542e` | 1 |
| `flows/9993b5/vision/operatorsNotes.md` | `a4f0bc86ee3858e25a985fbcd39a33e8ff24b3ff6cd0bbdf07657a45b0b4b490` | 1 |
| `flows/9993b5/vision/orchestrateCommitBinding.md` | `90314d8365a621415af617626fae36bbfd19c25fc05a50783cc4bbd02b697010` | 1 |
| `flows/9993b5/vision/orchestrateLocking.md` | `fcd32ffdbc8a31fa68738ec2ee79d22ad29e2433eef1b5c6e59442bc872d53bd` | 1 |
| `flows/9993b5/vision/powerLevels.md` | `2586558e60d2bf71f852a66cdbdc1747cdacb58a42f6cb8ca0ac317f56983343` | 1 |
| `flows/9993b5/vision/primaryNext.md` | `021e1a530699995c85e1664d9d1b153a71d74239ca959f92c66bfeb6f705bd85` | 1 |
| `flows/9993b5/vision/primarySkeleton.md` | `dec1482f635a672f806413df707b6d16cf395e602d037e61ca8b4e856409d852` | 1 |
| `flows/9993b5/vision/psycheChronology.md` | `571401b1e6d8c5a66a1b2e2bee57bb0f0b75751bdf914c493d68d6d31930da46` | 1 |
| `flows/9993b5/vision/psycheVsMind.md` | `5a7a0bedafe80eb1dc833098eb9e87556f244d685e35f707d20ea12c1e4d21ee` | 1 |
| `flows/9993b5/vision/rebootstrapWithPowers.md` | `6d3204d392ec83e53267b9fd8417f81606bccbc518005fb84c578c7351fd2de1` | 1 |
| `flows/9993b5/vision/remoteRotation.md` | `a376ec8f4de2c46539ad47c99d9fc49a383fb5623ebc3a27ff58edd8f2b1d01b` | 1 |
| `flows/9993b5/vision/selectiveImport.md` | `12d3b8968c593256a55753e2f492aaea7cc54bdbb58e282d80b5b50f29f77bfb` | 1 |
| `flows/9993b5/vision/sharedWorkspace.md` | `b9dc816d8e2c127d17ac65b91e7e3917279a65b3fade1a3726546926225d4175` | 1 |
| `flows/9993b5/vision/sprawlFix.md` | `727b2a9e4d6efa4f113c4bb6fadcd1ae92239e3cb0257b64064abed5a683379f` | 1 |
| `flows/9993b5/vision/structuredLog.md` | `5b214503607fba4ac12a7cae5cd41a14b2cdb6fc57896f2ac331ed59760172a4` | 1 |
| `flows/9993b5/vision/subflowIdentity.md` | `1134444a7ec927c60f3b47612fea0ea06fb5c768609087df17a3ed21f49e9195` | 1 |
| `flows/9993b5/vision/threadNaming.md` | `a988468a3e908a7aeec0b7b800952a539e51d7b1ceacdb616217d817c863d879` | 1 |
| `flows/9993b5/vision/transcriptArchive.md` | `52605f3eedb63346a84d325403ce5ef54f8c2b717a445bc54347c997d24e2fd6` | 1 |
| `flows/9993b5/vision/transcriptIndex.md` | `f82486f50149a0325eaebd9910aa97c59454ecf7fcb20669abdf6c6d66256650` | 1 |
| `flows/9993b5/vision/transcriptOverFiles.md` | `44c47cf1c46e6dee5e0857cb7b71676cf65ea225f19d8e08146813ba45b3dcd6` | 1 |
| `flows/9993b5/vision/transcriptSelfReference.md` | `2e4e9702a4ec149c89b12dfd37cd08f92b35cc85a7631f0cb2a6afd85e01f632` | 1 |
| `flows/9993b5/vision/transparentRefresh.md` | `e338145bd726d499103c858c623b8b08bfdc198729cc6b81170f6ef10b320cea` | 1 |
| `flows/9993b5/vision/typedString.md` | `3ca2a4528c6c7fc026872c6864961cb5d2d12bb13cafa67baf522a36b65485ed` | 1 |
| `flows/9993b5/vision/visionAccessibleToAll.md` | `446f667f10666237d52f5c2b5d5fa297e63102881bf235be94a3964bfbee1124` | 1 |
| `flows/9993b5/vision/workspaceProvisioning.md` | `c6f1ce7846d169d5725225c97c5f59cfb9eb680cdff5a45391db7f873919f90a` | 1 |
| `flows/9993b5/vision/worktreeHygiene.md` | `36cceed189be2f896f698009bf30276e9432410e225130fed3460514937b04f2` | 1 |
| `flows/9e7c9f/vision/cloudRemoteServer.md` | `9d732d2932c926c60ac2fee6a6d63ac59e0c0456165c904eb81fd0870cff15ab` | 1 |
| `flows/9e7c9f/vision/distillAnythingThatIsUsed.md` | `eba2fe6cf511a94ae63ecc4a73d5f54f7672316f0576169cc07b3398a39e1b59` | 1 |
| `flows/9e7c9f/vision/models.md` | `d9a2596726dc4f2f0c22108bcfcb12a8ea4294b081406c4625c3b6c8df6a06a1` | 1 |
| `flows/9e7c9f/vision/remoteControl.md` | `9ad9edceb2910fe545defaa5de2fb0442751260e444fa7af6cc27fdd24e1f85c` | 1 |
| `flows/9e7c9f/vision/subflows.md` | `d5eb3275c3c2825c55dcee7cec20a19f33d81bbd1567a08a2de2319807f69257` | 1 |
| `flows/9e7c9f/vision/theLiving.md` | `7b155c81eb7743f967d5db3b2768f4a5fcb24af0a7df3adf3f86574e36bd0ca7` | 1 |
| `flows/a5587095/vision/rustComponentArchitecture.md` | `cf8b1d25400ca2f47ca9fa6e3f5c8f4c7b1dcf65cd10817c7c43cd8836fd6b02` | 3 |
| `flows/a5940a/vision/mainFlowShouldNeverTryToLocateAFile.md` | `3da13432e61ce9a62d7844acb697bc4420dce77d9e0f08bdb51cd4229631d7fd` | 1 |
| `flows/a60a9e85/vision/demandDrivenDesign.md` | `03463e1c3552b4e4ad917eae7ec9f5c066b412a0f949fd4d99df10cc36ebc43e` | 1 |
| `flows/a60a9e85/vision/distillation.md` | `ec655c2e07a039b9e69b18c57bf148aa20fcff3447143874b86c007593dd7d49` | 1 |
| `flows/a60a9e85/vision/llmUnderstanding.md` | `c3cfd9244a0e84cd38c6b96b3c4db97a97ff0476d1a1cb5bf724e92802fc93fe` | 2 |
| `flows/a60a9e85/vision/outputNoise.md` | `4e54498572e29341ef1ad3b3252f6a167e16e8e1223e3154fc4ffa6277376729` | 1 |
| `flows/a60a9e85/vision/skillDesigning.md` | `a5df50ec2bb7914945bfd63b4f99e080742f264bdebe124f0a30a1df159759f0` | 3 |
| `flows/aa4c7747/vision/basePrompt.md` | `ab9ff6d998fd16c0f9c558b6351d97ede105cd021ac9e5885ffeb9dc95278af5` | 1 |
| `flows/aa4c7747/vision/dispatches.md` | `fc738f437298e596cb7191eea88fd699f0f9eae9023e5e3c123a8f69a7030f10` | 2 |
| `flows/aa4c7747/vision/orchestrate.md` | `dad74a7ef2b106c3b8440353721d188df59f52fe50b43b6c6910c05a798a2aa4` | 2 |
| `flows/aa4c7747/vision/promptCrafting.md` | `d4f9fe7746703156d7492c4bd554404f7485e58229f08c3a7c6b3a7063443d2c` | 1 |
| `flows/aa4c7747/vision/sessionLog.md` | `34f6309849e06f574d21f183a41e58965e20da4c8c5cd430d84f8ecc996cebf4` | 1 |
| `flows/aa4c7747/vision/skillDesigning.md` | `ab22d5a3a1e0a37556a1d5280385c2e0432631b800a6a1759f1ce6be747b6fcf` | 2 |
| `flows/aa4c7747/vision/spokenVocabulary.md` | `ae110f41f977dc3b640b7594be4b1061c0e2cedd4a5b316e394f72b5c7078c7a` | 2 |
| `flows/aa4c7747/vision/uncommittedChanges.md` | `78a53ea2f73f2ff50fc7c7ae720915b63fc720e12f2d2aa42464dc7aae4628ac` | 2 |
| `flows/ac1e9ec8/vision/distillationNegatives.md` | `56f4520b2c58e8e49bf6ef0544442f78685037ee1da95ee1ac671f5ec9b68e77` | 0 |
| `flows/acbb6006/vision/approval.md` | `a86e0c6dc018c37678e3296027080a8961e862c1f446cbe7dab0c38883be161d` | 1 |
| `flows/acbb6006/vision/distillation.md` | `e5ab7c3e696439a3796f63e2eb50a77c0fdad78fd0c42781706d6a68ad7cb7a9` | 1 |
| `flows/acf06f/vision/wisprInteraction.md` | `0013041f8fb27333d19d4fd4679a59376c8a77699f6672e3175e3b39af1f4d89` | 0 |
| `flows/ad19b1/vision/distillation.md` | `ec6e072873fe4ae2d775c1865e9fc9851d627a574fade920573efaa7b51c110b` | 3 |
| `flows/ad19b1/vision/psycheSystem.md` | `97999a8a02636dbb0050f89dc2333bf13bbf0b325348213e7c7bd366e1bd8d62` | 1 |
| `flows/b05237/vision/operational-centralMessenger.md` | `ca1b548be393ca25937cc4d613dfbf7094cb30b6b330942cb66429b68828c29d` | 1 |
| `flows/b05237/vision/operational-clusterDataAndHardwareAnatomy.md` | `5b4a95101724f88d7fea2762a5f6dae67bafc6eff10e6dfd948a2cf2074e987e` | 1 |
| `flows/b05237/vision/operational-codexRemoteVersionRouter.md` | `ec000ff62ebf5f309dba2efb9995a981f405f7790f130ca18410ff112424ac91` | 1 |
| `flows/b05237/vision/operational-criomosModularHardware.md` | `27a434c31c5d6027e09416d37373c8a84d471c472db473632f6d7d0fa4f1ae10` | 1 |
| `flows/b05237/vision/operational-delegationChain.md` | `a337bbf30011b35d7315e1b6d0791b505846d5c71a7925b9145880443e8fa6f9` | 1 |
| `flows/b05237/vision/operational-effortIntoIntent.md` | `bb57d34798c7de49499ae380263a94208ab07d3866fd5112cdcaebfdea6be828` | 1 |
| `flows/b05237/vision/operational-fableRestartWithRecoveredVision.md` | `7c270853cc147289c0ba4b0556d6d3524b8e9d47b021f063f7b651447bc47d79` | 1 |
| `flows/b05237/vision/operational-fieldEnergyLevels.md` | `f25829218d84acd76027b38d8882791a3968f386140dbe2256c4dfd8264f258e` | 1 |
| `flows/b05237/vision/operational-fieldFlowNotReaper.md` | `01d20f3e8a30615b3140af23243caa080a82dbf5e908ea13c33a2d8d5834ebef` | 1 |
| `flows/b05237/vision/operational-fieldKeepsThingsWorking.md` | `44efd961dab410778553d9fff07879dc566113221ea6bc1bbabbe89620b73adb` | 1 |
| `flows/b05237/vision/operational-fieldLunaWatcherAndArchiving.md` | `7844b7855c439353daea4772f669ba6230476aa709e66030e68a0015c184941d` | 1 |
| `flows/b05237/vision/operational-fieldTestingAndUltraLow.md` | `1e371f5b7a6570141acc16864a507ed57807ccb4530042f16f8a80aa72a9d7c7` | 1 |
| `flows/b05237/vision/operational-fieldTwoSeatsAndRefreshNaming.md` | `9fff834a26d08854d746440529ddb9be0d3030c214a1b25cf11dac534b27d7e4` | 1 |
| `flows/b05237/vision/operational-herderUserExperience.md` | `5a75c6ce99eb165ec9548f62f6e017f816fb1fcbad464eb619a13d5ff2700fc3` | 1 |
| `flows/b05237/vision/operational-herderWindowManagement.md` | `3b7c47b1bf8721aaef47fc2229f6ba331814e5bdbcae3afc794f81305c7c4137` | 1 |
| `flows/b05237/vision/operational-logOnMainNowMigrateLater.md` | `5225f395797b7df7d3c4b5e8c6e7a2ac4b2ff0da78d0eac452beca9c3d9dfe7e` | 1 |
| `flows/b05237/vision/operational-mainFlowUsesSubflows.md` | `69cdf515d495658659af5dc3070a43d488db3a1ef5ba431031b1f95099bdaa87` | 1 |
| `flows/b05237/vision/operational-mermaidThenSvg.md` | `9b0c9fe636ba493f25565bf97bc19e027db9c4bd701671c886b0ce874544c898` | 1 |
| `flows/b05237/vision/operational-messagingAccuracyAndFieldAwareness.md` | `f0bede786714e628b6bcabf6b0e6fb93ef1622aaa627a5ab145570e62635c99f` | 1 |
| `flows/b05237/vision/operational-messagingDatomSyntax.md` | `1adb08938ba068be445c7ee3e0c0c060786b4d5c21be567e9c6fe97a7e9d9cb9` | 1 |
| `flows/b05237/vision/operational-messagingToDeployment.md` | `c223a06cdcca07b34dff56233c0c872e1487f7555ef1bd1259f9828086c26d8c` | 1 |
| `flows/b05237/vision/operational-messengerGlanceApproval.md` | `aa8a5283b509ec20b665c35ce708400a653b875772d95a04b8cea8099c2d42e2` | 1 |
| `flows/b05237/vision/operational-messengerPaneSyncFailure.md` | `49e783245f3f6a314a6a7cbe42c06aa6fb2e086242952d7630c30c6624fde6c7` | 1 |
| `flows/b05237/vision/operational-messengerSynchronizesRoster.md` | `03a158d75c3cc133f6aaa4b0c4fd472eb390ae673a3e219d3c0894b419614450` | 1 |
| `flows/b05237/vision/operational-mind.md` | `76ed56b3dd2b669cd32c6eee9c98521d96711c2abb9790fd39a2e00c5f41bbf6` | 1 |
| `flows/b05237/vision/operational-ownApp.md` | `26c6352a37508e50a3d5b2fa68350ef8332672b7e1cab3a33993bd647caf90a0` | 1 |
| `flows/b05237/vision/operational-paneDeathAndMessagingIndex.md` | `613ac41c000cdc9242589df2c9404b3742d03967c42c8fcbadc5674facc3fc80` | 1 |
| `flows/b05237/vision/operational-powerLevelDistillation.md` | `2afc4779e09edfb9d9dbf09d09a946af95aa33eb34cf4adf814813ec53f0dc0e` | 1 |
| `flows/b05237/vision/operational-primaryNextPsycheLogging.md` | `ec3b24b8047b8086ea1193ee7f072dd50030ae698e22a93c747d1d2266bdc88a` | 1 |
| `flows/b05237/vision/operational-psycheMindAndTheThirdComponent.md` | `99d4683ed13a8d9f99516a1e918de35ee14fc205054aa57ad9fe30e97a576d0f` | 1 |
| `flows/b05237/vision/operational-reaperSubflow.md` | `7eb24a62192764b3f8c8a95d78ad6d4d6d85b73b50d2d19f789bfb05b560505b` | 1 |
| `flows/b05237/vision/operational-reportFormat.md` | `f94e28b18313ec0b6038334c3f01b3ec00dcbb0294c6c9d4751c233e492d115c` | 1 |
| `flows/b05237/vision/operational-reportIsTranscript.md` | `56afa7a170e84e1860da633e00c40936aeebc9fc75f0e8801d04aadb72314bd8` | 1 |
| `flows/b05237/vision/operational-reportWatcherAndIllustrator.md` | `b6dcac9d9e7cf87ad655336b1bef1be0393fcd5e0db644aa610a455ee9399d08` | 1 |
| `flows/b05237/vision/operational-signalOriginHandshake.md` | `35eb75dcff5ca9eb9e6c1424183b7170b30592ea66836f4b8817297df2eb09e7` | 1 |
| `flows/b05237/vision/operational-situationReportAndMediumLayerOperation.md` | `cc5030bac0bceaebcbf7764f51fc6e97afce6eacc73f419fdca4d9ecf116fc0c` | 1 |
| `flows/b05237/vision/operational-skillIsVisionPrefixed.md` | `16723ff173feb151595c46c99e6f22788c1f0771acfaf1208922e39550b7bba6` | 1 |
| `flows/b05237/vision/operational-skillTypesTriad.md` | `e0e905803f584831f4c77c19ab097e90d067cea36d23afc9b678e4a7aa6007d1` | 1 |
| `flows/b05237/vision/operational-standardMessagingSkill.md` | `351e95602efef1c64c7396c2319ce89ec98fb2af5571ad312af10eb0d02324d9` | 1 |
| `flows/b05237/vision/operational-structuredEditingDatomEvolution.md` | `d6334a1045c7cea3cdf6d7a89d8cb70402e9ba69416b81d47fbeb54102ef2799` | 1 |
| `flows/b05237/vision/operational-testSkillForIllustration.md` | `883586baf49dd02197cd1b76712f51a3f7427365921c13a82aa1d6c607c89683` | 1 |
| `flows/b05237/vision/operational-theField.md` | `41fdbeb5bef045c298d9e30610a9fb6ff8479de6f8bd3d573fb6f5cc344ac5c6` | 1 |
| `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md` | `27d8e4659dd866a2c548bca68a2c3bcc370c5fc7c027f28f0359a8b18183da24` | 1 |
| `flows/b05237/vision/operational-transcriptAsLog.md` | `22ecd3cb75fd03cf6ccbb60f9137d182cdce8f0e0e71b054fddc01053a17d8be` | 1 |
| `flows/b05237/vision/operational-transcriptBlockExtraction.md` | `b08b6f8a952f3e19dfc711958820b764bcb38fb07e12718212d62018b8b55bc0` | 1 |
| `flows/b05237/vision/operational-typedMessagesDistinguishPsyche.md` | `c993d373fa26ae2ea9013db94c631a02cec3bf543603fd7f45733613d1b25906` | 1 |
| `flows/b05237/vision/operational-voicePsycheDesktopAccess.md` | `91bebc482a438f4691de7d880bce5e2c7efde694e83504db833e6db6fc59c5e6` | 1 |
| `flows/b05237/vision/operational-wisprFlowCodexPaste.md` | `38e50b46e2afcfddc7f669e4d0ff5bd1234334b8e1d6ca7fb9870ad0be0ecd71` | 1 |
| `flows/b2da01/vision/skillDesigning.md` | `6763db23ff8d61e37c3d61261e451e9925b9be89899c8b563b817af5c32bb14b` | 1 |
| `flows/b2da01/vision/wisprFlowService.md` | `88cb525e3d8192e738441b2f3e1ab8fb5fa34f20cbf74146769f5b607dcf0f63` | 1 |
| `flows/b49251/vision/flowLaunching.md` | `80deb22f76af08c6e9a5c9a2e8711b2503580bcaebb4b7bcc8b53d1ae618ca35` | 4 |
| `flows/b49251/vision/heartbeat.md` | `a22b36fa01e98394ba1c0c7cdfe57ef7ac20552b0ab9b34096d23eed2479f075` | 1 |
| `flows/b49251/vision/layers.md` | `de2789b87ef5ce6b77dcfad765f2ed833d8c78ec6ca4a4c9b28fda0c080a1da3` | 1 |
| `flows/b49251/vision/nexusAnatomy.md` | `8cc0677146f5b4b96bbd811bfb3ec0fdeb17a4cb88d9102edb5b4171f163ea03` | 1 |
| `flows/b49251/vision/psycheFlows.md` | `96f7394c9078a71d90e53ec123dd84ee17a70f14df52ac8aaf346aa52a4811e3` | 7 |
| `flows/b49251/vision/quota.md` | `418a13c72beaf8bb2682aaf90e32b653203dcf970f6d69f5871287c7c187b61c` | 1 |
| `flows/b49251/vision/subflowDispatch.md` | `894eb73377feff1343680d895b7396d8162747b713c84bd701d30f386065e502` | 1 |
| `flows/b49251/vision/systemPrompt.md` | `f7c460ef911ecbc07d21260154a33f061d0243022cab87a99453c670f954e226` | 1 |
| `flows/b49251/vision/visualPublication.md` | `11f26e5ab70e5aa6b916af4ba7d2828b405d681e755e4fdd8bf59f133393a402` | 1 |
| `flows/b675f3d9/vision/distillation.md` | `3bb95ea197549f1ef49b7946032d04e0b5e2542b8d6226d28429695c0d5b6569` | 0 |
| `flows/b675f3d9/vision/highLevelView.md` | `16d03ba82cd5ee0d2449c210b293cb6c250d8a3437336e6ba59c80aa864096ca` | 0 |
| `flows/b675f3d9/vision/remembering.md` | `57b381d1aca3d2fd69630b442c15c56400757a0dde07e0c90be92d33a5518395` | 0 |
| `flows/b675f3d9/vision/spokenVocabulary.md` | `eb5845be92a4d4d6028dc30ce33aa39e259270c86e0c027f846246101a10169f` | 0 |
| `flows/b675f3d9/vision/visionImpurities.md` | `ac384d09d6c4a5d9d523634c5c6437718c0d85307d7ae455e1441bb81fe69f73` | 0 |
| `flows/b7465e71/vision/remembering.md` | `05dd0fa8e467766cf8960dbeb924b8e3e37b1d70d35d323dea7a76e93de50e5f` | 4 |
| `flows/b9f4f6/vision/flowModel.md` | `21880127de9dc3e519cb9313c3ec53315c6753b39c2c9ad5b7ee4413acbcd93a` | 1 |
| `flows/b9f4f6/vision/presentation.md` | `04a858de6fc666e5916efdfe8d113cdc699a90f92d855658fbe81731ee52976e` | 2 |
| `flows/b9f4f6/vision/skillDesign.md` | `ab7cf523894dffa6485297fdf5fa37c8d26ec082fee7e1a49ec4230ca557acf3` | 1 |
| `flows/b9f4f6/vision/topStratum.md` | `e6fc4cb4e2ef59566c49cc7f50826214198e4d3defab428aafdd753ce2989918` | 2 |
| `flows/ba906ae2/vision/signalIsOurMessagingLayer.md` | `ad8e9c8af6af978a29ede3d7e82d127b76f137ce1ecee8ae38789ef2cead74f1` | 2 |
| `flows/ba906ae2/vision/skillsRepoSourceOnly.md` | `bf844718af6ba29f9159c49cfdd5f90d22747ce7c9c15b0b727e6a0222a5e702` | 1 |
| `flows/bc05da32/vision/mainFunction.md` | `6239e47eeceea4f648b7da283749bd5aa80ac33a221c720445dee28706a66603` | 2 |
| `flows/bc05da32/vision/skillDesigning.md` | `ae19ff7c7c3be52cdaac9dc78f8fa82585791e4faf3efd34e1eea85e917a2190` | 5 |
| `flows/bcd02a/vision/context.md` | `cf720d49c3d74e636a15d578c086f7b97f3153b35102d35e065e803fc172b8b8` | 2 |
| `flows/bcd02a/vision/council.md` | `857a787b665767d38843cff1e204805fd0a9700edde610915a7b488ceddfeaf1` | 1 |
| `flows/bcd02a/vision/network.md` | `d6f53d6ff5a2a89bb67d6edbc02c47ab7fa85e91cc427dbc7bf452e922bf2739` | 1 |
| `flows/bcd02a/vision/nexus.md` | `7f93fb76e49bdb22e2008d68b80ea553bec5b74375d26f5998b4aa593406bc3c` | 1 |
| `flows/bcd02a/vision/paired-flows.md` | `ebf84d6e663f5295d4164e80a3680842e57c8c230bcc17dbb8087dd37cbd8b08` | 3 |
| `flows/bcd02a/vision/runtime.md` | `91fe97c9bffe3a2cd787caa36d7e8bedca9b90f45fef1d560e500f5ebe980fd3` | 1 |
| `flows/bcd02a/vision/signal.md` | `0df16dc5e952d17866dd0d78bf8504598607d80344786fe254aa0e4c6b453b2e` | 1 |
| `flows/c7128c/vision/commitSubflowScript.md` | `d22b896cf7122fd6c31075e52bdbf9e9168ad09c188225f56ea8b39c3895c000` | 1 |
| `flows/c7128c/vision/jobEffortLevels.md` | `48c273d3887eac31cfa7c7400ec574a7a6a1232bf1a42e1dcc46287734ccbd96` | 1 |
| `flows/c7128c/vision/messageAndFlow.md` | `62245e305068b7ace3a405d9db40f5fff485389430395c25552dd02847d2231d` | 1 |
| `flows/c7128c/vision/psycheVersusMachineMessaging.md` | `7f8cec9789eddbf093906939a887879a1f9ba1360c296e7c9415f27a56e8c03b` | 1 |
| `flows/c7128c/vision/transcriptAndMachineFlow.md` | `77ecb660a2d1422473dfaac822770761ae76cfe597409afe6f47499cbd76f6f3` | 1 |
| `flows/c7128c/vision/visualization.md` | `cca563841b5d45244459be2f60d0b69835634af1a6024b5931e453c9ae033154` | 1 |
| `flows/c7128c/vision/workspaceAndWhitelistIgnore.md` | `45ecfb6768617abed22fc2931143a3770f2102b79a08b48eb08ed3d6cfaa2c50` | 1 |
| `flows/ceb3b9fd/vision/hijackRepositories.md` | `49bb9d9768d5fc30eff01ab339792fcbdc1b4f6ac5cab5a93daa1d786039aa27` | 2 |
| `flows/ceb3b9fd/vision/topStratum.md` | `ee1f872bafc61a42412945f77758a3424c7ae6f28a428fa2b4809c8fbea00f15` | 4 |
| `flows/cf0ed9/vision/openaiLacksTheFeatureIWant.md` | `572fc244cdffa0611d2e2e9faaa34e9c5793b5548346e9d4375669dbe56237a7` | 1 |
| `flows/cf3553/vision/operational-mainFlowStartupCorrection.md` | `4ac46a167b0184dd6ae7c40a75d901e3fe2a9bbde087a62c3f0c25d0755b98cd` | 1 |
| `flows/cff271af/vision/distillation.md` | `4a3bd80018a1cfa1a5b81095c5c2f1c4906998dcf50a7f55ca699984501eb4f4` | 3 |
| `flows/cff271af/vision/reports.md` | `6b7357861fc208462fcd7bbbd73a12419b2b6c7350d9ab7da49729c885a0d39b` | 2 |
| `flows/cff271af/vision/skillDesigning.md` | `57afc6119d60ccc271cf39a9dbb175636d8b9a84530722fd38d9773f3be5ff3c` | 2 |
| `flows/cff271af/vision/tuples.md` | `ae2e4773e18df8af9ece080c3dc209b25fbe0c5c40139d1e0e82411bb5903aff` | 6 |
| `flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md` | `4d9be9743e9634d0d8ee34048ad5cd9478bf8c3f8216102a79c6bf76dfc85e45` | 2 |
| `flows/da1e3f/vision/operational-coreSoulCluster.md` | `bbced76b60a3d9abbaa00d04171a79fc770f815f934990ac2b42081235dd16e8` | 1 |
| `flows/da1e3f/vision/operational-flowVsMessage.md` | `c39621a112a94b4d238f7d770ec398c3b27e4e58069047557a5310adfb13d833` | 2 |
| `flows/da1e3f/vision/operational-harnessSpecificRules.md` | `cc92a8800810c021fa7eb8f4ae10de532f5a17231fe9056f032a5479cbbdbbd5` | 1 |
| `flows/da1e3f/vision/operational-launcher.md` | `ce946f2ed9e677a50bf21f2a36972bc8c23da01e8bd0ff5eb3d13c6dbceb6483` | 1 |
| `flows/da1e3f/vision/operational-psycheAndMind.md` | `b02dd7809f93ecc23d246aa69a1363dd1573fa7883cc1560b001982619994c3a` | 1 |
| `flows/da1e3f/vision/operational-psycheClusters.md` | `86ae66cb45fb7bcbad823333d820b50d4ed2b49378b73363471df0df1696eee5` | 3 |
| `flows/da1e3f/vision/operational-restartDirectives.md` | `10ca79d51bc1cb1e4edc2dc80a83714ef5929acb6c9ce091b281f666a4fbe0b8` | 1 |
| `flows/da1e3f/vision/operational-skillsMissTheCliShape.md` | `6b634d20091b95e951e4b1d27c1e1174b19108f20e4ea6004185ab4dd7d80fb7` | 1 |
| `flows/da1e3f/vision/operational-toolsNotShellScripts.md` | `312df1b4a3d39801993de0b26e9730d5555a0f0335d33e010c9c77206e0883f5` | 1 |
| `flows/da1e3f/vision/operationalVision.md` | `a0ba8ee62c457b5563bf6c338ed048b5c315a671d6b7709cfbef7a33c7d34558` | 1 |
| `flows/db267d/vision/reminders.md` | `12c4bce96abb2e02db868a0ae23d8f3df73691b76113a9e807365c2f87f70ca0` | 0 |
| `flows/db97561c/vision/context.md` | `8a3dfdfacddac81da494cd09c4bb240dba892d6565fb5d19b6e586bb7af537ff` | 1 |
| `flows/db97561c/vision/promptCrafting.md` | `703148e720fcbf54551f2188c7a5a117e8c316fd1766636fcaf08685d95392c9` | 3 |
| `flows/db97561c/vision/psycheLogging.md` | `817d9eb8921aedbbbc2e175371a27c5446d3a362677bc934f8d35df318baf74a` | 1 |
| `flows/dc1c58/vision/dualingo-compositions.md` | `e714a98b858fde372bc268ef85fed95c244d97ba654ecb095c04a6506c1ada7a` | 0 |
| `flows/e06e4c07/vision/flowDaemon.md` | `1be4da1c69483362191a505aa301f5fa06fffddfab0cafd4d65220005e894567` | 0 |
| `flows/e06e4c07/vision/flowKnowledge.md` | `537e930b8d2d9dfa3b59bbe0b2d3862382529e0bac86a5edab70a483b8b72abc` | 3 |
| `flows/e06e4c07/vision/flowsNotAgents.md` | `2a2c3aa94f48b0481969a697fdb1592760bc78059121db95471a8fb130f9ebb7` | 1 |
| `flows/e06e4c07/vision/gradientsOfAuthority.md` | `de9fb3b439f2e00360a23db1e234b800b09ab86fdf5123503431f2ec94f470ee` | 2 |
| `flows/e06e4c07/vision/letsUseTheSameVocabulary.md` | `bc2ab3f57e69a647d209891eee3c309bafea57f91281b856e892d347a2bb4286` | 2 |
| `flows/e06e4c07/vision/managementDelegation.md` | `dbfba35d51467e61b989e498a3795c2b5044f7dde0ccd29f7c9cd7780e1b2898` | 3 |
| `flows/e06e4c07/vision/rustComponentArchitecture.md` | `313b6c84f980e7347d6d6337c4e77e472a8b516751b795749d7c7efc20eec6dd` | 1 |
| `flows/e06e4c07/vision/skillDesigning.md` | `1946c8a46617e3bc13f698917c0701d0a9040b6450f9ca578bb0a00d5f5043fd` | 3 |
| `flows/e06e4c07/vision/testTravesties.md` | `331d24e1d330c88a75671b314262e2cfbe47f7ba0f422e5e3272033b163582f2` | 5 |
| `flows/e1953c/vision/contextStrata.md` | `54bb17266d24ff5ca00e45c2ee0f5eaf0d2866d27abe93927f29e45bea40cfe8` | 1 |
| `flows/e1953c/vision/criome.md` | `b2c2e874cf14cdd0c9a752dc515cba6a87d2eca8ef31a7f3a71cc4944c64ebeb` | 2 |
| `flows/e1953c/vision/flowIdentity.md` | `ed5282bade360ea71092500920f24300f5c8d6f18a6cbcea98e3a62d6fe99f10` | 2 |
| `flows/e1953c/vision/flowLifecycle.md` | `c0c58431b1f189eee002aa0fa6ce5a8759fa631d9d63d8796df7b07937b2b80c` | 1 |
| `flows/e1953c/vision/mesh.md` | `79b7b3b1c3cd969329c184cf17de55d712147dab2bff94f0a406128ce9de607e` | 2 |
| `flows/e1953c/vision/nexus.md` | `9ab41cf47be15ec11f33a7ebbd13fbac95df51b2ee823a3c0e34d58f928d6601` | 4 |
| `flows/e1953c/vision/privateLayer.md` | `b31f9c43f519b1204ee61bdeb0894d57819ea2498fc0a94b477d56b6531ac068` | 1 |
| `flows/e1953c/vision/repositories.md` | `e10cb671b8d255b6a7190823bb5d740117433aeeb394b79dbabb5cd0331e750d` | 1 |
| `flows/e1953c/vision/secrets.md` | `c08ca4b84bcad1ec8e2ed9b2e86f455d526691af0bac08e125276ed008b1551a` | 1 |
| `flows/e1953c/vision/terminal.md` | `a77b66d61c3375743739ae606210a32270c6e645c5f488550b692fee8d3c2cd5` | 2 |
| `flows/e1953c/vision/thirdModel.md` | `40c09d3a5d78bac1e770573286e94ee5c1a18c80480917d36ccdf27fc8fa9326` | 1 |
| `flows/e1953c/vision/triad.md` | `c5e953567393575d243b3b993161c17c81dfa00817c9b6de7f58cf75914d3b30` | 1 |
| `flows/e4a40e/vision/distillation.md` | `2e4698aa24911583ffeda579a3a4c580c6f8fe0ff867f62aa990247e7bc4941f` | 5 |
| `flows/e4a40e/vision/witnesses.md` | `7408c6e99bed1ddeedbf636ac376839ccdf2f6b251a6fb94f69cf0be6859c957` | 2 |
| `flows/e4be1c4a/vision/awarenessIsGeneralUnderstanding.md` | `8685bd55a5591c423beff8453132da8ea85164bbe995df0ff917c38bb2df4b94` | 1 |
| `flows/e4be1c4a/vision/codeAnalysisTools.md` | `20bf9e60029e78c521bd36f65bca85b5c6b6fece863c0bc7ab1d0a59cf07b3ea` | 1 |
| `flows/e4be1c4a/vision/rustComponentArchitecture.md` | `9ddc4419c390bdd07df0c3906c43af256025a90d838008a9497205d21d10d818` | 2 |
| `flows/e4be1c4a/vision/skillTypes.md` | `a46bdd470e092813351b985869dde9c93e8761db72e90b7b9820b888086e64f7` | 2 |
| `flows/e4be1c4a/vision/skillsRepository.md` | `82a48ac8b1ebf9cd7be1b9360e24875e57242a669bde7fcc7df162ab87ac2823` | 3 |
| `flows/e71fa5/vision/private-data-separation.md` | `4ab3405867a4826f841f5bfb200e50ec91b548450fbf4e0737ca5d4bdbf61348` | 1 |
| `flows/e8c4cc61/vision/designExamples.md` | `225838de87c1a474b76157e27b8cb174f97c32a8b34ce0eb96780e27b887455b` | 1 |
| `flows/e8c4cc61/vision/designPractice.md` | `1726a8286b87e933c4bc64ebcd5290890ffbfed05fd24c8c3b54766444e36c9c` | 7 |
| `flows/e8c4cc61/vision/psycheLayers.md` | `6c60d5aa85cffcceeb584b9d57ef5219429d38d752acae67d1b0e2ac168892cd` | 4 |
| `flows/e996e8/vision/editCoordination.md` | `10646055ac61f6b7215bfce8e4bc54fb72899bfd3f91e770621b9d0f2101589d` | 1 |
| `flows/e996e8/vision/flows.md` | `7c849b46f2db0cab5320d78bc0ecce527ced413ef7e1b0ed04a1a01ae1d5672a` | 3 |
| `flows/e996e8/vision/workspace.md` | `0de82b21d3ce5bdef7c45a14f63e353cd10d154251279b3020074a9fa6b85702` | 1 |
| `flows/ea1e56/vision/desktopCodexIntegration.md` | `859b6f06787e1866a471695fcf222af5520d006eee259d75d3ab28774cf7385a` | 1 |
| `flows/eae736/vision/sessionAccess.md` | `8580564b665c7e7ff2c538940911af3673be9af467709abd2a7aa6cd95678b26` | 1 |
| `flows/f426777b/vision/skillDesigning.md` | `ea9308e87092f638325ef57b7d0da5102b01101cb38c57871207b8dc70a23b61` | 1 |
| `flows/f55ec8/vision/cloud.md` | `71df66f466b83f89fd1072ddc2266ae6ec02eccc54f75359fc0032123171a8f4` | 1 |
| `flows/f55ec8/vision/flowIdentity.md` | `c9faa16fd9e37ff50d21db69a6081cdb5cca5d522a4d9b110664603800bfd9e6` | 1 |
| `flows/f55ec8/vision/flowRefresh.md` | `1672bbe84e4248f4a580d7fac065254477123d4e096db786ec3cfe8ec6835c70` | 3 |
| `flows/f55ec8/vision/heartbeat.md` | `a65c7d6b1af8e7c074bffd551b458f030e00f5317e9d7661ae3ad41a2144690a` | 1 |
| `flows/f55ec8/vision/layers.md` | `bc4c0d9ed990cd76813170569685ac05c33faec999a2ec93e4a77f1bb3ed4cbc` | 4 |
| `flows/f55ec8/vision/modelRoles.md` | `cee6bfd742948e45f25e5c1d4e803df10c1b2caa6c5805f4606f89758d9cac8e` | 3 |
| `flows/f55ec8/vision/networking.md` | `875494670ca7d221e6baa9ab365d2290438dba25f8fecfd0a4b220513ee0bf62` | 1 |
| `flows/f55ec8/vision/psycheLayers.md` | `353fe604e2877f17c0c94b165a54e7d20d28818e207cf09607fd012ab21c100a` | 1 |
| `flows/f55ec8/vision/psycheMedium.md` | `1a24698b6b46b01a19b65d86ca5f77fbe91cf1651739011cf301b05cafcde0a9` | 1 |
| `flows/f55ec8/vision/psycheTool.md` | `374083954decbaf7fb3e9cfaaae909b273ea8ee2deac9fe2fb15fd5cc1d548fa` | 1 |
| `flows/f55ec8/vision/quota.md` | `45d8161fd36deedab4413fd62e07e924ff11b481505594e2d24ad5118c567c5d` | 3 |
| `flows/f55ec8/vision/visualPublication.md` | `0f4c0a7149be2f7e12d71741954a973983e1af85e206272ae8a0e8bd9dc21618` | 3 |
| `flows/f6db8d/vision/arity.md` | `810b1fc205afb813da5f9e22e7ea8b2d9dcc77f36a840a09d29b7d2255c8c784` | 1 |
| `flows/f6db8d/vision/designPractice.md` | `589db665da17cf37c37f89cd6988616165c4d3ded980b8f2d2d95acb9d07b8bc` | 1 |
| `flows/f6db8d/vision/metaCli.md` | `6189c8cdaaef06597b37a1dffa19950124bed3d8921a13026dc6c21ed81a0a04` | 1 |
| `flows/f6db8d/vision/workPractice.md` | `0ead60797466fb82d5e880c79fffa213c0738b7127b088fed26474942abb9569` | 1 |
| `flows/fb1008c0/vision/context.md` | `f75521bc1d2d8f74ba264a5b4d2b899ae0f809a552752b809bdfd71d524221a1` | 1 |
| `flows/fb1008c0/vision/psycheLogStructure.md` | `4c05de270c587590deba9bcf43a3175b15d038709335924f400a8599a59d9a33` | 1 |
| `flows/fb1008c0/vision/skillDesigning.md` | `72da46bbb3073de95843a5109551757fa75d8faff428e70e8b38ce4c50c64dad` | 2 |
| `flows/fd0f97/vision/firstPrompt.md` | `257d045d2716a80d21e699f325fdb7e40d0b3e3b8385eb006ed5df9762f6792c` | 1 |
| `flows/fd0f97/vision/flowLifecycle.md` | `45b8e25a702c579a3df0f93dee1cf0dae29cf4281943df07c65f5e7d06871471` | 2 |
| `flows/fd0f97/vision/flowTypes.md` | `90a7c67b0de5f25892d57b44940ef308a6e5fc23e4bad9576472ff25c1822230` | 1 |
| `flows/fd0f97/vision/google.md` | `eba9cc781c25e9020a3a2a1bbb878da82f0186bce8de73561b301b9251550a87` | 1 |
| `flows/fd0f97/vision/identifiers.md` | `fe1ce0c2fef8c8ca3633ca06709cfb57471ec5eb3234b755a9d8d9410adc2c6f` | 1 |
| `flows/fd0f97/vision/launch.md` | `0dc92a832e0473b27eff22c87e699c60241ecb2032f406158f016054759e6856` | 4 |
| `flows/fd0f97/vision/layerNames.md` | `36ababeed50618a1b2f6a8eb20542d0068c07b0cea4c798942a3147c7ee1a05f` | 1 |
| `flows/fd0f97/vision/messages.md` | `ace6ec928c7fa4fc895916c198d852f5a9f9f16dc69cb0fd884a9f7115c3e311` | 2 |
| `flows/fd0f97/vision/notification.md` | `3dc168695b73993ce867eb090412c228750fa5ea43170147bd160d285d91791a` | 1 |
| `flows/fd0f97/vision/persona.md` | `319bca9e8293bcfa2c12a3b2da9fe95faded77de4b940f578d6aa60b011fb288` | 1 |
| `flows/fd0f97/vision/philosophy.md` | `4ff9d32458147b40bd1e5a5ada27585fe952d089a3797b2b86df76ac3d5fd1c4` | 1 |
| `flows/fd0f97/vision/psyche.md` | `de1839f03de0ef5066f5f80bc68bb0b094aa04900238f63e4821ba0dcd9abc93` | 1 |
| `flows/fd0f97/vision/relay.md` | `6542e47d9aa19426f1e0a0a85b9c49f1c5764d90c7f16e06079671cf50ac5921` | 1 |
| `flows/fd0f97/vision/remoteControl.md` | `800787781b8c1d0fb3f4441100f8e7614e41137a061b97af296105a3917e9ce1` | 1 |
| `flows/fd0f97/vision/visionUpkeep.md` | `25a5903e28fa0faa9cab36b64535d59639a99910ffa58586f71c868c03bc7241` | 1 |
| `flows/fd301d9a/vision/actorLibrary.md` | `427485134fb66d908271f6f843983fe9bde8ccad944c8ee6c3c38a478aad3222` | 7 |
| `flows/fd301d9a/vision/nexusTraits.md` | `0c4fa01252b25225f7b61012d7090a16fabbecda3312d6d8d94f053f387f47b1` | 2 |
| `flows/fe34eb/vision/datom.md` | `78a3b2d2447744d448546bed73114d1aa89f1a8958203d0b53ba94f0aa41967a` | 2 |
| `flows/fe34eb/vision/designPractice.md` | `c155296050eca49d4b5303d306d847115b16badc720cc4d6fbee4e043e90d725` | 1 |
| `flows/fe34eb/vision/ethos.md` | `d1327ce31c523782b049890e90ba58101ed5b5c4a6acb061f8987d6429989a94` | 4 |
| `flows/fe34eb/vision/nexus.md` | `dafd36de001f8eb755c64ae58def9715e8fbc8cae5cc7c2056b89224e1c3d397` | 7 |
| `flows/fe34eb/vision/reports.md` | `c731d64f34e4564d6570967dcc43a2b5c5466be947692785392359b4779d2ad1` | 1 |
| `flows/fe34eb/vision/signal.md` | `f13a46062f6bd996d675584d068e6e048e909d3f35de38a9954db5188bb637b3` | 3 |

### 2.9 archive (Vision raw) — 132 files

| path | sha256 | `## ` headings |
|---|---|---|
| `flows/012fbf07/vision/archive-threeStacks.md` | `d40ad08ad3bcd3ec663ab6c1458c2dd48c6a238f26931eb94225d517d4382cbd` | 8 |
| `flows/01a02a34/vision/archive-datum.md` | `6a4b86c69501120dc4c5f20580b8e41b1dc7b0d4011565cb63fbe2c19ce45c2a` | 2 |
| `flows/01a02a34/vision/archive-ethos.md` | `ea39bfd08d86c17464fb570a8519cbc19611ccbff2afd1f7c1688c0d7d1ff081` | 2 |
| `flows/01a02a34/vision/archive-schemaSyntax.md` | `778830bd7f492d8364fdaf34c89ae401cc794e668d10742002b4a9169dc03938` | 1 |
| `flows/01a02fd5/vision/archive-metaOrchestrate.md` | `00debccae9bd731b5243bba94bd78e3cb6fd601fc7cfced65fcfdddee78d84b5` | 2 |
| `flows/01a02fd5/vision/archive-nexuses.md` | `b45f6675e7f081e6c6aedf62ae66e71468485af046637f673f7e6d588f9c5a27` | 1 |
| `flows/01a035d3/vision/archive-rustCodeFromTheData.md` | `13ae92d0fdcd8479f32feebb8a4f6acc1e515e5f9f377b76039c90c9b2d2938a` | 2 |
| `flows/01a038be/vision/archive-x11.md` | `9491a6d22f3f68ac905a5e0736e49b1339662c9169339978d82ba71f3b2199d5` | 1 |
| `flows/01a03d6e/vision/archive-dotosFiles.md` | `d02cb45c7b4e45f62c51b1d6f10e22f0bd5e04b4d696a92aa7a49ca8df9d3fa6` | 2 |
| `flows/01a03d6e/vision/archive-ethosInterfaces.md` | `0f1610f7bc73b204dd1ba2f337076def21a9ff888f2e445f5aa819898f86ffd5` | 3 |
| `flows/01a03d6e/vision/archive-nexus.md` | `8224ea1f83c0c087909dcd72e629cadb7ce68994c292ad542d7664181c0f11a1` | 5 |
| `flows/01a03d6e/vision/archive-orchestrateDeployment.md` | `5fab7210dd243f5e1de3bfca6d5f8b80717c15babee768da62eb4a2e151b9f95` | 3 |
| `flows/01a03d6e/vision/archive-orchestrateSkill.md` | `f1d2030443ff09e9d04441ba07b9ba9d26987c861ae82e17b7088115563713b8` | 1 |
| `flows/01a03eda/vision/archive-datomInteger.md` | `5fea09193c3d9977a2c517a7a23e42757132b4b9d363f7d2cb792464b20dbb5a` | 1 |
| `flows/01a03eda/vision/archive-datomSyntax.md` | `e741b97a06a693d8680e2ed8400f537fd3dd3d6709a06cdaa01836ffa4869c42` | 1 |
| `flows/01a04339/vision/archive-datom.md` | `d8b6a197e0eb7d6e693c2544d5aa5f570553bb37e130d92a45537991da7fc59a` | 1 |
| `flows/01a05487/vision/archive-nexus.md` | `04e855e8201b42621f3fe3d92c6beb63707a0d1ce7449fcd6deeeb1ff3336b1f` | 0 |
| `flows/04db2fd2/vision/archive-anatomy.md` | `e66e989e554a6a64739ac085e28980b8aa0cfdf92ec823b3681c958785b638f6` | 6 |
| `flows/04db2fd2/vision/archive-datomMaps.md` | `e7ef75e244fee2d3918683bd320cb89b28ec52b02bfcab60000f7429800ce33d` | 1 |
| `flows/04db2fd2/vision/archive-datomNexus.md` | `cac5599fd2f4afaf1be264f0bb47ea923de772de1d732a269c1bebf6bc02ee9c` | 1 |
| `flows/04db2fd2/vision/archive-delimiters.md` | `4dbe29d8a9da8ee41c0f97852536a558f3f6265df5831834f94e18ef2cafc1c7` | 1 |
| `flows/04db2fd2/vision/archive-directionAsymmetry.md` | `31cbbb13861602926d620e164578ab7ba2dc3b159a259aadba1adaa881c70d1d` | 1 |
| `flows/04db2fd2/vision/archive-kinds.md` | `7dcfca88a89bb6e7c2875cccc0ade45f6cb9048330a382ac699072e6e054ce6e` | 11 |
| `flows/04db2fd2/vision/archive-multiPass.md` | `c4fee6d608ec4d40de5d6eef9b92d08feddcfa211814113e9c674a2d7e98d1ce` | 2 |
| `flows/04db2fd2/vision/archive-portion.md` | `ca2063a05b3f7923051495d545c4fb5e21a6018de610a379418634a587298093` | 9 |
| `flows/04db2fd2/vision/archive-text.md` | `a5d91016c6224a6a958de25c8214215957d39b043d1164b765454e1a561a931f` | 1 |
| `flows/04db2fd2/vision/archive-textualTypes.md` | `7672a75ecc5924ad5f561df8506bb5f226574eeb1f687b7edd8ecad64a005463` | 4 |
| `flows/06196cc7/vision/archive-datomSyntax.md` | `1ada43c170705b6410bfdd61c659fbe4118d095b01aec581b0de4ee7b9d0686f` | 10 |
| `flows/06196cc7/vision/archive-encodedFormIsTheCode.md` | `debe834bde2115cf2690695f5ee87c35a82213595cdd2d56b318c3bed687e910` | 2 |
| `flows/06196cc7/vision/archive-traitsAsCapabilities.md` | `a5a355d1791e7bea5871824c31e7ae45e96ee873f198aaf26b874cab123979fe` | 6 |
| `flows/15b67974/vision/archive-actorLibrary.md` | `bf121966c7a0b9ae1537e6e6c0083528cc4bfe13c3198b541219604987eb328b` | 2 |
| `flows/1a6ca4/vision/archive-datom.md` | `ba014fe53a2c4b4bc19b5b59b986e28ec9c55a56c58c7382afdb4cdb32ee790a` | 2 |
| `flows/1a6ca4/vision/archive-nexus.md` | `445eca73fd080e72357628c6e91274b1f365cd61706969d79e0f323d6b243ced` | 1 |
| `flows/1c282d/vision/archive-protosizable.md` | `0e907b8de32ffefb6ac73722cc1528a26e29d6ea9f668e4f8d11efcb4725e63c` | 3 |
| `flows/1c282d/vision/archive-vocabulary.md` | `76a2f43bf31ec6dab198f01b253066aa5f1ccd33ca502c7452e988785e24eac8` | 2 |
| `flows/2b34fafa/vision/archive-ethosNamespaces.md` | `43a7ad9da4b5d639f384894d4eb75a917606592f90cff95bb0be3a1c5e5f9a00` | 1 |
| `flows/2b34fafa/vision/archive-ethosSourceFiles.md` | `34a2a2858b360918898b1b1be8dab517caf35aae8d70324d3c6438a77c1fc7dc` | 2 |
| `flows/2b34fafa/vision/archive-traitsAsCapabilities.md` | `b0e520a248b79e9a04d6db76fa5534148cda9926088166db96234d4473d55688` | 1 |
| `flows/2ef42163/vision/archive-ethos.md` | `90173611332f8e0228e0a28e5ce1a6a5f362d1ef4e980608ffb5307cef6d32f4` | 1 |
| `flows/2ef42163/vision/archive-kinds.md` | `86fe109de28d860edc0fa6dfb137ef07150587b8a487ae3b6041fc192c176a5b` | 9 |
| `flows/358f143a/vision/archive-flowDaemon.md` | `0fd4bc35d75ddf73d5172e25cad2eb6974b553dbf26cf1eafb214ed1d6933b3d` | 1 |
| `flows/4d5fc7da/vision/archive-datom.md` | `3fcf73b1a77bafc5b63b3182aec3f52cad98981e2e7534e6d2b51fc2140833f0` | 1 |
| `flows/4decf7/vision/archive-datomSyntax.md` | `2a88695f7c4234187345fea59818c4effd700d624221b1a26bf16e13ef206f68` | 2 |
| `flows/4decf7/vision/archive-kinds.md` | `6f7ffc5dc69330250c4d7a9da08605aede419b1db944676a904963abeb8eb16d` | 2 |
| `flows/542442/vision/archive-datom.md` | `e5b0963c9e6182326c4e7284fca6a1e167d360e6808ce1d10de66e5e7fd2013f` | 1 |
| `flows/55d18f4f/vision/archive-rustComponentArchitecture.md` | `abb6c007f47bf54e7b7edbbdc143ddcb5a010d796ce693d7f0809663e755ff65` | 1 |
| `flows/55d18f4f/vision/archive-signalIsOurMessagingLayer.md` | `e38d99070a3e3dc9546402dfc76e23f67bd9104ea7b56212630e4a80fcbfdd43` | 1 |
| `flows/564f55/vision/archive-datom.md` | `f7f159f99c4979be0aff51970f22957169866e26bed452cd66414b6008ca465d` | 19 |
| `flows/564f55/vision/archive-ethos.md` | `7eb33b252eef6881d059ade0f6ba2d8309fd80bed59c048d0d9b99005064bad9` | 9 |
| `flows/564f55/vision/archive-nexus.md` | `58de299f8206219c26ce94572bf50921783d07bc28e20ffcef8c621a0e0acf56` | 1 |
| `flows/564f55/vision/archive-protos.md` | `e769598ecc607c3b42ebb72ad03b6285e1db79c8782b34be6ac6e56ee3a3871e` | 16 |
| `flows/564f55/vision/archive-sema.md` | `58ce4fb8b124c87379207d3f9edd7d94090160e4089b8eba277a15cfc38f01b3` | 1 |
| `flows/564f55/vision/archive-signal.md` | `b3b35635320655f85f992c4d707b0e6757ff27168f20b904578c50832d76a6cb` | 2 |
| `flows/5abf3be8/vision/archive-colonLegalInStringPosition.md` | `470ee0ef1a1d6dd0091c703cee1bb867bade133654dd2312851efc6ffcb60a23` | 0 |
| `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md` | `c755991288ca0068d04e2c39148612cb77ed48b1c04b51f3d50e7d66d5fde061` | 0 |
| `flows/62022e8f/vision/archive-concept.md` | `724c377f9a19f5218b5f4245292d1fd8ca8f43d651b9c8e97a805aed969790b4` | 5 |
| `flows/62022e8f/vision/archive-datomSyntax.md` | `06a207ec4780c12900370e1664a952ed5f253be6d9051dea62b9e569dc0b368a` | 1 |
| `flows/62022e8f/vision/archive-designPractice.md` | `a52cfed914a27c199480bb42a45ef0e91be1ce127d725d2451777d6c1e0cac91` | 2 |
| `flows/62022e8f/vision/archive-ethosTypes.md` | `8753bca2db0eceeae475de1884bd05b66ff9486085bb181e7b590be9b112c371` | 1 |
| `flows/62022e8f/vision/archive-headedAndContained.md` | `358451c26cf50dde663e775f38e30349876a8109de739ed0c64b656956e7fa04` | 2 |
| `flows/62022e8f/vision/archive-kinds.md` | `f475a29cefc7d5a31a36dfc803859cdf9cf68d8cd564870727c5e7bce89d9c19` | 5 |
| `flows/62022e8f/vision/archive-layers.md` | `980e56cc2998943c9231e96412b99cf899b3cb3846c396316e3c81485ecace6e` | 2 |
| `flows/62022e8f/vision/archive-passes.md` | `f9d1887f31d060f606488a1b6d9214d72d11b636642380ba17b20da53a960303` | 1 |
| `flows/62022e8f/vision/archive-symbols.md` | `2eadb81938da8348d0296108dcce10fb086b4412401d85f29d347ea50b198562` | 1 |
| `flows/62022e8f/vision/archive-vocabulary.md` | `e58008d3395813545c75b135b774e8a781f0cbcca07d1e84b5bb57d1a1efa1b3` | 3 |
| `flows/6329f1/vision/archive-ethos.md` | `706a8f72f3cea2864884c61b0319cec8ec818d7aa3ea0681ee51b265395a5fe9` | 2 |
| `flows/6329f1/vision/archive-protos.md` | `2d1757c159556e8e8d825ac91f119179d0a5383dcdd7ef85de9c99ca1d58c926` | 5 |
| `flows/6329f1/vision/archive-vocabulary.md` | `d1e18226dea4f4e5811f2ab3414efc20c7587568ec6ad0b5429d065c47eda4c6` | 1 |
| `flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md` | `72215f5afa3e0edc7879ffec75a09a5e20acc6002728b1239c92db1a38ed12a4` | 2 |
| `flows/6863ef19/vision/archive-traitsAsCapabilities.md` | `8e9e28c0b8d0b4e062e876e36f909a3e21a003e5f73e380ab7e0841a076add31` | 2 |
| `flows/98fbfa47/vision/archive-metaCliIsComponentDashMeta.md` | `67a98ef526c26b7fbf24eae0343a501f3dae015523d49afb9cba31a8f31d96b5` | 1 |
| `flows/98fbfa47/vision/archive-metaSignalNotOptional.md` | `e076484cf2ddfc922b63666b05257c7ded11ccd10619d48234f6763b2badc8fb` | 1 |
| `flows/995a164e/vision/archive-datomSyntax.md` | `d56acf26dea6c5718117947483a5c33bdc776c76c69c634fdbd0857035e27c55` | 1 |
| `flows/995a164e/vision/archive-ethosTypes.md` | `7029ea29a29e0c3ce8fc2728419aa19c5896c2659c28e1adfba9d28ffecc67b0` | 1 |
| `flows/a5587095/vision/archive-colonFormTransformerSyntax.md` | `72ef668e4c0bd64fa1ea3f6b1d36be5c76550e69e52ad9249e8483d89735073a` | 1 |
| `flows/a5587095/vision/archive-datomSyntax.md` | `cd27765c6c25bfeaf47e8050ded51757f1fbbbef267d96025d332654f100f2ea` | 3 |
| `flows/a5587095/vision/archive-protosIsTheSharedStyle.md` | `c6497231327e425f6c886d7a549d4860abc4c61bb109f51eed8c3175182d616d` | 9 |
| `flows/a5587095/vision/archive-structuredStringType.md` | `7febde07ad056888b885731f2b92ce54330f1952aac26908422e9c8d31535663` | 7 |
| `flows/a5587095/vision/archive-threeStacks.md` | `24c9b55a084075d3a4192a3b57e61725a6ff0293823c9172836d1f3b52f6168e` | 1 |
| `flows/aa4c7747/vision/archive-ethos.md` | `62ed8391df4de5df61d47e522a115a703a500878ebec820148b876ac5666979a` | 1 |
| `flows/aa4c7747/vision/archive-ethosMonolith.md` | `82a8b95a13419b6cc8d04afd6ba7770fa9e6ccd148fa19b6cbb4135072bf1578` | 4 |
| `flows/aa4c7747/vision/archive-ethosTraitSyntax.md` | `5888e4890f2906ac29d3d7d21c15b32ebf427debb16a62d90c106174727eb102` | 5 |
| `flows/aa4c7747/vision/archive-interactions.md` | `90ff07048095de66eb65f34b26cc23800530239bf5659be80275751cf19874d7` | 2 |
| `flows/aa4c7747/vision/archive-tuples.md` | `1b0bc87a6c7bd7b2b0de27d04326a60fe5f9b69f197dc0cbdc675750a1e5f674` | 1 |
| `flows/ac1e9ec8/vision/archive-datomIsData.md` | `ff8042e7e33c5b509a450428578e76b7213da8d0be9f1be056d0d001982b6508` | 1 |
| `flows/ac1e9ec8/vision/archive-datomSyntax.md` | `08c41a13388a33c8afbb2253f0fb982a6c2a8724ee85a246d9afe0aaa0626217` | 6 |
| `flows/ac1e9ec8/vision/archive-distillationNegatives.md` | `58ccde92d942adb99248b00fb44780518902ae46902443e579a5f14d791d768c` | 2 |
| `flows/acbb6006/vision/archive-distillation.md` | `0c5bc265c9f308653ae6e06baceef51b09efdeddd17f42569ea31c736c9cd535` | 5 |
| `flows/acbb6006/vision/archive-nexus.md` | `f9776583c1e38f6df5436c1a87436c77ca97729316e9eec34e485dac76246933` | 12 |
| `flows/ad19b1/vision/archive-datom.md` | `7af24ef4cb270b6743b9869e6ac7e88a48559642f4420ed637aa3b06017afe8d` | 3 |
| `flows/ad19b1/vision/archive-designPractice.md` | `4fe496660027a6f99ca1beec85ae2ed875b161094ec9d890b66e773949d59b0d` | 1 |
| `flows/ad19b1/vision/archive-ethos.md` | `bc05650b0a6444935e534eef39c34e9556781cee5603ba6f032d6332b1f518f9` | 4 |
| `flows/ad19b1/vision/archive-kinds.md` | `742f401b58a3887488e7cb43957a4774c36c2b4e413aee3da56aba8cdececaa2` | 5 |
| `flows/ad19b1/vision/archive-meaning.md` | `b57a656db1631fb9f15e67cb2b7ec202195e865e6ff51107900977818bb38369` | 3 |
| `flows/ad19b1/vision/archive-protos.md` | `95fea1d35ee65949d8f1c5389f9637c6ea92c8092a5b1fb7291f740482a9a11f` | 1 |
| `flows/b675f3d9/vision/archive-distillation.md` | `87eb946eb3f3d7ea6dafdced084d2057700a65c73b352e67a40b047e71e3923e` | 1 |
| `flows/b675f3d9/vision/archive-ethosMonolith.md` | `96c7f8e446e3ec969f9516cd374004d2699cad9961ee965a3977431d56efad7d` | 1 |
| `flows/b675f3d9/vision/archive-highLevelView.md` | `19b88733b875ca455b09992379be622fa0b06dc26dc9c2bceea9ed961edc738f` | 1 |
| `flows/b675f3d9/vision/archive-kinds.md` | `16e527328d82ad659d08f0a253c8dffb36b65634908b1d49112c1b77eec99db8` | 8 |
| `flows/b675f3d9/vision/archive-remembering.md` | `8c93ee83a1e056195d4527ee7104c96ed4c1a0c7dd003ebddd57697b5f06e272` | 3 |
| `flows/b675f3d9/vision/archive-structuralParsing.md` | `7c007c1e53c5cd88a81b2abc31a71e4df92226dac44c81754917473791febe02` | 3 |
| `flows/b675f3d9/vision/archive-visionImpurities.md` | `58740f703d4e02bfd166e1187ed6fc0d2643488fb2190e384fb13dcab5af5fad` | 4 |
| `flows/ba906ae2/vision/archive-encodedFormIsTheCode.md` | `f31691d2dbfcf87d95699d79a83093f011c611aa8919e2617ae3b461304db9d6` | 1 |
| `flows/ba906ae2/vision/archive-protosIsTheSharedStyle.md` | `9bd054fbda3f86b7d885d8e277e0c50b7357f7623a2cba88b6ca3db5a221e3de` | 1 |
| `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md` | `82a24a6f6565d5c40c27affa439d1cb5b479aaf267f0c9c947a4fb4d55e52a93` | 7 |
| `flows/ba906ae2/vision/archive-threeStacks.md` | `4f4da5875845165d3161d1a2ad656993dcfd23816486db0d8806c93d64a130e4` | 1 |
| `flows/bc05da32/vision/archive-interfaceRootEnumerators.md` | `c1ffc6c3e1671606578bbf0a63423ff48e942abe61448bbccf7a7efb081e925d` | 1 |
| `flows/c6b71b4c/vision/archive-threeStacks.md` | `8515af0a76709a645b5cdbe38b232733d60386df0cd72e167ab6a4a4eee2b4d1` | 3 |
| `flows/d63804f2/vision/archive-interfaceRootEnumerators.md` | `16feae9f79d7ea7e31e93b9bf3f322023d5a900e2e235c11b5eed0d775452140` | 1 |
| `flows/db97561c/vision/archive-nexus.md` | `918a4560f619fe3415fb4246997790341afbc054b2c789251744040023cebc58` | 1 |
| `flows/db97561c/vision/archive-prospective.md` | `fa92b0d4c3e16eef4396719ec18ad9b9c09436ed5d8d2dba74e2fd7a8b99e14e` | 4 |
| `flows/e06e4c07/vision/archive-flowDaemon.md` | `4e4c58de77402bec1456c0fbe5431116083aff00eeef143807018c2b4c79e3c9` | 1 |
| `flows/e06e4c07/vision/archive-nexus.md` | `05bc5af408c0c620ae6f272f29d502f4504f0fe4527eedc1e00dfc800da977ad` | 5 |
| `flows/e4a40e/vision/archive-datom.md` | `6077021b18601cfcfab43c096af00d8dea6b7d27a49b8db5dce266c4d1900ee9` | 5 |
| `flows/e4a40e/vision/archive-kinds.md` | `7f398daba6347a03d8764f897dd6e50eb15bde9c033e2ed29153f3aaae1eea92` | 2 |
| `flows/e4a40e/vision/archive-newtypeWrappingAndSingleFieldStructs.md` | `c9662cef47b3aebae59ecf8ef12d888d3735cba5912f1f8a76e3c91826d05b19` | 1 |
| `flows/e4a40e/vision/archive-protos.md` | `4f1fd19f8561ea552af678a8338b99dfb69a3554ca6e3ce3a366012b5235b94b` | 1 |
| `flows/e4a40e/vision/archive-vocabulary.md` | `4321cf9d9a4a450cd4ae623db37e595b2cf0daccab8b90f2131ea4679852b179` | 1 |
| `flows/e8c4cc61/vision/archive-datomSyntax.md` | `24ccb9b7577e3232fcffd3950bb413df660d4189b7e20f9c772c9f63226f4f6a` | 2 |
| `flows/e8c4cc61/vision/archive-datomizable.md` | `ec62272a432d76b48789105c4ffa6d2b252ff88df3165e313e18e59c100be8d5` | 5 |
| `flows/e8c4cc61/vision/archive-ethosFileAnatomy.md` | `a8f801383967aa0848acb21973ec5c2a96d82c46a39dbe82c17befb4bb2eb2ef` | 7 |
| `flows/e8c4cc61/vision/archive-ethosTypes.md` | `7b150577de2eec0e89500a0337bf9d5bb1932bfd16553e9c7675fb71d23de2e5` | 2 |
| `flows/e8c4cc61/vision/archive-kinds.md` | `5fd4f6b6b4343063b80c81a7c8324ee08b421fa4a9e637d4d4ab82e84c75c734` | 10 |
| `flows/e8c4cc61/vision/archive-prospective.md` | `da75d92c6406074f896ab31606a8abfd5a449a9cfae4f78a20b98534afb7291f` | 6 |
| `flows/e8c4cc61/vision/archive-protos.md` | `9c4970def437d1eafe69604ff75d92b6a8e505993c1d52a507bf6e562aec0aff` | 2 |
| `flows/e996e8/vision/archive-datom.md` | `3bfddea0ccdabb97646575ac6d9fd775528e853b945afb9ca47f167112bced67` | 2 |
| `flows/e996e8/vision/archive-ethos.md` | `6670931f411f87495d2a1b379e1d4bd70d9cf3376da9d5e1edddf4475c3d3e9d` | 1 |
| `flows/e996e8/vision/archive-protos.md` | `42ac65da3e2170114eef7db300c0eb134f3cbe45c8ec0d0c131dd69402f74bb7` | 3 |
| `flows/f426777b/vision/archive-ethosSourceFiles.md` | `e20925495c8371827fcbe45babb610524f7131889d5f1c6d9eb6a1e30430f00b` | 2 |
| `flows/f426777b/vision/archive-nexusTraits.md` | `b06f1ff63356c5dbb4f4125a1a5f03d6d63d56716a2d51f906b384f5913d18e7` | 3 |
| `flows/f426777b/vision/archive-spokenVocabulary.md` | `8305ebc62c62d872ac2ab8d803e0ef02d31e7e92720a4cb0bbaa51d6f3b359ee` | 4 |
| `flows/fd301d9a/vision/archive-nexusTraits.md` | `0d0db42287470dd9b7f865bbb39761c460f3e028a3944fe1b5b3438a85ec0f79` | 3 |

### 2.10 Notion (raw) — 28 files

| path | sha256 | `## ` headings |
|---|---|---|
| `flows/01a04e75/notion/continuousRecordingUsingWisprFlowChunks.md` | `210dae018b2c5030fa90855deddce3481d0f66559f62a9a4fd5938e23711d189` | 1 |
| `flows/01a05487/notion/rollingCodexServices.md` | `2e8c1db659f4cde13975399dc4d81063190283825cf51cf9a7ed9e5a9214a936` | 0 |
| `flows/024bc7/notion/ethosDelta.md` | `1226c9880996950e0c3aae0528f9477d24e16a5f7900c53690316a495574bcfa` | 1 |
| `flows/05c604/notion/layers.md` | `2ce4ec3353d8921d77e2fa96e56519ed35e6e40b180e08b597b0676765eb37fc` | 1 |
| `flows/542442/notion/pod.md` | `2d9c3e6a6d7f70f9943097da3f1fa31b3bfdfb9c0dff357be1697ea3ec6e1202` | 1 |
| `flows/542442/notion/terminology.md` | `d0a909a2ddd2c15b6f0ea1b4e3a385081b4ffff6bc5a3c80d84f6cdc0c06fcfe` | 1 |
| `flows/564f55/notion/datom.md` | `2254a4a96be8858473f3b058a03ceaacacefad43e634f00437db1edc697b9c8f` | 2 |
| `flows/62022e8f/notion/layerMatching.md` | `5040688becc19eba032a8a95334117e47c0edcb5b12e9d0702889baa5b48f79e` | 4 |
| `flows/62022e8f/notion/terminology.md` | `e94e6284cb2c3a40319e1857bc80c86d491d0206fe7ce073f85c563f4ef54ee7` | 1 |
| `flows/692df8/notion/logging.md` | `2f718e562c6caa7ddc5e8e1a7166739589704ab71cda3fc7478bf974928cb1ef` | 2 |
| `flows/6cc91b/notion/datomMcp.md` | `bc7eb486487f682fbaf6c3402c67727d33acdd09d3ed5c49274aa05592a5c204` | 1 |
| `flows/6cc91b/notion/harnessPurity.md` | `d36a3d979c113eeb3c601de20305987c47e7d9fafbc7ed0f7fd33a4149a27186` | 1 |
| `flows/6cc91b/notion/orchestrator.md` | `7d323d9366331f253338608a151a742dfc26496d88bb640a45101cc9ebef0d3c` | 1 |
| `flows/6cc91b/notion/persona.md` | `7d52866139cfdcfec19919a6dc85b67fdd2812b9e6bc35cdf2bb518d8c11f6e6` | 1 |
| `flows/753090/notion/speech-to-text.md` | `f15ecd1479fe294539ea6030c0f2be624fdbb984f0eefe85e3e0a4957eb1af14` | 1 |
| `flows/bcd02a/notion/ethos.md` | `ebcc58f64484c25e36402badf2733aabd4a8049fcd2b6bdd0c7e7fb5e10a9acf` | 2 |
| `flows/bcd02a/notion/models.md` | `7ed7725de7a6a5aa5f169acc9eab15065cb2ff7d8e3ef94f53dcac08688d0141` | 1 |
| `flows/bcd02a/notion/nexus.md` | `a7ee7387fa5582eb7b7f07d5bb04023f32426b10acc5c8f9e241a66b52c97430` | 1 |
| `flows/bcd02a/notion/persona.md` | `233b197e3b1203e756253eb9d64b0e6cfdd654f260390c5b56d1588c69f22a4d` | 2 |
| `flows/bcd02a/notion/prometheus.md` | `983634db53e0194ac54ec096a58e316beebe1fe5cad59adca43973c39a569c44` | 1 |
| `flows/bcd02a/notion/router.md` | `372392215bd40be9ef037a1b9971c2a6df48d8af6b6da926c85d12dba9a830b6` | 2 |
| `flows/bcd02a/notion/sandbox.md` | `834095e4e65d6eb1f21877a97978335e57ea454f445361b52b267c36500cc38a` | 2 |
| `flows/bcd02a/notion/speech.md` | `39fc25a1d5aa6342ac832f2a89ab2c03ea5eb20a7c7a5951c37bb50c27645005` | 1 |
| `flows/bcd02a/notion/web-conversations.md` | `3104e974ce8cea4ba323b67d239e63fa0976dadf47f842881204f3cfc93b80fd` | 1 |
| `flows/ceb3b9fd/notion/thinkingProcess.md` | `536a9c18d8cb76361ba5e58b8dbf52717cb78d4f7766b9fa1e0c840514fd569b` | 1 |
| `flows/d1c570/notion/pairs.md` | `c57f357de28e860b8f706a9229cd9b83f7b78381b0df192ab7ed1e7443b1bda2` | 1 |
| `flows/dc1c58/notion/meta-flow.md` | `ec6f1bb0fe3ffd700cc40a1b681044535b6cee5741c65251f9287b60936508d2` | 1 |
| `flows/fe34eb/notion/reports.md` | `7d4a38cef22ab96c13d913174f18d43b019b91411e30bb2c8f7893da875ff8d4` | 1 |

### 2.11 Out-of-glob handoff-bundle vision records — 89 files (NOT part of the enumerated corpus)

| path | sha256 | `## ` headings |
|---|---|---|
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/flowLaunching.md` | `897ef337afe694dd7ce30cc1ce16dd2b4a1046afaeaaf8d88f6dca11abeee0c6` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/heartbeat.md` | `a22b36fa01e98394ba1c0c7cdfe57ef7ac20552b0ab9b34096d23eed2479f075` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/layers.md` | `de2789b87ef5ce6b77dcfad765f2ed833d8c78ec6ca4a4c9b28fda0c080a1da3` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/nexusAnatomy.md` | `8cc0677146f5b4b96bbd811bfb3ec0fdeb17a4cb88d9102edb5b4171f163ea03` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/psycheFlows.md` | `590b2709e7b873c219f0b684afb2db3dd5e4151184b60f069ce2382ea18c287e` | 5 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/quota.md` | `418a13c72beaf8bb2682aaf90e32b653203dcf970f6d69f5871287c7c187b61c` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/subflowDispatch.md` | `894eb73377feff1343680d895b7396d8162747b713c84bd701d30f386065e502` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/systemPrompt.md` | `f7c460ef911ecbc07d21260154a33f061d0243022cab87a99453c670f954e226` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/b49251/vision/visualPublication.md` | `11f26e5ab70e5aa6b916af4ba7d2828b405d681e755e4fdd8bf59f133393a402` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/authority.md` | `e2555343149b5acaddfb187ace6a0c48ad2e9ec0edaaf4c32a5639e76acd5007` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/branches.md` | `00aba2b8190081d536e776d815adc229e2f4f76f650f52a19108550212deecfd` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/callerIdentity.md` | `8dddddb97051248728f6d12b207b94236d08fca78369138f777c6a50d7bf7744` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/cloudHosts.md` | `2cac8870644be7b98839320abbb3a24d416940b8727f80c88d901cecdbe51e3f` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/cloud.md` | `d37d070f4c409639c429df2d3705e897e0bde57cce59c232d832a393dc5fccfd` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/codexAccess.md` | `4d5dd312422bb0bcf03e812ef6acf47f5a06063d0838035e4d433fd5dfa4eaff` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/deployment.md` | `92c116a0d1af1d06f6f82c910dc672e0d914f17b5acb4b120672d605ff88b542` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/distillation.md` | `488d4f97e18894b337b2c241d7e3d3740bfec53d2202202c4939ce64e2bc93b4` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/domains.md` | `2bc3ff53c66d8a153ead8ee4cdc1f23d72bfe754355e4290987b913ebc1a0f7f` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/harnessRepositories.md` | `736d78a203f129d9efcd86f70f6249e199664faae6ad0f76d2422d6004cbb422` | 2 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/heartbeat.md` | `c4bb5d9448ea959bb5609abbbf0d412be6fbec0378ba7fae4d9413cfa06adc46` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/incrementalRuntime.md` | `5d104423d33e95bf33c76ad66edb60da2259b314603a47e3a7331dbb4d49eab7` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/law.md` | `e6e7e2e3b1bdb12f714eb1010ae320a38ad1422adb4b496de52e16ddf4871701` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/layers.md` | `34437b8ff81eae327deccf14920c44ea56174536a06b518ab7374d2804ecf0ae` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/lojix.md` | `1d5aa5ae6588ce6dc4bd22189a9c9b138cdf9dac09c13a7099ac60cfb1147862` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/mcp.md` | `4ee2bdb445fc93987fb6c7a608c527fda5b149cfbb416f63344ac37ce520737e` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/messages.md` | `06c584e025e93118b66db510352822ec0b80ae65150b2b14bdb13ad2669692f9` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/modelRoles.md` | `21810663aef82e27ef13549b9c2b3946a0472792cf149a4b69b49e24b6904aac` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/operation.md` | `d0c9d78679076d968a38469871199c8d71e32712cb31643dfd164d5767cc129b` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/parallelContext.md` | `20ee4d161cc2863af696887348b06d5f7bd0163507ea8c313f3a1044a7729857` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/quota.md` | `fecee1eab27f85c9bbf86f042f2a0f2b0fc5ea9425b4cdd4f7ef747fde2519ee` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/scripts.md` | `be2bfac178a9a97fb6e30e2ae60bf6f0d34f7e3e9ff1393c53a5242239a8f260` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/sema.md` | `78d5e74e814ad2fb0c716d074705af495b0cf539a2cc5c6bfcc6a773810c25c2` | 2 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/skillApproval.md` | `6e88c600fcd03f01680dd951d2a57098c8f9490a1f4a33ff9181166443b9f75b` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/specificationVersionControl.md` | `46704821a20a90bb06244b7d67b9d84bf3c2b51e4a00e157e7c1ca4bb533e355` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/subflowDispatch.md` | `7e6395e3aa08bb5462cc3e54788b2af626571777e3e8a541c9c2321b16bd479d` | 3 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/syntaxHighlighting.md` | `a6841fb36850a992f4aaf1c2505d2aeb1e05081191b6d6d810fa3056e3718074` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/systemPrompt.md` | `bf0e1add453f8f4766bc4119c33895370b34be5f42ffdd9fde9e42c6e7c62fc6` | 2 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/testing.md` | `964639a2199142b2ffa5173c112ba6edcfd62f4adf0cab61fab543e5169230e0` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/tokenEfficiency.md` | `ca4595d934c844d696a404f01bf57935b9ca967242aacb62fbfd7e5c7c24c2da` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/transcriptReporting.md` | `5ebd0de05306ba180874daeecbe0554c1f59f7a1eb86e5346c5b0a1163ead14a` | 2 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/versionControl.md` | `d23c17a0983146137860863cc625db089b80d9c75a3e29f476856063fdb87995` | 2 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/cloud.md` | `71df66f466b83f89fd1072ddc2266ae6ec02eccc54f75359fc0032123171a8f4` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/flowIdentity.md` | `c9faa16fd9e37ff50d21db69a6081cdb5cca5d522a4d9b110664603800bfd9e6` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/flowRefresh.md` | `ff00bebac96df321a5f76985b17b3188319a3a17d980dda1d1eac95aa1b04de8` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/heartbeat.md` | `a65c7d6b1af8e7c074bffd551b458f030e00f5317e9d7661ae3ad41a2144690a` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/layers.md` | `bc4c0d9ed990cd76813170569685ac05c33faec999a2ec93e4a77f1bb3ed4cbc` | 4 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/modelRoles.md` | `cee6bfd742948e45f25e5c1d4e803df10c1b2caa6c5805f4606f89758d9cac8e` | 3 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/networking.md` | `875494670ca7d221e6baa9ab365d2290438dba25f8fecfd0a4b220513ee0bf62` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/psycheTool.md` | `374083954decbaf7fb3e9cfaaae909b273ea8ee2deac9fe2fb15fd5cc1d548fa` | 1 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/quota.md` | `45d8161fd36deedab4413fd62e07e924ff11b481505594e2d24ad5118c567c5d` | 3 |
| `flows/b49251/handoff/psyche-medium-v1/modules/sources/f55ec8/vision/visualPublication.md` | `cebf7cf52965a8fa2adcff53fd29af5d21a4e76c23e2931498f48aba81d6827f` | 2 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/branches.md` | `00aba2b8190081d536e776d815adc229e2f4f76f650f52a19108550212deecfd` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/cloudHosts.md` | `2cac8870644be7b98839320abbb3a24d416940b8727f80c88d901cecdbe51e3f` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/cloud.md` | `d37d070f4c409639c429df2d3705e897e0bde57cce59c232d832a393dc5fccfd` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/codexAccess.md` | `4d5dd312422bb0bcf03e812ef6acf47f5a06063d0838035e4d433fd5dfa4eaff` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/deployment.md` | `92c116a0d1af1d06f6f82c910dc672e0d914f17b5acb4b120672d605ff88b542` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/distillation.md` | `488d4f97e18894b337b2c241d7e3d3740bfec53d2202202c4939ce64e2bc93b4` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/domains.md` | `2bc3ff53c66d8a153ead8ee4cdc1f23d72bfe754355e4290987b913ebc1a0f7f` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/harnessRepositories.md` | `3305bd473666b58133f6cfcabe439b52a2b749dc07a9ec96271838de34dda969` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/heartbeat.md` | `c4bb5d9448ea959bb5609abbbf0d412be6fbec0378ba7fae4d9413cfa06adc46` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/incrementalRuntime.md` | `5d104423d33e95bf33c76ad66edb60da2259b314603a47e3a7331dbb4d49eab7` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/law.md` | `e6e7e2e3b1bdb12f714eb1010ae320a38ad1422adb4b496de52e16ddf4871701` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/layers.md` | `34437b8ff81eae327deccf14920c44ea56174536a06b518ab7374d2804ecf0ae` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/lojix.md` | `1d5aa5ae6588ce6dc4bd22189a9c9b138cdf9dac09c13a7099ac60cfb1147862` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/mcp.md` | `4ee2bdb445fc93987fb6c7a608c527fda5b149cfbb416f63344ac37ce520737e` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/messages.md` | `06c584e025e93118b66db510352822ec0b80ae65150b2b14bdb13ad2669692f9` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/modelRoles.md` | `21810663aef82e27ef13549b9c2b3946a0472792cf149a4b69b49e24b6904aac` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/operation.md` | `d0c9d78679076d968a38469871199c8d71e32712cb31643dfd164d5767cc129b` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/parallelContext.md` | `20ee4d161cc2863af696887348b06d5f7bd0163507ea8c313f3a1044a7729857` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/scripts.md` | `be2bfac178a9a97fb6e30e2ae60bf6f0d34f7e3e9ff1393c53a5242239a8f260` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/sema.md` | `78d5e74e814ad2fb0c716d074705af495b0cf539a2cc5c6bfcc6a773810c25c2` | 2 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/skillApproval.md` | `6e88c600fcd03f01680dd951d2a57098c8f9490a1f4a33ff9181166443b9f75b` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/specificationVersionControl.md` | `46704821a20a90bb06244b7d67b9d84bf3c2b51e4a00e157e7c1ca4bb533e355` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/subflowDispatch.md` | `09faf06d5961d63c08a0d63f78932063e0f343e34e2afaf74b7458ea70683c5b` | 2 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/syntaxHighlighting.md` | `a6841fb36850a992f4aaf1c2505d2aeb1e05081191b6d6d810fa3056e3718074` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/systemPrompt.md` | `bf0e1add453f8f4766bc4119c33895370b34be5f42ffdd9fde9e42c6e7c62fc6` | 2 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/testing.md` | `964639a2199142b2ffa5173c112ba6edcfd62f4adf0cab61fab543e5169230e0` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/tokenEfficiency.md` | `ca4595d934c844d696a404f01bf57935b9ca967242aacb62fbfd7e5c7c24c2da` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/transcriptReporting.md` | `69fb2d33d4e905d12f4b7865153f3b1bf1714981c106435947f5f3abf14d1396` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/versionControl.md` | `d23c17a0983146137860863cc625db089b80d9c75a3e29f476856063fdb87995` | 2 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/cloud.md` | `71df66f466b83f89fd1072ddc2266ae6ec02eccc54f75359fc0032123171a8f4` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/flowIdentity.md` | `c9faa16fd9e37ff50d21db69a6081cdb5cca5d522a4d9b110664603800bfd9e6` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/flowRefresh.md` | `ff00bebac96df321a5f76985b17b3188319a3a17d980dda1d1eac95aa1b04de8` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/layers.md` | `bc4318335eee4ac5a89c471be31f242236b14437a2a1adc5d251c74064233df8` | 3 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/modelRoles.md` | `cee6bfd742948e45f25e5c1d4e803df10c1b2caa6c5805f4606f89758d9cac8e` | 3 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/networking.md` | `875494670ca7d221e6baa9ab365d2290438dba25f8fecfd0a4b220513ee0bf62` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/psycheTool.md` | `374083954decbaf7fb3e9cfaaae909b273ea8ee2deac9fe2fb15fd5cc1d548fa` | 1 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/quota.md` | `45d8161fd36deedab4413fd62e07e924ff11b481505594e2d24ad5118c567c5d` | 3 |
| `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/visualPublication.md` | `cebf7cf52965a8fa2adcff53fd29af5d21a4e76c23e2931498f48aba81d6827f` | 2 |

## 3. Explicit recorded relationships

Every edge below is stated by the file in the "stated in" column. The quotation is
the exact phrase that states it. Where a stated target does not resolve to a file at
this revision, that is recorded rather than repaired.

**Totals: 642 explicit edges** — 181 source-index, 107 archive-distillation,
1 retirement, 353 in-record cross-reference. A further 109 stated references do not
resolve to an enumerated file and are listed in 3.5 and 3.6 as references, not edges.

### 3.1 Source-index edges — 181

A `Vision/sources/<topic>.md` or `Intent/sources/<topic>.md` file is an index whose
every line names a raw record that fed the distilled topic of the same name. The
file's own `# Sources — <topic>` heading states the relation; each line is one edge,
written as `<flow-short-id> <topic>` or `vision-raw <topic>`. All 181 lines resolve
to a file at this revision (134 of them to the `archive-` form of the named topic,
which is how a raw record is marked once its words have landed in a distilled file).

**`Vision/sources/datom.md`** — index for `Vision/datom.md`, 47 lines. Quoted heading: `# Sources — datom`.

| line (quoted) | resolves to |
|---|---|
| `ac1e9ec8 datomSyntax` | `flows/ac1e9ec8/vision/archive-datomSyntax.md` (archived form) |
| `ac1e9ec8 datomIsData` | `flows/ac1e9ec8/vision/archive-datomIsData.md` (archived form) |
| `01a03eda datomInteger` | `flows/01a03eda/vision/archive-datomInteger.md` (archived form) |
| `04db2fd2 datomMaps` | `flows/04db2fd2/vision/archive-datomMaps.md` (archived form) |
| `04db2fd2 datomNexus` | `flows/04db2fd2/vision/archive-datomNexus.md` (archived form) |
| `04db2fd2 text` | `flows/04db2fd2/vision/archive-text.md` (archived form) |
| `04db2fd2 textualTypes` | `flows/04db2fd2/vision/archive-textualTypes.md` (archived form) |
| `04db2fd2 anatomy` | `flows/04db2fd2/vision/archive-anatomy.md` (archived form) |
| `04db2fd2 portion` | `flows/04db2fd2/vision/archive-portion.md` (archived form) |
| `04db2fd2 directionAsymmetry` | `flows/04db2fd2/vision/archive-directionAsymmetry.md` (archived form) |
| `e8c4cc61 datomSyntax` | `flows/e8c4cc61/vision/archive-datomSyntax.md` (archived form) |
| `e8c4cc61 datomizable` | `flows/e8c4cc61/vision/archive-datomizable.md` (archived form) |
| `e8c4cc61 protos` | `flows/e8c4cc61/vision/archive-protos.md` (archived form) |
| `62022e8f datomSyntax` | `flows/62022e8f/vision/archive-datomSyntax.md` (archived form) |
| `62022e8f kinds` | `flows/62022e8f/vision/archive-kinds.md` (archived form) |
| `62022e8f symbols` | `flows/62022e8f/vision/archive-symbols.md` (archived form) |
| `62022e8f headedAndContained` | `flows/62022e8f/vision/archive-headedAndContained.md` (archived form) |
| `995a164e datomSyntax` | `flows/995a164e/vision/archive-datomSyntax.md` (archived form) |
| `01a04339 datom` | `flows/01a04339/vision/archive-datom.md` (archived form) |
| `01a035d3 rustCodeFromTheData` | `flows/01a035d3/vision/archive-rustCodeFromTheData.md` (archived form) |
| `01a03d6e dotosFiles` | `flows/01a03d6e/vision/archive-dotosFiles.md` (archived form) |
| `01a03d6e ethosInterfaces` | `flows/01a03d6e/vision/archive-ethosInterfaces.md` (archived form) |
| `a5587095 structuredStringType` | `flows/a5587095/vision/archive-structuredStringType.md` (archived form) |
| `5abf3be8 colonLegalInStringPosition` | `flows/5abf3be8/vision/archive-colonLegalInStringPosition.md` (archived form) |
| `06196cc7 datomSyntax` | `flows/06196cc7/vision/archive-datomSyntax.md` (archived form) |
| `b675f3d9 structuralParsing` | `flows/b675f3d9/vision/archive-structuralParsing.md` (archived form) |
| `4decf7 datomSyntax` | `flows/4decf7/vision/archive-datomSyntax.md` (archived form) |
| `e4a40e datom` | `flows/e4a40e/vision/archive-datom.md` (archived form) |
| `e4a40e vocabulary` | `flows/e4a40e/vision/archive-vocabulary.md` (archived form) |
| `e4a40e newtypeWrappingAndSingleFieldStructs` | `flows/e4a40e/vision/archive-newtypeWrappingAndSingleFieldStructs.md` (archived form) |
| `06196cc7 encodedFormIsTheCode` | `flows/06196cc7/vision/archive-encodedFormIsTheCode.md` (archived form) |
| `a5587095 datomSyntax` | `flows/a5587095/vision/archive-datomSyntax.md` (archived form) |
| `a5587095 threeStacks` | `flows/a5587095/vision/archive-threeStacks.md` (archived form) |
| `a5587095 colonFormTransformerSyntax` | `flows/a5587095/vision/archive-colonFormTransformerSyntax.md` (archived form) |
| `a5587095 protosIsTheSharedStyle` | `flows/a5587095/vision/archive-protosIsTheSharedStyle.md` (archived form) |
| `01a03eda datomSyntax` | `flows/01a03eda/vision/archive-datomSyntax.md` (archived form) |
| `vision-raw datomSyntax` | `vision-raw/archive-datomSyntax.md` (archived form) |
| `ad19b1 meaning` | `flows/ad19b1/vision/archive-meaning.md` (archived form) |
| `ad19b1 datom` | `flows/ad19b1/vision/archive-datom.md` (archived form) |
| `ad19b1 protos` | `flows/ad19b1/vision/archive-protos.md` (archived form) |
| `e996e8 datom` | `flows/e996e8/vision/archive-datom.md` (archived form) |
| `564f55 datom` | `flows/564f55/vision/datom.md` |
| `564f55 protos` | `flows/564f55/vision/archive-protos.md` (archived form) |
| `4d5fc7da datom` | `flows/4d5fc7da/vision/archive-datom.md` (archived form) |
| `1a6ca4 datom` | `flows/1a6ca4/vision/archive-datom.md` (archived form) |
| `fe34eb datom` | `flows/fe34eb/vision/datom.md` |
| `542442 datom` | `flows/542442/vision/archive-datom.md` (archived form) |

**`Vision/sources/distillation.md`** — index for `Vision/distillation.md`, 4 lines. Quoted heading: `# Sources — distillation`.

| line (quoted) | resolves to |
|---|---|
| `b675f3d9 visionImpurities` | `flows/b675f3d9/vision/visionImpurities.md` |
| `acbb6006 distillation` | `flows/acbb6006/vision/distillation.md` |
| `b675f3d9 distillation` | `flows/b675f3d9/vision/distillation.md` |
| `ac1e9ec8 distillationNegatives` | `flows/ac1e9ec8/vision/distillationNegatives.md` |

**`Vision/sources/ethos.md`** — index for `Vision/ethos.md`, 42 lines. Quoted heading: `# Sources — ethos`.

| line (quoted) | resolves to |
|---|---|
| `01a02a34 ethos` | `flows/01a02a34/vision/archive-ethos.md` (archived form) |
| `01a02a34 schemaSyntax` | `flows/01a02a34/vision/archive-schemaSyntax.md` (archived form) |
| `vision-raw ethosDotosDivisionAndHelp` | `vision-raw/archive-ethosDotosDivisionAndHelp.md` (archived form) |
| `vision-raw ethosNonRepetitionLaw` | `vision-raw/archive-ethosNonRepetitionLaw.md` (archived form) |
| `f426777b spokenVocabulary` | `flows/f426777b/vision/archive-spokenVocabulary.md` (archived form) |
| `b675f3d9 kinds` | `flows/b675f3d9/vision/archive-kinds.md` (archived form) |
| `6863ef19 traitsAsCapabilities` | `flows/6863ef19/vision/archive-traitsAsCapabilities.md` (archived form) |
| `06196cc7 traitsAsCapabilities` | `flows/06196cc7/vision/archive-traitsAsCapabilities.md` (archived form) |
| `2b34fafa traitsAsCapabilities` | `flows/2b34fafa/vision/archive-traitsAsCapabilities.md` (archived form) |
| `04db2fd2 kinds` | `flows/04db2fd2/vision/archive-kinds.md` (archived form) |
| `5abf3be8 encodedFormFingerprintTraitDesign` | `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md` (archived form) |
| `4decf7 kinds` | `flows/4decf7/vision/archive-kinds.md` (archived form) |
| `2ef42163 ethos` | `flows/2ef42163/vision/archive-ethos.md` (archived form) |
| `e8c4cc61 kinds` | `flows/e8c4cc61/vision/archive-kinds.md` (archived form) |
| `b675f3d9 structuralParsing` | `flows/b675f3d9/vision/archive-structuralParsing.md` (archived form) |
| `ac1e9ec8 datomSyntax` | `flows/ac1e9ec8/vision/archive-datomSyntax.md` (archived form) |
| `e4a40e kinds` | `flows/e4a40e/vision/archive-kinds.md` (archived form) |
| `ad19b1 kinds` | `flows/ad19b1/vision/archive-kinds.md` (archived form) |
| `e8c4cc61 ethosFileAnatomy` | `flows/e8c4cc61/vision/archive-ethosFileAnatomy.md` (archived form) |
| `e8c4cc61 kinds` | `flows/e8c4cc61/vision/archive-kinds.md` (archived form) |
| `995a164e ethosTypes` | `flows/995a164e/vision/archive-ethosTypes.md` (archived form) |
| `62022e8f ethosTypes` | `flows/62022e8f/vision/archive-ethosTypes.md` (archived form) |
| `aa4c7747 interactions` | `flows/aa4c7747/vision/archive-interactions.md` (archived form) |
| `aa4c7747 tuples` | `flows/aa4c7747/vision/archive-tuples.md` (archived form) |
| `aa4c7747 ethosTraitSyntax` | `flows/aa4c7747/vision/archive-ethosTraitSyntax.md` (archived form) |
| `2b34fafa ethosSourceFiles` | `flows/2b34fafa/vision/archive-ethosSourceFiles.md` (archived form) |
| `2b34fafa ethosNamespaces` | `flows/2b34fafa/vision/archive-ethosNamespaces.md` (archived form) |
| `b675f3d9 kinds` | `flows/b675f3d9/vision/archive-kinds.md` (archived form) |
| `b675f3d9 structuralParsing` | `flows/b675f3d9/vision/archive-structuralParsing.md` (archived form) |
| `ad19b1 ethos` | `flows/ad19b1/vision/archive-ethos.md` (archived form) |
| `ad19b1 designPractice` | `flows/ad19b1/vision/archive-designPractice.md` (archived form) |
| `6329f1 ethos` | `flows/6329f1/vision/archive-ethos.md` (archived form) |
| `e996e8 ethos` | `flows/e996e8/vision/archive-ethos.md` (archived form) |
| `ad19b1 protos` | `flows/ad19b1/vision/archive-protos.md` (archived form) |
| `564f55 ethos` | `flows/564f55/vision/ethos.md` |
| `564f55 datom` | `flows/564f55/vision/datom.md` |
| `564f55 signal` | `flows/564f55/vision/archive-signal.md` (archived form) |
| `aa4c7747 ethos` | `flows/aa4c7747/vision/archive-ethos.md` (archived form) |
| `e8c4cc61 ethosTypes` | `flows/e8c4cc61/vision/archive-ethosTypes.md` (archived form) |
| `ba906ae2 signalIsOurMessagingLayer` | `flows/ba906ae2/vision/signalIsOurMessagingLayer.md` |
| `62022e8f designPractice` | `flows/62022e8f/vision/designPractice.md` |
| `fe34eb ethos` | `flows/fe34eb/vision/ethos.md` |

**`Vision/sources/ethosMonolith.md`** — index for `Vision/ethosMonolith.md`, 3 lines. Quoted heading: `# Sources — ethosMonolith`.

| line (quoted) | resolves to |
|---|---|
| `vision-raw threeStacks` | `vision-raw/archive-threeStacks.md` (archived form) |
| `vision-raw rustComponentArchitecture` | `vision-raw/rustComponentArchitecture.md` |
| `aa4c7747 ethosMonolith` | `flows/aa4c7747/vision/archive-ethosMonolith.md` (archived form) |

**`Vision/sources/flowNexus.md`** — index for `Vision/flowNexus.md`, 6 lines. Quoted heading: `# Sources — flowNexus`.

| line (quoted) | resolves to |
|---|---|
| `358f143a flowDaemon` | `flows/358f143a/vision/flowDaemon.md` |
| `e06e4c07 flowDaemon` | `flows/e06e4c07/vision/flowDaemon.md` |
| `acbb6006 nexus` | `flows/acbb6006/vision/archive-nexus.md` (archived form) |
| `1a6ca4 nexus` | `flows/1a6ca4/vision/archive-nexus.md` (archived form) |
| `1ac573 operational-nameSessionAfterAncestor` | `flows/1ac573/vision/operational-nameSessionAfterAncestor.md` |
| `1ac573 operational-reapReplacedSessions` | `flows/1ac573/vision/operational-reapReplacedSessions.md` |

**`Vision/sources/highLevelView.md`** — index for `Vision/highLevelView.md`, 2 lines. Quoted heading: `# Sources — highLevelView`.

| line (quoted) | resolves to |
|---|---|
| `vision-raw highLevelView` | `vision-raw/highLevelView.md` |
| `b675f3d9 highLevelView` | `flows/b675f3d9/vision/highLevelView.md` |

**`Vision/sources/messaging.md`** — index for `Vision/messaging.md`, 5 lines. Quoted heading: `# Sources — messaging`.

| line (quoted) | resolves to |
|---|---|
| `108ab0 operational-messageAsDatomInPrompt` | `flows/108ab0/vision/operational-messageAsDatomInPrompt.md` |
| `108ab0 operational-messagePriorityTiers` | `flows/108ab0/vision/operational-messagePriorityTiers.md` |
| `108ab0 operational-abruptPerHarness` | `flows/108ab0/vision/operational-abruptPerHarness.md` |
| `108ab0 operational-herderMuxKeypress` | `flows/108ab0/vision/operational-herderMuxKeypress.md` |
| `1ac573 operational-modelRoles` | `flows/1ac573/vision/operational-modelRoles.md` |

**`Vision/sources/modelRoles.md`** — index for `Vision/modelRoles.md`, 6 lines. Quoted heading: `# Sources — modelRoles`.

| line (quoted) | resolves to |
|---|---|
| `f55ec8 modelRoles` | `flows/f55ec8/vision/modelRoles.md` |
| `f55ec8 layers` | `flows/f55ec8/vision/layers.md` |
| `1ac573 operational-modelRoles` | `flows/1ac573/vision/operational-modelRoles.md` |
| `1ac573 operational-olderOpusIs46` | `flows/1ac573/vision/operational-olderOpusIs46.md` |
| `1ac573 operational-defaultModelPsycheMediumClaude` | `flows/1ac573/vision/operational-defaultModelPsycheMediumClaude.md` |
| `1ac573 operational-modelDeclaredInOnePlace` | `flows/1ac573/vision/operational-modelDeclaredInOnePlace.md` |

**`Vision/sources/nexus.md`** — index for `Vision/nexus.md`, 14 lines. Quoted heading: `# Sources — nexus`.

| line (quoted) | resolves to |
|---|---|
| `e06e4c07 nexus` | `flows/e06e4c07/vision/archive-nexus.md` (archived form) |
| `01a03d6e nexus` | `flows/01a03d6e/vision/archive-nexus.md` (archived form) |
| `acbb6006 nexus` | `flows/acbb6006/vision/archive-nexus.md` (archived form) |
| `98fbfa47 metaCliIsComponentDashMeta` | `flows/98fbfa47/vision/metaCliIsComponentDashMeta.md` |
| `012fbf07 threeStacks` | `flows/012fbf07/vision/threeStacks.md` |
| `15b67974 actorLibrary` | `flows/15b67974/vision/actorLibrary.md` |
| `564f55 nexus` | `flows/564f55/vision/archive-nexus.md` (archived form) |
| `01a05487 nexus` | `flows/01a05487/vision/archive-nexus.md` (archived form) |
| `db97561c nexus` | `flows/db97561c/vision/archive-nexus.md` (archived form) |
| `fd301d9a nexusTraits` | `flows/fd301d9a/vision/nexusTraits.md` |
| `f426777b nexusTraits` | `flows/f426777b/vision/archive-nexusTraits.md` (archived form) |
| `f426777b ethosSourceFiles` | `flows/f426777b/vision/archive-ethosSourceFiles.md` (archived form) |
| `b675f3d9 ethosMonolith` | `flows/b675f3d9/vision/archive-ethosMonolith.md` (archived form) |
| `fe34eb nexus` | `flows/fe34eb/vision/nexus.md` |

**`Vision/sources/orchestrate.md`** — index for `Vision/orchestrate.md`, 2 lines. Quoted heading: `# Sources — orchestrate`.

| line (quoted) | resolves to |
|---|---|
| `01a03d6e orchestrateDeployment` | `flows/01a03d6e/vision/orchestrateDeployment.md` |
| `01a03d6e orchestrateSkill` | `flows/01a03d6e/vision/orchestrateSkill.md` |

**`Vision/sources/protos.md`** — index for `Vision/protos.md`, 30 lines. Quoted heading: `# Sources — protos`.

| line (quoted) | resolves to |
|---|---|
| `a5587095 protosIsTheSharedStyle` | `flows/a5587095/vision/archive-protosIsTheSharedStyle.md` (archived form) |
| `ba906ae2 protosIsTheSharedStyle` | `flows/ba906ae2/vision/archive-protosIsTheSharedStyle.md` (archived form) |
| `ba906ae2 encodedFormIsTheCode` | `flows/ba906ae2/vision/archive-encodedFormIsTheCode.md` (archived form) |
| `e4a40e protos` | `flows/e4a40e/vision/archive-protos.md` (archived form) |
| `04db2fd2 anatomy` | `flows/04db2fd2/vision/archive-anatomy.md` (archived form) |
| `04db2fd2 multiPass` | `flows/04db2fd2/vision/archive-multiPass.md` (archived form) |
| `04db2fd2 portion` | `flows/04db2fd2/vision/archive-portion.md` (archived form) |
| `04db2fd2 delimiters` | `flows/04db2fd2/vision/archive-delimiters.md` (archived form) |
| `e8c4cc61 protos` | `flows/e8c4cc61/vision/archive-protos.md` (archived form) |
| `e8c4cc61 prospective` | `flows/e8c4cc61/vision/archive-prospective.md` (archived form) |
| `e8c4cc61 kinds` | `flows/e8c4cc61/vision/archive-kinds.md` (archived form) |
| `62022e8f kinds` | `flows/62022e8f/vision/archive-kinds.md` (archived form) |
| `62022e8f layers` | `flows/62022e8f/vision/archive-layers.md` (archived form) |
| `62022e8f concept` | `flows/62022e8f/vision/archive-concept.md` (archived form) |
| `62022e8f passes` | `flows/62022e8f/vision/archive-passes.md` (archived form) |
| `62022e8f vocabulary` | `flows/62022e8f/vision/archive-vocabulary.md` (archived form) |
| `2ef42163 kinds` | `flows/2ef42163/vision/archive-kinds.md` (archived form) |
| `b675f3d9 structuralParsing` | `flows/b675f3d9/vision/archive-structuralParsing.md` (archived form) |
| `b675f3d9 kinds` | `flows/b675f3d9/vision/archive-kinds.md` (archived form) |
| `1c282d protosizable` | `flows/1c282d/vision/archive-protosizable.md` (archived form) |
| `1c282d vocabulary` | `flows/1c282d/vision/archive-vocabulary.md` (archived form) |
| `ad19b1 ethos` | `flows/ad19b1/vision/archive-ethos.md` (archived form) |
| `6329f1 protos` | `flows/6329f1/vision/archive-protos.md` (archived form) |
| `6329f1 vocabulary` | `flows/6329f1/vision/archive-vocabulary.md` (archived form) |
| `04db2fd2 directionAsymmetry` | `flows/04db2fd2/vision/archive-directionAsymmetry.md` (archived form) |
| `ad19b1 protos` | `flows/ad19b1/vision/archive-protos.md` (archived form) |
| `e996e8 protos` | `flows/e996e8/vision/archive-protos.md` (archived form) |
| `564f55 protos` | `flows/564f55/vision/archive-protos.md` (archived form) |
| `564f55 datom` | `flows/564f55/vision/datom.md` |
| `564f55 signal` | `flows/564f55/vision/archive-signal.md` (archived form) |

**`Vision/sources/remembering.md`** — index for `Vision/remembering.md`, 1 lines. Quoted heading: `# Sources — remembering`.

| line (quoted) | resolves to |
|---|---|
| `b675f3d9 remembering` | `flows/b675f3d9/vision/remembering.md` |

**`Vision/sources/sema.md`** — index for `Vision/sema.md`, 5 lines. Quoted heading: `# Sources — sema`.

| line (quoted) | resolves to |
|---|---|
| `564f55 sema` | `flows/564f55/vision/archive-sema.md` (archived form) |
| `564f55 ethos` | `flows/564f55/vision/ethos.md` |
| `f426777b ethosSourceFiles` | `flows/f426777b/vision/archive-ethosSourceFiles.md` (archived form) |
| `62022e8f designPractice` | `flows/62022e8f/vision/designPractice.md` |
| `aa4c7747 ethosMonolith` | `flows/aa4c7747/vision/archive-ethosMonolith.md` (archived form) |

**`Vision/sources/signal.md`** — index for `Vision/signal.md`, 7 lines. Quoted heading: `# Sources — signal`.

| line (quoted) | resolves to |
|---|---|
| `564f55 signal` | `flows/564f55/vision/archive-signal.md` (archived form) |
| `564f55 protos` | `flows/564f55/vision/archive-protos.md` (archived form) |
| `55d18f4f signalIsOurMessagingLayer` | `flows/55d18f4f/vision/archive-signalIsOurMessagingLayer.md` (archived form) |
| `6863ef19 signalIsOurMessagingLayer` | `flows/6863ef19/vision/signalIsOurMessagingLayer.md` |
| `ba906ae2 signalIsOurMessagingLayer` | `flows/ba906ae2/vision/signalIsOurMessagingLayer.md` |
| `98fbfa47 metaSignalNotOptional` | `flows/98fbfa47/vision/archive-metaSignalNotOptional.md` (archived form) |
| `fe34eb signal` | `flows/fe34eb/vision/signal.md` |

**`Intent/sources/anatomy.md`** — index for `Intent/anatomy.md`, 1 lines. Quoted heading: `# Sources — anatomy`.

| line (quoted) | resolves to |
|---|---|
| `1a6ca4 datom` | `flows/1a6ca4/vision/archive-datom.md` (archived form) |

**`Intent/sources/context.md`** — index for `Intent/context.md`, 2 lines. Quoted heading: `# Sources — context`.

| line (quoted) | resolves to |
|---|---|
| `564f55 datom` | `flows/564f55/vision/datom.md` |
| `564f55 protos` | `flows/564f55/vision/archive-protos.md` (archived form) |

**`Intent/sources/conversion.md`** — index for `Intent/conversion.md`, 2 lines. Quoted heading: `# Sources — conversion`.

| line (quoted) | resolves to |
|---|---|
| `564f55 protos` | `flows/564f55/vision/archive-protos.md` (archived form) |
| `564f55 datom` | `flows/564f55/vision/datom.md` |

**`Intent/sources/models.md`** — index for `Intent/models.md`, 2 lines. Quoted heading: `# Sources — models`.

| line (quoted) | resolves to |
|---|---|
| `1ac573 operational-effortIsAlwaysMedium` | `flows/1ac573/vision/operational-effortIsAlwaysMedium.md` |
| `024bc7 effort` | `flows/024bc7/vision/effort.md` |

### 3.2 Archive-header distillation edges — 107 (from 100 archived raw records)

Each archived raw record opens with a header stating where its words were carried,
which flow carried them, and when. Several name two targets, hence 107 edges from 100
files. Six edges point at a file that does not exist at this revision; they are marked
DANGLING and are listed with the others rather than silently dropped.

| archived record | stated target | status | quoted header |
|---|---|---|---|
| `flows/012fbf07/vision/archive-threeStacks.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/012fbf07/vision/archive-threeStacks.md` | `Vision/ethosMonolith.md` | DANGLING | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/01a02a34/vision/archive-datum.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/01a02a34/vision/archive-ethos.md` | `Vision/ethos.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/ethos. |
| `flows/01a02a34/vision/archive-ethos.md` | `Vision/ethosMonolith.md` | DANGLING | Archived 2026-08-23 by flow 68512643; distilled into Vision/ethos. |
| `flows/01a02a34/vision/archive-schemaSyntax.md` | `Vision/ethos.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/ethos. |
| `flows/01a035d3/vision/archive-rustCodeFromTheData.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/01a03d6e/vision/archive-dotosFiles.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/01a03d6e/vision/archive-ethosInterfaces.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/01a03eda/vision/archive-datomInteger.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/01a03eda/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/01a04339/vision/archive-datom.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/04db2fd2/vision/archive-anatomy.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/04db2fd2/vision/archive-anatomy.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/04db2fd2/vision/archive-datomMaps.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/04db2fd2/vision/archive-datomNexus.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/04db2fd2/vision/archive-delimiters.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/04db2fd2/vision/archive-directionAsymmetry.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/04db2fd2/vision/archive-directionAsymmetry.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/04db2fd2/vision/archive-kinds.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/04db2fd2/vision/archive-multiPass.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/04db2fd2/vision/archive-portion.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/04db2fd2/vision/archive-text.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/04db2fd2/vision/archive-textualTypes.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/06196cc7/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/06196cc7/vision/archive-encodedFormIsTheCode.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/06196cc7/vision/archive-traitsAsCapabilities.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/1c282d/vision/archive-protosizable.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/1c282d/vision/archive-vocabulary.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/2b34fafa/vision/archive-ethosNamespaces.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/2b34fafa/vision/archive-ethosSourceFiles.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/2b34fafa/vision/archive-traitsAsCapabilities.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/2ef42163/vision/archive-ethos.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/2ef42163/vision/archive-kinds.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/2ef42163/vision/archive-kinds.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/4decf7/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/4decf7/vision/archive-kinds.md` | `Vision/kinds.md` | DANGLING | Archived on landing: these words were distilled as they were spoken, into Vision/kinds. |
| `flows/542442/vision/archive-datom.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled, with the "logics" confirmation heard in flow fe34eb, into Vision/datom. |
| `flows/5abf3be8/vision/archive-colonLegalInStringPosition.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/62022e8f/vision/archive-concept.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/62022e8f/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/62022e8f/vision/archive-ethosTypes.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/62022e8f/vision/archive-headedAndContained.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/62022e8f/vision/archive-kinds.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/62022e8f/vision/archive-kinds.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/62022e8f/vision/archive-layers.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/62022e8f/vision/archive-passes.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/62022e8f/vision/archive-symbols.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/62022e8f/vision/archive-vocabulary.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/6329f1/vision/archive-ethos.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/6329f1/vision/archive-protos.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/6329f1/vision/archive-vocabulary.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/6863ef19/vision/archive-traitsAsCapabilities.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/995a164e/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/995a164e/vision/archive-ethosTypes.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/a5587095/vision/archive-colonFormTransformerSyntax.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/a5587095/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/a5587095/vision/archive-protosIsTheSharedStyle.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/a5587095/vision/archive-structuredStringType.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/a5587095/vision/archive-threeStacks.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/aa4c7747/vision/archive-ethosMonolith.md` | `Vision/ethosMonolith.md` | DANGLING | Archived on landing: distilled into Vision/ethosMonolith. |
| `flows/aa4c7747/vision/archive-ethosTraitSyntax.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/aa4c7747/vision/archive-interactions.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/aa4c7747/vision/archive-tuples.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/ac1e9ec8/vision/archive-datomIsData.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/ac1e9ec8/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/ac1e9ec8/vision/archive-datomSyntax.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/ad19b1/vision/archive-datom.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/ad19b1/vision/archive-ethos.md` | `Vision/ethos.md` | OK | Archived on landing: the spacing record is distilled into Vision/protos. |
| `flows/ad19b1/vision/archive-ethos.md` | `Vision/protos.md` | OK | Archived on landing: the spacing record is distilled into Vision/protos. |
| `flows/ad19b1/vision/archive-kinds.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/ad19b1/vision/archive-meaning.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/ad19b1/vision/archive-protos.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/ad19b1/vision/archive-protos.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/b675f3d9/vision/archive-kinds.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/b675f3d9/vision/archive-structuralParsing.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/b675f3d9/vision/archive-structuralParsing.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/b675f3d9/vision/archive-structuralParsing.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/ba906ae2/vision/archive-encodedFormIsTheCode.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/ba906ae2/vision/archive-protosIsTheSharedStyle.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/ba906ae2/vision/archive-threeStacks.md` | `Vision/ethosMonolith.md` | DANGLING | Archived 2026-08-23 by flow 68512643; distilled into Vision/ethosMonolith. |
| `flows/bc05da32/vision/archive-interfaceRootEnumerators.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/c6b71b4c/vision/archive-threeStacks.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/d63804f2/vision/archive-interfaceRootEnumerators.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `flows/e4a40e/vision/archive-datom.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/e4a40e/vision/archive-kinds.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/e4a40e/vision/archive-newtypeWrappingAndSingleFieldStructs.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/e4a40e/vision/archive-protos.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/e4a40e/vision/archive-vocabulary.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/e8c4cc61/vision/archive-datomizable.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/e8c4cc61/vision/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived on landing: these words were distilled as they were spoken, into Vision/datom. |
| `flows/e8c4cc61/vision/archive-ethosFileAnatomy.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/e8c4cc61/vision/archive-kinds.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/e8c4cc61/vision/archive-kinds.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/e8c4cc61/vision/archive-prospective.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/e8c4cc61/vision/archive-protos.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/e996e8/vision/archive-datom.md` | `Vision/datom.md` | OK | Archived on landing: distilled into Vision/datom. |
| `flows/e996e8/vision/archive-ethos.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `flows/e996e8/vision/archive-protos.md` | `Vision/protos.md` | OK | Archived on landing: distilled into Vision/protos. |
| `flows/f426777b/vision/archive-spokenVocabulary.md` | `Vision/ethos.md` | OK | Archived on landing: distilled into Vision/ethos. |
| `vision-raw/archive-datomSyntax.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `vision-raw/archive-ethosDotosDivisionAndHelp.md` | `Vision/ethos.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/ethos. |
| `vision-raw/archive-ethosNonRepetitionLaw.md` | `Vision/ethos.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/ethos. |
| `vision-raw/archive-threeStacks.md` | `Vision/datom.md` | OK | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `vision-raw/archive-threeStacks.md` | `Vision/ethosMonolith.md` | DANGLING | Archived 2026-08-23 by flow 68512643; distilled into Vision/datom. |
| `vision-raw/archive-traitsAsCapabilities.md` | `Vision/ethos.md` | OK | Archived as superseded by "code/encoded dropped" and "textualize is approved" (transcodable vocabulary, 06196cc7/ba906ae2), "no Create alias over TryFrom/From" (aa4c7747), and qualifier-named kinds (Vision/ethos. |

### 3.3 Retirement edge — 1

| stated in | target | quoted |
|---|---|---|
| `Vision/archive-ethosMonolith.md` (file head, before `# Ethos-monolith`) | `Vision/ethos.md`, heading `Zero` | "Retired on landing by flow fe34eb, 2026-09-10. The living ruled Ethos Monolith and Ethos Zero the same thing: the name was changed, there is no separate stage. What still stands is carried by Vision/ethos.md, heading Zero; the words are kept here." |

This is the only retirement of a distilled Vision topic recorded in the corpus. It is
also the reason six edges in 3.2 and one index in 3.1 (`Vision/sources/ethosMonolith.md`)
point at `Vision/ethosMonolith.md`, a path that no longer exists.

### 3.4 In-record cross-reference edges — 353

A record states a relation to another record by naming it: "the message continues in
X.md", "pairs with X.md", "same date", "Source: <path>", "supersedes the earlier ...".
One row per distinct (source, target) pair; where a pair is stated more than once the
first statement is quoted. The quotation is truncated to 260 characters where longer.

| stated in | heading | target | quoted phrase |
|---|---|---|---|
| `Intent/data.md`:22 | (file head) Data | `flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md` | flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md. |
| `Intent/protosParsing.md`:23 | (file head) Protos parsing | `flows/6863ef19/vision/encodedFormIsTheCode.md` | *(2026-08-14 annotation, consistency audit  "two-way structural transcoding" in this provenance paragraph is dead vocabulary — code/encoded was dropped 2026-08-13 per encodedFormIs |
| `Vision/archive-ethosMonolith.md`:3 | (file head) | `Vision/ethos.md` | no separate stage. What still stands is carried by Vision/ethos.md, |
| `Vision/psyche.md`:8 | (file head) Psyche | `flows/8393ca/vision/operational-herdrVoiceAccess.md` | `flows/8393ca/vision/operational-herdrVoiceAccess.md` (archive ordinal 1833). |
| `flows/012fbf07/vision/archive-threeStacks.md`:93 | 2026-08-11 — datom is just a renamed dotos; no new repo was needed | `vision-raw/parserIsTheParser.md` | with parserIsTheParser.md  one parser, nothing else implements its |
| `flows/01a02b46/vision/zeusUpdate.md`:75 | 2026-08-09T13:00:32.409Z — universal cluster/home fix | `flows/019fe641/vision/hostEnvironmentRecovery.md` | `flows/019fe641/vision/hostEnvironmentRecovery.md` records |
| `flows/01a02b46/vision/zeusUpdate.md`:49 | 2026-08-13T15:40:20+02:00, 2026-08-13T23:32:19+02:00, and 2026-08-14T09:06+02:00 — Lojix b | `vision-raw/lojixOwnership.md` | `psyche-raw/Vision/lojixOwnership.md` records |
| `flows/06196cc7/vision/archive-datomSyntax.md`:14 | 2026-08-13 — Meaning postponed in datom; () or curly quotes both land as String for now | `vision-raw/structuredStringType.md` | pointing at the later Meaning type (structuredStringType.md). This |
| `flows/06196cc7/vision/archive-encodedFormIsTheCode.md`:12 | 2026-08-13 — "working" rejected: it smells like a verb | `vision-raw/structuredStringType.md` | (structuredStringType.md, bead primary-xqb.8.5) — to be raised |
| `flows/06196cc7/vision/archive-encodedFormIsTheCode.md`:22 | 2026-08-14 — the real form; Realize | `vision-raw/traitsAsCapabilities.md` | paired with protos  Textualize (traitsAsCapabilities.md |
| `flows/06196cc7/vision/archive-traitsAsCapabilities.md`:23 | 2026-08-13 — a type for the text block; textualize on the true type; maybe drop code/encod | `flows/6863ef19/vision/encodedFormIsTheCode.md` | on encodedFormIsTheCode.md 2026-08-06 ("the encoded form is the |
| `flows/1030529c/vision/workspace20.md`:6 | 2026-08-14T00:27+02:00 — shared parent workspace per aspect; sub workspace per flow; aware | `flows/f55ec8/vision/cloud.md` | Ellipses mark trims. "cloud" is dictation for Claude; "cloud.md" for |
| `flows/108ab0/vision/operational-designMosaic.md`:46 | Governance of vision and skills | `flows/564f55/notion/datom.md` | - Skill IS vision. Same file. A topic has faces  core (`datom.md`), extended (`datom-extended.md` or `datom/extended.md`), subtopic-specific (`datom-strings.md`). |
| `flows/108ab0/vision/operational-diskHygiene.md`:5 | Send someone to garbage collect old worktrees, clean up leftover build directories, and ar | `flows/108ab0/vision/operational-sameTreeAndMerger.md` | Context  same message as `operational-sameTreeAndMerger.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-distillationHierarchy.md`:5 | What runs today is Vision, Intent, Spirit. Notion is below Vision — a distilled Notion tha | `flows/108ab0/vision/operational-primaryIsPsyche.md` | Context  same message as `operational-primaryIsPsyche.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-flowCliListAttachProvenance.md`:5 | Flow startup from the CLI just creates the herdr job for now. Flow knows where to find flo | `flows/108ab0/vision/operational-promptMosaicComposition.md` | Context  typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 in the same message as `operational-promptMosaicComposition.md`, closing the design of the Flow CL |
| `flows/108ab0/vision/operational-flowStartsFlows.md`:5 | We need an easy way to start Flow, and for a Flow to start a new flow just by calling Flow | `flows/108ab0/vision/operational-messageAsDatomInPrompt.md` | Context  same message as `operational-multiplexerInjection.md` and `operational-messageAsDatomInPrompt.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-flowStartsFlows.md`:5 | We need an easy way to start Flow, and for a Flow to start a new flow just by calling Flow | `flows/108ab0/vision/operational-multiplexerInjection.md` | Context  same message as `operational-multiplexerInjection.md` and `operational-messageAsDatomInPrompt.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-freshPrimary.md`:5 | Change primary. Fork from the first commit onto a new branch, copy only the bare minimum a | `flows/108ab0/vision/operational-diskHygiene.md` | Context  same message as `operational-sameTreeAndMerger.md` and `operational-diskHygiene.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-freshPrimary.md`:5 | Change primary. Fork from the first commit onto a new branch, copy only the bare minimum a | `flows/108ab0/vision/operational-sameTreeAndMerger.md` | Context  same message as `operational-sameTreeAndMerger.md` and `operational-diskHygiene.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-messageAsDatomInPrompt.md`:5 | The specification: messages come in directly from the message CLI. It returns the string,  | `flows/108ab0/vision/operational-multiplexerInjection.md` | Context  same message as `operational-multiplexerInjection.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-operationalSkillsRepo.md`:5 | Operational is the stuff the agents write. It lives in a different repo — a different modu | `flows/108ab0/vision/operational-skillIsVisionUnified.md` | Context  same message as `operational-skillIsVisionUnified.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-programmaticPromptComposition.md`:5 | Load vision-as-skills at the first prompt, using skill variables and the skill-loading syn | `flows/108ab0/vision/operational-curriculumAsModuleSystem.md` | Context  same message as `operational-curriculumAsModuleSystem.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-pushMessagingForEmergency.md`:5 | We need the push server style for time-type system emergencies — time-based things that ha | `flows/108ab0/vision/operational-timeBasedMergeSlots.md` | Context  typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 in the same message as `operational-timeBasedMergeSlots.md`. Logged by the main flow before acting |
| `flows/108ab0/vision/operational-skillIsVisionUnified.md`:5 | Unify. There is no separate Datom skill and Datom vision — same thing. A topic has faces:  | `flows/108ab0/vision/operational-coreAndExtendedVision.md` | Context  typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 while writing the restart artifact, extending the earlier `operational-skillsAreVision.md` and `op |
| `flows/108ab0/vision/operational-skillIsVisionUnified.md`:5 | Unify. There is no separate Datom skill and Datom vision — same thing. A topic has faces:  | `flows/108ab0/vision/operational-skillsAreVision.md` | Context  typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 while writing the restart artifact, extending the earlier `operational-skillsAreVision.md` and `op |
| `flows/108ab0/vision/operational-skillLagsVisionObservability.md`:5 | Consider using Curriculum at runtime with vision files as one of the sources for skill gen | `flows/108ab0/vision/operational-curriculumSkillsRepo.md` | Context  typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 in the same message that named `curriculum-skills` (see `operational-curriculumSkillsRepo.md`). Li |
| `flows/108ab0/vision/operational-skillTypes.md`:5 | Give skills a type when they are created. Not every type is agent-accessible — some are ju | `flows/108ab0/vision/operational-curriculumAsModuleSystem.md` | Context  same message as `operational-curriculumAsModuleSystem.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-skillsAreVision.md`:5 | Skills are basically vision. An operational skill can be agent-written on a light proposal | `flows/108ab0/vision/operational-distillationHierarchy.md` | Context  same message as `operational-primaryIsPsyche.md` and `operational-distillationHierarchy.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/108ab0/vision/operational-skillsAreVision.md`:5 | Skills are basically vision. An operational skill can be agent-written on a light proposal | `flows/108ab0/vision/operational-primaryIsPsyche.md` | Context  same message as `operational-primaryIsPsyche.md` and `operational-distillationHierarchy.md`, 2026-09-17. Logged by the main flow before acting. |
| `flows/15b67974/vision/entryFiles.md`:5 | 2026-08-22 — entry files taken over completely; workspace specifics in @-prefixed secondar | `vision-raw/spirit.md` | (spirit.md, same date) |
| `flows/15b67974/vision/letsUseTheSameVocabulary.md`:4 | 2026-08-22 — the living is a perfect shorthand for living psyche | `flows/012fbf07/vision/psycheLogStructure.md` | coined mid-ruling (the full message in psycheLogStructure.md, same |
| `flows/15b67974/vision/psycheLogStructure.md`:87 | 2026-08-22 — forks ruled: psyche-raw good; the case split liked; raw intent and spirit onl | `flows/15b67974/vision/entryFiles.md` | entry files) in spirit.md and entryFiles.md, same date. |
| `flows/15b67974/vision/psycheLogStructure.md`:68 | 2026-08-22 — a skill is still a file; rename the undistilled corpus; log vision: flows/<id | `vision-raw/spirit.md` | logged in spirit.md (2026-08-22). |
| `flows/1ac573/vision/operational-fableFlowAndOpusComparison.md`:17 | I'm not sure if the old Opus is better than you. You can maybe talk about that with Fable. | `flows/1ac573/vision/operational-mirroredMessagesAreAddressed.md` | `operational-mirroredMessagesAreAddressed.md`  a mirrored statement keeps its |
| `flows/1ac573/vision/operational-mirrorToEveryoneAndRoster.md`:11 | Pass all of the psyche messages along to everyone, and stay aware of how many flows there  | `flows/1ac573/vision/operational-psycheMindAstra.md` | `operational-psycheMindAstra.md` for the Astra half. Logged by the main flow |
| `flows/2ef42163/vision/archive-kinds.md`:61 | there's no Embodied; embody returns the actual type, which implements Embodiable | `flows/04db2fd2/vision/psycheLogging.md` | STT corrections made in the quote  "returns to actual type" → "returns the actual type"; "rest" (three times) → "Rust"; "casted" → "cast". The psyche corrected the transcription in |
| `flows/4ddc321d/vision/hijackRepositories.md`:52 | 2026-08-26 — skills block: first line mark | `flows/1a6ca4/vision/flow.md` | in vision/flow.md. |
| `flows/4ddc321d/vision/hijackRepositories.md`:39 | 2026-08-26 — personality block marked | `flows/4ddc321d/vision/subjectivity.md` | Upon the refined diagnosis (see vision/subjectivity.md) |
| `flows/4decf7/vision/archive-kinds.md`:4 | (file head) Kinds | `flows/995a164e/vision/kinds.md` | into Vision/kinds.md (Kind, Naming), flow 4decf7, 2026-09-03. Their |
| `flows/55d18f4f/vision/itsATranslator.md`:12 | 2026-08-08T11:47:07.277Z — its misnamed. its a translator. it translates code into text. r | `flows/6863ef19/vision/encodedFormIsTheCode.md` | *(2026-08-14 annotation, consistency audit  "code" here is used in the pre-drop sense — the encoded/binary form; code/encoded vocabulary was dropped 2026-08-13 per encodedFormIsThe |
| `flows/564f55/vision/archive-ethos.md`:70 | 2026-09-09 — the derived name for the data-carrying variant: yes; Signal's root enums are  | `flows/fe34eb/vision/ethos.md` | See flows/fe34eb/vision/nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/564f55/vision/archive-ethos.md`:70 | 2026-09-09 — the derived name for the data-carrying variant: yes; Signal's root enums are  | `flows/fe34eb/vision/nexus.md` | See flows/fe34eb/vision/nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/564f55/vision/archive-nexus.md`:14 | 2026-09-09 — the nexus core, the nexus kernel: the core logic of the nexus, not the daemon | `flows/fe34eb/vision/ethos.md` | See flows/fe34eb/vision/nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/564f55/vision/archive-nexus.md`:14 | 2026-09-09 — the nexus core, the nexus kernel: the core logic of the nexus, not the daemon | `flows/fe34eb/vision/nexus.md` | See flows/fe34eb/vision/nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md`:21 | (file head) "encodedform trait must implement the fingerprint trait" | `flows/15b67974/vision/letsUseTheSameVocabulary.md` | letsUseTheSameVocabulary.md  TrueName is the trait, EncodedName |
| `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md`:24 | (file head) "encodedform trait must implement the fingerprint trait" | `flows/6863ef19/vision/encodedFormIsTheCode.md` | *(2026-08-14 annotation, consistency audit  this entire 2026-08-06 entry is in dead vocabulary — encodedform, encodable, and EncodedName all carry code/encoded, which was dropped 2 |
| `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md`:24 | (file head) "encodedform trait must implement the fingerprint trait" | `vision-raw/traitsAsCapabilities.md` | *(2026-08-14 annotation, consistency audit  this entire 2026-08-06 entry is in dead vocabulary — encodedform, encodable, and EncodedName all carry code/encoded, which was dropped 2 |
| `flows/5abf3be8/vision/letsUseTheSameVocabulary.md`:17 | 2026-08-06T22:05:53.515Z — "lets use the same vocabulary" | `flows/6863ef19/vision/encodedFormIsTheCode.md` | *(2026-08-14 annotation, consistency audit  EncodedName carries the code/encoded vocabulary dropped 2026-08-13; its successor lineage is open per traitsAsCapabilities.md 2026-08-13 |
| `flows/5abf3be8/vision/letsUseTheSameVocabulary.md`:17 | 2026-08-06T22:05:53.515Z — "lets use the same vocabulary" | `vision-raw/traitsAsCapabilities.md` | *(2026-08-14 annotation, consistency audit  EncodedName carries the code/encoded vocabulary dropped 2026-08-13; its successor lineage is open per traitsAsCapabilities.md 2026-08-13 |
| `flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md`:23 | 2026-08-13 — signal must be specified: portable rkyv; CapnProto as universal signal | `flows/012fbf07/vision/threeStacks.md` | signal repo" (threeStacks.md 2026-08-11, name unruled, bead |
| `flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md`:19 | 2026-08-13 — signal must be specified: portable rkyv; CapnProto as universal signal | `vision-raw/mentci.md` | the Mentci front-end problem (mentci.md)  a non-Rust front-end |
| `flows/6863ef19/vision/archive-signalIsOurMessagingLayer.md`:36 | 2026-08-13 — universal signal is a capnp transcodable implementation of ethos; not there y | `vision-raw/traitsAsCapabilities.md` | *(2026-08-14 annotation, consistency audit  "transcodable" and "capnp transcodable" in the 2026-08-13 entries above predate the code/encoded vocabulary drop; Transcodable as a trai |
| `flows/6863ef19/vision/archive-traitsAsCapabilities.md`:14 | 2026-08-13 — all traits are qualifiers; reconsider traits as capabilities | `flows/5abf3be8/vision/archive-encodedFormFingerprintTraitDesign.md` | Rules the open 2026-08-06 question (encodedFormFingerprintTraitDesign.md |
| `flows/6863ef19/vision/codeIsLanguage.md`:14 | 2026-08-13 — the vocabulary drives the code; the implemented code drives the vocabulary | `flows/15b67974/vision/letsUseTheSameVocabulary.md` | Related  letsUseTheSameVocabulary.md. |
| `flows/6863ef19/vision/encodedFormIsTheCode.md`:11 | 2026-08-13 — the different forms; the textual form is data, a type | `vision-raw/traitsAsCapabilities.md` | the Designer's capability re-cut (traitsAsCapabilities.md). A thing |
| `flows/6863ef19/vision/signalIsOurMessagingLayer.md`:7 | 2026-08-13 — the router repo concept is routable signal | `flows/012fbf07/vision/threeStacks.md` | repo concept (threeStacks.md 2026-08-11; bead primary-xqb.8.3) is |
| `flows/7c3f0c1d/vision/psycheLogStructure.md`:5 | 2026-08-19 — duplicate topics: distill the psyche instead; review that protocol, we've nev | `vision-raw/session-log.md` | `session-log.md` by appending its entries verbatim |
| `flows/98fbfa47/vision/shortHeaderNotNow.md`:17 | (file head) The short header — "a great idea, but it's quite low level" — not now | `flows/98fbfa47/vision/draftIdeasForImprovement.md` | idea for future improvement (see draftIdeasForImprovement.md). |
| `flows/9993b5/vision/autoCommitOnWrite.md`:5 | Eventually, I want a file write event that automatically creates a commit | `flows/9993b5/vision/datomStructuralEditing.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the shared-workspace and datom-structural-editing visions (sharedWorkspace.md, datomS |
| `flows/9993b5/vision/autoCommitOnWrite.md`:5 | Eventually, I want a file write event that automatically creates a commit | `flows/9993b5/vision/sharedWorkspace.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the shared-workspace and datom-structural-editing visions (sharedWorkspace.md, datomS |
| `flows/9993b5/vision/blockPropagation.md`:5 | These things should be continually proposed until they are seen by the psyche; this is why | `flows/05c604/vision/messages.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that carries the harness-block-documentation vision (harnessBlockDocumentation.md, same |
| `flows/9993b5/vision/blockPropagation.md`:5 | These things should be continually proposed until they are seen by the psyche; this is why | `flows/9993b5/vision/harnessBlockDocumentation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that carries the harness-block-documentation vision (harnessBlockDocumentation.md, same |
| `flows/9993b5/vision/blockedCallsAndOtherModel.md`:5 | So I had to allow you to send a message; is that what just happened? it is really frustrat | `flows/9993b5/vision/fullSystemAccess.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 after this flow finally checked the agent-intercom MCP tools and found them working. The living was prompted |
| `flows/9993b5/vision/blockedCallsAndOtherModel.md`:5 | So I had to allow you to send a message; is that what just happened? it is really frustrat | `flows/9993b5/vision/harnessBlockDocumentation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 after this flow finally checked the agent-intercom MCP tools and found them working. The living was prompted |
| `flows/9993b5/vision/blockedCallsAndOtherModel.md`:5 | So I had to allow you to send a message; is that what just happened? it is really frustrat | `flows/9993b5/vision/harnessReplacement.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 after this flow finally checked the agent-intercom MCP tools and found them working. The living was prompted |
| `flows/9993b5/vision/blockedCallsAndOtherModel.md`:5 | So I had to allow you to send a message; is that what just happened? it is really frustrat | `flows/9993b5/vision/noRetryRefused.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 after this flow finally checked the agent-intercom MCP tools and found them working. The living was prompted |
| `flows/9993b5/vision/callerIdentity.md`:5 | A way to identify the process that called the CLI that created the call; implemented in th | `flows/9993b5/vision/flowRestart.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same mid-turn message as the flow-restart vision (flowRestart.md, same date); an extension of efa157' |
| `flows/9993b5/vision/codexAsDoing.md`:5 | Can you use Codex to help you if you need to do something big, because we cannot afford to | `flows/9993b5/vision/codexScarcity.md` | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17 immediately after the Codex-scarcity statement (codexScarcity.md, same date), relayed to primary Psyche opus (this flo |
| `flows/9993b5/vision/codexNeededHere.md`:5 | This would be perfect for Codex to do this; I need Codex here | `flows/9993b5/vision/codexAsDoing.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that carries the remote-rotation, selective-import, and criomOsUpgrade visions (remoteRo |
| `flows/9993b5/vision/codexNeededHere.md`:5 | This would be perfect for Codex to do this; I need Codex here | `flows/9993b5/vision/codexRemoteAccess.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that carries the remote-rotation, selective-import, and criomOsUpgrade visions (remoteRo |
| `flows/9993b5/vision/codexNeededHere.md`:5 | This would be perfect for Codex to do this; I need Codex here | `flows/9993b5/vision/criomOsUpgrade.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that carries the remote-rotation, selective-import, and criomOsUpgrade visions (remoteRo |
| `flows/9993b5/vision/codexNeededHere.md`:5 | This would be perfect for Codex to do this; I need Codex here | `flows/9993b5/vision/remoteRotation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that carries the remote-rotation, selective-import, and criomOsUpgrade visions (remoteRo |
| `flows/9993b5/vision/codexNeededHere.md`:5 | This would be perfect for Codex to do this; I need Codex here | `flows/9993b5/vision/selectiveImport.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that carries the remote-rotation, selective-import, and criomOsUpgrade visions (remoteRo |
| `flows/9993b5/vision/codexRelaysPsyche.md`:5 | Well, actually, I've asked him to relay the Psyche with context every time I talk to him | `flows/9993b5/vision/middleLayerRouting.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the living confirmed running the v6 Codex launcher and having Codex reach out to primary P |
| `flows/9993b5/vision/codexRemoteAccess.md`:5 | I need to be able to talk to Codex; if Claude is low, I need to be able to talk to Codex;  | `flows/9993b5/vision/sprawlFix.md` | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17, relayed to primary Psyche opus (this flow, 9993b5) by Fable's correction message. Names the immediate operational req |
| `flows/9993b5/vision/codexScarcity.md`:5 | We need to start using Codex; we do not have a lot of Claude usage | `flows/9993b5/vision/codexAsDoing.md` | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17, relayed to primary Psyche opus (this flow, 9993b5) by Fable's correction message. Names the operational reality  Clau |
| `flows/9993b5/vision/criomOsUpgrade.md`:5 | With the new server's version being updated, let us make sure it is the latest version; th | `flows/9993b5/vision/codexNeededHere.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, selective-import, and codex-needed-here visions (remoteRotation. |
| `flows/9993b5/vision/criomOsUpgrade.md`:5 | With the new server's version being updated, let us make sure it is the latest version; th | `flows/9993b5/vision/remoteRotation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, selective-import, and codex-needed-here visions (remoteRotation. |
| `flows/9993b5/vision/criomOsUpgrade.md`:5 | With the new server's version being updated, let us make sure it is the latest version; th | `flows/9993b5/vision/selectiveImport.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, selective-import, and codex-needed-here visions (remoteRotation. |
| `flows/9993b5/vision/curriculumNexus.md`:5 | This is where we want to go: towards Curriculum being a Nexus and taking it in; we take co | `flows/9993b5/vision/operatorsNotes.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, workspace-provisioning, and primary-skeleton visions (operatorsN |
| `flows/9993b5/vision/curriculumNexus.md`:5 | This is where we want to go: towards Curriculum being a Nexus and taking it in; we take co | `flows/9993b5/vision/primarySkeleton.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, workspace-provisioning, and primary-skeleton visions (operatorsN |
| `flows/9993b5/vision/curriculumNexus.md`:5 | This is where we want to go: towards Curriculum being a Nexus and taking it in; we take co | `flows/9993b5/vision/transcriptOverFiles.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, workspace-provisioning, and primary-skeleton visions (operatorsN |
| `flows/9993b5/vision/curriculumNexus.md`:5 | This is where we want to go: towards Curriculum being a Nexus and taking it in; we take co | `flows/9993b5/vision/workspaceProvisioning.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, workspace-provisioning, and primary-skeleton visions (operatorsN |
| `flows/9993b5/vision/datomStructuralEditing.md`:5 | We are going to create this language to edit through our own CLI, the right tool; oh my go | `flows/9993b5/vision/autoCommitOnWrite.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the shared-workspace and auto-commit-on-write visions (sharedWorkspace.md, autoCommit |
| `flows/9993b5/vision/datomStructuralEditing.md`:5 | We are going to create this language to edit through our own CLI, the right tool; oh my go | `flows/9993b5/vision/sharedWorkspace.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the shared-workspace and auto-commit-on-write visions (sharedWorkspace.md, autoCommit |
| `flows/9993b5/vision/distillEveryTurn.md`:5 | We need to, every turn, have some little bit of vision distilled; even if it is just a lit | `flows/9993b5/vision/psycheVsMind.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the vision-accessible-to-all vision (visionAccessibleToAll.md, same date). Names a co |
| `flows/9993b5/vision/distillEveryTurn.md`:5 | We need to, every turn, have some little bit of vision distilled; even if it is just a lit | `flows/9993b5/vision/sprawlFix.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the vision-accessible-to-all vision (visionAccessibleToAll.md, same date). Names a co |
| `flows/9993b5/vision/distillEveryTurn.md`:5 | We need to, every turn, have some little bit of vision distilled; even if it is just a lit | `flows/9993b5/vision/visionAccessibleToAll.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the vision-accessible-to-all vision (visionAccessibleToAll.md, same date). Names a co |
| `flows/9993b5/vision/easyFlowDispatch.md`:5 | We need this to make this dispatching really really really efficient and easy with the Flo | `Vision/flowNexus.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, psyche-vs-mind, and flow-origin-clue visions (oneSharedPrimar |
| `flows/9993b5/vision/easyFlowDispatch.md`:5 | We need this to make this dispatching really really really efficient and easy with the Flo | `flows/9993b5/vision/flowAnatomy.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, psyche-vs-mind, and flow-origin-clue visions (oneSharedPrimar |
| `flows/9993b5/vision/easyFlowDispatch.md`:5 | We need this to make this dispatching really really really efficient and easy with the Flo | `flows/9993b5/vision/flowOriginClue.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, psyche-vs-mind, and flow-origin-clue visions (oneSharedPrimar |
| `flows/9993b5/vision/easyFlowDispatch.md`:5 | We need this to make this dispatching really really really efficient and easy with the Flo | `flows/9993b5/vision/oneSharedPrimary.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, psyche-vs-mind, and flow-origin-clue visions (oneSharedPrimar |
| `flows/9993b5/vision/easyFlowDispatch.md`:5 | We need this to make this dispatching really really really efficient and easy with the Flo | `flows/9993b5/vision/psycheVsMind.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, psyche-vs-mind, and flow-origin-clue visions (oneSharedPrimar |
| `flows/9993b5/vision/easyFlowDispatch.md`:5 | We need this to make this dispatching really really really efficient and easy with the Flo | `flows/9993b5/vision/workspaceProvisioning.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, psyche-vs-mind, and flow-origin-clue visions (oneSharedPrimar |
| `flows/9993b5/vision/editNexusName.md`:5 | Edit is the right name; the edit nexus | `Vision/nexus.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a direct naming ruling on the datom structural editing CLI proposed in the previous turn (datomStructural |
| `flows/9993b5/vision/editNexusName.md`:5 | Edit is the right name; the edit nexus | `flows/9993b5/vision/datomStructuralEditing.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a direct naming ruling on the datom structural editing CLI proposed in the previous turn (datomStructural |
| `flows/9993b5/vision/fixMessagingApproval.md`:5 | Every time you want to send a message, I have to allow it, so you have to fix that | `flows/9993b5/vision/blockedCallsAndOtherModel.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that confirms the living has run the v6 Codex launcher command and Codex is now up. The |
| `flows/9993b5/vision/fixMessagingApproval.md`:5 | Every time you want to send a message, I have to allow it, so you have to fix that | `flows/9993b5/vision/fullSystemAccess.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that confirms the living has run the v6 Codex launcher command and Codex is now up. The |
| `flows/9993b5/vision/fixMessagingApproval.md`:5 | Every time you want to send a message, I have to allow it, so you have to fix that | `flows/9993b5/vision/harnessReplacement.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that confirms the living has run the v6 Codex launcher command and Codex is now up. The |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `Vision/flowNexus.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `flows/9993b5/vision/callerIdentity.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `flows/9993b5/vision/flowIdLayers.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `flows/9993b5/vision/mindMemory.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `flows/9993b5/vision/structuredLog.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `flows/9993b5/vision/transparentRefresh.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `flows/9993b5/vision/typedString.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowAnatomy.md`:5 | We have the flow data, which is also essentially right now our biggest problem in terms of | `flows/9993b5/vision/workspaceProvisioning.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the flow-id-layers, transparent-refresh, mind-memory, structured-log, |
| `flows/9993b5/vision/flowIdLayers.md`:5 | Right now, our identifier, the flow ID, is just semi-secure, but it is fine, and it will b | `flows/9993b5/vision/callerIdentity.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, transparent-refresh, mind-memory, structured-log, and typed-string |
| `flows/9993b5/vision/flowIdLayers.md`:5 | Right now, our identifier, the flow ID, is just semi-secure, but it is fine, and it will b | `flows/9993b5/vision/flowAnatomy.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, transparent-refresh, mind-memory, structured-log, and typed-string |
| `flows/9993b5/vision/flowIdLayers.md`:5 | Right now, our identifier, the flow ID, is just semi-secure, but it is fine, and it will b | `flows/9993b5/vision/mindMemory.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, transparent-refresh, mind-memory, structured-log, and typed-string |
| `flows/9993b5/vision/flowIdLayers.md`:5 | Right now, our identifier, the flow ID, is just semi-secure, but it is fine, and it will b | `flows/9993b5/vision/structuredLog.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, transparent-refresh, mind-memory, structured-log, and typed-string |
| `flows/9993b5/vision/flowIdLayers.md`:5 | Right now, our identifier, the flow ID, is just semi-secure, but it is fine, and it will b | `flows/9993b5/vision/transparentRefresh.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, transparent-refresh, mind-memory, structured-log, and typed-string |
| `flows/9993b5/vision/flowIdLayers.md`:5 | Right now, our identifier, the flow ID, is just semi-secure, but it is fine, and it will b | `flows/9993b5/vision/typedString.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, transparent-refresh, mind-memory, structured-log, and typed-string |
| `flows/9993b5/vision/flowOriginClue.md`:5 | One of the clues is probably going to be a programmatically provided origin of where the F | `flows/9993b5/vision/callerIdentity.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the one-shared-primary, psyche-vs-mind, and easy-flow-dispatch visions |
| `flows/9993b5/vision/flowOriginClue.md`:5 | One of the clues is probably going to be a programmatically provided origin of where the F | `flows/9993b5/vision/easyFlowDispatch.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the one-shared-primary, psyche-vs-mind, and easy-flow-dispatch visions |
| `flows/9993b5/vision/flowOriginClue.md`:5 | One of the clues is probably going to be a programmatically provided origin of where the F | `flows/9993b5/vision/oneSharedPrimary.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the one-shared-primary, psyche-vs-mind, and easy-flow-dispatch visions |
| `flows/9993b5/vision/flowOriginClue.md`:5 | One of the clues is probably going to be a programmatically provided origin of where the F | `flows/9993b5/vision/psycheVsMind.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the one-shared-primary, psyche-vs-mind, and easy-flow-dispatch visions |
| `flows/9993b5/vision/flowRestart.md`:5 | A harness that locks itself out of relaunching its own flow is a design defect; how flows  | `flows/9993b5/vision/callerIdentity.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the mid-turn message that also carries the caller-identity vision (callerIdentity.md, same date); the sam |
| `flows/9993b5/vision/fullSystemAccess.md`:5 | Why do I keep having to allow stuff? just give yourself full permissions; do not ask me, a | `flows/9993b5/vision/sprawlFix.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the sprawl-fix corrective (sprawlFix.md, same date). Explicit, categorical authorization |
| `flows/9993b5/vision/harnessBlockDocumentation.md`:5 | We need to document this in the Claude harness; this is what Claude harness documentation  | `flows/9993b5/vision/blockPropagation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17, after this flow's answer explaining the Claude Code auto-mode classifier (what it is, what triggers it, wha |
| `flows/9993b5/vision/harnessReplacement.md`:5 | I do not like that this is going to be a very big rare exception — me actually writing a f | `flows/9993b5/vision/fullSystemAccess.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 after a whole session of the classifier refusing every launch-shaped and settings-editing action, forcing ma |
| `flows/9993b5/vision/integratorFlow.md`:5 | We can have an integrator flow type; I would run these as integrator, mostly on the Codex  | `flows/01a05826/vision/subflowIdentity.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the orchestrate-locking, subflow-identity, and transcript-over-files vision |
| `flows/9993b5/vision/integratorFlow.md`:5 | We can have an integrator flow type; I would run these as integrator, mostly on the Codex  | `flows/9993b5/vision/orchestrateLocking.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the orchestrate-locking, subflow-identity, and transcript-over-files vision |
| `flows/9993b5/vision/integratorFlow.md`:5 | We can have an integrator flow type; I would run these as integrator, mostly on the Codex  | `flows/9993b5/vision/transcriptOverFiles.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the orchestrate-locking, subflow-identity, and transcript-over-files vision |
| `flows/9993b5/vision/launchOnMain.md`:5 | From henceforth we launch all the primary flows directly on main unless specified otherwis | `flows/9993b5/vision/noMoreBranches.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the no-more-branches correction (noMoreBranches.md, same date) and after this flow dispatc |
| `flows/9993b5/vision/mergeQueue.md`:5 | Or we have to lean out primary and then make pushing essentially the committing, right? be | `flows/9993b5/vision/launchOnMain.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the launch-on-main rule (launchOnMain.md, same date) and while a subflow was running to me |
| `flows/9993b5/vision/messagingBootstrap.md`:5 | Why isn't the agent intercom working? where did the messaging go? it was working; I want t | `flows/9993b5/vision/messagingIsScripts.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 after this flow gave the living a terminal command to run the v6 Codex launcher manually, and after a whole |
| `flows/9993b5/vision/messagingIsScripts.md`:5 | Do you understand that my division and my psyche that reaches you have to come through you | `flows/9993b5/vision/middleLayerRouting.md` | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17, relayed to primary Psyche opus (this flow, 9993b5) by Fable's correction message. Twofold statement  (a) a check that |
| `flows/9993b5/vision/middleLayerRouting.md`:5 | Make sure all of my psyche that I've given to him comes to you through your middle layer | `flows/9993b5/vision/flowIdLayers.md` | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17 as a direct order about the psyche-routing between the layers, relayed to primary Psyche opus (this flow, 9993b5) by F |
| `flows/9993b5/vision/mindMemory.md`:5 | The Flow's memory will live in Mind, and so Mind will become our most bloated component in | `flows/9993b5/vision/flowAnatomy.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, structured-log, and typed-stri |
| `flows/9993b5/vision/mindMemory.md`:5 | The Flow's memory will live in Mind, and so Mind will become our most bloated component in | `flows/9993b5/vision/flowIdLayers.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, structured-log, and typed-stri |
| `flows/9993b5/vision/mindMemory.md`:5 | The Flow's memory will live in Mind, and so Mind will become our most bloated component in | `flows/9993b5/vision/structuredLog.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, structured-log, and typed-stri |
| `flows/9993b5/vision/mindMemory.md`:5 | The Flow's memory will live in Mind, and so Mind will become our most bloated component in | `flows/9993b5/vision/transparentRefresh.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, structured-log, and typed-stri |
| `flows/9993b5/vision/mindMemory.md`:5 | The Flow's memory will live in Mind, and so Mind will become our most bloated component in | `flows/9993b5/vision/typedString.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, structured-log, and typed-stri |
| `flows/9993b5/vision/oneSharedPrimary.md`:5 | I think you all just need to go back onto one shared primary for now and use the Orchestra | `flows/9993b5/vision/easyFlowDispatch.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the psyche-vs-mind, easy-flow-dispatch, and flow-origin-clue visions ( |
| `flows/9993b5/vision/oneSharedPrimary.md`:5 | I think you all just need to go back onto one shared primary for now and use the Orchestra | `flows/9993b5/vision/flowOriginClue.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the psyche-vs-mind, easy-flow-dispatch, and flow-origin-clue visions ( |
| `flows/9993b5/vision/oneSharedPrimary.md`:5 | I think you all just need to go back onto one shared primary for now and use the Orchestra | `flows/9993b5/vision/psycheVsMind.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the psyche-vs-mind, easy-flow-dispatch, and flow-origin-clue visions ( |
| `flows/9993b5/vision/oneSharedPrimary.md`:5 | I think you all just need to go back onto one shared primary for now and use the Orchestra | `flows/9993b5/vision/sharedWorkspace.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 opening the message that also carries the psyche-vs-mind, easy-flow-dispatch, and flow-origin-clue visions ( |
| `flows/9993b5/vision/operatorsNotes.md`:5 | This comes back to the operators' notes skill that agents can compose; the Claude harness  | `flows/9993b5/vision/curriculumNexus.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the curriculum-nexus, workspace-provisioning, and primary-skeleton visions |
| `flows/9993b5/vision/operatorsNotes.md`:5 | This comes back to the operators' notes skill that agents can compose; the Claude harness  | `flows/9993b5/vision/harnessBlockDocumentation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the curriculum-nexus, workspace-provisioning, and primary-skeleton visions |
| `flows/9993b5/vision/operatorsNotes.md`:5 | This comes back to the operators' notes skill that agents can compose; the Claude harness  | `flows/9993b5/vision/primarySkeleton.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the curriculum-nexus, workspace-provisioning, and primary-skeleton visions |
| `flows/9993b5/vision/operatorsNotes.md`:5 | This comes back to the operators' notes skill that agents can compose; the Claude harness  | `flows/9993b5/vision/workspaceProvisioning.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the curriculum-nexus, workspace-provisioning, and primary-skeleton visions |
| `flows/9993b5/vision/orchestrateCommitBinding.md`:5 | We have the Orchestrate tool, right? if we ask people to use the Orchestrate tool to lock  | `flows/9993b5/vision/autoCommitOnWrite.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a design vision immediately after the "make it operational" corrective and my push of flow/9993b5 to orig |
| `flows/9993b5/vision/orchestrateCommitBinding.md`:5 | We have the Orchestrate tool, right? if we ask people to use the Orchestrate tool to lock  | `flows/9993b5/vision/easyFlowDispatch.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a design vision immediately after the "make it operational" corrective and my push of flow/9993b5 to orig |
| `flows/9993b5/vision/orchestrateLocking.md`:5 | I don't want to have all these branches; I really don't want to have it like we used to, w | `flows/01a05826/vision/subflowIdentity.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the integrator-flow, subflow-identity, and transcript-over-files visions (i |
| `flows/9993b5/vision/orchestrateLocking.md`:5 | I don't want to have all these branches; I really don't want to have it like we used to, w | `flows/9993b5/vision/integratorFlow.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the integrator-flow, subflow-identity, and transcript-over-files visions (i |
| `flows/9993b5/vision/orchestrateLocking.md`:5 | I don't want to have all these branches; I really don't want to have it like we used to, w | `flows/9993b5/vision/transcriptOverFiles.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the integrator-flow, subflow-identity, and transcript-over-files visions (i |
| `flows/9993b5/vision/orchestrateLocking.md`:5 | I don't want to have all these branches; I really don't want to have it like we used to, w | `flows/9993b5/vision/worktreeHygiene.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the integrator-flow, subflow-identity, and transcript-over-files visions (i |
| `flows/9993b5/vision/powerLevels.md`:5 | What are the open-source models that were contenders for the high, medium, and low power l | `flows/f55ec8/vision/modelRoles.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 mid-turn during the "make it operational" corrective. Renames the layer axis from High/Medium/Low as pure po |
| `flows/9993b5/vision/primaryNext.md`:5 | Let us focus on restructuring primary to be on one shared worktree, like the main; we shou | `flows/9993b5/vision/easyFlowDispatch.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a mid-turn concentration order, immediately after the one-shared-primary, psyche-vs-mind, easy-flow-dispa |
| `flows/9993b5/vision/primaryNext.md`:5 | Let us focus on restructuring primary to be on one shared worktree, like the main; we shou | `flows/9993b5/vision/flowOriginClue.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a mid-turn concentration order, immediately after the one-shared-primary, psyche-vs-mind, easy-flow-dispa |
| `flows/9993b5/vision/primaryNext.md`:5 | Let us focus on restructuring primary to be on one shared worktree, like the main; we shou | `flows/9993b5/vision/oneSharedPrimary.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a mid-turn concentration order, immediately after the one-shared-primary, psyche-vs-mind, easy-flow-dispa |
| `flows/9993b5/vision/primaryNext.md`:5 | Let us focus on restructuring primary to be on one shared worktree, like the main; we shou | `flows/9993b5/vision/primarySkeleton.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a mid-turn concentration order, immediately after the one-shared-primary, psyche-vs-mind, easy-flow-dispa |
| `flows/9993b5/vision/primaryNext.md`:5 | Let us focus on restructuring primary to be on one shared worktree, like the main; we shou | `flows/9993b5/vision/psycheVsMind.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a mid-turn concentration order, immediately after the one-shared-primary, psyche-vs-mind, easy-flow-dispa |
| `flows/9993b5/vision/primarySkeleton.md`:5 | The way the data is kept, the primary workspace is minimal; it is just a skeleton; we need | `flows/9993b5/vision/curriculumNexus.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, curriculum-nexus, and workspace-provisioning visions (operatorsN |
| `flows/9993b5/vision/primarySkeleton.md`:5 | The way the data is kept, the primary workspace is minimal; it is just a skeleton; we need | `flows/9993b5/vision/operatorsNotes.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, curriculum-nexus, and workspace-provisioning visions (operatorsN |
| `flows/9993b5/vision/primarySkeleton.md`:5 | The way the data is kept, the primary workspace is minimal; it is just a skeleton; we need | `flows/9993b5/vision/workspaceProvisioning.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, curriculum-nexus, and workspace-provisioning visions (operatorsN |
| `flows/9993b5/vision/primarySkeleton.md`:5 | The way the data is kept, the primary workspace is minimal; it is just a skeleton; we need | `flows/9993b5/vision/worktreeHygiene.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, curriculum-nexus, and workspace-provisioning visions (operatorsN |
| `flows/9993b5/vision/psycheChronology.md`:5 | Living psyche input is the center of everything; psyche is the highest authority, so prima | `flows/9993b5/vision/threadNaming.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that approved the situation report ("glanced at it and trusted it to be fairly accurate, |
| `flows/9993b5/vision/psycheChronology.md`:5 | Living psyche input is the center of everything; psyche is the highest authority, so prima | `flows/9993b5/vision/transcriptSelfReference.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that approved the situation report ("glanced at it and trusted it to be fairly accurate, |
| `flows/9993b5/vision/psycheVsMind.md`:5 | This is why Psyche needs to be separate from Mind: if you are searching Psyche, you want t | `flows/9993b5/vision/easyFlowDispatch.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, easy-flow-dispatch, and flow-origin-clue visions (oneSharedPr |
| `flows/9993b5/vision/psycheVsMind.md`:5 | This is why Psyche needs to be separate from Mind: if you are searching Psyche, you want t | `flows/9993b5/vision/flowIdLayers.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, easy-flow-dispatch, and flow-origin-clue visions (oneSharedPr |
| `flows/9993b5/vision/psycheVsMind.md`:5 | This is why Psyche needs to be separate from Mind: if you are searching Psyche, you want t | `flows/9993b5/vision/flowOriginClue.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, easy-flow-dispatch, and flow-origin-clue visions (oneSharedPr |
| `flows/9993b5/vision/psycheVsMind.md`:5 | This is why Psyche needs to be separate from Mind: if you are searching Psyche, you want t | `flows/9993b5/vision/mindMemory.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, easy-flow-dispatch, and flow-origin-clue visions (oneSharedPr |
| `flows/9993b5/vision/psycheVsMind.md`:5 | This is why Psyche needs to be separate from Mind: if you are searching Psyche, you want t | `flows/9993b5/vision/oneSharedPrimary.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the one-shared-primary, easy-flow-dispatch, and flow-origin-clue visions (oneSharedPr |
| `flows/9993b5/vision/rebootstrapWithPowers.md`:5 | You need to rebootstrap; do you want to give me a command to help you do that, where you w | `flows/9993b5/vision/fixMessagingApproval.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as a direct offer from the living  they will run a single command that both rebootstraps primary Psyche opus |
| `flows/9993b5/vision/remoteRotation.md`:5 | Since the remote is working so badly, why don't we just restart a new one, and then we can | `flows/9993b5/vision/codexNeededHere.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the selective-import, criomOsUpgrade, and codex-needed-here visions (select |
| `flows/9993b5/vision/remoteRotation.md`:5 | Since the remote is working so badly, why don't we just restart a new one, and then we can | `flows/9993b5/vision/criomOsUpgrade.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the selective-import, criomOsUpgrade, and codex-needed-here visions (select |
| `flows/9993b5/vision/remoteRotation.md`:5 | Since the remote is working so badly, why don't we just restart a new one, and then we can | `flows/9993b5/vision/primaryNext.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the selective-import, criomOsUpgrade, and codex-needed-here visions (select |
| `flows/9993b5/vision/remoteRotation.md`:5 | Since the remote is working so badly, why don't we just restart a new one, and then we can | `flows/9993b5/vision/selectiveImport.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the selective-import, criomOsUpgrade, and codex-needed-here visions (select |
| `flows/9993b5/vision/selectiveImport.md`:5 | Just start clean and just import a few sessions that are relevant because they are from ou | `flows/9993b5/vision/codexNeededHere.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, criomOsUpgrade, and codex-needed-here visions (remoteRotation.md |
| `flows/9993b5/vision/selectiveImport.md`:5 | Just start clean and just import a few sessions that are relevant because they are from ou | `flows/9993b5/vision/criomOsUpgrade.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, criomOsUpgrade, and codex-needed-here visions (remoteRotation.md |
| `flows/9993b5/vision/selectiveImport.md`:5 | Just start clean and just import a few sessions that are relevant because they are from ou | `flows/9993b5/vision/remoteRotation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, criomOsUpgrade, and codex-needed-here visions (remoteRotation.md |
| `flows/9993b5/vision/selectiveImport.md`:5 | Just start clean and just import a few sessions that are relevant because they are from ou | `flows/9993b5/vision/transcriptArchive.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, criomOsUpgrade, and codex-needed-here visions (remoteRotation.md |
| `flows/9993b5/vision/selectiveImport.md`:5 | Just start clean and just import a few sessions that are relevant because they are from ou | `flows/9993b5/vision/worktreeHygiene.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the remote-rotation, criomOsUpgrade, and codex-needed-here visions (remoteRotation.md |
| `flows/9993b5/vision/sharedWorkspace.md`:5 | If they are all primary, then they should all work in a shared space, so we would almost h | `flows/9993b5/vision/autoCommitOnWrite.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17, opening the message that also carries the auto-commit-on-write and datom-structural-editing visions (autoCo |
| `flows/9993b5/vision/sharedWorkspace.md`:5 | If they are all primary, then they should all work in a shared space, so we would almost h | `flows/9993b5/vision/datomStructuralEditing.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17, opening the message that also carries the auto-commit-on-write and datom-structural-editing visions (autoCo |
| `flows/9993b5/vision/sharedWorkspace.md`:5 | If they are all primary, then they should all work in a shared space, so we would almost h | `flows/9993b5/vision/orchestrateLocking.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17, opening the message that also carries the auto-commit-on-write and datom-structural-editing visions (autoCo |
| `flows/9993b5/vision/sprawlFix.md`:5 | For me right now, our biggest problem is sprawl; let us fix this sprawl, merge, create coh | `flows/9993b5/vision/fullSystemAccess.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as an escalated corrective after a whole session of the flow offering plans instead of acting on merge/commi |
| `flows/9993b5/vision/structuredLog.md`:5 | It is going to be about remembering the logs, basically; the more we specify a language of | `flows/9993b5/vision/blockPropagation.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, and typed-string |
| `flows/9993b5/vision/structuredLog.md`:5 | It is going to be about remembering the logs, basically; the more we specify a language of | `flows/9993b5/vision/flowAnatomy.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, and typed-string |
| `flows/9993b5/vision/structuredLog.md`:5 | It is going to be about remembering the logs, basically; the more we specify a language of | `flows/9993b5/vision/flowIdLayers.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, and typed-string |
| `flows/9993b5/vision/structuredLog.md`:5 | It is going to be about remembering the logs, basically; the more we specify a language of | `flows/9993b5/vision/mindMemory.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, and typed-string |
| `flows/9993b5/vision/structuredLog.md`:5 | It is going to be about remembering the logs, basically; the more we specify a language of | `flows/9993b5/vision/transparentRefresh.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, and typed-string |
| `flows/9993b5/vision/structuredLog.md`:5 | It is going to be about remembering the logs, basically; the more we specify a language of | `flows/9993b5/vision/typedString.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, and typed-string |
| `flows/9993b5/vision/subflowIdentity.md`:5 | That's what subflows can do: they can create an entry, and they're given a job name; that  | `flows/9993b5/vision/integratorFlow.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the integrator-flow, orchestrate-locking, and transcript-over-files visions (integrat |
| `flows/9993b5/vision/subflowIdentity.md`:5 | That's what subflows can do: they can create an entry, and they're given a job name; that  | `flows/9993b5/vision/orchestrateLocking.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the integrator-flow, orchestrate-locking, and transcript-over-files visions (integrat |
| `flows/9993b5/vision/subflowIdentity.md`:5 | That's what subflows can do: they can create an entry, and they're given a job name; that  | `flows/9993b5/vision/transcriptOverFiles.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the integrator-flow, orchestrate-locking, and transcript-over-files visions (integrat |
| `flows/9993b5/vision/threadNaming.md`:5 | Agree on naming terminology that makes sense for naming the remote threads; likes "primary | `flows/9993b5/vision/psycheChronology.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that carries the psyche-chronology and transcript-self-reference visions (psycheChronology.md |
| `flows/9993b5/vision/threadNaming.md`:5 | Agree on naming terminology that makes sense for naming the remote threads; likes "primary | `flows/9993b5/vision/transcriptSelfReference.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that carries the psyche-chronology and transcript-self-reference visions (psycheChronology.md |
| `flows/9993b5/vision/transcriptArchive.md`:5 | All this is why we need a way to archive what matters from the transcript files so we can  | `flows/9993b5/vision/mindMemory.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that reports the ChatGPT desktop app crashing (an operational observation, kept in the l |
| `flows/9993b5/vision/transcriptArchive.md`:5 | All this is why we need a way to archive what matters from the transcript files so we can  | `flows/9993b5/vision/structuredLog.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that reports the ChatGPT desktop app crashing (an operational observation, kept in the l |
| `flows/9993b5/vision/transcriptArchive.md`:5 | All this is why we need a way to archive what matters from the transcript files so we can  | `flows/9993b5/vision/transcriptIndex.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that reports the ChatGPT desktop app crashing (an operational observation, kept in the l |
| `flows/9993b5/vision/transcriptArchive.md`:5 | All this is why we need a way to archive what matters from the transcript files so we can  | `flows/9993b5/vision/transcriptOverFiles.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that reports the ChatGPT desktop app crashing (an operational observation, kept in the l |
| `flows/9993b5/vision/transcriptIndex.md`:5 | Do we have a way to reference all these transcripts, such-and-such spot in the log, and so | `flows/9993b5/vision/flowOriginClue.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the transcript-archive vision (transcriptArchive.md, same date). Names the second hal |
| `flows/9993b5/vision/transcriptIndex.md`:5 | Do we have a way to reference all these transcripts, such-and-such spot in the log, and so | `flows/9993b5/vision/structuredLog.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the transcript-archive vision (transcriptArchive.md, same date). Names the second hal |
| `flows/9993b5/vision/transcriptIndex.md`:5 | Do we have a way to reference all these transcripts, such-and-such spot in the log, and so | `flows/9993b5/vision/transcriptArchive.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the transcript-archive vision (transcriptArchive.md, same date). Names the second hal |
| `flows/9993b5/vision/transcriptIndex.md`:5 | Do we have a way to reference all these transcripts, such-and-such spot in the log, and so | `flows/9993b5/vision/transcriptSelfReference.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the transcript-archive vision (transcriptArchive.md, same date). Names the second hal |
| `flows/9993b5/vision/transcriptOverFiles.md`:5 | Actually, the report becomes everything is in the transcript; we don't want to make files  | `flows/01a05826/vision/subflowIdentity.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as the last thought in the message that also carries the integrator-flow, orchestrate-locking, and subflow-i |
| `flows/9993b5/vision/transcriptOverFiles.md`:5 | Actually, the report becomes everything is in the transcript; we don't want to make files  | `flows/9993b5/vision/integratorFlow.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as the last thought in the message that also carries the integrator-flow, orchestrate-locking, and subflow-i |
| `flows/9993b5/vision/transcriptOverFiles.md`:5 | Actually, the report becomes everything is in the transcript; we don't want to make files  | `flows/9993b5/vision/orchestrateLocking.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as the last thought in the message that also carries the integrator-flow, orchestrate-locking, and subflow-i |
| `flows/9993b5/vision/transcriptOverFiles.md`:5 | Actually, the report becomes everything is in the transcript; we don't want to make files  | `flows/9993b5/vision/transcriptSelfReference.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 as the last thought in the message that also carries the integrator-flow, orchestrate-locking, and subflow-i |
| `flows/9993b5/vision/transcriptSelfReference.md`:5 | We need the transcript tool: are the models aware of an output number or something in the  | `flows/9993b5/vision/psycheChronology.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that carries the psyche-chronology and thread-naming visions (psycheChronology.md, threa |
| `flows/9993b5/vision/transcriptSelfReference.md`:5 | We need the transcript tool: are the models aware of an output number or something in the  | `flows/9993b5/vision/threadNaming.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that carries the psyche-chronology and thread-naming visions (psycheChronology.md, threa |
| `flows/9993b5/vision/transparentRefresh.md`:5 | The whole refreshing of the flow is going to happen a lot more transparently, essentially, | `flows/9993b5/vision/flowAnatomy.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, mind-memory, structured-log, and typed-string visio |
| `flows/9993b5/vision/transparentRefresh.md`:5 | The whole refreshing of the flow is going to happen a lot more transparently, essentially, | `flows/9993b5/vision/flowIdLayers.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, mind-memory, structured-log, and typed-string visio |
| `flows/9993b5/vision/transparentRefresh.md`:5 | The whole refreshing of the flow is going to happen a lot more transparently, essentially, | `flows/9993b5/vision/mindMemory.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, mind-memory, structured-log, and typed-string visio |
| `flows/9993b5/vision/transparentRefresh.md`:5 | The whole refreshing of the flow is going to happen a lot more transparently, essentially, | `flows/9993b5/vision/structuredLog.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, mind-memory, structured-log, and typed-string visio |
| `flows/9993b5/vision/transparentRefresh.md`:5 | The whole refreshing of the flow is going to happen a lot more transparently, essentially, | `flows/9993b5/vision/typedString.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, mind-memory, structured-log, and typed-string visio |
| `flows/9993b5/vision/transparentRefresh.md`:5 | The whole refreshing of the flow is going to happen a lot more transparently, essentially, | `flows/f55ec8/vision/flowRefresh.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the flow-anatomy, flow-id-layers, mind-memory, structured-log, and typed-string visio |
| `flows/9993b5/vision/typedString.md`:5 | Those are the better anatomical designs for storage, essentially; this structures the mean | `Intent/mandatoryTraits.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, an |
| `flows/9993b5/vision/typedString.md`:5 | Those are the better anatomical designs for storage, essentially; this structures the mean | `Vision/datom.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, an |
| `flows/9993b5/vision/typedString.md`:5 | Those are the better anatomical designs for storage, essentially; this structures the mean | `flows/9993b5/vision/flowAnatomy.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, an |
| `flows/9993b5/vision/typedString.md`:5 | Those are the better anatomical designs for storage, essentially; this structures the mean | `flows/9993b5/vision/flowIdLayers.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, an |
| `flows/9993b5/vision/typedString.md`:5 | Those are the better anatomical designs for storage, essentially; this structures the mean | `flows/9993b5/vision/mindMemory.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, an |
| `flows/9993b5/vision/typedString.md`:5 | Those are the better anatomical designs for storage, essentially; this structures the mean | `flows/9993b5/vision/structuredLog.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, an |
| `flows/9993b5/vision/typedString.md`:5 | Those are the better anatomical designs for storage, essentially; this structures the mean | `flows/9993b5/vision/transparentRefresh.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 closing the message that also carries the flow-anatomy, flow-id-layers, transparent-refresh, mind-memory, an |
| `flows/9993b5/vision/visionAccessibleToAll.md`:5 | This is why the vision, all of the primary, has to work together so that all the vision is | `flows/9993b5/vision/distillEveryTurn.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the merge queue vision (mergeQueue.md, same date) and before the merge subflow reported it |
| `flows/9993b5/vision/visionAccessibleToAll.md`:5 | This is why the vision, all of the primary, has to work together so that all the vision is | `flows/9993b5/vision/mergeQueue.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the merge queue vision (mergeQueue.md, same date) and before the merge subflow reported it |
| `flows/9993b5/vision/workspaceProvisioning.md`:5 | When Flow starts, it can ask for curriculum: "Okay, give me a primary psyche, main Flow, l | `flows/9993b5/vision/curriculumNexus.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, curriculum-nexus, and primary-skeleton visions (operatorsNotes.m |
| `flows/9993b5/vision/workspaceProvisioning.md`:5 | When Flow starts, it can ask for curriculum: "Okay, give me a primary psyche, main Flow, l | `flows/9993b5/vision/operatorsNotes.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, curriculum-nexus, and primary-skeleton visions (operatorsNotes.m |
| `flows/9993b5/vision/workspaceProvisioning.md`:5 | When Flow starts, it can ask for curriculum: "Okay, give me a primary psyche, main Flow, l | `flows/9993b5/vision/primarySkeleton.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the operators-notes, curriculum-nexus, and primary-skeleton visions (operatorsNotes.m |
| `flows/9993b5/vision/worktreeHygiene.md`:5 | We cannot just keep spawning new worktrees; we need to rebase primary and cut a lot of stu | `flows/9993b5/vision/psycheChronology.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 mid-turn, after the Fable restart order and the three visions logged this turn (psycheChronology.md, threadN |
| `flows/9993b5/vision/worktreeHygiene.md`:5 | We cannot just keep spawning new worktrees; we need to rebase primary and cut a lot of stu | `flows/9993b5/vision/threadNaming.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 mid-turn, after the Fable restart order and the three visions logged this turn (psycheChronology.md, threadN |
| `flows/9993b5/vision/worktreeHygiene.md`:5 | We cannot just keep spawning new worktrees; we need to rebase primary and cut a lot of stu | `flows/9993b5/vision/transcriptSelfReference.md` | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 mid-turn, after the Fable restart order and the three visions logged this turn (psycheChronology.md, threadN |
| `flows/a5587095/vision/archive-colonFormTransformerSyntax.md`:23 | 2026-08-11 — transformer payloads take `.[` or `.{`; parentheses freed in Ethos | `vision-raw/structuredStringType.md` | structuredStringType.md. |
| `flows/a5587095/vision/archive-datomSyntax.md`:11 | 2026-08-11 — parentheses must not be unused in Datom | `vision-raw/colonFormTransformerSyntax.md` | (colonFormTransformerSyntax.md) and floated the structured string |
| `flows/a5587095/vision/archive-datomSyntax.md`:12 | 2026-08-11 — parentheses must not be unused in Datom | `vision-raw/structuredStringType.md` | type (structuredStringType.md) without assigning it a delimiter. |
| `flows/a5587095/vision/archive-protosIsTheSharedStyle.md`:161 | 2026-08-13 — the Protos parsing Intent is graduated | `Intent/protosParsing.md` | psyche/Intent/protosParsing.md — the first Intent graduated from |
| `flows/a5587095/vision/archive-protosIsTheSharedStyle.md`:49 | 2026-08-11 — there is always a parsing context; it changes, never suspends; always use tra | `flows/2b34fafa/vision/rustComponentArchitecture.md` | rustComponentArchitecture.md. |
| `flows/a5587095/vision/archive-protosIsTheSharedStyle.md`:53 | 2026-08-11 — two-way structural transcoding; flesh out before Intent; the design pattern | `flows/6863ef19/vision/encodedFormIsTheCode.md` | *(2026-08-14 annotation, consistency audit  "two-way structural transcoding" in this agent-authored heading is dead vocabulary — code/encoded was dropped 2026-08-13; the psyche's s |
| `flows/a5587095/vision/archive-protosIsTheSharedStyle.md`:17 | 2026-08-11 — the definition; context-switching parse; the protos engine | `vision-raw/structuredStringType.md` | during the structured-string design (structuredStringType.md — the |
| `flows/a5587095/vision/archive-protosIsTheSharedStyle.md`:124 | 2026-08-12 — ProtosShape is a trait types implement; the match on standard shapes; types c | `vision-raw/traitsAsCapabilities.md` | *(2026-08-14 annotation, consistency audit  naming fork closed — ShapeDefined confirmed 2026-08-14 in traitsAsCapabilities.md ("ShapeDefined is good"); ProtosShaped is dropped.)* |
| `flows/a5587095/vision/archive-structuredStringType.md`:91 | 2026-08-11 — Meaning lives in datom; seen by both languages | `flows/012fbf07/vision/threeStacks.md` | minimum for signal data intake. Also logged in threeStacks.md; the |
| `flows/a5587095/vision/archive-structuredStringType.md`:15 | 2026-08-11 — the idea | `flows/01a03eda/vision/archive-datomSyntax.md` | (datomSyntax.md). No delimiter, language assignment, or anatomy has |
| `flows/a5587095/vision/archive-structuredStringType.md`:56 | 2026-08-11 — the Meaning delimiter; context-switching parse | `flows/2b34fafa/vision/protosIsTheSharedStyle.md` | (protosIsTheSharedStyle.md). |
| `flows/a5587095/vision/archive-structuredStringType.md`:13 | 2026-08-11 — the idea | `vision-raw/colonFormTransformerSyntax.md` | `.{`, freeing parentheses (colonFormTransformerSyntax.md); the |
| `flows/a5587095/vision/archive-threeStacks.md`:9 | 2026-08-11 — ethos depends on datom; Meaning goes in datom | `vision-raw/structuredStringType.md` | during the structured-string design (structuredStringType.md). A |
| `flows/a5587095/vision/rustComponentArchitecture.md`:14 | 2026-08-11 — all method calls in our rust code are part of a trait | `flows/2b34fafa/vision/protosIsTheSharedStyle.md` | (protosIsTheSharedStyle.md). The comprehension surface is traits and |
| `flows/aa4c7747/vision/archive-ethosMonolith.md`:30 | 2026-08-24 — ethos-monolith bootstraps ethos-zero; call it ethos-cc?; ethos-zero is versio | `Vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `flows/aa4c7747/vision/archive-ethosMonolith.md`:28 | 2026-08-24 — ethos-monolith bootstraps ethos-zero; call it ethos-cc?; ethos-zero is versio | `Vision/sources/ethosMonolith.md` | nexus-core runtime concept overthinking. Vision/ethosMonolith.md is |
| `flows/aa4c7747/vision/archive-ethosMonolith.md`:30 | 2026-08-24 — ethos-monolith bootstraps ethos-zero; call it ethos-cc?; ethos-zero is versio | `flows/fe34eb/vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `flows/aa4c7747/vision/basePrompt.md`:5 | 2026-08-24 — harnesses are told to copy the code they find; change that in the base prompt | `flows/aa4c7747/vision/dispatches.md` | (Spoken as an aside while ruling the dispatch process, on why vertical-slice implementations go to a new repository; see dispatches.md.) |
| `flows/aa4c7747/vision/dispatches.md`:7 | 2026-08-24 — agreed design rounds print a dispatch to a codex flow for vertical slices | `flows/aa4c7747/vision/basePrompt.md` | (The base-prompt aside spoken immediately after this is logged in basePrompt.md.) |
| `flows/acbb6006/vision/archive-distillation.md`:5 | A small bit of psyche is not expanded into a theory | `Vision/datom.md` | 2026-08-27T15 20 37Z, the psyche, typed, on the proposed Vision/datom.md statement "Reply shape" ("A Nexus reply is written as its heads down to its data, and only what carries dat |
| `flows/acbb6006/vision/archive-distillation.md`:11 | Impurities are dissected out of the log, so the valid vision is not lost with them | `Vision/distillation.md` | 2026-08-27T15 20 37Z, the psyche, typed, on the proposed Vision/distillation.md statement "an impurity is destroyed, never archived." |
| `flows/acbb6006/vision/archive-distillation.md`:33 | A sources line is the id and the topic, nothing else | `flows/e06e4c07/vision/archive-nexus.md` | 2026-08-27T16 38 50Z, the psyche, typed, on the proposed sources-file format ("the archived file path and the record's heading and date — e.g. flows/e06e4c07/vision/archive-nexus.m |
| `flows/acbb6006/vision/archive-nexus.md`:33 | Skills live outside the runtime repository | `Vision/flowNexus.md` | 2026-08-27T14 40 26Z, the psyche, typed, quoting the proposed Vision/flowNexus.md statement "The flow repository holds the machinery of the Flow Nexus and a few basic skills " |
| `flows/acbb6006/vision/archive-nexus.md`:5 | Clients are packaged with the nexus, as separate crates: a datom-converting CLI per socket | `Vision/nexus.md` | 2026-08-27T14 40 26Z, the psyche, typed, on the proposed Vision/nexus.md statement "A Nexus is the whole" (reports/distillProposalNexus.md), quoting "the default CLI clients that s |
| `flows/acbb6006/vision/archive-nexus.md`:27 | The "first Nexus" statement is discarded | `Vision/orchestrate.md` | 2026-08-27T14 40 26Z, the psyche, typed, quoting the proposed Vision/orchestrate.md statement "Orchestrate is the first Nexus " |
| `flows/acbb6006/vision/archive-nexus.md`:39 | The engine inside a Nexus is Nexus Core | `Vision/sources/ethosMonolith.md` | 2026-08-27T15 20 37Z, the psyche, typed, on tension 1 (Nexus Core, the psyche's 2026-08-19 words, against "Nexus kernel" in Vision/ethosMonolith.md and "Nexus Kernel" in the nexus |
| `flows/acbb6006/vision/archive-nexus.md`:49 | The engine inside a Nexus is Nexus Core | `flows/fe34eb/vision/ethos.md` | See flows/fe34eb/vision/nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/acbb6006/vision/archive-nexus.md`:49 | The engine inside a Nexus is Nexus Core | `flows/fe34eb/vision/nexus.md` | See flows/fe34eb/vision/nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/acbb6006/vision/distillation.md`:5 | The listed impurities are destroyed | `Vision/sources/ethosMonolith.md` | 2026-08-27T15 20 37Z, the psyche, typed, on the impurity list of reports/distillProposalNexus.md, distillProposalProtosDatomAddendum.md, distillProposalPsycheProcess.md and Vision/ |
| `flows/ad19b1/vision/archive-kinds.md`:32 | 2026-09-04 — why is it Vision/kinds and not Vision/ethos? | `flows/995a164e/vision/kinds.md` | On the Identity distillate's destination, Vision/kinds.md |
| `flows/b05237/vision/operational-messengerPaneSyncFailure.md`:12 | Let's make sure the messenger is staying in sync with pane changes, because some messages  | `flows/b05237/vision/operational-reaperSubflow.md` | (operational-reaperSubflow.md) with the messenger angle, and connects to the |
| `flows/b05237/vision/operational-messengerSynchronizesRoster.md`:13 | If he makes all the calls, that means he can stay aware of who's who. He's synchronizing t | `flows/1ac573/vision/operational-mirrorToEveryoneAndRoster.md` | (1ac573/vision/operational-mirrorToEveryoneAndRoster.md) by giving that |
| `flows/b05237/vision/operational-messengerSynchronizesRoster.md`:7 | If he makes all the calls, that means he can stay aware of who's who. He's synchronizing t | `flows/b05237/vision/operational-centralMessenger.md` | (operational-centralMessenger.md, same date). The living names the consequence |
| `flows/b05237/vision/operational-reaperSubflow.md`:7 | We need the sessions that are done in Herder to be reaped. It's a temporary flow, and we c | `flows/1ac573/vision/operational-reapReplacedSessions.md` | (operational-reapReplacedSessions.md, flow 1ac573) named the need; this names |
| `flows/b05237/vision/operational-skillTypesTriad.md`:7 | The psyche and the mind is essentially what we call the operational skill — the knowledge  | `flows/8393ca/vision/operational-herdrVoiceAccess.md` | Source  flows/8393ca/vision/operational-herdrVoiceAccess.md. The living maps |
| `flows/b05237/vision/operational-voicePsycheDesktopAccess.md`:7 | We have a persona meta-harness in Herder. Access it from the desktop app with interactive  | `flows/8393ca/vision/operational-herdrVoiceAccess.md` | Source  flows/8393ca/vision/operational-herdrVoiceAccess.md, originating |
| `flows/b49251/vision/flowLaunching.md`:5 | Not only these kinds of flows run in the cluster: each main flow may run subflows in other | `flows/b49251/vision/psycheFlows.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the end of the message whose parts are in psycheFlows.md and visualPublication.md. "Show us the anatomy first. Ma |
| `flows/b49251/vision/flowLaunching.md`:5 | Not only these kinds of flows run in the cluster: each main flow may run subflows in other | `flows/b49251/vision/visualPublication.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the end of the message whose parts are in psycheFlows.md and visualPublication.md. "Show us the anatomy first. Ma |
| `flows/b49251/vision/heartbeat.md`:5 | A few different heartbeats; if Luna runs out the heartbeat cannot run, so it needs a backu | `flows/05c604/vision/quota.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the end of the message whose parts are in psycheFlows.md and quota.md. The closing questions (is that the compone |
| `flows/b49251/vision/heartbeat.md`:5 | A few different heartbeats; if Luna runs out the heartbeat cannot run, so it needs a backu | `flows/b49251/vision/psycheFlows.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the end of the message whose parts are in psycheFlows.md and quota.md. The closing questions (is that the compone |
| `flows/b49251/vision/layers.md`:5 | The second layer keeps all the knowledge of what is talked about, on the old Opus, because | `flows/b49251/vision/psycheFlows.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the third part of the message whose first parts are in psycheFlows.md and subflowDispatch.md. Logged by the main |
| `flows/b49251/vision/layers.md`:5 | The second layer keeps all the knowledge of what is talked about, on the old Opus, because | `flows/b49251/vision/subflowDispatch.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the third part of the message whose first parts are in psycheFlows.md and subflowDispatch.md. Logged by the main |
| `flows/b49251/vision/psycheFlows.md`:41 | Three levels of psyche flows, low, medium and high effort, with a Codex and a Claude equiv | `flows/05c604/notion/layers.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, after the per-harness correction ("this is coming together even more now"). The message continues in subflowDispa |
| `flows/b49251/vision/psycheFlows.md`:5 | An adaptable configuration of cluster flows by power consumption; by model, primary Astra, | `flows/05c604/vision/quota.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, right after its readiness report and the recycle of f55ec8, with the Codex weekly window at 3 percent. "codec" re |
| `flows/b49251/vision/psycheFlows.md`:41 | Three levels of psyche flows, low, medium and high effort, with a Codex and a Claude equiv | `flows/2f6b1dc5/vision/systemPrompt.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, after the per-harness correction ("this is coming together even more now"). The message continues in subflowDispa |
| `flows/b49251/vision/psycheFlows.md`:5 | An adaptable configuration of cluster flows by power consumption; by model, primary Astra, | `flows/b49251/vision/heartbeat.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, right after its readiness report and the recycle of f55ec8, with the Codex weekly window at 3 percent. "codec" re |
| `flows/b49251/vision/psycheFlows.md`:41 | Three levels of psyche flows, low, medium and high effort, with a Codex and a Claude equiv | `flows/b49251/vision/subflowDispatch.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, after the per-harness correction ("this is coming together even more now"). The message continues in subflowDispa |
| `flows/b49251/vision/psycheFlows.md`:25 | A variable number of flows on a cluster; the high-powered thinking module put on receiving | `flows/f55ec8/vision/flowRefresh.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, after the answer on Herder and the heartbeat. "3,740%" is read as thirty or forty percent, the refresh point the |
| `flows/b49251/vision/quota.md`:5 | When Fable gets scarce by itself, a way to get the usage out of Claude: entering the usage | `flows/b49251/vision/heartbeat.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the middle of the message whose first part is in psycheFlows.md and whose end is in heartbeat.md. The questions ( |
| `flows/b49251/vision/quota.md`:5 | When Fable gets scarce by itself, a way to get the usage out of Claude: entering the usage | `flows/b49251/vision/psycheFlows.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the middle of the message whose first part is in psycheFlows.md and whose end is in heartbeat.md. The questions ( |
| `flows/b49251/vision/subflowDispatch.md`:5 | The low effort answers quickly, "I'm going to think about this and launch flows to investi | `flows/b49251/vision/psycheFlows.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the second part of the message whose first part is in psycheFlows.md (third entry). "Isn't that the most reliable |
| `flows/b49251/vision/systemPrompt.md`:5 | The vision can start being included in the injected prompt or in the system prompt, depend | `flows/05c604/notion/layers.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the end of the message whose parts are in psycheFlows.md, subflowDispatch.md and layers.md. "If we are already do |
| `flows/b49251/vision/systemPrompt.md`:5 | The vision can start being included in the injected prompt or in the system prompt, depend | `flows/b49251/vision/psycheFlows.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the end of the message whose parts are in psycheFlows.md, subflowDispatch.md and layers.md. "If we are already do |
| `flows/b49251/vision/systemPrompt.md`:5 | The vision can start being included in the injected prompt or in the system prompt, depend | `flows/b49251/vision/subflowDispatch.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, the end of the message whose parts are in psycheFlows.md, subflowDispatch.md and layers.md. "If we are already do |
| `flows/b49251/vision/visualPublication.md`:5 | The vision distillation uses the book visual style report; an index of all these artifacts | `flows/b49251/vision/psycheFlows.md` | Context  typed to the primary Claude b49251 on 2026-09-16 evening, in the message whose stack answers are in psycheFlows.md. "I didn't see the updated version for that either" refe |
| `flows/b675f3d9/vision/archive-ethosMonolith.md`:14 | It becomes a nexus; everything will be a nexus | `Vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `flows/b675f3d9/vision/archive-ethosMonolith.md`:12 | It becomes a nexus; everything will be a nexus | `Vision/sources/ethosMonolith.md` | nexus-core runtime concept overthinking. Vision/ethosMonolith.md is |
| `flows/b675f3d9/vision/archive-ethosMonolith.md`:14 | It becomes a nexus; everything will be a nexus | `flows/fe34eb/vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `flows/b9f4f6/vision/flowModel.md`:5 | (file head) flowModel | `flows/ceb3b9fd/notion/thinkingProcess.md` | flows/ceb3b9fd/notion/thinkingProcess.md (types × phases, three a |
| `flows/b9f4f6/vision/flowModel.md`:3 | (file head) flowModel | `flows/ceb3b9fd/vision/topStratum.md` | Continues flows/ceb3b9fd/vision/topStratum.md (a phase is its own |
| `flows/b9f4f6/vision/presentation.md`:3 | (file head) presentation | `flows/04db2fd2/vision/overtalking.md` | Continues flows/04db2fd2/vision/overtalking.md (2026-08-27  "Stop |
| `flows/ba906ae2/vision/archive-encodedFormIsTheCode.md`:13 | 2026-08-14 — textualize is approved | `vision-raw/traitsAsCapabilities.md` | traitsAsCapabilities.md audit note "successor capability names are |
| `flows/ba906ae2/vision/archive-threeStacks.md`:27 | 2026-08-14 — the shortcut stack becomes a daemon; renamed ethos monolith | `flows/2b34fafa/vision/rustComponentArchitecture.md` | rustComponentArchitecture.md at the same timestamp. |
| `flows/bc05da32/vision/archive-interfaceRootEnumerators.md`:24 | 2026-08-22 — no derive for cli config: datom creates configuration options by its very sha | `flows/15b67974/vision/worldModelBeforeCode.md` | worldModelBeforeCode.md 2026-08-21. |
| `flows/bc05da32/vision/mainFunction.md`:5 | 2026-08-22 — maybe all we want is a simple macro: datom-derived type in, input selection a | `flows/bc05da32/vision/archive-interfaceRootEnumerators.md` | (interfaceRootEnumerators.md 2026-08-22 — configuration comes from |
| `flows/bc05da32/vision/skillDesigning.md`:17 | 2026-08-22 — a toy is not a good example; the proposed toy replacement is quackery | `vision-raw/machineAnatomy.md` | continuous with machineAnatomy.md 2026-08-21 (mine existing projects |
| `flows/ceb3b9fd/notion/thinkingProcess.md`:6 | 2026-08-30 — splitting the thinking process into phases; types × phases; three phases a gu | `flows/b9f4f6/vision/topStratum.md` | anatomy questions (vision/topStratum.md). The psyche marked the |
| `flows/ceb3b9fd/vision/hijackRepositories.md`:43 | 2026-08-30 — Autonomy-and-persistence block: overlaps our skills, thin, contradictory, one | `flows/b9f4f6/vision/topStratum.md` | vision/topStratum.md. |
| `flows/ceb3b9fd/vision/topStratum.md`:6 | 2026-08-30 — different top stratums for different jobs; the top stratum programmable per f | `flows/4ddc321d/vision/hijackRepositories.md` | assessment (vision/hijackRepositories.md), after finding that block |
| `flows/ceb3b9fd/vision/topStratum.md`:49 | 2026-08-30 — the above was drafting | `flows/ceb3b9fd/notion/thinkingProcess.md` | × phases, three as a guideline) is a notion  notion/thinkingProcess.md. |
| `flows/da1e3f/vision/operational-launcher.md`:5 | The current view of the system passes over into a launch script — one that the primary Psy | `flows/da1e3f/vision/operationalVision.md` | Context  typed to primary Psyche opus on 2026-09-17 as the closing of the operational-vision message (operationalVision.md, same date). The launcher target sits alongside Flow Nexu |
| `flows/da1e3f/vision/operational-psycheClusters.md`:5 | The psyche can be different models, not just Claude models; we're running it like that for | `flows/da1e3f/vision/operational-launcher.md` | Context  typed to primary Psyche opus on 2026-09-17. First half of the message; the second half is the Astra Psyche and doubting-role entry below, then the launcher goal in operati |
| `flows/da1e3f/vision/operational-psycheClusters.md`:5 | The psyche can be different models, not just Claude models; we're running it like that for | `flows/da1e3f/vision/operationalVision.md` | Context  typed to primary Psyche opus on 2026-09-17. First half of the message; the second half is the Astra Psyche and doubting-role entry below, then the launcher goal in operati |
| `flows/da1e3f/vision/operationalVision.md`:5 | Operational vision is vision that hasn't really been approved but can be used for now for  | `flows/da1e3f/vision/operational-psycheClusters.md` | Context  typed to primary Psyche opus (Claude, medium, flow da1e3f) on 2026-09-17 as part of the same message that refined the psyche cluster / mind cluster / core soul cluster pic |
| `flows/e06e4c07/vision/archive-nexus.md`:237 | 2026-08-19 — a Nexus is the whole component; the Nexus part is its execution engine; two s | `flows/024bc7/vision/nexus.md` | nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/e06e4c07/vision/archive-nexus.md`:237 | 2026-08-19 — a Nexus is the whole component; the Nexus part is its execution engine; two s | `flows/fe34eb/vision/ethos.md` | nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/e06e4c07/vision/archive-nexus.md`:244 | 2026-08-19 — a Nexus is the whole component; the Nexus part is its execution engine; two s | `flows/fe34eb/vision/nexus.md` | See flows/fe34eb/vision/nexus.md and flows/fe34eb/vision/ethos.md. |
| `flows/e4a40e/vision/distillation.md`:6 | 2026-09-03 — a proposal says where it goes and what it replaces, distilling with the disti | `Vision/protos.md` | they land in Vision/protos.md, without the current distilled text or |
| `flows/f426777b/vision/archive-nexusTraits.md`:30 | 2026-08-26 — the carrying syntax is very unrefined: too many heads in a row; traits must n | `flows/aa4c7747/vision/spokenVocabulary.md` | full statement is in spokenVocabulary.md.) |
| `flows/f426777b/vision/archive-nexusTraits.md`:70 | 2026-08-26 — Apply liked, not certain; the returned-generic trait prompts a need for new t | `flows/bc05da32/vision/mainFunction.md` | mainFunction.md 2026-08-21 ("not everything is a conversion, of |
| `flows/f426777b/vision/archive-nexusTraits.md`:74 | 2026-08-26 — Apply liked, not certain; the returned-generic trait prompts a need for new t | `vision-raw/genericParametersAreTraits.md` | on genericParametersAreTraits.md 2026-08-01 ("T would be a trait!"). |
| `flows/f426777b/vision/archive-spokenVocabulary.md`:71 | 2026-08-26 — Capability is great; wanted: "an object which has a capability" in one word;  | `flows/01a01a93/vision/skillDesigning.md` | skillDesigning.md — and asked what BFO is.) |
| `flows/f426777b/vision/archive-spokenVocabulary.md`:10 | 2026-08-26 — a different vocabulary one abstraction up from Rust; "trait" disliked as acou | `flows/fd301d9a/vision/nexusTraits.md` | those passages are additionally logged in nexusTraits.md.) |
| `flows/f426777b/vision/skillDesigning.md`:16 | 2026-08-26 — the protos philosophy was not understood in the first nexus/sema prototype; t | `flows/2b34fafa/vision/rustComponentArchitecture.md` | training-problem lineage (rustComponentArchitecture.md 2026-08-19 |
| `flows/f426777b/vision/skillDesigning.md`:18 | 2026-08-26 — the protos philosophy was not understood in the first nexus/sema prototype; t | `vision-raw/traitsAsCapabilities.md` | traitsAsCapabilities.md 2026-08-20 "a cornerstone of models not |
| `flows/f55ec8/vision/heartbeat.md`:5 | If Fable runs out, a Luna monitor sees the main Fable ran out and could not restart itself | `flows/05c604/notion/layers.md` | Context  typed to the primary Claude f55ec8 on 2026-09-16 evening, the end of the message in layers.md (same date) and the one-line reply that followed ("Yeah, heartbeat. Core is t |
| `flows/f55ec8/vision/modelRoles.md`:5 | Two Opus models, named by role: the older Opus, the wiser one, and the newer Opus, faster  | `flows/05c604/notion/layers.md` | Context  typed to the primary Claude f55ec8 on 2026-09-16, mid-turn, after the witness that claude-opus-4-6, claude-opus-4-7 and their [1m] ids are callable and the alias opus is O |
| `flows/f55ec8/vision/psycheMedium.md`:5 | Psyche Medium online, the one the living talks to instead of the Fable primary | `flows/05c604/notion/layers.md` | Context  typed to the primary Claude f55ec8 on 2026-09-17, during the recovery, after the evening's words on an interfacing flow on the old Opus in front of the Fable (layers.md, 2 |
| `flows/f55ec8/vision/psycheTool.md`:5 | Use Psyche to test Psyche: whether it can hold the four layers of psyche logging with the  | `flows/01a03d6e/vision/flowIdentity.md` | Context  typed to the primary Claude f55ec8 on 2026-09-16, the middle of the message whose surrounding parts are in flowIdentity.md, same date. Logged by the main flow before actin |
| `flows/f55ec8/vision/visualPublication.md`:30 | It is always a report, a Markdown report with flowcharts, the basis of the visual represen | `flows/e8c4cc61/vision/psycheLayers.md` | Context  typed to the primary Claude f55ec8 on 2026-09-17, the rest of the message in psycheLayers.md. Logged by the main flow before acting. |
| `flows/f6db8d/vision/arity.md`:5 | 2026-09-12 — reintroduce arity where it makes most sense, likely in Compositional | `Vision/datom.md` | Context  told that datom-codec 0.26.x had removed ARITY against the letter of Vision/protos.md 85 and Vision/datom.md 120,141, and that the open question was whether Compositional |
| `flows/f6db8d/vision/arity.md`:5 | 2026-09-12 — reintroduce arity where it makes most sense, likely in Compositional | `Vision/protos.md` | Context  told that datom-codec 0.26.x had removed ARITY against the letter of Vision/protos.md 85 and Vision/datom.md 120,141, and that the open question was whether Compositional |
| `flows/f6db8d/vision/metaCli.md`:5 | 2026-09-12 — the meta CLI is <component>-meta | `Vision/nexus.md` | Context  asked to settle the conflict between Vision/orchestrate.md ("meta-orchestrate") and Vision/nexus.md ("component-meta") that blocked the Orchestrate landing. |
| `flows/f6db8d/vision/metaCli.md`:5 | 2026-09-12 — the meta CLI is <component>-meta | `Vision/orchestrate.md` | Context  asked to settle the conflict between Vision/orchestrate.md ("meta-orchestrate") and Vision/nexus.md ("component-meta") that blocked the Orchestrate landing. |
| `flows/fd301d9a/vision/actorLibrary.md`:43 | 2026-08-21 — persona-spirit is abandoned | `vision-raw/spiritComponentAndFile.md` | Source  `psyche-raw/Vision/spiritComponentAndFile.md`, 2026-08-21, design session `15b67974`, typed and captured 2026-08-21T17 21+02 00. |
| `flows/fd301d9a/vision/nexusTraits.md`:5 | 2026-08-13 — mandatory traits are the comprehension surface | `Intent/mandatoryTraits.md` | Source  `psyche-raw/Intent/mandatoryTraits.md`, 2026-08-13, psyche-approved wording. |
| `vision-raw/archive-rustComponentArchitecture.md`:157 | 2026-08-14 — reconsider everything; keep the Signal Nexus SEMA vocabulary and principles,  | `Vision/archive-ethosMonolith.md` | retired to Vision/archive-ethosMonolith.md; what still stands is in |
| `vision-raw/archive-rustComponentArchitecture.md`:158 | 2026-08-14 — reconsider everything; keep the Signal Nexus SEMA vocabulary and principles,  | `Vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `vision-raw/archive-rustComponentArchitecture.md`:156 | 2026-08-14 — reconsider everything; keep the Signal Nexus SEMA vocabulary and principles,  | `Vision/sources/ethosMonolith.md` | nexus-core runtime concept overthinking. Vision/ethosMonolith.md is |
| `vision-raw/archive-rustComponentArchitecture.md`:158 | 2026-08-14 — reconsider everything; keep the Signal Nexus SEMA vocabulary and principles,  | `flows/fe34eb/vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `vision-raw/archive-threeStacks.md`:67 | 2026-08-11 — move forward; everything migrates to datom; the old repo is not a worry | `Vision/archive-ethosMonolith.md` | retired to Vision/archive-ethosMonolith.md; what still stands is in |
| `vision-raw/archive-threeStacks.md`:68 | 2026-08-11 — move forward; everything migrates to datom; the old repo is not a worry | `Vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `vision-raw/archive-threeStacks.md`:66 | 2026-08-11 — move forward; everything migrates to datom; the old repo is not a worry | `Vision/sources/ethosMonolith.md` | nexus-core runtime concept overthinking. Vision/ethosMonolith.md is |
| `vision-raw/archive-threeStacks.md`:68 | 2026-08-11 — move forward; everything migrates to datom; the old repo is not a worry | `flows/fe34eb/vision/ethos.md` | Vision/ethos.md, heading Zero. See flows/fe34eb/vision/ethos.md. |
| `vision-raw/archive-traitsAsCapabilities.md`:19 | 2026-08-13 — types first; traits are what types implement | `flows/6863ef19/vision/encodedFormIsTheCode.md` | *(2026-08-14 annotation, consistency audit  the "transcodable" vocabulary introduced in this entry was superseded later 2026-08-13 by the code/encoded drop and the ruling below ("t |
| `vision-raw/archive-traitsAsCapabilities.md`:52 | 2026-08-21 — ruling: infinitive verb form for action traits — Write, Read, Resolve, Create | `vision-raw/assembly.md` | statement is logged under assembly.md 2026-08-21; the lines bearing |
| `vision-raw/assembly.md`:94 | 2026-08-21 — Create dissolves: it would just be TryFrom | `flows/15b67974/vision/worldModelBeforeCode.md` | statement is logged under worldModelBeforeCode.md 2026-08-21; the |
| `vision-raw/assembly.md`:69 | 2026-08-21 — two things: the registry (index of sources) and the assembly file; combined b | `vision-raw/traitsAsCapabilities.md` | (d) the trait-naming ruling is logged in traitsAsCapabilities.md |
| `vision-raw/colonFormTransformerSyntax.md`:14 | (file head) "Name:TransformerName.( ... ) is the better syntax for named transformers" | `vision-raw/archive-colonConfusion.md` | `Name.Transformer.(...)`. Later same-topic entry  colonConfusion.md |
| `vision-raw/draftIdeasForImprovement.md`:15 | (file head) "a way to mark parts of the design as sort of draft ideas for improvement" | `flows/98fbfa47/vision/everyConceptShouldHaveItsRepo.md` | passage is logged in everyConceptShouldHaveItsRepo.md) |
| `vision-raw/importResolution.md`:19 | 2026-08-21 — the manifest should have everything needed to assemble; maybe an assembly fil | `flows/bc05da32/vision/mainFunction.md` | is logged under mainFunction.md 2026-08-21; the lines bearing on this |
| `vision-raw/importResolution.md`:12 | 2026-08-20 — a type that needs a name handed in to resolve the import is not resolvable | `vision-raw/traitsAsCapabilities.md` | trait-approach correction logged in traitsAsCapabilities.md |
| `vision-raw/machineAnatomy.md`:73 | 2026-08-21 — work backwards from the want; at least four parts: inputs, coherent input, co | `flows/58a86d/vision/visuals.md` | everywhere". Also carried  the visuals ruling (logged in visuals.md |
| `vision-raw/mainFunction.md`:160 | 2026-08-22 — main's chain begins at the input: a strictly typed object coming in as datom | `flows/15b67974/vision/flowDaemon.md` | input's contents. Continues flowDaemon.md 2026-08-18 (100% typed |
| `vision-raw/mainFunction.md`:72 | 2026-08-21 — main is a few lines; the program is a spec of objects tied by conversions; Tr | `flows/15b67974/vision/worldModelBeforeCode.md` | worldModelBeforeCode.md 2026-08-20/21. |
| `vision-raw/mainFunction.md`:69 | 2026-08-21 — main is a few lines; the program is a spec of objects tied by conversions; Tr | `flows/2b34fafa/vision/importResolution.md` | importResolution.md 2026-08-20, which concerned the authored side) |
| `vision-raw/mainFunction.md`:130 | 2026-08-21 — assembled Rust, not generated: still-to-write is not yet generated; the assem | `vision-raw/assembly.md` | unanswered at capture. (Ruled two the same day  assembly.md |
| `vision-raw/mentci.md`:26 | 2026-08-13 — the daemon is the central logic; front-ends are not Rust; Qt for Linux first | `flows/6863ef19/vision/signalIsOurMessagingLayer.md` | signalIsOurMessagingLayer.md, 2026-08-13. |
| `vision-raw/spirit.md`:19 | 2026-08-22 — spirit should start to live in entry-files: guaranteed higher stratum; a top  | `flows/012fbf07/vision/psycheLogStructure.md` | is in psycheLogStructure.md, same date) — the 2026-08-14 |
| `vision-raw/spirit.md`:40 | 2026-08-22 — the spirit skill retires when entry files carry spirit, generated; kept for n | `flows/15b67974/vision/entryFiles.md` | The message continues on entry files; that part is in entryFiles.md, |
| `vision-raw/structuredStringType.md`:5 | 2026-08-14 — cross-reference: datom rulings 2026-08-13/14 govern string and Meaning progre | `flows/01a03eda/vision/archive-datomSyntax.md` | *(2026-08-14 annotation, consistency audit  this file has no entries after 2026-08-12; the governing downstream rulings for the structured string live in datomSyntax.md and must be |
| `vision-raw/structuredStringType.md`:5 | 2026-08-14 — cross-reference: datom rulings 2026-08-13/14 govern string and Meaning progre | `flows/6863ef19/vision/encodedFormIsTheCode.md` | *(2026-08-14 annotation, consistency audit  this file has no entries after 2026-08-12; the governing downstream rulings for the structured string live in datomSyntax.md and must be |
| `vision-raw/traitsAsCapabilities.md`:20 | 2026-08-20 — trait methods that are regular functions pretending to be traits; a cornersto | `flows/2b34fafa/vision/rustComponentArchitecture.md` | training-problem lineage (rustComponentArchitecture.md 2026-08-16, |
| `vision-raw/visuals.md`:6 | 2026-08-21 — more visuals all the time; ASCII in responses, mermaid in artifacts | `vision-raw/machineAnatomy.md` | statement is logged under machineAnatomy.md 2026-08-21; the lines |
| `vision-raw/worldModelBeforeCode.md`:63 | 2026-08-21 — the protocol for creating the anatomy; From over Into, demand-driven; a softw | `flows/2b34fafa/vision/rustComponentArchitecture.md` | rustComponentArchitecture.md 2026-08-19, now named; (c) ruling  From |
| `vision-raw/worldModelBeforeCode.md`:60 | 2026-08-21 — the protocol for creating the anatomy; From over Into, demand-driven; a softw | `vision-raw/assembly.md` | assembly.md 2026-08-21); (b) still owed  the protocol for creating |
| `vision-raw/worldModelBeforeCode.md`:19 | 2026-08-20 — catching fake traits means we already failed; code before a model of the worl | `vision-raw/traitsAsCapabilities.md` | was written without the map. Continues traitsAsCapabilities.md |

### 3.5 Stated references whose target does not resolve to one file — 19

These are explicit references, but the name given matches several enumerated files
(the legacy `psyche-raw/` prefix has no directory at this revision, and topic
basenames repeat across flows). They are recorded as references, not edges: choosing
one target would be invention.

| stated in | heading | named target | candidates | quoted phrase |
|---|---|---|---|---|
| `Intent/protosParsing.md`:21 | (file head) Protos parsing | `psyche/Vision/protosIsTheSharedStyle.md` | 2 | psyche/Vision/protosIsTheSharedStyle.md. |
| `flows/01a02b46/vision/zeusUpdate.md`:59 | 2026-08-14 through 2026-08-19 — setup-independent deployment | `psyche-raw/Vision/setupIndependentInterfaces.md` | 2 | `psyche-raw/Vision/setupIndependentInterfaces.md` records |
| `flows/995a164e/vision/intent.md`:6 | Intent is never raw | `psyche-raw/Intent/data.md` | 2 | psyche-raw/Intent/data.md, following the two existing Intent files |
| `flows/995a164e/vision/vocabulary.md`:5 | The vocabulary is not settled enough to judge the distillation wording | `Vision/layers.md` | 4 | Context  terminal, on the flow's proposed Vision/layers.md sentence. |
| `flows/9993b5/vision/blockPropagation.md`:5 | These things should be continually proposed until they are seen by the | `efa157/heartbeat.md` | 2 | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that carries the harness-block-documentation vision (harnessBlockDocumentation.md, same |
| `flows/9993b5/vision/codexAsDoing.md`:5 | Can you use Codex to help you if you need to do something big, because | `efa157/vision/layers.md` | 4 | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17 immediately after the Codex-scarcity statement (codexScarcity.md, same date), relayed to primary Psyche opus (this flo |
| `flows/9993b5/vision/codexScarcity.md`:5 | We need to start using Codex; we do not have a lot of Claude usage | `efa157/vision/modelRoles.md` | 3 | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17, relayed to primary Psyche opus (this flow, 9993b5) by Fable's correction message. Names the operational reality  Clau |
| `flows/9993b5/vision/messagingIsScripts.md`:5 | Do you understand that my division and my psyche that reaches you have | `efa157/vision/messages.md` | 3 | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17, relayed to primary Psyche opus (this flow, 9993b5) by Fable's correction message. Twofold statement  (a) a check that |
| `flows/9993b5/vision/middleLayerRouting.md`:5 | Make sure all of my psyche that I've given to him comes to you through | `efa157/vision/layers.md` | 4 | Context  typed to primary Psyche fable (9d58d3) on 2026-09-17 as a direct order about the psyche-routing between the layers, relayed to primary Psyche opus (this flow, 9993b5) by F |
| `flows/9993b5/vision/powerLevels.md`:5 | What are the open-source models that were contenders for the high, med | `efa157/vision/layers.md` | 4 | Context  typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 mid-turn during the "make it operational" corrective. Renames the layer axis from High/Medium/Low as pure po |
| `flows/a60a9e85/vision/llmUnderstanding.md`:22 | 2026-08-23 — understanding by enactment, not regurgitation | `psyche-raw/Vision/context.md` | 7 | psyche-raw/Vision/context.md, 2026-08-17 — "LLMs don't actually have |
| `flows/cff271af/vision/distillation.md`:6 | 2026-08-22 — "It's always better to distill"; distilled psyche has mor | `psyche-raw/Vision/mainFunction.md` | 2 | correction to psyche-raw/Vision/mainFunction.md (a fabricated |
| `flows/fd301d9a/vision/actorLibrary.md`:35 | 2026-08-14 — the main engine is actor-driven and the library was forke | `psyche-raw/Vision/rustComponentArchitecture.md` | 7 | Source  `psyche-raw/Vision/rustComponentArchitecture.md`, 2026-08-14, typed. |
| `flows/fd301d9a/vision/actorLibrary.md`:50 | 2026-08-21 — hexis is not trusted | `psyche-raw/Vision/hexis.md` | 2 | Source  `psyche-raw/Vision/hexis.md`, 2026-08-21, design session `15b67974`, typed and captured 2026-08-21T17 21+02 00. |
| `flows/fd301d9a/vision/archive-nexusTraits.md`:11 | 2026-08-19 — universal Nexus traits are the ontology of an actor/dataf | `psyche-raw/Vision/nexus.md` | 9 | Source  `psyche-raw/Vision/nexus.md`, 2026-08-19, design session `e06e4c07`, typed and captured 2026-08-19T14 51+02 00. |
| `flows/fd301d9a/vision/archive-nexusTraits.md`:23 | 2026-08-19 — ontology before implementation | `psyche-raw/Vision/nexus.md` | 9 | Source  `psyche-raw/Vision/nexus.md`, 2026-08-19, design session `e06e4c07`, dictated and captured 2026-08-19T13 49+02 00. |
| `flows/fd301d9a/vision/archive-nexusTraits.md`:5 | 2026-08-22 — old code is at most inspiration for the map | `psyche-raw/Vision/worldModelBeforeCode.md` | 2 | Source  `psyche-raw/Vision/worldModelBeforeCode.md`, 2026-08-22, design session `15b67974`, typed and captured 2026-08-22T15 19+02 00. |
| `flows/fd301d9a/vision/nexusTraits.md`:17 | 2026-08-19 — the Nexus contains the execution engine | `psyche-raw/Vision/nexus.md` | 9 | Source  `psyche-raw/Vision/nexus.md`, 2026-08-19, design session `e06e4c07`, dictated and captured 2026-08-19T13 49+02 00. |
| `vision-raw/archive-threeStacks.md`:61 | 2026-08-11 — move forward; everything migrates to datom; the old repo  | `psyche/Vision/datomSyntax.md` | 9 | psyche/Vision/datomSyntax.md. |

### 3.6 Stated references pointing outside the psyche corpus — 90 lines

These name a file that is not a psyche record at this revision: flow logs, flow
reports, design documents, repository-root files, and `efa157/...` paths whose flow
directory does not exist. They are provenance the corpus asserts; they are not edges
between psyche records.

| named target | times stated | example site |
|---|---|---|
| `log.md` | 36 | `flows/056f6d/vision/messaging.md`:5 |
| `AGENT_VARIABLES.md` | 4 | `flows/358f143a/vision/entryFiles.md`:30 |
| `ARCHITECTURE.md` | 3 | `flows/98fbfa47/vision/draftIdeasForImprovement.md`:1 |
| `reports/PsycheConsistencyAudit-2026-08-14.md` | 2 | `flows/06196cc7/vision/psycheLogStructure.md`:13 |
| `awareness/realization.md` | 2 | `flows/358f143a/vision/awarenessIsGeneralUnderstanding.md`:7 |
| `SKILL_VARIABLES.md` | 2 | `flows/358f143a/vision/entryFiles.md`:65 |
| `reports/CodexInjectedInstructions.md` | 2 | `flows/358f143a/vision/skillDesigning.md`:14 |
| `efa157/vision/codexAccess.md` | 2 | `flows/9993b5/vision/codexRemoteAccess.md`:5 |
| `design/ProtosEngine/twoWayStructuralTranscoding-2026-08-11.md` | 2 | `flows/a5587095/vision/archive-protosIsTheSharedStyle.md`:73 |
| `reports/distillProposalNexus.md` | 2 | `flows/acbb6006/vision/archive-nexus.md`:5 |
| `reports/distillProposalProtosDatom.md` | 2 | `flows/b675f3d9/vision/archive-distillation.md`:5 |
| `flows/e06e4c07/log.md` | 1 | `flows/01a01bac/vision/testTravesties.md`:18 |
| `awareness/design.md` | 1 | `flows/1030529c/vision/awarenessIsGeneralUnderstanding.md`:34 |
| `datom-extended.md` | 1 | `flows/108ab0/vision/operational-designMosaic.md`:46 |
| `datom/extended.md` | 1 | `flows/108ab0/vision/operational-designMosaic.md`:46 |
| `datom-strings.md` | 1 | `flows/108ab0/vision/operational-designMosaic.md`:46 |
| `realization.md` | 1 | `flows/358f143a/vision/skillVoice.md`:34 |
| `design.md` | 1 | `flows/358f143a/vision/skillVoice.md`:35 |
| `handoff.md` | 1 | `flows/5c8be3ca/vision/flowArtifacts.md`:3 |
| `annotations.md` | 1 | `flows/5c8be3ca/vision/flowArtifacts.md`:71 |
| `sessionLogging.md` | 1 | `flows/7c3f0c1d/vision/psycheLogStructure.md`:4 |
| `component-triad.md` | 1 | `flows/98fbfa47/vision/archive-metaSignalNotOptional.md`:13 |
| `architecture.md` | 1 | `flows/98fbfa47/vision/draftIdeasForImprovement.md`:3 |
| `efa157/vision/incrementalRuntime.md` | 1 | `flows/9993b5/vision/criomOsUpgrade.md`:5 |
| `efa157/vision/lojix.md` | 1 | `flows/9993b5/vision/flowIdLayers.md`:5 |
| `efa157/vision/harnessRepositories.md` | 1 | `flows/9993b5/vision/harnessReplacement.md`:5 |
| `transcriptReporting.md` | 1 | `flows/9993b5/vision/structuredLog.md`:5 |
| `efa157/transcriptReporting.md` | 1 | `flows/9993b5/vision/transcriptOverFiles.md`:5 |
| `distillProposalProtosDatomAddendum.md` | 1 | `flows/acbb6006/vision/distillation.md`:5 |
| `distillProposalPsycheProcess.md` | 1 | `flows/acbb6006/vision/distillation.md`:5 |
| `reports/rustTraitAnatomy.md` | 1 | `flows/b675f3d9/vision/archive-kinds.md`:25 |
| `reports/capabilityAnatomy.md` | 1 | `flows/b675f3d9/vision/archive-kinds.md`:59 |
| `reports/flowsSkillEditProposal.md` | 1 | `flows/b675f3d9/vision/archive-remembering.md`:17 |
| `reports/distillProposalEthos.md` | 1 | `flows/b675f3d9/vision/archive-visionImpurities.md`:5 |
| `reports/visionImpuritiesSkillProposal.md` | 1 | `flows/b675f3d9/vision/archive-visionImpurities.md`:12 |
| `DesignExemplars-Rust-2026-08-21.md` | 1 | `flows/bc05da32/vision/skillDesigning.md`:19 |
| `operational-promptComponent.md` | 1 | `flows/da1e3f/vision/operational-harnessSpecificRules.md`:5 |
| `reports/mapSyntaxCorrection.md` | 1 | `flows/db97561c/vision/archive-prospective.md`:7 |
| `reports/protosDatomicEthosZeroRealization.md` | 1 | `flows/db97561c/vision/promptCrafting.md`:5 |
| `flows/e996e8/log.md` | 1 | `flows/e996e8/vision/editCoordination.md`:5 |
| `reports/CreateTraitCrateSearch-2026-08-21.md` | 1 | `vision-raw/assembly.md`:80 |
| `architecture-editor.md` | 1 | `vision-raw/draftIdeasForImprovement.md`:20 |

### 3.7 Graph density of the explicit edge set

Of the 953 enumerated files, **377 take part in at least one explicit edge** and
**576 take part in none** — 486 raw flow-vision records, 64 `vision-raw/` records,
25 notion records, and one distilled file, `Vision/x11.md`. Only 2 of the 81
non-archived `vision-raw/` records are cited by any source index.

A graph proposal must therefore expect roughly 60% of the corpus to be isolated
nodes under recorded relationships alone. That isolation is a fact about what the
records say, not evidence that those records are unrelated.

## 4. Inferred, unrecorded — this flow's inference, NOT grounded

Fifteen relationships that look likely but that no record states. None of these may
be drawn as an edge without the living psyche's word or a new record. One line of
reasoning each.

1. `vision-raw/highLevelView.md` ~ `flows/b675f3d9/vision/highLevelView.md` — the
   only byte-identical pair in the corpus (same SHA-256), so one is a copy of the
   other, but neither file says which came first.
2. `psyche-raw/Vision/<topic>.md` (cited 12 times) ~ `vision-raw/<topic>.md` — no
   `psyche-raw/` directory exists at this revision and the basenames match exactly,
   suggesting a directory rename that no record documents.
3. `psyche-raw/Intent/data.md` (cited in `flows/995a164e/vision/intent.md`) ~
   `Intent/data.md` — same rename inference, one level up.
4. `efa157/vision/<topic>.md` (cited 10 times from `flows/9993b5/vision/`) ~ the
   copies under `flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/`
   and `flows/f55ec8/handoff/successors-v7/sources/efa157/vision/` — identical
   relative path shape, and no `flows/efa157*` directory exists to hold the originals.
5. `flows/4decf7/vision/archive-kinds.md` → `Vision/ethos.md` — its header names
   `Vision/kinds.md`, which does not exist, while `Vision/sources/ethos.md` lists
   `4decf7 kinds`, so the target was probably folded into ethos and the header never
   updated.
6. `Vision/ethosMonolith.md` (6 dangling edge targets) ~ `Vision/archive-ethosMonolith.md`
   — the retirement note in 3.3 says what content moved, but nothing states that the
   file itself was renamed to the `archive-` form.
7. `Vision/sources/ethosMonolith.md` ~ `Vision/archive-ethosMonolith.md` — the index
   still indexes a retired topic, so it likely belongs with the archive, unstated.
8. `Vision/psyche.md` and `Vision/x11.md` lack a `Vision/sources/` index — probably
   authored directly rather than distilled, but nothing records their origin.
9. `Intent/data.md`, `Intent/mandatoryTraits.md`, `Intent/protosParsing.md` lack an
   `Intent/sources/` index — same gap at Intent level, and Intent is entered only on
   the living's explicit word, so the missing provenance is conspicuous.
10. The 15 files named `skillDesigning.md` across flows are plausibly one evolving
    topic, but only `flows/01a01bac/vision/skillDesigning.md` states a supersession,
    and it names no file.
11. The 9 files named `archive-datomSyntax.md` all cite `Vision/datom.md (Syntax)`
    under flow `e4a40e`/`e996e8`; they are plausibly siblings of one distillation
    pass, but no record states a sibling relation.
12. `flows/056f6d/vision/messaging.md` ~ `Vision/messaging.md` — same topic name, but
    `Vision/sources/messaging.md` lists only `108ab0` and `1ac573`, so the 056f6d
    record is probably undistilled rather than a source; its status is unwritten.
13. The 64 uncited `vision-raw/` records are plausibly still awaiting distillation per
    the `psyche` skill's "draining into `Vision/` as distillation touches it", but
    per-file drainage status is recorded only where an `archive-` header exists.
14. `flows/f55ec8/vision/*.md` ~ `flows/f55ec8/handoff/successors-v7/sources/f55ec8/vision/*.md`
    — 15 hashes are shared between the handoff bundles and the enumerated corpus, so
    some are exact copies, but no record pairs them file by file.
15. `flows/b49251/handoff/psyche-medium-v1/` and `flows/f55ec8/handoff/successors-v7/`
    both carry an `efa157` source set (32 and 29 files) that overlap by content; one
    bundle plausibly derives from the other, and neither says so.

## 5. Disconfirming checks run

- Every source-index line was resolved against the filesystem rather than assumed:
  181/181 resolve, 0 missing. Had any failed, it would appear here.
- Every archive-header target was checked for existence rather than trusted: 6 of 107
  are dangling, and they are listed in 3.2 with the others.
- Every `*.md` token appearing in record text was resolved: 353 resolved to one
  enumerated file, 19 matched several candidates, 90 pointed outside the corpus. The
  last two groups are kept out of the edge count.
- Heading counts were taken mechanically (`grep -c '^## '`) and are reported as
  candidate nodes; no heading was promoted to an edge anywhere in this manifest.
- The brief's globs were checked against `find`, which surfaced 89 vision records the
  globs do not reach. Reporting only the globbed set would have understated the corpus.
- All 953 files were tested for emptiness and UTF-8 decodability; none failed, so no
  file is reported as unread.

## Sources

Method: direct read of the working tree at
`6e59653af467dd099f6a0f95ebe4ab33eeb4219c`, on 2026-09-18, by a read-demanding Fable
subflow of main flow 056f6d. Enumeration, hashing, heading counting, and reference
resolution were done mechanically over the file set; quotations are verbatim from the
files named.

- Revision: `git rev-parse HEAD` and `jj log -r @-` in `/home/li/primary`, both
  `6e59653af467dd099f6a0f95ebe4ab33eeb4219c`.
- File set: `Vision/*.md`, `Vision/sources/*.md`, `Intent/*.md`, `Intent/sources/*.md`,
  `vision-raw/*.md`, `flows/*/vision/*.md`, `flows/*/notion/*.md` — 953 distinct files.
- Hashes: `sha256sum` per file. Heading counts: `grep -c '^## '` per file.
- Out-of-glob set: `find flows -path '*/vision/*.md'` minus the globbed set — 89 files.
- Relationship extraction: `grep` over the file set for `supersed`, `continues in`,
  `corrects`, `answers`, `distilled from`, `replaces`, `see also`, `provenance`,
  `originat`, `Source`, `Retired`, and for any `*.md` token in record text; each hit
  read in place and quoted.
- Skills loaded through the Skill tool: `subflow`, `psyche`, `flow-evidence`,
  `behavior`, `spirit`.
- Claim grade: every row in section 3 is witnessed by this flow's own read of the
  named file at the named line. Section 4 is this flow's inference and is witnessed by
  nothing.
