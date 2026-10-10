# Ouranos ClaviFaber recovery: partial activation result

The fixed immutable source passed Evaluate (35) and Realize (36). Its single
authorized ActivateNow request (37) is durably terminal
`Failed.(Activate ActivationFailed)`.

The candidate system did switch live and persistently to generation 165.
`complex-init.service` now succeeds, and the public ClaviFaber publication
artifact exists with root ownership and mode 0644. Lojix remains healthy at
0.18.0 with its nine-field, timeout-free startup configuration.

The PID-1 transient journal says the switch completed, then the transient
returned status 1. Lojix's durable terminal record therefore disagrees with
the healthy live system. `bootctl list` marks generation 165 default while
`bootctl status` still names generation 153 as its default entry. No recovery
action was taken.

## Sources

- [recovery witness](../witnesses/ouranosClaviFaberRecovery.md)
- [previous partial activation result](ouranosLojixSelfUpgradeFinal.md)
