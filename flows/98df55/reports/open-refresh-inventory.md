# Open refreshes without a stored caller: ouranos Flow Nexus

Result: **0 open refreshes were found at 2026-11-14T20:44:14.856–20:44:14.922Z.** The Memory families that hold open refreshes were both empty. This is a point-in-time observation, not a standing guarantee.

## Daemon

- Unit: `flow-nexus-0550.service` (user), active since 2026-11-14 05:43:49 CST, main PID 654687. The unit's Description still says "Flow Nexus 0.55.0", but its ExecStart runs 0.56.2.
- Binary: `/nix/store/nwwm7mri2zv87klslckq94gjpjx2nh1l-flow-configured-0.56.2/bin/flow-nexus-daemon "{ «main» «/run/user/1001/nexus/main» «/home/li/.local/state/nexus/main» }"`
- Version: 0.56.2. The configured package's daemon is built by `rust_flow-nexus-0.56.2-bin.drv` (mib7h4ng…), whose `src` is `/nix/store/ig9191apcbidhwjyhvimczhxyccr5i3h-flow-nexus-0.56.2`. Running `diff -r` between that source and `crates/flow-nexus` at origin/main `eabddc8d29ddd30b4665065cec4bee57ea7410ce` ("Flow 0.56.2: …") finds no difference except `tests/`, which the build leaves out. The workspace version at eabddc8d is 0.56.2. The daemon links the library `rust_flow-nexus-0.56.2.drv` (s1kcn677…, features `datom default`) and `rust_sema-engine-0.19.0.drv` (i31cfg23…). It uses redb 4.3.0.
- State directory: `/home/li/.local/state/nexus/main`. Store: `flow.sema` (77,713,408 bytes, inode 52455239). The directory also holds `energy.rkyv`, `energy-translator.rkyv`, and `flow.sema.leaking-1111`, which is stale and was last modified on Nov 11; none of these were read.

## Where 0.56.2 records a Refresh in Memory

- **Queued, pending at the next rest:** table `flow_nexus_ordered_replacements`, family `flow-nexus-ordered-replacement`, schema `flow-nexus-ordered-replacement-v1`. The record is `OrderedReplacement.{ Address Predecessor ReplacementOrder }` and is keyed by the Address. A queued Refresh is `ReplacementOrder::Refresh`. `waking.rs` `queue_refresh` writes it and answers RefreshQueued; `forget_ordered_replacement` retracts it when the order is carried out or spent.
- **Succession not completed:** table `flow_nexus_successor_intents`, family `flow-nexus-successor-intent`, schema `flow-nexus-successor-intent-v3`. The record is `SuccessorIntent.{ Address Predecessor SuccessionCause LaunchRequestId }`, keyed by the Address. An ordered Refresh's succession is `SuccessionCause::Ordered`; a threshold refresh is `Refresh`. The intent is retracted in the write in which the successor takes the Address (`successor_given`).
- Neither record has a field for a caller, a time, or a RequestId, so at 0.56.2 every open refresh would lack a stored caller. The RefreshQueued answer carries no RequestId either. The other refresh state, the waking lease, the dispatch gate and `RefreshRefusals`, lives only in process memory.

## Snapshot method

- Engine guarantees, read from source: redb 4.3.0 commits default to `Durability::Immediate`, meaning fsync on every commit. Pages are written copy-on-write with `pwrite`, so mtime and ctime change on each write. The file header has two checksummed commit slots, and an open that finds the recovery flag set picks the newest valid slot. sema-engine `commit_atomic` puts each atomic commit in one redb write transaction (`Sema::write` → `begin_write` … `commit`).
- No engine-supported snapshot was available from outside the daemon. The daemon holds the redb file, sema-engine's snapshot identifiers and checkpoints are in-process, and no 0.56.2 socket request exports Memory.
- The copy, taken by `/tmp/claude-1001/-home-li-primary/98df550b-580c-5645-ac3b-d5ccbe75016d/scratchpad/snap.sh`: stat the store (inode, size, mtime, ctime), `cp` it to copy A, stat, `cp` to copy B, stat, then compute SHA-256 of both. A copy is accepted only if the stat before A equals the stat after B and the two hashes are equal. The first attempt was accepted:
  - Window: 2026-11-14T20:44:14.855964022Z to 20:44:14.921654541Z.
  - Stat before, between, and after the copies: `52455239 77713408 1794689049.347529836 1794689049.347529836`. The store's last write was at 20:44:09.348Z, about 5.5 s before the copies.
  - SHA-256 of A and of B: `d157a05763f1214c6a1c5694916d75298ff9988d342bb1c9d87886365ca06626`.
