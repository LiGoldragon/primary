# Listener desktop integration handover

## Purpose

Carry only the current Listener desktop experience into a fresh context. The next work is to restore dependable delivery feedback and add a lightweight network connection widget without weakening cancellation, privacy, or responsiveness.

## Current user-visible behavior

- Active deployment: Listener `0.13.0`, signal-listener `0.8.0`, meta-signal-listener `0.3.0`, user generation `145`.
- `listener.service` is active. The installed CLI accepts a single schema-defined NOTA object; positional and legacy command forms are rejected.
- Effective Niri shortcuts are:
  - `Mod+C`: `Start.{}` starts capture.
  - `Mod+V`: the stop helper submits `Stop.<active-session>` for graceful completion, then asynchronous finalization, transcription, and clipboard delivery.
  - `Mod+Ctrl+C`: the cancel helper submits `Cancel.<active-session>` and discards the active capture.
  - `Mod+Alt+V` opens Listener recall.
- The active Noctalia bar has the Listener widget in its right section. It consumes the Listener status socket and renders recording, finalizing, transcribing, cancelling, cancelled, delivered, and error states.

## Settled invariants

- Human CLI input is exactly one schema-defined NOTA request object, such as `Start.{}`, `Stop.<session>`, or `Cancel.<session>`; no positional or legacy form is supported.
- Graceful completion is asynchronous. The daemon promptly replies with `CompletionRequested`, then finalizes, transcribes, and delivers in background actor work.
- Explicit cancellation suppresses transcript delivery. This remains true when cancellation races finalization or transcription: cancellation must not publish `delivered`, write transcript history, or reach the clipboard path.
- Clipboard delivery is the configured output target. The `delivered` status is published only after the delivery outcomes succeed; failure produces `error`.
- Listener status traffic is state/level only. Do not casually put transcript or excerpt text on this socket.
- Transcript excerpts are private desktop-only material. Never put them in logs, persistent files, source comments, reports, chat, test output, status streams, telemetry, or real test fixtures.
- Desktop integrations must be push/event-driven where possible. Do not introduce frequent shell polling, heavyweight status scans, or radio scans.

## Verified source and component map

Source revisions can move; use these paths as the durable owners and re-check their current revision before editing.

| Surface | Owner and locator | Confirmed responsibility |
|---|---|---|
| Listener CLI | `LiGoldragon/listener`, `src/command.rs` | Parses one NOTA request into `signal_listener::Input`; rejects flags, missing/multiple arguments, and positional commands. |
| Listener lifecycle | `LiGoldragon/listener`, `src/daemon.rs`, `src/runtime.rs`, `src/status.rs` | Actor-owned completion/cancellation work, `CompletionRequested`/`CancellationRequested`, status publication, and the cancellation gates that precede delivery. `tests/runtime.rs` covers cancellation during finalization and transcription without delivery. |
| Clipboard delivery | `LiGoldragon/listener`, `src/delivery.rs` | Dispatches `SystemClipboard` through the configured clipboard program (`wl-copy` by default). |
| Ordinary Listener contract | `LiGoldragon/signal-listener`, `schema/lib.schema` | Defines Start, Stop, Cancel, Status, Toggle, `CompletionRequested`, `CancellationRequested`, delivery outcomes, and typed operations/replies. |
| Privileged Listener contract | `LiGoldragon/meta-signal-listener`, `schema/lib.schema` and `src/lib.rs` | Owner/meta configuration surface; it is not the ordinary desktop-control path. |
| Listener service, helpers, bindings | `LiGoldragon/CriomOS-home`, `modules/home/profiles/min/dictation.nix` | Packages Listener; configures the user service; owns `listener-stop-capture` and `listener-cancel-capture`; defines `Mod+C`, `Mod+V`, `Mod+Alt+V`, and `Mod+Ctrl+C`. |
| Current bar and plugin installation | `LiGoldragon/CriomOS-home`, `modules/home/profiles/min/sfwbar.nix` | Despite its historical filename, this owns the active Noctalia bar layout, installs `libnotify`, enables the `listener-level` plugin, and maps its QML into the managed Noctalia plugin directory. |
| Dictation bar widget | `LiGoldragon/CriomOS-home`, `modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml` and `manifest.json` | Connects to `$XDG_RUNTIME_DIR/listener/status.sock`, parses newline JSON, uses `notify-send` on a `delivered` state transition, and colors `delivered` green. It has no explicit short success-flash lifecycle. |
| Desktop startup | `LiGoldragon/CriomOS-home`, `modules/home/profiles/min/niri.nix` | Starts Mako and Noctalia/QuickShell; the live QuickShell process is present. |
| Existing focused checks | `LiGoldragon/CriomOS-home`, `checks/listener-dictation-bindings/default.nix` and `checks/listener-level-widget/default.nix` | Pin the binding meanings, schema-only helper calls, cancellation distinction, widget states, plugin registration, notification invocation, and absence of transcript/text handling in the widget. |
| Existing older network configuration | `LiGoldragon/CriomOS-home`, `modules/home/profiles/min/waybar.nix` | Contains a Waybar network display based on percentage. The active bar is Noctalia, so this is precedent only, not the default implementation target. |

