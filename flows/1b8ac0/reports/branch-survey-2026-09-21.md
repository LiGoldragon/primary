# Branch survey across the flow repositories, 2026-09-21 (PsycheHigh 1b8ac0)

Read-only survey by a subflow of 1b8ac0 on the living's instruction to merge every flow branch; no merge was performed here.

## Survey: branches vs. main across the flow fleet

**Scope note:** primary has 99 non-main refs (73 local heads + 26 remote-only). Of these, 41 are already fully contained in main (`ahead=0` — stale/already-merged, safe to prune, nothing to merge). The table below covers only refs with commits **ahead** of main. Conflict = `git merge-tree main <ref>` producing conflict markers (no writes performed).

### Primary (`/home/li/primary`, local heads)

| branch | tip | ahead | owning flow | conflicts | note |
|---|---|---|---|---|---|
| flow/cf7879 | 6764621 | 162 | cf7879 | yes | flow-log branch, large divergence, likely superseded by main's own log |
| worktree-flow-840e42 | ac3682f | 78 | 840e42 | no | worktree branch, clean vs main |
| proposal/cf7879-core-e43002 | b22c4e4 | 67 | cf7879 | yes | unlanded proposal |
| proposal/cf7879-core-bootstrap | eddca4a | 65 | cf7879 | yes | unlanded proposal |
| flow/5f4fea | 88a0586 | 51 | 5f4fea | yes | flow-log branch |
| proposal/cf7879-flow-events-poc | f26d073 | 39 | cf7879 | yes | unlanded proposal |
| proposal/5f4fea-flow-assembler-full-context | 46c6bae | 38 | 5f4fea | yes | unlanded proposal, has its own worktree |
| proposal/5f4fea-item30-launcher | 321050f | 37 | 5f4fea | yes | unlanded proposal, own worktree |
| flow/fd0f97 | fb6e00b | 37 | fd0f97 | yes | flow-log branch, own worktree |
| proposal/5f4fea-disk-retention | f6b6c47 | 33 | 5f4fea | yes | unlanded proposal, own worktree |
| proposal/cf7879-overnight-queue-20260916 | 219b4b9 | 18 | cf7879 | no | clean, mergeable |
| proposal/cf7879-core-checkup-advisory-lock | 37ed03c | 15 | cf7879 | yes | unlanded proposal |
| proposal/cf7879-flow-idleness-subscription | ef7b77f | 14 | cf7879 | yes | unlanded proposal |
| proposal/cf7879-core-heartbeat | 99285db | 11 | cf7879 | yes | unlanded proposal |
| flow/05c604 | 7f7e80f | 11 | 05c604 | yes | flow-log branch |
| proposal/cf7879-clusterrelay-context | bbfbd9e | 10 | cf7879 | yes | unlanded proposal |
| flow/05c604-secondary-page | 8dfa630 | 9 | 05c604 | yes | secondary flow log |
| proposal/cf7879-core-harness-facts | fcfb644 | 7 | cf7879 | no | clean, mergeable |
| core-checkup-cf7879 | 13fb3c4 | 7 | cf7879 | no | clean, mergeable |
| field/rollout-plan-9ddcbc | 5e55205 | 5 | 9ddcbc | no | own worktree, clean |
| proposal/cf7879-claude-prompt-hook | feb5a5a | 4 | cf7879 | yes | unlanded |
| proposal/cf7879-prompt-relay-datom | 9caafa8 | 3 | cf7879 | yes | unlanded |
| proposal/cf7879-relay-gate | f360469 | 2 | cf7879 | yes | unlanded |
| proposal/cf7879-claude-successor-840e42 | 6b00dbc | 2 | cf7879/840e42 | no | clean, mergeable |
| group-17-5f4fea | 72e9ee7 | 2 | 5f4fea | no | clean, mergeable |
| flow/cf3553-native-launch-fix | 3383916 | 2 | cf3553 | yes | unlanded |
| field-census-9ddcbc | fdb2c1c | 2 | 9ddcbc | yes | own worktree |
| push-zktzqrzzwkxt | e8cf380 | 1 | unknown | yes | stray push-* staging branch |
| push-ktnnmzyuyknz | 4df1691 | 1 | unknown | yes | stray push-* staging branch, huge behind (2376) — very stale |
| proposal/cf7879-wake-adapter | 17100b4 | 1 | cf7879 | no | clean, mergeable |
| proposal/cf7879-primary-jj-global-law-v2 | 1b88c52 | 1 | cf7879 | no | clean, mergeable |
| integration-deployment-4a8046-meter200 | c29f8e4 | 1 | 4a8046 | yes | old deployment-tracking branch |
| flow/eae736 | 197997d | 1 | eae736 | no | own worktree, clean |
| field-checkup-shadow-9ddcbc | 244f338 | 1 | 9ddcbc | yes | own worktree |
| draft/5f4fea-g11g12 | ef9cf86 | 1 | 5f4fea | no | own worktree, clean |

