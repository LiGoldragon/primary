---
title: 465 - Agent Memory Claude Gating Exploration
role: operator
variant: Audit
date: 2026-06-25
topics: [agent-memory, claude, mind]
description: |
  Delegated exploration for gating Claude-specific memory defaults and routing
  shared agent memory through a reliable workspace substrate that all harnesses
  can use.
---

# 465 - Agent Memory Claude Gating Exploration

## Intent Anchors

[Agent memory defaults route through a reliable shared memory system shared across agents; Claude-specific memory use is an explicit gated path.] (Spirit `wl2a`)

[Persistent memory for tool-using agents is the queryable tool-call trace, not the model context window. Expose query_history back to the agent - structured filter, summary-on-demand, or vector retrieval modes.] (Spirit `rpog`)

[For normal harness agents, the main-thread baseline is a purpose-bounded lead/helper split: lead agents preserve early context by asking the psyche, dispatching helpers for all meaningful exploration, verifying only small mechanical facts, and synthesizing helper returns.] (Spirit `kc8t`)

## Psyche-Facing Training Requirements

This turn is a delegated-reader turn. The lead should not redo broad reading; it should synthesize from this report, inspect only narrow anchors while editing, and keep the final integration responsibility.

The relevant training requirements are:

- Capture durable psyche intent before source exploration. This report records new Spirit intent `wl2a` from the psyche's request to make shared memory the default and gate Claude-specific memory.
- Use public Spirit queries for public workspace mechanism, not private repositories. No `private-repos/` content was opened. User-level Claude credentials, history, and paste cache were not read.
- Write substantive findings to the active report lane; chat carries only path plus user-attention items.
- Treat current implementation as the source of truth for code shape, with beauty as the gate: shared memory should collapse into the existing `mind` substrate rather than adding a second Claude-only memory lane.
- If production code is edited after this report, follow repo intent first, use `jj`, commit the whole working copy on primary, and use targeted tests as witnesses.

## Spirit Findings

Spirit queries used:

- `spirit "(PublicTextSearch [Claude memory])"`
- `spirit "(PublicTextSearch [shared memory agents])"`
- `spirit "(PublicTextSearch [psyche-facing agent training])"`
- `spirit "(PublicTextSearch [memory system])"`
- Then `spirit "(Record ...)"`, accepted as `wl2a`.

Privacy-safe findings:

- `rpog` already says persistent memory for tool-using agents is a queryable tool-call trace, not model context.
- `kc8t`, `3ey7`, `30cu`, `69fa`, and `hu84` establish lead/helper discipline: subagents carry broad reading, the lead integrates, and cross-model audit is expected.
- `ky10` places `intent-alignment` in the common interactive-agent contract reached by Claude through `CLAUDE.md` and by Codex directly.
- `xlfo` says dispatched subagents inherit the dispatcher's lane/report numbering slot.
- `wl2a` adds the new specific policy: default memory should be shared across agents, while Claude-specific memory is explicit and gated.

## Current Claude Memory Surface

Primary workspace docs already point the right way:

- `CLAUDE.md` is only `@AGENTS.md`, so Claude reads the same workspace contract as everyone else.
- `INTENT.md:128-133` says memory and persistent state live in workspace files, not harness-dependent memory invisible to other harnesses or the human.
- `ARCHITECTURE.md:123-124` excludes persistent agent memory beyond workspace files, and `ARCHITECTURE.md:143-144` repeats that memory belongs in workspace files every agent can read.
- `.claude/settings.json:1-15` only adds a Rust-edit hook. It does not configure shared memory or disable Claude auto-memory.

The installed Claude CLI has a concrete default-memory gate:

- `claude --help` documents `--bare` as minimal mode that skips hooks, plugin sync, attribution, background prefetches, keychain reads, `CLAUDE.md` auto-discovery, and **auto-memory**. Therefore normal Claude startup includes an auto-memory path unless launch uses `--bare` or an equivalent future setting.
- `~/.claude.json` was inspected only for non-secret key names and specific non-secret flags. Current local flags show `cachedGrowthBookFeatures.tengu_session_memory = false`, `tipLifetimeShownCounts.memory-command = 2`, and no MCP servers configured for `/home/li/primary`. This is useful evidence but not a reliable policy gate; a GrowthBook flag can change.
- `claude mcp list` reports no configured MCP servers.
- CriomOS-home installs Claude Code in the Home profile at `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix:201-204` and sets `ENABLE_CLAUDEAI_MCP_SERVERS = "false"` at lines `522-525`. That disables ClaudeAI MCP servers but does not disable auto-memory.

Orchestrate currently assigns Claude by role:

- `/git/github.com/LiGoldragon/orchestrate/src/role.rs:175-180` maps `designer`, `second-designer`, `third-designer`, `nota-designer`, `system-designer`, `cloud-designer`, `poet`, and `counselor` to `HarnessKind::Claude`; all other roles default to Codex.
- `/git/github.com/LiGoldragon/harness/src/harness.rs:18-24` models `HarnessKind` as `Codex`, `Claude`, `Pi`, and `Fixture`.

## Current Shared Memory System

`mind` is the existing shared-memory candidate. Repo intent says `mind` owns Persona's central workspace state: work items, typed thoughts and relations, notes, dependencies, decisions, aliases, event history, subscriptions, and ready/blocked views. It persists through workspace-local `mind.sema`, opened only by `StoreKernel`.

Concrete anchors:

- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md:391-405` defines the work graph as the typed replacement for BEADS and lists implemented reducer requests: open, add note, link, change status, add alias, and query.
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md:568-575` states that the daemon owns `mind.sema`, CLI never opens the database, `StoreKernel` is the only database owner, and work/memory writes replace the typed `memory_graph` before success replies.
- `/git/github.com/LiGoldragon/mind/src/tables.rs:23-28` declares the `memory_graph`, thoughts, relations, and subscription tables; lines `157-174` register them through `sema-engine`.
- `/git/github.com/LiGoldragon/mind/src/actors/store/memory.rs:41-69` stages a memory write, commits it through `StoreKernel`, and only then replaces in-memory state.
- `/git/github.com/LiGoldragon/signal-mind/src/lib.rs:868-935` exposes the current work-memory request surface: `Opening`, `NoteSubmission`, `Link`, `StatusChange`, `AliasAssignment`, and `Query`.
- `/git/github.com/LiGoldragon/signal-mind/src/graph.rs:440-443` includes `ThoughtBody::Memory`; lines `626-642` define `MemoryBody` with `Session`, `Thread`, `IncidentRecord`, `Report`, and `Other` memory variants.
- `/git/github.com/LiGoldragon/mind/tests/cli.rs:46-74` proves text NOTA maps to `Opening` and `Query`; lines `132-168` prove the CLI opens and queries through the daemon.
- `/git/github.com/LiGoldragon/mind/tests/daemon_wire.rs:321-377` proves a work/memory graph item survives a daemon restart.

Verification run during this exploration:

- `cargo test mind_cli_opens_and_queries_work_item_through_daemon --test cli` in `/git/github.com/LiGoldragon/mind`: passed, 1 test.
- `cargo test mind_memory_graph_survives_process_restart --test daemon_wire` in `/git/github.com/LiGoldragon/mind`: passed, 1 test.

## Recommended Implementation Plan

Minimal write set:

1. Primary documentation manifestation:
   - Update `INTENT.md` near "Workspace truth lives in files every agent can open" to include Spirit `wl2a`: shared agent memory is the default; Claude-specific memory is gated.
   - Update `ARCHITECTURE.md` constraints to name the concrete gate: harness-private memory is not a default memory substrate; Claude auto-memory is only allowed through an explicit launch mode.

2. CriomOS-home Claude launch gate:
   - Add a wrapper or launcher setting in `/git/github.com/LiGoldragon/CriomOS-home` so ordinary workspace Claude launches use `claude --bare` or an equivalent explicit settings file that disables auto-memory by default.
   - Preserve a separate explicit escape hatch, for example `claude-with-memory`, for sessions where the psyche intentionally wants Claude's own memory. The positive rule is: normal Claude launch is shared-memory-only; the alternate command opts into Claude-specific memory.
   - Verify `claude --help` still advertises `--bare` and run the wrapper with `--help` or a harmless `--version`/print-mode smoke test.

3. Shared memory access surface:
   - Prefer `mind` as the shared memory substrate rather than adding a new store. For the first slice, expose a tiny command or skill-level protocol that writes durable notes/tasks through `mind` NOTA text:
     - open memory/work: `mind "(Opening Task High [title] [body])"`
     - add note: `mind "(NoteSubmission (Display <id>) [body])"`
     - query: `mind "(Query (Open) 10)"`
   - If the desired data is not work-item-shaped, use the typed thought-memory surface in `signal-mind` rather than broadening Claude storage. That may require extending `mind` text projection around `ThoughtBody::Memory`.

4. Orchestrate/harness integration:
   - Add the memory gate at the Claude launch/spawn boundary, not at every role mapping site. The role mapping in `orchestrate/src/role.rs` should continue to choose Claude for designer-like lanes; the spawn adapter should decide whether Claude starts in normal shared-memory-only mode or explicit Claude-memory mode.
   - Future `harness` integration should record/query shared memory through `mind` and observe harness transcript history separately, matching `harness/INTENT.md`: harness owns transcript observations and lifecycle, not cross-agent memory policy.

Recommended verification commands:

- In `mind`: `cargo test mind_cli_opens_and_queries_work_item_through_daemon --test cli`
- In `mind`: `cargo test mind_memory_graph_survives_process_restart --test daemon_wire`
- In `CriomOS-home`: run the existing flake/Home check for the min profile or the narrow package check that covers the AI package set, then smoke-test the new Claude wrapper with `claude-shared --help` or equivalent.
- In `orchestrate` or `harness` if the spawn adapter changes: run the role/harness mapping tests and add one witness that a Claude-bound role receives the shared-memory-only launch vector by default.

## Risks And Open Questions

- The local Claude CLI flag `--bare` also skips hooks and `CLAUDE.md` auto-discovery. If the wrapper uses `--bare` directly, it must re-add the workspace contract explicitly through `--add-dir`, `--append-system-prompt`, or another controlled context path. Otherwise the memory gate would accidentally bypass the agent contract.
- `cachedGrowthBookFeatures.tengu_session_memory = false` is not enough as policy; it is a local experiment flag and can flip.
- `mind` has two memory surfaces: the implemented work-memory graph and the typed `ThoughtBody::Memory` graph. The first slice should decide whether shared agent memory means operational work notes first, or typed session/thread/report memory first.
- User-level `~/.claude` contains credentials, history, and paste-cache. I did not inspect those contents. Any migration or cleanup of Claude-private state needs explicit psyche authorization and a privacy plan.
- I did not find current Claude MCP servers. A future shared-memory bridge can be a CLI wrapper first; an MCP bridge is optional and should not be assumed to exist.
