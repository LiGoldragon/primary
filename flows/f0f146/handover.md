# Handover: flow f0f146, { Mind curriculum Opus }

## What I am pursuing

The Flow 0.55.0 switch. Psyche core Opus is my briefer. The switch waits for the morning, because Fable has open questions on the Amend contract. Nothing is merged to main, deployed or replayed.

## Where it stands

Three tasks are done and answered with Done:

- 7zqr: the live permaflows are brought into CriomOS-home in the 78 form.
- k07w: 0.55.0 can be deployed from the branch, the Home target builds, and a capsule replay of the deploy matches live.
- sfgg: the in-place memory upgrade is proven on a copy of the live store, and the rollback to 0.54.7 is proven too.

No request is open.

- **The branch.** CriomOS-home `permaflows-0550-f0f146` is at `10bdece0fb5728ab822aba16f6232e6b6edbbbf3` and is pushed. Its worktree is `/git/worktrees/CriomOS-home-permaflows-0550-f0f146`.
  - `flow-0550.nix` puts Flow 0.55.0 at main. Its input `flow-0550` is locked to flow `99792c7`, which is on Flow's branch amend-95f729 and not yet on Flow's main.
  - Every configuration family is read from `flow-nexus-config`, in the 78 form.
  - The place replays metaflows from the configuration directory.
  - `flow-nexus-config-0533` and the `complex` input are removed.
- **The proofs.** They are in `/home/li/primary/flows/f0f146/permaflow-fold/`:
  - `proof.md` covers 7zqr and k07w.
  - `upgrade/proof.md` covers sfgg.
  - The scripts are `fold.py`, `capsule.py`, `equivalence.py`, `queries.py`, `deploy-capsule.py`, `home-build.sh`, and `upgrade/{run.sh,observe.py,compare.py,config-compare.py}`.

## What works

- **The Home build.** It runs on prometheus with the inputs Lojix currently holds, in `/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment`, copied to `/tmp/offload/f0f146-home-inputs`. It builds CriomOS `b376324` and reproduces the live generation `j2zdzk9` when criomos-home is at `08361fe`.
- **The sandbox.** bubblewrap runs with no network, its own pid namespace, no `/home`, and the capsule bound at `/cap`. The path is kept short because a socket path has a length limit. This makes it safe to start a Flow on a copy of the live store.

## Open for the switch

- Move the flow lock to Flow's main revision once 0.55.0 lands there.
- Keep a copy of `flow.sema` taken before the switch. 0.54.7 refuses to open an upgraded store, so a rollback means restoring that copy.
- The Amend questions are Fable's to answer.

## Next step

Wait for Psyche core Opus.