Live inspection confirmed the active Niri configuration uses the three stated Listener shortcuts and an installed `listener-0.13.0` executable; the active bar registers `plugin:listener-level`. The live deployment query includes generation `145`. Published source versions match the stated Listener, signal-listener, and meta-signal-listener versions.

## Desired next behavior

### Delivery notification and success feedback

The clipboard-delivery notification used to appear but no longer does. Treat the failure boundary as unknown. Diagnose, without presuming the cause, whether it is:

- no delivered event after actual clipboard success;
- widget socket/state-transition handling;
- `notify-send` invocation or environment;
- Mako/desktop notification service availability or permissions; or
- Noctalia/QuickShell plugin loading or integration.

The current widget does contain a `delivered` transition branch that calls `notify-send` with a generic delivery message. It also colors `delivered` green. These source facts do not prove that the notification was emitted or displayed in the affected user flow.

After diagnosis, restore a short green success animation/flash that begins only after successful transcription **and** clipboard delivery. Cancellation and every error path must never trigger it.

The desired notification needs an immediate content cue:

- The title is not settled. `Listener Clipboard:` is the current lean, but `Listener:`, `Listener into clipboard`, and similar wording remain live alternatives.
- The private body policy is not settled: either roughly the first 12 transcript words, or the first six plus the last six words.
- Do not decide title, truncation, punctuation, ellipsis behavior, or excerpt emission ownership by accident while fixing the regression.
- Keep any excerpt transient and desktop-local. In particular, do not copy it into the status socket, a durable history, diagnostics, or test evidence. Verify the chosen notification backend does not retain it in a history/log outside the intended transient desktop display.

### Network connection widget

Add a Noctalia-compatible network widget that reports the active connection truthfully:

- Ethernet active: show an Ethernet representation.
- Wi-Fi active: show a Wi-Fi icon, the actual radio value with its unit, a small meter, and a good/bad color scale that teaches the user how to read it.
- The likely truthful Wi-Fi measurement is RSSI/signal in dBm, not a synthesized percentage and not “color temperature.” A read-only live probe through `iw dev <wireless-device> link` exposed `signal: -57 dBm`; treat the number as dynamic evidence that this source is available, not as a threshold or persistent fact.
- NetworkManager is active and the default route currently selects a Wi-Fi device. This is an observation only; it does not settle the widget’s multi-link policy.

No custom Noctalia network plugin currently exists beside the Listener plugin. The likely ownership area is the same Noctalia/plugin integration route, but confirm the component boundary before adding one.

## Acceptance criteria for the next implementation

1. A real successful completion produces one visible desktop notification and one short green success feedback event after clipboard delivery, not merely after capture stop or transcription start.
2. The notification title/excerpt behavior matches an explicit decision. Its body contains only the chosen transient excerpt and never appears in logs, persistence, status IPC, or durable automated evidence.
3. Cancel during recording, finalization, and transcription yields no delivery, no success notification, and no green success feedback. Error and clipboard-failure paths do the same.
4. The existing shortcuts retain their exact meanings and use schema-defined NOTA requests only.
5. The network widget distinguishes Ethernet, Wi-Fi, and disconnected states; Wi-Fi displays the selected real metric with its unit, meter, and documented color thresholds.
6. Widget updates come from event/subscription data or bounded lifecycle reconnects, not periodic shell commands, connection scans, or transcript-bearing polling.
7. Existing Listener widget, binding, and desktop integration checks still pass; new checks cover all new state and privacy boundaries.

## Privacy and resource constraints

