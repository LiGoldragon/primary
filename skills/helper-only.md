# Skill — helper-only

## Lead packet

When the psyche requests helper-only, subagent-only, main-thread no-reading, or
learning through helpers only, the lead keeps its own workspace reads to the
skill index and the generated brief. The lead packet contains:

- The exact psyche task.
- The harness and mode: Codex or Claude, explore or implement.
- Authority: read-only, report, or edit.
- The working directory, lane if known, and explicit source manifest.
- The return schema the helper must satisfy.

Generate the packet with `tools/helper-only-brief` whenever available. Do not
hand-write a broader brief from memory when the deterministic generator can
produce it.

## Helper packet

The helper receives the full reading envelope and does the meaningful reading.
Its packet names:

- Required startup reads: `AGENTS.md`, `skills/skills.nota`, and every skill
  triggered by the task.
- Allowed sources from the source manifest and any task-specific commands.
- Forbidden paths and actions.
- Dirty-state facts from `jj st`.
- The exact return schema.

The helper reports distilled findings, file locators, commands run, blockers,
and recommended next actions. If authority is edit, the helper edits directly
and reports the verification.

## Deterministic workflow

1. Lead runs `tools/helper-only-brief` with the exact task and authority.
2. Lead spawns the helper with the generated packet unchanged.
3. Helper performs the reading, command work, report writing, or edits.
4. Lead reads only the helper return and any explicitly named finished artifact
   needed to answer the psyche.
5. Lead asks the psyche only when the helper return exposes a real judgment
   fork, private scope, or missing authority.

## Forbidden actions

- Lead does not perform broad repo inspection, report triage, or multi-file
  context gathering.
- Lead does not inspect `private-repos/` or search `/nix/store`.
- Lead does not use raw `git`; version-control status and commits go through
  `jj` and the workspace `jj` skill.
- Helper does not exceed its authority. Read-only helpers never edit. Report
  helpers write only the named report lane. Edit helpers keep changes scoped to
  the packet.
- Neither lead nor helper infers durable psyche intent when the task is
  unclear; ask instead.

## Return

The helper return must include files read or changed, commands run, findings,
blockers, dirty-state changes, and the next concrete action. Chat carries only
the locator plus user-attention items when a report is written.
