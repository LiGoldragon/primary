# Pre-delete artifact measurements

Method: probe each exact candidate path with `du -sx --bytes PATH` (one
filesystem total, allocated bytes as reported by GNU `du`), `find PATH -type
f` for a file count, `stat` for type and timestamp, and `jj status --no-pager`
from each Jujutsu repository root. Active build processes were checked with
`pgrep -af '(^|/)(cargo|rustc|rustdoc|cargo-watch|nix-build|nix develop|nix run|python.*build)'`;
none were running. No `/nix/store` search was performed.

The selected set contains 32 paths: 24 clean `/git` Cargo targets, one clean
`/git` Python cache, and seven clean `/home/li/wt` Cargo targets. The selected
set's pre-delete allocated total is **37,930,817,068 bytes** (35.325826 GiB,
37.930817 GB).

## Selected `/git` artifacts

| Repository | Artifact | Bytes | Files |
| --- | --- | ---: | ---: |
| `LiGoldragon/chroma` | `/git/github.com/LiGoldragon/chroma/target` | 4,361,956,388 | measured in scan |
| `LiGoldragon/content-identity` | `/git/github.com/LiGoldragon/content-identity/target` | 211,785,161 | measured in scan |
| `LiGoldragon/core-ethos` | `/git/github.com/LiGoldragon/core-ethos/target` | 400,518,647 | measured in scan |
| `LiGoldragon/core-logos` | `/git/github.com/LiGoldragon/core-logos/target` | 227,658,531 | measured in scan |
| `LiGoldragon/core-nomos` | `/git/github.com/LiGoldragon/core-nomos/target` | 299,650,436 | measured in scan |
| `LiGoldragon/curriculum-deploy` | `/git/github.com/LiGoldragon/curriculum-deploy/target` | 224,355,442 | measured in scan |
| `LiGoldragon/datom` | `/git/github.com/LiGoldragon/datom/target` | 382,030,837 | measured in scan |
| `LiGoldragon/dotos` | `/git/github.com/LiGoldragon/dotos/target` | 322,409,070 | measured in scan |
| `LiGoldragon/ethos-monolith` | `/git/github.com/LiGoldragon/ethos-monolith/target` | 1,239,232,662 | measured in scan |
| `LiGoldragon/ethos-monolith` | `/git/github.com/LiGoldragon/ethos-monolith/checks/__pycache__` | 0 | empty directory; 4,096 apparent bytes |
| `LiGoldragon/horizon-rs` | `/git/github.com/LiGoldragon/horizon-rs/target` | 299,253,618 | measured in scan |
| `LiGoldragon/meta-signal-orchestrate` | `/git/github.com/LiGoldragon/meta-signal-orchestrate/target` | 799,223,476 | measured in scan |
| `LiGoldragon/meta-signal-psyche` | `/git/github.com/LiGoldragon/meta-signal-psyche/target` | 16,604,307 | measured in scan |
| `LiGoldragon/meta-signal-spirit` | `/git/github.com/LiGoldragon/meta-signal-spirit/target` | 279,961,625 | measured in scan |
| `LiGoldragon/orchestrate` | `/git/github.com/LiGoldragon/orchestrate/target` | 1,099,239,024 | measured in scan |
| `LiGoldragon/protos` | `/git/github.com/LiGoldragon/protos/target` | 528,973,943 | measured in scan |
| `LiGoldragon/psyche` | `/git/github.com/LiGoldragon/psyche/target` | 19,318,314 | measured in scan |
| `LiGoldragon/rust-logos` | `/git/github.com/LiGoldragon/rust-logos/target` | 289,665,188 | measured in scan |
| `LiGoldragon/schema-rust` | `/git/github.com/LiGoldragon/schema-rust/target` | 1,462,321,512 | measured in scan |
| `LiGoldragon/sema-engine` | `/git/github.com/LiGoldragon/sema-engine/target` | 1,447,645,490 | measured in scan |
| `LiGoldragon/sema-translator` | `/git/github.com/LiGoldragon/sema-translator/target` | 393,466,763 | measured in scan |
| `LiGoldragon/signal-domain` | `/git/github.com/LiGoldragon/signal-domain/target` | 478,698,769 | measured in scan |
| `LiGoldragon/signal-orchestrate` | `/git/github.com/LiGoldragon/signal-orchestrate/target` | 915,260,614 | measured in scan |
| `LiGoldragon/signal-psyche` | `/git/github.com/LiGoldragon/signal-psyche/target` | 7,065,445 | measured in scan |
| `LiGoldragon/signal-spirit` | `/git/github.com/LiGoldragon/signal-spirit/target` | 1,344,601,744 | measured in scan |

The `/git` selected Cargo targets all have a repository-level `Cargo.toml`,
`Cargo.lock`, and `flake.nix`; their `jj status` was clean. The `__pycache__`
directory is empty and sits in the clean `ethos-monolith/checks` tree.

## Selected `/home/li/wt` artifacts

| Repository/worktree | Artifact | Bytes |
| --- | --- | ---: |
| `chroma-terminal-state` | `/home/li/wt/github.com/LiGoldragon/chroma-terminal-state/target` | 5,387,652,451 |
| `datom/epic-datom-path-locks-20260822` | `/home/li/wt/github.com/LiGoldragon/datom/epic-datom-path-locks-20260822/target` | 97,440,130 |
| `listener/parallel-transcription-healing` | `/home/li/wt/github.com/LiGoldragon/listener/parallel-transcription-healing/target` | 2,823,993,538 |
| `lojix/fixlojixbootownership` | `/home/li/wt/github.com/LiGoldragon/lojix/fixlojixbootownership/target` | 3,676,685,294 |
| `lojix/remove-effect-timeout` | `/home/li/wt/github.com/LiGoldragon/lojix/remove-effect-timeout/target` | 6,092,832,625 |
| `meta-signal-orchestrate/epic-datom-path-locks-20260822` | `/home/li/wt/github.com/LiGoldragon/meta-signal-orchestrate/epic-datom-path-locks-20260822/target` | 440,319,763 |
| `orchestrate/epic-datom-path-locks-20260822` | `/home/li/wt/github.com/LiGoldragon/orchestrate/epic-datom-path-locks-20260822/target` | 2,360,996,261 |

All seven worktree roots have repository-level `Cargo.toml`, `Cargo.lock`,
and `flake.nix`; `jj status --no-pager` reported no working-copy changes.

## Preserved candidates

These clear derived candidates were measured but not selected:

| Path | Bytes | Reason |
| --- | ---: | --- |
| `/git/github.com/LiGoldragon/Curriculum/target` | 2,033,177,042 | repository has target-only pre-existing dirty state; preserve exactly |
| `/git/github.com/LiGoldragon/lojix/target` | 10,644,240,040 | repository has pre-existing `.beads` dirty state |
| `/git/github.com/LiGoldragon/spirit/target` | 495,431,163 | repository has pre-existing source edits |
| `/git/github.com/LiGoldragon/spirit-ethos/target` | 120,784 | repository has pre-existing source edits and target additions |
| `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__` | 57,231 | Git-only archive repository; dirty state cannot be inspected under local VCS rules |

Other generated-looking names (`build`, `dist`, `out`, `result*`, and
`linux-7.1.8`) were retained because they are source/package outputs,
Nix-result links, rollback-adjacent state, or otherwise not proven disposable.
Node dependency trees and virtual environments were excluded as dependencies,
not build artifacts.

## Sources

- `flows/1ebea3fb/witnesses/congregationInventory.md`
- Probe commands and exact outputs from the pre-delete scan in the flow
  transcript.
