---
title: 516 — System deep audit — frame and method
role: designer
variant: Psyche
date: 2026-06-04
session: meta-report directory (sub-agent session)
topics: [audit, schema, nota, engine, wire-contract, runtime-triad, intent, design-constraints, code-bulk, bad-patterns]
description: |
  Orchestrator frame for a psyche-requested deep audit: a series of
  Psyche reports explaining the schema-derived stack with REAL RUN CODE
  (no guesswork), plus an audit for gaps / bad patterns / repetition /
  code-bulk, plus an intent-file review across the active repo set, with
  the most important design constraints isolated toward each repo's
  INTENT.md.
---

# 516 — System deep audit — frame and method

## What the psyche asked for

A full deep audit to "get to know my software." Four threads, in the
psyche's own framing:

1. **Explain the system with real run code.** A series of Psyche
   reports explaining different parts — "I want to see schema, how
   schema relates to NOTA, how schema creates an engine or how it
   creates a Y-only [wire-only] interface." Hard constraint: **"actual
   code that has been run … no guesswork. Just pure real stuff."** Every
   mechanism claim is backed by a command that was actually executed and
   its verbatim output.

2. **Audit for gaps and bad patterns — report only.** "Look for gaps,
   bad patterns, any bad patterns … report them and then we can see
   what we want to do with them. Especially things that are common —
   where does the bulk of the code end up, where do repetitions appear,
   anything that looks ugly." No fixes this pass; surface and catalogue.

3. **Isolate the most important design constraints.** "What are the most
   important design constraints? Let's start to isolate those. Those
   should be in the INTENT.md of the repository."

4. **Review every repository's INTENT.md.** "Every repository needs an
   intent file. It's the first thing we should create. What is the
   intent of this repository? What is it for?" The INTENT.md holds the
   most important AND ONLY the most important design intent for that
   project. Psyche reports explaining a repo should be based on its
   reviewed/curated INTENT.md. Captured as Spirit record `nqsb`
   (Principle, VeryHigh, 2026-06-04).

## Method — the no-guesswork discipline

Every mechanism report in this directory follows one rule: **a code
claim is only allowed if a command was run and its real output pasted.**
Reports name the exact command, the repo it ran in, and the verbatim
result. Where something could not be run in this environment, the report
says so explicitly rather than inventing an output. A separate
adversarial verification pass re-runs the load-bearing commands of each
mechanism report and records whether the pasted output is genuine
(`real` / `partial` / `guesswork`). The verdict travels with the report.

Tooling confirmed live this session: `cargo` (`~/.nix-profile/bin/cargo`,
stable channel) builds these crates; the deployed `spirit` CLI
(`spirit-v0.5.1`) accepts NOTA and replies with typed NOTA records.

## Scope

**Deep run-code mechanism reports — the schema-derived stack core:**
`nota-next`, `nota-codec`, `schema-next`, `schema-rust-next`,
`triad-runtime`, `spirit`, and the contract pattern (`signal-spirit`).
This is where "schema ↔ NOTA / schema → engine / schema → wire-only"
actually lives.

**Intent-file review — broad** across the active repo set
(`protocols/active-repositories.md`): does each repo have an INTENT.md,
what is it for, what are its most important design constraints, and what
should its curated INTENT.md say. Missing INTENT.md files are flagged.

**Code-bulk / repetition / bad-pattern audit** spans the core stack and
samples the wider set.

## Directory layout (this meta-report)

- `0-frame-and-method.md` — this file.
- `1`–`6` — mechanism deep-dives (NOTA, schema↔NOTA, the pipeline,
  schema→engine, schema→wire-only, the runtime triad in spirit), each
  with run output and a verification verdict.
- `7`–`8` — audit dimensions (code-bulk + repetition; bad-patterns +
  ugliness + gaps).
- `9`–`10` — intent-file review (core stack; wider set).
- highest-numbered `*-overview.md` — orchestrator synthesis: the most
  important design constraints isolated system-wide, the cross-cutting
  audit findings, and the per-repo INTENT.md recommendations.

This directory IS the meta-report; it is garbage-collected as one
session unit. The findings are report-only — no code or INTENT.md was
changed by this audit; recommendations await psyche decision.
