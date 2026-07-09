---
name: repository-management
description: 'Minimal ghq and gh discipline for local clone discovery, repository metadata, issue/PR operations, and deciding when a new repository is justified.'
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

## repository management

### Rules

Use this for GitHub repository objects, metadata, issue or PR operations, and local clone discovery through `ghq`.

Use `ghq` to fetch and discover local clones. Do not hand-create clone directories or rely on filesystem searches as the repo index. Preserve the canonical owner/repo casing reported by the forge.

Examples use canonical identities, not local paths:

```sh
ghq get github.com/<owner>/<repo>
ghq get --update github.com/<owner>/<repo>
ghq list
ghq look <substring>
```

Use `gh` for forge-side objects and metadata:

```sh
gh repo view LiGoldragon/<name> --json nameWithOwner,visibility,description,homepageUrl
gh issue list --repo LiGoldragon/<name> --state open
gh pr checks --repo LiGoldragon/<name> <number>
```

Use Jujutsu for local history and bookmark pushes. Do not use raw Git for ordinary commits or pushes.

### New repositories

Create a new repository only for a genuinely new project or concern. Major rewrites, experiments, mockups, fixtures, reproductions, and alternate versions of an existing project belong on branches or tracked work items in the existing repository.

Before creating or repurposing a repository, surface unmerged branches, stale dependencies, and dependencies with unmerged branches that affect the decision.

When unsure whether a name should become a repository, ask before creating the repo.
