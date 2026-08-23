# Ouranos Lojix self-upgrade: partial activation result

The corrected immutable Evaluate (deployment 32) and Realize (33) succeeded.
The one authorized PID-1-owned ActivateNow self-switch (34) terminally failed
at activation.

PID 1 nevertheless changed the persistent and live system links to generation
164 and restarted Lojix as 0.18.0. The service is healthy, its nine-field
startup writer has no timeout, its sockets and SSH remain healthy, and
`bootctl list` marks generation 164 as default.

The transient failed because `complex-init.service` failed during candidate
`switch-to-configuration switch`, with a ClaviFaber Dotos-decoding error.
Lojix therefore records deployment 34 as
`Failed.(Activate ActivationFailed)`, not Current. `bootctl status` and
`bootctl list` disagree about the default-entry projection, so both are
preserved as observations.

No retry, reboot, reset, garbage collection, hot fix, user-environment
deployment, or recovery action was taken. Further action needs explicit
authority for this live-system/ledger divergence and the failed service.

## Sources

- [execution witness](../witnesses/ouranosLojixSelfUpgradeExecution.md)
- [self-upgrade plan](lojixSelfUpgrade.md)
- [stale deployment diagnosis](ouranosStaleDeployments.md)
