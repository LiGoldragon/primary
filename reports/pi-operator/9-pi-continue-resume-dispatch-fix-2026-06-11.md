---
title: 9 — pi-continue resume dispatch fix
role: pi-operator
date: 2026-06-11
topics: [pi, pi-continue, continuation]
description: Diagnose and patch the pi-continue automatic continuation resume failure shown by Pi's continuation UI.
---

# 9 — pi-continue resume dispatch fix

## Symptom

The screenshot showed Pi after an automatic continuation failure:

- `Warning: The previous continuation is still resuming; no new handoff was started.`
- `Operation aborted`
- `Error: automatic continuation: resume request failed.`

That is the `pi-continue` package's resume-dispatch path, not core Pi compaction alone.

## Installed package state

The active Home profile had `pi-continue` version `0.8.2`. The npm registry and upstream repository both report `0.8.2` as latest, so there was no newer upstream package containing a fix.

## Root cause hypothesis

`pi-continue` queued the same-session resume prompt with Pi follow-up delivery. Follow-up delivery waits for the current agent run to become fully idle. During automatic mid-run continuation, the parent run has already been aborted after a completed tool-result batch, but it can still reach another pre-provider context check before the follow-up queue drains. At that point the saved handoff is still in `resume.status = pending`, so the next automatic guard sees an active previous continuation, aborts the old run, and the pending resume can time out as a resume-request failure.

The observed warning plus failure line match that state machine shape.

## Fix applied

CriomOS-home now patches the unpacked `pi-continue` package at build time:

- `packages/pi-continue/default.nix` applies a local patch after unpacking the npm tarball.
- `packages/pi-continue/resume-dispatch-steer.patch` changes resume prompt delivery from `followUp` to `steer`, with a bare `sendUserMessage` fallback for idle API variants.

Steering delivery is the needed boundary: resume before the next provider request from the old turn, instead of waiting until the old run is fully idle.

## Validation

Validation completed:

- Built `.#packages.x86_64-linux.pi-continue` successfully.
- Loaded the built extension with Pi RPC and confirmed the `/continue` command registers.
- Pushed CriomOS-home commit `37e5d39b` (`home: steer pi-continue resume dispatch`) to `main`.

## Local activation note

For immediate use on Ouranos, `$HOME/.pi/agent/packages/pi-continue` was repointed to the fixed built package. Future Home profile rebuilds from CriomOS-home `main` will make the same fix declarative again. Existing Pi processes should run `/reload` or restart to load the patched extension.
