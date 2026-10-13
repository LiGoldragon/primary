---
description: A generated tree is claimed to match its authored source, or an authored source has changed and the consumers may be stale.
dependencies: [operation-testing, operation-file-editing]
---

Prove freshness by regenerating and reading what moved in the generated paths alone:

    git status --short -- <generated roots>   # must be empty first
    <the documented regenerator>
    git status --short -- <generated roots>   # what it prints is the drift

An empty status after the regeneration is the proof that every generated file matches its source.

Name the regenerator you ran, the checkout that defines it, and the source and consumer roots you passed it. The regenerator often does not live in the repository holding the authored source.

Regenerate before editing the source as well, so drift already in the tree is not attributed to your change.
