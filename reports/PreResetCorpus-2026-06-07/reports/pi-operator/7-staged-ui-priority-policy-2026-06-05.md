# Staged UI priority policy implementation

Date: 2026-06-05
Role: pi-operator

## Implemented but not deployed

CriOMOS-home now has a staged, component-specific UI priority module at:

- `modules/home/profiles/min/ui-priority.nix`

It is imported by `modules/home/default.nix` and is enabled only for Horizon `edge` desktop roles.

No live Home activation, Niri reload, or deployment was run while implementing this.

## What the module installs

The module installs two commands:

- `criomos-ui-priority-apply`
- `criomos-ui-priority-status`

It also declares a oneshot user service:

- `criomos-ui-priority.service`
- wanted by `graphical-session.target`

The service is intended to run after the graphical session exists and apply runtime resource properties to specific units/scopes.

## Safety boundary

The module does not declare `systemd.user.slices` and does not own `session.slice` or `background.slice`.

The apply command uses:

- `systemctl --user set-property --runtime`

That means it applies runtime cgroup properties to already-existing units/scopes instead of writing persistent drop-ins for live parent slices or restarting the compositor.

## Components targeted

Stable user services targeted by name:

- `niri.service`
- `dbus-broker.service`
- `xdg-desktop-portal.service`
- `xdg-desktop-portal-gtk.service`
- `xdg-document-portal.service`
- `xdg-permission-store.service`
- `pipewire.service`
- `wireplumber.service`

Transient app scopes targeted by process command-line discovery:

- Noctalia / QuickShell
- Mako

The rescue terminal remains protected independently by its own transient `systemd-run --user --scope` launch path and `Mod+Ctrl+Return` Niri binding.

## Validation performed

Repository-only validation was performed:

- Nix parse for the new module and aggregate module passed.
- CriOMOS evaluation with local CriOMOS-home override showed:
  - UI-priority apply package present.
  - UI-priority status package present.
  - `criomos-ui-priority.service` present.
  - `Mod+Ctrl+Return` rescue binding present.
  - `systemd.user.slices` remains empty.
- CriOMOS Home activation package build passed with local CriOMOS-home override.
- Generated apply/status scripts passed `bash -n` syntax checks.

No live application of the policy was performed.

## Remaining deployment warning

The active running Home profile had previously been activated with bad generated user slice files. Main is repaired and now has staged component-specific policy, but the next live activation should still be treated as a recovery/safety operation. Do not run it in an active high-value agent session without a deliberate safe window.