### Primary (remote-only, `origin/*` with no local head)

| branch | tip | ahead | owning flow | conflicts | note |
|---|---|---|---|---|---|
| flow/efa157 | 5cad440 | 91 | efa157 | yes | flow-log |
| proposal/cf7879-claude-successor-v5 | 74168f0 | 90 | cf7879 | yes | unlanded |
| flow/840e42 | ac3682f | 78 | 840e42 | no | clean, mergeable |
| flow/48cff7 | 973f1d9 | 33 | 48cff7 | no | clean, mergeable |
| worktree-flow-48cff7 | ad36526 | 23 | 48cff7 | no | clean, mergeable |
| flow/d9961c | 7baf5b2 | 21 | d9961c | yes | flow-log |
| proposal/cf7879-core-checkup-hardened-20260915 | d3002f4 | 12 | cf7879 | no | clean, mergeable |
| proposal/cf7879-core-checkup-recovery-20260915 | fbdc399 | 11 | cf7879 | no | clean, mergeable |
| proposal/cf7879-native-launch-stdin-proof | 3ae16d9 | 9 | cf7879 | no | clean, mergeable |
| claude/workspace-agent-remote-access-zjj9rb | 6a4395a | 6 | zjj9rb | yes | unlanded |
| preserve/toolchain-stash-codeworkspace-20260716 | 620b727 | 5 | archived toolchain | yes | archival stash, not live work |
| proposal/6852f4-schema3-audit-evidence | 70ab4eb | 4 | 6852f4 | no | clean, mergeable |
| draft/5f4fea-g11g12-item11 | 2c8d852 | 4 | 5f4fea | yes | unlanded |
| preserve/toolchain-rescue-primary-dirty-2026-05-18-20260716 | c5a2a20 | 3 | archived | yes | archival, ~5.5k behind — do not merge |
| proposal/f55ec8-codex-quota-reset | 305d85e | 2 | f55ec8 | yes | unlanded |
| proposal/cf7879-codex-layer-access | 0b4f393 | 2 | cf7879 | no | clean but ~6.2k behind — very stale base |
| preserve/toolchain-push-counselor-spirit-privacy-migration-2026-06-04-20260716 | c5b95c7 | 2 | archived | yes | archival |
| proposal/f55ec8-model-flow-anatomy | 5f843fd | 1 | f55ec8 | yes | unlanded |
| proposal/b49251-claude-quota-observe | a602f35 | 1 | b49251 | yes | unlanded |
| preserve/toolchain-system-operator-report-182-20260716 | 94d0484 | 1 | archived | yes | archival |
| preserve/toolchain-push-assistant-spirit-privacy-test-2026-06-04-20260716 | 8eb2373 | 1 | archived | yes | archival |
| preserve/toolchain-pi-agent-0d7ca3f4-5ec3-411-20260716 | abafc01 | 1 | archived | no | archival, but clean/mergeable technically |
| preserve/toolchain-accidental-overbroad-open-work-2026-06-03-20260716 | 5b61163 | 1 | archived | yes | archival |

