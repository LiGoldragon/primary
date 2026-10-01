# Worktree and commit audit — 2026-09-30

**Authority and scope.** Main Flow `1bc255` delegated this evidence report after
an independent worktree review. It is an observation record for the captain and
Mind. It does not authorize cleanup, `jj workspace forget`, `jj abandon`, branch
deletion, GC, reflog expiry, or moving a bookmark.

**Time bounds.** Local primary inspection was run at
`2026-09-30T19:24:40-06:00`; the report also incorporates the read-only
`handoff_witness` filesystem survey and the bounded `messenger_route` ref audit
run about 19:20–19:30 local during this task. Paths and refs can change after
those observations.

## Commands and roots inspected

On `/home/li/primary` the local audit used:

```sh
jj workspace list
jj status
jj bookmark list --all
jj log -r 'all() & ~::main'
jj op log -n 20
find /home/li/wt -type d -name .jj -printf '%h\n' | sort
```

It checked each primary temporary workspace with `stat`, `jj -R <path> log -r
'@|@-' -n 2`, and `jj -R <path> status --quiet`. The wider survey enumerated 77 filesystem Jujutsu workspaces and 46 linked-root
registry entries. No registration was found outside `/git`, `/home/li/wt`, and
`/tmp`; broken/no-working-copy roots prevent a complete all-repository result.
The filesystem workspaces include these repository groups: `primary`; CriomOS (4); CriomOS-home
(11); Curriculum (3); HackingMessenger/HackyMessenger (4); datomic (3); Field
(1); Flow (24); Messenger-related repositories (13); listener (2); plus
single workspaces for Goldragon, harness, persona-test, plannotator,
claude-hijack-stock, codex-hijack, and Lojix's concluded-workspace directory.
This is a path inventory, not proof that every filesystem directory has a
healthy backing repository.

The ref auditor additionally used Jujutsu workspace/bookmark/log/operation
views and Git's `for-each-ref`, reflog, and fsck in primary and representative
canonical repositories. Those commands were read-only.

## Primary repository at the observation boundary

`jj workspace list` showed eight registered primary workspaces:

| Workspace | Exact path | Observed working-copy state |
| --- | --- | --- |
| `1bc255-record` | `/home/li/wt/primary/1bc255-record` | Main-owned dirty `flows/1bc255/log.md` and added `flows/1bc255/vision/stateful.md`; this audit did not touch either. |
| `b666e7-defect` | `/tmp/primary-b666e7-defect.dJngRs` | Empty working copy; parent `0c3473259e0b` under bookmark `b666e7-source-defect-fix`. |
| `b666e7-fable` | `/tmp/primary-b666e7-fable.IfRHAN` | Empty; parent `8ca8eaa3ca28`, `b666e7-fable-composition`. |
| `b666e7-latest` | `/tmp/primary-b666e7-latest.7yp34R` | Empty; parent `7561d28f53e5`, `b666e7-basehost-dry-activate`. |
| `b666e7-publish` | `/tmp/primary-b666e7-publish.aNCVZ2` | Empty; parent `147b73a29cb4`, `b666e7` observer-deployment gate record. |
| `b666e7-start` | `/tmp/primary-b666e7-start.jDhpsh` | Empty; parent `74c55635d9b0`, `b666e7-transient-start`. |
| `primary-1bc255-log-9207` | `/tmp/primary-1bc255-log-9207` | Empty; parent `9100575c8445`, Field Sol launch handoff. |
| `default` | `/home/li/primary` | Substantial concurrently owned dirt; see limits. |

The exact publish path contains the trailing `Z`: it existed at the audit
boundary with mtime `2026-09-29 17:36:21-06:00`. The similarly named path
without the `Z`, `/tmp/primary-b666e7-publish.aNCV2`, was absent. The earlier
missing-path report omitted that final character; it is not evidence of a
removed workspace.

## Durability and recovery classification

