# Listener Live Activation Evidence

## Task And Scope

Tracker items: `primary-acmr.6`, `primary-jwx0`, and `primary-c8w0`.

Scope was to resolve the live-smoke blocker where `meta-lojix` rejected the
documented `UserEnvironment` request shape, then safely activate the audited
Listener status-bar generation on `goldragon` / `ouranos` for user `li`.

No source code was changed for Listener, CriomOS, CriomOS-home, or Lojix. No
OpenAI key, secret-store output, clipboard text, transcript text, or private
speech was printed or recorded.

## Result

Result: **activation and reload succeeded; real spoken smoke remains blocked on
human input**.

The live Lojix blocker was a deployed-tooling/doctrine mismatch:

- Local checked-out current `meta-signal-lojix` source defines
  `DeployRequest [(Host HostDeployment) (UserEnvironment UserEnvironmentDeployment)]`.
- The installed `meta-lojix` binary on this host is `lojix-0.3.10`.
- The installed CLI rejected the documented new request with
  `unknown DeployRequest variant UserEnvironment`.
- A decode probe using the old `Home` top-level variant and the new
  `ActivateNow` action failed at `unknown HomeMode variant ActivateNow`, proving
  the deployed contract recognizes `Home` but not the new action vocabulary.
- `lojix "(Query (ByNode (goldragon ouranos None)))"` still reports generations
  with old `HomeOnly` / `FullOs` artifact names.

The correct invocation for this deployed daemon is therefore:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/<rev> <Build|Activate> None [])))"
```

For this task the activated home revision was
`a4adfc961f06cbbc84ebd59201c4a706e399c388`, pinned by CriomOS commit
`731d999fb1fcc9f78b79e9cd92a0bff033377037`.

## Deployment

Target transition:

- Cluster/node/user: `goldragon` / `ouranos` / `li`.
- Live-daemon artifact kind: legacy `Home` / `HomeOnly`, equivalent to the
  intended user-environment profile activation.
- Requested actions: non-activating `Build`, then `Activate`.
- Source revision policy: exact pushed CriomOS-home revision
  `a4adfc961f06cbbc84ebd59201c4a706e399c388`, reached through the audited
  CriomOS pin.
- Builder: `None`.
- Rollback path: previous Lojix HomeOnly current generation remains available
  in the generation query.

Commands run:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/a4adfc961f06cbbc84ebd59201c4a706e399c388 Build None [])))"
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/a4adfc961f06cbbc84ebd59201c4a706e399c388 Activate None [])))"
```

Observed results:

- The Build request was admitted as deployment `32` and reached a terminal
  `Deployed` line in `lojix-daemon.service`.
- The Activate request was admitted as deployment `32` with a newer marker and
  reached a terminal `Deployed` line in `lojix-daemon.service`.
- `lojix "(Query (ByNode (goldragon ouranos None)))"` then listed generation
  `32` as `goldragon ouranos HomeOnly Switch Current`.

## Post-Activation Reload

Commands/actions run:

- `systemctl --user daemon-reload`
- `systemctl --user restart listener.service`
- `niri msg action load-config-file`
- Terminated the old QuickShell process.
- Started `/home/li/.nix-profile/bin/noctalia-shell` through
  `niri msg action spawn`.

Observed facts:

- New Noctalia/QuickShell process is under
  `app-niri-noctalia-shell-332129.scope`.
- The process environment has `QS_CONFIG_PATH` pointing at the activated
  Noctalia shell package.
- The QuickShell package revision itself remained the same package revision;
  the active configuration and profile wrapper changed.

## Listener Evidence

Observed facts:

- `listener.service` is active/running.
- The running listener daemon executable resolves to package name
  `listener-0.4.0`.
- `nix eval --raw github:LiGoldragon/listener/4080f8e89acc173ac124d814147e13dcb971a7a5#packages.x86_64-linux.default.version`
  returned `0.4.0`.
- `$XDG_RUNTIME_DIR/listener/status.sock` exists after daemon restart.
- The generated `listener.service` contains `EnvironmentFile` and `ExecStart`,
  but grep found no `LISTENER_TRANSCRIPTION_PROGRAM` and no
  `listener-openai-transcribe`.
- No Listener transcript, clipboard content, or secret value was read.

Interpretation:

- The live Listener runtime is now the audited internal-transcription/status
  runtime, not the previous Listener `0.3.0` generation.
- The rejected external transcription program override is absent from the live
  generated user service wrapper.

## Noctalia Evidence

Observed facts:

- `~/.config/noctalia/settings.json` places `plugin:listener-level`
  immediately before `plugin:whisrs-level` in the right bar list.
- `~/.config/noctalia/plugins.json` enables both `listener-level` and
  `whisrs-level`.
- The activated profile installs both Listener and Whisrs plugin manifests and
  QML files under `~/.config/noctalia/plugins`.
- `niri validate` reported the active config is valid.

Interpretation:

- The active Noctalia configuration now includes the Listener widget adjacent
  to Whisrs and the bar process was restarted after activation.

## Whisrs Preservation Evidence

Observed facts:

- `whisrs.service` is active.
- `whisrs status` returned `idle`.
- Active Niri bindings still include:
  - `Mod+V` -> `whisrs toggle-copy`
  - `Mod+Shift+V` -> `whisrs toggle`
  - `Mod+Alt+V` -> `whisrs-recall`
  - `Mod+Ctrl+V` -> `whisrs cancel`
- Listener binding remains `Mod+Alt+L` -> `listener-toggle-capture toggle`.
- Whisrs plugin files and Noctalia plugin state remain present.

Interpretation:

- The Listener activation did not remove the Whisrs service, plugin, or Niri
  bindings.

## Microphone Evidence

Observed facts:

- The default source is the USB wireless microphone source.
- The default source is not muted.
- The source volume is 100%.

Interpretation:

- The microphone is ready for a real spoken smoke test, but no real
  operator-spoken phrase was available in this run.

## Smoke-Test Status

`primary-acmr.6` is **not complete**.

Remaining exact human condition:

An operator must speak a non-private test phrase into the live microphone while
Listener `0.4.0` is active, using the deployed `Mod+Alt+L` binding or deployed
command path, and observe without disclosing transcript content that:

- recording state appears red;
- transcribing state appears yellow;
- generic copied notification appears;
- clipboard receives the expected phrase class;
- Whisrs remains intact.

No synthetic audio, replayed audio, or private transcript disclosure was used.

## Tracker Impact

- `primary-acmr.6`: deployment blocker resolved; remains blocked only on the
  real operator-spoken microphone-to-clipboard observation above.
- `primary-jwx0`: cannot close yet because it depends on the same real spoken
  smoke evidence.
- `primary-c8w0`: cannot advance yet because `primary-jwx0` remains blocked.

## Commands Consulted

- `spirit "(PublicTextSearch [lojix deploy user environment home listener])"`:
  no matching public record.
- `readlink -f /home/li/.nix-profile/bin/meta-lojix`: installed binary is
  `lojix-0.3.10`.
- Current source reads from
  `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema` and
  `/git/github.com/LiGoldragon/meta-signal-lojix/src/schema/lib.rs`.
- Decode probe:
  `meta-lojix "(Deploy (Home (... ActivateNow None [])))"` rejected at
  `unknown HomeMode variant ActivateNow`.
- `lojix "(Query (ByNode (goldragon ouranos None)))"` before and after deploy.
- `systemctl status lojix-daemon.service --no-pager` for terminal deploy
  evidence, filtered through `redact-nix-store-paths`.
- `systemctl --user daemon-reload`
- `systemctl --user restart listener.service`
- `systemctl --user status listener.service --no-pager`
- `systemctl --user cat listener.service`
- `niri msg action load-config-file`
- `niri msg action spawn -- /home/li/.nix-profile/bin/noctalia-shell`
- Focused searches of active Noctalia and Niri config.
- `systemctl --user status whisrs.service --no-pager`
- `whisrs status`
- `pactl get-default-source`, source mute, and source volume checks.
- `niri validate`

## Blockers And Follow-Up

The live Lojix daemon still needs doctrine/tooling reconciliation: either
upgrade the deployed Lojix runtime to the nonlegacy `Host` /
`UserEnvironment` contract, or restore runtime guidance for hosts still on
`lojix-0.3.10`. This task used the deployed 0.3.10 contract only after proving
the live daemon accepted `Home` and rejected `UserEnvironment`.

Do not start `primary-llep` or `primary-gm05` from this evidence; they remain
out of scope for this task.
