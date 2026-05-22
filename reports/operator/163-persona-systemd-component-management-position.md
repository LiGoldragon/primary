# 163 - Persona systemd component management position

## Summary

Psyche clarified that Persona will be a permissioned system daemon and
asked whether it should use systemd units to manage component daemons.

Operator position: yes. In production, Persona should use systemd as
the process-control substrate for component daemons. Persona remains
the authority brain: it owns the desired component graph, active-version
selector, upgrade protocol, handover state, and event log. systemd owns
process creation, cgroups, restart mechanics, socket/unit permissions,
and sandboxing.

## Boundary

Persona should not become a raw long-running process launcher for
production. The current in-process launcher is still useful for tests
and early sandbox work, but a permissioned system daemon has a better
production primitive available: systemd already knows how to start,
stop, restart, supervise, isolate, and account for daemons.

The split should be:

- Persona decides which component version should run.
- Persona drives `signal-version-handover` over component upgrade
  sockets.
- Persona records `UpgradePrepared`, `ActiveVersionChanged`,
  `VersionQuarantined`, and future recovery events in manager storage.
- Persona asks systemd to start, stop, or restart the concrete component
  unit.
- systemd owns unit lifecycle, cgroups, logs, restart policy, process
  identity, and file/socket permission setup.

This keeps the root authority in Persona while using the operating
system's native supervisor instead of reimplementing it.

## Unit Shape

The clean production shape is a systemd template unit per component
version:

```text
persona-component@<component>:<version>.service
```

For the first Spirit cutover this can be simplified to concrete units
or a component-specific template, but the target model should preserve
component and version as unit identity.

Example conceptual mapping:

```text
persona-component@persona-spirit:v0.1.0.service
persona-component@persona-spirit:v0.1.1.service
```

Each unit runs exactly one component daemon version with a NOTA
configuration argument or a generated config file path if the existing
daemon still needs a file-shaped configuration. The daemon still
speaks its normal ordinary, owner, and private upgrade sockets.

The unversioned public selector should not be a shell alias. Persona's
active-version selector is the authority. Systemd may expose stable
socket paths, but Persona decides which version owns the public path
or which proxy/router maps public traffic to the active version.

## Persona Implementation Shape

Inside Persona, add a data-bearing actor such as `SystemdUnitManager`
or `ComponentUnitManager`. It should own a typed trait boundary:

```text
UnitController::start(ComponentUnit)
UnitController::stop(ComponentUnit)
UnitController::restart(ComponentUnit)
UnitController::status(ComponentUnit)
```

Production implementation uses systemd D-Bus. Tests use a fake
controller. This lets Nix tests prove Persona's orchestration without
requiring a mutable host systemd instance.

The existing process launcher remains useful as a sandbox controller
or test controller. It should not be the production management path
for a permissioned system daemon.

## Upgrade Flow

For a no-downtime component upgrade, Persona should eventually drive:

1. Ask systemd to start the next-version component unit.
2. Wait until the next daemon's private upgrade socket is available.
3. Ask main and next for handover markers.
4. Require marker parity before freezing main.
5. Ask main to enter readiness.
6. Complete handover, or recover main if completion fails.
7. Append `ActiveVersionChanged` only after finalization.
8. Ask systemd to stop or retire the old unit after the confidence
   window, or keep it private-upgrade-only if mirroring/recovery needs
   it.

This fits the code that landed today: Persona already drives the socket
protocol and records selector changes only after finalization. The
missing production slice is systemd-backed next-unit startup and
retirement.

## Permission Model

Persona should not need unrestricted root behavior. The intended
production permission is narrower:

- Persona runs as a system daemon with authority to manage only
  Persona-owned component units.
- Component daemons can run under dedicated users or constrained
  DynamicUser-style identities.
- Unit files and socket paths carry the OS permission boundary.
- Emergency owner operations still arrive through Persona's owner
  socket and become explicit event-log facts.

The exact PolicyKit/systemd authorization shape is system-specialist
surface, but the implementation should assume a restricted
systemd-management authority rather than ambient root.

## Operator Recommendation

Proceed with a systemd-backed unit manager abstraction in Persona.
Keep the current direct process launcher for Nix sandbox tests and
early non-host integration, but make it one implementation of the
unit-control interface rather than the production path.

No new psyche design decision is needed for the high-level question:
yes, systemd is the right daemon-management substrate for a
permissioned Persona daemon. The remaining decision is implementation
detail for system-specialist: whether production uses concrete units
first or jumps directly to template units.
