*Kind: Frame · Topic: Persona engine architecture · Date: 2026-05-22*

# 0 — Frame and method

## What this directory is

This directory is a **meta-report** per intent record 231 — a
sub-agent session where the orchestrating second-designer dispatches
multiple specialised sub-agents (one per component slice), and each
sub-agent writes a numbered sub-report inside this directory. The
final synthesis sits in `9-overview.md`.

The session was authorised by psyche 2026-05-22 (the turn that
captured intent records 229–235) with the specific task: spec the
`owner-signal-version-handover` contract and produce a wide-view
architecture overview of the entire Persona engine — every
component it touches, what's implemented, what's pending, and how
the pieces fit together.

## Sub-reports

| #   | Title                                            | Author            |
|-----|--------------------------------------------------|-------------------|
| 0   | Frame and method (this file)                     | second-designer   |
| 1   | Persona daemon (engine-manager)                  | sub-agent         |
| 2   | signal-persona (Engine + EngineManagement)       | sub-agent         |
| 3   | signal-version-handover (working contract)       | sub-agent         |
| 4   | version-projection (trait library)               | sub-agent         |
| 5   | sema-stack — sema-engine + sema-upgrade          | sub-agent         |
| 6   | persona-spirit (first cutover target)            | sub-agent         |
| 7   | owner-signal-version-handover (wire spec)        | second-designer   |
| 8   | Standard agent behavior — workspace skill edits  | sub-agent         |
| 9   | Overview (meta-graph + synthesis)                | second-designer   |

Each component sub-report carries the same internal shape:

- `## What it is` — one-paragraph role of the component
- `## Current state` — what's implemented vs pending (with commits / beads)
- `## Diagram` — a mermaid diagram of its internal shape OR its role in the bigger picture
- `## Open design questions` — competing ideas to preserve (per intent 229)
- `## How it fits` — links to neighbouring sub-reports
- `## ARCHITECTURE.md update` — what the sub-agent changed in the component's ARCH file, if anything

The final overview (`9-overview.md`) composes a meta-graph using
selected diagrams from sub-reports (especially the implemented +
in-test parts), names the holes, and surfaces the next-step queue.

## Intent records this directory encodes

The session ran under intent records 229–235 (captured at the start
of the turn):

- **229** beads Principle — closing duplicate beads preserves
  information; competing design ideas kept
- **230** persona Decision — second-operator pivots to Persona
  review
- **231** reports Decision — sub-agent sessions land in a meta-report
  directory (`reports/<role>/<N>-<name>/`); this directory is the
  first instance
- **232** reports Principle — standard agent behavior: every chat
  response paraphrases a per-response report; 3–7 items in three
  balanced categories
- **233** workspace Principle — Criome workspace is intent-and-design-driven;
  designer/operator dance
- **234** workspace Decision — third role: auditor (mechanical
  flaw/pattern detector)
- **235** workspace Decision — automate the auditor; DeepSeek is the
  main auditor

Plus older records load-bearing for the architecture (203 smart
handover supersedes Path A · 207 commit_sequence in sema-engine · 208
Persona engine is the root component upgrade orchestrator · 209
Persona lands before Spirit cutover · 210 upgrade orders come via
the owner socket · 214 create owner-signal-version-handover ·
215+216 Persona naming).

## Sub-agent contract

Each sub-agent was dispatched with:

1. The scope of its component
2. The intent records relevant to it
3. The recent reports that already cover it (operator/158, /159,
   /160, /161, designer/285, /287, /286, etc.)
4. The directory path to write its sub-report into
5. Authority to update the component's `ARCHITECTURE.md` if
   substance changed (designer-tier work)
6. **No further sub-agent dispatch** (per intent record 5)
7. Output: one sub-report + optionally one or more ARCH.md commits

Each sub-agent returns a short chat-shaped paraphrase (per intent
232) of its sub-report; the substance lives in the file.

## How to read this directory

For agents picking this up later:

- Read `9-overview.md` first — it carries the meta-graph and points
  back to sub-reports for detail.
- For implementation work on a specific component, read the
  component's sub-report (#1–8).
- For session methodology (sub-agent dispatch shape, meta-report
  directory pattern), read this frame.

## Garbage collection

Per intent 231 this directory is one session unit. When the
substance migrates to permanent homes (ARCHITECTURE.md files,
skills, ESSENCE, INTENT.md), the whole directory retires together
— not piece by piece. The retirement should land via a
context-maintenance sweep.
