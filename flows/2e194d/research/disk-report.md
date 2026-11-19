# Disk cleanup: about 25 GB recovered on the laptop

**Progress report, 18 November.** The laptop has about **25.3 GB more available space**. Its disk use fell from **74% to 72%**. No files have been deleted on Prometheus. Garbage collection and some builder-cache decisions are still waiting for the ongoing deployment work to release them safely. This is not a claim that every requested step is finished.

All figures use decimal GB. “Available” means space ordinary users can allocate; reserved filesystem space explains why used plus available is below total. Directory sizes are allocated-block estimates, not the same measurement as whole-filesystem free space. Concurrent work continues to write files.

## Before and after, by host

| Host | Total GB | Used before GB | Available before GB | Used now GB | Available now GB | Observed availability change GB |
|---|---:|---:|---:|---:|---:|---:|
| Laptop — ouranos | 982.83 | 688.53 | 244.31 | 663.24 | 269.59 | +25.29 |
| Builder — prometheus | 1999.32 | 1385.40 | 594.26 | 1385.49 | 594.17 | −0.09 |

The builder's small change is concurrent activity, **not cleanup**. Approximately50.0 GB on the laptop and19.7 GB on the builder are outside the used-plus-user-available figures because of filesystem reservations/accounting.

## What each cleanup step did

Before each deletion phase I reported the proposed scope and measured size. Changing, reserved, unverified or in-use items were held back. “Removed GB” below counts completed removals' allocated blocks; the filesystem-wide gain above is the better measure of the practical result.

| Step | Laptop: removed GB and outcome | Prometheus: removed GB and outcome | What changes in practice |
|---|---|---|---|
| Old build output | 0 separately classified repository outputs found eligible. Old test/build outputs inside temporary scratch are counted below, not twice. Active-project caches were preserved. | 0; old active-project build caches await explicit custody confirmation. | Cleared build scratch will compile again if its old tests are repeated. Current build inputs/caches were protected. |
| Merged worktrees | **0.020 GB**,44 clean worktrees merged into their main branch. | 0; no builder worktree removed. | Extra checkout directories disappear; branches and history remain in their parent repositories. |
| Temporary files older than seven days | **18.853 GB**,17326 completed scratch-root removals. Three root-owned residues required a guarded root retry. One66.6 MB plugin-cache residue remains because its running-tool dependency is uncertain. | 0. Only a tiny old host-input staging directory qualified in the bounded scan; it was retained as uncertain deployment material. The large scratch areas are recent or held. | Old logs and test/build scratch are gone. They cannot be used later as local historical evidence. Explicitly retained deployment, native-test and private-audit evidence was excluded. |
| Transcripts older than a month | **0.171 GB**,268 old regular JSONL transcripts, with fresh identity/open-file checks and no current native-session match. | 0; no corresponding transcript directories were found in the checked home. | Those old local conversations cannot be reopened from the deleted files. Current conversations remain. |
| Nix-store garbage collection | **Pending;0 claimed.** | **Pending;0 claimed.** | Profiles and roots have not been removed. Required deployment caches are not all rooted yet; collecting them now could erase work the active repair must reuse. |
| Inactive repositories | **6.356 GB**,114 checkouts removed after fresh checks of cleanliness, every branch/tag on the actual remote, no extra local references, no reflog-only commits and no worktree/process/reservation use. Nine final candidates were held when current use/reservations matched. | 0; there is no `/git` checkout tree on this host. Other source copies are findings, not automatically treated as disposable repositories. | An agent can shallow-clone these again when needed. No verified unique local work was discarded. |
| Old procedures | No deletion. See below. | No deletion. | The existing rules are guidance; no automatic cleanup service was installed. |

Completed removals total **25.400 GB of allocated blocks**. The measured whole-disk availability gain is **25.289 GB**. These differ because of concurrent writes and filesystem accounting; neither number is substituted for the other.

