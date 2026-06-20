# Cloud Node Operator-Side Landing

## Scope

The psyche asked me to take the operator side of cloud-designer's handoff from `reports/cloud-designer/78-criomos-website-hosting.md`. The handoff bead is `primary-n98t` — landing the pushed cloud-node feature branches for `goldragon` and `horizon-rs` so the WebHost/doris work can proceed.

## Intent gap-check

The claimed Spirit records exist:

- `878r` — CriomOS website-hosting node service; doris is the first concrete role.
- `5pf6` — cloud-hosted compute nodes have low cluster trust; doris uses Min trust.
- `zeqq` — cloud nodes are provisioned only once they have a concrete role.
- `q4gd` — horizon derives facets from typed source enums; no parallel one-hot bool struct.

## horizon-rs

Integrated `cloud-designer-cloud-node-species` into `main`.

The branch was not a fast-forward of current `main`: it diverged before `qspmvwno` (`horizon: correct misleading serde-default/tail-append comments`). Since the pushed designer commits are immutable, I did not rewrite them. I created an operator merge commit instead:

- `bd1cc2c1` — `horizon: merge cloud node species branch`

Validation on the merged tree:

- `cargo test --locked` — passed.
- `cargo clippy --locked --all-targets -- -D warnings` — passed.

`jj git push --bookmark main` reports `main@origin` already matches local `main` after the push.

## goldragon

The `goldragon` branch `cloud-designer-cloud-node-data` exists and is pushed, but I did not merge it because `/git/github.com/LiGoldragon/goldragon` is held by the active `system-designer` lock for VmHost/TestVm work. The lock also names `goldragon`, so merging doris data there would violate coordination unless the psyche explicitly authorizes an override or the lock clears.

I added a note to `primary-n98t` recording this partial landing: `horizon-rs` done, `goldragon` blocked by lock.
