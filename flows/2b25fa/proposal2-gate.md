# Proposal 2 — exact 0.60.1 whole-gate packet

Prepared by actual current owner01a511 after RefreshRejected.Locked. Source
reservation427, packet422. Core dw8q/Psycheig50 authorize own release metadata;
this packet requests exact metadata review and whole-gate custody/admission.

## Immutable candidate

`/git/worktrees/flow-order-lifetime-2b25fa`, branch order-lifetime-2b25fa,
**7a97f37c01ddcd431b05725c0758d0da81016ad7**, parent
**20ca7d8b77dc2618bb1ada46262c352a53da5026**, which independently passed
Proposal2 source review `/tmp/order-lifetime-audit.l9U4PX/report.md`.
Clean after commit. No publication/merge/runtime action. Answer read exception
is ruled on8b/0dfu, unchanged in this candidate.

The exact metadata delta is FOUR replacements0.60.0→0.60.1:
- crates/flow-nexus/Cargo.toml package version;
- Cargo.lock flow-nexus package version;
- Cargo.nix flow-nexus package version;
- flake.nix package version.

Dependency versions/features/pins, flake.lock, crate-hashes.json, all other
members and generated schemas are unchanged. No reminder source is included.
The four files reuse the byte-identical already-generated metadata artifact
from frozen cda44973, whose complete Cargo manifests, Cargo.lock, Cargo.nix,
crate-hashes.json and flake.lock match this candidate byte for byte. This is
artifact reuse, NOT a claim of a fresh generation run: no generator/build
was started. `checks.cargo-nix` must prove current offline regeneration in
the immutable full gate. If policy requires a separate fresh generation,
Core must grant that exact bounded phase before accepting this candidate.

Recheck commands (read-only):
```sh
cd /git/worktrees/flow-order-lifetime-2b25fa
git status --porcelain
git diff 20ca7d8b 7a97f37c -- Cargo.lock Cargo.nix crates/flow-nexus/Cargo.toml flake.nix
git diff cda44973 7a97f37c -- Cargo.toml ':(glob)crates/**/Cargo.toml' Cargo.lock Cargo.nix crate-hashes.json flake.lock
```
The second diff must contain four version replacements; the third must be
empty. None stands for the authored tests having run.

## Exact proposed whole gate — NOT STARTED

Core owns final execution/admission. Psycheig50 reports Field trace ended;
Core must reconcile its resource-terminal event before admitting this phase.
No concurrent phase, baseline build, local evaluation/cargo or automatic retry.
Use an unpublished immutable git+file source, not a remote URL falsely
claiming that this commit was published. Nix-fast-build copies the committed
source store path to the builder. Same supported normal loginzsh SSH route
as predecessor correction; no credential/socket hardwiring.

```sh
# Run only after Core's exact review/admission; through login /bin/zsh.
ssh -o BatchMode=yes prometheus true || exit
SCRATCH=$(mktemp -d /tmp/flow-order-gate-01a511.XXXXXXXX)
printf '%s\n' 7a97f37c01ddcd431b05725c0758d0da81016ad7 > "$SCRATCH/revision"
date -u +%FT%TZ > "$SCRATCH/start.utc"
setsid timeout --signal=INT --kill-after=60s 90m \
 /nix/store/hpnzk4zly83kir2gli94ai6yhm9nxw0y-nix-fast-build-2.0.4/bin/nix-fast-build \
 --remote prometheus --no-nom --no-download --no-link \
 --max-jobs 1 --eval-workers 1 --eval-max-memory-size 2048 \
 --option max-jobs 1 --option cores 2 --option timeout 5400 \
 --result-file "$SCRATCH/result.json" \
 --flake 'git+file:///git/worktrees/flow-order-lifetime-2b25fa?rev=7a97f37c01ddcd431b05725c0758d0da81016ad7#checks.x86_64-linux' \
 > "$SCRATCH/gate.log" 2>&1 &
gate_process=$!
printf '%s\n' "$gate_process" > "$SCRATCH/gate.pid"
# Send Core+Field START: revision, command, PID/PGID, scratch/log/start time.
wait "$gate_process"
gate_exit=$?
printf '%s\n' "$gate_exit" > "$SCRATCH/exit"
date -u +%FT%TZ > "$SCRATCH/end.utc"
# Terminal receipts and attributable process/scratch reconciliation follow.
```

One evalworker/buildjob/two cores,90m wall/5400s per derivation, INT→KILL60s.
2048MiB eval recycle is NOT a total memory cap. Psyche's accepted daemon
exception/OOM backstop applies; no extra floor/reserve claim. The owner waits
on completion as an event and directly sends Core+Field terminal exit,
failedattributes, exact attributable local/remote process status and scratch
cleanup. Attribution uncertainty retains the slot; no broad executable-name
kill, daemon stop, retry, extension or next phase. Preserve logs/results
outside removed workload scratch. No silent assertion that ended clients mean
all daemon-owned builders ended.

## Required acceptance after gate

Whole `checks.x86_64-linux`, including cargo-nix and ALL authored fixtures,
is the gate; static SOURCEPASS is no substitute. Only a green immutable gate
advances to reviewed isolated native bootstrap/matrix, one nonwriter audit of
commit+evidence against Proposal2, Psyche acceptance, then main/next switch.

Bootstrap is our task under zttr, not yet executable. Credential ruling5pje
now permits private CODEX_HOME/auth.json symlink to the single production
auth.json, expressly no device-login/copy; source must first verify the actual
installed auth-save/refresh follows its linked target. No auth contents have
been read or any link created. Every other Home/config/session/socket/Memory/
Herdr/Curriculum boundary stays private. Native binary is pinned by Fieldxt8o
at `/nix/store/z5fprnr4ny9rgk8yn3f5s4vaj84ak76x-codex-next/bin/codex-next`,
version0.161.0-alpha.2. Native model/effort is a bounded frozenConfiguration
read, not a guessed collaboration label. Field runs only reviewed commands.

Eventual narrow live activation includes all Ouranos ordinary0.68 peers and
Energy, no67backport; Core consolidates source inventory, Field actualruntime
inventory. No production configuration replay or assumed0.60.0 equivalence.
