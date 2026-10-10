# Codex and Claude Desktop deployment

Method: probe `nix eval --impure --json --expr …` against the pushed Home
`main` revision.

For a projected medium graphical Agent Intercom user, evaluation returned:

```text
codexCliMatchesDesktop: true
codexRemoteMatches: true
codexName: codex-0.149.0
claudeDesktopInstalled: true
claudeDesktopName: claude-desktop-1.34493.1
```

For the same graphical capability with a small user profile, evaluation
returned:

```text
codexDesktopEnabled: false
claudeDesktopInstalled: false
```

The aggregate `nix flake check --offline --no-build` reaches the Home
flake's intentional no-system-input stub and is not the targeted deployment
proof.  The exact pushed Home revision instead passed the targeted graphical
TUI contract with separate evaluation and a remote-only build:

```text
nix eval --refresh --raw --show-trace \
  --override-input system <materialized-system> \
  --override-input horizon <materialized-horizon> \
  --override-input pkgs /git/github.com/LiGoldragon/CriomOS-pkgs \
  github:LiGoldragon/CriomOS-home/f05a3639de72#checks.x86_64-linux.agent-intercom-graphical-tui.drvPath

nix build --refresh --no-link --option max-jobs 0 --option fallback false \
  --builders '@/etc/nix/machines' \
  --override-input system <materialized-system> \
  --override-input horizon <materialized-horizon> \
  --override-input pkgs /git/github.com/LiGoldragon/CriomOS-pkgs \
  github:LiGoldragon/CriomOS-home/f05a3639de72#checks.x86_64-linux.agent-intercom-graphical-tui
```

Both exited successfully.  Nix reports the Codex, Claude Desktop, Desktop
integration, Agent Intercom, and graphical-TUI contract derivations built on
`ssh-ng://nix-ssh@prometheus.goldragon.criome`; local jobs were disabled and
fallback was false.

CriomOS commit `e1008e20abad` then pinned this exact Home revision.  Its
materialized `nixosConfigurations.target` passed the same separate evaluation
and remote-only build discipline with the system, horizon, deployment, and
secrets materialized inputs.  That build also ran on Prometheus and exited
successfully.
