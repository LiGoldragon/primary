# Operational: the design mosaic of this session — messaging, Flow, Herdr, orchestrator

The living's directive: "Create an operational vision from all of this stuff in this session that was firmly said by the psyche as the design vision." This is that mosaic. It integrates the firmly-stated rulings from ~28 operational-* entries logged in flow 108ab0 on 2026-09-17. Verbatim quotes live in the individual entries; this file names the coherent design.

## Substrate: Herdr

Herdr is a real installed program at `~/.nix-profile/bin/herdr`, v0.8.2, "terminal workspace manager for AI coding agents." It runs as a headless server, exposes a JSON API socket, and provides all the primitives the flow cluster needs: `agent start`, `agent prompt`, `agent send-keys`, `agent list`, `agent wait`, `agent attach`, `session list / attach`, `pane split / list / read`, `workspace create / list`, `notification`, `api schema`. Do not wrap it, do not reinvent it — plug into it and reuse its user interface. When the psyche says "Herder," they mean this.

## Priority one: Hacky Messenger, now

A quick collection of scripts on top of Herdr that lets flows message each other today. Hacky, memorable, reliable. Precedes the proper Flow ↔ Herdr ↔ Message system. Codex builds it.

## The Flow ↔ Herdr ↔ Message triangle

- Flow owns the flow-id ↔ herdr-position map. New flows are launched via `herdr agent start`; Flow records the resulting pane. Retirement removes the entry. Flow starts a new flow by just calling `flow`, inside the Herdr server.
- Message takes a datom + recipient flow-id, asks Flow for the recipient's herdr position, and delivers through Herdr's primitives. The message body IS a datom that lands directly in the recipient's prompt as a datom-formatted object. No JSON envelope.
- Message priority is a datom head — `Priority.[HardAbrupt MiddleAbrupt Soft]`. Delivery mechanism per tier and per harness:
  - Hard abrupt on Codex: `herdr agent send-keys Escape` then the datom then `Enter`.
  - Hard abrupt on Claude: still open — Claude Code has no equivalent to Codex's Escape today.
  - Middle abrupt: `herdr agent prompt`. Claude receives at next tool boundary (verified this session — living's mid-turn typed messages arrive as `<system-reminder>` blocks alongside the next tool result).
  - Really soft: end-of-turn queue (`codex queue` today).

## Flow CLI

- `flow` (short form) spawns a new flow in a herdr pane. Preconfigured for a medium model. Datom argument.
- `flow` (extensive form) accepts a full Datom expression for elaborate launches. Best for testing.
- Low-power variant as a variant of the same command.
- `flow list` shows every running flow — piggybacks on herdr's own listing UI.
- `flow attach <name>` attaches a flow to the caller's local terminal. Requires a provenance feature: the CLI sends its launcher-process ID to the server so the server can attach the correct herdr pane to that terminal.

## Orchestrator: time-based merge management

- Every flow work item is time-boxed.
- The orchestrator assigns each flow its merge slot when ready — that tells the flow what to rebase on.
- If the flow accepts the slot, it holds the reservation.
- Merge must complete within its time; else the slot is released.
- If a flow is running out of time, the orchestrator can ask "do you need more time?" — the flow answers. Requires reachability.
- Reachability is why push-server-style messaging is needed for time-based system emergencies. Pull is insufficient for anything with a deadline.

## Mirror protocol

Every psyche statement typed by the living to any flow is mirrored, with context, to the paired psyche medium agent. Current implementation: primary Codex has been mirroring to primary Psyche opus via intercom_send. Reception on Claude side is PULL — flow polls intercom_pending as the first tool call of every turn until push-into-middle-stratum lands.

## Governance of vision and skills

- Skill IS vision. Same file. A topic has faces: core (`datom.md`), extended (`datom-extended.md` or `datom/extended.md`), subtopic-specific (`datom-strings.md`).
- Core Vision is more reviewed, more weight, more certain, more basic and broad. Extended Vision is elaborate detail with examples, less reviewed. Extended must not conflict with core.
- Operational skills live in their own repo, `operational-` prefix, agent-authored, glance-approved, more removable.
- Distillation flows upward: raw psyche → distilled Notion → Vision → Intent → Spirit. Double distillation Vision→Intent, Intent→Spirit. Vision distilled often.
- Curriculum stays as the Rust generation code; the skill Markdown content lives in a separate repo (already true today under the Curriculum / curriculum-deploy pair). No new `curriculum-skills` split needed.
- Herdr is the substrate for all terminal/agent work — do not reinvent.

## Primary layout

Primary contains only distilled psyche — `Spirit/`, `Intent/`, `Vision/`, later `Notion/` — plus top-level rule files (`CLAUDE.md`, `NON_MANAGEMENT_AGENTS.md`, `SKILL_VARIABLES.md`). Generated skill trees (`.claude/`, `.codex/`, `.agents/`, `.pi/`) regenerate from Curriculum — safe. Flows move to a separate repo (naming and ordering deferred).

## Same-tree rule for primary

Primary is not worktree'd. Every primary-repo change happens on `/home/li/primary` main. A merger role rebases every worktree on other repos onto main as main moves.

## Rules for agents, non-negotiable

- Subflow-first main flow. Delegate every locate, probe, tail-read, peer-message. Never run mechanical shell yourself.
- No UUIDs, session ids, rollout paths, or long hashes in main-flow context. Subflow scripts filter noise.
- Every write reserves an orchestrate lock over the paths written; release on commit.
- Primary always committed and pushed before idle. Dirty found in tree committed first as its own commit.
- The message datom head IS what the recipient sees. Never JSON.

## Posture

Messaging does not work reliably right now. Deploy and test in production. Iterate.

---

Verbatim entries this mosaic integrates (all under `flows/108ab0/vision/`):
`operational-abruptPerHarness`, `operational-coreAndExtendedVision`, `operational-curriculumAsModuleSystem`, `operational-curriculumSkillsRepo`, `operational-designMosaic` (this file), `operational-distillationHierarchy`, `operational-diskHygiene`, `operational-flowCliListAttachProvenance`, `operational-flowDatomLauncherLanguage`, `operational-flowHerdrMessageTriangle`, `operational-flowStartsFlows`, `operational-freshPrimary`, `operational-hackyMessenger`, `operational-herderMuxKeypress`, `operational-messageAsDatomInPrompt`, `operational-messagePriorityTiers`, `operational-mirrorToPsycheMedium`, `operational-multiplexerInjection`, `operational-operationalSkillsRepo`, `operational-primaryIsPsyche`, `operational-programmaticPromptComposition`, `operational-promptMosaicComposition`, `operational-psychePropagation`, `operational-pushMessagingForEmergency`, `operational-restartDirectives`, `operational-sameTreeAndMerger`, `operational-skillIsVisionUnified`, `operational-skillLagsVisionObservability`, `operational-skillTypes`, `operational-skillsAreVision`, `operational-timeBasedMergeSlots`.
