# PrimaryId8a Nix Auditor Review

## Task And Scope

Audit tracker item `primary-id8a`: Listener CriomOS-home side-by-side deployment for a production trial. Reviewed final deployed source commits:

- CriomOS-home `fdf84be335a35f6ad9d428f4cf66524603be1efe`
- CriomOS `6954c08a065cf6d02034bf5e968836c9bc6debc22`
- Primary evidence/tracker commit `ee0a58a133d4f09d5affc5ba15187523048ec0b7`

Context read first:

- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- `/home/li/primary/agent-outputs/ListenerFreshUsableTrial/TrackerWeaver-Closeout.md`
- Tracker items `primary-dkrt` and `primary-id8a`

Spirit query evidence: `PublicTextSearch [listener CriomOS home deployment]` returned no matching public intent record, so this audit used the brief, tracker, repo doctrine, and source as controlling context.

## Findings

No blocking source or Nix defects found.

No finding blocks `primary-jwx0` from starting as the next work item, but the smoke-test runner must treat active-session activation as a required first step. Current deployed generation evidence is sufficient for audit pass and source/profile readiness; it is not evidence that the running compositor has already loaded `Mod+Alt+L`.

## Operator Gate

Operator action required before real microphone-to-clipboard testing:

- Run a safe Home Manager activation for generation 29 or start a fresh graphical session that realizes that generation.
- After activation, explicitly reload Niri config with the documented operator IPC procedure or start a fresh Niri session.
- Provide real STT configuration by creating `~/.config/listener/environment` with `LISTENER_TRANSCRIPTION_PROGRAM` before claiming real transcription.

Observed facts:

- Lojix reports generation 29 for `goldragon/ouranos` as current `HomeOnly` profile state.
- The generation 29 Home Manager `home-path` contains `listener`, `listener-daemon`, and `listener-toggle-capture`.
- The generation 29 generated systemd files contain `listener.service` and `whisrs.service`.
- The currently active user profile path did not expose the Listener binaries during this audit.
- The currently active user systemd config did not contain `listener.service`; `systemctl --user cat listener.service` reported no unit.
- The active user systemd config still had `whisrs.service`.

Interpretation:

- The implementation evidence correctly describes the no-live-activation/no-Niri-reload boundary at `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md:148`.
- The phrase "active Home Manager profile exposes these executable profile entries" in that evidence should be read as Lojix/Home Manager generation state, not current shell `PATH` or currently loaded user systemd state.
- This does not fail `primary-id8a`, because the source and Lojix profile state are ready for the next operator-controlled step. It does mean `primary-jwx0` begins with activation/reload, not with pressing `Mod+Alt+L`.

## Source Review

CriomOS-home final tree at `fdf84be3`:

- `flake.nix:90-94` adds Listener as a normal remote flake input and makes it follow the profile `nixpkgs` and shared `crane`.
- `flake.lock:1077-1099` pins Listener to `fb54c1018f4a4011c870606934a1905d2f18b351`.
- `modules/home/profiles/min/dictation.nix:17-18` reaches Whisrs and Listener through Nix package values, not filesystem search.
- `modules/home/profiles/min/dictation.nix:105-112` adds `whisrs`, `listener`, and `listenerToggle` to `home.packages`.
- `modules/home/profiles/min/dictation.nix:178-204` defines `listener.service` as a user systemd service with `EnvironmentFile = "-%h/.config/listener/environment"`.
- `modules/home/profiles/min/dictation.nix:59-65` defaults capture and clipboard commands while intentionally not setting `LISTENER_TRANSCRIPTION_PROGRAM`.
- `modules/home/profiles/min/dictation.nix:138-144` installs `listener/environment.example` and documents the operator-owned real STT configuration point.
- `modules/home/profiles/min/dictation.nix:68-102` packages `listener-toggle-capture` as a profile binary and starts `listener.service` if the daemon is unavailable.
- `modules/home/profiles/min/dictation.nix:296-324` keeps Whisrs bindings on `Mod+V`, `Mod+Shift+V`, `Mod+Alt+V`, and `Mod+Ctrl+V`, and adds Listener on `Mod+Alt+L`.
- `checks/listener-dictation-bindings/default.nix:18-27` imports the dictation module and reads the actual Niri binding values.
- `checks/listener-dictation-bindings/default.nix:31-45` checks executable suffixes and argument count, avoiding brittle full store-path equality.
- `checks/listener-dictation-bindings/default.nix:57-68` checks all four Whisrs bindings plus `Mod+Alt+L`.
- `checks/whisrs-dictation-bindings/default.nix:47-58` independently checks all four Whisrs bindings.

