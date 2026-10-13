---
name: compensation-testing
description: A test is written, chosen or judged.
dependencies: [compensation-nix-workflow]
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

Test the changed contract with the smallest meaningful witness.
Use the repository's durable test gate.
Infrastructure reports are ground: a build reported green is green, wherever it ran.
Expose every durable test through a Nix check.
Keep stateful test requirements explicit.

A test runs the machinery and observes what it does. A test that
searches or compares source text is a change-detector: it fails on
any edit and catches no behavior — never write one. Text may be
asserted only where the text is itself the product, as generated
output against its authored source.

A new test is seen failing once before it is trusted.
The expected value comes from outside the code under test; a test
that computes it through the tested path confirms nothing.
A test waits on the tested event, never on the clock.
Tests share no mutable state — no process environment, no working
directory, no order between them.
A run that may exhaust memory or time is bounded (a memory cap and a timeout) so that it cannot take the harness down with it.
