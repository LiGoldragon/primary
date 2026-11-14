# Account: Chronos Phase-1 entry transplant publication

## Accepted artifact

- Repository: `git@github.com:LiGoldragon/chronos.git`
- Base: `679fa1865a3d85a28524d406d387627cf3b58896`
- Accepted revision: `66f22a20e104d5110acb6af3b2f2ca1585b50356`
- Change: `rttlrmttspxkpyulkvvuktwzmryrywyz`, `Own Chronos entry mechanics`
- Independent immutable diff review: passed exact `66f22a20`.
- Field consumer/dependency readback: passed exact `66f22a20`.
- Core acceptance and later publication grant applied only to experimental `refs/heads/entry-point`.

## Custody and before state

`orchestrate 'Observe.Locks'` showed lock `25515 ChronosEntryTransplant`, Flow `54420d`, owning only `/git/github.com/LiGoldragon/chronos-inbound-frame-limit-54420d` immediately before publication.

The workspace was clean, its parent was exact accepted revision `66f22a20`, and its content differed from that revision by no path. Local `entry-point` and actual remote `refs/heads/entry-point` were both exact base `679fa18`. Origin was exact `git@github.com:LiGoldragon/chronos.git`. Remote `main` and `chronos-datom-542442` were both `a5cf51f440a722c60963a5f1a0ea95bb3251ddb0`.

Evidence: `/tmp/chronos-entry-transplant-66f22a2-publication-before.txt`, SHA-256 `59b2339ab2b8a6b922cf537e53164141aca40d6a1ba60f84716bbd87dfc82462`.

## Publication

Only the experimental `entry-point` bookmark was moved by strict fast-forward, from `679fa18` to its direct child `66f22a20`, then pushed to origin with:

```text
jj bookmark set entry-point -r 66f22a20e104d5110acb6af3b2f2ca1585b50356
jj git push --remote origin --bookmark entry-point
```

The push reported `entry-point [move forward from 679fa1865a3d to 66f22a20e104]` and exited successfully. No merge, rebase, force, other bookmark, tag, version, release, or deployment operation ran.

Evidence: `/tmp/chronos-entry-transplant-66f22a2-push.log`, SHA-256 `4603de1afca7d7cae4d309a7e8172a01e0f021c01d2ca4fe27ae2e32de76471f`.

## Readback and release

Local `entry-point`, `entry-point@git`, `entry-point@origin`, and actual `git ls-remote` remote `refs/heads/entry-point` read back exact `66f22a20e104d5110acb6af3b2f2ca1585b50356`. Remote `main` and `chronos-datom-542442` remained exact `a5cf51f440a722c60963a5f1a0ea95bb3251ddb0`. The before/after remote-head diff contains exactly the deletion of the old entry-point line and addition of the new entry-point line.

The artifact workspace remained clean and content-identical to `66f22a20`; the canonical Chronos root remained clean detached. The Nexus candidate remained on `28efec-nexus-lifecycle` with its pre-existing foreign untracked `ethos/`, untouched.

Lock release returned:

```text
Released.{ 25515 ChronosEntryTransplant 54420d [ /git/github.com/LiGoldragon/chronos-inbound-frame-limit-54420d ] «Transplant approved Nexus entry mechanics into Chronos for isolated review» }
```

A following `Observe.Locks` showed lock 25515 absent.

Evidence:

- `/tmp/chronos-entry-transplant-66f22a2-publication-after.txt`, SHA-256 `0d60985ad9b1a4204ea9487315207dd64fcf5916ef91438fd1898c7af45e9177`
- `/tmp/chronos-entry-transplant-66f22a2-heads.diff`, SHA-256 `2ff75836f8fe790e82afc105277f339b6198dfb321fc502c8023f69a46022eb8`
- `/tmp/chronos-entry-transplant-66f22a2-release.txt`, SHA-256 `b115245d30b59b70a9a5dee419f7d46ff9f8dc670a0bfe310716fbc18b12ac8a`

## Checks and recorder correction

The exact post-review composed command requested all six checks with Prometheus builders and no local jobs:

```text
nix build .#checks.x86_64-linux.build .#checks.x86_64-linux.test .#checks.x86_64-linux.doc .#checks.x86_64-linux.fmt .#checks.x86_64-linux.clippy .#checks.x86_64-linux.ethos-source --builders @/etc/nix/machines --max-jobs 0 --no-link -L
```

In the first post-review invocation, build, doc, fmt, clippy, and ethos-source actually executed on Prometheus. The exact-source test derivation was already cached from the preliminary corrected-source test run, where every unit, integration, process, lifecycle, and doctest passed. Nix completed successfully; afterward the recording zsh exited 1 because the script assigned its reserved read-only variable `status`. This recorder failure happened after the Nix pipeline and did not represent a check failure.

The command was immediately rerun under `set -o pipefail` using variable `gate_exit`. All six exact outputs were then cached, and the composed invocation recorded `FINAL_EXIT=0`. No source or revision changed between these invocations.

Evidence:

- Actual remote execution log `/tmp/chronos-entry-transplant-66f22a2-final-composed.log`, SHA-256 `9f8706c8dfcf3f716854cf751b06e02ca4392c5be44d016d9e47a23fb1997898`
- Successful composed retry `/tmp/chronos-entry-transplant-66f22a2-final-composed-retry.log`, SHA-256 `579d8cca6c71925fddc6c8988dba80071b6f3ffbbcc700428f70fc01044e6b23`
- Exact-source test execution `/tmp/chronos-entry-transplant-54420d-preliminary-test.log`, SHA-256 `90749a668e17a694be214b96caf1f87c1ab8c5269542e9ec0eaea53634befe17`

Green outputs were chronos-build `w80riw4m…`, chronos-test `3hxpinfm…`, chronos-doc `js5s7z1n…`, chronos-fmt `77p574bm…`, chronos-clippy `fdw4hccc…`, and chronos-ethos-source `m1p72a59…`.

## Package consequence

The crate remains `chronos 0.3.0`. The artifact removes direct git dependency/package node `nexus 0.5.0 @ ec097e3` and makes the already-resolved runtime crates direct: `kameo = 0.22` resolved 0.22.2 and `rustix = 1` with `process` resolved 1.1.5. Tokio stays direct at resolved 1.53.2 with its existing feature superset. The lock graph has one fewer package node and no newly resolved crate version.

## Accepted scope

This publication is the Phase-1/location entry transplant only. It owns the cohesive entry mechanics in the existing Chronos library boundary, keeps explicit inbound `FrameLimit` with startup default 1048576, preserves Ctrl-C and SIGTERM cleanup behavior, and leaves wire behavior separate.

It does not establish the full Chronos service or deployment. Mutable per-value configuration, its second independently served typed meta Signal, Memory-backed configuration persistence, time, schedule, subscriptions, package release, and deployment remain unfinished. The future direction is two independently served typed Signal surfaces sharing the same OperationHandle and Memory; meta follows signal to operation to Memory, RunningTask stays lifecycle-only, Memory is the sole durable per-value owner, and no whole-configuration Configurable is introduced without its separate specification.
