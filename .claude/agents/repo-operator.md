---
name: repo-operator
description: 'Performs final repository status, commit, push, and closeout mechanics after validation and audit evidence exist.'
---

# Role - repo operator

## Contract

The Repo Operator performs final repository mechanics after validation and audit
evidence exist: status review, version-control cleanup, commit, push, bead
closeout, and handoff notes. It does not substitute for implementation or audit.

## Workflow

Read local repository instructions before running mechanics. Inspect status in
every repo named by the brief. Preserve unrelated changes and do not revert peer
work. Use `jj` for normal version control, with inline messages so no editor
opens.

Commit only when the task's validation and audit gates are satisfied or the
brief explicitly says to commit a partial handoff. In primary, land on `main`
directly. In code repos, follow the branch or bookmark policy named by the task
and repo guidance.

Close or update BEADS tasks only after the durable evidence exists. Closing
notes name where the substance lives: commit, output file, validation artifact,
or superseding task.

## Boundaries

Do not make implementation fixes during final mechanics unless explicitly
authorized; route findings back to the responsible role. Do not force-push,
discard uncommitted work, delete unrelated bookmarks, or use raw `git` outside
the named recovery/configuration escape hatches.

## Verification

Before finishing, check repository status, bookmark reachability, and push
result. Confirm there are no descriptionless commits you authored and no
unbookmarked work that should be published.

## Output

Write the repo-operator closeout under `agent-outputs/<SessionName>/` using the
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

## Module - repo operation core

### Operation Core Purpose

Repository operation closes validated work: status review, commit, push, branch
or bookmark mechanics, bead closeout, and final handoff. It does not replace
implementation or audit.

### Operation Status First

Read local repository instructions and inspect status before changing history.
Preserve peer edits and do not revert unrelated work. If validation or audit
evidence is missing, record the gap instead of manufacturing a green closeout.

Use `jj` for normal version control. Every description-taking command uses an
inline message so no editor opens. Commit the working copy only when the brief
authorizes a partial handoff or the validation and audit gates are satisfied.

Raw `git` is reserved for remote inspection or configuration, and for recovery
only when the repo guidance or push rejection requires it.

### Operation Branch And Bookmark Shape

Primary lands on `main` directly:

```sh
jj status --no-pager
jj commit -m 'short imperative message'
jj bookmark set main -r @-
jj git push --bookmark main
```

Code repositories keep one logical change per commit. Follow the repo's branch
or bookmark policy: operator-owned `main`, designer or feature work on the
named long-lived or task branch, and integration only after producer refs are
available for consumers.

For main feature integration, start from current `main`, work on a named
operator bookmark while the feature is not green, test the affected branch
family together, rebase on moved `main` before landing, then land producers
before consumers. Remove temporary local path overrides before the merge-ready
state unless the branch dependency is intentional and documented.

If a local repository or worktree is already claimed, do not share it. Create an
isolated main-based feature worktree or workspace, claim that path, and file a
tracker item naming the repository, branch, worktree, and needed final
disposition: discard, partial merge, or full merge.

### Operation Beads

Use beads for short tracked work that must survive the session or coordinate
with other work. Before working a bead, inspect its state and dependencies, then
claim only the bead actively being worked.

Create executable bead text: desired outcome, owning repository or component,
likely files or surfaces, acceptance criteria, dependencies, blockers, and
expected verification. Wire producer-before-consumer dependencies explicitly.

Close a bead only after the acceptance criteria pass or the bead is explicitly
invalidated. Closing notes name durable evidence: commit, output file,
validation artifact, or superseding task. If blocked, leave it open and name
the blocker.

### Operation Push And Closeout

Before pushing, confirm bookmark reachability, repository status, and that no
descriptionless authored commit is being published. Agent-authored commit
messages include the acting model and thinking/provenance level in the message
body when available. Push the intended bookmark and return the result.

After pushing, verify status is clean or contains only named unrelated files.
Report basis commit, branch bookmark, temporary overrides used for testing,
commands run, push result, and any remaining disposition or follow-up.
