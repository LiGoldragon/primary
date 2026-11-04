Brief: { Mind codexManager Secondary }, from { Psyche codexManager Secondary a53796 }.

When the living types `codex` he gets 0.158.0-alpha.9; he wants the latest (npm @openai/codex is 0.166.0). `codex` on PATH is a home-manager wrapper from CriomOS-home (modules/home/default.nix, modules/home/profiles/min/codex-next-candidate.nix, codex-remote-control.nix, packages/flow-deployment/default.nix) that runs codex-next 0.158 against an app-server socket in ~/.codex-next; codex-next is 0.161, codex-remote 0.163.

Make `codex` the latest release, packaged in Nix, keeping his login and the running flows' clients (codex-next-flow-client, codex-stable-flow-client, the app-servers) working through the switch. Say what the other wrappers are for, and which of them are now redundant, without removing any. Deploy with home-manager, then verify `codex --version` in a fresh shell.

Report to { Psyche codexManager Secondary }: the version now, what changed, and anything that needs the living.
