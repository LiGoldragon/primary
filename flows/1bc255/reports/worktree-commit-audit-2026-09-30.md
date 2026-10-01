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
The filesystem workspaces span `primary`, CriomOS, CriomOS-home, Curriculum,
HackingMessenger/HackyMessenger, datomic, Field, Flow, Messenger-related
repositories, listener, Goldragon, harness, persona-test, plannotator,
claude-hijack-stock, codex-hijack, and Lojix's concluded-workspace directory.
The 77 total is the `find` result; this grouping is deliberately non-additive
because some paths sit under shared repository roots. It is a path inventory,
not proof that every filesystem directory has a healthy backing repository.

The ref auditor additionally used Jujutsu workspace/bookmark/log/operation
views and Git's `for-each-ref`, reflog, and fsck. The Git pass at about 19:30
used no `jj status` command. Its exact bounded scope is shared primary, the ten
canonical Jujutsu-linked Git roots named below, and the fourteen specifically
enumerated Git-only roots below. The broader filesystem contains unrelated and
dependency Git repositories; other Git-only roots were not scanned. All audit
commands were read-only except the separately disclosed messenger-clj Jujutsu
metadata-import incident.

## Git reachability scope and object counts

All figures in this section are **Git commit-object** counts, expressed as
`default fsck / fsck --no-reflogs`; a zero is bounded to the named root. Git
heads/remotes/tags are shown as `h/r/t` where collected.

| Canonical Jujutsu-linked root | Commit candidates | Boundary |
| --- | --- | --- |
| CriomOS | 0 / 0 | Default root only; its active source workspace has separate untracked-build-output limits. |
| Curriculum | 11 / 12 | Git candidates need owner/history attribution. |
| field | 0 / 0 | Field source remains separately dirty. |
| flow | 6 / 6 | Six are stash-style commit subjects, not established loss. |
| listener | 0 / 0 | Bounded default-root check. |
| message | 0 / 0 | Bounded default-root check. |
| messenger-clj | 0 / 0 | Git check at 19:26:33; separate Jujutsu import/reset incident below. |
| meta-signal-flow | 0 / 0 | Bounded default-root check. |
| signal-flow | 0 / 0 | Bounded default-root check. |
| signal-message | 0 / 0 | Bounded default-root check. |

For shared primary, default `git fsck --unreachable` counted **57 commits,
12,100 trees, 104 blobs, 0 tags**. `--no-reflogs` counted **104 commits,
12,244 trees, 772 blobs, 0 tags**. The **47 difference applies only to commit
objects** and identifies reflog-only recoverability at this counting boundary.
Flow's six candidate commit objects had the same count in both modes (6
commits, 91 trees, 6 blobs, 0 tags). These type counts do not establish that
any object is ownerless or ready for deletion.

### Git-only roots, outside the Jujutsu-linked set

These 14 roots have no sibling `.jj` evidence in this survey. Each was checked
with `git for-each-ref`, `git reflog show --all`, and both fsck modes; `git
status` was deliberately not run, so **untracked state is Unknown**.

| Root(s) | Heads/remotes/tags | Commit candidates | Result |
| --- | --- | --- | --- |
| `/git/.../Ashtadhyayi` | 1 / 1 / 0 | 0 / 0 | Bounded Git-only check. |
| `/git/.../nixpkgs` | 0 / 0 / 0 | 0 / 0 | Bounded Git-only check. |
| `/git/.../release-train-dogfood/checkouts/{content-identity,core-schema,name-table,raw-discovery,structural-codec,structural-codec-derive}` | each 1 / 2 / 0 | each 0 / 0 | Six bounded Git-only checks. |
| `/git/.../signal-5f4fea-word-identifiers` | 8 / 6 / 0 | 0 / 0 | Bounded Git-only check. |
| `/home/li/wt/.../CriomOS/{bootstrap-piperless-31147a,step2-piperless-31147a,tailnet-restart-trigger-56ae53}` | each 98 / 104 / 0 | each 0 / 0 | Three bounded Git-only checks. |
| `/home/li/wt/.../CriomOS-home/flow-0173-stage-56ae53-5ba2e1e` | 117 / 124 / 0 | 0 / 3 | Same three reflog-only commits as the next row. |
| `/home/li/wt/.../CriomOS-home/remove-piper-31147a` | 117 / 124 / 0 | 0 / 3 | Same three reflog-only commits as the prior row. |

