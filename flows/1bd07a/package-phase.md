# Proposal 2 — one bounded package resolution/materialization phase

Requested by Core cspb; authorization is pending. This phase changes no source, pins, refs, Memory, credentials or service. It launches no native flow. Core uu6e reports Psyche accepts the independent source/command/results witness; there is no stamped-check rebuild in this request.

## Immutable inputs and exact scope

Published source: `github:LiGoldragon/flow?rev=fe5a6930871707a7086c9a647867a519734220ef`, remote candidate readback recorded in `source-publication.md`. Its committed flake.lock pins base `7fca4d583adfd2354903c59cbc7f5e928e1baa76`, Curriculum `60609c55f90432782625275294636a4e396d9497`, translator `6892a15b11653a2ef8932a4390b34f5e81583744`. No override input or copied tree is used.

Only these three actual package attributes are selected:

- `packages.x86_64-linux.default`: complete Flow workspace binaries, NOT checks.default.
- `packages.x86_64-linux.curriculum`: that exact pinned Curriculum package, NOT curriculum-cargo-nix.
- `packages.x86_64-linux.nexus-configure`: the pinned translator's place compiler.

I read the actual pinned flake definitions and installed NFB2.0.4 help. Its supported `--select` filters the evaluation root before jobs. The local machine reads flake metadata; NFB `--remote` evaluates and builds on Prometheus. Omitting `--no-download` deliberately materializes these three outputs locally for the isolated driver. Dependencies are reused by derivation; no alternate build/copy-executable fallback or gate rerun is allowed.

## Proposed exact workload command

Create one fresh `/tmp/flow-packages-1bd07a.XXXXXXXX` scratch directory and retain its absolute path, source/readback/lock pins and start/end receipts. The full command is:

```sh
timeout --signal=INT --kill-after=60s 45m \
 /nix/store/hpnzk4zly83kir2gli94ai6yhm9nxw0y-nix-fast-build-2.0.4/bin/nix-fast-build \
 --remote prometheus --no-nom --no-link --retries 0 --fail-fast \
 --max-jobs 1 --eval-workers 1 --eval-max-memory-size 2048 \
 --option max-jobs 1 --option cores 2 --option timeout 2400 \
 --select 'packages: { inherit (packages) default curriculum nexus-configure; }' \
 --result-file "$SCRATCH/result.json" \
 --flake 'github:LiGoldragon/flow?rev=fe5a6930871707a7086c9a647867a519734220ef#packages.x86_64-linux' \
 > "$SCRATCH/packages.log" 2>&1
```

Maximum whole phase:45 minutes, INT then KILL60 seconds; derivation deadline2400 seconds, one build job/two cores, one evaluator/2048MiB. Zero retries. A transport, selection, evaluation, build or copy failure stops the phase; missing paths never cause a second build command. Metadata/source pins and source worktree cleanliness are rechecked before entry. The foreground command's terminal event is awaited.

## Ownership, cleanup and acceptance evidence

Primary1bd07a owns the phase and its evidence; Core owns the exclusive resource grant/release. Before starting, capture bounded local controller identity and remote nixbld/NFB/evaluator baseline. Launch the foreground timeout/NFB in one fresh process session, recording its exact live process identity and group; the retained controller forwards only to that still-owned live process group on interruption and waits for its terminal event. No executable-name or stale-PID kill is used. NFB owns its remote scratch cleanup. After exit, retain exact terminal code and perform bounded read-only local and Prometheus process reconciliation plus the exact NFB-owned remote scratch absence check from its retained command/log provenance. An uncertain remote child or failed cleanup retains Core's allocation; report rather than retry or name-kill.

Require exactly the selected three package attributes, successful EVAL/BUILD result entries and a successful local download/materialization, with concrete drv/output paths retained. For each exact local output record existence and executable metadata; require Flow's flow/flow-meta/flow-hook/flow-nexus-daemon, Curriculum's curriculum/curriculum-nexus and compiler's nexus-configure. Hash those executable bytes, retaining resolved targets and provider roots. Do not execute any of them. These results fill the final driver manifest; check aggregate paths, mutable copied capture directories and individually copied executables are refused substitutes.

Submit terminal result, exact outputs/local presence/hashes, cleanup and resource-release request to Core; copy Field the source-only final packet after acceptance. Neither this phase nor green packages grants native execution, auth-link creation, service start, deployment or switch.
