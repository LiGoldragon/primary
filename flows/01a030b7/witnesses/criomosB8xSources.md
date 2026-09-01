# CriomOS-b8x source and remote-build witness

Method: implementation subflow direct source and remote-Nix observations,
returned 2026-08-24. Producer Home `30e19a081d1fdc8916b7645b7fa4ffffda3c1a8d`
updated Codex input `05b1b39da135e34526f898600e09e67b55d5436c` to stable
0.149.1, sidebar 26.5818.61809, and six check expectations; Claude remained
2.1.241. Final producer `0836e4b7e367efe6a81a4fa657e2a2f741f0d801` fixed
stale sidebar metadata/lifecycle expectations exposed by the candidate build.
Final CriomOS consumer `ab005ef8bc8828e1f92563cbb4bb966c2adda5bc` pins it.

The initial Home-only check attempt returned `CriomOS-home: no system input
was provided`, a negative evaluation witness; no build occurred. It showed
that the Home checks need OS-owned projected system/horizon inputs.

Final independent command shape:

```sh
nix eval --raw --refresh --option max-jobs 0 --option fallback false \
  --builders '@/etc/nix/machines' \
  github:LiGoldragon/CriomOS/ab005ef8bc8828e1f92563cbb4bb966c2adda5bc#nixosConfigurations.target.config.system.build.toplevel.drvPath \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/horizon \
  --override-input deployment /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/deployment \
  --override-input secrets /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/secrets
```

Evaluation exited 0. The matching immutable `--no-link` build exited 0: all
35 derivations ran only on Prometheus through
`ssh-ng://nix-ssh@prometheus.goldragon.criome`, with local `max-jobs=0` and
`fallback=false`. Closure includes Codex 0.149.1 and VSIX 26.5818.61809.
