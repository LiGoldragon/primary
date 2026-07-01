# PrimaryJwx0 Operating System Implementer Evidence

## Task And Scope

Tracker item `primary-jwx0` requested the first real Listener microphone-to-clipboard smoke test on the target host. The test was allowed to use safe Home activation and an explicit Niri reload, but was not allowed to simulate real transcription success.

Target:

- cluster: `goldragon`
- node: `ouranos`
- user: `li`
- artifact kind: current HomeOnly/user-environment profile, deployed as Lojix generation 29
- requested local state transition: activate the already-current Home Manager profile and reload Niri config
- source revision policy: no new deploy or build; use the current deployed profile
- builder: none
- rollback expectation: activate an earlier Home Manager generation or start a fresh session on an earlier profile if the live activation caused user-session trouble

## Context Consulted

- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PrimaryId8a/NixAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- Tracker item `primary-jwx0`
- Tracker item `primary-c8w0`
- Local operating-system, work-tracking, secrets, and version-control doctrine

## Commands And Actions Run

- `bd show primary-jwx0 --json`
- `bd show primary-c8w0 --json`
- `bd update primary-jwx0 --claim --json`
- `lojix "(Query (ByNode (goldragon ouranos None)))"`
- active and deployed profile executable probes for `listener`, `listener-daemon`, `listener-toggle-capture`, `whisrs`, and `whisrs-recall`
- `systemctl --user cat listener.service`
- `systemctl --user cat whisrs.service`
- `systemctl --user is-active listener.service`
- `pactl get-default-source`
- `pactl list sources` for the default source state, description, and mute state
- `niri validate`
- `niri msg version`
- Home Manager activation: `~/.local/state/nix/profiles/home-manager/activate`
- Niri reload: `niri msg action load-config-file`
- Listener status probe: `listener status`

## Observed Facts

- Date and host: `2026-07-01T19:02:45+02:00`, user `li`, host `ouranos`.
- Lojix reports generation 29 as current for `goldragon/ouranos` HomeOnly state.
- Before local activation, the deployed Home Manager profile contained Listener binaries, but the active shell path and active user systemd state did not expose Listener.
- Home Manager activation completed successfully and started `listener.service`.
- After activation, the active shell path sees `listener`, `listener-daemon`, `listener-toggle-capture`, `whisrs`, and `whisrs-recall`.
- After activation, `systemctl --user cat listener.service` succeeds; the unit has an optional `%h/.config/listener/environment` environment file and an ExecStart for `listener-daemon`.
- `listener.service` is active after activation.
- `listener status` reports idle after activation.
- Active Niri config validates successfully.
- Active Niri config contains `Mod+Alt+L` for `listener-toggle-capture toggle`.
- Active Niri config still contains Whisrs bindings for `Mod+V`, `Mod+Shift+V`, `Mod+Alt+V`, and `Mod+Ctrl+V`.
- `niri msg action load-config-file` returned success, so the running compositor was explicitly reloaded after activation.
- The system default source is present, running, and not muted. Its description is `Wireless Microphone RX Analog Stereo`.
- `~/.config/listener/environment` is absent.
- The current shell does not export `LISTENER_TRANSCRIPTION_PROGRAM`.
- The deployed `environment.example` names `LISTENER_TRANSCRIPTION_PROGRAM` as the real transcription configuration point.

## Smoke-Test Result

Result: blocked.

The real microphone-to-clipboard smoke test was not started because proof condition 3 failed: no `LISTENER_TRANSCRIPTION_PROGRAM` or equivalent real STT backend configuration was present. Starting and stopping capture without that backend would only exercise the explicit not-configured path, not a real transcript.

Tested conditions:

- Condition 1, live environment sees Listener from deployed Home profile: pass after Home activation.
- Condition 2, running compositor/session sees `Mod+Alt+L`: pass after Niri config validation and explicit `niri msg action load-config-file`.
- Condition 3, real STT backend configured and usable: blocked; no configured backend was present.
- Condition 4, deployed toggle captures system default microphone: not attempted after the STT blocker. Precondition evidence shows the default microphone source exists, is running, and is not muted.
- Condition 5, stopping capture sends real transcript to clipboard: not attempted after the STT blocker.
- Condition 6, Whisrs remains usable or present and not overwritten: pass for preservation evidence; active path, service, and all four configured bindings remain present.

## Blocker

Precise blocker: Listener lacks real STT configuration in the live user environment.

Exact condition needed: create a non-secret-reportable `~/.config/listener/environment` or equivalent live service environment that defines `LISTENER_TRANSCRIPTION_PROGRAM` to a usable real transcription program. Any credentials consumed by that program must remain in the secret store or the program's private runtime environment and must not be copied into reports, chat, or commits.

Expected proof after the blocker is cleared:

- `listener.service` is restarted or otherwise receives the configured backend.
- `listener status` is idle before capture.
- Pressing `Mod+Alt+L` or running the deployed `listener-toggle-capture toggle` starts capture from the system default microphone.
- Pressing the binding or toggle again stops capture.
- The system clipboard receives the spoken test phrase or expected test text. The phrase content should not be copied into public evidence if private; evidence should report only that the expected text was present.

## Tracker And Downstream State

`primary-jwx0` should remain open and blocked until real STT configuration is present and the capture/clipboard proof is completed.

`primary-c8w0` cannot start yet because it depends on the smoke-test result or precise blocker from `primary-jwx0`; this evidence provides the blocker but not a completed real smoke-test pass.

## Checks Not Run

- No Listener capture was started.
- No real audio transcript was generated.
- No clipboard content was read or reported.
- No follow-on crash durability or policy work was started.
