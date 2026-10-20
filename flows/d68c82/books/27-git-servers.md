<!-- to-the-living:start -->
Presentation.{ «Git servers for the thinking machine» }

# Git servers for the thinking machine

```
 flows on every host
     |  push over SSH
     v
 +------------------------+
 | the node with the      |
 | GitServer role         |
 | (Prometheus, in data)  |
 +------------------------+
     |  after every push
     v
 +------------------------+
 | GitHub, the backup     |
 | mirror                 |
 +------------------------+
```

The cluster already runs gitolite, today on Ouranos. The GitServer role moves it to the node the cluster data names; this is in a development branch, under audit.

## The options

| | what it is | keys from cluster data | mirror to GitHub | weight |
|---|---|---|---|---|
| git over SSH, git-shell | one git user, bare repositories, nothing else | yes, as that user's SSH keys | a hook after each push | git and sshd only |
| gitolite | git over SSH plus per-repository access rules | yes, declared into its key folder | a hook after each push | a Perl script, no daemon, no database |
| Soft Serve | a Git server with a terminal interface | admin keys only; others added by command | pull only; push needs a hook | one Go program and a database |
| Forgejo, Gitea | a GitHub-like web forge | no: keys are added through its API | built in, on every push | a web service and a database |
| GitLab | a full web platform | no | built in | 8 cores and 16 GB recommended |

## Why one or the other

- **git-shell** is the least there is: every key reaches every repository, and a key removed from the cluster data is gone at the next deploy.
- **gitolite** adds rules per repository and per key, still declared, still without a daemon. It is already in the system.
- **Soft Serve** suits people browsing in a terminal; its users live in its own database, not in the cluster data.
- **Forgejo, Gitea, GitLab** are built around a web interface and pull requests for people; their users and keys live in their database.

For machines that push and fetch, the first two fit; the forges carry what only people use.

## Proposal 1: what the Git server is

File: psyche-context/skills/vision-git.md, new

+ ---
+ description: The cluster's own Git server is set up or changed.
+ dependencies: []
+ ---
+
+ ## Git server
+
+ The cluster runs its own Git server on the node whose cluster data gives it the GitServer role. It serves thinking machines: it accepts the SSH keys the cluster data holds, carries no web interface, and mirrors every repository to GitHub as a backup.

Ruling: land, amend, or reject.

## Proposal 2: gitolite serves it

File: psyche-context/skills/vision-git.md, after Proposal 1's paragraph

+ Gitolite serves it, with every key and every access rule declared from the cluster data.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
