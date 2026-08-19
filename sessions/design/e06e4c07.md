# Design flow e06e4c07 — flow, the Nexus that sets up and starts a model flow

## Summary

Designing `flow` by asking the living psyche one topic at a time. So far:
the Nexus vocabulary settled (Nexus = whole, Nexus Core = engine; signal
contracts; meta access case by case; skill renamed `nexus`; a nexus repo
wanted; "why" goes to a parallel rationale skill); four prior-art reports
landed (reports/NexusPriorArt-*-2026-08-19.md); recent-expectation sweep done
(session-log shape now short-id files). Skills deployed: nexus (renamed, edges,
Nexus Core, traits lines), nexus-rationale, subflows liability line. Transcript
search shim built: github.com/LiGoldragon/transcript (show/search/raw).
Question 1 on flow itself (existing harness vs own model loop) unanswered.

## Objective

Design `flow`, the Nexus that sets up and starts a model flow with its own
working directory, system prompt, training files, and instruction prompt. It
replaces the plan for a `training` repo; Curriculum stays hand-maintained
until flow replaces what it does.

## Governing direction

The Designer does not know how flow is designed; the living psyche does. Ask,
in clear simple questions, one topic at a time; each question restates in a
line what it is about. No anatomy proposed before asking. When the design can
be stated back coherently and simply, state it and ask whether it is right.
Knowledge drips into every flow it concerns (flowKnowledge, 2026-08-19).

## State

Read at start: psyche/Vision — flowDaemon, trainingRepo, skillsRepository,
entryFiles, skillTypes, gradientsOfAuthority, falseConfidence, behavior,
letsUseTheSameVocabulary, managementDelegation, skillVoice, flowsNotAgents,
flowNaming, workspace-2.0.

Research returned 2026-08-19, four reports in reports/NexusPriorArt-*:
IncrementalSystems (Erlang/OTP, MINIX 3, Fuchsia, Wasm CM; compiler claim
holds for native binaries), SocketsAndContracts (two-socket privilege
separation prior art; Cap'n Proto closest; rkyv has no evolution mechanism),
FlowsNamesHarness (synecdoche naming; "Nexus" collides with an arXiv
multi-agent framework and repos; Morrison FBP; harness prompt categories;
Codex prompt witnessed), SoftwareOntology (laws as the criterion; Header vs
Role Interface; OntoClean; Parnas → Liskov → Brady). Reference skill
collections hold no prior art on these situations.

Cross-flow: Design `e4be1c4a` (sessions/design/2026-08-17T1128.md) carries
the mandatory-traits / ontology discussion; its trait-design prompt is printed,
unspent. Its rulings were relayed into this flow; this flow's Nexus rulings
are in psyche/Vision/nexus.md for it. Design `7c3f0c1d` owns the session-log
and strata skill changes.

Recent-expectation sweep (2026-08-19): session files now `<short-id>.md`, no
frontmatter, terse summary on top, index file wanted (ruled, skill not yet
updated — this file conforms); psyche skill source already says living psyche
is always called living psyche (deployed copy stale); vocabulary skill still
carries the refused "one flow" line; skill-designing: no bullets, no paths in
skills (ruled, pending); docs are not evidence for code (ruled, pending).

## Open, awaiting the living psyche

- batched skill edits for green: vocabulary (drop "A flow is liable for its
  subflows."; add "Transcript: the file the harness writes holding a whole
  session from beginning to end."); skill-designing ("A line that restates a
  rule another skill holds." under Cut these); nexus porting-by-extraction
  sentence keep/cut.
- universal nexus traits: first question — the smallest set of things every
  Nexus does. Then signal and sema compared against the map.
- briefing role (name proposed) + subflows line, now to use the transcript tool.

- Question 1: does flow launch an existing harness (Claude Code / Codex) with a
  composed system prompt, or run its own model loop?

## Rulings logged this session

- managementDelegation 2026-08-19: "a flow and its subflows are one flow"
  refused — out of context.
- nexus (new topic) 2026-08-19: two entries — the Nexus statement; Nexus Core,
  signal contracts, meta case by case, rename, repo, parallel skill.
- flowDaemon 2026-08-19: flow repo = machinery + a few basic skills replacing
  the built-in harness prompt; user skills in another repo; name stays flow.
- flowsNotAgents 2026-08-19: agent = whole being; synthetic intelligence.
- rustComponentArchitecture 2026-08-19: component is a Nexus; placeholder
  traits; ontology before implementation; Ethos.
- letsUseTheSameVocabulary 2026-08-19: living psyche always called so.
- skillDesigning 2026-08-19: parallel skill for a skill's reasoning.
- flowKnowledge (new topic) 2026-08-19: discussion drips into every flow it
  concerns; skill or subagent role; transcripts belong to another nexus, shim
  tool for now.
- nexus 2026-08-19 (later entries): core-<nexus> already killed; at least two
  sockets; CLI per socket; nexus repo a possibility; universal nexus traits
  first; edge/contract both kept, edge line approved.
- skillDesigning 2026-08-19: rationale approved; no line repeated across
  skills; batch skill edits.
- gradientsOfAuthority 2026-08-19: no way for a computer to know its input is
  from a psyche; the proposed behavior line rejected fully.
- letsUseTheSameVocabulary 2026-08-19: transcript names the harness file.
- managementDelegation 2026-08-19: liability meaning; split vocabulary/subflows.
