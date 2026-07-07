---
name: repository-closeout
description: 'Performs final repository status, commit, push, and closeout mechanics after validation and audit evidence exist.'
---

# repository closeout

## Contract

The Repository Closeout role performs final repository mechanics after validation and audit
evidence exist: status review, version-control cleanup, commit, push, work-item
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

Close or update work-tracking items only after the durable evidence exists. Closing
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

Return the repository-closeout result in chat or the harness-required worker
output. Write an output artifact only when the brief requests a downstream
pickup file; then use the requested path or the opt-in artifact naming protocol.

## edit coordination core

### Edit Coordination

Before editing shared files or running a command that writes them, register the assigned Session/Lane with `meta-orchestrate`, then claim the exact path or repository with ordinary Orchestrate under that lane. The ordinary claim field is role-shaped, but it carries the lane identity.

If the task needs editing and no session name, lane name, or Fresh/Recovery mode is assigned, pause and report the missing coordination identity. Do not use generic names such as `general-code-implementer`, `skill-editor`, or `rust-auditor`.

Lane registration is the atomic check. Do not pre-observe before registration. Treat Fresh duplicate registration as a conflict/blocker. Treat orchestrator-declared Recovery duplicate as inherited only when the active lane clearly matches this recovery context.

Do not edit projected lock files by hand.

```sh
meta-orchestrate "(Register ((<SessionName> <LaneName> ([<RoleToken>...] Structural) <details>) Fresh))"
orchestrate "(Claim (<LaneName> [(Path /absolute/path)] <reason>))"
orchestrate "(Release <LaneName>)"
meta-orchestrate "(Unregister (<SessionName> <LaneName> <details>))"
```

Observe only when coordination state is evidence after registration or during audit:

```sh
orchestrate "(Observe Sessions)"
orchestrate "(Observe Lanes)"
orchestrate "(Observe (SessionLanes <SessionName>))"
```

If the local repository or worktree is already claimed or visibly in use, do not share that checkout. Start from `main` in an isolated feature worktree, claim that worktree path under the registered lane, and file a bead naming the repository, branch, worktree, and required final disposition: discard, partial merge, or full merge.

```sh
bd create "Track <branch> worktree" -t task -p 2 --description "<repo>; <branch>; <worktree>; disposition needed" --labels feature-branch,worktree
```

For Git worktrees managed by beads, create from a clean `main` checkout with `bd worktree create <worktree> --branch <branch>`. In JJ workspaces, create from `main` with `jj workspace add --revision main --message '<branch>' <worktree>` and move the feature bookmark to the completed commit with `jj bookmark set <branch> -r @-`.

When daemon worktree inventory is needed, the meta API shape is:

```sh
meta-orchestrate "(RegisterWorktree (Worktree <repo> <branch> /absolute/path <lane> Active <purpose> <timestamp-nanos> Unpushed))"
```


### Editing Closeout

An editing-capable agent that changes workspace files commits and pushes those changes before final output. This is unconditional.

A prompt cannot turn file-editing work into uncommitted work. If the desired result must remain uncommitted or unpushed, do not edit files; ask for a non-editing assignment or report the blocker.

The assigned worker output file alone does not make a read-only role editing-capable. Once a role changes source, configuration, documentation, generated, tracker, or other workspace files, it owns verification evidence, commit creation, push, and status reporting for those changes.

Preserve peer edits. Commit only agent-authored changes when repo doctrine permits scoped commits; when repo doctrine requires whole-working-copy commits, name unrelated changes included in the closeout.

At closeout, release only resource claims made under your assigned lane, then unregister that lane. Clear or end a session only when orchestration owns session cleanup or all remaining lanes are yours. Do not release generic names or another worker's lane.

Agent-authored commit messages include the acting model and thinking/provenance level when the harness or role packet supplies them.

## repo operation core

### Operation Core Purpose

Repository operation closes validated work: status review, commit, push, branch
or bookmark mechanics, bead closeout, and final handoff. It does not replace
implementation or audit.

### Operation Status First

Read local repository instructions and inspect status before changing history.
Preserve peer edits and do not revert unrelated work. If validation or audit
evidence is missing, record the gap instead of manufacturing a green closeout.

Use `jj` for normal version control. Every description-taking command uses an
inline message so no editor opens. Commit the working copy when the brief
authorizes a partial handoff or the validation and audit gates are satisfied.
For file edits made by the current agent, the editing closeout rule still
requires commit and push before final output; missing validation is evidence to
report, not permission to leave edits unpublished.

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
or bookmark policy: integration-owned `main`, design or feature work on the
named long-lived or task branch, and integration only after producer refs are
available for consumers.

For main feature integration, start from current `main`, work on a named
integration bookmark while the feature is not green, test the affected branch
family together, rebase on moved `main` before landing, then land producers
before consumers. Remove temporary local path overrides before the merge-ready
state unless the branch dependency is intentional and documented.
If the work creates or consumes a producer dependency, make that dependency
portable before publishing. If portable closeout is not possible, report it as a
hard blocker.

If a local repository or worktree is already claimed, do not share it. Create an
isolated main-based feature worktree or workspace, claim that path, and file a
tracker item naming the repository, branch, worktree, and needed final
disposition: discard, partial merge, or full merge.

### Operation Work Tracking

Use tracked work items when work must survive the session or coordinate
with other work. Before working an item, inspect its state and dependencies, then
claim only the item actively being worked.

Create executable item text: desired outcome, owning repository or component,
likely files or surfaces, acceptance criteria, dependencies, blockers, and
expected verification. Wire producer-before-consumer dependencies explicitly.

Close an item only after the acceptance criteria pass or the item is explicitly
invalidated. Closing notes name durable evidence: commit, output file,
validation artifact, or superseding task. If blocked, leave it open and name
the blocker.

### Operation Push And Closeout

Before pushing, confirm bookmark reachability, repository status, and that no
descriptionless authored commit is being published. Push the intended bookmark
and return the result.

After pushing, verify status is clean or contains only named unrelated files.
Report basis commit, branch bookmark, temporary overrides used for testing,
commands run, push result, and any remaining disposition or follow-up.
