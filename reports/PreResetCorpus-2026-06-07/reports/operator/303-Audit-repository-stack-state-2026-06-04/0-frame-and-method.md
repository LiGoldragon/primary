---
title: 303 - Repository stack state audit - frame and method
role: operator
variant: Audit
date: 2026-06-04
topics: [repository, audit, spirit, schema-stack, dependencies, active-repositories]
description: |
  Frame for the operator repository audit requested after the old
  operator session became too large. The audit inspects active versus
  stale repositories, Spirit source topology, deployment stack split, and
  important dependency versions.
---

# 303 - Repository stack state audit - frame and method

## Prompt

The psyche asked the new operator session to delete the obsolete research
cloud/session-cleanup report, refresh on intent and skills, inspect the
designer's current design-to-code audit, and produce a full repository
situation report covering active versus abandoned repositories, Spirit source
topology, important dependency versions, stack handling, glaring issues,
questions, proposed solutions, visuals, and code.

## Method

The operator used `protocols/active-repositories.md` as the active repository
map, `RECENT-REPOSITORIES.md` and local `repos/` symlinks as broader checkout
context, and per-repo metadata (`AGENTS.md`, `skills.md`, `INTENT.md`,
`ARCHITECTURE.md`, `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`,
tests, and recent history) for the audit surface.

Two non-blocking explorer subagents were dispatched under the operator lane:

- `1-spirit-source-topology.md` — Spirit family source, production versus next
  topology, and whether there are two source repositories.
- `2-dependency-version-inventory.md` — important dependency versions across
  active repositories and visible drift.

The operator synthesis lands as `3-overview.md`. The psyche-facing summary
lands separately as `reports/operator/304-Psyche-repository-stack-state-2026-06-04.md`.
