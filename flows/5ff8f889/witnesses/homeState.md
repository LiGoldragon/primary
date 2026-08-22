# Home repository and worktree state

Method: probe `jj status -R /git/github.com/LiGoldragon/CriomOS-home`; `jj log -R /git/github.com/LiGoldragon/CriomOS-home -r main -n 3 --no-graph`; `jj log -R /git/github.com/LiGoldragon/CriomOS-home -r @ -n 3 --no-graph`; `jq` reads of `flake.lock`.

`/home/li/primary/CriomOS-home` does not exist. The configured repository root
from `SKILL_VARIABLES.md` is `/git/github.com/LiGoldragon/CriomOS-home`, which
is the repository inspected here.

The Home repository worktree has no changes. Its `main` bookmark is
`1a6e22da155bb75a6362d10623301b13d0c24b34` (`flake: update generated primary
source`). The working copy is an empty detached child `fedf1da9` whose parent
is `9d2896c7` (`Recover contradictory managed Codium extension state`).

The Home lock pins Chroma revision
`eea85f4aae5a21813314a128faa5dce1e22eff48`. The OS repository
`/git/github.com/LiGoldragon/CriomOS` is also clean; its `main` is
`d04f6daf` (`flake: update CriomOS-home input`) and pins Home at the same
`1a6e22da...` revision. The local Chroma repository is not clean: its working
copy has an added `.beads/issues.jsonl` from existing bead initialization; its
product `main` is `eea85f4a`. The local `CriomOS-emacs` repository is clean,
but remains an empty-child checkout over scaffold `main` `50e9ee3b`.

Method: probe `gh repo view LiGoldragon/chroma-emacs --json ...` and
`gh api repos/LiGoldragon/chroma-emacs/branches`.

Both public-repository queries returned 404. No local `chroma-emacs` checkout
exists. The accepted repository therefore has no source, lockable revision, or
observable package output at this time.

## Sources

- `/home/li/primary/SKILL_VARIABLES.md`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS-emacs/README.md`
- Flow `5ff8f889`
