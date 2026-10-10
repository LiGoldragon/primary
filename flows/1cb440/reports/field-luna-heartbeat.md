# Field Luna heartbeat assessment

This is an evidence report, not a timer or a lifecycle receipt.

The living authorized an ultra-low Luna heartbeat every 30 minutes for Field
reaping and archive maintenance. Luna is the ultra-low tier and medium is its
configured effort.

## Current mechanism

`core-checkup.timer` is already enabled as a persistent systemd user timer.
It runs a bounded `core-checkup.service` every 30 minutes, with a 120-second
runtime limit, 256 MiB memory limit, and no long-running model process. Its
policy enables the existing ephemeral Luna analysis. The next observed timer
trigger is 2026-09-19 13:57 CST.

That installed job is monitoring-only. Its verified source collects projected
endpoint, unit, liveness, message-health, and quota metadata, then sends only
a thin summary to ephemeral `gpt-5.6-luna`. It has no operation for a Herdr
route, Hacky Messenger retirement, transcript archive, lifecycle judgment, or
reaper receipt.

`tools/field-watcher` is also non-destructive. `tools/reaper --dry-run` lists
Herdr and HM state and explicitly refuses broad execution. The live dry-run
on 2026-09-19 found a done Mind Astra route plus idle routes, but each still
requires an explicit route audit; working and no-agent entries were retained.
No cleanup was inferred from these statuses.

## Why no new timer was activated

The current `core-checkup` implementation is pinned from an earlier primary
revision and its Home module is no longer in the current CriomOS-home source.
The current implementation cannot be configured to reap or archive. Adding
an unmanaged unit or an ExecStart drop-in would bypass the declarative
operating-system source, and would not supply the required lifecycle evidence.

The minimum compliant implementation is a declared replacement for the
existing bounded 30-minute user timer. Its Field Luna oneshot must consume
metadata only, record a durable scan/archive receipt, and admit an exact
target only when it has: completed, superseded, or dead lifecycle evidence;
retained transcript or handoff; no active work, lock, or unpersisted state;
and a last-moment native identity and HM-route preflight. It must leave
protected, active, and unresolved targets untouched. A model is not kept
alive between runs, and the job must not create a Field or Psyche main seat.

No transcript content was placed in routine model context. No existing timer,
route, archive, Flow identity, or Fable artifact was changed.