- Never inspect, save, quote, or assert against a real transcript while diagnosing this work. Use generated non-personal test tokens only where text-selection behavior must be tested, and keep them out of test logs.
- Do not send transcript text across the Listener status socket merely to let QML compose a notification. A text-bearing IPC change is a contract/privacy decision, not an incidental widget edit.
- Do not use `dbus-monitor`, journal captures, or similar broad logging while a notification body may contain a transcript excerpt.
- Keep Listener’s existing socket-driven status model. The widget’s reconnect timer is recovery behavior, not a reason to add polling.
- Prefer NetworkManager/D-Bus or another native event source for connection changes. If `iw` is used for RSSI, bound reads to the selected active Wi-Fi interface and update only on meaningful connection/signal events or a consciously justified low-rate refresh; do not scan networks.

## Open decisions and questions

1. Which process owns notification emission after diagnosis: the Listener daemon at confirmed delivery, the widget after a status event, or another narrowly scoped desktop bridge? How can it receive a private excerpt without widening a status/wire surface?
2. Which notification title is wanted, and which body truncation rule is wanted: first ~12 words or first six plus last six?
3. Does the active notification stack guarantee a transient private body, or does it maintain history/logging that requires a different mechanism or policy?
4. What precise event/state begins and ends the green feedback? Is the existing `delivered` state sufficient once its lifecycle is traced, or is a separate one-shot desktop event needed?
5. For several simultaneous links, what defines “active”: NetworkManager’s primary connection, the device carrying the default route, or another explicit policy? How should VPN/tunnel links affect display?
6. What should disconnected, connecting, captive/no-route, and Ethernet-without-carrier states look like?
7. Which source is authoritative for Wi-Fi signal on this desktop, and what RSSI dBm thresholds map to good, fair, weak, and bad? Do not label a percentage conversion or arbitrary colors as the metric.
8. Is a continuously updating RSSI display required, and if so what event-driven or bounded-refresh mechanism is acceptable without a shell-polling loop?

## Suggested dependency order

1. Trace the current success path end-to-end with a private-safe, human-observed completion: Listener delivery outcome, status event, widget connection/state transition, `notify-send`, Mako, and visible desktop result. Record only component outcomes, never notification body text.
2. Choose the notification emitter and private excerpt boundary, then obtain explicit decisions for title and truncation. Escalate before adding a transcript-bearing IPC/schema surface.
3. Implement and test the restored notification plus one-shot green success feedback against delivered, cancelled, and error states.
4. Define the network state model and authoritative source/thresholds, then add the independent Noctalia widget and bar registration.
5. Run focused Nix checks, deploy through the normal home path only when authorized, reload Niri/Noctalia as required, and perform privacy-safe live acceptance observation.

The notification work and network widget can share the Noctalia integration surface but should remain separate components after the common bar/plugin ownership is understood.

## Concrete verification plan

### Source and Nix checks

- Preserve and run `listener-dictation-bindings` and `listener-level-widget`; extend them to pin any new notification success/cancel/error rule without embedding transcript text.
- Add a focused check for the network widget’s registration, Ethernet/Wi-Fi/disconnected rendering model, dBm unit, threshold legend, and no shell polling/scanning command.
- Run the relevant Listener runtime tests that cover asynchronous completion and cancellation during finalization/transcription; add a delivery-status test for the selected notification event boundary.
- Run the narrow named Nix checks first, then the relevant `nix flake check` surface after shared home/bar wiring changes.

### Private-safe live verification

- Confirm the active widget receives state events and that the notification service and QuickShell plugin are live before attempting a completion.
- With user-approved non-private speech, observe one successful delivery notification and green flash without recording or copying its text into terminal, logs, reports, screenshots, or test output.
- Cancel once while recording and once after graceful completion has begun; observe no notification, green feedback, clipboard delivery, or `delivered` status.
- Exercise an error or controlled clipboard-unavailable path without transcript disclosure; observe error feedback and no success behavior.
- Verify Wi-Fi and Ethernet presentation using connection-state fixtures or safe live changes where available; compare the displayed Wi-Fi dBm value with the selected radio source without recording SSID or other private network identifiers.

## Current evidence boundaries

- Read-only inspection was used. No product source, service, deployment, shortcut, widget, clipboard, audio, or transcript was changed.
- Normal coordination is operational for pickup.
- This handover intentionally omits unrelated coordination history and all transcript material.
