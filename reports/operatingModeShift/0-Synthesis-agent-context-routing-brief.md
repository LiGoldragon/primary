---
title: 0 — Agent Context Routing Brief
role: operatingModeShift
variant: Synthesis
date: 2026-06-25
topics: [agent-workflow, context-routing, subagents, mentci]
description: |
  Compact synthesis for a proposed operating-mode shift: lead agents preserve
  early context by delegating exploratory reads, while named short-lived
  sessions are routed by a controlled preflight process that selects skills,
  context, and prompt packs before the user prompt is handed to the worker.
---

# 0 — Agent Context Routing Brief

## Intent Anchors

[The main thread is the most precious context: the early high-fidelity window is reserved for the lead agent's deepest thinking and intent alignment.]

[Complex orientation uses fresh-context subagents first: when work needs exploration beyond one or two files, the lead dispatches a helper before opening files itself.]

[Agents keep the main thread in one of two modes: delegate any meaningful read, including startup orientation beyond the skill index, to a subagent; or interact directly with the psyche through questions, suggestions, and clarifications.]

[Subagent-by-default and parallel cross-audit are the universal workspace protocol, not a designer-only exception.]

## Local Procedures Triggered

The relevant local skills are `human-interaction`, `intent-alignment`, `when-to-use-helpers`, `helper-context-transfer`, `session-lanes`, `reporting`, `report-naming`, `intent-log`, and `spirit-cli`. `autonomous-agent` was relevant only for the work-loop contrast; no code work was authorized. `jj` was not triggered because this pass writes only a lane-owned report and makes no requested commit.

Lead procedure now:

1. Treat the current prompt as proposed direction unless the psyche ratifies it explicitly. Do not record a new Spirit entry yet.
2. Keep the lead in the two-mode discipline: either ask one focused psyche question, or dispatch a helper with the full reading envelope and stop reading.
3. For every helper, pass the required files, commands, source locators, boundaries, write authority, and return shape. The helper owns the broad read; the lead synthesizes from the distilled result.
4. If a helper writes a report or file, read back the written artifact for residue before trusting it.
5. Substantive synthesis belongs in `reports/<lane>/`; chat carries the path and the user-attention items.

## Problem Model

Early context is spent in four places:

1. Harness boot context: system/developer instructions, tool schemas, installed skills/plugins, connector metadata, and workspace `AGENTS.md`.
2. Durable project context: `AGENTS.md`, selected skill instructions, lane/report conventions, Spirit query results, and repo instructions.
3. Exploratory working context: file reads, command outputs, logs, search results, report triage, and source chasing.
4. Deliberation context: intent alignment, tradeoffs, decisions, plan graph, and final synthesis.

The proposed shift is sound if it moves item 3 out of the lead window while keeping item 4 in the lead. Item 1 is mostly fixed by the harness. Item 2 can be reduced through progressive disclosure and precomputed prompt packs, but cannot disappear without losing policy and intent safety.

Current official harness behavior aligns with this model:

- Codex `AGENTS.md` discovery is loaded before work and capped by `project_doc_max_bytes`, 32 KiB by default.
- Codex skills use progressive disclosure: the initial skill list is bounded, and full skill instructions load only after selection.
- Codex subagents are explicit, inherit sandbox/runtime policy, and are recommended for read-heavy exploration, triage, tests, and summarization.
- Claude Code also treats subagents as separate context windows for keeping exploration out of the main conversation; built-in Explore and Plan agents are read-only and optimized for research/planning.
- Generic OpenAI Agents SDK architecture distinguishes manager-style specialists-as-tools from handoffs. The manager-as-owner pattern fits this workspace: lead stays responsible, helpers are bounded capabilities.

## MENCI-Style Routing Shape

Use a contained preflight call before a named short-lived session starts. The preflight is not the worker and does not read broad context. It returns a typed routing packet:

```text
SessionRequest(user_prompt, cwd, requested_lane?, discipline_hint?, privacy_scope?)
  -> PreflightRouter
  -> SessionLaunchPacket(
       lane_name,
       discipline,
       required_startup_reads,
       selected_skills,
       spirit_queries,
       helper_plan,
       prompt_pack,
       sandbox_and_tools,
       report_slots,
       stop_conditions
     )
```

Recommended workflow:

1. Intake: classify privacy, authority, likely discipline, repo/lane scope, and whether the prompt is action, research, or alignment.
2. Skill routing: read only `skills/skills.nota`, select relevant skills, and avoid loading full skill bodies in the lead unless the lead itself must act.
3. Spirit routing: run a small set of public intent queries keyed by referents/topics; do not dump broad Spirit results into the worker prompt.
4. Prompt-pack build: assemble compact, versioned packs: workspace base, lane/report rules, selected skill excerpts, repo pointers, and helper dispatch templates.
5. Worker launch: start the named short-lived agent with the pack plus the psyche prompt. For broad exploration, launch an explorer first and require a report/structured brief before the lead proceeds.
6. Trace and drain: store the packet, source list, helper outputs, final report path, and drain result. Durable decisions go to Spirit; implementable work goes to beads; stale exploration retires.

For MENCI / `mentci` / `mencie` naming: local Spirit records mention both `mentci` as a psyche-facing status board for guarded workflows and `mencie` as a persona multi-modal UI implemented as Nexus schemas. The name and ownership should be clarified before writing architecture.

## Risks And Controls

Context blowup risk: subagents can multiply total token usage even while preserving lead context. Cap depth at one unless deliberately authorized; cap parallel workers; force structured return shapes and maximum report size.

Misrouting risk: a tiny preflight may choose the wrong skills or privacy level. Keep preflight conservative: when privacy/authority/domain is unclear, it returns a lead question rather than launching.

Duplicated reading risk: the lead reads what the helper reads. Enforce the minimal dispatch envelope and make helper reports carry exact file-section pointers.

Prompt-pack bloat risk: packs accrete every useful rule. Make packs layered and inspectable: base pack, discipline pack, task pack, repo pack. Each pack should have a byte/token budget and a source manifest.

Loss of judgment risk: routing can become automatic planning. The router should select context and ask/launch boundaries; the lead still owns synthesis and irreversible decisions.

Stale-context risk: precomputed packs drift. Put each pack under versioned generation with source paths, Spirit marker if used, and an expiry trigger when the source files or relevant Spirit records change.

## First Intent-Alignment Questions

Ask one per turn, but these are the first six in order:

1. Should this shift become a durable workspace rule now, or stay as an experiment for a few named lanes first? Recommended: experiment first, because the architecture touches routing, privacy, skill loading, and report discipline.
2. What is the first success case: a lead session that dispatches one explorer before reading, or a full MENCI-style preflight that launches a named short-lived session with selected skills and prompt packs? Recommended: one explorer-first session, then use its trace to design the preflight.
3. Who owns the final answer in the target workflow: the lead agent after helper summaries, or the routed specialist session itself? Recommended: lead owns the final answer; specialists are bounded tools unless there is an explicit handoff.
4. What should the preflight router be allowed to read before launch: only `skills/skills.nota` plus Spirit queries, or also selected report indexes / lane registry / repo metadata? Recommended: skill index plus narrow Spirit queries first; add indexes only when a concrete failure proves they are needed.
5. Should MENCI be the UI/status board for this routing, the process controller that launches sessions, or only the visible surface over orchestrate/agent/mind/criome? Recommended: MENCI as visible status/control surface, with orchestration owned by the existing typed components.
6. What is the hard budget for startup context in a routed worker: bytes, tokens, or named pack count? Recommended: explicit token/byte budgets per pack layer, because "small" will drift.

## Sources

Local: `skills/skills.nota`, `skills/human-interaction.md`, `skills/intent-alignment.md`, `skills/when-to-use-helpers.md`, `skills/helper-context-transfer.md`, `skills/session-lanes.md`, `skills/reporting.md`, `skills/report-naming.md`, `skills/intent-log.md`, `skills/spirit-cli.md`; Spirit records returned by searches for `subagent helper context`, `early context lead agent`, `MENCI`, and `session lane`.

External official/current sources: OpenAI Codex manual via `/tmp/openai-docs-cache/codex-manual.md` from `https://developers.openai.com/codex/codex-manual.md`; OpenAI Agents SDK docs at `https://developers.openai.com/api/docs/guides/agents` and `https://developers.openai.com/api/docs/guides/agents/orchestration`; OpenAI Agents Python tracing docs at `https://openai.github.io/openai-agents-python/tracing/`; Claude Code subagents at `https://code.claude.com/docs/en/sub-agents`; Claude Code memory at `https://code.claude.com/docs/en/memory`; Claude context windows at `https://platform.claude.com/docs/en/build-with-claude/context-windows`.
