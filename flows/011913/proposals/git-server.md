Presentation.{ «The Git server is a node capability» Proposal }

# The Git server is a node capability

Created by Fable 5.1, on the living's words of 2026-11-09.

### Proposal 1: A capability, and its name · psyche-belief › vision/git-server.md

::: comment
GitHub unreachable today left a landed commit unpushed. The living: a feature in Horizon that a node turns on, making it the cluster's Git server, and `git.<cluster>.<domain>` resolving to it. vision:horizon says everything a node does is a capability, so the role becomes one, declared in the cluster data, and the domain is the cluster's.
:::

- The cluster runs its own Git server on the node whose cluster data gives it the GitServer role. It serves thinking machines: it accepts the SSH keys the cluster data holds, carries no web interface, and mirrors every repository to GitHub as a backup.
+ The cluster runs its own Git server on the node whose cluster data gives it the GitServer capability, one capability among the node's others. It serves thinking machines: it accepts the SSH keys the cluster data holds, carries no web interface, and mirrors every repository to GitHub as a backup. The cluster's domain names it: `git.<cluster-name>.<domain>` resolves to that node, and every flake input and every clone on the cluster names a repository there, so GitHub's reachability is no longer the cluster's.

+ ```datom
+ ; a node in the cluster data, with the capability turned on; the names are an example
+ { builder [ GitServer RemoteBuilder ] }
+ ```

+ ```nix
+ inputs.flow.url = "git+ssh://git.example.criom.net/flow";   # the cluster's own server; flake.lock holds the commit
+ ```

+ ```mermaid
+ flowchart TB
+     c["cluster data: a node with GitServer"] -- "Horizon composes, Lojix deploys" --> n["the node, serving Git over SSH"]
+     d["git.cluster.domain"] -- "resolves to" --> n
+     n -- "mirrors every repository to" --> g["GitHub, the backup"]
+ ```
