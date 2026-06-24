---
title: 462 — Psyche alignment and session management
role: operator
variant: Research
date: 2026-06-24
topics: [psyche-alignment, session-management, lanes]
description: |
  Frame for exploring how fresh-session workflow, psyche alignment, lane naming,
  and external "grill me" workflow practice should map into this workspace.
parent_meta_report: reports/operator/462-Research-psyche-alignment-session-management
slot: 0
---

# 462 — Psyche alignment and session management

## Intent Anchors

[Agent workflow should favor fresh sessions over context compacting: the psyche clears context and starts a new session for a new topic, while context compaction remains appropriate for a continuing agent that is still applying work in the same session.] Spirit `80zj`.

## Frame

The psyche wants to align on a changed workflow: new agent sessions by topic, clear context as the normal boundary, and use compaction only when an already-running agent is still applying work. The current lane names (`operator`, `designer`, `system-operator`, etc.) no longer stay visible as stable session labels in Codex/cloud harnesses after clearing context, so the session label may need to come from the first prompt or topic instead of from the role lane.

The psyche also wants the old "grill me" inspiration checked against the workspace's `alignment-interview` skill. The current local skill already requires exactly one focused plain-chat question per turn; the open question is whether the name and mechanism should become "psyche alignment" and whether the skill should more forcefully produce brief, concise responses.

## Method

One background explorer receives slot `1-pocock-project-and-session-lifecycle.md`. Its task is to find the external Matt Pocock / Sandcastle / "grill me" project or nearest public source, inspect how it handles session setup, alignment, archiving, deletion, garbage collection, and stale planning artifacts, and report only the mechanisms relevant to this workspace.

The main operator continues the live alignment in chat using the local rule: exactly one focused question per turn, with a recommendation and alternatives.