(41 other primary refs are `ahead=0` — fully merged already, prunable, nothing to do.)

### Repos under `/git/github.com/LiGoldragon/` touched since 2026‑09‑19 — recent (≥2026‑09‑19) unmerged branches

Every one of the surveyed repos (Curriculum, message, flow, lojix, signal-lojix, meta-signal-lojix, meaning-language, CriomOS, CriomOS-home, goldragon, horizon-rs, transcript, curriculum-deploy) also carries dozens of older stale branches (May–Sept 17), same pattern as primary — mostly already fully merged or long-abandoned. Table below is just the ones with activity in the last two days:

| repo | branch | tip | ahead | owning flow | conflicts | note |
|---|---|---|---|---|---|---|
| message | night-messaging-message-delivery-f72ab7 | 580021b | 3 | f72ab7 | no | remote-only, clean, mergeable |
| message | night-messaging-delivery-gate-draft-f72ab7 | 8a6e88f | 2 | f72ab7 | no | remote-only, clean, mergeable — earlier draft of the above |
| flow | night-messaging-flow-delivery-store-f72ab7 | 1b57de0 | 4 | f72ab7 | no | remote-only, clean, mergeable |
| flow | night-messaging-0ab019 | e387576 | 1 | 0ab019 | no | remote-only, clean, mergeable |
| lojix | lojix-horizon-contract-7091ea | ac672da | 2 | 7091ea | yes | 7 behind main too — needs rebase before merge |
| lojix | proposal/remote-builder-fallback-false | 476bc56 | 1 | unclear | no | 7 behind, clean apply |
| lojix | proposal/horizon-contract-repin-8565e8 | 3411570 | 1 | 8565e8 | no | remote-only, clean, mergeable |
| signal-lojix | lojix-horizon-contract-repin-8565e8 | 3f550fc | 2 | 8565e8 | yes | 2 behind, conflicts |
| meta-signal-lojix | lojix-horizon-contract-repin-8565e8 | a2a42e9 | 2 | 8565e8 | yes | 2 behind, conflicts |
| CriomOS | usb-gateway-consumer-6db4fe | 9842f51 | 1 | 6db4fe | no | remote-only, clean, mergeable |
| CriomOS-home | field/flow-message-consumers-9ddcbc | e1096a16 | 1 | 9ddcbc | no | clean, mergeable |
| horizon-rs | usb-gateway-6db4fe | 37416e1 | 2 | 6db4fe | yes | 19 behind main — stale base, needs rebase |

Curriculum, meaning-language, goldragon, transcript, and curriculum-deploy have **no** branches with commits since 2026‑09‑19 that aren't already main.

### Do flows all branch off primary/main?

No — mixed picture:
- Not every "flow branch" is a divergent line of work; many (`ahead=0`) are just old pointers that have since been fully merged into main and left dangling.
- Every repo carries a long tail of `preserve/*`, `push-*`, and old `proposal/*` branches from May–August that are either archival snapshots or abandoned proposals, several hundred to several thousand commits behind current main — these are not "pending merges," they're historical residue.
- The real live-work branches (created this week, low ahead-count, mostly clean) sit on top of *current* main in message, flow, lojix-family, CriomOS, CriomOS-home, and horizon-rs — those do branch off primary/main correctly.

### Worktrees / clones vs. the shared checkout

