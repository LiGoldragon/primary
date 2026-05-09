# Skill — repository management

*How to create and maintain GitHub repositories from this workspace.*

---

## What this skill is for

Use this when a local repo needs a GitHub remote, when repository metadata needs
to be changed, when the work needs basic GitHub issue/PR operations through the
`gh` CLI, or when finding / fetching / updating local clones via `ghq`.

Repositories in this workspace are public by default. A private repository is
an exception that needs a concrete reason: secrets, private credentials,
personal data, unpublished third-party code, or another explicit confidentiality
constraint. Absent that reason, create the repository as public.

---

## Where repositories live — the ghq layout

**Every local clone lives at `/git/<host>/<owner>/<repo>`.**
`ghq` is the canonical fetcher and indexer; `~/git/` is retired
(the migration finished 2026-05-09; see the closing note on
BEADS `primary-77l`).

```
/git/
├── github.com/
│   ├── LiGoldragon/<repo>     ← canonical case (matches GitHub's user.login)
│   ├── Criome/<repo>          ← canonical case (Criome org)
│   ├── nix-community/<repo>
│   ├── rkyv/<repo>
│   ├── … (every other owner you've ever cloned from)
├── codeberg.org/<owner>/<repo>
├── gitlab.com/<owner>/<repo>
├── git.sr.ht/~<owner>/<repo>
└── …
```

The workspace's `~/primary/repos/` directory holds symlinks
into this tree — `~/primary/repos/<repo>` → `/git/<host>/<owner>/<repo>`.
Symlinks are gitignored; they're a local index, regenerated
from the filesystem.

### Cloning a new repo — `ghq get`

Fetch a remote into the canonical location with one command:

```sh
ghq get https://github.com/<owner>/<repo>
ghq get -p https://github.com/<owner>/<repo>     # use SSH (preferred for own repos)
ghq get --update github.com/<owner>/<repo>       # update if already cloned
```

`ghq` derives the destination from the URL. Don't manually
create directories under `/git/...` — let `ghq` do it. The
case in the URL determines the case on disk; **use the
canonical case from GitHub's API** (`gh api users/<name> | jq .login`)
or the org's about page. `LiGoldragon` not `ligoldragon`;
`Criome` not `criome`.

### Finding a local clone — `ghq list` + `ghq look`

```sh
ghq list                              # every clone, full host/owner/repo path
ghq list | grep nota                  # find by substring
ghq list -p                           # print full filesystem paths
ghq look <substring>                  # cd into a matching clone (interactive shell)
```

`ghq list` is the source-of-truth for "what repos do I have
locally" — faster than `find /git/`, and only shows actual
git checkouts (not stray subdirs).

### Updating clones in bulk

```sh
ghq get --update --shallow github.com/<owner>/<repo>     # one
ghq list | xargs -I{} ghq get --update {}                # all (slow; use sparingly)
```

For per-repo updates, prefer `jj git fetch` inside the
checkout — it integrates with the workspace's jj discipline
(`skills/jj.md`). `ghq get --update` is for bulk passes.

### Don't deviate from the layout

| Don't | Do |
|---|---|
| Clone into `~/git/` (retired) | `ghq get <url>` (lands in `/git/<host>/<owner>/<repo>`) |
| Use `git clone` directly | `ghq get` (preserves the layout) |
| Lowercase a path that GitHub canonicalises as mixed-case | Match GitHub's casing exactly |
| Delete a clone with `rm -rf` then re-clone elsewhere | `ghq get --update` to refresh in place |
| Move a clone manually | `ghq get` it again at the right location, then delete the wrong one |

If the layout drifts (case mismatch, wrong location, manual
clones), the fix is mechanical — `git remote set-url origin
<canonical-url>`, `mv` to the canonical path, update any
`primary/repos/` symlinks. The `primary-77l` closing note has
the worked example for the recent ~/git → /git migration.

### Adding to ghq's index after a manual clone

If you somehow ended up with a checkout outside `/git/`:

```sh
mv <wrong-path> /git/<host>/<owner>/<repo>
# verify ghq sees it
ghq list | grep <repo>
```

`ghq` indexes the filesystem on each `list`; no separate
"add to index" step.

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
