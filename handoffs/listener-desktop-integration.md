# Listener desktop integration handover

## Goal

Complete and verify Listener desktop integration only:

- clipboard-delivery notifications with a private transcript cue;
- one-shot green success animation;
- separate lightweight active-network widget;
- deployment and private-safe real-world verification.

Do not broaden into unrelated coordination or operating-system work.

## Psyche vision and approved behavior

- Current shortcuts retain their meanings:
  - `Mod+C` starts recording.
  - `Mod+V` completes, transcribes, and delivers.
  - `Mod+Ctrl+C` cancels and discards.
  - `Mod+Alt+V` opens Listener recall.
- Human CLI input remains exactly one schema-defined NOTA object. Positional and legacy arguments are forbidden.
- Graceful completion acknowledges promptly, then finalizes, transcribes, and delivers asynchronously.
- Cancellation suppresses transcript history, clipboard delivery, notification, and success animation.
- Success notification ownership is in the Listener daemon after clipboard delivery succeeds.
- Notification title is exactly `Listener Clipboard:`.
- For more than 12 whitespace-delimited words, the body is the first six words, ` … `, and the last six words. A transcript of 12 words or fewer is shown whole.
- Transcript text does not enter the Listener status socket, logs, journals, reports, comments, test output, telemetry, persistent notification history, or process arguments.
- Mako history is disabled only for app-name `Listener`.
- The Listener widget owns only a 700 ms one-shot green success flash on the delivered transition. It does not emit the notification.
- The network widget is separate from Listener.
- Network representation follows NetworkManager’s primary physical connection. Simultaneous Ethernet/Wi-Fi shows the primary one. VPN remains a badge over the underlying physical link.
- Network states distinguish connecting, limited/no-route, captive, failed/auth, and disconnected.
- Wi-Fi shows truthful RSSI and `dBm`, with:
  - Good: >= -55 dBm, green
  - Fair: -56..-67 dBm, yellow
  - Weak: -68..-75 dBm, orange
  - Bad: <= -76 dBm, red
- NetworkManager D-Bus signals drive state. A non-scanning `iw dev IFACE link` read runs no more often than every five seconds and only while primary Wi-Fi is active. RSSI expires after 30 seconds.
- No real transcript contents, SSID, or network identity should be inspected or quoted.

## Verified repository state

### Listener

- Repository: `LiGoldragon/listener`
- `main` is pushed at `80b71730bc5e56230877d45da3af6a2dc9204621`.
- Direct freedesktop notification D-Bus emission is implemented without transcript process arguments.
- The production D-Bus message test verifies destination, object path, interface, method, no-reply flag, argument signature/order/types, app name, title/body, empty actions, transient hint, and 2500 ms expiry.
- Finalization has an atomic lifecycle boundary: `Cancellable -> CancellationRequested | DeliveryOwned`.
- Deterministic tests prove cancellation before delivery ownership prevents history, delivery, notification, and delivered status; cancellation after ownership truthfully reports completion ownership.
- Final Rust audit found no blocking or medium findings.
- Strict clippy still reports one pre-existing unrelated `collapsible_if` in `src/daemon.rs:947`.

### CriomOS-home

- Repository: `LiGoldragon/CriomOS-home`
- `main` and `main@origin` are pushed at `62d3d68a3153`.
- The lock pins Listener `80b71730bc5e56230877d45da3af6a2dc9204621`.
- Listener desktop changes include:
  - exact Mako app-name `Listener` history exclusion;
  - removal of widget-owned `notify-send` success notification;
  - 700 ms one-shot green delivered flash;
  - unchanged Listener shortcut and schema-only NOTA checks.
- Active Network is a separate Noctalia plugin.
- A systemd user helper consumes NetworkManager D-Bus signals and publishes NDJSON at `$XDG_RUNTIME_DIR/active-network/status.sock`.
- The helper uses a runtime directory mode of 0700 and socket mode of 0600.
- D-Bus loss fails the helper so `Restart=on-failure` with `RestartSec=2s` recreates it.
- Client output is bounded to latest-state delivery with a one-second drain timeout and slow-client eviction.
- QML uses an executable shared JS semantic validator and rejects malformed enum/numeric/state combinations.
- Tests cover malformed `kind` and `connectivity`, primary/VPN semantics, RSSI fixtures and boundaries, no scans, five-second active-only refresh, 30-second expiry, socket lifecycle, and fast-peer delivery alongside slow-peer eviction.
- Focused checks and `nix flake check --no-build` passed.
- Final Nix audit found no blocking or medium findings and judged the feature merge/deployment-ready.
- No Listener paths changed in the network feature chain.

## Verified orchestration hygiene before deployment

- Listener and CriomOS-home delivery-feedback worktrees were concluded through Orchestrate as merged.
- The approved abandoned CriomOS-home recovery checkout was verified clean with no unique work and concluded as rejected/discarded.
- Active-network feature worktrees were concluded after landing; the integration worker reported no active-network worktree remained.
- Integration lanes were released, unregistered, and retired with no active claims.

## Deployment state: unresolved

- A deployment worker was launched as:
  - Session: `ListenerDesktopDeployment`
  - Lane: `DeployAndVerifyDesktopIntegration`
  - Run: `e880be19-faff-49b6-b85b-04244221b0de`
- The async runner was marked failed by stale-run reconciliation. The report stated that PID `2750288` still appeared live but ownership could not be verified; the status age was anomalous.
- No valid deployment result was returned. Activation success, current user generation, service state, rollback target, deployment-lane state, and claim state are unknown.
- A read-only recovery scout was launched as run `d0b96cf6-0561-4957-83da-ea0b1f5ffc22` to inspect the PID, deployment outcome, services, sockets, rendered Mako rule, and orchestration state. It had not returned when this handover was written.
- Do not assume deployment succeeded or failed from the stale-run marker alone.

## Last known deployed baseline before this work

- Listener 0.13.0
- signal-listener 0.8.0
- meta-signal-listener 0.3.0
- User generation 145
- `listener.service` active

## Source references

- Listener command: `LiGoldragon/listener/src/command.rs`
- Listener lifecycle: `LiGoldragon/listener/src/daemon.rs`, `src/runtime.rs`, `src/status.rs`
- Clipboard delivery: `LiGoldragon/listener/src/delivery.rs`
- Notification implementation: `LiGoldragon/listener/src/notification.rs`
- Listener contract: `LiGoldragon/signal-listener/schema/lib.schema`
- Desktop dictation/service: `LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- Noctalia/Mako integration: `LiGoldragon/CriomOS-home/modules/home/profiles/min/sfwbar.nix`
- Listener widget: `LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/`
- Active Network module: `LiGoldragon/CriomOS-home/modules/home/profiles/min/active-network.nix`
- Active Network widget/helper: `LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/active-network/`
- Listener checks: `CriomOS-home/checks/listener-dictation-bindings/`, `checks/listener-level-widget/`
- Network checks: `CriomOS-home/checks/active-network-widget/`

## Real-world evidence not yet obtained

- Current deployed user generation and rollback target.
- Exactly one visible private Listener notification after a real successful completion.
- One 700 ms green flash after the same successful clipboard delivery.
- No delivery/notification/green flash for cancellation during recording, finalization, or transcription.
- No success feedback on transcription or clipboard errors.
- Quickshell loading the deployed shared validator and separate Active Network plugin.
- Live Ethernet, Wi-Fi, disconnected, VPN, captive/limited, and reconnect transitions.
- Actual dBm and meter presentation on target hardware.
