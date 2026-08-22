# VSCodium source inventory

Method: probe `rg -l -i --glob '!result*' '(vscodium|codium|claude-code-codium|claude-code-vsix|visualjj-vsix|codex-chatgpt-vsix)' /git/github.com/LiGoldragon/CriomOS-home | sort`.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`, `flake.lock`, `modules/home/default.nix`, `modules/home/base.nix`, `modules/home/text-scale.nix`, `modules/home/profiles/med/codium.nix`, `modules/home/profiles/med/emacs.nix`, `modules/home/desktop-database.nix`, `modules/home/vscodium/vscodium/default.nix`, `modules/home/vscodium/vscodium/claude-lifecycle.sh`, `modules/home/vscodium/vscodium/codium-launch.sh`, `modules/home/vscodium/vscodium/codium-supervisor.sh`, `packages/vscodium-casual/default.nix`, `packages/claude-code/default.nix`, `packages/agent-intercom/default.nix`, `modules/home/profiles/min/agent-intercom.nix`, `checks/vscodium-casual/default.nix`, `checks/vscodium-claude-lifecycle/default.nix`, and `checks/agent-intercom/default.nix`.

Method: code read `/git/github.com/LiGoldragon/CriomOS/flake.nix:35-49` and `/git/github.com/LiGoldragon/CriomOS/flake.lock:882-994` to identify the external consumer's pinned CriomOS-home revision.

Observations:

- The repository-wide reference scan finds the direct VSCodium implementation in the Home aggregate, the medium Codium desktop profile, the VSCodium module and three runtime scripts, the casual package, two VSCodium checks, and the Agent Intercom check. Cross-configuration references also occur in `base.nix`, `text-scale.nix`, and the medium Emacs profile.
- `modules/home/default.nix:32-90` imports both `./profiles/med/codium.nix` and `./vscodium/vscodium`; its `vscodium-ext` mention at lines 14-16 is only a comment and is not a current argument or input binding.
- `modules/home/vscodium/vscodium/default.nix:15-97` constructs the casual package, lifecycle, supervisor, launcher, and managed package; lines 119-182 construct VisualJJ, Claude, and ChatGPT/Codex VSIX derivations; lines 247-356 declare extensions, settings, preferred-editor behavior, activation, and managed settings.
- `claude-lifecycle.sh`, `codium-launch.sh`, and `codium-supervisor.sh` are the complete authored mutable-state and launch runtime surface. Their Nix substitutions and absolute helper closures are assembled in the VSCodium module.
- The durable lifecycle check evaluates the module and uses fake Codium/Nix-root boundaries. Its exact three-version contradiction fixture is at `checks/vscodium-claude-lifecycle/default.nix:859-919`; the casual check is a generated-wrapper/source assertion at `checks/vscodium-casual/default.nix:1-22`.
- The external CriomOS consumer pins CriomOS-home to revision `1a6e22da155bb75a6362d10623301b13d0c24b34` at `/git/github.com/LiGoldragon/CriomOS/flake.nix:35-49`, while the inspected home repository has a later local parent `9d2896c7`. The deployment consumer therefore does not automatically consume this audit's inspected source.
- No build, test, activation, Codium command, process launch, signal, or runtime-state write was performed for this witness.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/text-scale.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/desktop-database.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/vscodium-casual/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/agent-intercom/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-casual/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock`
