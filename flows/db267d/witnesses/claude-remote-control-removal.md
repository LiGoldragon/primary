# Claude Remote Control removal

## Method

Fresh `jj git clone --colocate` of each repo's `origin/main` into
`~/wt/github.com/LiGoldragon/CriomOS-home-db267d` and
`~/wt/github.com/LiGoldragon/CriomOS-db267d`; no existing checkout was reused.
Referent located by repository-wide grep, then read before deletion. Evaluation
only — no build of the VM test suite, no deployment, no live host touched.

Both flakes stub their `system` input and throw until a deploy tool
materializes one. For evaluation only, a two-line flake whose sole output is
`system = "x86_64-linux"` was written to the session scratchpad and supplied
with `--override-input system`. `NIXPKGS_ALLOW_UNFREE=1` plus `--impure` were
needed because Home's package set contains unfree entries. `--no-write-lock-file`
kept the override out of the committed locks.

## What the referent is

`modules/home/profiles/min/claude-remote-control.nix` in CriomOS-home: a
home-manager module gated on `user.size.min`, declaring the systemd user service
`claude-remote-control` with `Restart=always`, `RestartSec=2s`,
`ExecStart=… claude remote-control --spawn=… --permission-mode bypassPermissions`,
and the options `criomos.claudeRemoteControl.workingDirectory` / `.spawn`.

Nothing in either repo ever set those options; every consumer took the default
`$HOME/primary`. No host or user profile enables it separately — the minimum
profile import was the only switch, so bird and li received it through
`modules/home/default.nix`.

`codex-remote-control` is a different module
(`modules/home/profiles/min/agent-intercom.nix`) declaring a different unit from
a different package. The two share no code. Untouched.

## Removed — CriomOS-home

- `modules/home/profiles/min/claude-remote-control.nix` (deleted)
- `checks/claude-remote-control/` (deleted)
- `modules/home/default.nix`: the module import
- `flake.nix`: the `"claude-remote-control"` entry in `ownedCheckNames` and the
  `checks.claude-remote-control` `callPackage`
- `ARCHITECTURE.md`: the persistent-owner paragraph, replaced by a statement
  that Home declares no such owner
- `UPGRADES.md`: the `## Persistent Claude Remote Control` section deleted; the
  Fable 5.1 section rewritten to drop owner-restart guidance; a new
  `## Claude Remote Control removal` section added

## Removed — CriomOS

- `checks/lojix-ownership/default.nix`: the `claudeRemoteControl` binding and
  its `WorkingDirectory` / `Restart` / `UMask` assertions, replaced by negative
  assertions that no projected user has a `claude-remote-control` service
