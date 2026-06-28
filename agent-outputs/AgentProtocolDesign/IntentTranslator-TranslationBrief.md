# Intent Translator Translation Brief

Source: clarified psyche intent supplied in the AgentProtocolDesign session on 2026-06-28.

The BEADS graph was created as a V1 implementation weave for generated worker role packets and the agent output protocol. It uses one parent epic and nine child tasks. The first executable step is a read-only Scout map because the prompt explicitly leaves exact skills-generation repository location, generator tooling, and Claude/Codex/Pi harness target requirements to local discovery.

## Graph Summary

Parent epic:

- Generated worker role packets and agent output protocol V1 (`primary-y0h6`)

Dependency order:

1. Map skills-generation tooling and harness agent targets (`primary-y0h6.1`)
2. Add active Role/Skill manifest and module dependency index (`primary-y0h6.2`)
3. Add V1 role source modules and agent-output-protocol (`primary-y0h6.3`)
4. Implement role-packet generation, dependency expansion, and cleanup (`primary-y0h6.4`)
5. Emit physical role files for Claude, Codex, and Pi (`primary-y0h6.5`)
6. Revise intent-led orchestration and role doctrine (`primary-y0h6.6`)
7. Validate generated role outputs and cleanup behavior (`primary-y0h6.7`)
8. Independently audit role packet generator and doctrine (`primary-y0h6.8`)
9. Repo Operator commit and push role-packet V1 (`primary-y0h6.9`)

Blocking edges created:

- Scout map blocks manifest/index, role sources, generator implementation, harness outputs, and intent-doctrine revision.
- Manifest/index blocks role source activation and generator implementation.
- Role sources block generator implementation and intent-doctrine revision.
- Generator implementation blocks harness outputs.
- Harness outputs and intent-doctrine revision both block validation.
- Validation blocks independent audit.
- Independent audit blocks Repo Operator commit/push.

`bd dep cycles` returned no dependency cycles.

## BEADS Created

### Generated worker role packets and agent output protocol V1 (`primary-y0h6`)

Parent epic coordinating the full V1 implementation: current-state discovery, active manifest, sidecar dependency index, role source modules, shared `agent-output-protocol`, generator support, physical copied outputs for Claude/Codex/Pi, affirmative intent-layer doctrine, validation, independent audit, and Repo Operator handoff.

Completion claim: V1 role packets are generated from modular source through one active manifest, copied to all three harness discovery locations, validated, audited, and handed to Repo Operator with evidence-backed close notes.

### Map skills-generation tooling and harness agent targets (`primary-y0h6.1`)

Scout bead. It asks for a read-only Situational Map at `agent-outputs/AgentProtocolDesign/Scout-SituationalMap.md`, separating observed facts from interpretations. It exists because exact harness target paths and wrappers are intentionally not invented by the translator.

Completion claim: source/tooling surface and proven Claude/Codex/Pi locations are mapped, or exact unknowns are listed.

### Add active Role/Skill manifest and module dependency index (`primary-y0h6.2`)

Skill-system data bead. It captures the single active NOTA manifest with distinct `Role(...)` and `Skill(...)` records, plus a dependency-only sidecar module index.

Completion claim: manifest/index parse cleanly, express only active outputs, and carry dependency data structurally rather than in comments.

### Add V1 role source modules and agent-output-protocol (`primary-y0h6.3`)

Role-source bead. It covers the ten active V1 roles: Intent Translator, Scout, Repo Scaffolder, General Code Implementer, CriomOS Implementer, Rust Auditor, Nix Auditor, Skill Editor, Intent Maintainer, and Repo Operator. It also creates the shared `agent-output-protocol` source module and includes it in all spawned worker packets.

Completion claim: role main markdown files start with their role contracts, agent-output-protocol is shared, and corpus/audit learning is framed as provisional until psyche review.

### Implement role-packet generation, dependency expansion, and cleanup (`primary-y0h6.4`)

