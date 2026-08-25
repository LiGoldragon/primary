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
flake's intentional no-system-input stub. The Nix builder configuration points
to an absent machines file, so no configured remote builder is available. No
local build was run.
