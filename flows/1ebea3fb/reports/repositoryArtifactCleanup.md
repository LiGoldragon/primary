# Repository artifact cleanup

The cleanup removed 37 understood derived artifacts without touching source,
package caches, boot or rollback state, or uncertain ownership. The first
round removed 31 Cargo `target/` trees and one Python `__pycache__`; a bounded
follow-up resolved and removed four previously preserved Cargo targets and
one archive Python `__pycache__`.

## Congregations and repository map

The complete congregation and repository map is witnessed in
`flows/1ebea3fb/witnesses/congregationInventory.md`. The important boundary is
that `/home/li/primary/repos` is a symlink to `/git/github.com/LiGoldragon`,
not a second copy. The scan found 595 unique VCS roots under `/git`, 238
unique roots in the focused `/home/li` scan, 132 archived roots, 72 isolated
`/home/li/wt` roots, and the additional worktree/history/cache roots recorded
in the witness. The focused repositories carried multi-label markers for Rust
(105), Nix (152), Python (14), and Node (22); 51 had no recognized marker.
The broader `/git` scan found 595 roots: 404 Git-only and 191 with both Git
and Jujutsu markers. Its multi-label markers were Rust 236, Nix 344, Python
39, and Node 89; 141 had no recognized marker and 228 had multiple markers.

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

The first-round pre-delete `du -sx --bytes` sum was 37,930,817,068 bytes
(35.325826 GiB). The first-round post-delete sum was 0 bytes, yielding
37,930,817,068 directory-measured bytes reclaimed. The follow-up receipt in
`flows/1ebea3fb/witnesses/incrementalCandidateCleanup.md` measured
13,172,906,260 additional bytes before deletion and 0 afterward. Cumulative
directory-measured reclaim is therefore **51,103,723,328 bytes** (47.594051
GiB, 51.103723 GB). The independent first-round `df -P` delta was
38,011,604,992 bytes (35.401066 GiB); the follow-up observed a separate
13,277,585,408-byte used-block decrease, reported independently because
filesystem allocation includes metadata and other effects. All 37 selected
paths are absent. Deletion completed with 37 successes and 0 failures.

## Incremental resolution of the five preserved candidates

The first round preserved four dirty Cargo targets and one archive Python
cache. The explicit cleanup request settled that dirty work elsewhere is not
itself a reason to retain an independent derived output, so each path was
audited against repository metadata, parent-commit/index evidence, and its
payload before deletion. The exact evidence and measurements are in
`flows/1ebea3fb/witnesses/incrementalCandidateCleanup.md`.

- `/git/github.com/LiGoldragon/Curriculum/target`: Cargo markers and only
  Cargo output; no current manifest, no parent-commit match, and 3,410
  target-only working-copy additions. Safe as untracked derived output; its
  2,033,177,042 bytes were removed.
- `/git/github.com/LiGoldragon/lojix/target`: successful offline Cargo
  metadata, `target/` ignore rule, no parent-commit match, and no target
  status entries. Safe and reproducible; 10,644,240,040 bytes removed.
- `/git/github.com/LiGoldragon/spirit/target`: successful offline Cargo
  metadata, `/target` ignore rule, no parent-commit match, and no target
  status entries. Safe and reproducible; 495,431,163 bytes removed.
- `/git/github.com/LiGoldragon/spirit-ethos/target`: successful offline Cargo
  metadata, no parent-commit match, and 15 target additions distinct from
  six source/config changes. Safe as wholly derived untracked output;
  120,784 bytes removed.
- `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__`:
  parent repo has `.git` and `.jj`, no parent-commit match, no index strings
  for the cache, and the directory held 11 `.pyc` files beside eight `.py`
  sources. Safe as untracked Python bytecode; 57,231 bytes removed.

All five exact paths were absent after deletion, with five successes and zero
failures. The containing repositories' unrelated dirty work was preserved.

## Historical first-round preservation and final disposition

Four clear targets were preserved during the first round because their
repositories had pre-existing dirty work: `Curriculum` (target-only dirty
state), `lojix` (dirty `.beads`), `spirit` (dirty source edits), and
`spirit-ethos` (dirty source edits plus target additions). The follow-up
metadata audit established that each target itself was independent derived
output, so all four were then deleted. The archive Python cache was likewise
audited as an untracked, wholly derived cache in the both-VCS-marker
`Mentci-AI` repository and then deleted. None remains and there were no
deletion failures.

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
- `flows/1ebea3fb/witnesses/incrementalCandidateCleanup.md`
- `flows/1ebea3fb/log.md`