The three Git-only CriomOS-home candidates are
`da1ed221af78df4f49233c47e0898e1daa64df76` (`Exercise packaged Message
configuration writer`), `0194fdab0746a663557ed6add85fb2b9402d855a` (`Fix
Message startup configuration Datom`), and
`17e00d9969cb57e4c45690677c7fbf000b6c8792` (`Home: create OpenCode scratch
before service start`). They occur only when reflogs are ignored, hence are
reflog-recoverable rather than evidence that a commit is lost.

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
| Operation/reflog recovery | `jj op log -n 20` retained recent commit, rebase, bookmark, push, and workspace operations. Primary has 142 local heads, 205 remotes, no tags, and 38,537 `refs/jj/keep`. Its Git fsck commit count is 57 with reflogs considered and 104 with `--no-reflogs`; the 47 difference is reflog-only recoverable. Exact type counts are in the reachability table above. | These counts show a recovery surface, not permission to rewrite or expire it. No expiry, GC, or restoration was run. |
| Git fsck candidates awaiting Jujutsu-history classification | Primary fsck named `038211b2a4c43b94dcb362e999c8f02cadfa40a1`, `4d0f58edc4ac0bd8ec68b32a65ebda3a023cbda6`, `7518b8e5d080f2ffcbdb70abf1d430a398a1870b`, and `01ed5aba5a0b8fd69dd0fd222a67e282d210364f`; targeted Jujutsu lookup found none. Flow fsck named six stash-style candidates: `368579d812d9b22edfab591d33324c0d249c9608`, `06a676a16cd20f8ea5a85ea1187a0fdd9f2139c2`, `f3af621a675deb63dd58ce58482ee3da8d4f8d0b`, `2ff117d37eedc5e4d216af68d37d858b5809850f`, `a4361799e274b71f91b7f539e1b8519cbf964189`, and `c99cb9f9c7ba42bf969c4fa7ca5a62c36d305473`. | Git-unreachable does **not** mean lost or genuinely unreferenced while Jujutsu operation/history checks remain incomplete. Preserve object IDs and recovery metadata; this audit establishes neither ownership nor redundancy. |

Canonical CriomOS and Field default fsck runs found zero unreachable commits.
That is bounded evidence for those default repositories, not a statement about
their registered workspaces or every alternate repository root. This report names four primary samples only; the complete 57-object listing is
relayed separately in the `messenger_route` transcript and is not a preservation
claim. Jujutsu operation attribution and broken/no-working-copy roots remain
separate Unknowns.

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

## Appendix: Git-unreachable commit candidate manifests

These are **Git-unreachable commit candidates at the audit boundary; they are
not classified as lost, ownerless, or removable.** The lists retain evidence for
future owner and Jujutsu-history attribution.

### Shared primary: 57 candidates with reflogs considered

