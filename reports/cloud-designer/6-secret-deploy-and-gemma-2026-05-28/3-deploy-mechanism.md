# 3 · Deploy mechanism (scout synthesis)

## lojix-cli, not nixos-rebuild

The deploy tool is `lojix-cli` (on PATH; source
`/git/github.com/LiGoldragon/lojix-cli`). It takes one positional NOTA
record, no flags. CriomOS is network-neutral and exposes only
`nixosConfigurations.target`; host identity (prometheus) enters at
deploy time via a lojix-projected `--override-input
horizon/system/deployment`. You never name `.#prometheus` to Nix.

## Build-on-prometheus, skip local copy

- prometheus is a registered builder in `/etc/nix/machines`
  (`ssh-ng://nix-ssh@prometheus.goldragon.criome`) and a cache
  (`http://nix.prometheus.goldragon.criome`).
- `ssh root@prometheus.goldragon.criome` works for the current user
  (verified read-only). lojix deploys over root.
- **When builder == target, lojix wraps the whole `nix build` in
  `ssh root@<target>` and skips the closure-copy phase entirely**
  (`build.rs:374`, `copy.rs:62`, `deploy.rs:181`). The model FODs build
  on prometheus and nothing is copied to the local store — exactly the
  build-on-prometheus / no-local-pull constraint (intent 1016).

## The exact command

```sh
lojix-cli '(FullOs goldragon prometheus [./datom.nota] [github:LiGoldragon/CriomOS/main] Switch (Some prometheus) None)'
```

Run from `/git/github.com/LiGoldragon/goldragon/` so `./datom.nota`
resolves. The `(Some prometheus)` builder slot is load-bearing: it
makes the build run on prometheus and skips the local copy. `Boot` or
`BootOnce` instead of `Switch` for non-live / revertible activation.

Pre-flight (read-only): `ssh -o BatchMode=yes root@prometheus.goldragon.criome 'nix --version'`
(verified OK), `grep prometheus /etc/nix/machines` (present).

This works because prometheus is both target and cache; a different
builder would risk unsigned-path rejection under `require-sigs`
(`skills/system-operator.md` §"Cluster Nix signing").
