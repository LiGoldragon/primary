# Core checkup

`systemd/user/core-checkup.{service,timer}` is a source-controlled user-unit payload. Deployment must materialize `config.json` from the active projection: it supplies the actual Ygg endpoints, allowlisted owned units, liveness facts, and quota reading. The job never invents addresses or executes model-produced commands.

The default is observation. A restart requires all of `allowRepair`, `owned`, and `allowRestart`; it occurs once when a unit first enters a failed episode and is recorded as a scalar event. The guard clears after an active observation. Message process/socket liveness is distinct from semantic health; semantic health remains `unverified` without a supported runtime API. Wake results are `accepted` or `undelivered`; a failed wake is never repair evidence.

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
evaluated. Codex's supported app-server account read returned 55% remaining;
the same API has no Claude reading.

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
