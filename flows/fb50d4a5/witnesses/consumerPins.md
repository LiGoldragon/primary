# Consumer pins

Method: code read `/git/github.com/LiGoldragon/*/Cargo.toml`, `/git/github.com/LiGoldragon/*/Cargo.lock`, and `/git/github.com/LiGoldragon/lojix/Cargo.toml`; probe `rg -n --glob 'Cargo.toml' 'kameo\\s*=.*(branch|rev)|kameo\\s*=.*github.com/LiGoldragon/kameo' /git/github.com/LiGoldragon` and `rg -n --glob 'Cargo.lock' 'source = "git\\+https://github.com/LiGoldragon/kameo' /git/github.com/LiGoldragon`

Observed local dependency declarations:

- 20 repositories have a direct `LiGoldragon/kameo` URL in `Cargo.toml`.
- 15 direct manifests use `branch = "main"`.
- 4 direct manifests use `rev = "f491b45d7dcb55e5837eddde3d5d7ca8ceaa9f01"`: `ethos-engine`, `logos-engine`, `sema-storage`, and `triad-runtime`.
- `persona-spirit` uses `branch = "persona-lifecycle-terminal-outcome"`; the forge witness says that branch is currently absent. Its lockfile names commit `22514f7c6900da00703a4a0ef096f21a45c95a99`.
- `lojix/Cargo.toml` declares crates.io `kameo = "0.20"`, while its local `Cargo.lock` contains LiGoldragon fork source entries at `f491b45d...`. The manifest/lock discrepancy is an evidence boundary; it was not resolved by running Cargo.
- Many lockfiles for `branch = "main"` dependencies still resolve to `#f491b45d...`, not the docs-only fork head `3486e4f6`; this is a stale lock snapshot, though the fork head's only post-`f491b45d` change is the `AGENTS.md` metadata commit.

The 15 branch consumers and four revision consumers therefore have a coherent source-level fork ancestry at `f491b45d`, but branch-based manifests are not immutable authorities for future builds. The persona branch and lojix manifest/lock require separate build-resolution checks before relying on them.

## Sources

- Witness: `flows/fb50d4a5/witnesses/upstreamIdentity.md`
- `/git/github.com/LiGoldragon/persona-spirit/Cargo.toml`
- `/git/github.com/LiGoldragon/persona-spirit/Cargo.lock`
- `/git/github.com/LiGoldragon/lojix/Cargo.toml`
- `/git/github.com/LiGoldragon/lojix/Cargo.lock`
- Representative lockfiles: `/git/github.com/LiGoldragon/chroma/Cargo.lock`, `/git/github.com/LiGoldragon/triad-runtime/Cargo.lock`, `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock`
