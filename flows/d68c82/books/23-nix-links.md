<!-- to-the-living:start -->
Presentation.{ «A folder too full to index» }

# A folder too full to index

```
 every build Nix imports
     |
     v
 +------------------------+
 | Nix compares each file |
 | and hardlinks the      |
 | duplicates             |
 +------------------------+
     |  one entry per file
     v
 +------------------------+
 | /nix/store/.links      |
 | one folder, 730 MB of  |
 | entries                |
 +------------------------+
     |  index at its
     |  two-level limit
     v
 +------------------------+
 | "no space left" on     |
 | every new link         |
 | (93 GB are free)       |
 +------------------------+
```

## What was measured on Ouranos

| | value |
|---|---|
| a Flow import | 5,467 failed links; the import still succeeded |
| kernel, in one minute | 43,346 index-full events |
| a quiet minute with no events | processes waiting on IO 79% of the time |
| that same quiet minute | NVMe busy 2%, 5,935 pages read back from disk |

The full folder is real, and it is only part of the stutter. In the quiet minute the disk was almost idle while processes still waited. The likeliest cause of those waits, not yet proven, is memory being paged back in.

Only Ouranos is measured; the other hosts are not assumed to match.

## Proposal 1: stop linking duplicates on Ouranos

File: CriomOS modules/nixos/nix/retention-agent.nix

```nix
- nix.settings.auto-optimise-store = true;
+ nix.settings.auto-optimise-store =
+   node.storeOptimisation;
```

Each node's value comes from the cluster data: false for Ouranos, true for the others. Links already made stay. Duplicates in new builds take more disk, by an amount not estimated. It is undone by setting the value back.

Ruling: land, amend, or reject.

## Proposal 2: let the folder grow past the limit

The disk's large-directory feature is switched on once, offline, from a recovery system. New disks are formatted with it. It cannot be switched off again: a system rollback does not undo it, and going back means restoring from a backup. Every kernel and recovery tool that boots the laptop must support it.

Ruling: land, amend, or reject.

## Question

Proposal 1 is small and reversible; Proposal 2 removes the limit for good at a permanent format cost. Either, both, or neither?
<!-- to-the-living:end -->
