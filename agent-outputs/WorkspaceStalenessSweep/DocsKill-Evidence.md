# Docs Kill Evidence

Task: `primary-5rzf.6` docs/skills cleanup for the confirmed verifier ledger section `CONFIRMED FOR DOCS KILL (.6)`.

Scope: only D1-D14 from `agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`. `private-repos/` and Spirit intent records were not inspected or swept. The requested evidence path is this file; the bead body names `KillDocsSkills-Evidence.md`, but the dispatch supplied `DocsKill-Evidence.md`.

Consulted:

- `AGENTS.md`
- `agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md`
- `agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`
- `bd show primary-5rzf.6`
- `orchestrate "(Observe Roles)"`
- `orchestrate "(Claim (assistant [...paths...] [primary-5rzf.6 confirmed docs skills cleanup]))"`

## Changed Files

Manual docs edits:

- `ARCHITECTURE.md`
- `orchestrate/AGENTS.md`
- `orchestrate/ARCHITECTURE.md`
- `repos/spirit-guardian-config/INTENT.md`
- `repos/spirit-guardian-config/ARCHITECTURE.md`
- `.claude/worktrees/nota-codec-mockup-2/README.md`

Skill source and manifest edits:

- `repos/skills/modules/rust-crate-layout/full.md`
- `repos/skills/modules/operating-system-operations/full.md`
- `repos/skills/manifests/active-outputs.nota`
- `repos/skills/manifests/skills-roster.nota`
- `repos/skills/skills.md`

Generated reconciliation from skill source:

- `.agents/skills/rust-crate-layout/SKILL.md`
- `.claude/skills/rust-crate-layout/SKILL.md`
- `.agents/skills/operating-system-operations/SKILL.md`
- `.claude/skills/operating-system-operations/SKILL.md`

Observation: `nix run ./repos/skills#generate-skills -- /home/li/primary` rewrote the configured runtime output set. Primary `jj status --no-pager` also shows pre-existing or parallel working-copy changes outside this bead, including generated role/skill outputs, `primary.code-workspace`, and other `agent-outputs/WorkspaceStalenessSweep/*` files. Those were not manually edited for `.6` and were not reverted.

## Item Evidence

D1 `mind` replaced `persona-mind`: Replaced `persona-mind` identity prose with
`mind` / `mind-daemon` in `ARCHITECTURE.md`, `orchestrate/AGENTS.md`,
`repos/skills/modules/rust-crate-layout/full.md`, and generated
`rust-crate-layout` skill mirrors. `/home/li/primary/INTENT.md` is absent in
this checkout, so that locator had no editable surface.

D2 `signal-mind` replaced `signal-persona-mind`: Replaced BEADS target prose
with `signal-mind` in `orchestrate/AGENTS.md`.

D3 daemon-backed `orchestrate` replaced argv helper/crate: Removed stale
helper/crate names and old shell grammar examples from
`orchestrate/ARCHITECTURE.md` and `orchestrate/AGENTS.md`; retained current NOTA
invocation shape.

D4 typed worktree registry replaced `verify-jj`: Removed the old command name
from `orchestrate/AGENTS.md` and kept the `Observe Worktrees` / normal `jj`
guidance.

D5 session lanes replaced fixed role-named lanes: Removed fixed-role and
ordinal/qualifier retirement prose from `ARCHITECTURE.md` and
`orchestrate/AGENTS.md`; kept dynamic per-session lane guidance.

D6 topic labels replaced role-labeled beads: Rewrote the
`orchestrate/AGENTS.md` section to topic-label guidance without old `role:*`
label or discipline-pool wording.

D7 deployed `spirit` CLI replaced intent file append / `intent/*.nota`: Removed
file-append and legacy substrate wording from `orchestrate/AGENTS.md`; kept
deployed `spirit` CLI guidance.

D8 `lojix` / `meta-lojix` replaced deprecated `lojix-cli`: Removed deprecated
CLI mention from `repos/skills/modules/operating-system-operations/full.md`,
`repos/skills/manifests/active-outputs.nota`, and
`repos/skills/manifests/skills-roster.nota`; generated
`operating-system-operations` skill mirrors were reconciled.

D9 logged-fold migration replaced copy-everything migration binaries: Removed
retired binary names and copy-everything framing from
`repos/spirit-guardian-config/INTENT.md`; kept `spirit-migrate-store` as the one
entry point.

D10 `SubscribeIntent` and `Untap` replaced old `Watch` / `Unwatch` coverage:
Removed old watch/unwatch names from
`repos/spirit-guardian-config/ARCHITECTURE.md`; kept current subscription and
token-cancellation wording.

D11 generated Signal/Nexus/SEMA triad replaced old `persona-spirit` actor tree:
Removed old actor-tree wording from
`repos/spirit-guardian-config/ARCHITECTURE.md`; kept generated flow statement.

D12 owner-only `CollectRemovalCandidates` replaced old working-signal deletion
path: Removed old component provenance wording from
`repos/spirit-guardian-config/ARCHITECTURE.md`; kept owner-only meta operation
and archive database shape.

D13 typed NOTA codec replaced previous serde-based path: Removed stale
replacement sentence from `.claude/worktrees/nota-codec-mockup-2/README.md`.

D14 first-class skill targets replaced command/prompt invocation extras: Removed
command/prompt extras sentence from `repos/skills/skills.md`; kept `AgentsSkill`
and `ClaudeSkill` target guidance.

## Checks

Passed:

- `nix run ./repos/skills#generate-skills -- /home/li/primary`
- `nix run ./repos/skills#check-skills -- /home/li/primary`
- `nix flake check ./repos/skills`
- Scoped stale-term `rg` checks for D1-D14 against the confirmed locator files: no matches.
- Source-frontmatter check on edited skill modules: no harness frontmatter found.
- Duplicate-heading check on edited markdown files: no duplicates found.
- Generated-notice check on touched generated skill mirrors: no generated-file notices found.
- `jj status --no-pager` in `repos/skills`: only the five intended source/manifest files are modified.

Working-copy notes:

- Primary `jj status --no-pager` remains dirty with unrelated or parallel changes outside this bead. I did not commit, push, revert, or alter those changes.
- A broad docs scan found `persona-spirit` in primary `ARCHITECTURE.md`, but that locator is not in D11 or D12. It was intentionally left untouched to stay inside the verifier ledger boundary.
- `orchestrate "(Release assistant)"` acknowledged additional `assistant` claims beyond the paths claimed for this bead, apparently from parallel workspace work using the same lane name. A follow-up `orchestrate "(Observe Roles)"` shows `assistant` has no active claims.

## Closeout

`primary-5rzf.6` is ready to close after this evidence file is recorded. Remaining closeout and commit/push work belongs to `primary-5rzf.9` per the bead graph.
