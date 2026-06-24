---
title: 241 - Lojix production runtime current surface
role: system-operator
variant: Refresh
date: 2026-06-24
topics: [lojix, production-runtime, deploy, context-maintenance]
description: |
  Refresh of the system-operator lojix production runtime handoff,
  readiness, and regression reports. Carries forward the installed daemon
  state, fixed activation-regression facts, current verification gap, and
  remaining operational follow-ups.
---

# 241 - Lojix production runtime current surface

## Intent Anchors

[Context maintenance is research-driven intent-alignment refresh, not deletion: read intent first to weight currency, review stale reports and live context against current engine, architecture, and intent, and for each item whose abandon/keep/migrate/forward disposition is unclear, ask the psyche one focused intent-alignment question before deciding. Re-research and write the necessary superseding review or handoff that brings substance forward. Output is a small load-bearing current-state set and a clean starting point for the next session, not an accumulating archive.]

[Reports are a small load-bearing set, not an accumulating archive; history lives in jj/git. Context maintenance reduces report count without losing information by agglomerating per topic: multiple reports become one Refresh report (the Capital variant tag after the number) preserving un-contradicted, un-superseded substance in better form; source reports are then deleted with the Refresh report as landing witness.]

## Current Runtime State

The installed lojix daemon is active on Ouranos.

Fresh checks on 2026-06-24:

- `systemctl is-active lojix-daemon.service` returned `active`.
- `lojix-daemon.service` is running installed `lojix-0.3.10` with exactly one startup argument, `/run/lojix/startup.rkyv`.
- `/run/lojix/owner.sock` is `0600 li:users`.
- `/run/lojix/ordinary.sock` is `0660 li:users`.
- `/run/lojix/startup.rkyv` is `0600 li:users`.
- `/home/li/.nix-profile/bin/lojix-run` resolves to `lojix-run-0.3.10`.
- `spirit Version` reports `0.16.0`.
- `systemctl --failed` reports zero failed system units.

The older production-runtime reports that still said Spirit was `0.15.0`, or that the installed daemon/query work was still pending, are stale.

## Query Gap

A fresh ordinary query today returned:

```text
(Queried ([] (264 264)))
```

This is not carried forward as the old report-222 bug unchanged. `reports/system-maintainer/11-lojix-daemon-zeus-live-switch-query-parity-2026-06-15.md` proves that after the 2026-06-15 Zeus live `Switch`, ordinary query returned the current live generation and the empty-query symptom was fixed for that real terminal activation.

The current empty result is therefore a fresh verification gap: either the current database has no current generation row for this query shape, the query semantics changed, or a later deploy path records marker progress without a generation row. A future system-operator or system-maintainer pass should retest with a real deploy context before reopening the old bug framing.

## What Is Settled

- The source-tree-only daemon validation is no longer the acceptance path. Production readiness means installed binaries, generated rkyv startup, systemd service, socket modes, and installed clients.
- The installed daemon/service path exists and is active on Ouranos.
- The temporary `CriomOS-home/criomos-home-spirit-bypass` activation regression has been fixed: `lojix-run` now resolves to `0.3.10`, not the old `lojix-cli` wrapper line.
- The `/tmp/spirit-sb2` sandbox daemon is not running, but stale files and socket pathnames still exist under `/tmp/spirit-sb2`.

## Remaining Operational Follow-ups

- Recheck ordinary generation query semantics during the next real terminal deploy or activation validation.
- Decide whether stale `/tmp/spirit-sb2` artifacts can be removed; no process is running, but the directory still contains `config.rkyv`, `daemon.log`, `spirit.sema`, and stale socket pathnames.
- Track the admission-vs-terminal-success vocabulary cleanup: `meta-lojix` still replies with `Deployed` at admission time because the contract names the accepted deploy handle that way.
- Move daemon deploy credentials toward first-class key-management design. The installed service currently relies on the operator user's SSH agent socket for target copy.

## Retired Sources

This Refresh absorbs and retires these system-operator sources; git history keeps the old reports:

- `reports/system-operator/220-lojix-daemon-install-zeus-deploy-handoff-2026-06-14.md` - the install-first handoff completed; installed service/socket acceptance carries forward here.
- `reports/system-operator/222-Refresh-lojix-daemon-production-readiness-2026-06-15.md` - superseded by system-maintainer closeout 11 and fresh runtime checks.
- `reports/system-operator/233-lojix-run-profile-regression-root-report.md` - the bypass-ref regression fix, `lojix-run-0.3.10` verification, sandbox-daemon residue, and child-process-leak note carry forward here; no live daemon child leak was re-observed in this pass.
