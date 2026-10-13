---
description: A flow edits files or publishes work outside Primary.
dependencies: []
---

Outside Primary, commit and push every change your work produces in every affected repository, including generated output.

Outside Primary, commit existing dirty changes first with an appropriate message
before starting new work.

Every `jj` command that takes a description uses `-m`. Never open
an editor. Never use raw `git`.

A source file is written in pieces of a few hundred lines; a module that would exceed that is split.