| Class | Evidence | Interpretation |
| --- | --- | --- |
| Durable published refs | `jj bookmark list --all` showed `main` and numerous `@origin` bookmarks. Examples relevant to this audit include Field polling source commit `310f5ba49c9a0aa2331298bf4c64bf1db033d239` on its matching origin bookmark and CriomOS `d12e46c2ae17` on `integration-b7da5d-criomos-home-017@origin`. | These are ref-retained. Their existence does not make their associated worktrees disposable. |
| Registered workspace heads | The eight primary workspace heads above, CriomOS-home `e4b6df5a`, and Flow `da65ede4` are held by registered workspaces. | They are not “lost commits.” Owner confirmation is required before any conclusion or cleanup. |
| Operation/reflog recovery | `jj op log -n 20` retained recent commit, rebase, bookmark, push, and workspace operations. Primary has 142 local heads, 205 remotes, no tags, and 38,537 `refs/jj/keep`. Git fsck found 57 Git-unreachable commit objects with reflogs considered and 104 with `--no-reflogs`; the difference, 47, is reflog-only recoverable. | These counts show a recovery surface, not permission to rewrite or expire it. No expiry, GC, or restoration was run. |
| Git fsck candidates awaiting Jujutsu-history classification | Primary fsck named `038211b2a4c43b94dcb362e999c8f02cadfa40a1`, `4d0f58edc4ac0bd8ec68b32a65ebda3a023cbda6`, `7518b8e5d080f2ffcbdb70abf1d430a398a1870b`, and `01ed5aba5a0b8fd69dd0fd222a67e282d210364f`; targeted Jujutsu lookup found none. Flow fsck named six stash-style candidates: `368579d812d9b22edfab591d33324c0d249c9608`, `06a676a16cd20f8ea5a85ea1187a0fdd9f2139c2`, `f3af621a675deb63dd58ce58482ee3da8d4f8d0b`, `2ff117d37eedc5e4d216af68d37d858b5809850f`, `a4361799e274b71f91b7f539e1b8519cbf964189`, and `c99cb9f9c7ba42bf969c4fa7ca5a62c36d305473`. | Git-unreachable does **not** mean lost or genuinely unreferenced while Jujutsu operation/history checks remain incomplete. Preserve object IDs and recovery metadata; this audit establishes neither ownership nor redundancy. |

Canonical CriomOS and Field default fsck runs found zero unreachable commits.
That is bounded evidence for those default repositories, not a statement about
their registered workspaces or every alternate repository root. The complete
57-object primary fsck listing remains in the `messenger_route` transcript; it
is intentionally not copied here as a claim that those objects need rescue.

## Dirty, blocked, and broken leads

| Path or class | Evidence | Why it is not a cleanup candidate |
| --- | --- | --- |
| `/home/li/primary` default workspace | `jj status` refused to snapshot two oversized untracked PNGs under `flows/bd0019/books-situation/`; concurrent dirt spans multiple other flows. | The refused files make normal status incomplete; all content is concurrently owned. |
| `/home/li/wt/primary/1bc255-record` | Main-owned dirty log and `vision/stateful.md`, observed during this report task. | Delegated report work excluded both paths. |
| CriomOS-home `flow-0173-validation-56ae53` | Three dirty logs in sibling survey. | Owner and intended landing unknown. |
| CriomOS-home `flow-0174-stage-56ae53` | Two source modifications; workspace commit `e4b6df5a`. | Registered current workspace commit; source changes need owner review. |
| CriomOS `field-clj-b7da5d-repin` | Commit `d12e46c2`, integration bookmark, flake/Nix work. | Published/integration-referenced work, not redundant. |
| Flow `codex-session-binding-6fe957` | Dirty workspace commit `da65ede4`. | Separate source owner and active change surface. |
| Claude and Codex proposals | Dirty proposal commits `d20c93a9` and `9ad45c28` in sibling survey. | Proposal ownership/landing status not established. |
| CriomOS `usb-observer-carrier-b666e7` | Status blocked by large untracked Rust `target` artifacts; source parent `7cceb6e7`. | Build output prevents a complete working-copy conclusion; do not remove or infer source dirt. |
| HackingMessenger/HackyMessenger (4), datomic (3), concluded Lojix workspace | Linked Jujutsu source metadata points to missing backing roots. | Reachability cannot be fully determined from the broken links. Repair/forensic ownership precedes any forget or deletion. |
| Curriculum docs (3), Flow `claude-launch-cap-removal`, message default | No working-copy commit in sibling survey. | Empty status is not redundancy evidence without source/owner intent. |
| Source-root status boundaries | Handoff witness found CriomOS dirty/unclassifiable because untracked Rust target files make Jujutsu snapshot refuse; Field is dirty with `.9e735b.flow-id.lock`. Curriculum, Flow, listener, message, meta-signal-flow, signal-flow, and signal-message were observed clean at their particular checks. | A point-in-time clean status is not cleanup authority. |
| messenger-clj metadata incident | At 19:26:33, sibling ran `jj -R /git/github.com/LiGoldragon/messenger-clj status`. Jujutsu reported it reset the working-copy parent while importing a pre-existing Git HEAD and refs: `main`/`main@origin` moved `4bce278c` → `990a9333`; WC became empty `1243c0d1` with parent `990a9333`. Operation IDs were `2a1718d07459` (import Git HEAD) and `4e55ec3dbab4` (import Git refs). | No file delta or new commit was proven; the pre-command WC parent was not captured. Do not use the prior clean claim, alter this repository, or infer a correction without owner review. |

## Conclusion and next safe step

No path has both a proven redundant ownerless copy and a separately verified
recoverable durable copy. The appropriate next action is a per-path owner
assignment that records whether to preserve, publish, restore from a named
object/operation, or conclude a workspace. Until then, retain all workspace
registrations, Git objects, reflogs, operation history, untracked build output,
and linked-metadata evidence.
