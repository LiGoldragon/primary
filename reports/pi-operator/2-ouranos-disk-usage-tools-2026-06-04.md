# Ouranos disk-usage tools and current disk map

Date: 2026-06-04
Role: pi-operator
Host: `ouranos`

## Scope and privacy posture

This is a small operator report for finding the disk-usage tools currently available in the CriomOS home profile and choosing the most agent-friendly way to inspect disk usage. I kept the scan at system, top-level directory, repo, cache, and build-artifact granularity. I did not print shell-history command arguments, deleted-file names, or raw Nix store paths.

## Installed tools found

The active user profile has these disk/filesystem inspection tools on `PATH`:

| Tool | Installed | Current role |
|---|---:|---|
| `dua` | yes, version 2.34.0 | Best installed modern scanner for quick agent/human size scans. |
| `ncdu` | yes, version 2.9.2 | Best installed interactive human cleanup browser; can also export scans. |
| `du` / `df` | yes, GNU coreutils 9.10 | Best fallback for stable scriptable tables. |
| `broot`, `eza`, `fd`, `rg`, `lsblk` | yes | Navigation/search/support tools, not primary disk-usage analyzers. |
| `erdtree` / `erd` | no | The remembered “ErdTree or something” is not currently installed on this machine. |
| `dust`, `gdu`, `duf`, `dysk`, `agedu` | no | Not currently installed in the active profile. |

CriomOS-home source confirms `dua` and `ncdu` are intentional profile tools: `modules/home/profiles/min/default.nix` installs `dua # Disk usage` and `ncdu # File visualizing` in the minimum profile.

Shell-history check: only `.bash_history` was present; candidate disk-tool command names did not appear in the sanitized first-token count. I did not inspect or report arguments.

## Recommendation for agents

Use this stack:

1. `df -hT -x tmpfs -x devtmpfs -x efivarfs` for filesystem pressure.
2. `NO_COLOR=1 dua -x -f gib PATHS...` for quick modern size scans.
3. `du -x -BM -d1 PATH | sort -nr` when exact, parseable, no-ANSI output matters more than speed.
4. `ncdu -x -r PATH` for a human cleanup session. If an agent needs a reusable snapshot, use `ncdu -0 -x -o /tmp/name.ncdu PATH` and parse/export privately rather than putting the tree in chat.

For this machine, `dua` is the best installed modern choice, but `du` remains the best fully deterministic agent-reporting primitive because it produces plain, stable text with no TUI assumptions.

## Current disk pressure

`df` reports the root filesystem as 916 GiB total, 808 GiB used, 62 GiB available, 93% full. This is high enough that cleanup should be treated as near-term maintenance, especially before large builds.

Readable top-level disk buckets from non-root scans:

| Bucket | Approximate size | Notes |
|---|---:|---|
| `/git` | 309 GiB | Largest readable bucket. Mostly public LiGoldragon repo build artifacts. |
| `/home` | 173 GiB | Mostly worktrees, downloads/media, agent logs, and caches. |
| `/nix/store` | 138 GiB | Large but not currently showing user-visible GC reclaim. |
| `/tmp` | 13 GiB | Agent/test sandboxes and temporary build/test outputs. |
| `/var` | 6 GiB | Not the main pressure point from user-readable scan. |

The readable `du` total is materially lower than `df` used space. Non-root scanning cannot fully explain the gap. Visible deleted-open files account for about 19 GiB, held mainly by `mpv`, `chrome`, and a Nautilus wrapper process. The remaining gap needs root-level inspection to distinguish root-owned inaccessible files, other deleted-open files, ext4 reserved blocks, or accounting differences.

## Biggest actionable consumers

### `/git`: Rust target directories dominate

`/git/github.com/LiGoldragon` is about 287 GiB. `target` directories under it total about 282 GiB by `du -c`, so this bucket is essentially build output, not source.

Largest examples:

| Path | Approximate size |
|---|---:|
| `/git/github.com/LiGoldragon/persona/target` | 48 GiB |
| `/git/github.com/LiGoldragon/persona-spirit/target` | 34 GiB |
| `/git/github.com/LiGoldragon/router/target` | 20 GiB |
| `/git/github.com/LiGoldragon/mind/target` | 19 GiB |
| `/git/github.com/LiGoldragon/terminal/target` | 17 GiB |
| `/git/github.com/LiGoldragon/chroma/target` | 16 GiB |
| `/git/github.com/LiGoldragon/message/target` | 10 GiB |
| `/git/github.com/LiGoldragon/introspect/target` | 10 GiB |

### `/home/li/wt`: worktree build outputs

`/home/li/wt` is about 74 GiB. `target` directories under LiGoldragon worktrees total about 73 GiB, again mostly Rust build output.

Largest examples:

| Path | Approximate size |
|---|---:|
| `/home/li/wt/github.com/LiGoldragon/kameo/kameo-push-only-lifecycle/target` | 10 GiB |
| `/home/li/wt/github.com/LiGoldragon/persona-spirit/spirit-privacy-archive-2026-06-04/target` | 8 GiB |
| `/home/li/wt/github.com/LiGoldragon/chroma/next/target` | 5 GiB |
| `/home/li/wt/github.com/LiGoldragon/persona-spirit/spirit-random-hash-identities/target` | 4 GiB |
| `/home/li/wt/github.com/LiGoldragon/lojix/*/target` | several 4 GiB targets |

### Home caches and agent state

Readable top-level Home buckets include:

| Bucket | Approximate size | Notes |
|---|---:|---|
| `/home/li/Downloads` | 25 GiB | Personal/download content; not expanded. |
| `/home/li/.codex` | 16 GiB | Mostly Codex session state. |
| `/home/li/.cache` | 13 GiB | Mostly Go build cache, Nix eval/cache, Chrome, Puppeteer, Hugging Face, uv, qutebrowser. |
| `/home/li/Audiobooks` | 10 GiB | Personal media; not expanded. |

### `/tmp`

`/tmp` is about 13 GiB. The largest visible sub-bucket is `/tmp/pi-subagents-uid-1001` at about 4.1 GiB. Several old schema/cloud/spirit audit or mockup sandboxes are each hundreds of MiB. This is easy space to reclaim once no active agent session depends on those directories.

## Cleanup priorities

1. Highest impact: remove stale Rust `target` directories in inactive `/git/github.com/LiGoldragon/*` checkouts and inactive `~/wt` worktrees. This is the clear dominant use of readable space and could recover hundreds of GiB. Do not remove targets for active work without checking current lanes/locks.
2. Medium impact: clear stale `/tmp` agent/test sandboxes after confirming no live agent/session uses them.
3. Medium impact: prune `.codex` sessions and selected Home caches only with a retention policy; they are useful debugging/session substrate and may contain private context.
4. Lower confidence: Nix store GC is not the obvious win from this account; `nix store gc --dry-run` reported `0 store paths would be deleted`. Root/system GC may differ, but should be a separate root-authorized maintenance action.
5. Root-required: investigate the remaining `df` versus readable-`du` gap. Start with root `du`, root `lsof +L1`, and ext4 reserved-block/accounting checks before deleting anything.
