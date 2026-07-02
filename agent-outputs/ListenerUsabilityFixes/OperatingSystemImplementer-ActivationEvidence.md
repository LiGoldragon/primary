# Listener Usability Fix Live Activation Evidence

## Task And Scope

Tracker item: `primary-zddv.7`.

Activated the audited Listener usability-fix home generation on `goldragon` /
`ouranos` for user `li`, reloaded live user surfaces, and verified the active
Listener, Niri, Noctalia/QuickShell, and Whisrs state required before live
smoke testing.

No full live tap/cancel/speech smoke test was run. No transcript text,
clipboard contents, audio contents, secrets, or raw Nix store paths are recorded
in this evidence.

## Context Consulted

- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/NixAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/RustAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerLiveLevelResponsiveness/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerCancelSemantics/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/OperatingSystemImplementer-LiveActivationEvidence.md`
- `bd show primary-zddv.7 --json`
- `bd show primary-zddv.8 --json`
- `lojix "(Query (ByNode (goldragon ouranos None)))"`
- `systemctl` user and system service status, redacted for store paths
- Active Niri and Noctalia user configuration under `/home/li/.config`

## Deployment

Target transition:

- Cluster/node/user: `goldragon` / `ouranos` / `li`.
- Deployment shape: legacy installed Lojix `Home`, reported as `HomeOnly`.
- Source revision: `github:LiGoldragon/CriomOS-home/406417507d6b767edb69b1dbc9cff098736d11ce`.
- Builder: `None`.
- Extra substituters: `[]`.
- Requested actions: `Build`, then `Activate`.
- Rollback expectation: the previous current Home generation, deployment `35`,
  remained visible in the Lojix generation query before activation.

Installed deploy client evidence:

- `/home/li/.nix-profile/bin/meta-lojix` resolves to installed package
  `lojix-0.3.10`.
- The deployed daemon accepts the legacy `Home` request shape used by prior live
  activation evidence.

Commands used:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/406417507d6b767edb69b1dbc9cff098736d11ce Build None [])))"
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/406417507d6b767edb69b1dbc9cff098736d11ce Activate None [])))"
```

Observed results:

- Build request returned `(Deployed (36 (582 582)))`.
- `lojix-daemon.service` later logged terminal deployed output for deployment
  `36` at database marker `582`.
- Activate request returned `(Deployed (36 (586 586)))`.
- `lojix-daemon.service` later logged terminal deployed output for deployment
  `36` at database marker `586`.
- Final `lojix "(Query (ByNode (goldragon ouranos None)))"` included
  deployment `36` as `goldragon ouranos HomeOnly Switch Current`; the query
  database marker was `597`.

## Post-Activation Reload

Commands run after Lojix activation reached terminal deployed state:

```sh
systemctl --user daemon-reload
systemctl --user restart listener.service
niri msg action load-config-file
kill <old-quickshell-pid>
niri msg action spawn -- /home/li/.nix-profile/bin/noctalia-shell
```

Observed results:

- `listener.service` restarted at `2026-07-02T16:32:54+02:00` and remained
  active/running.
- QuickShell restarted as a new process with `QS_CONFIG_PATH` pointing at the
  activated Noctalia shell package.
- `niri validate` reported `/home/li/.config/niri/config.kdl` as valid after
  reload.

## Listener Evidence

Observed facts:

- `/home/li/.nix-profile/bin/listener` resolves to package `listener-0.5.1`.
- `/home/li/.nix-profile/bin/listener-daemon` resolves to package
  `listener-0.5.1`.
- `systemctl --user status listener.service` showed the service active/running
  after restart.
- `$XDG_RUNTIME_DIR/listener/status.sock` exists as a socket after daemon
  restart.
- `listener status` returned `(StatusReported Idle)`.
- `systemctl --user cat listener.service` contains `EnvironmentFile` and
  `ExecStart`, and a focused search found no `LISTENER_TRANSCRIPTION_PROGRAM`,
  no `listener-openai-transcribe`, no `whisrs`, and no clipboard reference in
  the generated Listener service wrapper.

