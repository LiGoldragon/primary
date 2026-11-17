# Flow 0.56.3 — gated recovery release

## Cohort and custody
Published Flow revision fc7ecd9e1ec60caa4499c7db7676dc3bfe7d9828, branch recovery0563-56ca20, worktree /git/worktrees/flow-recovery0563-56ca20 (reservation377). Exact live61242e2dfe7db8f472e5b1d353f857d7d3bbc464 is its ancestor. Only flow-nexus crate version changes to0.56.3; unchanged members remain0.56.2. Ordinary64/meta83 and every dependency/base/flake pin remain unchanged. Base4ea69d1fc87c95e7c1f54d02b21166ffb3285edd; source flake.lock is authoritative. Field core Sol solely owns coherent Home/CriomOS pins, gates and Ouranos rollout. Capsule and370g remain held.

## Gate
Full immutable remote checks.x86_64-linux gate passed exit0,20 checks including default; flow-nexus1019 passed,8 ignored. Final evidence /tmp/flow0563-56ca20.qfTb15/{gate3-invocation.txt,gate3.log,gate3.exit}. It ran via nix-fast-build on Prometheus, one evaluation worker, no-download. Remote gate scratch removal reported. The earlier gate and gate2 failures were fixture compilation/clippy issues, not accepted results; final candidate fixes all. No native probe or live Memory access occurred.

## Recovery contract
Opus sqs0 rules this exact behavioral shape. The9-line production delta accepts only the exact v1 catalog identities of flow_nexus_flow_transitions and flow_nexus_hold. Both remain optional, absent families stay absent; this binary does not register, decode or write their records. It ignores stored Hold, as an old-behavior recovery reader. Unknown family names or changed schema hashes retain strict refusal. No existing Memory format changes.

Tests panel_families_are_preserved_unread_while_latest_memory_advances and panel_recovery_refuses_wrong_identities_without_changing_memory are green. They exercise configuration-only and running stores, deliberately opaque non-archive panel rows (proving no decoding), a new postmigration context write surviving another reopen, unchanged panel bytes and counts, and wrong-family/wrong-schema refusals leaving the entire store byte-identical.

Deploy0563 first. Once its live package/profile/configuration/harness preservation is verified, the059 rebuild can proceed. Later recovery from057/058/059 switches the daemon plus compatible client to0563 on the SAME latest Memory path; never replace Memory with a pre-switch copy. Panel records stay intact but unread until roll-forward. An arbitrary unrelated corruption is not repaired by this promise; retain the latest store and report refusal rather than rewinding it.

## Preservation and runtime acceptance
All source outside store.rs and release metadata is byte-identical to serving612; in particular once-only reminder checks, protected-address decisions, startup obligations, stop and reaping bodies are unchanged. No new harness reader, hook, transcript measure or context ingestion is added. No configuration is seeded or replayed by this patch.

Field must use actual-parent consumer pins, its full immutable consumer gate, whole retained Configuration comparison (including protected Fable/Energy), and service/process ownership preflight. Capture Fable native session/PID/start before and after; no hand-made service/config/runtime changes.

Source safety limitation: existing protection is threshold-only. Startup may act on preexisting explicit restart/successor/reap orders; unchanged code proves preservation, not actual absence of such production obligations. Field reports an exhaustive supported obligation oracle unverified. Question fu2g asks Opus whether existing semantics plus supported Inspect and service/process checks suffice for0563 or stronger behavior is required. This report does not waive that unresolved pre-activation boundary. Field may prepare/gate source now; wait for its safety ruling before activation.

## Next release remains unstarted
Opus sqs0/xbmv require0571/0581/0591 on live612-derived history, preserving accepted0v72 reminder delta, keeping gated059 transitions and withdrawing the cut. No next-release source work starts before0563 is gated and deployed. Transition Subscribe is held committed2083fa43, ungated.

## Safety ruling received
Opus Result fu2g accepts existing explicit-obligation semantics with no source change. Just before restart, Field reads Inspect and service/process state for { Psyche core Fable }. If any restart, successor or reap is recorded for Fable, or Inspect cannot show Fable entries at all, Field holds the restart and asks Opus; otherwise it restarts. Relayed directly to Field. This replaces only the pending-question boundary above.