- `flake.nix` + `flake.lock`: `criomos-home` pin advanced
  `08717ef8950e514c346cbdfbc69143e4369056fb` → `1ae5da86099e323cda8f79ab239ca4efaa12ce47`
  (Home's `chroma` follow moved with it, a consequence of the pin)
- `checks/lojix-ownership/default.nix`: `expectedHomeRevision` follows the pin

## Coupling found

`checks/lojix-ownership/default.nix` in CriomOS was the one place asserting both
remote controls together. It is a shared assertion site, not shared machinery;
the Codex half is byte-identical to before.

`checks/bird-home-isolation/default.nix` in CriomOS-home asserts
`codex-remote-control` only — no Claude reference, unchanged.

## Evaluation

### CriomOS-home — check surface no longer names the removed check

Baseline, `origin/main` before the change:

```
$ NIXPKGS_ALLOW_UNFREE=1 nix eval --impure --no-write-lock-file \
    --override-input system path:$SP/system-input --raw \
    'github:LiGoldragon/CriomOS-home/654144d71a51f92bba56e405faab3243e2dce4ba#checks.x86_64-linux' \
    --apply 'cs: builtins.concatStringsSep "\n" (builtins.map (n: n) (builtins.attrNames cs))'
$ grep -n 'claude-remote-control' base-names.txt
12:claude-remote-control
$ wc -l base-names.txt
77
```

After the change, in the worktree:

```
$ NIXPKGS_ALLOW_UNFREE=1 nix eval --impure --no-write-lock-file \
    --override-input system path:$SP/system-input --raw \
    .#checks.x86_64-linux \
    --apply 'cs: builtins.concatStringsSep "\n" (builtins.attrNames cs)' \
  | grep -c 'claude-remote-control'
0
```

### CriomOS-home — Home configurations still evaluate

Forcing `drvPath` on the checks that materialize home-manager configurations,
i.e. the consumers that imported the deleted module:

```
$ NIXPKGS_ALLOW_UNFREE=1 nix eval --impure --no-write-lock-file \
    --override-input system path:$SP/system-input --raw .#checks.x86_64-linux \
    --apply 'cs: builtins.concatStringsSep "\n" (builtins.map (n: n + " -> " + builtins.baseNameOf cs.${n}.drvPath) [ "bird-home-isolation" "codex-remote-control" "system-projection-boundary" "agent-intercom" "ai-agent-launch-orchestration" "pi-harness-profile" ])'
bird-home-isolation -> …-bird-home-role-isolation.drv
codex-remote-control -> …-codex-remote-control-contract.drv
system-projection-boundary -> …-system-projection-boundary.drv
agent-intercom -> …-agent-intercom-integration-contract.drv
ai-agent-launch-orchestration -> …-ai-agent-launch-orchestration.drv
pi-harness-profile -> …-pi-harness-profile.drv
```

All six evaluated to derivations. Store hashes are omitted here on purpose.

Forcing the whole CriomOS-home check set stops at
`checks/orchestrate-wrapper-fallback/default.nix:35` (`attribute 'config'
missing`). That check is untouched by this change and fails the same way on the
unmodified parent revision.

### CriomOS — text

```
$ grep -rIn -e 'claude-remote-control' -e 'claudeRemoteControl' . \
    --exclude-dir=.git --exclude-dir=.jj
(no output)
```

### CriomOS — lojix-ownership contract

`origin/main` (57ec0138), unmodified, already fails this check before any change
of mine:

```
$ NIXPKGS_ALLOW_UNFREE=1 nix eval --impure --no-write-lock-file \
    --override-input system path:$SP/system-input --raw \
    "git+file://$PWD?rev=57ec0138…#checks.x86_64-linux.lojix-ownership.drvPath"
error: string '"08717ef8950e514c346cbdfbc69143e4369056fb"' is not equal to
       string '"c40ff0cde736a4b092b7c713571afce40361a395"'
```

That is `expectedHomeRevision` drift, fixed by this change's pin advance. The
next assertion in the same file is drift I did not cause and did not touch:

```
$ git show origin/main:checks/lojix-ownership/default.nix | grep expectedOrchestrateRevision
  expectedOrchestrateRevision = "9585484738ce0748d0cf23f0431285f9693ca2ec";
root  flake.lock orchestrate rev = 5f016531e765d9b679a86cc47a2d75eaca43d624
home  flake.lock orchestrate rev = ac8a92666f4abd8356522c4d52ab23ddcdff4c15
```

The check asserts CriomOS and CriomOS-home share one Orchestrate lock. They do
not; the two locks disagree with each other and with the expectation. No single
value satisfies it, so this cannot be repaired by editing the expectation, and
repinning Orchestrate is outside this task. Reported, not guessed at.

To evaluate my own assertions past that pre-existing block, the four pin
assertions were temporarily disabled in the worktree (probe only, reverted
before commit — the pushed file contains them unchanged):

```
$ NIXPKGS_ALLOW_UNFREE=1 nix eval --impure --no-write-lock-file \
    --override-input system path:$SP/system-input --raw .#checks.x86_64-linux \
    --apply 'cs: … cs.${n}.drvPath …'
error: MS2130 UVC patch must be reviewed for the selected kernel
```

`lojix-ownership` sorts before `ms2130-uvc-aspect-quirk`, so it was forced and
passed: the negative `claude-remote-control` assertions hold and the Codex
assertions still hold.

Control — the identical probe applied to a detached worktree of unmodified
`origin/main` (57ec0138):

```
$ git worktree add --detach $SP/criomos-baseline origin/main
HEAD is now at 57ec013 Pin Orchestrate framed Datom Signals
$ NIXPKGS_ALLOW_UNFREE=1 nix eval --impure --no-write-lock-file \
    --override-input system path:$SP/system-input --raw .#checks.x86_64-linux \
    --apply 'cs: … cs.${n}.drvPath …'
error: MS2130 UVC patch must be reviewed for the selected kernel
```

Same failure, same point, on the unmodified baseline. The MS2130 check needs a
lojix-materialized kernel selection that a synthesized `system` input cannot
supply. This change introduces no new evaluation failure in CriomOS.

## Pushed revisions

- CriomOS-home `main` = `1ae5da86099e323cda8f79ab239ca4efaa12ce47`
  ("Remove the Claude Remote Control server")
- CriomOS `main` = `a48f9cb843f7107772b3b5405bdeadfef06fc038`
  ("Drop Claude Remote Control from the OS contract")

Producer pushed before consumer. Not deployed.

## Residual, for the flow to decide

An account that already ran the previous generation keeps the unit running
after activation; home-manager removes it from the managed set but does not stop
a live unit. `systemctl --user disable --now claude-remote-control.service` on
each such account, once, at deploy time. Recorded in CriomOS-home `UPGRADES.md`.
