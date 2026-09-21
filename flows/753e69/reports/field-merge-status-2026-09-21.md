# Field branch merge status — 2026-09-21

The living authorized merging Field branches into repository mains. The integration is source work; no live network, Home, Ouranos, or service activation follows from a merge.

| Repository | Current integration result | Evidence and remaining gate |
| --- | --- | --- |
| Primary | Field census, passive checkup, and rollout report branch tips are ancestors of `main` at `e0000abac6d7`. | Field Medium 9ddcbc used ancestry merges while preserving the newer census/checkup tree. The only final tree delta is three owned reports. Census, cycle and shadow tests passed; remote head was read back. No timer/service activation. |
| Horizon | USB branch `37416e10c00c` is an ancestor of remote main `92d40e362393`; old-schema USB capability contract tests passed. | The merge retained current main's generated `ClusterDefinition` API and OpenCodeTesting, but did not carry forward the branch's authored `ClusterProposal`/`NodeService` API or Datomic proposal tests. It is not yet the accepted typed producer for Signal/Lojix. Corrective source integration and remote proof remain. |
| signal-lojix | Typed DTO graph precursor `83885263bfde` is published on a candidate bookmark, not main. | Generated Signal contract and USB binary/Datomic fixture pass a Prometheus-only check in a dirty producer worktree. Complete fallible authored-input conversion, old-schema refusal, coherent publication, and main merge remain. |
| meta-signal-lojix | No USB revision or main merge. | Waits for the accepted ordinary Signal wire revision and same-graph tests. |
| Lojix | Published historical proposals remain outside main; current USB candidate is unpublished. | Old Horizon APIs fail the current compilation path. It needs the ordinary and meta producers, typed pre-socket viewpoint materialization, coherent pins, and remote proof. |
| Goldragon | No USB data revision or main merge. | All-node proposal and materialization await Lojix's exact accepted pin; protected data lock 4044 remains. |
| CriomOS | Published source candidate `9842f51a86ce` remains outside main. | An isolated clean merge was formed, but the current remote-only focused check stopped before policy evaluation with `CriomOS: no system input was provided`. The repository uses a deliberate no-system stub; a real Lojix-materialized input is required. The unpushed merge was abandoned; main remains `d8c765db`. |
| CriomOS-home | Field Medium 9ddcbc retains consumer source lock 3776; no main merge or Home activation claimed. | Flow/Message pair, exact pins, remote build, migration, rollback and runtime ownership gates remain. |

The protected Flow, Message and signal-flow branches belong to f72ab7 and remain outside this Field merge lane. The current Field branches above are not interchangeable: their producer, consumer, and runtime gates are evaluated at each repository's actual main head. Further main merges will be recorded after verified candidate checks and remote readback.

The Horizon grade was corrected after a direct comparison of `37416e10c00c` with `92d40e362393`: the latter lacks `lib/src/proposal.rs` and the authored `ClusterProposal` public type while the current Signal candidate targets those types. Git ancestry and an old-schema capability test cannot establish the accepted mandatory-Datomic producer alignment. Signal remains pinned to the typed candidate until Horizon publishes a coherent replacement; no consumer pin is advanced on the basis of `92d40e362393`.
