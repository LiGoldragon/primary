---
description: A test is written, chosen or judged.
dependencies: [operation-nix-workflow]
---

A test never searches production code for a string. It runs the whole
system under normal use, in a developer build with tracing, and passes
when the expected trace appears, in order where order matters.

Package build and test execution in Nix and run heavy work on the
configured remote builder, NixBuilder, rather than the laptop. A failed
remote route is a concrete blocker, never a reason to fall back to local
compilation or a heavy local test run.

Publish the owned source changes through the repository's supported
path-scoped commit and push route. Run acceptance checks against that
exact immutable published revision and report the revision, remote
builder, check and result together. Keep the laptop's work to lightweight
inspection and orchestration; expensive evaluation also belongs on a
supported remote route. Remote compilation alone does not prove that
evaluation ran remotely.
