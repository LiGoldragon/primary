# Flow worktrees: 75 to one

**Done:** The cleaned `/git/github.com/LiGoldragon/flow/.git` repository now registers only its canonical checkout. Source from the dirty copies is reachable on 12 pushed archive branches; two formerly unreachable clean HEADs have pushed archive tags. All 74 original linked HEADs remain reachable. **Production code removed 0 / added 0.** Other clones and their active work remain preserved.

**Exact scope:** 75→1 is registration reduction in the common Git repository `/git/github.com/LiGoldragon/flow/.git`. A separate common repository `/home/li/primary/flow/.git` survives with the active `/home/li/worktrees/flow-heartbeat-24eb5b` checkout. Its paired `/home/li/worktrees/meta-heartbeat-24eb5b` belongs to `/git/github.com/LiGoldragon/meta-signal-flow/.git`. Both active paths and lock24937 were preserved. This is **not** proof of one Flow working copy across all clones; no further cleanup is requested. Direct path/admin witnesses are in `heartbeat-preservation.md`.

## Witness

```text
worktree /git/github.com/LiGoldragon/flow
HEAD 60434783b3ed292e3f0b8f4efe3a3c5561a76b96
branch refs/heads/main
```

- Removed 61 clean and 12 dirty linked directories with normal `git worktree remove`, without force. Pruned one already-missing registration after checking its retained branch/HEAD. Canonical dirty main stays.
- Eight dirty copies contained source changes; four contained only reproducible `/nix/store` result links. The source-bearing archive tips preserve the tracked changes and the reviewed untracked Rust source. All original commits remain ancestors/reachable.
- Every archived source blob was verified against the corresponding current file before removal; all 74 old HEADs were checked again afterward. Independent validation also checked recorded archive blobs, local branch/tag OIDs and the single-checkout registry.
- Verification caught one index-added Rust file missing from the first temporary-index archive. Before removal or push, a descendant commit included it and retained the incomplete commit as history. Final archive verification passed. There are nine new archival commits, not nine source fixes.
- Ignored entries in linked copies were checked once: Cargo target metadata/build directories and empty target/tmp, with no non-build root entry found. Four result links were recorded before unlinking; store targets were untouched. No nested repository was found in the source-tree scan, no gitlinks existed, and reviewed changed source had no strong credential-marker match. No credential material was printed or committed.

## Pushed and independently read back

| Ref | Remote object ID |
|---|---|
| `refs/heads/worktree/flow-0.40-74e4d1` | `a8730b7e5c5cc0cb5ee7a132c315cab375712dce` |
| `refs/heads/worktree/flow-2256c2-batch4` | `8ee3030e8c7822311873ae41c7a411c298ab3c6b` |
| `refs/heads/worktree/flow-2c06c7-batch3` | `e904c86c36db95bd1d91506e448b73f87fc2efe4` |
| `refs/heads/worktree/flow-36ac89-unrestrict` | `f70a54be593c880d32e6c973852490f927ee2751` |
| `refs/heads/worktree/flow-b11-capsule-2c06c7` | `28ea9d43fd46bf00e4e54dd0c237167b344221d0` |
| `refs/heads/worktree/flow-b2-deploy-2c06c7` | `e43ff349514c8f2918768ea13672ae92d54c5a27` |
| `refs/heads/worktree/flow-batch10-2c06c7` | `7bd2e4417123474480c57c0d0caef2ac86bd09db` |
| `refs/heads/worktree/flow-batch7-2c06c7` | `0abe10e7f7cb48bfb4053eb2ea3e90c78193613a` |
| `refs/heads/worktree/flow-queue-emergency-2c06c7` | `7fc67285f41e30e338c6f6eda8e8ca4a3d08c456` |
| `refs/heads/worktree/flow-refresh-c27520` | `b59f989dc60b0f78a3655cb2b4f585a040cb211c` |
| `refs/heads/worktree/flow-store-migration` | `c520059011380d822d7e3b948da1bbd9b482fc04` |
| `refs/heads/worktree/wt-flow` | `4adb9f5472f5a56f88f2bf3e3a5640759850ab88` |
| `refs/tags/archive/worktree-flow-d0-repair-4db1d3` | `26faebdc3032f39ab62c012e05e15535f9d14dbd` |
| `refs/tags/archive/worktree-flow-tools-9ed-exact` | `9ed7b8ae5a17655a0bb90fcab1e2c0d99306a548` |

## Reservations and canonical preservation

The fresh snapshot had 13 worktree entries overlapping Orchestrate reservations: 12 linked entries plus canonical. The latest direct Psyche Primary order authorized takeover. The 12 linked reservations were released with typed receipts and all 74 linked paths acquired under lock24940, then released after cleanup. Canonical source reservations were preserved, not retired. Common refs/administration and this report used lock24939; final release is reported separately. Inventory report lock24938 was released.

Canonical HEAD remained `60434783b3ed292e3f0b8f4efe3a3c5561a76b96`. Its physical index SHA256 was identical before and immediately after archival/removal: `9b63722a77426b1d2cef29ab5340e6a1b81f8f47a1ad30037960ab97bf7b3549`. A later independent check saw a different physical index digest. No reset/restoration was attempted: a fresh optional-locks-disabled comparison still exactly matches the original 45 status/path entries (44 unstaged modifications and intent-to-add result), with no cached source delta. Physical-byte preservation is claimed only at the recorded execution boundary, not indefinitely while other readers/writers run. The validator subsequently confirmed running `git write-tree`, which can update cache-tree metadata; its returned Git tree OID was initially compared incorrectly with the physical SHA256. That comparison was withdrawn. No staged source delta or status/path loss was found; the execution-boundary physical digest witness remains valid.

## The source of the habit

Historical explicit `git worktree add` calls are witnessed creators; the instruction/context motivating them remains unknown. Current roles already say shared workspace/no worktree, and `.claude/settings.json` already has `worktree.bgIsolation=none`. No active causal line was found to delete; those protective settings were retained. Primary accepted this no-patch source finding, and the latest Psyche ruling accepts the witness when no such line remains. No hypothetical source edit or fresh synthetic write task was invented.

No later authorized canonical write-task launch has yet been observed; that future launch/isolation check is not claimed complete. No build, test execution, Home change, process termination or Flow cutover action was performed by this cleanup.

Full per-path initial state: `flow-worktree-inventory.json`. Typed releases, archived file hashes, original/final refs, push/read-back and removal receipts: `flow-worktree-execution.json`.
