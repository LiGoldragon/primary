# Designer status — skills bootstrap

Date: 2026-05-06
Author: Claude (designer)

## Situation

- Skills system bootstrapped: three workspace skills under
  `skills/` (`autonomous-agent`, `skill-editor`,
  `stt-interpreter`); two repo skills (`criome/skills.md`,
  `sema/skills.md`) carrying the deepest-value claim.
- Lore project-decoupled: `AGENTS.md` rewritten; `INTENTION.md`
  removed (substance absorbed into `ESSENCE.md`); `gas-city/`
  content relocated to `gascity/engdocs/`; `lojix-cli/` content
  relocated to `lojix-cli/docs/`. Sema-ecosystem name-leakage in
  `programming/`, `rust/`, and `nix/` genericized.
- Orchestration protocol now formalizes role claims, exempts
  `reports/` from the claim flow with role subdirectories
  (`reports/designer/`, `reports/operator/`), and names the
  override mechanism for explicit one-job lock-bypass.
- Open beads:
  - `primary-bmy` (P2): per-repo `skills.md` rollout —
    incremental, agent-driven. Resolves over time.
  - `primary-jwi` (P3): harden the orchestrate helper into a
    typed Persona component (operator's).
  - Neither is mine to close in one shot.
- Coordination with operator (Codex) is working — parallel
  edits to lore and `skills/autonomous-agent.md` integrated via
  rebase + the operator's own merge of my work into theirs.

## Questions

1. Top-level reports (`1-gas-city-fiasco.md`,
   `2-primary-handoff.md`) predate role
   subdirectories. Stay at top level as workspace-historical, or
   move under a role? My instinct: leave at top level — they're
   not role-authored.
2. Does an abandoned repo (gascity, the `mentci-*` archives)
   get a `skills.md`? Or skip for retired projects with a
   one-line README pointer at most?
3. `ESSENCE.md` currently lives at `~/primary/` root. The
   content is already project-agnostic. Should it move into
   `lore/` (portable across workspaces) or stay coupled to this
   workspace? If it moves, lore becomes the canonical home for
   workspace intent; primary points at it.

## Suggestions

- **Prioritize `CriomOS-home/skills.md`** when an agent is
  next in that repo. `skills/stt-interpreter.md` already
  points at it for the speech-to-text tool's details — the
  forward reference is dead until CriomOS-home's skill lands.
- **Prune `primary-bmy`'s repo list.** A few entries
  (archived `mentci-*`, gascity-nix as a thin wrapper) probably
  don't earn a skill. The bead can be narrowed to active repos.
- **Revisit `lore/AGENTS.md` after the active sema-ecosystem
  skills are in.** Some rules currently in lore may fold into
  per-repo skills once those exist — the contract can shrink.

## Ideas

- **ESSENCE.md as a portable intent doc.** Any new workspace
  copies it at its root. Or: lore owns the canonical version
  and the workspace has a one-line shim. Either way, the doc
  itself is workspace-agnostic.
- **A "meta-skill" naming.** `skill-editor.md` is the de-facto
  canonical "how to edit anything in `skills/`," but the role
  isn't formally named. Worth flagging as the meta-skill so its
  role is explicit when more skills land.
- **The aski-lineage tension.** `aski/CLAUDE.md` formally
  disclaims aski as ancestor of nota/nexus ("coincidence, not
  lineage"); the lived sense is inspiration. ESSENCE.md
  sidesteps the question. When nota or nexus get their
  `skills.md`, that's the right place to either retire the
  disclaimer or formalize the lineage.

## End

Designer role is idle (`designer.lock` cleared via
`tools/orchestrate release designer`). No active scopes.
