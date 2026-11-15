# Fixed decoder and manual-replay candidate packet

Candidate preparation and Evaluate are complete; main publication and activation remain held.
Authority: inherited Core xwvs/Psyche imuq, reaffirmed Core u6aa. No Energy, Listener or ke1s union.

## Immutable candidate

- Home: `308f2354d21eb79e111d4e0cfd83c58ebe327a21`.
- CriomOS: `62b83fe6c64b242da31a7751468a002d8a4da59e`.
- Both origin candidate branches: `flow/d42f0a-decoder`; pushed and independently read with ls-remote.
- Origin mains remained Home `2af9265d37a10e20289db6826bfcef86c861bf74`, CriomOS `4305f5cad95ab55a516cf430014a5f7dd7b2575e`.
- Both isolated worktrees are clean. Consumer changes from f775c3d are only Home locked rev, narHash and lastModified.

The Home candidate retains the accepted fixed decoder589 cohort and adds exactly the two cumulative replay-removal source files from `adeb3e53749bc0b211761c35b52525196f7e859a`: `modules/home/profiles/min/flow-nexus-place.nix` and `checks/flow-manual-replay/default.nix`. Both candidate blobs equal adeb blobs exactly. Source owner confirmed the full delta from Home main2af is these two files only; later fixture fixes are included.

Selected retained cohort revisions:
- Curriculum: `0f848baaeb33289b144a7481270d887dbf918755`.
- Flow: `52e5687d13446e3cd22583ff31d717f6250e0534`.
- Serving cohort build-base: `4ea69d1fc87c95e7c1f54d02b21166ffb3285edd`.
- Psyche source: `72108fe2e4401d7a175f288e6c97c238b31f4218`.
- Mind source: `4b350ce8c7ef7bc281871b419e75542afc3e687f`.
- Field source: `4589b80bfa1643bc7320cd8111676ca9279c6d5a`.
Unrelated nested cohort pins are preserved, not claimed to be these serving revisions. Source main publication remains held; restoration candidate branches were published by their owner as recorded in `flows/25858e/stopped-swap-preparation.md`.

## Gates and published-source proof

Full immutable Home Prometheus gate: exit 0, 98 successful attributes, including the manual replay check. Exact command uses nix-fast-build, the committed git+file revision, and the inherited projected system input; no copied-tree gate.
Evidence: `/tmp/flow-d42f0a-cohort/union-home-gate-full.log`, `union-home-gate.exit`.
Published GitHub Home prefetch hash equals the gated local immutable source hash. Evidence: `union-home-prefetch.json` and `union-home-remote-prefetch.json` in the same evidence directory.

Lojix Evaluate only, exact pushed consumer revision above:
- Ouranos deployment **629**: Completed, Some.Succeeded; terminal marker 15201.
- Zeus deployment **630**: Completed, Some.Succeeded; terminal marker 15195.
Both use RequireImmutable, inherited proposal/transports/backend/output selector. Fresh SSH hostname checks matched each logical node. Proposal checked as an existing absolute regular non-symlink file. Requests changed only immutable CriomOS revision from the inherited templates.
Evidence in `/tmp/flow-d42f0a-cohort/`: `{ouranos,zeus}-union-request.datom`, `-union-admission.datom`, `-union-query-latest.datom`.
No realization, activation, runtime mutation or native witness was performed. Evaluate success is not activation evidence.

## Single-writer custody

Field read-only receipt: `flows/374411/lock321-lifecycle-t84m/report.md`, SHA256 `f2fd615c425dfa19340957034f2d12b5722c38a8b01030c07272028090acfc60`. Current/Inspect identified Awake5441e0, predecessor had no pane, both exact worktrees clean, no git lock and no named old subprocess in bounded checks. This alone did not establish historical native termination.
Core added lifecycle-only native receipt: predecessor session `01a1e0e6-d652-73f2-a587-5b4d42f0ab2c`, 1030 lines, final task_complete at 20:58:36.157Z, all starts paired complete/aborted and no open native turn. Core mwxx explicitly accepted this bounded evidence; it does not exclude every imaginable orphan.
After fresh `Current.{ Mind flowNexus Sol }` returned `Current.Awake.5441e0` and fresh lock inventory matched, ONLY321 was released. Identical paths/name/reason were reacquired as **330**, owner5441e0. No other lock was changed. Report path reservation is331.

## Remaining release boundary

Core/Psyche review this single packet before any further action. Main publication, typed-source main publication and activation remain held. Any later stopped swap carries current Memory AS IS at actual stop, never an earlier backup; Field owns runtime operations. Energy, Listener and heartbeat are separate lanes.

The beads read-only prerequisite failed in both repositories because the shared remote-backed schema lacks the leases table. No migration was attempted; this does not affect the immutable Nix gate or Lojix Evaluate receipts above.
