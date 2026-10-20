
## 2026-10-16 11:00 Our own Git server

"Let's get our own Git server up. We should have done that a long time ago. ... how we could best fit it in a cluster role. Obviously nothing is hardwired in the code, right? It's all configured using the cluster data. If there's a node that has the Git server role, we'll make that Prometheus for now and use something simple. It can be preconfigured to accept the SSH keys that we have in the cluster data. ... Then we can have our own Git server with GitHub backup mirroring."
-- psyche, STT.

## 2026-10-16 11:14 The role is named Git server

"Yeah the name is Git server obviously."

Context: choosing between the new GitServer capability and the existing GitoliteServer marker.
-- psyche, typed.

## 2026-10-16 11:15 A Git server for the thinking machine

"I don't particularly care for a fancy web user interface because this is a Git server that's being used by the thinking machine. All the visualization can be done through other means than using a web UI for the Git server."

Context: asking to review the Git server options and why one or another.
-- psyche, STT.

## 2026-10-16 11:25 The module is named Git Server; the type is the directory

"This should be called Git Server. Let's get someone to change the code and the way the files are structured so that we don't have a skill directory and so that the context module type is the directory."

Context: comment on «Git servers for the thinking machine», Proposal 1 target file vision-git.md.
-- psyche, STT.
