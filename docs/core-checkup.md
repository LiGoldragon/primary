# Core checkup

`systemd/user/core-checkup.{service,timer}` is a source-controlled user-unit payload. Deployment must materialize `config.json` from the active projection: it supplies the actual Ygg endpoints, allowlisted owned units, liveness facts, and quota reading. The job never invents addresses or executes model-produced commands.

The default is observation. A roster entry may be `applicable: false`: the unit is recorded as `not-applicable`, never becomes a failed episode, and cannot be restarted. The current `cc-daemon.service` is such a legacy name: observed through the user manager as `LoadState=not-found`, `ActiveState=inactive`, `SubState=dead`. It is not the live Claude harness; Claude liveness comes from `claude agents --json`.

 A restart requires all of `allowRepair`, `owned`, and `allowRestart`; it occurs once when a unit first enters a failed episode and is recorded as a scalar event. The guard clears after an active observation. Message process/socket liveness is distinct from semantic health; semantic health remains `unverified` without a supported runtime API. Wake results are `accepted` or `undelivered`; a failed wake is never repair evidence.

Every NDJSON record has schema `core-checkup/v1` and only scalar fields or
bounded enum arrays: a timestamp, stable kind/status/finding codes, and a
configured target identifier. It never retains prompt or transcript text,
model prose, command output, or raw errors. `config.json` must state the
event-log retention owner and policy explicitly; this payload neither invents
a retention period nor deletes history. A separately addressed diagnostic
artifact may be referenced by identifier and hash in a future schema, but not
embedded in the thin log.

When the projected config sets `luna: true`, the program makes one ephemeral
`codex exec --model gpt-5.6-luna --sandbox read-only --skip-git-repo-check` call. Its prompt contains
only the deterministic thin probe summary; its JSON-schema response is limited
to a status and at most three stable finding codes. The runner never executes text
from that response. It has a 90-second child timeout, while the user service
has a 120-second runtime and start timeout and a 256 MiB memory cap. If the
call is unavailable or malformed, the event is `luna/unavailable`; probes and
state recording still complete. This is analysis, not a repair channel.

## Read-only witness, 2026-09-15T23:05Z

The job ran with `allowRepair: false` against addresses already configured in
`/etc/hosts`, rather than inferred addresses. IPv6 pings to ouranos,
prometheus, and zeus succeeded. `orchestrate-nexus.service`,
`message-daemon.service`, `codex-remote-control.service`, and system
`lojix.service` were active. `cc-daemon.service` was inactive; it is neither
owned nor allowlisted, so the job only recorded `failed` and made no restart.
The Message semantic-health event remained `unverified`. Claude's supported
`agents --json` command reported the primary and secondary as idle, but gives
no reliable idle-duration field, so wake eligibility was deliberately not
evaluated. The raw app-server response's `codex_bengalfox` readings were 0%
used for a 300-minute window resetting `2026-09-16T04:06:58Z` and 0% used for
a 10,080-minute window resetting `2026-09-22T23:06:58Z`, with three reset
credits. A separate normalized situation report rendered 55% remaining with a
Saturday reset; it is not a raw app-server field and must not be treated as
one. The API supplied no Claude reading.

## Deployment proposal

CriomOS-home may declare the generic user service and timer, because it owns
the user environment. It must not embed the Lojix probe or configuration:
its architecture says, exactly, “Lojix is exclusively OS-owned; this
repository has no Lojix input, package, app, service, state, environment, or
executable surface.” The split is therefore a generic Home timer that invokes
the primary-owned checkup program, plus an OS/Horizon-projected runtime config
which supplies the observed-unit and endpoint roster. No activation is
proposed until that projection and the primary's identity/lane bootstrap are
witnessed.

## Transient timer witness

`tools/core-checkup-witness.mjs CONFIG ARTIFACT_DIRECTORY` creates one uniquely
named transient *user* timer, scheduled one second ahead. It refuses any config
other than `allowRepair: false`, `luna: true`, and no wake transport. The
transient service has the same 120-second and 256 MiB limits as the proposed
persistent service. The helper retains a run-scoped config, events, journal,
and `core-checkup-witness/v1` receipt in the caller-provided artifact directory,
then stops and resets only its own timer and service. It is a one-shot test,
not installation or enablement of the 30-minute timer.


## Persistent activation gaps

The 30-minute unit source is ready but remains inactive. Its projected config must
provide `eventLog.retention`, the endpoint/unit roster, and `livenessProbe.targets`
for the primary and secondary Claude IDs. If that config is absent or invalid, the runner appends only `config/missing` or `config/invalid` to its own event path and exits non-successfully. Each invocation runs `claude agents --json`
fresh and maps `waiting` to ineligible; the CLI has no idle-since field, so every
idle duration remains `null` and wake remains suppressed. The supported app-server reader makes only `initialize`, `initialized`, `account/rateLimits/read`, and `account/usage/read` calls. It emits independent account, `codex_bengalfox` primary, and `codex_bengalfox` secondary windows with raw `usedPercent`, explicitly derived `remainingPercent`, exact `windowMinutes`, and UTC `resetsAt`. Claude quota is always `unknown` until its own supported reader exists. It never calls rate-limit-reset credit consumption. The OS/Horizon projection must
be materialized and evaluated, then the user-environment owner must install and
enable the source-controlled unit with an activation receipt. No current CriomOS
proposal has a source-bound materialization receipt, so this change does not claim
persistent activation.
