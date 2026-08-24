# CriomOS-b8x source and build evidence

Method: implementation-subflow direct source, remote-Nix, and Lojix
observations returned to this flow on 2026-08-24; the immutable revisions,
commands, and terminal results below are reproducible.

Final producer: CriomOS-home
`0836e4b7e367efe6a81a4fa657e2a2f741f0d801`. Its preceding commit
`30e19a081d1fdc8916b7645b7fa4ffffda3c1a8d` updated the Codex input to
`05b1b39da135e34526f898600e09e67b55d5436c` (stable 0.149.1), advanced the
coupled sidebar to 26.5818.61809, and updated six existing check expectations.
Claude Code and its VSIX remain 2.1.241. The final producer commit corrected
sidebar metadata/lifecycle expectations from 26.5814.41407 after a candidate
realization exposed that stale surface.

Final consumer: CriomOS
`ab005ef8bc8828e1f92563cbb4bb966c2adda5bc`; its only source boundary is the
exact Home lock refresh. The producer and consumer commits were pushed with
the `main` bookmark from clean isolated Jujutsu worktrees.

The first producer check attempt was a negative witness, not a build:
evaluating immutable `30e19a…` returned `CriomOS-home: no system input was
provided`. Its Home checks require OS-owned projected `system` and `horizon`.

The final consumer evaluation was independent and green:

```sh
nix eval --raw --refresh --option max-jobs 0 --option fallback false \
  --builders '@/etc/nix/machines' \
  github:LiGoldragon/CriomOS/ab005ef8bc8828e1f92563cbb4bb966c2adda5bc#nixosConfigurations.target.config.system.build.toplevel.drvPath \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/horizon \
  --override-input deployment /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/deployment \
  --override-input secrets /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/secrets
```

The matching immutable `--no-link` build exited 0. All 35 derivations ran on
Prometheus only, `ssh-ng://nix-ssh@prometheus.goldragon.criome`; local
`max-jobs=0` and `fallback=false`. The returned closure includes Codex CLI
0.149.1 and Codex VSIX 26.5818.61809.

Authored Home source requires the Codex sidebar to advance with the CLI, so
the VSIX is a coupled package surface rather than an independent scope guess.
