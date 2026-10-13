---
name: knowledge-file-editing
description: The non-Primary jj publication procedure is needed.
dependencies: [compensation-file-editing]
---

In another repository or independent jj workspace, a commit names only the paths this flow edited: `jj commit -m 'message' path ...`.

The sequence for landing normal non-Primary jj work:

    jj commit -m 'short imperative message'
    jj bookmark set main -r @-
    jj git push --bookmark main

`jj commit` snapshots the working copy. After it, `@-` is that
commit. `jj bookmark set main -r @-` advances main to it. Then
push.
