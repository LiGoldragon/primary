# PrimaryDkrt Operating System Implementer Evidence

## Task And Scope

Tracker item `primary-dkrt` requested a production-trial deployment of Listener through CriomOS-home while preserving the existing working speech solution. The scope was the `li` home environment on cluster `goldragon`, node `ouranos`, with Listener on a distinct keyboard binding and Whisrs bindings left intact.

The work deliberately avoided a real microphone-to-clipboard smoke test. That remains assigned to `primary-jwx0`.

## Context Consulted

- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- `/home/li/primary/agent-outputs/ListenerFreshUsableTrial/TrackerWeaver-Closeout.md`
- `/home/li/primary/agent-outputs/ListenerFreshUsableTrial/TrackerWeaver-AdvancePrimary7qei.md`
- `/home/li/primary/agent-outputs/PrimaryZ1aq/GeneralCodeImplementer-Evidence.md`
- `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/README.md`
- `/git/github.com/LiGoldragon/CriomOS-home/skills.md`
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- Operating-system, Nix, edit-coordination, repository-closeout, and work-tracking doctrine from the role packet.

Spirit query:

- `PublicTextSearch [Listener CriomOS-home speech binding]` returned no matching public intent record.

## Source Changes

CriomOS-home repository: `/git/github.com/LiGoldragon/CriomOS-home`

Changed files:

- `flake.nix`
- `flake.lock`
- `modules/home/profiles/min/dictation.nix`
- `checks/listener-dictation-bindings/default.nix`
- `checks/whisrs-dictation-bindings/default.nix`
- `skills.md`

Changes made:

- Added Listener as a flake input pinned through `flake.lock`.
- Added Listener binaries to the Home Manager profile.
- Added `listener.service` as a user systemd service.
- Added `listener-toggle-capture` as a profile binary.
- Added `~/.config/listener/environment.example` to surface real-STT configuration honestly.
- Added a Listener Niri binding: `Mod+Alt+L` runs `listener-toggle-capture toggle`.
- Preserved existing Whisrs bindings:
  - `Mod+V` -> `whisrs toggle-copy`
  - `Mod+Shift+V` -> `whisrs toggle`
  - `Mod+Alt+V` -> `whisrs-recall`
  - `Mod+Ctrl+V` -> `whisrs cancel`
- Added a Listener binding check and strengthened the Whisrs binding check to cover recall.
- Documented side-by-side Whisrs/Listener behavior in `skills.md`.

CriomOS repository: `/git/github.com/LiGoldragon/CriomOS`

Changed files:

- `flake.lock`

Changes made:

- Updated the `criomos-home` input to the pushed CriomOS-home revision containing the Listener trial profile.

## Commits Pushed

CriomOS-home:

- `374dbc6bcbb18088474a15b17763ef8771e0408a` — `CriomOS-home: add Listener trial binding`
- `fdf84be335a35f6ad9d428f4cf66524603be1efe` — `CriomOS-home: package Listener toggle as profile binary`

CriomOS:

- `6954c08a065cf6d02034bf5e968836c9bc6debc22` — `CriomOS: pin Listener trial home profile`

Both repositories were pushed with `jj git push --bookmark main`; `main` and `main@origin` agree in each repository.

## Verification

Formatting:

- `nix run nixpkgs#nixfmt -- modules/home/profiles/min/dictation.nix checks/listener-dictation-bindings/default.nix checks/whisrs-dictation-bindings/default.nix` succeeded.
- `nix fmt` in CriomOS-home failed with an empty-input formatter wrapper issue; direct formatter invocation succeeded on touched Nix files.

CriomOS-home checks:

- `nix build .#checks.x86_64-linux.listener-dictation-bindings --no-link --print-out-paths` passed.
- `nix build .#checks.x86_64-linux.whisrs-dictation-bindings --no-link --print-out-paths` passed.
- `nix flake check --no-build` passed for `x86_64-linux`, with existing warnings about unknown outputs/incompatible systems and nixfmt-rfc-style deprecation.

Listener package:

- `nix build github:LiGoldragon/listener/fb54c1018f4a4011c870606934a1905d2f18b351 --no-link --print-out-paths` passed.

Home activation package:

- Generated activation package build from local CriomOS-home path passed after changing `listener-toggle-capture` to a profile binary.
- Immutable generated activation package build from `github:LiGoldragon/CriomOS-home/fdf84be335a35f6ad9d428f4cf66524603be1efe` passed with the local generated `horizon` and `system` overrides used by Lojix.

No-microphone Listener CLI probe:

- Used a fake capture command and no real STT backend.
- `listener status` reported idle before capture.
- `listener start` returned a started session.
- `listener status` reported an active capturing session.
- `listener stop` produced the explicit not-configured transcript message, proving the deployment stays honest when real transcription is not configured.

Post-deploy profile evidence:

- Before deployment, the latest current HomeOnly generation was 28.
- `meta-lojix` accepted a profile-only home deploy as deployment 29 using the deployed Lojix 0.3.10 contract shape:
  - operation class: `Deploy`
  - deployment variant: `Home`
  - mode: `Profile`
  - target: `goldragon/ouranos`, user `li`
  - source: `/git/github.com/LiGoldragon/goldragon/datom.nota`
  - flake: `github:LiGoldragon/CriomOS-home/fdf84be335a35f6ad9d428f4cf66524603be1efe`
- Lojix query showed HomeOnly generation 29 became current.
- The active Home Manager profile exposes these executable profile entries:
  - `listener`
  - `listener-daemon`
  - `listener-toggle-capture`

## Deployment Status

Completed:

- Listener is in the normal CriomOS-home Home Manager profile path.
- CriomOS pins the deployed CriomOS-home revision.
- Lojix recorded HomeOnly generation 29 as current after a profile-only deployment.
- Listener has a distinct configured binding, `Mod+Alt+L`.
- Whisrs bindings remain configured and are covered by Nix checks.

Not performed:

- No live Home Manager activation package was run.
- No live Niri config reload was run.
- No real microphone/STT/clipboard smoke test was run.

## Real STT Configuration Honesty

The deployed service does not claim real transcription without configuration. The service defaults capture and clipboard commands, but intentionally does not set `LISTENER_TRANSCRIPTION_PROGRAM`.

The deployment includes `~/.config/listener/environment.example`; copying it to `~/.config/listener/environment` and setting `LISTENER_TRANSCRIPTION_PROGRAM` is the surfaced configuration point for real STT. Without that setting, Listener returns the explicit not-configured transcript.

## Blocker And Operator Boundary

The remaining live-use boundary is active session activation. The deployed profile contains Listener and the Niri binding, but the running compositor will not necessarily load `Mod+Alt+L` until an operator either starts a new session or explicitly runs the Niri reload procedure after a suitable Home activation state.

I did not run live Home activation or `niri msg action load-config-file` because that changes the active compositor/session state while the existing Whisrs speech workflow is in use. This is the precise human-controlled condition left for the operator.

## Recommended Audit Scope For `primary-id8a`

Audit `primary-id8a` should inspect:

- The CriomOS-home diff for `modules/home/profiles/min/dictation.nix`.
- The new and strengthened binding checks.
- The CriomOS `flake.lock` pin to CriomOS-home `fdf84be335a35f6ad9d428f4cf66524603be1efe`.
- The Lojix profile-only deployment evidence for HomeOnly generation 29.
- The distinction between deployed profile state and live compositor reload state.
- The real-STT honesty path: `LISTENER_TRANSCRIPTION_PROGRAM` is only an operator-provided environment setting.

