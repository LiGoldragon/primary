*Kind: Frame · Topic: intent-manifestation sub-agent session · Date: 2026-05-23*

# 0 — Frame and method

## What this directory is

Meta-report per intent record 231 — the orchestrating second-designer
dispatches multiple specialised sub-agents to manifest recent
psyche intent into workspace files (ARCH, skills, beads), audit
recent operator work, and write sub-reports here. The final
synthesis lives in `7-overview.md` (the highest-numbered file).

Per psyche 2026-05-23:
- "start subagents in parallel when you have all the intent, and
  send them on errands to manifest intent into architecture files
  and design/implement/audit beads and final reports in a
  meta-report directory"
- "read all fresh intent and designer/operator reports"

## Intent records being manifested

The session manifests intent records captured in the last ~6 hours
(running count as of dispatch):

- **270** component-shape Clarification — component binary naming
  (CLI is `<component>`, daemon is `<component>-daemon`; no separate
  binary called the component name; `persona`, `spirit`, `harness`,
  `orchestrator` follow the same pattern)
- **271** signal Decision — refined 64-bit signal type structure:
  byte 0 root verb (most universal quality, "beingness"); bytes 1-7
  data-carrying sub-variants forming the verb namespace; 8 enums
  total (1 root + 7 sub)
- **272** signal Decision — universal data variants pre-allocated
  across all signal namespaces (U8, U16, possibly more); Criome may
  use 16-bit short ID for public key with polite-rename-on-collision
  convention
- **273** signal Decision — extended (64-byte / 512-bit) version
  accommodates public keys, identities, larger structured data;
  Criome authorization payload is the canonical example
- **274** signal Clarification — Mirror payload (signal-version-handover)
  is raw bytes in a SEPARATE container outside the typed database;
  type signature is "unspecified raw payload"; deferred typed-enum
  decision
- **275** persona-mind Decision — once persona-mind ships, agent
  errors (mermaid syntax, NOTA formatting, naming violations, etc.)
  log into Mind as typed events; basis for skill-improvement loops
  + auditor input; subtypes-development is one of the most important
  parts of Criome-stack design
- **276** workspace Decision — code comments use NOTA-formatted
  signal records ("nota in the comments"); signal-in-text-form
  because comment lives in code; markdown-readable +
  NOTA-syntax-highlightable; enables Mind to read code-as-signal;
  comments carry the why of each edit

Plus historical context for the manifestation:
- **244** + **251** three-tier signal sizing (Part 1 leans adopted)
- **252** Design D ratified (Persona FD-handoff via SCM_RIGHTS)
- **255** designer delegation pattern
- **256** audits feed beads

## Sub-reports + sub-agent assignments

| # | Title | Author |
|---|---|---|
| 0 | Frame and method (this file) | second-designer (orchestrator) |
| 1 | Signal 64-bit verb-namespace ARCH manifestation | sub-agent A |
| 2 | Component binary naming convention codification | sub-agent B |
| 3 | signal-version-handover Mirror raw-container ARCH refresh | sub-agent C |
| 4 | NOTA-as-comments new skill | sub-agent D |
| 5 | persona-mind agent-error event design | sub-agent E |
| 6 | Operator work audit + recent commits absorption | sub-agent F |
| 7 | Overview (final synthesis) | second-designer (orchestrator) |

Each component sub-report carries this internal shape:

- Frontmatter: `*Kind: ... · Topic: ... · Date: 2026-05-23*`
- `## What this slice is` — the scope
- `## Workspace files changed` — list of edits (with jj commit refs
  when ARCH or skill files land)
- `## Diagram(s)` — mermaid where it helps (per
  `skills/mermaid.md`; avoid `;` in sequence-diagram Notes; avoid
  Unicode arrows in sequence body; avoid pipe-delimited labels in
  sequenceDiagram — flowchart syntax bleeds in often, fix is
  separate sequence-diagram messages or move to flowchart)
- `## Beads filed or updated`
- `## Open follow-ons` — questions surfaced that need future
  attention
- `## How it fits` — links to neighbouring sub-reports

## Sub-agent contract (read by every sub-agent)

1. You are a second-designer-window sub-agent (designer discipline:
   architecture as craft).
2. Do the slice described in your prompt. Don't expand scope.
3. **Do NOT dispatch your own sub-agents** (intent record 5).
4. Use the deployed `spirit` CLI for intent observation if needed;
   do NOT capture new intent records (the orchestrator handles
   intent capture).
5. Use `jj` for version control with HEADLESS `-m '<msg>'` flag
   (intent 237). Never let jj open an editor.
6. All `nix` invocations use `--max-jobs 0`.
7. Use full English names per `skills/naming.md`.
8. NOTA records are positional per `skills/nota-design.md`.
9. No `---` horizontal-rule lines in markdown.
10. Opaque identifiers (commit hashes, bead UIDs) carry inline
    description on first mention in chat-facing text.
11. Sub-report path: `/home/li/primary/reports/second-designer/159-intent-manifestation/<N>-<slug>.md`.
12. Chat response paraphrases your sub-report per intent 232:
    3-7 items, balanced across (a) intent questions/clarifications,
    (b) observations/explanations, (c) examples/evolving picture.

## How to read this directory

- Read `7-overview.md` first for the synthesis.
- For specific manifestations, read the relevant sub-report (#1-6).
- For session methodology, read this frame.

## Garbage collection

Per intent 231 this directory is one session unit. When its
substance has fully migrated to permanent homes (ARCH, skills,
INTENT, beads), the directory retires together. Context-maintenance
sweep handles the retirement.
