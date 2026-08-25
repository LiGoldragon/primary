# Repository artifact cleanup

The cleanup removed 32 understood derived artifacts without touching source,
package caches, boot or rollback state, or uncertain ownership. The selected
directories were 31 Cargo `target/` trees and one Python `__pycache__`.

## Congregations and repository map

The complete congregation and repository map is witnessed in
`flows/1ebea3fb/witnesses/congregationInventory.md`. The important boundary is
that `/home/li/primary/repos` is a symlink to `/git/github.com/LiGoldragon`,
not a second copy. The scan found 595 unique VCS roots under `/git`, 238
unique roots in the focused `/home/li` scan, 132 archived roots, 72 isolated
`/home/li/wt` roots, and the additional worktree/history/cache roots recorded
in the witness. The focused repositories carried multi-label markers for Rust
(105), Nix (152), Python (14), and Node (22); 51 had no recognized marker.

## Deleted artifacts, grouped by ecosystem and repository

### Rust Cargo targets

Each path below had a repository-level `Cargo.toml`, `Cargo.lock`, and
`flake.nix`, and its Jujutsu root was clean before deletion.

`/git` repositories:

- `chroma`: `/git/github.com/LiGoldragon/chroma/target`
- `content-identity`: `/git/github.com/LiGoldragon/content-identity/target`
- `core-ethos`: `/git/github.com/LiGoldragon/core-ethos/target`
- `core-logos`: `/git/github.com/LiGoldragon/core-logos/target`
- `core-nomos`: `/git/github.com/LiGoldragon/core-nomos/target`
- `curriculum-deploy`: `/git/github.com/LiGoldragon/curriculum-deploy/target`
- `datom`: `/git/github.com/LiGoldragon/datom/target`
- `dotos`: `/git/github.com/LiGoldragon/dotos/target`
- `ethos-monolith`: `/git/github.com/LiGoldragon/ethos-monolith/target`
- `horizon-rs`: `/git/github.com/LiGoldragon/horizon-rs/target`
- `meta-signal-orchestrate`: `/git/github.com/LiGoldragon/meta-signal-orchestrate/target`
- `meta-signal-psyche`: `/git/github.com/LiGoldragon/meta-signal-psyche/target`
- `meta-signal-spirit`: `/git/github.com/LiGoldragon/meta-signal-spirit/target`
- `orchestrate`: `/git/github.com/LiGoldragon/orchestrate/target`
- `protos`: `/git/github.com/LiGoldragon/protos/target`
- `psyche`: `/git/github.com/LiGoldragon/psyche/target`
- `rust-logos`: `/git/github.com/LiGoldragon/rust-logos/target`
- `schema-rust`: `/git/github.com/LiGoldragon/schema-rust/target`
- `sema-engine`: `/git/github.com/LiGoldragon/sema-engine/target`
- `sema-translator`: `/git/github.com/LiGoldragon/sema-translator/target`
- `signal-domain`: `/git/github.com/LiGoldragon/signal-domain/target`
- `signal-orchestrate`: `/git/github.com/LiGoldragon/signal-orchestrate/target`
- `signal-psyche`: `/git/github.com/LiGoldragon/signal-psyche/target`
- `signal-spirit`: `/git/github.com/LiGoldragon/signal-spirit/target`

`/home/li/wt` worktrees:

- `chroma-terminal-state`: `/home/li/wt/github.com/LiGoldragon/chroma-terminal-state/target`
- `datom/epic-datom-path-locks-20260822`: `/home/li/wt/github.com/LiGoldragon/datom/epic-datom-path-locks-20260822/target`
- `listener/parallel-transcription-healing`: `/home/li/wt/github.com/LiGoldragon/listener/parallel-transcription-healing/target`
- `lojix/fixlojixbootownership`: `/home/li/wt/github.com/LiGoldragon/lojix/fixlojixbootownership/target`
- `lojix/remove-effect-timeout`: `/home/li/wt/github.com/LiGoldragon/lojix/remove-effect-timeout/target`
- `meta-signal-orchestrate/epic-datom-path-locks-20260822`: `/home/li/wt/github.com/LiGoldragon/meta-signal-orchestrate/epic-datom-path-locks-20260822/target`
- `orchestrate/epic-datom-path-locks-20260822`: `/home/li/wt/github.com/LiGoldragon/orchestrate/epic-datom-path-locks-20260822/target`

### Python cache

- `ethos-monolith/checks`: `/git/github.com/LiGoldragon/ethos-monolith/checks/__pycache__`
  (empty; 0 allocated bytes)

## Measurements and outcome

The pre-delete `du -sx --bytes` sum was 37,930,817,068 bytes (35.325826
GiB). The post-delete sum for all selected paths is 0 bytes, yielding
37,930,817,068 directory-measured bytes reclaimed. The independent filesystem
`df -P` delta was 38,011,604,992 bytes (35.401066 GiB). Deletion completed
with 32 successes and 0 failures; all selected paths were absent afterward.

## Preserved, skipped, and failures

Four clear targets were skipped because their repositories had pre-existing
dirty work: `Curriculum` (target-only dirty state), `lojix` (dirty `.beads`),
`spirit` (dirty source edits), and `spirit-ethos` (dirty source edits plus
target additions). Their post-delete sizes are 2,033,177,042,
10,644,240,040, 495,431,163, and 120,784 bytes respectively. The archive
Python cache `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__`
(57,231 bytes) was skipped because its Git-only repository's dirty state
cannot be inspected under local VCS rules. There were no deletion failures.

Nix `result`, `result-1`, and `result-2` links, `linux-7.1.8`, rollback
evidence, package caches, Node dependency trees, virtual environments, and
source-like `build`, `dist`, and `out` directories were retained. No
`/nix/store` search was performed.

The Orchestrate registration and claim were attempted for the exact cleanup
paths, but both CLIs returned a transport `ENOENT` because their daemon socket
was unavailable. This advisory coordination failure is recorded; no other
agent's dirty work was overwritten.

## Sources

- `flows/1ebea3fb/witnesses/congregationInventory.md`
- `flows/1ebea3fb/witnesses/preDeleteArtifactSizes.md`
- `flows/1ebea3fb/witnesses/postDeleteArtifactSizes.md`
- `flows/1ebea3fb/log.md`
