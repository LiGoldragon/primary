---
name: operation-file-editing
description: Publish edits through the repository’s designated committer.
dependencies: []
---

Outside Primary, commit and push every change your work produces in every affected repository, including generated output.

Outside Primary, commit existing dirty changes first with an appropriate message
before starting new work.

Only the standing Field Quaternary committer commits and pushes Primary. It holds PrimaryPublish for its lifetime and works in the shared working copy with jj, never a clone or another worktree. Editing flows leave their owned changes in place; their supported turn-end hook notifies that committer only when Primary is dirty, carrying the actual editor FLOW_ID or native session_id and transcript path. The committer reads the transcript and commits the owner’s named paths, preserving other writers’ work and reporting collisions. Follow `compensation-primary-commit` for publication and late-change squashing; editors never acquire a competing publication lock or commit Primary themselves. In another repository or independent jj workspace, a commit names only the paths this flow edited: `jj commit -m 'message' path ...`.

The sequence for landing normal non-Primary jj work:

    jj commit -m 'short imperative message'
    jj bookmark set main -r @-
    jj git push --bookmark main

`jj commit` snapshots the working copy. After it, `@-` is that
commit. `jj bookmark set main -r @-` advances main to it. Then
push.

Every `jj` command that takes a description uses `-m`. Never open
an editor. Never use raw `git`.

A source file is written in pieces of a few hundred lines; a module that would exceed that is split.