## Binding And Wrapper Evidence

Active Niri config after reload:

- `Mod+Alt+M` has title `Listener Capture` and spawns
  `listener-toggle-capture toggle`.
- `Mod+Ctrl+Alt+M` has title `Listener Cancel` and spawns
  `listener-cancel-capture cancel`.
- Focused search found no active Listener `Mod+Alt+L` binding.

`listener-cancel-capture` evidence:

- The wrapper is present at `/home/li/.nix-profile/bin/listener-cancel-capture`.
- `bash -n` on the wrapper passed.
- Focused search showed the wrapper executes `listener cancel "$session"`.
- Focused search found no `listener stop`, no transcription command, no
  clipboard command, and no Whisrs reference in the wrapper.
- The wrapper only extracts a numeric active Listener session from the typed
  `StatusReported (Capturing ...)` status shape, then calls typed cancel.

## Noctalia And QuickShell Evidence

Observed active configuration:

- `/home/li/.config/noctalia/settings.json` places `plugin:listener-level`
  immediately before `plugin:whisrs-level`.
- `/home/li/.config/noctalia/plugins.json` enables both `listener-level` and
  `whisrs-level`.
- Active plugin files exist for:
  - `/home/li/.config/noctalia/plugins/listener-level/BarWidget.qml`
  - `/home/li/.config/noctalia/plugins/listener-level/manifest.json`
  - `/home/li/.config/noctalia/plugins/whisrs-level/BarWidget.qml`
  - `/home/li/.config/noctalia/plugins/whisrs-level/manifest.json`
- The active Listener QML has `listenerState === "cancelled"` support, a
  `Capture cancelled` notification branch, and `visibleMicrophoneLevel`
  smoothing.
- QuickShell is running from the refreshed Noctalia spawn after activation.

## Whisrs Preservation Evidence

Observed facts:

- `whisrs.service` is active.
- `whisrs status` returned `idle`.
- Active Niri Whisrs bindings remain present:
  - `Mod+V` -> `whisrs toggle-copy`
  - `Mod+Shift+V` -> `whisrs toggle`
  - `Mod+Alt+V` -> `whisrs-recall`
  - `Mod+Ctrl+V` -> `whisrs cancel`
- `whisrs-level` remains enabled and adjacent to `listener-level` in Noctalia.

## Checks Run

Passed:

- `lojix "(Query (ByNode (goldragon ouranos None)))"` before and after deploy.
- `systemctl status lojix-daemon.service --no-pager | redact-nix-store-paths`.
- `systemctl --user daemon-reload`.
- `systemctl --user restart listener.service`.
- `niri msg action load-config-file`.
- `niri validate`.
- Noctalia/QuickShell restart through `niri msg action spawn`.
- `systemctl --user status listener.service --no-pager`.
- `systemctl --user status whisrs.service --no-pager`.
- `test -S "$XDG_RUNTIME_DIR/listener/status.sock"`.
- `listener status`.
- Focused searches over active Niri, Listener wrapper, Listener service, and
  Noctalia plugin/config surfaces.
- `bash -n "$(command -v listener-cancel-capture)"`.

Not run:

- Full live microphone tap/cancel/speech smoke. That remains owned by
  `primary-zddv.8`.

Command note:

- `listener --version` and `listener version` are not supported CLI commands.
  Version evidence came from the activated profile binary package names.
- A direct `nix eval` form for the remote flake input version used the wrong
  flake attribute path and failed; it was not needed because the live profile
  package names proved `listener-0.5.1`.

## Tracker Impact

- `primary-zddv.7` acceptance criteria are met and can close with this evidence.
- `primary-zddv.8` can start. Its prerequisite activation item is complete, and
  live smoke remains intentionally unrun here.

## Blockers And Follow-Up

No activation blocker remains.

Follow-up for `primary-zddv.8`: run live smoke for mic-tap responsiveness,
cancel no-spend/no-clipboard with retained artifact, and normal
record/transcribe/copy behavior using only non-private phrase evidence and
without exposing transcript text, clipboard contents, audio contents, or
secrets.
