# Rescue terminal slice incident and repair

Date: 2026-06-05
Role: pi-operator

## What went wrong

The intended change was a dedicated rescue terminal and research-backed resource protection for the minimum desktop path needed to keep the computer operable.

The unsafe implementation overreached. It added Home Manager ownership of the standard user slices `session.slice` and `background.slice`. The dangerous one is `session.slice`: the live Niri compositor is under `session.slice`, along with user-session services such as the user D-Bus bus and PipeWire.

A live `HomeOnly Activate` then reconciled user systemd units. Reconciliation of a live slice that contains the compositor can stop or replace that slice, which terminates the compositor and logs the user out. That is a deploy bug and an unacceptable activation behavior, not normal `HomeOnly Activate` behavior.

## Current observed state after the incident

No leftover `lojix`, activation, or Home Manager deployment process was visible after the logout.

The active home profile did contain Home-managed files for both `session.slice` and `background.slice`. That confirms the local profile was left in the unsafe shape from the prior activation.

The current live UI cgroup layout showed these critical components:

- `niri.service` under `session.slice`: compositor and window manager; absolutely critical.
- `dbus-broker.service` under `session.slice`: user session bus; critical for desktop IPC.
- `pipewire.service` and `wireplumber.service` under `session.slice`: audio/media; useful for full session health, not the first survival target.
- `quickshell` / Noctalia under an `app.slice` transient app scope: shell/panel/launcher surface; critical for normal desktop operation.
- `mako` under an `app.slice` transient app scope: notifications; useful but not core recovery.
- `xdg-desktop-portal*` and permission/document portal services: app integration; useful for normal session operation.
- Ghostty app scopes under `app.slice`: ordinary terminals; should not all be boosted because agent/build children live under them.

## Immediate repository repair

The repaired Home profile removes all Home Manager ownership of `session.slice` and `background.slice`.

The rescue terminal remains, but only as a specific launch path:

- Niri binding: `Mod+Ctrl+Return`.
- Command: `criomos-rescue-terminal`.
- Launch mechanism: a fresh transient `systemd-run --user --scope` for the rescue terminal instance.
- Resource policy is attached to that transient scope, not to the live parent desktop slice.

The repaired profile evaluates with no declared `systemd.user.slices` entries, while retaining the rescue terminal binding and the reusable Nix-store redaction helper.

## What not to do now

Do not run another live `HomeOnly Activate` from the unsafe profile path while the current graphical session matters. A corrected repository commit prevents future pinned profiles from carrying the broad slice ownership, but activation of the transition away from the bad generation still needs a safe method because the current active Home generation already contains the bad slice unit files.

Safe cleanup options need to be chosen deliberately:

- activate only from a logged-out or throwaway graphical session;
- use a Home activation mode that updates files but does not stop/restart user units, if verified;
- or handle the stale user slice files manually with a tested non-disruptive path.

The next activation should be treated as a recovery step, not a normal profile update.

## Next design direction

The desktop survivability design should favor specific recovery components, not broad live slices:

- protect the compositor/session path without making Home Manager own `session.slice`;
- protect Noctalia/Quickshell launcher/shell through a specific transient scope or a stable app-unit policy that does not restart it under the active session;
- protect one rescue terminal only, not all Ghostty terminal scopes;
- demote future agent/build/deploy workloads into explicit background/workload scopes;
- add pressure visibility and kill controls for those workload scopes.

This preserves the original goal: the user can still operate the computer during resource pressure, inspect what is happening, and close or kill heavy work without the resource policy itself becoming a logout hazard.
