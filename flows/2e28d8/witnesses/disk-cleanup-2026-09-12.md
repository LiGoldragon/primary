# Disk cleanup witness — 2026-09-12

Baseline: root used 920,810,106,880 B; free 12,022,657,024 B (99%). Nix had 134,795 paths and 358,141,801,760 B NAR total.

Removed 68 rebuildable Rust `target` directories under `/git/github.com`, measured at 246,902,869,905 B, and seven scoped repository/primary `result*` symlinks. Removed Home Manager generations 1024 and 1025, preserving current generation 1026. System-profile pruning through `nix-env --delete-generations old --profile /nix/var/nix/profiles/system` failed as expected with permission denied; current boot and system profile both resolve to `41cvi7l9rjy3n05jixzqdk937rg8gz27-nixos-system-ouranos-26.11.20260813.0e251e2`, and system links 181–183 remain.

Removed 18 stale, checked-clear temporary build/extraction trees, including `/tmp/flow857335-spirit-1050` (33,042,791,419 B) and the large `tmp.*`, Wispr, ChatGPT, Claude Desktop, Lojix, listener, spirit, and Orchestrate audit trees. `/tmp/claude-1001` was retained because a live Claude process held an open directory FD. Runtime socket/profile directories, browser data, caches, Waydroid, and user-decision items were excluded. One protected Go-module temporary tree could not be fully removed due to permission-denied descendants; no sudo was used.

One `nix store gc` ran after confirming no active real GC (two other observed commands were dry runs). It completed successfully. After cleanup, root used 517,249,900,544 B; free 415,582,863,360 B (56%), an increase of 403,560,206,336 B. Nix then had 114,326 paths and 268,538,124,960 B NAR total.
