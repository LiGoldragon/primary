# ljk5 notification source candidate

## Candidate

- Base: published CriomOS-home main `08361fef939664f26b06b86b8cdf28512adc10f4`.
- Branch: `flow-1541ef-notification-fix`.
- Commit: `9c293d8b62cea98f85c6a7ed94457a515ccbd6cf`.
- Four edited files: the existing desktop-shell module and composition check, one event monitor, and its scenario test.

## Behavior

Mako now ignores every sender-requested timeout, including zero. Its normal surface duration is 3 seconds and its critical duration is 10 seconds.

Noctalia's freedesktop notification daemon is explicitly disabled and its built-in battery warning threshold is zero. Its bar continues presenting battery state.

The graphical-session `battery-notification` service listens to UPower property-change signals. It emits level-triggered warnings at 10, 5 and 2 percent through `org.freedesktop.Notifications`, replacing the held notification ID as the warning deepens. Charging, full-charge, pending-charge, absence, or UPower's AC state closes the held ID and re-arms the warnings. The service performs no polling and waits for the notification service's D-Bus ownership event.

## Narrow evidence

The composition check asserts Mako's timeout policy, Noctalia's disabled daemon/battery warning, and the graphical-session service. Scenario tests cover the 10/5/2 transitions, ID reuse, AC close, and a fresh ID after the next discharge. Nix parsing, Python compilation and `git diff --check` passed.

Prometheus built the final narrow check:

`/nix/store/gwm9v8ww5ngk0xc4qy1yb5m6dzqxxfiz-noctalia-settings-composition`

Log: `/home/li/primary/flows/1541ef/notification-fix/narrow-notification-build-final.log`.

## Remaining Noctalia notices

The deployed Noctalia source provides settings for its external notification daemon and battery warnings; both are off in this candidate. It provides no setting to disable its internal configuration-error and configuration-migration notices. Its manual IPC and debug notification creators likewise have no setting, but create nothing without an explicit call. Per Opus ruling, these paths remain unchanged tonight; no Noctalia source patch was introduced.

## Boundary

No main, consumer, activation, process, notification card, or live desktop state changed. Curriculum remains the sole naming integrator; Field owns any later realization and activation.
