---
title: 0 — Schema help daemon pilot frame and method
role: schema-help-daemon-pilot-operator
variant: Synthesis
date: 2026-06-24
topics: [schema, help, daemon, beads]
description: |
  Session frame for the operator lane implementing, testing, auditing,
  and fixing the schema-help daemon pilot bead graph rooted at
  primary-80cw.
slot: 0
---

# 0 — Schema help daemon pilot frame and method

## Trigger

The psyche asked this lane to use a subagent to decide whether the work is
intent-aligned enough to fan out implementation subagents, and if so to launch
subagents to implement, test, audit, and fix the bead graph rooted at
primary-80cw.

Spirit gate outcome: no capture. The prompt is a task-only order against an
already-filed bead graph and does not add durable workspace intent.

## Lane

This session is registered as `schema-help-daemon-pilot-operator`, carrying the
operator discipline. Reports for this session live in this directory. Reports
are claim-exempt; shared code, schema, and documentation edits must be claimed
through `orchestrate`.

## Root Work

Root bead: `primary-80cw` (schema help daemon pilot: embedded catalogs plus
registry for production cutover).

The graph's visible chain is:

- `primary-80cw.1` schema-owned rkyv help catalog over `SpecifiedSchema`.
- `primary-80cw.2` schema-rust embedded catalogs and type-attached help
  accessors.
- `primary-80cw.3` schema-daemon registry/query contract.
- `primary-80cw.4` schema-daemon persisted catalog registry and type-help
  lookup.
- `primary-80cw.5` mentci pilot type-spec panel from schema-daemon.
- `primary-80cw.6` signal-spirit canary off schema-owned help catalog.
- `primary-80cw.7` production cutover readiness gate.
- `primary-80cw.8` Spirit 6th4 intent/report maintenance.

Known blockers from the psyche's prompt:

- `primary-vllc` blocks the schema-owned help catalog.
- `primary-yeom` blocks generated embedded help.
- `primary-lwc6` blocks daemon registry implementation.

## Method

Slot allocation begins with one critical-path context subagent:

- Slot 1:
  `reports/schema-help-daemon-pilot-operator/1-schema-help-alignment-context.md`
  — collect live repo, report, bead, and intent context; decide whether the graph
  is aligned enough to fan out implementation subagents; if yes, propose the
  concrete disjoint subagent slices and write-ready briefs.

If slot 1 says the graph is aligned, this lane launches a second wave with
disjoint write scopes, preallocated report slots, and explicit worktree/claim
instructions. If slot 1 finds a blocking design or intent gap, the lane writes
that gap into this session directory and stops fanout until the gap is resolved.

Every implementation slice must obey the operator discipline:

- read the target repo's `INTENT.md` before code;
- read that repo's `AGENTS.md`, `skills.md`, and `ARCHITECTURE.md`;
- claim the task and exact path scopes before edits;
- use feature worktrees for code-repo subagent edits;
- keep Rust behavior on data-bearing types or trait impls;
- prove schema-derived behavior with generated types and rkyv/NOTA witnesses;
- expose tests through Nix, not only `cargo test`;
- commit and push with `jj` using inline messages.
