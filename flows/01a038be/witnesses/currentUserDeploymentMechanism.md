# Current UserEnvironment deployment mechanism

## Method

Read the current flow records, the deployment witnesses from flows
`01a02fe5`, `01a02b6a`, and `491750ff`, the current Home/CriomOS source, and
the current `goldragon/datom.dotos`.  No Lojix request, activation, source
edit, or target mutation was performed.  Repository status was checked with
`jj status`.

## Current source state

- `/git/github.com/LiGoldragon/CriomOS-home` is clean at parent
  `f05a3639de72` (`home: deploy shared Codex and Claude Desktop`), with empty
  working-copy commit `94bb5ad0cce8`.
- `/git/github.com/LiGoldragon/CriomOS` is clean at parent `e1008e20abad`
  (`criomos: pin shared Codex desktop deployment`), with empty working-copy
  commit `1c7b90271d5c`.  Its flake pins
  `github:LiGoldragon/CriomOS-home/f05a3639de72e4976c5ba87a932a39dc2f9ccf1c`.
- `/git/github.com/LiGoldragon/goldragon` is clean at `4b5bae42a5d0`.
  The proposal describes `ouranos` as `Large` with
  `AgentIntercomGraphical`, and user `li` as `Max`; that projection is the
  relevant gate for the Desktop package.

## Source observations

- `CriomOS-home/packages/codex/default.nix` returns
  `inputs.llm-agents.packages.${pkgs.stdenv.hostPlatform.system}.codex`; the
  Codex derivation is declared once and reused by terminal/Desktop/Intercom
  consumers.
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix` defines
  `desktopEnabled = graphicalEnabled && mediumEnabled`, takes Claude Desktop
  from `inputs.llm-agents.packages.${homeSystem}.claude-desktop`, and exposes
  the Desktop block only when that gate is true.
- `CriomOS-home/flake.nix` exports
  `homeConfigurations = builtins.mapAttrs mkHomeConfiguration horizon.users`
  and imports the maintained `codex-desktop-linux` integration at its pinned
  input.  The current package identity is therefore auditable, but the
  embedded Claude Code runtime remains package-managed and not externally
  observable for exact parity.
- `CriomOS/flake.nix` exports
  `homeConfigurations.<user>.activationPackage` as the activation package
  embedded in the materialized NixOS target and keeps the independently
  evaluated CriomOS-home outputs separate.  User deployment must select the
  projected target output, not a differently configured second evaluation.

## Deployment implication

The remembered exact request is recorded in
`flows/01a038be/reports/rememberedUserDeployment.md`: immutable Home revision,
`Horizon`, `(homeConfigurations.li.activationPackage)`, explicit Ouranos
transport, `HomeManagerNixProfileV1`, `RequireImmutable`, owner
`meta-lojix`, and ordinary-socket terminal observation.  The historical
`01a02fe5` incident makes endpoint identity a required pre-admission witness;
the current source state does not remove that requirement.