CriomOS final tree at `6954c08a`:

- `flake.lock:673-755` pins `criomos-home` to `fdf84be335a35f6ad9d428f4cf66524603be1efe`.
- `flake.lock:1627-1648` carries the same Listener revision as CriomOS-home, so the downstream lock is coherent with the home input.

Primary evidence commit `ee0a58a1`:

- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md:39-57` accurately names the changed deployment surfaces and side-by-side binding intent.
- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md:105-122` records profile-only deployment 29 and the Listener profile entries.
- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md:137-144` truthfully states that real STT is not configured by Nix and is operator-provided.
- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md:146-150` accurately leaves live Home activation and Niri reload outside the implementer boundary.

## Checks Run

Passed:

- `jj status --no-pager` in CriomOS-home: clean.
- `jj status --no-pager` in CriomOS: clean.
- `jj status --no-pager` in primary: clean before this audit report/tracker update.
- `nix eval --json .#checks.x86_64-linux.listener-dictation-bindings.name`: returned `listener-dictation-bindings`.
- `nix eval --json .#checks.x86_64-linux.whisrs-dictation-bindings.name`: returned `whisrs-dictation-bindings`.
- `nix build .#checks.x86_64-linux.listener-dictation-bindings --no-link --print-out-paths`: passed.
- `nix build .#checks.x86_64-linux.whisrs-dictation-bindings --no-link --print-out-paths`: passed.
- `nix flake check --no-build` in CriomOS-home: passed for `x86_64-linux`; warnings were unknown custom outputs, incompatible non-host systems omitted, and nixfmt-rfc-style deprecation.
- `jq -r '.nodes["criomos-home"].locked.rev' flake.lock` in CriomOS: returned `fdf84be335a35f6ad9d428f4cf66524603be1efe`.
- `jq -r '.nodes.listener.locked.rev' flake.lock` in CriomOS-home: returned `fb54c1018f4a4011c870606934a1905d2f18b351`.
- `jq -r '.nodes.listener.locked.rev' flake.lock` in CriomOS: returned `fb54c1018f4a4011c870606934a1905d2f18b351`.
- `lojix '(Query (ByGeneration 29))'`: returned generation 29 as current `HomeOnly` generation.
- `find /home/li/.local/state/nix/profiles/home-manager/home-path/bin ...`: found `listener`, `listener-daemon`, `listener-toggle-capture`, `whisrs`, and `whisrs-recall`.
- `find /home/li/.local/state/nix/profiles/home-manager/home-files/.config/systemd/user ...`: found `listener.service` and `whisrs.service`.
- Runtime config probe: `~/.config/listener/environment` is absent, so no real STT program is currently configured through the operator file.

Failed or not proof of readiness:

- `systemctl --user cat listener.service`: no unit in the currently active user systemd config.
- Active user profile probe for `listener`, `listener-daemon`, and `listener-toggle-capture`: not present in the currently active ordinary profile path.
- `lojix '(Query (ByNode (goldragon ouranos (Some UserEnvironment))))'`: rejected because this deployed contract uses the `HomeOnly` artifact naming, not `UserEnvironment`.
- `nix eval --raw --expr ... builtins.readFile /absolute/flake.lock`: rejected by pure evaluation. Replaced with `jq` lock reads.

Skipped:

- No live Home activation.
- No Niri reload.
- No real microphone/STT/clipboard smoke test.
- No paid STT API call.

## Tracker State

Audit result: pass with operator gate.

`primary-id8a` can close because the audit reviewed the changed Nix/deployment surfaces, found no blocking defect, and clearly states the remaining activation/reload/configuration actions.

`primary-jwx0` may start next, but it must begin by satisfying the operator gate above before attempting real microphone-to-clipboard validation.
