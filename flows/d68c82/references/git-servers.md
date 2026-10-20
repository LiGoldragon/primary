# Self-hosted Git server on the NixOS cluster: comparison

Research date: 2026-10-16. Asked for by the psyche's order (flows/d68c82/vision/git.md):
one node with the Git-server role from cluster data, access from the SSH public keys
already in cluster data, simple, push-mirroring every repository to GitHub as backup.

Evidence notes. NixOS module facts were read from the nixpkgs `master` source files
(raw.githubusercontent.com) on 2026-10-16. github.com itself, api.github.com and
githubstatus.com could not be reached from this host (see the last section), so GitHub
star counts and GitHub-hosted release pages were not read; release versions come from the
Go module proxy, Codeberg's API or project sites instead. RAM figures are marked
"official" only where the project states them; others are marked as unverified estimates.

## One fact that applies to every option

GitHub does not create a repository on push. Every option below needs the GitHub
repository to exist first (created by `gh repo create` or the GitHub REST API), and a
credential that can write to it: a fine-grained personal access token with Contents
write (plus Workflows if the repo has `.github/workflows`), or an SSH key. A GitHub deploy
key is per repository; one SSH key for many repositories means a machine-user account
key. Sources: Forgejo mirror docs and Gitea mirror docs below both state this.

## Soft Serve (Charm)

- Stack: Go, single binary. SSH, HTTP and git:// servers in-process; TUI over SSH.
  Database: SQLite by default, PostgreSQL optional. Git LFS built in.
  https://github.com/charmbracelet/soft-serve (README read via
  https://raw.githubusercontent.com/charmbracelet/soft-serve/main/README.md)
- RAM: not stated by the project. Unverified estimate: tens of MB at small scale.
- Users and keys: `initial_admin_keys` in `config.yaml` (or
  `SOFT_SERVE_INITIAL_ADMIN_KEYS`) creates an `admin` user with those keys; every key
  listed there is an admin. Non-admin users and their keys are added at runtime over SSH
  (`ssh host user create NAME`, `user add-pubkey NAME KEY`) and stored in the database.
  So: declarable from Nix only if every cluster key is an admin key; per-user
  declarations need an activation script calling the SSH admin commands. Repos are
  created on `git push`.
- GitHub mirror: built-in mirroring is pull only (`repo import --mirror`, job
  `mirror_pull: "@every 10m"`). No push mirror. Push to GitHub must be a server-side
  hook: Soft Serve runs `pre-receive`, `update`, `post-update`, `post-receive`, per repo
  or global in `$SOFT_SERVE_DATA_PATH/hooks`. It also has HTTP webhooks per repo.
  Auth to GitHub is whatever the hook uses (an SSH key or token readable by the service).
- NixOS: `services.soft-serve` with `enable`, `package`, `settings` (free-form YAML).
  Runs with `DynamicUser`, state in `/var/lib/soft-serve`; the module adds `ExecPaths`
  for repos so hooks can run. No option for global hooks or keys beyond `settings`.
  Maintainer: `dadada`.
  https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/misc/soft-serve.nix
