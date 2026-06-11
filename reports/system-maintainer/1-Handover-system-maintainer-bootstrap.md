---
title: 1 — System maintainer bootstrap
role: system-maintainer
variant: Handover
date: 2026-06-11
topics: [system-maintainer, crayon-os, deployment]
description: |
  Bootstrap handover for the new system-maintainer role: role scope,
  report lane, orchestration registration, and first-test readiness.
---

# 1 — System maintainer bootstrap

## Intent Anchors

[The primary workspace has a new system-maintainer role: the system maintainer owns mostly updating, debugging, and deploying Crayon OS on various hosts, is expert in Crayon OS and Logic, knows the current production and development stacks, overlaps system-operator but is less development-focused and more maintenance/deployment-focused.]

## Ready state

The `system-maintainer` role exists as an operational lane for Crayon OS and Logic maintenance. It is registered in the workspace role list, has its own skill, and has this report directory as its lane-owned communication surface.

The role's working boundary is maintenance-first: update, debug, deploy, verify, recover, and hand over. Structural platform changes, deploy topology redesign, and broad development remain system-operator or designer work unless the task is a focused operational fix.

## Standing map

Production work stays on the current live stack: canonical mainline checkouts for CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon, and their production pins. Development work stays on the lean rewrite worktrees and branches until cutover is explicit.

The first action on any host task is to name the stack and target host. The first action before any code edit is to read that repo's `INTENT.md`, then `AGENTS.md`, `ARCHITECTURE.md`, and `skills.md`.

## First test readiness

The role can now be claimed through `tools/orchestrate claim system-maintainer ...`; reports land under `reports/system-maintainer/`. The first test should be a bounded maintenance task with one target host or one deploy path, so the role can prove the loop: identify stack, claim narrow scope, build from pushed state, activate through the typed deploy path, verify runtime state, and report only the load-bearing result.
