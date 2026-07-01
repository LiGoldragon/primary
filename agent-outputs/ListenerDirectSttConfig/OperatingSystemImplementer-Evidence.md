# Listener Direct STT Configuration Evidence

## Task And Scope

Configure Listener to use the same real STT provider/backend pattern as the
working Whisrs setup without invoking Whisrs. Then deploy the configuration for
the `li` Home profile on `goldragon/ouranos` and rerun the real
microphone-to-clipboard smoke test only if the real-world conditions are
available.

Target deployment context:

- cluster: `goldragon`
- node: `ouranos`
- user: `li`
- artifact kind: HomeOnly/user environment
- requested state transition: build and activate a Home profile with direct
  Listener STT wiring
- source revision policy: pushed immutable refs
- builder: Lojix default/none in the deployed older `Home` request shape
- rollback path: reactivate Home generation 29 or deploy the previous
  CriomOS-home commit if generation 30 caused trouble

## Context Consulted

- `/home/li/primary/agent-outputs/PrimaryJwx0/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PrimaryId8a/NixAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- tracker items `primary-jwx0` and `primary-c8w0`
- `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/docs/ROADMAP.md`
- `/git/github.com/LiGoldragon/CriomOS-home/skills.md`
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS/docs/ROADMAP.md`
- `/git/github.com/LiGoldragon/CriomOS/README.md`
- Listener source README, architecture, and transcription implementation
- Whisrs service and CriomOS-home dictation module

Spirit query:

- `PublicTextSearch [Listener Whisrs transcription backend provider]` returned
  no matching public intent record.

## Backend Discovered

Observed facts:

- Whisrs is configured with backend `openai`.
- Whisrs uses OpenAI REST transcription with model `gpt-4o-transcribe`.
- The Whisrs daemon wrapper reads the provider key from `gopass openai/api-key`
  into Whisrs' own runtime environment.
- The Whisrs config sets English language and a prompt/vocabulary oriented to
  dictated technical text.

Interpretation:

- "Use the same backend we are using now with Whisrs" means Listener should use
  OpenAI REST transcription with `gpt-4o-transcribe` and the same `gopass`
  secret source, not Whisrs as a subprocess or dependency.

No secret values were read into evidence, chat, commits, or reports.

## Source Changes

CriomOS-home changed files:

- `modules/home/profiles/min/dictation.nix`
- `checks/listener-dictation-bindings/default.nix`
- `skills.md`

Changes:

- Added `listener-openai-transcribe`, a Home-managed wrapper that:
  - accepts Listener's raw `s16le` 16 kHz mono PCM export path;
  - converts it to a temporary WAV file with ffmpeg;
  - reads `gopass openai/api-key` at runtime;
  - calls OpenAI REST transcription directly with `gpt-4o-transcribe`;
  - prints only transcript text to stdout for Listener.
- Set Listener's service wrapper default `LISTENER_TRANSCRIPTION_PROGRAM` to
  `listener-openai-transcribe`.
- Kept `~/.config/listener/environment` as the local override file.
- Added `listener-openai-transcribe` to the Home profile packages.
- Extended the Listener binding check to prove:
  - `Mod+Alt+L` still runs `listener-toggle-capture toggle`;
  - Whisrs bindings remain present;
  - `listener.service` keeps the local environment override;
  - the generated Listener service wrapper contains a transcription program;
  - the generated Listener service wrapper references
    `listener-openai-transcribe`;
  - the generated Listener service wrapper does not mention Whisrs;
  - both generated shell scripts pass `bash -n`.
- Updated `skills.md` so future agents know Listener has a direct OpenAI
  default while the environment file remains an override.

CriomOS changed files:

- `flake.lock`

Changes:

- Updated the `criomos-home` input to the CriomOS-home commit containing the
  direct Listener STT wrapper, so the full-system input graph pins the same
  Home configuration for reboot persistence.

Local/uncommitted configuration:

- No secret-bearing local Listener environment file was created.
- No API key or token was committed.
- No source or tracker changes were left uncommitted by this work.

## Commits Pushed

- CriomOS-home `84dbf53811fc31459fb443954a067d33ad8e648c`:
  `CriomOS-home: configure Listener OpenAI transcription`
- CriomOS `efa4b336698e0e9e80c335c1982758f7e5b4f1a2`:
  `CriomOS: pin Listener OpenAI transcription home`

Both repositories reported clean working copies after push.

## Checks Run

CriomOS-home local checks:

- `nix run nixpkgs#nixfmt -- modules/home/profiles/min/dictation.nix checks/listener-dictation-bindings/default.nix`
  passed, with an existing flake registry warning.
- `nix build .#checks.x86_64-linux.listener-dictation-bindings --no-link --print-out-paths`
  passed.
- `nix build .#checks.x86_64-linux.whisrs-dictation-bindings --no-link --print-out-paths`
  passed.
