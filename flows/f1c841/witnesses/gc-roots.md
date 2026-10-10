# Witness: durable GC roots for the home-manager candidate and rollback generations

Flow f1c841, subflow. Observed 2026-10-03 00:33 local.

## Method

Each generation was registered as an indirect GC root with
`nix-store --add-root <link> --indirect -r <path>`. This command only creates the
link `<link>` and a matching entry in `/nix/var/nix/gcroots/auto/`. Nothing was
built, switched, activated, deleted or garbage-collected. Before and after, the
roots were checked with `nix-store -q --roots`.

## Before

- `rn8fzfbw…-home-manager-generation` (candidate, orchestrate 0.36.1): the only root was
  `/tmp/claude-1001/-home-li-primary/3ec6480d-…/scratchpad/home-branch`, a link in the flow 3ec648 scratchpad.
- `xp12f872…-home-manager-generation` (rollback): its roots were `~/.local/state/home-manager/gcroots/current-home`,
  `…/gcroots/new-home`, `~/.local/state/nix/profiles/home-manager-1039-link`, and the 3ec648 scratchpad `home-main`.

## Commands

```
mkdir -p /home/li/.local/state/f1c841/gcroots
nix-store --add-root /home/li/.local/state/f1c841/gcroots/hm-candidate-orchestrate-0.36.1 --indirect -r /nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation
nix-store --add-root /home/li/.local/state/f1c841/gcroots/hm-rollback --indirect -r /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation
nix-store -q --roots <each path>
ls -la /nix/var/nix/gcroots/auto | grep f1c841
```

## Output (after)

```
/home/li/.local/state/f1c841/gcroots/hm-candidate-orchestrate-0.36.1 -> /nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation
/home/li/.local/state/f1c841/gcroots/hm-rollback -> /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation

== /nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation
/tmp/claude-1001/-home-li-primary/3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3/scratchpad/home-branch -> /nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation
/home/li/.local/state/f1c841/gcroots/hm-candidate-orchestrate-0.36.1 -> /nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation
== /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation
/home/li/.local/state/home-manager/gcroots/current-home -> /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation
/tmp/claude-1001/-home-li-primary/3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3/scratchpad/home-main -> /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation
/home/li/.local/state/nix/profiles/home-manager-1039-link -> /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation
/home/li/.local/state/f1c841/gcroots/hm-rollback -> /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation
/home/li/.local/state/home-manager/gcroots/new-home -> /nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation

/nix/var/nix/gcroots/auto entries:
0w4qb82m0sy5ycksz1pgp9lmxwcpz2zr -> /home/li/.local/state/f1c841/gcroots/hm-rollback
k2f9c2yvsg0kkif4gmjz8qyfawl5skjp -> /home/li/.local/state/f1c841/gcroots/hm-candidate-orchestrate-0.36.1
```

## Result

Both store paths now have a root outside /tmp, under `~/.local/state/f1c841/gcroots/`.
These roots last until someone deletes the links in that directory. Once the morning
ruling is settled and the generations no longer need holding, deleting the two links
is all the cleanup required.
