# Core checkup

`systemd/user/core-checkup.{service,timer}` is a source-controlled user-unit payload. Deployment must materialize `config.json` from the active projection: it supplies the actual Ygg endpoints, allowlisted owned units, liveness facts, and quota reading. The job never invents addresses or executes model-produced commands.

The default is observation. A restart requires all of `allowRepair`, `owned`, and `allowRestart`; it occurs once when a unit first enters a failed episode and is recorded as a scalar event. The guard clears after an active observation. Message process/socket liveness is distinct from semantic health; semantic health remains `unverified` without a supported runtime API. Wake results are `accepted` or `undelivered`; a failed wake is never repair evidence.
