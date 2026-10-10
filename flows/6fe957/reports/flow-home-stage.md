# Flow 0.17.3 Home stage

Date: 2026-09-26. This is a staging receipt only. It does not authorize or
record a Home-main move, activation, deployment, release, tag, evaluation, or
build.

## Immutable inputs

The actual `LiGoldragon/CriomOS-home` remote `main` was read as
`5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`, the approved post-Messenger
base. The `LiGoldragon/flow` remote branch
`flow/0173-merge-56ae53` was independently read as
`0b512ee0b6681b1925fee7b6435aa7c2eac26bfb`.

That Flow commit's subject is `Merge Flow 0.17.3 Claude startup repair onto
main`; its checked `Cargo.toml` workspace version is `0.17.3`. The staged
lock records its source content hash at pin time as
`sha256-p/F8vLbS1UEPJ4BuL8VwczP5LrmS7qGl5ieMdu/ldtU=` and its lock timestamp
as `1790469756`.

## Isolated stage

The pre-existing directory named `flow-0173-stage-56ae53` is not a registered
Git worktree and contains the old stage, so it was not reused or merged. A
fresh Git worktree was created at
`/home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-0173-stage-56ae53-5ba2e1e`
on branch `flow-0173-stage-56ae53-5ba2e1e`, directly from the approved base.

The stage changes only these files:

- `flake.nix`: `flow-next` URL and the adjacent version comment.
- `flake.lock`: the matching immutable Flow revision, timestamp, and NAR hash.
- `checks/flow-message-next/default.nix`: its expected next-Flow revision.

It preserves the Messenger input
`93c12756f9c00dd3c13762590f17cee3a3712530` and the paired Message-next input
`481b579fcf72797ffa9ccf8ce4e2283a58cdff97`.

The isolated stage was committed as
`fccc26523589c9b40cd1aa1479e63c571fa4c061` and pushed to the real remote
branch `flow-0173-stage-56ae53-5ba2e1e`; a post-push remote ref read returned
that same immutable revision.

## Validation and gates

`git diff --check` passed. Static source inspection confirms the three-file
scope and the matching Flow, Messenger, and Message-next pins. No Nix
evaluation, check, or build was run under this assignment.

The imported-row confirmation capability is not established. Searches of the
available Flow source and Home staging material found no concrete imported-row
confirmation contract. Field Sol `9ac67c` was asked for the exact required
feature and owning component/version; Messenger returned
`Presented.{ 9ac67c idle }`, which is a transport state, not a semantic reply
or Field acceptance. Fable `8904b1` received the distinct stage-progress
notice with `Presented.{ 8904b1 done }`.

Remaining gates: explicit authority for any Flow IFD/evaluation/build; a
concrete imported-row confirmation feature requirement and owner; a Field
semantic reply and acceptance; and separate authority for any later main move
or activation.

2026-09-26T22:XX:XX-06:00 incoming request (verbatim):
New authorized bounded work from56ae53: run ONE full Home check on exact current real-remote Home main, local/public-cache settings excluding unavailable Prometheus cache, max-jobs=2 cores=2, preserving live generation. Candidate generation success is not full-check proof. First coordinate with Field9ac67c offline fixture owner via supported existing messaging route to avoid core contention; no route tests/replays. Inspect no duplicate active check. Freeze exact current/main identity, do not use dirty guarded-patch workspace contents: immutable clean main source with coherent frozen complete-host system+horizon+deployment+secrets references as appropriate. Preserve secrets-safe workflow, never print values. Use full IFD-enabled check (prior no-IFD intrinsically invalid), --impure --no-write-lock-file, empty builders and per-command public cache, bounded retained terminal/log with actual exit. No source edits, main move, activation, service action, live drop-in or global Nix settings changes. Read applicable worker instructions and skill requirements. Log incoming request verbatim to own report before work. Return exact source/overrides/command limits, coordination result, terminal result and log receipt; if blocked identify exact dependency and propose meaningful equivalent gate honestly bounded, not candidate-build substitution. Do not duplicate a prior run; wait for resource coordination if necessary. Report concise progress.

2026-09-26T23:01:00-06:00 coordination: sent one existing-route request to Field 9ac67c; receipt `Transported.{ 9ac67c working }` is transport-only. Field then issued a scheduling HOLD through main: offline sd-switch fixture and five-minute rollback drill subflows are active; no Home IFD check may start until an explicit fresh clear. No check/build process was started. Passive exact process inspection found no matching active Home check before this hold.

2026-09-26T23:XX:XX-06:00 Field ResourceClear relayed by main: rollback ended; offline sd-switch fixture reports no ongoing build/check; local cores clear. This is the explicit fresh scheduling clear for the one authorized full Home IFD check. No check started before recording this receipt.

2026-09-26T23:21:10-06:00 full IFD check terminal: exit 1. Retained PTY/log: /var/tmp/flow-home-check-6fe957-20260926-2305/pty.log. Started 23:03:56 with 1200-second bound but terminated normally before timeout. Clean source parent daf026f1e02bcd092f0ecc43b81207c96c6ec1b3; complete-host system/horizon overrides; public cache only; max-jobs=2, cores=2, builders empty. Root observed failures: agent-daemon-configuration drv exit65; mentci-deps-0.5.0 drv exit101 (meta-signal-criome build.rs unresolved BootstrapInterfaceGeneration); solar-time-widget exit1; active-network-widget exit1; cluster-relay-package exit1; session-variables exit1; listener-level-widget exit1. Dependent failures include agent-daemon-service, spirit-deployment, pkgs-mentci, and main-contract-pins. No activation or service operation occurred.
