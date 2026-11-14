# Disk reclaim on ouranos (by Psyche core Sonnet c3c1a0)

Root was 865G used, 4.6G free. After steps 1 to 3: 648G used, 222G free (about 217G freed). All listings are in `/home/li/primary/flows/678f21/disk/`.

## Freed (steps 1 to 3)
| Step | What | Freed |
|---|---|---|
| 1 | 49 Rust `target/` directories next to a Cargo.toml (none written in the last 30 min) and 45 Nix `result*` symlinks into /nix/store (lists: targets-delete.txt, results-delete.txt) | ~53G (targets) |
| 2 | `nix-collect-garbage -d` (user profiles; `sudo -n` needs a password, so the system profile was not touched) | 147.2G, 34569 store paths |
| 2 | `nix store optimise` (ended with a "No space left" error on one link at 8 min; hard linking freed 315 MiB more) | 0.3G |
| 3 | ~/.cache/{nix,zig,uv,fontconfig}, ~/.npm/_cacache, ~/.cargo/registry/{cache,src} | ~8G |

## Biggest candidate: one repository, git temp files (not deleted)
| Size | What |
|---|---|
| 108G | `/git/github.com/openclaw/openclaw/.git/objects/pack/` holds 29 `tmp_pack_*` files (3 to 6G each, written 2026-11-06/07): partial packs of fetches that never finished. No git process is running. They hold no committed content; `git -C /git/github.com/openclaw/openclaw gc --prune=now` or deleting `tmp_pack_*` frees them. Needs your word. |

## Section 4: home-root repositories against /git
| Path | Size | What | Safe to delete? |
|---|---|---|---|
| core, secondary, tertiary, quaternary | 0 | symlinks into /git/github.com/LiGoldragon/ | symlinks only |
| .primary-old-vcs-01e496 | 2.6G | clone of LiGoldragon/primary | check for unpushed commits first; not compared |
| primary-stale-backup-01e496 | 657M | not a repository, tree copy | looks safe |
| private-repos | 18.7G | not a repository; flow-evidence 16.3G, recovery 1.7G, worktree-retirement-archives 0.6G | evidence archives: your decision |
| wt | 503M | github.com 476M, flow/criomos evidence dirs | looks stale |
| worktrees | 988M | belief-rename-8d9ef9 612M, noctalia-external-01a01b52 281M, small ones | after worktree check |
| recovery | 221M | criomos-home baselines | looks safe |
| work, scratch-store-migration, gh, witnesses | 20M, 37M, 1M, 14M | small | leave |

## Section 5: git worktrees
452 linked worktrees, 3.1G in all (sec5.txt: size, path, branch, last commit date, upstream, dirty count). 323 are in /git/worktrees (0.8G), 70 in /tmp/claude-1001 (1.5G, old scratchpads), 27 in /home/li (64M). Biggest: /tmp/belief-final-9a6 503M, /tmp/claude-1001/*/scratchpad/{rec,wt,wt-primary} ~360M each. Not worth the effort next to the 108G above.

## Section 6: largest places (root 660G used before this section's tmp_pack removal)
| Size | Where |
|---|---|
| 231G | /nix (after GC) |
| 180G | /home: Downloads 60.6G, private-repos 18.7G, .local 17.9G (share 10.1G, state 7.8G), .codex 13.4G, Audiobooks 10.0G, .codex-next-8mkkxq293hk2 9.6G, .config 8.5G, .cache 8.0G, .codex-next 6.7G, Documents 4.3G, Music 4.0G, .claude 3.9G |
| 147G | /git: openclaw 110G (of which 108G tmp_pack), LiGoldragon 11G, NixOS 5.7G, stablyai 2.6G |
| 61G | /tmp: claude-1001 34.6G (743 entries), flow-integ-2zHX 9.4G, beads-supported.V6r4gb 3.5G, flow-052-* 4.5G, herdr-ready-race 1.8G |
| 7.9G | /var: log 4.1G, lib 3.7G (waydroid images 2.9G) |
Largest single files: sec6-bigfiles.txt (tmp_packs first; then chrome OptGuide weights.bin 4.0G, nixpkgs pack 3.6G, codex thread_history sqlite 3.5G/2.1G/1.3G, Succession season videos in Downloads, waydroid system.img 2.4G).

## Section 7: large files not modified in over six months (>50M, 77 files, sec7-stale-files.txt)
No file over 100M has also gone unread for six months (read times are recent). By modification age only: nixpkgs pack 3.6G (2025-07), waydroid system.img 2.4G and vendor.img 0.5G (2025-08), Audiobooks (m4b/rar/webm, 0.4 to 1.3G each, 2025-10 to 2026-02), old packs of langgraph/OpenHands/wezterm. Downloads video files (60G in all, 2026-09) are read recently.

## Section 8: agent directories
| Directory | Large parts |
|---|---|
| ~/.codex (13.4G) | .tmp 8.2G (many `git-*` temp dirs and plugin sync), archived_sessions 0.9G, thread_history_1.sqlite 3.5G |
| ~/.codex-next (6.7G) | archived_sessions 3.4G, .tmp 1.1G, thread_history_1.sqlite 1.3G |
| ~/.codex-next-8mkkxq293hk2 (9.6G) | archived_sessions 4.1G, sessions 2.3G, thread_history_1.sqlite 2.1G (written today: in use) |
| ~/.claude (3.9G) | projects 3.8G (transcripts) |
| ~/.traycer (2.7G) | host 2.0G, models 0.6G |
| ~/.gemini (0.7G) | tmp 0.7G |
~/.codex/.tmp (8.1G) looks like regenerable temp.

## Needs your decision (largest first)
1. openclaw `tmp_pack_*`: 108G.
2. /tmp: 61G (claude-1001 scratchpads, flow-integ, beads, flow-052 checks), if no flow still uses them.
3. ~/.codex/.tmp 8.1G; archived codex sessions ~8.4G.
4. Downloads videos 60G, private-repos/flow-evidence 16G, system-profile GC (`sudo` needed).