### What stayed

The repository audit covered746 checkouts. It found148 with changed/untracked files and93 with branch commits absent from their recorded remote references; these groups overlap. They were preserved. Other checkouts lacked sufficiently strong current remote proof, had extra local references/reflog work, were active, or had worktrees/current use. A stale remote reference alone was not accepted as proof of safe removal.

Of882 linked worktrees in that checkout audit,44 were removed and838 retained. Many were unmerged; others were detached, dirty, reserved or uncertain. The primary workspace's separate worktree registry was also retained, including its detached and relocation checkouts. A further47 checkouts were identified inside the older home workspace collections:13 were dirty and21 had branch work absent from recorded remote references, with overlap. None was deleted.

## File system at a glance

These are **measured before-cleanup directory snapshots**, except the explicitly calculated residuals. They give a consistent overview without pretending every directory was measured again after concurrent cleanup. Each row has a parent for an area chart. Expand a parent into its children; do not add a parent's size to its children.

### Laptop

| Area | Parent | GB | What it is |
|---|---|---:|---|
| Nix software store (`/nix/store`) | Used disk | 327.57 | Installed software, shared build outputs and cached dependencies; reclaimable portion not measured. |
| User home (`/home/li`) | Used disk | 200.69 | Personal files, tools, recordings and workspaces. |
| Repository collection (`/git`) | Used disk | 41.35 | Source checkouts and worktrees; smaller now after repository cleanup. |
| Temporary area (`/tmp`) | Used disk | 74.67 | Test/build scratch and temporary working files; substantially smaller now. |
| System variable data (`/var`) | Used disk | 8.31 | System logs and service data. |
| Remaining used space | Used disk | 35.94 | Calculated residual: other directories, filesystem overhead and measurement differences; not individually classified. |
| Downloads (`/home/li/Downloads`) | User home | 63.58 | Mostly downloaded media. |
| Private repository collection (`/home/li/private-repos`) | User home | 19.57 | Private source material; uniqueness not audited for deletion. |
| All measured Codex homes | User home | 33.53 | Session recordings, archives and runtime scratch across four installations. |
| Local application data (`/home/li/.local`) | User home | 19.82 | Search indexes and application/runtime data. |
| Tool caches (`/home/li/.cache`) | User home | 10.98 | Browser downloads, model files and tool caches. |
| Application configuration (`/home/li/.config`) | User home | 10.27 | Configuration and application-owned data. |
| Audiobooks (`/home/li/Audiobooks`) | User home | 10.49 | Personal audio library. |
| Main workspace (`/home/li/primary`) | User home | 4.77 | Source, reports, working records and repository history. |
| Claude recordings (`/home/li/.claude`) | User home | 4.42 | Mostly conversation recordings. |
| Documents and music | User home | 8.69 | Personal documents and music, combined. |
| Other home contents | User home | 14.57 | Calculated residual after the listed home areas. |

The main workspace is mostly its working files, not its Git history: working-flow material is about3.30 GB, while its Git directory is about0.293 GB.

### Prometheus

| Area | Parent | GB | What it is |
|---|---|---:|---|
| Temporary work (`/tmp`) | Used disk | 96.74 | Remote source/build/test staging. |
| User home (`/home/li`) | Used disk | 32.51 | Older build copies, source workspaces and tool data. |
| Store and other system data, not separated | Used disk | 1256.15 | Calculated residual. The store-size scan was stopped when the priority test VM was observed; no exact store size or garbage estimate is claimed. |
| Shared offload scratch (`/tmp/offload`) | Temporary work | 61.63 | Source and build copies sent from the laptop;45.56 GB is in deployment-tool scratch, which was not touched. |
| Large old integration scratch | Temporary work | 12.23 | Historical integration work; not established as safe to discard. |
| Another integration scratch area | Temporary work | 7.79 | Historical test/source material; retained. |
| Belief-generation scratch | Temporary work | 6.84 | Source/generation staging; retained. |
| Additional offload staging | Temporary work | 5.04 | More copied work material; retained. |
| Remaining temporary work | Temporary work | 3.21 | Calculated residual. |
| Build collection (`/home/li/build`) | User home | 10.71 | Mostly old compiler output. |
| Another old integration build copy | User home | 9.92 | Almost all compiler output;9.91 GB is its target directory. |
| Source/test work collection (`/home/li/work`) | User home | 2.99 | Several source copies and their compiler output. |
| Tool cache | User home | 1.72 | Downloaded/runtime cache. |
| Remaining home contents | User home | 7.17 | Calculated residual. |