- Consistency judgment: **consistent with high confidence, not proven.** The file was not written during the copy window, so both copies are the file as it stood after its last write. Within the engine's guarantees, that file state decodes to a committed state: either the last commit, or, if a commit had paused for more than 5.5 s between its page writes and its header write, the slot repair falls back to the previous valid commit. Limits: this rests on mtime tracking `pwrite`, which holds on Linux for this backend. It is not a transaction taken inside the daemon. Anything queued after 20:44:14.922Z is not covered.
- The copies were deleted afterwards. Opening copy A with the engine wrote to that copy (redb slot repair plus sema's schema transaction), so A's hash changed to `cad17c7f…`. Copy B was only checked, and its hash was unchanged afterwards.

## Decoding (Flow's own code at that version)

1. The deployed `flow-store-check` was run on copy B: `Opens.…/b.sema`, exit code 0. This is Flow 0.56.2's own configured open, run on a private copy that the tool makes itself.
2. A reader was built as an extra binary of the eabddc8d `flow-nexus` crate, using build-base's `overrideBinaries`. It links the same library derivation as the daemon (s1kcn677…) and the same sema-engine (i31cfg23…). Source and build expression: `/tmp/claude-1001/-home-li-primary/98df550b-580c-5645-ac3b-d5ccbe75016d/scratchpad/reader/open-refresh-read.rs` and `/tmp/claude-1001/-home-li-primary/98df550b-580c-5645-ac3b-d5ccbe75016d/scratchpad/reader/default.nix`; output: `/tmp/claude-1001/-home-li-primary/98df550b-580c-5645-ac3b-d5ccbe75016d/scratchpad/read.out`. The reader opens copy A with `sema_engine::Engine::open(SchemaVersion 3)`. It registers the two tables with Flow's generated `OrderedReplacement` and `SuccessorIntent` types and their own `MemoryDefinition::schema_hash()`, plus `StoredMetaflow`, and calls `match_records(QueryPlan::all)`.
3. What it read:
   - All three families are present in the catalog, so an empty result is a true zero and not a missing family.
   - `flow_nexus_ordered_replacements`: 0 records.
   - `flow_nexus_successor_intents`: 0 records.
   - `flow_nexus_metaflows`: 30 records; none were referenced by an open order.
   - Commit log: 101,186 entries, complete from sequence 1 to the latest, 101186. Over that history the ordered-replacements table has 76 Assert, 1 Mutate and 76 Retract operations, and the successor-intents table has 57 Assert and 57 Retract. Folding the log per key leaves no key whose last operation is not a Retract. The last operations were successor intent `Psyche:4:core:Fable`, asserted at 99426 and retracted at 99446, and ordered replacements `Mind:9:flowNexus:Sol` and `Mind:9:flowNexus:Opus`, retracted at 95656 and 95658.

## Cross-check with the daemon's journal

Every `flow X works; its refresh waits for its rest` logged since the daemon started has a later completion line. The flows are 17e257, 299aa3, 54269e, 7cd167, 1203fb, 6be617, 521d44, 1dd428, 2987ba, bdb323 and 90d453. Each completion line is either `refreshed; … sleeps` or `refreshed at its rest; its successor … runs; its reap is Owed`. Predecessor reaps left pending (`PendingReap`) were not read. They follow a succession that has already completed, and they are not refresh requests.

## Open refreshes lacking a caller

None observed at 2026-11-14T20:44:14.9Z (store SHA-256 d157a057…, latest commit 101186).
