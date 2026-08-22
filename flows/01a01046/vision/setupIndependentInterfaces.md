## 2026-08-17T17:34:10.507+02:00 — local user deployment does not loop through root SSH

> youre already user li, thats just adding ssh overhead to go in a complete circle right back to where you started. not that its a grave mistake, but its useless churn.

Context: an agent proposed deploying the local `li` user environment by connecting over SSH to the same host as root and then switching back to `li`. The psyche identified the route as circular overhead for a deployment whose target user is already the local caller.

