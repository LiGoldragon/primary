# Flow 0.60.1: hnc2 source and gate request

## Immutable source
- Repository/worktree: `/git/worktrees/flow-reminder-7b5174`, branch `reminder-link-7b5174`.
- Published commit: `cda44973b69ba36d0765cfd64be80c19abef4098`; parent `ec4eb9356e9441aec58bee94810d7e67014cbf0b`; worktree clean after push.
- Reservation 417 remains held for the same permaflow; successor 2b25fa adoption explicitly confirmed by Opus epvq and Core zg23. Packet reservation 422.

## Anatomy and source review
- `crates/flow-nexus/ethos/send_tool.ethos`: internal SendKind adds Done.RequestId. Generated `src/generated/send_tool.rs` changes by exactly that variant; no public wire, Memory, Cargo or flake change.
- `src/send_tool.rs`: tool declaration and parser admit Result and Done with request. BecomesRequest/BecomesMessage now produce public SendableRequest/SendableMessage. The actual handler calls the existing `resolve_sendable_message` before answer_route, including the kept-answer branch. The resolver supplies the original logical id, validates open/delivered binding and distinguishes Result for Order/Question from Done for Task. The old empty logical-id construction is gone.
- `src/store/logical_delivery.rs`: ordinary Done admission uses the binding instead of requiring a reminder. The existing atomic closure commit retracts the reminder only when present, as the tool path already does. This preserves Done after Silence and keeps closure/reminder removal atomic.
- Inherited lock-order review: ordinary admission explicitly drops `_handover_guard` and `_guard` before withdrawing reminder Notices; tool admission drops `_guard` before doing so. Silence calls close_reminder to completion, then withdraws Notices under the dispatch gate; close_reminder retains no store write gate across that return. No additional lock-order change was needed. This is static review, not concurrency execution proof.
- `crates/flow/src/hook.rs`: replaces the complex fixture tuple with named ProcessRow fields; no lint allowance or production behavior change.

## Fixtures and evidence boundaries
- `tests/unit/queue_operations.rs`: actual JSON/parser/handler Result-to-Task refusal and ordinary parity for addressed, Unbound, Flow and Unknown origins; correct tool Done closes those Tasks and removes schedules. Silence then Done runs both ordinary and tool paths for those origins, verifies Open then Answered, no schedule, replay stability, and second-answer refusal. A separate handler fixture covers undelivered/unknown/closed requests, Done-to-Order refusal, and the routed Result original logical identity.
- `tests/unit/send_tool.rs`: declaration conditional now names Result and Done; parser fixtures cover Done with id, missing id and wrong id type.
- These fixtures are UNRUN. Baseline regression expectations are source-derived, not observed failing tests: ec4eb935 incorrectly accepts tool Result/Task, parses Done as malformed, and refuses ordinary addressed Done after Silence. No baseline compilation or candidate test pass is claimed.
- Formatting and `git diff --check` passed. No build, cargo test, clippy or Nix gate has run in this flow.
- Generation used existing `/nix/store/i3q64y2k95qkkgxa4khyxa6lzk6s24pb-rust_ethos-zero-29.0.0-bin/bin/ethos-zero`. Its derivation source `/nix/store/pf0hfh43ihyfdll14v3sf4l6m67ggcja-ethos-zero-29.0.0/src` compares byte-for-byte equal to cached git source f23eacf338a90ce4a6dea011554724fa6488fcc9 src. Generated output contains exactly the new variant; nothing generated was edited by hand.

## Requested gate and resource-control decision
One whole per-crate Nix gate, no separate cargo compilation, against the published immutable commit above. The gate evaluates and builds remotely and downloads no result. Candidate command, NOT STARTED and NOT a complete resource harness:

```sh
nix run github:Mic92/nix-fast-build -- --remote prometheus \
  --no-nom --no-download --eval-workers 1 \
  --flake 'github:LiGoldragon/flow?rev=cda44973b69ba36d0765cfd64be80c19abef4098#checks.x86_64-linux'
```

Core zg23 reports no verified daemon-contained capped harness. A client-unit MemoryMax does not contain Nix-daemon builds. Therefore this packet requests either an accepted exact daemon-contained resource envelope or an explicit Psyche exception before Core grants the slot. The required floor is 24 GiB; available memory, safe limit, aggregate overlapping build allocation and mechanism are not verified here. The command above alone supplies no such guarantee. No heavy job may start on its authority.

On grant, send exact revision, invocation, enforced scope/limits and process/log locations directly to Core and Field at start. Wait for terminal exit as an event. Send terminal status, process-ended and scratch-cleanup receipts directly to both. Freeze source throughout. Green checks are required before main landing/Field handoff; Field owns switches. Source is ready for review, not gated or released.

## Following work
Opus epvq orders the named meta overrides after 0.60.1: inspect `flows/1e2133/proposals/overrides-2.md` and build the missing ones, preserving existing CloseRequest. Earlier 5f30 queues the Living Reading-field contract release; epvq supplies the newer next-work order. Neither lane has been edited here. Do not reopen historical carried requests without current direction.

## Resource exception and exact revised gate proposal (Core a2df)
Core reports Psyche kuh4 plus 3lvq permit daemon work outside the client envelope, withdraw the memory watcher, and require one heavy phase at a time, bounded start/exit and kernel OOM backstop. This supersedes the earlier need to prove a daemon-contained cap; it does not grant this gate. Subscription has the current preparation grant; this run waits for its terminal/cleanup and Core's explicit grant.

