# Skill Editor Orchestration Doctrine

Task: revise intent-led orchestration and role doctrine for the AgentProtocolDesign weave.

BEADS: `primary-y0h6.6` - Revise intent-led orchestration and role doctrine.

## Status

Implemented locally. I claimed the task through orchestration as `skill-editor` over the bead, the intent-led orchestration source module, the role source directory, and this output file.

No commit or push was performed. The weave assigns final repository mechanics to the downstream Repo Operator task after validation and independent audit.

## Changed Files

In `/git/github.com/LiGoldragon/skills`:

- `modules/intent-led-orchestration/full.md`
  - States that the lead/orchestrator is a special intent-only session lane, not a generated spawned worker role.
  - Defines the lead context interface as psyche chat, psyche-pasted content, spawned agents, and returned agent output files.
  - Keeps source/domain reading, commands, edits, verification, commits, and pushes with spawned workers.
  - Adds the clarified workflow: locked alignment, Intent Translator default for nontrivial work, method approval, implementer handoff, distinct auditor for substantial work, evidence-backed success, psyche satisfaction authority, and concise final synthesis.
- `roles/intent-translator/full.md`
  - Expands the translator output to include implementation briefs, decision ownership, completion claims, path-preferred source context, evidence expectations, auditor recommendation, and remaining psyche decision points or blockers.
  - Makes the distinct-auditor recommendation explicit for substantial work.
  - Keeps lead orchestration outside the generated role packet set.
- `manifests/active-outputs.nota`
  - Updates the generated `intent-led-orchestration` skill description to name Intent Translator handoff, evidence-backed worker flow, and intent-only lead orchestration through agent outputs.
- `manifests/skills-roster.nota`
  - Mirrors the same description in the compatibility roster.

Generated in `/home/li/primary`:

- `.agents/skills/intent-led-orchestration/SKILL.md`
- `.claude/skills/intent-led-orchestration/SKILL.md`
- `skills/skills.nota`
- `.claude/agents/intent-translator.md`
- `.codex/agents/intent-translator.toml`
- `.pi/agents/intent-translator.md`

The generator refreshed all configured skill and role outputs; the doctrine-bearing changes are the files above.

## BEADS Status Changes

Claim command:

```sh
orchestrate "(Claim (skill-editor [(Task primary-y0h6.6) (Path /git/github.com/LiGoldragon/skills/modules/intent-led-orchestration/full.md) (Path /git/github.com/LiGoldragon/skills/roles) (Path /home/li/primary/agent-outputs/AgentProtocolDesign/SkillEditor-OrchestrationDoctrine.md)] [revise intent-led orchestration and role doctrine]))"
```

Result: accepted.

Close command:

```sh
bd close primary-y0h6.6 -r "Revised intent-led orchestration and Intent Translator doctrine to reflect intent-only lead, returned agent output files, default translator handoff, distinct auditor for substantial work, evidence-backed success, psyche satisfaction authority, and provisional audit/corpus learning. Regenerated primary skill/role outputs and passed generator check plus cargo test. Evidence: /home/li/primary/agent-outputs/AgentProtocolDesign/SkillEditor-OrchestrationDoctrine.md."
```

Result: closed.

Release command:

```sh
orchestrate "(Release skill-editor)"
```

Result: released the task and path claims.

## Generation And Checks

Run in `/git/github.com/LiGoldragon/skills`:

```sh
SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-generate.nota
SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota
cargo test
```

Results:

- `skills-generate.nota`: passed and refreshed primary generated outputs.
- `skills-check.nota`: passed with no generated drift.
- `cargo test`: passed; 12 integration tests passed.

Additional scoped checks:

- Searched for obsolete `tool-free`, `final returns from subagents`, and `Links in subagent returns` wording on the touched doctrine surfaces; no matches remained.
- Confirmed generated `intent-led-orchestration` surfaces include the intent-only lead, returned output files, Intent Translator handoff, distinct auditor default, evidence-backed success, psyche satisfaction authority, and final synthesis wording.
- Confirmed generated Intent Translator role packets include implementation briefs, path-preferred worker context, distinct auditor recommendation, provisional guideline/corpus observation framing, and no generic lead role.

## Remaining Doctrine Questions

No remaining doctrine question blocks the next bead. Runtime validation of Codex and Pi role discovery remains downstream validation work, not doctrine work.
