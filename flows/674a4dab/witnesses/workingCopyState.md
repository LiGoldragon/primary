# Working-copy state of the CriomOS stack checkouts

Method: probe `for r in ...; do git -C /git/github.com/LiGoldragon/$r rev-parse --abbrev-ref HEAD; git rev-parse --short HEAD main origin/main; git rev-list --left-right --count HEAD...origin/main; git status --porcelain; done` (2026-08-28, flow 674a4dab)

| Repository | HEAD | origin/main | behind | dirty |
|---|---|---|---|---|
| CriomOS | detached 21af0c3 (2026-08-26) | 45e83fb | 11 commits, 10 files (+127/−354) | 0 |
| CriomOS-home | detached 4e36d44 (2026-08-27) | ed6832c | 9 commits, 64 files (+3239/−975) | 0 |
| goldragon | main be4bf4d (2026-08-13) | 5bc563b | 1 commit, 2 files | 0 |
| lojix | main 782805b (2026-08-23) | 33b8b6b | 1 commit, 5 files | 13 untracked `.beads/` (dolt) files |
| horizon-rs | main 6f8e680 (2026-08-13) | c70915e | 1 commit, 12 files (+64/−238) | 0 |
| criomos-horizon-config | e222d3a | e222d3a | 0 | 0 |
| CriomOS-lib | 6e3bcb0 | 6e3bcb0 | 0 | 0 |
| CriomOS-pkgs | c64ea0e | c64ea0e | 0 | 0 |

Method: probe `git show origin/main:flake.nix | grep -i horizon-config` in CriomOS; `git grep -i 'horizon-config\|horizon.dotos' origin/main` in horizon-rs — CriomOS's flake at origin/main does not reference criomos-horizon-config; horizon-rs at origin/main mentions it only in AGENTS.md/ARCHITECTURE.md/skills.md, not in Rust source.

Method: probe `ls /git/github.com/LiGoldragon | grep -i core` — no `criomos-core` repository exists.
