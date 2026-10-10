# Repository relationship

Method: probe `jj -R /git/github.com/LiGoldragon/kameo status; jj ... git remote list; jj ... bookmark list --all-remotes; jj ... log -r '::main & ~::main@upstream'; jj ... log -r '::main@upstream & ~::main'; jj ... log -r '::main & ::main@upstream' -n 1`

Observed on 2026-08-22:

- Checkout: `/git/github.com/LiGoldragon/kameo`.
- Working copy clean; working-copy commit is an empty child of fork `main`.
- `origin` is `git@github.com:LiGoldragon/kameo.git`; `upstream` is `git@github.com:tqwewe/kameo.git`.
- Local `main`/`main@origin`/`main@git`: `3486e4f63ea4e87123476cfbdefeb12403540306`, subject `docs: mark Protos estate status`.
- Local `main@upstream`: `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`, subject `chore(deps): update syn requirement from 2.0.52 to 3.0.2 (#383)`.
- Latest common ancestor: `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`, subject `chore: use libp2p::identity instead of libp2p_identity directly (#339)`.
- Fork-only ancestry has six commits: `1325f6ae`, `da0f64af`, `1980e34b`, `8ea1e3fa`, `f491b45d`, `3486e4f6`.
- Local upstream-only ancestry count is 49 commits.
- The local checkout has no uncommitted changes. No fetch or ref update was run.

The local refs therefore already represent the current forge heads witnessed separately, but the checkout's code/refs must still be treated as a snapshot rather than a permanent freshness guarantee.

## Sources

- Witness: `flows/fb50d4a5/witnesses/upstreamIdentity.md`
- Witness: `flows/fb50d4a5/witnesses/forkApiArchitecture.md`
