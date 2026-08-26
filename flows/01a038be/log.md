# Flow 01a038be

## About

Deploy Claude Desktop and Codex CLI through an external flake after auditing its source and installation behavior.

Remembered: 01a0338f — depth 1
Remembered: 01a02fe5 — depth 1

## Settled

- Flow 01a0338f established that Ouranos's `ChatGPT` entry is an unofficial `ilysenko/codex-desktop-linux` Electron package, Zeus's `Codex` entry is a Chrome PWA, and neither host had Claude Desktop; both hosts had Claude Code.
- The living wants Desktop applications on medium-size graphical nodes, a streamlined source/install audit on every third-party-flake update, and explicit terminal/Desktop engine-version alignment.
- The living narrowed Codex alignment to one `llm-agents` derivation declared once and used by every consumer; upstream Desktop launcher behavior remains unchanged.
- Home commit `f05a3639de72` removes the standalone Codex provider, installs Claude Desktop at the medium graphical gate, and evaluates the Codex terminal/Desktop/remote package equality on the pushed revision.
- The exact pushed Home revision passed its graphical-TUI contract evaluation and remote-only build through the configured Prometheus Nix builder.  The build included Codex `0.149.0`, Claude Desktop `1.34493.1`, the maintained Desktop integration, Agent Intercom, and the contract itself.
- CriomOS commit `e1008e20abad`, on top of preserved commit `4c3da1562c49`, pins `criomos-home` exactly to `f05a3639de72`.  Its exact pushed materialized NixOS target passed separate evaluation and a remote-only Prometheus build.
- After endpoint identity proof, Lojix UserEnvironment deployment `61` activated immutable Home revision `f05a3639de72` for `goldragon/ouranos/li`.  Its terminal node-ledger record is `Completed/Succeeded` and Current; the live Home generation changed, Codex reports `0.149.0`, Claude Code reports `2.1.241`, both desktop executables are present, and the Codex remote-control and bridge services are active.
- Read-only live diagnosis found that the maintained Codex Desktop frontend is itself named `ChatGPT` by its shipped desktop metadata; the wrapper remains active and supplies the shared Codex CLI.  Claude Desktop instead has a missing discoverable `claude://` handler entry, which explains the callback chooser failure and has a small declarative repair path.
- Home commit `8d6e790c06e6` declares the existing package-owned `claude-desktop.desktop` in the active XDG applications directory and maps `x-scheme-handler/claude` to it at the same medium graphical gate.  Its focused contract passed separate evaluation and a Prometheus-only build, including entry, `%U`, MIME cache, and default-handler proof.
- CriomOS commit `1402eaa692ec` pins that exact Home revision.  After separate consumer evaluation and Prometheus-only top-level build, Lojix deployment `62` activated it for `goldragon/ouranos/li` and reached `Completed/Succeeded` Current.  The live profile changed and now exposes the Claude entry, URI cache mapping, and XDG default without opening an OAuth callback.
- The living's exact ruling that Software must not offer stateful installation is preserved in [its vision record](vision/installingSoftwareStatefully.md).
- Home commit `2fb9f089fafb` replaces the obsolete converted Codex Desktop
  integration with the official `llm-agents` ChatGPT Linux package at the
  existing medium graphical gate. It retains the one shared Codex derivation,
  now version `0.149.1`, and the existing Claude URI registration; former
  Computer Use/remote-control wiring is removed because the official Linux
  preview does not support it.
- CriomOS commit `e8b3e8e9951b` pins that exact Home revision. Both clean
  GitHub evaluations and configured Prometheus-only builds passed. Lojix
  deployment `63` completed/succeeded and is Current for `goldragon/ouranos/li`; the active generation
  exposes official ChatGPT `26.818.61809` as `chatgpt.desktop` and the
  `codex` URI handler, and preserves `claude-desktop.desktop` as the Claude
  URI handler. See the [correction report](reports/officialChatgptCorrectionDeployment.md).
- Read-only live diagnosis after two freezes found timestamped Intel i915 GPU
  hangs and context resets in ChatGPT's forced-X11 Electron process tree. The
  app had no OOM or cgroup pressure; severe system-wide I/O pressure was
  concurrent but not attributable to the app. Niri geometry corroborates the
  reported full-output-height non-fullscreen symptom, while the later
  interaction freeze lacks a separate timestamped kernel event. See the
  [freeze diagnosis](reports/officialChatgptFreezeDiagnosis.md).
- The living's new direction is preserved verbatim in its
  [X11 vision record](vision/x11.md). It settles an eventual goal to remove
  X11 from CriomOS, but does not itself authorize a configuration change.

## Open

- Claude Desktop's embedded Code runtime version remains unobservable through the supported package interface.  The package identity is checked, but no unsupported external-runtime override or exact embedded-runtime parity claim exists.