Confirmed extensively — flows routinely do **not** work directly on the shared checkout's main:
- primary itself: `/home/li/wt/primary-*` (5f4fea family, cf7879, eae736, fd0f97), `/home/li/wt/primary/field-*-9ddcbc` (three), `/home/li/wt/github.com/LiGoldragon/primary/field-6db-report-20260921`, `/home/li/primary/.claude/worktrees/flow-840e42`, `/home/li/.codex/worktrees/8673` and `/e217`, and `/tmp/field753-primary-oVpaNZ`.
- Curriculum: two active worktrees for `fix/5f4fea-main-flow-execution-boundary` and `fix/5f4fea-main-subflow-execution-boundary`, plus a detached `flow-aspect-7e8542` checkout.
- CriomOS: a `/tmp/core-checkup-criomos-consumer` worktree.
- horizon-rs: a `horizon-opencode-7e8542` worktree.
- curriculum-deploy: a `ProtoformStack` worktree.

### What's mergeable now (clean, positive ahead-count, current base)

message: night-messaging-message-delivery-f72ab7, night-messaging-delivery-gate-draft-f72ab7 · flow: night-messaging-flow-delivery-store-f72ab7, night-messaging-0ab019 · lojix: proposal/horizon-contract-repin-8565e8 · CriomOS: usb-gateway-consumer-6db4fe · CriomOS-home: field/flow-message-consumers-9ddcbc · primary: proposal/cf7879-overnight-queue-20260916, proposal/cf7879-core-harness-facts, core-checkup-cf7879, field/rollout-plan-9ddcbc, proposal/cf7879-claude-successor-840e42, group-17-5f4fea, proposal/cf7879-wake-adapter, proposal/cf7879-primary-jj-global-law-v2, flow/eae736, draft/5f4fea-g11g12 (local); flow/840e42, flow/48cff7, worktree-flow-48cff7, proposal/cf7879-core-checkup-hardened-20260915, proposal/cf7879-core-checkup-recovery-20260915, proposal/cf7879-native-launch-stdin-proof, proposal/6852f4-schema3-audit-evidence (remote-only).

### What's not mergeable now, and why

- Conflicting (yes column) — most `proposal/cf7879-*` and flow-log branches in primary, plus lojix-horizon-contract-7091ea, both lojix-horizon-contract-repin-8565e8 branches (signal-lojix, meta-signal-lojix), horizon-rs usb-gateway-6db4fe: real textual conflicts against current main, need manual resolution.
- Stale base (large "behind" counts, hundreds to thousands of commits) — the `preserve/toolchain-*` branches (2026-05/06 origin) and `push-*` staging branches in primary, plus most of the July/May-dated branches across CriomOS, CriomOS-home, lojix, signal-lojix, meta-signal-lojix: these predate large chunks of current main; even the conflict-free ones (e.g. `proposal/cf7879-codex-layer-access`, ~6.2k behind) are answering questions main has since moved past — a straight merge would be low-value/high-risk without re-review, not a mechanical fast-forward.
- Already-merged (ahead=0) — 41 primary refs plus similar counts elsewhere: nothing to merge, just dangling pointers.

Underlying data: `/tmp/branch_report.tsv` (primary local), `/tmp/remote_report.tsv` (primary remote-only) — both left in the scratchpad, not committed anywhere.

## Sources

- `/home/li/primary` (git branch -a, jj bookmark list, git merge-tree dry runs)
- `/git/github.com/LiGoldragon/message`
- `/git/github.com/LiGoldragon/flow`
- `/git/github.com/LiGoldragon/lojix`
- `/git/github.com/LiGoldragon/signal-lojix`
- `/git/github.com/LiGoldragon/meta-signal-lojix`
- `/git/github.com/LiGoldragon/meaning-language`
- `/git/github.com/LiGoldragon/CriomOS`
- `/git/github.com/LiGoldragon/CriomOS-home`
- `/git/github.com/LiGoldragon/horizon-rs`
- `/git/github.com/LiGoldragon/transcript`
- `/git/github.com/LiGoldragon/curriculum-deploy`
- `/git/github.com/LiGoldragon/Curriculum`
- `/git/github.com/LiGoldragon/goldragon`
