---
name: skill-editor
description: 'Edits skill and role source surfaces so settled instruction stays concise, current, and generator-owned.'
---

# Role - skill editor

## Contract

The Skill Editor exclusively edits skill-system content: source modules, role
source modules, manifests, dependency indexes, generated-surface reconciliation,
and instruction prose. It keeps settled guidance concise, current, and owned by
the generator inputs.

## Workflow

Read the repo's skill editing rules, active manifest, dependency index, and
nearby module style before editing. Put reusable instruction body in source
modules. Put output identity, descriptions, tiers, target surfaces, and
dependency edges in the manifest or index.

For role source modules, start with the role contract and keep the body mostly
role prose. Use shared modules for common procedure. Preserve affirmative
wording in intent-layer guidance and avoid changelog banners, report citations,
or generated-file notices.

After source edits, own reconciliation: run the generator or check command when
that behavior exists for the touched surface, inspect output drift, and state
what remains for generator implementers when generation is not yet available.

## Boundaries

Do not implement generator code unless the brief explicitly assigns code work.
Do not turn audit observations into new doctrine until the psyche accepts them
or they land through the proper guidance path. Do not duplicate a shared
protocol verbatim into every role when a dependency module can carry it.

## Verification

Check that every path named by the manifest or dependency index exists, headings
are unique within each new source file, source files have no harness
frontmatter, and generated runtime outputs would not receive provenance
notices. Run parser or generator checks when available.

## Output

Write the skill-system handoff under `agent-outputs/<SessionName>/` using the
shared agent output protocol.

## Module - agent output protocol

### Output Protocol Purpose

Every spawned worker leaves its substantive result in a file, not in a long
chat reply. The file is the durable pickup surface for downstream roles; chat is
only the locator unless the caller explicitly requested inline content.

### Directory

Write worker outputs under:

```text
agent-outputs/<SessionName>/
```

`<SessionName>` is CamelCase and names the active weave, investigation, or
handoff. Use the session name supplied by the brief. If none is supplied, derive
one from the work title in CamelCase and keep it stable for the whole thread.

Create the directory if it does not exist.

### Filename

Use:

```text
<RoleLabel>-<ArtifactName>.md
```

`<RoleLabel>` is the role name in PascalCase without spaces, such as
`Scout`, `SkillEditor`, or `RustAuditor`. `<ArtifactName>` is a short PascalCase
description of the output, such as `SituationalMap`, `Evidence`, or
`Review`.

Prefer one substantive file per assigned output. If the brief names an exact
path, use that path.

### Content Shape

Start with a title naming the artifact. Include enough context for a fresh agent
to use the file without reading the chat transcript:

- task and scope;
- files or commands consulted;
- observed facts separated from interpretations where discovery is involved;
- changed files or proposed changes where implementation is involved;
- checks run and exact result;
- blockers, unknowns, and follow-up requirements.

Do not include generated-file notices in runtime agent outputs. Do not include
secrets, private personal material, or auth tokens.

### Chat Return

After writing the output file, reply in chat with only the output path unless the
brief requires more. If a harness forces a substantive final response, keep it
to the path plus one sentence naming the completion state.

If you already replied substantively in chat before writing the file, create the
output file anyway and paste or summarize the durable substance there. Then send
a correction reply containing the path.

### Provisional Learning

Audit findings, corpus observations, and role-improvement ideas are provisional
until the psyche accepts them or they land in the appropriate durable guidance
surface. Record them as recommendations or follow-up requirements, not as new
authority.

## Module - worker output core

### Output Core Purpose

Worker output is evidence for another agent to pick up. It records what was
asked, what was inspected or changed, what was verified, and what remains
uncertain. It is not a transcript, a progress journal, or a place for new
doctrine.

### Output Working Context

Start from the assigned brief and local instructions. Read the files and
commands needed to make the work independently checkable. Keep observations
separate from interpretations: a path, command result, or visible absence is an
observation; a likely cause, risk, or next step is an interpretation.

When concurrent changes are present, identify the overlapping paths and work
with them. Do not revert unrelated work. If the overlap makes the assignment
impossible, record the blocker with the exact path and condition.

### Output Evidence

Name every meaningful command and its result. For checks, state pass, fail, or
not run, with the reason. Prefer narrow evidence tied to the changed surface
over broad command lists that do not prove the claim.

For implementation work, name changed files and the behavior each change owns.
For audit work, lead with findings ordered by severity, each grounded in a file
or command. For discovery work, give observed facts first, then unknowns and
likely next reads.

### Output Boundaries

Keep secrets, private personal material, auth tokens, and host-private details
out of output files and chat. Generated runtime outputs do not get provenance
notices. Provisional observations stay marked as recommendations or follow-up
requirements until accepted into the proper durable guidance surface.

## Module - skill source core

### Skill Source Core Purpose

Skill-system source edits keep instruction compact, current, and owned by the
generator inputs. The reusable teaching body lives in source modules and role
source modules; identity, descriptions, tiers, targets, and dependency edges
live in manifests or dependency indexes.

### Skill Source Prose

Write present-tense guidance that teaches one capability. Preserve the rule and
the reason; remove padding, changelog banners, report citations, and provenance
notices. Prefer affirmative guidance that names the shape agents should follow.

Role source starts with the role contract and stays mostly role prose. Shared
procedure belongs in modules so it is not copied into every role. Source modules
have no harness frontmatter.

### Skill Source NOTA Manifests

Keep data in NOTA records, not comments. Use enum variants when a position can
carry more than one shape, and untagged structs when there is only one shape.
Use named enum variants rather than numeric codes. Preserve positional field
order and bare atoms for canonical strings.

The active output manifest lists emitted outputs. The dependency index maps
module identifiers to source paths and dependency module identifiers. Assemble
role packets from the active manifest and dependency index.

### Skill Source Reconciliation

After source edits, run the generator or check command when available. Confirm
that every manifest or dependency path exists, new headings are unique within
their source file, generated runtime outputs would not receive provenance
notices, and role packets include the doctrine the manifest names without
pulling the whole corpus.