Independent review `/tmp/flow0601-source-review.TrseIa/report.md` names exact commit/parent/tree above, SOURCE-READY/UNRUN, no introduced findings. Queued duplicate review ear8 was cancelled, `Cancelled.ear8`.

Proposed owner: Mind flowNexus Sol, current flow 2b25fa. One immutable whole check gate, no baseline build, cargo duplicate, concurrent gate, local evaluation or compilation. Use the already present nix-fast-build 2.0.4 executable below rather than invoking another tool build. Parameters submitted for Core acceptance: 90-minute wall limit; INT then KILL after 60 seconds; one gate worker, one eval worker, one Nix build job and two cores. The 2048 MiB eval recycle setting is not a memory cap. No 24 GiB reserve or daemon memory ceiling is claimed under the exception.

```sh
# SCRATCH is a new mktemp directory, made only after grant.
setsid timeout --signal=INT --kill-after=60s 90m \
  /nix/store/hpnzk4zly83kir2gli94ai6yhm9nxw0y-nix-fast-build-2.0.4/bin/nix-fast-build \
  --remote prometheus --no-nom --no-download --no-link \
  --max-jobs 1 --eval-workers 1 --eval-max-memory-size 2048 \
  --option max-jobs 1 --option cores 2 --option timeout 5400 \
  --result-file "$SCRATCH/result.json" \
  --flake 'github:LiGoldragon/flow?rev=cda44973b69ba36d0765cfd64be80c19abef4098#checks.x86_64-linux' \
  >"$SCRATCH/gate.log" 2>&1 &
gate_process=$!
printf '%s\n' "$gate_process" >"$SCRATCH/gate.pid"
wait "$gate_process"
```

The owning flow waits on command completion as an event. It sends the exact PID/process group, revision, start time, scratch/log paths and exception to Core/Field directly. Timeout exit, failure, OOM, source drift or a stop order is terminal, not grounds to restart. On owner stop, send INT to the recorded gate process group only; allow the same 60-second cleanup window, then KILL remaining members of that same group. Never kill by a broad executable-name match or stop the shared daemon.

After terminal, record exit and end time, inspect the recorded local process group and attributable remote ssh/eval/build clients once, and reconcile any remaining derivation against this gate's log before releasing the slot. Closing clients is not proof daemon-owned builders ended. If they remain or attribution is uncertain, retain the slot and ask Core/Field to finish supported cancellation; report the gap rather than claiming cleanup. nix-fast-build's remote_temp_dir context normally removes its own remote scratch; on interrupted cleanup, remove only its exact recorded directory after checking no owned process uses it. Preserve returned logs/results as evidence, then remove the owned scratch only. Send terminal, owned-process and scratch-cleanup receipts directly to Core and Field; no slot release until those boundaries are verified. This proposal is NOT STARTED.

## Granted attempt: immediate authentication failure
Core baw2 granted one attempt after Subscription terminal/cleanup. Exact accepted command ran at 2026-11-18T20:07:26Z, gate PID/process group 604741; terminal 2026-11-18T20:07:27Z, exit 1. nix-fast-build failed during parse_args/get_nix_config, before evaluation, remote temporary-directory creation or derivation submission. Its SSH error was `li@prometheus.goldragon.criome: Permission denied (publickey,keyboard-interactive).` No check failed attribute list or test result exists; this is not a source gate result.

The command was executed through a non-login bash wrapper. Read-only `ssh prometheus` from the normal login zsh tool path succeeded immediately before and after; why the NFB invocation lacked successful authentication remains UNKNOWN, not a source defect established. No gate retry was attempted. Core/Field received immediate START/terminal notices p5bw/rmen.

Local recorded PGID 604741 is empty after terminal. One read-only remote process snapshot found no nix-fast-build/nix-eval-jobs/rustc/clippy-driver. No daemon build could have been submitted before the failed initial get_nix_config; therefore no candidate-owned daemon derivation or remote workload scratch exists. Gate log and timing/PID/exit evidence were copied to a separate temporary evidence directory; the original workload scratch `/tmp/flow0601-gate-2b25fa.2zIcWI` was removed and absence verified. Authentication diagnosis and a NEW explicit start grant are required before another attempt; no source mutation, build or retry follows automatically.

## Supported authentication correction proposal
Core 57ws accepted the prior terminal/process/scratch receipt and RELEASED the slot. Field ztyr/nkyi reproduced the same-route authentication contrast using actual tool environments: nonlogin bash selects the gcr socket and fails BatchMode ssh true with 255; normal login zsh selects the gnupg SSH agent socket and succeeds with 0. Both sockets exist. NFB does not override SSH_AUTH_SOCK; its prefixed dependency paths contain no ssh. The original failed-process environment was not captured, so that historical cause is qualified.

Submit the SAME immutable gate command and limits through `exec_command` with `shell: /bin/zsh, login: true` (the ordinary successful environment), instead of `shell: /bin/bash, login: false`. No host, route, executable, gate parameter, source, credential or hardwired socket change. The shell wrapper creates scratch, records start/PID, waits for the child exit and records terminal as before. This is a proposal, not another attempt; a NEW Core grant is required. Field owns any further auth diagnosis. Source remains clean cda44973.
