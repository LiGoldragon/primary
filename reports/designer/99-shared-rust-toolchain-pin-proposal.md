# 99 — Sync Rust toolchains across the workspace — one script

*Designer note. The earlier draft of this report proposed a
new `rust-pin` repo with role cascades and a BEADS chain.
That was over-engineered: the fix is one script using existing
nix machinery (`nix flake lock --inputs-from`, already
documented in `~/primary/skills/nix-discipline.md` §"Lock-side
pinning"). This is the corrected proposal.*

---

## Problem

Every Rust flake in the workspace declares its own
`inputs.fenix` and pins the rev in its own `flake.lock`. Across
~30 Rust repos those locks drift across update windows. Same
Rust version through fenix's overlay → different rustc
derivations → different `/nix/store/<hash>-rust-…` paths → one
~200 MB redownload per divergent rev.

## Solution

Pick one Rust repo as the canonical fenix-lock source (e.g.
`signal-core`). Every other Rust repo copies fenix's lock from
that one with `nix flake lock --inputs-from path:<canonical>`.
A small shell script walks every Rust repo and runs the copy.

## The script

`~/primary/tools/sync-rust-fenix`:

```sh
#!/usr/bin/env bash
# Sync every Rust repo's fenix lock to signal-core's.
# Run after: cd signal-core && nix flake update fenix && jj git push.
set -euo pipefail

CANONICAL=/git/github.com/LiGoldragon/signal-core

for flake in /git/github.com/LiGoldragon/*/flake.nix; do
    repo="$(dirname "$flake")"
    [ "$repo" = "$CANONICAL" ] && continue
    grep -q '"github:nix-community/fenix"' "$flake" || continue
    printf '%s\n' "$(basename "$repo")"
    (cd "$repo" \
       && nix flake lock --inputs-from "path:$CANONICAL" \
       && jj commit -m 'sync fenix lock' \
       && jj bookmark set main -r @- \
       && jj git push --bookmark main)
done
```

`--inputs-from` is the key — it resolves any matching inputs
(only `fenix` here, since other inputs differ legitimately
across repos) using the canonical flake's locked entries. No
hash typing by hand; no new repo; no design ceremony.

## Workspace-wide rust bump

```sh
cd /git/github.com/LiGoldragon/signal-core
nix flake update fenix
jj commit -m 'bump fenix' && jj bookmark set main -r @- && jj git push --bookmark main
~/primary/tools/sync-rust-fenix
```

After this, every Rust repo references the same fenix rev →
one rustc store path → one download per machine.

## Owner

System-specialist authors `~/primary/tools/sync-rust-fenix`.
That's the whole change.

## See also

- `~/primary/skills/nix-discipline.md` §"Lock-side pinning" —
  the `--inputs-from` mechanism this script uses.
- `~/primary/repos/lore/rust/nix-packaging.md` §"Canonical
  flake.nix" — the per-repo template; unchanged by this
  proposal.
