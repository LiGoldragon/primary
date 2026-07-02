# Listener Live Smoke Evidence

## Task And Scope

Tracker item: `primary-acmr.6`.

Scope was the requested live production-trial smoke test for Listener after the
internal transcription and status-bar integration. The approved target was the
`goldragon` cluster, `ouranos` node, user `li`, with CriomOS commit
`731d999fb1fcc9f78b79e9cd92a0bff033377037` pinning CriomOS-home
`a4adfc961f06cbbc84ebd59201c4a706e399c388` and Listener `0.4.0`.

No source code was edited. No secret value was printed or recorded. Transcript
text from a live daemon reply was not included here.

## Result

Result: **blocked**.

The live `meta-lojix` command rejected the current documented
`UserEnvironment` deployment request shape before any build, activation, profile
mutation, user-unit reload, Noctalia reload, or service restart occurred. The
loaded operating-system doctrine requires the current direct `meta-lojix`
interface and forbids falling back to retired deploy names, so the audited
Listener `0.4.0` Home profile could not be activated safely in this run.

Because activation was blocked, the real spoken microphone-to-clipboard test
was not run and the visual status-bar success path was not claimed.

## Activation And Reload Actions

Planned transition:

- Target: `goldragon` / `ouranos` / `li`.
- Artifact kind: `UserEnvironment`.
- Requested action: `ActivateNow`.
- Source revision policy: immutable CriomOS ref
  `github:LiGoldragon/CriomOS/731d999fb1fcc9f78b79e9cd92a0bff033377037`.
- Builder: `None`.
- Rollback expectation: previous Home Manager/Lojix user-environment
  generation remains the rollback surface.

Command run:

```sh
meta-lojix "(Deploy (UserEnvironment (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/731d999fb1fcc9f78b79e9cd92a0bff033377037 ActivateNow RequireImmutable None [])))"
```

Result:

```text
(CliRejected [NOTA request did not decode: unknown DeployRequest variant UserEnvironment])
```

Interpretation:

- Admission failed before deployment side effects.
- I did not use the older `Home` deployment request shape because the active
  role packet says to use the current `UserEnvironment` interface and not use
  retired request names.
- I did not run Home Manager activation manually, restart Noctalia/QuickShell,
  run `niri msg action load-config-file`, or restart `listener.service` after
  the deploy-surface rejection.

## Live Pre-Activation Evidence

Observed facts:

- Host/session: `hostname` returned `ouranos`; `id -un` returned `li`;
  session variables reported Niri on Wayland with `XDG_RUNTIME_DIR` under the
  user runtime directory.
- `lojix "(Query (ByNode (goldragon ouranos None)))"` returned current
  historical user-environment entries through generation `31`, but this did
  not prove the audited Listener generation was active.
- `listener.service` was active before activation, but its running process was
  Listener `0.3.0`, not Listener `0.4.0`.
- The live profile resolved `listener-daemon` to Listener `0.3.0`.
- `systemctl --user cat listener.service` showed the generated unit still used
  an `EnvironmentFile` and an `ExecStart` wrapper, and the old active runtime
  had no Listener status stream.
- `$XDG_RUNTIME_DIR/listener/status.sock` was absent.
- `$XDG_RUNTIME_DIR/listener.sock` was present.
- Noctalia/QuickShell process was running, but the managed Noctalia plugin
  config contained `whisrs-level` and did not contain `listener-level`.
- `systemctl --user is-active listener.service` returned active; `noctalia.service`
  and `quickshell.service` were not active as systemd user services.
- Process inspection found a running QuickShell process.

Interpretation:

- The prerequisite "Listener service is from Listener `0.4.0`" failed.
- The prerequisite "status socket exists after daemon start" failed.
- The prerequisite "Listener widget is visible beside Whisrs" was not met from
  the active config; only Whisrs was configured.
- The live state was too old for the approved `primary-acmr.6` smoke test.

## Microphone Evidence

Observed facts:

- `pactl get-default-source` returned a USB wireless microphone source.
- `pactl list sources` showed that source in `RUNNING` state and not muted.

Interpretation:

- A real microphone source was available, but it was not used for the approved
  smoke test because the audited Listener deployment was not active.

## Clipboard And Transcript Handling

An attempted probe against the old Listener command path returned a terminal
reply from the existing `0.3.0` daemon and delivered to the system clipboard.
That result is explicitly **not** acceptance evidence because it used the old
runtime before audited activation. The transcript text from that reply is not
included in this report.

No clipboard contents were printed or reported.

## Visual Status-Bar Evidence

Observed facts:

- The active Noctalia plugin configuration contained `whisrs-level`.
- The active Noctalia plugin configuration did not contain `listener-level`.
- `$XDG_RUNTIME_DIR/listener/status.sock` was absent.

Interpretation:

- Red recording level, yellow transcribing state, and copied notification could
  not be validly observed for Listener `0.4.0` in this run.

## Whisrs Preservation Evidence

Observed facts:

- `whisrs status` returned idle.
- `whisrs.service` was active.
- The active Noctalia plugin configuration still contained `whisrs-level`.
- `niri validate` reported the current config is valid.
- The active Niri config still contained Whisrs bindings for `Mod+V`,
  `Mod+Shift+V`, `Mod+Alt+V`, and `Mod+Ctrl+V`.

Interpretation:

- Whisrs remained present and operational in the pre-activation live session.

## Tracker Impact

`primary-acmr.6` remains blocked on live deployment/activation of the audited
generation through the current Lojix deploy interface, or an explicit updated
operator instruction that reconciles the deployed Lojix daemon's accepted schema
with current doctrine.

`primary-jwx0` cannot be unblocked or closed. Its successor smoke-test evidence
does not exist yet.

`primary-c8w0` cannot start. The production-trial readiness closeout still
depends on successful `primary-acmr.6` evidence or a resolved blocker.

## Commands Consulted

- `spirit "(PublicTextSearch [listener transcription status bar])"` returned no
  matching public record; the task brief and tracker acceptance criteria were
  used as authority.
- `bd show primary-acmr.6 --json` confirmed the requested acceptance criteria
  and that it blocks `primary-jwx0`.
- `bd show primary-c8w0 --json` confirmed readiness closeout depends on
  `primary-jwx0`.
- `lojix "(Query (ByNode (goldragon ouranos None)))"` listed current historical
  generations through `31`.
- `systemctl --user status listener.service --no-pager` showed Listener
  `0.3.0` active before activation.
- `systemctl --user cat listener.service` inspected the active generated user
  unit without printing secrets.
- `test -S "$XDG_RUNTIME_DIR/listener/status.sock"` found no status socket.
- `rg -n "listener-level|whisrs-level" ~/.config/noctalia ~/.config/quickshell
  ~/.config/systemd/user/listener.service` found `whisrs-level` only.
- `pactl get-default-source` and focused `pactl list sources` inspection
  confirmed the default microphone source was present and not muted.
- `whisrs status` and `systemctl --user status whisrs.service --no-pager`
  confirmed Whisrs remained active and idle.
- `niri validate` reported the config was valid.
- Focused active Niri config search confirmed Whisrs bindings for `Mod+V`,
  `Mod+Shift+V`, `Mod+Alt+V`, and `Mod+Ctrl+V`, plus the existing old Listener
  `Mod+Alt+L` binding.

## Follow-Up Requirement

Resolve the deploy-surface mismatch before rerunning the smoke test. The next
attempt must first make the audited Listener `0.4.0` Home profile active, reload
the user systemd manager, restart `listener.service`, restart or reload
Noctalia/QuickShell so `listener-level` is loaded, and only then ask the
operator for a real non-private spoken phrase.
