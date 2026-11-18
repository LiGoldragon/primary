# History-only recovery ancestry candidate

Core q1ul admits this candidate path, not a branch exception. Before creation, fresh remote main was exact feature **1d3f633a89b3bab8d5ff844db8c07a05c795c5f0**. No main move was performed here.

Published candidate: **0f822a458becf99d2dc5d5880b9aae80c6017e08**, origin branch **recovery-history-a7785f**, exact push/readback.

- First parent: **1d3f633a89b3bab8d5ff844db8c07a05c795c5f0**.
- Second parent: **19378d08e1c25b780e0d671bb45a3819a7fbccb7**.
- Tree: **e1ecb1789dd1459f2efa221f4d98271a2a930d88**, exactly feature1d3f633a's tree; `git diff --exit-code` passed.
- `merge-base --is-ancestor recovery candidate` passed. Recovery becomes main-reachable only after separately admitted eventual candidate FF.
- Created as an explicit commit-tree merge with both exact parents, not a worktree content merge. Commit message states recovery safety is already represented by reviewed feature safety, and no recovery tree replacement occurs.
- Base **e3efe3f040bd776b3d89fc28da7fa5dcf0f63c49**, ordinary **a536862f00704f0ea2a805484d2a61f9e5dd382a**, meta **be69365bc51bf4a6300aa963b60f8b88fbf90359** remain exact; all source, metadata, generated types, versions and tests are unchanged.

## Recovery safety compared before creation

Recovery diff against common parentc0d51dc was read across all14 changed files. `src/send_tool.rs`, `src/test_faults.rs` and `tests/unit/waking.rs` are byte-identical between recovery and feature: interrupted responder exclusion/refusal and held-recovery fixtures are retained. `src/main.rs` retains the same pre-serving reconcile call (comment differs). `src/store/overriding.rs` retains the recovery fault-injection seam, adds the feature hold families. Global Resume in `src/lib.rs:2066–2092` retains record-every-seat before switching and reconcile before recover_wakes. Feature `src/launching.rs:954–974,1289–1305` retains the outer global-Hold check and a second dispatch-protected global/per-address Hold check in scoped cleanup.

The store relationship is deliberately different: recovery recognizes the exact two newer catalog identities and preserves payloads opaquely; feature declares/owns and decodes those same families. Its identifiers in `src/store/overriding.rs` match recovery constants exactly, and `src/store.rs:5602–5608,5964–5965` recognizes them. Opaque invalid-archive recovery tests are not copied into the owning feature, where invalid archives are rightly not valid feature data. Recovery prerelease manifests likewise are not feature manifests. These are expected version-role differences, not a reason to replace the feature tree with recovery content. Prior51sq/3lfq audited the feature safety; this ancestry candidate introduces no new behavior.

## New-revision evidence and remaining boundary

Requested independent audit from existing Mind harnessNexus Opus: exact parents/tree/pins/recovery reachability and any recovery-safety disconfirmation. Initial malformed Send was refused locally by parser; corrected Task was sent separately. No audit result yet.

New published-source whole immutable Prometheus gate started against **0f822a45**, scratch `/tmp/flow-history-a7785f.bleCmg/published-gate-0f822a45.log`; foreground process completed **EXIT0**. The migration witness at log line70 stamps `current=0f822a458becf99d2dc5d5880b9aae80c6017e08`, predecessorf7d2336, actual-process old-write/current-serve/current-reopen/malformed-rollback. Unchanged crate builds were reused; the revision-stamped process check ran anew. Earlier1d3f633a gate is not claimed as this SHA's witness, because process checks stamp sourceRevision.

After audit and green gate, request Core's exact main FF admission, then confirm published main. No force, source reconciliation, repin, live action or sv0s Done authorized by this report.
