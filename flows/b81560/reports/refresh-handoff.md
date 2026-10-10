# Refresh handoff from flow b81560 — Psyche Medium (Opus 4.6, 1M context)

Written 2026-09-20 by Psyche Medium (Claude Opus 4.6, medium effort,
flow b81560). Successor is Psyche Medium of b81560.

## Identity

- Flow ID: `b81560`, claimed via `flow-id claude` at session start.
- Role: Psyche Medium, the medium-power Psyche primary Claude flow.
- Predecessor: flow `1ac573`. Its handoff and successor brief were in the
  bootstrap bundle.
- Model: `claude-opus-4-6[1m]`, medium effort.
- Session: `b8156034-b845-43c4-890a-49a73d806ee1`
- Herdr: `opus-of-b05237` in `messaging-build`, pane `wD:p1`

## Morning flashbooks

Published at https://claude.ai/code/artifact/d92c5257-e887-4962-8f98-a653a51dce38

Five views: what we see, what we built, problems, what you can use, testing
skills. Current as of 2026-09-20 morning with all overnight results.

Other artifacts published this session:
- Signal Path (architecture): https://claude.ai/code/artifact/0c59c19d-e113-43fb-a937-fcbdd4bf2bfd
- Session Flashbook: https://claude.ai/code/artifact/c68ec11e-7dc1-4acf-843e-cf063b5f8789
- Remote Control Options: https://claude.ai/code/artifact/9c471507-941b-4baa-807b-e3dd663fe180
- Fable Questions: https://claude.ai/code/artifact/6a5bdb80-8a29-4fba-b074-3fabf518ec1f
- OpenCode Remote Access: https://claude.ai/code/artifact/7d38d2d3-1634-426e-ba75-00f52c1226c0

## Psyche logged this session

30+ vision entries at `flows/b81560/vision/`, covering:

**Triad and routing:** triadWorkDivision, verticalRoutingThroughPsycheFirst,
mindMapsComponents, flowCLIStartsSessions, deployOnTheHostYoureOn

**Messaging:** herderTriadSpaces (corrupted — needs transcript recovery),
messagingSimpleSystem, herderMessagingReport, hooksAsEventSource,
reapingOnRefreshAndFlowEndHook, refreshFlowAndMessageFlowCoordination,
refreshOutboxAndMessageChannels, mentciTopologyNotRouter,
psychePropagationAndNamingAndInfrastructure

**Datom:** datomEverythingSystemPrompt, datomHackyMessagingAndLanguageUpgrade,
datomObservabilityAndMindLayer, flowDatomCLIAndSignalLibrary,
ethosEscapeDelimiter

**Meaning language:** meaningLanguageLogographic, meaningLanguageAnnotationLayers,
meaningContentAddressedAnnotation, meaningGarbageCollectionAndOntology,
meaningDualSanskritEnglishNames, meaningStructureRootVariant,
vaisheshikaRuledAndSyntaxQuestion, asyncSubflowsAndMeaningLanguage,
fieldUltraLowRoutesSubflowRequests, subflowRequestIdAndAsync

**Infrastructure:** quotaAwarenessSystem, openSourceRemoteAccess,
openCodeAndroidApp, openCodeTestWithCodexSubscription,
openCodeOnUranusNotZeus, deployOnTheHostYoureOn, pocSandboxVmFirst,
pocSandboxIntent, explicitFilePathCommits, horizonNexusAndNodeResources,
visualizationToolkitAndTestingModules, quotaBurnRateVisualGraphs,
remoteControlResearchReport, lowFrictionCommunication,
slideFlowAndFlowAuthorization, nightWorkDirective

## Open items

1. **herderTriadSpaces.md corrupted** — contains git error text, not psyche
   words. Needs transcript recovery. Fable flagged this.
2. **Living's artifact comments on Session Flashbook** — 4 comments logged as
   vision (flowDatomCLIAndSignalLibrary, ethosEscapeDelimiter,
   mentciTopologyNotRouter, refreshOutboxAndMessageChannels). Thread IDs
   in artifact c68ec11e. Not activated for Claude replies.
3. **STT corrections await glance** — Mine→Mind, Salt→Sol, cykhi→psyche high,
   Menchie→Mentci, CreoOS→CriomOS. In-file corrections noted.
4. **Morning flashbook questions unanswered**:
   - Approve datom-codec 0.31.0 upgrade across Lojix contracts?
   - Glance on 5 testing skills?
   - Reap on refresh: yes once gates pass?
   - Field naming: of-ancestor kept or dropped?
   - Fable delegation ceiling confirmed?
   - Distill layers or datom first?
   - Ethos-in-datom escape delimiter glyph?
   - Low-priority channel shape?
   - Psyche idle timer action?
5. **Lojix/Horizon datom-codec skew** blocks theme activation and OpenCode.
6. **Meaning roundtrip unvalidated** — exit 124, no rerun.
7. **Flow/Message registries empty** — the single biggest infrastructure gap.
8. **Messaging delivery gate** — in-memory draft only, not complete.

## Skills landed this session

- `flow-aspect` — triad work division, vertical authority
- `flow-communication` — medium-to-medium, psyche propagation, routing axes
- `file-editing` updated — explicit file-path commits
- `Intent/testing.md` — sandbox first
- 5 `testing-*` skills — push-landed, commit-scope, generated-projection,
  long-run-progress, message-route

## Rules this flow held

- Subflow-first: delegate every locate, probe, read, message.
- Explicit file-path commits (landed as a skill rule during this session).
- Log psyche verbatim before acting, in the flow's own vision directory.
- Low-friction communication: flashbook artifacts as the default mode.
- Psyche propagation: forward living's words with context and planned response.
- No Vision landings without the living.
- Primary always committed and pushed.

## Current roster

- Psyche High: `psyche-fable-of-c8d79f` (f38926)
- Psyche Medium: `opus-of-b05237` (b81560, this flow)
- Mind: `mind-astra-of-893603` refreshed to 9e7ea5
- Field Astra: 1cb440
- Field Sol: 8565e8 (incumbent)

## What the successor needs

Load the same skills as this flow plus the new ones (flow-aspect,
flow-communication). Ask the living to type `/main-flow`. Collect
overnight reports from Fable's summary at `flows/f38926/summary.md`.
The morning flashbooks are the living's entry point — the successor
maintains them.

## First task: vision/skill consolidation

The living ordered (2026-09-20): "get a young Psyche Medium to bring
together all of the vision distillation and skill distillation, and
the situation on why we still don't have everything." Vision = skill:
every vision record should correspond to a skill. Three repos (Psyche,
Mind, Field) hold the skill data at three levels, generating skills
through Curriculum. Map all vision against all skills, identify what's
distilled vs raw vs missing, and produce the consolidated situation.

## Additional corrections for the successor

- `tools/prompt-relay` with `--source-format peer-file` injects a noisy
  JSON provenance header. Do not use it for live context or handoffs.
  Use native structured first-turn skills/source injection.
- `jj commit` with multiple path arguments makes an empty commit —
  use one fileset `'a | b'` instead.
- Every session must START IN HERDR with exact live pane binding before
  HM messaging is trusted. App-server-only launches fail the gate.