## Possible savings — not deleted

Sizes below overlap where an item is part of a larger area. They are **not an additive reclamation promise**. Dates are directory-entry modification dates, not proof of last use; descendant activity/ownership is unknown unless specifically stated.

| Possible saving, largest first | Measured size | Last change / unique work | If approved / if kept |
|---|---:|---|---|
| Nix garbage on both hosts | **Unknown** | No safe garbage quantity measured. Some needed active caches are currently unrooted. | After owner release, ordinary root-preserving collection can reclaim genuinely dead outputs. Keeping them retains reuse but occupies space. No profile pruning was performed. |
| Downloaded media | 63.58 GB | Container last changed3 October; uniqueness against other copies not audited. | Deleting selected media frees space but loses the local viewing copy. Keeping it preserves the library. |
| Builder shared offload area | 61.63 GB total, **not all disposable** | Contains current deployment-tool work. Old-looking names are not sufficient evidence. | Archive/remove only individually released work. Keeping it preserves source, evidence and reuse. |
| Builder home build/source copies | Up to23.62 GB across the three collections above, **not all confirmed outputs** | Exact current dependency confirmation requested; no unique-source comparison completed. | Clearing only released compiler targets would retain source but require recompilation. Keeping them preserves reuse. |
| Private repository collection | 19.57 GB | Container last changed19 October; local-only work unknown. | Requires a separate private inventory/backup decision. Keeping it protects material that may exist nowhere else. |
| Browser/model/runtime caches | Up to10.98 GB total | Some tools are currently active. Browser/runtime cache directories range from July to18 November; modification age does not prove disuse. | Removing selected caches may trigger downloads or break a running tool's expected files. Keeping them avoids that disruption. No unused-tool claim was established. |
| Archived Codex recordings outside the requested session roots | 8.79 GB | Archive containers changed30 October,31 October and8 November; individual retention/backup status not audited. | A separate archive-retention decision could remove older history. Keeping it preserves reopenable records. |
| Main workspace working records | 3.30 GB total, **not established as disposable** | Only two tiny directories,32 KB combined, had every examined entry older than a month. Most old-looking records have newer file timestamps. | Requires a retention/ownership decision, not deletion by an old-looking name. Keeping it retains the working record. |
| Old primary version-control backup (`/home/li/.primary-old-vcs-01e496`) | 2.80 GB | Container changed2 October.7181 changed/untracked status items and10 branch commits absent from recorded remote refs: potentially unique work. | Preserve/backup and compare before considering removal. Keeping it protects those changes. |
| Older home worktrees (`/home/li/worktrees`) | 1.05 GB | Directory changed18 November; contains checkouts with local changes/unpublished work. | Integrate/backup individually before removal. Keeping preserves work not proven elsewhere. |
| Stale workspace backup (`/home/li/primary-stale-backup-01e496`) | 0.688 GB | Directory changed2 October; not a standalone Git repository, uniqueness unknown. | Compare/backup before deletion. Keeping preserves a possible recovery copy. |
| Another old workspace collection (`/home/li/wt`) | 0.527 GB | Directory changed3 November; uniqueness varies by checkout and is not fully resolved. | Review individually; do not erase the collection wholesale. |
| Main workspace Git history | 0.293 GB |346 branch commits absent from recorded remotes and208 changed/untracked status items in the working tree. | Only the proposal below is offered. Keeping history costs much less than the working records and avoids coordination risk. |
| Old store-migration scratch (`/home/li/scratch-store-migration`) | 0.038 GB | Directory changed28 October; unique work unknown. | Compare/backup before removal; keeping it costs little. |
| Older secondary, tertiary and quaternary workspace links | Targets0.010,0.0034,0.0032 GB | Links changed14 September. Their targets were clean with no branch work absent from recorded remote refs, but that alone is not fresh remote proof of every reference. | Removing the links would save essentially no space; target removal still requires the full safeguards. Kept. |
| Temporary Claude configuration files | 0.0078 GB,38 files | Latest file change17 November; uniqueness/active writer not established. | Removing confirmed stale copies would save little. Kept as a finding, not treated as transcript/temp-directory authority. |
| Old user-profile generations |106 links; recoverable closure size **not measured** | Latest link change18 November. Shared store contents mean adding per-generation sizes would double-count. | Pruning generations needs an explicit rollback-retention choice. Keeping them retains rollback and roots their software. |

