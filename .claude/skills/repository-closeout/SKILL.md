---
name: repository-closeout
description: 'Repository closeout for standalone agents: status, jj/Jujutsu commit and push, BEADS/beads closure, and final evidence reporting after validation.'
---

# repository publication

## Publication Rules

Use this when a code or engine repository lacks a remote, needs a public remote, or must make dependency pushes portable.

Code and engine repositories are public by default. Use a private repository only for secrets, credentials, personal data, unpublished third-party code, or an explicit confidentiality constraint.

Create the public GitHub repository from the local source when the repository does not already exist:

```sh
gh repo create LiGoldragon/<name> --public --source . --remote origin --push
```

When the forge repository exists but the local repository lacks `origin`, inspect the canonical remote and add it as remote configuration; raw Git is acceptable only for remote configuration.

```sh
gh repo view LiGoldragon/<name> --json nameWithOwner,visibility,sshUrl
git remote add origin git@github.com:LiGoldragon/<name>.git
```

Use Jujutsu for ordinary history and bookmark pushes after the remote exists.

A dependency is portable only when consumers point at a public owner/repo remote and the required branch or bookmark is pushed. Local path dependencies, unpublished producer branches, and missing remotes block portable closeout.

Do not change an existing private repository to public without explicit authorization.

## repository closeout

### Rules

Use repository closeout after implementation and validation evidence exist. Inspect local instructions and status first, preserve unrelated edits, and do not manufacture green evidence for missing checks.

Use `jj`/Jujutsu for normal version control. Every description-taking command uses an inline message. Before publishing, confirm bookmark reachability, repository status, and that no descriptionless authored commit is being pushed. Agent-authored commit messages include the acting model and thinking/provenance level in the message body when available.

After validation, commit and push implementation changes. Do not leave edited work uncommitted or unpushed. At closeout, release only resource claims made under your assigned lane, then unregister that lane. Do not release generic names or another worker's lane.

If the work creates or consumes a producer dependency, make that dependency portable before publishing. Surface stale dependency pins, unmerged producer branches, and dependencies that have unmerged branches when they affect integration, deployment, repurpose, or closeout. If portable closeout is not possible, report it as a hard blocker.

For primary-style direct main closeout:

```sh
jj status --no-pager
jj commit -m 'short imperative message'
jj bookmark set main -r @-
jj git push --bookmark main
```

Use BEADS/beads for tracked work that must survive the session or coordinate with other work. Close a bead only after acceptance criteria pass or the bead is invalidated; closing notes name durable evidence such as the commit, validation artifact, output file, or superseding task.

After pushing, verify status is clean or contains only named unrelated files. Report basis commit, bookmark, commands run, push result, and remaining blockers or disposition.