```
7518b8e5d080f2ffcbdb70abf1d430a398a1870b
eb3bb8c6b2afbe42682449fd3bcf93fdec85500e
9d3e70106bbae3f92439ba1d3a9a6ab37fb714be
854da07368d4052f5f9ec148df7e6d1eb9baa2ae
045580096545ea036d3859140a65f586754185f2
bc64e010ee155f05c6b25597186289dbcb3a9b51
166f00090a3030f2f3c63b95f2044372820fbaab
4408f99cfb5f712b6af740bd69d1ae04a3966234
a00fc1aeba7108b17aba5648c083862dc74247f5
eb3141932bcf01579065d62b456f6c1062b4f703
e851c99f51eb5cc401fd5c6490c911d7960e9bc8
085949f6a0b8a3067f90c9382b9369f93c207697
7963693a04dbdcfe53f08e7ece2ff849b35a6540
5b77315b8881cf9b1d83088c6124afb9d1019da6
bd78e12e9ccd34fb4215c90e27a7a6a663cc398f
038211b2a4c43b94dcb362e999c8f02cadfa40a1
ca92b906eb6e87503074d88bd5069fb3a9ddc58d
761ffaf5628ed281c1376e7e4f7cab690beea7dc
162d22101bcd3178387f919df9a327966f82800c
0b57c2f1271e6cafbf6c5ee3f97e37d152e58255
896eaa4c301abb5a039bbfe6b3bcc677311ec742
daf232449f5efc74e91ac7ba406cab108cd8eda1
59fcdaadbbbccf155235abc5ad21c3959d63d5e2
132b0b527e09ce0bf956a2161e98359c6b4974ee
a13c333abf924cf96f1b051db6a3310dae81dd43
ebab430bad591336613b1dc4335484515b401ac8
d5b2fb88f12267f48586a524ce34acdcef6ccf68
c3eefbf663d7c5508b92de0179ab9d29b6f00feb
2d0ebc6b937dce6e48fc131e03d9fbc8ae5541ee
2a193433d27ef838913881302e0ba013a4dfe9ff
b356e4f670092b03e7de297ea12976a80f999d6b
4f68f49dd04a9ffea0e32e85d5f51d53b4f300ff
cca084e7a5ce63c72d0ca21c86076e047d8fa2ca
62be04fa8ae089e7963c8ea2f178484e7f5f2eee
6ac3fc609031fa0e3b61f341a0146308bdc8271e
1920c539b30d189ec2c70c1ed863217482e9203a
18358dbd39edff92ebaa22531f9b93b5c162c7b1
834f657b56a36b7025c7d0f9d4dfe07636d648f7
4c9e957c16da04cd5df126964b69797238a65a6d
66d7b514e4178ec590b725eb4d3118d482c74c31
22de6d37dda9b7e339eec787b9eda91b129541c3
d4193682053a7b58e37bd7968023fd025f338943
5a4426c10ca841e2ca5d517328599a66466d8935
8e472e422a86756c9737a498f6e9c2a1c4cc0d6a
234a06101797febe5d9d8c28b8f4c4cc0aa535be
33736e08379ae7571fd911b674133829ef9376ef
8bb3ce8df2d6817c652008a4319cefe02d58181e
a3e1b6a0304ae0cb50fc6bfc12a68c22ad6c5a10
04f4ae59f6ff32f2a6f357aa8aa3a14f1fca9262
39fddefe0c65e72ee22defadb83529b295d1ed31
2503cf9a8c4864f794115543e6d5c468734ac3d6
b01a0f67a88ae8773b22e5de5bd7ba2299afa34c
d32a4ffa4dc7a63574b53062180513d00e7096f6
24424f5b382341b1a2964562cdd761e5509b6f28
c8664fe09f9957658f03ab7236f6b70b78bb66a1
278dc7002be2e87afb222c9440596efdc9a5f2c7
3f8ea7a5aba9845fd4c576d395c12c227fbefeed
```

### Curriculum: 11 default candidates; one additional when reflogs ignored

Default 11:

```
2702dabd2e8da2bba280670bd8f02c1ddbe97480
81a06616f11a90d8719da2e35727c8c8f4f52f12
9cadad6b595c21ce7ef1ca61a74ff0272cdc8cbf
fc346acd58bac4547c1c6ab9df6f011a146cfed0
01ba2e39592a41cef095f6c2251f46e25a443675
f8beb439d74912b974d103a520e490aa8ac967e9
cc4b4dad381676460eb36881bd86388c44e5b1db
5e4e2e5bc4e5046a628b1ed19e5309a671e1696c
4c667f434bef5818eecd881ae040a8434724c66f
f6ecea74a74589a8f933d4789c9082b38bfab5f0
ac7d07122e121f7753c87b4eb05ca1a5bae89d2b
```

`ac22bbf90e67333f848e99e2c9d1633f94ee7784` appears only with
`--no-reflogs`, so it is reflog-only recoverable. All 12 require owner and
Jujutsu attribution.

### Flow: six candidates in both modes

```
368579d812d9b22edfab591d33324c0d249c9608
06a676a16cd20f8ea5a85ea1187a0fdd9f2139c2
f3af621a675deb63dd58ce58482ee3da8d4f8d0b
2ff117d37eedc5e4d216af68d37d858b5809850f
a4361799e274b71f91b7f539e1b8519cbf964189
c99cb9f9c7ba42bf969c4fa7ca5a62c36d305473
```

## Conclusion and next safe step

No path has both a proven redundant ownerless copy and a separately verified
recoverable durable copy. The appropriate next action is a per-path owner
assignment that records whether to preserve, publish, restore from a named
object/operation, or conclude a workspace. Until then, retain all workspace
registrations, Git objects, reflogs, operation history, untracked build output,
and linked-metadata evidence.
