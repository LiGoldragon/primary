# Core checkup

`systemd/user/core-checkup.{service,timer}` is a source-controlled user-unit payload. The OS owns `/etc/core-checkup/roster.json`, containing endpoints, unit identities, ownership, and the global restart allowlist. The user environment owns the separate policy file containing retention, quota socket, harness targets, and a request to restart a roster unit. Policy cannot add a unit, change its scope or ownership, or override the OS allowlist. The job never invokes a model or executes model-produced commands.

The default is observation. A roster entry may be `applicable: false`: the unit is recorded as `not-applicable`, never becomes a failed episode, and cannot be restarted. The current `cc-daemon.service` is such a legacy name: observed through the user manager as `LoadState=not-found`, `ActiveState=inactive`, `SubState=dead`. It is not the live Claude harness; Claude liveness comes from `claude agents --json`.

 A restart requires all of `allowRepair`, OS ownership, both OS and policy restart permission, and an observed `is-failed` result. It occurs at most once per run and failure episode. State is atomically claimed before the restart; an existing state lock fails closed. Inactive, missing, and probe-bus failures are never repaired. A Ygg endpoint needs both a route through `yggTun` and a successful IPv6 ping. Message process/socket liveness is distinct from semantic health; semantic health remains `unverified` without a supported runtime API. Approval waits and unknown idleness never wake a Flow.

Every NDJSON record has schema `core-checkup/v1` and only scalar fields or
bounded enum arrays: a timestamp, stable kind/status/finding codes, and a
configured target identifier. It never retains prompt or transcript text,
model prose, command output, or raw errors. `config.json` must state the
event-log retention owner and policy explicitly; this payload neither invents
a retention period nor deletes history. A separately addressed diagnostic
artifact may be referenced by identifier and hash in a future schema, but not
embedded in the thin log.

The monitor is deterministic: `luna` must be exactly `false`; a policy that
requests a model is rejected as `config/invalid` before any child command is
started. A future model decision job is a separate, unimplemented surface.
Every deterministic command is killed after 10 seconds. The `flock --no-fork`
wrapper is also capped at 180 seconds for direct CLI use. The user unit has a
180-second `TimeoutStartSec` and `KillMode=control-group`, which bounds the
whole invocation and any remaining child process. The OS roster is capped at
eight endpoints and eight units; the global deadline may therefore end an
incomplete checkup rather than promise every probe completes. `MemoryMax=256M`
is retained from the existing unit; removing the model child reduces its demand
but does not claim a new observed peak or raise the limit.

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

`tools/core-checkup-witness.mjs ROSTER POLICY ARTIFACT_DIRECTORY` creates one uniquely
named transient *user* timer, scheduled one second ahead. It refuses any config
other than `allowRepair: false`, `luna: false`, and no wake transport. The
transient service has the same 180-second and 256 MiB limits as the proposed
persistent service. The helper retains a run-scoped config, events, journal,
and `core-checkup-witness/v1` receipt in the caller-provided artifact directory,
then stops and resets only its own timer and service. It is a one-shot test,
not installation or enablement of the 30-minute timer.

The final integrated witness is recorded in
`docs/witnesses/core-checkup-transient-cf7879-final-20260915/`. It used the
published source commit `701b101a8c53623a9d4f7dbbd846272a82d699cc`, a policy
with `allowRepair:false` and `wake.enabled:false`, and finished successfully.
It observed ouranos as a local address assigned to `yggTun`, and prometheus and
zeus through remote `yggTun` routes. The primary Claude Flow was an approval
wait, so no wake was eligible or attempted.


## Persistent activation gaps

The 30-minute unit source is ready but remains inactive. Its OS roster must provide
endpoints, units, and `allowRestart`; its separate generic policy must provide `eventLog.retention` and optional harness targets. The harness collector uses the existing exact Codex thread and Claude transcript adapters. It treats approval waits and unknown state as ineligible. The generic policy does not own a privileged unit or Lojix configuration. If either source is absent or invalid, the runner appends only `config/missing` or `config/invalid` to its own event path and exits non-successfully. Each invocation runs `claude agents --json`
fresh and maps `waiting` to ineligible; the CLI has no idle-since field, so every
idle duration remains `null` and wake remains suppressed. The supported app-server reader makes only `initialize`, `initialized`, `account/rateLimits/read`, and `account/usage/read` calls. It emits independent account, `codex_bengalfox` primary, and `codex_bengalfox` secondary windows with raw `usedPercent`, explicitly derived `remainingPercent`, exact `windowMinutes`, and UTC `resetsAt`. Claude quota is always `unknown` until its own supported reader exists. It never calls rate-limit-reset credit consumption. The OS/Horizon projection must
be materialized and evaluated, then the user-environment owner must install and
enable the source-controlled unit with an activation receipt. No current CriomOS
proposal has a source-bound materialization receipt, so this change does not claim
persistent activation.
