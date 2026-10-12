---
description: A test is written, chosen or judged.
dependencies: [operation-testing, operation-nix-workflow]
---

A test runs the whole system under normal use, in a developer build
with tracing, and passes when the expected trace appears, in order
where order matters.

Heavy work, expensive evaluation included, runs on the configured remote
builder, NixBuilder; the laptop keeps to lightweight inspection and
orchestration. Outside a condition `compensation-temporary` declares, a
failed remote route is a concrete blocker, never a reason to fall back
to local compilation or a heavy local test run. Remote compilation alone
does not prove that evaluation ran remotely.

Run acceptance checks against the exact immutable published revision
of the owned changes, and report the revision, remote builder, check
and result together.
