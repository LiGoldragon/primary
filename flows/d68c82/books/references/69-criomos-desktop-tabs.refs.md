# References: CriomOS: the desktop opens nothing on its own

## Proposal 1 (psyche-context vision/criomos.md, a new file)

- flows/d68c82/vision/criomos.md — Nobody edits files; the system is declarative (2026-10-11): declarative statement
- flows/d68c82/vision/criomos.md — A proper fix replaces every hotfix (2026-10-15): proper fix and deploy; hotfixes removed
- flows/d68c82/vision/criomos.md — A hardware fix keyed by hardware in cluster data (2026-10-16): hardware fix as cluster-data value; hardware library
- flows/d68c82/vision/criomos.md — Nothing opens tabs in the desktop browser on its own (last entry, undated): desktop statement
- flows/9993b5/vision/criomOsUpgrade.md — new service in CriomOS at its latest version (2026-09-17): services statements
- flows/b05237/vision/operational-criomosModularHardware.md — modular CriomOS, anatomy, stock harnesses, hardware type, Libre M5 (2026-09-18): CriomOS modularity, hardware type, harnesses statements; the stable/next Codex remote server and mobile-profile parts are not in this module
- psyche-context vision/ at bf5da81: no criomos.md; vision/x11.md, vision/git-server.md as form models

## Proposal 2 (CriomOS-home modules/home/profiles/min/codex-remote-control.nix)

- CriomOS-home at 56d9a9c7: home.activation.mergeClaudePermissionDefaults writes $HOME/.claude/settings.json through hexis mkManagedConfig, in the unconditional first block (every host)
- hexis ARCHITECTURE.md: default mode ensure, declared wins at the pointers it names, other keys survive
- witnessed 2026-10-18: ~/.claude/settings.json env holds only CLAUDE_CODE_DISABLE_AUTO_MEMORY; CLAUDE_CODE_ARTIFACT_AUTO_OPEN is unset
- caller's witness: Claude Code 2.1.294 Artifact tool runs xdg-open on each new artifact from an interactive main thread with a display; CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0 turns it off

## Proposal 3 (field-context compensation/book-crystallization.md)

- field-context at 8ef1ca4: "Check every book at phone width before publishing."
- witnessed 2026-10-18: five headless Chrome trees, children of the systemd user manager, started 10-13..16, profiles under flow scratchpads (one named cprof15v2-320light) and /tmp/m-*/p; no module in CriomOS or CriomOS-home launches them