- `nix flake check --no-build` passed for `x86_64-linux`, with existing
  warnings about unknown outputs, omitted incompatible systems, and nixfmt
  naming deprecation.

Pushed-ref checks:

- `nix build` of the pushed CriomOS-home Listener binding check through the
  remote SSH flake ref passed.
- `nix build` of the pushed CriomOS-home Whisrs binding check through the
  remote SSH flake ref passed.

CriomOS checks:

- `nix flake update criomos-home` updated only the intended lock entry.
- `jq` confirmed the CriomOS lock pins CriomOS-home
  `84dbf53811fc31459fb443954a067d33ad8e648c`.
- `nix flake metadata` confirmed the pushed CriomOS ref
  `efa4b336698e0e9e80c335c1982758f7e5b4f1a2` is fetchable.
- `nix flake check --no-build` in CriomOS did not evaluate because this repo
  requires Lojix-projected `system` input overrides. This is the expected
  direct-evaluation boundary from CriomOS itself, not evidence of a lock defect.

Secret/config checks:

- `gopass show -o openai/api-key >/dev/null` succeeded; the secret value was
  not printed.
- The generated Listener service wrapper was checked for
  `LISTENER_TRANSCRIPTION_PROGRAM`, `listener-openai-transcribe`, and absence
  of `whisrs`.

## Deployment And Live Session Evidence

Deployment actions:

- Queried current Lojix state before deployment; Home generation 29 was current.
- Submitted a Home deployment through the older deployed Lojix `Home` request
  shape because the on-host `meta-lojix` rejected the newer
  `UserEnvironment` variant.
- The accepted and queryable deployed generation is Home generation 30.
- Queried Lojix after deployment; generation 30 is current for
  `goldragon/ouranos`.
- Ran the Home Manager activation script for the current profile.
- Ran explicit Niri config reload with `niri msg action load-config-file`.
- Restarted `listener.service` after activation to remove ambiguity about the
  running process environment.

Live evidence:

- `listener.service` is active.
- `listener status` reports idle after restart.
- The active Home profile contains `listener`, `listener-daemon`,
  `listener-toggle-capture`, `listener-openai-transcribe`, `whisrs`, and
  `whisrs-recall`.
- The active Listener service wrapper exports `LISTENER_TRANSCRIPTION_PROGRAM`
  to `listener-openai-transcribe`.
- The active Listener service wrapper does not reference Whisrs.
- `niri validate` passed and `niri msg action load-config-file` returned
  success.
- Active Niri config contains `Mod+Alt+L` for Listener and the existing Whisrs
  bindings for `Mod+V`, `Mod+Shift+V`, `Mod+Alt+V`, and `Mod+Ctrl+V`.
- `whisrs.service` remains active and `whisrs status` reports idle.
- The system default source is present and unmuted; at verification time it was
  the laptop digital microphone.
- Clipboard tooling is present.

## Smoke-Test Result

Result: blocked.

Conditions:

- Live session sees Listener from the deployed Home profile: pass.
- Niri sees `Mod+Alt+L`: pass after explicit reload.
- Listener has a real STT backend configured independently and directly,
  matching the Whisrs backend/provider without invoking Whisrs: pass.
- Starting/stopping capture uses the system default microphone and sends a real
  transcript to clipboard: not attempted.
- Whisrs remains present and configured: pass.

Precise blocker:

- A real operator-spoken microphone phrase was not available during this agent
  run. I did not synthesize audio, play TTS, use Whisrs, or otherwise simulate
  microphone speech because that would not satisfy the requested real
  microphone-to-clipboard proof.

Exact condition needed:

- With the current generation 30 live session active, an operator should speak
  a non-private test phrase into the system default microphone while
  `listener-toggle-capture toggle` or `Mod+Alt+L` starts/stops capture. Then
  verify with clipboard contents that the expected phrase arrived, without
  copying private transcript text into public evidence.

Clipboard delivery evidence:

- Clipboard tooling is present.
- No transcript clipboard read was performed because no real microphone
  transcription was attempted.

## Tracker State

- `primary-jwx0` remains blocked, but the blocker changed from "no Listener
  STT backend configured" to "needs operator-spoken real microphone phrase for
  final clipboard proof."
- `primary-c8w0` should not close a passing production-trial readiness result
  yet. It can only start if its scope is to close around the precise remaining
  smoke-test blocker rather than a passed real transcript result.

## Blockers And Follow-Up

Open blocker:

- Complete the real operator-spoken Listener capture and clipboard proof.

Follow-up command shape once an operator is ready:

- Confirm `listener status` is idle.
- Run `listener-toggle-capture toggle` or press `Mod+Alt+L`.
- Speak the agreed non-private phrase.
- Run `listener-toggle-capture toggle` or press `Mod+Alt+L` again.
- Confirm `listener status` returns idle.
- Confirm clipboard contains the expected phrase without pasting the transcript
  into public evidence.

Out of scope not started:

- `primary-llep`
- `primary-gm05`
