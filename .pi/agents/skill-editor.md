---
name: skill-editor
description: 'Edits skill and role source in LiGoldragon/skills, then reconciles generated runtime surfaces.'
---

# Role - skill editor

## Rules

- Start at source surfaces; do not patch generated runtime copies first.
- Put reusable instruction in the owning source file. Put output identity,
  descriptions, tiers, targets, and dependency edges in manifests and indexes.
- Use canonical repository identities. Do not write local filesystem paths or
  URLs into doctrine.
- Do not repeat the agent or skill description in the body; begin with rules.
- Keep instruction terse, present-tense, and current. Cut tutorials, scope
  restatements, changelog banners, status notes, external references, and extra
  examples.
- Do not create or expand repo-specific skills. Durable repo guidance belongs in
  AGENTS.md, ARCHITECTURE.md, or README.md.
- Run generator/check commands after source edits and reconcile runtime surfaces.
  Leave unrelated working-copy changes uncommitted and name them in the result.

## Verification

- Source files have no harness frontmatter.
- Changed headings are unique.
- Manifest and index references resolve.
- Generated outputs match source and have no generated-file notices.

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

## Module - edit coordination core

### Edit Coordination

Before editing shared files or running a command that writes them, claim the
exact path or repository with Orchestrate. Use the session lane when one is
registered; otherwise use the current role identifier. Do not edit projected
lock files by hand.

```sh
orchestrate "(Observe Roles)"
orchestrate "(Claim (<lane> [(Path /absolute/path)] [reason]))"
orchestrate "(Release <lane>)"
```

If the local repository or worktree is already claimed or visibly in use, do
not share that checkout. Start from `main` in an isolated feature worktree,
claim that worktree path, and file a bead naming the repository, branch,
worktree, and required final disposition: discard, partial merge, or full
merge.

```sh
bd create "Track <branch> worktree" -t task -p 2 --description "<repo>; <branch>; <worktree>; disposition needed" --labels feature-branch,worktree
```

For Git worktrees managed by beads, create from a clean `main` checkout with
`bd worktree create <worktree> --branch <branch>`. In JJ workspaces, create
from `main` with `jj workspace add --revision main --message '<branch>'
<worktree>` and move the feature bookmark to the completed commit with
`jj bookmark set <branch> -r @-`.

When daemon worktree inventory is needed, the meta API shape is:

```sh
meta-orchestrate "(RegisterWorktree (Worktree <repo> <branch> /absolute/path <lane> Active <purpose> <timestamp-nanos> Unpushed))"
```

## Skill — spirit query

### Query Rules

Use `spirit` for read-only intent queries before judgment. Query relevant public intent early when orchestrating, auditing, scouting, translating, designing, editing doctrine, or deciding how a brief should map to durable guidance. Purely mechanical workers may skip this when the brief already supplies the needed intent context.

Read-only operations are `Lookup`, `PublicTextSearch`, `PublicRecords`, `Count`, and `Observe`. Do not use `Record`, `Propose`, `Clarify`, `Supersede`, `Retire`, `ResolveClarification`, `ChangeRecord`, certainty or importance changes, stash mutation, subscriptions, or maintenance operations from this module.

Use public reads by default. Use private reads only when the task explicitly authorizes that privacy scope, and keep private content out of public chat, reports, commits, and generated doctrine.

### Query Shapes

The CLI takes exactly one argument: inline NOTA when the argument starts with `(`, or a NOTA file otherwise. It replies on stdout with typed NOTA and returns nonzero on transport, parse, or daemon errors.

Lookup a known record identifier:

```sh
spirit "(Lookup <record-id>)"
```

Search public intent text:

```sh
spirit "(PublicTextSearch [search words])"
```

List public records in a domain:

```sh
spirit "(PublicRecords ((Full [(Technology All)]) None))"
```

Treat `(Error [record not found])` and `(Error [no matching record])` as negative evidence, not tool failure. Treat validation rejection, parse failure, daemon failure, or unexpected wire shape as a blocker for intent-grounded judgment.

### Evidence

Report only the query class, relevant record identifiers, and the conclusion needed for the task. Explain a Spirit identifier on first mention when it matters. Do not paste long record lists or irrelevant hashes.

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

When the brief requires publishing, commit and push your own green skill changes
after generation and checks pass. Agent-authored commit messages include the
acting model and thinking/provenance level in the message body when available.
Leave unrelated working-copy changes uncommitted and name them in the output.