- Steward, licence, activity: Charm (charmbracelet), MIT. Latest v0.12.3, 2026-10-05
  (https://proxy.golang.org/github.com/charmbracelet/soft-serve/@latest). Still 0.x.
- Reliability record: a long advisory list, including two authentication bypasses
  (GHSA-mc97-99j4-vm2v, 2023; GHSA-pchf-49fh-w34r, 2026-01), arbitrary code execution via
  LFS (GHSA-m445-w3xr-vp2f, 2024), path traversal (GHSA-j4jw-m6xr-fv6c, 2025), arbitrary
  file write via SSH API (GHSA-33pr-m977-5w97, 2025), SSRF (GHSA-vwq2-jx9q-9h9f,
  GHSA-3fvx-xrxq-8jvv), private repo clone via import (GHSA-xgxp-f695-6vrp, 2026-03).
  Source: OSV query for Go package github.com/charmbracelet/soft-serve,
  https://api.osv.dev/v1/query
- Web UI: none (SSH TUI only). No pull requests, no CI.

## gitolite

- Stack: Perl plus sh, git and OpenSSH. No daemon, no database; authorization layer that
  sits in `~git/.ssh/authorized_keys` forced commands. Requirements: "any unix system,
  sh, git 1.6.6 or later, perl 5.8.8 or later, openssh 5.0 or later".
  https://raw.githubusercontent.com/sitaramc/gitolite/master/README.markdown
- RAM: no resident process; only per-SSH-connection Perl. Unverified: a few MB per
  connection.
- Users and keys: normally via the `gitolite-admin` repo (`keydir/NAME.pub`,
  `conf/gitolite.conf`). There is an official on-server mode without the admin repo:
  `gitolite setup -a dummy`, then keys in `~/.gitolite/keydir`, rules in
  `~/.gitolite/conf/gitolite.conf`, then `gitolite compile; gitolite trigger
  POST_COMPILE`. That mode can be driven fully from Nix by an activation script writing
  keydir and conf from cluster data. Wild repos (`C` permission) allow create-on-push.
  https://gitolite.com/gitolite/odds-and-ends.html (section "administering gitolite
  directly on the server")
- GitHub mirror: gitolite's own mirroring is gitolite-to-gitolite only (master does
  `git push --mirror` to copies; copies must answer gitolite's `hello`).
  https://gitolite.com/gitolite/mirroring.html . To GitHub: a common `post-receive`
  hook running `git push --mirror`; auth by the git user's SSH key or a token.
- NixOS: `services.gitolite` with `enable`, `dataDir`, `adminPubkey` ("will only be used
  once, upon the first initialization"), `enableGitAnnex`, `commonHooks` (list of hook
  paths copied to `~/.gitolite/hooks/common`), `extraGitoliteRc`, `user`, `group`,
  `description`. `commonHooks` is the declared place for a GitHub-mirror hook. No
  `meta.maintainers` in the file.
  https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/misc/gitolite.nix
- Steward, licence, activity: Sitaram Chamarty, GPLv2. Moved primary hosting to Codeberg
  (commit "change URLs to use codeberg instead of github", 2026-08-09). Latest tag
  v3.6.15 (2026-08-08); previous v3.6.14 (2025-07-18), v3.6.13 (2023-07-14). Last commit
  2026-09-29. Single-maintainer, slow, stable.
  https://codeberg.org/sitaramc/gitolite , https://gitolite.com/gitolite/index.html
- Reliability: mature (v3 since 2012); no advisory list was searched for it in this
  pass.
- Web UI, PRs, CI: none; pair with cgit or gitweb for browsing.

## Plain git over SSH (git-shell) plus cgit or gitweb

- Stack: git and OpenSSH only. `git-shell` is "a login shell for SSH accounts to provide
  restricted Git access. It permits execution only of server-side Git commands
  implementing the pull/push functionality, plus custom commands present in a
  subdirectory named `git-shell-commands`". No database, no daemon.
  https://git-scm.com/docs/git-shell
- RAM: none resident beyond sshd; cgit is a CGI under nginx/fcgiwrap (C).
- Users and keys: one Unix user (`git`), `users.users.git.openssh.authorizedKeys.keys`
  set from the cluster's key list; shell `git-shell`. Entirely native NixOS, no app
  state. Limits: every key gets the same access to every repo (no per-user ACL, no
  per-user identity in logs beyond the key fingerprint sshd logs). Repos are not created
  on push; create them by a declared list (activation script `git init --bare`) or a
  `git-shell-commands/create` script.
- GitHub mirror: a `post-receive` hook doing `git push --mirror github` (backgrounded so
  the user's push does not wait), plus a systemd timer that retries all repos. A single
  hook for all repos can be set system-wide with `core.hooksPath` in `/etc/gitconfig`
  (NixOS `programs.git.config`); see https://git-scm.com/docs/githooks and
  https://git-scm.com/docs/git-config#Documentation/git-config.txt-corehooksPath .
- NixOS: no git-server module needed (users, openssh, programs.git). Web view:
  `services.cgit.<name>` with `enable`, `nginx.virtualHost`, `nginx.location`, `repos`,
  `scanPath`, `settings`, `extraConfig`, `user`, `group`.
  https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/networking/cgit.nix
  gitweb also exists as `services.gitweb` (not inspected in this pass).
- Steward, licence: git is GPLv2 (git project). cgit: C, GPLv2, Jason A. Donenfeld,
  "A hyperfast web frontend for git repositories written in C"; last commits 2026-09-18.
  https://git.zx2c4.com/cgit/about/ , https://git.zx2c4.com/cgit/log/
- Web UI: cgit/gitweb read-only browsing. No PRs, no CI.

## Forgejo

- Stack: Go single binary (Gitea soft fork), web app plus built-in or host SSH. Database
  required: SQLite, PostgreSQL 14+, MySQL 8.4+, MariaDB 10.6+ ("No maintenance is
  expected by using SQLite"). https://forgejo.org/docs/latest/admin/database-preparation/
- RAM: Forgejo does not state one; Gitea (same codebase origin) states "2 CPU cores and
  1GB RAM is typically sufficient for small teams/projects" and "A Raspberry Pi 3 is
  powerful enough". https://docs.gitea.com/ . Unverified estimate of idle RSS: ~150-300 MB.
- Users and keys: no CLI to add an SSH key. `forgejo admin user create` exists (CLI);
  keys via API `POST /admin/users/{username}/keys`, removal `DELETE
  /admin/users/{username}/keys/{id}`. So declarative keys need a Nix oneshot that
  reconciles users and keys over the API with an admin token. The web install wizard can
  be skipped (NixOS `useWizard = false` default).
  https://forgejo.org/docs/latest/admin/command-line/ ; API: https://codeberg.org/swagger.v1.json
- GitHub mirror: built in, per repository. "Sync when new commits are pushed" for GitHub
  targets plus an optional periodic sync. Pushes are forced (`git push --mirror` when no
  branch filter). Auth: GitHub username plus fine-grained token, or "Use SSH
  authentication" where Forgejo generates an Ed25519 key per mirror to be added as a
  GitHub deploy key (choosable only at creation; LFS not mirrored over SSH). API: `POST
  /repos/{owner}/{repo}/push_mirrors` with `remote_address`, `remote_username`,
  `remote_password`, `sync_on_commit`, `interval`, `branch_filter`, `use_ssh`. There is
  no instance-wide "mirror every repo" setting; each new repo needs a mirror created
  (by the reconciler or a webhook).
  https://forgejo.org/docs/latest/user/repo-mirror/
- NixOS: `services.forgejo`, maintained by `lib.teams.forgejo`, with a manual chapter.
  Options include `package` (default `forgejo-lts`), `useWizard`, `stateDir`,
  `customDir`, `user`, `group`, `database.{type,host,port,name,user,passwordFile,socket,
  path,createDatabase}`, `dump.{enable,interval,backupDir,type,file,age}`,
  `lfs.{enable,contentDir}`, `repositoryRoot`, `settings` (app.ini), `secrets`. Mature.
  https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/misc/forgejo.nix
  and forgejo.md beside it.
- Steward, licence, activity: non-profit governance with Codeberg e.V. as custodian
  since the 2022-12-15 founding (fork in response to Gitea Ltd's formation);
  GPLv3-or-later from v9.0 (earlier MIT). Latest stable v17.0.0 (2026-10-15), LTS
  v15.0.10 (2026-10-12), majors roughly quarterly. 5,658 stars on Codeberg, last updated
  2026-10-16.
  https://forgejo.org/2022-12-15-hello-forgejo/ , https://forgejo.org/2024-08-gpl/ ,
  https://forgejo.org/releases/ , https://codeberg.org/forgejo/governance ,
  https://codeberg.org/api/v1/repos/forgejo/forgejo
- Web UI: full forge; pull requests, issues, Forgejo Actions CI (runner separate).

## Gitea

- Stack: Go single binary; SQLite, PostgreSQL, MySQL, MSSQL drivers. Official sizing:
  "2 CPU cores and 1GB RAM is typically sufficient for small teams/projects".
  https://docs.gitea.com/
- Users and keys: same shape as Forgejo (CLI user create; keys via admin API).
- GitHub mirror: built in, per repo; "Sync when new commits are pushed" since 1.18;
  token as password over HTTPS. "Currently Gitea supports no ssh push mirrors";
  workaround is a post-receive hook. https://docs.gitea.com/usage/repo-mirror
- NixOS: `services.gitea`, maintainers `techknowlogick`, `SuperSandro2000`; options
  parallel to Forgejo's. nixpkgs warns not to run Forgejo through it.
  https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/misc/gitea.nix
- Steward, licence, activity: MIT; "leadership and commercial support from CommitGo";
  paid Enterprise tier exists. Latest v1.27.3 (2026-08-29,
  https://proxy.golang.org/code.gitea.io/gitea/@latest). https://about.gitea.com/
- Web UI: full forge; PRs, Gitea Actions CI.

## GitLab CE

- Stack: Ruby on Rails (Puma, Sidekiq) plus Go components (Gitaly, Workhorse, Shell),
  PostgreSQL (only supported DB), Redis/Valkey. Minimum single node: 8 vCPU, 16 GB RAM
  ("can run with at least 8 GB" when memory-constrained).
  https://docs.gitlab.com/install/requirements/
- Users and keys: web/API; no Nix-declared users.
- GitHub mirror: push mirroring is in Free tier; updates within five minutes of a push
  (one minute if only protected branches); auth is a GitHub personal access token over
  HTTPS; max 10 push mirrors per project.
  https://docs.gitlab.com/user/project/repository/mirror/push/
- NixOS: `services.gitlab`, `meta.teams = [ teams.gitlab ]`, large module.
  https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/misc/gitlab/default.nix
- Steward, licence: GitLab Inc., CE under MIT. Full forge with CI.
- Fit: far too heavy for "simple".

## Gerrit (one line)

Java/JVM code-review server with NoteDb in-repo storage; GitHub push via the
`replication` plugin (event-driven per ref update, SSH key from `~/.ssh/config` or HTTP
credentials in `secure.config`); NixOS `services.gerrit` has `replicationSettings`,
`plugins`, `builtinPlugins`, `jvmHeapLimit`. Review-workflow-centric, heavy, not a fit.
https://gerrit.googlesource.com/plugins/replication/+/refs/heads/master/src/main/resources/Documentation/config.md ,
https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/web-apps/gerrit.nix

## Recommendation for "declared keys + automatic GitHub mirror"

Simplest fit: plain git over SSH with `git-shell`, optionally cgit for browsing.
- Keys: `users.users.git.openssh.authorizedKeys.keys` generated from the cluster's key
  list on the node with the Git-server role. No application state, no database, no
  admin API, nothing to reconcile; removing a key from cluster data removes access on
  the next deploy.
- Mirror: one hook set system-wide by `core.hooksPath`, a `post-receive` that runs
  `git push --mirror` to `git@github.com:<owner>/<repo>.git` in the background with a
  machine-user SSH key (or token) delivered as a secret, plus a systemd timer that
  re-mirrors every repo to cover failed pushes and GitHub outages.
- Repos: a declared list or a `git-shell-commands/create` script that runs
  `git init --bare` and `gh repo create`.

Step up: gitolite in on-server mode (keydir and conf written by Nix, mirror hook via
`services.gitolite.commonHooks`) when per-user or per-repo access rules are wanted;
it also gives create-on-push via wild repos. Choose Forgejo only if a web UI, pull
requests or CI become wanted; its mirror is built in, but keys and per-repo mirrors
must be reconciled over its API. Soft Serve is declarable only with all keys as
admins, has no push mirror, and has a record of authentication-bypass advisories.

## GitHub status, 2026-10-16

- From this host, github.com (140.82.113.3), api.github.com and www.githubstatus.com
  all failed to connect (ECONNREFUSED/timeout). status.atlassian.com, another Atlassian
  Statuspage host, also timed out, while codeberg.org, gitlab.com, google.com,
  raw.githubusercontent.com and cloudflarestatus.com answered. The failure therefore
  looks like a local route problem, not proof of a GitHub outage, and githubstatus.com
  could not be read directly.
- Search results (indirect, not the live page): the cached githubstatus.com page showed
  no incident under an Oct 16 heading; UptimeRobot and IncidentHub (check at 16:05 UTC
  Oct 16) reported GitHub operational. Recent incidents: Oct 15 (~26 min, automations
  delay), Oct 12 (Actions, Pull Requests, Issues, ~8 h), Oct 7 (Git operations, PRs,
  Actions, resolved same day).
  https://www.githubstatus.com/ , https://uptimerobot.com/is-it-down/github/ ,
  https://incidenthub.cloud/status/github ,
  https://gvwire.com/2026/10/07/github-down-for-thousands-of-users-downdetector-shows/
