# Skill — repository management

*How to create and maintain GitHub repositories from this workspace.*

---

## What this skill is for

Use this when a local repo needs a GitHub remote, when repository metadata needs
to be changed, or when the work needs basic GitHub issue/PR operations through
the `gh` CLI.

Repositories in this workspace are public by default. A private repository is
an exception that needs a concrete reason: secrets, private credentials,
personal data, unpublished third-party code, or another explicit confidentiality
constraint. Absent that reason, create the repository as public.

---

## Create a repository

From the repo root:

```sh
gh repo create LiGoldragon/<name> --public --source . --remote origin --push
```

If the local repo already has an `origin` remote, create the remote without
rewriting local config, then push with `jj`:

```sh
gh repo create LiGoldragon/<name> --public
jj git remote add origin git@github.com:LiGoldragon/<name>.git
jj git push --bookmark main
```

Private creation is explicit and rare:

```sh
gh repo create LiGoldragon/<name> --private --source . --remote origin --push
```

Only use `--private` when the reason is clear in the task or in the repository
contents.

---

## Change visibility and metadata

Make a repository public:

```sh
gh repo edit LiGoldragon/<name> --visibility public --accept-visibility-change-consequences
```

Make a repository private only with an explicit reason:

```sh
gh repo edit LiGoldragon/<name> --visibility private --accept-visibility-change-consequences
```

Set description and homepage:

```sh
gh repo edit LiGoldragon/<name> --description "Short description"
gh repo edit LiGoldragon/<name> --homepage "https://example.test"
```

Inspect current metadata:

```sh
gh repo view LiGoldragon/<name> --json nameWithOwner,visibility,url,description,homepageUrl
```

---

## Issues and pull requests

Create an issue:

```sh
gh issue create --repo LiGoldragon/<name> --title "Short title" --body "Actionable body"
```

List open issues:

```sh
gh issue list --repo LiGoldragon/<name> --state open
```

Create a draft PR:

```sh
gh pr create --repo LiGoldragon/<name> --draft --title "Short title" --body "What changed and why"
```

View PR checks:

```sh
gh pr checks --repo LiGoldragon/<name> <number>
```

Use the GitHub plugin skills for deep PR review or CI triage. This skill is the
minimal daily repository-management layer.

---

## Version-control boundary

Use `gh` for GitHub repository objects and metadata. Use `jj` for local history
and pushing bookmarks. Do not use raw `git` for ordinary commits or pushes; see
this workspace's `skills/jj.md`.

---

## See also

- this workspace's `skills/jj.md` — local history, commits, bookmarks, pushes.
- this workspace's `skills/autonomous-agent.md` — when routine repository
  obstacles are solved without asking.