## Main history: archive-and-restart proposal only

The current Git directory is **about293 MB**, not several gigabytes. Its packed objects account for about240 MB; the rest is loose objects and metadata. Rewriting history therefore has a limited immediate disk benefit compared with scratch cleanup.

If you want a fresh beginning:
1. Pause writers and inventory every branch, tag, local-only commit, worktree and changed/untracked file. Keep private material private; a history archive is not permission to publish secrets or private files.
2. Make a complete recoverable archive, including local references and working changes. Upload the approved full history to a GitHub archive repository/branch with the intended access controls. Verify it by a fresh restore and reference/content checks before removing anything locally.
3. Prepare a separate clean repository from the approved current files, with one new initial commit. Review ignored/untracked files deliberately; they are not automatically included.
4. Agree the new canonical remote/branch and update every dependent worktree/tool together. Switch only after verification and approval; retain the old archive until the new workspace is proven.
5. Then retire the old local history and explicitly obsolete worktrees. Do not force-rewrite a shared branch while flows are working.

**None of this was done.** The existing workspace, history, branches and active work remain in place.

## What went right, what did not, and the practical result

- **Worked:** the laptop recovered about25 GB without touching active deployment work or deleting verified unique source changes. Remote verification prevented stale local “pushed” markers from being treated as sufficient proof.
- **Held safely:** uncertain repositories/worktrees, retained evidence, private data, profile generations and active-tool material. The cleanup did not stop, restart or reconfigure the running services.
- **Initial permission refusals:** three old scratch residues needed a root retry; those were then removed after fresh checks. The uncertain plugin-cache residue was kept.
- **Not finished:** garbage collection on both hosts and the builder's old active-project target caches. Required build caches are not all rooted, and the deployment test has priority. No builder-space gain is claimed. The builder store-size scan was stopped to avoid competing with that test.
- **No automated resource monitor was installed.** This was a guarded one-time cleanup, not a new retention system.

## Existing cleanup knowledge and operator records

The authored repository policy says to preserve dirty/unpushed work, use shallow clones and remove unused checkouts only after a configured age; that age/timer has not been configured. The new direct cleanup order supplied authority for this run instead. The build policy says shared build outputs belong on the builder and worthwhile builds need registry roots. No ready-made guarded cleanup procedure was found in the bounded authored knowledge/vision search; unrelated code-level cleanup references were not treated as a host-cleanup procedure.

Full measured inventories, retained-work reasons, remote verification and removal receipts are in the operator evidence directory (`/tmp/ebfp-disk-a4f252.Z7wc4TDJ`). Those machine-readable lists retain the individual paths; the plain-English summary above does not require looking up technical identifiers. No credentials were printed and private audit contents were not inspected.