Generator bead. It covers reading `Role` and `Skill` manifest records, expanding ordered includes plus sidecar dependencies, dependency-before-dependent ordering, first-position deduplication by module id, omission of generated-file notices in runtime agent files, physical outputs, and cleanup of generator-owned inactive outputs.

Completion claim: generator behavior is implemented with tests/fixtures and preserves source files plus non-owned target files.

### Emit physical role files for Claude, Codex, and Pi (`primary-y0h6.5`)

Harness-output bead. It converts Scout-proven harness facts into physical copied role files in each harness-specific discovery location, with shared V1 body and only required wrapper/frontmatter/path differences.

Completion claim: all active V1 worker roles exist as physical copied files for Claude, Codex, and Pi, with no symlink dependency.

### Revise intent-led orchestration and role doctrine (`primary-y0h6.6`)

Intent-layer doctrine bead. It updates guidance so the lead/orchestrator is intent-only, nontrivial work defaults to Intent Translator after clarification, substantial work gets a distinct auditor, success is evidence-backed, psyche satisfaction remains authoritative, and auditor-proposed guidelines remain provisional before psyche review.

Completion claim: intent-layer and generated role guidance use affirmative commitment wording and no contradictory old doctrine remains on the touched surfaces.

### Validate generated role outputs and cleanup behavior (`primary-y0h6.7`)

Evidence bead. It requires generator checks, generated-output inventory/diff, a sample assembled role packet, cleanup proof, and implementation evidence written to `agent-outputs/AgentProtocolDesign/Implementer-Evidence.md` or equivalent.

Completion claim: checks demonstrate parser, expansion, copy, no-notice, and cleanup behavior across all three harnesses, or exact blockers are documented.

### Independently audit role packet generator and doctrine (`primary-y0h6.8`)

Audit bead. It enforces a separate auditor after validation. Audit focus includes generator code behavior, NOTA manifest/index shape, cleanup safety, physical harness outputs, role boundaries, affirmative wording, and evidence claims. It directs Rust Auditor, Nix Auditor, and Skill Editor expertise based on touched surfaces.

Completion claim: `agent-outputs/AgentProtocolDesign/Auditor-Report.md` separates findings from provisional observations and recommends fixes or approval from evidence.

### Repo Operator commit and push role-packet V1 (`primary-y0h6.9`)

Version-control bead. It starts only after audit. It hands final mechanics to Repo Operator under primary workspace `jj` rules.

Completion claim: whole working copy is committed, `main` bookmark is moved and pushed, and close notes point to commit plus validation/audit evidence.

## Grouping Rationale

The graph separates discovery, data model, source content, generator behavior, harness projection, workflow doctrine, validation, audit, and version-control mechanics because each has a distinct owner and success signal.

Scout is first because local target facts are deliberately unresolved by psyche intent. The translator created implementation-discovery work rather than guessing a skills-generation repo path or Pi/Claude/Codex wrapper format.

Manifest/index work comes before generator and role activation because the generator needs a stable structural contract: active outputs in one manifest, dependencies in one sidecar index.

Role source content and generator support are separate because Skill Editor owns source/generated content reconciliation, while General Code Implementer may need to change generator code. This preserves the generator-code boundary.

Harness output is after generator support because physical copied files and cleanup are generator behavior projected into target directories. Harness-specific body tuning is deliberately out of scope for V1.

Intent-led orchestration revision is parallel to harness output after role sources because it is doctrinal content, not path generation. It joins the graph at validation so generated role packets and orchestration guidance are checked together.

Validation precedes audit because auditors need evidence to review. Audit precedes Repo Operator because substantial work should not be committed/pushed as complete before independent review findings are resolved or explicitly deferred.

## Clarification Questions

No psyche clarification is required before implementation begins. The first bead is intentionally a Scout map for local facts that would otherwise be invented.

Implementation should stop for psyche clarification only if Scout discovery shows there is no existing skills-generation source surface and more than one plausible ownership model exists for where generated agent role sources should live.
