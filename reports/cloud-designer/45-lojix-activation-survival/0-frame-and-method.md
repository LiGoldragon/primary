# 45 · Lojix activation + SSH-survival (S4) — grounding frame

## Goal

Make the lojix daemon actually **deploy a full OS**, and make a deploy
**survive an SSH disconnect** — the last big engineering stage before the live
e2e (S5). Today the activation path is stubbed: `activate_system` references an
unset `$CLOSURE` shell var, `CopyClosure`/`ActivateGeneration` are not
target-safe, and the reject-guard (`unsupported_deploy_reason`) rejects every
activating action (only System Eval/Build + Home Build are accepted). The
parity bar (Spirit `tvbn`/`up9q`, the report-9 baseline): carry the real built
closure through copy + activate, and port `lojix-cli`'s `systemd-run --collect`
PID-1 transient-unit BootOnce so the activation outlives a dropped session.

## Why ground first

Two intricate, correctness-critical pieces: (1) threading the real closure
through copy+activate and opening the reject-guard only for now-safe actions
without breaking the existing eval/build path; (2) the disconnect-survival
design across **two** surfaces — client→daemon (the CLI's socket drops
mid-deploy) and daemon→target (the daemon's ssh to the node drops) — mapped
onto Spirit `up9q` (a job actor owns the process + persists job state; no
blanket kill-on-drop) and the `lojix-cli` transient-unit reference. Get the
design pinned to the real code before writing it.

## Method

Read-only reconnaissance fan-out, each dimension a numbered file, then a
synthesis implementation plan. No mutation; no live deploy (that is S5).

Dimensions:

1. lojix's current deploy pipeline — the effect chain, the activation stub,
   where the built closure path lives, the reject-guard, the seam to change
2. `lojix-cli` BootOnce parity mechanism — the exact `systemd-run --collect`
   transient-unit + `nix copy --to ssh-ng` + boot-once-without-moving-default
   + EFI reconcile to port
3. disconnect-survival job model — `up9q`/`1lex`/`xv9v`/`kx32`, whether the
   current deploy is coupled to the connection task, and the triad-runtime
   job/actor model that lets a deploy outlive its request
4. synthesis — the S4 implementation plan + what is testable without a live
   target vs what needs S5
