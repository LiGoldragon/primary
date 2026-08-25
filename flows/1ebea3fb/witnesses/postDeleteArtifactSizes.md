# First-round post-delete artifact measurements

Method: rerun `test -e PATH` for every selected path, rescan `/git` and the
worktree congregations with the same `find` candidate expression used before,
rerun `du -sx --bytes` on preserved candidates, and rerun `jj status
--no-pager` for every selected and preserved Jujutsu root.

All 32 first-round selected paths are absent: `selected_missing=32`,
`selected_residue=0`. At this first-round measurement, the post-delete
candidate scan contained only the four preserved dirty-repository targets:

- `/git/github.com/LiGoldragon/Curriculum/target`
- `/git/github.com/LiGoldragon/lojix/target`
- `/git/github.com/LiGoldragon/spirit/target`
- `/git/github.com/LiGoldragon/spirit-ethos/target`

No cleanup candidate remained under `/home/li/wt`, `/home/li/worktrees`,
`/home/li/primary-worktrees`, or `/home/li/primary-workspaces`. The
archive `__pycache__` was also intentionally skipped at this first-round
measurement. The follow-up witness
`flows/1ebea3fb/witnesses/incrementalCandidateCleanup.md` records the
metadata audit and subsequent deletion of these five preserved candidates;
all five are absent in the final state. Package/dependency trees and
virtual-environment `site-packages/**/__pycache__` directories were excluded
from the cleanup scan and retained.

## First-round preserved post-delete measurements

| Path | Post-delete bytes |
| --- | ---: |
| `/git/github.com/LiGoldragon/Curriculum/target` | 2,033,177,042 |
| `/git/github.com/LiGoldragon/lojix/target` | 10,644,240,040 |
| `/git/github.com/LiGoldragon/spirit/target` | 495,431,163 |
| `/git/github.com/LiGoldragon/spirit-ethos/target` | 120,784 |
| `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__` | 57,231 |

The selected directories' post-delete allocated total is 0 bytes, so the
directory-measured reclaimed total is **37,930,817,068 bytes** (35.325826
GiB, 37.930817 GB). An independent `df -P` observation changed used space
from 536,966,636 to 499,845,928 1-KiB blocks, a filesystem delta of
38,011,604,992 bytes (35.401066 GiB); this includes filesystem allocation
rounding and concurrent report/metadata activity, so the directory sum is the
cleanup receipt.

All 31 selected Jujutsu repository roots remained clean after deletion. The
four dirty repositories retained their pre-existing dirty state; no source,
beads, boot, rollback, or package-cache paths were changed.

## Sources

- `flows/1ebea3fb/witnesses/preDeleteArtifactSizes.md`
- `flows/1ebea3fb/witnesses/congregationInventory.md`
- `flows/1ebea3fb/witnesses/incrementalCandidateCleanup.md`
- Deletion command output in the flow transcript: 32 `DELETED` lines,
  `deleted=32 failures=0 selected=32`.
