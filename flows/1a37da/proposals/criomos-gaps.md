Gaps for knowledge:criomos, from Field core Primary's read-only reader (CriomOS adc2e8d5, dirty checkout):
- criome implementation not established.
- Lojix deploy/eval/state/rollback Rust path not freshly verified; public Deploy/Query claims rest on knowledge:lojix and history.
- Lojix reset is not proof of rollback.
- flake 147-149 host artifacts are comments, not implementation proof.
Verified pointers: flake 94-105 (lojix input), 118-137 (Horizon/deployment input); modules/nixos/criomos.nix 7-30; modules/nixos/lojix.nix 48-267.
The draft's lojix/src/bootstrap.rs:478-503 citation (NixosSystemdBootV1 steps) is the Sonnet author's own and goes beyond this reader.

## Inspected revisions
Repositories under /git/github.com/LiGoldragon/. Dirty = `git status --short | wc -l`. CriomOS citations were read from HEAD (`git show HEAD:<path>`), not the dirty working tree; the others were read from the working tree.

| Repository | HEAD | Dirty |
|---|---|---|
| CriomOS | adc2e8d5f572a833baa492c3c3e9615cb1bf1019 | 20 |
| criome | 6582e5ff3724acd43db3673c3bdff5345e7f1eea | 1 (Cargo.lock) |
| lojix | 5d75a4032079cd942a3d4f5ba676da9ade5e8249 | 0 |
| horizon-rs | b45d6ad48b5ee5d28eb0127f17c6e0084b696e60 | 0 |
| signal-lojix | f7866bf013499503d21491bcdaadaf88ea6c810c | 0 |
| meta-signal-lojix | b500561f0ce813917366997581412b7a79aebc99 | 0 |

Citation recheck: every file:line in criomos.md pointed at the claimed code at these revisions; none drifted. Added `adapters.rs:247`, a second `Rollback` slot declaration, to the rollback citation.
